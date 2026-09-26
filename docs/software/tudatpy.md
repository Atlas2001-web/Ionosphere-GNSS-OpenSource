# tudatpy · TU Delft 天体动力学 Python 工具箱 操作手册

目录：`PROJECTS.json` **`tudatpy`** · 上游 <https://github.com/tudat-team/tudatpy> · develop **`5c61b03`**（2026-09-24 06:03 EDT）· tag **v1.0.0** · **BSD-3-Clause** · ★91 · 文档 <https://docs.tudat.space> · 本机：conda 频道 **`tudat-team`** 包 `tudatpy 1.0.0`（`py312h3558349_3`）+ `tudat-resources 2.4` / Python **3.12.14** / numpy **1.26.4** / scipy **1.17.1** / micromamba **2.9.0** · 真跑 2026-09-26 02:23–02:35 EDT

> 岗位：Python 前端 + C++ 内核的**数值轨道积分 + 估计**（力模型、变分方程、最小二乘定轨/参数估计）。与 [orekit](./orekit.md) 同层，不用 JVM。只管轨道，不管观测值/TEC。冲突时：**docs.tudat.space / 上游 API 文档 > 本文**。
> 姊妹篇：[orekit](./orekit.md)（同一 PRN 02 算例，下表逐项对照）· [python-sgp4](./python-sgp4.md) · 精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md) / [gnssanalysis](./gnssanalysis.md)。

## 1. 用途与边界

**做：** 力模型积分（球谐重力 / 三体 / SRP / 相对论 / 阻力…）、IERS 2010 高精度 GCRS↔ITRS（`gcrs_to_itrs`）、SPICE 星历、`create_best_fit_to_ephemeris` 拟合星历并估参数（初态 + Cr 等）。

**不做：**

- **不读 SP3**：没有 SP3 解析器，自己解析 → 表格星历（§3.5）
- **不能 pip**：PyPI `tudatpy` **404**；conda-forge 也 **404**；只在 `tudat-team` 频道（§2）
- **不是 GNSS 处理器**：无伪距/相位/钟差
- **TLE 不是 SDP4**：`ephemeris.sgp4` 实为 SPICE `ev2lin`（近地 SGP4），GPS 差 **18 km**（§3.6，头号坑之一）

## 2. 安装

上游唯一支持路线是 conda（`conda install -c tudat-team -c conda-forge tudatpy`）。本机用 micromamba：

```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj bin/micromamba   # 2 s，2.9.0
export MAMBA_ROOT_PREFIX=$PWD/mamba
# 官方全依赖：求解 334 包 / 下载 518 MB；本机盘剩 3.4 GB，解包到 2.9 GB 时 No space left → 失败
./bin/micromamba create -p ./env -c tudat-team -c conda-forge tudatpy
```

瘦身路线（本机实际用；跳过 qt/pyarrow/git/perl 等传递依赖）：

```bash
./bin/micromamba create -y -p ./env -c tudat-team -c conda-forge python=3.12 numpy=1.26 scipy pandas \
    boost-cpp=1.84 cspice nrlmsise-00 sofa-cmake tudat-resources=2.4 spiceypy tabulate tqdm colorama matplotlib-base
                                          # 97 包 / 182 MB / 27 s
./bin/micromamba install -y --no-deps -p ./env -c tudat-team tudatpy=1.0.0          # 7 s
./bin/micromamba install -y -p ./env -c conda-forge astropy-base astroquery          # 44 包 / 32 MB / 11 s（必需，见坑 2）
./bin/micromamba clean -a -y
./env/bin/python -c "import tudatpy,sys;print(tudatpy.__version__, sys.version.split()[0])"
# 1.0.0 3.12.14
```

`env` **1.2 GB**（`tudatpy` 包本体 64 MB）。`tudat-resources` 的 post-link 脚本再 `curl` **1.49 GB** `resource.tar.gz`（GitHub release v2.4）解到 **`~/.tudat/resource`**（2.23 GB / 176 项：spice_kernels 1.65 GB、atmosphere_tables 406 MB、gravity_models 122 MB、earth_orientation 6.8 MB…）；本机 17 s。解包中途盘满时 **`micromamba create` 仍返回 rc=0**（日志里只有 `tar: Exiting with failure status`）——装完务必核对：

