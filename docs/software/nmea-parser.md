# nmea-parser · Rust NMEA 0183 + AIS 解析库操作手册

目录：上游 <https://github.com/zaari/nmea-parser>（作者 Timo Saarinen / zaari）· crates.io **`nmea-parser` 0.11.0**（2024-06-13 发布；总下载 **513802**，近 90 天 **93741**）· tag **`v0.11.0`=`865e7e5`**；master tip **`bc0a89f`**（领先 2 commit，只改 CHANGELOG/Cargo 版本号/README，**源码与 0.11.0 相同**）· **Apache-2.0** · ★**51** · 纯库（crate 包 62837 B）· **无 features**（`[features]` 为空）· **未声明 MSRV**（0.10.0 曾写 `rust-version = 1.56`，0.11.0 删了）/ edition 2018 · 本机 **rustc 1.98.1**（2026-09-26 01:17–01:30 EDT）：gpsd 真实日志 ZED-F9P **1015** 句、AIS+NMEA **1496** 句逐类计数与 pynmeagps **1.1.7** / pyais **3.2.3** 一致；GGA **29/29**、**164/164** 行 UTC/经纬度/卫星数/高度逐行相同；AIS 动态报 **144** 条与 pyais 多重集合完全一致；**UBX 混流原样喂入 → panic（exit 101）**；NMEA 4.10 GSV 信号 ID 被当成 PRN，F9P 日志多出 **145** 颗假卫星

> 岗位：**一行 NMEA 文本 → Rust 结构体**（校验和、talker 识别、GSV/AIS 多句拼接、AIS 6-bit 载荷解码）。冲突时：**docs.rs / 本机源码 > 上游 README > 本文**。  
> **解析库 ≠ 定位解算器 ≠ 串口/NTRIP 客户端。** 它只看你给的字符串，不开串口、不连 caster、不算位置。C 同类 → [minmea](./minmea.md) / [libnmea](./libnmea.md)；Python 同类 → [pynmea2](./pynmea2.md) / [pynmeagps](./pynmeagps.md)；守护进程 → [gpsd](./gpsd.md)。

## 1. 用途与边界

**做：**

- `NmeaParser::parse_sentence(&str) -> Result<ParsedMessage, ParseError>`，一次一句
- GNSS：ALM、DBS、DPT、DTM、GGA、GLL、GNS、GSA、GSV、HDT、MTW、MWV、RMC、VTG、MSS、STN、VBW、VHW、ZDA
- AIS：`!AIVDM`/`!AIVDO` 类型 1–6、9–27（7、8 返回 `UnsupportedSentenceType`），Class A/B
- 多句状态存在 `NmeaParser` 内部：GSV 按 `(句头,总句数,序号)`、AIS 按 `(消息ID,片号,信道)` 拼接；24A/24B 合并成一条 `VesselStaticData`
- GNSS 结构体 `#[derive(Serialize)]`（serde，可直接 `serde_json::to_string`）

**不做：**

- **不**开串口、不读 TCP/NTRIP → 自己用 `serialport`/`tokio`，或 [gpsd](./gpsd.md)
- **不**做定位解算、不用 GSV/GSA 算 DOP，只搬运接收机给的字段
- **不**解析 UBX/RTCM 二进制 → [ublox](./ublox.md) / [rtcm-rs](./rtcm-rs.md)；RAWX→RINEX → [ubx2rinex](./ubx2rinex.md)
- **不**切帧：给它字节流它不会找 `\r\n`，遇到二进制可能 panic（§3.4）
- **不能编码/生成 NMEA**：全库没有 encode / to_sentence / `Display for GgaData` 之类 API，结构体只实现 `Serialize`（JSON），不实现 `Deserialize`
- 不认 GST、GBS、TXT、`$PUBX` 等专有句 → `UnsupportedSentenceType`

