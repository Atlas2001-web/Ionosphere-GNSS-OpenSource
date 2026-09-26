# nyx · nyx-space Rust 航天动力学库（PyPI `nyx_space` / crate `nyx-space`）操作手册

目录：`PROJECTS.json` **`nyx`**（orbit-clock / 轨道动力学，Rust）· 上游 <https://github.com/nyx-space/nyx> · master = tag **2.6.0** = `7452963`（2026-09-12 01:05 EDT）· **AGPL-3.0** · ★490 · 本机：PyPI **`nyx_space` 2.6.0**（cp313 manylinux wheel，2026-09-12 上传；内含 ANISE 帧/星历模块）/ Python **3.13.5**；Rust 路线 crate **`nyx-space` 2.6.0** + `anise` **0.10.6** + `hifitime` **4.3.1** / rustc **1.98.1** · 真跑 2026-09-26 02:46–02:53 EDT

> 岗位：**高保真轨道积分 + 卡尔曼滤波定轨**（EKF，可估 Cr），帧/星历/EOP 全走 ANISE（SPICE 内核：DE440s、PCK、`earth_latest_high_prec.bpc`）。冲突时：**上游 `nyx-py/nyx_space/*.pyi` 与 `nyx-core/src` > 本文**。
> 姊妹篇（同一 PRN 02 算例，§3.5 表逐项对照）：[orekit](./orekit.md) · [tudatpy](./tudatpy.md) · [orbdetpy](./orbdetpy.md) · 精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md)。

## 1. 用途与边界

**做：** 航天器数值积分（球谐重力 COF/SHADR、点质量三体、cannonball SRP（地影/月影）、NRLMSISE-00 阻力、固体潮）；RK89/DP78 等自适应积分器；事件求根（近地点、食）；**位置观测 EKF 定轨**（`SpacecraftPositionODProcess`，状态 9 维 = 6 + Cr + Cd + 质量）与测站距离/多普勒定轨；Monte Carlo；导出 Parquet / CCSDS OEM / SPICE BSP。

**不做 / 边界：**

- **没有广义相对论加速度**（2.6.0 的 `AccelModels` 只有 `point_masses` / `gravity_field` / `solid_tides`；源码 `src/dynamics/` 无 relativity）
- **不读 SP3**：要自己解析（本文 1 行 Python，§3.4），SP3 只当"位置观测"或真值
- **Python 没有批处理最小二乘**（只绑了 EKF + RTS 平滑）；Rust 有 `od::blse::BatchLeastSquares`（观测维度 U1，即标量距离/多普勒类；本文未测）。"从 t0 一条弧拟合"要自己回推（§3.4）
- **不读 TLE、没有 SGP4**：TLE 走 [python-sgp4](./python-sgp4.md)
- **不是 GNSS 处理器**：无伪距/相位/钟差；测地级 POD 选 Ginan / GROOPS
- **AGPL-3.0**：闭源服务端集成要注意传染

## 2. 安装

两条路线都实测通过；**Python wheel 是现实路线**（12 s 装完，不用 Rust 工具链）。

```bash
python3 -m venv venv && ./venv/bin/pip install -q nyx_space==2.6.0 numpy
./venv/bin/pip list | grep -i -E "nyx|numpy"
# numpy             2.5.3
# nyx_space         2.6.0
du -sh venv            # 529M（顺带装 polars 1.44.2 172 MB、scipy、plotly、ruff）
```

数据（不走 `MetaAlmanac.latest()`，手工下载到自己的目录，共 ~39 MB）：

```bash
mkdir -p data && cd data
curl -sSLO http://public-data.nyxspace.com/anise/de440s.bsp            # 32726016 B
curl -sSLO http://public-data.nyxspace.com/anise/v0.5/pck11.pca        # 38067 B
curl -sSLO https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc   # 5137408 B
curl -sSLO https://media.githubusercontent.com/media/nyx-space/nyx/master/data/01_planetary/EGM96.cof.gz  # 1261082 B（仓内是 LFS 指针，要走 media 域）
```

Rust 路线（released crate + 最小例，不编整个 workspace）：

