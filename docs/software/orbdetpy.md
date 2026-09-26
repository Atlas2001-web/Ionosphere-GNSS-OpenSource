# orbdetpy · UT ASTRIA 轨道确定（Python 前端 + Orekit 11 gRPC 服务）操作手册

目录：`PROJECTS.json` **`orbdetpy`**（orbit-clock，Java）· 上游 <https://github.com/ut-astria/orbdetpy> · develop **`1140678`**（2023-04-29 00:21 EDT，最后推送 2023-07-05）· master/tag **2.1.0** = `d615dd1`（2022-03-30）· **GPL-3.0** · ★129 · 本机：PyPI **`orbdetpy` 2.1.0**（wheel 41 MB，2022-03-30 上传，内置 `orbdetpy-server-2.1.0.jar` = **Orekit 11.0.2**，Build-Jdk 11）/ grpcio **1.84.0** / protobuf **7.36.2** / numpy **2.5.3** / OpenJDK **21.0.12.1** / Python **3.13.5** · 真跑 2026-09-26 02:37–02:44 EDT

> 岗位：Python 调 Java 的**小型定轨工具**：EKF / UKF / 批处理最小二乘（BLS），测量类型 Az/El、RA/Dec、距离、距离变化率、位置、PV；外带 TLE 传播、SP3/TDM/OEM 导入导出、多目标 CAR-MHF。偏空间态势感知（SSA）。冲突时：**上游源码（`orbdetpy/src/main/java/org/astria/*.java`）> 本文**。
> 姊妹篇（同一 PRN 02 算例，§3 表逐项对照）：[orekit](./orekit.md) · [tudatpy](./tudatpy.md) · [python-sgp4](./python-sgp4.md) · 精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md)。

## 1. 用途与边界

**做：** 从 Python 用 protobuf `Settings` 配力模型（球谐 EGM96、日月、球/盒翼 SRP、阻力 MSISE/指数/WAM、潮汐、机动）→ `propagate_orbits` / `determine_orbit`；`import_SP3` 一次把 SP3 全部卫星插值到任意时刻/帧；`transform_frame` 帧转换。

**不做 / 边界：**

- **停更**：2023-07 后无推送，PyPI 停在 2022 的 2.1.0；内核 Orekit **11.0.2**（现行 13.x）。但本机 Py 3.13 + protobuf 7 **能跑**（§3，没有兼容性报错）
- **无相对论力**（Settings 没有 GR 选项）；SRP 地影只用地球球体、不算月影
- **BLS 不估参数**：Cr 设 `ESTIMATE` 也只解 6 维状态，输出无残差/协方差（坑 5）；估 Cr 要用 EKF
- **TLE 只能纯 SGP4/SDP4**：给了 `prop_initial_TLE` 就走 `TLEPropagator`，力模型参数全被忽略（坑 7）
- **不是 GNSS 处理器**：无伪距/相位/钟差；GNSS 测地级 POD 另选 Ginan / GROOPS

## 2. 安装

```bash
mkdir -p /workspace/orbdetwork && cd /workspace/orbdetwork
python3 -m venv venv && . venv/bin/activate
pip install --no-cache-dir orbdetpy        # 12 s；拉 grpcio/grpcio-tools/matplotlib/numpy/protobuf/psutil/requests
python -c "import orbdetpy,sys;print(orbdetpy.__version__, sys.version.split()[0])"
# 2.1.0 3.13.5
python -c "from orbdetpy.astro_data import update_data; update_data()"   # 10 s，必做（坑 1）
```

Java 要求：`PATH` 里的 `java`（或 `$JAVA_HOME/bin/java`）；本机复用系统 OpenJDK 21（Orekit 篇同一个），jar 是 JDK 11 编译，21 上跑无报错。venv **272 MB**（`orbdetpy` 包 55 MB：jar 30 MB + 自带 orekit-data ~25 MB）。`update_data()` 从 `maia.usno.navy.mil` 拉 `finals.all`/`finals2000A.all`/`tai-utc.dat`、从 CelesTrak 拉 `SW-All.txt`，**写进 site-packages**（venv 须可写）；本机两站均可达，无需账号。

## 3. 真命令 + 实测输出

数据与 [orekit §3](./orekit.md) / [tudatpy §3](./tudatpy.md) 相同：BKG 镜像 `IGS0OPSULT_20262680000_02D_15M_ORB.SP3`（2026-09-25 00:00 GPST 起 48 h，15 min）· CelesTrak `gps-ops.tle`（2026-09-26 02:09 EDT 抓）PRN 02 = `28474`。以下误差全是**本人比对**：输出转 ITRF 与 SP3 原始 `PG02` 行逐历元求 3D 差。