| 易混 | 是什么 | 与本库关系 |
| --- | --- | --- |
| **本文** `nmea-parser` | Rust，NMEA 0183 + AIS | `cargo add nmea-parser@0.11.0` |
| crates.io `nmea`（AeroRust） | 另一个 Rust NMEA crate（0.8.0） | 不同作者、API 不同、**不含 AIS**；本库未对比实测 |
| [minmea](./minmea.md) / [libnmea](./libnmea.md) | C 解析库 | 嵌入式 C 选它们 |
| [pynmea2](./pynmea2.md) / [pynmeagps](./pynmeagps.md) | Python 解析库 | pynmeagps 可生成 NMEA、懂 NMEA 4.10 信号 ID；本文交叉核对用它 |
| [gpsd](./gpsd.md) | C 守护进程 | 自带 NMEA/AIS 驱动；本文测试数据取自 gpsd 回归日志 |

## 2. 安装

```bash
. "$HOME/.cargo/env"; rustc --version        # 本机 1.98.1；0.11.0 未声明 MSRV
cargo new --bin nmea_demo && cd nmea_demo
cargo add nmea-parser@=0.11.0                  # 依赖树 22 个 crate：bitvec/chrono/hashbrown/log/num-traits/serde…
```

- 没有可开关的 feature；serde 以**默认特性**（含 `std`）被拉入。CHANGELOG 说 0.9.0 起支持 `no_std`（仍要 allocator），但 0.11.0 的 serde 依赖没关 default-features，`no_std` 目标本篇**未验证**；把 serde 挪到 feature 的 PR #49（2025-06）至今未合。
- 维护状态：0.11.0 之后无发版；issue #52（2026-09-15）公开询问维护状态，修 panic 的 PR #50（2025-11）未合。

## 3. 端到端（本机真跑；2026-09-26 01:17–01:30 EDT）

### 3.1 真实输入：gpsd 回归测试日志

来源 `https://gitlab.com/gpsd/gpsd/-/raw/master/test/daemon/<文件>`（gpsd master `43362cd2`，BSD-2），均为真实接收机录制：

| 文件 | 大小 | sha256₁₂ | 内容 |
| --- | ---: | --- | --- |
| `ublox-zed-f9p-nmea.log` | 58367 B | `6f99714a2800` | ZED-F9P HPG 1.11，NMEA 4.10+（GSV 带信号 ID），新西兰 Dunedin，2019-04-12，29 个历元 |
| `ais-nmea.log` | 85460 B | `ac2d9f36e457` | GPS NMEA + `!AIVDM` 混录，荷兰 Lemmer 附近，2020-04-07 |
| `ublox-zed-f9t-ubx_nmea_l5.log` | 31754 B | `0531482cc9ea` | EVK-F9T，UBX 二进制与 NMEA 混在一个文件里（83 个 `b5 62` 同步头），2025-07-31 |

以 `#` 开头的是 gpsd 注释行，要跳过。

### 3.2 解析 + 计数 + 取字段（`src/main.rs`，完整可编）

