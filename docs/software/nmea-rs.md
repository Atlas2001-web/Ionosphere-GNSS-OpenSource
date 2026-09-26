# nmea（AeroRust）· Rust NMEA 0183 解析库操作手册

目录：上游 <https://github.com/AeroRust/nmea>（AeroRust 组织）· crates.io **`nmea` 0.8.0**（2026-08-08 08:34 EDT 发布；总下载 **193018**，近 90 天 **40131**）· crate 内 `.cargo_vcs_info.json` = **`7ab1334`** = 当前 main tip（GitHub **没有 `v0.8.0` tag**，最新 tag `v0.7.0`=`8328959`）· **Apache-2.0**（0.6.0 及以前是 MIT OR Apache-2.0）· ★**110** · **MSRV 1.87.0** / edition 2024 · 本机 **rustc 1.98.1**（2026-09-26 01:26–01:33 EDT）：与 [nmea-parser](./nmea-parser.md) 用**同一批** gpsd 真实日志，F9P **1015** 句、AIS 文件 GPS 部分 **1313** 句、F9T 混流 **252** 句 NMEA 逐类与 pynmeagps **1.1.7** 一致（GBS 除外，见坑 #2）；RMC/GGA/ZDA 行 **87/87、328/328、27/27** 逐字段相同；GSV 卫星条目 **2378** = pynmeagps（nmea-parser 为 2523，多 145 假星）；UBX 混流 **62830** 次喂入 **0 panic**，但有状态 `Nmea` 可被一条合成 GSV 毒化后 panic

> 岗位：**一行 NMEA 文本 → Rust 结构体**，外加一个有状态的 `Nmea` 把 GGA/RMC/GSA/GSV… 融合成「当前 fix + 卫星表」。冲突时：**docs.rs / 本机源码 > 上游 README > 本文**。  
> **解析库 ≠ 定位解算器 ≠ 串口/NTRIP 客户端。** 它只看你给的 `&str`，不开串口、不连 caster、不从观测值算位置，fix 全是接收机自己算好写在句子里的。

## 1. 用途与边界

**做：** `parse_str(&str)` / `parse_bytes(&[u8])` → `ParseResult`（30 种句型：AAM ALM APA BOD BWC BWW DBK DBS DPT GBS GGA GLL GNS GSA GST GSV HDT MDA MTW MWV RMC TTM TXT VHW VTG WNC ZDA ZFO ZTG + Garmin `PGRMZ`）；`Nmea::parse` / `parse_for_fix` 有状态融合；`no_std`（heapless，无分配器）；可选 serde（`ParseResult` 0.8.0 起 Serialize+Deserialize）、defmt。

**不做：** 不开串口/TCP/NTRIP（自己用 `serialport`/`tokio`，或 [gpsd](./gpsd.md)）；不做定位解算；**不解 AIS**（`!AIVDM` → `ParsingError`，要 AIS 用 [nmea-parser](./nmea-parser.md)）；不解 UBX/RTCM（→ [ublox](./ublox.md) / [rtcm-rs](./rtcm-rs.md)）；不切帧；**不能生成 NMEA**——没有 encode/to_sentence，`impl Display for Nmea` 只是人读摘要（`Some(00:39:56): lat: … [[Beidou,1,…]]`），唯一相关的是 `NmeaSentence::calc_checksum()`；不认 `$PUBX` 等专有句（仅 `PGRMZ`）。

## 2. 安装与 features

```bash
. "$HOME/.cargo/env"; rustc --version          # 本机 1.98.1；crate 要求 ≥ 1.87.0（本篇未用 1.87 实测）
cargo new --bin demo && cd demo
cargo add nmea@=0.8.0                           # 依赖：nom 8 / chrono / heapless 0.9 / arrayvec / num-traits(libm) / cfg-if
```

