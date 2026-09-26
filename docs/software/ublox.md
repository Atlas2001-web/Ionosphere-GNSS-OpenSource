# ublox · u-blox UBX 协议编解码 Rust 库操作手册

目录：上游 <https://github.com/ublox-rs/ublox> · crates.io **`ublox` 0.10.0**（2026-03-11 发布，下载 **78230**）· tag **`v0.10.0`=`284e7fb`**；master tip **`c9f73ab`**（2026-09-22，领先 tag **23** commit，未发 crates）· **MIT** · ★**84** · 纯库（crate 包 125917 B，**不含** examples）· MSRV **1.88.0** / edition 2021 · 本机 **rustc 1.98.1**（2026-09-26 01:11–01:15 EDT）：上游 `F9T-L2-5min.ubx`（1032742 B）**3066 帧 / 0 错**，与 pyubx2 **1.3.7** 计数逐类一致；NAV-PVT **44.0688095°N / −121.3140302°E / hMSL 1131.618 m**；RAWX **46** 观测，G01 PR **21360867.696 m** / cno **47 dBHz**；默认 `ubx_proto23` 下 NAV-POSECEF/NAV-SIG/MON-RF 落 **`Unknown`**，`ubx_proto31` 全识别；CFG-VALSET **28 B** 与 pyubx2 **逐字节相同**

> 岗位：**UBX 字节流 ↔ Rust 结构体**（帧同步、校验和、按协议版本解码；Builder 生成配置帧）。冲突时：**docs.rs / 本机源码 > 上游 README > 本文**。  
> **编解码库 ≠ 驱动/配置工具 ≠ RINEX 转换。** 转 RINEX → [ubx2rinex](./ubx2rinex.md)（**就是基于本库**，见 §1）；Python 同类 → [pyubx2](./pyubx2.md)；ROS 驱动 → [ublox-dgnss](./ublox-dgnss.md)（ROS 2，C++）/ [ublox-driver](./ublox-driver.md)（ROS 1，C++）；守护进程 → [gpsd](./gpsd.md)。

## 1. 用途与边界

**做：**

- 帧层：`Parser::consume_ubx(&[u8])` 找 `b5 62`、校 Fletcher-8 `CK_A/CK_B`，内部缓冲跨块拼帧
- 混合流：`consume_ubx_rtcm(..)` / `consume_ubx_rtcm_nmea(..)` 同时切出 RTCM3、NMEA 帧（**只切帧不解析**，给 `&[u8]`）
- 消息层：`UbxPacket::Proto23(PacketRef::NavPvt(..))` 等；`#[ubx(scale=..)]` 已缩放（°、m、m/s）
- 编码：`XxxBuilder{..}.into_packet_bytes()`（定长）/ `.extend_to(&mut Vec)`（CFG-VALSET 等变长）
- `no_std`：`ParserBuilder::new().with_fixed_buffer::<N>()`；可选 `serde`

**不做：**

- **不**开串口、不管波特率/重连 → 自己用 `serialport`；上游 examples 里的 `ublox-device` 只是示范封装
- **不**组历元、不写 RINEX → [ubx2rinex](./ubx2rinex.md)
- **不**解析 RTCM/NMEA 内容 → [rtcm-rs](./rtcm-rs.md) / NMEA 库（[pynmeagps](./pynmeagps.md)/[minmea](./minmea.md)）
- **不**定位、不给 TEC；RXM-SFRBX 默认只给原始字，GPS/QZSS 电文解释要开 `sfrbx-gps`（拖入 [gnss-protos](./gnss-protos.md)）