```bash
export CARGO_HOME=$PWD/cargo CARGO_TARGET_DIR=$PWD/target CARGO_PROFILE_RELEASE_DEBUG=0
cargo new nyxmin && cd nyxmin && cargo add nyx-space@2.6.0 anise@0.10.6 hifitime
cargo build --release -j4
# 本机：241 个 Compiling 行，退出码 0，163 s；target 843 MB + CARGO_HOME 257 MB，二进制 3.3 MB
```

纯 ANISE（PyPI `anise` 0.10.6）只管帧/星历/EOP，不能积分定轨；`nyx_space.anise` 已内含同一套 API，不用另装。

## 3. 真命令 + 实测输出

算例：IGS ULT `IGS0OPSULT_20262680000_02D_15M_ORB.SP3` 的 **PRN 02**，初值 = **Orekit 篇的 GCRF 状态** @ 2026-09-25 03:00 GPST（`orekitwork/okpv.py`：`14044216.5494 7864665.4457 21386225.5616 m`，`-2561.2806770 2769.9149102 736.5382281 m/s`），当作 nyx 的 `EME2000` 输入；m=1100 kg、A=13 m²、Cr=1.5（猜）；EGM96 12×12（ITRF93 帧）+ 日月点质量 + SRP（遮挡体 Earth+Moon）；RK89 默认选项；输出 97 个 15 min 历元，ANISE 转 ITRF93 与 SP3 原始位置求 3D 差。

### 3.1 最小骨架（Python）

```python
import numpy as np
from nyx_space import Spacecraft, Mass, SRPData
from nyx_space.anise import Almanac
from nyx_space.anise.astro import Orbit
from nyx_space.anise.constants import Frames, CelestialObjects as CO
from nyx_space.mission_design import (AccelModels, Dynamics, ForceModels, GravityFieldConfig,
    IntegratorMethod, IntegratorOptions, PointMasses, Propagator, SolarPressure)
from nyx_space.time import Epoch, Unit
alm = Almanac("data/de440s.bsp").load("data/pck11.pca").load("data/earth_latest_high_prec.bpc")
eme, itrf = alm.frame_info(Frames.EME2000), alm.frame_info(Frames.EARTH_ITRF93)
T0 = Epoch("2026-09-25 03:00:00 GPST")
orb = Orbit(14044.2165494, 7864.6654457, 21386.2255616, -2.5612806770, 2.7699149102, 0.7365382281, T0, eme)  # km, km/s
acc = AccelModels(point_masses=PointMasses(celestial_objects=[CO.SUN, CO.MOON]),
                  gravity_field=GravityFieldConfig(degree=12, order=12, filepath="data/EGM96.cof.gz",
                                                   frame=Frames.EARTH_ITRF93.to_frameuid()))
srp = SolarPressure([Frames.EARTH_J2000, Frames.MOON_J2000], alm)          # phi 默认 1367.0 W/m²
prop = Propagator(Dynamics(acc, force_models=ForceModels(solar_pressure=srp)), alm,
                  IntegratorMethod.RungeKutta89, IntegratorOptions())
sc = Spacecraft(orb, Mass(dry_mass_kg=1100.0), SRPData(area_m2=13.0, coeff_reflectivity=1.5))
traj = prop.for_duration(sc, Unit.Day * 1, trajectory=True).trajectory
q = alm.transform_to(traj.at(T0 + Unit.Hour * 24).orbit, itrf)            # q.x_km ... 与 SP3 比
```

`IntegratorOptions()` 实际值：`min_step: 1 ms, max_step: 45 min, tol: 1e-12, attempts: 50`。

### 3.2 帧核对（本人比对）

SP3 ITRF 位置 + Orekit ITRF 速度，用 ANISE 转回惯性系，与 Orekit GCRF 初值比：

```text
SP3 ITRF93 -> EME2000     minus Orekit GCRF: dpos=1.747 m dvel=0.00032 m/s
SP3 ITRF93 -> GCRF        minus Orekit GCRF: dpos=4.016 m dvel=0.00015 m/s
SP3 ITRF93 -> EARTH_J2000 minus Orekit GCRF: dpos=1.747 m dvel=0.00032 m/s
Earth ICRS Earth J2000
```

NAIF 的 ITRF93 BPC 以 "J2000" 为父帧（DE 星历实际按 ICRF 对齐），所以 Orekit GCRF 状态要当 **`EME2000`** 喂；选 ANISE 的 `GCRF` 反而多偏 2.3 m（坑 3）。

