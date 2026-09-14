# 精密定位 / Precise Positioning
> 共 **58** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

## PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH) | 多星座 PPP 源码（GAMP 相关整理） | — | 78 | 🏷️ 高校实验室 · ★ Star |
| [GPSPACE](https://github.com/CGS-GIS/GPSPACE) | 加拿大 NRCan GPSPACE PPP Fortran 程序 | Fortran | 58 | 🏷️ 个人社区 |
| [PPP](https://github.com/XiaoGongWei/PPP) | 静态 PPP 相关 C++ 实现（MG-APP 作者相关） | C++ | 23 | 🏷️ 高校实验室 |
| [ppp_rtklib](https://github.com/mulin33/ppp_rtklib) | 从 RTKLIB 抽出的独立 PPP 模块，便于精读源码 | C | 4 | 🏷️ 个人社区 |
| [PPPH-UAV](https://github.com/BerkayBahadur/PPPH-UAV) | 面向无人机摄影测量的 GNSS PPP 处理（MATLAB） | MATLAB | 14 | 🏷️ 个人社区 |
| [PPPLib](https://github.com/yxw027/PPPLib) | 精密单点定位库 PPPLib | — | 49 | 🏷️ 高校实验室 |
| [raPPPid](https://github.com/TUW-VieVS/raPPPid) | 维也纳 VieVS 的 PPP 模块 raPPPid | MATLAB | 149 | 🏷️ 个人社区 · 核心 |
| [RTPPP_B2b](https://github.com/floating0516/RTPPP_B2b) | 北斗 PPP-B2b 改正数解码与实时 PPP 接口 | C | 10 | 🏷️ 个人社区 · 核心 |

### 详细说明

#### [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH)  
*🏷️ 高校实验室 · ★ Star*

语言：— · 许可：— · 星标约：78 · 宿主：github

整理/公开的多星座 PPP 相关源码，常被中文社区当作 GAMP 学习材料。适合对照教材读流程。官方维护关系与许可需自行核实，慎直接用于生产。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [GPSPACE](https://github.com/CGS-GIS/GPSPACE)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：58 · 宿主：github

NRCan 公开的 PPP Fortran 代码，历史与官方 CSRS-PPP 服务同源脉络。适合研究官方级 PPP 模型细节。编译与依赖偏传统；日常用户更多用在线 CSRS-PPP。

#### [PPP](https://github.com/XiaoGongWei/PPP)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：23 · 宿主：github

偏静态精密单点定位流程的 C++ 练习/研究代码，作者与 MG-APP 系列相关，便于对照阅读观测方程与参数估计骨架。适合理解 PPP 基本流程。工程完整度、多星座产品与模糊度固定支持有限；生产级 PPP-AR 请优先使用 PRIDE-PPPAR、Ginan 或 MRTKLIB 等更完整套件。

#### [ppp_rtklib](https://github.com/mulin33/ppp_rtklib)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：4 · 宿主：github

从 RTKLIB 源码中抽出 PPP 相关模块做成更小阅读单元，降低在庞大工程里迷路的成本，方便精读观测模型与参数估计。适合源码课与自学。功能范围取决于抽取边界，不保证与完整 RTKLIB 行为一致；修改后应回到官方工程跑回归再谈精度对比。

#### [PPPH-UAV](https://github.com/BerkayBahadur/PPPH-UAV)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：14 · 宿主：github

在 PPPH 思路上处理无人机原始 GNSS，服务摄影测量轨迹与产品生成，MATLAB 实现便于改流程与出图。做 UAV 测图轨迹增强、POS 辅助时可作参考。通用多星座 PPP-AR、模糊度固定与实时能力不如 PRIDE、Ginan；许可未显著标明，使用与再分发前请阅读仓库说明。影像时间戳与 GNSS 历元对齐是摄影测量成败关键。

#### [PPPLib](https://github.com/yxw027/PPPLib)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：49 · 宿主：github

开源 PPP 库，便于阅读 PPP 状态估计与资源管理结构。适合课程设计与二次开发起点。社区体量小于 PRIDE/RTKLIB；功能完整性以实测为准。

#### [raPPPid](https://github.com/TUW-VieVS/raPPPid)  
*🏷️ 个人社区 · 核心*

语言：MATLAB · 许可：GPL-3.0 · 星标约：149 · 宿主：github

VieVS 体系下的精密单点定位模块，MATLAB 实现，适合与 VLBI/大地测量流程结合的课题组。非实时引擎；工业 RTK 请看 RTKLIB/商业机。

#### [RTPPP_B2b](https://github.com/floating0516/RTPPP_B2b)  
*🏷️ 个人社区 · 核心*

语言：C · 许可：— · 星标约：10 · 宿主：github

解码北斗 PPP-B2b 广播的精密轨道钟差改正，带流解析、缓冲与完整性检查，便于接入实时 PPP 流水线。做 BDS-3 短报文 PPP 或接收机原型时应优先阅读。仓库体量小、许可未标明，工程化与多系统融合仍需自补；可与 PRIDE、Ginan、RTKLIB 实时分支对照改正数接口设计。区域服务范围与信号可见性会直接影响改正可用性。

## PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PPP_AR](https://github.com/heiwa0519/PPP_AR) | 多星座 PPP 模糊度固定（PPP-AR）相关实现 | C | 40 | 🏷️ 个人社区 |
| [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR) | 武汉大学 PRIDELab 多星座 PPP 模糊度固定 | C | 415 | 🏷️ 高校实验室 · ★ Star · 核心 |

### 详细说明

#### [PPP_AR](https://github.com/heiwa0519/PPP_AR)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：40 · 宿主：github

围绕多星座 PPP 模糊度固定（PPP-AR）组织的实现，便于对照教材中的宽巷/窄巷与产品依赖关系。适合学习 PPP-AR 流程。工程化程度、实时性与 OSB/UPD 产品格式支持参差不齐；严肃精度评估请交叉验证 PRIDE-PPPAR、Ginan 或 MRTKLIB。

#### [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR)  
*🏷️ 高校实验室 · ★ Star · 核心*

语言：C · 许可：GPL-3.0 · 星标约：415 · 宿主：github

面向多 GNSS 的 PPP-AR 开源软件，科研引用多，模糊度固定与产品接口成熟。适合高精度事后 PPP、地壳形变、气象 ZTD。实时 PPP-RTK 与图形界面非重点；学习曲线陡于 RTKLIB。

## PPP/HAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HASPPP](https://github.com/ZhangRunzhi20/HASPPP) | Galileo HAS 精密单点定位开源实现 | C++ | 44 | 🏷️ 个人社区 |

### 详细说明

#### [HASPPP](https://github.com/ZhangRunzhi20/HASPPP)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：44 · 宿主：github

针对 Galileo High Accuracy Service 的 PPP 开源实现，便于评估 HAS 改正性能。适合欧洲星座 HAS 试验。通用多星座 PPP-AR 请仍看 PRIDE 等。

## PPP/PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MRTKLIB](https://github.com/h-shiono/MRTKLIB) | 面向 PPP/PPP-AR/PPP-RTK（CLAS/MADOCA）的现代 GNSS 定位库 | C | 78 | 🏷️ 高校实验室 · 核心 |
| [mrtklib-docker-ui](https://github.com/h-shiono/mrtklib-docker-ui) | MRTKLIB 的 Docker/Web 界面，方便后处理与实时演示 | TypeScript | 10 | 🏷️ 高校实验室 |
| [pygnsslab](https://github.com/PyGnssLab/pygnsslab) | Python 模块化 RINEX/PPP/PPP-AR 与实时流 | Python | 34 | 🏷️ 个人社区 |
| [Urban-RTKLIB](https://github.com/MayHarryWang/Urban-RTKLIB) | 面向城市导航的 RTKLIB 改版，侧重 PPP/PPP-RTK | C | 25 | 🏷️ 高校实验室 |

### 详细说明

#### [MRTKLIB](https://github.com/h-shiono/MRTKLIB)  
*🏷️ 高校实验室 · 核心*

语言：C · 许可：— · 星标约：78 · 宿主：github

面向 PPP、PPP-AR 与 PPP-RTK（含 CLAS/MADOCA 等区域增强）的现代定位库，比经典 RTKLIB 默认树更贴近亚太 PPP-RTK 场景。适合评估 SSR/CSSR 改正接入与模糊度固定。文档与样例需要时间消化；与 PRIDE、Ginan、Urban-RTKLIB 对照时重点看改正数接口、收敛时间与固定率。上游许可请仔细阅读。

#### [mrtklib-docker-ui](https://github.com/h-shiono/mrtklib-docker-ui)  
*🏷️ 高校实验室*

语言：TypeScript · 许可：MIT · 星标约：10 · 宿主：github

给 MRTKLIB 套一层容器与网页操作，降低命令行门槛，便于课堂或外场演示 PPP/PPP-RTK。适合快速试 CLAS/MADOCA 相关配置与看星空图类状态。解算能力完全取决于背后的 MRTKLIB 版本与改正源；复杂工程参数仍建议回到命令行复现，并把容器镜像 tag 钉死以免漂移。

#### [pygnsslab](https://github.com/PyGnssLab/pygnsslab)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：34 · 宿主：github

纯 Python 方向的模块化工具，含 RINEX、PPP/PPP-AR 与实时流支持，降低 C++ 编译门槛。适合原型与教学。极致性能与完备产品化仍不及 PRIDE/Ginan。

#### [Urban-RTKLIB](https://github.com/MayHarryWang/Urban-RTKLIB)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：25 · 宿主：github

基于 RTKLIB 改造、面向城市峡谷导航的版本，更强调 PPP/PPP-RTK 在遮挡环境下的可用性。适合低成本城市精密定位试验。具体改动需对照上游 diff 与配置文件；与 MRTKLIB、rtklibexplorer 并列评估时，重点看遮挡建模、改正数接口与固定率统计。

## PPP/RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-rtk](https://github.com/nav-solutions/gnss-rtk) | Rust 实现的 PPP/RTK 解算器 | Rust | 79 | 🏷️ 个人社区 |
| [laika](https://github.com/commaai/laika) | comma.ai 的轻量 Python GNSS 处理库 | Python | 723 | 🏷️ 个人社区 · 核心 |

### 详细说明

#### [gnss-rtk](https://github.com/nav-solutions/gnss-rtk)  
*🏷️ 个人社区*

语言：Rust · 许可：AGPL-3.0 · 星标约：79 · 宿主：github

rtk-rs/nav-solutions 系精密定位解算，与 rinex 库同一生态，AGPL。适合 Rust 栈爱好者。生态年轻于 RTKLIB；许可对闭源集成不友好。

#### [laika](https://github.com/commaai/laika)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：MIT · 星标约：723 · 宿主：github

面向自动驾驶与研究的精简 GNSS 库，可下载星历与改正、做伪距定位并与 RTKLIB 风格流程对接，Python 接口干净。适合想快速验证定位链路、而不愿先啃完整测地软件栈的工程师与学生。功能覆盖远小于 PRIDE、Ginan、RTKLIB，模糊度固定与多频多星座产品化能力弱；和 rtklib-py、goGPS 对照时，优势在轻量与可嵌入脚本。

## PPP/改正数

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [B2bLIB](https://github.com/GCCLib/B2bLIB) | 北斗 PPP-B2b 服务研究用的 C/C++ 库 | C | 26 | 🏷️ 个人社区 · 核心 |
| [CSSR-tool](https://github.com/MayHarryWang/CSSR-tool) | 多源协同 CSSR-PPP 改正数预处理工具 | C | 7 | 🏷️ 高校实验室 |
| [ginan](https://github.com/GeoscienceAustralia/ginan) | Geoscience Australia 精密定位与改正数工具包 | C++ | 343 | 🏷️ 官方 · 核心 |
| [NavDecoder](https://github.com/NavSesne/NavDecoder) | 解码 PPP-B2b 与 Galileo HAS 并做校验的工具 | Python | 37 | 🏷️ 个人社区 · 核心 |
| [RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b) | 基于 RTKLIB 的北斗 PPP-B2b 解码与定位工具包 | C | 74 | 🏷️ 高校实验室 · 核心 |

### 详细说明

#### [B2bLIB](https://github.com/GCCLib/B2bLIB)  
*🏷️ 个人社区 · 核心*

语言：C · 许可：— · 星标约：26 · 宿主：github

为北斗 PPP-B2b 服务研究提供的 C/C++ 库，降低从广播电文到改正应用试验的门槛。适合高校北斗 PPP 课题与 ICD 对照。可与 UCAS RTKLIB-B2b、floating0516/RTPPP_B2b、NavDecoder 互补；电文版本升级后需回归，许可未标明时商用应先联系作者。

#### [CSSR-tool](https://github.com/MayHarryWang/CSSR-tool)  
*🏷️ 高校实验室*

语言：C · 许可：GPL-3.0 · 星标约：7 · 宿主：github

面向多源协同 CSSR-PPP 的改正数预处理工具，把区域增强类电文整理成后续引擎可用的形式。适合 PPP-RTK/CSSR 试验的数据准备环节。本身不完成完整定位；电文版本、星座与测站网格定义要按样例核验，再接到 MRTKLIB 或自研解算器。

#### [ginan](https://github.com/GeoscienceAustralia/ginan)  
*🏷️ 官方 · 核心*

语言：C++ · 许可：— · 星标约：343 · 宿主：github

澳大利亚定位项目开源工具包，支撑精密定位与改正数生成，工程化程度高。适合要看现代化 C++ 精密定位与服务化架构的人。编译依赖重；完全复现运营服务还需数据与配置。

#### [NavDecoder](https://github.com/NavSesne/NavDecoder)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：— · 星标约：37 · 宿主：github

同时解码北斗 PPP-B2b 与 Galileo HAS 精密改正并做校验，方便多星座增强产品对比与电文一致性检查。适合 SSR/HAS 电文层研究与教学演示。仓库名拼写特殊但不影响克隆；完整 PPP 解算需另接引擎，本库主责改正数解析。版本升级后应用官方样例回归。

#### [RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b)  
*🏷️ 高校实验室 · 核心*

语言：C · 许可：— · 星标约：74 · 宿主：github

基于 RTKLIB 改造的北斗 PPP-B2b 解码与定位工具包，填补开源社区在 B2b 实操链路上的缺口。适合对照 ICD 评估收敛、精度与可用性。可与 floating0516/RTPPP_B2b、GCCLib/B2bLIB、NavDecoder 并列试验；注意电文版本、接收机原始流格式与许可声明是否满足你的使用场景。

## PPP套件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Ginan-GA-portal](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/about-the-program/analysis-centre-software) | 澳大利亚地球科学署 Ginan 分析中心软件官方介绍页 | C++ | — | 🏷️ 官方 |

### 详细说明

#### [Ginan-GA-portal](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/about-the-program/analysis-centre-software)  
*🏷️ 官方*

语言：C++ · 许可：Apache-2.0 (see GitHub) · 星标约：— · 宿主：official_site

Geoscience Australia 对开源 GNSS 分析中心软件 Ginan 的官方说明，介绍实时改正服务与产品生成角色，并指向 GA GitHub 获取源码。适合了解国家级 PPP/改正链路背景；具体编译、模块划分与许可以 GitHub 仓库 README 为准。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## PPP脚本

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ppp-tools](https://github.com/aewallin/ppp-tools) | 基于 RINEX 的 PPP 脚本工具集 | Python | 121 | 🏷️ 个人社区 |

### 详细说明

#### [ppp-tools](https://github.com/aewallin/ppp-tools)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-2.0 · 星标约：121 · 宿主：github

用脚本把 RINEX 丢给 PPP 引擎并整理结果，常用于时间实验室/钟差相关 PPP。适合自动化胶水道具。核心解算器仍依赖外部程序。

## PVT

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gps_pvt](https://github.com/fenrir-naru/gps_pvt) | Ruby 可控的 GNSS PVT 与多格式解析 | C++ | 6 | 🏷️ 个人社区 |

### 详细说明

#### [gps_pvt](https://github.com/fenrir-naru/gps_pvt)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：6 · 宿主：github

提供可在 Ruby 下控制的 PVT 解算，并解析 RINEX/SP3/ANTEX/UBX。适合自动化脚本爱好者。小众语言生态限制了社区规模。

## PVT/精密定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT) | 武汉大学 GREAT 组精密定位与导航软件 | C++ | 279 | 🏷️ 高校实验室 · ★ Star · 核心 |

### 详细说明

#### [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT)  
*🏷️ 高校实验室 · ★ Star · 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：279 · 宿主：github

GREAT-PVT 覆盖精密 PVT 相关能力，与 GREAT-MSF 等组合导航仓库同源风格。适合跟进武大 GREAT 公开算法。文档/用例完整度因版本而异；与 PRIDE 定位分工不同（更偏导航软件栈）。

## RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK) | AGV 用 GNSS-RTK 路径规划与车载显示（Python） | Python | 3 | 🏷️ 个人社区 |
| [HPRTK](https://github.com/yxw027/HPRTK) | 高精度实时定位相关工程（HPRTK） | C++ | 17 | 🏷️ 高校实验室 |
| [OpenRTK](https://github.com/AndreasArendt/OpenRTK) | 开源精密 GNSS/RTK 软件 | C++ | 23 | 🏷️ 个人社区 |
| [RTK](https://github.com/GYH-WHU/RTK) | GPS/BDS 双系统 RTK（浮点/固定）C++ 教学系统 | C++ | 11 | 🏷️ 高校实验室 |
| [rtkbase](https://github.com/Stefal/rtkbase) | 树莓派等 SBC 上自建 GNSS 基准站与 Web 管理 | Python | 769 | 🏷️ 个人社区 · 核心 |
| [rtklib-py](https://github.com/rtklibexplorer/rtklib-py) | 基于 demo5 的 RTKLIB Python 实现（侧重 PPK） | Python | 244 | 🏷️ 个人社区 |

### 详细说明

#### [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：3 · 宿主：github

面向自动导引车（AGV）的 GNSS-RTK 应用：读取 SimpleRTK 等板卡数据，生成高精度行驶路径、地图标绘、到目标点距离，并设计车载显示界面。适合室外 AGV/机器人导引原型。归类为精密定位而非对流层或 GNSS-IR；RTK 解算深度不及 RTKLIB，强项在路径业务与人机界面集成。改正数链路与板卡配置需按 ArduSimple 等厂商文档准备。

#### [HPRTK](https://github.com/yxw027/HPRTK)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：17 · 宿主：github

围绕高精度实时定位组织的 C++ 工程，可作为网络 RTK 与实时改正链路的结构参考。适合阅读数据流调度、改正数接入与解算线程划分方式。文档完整度与持续维护情况一般；关键精度与固定率请用标准基线网评估，并与 RTKLIB 或商业引擎交叉验证后再写进论文指标。

#### [OpenRTK](https://github.com/AndreasArendt/OpenRTK)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：23 · 宿主：github

小型开源 RTK/精密 GNSS 实现，MIT 许可友好。适合嵌入式或教学裁剪。成熟度与社区小于 RTKLIB。

#### [RTK](https://github.com/GYH-WHU/RTK)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：11 · 宿主：github

实现 GPS/BDS 双系统相对定位，覆盖单点、RTK 浮点解到固定解的基本流程，代码面向教学。适合课堂复现双差观测与模糊度固定。基线长度适应性、周跳探测与多路径抑制相对简化；与 RTKLIB、GraphGNSSLib 对照可读差异，不宜直接当作生产级 RTK 引擎。

#### [rtkbase](https://github.com/Stefal/rtkbase)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：AGPL-3.0 · 星标约：769 · 宿主：github

把 u-blox、Septentrio 等接收机、RTKLIB str2str、NTRIP 与 Web GUI 捆成可部署的基准站方案，适合野外站、农场与 DIY CORS。运维人员与低成本 RTK 爱好者最常用。精度与完好性取决于接收机、天线与网络质量，不是测地级网平差软件；与 BNC、商业 caster 相比更偏单站自建与易用性。

#### [rtklib-py](https://github.com/rtklibexplorer/rtklib-py)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：244 · 宿主：github

把 rtklibexplorer/demo5 思路迁到 Python，当前以事后 PPK 为主，便于阅读算法与改实验脚本。适合不想编译 C 版、又要贴近 RTKLIB 流程的人。实时 RTK、完整 GUI 与全部信号支持仍以 C 版 RTKLIB/explorer 为准；与 laika 相比更贴近经典差分定位公式，和 goGPS_MATLAB 可对照语言栈。

## RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | 经典开源 GNSS 定位包（RTK/PPP 等） | C | 3128 | 🏷️ 个人社区 · ★ Star · 核心 |
| [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB) | 面向低成本接收机优化的 RTKLIB 分支 | C | 971 | 🏷️ 个人社区 · 核心 |

### 详细说明

#### [RTKLIB](https://github.com/tomojitakasu/RTKLIB)  
*🏷️ 个人社区 · ★ Star · 核心*

语言：C · 许可：— · 星标约：3128 · 宿主：github

Takasu 的 RTKLIB 是开源 RTK/PPP 事实标准之一，窗口工具与嵌入式移植极广。适合入门精密定位与低成本接收机。默认版本对部分新信号/PPP-AR 不如专用科研软件；社区常用 rtklibexplorer 分支。

#### [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB)  
*🏷️ 个人社区 · 核心*

语言：C · 许可：— · 星标约：971 · 宿主：github

基于 2.4.3、针对 u-blox 等低成本设备优化的活跃分支，文档与讨论区（博客）丰富。适合手持/无人机 RTK。官方声明无担保，实时关键应用需自测；PPP-AR 科研可并行看 PRIDE/Ginan。

## RTKLIB封装

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MatRTKLIB](https://github.com/taroz/MatRTKLIB) | RTKLIB 的 MATLAB 封装与分析辅助 | MATLAB | 99 | 🏷️ 个人社区 |
| [pyrtklib](https://github.com/IPNL-POLYU/pyrtklib) | 港理工 IPNL 的 RTKLIB Python 绑定，可直接在脚本里调用核心解算 | C | 182 | 🏷️ 高校实验室 · 核心 |
| [pyrtklib_demo5](https://github.com/IPNL-POLYU/pyrtklib_demo5) | 基于 rtklibexplorer demo5 分支的 pyrtklib 变体 | C | 13 | 🏷️ 高校实验室 |

### 详细说明

#### [MatRTKLIB](https://github.com/taroz/MatRTKLIB)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：99 · 宿主：github

在 MATLAB 里调用 RTKLIB 并补齐科研常用分析步骤，降低「C 程序+画图」切换成本。适合已有 RTKLIB 经验的科研人员。性能关键路径仍在 RTKLIB 侧。

#### [pyrtklib](https://github.com/IPNL-POLYU/pyrtklib)  
*🏷️ 高校实验室 · 核心*

语言：C · 许可：MIT · 星标约：182 · 宿主：github

港理工 IPNL 将 RTKLIB C 核心封装为 Python 扩展，便于在科研脚本里直接调用 PPK/RTK/PPP 而不反复改 C 工程。适合算法对比、批量后处理与教学演示。接口覆盖取决于绑定版本；实时流与新信号支持需对照所选 RTKLIB 分支。与 rtklib-py（纯 Python 重写）不同，本库强调调用原生 C 性能。

#### [pyrtklib_demo5](https://github.com/IPNL-POLYU/pyrtklib_demo5)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：13 · 宿主：github

在 pyrtklib 思路上对接 rtklibexplorer/demo5 补丁树，更贴近低成本接收机与社区常用改进。适合已经跟随 demo5 博客流程的用户迁移到 Python 批处理。维护节奏可能与主 pyrtklib 分叉；投产前用同一观测数据交叉比对官方 RTKLIB、demo5 命令行与本绑定输出。

## SPP/RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS-Explorer](https://github.com/brucezhcw/GNSS-Explorer) | 基于 RTKLIB 的 SPP 算法优化探索 | C | 21 | 🏷️ 个人社区 |
| [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library) | 现代 C++20 GNSS 工具包（SPP/RTK/PPP/CLAS） | C++ | 189 | 🏷️ 个人社区 |
| [MobileGNSS-SPP](https://github.com/salmoshu/MobileGNSS-SPP) | 面向智能手机的 EKF 单点定位优化实现 | C | 41 | 🏷️ 高校实验室 |
| [SatellitePosition](https://github.com/LStudioLoren/SatellitePosition) | Python 实现卫星单点定位与 RTK 相对定位的学习项目 | Python | 62 | 🏷️ 个人社区 |
| [SPP_SPV](https://github.com/GYH-WHU/SPP_SPV) | 武大相关 GPS/BDS 单点定位与测速（C++/MATLAB）教学实现 | C++ | 7 | 🏷️ 高校实验室 |

### 详细说明

#### [GNSS-Explorer](https://github.com/brucezhcw/GNSS-Explorer)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：21 · 宿主：github

在 RTKLIB 框架上探索 SPP 算法改进，例如加权模型、粗差探测或选星策略的小改动试验场。适合对照默认配置做消融实验与课程报告。不是独立大型定位套件；若计划回馈社区分支，需注意许可证、代码风格与完整回归测试，避免只报告单一场景上的收益。

#### [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：189 · 宿主：github

C++20 风格的 SPP/RTK/PPP/CLAS 工具包，含 Python 绑定、Docker、ROS2 支持。适合新架构嵌入式/机器人项目。测地学事后高精度产品力需与 PRIDE 等对比评估。

#### [MobileGNSS-SPP](https://github.com/salmoshu/MobileGNSS-SPP)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：41 · 宿主：github

针对智能手机 GNSS 原始测量设计的 EKF 单点定位实现，意在改善消费级轨迹连续性与噪声表现。适合手机导航算法原型与课程项目。精度达不到载波相位 RTK/PPP；天线相位中心、占空比与多路径仍在，可与 android_rinex、PRIDE-GeoDataLogger 采集链衔接做进一步研究。

#### [SatellitePosition](https://github.com/LStudioLoren/SatellitePosition)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：62 · 宿主：github

用 Python 从零实现卫星单点定位与 RTK 相对定位的学习项目，注释与结构偏教学向。适合编程课、导航算法入门与作业模板。数值稳健性、周跳探测与多路径处理不及成熟库；学完概念后应用 RTKLIB 或 goGPS 做精度与固定率对照，避免把作业代码当生产引擎。

#### [SPP_SPV](https://github.com/GYH-WHU/SPP_SPV)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：7 · 宿主：github

基于 C++/MATLAB 的 GPS+BDS 单点定位与测速教学系统，可解码 NovAtel 等接收机输出后完成基本解算。适合本科/研究生课程设计。精度、完备性监测与粗差处理不及 RTKLIB 或商用引擎；科研对比应统一星历钟差产品与误差模型后再引用数值结论。

## 因子图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gtsam_gnss](https://github.com/taroz/gtsam_gnss) | 基于 GTSAM 的 GNSS 因子与 MATLAB 封装 | C++ | 136 | 🏷️ 个人社区 |

### 详细说明

#### [gtsam_gnss](https://github.com/taroz/gtsam_gnss)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：136 · 宿主：github

为 GTSAM 提供 GNSS 因子与 MATLAB 包装，方便在因子图框架里拼伪距/相位/IMU。适合算法研究。完整测地产品链需自配数据与模糊度策略。

## 因子图RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | 因子图优化的 GNSS 定位与 RTK | C | 628 | 🏷️ 个人社区 · 核心 |

### 详细说明

#### [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib)  
*🏷️ 个人社区 · 核心*

语言：C · 许可：— · 星标约：628 · 宿主：github

用因子图做 GNSS 定位/RTK 的开源包，把现代图优化引入经典差分定位。适合研究 FGO+GNSS、城市峡谷鲁棒性。传统基站网 RTK 运维流程不是其主场。

## 城市峡谷

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu) | CUDA 粒子滤波+3D 城市模型的 NLOS 抑制定位 | Python | 83 | 🏷️ 个人社区 |

### 详细说明

#### [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：83 · 宿主：github

用 GPU 粒子滤波和城市三维模型射线追踪抑制 NLOS，面向都市峡谷。适合研究型城市定位。依赖 CUDA 与城市模型数据，不适合无 GPU 的测地事后处理。

## 处理/绘图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyRTKLib](https://github.com/alainmuls/pyRTKLib) | RINEX GPS/Galileo 处理与绘图 | Python | 50 | 🏷️ 个人社区 |

### 详细说明

#### [pyRTKLib](https://github.com/alainmuls/pyRTKLib)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：50 · 宿主：github

Python 下处理/绘制基于 RINEX 的 GPS 与 Galileo 数据，教学演示友好。精密模糊度固定与多星座全产品不如专用 PPP-AR 软件。

## 多GNSS定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MG_APP](https://github.com/XiaoGongWei/MG_APP) | MG-APP 多 GNSS 精密定位应用（论文配套） | C++ | 98 | 🏷️ 高校实验室 |
| [QuadSPP](https://github.com/hdkarimi/QuadSPP) | 多星座标准单点定位（SPP）实现 | C | 14 | 🏷️ 个人社区 |

### 详细说明

#### [MG_APP](https://github.com/XiaoGongWei/MG_APP)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：98 · 宿主：github

与 GPS Solutions 论文配套的多 GNSS 定位软件，便于对照文章复现。适合学术复现。工程支持与持续更新取决于作者精力。

#### [QuadSPP](https://github.com/hdkarimi/QuadSPP)  
*🏷️ 个人社区*

语言：C · 许可：MIT · 星标约：14 · 宿主：github

多星座标准单点定位（SPP）实现，代码结构相对直接，便于核对广播星历、钟差与几何距离等基本模型。适合 SPP 基线实验与教学作业。不含模糊度固定与精密产品深度；进入 PPP/RTK 请换专用库，本仓库用来验证伪距定位链路与粗差剔除策略即可。

## 多功能引擎

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sidereon](https://github.com/neilberkman/sidereon) | Rust 统一引擎：SPP/RTK/PPP + 轨道力学 + 多格式 | Rust | 18 | 🏷️ 个人社区 |

### 详细说明

#### [sidereon](https://github.com/neilberkman/sidereon)  
*🏷️ 个人社区*

语言：Rust · 许可：MIT · 星标约：18 · 宿主：github

一个核心提供 SPP/RTK/PPP、SGP4/会合等与 RINEX/RTCM/SP3/NTRIP 解析，并带多语言绑定。适合想要「单依赖多协议」的新项目。相对经典库验证样本仍在积累，关键应用需交叉比对 RTKLIB/IGS。

## 大地测量/GNSS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnatss](https://github.com/seafloor-geodesy/gnatss) | 海底 GNSS-A 换能器测量社区软件（Python） | Python | 17 | 🏷️ 个人社区 |
| [groops](https://github.com/groops-devs/groops) | 重力场与 GNSS 处理工具包 GROOPS | C++ | 244 | 🏷️ 个人社区 · ★ Star · 核心 |

### 详细说明

#### [gnatss](https://github.com/seafloor-geodesy/gnatss)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：17 · 宿主：github

海床大地测量社区维护的 GNSS-Acoustic（GNSS-A）软件：海面 GNSS 与水声测距联合约束海底换能器/点位，用于海底形变与板块边界监测。面向海洋大地测量课题组。不是陆地 RTK/PPP；依赖船舶、声学与时间同步链路，作业与数据成本远高于陆基站网。社区仓库，版本接口以上游发布说明为准。

#### [groops](https://github.com/groops-devs/groops)  
*🏷️ 个人社区 · ★ Star · 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：244 · 宿主：github

GRAZ 等地学机构风格的工具包，覆盖重力场恢复与 GNSS 处理，适合大地测量联合反演。学习成本高；纯导航 RTK 不是最短路径。

## 定位软件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Net_Diff](https://github.com/YizeZhang/Net_Diff) | GNSS 数据下载、定位解算与结果分析套件 | HTML | 178 | 🏷️ 个人社区 |
| [POSGO](https://github.com/lizhengnss/POSGO) | 开源 GNSS 定位软件 POSGO | C++ | 116 | 🏷️ 个人社区 |

### 详细说明

#### [Net_Diff](https://github.com/YizeZhang/Net_Diff)  
*🏷️ 个人社区*

语言：HTML · 许可：— · 星标约：178 · 宿主：github

张一泽等维护的综合工具，覆盖 GNSS 产品下载、多种定位模式与结果分析，中文资料与用户基础较好。适合教学演示、课程设计与中小规模科研试验。相对 PRIDE-PPPAR、Ginan 等，源码开放形态与工程依赖需按仓库说明核对；大规模业务化 PPP-AR 仍建议对照专用精密引擎。版本更新后注意示例配置与产品路径是否仍兼容。

#### [POSGO](https://github.com/lizhengnss/POSGO)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：116 · 宿主：github

C++ 开源定位软件，中文导航学习社区常见推荐。适合跟 Navigation-Learning 笔记对照源码。功能边界以仓库文档为准，和 PRIDE/Ginan 分工不同。

## 教学/PPP套件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gLAB-Download](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite-links/glab-download) | gLAB 官方下载页：Linux 源码包与 Windows/Cygwin 安装包 | C/Python | — | 🏷️ 高校实验室 |
| [gLAB-UPC](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite) | UPC gAGE 官方 gLAB：ESA 合同支持的 GNSS 处理与教学套件 | C/Python | — | 🏷️ 高校实验室 · 核心 |

### 详细说明

#### [gLAB-Download](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite-links/glab-download)  
*🏷️ 高校实验室*

语言：C/Python · 许可：Apache-2.0 + LGPL-3.0 (GUI) · 星标约：— · 宿主：official_site

UPC gAGE 的 gLAB 发行下载页，列出各版本安装包、校验和与许可说明（GUI LGPL-3，核心/绘图 Apache 2.0）。做教学实验请从此获取而非不明镜像。版本与 Qt/Python 依赖需按说明匹配目标发行版，避免混用旧 GUI 与新核心。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [gLAB-UPC](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite)  
*🏷️ 高校实验室 · 核心*

语言：C/Python · 许可：Apache-2.0 + LGPL-3.0 (GUI) · 星标约：— · 宿主：official_site

加泰罗尼亚理工 gAGE 组发布的 GNSS-Lab Tool，覆盖观测建模、SPP/PPP、电离层与绘图。核心与绘图工具 Apache 2.0，Qt GUI 为 LGPL-3。官方下载含 Linux 源码包与 Windows 安装包；GitHub 上多为非官方镜像。适合教学与算法对照，非业务级实时引擎。

## 相对定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java) | goGPS Java 观测处理库 | Java | 66 | 🏷️ 高校实验室 |

### 详细说明

#### [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java)  
*🏷️ 高校实验室*

语言：Java · 许可：— · 星标约：66 · 宿主：github

goGPS 的 Java 实现，便于嵌进 JVM 应用。功能气质同 MATLAB 版但生态不同。移动端/服务器集成可考虑；算法试验仍有人偏 MATLAB 版。

## 相对定位/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | goGPS MATLAB：低成本 GNSS 增强定位 | MATLAB | 327 | 🏷️ 高校实验室 · ★ Star · 核心 |

### 详细说明

#### [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB)  
*🏷️ 高校实验室 · ★ Star · 核心*

语言：MATLAB · 许可：— · 星标约：327 · 宿主：github

长期发展的 MATLAB GNSS 处理包，相对定位与低成本设备场景见长，教科研友好。适合实验室快速改算法。部署与授权不如 C/C++ 开源引擎；Java 版见 goGPS_Java。

## 解析/分析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py) | Stanford NAV Lab：GNSS 解析、分析与可视化 | Python | 266 | 🏷️ 高校实验室 · 核心 |

### 详细说明

#### [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py)  
*🏷️ 高校实验室 · 核心*

语言：Python · 许可：MIT · 星标约：266 · 宿主：github

模块化解析 Android/原始测量与状态估计结果，可视化强，适合智能手机定位与算法课。不是传统测地 PPP 产品线；与 gps-measurement-tools 数据衔接好。
