# sp3 · IGS SP3 精密轨道解析库操作手册

目录：[`PROJECTS.json` → `sp3`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/sp3> · crates.io **`sp3` 1.4.1** · tip tag **`v1.4.1`=`0ac81cf`**（main 仓内已 **1.5.0**/`12fba37`，**未**发 crates）· **MPL-2.0** · ★**7** · **无 [[bin]]**（纯库）· MSRV **1.82** · 本机验证 **rustc 1.98.1**（2026-09-24 07:18 EDT；**质检复跑 07:25 EDT**：`cargo add sp3@1.4`→**1.4.1**；GRG **96**/75/7200；G15 clock=**−221.978679 µs**；Lagrange11=(**−5993.440743463601**, **20635.00691799316**, **15048.636189188246**) km；gz/`from_gzip_file`；ESA RAP **96**/ESOC/ITRF2/week**2277**；Rev A `NonSupportedRevision`；空/垃圾 `Ok` 空壳；缺路径 panic；写回 dx=**0**）：`cargo add sp3@1.4`→**1.4.1**；[rnx2cggtts](./rnx2cggtts.md) 同源 GRG `…20201770000…ORB.SP3` → epochs **96**/SV **75**/keys **7200**/G15@00:00 xyz=**(5550.690261, −21648.534281, 13744.298178) km**/clock=**−221.978679 µs**；`.gz` 须 `from_gzip_file`（`from_file`→UTF-8 `FileIo`）；Lagrange@12:07:30 order11 ≈**(−5993.440743, 20635.006918, 15048.636189) km**；写回 96→96；Rev A `NonSupportedRevision`；缺路径 **panic**

> 岗位：nav-solutions **IGS SP3** 精密轨道（+可选星钟）文件的 **解析 / 写出 / 拉格朗日插值** Rust 库。冲突时：**上游 README / docs.rs / 本机 `cargo doc -p sp3` > 本文**。  
> 消费本库的共视 CLI → [rnx2cggtts.md](./rnx2cggtts.md)；CGGTTS → [cggtts.md](./cggtts.md)；RINEX → [rinex.md](./rinex.md)/[rinex-cli.md](./rinex-cli.md)；多 AC 钟差合成 → [clkcomb.md](./clkcomb.md)；GFZ 综合登记墙 → [spocc.md](./spocc.md)；Python 轻量 SP3 → [gnsstools.md](./gnsstools.md)。**库 ≠ POD/定位；SP3 ≠ 独立 CLK 产品（本库可读 SP3 内嵌钟列，不是 RINEX CLK 解析器）。**

## 1. 用途与边界

**做：**

- `SP3::from_file` / `from_gzip_file`（默认 feature **`flate2`**）：读明文 / gzip SP3 → `Header` + `BTreeMap<SP3Key, SP3Entry>`
- `to_file`：结构体写回 SP3 文本
- 遍历：`satellites_position_km_iter`、`satellites_clock_offset_sec_iter`（及 drift）
- 插值：`satellite_position_lagrangian_{9,11,17}_interpolation`（奇数阶；需两侧邻域）
- 元数据：`total_epochs` / `first_epoch` / `has_steady_sampling`；文件名合规则 `prod_attributes`
- 可选 feature：`qc` / `processing` / `anise` / `nyx-space`（重）

**不做：**

- **不是** 精密定轨 / PPP / 定位引擎 → [great-podflt.md](./great-podflt.md)/[rtklib.md](./rtklib.md)/[pride-pppar.md](./pride-pppar.md)
- **不是** RINEX CLK 专用产品解析（`.clk` 另库；本库只吃 SP3 正文里的钟列）
- **不是** 多 AC 轨道/钟综合 → [spocc.md](./spocc.md)/[clkcomb.md](./clkcomb.md)
- **不是** CLI：无同名 bin；自写 `main`/`examples`
- Revision **A/B** → `NonSupportedRevision`（只认 **C/D**）

一句话：`sp3` = **SP3 C/D ↔ 结构体 + 插值**；精密产品链的「读轨道」一环，不是解算器。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `sp3` | Rust 纯库 1.4.1 | `cargo add sp3@1.4`；无同名命令 |
| [rnx2cggtts.md](./rnx2cggtts.md) | OBS+NAV+**SP3**→`.ggs` | 内锁旧 `sp3` **1.0.6**；`.sp3.gz` 未开 flate2→panic |
| [gnsstools.md](./gnsstools.md) | Python 读 SP3→pandas | 无 crates；教学壳 |
| [clkcomb.md](./clkcomb.md) | 多 AC **CLK** 合成 | 出 `.clk`，不是本库 API |
| [spocc.md](./spocc.md) | GFZ VCE 综合 | 登记墙；出综合 SP3/CLK |

| 术语 | 含义 |
| --- | --- |
| SP3-c / SP3-d | IGS 修订；本库 **只解析 C/D** |
| `DataType::Position` | 状态向量（位置必有；钟可选） |
| `clock_us` | `SP3Entry` 内单位 **µs**；`satellites_clock_offset_sec_iter` → **秒** |
| `position_km` | ECEF **km**（约 mm 级文本精度） |
| Lagrange 奇阶 | 窗口须居中；文件首/末历元附近常 `None` |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1（≥ MSRV 1.82）

cargo new --bin sp3_demo && cd sp3_demo
cargo add sp3@1.4
# 默认 feature：flate2（gzip）
# 可选：--features qc,processing  或 anise / nyx-space（重）

# tip 对照（可选；仓内已 1.5.0，日常钉 crates）
# git clone https://github.com/nav-solutions/sp3 && cd sp3
# git checkout v1.4.1 && git log -1 --oneline   # 0ac81cf
# git submodule update --init --depth 1 data
# ls data/SP3/C/ESA0OPSRAP_20232390000_01D_15M_ORB.SP3.gz
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `.sp3.gz` + `from_file` | 当文本读 → UTF-8 `FileIo` | `from_gzip_file`；或先 `gunzip` |
| rnx2cggtts 对 gz panic | 其锁 **sp3 1.0.6** 未开 flate2 | 解压后再 `-f`（见 [rnx2cggtts](./rnx2cggtts.md)） |
| `NonSupportedRevision` | Rev A/B | 换 C/D 产品 |
| 缺文件 | `File::open` unwrap | **panic**（非 Result） |
| 跟 tip 1.5.0 | 未发 crates | 生产钉 **1.4.1** |

## 3. 端到端（本机 1.4.1 真跑；2026-09-24 07:18 EDT；质检复跑 07:25 EDT）

样例：[rnx2cggtts.md](./rnx2cggtts.md) 同源 `GRG0MGXFIN_20201770000_01D_15M_ORB.SP3`（明文 **443618 B** / `.gz` **198794 B**）；官方 submodule `ESA0OPSRAP_20232390000_01D_15M_ORB.SP3.gz`。

### 3.1 解析 GRG 明文 + 写回

```rust
use sp3::prelude::*;
use std::str::FromStr;

let sp3 = SP3::from_file("data/GRG0MGXFIN_20201770000_01D_15M_ORB.SP3")?;
assert_eq!(sp3.header.version, Version::C);
assert_eq!(sp3.header.data_type, DataType::Position);
assert_eq!(sp3.header.orbit_type, OrbitType::FIT);
assert_eq!(sp3.header.agency, "GRGS");
assert_eq!(sp3.header.coord_system, "IGb14");
assert_eq!(sp3.header.constellation, Constellation::Mixed);
assert_eq!(sp3.header.timescale, TimeScale::GPST);
assert_eq!(sp3.header.week, 2111);
assert_eq!(sp3.header.sampling_period.to_seconds() as u32, 900);
assert_eq!(sp3.total_epochs(), 96);
assert!(sp3.has_steady_sampling());
assert_eq!(sp3.data.len(), 7200); // 96×75

let sv = SV::from_str("G15")?;
let t0 = Epoch::from_str("2020-06-25T00:00:00 GPST")?;
let e = sp3.data.get(&SP3Key { epoch: t0, sv }).unwrap();
assert!((e.position_km.0 - 5550.690261).abs() < 1e-9);
assert!((e.clock_us.unwrap() - (-221.978679)).abs() < 1e-9);

sp3.to_file("/tmp/sp3_rt.SP3")?;
let back = SP3::from_file("/tmp/sp3_rt.SP3")?;
assert_eq!(back.total_epochs(), 96);
assert_eq!(back.data.len(), 7200);
```

**本机 stdout 要点：**

| 量 | 值 |
| --- | --- |
| version / agency / coord | **C** / **GRGS** / **IGb14** |
| week / sampling | **2111** / **900 s** |
| epochs / unique SV / keys | **96** / **75** / **7200** |
| steady | **true** |
| prod_attributes | agency=**GRG** / Final / DOY **177** / 2020 / Daily / gzip=**false** |
| G01@00:00 GPST xyz | **(−10814.532184, 19731.805009, −14065.684961) km** |
| G01 clock | **15.943802 µs** ≡ **15943.802 ns** |
| G15@00:00 GPST xyz | **(5550.690261, −21648.534281, 13744.298178) km** |
| G15 clock | **−221.978679 µs** ≡ **−221978.679 ns** |
| roundtrip | 96→96；首键位差 **0** |

文件首行原文对照：`#cP2020  6 25 … 96 TRACK IGb14 FIT GRGS`；`PG15   5550.690261 -21648.534281  13744.298178   -221.978679`。

### 3.2 gzip / 官方 ESA RAP / 插值

```rust
// 同内容 gzip
let gz = SP3::from_gzip_file("data/GRG0MGXFIN_20201770000_01D_15M_ORB.SP3.gz")?;
assert_eq!(gz.total_epochs(), 96);

// 官方 Rapid fixture
let esa = SP3::from_gzip_file("data/ESA0OPSRAP_20232390000_01D_15M_ORB.SP3.gz")?;
assert_eq!(esa.header.agency, "ESOC");
assert_eq!(esa.header.coord_system, "ITRF2");
assert_eq!(esa.header.week, 2277);
assert_eq!(esa.total_epochs(), 96);
assert!(esa.prod_attributes.as_ref().unwrap().gzip_compressed);

// 中段插值（首历元两侧不足 → None）
let sv = SV::from_str("G15")?;
let t_off = Epoch::from_str("2020-06-25T12:07:30 GPST")?;
let p11 = sp3.satellite_position_lagrangian_11_interpolation(sv, t_off).unwrap();
// 本机 ≈ (−5993.440743463601, 20635.00691799316, 15048.636189188246) km
let noon = Epoch::from_str("2020-06-25T12:00:00 GPST")?;
let sample = sp3.data.get(&SP3Key { epoch: noon, sv }).unwrap();
// sample xyz ≡ 文件 PG15 @12:00：(-5639.739459, 21438.940199, 14031.689016)
```

**本机插值：**

| 目标 | order9 / 11 / 17 |
| --- | --- |
| G15@12:07:30 GPST | 均有值；11 与 17 在 µm 级内一致 |
| G15@t0（文件首历元） | **None**（无左侧邻域） |

### 3.3 失败边界（如实）

| 输入 | 本机 |
| --- | --- |
| `.SP3.gz` + `from_file` | `Err(File i/o error: stream did not contain valid UTF-8)` |
| Rev A `sio06492.sp3` | `Err(ParsingError(NonSupportedRevision))` |
| 空文件 / `"not an sp3\n"` | **`Ok` 空壳**：version=**D** / epochs=**0** / keys=**0**（不报错） |
| 仅 `#\n` | `Err(ParsingError(MalformedH1))` |
| 路径不存在 | **`panic!("File open error: …")`**（非 Result） |

## 4. 输入 / 输出

| API | 作用 |
| --- | --- |
| `SP3::from_file` / `from_gzip_file` | 读盘；缺文件 panic |
| `SP3::to_file` | 写明文 SP3 |
| `satellites_position_km_iter` | `(Epoch, SV, predicted, maneuver, (x,y,z)_km)` |
| `satellites_clock_offset_sec_iter` | `(Epoch, SV, clock_s)` ← 内部 `clock_us×10⁻⁶` |
| `satellite_position_lagrangian_*` | 奇阶拉格朗日；边缘 `None` |

| 输入 | 说明 |
| --- | --- |
| `.SP3` / `.sp3` 明文 | C/D；A/B 拒 |
| `.sp3.gz` | 默认 flate2：`from_gzip_file` |
| 文件名合 IGS 长名 | 填充 `prod_attributes`（agency/批次/Rapid|Final/DOY…） |

| 输出 | 说明 |
| --- | --- |
| `Header` | version、`DataType`、`OrbitType`、agency、coord、constellation、timescale、week、`sampling_period` |
| `SP3Entry` | `position_km`、可选 `velocity_km_s` / `clock_us` / `clock_drift_ns`、predicted/maneuver 旗 |
| 文件 | `to_file` SP3 文本 |

单位：

| 字段 | 单位 |
| --- | --- |
| `position_km` | **km** |
| `clock_us` | **µs**（×10³→ns；×10⁻⁶→s） |
| `satellites_clock_offset_sec_iter` | **s** |
| `sampling_period` | hifitime `Duration`（本机 GRG=**900 s**） |

## 5. 接到哪一步

```text
IGS/AC SP3(.gz) ──from_gzip_file / gunzip+from_file──► 本文
        │
        ├─► rnx2cggtts（强制 SP3；旧锁注意 flate2）→ CGGTTS
        ├─► 自研 PPP/共视：插值取历元位置/钟
        └─► ≠ clkcomb/spocc（综合产品）≠ great-podflt（定轨）
独立 .CLK 产品 → 勿指望本文；走 CLK 工具链
```

| 上游 | 本库 | 下游 |
| --- | --- | --- |
| CDDIS/WHU SP3 | 解析/插值/写回 | [rnx2cggtts](./rnx2cggtts.md) / 自研 |
| [rinex-cli](./rinex-cli.md) 上下文 | SP3 亦可被 rinex-cli 部分消费 | 勿混岗位 |
| [clkcomb](./clkcomb.md)/[spocc](./spocc.md) | **无直接接口** | 综合后再读落盘 SP3 可用本文 |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | gz + `from_file` UTF-8 错 | 未走 gzip 路径 | `from_gzip_file` 或 gunzip |
| 2 | rnx2cggtts gz panic | 旧 sp3 无 flate2 | 先解压（边界已记 rnx2cggtts） |
| 3 | Rev A/B 失败 | 库只认 C/D | 换现代产品 |
| 4 | 空/垃圾文件 `Ok` 空壳 | 无头行时默认 Header | 查 `total_epochs()==0` |
| 5 | 缺文件 panic | `unwrap_or_else(panic!)` | 先 `Path::exists` |
| 6 | 首末历元插值 `None` | 居中窗口要两侧点 | 用日中；或降低阶/扩文件 |
| 7 | Display 像 UTC | hifitime 打印时标 | 查询键用 `… GPST` 字符串 |
| 8 | 当 POD/PPP | 误解岗位 | 只做文件 I/O+插值 |
| 9 | 当 RINEX CLK 库 | SP3 钟列≠`.clk` | clk 走专用工具 |
| 10 | tip **1.5.0** ≠ crates | 未发布 | 钉 **1.4.1** |
| 11 | 偶数阶插值 | API 要求奇数阶 | 用 9/11/17 |
| 12 | 测完残留 | 临时 crate | `rm -rf` demo；无常驻进程 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust 解析/写出/插值 SP3 C/D | **本文 `sp3` 1.4.1** |
| RINEX→CGGTTS（强制 SP3） | [rnx2cggtts.md](./rnx2cggtts.md) |
| CGGTTS 2E 纯库 | [cggtts.md](./cggtts.md) |
| Python 读 SP3 | [gnsstools.md](./gnsstools.md)/[georinex.md](./georinex.md) |
| 多 AC 钟差合成 | [clkcomb.md](./clkcomb.md) |
| 多 AC 轨道+钟综合（登记） | [spocc.md](./spocc.md) |
| 滤波精密定轨 | [great-podflt.md](./great-podflt.md)（≠ 本库） |

## 8. 相关

[rnx2cggtts.md](./rnx2cggtts.md) · [cggtts.md](./cggtts.md) · [rinex.md](./rinex.md) · [rinex-cli.md](./rinex-cli.md) · [binex.md](./binex.md) · [clkcomb.md](./clkcomb.md) · [spocc.md](./spocc.md) · [gnsstools.md](./gnsstools.md) · [groops.md](./groops.md) · [data-access.md](../data-access.md) · [README.md](./README.md)