### 3.3 24 h 积分 vs SP3（`prop.py`，本人比对）

```text
init 2026-09-25T03:00:00 GPST a=26559.059 km e=0.01710 i=54.974 deg
12x12+Sun/Moon+SRP(Cr1.5)          mean=  37.98 @6h=  17.65 @12h=  33.05 @24h=  67.03 m (0.11s)
12x12+Sun/Moon+SRP, +EARTH in PM   mean=  37.98 @6h=  17.65 @12h=  33.05 @24h=  67.03 m (0.06s)
12x12+Sun/Moon (no SRP)            mean=  57.45 @6h=  15.90 @12h=  54.42 @24h= 107.35 m (0.05s)
12x12 only                         mean=1444.61 @6h= 497.25 @12h=1630.91 @24h=3212.45 m (0.06s)
J2..12 off (point mass+Sun/Moon)   mean=15653.82 @6h=8394.69 @12h=13744.11 @24h=27512.78 m (0.01s)
12x12+Sun/Moon+SRP DP78            mean=  37.98 @6h=  17.65 @12h=  33.05 @24h=  67.03 m (0.04s)
same, ANISE-rotated SP3 start      mean=  25.63 @6h=  10.73 @12h=  21.28 @24h=  44.31 m (0.11s)
```

另测：JGM3 代替 EGM96 → 38.00 / 67.07 m；20×20 与 12×12 到 0.01 m 相同，8×8 为 38.00 / 67.03 m；RK89 容差 1e-14、最大步 60 s → 37.98 / 67.03 m（0.35 s）；重力场放 `IAU_EARTH_FRAME`（上游示例写法）→ **40.51 / 71.95 m**。本日 PRN 02 无食（97 个历元 `solar_eclipsing` 全为 "no eclipse"），去掉月影结果不变。

Rust 最小例（同力模型同初值，`nyxmin/src/main.rs`，参数是 SP3 在 +24 h 的 ITRF km）：

```text
$ ./target/release/nyxmin 15158.857114 -4627.922556 21587.079092
end 2026-09-26T03:00:00 GPST ITRF93 [15158.854806 -4627.855581 21587.080531] km  |err vs SP3| = 67.03 m  (35.36ms)
```

与 Python wheel 的 @24h 67.03 m 一致（同一 Rust 内核）。

### 3.4 定轨：SP3 位置当观测，EKF 估 Cr（`nyx_od.py`，本人比对）

```python
from nyx_space.orbit_determination import (PositionDevice, StochasticNoise, WhiteNoise, MeasurementType as MT,
    Measurement, TrackingDataArc, SpacecraftEstimate, SpacecraftPositionODProcess, KalmanVariant)
srp = SolarPressure([Frames.EARTH_J2000, Frames.MOON_J2000], alm, estimate=True)   # Cr 进状态
noise = StochasticNoise(white_noise=WhiteNoise(mean=0.0, sigma=1e-3))              # km → 1 m
dev = PositionDevice("SP3", itrf).with_noise(MT.X, noise).with_noise(MT.Y, noise).with_noise(MT.Z, noise)
raw = np.array([[float(v) for v in l[4:46].split()] for l in open(SP3F) if l.startswith("PG02")])[12:]  # km，[12] = 03:00 GPST
ms = []
for k in range(49):                                       # 12 h；SP3 ITRF 位置（km）
    m = Measurement("SP3", T0 + Unit.Minute * (15 * k))
    m.push(MT.X, raw[k, 0]); m.push(MT.Y, raw[k, 1]); m.push(MT.Z, raw[k, 2]); ms.append(m)
est = SpacecraftEstimate.from_diag(sc, np.array([1e-2]*3 + [1e-5]*3 + [0.5, 0.0, 0.0])**2)  # 方差，不是 sigma
sol = SpacecraftPositionODProcess(prop, KalmanVariant.ReferenceUpdate, {"SP3": dev}).process_arc(est, TrackingDataArc(ms))
last = sol.to_traj().at(T0 + Unit.Hour * 12); print(last.srp.coeff_reflectivity)
b = prop.for_duration(last, Unit.Hour * -12, trajectory=False).state        # 回推到 t0，再飞 24 h
```