| feature | 默认 | 含义 |
| --- | --- | --- |
| `std` | **开** | nom/chrono/arrayvec 的 std；关掉即 `no_std` |
| `all-sentences` | **开** | = `GNSS` + `waypoint` + `maritime` + `water` + `vendor-specific` + `other` |
| `GNSS` | 随上 | APA ALM GBS GGA GLL GNS GSA GST GSV RMC VTG |
| `waypoint` / `maritime` | 随上 | AAM BOD BWC BWW WNC ZFO ZTG / = waypoint + water + radar |
| `water` / `radar` | 随上 | DBK DBS DPT MTW VHW / TTM |
| `vendor-specific` / `other` | 随上 | RMZ（`$PGRMZ`）/ HDT MDA MWV TXT ZDA |
| 30 个单句 feature（`GGA`、`RMC`…） | 随上 | 可逐句开关 |
| `serde` / `defmt` / `features-docs` | 关 | 序列化 / 嵌入式日志 / 文档用 |

裁剪实测：`cargo add nmea@=0.8.0 --no-default-features -F GGA,RMC,GSV,GSA`，`#![no_std]` 库 `cargo build --target thumbv7em-none-eabihf` 通过；只开 `GGA` 时喂 RMC → `Err(DisabledSentence)`（`parse_str` 与 `Nmea::parse` 都是）。x86_64 默认 features 下 `size_of::<Nmea>()` = **13296 B**、`ParseResult` = 344 B——MCU 上别放栈。

## 3. 端到端（本机真跑；2026-09-26 01:26–01:33 EDT）

### 3.1 真实输入

`https://gitlab.com/gpsd/gpsd/-/raw/43362cd2/test/daemon/<文件>`（gpsd master **`43362cd2`**，2026-09-24；BSD-2-Clause），真实接收机录制，sha256 前 12 位与 nmea-parser 篇相同：

| 文件 | 大小 | sha256₁₂ | 内容 |
| --- | ---: | --- | --- |
| `ublox-zed-f9p-nmea.log` | 58367 B | `6f99714a2800` | ZED-F9P HPG 1.11，NMEA 4.10+（GSV 带信号 ID，含**真实 `$GBGSV`**），Dunedin，2019-04-12，29 历元 |
| `ais-nmea.log` | 85460 B | `ac2d9f36e457` | `$GP…` + `!AIVDM` 混录，2020-04-07 |
| `ublox-zed-f9t-ubx_nmea_l5.log` | 31754 B | `0531482cc9ea` | EVK-F9T，UBX 二进制与 NMEA 同文件，2025-07-31 |

### 3.2 逐句解析 + 计数（`src/main.rs`，完整可编）

```rust
use nmea::{parse_str, Error, ParseResult, SentenceType};
use std::collections::BTreeMap;

fn main() {
    let path = std::env::args().nth(1).expect("usage: demo FILE");
    let raw = std::fs::read(&path).unwrap();
    let mut n: BTreeMap<String, usize> = BTreeMap::new();
    for line in raw.split(|&b| b == b'\n') {
        if line.first() == Some(&b'#') { continue; } // gpsd 注释行
        // UBX 混流：只取最后一个非 ASCII 字节之后，再从第一个 '$' 起
        let tail = match line.iter().rposition(|b| !b.is_ascii()) {
            Some(i) => &line[i + 1..],
            None => line,
        };
        let s = std::str::from_utf8(tail).unwrap().trim_end();
        let s = match s.find('$') { Some(i) => &s[i..], None => s };
        if s.is_empty() { continue; }
        let r = parse_str(s);
        let k = match &r {
            Ok(p) => format!("{:?}", SentenceType::from(p)),
            Err(Error::ParsingError(_)) if s.starts_with(['$', '!']) => format!("ErrParsing({})", &s[3..6]),
            Err(Error::ParsingError(_)) => "ErrParsing(junk)".into(),
            Err(e) => format!("Err {e}"),
        };
        if !n.contains_key(&k) {
            match &r {
                Ok(ParseResult::GGA(g)) => println!("GGA t={} lat={:.9} lon={:.9} sats={:?} alt={:?} m fix={:?}",
                    g.fix_time.unwrap(), g.latitude.unwrap(), g.longitude.unwrap(),
                    g.fix_satellites, g.altitude, g.fix_type),
                Ok(ParseResult::RMC(m)) => println!("RMC {:?} {:?} sog={:?} kn", m.fix_date, m.fix_time, m.speed_over_ground),
                Ok(ParseResult::GSA(a)) => println!("GSA talker={} sys={:?} prns={:?}", a.talker_id, a.system_id, a.fix_sats_prn),
                Ok(ParseResult::ZDA(z)) => println!("ZDA {:?} {:?}-{:?}-{:?}", z.utc_time, z.year, z.month, z.day),
                Ok(ParseResult::GST(g)) => println!("GST lat_sd={:?} lon_sd={:?} alt_sd={:?} m", g.lat_sd, g.long_sd, g.alt_sd),
                _ => {}
            }
        }
        if let Ok(ParseResult::GSV(v)) = &r {
            *n.entry("GSV_sats".into()).or_default() += v.sats_info.iter().flatten().count();
        }
        *n.entry(k).or_default() += 1;
    }
    println!("{:?}", n);
}
```

