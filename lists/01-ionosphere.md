# 电离层 / Ionosphere
> **247** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

电离层研究软件：GNSS 双频 TEC 估计、GIM/IONEX 处理、TEC 预报（含机器学习）、闪烁/ROTI、TID、层析、掩星与法拉第旋转。也收录 IRI/NeQuick 等电离层模型、MSIS/HWM 中性大气模型、测高仪与雷达/ISR 工具、HF 射线追踪和磁坐标库；电离层产品与空间天气数据门户已移至「GNSS 数据源」。

## 数据接口

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [viresclient](https://github.com/ESA-VirES/VirES-Python-Client) | viresclient：ESA VirES Python 客户端（Swarm） | Python | 23 | 🏷️ 官方 |
| [geomagindices](https://github.com/space-physics/geomagindices) | geomagindices：地磁指数 Python 读写工具 | Python | 17 | 🏷️ 个人社区 |
| [madrigalWeb](https://github.com/MITHaystack/madrigalWeb) | OpenMadrigal/CEDAR Python 数据客户端 | Python | 4 | 🏷️ 高校实验室 |
| [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader) | swds-api-downloader：Embrace SWDS API 自动下载示例 | Python | 4 | 🏷️ 官方 |
| [digisondeindices](https://github.com/sunipkm/digisondeindices) | 从 GIRO DIDBase 下载并解析 Digisonde 标定参数为 xarray 的 Python 工具 | Python | 2 | 🏷️ 个人社区 |
| [Ionosonde-Data-Downloader](https://github.com/bzossi/Ionosonde-Data-Downloader) | 自动拉取公共测高仪库数据的轻量脚本 | Python | 2 | 🏷️ 个人社区 |
| [IRTS_SDK](https://github.com/1acheng/IRTS_SDK) | IRTS_SDK：ionosphere.cn 实时电离层服务客户端 | — | 2 | 🏷️ 个人社区 |
| [ismr_downloader](https://github.com/GEGE-UNESP/ismr_downloader) | ismr_downloader：ISMR 闪烁监测数据命令行下载器 | Python | 1 | 🏷️ 高校实验室 |

### 详细说明

#### [viresclient](https://github.com/ESA-VirES/VirES-Python-Client)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：23 · 宿主：github

官方推荐的 Swarm（及 Aeolus）数据访问库，可按需拉取 EFI Langmuir 探针、TECxTMS_2F 绝对/相对 TEC、以及 CHAMP/GRACE 等扩展 TEC/Ne 产品并载入 pandas/xarray。做 LEO POD 衍生 TEC 与就地电子密度对照时几乎是默认入口。需 VirES 账号；本身不做反演，只负责服务端点与本地装载。

#### [geomagindices](https://github.com/space-physics/geomagindices)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：17 · 宿主：github

space-physics 维护的指数下载与解析工具，按时间返回 Ap、Kp 与 F10.7（含平滑值）的 pandas 表，缺测为 NaN，常作电离层/空间天气研究的辅助输入。MIT 许可，有 Zenodo DOI；与 igrf、iri2016 等模型接口互补。README 自述 2018 年后的新数据源读取器尚待补充，使用前请核对所需时段是否覆盖。

#### [madrigalWeb](https://github.com/MITHaystack/madrigalWeb)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

访问全球 Madrigal 站点（含 CEDAR）的官方 Python 客户端，可检索/下载非相干散射雷达、GNSS TEC 等空间天气与电离层归档。MIT。适合批量脚本拉取；需遵守各站点数据政策，部分实验需注册。配套门户见 OpenMadrigal。

#### [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

演示如何调用 Embrace 空间天气数据服务（SWDS）API 自动下载产品，方便把取数写进科研脚本。适合 GNSS—空间天气交叉研究的数据入口。接口字段、鉴权与限流可能随官方升级变化；时间范围与产品类型以站点文档为准，勿长期硬编码过期端点。

#### [digisondeindices](https://github.com/sunipkm/digisondeindices)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

个人开发者发布的 Python 小工具，MIT 许可。按时间与台站代码从 Lowell GIRO 的 DIDBase 获取 Digisonde 自动/人工标定参数，包括 foF2、foF1、foE、hmF2、MUFD、半厚度、B0 与测高仪推算 TEC 以及自动标定置信度，统一输出为 xarray Dataset，缺测时返回空数据集。适合把测高仪参数批量接入 IRI 对比、TEC 校验或机器学习流程。功能单一、星标少，依赖 DIDBase 在线服务，使用时请遵守 GIRO 数据政策。

#### [Ionosonde-Data-Downloader](https://github.com/bzossi/Ionosonde-Data-Downloader)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

按站点/时间从公共测高仪仓库批量下载，减少手工翻目录。适合底部电离层档案收集。上游目录或接口变更会导致脚本失效；不做描迹反演或质量控制，需另接 Autoscala/SAO 等工具。

#### [IRTS_SDK](https://github.com/1acheng/IRTS_SDK)  
*🏷️ 个人社区*

语言：— · 许可：GPL-3.0 · 星标约：2 · 宿主：github

面向 ionosphere.cn 实时电离层服务的 C/C++ SDK，封装连接与 TEC 获取，便于导航终端做单频改正演示。输入为服务端连接参数与查询位置/时间；输出为实时 TEC/延迟相关量。局限：依赖云服务可用性与账号策略；不是离线开源模式本体。

#### [ismr_downloader](https://github.com/GEGE-UNESP/ismr_downloader)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

从 ISMR Query Tool API 拉取 GNSS/ISMR 闪烁监测数据的命令行下载器。适合批量建闪烁样本库。依赖上游 API 可用性与账号策略；本地下载后需自行做质控。

## 层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoTomo](https://github.com/Joshuaalbert/IonoTomo) | IonoTomo：射电天文射线追踪与电离层层析仿真 | Jupyter Notebook | 11 | 🏷️ 个人社区 |
| [iono-tomography](https://github.com/brianbreitsch/iono-tomography) | iono-tomography：电离层层析 Python 实验原型 | Python | 4 | 🏷️ 个人社区 |
| [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl) | synthetic_ionospheric_tomography_isl：多 GNSS 星间链路层析仿真 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [317Lab-tomography](https://github.com/317Lab/tomography) | 317Lab-tomography：Lynch 火箭实验室电离层层析代码 | Jupyter Notebook | 1 | 🏷️ 高校实验室 |
| [GNSS_TOM](https://github.com/sailvssea/GNSS_TOM) | GNSS_TOM：GNSS 对流层与电离层层析 C++（仿 GPSTk 风） | C++ | 1 | 🏷️ 个人社区 |
| [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy) | 层析几何矩阵构建（C++，yujieqing） | C++ | — | 🏷️ 个人社区 ★ |
| [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation) | SegmentsComputation：体素层析射线段矩阵（已归档） | C++ | 0 | 🏷️ 个人社区 |

### 详细说明

#### [IonoTomo](https://github.com/Joshuaalbert/IonoTomo)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：11 · 宿主：github

结合射线追踪与射电观测仿真做电离层层析，面向射电天文与空间天气交叉课题，Notebook 形式便于改参数。适合需要正演电离层对射电信号影响的人。不是 GNSS 双频 TEC 业务软件；地基 GNSS 体素层析可并行参考 SegmentsComputation 与 synthetic 层析仓库。仿真假设与真实射电阵几何差异需要单独评估。仓库已于 2020-11 归档（只读）。

#### [iono-tomography](https://github.com/brianbreitsch/iono-tomography)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：4 · 宿主：github

开源层析实验代码，便于搭建体素/基函数反演原型。输入为 STEC 与几何；输出为电子密度反演结果。局限：文档与完整度需自行评估；工程稳健性弱于商业/大型实验室系统。

#### [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：2 · 宿主：github

仿真多 GNSS 星间链路（ISL）辅助的电离层层析，探索新观测几何对电子密度反演的贡献。适合读相关论文后复现实验设置与几何配置。公开星标低、偏研究原型，落地需自备真实 ISL 或地基数据接口；可与 SegmentsComputation、IonoTomo 对照正演与矩阵环节。仿真噪声模型应尽量贴近目标星座链路预算。

#### [317Lab-tomography](https://github.com/317Lab/tomography)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：— · 星标约：1 · 宿主：github

火箭/地基联合场景下的电离层层析教学与研究代码。输入为层析观测几何与 TEC；输出为二维/三维重建。局限：星数少、场景专用；需对照实验室文档。

#### [GNSS_TOM](https://github.com/sailvssea/GNSS_TOM)  
*🏷️ 个人社区*

语言：C++ · 许可：LGPL-3.0 · 星标约：1 · 宿主：github

同时面向对流层水汽与电离层 TEC 的层析代码，C++ 实现并参考 GPSTk 风格。输入为 GNSS 相关观测量/几何；输出层析体素场。局限：星数低、文档少；电离层与对流层模块成熟度需实测；许可为 LGPL-3.0。

#### [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：GPL-3.0 · 星标约：— · 宿主：github

yujieqing 仓库：为电离层层析准备几何/射线矩阵相关代码，可与同作者 SegmentsComputation 等配合。偏矩阵构造环节，不是完整层析反演或 TEC 预处理流水线；仓库活跃度与文档需自行评估。

#### [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：0 · 宿主：github

专注层析反演里体素穿越段（segment）几何矩阵的 C++ 实现，是三维电子密度反演的前置数值模块。仓库已于 2021-09 归档（只读）；yxw027 同名仓为相同文件树副本，目录已去重只留本仓。不是完整层析软件，需自备观测方程与正则化。

## 电离层与PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PPP-RTK-Ionosphere](https://github.com/nickdaychen/PPP-RTK-Ionosphere) | PPP-RTK-Ionosphere：MATLAB PPP-RTK 与电离层试验 | MATLAB | 7 | 🏷️ 个人社区 |
| [AETHER](https://github.com/LiZhengXiao99/AETHER) | AETHER：PPP-RTK 区域 STEC/VTEC 与 ZWD/ZTD 建模 | C++ | 6 | 🏷️ 个人社区 |
| [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP) | WA_ion_model_PPP：广域电离层约束进 PPP 的实践代码 | C++ | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [PPP-RTK-Ionosphere](https://github.com/nickdaychen/PPP-RTK-Ionosphere)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：7 · 宿主：github

围绕 PPP-RTK 与电离层约束/改正的 MATLAB 试验代码，便于改映射函数与随机模型做对比实验。适合课堂与方法验证。仓库说明偏少，输入改正产品与参考真值需自行准备；实时流与多星座完备性不是其主场。

#### [AETHER](https://github.com/LiZhengXiao99/AETHER)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：6 · 宿主：github

从 GNSS 观测抽取大气延迟，构建区域 STEC/VTEC 与 ZWD/ZTD 模型以增强 PPP-RTK 收敛与精度。适合研究大气约束对网络 RTK/PPP-RTK 的贡献。结果依赖测站网密度与初始解质量；不能替代全球 GIM 或官方对流层格网产品。

#### [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：— · 宿主：github

把广域电离层模型和 PPP 联系起来的实践代码，适合看电离层约束如何进精密单点。完整度与星座支持需实测；系统级 PPP 仍建议对照 PRIDE、Ginan、raPPPid。

## 模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ppigrf](https://github.com/IAGA-VMOD/ppigrf) | IAGA V-MOD 工作组托管的纯 Python IGRF 地磁参考场计算库 | Python | 80 | 🏷️ 官方 |
| [igrf](https://github.com/space-physics/igrf) | igrf：IGRF13 地磁模型 Python/Matlab 接口 | Python | 77 | 🏷️ 个人社区 |
| [GEMINI3D](https://github.com/gemini3d/gemini3d) | GEMINI3D：三维电离层物理模式 | Fortran | 69 | 🏷️ 高校实验室 |
| [ChaosMagPy](https://github.com/ancklo/ChaosMagPy) | 丹麦技术大学 CHAOS 地磁场模型的 Python 计算包 | Python | 34 | 🏷️ 高校实验室 |
| [wmm2020](https://github.com/space-physics/wmm2020) | wmm2020：世界磁模型 WMM2020 Python 接口 | Python | 29 | 🏷️ 个人社区 |
| [GITM](https://github.com/GITMCode/GITM) | GITM：全球电离层-热层模式社区 Fortran 源码 | Fortran | 28 | 🏷️ 高校实验室 |
| [Aether-IT-model](https://github.com/AetherModel/Aether) | Aether：热层-电离层耦合物理模式（非 PPP-RTK AETHER） | C++ | 27 | 🏷️ 高校实验室 |
| [TIE-GCM](https://github.com/NCAR/tiegcm) | TIE-GCM：NCAR 热层-电离层-电动力学环流模式 | Fortran | 27 | 🏷️ 官方 |
| [LongwaveModePropagator.jl](https://github.com/fgasdia/LongwaveModePropagator.jl) | LongwaveModePropagator.jl：VLF 长波模传播 Julia 模型 | Julia | 26 | 🏷️ 个人社区 |
| [sami2py](https://github.com/sami2py/sami2py) | sami2py：NRL SAMI2 二维电离层模式的 Python 封装 | Python/Fortran | 21 | 🏷️ 高校实验室 |
| [NCAR-GLOW](https://github.com/space-physics/NCAR-GLOW) | NCAR-GLOW：气辉模型 CMake/Python/Matlab 构建扩展 | Python | 11 | 🏷️ 个人社区 |
| [dvoacap-python](https://github.com/skyelaird/dvoacap-python) | VOACAP/DVOACAP 短波电离层传播预测引擎的 Python 移植版 | Python | 8 | 🏷️ 个人社区 |
| [sami3_gitm](https://github.com/jdhuba/sami3_gitm) | sami3_gitm：Huba 公开 SAMI3/GITM 基础耦合代码 | Fortran | 7 | 🏷️ 官方 |
| [transcar](https://github.com/space-physics/transcar) | transcar：一维沉降电离层 Fortran 模式 | Fortran | 7 | 🏷️ 个人社区 |
| [gcmprocpy](https://github.com/NCAR/gcmprocpy) | gcmprocpy：TIE-GCM / WACCM-X 输出后处理 Python 工具 | Python | 6 | 🏷️ 官方 |
| [mat_gemini](https://github.com/gemini3d/mat_gemini) | mat_gemini：GEMINI 三维电离层模式 MATLAB 核心脚本 | MATLAB | 6 | 🏷️ 高校实验室 |
| [SAMI2](https://github.com/NRL-Plasma-Physics-Division/SAMI2) | SAMI2：NRL 二维电离层模式官方 Fortran 源码 | Fortran | 6 | 🏷️ 官方 |
| [SAMI3-GITM-python](https://github.com/abukowski21/SAMI3-GITM-python) | SAMI3-GITM-python：SAMI3–GITM 耦合输出 Python/Notebook 分析 | Python | 6 | 🏷️ 个人社区 |
| [IPE](https://github.com/NOAA-SWPC/IPE) | IPE：NOAA SWPC 电离层-等离子体层-电动力学模式 | Fortran | 5 | 🏷️ 官方 |
| [AURORA](https://github.com/egavazzi/AURORA) | AURORA：电离层电子输运时变模型（UiT） | MATLAB | 3 | 🏷️ 个人社区 |
| [ntcmg](https://github.com/lguldur/ntcmg) | ntcmg：Galileo NTCM-G 电离层改正 C++ 实现 | C++ | 3 | 🏷️ 个人社区 |
| [pytiegcm](https://github.com/asher-pembroke/pytiegcm) | pytiegcm：TIE-GCM 输出的轻量 Python 读取器 | Python | 3 | 🏷️ 个人社区 |
| [Klobuchar.jl](https://github.com/bukvoj/Klobuchar.jl) | Klobuchar.jl：广播电离层延迟模型的 Julia 实现 | Julia | 2 | 🏷️ 个人社区 |
| [IRI_TID](https://github.com/w2naf/IRI_TID) | IRI_TID：PyIRI 密度场叠加正弦 TID 扰动 | Python | 1 | 🏷️ 高校实验室 |
| [SAMI3-4.00](https://github.com/jdhuba/sami3-4.00) | SAMI3-4.00：作者侧公开的现代化 Fortran 源码 | Fortran | 1 | 🏷️ 官方 |
| [CCMC-SAMI3](https://ccmc.gsfc.nasa.gov/models/SAMI3~3.22) | CCMC 上的 SAMI3 模型入口（文档/运行请求/发布信息） | data-portal | — | 🏷️ 官方 |
| [gri-iono](https://gitlab.com/geosol-foss/python/gri-iono) | gri-iono：跨电离层延迟与角度改正 Python 包 | Python | 0 | 🏷️ 个人社区 |
| [HAO-TGCM-portal](https://www.hao.ucar.edu/modeling/tgcm/) | NCAR HAO TGCM/TIE-GCM 文档与发布说明门户 | data-portal | — | 🏷️ 官方 |
| [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx) | ITU-R-iono-tropo-software：ITU-R 电离层/对流层传播软件与验证数据 | various | — | 🏷️ 官方 |
| [Klobuchar-study-code](https://github.com/KaijingZheng/Klobuchar-ionosphere-model-in-global-navigation-satellite-systems) | Klobuchar-study-code：广播八参数模型评估 MATLAB | MATLAB | 0 | 🏷️ 个人社区 |
| [RIM](https://github.com/SWMFsoftware/RIM) | RIM：SWMF 体系中的 Ridley 高纬电离层模式 | Fortran | 0 | 🏷️ 官方 |
| [SAMI3-3.22-CCMC-mirror](https://github.com/sylee918/SAMI3) | SAMI3-3.22-CCMC-mirror：SAMI3-3.22 Fortran 个人 git 镜像 | Fortran | 0 | 🏷️ 个人社区 |
| [SAMI3-3.22-Zenodo](https://doi.org/10.5281/zenodo.7895858) | SAMI3-3.22-Zenodo：SAMI3 三维电离层/等离子体层模型源码存档 | Fortran | — | 🏷️ 个人社区 |
| [swarm-vip-dynamic-models](https://gitlab.com/KNMI-OSS/spaceweather/libs/swarm-vip-dynamic-models) | swarm-vip-dynamic-models：Swarm 原位 Ne/RODI 的 GLM 经验模型包 | Python | 0 | 🏷️ 官方 |

### 详细说明

#### [ppigrf](https://github.com/IAGA-VMOD/ppigrf)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：80 · 宿主：github

由国际地磁与高空物理协会（IAGA）V-MOD 工作组组织托管的纯 Python IGRF 实现，MIT 许可并有 Zenodo DOI，已跟进 IGRF-14。无需编译 Fortran，即可按时间、地理或地心坐标批量计算地磁场分量，适合嵌入 TEC 投影、磁纬换算、电离层穿刺点磁坐标与闪烁统计等流程。与 space-physics 的 igrf（封装 Fortran）相比依赖更轻、易于部署。仓库附 IGRF 官方参考链接；需要高精度外场模型时应另选 CHAOS 等模型。

#### [igrf](https://github.com/space-physics/igrf)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：77 · 宿主：github

space-physics 对 IGRF13 的 Python/Matlab 接口，常用于电离层/磁层研究与 GNSS 相关地磁校正对照。MIT 许可；与 hwm93、msise00、ocbpy 等空间物理工具互补。模型系数随 IGRF 代际更新，请核对仓库绑定的世代与引用方式。

#### [GEMINI3D](https://github.com/gemini3d/gemini3d)  
*🏷️ 高校实验室*

语言：Fortran · 许可：Apache-2.0 · 星标约：69 · 宿主：github

GEMINI3D 是面向电离层的三维流体电动力学数值模式，用 Fortran 求解等离子体密度、速度与电场等，常用于极光区、不规则体和无线电传播相关的物理仿真。输入通常包括中性大气背景、太阳/地磁驱动与网格配置；输出为三维电子密度与相关场量的时序场。对 GNSS 用户而言，它不是直接从 RINEX 算 TEC 的工具，而是提供物理一致性的电子密度场，可再投影为 STEC/VTEC 做对比实验。局限：需要编译与并行计算资源，参数调校门槛高，不适合当作日常 GIM 生产流水线。

#### [ChaosMagPy](https://github.com/ancklo/ChaosMagPy)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：34 · 宿主：github

DTU Space 研究者维护的 Python 包，主体为 MIT 许可（部分文档示例脚本为 LGPL-3.0），有 Zenodo DOI 与 ReadTheDocs 文档，可 pip 安装。用于计算 CHAOS 系列地磁场模型（基于 Swarm、CHAMP 等卫星与观测台数据）的内源场、外源磁层场及其时变，也可读取其他球谐模型系数。相比 IGRF 时间分辨率更高、含外源场，适合精细磁坐标换算与电离层电流分析。模型系数文件需从 DTU 网站另行下载。

#### [wmm2020](https://github.com/space-physics/wmm2020)  
*🏷️ 个人社区*

语言：Python · 许可：public-domain · 星标约：29 · 宿主：github

space-physics 对 NOAA/NGA World Magnetic Model 2020 的 Python 封装，用于磁偏角/磁倾角等计算，辅助导航与电离层相关研究。上游 WMM 源码为美国政府公有领域；封装层许可见仓库。注意模型有效年代，过期后应换用更新的 WMM 世代。

#### [GITM](https://github.com/GITMCode/GITM)  
*🏷️ 高校实验室*

语言：Fortran · 许可：Apache-2.0 · 星标约：28 · 宿主：github

GITM（Global Ionosphere/Thermosphere Model）是广泛使用的全球三维热层-电离层模式，源码以 Fortran 为主，可在社区组织 GITMCode 下获取。用于风暴期、极光加热、电子密度扰动等过程研究；输出 netCDF/二进制场，常与 Kamodo、自研插值脚本对接做卫星轨道飞越或 GNSS 射线对比。局限：编译与输入驱动（太阳指数、高纬强迫等）复杂；与 aaronjridley/GITM 等镜像存在并行维护情况，选用时注意版本与补丁一致性。

#### [Aether-IT-model](https://github.com/AetherModel/Aether)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：27 · 宿主：github

AetherModel/Aether 是热层/电离层耦合的第一性原理模式（C++），面向空间天气与电离层物理过程仿真，与目录里已有的 LiZhengXiao99/AETHER（区域 STEC/VTEC/对流层延迟建模）完全不是同一软件。适用于需要自洽中性-离子耦合输出的研究。局限：部署与算力要求高，文档与输入数据准备有门槛；做 GNSS 测地应用前通常还要额外做射线积分或映射。

#### [TIE-GCM](https://github.com/NCAR/tiegcm)  
*🏷️ 官方*

语言：Fortran · 许可：NCAR TIE-GCM academic research licence (non-commercial, no operational use) · 星标约：27 · 宿主：github

TIE-GCM 是 NCAR HAO 发展的三维耦合热层-电离层-电动力学 GCM，GitHub 上现为官方开源仓库（含 src、scripts、tiegcmrun）。输入需配套数据文件（太阳、地磁、边界等），输出 netCDF 压力层/高度场。GNSS 研究里常拿来做风暴期 TEC/电子密度对照或数据同化背景。局限：需要 Fortran/MPI/netCDF 与较大输入数据集；业务化改正仍多用 IRI/NeQuick/GIM，而非直接跑 TIE-GCM。

#### [LongwaveModePropagator.jl](https://github.com/fgasdia/LongwaveModePropagator.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：26 · 宿主：github

用 Julia 模拟 VLF 在地球-电离层波导中的模态传播，服务低电离层与远距 VLF 研究，和 GNSS L 波段 TEC 工具链互补。局限：领域偏 VLF；对 GNSS 测地用户直接用途有限。

#### [sami2py](https://github.com/sami2py/sami2py)  
*🏷️ 高校实验室*

语言：Python/Fortran · 许可：BSD-3-Clause · 星标约：21 · 宿主：github

sami2py 把海军实验室 SAMI2 二维电离层模式包成 Python：可设置经度、年积日等驱动并运行 Fortran 内核，再把输出归档、加载与绘图。相对完整 IRI/NeQuick 气候模型，它更强调沿磁力线的等离子体动力学。输入含经度、日期、可选中性大气缩放与自定义 ExB 漂移等；输出为模式场。局限：依赖 Fortran 编译器；二维近似不覆盖全球三维结构；仓库近年更新偏少。

#### [NCAR-GLOW](https://github.com/space-physics/NCAR-GLOW)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：11 · 宿主：github

为 NCAR GLOW（气辉/电离层相关）基线代码补充 CMake、Meson、Matlab、Python 构建与封装，Apache-2.0。与 pyglow 互补：本仓偏构建与上游对接。运行仍依赖 GLOW 科学代码与输入大气/太阳条件。适合上层大气/气辉与 GNSS 闪烁背景对照实验。

#### [dvoacap-python](https://github.com/skyelaird/dvoacap-python)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：8 · 宿主：github

业余无线电社区将 VE3NEA 的 DVOACAP（Delphi 实现的 VOACAP 短波传播预测引擎）移植为 Python 的项目，MIT 许可。基于 CCIR/URSI 系数的电离层 F2/E 层参数计算最高可用频率、路径损耗与信噪比等，附带与原版对比的回归验证与 CI。虽面向 HF 通信而非 GNSS，但其电离层剖面建模思路可与 IRI、NeQuick 对照，也适合教学演示太阳活动对电离层的影响。README 给出新手安装脚本；数值精度以其验证报告为准，科研使用需自行复核。

#### [sami3_gitm](https://github.com/jdhuba/sami3_gitm)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：7 · 宿主：github

作者仓库提供的 SAMI3 与 GITM 数据接口的基础（vanilla）版本，使用 EUVAC 等驱动，适合追溯耦合实现。局限：偏早期快照；缺少现代文档与测试；生产研究更建议结合 SAMI3-4.00 / GITM 新仓与论文配置。

#### [transcar](https://github.com/space-physics/transcar)  
*🏷️ 个人社区*

语言：Fortran · 许可：Apache-2.0 · 星标约：7 · 宿主：github

Blelly/Lilensten/Zettergren 一维沉降电离层模式，用于粒子沉降加热与密度响应研究。输入为沉降能谱等；输出为一维剖面时序。局限：非全球 GIM；与 GNSS 射线积分需自行耦合。

#### [gcmprocpy](https://github.com/NCAR/gcmprocpy)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：6 · 宿主：github

gcmprocpy 面向 NCAR TIE-GCM 与 WACCM-X 模式输出，做后处理、诊断与可视化，降低直接啃 netCDF 压力层网格的成本。输入为模式标准输出；输出为分析用场量/图。局限：本身不运行模式；强依赖对应模式版本的变量命名与网格约定；WACCM-X 完整源码通常走 CESM 体系，本仓库只覆盖后处理侧。

#### [mat_gemini](https://github.com/gemini3d/mat_gemini)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：6 · 宿主：github

为 GEMINI 离子层模式提供 MATLAB 侧核心脚本（配置、读写、后处理接口）。输入为 GEMINI 工程与网格；输出为可分析的场量。局限：需配合 GEMINI 主程序；与目录中 gemini3d 本体分工不同。

#### [SAMI2](https://github.com/NRL-Plasma-Physics-Division/SAMI2)  
*🏷️ 官方*

语言：Fortran · 许可：CC0-1.0 · 星标约：6 · 宿主：github

Naval Research Laboratory 的 SAMI2（Sami2 is Another Model of the Ionosphere）Fortran 源码，沿磁力线描述低纬—中纬等离子体。输入为经度、季节、太阳活动等；输出为二维密度等场。局限：二维近似；编译与驱动准备有门槛（可与 sami2py 对照）。

#### [SAMI3-GITM-python](https://github.com/abukowski21/SAMI3-GITM-python)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：6 · 宿主：github

围绕 SAMI3–GITM 耦合或对照实验的 Python/Notebook 工具集，便于读场、画图与做简单诊断，而不是完整模式本体。适合已有模式输出、需要快速分析的用户。局限：文档偏少；依赖具体输出格式；不能替代官方模式仓库。

#### [IPE](https://github.com/NOAA-SWPC/IPE)  
*🏷️ 官方*

语言：Fortran · 许可：GPL-3.0 · 星标约：5 · 宿主：github

IPE（Ionosphere Plasmasphere Electrodynamics）由 NOAA 空间天气预测中心开源，描述电离层与等离子体层耦合及电动力学，面向业务与科研的全球电子密度等产品。适合作为物理/半业务背景场，与实测 TEC、闪烁指数对比。局限：配置与耦合运行门槛不低；星数不多、社区文档相对 GITM/TIE-GCM 更散；不宜直接替代经验修正模型做接收机实时改正。

#### [AURORA](https://github.com/egavazzi/AURORA)  
*🏷️ 个人社区*

语言：MATLAB · 许可：GPL-3.0 · 星标约：3 · 宿主：github

描述电离层中电子输运的时间相关模型（MATLAB），用于沉降/能量沉积相关过程理解。输入为驱动与边界条件；输出为电子输运相关场。局限：非 GNSS 测地产品线；配置与物理背景要求较高。

#### [ntcmg](https://github.com/lguldur/ntcmg)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：3 · 宿主：github

按 Galileo OS《NTCM-G Ionospheric Model Description》实现的 NTCM-G 经验改正，与 NeQuick-G 同属单频用户电离层延迟估算路线，但是不同算法族。输入为广播/模型所需系数与链路几何；输出为电离层延迟估计。局限：仓库体量小、星数低；需对照官方 PDF 验证实现完整度；不替代双频无消电离层或 GIM。

#### [pytiegcm](https://github.com/asher-pembroke/pytiegcm)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：3 · 宿主：github

小型 Python reader，方便把 TIE-GCM netCDF 读进分析脚本。适合不想上完整 Kamodo/gcmprocpy 时做快速检查。局限：功能远少于 Kamodo；维护不活跃（约 2022）；变量覆盖需自测。

#### [Klobuchar.jl](https://github.com/bukvoj/Klobuchar.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：2 · 宿主：github

实现 GNSS 单频广播 Klobuchar 模型，便于与广播 α/β 参数对照课堂计算。输入为时间、用户位置、视线方向与八参数；输出为电离层时间延迟。局限：仓库体量很小，功能单一；精度受广播模型本身限制。

#### [IRI_TID](https://github.com/w2naf/IRI_TID)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

先跑 PyIRI 得到三维电子密度，再叠加行进电离层扰动（TID）正弦扰动，切片后可送入 PyLap/PHaRLAP 等 HF 射线程序。服务中纬度 TID/重力波传播研究。局限：扰动为简化解析形式；依赖 PyIRI；不是观测反演 TID 的工具。

#### [SAMI3-4.00](https://github.com/jdhuba/sami3-4.00)  
*🏷️ 官方*

语言：Fortran · 许可：Apache-2.0 · 星标约：1 · 宿主：github

Joe Huba 等在 GitHub 公开的 SAMI3-4.00，基于 3.22 做了现代化整理，属于少有的 SAMI3 可直接 clone 的源码树。用于三维电离层/等离子体层物理仿真。局限：用户手册仍在完善；输入驱动与编译环境需自行摸索；与 CCMC/Zenodo 上的 3.22 发行版并存，科研引用需写清版本。

#### [CCMC-SAMI3](https://ccmc.gsfc.nasa.gov/models/SAMI3~3.22)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NASA CCMC 的 SAMI3~3.22 模型页面，汇总模型说明、版本与社区获取途径，是找 SAMI3 官方发行与 Runs-on-Request 的入口。局限：页面本身不是 git 仓；源码下载可能指向 Zenodo/协议流程；实际算例仍要本地或 CCMC 环境。

#### [gri-iono](https://gitlab.com/geosol-foss/python/gri-iono)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：0 · 宿主：gitlab

gri-iono（PyPI 可装）面向信号穿电离层传播，提供 Bent、IRI、NeQuick2、NeQuickG 等延迟与角度改正接口，偏通信/测控链路而不是 GNSS 测站 TEC 建图。输入为时间、位置、频率与模型开关；输出延迟与角度改正量。局限：源码在 GitLab；部分底层模式仍依赖外部系数/可执行文件；与测地学 GIM/STEC 流水线目标不同。

#### [HAO-TGCM-portal](https://www.hao.ucar.edu/modeling/tgcm/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

HAO 上的 TIE-GCM/TIME-GCM 家族说明、用户指南与发布历史入口，补充 GitHub 源码仓的文档侧。局限：部分老版本下载流程可能仍要邮件注册；以 GitHub NCAR/tiegcm 为当前源码主渠道更合适。

#### [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx)  
*🏷️ 官方*

语言：various · 许可：ITU terms · 星标约：— · 宿主：official_site

国际电联无线电通信部门汇总的电离层与对流层传播预测软件、数据与验证示例入口，涵盖推荐方法相关数字产品。许可与获取按 ITU 条款办理。适合传播与链路预算研究；GNSS 精密定位仍多用 IRI、NeQuick、VMF 等专用实现。

#### [Klobuchar-study-code](https://github.com/KaijingZheng/Klobuchar-ionosphere-model-in-global-navigation-satellite-systems)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：0 · 宿主：github

教学/研究向的 Klobuchar 实现与精度探讨，便于理解 GPS 广播八参数改正。局限：非新品算法库；星数为 0；改进结论需独立验证。

#### [RIM](https://github.com/SWMFsoftware/RIM)  
*🏷️ 官方*

语言：Fortran · 许可：Apache-2.0 · 星标约：0 · 宿主：github

Space Weather Modeling Framework 组件之一，描述高纬电离层电动力学等，常与全球磁层模式耦合。局限：通常作为 SWMF 整体使用；单独跑与输入耦合复杂；许可为 Apache-2.0（密歇根大学版权）。

#### [SAMI3-3.22-CCMC-mirror](https://github.com/sylee918/SAMI3)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：0 · 宿主：github

从 CCMC/Zenodo 体系搬运的 SAMI3-3.22 Fortran 源码镜像，方便 git clone。正式引用仍建议指向 CCMC 模型页或 Zenodo DOI。局限：非官方持续维护仓；体积大；配置与运行说明需回到 CCMC 文档。

#### [SAMI3-3.22-Zenodo](https://doi.org/10.5281/zenodo.7895858)  
*🏷️ 个人社区*

语言：Fortran · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

作者 Joe Huba（Zenodo 署名单位为 Syntek Technologies 公司）在 Zenodo 以 software 类型存档的 SAMI3-3.22 源码包（concept DOI 10.5281/zenodo.7895858），附 sami3-3.22.tgz（约 39 MB）与用户手册。用于全球电离层–等离子体层物理仿真，常与 GNSS TEC/掩星对比。许可 CC-BY-4.0。另有 GitHub 镜像与 CCMC 门户；这里是可直接下载的 Zenodo 软件存档。

#### [swarm-vip-dynamic-models](https://gitlab.com/KNMI-OSS/spaceweather/libs/swarm-vip-dynamic-models)  
*🏷️ 官方*

语言：Python · 许可：BSD-3-Clause · 星标约：0 · 宿主：gitlab

荷兰皇家气象研究所（KNMI）在 GitLab 发布的 Python 包，评估 Swarm VIP Dynamic 项目拟合的广义线性模型，按地理位置、磁纬/地方时、季节、F10.7、Kp/Hp30 与太阳风等输入预测 Ne、RODI 等电离层参数，覆盖赤道至极区。依赖 pandas/numpy，可自动拉取 OMNI/F10.7/Kp。BSD-3-Clause。适合 Swarm 原位气候态对照与不规则性气候研究；非 GNSS TEC 估计器。仓库可公开克隆。

## TEC估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | gnss-tec：RINEX 斜路径 TEC 重建 | Python | 54 | 🏷️ 高校实验室 核心 |
| [PyGPS](https://github.com/gregstarr/PyGPS) | PyGPS：RINEX→TEC/偏差研究工具箱 | Python | 47 | 🏷️ 个人社区 |
| [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB) | TEC-calculation-MATLAB：双频 RINEX 2.11 TEC | MATLAB | 33 | 🏷️ 高校实验室 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | PyTECGg：多星座 TEC 重建与校准 | Python | 29 | 🏷️ 个人社区 🔀 ★ 核心 |
| [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | ALBUS_ionosphere：GPS 估计 TEC 与法拉第旋转量 RM | Python | 26 | 🏷️ 个人社区 |
| [tec-suite](https://github.com/gnss-lab/tec-suite) | tec-suite：SIMuRG 团队斜向 TEC 重建软件 | Python | 23 | 🏷️ 高校实验室 |
| [pygnss-tec](https://github.com/eureka-0/pygnss-tec) | pygnss-tec：RINEX 读数与 TEC 计算（Rust 加速） | Python | 16 | 🏷️ 个人社区 |
| [VARION](https://github.com/giorgiosavastano/VARION) | VARION：变分法实时电离层监测（Savastano 个人仓） | Python | 15 | 🏷️ 个人社区 |
| [gsit](https://github.com/aldebaran1/gsit) | GSIT：TEC/ROTI/IPP 与光学磁力计 Python 工具 | Python | 10 | 🏷️ 个人社区 |
| [ionotec](https://github.com/sylvathle/ionotec) | ionotec：从 RINEX 计算 TEC 的轻量 Python 库 | Python | 6 | 🏷️ 个人社区 |
| [TEC_calculation_RINEX3](https://github.com/cssrg-kmitl/TEC_calculation_RINEX3) | TEC_calculation_RINEX3：RINEX 3.04 双频 TEC/ROTI（MATLAB） | MATLAB | 6 | 🏷️ 高校实验室 |
| [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation) | TEC_gradient_computation：单/双频电离层延迟梯度估计 | MATLAB | 6 | 🏷️ 高校实验室 |
| [MyIonosphere_Library](https://github.com/mguerra96/MyIonosphere_Library) | MyIonosphere_Library：相位 GFLC 与 IPP 的 MATLAB 函数库 | MATLAB | 4 | 🏷️ 个人社区 |
| [tec-example](https://github.com/embrace-inpe/tec-example) | tec-example：INPE Embrace TEC 处理示例 | Python | 3 | 🏷️ 官方 |
| [ESA-UGI](https://essr.esa.int/project/unified-gnss-ionosphere) | ESA-UGI：多系统 GNSS 估 vTEC/IFB/模糊度（ESSR） | unknown | — | 🏷️ 官方 |
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | Get_IPP：电离层穿刺点（IPP）C++ 计算 | C++ | — | 🏷️ 个人社区 ★ |
| [GNSS-Workshop-TEC](https://github.com/breid-phys/GNSS-Workshop) | GNSS-Workshop-TEC：研讨班 GNSS 探索到 TEC 测量材料 | Python | 0 | 🏷️ 个人社区 |
| [Heki-GNSS-TEC-Software](https://www.ep.sci.hokudai.ac.jp/~heki/software.htm) | Heki 公开 Fortran：L4/STEC 与电离层层析 | Fortran | — | 🏷️ 高校实验室 |
| [IONOLAB-TEC-Software](https://www.ionolab.org/index.php?language=en&page=ionolabtec) | IONOLAB-TEC：土耳其实验室 GNSS TEC/STEC 估计软件 | unknown | — | 🏷️ 高校实验室 |
| [KOH2-ionosphere](https://github.com/asparuhkamburov/KOH2-ionosphere) | KOH2-ionosphere：南极 KOH2 站 TEC 与太阳周 25 分析 | Python | 0 | 🏷️ 个人社区 |
| [Okoh-MATLAB-TEC-from-RINEX](https://doi.org/10.5281/zenodo.7711905) | Okoh-MATLAB-TEC-from-RINEX：RINEX 提 TEC 的 MATLAB 集 | MATLAB | — | 🏷️ 高校实验室 |
| [quakeion](https://github.com/Gm015555/quakeion) | quakeion：震例目录 + CODE GIM TEC/ROT/ROTI 分析 | Python | 0 | 🏷️ 个人社区 |
| [Seemala-GPS-TEC](https://seemala.blogspot.com/2026/08/gps-tec-analysis-program-version-37.html) | Seemala GPS-TEC：RINEX 估计 GPS TEC（Windows） | Windows/Exe | — | 🏷️ 个人社区 |
| [vtec](https://github.com/mfkiwl/vtec) | vtec：多 GNSS 球谐全球电离层图与 DCB 估计（C++） | C++ | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [gnss-tec](https://github.com/gnss-lab/gnss-tec)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：54 · 宿主：github

SIMuRG/gnss-lab 系经典 STEC 重建库，输入 RINEX 相位与伪距，输出斜路径 TEC，MIT 许可友好。适合论文复现与批处理建站网 TEC。GIM 成图、闪烁指数需另接 mosgim/OASIS 等；DCB 处理策略要按数据源核对。

#### [PyGPS](https://github.com/gregstarr/PyGPS)  
*🏷️ 个人社区*

语言：Python · 许可：AGPL-3.0 · 星标约：47 · 宿主：github

把读 RINEX、存 HDF5、算 TEC、卫星位置与接收机/卫星偏差串在一起，偏研究原型。适合快速探索。AGPL 较严；长期维护与测试覆盖不如专门 TEC 库，关键步骤建议交叉验证。README 注明 2020-08 起不再维护，功能并入 gsit，读 RINEX 建议改用 georinex。

#### [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：33 · 宿主：github

基于双频接收机观测在 MATLAB 里算 TEC，输入偏 RINEX 2.11/GPS，教学友好。适合本科实验与快速验证。多星座、RINEX 3/4 与现代化 DCB 产品支持有限；科研产线建议再接 PyTECGg 等。

#### [PyTECGg](https://github.com/viventriglia/PyTECGg)  
*🏷️ 个人社区 🔀 ★ 核心*

语言：Python · 许可：GPL-3.0 · 星标约：29 · 宿主：github

从 RINEX 做多星座 TEC 重建与接收机/卫星偏差相关校准，Rust 核心加快批处理。适合需要可编程 TEC 流水线、又想兼顾性能的研究组。Atlas2001-web 已 fork。GPL 许可需注意与闭源流程衔接；与 gnss-tec、tec-suite 比，更偏「可嵌入 Python 生态」。

#### [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-2.0-or-later · 星标约：26 · 宿主：github

面向射电天文/地空链路，从 GPS 接收机数据估 TEC 与法拉第旋转相关量。适合需要 TEC+RM 联合的场景。通用 GNSS 多星座精密 TEC 流水线不是其主场；协议与输入格式需按仓库说明准备。

#### [tec-suite](https://github.com/gnss-lab/tec-suite)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：23 · 宿主：github

SIMuRG 团队的 tec-suite 读 RINEX 2/3 观测（含 Hatanaka 与 .Z/.gz 压缩）和导航文件，按站按卫星输出斜向 TEC 序列，支持 GPS/GLONASS/Galileo/BeiDou/GEO/IRNSS，提供 Windows/Linux/macOS 预编译包。本身不做 VTEC 格网或 GIM 建模，成图要接后续工具；GPL 约束与文档深度因版本而异，轻量嵌入可优先 gnss-tec。

#### [pygnss-tec](https://github.com/eureka-0/pygnss-tec)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

Python 包读 RINEX 并算 TEC，关键路径用 Rust 加速，和 PyTECGg 同属「Py+加速核」路线。适合中等规模批处理。社区体量小于 gnss-tec；算法假设（映射、DCB）使用前要读文档核对。

#### [VARION](https://github.com/giorgiosavastano/VARION)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：15 · 宿主：github

Giorgio Savastano 个人仓发布的变分法电离层观测工具（方法源自罗马一大 Sapienza 相关论文），读取 RINEX 观测/广播星历估计 slant TEC 变化，用于站级近实时扰动监测（如海啸电离层扰动）。Python+NumPy/Pandas，GPL-3。适合单站高频 TEC 扰动教学与案例复现；依赖较旧的 Python 2.7+ 生态，需自行准备导航文件与站坐标。

#### [gsit](https://github.com/aldebaran1/gsit)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：10 · 宿主：github

面向电离层社区的 Python 框架（MIT）：双频伪距/相位 TEC、相位改正 TEC、ROTI、薄壳 VTEC、IPP，以及卫星 AER/WGS84 位置；并含全天空成像与 IPP 叠置、三轴磁力计 HDZ↔XYZ、OMNIWeb IMF 读取与轨迹绘图。适合教学与多传感器对照原型。仓库近年少更新（约 2017 推送），依赖与 RINEX 版本覆盖需自行验证；不是生产级 GIM/PPP 引擎。

#### [ionotec](https://github.com/sylvathle/ionotec)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

面向 RINEX 观测的 TEC 计算库（原 pytec 更名/迁移至 ionotec），补齐“读观测→几何无关组合→TEC”的轻量路径。适合快速脚本化实验。功能面小于 PyTECGg/tec-suite 一类完整标定流水线；多星座 DCB/硬件延迟处理需自行核对。

#### [TEC_calculation_RINEX3](https://github.com/cssrg-kmitl/TEC_calculation_RINEX3)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

泰国 KMITL CSSRG 实验室程序，由双频 RINEX 3 计算 STEC/VTEC、DCB 与 ROTI，主入口 ProcessTECCalculation.m。输入为观测/星历等；输出为一日 TEC 结构与 ROTI。局限：依赖 Linux/Cygwin 命令环境；主要面向 GPS 双频教学实验。

#### [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

从 RINEX 估计电离层延迟梯度，服务于 GBAS/局域增强等对空间梯度敏感的应用。适合机场周遭或短基线梯度研究。全球 GIM 不是目标；与 ROTI/闪烁监测可互补。

#### [MyIonosphere_Library](https://github.com/mguerra96/MyIonosphere_Library)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：4 · 宿主：github

计算相位几何自由组合（GFLC）与电离层穿刺点，适合教学推导 STEC 观测方程。输入为起止时间与 RINEX 观测文件目录（GPS/Galileo/GLONASS/BeiDou/SBAS）；输出为 GFLC/IPP。局限：不是完整 TEC 定标与 DCB 解算套件。

#### [tec-example](https://github.com/embrace-inpe/tec-example)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：3 · 宿主：github

INPE Embrace 相关的 TEC 处理示例脚本，降低接触其数据产品与基本流程的门槛。适合南美区域 TEC 或空间天气入门。仓库体量小，不是完整产线；深度批处理请接 gnss-tec、PyTECGg 或 Embrace 官方推荐流程，并核对映射函数与 DCB 假设。

#### [ESA-UGI](https://essr.esa.int/project/unified-gnss-ionosphere)  
*🏷️ 官方*

语言：unknown · 许可：ESA Community License v2.4 Weak Copyleft (Type 2) · 星标约：— · 宿主：official_site

欧洲航天局在 ESSR 发布的 Unified GNSS Ionosphere（UGI）程序包，面向 GPS/Galileo/BDS 双频观测估计垂直 TEC、频间偏差与载波模糊度，支持体素/多层/球谐等 2D–3D 电离层表征。适合作为 GNSS 电离层估计研究的可复现起点。源码托管在 ESSR 的 git，下载需注册 ESA Community 账号并接受 ESA Community License v2.4 Weak Copyleft；输入需预先标记/改正周跳。

#### [Get_IPP](https://github.com/Chenjiajun01/Get_IPP)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：— · 宿主：github

根据测站与卫星几何求电离层穿刺点，GIM/层析前处理常用。适合教学与自写映射函数前的几何模块。单薄脚本型项目，坐标框架与壳层高度约定要与主流程一致。

#### [GNSS-Workshop-TEC](https://github.com/breid-phys/GNSS-Workshop)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：0 · 宿主：github

教学/研讨班 Jupyter 材料，演示 GNSS 数据探索与 TEC 测量流程，适合入门。局限：非生产库；依赖研讨班数据布局。

#### [Heki-GNSS-TEC-Software](https://www.ep.sci.hokudai.ac.jp/~heki/software.htm)  
*🏷️ 高校实验室*

语言：Fortran · 许可：academic research (as-is) · 星标约：— · 宿主：official_site

日置幸一郎课题组公开的 Fortran 工具页：rdrnx/rdrnx3 从 RINEX 生成几何无关 L4、rdeph 算卫星位置、tomo 做三维电子密度层析，并含 CID 仿真与 GEONET 荷载示例。学术研究常用。许可为研究用公开源码（非 SPDX）；社区镜像见 yu-0124/GNSS-TEC_tools。编译与坐标系约定需对照说明书。

#### [IONOLAB-TEC-Software](https://www.ionolab.org/index.php?language=en&page=ionolabtec)  
*🏷️ 高校实验室*

语言：unknown · 许可：academic research (non-commercial; cite required) · 星标约：— · 宿主：official_site

Hacettepe/IONOLAB 团队提供的 IONOLAB-TEC/STEC 本地下载软件入口，与站点上的 IONOLAB-TEC Online、IRI-Plas 在线服务配套，面向学术 GNSS TEC/STEC 估计。下载页明确要求先登录；新用户需在 ionolab.org 注册。面向科研非商业用途，发表需引用服务页所列论文。IRI-Plas 子页偶发 500，以 TEC 软件页为准。

#### [KOH2-ionosphere](https://github.com/asparuhkamburov/KOH2-ionosphere)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：0 · 宿主：github

单站（KOH2）TEC 处理、检验与太阳周 25 分析脚本，可作为极区测站流程参考。局限：强绑定单站个例；泛化到其他站需改路径与偏差策略。

#### [Okoh-MATLAB-TEC-from-RINEX](https://doi.org/10.5281/zenodo.7711905)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

NASRDA 研究人员 Daniel Okoh 在 Zenodo 发布的 MATLAB 代码包（concept DOI 10.5281/zenodo.7711905），面向 RINEX 观测做周跳检测/改正、相位平滑与 TEC 提取，示例来自 U-Blox 接收机。许可 CC-BY-4.0，文件为可直接下载的 .m 脚本，无 GitHub 依赖。适合教学与单站 TEC 试验；生产级多系统流水线可对照 Seemala/IONOLAB 等工具。

#### [quakeion](https://github.com/Gm015555/quakeion)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

把地震目录与电离层 TEC/ROT/ROTI 分析串起来，并可用 Kp/Dst 过滤地磁暴，强调无需额外 API Key。适合震电离层耦合统计入门。局限：依赖 GIM/IONEX 而非测站原始 STEC；因果解释需谨慎；星数为 0。

#### [Seemala-GPS-TEC](https://seemala.blogspot.com/2026/08/gps-tec-analysis-program-version-37.html)  
*🏷️ 个人社区*

语言：Windows/Exe · 许可：freeware for research (cite Seemala 2023) · 星标约：— · 宿主：other

空间物理学者 Gopi Seemala 在个人博客发布维护的经典 GPS TEC 分析程序（博客当前为 v3.7）。读取 GPS RINEX 2/3 观测与导航文件并自动拉取 DCB，输出 CMN 文本与日变化图；Windows 便携 ZIP，无需安装。低纬电离层教学与区域 TEC 研究引用极广；目前文档称暂仅 GPS。请按 Seemala 2023 章节引用，注意 VC++ 运行库依赖。非开源源码发布。

#### [vtec](https://github.com/mfkiwl/vtec)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：MIT · 星标约：— · 宿主：github

C++ 写的全球电离层 VTEC 估计系统（中文 README）：读 RINEX 2/3 观测与广播/SP3 星历，做周跳探测和相位平滑伪距得到 STEC，经 SLM/MSLM 等映射转 VTEC，再用球谐函数建全球电离层图并联合估计卫星与接收机 DCB，输出 IONEX；支持 GPS/GLONASS/Galileo/BeiDou/QZSS。README 未署作者，星标少、缺外部验证，结果应先与 CODE/IGS GIM 对比。MIT。

## 测高仪

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [jvierine-ionosonde](https://github.com/jvierine/ionosonde) | ionosonde（jvierine）：开源测高仪/电离图 Python 软件 | Python | 23 | 🏷️ 个人社区 |
| [ionosonde_volgatech](https://github.com/Vladimi-lan/ionosonde_volgatech) | ionosonde_volgatech：伏尔加技术大学测高仪数据处理代码（个人仓） | Python | 13 | 🏷️ 个人社区 |
| [Alouette_ISIS_extract](https://github.com/asc-csa/Alouette_ISIS_extract) | Alouette_ISIS_extract：CSA 历史扫描电离图提取 | Python | 11 | 🏷️ 官方 |
| [POLAN](https://github.com/space-physics/POLAN) | POLAN：Titheridge 虚高→真高反演（现代封装） | Fortran | 11 | 🏷️ 个人社区 |
| [AlouetteApp](https://github.com/asc-csa/AlouetteApp) | 加拿大航天局 Alouette-I 顶部探测电离图筛选、下载与可视化 Dash 应用 | Python | 8 | 🏷️ 官方 |
| [pynasonde](https://github.com/shibaji7/pynasonde) | pynasonde：精密电离层测高/探测 Python 应用 | Python | 5 | 🏷️ 个人社区 |
| [HamSCI-ionosonde](https://github.com/HamSCI/hamsci_ionosonde) | HamSCI-ionosonde：低成本啁啾测高仪处理与验证 | Python | 1 | 🏷️ 高校实验室 |
| [Autoscala-INGV](http://iononet.ingv.it/index.php/download/software) | Autoscala-INGV：INGV Autoscala 测高仪自动缩放软件入口 | various | — | 🏷️ 官方 |
| [CARP-Average-Profile](https://ulcar.uml.edu/SoftwareUtilities/CARP/) | CARP-Average-Profile：测高仪平均代表剖面计算 | Fortran | — | 🏷️ 高校实验室 |
| [Drift-X](https://ulcar.uml.edu/Drift-X.html) | Drift-X：Digisonde 漂移数据可视化与分析（Java） | Java | — | 🏷️ 高校实验室 |
| [NHPC-TrueHeight](https://ulcar.uml.edu/SoftwareUtilities/NHPC/) | NHPC：测高仪迹线真高剖面反演（Digisonde/ARTIST） | Fortran/C | — | 🏷️ 高校实验室 |
| [SAO-Explorer](https://ulcar.uml.edu/SAO-X/) | GIRO/Digisonde 测高仪缩放与 DIDBase 访问工具（免费二进制） | Java | — | 🏷️ 官方 |
| [UMLCAR-Downloads](https://ulcar.uml.edu/downloads.html) | UMLCAR-Downloads：UML Digisonde 工具下载总目录（SAO-X 等） | data-portal | — | 🏷️ 高校实验室 |

### 详细说明

#### [jvierine-ionosonde](https://github.com/jvierine/ionosonde)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：23 · 宿主：github

面向测高仪数据处理与实验的 Python 项目，可用于电离图获取/分析相关工作流。与 GNSS TEC 互补，提供底部电离层约束。局限：README 信息偏少，需读代码确认具体仪器格式；不替代 GIRO/SAO 官方工具链。

#### [ionosonde_volgatech](https://github.com/Vladimi-lan/ionosonde_volgatech)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：13 · 宿主：github

与具体测高仪系统相关的 Python 处理代码，体量不小，可作为非 GIRO 数据源处理参考。局限：缺少清晰英文 README；通用性与许可需使用者自行确认（仓库未声明许可）。

#### [Alouette_ISIS_extract](https://github.com/asc-csa/Alouette_ISIS_extract)  
*🏷️ 官方*

语言：Python · 许可：CSA · 星标约：11 · 宿主：github

CSA 开源项目，从 Alouette 与 ISIS 卫星历史扫描电离图图像中提取数据与元数据，服务历史底部电离层档案数字化。局限：面向图像档案而非现代 GNSS；处理流水线偏研究复现。

#### [POLAN](https://github.com/space-physics/POLAN)  
*🏷️ 个人社区*

语言：Fortran · 许可：MIT · 星标约：11 · 宿主：github

经典 POLAN 算法用于从测高仪/电离图虚高估计真实高度剖面，space-physics 仓库提供可编译的现代维护。对把测高仪 foF2/hmF2 与 GNSS TEC 联合分析很有用。局限：需要质量较好的描迹/虚高输入；不直接处理 GNSS；使用者需了解测高仪反演假设。

#### [AlouetteApp](https://github.com/asc-csa/AlouetteApp)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：8 · 宿主：github

加拿大航天局（CSA）官方开源的 Plotly Dash 应用，MIT 许可，面向 1962 年发射的 Alouette-I 顶部探测仪历史电离图数字化成果：可按时间、地面站、坐标、频率等条件筛选电离图，导出提取特征 CSV 或原始图像，并在地图与折线图中概览所选数据。是少见的官方历史顶部电离层数据开放入口，适合做长期电离层气候或 IRI 顶部剖面对比。与 alouette_isis_extract 为同源项目（后者负责特征提取）。法英双语文档。

#### [pynasonde](https://github.com/shibaji7/pynasonde)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：5 · 宿主：github

面向精密电离层无线电探测（sounding）的 Python 应用，服务实验测高/探测数据处理。局限：相对传统 Digisonde 软件生态仍小；硬件/数据格式适配需对照文档。

#### [HamSCI-ionosonde](https://github.com/HamSCI/hamsci_ionosonde)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：1 · 宿主：github

配套 HamSCI 低成本 chirp 测高仪：SDR 发收、互相关测时延、估算虚高，并在日食等事件中与业务测高仪对比。输入为 SDR/GNU Radio 采集；输出时延与虚高序列。局限：依赖实验执照与硬件；频段 2–10 MHz，与 GNSS 频段不同。

#### [Autoscala-INGV](http://iononet.ingv.it/index.php/download/software)  
*🏷️ 官方*

语言：various · 许可：scientific distribution (INGV portal) · 星标约：— · 宿主：official_site

意大利国家地球物理与火山学研究所（INGV）测高仪团队的软件下载页，介绍 Autoscala 自动缩放（foF2、MUF 等）以及数据分析、电离层模型配套工具。适合欧洲/INGV 站网 ionogram 自动处理路线。页面偏门户说明，具体包获取方式以站点 Restricted area / 联系渠道为准，并非 GitHub 式即开即用源码仓。

#### [CARP-Average-Profile](https://ulcar.uml.edu/SoftwareUtilities/CARP/)  
*🏷️ 高校实验室*

语言：Fortran · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

UMLCAR 提供的平均代表剖面工具，用于从多幅测高图剖面提取统计代表结构。服务气候态与模型验证场景；与 NHPC/SAO-X 同属测高仪处理链。

#### [Drift-X](https://ulcar.uml.edu/Drift-X.html)  
*🏷️ 高校实验室*

语言：Java · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

UMLCAR 发布的 Digisonde 漂移（DDA）数据查看器，当前发行约 1.2.14-FB3，ZIP 解压即用。面向测高仪漂移观测质控与教学；与 SAO-X 测高图定标流程互补，不直接输出 GNSS TEC。

#### [NHPC-TrueHeight](https://ulcar.uml.edu/SoftwareUtilities/NHPC/)  
*🏷️ 高校实验室*

语言：Fortran/C · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

将 ARTIST 等自动/人工定标的测高仪迹线反演为等离子体频率–真高剖面的经典工具，常嵌入 SAO Explorer 工作流。适合底层电离层剖面研究与 IRI/IRTAM 对照；输入依赖合格 SAO/定标结果，非 GNSS TEC 估计器。

#### [SAO-Explorer](https://ulcar.uml.edu/SAO-X/)  
*🏷️ 官方*

语言：Java · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

处理 SAO/SAOXML、内置 ARTIST-5 与剖面反演，并可连 Lowell DIDBase。irimodel 相关的 IRTAM/GIRO 生态常用桌面工具。官方提供跨平台 zip，属免费科学软件而非公开 OSS 源码（license 标 proprietary-freeware）。不做 GNSS TEC 建图；源码级二次开发请另寻开源栈。

#### [UMLCAR-Downloads](https://ulcar.uml.edu/downloads.html)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

洛厄尔麻省大学大气研究中心官方下载索引：SAO Explorer（含 ARTIST-5）、Drift-X、BinBrowser、DCART、NHPC、CARP 等 Digisonde/测高仪工具集中入口。SAO-X 另有独立主页；本页作为软件总目录，便于发现其余开源/可下载工具。

## 磁坐标

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [apexpy](https://github.com/aburrell/apexpy) | apexpy：Apex/准偶极地磁坐标 Python 封装 | Python | 40 | 🏷️ 个人社区 |
| [aacgmv2](https://github.com/aburrell/aacgmv2) | aacgmv2：AACGM-v2 地磁坐标 Python 库 | Python | 35 | 🏷️ 个人社区 |
| [ocbpy](https://github.com/aburrell/ocbpy) | ocbpy：极盖边界自适应磁坐标转换库 | Python | 11 | 🏷️ 个人社区 |

### 详细说明

#### [apexpy](https://github.com/aburrell/apexpy)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：40 · 宿主：github

电离层研究里把地理坐标转到 Apex/准偶极坐标的常用库，PyIRI 等也依赖同类坐标。输入纬经高与时间；输出磁纬磁地方时等。局限：不是电子密度模型；需注意 IGRF 年代与外推。

#### [aacgmv2](https://github.com/aburrell/aacgmv2)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：35 · 宿主：github

aburrell 维护的 AACGM-v2 Python 库，在地理坐标与高度调整校正地磁坐标间转换，电离层/极光研究常用。MIT 许可；引用需同时给出包 DOI 与 Shepherd 2014 论文。与 apexpy、igrf 互补，它本身不是 GNSS 观测解算器。

#### [ocbpy](https://github.com/aburrell/ocbpy)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：11 · 宿主：github

与 apexpy 同作者体系的 ocbpy，把观测转换到基于极盖边界（OCB）的自适应磁坐标，便于高纬电离层与磁层统计研究。许可 BSD-3-Clause。主要服务空间物理坐标变换，不直接读取 RINEX 或做 TEC 反演；常与极光电集流等数据集联用。

## 闪烁/ROTI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | IonoMoni：多星座 ROTI/AATR/STEC/VTEC | C++ | 37 | 🏷️ 个人社区 ★ |
| [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator) | gnss-scintillation-simulator：GNSS 闪烁相位/幅度仿真 | MATLAB | 25 | 🏷️ 高校实验室 |
| [OASIS](https://github.com/giorgiopicanco/OASIS) | OASIS：RINEX 扰动指标计算 | Python | 16 | 🏷️ 个人社区 核心 |
| [SbfParser](https://github.com/septentrio-gnss/SbfParser) | SbfParser：Septentrio SBF 流/文件厂商解析器 | Cython | 12 | 🏷️ 个人社区 |
| [saga-utils](https://github.com/perrysou/saga-utils) | 阿拉斯加闪烁极光 GPS 阵列（SAGA）数据处理与估计工具（MATLAB） | MATLAB | 10 | 🏷️ 个人社区 |
| [scintill-ai](https://github.com/viventriglia/scintill-ai) | scintill-ai：机器学习电离层闪烁分析研究项目 | Shell | 8 | 🏷️ 个人社区 |
| [TITIPy](https://github.com/pignalberi/TITIPy) | Swarm 顶部电离层 RODI/ROTI/ROTEI（Python） | Python | 8 | 🏷️ 高校实验室 |
| [gnss-scintillation-simulator_2-param](https://github.com/cu-sense-lab/gnss-scintillation-simulator_2-param) | gnss-scintillation-simulator_2-param：CU 两参数闪烁仿真 | MATLAB | 6 | 🏷️ 高校实验室 |
| [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP) | Ionospheric-Scintillation-Maps-and-PDOP：闪烁成像与 PDOP 影响 | MATLAB | 5 | 🏷️ 个人社区 |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据清洗与指标计算工具 | Python | 3 | 🏷️ 个人社区 ★ |
| [Ionospheric-TEC-ROTI-Interactives](https://github.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives) | Ionospheric-TEC-ROTI-Interactives：交互式 TEC/ROTI 计算 | Python | 3 | 🏷️ 个人社区 |
| [roti-gnss-ml](https://github.com/NeelayS/roti-gnss) | roti-gnss-ml：深度学习 GNSS ROTI 时序预报实验 | Python | 3 | 🏷️ 个人社区 |
| [BiScEF](https://github.com/kartverket/BiScEF) | BiScEF：Kartverket 闪烁数据二进制交换格式实现 | Python | 2 | 🏷️ 官方 |
| [igs-roti](https://github.com/jonathanblade/igs-roti) | igs-roti：IGS ROTI Maps 产品的 Web 可视化 | Python | 2 | 🏷️ 个人社区 |
| [ionospheric-scintillation-mitigation](https://github.com/fengjie0325/ionospheric-scintillation-mitigation) | ionospheric-scintillation-mitigation：闪烁抑制算法 MATLAB 码 | MATLAB | 2 | 🏷️ 个人社区 |
| [FARR](https://gitlab.com/longleywj/farr) | FARR：磁化碰撞等离子体三维 FDTD 电波传播（GitLab） | C++ | 1 | 🏷️ 高校实验室 |
| [gnss-vector-scintillation](https://github.com/DTUSWx/gnss-vector-scintillation) | 矢量闪烁：Jones–Stokes GNSS 闪烁 MATLAB 参考码 | MATLAB | 1 | 🏷️ 高校实验室 |
| [scintkit](https://github.com/qwsae10/scintkit) | scintkit：ScintPi/GNSS 闪烁快看工具集 | Jupyter Notebook | 1 | 🏷️ 个人社区 |
| [IBP-Model](https://igit.iap-kborn.de/ibp/ibp-model) | IBP-Model：低纬赤道等离子体泡发生概率（IAP Kühlungsborn） | Python | 0 | 🏷️ 高校实验室 |
| [M_ISSION](https://github.com/wulide4/M_ISSION) | M_ISSION：多 GNSS 电离层闪烁指数计算软件 | C++ | 0 | 🏷️ 个人社区 |
| [Okoh-MATLAB-ROT-ROTI](https://doi.org/10.5281/zenodo.7913105) | Okoh-MATLAB-ROT-ROTI：TEC 序列算 30s ROT 与 5min ROTI | MATLAB | — | 🏷️ 个人社区 |
| [ScintPi-1.0-Software](https://doi.org/10.5281/zenodo.4905193) | ScintPi-1.0-Software：UT Dallas 低成本闪烁仪配套软件 | binary (PyInstaller) | — | 🏷️ 高校实验室 |
| [Swarm-VIP-Dynamic](https://gitlab.com/KNMI-OSS/spaceweather/swarm-vip-dynamic) | Swarm-VIP-Dynamic：KNMI 的 ISMR 闪烁处理与模型评估工作仓 | Python | 0 | 🏷️ 官方 |

### 详细说明

#### [IonoMoni](https://github.com/qiliu2025/IonoMoni)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：GPL-3.0 · 星标约：37 · 宿主：github

C++ 实现多星座电离层监测指标（ROTI、AATR、STEC/VTEC），偏近实时监测。适合需要编译型性能的台站软件。README 声明以 GPLv3 发布；科研绘图可再接 Python 可视化。

#### [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：25 · 宿主：github

科罗拉多大学 Boulder Satellite Navigation and Sensing Lab（cu-sense-lab）开源的 GNSS 闪烁仿真器，生成相位与幅度闪烁序列，用于接收机跟踪环与完好性试验。适合算法仿真，不是实测 ROTI 产品生成器；参数需对照文献与实测统计。同实验室还有简化两参数版 gnss-scintillation-simulator_2-param。

#### [OASIS](https://github.com/giorgiopicanco/OASIS)  
*🏷️ 个人社区 核心*

语言：Python · 许可：CC-BY-NC-4.0 · 星标约：16 · 宿主：github

Open-Access System for Ionospheric Studies：从 GNSS 观测算 ROTI、ΔTEC、SIDX 等，做扰动与闪烁相关监测。适合空间天气事件个例与台站网指标产品。高采样率接收机原始闪烁指数（S4/σφ）仍需专用接收机或仿真器。ohm1122/OASIS 是本仓的 fork（维护者星标），无独立提交且落后上游 28 个提交。

#### [SbfParser](https://github.com/septentrio-gnss/SbfParser)  
*🏷️ 个人社区*

语言：Cython · 许可：BSD-3-Clause · 星标约：12 · 宿主：github

Septentrio 厂商发布的 Python/Cython 解析器，把 SBF 流转成 JSON 结构，社区已扩展 ISMR（4086）等闪烁监测块，便于从 PolaRx 系列提取 S4、σφ 等。输入为 SBF 文件或流；输出为结构化观测/状态块。局限：侧重解码而非完整闪烁科学产品流水线；大文件需注意内存策略。

#### [saga-utils](https://github.com/perrysou/saga-utils)  
*🏷️ 个人社区*

语言：MATLAB · 许可：GPL-3.0 · 星标约：10 · 宿主：github

面向 Scintillation Auroral GPS Array（SAGA，部署于阿拉斯加 Poker Flat 的多接收机阵列）的数据处理、分析与状态估计工具集，GPL-3.0 许可，MATLAB 实现，出自相关高校课题组研究生工作。可读取高采样率接收机数据，计算 S4、σφ 等闪烁指数，并利用阵列几何估计电离层不规则体漂移速度。适合高纬闪烁与接收机阵列研究者参考算法实现；仓库自 2018 年后未更新，说明文档很少，依赖原始数据格式需自行适配。

#### [scintill-ai](https://github.com/viventriglia/scintill-ai)  
*🏷️ 个人社区*

语言：Shell · 许可：MIT · 星标约：8 · 宿主：github

探索用机器学习刻画或预测电离层闪烁相关现象的研究型仓库，偏数据驱动实验原型。适合空间天气与机器学习交叉课题入门。闪烁事件稀缺、标签噪声与跨站点泛化是主要风险；报告结果时应保留 S4、σφ、ROTI 等物理基线对照，避免只展示神经网络分数而缺少可解释性。

#### [TITIPy](https://github.com/pignalberi/TITIPy)  
*🏷️ 高校实验室*

语言：Python · 许可：CC-BY-NC-SA-3.0 · 星标约：8 · 宿主：github

INGV/ESA INTENS 的 Swarm 顶部电离层湍流指数工具（Python）：从 Langmuir 探针与 POD/TEC 产品算 RODI/ROTI/ROTEI 并制图，含下载与 CDF 读取。CC BY-NC-SA 3.0，需自备 Swarm 账号；面向顶部电离层闪烁研究，不是地基双频 TEC 解算器。

#### [gnss-scintillation-simulator_2-param](https://github.com/cu-sense-lab/gnss-scintillation-simulator_2-param)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

科罗拉多大学 Sense Lab 的两参数版 GNSS 闪烁仿真，相对完整版简化相位/幅度扰动建模，便于接收机与信号处理压力测试。适合教学与算法试验。真实赤道/极区场景请结合实测 ISMR 与原版多参数仿真器对照评估。

#### [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：5 · 宿主：github

研究电离层闪烁空间成像及其对定位几何（PDOP）影响的代码，把空间天气扰动与导航可用性联系起来。适合闪烁—PNT 耦合与完好性相关课题。不是业务级闪烁监测网软件；输入场与网格假设应按论文复现，并可与 OASIS、ROTI 类工具对照物理指标定义。

#### [gnssutils](https://github.com/ljlamarche/gnssutils)  
*🏷️ 个人社区 ★*

语言：Python · 许可：GPL-3.0 · 星标约：3 · 宿主：github

面向地基 GNSS 闪烁接收机数据流的实用函数集，便于清洗与指标计算。适合已有 ISMR/闪烁观测的课题组。GPL 许可需留意；不替代通用 TEC/GIM 或业务闪烁预警系统。

#### [Ionospheric-TEC-ROTI-Interactives](https://github.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：3 · 宿主：github

带 Tkinter/交互流程的 TEC 与 ROTI 计算工具，可按高度角筛选并对比扰动日与静日，输出 30 s 与 5 min 窗口 ROTI。输入为用户准备的 TEC 数据文件夹（非完整 RINEX 解算链）。局限：依赖外部已算好的 TEC；GUI 交互偏本地脚本；许可未声明。

#### [roti-gnss-ml](https://github.com/NeelayS/roti-gnss)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：3 · 宿主：github

Notebook 实验：对 GNSS 导出的 ROTI 做深度学习时序预报。局限：研究原型；数据与复现说明有限；不是业务 ROTI 生成器。

#### [BiScEF](https://github.com/kartverket/BiScEF)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

挪威制图局（Kartverket）维护的 Binary Scintillation Exchange Format 实现与示例；stenseng/BiScEF 已声明迁移至此仓，故目录只保留官方仓。便于闪烁监测接收机数据互通；做多源融合时关注格式版本。通用 TEC/ROTI 计算仍用 IonoMoni/OASIS 等。

#### [igs-roti](https://github.com/jonathanblade/igs-roti)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：2 · 宿主：github

针对 IGS ROTI map 产品的可视化网页/工具，方便快速查看全球/区域 ROTI 图，而不是从原始观测算 ROTI。局限：依赖 IGS 产品发布；仓库小、维护有限。

#### [ionospheric-scintillation-mitigation](https://github.com/fengjie0325/ionospheric-scintillation-mitigation)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：2 · 宿主：github

论文配套闪烁抑制算法实现（MATLAB），用于理解跟踪环/信号处理层面的缓解思路。输入为受闪烁影响的信号/观测量仿真或实测；输出为抑制后结果对比。局限：代码体量小、场景专用；不替代接收机厂商闭源算法。

#### [FARR](https://gitlab.com/longleywj/farr)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0-or-later · 星标约：1 · 宿主：gitlab

NJIT/Boston University 的三维 FDTD 开源码（GitLab，GPL-3.0-or-later），仿真磁化碰撞等离子体中的电波传播与闪烁。提供 CMake/Docker/Python 辅助。面向传播机理研究，不是 GNSS 观测解算或 GIM 产品工具。

#### [gnss-vector-scintillation](https://github.com/DTUSWx/gnss-vector-scintillation)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：1 · 宿主：github

配套 Radio Science 投稿的 MATLAB 参考代码，用统一 Jones–Stokes 表述把幅度、相位闪烁扩展到极化观测量，并覆盖地基、掩星与反射几何。面向科研复现而非业务接收机。星标少但有 DOI；不替代 S4/σφ 业务处理流水线。

#### [scintkit](https://github.com/qwsae10/scintkit)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：1 · 宿主：github

面向 ScintPi 与 GNSS 闪烁的简单处理与看图，偏教学演示。论文级闪烁指数、多站网与业务化质控需接更完整工具链。

#### [IBP-Model](https://igit.iap-kborn.de/ibp/ibp-model)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：0 · 宿主：other

莱布尼茨大气物理所 Kühlungsborn 在机构 GitLab（igit.iap-kborn.de）开源的 Ionospheric Bubble Probability 模型，基于 CHAMP/Swarm 磁场与电子密度，输出随 DOY/经度/地方时/F10.7 变化的低纬泡发生概率指数（0–1），并可 pip 安装 ibpmodel。MIT 许可，文档见 ReadTheDocs。适合赤道闪烁/EPB 气候概率与 Swarm L2 IBP_CLI 产品对照；非 TEC 反演工具。

#### [M_ISSION](https://github.com/wulide4/M_ISSION)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：0 · 宿主：github

面向多系统 GNSS 的闪烁指数（如 S4 等）处理软件，仓库体积较大，适合闪烁监测实验。输入为高频采样 GNSS 观测；输出为闪烁指数产品。局限：开源许可与文档需自行确认；部署依赖可能偏工程化。

#### [Okoh-MATLAB-ROT-ROTI](https://doi.org/10.5281/zenodo.7913105)  
*🏷️ 个人社区*

语言：MATLAB · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

配套 Zenodo 软件存档（concept DOI 10.5281/zenodo.7913105），提供 rot30s_mean.m 与 roti5m.m，从 GNSS/其他仪器 TEC 时间序列计算 30 秒 TEC 变化率与 5 分钟 ROTI。CC-BY-4.0，体积小、接口清晰，便于嵌入已有 TEC 流水线做不规则性监测。需自备定标后的 TEC 输入。

#### [ScintPi-1.0-Software](https://doi.org/10.5281/zenodo.4905193)  
*🏷️ 高校实验室*

语言：binary (PyInstaller) · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

德州大学达拉斯分校发布的 ScintPi 1.0 官方采集/可视化软件 ZIP（concept DOI 10.5281/zenodo.4905193），经 USB 连接硬件，面向教育与低成本闪烁监测。CC-BY-4.0，“as is”无质保；ZIP 内只有 PyInstaller 打包的可执行文件（Windows 绘图 exe 与树莓派采集程序），不含源码。与 GitHub 上第三方 scintkit 小工具不同，这里是仪器配套官方软件存档。适合教学网部署；论文级多站 S4/σφ 分析仍需专用 GISTM 或商用接收机链路。

#### [Swarm-VIP-Dynamic](https://gitlab.com/KNMI-OSS/spaceweather/swarm-vip-dynamic)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：0 · 宿主：gitlab

KNMI 在 Swarm-VIP-Dynamic（UiO/Birmingham/INGV/DLR/KNMI）合作中的代码仓：含有效 F10.7 代理、Septentrio PolaRX5S ISMR 闪烁监测文件处理与可视化、项目模型及 IBP 等外部模型评估、Swarm 轨道派生磁纬/地方时等。与 swarm-vip-dynamic-models 库配套，偏研究流水线与闪烁数据可视化。公开 GitLab 仓，无 LICENSE 文件，pyproject.toml 标 Apache License v2.0。

## 工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PySPEDAS](https://github.com/spedas/pyspedas) | 空间物理多任务数据检索、分析与绘图 Python 框架（含地面磁力计模块） | Python | 204 | 🏷️ 官方 |
| [pysat](https://github.com/pysat/pysat) | pysat：日地空间科学数据分析框架 | Python | 173 | 🏷️ 个人社区 |
| [MagPy](https://github.com/geomagpy/magpy) | 地磁观测台数据处理 Python 包 MagPy（GeomagPy），支持 IAGA-2002/ImagCDF 等格式 | Python | 67 | 🏷️ 高校实验室 |
| [Kamodo](https://github.com/nasa/Kamodo) | Kamodo：NASA CCMC 日地模式输出函数化套件 | Python | 58 | 🏷️ 官方 |
| [geospacelab](https://github.com/JouleCai/geospacelab) | geospacelab：日地空间数据管理与可视化 | Python | 48 | 🏷️ 个人社区 |
| [pysatNASA](https://github.com/pysat/pysatNASA) | pysatNASA：pysat 的 NASA 空间科学仪器数据扩展（BSD-3） | Python | 25 | 🏷️ 个人社区 |
| [Lompe](https://github.com/klaundal/lompe) | 极区电离层电动力学局地反演工具 Lompe（多源数据融合） | Python | 23 | 🏷️ 高校实验室 |
| [SuperSID](https://github.com/sberl/supersid) | SuperSID：VLF 突发电离层扰动（SID）监测 | Python | 16 | 🏷️ 个人社区 |
| [pysatMissions](https://github.com/pysat/pysatMissions) | pysatMissions：pysat 任务规划与仪器工具扩展 | Python | 14 | 🏷️ 个人社区 |
| [pysatSpaceWeather](https://github.com/pysat/pysatSpaceWeather) | pysatSpaceWeather：pysat 空间天气指数支持库 | Python | 14 | 🏷️ 个人社区 |
| [pysatCDF](https://github.com/pysat/pysatCDF) | pysatCDF：NASA CDF 格式 Python 读取器（pysat） | Python | 13 | 🏷️ 个人社区 |
| [ionosphereAI](https://github.com/space-physics/ionosphereAI) | ionosphereAI：多源噪声数据中的电离层特征检测 | Python | 11 | 🏷️ 个人社区 |
| [pysatModels](https://github.com/pysat/pysatModels) | pysatModels：pysat 模式分析与模式-数据对比 | Python | 9 | 🏷️ 个人社区 |
| [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting) | ionosphere-plotting：TEC/foF2/DST 等指数绑图脚本 | Python | 7 | 🏷️ 个人社区 |
| [radionopy](https://github.com/UPennEoR/radionopy) | radionopy：大尺度电离层行为 Python/C 计算工具 | C | 7 | 🏷️ 高校实验室 |
| [GRITI](https://github.com/dinsmoro/GRITI) | GRITI：多源电离层瞬变分析与可视化工具箱 | Python | 5 | 🏷️ 高校实验室 |
| [Kamodo-core](https://github.com/nasa/Kamodo-core) | Kamodo-core：科学数据函数化 API 核心（NASA） | Python | 5 | 🏷️ 官方 |
| [mitiono](https://github.com/sabrinastronomy/mitiono) | mitiono：由 GPS 接收机数据提取电离层与波束图 | Jupyter Notebook | 4 | 🏷️ 个人社区 |
| [SubionosphericVLFInversionAlgorithms.jl](https://github.com/fgasdia/SubionosphericVLFInversionAlgorithms.jl) | SubionosphericVLFInversionAlgorithms.jl：VLF 反演低电离层 Julia 算法 | Julia | 4 | 🏷️ 个人社区 |
| [nleht-fdtd-ionosphere](https://gitlab.com/nleht/fdtd) | nleht-fdtd：电离层 VLF 波 MPI 并行 FDTD（GitLab） | C++ | 1 | 🏷️ 高校实验室 |
| [pypride](https://gitlab.com/gofrito/pypride) | pypride：行星雷达/VLBI 库（含 IONEX 与闪烁表 TEC） | Python | 1 | 🏷️ 个人社区 |
| [Boston-College-ISR-Ionospheric-Studies](https://www.bc.edu/bc-web/research/sites/institute-for-scientific-research/research/ionospheric-studies.html) | Boston College ISR 电离层研究组主页（闪烁、层析与 GNSS TEC 方向） | data-portal | — | 🏷️ 高校实验室 |
| [IMSP-MGS](https://essr.esa.int/project/ionosphere-modular-software-package-imsp-mgs) | IMSP-MGS：GNSS-R/SAR/雷达测深电离层效应仿真（ESA） | unknown | — | 🏷️ 官方 |
| [IonTools](https://github.com/rumkex/IonTools) | IonTools：电离层分析辅助小工具（C++） | C++ | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [PySPEDAS](https://github.com/spedas/pyspedas)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：204 · 宿主：github

SPEDAS 团队（源自 THEMIS/伯克利 SSL）维护的 Python 版空间物理数据分析框架，MIT 许可，可 pip 安装并有完整 ReadTheDocs 文档。统一封装数十个任务与数据源的下载和读取，包括 ACE、Arase、C/NOFS、DSCOVR、GOES、MMS、THEMIS 及其地面磁力计与全天空成像仪、Swarm、OMNI 等，并提供坐标变换、时间序列处理与 pytplot 绘图。做 GNSS 电离层事件分析时可一站式获取太阳风、地磁与卫星原位数据。持续活跃维护。

#### [pysat](https://github.com/pysat/pysat)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：173 · 宿主：github

pysat 提供跨平台一致的数据分析工作流，生态含空间天气指数、模式接口等，常与电离层卫星/地基数据一起用。局限：本身不是 IRI/TEC 专用包；学习曲线在“生态”而非单函数。

#### [MagPy](https://github.com/geomagpy/magpy)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：67 · 宿主：github

奥地利 GeoSphere（原 ZAMG）Conrad 观测台团队主导开发的地磁数据分析包，BSD-3-Clause 许可。面向观测台日常处理：读写 ImagCDF、IAGA-2002、WDC、IAF、BLV 等格式，做基线值与基线计算、滤波、合并、指数计算与数据库管理，完整安装还带图形界面 XMagPy。适合需要把 INTERMAGNET 或自建磁力计数据接入 GNSS 电离层研究流程的用户。作者提示 2.x 版本仍在频繁改动，升级前应阅读发布说明。

#### [Kamodo](https://github.com/nasa/Kamodo)  
*🏷️ 官方*

语言：Python · 许可：NASA-1.3 · 星标约：58 · 宿主：github

Kamodo（CCMC 读者套件）把多种日地空间模式输出“函数化”，统一插值、单位换算、可视化与卫星飞越（flythrough）。对电离层目录特别有价值：支持 GITM、TIEGCM、IRI、WACCM-X、CTIPe、SWMF-IE 等，便于把物理模式电子密度接到观测对比。输入是各模式输出目录；输出是可调用的 Kamodo 对象与图。局限：依赖与内存要求不低；不同模式 reader 成熟度不一；不是从 GNSS 观测解算 TEC 的软件。

#### [geospacelab](https://github.com/JouleCai/geospacelab)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：48 · 宿主：github

GeospaceLAB 用 Python 统一拉取与管理 OMNI、地磁指数、EISCAT、DMSP、Swarm、TEC、AMPERE 等，并做可视化，适合快速搭电离层观测对比分析环境。输入多为各数据中心接口或本地缓存；输出为结构化数据集与图。局限：依赖外部数据源可用性与注册策略；不是 TEC 解算引擎本身；包体与依赖较重。

#### [pysatNASA](https://github.com/pysat/pysatNASA)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：25 · 宿主：github

为 pysat 框架提供 NASA 相关仪器/任务数据支持的扩展包，BSD-3-Clause。便于把空间天气与高层大气观测拉进统一分析工作流，可与 GNSS 电离层研究对照。依赖 pysat 核心与上游数据政策；并非 GNSS 解算库。适合需要多源空间数据对齐的科研脚本。

#### [Lompe](https://github.com/klaundal/lompe)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：23 · 宿主：github

Karl M. Laundal 等开发、Trond Mohn 基金会与挪威研究理事会资助的 LOcal Mapping of Polar ionospheric Electrodynamics，MIT 许可，Python 实现并提供 Binder 可运行示例。在局地立方球网格上，融合 SuperDARN 对流、卫星磁场/离子漂移与地面磁力计扰动等观测，反演区域电场、电流与电势分布，Hall/Pedersen 电导需用户以函数形式给出。适合研究极光区电动力学与 GNSS 闪烁、TEC 斑块的驱动过程。学习曲线较陡，建议先跑仓库自带示例笔记本。近期仍有更新。

#### [SuperSID](https://github.com/sberl/supersid)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

SuperSID 用简易 VLF 接收监测突发电离层扰动（太阳耀斑等引起的 D 区吸收变化），sberl 分支相对活跃。输出 SID 幅度时间序列。局限：监测的是 VLF 幅度而非 GNSS TEC；站点环境噪声影响大。

#### [pysatMissions](https://github.com/pysat/pysatMissions)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：14 · 宿主：github

pysat 生态的任务/仪器规划工具包，BSD-3-Clause，便于把卫星任务几何与空间天气数据流接到统一分析框架。非 GNSS 解算库，但对星载 GNSS 接收或电离层探测任务规划有辅助价值。依赖 pysat 核心版本。适合科研脚本化任务仿真。

#### [pysatSpaceWeather](https://github.com/pysat/pysatSpaceWeather)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：14 · 宿主：github

为 pysat 生态提供空间天气指数与相关数据接口，便于把 F10.7、地磁指数等驱动接到电离层分析。输入为数据源配置；输出为统一的 pysat Instrument 对象。局限：本身不算 TEC 解算器；需与 pysat 主库配合。

#### [pysatCDF](https://github.com/pysat/pysatCDF)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：13 · 宿主：github

为 pysat 提供 NASA Common Data Format（CDF）读取支持，BSD-3-Clause。空间物理与部分 GNSS/电离层衍生产品常以 CDF 分发，可与 CDAWeb/SPDF 下载流程衔接。适合把官方 CDF 拉进 Python 分析管线。

#### [ionosphereAI](https://github.com/space-physics/ionosphereAI)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：11 · 宿主：github

面向多种电离层遥感噪声数据的特征检测工具，偏机器学习/信号处理，不是 GNSS TEC 解算。局限：与 GNSS 流水线耦合需自行对接；任务定义随数据源变化。

#### [pysatModels](https://github.com/pysat/pysatModels)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：9 · 宿主：github

在 pysat 框架下对接模式输出并做模式-观测对比，便于把经验/物理电离层模式纳入同一分析脚本。局限：需先熟悉 pysat。

#### [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：7 · 宿主：github

面向 TEC、foF2、DST 等指数与时间序列的 Python 绑图工具，适合快速出教学图或报告插图。研究级 GIM/STEC 重建请用 gnss-tec、MosGIM2 等；本仓库偏可视化与展示，数据获取与许可需自备，不宜单独支撑反演论文。输入数据格式需按脚本说明自行对齐时间与单位。选用前请用自有数据做交叉验证。

#### [radionopy](https://github.com/UPennEoR/radionopy)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：7 · 宿主：github

面向射电天文/大尺度电离层效应的数值工具，可计算大范围电离层相关量。输入为模式/几何配置；输出为电离层影响相关场。局限：场景偏射电传播，不是标准 IONEX 生产。

#### [GRITI](https://github.com/dinsmoro/GRITI)  
*🏷️ 高校实验室*

语言：Python · 许可：AGPL-3.0 · 星标约：5 · 宿主：github

宾州州立相关开源仓 GRITI，面向电离层瞬变事件的 Python 分析流水线：可自动拉取 Madrigal δvTEC、AMPERE、Kp 与 OMNI，并做 keogram、滑动相关、FFT/Lomb-Scargle 等。需要本地配置路径与部分账号；部分 ISR/磁强计数据需自行下载。适合空间天气个例研究，不是从 RINEX 重建 TEC 的解算器。

#### [Kamodo-core](https://github.com/nasa/Kamodo-core)  
*🏷️ 官方*

语言：Python · 许可：NASA-1.3 · 星标约：5 · 宿主：github

Kamodo-core 提供函数化科学数据访问的核心 API，CCMC 的 Kamodo readers 建立其上。单独使用可把任意网格场变成可组合函数；与 nasa/Kamodo 搭配更完整。局限：只有 core 时缺少各模式专用 reader；安装路径在历史上有 ensemblegov 与 nasa 组织迁移，注意文档版本。

#### [mitiono](https://github.com/sabrinastronomy/mitiono)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：4 · 宿主：github

配套射电/干涉测量电离层缓解研究，从 GPS 数据生成电离层与波束相关图（见 arXiv:2411.06144）。输入为 Septentrio 接收机的 SBF（及 NMEA）文件；输出为电离层/波束产品。局限：面向特定科学场景；后续基带互相关仍在规划。

#### [SubionosphericVLFInversionAlgorithms.jl](https://github.com/fgasdia/SubionosphericVLFInversionAlgorithms.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：4 · 宿主：github

实现亚电离层 VLF 信号反演以估计低电离层参数，适合教学理解“电波—电离层”反问题。输入为 VLF 观测量与传播几何；输出为低电离层特征量估计。局限：与 GNSS TEC/GIM 流水线不同；对传播正演与初值敏感。

#### [nleht-fdtd-ionosphere](https://gitlab.com/nleht/fdtd)  
*🏷️ 高校实验室*

语言：C++ · 许可：no licence (README: copyright reserved, reference use only) · 星标约：1 · 宿主：gitlab

面向电离层中甚低频（VLF）波传播的三维时域有限差分 C++ 代码，支持 MPI 多节点。适合低电离层/波导传播与 D 区扰动数值实验，与 GNSS L 波段闪烁工具互补。公开 GitLab 项目，但 README 声明代码受版权保护、仅供参考，未授予开源许可，且已停止活跃开发。

#### [pypride](https://gitlab.com/gofrito/pypride)  
*🏷️ 个人社区*

语言：Python · 许可：MIT (pyproject license field; classifier says GPLv3+; no LICENSE file) · 星标约：1 · 宿主：gitlab

GitLab 上的 pypride（PRIDE 相关派生）Python/Fortran 混合包，面向深空/VLBI 几何与延迟处理；内含从 CDDIS 拉取 IONEX 及 computeTEC 等由闪烁观测表估计上下行电离层贡献的脚本。pyproject.toml 许可字段写 MIT，classifier 却写 GPLv3+，仓内无 LICENSE 文件，再分发前需向作者确认。对 GNSS 电离层用户价值在于 IONEX 自动获取与行星际闪烁相关 TEC 估算；主业并非地面 GNSS TEC 流水线。公开仓可克隆。

#### [Boston-College-ISR-Ionospheric-Studies](https://www.bc.edu/bc-web/research/sites/institute-for-scientific-research/research/ionospheric-studies.html)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

波士顿学院科学研究所电离层研究方向介绍，涵盖全球扰动、层析与闪烁对 GNSS 影响等。可作为 Seemala GPS-TEC 等工具的机构背景页；部分站点可能对非浏览器客户端返回 406，建议用常规浏览器打开。

#### [IMSP-MGS](https://essr.esa.int/project/ionosphere-modular-software-package-imsp-mgs)  
*🏷️ 官方*

语言：unknown · 许可：ESA Community License v2.4 Strong Copyleft (Type 1) · 星标约：— · 宿主：official_site

ONERA/RDA/IEEC 在 ESA TDE 框架下开发、经 ESSR 发布的 Ionosphere Modular Software Package，用于仿真 GNSS-R、SAR 与雷达测深等任务几何及 30 MHz–3 GHz 主要电离层效应。适合任务设计与电离层误差敏感性分析，而非地面 GNSS TEC 产品流水线。源码经 ESSR git 提供，许可为 ESA Community License v2.4 Strong Copyleft；下载需 ESSR 账号。

#### [IonTools](https://github.com/rumkex/IonTools)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：BSD-3-Clause · 星标约：— · 宿主：github

GitHub rumkex/IonTools，偏辅助脚本/小工具集合，用来补主流程里零散步骤。关键 TEC/GIM 结论建议用主流库复核，勿把过时脚本当生产基线。

## IRI模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyglow](https://github.com/timduly4/pyglow) | pyglow：上层大气气候态 Python 库 | Python/Fortran | 117 | 🏷️ 个人社区 核心 |
| [iri2016](https://github.com/space-physics/iri2016) | iri2016：IRI-2016 现代语言接口 | Fortran | 85 | 🏷️ 个人社区 |
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | PyIRI：纯 Python 国际参考电离层 | Python | 48 | 🏷️ 个人社区 核心 |
| [iri2020](https://github.com/space-physics/iri2020) | iri2020：IRI-2020 Fortran/Python 可调用封装 | Fortran | 25 | 🏷️ 个人社区 |
| [pyIRI2016](https://github.com/rilma/pyIRI2016) | pyIRI2016：IRI-2016 的 f2py Python 包装（非 space-physics/iri2016） | Python/Fortran | 21 | 🏷️ 个人社区 |
| [iri90](https://github.com/space-physics/iri90) | iri90：IRI-90 国际参考电离层的 Python 封装 | Python | 8 | 🏷️ 个人社区 |
| [FIRI.jl](https://github.com/fgasdia/FaradayInternationalReferenceIonosphere.jl) | FIRI.jl：法拉第国际参考电离层 Julia 工具 | Julia | 5 | 🏷️ 个人社区 |
| [PyIRTAM](https://github.com/victoriyaforsythe/PyIRTAM) | IRTAM 系数下载与全球网格电子密度重建（纯 Python，对接 PyIRI） | Python | 4 | 🏷️ 个人社区 核心 |
| [FIRI-2018](https://github.com/AlexT1983/FIRI-2018) | FIRI-2018：低电离层经验模型 FIRI-2018 的 MATLAB 实现 | MATLAB | 2 | 🏷️ 个人社区 |
| [iricore](https://github.com/MIST-Experiment/iricore) | ctypes 包装 IRI-2016/2020，可算 VTEC/STEC 并更新指数文件 | Python/Fortran | 2 | 🏷️ 高校实验室 |
| [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/) | CCMC-IRI-online：NASA CCMC 的 IRI-2020 在线运行与说明 | — | — | 🏷️ 官方 |
| [GAMBIT-Database-Reader-Java](https://giro.uml.edu/GAMBIT/GambitReader_Java_V0.1.zip) | 官方示例：GAMBIT 数据库 Java 读入/解包（拉 IRTAM 系数） | Java | — | 🏷️ 官方 |
| [IRI-2001-package](https://irimodel.org/IRI-2001/) | IRI-2001-package：官方 Fortran 历史版源码目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2007-package](https://irimodel.org/IRI-2007/) | IRI-2007-package：官方 Fortran 历史版源码目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2012-package](https://irimodel.org/IRI-2012/) | IRI-2012-package：官方 Fortran 包（含轨道剖面示例） | Fortran | — | 🏷️ 官方 |
| [IRI-2016-package](https://irimodel.org/IRI-2016/) | IRI-2016-package：官方 Fortran 源码与系数目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2020-package](https://irimodel.org/IRI-2020/) | IRI-2020-package：官方 Fortran/系数/许可证与压缩包 | Fortran | — | 🏷️ 官方 |
| [IRI-2026-package](https://irimodel.org/IRI-2026/) | IRI-2026-package：官方最新 Fortran 源码包 | Fortran | — | 🏷️ 官方 核心 |
| [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/) | IRI-COMMON-FILES：各版 IRI 共用系数目录 | — | — | 🏷️ 官方 核心 |
| [IRI-Fortran](https://irimodel.org/) | IRI：国际参考电离层官方 Fortran | Fortran | — | 🏷️ 官方 核心 |
| [IRI-indices](https://irimodel.org/indices/) | IRI-indices：IRI 官方太阳/地磁指数文件发布页 | — | — | 🏷️ 官方 |
| [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model) | IRI-MATLAB：官方指向的 File Exchange 封装 | MATLAB | — | 🏷️ 官方 核心 |
| [IRI-Plas-SPIM-IZMIRAN](https://www.izmiran.ru/ionosphere/weather/grif/SPIM/) | IRI-Plas/SPIM：IZMIRAN 等离子体层扩展 IRI Fortran | Fortran | — | 🏷️ 官方 |
| [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters) | IRI2020_parameters：IRI2020 运行参数/系数整理仓 | MATLAB | — | 🏷️ 个人社区 ★ |
| [IRTAM-Coefficient-Reader-Fortran](https://giro.uml.edu/GAMBIT/IrtamReader_Fortran_V1.0.zip) | 官方示例：IRTAM 系数 Fortran 读入器（对接 IRI 同化） | Fortran | — | 🏷️ 官方 |
| [pyFIRI2018](https://bitbucket.org/ozolotov/pyfiri2018) | pyFIRI2018：FIRI-2018 D 区参考电离层 Python 实现 | Python | — | 🏷️ 个人社区 |

### 详细说明

#### [pyglow](https://github.com/timduly4/pyglow)  
*🏷️ 个人社区 核心*

语言：Python/Fortran · 许可：MIT · 星标约：117 · 宿主：github

把 IRI 等上层大气经验模型接到 Python，irimodel.org 在「pyglow」一行直接链到本仓库，说明它是社区里常用的 IRI-2012/2016 包装路径。适合脚本化批量取 Ne/Te 剖面、和 GNSS TEC 产品做气候态对照。底层仍依赖 Fortran 模型文件与指数更新；跟官方最新 IRI-2020/2026 发布节奏可能不同步，精密业务应核对所绑版本。许可 MIT，比部分需注册的官方 C 发行更好集成。

#### [iri2016](https://github.com/space-physics/iri2016)  
*🏷️ 个人社区*

语言：Fortran · 许可：MIT · 星标约：85 · 宿主：github

把 IRI-2016 Fortran 核心包一层现代语言接口，结果更接近社区惯用的官方模型。适合需要标准 IRI-2016 输出的论文。编译环境与 IRI-2020 升级需注意；纯 Python 偏好可选 PyIRI。

#### [PyIRI](https://github.com/victoriyaforsythe/PyIRI)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：48 · 宿主：github

不绑 Fortran 也能跑 IRI 气候学电子密度/TEC 等，便于嵌进 Python 科研脚本。适合需要气候学背景场或与 GNSS TEC 对比的工作。实时扰动与闪烁物理不在 IRI 范围；要官方 IRI 数值一致性时可对照 iri2020 封装。

#### [iri2020](https://github.com/space-physics/iri2020)  
*🏷️ 个人社区*

语言：Fortran · 许可：MIT · 星标约：25 · 宿主：github

跟进 IRI-2020 的可调用封装，便于更新背景场或做版本差异试验。依赖 Fortran 构建；与 GNSS 实测 TEC 同化需另接观测链。

#### [pyIRI2016](https://github.com/rilma/pyIRI2016)  
*🏷️ 个人社区*

语言：Python/Fortran · 许可：MIT · 星标约：21 · 宿主：github

用现代 CMake + f2py 暴露 iriwebg，便于在 Python 中调用 IRI-2016。与 space-physics/iri2016、官方 irimodel 目录并存时，注意不要混淆仓库名与系数版本。需要编译器链；要最新物理选项仍应回 irimodel.org 的 IRI-2020/2026。

#### [iri90](https://github.com/space-physics/iri90)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：8 · 宿主：github

把经典 IRI-90 Fortran/数据流程包装成 Python，便于脚本化计算给定时刻与位置的电子密度等廓线，适合课堂演示与快速对比 GNSS TEC。输入一般为日期、地理坐标与高度网格；输出为模式密度/相关参量。局限：模型年代较早，精度与 IRI-2016/2020 有差距；依赖编译/数据文件配置，不替代业务 GIM。仓库已于 2022-08 归档（只读）。

#### [FIRI.jl](https://github.com/fgasdia/FaradayInternationalReferenceIonosphere.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：5 · 宿主：github

面向 FIRI（Faraday International Reference Ionosphere）廓线的 Julia 读写与处理库，常用于低频/VLF 传播与低电离层研究。输入为 FIRI 剖面数据与查询坐标；输出为便于后续射线或吸收计算的电子密度廓线。局限：覆盖低电离层场景，不是 GNSS L 波段 TEC 改正主工具；需 Julia 环境。

#### [PyIRTAM](https://github.com/victoriyaforsythe/PyIRTAM)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

面向 GIRO/IRTAM 同化产物：可读/下载 IRTAM 系数，在给定全球网格与全日时间轴上同时评估 foF2/hmF2 等并重建 Ne。适合把实时同化电离层接到 Python 科研流水线，与气候态 PyIRI 对照。系数来自 LGDC/GAMBIT 接口，需遵守站点访问节奏；不是官方 Fortran irirtam.for 的逐行移植，数值对比请以 IRI-2020 包内 irirtam 子程序为参照。

#### [FIRI-2018](https://github.com/AlexT1983/FIRI-2018)  
*🏷️ 个人社区*

语言：MATLAB · 许可：BSD-3-Clause · 星标约：2 · 宿主：github

FIRI（Faraday-International Reference Ionosphere）侧重低电离层电子密度，本仓库给出 2018 版 MATLAB 实现，可与 IRI 高层剖面拼接思路对照。输入为位置/时间等模型参数；输出低电离层 Ne。局限：主要服务低频/VLF/吸收研究，对 GNSS L 波段 TEC 贡献相对小；MATLAB 生态。

#### [iricore](https://github.com/MIST-Experiment/iricore)  
*🏷️ 高校实验室*

语言：Python/Fortran · 许可：MIT · 星标约：2 · 宿主：github

把官方 Fortran IRI 编进可 pip 安装的 Python 包，暴露剖面与垂直/斜 TEC，并提供指数文件更新入口。适合 Linux 科研脚本里快速取气候态背景。文档写明主要处理 OUTF、未实现 OARR 用户输入；Windows 需 WSL，且维护节奏偏慢，跟 IRI-2026 对齐前应核对所绑 Fortran 版本。

#### [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：— · 宿主：official_site

NASA 社区协调建模中心提供的 IRI 在线计算与模型说明入口，适合快速查剖面、看输入开关，而不是本地二次开发。要嵌入自己的 GNSS/TEC 流水线仍需下载 irimodel Fortran 或 Python/MATLAB 包装。页面会指向模型版本与相关文献，可作为官方文档跳板。

#### [GAMBIT-Database-Reader-Java](https://giro.uml.edu/GAMBIT/GambitReader_Java_V0.1.zip)  
*🏷️ 官方*

语言：Java · 许可：UMLCAR/GIRO distribution (see archive) · 星标约：— · 宿主：official_site

GIRO 提供的 Java 示例，用于从 GAMBIT 侧取系数并解包。适合需要脚本化批量取同化系数、又不走 Python 的环境。示例级代码，商用实时 Situation Room 另需订阅协议；系数下载请遵守站点建议的请求间隔。

#### [IRI-2001-package](https://irimodel.org/IRI-2001/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

更早的官方 IRI 发行，主要用于历史复现。系数与选项与当代版本差异大，不适合作为现行 GNSS 电离层改正基准；对照阅读可看官网更新说明与 Bilitza 综述。

#### [IRI-2007-package](https://irimodel.org/IRI-2007/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

官方保留的 IRI-2007 发行，便于复现该年代论文或对比模型演进。新项目应改用 IRI-2020/2026；仅当审稿或历史对比需要锁定旧物理选项时再下载本目录。

#### [IRI-2012-package](https://irimodel.org/IRI-2012/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

官方 IRI-2012 发行目录。官网特别提到该版带有 iriorbit 一类沿卫星轨道取 IRI 参数的示例程序，适合空间任务剖面复现与旧论文对照。功能与数据源已有后续版本更新；除非复现 2012 时代结果，新项目优先 IRI-2020/2026，MATLAB/pyglow 用户也要分清自己绑的是哪一代。

#### [IRI-2016-package](https://irimodel.org/IRI-2016/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

COSPAR/URSI IRI 工作组在 irimodel.org 发布的 IRI-2016 源码目录，含 Fortran 子程序、系数与说明。很多文献与 MATLAB/pyglow 包装仍对齐这一代。新研究若无追踪官方最新物理选项，应同时看 IRI-2020/2026；指数文件需按官网说明单独更新。

#### [IRI-2020-package](https://irimodel.org/IRI-2020/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

irimodel.org 上 IRI-2020 的文件目录，可直接获取 00_iri.zip/tar、许可证与各 .for 系数文件。便于固定版本复现实验与回归测试。新版本（如 IRI-2026）请回主站查看；Python 封装见社区 iri2020/PyIRI，官方数值仍以此目录为准。

#### [IRI-2026-package](https://irimodel.org/IRI-2026/)  
*🏷️ 官方 核心*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

irimodel.org 上标注日期最新的 IRI Fortran 发行目录，工作组持续更新的气候态电离层国际标准模型入口。做与最新文献对齐的 Ne/Te/离子成分剖面时优先从这里取源码与系数。指数文件仍需按官网说明单独更新；Python/MATLAB 包装未必已跟上 2026，绑定前核对版本号。

#### [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/)  
*🏷️ 官方 核心*

语言：— · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

irimodel 写明：除版本包外通常还要 COMMON FILES（若 zip 未打进包内）。缺公共系数时编译或运行常失败。搭本地 IRI 时与具体版本目录、最新 INDICES 一起下载；不要只克隆 GitHub 包装而漏官方公共文件。

#### [IRI-Fortran](https://irimodel.org/)  
*🏷️ 官方 核心*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

国际参考电离层 IRI 的官方 Fortran 发行入口，由 COSPAR/URSI 工作组维护，提供电子密度、温度、离子成分与 vTEC 等气候态输出。可直接下载 IRI-2020/2026 压缩包与指数文件。适合作为标准对照模型写入论文复现实验；实时闪烁或扰动过程需另接观测或同化产品，不宜单独当作业务电离层改正引擎。

#### [IRI-indices](https://irimodel.org/indices/)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：— · 宿主：official_site

官方指数文件入口（如 ap、IG、F10.7 相关序列）。IRI 按日期查内部指数，过期指数会让剖面偏离。业务或论文复现应定期更新本页文件；pyglow/第三方包装若自带指数，也要核对其时效。

#### [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model)  
*🏷️ 官方 核心*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：— · 宿主：official_site

irimodel.org 官方列出的 IRI MATLAB 入口（MathWorks File Exchange，含 2012/2016）。适合已在 MATLAB 做气候态对比、不想先编译 Fortran 的用户。包内 license.txt 为 BSD 两条款许可（作者 Drew Compston），代码通过 curl 调用 IRI 在线接口而非本地 Fortran；追最新物理更新仍应回 irimodel.org / IRI 主源码。

#### [IRI-Plas-SPIM-IZMIRAN](https://www.izmiran.ru/ionosphere/weather/grif/SPIM/)  
*🏷️ 官方*

语言：Fortran · 许可：scientific distribution (cite required) · 星标约：— · 宿主：official_site

IZMIRAN 官方 IRI-Plas/SPIM 下载页：Fortran 主程序与系数包，把 IRI 扩展到等离子体层并可同化 GPS TEC。适合需要等离子体层 TEC 的气候态/同化试验；编译与系数版本须与页面 ZIP 对齐，不是 GNSS STEC 观测解算器。

#### [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：— · 宿主：github

整理 IRI2020 运行所需参数/资源，减少自己找系数文件的时间。宜与 iri2020 主仓库搭配，而非独立模型。

#### [IRTAM-Coefficient-Reader-Fortran](https://giro.uml.edu/GAMBIT/IrtamReader_Fortran_V1.0.zip)  
*🏷️ 官方*

语言：Fortran · 许可：UMLCAR/GIRO distribution (see archive) · 星标约：— · 宿主：official_site

从 GAMBIT 页下载的 Fortran 示例，演示如何解析 IRTAM 系数消息并与 IRI 模型联用。适合本地同化/复现研究，而非网页看图。仅为示例读入器，完整实时同化流水线与系数服务条款见 GIRO/GAMBIT；Python 侧可对照 PyIRTAM。

#### [pyFIRI2018](https://bitbucket.org/ozolotov/pyfiri2018)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：— · 宿主：other

Oleg Zolotov 等实现的 FIRI-2018（Friedrich 等更新的低电离层经验模式）Python 包，用 xarray 对论文附表电子密度剖面插值，服务 VLF/低频传播与 D 区研究。Apache-2.0。原 GitLab 镜像注明已迁至 Bitbucket；与 GitHub 上其他 FIRI 表格式发布可并存。请同时引用 Friedrich et al. 2018 与 Zolotov et al. SoftwareX 2021。

## 掩星

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [COSMIC-IONPRF-Ne-TEC](https://github.com/HassanNooreldeen/COSMIC-IONPRF-NC-CDAAC-UCAR-Ne-TEC) | COSMIC-IONPRF-Ne-TEC：COSMIC CDAAC 掩星 Ne/TEC MATLAB 下载分析 | MATLAB | 9 | 🏷️ 个人社区 |
| [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research) | CDAAC_COSMIC-TEC：Jupyter 处理 COSMIC 掩星 NetCDF 做 TEC | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [IonOccAnalysis](https://github.com/wonder2019WHU/IonOccAnalysis) | IonOccAnalysis：GNSS 电离层掩星数据分析（个人仓） | C++ | 2 | 🏷️ 个人社区 |

### 详细说明

#### [COSMIC-IONPRF-Ne-TEC](https://github.com/HassanNooreldeen/COSMIC-IONPRF-NC-CDAAC-UCAR-Ne-TEC)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：9 · 宿主：github

下载并筛选 COSMIC 掩星电子密度廓线，做多年统计分析与教学绘图。输入为 CDAAC 访问与时间范围；输出为 Ne/TEC 相关统计。局限：依赖数据中心政策；不是地基双频 TEC。

#### [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：2 · 宿主：github

Jupyter 流程读取 CDAAC/COSMIC 掩星 NetCDF，面向 TEC 与掩星电离层剖面研究，便于复现空基电子含量分析。做 GNSS-RO 与空间天气的人可作起点。不是地基双频 TEC 或 GIM 软件；产品字段、版本与质量控制需对照 CDAAC 官方文档，结果宜与地基网交叉验证。不同任务期产品版本不要混用后直接拼时间序列。

#### [IonOccAnalysis](https://github.com/wonder2019WHU/IonOccAnalysis)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：2 · 宿主：github

C++ 工具面向 GNSS 电离层掩星数据处理与分析，适合理解 LEO—GNSS 链路反演电子密度。输入为掩星观测/相关产品；输出为分析与可视化结果。局限：文档与维护节奏需自行评估；与地基双频 TEC 流程不同。

## GIM

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现（维护者自有，此处不展开） | MATLAB | 104 | 🏷️ 个人社区 🚩 核心 |
| [M_GIM-zcytju](https://github.com/zcytju/M_GIM) | M_GIM：多系统全球/区域电离层 GIM 建模（MATLAB） | MATLAB | 23 | 🏷️ 个人社区 ★ |
| [mosgim2](https://github.com/PadArt/mosgim2) | mosgim2：相位差法构建 GNSS 全球电离层图 | Python | 17 | 🏷️ 个人社区 ★ |
| [TEC-Maps-of-Nepal](https://github.com/Binabh/TEC-Maps-of-Nepal) | TEC-Maps-of-Nepal：UNAVCO CORS 生成尼泊尔区域 TEC 图 | Python | 12 | 🏷️ 个人社区 |
| [csonde-gnss-ionosphere](https://github.com/csonde/gnss) | csonde-gnss-ionosphere：RINEX 解析与格网/球谐电离层建模 | C | 10 | 🏷️ 个人社区 |
| [mosgim](https://github.com/gnss-lab/mosgim) | mosgim：Padokhin 早期 MosGIM 相位差 GIM 实现 | Python | 6 | 🏷️ 高校实验室 |
| [real-time-ionospheric-maps-Kalman](https://github.com/AlexandraKoulouri/real-time-ionospheric-maps-using-Kalman) | real-time-ionospheric-maps-Kalman：南美区域集合卡尔曼电离层图 | MATLAB | 3 | 🏷️ 个人社区 |
| [GIM_fusion_VLBI](https://github.com/arrueegg/GIM_fusion_VLBI) | GIM_fusion_VLBI：把 VLBI 信息融入全球电离层图 | Python | 1 | 🏷️ 个人社区 |
| [m_gim-PANXIONG](https://github.com/PANXIONG-CN/m_gim) | m_gim-PANXIONG：小体量 MATLAB GIM 脚本草稿 | MATLAB | 1 | 🏷️ 个人社区 ★ |
| [DiffIonMap](https://github.com/Jin-Whu/DiffIonMap) | IONEX 差分成图：对比分析中心或风暴扰动 | Python | 0 | 🏷️ 个人社区 |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS.IonosphereMaps：Java 电离层图工具 | Java | — | 🏷️ 个人社区 ★ |
| [Ionospheric-TEC-Kriging-Turkiye](https://github.com/skaratay/Ionospheric-TEC-Kriging-Turkiye) | Ionospheric-TEC-Kriging-Turkiye：土耳其区域 TEC 克里金/GPR | MATLAB | 0 | 🏷️ 高校实验室 |
| [Zenodo-VTEC-map-generation-SBAS](https://doi.org/10.5281/zenodo.10058636) | Zenodo-VTEC-map-generation-SBAS：SBAS 误差模型用 VTEC 图生成补充包 | MATLAB | 0 | 🏷️ 高校实验室 |

### 详细说明

#### [SH-GIM](https://github.com/Atlas2001-web/SH-GIM)  
*🏷️ 个人社区 🚩 核心*

维护者自有仓库，本索引仅作分类收录，不作详细介绍。请直接查看上游 README。

#### [M_GIM-zcytju](https://github.com/zcytju/M_GIM)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：— · 星标约：23 · 宿主：github

面向多系统全球与区域电离层建模的 MATLAB 工具（仓库描述：Multi-system global and regional ionospheric modeling）。适合已有 MATLAB 电离层工作流的人试用。请自行核验 IONEX/球谐输入输出约定；与 PANXIONG 的 m_gim-PANXIONG 小脚本不是同一项目。

#### [mosgim2](https://github.com/PadArt/mosgim2)  
*🏷️ 个人社区 ★*

语言：Python · 许可：MIT · 星标约：17 · 宿主：github

MosGIM 系第二代实现，侧重相位差思路从 GNSS 观测建 GIM，Python 栈便于接到现有数据流水线。适合研究组快速试算区域/全球 TEC 图。文档与工程化程度不如商业或大机构产品；球谐/网格参数需自行调，可与 gnss-tec、同类 GIM 工具做方法对比。

#### [TEC-Maps-of-Nepal](https://github.com/Binabh/TEC-Maps-of-Nepal)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：12 · 宿主：github

加德满都大学本科毕业设计：按日期与测站自动从 UNAVCO 下载 CORS 观测、从 CODE 下载月 DCB，生成尼泊尔区域 TEC 图并输出 IONEX，带 Tkinter 图形界面和理论报告。MIT 许可，依赖 georinex、pymap3d 等。方法偏教学/区域试验，非全球 GIM 产品；UNAVCO 已并入 EarthScope，脚本里的下载地址可能需要更新。

#### [csonde-gnss-ionosphere](https://github.com/csonde/gnss)  
*🏷️ 个人社区*

语言：C · 许可：GPL-3.0 · 星标约：10 · 宿主：github

BME（匈牙利）学生论文配套个人代码：含 RINEX 解析、格网电离层模型、球谐模型求解与 PCA 等，适合作为区域建模教学示例。局限：偏研究原型；构建与输入约定需读论文/源码；GPL。

#### [mosgim](https://github.com/gnss-lab/mosgim)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

MosGIM 早期公开版本，便于追溯相位差 GIM 的原始流程。适合读论文后对照算法步骤。维护与功能完整度不如 mosgim2；新项目建议优先 mosgim2，本仓库作历史对照即可。

#### [real-time-ionospheric-maps-Kalman](https://github.com/AlexandraKoulouri/real-time-ionospheric-maps-using-Kalman)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：3 · 宿主：github

用 Ensemble Kalman Filter 重建南美区域电离层图，展示实时/近实时制图思路。输入为区域 GNSS TEC 相关观测量；输出为时序电离层图。局限：区域与方法绑定；工程化 GIM/IONEX 生产需额外封装。

#### [GIM_fusion_VLBI](https://github.com/arrueegg/GIM_fusion_VLBI)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：1 · 宿主：github

探索将 VLBI 相关信息融入 GIM 的数据同化/融合流程，拓展传统纯 GNSS GIM。局限：研究仓、星数低；输入数据与实验配置需读论文/脚本；非业务 GIM 软件。

#### [m_gim-PANXIONG](https://github.com/PANXIONG-CN/m_gim)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：— · 星标约：1 · 宿主：github

个人小仓 MATLAB GIM 相关脚本，适合课程作业或方法草稿。功能面窄，不宜单独承担业务化建图；更完整的多系统建模见 zcytju/M_GIM。

#### [DiffIonMap](https://github.com/Jin-Whu/DiffIonMap)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：0 · 宿主：github

读入两份 IONEX，生成差分 TEC 图，便于对比分析中心产品或风暴扰动相对变化。极简、久未更新。不负责产品下载与质量控核；批量业务制图请用专业 IONEX/GIM 流水线。

#### [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps)  
*🏷️ 个人社区 ★*

语言：Java · 许可：Apache-2.0 · 星标约：— · 宿主：github

gurkanguldas 的 Java 仓库，面向 GNSS 电离层图处理与展示。适合 JVM 技术栈快速查看 TEC 图；算法深度与产品化程度以 README 为准，科研级 GIM 仍建议对照 IGS/CODE 流程。

#### [Ionospheric-TEC-Kriging-Turkiye](https://github.com/skaratay/Ionospheric-TEC-Kriging-Turkiye)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：0 · 宿主：github

用普通克里金（及 GPR 表述）做土耳其上空 TEC 时空分析，覆盖太阳周 24–25 风暴个例，属于区域插值建图示例。局限：区域与个例绑定；MATLAB；推广到全球网格需改观测网与协方差模型。

#### [Zenodo-VTEC-map-generation-SBAS](https://doi.org/10.5281/zenodo.10058636)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：CC-BY-4.0 · 星标约：0 · 宿主：zenodo

Tampere University 发布的 VTEC 图生成代码/数据补充（VTEC_FORZENODO.zip），用于支撑星基导航电离层误差模型研究与复现。包内为 MATLAB 脚本（Main.m 与 lib/）和预存的 TEC_HourMap.mat，示例给随机用户位置取 VTEC。局限：README 说明是论文代码的简化版，只给 VTEC、不含 STEC 与星座几何；文件声明 CC-BY-4.0，使用需引用 Imad 等人论文。

## TEC预报/ML

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tec_forecast](https://github.com/mauriciodev/tec_forecast) | tec_forecast：深度学习全球 TEC 图预报示例 | Jupyter Notebook | 31 | 🏷️ 个人社区 ★ |
| [tec_prediction-ONERA](https://github.com/aboulch/tec_prediction) | tec_prediction-ONERA：ConvLSTM/U-Net 全球 TEC 图预报 | Python | 19 | 🏷️ 高校实验室 |
| [DeepPredTEC](https://github.com/vtsuperdarn/DeepPredTEC) | DeepPredTEC：深度学习 GPS TEC 图预报 | Python | 13 | 🏷️ 高校实验室 |
| [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM) | ED-AttConvLSTM：注意力 ConvLSTM 的 TEC 图预报 | Jupyter Notebook | 10 | 🏷️ 个人社区 |
| [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting) | IAG 研究组 ML 预报 VTEC 的教学示例 | Jupyter Notebook | 9 | 🏷️ 高校实验室 ★ |
| [Global-TEC-forecasting-DL](https://github.com/Laboratorio-Computacion-Cientifica/Global-TEC-forecasting-for-space-weather-application-based-on-deep-learning-techniques) | Global-TEC-forecasting-DL：全球 TEC 24h LSTM/GRU/CNN 流水线 | Python | 6 | 🏷️ 高校实验室 |
| [IonCast-Heliolab2025](https://github.com/FrontierDevelopmentLab/2025-HL-Ionosphere) | IonCast-Heliolab2025：NASA FDL ConvLSTM/GNN/SFNO 电离层预报 | Python | 5 | 🏷️ 高校实验室 |
| [ionopy](https://github.com/spaceml-org/ionopy) | ionopy：SpaceML Time-Fusion Transformer 电离层预报 | Python | 4 | 🏷️ 高校实验室 |
| [TEC-MoLLM](https://github.com/PANXIONG-CN/TEC-MoLLM) | TEC-MoLLM：GNN+时序 CNN+LLM（LoRA）全球 TEC 预报 | Python | 4 | 🏷️ 个人社区 |
| [IonoBench](https://github.com/Mert-chan/IonoBench) | IonoBench：全球电离层时空预报模型基准框架 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [gps-tec-cnn-lstm-attention](https://github.com/hyy-why/gps-tec-cnn-lstm-attention) | 论文配套：注意力机制 TEC 时序预测示例 | Python | 1 | 🏷️ 个人社区 |
| [Ion-Phys-Toolkit](https://github.com/PANXIONG-CN/Ion-Phys-Toolkit) | Ion-Phys-Toolkit：TEC 预报物理信息学习最小复现包 | Python | 0 | 🏷️ 个人社区 |
| [ionospheric-tec-forecasting-IISC](https://github.com/codewithavra/ionospheric-tec-forecasting) | ionospheric-tec-forecasting-IISC：单站 TEC 日前预报 | Jupyter Notebook | 0 | 🏷️ 个人社区 |
| [PMGC-SimVP](https://github.com/OnlyYouNotInCity/PMGC-SimVP) | PMGC-SimVP：多尺度门控卷积+SimVP 全球 TEC 预报 | Python | 0 | 🏷️ 高校实验室 |
| [SpatioTECformer](https://github.com/research1011/SpatioTECformer) | SpatioTECformer：多尺度 CNN+Transformer 的 TEC 网格预报（PyTorch） | Python | 0 | 🏷️ 个人社区 |
| [TEC-forecast-F107](https://github.com/hekaixuan-atm/TEC-forecast) | 空间非均匀 F10.7 强迫的全球 TEC 预报代码 | Python | 0 | 🏷️ 个人社区 |

### 详细说明

#### [tec_forecast](https://github.com/mauriciodev/tec_forecast)  
*🏷️ 个人社区 ★*

语言：Jupyter Notebook · 许可：MIT · 星标约：31 · 宿主：github

用 Keras/TF2 在全球电离层图上做 TEC 预报实验，含 de Paulo 等 2023（GPS Solut）次日 GIM 预报的编码-解码 ConvLSTM，部分模型参考 Boulch 2018。适合学 ML+空间天气交叉的人对照复现。不是业务预报系统；数据切分、基线与物理约束要自己补齐，可与 ED-AttConvLSTM 等对比。

#### [tec_prediction-ONERA](https://github.com/aboulch/tec_prediction)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 (research); commercial contact ONERA · 星标约：19 · 宿主：github

卷积循环网络做电离层活动/TEC 图预报的早期公开代码，后被多篇 DeepTEC 类工作引用。研究非商业用途按仓库说明为 GPLv3，商业需联系 ONERA。适合当 ML TEC 基线；年代较早（约 2018），依赖与数据管道需自行适配现行 IONEX/GIM。

#### [DeepPredTEC](https://github.com/vtsuperdarn/DeepPredTEC)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：13 · 宿主：github

面向 GPS TEC 图时空预报的深度学习开源实现（SuperDARN 相关团队），可复现论文结构并作空间天气基线。适合电离层 ML 实验。工程同化与多源融合需自建；输入网格、缺失填充与评分指标要与业务 GIM 对齐后再谈业务化。

#### [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：no licence granted (README: contact authors before reuse) · 星标约：10 · 宿主：github

编码器—解码器加注意力的 ConvLSTM，针对 TEC 图时序预报。适合复现相关论文结构。工程部署与多源同化不在范围；输入 GIM 分辨率与缺失值处理需自建。

#### [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting)  
*🏷️ 高校实验室 ★*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：9 · 宿主：github

IAG ICCT「大地测量中的机器学习」联合研究组示例，用公开流程演示 VTEC 机器学习预报，Apache-2.0 许可清晰。适合课堂与方法入门。模型深度与业务指标达不到业务空间天气预报标准。

#### [Global-TEC-forecasting-DL](https://github.com/Laboratorio-Computacion-Cientifica/Global-TEC-forecasting-for-space-weather-application-based-on-deep-learning-techniques)  
*🏷️ 高校实验室*

语言：Python · 许可：AGPL-3.0 · 星标约：6 · 宿主：github

覆盖采数、预处理、建模与评估的完整深度学习流水线，比较 LSTM、GRU、CNN 做提前 24 小时全球 TEC 预报，并用 DVC 管数据版本。偏工程化复现空间天气业务原型。数据大文件走 DVC 远端，克隆后需按 dvc.yaml 拉数；许可为 AGPL-3.0。

#### [IonCast-Heliolab2025](https://github.com/FrontierDevelopmentLab/2025-HL-Ionosphere)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：5 · 宿主：github

Frontier Development Lab 电离层-热层孪生项目仓库，含 IonCast ConvLSTM 训练/评估脚本，分支覆盖 GNN 与球面 FNO；配套 Zenodo 数据与 ionopy 引用。适合复现较新的全球 TEC/电离层动力学深度学习基线。环境与数据体量不小；ionopy 子目录可能滞后，维护说明指向 spaceml-org/ionopy。

#### [ionopy](https://github.com/spaceml-org/ionopy)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：4 · 宿主：github

SpaceML 维护的电离层预报代码与笔记本，强调时间融合 Transformer，被 IonCast/Heliolab 仓库引用为较新实现。适合跟深度学习 TEC/电离层序列模型。仓库与 README 均未声明许可证，使用或再分发前应先联系作者；数据与训练配置需自备。

#### [TEC-MoLLM](https://github.com/PANXIONG-CN/TEC-MoLLM)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：4 · 宿主：github

多模态深度学习 TEC 预报原型，组合图网络、时序卷积与大模型 LoRA 微调。输入为历史 TEC/空间天气特征；输出预报场。局限：算力与复现成本高；与经典物理/经验模式比可解释性弱；许可未标明。

#### [IonoBench](https://github.com/Mert-chan/IonoBench)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：MIT · 星标约：2 · 宿主：github

提供对比多种时空深度学习/统计模型预报全球电离层的基准流程，便于复现论文实验。输入为历史 TEC/GIM 类数据与模型配置；输出为预报评分与对比。局限：侧重 ML 基准而非物理模式；数据准备与算力要求不低。

#### [gps-tec-cnn-lstm-attention](https://github.com/hyy-why/gps-tec-cnn-lstm-attention)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：1 · 宿主：github

论文配套的 CNN-BiLSTM 注意力 TEC 预测代码，目标是复现实验而非业务运行。星标与文档有限，数据准备脚本完整度需自查。业务空间天气预报请用业务模式或同化产品。

#### [Ion-Phys-Toolkit](https://github.com/PANXIONG-CN/Ion-Phys-Toolkit)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

物理信息（PINN/类 PINN）TEC 预报的精简发布，便于复现论文设定。局限：仓库自称最小发布版（minimal release）；功能面窄；需自备训练数据。

#### [ionospheric-tec-forecasting-IISC](https://github.com/codewithavra/ionospheric-tec-forecasting)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：MIT · 星标约：0 · 宿主：github

针对 IISC 站分钟级 TEC，对比序列到序列 LSTM 与 CNN+窗口 Transformer，并把预报 TEC 换成 L1/L2/L5 电离层延迟。教学与单站实验很直观，还带 RoTI 相关分析笔记本。站点/时段特定，不是全球 GIM 预报器；体量含数据集，克隆较大。

#### [PMGC-SimVP](https://github.com/OnlyYouNotInCity/PMGC-SimVP)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：0 · 宿主：github

深度学习全球 TEC 预报实现（PMGC-SimVP），Apache-2.0。局限：研究代码；训练数据与超参需自行对齐论文；推理前要有历史 TEC 栅格。

#### [SpatioTECformer](https://github.com/research1011/SpatioTECformer)  
*🏷️ 个人社区*

语言：Python · 许可：no licence granted (README: research use, contact author) · 星标约：0 · 宿主：github

把多尺度卷积、自适应融合与 Transformer 编码器拼成 71×73 网格 TEC 预报流水线，模块拆成 model/enhanced_cnn 等文件，代码量小但完整可跑。适合读论文式复现。未标 SPDX 许可证；训练依赖作者 HDF5 特征文件，需自备或按 README 路径改。

#### [TEC-forecast-F107](https://github.com/hekaixuan-atm/TEC-forecast)  
*🏷️ 个人社区*

语言：Python · 许可：no formal licence (README: academic and research use) · 星标约：0 · 宿主：github

论文配套实验：在深度学习 TEC 预报中引入空间非均匀 F10.7 强迫，探索太阳辐射空间差异的影响。适合复现与对比基线。仓库体量小、数据划分依赖作者设定，非业务级物理/同化模式。

## SBAS电离层

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EGNOS_SDK_Core](https://github.com/EpsilonRTD/EGNOS_SDK_Core) | EGNOS_SDK_Core：EGNOS Android SDK 核心（兼容 Android 5） | Java | 5 | 🏷️ 个人社区 |
| [EGNOSTools](https://github.com/DfAC/EGNOSTools) | EGNOSTools：EGNOS 处理支持工具（含 EMS 转换） | Python | 1 | 🏷️ 个人社区 |

### 详细说明

#### [EGNOS_SDK_Core](https://github.com/EpsilonRTD/EGNOS_SDK_Core)  
*🏷️ 个人社区*

语言：Java · 许可：EUPL-1.1 · 星标约：5 · 宿主：github

在移动端集成 EGNOS/SBAS 改正能力的 SDK 核心，便于理解终端如何消费 SBAS 电离层格网。输入为 SDK API 与 SBAS 数据通道；输出为改正后的定位相关量。局限：偏移动集成；不是开源 EMS 全链路解析教程。

#### [EGNOSTools](https://github.com/DfAC/EGNOSTools)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：1 · 宿主：github

辅助 EGNOS/SBAS 消息与 EMS 等格式处理的小工具集，便于课堂演示 MT18/MT26 电离层格网改正链路。输入为 EGNOS/EMS/RINEX 相关文件；输出为转换/解析结果。局限：仓库很小，需与规范文档对照使用。

## NeQuick

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NequickG](https://github.com/tpl2go/NequickG) | NequickG：Galileo NeQuick-G Python 版 | Python | 45 | 🏷️ 个人社区 核心 |
| [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR) | Nequick-ITUR：ITU-R NeQuick 2 的 Python/Fortran 封装 | Fortran | 4 | 🏷️ 个人社区 |
| [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC) | NeQuickJRC：JRC NeQuickG 的 ANSI-C 可编译整理 | C | 4 | 🏷️ 个人社区 |
| [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code) | NeQuick G：Galileo 单频电离层改正 | C | — | 🏷️ 官方 核心 |
| [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code) | NeQuick2-ICTP：ICTP 官方 NeQuick 2 源码申请页 | Fortran | — | 🏷️ 官方 核心 |
| [NeQuick2-MLF2](https://github.com/SkydelSolutions/nequick2-mlf2) | NeQuick2-MLF2：NeQuick-G 思路改写（Gustave Eiffel/Safran） | C | 0 | 🏷️ 个人社区 |
| [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model) | NeQuickG-ESSR：ESA 登记的 Galileo 电离层改正实现 | C | — | 🏷️ 官方 |

### 详细说明

#### [NequickG](https://github.com/tpl2go/NequickG)  
*🏷️ 个人社区 核心*

语言：Python · 许可：— · 星标约：45 · 宿主：github

实现 Galileo 单频改正常用的 NeQuick-G，便于与 Galileo ICD/性能评估对照。适合 SBAS/单频仿真与教学。官方 JRC 参考实现之外的社区版，数值对齐要用标准算例核验；C 版可见 NeQuickJRC。

#### [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：4 · 宿主：github

为 ITU-R NeQuick 2 Fortran 核心提供 Python 包装，便于在脚本里调用气候学电离层模型做链路预算或单频改正对比。与 Galileo 专用 NeQuick-G（NequickG 仓库）分属不同标准版本，数值对齐要用官方算例；亦可对照 PyIRI、iri2016，避免混用模型参数。

#### [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC)  
*🏷️ 个人社区*

语言：C · 许可：EUPL v1 (JRC NeQuickG C sources) + MIT (Python package per pyproject.toml) · 星标约：4 · 宿主：github

整理 JRC NeQuickG 的 C 实现便于编译调用，偏工程嵌入。作者声明非 JRC 原开发托管；C 源码头注释为 JRC 的 EUPL v1，Python 包在 pyproject.toml 中标 MIT，使用前核对版本。需要 Python 胶水时可与 NequickG 对照。

#### [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code)  
*🏷️ 官方 核心*

语言：C · 许可：EUPL-1.2 · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心提供的 NeQuick G 官方 C11 实现（含 JRC 库与测试驱动），面向 Galileo 单频用户电离层延迟改正。需注册并接受 EUPL 后下载加密包。与社区 GitHub 镜像相比应以本页为权威来源；气候态 NeQuick2 仍见 ICTP，二者算法与输入不同，集成前请对照 Galileo OS 电离层文档。

#### [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code)  
*🏷️ 官方 核心*

语言：Fortran · 许可：scientific distribution (request) · 星标约：— · 宿主：official_site

阿卜杜斯·萨拉姆国际理论物理中心 T/ICT4D 发布的 NeQuick 2 气候态电子密度模型，含 ITU 系数与太阳活动/modip 文件。面向穿电离层传播与 TEC 积分研究。源码需向维护者邮件申请；若做 Galileo 单频接收机改正，请改用 GSC 的 NeQuick G 官方实现以免版本混淆。

#### [NeQuick2-MLF2](https://github.com/SkydelSolutions/nequick2-mlf2)  
*🏷️ 个人社区*

语言：C · 许可：EUPL-1.2 · 星标约：0 · 宿主：github

该仓库提供 NeQuick2-MLF2 电离层模式实现，说明基于 Galileo NeQuick-G 算法并由 Gustave Eiffel University / Safran Trusted 4D 修改。对需要在仿真器或接收机侧嵌入 NeQuick 族改正的开发者有参考价值。局限：星数为 0；与官方 NeQuick2/NeQuick-G 发布渠道并行，引用与验证需自行对照 ICTP/ESA/JRC 参考实现；文档相对简略。

#### [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model)  
*🏷️ 官方*

语言：C · 许可：ESA Community License v2.4 · 星标约：— · 宿主：official_site

ESA 软件资源库中的 NeQuick G 条目，说明该实现按 Galileo 单频电离层改正算法文档适配，区别于 ITU 气候态 NeQuick Fortran。注册后获取，许可为 ESA Community License。日常下载更常走欧盟 GSC 页面；本页适合核对 ESA 侧登记信息与许可类型。

## HF射线追踪

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Ionort-raytrace](https://github.com/blair3sat/ionosphere-rt) | Ionort-raytrace：INGV IONORT 三维 HF 射线追踪（MATLAB + Fortran） | MATLAB | 17 | 🏷️ 高校实验室 |
| [PyLap](https://github.com/HamSCI/PyLap) | PyLap：HamSCI 对 PHaRLAP 的 Python 接口 | Python | 14 | 🏷️ 高校实验室 |
| [PyRayHF](https://github.com/victoriyaforsythe/PyRayHF) | PyRayHF：纯 Python 电离层 HF 射线追踪 | Python | 10 | 🏷️ 个人社区 |
| [Raytrace-Model](https://github.com/kyruzic/Raytrace-Model) | 电离层中电波三维传播的 MATLAB 射线追踪 | MATLAB | 7 | 🏷️ 个人社区 |
| [hfpytrace](https://github.com/shibaji7/trace) | hfpytrace：HF 射线追踪（PHaRLAP 等色散，含 PyIRI 例） | Python | 1 | 🏷️ 个人社区 |
| [PHaRLAP](https://www.dst.defence.gov.au/our-technologies/pharlap-provision-high-frequency-raytracing-laboratory-propagation-studies) | PHaRLAP：DSTG HF 电离层射线追踪 Matlab 工具箱 | Fortran/MATLAB | — | 🏷️ 官方 |

### 详细说明

#### [Ionort-raytrace](https://github.com/blair3sat/ionosphere-rt)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：CC-BY-NC-ND-3.0 (INGV IONORT MATLAB code per MATLAB/README.TXT; Julia port unstated) · 星标约：17 · 宿主：github

INGV 开发的 IONORT（IONOsphere Ray-Tracing）三维 HF 射线追踪程序：MATLAB 界面（ionort.m / ionort_gui.m）负责参数输入与绘图，并调用预编译的 Windows Fortran 求解器（Chapman 或离散网格电子密度，分有/无地磁场共四个版本）。维护者主要把注释从意大利语译成英文；README 说明旧式定长格式的 Fortran 源码大概率已无法直接编译，Julia 重写只有几行起步代码。适合 HF/GNSS 传播与层析正演的教学参考；INGV 的 MATLAB 部分按 CC BY-NC-ND 3.0 发布，不可商用、不可改作再分发。

#### [PyLap](https://github.com/HamSCI/PyLap)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：14 · 宿主：github

用 Python/C 调用 PHaRLAP Fortran 引擎，摆脱 Matlab 授权门槛，保留建 IRI 电离层、射线追踪与绘图等核心流程。业余与科研 HF 传播实验友好。安装目前偏 Ubuntu/x86，且必须先向 DSTG 申请 PHaRLAP 本体与 Intel Fortran 运行库；本身不是可独立运行的完整射线引擎。

#### [PyRayHF](https://github.com/victoriyaforsythe/PyRayHF)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：10 · 宿主：github

Victoriya Forsythe 等发布的 HF 射线工具，从电子密度剖面计算虚高与二维射线路径，文档在 Read the Docs，与同作者 PyIRI/PyIRTAM 生态衔接自然。适合教学与轻量传播实验。能力相对 PHaRLAP 全磁离子 3D NRT 更聚焦；复杂回波与三维磁离子场景仍可能需要更重的引擎。

#### [Raytrace-Model](https://github.com/kyruzic/Raytrace-Model)  
*🏷️ 个人社区*

语言：MATLAB · 许可：GPL-3.0 · 星标约：7 · 宿主：github

在给定电子密度模型下做三维射线追踪，服务传播教学与研究型实验。GPL 许可、偏原型实现。输入电离层模型与数值步长需用户自行校验；业务链路预算请对照 ITU/专业传播软件。

#### [hfpytrace](https://github.com/shibaji7/trace)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

开源 HF 射线追踪包，文档与示例演示 IRI 笛卡尔/球坐标斜向射线，密度后端可接 PyIRI。适合想在 Python 里做传播几何、又不愿只绑 Matlab mex 的人。仓库内仍可见 pharlap_lib 相关痕迹，授权与依赖请读上游 LICENSE/文档；与 HamSCI PyLap 路线不同，选型前先确认你是否已有 DSTG PHaRLAP。

#### [PHaRLAP](https://www.dst.defence.gov.au/our-technologies/pharlap-provision-high-frequency-raytracing-laboratory-propagation-studies)  
*🏷️ 官方*

语言：Fortran/MATLAB · 许可：DSTG request freeware (no redistribution) · 星标约：— · 宿主：official_site

提供 2D/全磁离子 3D 数值射线追踪与解析追踪，可挂 IRI/IGRF 或用户网格。HF 传播与回波几何研究里事实上的常用引擎，Fortran 核心经 mex 进 Matlab。许可为 DSTG 科学发放：个人申请、禁止再分发。若缺 Matlab，可看 HamSCI PyLap 开源接口，但仍需另行申请 PHaRLAP 本体。

## IONEX/TEC图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [INX_Editor](https://github.com/1acheng/INX_Editor) | INX_Editor：跨平台 IONEX 文件编辑工具 | — | 16 | 🏷️ 个人社区 ★ |
| [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX) | INPE-TEC-Maps-IONEX：INPE TEC 图与 IONEX 生成 | Python | 15 | 🏷️ 个人社区 ★ |
| [ionex](https://github.com/gnss-lab/ionex) | ionex：Python IONEX 读入 | Python | 12 | 🏷️ 高校实验室 核心 |
| [ionex-rs](https://github.com/nav-solutions/ionex) | ionex-rs：Rust IONEX 解析库 | Rust | 7 | 🏷️ 个人社区 核心 |
| [IonMap](https://github.com/Jin-Whu/IonMap) | IonMap：由 IONEX 绘制电离层 TEC 地图 | Python | 4 | 🏷️ 个人社区 |
| [rtcm2ionex](https://github.com/d-roma/rtcm2ionex) | rtcm2ionex：RTCM VTEC 消息转 IONEX | Python | 3 | 🏷️ 个人社区 |
| [ionex_formatter](https://github.com/gnss-lab/ionex_formatter) | gnss-lab IONEX 写出/格式化模块（与 ionex 读取库配套） | Python | 2 | 🏷️ 高校实验室 |
| [Ionex_Parser](https://github.com/ajayraghASL/Ionex_Parser) | Ionex_Parser：读取 IONEX 返回网格 TEC 的脚本 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [ionex_reader](https://github.com/bbrawar/ionex_reader) | IONEX→xarray 读取与可视化（支持 JPL/CODE/ESA 等产品） | Python | 2 | 🏷️ 高校实验室 |
| [mgfernan-pygnss](https://github.com/mgfernan/pygnss) | Python GNSS 工具集：IONEX/GIM、Hatanaka、与 NeQuick 对比 CLI | Python | 2 | 🏷️ 个人社区 |
| [ionex-analyzer](https://github.com/matador96/ionex-analyzer) | ionex-analyzer：Electron/React 的 IONEX 可视化 | JavaScript | 0 | 🏷️ 个人社区 |
| [MathWorks-ionex_reader](https://www.mathworks.com/matlabcentral/fileexchange/172149-ionex_reader) | MathWorks-ionex_reader：IONEX 读图与单点 TEC 时序 | MATLAB | 0 | 🏷️ 个人社区 |

### 详细说明

#### [INX_Editor](https://github.com/1acheng/INX_Editor)  
*🏷️ 个人社区 ★*

语言：— · 许可：GPL-3.0 · 星标约：16 · 宿主：github

面向 IONEX 的桌面编辑与检查，改网格、头信息或局部 TEC 值时比手改文本省事。适合产品质检与教学演示。不是 TEC 估计算法库；重建 TEC 仍需 PyTECGg/gnss-tec 等。

#### [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX)  
*🏷️ 个人社区 ★*

语言：Python · 许可：no formal licence (README: free reproduction, keep author credit) · 星标约：15 · 宿主：github

把电离层预报/分析系统输出整理成 TEC 图和 IONEX，方便与国际产品格式对齐。适合需要 IONEX 交换或南美区域 TEC 图的用户。对全球多分析中心产品融合支持有限；格式细节建议对照 IONEX 标准与 INX_Editor 一起核。

#### [ionex](https://github.com/gnss-lab/ionex)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：12 · 宿主：github

gnss-lab 出品的轻量 IONEX 读入模块，把网格 TEC 图载入 Python 便于插值与绘图。做 GIM 对比、穿刺点改正或教学演示时很省事。不生成 GIM、不算 STEC；写 IONEX 或更高阶分析可看 nav-solutions/ionex（Rust）与 IonMap、rtcm2ionex 等配套工具，和 gnss-tec 流水线衔接自然。

#### [ionex-rs](https://github.com/nav-solutions/ionex)  
*🏷️ 个人社区 核心*

语言：Rust · 许可：MPL-2.0 · 星标约：7 · 宿主：github

GeoRust/nav-solutions 生态下的 IONEX 库，强调类型安全与可嵌入 rinex-cli 一类工具链，适合已在 Rust GNSS 栈中处理格网电离层改正的人。Python 科研脚本更常直接用 gnss-lab/ionex；两者互补而非替代完整 GIM 建模，写图与球谐仍看 MosGIM2 等 GIM 工具。

#### [IonMap](https://github.com/Jin-Whu/IonMap)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：4 · 宿主：github

读取 IONEX 并绘制电离层 TEC 地图，适合论文插图、课程展示全球或区域 VTEC 分布。功能集中在可视化，不估计 STEC、不做球谐或层析建模；与 gnss-lab/ionex、ionosphere-plotting 等输出对照使用更完整，批处理画图时可脚本化调用。色标与投影选择会影响观感，分析结论仍看数值产品。

#### [rtcm2ionex](https://github.com/d-roma/rtcm2ionex)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：3 · 宿主：github

把实时 RTCM 垂直 TEC 类消息写成 IONEX 格网文件，便于与事后 GIM 工具链、画图脚本对接。做实时电离层流试验或把 NTRIP 电离层产品落地存档时有用。星标少、场景窄，不替代双频 STEC 估计或球谐 GIM 建模，可与 gnss-lab/ionex、IonMap 串联。输出格网分辨率受源 RTCM 消息定义约束。

#### [ionex_formatter](https://github.com/gnss-lab/ionex_formatter)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

与 gnss-lab/ionex 同属 Padokhin 工具链一侧，侧重把网格化 TEC 整理成可交换的 IONEX。适合自建 GIM/区域图后需要标准化交付的场景。文档与星标很少，集成前请跑样例并对照 IONEX 1.0/1.1 规范；读取侧仍推荐同组织的 ionex。

#### [Ionex_Parser](https://github.com/ajayraghASL/Ionex_Parser)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：2 · 宿主：github

轻量解析 IONEX，取出各历元 TEC 格网，适合作业与快速画图。输入为 IONEX 文件；输出为 TEC 数组/表格。局限：功能覆盖面小于完整读写库；大文件与 RMS 图支持需自测。

#### [ionex_reader](https://github.com/bbrawar/ionex_reader)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

按文件头解析网格，把 TEC/RMS 装进 xarray，可选日夜界与地磁纬线叠加。适合快速抽检 IGS 各分析中心 IONEX、做差分或画图。功能偏读与展示，不负责建图或写回完整 IONEX；写格式可对照 gnss-lab/ionex、ionex_formatter 或 pygnss。

#### [mgfernan-pygnss](https://github.com/mgfernan/pygnss)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

作者亦维护 NeQuickJRC；本库提供 IONEX 加载、GIM handler、ionex_diff（可对 NeQuick）以及 RINEX/Hatanaka 辅助。适合把电离层图产品接到脚本化质检。与 semuconsulting/pygnss* 系列同名空间易混淆，克隆时认准 mgfernan/pygnss；功能广度不如大型测地套件。

#### [ionex-analyzer](https://github.com/matador96/ionex-analyzer)  
*🏷️ 个人社区*

语言：JavaScript · 许可：— · 星标约：0 · 宿主：github

用 Electron/React 做的 IONEX 可视化桌面小应用，交互浏览格网 TEC 较友好，来源为毕业设计风格仓库。适合演示与教学展示。研究级批处理、插值、DCB 与建模请回到 Python/MATLAB 工具链；星标低，仓库已于 2023-04 归档（只读），当作原型参考即可，勿当生产依赖。若只需脚本绑图，优先轻量 Python 方案更易维护。

#### [MathWorks-ionex_reader](https://www.mathworks.com/matlabcentral/fileexchange/172149-ionex_reader)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：0 · 宿主：other

Bhuvnesh 发布的 ionex_reader 工具箱，可读取 IONEX、绘制 TEC/RMS 图并提取任意位置 TEC 时序，适合课堂快速可视化 IGS GIM。输入为 IONEX 文件与经纬坐标；输出为图与时序。局限：File Exchange 许可与更新节奏需查看页面；功能以读/画为主，不含球谐估解。

## TID

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tidd](https://github.com/vc1492a/tidd) | tidd：用 GPS sTEC 变化率异常检测 TID（海啸/地震等） | Jupyter Notebook | 10 | 🏷️ 高校实验室 |
| [hamsci_LSTID_detection](https://github.com/HamSCI/hamsci_LSTID_detection) | HamSCI 从业余无线电 spot 数据自动检测大尺度行进电离层扰动的代码 | Python | 7 | 🏷️ 高校实验室 |
| [t-fors](https://github.com/viventriglia/t-fors) | t-fors：TID 行进式电离层扰动预报组件 | HTML | 7 | 🏷️ 个人社区 |
| [DARNtids](https://github.com/w2naf/DARNtids) | SuperDARN TID 行进扰动检测工具 | Python | 4 | 🏷️ 高校实验室 |
| [psws-drf-tid-tools](https://github.com/N6RFM/psws-drf-tid-tools) | 基于 HamSCI Grape 数字 RF 记录估计 TID 传播速度与方向的 Python 流程 | Python | 4 | 🏷️ 个人社区 |
| [IonKit-NH](https://github.com/tanggdut/IonKit-NH) | IonKit-NH：MATLAB 多系统 GNSS TEC 自然灾害电离层扰动检测工具包（原作者仓） | MATLAB | — | 🏷️ 个人社区 ★ |
| [lstid_processing](https://github.com/USNavalResearchLaboratory/lstid_processing) | 美国海军研究实验室 C/NOFS IVM 与 SAMI3 大尺度 TID 分析工具包 | Python | 0 | 🏷️ 官方 |

### 详细说明

#### [tidd](https://github.com/vc1492a/tidd)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：10 · 宿主：github

JPL、罗马一大与 UCLA 合作的工具包：对地面接收机观测 GPS 卫星得到的 sTEC 变化率（d/dt）做异常检测，识别海啸、地震、爆炸等引起的行进式电离层扰动（TID），附方法笔记本。输入为 sTEC 时序；输出为异常检测结果。局限：研究案例向；虚警/漏检与空间天气干扰需注意。

#### [hamsci_LSTID_detection](https://github.com/HamSCI/hamsci_LSTID_detection)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：7 · 宿主：github

HamSCI（NASA SWO2R 团队，Frissell 等）开源的 LSTID 自动检测代码，MIT 许可并有 Zenodo DOI。输入为 CEDAR Madrigal 中 RBN、PSKReporter、WSPRNet 业余无线电 spot 的每日 HDF5，将 spot 按距离-时间分箱成热图，经预处理与边缘检测后做正弦拟合，给出大尺度 TID 的出现与周期（1–4.5 小时），附 Madrigal 下载脚本与依赖版本清单。提供了不同于 GNSS TEC 的 TID 独立观测途径，可与 Madrigal GNSS TEC、DARNtids 结果互证。运行环境要求 Python 3.11 与 Linux。

#### [t-fors](https://github.com/viventriglia/t-fors)  
*🏷️ 个人社区*

语言：HTML · 许可：MIT · 星标约：7 · 宿主：github

欧盟 Horizon 资助的 TID 预报相关开源组件/门户代码，面向扰动预警演示。输入为电离层扰动相关观测与模型配置；输出为 TID 预报产品。局限：业务可用性依赖数据源；与实时 GIM 生产不同。

#### [DARNtids](https://github.com/w2naf/DARNtids)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：4 · 宿主：github

面向 SuperDARN 雷达数据的 TID（Traveling Ionospheric Disturbance）检测与分析代码，GPL-3.0。适合将高频雷达观测与 GNSS TEC/TID 研究对照。依赖 SuperDARN 数据环境与雷达物理背景；不是 GNSS RINEX 处理链。

#### [psws-drf-tid-tools](https://github.com/N6RFM/psws-drf-tid-tools)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

业余无线电爱好者开源的 Python 管线，MIT 许可，面向 HamSCI Grape 系列个人空间天气站的 Digital RF I/Q 记录：从多站多普勒变化估计行进电离层扰动的传播速度和方向，并附获取 Madrigal GNSS TEC 以作对比的脚本。README 明确说明平面波、单跳 F 层、中点垂直反射等简化假设，建议结合 Kp、AE 指数与 hamsci_LSTID_detection 结果判读。适合公民科学与 TID 教学，数值结论宜谨慎。近期仍在更新。

#### [IonKit-NH](https://github.com/tanggdut/IonKit-NH)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：GPL-3.0 · 星标约：— · 宿主：github

IonKit-NH 的原作者仓（Tang L.），MATLAB 工具包，用 GPS/GLONASS/Galileo/BDS 双频组合求 TEC，生成时间-距离图和二维 TEC 扰动图，检测地震、海啸、火山喷发激发的行进式电离层扰动。代码以 IonKit-NH.zip 分发（18 个 .m 文件加示例 RINEX 与 TEC 数据），用法见用户手册；使用请引用 Tang 2024（Earthquake Research Advances）。ohm1122/IonKit-NH 是它的 fork（维护者星标来源），自 2024-05 复制后没有任何新提交。

#### [lstid_processing](https://github.com/USNavalResearchLaboratory/lstid_processing)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

美国海军研究实验室（NRL）官方开源的 Python 包，MIT 许可，已发布 PyPI 并有 ReadTheDocs 文档与 Zenodo DOI。用于在 C/NOFS 卫星 CINDI 离子速度计数据中识别中、大尺度行进电离层扰动（TID），并提供处理 SAMI3 电离层模式输出及下载案例模式数据的例程，服务于 Burrell 等 2026 年 JGR 论文的可复现性。作者说明不会频繁更新，更适合作为 TID 研究参考实现，可与 GNSS TEC 类 TID 检测工具对照。

## 中性大气

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [msise00](https://github.com/space-physics/msise00) | NRLMSISE-00 的 Python/Matlab 封装 | Python | 63 | 🏷️ 个人社区 |
| [pymsis](https://github.com/SWxTREC/pymsis) | pymsis：NRLMSIS 中性大气的现代 Python 接口 | Python | 39 | 🏷️ 高校实验室 |
| [hwm93](https://github.com/space-physics/hwm93) | hwm93：HWM93 水平风模型 Python/Matlab 接口 | Python | 23 | 🏷️ 个人社区 |
| [Python-NRLMSISE-00](https://github.com/DeepHorizons/Python-NRLMSISE-00) | Python-NRLMSISE-00：NRLMSISE-00 经验大气的纯 Python 移植 | Python | 14 | 🏷️ 个人社区 |
| [hwm14](https://github.com/gemini3d/hwm14) | hwm14：NRL 水平风场模型开源 CMake 构建 | Fortran | 7 | 🏷️ 高校实验室 |

### 详细说明

#### [msise00](https://github.com/space-physics/msise00)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：63 · 宿主：github

把经典 NRLMSISE-00 中性大气模式包成 Python/Matlab 接口，便于算密度、温度等高度剖面。GNSS 气象与火箭/掩星背景大气、以及部分电离层驱动耦合研究常作辅料。注意它是中性大气模式，不是 TEC/IRI；引用与系数版本请按 NRL 原文献与仓库说明。

#### [pymsis](https://github.com/SWxTREC/pymsis)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：39 · 宿主：github

SWxTREC 维护的 NRLMSIS Python 接口，用于计算卫星高度中性大气密度与成分，MIT 许可。服务低轨大气阻力与空间天气背景，与 GNSS/LEO 精密定轨相关。依赖上游 MSIS 系数与输入太阳/地磁指数。适合科研脚本，而非 GNSS 观测解算。

#### [hwm93](https://github.com/space-physics/hwm93)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：23 · 宿主：github

space-physics 对经典 NASA Horizontal Wind Model 93 的 Python/Matlab 封装，常与电离层/热层研究及 GNSS 相关大气分析联用。MIT 许可；提供仍被文献引用的 HWM93 基线接口（新版见 hwm14）。模型年代较早，现代工作请对照 HWM14 或其他再分析风场产品验证。需 Fortran 编译器（f2py 构建）。仓库已于 2022-08 归档（只读）。

#### [Python-NRLMSISE-00](https://github.com/DeepHorizons/Python-NRLMSISE-00)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：14 · 宿主：github

NRLMSISE-00（2001）经验中性大气模型的 Python 移植，MIT 许可。与 msise00/pymsis 形成不同实现对照，便于无 Fortran 包装环境下估算密度。输出依赖历元与地磁/太阳输入；模型有适用高度范围。适合轨道与空间环境教学试验。

#### [hwm14](https://github.com/gemini3d/hwm14)  
*🏷️ 高校实验室*

语言：Fortran · 许可：Apache-2.0 · 星标约：7 · 宿主：github

gemini3d 维护的 NRL Horizontal Wind Model 2014 可构建库，用 CMake 生成 libhwm14，供上层大气/电离层耦合与轨迹仿真调用。Apache-2.0。是中性风经验模型而非 GNSS 处理软件；旧 HWM93 包装仓已归档，新集成优先此仓。

## 法拉第旋转

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RMextract](https://github.com/lofar-astron/RMextract) | RMextract：ASTRON 射电天文 TEC/RM 经典工具（已继任） | C | 36 | 🏷️ 官方 |
| [ionFR](https://github.com/csobey/ionFR) | ionFR：用 IGRF+IONEX 估计电离层法拉第旋转 | Python | 12 | 🏷️ 个人社区 |
| [spinifex](https://git.astron.nl/RD/spinifex) | ASTRON Spinifex：射电天文 TEC/RM 电离层工具 | Python | 4 | 🏷️ 官方 |

### 详细说明

#### [RMextract](https://github.com/lofar-astron/RMextract)  
*🏷️ 官方*

语言：C · 许可：GPL-3.0 · 星标约：36 · 宿主：github

荷兰 ASTRON 长期使用的 RMextract，面向射电干涉测量从 GPS TEC 与地磁模型估计旋转量度等。仓库注明已被 Spinifex 继任且不再积极开发，但仍广泛出现在文献与旧流程中。适合对照复现；新项目优先 Spinifex。许可 GPL-3.0。

#### [ionFR](https://github.com/csobey/ionFR)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：12 · 宿主：github

给定视线、地理位置与历元，结合 IGRF 地磁场与 IONEX TEC 图估计电离层法拉第旋转（FR），GPL-3.0。服务射电天文与极化校正，也与 GNSS 电离层产品消费相关。依赖外部 IONEX/IGRF 文件质量；输出是 FR 估计而非 STEC 重建。适合电离层传播旁路分析，而非 PPP 改正生成。

#### [spinifex](https://git.astron.nl/RD/spinifex)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：4 · 宿主：gitlab

荷兰 ASTRON 维护的 Spinifex，用纯 Python 从 IONEX/TOMION 等模型估计视线 TEC 与旋转量度（RM），面向 LOFAR 等干涉测量改正。可 pip 安装 GitLab 主仓；GitHub 仅为镜像。依赖外部 IONEX 下载与地磁模型，不是 GNSS 双频 STEC 估计算法本身。

## 雷达/ISR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyDARN](https://github.com/SuperDARN/pydarn) | SuperDARN 官方社区维护的 Python 数据可视化库 | Python | 38 | 🏷️ 高校实验室 |
| [SuperDARN RST](https://github.com/SuperDARN/rst) | SuperDARN 雷达软件工具包 RST：原始数据处理、拟合与对流图生成 | C | 28 | 🏷️ 高校实验室 |
| [inscar](https://github.com/engeir/inscar) | 计算斜向磁场条件下非相干散射谱的 Python 库（支持非麦克斯韦分布） | Python | 7 | 🏷️ 高校实验室 |
| [LPI](https://github.com/ilkkavir/LPI) | 奥卢大学非相干散射雷达电压级数据滞后剖面反演 R 包（MPI 版） | R | 5 | 🏷️ 高校实验室 |
| [MIPS](https://github.com/MITHaystack/MIPS) | MIT Haystack 非相干散射雷达系统性能仿真器 | Python | 5 | 🏷️ 高校实验室 |
| [resolvedvelocities](https://github.com/amisr/resolvedvelocities) | AMISR 视线速度反演三维离子漂移与电场矢量的 Python 实现 | Python | 5 | 🏷️ 官方 |
| [BAFIM](https://github.com/ilkkavir/BAFIM) | GUISDAP 非相干散射分析的贝叶斯时间滤波先验模块 | MATLAB | 4 | 🏷️ 高校实验室 |
| [isr-raw](https://github.com/space-physics/isr-raw) | 处理 PFISR 等非相干散射雷达原始 I/Q 电压数据的 Python 工具 | Python | 4 | 🏷️ 个人社区 |

### 详细说明

#### [pyDARN](https://github.com/SuperDARN/pydarn)  
*🏷️ 高校实验室*

语言：Python · 许可：LGPL-3.0 · 星标约：38 · 宿主：github

SuperDARN 数据分析工作组维护的 Python 可视化库，LGPL-3.0 许可，有 Zenodo DOI 与 ReadTheDocs 文档，可 pip 安装。支持绘制距离-时间图、扇区扫描图、对流图、功率谱等，读取 FITACF、grid、map 等 SuperDARN 标准格式（底层读写由 pyDARNio 负责），新版本增加 FITACF 去趋势与对流图真实速度。适合研究高纬电离层对流及其与 GNSS 闪烁、TEC 结构的联系。数据需另行从 FRDR、BAS 等镜像获取。仓库持续维护。

#### [SuperDARN RST](https://github.com/SuperDARN/rst)  
*🏷️ 高校实验室*

语言：C · 许可：GPL-3.0 · 星标约：28 · 宿主：github

SuperDARN 数据分析工作组（DAWG）维护的 Radar Software Toolkit，GPL-3.0 许可，C 语言命令行工具集并有 Zenodo DOI。负责从 rawacf 做 ACF 拟合生成 fitacf，再经网格化、球谐拟合生成全球对流图，是 SuperDARN 标准数据产品的官方处理链。文档分为 ReadTheDocs 安装教程与 API 说明两站，支持 Linux 与 macOS，Windows 暂不支持。适合需要自行重处理 SuperDARN 数据的研究者，与 pyDARN 可视化配合使用。

#### [inscar](https://github.com/engeir/inscar)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：7 · 宿主：github

特罗姆瑟大学研究者发布的 Python 包，MIT 许可，已上架 PyPI 并有 ReadTheDocs 文档、测试与覆盖率 CI。可在雷达视线与地磁场成任意斜角时，针对各向同性但不一定为麦克斯韦分布的电子速度分布计算非相干散射功率谱，用于研究超热电子、等离子体线等效应。适合学习 ISR 理论或检验 EISCAT、AMISR 谱拟合假设，不直接处理实测数据。与 LPI 分别处于理论谱计算与原始数据反演两端，可配合阅读。

#### [LPI](https://github.com/ilkkavir/LPI)  
*🏷️ 高校实验室*

语言：R · 许可：BSD-2-Clause · 星标约：5 · 宿主：github

奥卢大学 Ilkka Virtanen 开发的 Lag Profile Inversion R 包，BSD-2-Clause 许可并有 Zenodo DOI。从电压级非相干散射雷达采样出发，反卷积得到各距离门的滞后剖面（自相关函数），是后续拟合电子密度、温度等参数的前一步；当前主分支为适配 HPC 的 MPI 版，数据 I/O 由 LPI.gdf、LPI.KAIRA 等配套包提供。适合 EISCAT/EISCAT_3D 等雷达的原始数据研究者。使用说明见仓库内 PDF 手册与教程，README 本身较简。

#### [MIPS](https://github.com/MITHaystack/MIPS)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-2-Clause · 星标约：5 · 宿主：github

MIT 海斯塔克天文台发布的 Incoherent Scatter Performance Simulator，BSD-2-Clause 许可。基于物理的雷达性能模型，考虑一阶与二阶效应及测量统计，可评估不同波形带宽、中心频率、占空比、阵列布局、单站/双站配置与功率孔径组合下的信噪比、测量速度和参数估计误差，用于下一代地球空间雷达的设计权衡。适合 ISR 系统设计与观测模式规划，不处理实测数据。README 附引用信息；文档较精简，需要一定雷达理论基础。

#### [resolvedvelocities](https://github.com/amisr/resolvedvelocities)  
*🏷️ 官方*

语言：Python · 许可：GPL-3.0 · 星标约：5 · 宿主：github

AMISR 官方 GitHub 组织发布的 Python 包，GPL-3.0 许可，实现 Heinselman 与 Nicolls 的贝叶斯重建算法，从 PFISR/RISR 多波束视线速度反演三维离子漂移速度和电场矢量。提供按磁纬分箱（F 区局地对流）与按高度分箱（E 区速度剖面）两种命令行程序，均以配置文件驱动，依赖 numpy 与 apexpy。输入为 SRI ISR 数据库中的处理后 HDF5 文件。适合研究高纬对流与电离层不规则体驱动的用户。

#### [BAFIM](https://github.com/ilkkavir/BAFIM)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：4 · 宿主：github

奥卢大学 Ilkka Virtanen 开发的 GUISDAP 扩展模块，BSD-2-Clause 许可，MATLAB 实现。以时间上的贝叶斯滤波替代 GUISDAP 默认基于 IRI 的先验，并在距离方向使用相关先验保持剖面平滑，可用于沿磁力线与斜向波束以及远程站数据，从而提高 EISCAT 等雷达参数拟合的时间分辨率与稳定性。新版 GUISDAP 已内置该模块，仅需另装 flipchem 离子化学模块。与 LPI 同一作者，适合 ISR 数据分析人员。

#### [isr-raw](https://github.com/space-physics/isr-raw)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：4 · 宿主：github

space-physics 组织（Michael Hirsch 等）发布的 Python 工具集，Apache-2.0 许可，面向 Poker Flat AMISR 手动申请的原始 I+jQ 电压样本，可按单脉冲读取原始功率、自相关与等离子体线数据，并通过 ini 配置的绘图程序检查湍流活动（含 CFAR 检测）等现象。适合需要比标准处理产品更高时间分辨率的 ISR 研究，如极光与阿尔芬波相关散射。原始数据需向 SRI 专门申请；代码近年更新较少，依赖版本需自行适配。
