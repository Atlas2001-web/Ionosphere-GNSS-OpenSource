# 精密定位 / Precise Positioning
> 共 **30** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

## RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | 经典开源 GNSS 定位包（RTK/PPP 等） | C | 3128 | ★ Star · 核心 |
| [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB) | 面向低成本接收机优化的 RTKLIB 分支 | C | 971 | 核心 |

### 详细说明

#### [RTKLIB](https://github.com/tomojitakasu/RTKLIB)  
*★ Star · 核心*

语言：C · 星标约：3128

Takasu 的 RTKLIB 是开源 RTK/PPP 事实标准之一，窗口工具与嵌入式移植极广。适合入门精密定位与低成本接收机。默认版本对部分新信号/PPP-AR 不如专用科研软件；社区常用 rtklibexplorer 分支。

#### [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB)  
*核心*

语言：C · 星标约：971

基于 2.4.3、针对 u-blox 等低成本设备优化的活跃分支，文档与讨论区（博客）丰富。适合手持/无人机 RTK。官方声明无担保，实时关键应用需自测；PPP-AR 科研可并行看 PRIDE/Ginan。


## 因子图RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | 因子图优化的 GNSS 定位与 RTK | C | 628 | 核心 |

### 详细说明

#### [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib)  
*核心*

语言：C · 星标约：628

用因子图做 GNSS 定位/RTK 的开源包，把现代图优化引入经典差分定位。适合研究 FGO+GNSS、城市峡谷鲁棒性。传统基站网 RTK 运维流程不是其主场。


## PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR) | 武汉大学 PRIDELab 多星座 PPP 模糊度固定 | C | 415 | ★ Star · 核心 |

### 详细说明

#### [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR)  
*★ Star · 核心*

语言：C · 许可：GPL-3.0 · 星标约：415

面向多 GNSS 的 PPP-AR 开源软件，科研引用多，模糊度固定与产品接口成熟。适合高精度事后 PPP、地壳形变、气象 ZTD。实时 PPP-RTK 与图形界面非重点；学习曲线陡于 RTKLIB。