| 易混 | 是什么 | 与本库关系 |
| --- | --- | --- |
| **本文** `ublox` | Rust UBX 编解码层 | `cargo add ublox@0.10.0` |
| [ubx2rinex](./ubx2rinex.md) | Rust CLI：UBX→RINEX | crates 0.3.0 依赖 **`ublox ^0.6`**，git tip `3b67fd0` 依赖 **`ublox 0.8`**（均 `std,sfrbx-gps`）；即本库的下游应用 |
| [pyubx2](./pyubx2.md) | Python 同类（semuconsulting） | 字段名用手册缩写 `prMes`；本库用 snake_case `pr_mes()` |
| [ublox-dgnss](./ublox-dgnss.md) / [ublox-driver](./ublox-driver.md) | ROS 2 / ROS 1 C++ 驱动 | 各自内置 UBX 解析，**不依赖**本库 |
| [gpsd](./gpsd.md) | C 守护进程 | 自带 UBX 驱动，对外出 JSON |
| [rtcm-rs](./rtcm-rs.md) / [binex](./binex.md) / [gnss-protos](./gnss-protos.md) | RTCM3 / BINEX / GPS 电文比特 | 同为 Rust 格式层；`gnss-protos` 是本库 `sfrbx-gps` 的依赖 |

crates.io 反向依赖 **6** 个：`ubx2rinex`、`rinex`、`ubx2cggtts`、`ublox-rnx`、`rgps-daemon`、`rt-navi`。

## 2. 安装与 features

```bash
. "$HOME/.cargo/env"; rustc --version   # 本机 1.98.1（≥ MSRV 1.88.0；0.9.0 为 1.83）
cargo new --bin ubx_demo && cd ubx_demo
cargo add ublox@0.10.0                  # 默认 = std + ubx_proto23；依赖树 15 行（bitflags/chrono/num-traits/derive）
# F9 系（HPG/TIM 固件）建议：
# cargo add ublox@0.10.0 --no-default-features -F std,ubx_proto31
```

| feature | 作用 | 本机观察 |
| --- | --- | --- |
| `ubx_proto23`（默认） | M8 代消息表 | F9T 文件里 NAV-POSECEF(01,01)/NAV-SIG(01,43)/MON-RF(0A,38) → `Unknown` |
| `ubx_proto27` / `ubx_proto31` | F9 代消息表 | F9T 文件 **0 Unknown**；coldstart 文件仍有 14 类 Unknown（见 §3.2） |
| `ubx_proto33` | 0.10.0 新增「基本支持」 | coldstart 里 MON-SPAN/MSGPP/RXBUF/TXBUF 反而变 `Unknown` |
| `ubx_proto14` | 旧 M6 消息 | 未测 |
| `std` / `alloc` | `Vec` 缓冲、`Parser::default()`、`extend_to` | 只开 `ubx_proto23` 时 `Parser::default()` **不存在**（E0599） |
| `serde` | Serialize | 未测 |
| `sfrbx-gps` | 解释 GPS/QZSS SFRBX | ubx2rinex 用 |
| `full` | 全部协议 + serde + sfrbx-gps | 多协议并开见坑 #3 |

上游 examples（workspace 成员，`publish=false`，**不随 crate 发布**）：`simple-parse`、`basic-cli`、`send-receive`、`ublox-tui`（ratatui）、`dds`、公用库 `ublox-device`。全部只收 `-p/--port` 串口，**无文件回放参数**；本机 `simple-parse -p /dev/ttyACM0` → `Error { kind: Io(NotFound) … }`。crates.io 上**没有** `ublox-cli` / `ublox-tui` 包。

## 3. 端到端（本机真跑；2026-09-26 01:11–01:15 EDT）

### 3.1 真实输入：F9T RAWX 录制

```bash
# ubx2rinex 手册同源：nav-solutions/data 子模 UBX/（HTTPS clone ubx2rinex 后 submodule update）
cp ~/iono_ops/ubx2rinex/data/UBX/F9T-L2-5min.ubx.gz . && gunzip -k F9T-L2-5min.ubx.gz
# 1032742 B，sha256 前 12 位 6a3fae80a8b0；另测 16dBatt_no_interference_coldstart.ubx（3000000 B，截断录制）
```

