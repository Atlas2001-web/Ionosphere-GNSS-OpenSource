# rinex · Rust RINEX 解析/生成库（nav-solutions）操作手册

目录：[`PROJECTS.json` → `rinex`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/rinex> · crates.io **`rinex` 0.22.0**（**tip 超前** → 仓内 **`0.23.0`**）· tip **`25ca197`**（2026-09-10；RINEX **4.02** NAV）· **MPL-2.0** · MSRV **1.89**（本机 **rustc 1.98.1**）· 本机验证（**2026-09-24 06:36 EDT**）：`cargo build --release`（features 默认+`obs`）；ACOR V3.4 **25** 历元 / G07 **C1C=23818653.24** / **L1C=125167854.812** / 信号 **9036** / `format` **182225** B；同站 `.crx` → `is_crinex` + 同观测；delf V2.11 **105** 历元 · **质检复跑** 2026-09-24 06:40 EDT（tip **`25ca197`**/仓内 **0.23.0**/rustc **1.98.1**；ACOR RNX **25**/C1C=**23818653.24**/L1C=**125167854.812**/信号 **9036**/format **182225** B；`data/CRNX/V3` 同站 `.crx` → `is_crinex` + 同值 / format **77603** B；delf **105**/format **252130** B；交叉 [rinex-cli](./rinex-cli.md)/[georinex](./georinex.md)/[crx2rnx](./crx2rnx.md)/[ionex-rs](./ionex-rs.md)；**未改** 对照页；**未臆造** NAV/IONEX stdout）

> 岗位：把 OBS/NAV/MET/CLK/ANTEX 等 **RINEX 解析进 Rust**，可写回、可 CRX、可挂预处理/QC feature。冲突时：**docs.rs `rinex` / 仓内 README / 本机 binary > 本文**。  
> **CLI QC** → [rinex-cli](./rinex-cli.md)；Python xarray → [georinex](./georinex.md)；C++ 核 → [gnsstk](./gnsstk.md)；IONEX 另库 → [ionex-rs](./ionex-rs.md)；Hatanaka 官方/Python → [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)；仅解压 CLI → [crx2rnx](./crx2rnx.md)；改头 → [rinexmod](./rinexmod.md)；清洗 → [gfzrnx](./gfzrnx.md)。

## 1. 用途与边界

**做：**

- `Rinex::from_file` / `from_gzip_file`；`format(&mut BufWriter<_>)` 写回
- OBS（`obs` feature）：历元迭代、`record.as_obs()`、信号组合等
- 原生读 **CRINEX**（`header.is_crinex()`）；现代 Hatanaka 编解码在库内
- NAV/MET/CLK/ANTEX 等按 feature 增强；可选 `rtcm`/`ublox`/`binex`/`qc`/`processing`/`nav`(anise)
- 与 [rinex-cli](./rinex-cli.md)/[crx2rnx](./crx2rnx.md)/[ubx2rinex](./ubx2rinex.md) 同生态

**不做：**

- **不是** 命令行 QC HTML 工具 → [rinex-cli](./rinex-cli.md)
- **不是** Python `georinex` / pandas 科研读盘 → [georinex](./georinex.md)/[gnsspy](./gnsspy.md)
- **不是** GNSSTK/`RinSum` C++ 栈 → [gnsstk](./gnsstk.md)
- **不是** IONEX 图 → 另仓 [ionex-rs](./ionex-rs.md)（勿 `Rinex::` 硬读 `.I`）
- 上游警告：部分生产写回仍缺功能；Glonass/SBAS/IRNSS **导航解**受限
- crates.io **0.22.0** ≠ tip **0.23.0**——复现请 pin git / 看 `Cargo.toml`

一句话：`rinex` = **Rust RINEX 读写核**；日常脚本优先 georinex，QC 报告用 rinex-cli。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `rinex` | Rust **库** | `cargo add rinex`；无同名 bin |
| [rinex-cli](./rinex-cli.md) | 同生态 **CLI** | `rinex-cli -V` |
| [georinex](./georinex.md) | Python→xarray | `python -m georinex` |
| [gnsstk](./gnsstk.md) | C++ + RinSum | `RinSum --help` |
| [ionex-rs](./ionex-rs.md) | Rust **IONEX** | crate 名 `ionex` |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1（MSRV 1.89）

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/nav-solutions/rinex.git
cd rinex
git rev-parse --short HEAD   # 本机：25ca197

# data/ 是 submodule；.gitmodules 用 HTTPS 时可：
rm -rf data && git clone --depth 1 https://github.com/nav-solutions/data.git data
ls data/OBS/V3/ACOR00ESP_R_20213550000_01D_30S_MO.rnx

# 应用内（crates.io 較旧）：
# cargo add rinex
# tip / 要 4.02 NAV：path 或 git 依赖，features 加 obs
```

最小冒烟 crate：

```toml
# ~/iono_ops/rinex-e2e/Cargo.toml
[package]
name = "rinex-e2e"
version = "0.1.0"
edition = "2021"
[dependencies]
rinex = { path = "../rinex", features = ["obs"] }  # default 已含 flate2+serde
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `msrv`/edition 编不过 | rustc &lt; 1.89 | `rustup update stable` |
| `data/OBS` 空 | 未拉 submodule | `git clone …/data.git data` |
| `format` 类型错 | 要 `BufWriter` | `BufWriter::new(File::create(..))` |
| 找不着信号 API | 未开 `obs` | `features = ["obs"]` |

## 3. 端到端（本机真跑）

```rust
use std::io::BufWriter;
use rinex::prelude::*;

let rnx = Rinex::from_file("data/OBS/V3/ACOR00ESP_R_20213550000_01D_30S_MO.rnx")?;
println!("{}.{} obs={} crinex={}",
    rnx.header.version.major, rnx.header.version.minor,
    rnx.is_observation_rinex(), rnx.header.is_crinex());
println!("epochs {}", rnx.epoch_iter().count());
if let Some(rec) = rnx.record.as_obs() {
    let (k, obs0) = rec.iter().next().unwrap();
    for so in &obs0.signals {
        if so.sv.to_string()=="G07" && so.observable.to_string()=="C1C" {
            println!("G07 C1C {}", so.value);
        }
    }
    let _ = k;
}
let mut out = BufWriter::new(Vec::new());
rnx.format(&mut out)?;
```

**本机 stdout（tip `25ca197`，2026-09-24 06:36 EDT；质检复跑 06:40 EDT 对齐）：**

```text
# ACOR …MO.rnx
version 3.4  is_observation true  is_crinex false  marker ACOR  sampling_s 30
n_epochs 25  epoch_first 2021-12-21T00:00:00 GPST  last …T00:12:00 GPST
n_signal_obs 9036  G07_C1C 23818653.24  G07_L1C 125167854.812
format_bytes 182225

# data/CRNX/V3/ACOR…MO.crx → is_crinex true；C1C/L1C/历元数一致；format_bytes 77603
# data/OBS/V2/delf0010.21o → version 2.11；n_epochs 105；format_bytes 252130
```

G07 C1C 与 [rinex-cli](./rinex-cli.md)/[crx2rnx](./crx2rnx.md)/GSI 对照链一致（**23818653.24**）。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `.rnx` / `.*o` / `.crx` / `.gz` | gzip 走 `from_gzip_file`（默认 `flate2`） |
| NAV/MET/CLK/… | 按 `header.rinex_type`；增强功能开对应 feature |

| 输出 | 说明 |
| --- | --- |
| `Rinex` / `epoch_iter` / `as_obs` | 结构化访问 |
| `format` | 写回文本；CRX 源可写回压缩形态（体积本机 77603） |
| 不输出 | IONEX 格网（→ [ionex-rs](./ionex-rs.md)）；Python xarray |

## 5. 接到哪步

| 场景 | 链接 |
| --- | --- |
| HTML QC / filegen CLI | [rinex-cli](./rinex-cli.md) |
| Python 科研读盘 | [georinex](./georinex.md) |
| 仅 CRX→RNX 小工具 | [crx2rnx](./crx2rnx.md) / [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md) |
| 改头/长短名 | [rinexmod](./rinexmod.md) |
| 批量清洗 | [gfzrnx](./gfzrnx.md) |
| IONEX | [ionex-rs](./ionex-rs.md) / [ionex-gim](./ionex-gim.md) |
| 路径 A | 本库/CLI 探活 → georinex → [pytecgg](./pytecgg.md) |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | crates.io 与 tip API/版本不一致 | **0.22.0** vs **0.23.0** | pin git/`path`；读仓内 `Cargo.toml` |
| 2 | `format(&mut Vec)` 编不过 | 签名要 `BufWriter` | 包一层 `BufWriter` |
| 3 | 无 `as_obs` / 组合迭代 | 缺 `obs` feature | `features = ["obs"]` |
| 4 | `data/` 空导致测试/样例失败 | submodule 未拉 | HTTPS clone `nav-solutions/data` |
| 5 | 把本库当 `rinex-cli` | 库无 HTML QC bin | 装 [rinex-cli](./rinex-cli.md) |
| 6 | 用本库读 IONEX | 格式分仓 | [ionex-rs](./ionex-rs.md) |
| 7 | 与 georinex 比 DataArray | 不同抽象 | Rust 用 `record`；Python 用 xarray |
| 8 | MSRV 报错 | rustc &lt; 1.89 | rustup 升级 |
| 9 | 写回缺字段/不等长 | 生产写回仍补齐中 | 关键归档先 [gfzrnx](./gfzrnx.md)/官方工具 |
| 10 | CRX 当明文 `from_file` 失败 | 实为 Hatanaka | 本库可直读；或先 [crx2rnx](./crx2rnx.md) |
| 11 | ACOR「全日」头 vs **25** 历元 | 样例截断到 12 min | 以 `epoch_iter` 计数为准 |
| 12 | `nav` feature 拉 anise 很重 | 设计如此 | 只要 OBS 时别开 `nav` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust 服务/嵌入解析 RINEX | **本文** |
| Rust QC HTML / 文件手术 | [rinex-cli](./rinex-cli.md) |
| Python 读进 xarray | [georinex](./georinex.md) |
| C++ 全功能+CLI | [gnsstk](./gnsstk.md) |
| IONEX | [ionex-rs](./ionex-rs.md) / [ionex-gim](./ionex-gim.md) |
| 官方 Hatanaka 二进制 | [rnxcmp](./rnxcmp.md) |

## 8. 相关

[rinex-cli](./rinex-cli.md) · [georinex](./georinex.md) · [gnsstk](./gnsstk.md) · [ionex-rs](./ionex-rs.md) · [crx2rnx](./crx2rnx.md) · [hatanaka](./hatanaka.md) · [rnxcmp](./rnxcmp.md) · [rinexmod](./rinexmod.md) · [gfzrnx](./gfzrnx.md) · [ubx2rinex](./ubx2rinex.md) · [README](./README.md)
