# gnss-ins-sim 操作手册（GNSS/INS 轨迹 + IMU/GPS 传感器数据仿真）

> 仓库：<https://github.com/Aceinna/gnss-ins-sim> · Aceinna · **MIT** · ★1493 · tip **`966ff27`**（2024-11-27）· `setup.py` 版本 2.1，`ins_sim.py` 内 `VERSION = '3.0.0_alpha'`
> 本页实测：2026-09-26 01:00–01:08 EDT，Python 3.13 venv，`pip install -e .` 装到 numpy 2.5.3 / matplotlib 3.11.2，均无报错。

## 1. 它是什么 / 和 GNSS、电离层工作的关系

一句话：**你写一张“车怎么动”的表（运动定义），它算出真值轨迹，再按你给的误差参数生成带噪声的陀螺、加速度计、磁力计、GPS 位置/速度、里程计数据**，并可以把你自己的导航算法挂上去和真值比误差。

**先说清边界（看过源码）：**

- 它的“GNSS”只是**在真值位置/速度上加高斯白噪声**：`pathgen.gps_gen()` 里就是 `pos_noise = stdp * randn`、`vel_noise = stdv * randn`，没有别的误差项。
- **没有卫星、没有伪距/载波、没有星历、没有电离层/对流层模型、不输出 RINEX/NMEA。** `grep -riE "iono|tropo|pseudorange|ephemer|rinex|nmea"` 在仿真核心里零命中。
- 所以它**不能**用来研究电离层延迟、闪烁或 TEC。对 GNSS 这边的用处是：给 GNSS/INS 组合导航（松耦合滤波）准备“已知真值”的 IMU + GNSS 定位输入；比如测试“GNSS 中断 20 s（隧道、强闪烁导致失锁）期间 INS 能撑多久”，失锁本身要你用 `GPS visibility` 列**手动**指定。
- 要生成真正的 GNSS 信号/观测量，看 [gps-sdr-sim.md](./gps-sdr-sim.md)（基带 IQ）；要解算真实观测，看 [rtklib.md](./rtklib.md)。

**名词速查**

- **IMU**：惯性测量单元 = 3 轴陀螺（角速度，deg/s）+ 3 轴加速度计（比力，m/s²）。`axis=9` 再加 3 轴磁力计。
- **INS / 捷联惯导**：把 IMU 积分成姿态、速度、位置。误差随时间发散，所以要用 GNSS 周期性纠正（组合导航）。
- **bias（零偏）**：传感器静止时的非零输出。本工具分三部分：常值 `b`、**零偏不稳定性** `b_stability`（一阶马尔可夫漂移，相关时间 `b_corr` 秒）。
- **ARW（Angle Random Walk，角度随机游走）**：陀螺白噪声，单位 deg/√hr。换算到每个采样点的标准差 σ = ARW/60 × √fs（deg/s）。本页实测 0.25 deg/√hr、100 Hz → 理论 0.0417 deg/s，静止 5 s 实测 std **0.0447/0.0401/0.0410**。
- **VRW（Velocity Random Walk）**：加速度计白噪声，m/s/√hr。
- **运动定义（motion definition）**：CSV，第 2 行是初始位置（纬经高）/机体速度/欧拉角，第 4 行起每行一个运动命令（类型 1–5）+ 持续时间 + GPS 是否可见。
- **NED**：北-东-地坐标系（z 向下）。**body 系**：x 前、y 右、z 下。所以静止平放时加速度计 z 读数约 **−9.8 m/s²**（比力，不是重力本身）。本工具**不用 ENU**，从 ENU 习惯转过来的人要小心符号。
- **ZYX 欧拉角**：先绕 z（yaw 航向）、再 y（pitch 俯仰）、再 x（roll 横滚）。

## 2. 安装

```bash
git clone --depth 1 https://github.com/Aceinna/gnss-ins-sim
cd gnss-ins-sim
python3 -m venv .venv && . .venv/bin/activate
pip install -e .                  # 依赖只有 numpy、matplotlib
export MPLBACKEND=Agg             # 无显示器/不想弹窗
```

PyPI 上没有官方发布，按源码装。所有 demo 都假设**当前目录是仓库根**（见坑 1）。

## 3. 端到端实测

### 3.1 仓内最简 demo：只生成数据

