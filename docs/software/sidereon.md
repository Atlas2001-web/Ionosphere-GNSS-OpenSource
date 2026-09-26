# sidereon · Rust GNSS 定位（SPP/RTK/PPP）+ RINEX/SP3/RTCM 解析库 操作手册

目录：上游 <https://github.com/neilberkman/sidereon> · crates.io **`sidereon` 2.1.1**（2026-09-22 21:48 EDT 发布；同批 `sidereon-core` 2.1.1）= tag **`v2.1.1` → `ce702db`**（GitHub release 21:44 EDT）· main **`33f2cdd`**（2026-09-25 07:25 EDT，比 v2.1.1 多 **125** 个提交，`Cargo.toml` 已是 **3.0.0**，**未发版**）· **MIT** · ★**18** · 下载 **3476** · MSRV **1.89**（`rust-version`）· 本机 **rustc 1.98.1**（2026-09-26 03:10–03:29 EDT 实测）· PROJECTS 登记名 `sidereon`

> **质检复跑通过（有小修正）**（2026-09-26 03:47–03:59 EDT）。
> - 环境：独立 target 目录，共享 `~/.cargo` 注册表；`cargo add sidereon@=2.1.1` 锁 65 个包，nalgebra 0.33.3 / rayon 1.12.0 / flate2 1.1.10 / crc32fast 1.5.2，release 冷编译 60 s。crates.io（2.1.1 发布于 2026-09-23 01:48 UTC = 09-22 21:48 EDT，下载 3476，MIT，MSRV 1.89）、tag `v2.1.1`→`ce702db`、main `33f2cdd`（领先 125 个提交，另落后 2 个；`crates/sidereon/Cargo.toml` 为 3.0.0）、★18 均核对无误。
> - 逐字复现：BKG/EUREF 同名文件，SINEX WTZR STAX/Y/Z 与 `REF` 一致；§3 三段 stdout 除耗时外逐位一致（多系统 2.195 m，仅 GPS 1.983 m，SP3 10.787 m；耗时 46.3 / 7.3 / 23.7 s）；§4.1 用 Debian rnx2rtkp 2.4.3 b34 按所述配置重跑，RTKLIB 两行（1.534/3.141、1.619/3.634）和逐历元差（中位 0.776 m、95% 3.263 m、最大 4.279 m、ΔU +0.726 m）一致；§4.2 CRX 127653 行、632 行不同复现；§5 的 `.gz`×3、CRX 直接喂、空 OBS/SP3 五类错误信息复现，NAV 共 4398 条。
> - 修正：§4.1 表中 sidereon 广播 G 的水平 0.901/2.085 是 numpy 插值分位，和 §3 程序（最近秩分位）输出的 0.902/2.084 不一致，已改为程序输出值；RTKLIB 各数两种算法相同。
> - 未复跑：§4.2 OBS/SP3/NAV 逐值比对，§4.3 诊断包装与 main 编译，§5 其余合成用例（截断、坏值、只留 3 星、DOY 250 星历），坑 5 的 `solve_spp_batch`，以及 CLI 和 RTK/PPP。

> 岗位：纯 Rust 的「读 RINEX/SP3 → 单点定位」一站式库，外加 RTK/PPP 求解器、TLE/SGP4、坐标/时间系统、NTRIP（sans-I/O）。冲突时：**上游源码 / docs.rs > 本文**。

## 1. 用途与边界

**做（本篇实测过的）：**

- `load_rinex_obs` / `load_rinex_nav` / `load_sp3` / `load_crinex`：明文 RINEX 3 OBS/NAV、SP3-c、Hatanaka CRX 解码
- `solve_spp_from_rinex_obs`：OBS 历元 → 自动选码（G/E `C1C`，C `C2I`，R `C1C`）→ Klobuchar + 对流层 → 逐历元最小二乘，10° 截止角
- `RinexSppSource::with_broadcast_context(&sp3, &nav)`：SP3 轨道/钟 + 广播电离层参数

**有 API、本篇未测：** `solve_rtk_float_with/fixed_with`、`solve_ppp_float_with/fixed_with`、`spp_inputs_from_rtcm_msm`（RTCM MSM → SPP）、ANTEX、Bias-SINEX、SBAS/SSR/HAS 改正、GNSS/INS 组合、SGP4 过境、`ntrip` 状态机。RTK/PPP 需自己组装 `rtk_filter`/`precise_positioning` 的历元结构，本篇没找到「给 RINEX 就出解」的一步入口。