### 3.2 解码 + 计数 + 取字段（`src/main.rs`，完整可编）

```rust
use std::collections::BTreeMap;
use ublox::{proto23::PacketRef, Parser, UbxPacket};

fn main() {
    let path = std::env::args().nth(1).expect("usage: demo <file.ubx>");
    let buf = std::fs::read(&path).unwrap();
    let mut parser = Parser::default(); // Vec 缓冲 + 默认协议（本工程 = Proto23）
    let mut cnt: BTreeMap<String, usize> = BTreeMap::new();
    let (mut errs, mut pvt_shown, mut rawx_shown) = (0usize, false, false);
    let cs: usize = std::env::var("CHUNK").ok().and_then(|s| s.parse().ok()).unwrap_or(4096);
    for chunk in buf.chunks(cs) {               // 模拟串口分块到达
        let mut it = parser.consume_ubx(chunk);
        while let Some(r) = it.next() {         // lending iterator，不能 for
            let p = match r {
                Ok(UbxPacket::Proto23(p)) => p,
                Err(e) => { errs += 1; if errs <= 3 { println!("ERR {e:?}"); } continue; }
            };
            let name = match &p {
                PacketRef::Unknown(u) => format!("Unknown({:02X},{:02X})", u.class, u.msg_id),
                other => format!("{other:?}").split('(').next().unwrap().to_string(),
            };
            *cnt.entry(name).or_default() += 1;
            match p {
                PacketRef::NavPvt(m) if !pvt_shown => {
                    pvt_shown = true;
                    println!("NAV-PVT {:04}-{:02}-{:02} {:02}:{:02}:{:02} nano={} iTOW={} ms fix={:?} numSV={}",
                        m.year(), m.month(), m.day(), m.hour(), m.min(), m.sec(),
                        m.nanosec(), m.itow(), m.fix_type(), m.num_satellites());
                    println!("  lat={:.7}° lon={:.7}° h_ell={:.3} m hMSL={:.3} m hAcc={:.3} m",
                        m.latitude(), m.longitude(), m.height_above_ellipsoid(),
                        m.height_msl(), m.horizontal_accuracy());
                }
                PacketRef::RxmRawx(m) if !rawx_shown => {
                    rawx_shown = true;
                    println!("RXM-RAWX rcvTow={} s week={} leapS={} numMeas={}",
                        m.rcv_tow(), m.week(), m.leap_s(), m.num_meas());
                    for x in m.measurements().filter(|x| x.gnss_id() == 0).take(2) {
                        println!("  gnssId={} sv={} PR={:.3} m CP={:.3} cyc D={:.3} Hz cno={} dBHz",
                            x.gnss_id(), x.sv_id(), x.pr_mes(), x.cp_mes(), x.do_mes(), x.cno());
                    }
                }
                _ => {}
            }
        }
    }
    println!("bytes={} errors={} leftover={}", buf.len(), errs, parser.buffer_len());
    for (k, v) in &cnt { println!("  {k}: {v}"); }
}
```

**本机打印（`cargo run --release -- ../F9T-L2-5min.ubx`，原样摘录）：**

```text
RXM-RAWX rcvTow=163891.001 s week=2379 leapS=18 numMeas=46
  gnssId=0 sv=1 PR=21360867.696 m CP=112252116.071 cyc D=804.339 Hz cno=47 dBHz
  gnssId=0 sv=2 PR=21861985.997 m CP=114885512.628 cyc D=-1426.926 Hz cno=45 dBHz
NAV-PVT 2025-08-11 21:31:13 nano=-92265 iTOW=163891000 ms fix=Fix3D numSV=25
  lat=44.0688095° lon=-121.3140302° h_ell=1110.269 m hMSL=1131.618 m hAcc=0.733 m
bytes=1032742 errors=0 leftover=0
  NavClock: 299  NavDop: 299  NavEoe: 299  NavPvt: 299  NavSat: 299  NavTimeGps: 299
  NavTimeLs: 1  NavVelECEF: 299  RxmRawx: 299
  Unknown(01,01): 299  Unknown(01,43): 299  Unknown(0A,38): 75
```