**本机打印（`cargo run --release -- <文件>`，原样）：**

```text
== ublox-zed-f9p-nmea.log
RMC Some(2019-04-12) Some(00:39:56) sog=Some(0.025) kn
GGA t=00:39:56 lat=-45.877567167 lon=170.500111333 sats=Some(12) alt=Some(14.2) m fix=Some(Gps)
GSA talker=GN sys=Some(Gps) prns=[13, 16, 21, 15, 10, 29, 27, 20]
GST lat_sd=Some(2.3) lon_sd=Some(3.5) alt_sd=Some(4.0) m
ZDA Some(00:39:56) Some(2019)-Some(4)-Some(12)
{"ErrParsing(GBS)": 29, "GGA": 29, "GLL": 29, "GSA": 116, "GST": 29, "GSV": 696, "GSV_sats": 2378, "RMC": 29, "VTG": 29, "ZDA": 29}
== ais-nmea.log
GSA talker=GP sys=Some(Gps) prns=[11, 32, 14, 28, 22, 3, 10, 8, 17]
RMC Some(2020-04-07) Some(21:39:50) sog=Some(0.02) kn
GGA t=21:39:50 lat=52.842278167 lon=5.705820000 sats=Some(9) alt=Some(-6.0) m fix=Some(Gps)
{"ErrParsing(VDM)": 183, "GGA": 164, "GLL": 164, "GSA": 165, "GSV": 492, "GSV_sats": 1658, "RMC": 164, "VTG": 164}
== ublox-zed-f9t-ubx_nmea_l5.log
RMC Some(2025-07-31) Some(19:33:34) sog=Some(0.014) kn
GGA t=19:33:34 lat=44.068854000 lon=-121.314135000 sats=Some(12) alt=Some(1139.9) m fix=Some(Gps)
GSA talker=GN sys=Some(Gps) prns=[8, 24, 2, 18, 27, 23, 32, 10]
GST lat_sd=Some(0.93) lon_sd=Some(1.2) alt_sd=Some(2.3) m
ZDA Some(19:33:34) Some(2025)-Some(7)-Some(31)
{"ErrParsing(\u{7}\0\u{2})": 1, "ErrParsing(GBS)": 9, "ErrParsing(junk)": 70, "GGA": 9, "GSA": 45, "GST": 9, "GSV": 153, "GSV_sats": 531, "RMC": 9, "VTG": 9, "ZDA": 9}
```

读法：GSV 一句一出（无 `Incomplete`，不拼组），`GSV_sats` 是所有句 `Some` 条目之和；F9T 的 71 条 `ErrParsing`（70 junk + 1 条 `$` 后跟二进制）是 UBX 残片，9 历元真 NMEA 一句没丢。**去掉 `s.find('$')` 那行**，F9T 的 RMC 只剩 **3/9**（UBX 帧尾的 ASCII 控制字节留在句首，`parse_str` 要求首字符就是 `$`）。

### 3.3 有状态融合：`Nmea::parse` / `parse_for_fix`（`src/bin/fuse.rs`）