```bash
MPLBACKEND=Agg python demo_no_algo.py
```

真实输出（节选，`plt.show()` 的 UserWarning 已略）：

```
Sample frequency of IMU: [fs] = 100.0 Hz
Reference frame: 1
Simulation time duration: 80.06 s
Simulation runs: 1
Simulation results are saved to /workspace/e2e/gnss-ins-sim/demo_saved_data/2026-09-26-05-00-14
The following results are saved:
	time: sample time
	ref_pos: true position in the local NED frame
	...
	gps: GPS position and velocity measurements in the local NED frame
	mag: magnetometer measurements
	ref_att_quat: true attitude (quaternion)
real	0m1.103s
```

输出目录名是**机器本地时间**戳（本机时钟为 UTC）。这个 demo 用 `ref_frame=1`，`gps-0.csv` 第一行是 `-2.707030832668846939e+06,4.688718241078561172e+06,3.360432169515063055e+06,...`——数值是 ECEF 量级，不是“local NED”（见坑 3）。

### 3.2 自写脚本：北京出发、直行、右转 90°、GPS 中断 20 s（`ref_frame=0`）

`my_motion.csv`：

```
ini lat (deg),ini lon (deg),ini alt (m),ini vx_body (m/s),ini vy_body (m/s),ini vz_body (m/s),ini yaw (deg),ini pitch (deg),ini roll (deg)
39.9042,116.4074,50,0,0,0,0,0,0
command type,yaw (deg),pitch (deg),roll (deg),vx_body (m/s),vy_body (m/s),vz_body (m/s),command duration (s),GPS visibility
1,0,0,0,0,0,0,10,1
2,0,0,0,15,0,0,20,1
1,0,0,0,0,0,0,20,1
3,90,0,0,0,0,0,15,1
1,0,0,0,0,0,0,20,0
1,0,0,0,0,0,0,15,1
```

含义：静止 10 s → 20 s 内加速到 15 m/s → 匀速 20 s → 15 s 内右转 90° → 匀速 20 s 且 **GPS 不可见** → 再 15 s。

`run_sim.py`：

```python
import numpy as np
from gnss_ins_sim.sim import imu_model, ins_sim
np.random.seed(42)                      # 库内不设种子，要复现必须自己设
imu_err = {'gyro_b': np.array([0.0, 0.0, 0.0]),          # deg/hr
           'gyro_arw': np.array([0.25, 0.25, 0.25]),      # deg/sqrt(hr)
           'gyro_b_stability': np.array([3.5, 3.5, 3.5]), # deg/hr
           'gyro_b_corr': np.array([100.0, 100.0, 100.0]),# s
           'accel_b': np.array([0.0, 0.0, 0.0]),          # m/s^2
           'accel_vrw': np.array([0.03, 0.03, 0.03]),     # m/s/sqrt(hr)
           'accel_b_stability': np.array([5e-5, 5e-5, 5e-5]),
           'accel_b_corr': np.array([100.0, 100.0, 100.0])}
gps_err = {'stdp': np.array([1.5, 1.5, 3.0]), 'stdv': np.array([0.05, 0.05, 0.05])}
imu = imu_model.IMU(accuracy=imu_err, axis=6, gps=True, gps_opt=gps_err)
sim = ins_sim.Sim([100.0, 1.0, 0.0], 'my_motion.csv', ref_frame=0, imu=imu,
                  mode=None, env=None, algorithm=None)
sim.run(1)
sim.results('out', gen_kml=True)
```

运行输出（原样节选）：

```
Reference frame: 0
Simulation time duration: 95.01 s
Simulation results are saved to /workspace/e2e/gis_run/out
	ref_pos: true LLA pos in the navigation frame
	ref_gps: true GPS LLA position and NED velocity
	gps: GPS LLA position and NED velocity measurements
```

输出文件（行数不含表头）：