（计数行为排版合并成三行，数值未改。）合计 **3066** 帧；首历元 RAWX 先于 NAV-PVT 到达（rcvTow 163891.001 s = GPST 21:31:31，NAV-PVT 给 UTC 21:31:13，差 18 s 闰秒）。G01 PR/CP/D 与 [ubx2rinex](./ubx2rinex.md) 首历元 C1C/L1C/D1C 相同。

| 核对 | 结果 |
| --- | --- |
| pyubx2 1.3.7 `UBXReader`（同文件） | 12 类计数**完全一致**（`NAV-POSECEF/NAV-SIG/MON-RF` = 299/299/75，即本库的三个 Unknown） |
| pyubx2 NAV-PVT | `lat=44.0688095 lon=-121.3140302 height=1110269 hMSL=1131618`（mm）numSV=25 |
| pyubx2 RAWX | `numMeas=46`，`prMes_03=21360867.69643313 cno_03=47`（G01） |
| 改 `-F std,ubx_proto31` | 同文件 **0 Unknown**：`NavPosEcef 299 / NavSig 299 / MonRf 75` |
| `CHUNK=1` / `7` / 整读 | 均 3066 帧、leftover 0 |
| coldstart（3000000 B，proto31） | 合计 **31176** = pyubx2；`RxmSfrbx 3843`；leftover **6 B**（尾部截断帧，静默留在缓冲） |
| coldstart 仍 Unknown（proto31） | NAV-TIMEGLO/BDS/GAL/QZSS、SBAS、ORB、GEOFENCE、SVIN、SLAS、TIMETRUSTED、RXM-MEASX(612)、RXM-RLM、MON-SYS、SEC-OSNMA |

### 3.3 编码：CFG-VALSET / CFG-MSG（**本机构造**）

```rust
use ublox::cfg_val::CfgVal::*;
use ublox::packets::{cfg_msg::CfgMsgSinglePortBuilder,
    cfg_val::{CfgLayerSet, CfgValSetBuilder}, nav_pvt::proto23::NavPvt};
let mut v = Vec::new();
CfgValSetBuilder { version: 0, layers: CfgLayerSet::RAM, reserved1: 0,
    cfg_data: &[MsgOutUbxRxmRawxUsb(1), MsgOutUbxNavPvtUsb(1), RateMeas(1000)] }
    .extend_to(&mut v);
let m = CfgMsgSinglePortBuilder::set_rate_for::<NavPvt>(1).into_packet_bytes();
```

```text
CFG-VALSET 28 B: b5 62 06 8a 14 00 00 01 00 00 a7 02 91 20 01 09 00 91 20 01 01 00 21 30 e8 03 f8 59
CFG-MSG    11 B: b5 62 06 01 03 00 01 07 01 13 51
```

pyubx2 `UBXMessage.config_set(SET_LAYER_RAM, TXN_NONE, [("CFG_MSGOUT_UBX_RXM_RAWX_USB",1),("CFG_MSGOUT_UBX_NAV_PVT_USB",1),("CFG_RATE_MEAS",1000)])` → **同 28 字节**。CFG-MSG 这里是 3 B 载荷「当前端口」形式；pyubx2 `UBXMessage("CFG","CFG-MSG",SET,msgClass=1,msgID=7,rateDDC=1)` 生成的是 8 B 六端口形式（`…08 00 01 07 01 00 00 00 00 00 18 e2`），对应本库 `CfgMsgAllPortsBuilder`。

### 3.4 失败边界（本机如实；输入由 F9T 首条真实 NAV-PVT 帧改造，载荷 92 B / 帧 100 B）