```bash
curl -sL https://github.com/tudat-team/tudat-resources/releases/download/v2.4/resource.tar.gz | tar -tvzf - > res_list.txt   # 仅列表，17 s
awk '$1 !~ /^d/ {print $6}' res_list.txt | while read f; do [ -f ~/.tudat/$f ] || echo MISSING $f; done
# 缺了就：cd ~/.tudat && curl -sL <同 URL> | tar -xzf - --skip-old-files
```

## 3. 真命令 + 实测输出

数据与 [orekit §3](./orekit.md) 相同：BKG 镜像 `IGS0OPSULT_20262680000_02D_15M_ORB.SP3`（2026-09-25 00:00 GPST 起 48 h，15 min）· CelesTrak `gps-ops.tle`（2026-09-26 02:09 EDT 抓）PRN 02 = `28474`。

### 3.1 SPICE 内核

```python
import time; t=time.time()
from tudatpy.interface import spice
spice.load_standard_kernels()          # 读 ~/.tudat/resource/spice_kernels
print(spice.get_total_count_of_kernels_loaded())
```

```text
import s=0.23
load_standard_kernels s=0.03  maxRSS=76 MB
kernels loaded: 13
```

`import tudatpy.dynamics + estimation` 0.75–0.80 s。内核按需内存映射，0.03 s 是因为不预读；资源目录缺文件会在**用到时**才报 SPICE 错。

### 3.2 时间：GPST → TDB 秒（J2000 起）

```python
import tudatpy.astro.time_representation as tr
TS=tr.TimeScales; conv=tr.default_time_scale_converter()
t_naive=tr.date_time_components_to_epoch(2026,9,25,3,0,0.0)     # 843577200.0（无时间尺的“日历秒”）
t0=conv.convert_time(TS.tai_scale, TS.tdb_scale, t_naive+19.0)  # GPST=TAI−19 s → 843577251.182393 TDB
```

```text
TDB−TAI=32.182393  TT−TAI=32.184000  UTC−TAI=−37.000000  UT1−TAI=−37.000020（stock EOP，见坑 4）
```

### 3.3 地球自转与帧：SP3(ITRF) → 惯性初值

```python
from tudatpy.dynamics import environment_setup as es, environment as envm
from tudatpy.dynamics.environment_setup import rotation_model as rm
bs=es.get_default_body_settings(['Sun','Moon','Earth'],'Earth','J2000')
bs.get('Earth').rotation_model_settings=rm.gcrs_to_itrs(rm.IAUConventions.iau_2006,'J2000')  # IERS 2010，CIO 法
bs.get('Earth').gravity_field_settings.associated_reference_frame='ITRS'                    # 默认 IAU_Earth，必须改
x_inertial=envm.transform_to_inertial_orientation(np.r_[x_itrf,v_itrf], t0, bodies.get('Earth').rotation_model)
x_itrf=bodies.get('Earth').rotation_model.inertial_to_body_fixed_rotation(t)@x_inertial[:3]   # 回 ITRF 比 SP3
```

SP3（IGS20≈ITRF2020）直接当 ITRS 用；初速度 = 惯性系里 11 点 Lagrange 求导（SP3 无 V 行）。与 Orekit GCRF 初值（§3.4 同历元）比：

```text
J2000, stock EOP(止于 2024-09-03)      dpos=39.847 m  dvel=0.00441 m/s
J2000, EOP 续到 2027-09（finals2000A）  dpos= 2.486 m  dvel=0.00048 m/s   ← 差的是 J2000↔GCRS 帧偏差
全局帧 'GCRS', EOP 续               dpos= 0.005 m  dvel=0.00043 m/s   ← 只能用于换算，传播会报 SPICE(UNKNOWNFRAME)
UT1−UTC @2026-09-25：stock −0.000024 s（=0，静默）/ 续表 −0.013947 s（Orekit −0.01395）
```

