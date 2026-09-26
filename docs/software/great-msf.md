# GREAT-MSF · 武大 GREAT 多源融合（PPP/RTK + INS）操作手册

目录：[`PROJECTS.json` → `GREAT-MSF`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-MSF> · 许可 **GPL-3.0** · ★**151** · tip **`4366a53`**（2025-11-01 09:20 EDT；无 tag；README 自称 **1.0**）· 本机：Debian g++ **14.2.0** / CMake **3.31.6** 源码编译（**无预编译 Linux 二进制**）· `-h` → **`GREAT-MSF [1.0.0]`** · 样例 `MSF_20201029` 城市车载 25 min：LCRTK/TCRTK/TCPPP 三模式 **exit 0** · 2026-09-26 00:31–00:39 EDT · **质检复跑**（2026-09-26 00:40–01:02 EDT，另起目录重 clone+编译）：tip/尺寸（`GREAT_MSF` **579456** B、`libLibGREAT.so` **4417416** B、`libLibGnut.so` **6788024** B）、原样链接 GL/GLFW undefined reference、§2 补丁后链接通过、三模式 exit 0、`.flt`/`.ins`/`.kml` 行数、`.ins` MeasType×AmbStatus 交叉计数、LCRTK `.flt` 首行与 Fixed 1495/Float 5、TCRTK Fixed 1490/Float 10、3D RMS **0.063/0.074/1.203** m（1498 秒匹配）全部逐字复现；Spent 43.1/45.7/13.3 s（本机负载 ≈37，墙时不可比）；TCPPP p95 用 numpy 默认线性插值得 1.628（原稿 1.632 属分位数算法差异，1.627–1.632）。新增坑 14：`-X` 写 stderr

> 岗位：**GNSS（PPP/RTK）+ IMU** 松/紧耦合滤波，XML 驱动；扩展自 [great-pvt](./great-pvt.md)。冲突时：**本机 `GREAT_MSF -h` / `-X` / `doc/*.pdf` > 本文**。

**质检边界：** 只跑了 `MSF_20201029` 一个包的 3 份 XML（LCPPP 与其余 3 个包未跑）；精度数字是本机用样例自带 `groundtruth/urban-groundtruth.txt` 逐秒比对 `.ins` 所得，**不是**上游公布值。未用 `plot/*.py`，未测 GLFW 可视化窗口（无显示跑）。

## 1. 用途与边界

**做：**

- INS 机械编排 + 误差补偿；**PPP/INS**、**RTK/INS** 松耦合（`LCI`）/紧耦合（`TCI`）
- PPP：`IONO_FREE` / 非差非组合；RTK：`RAW_MIX` + 模糊度固定（`SEARCH`、部分固定、ratio）
- 位置/速度辅助动态对准；ZUPT、NHC、轮速里程计（1.0 新增，说明文档 2.3/5.4 节）
- 自定义 IMU 轴向/单位/噪声；输出 `.flt`（GNSS）/`.ins`（融合）/`.kml`
- 同一 CMake 工程同时产出 `GREAT_MSF` 与一份 `GREAT_PVT`

**不做：**

- **不是** 产品生产：UPD → [great-upd](./great-upd.md)；卫星钟 → [great-pce](./great-pce.md)；定轨 → [great-podflt](./great-podflt.md)
- **不是** 因子图/ROS 栈 → [graphgnsslib](./graphgnsslib.md)；**不是** 纯 GNSS 精密 PVT → [great-pvt](./great-pvt.md)
- 视觉/LiDAR/UWB 上游称"陆续开源"，本版 **没有**
- 上游 README 只承诺 Windows；Linux "用户自行编译测试"（本机需 1 处补丁，见 §2）

| 术语 | 含义 |
| --- | --- |
| `LCI` / `TCI` | 松耦合（GNSS 位置当观测）/ 紧耦合（原始伪距相位进滤波） |
| `.flt` | GNSS 子滤波解（周内秒、ECEF、RMS、NSat、PDOP、AmbStatus、Ratio、基线长） |
| `.ins` | 融合解（ECEF、速度、姿态、陀螺/加表零偏、MeasType、AmbStatus） |
| `MeasType` | `GNSS`=该秒有 GNSS 更新；`INS`=纯惯导递推 |

## 2. 安装（Linux 源码；本机实测）

```bash
sudo apt-get install -y build-essential cmake libglfw3-dev libopengl-dev   # 本机已有 glfw 3.4-3
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/GREAT-WHU/GREAT-MSF.git   # 仓 ~190 MB 样例 zip 占大头
cd GREAT-MSF && git rev-parse --short HEAD    # 4366a53
```

**原样编译会在最后链接失败（本机实测）：** `-j8` 墙钟 **3m59s**（user 17m18s），exit **2**：

```text
/usr/bin/ld: .../build_Linux/Lib/libLibGREAT.so: undefined reference to `glVertex3f'
/usr/bin/ld: .../libLibGREAT.so: undefined reference to `glfwSetScrollCallback'
gmake: *** [Makefile:91: all] Error 2
```

原因：`third-party/GLFW` 只带 Windows `glfw3.lib`，Linux 分支不链 GLFW/GL。补丁（加在 `src/LibGREAT/CMakeLists.txt` 的 `else()` 分支 `link_directories(${BUILD_DIR}/Lib)` 之后）：

```cmake
    find_package(OpenGL REQUIRED)
    find_library(GLFW_LIB glfw REQUIRED)
    target_link_libraries(${PROJECT_NAME} ${GLFW_LIB} OpenGL::GL)
```

```bash
cmake -S src -B src/build -DCMAKE_BUILD_TYPE=Release
cmake --build src/build -j8        # 本机补丁后增量重链 <1 s，exit 0
export MSF_BIN=$PWD/src/build_Linux/Bin/GREAT_MSF
ls -l src/build_Linux/Bin src/build_Linux/Lib
```

**注意产物目录是 `<build 目录名>_Linux`**（CMake 里 `BUILD_DIR=${CMAKE_CURRENT_BINARY_DIR}_Linux`），不在 `build/` 里。本机产物（本机 build 目录为 `/tmp/msf0/build`，故产物在 `/tmp/msf0/build_Linux`）：

```text
Bin/GREAT_MSF  579456 B   Bin/GREAT_PVT  579784 B
Lib/libLibGREAT.so 4417416 B   Lib/libLibGnut.so 6788024 B
RUNPATH ${ORIGIN}/../Lib   （无需 LD_LIBRARY_PATH）
```

```bash
$MSF_BIN -h
```

```text
GREAT-MSF [1.0.0] compiled: Sep 26 2026 00:35:09 ($Rev: 2448 $)
Usage:
    -h|--help   .. this help            -V int  .. version
    -v int      .. verbosity level      -x file .. configuration input file
    --          .. configuration from stdinp
    -l file     .. spdlog output file   -X      .. output default configuration in XML
```

`-X` → exit 0，**115 行 / 3895 B** 默认 XML 骨架——**写到 stderr**：`GREAT_MSF -X > def.xml` 得 0 B 空文件，要 `GREAT_MSF -X 2> def.xml`；`-x /nonexist.xml` → exit **1**，`xconfig: not file read /nonexist.xml File was not found`。

## 3. 端到端：MSF_20201029 城市车载 25 min（本机真跑）

```bash
mkdir -p ~/iono_ops/msf-run && cd ~/iono_ops/msf-run
unzip -qo ~/iono_ops/GREAT-MSF/sample_data/MSF_20201029.zip     # 解压 215 MB
cd MSF_20201029
for f in xml/*.xml; do sed 's#\\#/#g' "$f" > "${f%.xml}_linux.xml"; done   # 反斜杠→正斜杠
mkdir -p result
env -u DISPLAY "$MSF_BIN" -x xml/GREAT_MSF_LCRTK_1029_linux.xml
```

包内容：`GNSS/Rover/SEPT3030.20O`、`GNSS/Base/R2933030.20o`、`GNSS/Product/`（BRDM + GBM 快速 SP3/CLK）、`IMU/ADIS.txt`（**240101** 行，100 Hz，`周内秒 Gyro_XYZ Accel_XYZ`）、`model/`（ATX/BLQ/DE405/EOP/闰秒）、`groundtruth/urban-groundtruth.txt`（**247543** 行）、4 份 XML（LC/TC × PPP/RTK）。窗口 `2020-10-29 05:59:00–06:24:00` GPST，1 Hz，GPS+GAL+BDS。

### 3.1 本机屏幕（LCRTK）

```text
xconfig: read from file xml/GREAT_MSF_LCRTK_1029_linux.xml
[W] warning: not defined upd mode[]
error: XDG_RUNTIME_DIR is invalid or not set in the environment.     ← 无显示环境 GLFW 噪声，不影响
SEPT: Start MSF Processing: 2020-10-29 05:59:00[GPS]   2020-10-29 06:24:00[GPS]
Alignment finished successfully:  2020-10-29 05:59:02[GPS]
Processing Epoch:  2020-10-29 06:23:59[GPS] Meas = GNSS 100.0%
Processing Finished!
Spent42.4364 seconds.
```

### 3.2 三模式结果（2026-09-26 00:36–00:38 EDT）

| XML | 墙钟 | `.flt`/`.ins`/`.kml` 行 | `.ins` MeasType/AmbStatus | 对 groundtruth 3D（1498 秒匹配） |
| --- | --- | --- | --- | --- |
| LCRTK | 46 s | 1503 / 1500 / 18073 | GNSS/Fixed 1484 · INS/Fixed 8 · INS/Float 6 | RMS **0.063** · p50 0.055 · p95 0.105 · max 0.516 m |
| TCRTK | 50 s | 1503 / 1500 / 18073 | GNSS/Fixed 1487 · GNSS/Float 10 · INS/Float 1 | RMS **0.074** · p50 0.057 · p95 0.107 · max 0.897 m |
| TCPPP | 18 s | 1502 / 1500 / 18073 | GNSS/Float 1497 · INS/Float 1 | RMS **1.203** · p50 1.069 · p95 1.632 · max 3.960 m |

LCRTK `.flt` 首行（sow 367140）：`NSat=23 PDOP=1.20 Fixed Ratio=4.12 BL=15187.248 m`；AmbStatus Fixed **1495** / Float **5**。TCPPP 25 min **全程 Float**、`.flt` 末历元 RMS≈(0.027,0.026,0.018) m——**短窗 PPP 未收敛是预期**，别拿它评 PPP/INS。比对脚本（自写）：按 `round(sow,2)` 把 `.ins` 第 1–4 列与 groundtruth 第 2–5 列配对算欧氏距离。

## 4. I/O

| 输入（XML `<inputs>`） | 说明 |
| --- | --- |
| `<rinexo>` | 流动站 + 基站观测（RTK 需 `<base>`/`<rover>` 与 `<receiver><rec id X Y Z>` 基站坐标，`<basepos>CFILE`） |
| `<rinexn>`/`<sp3>`/`<rinexc>` | 广播 + 精密轨道钟差 → [data-access](../data-access.md) |
| `<atx>`/`<blq>`/`<DE>`/`<EOP>` | 模型文件（样例 `model/` 自带） |
| `<imu>` | 文本 IMU：`sow gx gy gz ax ay az`，单位/轴向由 `<ins><DataFormat>` 解释 |

| 输出 | 含义 |
| --- | --- |
| `result/$(rec)-MSF.flt` | GNSS 解，RTK 带 Ratio/BL |
| `result/$(rec)-MSF.ins` | **融合轨迹 + 姿态 + 零偏**（主结果，1 Hz） |
| `result/$(rec)-MSF.kml` | Google Earth 轨迹 |
| cwd 下 `MSF`（8 KB）/`MSF.spd_log`（~8 MB）/`ratio-SEPT` | 日志与每历元 ratio，**写在当前目录** |

## 5. 关键参数

| 项 | 作用 |
| --- | --- |
| `<gen><beg>/<end>/<int>/<sys>` | 时段、采样、系统 |
| `<obs_combination>` | RTK 样例 `RAW_MIX`；PPP 样例 `IONO_FREE` |
| `<integration><GNSS Type>` | `OFF` / `LCI` / `TCI` |
| `<AntennaLever Type="RFU">` | 杆臂（右前上，m），样例 `0.01,-0.273,0.009` |
| `<Estimator Type>` | `Forward/Backward/FBS/RTS`（样例 Forward） |
| `<IMUErrorModel Type>` | `Customize` / `ADIS 16470` / `StarNeto` |
| `<Alignment Type>` | `OFF/STATIC/POS/VEL`；样例 `POS` + `CoarseAlignTime 300` |
| `<DataFormat>` | `AxisOrder`（garfu/gaflu/…）、`GyroUnit`（DPS/RPS/RAD/…）、`AcceUnit`、`Frequency` |
| `<ambiguity>` | `fix_mode SEARCH`、`part_fix`、`ratio 3`、`baseline_length_limit` |
| `<min_sat>` | LC 样例 6，TC 样例 2（紧耦合少星也能更新） |

## 6. 接到哪步

- 上游：观测 QC → [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)；精密产品下载 → [data-access](../data-access.md)
- PPP 固定需 UPD：[great-upd](./great-upd.md)（本样例 XML 未配，屏幕有 `not defined upd mode`）；自建钟/轨 → [great-pce](./great-pce.md) / [great-podflt](./great-podflt.md)
- 先用 [great-pvt](./great-pvt.md) 把纯 GNSS 解调通，再切本文加 IMU
- 因子图对照 → [graphgnsslib](./graphgnsslib.md)

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 链接 `undefined reference to glVertex3f / glfwSetScrollCallback` | 仓内 GLFW 仅 Windows `.lib` | §2 补丁 + `apt install libglfw3-dev libopengl-dev` |
| 2 | 编完在 `build/` 找不到二进制 | 产物在 `<build>_Linux/Bin` | `ls <build>_Linux/Bin` |
| 3 | **exit 0、Spent 0.7 s、`result/` 空** | 原版 XML `.\GNSS\Rover\...` 反斜杠 | `sed 's#\\#/#g'` 生成 `_linux.xml` |
| 4 | **exit 0、Spent 3.9e-05 s**，`Exception opening file ./IMU/ADIS.txt` | 不在样例根目录运行（路径相对 cwd） | `cd MSF_20201029` 再跑 |
| 5 | `ldd` 指向别处的 `libLibGREAT.so` | 残留 `LD_LIBRARY_PATH` 覆盖 RUNPATH | `unset LD_LIBRARY_PATH`；`ldd` 核对 |
| 6 | `error: XDG_RUNTIME_DIR is invalid` | GLFW 无显示环境 | 可忽略；本机 `env -u DISPLAY` 照常出结果 |
| 7 | 三个 XML 结果互相覆盖 | 输出名都是 `$(rec)-MSF.*` | 每跑完 `mv result res_<模式>` |
| 8 | TCPPP 米级、全程 Float | 25 min 未收敛 + 无 UPD | 长时段 + [great-upd](./great-upd.md)；别用短窗评 PPP/INS |
| 9 | `.ins` 零偏几百 deg/h 被当 bug | ADIS16470 MEMS 级 + 末段纯 INS | 看 `MeasType`；对照 `<GyroBias InitialSTD>` |
| 10 | 自有 IMU 发散 | 轴向/单位不符 | 改 `AxisOrder`/`GyroUnit`/`AcceUnit`/`Frequency`；先 `STATIC` 对准核 |
| 11 | 杆臂写反 | 坐标系是 RFU（右前上） | 按 RFU 填 `AntennaLever` |
| 12 | cwd 堆出 8 MB `MSF.spd_log` | 日志写当前目录 | 用 `-l file` 或 `<outputs verb>` 调 |
| 13 | clone 慢 | `sample_data/` 4 个 zip ≈190 MB | `--depth 1`；只解压需要的包 |
| 14 | `-X > def.xml` 得 **0 B** 空文件 | 默认 XML 输出到 **stderr** | `GREAT_MSF -X 2> def.xml`（115 行 / 3895 B） |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| GNSS+IMU 松/紧耦合（XML，武大体系） | **本文 GREAT-MSF** |
| 纯 GNSS PPP/RTK（有 Linux 预编译） | [great-pvt](./great-pvt.md) |
| UPD / 钟差 / 定轨产品 | [great-upd](./great-upd.md) / [great-pce](./great-pce.md) / [great-podflt](./great-podflt.md) |
| 因子图 GNSS（ROS） | [graphgnsslib](./graphgnsslib.md) |
| 轻量 RTK CLI | [rtklib](./rtklib.md) |

## 9. 相关

[great-pvt](./great-pvt.md) · [great-upd](./great-upd.md) · [great-ifcb](./great-ifcb.md) · [great-pce](./great-pce.md) · [great-podflt](./great-podflt.md) · [graphgnsslib](./graphgnsslib.md) · [data-access](../data-access.md) · [README](./README.md)

- 文档：`doc/GREAT-MSF 说明文档 1.1.pdf`、`doc/GREAT-MSF Documentation 1.1.pdf`、`doc/GREAT-MSF 代码讲解视频资料_2025年3月.pdf`
- 绘图：`plot/*.py`（numpy + matplotlib；本机未跑）