| 输入 | `consume_ubx` | `consume_ubx_rtcm_nmea` |
| --- | --- | --- |
| 原帧 | `NavPvt`，缓冲 0 | `Ubx(NavPvt)` |
| 翻 CK_B | `Err(InvalidChecksum{expect:24695, got:40823})` | 同 |
| 载荷翻 1 bit | `Err(InvalidChecksum{..})` | 同 |
| 截掉尾 8 B | 无输出，缓冲留 **92 B**（等数据） | 同 |
| `GARBAGE\xb5\x00` 前缀 + 帧 | `NavPvt`（垃圾静默跳过） | 同 |
| `$GPGGA…*66\r\n` + 帧 | `NavPvt`（NMEA 静默丢） | `Nmea("$GPGGA…")` + `Ubx(NavPvt)` |
| 截断帧 + 完整帧 | `Err(InvalidChecksum)` + `NavPvt` | 同 |
| 假头 `b5 62 02 15 ff ff` + 帧 | `NavPvt`（超协议表最大载荷，直接弃同步字） | 同 |
| 假头宣称 0x1000 B + 帧 | **无输出**，缓冲 106 B（挡住后面好帧） | 同 |
| 同上 + 再喂 6000 B 真流 | 1 个 `InvalidChecksum` 后**逐帧恢复**，无丢帧 | 同 |
| `with_fixed_buffer::<1024>()` 读 F9T | `OutOfMemory{required_size:1194/1490/…}` **247** 次：RAWX 丢 108、NAV-SIG 丢 139 | — |

校验错只丢 2 字节同步头再重扫，所以错帧不会连坐后续帧；但伪长度落在合法范围内时会**阻塞到攒够字节**。

## 4. 输入 / 输出

| API | 作用 |
| --- | --- |
| `Parser::default()` / `ParserBuilder::new().with_protocol::<P>().with_vec_buffer()` | 建解析器；多协议并开时必须显式 `with_protocol` |
| `with_fixed_buffer::<N>()` | no_std 定长；N 须 ≥ 最大期望载荷 + 8 |
| `consume_ubx(&[u8]) -> UbxParserIter` | `.next() -> Option<Result<UbxPacket, ParserError>>`；`None` = 缓冲不够一帧 |
| `consume_ubx_rtcm_nmea` | `AnyPacketRef::{Ubx, Rtcm, Nmea}`；后两者只给 `data: &[u8]` |
| `PacketRef::Unknown(UbxUnknownPacketRef{class,msg_id,payload})` | 当前协议表里没有的消息 |
| `p.to_owned()` | 转成可 move 的 `*Owned` |
| `XxxBuilder{..}.into_packet_bytes()` / `.extend_to(&mut Vec)` | 编码，含同步头与校验和 |

| 输出字段 | 单位 |
| --- | --- |
| `latitude()`/`longitude()` | °（1e-7 缩放已做） |
| `height_above_ellipsoid()`/`height_msl()`/`horizontal_accuracy()` | m |
| `pr_mes()` / `cp_mes()` / `do_mes()` | m / cycle / Hz |
| `cno()` | dBHz（u8） |
| `itow()` | ms；`rcv_tow()` s（f64） |

## 5. 接到哪一步