EOP 续表做法：把 orekit-data 的 `finals2000A.all`（Bulletin A，I/P 行）追加成 C04 格式行，覆盖 `~/.tudat/resource/earth_orientation/eopc04_14_IAU2000.62-now.txt`（先备份；dX/dY mas→″）。tudatpy 1.0 **没有**换 EOP 文件的 API 参数。

### 3.4 PRN 02 · 24 h 数值积分 vs SP3（同 Orekit 算例）

初值 2026-09-25 03:00 GPST，m=1100 kg、A=13 m²、Cr=1.5（猜）；Earth 12×12（默认 GGM02C）、Sun/Moon 点质量、cannonball SRP（遮挡体 Earth+Moon）、Schwarzschild；RKF78 定步 60 s；输出插值到 97 个 SP3 历元，转 ITRF 求 3D 差。

```python
from tudatpy.dynamics import propagation_setup as ps, simulator
from tudatpy.dynamics.environment_setup import radiation_pressure as rp
bs.add_empty_settings('GPS02'); bs.get('GPS02').constant_mass=1100.0
bs.get('GPS02').radiation_pressure_target_settings=rp.cannonball_radiation_target(13.0,1.5,{'Sun':['Earth','Moon']})
acc={'Earth':[ps.acceleration.spherical_harmonic_gravity(12,12), ps.acceleration.relativistic_correction(True)],
     'Sun':[ps.acceleration.point_mass_gravity(), ps.acceleration.radiation_pressure()],
     'Moon':[ps.acceleration.point_mass_gravity()]}
am=ps.create_acceleration_models(bodies,{'GPS02':acc},['GPS02'],['Earth'])
integ=ps.integrator.runge_kutta_fixed_step(60.0, ps.integrator.CoefficientSets.rkf_78)
s=ps.propagator.translational(['Earth'],am,['GPS02'],x0,t0,integ,ps.propagator.time_termination(t0+86400+600))
hist=simulator.create_dynamics_simulator(bodies,s).propagation_results.state_history   # {t_TDB: 6-vector}
```

```text
12x12+Sun/Moon+SRP+GR                    mean=   14.07 @6h=   4.11 @12h=  16.03 @24h=   29.15 m  (1.92s, 1451 steps)
12x12+Sun/Moon+GR (no SRP)               mean=   82.07 @6h=  34.89 @12h=  97.11 @24h=  190.32 m  (1.85s, 1451 steps)
12x12 only                               mean= 1402.97 @6h= 492.35 @12h=1587.43 @24h= 3126.10 m  (1.84s, 1451 steps)
J2 (2x0 via deg=2) only                  mean= 1323.61 @6h= 487.15 @12h=1482.20 @24h= 2972.29 m  (1.75s, 1451 steps)
```

**同一初速度才可比**：把 Orekit 的 SP3 插值速度（7 点、ITRF、仅位置）喂给 tudat：

```text
orekit-vel dv vs 10pt = 0.499 mm/s
ORK vel: 12x12+Sun/Moon+SRP+GR               mean=   46.14 @6h=  21.68 @12h=  41.67 @24h=   86.16 m
ORK vel: 12x12+Sun/Moon+GR (no SRP)          mean=   52.96 @6h=  12.38 @12h=  47.09 @24h=   91.22 m
ORK vel: 12x12 only                          mean= 1452.70 @6h= 498.92 @12h=1640.26 @24h= 3231.28 m
ORK vel: 2x2 only                            mean= 1372.89 @6h= 491.72 @12h=1534.63 @24h= 3076.87 m
```