```rust
use nmea_parser::{NmeaParser, ParsedMessage, ParseError};
use std::collections::BTreeMap;

fn main() {
    let path = std::env::args().nth(1).expect("usage: manex FILE");
    let raw = std::fs::read(&path).unwrap();
    let mut parser = NmeaParser::new();
    let mut n: BTreeMap<&str, usize> = BTreeMap::new();
    for line in raw.split(|&b| b == b'\n') {
        if line.first() == Some(&b'#') { continue; } // gpsd 日志注释行
        // 只喂最后一个非 ASCII 字节之后的尾巴：避开 UBX 二进制导致的 panic
        let tail = match line.iter().rposition(|b| !b.is_ascii()) {
            Some(i) => &line[i + 1..],
            None => line,
        };
        let s = std::str::from_utf8(tail).unwrap().trim_end();
        if s.is_empty() { continue; }
        let k = match parser.parse_sentence(s) {
            Ok(ParsedMessage::Gga(g)) => {
                if n.get("Gga").is_none() {
                    println!("GGA {} lat={:.7}° lon={:.7}° sats={:?} alt={:?} m t={:?}",
                        g.source, g.latitude.unwrap(), g.longitude.unwrap(),
                        g.satellite_count, g.altitude, g.timestamp.map(|t| t.time()));
                }
                "Gga"
            }
            Ok(ParsedMessage::Rmc(r)) => {
                if n.get("Rmc").is_none() { println!("RMC utc={:?} sog={:?} kn", r.timestamp, r.sog_knots); }
                "Rmc"
            }
            Ok(ParsedMessage::Gsv(v)) => { *n.entry("GsvSats").or_default() += v.len(); "Gsv" }
            Ok(ParsedMessage::Gsa(_)) => "Gsa",
            Ok(ParsedMessage::Vtg(_)) => "Vtg",
            Ok(ParsedMessage::VesselDynamicData(d)) => {
                if n.get("AisDyn").is_none() {
                    println!("AIS mmsi={} lat={:?} lon={:?} sog={:?} kn", d.mmsi, d.latitude, d.longitude, d.sog_knots);
                }
                "AisDyn"
            }
            Ok(ParsedMessage::VesselStaticData(_)) => "AisStatic",
            Ok(ParsedMessage::Incomplete) => "Incomplete",
            Ok(_) => "OtherOk",
            Err(ParseError::UnsupportedSentenceType(_)) => "ErrUnsupported",
            Err(ParseError::CorruptedSentence(_)) => "ErrCorrupted",
            Err(ParseError::InvalidSentence(_)) => "ErrInvalid",
        };
        *n.entry(k).or_default() += 1;
    }
    println!("{:?}", n);
}
```

**本机打印（`cargo run --release -- <文件>`，原样）：**

```text
== ublox-zed-f9p-nmea.log
RMC utc=Some(2019-04-12T00:39:56Z) sog=Some(0.025) kn
GGA combination lat=-45.8775672° lon=170.5001113° sats=Some(12) alt=Some(14.2) m t=Some(00:39:56)
{"ErrUnsupported": 58, "Gga": 29, "Gsa": 116, "Gsv": 232, "GsvSats": 2523, "Incomplete": 464, "OtherOk": 58, "Rmc": 29, "Vtg": 29}
== ais-nmea.log
RMC utc=Some(2020-04-07T21:39:50Z) sog=Some(0.02) kn
GGA GPS lat=52.8422782° lon=5.7058200° sats=Some(9) alt=Some(-6.0) m t=Some(21:39:50)
AIS mmsi=244660274 lat=Some(52.855395) lon=Some(5.678283333333333) sog=Some(0.0) kn
{"AisDyn": 144, "AisStatic": 16, "ErrUnsupported": 6, "Gga": 164, "Gsa": 165, "Gsv": 164, "GsvSats": 1658, "Incomplete": 345, "OtherOk": 164, "Rmc": 164, "Vtg": 164}
== ublox-zed-f9t-ubx_nmea_l5.log
RMC utc=Some(2025-07-31T19:33:34Z) sog=Some(0.014) kn
GGA combination lat=44.0688540° lon=-121.3141350° sats=Some(12) alt=Some(1139.9) m t=Some(19:33:34)
{"ErrInvalid": 71, "ErrUnsupported": 18, "Gga": 9, "Gsa": 45, "Gsv": 72, "GsvSats": 567, "Incomplete": 81, "OtherOk": 9, "Rmc": 9, "Vtg": 9}
```

读法：F9P 的 696 句 GSV = 232 组（29 历元 × 4 星座 × 2 信号）完整输出 + 464 句 `Incomplete`；`OtherOk` 58 = GLL 29 + ZDA 29；`ErrUnsupported` 58 = GST 29 + GBS 29。AIS 文件 183 句 `!AIVDM` = 动态 144 + 静态 16 + 类型 8 共 6 句 + 17 句前片 `Incomplete`（12 条类型 5 的 1/2 片 + 5 条 24A）。F9T 的 `ErrInvalid` 71 是 UBX 二进制里的 ASCII 残片，真 NMEA 一句没丢。

### 3.3 交叉核对

