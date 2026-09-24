# 电离层 / Ionosphere
> **239** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

## 层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoTomo](https://github.com/Joshuaalbert/IonoTomo) | 射电天文射线追踪与电离层层析仿真 | Jupyter Notebook | 11 | 🏷️ 个人社区 |
| [iono-tomography](https://github.com/brianbreitsch/iono-tomography) | 电离层层析相关 Python 实验代码 | Python | 4 | 🏷️ 高校实验室 |
| [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl) | 多 GNSS 星间链路辅助电离层层析仿真 | — | 2 | 🏷️ 个人社区 |
| [317Lab-tomography](https://github.com/317Lab/tomography) | Lynch 火箭实验室电离层层析成像代码库 | Jupyter Notebook | 1 | 🏷️ 高校实验室 |
| [GNSS_TOM](https://github.com/sailvssea/GNSS_TOM) | GNSS 对流层与电离层层析 C++ 实现（风格仿 GPSTk） | C++ | 1 | 🏷️ 高校实验室 |
| [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy) | 层析几何矩阵构建（C++，yujieqing） | C++ | — | 🏷️ 个人社区 ★ |
| [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation) | 体素电离层层析射线段矩阵计算（原作者仓，已归档） | C++ | 0 | 🏷️ 个人社区 |

### 详细说明

#### [IonoTomo](https://github.com/Joshuaalbert/IonoTomo)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：11 · 宿主：github

结合射线追踪与射电观测仿真做电离层层析，面向射电天文与空间天气交叉课题，Notebook 形式便于改参数。适合需要正演电离层对射电信号影响的人。不是 GNSS 双频 TEC 业务软件；地基 GNSS 体素层析可并行参考 SegmentsComputation 与 synthetic 层析仓库。仿真假设与真实射电阵几何差异需要单独评估。

#### [iono-tomography](https://github.com/brianbreitsch/iono-tomography)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：4 · 宿主：github

开源层析实验代码，便于搭建体素/基函数反演原型。输入为 STEC 与几何；输出为电子密度反演结果。局限：文档与完整度需自行评估；工程稳健性弱于商业/大型实验室系统。

#### [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：2 · 宿主：github

仿真多 GNSS 星间链路（ISL）辅助的电离层层析，探索新观测几何对电子密度反演的贡献。适合读相关论文后复现实验设置与几何配置。公开星标低、偏研究原型，落地需自备真实 ISL 或地基数据接口；可与 SegmentsComputation、IonoTomo 对照正演与矩阵环节。仿真噪声模型应尽量贴近目标星座链路预算。

#### [317Lab-tomography](https://github.com/317Lab/tomography)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：— · 星标约：1 · 宿主：github

火箭/地基联合场景下的电离层层析教学与研究代码。输入为层析观测几何与 TEC；输出为二维/三维重建。局限：星数少、场景专用；需对照实验室文档。

#### [GNSS_TOM](https://github.com/sailvssea/GNSS_TOM)  
*🏷️ 高校实验室*

语言：C++ · 许可：unknown · 星标约：1 · 宿主：github

同时面向对流层水汽与电离层 TEC 的层析代码，C++ 实现并参考 GPSTk 风格。输入为 GNSS 相关观测量/几何；输出层析体素场。局限：星数低、文档少；电离层与对流层模块成熟度需实测；许可为 NOASSERTION。

#### [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：GPL-3.0 · 星标约：— · 宿主：github

yujieqing 仓库：为电离层层析准备几何/射线矩阵相关代码，可与同作者 SegmentsComputation 等配合。偏矩阵构造环节，不是完整层析反演或 TEC 预处理流水线；仓库活跃度与文档需自行评估。

#### [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：0 · 宿主：github

专注层析反演里体素穿越段（segment）几何矩阵的 C++ 实现，是三维电子密度反演的前置数值模块。原作者仓现已 archived；yxw027 同名仓为相同文件树副本，目录已去重只留本仓。不是完整层析软件，需自备观测方程与正则化。

## 电离层与PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PPP-RTK-Ionosphere](https://github.com/nickdaychen/PPP-RTK-Ionosphere) | MATLAB 侧 PPP-RTK 与电离层相关试验代码 | MATLAB | 7 | 🏷️ 个人社区 |
| [AETHER](https://github.com/LiZhengXiao99/AETHER) | PPP-RTK 用区域 STEC/VTEC/ZWD/ZTD 大气建模 | C++ | 6 | 🏷️ 高校实验室 |
| [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP) | 广域电离层模型与 PPP 相关实现 | C++ | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [PPP-RTK-Ionosphere](https://github.com/nickdaychen/PPP-RTK-Ionosphere)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：7 · 宿主：github

围绕 PPP-RTK 与电离层约束/改正的 MATLAB 试验代码，便于改映射函数与随机模型做对比实验。适合课堂与方法验证。仓库说明偏少，输入改正产品与参考真值需自行准备；实时流与多星座完备性不是其主场。

#### [AETHER](https://github.com/LiZhengXiao99/AETHER)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：6 · 宿主：github

从 GNSS 观测抽取大气延迟，构建区域 STEC/VTEC 与 ZWD/ZTD 模型以增强 PPP-RTK 收敛与精度。适合研究大气约束对网络 RTK/PPP-RTK 的贡献。结果依赖测站网密度与初始解质量；不能替代全球 GIM 或官方对流层格网产品。

#### [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：— · 宿主：github

把广域电离层模型和 PPP 联系起来的实践代码，适合看电离层约束如何进精密单点。完整度与星座支持需实测；系统级 PPP 仍建议对照 PRIDE、Ginan、raPPPid。

## 模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GEMINI3D](https://github.com/gemini3d/gemini3d) | 三维电离层流体-电动力学物理模型（Fortran，社区活跃） | Fortran | 69 | 🏷️ 高校实验室 |
| [GITM](https://github.com/GITMCode/GITM) | 全球电离层-热层模式 GITM 官方社区源码（Fortran） | Fortran | 28 | 🏷️ 高校实验室 |
| [Aether-IT-model](https://github.com/AetherModel/Aether) | 热层-电离层耦合物理模式 Aether（勿与 PPP-RTK 的 AETHER 混淆） | C++ | 27 | 🏷️ 高校实验室 |
| [TIE-GCM](https://github.com/NCAR/tiegcm) | NCAR 官方热层-电离层-电动力学环流模式 TIE-GCM v3 源码 | Fortran | 27 | 🏷️ 官方 |
| [LongwaveModePropagator.jl](https://github.com/fgasdia/LongwaveModePropagator.jl) | 地球-电离层波导中 VLF 长波模传播的 Julia 模型 | Julia | 26 | 🏷️ 高校实验室 |
| [sami2py](https://github.com/sami2py/sami2py) | NRL SAMI2 二维电离层模式的 Python 封装（运行/读档/绘图） | Python/Fortran | 21 | 🏷️ 高校实验室 |
| [sami3_gitm](https://github.com/jdhuba/sami3_gitm) | Huba 公开的 SAMI3/GITM 基础耦合 vanilla 代码 | Fortran | 7 | 🏷️ 官方 |
| [transcar](https://github.com/space-physics/transcar) | Transcar 一维沉降电离层模式 | Fortran | 7 | 🏷️ 高校实验室 |
| [mat_gemini](https://github.com/gemini3d/mat_gemini) | GEMINI 三维电离层模式的核心 MATLAB 脚本 | MATLAB | 6 | 🏷️ 高校实验室 |
| [SAMI2](https://github.com/NRL-Plasma-Physics-Division/SAMI2) | NRL SAMI2 二维电离层模式官方源码 | Fortran | 6 | 🏷️ 官方 |
| [IPE](https://github.com/NOAA-SWPC/IPE) | NOAA SWPC 电离层-等离子体层-电动力学模式 IPE | Fortran | 5 | 🏷️ 官方 |
| [AURORA](https://github.com/egavazzi/AURORA) | 电离层电子输运时变模型 AURORA | MATLAB | 3 | 🏷️ 高校实验室 |
| [ntcmg](https://github.com/lguldur/ntcmg) | Galileo NTCM-G 电离层改正算法的 C++ 实现 | C++ | 3 | 🏷️ 个人社区 |
| [FIRI-2018](https://github.com/AlexT1983/FIRI-2018) | 低电离层经验模型 FIRI-2018 的 MATLAB 实现 | MATLAB | 2 | 🏷️ 高校实验室 |
| [Klobuchar.jl](https://github.com/bukvoj/Klobuchar.jl) | Klobuchar 广播电离层延迟模型的 Julia 实现 | Julia | 2 | 🏷️ 个人社区 |
| [IRI_TID](https://github.com/w2naf/IRI_TID) | 在 PyIRI 电子密度场上叠加正弦 TID 扰动，供 HF 射线追踪 | Python | 1 | 🏷️ 高校实验室 |
| [SAMI3-4.00](https://github.com/jdhuba/sami3-4.00) | SAMI3 作者侧公开的 4.00 现代化 Fortran 源码 | Fortran | 1 | 🏷️ 官方 |
| [CCMC-SAMI3](https://ccmc.gsfc.nasa.gov/models/SAMI3~3.22) | CCMC 上的 SAMI3 模型入口（文档/运行请求/发布信息） | data-portal | — | 🏷️ 官方 |
| [gri-iono](https://gitlab.com/geosol-foss/python/gri-iono) | 跨电离层传播延迟与角度改正（Bent/IRI/NeQuick2/NeQuickG 等）Python 包 | Python | 0 | 🏷️ 个人社区 |
| [HAO-TGCM-portal](https://www.hao.ucar.edu/modeling/tgcm) | NCAR HAO TGCM/TIE-GCM 文档与发布说明门户 | data-portal | — | 🏷️ 官方 |
| [Klobuchar-study-code](https://github.com/KaijingZheng/Klobuchar-ionosphere-model-in-global-navigation-satellite-systems) | Klobuchar 广播电离层模型精度评估与改进探索的 MATLAB 代码 | MATLAB | 0 | 🏷️ 个人社区 |
| [NeQuick2-MLF2](https://github.com/SkydelSolutions/nequick2-mlf2) | 基于 Galileo NeQuick-G 思路改写的 NeQuick2-MLF2（Gustave Eiffel / Safran） | C | 0 | 🏷️ 个人社区 |
| [RIM](https://github.com/SWMFsoftware/RIM) | SWMF 体系中的 Ridley 电离层模式（RIM） | Fortran | 0 | 🏷️ 官方 |
| [SAMI3-3.22-CCMC-mirror](https://github.com/sylee918/SAMI3) | CCMC 发布的 SAMI3-3.22 源码镜像（个人搬运） | Fortran | 0 | 🏷️ 个人社区 |

### 详细说明

#### [GEMINI3D](https://github.com/gemini3d/gemini3d)  
*🏷️ 高校实验室*

语言：Fortran · 许可：Apache-2.0 · 星标约：69 · 宿主：github

GEMINI3D 是面向电离层的三维流体电动力学数值模式，用 Fortran 求解等离子体密度、速度与电场等，常用于极光区、不规则体和无线电传播相关的物理仿真。输入通常包括中性大气背景、太阳/地磁驱动与网格配置；输出为三维电子密度与相关场量的时序场。对 GNSS 用户而言，它不是直接从 RINEX 算 TEC 的工具，而是提供物理一致性的电子密度场，可再投影为 STEC/VTEC 做对比实验。局限：需要编译与并行计算资源，参数调校门槛高，不适合当作日常 GIM 生产流水线。

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

语言：Fortran · 许可：NCAR-academic · 星标约：27 · 宿主：github

TIE-GCM 是 NCAR HAO 发展的三维耦合热层-电离层-电动力学 GCM，GitHub 上现为官方开源仓库（含 src、scripts、tiegcmrun）。输入需配套数据文件（太阳、地磁、边界等），输出 netCDF 压力层/高度场。GNSS 研究里常拿来做风暴期 TEC/电子密度对照或数据同化背景。局限：需要 Fortran/MPI/netCDF 与较大输入数据集；业务化改正仍多用 IRI/NeQuick/GIM，而非直接跑 TIE-GCM。

#### [LongwaveModePropagator.jl](https://github.com/fgasdia/LongwaveModePropagator.jl)  
*🏷️ 高校实验室*

语言：Julia · 许可：MIT · 星标约：26 · 宿主：github

用 Julia 模拟 VLF 在地球-电离层波导中的模态传播，服务低电离层与远距 VLF 研究，和 GNSS L 波段 TEC 工具链互补。局限：领域偏 VLF；对 GNSS 测地用户直接用途有限。

#### [sami2py](https://github.com/sami2py/sami2py)  
*🏷️ 高校实验室*

语言：Python/Fortran · 许可：BSD-3-Clause · 星标约：21 · 宿主：github

sami2py 把海军实验室 SAMI2 二维电离层模式包成 Python：可设置经度、年积日等驱动并运行 Fortran 内核，再把输出归档、加载与绘图。相对完整 IRI/NeQuick 气候模型，它更强调沿磁力线的等离子体动力学。输入含经度、日期、可选中性大气缩放与自定义 ExB 漂移等；输出为模式场。局限：依赖 Fortran 编译器；二维近似不覆盖全球三维结构；仓库近年更新偏少。

#### [sami3_gitm](https://github.com/jdhuba/sami3_gitm)  
*🏷️ 官方*

语言：Fortran · 许可：unknown · 星标约：7 · 宿主：github

作者仓库提供的 SAMI3 与 GITM 数据接口的基础（vanilla）版本，使用 EUVAC 等驱动，适合追溯耦合实现。局限：偏早期快照；缺少现代文档与测试；生产研究更建议结合 SAMI3-4.00 / GITM 新仓与论文配置。

#### [transcar](https://github.com/space-physics/transcar)  
*🏷️ 高校实验室*

语言：Fortran · 许可：NOASSERTION · 星标约：7 · 宿主：github

Blelly/Lilensten/Zettergren 一维沉降电离层模式，用于粒子沉降加热与密度响应研究。输入为沉降能谱等；输出为一维剖面时序。局限：非全球 GIM；与 GNSS 射线积分需自行耦合。

#### [mat_gemini](https://github.com/gemini3d/mat_gemini)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：6 · 宿主：github

为 GEMINI 离子层模式提供 MATLAB 侧核心脚本（配置、读写、后处理接口）。输入为 GEMINI 工程与网格；输出为可分析的场量。局限：需配合 GEMINI 主程序；与目录中 gemini3d 本体分工不同。

#### [SAMI2](https://github.com/NRL-Plasma-Physics-Division/SAMI2)  
*🏷️ 官方*

语言：Fortran · 许可：CC0-1.0 · 星标约：6 · 宿主：github

Naval Research Laboratory 的 SAMI2（Sami2 is Another Model of the Ionosphere）Fortran 源码，沿磁力线描述低纬—中纬等离子体。输入为经度、季节、太阳活动等；输出为二维密度等场。局限：二维近似；编译与驱动准备有门槛（可与 sami2py 对照）。

#### [IPE](https://github.com/NOAA-SWPC/IPE)  
*🏷️ 官方*

语言：Fortran · 许可：GPL-3.0 · 星标约：5 · 宿主：github

IPE（Ionosphere Plasmasphere Electrodynamics）由 NOAA 空间天气预测中心开源，描述电离层与等离子体层耦合及电动力学，面向业务与科研的全球电子密度等产品。适合作为物理/半业务背景场，与实测 TEC、闪烁指数对比。局限：配置与耦合运行门槛不低；星数不多、社区文档相对 GITM/TIE-GCM 更散；不宜直接替代经验修正模型做接收机实时改正。

#### [AURORA](https://github.com/egavazzi/AURORA)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：GPL-3.0 · 星标约：3 · 宿主：github

描述电离层中电子输运的时间相关模型（MATLAB），用于沉降/能量沉积相关过程理解。输入为驱动与边界条件；输出为电子输运相关场。局限：非 GNSS 测地产品线；配置与物理背景要求较高。

#### [ntcmg](https://github.com/lguldur/ntcmg)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：3 · 宿主：github

按 Galileo OS《NTCM-G Ionospheric Model Description》实现的 NTCM-G 经验改正，与 NeQuick-G 同属单频用户电离层延迟估算路线，但是不同算法族。输入为广播/模型所需系数与链路几何；输出为电离层延迟估计。局限：仓库体量小、星数低；需对照官方 PDF 验证实现完整度；不替代双频无消电离层或 GIM。

#### [FIRI-2018](https://github.com/AlexT1983/FIRI-2018)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：BSD-3-Clause · 星标约：2 · 宿主：github

FIRI（Faraday-International Reference Ionosphere）侧重低电离层电子密度，本仓库给出 2018 版 MATLAB 实现，可与 IRI 高层剖面拼接思路对照。输入为位置/时间等模型参数；输出低电离层 Ne。局限：主要服务低频/VLF/吸收研究，对 GNSS L 波段 TEC 贡献相对小；MATLAB 生态。

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

#### [HAO-TGCM-portal](https://www.hao.ucar.edu/modeling/tgcm)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

HAO 上的 TIE-GCM/TIME-GCM 家族说明、用户指南与发布历史入口，补充 GitHub 源码仓的文档侧。局限：部分老版本下载流程可能仍要邮件注册；以 GitHub NCAR/tiegcm 为当前源码主渠道更合适。

#### [Klobuchar-study-code](https://github.com/KaijingZheng/Klobuchar-ionosphere-model-in-global-navigation-satellite-systems)  
*🏷️ 个人社区*

语言：MATLAB · 许可：unknown · 星标约：0 · 宿主：github

教学/研究向的 Klobuchar 实现与精度探讨，便于理解 GPS 广播八参数改正。局限：非新品算法库；星数为 0；改进结论需独立验证。

#### [NeQuick2-MLF2](https://github.com/SkydelSolutions/nequick2-mlf2)  
*🏷️ 个人社区*

语言：C · 许可：unknown · 星标约：0 · 宿主：github

该仓库提供 NeQuick2-MLF2 电离层模式实现，说明基于 Galileo NeQuick-G 算法并由 Gustave Eiffel University / Safran Trusted 4D 修改。对需要在仿真器或接收机侧嵌入 NeQuick 族改正的开发者有参考价值。局限：星数为 0；与官方 NeQuick2/NeQuick-G 发布渠道并行，引用与验证需自行对照 ICTP/ESA/JRC 参考实现；文档相对简略。

#### [RIM](https://github.com/SWMFsoftware/RIM)  
*🏷️ 官方*

语言：Fortran · 许可：unknown · 星标约：0 · 宿主：github

Space Weather Modeling Framework 组件之一，描述高纬电离层电动力学等，常与全球磁层模式耦合。局限：通常作为 SWMF 整体使用；单独跑与输入耦合复杂；许可字段不清晰。

#### [SAMI3-3.22-CCMC-mirror](https://github.com/sylee918/SAMI3)  
*🏷️ 个人社区*

语言：Fortran · 许可：unknown · 星标约：0 · 宿主：github

从 CCMC/Zenodo 体系搬运的 SAMI3-3.22 Fortran 源码镜像，方便 git clone。正式引用仍建议指向 CCMC 模型页或 Zenodo DOI。局限：非官方持续维护仓；体积大；配置与运行说明需回到 CCMC 文档。

## TEC估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | gnss-tec：RINEX 斜路径 TEC 重建 | Python | 54 | 🏷️ 高校实验室 核心 |
| [PyGPS](https://github.com/gregstarr/PyGPS) | 读 RINEX、算 TEC/卫星位置与偏差的工具箱 | Python | 47 | 🏷️ 个人社区 |
| [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB) | MATLAB 双频 RINEX 2.11 TEC 计算 | MATLAB | 33 | 🏷️ 高校实验室 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python+Rust） | Python | 29 | 🏷️ 个人社区 🔀 ★ 核心 |
| [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | 由 GPS 数据估计电离层 TEC 与旋转量 RM | Python | 26 | 🏷️ 个人社区 |
| [tec-suite](https://github.com/gnss-lab/tec-suite) | SIMuRG 团队 TEC 重建套件 | Python | 23 | 🏷️ 高校实验室 |
| [pygnss-tec](https://github.com/eureka-0/pygnss-tec) | RINEX 读取与 TEC 计算（Rust 加速） | Python | 16 | 🏷️ 个人社区 |
| [VARION](https://github.com/giorgiosavastano/VARION) | Sapienza 变分法实时电离层：由 RINEX 估计 sTEC 变化（海啸扰动等） | Python | 15 | 🏷️ 高校实验室 |
| [gsit](https://github.com/aldebaran1/gsit) | GSIT：TEC/ROTI/IPP 与光学磁力计 Python 工具 | Python | 10 | 🏷️ 个人社区 |
| [tidd](https://github.com/vc1492a/tidd) | 用在轨 GPS sTEC 变化率异常检测海啸信号 | Jupyter Notebook | 10 | 🏷️ 高校实验室 |
| [TEC_calculation_RINEX3](https://github.com/cssrg-kmitl/TEC_calculation_RINEX3) | MATLAB 从 RINEX 3.04 双频观测计算 TEC/ROTI | MATLAB | 6 | 🏷️ 高校实验室 |
| [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation) | 单/双频方法估计电离层延迟梯度 | MATLAB | 6 | 🏷️ 高校实验室 |
| [TEC-MoLLM](https://github.com/PANXIONG-CN/TEC-MoLLM) | GNN+时序 CNN+LLM（LoRA）的全球 TEC 预报研究代码 | Python | 4 | 🏷️ 高校实验室 |
| [tec-example](https://github.com/embrace-inpe/tec-example) | INPE Embrace 相关的 TEC 处理示例 | Python | 3 | 🏷️ 官方 |
| [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research) | 处理 CDAAC COSMIC 掩星 NetCDF 做 TEC 研究 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [gps-tec-cnn-lstm-attention](https://github.com/hyy-why/gps-tec-cnn-lstm-attention) | 论文配套：注意力机制 TEC 时序预测示例 | Python | 1 | 🏷️ 个人社区 |
| [ESA-UGI](https://essr.esa.int/project/unified-gnss-ionosphere) | ESA UGI：从多系统 GNSS 观测估计 vTEC/IFB/模糊度的开源包（ESSR） | unknown | — | 🏷️ 官方 |
| [GNSS-Workshop-TEC](https://github.com/breid-phys/GNSS-Workshop) | 研讨班材料：从 GNSS 数据探索到 TEC 测量 | Python | 0 | 🏷️ 高校实验室 |
| [Ion-Phys-Toolkit](https://github.com/PANXIONG-CN/Ion-Phys-Toolkit) | 面向 TEC 预报的物理信息学习最小可复现工具包 | Python | 0 | 🏷️ 高校实验室 |
| [IONOLAB-TEC-Software](https://www.ionolab.org/index.php?language=en&page=ionolabtec) | IONOLAB-TEC/STEC：土耳其 IONOLAB 实验室 GNSS TEC/STEC 估计软件（需登录） | unknown | — | 🏷️ 高校实验室 |
| [KOH2-ionosphere](https://github.com/asparuhkamburov/KOH2-ionosphere) | 南极 Livingston 岛 KOH2 站 GNSS TEC 处理与太阳周 25 分析 | Python | 0 | 🏷️ 高校实验室 |
| [Okoh-MATLAB-TEC-from-RINEX](https://doi.org/10.5281/zenodo.7711905) | Daniel Okoh：从 GNSS RINEX 提取 TEC 的 MATLAB 脚本集（Zenodo） | MATLAB | — | 🏷️ 高校实验室 |
| [PMGC-SimVP](https://github.com/OnlyYouNotInCity/PMGC-SimVP) | 参数化多尺度门控卷积 + SimVP 的全球 TEC 时空预报 | Python | 0 | 🏷️ 高校实验室 |
| [quakeion](https://github.com/Gm015555/quakeion) | 震例目录 + CODE GIM TEC/ROT/ROTI 分析（零 API Key） | Python | 0 | 🏷️ 个人社区 |
| [Seemala-GPS-TEC](https://seemala.blogspot.com/2026/08/gps-tec-analysis-program-version-37.html) | Gopi Seemala GPS-TEC：从 RINEX 估计 GPS TEC 的便携 Windows 程序（当前 v3.7） | Windows/Exe | — | 🏷️ 高校实验室 |
| [TEC-forecast-F107](https://github.com/hekaixuan-atm/TEC-forecast) | 空间非均匀 F10.7 强迫的全球 TEC 预报代码 | Python | 0 | 🏷️ 高校实验室 |
| [vtec](https://github.com/mfkiwl/vtec) | 垂直 TEC（VTEC）计算相关工具 | — | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [gnss-tec](https://github.com/gnss-lab/gnss-tec)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：54 · 宿主：github

SIMuRG/gnss-lab 系经典 STEC 重建库，输入 RINEX 相位与伪距，输出斜路径 TEC，MIT 许可友好。适合论文复现与批处理建站网 TEC。GIM 成图、闪烁指数需另接 mosgim/OASIS 等；DCB 处理策略要按数据源核对。

#### [PyGPS](https://github.com/gregstarr/PyGPS)  
*🏷️ 个人社区*

语言：Python · 许可：AGPL-3.0 · 星标约：47 · 宿主：github

把读 RINEX、存 HDF5、算 TEC、卫星位置与接收机/卫星偏差串在一起，偏研究原型。适合快速探索。AGPL 较严；长期维护与测试覆盖不如专门 TEC 库，关键步骤建议交叉验证。

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

语言：Python · 许可：— · 星标约：26 · 宿主：github

面向射电天文/地空链路，从 GPS 接收机数据估 TEC 与法拉第旋转相关量。适合需要 TEC+RM 联合的场景。通用 GNSS 多星座精密 TEC 流水线不是其主场；协议与输入格式需按仓库说明准备。

#### [tec-suite](https://github.com/gnss-lab/tec-suite)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：23 · 宿主：github

比单库 gnss-tec 更偏「套件」形态，把重建流程串起来便于站点网作业。适合已在用 SIMuRG 工具链的人。GPL 约束与文档深度因版本而异；轻量嵌入可优先 gnss-tec。

#### [pygnss-tec](https://github.com/eureka-0/pygnss-tec)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

Python 包读 RINEX 并算 TEC，关键路径用 Rust 加速，和 PyTECGg 同属「Py+加速核」路线。适合中等规模批处理。社区体量小于 gnss-tec；算法假设（映射、DCB）使用前要读文档核对。

#### [VARION](https://github.com/giorgiosavastano/VARION)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：15 · 宿主：github

罗马一大（Sapienza）开源的变分法电离层观测工具，读取 RINEX 观测/广播星历估计 slant TEC 变化，用于站级近实时扰动监测（如海啸电离层扰动）。Python+NumPy/Pandas，GPL-3。适合单站高频 TEC 扰动教学与案例复现；依赖较旧的 Python 2.7+ 生态，需自行准备导航文件与站坐标。

#### [gsit](https://github.com/aldebaran1/gsit)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：10 · 宿主：github

面向电离层社区的 Python 框架（MIT）：双频伪距/相位 TEC、相位改正 TEC、ROTI、薄壳 VTEC、IPP，以及卫星 AER/WGS84 位置；并含全天空成像与 IPP 叠置、三轴磁力计 HDZ↔XYZ、OMNIWeb IMF 读取与轨迹绘图。适合教学与多传感器对照原型。仓库近年少更新（约 2017 推送），依赖与 RINEX 版本覆盖需自行验证；不是生产级 GIM/PPP 引擎。

#### [tidd](https://github.com/vc1492a/tidd)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：NOASSERTION · 星标约：10 · 宿主：github

演示从低轨 GPS 的 sTEC 时间变化中做异常检测以指示海啸扰动的方法与笔记本。输入为在轨 GPS TEC 时序；输出为异常检测结果。局限：研究案例向；虚警/漏检与空间天气干扰需注意。

#### [TEC_calculation_RINEX3](https://github.com/cssrg-kmitl/TEC_calculation_RINEX3)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

泰国 KMITL CSSRG 实验室程序，由双频 RINEX 3 计算 STEC/VTEC、DCB 与 ROTI，主入口 ProcessTECCalculation.m。输入为观测/星历等；输出为一日 TEC 结构与 ROTI。局限：依赖 Linux/Cygwin 命令环境；主要面向 GPS 双频教学实验。

#### [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

从 RINEX 估计电离层延迟梯度，服务于 GBAS/局域增强等对空间梯度敏感的应用。适合机场周遭或短基线梯度研究。全球 GIM 不是目标；与 ROTI/闪烁监测可互补。

#### [TEC-MoLLM](https://github.com/PANXIONG-CN/TEC-MoLLM)  
*🏷️ 高校实验室*

语言：Python · 许可：unknown · 星标约：4 · 宿主：github

多模态深度学习 TEC 预报原型，组合图网络、时序卷积与大模型 LoRA 微调。输入为历史 TEC/空间天气特征；输出预报场。局限：算力与复现成本高；与经典物理/经验模式比可解释性弱；许可未标明。

#### [tec-example](https://github.com/embrace-inpe/tec-example)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：3 · 宿主：github

INPE Embrace 相关的 TEC 处理示例脚本，降低接触其数据产品与基本流程的门槛。适合南美区域 TEC 或空间天气入门。仓库体量小，不是完整产线；深度批处理请接 gnss-tec、PyTECGg 或 Embrace 官方推荐流程，并核对映射函数与 DCB 假设。

#### [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：2 · 宿主：github

Jupyter 流程读取 CDAAC/COSMIC 掩星 NetCDF，面向 TEC 与掩星电离层剖面研究，便于复现空基电子含量分析。做 GNSS-RO 与空间天气的人可作起点。不是地基双频 TEC 或 GIM 软件；产品字段、版本与质量控制需对照 CDAAC 官方文档，结果宜与地基网交叉验证。不同任务期产品版本不要混用后直接拼时间序列。

#### [gps-tec-cnn-lstm-attention](https://github.com/hyy-why/gps-tec-cnn-lstm-attention)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：1 · 宿主：github

论文配套的 CNN-BiLSTM 注意力 TEC 预测代码，目标是复现实验而非业务运行。星标与文档有限，数据准备脚本完整度需自查。业务空间天气预报请用业务模式或同化产品。

#### [ESA-UGI](https://essr.esa.int/project/unified-gnss-ionosphere)  
*🏷️ 官方*

语言：unknown · 许可：ESA Community License v2.4 Weak Copyleft (Type 2) · 星标约：— · 宿主：official_site

欧洲航天局在 ESSR 发布的 Unified GNSS Ionosphere（UGI）程序包，面向 GPS/Galileo/BDS 双频观测估计垂直 TEC、频间偏差与载波模糊度，支持体素/多层/球谐等 2D–3D 电离层表征。适合作为 GNSS 电离层估计研究的可复现起点。源码托管在 ESSR 的 git，下载需注册 ESA Community 账号并接受 ESA Community License v2.4 Weak Copyleft；输入需预先标记/改正周跳。页面 HTTP 200 可访问。

#### [GNSS-Workshop-TEC](https://github.com/breid-phys/GNSS-Workshop)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：0 · 宿主：github

教学/研讨班 Jupyter 材料，演示 GNSS 数据探索与 TEC 测量流程，适合入门。局限：非生产库；依赖研讨班数据布局。

#### [Ion-Phys-Toolkit](https://github.com/PANXIONG-CN/Ion-Phys-Toolkit)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

物理信息（PINN/类 PINN）TEC 预报的精简发布，便于复现论文设定。局限：标注为 minimal release；功能面窄；需自备训练数据。

#### [IONOLAB-TEC-Software](https://www.ionolab.org/index.php?language=en&page=ionolabtec)  
*🏷️ 高校实验室*

语言：unknown · 许可：academic research (non-commercial; cite required) · 星标约：— · 宿主：official_site

Hacettepe/IONOLAB 团队提供的 IONOLAB-TEC/STEC 本地下载软件入口，与站点上的 IONOLAB-TEC Online、IRI-Plas 在线服务配套，面向学术 GNSS TEC/STEC 估计。下载页明确要求先登录；新用户需在 ionolab.org 注册。面向科研非商业用途，发表需引用服务页所列论文。软件页 HTTP 200；IRI-Plas 子页偶发 500，以 TEC 软件页为准。

#### [KOH2-ionosphere](https://github.com/asparuhkamburov/KOH2-ionosphere)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：0 · 宿主：github

单站（KOH2）TEC 处理、检验与太阳周 25 分析脚本，可作为极区测站流程参考。局限：强绑定单站个例；泛化到其他站需改路径与偏差策略。

#### [Okoh-MATLAB-TEC-from-RINEX](https://doi.org/10.5281/zenodo.7711905)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

NASRDA 研究人员 Daniel Okoh 在 Zenodo 发布的 MATLAB 代码包（concept DOI 10.5281/zenodo.7711905），面向 RINEX 观测做周跳检测/改正、相位平滑与 TEC 提取，示例来自 U-Blox 接收机。许可 CC-BY-4.0，文件为可直接下载的 .m 脚本，无 GitHub 依赖。适合教学与单站 TEC 试验；生产级多系统流水线可对照 Seemala/IONOLAB 等工具。

#### [PMGC-SimVP](https://github.com/OnlyYouNotInCity/PMGC-SimVP)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：0 · 宿主：github

深度学习全球 TEC 预报实现（PMGC-SimVP），Apache-2.0。局限：研究代码；训练数据与超参需自行对齐论文；推理前要有历史 TEC 栅格。

#### [quakeion](https://github.com/Gm015555/quakeion)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

把地震目录与电离层 TEC/ROT/ROTI 分析串起来，并可用 Kp/Dst 过滤地磁暴，强调无需额外 API Key。适合震电离层耦合统计入门。局限：依赖 GIM/IONEX 而非测站原始 STEC；因果解释需谨慎；星数为 0。

#### [Seemala-GPS-TEC](https://seemala.blogspot.com/2026/08/gps-tec-analysis-program-version-37.html)  
*🏷️ 高校实验室*

语言：Windows/Exe · 许可：freeware for research (cite Seemala 2023) · 星标约：— · 宿主：other

波士顿学院 ISR / 空间物理学者 Gopi Seemala 维护的经典 GPS TEC 分析程序（博客当前为 v3.7）。读取 GPS RINEX 2/3 观测与导航文件并自动拉取 DCB，输出 CMN 文本与日变化图；Windows 便携 ZIP，无需安装。低纬电离层教学与区域 TEC 研究引用极广；目前文档称暂仅 GPS。请按 Seemala 2023 章节引用，注意 VC++ 运行库依赖。非开源源码发布。

#### [TEC-forecast-F107](https://github.com/hekaixuan-atm/TEC-forecast)  
*🏷️ 高校实验室*

语言：Python · 许可：unknown · 星标约：0 · 宿主：github

论文配套实验：在深度学习 TEC 预报中引入空间非均匀 F10.7 强迫，探索太阳辐射空间差异的影响。适合复现与对比基线。仓库体量小、数据划分依赖作者设定，非业务级物理/同化模式。

#### [vtec](https://github.com/mfkiwl/vtec)  
*🏷️ 个人社区 ★*

语言：— · 许可：MIT · 星标约：— · 宿主：github

围绕 VTEC 换算与相关计算的小工具，适合把 STEC 投影到垂直方向做图或预报输入。功能边界较窄，完整双频重建与偏差估计需配合专业 TEC 库。

## 工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pysat](https://github.com/pysat/pysat) | pysat：日地空间科学数据分析框架 | Python | 173 | 🏷️ 高校实验室 |
| [Kamodo](https://github.com/nasa/Kamodo) | NASA CCMC Kamodo：把 GITM/TIEGCM/IRI/WACCM-X 等输出函数化分析 | Python | 58 | 🏷️ 官方 |
| [geospacelab](https://github.com/JouleCai/geospacelab) | 日地空间数据收集/管理/可视化库，含 TEC、Swarm、EISCAT 等 | Python | 48 | 🏷️ 高校实验室 |
| [apexpy](https://github.com/aburrell/apexpy) | Apex/准偶极地磁坐标 Python 封装（电离层坐标变换常用） | Python | 40 | 🏷️ 高校实验室 |
| [jvierine-ionosonde](https://github.com/jvierine/ionosonde) | 开源测高仪/电离图相关 Python 软件（社区星数较高） | Python | 23 | 🏷️ 高校实验室 |
| [Ionort-raytrace](https://github.com/blair3sat/ionosphere-rt) | 电离层三维射线追踪程序 Ionort（Azzarone 等）开源拷贝 | Fortran | 17 | 🏷️ 高校实验室 |
| [pysatSpaceWeather](https://github.com/pysat/pysatSpaceWeather) | pysat 空间天气指数与数据集支持库 | Python | 14 | 🏷️ 高校实验室 |
| [ionosonde_volgatech](https://github.com/Vladimi-lan/ionosonde_volgatech) | 伏尔加技术大学相关测高仪数据处理代码 | Python | 13 | 🏷️ 高校实验室 |
| [Alouette_ISIS_extract](https://github.com/asc-csa/Alouette_ISIS_extract) | 加拿大航天局：从 Alouette/ISIS 扫描电离图提取数据与元数据 | Python | 11 | 🏷️ 官方 |
| [ionosphereAI](https://github.com/space-physics/ionosphereAI) | 从光学/被动雷达/非相干散射等噪声数据中检测电离层特征 | Python | 11 | 🏷️ 高校实验室 |
| [ocbpy](https://github.com/aburrell/ocbpy) | ocbpy：极盖边界自适应磁坐标转换库 | Python | 11 | 🏷️ 高校实验室 |
| [POLAN](https://github.com/space-physics/POLAN) | Titheridge POLAN：测高仪虚高到真高反演（Fortran/现代封装） | Fortran | 11 | 🏷️ 高校实验室 |
| [COSMIC-IONPRF-Ne-TEC](https://github.com/HassanNooreldeen/COSMIC-IONPRF-NC-CDAAC-UCAR-Ne-TEC) | COSMIC CDAAC 掩星 Ne/TEC 下载与多年分析 MATLAB 脚本 | MATLAB | 9 | 🏷️ 个人社区 |
| [pysatModels](https://github.com/pysat/pysatModels) | pysat 生态中的模式分析与模式-数据对比接口 | Python | 9 | 🏷️ 高校实验室 |
| [Septentrio-PyDataLink](https://github.com/septentrio-gnss/Septentrio-PyDataLink) | Septentrio 数据流可视化与互联开源工具 | Python | 8 | 🏷️ 官方 |
| [radionopy](https://github.com/UPennEoR/radionopy) | 大尺度电离层行为计算的 Python/C 工具 | C | 7 | 🏷️ 高校实验室 |
| [Raytrace-Model](https://github.com/kyruzic/Raytrace-Model) | 电离层中电波三维传播的 MATLAB 射线追踪 | MATLAB | 7 | 🏷️ 个人社区 |
| [gcmprocpy](https://github.com/NCAR/gcmprocpy) | TIE-GCM / WACCM-X 输出后处理与分析的 Python 工具 | Python | 6 | 🏷️ 官方 |
| [SAMI3-GITM-python](https://github.com/abukowski21/SAMI3-GITM-python) | SAMI3 与 GITM 耦合输出的 Python/Jupyter 分析示例 | Python | 6 | 🏷️ 高校实验室 |
| [Kamodo-core](https://github.com/nasa/Kamodo-core) | Kamodo 核心库：科学数据函数化 API（与 CCMC readers 配套） | Python | 5 | 🏷️ 官方 |
| [pynasonde](https://github.com/shibaji7/pynasonde) | 精密电离层无线电探测的开源 Python 应用 | Python | 5 | 🏷️ 高校实验室 |
| [mitiono](https://github.com/sabrinastronomy/mitiono) | 从 GPS 接收机数据提取电离层与波束图（miti-iono） | Jupyter Notebook | 4 | 🏷️ 高校实验室 |
| [MyIonosphere_Library](https://github.com/mguerra96/MyIonosphere_Library) | 相位观测 GFLC 与穿刺点 IPP 的 MATLAB 函数库 | MATLAB | 4 | 🏷️ 个人社区 |
| [SubionosphericVLFInversionAlgorithms.jl](https://github.com/fgasdia/SubionosphericVLFInversionAlgorithms.jl) | 用 VLF 信号反演低电离层的 Julia 算法集 | Julia | 4 | 🏷️ 高校实验室 |
| [pytiegcm](https://github.com/asher-pembroke/pytiegcm) | TIE-GCM 输出的轻量 Python 读取器 | Python | 3 | 🏷️ 个人社区 |
| [IonOccAnalysis](https://github.com/wonder2019WHU/IonOccAnalysis) | 电离层掩星（Occultation）数据分析工具（武大相关） | C++ | 2 | 🏷️ 高校实验室 |
| [Ionosonde-Data-Downloader](https://github.com/bzossi/Ionosonde-Data-Downloader) | 自动拉取公共测高仪库数据的轻量脚本 | Python | 2 | 🏷️ 个人社区 |
| [SbfMixer](https://github.com/septentrio-gnss/SbfMixer) | 在 Node-RED 中直接使用 Septentrio 接收机 | JavaScript | 2 | 🏷️ 官方 |
| [HamSCI-ionosonde](https://github.com/HamSCI/hamsci_ionosonde) | HamSCI 低成本啁啾测高仪的处理与验证软件 | Python | 1 | 🏷️ 高校实验室 |

### 详细说明

#### [pysat](https://github.com/pysat/pysat)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：173 · 宿主：github

pysat 提供跨平台一致的数据分析工作流，生态含空间天气指数、模式接口等，常与电离层卫星/地基数据一起用。局限：本身不是 IRI/TEC 专用包；学习曲线在“生态”而非单函数。

#### [Kamodo](https://github.com/nasa/Kamodo)  
*🏷️ 官方*

语言：Python · 许可：NASA-Open · 星标约：58 · 宿主：github

Kamodo（CCMC 读者套件）把多种日地空间模式输出“函数化”，统一插值、单位换算、可视化与卫星飞越（flythrough）。对电离层目录特别有价值：支持 GITM、TIEGCM、IRI、WACCM-X、CTIPe、SWMF-IE 等，便于把物理模式电子密度接到观测对比。输入是各模式输出目录；输出是可调用的 Kamodo 对象与图。局限：依赖与内存要求不低；不同模式 reader 成熟度不一；不是从 GNSS 观测解算 TEC 的软件。

#### [geospacelab](https://github.com/JouleCai/geospacelab)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：48 · 宿主：github

GeospaceLAB 用 Python 统一拉取与管理 OMNI、地磁指数、EISCAT、DMSP、Swarm、TEC、AMPERE 等，并做可视化，适合快速搭电离层观测对比分析环境。输入多为各数据中心接口或本地缓存；输出为结构化数据集与图。局限：依赖外部数据源可用性与注册策略；不是 TEC 解算引擎本身；包体与依赖较重。

#### [apexpy](https://github.com/aburrell/apexpy)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：40 · 宿主：github

电离层研究里把地理坐标转到 Apex/准偶极坐标的常用库，PyIRI 等也依赖同类坐标。输入纬经高与时间；输出磁纬磁地方时等。局限：不是电子密度模型；需注意 IGRF 年代与外推。

#### [jvierine-ionosonde](https://github.com/jvierine/ionosonde)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：23 · 宿主：github

面向测高仪数据处理与实验的 Python 项目，可用于电离图获取/分析相关工作流。与 GNSS TEC 互补，提供底部电离层约束。局限：README 信息偏少，需读代码确认具体仪器格式；不替代 GIRO/SAO 官方工具链。

#### [Ionort-raytrace](https://github.com/blair3sat/ionosphere-rt)  
*🏷️ 高校实验室*

语言：Fortran · 许可：unknown · 星标约：17 · 宿主：github

基于 Ionort 射线追踪思想的 Fortran 实现，用于给定电子密度背景下追踪无线电射线路径，可服务 HF/GNSS 传播与层析正演。局限：仓库较旧；电子密度场需外部提供（IRI/模式）；与商业/成熟射线库相比文档与测试不足。

#### [pysatSpaceWeather](https://github.com/pysat/pysatSpaceWeather)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：14 · 宿主：github

为 pysat 生态提供空间天气指数与相关数据接口，便于把 F10.7、地磁指数等驱动接到电离层分析。输入为数据源配置；输出为统一的 pysat Instrument 对象。局限：本身不算 TEC 解算器；需与 pysat 主库配合。

#### [ionosonde_volgatech](https://github.com/Vladimi-lan/ionosonde_volgatech)  
*🏷️ 高校实验室*

语言：Python · 许可：unknown · 星标约：13 · 宿主：github

与具体测高仪系统相关的 Python 处理代码，体量不小，可作为非 GIRO 数据源处理参考。局限：缺少清晰英文 README；通用性与许可需使用者自行确认（license 字段为空）。

#### [Alouette_ISIS_extract](https://github.com/asc-csa/Alouette_ISIS_extract)  
*🏷️ 官方*

语言：Python · 许可：CSA · 星标约：11 · 宿主：github

CSA 开源项目，从 Alouette 与 ISIS 卫星历史扫描电离图图像中提取数据与元数据，服务历史底部电离层档案数字化。局限：面向图像档案而非现代 GNSS；处理流水线偏研究复现。

#### [ionosphereAI](https://github.com/space-physics/ionosphereAI)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：11 · 宿主：github

面向多种电离层遥感噪声数据的特征检测工具，偏机器学习/信号处理，不是 GNSS TEC 解算。局限：与 GNSS 流水线耦合需自行对接；任务定义随数据源变化。

#### [ocbpy](https://github.com/aburrell/ocbpy)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：11 · 宿主：github

与 apexpy 同作者体系的 ocbpy，把观测转换到基于极盖边界（OCB）的自适应磁坐标，便于高纬电离层与磁层统计研究。许可 BSD-3-Clause。主要服务空间物理坐标变换，不直接读取 RINEX 或做 TEC 反演；常与极光电集流等数据集联用。

#### [POLAN](https://github.com/space-physics/POLAN)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：11 · 宿主：github

经典 POLAN 算法用于从测高仪/电离图虚高估计真实高度剖面，space-physics 仓库提供可编译的现代维护。对把测高仪 foF2/hmF2 与 GNSS TEC 联合分析很有用。局限：需要质量较好的描迹/虚高输入；不直接处理 GNSS；使用者需了解测高仪反演假设。

#### [COSMIC-IONPRF-Ne-TEC](https://github.com/HassanNooreldeen/COSMIC-IONPRF-NC-CDAAC-UCAR-Ne-TEC)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：9 · 宿主：github

下载并筛选 COSMIC 掩星电子密度廓线，做多年统计分析与教学绘图。输入为 CDAAC 访问与时间范围；输出为 Ne/TEC 相关统计。局限：依赖数据中心政策；不是地基双频 TEC。

#### [pysatModels](https://github.com/pysat/pysatModels)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：9 · 宿主：github

在 pysat 框架下对接模式输出并做模式-观测对比，便于把经验/物理电离层模式纳入同一分析脚本。局限：需先熟悉 pysat；具体模式覆盖以文档为准。

#### [Septentrio-PyDataLink](https://github.com/septentrio-gnss/Septentrio-PyDataLink)  
*🏷️ 官方*

语言：Python · 许可：BSD-3-Clause · 星标约：8 · 宿主：github

pyDataLink 用于可视化与连接接收机数据流，便于实验教学中快速查看观测与配置链路。输入为接收机/记录数据流；输出为可视化与转发接口。局限：偏工程联调，不直接给出 TEC/闪烁科学指标。

#### [radionopy](https://github.com/UPennEoR/radionopy)  
*🏷️ 高校实验室*

语言：C · 许可：MIT · 星标约：7 · 宿主：github

面向射电天文/大尺度电离层效应的数值工具，可计算大范围电离层相关量。输入为模式/几何配置；输出为电离层影响相关场。局限：场景偏射电传播，不是标准 IONEX 生产。

#### [Raytrace-Model](https://github.com/kyruzic/Raytrace-Model)  
*🏷️ 个人社区*

语言：MATLAB · 许可：GPL-3.0 · 星标约：7 · 宿主：github

在给定电子密度模型下做三维射线追踪，服务传播教学与研究型实验。GPL 许可、偏原型实现。输入电离层模型与数值步长需用户自行校验；业务链路预算请对照 ITU/专业传播软件。

#### [gcmprocpy](https://github.com/NCAR/gcmprocpy)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：6 · 宿主：github

gcmprocpy 面向 NCAR TIE-GCM 与 WACCM-X 模式输出，做后处理、诊断与可视化，降低直接啃 netCDF 压力层网格的成本。输入为模式标准输出；输出为分析用场量/图。局限：本身不运行模式；强依赖对应模式版本的变量命名与网格约定；WACCM-X 完整源码通常走 CESM 体系，本仓库只覆盖后处理侧。

#### [SAMI3-GITM-python](https://github.com/abukowski21/SAMI3-GITM-python)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：6 · 宿主：github

围绕 SAMI3–GITM 耦合或对照实验的 Python/Notebook 工具集，便于读场、画图与做简单诊断，而不是完整模式本体。适合已有模式输出、需要快速分析的用户。局限：文档偏少；依赖具体输出格式；不能替代官方模式仓库。

#### [Kamodo-core](https://github.com/nasa/Kamodo-core)  
*🏷️ 官方*

语言：Python · 许可：NASA-Open · 星标约：5 · 宿主：github

Kamodo-core 提供函数化科学数据访问的核心 API，CCMC 的 Kamodo readers 建立其上。单独使用可把任意网格场变成可组合函数；与 nasa/Kamodo 搭配更完整。局限：只有 core 时缺少各模式专用 reader；安装路径在历史上有 ensemblegov 与 nasa 组织迁移，注意文档版本。

#### [pynasonde](https://github.com/shibaji7/pynasonde)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：5 · 宿主：github

面向精密电离层无线电探测（sounding）的 Python 应用，服务实验测高/探测数据处理。局限：相对传统 Digisonde 软件生态仍小；硬件/数据格式适配需对照文档。

#### [mitiono](https://github.com/sabrinastronomy/mitiono)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：— · 星标约：4 · 宿主：github

配套射电/干涉测量电离层缓解研究，从 GPS 数据生成电离层与波束相关图（见 arXiv:2411.06144）。输入为 GPS 接收机数据；输出为电离层/波束产品。局限：面向特定科学场景；后续基带互相关仍在规划。

#### [MyIonosphere_Library](https://github.com/mguerra96/MyIonosphere_Library)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：4 · 宿主：github

计算相位几何自由组合（GFLC）与电离层穿刺点，适合教学推导 STEC 观测方程。输入为相位观测与站星几何；输出为 GFLC/IPP。局限：不是完整 TEC 定标与 DCB 解算套件。

#### [SubionosphericVLFInversionAlgorithms.jl](https://github.com/fgasdia/SubionosphericVLFInversionAlgorithms.jl)  
*🏷️ 高校实验室*

语言：Julia · 许可：MIT · 星标约：4 · 宿主：github

实现亚电离层 VLF 信号反演以估计低电离层参数，适合教学理解“电波—电离层”反问题。输入为 VLF 观测量与传播几何；输出为低电离层特征量估计。局限：与 GNSS TEC/GIM 流水线不同；对传播正演与初值敏感。

#### [pytiegcm](https://github.com/asher-pembroke/pytiegcm)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：3 · 宿主：github

小型 Python reader，方便把 TIE-GCM netCDF 读进分析脚本。适合不想上完整 Kamodo/gcmprocpy 时做快速检查。局限：功能远少于 Kamodo；维护不活跃（约 2022）；变量覆盖需自测。

#### [IonOccAnalysis](https://github.com/wonder2019WHU/IonOccAnalysis)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：2 · 宿主：github

C++ 工具面向 GNSS 电离层掩星数据处理与分析，适合理解 LEO—GNSS 链路反演电子密度。输入为掩星观测/相关产品；输出为分析与可视化结果。局限：文档与维护节奏需自行评估；与地基双频 TEC 流程不同。

#### [Ionosonde-Data-Downloader](https://github.com/bzossi/Ionosonde-Data-Downloader)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

按站点/时间从公共测高仪仓库批量下载，减少手工翻目录。适合底部电离层档案收集。上游目录或接口变更会导致脚本失效；不做描迹反演或质量控制，需另接 Autoscala/SAO 等工具。

#### [SbfMixer](https://github.com/septentrio-gnss/SbfMixer)  
*🏷️ 官方*

语言：JavaScript · 许可：BSD-3-Clause · 星标约：2 · 宿主：github

通过 Node-RED 流程编排访问 Septentrio，适合演示数据采集与简单自动化。输入为接收机连接与流程节点配置；输出为可拖拽的数据管道。局限：教学/原型友好，科研级批处理与质控能力有限。

#### [HamSCI-ionosonde](https://github.com/HamSCI/hamsci_ionosonde)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：1 · 宿主：github

配套 HamSCI 低成本 chirp 测高仪：SDR 发收、互相关测时延、估算虚高，并在日食等事件中与业务测高仪对比。输入为 SDR/GNU Radio 采集；输出时延与虚高序列。局限：依赖实验执照与硬件；频段 2–10 MHz，与 GNSS 频段不同。

## 测高仪自动缩放

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Autoscala-INGV](http://iononet.ingv.it/index.php/download/software) | INGV Autoscala 测高仪自动缩放及相关分析软件入口 | various | — | 🏷️ 官方 |

### 详细说明

#### [Autoscala-INGV](http://iononet.ingv.it/index.php/download/software)  
*🏷️ 官方*

语言：various · 许可：scientific distribution (INGV portal) · 星标约：— · 宿主：official_site

意大利国家地球物理与火山学研究所（INGV）测高仪团队的软件下载页，介绍 Autoscala 自动缩放（foF2、MUF 等）以及数据分析、电离层模型配套工具。适合欧洲/INGV 站网 ionogram 自动处理路线。页面偏门户说明，具体包获取方式以站点 Restricted area / 联系渠道为准，并非 GitHub 式即开即用源码仓。

## IONEX/TEC图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [INX_Editor](https://github.com/1acheng/INX_Editor) | 跨平台 IONEX 文件编辑工具 | — | 16 | 🏷️ 个人社区 ★ |
| [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX) | INPE TEC 图与 IONEX 生成工具 | Python | 15 | 🏷️ 个人社区 ★ |
| [ionex](https://github.com/gnss-lab/ionex) | Python 读取 IONEX 电离层图文件 | Python | 12 | 🏷️ 高校实验室 核心 |
| [ionex-rs](https://github.com/nav-solutions/ionex) | Rust 实现的 IONEX 解析与处理 | Rust | 7 | 🏷️ 个人社区 核心 |
| [IonMap](https://github.com/Jin-Whu/IonMap) | 由 IONEX 绘制电离层 TEC 地图 | Python | 4 | 🏷️ 高校实验室 |
| [rtcm2ionex](https://github.com/d-roma/rtcm2ionex) | 将 RTCM VTEC 消息转为 IONEX | Python | 3 | 🏷️ 个人社区 |
| [ionex_formatter](https://github.com/gnss-lab/ionex_formatter) | gnss-lab IONEX 写出/格式化模块（与 ionex 读取库配套） | Python | 2 | 🏷️ 高校实验室 |
| [Ionex_Parser](https://github.com/ajayraghASL/Ionex_Parser) | 读取 IONEX 并返回网格 TEC 的 Python 脚本 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [ionex_reader](https://github.com/bbrawar/ionex_reader) | IONEX→xarray 读取与可视化（支持 JPL/CODE/ESA 等产品） | Python | 2 | 🏷️ 个人社区 |
| [mgfernan-pygnss](https://github.com/mgfernan/pygnss) | Python GNSS 工具集：IONEX/GIM、Hatanaka、与 NeQuick 对比 CLI | Python | 2 | 🏷️ 个人社区 |
| [Beihang-Ionosphere-CN](http://ionosphere.cn/) | 北航 ionosphere.cn：全球 GNSS TEC 图与空间天气研究产品门户 | data-portal | — | 🏷️ 高校实验室 |
| [ESA-IONMON](https://swe.ssa.esa.int/ionmon) | ESA IONMON：电离层监测最新全球 TEC/RMS 等产品应用 | data-portal | — | 🏷️ 官方 |
| [ESA-TIO-NRT-TEC](https://swe.ssa.esa.int/tio_tcr) | ESA TIO 近实时 TEC 图服务（穿越电离层电波链路） | data-portal | — | 🏷️ 官方 |
| [GFZ-Global-Ionosphere-Maps](https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/global-gnss-ionosphere-maps) | GFZ IGS 电离层分析中心全球 GNSS TEC 图产品说明页（EPOS.P8） | data-portal | — | 🏷️ 官方 |
| [ionex-analyzer](https://github.com/matador96/ionex-analyzer) | Electron/React 的 IONEX 可视化毕业作品 | JavaScript | 0 | 🏷️ 个人社区 |
| [MathWorks-ionex_reader](https://www.mathworks.com/matlabcentral/fileexchange/172149-ionex_reader) | MATLAB File Exchange：IONEX 读取、制图与单点 TEC 时序 | MATLAB | 0 | 🏷️ 个人社区 |
| [ROB-European-TEC](https://gnss.be/SpaceWeather/) | 比利时皇家天文台（ROB）欧洲近实时多 GNSS VTEC 空间天气门户 | data-portal | — | 🏷️ 官方 |
| [ROB-IONEX-Products](https://gnss.be/SpaceWeather/Products/IONEX) | ROB 欧洲 VTEC 产品 IONEX 公开下载目录 | data-portal | — | 🏷️ 官方 |
| [UWM-CDRSK-IGS-Validation](https://cdrsk.uwm.edu.pl/centrum-walidacji-i-kombinacji-igs/) | UWM CDRSK：IGS 电离层验证与组合中心机构介绍（波兰语门户） | data-portal | — | 🏷️ 高校实验室 |
| [UWM-IGS-Iono-Combination](https://igsiono.uwm.edu.pl/) | 波兰 Warmia-Mazury 大学 IGS 电离层组合/验证中心站点（igsiono） | data-portal | — | 🏷️ 高校实验室 |

### 详细说明

#### [INX_Editor](https://github.com/1acheng/INX_Editor)  
*🏷️ 个人社区 ★*

语言：— · 许可：GPL-3.0 · 星标约：16 · 宿主：github

面向 IONEX 的桌面编辑与检查，改网格、头信息或局部 TEC 值时比手改文本省事。适合产品质检与教学演示。不是 TEC 估计算法库；重建 TEC 仍需 PyTECGg/gnss-tec 等。

#### [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX)  
*🏷️ 个人社区 ★*

语言：Python · 许可：— · 星标约：15 · 宿主：github

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
*🏷️ 高校实验室*

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
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

按文件头解析网格，把 TEC/RMS 装进 xarray，可选日夜界与地磁纬线叠加。适合快速抽检 IGS 各分析中心 IONEX、做差分或画图。功能偏读与展示，不负责建图或写回完整 IONEX；写格式可对照 gnss-lab/ionex、ionex_formatter 或 pygnss。

#### [mgfernan-pygnss](https://github.com/mgfernan/pygnss)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

作者亦维护 NeQuickJRC；本库提供 IONEX 加载、GIM handler、ionex_diff（可对 NeQuick）以及 RINEX/Hatanaka 辅助。适合把电离层图产品接到脚本化质检。与 semuconsulting/pygnss* 系列同名空间易混淆，克隆时认准 mgfernan/pygnss；功能广度不如大型测地套件。

#### [Beihang-Ionosphere-CN](http://ionosphere.cn/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

北京航空航天大学团队维护的电离层与空间天气站点，提供 Final/Rapid/Ultra 及更高时间分辨率全球 TEC 图展示，并参与 IAG 实时电离层监测等工作组方向。与 CAS BDsmart IONEX 数据树不同，本站偏研究展示与联系入口；批量业务下载优先确认站内 archive 链接或并行使用 data.bdsmart.cn。

#### [ESA-IONMON](https://swe.ssa.esa.int/ionmon)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

ESA 空间天气网络中的电离层监测应用入口，面向全球 TEC 及相关质量信息的业务展示与档案访问。适合欧洲用户做空间天气态势与 GNSS 单频改正评估；具体文件格式与引用条款以门户内文档为准。

#### [ESA-TIO-NRT-TEC](https://swe.ssa.esa.int/tio_tcr)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

ESA SWE 网络 Transionospheric 服务族中的近实时 TEC 图产品页，用于评估跨电离层链路与 GNSS 相关影响。与 DLR IMPC、ROB 欧洲 TEC 同属欧洲业务产品生态，可多源交叉验证。

#### [GFZ-Global-Ionosphere-Maps](https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/global-gnss-ionosphere-maps)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

德国地学研究中心作为 IGS 电离层分析中心（IAAC）的官方产品介绍：基于约 250 站 IGS 网、GPS/GLONASS/Galileo，用 EPOS.P8 生成全球 VTEC 图，并给出 DOI 与文献。本页偏文档/入口；批量 IONEX 请转到 ISDC 或 CDDIS 的 GFZ 产品路径。

#### [ionex-analyzer](https://github.com/matador96/ionex-analyzer)  
*🏷️ 个人社区*

语言：JavaScript · 许可：— · 星标约：0 · 宿主：github

用 Electron/React 做的 IONEX 可视化桌面小应用，交互浏览格网 TEC 较友好，来源为毕业设计风格仓库。适合演示与教学展示。研究级批处理、插值、DCB 与建模请回到 Python/MATLAB 工具链；星标低、维护不确定，当作原型参考即可，勿当生产依赖。若只需脚本绑图，优先轻量 Python 方案更易维护。

#### [MathWorks-ionex_reader](https://www.mathworks.com/matlabcentral/fileexchange/172149-ionex_reader)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：0 · 宿主：other

Bhuvnesh 发布的 ionex_reader 工具箱，可读取 IONEX、绘制 TEC/RMS 图并提取任意位置 TEC 时序，适合课堂快速可视化 IGS GIM。输入为 IONEX 文件与经纬坐标；输出为图与时序。局限：File Exchange 许可与更新节奏需查看页面；功能以读/画为主，不含球谐估解。

#### [ROB-European-TEC](https://gnss.be/SpaceWeather/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

ROB/OMA 基于 EUREF 常设网 GPS+GLONASS+Galileo 观测生成欧洲区域近实时 VTEC 与变率产品（约 5 分钟、0.5° 网格，2022-05 起多系统）。门户提供统计对比图与北/中/南欧时间序列，联系 iono@oma.be。适合欧洲区域扰动监测与 PPP 区域改正对照；全球尺度仍需 IGS/各 AC 的 GIM。

#### [ROB-IONEX-Products](https://gnss.be/SpaceWeather/Products/IONEX)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

与 gnss.be/SpaceWeather 可视化配套的 IONEX 文件归档，便于脚本批量拉取欧洲近实时 TEC 图。格式与 IGS IONEX 兼容，适合接入自有 TEC 可视化或 PPP 区域改正试验。使用前请阅读站点免责声明与引用要求。

#### [UWM-CDRSK-IGS-Validation](https://cdrsk.uwm.edu.pl/centrum-walidacji-i-kombinacji-igs/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Warmia-Mazury 大学空间环境射电诊断中心（CDRSK）对 IGS 电离层验证/组合职能的机构页，可与 igsiono.uwm.edu.pl 技术页对照。对需要联系组合中心或了解 UWM 职责分工的用户有用。

#### [UWM-IGS-Iono-Combination](https://igsiono.uwm.edu.pl/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

University of Warmia and Mazury（Olsztyn）承担 IGS 电离层图组合与验证相关门户，面向各 IAAC 独立 GIM 的加权组合（如 IGSG）流程与产品入口。与 IGS Ionosphere WG 页面互补，适合追踪官方组合策略与验证信息。

## 闪烁

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SuperSID](https://github.com/sberl/supersid) | 突发电离层扰动（SID）监测软件（跨平台，社区维护分支） | Python | 16 | 🏷️ 个人社区 |
| [SbfParser](https://github.com/septentrio-gnss/SbfParser) | Septentrio SBF 二进制流/文件解析（含闪烁相关块） | Cython | 12 | 🏷️ 官方 |
| [gnss-scintillation-simulator_2-param](https://github.com/cu-sense-lab/gnss-scintillation-simulator_2-param) | CU Sense Lab 两参数 GNSS 闪烁仿真器 | MATLAB | 6 | 🏷️ 高校实验室 |
| [Ionospheric-TEC-ROTI-Interactives](https://github.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives) | 交互式 TEC/ROTI 计算（可选高度角，扰动日/静日对比） | Python | 3 | 🏷️ 个人社区 |
| [roti-gnss-ml](https://github.com/NeelayS/roti-gnss) | 基于深度学习的 GNSS ROTI 时间序列预报实验代码 | Python | 3 | 🏷️ 个人社区 |
| [BiScEF](https://github.com/kartverket/BiScEF) | 挪威制图局 Kartverket：闪烁数据二进制交换格式 BiScEF 官方实现 | Python | 2 | 🏷️ 官方 |
| [igs-roti](https://github.com/jonathanblade/igs-roti) | IGS ROTI Maps 产品的 Web 可视化小工具 | Python | 2 | 🏷️ 个人社区 |
| [ionospheric-scintillation-mitigation](https://github.com/fengjie0325/ionospheric-scintillation-mitigation) | 电离层闪烁抑制算法的原始计算机代码 | MATLAB | 2 | 🏷️ 个人社区 |
| [FARR](https://gitlab.com/longleywj/farr) | FARR：磁化碰撞等离子体中电波传播的三维 FDTD 开源代码（GitLab） | C++ | 1 | 🏷️ 高校实验室 |
| [gnss-vector-scintillation](https://github.com/DTUSWx/gnss-vector-scintillation) | 矢量闪烁：Jones–Stokes GNSS 闪烁 MATLAB 参考码 | MATLAB | 1 | 🏷️ 高校实验室 |
| [scintkit](https://github.com/qwsae10/scintkit) | scintkit：ScintPi/GNSS 闪烁快看工具集 | Jupyter Notebook | 1 | 🏷️ 个人社区 |
| [IBP-Model](https://igit.iap-kborn.de/ibp/ibp-model) | IAP Kühlungsborn IBP：低纬赤道等离子体泡发生概率经验/ML 模型（机构 GitLab） | Python | 0 | 🏷️ 高校实验室 |
| [M_ISSION](https://github.com/wulide4/M_ISSION) | 多 GNSS 电离层闪烁指数计算软件 | C++ | 0 | 🏷️ 个人社区 |
| [ScintPi-1.0-Software](https://doi.org/10.5281/zenodo.4905193) | UT Dallas ScintPi 1.0：低成本 GNSS 闪烁仪采集与可视化软件（Zenodo ZIP） | unknown | — | 🏷️ 高校实验室 |
| [Swarm-VIP-Dynamic](https://gitlab.com/KNMI-OSS/spaceweather/swarm-vip-dynamic) | KNMI Swarm-VIP-Dynamic 工作仓：ISMR 闪烁文件处理与电离层模型评估脚本 | Python | 0 | 🏷️ 官方 |

### 详细说明

#### [SuperSID](https://github.com/sberl/supersid)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

SuperSID 用简易 VLF 接收监测突发电离层扰动（太阳耀斑等引起的 D 区吸收变化），sberl 分支相对活跃。输出 SID 幅度时间序列。局限：监测的是 VLF 幅度而非 GNSS TEC；站点环境噪声影响大。

#### [SbfParser](https://github.com/septentrio-gnss/SbfParser)  
*🏷️ 官方*

语言：Cython · 许可：BSD-3-Clause · 星标约：12 · 宿主：github

官方生态 Python/Cython 解析器，把 SBF 流转成 JSON 结构，社区已扩展 ISMR（4086）等闪烁监测块，便于从 PolaRx 系列提取 S4、σφ 等。输入为 SBF 文件或流；输出为结构化观测/状态块。局限：侧重解码而非完整闪烁科学产品流水线；大文件需注意内存策略。

#### [gnss-scintillation-simulator_2-param](https://github.com/cu-sense-lab/gnss-scintillation-simulator_2-param)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

科罗拉多大学 Sense Lab 的两参数版 GNSS 闪烁仿真，相对完整版简化相位/幅度扰动建模，便于接收机与信号处理压力测试。适合教学与算法试验。真实赤道/极区场景请结合实测 ISMR 与原版多参数仿真器对照评估。

#### [Ionospheric-TEC-ROTI-Interactives](https://github.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：3 · 宿主：github

带 Tkinter/交互流程的 TEC 与 ROTI 计算工具，可按高度角筛选并对比扰动日与静日，输出 30 s 与 5 min 窗口 ROTI。输入为用户准备的 TEC 数据文件夹（非完整 RINEX 解算链）。局限：依赖外部已算好的 TEC；GUI 交互偏本地脚本；许可未声明。

#### [roti-gnss-ml](https://github.com/NeelayS/roti-gnss)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：3 · 宿主：github

Notebook 实验：对 GNSS 导出的 ROTI 做深度学习时序预报。局限：研究原型；数据与复现说明有限；不是业务 ROTI 生成器。

#### [BiScEF](https://github.com/kartverket/BiScEF)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：2 · 宿主：github

挪威制图局（Kartverket）维护的 Binary Scintillation Exchange Format 实现与示例；stenseng/BiScEF 已声明迁移至此仓，故目录只保留官方仓。便于闪烁监测接收机数据互通；做多源融合时关注格式版本。通用 TEC/ROTI 计算仍用 IonoMoni/OASIS 等。

#### [igs-roti](https://github.com/jonathanblade/igs-roti)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：2 · 宿主：github

针对 IGS ROTI map 产品的可视化网页/工具，方便快速查看全球/区域 ROTI 图，而不是从原始观测算 ROTI。局限：依赖 IGS 产品发布；仓库小、维护有限。

#### [ionospheric-scintillation-mitigation](https://github.com/fengjie0325/ionospheric-scintillation-mitigation)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：2 · 宿主：github

论文配套闪烁抑制算法实现（MATLAB），用于理解跟踪环/信号处理层面的缓解思路。输入为受闪烁影响的信号/观测量仿真或实测；输出为抑制后结果对比。局限：代码体量小、场景专用；不替代接收机厂商闭源算法。

#### [FARR](https://gitlab.com/longleywj/farr)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：1 · 宿主：gitlab

NJIT/Boston University 的三维 FDTD 开源码（GitLab，GPL-3.0），仿真磁化碰撞等离子体中的电波传播与闪烁。提供 CMake/Docker/Python 辅助。面向传播机理研究，不是 GNSS 观测解算或 GIM 产品工具。

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

莱布尼茨大气物理所 Kühlungsborn 在机构 GitLab（igit.iap-kborn.de）开源的 Ionospheric Bubble Probability 模型，基于 CHAMP/Swarm 磁场与电子密度，输出随 DOY/经度/地方时/F10.7 变化的低纬泡发生概率指数（0–1），并可 pip 安装 ibpmodel。MIT 许可，文档见 ReadTheDocs。适合赤道闪烁/EPB 气候概率与 Swarm L2 IBP_CLI 产品对照；非 TEC 反演工具。公开仓 HTTP 200。

#### [M_ISSION](https://github.com/wulide4/M_ISSION)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：0 · 宿主：github

面向多系统 GNSS 的闪烁指数（如 S4 等）处理软件，仓库体积较大，适合闪烁监测实验。输入为高频采样 GNSS 观测；输出为闪烁指数产品。局限：开源许可与文档需自行确认；部署依赖可能偏工程化。

#### [ScintPi-1.0-Software](https://doi.org/10.5281/zenodo.4905193)  
*🏷️ 高校实验室*

语言：unknown · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

德州大学达拉斯分校发布的 ScintPi 1.0 官方采集/可视化软件 ZIP（concept DOI 10.5281/zenodo.4905193），经 USB 连接硬件，面向教育与低成本闪烁监测。CC-BY-4.0，“as is”无质保。与 GitHub 上第三方 scintkit 小工具不同，本条是仪器配套官方软件存档。适合教学网部署；论文级多站 S4/σφ 分析仍需专用 GISTM 或商用接收机链路。

#### [Swarm-VIP-Dynamic](https://gitlab.com/KNMI-OSS/spaceweather/swarm-vip-dynamic)  
*🏷️ 官方*

语言：Python · 许可：see upstream repository · 星标约：0 · 宿主：gitlab

KNMI 在 Swarm-VIP-Dynamic（UiO/Birmingham/INGV/DLR/KNMI）合作中的代码仓：含有效 F10.7 代理、Septentrio PolaRX5S ISMR 闪烁监测文件处理与可视化、项目模型及 IBP 等外部模型评估、Swarm 轨道派生磁纬/地方时等。与 swarm-vip-dynamic-models 库配套，偏研究流水线与闪烁数据可视化。公开 GitLab 仓；许可以仓内说明为准。页面 HTTP 200。

## 电离层工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RMextract](https://github.com/lofar-astron/RMextract) | RMextract：ASTRON 射电天文 TEC/RM 经典工具（已继任） | C | 36 | 🏷️ 官方 |
| [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting) | TEC、foF2 与 DST 等指数的绘图脚本 | Python | 7 | 🏷️ 个人社区 |
| [GRITI](https://github.com/dinsmoro/GRITI) | GRITI：多源电离层瞬变分析与可视化工具箱 | Python | 5 | 🏷️ 高校实验室 |
| [spinifex](https://git.astron.nl/RD/spinifex) | ASTRON Spinifex：射电天文 TEC/RM 电离层工具 | Python | 4 | 🏷️ 官方 |
| [ionex-downloader](https://github.com/ohm1122/ionex-downloader) | 批量下载 IONEX/GIM 产品的脚本 | — | 1 | 🏷️ 个人社区 |
| [nleht-fdtd-ionosphere](https://gitlab.com/nleht/fdtd) | nleht/fdtd：电离层 VLF 波 MPI 并行 FDTD 计算代码（GitLab） | C++ | 1 | 🏷️ 高校实验室 |
| [pypride](https://gitlab.com/gofrito/pypride) | pypride：行星雷达/VLBI 处理库（含 IONEX TEC 获取与闪烁表 TEC 计算） | Python | 1 | 🏷️ 高校实验室 |
| [Boston-College-ISR-Ionospheric-Studies](https://www.bc.edu/bc-web/research/sites/institute-for-scientific-research/research/ionospheric-studies.html) | Boston College ISR 电离层研究组主页（闪烁、层析与 GNSS TEC 方向） | data-portal | — | 🏷️ 高校实验室 |
| [CARP-Average-Profile](https://ulcar.uml.edu/SoftwareUtilities/CARP/) | CARP：测高仪平均代表剖面（Average Representative Profile）计算工具 | Fortran | — | 🏷️ 高校实验室 |
| [Drift-X](https://ulcar.uml.edu/Drift-X.html) | Drift Explorer（Drift-X）：Digisonde 漂移数据可视化与分析 Java 工具 | Java | — | 🏷️ 高校实验室 |
| [IMSP-MGS](https://essr.esa.int/project/ionosphere-modular-software-package-imsp-mgs) | ESA IMSP+MGS：GNSS-R/SAR/雷达测深电离层效应模块化仿真包 | unknown | — | 🏷️ 官方 |
| [IonKit-NH](https://github.com/ohm1122/IonKit-NH) | IonKit-NH 电离层工具包 | — | — | 🏷️ 个人社区 ★ |
| [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH) | IonKit-NH 相关衍生/整理 | — | — | 🏷️ 个人社区 ★ |
| [IonTools](https://github.com/rumkex/IonTools) | IonTools：电离层分析辅助小工具（C++） | C++ | — | 🏷️ 个人社区 ★ |
| [NHPC-TrueHeight](https://ulcar.uml.edu/SoftwareUtilities/NHPC/) | NHPC：测高仪迹线真高剖面反演工具（Digisonde/ARTIST 配套） | Fortran/C | — | 🏷️ 高校实验室 |
| [NICT-Ionosonde-Data](https://wdc.nict.go.jp/Ionosphere/index.html) | NICT 日本测高仪（ionosonde）观测数据入口 | data-portal | — | 🏷️ 官方 |
| [SAO-Explorer](https://ulcar.uml.edu/SAO-X/) | GIRO/Digisonde 测高仪缩放与 DIDBase 访问工具（免费二进制） | Java | — | 🏷️ 官方 |
| [swarm-vip-dynamic-models](https://gitlab.com/KNMI-OSS/spaceweather/libs/swarm-vip-dynamic-models) | KNMI Swarm-VIP-Dynamic：Swarm 原位电子密度与不规则性 GLM 经验模型 Python 包 | Python | 0 | 🏷️ 官方 |
| [UMLCAR-Downloads](https://ulcar.uml.edu/downloads.html) | UMass Lowell UMLCAR 电离层软件下载中心（SAO-X/Drift-X/NHPC/DCART 等） | data-portal | — | 🏷️ 高校实验室 |

### 详细说明

#### [RMextract](https://github.com/lofar-astron/RMextract)  
*🏷️ 官方*

语言：C · 许可：GPL-3.0 · 星标约：36 · 宿主：github

荷兰 ASTRON 长期使用的 RMextract，面向射电干涉测量从 GPS TEC 与地磁模型估计旋转量度等。仓库注明已被 Spinifex 继任且不再积极开发，但仍广泛出现在文献与旧流程中。适合对照复现；新项目优先 Spinifex。许可 GPL-3.0。

#### [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：7 · 宿主：github

面向 TEC、foF2、DST 等指数与时间序列的 Python 绑图工具，适合快速出教学图或报告插图。研究级 GIM/STEC 重建请用 gnss-tec、MosGIM2 等；本仓库偏可视化与展示，数据获取与许可需自备，不宜单独支撑反演论文。输入数据格式需按脚本说明自行对齐时间与单位。选用前请用自有数据做交叉验证。

#### [GRITI](https://github.com/dinsmoro/GRITI)  
*🏷️ 高校实验室*

语言：Python · 许可：AGPL-3.0 · 星标约：5 · 宿主：github

宾州州立相关开源仓 GRITI，面向电离层瞬变事件的 Python 分析流水线：可自动拉取 Madrigal δvTEC、AMPERE、Kp 与 OMNI，并做 keogram、滑动相关、FFT/Lomb-Scargle 等。需要本地配置路径与部分账号；部分 ISR/磁强计数据需自行下载。适合空间天气个例研究，不是从 RINEX 重建 TEC 的解算器。

#### [spinifex](https://git.astron.nl/RD/spinifex)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：4 · 宿主：gitlab

荷兰 ASTRON 维护的 Spinifex，用纯 Python 从 IONEX/TOMION 等模型估计视线 TEC 与旋转量度（RM），面向 LOFAR 等干涉测量改正。可 pip 安装 GitLab 主仓；GitHub 仅为镜像。依赖外部 IONEX 下载与地磁模型，不是 GNSS 双频 STEC 估计算法本身。

#### [ionex-downloader](https://github.com/ohm1122/ionex-downloader)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：1 · 宿主：github

批处理拉取 IONEX（GIM）文件的小工具，减少手工下载 IGS 或分析中心产品的重复劳动。适合电离层课题数据准备与课程作业。维护活跃度与镜像源覆盖有限，生产流水线更常见用 wget/aria2、FAST 或机构自建镜像；下载后可用 IonMap 或 gnss-lab/ionex 继续处理。注意分析中心产品时延与文件命名规则变化。

#### [nleht-fdtd-ionosphere](https://gitlab.com/nleht/fdtd)  
*🏷️ 高校实验室*

语言：C++ · 许可：see upstream repository · 星标约：1 · 宿主：gitlab

面向电离层中甚低频（VLF）波传播的三维时域有限差分 C++ 代码，支持 MPI 多节点。适合低电离层/波导传播与 D 区扰动数值实验，与 GNSS L 波段闪烁工具互补。公开 GitLab 项目；许可与构建说明以仓库为准。页面可访问。

#### [pypride](https://gitlab.com/gofrito/pypride)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT (see upstream; classifiers also mention GPL) · 星标约：1 · 宿主：gitlab

GitLab 上的 pypride（PRIDE 相关派生）Python/Fortran 混合包，面向深空/VLBI 几何与延迟处理；内含从 CDDIS 拉取 IONEX 及 computeTEC 等由闪烁观测表估计上下行电离层贡献的脚本。MIT/GPL 标注并存，以仓内为准。对 GNSS 电离层用户价值在于 IONEX 自动获取与行星际闪烁相关 TEC 估算；主业并非地面 GNSS TEC 流水线。公开仓可克隆。

#### [Boston-College-ISR-Ionospheric-Studies](https://www.bc.edu/bc-web/research/sites/institute-for-scientific-research/research/ionospheric-studies.html)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

波士顿学院科学研究所电离层研究方向介绍，涵盖全球扰动、层析与闪烁对 GNSS 影响等。作为 Seemala GPS-TEC 等工具的机构背景页收录；部分站点可能对非浏览器客户端返回 406，建议用常规浏览器打开。

#### [CARP-Average-Profile](https://ulcar.uml.edu/SoftwareUtilities/CARP/)  
*🏷️ 高校实验室*

语言：Fortran · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

UMLCAR 提供的平均代表剖面工具，用于从多幅测高图剖面提取统计代表结构。服务气候态与模型验证场景；与 NHPC/SAO-X 同属测高仪处理链。

#### [Drift-X](https://ulcar.uml.edu/Drift-X.html)  
*🏷️ 高校实验室*

语言：Java · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

UMLCAR 发布的 Digisonde 漂移（DDA）数据查看器，当前发行约 1.2.14-FB3，ZIP 解压即用。面向测高仪漂移观测质控与教学；与 SAO-X 测高图定标流程互补，不直接输出 GNSS TEC。

#### [IMSP-MGS](https://essr.esa.int/project/ionosphere-modular-software-package-imsp-mgs)  
*🏷️ 官方*

语言：unknown · 许可：ESA Community License v2.4 Strong Copyleft (Type 1) · 星标约：— · 宿主：official_site

ONERA/RDA/IEEC 在 ESA TDE 框架下开发、经 ESSR 发布的 Ionosphere Modular Software Package，用于仿真 GNSS-R、SAR 与雷达测深等任务几何及 30 MHz–3 GHz 主要电离层效应。适合任务设计与电离层误差敏感性分析，而非地面 GNSS TEC 产品流水线。源码经 ESSR git 提供，许可为 ESA Community License v2.4 Strong Copyleft；下载需 ESSR 账号。页面 HTTP 200。

#### [IonKit-NH](https://github.com/ohm1122/IonKit-NH)  
*🏷️ 个人社区 ★*

语言：— · 许可：GPL-3.0 · 星标约：— · 宿主：github

IonKit-NH 工具包星标种子，覆盖电离层数据处理相关脚本。适合浏览星标工作流；与 tanggdut 衍生版注意分辨上游。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH)  
*🏷️ 个人社区 ★*

语言：— · 许可：GPL-3.0 · 星标约：— · 宿主：github

IonKit-NH 的衍生整理版，可能含路径或示例改动。合并进产线前先 diff 上游 ohm1122 版本，避免重复维护。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonTools](https://github.com/rumkex/IonTools)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：— · 宿主：github

GitHub rumkex/IonTools，偏辅助脚本/小工具集合，用来补主流程里零散步骤。功能边界以仓库说明为准；关键 TEC/GIM 结论建议用主流库复核，勿把过时脚本当生产基线。

#### [NHPC-TrueHeight](https://ulcar.uml.edu/SoftwareUtilities/NHPC/)  
*🏷️ 高校实验室*

语言：Fortran/C · 许可：UML academic (AS IS) · 星标约：— · 宿主：official_site

将 ARTIST 等自动/人工定标的测高仪迹线反演为等离子体频率–真高剖面的经典工具，常嵌入 SAO Explorer 工作流。适合底层电离层剖面研究与 IRI/IRTAM 对照；输入依赖合格 SAO/定标结果，非 GNSS TEC 估计器。

#### [NICT-Ionosonde-Data](https://wdc.nict.go.jp/Ionosphere/index.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Wakkanai、Kokubunji、Yamagawa、Okinawa 等日本测高仪数字化资料入口，可与 GIRO/DIDBase 全球测高仪生态对照。适合 foF2/hmF2 气候统计或与 GNSS TEC 联合分析；不是 GNSS IONEX 替代品。

#### [SAO-Explorer](https://ulcar.uml.edu/SAO-X/)  
*🏷️ 官方*

语言：Java · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

处理 SAO/SAOXML、内置 ARTIST-5 与剖面反演，并可连 Lowell DIDBase。irimodel 相关的 IRTAM/GIRO 生态常用桌面工具。官方提供跨平台 zip，属免费科学软件而非公开 OSS 源码（license 标 proprietary-freeware）。不做 GNSS TEC 建图；源码级二次开发请另寻开源栈。

#### [swarm-vip-dynamic-models](https://gitlab.com/KNMI-OSS/spaceweather/libs/swarm-vip-dynamic-models)  
*🏷️ 官方*

语言：Python · 许可：BSD-3-Clause · 星标约：0 · 宿主：gitlab

荷兰皇家气象研究所（KNMI）在 GitLab 发布的 Python 包，评估 Swarm VIP Dynamic 项目拟合的广义线性模型，按地理位置、磁纬/地方时、季节、F10.7、Kp/Hp30 与太阳风等输入预测 Ne、RODI 等电离层参数，覆盖赤道至极区。依赖 pandas/numpy，可自动拉取 OMNI/F10.7/Kp。BSD-3-Clause。适合 Swarm 原位气候态对照与不规则性气候研究；非 GNSS TEC 估计器。仓库可公开克隆。

#### [UMLCAR-Downloads](https://ulcar.uml.edu/downloads.html)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

洛厄尔麻省大学大气研究中心官方下载索引：SAO Explorer（含 ARTIST-5）、Drift-X、BinBrowser、DCART、NHPC、CARP 等 Digisonde/测高仪工具集中入口。已单独收录 SAO-X 主页，本条作为软件总目录便于发现其余开源/可下载工具。

## IRI模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyglow](https://github.com/timduly4/pyglow) | pyglow：上层大气气候态 Python 库 | Python/Fortran | 117 | 🏷️ 个人社区 核心 |
| [pyIRI2016](https://github.com/rilma/pyIRI2016) | IRI-2016 Fortran 的 f2py 包装（pyiri2016，与 space-physics/iri2016 不同仓） | Python/Fortran | 21 | 🏷️ 个人社区 |
| [PyIRTAM](https://github.com/victoriyaforsythe/PyIRTAM) | IRTAM 系数下载与全球网格电子密度重建（纯 Python，对接 PyIRI） | Python | 4 | 🏷️ 高校实验室 核心 |
| [iricore](https://github.com/MIST-Experiment/iricore) | ctypes 包装 IRI-2016/2020，可算 VTEC/STEC 并更新指数文件 | Python/Fortran | 2 | 🏷️ 个人社区 |
| [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/) | NASA CCMC 在线运行与说明页（IRI-2020） | — | — | 🏷️ 官方 |
| [GAMBIT-Database-Reader-Java](https://giro.uml.edu/GAMBIT/GambitReader_Java_V0.1.zip) | 官方示例：GAMBIT 数据库 Java 读入/解包（拉 IRTAM 系数） | Java | — | 🏷️ 官方 |
| [GIRO-GAMBIT](https://giro.uml.edu/GAMBIT/) | GIRO GAMBIT：底部电离层时间线全球同化模型门户与系数服务 | data-portal | — | 🏷️ 高校实验室 |
| [GIRO-IRTAM](https://giro.uml.edu/IRTAM/) | GIRO IRTAM：基于全球测高仪的 IRI 实时同化 foF2/hmF2 等映射 | data-portal | — | 🏷️ 高校实验室 |
| [IRI-2001-package](https://irimodel.org/IRI-2001/) | IRI-2001 官方 Fortran 历史版本源码目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2007-package](https://irimodel.org/IRI-2007/) | IRI-2007 官方 Fortran 历史版本源码目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2012-package](https://irimodel.org/IRI-2012/) | IRI-2012 官方 Fortran 源码包（含轨道剖面示例程序） | Fortran | — | 🏷️ 官方 |
| [IRI-2016-package](https://irimodel.org/IRI-2016/) | IRI-2016 官方 Fortran 源码与系数包目录 | Fortran | — | 🏷️ 官方 |
| [IRI-2026-package](https://irimodel.org/IRI-2026/) | IRI-2026 官方 Fortran 最新源码包目录 | Fortran | — | 🏷️ 官方 核心 |
| [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/) | 各版 IRI 共用的系数/公共文件目录（官网明确要求另下） | Fortran | — | 🏷️ 官方 核心 |
| [IRI-indices](https://irimodel.org/indices/) | IRI 运行所需太阳/地磁指数文件发布页 | — | — | 🏷️ 官方 |
| [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model) | irimodel.org 官方指向的 IRI MATLAB 封装（File Exchange，含 2012/2016） | MATLAB | — | 🏷️ 官方 核心 |
| [IRI-Plas-SPIM-IZMIRAN](https://www.izmiran.ru/ionosphere/weather/grif/SPIM/) | IZMIRAN IRI-Plas/SPIM：扩展至等离子体层的 IRI Fortran 源码与系数包 | Fortran | — | 🏷️ 官方 |
| [IRTAM-Coefficient-Reader-Fortran](https://giro.uml.edu/GAMBIT/IrtamReader_Fortran_V1.0.zip) | 官方示例：IRTAM 系数 Fortran 读入器（对接 IRI 同化） | Fortran | — | 🏷️ 官方 |
| [pyFIRI2018](https://bitbucket.org/ozolotov/pyfiri2018) | pyFIRI：FIRI-2018 非极光 D 区参考电离层的 Python3 实现（Bitbucket） | Python | — | 🏷️ 高校实验室 |

### 详细说明

#### [pyglow](https://github.com/timduly4/pyglow)  
*🏷️ 个人社区 核心*

语言：Python/Fortran · 许可：MIT · 星标约：117 · 宿主：github

把 IRI 等上层大气经验模型接到 Python，irimodel.org 在「pyglow」一行直接链到本仓库，说明它是社区里常用的 IRI-2012/2016 包装路径。适合脚本化批量取 Ne/Te 剖面、和 GNSS TEC 产品做气候态对照。底层仍依赖 Fortran 模型文件与指数更新；跟官方最新 IRI-2020/2026 发布节奏可能不同步，精密业务应核对所绑版本。许可 MIT，比部分需注册的官方 C 发行更好集成。

#### [pyIRI2016](https://github.com/rilma/pyIRI2016)  
*🏷️ 个人社区*

语言：Python/Fortran · 许可：MIT · 星标约：21 · 宿主：github

用现代 CMake + f2py 暴露 iriwebg，便于在 Python 中调用 IRI-2016。与 space-physics/iri2016、官方 irimodel 目录并存时，注意不要混淆仓库名与系数版本。需要编译器链；要最新物理选项仍应回 irimodel.org 的 IRI-2020/2026。

#### [PyIRTAM](https://github.com/victoriyaforsythe/PyIRTAM)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

面向 GIRO/IRTAM 同化产物：可读/下载 IRTAM 系数，在给定全球网格与全日时间轴上同时评估 foF2/hmF2 等并重建 Ne。适合把实时同化电离层接到 Python 科研流水线，与气候态 PyIRI 对照。系数来自 LGDC/GAMBIT 接口，需遵守站点访问节奏；不是官方 Fortran irirtam.for 的逐行移植，数值对比请以 IRI-2020 包内 irirtam 子程序为参照。

#### [iricore](https://github.com/MIST-Experiment/iricore)  
*🏷️ 个人社区*

语言：Python/Fortran · 许可：see upstream · 星标约：2 · 宿主：github

把官方 Fortran IRI 编进可 pip 安装的 Python 包，暴露剖面与垂直/斜 TEC，并提供指数文件更新入口。适合 Linux 科研脚本里快速取气候态背景。文档写明主要处理 OUTF、未实现 OARR 用户输入；Windows 需 WSL，且维护节奏偏慢，跟 IRI-2026 对齐前应核对所绑 Fortran 版本。

#### [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：— · 宿主：official_site

NASA 社区协调建模中心提供的 IRI 在线计算与模型说明入口，适合快速查剖面、看输入开关，而不是本地二次开发。要嵌入自己的 GNSS/TEC 流水线仍需下载 irimodel Fortran 或 Python/MATLAB 包装。页面会指向模型版本与相关文献，可作为官方文档跳板。

#### [GAMBIT-Database-Reader-Java](https://giro.uml.edu/GAMBIT/GambitReader_Java_V0.1.zip)  
*🏷️ 官方*

语言：Java · 许可：UMLCAR/GIRO distribution (see archive) · 星标约：— · 宿主：official_site

GIRO 提供的 Java 示例，用于从 GAMBIT 侧取系数并解包。适合需要脚本化批量取同化系数、又不走 Python 的环境。示例级代码，商用实时 Situation Room 另需订阅协议；系数下载请遵守站点建议的请求间隔。

#### [GIRO-GAMBIT](https://giro.uml.edu/GAMBIT/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GAMBIT（Global Assimilative Model of Bottomside Ionospheric Timeline）官方主页，提供与 IRTAM 相关的系数获取与工具说明。目录中已有 Java/Fortran 读取器下载链接，本条收录门户本身以便发现 API/文档更新。

#### [GIRO-IRTAM](https://giro.uml.edu/IRTAM/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Global Ionospheric Radio Observatory 的 IRI Real-Time Assimilative Mapping 服务页，将全球 Digisonde 近实时特性同化进 IRI，生成 F2 临界频率与峰高近实时图。已收录 IRTAM 系数读取器压缩包与 PyIRTAM，本条补齐官方产品可视化/服务入口。

#### [IRI-2001-package](https://irimodel.org/IRI-2001/)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

更早的官方 IRI 发行，主要用于历史复现。系数与选项与当代版本差异大，不适合作为现行 GNSS 电离层改正基准；对照阅读可看官网更新说明与 Bilitza 综述。

#### [IRI-2007-package](https://irimodel.org/IRI-2007/)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

官方保留的 IRI-2007 发行，便于复现该年代论文或对比模型演进。新项目应改用 IRI-2020/2026；仅当审稿或历史对比需要锁定旧物理选项时再下载本目录。

#### [IRI-2012-package](https://irimodel.org/IRI-2012/)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

官方 IRI-2012 发行目录。官网特别提到该版带有 iriorbit 一类沿卫星轨道取 IRI 参数的示例程序，适合空间任务剖面复现与旧论文对照。功能与数据源已有后续版本更新；除非复现 2012 时代结果，新项目优先 IRI-2020/2026，MATLAB/pyglow 用户也要分清自己绑的是哪一代。

#### [IRI-2016-package](https://irimodel.org/IRI-2016/)  
*🏷️ 官方*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

COSPAR/URSI IRI 工作组在 irimodel.org 发布的 IRI-2016 源码目录，含 Fortran 子程序、系数与说明。很多文献与 MATLAB/pyglow 包装仍对齐这一代。新研究若无追踪官方最新物理选项，应同时看 IRI-2020/2026；指数文件需按官网说明单独更新。

#### [IRI-2026-package](https://irimodel.org/IRI-2026/)  
*🏷️ 官方 核心*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

irimodel.org 上标注日期最新的 IRI Fortran 发行目录，工作组持续更新的气候态电离层国际标准模型入口。做与最新文献对齐的 Ne/Te/离子成分剖面时优先从这里取源码与系数。指数文件仍需按官网说明单独更新；Python/MATLAB 包装未必已跟上 2026，绑定前核对版本号。

#### [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/)  
*🏷️ 官方 核心*

语言：Fortran · 许可：— · 星标约：— · 宿主：official_site

irimodel 写明：除版本包外通常还要 COMMON FILES（若 zip 未打进包内）。缺公共系数时编译或运行常失败。搭本地 IRI 时与具体版本目录、最新 INDICES 一起下载；不要只克隆 GitHub 包装而漏官方公共文件。

#### [IRI-indices](https://irimodel.org/indices/)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：— · 宿主：official_site

官方指数文件入口（如 ap、IG、F10.7 相关序列）。IRI 按日期查内部指数，过期指数会让剖面偏离。业务或论文复现应定期更新本页文件；pyglow/第三方包装若自带指数，也要核对其时效。

#### [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model)  
*🏷️ 官方 核心*

语言：MATLAB · 许可：— · 星标约：— · 宿主：official_site

irimodel.org 官方列出的 IRI MATLAB 入口（MathWorks File Exchange，含 2012/2016）。适合已在 MATLAB 做气候态对比、不想先编译 Fortran 的用户。下载与许可以 File Exchange 为准；追最新物理更新仍应回 irimodel.org / IRI 主源码。

#### [IRI-Plas-SPIM-IZMIRAN](https://www.izmiran.ru/ionosphere/weather/grif/SPIM/)  
*🏷️ 官方*

语言：Fortran · 许可：scientific distribution (cite required) · 星标约：— · 宿主：official_site

IZMIRAN 官方 IRI-Plas/SPIM 下载页：Fortran 主程序与系数包，把 IRI 扩展到等离子体层并可同化 GPS TEC。适合需要等离子体层 TEC 的气候态/同化试验；编译与系数版本须与页面 ZIP 对齐，不是 GNSS STEC 观测解算器。

#### [IRTAM-Coefficient-Reader-Fortran](https://giro.uml.edu/GAMBIT/IrtamReader_Fortran_V1.0.zip)  
*🏷️ 官方*

语言：Fortran · 许可：UMLCAR/GIRO distribution (see archive) · 星标约：— · 宿主：official_site

从 GAMBIT 页下载的 Fortran 示例，演示如何解析 IRTAM 系数消息并与 IRI 模型联用。适合本地同化/复现研究，而非网页看图。仅为示例读入器，完整实时同化流水线与系数服务条款见 GIRO/GAMBIT；Python 侧可对照 PyIRTAM。

#### [pyFIRI2018](https://bitbucket.org/ozolotov/pyfiri2018)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：— · 宿主：other

Oleg Zolotov 等实现的 FIRI-2018（Friedrich 等更新的低电离层经验模式）Python 包，用 xarray 对论文附表电子密度剖面插值，服务 VLF/低频传播与 D 区研究。Apache-2.0。原 GitLab 镜像注明已迁至 Bitbucket；与 GitHub 上其他 FIRI 表格式发布可并存。请同时引用 Friedrich et al. 2018 与 Zolotov et al. SoftwareX 2021。页面 HTTP 200。

## GIM

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [csonde-gnss-ionosphere](https://github.com/csonde/gnss) | RINEX 解析 + 格网/球谐电离层建模的 C 程序集 | C | 10 | 🏷️ 高校实验室 |
| [GIM_fusion_VLBI](https://github.com/arrueegg/GIM_fusion_VLBI) | 把 VLBI 信息同化/融合进全球电离层图（GIM）的研究代码 | Python | 1 | 🏷️ 高校实验室 |
| [DiffIonMap](https://github.com/Jin-Whu/DiffIonMap) | IONEX 差分成图：对比分析中心或风暴扰动 | Python | 0 | 🏷️ 个人社区 |
| [Ionospheric-TEC-Kriging-Turkiye](https://github.com/skaratay/Ionospheric-TEC-Kriging-Turkiye) | 土耳其区域 TEC 风暴分析的普通克里金/GPR MATLAB 代码 | MATLAB | 0 | 🏷️ 高校实验室 |

### 详细说明

#### [csonde-gnss-ionosphere](https://github.com/csonde/gnss)  
*🏷️ 高校实验室*

语言：C · 许可：GPL-3.0 · 星标约：10 · 宿主：github

匈牙利相关学位论文配套代码：含 RINEX 解析、格网电离层模型、球谐模型求解与 PCA 等，适合作为区域建模教学示例。局限：偏研究原型；构建与输入约定需读论文/源码；GPL。

#### [GIM_fusion_VLBI](https://github.com/arrueegg/GIM_fusion_VLBI)  
*🏷️ 高校实验室*

语言：Python · 许可：unknown · 星标约：1 · 宿主：github

探索将 VLBI 相关信息融入 GIM 的数据同化/融合流程，拓展传统纯 GNSS GIM。局限：研究仓、星数低；输入数据与实验配置需读论文/脚本；非业务 GIM 软件。

#### [DiffIonMap](https://github.com/Jin-Whu/DiffIonMap)  
*🏷️ 个人社区*

语言：Python · 许可：unknown · 星标约：0 · 宿主：github

读入两份 IONEX，生成差分 TEC 图，便于对比分析中心产品或风暴扰动相对变化。极简、久未更新。不负责产品下载与质量控核；批量业务制图请用专业 IONEX/GIM 流水线。

#### [Ionospheric-TEC-Kriging-Turkiye](https://github.com/skaratay/Ionospheric-TEC-Kriging-Turkiye)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：0 · 宿主：github

用普通克里金（及 GPR 表述）做土耳其上空 TEC 时空分析，覆盖太阳周 24–25 风暴个例，属于区域插值建图示例。局限：区域与个例绑定；MATLAB；推广到全球网格需改观测网与协方差模型。

## TEC预报

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tec_forecast](https://github.com/mauriciodev/tec_forecast) | 基于深度学习的全球 TEC 图预报示例 | Jupyter Notebook | 31 | 🏷️ 个人社区 ★ |
| [DeepPredTEC](https://github.com/vtsuperdarn/DeepPredTEC) | 深度学习预报 GPS TEC 图（SuperDARN 相关） | Python | 13 | 🏷️ 高校实验室 |
| [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM) | 注意力 ConvLSTM 的 TEC 图预报模型 | Jupyter Notebook | 10 | 🏷️ 个人社区 |
| [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting) | IAG 研究组 ML 预报 VTEC 的教学示例 | Jupyter Notebook | 9 | 🏷️ 高校实验室 ★ |
| [t-fors](https://github.com/viventriglia/t-fors) | 行进式电离层扰动（TID）预报系统 T-FORS | HTML | 7 | 🏷️ 高校实验室 |
| [ESA-TIO-Forecast-TEC](https://swe.ssa.esa.int/tio_tcf) | ESA TIO TEC 预报图服务（约 1 小时量级电离层预报） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [tec_forecast](https://github.com/mauriciodev/tec_forecast)  
*🏷️ 个人社区 ★*

语言：Jupyter Notebook · 许可：MIT · 星标约：31 · 宿主：github

用 Keras/TF 等多类深度学习模型在全球电离层图上做 TEC 预报实验。适合学 ML+空间天气交叉的人对照复现。不是业务预报系统；数据切分、基线与物理约束要自己补齐，可与 ED-AttConvLSTM 等对比。

#### [DeepPredTEC](https://github.com/vtsuperdarn/DeepPredTEC)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：13 · 宿主：github

面向 GPS TEC 图时空预报的深度学习开源实现（SuperDARN 相关团队），可复现论文结构并作空间天气基线。适合电离层 ML 实验。工程同化与多源融合需自建；输入网格、缺失填充与评分指标要与业务 GIM 对齐后再谈业务化。

#### [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：10 · 宿主：github

编码器—解码器加注意力的 ConvLSTM，针对 TEC 图时序预报。适合复现相关论文结构。工程部署与多源同化不在范围；输入 GIM 分辨率与缺失值处理需自建。

#### [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting)  
*🏷️ 高校实验室 ★*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：9 · 宿主：github

IAG ICCT「大地测量中的机器学习」联合研究组示例，用公开流程演示 VTEC 机器学习预报，Apache-2.0 许可清晰。适合课堂与方法入门。模型深度与业务指标达不到业务空间天气预报标准。

#### [t-fors](https://github.com/viventriglia/t-fors)  
*🏷️ 高校实验室*

语言：HTML · 许可：MIT · 星标约：7 · 宿主：github

欧盟 Horizon 资助的 TID 预报相关开源组件/门户代码，面向扰动预警演示。输入为电离层扰动相关观测与模型配置；输出为 TID 预报产品。局限：业务可用性依赖数据源；与实时 GIM 生产不同。

#### [ESA-TIO-Forecast-TEC](https://swe.ssa.esa.int/tio_tcf)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

与近实时 TEC 配套的预报产品入口，服务短时电离层状态预估与链路质量评估。适合运行支持与教学演示；科学研究若需可复现网格文件，请在登录后按服务说明导出并记录版本/时次。

## 电离层产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IRTS_SDK](https://github.com/1acheng/IRTS_SDK) | 全球电离层实时云服务（IRTS）客户端 SDK | — | 2 | 🏷️ 个人社区 |
| [DLR-IMPC](https://impc.dlr.de/) | DLR 电离层监测与预报中心（IMPC，原 SWACI 继承）：近实时全球/欧洲 TEC、ROTI 与预警门户 | data-portal | — | 🏷️ 官方 |
| [DLR-IMPC-Products](https://impc.dlr.de/products) | DLR IMPC 产品与档案入口：近实时 TEC/ROTI 等电离层产品分类浏览与下载 | data-portal | — | 🏷️ 官方 |
| [ESA-SWE-Registration](https://swe.ssa.esa.int/registration) | ESA SWE/SSA 门户免费账号注册页（开通电离层 TIO 等服务的前置步骤） | data-portal | — | 🏷️ 官方 |
| [ESA-SWE-SSA](https://swe.ssa.esa.int/) | ESA 空间天气服务网络（SWE/SSA）门户：含穿越电离层电波链路等业务服务 | data-portal | — | 🏷️ 官方 |
| [ESA-TIO-Services](https://swe.ssa.esa.int/tio_services) | ESA 穿越电离层电波链路（TIO）服务总览：TEC、闪烁与扰动监测索引 | data-portal | — | 🏷️ 官方 |
| [NICT-WDC-Ionosphere-SpaceWeather](https://wdc.nict.go.jp/wdc-top/index.html) | 日本 NICT 世界数据中心（WDC-ISW）：电离层与空间天气长期数据门户 | data-portal | — | 🏷️ 官方 |
| [NOAA-NCEI-TEC-Archive](https://www.ncei.noaa.gov/products/space-weather/ionospheric-program/total-electron-content) | NOAA/NCEI US-TEC 与 GloTEC 国家归档说明与下载入口 | data-portal | — | 🏷️ 官方 |
| [NOAA-SWPC-GloTEC](https://www.spaceweather.gov/products/glotec) | NOAA/SWPC GloTEC：近实时全球 TEC 同化图（GNSS+COSMIC-2）业务产品页 | data-portal | — | 🏷️ 官方 |
| [NOAA-SWPC-GloTEC-Data](https://services.swpc.noaa.gov/products/glotec/) | NOAA/SWPC GloTEC 机器可读数据目录（GeoJSON / NetCDF） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IRTS_SDK](https://github.com/1acheng/IRTS_SDK)  
*🏷️ 个人社区*

语言：— · 许可：GPL-3.0 · 星标约：2 · 宿主：github

面向 ionosphere.cn 实时电离层服务的 C/C++ SDK，封装连接与 TEC 获取，便于导航终端做单频改正演示。输入为服务端连接参数与查询位置/时间；输出为实时 TEC/延迟相关量。局限：依赖云服务可用性与账号策略；不是离线开源模式本体。

#### [DLR-IMPC](https://impc.dlr.de/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

德国宇航中心（DLR）Neustrelitz 运营的业务电离层服务，明确为原 SWACI 的后继门户，并继续提供 SWACI 长期存档。产品包括欧洲/全球近实时 VTEC（约 15 分钟更新、时延通常 <5 分钟）、ROTI、梯度指数与 1 小时预报等，面向 GNSS 导航与空间天气用户。近实时下载需先注册账号；历史批量需邮件申请。适合作为欧洲区域 TEC 对照与扰动监测，不宜当作唯一全球精密 GIM 替代 IGS 最终 IONEX。

#### [DLR-IMPC-Products](https://impc.dlr.de/products)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IMPC 产品导航页，按 TEC、ROTI、梯度指数等分类链接到欧洲/全球近实时图及说明页。ASCII 矩阵与 PNG 为主要交付格式，新格式规划含 JSON。研究用途可与 ROB 欧洲 TEC、IGS GIM 交叉比对；业务引用请遵守 IMPC terms。

#### [ESA-SWE-Registration](https://swe.ssa.esa.int/registration)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

专用于创建 ESA 空间天气门户账号的注册表单。若目标是下载近实时/预报 TEC 图或使用 IONMON，需先完成本页注册再回主站登录授权。属于数据访问元条目，本身不托管观测文件。

#### [ESA-SWE-SSA](https://swe.ssa.esa.int/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲航天局空间态势感知空间天气段的统一门户，聚合地磁、太阳与电离层等多域服务。电离层相关能力集中在 Transionospheric Radio Link（TIO）与 IONMON 等应用。多数深度产品需注册后授权；公开仪表盘可先浏览当前状态。

#### [ESA-TIO-Services](https://swe.ssa.esa.int/tio_services)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

TIO 服务族目录页，汇总近实时/预报 TEC、闪烁图、扰动监测与电离层改正质量评估等入口。作为欧洲官方电离层业务导航页收录，便于从单一书签进入各子产品。

#### [NICT-WDC-Ionosphere-SpaceWeather](https://wdc.nict.go.jp/wdc-top/index.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

日本信息通信研究机构运营的世界数据中心，保存自 IGY 以来日本本土与南极测高仪等电离层资料及空间天气预警相关数据，并作为 WDS 成员对外分发。偏观测档案与空间天气，与 GNSS GIM 产品互补；做亚太区域电离层气候或闪烁背景研究时很有价值。

#### [NOAA-NCEI-TEC-Archive](https://www.ncei.noaa.gov/products/space-weather/ionospheric-program/total-electron-content)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国国家环境信息中心对 SWPC TEC 产品的权威归档页：US-TEC（约 2004–2023）与 GloTEC（约 2025 起）均可由此进入 cloud-access 下载，并附格式 README。历史事件复现与气候态统计用此页；近实时态势优先 SWPC GloTEC 产品页/services。

#### [NOAA-SWPC-GloTEC](https://www.spaceweather.gov/products/glotec)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国国家海洋大气局空间天气预测中心的全球 TEC 同化系统展示页。GloTEC 以 IRI-2016 为背景、Gauss-Markov 卡尔曼滤波同化地基 GNSS sTEC 与 COSMIC-2 掩星 sTEC，提供全球/北美/CONUS 图、相对 30 日中值异常与观测计数。面向 GNSS 延迟与空间天气态势感知；精密大地测量最终产品仍建议对照 IGS GIM。

#### [NOAA-SWPC-GloTEC-Data](https://services.swpc.noaa.gov/products/glotec/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

SWPC 官方 HTTP 产品树，提供 geojson_2d_urt 与 netcdf_2d_urt 等目录，便于自动化拉取近实时全球 TEC 网格。适合做业务监控看板或与自有 GNSS TEC 估计交叉验证；长期归档请改走 NCEI 空间天气门户。

## SBAS电离层

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EGNOS_SDK_Core](https://github.com/EpsilonRTD/EGNOS_SDK_Core) | EGNOS Android SDK 核心库（兼容 Android 5） | Java | 5 | 🏷️ 个人社区 |
| [EGNOSTools](https://github.com/DfAC/EGNOSTools) | EGNOS 处理支持工具（含 EMS 相关转换） | Python | 1 | 🏷️ 个人社区 |

### 详细说明

#### [EGNOS_SDK_Core](https://github.com/EpsilonRTD/EGNOS_SDK_Core)  
*🏷️ 个人社区*

语言：Java · 许可：— · 星标约：5 · 宿主：github

在移动端集成 EGNOS/SBAS 改正能力的 SDK 核心，便于理解终端如何消费 SBAS 电离层格网。输入为 SDK API 与 SBAS 数据通道；输出为改正后的定位相关量。局限：偏移动集成；不是开源 EMS 全链路解析教程。

#### [EGNOSTools](https://github.com/DfAC/EGNOSTools)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：1 · 宿主：github

辅助 EGNOS/SBAS 消息与 EMS 等格式处理的小工具集，便于课堂演示 MT18/MT26 电离层格网改正链路。输入为 EGNOS/EMS/RINEX 相关文件；输出为转换/解析结果。局限：仓库很小，需与规范文档对照使用。

## IRI/NeQuick

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [iri2016](https://github.com/space-physics/iri2016) | IRI-2016 的 Python/MATLAB 接口 | Fortran | 85 | 🏷️ 高校实验室 |
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | 国际参考电离层 IRI 的纯 Python 实现 | Python | 48 | 🏷️ 高校实验室 核心 |
| [NequickG](https://github.com/tpl2go/NequickG) | Galileo NeQuick-G 电离层模型 Python 实现 | Python | 45 | 🏷️ 个人社区 核心 |
| [iri2020](https://github.com/space-physics/iri2020) | iri2020：IRI-2020 Fortran/Python 可调用封装 | Fortran | 25 | 🏷️ 高校实验室 |
| [iri90](https://github.com/space-physics/iri90) | IRI-90 国际参考电离层的 Python 封装 | Python | 8 | 🏷️ 高校实验室 |
| [FIRI.jl](https://github.com/fgasdia/FaradayInternationalReferenceIonosphere.jl) | FIRI 法拉第国际参考电离层的 Julia 工具 | Julia | 5 | 🏷️ 高校实验室 |
| [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR) | ITU-R NeQuick 2 的 Python 封装 | Fortran | 4 | 🏷️ 个人社区 |
| [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC) | JRC NeQuickG C 实现镜像/整理 | C | 4 | 🏷️ 个人社区 |
| [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters) | IRI2020 参数相关资源 | MATLAB | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [iri2016](https://github.com/space-physics/iri2016)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：85 · 宿主：github

把 IRI-2016 Fortran 核心包一层现代语言接口，结果更接近社区惯用的官方模型。适合需要标准 IRI-2016 输出的论文。编译环境与 IRI-2020 升级需注意；纯 Python 偏好可选 PyIRI。

#### [PyIRI](https://github.com/victoriyaforsythe/PyIRI)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：MIT · 星标约：48 · 宿主：github

不绑 Fortran 也能跑 IRI 气候学电子密度/TEC 等，便于嵌进 Python 科研脚本。适合需要气候学背景场或与 GNSS TEC 对比的工作。实时扰动与闪烁物理不在 IRI 范围；要官方 IRI 数值一致性时可对照 iri2020 封装。

#### [NequickG](https://github.com/tpl2go/NequickG)  
*🏷️ 个人社区 核心*

语言：Python · 许可：— · 星标约：45 · 宿主：github

实现 Galileo 单频改正常用的 NeQuick-G，便于与 Galileo ICD/性能评估对照。适合 SBAS/单频仿真与教学。官方 JRC 参考实现之外的社区版，数值对齐要用标准算例核验；C 版可见 NeQuickJRC。

#### [iri2020](https://github.com/space-physics/iri2020)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：25 · 宿主：github

跟进 IRI-2020 的可调用封装，便于更新背景场或做版本差异试验。依赖 Fortran 构建；与 GNSS 实测 TEC 同化需另接观测链。

#### [iri90](https://github.com/space-physics/iri90)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：8 · 宿主：github

把经典 IRI-90 Fortran/数据流程包装成 Python，便于脚本化计算给定时刻与位置的电子密度等廓线，适合课堂演示与快速对比 GNSS TEC。输入一般为日期、地理坐标与高度网格；输出为模式密度/相关参量。局限：模型年代较早，精度与 IRI-2016/2020 有差距；依赖编译/数据文件配置，不替代业务 GIM。

#### [FIRI.jl](https://github.com/fgasdia/FaradayInternationalReferenceIonosphere.jl)  
*🏷️ 高校实验室*

语言：Julia · 许可：MIT · 星标约：5 · 宿主：github

面向 FIRI（Faraday International Reference Ionosphere）廓线的 Julia 读写与处理库，常用于低频/VLF 传播与低电离层研究。输入为 FIRI 剖面数据与查询坐标；输出为便于后续射线或吸收计算的电子密度廓线。局限：覆盖低电离层场景，不是 GNSS L 波段 TEC 改正主工具；需 Julia 环境。

#### [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：4 · 宿主：github

为 ITU-R NeQuick 2 Fortran 核心提供 Python 包装，便于在脚本里调用气候学电离层模型做链路预算或单频改正对比。与 Galileo 专用 NeQuick-G（NequickG 仓库）分属不同标准版本，数值对齐要用官方算例；亦可对照 PyIRI、iri2016，避免混用模型参数。

#### [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：4 · 宿主：github

整理 JRC NeQuickG 的 C 实现便于编译调用，偏工程嵌入。作者声明非 JRC 原开发托管，使用前核对版本与许可。需要 Python 胶水时可与 NequickG 对照。

#### [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：— · 宿主：github

整理 IRI2020 运行所需参数/资源，减少自己找系数文件的时间。宜与 iri2020 主仓库搭配，而非独立模型。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## NeQuick-G官方

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code) | NeQuick G：Galileo 单频电离层改正 | C | — | 🏷️ 官方 核心 |
| [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model) | ESA ESSR 登记的 NeQuick G 伽利略电离层改正实现（需注册） | C | — | 🏷️ 官方 |

### 详细说明

#### [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code)  
*🏷️ 官方 核心*

语言：C · 许可：EUPL-1.2 · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心提供的 NeQuick G 官方 C11 实现（含 JRC 库与测试驱动），面向 Galileo 单频用户电离层延迟改正。需注册并接受 EUPL 后下载加密包。与社区 GitHub 镜像相比应以本页为权威来源；气候态 NeQuick2 仍见 ICTP，二者算法与输入不同，集成前请对照 Galileo OS 电离层文档。

#### [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model)  
*🏷️ 官方*

语言：C · 许可：ESA Community License v2.4 · 星标约：— · 宿主：official_site

ESA 软件资源库中的 NeQuick G 条目，说明该实现按 Galileo 单频电离层改正算法文档适配，区别于 ITU 气候态 NeQuick Fortran。注册后获取，许可为 ESA Community License。日常下载更常走欧盟 GSC 页面；本页适合核对 ESA 侧登记信息与许可类型。

## 穿刺点IPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | 电离层穿刺点（IPP）计算 | C++ | — | 🏷️ 个人社区 ★ |

### 详细说明

#### [Get_IPP](https://github.com/Chenjiajun01/Get_IPP)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：— · 宿主：github

根据测站与卫星几何求电离层穿刺点，GIM/层析前处理常用。适合教学与自写映射函数前的几何模块。单薄脚本型项目，坐标框架与壳层高度约定要与主流程一致。

## 测高仪/同化

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GIRO-portal](https://giro.uml.edu/) | GIRO 全球电离层测高仪观测网门户（IRTAM 等数据入口） | — | — | 🏷️ 官方 |

### 详细说明

#### [GIRO-portal](https://giro.uml.edu/)  
*🏷️ 官方*

语言：— · 许可：— · 星标约：— · 宿主：official_site

UML 维护的 GIRO 门户，通向测高仪数据与 IRTAM 等实时同化产品相关入口。适合把测高仪峰值参数与 GNSS TEC/IRI 对比。主要是数据与服务门户，不是 GNSS 解算库；下载具体软件前在站内核对许可与程序页。

## TEC预报/ML

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tec_prediction-ONERA](https://github.com/aboulch/tec_prediction) | ONERA ConvLSTM/U-Net 全球 TEC 图预报经典开源实现（Boulch 2018） | Python | 19 | 🏷️ 高校实验室 |
| [Global-TEC-forecasting-DL](https://github.com/Laboratorio-Computacion-Cientifica/Global-TEC-forecasting-for-space-weather-application-based-on-deep-learning-techniques) | 全球 TEC 24 小时预报：LSTM/GRU/CNN 全流程（含 DVC） | Python | 6 | 🏷️ 高校实验室 |
| [IonCast-Heliolab2025](https://github.com/FrontierDevelopmentLab/2025-HL-Ionosphere) | NASA FDL Heliolab 2025 IonCast：ConvLSTM/GNN/SFNO 电离层预报实验代码 | Python | 5 | 🏷️ 高校实验室 |
| [ionopy](https://github.com/spaceml-org/ionopy) | Time-Fusion Transformer 数据驱动电离层预报（SpaceML） | Python | 4 | 🏷️ 高校实验室 |
| [IonoBench](https://github.com/Mert-chan/IonoBench) | 全球电离层时空预报模型基准测试框架 | Jupyter Notebook | 2 | 🏷️ 高校实验室 |
| [ionospheric-tec-forecasting-IISC](https://github.com/codewithavra/ionospheric-tec-forecasting) | IISC Bangalore 单站 TEC 日前预报（Seq2Seq LSTM 与 CNN-Transformer） | Jupyter Notebook | 0 | 🏷️ 高校实验室 |
| [SpatioTECformer](https://github.com/research1011/SpatioTECformer) | 多尺度 CNN + Transformer 的 TEC 时空预报模型（PyTorch） | Python | 0 | 🏷️ 个人社区 |

### 详细说明

#### [tec_prediction-ONERA](https://github.com/aboulch/tec_prediction)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 (research); commercial contact ONERA · 星标约：19 · 宿主：github

卷积循环网络做电离层活动/TEC 图预报的早期公开代码，后被多篇 DeepTEC 类工作引用。研究非商业用途按仓库说明为 GPLv3，商业需联系 ONERA。适合当 ML TEC 基线；年代较早（约 2018），依赖与数据管道需自行适配现行 IONEX/GIM。

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

语言：Python · 许可：see upstream README · 星标约：4 · 宿主：github

SpaceML 维护的电离层预报代码与笔记本，强调时间融合 Transformer，被 IonCast/Heliolab 仓库引用为较新实现。适合跟深度学习 TEC/电离层序列模型。许可证未在 GitHub 标 SPDX，使用前请读仓库说明；数据与训练配置需自备。

#### [IonoBench](https://github.com/Mert-chan/IonoBench)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：MIT · 星标约：2 · 宿主：github

提供对比多种时空深度学习/统计模型预报全球电离层的基准流程，便于复现论文实验。输入为历史 TEC/GIM 类数据与模型配置；输出为预报评分与对比。局限：侧重 ML 基准而非物理模式；数据准备与算力要求不低。

#### [ionospheric-tec-forecasting-IISC](https://github.com/codewithavra/ionospheric-tec-forecasting)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：MIT · 星标约：0 · 宿主：github

针对 IISC 站分钟级 TEC，对比序列到序列 LSTM 与 CNN+窗口 Transformer，并把预报 TEC 换成 L1/L2/L5 电离层延迟。教学与单站实验很直观，还带 RoTI 相关分析笔记本。站点/时段特定，不是全球 GIM 预报器；体量含数据集，克隆较大。

#### [SpatioTECformer](https://github.com/research1011/SpatioTECformer)  
*🏷️ 个人社区*

语言：Python · 许可：see upstream README · 星标约：0 · 宿主：github

把多尺度卷积、自适应融合与 Transformer 编码器拼成 71×73 网格 TEC 预报流水线，模块拆成 model/enhanced_cnn 等文件，代码量小但完整可跑。适合读论文式复现。未标 SPDX 许可证；训练依赖作者 HDF5 特征文件，需自备或按 README 路径改。

## 闪烁/ROTI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | 多星座 ROTI/AATR/STEC/VTEC 监测 | C++ | 37 | 🏷️ 个人社区 ★ |
| [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator) | CU Boulder Sense Lab：GNSS 频段相位/幅度闪烁仿真 | MATLAB | 25 | 🏷️ 高校实验室 |
| [OASIS](https://github.com/giorgiopicanco/OASIS) | 从 RINEX 计算 ROTI/ΔTEC/SIDX 等扰动指标 | Python | 16 | 🏷️ 个人社区 核心 |
| [scintill-ai](https://github.com/viventriglia/scintill-ai) | 用机器学习做电离层闪烁相关分析的研究项目 | Shell | 8 | 🏷️ 个人社区 |
| [TITIPy](https://github.com/pignalberi/TITIPy) | Swarm 顶部电离层 RODI/ROTI/ROTEI（Python） | Python | 8 | 🏷️ 高校实验室 |
| [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP) | 电离层闪烁成像及其对 PDOP 影响的研究代码 | MATLAB | 5 | 🏷️ 个人社区 |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据清洗与指标计算工具 | Python | 3 | 🏷️ 个人社区 ★ |
| [OASIS-ohm1122](https://github.com/ohm1122/OASIS) | OASIS 用户星标副本/相关仓库 | — | — | 🏷️ 个人社区 ★ |
| [Okoh-MATLAB-ROT-ROTI](https://doi.org/10.5281/zenodo.7913105) | Daniel Okoh：由 TEC 序列计算 30 s ROT 与 5 min ROTI 的 MATLAB 函数 | MATLAB | — | 🏷️ 高校实验室 |

### 详细说明

#### [IonoMoni](https://github.com/qiliu2025/IonoMoni)  
*🏷️ 个人社区 ★*

语言：C++ · 许可：— · 星标约：37 · 宿主：github

C++ 实现多星座电离层监测指标（ROTI、AATR、STEC/VTEC），偏近实时监测。适合需要编译型性能的台站软件。文档与许可信息需自行确认；科研绘图可再接 Python 可视化。

#### [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：25 · 宿主：github

科罗拉多大学 Boulder Satellite Navigation and Sensing Lab（cu-sense-lab）开源的 GNSS 闪烁仿真器，生成相位与幅度闪烁序列，用于接收机跟踪环与完好性试验。适合算法仿真，不是实测 ROTI 产品生成器；参数需对照文献与实测统计。同实验室还有简化两参数版 gnss-scintillation-simulator_2-param。

#### [OASIS](https://github.com/giorgiopicanco/OASIS)  
*🏷️ 个人社区 核心*

语言：Python · 许可：— · 星标约：16 · 宿主：github

Open-Access System for Ionospheric Studies：从 GNSS 观测算 ROTI、ΔTEC、SIDX 等，做扰动与闪烁相关监测。适合空间天气事件个例与台站网指标产品。高采样率接收机原始闪烁指数（S4/σφ）仍需专用接收机或仿真器。

#### [scintill-ai](https://github.com/viventriglia/scintill-ai)  
*🏷️ 个人社区*

语言：Shell · 许可：MIT · 星标约：8 · 宿主：github

探索用机器学习刻画或预测电离层闪烁相关现象的研究型仓库，偏数据驱动实验原型。适合空间天气与机器学习交叉课题入门。闪烁事件稀缺、标签噪声与跨站点泛化是主要风险；报告结果时应保留 S4、σφ、ROTI 等物理基线对照，避免只展示神经网络分数而缺少可解释性。

#### [TITIPy](https://github.com/pignalberi/TITIPy)  
*🏷️ 高校实验室*

语言：Python · 许可：CC-BY-NC-SA-3.0 · 星标约：8 · 宿主：github

INGV/ESA INTENS 的 Swarm 顶部电离层湍流指数工具（Python）：从 Langmuir 探针与 POD/TEC 产品算 RODI/ROTI/ROTEI 并制图，含下载与 CDF 读取。CC BY-NC-SA 3.0，需自备 Swarm 账号；面向顶部电离层闪烁研究，不是地基双频 TEC 解算器。

#### [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：5 · 宿主：github

研究电离层闪烁空间成像及其对定位几何（PDOP）影响的代码，把空间天气扰动与导航可用性联系起来。适合闪烁—PNT 耦合与完好性相关课题。不是业务级闪烁监测网软件；输入场与网格假设应按论文复现，并可与 OASIS、ROTI 类工具对照物理指标定义。

#### [gnssutils](https://github.com/ljlamarche/gnssutils)  
*🏷️ 个人社区 ★*

语言：Python · 许可：GPL-3.0 · 星标约：3 · 宿主：github

面向地基 GNSS 闪烁接收机数据流的实用函数集，便于清洗与指标计算。适合已有 ISMR/闪烁观测的课题组。GPL 许可需留意；不替代通用 TEC/GIM 或业务闪烁预警系统。

#### [OASIS-ohm1122](https://github.com/ohm1122/OASIS)  
*🏷️ 个人社区 ★*

语言：— · 许可：— · 星标约：— · 宿主：github

用户星标的 OASIS 相关仓库，实际算法与数据接口以 giorgiopicanco/OASIS 上游为准。引用论文时请核对 canonical URL。

#### [Okoh-MATLAB-ROT-ROTI](https://doi.org/10.5281/zenodo.7913105)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

配套 Zenodo 软件存档（concept DOI 10.5281/zenodo.7913105），提供 rot30s_mean.m 与 roti5m.m，从 GNSS/其他仪器 TEC 时间序列计算 30 秒 TEC 变化率与 5 分钟 ROTI。CC-BY-4.0，体积小、接口清晰，便于嵌入已有 TEC 流水线做不规则性监测。需自备定标后的 TEC 输入。

## GIM/球谐映射

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现（维护者自有，此处不展开） | MATLAB | 104 | 🏷️ 个人社区 🚩 核心 |
| [M_GIM-zcytju](https://github.com/zcytju/M_GIM) | zcytju：多系统全球/区域电离层 GIM 建模 MATLAB 软件 | MATLAB | 23 | 🏷️ 个人社区 ★ |
| [mosgim2](https://github.com/PadArt/mosgim2) | 相位差法构建 GNSS 全球电离层图 | Python | 17 | 🏷️ 个人社区 ★ |
| [mosgim](https://github.com/gnss-lab/mosgim) | Padokhin 早期 MosGIM GIM 技术实现 | Python | 6 | 🏷️ 高校实验室 |
| [real-time-ionospheric-maps-Kalman](https://github.com/AlexandraKoulouri/real-time-ionospheric-maps-using-Kalman) | 南美区域实时电离层图（集合卡尔曼）MATLAB 代码 | MATLAB | 3 | 🏷️ 高校实验室 |
| [m_gim-PANXIONG](https://github.com/PANXIONG-CN/m_gim) | PANXIONG：小体量 MATLAB GIM 脚本草稿 | MATLAB | 1 | 🏷️ 个人社区 ★ |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS.IonosphereMaps：Java 电离层图工具 | Java | — | 🏷️ 个人社区 ★ |
| [Zenodo-VTEC-map-generation-SBAS](https://doi.org/10.5281/zenodo.10058636) | Zenodo：支持星基导航误差模型的 VTEC 图生成补充材料 | — | 0 | 🏷️ 高校实验室 |

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

#### [mosgim](https://github.com/gnss-lab/mosgim)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

MosGIM 早期公开版本，便于追溯相位差 GIM 的原始流程。适合读论文后对照算法步骤。维护与功能完整度不如 mosgim2；新项目建议优先 mosgim2，本仓库作历史对照即可。

#### [real-time-ionospheric-maps-Kalman](https://github.com/AlexandraKoulouri/real-time-ionospheric-maps-using-Kalman)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：3 · 宿主：github

用 Ensemble Kalman Filter 重建南美区域电离层图，展示实时/近实时制图思路。输入为区域 GNSS TEC 相关观测量；输出为时序电离层图。局限：区域与方法绑定；工程化 GIM/IONEX 生产需额外封装。

#### [m_gim-PANXIONG](https://github.com/PANXIONG-CN/m_gim)  
*🏷️ 个人社区 ★*

语言：MATLAB · 许可：— · 星标约：1 · 宿主：github

个人小仓 MATLAB GIM 相关脚本，适合课程作业或方法草稿。功能面窄，不宜单独承担业务化建图；更完整的多系统建模见 zcytju/M_GIM。

#### [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps)  
*🏷️ 个人社区 ★*

语言：Java · 许可：Apache-2.0 · 星标约：— · 宿主：github

gurkanguldas 的 Java 仓库，面向 GNSS 电离层图处理与展示。适合 JVM 技术栈快速查看 TEC 图；算法深度与产品化程度以 README 为准，科研级 GIM 仍建议对照 IGS/CODE 流程。

#### [Zenodo-VTEC-map-generation-SBAS](https://doi.org/10.5281/zenodo.10058636)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：0 · 宿主：zenodo

Tampere University 发布的 VTEC 图生成代码/数据补充（VTEC_FORZENODO.zip），用于支撑星基导航电离层误差模型研究与复现。输入见压缩包说明；输出为 VTEC 图相关结果。局限：以论文复现为目的，接口与文档完整度因包而异；使用前请核对许可与引用。

## HF射线追踪

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyLap](https://github.com/HamSCI/PyLap) | HamSCI 对 PHaRLAP 的开源 Python 接口（生成电离层与射线绘图） | Python | 14 | 🏷️ 高校实验室 |
| [PyRayHF](https://github.com/victoriyaforsythe/PyRayHF) | 纯 Python 电离层 HF 射线追踪（虚高与二维射线，对接 PyIRI 生态） | Python | 10 | 🏷️ 高校实验室 |
| [hfpytrace](https://github.com/shibaji7/trace) | HF 射线追踪库 hfpytrace（PHaRLAP 与其它色散关系，含 PyIRI 示例） | Python | 1 | 🏷️ 高校实验室 |
| [PHaRLAP](https://www.dst.defence.gov.au/our-technologies/pharlap-provision-high-frequency-raytracing-laboratory-propagation-studies) | 澳大利亚 DSTG HF 电离层射线追踪 Matlab 工具箱（免费申请，不可再分发） | Fortran/MATLAB | — | 🏷️ 官方 |

### 详细说明

#### [PyLap](https://github.com/HamSCI/PyLap)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：14 · 宿主：github

用 Python/C 调用 PHaRLAP Fortran 引擎，摆脱 Matlab 授权门槛，保留建 IRI 电离层、射线追踪与绘图等核心流程。业余与科研 HF 传播实验友好。安装目前偏 Ubuntu/x86，且必须先向 DSTG 申请 PHaRLAP 本体与 Intel Fortran 运行库；本身不是可独立运行的完整射线引擎。

#### [PyRayHF](https://github.com/victoriyaforsythe/PyRayHF)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：10 · 宿主：github

Victoriya Forsythe 等发布的 HF 射线工具，从电子密度剖面计算虚高与二维射线路径，文档在 Read the Docs，与同作者 PyIRI/PyIRTAM 生态衔接自然。适合教学与轻量传播实验。能力相对 PHaRLAP 全磁离子 3D NRT 更聚焦；复杂回波与三维磁离子场景仍可能需要更重的引擎。

#### [hfpytrace](https://github.com/shibaji7/trace)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

开源 HF 射线追踪包，文档与示例演示 IRI 笛卡尔/球坐标斜向射线，密度后端可接 PyIRI。适合想在 Python 里做传播几何、又不愿只绑 Matlab mex 的人。仓库内仍可见 pharlap_lib 相关痕迹，授权与依赖请读上游 LICENSE/文档；与 HamSCI PyLap 路线不同，选型前先确认你是否已有 DSTG PHaRLAP。

#### [PHaRLAP](https://www.dst.defence.gov.au/our-technologies/pharlap-provision-high-frequency-raytracing-laboratory-propagation-studies)  
*🏷️ 官方*

语言：Fortran/MATLAB · 许可：DSTG request freeware (no redistribution) · 星标约：— · 宿主：official_site

提供 2D/全磁离子 3D 数值射线追踪与解析追踪，可挂 IRI/IGRF 或用户网格。HF 传播与回波几何研究里事实上的常用引擎，Fortran 核心经 mex 进 Matlab。许可为 DSTG 科学发放：个人申请、禁止再分发。若缺 Matlab，可看 HamSCI PyLap 开源接口，但仍需另行申请 PHaRLAP 本体。

## TEC计算

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ionotec](https://github.com/sylvathle/ionotec) | 从 RINEX 计算总电子含量的 Python 库 | Python | 6 | 🏷️ 个人社区 |

### 详细说明

#### [ionotec](https://github.com/sylvathle/ionotec)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

面向 RINEX 观测的 TEC 计算库（原 pytec 更名/迁移至 ionotec），补齐“读观测→几何无关组合→TEC”的轻量路径。适合快速脚本化实验。功能面小于 PyTECGg/tec-suite 一类完整标定流水线；多星座 DCB/硬件延迟处理需自行核对。

## IRI官方模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IRI-2020-package](https://irimodel.org/IRI-2020/) | IRI-2020 官方目录：Fortran 源码、系数、许可证与 zip/tar 包 | Fortran | — | 🏷️ 官方 |
| [IRI-Fortran](https://irimodel.org/) | IRI：国际参考电离层官方 Fortran | Fortran | — | 🏷️ 官方 核心 |

### 详细说明

#### [IRI-2020-package](https://irimodel.org/IRI-2020/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

irimodel.org 上 IRI-2020 的文件目录，可直接获取 00_iri.zip/tar、许可证与各 .for 系数文件。便于固定版本复现实验与回归测试。新版本（如 IRI-2026）请回主站查看；Python 封装见社区 iri2020/PyIRI，官方数值仍以此目录为准。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [IRI-Fortran](https://irimodel.org/)  
*🏷️ 官方 核心*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

国际参考电离层 IRI 的官方 Fortran 发行入口，由 COSPAR/URSI 工作组维护，提供电子密度、温度、离子成分与 vTEC 等气候态输出。可直接下载 IRI-2020/2026 压缩包与指数文件。适合作为标准对照模型写入论文复现实验；实时闪烁或扰动过程需另接观测或同化产品，不宜单独当作业务电离层改正引擎。

## 闪烁数据

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ismr_downloader](https://github.com/GEGE-UNESP/ismr_downloader) | ISMR 闪烁监测数据下载器 | Python | 1 | 🏷️ 高校实验室 |

### 详细说明

#### [ismr_downloader](https://github.com/GEGE-UNESP/ismr_downloader)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

从 ISMR Query Tool API 拉取 GNSS/ISMR 闪烁监测数据的命令行下载器。适合批量建闪烁样本库。依赖上游 API 可用性与账号策略；本地下载后需自行做质控。

## 传播模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx) | ITU-R 电离层/对流层电波传播软件与验证数据入口 | various | — | 🏷️ 官方 |

### 详细说明

#### [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx)  
*🏷️ 官方*

语言：various · 许可：ITU terms · 星标约：— · 宿主：official_site

国际电联无线电通信部门汇总的电离层与对流层传播预测软件、数据与验证示例入口，涵盖推荐方法相关数字产品。许可与获取按 ITU 条款办理。适合传播与链路预算研究；GNSS 精密定位仍多用 IRI、NeQuick、VMF 等专用实现。使用前请核验上游页面与许可条款。

## NeQuick官方

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code) | ICTP 官方 NeQuick 2 电离层电子密度模型 Fortran 源码申请页 | Fortran | — | 🏷️ 官方 核心 |

### 详细说明

#### [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code)  
*🏷️ 官方 核心*

语言：Fortran · 许可：scientific distribution (request) · 星标约：— · 宿主：official_site

阿卜杜斯·萨拉姆国际理论物理中心 T/ICT4D 发布的 NeQuick 2 气候态电子密度模型，含 ITU 系数与太阳活动/modip 文件。面向穿电离层传播与 TEC 积分研究。源码需向维护者邮件申请；若做 Galileo 单频接收机改正，请改用 GSC 的 NeQuick G 官方实现以免版本混淆。

## GNSS掩星处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ROM-SAF-ROPP](https://rom-saf.eumetsat.int/ropp/) | ROM SAF 无线电掩星处理包 ROPP（含电离层改正与 Abel 反演模块，注册获取） | Fortran | — | 🏷️ 官方 |

### 详细说明

#### [ROM-SAF-ROPP](https://rom-saf.eumetsat.int/ropp/)  
*🏷️ 官方*

语言：Fortran · 许可：ROM SAF scientific (registration) · 星标约：— · 宿主：official_site

EUMETSAT ROM SAF 维护的标准掩星处理套件，ropp_pp 等模块覆盖 excess phase→弯曲角、电离层改正与反演链路，是业务/科研里常见的开源可编译 Fortran 工具链。源码需登录 ROM SAF 账号下载（当前公开页指向 ROPP-12.0）。适合认真做 RO 预处理的人；只想快速读 COSMIC NetCDF 剖面，不必一上来就装整包。

## 物理模式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SAMI3-3.22-Zenodo](https://doi.org/10.5281/zenodo.7895858) | SAMI3 3.22：NRL 电离层/等离子体层三维模式 Fortran 源码（Zenodo 软件存档） | Fortran | — | 🏷️ 高校实验室 |

### 详细说明

#### [SAMI3-3.22-Zenodo](https://doi.org/10.5281/zenodo.7895858)  
*🏷️ 高校实验室*

语言：Fortran · 许可：CC-BY-4.0 · 星标约：— · 宿主：other

Joe Huba（Syntek/NRL）在 Zenodo 以 software 类型存档的 SAMI3-3.22 官方源码包（concept DOI 10.5281/zenodo.7895858），附 sami3-3.22.tgz（约 39 MB）与用户手册。用于全球电离层–等离子体层物理仿真，常与 GNSS TEC/掩星对比。许可 CC-BY-4.0。目录中另有 GitHub 镜像与 CCMC 门户，本条收录可直接下载的 Zenodo 软件存档本身。concept/record 页 HTTP 200。

## SWARM/LEO TEC

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [viresclient](https://github.com/ESA-VirES/VirES-Python-Client) | ESA VirES Python 客户端：Swarm Langmuir/TEC 等产品转 xarray | Python | 23 | 🏷️ 官方 |

### 详细说明

#### [viresclient](https://github.com/ESA-VirES/VirES-Python-Client)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：23 · 宿主：github

官方推荐的 Swarm（及 Aeolus）数据访问库，可按需拉取 EFI Langmuir 探针、TECxTMS_2F 绝对/相对 TEC、以及 CHAMP/GRACE 等扩展 TEC/Ne 产品并载入 pandas/xarray。做 LEO POD 衍生 TEC 与就地电子密度对照时几乎是默认入口。需 VirES 账号；本身不做反演，只负责服务端点与本地装载。

## 数据接口

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [madrigalWeb](https://github.com/MITHaystack/madrigalWeb) | OpenMadrigal/CEDAR Python 数据客户端 | Python | 4 | 🏷️ 高校实验室 |

### 详细说明

#### [madrigalWeb](https://github.com/MITHaystack/madrigalWeb)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

访问全球 Madrigal 站点（含 CEDAR）的官方 Python 客户端，可检索/下载非相干散射雷达、GNSS TEC 等空间天气与电离层归档。MIT。适合批量脚本拉取；需遵守各站点数据政策，部分实验需注册。配套门户见 OpenMadrigal。

## TID/扰动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [DARNtids](https://github.com/w2naf/DARNtids) | SuperDARN TID 行进扰动检测工具 | Python | 4 | 🏷️ 高校实验室 |

### 详细说明

#### [DARNtids](https://github.com/w2naf/DARNtids)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：4 · 宿主：github

面向 SuperDARN 雷达数据的 TID（Traveling Ionospheric Disturbance）检测与分析代码，GPL-3.0。适合将高频雷达观测与 GNSS TEC/TID 研究对照。依赖 SuperDARN 数据环境与雷达物理背景；不是 GNSS RINEX 处理链。

## TEC/层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Heki-GNSS-TEC-Software](https://www.ep.sci.hokudai.ac.jp/~heki/software.htm) | Heki 公开 Fortran：L4/STEC 与电离层层析 | Fortran | — | 🏷️ 高校实验室 |

### 详细说明

#### [Heki-GNSS-TEC-Software](https://www.ep.sci.hokudai.ac.jp/~heki/software.htm)  
*🏷️ 高校实验室*

语言：Fortran · 许可：academic research (as-is) · 星标约：— · 宿主：official_site

日置幸一郎课题组公开的 Fortran 工具页：rdrnx/rdrnx3 从 RINEX 生成几何无关 L4、rdeph 算卫星位置、tomo 做三维电子密度层析，并含 CID 仿真与 GEONET 荷载示例。学术研究常用。许可为研究用公开源码（非 SPDX）；社区镜像见 yu-0124/GNSS-TEC_tools。编译与坐标系约定需对照说明书。