**不做：** 串口/网络 I/O（NTRIP 只给协议状态机，socket 归调用方）；`.gz` 的 OBS/NAV/SP3（§5）；RINEX 2 未测。

| 易混 | 是什么 | 区别 |
| --- | --- | --- |
| **本文** `sidereon` | 薄门面，重导出 `sidereon-core` | `cargo add sidereon` 一个就够 |
| `sidereon-core` | 全部算法本体 | 默认 feature `parallel`（rayon），可选 `mmap` |
| `sidereon-cli`（仓内） | 二进制 `sidereon`：`solve`/`qc`/`metrics`/`inspect`/`tui`/`serve-mcp` | `publish = false`，**不在 crates.io**，本篇未编译（§8） |
| [gnss-rtk](./gnss-rtk.md) | nav-solutions 的 Rust PVT 求解器 | 需自己喂观测/轨道；配 [rinex](./rinex.md)/[sp3](./sp3.md) |

## 2. 安装

```bash
export CARGO_HOME=/tmp/sidereon-man/cargo-home CARGO_TARGET_DIR=/tmp/sidereon-man/target
cargo new spp_demo && cd spp_demo
cargo add sidereon@=2.1.1     # 实锁 65 个包：nalgebra =0.33.3 / rayon 1.12.0 / flate2 1.1.10 / crc32fast 1.5.2
cargo build --release         # 首次 1 min 05 s
```

- `sidereon` 自身无 feature；`nalgebra`/`simba` 是**精确版本锁**（上游把运算顺序当作「逐位一致」契约），别的 crate 若要求不同 nalgebra 版本会冲突。
- MSRV 1.89 只看了 metadata，**未用 1.89 实编**。

## 3. 最小可编译例子：WTZR 全天 SPP

数据（BKG 镜像，免账号）：`igs.bkg.bund.de/root_ftp/IGS/obs/2026/258/WTZR00DEU_R_20262580000_01D_30S_MO.crx.gz`、`…/IGS/BRDC/2026/258/BRDC00WRD_R_20262580000_01D_MN.rnx.gz`、`…/IGS/products/2436/IGS0OPSRAP_20262580000_01D_15M_ORB.SP3.gz`。参考坐标用 `…/EUREF/products/2436/ASI0EPNRAP_20262580000_01D_01D_SOL.SNX.gz` 的 WTZR `STAX/Y/Z`（**SINEX 标石坐标**；天线 ARP 在其上 0.0710 m，未扣）。RINEX 头 `APPROX POSITION XYZ` 与 SINEX 差 ENU（−0.723, −0.651, +0.056）m，本篇不用它当真值。

```bash
python -c "import hatanaka;open('WTZR258.rnx','w').write(hatanaka.decompress(open('WTZR258.crx','rb').read()).decode())"
zcat BRDC00WRD_R_20262580000_01D_MN.rnx.gz > BRDC258.rnx; zcat IGS0OPSRAP_*_ORB.SP3.gz > IGS258.sp3
```

`src/main.rs`：