| 算例（24 h，3D vs SP3） | Orekit 均值 / @24h | tudat 同初速 | tudat 自己 11 点惯性速度 |
| --- | --- | --- | --- |
| 12×12 + 日月 + SRP(Cr 1.5) + GR | 41.4 / 75.5 m | 46.1 / 86.2 m | **14.1 / 29.2 m** |
| 去 SRP | 55.3 / 100.2 m | 53.0 / 91.2 m | 82.1 / 190.3 m |
| 12×12 only | 1448 / 3220 m | 1453 / 3231 m | 1403 / 3126 m |
| 2×2（Orekit 标“J2”） | 1368 / 3066 m | 1373 / 3077 m | 1324 / 2972 m |
| 12 h 拟合估 Cr（§3.5） | 1.879，RMS 0.443 m | — | **1.851 ± 0.054**，RMS 0.370 m |
| 24 h 拟合估 Cr | 1.891，RMS 0.552 m | — | **1.901 ± 0.007**，RMS 0.521 m |
| TLE vs SP3（0–24 h） | 535 m（SDP4） | — | **17 852 m**（ev2lin，§3.6） |

读法：同初速时两库差 **≤ 5 m / 1–2%**（重力场 GGM02C vs EIGEN-6S、日月星历、SRP 常数不同）；**0.5 mm/s 初速差 = 24 h 后 ~60–100 m**，单点初值传播主要在比插值，不是比力模型。

初速插值点数（`npts+1` 点，惯性系）：

```text
npts= 4 dv vs 10pt = 34.141 mm/s  mean= 4252.58 @24h= 8404.49 m
npts= 6 dv vs 10pt =  0.124 mm/s  mean=   10.87 @24h=   17.45 m   ← 碰巧更好，不代表更准
npts= 8 dv vs 10pt =  0.002 mm/s  mean=   14.13 @24h=   29.38 m
npts=10 / 12                       mean=   14.07 / 14.06 @24h= 29.15 / 29.13 m
```

积分器（全模型）：RKF78 定步 30/120/300 s 结果不变（14.07 m），900 s 14.06 m；RKDP87 变步 tol 1e-8/1e-10/1e-12 → 100/101/138 步、0.13–0.19 s，均 14.07 m。GPS 高度积分误差可忽略，**别把 SP3 差归咎积分器**。重力场换 `egm96` 13.91 m、`goco05c` 14.07 m、`ggm02c` 14.06 m。

### 3.5 估 Cr：SP3 位置当观测

```python
from tudatpy.estimation import estimation_analysis as ea
from tudatpy.dynamics import parameters_setup as pa
bs.get('GPS02').ephemeris_settings=es.ephemeris.tabulated(tab,'Earth','J2000')   # tab={t_TDB: 惯性 6 维}，来自 SP3
out=ea.create_best_fit_to_ephemeris(bodies, am, ['GPS02'], ['Earth'], integ, t0, t0+48*900.0, 900.0,
        [pa.radiation_pressure_coefficient('GPS02')], 6, True, 0.0)
out.final_parameters[6], out.formal_errors[6]
```

```text
Calculating residuals and partials 120
Current residual: 5.97695
Parameter update    0.741018      1.20235    -0.900939 -1.32532e-05  8.39557e-06  5.86067e-05     0.351374
...
fit 49 epochs (12h) positions (x,y,z) in J2000: est Cr=1.8514  sigma=0.0542  RMS=0.370 m  n_obs=120 (5.9s)
  3D vs SP3 (ITRF): in-fit mean=0.698 max=1.675 | beyond fit to +24h mean=2.803 max=4.581 | @24h=3.772 m
fit 97 epochs (24h) positions (x,y,z) in J2000: est Cr=1.9008  sigma=0.0065  RMS=0.521 m  n_obs=264 (11.8s)
  3D vs SP3 (ITRF): in-fit mean=0.907 max=1.747 | @24h=1.747 m
```

一次迭代就收敛（Cr 1.5→1.8514）；Orekit 12 h 外推 +24 h 均值 1.77 m / @24h 2.81 m，tudat 2.80 / 3.77 m；24 h 拟合 in-fit 均值两边都是 0.906–0.907 m。

### 3.6 TLE / SGP4