```text
EKF 12h (49 ep): accepted=49 rejected=0 prefit RMS=0.138 postfit RMS=0.101 m  Cr=1.9109  (0.50s)
   back-prop to 2026-09-25T03:00:00 GPST, re-fly 24h: in-fit mean=0.367 max=0.843 | beyond fit mean=1.731 max=2.404 | @24h=1.371 m
   smoother: postfit RMS=46195.7 m, Cr @t0/@6h/@12h = 1.500 / 1.940 / 1.911
EKF 24h (97 ep): accepted=97 rejected=0 prefit RMS=0.184 postfit RMS=0.164 m  Cr=1.9180  (0.72s)
   back-prop to 2026-09-25T03:00:00 GPST, re-fly 24h: in-fit mean=0.622 max=1.034 | beyond fit mean=0.000 max=0.000 | @24h=0.995 m
```

另测：直接"12 h 最后滤波状态外推到 24 h"= mean 1.714 / max 2.403 / @24h 1.371 m；`DeviationTracking` 变体 12 h 接收 15 / 拒 34、Cr 1.939，24 h 接收 16 / 拒 81、Cr 1.996，postfit RMS 为 `nan`；观测 sigma 0.1 m → 12 h 拒 10/49、24 h 拒 52/97（默认 3σ 拒），sigma 10 m → 12 h Cr 1.807、24 h 1.910。RTS 平滑器结果不可用（坑 7）。

### 3.5 四库对照（同 SP3、统一 Orekit 初值，本人比对）

| 算例（24 h，3D vs SP3，均值 / @24h） | Orekit 13 | tudatpy 1.0 | orbdetpy 2.1.0 | **nyx 2.6.0** |
| --- | --- | --- | --- | --- |
| 12×12 + 日月 + SRP(Cr 1.5) | 41.4 / 75.5 m（+GR） | 46.1 / 86.2 m（+GR） | 42.8 / 76.1 m | **38.0 / 67.0 m**（无 GR） |
| 去 SRP | 55.3 / 100.2 m | 53.0 / 91.2 m | 55.5 / 99.8 m | **57.5 / 107.4 m** |
| 12×12 only | 1448 / 3220 m | 1403 / 3126 m（自身初值） | 1440 / 3203 m（自身初值） | **1445 / 3212 m** |
| 12 h 估 Cr | 1.879（LS，RMS 0.443 m） | 1.851 ± 0.054 | EKF 1.912 | **EKF 1.911**（postfit RMS 0.101 m） |
| 24 h 估 Cr | 1.891 | 1.901 | EKF 1.923 | **EKF 1.918** |
| 12 h 拟合 → 外推到 24 h | t0 LS：外推段 mean 1.77 / @24h 2.81 m | 2.80 / 3.77 m | 12 h 滤波态外推 0.42 / 0.73 m | 回推 t0 再飞：外推段 **1.73 / 1.37 m** |

读法：统一初值后 nyx 与 Orekit 差 3.4 m 均值 / 8.5 m @24h，与 tudat/orbdetpy 的离散同量级（GR 有无、EGM96 vs EIGEN、ITRF93 BPC vs IERS 2010 EOP 都在里面，本文未逐项拆）；EKF 估的 Cr 与 orbdetpy EKF 差 0.001–0.005。nyx 自己用 ANISE 旋转 SP3 起算是 25.6 / 44.3 m——**初值帧口径**的影响比力模型差异大。

## 4. I/O

| 输入 | 格式 |
| --- | --- |
| 时间 | `Epoch("2026-09-25 03:00:00 GPST")`，字符串带时间尺度（GPST/UTC/TAI/TDB…）；`+ Unit.Minute*15` |
| 状态 | `Orbit(x,y,z,vx,vy,vz, epoch, frame)`，**km、km/s**；frame 要 `alm.frame_info(...)` 取带 μ 的版本 |
| 航天器 | `Spacecraft(orbit, Mass(dry_mass_kg=…), SRPData(area_m2, coeff_reflectivity), DragData(...))` |
| 星历/帧/EOP | ANISE：`.bsp`（DE440s）、`.pca`（PCK11）、`.bpc`（ITRF93 地球定向）；或 `MetaAlmanac.latest()` 自动下载 |
| 重力场 | `GravityFieldConfig(degree, order, filepath, frame)`；先按 SHADR 读，失败再按 COF 读，`.gz` 直接读 |
| 观测 | `Measurement(tracker, epoch).push(MeasurementType.X, km)` → `TrackingDataArc([...])`；或 CCSDS TDM / Parquet |