## PPP/改正数

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ginan](https://github.com/GeoscienceAustralia/ginan) | Geoscience Australia 精密定位与改正数工具包 | C++ | 343 | 核心 |

### 详细说明

#### [ginan](https://github.com/GeoscienceAustralia/ginan)  
*核心*

语言：C++ · 星标约：343

澳大利亚定位项目开源工具包，支撑精密定位与改正数生成，工程化程度高。适合要看现代化 C++ 精密定位与服务化架构的人。编译依赖重；完全复现运营服务还需数据与配置。


## 相对定位/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | goGPS MATLAB：低成本 GNSS 增强定位 | MATLAB | 327 | ★ Star · 核心 |

### 详细说明

#### [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB)  
*★ Star · 核心*

语言：MATLAB · 星标约：327

长期发展的 MATLAB GNSS 处理包，相对定位与低成本设备场景见长，教科研友好。适合实验室快速改算法。部署与授权不如 C/C++ 开源引擎；Java 版见 goGPS_Java。


## PVT/精密定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT) | 武汉大学 GREAT 组精密定位与导航软件 | C++ | 279 | ★ Star · 核心 |

### 详细说明

#### [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT)  
*★ Star · 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：279

GREAT-PVT 覆盖精密 PVT 相关能力，与 GREAT-MSF 等组合导航仓库同源风格。适合跟进武大 GREAT 公开算法。文档/用例完整度因版本而异；与 PRIDE 定位分工不同（更偏导航软件栈）。


## 解析/分析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py) | Stanford NAV Lab：GNSS 解析、分析与可视化 | Python | 266 | 核心 |

### 详细说明

#### [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py)  
*核心*

语言：Python · 许可：MIT · 星标约：266

模块化解析 Android/原始测量与状态估计结果，可视化强，适合智能手机定位与算法课。不是传统测地 PPP 产品线；与 gps-measurement-tools 数据衔接好。


## 大地测量/GNSS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [groops](https://github.com/groops-devs/groops) | 重力场与 GNSS 处理工具包 GROOPS | C++ | 244 | ★ Star · 核心 |
| [gnatss](https://github.com/seafloor-geodesy/gnatss) | 海底 GNSS-A 换能器测量社区软件（Python） | Python | 17 |  |

### 详细说明

#### [groops](https://github.com/groops-devs/groops)  
*★ Star · 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：244

GRAZ 等地学机构风格的工具包，覆盖重力场恢复与 GNSS 处理，适合大地测量联合反演。学习成本高；纯导航 RTK 不是最短路径。

#### [gnatss](https://github.com/seafloor-geodesy/gnatss)

语言：Python · 星标约：17

海床大地测量社区维护的 GNSS-Acoustic（GNSS-A）软件：海面 GNSS 与水声测距联合约束海底换能器/点位，用于海底形变与板块边界监测。面向海洋大地测量课题组。不是陆地 RTK/PPP；依赖船舶、声学与时间同步链路，作业与数据成本远高于陆基站网。社区仓库，版本接口以上游发布说明为准。


## PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [raPPPid](https://github.com/TUW-VieVS/raPPPid) | 维也纳 VieVS 的 PPP 模块 raPPPid | MATLAB | 149 | 核心 |
| [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH) | 多星座 PPP 源码（GAMP 相关整理） | — | 78 | ★ Star |
| [GPSPACE](https://github.com/CGS-GIS/GPSPACE) | 加拿大 NRCan GPSPACE PPP Fortran 程序 | Fortran | 58 |  |
| [PPPLib](https://github.com/yxw027/PPPLib) | 精密单点定位库 PPPLib | — | 49 |  |

### 详细说明

#### [raPPPid](https://github.com/TUW-VieVS/raPPPid)  
*核心*

语言：MATLAB · 许可：GPL-3.0 · 星标约：149

VieVS 体系下的精密单点定位模块，MATLAB 实现，适合与 VLBI/大地测量流程结合的课题组。非实时引擎；工业 RTK 请看 RTKLIB/商业机。

#### [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH)  
*★ Star*

星标约：78

整理/公开的多星座 PPP 相关源码，常被中文社区当作 GAMP 学习材料。适合对照教材读流程。官方维护关系与许可需自行核实，慎直接用于生产。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [GPSPACE](https://github.com/CGS-GIS/GPSPACE)

语言：Fortran · 星标约：58

NRCan 公开的 PPP Fortran 代码，历史与官方 CSRS-PPP 服务同源脉络。适合研究官方级 PPP 模型细节。编译与依赖偏传统；日常用户更多用在线 CSRS-PPP。

#### [PPPLib](https://github.com/yxw027/PPPLib)

星标约：49

开源 PPP 库，便于阅读 PPP 状态估计与资源管理结构。适合课程设计与二次开发起点。社区体量小于 PRIDE/RTKLIB；功能完整性以实测为准。


## SPP/RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library) | 现代 C++20 GNSS 工具包（SPP/RTK/PPP/CLAS） | C++ | 189 |  |

### 详细说明

#### [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library)

语言：C++ · 许可：MIT · 星标约：189

C++20 风格的 SPP/RTK/PPP/CLAS 工具包，含 Python 绑定、Docker、ROS2 支持。适合新架构嵌入式/机器人项目。测地学事后高精度产品力需与 PRIDE 等对比评估。


## 因子图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gtsam_gnss](https://github.com/taroz/gtsam_gnss) | 基于 GTSAM 的 GNSS 因子与 MATLAB 封装 | C++ | 136 |  |

### 详细说明

#### [gtsam_gnss](https://github.com/taroz/gtsam_gnss)

语言：C++ · 许可：MIT · 星标约：136

为 GTSAM 提供 GNSS 因子与 MATLAB 包装，方便在因子图框架里拼伪距/相位/IMU。适合算法研究。完整测地产品链需自配数据与模糊度策略。


## PPP脚本

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ppp-tools](https://github.com/aewallin/ppp-tools) | 基于 RINEX 的 PPP 脚本工具集 | Python | 121 |  |

### 详细说明

#### [ppp-tools](https://github.com/aewallin/ppp-tools)

语言：Python · 许可：GPL-2.0 · 星标约：121

用脚本把 RINEX 丢给 PPP 引擎并整理结果，常用于时间实验室/钟差相关 PPP。适合自动化胶水道具。核心解算器仍依赖外部程序。


## 定位软件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [POSGO](https://github.com/lizhengnss/POSGO) | 开源 GNSS 定位软件 POSGO | C++ | 116 |  |

### 详细说明

#### [POSGO](https://github.com/lizhengnss/POSGO)

语言：C++ · 许可：GPL-3.0 · 星标约：116

C++ 开源定位软件，中文导航学习社区常见推荐。适合跟 Navigation-Learning 笔记对照源码。功能边界以仓库文档为准，和 PRIDE/Ginan 分工不同。


## RTKLIB封装

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MatRTKLIB](https://github.com/taroz/MatRTKLIB) | RTKLIB 的 MATLAB 封装与分析辅助 | MATLAB | 99 |  |

### 详细说明

#### [MatRTKLIB](https://github.com/taroz/MatRTKLIB)

语言：MATLAB · 许可：MIT · 星标约：99

在 MATLAB 里调用 RTKLIB 并补齐科研常用分析步骤，降低「C 程序+画图」切换成本。适合已有 RTKLIB 经验的科研人员。性能关键路径仍在 RTKLIB 侧。


## 多GNSS定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MG_APP](https://github.com/XiaoGongWei/MG_APP) | MG-APP 多 GNSS 精密定位应用（论文配套） | C++ | 98 |  |

### 详细说明

#### [MG_APP](https://github.com/XiaoGongWei/MG_APP)

语言：C++ · 星标约：98

与 GPS Solutions 论文配套的多 GNSS 定位软件，便于对照文章复现。适合学术复现。工程支持与持续更新取决于作者精力。


## 城市峡谷

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu) | CUDA 粒子滤波+3D 城市模型的 NLOS 抑制定位 | Python | 83 |  |

### 详细说明

#### [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu)

语言：Python · 许可：Apache-2.0 · 星标约：83

用 GPU 粒子滤波和城市三维模型射线追踪抑制 NLOS，面向都市峡谷。适合研究型城市定位。依赖 CUDA 与城市模型数据，不适合无 GPU 的测地事后处理。


## PPP/RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-rtk](https://github.com/nav-solutions/gnss-rtk) | Rust 实现的 PPP/RTK 解算器 | Rust | 79 |  |

### 详细说明

#### [gnss-rtk](https://github.com/nav-solutions/gnss-rtk)

语言：Rust · 许可：AGPL-3.0 · 星标约：79

rtk-rs/nav-solutions 系精密定位解算，与 rinex 库同一生态，AGPL。适合 Rust 栈爱好者。生态年轻于 RTKLIB；许可对闭源集成不友好。


## 相对定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java) | goGPS Java 观测处理库 | Java | 66 |  |

### 详细说明

#### [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java)

语言：Java · 星标约：66

goGPS 的 Java 实现，便于嵌进 JVM 应用。功能气质同 MATLAB 版但生态不同。移动端/服务器集成可考虑；算法试验仍有人偏 MATLAB 版。


## 处理/绘图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyRTKLib](https://github.com/alainmuls/pyRTKLib) | RINEX GPS/Galileo 处理与绘图 | Python | 50 |  |

### 详细说明

#### [pyRTKLib](https://github.com/alainmuls/pyRTKLib)

语言：Python · 星标约：50

Python 下处理/绘制基于 RINEX 的 GPS 与 Galileo 数据，教学演示友好。精密模糊度固定与多星座全产品不如专用 PPP-AR 软件。


## PPP/HAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HASPPP](https://github.com/ZhangRunzhi20/HASPPP) | Galileo HAS 精密单点定位开源实现 | C++ | 44 |  |

### 详细说明

#### [HASPPP](https://github.com/ZhangRunzhi20/HASPPP)

语言：C++ · 许可：GPL-3.0 · 星标约：44

针对 Galileo High Accuracy Service 的 PPP 开源实现，便于评估 HAS 改正性能。适合欧洲星座 HAS 试验。通用多星座 PPP-AR 请仍看 PRIDE 等。


## PPP/PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pygnsslab](https://github.com/PyGnssLab/pygnsslab) | Python 模块化 RINEX/PPP/PPP-AR 与实时流 | Python | 34 |  |

### 详细说明

#### [pygnsslab](https://github.com/PyGnssLab/pygnsslab)

语言：Python · 许可：MIT · 星标约：34

纯 Python 方向的模块化工具，含 RINEX、PPP/PPP-AR 与实时流支持，降低 C++ 编译门槛。适合原型与教学。极致性能与完备产品化仍不及 PRIDE/Ginan。


## RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [OpenRTK](https://github.com/AndreasArendt/OpenRTK) | 开源精密 GNSS/RTK 软件 | C++ | 23 |  |
| [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK) | AGV 用 GNSS-RTK 路径规划与车载显示（Python） | Python | 3 |  |

### 详细说明

#### [OpenRTK](https://github.com/AndreasArendt/OpenRTK)

语言：C++ · 许可：MIT · 星标约：23

小型开源 RTK/精密 GNSS 实现，MIT 许可友好。适合嵌入式或教学裁剪。成熟度与社区小于 RTKLIB。

#### [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK)

语言：Python · 星标约：3

面向自动导引车（AGV）的 GNSS-RTK 应用：读取 SimpleRTK 等板卡数据，生成高精度行驶路径、地图标绘、到目标点距离，并设计车载显示界面。适合室外 AGV/机器人导引原型。归类为精密定位而非对流层或 GNSS-IR；RTK 解算深度不及 RTKLIB，强项在路径业务与人机界面集成。改正数链路与板卡配置需按 ArduSimple 等厂商文档准备。


## 多功能引擎

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sidereon](https://github.com/neilberkman/sidereon) | Rust 统一引擎：SPP/RTK/PPP + 轨道力学 + 多格式 | Rust | 18 |  |

### 详细说明

#### [sidereon](https://github.com/neilberkman/sidereon)

语言：Rust · 许可：MIT · 星标约：18

一个核心提供 SPP/RTK/PPP、SGP4/会合等与 RINEX/RTCM/SP3/NTRIP 解析，并带多语言绑定。适合想要「单依赖多协议」的新项目。相对经典库验证样本仍在积累，关键应用需交叉比对 RTKLIB/IGS。


## PVT

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gps_pvt](https://github.com/fenrir-naru/gps_pvt) | Ruby 可控的 GNSS PVT 与多格式解析 | C++ | 6 |  |

### 详细说明

#### [gps_pvt](https://github.com/fenrir-naru/gps_pvt)

语言：C++ · 星标约：6

提供可在 Ruby 下控制的 PVT 解算，并解析 RINEX/SP3/ANTEX/UBX。适合自动化脚本爱好者。小众语言生态限制了社区规模。
