# Orekit · 航天动力学库（Python 包装 orekit_jpype）操作手册

目录：`PROJECTS.json` **`Orekit`**（orbit-clock，Java）· 上游 <https://github.com/CS-SI/Orekit>（GitHub 镜像；主仓 gitlab.orekit.org）· develop **`8c71f7b`**（2026-09-24 15:52 EDT）· 最新 tag **13.1.8** · **Apache-2.0** · ★299 · 本机：PyPI **`orekit_jpype` 13.1.8.0**（2026-09-20 上传，内置 `orekit-13.1.8.jar` + Hipparchus **4.0.3**）/ **JPype1 1.7.1** / OpenJDK **21.0.12.1** / Python **3.13.5** · 真跑 2026-09-26 02:17–02:21 EDT

> 岗位：Java 航天动力学全家桶：时间尺、IERS 帧、TLE/SGP4、SP3/CPF/OEM 读写、**数值积分**（重力场 + 三体 + 太阳辐射压 SRP + 相对论）、定轨/拟合。本库管轨道 **位置/速度**，不管 TEC、不管观测值。冲突时：**上游 javadoc / 官方教程 > 本文**。
> 姊妹篇：[python-sgp4](./python-sgp4.md)（同一 TLE 的 TEME 基准）· [satellite-js](./satellite-js.md) · 精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md) / [gnssanalysis](./gnssanalysis.md)。

## 1. 用途与边界

**做：** `TLEPropagator`（SGP4/SDP4）→ 任意帧（TEME/GCRF/ITRF，带完整 IERS EOP）；`SP3Parser` 读 SP3-c/d 并插值；`NumericalPropagator` 力模型积分；`JacobianPropagatorConverter` 把数值模型拟合到星历。

**不做：**

- **不带数据**：EOP、闰秒、JPL 星历、重力场要另装 `orekit-data`（§3.1，头号坑）
- **不下 TLE / SP3**：自己从 CelesTrak / BKG / CDDIS 拉（[data-access](../data-access.md)）
- **不是 GNSS 处理器**：不做伪距/相位解算、钟差估计、TEC

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `orekit_jpype`（PyPI） | JPype 桥，调原生 jar | `import orekit_jpype; orekit_jpype.initVM()` |
| conda-forge `orekit` | 旧的 JCC 包装（conda-forge 最新 13.1），API 相同、导入方式不同 | `import orekit; orekit.initVM()` + `from orekit.pyhelpers import setup_orekit_curdir`（本文**未实跑**） |
| Orekit Java | Maven `org.orekit:orekit` | 需要 JVM 项目时用 |
| [gmat](./gmat.md) | NASA GUI/脚本任务设计工具 | 脚本 `.script`，不是库 |

## 2. 安装

```bash
python3 -m venv venv && . venv/bin/activate
pip install orekit_jpype sgp4 astropy numpy          # 7 s；orekit_jpype 13.1.8.0 + jpype1 1.7.1
pip install git+https://gitlab.orekit.org/orekit/orekit-data.git   # 9.5 s；orekitdata 0.dev0+untagged.103.g3e376b3
java -version   # 需要本机 JDK（本机 21.0.12.1）；JPype 会自动找 libjvm.so
```

`orekit-data` HEAD **`3e376b3`**（2026-09-03 03:40 EDT，"Updated to September 2026"）：`finals2000A.all` 最后观测值（I）**MJD 61279 = 2026-08-27**，预测（P）到 **2027-09-04**；`tai-utc.dat` 最后一条 2017-01-01（TAI−UTC=37 s）；重力场 `eigen-6s.gfc`；`DE-440-ephemerides`。

## 3. 真命令 + 实测输出

测试数据与 [python-sgp4 §3](./python-sgp4.md) 相同：CelesTrak `gps-ops.tle`（2026-09-26 02:09:18 EDT 抓）PRN 02 = `28474`，历元 `26268.06454359`；BKG 公开镜像 `https://igs.bkg.bund.de/root_ftp/IGS/products/2437/IGS0OPSULT_20262680000_02D_15M_ORB.SP3.gz`（2026-09-25 00:00 GPST 起 48 h / 192 历元，前 24 h 观测段）。

### 3.1 没有 orekit-data 会怎样（原样）

