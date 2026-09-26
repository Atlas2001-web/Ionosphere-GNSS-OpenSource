# gnss-rtk

> crates.io **0.8.0** · tip tag **`v0.8.0`=`02dd852`** · main **`407f527`** · AGPL-3.0 · ★**79** · MSRV **1.82** · edition **2021**（tag；main 已改 **2024**）  
> 上游：<https://github.com/nav-solutions/gnss-rtk> · docs.rs：`gnss-rtk`  
> 本机：`rustc 1.98.1`（2026-09-24 07:23–07:30 EDT；**质检复跑** 2026-09-25 23:37–23:41 EDT，tag/main/★**79** 未变）· **无 [[bin]]** · feature 默认 **`[]`** / 可选 **`serde`**

一句话：`gnss-rtk` = **Rust PPP/RTK 位置（+绝对模式下钟态）解算纯库**；[rnx2cggtts](./rnx2cggtts.md) 依赖链核（其锁 **0.4.1** ≠ 本文 **0.8.0**）。**不是** GUI、**不是** RINEX/SP3 读写、**不是** 电离层 TEC 产品。

## 1. 用途与边界

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `gnss-rtk` | Rust 解算库 0.8.0 | `cargo add gnss-rtk@0.8`；无同名命令 |
| [rnx2cggtts.md](./rnx2cggtts.md) | OBS+NAV+SP3→`.ggs` CLI | 内锁 `gnss-rtk` **0.4.1** |
| [sp3.md](./sp3.md) / [rinex.md](./rinex.md) | 精密轨道 / RINEX 解析 | 只读产品；不解 PVT |
| [rinex-cli.md](./rinex-cli.md) / [cggtts.md](./cggtts.md) | QC HTML / CGGTTS 读写 | 上下游，非本求解器 |
| [rtklib.md](./rtklib.md) / [mrtklib.md](./mrtklib.md) | C/MATLAB 定位族 | 生态对照；API/许可证不同 |
| TEC/GIM 手册 | 电离层产品 | 本库不做 TEC 网格 |

| 术语 | 含义 |
| --- | --- |
| `Solver::ppp` / `Solver::rtk` | **绝对** / **差分** API（勿与 `Method::PPP` 混） |
| `Method::{SPP,CPP,PPP}` | 物理模式：单频码 / 双频码 / 码+相位 |
| `UserProfile` | Static / Pedestrian / …；错值 → `invalid user profile` |
| `PVTSolutionType::PPP` | 绝对解类型枚举名；**即使** `Method::SPP` 也可能标 PPP |
| RTK 钟态 | **不** 解接收机钟；要钟差用绝对 API |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1（≥ MSRV 1.82）

cargo new --bin gnss_rtk_smoke && cd gnss_rtk_smoke
cargo add gnss-rtk@0.8
# 可选：--features serde

# tip 对照（可选）
# git clone https://github.com/nav-solutions/gnss-rtk && cd gnss-rtk
# git checkout v0.8.0 && git log -1 --oneline   # 02dd852
# cargo test --lib spp::survey::static_spp -- --nocapture
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 想找 CLI | 纯库无 `[[bin]]` | 自写 `Solver`；或用 [rnx2cggtts](./rnx2cggtts.md) |
| `invalid navigation method` | `Method::from_str` 非法串 | 仅合法 `Method` 名 |
| `invalid user profile` | `UserProfile::from_str` 非法 | 用文档枚举名 |
| 绝对 `Method::PPP` 测例 ignored | 上游 README：**NOK** | 勿部署；用 SPP/CPP 或 RTK+PPP |
| rnx2cggtts 行为差 | 锁 **0.4.1** | 勿假定与 0.8.0 API/数值一致 |
| tip edition 2024 | main 超前 crates | 生产钉 **0.8.0**（edition 2021） |

## 3. 端到端（本机 0.8.0 / tip `02dd852` 真跑）

输入：**仓内测试夹具**（Galileo E1+E5b 伪距；与 [rnx2cggtts](./rnx2cggtts.md)/[sp3](./sp3.md) ESBC 同源参考坐标）。  
参考 ECEF（WGS84）：**(3582105.2910, 532589.7313, 5232754.8054) m**。  
历元：`2020-06-25T00:00/15/30/45:00 GPST`（**4** 历元）。  
星：Galileo **E5b**（首历元约 **8** 可见；低仰角 **E13** postfit 拒 → 有效约 **7**）。  
基准站（仅 RTK）：日志 `using remote MOJN/DNK reference`。

### 3.1 冒烟：`Method` / `UserProfile`（真实 stdout）

```rust
use gnss_rtk::prelude::*;
use std::str::FromStr;

fn main() {
    println!("Method ok: {:?}", Method::from_str("SPP").unwrap());
    println!("Method bad: {}", Method::from_str("SPPX").unwrap_err());
    println!("profile ok: {:?}", UserProfile::from_str("Static").unwrap());
    println!("profile bad: {}", UserProfile::from_str("FlyingCar").unwrap_err());
    let cfg = Config::default().with_navigation_method(Method::SPP);
    println!("cfg method={:?} max_gdop={}", cfg.method, cfg.solver.max_gdop);
}
```

