# 轨道与钟差 / Orbit & Clock
> **18** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。

## 时间比对

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cggtts](https://github.com/nav-solutions/cggtts) | CGGTTS 共视/全视时间比对解析库 | Rust | 18 | 🏷️ 个人社区 |

### 详细说明

#### [cggtts](https://github.com/nav-solutions/cggtts)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：18 · 宿主：github

处理 CGGTTS 格式与轨迹调度，服务 GNSS 共视/全视远程时间比对链路。适合时间频率实验室与计量场景。一般导航定位、RTK/PPP 用户通常用不到该格式栈。

## 钟差/相位偏差合成

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [clkcomb](https://github.com/YuanxinPan/clkcomb) | clkcomb：多 GNSS 钟差与相位偏差产品合成 | C++ | 3 | 🏷️ 高校实验室 |

### 详细说明

#### [clkcomb](https://github.com/YuanxinPan/clkcomb)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：3 · 宿主：github

Yuanxin Pan 开源的钟差/相位偏差合成工具，源于学位论文并应用于武大参与的 IGS 第三次重处理等研究，可综合多分析中心产品以改善 PPP-AR。附理论文档与论文索引。星标不多但科学指向明确；闭源 PPPx 二进制定位引擎不在本条目范围。

## 轨道钟差综合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GFZ-SPOCC-news](https://www.gfz.de/en/section/space-geodetic-techniques/overview/details-section-news/veroeffentlichung-der-software-for-precise-orbit-and-clock-combination-spocc-1) | GFZ 发布 SPOCC 的新闻说明：多 GNSS 轨道钟差综合开源 | Python | — | 🏷️ 官方 |
| [IGSMAIL-SPOCC](https://lists.igs.org/pipermail/igsmail/2025/008556.html) | IGSmail：SPOCC 轨道钟差综合软件向社区发布的公告 | text | — | 🏷️ 官方 |
| [SPOCC](https://gnss.gfz.de/services/spocc) | SPOCC：多分析中心轨道钟差综合 | Python | — | 🏷️ 官方 核心 |

### 详细说明

#### [GFZ-SPOCC-news](https://www.gfz.de/en/section/space-geodetic-techniques/overview/details-section-news/veroeffentlichung-der-software-for-precise-orbit-and-clock-combination-spocc-1)  
*🏷️ 官方*

语言：Python · 许可：open (GFZ release) · 星标约：— · 宿主：official_site

GFZ 正式介绍 SPOCC 背景与目标的新闻页，说明从原型到可发布 Python/Docker 包的过程，并指向 gnss.gfz.de 下载。适合了解发布动机与组合策略；实际安装、配置与示例仍以软件服务页及用户文档为准。使用前请核验上游页面与许可条款。

#### [IGSMAIL-SPOCC](https://lists.igs.org/pipermail/igsmail/2025/008556.html)  
*🏷️ 官方*

语言：text · 许可：n/a (announcement) · 星标约：— · 宿主：official_site

国际 GNSS 服务邮件列表中关于 SPOCC 开源发布的公告，确认软件面向多星座轨道与钟差加权综合，并给出 GFZ 服务页链接。属于官方发布记录，便于引用发布时间线；获取软件请转服务页，本页本身不是代码仓。使用前请核验上游页面与许可条款。

#### [SPOCC](https://gnss.gfz.de/services/spocc)  
*🏷️ 官方 核心*

语言：Python · 许可：open (GFZ release) · 星标约：— · 宿主：official_site

GFZ 发布的 Software for Precise Orbit and Clock Combination，用方差分量估计对多家分析中心 SP3/CLK 做多星座加权综合，并提供 Docker。面向 IGS 组合与 PPP 用户产品试验。2025 年起经 IGSmail 公开；输入需标准轨道钟差格式，不是单站 PPP 引擎。

## DCB/UPD/IFCB/OSB

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Gkit-Bias](https://github.com/LiZhengXiao99/Gkit-Bias) | Gkit-Bias：全频点卫星端偏差估计 | C++ | 8 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [Gkit-Bias](https://github.com/LiZhengXiao99/Gkit-Bias)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：8 · 宿主：github

C++ 实现三套偏差模式：DCB（码偏差与 VTEC 球谐联立）、UPD 与 IFCB（频间钟差），并支持向 OSB 转换，服务全频点 PPP-AR。输入侧重 RINEX 观测与星历。文档以中文为主，适合偏差链路研究；与 GREAT-UPD/IFCB、CAS DCB 产品对照使用，生产稳定性需自测。

## 钟差/轨道/UPD

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Cube](https://github.com/liush18/Cube) | Cube：精密测量院 GPS 钟差/PPP-AR（RTKLIB 二次开发） | C | 30 | 🏷️ 高校实验室 |
| [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD) | GREAT-UPD：多星座 UPD 估计 | C++ | 19 | 🏷️ 高校实验室 核心 |
| [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT) | GREAT_PODFLT：实时滤波精密定轨 | C++ | 17 | 🏷️ 高校实验室 核心 |
| [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB) | GREAT-IFCB：多 GNSS 频间钟差（IFCB）估计 | C++ | 15 | 🏷️ 高校实验室 |
| [rt-clk-service](https://github.com/DoubleString/rt-clk-service) | rt-clk-service：实时钟差/轨道/UPD/IFPB 服务代码 | C++ | 12 | 🏷️ 高校实验室 |
| [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE) | GREAT-PCE：精密卫星钟差估计 | C++ | 9 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [Cube](https://github.com/liush18/Cube)  
*🏷️ 高校实验室*

语言：C · 许可：BSD-2-Clause · 星标约：30 · 宿主：github

基于 RTKLIB 的服务端钟差/解耦钟（DCK）估计与用户端 PPP/PPP-AR 工具，可输出坐标、ZTD、模糊度与残差文件。BSD-2（继承 RTKLIB）。适合研究 IRC/DCK 模型与钟差产品生成；目前以 GPS、Windows 实验为主，多星座与跨平台移植需自行扩展。

#### [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：19 · 宿主：github

专门估计多星座 GNSS UPD/未校准相位延迟类产品，为 PPP-AR 模糊度固定提供相位偏差输入。适合需要自建相位偏差链路的课题组与教学演示。产品字段与 IGS OSB/UPD 惯例必须对齐才能接到 PRIDE 等下游；参考卫星选择、日边界与站网几何会直接影响稳定性，发布前应用公开网做交叉检验。

#### [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：— · 星标约：17 · 宿主：github

执行多 GNSS 实时滤波精密轨道确定（POD），偏产品生成与定轨算法验证，而非终端定位。适合轨道/钟差方向研究生对照 GREAT 流水线。公开算例与力模型文档完整度需自查；与 Ginan、GROOPS 等大型套件相比，更适合精读 GREAT 定轨滤波环节，而不是替代整套业务定轨系统。

#### [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：15 · 宿主：github

武大 GREAT 组开源的多星座频间钟差（IFCB）估计工具，服务于精密钟差与偏差产品链路，与 GREAT-PVT 等同一研究线。做三频 PPP、相位偏差与钟差产品的人应关注。它是独立小工具，不替代完整 POD 套件；轨道与 UPD/OSB 能力仍多见诸 Ginan、PRIDE、GROOPS 等大型系统。

#### [rt-clk-service](https://github.com/DoubleString/rt-clk-service)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：12 · 宿主：github

面向实时钟差、轨道与 UPD/IFPB 等偏差产品的服务向代码，贴近 PPP-AR 实时链。适合研究实时产品生成。公开完整度有限，需自备数据与对照 IGS 产品。

#### [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：9 · 宿主：github

聚焦精密卫星钟差估计，可与 GREAT-UPD、POD 模块组成轨道钟差产品链，服务 PPP 与时间传递相关研究。适合钟差建模、实时/事后产品试验。输入轨道与地面站网质量决定上限；若目标只是终端定位，通常直接使用 IGS/分析中心钟差即可，不必自建整条钟差产线。

## OSB/偏差估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MCOSB](https://github.com/GCCLib/MCOSB) | MCOSB：多 GNSS 多频码 OSB 估计 MATLAB 工具 | MATLAB | 11 | 🏷️ 高校实验室 |

### 详细说明

#### [MCOSB](https://github.com/GCCLib/MCOSB)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：see upstream README · 星标约：11 · 宿主：github

面向多系统多频码观测的 OSB 估计脚本集，含读观测、提取多通道偏差、估计与分析等步骤，并涉及 SINEX 类偏差文件。用户需自行准备测站网观测数据。适合偏差产品研究与教学；生产级 OSB 仍以 IGS/各分析中心产品为主，本库偏算法复现。

## 轨道确定/基础库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Orekit](https://github.com/CS-SI/Orekit) | Orekit：开源太空动力学与轨道传播基础库 | Java | 298 | 🏷️ 个人社区 |
| [orbdetpy](https://github.com/ut-astria/orbdetpy) | orbdetpy：Python/Java 轨道确定开源工具 | Java | 129 | 🏷️ 高校实验室 |
| [tudatpy](https://github.com/tudat-team/tudatpy) | tudatpy：TU Delft 天体动力学 Python 工具箱 | Python | 91 | 🏷️ 高校实验室 |

### 详细说明

#### [Orekit](https://github.com/CS-SI/Orekit)  
*🏷️ 个人社区*

语言：Java · 许可：Apache-2.0 · 星标约：298 · 宿主：github

CS-SI 维护的底层太空动力学库，覆盖轨道传播、力模型、姿态与时间尺度等，GNSS 精密轨道分析中常作基础组件。Apache-2.0；议题追踪多在 gitlab.orekit.org。质量高但非专用 GNSS POD 套件，观测模型需自建；主语言为 Java，Python 绑定需另寻社区包装。

#### [orbdetpy](https://github.com/ut-astria/orbdetpy)  
*🏷️ 高校实验室*

语言：Java · 许可：GPL-3.0 · 星标约：129 · 宿主：github

德州大学 ASTRIA 实验室的 Orbit Determination with Python，面向空间目标轨道确定与相关仿真。GPL-3.0；填补目录中小型 OD 工具缺口，与 tudatpy/Orekit 可对照。偏空间态势感知场景，GNSS 测地级 POD 请另选 Ginan、GROOPS 等专用处理链。

#### [tudatpy](https://github.com/tudat-team/tudatpy)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：91 · 宿主：github

Tudatpy 是 TU Delft Tudat 的 Python 接口，面向轨道传播、天体动力学仿真与教学。BSD-3-Clause；与 Orekit 互补（Python/C++ 绑定 vs Java）。非专用 GNSS POD 套件，但可作精密轨道/力模型实验底座；推荐用 conda 发行包，完整文档与示例见 tudat.space。

## 偏差与校准

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IGS-Bias-Calibration-WG](https://igs.org/wg/bias/) | IGS 偏差与校准工作组：DCB/OSB 等偏差产品入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IGS-Bias-Calibration-WG](https://igs.org/wg/bias/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

汇总 IGS Bias and Calibration 工作组活动，面向差分码偏差、可观测量特定偏差（OSB）及校准议题。对 PPP-AR、多系统组合与钟差产品一致性很关键。页面为活动与文档入口，具体偏差文件仍从 IGS 产品树获取。收录前已 HTTP 核验；引用请注明产品来源与版本。

## 时标产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BIPM-Time-FTP](https://www.bipm.org/en/time-ftp) | BIPM 时间 FTP：UTC/UTCr/TT(BIPM) 等时标产品入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BIPM-Time-FTP](https://www.bipm.org/en/time-ftp)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

国际计量局时间部门提供的 FTP/产品入口，涵盖 UTC、快速 UTC 与 TT(BIPM) 等时标文件，是 GNSS 时间比对、CGGTTS 与实验室钟差溯源的常用上游。页面说明访问方式与目录结构，实际文件经 FTP 拉取。时标修订与通告需对照 BIPM Circular T。收录前已 HTTP 核验；使用请遵守 BIPM 数据政策。