```text
u-blox 串口/USB ──serialport──> 字节块 ──本文 Parser──> NavPvt / RxmRawx / RxmSfrbx
   ├─ 要 RINEX → ubx2rinex（就是用本库 + sfrbx-gps 写的）
   ├─ RTCM 帧 → consume_ubx_rtcm 切出 → rtcm-rs 解析 / ntripserver 推流
   ├─ 要 ROS 话题 → ublox-dgnss / ublox-driver（自带解析，不经本库）
   └─ 配置接收机 → CfgValSetBuilder 生成帧写串口（等 ACK-ACK 自己判）
Python 脚本 / 快速看字段 → pyubx2（同一文件计数可互校）
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | F9 数据里 NAV-SIG/NAV-POSECEF/MON-RF 全是 `Unknown` | 默认 `ubx_proto23` 是 M8 消息表 | F9 用 `--no-default-features -F std,ubx_proto31`；先统计 Unknown 再下结论 |
| 2 | `ubx_proto33` 下 MON-SPAN 等反而 Unknown | 0.10.0 对 33 仅「基本支持」 | F9 优先 31；按实际文件核对 |
| 3 | 开两个 proto 后 `Parser::default()` 报 E0283 | 多个 `Default` impl | `ParserBuilder::new().with_protocol::<Proto31>().with_vec_buffer()`；match 须覆盖所有 `UbxPacket::ProtoNN` 变体 |
| 4 | 关 `std` 后 `Parser::default` 不存在 | 只在 std/alloc 下实现 | `with_fixed_buffer::<N>()` |
| 5 | 定长缓冲大量 `OutOfMemory` | RAWX 46 星 ≈ 1.5 KB > N | N ≥ 8184（RAWX 上限 8176 + 8）或按实际星数估 |
| 6 | README 例 `use ublox::CfgValSetBuilder` 编不过 | 0.10.0 Builder 在 `ublox::packets::<模块>::` 下 | 按 §3.3 的路径导入；以 docs.rs 为准 |
| 7 | `for p in it` 报错 | lending iterator | `while let Some(r) = it.next()` |
| 8 | NMEA/垃圾无声消失 | `consume_ubx` 只认 UBX | 需要 NMEA/RTCM 用 `consume_ubx_rtcm_nmea` |
| 9 | 截断录制尾部几字节 | 留在内部缓冲，不报错 | 结束时查 `parser.buffer_len()` |
| 10 | 伪长度帧挡住后续数据 | 需攒够声明长度才校验 | 流式无妨（自动恢复）；离线文件末尾检查 leftover |
| 11 | SFRBX 只有原始字 | 解释需 `sfrbx-gps` | 开 feature，或交给 ubx2rinex |
| 12 | 想跑上游 examples 却无硬件 | 只收 `-p` 串口、不随 crate 发布 | 离线用 §3.2 读文件；`socat` 造 pty 回放可行性本篇未测 |
| 13 | ubx2rinex 与本库版本不同步 | 下游钉 0.6 / 0.8 | 同一工程混用时以 `cargo tree -i ublox` 查重复 |
| 14 | MSRV 突跳（0.9→0.10：1.83→1.88） | 上游声明补丁版也可升 MSRV | 旧工具链钉 `=0.9.0` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust / 嵌入式解 UBX、生成 CFG 帧 | **本文 `ublox` 0.10.0** |
| Python 解析 / 构造 UBX | [pyubx2](./pyubx2.md)（CLI 在 [pygnssutils](./pygnssutils.md)） |
| UBX（含 RAWX）→ RINEX | [ubx2rinex](./ubx2rinex.md) |
| ROS 2 / ROS 1 接 F9P | [ublox-dgnss](./ublox-dgnss.md) / [ublox-driver](./ublox-driver.md) |
| 多厂商守护进程、JSON 输出 | [gpsd](./gpsd.md) |
| RTCM3 / BINEX / GPS 电文比特 | [rtcm-rs](./rtcm-rs.md) / [binex](./binex.md) / [gnss-protos](./gnss-protos.md) |
| Septentrio SBF | [pysbf2](./pysbf2.md) / [sbfparser](./sbfparser.md) |

## 8. 相关

[pyubx2.md](./pyubx2.md) · [ubx2rinex.md](./ubx2rinex.md) · [ublox-dgnss.md](./ublox-dgnss.md) · [ublox-driver.md](./ublox-driver.md) · [gpsd.md](./gpsd.md) · [rtcm-rs.md](./rtcm-rs.md) · [binex.md](./binex.md) · [gnss-protos.md](./gnss-protos.md) · [pygnssutils.md](./pygnssutils.md) · [pynmeagps.md](./pynmeagps.md) · [README.md](./README.md)