| 输出 | 内容 |
| --- | --- |
| `for_duration(...)` | `PropagationResult`：`.state`（终态 Spacecraft）、`.trajectory`（`.at(epoch)` 插值） |
| 轨迹导出 | `traj.to_parquet(path)`、`traj.to_ephemeris(name, ExportCfg())` → `write_ccsds_oem` / `write_spice_bsp` |
| OD 解 | `SpacecraftPositionODSolution`：残差（`accepted_residuals()` 每个有 `prefit`/`postfit`/`ratio`，单位 km）、`rms_*`、`nis_consistency()`、`to_traj()`、`to_parquet()`（150 列：状态、`cr`、协方差、增益、残差） |
| 出错 | 统一 Python `Exception`，消息是 Rust 错误串（坑 5、6） |

## 5. 参数

| 参数 | 本文取值 | 默认 / 影响 |
| --- | --- | --- |
| `GravityFieldConfig.frame` | `EARTH_ITRF93` | 上游示例用 `IAU_EARTH_FRAME`，本例差 2.5 / 4.9 m（均值 / @24h） |
| `degree/order` | 12/12 | GPS 高度 12 阶以上无变化（20×20 到 0.01 m 相同） |
| `PointMasses` | `[SUN, MOON]` | 中心体不用列（列上 EARTH 结果到 0.01 m 相同） |
| `SolarPressure(shadow_bodies, alm, flux_w_m2, estimate)` | Earth+Moon，1367 W/m²，OD 时 `estimate=True` | `estimate` 默认 **True** |
| `SRPData(area_m2, coeff_reflectivity)` | 13, 1.5 | `Spacecraft(orbit)` 默认 **A=0、Cr=1.8、质量 0**（坑 4） |
| `IntegratorMethod` / `IntegratorOptions` | RK89 默认 | 1 ms–45 min、tol 1e-12；GPS 下 DP78 与 1e-14 结果相同 |
| `KalmanVariant` | `ReferenceUpdate` | `DeviationTracking` 本例 postfit RMS `nan`（坑 8） |
| `SpacecraftEstimate.from_diag` | 方差 [1e-4 km²×3, 1e-10×3, 0.25, 0, 0] | 9 维：6 + Cr + Cd + 质量；**填的是方差** |
| `SigmaRejection` | 默认 3σ | 观测 sigma 定太小会大量拒收（坑 9） |

## 6. 接到哪步

SP3（[data-access](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md)）→ **nyx：积分 / EKF 估 Cr / 外推**（SP3 过期或缺历元时补轨道）→ ITRF93 坐标 → 高度角 / IPP / 掩星几何（本书 TEC 流程）。只需插值 SP3 用 [orekit](./orekit.md) 或 [sp3](./sp3.md)；TLE 起算用 [python-sgp4](./python-sgp4.md)。

## 7. 坑（均实测）

