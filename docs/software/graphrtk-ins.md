# GraphRTK-INS · 武大 GREAT 因子图 RTK / RTK+INS 紧耦合（GREAT-FGO）操作手册

目录：[`PROJECTS.json` → `GraphRTK-INS`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GraphRTK-INS> · 许可：GitHub 未识别（`license: null`），`doc/*.pdf` §3.2 写 **GPL-3.0** · ★**84** · tip **`25cf011`** = tag **`v1.1-beta`**（2026-07-23 02:22 EDT；另有 `v1.0-beta`）· README 自称 **GREAT-FGO 1.0 (Beta)** · 本机：Debian g++ **14.2.0** / CMake **3.31.6** 源码编译（**无 Linux 二进制**；需自编 **Ceres 1.14** + **2 处补丁**）· 样例 `FGO_20211012` 城市车载 1 h：RTK-FGO 与 TC-RTK/INS-FGO 两份 XML **exit 0** · 2026-09-26 00:40–01:31 EDT

> 岗位：**因子图（滑窗 + 边缘化）** 的 RTK 与 RTK/INS 紧耦合（IMU **预积分因子**），Ceres 求解，XML 驱动；与滤波版 [great-msf](./great-msf.md) 同源同 XML 风格。冲突时：**本机 `-h` / `doc/GraphRTK-INS说明文档 1.0.pdf` > 本文**。

**质检边界：** 只跑了 `FGO_20211012` 一个包（`FGO_20250928.rar` 未跑）；未跑 `plot/*.py`、未测 GLFW 窗口。精度数字是**本机自写脚本**把 `.fgo`/`.ins` 与包内 `ref/groundtruth_*.txt` 按周内秒逐秒比对所得，**不是**上游公布值；包内还附了**上游在 Windows 上跑出的 `result/`**，本文把它当第二参照。

## 1. 用途与边界

**做：**

- `GREAT_PVTFGO`：滑窗因子图 **RTK**（双差伪距/相位因子，模糊度 `SEARCH` 固定 + 边缘化传递模糊度先验）
- `GREAT_GINSFGO`：**TC RTK/INS** 因子图（IMU 预积分因子 + 双差因子；`msf_type GINS_TC`），动态快速初始化
- GPS/GLO/GAL/BDS-2/3；自定义 IMU 轴向/单位/噪声；输出 `.fgo`/`.ins`/`.kml`
- 同一工程顺带产出 `GREAT_PVT` 与 `GREAT_MSF`（与 [great-pvt](./great-pvt.md)/[great-msf](./great-msf.md) 同源）

**不做：**

- **不做 PPP**、不做 LC 松耦合（`<GNSS Type>` 文档只列 `TCI`）；滤波 PPP/INS 用 [great-msf](./great-msf.md)，因子图 PPP/INS 是姊妹仓 GREAT-PIFGO
- 视觉/LiDAR（`msf_type` 枚举里有 `VIL_SLAM/GVIL_*`，本版未开源）
- **不是**产品生产：UPD → [great-upd](./great-upd.md)；轨道钟差 → [great-podflt](./great-podflt.md) / [great-pce](./great-pce.md)
- 上游只承诺 Windows（VS 预编译 + Ceres `.lib/.dll`）；Linux "用户自行编译测试"

| 对照 | [great-msf](./great-msf.md)（滤波） | **GraphRTK-INS（因子图）** |
| --- | --- | --- |
| 估计器 | EKF（`Forward/Backward/FBS/RTS`） | 滑窗 FGO + Schur 边缘化，Ceres |
| GNSS 模式 | PPP + RTK | **只 RTK** |
| 耦合 | LCI / TCI | **TCI**（IMU 预积分） |
| 依赖 | GLFW/GL | GLFW/GL + **Ceres ≤2.1**（用 `LocalParameterization`）+ glog/gflags |
| 本机样例速度 | LCRTK 25 min 数据 46 s | TC 1 h 数据 **18 m41 s**（`Spent 1113.994 s`） |
| 本机样例精度（自算） | MSF_20201029 LCRTK 3D RMS 0.063 m | FGO_20211012 TC 3D RMS 0.414 m（前 3700 s；见 §3.3）|

两者样例不同、城市场景难度不同，**RMS 不可横比**。

## 2. 安装（Linux 源码；本机实测 ≈16 min）

```bash
sudo apt-get install -y build-essential cmake libeigen3-dev libgoogle-glog-dev libgflags-dev \
     libglfw3-dev libopengl-dev libarchive-tools          # bsdtar 解 RAR5
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/GREAT-WHU/GraphRTK-INS.git     # 457 MB（样例 2×~93 MB rar + Ceres Windows lib 58 MB）
```

**门 1：Ceres。** 仓内 `src/Third-party/ceres` 只有 Windows `.lib/.dll`（头文件是 **1.14**）。Debian 13 源里是 `libceres-dev 2.2`——**2.2 删了 `ceres::LocalParameterization`**，而 `gfactor/gpose_local_parameterization.h` 继承它，不能用。本机自编 1.14（墙钟 **~2.5 min** 含下载）：

```bash
curl -sL http://ceres-solver.org/ceres-solver-1.14.0.tar.gz | tar xz && cd ceres-solver-1.14.0
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
  -DBUILD_BENCHMARKS=OFF -DSUITESPARSE=OFF -DCXSPARSE=OFF -DLAPACK=OFF -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX=$HOME/iono_ops/ceres114
cmake --build build -j8 && cmake --install build        # → ceres114/lib/libceres.so.1.14.0
```

**门 2：原样编译第一步就挂（本机实测，21 s）：**

```text
src/LibGnut/gutils/gtriple.h:26:10: fatal error: Eigen/Dense: No such file or directory
```

原因：CMake 写 `${ROOT}/third-party/Eigen`，实际目录是 **`Third-party`**（Linux 大小写敏感）。用 `-DThird_Eigen_ROOT` / `-DThird_ceres_ROOT` 覆盖。

**补丁 A（链接）**：`src/LibGREAT/CMakeLists.txt` 的 Linux `else()` 分支 `link_directories(${ROOT}/build/Lib)` 之后加：

```cmake
	find_package(OpenGL REQUIRED)
	find_library(GLFW_LIB glfw REQUIRED)
	find_library(CERES_LIB ceres HINTS ${Third_ceres_ROOT}/lib REQUIRED NO_DEFAULT_PATH)
	target_link_libraries(${PROJECT_NAME} ${CERES_LIB} glog gflags ${GLFW_LIB} OpenGL::GL)
```

（Linux 分支原本不链 Ceres/GLFW/GL；GLFW/GL 与 great-msf 同病。本机是先打补丁再编，未单独复现"不打补丁时的链接报错"。）

**补丁 B（运行期崩溃，必须）**：`src/LibGREAT/gfgognss/gpvtfgo.cpp` 的 `bool t_gpvtfgo::_set_satdata(...)` 末尾缺 `return`（`g++ -fsyntax-only -Wreturn-type` 全仓扫只此 1 处）。GCC `-O3` 把"落出非 void 函数"当不可达 → RTK 第一历元即：

```text
terminate called after throwing an instance of 'std::length_error'
  what():  basic_string::_M_create           ← exit 134；gdb 栈顶 t_gpvtfgo::_set_satdata
```

在该函数最后的 `}` 前加一行 `return true;`（MSVC 不触发，所以上游 Windows 没事）。

```bash
cd ~/iono_ops/GraphRTK-INS
cmake -S src -B /tmp/fgo1/build -DCMAKE_BUILD_TYPE=Release \
  -DThird_Eigen_ROOT=/usr/include/eigen3 -DThird_ceres_ROOT=$HOME/iono_ops/ceres114
cmake --build /tmp/fgo1/build -j3          # 见坑 3：-j8 本机 OOM
cp -a ~/iono_ops/ceres114/lib/libceres.so* /tmp/fgo1/build_Linux/Lib/   # 见坑 4
export FGO_BIN=/tmp/fgo1/build_Linux/Bin
```

本机耗时：`-j8` 跑 **9m34s** 后 `c++: fatal error: Killed signal terminated program cc1plus`（`gnss_info_factor.cpp`，内存 15 GB 被其他进程占 9 GB）；续跑 `-j3` **3m30s** exit 0。产物在 **`<build 目录>_Linux/`**：

```text
Bin/GREAT_GINSFGO 590264 B   Bin/GREAT_PVTFGO 580984 B   Bin/GREAT_MSF 579264 B   Bin/GREAT_PVT 579784 B
Lib/libLibGREAT.so 5913672 B   Lib/libLibGnut.so 6792696 B      RUNPATH ${ORIGIN}/../Lib
```

```bash
$FGO_BIN/GREAT_GINSFGO -h
```

```text
G-Nut/PVT [0.9.0] compiled: Sep 26 2026 00:56:15 ($Rev: 2448 $)
Usage:
    -h|--help   .. this help            -V int  .. version
    -v int      .. verbosity level      -x file .. configuration input file
    --          .. configuration from stdinp
    -l file     .. spdlog output file   -X      .. output default configuration in XML
```

`GREAT_PVTFGO -h` 同款（横幅都是 **`G-Nut/PVT [0.9.0]`**，不是 FGO 版本号）。`-X` exit 0，但 XML **写 stderr**（`| wc` 得 0，用 `2>&1`），且只是 G-Nut 通用骨架、**没有 `<fgo>` 节点**——配置请抄样例 XML。`-x /nonexist.xml` → exit **1**，`xconfig: not file read /nonexist.xml File was not found`。

## 3. 端到端：FGO_20211012 城市车载 1 h（本机真跑）

```bash
mkdir -p ~/iono_ops/fgo-run && cd ~/iono_ops/fgo-run
bsdtar -xf ~/iono_ops/GraphRTK-INS/sample_data/FGO_20211012.rar     # 7 s；Debian 7zip 解不了，见坑 5
cd FGO_20211012
mv result result_upstream && mkdir result                            # 先保住上游参考结果！
for f in xml/*.xml; do sed 's#\\#/#g' "$f" > "${f%.xml}_linux.xml"; done
env -u DISPLAY $FGO_BIN/GREAT_PVTFGO  -x xml/GREAT-PVTFGO-RTK-1012-urban_linux.xml      > pvt.log  2>&1
env -u DISPLAY $FGO_BIN/GREAT_GINSFGO -x xml/GREAT-GINSFGO-TC-RTKINS-1012-urban_linux.xml > gins.log 2>&1
```

包内容：`GNSS/SEPT2850.21O`（流动站 137 MB，RINEX 3.04）、`GNSS/Base/WUDA2850.21o`（基站 71 MB）、`GNSS/BRDC00IGS_R_20212850000_01D_MN.rnx`（**只有广播星历**）、`IMU/smallimu_out.txt`（**1420190** 行，`sow gx gy gz ax ay az`，XML 声明 100 Hz/`garfu`/DPS/MPS2）、`model/`（ATX/BLQ/DE405/poleut1/闰秒）、`ref/groundtruth_1012_GNSS.txt`（天线相位中心）与 `ref/groundtruth_1012_ADIS.txt`（IMU 中心；各 ~13.6k 行）、上游 `result/`。窗口 `2021-10-12 07:33:20–08:35:00` GPST（sow 200000–203700），1 Hz，GPS+BDS+GAL，基线 ~9.3→18.4 km。

### 3.1 屏幕（节选；两程序相同的开头）

```text
xconfig: read from file xml/GREAT-GINSFGO-TC-RTKINS-1012-urban_linux.xml
[E] <main> : path is not file (skipped)!             ← 日志文案写反了：路径**是** file:// 时打印，无害
[E] <decode_data> : Not defined frequency code I09   ← NavIC 码，忽略
[W] <_fix_band> : Warning: Changing BDS-3 C7D/C7P/C7Z to C9D/C9P/C9Z in RINEX 3.04
Ceres Solver Report: Iterations: 2, Initial cost: 3.582790e+04, Final cost: 8.362098e+00, Termination: CONVERGENCE
Epoch: 200086.0000000000 time cost (ms): 212.8673680000 iter times: 0
...
Current Epoch:  2021-10-12 08:34:59[GPS] Processing Finished!
Spent1113.994 seconds.
```

### 3.2 结果（2026-09-26 00:56–01:28 EDT）

| 程序 | 墙钟 | 输出 | 行（去表头） | AmbStatus 本机 / 上游 `result/` |
| --- | --- | --- | --- | --- |
| `GREAT_PVTFGO` RTK | **9m27s**（`Spent564.008`；stdout **110 MB/416 万行**） | `result/SEPT-RTK.fgo` 788037 B + `.kml` + cwd `ratio-SEPT` | 3646 | Fixed **3127**/Float 519 · 上游 3190/456 |
| `GREAT_GINSFGO` TC | **18m41s**（`Spent1113.994`；stdout 3.9 MB） | `result/SEPT-RTK-TCI-ADIS-FGO.ins` 914894 B + `.kml` | 3702（MeasType GNSS 3668 / INS 34） | Fixed **3110**/Float 592 · 上游 3318/384 |

`.fgo` 首行（sow 200000）：`NSat=13 PDOP=1.49 Float BL=9280.330 m`；sow 200003 起首次 `Fixed Ratio=2.16`。文件大小与上游一字节不差，但数值不同（见下）。

### 3.3 精度（**本机自算**，对包内 groundtruth，逐秒 3D）

| 解 | 参照 | n | RMS | p50 | p95 | max |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 本机 RTK `.fgo` | GT_GNSS | 3646 | **0.678** | 0.114 | 1.340 | 20.679 |
| 上游 RTK `.fgo` | GT_GNSS | 3646 | 0.659 | 0.108 | 1.408 | 20.667 |
| 本机 RTK 仅 Fixed | GT_GNSS | 3127 | 0.367 | 0.102 | 0.630 | — |
| 本机 TC `.ins`（sow ≤203699） | GT_ADIS | 3700 | **0.414** | 0.108 | 0.993 | 4.137 |
| 上游 TC `.ins`（sow ≤203699） | GT_ADIS | 3700 | 0.318 | 0.096 | 0.708 | 4.275 |
| 本机 TC 仅 Fixed | GT_ADIS | 3110 | 0.305 | 0.096 | 0.411 | — |

- 末 2 历元（203700/203701）GNSS 已结束、纯 INS 外推，本机误差 ~30 m；全 3702 行 RMS 为 0.691 m，统计时去掉。
- 本机 vs 上游逐秒差：RTK p50 **0.014 m**、p95 0.531 m；TC p50 0.029 m。**中位数几乎一致，差异集中在模糊度固定与否的历元**。
- 本机 TC 比上游差，**推测**主因是 `<max_solver_time> 0.08 </max_solver_time>`（Ceres 墙钟上限）：本机单历元 ~200 ms、机器负载高，求解被截断，结果随 CPU 变——**FGO 结果不可逐位复现**（§7 坑 9）。另有 Eigen 3.4 vs 仓内 3.3.5、Ceres 无 SuiteSparse 等差异。
- 比对脚本（自写）：`round(sow,2)` 配对，`.fgo`/`.ins` 第 2–4 列 vs GT 第 3–5 列（GT 第 1 列是 GPS 周）。

## 4. I/O

| 输入（XML `<inputs>`） | 说明 |
| --- | --- |
| `<rinexo>` | 基站 + 流动站；`<gen><base>/<rover>`，基站坐标 `<receiver><rec id X Y Z>` + `<basepos>CFILE` |
| `<rinexn>` | 广播星历即可（RTK 双差）；多系统混合 `BRDC..._MN.rnx` → [data-access](../data-access.md) |
| `<atx>/<blq>/<de>/<eop>` | 模型文件（样例 `model/` 自带） |
| `<imu>` | 仅 GINSFGO；文本 `sow gx gy gz ax ay az`，由 `<ins><DataFormat>` 解释 |

| 输出 | 含义 |
| --- | --- |
| `$(rec)-RTK.fgo` | 19 列：sow、ECEF XYZ、V（RTK 恒 0）、XYZ-RMS、NSat、PDOP、sigma0、AmbStatus、Ratio、BL、Quality（Fixed=1/Float=5/6） |
| `$(rec)-RTK-TCI-ADIS-FGO.ins` | sow、ECEF、速度、Pitch/Roll/Yaw、陀螺/加表零偏、MeasType、Nsat、PDOP、AmbStatus、Ratio |
| `*.kml` | Google Earth |
| cwd `ratio-SEPT` / `<log>` | 每历元 ratio；日志 |

## 5. 关键参数（XML）

| 项 | 作用 |
| --- | --- |
| `<fgo><gnss_window_size>` | RTK 滑窗历元数；样例 **2**；注释称"<50 否则报错" |
| `<fgo><gins_window_size>` | RTK/INS 滑窗；样例 **2** |
| `<fgo><max_solver_time>` / `<max_num_iterations>` | Ceres 墙钟上限（样例 0.08 s）/ 迭代上限（10）——**决定结果与速度** |
| `<fgo><acc_n/acc_w/gyr_n/gyr_w>` | 预积分噪声：加表/陀螺白噪声与零偏随机游走 |
| `<fgo><imu_enable>` / `<gravity_norm>` | 是否用 IMU；重力 9.81 |
| `<fgomsf_sensors><msf_type>` | `GINS_TC`（可用）；`PURE_INS/GNSS/VIL_SLAM/GVIL_*` 列在注释里 |
| `<ins><InitialStates>` | 样例 `Alignment OFF`，**初始位置/速度/姿态直接写死**在 XML |
| `<integration><GNSS Type="TCI">` + `<AntennaLever Type="RFU">` | 紧耦合 + 杆臂（右前上，样例 0.01,-0.273,0.09 m） |
| `<process><obs_combination>` | `RAW_ALL`；`<frequency>2`；`<minimum_elev>10` |
| `<ambiguity>` | `SEARCH`、`part_fix YES`、`ratio 2` |
| `<gen><sat_rm>` | 样例剔 `C01–C05`（BDS GEO） |

## 6. 接到哪步

- 上游：观测 QC → [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)；星历/基站数据 → [data-access](../data-access.md)
- 先用 [great-pvt](./great-pvt.md) 验 RTK 双差/基站坐标，再用本文 `GREAT_PVTFGO`，最后加 IMU 上 `GREAT_GINSFGO`
- 滤波对照：同一数据用 [great-msf](./great-msf.md) `TCRTK` 跑一遍，差值即"滤波 vs 因子图"的实际收益
- ROS/港理工因子图 → [graphgnsslib](./graphgnsslib.md)

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Eigen/Dense: No such file or directory` | CMake 写 `third-party`，目录是 `Third-party` | `-DThird_Eigen_ROOT=/usr/include/eigen3` |
| 2 | apt 装了 `libceres-dev` 仍编不过 `LocalParameterization` | Debian 13 是 Ceres **2.2**，已删该类 | 自编 Ceres **1.14**（或 ≤2.1），`-DThird_ceres_ROOT` |
| 3 | `Killed signal terminated program cc1plus` | Ceres 模板 + `-O3`，`-j8` 内存爆 | `-j3`（本机 3m30s 编完） |
| 4 | `libceres.so.1: cannot open shared object file`，exit 127 | RUNPATH 只含 `${ORIGIN}/../Lib` | `cp libceres.so* <build>_Linux/Lib/` 或设 `LD_LIBRARY_PATH` |
| 5 | `7z x` → `ERROR: Unsupported Method`（17 个） | 样例是 RAR5 v6 方法；Debian `7zip` 去掉了 RAR | `bsdtar -xf`（libarchive-tools） |
| 6 | RTK 第一历元 `std::length_error ... _M_create`，exit 134 | `_set_satdata` 缺 `return`，GCC -O3 UB | 补丁 B：加 `return true;` |
| 7 | 跑完把上游 `result/` 覆盖了 | 输出名与包内参考同名 | 先 `mv result result_upstream` |
| 8 | 路径全找不到 / 结果空 | XML 里 `.\GNSS\...` 反斜杠；路径相对 cwd | `sed 's#\\#/#g'`；在包根目录跑 |
| 9 | 同 XML 两次/两台机器结果不同，固定率低于上游 | `max_solver_time 0.08 s` 是**墙钟**上限，慢机/高负载被截断 | 评精度时调大并记录（本机试 1.0 s：~75 历元/min，1 h 数据约 50 min，未跑完）；别拿单次结果做逐位回归 |
| 10 | RTK 跑 9 分钟、终端刷屏 | 每历元打印残差/雅可比，stdout 110 MB | `> pvt.log 2>&1` 或 `> /dev/null` |
| 11 | `path is not file (skipped)!` 红字 | 日志文案写反，实为正常读 `file://` | 忽略 |
| 12 | 末尾几秒误差几十米 | GNSS 结束后纯 INS 外推（MeasType=INS, Nsat 0） | 统计时按 MeasType 或时段裁掉 |
| 13 | 换自己数据一开始就发散 | `Alignment OFF`，初始 PVA 写死为样例值 | 改 `<InitialStates>` 或开 `POS/VEL` 对准 |
| 14 | `-h` 显示 `G-Nut/PVT [0.9.0]`、`-X` 无 `<fgo>` | 沿用 G-Nut 通用横幅/骨架 | 版本看 git tag；配置抄样例 XML |
| 15 | `-X` 管道得 0 字节 | 写 stderr | `-X 2>&1` |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 因子图 RTK / TC RTK+INS（武大 XML 体系） | **本文 GraphRTK-INS** |
| 滤波版 PPP/RTK + INS（LC/TC，更快，含 PPP） | [great-msf](./great-msf.md) |
| 纯 GNSS PPP/RTK（有 Linux 预编译） | [great-pvt](./great-pvt.md) |
| 因子图 **PPP / TC PPP/INS**（同族；手册待写） | GREAT-PIFGO（`PROJECTS.json` 已收录） |
| ROS 因子图 GNSS | [graphgnsslib](./graphgnsslib.md) |
| 轻量 RTK CLI | [rtklib](./rtklib.md) |

## 9. 相关

[great-msf](./great-msf.md) · [great-pvt](./great-pvt.md) · [great-upd](./great-upd.md) · [great-podflt](./great-podflt.md) · [great-pce](./great-pce.md) · [graphgnsslib](./graphgnsslib.md) · [data-access](../data-access.md) · [README](./README.md)

- 文档：`doc/GraphRTK-INS说明文档 1.0.pdf`（第 4 章只写 Windows cmake-gui；§6.2 列 `.fgo`/`.ins` 列定义）
- 绘图：`plot/plot.py`、`Evaluation.py`、`statistics.py`（本机未跑）；第二样例 `sample_data/FGO_20250928.rar`（未跑）