### 3.1 起服务 + 时间

```python
import orbdetpy
from orbdetpy import Frame
from orbdetpy.conversion import get_J2000_epoch_offset, get_UTC_string, transform_frame
t0 = get_J2000_epoch_offset("2026-09-25T02:59:42Z")   # 03:00 GPST = 02:59:42 UTC；返回 TT 秒（J2000 起）
print(t0, get_UTC_string(t0))
```

```text
orbdetpy 2.1.0 python 3.13.5 import+server s=1.40
t0 TT-J2000 = 843577251.184 -> 2026-09-25T02:59:42.000
```

第一次 import 任一子模块就 `Popen` 一个 `java -Xmx2G -jar orbdetpy-server-2.1.0.jar <随机端口> <orekit-data>`，走 gRPC；Python 退出时 `atexit` 杀掉。服务 RSS **432 MB**（一次跑完传播 + 估计后）。

### 3.2 SP3 导入

```python
from orbdetpy.utilities import import_SP3
T = [t0 + 900.0*k for k in range(97)]
r = import_SP3("/abs/path/IGS0OPSULT_20262680000_02D_15M_ORB.SP3", Frame.GCRF, T)   # 每颗星一个 MeasurementArray
X = [list(m.true_state) for m in next(a for a in r if a.array[0].station == "G02").array]
```

```text
SP3 via import_SP3 @t0 GCRF: [14044217.1049, 7864665.7723, 21386225.0768, -2561.2806, 2769.9151, 736.5381]
import_SP3->ITRF vs raw SP3 (97 ep): max 4.90e-05 m
import_SP3 (31 sats x 97 ep) s=0.04
init dpos vs Orekit13 = 0.806 m  dvel = 0.252 mm/s
```

内部就是 Orekit 11 `SP3Parser` + `getPropagator()`（位置 Hermite 插值，速度求导）；与 Orekit 13 篇同历元初值差 0.8 m / 0.25 mm/s。

### 3.3 PRN 02 · 24 h 数值积分 vs SP3（同 Orekit 算例）

初值 = §3.2 的 GCRF 状态 @03:00 GPST；m=1100 kg、A=13 m²、Cr=1.5（猜）；EGM96 12×12、日月点质量、cannonball SRP；**必须关掉** configure() 默认的潮汐/阻力（坑 3）。

```python
from orbdetpy import configure, DragModel, EstimationType, Parameter
from orbdetpy.propagation import propagate_orbits
cfg = configure(prop_start=t0, prop_end=t0+86400.0, prop_step=900.0, prop_initial_state=X[0],
        rso_mass=1100.0, rso_area=13.0, gravity_degree=12, gravity_order=12,
        ocean_tides_degree=-1, ocean_tides_order=-1, solid_tides_sun=False, solid_tides_moon=False,
        third_body_sun=True, third_body_moon=True, drag_model=DragModel.UNDEFINED, rp_sun=True,
        rp_coeff_reflection=Parameter(value=1.5, min=1.0, max=2.5, estimation=EstimationType.UNDEFINED),
        prop_inertial_frame=Frame.GCRF, output_flags=0)
out = propagate_orbits([cfg])[0]          # out.array[i].time（TT 秒）、.true_state（GCRF 6 维）
x_itrf = transform_frame(Frame.GCRF, [m.time for m in out.array], [list(m.true_state) for m in out.array],
                         Frame.ITRF_CIO_CONV_2010_ACCURATE_EOP)   # 批量时返回 DoubleArray 列表，取 .array
```

```text
12x12+Sun/Moon+SRP(Cr1.5)              mean=   32.88 @6h=   15.32 @12h=   28.87 @24h=   57.45 m  (0.58s)
12x12+Sun/Moon (no SRP)                mean=   59.20 @6h=   18.28 @12h=   58.08 @24h=  115.61 m  (0.19s)
12x12 only                             mean= 1439.95 @6h=  495.98 @12h= 1626.79 @24h= 3202.73 m  (0.11s)
2x0 (J2) only                          mean= 1183.51 @6h=  462.85 @12h= 1270.29 @24h= 2547.01 m  (0.08s)
2x2 only                               mean= 1360.26 @6h=  489.31 @12h= 1521.23 @24h= 3048.50 m  (0.32s)
Orekit init: 12x12+Sun/Moon+SRP        mean=   42.79 @6h=   20.63 @12h=   38.31 @24h=   76.09 m  (0.47s)
Orekit init: 12x12+Sun/Moon            mean=   55.49 @6h=   14.17 @12h=   50.01 @24h=   99.76 m  (0.14s)
```