| 核对 | 结果 |
| --- | --- |
| pynmeagps 1.1.7 `NMEAReader.parse(validate=1)`，F9P 逐行 | RMC/VTG/GGA/GLL/ZDA 各 29、GSA 116、GSV 696、GST 29、GBS 29，与本库**逐类一致** |
| GGA 逐行（UTC、纬度、经度、卫星数、高度，经纬度比到 1e-7°） | F9P **29/29**、AIS 文件 **164/164** 完全相同；首行 `00:39:56, −45.877567167°, 170.500111333°, 12, 14.2 m` |
| RMC 日期 | 本库 `2019-04-12T00:39:56Z` = pynmeagps `date(2019,4,12) time(0,39,56)` |
| GSV 卫星总数（F9P） | 本库 **2523**，pynmeagps **2378**，差 **145** = 本库假卫星数（坑 #1） |
| pyais 3.2.3 解 AIS 183 句 | 类型 1:116、3:21、18:7（动态合计 144）、5:12、24:9、8:6；动态报 MMSI/纬度/经度/航速**多重集合完全一致**；不可用值 91°/181°/102.3 kn 在本库是 `None` |
| AIS 静态报 | pyais 17 条带船名（类型 5 ×12 + 24A ×5，各片单独出），本库 16 条 = 类型 5 ×12 + **成对** 24A+24B ×4；PLEIADE 只有 24A，本库**永不输出** |
| F9T 混流 | 行内切出 `$GNRMC…` 后 pynmeagps 也得 9 条 RMC；pynmeagps 流式 `NMEAReader(nmeaonly=False)` 只读到 8 条（被二进制打乱一次）；GSV 153 句 = 本库 72 组 + 81 `Incomplete` |

### 3.4 失败边界（本机实测；「真实」= 取自上述日志原句，其余为**合成**）

| 输入 | 返回 |
| --- | --- |
| 真实 GGA `$GNGGA,003956.00,…*56` | `Ok(Gga)`，`timestamp = 2000-01-01T00:39:56+00:00`（GGA 无日期） |
| 合成：校验和改 `*57` | `Err(CorruptedSentence("Corrupted NMEA sentence: \"56\" != \"57\""))` |
| 合成：真实 VTG 校验和改小写 `*3b` | `Err(CorruptedSentence(… "3B" != "3b"))`——**小写十六进制被判坏** |
| 合成：去掉 `*56` | `Ok(Gga)`，照常解析（无校验和不报错） |
| 合成：只剩 `*5`（截一字符） | `Ok(Gga)`——不足两位就当「没有校验和」 |
| 合成：截断到 `…,S,17030.0`（无 `*`） | `Ok(Gga)`，**lon=170.5°**（真值 170.5001113°）、`satellite_count=None`，静默错值 |
| 同上再补上正确校验和 | 同上 `Ok` |
| 真实 `$GNGST…` / 合成 `$PUBX,00,…` | `Err(UnsupportedSentenceType("Unsupported sentence type: $GST"))` / `…$PUBX` |
| 空串 / `hello world` / `$` | `Err(InvalidSentence(…))` |
| 真实 GPS GSV 3 句依次 | `Incomplete`、`Incomplete`、`Ok(Gsv n=12)` |
| 合成：历元 A 丢 3/2，随后历元 B 的 3/1、3/2 | B 3/2 时输出 `Gsv n=12`，其中 3/3 是**历元 A 的旧句**（PRN29 C/N₀=13，B 应为 12），静默混历元 |
| 合成：`$GAGSV,1,1,01,33,62,034,08,7`（1 星 + 信号 ID 7） | `Ok(Gsv n=2 prn=[33, 7])`——信号 ID 变成 PRN 7 |
| 合成：`$GBGSV,…`（北斗 NMEA 4.10 talker） | `source = Other`（只认 `BD`），同样多出假星 |
| 真实 AIS 类型 5 两片，正序 / 倒序 | 都在第二片给 `VesselStaticData mmsi=371255000 name="SEA ENTERPRISE"` |
| 合成：AIS 3 片消息 | 三片全 `Incomplete`，**永不输出**（只支持 ≤2 片，只打 `warn!` 日志） |
| 真实 AIS 类型 8 | `Err(UnsupportedSentenceType("Unsupported !VDM message type: 8"))` |
| 真实 24A 单独到来 | `Incomplete`；等到同 MMSI 24B 才出 |
| 真实 F9T 行：UBX NAV-PVT 帧后紧跟 `$GNRMC…*01`，`from_utf8_lossy` 喂入 | `Err(CorruptedSentence("… \"98\" != \"01\""))`——从二进制里的第一个 `$` 起算校验和，好句被连坐 |
| 真实 F9T 第 100 行（纯 UBX，含 `$`/`!`/`*` 字节），lossy 喂入 | **panic**：`end byte index 121 is not a char boundary; it is inside '�'`（lib.rs:297），整个程序 exit 101 |
| 合成：`$GPGGA,1*\u{FFFD}` | 同一 panic，可 `catch_unwind` 兜住 |