```
accel-0.csv                    9501 rows | accel_x (m/s^2),accel_y (m/s^2),accel_z (m/s^2)
gps-0.csv                        96 rows | gps_lat (deg),gps_lon (deg),gps_alt (m),gps_vN (m/s),gps_vE (m/s),gps_vD (m/s)
gps_time.csv                     96 rows | gps_time (sec)
gps_visibility.csv               96 rows | gps_visibility ()
gyro-0.csv                     9501 rows | gyro_x (deg/s),gyro_y (deg/s),gyro_z (deg/s)
ref_accel.csv                  9501 rows | ref_accel_x (m/s^2),ref_accel_y (m/s^2),ref_accel_z (m/s^2)
ref_att_euler.csv              9501 rows | ref_Yaw (deg),ref_Pitch (deg),ref_Roll (deg)
ref_att_quat.csv               9501 rows | q0 (),q1,q2,q3
ref_gps.csv                      96 rows | ref_gps_lat (deg),ref_gps_lon (deg),ref_gps_alt (m),ref_gps_vN (m/s),ref_gps_vE (m/s),ref_gps_vD (m/s)
ref_gyro.csv                   9501 rows | ref_gyro_x (deg/s),ref_gyro_y (deg/s),ref_gyro_z (deg/s)
ref_pos.csv                    9501 rows | ref_pos_lat (deg),ref_pos_lon (deg),ref_pos_alt (m)
ref_vel.csv                    9501 rows | ref_vel_x (m/s),ref_vel_y (m/s),ref_vel_z (m/s)
time.csv                       9501 rows | time (sec)
```

另有 `ref_pos.kml`、`gps_0.kml`（Google Earth 可开）和 `summary.txt`。`-0` 后缀是第几次蒙特卡洛运行（`sim.run(N)` 会出 `-0…-(N-1)`，真值 `ref_*` 只有一份）。

用 numpy 检查（本机实测）：

```
gps epochs 96 visible 76 invisible at t= [61. 80.]
gps err std N/E/U (m): 1.55 1.48 2.81          # 设定 1.5/1.5/3.0
gps row at invisible epoch: [ 39.9083773  116.40992986  48.05519205]
static accel mean (first 5s): [ 1.0000e-04  2.0000e-04 -9.8014e+00]
static gyro std deg/s (first 5s): [0.0447 0.0401 0.041 ]
final yaw deg 89.95, final vel NED [1.2e-02 1.5e+01 0.0e+00]
final pos [ 39.908367 116.415868  50.      ]
```

读法：转弯后航向 89.95°、速度全在东向 15 m/s，说明命令类型 3（相对转 90°）按预期执行；**GPS 不可见的 t=61–80 s 期间 `gps-0.csv` 仍然有带噪声的数值**，只是 `gps_visibility=0`（坑 4）。

### 3.3 挂自带算法：纯惯导积分 10 次蒙特卡洛

```bash
MPLBACKEND=Agg python demo_free_integration.py
```

```
Simulation time duration: 10.0 s
Simulation runs: 10
-----------statistics for simulation position from algo (in units of ['m', 'm', 'm'])
	Simulation run algo0:
		--Max error: [0.12792156 0.03340563 0.02631552]
	Simulation run algo1:
		--Max error: [0.09542108 0.09448778 0.02968442]
```

（`err_stats_start=-1` 只统计最后一个点；两算法分别是带里程计/不带里程计的积分。每次运行随机数不同，你的数字会不一样。）输出目录里是 `pos_algo{0,1}_{0..9}_LLA.csv` + `.kml` 共 43 个文件。

其他 demo 在本机的真实状态：

| demo | 结果 |
|---|---|
| `demo_ins_loose.py` | 直接打印 `Still under development. Please try demo_aceinna_ins.py.` 退出 |
| `demo_aceinna_ins.py` | `Because the INS algorithm is compiled into a DLL, only Windows are supported.` |
| `demo_allan.py` | 可跑，1800 s 静止数据做 Allan 方差 |

也就是说**仓内没有能在 Linux 上直接跑的 GNSS/INS 组合滤波器**，组合算法要自己写并按 `demo_algorithms/free_integration.py` 的接口挂上。

## 4. 参数表

### 4.1 `ins_sim.Sim(fs, motion_def, ref_frame, imu, mode, env, algorithm)`