敏感性（全模型，初值同上）：容差 abs 1e-10/rel 1e-8 与 1e-14/1e-12、最大步长 60 s、重力 20×20 **全部 32.88 m**；+固体潮 32.72 m；+海潮 20×20 32.83 m。

### 3.4 定轨：SP3 位置当观测（估 Cr）

```python
from orbdetpy import Filter, MeasurementType, build_measurement
from orbdetpy.estimation import determine_orbit
meas = [build_measurement(T[k], "", X[k][:3]) for k in range(49)]          # 12 h；GCRF 位置
cfg = configure(..., prop_start=t0, prop_initial_state=X[0], output_flags=8,
        estm_DMC_corr_time=0.0, estm_DMC_sigma_pert=0.0, estm_process_noise=[1e-20]*6,
        rp_coeff_reflection=Parameter(value=1.5, min=1.0, max=2.5, estimation=EstimationType.ESTIMATE))
cfg.measurements[MeasurementType.POSITION].error[:] = [1.0, 1.0, 1.0]     # m
cfg.estm_filter = Filter.EXTENDED_KALMAN        # 或 UNSCENTED_KALMAN / BATCH_LEAST_SQUARES
cfg.estm_covariance[:] = [100.0, 100.0, 100.0, 1e-4, 1e-4, 1e-4, 0.25]   # 6 状态 + Cr 对角
fit = determine_orbit([cfg], [meas])[0]         # 出错时返回的是 traceback 字符串，不抛异常
fit[-1].estimated_state                          # EKF/UKF：[x y z vx vy vz Cr]
```

```text
EKF n_out=49 state_len=7  (3.1s)
Cr history: first 1.5000  last 1.9119
post-fit residual RMS per component = 0.060 m
in-fit 3D vs SP3(ITRF): mean=0.083 max=0.199 m
from k=48, Cr=1.9119 -> beyond fit to +24h: mean=0.423 max=0.731  @24h=0.731 m
EKF (24 h, 97 ep): Cr last 1.9227  post-fit RMS 0.090 m  in-fit mean=0.126 max=0.460 m
UKF n_out=49 state_len=7  (1.4s)
Cr history: first 1.5357  last 1.5798
post-fit residual RMS per component = 0.016 m
from k=48, Cr=1.5798 -> beyond fit to +24h: mean=10.722 max=24.418  @24h=20.150 m
BLS n_out=49 state_len=6  (3.8s)
in-fit 3D vs SP3(ITRF): mean=1.786 max=5.740 m
from k=0, Cr=1.5000 -> beyond fit to +24h: mean=15.724 max=27.560  @24h=11.713 m
BLS (Cr 手工固定 1.9119): in-fit mean=0.031 max=0.106 m | beyond fit to +24h mean=0.422 max=0.726 @24h=0.726 m
BLS (24 h, Cr 1.5 固定): in-fit mean=7.006 max=13.177 m
```

读法：EKF/UKF 的 in-fit 是**逐点滤波后**状态（贴着观测，不等于一条弧的拟合质量）；外推从最后一个滤波状态（12 h）起，只外推 12 h，**与 Orekit/tudat 的"从 t0 拟合再外推到 24 h"不同口径**。可比的是 BLS（从 t0 起一条弧）：Cr 固定 1.5 时 15.7 m，手工把 EKF 的 Cr 1.912 喂回 BLS 后 0.42 m。UKF 的 Cr 协方差给 0.01/0.25/1.0，Cr 都只挪到 1.50–1.58（1.0 与 0.25 输出逐位相同），本机未查明原因。

### 3.5 TLE / SGP4

```python
cfg = configure(prop_start=t0, prop_end=t0+86400.0, prop_step=900.0, prop_initial_TLE=[l1, l2], ...)   # 输出 GCRF
```

```text
TLE->SGP4/SDP4 (Orekit 11) vs SP3      mean=  572.01 @6h=  412.18 @12h=  663.35 @24h=  794.28 m  (0.22s) max=951.5
TLE->SGP4/SDP4 (orbdetpy/Orekit 11) vs SP3 G02, 00:00-23:45 GPST (96 ep): mean=534.4 max=829.7 m
TLE state@t0 -> 12x12+SunMoon+SRP      mean= 1136.23 @6h=  535.19 @12h= 1222.91 @24h= 2044.84 m  (0.59s)
```

00:00–23:45 窗口与 Orekit 篇同口径：534.4 vs 535.2 m（python-sgp4 篇 534 m）。03:00 起 24 h 为 572 m。把 SGP4 在 t0 的**平根数态**当密切初值喂数值积分反而更差（1136 m）。

