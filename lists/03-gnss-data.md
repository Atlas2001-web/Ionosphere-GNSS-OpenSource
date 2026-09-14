# GNSS 数据与格式 / GNSS Data I/O
> 共 **31** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。

## Android原始观测

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gps-measurement-tools](https://github.com/google/gps-measurement-tools) | Google GNSS Logger 与桌面分析套件 | Java | 841 | 核心 |

### 详细说明

#### [gps-measurement-tools](https://github.com/google/gps-measurement-tools)  
*核心*

语言：Java · 许可：Apache-2.0 · 星标约：841

Android 原始 GNSS 测量日志与桌面可视化分析工具，智能手机高精度研究几乎必用。Logger 官方维护状态有变化，常与 GPSTest 日志互通。不是全星座科研 PPP 引擎。


## RINEX读写

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [georinex](https://github.com/geospace-code/georinex) | 高速 Python RINEX 2/3 NAV/OBS/SP3 读入与 HDF5 转换 | Python | 269 | 🔀 Fork · ★ Star · 核心 |
| [rinex](https://github.com/nav-solutions/rinex) | Rust RINEX 解析/生成与 RINEX-Cli（含 SPP/PPP） | Rust | 126 | 核心 |
| [RinexReader](https://github.com/aaronboda24/RinexReader) | C++ RINEX 2.x/3.x 读取器 | C++ | 38 |  |
| [GNSSNexus-rinex](https://github.com/GNSSNexus/rinex) | RINEX 相关读写/处理组件 | Rust | — |  |

### 详细说明

#### [georinex](https://github.com/geospace-code/georinex)  
*🔀 Fork · ★ Star · 核心*

语言：Python · 许可：MIT · 星标约：269

Python 里最常用的 RINEX 读写库之一，覆盖观测/导航/SP3，可批量转 HDF5，速度接近 C。Atlas2001-web 已 fork。适合数据分析与 TEC/PPP 前处理。写回复杂 RINEX4/RTCM 不是长项；QC 可接 Anubis/rinex-cli。

#### [rinex](https://github.com/nav-solutions/rinex)  
*核心*

语言：Rust · 许可：MPL-2.0 · 星标约：126

GeoRust/nav-solutions 系 RINEX 库，附 RINEX-Cli，可做质检、SPP/PPP、CGGTTS 等，社区常把它比作 teqc/Anubis/gLAB 的开源组合拳。适合要强类型与高性能 IO 的人。学习曲线比 Python 陡；生态仍在演进。

#### [RinexReader](https://github.com/aaronboda24/RinexReader)

语言：C++ · 许可：MIT · 星标约：38

轻量 C++ RINEX 读取，覆盖 GPS/GLONASS/Galileo 等常见情况。适合嵌入自研 C++ 程序。功能广度不及 gnsstk；写文件与 QC 需自补。

#### [GNSSNexus-rinex](https://github.com/GNSSNexus/rinex)

语言：Rust · 许可：Apache-2.0

GNSSNexus 下的 RINEX 组件，适合特定工具链内使用。选型时与 georinex、nav-solutions/rinex 比较维护活跃度与格式版本覆盖。


## 下载/处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [FAST](https://github.com/ChangChuntao/FAST) | GNSS 数据下载、质量分析、SPP 与选站 | Python | 206 | ★ Star · 核心 |

### 详细说明

#### [FAST](https://github.com/ChangChuntao/FAST)  
*★ Star · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：206

模块化 Python 软件：IGS/数据下载、质量分析、单点定位、测站选择等，中文用户多。适合日常数据准备。精密 PPP-AR/科研级 POD 仍需 PRIDE/Ginan 等。


## 基础库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstk](https://github.com/SGL-UT/gnsstk) | 原 GPSTk 演进来的 C++ GNSS 基础库 | C++ | 183 | 核心 |

### 详细说明

#### [gnsstk](https://github.com/SGL-UT/gnsstk)  
*核心*

语言：C++ · 星标约：183

德州大学 SGL 的 GNSSTK 库（GPSTk 后继），提供时间系统、坐标、观测模型等底层能力，配套 gnsstk-apps。适合做 C++ 科研软件底座。应用层 PPP/RTK 需自行或接 apps；老文档仍可能写 GPSTk。


## 多路径/QC

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software) | GNSS 观测多路径分析 Python 软件 | Python | 141 | 核心 |
| [MAPS](https://github.com/GCCLib/MAPS) | MATLAB GNSS 多路径分析软件 | MATLAB | 35 |  |
| [gnss-multipath-detector](https://github.com/EvgeniiMunin/gnss-multipath-detector) | GPS L1 C/A 多路径异常检测模型 | Jupyter Notebook | 28 |  |

### 详细说明

#### [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software)  
*核心*

语言：Python · 许可：MIT · 星标约：141

专门分析 GNSS 观测多路径的开源软件，出图与指标适合论文与天线环境评估。适合选址与天线测试。不替代定位引擎；周跳修复见其他工具。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [MAPS](https://github.com/GCCLib/MAPS)

语言：MATLAB · 星标约：35

MATLAB 下的多路径分析开源实现，方便已有 MATLAB 流水线的实验室。与 paarnes 的 Python 软件可对照指标定义。

#### [gnss-multipath-detector](https://github.com/EvgeniiMunin/gnss-multipath-detector)

语言：Jupyter Notebook · 星标约：28

用数据驱动方法探测 GPS L1 C/A 多路径异常，偏研究 notebook。适合探索 ML+GNSS 质量控。生产嵌入需重做工程化。


## 质量检查

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Anubis](https://gnutsoftware.com/software/anubis) | RINEX 2/3 质量检查（基础版开源） | — | — | 核心 |

### 详细说明

#### [Anubis](https://gnutsoftware.com/software/anubis)  
*核心*

对 RINEX 做完整性、多路径、周跳等质量检查，基础版开源，Pro/实时功能收费。适合数据中心 QC。不是定位引擎；与 teqc 退役后的替代方案常被一并讨论。


## RTCM/NTRIP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BNC](https://igs.bkg.bund.de/ntrip/bnc) | BKG Ntrip Client：多流接收与实时 PPP | C++ | — | 核心 |
| [rtcm](https://github.com/Node-NTRIP/rtcm) | RTCM 3 消息编解码（至 3.3） | TypeScript | 48 |  |
| [nmea-msgs](https://github.com/ros-drivers/nmea_msgs) | ROS 包：NMEA 相关消息类型定义 | CMake | 38 |  |
| [ntripstreams](https://github.com/stenseng/ntripstreams) | Python NTRIP 协议读写接口 | Python | 16 |  |

### 详细说明

#### [BNC](https://igs.bkg.bund.de/ntrip/bnc)  
*核心*

语言：C++

BKG 开源多流 NTRIP 客户端，收 RTCM/RINEX 并可做实时 PPP，是 IGS 实时站常见工具。源码与二进制以 BKG/RTCM-Ntrip 站点为准。GUI/部署偏桌面运维，不是现代微服务架构。

#### [rtcm](https://github.com/Node-NTRIP/rtcm)

语言：TypeScript · 许可：GPL-3.0 · 星标约：48

覆盖至 RTCM 3.3 的消息编解码，JS/TS 生态少见。适合 Web 或 Node 实时应用。GPL；高性能 C++ 嵌入另选其他实现。

#### [nmea-msgs](https://github.com/ros-drivers/nmea_msgs)

语言：CMake · 星标约：38

ros-drivers 维护的 nmea_msgs，定义与 NMEA 标准相关的 ROS 消息，方便驱动、导航与记录节点交换 GNSS 语句。适合 ROS 机器人接入 GNSS 接收机。只提供消息契约，不含语句解析与 PVT；解析与定位需配合 nmea_navsat_driver 等包。消息字段随 ROS 发行版可能微调，编译前核对依赖。

#### [ntripstreams](https://github.com/stenseng/ntripstreams)

语言：Python · 许可：MIT · 星标约：16

用 Python 与 NTRIP Caster/客户端传 GNSS 流，适合接 RTCM 改正。适合自建流处理原型。完整 PPP 引擎与播发管理需另接 BNC/自研。


## Hatanaka/CRX

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html) | 日本地理院 RNXCMP：Hatanaka 压缩官方工具 | C | — | 核心 |
| [hatanaka](https://github.com/valgur/hatanaka) | Python 调用的 Hatanaka 压缩/解压 | C | 26 |  |
| [crx2rnx](https://github.com/nav-solutions/crx2rnx) | Rust 实现的 CRX2RNX 命令行工具 | Rust | 8 |  |

### 详细说明

#### [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html)  
*核心*

语言：C

RINEX 观测 Hatanaka 压缩/恢复的权威开源工具（CRX/RNX），IGS 数据分发广泛使用。下载与编译以 GSI 页面为准。GitHub 上多为封装；校验请用本官方包。

#### [hatanaka](https://github.com/valgur/hatanaka)

语言：C · 星标约：26

把 Hatanaka（RNXCMP）压缩解压接到 Python，方便批量解 CRX。适合 IGS 数据湖前处理。算法权威来源仍是 GSI RNXCMP；本仓库是便利封装。

#### [crx2rnx](https://github.com/nav-solutions/crx2rnx)

语言：Rust · 许可：MPL-2.0 · 星标约：8

Rust 版 Hatanaka 解压 CLI，便于现代工具链集成。适合不想绑官方 Fortran/C 发行包的场景。与官方 RNXCMP 的比特级兼容性需用样例回归。


## 基础库(归档)

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTk](https://github.com/SGL-UT/GPSTk) | GPSTk 归档库（请改用 GNSSTK） | C++ | 360 |  |

### 详细说明

#### [GPSTk](https://github.com/SGL-UT/GPSTk)

语言：C++ · 星标约：360

历史 GPSTk 仓库，已声明归档并迁移到 gnsstk / gnsstk-apps。仅作文献与旧脚本对照；新项目请用 GNSSTK。


## RINEX/工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsspy](https://github.com/GNSSpy-Project/gnsspy) | Python GNSS 数据工具包 | Python | 209 | ★ Star |

### 详细说明

#### [gnsspy](https://github.com/GNSSpy-Project/gnsspy)  
*★ Star*

语言：Python · 许可：MIT · 星标约：209

面向 GNSS 观测处理的 Python 工具包，读数据、做基础分析较方便。适合教学与中小脚本。功能深度不及 gnsstk/Ginan；精密定位请接专用引擎。


## Android/RINEX

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [android_rinex](https://github.com/rokubun/android_rinex) | GnssLogger/GPSTest 日志转 RINEX | Python | 104 |  |
| [BUAA-RINEX-Convertor](https://github.com/Jia-le-wang/BUAA-RINEX-Convertor) | 北航：GnssLogger 文本转 RINEX 3.04 | C++ | 20 |  |

### 详细说明

#### [android_rinex](https://github.com/rokubun/android_rinex)

语言：Python · 许可：BSD-2-Clause · 星标约：104

把 Android GNSS Logger / GPSTest 的 CSV 原始测量转成 RINEX，衔接手机数据与经典 GNSS 软件。适合智能手机 PPP/RTK 实验。手机天线/钟差特性仍须在定位端特殊处理。

#### [BUAA-RINEX-Convertor](https://github.com/Jia-le-wang/BUAA-RINEX-Convertor)

语言：C++ · 星标约：20

将 Google GnssLogger 文本日志转为 RINEX 3.04，面向安卓原始观测科研。可与 android_rinex 对照输出差异。维护与星座覆盖需实测。


## 基础库应用

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstk-apps](https://github.com/SGL-UT/gnsstk-apps) | GNSSTK 配套应用程序集 | — | 68 |  |

### 详细说明

#### [gnsstk-apps](https://github.com/SGL-UT/gnsstk-apps)

星标约：68

从原 GPSTk 拆出的应用程序仓库，提供基于 gnsstk 的命令行工具。适合不想从零写 C++ 调用的用户。与现代 Python 工具链相比部署偏重。


## 自动化处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [geode](https://github.com/demiangomez/geode) | 自动化 GNSS 数据处理与管理框架 | Python | 61 |  |

### 详细说明

#### [geode](https://github.com/demiangomez/geode)

语言：Python · 许可：BSD-3-Clause · 星标约：61

把下载、处理、分析、管理串成 Python 框架，减少手写胶水。适合中等规模台网运维原型。核心估计算法深度取决于所接后端。


## 元数据/SDR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS-Metadata-Standard](https://github.com/IonMetadataWorkingGroup/GNSS-Metadata-Standard) | GNSS 软件接收机元数据标准与工具 | C++ | 59 |  |

### 详细说明

#### [GNSS-Metadata-Standard](https://github.com/IonMetadataWorkingGroup/GNSS-Metadata-Standard)

语言：C++ · 许可：LGPL-3.0 · 星标约：59

定义 SDR/原始采样元数据标准并提供工具，便于交换 IQ 与前端配置。做 GNSS-SDR 或自研接收机时很有用。与 RINEX 观测生态互补而非替代。


## RINEX/SP3

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstools](https://github.com/arthurdjn/gnsstools) | Python 读 RINEX/SP3 与轨道改正工具 | Python | 39 |  |

### 详细说明

#### [gnsstools](https://github.com/arthurdjn/gnsstools)

语言：Python · 许可：MIT · 星标约：39

读 RINEX、SP3 等并做轨道相关处理的小工具集。适合脚本原型。大规模生产建议 georinex + 专业定位引擎。


## 下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-downloader](https://github.com/Mereithhh/gnss-downloader) | PyQt5 GUI：从 NASA/WHU FTP 下载 GNSS 数据 | Python | 23 |  |
| [GDDS](https://github.com/LECUT/GDDS) | IGS/CORS/产品/时序等多模块 GNSS 下载 | Python | 13 |  |

### 详细说明

#### [gnss-downloader](https://github.com/Mereithhh/gnss-downloader)

语言：Python · 星标约：23

带界面的 GNSS 数据下载器，对接常见 FTP 镜像，降低新手门槛。适合偶发下载。大规模自动化与断点策略不如专用脚本/FAST。

#### [GDDS](https://github.com/LECUT/GDDS)

语言：Python · 星标约：13

分模块下载全球 IGS、后处理产品、区域 CORS、时间序列等，并含解压。适合数据中心助理式抓取。维护活跃度与镜像可用性需自行跟踪。


## RINEX转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [prx](https://github.com/jtec/prx) | RINEX 3.05 观测转 CSV | Python | 23 |  |

### 详细说明

#### [prx](https://github.com/jtec/prx)

语言：Python · 许可：MIT · 星标约：23

把 RINEX 3.05 观测文件转成 CSV，便于表格软件或简单脚本分析。适合快速查看。高精度批处理与多格式支持不如 georinex。


## 处理/教学

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gLAB](https://github.com/valgur/gLAB) | gLAB（UPC/ESA）非官方镜像 | C | 22 | ★ Star |

### 详细说明

#### [gLAB](https://github.com/valgur/gLAB)  
*★ Star*

语言：C · 星标约：22

GNSS-Lab Tool 非官方镜像，便于 git 获取；官方发行仍以 UPC/ESA 渠道为准。gLAB 强于观测建模教学与 PPP 实验。商业许可与更新节奏以官方为准。


## 周跳

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cycle-slip-correction](https://github.com/embrace-inpe/cycle-slip-correction) | 周跳分析与改正命令行工具 | Python | 14 |  |

### 详细说明

#### [cycle-slip-correction](https://github.com/embrace-inpe/cycle-slip-correction)

语言：Python · 许可：MIT · 星标约：14

命令行分析并尝试改正周跳，常用于低纬电离层活跃区数据。适合前处理试验。与定位引擎内置周跳探测策略可能不一致，接入 PPP 前要统一标志。