```rust
use nmea::{Nmea, SentenceType};
use std::collections::BTreeMap;

fn main() {
    let text = std::fs::read_to_string("../data/ublox-zed-f9p-nmea.log").unwrap(); // 纯 ASCII 文件
    let lines: Vec<&str> = text.lines().filter(|l| !l.starts_with('#')).collect();
    let mut nmea = Nmea::default(); // ① 有状态 parse：喂第一历元 34 句
    for s in &lines[..34] { let _ = nmea.parse(s); }
    println!("{}", nmea.to_string().split(" [[").next().unwrap());
    println!("date={:?} used={:?} prns={} hdop={:?} vdop={:?} pdop={:?}", nmea.fix_date,
        nmea.num_of_fix_satellites, nmea.fix_satellites_prns.as_ref().unwrap().len(), nmea.hdop, nmea.vdop, nmea.pdop);
    let sats = nmea.satellites();
    println!("satellites() n={} with_snr={}", sats.len(), sats.iter().filter(|s| s.snr().is_some()).count());
    // ② parse_for_fix：要求同一 UTC 内 RMC+GGA 都到齐
    let mut nav = Nmea::create_for_navigation(&[SentenceType::RMC, SentenceType::GGA]).unwrap();
    let mut res: BTreeMap<String, usize> = BTreeMap::new();
    for s in &lines {
        let k = match nav.parse_for_fix(s) { Ok(f) => format!("Ok({f:?})"), Err(e) => format!("Err({})", format!("{e:?}").split('(').next().unwrap()) };
        *res.entry(k).or_default() += 1;
    }
    println!("{res:?}");
}
```

```text
Some(00:39:56): lat: Some(-45.877567166666665) lon: Some(170.50011133333334) alt: Some(14.2)
date=Some(2019-04-12) used=Some(12) prns=20 hdop=Some(0.64) vdop=Some(0.83) pdop=Some(1.05)
satellites() n=41 with_snr=6
{"Err(ParsingError)": 29, "Ok(Gps)": 29, "Ok(Invalid)": 957}
```

读法：融合后日期来自 RMC、高度/卫星数来自 GGA、DOP 来自 GSA；4 条 `$GNGSA` 按尾部系统 ID 累加成 **20** 颗 `(Some(Gps),13)…(Some(Beidou),21)`，而 GGA 的 `used=12`（u-blox 在 GGA 里封顶 12）。`parse_for_fix` 每历元在 GGA 那句返回一次 `Ok(Gps)`（29 次），其余句都是 `Ok(Invalid)`——`Invalid` 表示「这句没凑出 fix」，不是坏句；29 条 `Err` 全是 GBS。`satellites()` 41 颗（= GPS 12 + GLO 10 + GAL 9 + BDS 10）但只有 **6** 颗带 C/N₀：同星座第二个信号组（GPS 信号 6、GLO 3、GAL 2、BDS 空 ID）覆盖了第一组，第一组本有 **23** 颗带 C/N₀（坑 #1）。

### 3.4 交叉核对（pynmeagps 1.1.7，`NMEAReader.parse(validate=1)`，每行取最后一个 `$` 起）

| 核对 | 结果 |
| --- | --- |
| 逐类计数 F9P / AIS / F9T | pynmeagps `GGA/GLL/RMC/VTG/ZDA/GST 29、GSA 116、GSV 696、GBS 29` / `GGA/GLL/RMC/VTG 164、GSA 165、GSV 492` / `GGA/RMC/VTG/ZDA/GST 9、GSA 45、GSV 153、GBS 9`：除 GBS（本库全 `ParsingError`）外**逐类一致**；异常 0 |
| RMC（日期、UTC、纬经度）+ GGA（UTC、纬度、经度、卫星数、高度）+ ZDA（UTC、年月日），经纬度比到 1e-7° | **87/87、328/328、27/27** 行完全相同；首行 GGA `00:39:56, −45.8775672°, 170.5001113°, 12, 14.2 m` |
| GSV 卫星条目总数 | 本库 **2378 / 1658 / 531** = pynmeagps **2378 / 1658 / 531** |
| 同文件跑 nmea-parser 0.11.0 | GSV 条目 2523（145 条仰角/方位/C/N₀ 全空的假星）；`$GB` 609 条目 `source=Other`；GGA 首条 `2000-01-01T00:39:56Z`；GSA `source` 只有 `Combination` |