本机 stdout（质检 2026-09-25 23:40 EDT：crates **0.8.0** checksum `81f2190e…`；原稿 `cfg.max_gdop` → **E0609 编不过**，已改 `cfg.solver.max_gdop`）：

```text
Method ok: SPP
Method bad: invalid navigation method
profile ok: Static
profile bad: invalid user profile
cfg method=SPP max_gdop=5
```

### 3.2 绝对 SPP（`Solver::ppp` + `Method::SPP`）

```bash
cd /path/to/gnss-rtk   # checkout v0.8.0
RUST_LOG=info cargo test --lib spp:: -- --nocapture
# → test result: ok. 4 passed; 0 failed; 0 ignored; 47 filtered out; finished in 1.33s
#   （过滤串 spp:: 同时命中 spp::{initialized,survey} + rtk_spp::{initialized,survey}；只要绝对 SPP 用 spp::survey::static_spp）
```

首历元 **2020-06-25T00:00:00 GPST**（survey；`pvt.pos_m` / `clock_offset_s`）：

| 量 | 值 |
| --- | --- |
| ECEF xyz | **(3582062.8076439444, 532619.5462266047, 5232818.854390953) m** |
| 钟差 | **481026.148 ns**（`clock_offset_s=0.000481026148…`） |
| \|Δxyz\| vs 参考 | **42.483 / 29.815 / 64.049 m** |
| GDOP / TDOP | **2.697** / **1.297** |
| `solution_type` | `PPP`（枚举名；物理仍为 SPP） |
| 墙时 / 历元 | **1.33 s**（`spp::` 四测例；质检）/ **4** 历元 |
| `initialized`（预置位）首历元 | xyz **(3582062.794571543, 532619.544602773, 5232818.840965921) m**；钟 **481026.071 ns**；残差 **42.496/29.813/64.036 m**；lat/lon/h **55.49416738722345°/8.457386821884224°/91.3272916929441 m** |

后续历元残差（survey，m）：00:15 同 00:00；00:30 **56.231/31.074/26.630**；00:45 **65.437/39.284/30.270**。

### 3.3 绝对 CPP（`Method::CPP`）

```bash
RUST_LOG=info cargo test --lib cpp::survey::static_cpp -- --nocapture
# → ok. 1 passed; finished in 1.37s
```

首历元残差：**39.142 / 30.103 / 32.390 m**（GDOP≈**2.697**）；00:30 **48.137/30.224/0.281**；00:45 **50.589/37.202/43.519 m**（质检 1.28 s）。

### 3.4 RTK-SPP（`Solver::rtk` + `Method::SPP`）

```bash
RUST_LOG=info cargo test --lib rtk_spp::survey::static_rtk_spp -- --nocapture
# → ok. 1 passed; finished in 1.34s
```

首历元残差：**24.439 / 11.346 / 96.944 m**（日志 `x=24.43858…`）；`clock_offset_s=0`（RTK **不解钟**）；基准 `MOJN/DNK`。

### 3.5 绝对 `Method::PPP`（边界）

```bash
cargo test --lib ppp::survey::static_ppp -- --nocapture
# → ignored（#[ignore]）；上游表：PPP×绝对 = NOK
# 质检：同过滤命中 rtk_ppp::survey::static_rtk_ppp ... ok（1 passed; 1 ignored; 1.27s）
```

全库：`cargo test --lib` → **49 passed; 2 ignored; 6.61 s**（v0.8.0；质检）。

**未臆造** 绝对 PPP ECEF。缺星历/缺观测 → `Err`；接 RINEX/SP3 须自实现 `OrbitSource` / `EphemerisSource` / `Candidate`——API 偏重，本文以官方测例真实数字为准。

## 4. 交叉与边界

- **链：** [rinex](./rinex.md)/[rinex-cli](./rinex-cli.md) 读观测 →（可选 [sp3](./sp3.md)）→ **本库解 PVT/钟** → [rnx2cggtts](./rnx2cggtts.md)/[cggtts](./cggtts.md) 写共视；对照 [rtklib](./rtklib.md)/[mrtklib](./mrtklib.md)。
- **库 ≠ GUI**；**≠** TEC/GIM；**≠** NTRIP 播发。
- `Solver::ppp` ≠ `Method::PPP`；RTK 要几何、绝对要钟。
- 下一优先（本车道）：**`gnss-rs`**（仍缺篇）。勿抢 GREAT_* / Gkit / gnssrefl / mpsim / MCOSB。

## 5. 复现清单

1. `rustc ≥ 1.82`；`cargo add gnss-rtk@0.8`
2. 冒烟：`Method`/`UserProfile` `from_str`（上节 stdout）
3. `git checkout v0.8.0` → `RUST_LOG=info cargo test --lib spp:: -- --nocapture` → 对齐首历元 xyz/钟/残差
4. 可选：`cpp::survey`、`rtk_spp::survey`；确认 `ppp::survey` **ignored**
5. 清临时：`rm -rf gnss_rtk_smoke`；勿留 `cargo test` 后台
