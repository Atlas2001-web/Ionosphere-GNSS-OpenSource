# ionex-rs · Rust IONEX 解析库操作手册

目录：[`PROJECTS.json` → `ionex-rs`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/ionex> · crates.io **`ionex` 0.1.0** · tip **`bcb9171`** · **MPL-2.0** · MSRV 标 1.82（依赖实际常要 **≥1.88**；本机 **rustc 1.98.1**）· 本机验证：读 `CKMG0020.22I.gz` → 129575 点 / 25 图；格点 87.5°N/−180° = **9.2 TECU**；`format` 往返 807703 B · 2026-09-24 04:39 EDT · **质检复跑通过**（同 I/O，2026-09-24 04:44 EDT）

> 岗位：把 IONEX（全球/区域 TEC 格网）**解析进 Rust**，可写回 2D、可按格点索引。冲突时：**上游 README / docs.rs `ionex` / 本机 `cargo doc -p ionex` > 本文**。Python 科研读图 → [ionex-gim](./ionex-gim.md)（`gnss-lab/ionex`）；两图对照 → [diffionmap](./diffionmap.md)；GIM 边界 → [sh-gim](./sh-gim.md)。

## 1. 用途与边界

**做：**

- 解压/读 `.I` / `.i` / `.gz` IONEX（默认开 `flate2`）
- 头：`version`、壳高、经纬网格、采样、首末历元；体：`(Epoch, lat, lon, alt) → TEC`
- 2D 图写回（`format`）、标准化文件名、`MapCell` 空间邻域（插值在 cell API）
- 嵌进 nav-solutions / GeoRust 栈（`hifitime` 历元、`geo` 几何）

**不做：**

- **不是** Python 包 `ionex` → 见 [ionex-gim](./ionex-gim.md)
- **不是** 球谐建图 / 写分析中心产品 → [sh-gim](./sh-gim.md) 边界 + lists 其它 GIM
- **不是** 单站 STEC/ROTI → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- **Height map** 尚不支持（上游 Limitations）
- tip 的 `cargo test`（含 `qc` 等）可能因依赖 API 漂移编不过——**以 `cargo build` + 自写 binary 冒烟为准**

一句话：ionex-rs = **Rust 侧 IONEX 读写核**；日常画图/脚本仍优先 Python `ionex`。

| 符号 | 含义 |
| --- | --- |
| `IONEX` | 头 + `Record` + 可选 IGS 文件名属性 |
| `Key` | `(Epoch, QuantizedCoordinates)` 索引 |
| `TEC` | 电子含量；`tecu()` |
| `MapCell` | 四角格，供邻域/插值工作流 |
| `from_gzip_file` / `from_file` / `format` | 读 gz / 明文 / 写回 |

## 2. 安装

```bash
# 推荐 rustup（系统 apt rustc 1.85 常不够：geo 要 ≥1.88）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/nav-solutions/ionex.git ionex-rs
cd ionex-rs
# data/ 是 submodule，且 .gitmodules 常写 git@ —— 改 HTTPS：
rm -rf data
git clone --depth 1 https://github.com/nav-solutions/data.git data
ls data/IONEX/V1/CKMG0020.22I.gz

cargo build --release
# 期望：Finished `release` …（warning 可忽略）
```

crates.io：`cargo add ionex`（与 tip API 以 docs.rs 为准）。

最小依赖示例 crate（本机 E2E 用）：

```toml
# ~/iono_ops/ionex-rs-e2e/Cargo.toml
[package]
name = "ionex-rs-e2e"
version = "0.1.0"
edition = "2021"
[dependencies]
ionex = { path = "../ionex-rs" }
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `geo … requires rustc 1.88` | 系统 rustc 过旧 | `. "$HOME/.cargo/env"`；`rustup update` |
| `data/IONEX` 空 / SSH 失败 | submodule 用 `git@` | `git clone https://github.com/nav-solutions/data.git data` |
| `cargo test` E0432/E0599 | tip 测试/`qc` 与依赖不同步 | `cargo build --release`；自写 `main` 冒烟 |

## 3. 端到端：CKMG gzip → 格点 TEC → 写回（本机真跑）

数据：`data/IONEX/V1/CKMG0020.22I.gz`（CODE Klobuchar 风格日图，壳高 350 km，25 张 × 1 h）。

```bash
cd ~/iono_ops/ionex-rs-e2e   # 或任意 path 依赖 ionex 的 bin
cargo run --release -- ../ionex-rs/data/IONEX/V1/CKMG0020.22I.gz
```

示例 `main.rs` 核心：

```rust
use std::str::FromStr;
use ionex::prelude::*;

let ionex = IONEX::from_gzip_file(path).unwrap();
println!("version {}.{}", ionex.header.version.major, ionex.header.version.minor);
println!("n_record {}", ionex.record.iter().count());
println!("std_name {}", ionex.generate_standardized_filename());
let epoch = Epoch::from_str("2022-01-02T00:00:00 UTC").unwrap();
let key = Key::from_decimal_degrees_km(epoch, 87.5, -180.0, 350.0);
println!("tec {}", ionex.record.get(&key).unwrap().tecu());
// format 需 BufWriter：ionex.format(&mut BufWriter::new(File::create("out.I")?))?;
```

**本机 stdout（tip `bcb9171` + rustc 1.98.1，2026-09-24 04:39 EDT）：**

```text
path ../ionex-rs/data/IONEX/V1/CKMG0020.22I.gz
version 1.0
is_2d true
alt_km 350..350 width 0
base_radius_km 6371
sampling_ns 3600000000000
epoch_first 2022-01-02T00:00:00 UTC last 2022-01-03T00:00:00 UTC
n_record 129575 n_epochs 25
std_name CKMG0020.22I.gz
attr agency=CKM region=Worldwide year=2022 doy=2
tec@87.5,-180 = 9.2 TECU (OK)
tec@40,140 = 12.7 TECU
roundtrip n_record 129575 ver 1.0 bytes 807703
```

头字段交叉核对（`gzip -dc … \| head`）：`INTERVAL 3600`、`# OF MAPS 25`、`HGT 350`、`LAT 87.5…-2.5`、`LON -180…5.0`、`EXPONENT -1`。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IONEX 文本 / `.gz` | IGS 风格名可填 `attributes`；非标准名仍可解析 |
| 格点键 | 必须落在量化网格上；`get` **不插值** |

| 输出 | 说明 |
| --- | --- |
| `IONEX` / `TEC` | `tecu()` 已按 EXPONENT 还原 |
| `format` 文本 | 2D（含 RMS 图支持见上游）；往返后 `n_record` 应一致 |
| 不输出 | 球谐系数、STEC、ROTI、Height map |

## 5. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| Python 快速读图/画图 | [ionex-gim](./ionex-gim.md) |
| 两中心 IONEX 并排 | [diffionmap](./diffionmap.md) |
| GIM 课 / 多图对照 | [03](../tutorials/03-gim-ionex.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 自建边界 | [sh-gim](./sh-gim.md) · [10](../tutorials/10-build-gim-workflow.md) |
| 下载产品 | [data-access](../data-access.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `requires rustc 1.88` | apt `rustc` 偏旧 | `rustup update stable && . "$HOME/.cargo/env"` |
| 2 | clone 后无 `data/IONEX` | submodule SSH/`data/*` 空 | `git clone https://github.com/nav-solutions/data.git data` |
| 3 | `cargo test` 编不过 | tip 测试与 `geo`/qc API 漂移 | `cargo build --release`；用 path 依赖跑 binary |
| 4 | `record.len()` 无方法 | `Record` 未暴露 `len` | `ionex.record.iter().count()` |
| 5 | 找不到 `QuantizedCoordinates` | 未进 `prelude` | `Key::from_decimal_degrees_km(epoch, lat, lon, alt_km)` |
| 6 | `get` 得 `None` | 点不在网格 / 历元字符串错 | 先 `epochs_iter`；纬向 −2.5°、经向 5° 对齐 |
| 7 | 当 Python `import ionex` | 同名异栈 | Rust：`ionex` crate；Python → [ionex-gim](./ionex-gim.md) |
| 8 | TECU 差 10× | 自己又乘 EXPONENT | 信任 `tec.tecu()`；对照头 `EXPONENT` |
| 9 | 期望 Height map | 未实现 | 换 2D 壳层产品；盯上游 Issues |
| 10 | 把 CKMG 当 IGS Final | 该样例是 CODE Klobuchar 风格图 | 读 COMMENT；正式对比用 CODG/IGSG |
| 11 | gzip 当明文读 | 未走 `from_gzip_file` | 后缀 `.gz` 用 gzip API（需 `flate2` feature） |
| 12 | 插值用 `get` | `get` 只索引 | 组 `MapCell` 再插；或先双线性自写 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust 服务/嵌入解析 IONEX | **ionex-rs（本页）** |
| Python 读图/教学 | [ionex-gim](./ionex-gim.md) |
| 两图差分可视化 | [diffionmap](./diffionmap.md) |
| 发表级建图 | lists 中 MosGIM 等；非本库 |

## 8. 相关

[ionex-gim](./ionex-gim.md) · [diffionmap](./diffionmap.md) · [sh-gim](./sh-gim.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · [README](./README.md)