### 3.6 三库对照（同 SP3 / 同 TLE，本人比对）

| 算例（24 h，3D vs SP3） | Orekit 13 均值 / @24h | tudatpy 1.0 | **orbdetpy 2.1.0（Orekit 11）** |
| --- | --- | --- | --- |
| 12×12 + 日月 + SRP(Cr 1.5)，各自 SP3 插值初值 | 41.4 / 75.5 m（+GR） | 14.1 / 29.2 m（+GR，11 点惯性速度） | **32.9 / 57.5 m**（无 GR） |
| 同上，统一用 Orekit 13 初值 | 41.4 / 75.5 m | 46.1 / 86.2 m | **42.8 / 76.1 m** |
| 去 SRP（统一 Orekit 初值） | 55.3 / 100.2 m | 53.0 / 91.2 m | **55.5 / 99.8 m** |
| 12×12 only（各自初值） | 1448 / 3220 m | 1403 / 3126 m | **1440 / 3203 m** |
| 12 h 拟合估 Cr | 1.879，RMS 0.443 m | 1.851 ± 0.054，RMS 0.370 m | **EKF 1.912**（滤波后 RMS 0.060 m）；BLS 不估 |
| 24 h 拟合估 Cr | 1.891 | 1.901 | **EKF 1.923** |
| TLE vs SP3（00:00 起 0–24 h） | 535 m | 17 852 m（ev2lin） | **534 m** |

读法：统一初值后与 Orekit 13 差 **≤ 1.4 m 均值**（EGM96 vs EIGEN-6S、无 GR、SRP 地影模型）；各库自己插值的初值差 0.8 m / 0.25 mm/s 就能让 24 h 均值差 ~10 m——还是在比插值，不是比力模型。

## 4. I/O

| 输入 | 格式 |
| --- | --- |
| 时间 | **TT 秒（J2000 起）** float；用 `get_J2000_epoch_offset("...Z")`（UTC 串）换 |
| 初值 | `prop_initial_state`：`prop_inertial_frame` 下 6 维 m、m/s；或 `prop_initial_TLE=[l1,l2]` |
| 观测 | `build_measurement(t, station, values)`；POSITION/PV 在惯性系，角度 rad |
| SP3 / TDM / OEM | `utilities.import_SP3`（绝对路径）；`ccsds.import_TDM` / `export_OEM` / `export_TDM` |
| 数据 | `site-packages/orbdetpy/orekit-data`：EGM96（`egm96_to96`）、DE-430、EOP、tai-utc、空间天气、FES2004 |

| 输出 | 内容 |
| --- | --- |
| `propagate_orbits` | 每个 Settings 一个 `.array`：`time`、`true_state`（GCRF 6 维）、可选模拟观测 |
| `determine_orbit` | 每观测一个：`estimated_state`（EKF/UKF 6+参数；BLS 6）、`pre_fit`/`post_fit`（`output_flags` 含 8）、协方差（下三角） |
| 出错 | gRPC `_InactiveRpcError`，`details` 里是 Java 异常；`determine_orbit` 则**返回字符串** |

## 5. 参数

| 参数 | 本文取值 | configure() 默认 / 影响 |
| --- | --- | --- |
| `rso_mass` / `rso_area` | 1100 kg / 13 m² | **5 kg / 0.1 m²**（坑 3） |
| `gravity_degree/order` | 12/12 | 20/20；`order=0` 是 2×0，不是 2×2 |
| `ocean_tides_*` / `solid_tides_*` | −1 / False | 20×20 / True；GPS 上影响 ≤ 0.2 m |
| `drag_model` | `UNDEFINED` | **MSISE2000**，Cd 与 Cr 默认都是 `ESTIMATE` |
| `rp_coeff_reflection` | 1.5，ESTIMATE 仅 EKF/UKF 生效 | 1.5，范围 [1,2]；本例 EKF 估出 1.91 已贴近上限，本文放到 2.5 |
| `estm_DMC_corr_time` / `estm_process_noise` | 0 / 6×1e-20 | 40 s DMC；关 DMC 时**必须**给 6 个过程噪声，否则返回字符串 `java.lang.IllegalArgumentException`（无消息） |
| `estm_filter` | EKF | **UKF** |
| `integ_*` | 默认（DP853，1 ms–300 s，1e-14/1e-12） | GPS 下无影响（§3.3） |

## 6. 接到哪步