```python
import orekit_jpype as orekit; orekit.initVM()
from orekit_jpype.pyhelpers import setup_orekit_data
setup_orekit_data(from_pip_library=True)   # 未装 orekitdata、也没有 ./orekit-data.zip
from org.orekit.time import TimeScalesFactory
TimeScalesFactory.getUTC()
```

```text
WARNING:root:Failed to load orekitdata library.
                  Install with `pip install git+https://gitlab.orekit.org/orekit/orekit-data.git`
WARNING:root:File or folder: /workspace/orekitwork/orekit-data.zip not found
org.orekit.errors.OrekitException: no IERS UTC-TAI history data loaded
```

`setup_orekit_data` 只打 WARNING **不抛异常**，真正炸在第一次用 UTC 时。备选：`pyhelpers.download_orekit_data_curdir()` 下 `orekit-data-main.zip` 到当前目录，再 `setup_orekit_data('orekit-data.zip', from_pip_library=False)`。

### 3.2 TLE → TEME/ITRF，交叉 python-sgp4 / astropy / SP3（本人比对）

```python
import orekit_jpype as orekit; orekit.initVM()
from orekit_jpype.pyhelpers import setup_orekit_data; setup_orekit_data(from_pip_library=True)
from org.orekit.time import TimeScalesFactory
from org.orekit.frames import FramesFactory
from org.orekit.utils import IERSConventions
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.files.sp3 import SP3Parser
from org.orekit.data import DataSource
tle  = TLE(l1, l2); prop = TLEPropagator.selectExtrapolator(tle)
teme = FramesFactory.getTEME()
itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, False)   # False = 完整 EOP（非 simpleEOP）
sp3  = SP3Parser().parse(DataSource('IGS0OPSULT_20262680000_02D_15M_ORB.SP3'))
eph  = sp3.getSatellites().get('G02'); cs = eph.getSegments().get(0).getCoordinates()
for k in range(96):                      # SP3 历元（GPST），Orekit AbsoluteDate 自动换算
    d = cs.get(k).getDate()
    r_teme = prop.getPVCoordinates(d, teme).getPosition()
    r_itrf = prop.getPVCoordinates(d, itrf).getPosition()
```

```text
initVM+data s=0.52
GPS-UTC at 2026-09-25: 18.0
TLE epoch 2026-09-25T01:32:56.566176 sat 28474
SP3 timesys GPS coordsys IGc20 epochs 192 interp pts USE_P
G02 frame CIO/2010-based ITRF accurate EOP segments 1 interpSamples 7 filter USE_P
first SP3 epoch 2026-09-25T00:00:00.000 GPST = 2026-09-24T23:59:42.000 UTC
Orekit TEME vs python-sgp4 TEME: mean=6.432e-07 max=2.177e-05 m
Orekit ITRF(IERS2010,full EOP) vs astropy ITRS: mean=3.815 max=5.534 m
Orekit ITRF simpleEOP vs full EOP: mean=0.04981 max=0.08207 m
Orekit SGP4->ITRF vs SP3 G02: mean=535.2 max=831.4 m
astropy SGP4->ITRS vs SP3 G02: mean=534 max=828.4 m
total s=2.36
```

读法：SGP4 本体与 python-sgp4 **差 ≤ 22 µm**（同 Vallado 算法）；TEME→ITRF 与 astropy 差 **~4 m**（IERS 2010/2003/1996 都是 3.80–3.82 m；UT1−UTC 两边差 0.44 ms：Orekit −0.01395 s vs astropy −0.01351 s，只能解释约 0.9 m，余下是 TEME 定义/实现差异，未拆解）；对 SP3 **535 m**，与 python-sgp4 篇的 0.534 km 一致。误差来自 TLE，**不是**帧转换。`getGTOD`（无极移）对 astropy 差 **37 m**。

### 3.3 SP3 插值（留一法，本人比对）

用偶数历元（30 min 节点）做 `TimeStampedPVCoordinatesHermiteInterpolator(n, USE_P)`，预测奇数历元（15 min 中点）：

```text
SP3 LOO interp  4 pts @30min nodes -> 15min midpoints: mean=3589.714 max=4074.982 m (n=91)
SP3 LOO interp  8 pts @30min nodes -> 15min midpoints: mean=3.532 max=5.492 m (n=87)
SP3 LOO interp 10 pts @30min nodes -> 15min midpoints: mean=0.161 max=0.340 m (n=85)
SP3 LOO interp 12 pts @30min nodes -> 15min midpoints: mean=0.014 max=0.032 m (n=83)
SP3 propagator at 2026-09-25T02:37:30.000 GPST ITRF pos km [15295.21121098 -8751.05751271 20038.23216801] vel m/s [-193.93502874 2481.58196423 1316.12504832]
```

`eph.getPropagator()` 默认 **7 点**（`interpSamples 7`）、仅位置（`USE_P`，本文件无 V 行，速度由插值多项式求导）。ITRF 下地球自转让轨迹更弯，**点数不够会 km 级错**；精密用途 ≥ 10 点或换惯性系插值。

### 3.4 数值积分：从 SP3 状态起算 24 h（本人比对）

初值：SP3 插值 PV @ 2026-09-25 03:00 GPST → GCRF `CartesianOrbit`（a=26559.058 km, e=0.01710, i=54.974°）。`DormandPrince853`（1 mm 容差，步长 1 ms–300 s），输出转回 ITRF 与 SP3 逐历元比（97 点）。SRP 用**猜的**球模型：m=1100 kg, A=13 m², Cr=1.5（IIR 无盒翼模型）。

```text
HF12x12+Sun/Moon+SRP(cannonball)+GR    24h: 3D mean=   41.43 m  @6h=  20.51  @12h=  36.33  @24h=   75.51 m  (0.63s)
HF12x12+Sun/Moon+GR (no SRP)           24h: 3D mean=   55.26 m  @6h=  13.83  @12h=  51.72  @24h=  100.23 m  (0.18s)
HF12x12 only                           24h: 3D mean= 1447.85 m  @6h= 497.96  @12h=1634.80  @24h= 3220.46 m  (0.08s)
HF2x0 (J2) only                        24h: 3D mean= 1368.07 m  @6h= 490.85  @12h=1529.21  @24h= 3066.09 m  (0.05s)
```

再用 `NumericalPropagatorBuilder` + `JacobianPropagatorConverter(b, 1e-4, 100)` 拟合 SP3 位置（6 根数 + Cr）：

```text
fit 49 epochs (12h) positions-only, est Cr=1.879, fit RMS=0.443 m, evals=3 (4.9s)
  in-fit mean=0.686 m max=1.534 | beyond fit to +24h: mean=1.770 max=2.810 m | @24h=2.810 m