### 3.5 与 nmea-parser 对照（同一 F9P 文件实测，另列错误用例）

| 项 | `nmea` 0.8.0（本文） | `nmea-parser` 0.11.0 |
| --- | --- | --- |
| GSV 末句信号 ID（`$GAGSV,3,3,09,33,62,034,08,7*41`） | `[Some(33), None, None, None]`，**无假星**；但信号 ID 被**丢弃**、结构体里没有 | 信号 ID 7 变成 PRN 7，全文件多 145 颗 |
| `$GBGSV` 北斗 talker | `Beidou`（GSV/GSA 都认 `BD`/`GB`） | `Other` |
| GSA 系统 ID | `system_id: Some(Gps/Glonass/Galileo/Beidou)`；与 talker 冲突报 `SystemIdMismatch` | 不解析 |
| GGA 日期 | `fix_time: NaiveTime`，**不造日期**；`Nmea` 融合时取 RMC 日期 | 固定 2000-01-01 |
| GST / GBS | GST 解析 / **GBS 报错** | 都 `UnsupportedSentenceType` |
| AIS | 不支持 | 支持 1–6、9–27 |
| 多句 GSV | 一句一出；拼组靠 `Nmea` 状态 | `Incomplete` 拼组后一次出 |
| UBX 混流 lossy 整行 | `Err(ASCII)`，不 panic | panic（exit 101） |
| `no_std` | 是（本机 thumbv7em 编过） | 未验证 |
| 生成 NMEA | 否 | 否 |

## 4. 错误用例（本机实测；「真实」= 取自上述日志原句，其余为**合成**）

| 输入 | `parse_str` 返回 |
| --- | --- |
| 真实 GGA / 真实 GGA 后加 `\r\n` | `Ok(GGA)` / 同样 `Ok`（`*HH` 之后的内容被忽略） |
| 合成：校验和改 `*57` | `Err(ChecksumMismatch { calculated: 86, found: 87 })`（十进制） |
| 合成：真实 VTG 校验和改小写 `*3b` | `Ok(VTG)`——小写十六进制可接受 |
| 合成：去掉 `*56` / 只剩 `*5` | `Err(ParsingError(… TakeUntil))` / `Err(ParsingError(… Eof))`——**无校验和一律拒收** |
| 合成：截断到 `…,S,17030.0`；再补正确校验和 | `ParsingError(TakeUntil)`；`ParsingError(Char)`——不会静默给错值 |
| 合成：`$PUBX,00,…`（109 字符）/ 超长 `$GPTXT` | `Err(SentenceLength(109))`，上限 `SENTENCE_MAX_LEN` = 102 |
| 合成：`$GPXYZ,1,2,3*50`（未知句型） | `Err(ParsingError(… MapRes))`，不是 `Unknown` |
| 空串 / `hello world` / `$` / 句首空格的真实 GGA | 全是 `Err(ParsingError(…))` |
| 真实 `$GNGBS,003956.00,2.3,3.5,4.0,,,,,,*55` | `Err(ParsingError(… input: "2.3,3.5,4.0,,,,,,", MapRes))` |
| 真实 `!AIVDM,…` | `Err(ParsingError(… Char))` |
| 合成：`$GNGSV,…` | `Err(UnknownGnssType("GN"))` |
| 合成：`$GPGSA,…,3`（talker GPS、尾部系统 ID 3） | `Err(SystemIdMismatch { talker_sys_id: Gps, tail_sys_id: Galileo })` |
| 真实 F9T 第 85/14 行（UBX；第 14 行 UBX 帧后接 `$GNRMC`）：`parse_bytes` / lossy `parse_str` | `Err(Utf8Decoding)` / `Err(ASCII)` |
| 真实 F9T 全部行 × 每个起始字节偏移，`parse_bytes` + lossy `parse_str` 共 **62830** 次；合成随机 ASCII 20 万条 | **0 panic** |
| 真实 GPGSV：历元 A 三句，历元 B 丢 3/3 只来 3/1、3/2，`Nmea::satellites()` | 10 颗：PRN3 C/N₀=22（B）但 PRN28=31、PRN32=41 仍是 **A 的旧值**，无标记 |
| `Nmea::parse` 喂真实 ZDA / GST | `Err(Unsupported(ZDA))` / `Err(Unsupported(GST))`（`parse_str` 能解，融合器不收） |
| 合成：`$GPGSV,20,16,…` 连喂 16 句 | **panic**：`Should not get the more than expected number of satellites`（parser.rs:178） |
| 合成：上句只喂 **1** 次，再喂真实 GPGSV | 第 **15** 句真实 GSV 时同一 panic——一条校验和正确的坏句毒化整个 `Nmea` |
| 合成：7 句 `$GNGSA` 各 12 个不同 PRN（84 > `MAX_PRNS` 72） | **panic**：`prns exceeds maximum`（parser.rs:272） |

