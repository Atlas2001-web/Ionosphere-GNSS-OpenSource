# GNSS 数据与格式 / GNSS Data I/O
> 共 **56** 个已收录项目。本文件为链接索引，不含第三方源码。

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


## 基础库(归档)

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTk](https://github.com/SGL-UT/GPSTk) | GPSTk 归档库（请改用 GNSSTK） | C++ | 360 |  |

### 详细说明

#### [GPSTk](https://github.com/SGL-UT/GPSTk)

语言：C++ · 星标约：360

历史 GPSTk 仓库，已声明归档并迁移到 gnsstk / gnsstk-apps。仅作文献与旧脚本对照；新项目请用 GNSSTK。


## RINEX读写

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [georinex](https://github.com/geospace-code/georinex) | 高速 Python RINEX 2/3 NAV/OBS/SP3 读入与 HDF5 转换 | Python | 269 | 🔀 Fork · ★ Star · 核心 |
| [rinex](https://github.com/nav-solutions/rinex) | Rust RINEX 解析/生成与 RINEX-Cli（含 SPP/PPP） | Rust | 126 | 核心 |
| [RinexReader](https://github.com/aaronboda24/RinexReader) | C++ RINEX 2.x/3.x 读取器 | C++ | 38 |  |
| [READ_GNSS](https://github.com/dzd9798/READ_GNSS) | MATLAB 读取多种 GNSS 文件（含 RINEX/IONEX） | MATLAB | 10 |  |
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

#### [READ_GNSS](https://github.com/dzd9798/READ_GNSS)

语言：MATLAB · 星标约：10

在 MATLAB 中读入常见 GNSS 相关文件（含 RINEX、IONEX 等），降低自写解析器的成本，方便后续 TEC 或定位实验。适合已有 MATLAB 工作流的学生课题组。功能广度与健壮性不如 georinex、gnsstk；大型工程或多星座新格式建议仍用专门 IO 库并做交叉校验。遇到新 RINEX 版本时应抽检字段再批量入库。

#### [GNSSNexus-rinex](https://github.com/GNSSNexus/rinex)

语言：Rust · 许可：Apache-2.0

GNSSNexus 下的 RINEX 组件，适合特定工具链内使用。选型时与 georinex、nav-solutions/rinex 比较维护活跃度与格式版本覆盖。


## RINEX/工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsspy](https://github.com/GNSSpy-Project/gnsspy) | Python GNSS 数据工具包 | Python | 209 | ★ Star |

### 详细说明

#### [gnsspy](https://github.com/GNSSpy-Project/gnsspy)  
*★ Star*

语言：Python · 许可：MIT · 星标约：209

面向 GNSS 观测处理的 Python 工具包，读数据、做基础分析较方便。适合教学与中小脚本。功能深度不及 gnsstk/Ginan；精密定位请接专用引擎。


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
| [pyubx2](https://github.com/semuconsulting/pyubx2) | u-blox UBX 协议的 Python 编解码库 | Python | 254 |  |
| [gnsstk](https://github.com/SGL-UT/gnsstk) | 原 GPSTk 演进来的 C++ GNSS 基础库 | C++ | 183 | 核心 |
| [pynmeagps](https://github.com/semuconsulting/pynmeagps) | 解析/生成 NMEA 0183 语句的 Python 库，与 pyubx2 同系 | Python | 106 | 核心 |
| [gnss-protos](https://github.com/nav-solutions/gnss-protos) | GNSS 广播协议编解码的 Rust 库 | Rust | 4 |  |

### 详细说明

#### [pyubx2](https://github.com/semuconsulting/pyubx2)

语言：Python · 许可：BSD-3-Clause · 星标约：254

纯 Python 解析与生成 UBX 消息，覆盖配置、原始观测与导航输出，是连接 F9P 等模块的常用积木。嵌入式上位机、自动化测试与数据记录脚本都会用到。不处理 NMEA/RTCM（见 pygnssutils/pyrtcm），也不做定位滤波；若只要串口读星历伪距，它比完整 GUI 更轻，也比直接啃厂商二进制协议省事。

#### [gnsstk](https://github.com/SGL-UT/gnsstk)  
*核心*

语言：C++ · 星标约：183

德州大学 SGL 的 GNSSTK 库（GPSTk 后继），提供时间系统、坐标、观测模型等底层能力，配套 gnsstk-apps。适合做 C++ 科研软件底座。应用层 PPP/RTK 需自行或接 apps；老文档仍可能写 GPSTk。

#### [pynmeagps](https://github.com/semuconsulting/pynmeagps)  
*核心*

语言：Python · 许可：BSD-3-Clause · 星标约：106

semuconsulting 协议栈中专责 NMEA 0183 解析与生成的 Python 库，常与 PyGPSClient、pyubx2、pyrtcm 组合使用。适合日志解析、测试桩、桌面监控与自动化脚本。不做精密定位解算；字段完整性随接收机方言与专有语句变化，遇到厂商扩展语句时需要自行补充定义再解析。

#### [gnss-protos](https://github.com/nav-solutions/gnss-protos)

语言：Rust · 许可：MPL-2.0 · 星标约：4

集中处理多种 GNSS 广播与传输相关协议编解码的 Rust 库，为 rinex、rtk、ntrip 等 crate 提供底座。适合需要强类型与高性能 IO 的开发者。上层定位/质检算法需另接；协议覆盖范围随版本扩展，集成时建议锁定 crate 版本并跑官方样例报文。


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

语言：— · 星标约：68

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


## RTCM/NTRIP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyGPSClient](https://github.com/semuconsulting/PyGPSClient) | NMEA/UBX/RTCM/NTRIP 等协议的 Python 图形客户端 | Python | 839 | 核心 |
| [ntrip-cpp](https://github.com/ybzwyrcld/ntrip) | NTRIP 2.0 的 C++ caster/client/server 示例 | C++ | 177 |  |
| [pygnssutils](https://github.com/semuconsulting/pygnssutils) | NMEA/UBX/RTCM/NTRIP/SPARTN 的 Python CLI 工具集 | Python | 143 |  |
| [ntripclient](https://github.com/nunojpg/ntripclient) | NTRIP 2.0 命令行客户端 | C | 129 |  |
| [pyrtcm](https://github.com/semuconsulting/pyrtcm) | RTCM3 报文的 Python 解析与生成库 | Python | 115 |  |
| [ntripserver](https://github.com/nunojpg/ntripserver) | NTRIP 2.0 命令行服务端 | C | 74 |  |
| [ntrip-go](https://github.com/go-gnss/ntrip) | Go 语言 NTRIP 客户端与服务端库 | Go | 62 |  |
| [caster](https://github.com/Node-NTRIP/caster) | 支持 NTRIP V1/V2 的 Node.js caster 库 | TypeScript | 52 | 核心 |
| [cors-relay](https://github.com/tisyang/cors-relay) | CORS/NTRIP 差分流中继与重分发 | C | 49 |  |
| [rtcm](https://github.com/Node-NTRIP/rtcm) | RTCM 3 消息编解码（至 3.3） | TypeScript | 48 |  |
| [nmea-msgs](https://github.com/ros-drivers/nmea_msgs) | ROS 包：NMEA 相关消息类型定义 | CMake | 38 |  |
| [rtcm-rs](https://github.com/martinhakansson/rtcm-rs) | RTCM v3 编解码的 Rust crate | Rust | 32 |  |
| [gstream](https://github.com/Jin-Whu/gstream) | 面向 GNSS 的开源数据流客户端库 | C++ | 20 |  |
| [ntripstreams](https://github.com/stenseng/ntripstreams) | Python NTRIP 协议读写接口 | Python | 16 |  |
| [pyspartn](https://github.com/semuconsulting/pyspartn) | 解析 SPARTN 精密改正电文的 Python 库 | Python | 12 |  |
| [ntrip-client](https://github.com/nav-solutions/ntrip-client) | 纯 Rust 的简单 NTRIP 客户端对象 | Rust | 4 |  |
| [BNC](https://igs.bkg.bund.de/ntrip/bnc) | BKG Ntrip Client：多流接收与实时 PPP | C++ | — | 核心 |

### 详细说明

#### [PyGPSClient](https://github.com/semuconsulting/PyGPSClient)  
*核心*

语言：Python · 许可：BSD-3-Clause · 星标约：839

桌面 GUI 同时消化 NMEA、u-blox UBX、SBF、RTCM3、NTRIP 与 SPARTN，便于配置接收机、看星空图与差分链路。适合硬件联调、教学演示与低成本 RTK 调试。它是协议与可视化客户端，不是精密 PPP/RTK 解算引擎；底层解析依赖同作者的 pyubx2、pyrtcm、pygnssutils，深度算法请接 RTKLIB 或科研 PPP。

#### [ntrip-cpp](https://github.com/ybzwyrcld/ntrip)

语言：C++ · 许可：MIT · 星标约：177

提供 NTRIP 2.0 协议下 caster、客户端与服务端示例，星标较高，适合嵌入 C++ 服务或学习握手与挂载点逻辑。二次开发差分转发、教学演示都常见。完整鉴权、集群与监控需自增；Python/Go 生态另有 pygnssutils 与 go-gnss/ntrip，运维桌面场景仍常看 BNC。

#### [pygnssutils](https://github.com/semuconsulting/pygnssutils)

语言：Python · 许可：BSD-3-Clause · 星标约：143

在 pyubx2/pyrtcm 之上提供命令行读写、广播与 NTRIP 客户端/caster 小工具，方便把协议流接到管道或测试架。适合自动化采集、回归测试与协议联调。定位解算、质量评估仍需外接 RTKLIB 或科研引擎；相对 BNC 更偏开发者脚本而非运维级多流平台，和 PyGPSClient 形成 CLI/GUI 互补。

#### [ntripclient](https://github.com/nunojpg/ntripclient)

语言：C · 星标约：129

精简的 NTRIP v2 命令行客户端，适合在嵌入式 Linux 或脚本里拉取差分流，资源占用低。运维与 DIY 基准站、野外测试场景常见。功能止于传输层，不含 GUI 与 PPP；同作者还有 ntripserver、rtcm3torinex，可与 BNC、pygnssutils、cors-relay 按部署形态选型。

#### [pyrtcm](https://github.com/semuconsulting/pyrtcm)

语言：Python · 许可：BSD-3-Clause · 星标约：115

专注 RTCM 3.x 消息编解码，可嵌入 NTRIP 客户端或自研差分链路，便于在 Python 里拆 MSM、站星改正。适合不想拉起完整 BNC 又能看懂差分电文的人。不含 caster 调度与精密定位；与 go-gnss/ntrip、ybzwyrcld/ntrip、nunojpg 系列传输层工具互补，和 pyubx2 同属 semuconsulting 协议栈。

#### [ntripserver](https://github.com/nunojpg/ntripserver)

语言：C · 星标约：74

轻量 NTRIP v2 服务端，把本地串口或数据流发布为挂载点，常与 ntripclient 成对出现。适合单站发布、嵌入式 caster 与实验室联调。高并发、用户管理、TLS 与安全加固不如专用商业或大型开源 caster；大规模转发可看 cors-relay、ybzwyrcld/ntrip 或 BNC。

#### [ntrip-go](https://github.com/go-gnss/ntrip)

语言：Go · 许可：Apache-2.0 · 星标约：62

用 Go 实现 NTRIP 客户端与服务端能力，便于嵌入云原生或高并发转发服务，部署二进制简单。适合想用单一语言栈做差分流网关的人。协议覆盖、挂载点管理与运维工具不如 BNC 成熟；与 ybzwyrcld/ntrip、nunojpg 系列可按语言生态与性能需求选型。生产环境还需自行补齐日志、限流与监控。

#### [caster](https://github.com/Node-NTRIP/caster)  
*核心*

语言：TypeScript · 许可：GPL-3.0 · 星标约：52

用 TypeScript/Node 实现的 NTRIP caster 库，声明支持 V1/V2，便于自建小型网络 RTK 分发服务。适合实验室 CORS 试验与课程演示。高并发、计费鉴权与运维监控不如专用商业方案或 BNC 生态成熟；上线前应做压测、源挂死与证书过期等故障演练。

#### [cors-relay](https://github.com/tisyang/cors-relay)

语言：C · 许可：BSD-3-Clause · 星标约：49

把 CORS 差分数据中继再分发的 C 程序，基于 libev，常见于对接千寻等源并自建内网 caster 的场景。运维本地 RTK 网络、实验室分流时很实用。不是完整商业 caster 套件，账号权限、计费与高可用需自建；可与 ybzwyrcld/ntrip、BNC、ntripserver 对照部署复杂度。

#### [rtcm](https://github.com/Node-NTRIP/rtcm)

语言：TypeScript · 许可：GPL-3.0 · 星标约：48

覆盖至 RTCM 3.3 的消息编解码，JS/TS 生态少见。适合 Web 或 Node 实时应用。GPL；高性能 C++ 嵌入另选其他实现。

#### [nmea-msgs](https://github.com/ros-drivers/nmea_msgs)

语言：CMake · 星标约：38

ros-drivers 维护的 nmea_msgs，定义与 NMEA 标准相关的 ROS 消息，方便驱动、导航与记录节点交换 GNSS 语句。适合 ROS 机器人接入 GNSS 接收机。只提供消息契约，不含语句解析与 PVT；解析与定位需配合 nmea_navsat_driver 等包。消息字段随 ROS 发行版可能微调，编译前核对依赖。

#### [rtcm-rs](https://github.com/martinhakansson/rtcm-rs)

语言：Rust · 许可：Apache-2.0 · 星标约：32

专注 RTCM v3 消息编解码的 Rust crate，便于在服务端或嵌入式旁路处理差分与 SSR 流。适合自建 NTRIP 管道与协议测试。消息类型覆盖随版本增加；与 nav-solutions、pyrtcm 互操作时注意可选字段、端序与厂商扩展。

#### [gstream](https://github.com/Jin-Whu/gstream)

语言：C++ · 许可：MIT · 星标约：20

面向 GNSS 实时试验的开源数据流客户端库，可把 NTRIP、串口等多源观测收成可编程接口。适合自建监听、转发与录包原型。相对 BKG BNC 或商业 caster 客户端，功能面与运维工具更窄；协议边界、断线重连与鉴权要实测，关键链路建议加监控指标与原始流回放。

#### [ntripstreams](https://github.com/stenseng/ntripstreams)

语言：Python · 许可：MIT · 星标约：16

用 Python 与 NTRIP Caster/客户端传 GNSS 流，适合接 RTCM 改正。适合自建流处理原型。完整 PPP 引擎与播发管理需另接 BNC/自研。

#### [pyspartn](https://github.com/semuconsulting/pyspartn)

语言：Python · 许可：BSD-3-Clause · 星标约：12

补齐 SPARTN 精密改正电文解析，方便把 u-blox 等常用 SSR 风格改正接到 NTRIP 或串口流水线。适合低成本 PPP/RTK 改正数试验与协议调试。与 pyrtcm 分工明确：一个管 SPARTN，一个管 RTCM；终端固定效果取决于改正源质量与接收机配置，不能指望解析库单独提高精度。

#### [ntrip-client](https://github.com/nav-solutions/ntrip-client)

语言：Rust · 许可：MPL-2.0 · 星标约：4

纯 Rust 实现的轻量 NTRIP 客户端对象，便于嵌进 nav-solutions 或其他 Rust GNSS 工具链做实时拉流。适合自建差分/SSR 管道原型。功能少于 BNC 与专业运维客户端；TLS、NTRIPv2、挂载点列表与重连策略使用前应读文档，并用断网、鉴权失败等用例做回归。

#### [BNC](https://igs.bkg.bund.de/ntrip/bnc)  
*核心*

语言：C++

BKG 开源多流 NTRIP 客户端，收 RTCM/RINEX 并可做实时 PPP，是 IGS 实时站常见工具。源码与二进制以 BKG/RTCM-Ntrip 站点为准。GUI/部署偏桌面运维，不是现代微服务架构。


## RINEX/SP3

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstools](https://github.com/arthurdjn/gnsstools) | Python 读 RINEX/SP3 与轨道改正工具 | Python | 39 |  |

### 详细说明

#### [gnsstools](https://github.com/arthurdjn/gnsstools)

语言：Python · 许可：MIT · 星标约：39

读 RINEX、SP3 等并做轨道相关处理的小工具集。适合脚本原型。大规模生产建议 georinex + 专业定位引擎。


## Hatanaka/CRX

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [hatanaka](https://github.com/valgur/hatanaka) | Python 调用的 Hatanaka 压缩/解压 | C | 26 |  |
| [crz2rnx](https://github.com/zhufengGNSS/crz2rnx) | Hatanaka RNX2CRX/CRX2RNX 相关程序整理（v4 系） | C | 9 |  |
| [crx2rnx](https://github.com/nav-solutions/crx2rnx) | Rust 实现的 CRX2RNX 命令行工具 | Rust | 8 |  |
| [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html) | 日本地理院 RNXCMP：Hatanaka 压缩官方工具 | C | — | 核心 |

### 详细说明

#### [hatanaka](https://github.com/valgur/hatanaka)

语言：C · 星标约：26

把 Hatanaka（RNXCMP）压缩解压接到 Python，方便批量解 CRX。适合 IGS 数据湖前处理。算法权威来源仍是 GSI RNXCMP；本仓库是便利封装。

#### [crz2rnx](https://github.com/zhufengGNSS/crz2rnx)

语言：C · 星标约：9

整理 Hatanaka 压缩相关的 RNX2CRX/CRX2RNX 程序，方便在无外网环境解压紧凑 RINEX。适合镜像官方 RNXCMP 流程与批量预处理。请核对与国土地理院官方包版本一致性；长期应以官方发布为准，本仓库更适合作为备份或教学拷贝。

#### [crx2rnx](https://github.com/nav-solutions/crx2rnx)

语言：Rust · 许可：MPL-2.0 · 星标约：8

Rust 版 Hatanaka 解压 CLI，便于现代工具链集成。适合不想绑官方 Fortran/C 发行包的场景。与官方 RNXCMP 的比特级兼容性需用样例回归。

#### [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html)  
*核心*

语言：C

RINEX 观测 Hatanaka 压缩/恢复的权威开源工具（CRX/RNX），IGS 数据分发广泛使用。下载与编译以 GSI 页面为准。GitHub 上多为封装；校验请用本官方包。


## 下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GAMPII-GOOD](https://github.com/zhouforme0318/GAMPII-GOOD) | GOOD：GNSS 观测与产品下载器（GAMP II 配套） | C++ | 123 |  |
| [gnss-downloader](https://github.com/Mereithhh/gnss-downloader) | PyQt5 GUI：从 NASA/WHU FTP 下载 GNSS 数据 | Python | 23 |  |
| [GDDS](https://github.com/LECUT/GDDS) | IGS/CORS/产品/时序等多模块 GNSS 下载 | Python | 13 |  |
| [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader) | Embrace 空间天气数据服务 API 的自动下载示例 | Python | 4 |  |

### 详细说明

#### [GAMPII-GOOD](https://github.com/zhouforme0318/GAMPII-GOOD)

语言：C++ · 许可：GPL-3.0 · 星标约：123

面向 GNSS 观测值与精密产品的批量下载工具（GOOD），常与 GAMP/PPP 研究流程一起使用，星标较高。适合搭数据处理流水线的数据准备段。定位解算请接 GAMP_PPPH、PRIDE 或 RTKLIB；镜像源选择与断点续传策略需按网络环境自测，功能定位上可与 FAST 等下载器对照。批量任务建议记录校验和，避免镜像不同步。

#### [gnss-downloader](https://github.com/Mereithhh/gnss-downloader)

语言：Python · 星标约：23

带界面的 GNSS 数据下载器，对接常见 FTP 镜像，降低新手门槛。适合偶发下载。大规模自动化与断点策略不如专用脚本/FAST。

#### [GDDS](https://github.com/LECUT/GDDS)

语言：Python · 星标约：13

分模块下载全球 IGS、后处理产品、区域 CORS、时间序列等，并含解压。适合数据中心助理式抓取。维护活跃度与镜像可用性需自行跟踪。

#### [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader)

语言：Python · 许可：MIT · 星标约：4

演示如何调用 Embrace 空间天气数据服务（SWDS）API 自动下载产品，方便把取数写进科研脚本。适合 GNSS—空间天气交叉研究的数据入口。接口字段、鉴权与限流可能随官方升级变化；时间范围与产品类型以站点文档为准，勿长期硬编码过期端点。


## RINEX转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rtcm3torinex](https://github.com/nunojpg/rtcm3torinex) | 实时把 NTRIP RTCM3 流转成 RINEX | C | 65 |  |
| [prx](https://github.com/jtec/prx) | RINEX 3.05 观测转 CSV | Python | 23 |  |
| [ubx2rinex](https://github.com/nav-solutions/ubx2rinex) | Rust 实现的 u-blox 原始观测到 RINEX 转换/采集工具 | Rust | 12 |  |

### 详细说明

#### [rtcm3torinex](https://github.com/nunojpg/rtcm3torinex)

语言：C · 星标约：65

从 NTRIP 拉取 RTCM3 并实时写成 RINEX，便于把差分流或原始电文沉淀为事后可处理观测文件。野外部署、流归档与应急观测场景实用。转换完整性依赖 RTCM 消息类型与 MSM 配置，复杂多星座细节需实测；可与 BNC、RTKLIB 转换工具及 georinex 后续质检对照。建议对输出 RINEX 做 Anubis 或等价 QC 抽检。

#### [prx](https://github.com/jtec/prx)

语言：Python · 许可：MIT · 星标约：23

把 RINEX 3.05 观测文件转成 CSV，便于表格软件或简单脚本分析。适合快速查看。高精度批处理与多格式支持不如 georinex。

#### [ubx2rinex](https://github.com/nav-solutions/ubx2rinex)

语言：Rust · 许可：MPL-2.0 · 星标约：12

Rust 实现的 u-blox UBX 原始观测反序列化与 RINEX 采集工具，方便把低成本板卡数据送进经典后处理软件。适合外场脚本化采集与自动化。与 android_rinex、georinex 互补；天线高、观测码映射与时钟处理要按接收机配置核对，转换后建议跑质检工具。


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
| [DRCycleSlip](https://github.com/Jin-Whu/DRCycleSlip) | 周跳探测与修复的 Python 实现 | Python | 4 |  |

### 详细说明

#### [cycle-slip-correction](https://github.com/embrace-inpe/cycle-slip-correction)

语言：Python · 许可：MIT · 星标约：14

命令行分析并尝试改正周跳，常用于低纬电离层活跃区数据。适合前处理试验。与定位引擎内置周跳探测策略可能不一致，接入 PPP 前要统一标志。

#### [DRCycleSlip](https://github.com/Jin-Whu/DRCycleSlip)

语言：Python · 星标约：4

提供 GNSS 周跳探测与修复相关 Python 脚本，便于在预处理阶段清理相位观测、服务后续 TEC 或定位。适合教学和小数据试验。算法完备性与多星座鲁棒性有限，生产级 QC 更常见 Anubis 或规则化流水线；可与 embrace-inpe/cycle-slip-correction 对照方法与评价指标。


## 质量检查

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pinot](https://github.com/purpleskyfall/pinot) | “Pinot is not only TEQC”——开源 GNSS 数据质检/预处理取向工具 | Python | 25 | 核心 |
| [RNXQCE](https://github.com/cuizilu/RNXQCE) | RINEX 2/3 质量检查工具包，定位为 TEQC 停更后的替代取向 | Fortran | 6 |  |
| [Anubis](https://gnutsoftware.com/software/anubis) | RINEX 2/3 质量检查（基础版开源） | — | — | 核心 |

### 详细说明

#### [pinot](https://github.com/purpleskyfall/pinot)  
*核心*

语言：Python · 许可：GPL-2.0 · 星标约：25

口号 “Pinot is not only TEQC”，用 Python 做 GNSS 观测质量检查与预处理，意在填补 TEQC 停更后的工具缺口。适合 RINEX 质控、教学与脚本化入库。功能完备度与生态仍不及 Anubis/gfzrnx 组合；切换工具时应用标准站对比指标定义，避免质控阈值误伤。

#### [RNXQCE](https://github.com/cuizilu/RNXQCE)

语言：Fortran · 星标约：6

Fortran 编写的 GNSS 观测预处理与质量检查工具，宣称支持 RINEX 2/3，定位为 TEQC 停更后的替代取向之一。适合测站运维与数据入库前检查。社区体量小于 Anubis；质控指标与历史 TEQC 输出未必逐项相同，切换时要重训阈值阈值。

#### [Anubis](https://gnutsoftware.com/software/anubis)  
*核心*

语言：—

对 RINEX 做完整性、多路径、周跳等质量检查，基础版开源，Pro/实时功能收费。适合数据中心 QC。不是定位引擎；与 teqc 退役后的替代方案常被一并讨论。