SP3 / TLE（[data-access](../data-access.md#sp3--clk--bias) · [sp3](./sp3.md) · [python-sgp4](./python-sgp4.md)）→ **orbdetpy（积分 / EKF 估 Cr / SSA 测角定轨）** → GCRF/ITRF 坐标 → 高度角 / IPP（本书 TEC 流程）。只做 SP3 插值直接用 [orekit](./orekit.md) 或 [sp3](./sp3.md)。

## 7. 坑（均实测）

1. **自带 EOP 止于 2023-05（MJD 60085），过期静默**：不跑 `update_data()` 时 import_SP3→GCRF 初值与 Orekit 13 差 **~38 m**，24 h 全模型均值 **176.02 m / @24h 278.89 m**（更新后 32.88 / 57.45 m），无任何警告。
2. **`update_data()` 联网写包目录**：USNO + CelesTrak，10 s；离线/只读 site-packages 就只能手工替换 `orekit-data/Earth-Orientation-Parameters/IAU-2000/finals2000A.all`。
3. **configure() 默认是 LEO 小卫星**：不改质量面积直接跑 GPS → 均值 **75.60 m**；只改 m/A、保留潮汐+MSISE → 32.67 m（与关掉几乎一样，GPS 高度阻力≈0，但每次 1.7–2.5 s）。
4. **时间是 TT 秒**：把 GPST 串当 UTC 喂 `get_J2000_epoch_offset` → 偏 **18.000 s** = GPS 位置 **69.19 km**。
5. **BLS 不估 Cr、无残差**：`Filter.BATCH_LEAST_SQUARES` 源码只把力模型加进 builder、不选参数驱动，`estimated_state` 仅 6 维、`post_fit` 为空；Cr 固定 1.5 时 12 h 外推均值 15.7 m，手工给 1.912 则 0.42 m。
6. **UKF 估 Cr 基本不动**：初协方差 0.01 / 0.25 / 1.0 → Cr 1.503 / 1.580 / 1.580；EKF 同条件 1.912–1.913。估参数用 EKF 并核对 `estimated_state[6]` 的历史。
7. **给了 TLE 力模型就失效**：`prop_initial_TLE` 走纯 `TLEPropagator`，12×12/日月/SRP 设置被忽略（03:00 窗口 572 m）；想"TLE 起算 + 数值积分"须自己取 t0 状态，且 SGP4 平根数当密切初值更差（1136 m）。
8. **服务会成孤儿、会被复用**：Python 被 `os._exit`/kill 时 `atexit` 不执行，java 留着（本机实测残留 1 个，RSS 167 MB）；下次 import 发现命令行含同名 jar 就**直接连它**（0.17 s），哪怕数据目录不同。清理：`pgrep -af orbdetpy-server` 再按 PID `kill`（别用 `pkill -f` 匹配到自己的 shell）。
9. **`-Xmx2G` 写死**：`rpc/server.py` 硬编码，改内存只能改源码或先手工起服务（`start_server.sh`）。
10. **错误形态不统一**：`prop_step=0` → `_InactiveRpcError ... RuntimeException: Invalid propagation step size`；不给初值 → `NullPointerException: ... "this.propInitialTLE" is null`；`determine_orbit` 失败**返回 traceback 字符串**（如关 DMC 不给 `estm_process_noise` → 只有 `java.lang.IllegalArgumentException`），要 `isinstance(fit, str)` 判断。
11. **批量 `transform_frame` 返回 protobuf**：单点返回 list，传 list 返回 `DoubleArray` 列表，要 `[list(a.array) for a in ...]`。
12. **无 GR、SRP 只算地球球体地影**：与 Orekit 13（带 GR）统一初值后仍差 1.4 m 均值 / 0.6 m @24h；精密对比需知道此差。
13. **停更**：Orekit 11.0.2（2021）、grpc 依赖不锁上限；今天能装能跑，但哪天 protobuf/grpcio 大版本不兼容，只能锁旧版本或自己从 develop 构建 jar（本机未构建）。

## 8. 选型

| 需求 | 用 |
| --- | --- |
| TLE → km 级位置 / 过境 | [python-sgp4](./python-sgp4.md)（orbdetpy 结果与其一致，没必要为此起 JVM） |
| 严格 IERS 帧 + SP3 解析 + 积分 / 拟合估 Cr，持续维护 | [orekit](./orekit.md)（orbdetpy 的内核新版） |
| Python/conda 原生积分 + 变分方程 + 估参，不用 JVM | [tudatpy](./tudatpy.md) |
| 现成的 EKF/UKF 滤波定轨、测站 Az/El·RA/Dec 观测、多目标 CAR-MHF（SSA 教学/原型） | **orbdetpy（本文）**——接受停更与 Orekit 11 |
| GNSS 测地级 POD | Ginan / GROOPS（专用链） |