fit 97 epochs (24h) positions-only, est Cr=1.891, fit RMS=0.552 m, evals=4 (18.0s)
  in-fit mean=0.906 m max=1.406 | beyond fit to +24h: mean=0.000 max=0.000 m | @24h=1.406 m
```

结论：GPS 高度 **三体引力是主项**（去掉就 km 级）；单点初值 24 h ≈ 41 m 平均（误差主要来自插值速度）；拟合 12 h 后外推到 24 h **< 3 m**，对比 SGP4 的 **535 m**。

## 4. I/O

| 输入 | 读法 |
| --- | --- |
| TLE 两行 | `TLE(l1, l2)`；历元是 UTC |
| SP3-c/d | `SP3Parser().parse(DataSource(path))`；`.gz` 先解压或包 `DataSource` 过滤器 |
| orekit-data | `orekitdata` pip 包 / zip / 目录（`DirectoryCrawler`） |

| 输出 | 单位 / 帧 |
| --- | --- |
| `getPVCoordinates(date, frame)` | m、m/s；返回 Java `JDouble`，`float()` 或 `np.array` 转 |
| `AbsoluteDate.toString(ts)` | 按所给时间尺打印（UTC 输出带 `Z`） |
| SP3 `eph.getFrame()` | `IGc20` → `CIO/2010-based ITRF accurate EOP` |

## 5. 参数

| 参数 | 取值 | 影响 |
| --- | --- | --- |
| `getITRF(conv, simpleEOP)` | `IERS_2010`, `False` | `True` 省潮汐项，本例差 5–8 cm |
| `TLEPropagator.selectExtrapolator` | 自动选 SGP4/SDP4 | GPS（~12 h）走 SDP4 深空分支 |
| Hermite 点数 | 7（SP3 默认）/10–12 | §3.3 |
| `GravityFieldFactory.getNormalizedProvider(n, m)` | 12×12 | GPS 够用；J2-only 差 km |
| `NumericalPropagator.tolerances(dP, orbit, type)` | 0.001 m | 积分精度 |
| `IsotropicRadiationSingleCoefficient(A, Cr)` | 13 m², 1.5 | 猜值；可估 Cr（§3.4 估 1.88–1.89） |

## 6. 接到哪步

TLE/SP3 → **Orekit（帧/插值/积分）** → 卫星 ITRF 坐标 → 高度角 / IPP / 穿刺点（本书 TEC 流程）→ STEC→VTEC。只要 km 级可视化用 [python-sgp4](./python-sgp4.md)；精密 SP3 批处理用 [gnssanalysis](./gnssanalysis.md) / [sp3](./sp3.md)。

## 7. 坑（均实测）

1. **没 orekit-data**：`setup_orekit_data` 只 WARNING，稍后 `no IERS UTC-TAI history data loaded`（§3.1）。
2. **有闰秒、没 EOP 不报错**：目录只放 `tai-utc.dat`，`getITRF(...)` 照常返回，PRN 02 @03:00 GPST ITRF 位置差 **37.8 m**（15155.3224/−5275.0582/21422.7607 km vs 完整 EOP 15155.3475/−5275.0758/21422.7386 km）。
3. **EOP 过期静默外推为 0**：本数据 EOP history 到 **2027-10-24**；2027-11 UT1−UTC=0.00003 s、2028-11 0.00001 s（≈0，不报错）。每几个月 `pip install -U` orekit-data；2026-09-25 已是**预测段**（观测到 08-27）。
4. **在 `initVM()` 前 import Java 类**：`ModuleNotFoundError: No module named 'org'`。`initVM()` 第二次调用静默返回（不会换 classpath/参数）。
5. **UTC vs GPS 时间尺**：`AbsoluteDate(2026,9,25,0,0,0.0,utc)` 去比 SP3 首历元 → **57 685.8 m**；用 `gps` → 601.7 m。SP3 日期直接取 `cs.get(k).getDate()` 最安全。
6. **Orekit 13 的 `TimeOffset`**：`gps.offsetFromTAI(d) - utc.offsetFromTAI(d)` → `TypeError: unsupported operand type(s) for -: 'org.orekit.time.TimeOffset' and 'org.orekit.time.TimeOffset'`；要 `.toDouble()`（旧教程直接减）。
7. **JPype 类型**：`getX()` 返回 `<java class 'JDouble'>`；Java 对象不能下标（`'org.orekit.files.sp3.SP3Coordinate' object is not subscriptable`）；传列表要 `java.util.ArrayList`。`getPropagationParametersDrivers().getDrivers().get(0)` 不是 Cr（取到月球 GM=4.9028e12），要按 `getName()=='reflection coefficient'` 找。
8. **帧选错**：`getGTOD`（无极移）对 astropy 差 37 m；TEME 当 ITRF 用 = 万 km 级（见 [python-sgp4 §7](./python-sgp4.md)）。
9. **SP3 插值点数**：ITRF 30 min 节点 4 点 = 3.6 km、12 点 = 1.4 cm（§3.3）；数据边缘插值单侧，速度更差，数值积分初值别取首/末历元。
10. **TLE 历元漂移**：SGP4 vs SP3 0–24 h 均值 535 m，24–48 h **645 m**，最大 1119 m；TLE 超 1–2 天就换新。
11. **JVM 启动/内存**：`initVM` 0.5–1.05 s，最大 RSS **301 MB**（TLE+SP3 脚本）；循环里别重复起进程，批处理放一个进程。

## 8. 选型

| 需求 | 用 |
| --- | --- |
| TLE → km 级位置 / 过境，最轻 | [python-sgp4](./python-sgp4.md)（+astropy）/ [satellite-js](./satellite-js.md) |
| 严格 IERS 帧 + SP3 插值 + 数值积分 / 拟合，一个库全包 | **Orekit（本文）** |
| 精密 SP3 批量比较 / 合并 | [gnssanalysis](./gnssanalysis.md) · [sp3](./sp3.md) |
| GUI 任务设计 / 报告 | [gmat](./gmat.md) |
| Python 原生数值积分 / 估计（不用 JVM） | [tudatpy](./tudatpy.md) |
| 现成 EKF/UKF 定轨 + SSA 测角（Orekit 11 + gRPC，停更；同算例对照） | [orbdetpy](./orbdetpy.md) |
| pip 即装的 Rust 内核积分 + 位置观测 EKF 估 Cr（无 GR；同算例 38.0 / 67.0 m，Cr 1.911） | [nyx](./nyx.md) |
