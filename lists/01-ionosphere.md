# 电离层 / Ionosphere
> 共 **52** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

## GIM/球谐映射

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 维护者自有 GIM 实现（不展开） | MATLAB | 104 | 🚩 自有 |
| [mosgim2](https://github.com/PadArt/mosgim2) | 相位差法构建 GNSS 全球电离层图 | Python | 17 | ★ Star |
| [mosgim](https://github.com/gnss-lab/mosgim) | Padokhin 早期 MosGIM GIM 技术实现 | Python | 6 |  |
| [m_gim](https://github.com/PANXIONG-CN/m_gim) | MATLAB 侧 GIM 相关脚本 | MATLAB | 1 | ★ Star |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS 电离层图生成与处理 | — | — | ★ Star |
| [M_GIM](https://github.com/zcytju/M_GIM) | 电离层 GIM 相关 MATLAB/工具实现 | — | — | ★ Star |

### 详细说明

> 维护者自有仓库（SH-GIM）只在上表留链接，详细说明只写他人项目。


#### [mosgim2](https://github.com/PadArt/mosgim2)  
*★ Star*

语言：Python · 许可：MIT · 星标约：17

MosGIM 系第二代实现，侧重相位差思路从 GNSS 观测建 GIM，Python 栈便于接到现有数据流水线。适合研究组快速试算区域/全球 TEC 图。文档与工程化程度不如商业或大机构产品；球谐/网格参数需自行调，可与 gnss-tec、同类 GIM 工具做方法对比。

#### [mosgim](https://github.com/gnss-lab/mosgim)

语言：Python · 许可：MIT · 星标约：6

MosGIM 早期公开版本，便于追溯相位差 GIM 的原始流程。适合读论文后对照算法步骤。维护与功能完整度不如 mosgim2；新项目建议优先 mosgim2，本仓库作历史对照即可。

#### [m_gim](https://github.com/PANXIONG-CN/m_gim)  
*★ Star*

语言：MATLAB · 星标约：1

小体量 MATLAB GIM 相关代码，适合作为课程作业或方法草稿。功能覆盖面有限，不宜单独承担业务化建图。

#### [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps)  
*★ Star*

语言：—

侧重从 GNSS 观测生成与处理电离层图，适合做图件可视化或区域 TEC 展示。工程完整度与多星座支持需实测；若目标是可发表级全球 GIM，应同时参考 MosGIM2 与 IGS 产品规范。

#### [M_GIM](https://github.com/zcytju/M_GIM)  
*★ Star*

语言：—

面向 GIM 建模的 MATLAB 侧工具集合，适合已有 MATLAB 电离层工作流的人快速试用。公开说明偏少，需自行核验输入输出格式是否符合 IONEX/球谐习惯；可与 M_GIM 等变体对照使用。


## IRI/NeQuick

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [iri2016](https://github.com/space-physics/iri2016) | IRI-2016 的 Python/MATLAB 接口 | Fortran | 85 |  |
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | 国际参考电离层 IRI 的纯 Python 实现 | Python | 48 | 核心 |
| [NequickG](https://github.com/tpl2go/NequickG) | Galileo NeQuick-G 电离层模型 Python 实现 | Python | 45 | 核心 |
| [iri2020](https://github.com/space-physics/iri2020) | IRI-2020 气候模型封装 | Fortran | 25 |  |
| [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR) | ITU-R NeQuick 2 的 Python 封装 | Fortran | 4 |  |
| [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC) | JRC NeQuickG C 实现镜像/整理 | C | 4 |  |
| [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters) | IRI2020 参数相关资源 | — | — | ★ Star |

### 详细说明

#### [iri2016](https://github.com/space-physics/iri2016)

语言：Fortran · 许可：MIT · 星标约：85

把 IRI-2016 Fortran 核心包一层现代语言接口，结果更接近社区惯用的官方模型。适合需要标准 IRI-2016 输出的论文。编译环境与 IRI-2020 升级需注意；纯 Python 偏好可选 PyIRI。

#### [PyIRI](https://github.com/victoriyaforsythe/PyIRI)  
*核心*

语言：Python · 许可：MIT · 星标约：48

不绑 Fortran 也能跑 IRI 气候学电子密度/TEC 等，便于嵌进 Python 科研脚本。适合需要气候学背景场或与 GNSS TEC 对比的工作。实时扰动与闪烁物理不在 IRI 范围；要官方 IRI 数值一致性时可对照 iri2020 封装。

#### [NequickG](https://github.com/tpl2go/NequickG)  
*核心*

语言：Python · 星标约：45

实现 Galileo 单频改正常用的 NeQuick-G，便于与 Galileo ICD/性能评估对照。适合 SBAS/单频仿真与教学。官方 JRC 参考实现之外的社区版，数值对齐要用标准算例核验；C 版可见 NeQuickJRC。

#### [iri2020](https://github.com/space-physics/iri2020)

语言：Fortran · 许可：MIT · 星标约：25

IRI-2020 的可调用封装，跟进较新气候学版本。适合更新背景场或做版本差异试验。依赖 Fortran 构建；与 GNSS 实测 TEC 同化需另接。

#### [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR)

语言：Fortran · 星标约：4

为 ITU-R NeQuick 2 Fortran 核心提供 Python 包装，便于在脚本里调用气候学电离层模型做链路预算或单频改正对比。与 Galileo 专用 NeQuick-G（NequickG 仓库）分属不同标准版本，数值对齐要用官方算例；亦可对照 PyIRI、iri2016，避免混用模型参数。

#### [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC)

语言：C · 星标约：4

整理 JRC NeQuickG 的 C 实现便于编译调用，偏工程嵌入。作者声明非 JRC 原开发托管，使用前核对版本与许可。需要 Python 胶水时可与 NequickG 对照。

#### [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters)  
*★ Star*

语言：—

整理 IRI2020 运行所需参数/资源，减少自己找系数文件的时间。宜与 iri2020 主仓库搭配，而非独立模型。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## TEC估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | 由 RINEX 载波/伪距重建斜路径 TEC | Python | 54 | 核心 |
| [PyGPS](https://github.com/gregstarr/PyGPS) | 读 RINEX、算 TEC/卫星位置与偏差的工具箱 | Python | 47 |  |
| [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB) | MATLAB 双频 RINEX 2.11 TEC 计算 | MATLAB | 33 |  |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python+Rust） | Python | 29 | 🔀 Fork · ★ Star · 核心 |
| [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | 由 GPS 数据估计电离层 TEC 与旋转量 RM | Python | 26 |  |
| [tec-suite](https://github.com/gnss-lab/tec-suite) | SIMuRG 团队 TEC 重建套件 | Python | 23 |  |
| [pygnss-tec](https://github.com/eureka-0/pygnss-tec) | RINEX 读取与 TEC 计算（Rust 加速） | Python | 16 |  |
| [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation) | 单/双频方法估计电离层延迟梯度 | MATLAB | 6 |  |
| [tec-example](https://github.com/embrace-inpe/tec-example) | INPE Embrace 相关的 TEC 处理示例 | Python | 3 |  |
| [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research) | 处理 CDAAC COSMIC 掩星 NetCDF 做 TEC 研究 | Jupyter Notebook | 2 |  |
| [vtec](https://github.com/mfkiwl/vtec) | 垂直 TEC（VTEC）计算相关工具 | — | — | ★ Star |

### 详细说明

#### [gnss-tec](https://github.com/gnss-lab/gnss-tec)  
*核心*

语言：Python · 许可：MIT · 星标约：54

SIMuRG/gnss-lab 系经典 STEC 重建库，输入 RINEX 相位与伪距，输出斜路径 TEC，MIT 许可友好。适合论文复现与批处理建站网 TEC。GIM 成图、闪烁指数需另接 mosgim/OASIS 等；DCB 处理策略要按数据源核对。

#### [PyGPS](https://github.com/gregstarr/PyGPS)

语言：Python · 许可：AGPL-3.0 · 星标约：47

把读 RINEX、存 HDF5、算 TEC、卫星位置与接收机/卫星偏差串在一起，偏研究原型。适合快速探索。AGPL 较严；长期维护与测试覆盖不如专门 TEC 库，关键步骤建议交叉验证。

#### [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB)

语言：MATLAB · 星标约：33

基于双频接收机观测在 MATLAB 里算 TEC，输入偏 RINEX 2.11/GPS，教学友好。适合本科实验与快速验证。多星座、RINEX 3/4 与现代化 DCB 产品支持有限；科研产线建议再接 PyTECGg 等。

#### [PyTECGg](https://github.com/viventriglia/PyTECGg)  
*🔀 Fork · ★ Star · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：29

从 RINEX 做多星座 TEC 重建与接收机/卫星偏差相关校准，Rust 核心加快批处理。适合需要可编程 TEC 流水线、又想兼顾性能的研究组。Atlas2001-web 已 fork。GPL 许可需注意与闭源流程衔接；与 gnss-tec、tec-suite 比，更偏「可嵌入 Python 生态」。

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

#### [tec-example](https://github.com/embrace-inpe/tec-example)

语言：Python · 许可：MIT · 星标约：3

INPE Embrace 相关的 TEC 处理示例脚本，降低接触其数据产品与基本流程的门槛。适合南美区域 TEC 或空间天气入门。仓库体量小，不是完整产线；深度批处理请接 gnss-tec、PyTECGg 或 Embrace 官方推荐流程，并核对映射函数与 DCB 假设。

#### [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research)

语言：Jupyter Notebook · 星标约：2

Jupyter 流程读取 CDAAC/COSMIC 掩星 NetCDF，面向 TEC 与掩星电离层剖面研究，便于复现空基电子含量分析。做 GNSS-RO 与空间天气的人可作起点。不是地基双频 TEC 或 GIM 软件；产品字段、版本与质量控制需对照 CDAAC 官方文档，结果宜与地基网交叉验证。不同任务期产品版本不要混用后直接拼时间序列。

#### [vtec](https://github.com/mfkiwl/vtec)  
*★ Star*

语言：—

围绕 VTEC 换算与相关计算的小工具，适合把 STEC 投影到垂直方向做图或预报输入。功能边界较窄，完整双频重建与偏差估计需配合专业 TEC 库。


## 闪烁/ROTI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | 多星座 ROTI/AATR/STEC/VTEC 监测 | C++ | 37 | ★ Star |
| [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator) | GNSS 频段相位/幅度闪烁仿真 | MATLAB | 25 |  |
| [OASIS](https://github.com/giorgiopicanco/OASIS) | 从 RINEX 计算 ROTI/ΔTEC/SIDX 等扰动指标 | Python | 16 | 核心 |
| [scintill-ai](https://github.com/viventriglia/scintill-ai) | 用机器学习做电离层闪烁相关分析的研究项目 | Shell | 8 |  |
| [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP) | 电离层闪烁成像及其对 PDOP 影响的研究代码 | MATLAB | 5 |  |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据处理工具 | Python | 3 | ★ Star |
| [OASIS-ohm1122](https://github.com/ohm1122/OASIS) | OASIS 用户星标副本/相关仓库 | — | — | ★ Star |

### 详细说明

#### [IonoMoni](https://github.com/qiliu2025/IonoMoni)  
*★ Star*

语言：C++ · 星标约：37

C++ 实现多星座电离层监测指标（ROTI、AATR、STEC/VTEC），偏近实时监测。适合需要编译型性能的台站软件。文档与许可信息需自行确认；科研绘图可再接 Python 可视化。

#### [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator)

语言：MATLAB · 星标约：25

仿真电离层引起的相位与幅度闪烁，用于接收机跟踪环与完好性试验。适合算法仿真，不是实测 ROTI 产品生成器。参数调谐需对照文献与实测统计。

#### [OASIS](https://github.com/giorgiopicanco/OASIS)  
*核心*

语言：Python · 星标约：16

Open-Access System for Ionospheric Studies：从 GNSS 观测算 ROTI、ΔTEC、SIDX 等，做扰动与闪烁相关监测。适合空间天气事件个例与台站网指标产品。高采样率接收机原始闪烁指数（S4/σφ）仍需专用接收机或仿真器。

#### [scintill-ai](https://github.com/viventriglia/scintill-ai)

语言：Shell · 许可：MIT · 星标约：8

探索用机器学习刻画或预测电离层闪烁相关现象的研究型仓库，偏数据驱动实验原型。适合空间天气与机器学习交叉课题入门。闪烁事件稀缺、标签噪声与跨站点泛化是主要风险；报告结果时应保留 S4、σφ、ROTI 等物理基线对照，避免只展示神经网络分数而缺少可解释性。

#### [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP)

语言：MATLAB · 许可：MIT · 星标约：5

研究电离层闪烁空间成像及其对定位几何（PDOP）影响的代码，把空间天气扰动与导航可用性联系起来。适合闪烁—PNT 耦合与完好性相关课题。不是业务级闪烁监测网软件；输入场与网格假设应按论文复现，并可与 OASIS、ROTI 类工具对照物理指标定义。

#### [gnssutils](https://github.com/ljlamarche/gnssutils)  
*★ Star*

语言：Python · 许可：GPL-3.0 · 星标约：3

处理地基 GNSS 闪烁观测的实用函数，适合已有闪烁接收机数据流的课题组。不替代通用 TEC/GIM 流水线；GPL 许可留意。

#### [OASIS-ohm1122](https://github.com/ohm1122/OASIS)  
*★ Star*

语言：—

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
| [ionex](https://github.com/gnss-lab/ionex) | Python 读取 IONEX 电离层图文件 | Python | 12 | 核心 |
| [ionex-rs](https://github.com/nav-solutions/ionex) | Rust 实现的 IONEX 解析与处理 | Rust | 7 | 核心 |
| [IonMap](https://github.com/Jin-Whu/IonMap) | 由 IONEX 绘制电离层 TEC 地图 | Python | 4 |  |
| [rtcm2ionex](https://github.com/d-roma/rtcm2ionex) | 将 RTCM VTEC 消息转为 IONEX | Python | 3 |  |
| [ionex-analyzer](https://github.com/matador96/ionex-analyzer) | Electron/React 的 IONEX 可视化毕业作品 | JavaScript | 0 |  |

### 详细说明

#### [INX_Editor](https://github.com/1acheng/INX_Editor)  
*★ Star*

语言：— · 星标约：16

面向 IONEX 的桌面编辑与检查，改网格、头信息或局部 TEC 值时比手改文本省事。适合产品质检与教学演示。不是 TEC 估计算法库；重建 TEC 仍需 PyTECGg/gnss-tec 等。

#### [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX)  
*★ Star*

语言：Python · 星标约：15

把电离层预报/分析系统输出整理成 TEC 图和 IONEX，方便与国际产品格式对齐。适合需要 IONEX 交换或南美区域 TEC 图的用户。对全球多分析中心产品融合支持有限；格式细节建议对照 IONEX 标准与 INX_Editor 一起核。

#### [ionex](https://github.com/gnss-lab/ionex)  
*核心*

语言：Python · 许可：MIT · 星标约：12

gnss-lab 出品的轻量 IONEX 读入模块，把网格 TEC 图载入 Python 便于插值与绘图。做 GIM 对比、穿刺点改正或教学演示时很省事。不生成 GIM、不算 STEC；写 IONEX 或更高阶分析可看 nav-solutions/ionex（Rust）与 IonMap、rtcm2ionex 等配套工具，和 gnss-tec 流水线衔接自然。

#### [ionex-rs](https://github.com/nav-solutions/ionex)  
*核心*

语言：Rust · 许可：MPL-2.0 · 星标约：7

GeoRust/nav-solutions 生态下的 IONEX 库，强调类型安全与可嵌入 rinex-cli 一类工具链，适合已在 Rust GNSS 栈中处理格网电离层改正的人。Python 科研脚本更常直接用 gnss-lab/ionex；两者互补而非替代完整 GIM 建模，写图与球谐仍看 MosGIM2 等 GIM 工具。

#### [IonMap](https://github.com/Jin-Whu/IonMap)

语言：Python · 星标约：4

读取 IONEX 并绘制电离层 TEC 地图，适合论文插图、课程展示全球或区域 VTEC 分布。功能集中在可视化，不估计 STEC、不做球谐或层析建模；与 gnss-lab/ionex、ionosphere-plotting 等输出对照使用更完整，批处理画图时可脚本化调用。色标与投影选择会影响观感，分析结论仍看数值产品。

#### [rtcm2ionex](https://github.com/d-roma/rtcm2ionex)

语言：Python · 许可：GPL-3.0 · 星标约：3

把实时 RTCM 垂直 TEC 类消息写成 IONEX 格网文件，便于与事后 GIM 工具链、画图脚本对接。做实时电离层流试验或把 NTRIP 电离层产品落地存档时有用。星标少、场景窄，不替代双频 STEC 估计或球谐 GIM 建模，可与 gnss-lab/ionex、IonMap 串联。输出格网分辨率受源 RTCM 消息定义约束。

#### [ionex-analyzer](https://github.com/matador96/ionex-analyzer)

语言：JavaScript · 星标约：0

用 Electron/React 做的 IONEX 可视化桌面小应用，交互浏览格网 TEC 较友好，来源为毕业设计风格仓库。适合演示与教学展示。研究级批处理、插值、DCB 与建模请回到 Python/MATLAB 工具链；星标低、维护不确定，当作原型参考即可，勿当生产依赖。若只需脚本绑图，优先轻量 Python 方案更易维护。


## 层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoTomo](https://github.com/Joshuaalbert/IonoTomo) | 射电天文射线追踪与电离层层析仿真 | Jupyter Notebook | 11 |  |
| [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl) | 多 GNSS 星间链路辅助电离层层析仿真 | — | 2 |  |
| [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy) | 电离层层析几何矩阵相关代码 | — | — | ★ Star |
| [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation) | 体素电离层层析中的射线段矩阵计算 | C++ | 0 |  |

### 详细说明

#### [IonoTomo](https://github.com/Joshuaalbert/IonoTomo)

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：11

结合射线追踪与射电观测仿真做电离层层析，面向射电天文与空间天气交叉课题，Notebook 形式便于改参数。适合需要正演电离层对射电信号影响的人。不是 GNSS 双频 TEC 业务软件；地基 GNSS 体素层析可并行参考 SegmentsComputation 与 synthetic 层析仓库。仿真假设与真实射电阵几何差异需要单独评估。

#### [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl)

语言：— · 星标约：2

仿真多 GNSS 星间链路（ISL）辅助的电离层层析，探索新观测几何对电子密度反演的贡献。适合读相关论文后复现实验设置与几何配置。公开星标低、偏研究原型，落地需自备真实 ISL 或地基数据接口；可与 SegmentsComputation、IonoTomo 对照正演与矩阵环节。仿真噪声模型应尽量贴近目标星座链路预算。

#### [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy)  
*★ Star*

语言：—

构造电离层层析用的几何矩阵，是层析反演前处理关键一步。适合写层析原型时对照。完整正则化反演与三维可视化需自建或接其他库。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation)

语言：C++ · 星标约：0

专注层析反演里体素穿越段（segment）几何矩阵的算法实现，是三维电子密度反演的前置数值模块。做 GNSS 电离层层析的研究者可直接复用或对照公式。不是完整层析软件，需自备观测方程、权重与正则化；可与 IonoTomo、synthetic 层析仓库搭配搭建实验链。矩阵稀疏性与体素划分策略会显著影响反演稳定性。


## 穿刺点IPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | 电离层穿刺点（IPP）计算 | — | — | ★ Star |

### 详细说明

#### [Get_IPP](https://github.com/Chenjiajun01/Get_IPP)  
*★ Star*

语言：—

根据测站与卫星几何求电离层穿刺点，GIM/层析前处理常用。适合教学与自写映射函数前的几何模块。单薄脚本型项目，坐标框架与壳层高度约定要与主流程一致。


## 电离层工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting) | TEC、foF2 与 DST 等指数的绘图脚本 | Python | 7 |  |
| [ionex-downloader](https://github.com/ohm1122/ionex-downloader) | 批量下载 IONEX/GIM 产品的脚本 | — | 1 |  |
| [IonKit-NH](https://github.com/ohm1122/IonKit-NH) | IonKit-NH 电离层工具包 | — | — | ★ Star |
| [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH) | IonKit-NH 相关衍生/整理 | — | — | ★ Star |
| [IonTools](https://github.com/rumkex/IonTools) | 电离层分析工具集 | — | — | ★ Star |

### 详细说明

#### [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting)

语言：Python · 星标约：7

面向 TEC、foF2、DST 等指数与时间序列的 Python 绑图工具，适合快速出教学图或报告插图。研究级 GIM/STEC 重建请用 gnss-tec、MosGIM2 等；本仓库偏可视化与展示，数据获取与许可需自备，不宜单独支撑反演论文。输入数据格式需按脚本说明自行对齐时间与单位。选用前请用自有数据做交叉验证。

#### [ionex-downloader](https://github.com/ohm1122/ionex-downloader)

语言：— · 星标约：1

批处理拉取 IONEX（GIM）文件的小工具，减少手工下载 IGS 或分析中心产品的重复劳动。适合电离层课题数据准备与课程作业。维护活跃度与镜像源覆盖有限，生产流水线更常见用 wget/aria2、FAST 或机构自建镜像；下载后可用 IonMap 或 gnss-lab/ionex 继续处理。注意分析中心产品时延与文件命名规则变化。

#### [IonKit-NH](https://github.com/ohm1122/IonKit-NH)  
*★ Star*

语言：—

IonKit-NH 工具包星标种子，覆盖电离层数据处理相关脚本。适合浏览星标工作流；与 tanggdut 衍生版注意分辨上游。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH)  
*★ Star*

语言：—

IonKit-NH 的衍生整理版，可能含路径或示例改动。合并进产线前先 diff 上游 ohm1122 版本，避免重复维护。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonTools](https://github.com/rumkex/IonTools)  
*★ Star*

语言：—

电离层分析杂项工具集合，适合补充主流程里缺的小步骤。功能边界以仓库说明为准，关键科学结论建议用主流 TEC/GIM 库复核。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 电离层与PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP) | 广域电离层模型与 PPP 相关实现 | — | — | ★ Star |

### 详细说明

#### [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP)  
*★ Star*

语言：—

把广域电离层模型和 PPP 联系起来的实践代码，适合看电离层约束如何进精密单点。完整度与星座支持需实测；系统级 PPP 仍建议对照 PRIDE、Ginan、raPPPid。