UBX 混流结论：**不能**把 `String::from_utf8_lossy(整行)` 直接喂；§3.2 的「取最后一个非 ASCII 字节之后的尾巴」可避开 panic 且找回全部 9 句 RMC；更稳的做法是先用 [ublox](./ublox.md) 的 `consume_ubx_rtcm_nmea` 或 pyubx2 切帧，只把 NMEA 帧交给本库。

## 4. 输入 / 输出

| API | 作用 |
| --- | --- |
| `NmeaParser::new()` / `Default` | 建解析器；内部两张 HashMap 存 GSV/AIS 片段和 24A/24B |
| `parse_sentence(&str)` | 一句；句尾 `\r\n`、句首空格/杂字符都可（`$`/`!` 之前被丢弃，本机实测） |
| `reset()` | 清空全部未拼完的片段；换文件/断流后要调 |
| `ParsedMessage::Incomplete` | 多句消息尚未到齐 |
| `ParseError::{UnsupportedSentenceType, CorruptedSentence, InvalidSentence}(String)` | 三种错误，无错误码，只有文本 |

| 输出字段 | 单位 / 备注 |
| --- | --- |
| `GgaData.latitude/longitude` | °，f64，南纬/西经为负 |
| `GgaData.altitude` / `geoid_separation` | m（海拔 / 大地水准面差距） |
| `GgaData.timestamp` / `GllData.timestamp` | `DateTime<Utc>`，日期固定 **2000-01-01** |
| `RmcData.timestamp` / `ZdaData.timestamp_utc` | 带真实日期 |
| `RmcData.sog_knots` / `VtgData.sog_kph` | kn / km/h |
| `GsaData.prn_numbers` / `pdop/hdop/vdop` | `Vec<u8>`；**无** NMEA 4.10 系统 ID |
| `GsvData.prn_number/elevation/azimuth/snr` | u8 / ° / °（真北）/ C/N₀ dB-Hz；后三者 `Option<f32>` |
| `GsvData.source` / `GgaData.source` | 由 talker 得出：GP/GL/GA/BD/GI/QZ/GN，其他（含 **GB**）= `Other` |
| AIS `VesselDynamicData.latitude/longitude/sog_knots/cog/heading_true` | ° / kn / °；不可用值 → `None` |
| AIS `VesselStaticData.name/call_sign/destination/ship_type` | 字符串 / 枚举 |

## 5. 接到哪一步

