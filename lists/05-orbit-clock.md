# 轨道与钟差 / Orbit & Clock
> **31** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

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

Yuanxin Pan 开源的钟差/相位偏差合成工具，源于学位论文并应用于武大参与的 IGS 第三次重处理等研究，可综合多分析中心产品以改善 PPP-AR。附理论文档与论文索引。星标不多但科学指向明确；闭源 PPPx 二进制定位引擎不在本仓库内。

## DCB/UPD/IFCB/OSB

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Gkit-Bias](https://github.com/LiZhengXiao99/Gkit-Bias) | Gkit-Bias：全频点卫星端偏差估计 | C++ | 8 | 🏷️ 个人社区 核心 |

### 详细说明

#### [Gkit-Bias](https://github.com/LiZhengXiao99/Gkit-Bias)  
*🏷️ 个人社区 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：8 · 宿主：github

C++ 实现三套偏差模式：DCB（码偏差与 VTEC 球谐联立）、UPD 与 IFCB（频间钟差），并支持向 OSB 转换，服务全频点 PPP-AR。输入侧重 RINEX 观测与星历。文档以中文为主，适合偏差链路研究；与 GREAT-UPD/IFCB、CAS DCB 产品对照使用，生产稳定性需自测。

## 钟差/轨道/UPD

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Cube](https://github.com/liush18/Cube) | Cube：GPS 钟差/解耦钟与 PPP-AR（RTKLIB 二次开发） | C | 30 | 🏷️ 个人社区 |
| [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD) | GREAT-UPD：多星座 UPD 估计 | C++ | 19 | 🏷️ 高校实验室 核心 |
| [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT) | GREAT_PODFLT：实时滤波精密定轨 | C++ | 17 | 🏷️ 高校实验室 核心 |
| [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB) | GREAT-IFCB：多 GNSS 频间钟差（IFCB）估计 | C++ | 15 | 🏷️ 高校实验室 |
| [rt-clk-service](https://github.com/DoubleString/rt-clk-service) | rt-clk-service：实时钟差/轨道/UPD/IFPB 服务代码 | C++ | 12 | 🏷️ 个人社区 |
| [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE) | GREAT-PCE：精密卫星钟差估计 | C++ | 9 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [Cube](https://github.com/liush18/Cube)  
*🏷️ 个人社区*

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
*🏷️ 个人社区*

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

语言：MATLAB · 许可：— · 星标约：11 · 宿主：github

面向多系统多频码观测的 OSB 估计脚本集，含读观测、提取多通道偏差、估计与分析等步骤，并涉及 SINEX 类偏差文件。用户需自行准备测站网观测数据。适合偏差产品研究与教学；生产级 OSB 仍以 IGS/各分析中心产品为主，本库偏算法复现。

## 轨道钟差综合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SPOCC](https://gnss.gfz.de/services/spocc) | SPOCC：多分析中心轨道钟差综合 | Python | — | 🏷️ 官方 核心 |

### 详细说明

#### [SPOCC](https://gnss.gfz.de/services/spocc)  
*🏷️ 官方 核心*

语言：Python · 许可：SPOCC Scientific License v1.0 (proprietary; signed terms + registration, IGS/IAG contributors only) · 星标约：— · 宿主：official_site

GFZ 发布的 Software for Precise Orbit and Clock Combination，用方差分量估计对多家分析中心 SP3/CLK 做多星座加权综合，并提供 Docker。面向 IGS 组合与 PPP 用户产品试验，不是单站 PPP 引擎。发布见 IGSMAIL-8560（2025-01-24）与 GFZ 所属部门新闻页。服务页公布 SPOCC Scientific License v1.0：须签署条款登记后才能访问 git.gfz-potsdam.de/gnss/spocc，仅限对 IGS/IAG 有贡献的机构，运营中不得给非 IGS 产品加权，并非 OSI 开源。

## 轨道确定/基础库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Orekit](https://github.com/CS-SI/Orekit) | Orekit：开源太空动力学与轨道传播基础库 | Java | 298 | 🏷️ 个人社区 |
| [orbdetpy](https://github.com/ut-astria/orbdetpy) | orbdetpy：Python/Java 轨道确定开源工具 | Java | 129 | 🏷️ 高校实验室 |
| [GMAT](https://github.com/nasa/GMAT) | NASA 通用任务分析工具 GMAT：开源轨道设计、传播与估计（含 GNSS/测距观测）平台 | C++ | 112 | 🏷️ 官方 |
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

#### [GMAT](https://github.com/nasa/GMAT)  
*🏷️ 官方*

语言：C++ · 许可：Apache-2.0 · 星标约：112 · 宿主：github

NASA 戈达德主导的 General Mission Analysis Tool 的官方 GitHub 仓库，Apache-2.0 许可，C++ 实现并带脚本语言与 GUI。可做高精度轨道传播（多体引力、大气阻力、光压）、机动优化以及批处理/扩展卡尔曼滤波轨道确定，估计模块支持 GPS 伪距、DSN 测距测速等观测。对 GNSS 用户而言可用于低轨卫星星载 GNSS 定轨实验、可见性与覆盖分析。仓库根 README 较简，安装与构建说明在 application 目录；发行包另见 SourceForge。

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

汇总 IGS Bias and Calibration 工作组活动，面向差分码偏差、可观测量特定偏差（OSB）及校准议题。对 PPP-AR、多系统组合与钟差产品一致性很关键。页面为活动与文档入口，具体偏差文件仍从 IGS 产品树获取。引用请注明产品来源与版本。

## 时标产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BIPM-Time-FTP](https://www.bipm.org/en/time-ftp) | BIPM 时间 FTP：UTC/UTCr/TT(BIPM) 等时标产品入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BIPM-Time-FTP](https://www.bipm.org/en/time-ftp)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

国际计量局时间部门提供的 FTP/产品入口，涵盖 UTC、快速 UTC 与 TT(BIPM) 等时标文件，是 GNSS 时间比对、CGGTTS 与实验室钟差溯源的常用上游。页面说明访问方式与目录结构，实际文件经 FTP 拉取。时标修订与通告需对照 BIPM Circular T。

## EOP与参考系

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IERS-Datacenter](https://datacenter.iers.org/) | IERS 数据中心：EOP、地球物理流体与公报入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IERS-Datacenter](https://datacenter.iers.org/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

国际地球自转与参考系统服务（IERS）数据中心，提供地球定向参数（EOP）、地球物理流体、参考系相关下载、公报与简易分析工具。GNSS 精密定位与轨道确定常需对齐 EOP/时标。页面为目录与工具入口，具体文件按产品说明获取。请遵守 IERS 数据政策与引用格式。

## EOP产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IERS-EOP-PC](https://hpiers.obspm.fr/eop-pc/) | IERS 地球定向参数产品中心（巴黎天文台） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IERS-EOP-PC](https://hpiers.obspm.fr/eop-pc/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IERS EOP Product Center 门户，面向地球定向参数序列与相关说明，由巴黎天文台维护。与 IERS Datacenter 互补：本站偏 EOP 产品中心视角。精密 GNSS/VLBI/SLR 联合分析常用其序列。选用哪套 EOP 产品需对照分析策略与时效。

## 轨道根数

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CelesTrak-NORAD-GP](https://celestrak.org/NORAD/elements/) | CelesTrak 当前 NORAD/GP 轨道根数下载入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [CelesTrak-NORAD-GP](https://celestrak.org/NORAD/elements/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CelesTrak 提供的现行 GP（原 TLE）轨道根数获取页，含查询与专题数据说明，广泛用于卫星可见性与简易轨道预报。与 SpaceData 页互补：本页偏 GP 元素集。根数精度有限，不替代精密星历。

## SGP4传播

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [python-sgp4](https://github.com/brandon-rhodes/python-sgp4) | python-sgp4：Python SGP4/SDP4 由 TLE/OMM 传播位置 | Python | 472 | 🏷️ 个人社区 |

### 详细说明

#### [python-sgp4](https://github.com/brandon-rhodes/python-sgp4)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：472 · 宿主：github

经典 SGP4 的 Python 实现，MIT 许可，广泛用于由 TLE/OMM 传播卫星位置与速度。服务可见性、简易碰撞预警与教学，精度不及精密星历。与 CelesTrak GP 数据常配合使用。星数高、维护活跃，是 Python 轨道传播常用依赖。

## SGP4-JS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [satellite-js](https://github.com/shashwatak/satellite-js) | satellite-js：JavaScript/TypeScript SGP4/SDP4 轨道传播 | TypeScript | 1091 | 🏷️ 个人社区 |

### 详细说明

#### [satellite-js](https://github.com/shashwatak/satellite-js)  
*🏷️ 个人社区*

语言：TypeScript · 许可：MIT · 星标约：1091 · 宿主：github

模块化 JS/TS 实现的 SGP4/SDP4，用于浏览器或 Node 中传播 TLE/OMM，MIT 许可，星数很高。适合 Web 可见性可视化与前端演示，非测地精密轨道。输入根数时效与来源影响结果。补齐前端 GNSS/卫星几何工具链缺口。

## 可微SGP4

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [dSGP4](https://github.com/esa/dSGP4) | dSGP4：ESA 可微分 SGP4（机器学习友好） | Python | 97 | 🏷️ 官方 |

### 详细说明

#### [dSGP4](https://github.com/esa/dSGP4)  
*🏷️ 官方*

语言：Python · 许可：GPL-3.0 · 星标约：97 · 宿主：github

ESA 先进概念团队（ACT）成员在 ESA GitHub 组织发布的可微分 SGP4（PyTorch），对应 Acciarini、Baydin、Izzo 发表在 Acta Astronautica（2025）的论文。GPL-3.0，pip/conda 可装：可对时间和 TLE 参数求梯度，支持批量传播、TLE/OMM 读写，并含学习 SGP4 修正的混合模型 mldsgp4。用于状态转移矩阵、协方差传播与基于梯度的定轨；精度仍属 SGP4 族，不是精密轨道。

## SGP4-Rust

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sgp4-rs](https://github.com/neuromorphicsystems/sgp4) | sgp4-rs：Rust SGP4 卫星轨道传播（crates.io） | Rust | 120 | 🏷️ 高校实验室 |

### 详细说明

#### [sgp4-rs](https://github.com/neuromorphicsystems/sgp4)  
*🏷️ 高校实验室*

语言：Rust · 许可：MIT · 星标约：120 · 宿主：github

Rust 语言的 SGP4 传播实现，MIT 许可，便于嵌入式或高性能服务中做 TLE 传播。与 python-sgp4/satellite-js 形成多语言对照。协议与模型版本需与输入根数一致。适合 Rust GNSS/航天工具链开发者集成。

## 时标FTP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BIPM-WebTAI-FTP](https://webtai.bipm.org/ftp/) | BIPM 时间部门 WebTAI FTP：时标文件目录入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BIPM-WebTAI-FTP](https://webtai.bipm.org/ftp/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

BIPM Time Department 的 FTP 索引页，指向 pub 等时标相关目录，是 UTC/TAI 等文件的机器可达入口。与 BIPM-Time-FTP 说明页互补：本页偏目录浏览。

## 产品门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CDDIS-Orbit-Clock-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/orbit_and_clock_products.html) | NASA CDDIS：GNSS 轨道与钟差产品说明页 | data-portal | — | 🏷️ 官方 |
| [ESA-Navigation-Support-Office](https://navigation-office.esa.int/) | ESA OPS-GN：导航支持办公室门户 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [CDDIS-Orbit-Clock-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/orbit_and_clock_products.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CDDIS 对 IGS 等精密轨道（SP3）与钟差（CLK）产品的说明入口；站点提示已向 earthdata.nasa.gov 迁移。与 CDDIS 大气/IONEX/高采样页互补，本页专指轨道钟差派生产品文档。下载现多走 Earthdata；需遵守 NASA 账号与引用条款。

#### [ESA-Navigation-Support-Office](https://navigation-office.esa.int/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

ESA Navigation Support Office（OPS-GN）公开门户，介绍导航支持活动、产品与出版物入口。面向 GNSS 精密产品与任务支持用户，与 GSSC/Navipedia 等 ESA 导航资源互补。页面偏 JS 应用。

## VLBI/EOP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IVS-IVSOPAR](https://ivsopar.obspm.fr/) | 巴黎天文台 IVS 分析中心：大地测量 VLBI 产品门户 | data-portal | — | 🏷️ 官方 |
| [IVSCC](https://ivscc.gsfc.nasa.gov/) | IVS 协调中心：国际 VLBI 服务主站 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IVS-IVSOPAR](https://ivsopar.obspm.fr/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Observatoire de Paris 托管的 IVS 大地测量 VLBI 分析服务门户，提供 VLBI 解算与地球定向相关产品入口。轨道/参考框架与 EOP 用户可与 IERS EOP、GNSS 框架联合使用。产品级别与引用见 IVS/巴黎天文台说明。

#### [IVSCC](https://ivscc.gsfc.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

International VLBI Service 协调中心门户，介绍观测计划、台站网、数据产品与技术文件。与巴黎 IVSOPAR 分析中心互补，本站偏服务协调与总入口。EOP/TRF 与 GNSS 框架联合用户常用。

## 轨道动力学

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [nyx](https://github.com/nyx-space/nyx) | Nyx：高保真快验的 Rust 宇航动力学工具库 | Rust | 490 | 🏷️ 个人社区 |

### 详细说明

#### [nyx](https://github.com/nyx-space/nyx)  
*🏷️ 个人社区*

语言：Rust · 许可：AGPL-3.0 · 星标约：490 · 宿主：github

nyx-space 维护的 Rust 宇航动力学工具包，AGPL-3.0，星标近五百。覆盖轨道传播、定轨与任务分析等，可与 GNSS 精密轨道/钟差产品对照或做仿真前端。偏航天动力学而非 GNSS 观测解算；许可证对闭源集成有约束。

## SLR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ILRS](https://ilrs.gsfc.nasa.gov/) | ILRS：国际激光测距服务主站（IAG） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [ILRS](https://ilrs.gsfc.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

International Laser Ranging Service 官方门户，组织 SLR 网络、产品与会议信息，服务地球动力学与精密轨道。与 GNSS 精密定轨/参考框架联合解算相关，可补 IVS/IGS 空间大地测量链条。美国政府停摆期间可能暂停更新。