```rust
use sidereon::positioning::SolvePolicy;
use sidereon::{load_rinex_nav, load_rinex_obs, load_sp3, solve_spp_from_rinex_obs,
    GnssSatelliteId, GnssSystem, RinexSppOptions, RinexSppSource};

// WTZR 参考：EPN ASI0EPNRAP 2026-258 日解 SINEX STAX/Y/Z（标石，m）
const REF: [f64; 3] = [4075580.20926969, 931854.165234869, 4801568.35391166];

fn enu(d: [f64; 3]) -> [f64; 3] {
    let lon = REF[1].atan2(REF[0]);
    let lat = REF[2].atan2(REF[0].hypot(REF[1]) * (1.0 - 6.69437999014e-3));
    let (sl, cl, sp, cp) = (lon.sin(), lon.cos(), lat.sin(), lat.cos());
    [-sl * d[0] + cl * d[1],
     -sp * cl * d[0] - sp * sl * d[1] + cp * d[2],
      cp * cl * d[0] + cp * sl * d[1] + sp * d[2]]
}
fn q(mut v: Vec<f64>, p: f64) -> f64 {
    v.sort_by(|a, b| a.total_cmp(b));
    v[((v.len() - 1) as f64 * p).round() as usize]
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let a: Vec<String> = std::env::args().collect();
    let obs = load_rinex_obs(&a[1])?;            // 明文 RINEX 3 OBS
    let nav = load_rinex_nav(&a[2])?;            // 明文 RINEX 3 NAV（也提供 Klobuchar）
    let mut opt = RinexSppOptions::default_for(&obs)?; // G/E C1C, C C2I, R C1C; 电离层+对流层
    if std::env::var("GPS_ONLY").is_ok() {
        opt = opt.with_satellites((1..=32).map(|p| GnssSatelliteId::new(GnssSystem::Gps, p).unwrap()));
    }
    let t = std::time::Instant::now();
    let sols = match a.get(3) {
        Some(p) => {
            let sp3 = load_sp3(&std::fs::read(p)?)?;
            let src = RinexSppSource::with_broadcast_context(&sp3, &nav);
            solve_spp_from_rinex_obs(&src, &obs, &opt, true, SolvePolicy::default())?
        }
        None => solve_spp_from_rinex_obs(&nav, &obs, &opt, true, SolvePolicy::default())?,
    };
    let (mut h, mut d3, mut m, mut ns) = (vec![], vec![], [0.0; 3], 0);
    for s in sols.iter().filter_map(|s| s.solution.as_ref().ok()) {
        let p = s.position.as_array();
        let e = enu([p[0] - REF[0], p[1] - REF[1], p[2] - REF[2]]);
        (0..3).for_each(|k| m[k] += e[k]);
        h.push(e[0].hypot(e[1]));
        d3.push((e[0] * e[0] + e[1] * e[1] + e[2] * e[2]).sqrt());
        ns += s.used_sats.len();
    }
    let n = h.len() as f64;
    println!("obs epochs {}  assembled {}  ok {}  ({:.1} s)", obs.epochs().len(), sols.len(), h.len(), t.elapsed().as_secs_f64());
    println!("mean sats {:.1}  mean ENU-ref E {:+.3} N {:+.3} U {:+.3} m", ns as f64 / n, m[0] / n, m[1] / n, m[2] / n);
    println!("horiz median {:.3} m  95% {:.3} m | 3D median {:.3} m  95% {:.3} m",
        q(h.clone(), 0.5), q(h, 0.95), q(d3.clone(), 0.5), q(d3, 0.95));
    Ok(())
}
```

真实 stdout（2880 历元 × 30 s，RINEX 3.04，Leica GR50）：

```text
$ spp_demo WTZR258.rnx BRDC258.rnx                     # 广播星历，多系统 G+R+E+C
obs epochs 2880  assembled 2880  ok 2880  (55.2 s)
mean sats 32.3  mean ENU-ref E -0.108 N +0.787 U +0.269 m
horiz median 1.072 m  95% 2.514 m | 3D median 2.195 m  95% 4.179 m
$ GPS_ONLY=1 spp_demo WTZR258.rnx BRDC258.rnx          # 广播星历，仅 GPS
obs epochs 2880  assembled 2880  ok 2880  (7.6 s)
mean sats 8.9  mean ENU-ref E -0.049 N +0.800 U +0.465 m
horiz median 0.902 m  95% 2.084 m | 3D median 1.983 m  95% 3.532 m
$ GPS_ONLY=1 spp_demo WTZR258.rnx BRDC258.rnx IGS258.sp3   # SP3 精密星历（IGS 快速，仅 GPS）
obs epochs 2880  assembled 2880  ok 2880  (23.9 s)
mean sats 9.0  mean ENU-ref E +1.254 N +5.115 U -4.762 m
horiz median 6.906 m  95% 16.098 m | 3D median 10.787 m  95% 23.878 m
```

**SP3 反而比广播差 5 倍** —— 不是数据问题，是 2.1.1 的模型缺项，见 §4.3 与坑 1。

## 4. 交叉检查

### 4.1 同数据 RTKLIB（Debian `rnx2rtkp` 2.4.3 b34）

配置：`posmode=single`、`frequency=l1`、`elmask=10`、`ionoopt=brdc`、`tropopt=saas`、`navsys=1`（GPS），SP3 版加 `sateph=precise` 并给 `IGS0OPSRAP…05M_CLK.CLK`。两者都是 2880/2880 历元出解。

