# GREAT-PIFGO · 武大 GREAT 因子图 PPP / PPP+INS 紧耦合 操作手册

目录：[`PROJECTS.json` → `GREAT-PIFGO`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-PIFGO> · 许可：GitHub 未识别（`license: null`），`doc/GREAT-PIFGO说明文档.pdf` §3.2 写 **GPL-3.0** · ★**18** · 默认分支 `master` · tip **`47c8c6e`**（2026-08-07 08:21 EDT；**无 tag**）· 本机：Debian g++ **14.2.0** / CMake **3.31.6** 源码编译（**无 Linux 二进制**；需自编 **Ceres 1.14** + **1 处链接补丁**）· 3 个样例包 PPP-FGO / TC PPP/INS-FGO 全部 **exit 0** · 2026-09-26 01:31–02:10 EDT

> 岗位：**因子图（滑窗 + 边缘化）PPP** 与 **PPP/INS 紧耦合**（IMU 预积分因子 + 无电离层组合伪距/相位因子），Ceres 求解，XML 驱动。姊妹仓：[graphrtk-ins](./graphrtk-ins.md)（因子图 **RTK**）、[great-msf](./great-msf.md)（**滤波** PPP/RTK+INS）。冲突时：**本机 `-h` / `doc/*.pdf` > 本文**。

**质检边界：** 跑了 `FGO_20211012`（PPP-FGO + TC PPP/INS-FGO + 包内同 XML 的滤波 PPP/PPP-INS 对照）、`FGO_20211013`（同上两 FGO）、`FGO_20211128`（PPP-FGO + 滤波 PPP）。全部是**完整窗口**（最长 1 h 数据 8m39s，未截断）。**PPP-AR 未测**（样例全是 `fix_mode NO`，包里无 UPD）。未跑 `plot/*.py`、未测 GLFW 窗口。下文精度数字全是**本机自写脚本**（逐秒 ECEF 差 → 站心 ENU）对**包内 groundtruth** 的比对，**不是**上游公布值；包里附的上游 Windows `result*/` 作第二参照（上游自带 `_statistics.txt` 的 3D RMS 0.349 m 与本机脚本复算一致，脚本口径可信）。

## 1. 用途与边界

**做：**

- `GREAT_PVTFGO`：滑窗因子图 **PPP**（`IONO_FREE` 双频，精密 SP3/CLK，`amb_propagation` 边缘化传递模糊度）
- `GREAT_GINSFGO`：**TC PPP/INS** 因子图（`msf_type GINS_TC`，IMU 预积分 + IF 伪距/相位因子）
- GPS/GAL/BDS-2/3/GLO；自定义 IMU 轴向/单位/噪声；输出 `.fgo`/`.ins`/`.kml`
- 同工程顺带产出 `GREAT_PVT`（滤波 PPP）与 `GREAT_MSF`（滤波 PPP/INS），样例包里有对应 XML，可同数据"滤波 vs 因子图"对照

**不做：**

- **不做 RTK**（双差）→ [graphrtk-ins](./graphrtk-ins.md)；不做 LC 松耦合 FGO
- 样例**全是浮点 PPP**（`fix_mode NO`）。代码里有 PPP-AR 入口（`<inputs><upd>` + `<ambiguity><fix_mode>SEARCH` + `<upd>`），但**需外部 UPD 产品** → [great-upd](./great-upd.md)；本机未验证
- 不产轨道钟差：精密 SP3/CLK 从 [data-access](../data-access.md) 下（样例用 `COD0MGXFIN`）；实时钟差 → [great-pce](./great-pce.md)
- 视觉/LiDAR（`msf_type` 注释列了 `VIL_SLAM/GVIL_*`，本版未开源）
- 上游 README："目前支持在 Windows 下编译运行，Linux 系统需要用户自行编译测试"

| 对照 | [great-msf](./great-msf.md)（滤波） | [graphrtk-ins](./graphrtk-ins.md)（FGO） | **GREAT-PIFGO（FGO）** |
| --- | --- | --- | --- |
| GNSS 模式 | PPP + RTK | 只 RTK | **只 PPP** |
| 观测组合 | IF / RAW | RAW 双差 | **IF 非差** |
| 依赖 | GLFW/GL | + Ceres ≤2.1、glog/gflags | 同 graphrtk-ins |
| Linux 补丁 | 链接 | 链接 + `_set_satdata` 缺 return | **只链接**（`_set_satdata` 上游已修） |
| 本机样例 1 h（FGO_20211012） | TC PPP/INS **41 s**（同包 MSF XML） | TC RTK/INS 18m41s | TC PPP/INS **8m39s** |

## 2. 安装（Linux 源码；本机实测编译 10m26s）

与 [graphrtk-ins](./graphrtk-ins.md) §2 同病同药，下面只写差异与本机真值。

```bash
sudo apt-get install -y build-essential cmake libeigen3-dev libgoogle-glog-dev libgflags-dev \
     libglfw3-dev libopengl-dev libarchive-tools
cd ~/iono_ops && git clone --depth 1 https://github.com/GREAT-WHU/GREAT-PIFGO.git   # 424 MB
# Ceres 1.14 自编 → ~/iono_ops/ceres114（命令见 graphrtk-ins.md 门 1；apt 的 2.2 删了 LocalParameterization）
```

**补丁 A（链接，必须）**：`src/LibGREAT/CMakeLists.txt` Linux `else()` 分支 `link_directories(${ROOT}/build/Lib)` 之后加 4 行（与 graphrtk-ins 逐字相同，`git apply` 直接套上）：

```cmake
	find_package(OpenGL REQUIRED)
	find_library(GLFW_LIB glfw REQUIRED)
	find_library(CERES_LIB ceres HINTS ${Third_ceres_ROOT}/lib REQUIRED NO_DEFAULT_PATH)
	target_link_libraries(${PROJECT_NAME} ${CERES_LIB} glog gflags ${GLFW_LIB} OpenGL::GL)
```

**缺 return 扫描**：本机把根 `CMakeLists.txt` 的 `-w` 换成 `-Wno-all -Wreturn-type` 整仓编一次，只报 **1 处**：

```text
src/LibGREAT/gset/gsetamb.cpp:194:5: warning: control reaches end of non-void function [-Wreturn-type]
```

即 `fixmode2str()` 的 `switch` 覆盖了 `NO/SEARCH` 两个枚举但无兜底 `return`——合法枚举走不到，**未打补丁**，三个样例都没崩。GraphRTK-INS 里致命的 `t_gpvtfgo::_set_satdata` 在本仓**已有 `return updated;`**。

```bash
cd ~/iono_ops/GREAT-PIFGO
cmake -S src -B /tmp/pifgo/build -DCMAKE_BUILD_TYPE=Release \
  -DThird_Eigen_ROOT=/usr/include/eigen3 -DThird_ceres_ROOT=$HOME/iono_ops/ceres114   # 路径大小写：见坑 1
cmake --build /tmp/pifgo/build -j3            # 本机 626 s，exit 0（-j8 会 OOM，见坑 3）
cp -a ~/iono_ops/ceres114/lib/libceres.so* /tmp/pifgo/build_Linux/Lib/
export B=/tmp/pifgo/build_Linux/Bin
```

```text
Bin/GREAT_GINSFGO 586168 B   Bin/GREAT_PVTFGO 577016 B   Bin/GREAT_MSF 575168 B   Bin/GREAT_PVT 579784 B
Lib/libLibGREAT.so 6803048 B   Lib/libLibGnut.so 6792696 B     （RUNPATH ${ORIGIN}/../Lib）
```

```bash
$B/GREAT_PVTFGO -h          # exit 0
```

```text
G-Nut/PVT [0.9.0] compiled: Sep 26 2026 01:42:08 ($Rev: 2448 $)
Usage:
    -h|--help              .. this help
    -V int                 .. version
    -v int                 .. verbosity level
    -x file                .. configuration input file
    --                     .. configuration from stdinp
    -l file                .. spdlog output file
    -X                     .. output default configuration in XML
```

`GREAT_GINSFGO -h` 同款横幅。`-x /nonexist.xml` → exit **1**：`xconfig: not file read /nonexist.xml File was not found`。`-X 2>&1 | grep -c fgo` = **0**（通用 G-Nut 骨架，无 `<fgo>`；抄样例 XML）。

## 3. 端到端（本机真跑）

```bash
mkdir -p ~/iono_ops/pifgo-run && cd ~/iono_ops/pifgo-run
for f in ~/iono_ops/GREAT-PIFGO/sample_data/*; do bsdtar -xf "$f"; done   # 4.2 s / 0.8 s / 3.5 s
cd FGO_20211012/FGO_20211012                   # 注意双层目录
for r in result*; do cp -a "$r" "${r}_upstream"; done            # 先保住上游参考结果（坑 7）
for f in xml/*.xml; do sed 's#\\#/#g' "$f" > "${f%.xml}_linux.xml"; done
env -u DISPLAY $B/GREAT_PVTFGO  -x xml/GREAT-PVTFGO-PPP-1012_linux.xml   > pvtfgo.log  2>&1
env -u DISPLAY $B/GREAT_GINSFGO -x xml/GREAT-GINSFGO-PPPINS-1012_linux.xml > ginsfgo.log 2>&1   # 与上一条别并行（坑 9）
# 滤波对照（同包 XML）：$B/GREAT_PVT -x xml/GREAT-PVT-PPP-1012_linux.xml；$B/GREAT_MSF -x xml/GREAT-MSF-PPPINS-1012_linux.xml
```

样例包（本版是 **7z / zip**，不是 GraphRTK-INS 的 RAR5；Debian `7z t` 也能过）：

| 包 | 内容 | 窗口（GPST） | XML |
| --- | --- | --- | --- |
| `FGO_20211012` | `GNSS/SEPT2850.21O` 137 MB + `COD0MGXFIN` SP3/CLK + BRDC；`IMU/smallimu_out.txt` 1420190 行 100 Hz ADIS16470；`ref/groundtruth_1012_{GNSS,ADIS}.txt`；上游 `resultPPP{FGO,FLT,INSFGO,INSFLT}/` | 10-12 07:33:20–08:35:00（sow 200000–203700），城市车载 | PVTFGO/GINSFGO/PVT/MSF 各 1 |
| `FGO_20211013` | `SEPT2860.21O` 42 MB + `brdm2860.21p` + COD SP3/CLK；IMU 372960 行；`groundtruth/`；上游 4 个 result | 10-13 08:31–09:11 | 同上 |
| `FGO_20211128` | `gnss/` 下观测+SP3/CLK/DCB/ATX/DE405/poleut1；`GT/28/TC_Combined_SmoothedtoAnt1.txt`（IE 8.90 平滑 TC，10 Hz）；**无 IMU、无上游结果文件**（只有 png） | 11-28 08:49–09:13 | 只 PVTFGO/PVT |

### 3.1 屏幕（节选）

```text
xconfig: read from file xml/GREAT-PVTFGO-PPP-1012_linux.xml
[W] <> : warning: not defined upd mode[]                ← 没配 <upd>，浮点 PPP 正常
SEPT: Start GNSS Processing:  2021-10-12 07:33:20[GPS]  2021-10-12 08:35:00[GPS]
###oldest_pos 200000 -2276205.2086 5005525.7581 3220931.0486      ← 滑窗最老历元出窗即输出
 2021-10-12 07:33:21[GPS] Q = 2   0.0%sigma: 0.1086  vtpv: 1.8458
...
 2021-10-12 08:35:00[GPS] Q = 2 100.0%Spent286.1639 seconds.
```

```text
xconfig: read from file xml/GREAT-GINSFGO-PPPINS-1012_linux.xml
gimu:1420190
error: XDG_RUNTIME_DIR is invalid or not set in the environment.     ← GLFW，无头机无害
SEPT: Start GNSS/SINS Integration Processing: 2021-10-12 06:22:12[GPS]  2021-10-12 10:18:55[GPS]
Epoch: 200001 time cost (ms): 302.295 iter times: 0
SEPT outlier (L1) E27 v:            4.984
Current Epoch:  2021-10-12 08:34:59[GPS] Processing Finished!
Spent509.348 seconds.
```

### 3.2 结果（2026-09-26 01:45–02:05 EDT；全部 exit 0）

| 包 · 程序 | 墙钟 | 输出（行，去表头） | 解状态 |
| --- | --- | --- | --- |
| 1012 · `GREAT_PVTFGO` PPP | 4m50s（`Spent286.164`） | `resultPPPFGO/SEPT-PPP.fgo` 712760 B（3672）+ `.kml` | 全 Float |
| 1012 · `GREAT_GINSFGO` TC | 8m39s（`Spent509.348`） | `resultPPPINSFGO/SEPT-PPP-INS-FGO.ins` 914894 B（3702：GNSS 3671 / INS 31）+ `.kml` | 全 Float |
| 1012 · `GREAT_PVT` / `GREAT_MSF`（滤波对照） | 46 s / 51 s | `resultPPPFLT/SEPT-PPP.flt` / `resultPPPINSFLT/SEPT-PPP-INS-FLT.ins` | Float |
| 1013 · `GREAT_PVTFGO` | 3m03s（`Spent181.245`） | `resultPPPFGO/SEPT-PPP.fgo`（2391 对上 GT） | Float |
| 1013 · `GREAT_GINSFGO` | 5m20s（`Spent314.958`） | `resultPPPINSFGO/SEPT-PPP-INS-FGO.ins` 593053 B（2399：GNSS 2387 / INS 12） | Float |
| 1128 · `GREAT_PVTFGO` / `GREAT_PVT` | 2m12s（`Spent129.183`）/ 12 s | `resultPPPFGO/SEPT-PVT.fgo` 278504 B（1441）/ `resultPPPFLT/SEPT-PVT.flt` | Float |

`.fgo` 首行（1012，sow 200000）：`NSat 16  PDOP 1.42  sigma0 0.09  Float  Quality 6`。

### 3.3 精度（**本机自算**，对包内 groundtruth，逐秒，站心 ENU）

| 解 | n | E/N/U RMS | 3D RMS | 3D p50 | 3D p95 | 3D max |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 1012 本机 PPP-FGO | 3671 | 0.694/1.121/5.769 | 5.918 | **0.793** | 2.006 | 347.7 |
| 1012 上游 PPP-FGO | 3671 | 0.682/1.119/5.783 | 5.930 | 0.779 | 2.310 | 347.9 |
| 1012 本机 PPP 滤波（`GREAT_PVT`） | 3671 | 0.788/1.356/6.683 | 6.865 | 1.003 | 2.479 | 402.2 |
| 1012 本机 **TC PPP/INS-FGO**（vs GT_ADIS，MeasType=GNSS） | 3671 | 0.153/0.172/0.263 | **0.349** | 0.197 | 0.646 | 1.634 |
| 1012 本机 TC PPP/INS 滤波（`GREAT_MSF`） | 3668 | 0.160/0.219/0.334 | 0.430 | 0.273 | 0.933 | 1.105 |
| 1013 本机 PPP-FGO | 2391 | 0.734/0.418/1.541 | 1.758 | 0.466 | 1.865 | 59.3 |
| 1013 上游 PPP-FGO | 2391 | 0.736/0.418/1.503 | 1.725 | 0.354 | 1.638 | 59.0 |
| 1013 上游 PPP 滤波 | 2391 | 0.736/0.425/1.560 | 1.777 | 0.686 | 1.667 | 59.1 |
| 1013 本机 **TC PPP/INS-FGO**（vs GT_ADIS） | 2387 | 0.093/0.089/0.308 | **0.334** | 0.219 | 0.636 | 1.632 |
| 1013 上游 TC PPP/INS 滤波 | 2385 | 0.100/0.097/0.373 | 0.399 | 0.283 | 0.713 | 2.145 |
| 1128 本机 PPP-FGO（窗 5） | 1441 | 0.150/0.134/0.933 | **0.955** | 0.772 | 1.765 | 4.012 |
| 1128 本机 PPP 滤波（`GREAT_PVT`） | 1441 | 0.184/0.343/1.162 | 1.225 | 1.089 | 2.089 | 6.471 |

- **TC PPP/INS-FGO 本机与上游 Windows 结果逐秒差 p50 0.0000 m、max 0.002 m（1012、1013 都是）**——可复现；1012 滤波 PPP/INS（`GREAT_MSF`）差 p50 0.021 m。
- **纯 PPP-FGO 与上游不逐位一致**（逐秒差 p50：1012 **0.15 m**、1013 **0.18 m**），统计量基本持平。推测：PPP XML 没写 `<max_solver_time>`，走默认墙钟上限，受 CPU 负载影响（同 graphrtk-ins 坑 9）；本机未单独验证。
- 城市纯 PPP 的 RMS 被少数跳点拉爆（1012 max 347 m），**看 p50/p95**；加 IMU 后 3D RMS 5.9 → 0.35 m。
- 这是 **1 h 以内浮点 PPP**：1012 去掉前 600 s 后 TC PPP/INS-FGO 3D RMS 0.233 m（p95 0.415），仍远不到 PPP-AR/厘米级。
- 比对脚本（自写，`~/iono_ops/pifgo-run/tools/cmp.py`）：`round(sow,2)` 配对；`.fgo`/`.ins` 第 2–4 列 vs GT 第 3–5 列（GT 第 1 列是 GPS 周）；`.ins` 只取 MeasType=GNSS 行并截到 sow ≤ 203699。

## 4. I/O

| 输入（XML `<inputs>`） | 说明 |
| --- | --- |
| `<rinexo>` | 流动站观测（PPP 只要一个站；1012 包里的 `GNSS/Base/WUDA` 基站 PPP 用不到） |
| `<rinexn>` | 广播星历（多系统 `BRDC..._MN.rnx` / `brdm`） |
| `<sp3>` / `<rinexc>` | **精密轨道 / 钟差，PPP 必需**（样例 CODE MGEX FIN 5 min/30 s）→ [data-access](../data-access.md) |
| `<atx>/<blq>/<de>/<eop>` | 天线/海潮/DE405/`poleut1`（1012/1013 在 `model/`，1128 在 `gnss/`） |
| `<imu>` | 仅 GINSFGO；文本 `sow gx gy gz ax ay az`，由 `<ins><DataFormat>` 解释 |
| `<upd>`（可选） | PPP-AR 用 UPD，样例未给 → [great-upd](./great-upd.md) |

| 输出 | 含义 |
| --- | --- |
| `$(rec)-PPP.fgo` | **18 列**：sow、ECEF XYZ、V（PPP 恒 0）、XYZ-RMS、V-RMS、NSat、PDOP、sigma0、AmbStatus、Quality（PDF 表 6.2 写 20 列，第 18/19 列 Ratio/BL，PPP 实际没有，坑 10） |
| `$(rec)-PPP-INS-FGO.ins` | 21 列：sow、ECEF、速度、Pitch/Roll/Yaw、陀螺/加表零偏、MeasType（GNSS/INS）、Nsat、PDOP、AmbStatus、Ratio |
| `*.kml` | Google Earth |
| cwd 副产物 | `GREAT_FGO_FLOAT.txt`（FGO 结果副本，列格式不同）、`ppp_first_epoch_equations.csv`、`<log name>` + `.spd_log`（如 `PPPFGO.spd_log` 4.9 MB） |

## 5. 关键参数（XML）

| 项 | 作用 |
| --- | --- |
| `<fgo><gnss_window_size>` | PPP 滑窗历元数；样例 1012=**2**、1013=**3**、1128=**5**；注释"<50 否则报错" |
| `<fgo><amb_propagation>` | 1=边缘化时传递模糊度先验（默认） |
| `<fgo><gins_window_size>` | PPP/INS 滑窗；样例 **2** |
| `<fgo><max_solver_time>` / `<max_num_iterations>` | Ceres 墙钟上限 / 迭代上限；GINSFGO 样例 **1 s** / 10（GraphRTK-INS 样例是 0.08 s）；PVTFGO 样例不写 |
| `<fgo><acc_n/acc_w/gyr_n/gyr_w>` | 预积分噪声 |
| `<fgomsf_sensors><msf_type>` | `GINS_TC` |
| `<process><obs_combination>` | `IONO_FREE`；`<frequency>2`；`<minimum_elev>7`；`<max_res_norm>` 2–3 |
| `<ambiguity><fix_mode>` | 样例 **`NO`**；`SEARCH` + `<upd>` 才是 PPP-AR |
| `<ins><InitialStates>` | 样例 `Alignment OFF`，初始 PVA **写死**在 XML |
| `<integration><GNSS Type="TCI">` + `<AntennaLever Type="RFU">` | 紧耦合 + 杆臂（1012：0.01,-0.273,0.09 m） |
| `<gen><sat_rm>` | 1012 剔 `C01–C05`（BDS GEO） |

## 6. 接到哪步

- 上游数据：观测 QC → [anubis](./anubis.md)；SP3/CLK/BRDC → [data-access](../data-access.md)
- 想要 PPP-AR：先用 [great-upd](./great-upd.md) 出 WL/NL UPD（或 [gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md) 转 OSB 生态），再在 XML 配 `<upd>` + `fix_mode SEARCH`（本文未验证）
- 自估实时钟差 → [great-pce](./great-pce.md)；实时轨道 → [great-podflt](./great-podflt.md)
- 先用 [great-pvt](./great-pvt.md) 验证 PPP 配置，再上 `GREAT_PVTFGO`，最后加 IMU 上 `GREAT_GINSFGO`
- 滤波对照：同包 `GREAT-MSF-PPPINS-*.xml` 用 [great-msf](./great-msf.md) 跑，差值即因子图收益（1012：3D RMS 0.430 → 0.349 m）
- 有基站要 RTK → [graphrtk-ins](./graphrtk-ins.md)

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Eigen/Dense: No such file or directory` | CMake 写 `third-party`，目录是 `Third-party` | `-DThird_Eigen_ROOT=/usr/include/eigen3 -DThird_ceres_ROOT=…` |
| 2 | `LocalParameterization` 编不过 | apt Ceres **2.2** 已删该类 | 自编 Ceres **1.14** |
| 3 | `Killed signal terminated program cc1plus` | Ceres 模板 + `-O3`，并发高内存爆 | `-j3`（本机 10m26s） |
| 4 | `libceres.so.1: cannot open shared object file` | RUNPATH 只有 `${ORIGIN}/../Lib` | `cp libceres.so* <build>_Linux/Lib/` |
| 5 | **1013 exit 0 但 `resultPPPFGO/` 空**，日志 `Exception opening file ./GNSS/SEPT2860.21o: std::exception`，`Spent0.356 seconds` | XML 写 `.21o`，文件是 `.21O`；Linux 大小写敏感，**找不到观测也返回 0** | `ln -s SEPT2860.21O GNSS/SEPT2860.21o`；跑完先查 `Spent` 秒数和输出行数 |
| 6 | 路径全找不到 | XML 里 `.\GNSS\...` 反斜杠；路径相对 cwd | `sed 's#\\#/#g'`；在**内层**包目录（`FGO_20211012/FGO_20211012`）跑 |
| 7 | 上游 `result*/` 被覆盖 | 输出与包内参考同名同目录 | 先 `cp -a resultX resultX_upstream` |
| 8 | 城市纯 PPP RMS 5.9 m 吓人 | 少数跳点（max 347 m）+ 浮点 1 h 未收敛 | 看 p50/p95；或加 IMU（TC 0.35 m） |
| 9 | `GREAT_FGO_FLOAT.txt` 成了二进制乱码 | PVTFGO 与 GINSFGO 在同一 cwd 并行，**都往 cwd 写这个固定名文件** | 同一目录串行跑，或分目录 |
| 10 | 按 PDF 表 6.2 把 `.fgo` 第 18 列当 Ratio，读到的是 `6` | PPP `.fgo` 实际 **18 列**，第 18 列就是 Quality；PDF 表是 RTK 版（含 Ratio/BL） | 按文件表头取列 |
| 11 | 纯 PPP-FGO 与上游结果逐秒差 ~0.15 m，重跑不逐位一致 | Ceres 墙钟上限，结果随 CPU 负载变（推测） | 回归测试用 TC XML（`max_solver_time 1`，本机与上游差 ≤2 mm）或自己设大上限 |
| 12 | 全程 `Float`，没有 Fixed | 样例 `fix_mode NO`、无 UPD | PPP-AR 需 [great-upd](./great-upd.md) 产品 + `SEARCH` |
| 13 | `.ins` 末尾 31 行 `INS  0  0.00` | GNSS 中断/结束时纯 INS 外推 | 统计按 MeasType 过滤 |
| 14 | 换自己数据一开始就发散 | `Alignment OFF`，初始 PVA 写死为样例值 | 改 `<InitialStates>` 或开 `POS/VEL` 对准 |
| 15 | `XDG_RUNTIME_DIR is invalid`、`path is not file (skipped)!`、`not defined upd mode[]` | GLFW 无头 / 日志文案 / 没配 UPD | 均无害；`env -u DISPLAY` 跑 |
| 16 | tail 日志看着卡住不动 | stdout 被块缓冲，重定向到文件时成批落盘 | 以进程是否在、`Spent` 为准 |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 因子图 **PPP / TC PPP+INS**（无基站，武大 XML） | **本文 GREAT-PIFGO** |
| 因子图 RTK / TC RTK+INS（有基站） | [graphrtk-ins](./graphrtk-ins.md) |
| 滤波 PPP/RTK + INS（LC/TC，快 10×） | [great-msf](./great-msf.md) |
| 纯 GNSS 滤波 PPP/RTK | [great-pvt](./great-pvt.md) |
| PPP-AR 开箱即用（自带产品链） | [pride-pppar](./pride-pppar.md) |
| 产 UPD / 钟差 / 轨道 | [great-upd](./great-upd.md) / [great-pce](./great-pce.md) / [great-podflt](./great-podflt.md) |
| ROS 因子图 GNSS | [graphgnsslib](./graphgnsslib.md) |

## 9. 相关

[graphrtk-ins](./graphrtk-ins.md) · [great-msf](./great-msf.md) · [great-upd](./great-upd.md) · [great-pvt](./great-pvt.md) · [great-pce](./great-pce.md) · [great-podflt](./great-podflt.md) · [gkit-bias](./gkit-bias.md) · [mcosb](./mcosb.md) · [data-access](../data-access.md) · [README](./README.md)

- 文档：`doc/GREAT-PIFGO说明文档.pdf`（§3.2 GPL-3.0；§6.2 列定义；正文称 C++17，CMake 实际 `-std=c++11`）
- 绘图：各包 `plot/*.py`（本机未跑）