错误类型：`Error<'a>` 枚举（`ChecksumMismatch`、`ParsingError(nom::Err)`、`SentenceLength`、`ASCII`、`Utf8Decoding`、`UnknownGnssType`、`SystemIdMismatch`、`Unsupported`、`DisabledSentence`…），**借用输入串**，要存下来得先 `to_string()`。

## 5. 输入 / 输出

| API | 作用 |
| --- | --- |
| `parse_str(&str)` / `parse_bytes(&[u8])` | 一句、无状态；必须以 `$` 开头、带 `*HH`、≤102 字符、纯 ASCII |
| `Nmea::default()` / `create_for_navigation(&[SentenceType])` | 融合器；后者给 `parse_for_fix` 指定必需句（空切片 → `EmptyNavConfig`） |
| `Nmea::parse(&str) -> Result<SentenceType, _>` | 合并 GGA/RMC/GNS/GSA/GSV/VTG/GLL/TXT，其余句型返回 `Err(Unsupported)` |
| `Nmea::parse_for_fix(&str) -> Result<FixType, _>` | UTC 变化即清空；必需句到齐且 fix 有效才返回非 `Invalid` |
| `satellites()` / `fix_satellites_prns` / `gsa_cycle_complete` | 在视卫星（按星座+PRN 去重）/ 参与解算 `(系统ID, PRN)` / GSA 组已收完 |