```text
接收机串口/USB ──serialport 按 \r\n 切行──> 纯 ASCII 句 ──本文──> Gga/Rmc/Gsv… 结构体 ──> 你的应用/serde_json
UBX+NMEA 混流 ──ublox consume_ubx_rtcm_nmea 切帧──> Nmea 帧 → 本文 / Ubx 帧 → ublox
AIS 接收机 (!AIVDM) ──本文──> VesselDynamicData / VesselStaticData（船位、船名）
要多进程共享、JSON 输出 → gpsd；要离线大批量核对/生成 NMEA → pynmeagps
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | F9P 日志 GSV 多出 145 颗「卫星」，仰角/方位/C/N₀ 全 `None` | NMEA 4.10 句尾信号 ID；末句不足 4 星时该字段落在 PRN 位 | 丢弃三项全 `None` 的条目；或自己先验校验和，`(字段数−4) % 4 == 1` 时删掉末字段（信号 ID）与 `*HH` 再喂（无校验和本库照收） |
| 2 | UBX 混流 panic（exit 101） | `rfind('*')` 后按字节切片，落在 U+FFFD 中间（lib.rs:297；PR #50 未合） | 只喂纯 ASCII；§3.2 尾巴法或先切帧；兜底 `catch_unwind` |
| 3 | 真 NMEA 句前粘着二进制时报 `CorruptedSentence` | 从第一个 `$`/`!` 起算，二进制里也可能有 `$` | 切到最后一个非 ASCII 字节之后 |
| 4 | 小写校验和 `*3b` 被判坏 | 用 `{:02X}` 大写字符串比较 | 喂前把 `*` 后两位转大写 |
| 5 | 无校验和 / 截断句照样 `Ok`，值是错的 | 校验和缺失或不足两位就跳过校验 | 自己先要求 `*HH` 存在；链路不可靠时必须 |
| 6 | GSV 静默混历元 | 片段按 `(句头,总数,序号)` 存、无超时，旧片会被后来的补齐 | 以 GGA/RMC 为历元边界调 `reset()`，或自己按历元收 GSV |
| 7 | GGA/GLL 时间是 2000-01-01 | 句子里没有日期，0.9.0 起固定此日（issue #24） | 用同历元 RMC/ZDA 的日期拼 |
| 8 | 四条 `$GNGSA` 分不清星座 | 未解析 NMEA 4.10 系统 ID，`source` 全是 `Combination` | 按 PRN 段或上下文判断；需要时换 pynmeagps |
| 9 | 北斗 `$GBGSV` 的 `source` 是 `Other` | talker 表只有 `BD` | 自己按原句前三字符映射 |
| 10 | AIS 3 片以上消息永远 `Incomplete` | 只实现 1–2 片 | 罕见；需要时换 pyais / gpsd |
| 11 | 24A 没等到 24B 就没有船名输出 | 24A/24B 合并后才出 | 需要船名尽早可见时自己解 24A |
| 12 | AIS 类型 7/8 报错 | 0.11.0 未实现（roadmap 0.12） | 类型 8 用 pyais / gpsd |
| 13 | 错误信息 `Unsupported NMEA sentence type: Unsupported !VDM …` 前缀重复 | `Display` 又加一遍前缀 | 匹配枚举变体，不要解析文本 |
| 14 | 以为能生成 NMEA 发给设备 | 无编码 API | 自己拼字符串 + XOR 校验和，或 pynmeagps |
| 15 | 长跑内存涨 | 丢片永远留在 HashMap | 周期性 `reset()` |
| 16 | 上游不活跃 | 0.11.0 后无发版，PR 积压（#49/#50） | 生产用先 fork 打补丁（#50 就是坑 #2 的修复） |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust 服务里解 NMEA + AIS（船位、船名） | **本文 `nmea-parser` 0.11.0**（先做 ASCII 过滤 + GSV 修正） |
| 嵌入式 C、无动态分配 | [minmea](./minmea.md) |
| C、可插拔句型模块 | [libnmea](./libnmea.md) |
| Python 快速解析 / 生成 NMEA、NMEA 4.10 信号 ID | [pynmeagps](./pynmeagps.md)（经典 API → [pynmea2](./pynmea2.md)） |
| 守护进程、多客户端、JSON（含 AIS） | [gpsd](./gpsd.md) |
| UBX / RTCM3 二进制 | [ublox](./ublox.md) / [rtcm-rs](./rtcm-rs.md) |
| 观测值转 RINEX | [ubx2rinex](./ubx2rinex.md) |

## 8. 相关

[minmea.md](./minmea.md) · [libnmea.md](./libnmea.md) · [pynmea2.md](./pynmea2.md) · [pynmeagps.md](./pynmeagps.md) · [gpsd.md](./gpsd.md) · [ublox.md](./ublox.md) · [rtcm-rs.md](./rtcm-rs.md) · [ubx2rinex.md](./ubx2rinex.md) · [README.md](./README.md)