| 参数 | 取值 | 说明 |
|---|---|---|
| `fs` | `[fs_imu, fs_gps, fs_mag]` Hz | `fs_imu` 即仿真步长；`fs_gps=0` 不出 GPS；`fs_mag` 未使用（磁力计与 IMU 同频） |
| `motion_def` | CSV 路径 / 同内容字符串 / 数据目录 | 目录模式 = 用已录数据回放（`demo_gen_data_from_files.py`，`imu=None`） |
| `ref_frame` | `0` NED（默认）/ `1` 虚拟惯性系 | 0：位置输出纬经高；1：位置 = 初始 ECEF + 相对 NED 位移（源码注释承认这是为了生成 kml 的拼凑） |
| `imu` | `imu_model.IMU(...)` | 见 4.2 |
| `mode` | `None` 或 `[最大加速度 m/s², 最大角加速度 deg/s², 最大角速度 deg/s]` | 限制命令 2–5 的执行速度；字符串模式“not implemented yet” |
| `env` | `None` 或字典 `{'acc': ..., 'gyro': ...}`；值如 `'[0.1 0.01 0.11]g-random'`、`'[1 1 1]-5Hz-sinusoidal'`、陀螺用 `'[..]d-random'`，或 (n,4) 单边 PSD 数组 | 振动叠加到加速度计/陀螺（源码 `self.env.keys()`，传裸字符串会报错） |
| `algorithm` | 算法对象或列表 | 多算法需同输入同输出 |

`sim.run(N)` 跑 N 次；`sim.results(dir, err_stats_start=0, gen_kml=False)` 写文件；`sim.plot([...])` 画图；`sim.get_data([...])` 直接取内存数组。

### 4.2 `imu_model.IMU(accuracy, axis, gps, gps_opt, odo, odo_opt)`

| 键 | 单位 | 内置 low / mid / high（`imu_model.py` 源码值） |
|---|---|---|
| `gyro_b` | deg/hr | 0 / 0 / 0 |
| `gyro_b_stability` | deg/hr | 10 / 3.5 / 0.1 |
| `gyro_b_corr` | s | 100 / 100 / 100 |
| `gyro_arw` | deg/√hr | 0.75 / 0.25 / 0.002 |
| `accel_b` | m/s² | 0 / 0 / 0 |
| `accel_b_stability` | m/s² | 2e-4 / 5e-5 / 3.6e-6 |
| `accel_vrw` | m/s/√hr | 0.05 / 0.03 / 2.5e-5 |
| `mag_std` | µT | 0.1 / 0.01 / 0.001 |
| `gps_opt['stdp']` | m（N,E,D） | 默认 `[5, 5, 7]`（只有这一档） |
| `gps_opt['stdv']` | m/s | 默认 `[0.05, 0.05, 0.05]`（docstring 写“vertical RMS error”，实为速度） |
| `odo_opt` | `scale`, `stdv` m/s | 默认 0.99 / 0.1 |

源码注释：low 取自 Aceinna AHRS380、mid 部分取自 IMU381、high 部分取自 HG9900。`axis=6` 仅 IMU，`axis=9` 加磁力计（磁场用内置 **WMM-2015** 系数 `WMM.COF`）。

### 4.3 运动命令类型（CSV 第 1 列）

| 类型 | 第 2–7 列含义 | 第 8 列 |
|---|---|---|
| 1 | 欧拉角**变化率**（deg/s）+ 机体速度**变化率**（m/s²） | 精确持续时间 |
| 2 | 绝对姿态 + 绝对速度（目标值） | 最长时间，提前到达就进入下一条 |
| 3 | 相对姿态变化 + 相对速度变化 | 最长时间 |
| 4 | 绝对姿态 + 相对速度变化 | 最长时间 |
| 5 | 相对姿态变化 + 绝对速度 | 最长时间 |

第 9 列 `GPS visibility`：0/1。只想完全控制时长就全用类型 1。

## 5. 坑（现象 → 原因 → 修复命令）

1. **`UserWarning: genfromtxt: Empty input file: "['/tmp/demo_motion_def_files//motion_def-3d.csv']"` 然后 `IndexError: index 0 is out of bounds`**
   → demo 用 `os.path.abspath('.//demo_motion_def_files//')`，相对当前工作目录找文件。
   → `cd /path/to/gnss-ins-sim && MPLBACKEND=Agg python demo_no_algo.py`。

2. **`ValueError: accuracy should at least have keys: gyro_b, gyro_b_stability, gyro_arw, accel_b, accel_b_stability and accel_vrw`**
   → 自定义 IMU 字典缺了 6 个必需键之一（`*_b_corr`、`mag_std` 可选）。
   → 从 `demo_free_integration.py` 复制完整字典：`sed -n '/imu_err = {/,/}/p' demo_free_integration.py`。