1. **仓内数据是 Git LFS 指针**：`gh api .../data/01_planetary/JGM3.cof.gz` 拿到的是 130 B 的 `version https://git-lfs.github.com/spec/v1` 文本；要从 `media.githubusercontent.com/media/nyx-space/nyx/master/...` 下载（或用 `MetaFile` 从 `public-data.nyxspace.com`）。
2. **不加载 BPC 就没有 ITRF93**：只 load DE440s+PCK11 时 `transform_to(..., EARTH_ITRF93)` 报 `ID 3000 not in look up table`；`earth_latest_high_prec.bpc` 每天更新，结果会随下载日期漂移（本文文件覆盖到 2026-12-22）。
3. **GCRF ≠ 你以为的 GCRF**：Orekit GCRF 状态当 ANISE `GCRF` 用，与 SP3 反算差 4.016 m；当 `EME2000` 用差 1.747 m。与 Orekit/SPICE 对接一律用 `EME2000`/`EARTH_J2000`。
4. **`Spacecraft(orbit)` 默认质量 0**：开着 SRP 直接跑 → `Exception: encountered a dynamics error spacecraft total mass is zero, cannot compute any force model`；默认 `SRPData { area_m2: 0.0, coeff_reflectivity: 1.8 }`，必须显式给 `Mass` 和 `SRPData`。
5. **重力文件路径是惰性检查**：构造 `GravityFieldConfig("nope.cof.gz")` 不报错，到 `for_duration` 才 `propagation encountered an error: Could not read file: File not found: "nope.cof.gz"`；相对路径相对于**当前工作目录**。
6. **单位是 km、km/s**：`Orbit`、观测值、噪声 sigma（`1e-3` = 1 m）、残差（`prefit` 返回 km）全是 km；把 m 喂进去不会报错，只会结果离谱。
7. **RTS 平滑器输出不可信**：`sol.smooth(alm)` 后 postfit RMS **46195.7 m**，t0 的 Cr 仍是先验 1.500、6 h 处 1.940、12 h 1.911（常参数平滑后本应处处相同）；Parquet 里平滑结果首行就是先验状态。估 Cr 用滤波末态，t0 状态自己回推（§3.4）。
8. **`DeviationTracking` 在本例大量拒收**：12 h 拒 34/49、24 h 拒 81/97，postfit RMS `nan`，Cr 1.939 / 1.996（ReferenceUpdate 0 拒、1.911 / 1.918）；拒收时 stderr 打进度 ` 90% done - 2026-09-26T01:00:00 GPST - 16 measurements accepted, 73 rejected`，先看这行再信结果。
9. **观测 sigma 决定 Cr**：sigma 0.1 m → 默认 3σ 拒掉 10/49（24 h 拒 52/97），postfit `nan`；sigma 10 m → 12 h Cr 1.807。SP3 位置本身 cm 级，但 12×12 力模型误差是 dm 级，sigma 取 ~1 m 才稳定。
10. **`from_diag` 实际填方差**：上游 Python 测试注释写 "always defined in 1-sigma!"，但 `py_od.rs` 把数组原样交给 `KfEstimate::from_diag`（协方差对角）；本文传 Cr 项 0.25，Parquet 首行 `Sigma Cr` = 0.5，证明是方差（滤波末 `Sigma Cr` = 0.0292）。
11. **没有 GR**：与带 GR 的 Orekit 13 统一初值后仍差 3.4 m 均值；GNSS 精密比对要知道此差。
12. **wheel 顺带装一堆**：`nyx_space` 依赖 polars、scipy、plotly、**ruff**，venv 529 MB；只要帧转换装 `anise` 即可。
13. **Rust 路线吃盘**：最小例编译 241 个 crate、163 s、`target/` 843 MB + `CARGO_HOME` 257 MB（`CARGO_PROFILE_RELEASE_DEBUG=0` 下）；盘紧就走 Python wheel，@24h 同为 67.03 m。
14. **GPST 字符串要写尺度**：`Epoch("... GPST")` 与 `"... UTC"` 差 18 s（GPS 位置差约 70 km，orbdetpy 篇实测 69.19 km）；SP3 历元是 GPST。

## 8. 选型

| 需求 | 用 |
| --- | --- |
| TLE → km 级位置 / 过境 | [python-sgp4](./python-sgp4.md)（nyx 无 SGP4） |
| Rust 里做 TLE/OMM → TEME | [sgp4-rs](./sgp4-rs.md) |
| 严格 IERS 2010 帧 + SP3 解析插值 + 积分 / 最小二乘拟合，含 GR | [orekit](./orekit.md) |
| Python/conda 原生积分 + 变分方程 + 最小二乘估参 | [tudatpy](./tudatpy.md) |
| 现成 EKF/UKF + 测站测角、SSA 原型（停更，Orekit 11） | [orbdetpy](./orbdetpy.md) |
| **pip 一条装好、不起 JVM、积分 0.1 s 级、EKF 估 Cr、导出 OEM/BSP/Parquet，或要在 Rust 里嵌动力学** | **nyx（本文）**——接受无 GR、Python 无 BLS、平滑器待核、AGPL |
| 只要帧/星历/EOP（SPICE 替代） | ANISE（PyPI `anise` / crate `anise`） |
| GNSS 测地级 POD | Ginan / GROOPS（专用链） |