| 解 | 平均 ENU（m） | 水平 中位/95% | 3D 中位/95% |
| --- | --- | --- | --- |
| RTKLIB 广播 G | (+0.012, +0.829, −0.260) | 0.912 / 2.120 | 1.534 / 3.141 |
| **sidereon 2.1.1 广播 G** | (−0.049, +0.800, +0.465) | 0.902 / 2.084 | 1.983 / 3.532 |
| RTKLIB SP3+CLK G | (+0.010, +0.813, −0.123) | 0.964 / 2.177 | 1.619 / 3.634 |
| **sidereon 2.1.1 SP3 G** | (+1.254, +5.115, −4.762) | 6.906 / 16.098 | 10.787 / 23.878 |

逐历元差（sidereon − RTKLIB，同为广播 G）：|Δ|₃D 中位 **0.776 m**、95% **3.263 m**、最大 4.279 m，平均 ΔU +0.726 m（加权模型不同：RTKLIB 按高度角定权）。

### 4.2 解析字段与原文逐值比对（独立 Python 列宽解析，不经 georinex）

- OBS：**1791283** 个观测值，键（历元, 卫星, 码）集合完全一致，max|Δ| = **0**（IRNSS 在库里叫 `Navic`）
- SP3：3072 条（32 星 × 96 历元），位置 max|Δ| 3.7×10⁻⁹ m（km→m 浮点），钟 max|Δ| **0**
- NAV（GPS）：原文 424 条，库 423 条；`af0`/`√A`/`e`/`TGD`/健康 max|Δ| = **0**；少的那条是 G13 22:00（健康字 63），**加载时静默丢弃不健康记录**
- CRX：`load_crinex` 与 hatanaka 2.8.1 输出同为 127653 行，632 行不同，全部是 `0.880` vs ` .880` 这类前导零写法，数值无差

### 4.3 SP3 误差来源定位（诊断包装，非上游代码）

在 `EphemerisSource` 外包一层补项后重跑（GPS，同上）：

| 在 SP3 钟上补 | 3D 中位/95%（m） | 与 RTKLIB SP3 的 |Δ| 中位 |
| --- | --- | --- |
| 不补（2.1.1 原样） | 10.787 / 23.878 | 10.614 |
| 相对论周期项 −2 r·v/c² | 4.381 / 10.516 | 4.479 |
| 再换 5 min CLK 钟 | 4.387 / 10.271 | 4.383 |
| 相对论项 + 广播 TGD | **2.184 / 4.309** | **0.779** |

结论：2.1.1 源码注释写「SP3 precise clocks include it」，但 IGS SP3/CLK 约定**不含**相对论周期项，也不含 L1 C/A 的 TGD；两项补上后与 RTKLIB 对齐。上游 main `33f2cdd` 已改成由 SP3 源返回 `peph2pos` 相对论项：同一例子编 main 得 3D 中位 **3.686** m / 95% 10.340 m（与只补相对论项的 4.4 m 同量级，TGD 仍缺），广播 G 与 RTKLIB |Δ| 中位降到 **0.051** m，SP3 解算耗时 23.9 s → 3.9 s。

## 5. 错误用例（除「错一天星历」外均为合成输入）

| 输入 | 结果 |
| --- | --- |
| 合成：空文件 → OBS/NAV/SP3 | `Err`：`no END OF HEADER` / `SP3 missing header line 1` |
| 合成：OBS 截断一半 / 只有头 | `Err`：`epoch truncated: missing satellite line`（只有头也报这个） |
| 合成：C1C 写成 `abc.defghijk` | `Err`：`observation.value is not a valid float`，带原行 |
| 合成：历元日期 2026-13-45 | `Err`：`not a valid civil date` |
| 合成：删 `APPROX POSITION XYZ` | 加载 Ok；SPP `Err`：`needs APPROX POSITION XYZ or an initial guess`（用 `with_initial_guess` 解决） |
| CRX 直接喂 `load_rinex_obs` | `Err`：`rcv_clock_offset_s is not a valid float`（没有「这是 CRINEX」的提示） |
| `.gz` 喂 OBS/NAV/SP3 | `Err`：`stream did not contain valid UTF-8` / `SP3 is not valid UTF-8`，不自动解压 |
| 合成：NAV 截断一半 | **加载 Ok（4082 条），静默**；SPP 只 843/2880 历元出解，其余 `only 0 usable satellites` |
| 合成：NAV 只留 G10/G12/G14 | 加载 Ok 40 条；SPP 0/2880，`only 1 usable satellites; need at least 4` |
| 观测只放行 3 / 4 颗 GPS | 0/2071、129/2071 出解；其余同上 `Err`（首个失败历元只有 1 颗可见） |
| 真实：用 DOY 250 的 BRDC 解 DOY 258 | 0/2880，`only 0 usable satellites`，不外推、不给假解 |
| 合成：SP3 截断 / 坐标 `72x6.598455` | `Err`：`position record truncated` / `coordinate is not a valid float` |