3. **`ref_frame=1` 时 `ref_pos.csv`/`gps-0.csv` 标注 “local NED” 但数值是几百万米**
   → 虚拟惯性系下位置 = 初始 ECEF + NED 相对位移；表头文字没随之改。
   → 要纬经高就用 `ref_frame=0`：`sed -i 's/ref_frame=1/ref_frame=0/' demo_no_algo.py`。

4. **GPS 中断段里 `gps-0.csv` 仍有“正常”的位置，滤波器根本没经历中断**
   → 不可见历元照样写出带噪声的值，只在 `gps_visibility.csv` 标 0。
   → 读数据时必须过滤：`paste -d, gps-0.csv gps_visibility.csv | awk -F, 'NR==1||$7==1' > gps_visible.csv`。

5. **每次跑结果都不一样，写论文无法复现**
   → 库内全用 `np.random.randn` 且不设种子。
   → 在脚本开头 `import numpy as np; np.random.seed(42)`（本页 3.2 即如此）。

6. **远程/无显示环境里卡住或刷一堆 `FigureCanvasAgg is non-interactive`**
   → demo 末尾 `sim.plot(...)` 会调 `plt.show()`。
   → `export MPLBACKEND=Agg`，或删掉 plot 行：`sed -i '/sim.plot(/d' demo_no_algo.py`。

7. **把输出当 ENU 用，高度方向或加速度 z 符号全反**
   → 导航系是 NED（D 向下），body 系 z 向下；静止 `accel_z ≈ −9.80`（实测 −9.8014）。
   → 转 ENU：`awk -F, 'NR>1{print $2","$1","(-$3)}' ref_vel.csv`（N,E,D → E,N,U；`-$3` 必须加括号，否则 awk 把 `","-$3` 当减法吞掉逗号）。

8. **Linux 上跑 `demo_aceinna_ins.py` / `demo_ins_loose.py` 没有结果**
   → 前者只有 Windows DLL，后者直接提示“Still under development”。
   → 用可跑的纯惯导 demo 验证管线：`MPLBACKEND=Agg python demo_free_integration.py`，组合滤波自己实现。

9. **同一进程里自定义过 IMU 后，再用 `'low-accuracy'` 得到的却是自定义参数**
   → `IMU.__init__` 先 `self.gyro_err = gyro_low_accuracy`（模块级字典引用），再原地改键，等于改了全局默认。实测：内置 low 的 `arw` 从 0.000218 rad/√s 变成自定义的 0.002618，`reload` 后恢复。
   → 每个配置单独进程跑，或在创建前 `import importlib, gnss_ins_sim.sim.imu_model as m; importlib.reload(m)`。

## 6. 诚实的局限

- **GNSS 部分只是“真值 + 白噪声”的位置/速度**：无卫星几何（没有 DOP 概念）、无多路径、无电离层/对流层、无钟差、无伪距/载波，也没有时间相关误差。对电离层研究没有直接价值；最多是为“闪烁导致失锁”场景提供 INS 侧数据，失锁时段靠手工 `GPS visibility`。
- 地球模型：重力取初始点局地值，磁场用 WMM-2015 系数（2026 年已过有效期，WMM 每 5 年更新）。
- 没有可在 Linux 直接运行的组合导航算法（见 3.3 表）。
- `mode` 字符串模式、`fs_mag` 均未实现；`VERSION` 写着 `3.0.0_alpha`。
- 只做过本页三个 demo/脚本的实测；`demo_mag_cal.py`（依赖 `libmagcal.so`）、`demo_kml_gen.py`、`demo_ui_ans.py` 未跑。

## 7. 交叉链接

- [gps-sdr-sim.md](./gps-sdr-sim.md)：真正生成 GNSS 信号（基带 IQ）；它的 `-u` 吃 10 Hz ECEF 运动 CSV，可把本工具 `ref_pos` 降采样+转 ECEF 后喂进去（需自己写转换）
- [pymap3d.md](./pymap3d.md)：LLA / ECEF / NED / ENU 互转
- [gnss_lib_py.md](./gnss_lib_py.md)：真实 GNSS 测量的 Python 处理，与本工具的“仿真定位”对照
- [rtklib.md](./rtklib.md)：真实观测量解算，得到可替换 `gps-0.csv` 的 GNSS 位置
