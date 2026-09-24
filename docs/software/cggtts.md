# cggtts · CGGTTS 解析/合成库操作手册

目录：[`PROJECTS.json` → `cggtts`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/cggtts> · crates.io **`cggtts` 4.4.0** · tip **`fc75b91`**（2026-09-08；仓内 `Cargo.toml` **4.4.0**/edition tip 2024，crates 发布 edition **2018**）· **MPL-2.0** · ★**18** · **无 [[bin]]**（纯库）· MSRV **1.82.0** · 本机验证 **rustc 1.98.1**（2026-09-24 07:09 EDT；**质检复跑 07:17 EDT**：fixture `GZGTR560.258` **271219** B → tracks **2097**/G08 REFSV=**151304.2 ns**/REFSYS=**−28.1 ns**/ELV=**24.5°**/TRKL=**780 s**/MSIO=**5.7 ns**；写回再读齐；`cargo test --lib tests::parser` **4**/4；ESBC 补丁后 tracks **169**/station **ESBC00DNK**/unique SAT **24**/G15@024600 C1C REFSV=**258796.8 ns**/REFSYS=**480750.6 ns**/ELV=**70.8°**/AZTH=**237.9°**/TRKL=**960 s**/DSG=**42.0 ns**）：官方 fixture `GZGTR560.258` → tracks **2097**/G08 REFSV=**151304.2 ns**/ELV=**24.5°**/TRKL=**780 s**/MSIO 有；写回再读齐；`rnx2cggtts` 产物 ESBC `.ggs` 须改 VERSION 空格+XYZ ` m`+RCVR 三元组 + `from_file_infaillible_crc` → tracks **169**/G15@024600 C1C REFSV=**258796.8 ns**/REFSYS=**480750.6 ns**/ELV=**70.8°**/TRKL=**960 s**

> 岗位：nav-solutions **CGGTTS 2E** 文件的 **Header/Track 解析与合成** Rust 库。冲突时：**上游 README / docs.rs / 本机 `cargo doc -p cggtts` > 本文**。  
> RINEX→CGGTTS **CLI** → [rnx2cggtts.md](./rnx2cggtts.md)；RINEX→BINEX → [rinex2bin.md](./rinex2bin.md)；钟差综合 → [clkcomb.md](./clkcomb.md)；RINEX 库/CLI → [rinex.md](./rinex.md)/[rinex-cli.md](./rinex-cli.md)。

## 1. 用途与边界

**做：**

- `CGGTTS::from_file` / `parse`：读 **2E** 文件 → `Header` + `Vec<Track>`
- `to_file` / `format`：把内存结构写回标准 2E
- `Track::new` / `TrackData` / 可选 `IonosphericData`：手工合成轨
- 查询：`is_gps_cggtts`、`has_ionospheric_data`、`follows_bipm_tracking`（轨长是否 **780 s**）、`single_channel`
- feature：`scheduler`（共视日程）、`tracker`（拟合）、`logs`

**不做：**

- **不是** 定位/PPP/TEC 引擎 → [rtklib.md](./rtklib.md)/[georinex.md](./georinex.md)/[pytecgg.md](./pytecgg.md)
- **不是** RINEX→CGGTTS 流水线 → [rnx2cggtts.md](./rnx2cggtts.md)（本库只吃/吐 `.ggs`/`.258` 文本）
- **不是** 完整 BIPM 双边共视比对（差两站轨、选共视对、OTC）——库停在文件层
- **不是** CLI：无同名 bin；自写 `main`/`examples`
- 只认 revision **2E**；其它版本 → `NonSupportedRevision` / `VersionFormat`

一句话：`cggtts` = **CGGTTS 2E ↔ 结构体**；时间传递产品链的「读/写文件」一环，不是解算器。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `cggtts` | Rust 纯库 4.4 | `cargo add cggtts@4.4`；无同名命令 |
| [rnx2cggtts.md](./rnx2cggtts.md) | OBS+NAV+SP3→`.ggs` CLI | `rnx2cggtts -V` → `1.0.2` |
| [rinex2bin.md](./rinex2bin.md) | RINEX→BINEX | 二进制交换，非共视轨 |
| [clkcomb.md](./clkcomb.md) | 多 AC 钟差合成 | 出 CLK，不出 CGGTTS |

| 术语 | 含义 |
| --- | --- |
| CGGTTS 2E | BIPM 共视格式；本库**只吃 2E** |
| REFSV / REFSYS | 相对星钟 / 系统时差；文件列单位 **0.1 ns** → 库内 **秒** |
| TRKL / `duration` | 跟踪时长；BIPM 默轨 **780 s** |
| ELV / AZTH | 仰角/方位；文件 **0.1°** → 库内 **度** |
| `follows_bipm_tracking` | 仅检查 `duration == 780 s`，不验证拟合算法 |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1（≥ MSRV 1.82）

cargo new --bin cggtts_demo && cd cggtts_demo
cargo add cggtts@4.4
# 可选：cargo add cggtts@4.4 --features scheduler,tracker,logs

# 官方样例（submodule data）：
# git clone https://github.com/nav-solutions/cggtts && cd cggtts
# git submodule update --init --depth 1 data
# ls data/CGGTTS/GZGTR560.258
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `VersionFormat` | 首行不是 `CGGTTS     GENERIC…`（**5** 空格） | 改空格；或换官方 fixture |
| `ChecksumError` | 改过头字段 | `from_file_infaillible_crc` |
| RCVR `InvalidFormat` | 第 4 段当年份 `u16` 溢出（如序列号 3047937） | 收成 3 段：`厂商 型号 序列号` |
| 缺文件 | `from_file` **panic**（非 Result） | 先 `Path::exists` |

## 3. 端到端（本机 4.4.0 真跑；2026-09-24 07:09 EDT）

### 3.1 解析官方 fixture + 写回

样例：上游 submodule `data/CGGTTS/GZGTR560.258`（本机 **271219 B** / 数据行 **2097**）。

```rust
use cggtts::prelude::{CGGTTS, CommonViewClass};
use hifitime::Unit;

let cgg = CGGTTS::from_file("data/GZGTR560.258")?;
assert_eq!(cgg.header.station, "LAB");
assert_eq!(cgg.tracks.len(), 2097);
assert!(cgg.is_gps_cggtts());
assert!(cgg.has_ionospheric_data());
assert!(cgg.follows_bipm_tracking()); // 全部 TRKL=780 s
assert!(!cgg.single_channel());

let t0 = &cgg.tracks[0];
assert_eq!(t0.sv.to_string(), "G08");
assert_eq!(t0.class, CommonViewClass::MultiChannel); // FF
assert_eq!(t0.epoch.to_mjd_utc(Unit::Day).floor() as u32, 60258);
assert_eq!(t0.duration.to_seconds() as u32, 780);
assert!((t0.elevation_deg - 24.5).abs() < 1e-9);
assert!((t0.azimuth_deg - 295.4).abs() < 1e-9);
assert!((t0.data.refsv * 1e9 - 151304.2).abs() < 0.05); // 秒→ns
assert!((t0.data.refsys * 1e9 - (-28.1)).abs() < 0.05);
assert_eq!(t0.frc, "L1C");
assert!(t0.iono.is_some());

cgg.to_file("/tmp/cggtts_rt.ggs")?;
let back = CGGTTS::from_file("/tmp/cggtts_rt.ggs")?;
assert_eq!(back.tracks.len(), 2097);
assert!((back.tracks[0].data.refsv - t0.data.refsv).abs() < 1e-15);
```

**本机 stdout 要点：**

| 量 | 值 |
| --- | --- |
| station / channels | **LAB** / **20** |
| APC XYZ | **3970727.80 / 1018888.02 / 4870276.84 m** |
| tracks / cal | **2097** / `CalibrationID { process_id: **1015**, year: **2021** }` |
| T0 SV/FRC/class | **G08** / **L1C** / MultiChannel |
| T0 REFSV / REFSYS | **151304.2 ns** / **−28.1 ns** |
| T0 ELV / AZTH / TRKL | **24.5°** / **295.4°** / **780 s** |
| T0 MSIO（iono） | **5.7 ns** |
| roundtrip | tracks **2097→2097**；REFSV bit 齐 |

### 3.2 读 `rnx2cggtts` 产物（须补丁）

同源：[rnx2cggtts.md](./rnx2cggtts.md) 的 `ESBC-GPS-SPP-2h.ggs`（**169** TRACK / **24** SAT；G15@024600 C1C）。

```text
# 原始首行（1 空格）→ VersionFormat
CGGTTS GENERIC DATA FORMAT VERSION = 2E

# 库要求（5 空格）
CGGTTS     GENERIC DATA FORMAT VERSION = 2E
```

另两处本机必改：

1. `X/Y/Z = …` 末尾加 **` m`**（解析用 `line[..len-1]`，无单位会吞掉末位数字）
2. `RCVR`/`IMS` 收成三元组（否则序列号进 `year: u16` 溢出 → `InvalidFormat`）  
   例：`RCVR = SEPT POLARX5 3047937`

改头后 CRC 失配 → 用 **`CGGTTS::from_file_infaillible_crc`**。

**本机（补丁后）：**

| 量 | 值 |
| --- | --- |
| station / tracks | **ESBC00DNK** / **169** |
| has_iono / bipm_all / single_ch | **false** / **false** / **true** |
| APC XYZ | **3582105.291 / 532589.7313 / 5232754.8054 m** |
| G15@024600 C1C ELV/AZTH | **70.8°** / **237.9°** |
| G15 REFSV / REFSYS / DSG | **258796.8 ns** / **480750.6 ns** / **42.0 ns** |
| G15 TRKL | **960 s** → `follows_bipm_tracking()==false` |
| unique SAT | **24**（G01…G32 子集） |

与 [rnx2cggtts.md](./rnx2cggtts.md) 表内 G15 C1C 物理量**一致**（同一 `.ggs`）。

### 3.3 合成轨 → 写盘 → 读回

```rust
use cggtts::prelude::*;
use std::str::FromStr;

let data = TrackData {
    refsv: 1235.0 * 0.1e-9, // 123.5 ns（按 0.1 ns 量子）
    srsv: 10.0 * 0.1e-12,
    refsys: -50.0 * 0.1e-9,
    srsys: -2.0 * 0.1e-12,
    dsg: 3.0 * 0.1e-9,
    ioe: 12,
    mdtr: 100.0 * 0.1e-9,
    smdt: -5.0 * 0.1e-12,
    mdio: 40.0 * 0.1e-9,
    smdi: -1.0 * 0.1e-12,
};
let trk = Track::new(
    SV::from_str("G01")?,
    Epoch::from_str("2024-01-01T00:10:00 UTC")?,
    Duration::from_seconds(780.0),
    CommonViewClass::SingleChannel,
    45.0,
    120.0,
    data,
    None,
    0,
    "C1C",
);
let header = Header::default()
    .with_station("DEMO")
    .with_channels(12)
    .with_receiver_hardware(
        Hardware::default()
            .with_manufacturer("DEMO")
            .with_model("RX")
            .with_serial_number("1"),
    )
    .with_apc_coordinates(Coordinates { x: 1e6, y: 2e6, z: 3e6 })
    .with_reference_frame("ITRF")
    .with_utc_reference_time()
    .with_comment("demo");
let doc = CGGTTS { header, tracks: vec![trk] };
doc.to_file("/tmp/cggtts_synth.ggs")?;
let back = CGGTTS::from_file("/tmp/cggtts_synth.ggs")?;
assert!((back.tracks[0].data.refsv * 1e9 - 123.5).abs() < 0.05);
assert!(back.tracks[0].follows_bipm_tracking());
```

**本机：** synth REFSV=**123.5 ns** / TRKL=**780 s** / FRC=**C1C** / station=**DEMO**；非 0.1 ns 整数倍会在写盘时量子化（勿断言 123.45）。

### 3.4 失败边界（如实）

| 输入 | 本机 |
| --- | --- |
| 空文件 | `Err(VersionFormat)` |
| `…VERSION = 1A` | `Err(NonSupportedRevision)` |
| ESBC 原始（1 空格 VERSION） | `Err(VersionFormat)` |
| 补丁后严格 `from_file` | `Err(ChecksumError)`（头改过） |
| 路径不存在 | **`panic!("File open error: …")`**（非 Result） |

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `.ggs` / `.258` 等 2E 文本 | `from_file` / `from_file_infaillible_crc` / `parse` |
| 可选 gzip | feature 视发布；4.4.0 默认无强依赖 |

| 输出 | 说明 |
| --- | --- |
| `Header` | station、receiver/IMS `Hardware`、APC、`SystemDelay`、comments… |
| `Track` | `sv`/`epoch`/`duration`/`elevation_deg`/`azimuth_deg`/`data`/`iono`/`frc`/`hc` |
| `TrackData` | `refsv`/`srsv`/`refsys`/`srsys`/`dsg`/`ioe`/`mdtr`/`smdt`/`mdio`/`smdi`（**秒**） |
| 文件 | `to_file` 标准 2E 文本 |

单位换算（读文件后）：

| 文件列 | 库字段 | 到常用单位 |
| --- | --- | --- |
| REFSV（0.1 ns） | `data.refsv`（s） | `×1e9` → ns |
| SRSV（0.1 ps/s） | `data.srsv`（s/s） | `×1e12` → ps/s |
| ELV（0.1°） | `elevation_deg` | 已是度 |

## 5. 接到哪一步

| 上游 | 本库 | 下游 |
| --- | --- | --- |
| [rnx2cggtts.md](./rnx2cggtts.md) 写出 `.ggs` | 解析/质检/改头再写 | 两站交换后自写共视差（本仓无专用比对 CLI） |
| 实验室接收机原生 CGGTTS | 直接 `from_file` | 归档 / 与 BIPM 日程对齐（`scheduler` feature） |
| [rinex2bin.md](./rinex2bin.md) | **无直接接口**（BINEX≠CGGTTS） | 勿混 |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `VersionFormat` | VERSION 行空格≠5 | 对齐 `CGGTTS     GENERIC…` |
| 2 | XYZ 末位错 | 解析掐末字符 | 坐标行加 ` m` |
| 3 | RCVR 解析炸 | 年份槽吃到序列号 | 三元组硬件行 |
| 4 | 改头后 CRC 失败 | 校验和未重算 | `from_file_infaillible_crc` |
| 5 | 缺文件 panic | `File::open` unwrap | 先存在性检查 |
| 6 | `follows_bipm_tracking==false` | TRKL≠780（如 rnx2cggtts 默认 **960 s**） | 勿当“轨无效”；只说明非 BIPM 默长 |
| 7 | 合成值读回偏移 | 写盘按 0.1 ns 量子 | 用整数个 0.1 ns |
| 8 | 当 TEC/定位输出 | 误解岗位 | 只做共视文件 I/O |
| 9 | 与 tip edition 2024 混用 | crates 4.4.0 仍 edition 2018 | 日常钉 crates；跟 tip 自备 nightly/新 stable |
| 10 | `scheduler`/`tracker` 找不到 | feature 未开 | `--features scheduler,tracker` |
| 11 | 混星座文件 | 库假定单星座 tracks | 按星座拆文件 |
| 12 | 测完留进程 | 无后台服务 | 无常驻；清 `/tmp` 试写即可 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 解析/合成 CGGTTS 2E | **本文 `cggtts` 4.4** |
| RINEX→CGGTTS CLI | [rnx2cggtts.md](./rnx2cggtts.md) |
| RINEX→BINEX | [rinex2bin.md](./rinex2bin.md) |
| 多 AC 钟差 CLK | [clkcomb.md](./clkcomb.md) |
| SP3 轨道库 | 待写 `sp3`（crates nav-solutions）；勿与本库混 |

## 8. 相关

[rnx2cggtts.md](./rnx2cggtts.md) · [rinex2bin.md](./rinex2bin.md) · [rinex.md](./rinex.md) · [rinex-cli.md](./rinex-cli.md) · [clkcomb.md](./clkcomb.md) · [georinex.md](./georinex.md) · [ubx2rinex.md](./ubx2rinex.md) · [data-access.md](../data-access.md) · [README.md](./README.md)