| 输出字段 | 单位 / 备注 |
| --- | --- |
| `GgaData.latitude/longitude` · `RmcData.lat/lon` | °，f64，南纬/西经为负 |
| `GgaData.altitude` / `geoid_separation` | m（海拔 / 大地水准面差距），f32 |
| `GgaData.fix_time` / `RmcData.fix_date` / `ZdaData.year/month/day` | `NaiveTime`（无时区）/ `NaiveDate` / 整数 |
| `RmcData.speed_over_ground` / `VtgData.speed_over_ground` | kn |
| `GstData.lat_sd/long_sd/alt_sd` | m（1σ） |
| `GsvData.sats_info[i]` → `prn/elevation/azimuth/snr` | u32 / ° / °（真北）/ C/N₀ dB-Hz；**无信号 ID** |
| `GsaData.system_id` / `talker_id` | NMEA 4.10 系统 ID（缺省时由 talker 推）/ 2 字符 |

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 多信号接收机 `satellites()` C/N₀ 大面积 `None`（F9P 6/41） | GSV 信号 ID 被丢弃，同星座 L1/L2 组进同一队列，按 `sentence_num` 保留最后几句 | 要 C/N₀ 就自己用 `parse_str` 按原句信号 ID 分组，别用 `satellites()` |
| 2 | u-blox 真实 GBS 全部 `ParsingError` | GBS 纬/经误差（m）被当成「度分+N/S」坐标解析 | 需要 GBS 用 pynmeagps；或跳过 |
| 3 | `Nmea::parse` 对 ZDA/GST/HDT… 返回 `Err(Unsupported)` | 融合器只收 8 种句型 | 忽略 `Unsupported`；ZDA 日期另用 `parse_str` 取 |
| 4 | 句首有空格/二进制残留就 `ParsingError`（F9T RMC 3/9） | 必须首字符 `$` | 截到最后一个非 ASCII 字节后再 `find('$')` |
| 5 | 无校验和的句子（模拟器、手敲测试串）全被拒 | `*HH` 是语法必需 | 测试串先补校验和；或换 nmea-parser |
| 6 | `$PUBX,00`、长 `$PSTI` 报 `SentenceLength` | 硬上限 102 字符，先于句型检查 | 专有句另行处理 |
| 7 | 一条坏 GSV 让进程数秒后 panic；>72 个 GSA PRN panic；>58 颗卫星 `satellites()` panic（issue #158，开放中） | heapless 定长容器 + `expect`/`unwrap` | 融合器放 `catch_unwind` 或独立任务；明显异常的 GSV（`sentence_num`>9）先丢 |
| 8 | GSV 丢句后卫星表混入上一历元值 | 队列无历元概念 | 以 GGA/RMC UTC 为界自己重建 `Nmea` |
| 9 | `$GNGSV` → `UnknownGnssType("GN")` | GSV talker 只认 GA/GP/GL/BD/GB/GI/GQ/PQ/QZ | 按信号/PRN 段自己映射 |
| 10 | GGA `used=12` 与 `fix_satellites_prns` 20 颗对不上 | 接收机 GGA 封顶；GSA 才全 | 以 GSA 为准 |
| 11 | `parse_for_fix` 绝大多数返回 `Ok(Invalid)` | 只在凑齐必需句那一句返回 fix | 看返回值 `is_valid()`，别把 `Invalid` 当错误 |
| 12 | MCU 栈溢出 | `Nmea` 13296 B | `static`/堆上放；`--no-default-features` 只开需要的句 |
| 13 | 关了 feature 的句型报 `DisabledSentence` 而非 `Unsupported` | cfg 裁剪 | 两种都当「跳过」 |
| 14 | `Error<'a>` 生命周期卡住缓冲区复用 | 错误借用输入 | `e.to_string()` 后再存 |
| 15 | 按 tag 找 0.8.0 源码找不到 | 上游未打 `v0.8.0` tag | 用 `7ab1334`（crate 内 vcs 信息） |
| 16 | 想用它发配置句 | 无编码 API | 自己拼串 + `NmeaSentence::calc_checksum`，或 pynmeagps |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust（含 `no_std` MCU）解 GNSS NMEA、要 NMEA 4.10 系统 ID、GST | **本文 `nmea` 0.8.0**（融合器包 `catch_unwind`，C/N₀ 自己按信号分组） |
| Rust 解 NMEA **+ AIS**，要容忍无校验和输入 | [nmea-parser](./nmea-parser.md)（先滤非 ASCII、修 GSV 假星） |
| 嵌入式 C、零分配 / 可插拔句型模块 | [minmea](./minmea.md) / [libnmea](./libnmea.md) |
| Python 解析**并生成** NMEA、信号 ID、GBS | [pynmeagps](./pynmeagps.md)（经典 API → [pynmea2](./pynmea2.md)） |
| 守护进程、多客户端、JSON、串口自动识别 | [gpsd](./gpsd.md) |
| UBX / RTCM3 二进制 | [ublox](./ublox.md) / [rtcm-rs](./rtcm-rs.md) |

**相关：** [nmea-parser.md](./nmea-parser.md) · [minmea.md](./minmea.md) · [libnmea.md](./libnmea.md) · [pynmea2.md](./pynmea2.md) · [pynmeagps.md](./pynmeagps.md) · [gpsd.md](./gpsd.md) · [ublox.md](./ublox.md) · [rtcm-rs.md](./rtcm-rs.md) · [README.md](./README.md)