```python
bs.add_empty_settings('G02'); bs.get('G02').ephemeris_settings=es.ephemeris.sgp4(l1,l2,'Earth','J2000')
```

```text
tudat SGP4 (J2000->ITRS) vs SP3 G02, 0-24h (97 ep): mean=17851.6 max=20891.1 m
tudat sgp4 vs R*spiceypy.evsgp4(same TDB t): mean=18060.054 max=21496.902 m
spice evsgp4(TDB t) vs python-sgp4(UTC=t-69.1839), both TEME: mean=5.937 max=6.091 m
tudat sgp4 ephemeris vs R*spiceypy.ev2lin(UTC t, tudat epoch): mean=0.0000 max=0.0000 m
ISS: tudat sgp4 vs python-sgp4 (TEME->J2000 same matrix), 24h/145 ep: mean=51.724 max=77.289 m
```

docstring 说用 `evsgp4_c`，实际 C++（`spiceInterface.cpp::getCartesianStateFromTleAtEpoch`）调 **`ev2lin_`**＝近地 SGP4，无深空项；GPS（12 h 周期）必错。LEO 与 python-sgp4 差 ~50 m。TLE 请走 [python-sgp4](./python-sgp4.md)，再把状态喂给 tudat。

## 4. I/O

| 输入 | 读法 |
| --- | --- |
| SP3 | 自己解析 → `ephemeris.tabulated(dict,'Earth','J2000')`（固定 6 阶 Lagrange）或当初值 |
| TLE | `ephemeris.sgp4(l1,l2)`（近地 only）/ `environment.Tle(l1+'\n'+l2)` 取根数 |
| 数据 | `~/.tudat/resource`：SPICE、重力场（Earth：GGM02C 默认、GGM02S、EGM96、GOCO05c）、EOP、空间天气 |

| 输出 | 单位 / 帧 |
| --- | --- |
| `propagation_results.state_history` | `{float t_TDB: ndarray(6)}`，m、m/s，全局帧（J2000） |
| `inertial_to_body_fixed_rotation(t)` | 3×3，惯性→ITRS（`gcrs_to_itrs` 时） |
| `EstimationOutput` | `final_parameters`、`formal_errors`、`final_residuals`、`parameter_history` |

## 5. 参数

| 参数 | 取值 | 影响 |
| --- | --- | --- |
| 全局帧 | `'J2000'` | `'GCRS'` 可建体但传播时 SPICE 不认（坑 6） |
| `rotation_model` | `gcrs_to_itrs(iau_2006,'J2000')` | 默认 IAU_Earth：24 h 均值 205.7 m（坑 5） |
| `gravity_field_settings.associated_reference_frame` | `'ITRS'` | 不改直接报错（坑 7） |
| `spherical_harmonic_gravity(n,m)` | 12,12 | 默认场 GGM02C 201×201 截断；μ=3.9860044150e14，R=6378136.3 m |
| `cannonball_radiation_target(A,Cr,{Sun:[遮挡体]})` | 13, 1.5, Earth+Moon | 可估 Cr（§3.5） |
| 积分器 | RKF78 定步 60 s / RKDP87 tol 1e-10 | GPS 下几乎无影响（§3.4） |
| 初速插值点数 | ≥ 9 点，惯性系 | 5 点 = 8.4 km @24h |

## 6. 接到哪步

SP3 / TLE（[data-access](../data-access.md) · [sp3](./sp3.md) · [gnssanalysis](./gnssanalysis.md) · [python-sgp4](./python-sgp4.md)）→ **tudatpy（力模型积分 / 拟合 / 估参）** → 惯性或 ITRS 坐标 → 高度角 / IPP（本书 TEC 流程）。只要 SP3 插值不需要本库。

## 7. 坑（均实测）