全部用 `catch_unwind` 包着跑：**0 次 panic**；失败逐历元留在 `RinexSppEpochSolution::solution` 里，外层 `Result` 只管装配。

## 6. I/O 速查

| 入 | 函数 | 备注 |
| --- | --- | --- |
| RINEX 3 OBS（明文） | `load_rinex_obs(path)` / `parse_rinex_obs(&str)` | 30 MB 日文件，OBS+NAV 共 0.45 s |
| RINEX 3 NAV（明文，混合） | `load_rinex_nav` | 只留健康记录；Klobuchar/NeQuick/BDS 参数、GLONASS 频道号进 SPP |
| SP3 | `load_sp3(&[u8])` | 注意是**字节**不是路径 |
| CRINEX | `load_crinex(path)` → `String` → `parse_rinex_obs` | 也有 `encode_crinex` |
| RINEX CLK | `load_rinex_clock` | 可取钟，但 SPP 不会自动与 SP3 合用 |

出：`ReceiverSolution{position(ITRF ECEF m), geodetic(弧度+椭球高), rx_clock_s, system_clocks_s, dop, position_covariance(ecef/enu m²), residuals_m, used_sats, rejected_sats(NoEphemeris/LowElevation…)}`；`epoch` 是文件里的民用时间原样。

## 7. 坑

1. **2.1.1 的 SP3 SPP 差 10 m 级**：不加相对论周期项、不加 TGD（§4.3）。要精密轨道单点先用 main（未发版）或自己包 `EphemerisSource`；广播星历路径正常。
2. 不认 `.gz`、不自动认 CRX：自己 `flate2`/`hatanaka` 解压，CRX 走 `load_crinex`。
3. NAV 截断时**静默**加载前半，只在 SPP 里表现为大量 `only 0 usable satellites`，要自查 `records().len()`。
4. 不健康星历（健康字 ≠ 0）加载就被丢，`records()` 看不到；G05/G31 在 00:00 报 `NoEphemeris` 是 BRDC 本身缺 2 h 内记录。
5. 多系统比仅 GPS 慢 7 倍（55 s vs 7.6 s / 2880 历元，单线程 serial 求解）；批量用 `solve_spp_batch`（rayon）。
6. 默认单频、10° 截止角、`SolvePolicy::default()`；参考点问题：解的是天线相位中心附近，SINEX 是标石，差 ARP 高 0.071 m + PCO。
7. IRNSS 的系统名是 `Navic`；BeiDou 默认码随 RINEX 小版本切换 `C1I`/`C2I`。
8. main 已 3.0.0（大版本），2.1.1 → main 的 API 未逐项核对；同 API 的例子（load_* + `solve_spp_from_rinex_obs` + `RinexSppSource`）在 main 上原样编过。

## 8. 未测

- RTK / PPP（float/fixed）、DGNSS、RTCM MSM → SPP、SSR/HAS/SBAS 改正：**未测**
- `sidereon-cli`（`solve`/`qc`/`tui`/`serve-mcp`）：仓内有源码，本机编译时磁盘满失败，**未测**
- NTRIP、`tui` 实时流：**未在真接收机测试**
- RINEX 2、RINEX 4 NAV、MSRV 1.89、Python/C/Elixir/WASM 绑定：未测

## 9. 选型

| 需求 | 选 |
| --- | --- |
| Rust 里「RINEX + 星历 → 单点坐标」一步到位 | **本库**（广播星历路径；SP3 等发版） |
| Rust 可控的 PVT/RTK 求解器，配 nav-solutions 生态 | [gnss-rtk](./gnss-rtk.md) + [rinex](./rinex.md)/[sp3](./sp3.md)，CLI 用 [rinex-cli](./rinex-cli.md) |
| 成熟的 SPP/RTK/PPP 基准 | [rtklib](./rtklib.md)（本篇的对照）/[rtklib-explorer](./rtklib-explorer.md) |
| 只解析、Python 生态 | [georinex](./georinex.md)；CRX 用 [hatanaka](./hatanaka.md)/[crx2rnx](./crx2rnx.md) |
| RTCM 解码 | [rtcm-rs](./rtcm-rs.md)/[pyrtcm](./pyrtcm.md)（本库只把 MSM 转 SPP 输入） |
