# 精密定位 / Precise Positioning
> **103** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

## 多星座PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [APAS-TR](https://github.com/Birinci-S/APAS_TR) | APAS-TR：土耳其高校 MATLAB 多星座 PPP | MATLAB | 19 | 🏷️ 高校实验室 |

### 详细说明

#### [APAS-TR](https://github.com/Birinci-S/APAS_TR)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：GPL-3.0 · 星标约：19 · 宿主：github

Automatic PPP Analysis Software-Türkiye（APAS-TR）处理 GPS/GLONASS/Galileo/BDS/QZSS，提供统计图与分析选项。论文强调地磁暴期用 ROTI 自适应门限降低周跳误判，并在 IGS MGEX 测站上验证多星座收敛。适合教学与电离层扰动场景的 PPP 方法复现；需 MATLAB 环境，非实时引擎。

## PPP/改正数

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ginan](https://github.com/GeoscienceAustralia/ginan) | ginan：精密定位与改正数工具包 | C++ | 343 | 🏷️ 官方 核心 |
| [RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b) | RTKLIB-B2b：北斗 PPP-B2b 解码定位包 | C | 74 | 🏷️ 高校实验室 核心 |
| [PPP-BayesTree](https://github.com/wvu-navLab/PPP-BayesTree) | PPP-BayesTree：增量图优化 PPP 收敛研究代码 | C++ | 57 | 🏷️ 高校实验室 |
| [Virtual-Network-DGNSS](https://github.com/Azurehappen/Virtual-Network-DGNSS-Project) | VN-DGNSS：PPP/SSR 驱动的开源虚拟基站差分 | C++ | 39 | 🏷️ 高校实验室 |
| [NavDecoder](https://github.com/NavSesne/NavDecoder) | NavDecoder：PPP-B2b 与 HAS 电文解码 | Python | 37 | 🏷️ 个人社区 核心 |
| [B2bLIB](https://github.com/GCCLib/B2bLIB) | B2bLIB：北斗 PPP-B2b C/C++ 解码库 | C | 26 | 🏷️ 高校实验室 核心 |
| [CSSR-tool](https://github.com/MayHarryWang/CSSR-tool) | CSSR-tool：多源协同 CSSR-PPP 改正数预处理 | C | 7 | 🏷️ 高校实验室 |
| [GipsyX-JPL](https://gipsy-oasis.jpl.nasa.gov/) | JPL GipsyX：授权精密定位软件与产品门户 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [ginan](https://github.com/GeoscienceAustralia/ginan)  
*🏷️ 官方 核心*

语言：C++ · 许可：— · 星标约：343 · 宿主：github

澳大利亚定位项目开源工具包，支撑精密定位与改正数生成，工程化程度高。适合要看现代化 C++ 精密定位与服务化架构的人。编译依赖重；完全复现运营服务还需数据与配置。

#### [RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b)  
*🏷️ 高校实验室 核心*

语言：C · 许可：— · 星标约：74 · 宿主：github

基于 RTKLIB 改造的北斗 PPP-B2b 解码与定位工具包，填补开源社区在 B2b 实操链路上的缺口。适合对照 ICD 评估收敛、精度与可用性。可与 floating0516/RTPPP_B2b、GCCLib/B2bLIB、NavDecoder 并列试验；注意电文版本、接收机原始流格式与许可声明是否满足你的使用场景。

#### [PPP-BayesTree](https://github.com/wvu-navLab/PPP-BayesTree)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：57 · 宿主：github

西弗吉尼亚大学导航实验室公开的 PPP 与增量图优化实验代码，对应论文中关于精密单点定位收敛性的评估设置。MIT 许可，偏研究复现而非开箱即用工程套件；依赖与数据路径见仓库说明。适合因子图/滑窗 PPP 方法对照，生产环境请另选 Ginan、PRIDE、raPPPid 等成熟链。

#### [Virtual-Network-DGNSS](https://github.com/Azurehappen/Virtual-Network-DGNSS-Project)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：39 · 宿主：github

加州大学河滨分校相关团队开源的虚拟网络差分 GNSS：服务端消费 SSR，向客户端输出虚拟参考站 RTCM OSR（GPS L1/BDS B1/Galileo E1），免建物理基站。面向车道级/车辆定位研究。依赖实时 SSR 源与 Ubuntu 构建；不是传统 CORS 网。GPL-3.0。

#### [NavDecoder](https://github.com/NavSesne/NavDecoder)  
*🏷️ 个人社区 核心*

语言：Python · 许可：— · 星标约：37 · 宿主：github

同时解码北斗 PPP-B2b 与 Galileo HAS 精密改正并做校验，方便多星座增强产品对比与电文一致性检查。适合 SSR/HAS 电文层研究与教学演示。仓库名拼写特殊但不影响克隆；完整 PPP 解算需另接引擎，本库主责改正数解析。版本升级后应用官方样例回归。

#### [B2bLIB](https://github.com/GCCLib/B2bLIB)  
*🏷️ 高校实验室 核心*

语言：C · 许可：— · 星标约：26 · 宿主：github

为北斗 PPP-B2b 服务研究提供的 C/C++ 库，降低从广播电文到改正应用试验的门槛。适合高校北斗 PPP 课题与 ICD 对照。可与 UCAS RTKLIB-B2b、floating0516/RTPPP_B2b、NavDecoder 互补；电文版本升级后需回归，许可未标明时商用应先联系作者。

#### [CSSR-tool](https://github.com/MayHarryWang/CSSR-tool)  
*🏷️ 高校实验室*

语言：C · 许可：GPL-3.0 · 星标约：7 · 宿主：github

面向多源协同 CSSR-PPP 的改正数预处理工具，把区域增强类电文整理成后续引擎可用的形式。适合 PPP-RTK/CSSR 试验的数据准备环节。本身不完成完整定位；电文版本、星座与测站网格定义要按样例核验，再接到 MRTKLIB 或自研解算器。

#### [GipsyX-JPL](https://gipsy-oasis.jpl.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

JPL Near Earth Tracking 维护的 GipsyX 门户，提供软件发行说明、轨道钟差与 PPP 产品、论坛与文档入口。软件面向获授权科研/教育用户下载，非纯 OSI 开源；产品与公告对 PPP 社区仍有高频参考价值。许可与账号以站内 download area 为准，勿与完全开源套件混用条款。

## QZSS CLAS PPP-RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CLASLIB](https://github.com/QZSS-Strategy-Office/claslib) | CLASLIB：QZSS CLAS 厘米级增强库 | C | 56 | 🏷️ 官方 核心 |

### 详细说明

#### [CLASLIB](https://github.com/QZSS-Strategy-Office/claslib)  
*🏷️ 官方 核心*

语言：C · 许可：see upstream (derived RTKLIB/GSILIB) · 星标约：56 · 宿主：github

CLAS 测试库解码 Compact SSR（RTCM MT4073），提供 SSR2OSR、SSR2OBS 与事后 RNX2RTKP 等 PPP-RTK/VRS 工具链。源自 RTKLIB 与 GSILIB，由准天顶卫星系统战略室维护。适合日本境内厘米级增强服务研究与消息转换；部署前须阅读各版本内容差异与官方可靠性免责。

## PPP/PPP-RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cssrlib](https://github.com/hirokawa/cssrlib) | cssrlib：Python PPP/PPP-RTK 工具包 | Jupyter Notebook | 211 | 🏷️ 高校实验室 核心 |
| [PPP-RTK-Beechan](https://github.com/MichaelBeechan/PPP-RTK) | PPP-RTK（Beechan）：C 版 SPP/RTD/PPP/RTK/PPP-RTK | C | 26 | 🏷️ 个人社区 |
| [Easy4PTK](https://github.com/alxanderjiang/Easy4PTK) | Easy4PTK：易移植多星座 PPP-RTK Python/Jupyter 试验箱 | Jupyter Notebook | 5 | 🏷️ 个人社区 |

### 详细说明

#### [cssrlib](https://github.com/hirokawa/cssrlib)  
*🏷️ 高校实验室 核心*

语言：Jupyter Notebook · 许可：MIT · 星标约：211 · 宿主：github

基于 RTKLIB 思路的 Python 工具包，解码 Compact SSR、RTCM/IGS SSR 等，对接 QZSS CLAS、Galileo HAS、北斗 PPP 与 IGS 服务做 PPP/PPP-RTK/RTK 教学与试验。附 Colab 教程，适合快速理解开放增强服务。实时生产与完好性需自测；与 MADOCALIB/CLASLIB/MRTKLIB 的 C 实现对照选型。

#### [PPP-RTK-Beechan](https://github.com/MichaelBeechan/PPP-RTK)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：26 · 宿主：github

汇总 SPP、RTD、PPP、RTK、PPP-RTK 及 RAIM/ARAIM 等模块的 C 试验工程，便于对照教材读差分、精密定位与完好性流程。适合算法学习与课堂演示。文档与维护节奏需自查；生产部署请优先 PRIDE、Ginan、MRTKLIB 等成熟套件并做回归。

#### [Easy4PTK](https://github.com/alxanderjiang/Easy4PTK)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：5 · 宿主：github

Python/Jupyter 多星座 PPP-RTK 试验箱，强调可读与易移植，便于改状态估计、模糊度策略与改正接入。适合教学与方法原型验证。性能与电文覆盖通常弱于 cssrlib、MRTKLIB；产线或论文对比请用独立真值交叉验证。

## PPP-B2b

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Easy4B2b](https://github.com/alxanderjiang/Easy4B2b) | Easy4B2b：易移植 Python PPP-B2b 工具箱 | Jupyter Notebook | 0 | 🏷️ 个人社区 |
| [RTKNAVI-BH](https://github.com/cigit001/RTKNAVI-BH) | RTKNAVI-BH：RTKNAVI 扩展实时 PPP-B2b 与 HAS | — | 0 | 🏷️ 个人社区 |

### 详细说明

#### [Easy4B2b](https://github.com/alxanderjiang/Easy4B2b)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：0 · 宿主：github

面向北斗 PPP-B2b 的 Python 工具箱，强调易移植与试验。适合快速摸电文与改正字段，不先上 C++ 工程。性能与完备性通常弱于 B2bLIB/RTKLIB-B2b；产线应用建议交叉验证 C/C++ 实现。

#### [RTKNAVI-BH](https://github.com/cigit001/RTKNAVI-BH)  
*🏷️ 个人社区*

语言：— · 许可：NOASSERTION · 星标约：0 · 宿主：github

在 RTKNAVI 上扩展，尝试同时吃 PPP-B2b 与 Galileo HAS 改正做实时 PPP。适合桌面端联调双系统改正源。仓库较新、文档与稳定性需自测；复杂场景仍建议对照官方测试库与 demo5/RTKLIB 分支。

## 经典定位库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Essential-GNSS](https://sourceforge.net/projects/gnsstk/) | Essential-GNSS：轻量 C 库与事后 LSQ/EKF/RTK（SourceForge） | C | — | 🏷️ 个人社区 |

### 详细说明

#### [Essential-GNSS](https://sourceforge.net/projects/gnsstk/)  
*🏷️ 个人社区*

语言：C · 许可：BSD-style · 星标约：— · 宿主：sourceforge

Glenn MacGougan 等维护的 Essential GNSS Project，提供 RINEX 2.x 解码、YUMA/SEM、NovAtel OEM4 以及 LSQ/EKF/RTK 事后处理示例，许可证偏宽松 BSD 风格。与 Texas SGL 的 GPSTk/gnsstk 同名不同源，勿混淆。代码偏经典教学/嵌入，现代多星座 RINEX3+/PPP 请优先用更新栈。

## PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [raPPPid](https://github.com/TUW-VieVS/raPPPid) | raPPPid：维也纳 VieVS 的 PPP 模块 | MATLAB | 149 | 🏷️ 高校实验室 核心 |
| [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH) | GAMP_PPPH：多星座 PPP 学习源码 | — | 78 | 🏷️ 高校实验室 ★ |
| [GPSPACE](https://github.com/CGS-GIS/GPSPACE) | GPSPACE：加拿大 NRCan 开源 PPP Fortran 程序 | Fortran | 58 | 🏷️ 官方 |
| [PPPLib](https://github.com/yxw027/PPPLib) | PPPLib：开源精密单点定位库 | — | 49 | 🏷️ 高校实验室 |
| [PPP](https://github.com/XiaoGongWei/PPP) | PPP：静态精密单点定位 C++ 练习实现 | C++ | 23 | 🏷️ 高校实验室 |
| [PPPH-UAV](https://github.com/BerkayBahadur/PPPH-UAV) | PPPH-UAV：无人机摄影测量向 GNSS PPP（MATLAB） | MATLAB | 14 | 🏷️ 高校实验室 |
| [RTPPP_B2b](https://github.com/floating0516/RTPPP_B2b) | RTPPP_B2b：B2b 改正实时 PPP 接口 | C | 10 | 🏷️ 个人社区 核心 |
| [PyGNSSFix](https://github.com/rodrigo-moliveira/PyGNSSFix) | Python SPP/PPP 工具箱（WLS/EKF，GPS+GAL） | Python | 7 | 🏷️ 个人社区 |
| [ppp_rtklib](https://github.com/mulin33/ppp_rtklib) | ppp_rtklib：自 RTKLIB 抽出的独立 PPP 模块 | C | 4 | 🏷️ 个人社区 |

### 详细说明

#### [raPPPid](https://github.com/TUW-VieVS/raPPPid)  
*🏷️ 高校实验室 核心*

语言：MATLAB · 许可：GPL-3.0 · 星标约：149 · 宿主：github

VieVS（TU Wien）精密单点定位模块，MATLAB 实现，便于与 VLBI/大地测量流程结合。非实时引擎；工业 RTK/嵌入式请看 RTKLIB 或商业机。

#### [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH)  
*🏷️ 高校实验室 ★*

语言：— · 许可：— · 星标约：78 · 宿主：github

整理/公开的多星座 PPP 相关源码，常被中文社区当作 GAMP 学习材料。适合对照教材读流程。官方维护关系与许可需自行核实，慎直接用于生产。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [GPSPACE](https://github.com/CGS-GIS/GPSPACE)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：58 · 宿主：github

官方背景的 Fortran PPP，便于对照国家机构处理流程。适合研究与教学对照。现代多星座实时服务请结合 CSRS-PPP 网页与其他开源引擎。

#### [PPPLib](https://github.com/yxw027/PPPLib)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：49 · 宿主：github

开源 PPP 库，便于阅读 PPP 状态估计与资源管理结构。适合课程设计与二次开发起点。社区体量小于 PRIDE/RTKLIB；功能完整性以实测为准。

#### [PPP](https://github.com/XiaoGongWei/PPP)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：23 · 宿主：github

偏静态精密单点定位流程的 C++ 练习/研究代码，作者与 MG-APP 系列相关，便于对照阅读观测方程与参数估计骨架。适合理解 PPP 基本流程。工程完整度、多星座产品与模糊度固定支持有限；生产级 PPP-AR 请优先使用 PRIDE-PPPAR、Ginan 或 MRTKLIB 等更完整套件。

#### [PPPH-UAV](https://github.com/BerkayBahadur/PPPH-UAV)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：14 · 宿主：github

在 PPPH 思路上处理无人机原始 GNSS，服务摄影测量轨迹与产品生成，MATLAB 实现便于改流程与出图。做 UAV 测图轨迹增强、POS 辅助时可作参考。通用多星座 PPP-AR、模糊度固定与实时能力不如 PRIDE、Ginan；许可未显著标明，使用与再分发前请阅读仓库说明。影像时间戳与 GNSS 历元对齐是摄影测量成败关键。

#### [RTPPP_B2b](https://github.com/floating0516/RTPPP_B2b)  
*🏷️ 个人社区 核心*

语言：C · 许可：— · 星标约：10 · 宿主：github

解码北斗 PPP-B2b 广播的精密轨道钟差改正，带流解析、缓冲与完整性检查，便于接入实时 PPP 流水线。做 BDS-3 短报文 PPP 或接收机原型时应优先阅读。仓库体量小、许可未标明，工程化与多系统融合仍需自补；可与 PRIDE、Ginan、RTKLIB 实时分支对照改正数接口设计。区域服务范围与信号可见性会直接影响改正可用性。

#### [PyGNSSFix](https://github.com/rodrigo-moliveira/PyGNSSFix)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：7 · 宿主：github

面向事后处理的 Python GNSS 定位工具包（MIT），实现 SPP、伪距 PPP 与载波 PPP，支持 GPS/Galileo、单双频与消电离层组合，求解器含 WLS 与 EKF，并含周跳检测与模糊度相关流程。适合教学与可复现实验。目前星座覆盖与工程化程度不及 PRIDE/Ginan 一类大型套件；配置与产品输入需按仓库示例核对。

#### [ppp_rtklib](https://github.com/mulin33/ppp_rtklib)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：4 · 宿主：github

从 RTKLIB 源码中抽出 PPP 相关模块做成更小阅读单元，降低在庞大工程里迷路的成本，方便精读观测模型与参数估计。适合源码课与自学。功能范围取决于抽取边界，不保证与完整 RTKLIB 行为一致；修改后应回到官方工程跑回归再谈精度对比。

## PPP套件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Ginan-GA-portal](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/about-the-program/analysis-centre-software) | Ginan-GA-portal：GA 对 Ginan 分析中心软件的官方介绍页 | C++ | — | 🏷️ 官方 |

### 详细说明

#### [Ginan-GA-portal](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/about-the-program/analysis-centre-software)  
*🏷️ 官方*

语言：C++ · 许可：Apache-2.0 (see GitHub) · 星标约：— · 宿主：official_site

Geoscience Australia 对开源 GNSS 分析中心软件 Ginan 的官方说明，介绍实时改正服务与产品生成角色，并指向 GA GitHub 获取源码。适合了解国家级 PPP/改正链路背景；具体编译、模块划分与许可以 GitHub 仓库 README 为准。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 教学/PPP套件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gLAB-Download](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite-links/glab-download) | gLAB-Download：UPC gLAB 官方源码与 Win/Cygwin 安装包页 | C/Python | — | 🏷️ 高校实验室 |
| [gLAB-UPC](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite) | gLAB：GNSS 处理与教学套件 | C/Python | — | 🏷️ 高校实验室 核心 |

### 详细说明

#### [gLAB-Download](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite-links/glab-download)  
*🏷️ 高校实验室*

语言：C/Python · 许可：Apache-2.0 + LGPL-3.0 (GUI) · 星标约：— · 宿主：official_site

UPC gAGE 的 gLAB 发行下载页，列出各版本安装包、校验和与许可说明（GUI LGPL-3，核心/绘图 Apache 2.0）。做教学实验请从此获取而非不明镜像。版本与 Qt/Python 依赖需按说明匹配目标发行版，避免混用旧 GUI 与新核心。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [gLAB-UPC](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite)  
*🏷️ 高校实验室 核心*

语言：C/Python · 许可：Apache-2.0 + LGPL-3.0 (GUI) · 星标约：— · 宿主：official_site

加泰罗尼亚理工 gAGE 组发布的 GNSS-Lab Tool，覆盖观测建模、SPP/PPP、电离层与绘图。核心与绘图工具 Apache 2.0，Qt GUI 为 LGPL-3。官方下载含 Linux 源码包与 Windows 安装包；GitHub 上多为非官方镜像。适合教学与算法对照，非业务级实时引擎。

## 大地测量/GNSS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [groops](https://github.com/groops-devs/groops) | GROOPS：重力场与 GNSS 处理（TU Graz） | C++ | 244 | 🏷️ 高校实验室 ★ 核心 |
| [GARPOS](https://github.com/s-watanabe-jhod/garpos) | GARPOS：日本海保 GNSS-声学海底定位开源解算器 | Python | 25 | 🏷️ 官方 |
| [gnatss](https://github.com/seafloor-geodesy/gnatss) | gnatss：海底 GNSS-A 换能器测量社区软件 | Python | 17 | 🏷️ 个人社区 |
| [GAMIT/GLOBK](https://geoweb.mit.edu/gg/) | MIT EAPS 维护的 GAMIT/GLOBK 高精度 GNSS 大地测量解算套件主页 | Fortran/C | — | 🏷️ 高校实验室 |

### 详细说明

#### [groops](https://github.com/groops-devs/groops)  
*🏷️ 高校实验室 ★ 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：244 · 宿主：github

格拉茨工业大学 ITSG 背景的 GROOPS，覆盖重力场恢复、GNSS 处理与轨道确定，含 GUI 与 MPI 并行。适合大地测量联合反演与科研计算。学习曲线陡；纯导航 RTK/PPP-AR 工程请优先专用套件。

#### [GARPOS](https://github.com/s-watanabe-jhod/garpos)  
*🏷️ 官方*

语言：Python · 许可：GPL-3.0 · 星标约：25 · 宿主：github

日本海上保安厅水路部公开的 GARPOS，专用于 GNSS-Acoustic（船载 GNSS + 海底应答器测距）联合解算，并可同时估计声速结构相关参数。面向海底大地测量而非陆地 RTK/PPP。Python 实现，GPL-3.0；需准备观测配置与海洋声学先验，门槛偏专业。

#### [gnatss](https://github.com/seafloor-geodesy/gnatss)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：17 · 宿主：github

海床大地测量社区维护的 GNSS-Acoustic（GNSS-A）软件：海面 GNSS 与水声测距联合约束海底换能器/点位，用于海底形变与板块边界监测。面向海洋大地测量课题组。不是陆地 RTK/PPP；依赖船舶、声学与时间同步链路，作业与数据成本远高于陆基站网。社区仓库，版本接口以上游发布说明为准。

#### [GAMIT/GLOBK](https://geoweb.mit.edu/gg/)  
*🏷️ 高校实验室*

语言：Fortran/C · 许可：scientific distribution (request) · 星标约：— · 宿主：official_site

MIT 地球大气与行星科学系长期维护的 GAMIT/GLOBK 套件，GAMIT 负责双差相位网解（轨道、站坐标、对流层参数），GLOBK 用卡尔曼滤波合并多期松弛解生成速度场与时间序列，是构造地壳形变研究的主力工具之一。主页集中了快速入门、GAMIT/GLOBK 参考手册、更新记录与依赖说明；源码需先提交许可申请后获取，非 SPDX 开源许可。与 Bernese、GipsyX 属同一档次的科研解算软件，适合与本目录 PPP 类开源工具对照。收录前已 HTTP 200 核验。

## SPP/RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library) | libgnss++：现代 C++20 GNSS 工具包（SPP/RTK/PPP/CLAS） | C++ | 189 | 🏷️ 个人社区 |
| [SatellitePosition](https://github.com/LStudioLoren/SatellitePosition) | SatellitePosition：Python 单点/RTK 学习实现 | Python | 62 | 🏷️ 个人社区 |
| [MobileGNSS-SPP](https://github.com/salmoshu/MobileGNSS-SPP) | MobileGNSS-SPP：手机 GNSS 的 EKF 单点定位 | C | 41 | 🏷️ 高校实验室 |
| [GNSS-Explorer](https://github.com/brucezhcw/GNSS-Explorer) | GNSS-Explorer：基于 RTKLIB 的 SPP 算法优化探索 | C | 21 | 🏷️ 高校实验室 |
| [GNSSPositioning](https://github.com/bitecc/GNSSPositioning) | GNSSPositioning：含电离层/对流层改正的 SPP 教学程序 | C++ | 12 | 🏷️ 个人社区 |
| [SPP_SPV](https://github.com/GYH-WHU/SPP_SPV) | SPP_SPV：武大相关 GPS/BDS 单点定位与测速教学 | C++ | 7 | 🏷️ 高校实验室 |
| [GSILIB](https://terras.gsi.go.jp/geo_info/gsilib/gsilib.html) | GSILIB：多 GNSS 基线/PPP 解析库 | C | — | 🏷️ 官方 核心 |

### 详细说明

#### [libgnss++](https://github.com/rsasaki0109/gnssplusplus-library)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：189 · 宿主：github

含 Python 绑定、Docker 与 ROS2 支持，架构较新。适合嵌入式/机器人集成试验。精密产品级完整性与多星座策略仍需自测。

#### [SatellitePosition](https://github.com/LStudioLoren/SatellitePosition)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：62 · 宿主：github

用 Python 从零实现卫星单点定位与 RTK 相对定位的学习项目，注释与结构偏教学向。适合编程课、导航算法入门与作业模板。数值稳健性、周跳探测与多路径处理不及成熟库；学完概念后应用 RTKLIB 或 goGPS 做精度与固定率对照，避免把作业代码当生产引擎。

#### [MobileGNSS-SPP](https://github.com/salmoshu/MobileGNSS-SPP)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：41 · 宿主：github

针对智能手机 GNSS 原始测量设计的 EKF 单点定位实现，意在改善消费级轨迹连续性与噪声表现。适合手机导航算法原型与课程项目。精度达不到载波相位 RTK/PPP；天线相位中心、占空比与多路径仍在，可与 android_rinex、PRIDE-GeoDataLogger 采集链衔接做进一步研究。

#### [GNSS-Explorer](https://github.com/brucezhcw/GNSS-Explorer)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：21 · 宿主：github

在 RTKLIB 框架上探索 SPP 算法改进，例如加权模型、粗差探测或选星策略的小改动试验场。适合对照默认配置做消融实验与课程报告。不是独立大型定位套件；若计划回馈社区分支，需注意许可证、代码风格与完整回归测试，避免只报告单一场景上的收益。

#### [GNSSPositioning](https://github.com/bitecc/GNSSPositioning)  
*🏷️ 个人社区*

语言：C++ · 许可：Apache-2.0 · 星标约：12 · 宿主：github

中文注释友好的 SPP 示例：解码、卫星位置、SPP/SPV 及电离层对流层改正，适合本科课程。输入为 GNSS 观测；输出为定位结果与延迟改正中间量。局限：功能聚焦教学 SPP，不是精密 TEC/GIM 软件。

#### [SPP_SPV](https://github.com/GYH-WHU/SPP_SPV)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：7 · 宿主：github

基于 C++/MATLAB 的 GPS+BDS 单点定位与测速教学系统，可解码 NovAtel 等接收机输出后完成基本解算。适合本科/研究生课程设计。精度、完备性监测与粗差处理不及 RTKLIB 或商用引擎；科研对比应统一星历钟差产品与误差模型后再引用数值结论。

#### [GSILIB](https://terras.gsi.go.jp/geo_info/gsilib/gsilib.html)  
*🏷️ 官方 核心*

语言：C · 许可：BSD-2-Clause (ANTApp GPL-3.0) · 星标约：— · 宿主：official_site

国土地理院（GSI）基于 RTKLIB 2.4.2 与 ANTTOOL 发布的多 GNSS 解析软件，支持 GPS/QZSS/GLONASS/Galileo 的 L1/L2/L5 基线处理，并新增异机种 IFB/ISB 估计与 L2P–L2C 四分之一周校正。BSD-2（ANTApp 为 GPL-3）。适合日本公共测量与多星座短基线实验；Windows 为主，功能分批核验后公开，不是完整实时 RTK 套件。

## PPP后处理工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-ppp-matlab-toolbox](https://github.com/hvandermarel/gnss-ppp-matlab-toolbox) | gnss-ppp-matlab-toolbox：合并 NRCan CSRS-PPP 多日解 | MATLAB | 4 | 🏷️ 高校实验室 |

### 详细说明

#### [gnss-ppp-matlab-toolbox](https://github.com/hvandermarel/gnss-ppp-matlab-toolbox)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：4 · 宿主：github

Hans van der Marel（TU Delft）发布的 PPP 后处理工具箱，读取 CSRS-PPP 汇总/位置文件，把单日静力解合成为多日估计并做粗差与质量图形分析，另可读运动学位置、钟差与 ZTD。适合测站坐标与 GNSS 战役质控；本身不做观测级 PPP，依赖 NRCan 在线解与配套 crsutil 工具箱。

## PPP/RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [laika](https://github.com/commaai/laika) | laika：comma.ai 轻量 Python GNSS 库 | Python | 723 | 🏷️ 个人社区 核心 |
| [gnss-rtk](https://github.com/nav-solutions/gnss-rtk) | gnss-rtk：Rust PPP/RTK 解算（AGPL） | Rust | 79 | 🏷️ 个人社区 |

### 详细说明

#### [laika](https://github.com/commaai/laika)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：723 · 宿主：github

面向自动驾驶与研究的精简 GNSS 库，可下载星历与改正、做伪距定位并与 RTKLIB 风格流程对接，Python 接口干净。适合想快速验证定位链路、而不愿先啃完整测地软件栈的工程师与学生。功能覆盖远小于 PRIDE、Ginan、RTKLIB，模糊度固定与多频多星座产品化能力弱；和 rtklib-py、goGPS 对照时，优势在轻量与可嵌入脚本。

#### [gnss-rtk](https://github.com/nav-solutions/gnss-rtk)  
*🏷️ 个人社区*

语言：Rust · 许可：AGPL-3.0 · 星标约：79 · 宿主：github

与 rinex 库同一 Rust 生态的精密定位解算，AGPL。适合 Rust 栈爱好者。生态年轻于 RTKLIB；AGPL 对闭源集成不友好。

## 城市峡谷

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu) | gnss_gpu：CUDA 粒子滤波城市定位 | Python | 83 | 🏷️ 个人社区 |

### 详细说明

#### [gnss_gpu](https://github.com/rsasaki0109/gnss_gpu)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：83 · 宿主：github

用 GPU 粒子滤波和城市三维模型射线追踪抑制 NLOS，面向都市峡谷。适合研究型城市定位。依赖 CUDA 与城市模型数据，不适合无 GPU 的测地事后处理。

## 解析/分析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py) | gnss_lib_py：GNSS 解析、分析与可视化 | Python | 266 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：266 · 宿主：github

模块化解析 Android/原始测量与状态估计结果，可视化强，适合智能手机定位与算法课。不是传统测地 PPP 产品线；与 gps-measurement-tools 数据衔接好。

## RTKLIB移植

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssgo](https://github.com/FengXuebin/gnssgo) | gnssgo：Go 语言移植的 RTKLIB 2.4.3 b34 | Go | 22 | 🏷️ 个人社区 |

### 详细说明

#### [gnssgo](https://github.com/FengXuebin/gnssgo)  
*🏷️ 个人社区*

语言：Go · 许可：GPL-3.0 · 星标约：22 · 宿主：github

将经典 RTKLIB 2.4.3 核心用 Go 重写，便于在微服务与云环境中部署 GNSS 定位组件。示例数据需另行从原版 RTKLIB 获取。算法世代停在 b34；需要新信号/新改正时应评估上游活跃 RTKLIB 分支或 MRTKLIB，而非仅依赖本移植。

## RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rtkbase](https://github.com/Stefal/rtkbase) | rtkbase：树莓派自建 GNSS 基准站与 Web 管理 | Python | 769 | 🏷️ 个人社区 核心 |
| [rtklib-py](https://github.com/rtklibexplorer/rtklib-py) | rtklib-py：demo5 思路的 Python RTKLIB（偏 PPK） | Python | 244 | 🏷️ 个人社区 |
| [OpenRTK](https://github.com/AndreasArendt/OpenRTK) | OpenRTK：轻量开源精密 GNSS/RTK | C++ | 23 | 🏷️ 个人社区 |
| [HPRTK](https://github.com/yxw027/HPRTK) | HPRTK：高精度实时定位 C++ 工程参考 | C++ | 17 | 🏷️ 高校实验室 |
| [RTK](https://github.com/GYH-WHU/RTK) | RTK：GPS/BDS 双系统浮点/固定 RTK 教学实现 | C++ | 11 | 🏷️ 高校实验室 |
| [Qelaro](https://github.com/atoofihub/Qelaro) | 面向教学与可复现的 Python GNSS 双差基线解算工具箱（CLI+GUI） | Python | 10 | 🏷️ 个人社区 |
| [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK) | GNSSRTK：AGV 路径规划与车载显示的 GNSS-RTK 程序 | Python | 3 | 🏷️ 个人社区 |

### 详细说明

#### [rtkbase](https://github.com/Stefal/rtkbase)  
*🏷️ 个人社区 核心*

语言：Python · 许可：AGPL-3.0 · 星标约：769 · 宿主：github

把 u-blox/Septentrio、str2str、NTRIP 与网页管理捆成可部署基站。适合爱好者与小型台站。天线环境、电源与网络安全决定可用性；不是国家级 CORS 替代。

#### [rtklib-py](https://github.com/rtklibexplorer/rtklib-py)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：244 · 宿主：github

便于阅读算法与改实验脚本，当前侧重事后 PPK。适合不想编译 C 的教学。实时性能与完整性不及原生 RTKLIB/厂商方案。

#### [OpenRTK](https://github.com/AndreasArendt/OpenRTK)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：23 · 宿主：github

体量较小的开源 RTK/精密 GNSS 代码，MIT 许可便于嵌入式或课程裁剪。社区与文档成熟度明显小于 RTKLIB；上线前请自测模糊度与多星座支持范围。

#### [HPRTK](https://github.com/yxw027/HPRTK)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：17 · 宿主：github

围绕高精度实时定位组织的 C++ 工程，可作为网络 RTK 与实时改正链路的结构参考。适合阅读数据流调度、改正数接入与解算线程划分方式。文档完整度与持续维护情况一般；关键精度与固定率请用标准基线网评估，并与 RTKLIB 或商业引擎交叉验证后再写进论文指标。

#### [RTK](https://github.com/GYH-WHU/RTK)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：11 · 宿主：github

实现 GPS/BDS 双系统相对定位，覆盖单点、RTK 浮点解到固定解的基本流程，代码面向教学。适合课堂复现双差观测与模糊度固定。基线长度适应性、周跳探测与多路径抑制相对简化；与 RTKLIB、GraphGNSSLib 对照可读差异，不宜直接当作生产级 RTK 引擎。

#### [Qelaro](https://github.com/atoofihub/Qelaro)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：10 · 宿主：github

个人开发者发布的 Python GNSS/大地测量工具箱，MIT 许可并有 Zenodo DOI。首个版本聚焦基于 RINEX 观测、导航文件与 SP3 的双差基线最小二乘解算，提供命令行与 Web 图形界面（NestJS 前端 + FastAPI 服务），另含 SPP（Klobuchar/NeQuick-G 电离层改正）、LAMBDA 模糊度固定与 Melbourne-Wübbena 周跳探测等模块，并配有观测模型、差分策略与平差理论文档。代码透明、带测试 CI，适合课程作业或理解 RTK 原理，而非替代 RTKLIB 等成熟引擎。项目较新、星标不多，功能以文档声明为准。

#### [GNSSRTK](https://github.com/SupakunZ/GNSS_RTK)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：3 · 宿主：github

面向自动导引车（AGV）的 GNSS-RTK 应用：读取 SimpleRTK 等板卡数据，生成高精度行驶路径、地图标绘、到目标点距离，并设计车载显示界面。适合室外 AGV/机器人导引原型。归类为精密定位而非对流层或 GNSS-IR；RTK 解算深度不及 RTKLIB，强项在路径业务与人机界面集成。改正数链路与板卡配置需按 ArduSimple 等厂商文档准备。

## 相对定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java) | goGPS Java：JVM 版 GNSS 观测处理 | Java | 66 | 🏷️ 高校实验室 |

### 详细说明

#### [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java)  
*🏷️ 高校实验室*

语言：Java · 许可：— · 星标约：66 · 宿主：github

goGPS 的 Java 实现，便于嵌进 JVM 应用。功能气质同 MATLAB 版但生态不同。移动端/服务器集成可考虑；算法试验仍有人偏 MATLAB 版。

## 相对定位/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | goGPS MATLAB：低成本 GNSS 增强定位 | MATLAB | 327 | 🏷️ 高校实验室 ★ 核心 |

### 详细说明

#### [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB)  
*🏷️ 高校实验室 ★ 核心*

语言：MATLAB · 许可：— · 星标约：327 · 宿主：github

长期发展的 MATLAB GNSS 处理包，相对定位与低成本设备场景见长，教科研友好。适合实验室快速改算法。部署与授权不如 C/C++ 开源引擎；Java 版见 goGPS_Java。

## PVT

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [deep_gnss](https://github.com/Stanford-NavLab/deep_gnss) | deep_gnss：NavLab 深度学习 GNSS 定位实验代码 | Python | 127 | 🏷️ 高校实验室 |
| [snapshot-gnss-algorithms](https://github.com/JonasBchrt/snapshot-gnss-algorithms) | snapshot-gnss-algorithms：短快照 GNSS 定位算法集 | Python | 36 | 🏷️ 高校实验室 |
| [PrNet](https://github.com/AILocAR/PrNet) | PrNet：神经网络伪距改正（手机 GNSS） | Python | 30 | 🏷️ 高校实验室 |
| [E2EPrNet](https://github.com/AILocAR/E2EPrNet) | E2EPrNet：端到端神经伪距改正实现 | Python | 6 | 🏷️ 高校实验室 |
| [gps_pvt](https://github.com/fenrir-naru/gps_pvt) | gps_pvt：Ruby 可控 PVT + RINEX/SP3/UBX 解析 | C++ | 6 | 🏷️ 个人社区 |
| [NeRC](https://github.com/AILocAR/NeRC) | NeRC：可微地平线定位中的神经测距改正 | Python | 6 | 🏷️ 高校实验室 |

### 详细说明

#### [deep_gnss](https://github.com/Stanford-NavLab/deep_gnss)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：127 · 宿主：github

Stanford NavLab 公开的基于深度神经网络的 GNSS 位置估计仓库，用于学习型定位与传统模型对照实验。MIT 许可，偏论文复现与教学演示。数据划分与训练配置见仓库 README；非工程级 PPP/RTK 替代品，生产部署需配合物理模型、完备质控与完好性设计。

#### [snapshot-gnss-algorithms](https://github.com/JonasBchrt/snapshot-gnss-algorithms)  
*🏷️ 高校实验室*

语言：Python · 许可：ISC · 星标约：36 · 宿主：github

面向短时 GNSS snapshot 观测的定位估计算法实现，适用于功耗受限或间歇采样场景。ISC 许可，Python 为主。与连续跟踪接收机流水线不同；算法假设与样例数据见仓库，可与 SoftGNSS、PocketSDR 等 SDR 前端组合做快照定位试验，注意历元与辅助数据对齐。

#### [PrNet](https://github.com/AILocAR/PrNet)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：30 · 宿主：github

AILocAR 提出的 Neural Pseudorange Correction，用学习模型改正手机等低成本 GNSS 伪距偏差。Apache-2.0；衔接 Android 原始观测与城市峡谷定位研究。训练数据与推理配置见仓库；非物理完好性替代，生产需独立质控与完好性设计。

#### [E2EPrNet](https://github.com/AILocAR/E2EPrNet)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：6 · 宿主：github

AILocAR 在 PrNet 之后的端到端神经伪距改正实现，把改正与定位环节更紧耦合。Apache-2.0；星级不高但与 PrNet/NeRC 同谱系，便于对照实验。依赖与复现脚本见仓库 README，适合学习型定位研究而非工程级 RTK/PPP 替代。

#### [gps_pvt](https://github.com/fenrir-naru/gps_pvt)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：6 · 宿主：github

提供可在 Ruby 下控制的 PVT，并解析 RINEX/SP3/ANTEX/UBX。适合脚本自动化爱好者。小众语言生态限制社区体量；精密 PPP-AR 请看专用引擎。

#### [NeRC](https://github.com/AILocAR/NeRC)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：6 · 宿主：github

AILocAR 的 Neural Ranging Correction，结合可微移动地平线定位做测距改正，面向学习型 GNSS 定位链条。Apache-2.0；与 PrNet/E2EPrNet 同组，便于读论文复现。星级低、偏研究原型，工程部署需自备数据管线与评估指标。

## 因子图RTK

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | GraphGNSSLib：FGO 风格 GNSS/RTK 开源库 | C | 628 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib)  
*🏷️ 高校实验室 核心*

语言：C · 许可：— · 星标约：628 · 宿主：github

用因子图做 GNSS 定位与 RTK，把现代图优化引入经典差分流程。适合研究城市峡谷鲁棒性与 FGO+GNSS。传统基站网运维与播发不是其主场；LEO 扩展见 GraphGNSSLib_LEO。

## PVT/精密定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT) | GREAT-PVT：武大 GREAT 精密 PVT 软件 | C++ | 279 | 🏷️ 高校实验室 ★ 核心 |

### 详细说明

#### [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT)  
*🏷️ 高校实验室 ★ 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：279 · 宿主：github

GREAT-PVT 覆盖精密 PVT 相关能力，与 GREAT-MSF 等组合导航仓库同源风格。适合跟进武大 GREAT 公开算法。文档/用例完整度因版本而异；与 PRIDE 定位分工不同（更偏导航软件栈）。

## 因子图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RobustGNSS](https://github.com/wvu-navLab/RobustGNSS) | RobustGNSS：因子图稳健 GNSS 处理研究代码 | C++ | 149 | 🏷️ 高校实验室 |
| [gtsam_gnss](https://github.com/taroz/gtsam_gnss) | gtsam_gnss：GTSAM GNSS 因子 + MATLAB 包装 | C++ | 136 | 🏷️ 个人社区 |
| [ICE-Incremental-Covariance](https://github.com/wvu-navLab/ICE) | ICE：增量协方差估计稳健定位研究代码 | Shell | 60 | 🏷️ 高校实验室 |
| [GraphGNSSLib_LEO](https://github.com/PolyU-TASLAB/GraphGNSSLib_LEO) | GraphGNSSLib_LEO：GNSS+LEO 因子图定位开源包 | C++ | 18 | 🏷️ 高校实验室 |
| [GraphGNSSLib_LEO_V1.2](https://github.com/Gao-tech1/GraphGNSSLib_LEO_V1.2) | GraphGNSSLib_LEO_V1.2：LEO+GNSS 因子图定位 | C | 18 | 🏷️ 高校实验室 |
| [Robust-GNSS-FG-GMM-TD](https://github.com/TMBOC/Robust-GNSS-Estimation-using-FG-GMM-TD) | FG-GMM-TD：因子图与混合模型稳健 GNSS 估计 | MATLAB | 10 | 🏷️ 高校实验室 |

### 详细说明

#### [RobustGNSS](https://github.com/wvu-navLab/RobustGNSS)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：149 · 宿主：github

西弗吉尼亚大学导航实验室公开的稳健 GNSS 处理实现，基于因子图框架抑制粗差与非高斯噪声。MIT 许可；与同实验室 PPP-BayesTree、ICE 形成系列。偏论文复现与方法对照，非开箱测地生产链；依赖与示例数据见仓库，部署前需核对编译环境。

#### [gtsam_gnss](https://github.com/taroz/gtsam_gnss)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：136 · 宿主：github

在因子图框架里拼伪距/相位/IMU 等 GNSS 因子，并提供 MATLAB 包装。适合算法研究。完整测地产品链与模糊度策略需自配。

#### [ICE-Incremental-Covariance](https://github.com/wvu-navLab/ICE)  
*🏷️ 高校实验室*

语言：Shell · 许可：MIT · 星标约：60 · 宿主：github

西弗吉尼亚大学导航实验室发布的 Incremental Covariance Estimation 稳健定位软件，对应测量误差协方差自适应相关论文。MIT 许可；与同实验室 PPP-BayesTree 互补，偏方法复现而非测地生产套件。依赖、数据路径与 Shell 入口脚本见仓库说明，跑通前先核对环境。

#### [GraphGNSSLib_LEO](https://github.com/PolyU-TASLAB/GraphGNSSLib_LEO)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：18 · 宿主：github

香港理工 TASLab 在 GraphGNSSLib 基础上扩展的 GNSS–LEO 耦合定位包，用因子图融合 GNSS 实测与 LEO 仿真伪距/多普勒，并与 SPP 对比。面向城市峡谷等场景研究，依赖 ROS/Ceres 与 RTKLIB 读 RINEX。LEO 观测量多为仿真，实网可用性取决于数据准备。

#### [GraphGNSSLib_LEO_V1.2](https://github.com/Gao-tech1/GraphGNSSLib_LEO_V1.2)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：18 · 宿主：github

在 GraphGNSSLib 思路上面向 LEO 增强的因子图定位实现（FGO），MIT 许可。与 PolyU GraphGNSSLib_LEO 同主题、不同仓库版本线，便于对照 LEO-PNT/增强试验。偏研究原型，数据接口与依赖以仓库为准，非测地生产套件。

#### [Robust-GNSS-FG-GMM-TD](https://github.com/TMBOC/Robust-GNSS-Estimation-using-FG-GMM-TD)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：10 · 宿主：github

配套 ION ITM 2020 论文的开源实现：因子图、改进高斯混合模型与变换域方法做稳健 GNSS 估计。MIT 许可；适合粗差/非高斯场景方法对照。偏学术复现，工程集成需自行整理接口与数据格式，星级不高但主题与 RobustGNSS 互补。

## PPP-RTK/HAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HASlib.jl](https://github.com/feanor12/HASlib.jl) | HASlib.jl：Galileo HAS 库的 Julia 包装 | Julia | 0 | 🏷️ 个人社区 |
| [HASlibTestSuite](https://github.com/nlsfi/HASlibTestSuite) | 官方 HASlib 解码正确性测试套件 | — | 0 | 🏷️ 官方 |

### 详细说明

#### [HASlib.jl](https://github.com/feanor12/HASlib.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：0 · 宿主：github

把 HASlib 思路接到 Julia 的社区包装，方便 Julia 用户试验 Galileo HAS。维护与功能覆盖可能落后官方 C 库，关键路径建议仍对照 nlsfi/HASlib。

#### [HASlibTestSuite](https://github.com/nlsfi/HASlibTestSuite)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：0 · 宿主：github

配套 nlsfi/HASlib 的官方测试套件，用固定样例回归 Galileo HAS 解码与接口兼容性。集成或升级 HAS 库前应用它核对版本差异。本身不是定位引擎；解算仍依赖 HASlib 与下游 PPP 实现。

## PPP/HAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HASPPP](https://github.com/ZhangRunzhi20/HASPPP) | HASPPP：Galileo HAS 嵌入式 PPP 开源包 | C++ | 44 | 🏷️ 高校实验室 |

### 详细说明

#### [HASPPP](https://github.com/ZhangRunzhi20/HASPPP)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：44 · 宿主：github

针对 Galileo High Accuracy Service 的 PPP 开源实现，便于评估 HAS 改正性能。适合欧洲星座 HAS 试验。通用多星座 PPP-AR 请仍看 PRIDE 等。

## QZSS MADOCA-PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MALIB](https://github.com/JAXA-SNU/MALIB) | MALIB：MADOCA-PPP L6E 定位库 | C | 77 | 🏷️ 官方 |
| [MADOCALIB](https://github.com/QZSS-Strategy-Office/madocalib) | MADOCALIB：QZSS MADOCA-PPP 参考实现 | C | 59 | 🏷️ 官方 核心 |

### 详细说明

#### [MALIB](https://github.com/JAXA-SNU/MALIB)  
*🏷️ 官方*

语言：C · 许可：see upstream (RTKLIB-derived) · 星标约：77 · 宿主：github

日本宇宙航空研究开发机构与合作方发布的 MADOCA-PPP 专用程序包，在 RTKLIB 基础上强化 L6E 改正与 rtkrcv/rnx2rtkp 流程，并附带开空测试数据。面向实时与事后 MADOCA 定位试验。与内阁府 MADOCALIB/CLASLIB 互补；上游标注为 RTKLIB fork，选用时注意许可证与版本对应关系。

#### [MADOCALIB](https://github.com/QZSS-Strategy-Office/madocalib)  
*🏷️ 官方 核心*

语言：C · 许可：BSD-2-Clause (+ additional clauses) · 星标约：59 · 宿主：github

内阁府准天顶卫星系统战略室发布的 MADOCA-PPP 参考实现，源自 RTKLIB，面向多 GNSS 精密轨道钟差增强的 PPP/PPP-AR 与电离层改正试验。官方页与 GitHub 同步提供手册、样例与可选 Python GUI 前端。适合对接 QZSS MADOCA 服务做用户端算法验证；实时流处理与生产可靠性声明需对照官方免责与版本说明。

## RTKLIB封装

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyrtklib](https://github.com/IPNL-POLYU/pyrtklib) | pyrtklib：RTKLIB 的 Python 绑定 | C | 182 | 🏷️ 高校实验室 核心 |
| [MatRTKLIB](https://github.com/taroz/MatRTKLIB) | MatRTKLIB：RTKLIB 的 MATLAB 封装 | MATLAB | 99 | 🏷️ 个人社区 |
| [pyrtklib_demo5](https://github.com/IPNL-POLYU/pyrtklib_demo5) | pyrtklib_demo5：对接 rtklibexplorer demo5 的 pyrtklib | C | 13 | 🏷️ 高校实验室 |

### 详细说明

#### [pyrtklib](https://github.com/IPNL-POLYU/pyrtklib)  
*🏷️ 高校实验室 核心*

语言：C · 许可：MIT · 星标约：182 · 宿主：github

港理工 IPNL 将 RTKLIB C 核心封装为 Python 扩展，便于在科研脚本里直接调用 PPK/RTK/PPP 而不反复改 C 工程。适合算法对比、批量后处理与教学演示。接口覆盖取决于绑定版本；实时流与新信号支持需对照所选 RTKLIB 分支。与 rtklib-py（纯 Python 重写）不同，本库强调调用原生 C 性能。

#### [MatRTKLIB](https://github.com/taroz/MatRTKLIB)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：99 · 宿主：github

在 MATLAB 里调用 RTKLIB 并补齐科研常用分析步骤，降低「C 程序+画图」切换成本。适合已有 RTKLIB 经验的科研人员。性能关键路径仍在 RTKLIB 侧。

#### [pyrtklib_demo5](https://github.com/IPNL-POLYU/pyrtklib_demo5)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：13 · 宿主：github

在 pyrtklib 思路上对接 rtklibexplorer/demo5 补丁树，更贴近低成本接收机与社区常用改进。适合已经跟随 demo5 博客流程的用户迁移到 Python 批处理。维护节奏可能与主 pyrtklib 分叉；投产前用同一观测数据交叉比对官方 RTKLIB、demo5 命令行与本绑定输出。

## 多GNSS定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MG_APP](https://github.com/XiaoGongWei/MG_APP) | MG-APP：多 GNSS 精密定位应用 | C++ | 98 | 🏷️ 高校实验室 |
| [QuadSPP](https://github.com/hdkarimi/QuadSPP) | QuadSPP：多星座标准单点定位（SPP） | C | 14 | 🏷️ 个人社区 |

### 详细说明

#### [MG_APP](https://github.com/XiaoGongWei/MG_APP)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：98 · 宿主：github

与 GPS Solutions 论文配套的多 GNSS 定位软件，便于对照文章复现。适合学术复现。工程支持与持续更新取决于作者精力。

#### [QuadSPP](https://github.com/hdkarimi/QuadSPP)  
*🏷️ 个人社区*

语言：C · 许可：MIT · 星标约：14 · 宿主：github

多星座标准单点定位（SPP）实现，代码结构相对直接，便于核对广播星历、钟差与几何距离等基本模型。适合 SPP 基线实验与教学作业。不含模糊度固定与精密产品深度；进入 PPP/RTK 请换专用库，本仓库用来验证伪距定位链路与粗差剔除策略即可。

## PPP/PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MRTKLIB](https://github.com/h-shiono/MRTKLIB) | MRTKLIB：现代 PPP/PPP-RTK 定位库 | C | 78 | 🏷️ 高校实验室 核心 |
| [pygnsslab](https://github.com/PyGnssLab/pygnsslab) | pygnsslab：纯 Python 模块化 RINEX/PPP/PPP-AR | Python | 34 | 🏷️ 个人社区 |
| [Urban-RTKLIB](https://github.com/MayHarryWang/Urban-RTKLIB) | Urban-RTKLIB：面向城市峡谷的 RTKLIB 改版 | C | 25 | 🏷️ 高校实验室 |
| [mrtklib-docker-ui](https://github.com/h-shiono/mrtklib-docker-ui) | mrtklib-docker-ui：MRTKLIB 的 Docker/Web 演示界面 | TypeScript | 10 | 🏷️ 高校实验室 |
| [PPP-Wizard](http://www.ppp-wizard.net/) | PPP-Wizard：CNES 整数模糊度 PPP-AR | C++ | — | 🏷️ 官方 核心 |

### 详细说明

#### [MRTKLIB](https://github.com/h-shiono/MRTKLIB)  
*🏷️ 高校实验室 核心*

语言：C · 许可：— · 星标约：78 · 宿主：github

面向 PPP、PPP-AR 与 PPP-RTK（含 CLAS/MADOCA 等区域增强）的现代定位库，比经典 RTKLIB 默认树更贴近亚太 PPP-RTK 场景。适合评估 SSR/CSSR 改正接入与模糊度固定。文档与样例需要时间消化；与 PRIDE、Ginan、Urban-RTKLIB 对照时重点看改正数接口、收敛时间与固定率。上游许可请仔细阅读。

#### [pygnsslab](https://github.com/PyGnssLab/pygnsslab)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：34 · 宿主：github

纯 Python 方向的模块化工具，含 RINEX、PPP/PPP-AR 与实时流支持，降低 C++ 编译门槛。适合原型与教学。极致性能与完备产品化仍不及 PRIDE/Ginan。

#### [Urban-RTKLIB](https://github.com/MayHarryWang/Urban-RTKLIB)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：25 · 宿主：github

基于 RTKLIB 改造、面向城市峡谷导航的版本，更强调 PPP/PPP-RTK 在遮挡环境下的可用性。适合低成本城市精密定位试验。具体改动需对照上游 diff 与配置文件；与 MRTKLIB、rtklibexplorer 并列评估时，重点看遮挡建模、改正数接口与固定率统计。

#### [mrtklib-docker-ui](https://github.com/h-shiono/mrtklib-docker-ui)  
*🏷️ 高校实验室*

语言：TypeScript · 许可：MIT · 星标约：10 · 宿主：github

给 MRTKLIB 套一层容器与网页操作，降低命令行门槛，便于课堂或外场演示 PPP/PPP-RTK。适合快速试 CLAS/MADOCA 相关配置与看星空图类状态。解算能力完全取决于背后的 MRTKLIB 版本与改正源；复杂工程参数仍建议回到命令行复现，并把容器镜像 tag 钉死以免漂移。

#### [PPP-Wizard](http://www.ppp-wizard.net/)  
*🏷️ 官方 核心*

语言：C++ · 许可：see upstream · 星标约：— · 宿主：official_site

法国空间研究中心（CNES）PPP-WIZARD 项目门户，介绍零差整数模糊度 PPP-AR 演示软件、SSR 计算与日产品/监测入口。适合了解 CNES 实时 PPP-AR 路线并申请软件包。源码不在本页直接 git 克隆；获取方式与许可以官网说明为准，并与 IGS 实时流配合使用。

## 定位软件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Net_Diff](https://github.com/YizeZhang/Net_Diff) | Net_Diff：下载+定位+分析综合套件 | HTML | 178 | 🏷️ 高校实验室 |
| [POSGO](https://github.com/lizhengnss/POSGO) | POSGO：C++ 开源 GNSS 定位软件 | C++ | 116 | 🏷️ 高校实验室 |

### 详细说明

#### [Net_Diff](https://github.com/YizeZhang/Net_Diff)  
*🏷️ 高校实验室*

语言：HTML · 许可：— · 星标约：178 · 宿主：github

张一泽等维护的综合工具，覆盖 GNSS 产品下载、多种定位模式与结果分析，中文资料与用户基础较好。适合教学演示、课程设计与中小规模科研试验。相对 PRIDE-PPPAR、Ginan 等，源码开放形态与工程依赖需按仓库说明核对；大规模业务化 PPP-AR 仍建议对照专用精密引擎。版本更新后注意示例配置与产品路径是否仍兼容。

#### [POSGO](https://github.com/lizhengnss/POSGO)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：116 · 宿主：github

面向定位算法实验与二次开发的 C++ 仓。适合跟进图优化/组合导航课程作业。成熟度与文档因版本而异，引用前请自备回归数据。

## PPP脚本

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ppp-tools](https://github.com/aewallin/ppp-tools) | ppp-tools：RINEX→PPP 自动化脚本（时间实验室向） | Python | 121 | 🏷️ 个人社区 |

### 详细说明

#### [ppp-tools](https://github.com/aewallin/ppp-tools)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-2.0 · 星标约：121 · 宿主：github

脚本化调用外部 PPP 并归档结果，常见于时间实验室/钟差相关流程。适合自动化胶水道具。核心解算仍依赖外部引擎；不是独立精密定位库。

## PPP-AR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR) | PRIDE-PPPAR：多星座 PPP 模糊度固定 | C | 415 | 🏷️ 高校实验室 ★ 核心 |
| [PPP_AR](https://github.com/heiwa0519/PPP_AR) | PPP_AR：多星座 PPP 模糊度固定实现 | C | 40 | 🏷️ 高校实验室 |

### 详细说明

#### [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR)  
*🏷️ 高校实验室 ★ 核心*

语言：C · 许可：GPL-3.0 · 星标约：415 · 宿主：github

面向多 GNSS 的 PPP-AR 开源软件，科研引用多，模糊度固定与产品接口成熟。适合高精度事后 PPP、地壳形变、气象 ZTD。实时 PPP-RTK 与图形界面非重点；学习曲线陡于 RTKLIB。

#### [PPP_AR](https://github.com/heiwa0519/PPP_AR)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：40 · 宿主：github

围绕多星座 PPP 模糊度固定（PPP-AR）组织的实现，便于对照教材中的宽巷/窄巷与产品依赖关系。适合学习 PPP-AR 流程。工程化程度、实时性与 OSB/UPD 产品格式支持参差不齐；严肃精度评估请交叉验证 PRIDE-PPPAR、Ginan 或 MRTKLIB。

## 处理/绘图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyRTKLib-RINEX](https://github.com/alainmuls/pyRTKLib) | pyRTKLib：RINEX GPS/Galileo 处理与绘图 | Python | 50 | 🏷️ 个人社区 |

### 详细说明

#### [pyRTKLib-RINEX](https://github.com/alainmuls/pyRTKLib)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：50 · 宿主：github

个人维护的 Python 工具，侧重 RINEX GPS/Galileo 观测处理与绘图，教学演示友好。与港理工 IPNL 的 pyrtklib（原生 RTKLIB C 绑定）不是同一项目；精密模糊度固定与多星座 PPP-AR 请用专用引擎。

## RAIM/完好性

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RAIM_PANG_NAV](https://github.com/MichaelBeechan/RAIM_PANG_NAV) | RAIM_PANG_NAV：PANG-NAV 向 MATLAB RAIM 完好性监测 | MATLAB | 14 | 🏷️ 个人社区 |
| [gnss-integrity-raim](https://github.com/OrbitAR7/gnss-integrity-raim) | gnss-integrity-raim：Python RAIM 与保护级示例 | Python | 4 | 🏷️ 个人社区 |

### 详细说明

#### [RAIM_PANG_NAV](https://github.com/MichaelBeechan/RAIM_PANG_NAV)  
*🏷️ 个人社区*

语言：MATLAB · 许可：BSD-3-Clause · 星标约：14 · 宿主：github

在单点定位工具链上补充接收机自主完好性监测（RAIM），用于故障探测/排除与完好性告警相关研究与教学。适合航空等对完好性敏感的场景入门。实现深度与标准符合性需对照 DO-229 等规范自行核验；本仓并非完整 SBAS/ARAIM 产品级软件。

#### [gnss-integrity-raim](https://github.com/OrbitAR7/gnss-integrity-raim)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

实用的 Receiver Autonomous Integrity Monitoring 教学实现，含卡方故障探测、排除与 HPL/VPL，并提供 Stanford 图等可视化。MIT 许可；填补目录中开源 RAIM 示例缺口。偏演示与课程，航空级认证请遵循相应 DO 标准与审定流程。

## RTK/PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | RTKLIB：经典开源 GNSS 定位工具箱（RTK/PPP） | C | 3128 | 🏷️ 个人社区 ★ 核心 |
| [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB) | RTKLIB-explorer：面向低成本接收机的 RTKLIB 分支 | C | 971 | 🏷️ 个人社区 核心 |

### 详细说明

#### [RTKLIB](https://github.com/tomojitakasu/RTKLIB)  
*🏷️ 个人社区 ★ 核心*

语言：C · 许可：— · 星标约：3128 · 宿主：github

窗口工具与嵌入式移植极广，是开源 RTK/PPP 入门与生产原型的常见底座。适合低成本接收机与教学实验。默认分支对部分多星座/低成本场景需配合 demo5 等社区分支；实时链路与模糊度策略要因机型验证。

#### [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB)  
*🏷️ 个人社区 核心*

语言：C · 许可：— · 星标约：971 · 宿主：github

针对低成本 GNSS 的活跃社区分支，博客与讨论丰富。适合手持/无人机 RTK 试验。非官方担保；升级与实时安全策略请自行回归。

## 多功能引擎

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sidereon](https://github.com/neilberkman/sidereon) | sidereon：Rust 统一 SPP/RTK/PPP 与轨道力学引擎 | Rust | 18 | 🏷️ 个人社区 |

### 详细说明

#### [sidereon](https://github.com/neilberkman/sidereon)  
*🏷️ 个人社区*

语言：Rust · 许可：MIT · 星标约：18 · 宿主：github

一个核心提供 SPP/RTK/PPP、SGP4/会合等与 RINEX/RTCM/SP3/NTRIP 解析，并带多语言绑定。适合想要「单依赖多协议」的新项目。相对经典库验证样本仍在积累，关键应用需交叉比对 RTKLIB/IGS。

## 定位引擎绑定

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sidereon-python](https://github.com/neilberkman/sidereon-python) | sidereon 引擎 Python 包（SPP/轨道/格式） | Python | 1 | 🏷️ 个人社区 |

### 详细说明

#### [sidereon-python](https://github.com/neilberkman/sidereon-python)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

sidereon 统一 GNSS+轨道力学引擎的 Python 发行（MIT，pip install sidereon），以 numpy 数组暴露 SPP、TLE 传播、SP3 加载与时间/坐标系转换；核为静态链接 Rust。目录已收录 Rust 主仓 sidereon，本条便于 Python 用户直达。功能面仍在演进；精密 PPP/RTK 深度需对照主仓路线图。

## 形变/多源联合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IGP-TUDelft](https://github.com/TUDelftGeodesy/IGP) | TU Delft IGP：GNSS/InSAR/水准 STM 联合处理 | MATLAB | 2 | 🏷️ 高校实验室 |

### 详细说明

#### [IGP-TUDelft](https://github.com/TUDelftGeodesy/IGP)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：2 · 宿主：github

TU Delft 开源 IGP（MATLAB，Apache-2.0）：以 Space-Time Matrix 统一 GNSS/InSAR/水准等多源形变处理（选择、检验、预测与可视化）。需 MATLAB；InSAR 初始化与数据准备成本不低，偏大地测量形变而非电离层 TEC。

## RTK客户端

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TouchRTKStation](https://github.com/taroz/TouchRTKStation) | TouchRTKStation：RTKLIB 单频流动/基准站方案 | C | 99 | 🏷️ 个人社区 |
| [ELT_RTKBase](https://github.com/GNSSOEM/ELT_RTKBase) | ELT_RTKBase：多品牌接收机的树莓派 RTK 基准站 | Shell | 70 | 🏷️ 个人社区 |
| [rtk_client](https://github.com/tobiasnix/rtk_client) | Python 终端 RTK：NTRIP + 串口 GNSS 客户端 | Python | 0 | 🏷️ 个人社区 |

### 详细说明

#### [TouchRTKStation](https://github.com/taroz/TouchRTKStation)  
*🏷️ 个人社区*

语言：C · 许可：MIT · 星标约：99 · 宿主：github

taroz 维护的单频 RTK-GNSS 流动/基准站方案，底层依托 RTKLIB，面向可触摸终端与野外快速架站。MIT 许可；与纯命令行 RTKLIB 相比更偏整机与交互体验。适合教学与低成本单频实验，多频与完好性能力有限，硬件串口与电台配置见仓库说明。

#### [ELT_RTKBase](https://github.com/GNSSOEM/ELT_RTKBase)  
*🏷️ 个人社区*

语言：Shell · 许可：AGPL-3.0 · 星标约：70 · 宿主：github

基于 Stefal/rtkbase 的分支增强，面向树莓派等单板，适配 Unicore UM98x、Bynav M2x、Septentrio Mosaic X5 与 u-blox ZED-X20P 等接收机。AGPL-3.0；提供 Web GUI 自建 NTRIP 基准。许可与上游 rtkbase 一致需注意传染性；硬件接线与安装脚本见仓库。

#### [rtk_client](https://github.com/tobiasnix/rtk_client)  
*🏷️ 个人社区*

语言：Python · 许可：AGPL-3.0 · 星标约：0 · 宿主：github

Python 终端 RTK 客户端（AGPL-3.0）：经 NTRIP 拉取 RTCM3 改正并注入串口 GNSS 模块，curses 界面显示 Fixed/Float、卫星与 SNR，支持 TLS、YAML 配置、CSV 轨迹日志、自动重连与模块配置文件（LC29H / generic NMEA）。面向低成本流动站联调，不是模糊度固定解算库（依赖接收机内部 RTK）。星标虽少但 2026 仍有推送；部署需自备 NTRIP 账号与兼容接收机。

## 实时PVT

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rt-navi](https://github.com/nav-solutions/rt-navi) | rt-navi：Rust 实时导航演示（U-Blox + gnss-rtk） | Rust | 12 | 🏷️ 个人社区 |

### 详细说明

#### [rt-navi](https://github.com/nav-solutions/rt-navi)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：12 · 宿主：github

nav-solutions 框架下的实时 PoC：以 U-Blox 原始/手动模式作测量源，喂给同组织的 PVT 解算器并与接收机固件解对比。MPL-2.0；当前单串口单接收机。偏工程验证而非测地级 PPP-AR 产品，外参、时间同步与对流层模型需使用者自理。与已收录的 gnss-rtk/rinex 等 crate 同一生态。

## GNSS算法库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [libswiftnav](https://github.com/swift-nav/libswiftnav) | libswiftnav：Swift Navigation 可移植 GNSS 算法 C 库 | C | 23 | 🏷️ 个人社区 |

### 详细说明

#### [libswiftnav](https://github.com/swift-nav/libswiftnav)  
*🏷️ 个人社区*

语言：C · 许可：LGPL-3.0 · 星标约：23 · 宿主：github

标准 C 实现的平台无关 GNSS 工具库（libswiftnav），LGPL-3.0，面向软件接收机或需 GNSS 数值例程的嵌入式/主机程序。不负责与 Swift 接收机通信（那是 libsbp）；本库偏算法与公用函数。构建需 CMake；API 随版本演进，接入前请对照文档与测试。与已收录的 libsbp/piksi_tools 同属厂商开源栈。

## 多路径AI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NavAI](https://github.com/AlvaroTena/NavAI) | NavAI：多路径缓解与观测加权的 AI 研究代码 | Python | 6 | 🏷️ 个人社区 |

### 详细说明

#### [NavAI](https://github.com/AlvaroTena/NavAI)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

博士课题开源：将机器学习用于 GNSS 观测可靠性与多路径抑制，并含仿真与加权实验代码，MIT 许可。星数不多但补齐多路径/AI 交叉这一薄点。结果依赖训练数据与场景，不能直接当作通用测地产品。适合算法对照与复现实验；部署需自备观测与标签管线。

## PPK教程

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS-Correction-RTKLIB](https://github.com/bpurinton/GNSS-Correction-RTKLIB) | GNSS-Correction-RTKLIB：dGPS/PPK 教程与 RTKLIB 批处理脚本 | Python | 24 | 🏷️ 个人社区 |

### 详细说明

#### [GNSS-Correction-RTKLIB](https://github.com/bpurinton/GNSS-Correction-RTKLIB)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：24 · 宿主：github

面向野外 dGPS/PPK 的开源手册与示例：Trimble 采集说明、RTKLIB 差分解算步骤，以及 Python 批处理脚本（可输出 CSV/SHP），GPL-3.0。偏教学与可复现工作流，而非新型解算引擎。配置文件与路径需按本机 RTKLIB 安装调整。适合入门 PPK 与批量点位改正。