1. **不能 pip、conda-forge 也没有**：PyPI 404、`conda-forge/tudatpy` 404；`-c conda-forge` 单独求解 → `tudatpy =* * does not exist`。必须 `-c tudat-team -c conda-forge`。
2. **`--no-deps` 瘦装缺 astropy**：`import tudatpy.dynamics` → `ModuleNotFoundError: No module named 'astropy'`（`ephemeris/horizons_wrapper.py` 顶层 import）。装 `astropy-base astroquery`。
3. **资源 2.2 GB 在 `$HOME/.tudat`，失败不报错**：post-link 下 1.49 GB，盘满时 conda rc=0、目录半截（本机第一次缺 `gravity_models`/`quadrature`）。§2 核对脚本。
4. **EOP 过期静默置零**：自带 `eopc04_14` 止于 **2024-09-03**；2024-09-10 起 UT1−UTC=0.000006 s、极移=0，无警告。结果：初值差 Orekit **39.8 m**，24 h 传播对 SP3 均值 **227.47 m**（续表后 14.07 m）——极移错是体固系转动，**不能**靠“进出同一模型”抵消。
5. **默认地球自转是 `IAU_Earth`**（非 IERS 2010）：SP3 当 IAU_Earth 用 → 24 h 均值 **205.70 m**。精密必须 `gcrs_to_itrs`。`rm.spice('J2000','ITRF93')` 在 2026 → `SPICE(FRAMEDATANOTFOUND)`（自带 bpc 不覆盖/未加载）。
6. **全局帧 `'GCRS'`**：换算 OK，传播时 `SPICE(UNKNOWNFRAME) The string supplied to specify the reference frame was 'GCRS'`，积分 0 步就退出（`Error, propagation terminated at t=843577251.182393`）且**不抛异常**，下游拿到 1 个点。用 `'J2000'`（与 GCRS 差 2.5 m 帧偏差，tudat 内部补）。
7. **重力场帧名**：换了 `gcrs_to_itrs` 不改场帧 → `RuntimeError: ... rotation model found for Earth is incompatible, frames are: ITRS and IAU_Earth`。
8. **时间是 TDB 浮点秒**：`date_time_components_to_epoch` 给的是无尺度日历秒；GPST 要 +19 s 当 TAI 再转 TDB，差 **51.18 s**（GPS 4 km/s ≈ 200 km）。
9. **`ephemeris.sgp4` = ev2lin**：GPS 对 SP3 **17.9 km**（python-sgp4 535 m），与 `spiceypy.ev2lin` 逐点 0.0000 m 相同（§3.6）。
10. **API 签名变了**（1.0）：`runge_kutta_variable_step(step, coeffs, control)` → `TypeError: incompatible function arguments`，必须再给 `step_size_validation(min,max)`；旧教程的 `tudatpy.numerical_simulation.*` 在 1.0 仍可 import（兼容），新文档与本文用 `tudatpy.dynamics.*`。
11. **`create_best_fit_to_ephemeris` 观测数少于历元**：12 h/49 历元只用 **40**（120 分量），24 h/97 历元用 **88**（264）；RMS 是逐分量，不是 3D。
12. **初速主导误差**：0.5 mm/s → 24 h 60–100 m（§3.4）；比较两库先统一初值。
13. **内存/时间**：单次 24 h 全模型 60 s 步 1.9 s；8 次传播进程 13.9 s；估计 12 h 5.9 s；maxRSS 165–212 MB（Orekit 301 MB）。安装盘占 env 1.2 GB + 资源 2.2 GB。

## 8. 选型

| 需求 | 用 |
| --- | --- |
| TLE → km 级位置 / 过境 | [python-sgp4](./python-sgp4.md)（**别用** tudat `sgp4` 给 GPS） |
| 严格 IERS 帧 + SP3 解析 + 积分/拟合，一个库全包、EOP 数据包好更新 | [orekit](./orekit.md) |
| Python/conda 原生积分 + 变分方程 + 估参（多参数、多弧、自定义加速度） | **tudatpy（本文）** |
| 精密 SP3 批量比较 / 合并 | [gnssanalysis](./gnssanalysis.md) · [sp3](./sp3.md) |
| GNSS 测地级 POD | Ginan / GROOPS（专用链） |
