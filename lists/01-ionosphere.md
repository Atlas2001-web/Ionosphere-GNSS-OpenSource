# 电离层 / Ionosphere
> 共 **37** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

## GIM/球谐映射

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现 | MATLAB | 104 | 🚩 自有 · 核心 |
| [mosgim2](https://github.com/PadArt/mosgim2) | 相位差法构建 GNSS 全球电离层图 | Python | 17 | ★ Star |
| [mosgim](https://github.com/gnss-lab/mosgim) | Padokhin 早期 MosGIM GIM 技术实现 | Python | 6 |  |
| [m_gim](https://github.com/PANXIONG-CN/m_gim) | MATLAB 侧 GIM 相关脚本 | MATLAB | 1 | ★ Star |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS 电离层图生成与处理 | — | — | ★ Star |
| [M_GIM](https://github.com/zcytju/M_GIM) | 电离层 GIM 相关 MATLAB/工具实现 | — | — | ★ Star |

### 详细说明

#### [SH-GIM](https://github.com/Atlas2001-web/SH-GIM)  
*🚩 自有 · 核心*

语言：MATLAB · 许可：MIT · 星标约：104

用球谐系数把 GNSS 斜路径 TEC 拟合成全球电离层图，输出可与 IONEX/IGS GIM 对照。适合做 GIM 方法复现、球谐阶次试验和教学演示。代码体量集中、依赖 MATLAB，规模化批处理与多星座 DCB 自洽估计仍需自补；与 MosGIM2、PRIDE 电离层产品等并列阅读时，重点看球谐约束与穿刺点建模差异。

#### [mosgim2](https://github.com/PadArt/mosgim2)  
*★ Star*

语言：Python · 许可：MIT · 星标约：17

MosGIM 系第二代实现，侧重相位差思路从 GNSS 观测建 GIM，Python 栈便于接到现有数据流水线。适合研究组快速试算区域/全球 TEC 图。文档与工程化程度不如商业或大机构产品；球谐/网格参数需自行调，和 SH-GIM、gnss-tec 搭配可做方法对比。

#### [mosgim](https://github.com/gnss-lab/mosgim)

语言：Python · 许可：MIT · 星标约：6

MosGIM 早期公开版本，便于追溯相位差 GIM 的原始流程。适合读论文后对照算法步骤。维护与功能完整度不如 mosgim2；新项目建议优先 mosgim2，本仓库作历史对照即可。

#### [m_gim](https://github.com/PANXIONG-CN/m_gim)  
*★ Star*

语言：MATLAB · 星标约：1

小体量 MATLAB GIM 相关代码，适合作为课程作业或方法草稿。功能覆盖面有限，不宜单独承担业务化建图。

#### [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps)  
*★ Star*

侧重从 GNSS 观测生成与处理电离层图，适合做图件可视化或区域 TEC 展示。工程完整度与多星座支持需实测；若目标是可发表级全球 GIM，应同时参考 SH-GIM/MosGIM2 与 IGS 产品规范。

#### [M_GIM](https://github.com/zcytju/M_GIM)  
*★ Star*

面向 GIM 建模的 MATLAB 侧工具集合，适合已有 MATLAB 电离层工作流的人快速试用。公开说明偏少，需自行核验输入输出格式是否符合 IONEX/球谐习惯；可与 SH-GIM、M_GIM 变体对照使用。


## TEC估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | 由 RINEX 载波/伪距重建斜路径 TEC | Python | 54 | 核心 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python+Rust） | Python | 29 | 🔀 Fork · ★ Star · 核心 |
| [PyGPS](https://github.com/gregstarr/PyGPS) | 读 RINEX、算 TEC/卫星位置与偏差的工具箱 | Python | 47 |  |
| [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB) | MATLAB 双频 RINEX 2.11 TEC 计算 | MATLAB | 33 |  |
| [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | 由 GPS 数据估计电离层 TEC 与旋转量 RM | Python | 26 |  |
| [tec-suite](https://github.com/gnss-lab/tec-suite) | SIMuRG 团队 TEC 重建套件 | Python | 23 |  |
| [pygnss-tec](https://github.com/eureka-0/pygnss-tec) | RINEX 读取与 TEC 计算（Rust 加速） | Python | 16 |  |
| [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation) | 单/双频方法估计电离层延迟梯度 | MATLAB | 6 |  |
| [vtec](https://github.com/mfkiwl/vtec) | 垂直 TEC（VTEC）计算相关工具 | — | — | ★ Star |

### 详细说明

#### [gnss-tec](https://github.com/gnss-lab/gnss-tec)  
*核心*

语言：Python · 许可：MIT · 星标约：54

SIMuRG/gnss-lab 系经典 STEC 重建库，输入 RINEX 相位与伪距，输出斜路径 TEC，MIT 许可友好。适合论文复现与批处理建站网 TEC。GIM 成图、闪烁指数需另接 mosgim/OASIS 等；DCB 处理策略要按数据源核对。

#### [PyTECGg](https://github.com/viventriglia/PyTECGg)  
*🔀 Fork · ★ Star · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：29

从 RINEX 做多星座 TEC 重建与接收机/卫星偏差相关校准，Rust 核心加快批处理。适合需要可编程 TEC 流水线、又想兼顾性能的研究组。Atlas2001-web 已 fork。GPL 许可需注意与闭源流程衔接；与 gnss-tec、tec-suite 比，更偏「可嵌入 Python 生态」。

#### [PyGPS](https://github.com/gregstarr/PyGPS)

语言：Python · 许可：AGPL-3.0 · 星标约：47

把读 RINEX、存 HDF5、算 TEC、卫星位置与接收机/卫星偏差串在一起，偏研究原型。适合快速探索。AGPL 较严；长期维护与测试覆盖不如专门 TEC 库，关键步骤建议交叉验证。

#### [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB)

语言：MATLAB · 星标约：33

基于双频接收机观测在 MATLAB 里算 TEC，输入偏 RINEX 2.11/GPS，教学友好。适合本科实验与快速验证。多星座、RINEX 3/4 与现代化 DCB 产品支持有限；科研产线建议再接 PyTECGg 等。

#### [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere)

语言：Python · 星标约：26

面向射电天文/地空链路，从 GPS 接收机数据估 TEC 与法拉第旋转相关量。适合需要 TEC+RM 联合的场景。通用 GNSS 多星座精密 TEC 流水线不是其主场；协议与输入格式需按仓库说明准备。

#### [tec-suite](https://github.com/gnss-lab/tec-suite)

语言：Python · 许可：GPL-3.0 · 星标约：23

比单库 gnss-tec 更偏「套件」形态，把重建流程串起来便于站点网作业。适合已在用 SIMuRG 工具链的人。GPL 约束与文档深度因版本而异；轻量嵌入可优先 gnss-tec。

#### [pygnss-tec](https://github.com/eureka-0/pygnss-tec)

语言：Python · 许可：MIT · 星标约：16

Python 包读 RINEX 并算 TEC，关键路径用 Rust 加速，和 PyTECGg 同属「Py+加速核」路线。适合中等规模批处理。社区体量小于 gnss-tec；算法假设（映射、DCB）使用前要读文档核对。

#### [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation)

语言：MATLAB · 星标约：6

从 RINEX 估计电离层延迟梯度，服务于 GBAS/局域增强等对空间梯度敏感的应用。适合机场周遭或短基线梯度研究。全球 GIM 不是目标；与 ROTI/闪烁监测可互补。

#### [vtec](https://github.com/mfkiwl/vtec)  
*★ Star*

围绕 VTEC 换算与相关计算的小工具，适合把 STEC 投影到垂直方向做图或预报输入。功能边界较窄，完整双频重建与偏差估计需配合专业 TEC 库。


## IRI/NeQuick

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | 国际参考电离层 IRI 的纯 Python 实现 | Python | 48 | 核心 |
| [NequickG](https://github.com/tpl2go/NequickG) | Galileo NeQuick-G 电离层模型 Python 实现 | Python | 45 | 核心 |
| [iri2016](https://github.com/space-physics/iri2016) | IRI-2016 的 Python/MATLAB 接口 | Fortran | 85 |  |
| [iri2020](https://github.com/space-physics/iri2020) | IRI-2020 气候模型封装 | Fortran | 25 |  |
| [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC) | JRC NeQuickG C 实现镜像/整理 | C | 4 |  |
| [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters) | IRI2020 参数相关资源 | — | — | ★ Star |

### 详细说明

#### [PyIRI](https://github.com/victoriyaforsythe/PyIRI)  
*核心*

语言：Python · 许可：MIT · 星标约：48

不绑 Fortran 也能跑 IRI 气候学电子密度/TEC 等，便于嵌进 Python 科研脚本。适合需要气候学背景场或与 GNSS TEC 对比的工作。实时扰动与闪烁物理不在 IRI 范围；要官方 IRI 数值一致性时可对照 iri2020 封装。

#### [NequickG](https://github.com/tpl2go/NequickG)  
*核心*

语言：Python · 星标约：45

实现 Galileo 单频改正常用的 NeQuick-G，便于与 Galileo ICD/性能评估对照。适合 SBAS/单频仿真与教学。官方 JRC 参考实现之外的社区版，数值对齐要用标准算例核验；C 版可见 NeQuickJRC。

#### [iri2016](https://github.com/space-physics/iri2016)

语言：Fortran · 许可：MIT · 星标约：85

把 IRI-2016 Fortran 核心包一层现代语言接口，结果更接近社区惯用的官方模型。适合需要标准 IRI-2016 输出的论文。编译环境与 IRI-2020 升级需注意；纯 Python 偏好可选 PyIRI。

#### [iri2020](https://github.com/space-physics/iri2020)

语言：Fortran · 许可：MIT · 星标约：25

IRI-2020 的可调用封装，跟进较新气候学版本。适合更新背景场或做版本差异试验。依赖 Fortran 构建；与 GNSS 实测 TEC 同化需另接。

#### [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC)

语言：C · 星标约：4

整理 JRC NeQuickG 的 C 实现便于编译调用，偏工程嵌入。作者声明非 JRC 原开发托管，使用前核对版本与许可。需要 Python 胶水时可与 NequickG 对照。

#### [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters)  
*★ Star*

整理 IRI2020 运行所需参数/资源，减少自己找系数文件的时间。宜与 iri2020 主仓库搭配，而非独立模型。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 闪烁/ROTI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [OASIS](https://github.com/giorgiopicanco/OASIS) | 从 RINEX 计算 ROTI/ΔTEC/SIDX 等扰动指标 | Python | 16 | 核心 |
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | 多星座 ROTI/AATR/STEC/VTEC 监测 | C++ | 37 | ★ Star |
| [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator) | GNSS 频段相位/幅度闪烁仿真 | MATLAB | 25 |  |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据处理工具 | Python | 3 | ★ Star |
| [OASIS-ohm1122](https://github.com/ohm1122/OASIS) | OASIS 用户星标副本/相关仓库 | — | — | ★ Star |

### 详细说明

#### [OASIS](https://github.com/giorgiopicanco/OASIS)  
*核心*

语言：Python · 星标约：16

Open-Access System for Ionospheric Studies：从 GNSS 观测算 ROTI、ΔTEC、SIDX 等，做扰动与闪烁相关监测。适合空间天气事件个例与台站网指标产品。高采样率接收机原始闪烁指数（S4/σφ）仍需专用接收机或仿真器。

#### [IonoMoni](https://github.com/qiliu2025/IonoMoni)  
*★ Star*

语言：C++ · 星标约：37

C++ 实现多星座电离层监测指标（ROTI、AATR、STEC/VTEC），偏近实时监测。适合需要编译型性能的台站软件。文档与许可信息需自行确认；科研绘图可再接 Python 可视化。

#### [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator)

语言：MATLAB · 星标约：25

仿真电离层引起的相位与幅度闪烁，用于接收机跟踪环与完好性试验。适合算法仿真，不是实测 ROTI 产品生成器。参数调谐需对照文献与实测统计。

#### [gnssutils](https://github.com/ljlamarche/gnssutils)  
*★ Star*

语言：Python · 许可：GPL-3.0 · 星标约：3

处理地基 GNSS 闪烁观测的实用函数，适合已有闪烁接收机数据流的课题组。不替代通用 TEC/GIM 流水线；GPL 许可留意。

#### [OASIS-ohm1122](https://github.com/ohm1122/OASIS)  
*★ Star*

用户星标的 OASIS 相关仓库，实际算法与数据接口以 giorgiopicanco/OASIS 上游为准。引用论文时请核对 canonical URL。


## TEC预报

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tec_forecast](https://github.com/mauriciodev/tec_forecast) | 基于深度学习的全球 TEC 图预报示例 | Jupyter Notebook | 31 | ★ Star |
| [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM) | 注意力 ConvLSTM 的 TEC 图预报模型 | Jupyter Notebook | 10 |  |
| [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting) | 机器学习预报垂直 TEC 的示例项目 | Jupyter Notebook | 9 | ★ Star |

### 详细说明

#### [tec_forecast](https://github.com/mauriciodev/tec_forecast)  
*★ Star*

语言：Jupyter Notebook · 星标约：31

用 Keras/TF 等多类深度学习模型在全球电离层图上做 TEC 预报实验。适合学 ML+空间天气交叉的人对照复现。不是业务预报系统；数据切分、基线与物理约束要自己补齐，可与 ED-AttConvLSTM 等对比。

#### [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM)

语言：Jupyter Notebook · 星标约：10

编码器—解码器加注意力的 ConvLSTM，针对 TEC 图时序预报。适合复现相关论文结构。工程部署与多源同化不在范围；输入 GIM 分辨率与缺失值处理需自建。

#### [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting)  
*★ Star*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：9

教学向示例：用机器学习预报 VTEC，Apache 许可清晰。适合课堂与入门实验。模型深度和业务指标达不到业务空间天气预报标准。


## IONEX/TEC图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [INX_Editor](https://github.com/1acheng/INX_Editor) | 跨平台 IONEX 文件编辑工具 | — | 16 | ★ Star |
| [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX) | INPE TEC 图与 IONEX 生成工具 | Python | 15 | ★ Star |

### 详细说明

#### [INX_Editor](https://github.com/1acheng/INX_Editor)  
*★ Star*

星标约：16

面向 IONEX 的桌面编辑与检查，改网格、头信息或局部 TEC 值时比手改文本省事。适合产品质检与教学演示。不是 TEC 估计算法库；重建 TEC 仍需 PyTECGg/gnss-tec 等。

#### [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX)  
*★ Star*

语言：Python · 星标约：15

把电离层预报/分析系统输出整理成 TEC 图和 IONEX，方便与国际产品格式对齐。适合需要 IONEX 交换或南美区域 TEC 图的用户。对全球多分析中心产品融合支持有限；格式细节建议对照 IONEX 标准与 INX_Editor 一起核。


## 层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy) | 电离层层析几何矩阵相关代码 | — | — | ★ Star |

### 详细说明

#### [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy)  
*★ Star*

构造电离层层析用的几何矩阵，是层析反演前处理关键一步。适合写层析原型时对照。完整正则化反演与三维可视化需自建或接其他库。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 穿刺点IPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | 电离层穿刺点（IPP）计算 | — | — | ★ Star |

### 详细说明

#### [Get_IPP](https://github.com/Chenjiajun01/Get_IPP)  
*★ Star*

根据测站与卫星几何求电离层穿刺点，GIM/层析前处理常用。适合教学与自写映射函数前的几何模块。单薄脚本型项目，坐标框架与壳层高度约定要与主流程一致。


## 电离层工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonKit-NH](https://github.com/ohm1122/IonKit-NH) | IonKit-NH 电离层工具包 | — | — | ★ Star |
| [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH) | IonKit-NH 相关衍生/整理 | — | — | ★ Star |
| [IonTools](https://github.com/rumkex/IonTools) | 电离层分析工具集 | — | — | ★ Star |

### 详细说明

#### [IonKit-NH](https://github.com/ohm1122/IonKit-NH)  
*★ Star*

IonKit-NH 工具包星标种子，覆盖电离层数据处理相关脚本。适合浏览星标工作流；与 tanggdut 衍生版注意分辨上游。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH)  
*★ Star*

IonKit-NH 的衍生整理版，可能含路径或示例改动。合并进产线前先 diff 上游 ohm1122 版本，避免重复维护。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonTools](https://github.com/rumkex/IonTools)  
*★ Star*

电离层分析杂项工具集合，适合补充主流程里缺的小步骤。功能边界以仓库说明为准，关键科学结论建议用主流 TEC/GIM 库复核。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 电离层与PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP) | 广域电离层模型与 PPP 相关实现 | — | — | ★ Star |

### 详细说明

#### [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP)  
*★ Star*

把广域电离层模型和 PPP 联系起来的实践代码，适合看电离层约束如何进精密单点。完整度与星座支持需实测；系统级 PPP 仍建议对照 PRIDE、Ginan、raPPPid。
