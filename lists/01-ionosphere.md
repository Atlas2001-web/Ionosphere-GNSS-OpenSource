# 电离层 / Ionosphere
> 共 **70** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

## GIM/球谐映射

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现（维护者自有，此处不展开） | MATLAB | 104 | 🏷️ 个人社区 · 🚩 |
| [mosgim2](https://github.com/PadArt/mosgim2) | 相位差法构建 GNSS 全球电离层图 | Python | 17 | 🏷️ 个人社区 · ★ Star |
| [mosgim](https://github.com/gnss-lab/mosgim) | Padokhin 早期 MosGIM GIM 技术实现 | Python | 6 | 🏷️ 高校实验室 |
| [m_gim](https://github.com/PANXIONG-CN/m_gim) | MATLAB 侧 GIM 相关脚本 | MATLAB | 1 | 🏷️ 个人社区 · ★ Star |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS 电离层图生成与处理 | — | — | 🏷️ 个人社区 · ★ Star |
| [M_GIM](https://github.com/zcytju/M_GIM) | 电离层 GIM 相关 MATLAB/工具实现 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

侧重从 GNSS 观测生成与处理电离层图，适合做图件可视化或区域 TEC 展示。工程完整度与多星座支持需实测；若目标是可发表级全球 GIM，应同时参考 MosGIM2 与 IGS 产品规范。

#### [m_gim](https://github.com/PANXIONG-CN/m_gim)  
*🏷️ 个人社区 · ★ Star*

语言：MATLAB · 许可：— · 星标约：1 · 宿主：github

小体量 MATLAB GIM 相关代码，适合作为课程作业或方法草稿。功能覆盖面有限，不宜单独承担业务化建图。

#### [M_GIM](https://github.com/zcytju/M_GIM)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

面向 GIM 建模的 MATLAB 侧工具集合，适合已有 MATLAB 电离层工作流的人快速试用。公开说明偏少，需自行核验输入输出格式是否符合 IONEX/球谐习惯；可与 M_GIM 等变体对照使用。

#### [mosgim](https://github.com/gnss-lab/mosgim)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

MosGIM 早期公开版本，便于追溯相位差 GIM 的原始流程。适合读论文后对照算法步骤。维护与功能完整度不如 mosgim2；新项目建议优先 mosgim2，本仓库作历史对照即可。

#### [mosgim2](https://github.com/PadArt/mosgim2)  
*🏷️ 个人社区 · ★ Star*

语言：Python · 许可：MIT · 星标约：17 · 宿主：github

MosGIM 系第二代实现，侧重相位差思路从 GNSS 观测建 GIM，Python 栈便于接到现有数据流水线。适合研究组快速试算区域/全球 TEC 图。文档与工程化程度不如商业或大机构产品；球谐/网格参数需自行调，可与 gnss-tec、同类 GIM 工具做方法对比。

#### [SH-GIM](https://github.com/Atlas2001-web/SH-GIM)  
*🏷️ 个人社区 · 🚩*

维护者自有仓库，本索引仅作分类收录，不作详细介绍。请直接查看上游 README。

## IONEX/TEC图

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [INX_Editor](https://github.com/1acheng/INX_Editor) | 跨平台 IONEX 文件编辑工具 | — | 16 | 🏷️ 个人社区 · ★ Star |
| [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX) | INPE TEC 图与 IONEX 生成工具 | Python | 15 | 🏷️ 个人社区 · ★ Star |
| [ionex](https://github.com/gnss-lab/ionex) | Python 读取 IONEX 电离层图文件 | Python | 12 | 🏷️ 高校实验室 · 核心 |
| [ionex-rs](https://github.com/nav-solutions/ionex) | Rust 实现的 IONEX 解析与处理 | Rust | 7 | 🏷️ 个人社区 · 核心 |
| [IonMap](https://github.com/Jin-Whu/IonMap) | 由 IONEX 绘制电离层 TEC 地图 | Python | 4 | 🏷️ 高校实验室 |
| [rtcm2ionex](https://github.com/d-roma/rtcm2ionex) | 将 RTCM VTEC 消息转为 IONEX | Python | 3 | 🏷️ 个人社区 |
| [ionex-analyzer](https://github.com/matador96/ionex-analyzer) | Electron/React 的 IONEX 可视化毕业作品 | JavaScript | 0 | 🏷️ 个人社区 |

### 详细说明

#### [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX)  
*🏷️ 个人社区 · ★ Star*

语言：Python · 许可：— · 星标约：15 · 宿主：github

把电离层预报/分析系统输出整理成 TEC 图和 IONEX，方便与国际产品格式对齐。适合需要 IONEX 交换或南美区域 TEC 图的用户。对全球多分析中心产品融合支持有限；格式细节建议对照 IONEX 标准与 INX_Editor 一起核。

#### [INX_Editor](https://github.com/1acheng/INX_Editor)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：16 · 宿主：github

面向 IONEX 的桌面编辑与检查，改网格、头信息或局部 TEC 值时比手改文本省事。适合产品质检与教学演示。不是 TEC 估计算法库；重建 TEC 仍需 PyTECGg/gnss-tec 等。

#### [ionex](https://github.com/gnss-lab/ionex)  
*🏷️ 高校实验室 · 核心*

语言：Python · 许可：MIT · 星标约：12 · 宿主：github

gnss-lab 出品的轻量 IONEX 读入模块，把网格 TEC 图载入 Python 便于插值与绘图。做 GIM 对比、穿刺点改正或教学演示时很省事。不生成 GIM、不算 STEC；写 IONEX 或更高阶分析可看 nav-solutions/ionex（Rust）与 IonMap、rtcm2ionex 等配套工具，和 gnss-tec 流水线衔接自然。

#### [ionex-analyzer](https://github.com/matador96/ionex-analyzer)  
*🏷️ 个人社区*

语言：JavaScript · 许可：— · 星标约：0 · 宿主：github

用 Electron/React 做的 IONEX 可视化桌面小应用，交互浏览格网 TEC 较友好，来源为毕业设计风格仓库。适合演示与教学展示。研究级批处理、插值、DCB 与建模请回到 Python/MATLAB 工具链；星标低、维护不确定，当作原型参考即可，勿当生产依赖。若只需脚本绑图，优先轻量 Python 方案更易维护。

#### [ionex-rs](https://github.com/nav-solutions/ionex)  
*🏷️ 个人社区 · 核心*

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

## IRI/NeQuick

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [iri2016](https://github.com/space-physics/iri2016) | IRI-2016 的 Python/MATLAB 接口 | Fortran | 85 | 🏷️ 高校实验室 |
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | 国际参考电离层 IRI 的纯 Python 实现 | Python | 48 | 🏷️ 高校实验室 · 核心 |
| [NequickG](https://github.com/tpl2go/NequickG) | Galileo NeQuick-G 电离层模型 Python 实现 | Python | 45 | 🏷️ 个人社区 · 核心 |
| [iri2020](https://github.com/space-physics/iri2020) | IRI-2020 气候模型封装 | Fortran | 25 | 🏷️ 高校实验室 |
| [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR) | ITU-R NeQuick 2 的 Python 封装 | Fortran | 4 | 🏷️ 个人社区 |
| [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC) | JRC NeQuickG C 实现镜像/整理 | C | 4 | 🏷️ 个人社区 |
| [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters) | IRI2020 参数相关资源 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [iri2016](https://github.com/space-physics/iri2016)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：85 · 宿主：github

把 IRI-2016 Fortran 核心包一层现代语言接口，结果更接近社区惯用的官方模型。适合需要标准 IRI-2016 输出的论文。编译环境与 IRI-2020 升级需注意；纯 Python 偏好可选 PyIRI。

#### [iri2020](https://github.com/space-physics/iri2020)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：25 · 宿主：github

IRI-2020 的可调用封装，跟进较新气候学版本。适合更新背景场或做版本差异试验。依赖 Fortran 构建；与 GNSS 实测 TEC 同化需另接。

#### [IRI2020_parameters](https://github.com/ohm1122/IRI2020_parameters)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

整理 IRI2020 运行所需参数/资源，减少自己找系数文件的时间。宜与 iri2020 主仓库搭配，而非独立模型。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [Nequick-ITUR](https://github.com/tpl2go/Nequick-ITUR)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：4 · 宿主：github

为 ITU-R NeQuick 2 Fortran 核心提供 Python 包装，便于在脚本里调用气候学电离层模型做链路预算或单频改正对比。与 Galileo 专用 NeQuick-G（NequickG 仓库）分属不同标准版本，数值对齐要用官方算例；亦可对照 PyIRI、iri2016，避免混用模型参数。

#### [NequickG](https://github.com/tpl2go/NequickG)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：— · 星标约：45 · 宿主：github

实现 Galileo 单频改正常用的 NeQuick-G，便于与 Galileo ICD/性能评估对照。适合 SBAS/单频仿真与教学。官方 JRC 参考实现之外的社区版，数值对齐要用标准算例核验；C 版可见 NeQuickJRC。

#### [NeQuickJRC](https://github.com/mgfernan/NeQuickJRC)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：4 · 宿主：github

整理 JRC NeQuickG 的 C 实现便于编译调用，偏工程嵌入。作者声明非 JRC 原开发托管，使用前核对版本与许可。需要 Python 胶水时可与 NequickG 对照。

#### [PyIRI](https://github.com/victoriyaforsythe/PyIRI)  
*🏷️ 高校实验室 · 核心*

语言：Python · 许可：MIT · 星标约：48 · 宿主：github

不绑 Fortran 也能跑 IRI 气候学电子密度/TEC 等，便于嵌进 Python 科研脚本。适合需要气候学背景场或与 GNSS TEC 对比的工作。实时扰动与闪烁物理不在 IRI 范围；要官方 IRI 数值一致性时可对照 iri2020 封装。

## IRI官方模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IRI-2020-package](https://irimodel.org/IRI-2020/) | IRI-2020 官方目录：Fortran 源码、系数、许可证与 zip/tar 包 | Fortran | — | 🏷️ 官方 |
| [IRI-Fortran](https://irimodel.org/) | COSPAR/URSI 官方 IRI 经验电离层模型 Fortran 源码与系数包 | Fortran | — | 🏷️ 官方 · 核心 |

### 详细说明

#### [IRI-2020-package](https://irimodel.org/IRI-2020/)  
*🏷️ 官方*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

irimodel.org 上 IRI-2020 的文件目录，可直接获取 00_iri.zip/tar、许可证与各 .for 系数文件。便于固定版本复现实验与回归测试。新版本（如 IRI-2026）请回主站查看；Python 封装见社区 iri2020/PyIRI，官方数值仍以此目录为准。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [IRI-Fortran](https://irimodel.org/)  
*🏷️ 官方 · 核心*

语言：Fortran · 许可：IRI permissive (AS IS + attribution) · 星标约：— · 宿主：official_site

国际参考电离层 IRI 的官方 Fortran 发行入口，由 COSPAR/URSI 工作组维护，提供电子密度、温度、离子成分与 vTEC 等气候态输出。可直接下载 IRI-2020/2026 压缩包与指数文件。适合作为标准对照模型写入论文复现实验；实时闪烁或扰动过程需另接观测或同化产品，不宜单独当作业务电离层改正引擎。

## NeQuick-G官方

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code) | 欧盟 GSC 发布的 Galileo 单频电离层改正 NeQuick G 官方 C 源码 | C | — | 🏷️ 官方 · 核心 |
| [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model) | ESA ESSR 登记的 NeQuick G 伽利略电离层改正实现（需注册） | C | — | 🏷️ 官方 |

### 详细说明

#### [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code)  
*🏷️ 官方 · 核心*

语言：C · 许可：EUPL-1.2 · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心提供的 NeQuick G 官方 C11 实现（含 JRC 库与测试驱动），面向 Galileo 单频用户电离层延迟改正。需注册并接受 EUPL 后下载加密包。与社区 GitHub 镜像相比应以本页为权威来源；气候态 NeQuick2 仍见 ICTP，二者算法与输入不同，集成前请对照 Galileo OS 电离层文档。

#### [NeQuickG-ESSR](https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model)  
*🏷️ 官方*

语言：C · 许可：ESA Community License v2.4 · 星标约：— · 宿主：official_site

ESA 软件资源库中的 NeQuick G 条目，说明该实现按 Galileo 单频电离层改正算法文档适配，区别于 ITU 气候态 NeQuick Fortran。注册后获取，许可为 ESA Community License。日常下载更常走欧盟 GSC 页面；本页适合核对 ESA 侧登记信息与许可类型。

## NeQuick官方

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code) | ICTP 官方 NeQuick 2 电离层电子密度模型 Fortran 源码申请页 | Fortran | — | 🏷️ 官方 |

### 详细说明

#### [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code)  
*🏷️ 官方*

语言：Fortran · 许可：scientific distribution (request) · 星标约：— · 宿主：official_site

阿卜杜斯·萨拉姆国际理论物理中心 T/ICT4D 发布的 NeQuick 2 气候态电子密度模型，含 ITU 系数与太阳活动/modip 文件。面向穿电离层传播与 TEC 积分研究。源码需向维护者邮件申请；若做 Galileo 单频接收机改正，请改用 GSC 的 NeQuick G 官方实现以免版本混淆。

## TEC估计

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | 由 RINEX 载波/伪距重建斜路径 TEC | Python | 54 | 🏷️ 高校实验室 · 核心 |
| [PyGPS](https://github.com/gregstarr/PyGPS) | 读 RINEX、算 TEC/卫星位置与偏差的工具箱 | Python | 47 | 🏷️ 个人社区 |
| [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB) | MATLAB 双频 RINEX 2.11 TEC 计算 | MATLAB | 33 | 🏷️ 高校实验室 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python+Rust） | Python | 29 | 🏷️ 个人社区 · 🔀 Fork · ★ Star · 核心 |
| [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | 由 GPS 数据估计电离层 TEC 与旋转量 RM | Python | 26 | 🏷️ 个人社区 |
| [tec-suite](https://github.com/gnss-lab/tec-suite) | SIMuRG 团队 TEC 重建套件 | Python | 23 | 🏷️ 高校实验室 |
| [pygnss-tec](https://github.com/eureka-0/pygnss-tec) | RINEX 读取与 TEC 计算（Rust 加速） | Python | 16 | 🏷️ 个人社区 |
| [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation) | 单/双频方法估计电离层延迟梯度 | MATLAB | 6 | 🏷️ 高校实验室 |
| [tec-example](https://github.com/embrace-inpe/tec-example) | INPE Embrace 相关的 TEC 处理示例 | Python | 3 | 🏷️ 官方 |
| [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research) | 处理 CDAAC COSMIC 掩星 NetCDF 做 TEC 研究 | Jupyter Notebook | 2 | 🏷️ 个人社区 |
| [vtec](https://github.com/mfkiwl/vtec) | 垂直 TEC（VTEC）计算相关工具 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：26 · 宿主：github

面向射电天文/地空链路，从 GPS 接收机数据估 TEC 与法拉第旋转相关量。适合需要 TEC+RM 联合的场景。通用 GNSS 多星座精密 TEC 流水线不是其主场；协议与输入格式需按仓库说明准备。

#### [CDAAC_COSMIC-TEC_Data-Research](https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：2 · 宿主：github

Jupyter 流程读取 CDAAC/COSMIC 掩星 NetCDF，面向 TEC 与掩星电离层剖面研究，便于复现空基电子含量分析。做 GNSS-RO 与空间天气的人可作起点。不是地基双频 TEC 或 GIM 软件；产品字段、版本与质量控制需对照 CDAAC 官方文档，结果宜与地基网交叉验证。不同任务期产品版本不要混用后直接拼时间序列。

#### [gnss-tec](https://github.com/gnss-lab/gnss-tec)  
*🏷️ 高校实验室 · 核心*

语言：Python · 许可：MIT · 星标约：54 · 宿主：github

SIMuRG/gnss-lab 系经典 STEC 重建库，输入 RINEX 相位与伪距，输出斜路径 TEC，MIT 许可友好。适合论文复现与批处理建站网 TEC。GIM 成图、闪烁指数需另接 mosgim/OASIS 等；DCB 处理策略要按数据源核对。

#### [pygnss-tec](https://github.com/eureka-0/pygnss-tec)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

Python 包读 RINEX 并算 TEC，关键路径用 Rust 加速，和 PyTECGg 同属「Py+加速核」路线。适合中等规模批处理。社区体量小于 gnss-tec；算法假设（映射、DCB）使用前要读文档核对。

#### [PyGPS](https://github.com/gregstarr/PyGPS)  
*🏷️ 个人社区*

语言：Python · 许可：AGPL-3.0 · 星标约：47 · 宿主：github

把读 RINEX、存 HDF5、算 TEC、卫星位置与接收机/卫星偏差串在一起，偏研究原型。适合快速探索。AGPL 较严；长期维护与测试覆盖不如专门 TEC 库，关键步骤建议交叉验证。

#### [PyTECGg](https://github.com/viventriglia/PyTECGg)  
*🏷️ 个人社区 · 🔀 Fork · ★ Star · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：29 · 宿主：github

从 RINEX 做多星座 TEC 重建与接收机/卫星偏差相关校准，Rust 核心加快批处理。适合需要可编程 TEC 流水线、又想兼顾性能的研究组。Atlas2001-web 已 fork。GPL 许可需注意与闭源流程衔接；与 gnss-tec、tec-suite 比，更偏「可嵌入 Python 生态」。

#### [TEC-calculation-MATLAB](https://github.com/cssrg-kmitl/TEC-calculation-MATLAB)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：33 · 宿主：github

基于双频接收机观测在 MATLAB 里算 TEC，输入偏 RINEX 2.11/GPS，教学友好。适合本科实验与快速验证。多星座、RINEX 3/4 与现代化 DCB 产品支持有限；科研产线建议再接 PyTECGg 等。

#### [tec-example](https://github.com/embrace-inpe/tec-example)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：3 · 宿主：github

INPE Embrace 相关的 TEC 处理示例脚本，降低接触其数据产品与基本流程的门槛。适合南美区域 TEC 或空间天气入门。仓库体量小，不是完整产线；深度批处理请接 gnss-tec、PyTECGg 或 Embrace 官方推荐流程，并核对映射函数与 DCB 假设。

#### [tec-suite](https://github.com/gnss-lab/tec-suite)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：23 · 宿主：github

比单库 gnss-tec 更偏「套件」形态，把重建流程串起来便于站点网作业。适合已在用 SIMuRG 工具链的人。GPL 约束与文档深度因版本而异；轻量嵌入可优先 gnss-tec。

#### [TEC_gradient_computation](https://github.com/cssrg-kmitl/TEC_gradient_computation)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：6 · 宿主：github

从 RINEX 估计电离层延迟梯度，服务于 GBAS/局域增强等对空间梯度敏感的应用。适合机场周遭或短基线梯度研究。全球 GIM 不是目标；与 ROTI/闪烁监测可互补。

#### [vtec](https://github.com/mfkiwl/vtec)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

围绕 VTEC 换算与相关计算的小工具，适合把 STEC 投影到垂直方向做图或预报输入。功能边界较窄，完整双频重建与偏差估计需配合专业 TEC 库。

## TEC预报

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tec_forecast](https://github.com/mauriciodev/tec_forecast) | 基于深度学习的全球 TEC 图预报示例 | Jupyter Notebook | 31 | 🏷️ 个人社区 · ★ Star |
| [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM) | 注意力 ConvLSTM 的 TEC 图预报模型 | Jupyter Notebook | 10 | 🏷️ 个人社区 |
| [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting) | 机器学习预报垂直 TEC 的示例项目 | Jupyter Notebook | 9 | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [ED-AttConvLSTM](https://github.com/leeliangchao/ED-AttConvLSTM)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：10 · 宿主：github

编码器—解码器加注意力的 ConvLSTM，针对 TEC 图时序预报。适合复现相关论文结构。工程部署与多源同化不在范围；输入 GIM 分辨率与缺失值处理需自建。

#### [Ionospheric-VTEC-Forecasting](https://github.com/ICCT-ML-in-geodesy/Ionospheric-VTEC-Forecasting)  
*🏷️ 个人社区 · ★ Star*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：9 · 宿主：github

教学向示例：用机器学习预报 VTEC，Apache 许可清晰。适合课堂与入门实验。模型深度和业务指标达不到业务空间天气预报标准。

#### [tec_forecast](https://github.com/mauriciodev/tec_forecast)  
*🏷️ 个人社区 · ★ Star*

语言：Jupyter Notebook · 许可：— · 星标约：31 · 宿主：github

用 Keras/TF 等多类深度学习模型在全球电离层图上做 TEC 预报实验。适合学 ML+空间天气交叉的人对照复现。不是业务预报系统；数据切分、基线与物理约束要自己补齐，可与 ED-AttConvLSTM 等对比。

## 传播模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx) | ITU-R 电离层/对流层电波传播软件与验证数据入口 | various | — | 🏷️ 官方 |

### 详细说明

#### [ITU-R-iono-tropo-software](https://www.itu.int/en/ITU-R/study-groups/rsg3/rwp3m/Pages/digprod.aspx)  
*🏷️ 官方*

语言：various · 许可：ITU terms · 星标约：— · 宿主：official_site

国际电联无线电通信部门汇总的电离层与对流层传播预测软件、数据与验证示例入口，涵盖推荐方法相关数字产品。许可与获取按 ITU 条款办理。适合传播与链路预算研究；GNSS 精密定位仍多用 IRI、NeQuick、VMF 等专用实现。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。

## 层析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoTomo](https://github.com/Joshuaalbert/IonoTomo) | 射电天文射线追踪与电离层层析仿真 | Jupyter Notebook | 11 | 🏷️ 个人社区 |
| [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl) | 多 GNSS 星间链路辅助电离层层析仿真 | — | 2 | 🏷️ 个人社区 |
| [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy) | 电离层层析几何矩阵相关代码 | — | — | 🏷️ 个人社区 · ★ Star |
| [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation) | 体素电离层层析中的射线段矩阵计算 | C++ | 0 | 🏷️ 个人社区 |

### 详细说明

#### [Geometric-Matrix-For-Ionospheric-Tomogrphy](https://github.com/yujieqing/Geometric-Matrix-For-Ionospheric-Tomogrphy)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

构造电离层层析用的几何矩阵，是层析反演前处理关键一步。适合写层析原型时对照。完整正则化反演与三维可视化需自建或接其他库。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonoTomo](https://github.com/Joshuaalbert/IonoTomo)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：Apache-2.0 · 星标约：11 · 宿主：github

结合射线追踪与射电观测仿真做电离层层析，面向射电天文与空间天气交叉课题，Notebook 形式便于改参数。适合需要正演电离层对射电信号影响的人。不是 GNSS 双频 TEC 业务软件；地基 GNSS 体素层析可并行参考 SegmentsComputation 与 synthetic 层析仓库。仿真假设与真实射电阵几何差异需要单独评估。

#### [SegmentsComputation](https://github.com/yujieqing/SegmentsComputation)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：0 · 宿主：github

专注层析反演里体素穿越段（segment）几何矩阵的算法实现，是三维电子密度反演的前置数值模块。做 GNSS 电离层层析的研究者可直接复用或对照公式。不是完整层析软件，需自备观测方程、权重与正则化；可与 IonoTomo、synthetic 层析仓库搭配搭建实验链。矩阵稀疏性与体素划分策略会显著影响反演稳定性。

#### [synthetic_ionospheric_tomography_isl](https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：2 · 宿主：github

仿真多 GNSS 星间链路（ISL）辅助的电离层层析，探索新观测几何对电子密度反演的贡献。适合读相关论文后复现实验设置与几何配置。公开星标低、偏研究原型，落地需自备真实 ISL 或地基数据接口；可与 SegmentsComputation、IonoTomo 对照正演与矩阵环节。仿真噪声模型应尽量贴近目标星座链路预算。

## 电离层与PPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP) | 广域电离层模型与 PPP 相关实现 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [WA_ion_model_PPP](https://github.com/FearlessWu/WA_ion_model_PPP)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

把广域电离层模型和 PPP 联系起来的实践代码，适合看电离层约束如何进精密单点。完整度与星座支持需实测；系统级 PPP 仍建议对照 PRIDE、Ginan、raPPPid。

## 电离层工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting) | TEC、foF2 与 DST 等指数的绘图脚本 | Python | 7 | 🏷️ 个人社区 |
| [ionex-downloader](https://github.com/ohm1122/ionex-downloader) | 批量下载 IONEX/GIM 产品的脚本 | — | 1 | 🏷️ 个人社区 |
| [IonKit-NH](https://github.com/ohm1122/IonKit-NH) | IonKit-NH 电离层工具包 | — | — | 🏷️ 个人社区 · ★ Star |
| [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH) | IonKit-NH 相关衍生/整理 | — | — | 🏷️ 个人社区 · ★ Star |
| [IonTools](https://github.com/rumkex/IonTools) | 电离层分析工具集 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [ionex-downloader](https://github.com/ohm1122/ionex-downloader)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：1 · 宿主：github

批处理拉取 IONEX（GIM）文件的小工具，减少手工下载 IGS 或分析中心产品的重复劳动。适合电离层课题数据准备与课程作业。维护活跃度与镜像源覆盖有限，生产流水线更常见用 wget/aria2、FAST 或机构自建镜像；下载后可用 IonMap 或 gnss-lab/ionex 继续处理。注意分析中心产品时延与文件命名规则变化。

#### [IonKit-NH](https://github.com/ohm1122/IonKit-NH)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

IonKit-NH 工具包星标种子，覆盖电离层数据处理相关脚本。适合浏览星标工作流；与 tanggdut 衍生版注意分辨上游。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [IonKit-NH-tanggdut](https://github.com/tanggdut/IonKit-NH)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

IonKit-NH 的衍生整理版，可能含路径或示例改动。合并进产线前先 diff 上游 ohm1122 版本，避免重复维护。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [ionosphere-plotting](https://github.com/arwildo/ionosphere-plotting)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：7 · 宿主：github

面向 TEC、foF2、DST 等指数与时间序列的 Python 绑图工具，适合快速出教学图或报告插图。研究级 GIM/STEC 重建请用 gnss-tec、MosGIM2 等；本仓库偏可视化与展示，数据获取与许可需自备，不宜单独支撑反演论文。输入数据格式需按脚本说明自行对齐时间与单位。选用前请用自有数据做交叉验证。

#### [IonTools](https://github.com/rumkex/IonTools)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

电离层分析杂项工具集合，适合补充主流程里缺的小步骤。功能边界以仓库说明为准，关键科学结论建议用主流 TEC/GIM 库复核。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## 穿刺点IPP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | 电离层穿刺点（IPP）计算 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [Get_IPP](https://github.com/Chenjiajun01/Get_IPP)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

根据测站与卫星几何求电离层穿刺点，GIM/层析前处理常用。适合教学与自写映射函数前的几何模块。单薄脚本型项目，坐标框架与壳层高度约定要与主流程一致。

## 闪烁/ROTI

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | 多星座 ROTI/AATR/STEC/VTEC 监测 | C++ | 37 | 🏷️ 个人社区 · ★ Star |
| [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator) | GNSS 频段相位/幅度闪烁仿真 | MATLAB | 25 | 🏷️ 个人社区 |
| [OASIS](https://github.com/giorgiopicanco/OASIS) | 从 RINEX 计算 ROTI/ΔTEC/SIDX 等扰动指标 | Python | 16 | 🏷️ 个人社区 · 核心 |
| [scintill-ai](https://github.com/viventriglia/scintill-ai) | 用机器学习做电离层闪烁相关分析的研究项目 | Shell | 8 | 🏷️ 个人社区 |
| [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP) | 电离层闪烁成像及其对 PDOP 影响的研究代码 | MATLAB | 5 | 🏷️ 个人社区 |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据处理工具 | Python | 3 | 🏷️ 个人社区 · ★ Star |
| [OASIS-ohm1122](https://github.com/ohm1122/OASIS) | OASIS 用户星标副本/相关仓库 | — | — | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [gnss-scintillation-simulator](https://github.com/cu-sense-lab/gnss-scintillation-simulator)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：25 · 宿主：github

仿真电离层引起的相位与幅度闪烁，用于接收机跟踪环与完好性试验。适合算法仿真，不是实测 ROTI 产品生成器。参数调谐需对照文献与实测统计。

#### [gnssutils](https://github.com/ljlamarche/gnssutils)  
*🏷️ 个人社区 · ★ Star*

语言：Python · 许可：GPL-3.0 · 星标约：3 · 宿主：github

处理地基 GNSS 闪烁观测的实用函数，适合已有闪烁接收机数据流的课题组。不替代通用 TEC/GIM 流水线；GPL 许可留意。

#### [IonoMoni](https://github.com/qiliu2025/IonoMoni)  
*🏷️ 个人社区 · ★ Star*

语言：C++ · 许可：— · 星标约：37 · 宿主：github

C++ 实现多星座电离层监测指标（ROTI、AATR、STEC/VTEC），偏近实时监测。适合需要编译型性能的台站软件。文档与许可信息需自行确认；科研绘图可再接 Python 可视化。

#### [Ionospheric-Scintillation-Maps-and-PDOP](https://github.com/AlexandraKoulouri/Ionospheric-Scintillation-Maps-and-PDOP)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：5 · 宿主：github

研究电离层闪烁空间成像及其对定位几何（PDOP）影响的代码，把空间天气扰动与导航可用性联系起来。适合闪烁—PNT 耦合与完好性相关课题。不是业务级闪烁监测网软件；输入场与网格假设应按论文复现，并可与 OASIS、ROTI 类工具对照物理指标定义。

#### [OASIS](https://github.com/giorgiopicanco/OASIS)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：— · 星标约：16 · 宿主：github

Open-Access System for Ionospheric Studies：从 GNSS 观测算 ROTI、ΔTEC、SIDX 等，做扰动与闪烁相关监测。适合空间天气事件个例与台站网指标产品。高采样率接收机原始闪烁指数（S4/σφ）仍需专用接收机或仿真器。

#### [OASIS-ohm1122](https://github.com/ohm1122/OASIS)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：— · 宿主：github

用户星标的 OASIS 相关仓库，实际算法与数据接口以 giorgiopicanco/OASIS 上游为准。引用论文时请核对 canonical URL。

#### [scintill-ai](https://github.com/viventriglia/scintill-ai)  
*🏷️ 个人社区*

语言：Shell · 许可：MIT · 星标约：8 · 宿主：github

探索用机器学习刻画或预测电离层闪烁相关现象的研究型仓库，偏数据驱动实验原型。适合空间天气与机器学习交叉课题入门。闪烁事件稀缺、标签噪声与跨站点泛化是主要风险；报告结果时应保留 S4、σφ、ROTI 等物理基线对照，避免只展示神经网络分数而缺少可解释性。

## IRI官方入口（本轮补录）

| 项目 | 一句话 | 语言 | 标记 |
|---|---|---|---|
| [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model) | irimodel.org 官方指向的 IRI MATLAB 封装（File Exchange，含 2012/2016） | MATLAB | 核心 · 🏷️ 官方 |
| [pyglow](https://github.com/timduly4/pyglow) | Python 上层大气气候态库，包装 IRI-2012/2016 等（irimodel 官网推荐） | Python/Fortran | 核心 · 🏷️ 个人社区 |
| [IRI-2016-package](https://irimodel.org/IRI-2016/) | IRI-2016 官方 Fortran 源码与系数包目录 | Fortran | 🏷️ 官方 |
| [IRI-2012-package](https://irimodel.org/IRI-2012/) | IRI-2012 官方 Fortran 源码包（含轨道剖面示例程序） | Fortran | 🏷️ 官方 |
| [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/) | NASA CCMC 在线运行与说明页（IRI-2020） | — | 🏷️ 官方 |

### 详细说明（本轮补录）

#### [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model)  
*核心 · 🏷️ 官方*

语言：MATLAB

国际参考电离层工作组官网明确列出的 MATLAB 版本入口，指向 MathWorks File Exchange 条目，覆盖 IRI-2012 与 IRI-2016 的 MATLAB 调用。适合已经在用 MATLAB 做电离层气候态对比、不想先啃 Fortran 编译链的人。这不是 GitHub 仓，下载与许可以 File Exchange 页面为准；要最新 Fortran 物理更新仍应回到 irimodel.org 的 IRI-2020/2026 源码包。与 space-physics/iri2016 等第三方包装不同，本条目以官网推荐链接为准。

#### [pyglow](https://github.com/timduly4/pyglow)  
*核心 · 🏷️ 个人社区*

语言：Python/Fortran · 许可：MIT · 星标约：117

把 IRI 等上层大气经验模型接到 Python，irimodel.org 在「pyglow」一行直接链到本仓库，说明它是社区里常用的 IRI-2012/2016 包装路径。适合脚本化批量取 Ne/Te 剖面、和 GNSS TEC 产品做气候态对照。底层仍依赖 Fortran 模型文件与指数更新；跟官方最新 IRI-2020/2026 发布节奏可能不同步，精密业务应核对所绑版本。许可 MIT，比部分需注册的官方 C 发行更好集成。

#### [IRI-2016-package](https://irimodel.org/IRI-2016/)  
*🏷️ 官方*

语言：Fortran

COSPAR/URSI IRI 工作组在 irimodel.org 发布的 IRI-2016 源码目录，含 Fortran 子程序、系数与说明。很多文献与 MATLAB/pyglow 包装仍对齐这一代。新研究若无追踪官方最新物理选项，应同时看 IRI-2020/2026；指数文件需按官网说明单独更新。

#### [IRI-2012-package](https://irimodel.org/IRI-2012/)  
*🏷️ 官方*

语言：Fortran

官方 IRI-2012 发行目录。官网特别提到该版带有 iriorbit 一类沿卫星轨道取 IRI 参数的示例程序，适合空间任务剖面复现与旧论文对照。功能与数据源已有后续版本更新；除非复现 2012 时代结果，新项目优先 IRI-2020/2026，MATLAB/pyglow 用户也要分清自己绑的是哪一代。

#### [CCMC-IRI-online](https://ccmc.gsfc.nasa.gov/models/IRI~2020/)  
*🏷️ 官方*

NASA 社区协调建模中心提供的 IRI 在线计算与模型说明入口，适合快速查剖面、看输入开关，而不是本地二次开发。要嵌入自己的 GNSS/TEC 流水线仍需下载 irimodel Fortran 或 Python/MATLAB 包装。页面会指向模型版本与相关文献，可作为官方文档跳板。

## IRI官网目录补全

| 项目 | 一句话 | 标记 |
|---|---|---|
| [IRI-2026-package](https://irimodel.org/IRI-2026/) | IRI-2026 官方 Fortran 最新源码包目录 | 🏷️ 官方 · 核心 |
| [IRI-2007-package](https://irimodel.org/IRI-2007/) | IRI-2007 官方 Fortran 历史版本源码目录 | 🏷️ 官方 |
| [IRI-2001-package](https://irimodel.org/IRI-2001/) | IRI-2001 官方 Fortran 历史版本源码目录 | 🏷️ 官方 |
| [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/) | 各版 IRI 共用的系数/公共文件目录（官网明确要求另下） | 🏷️ 官方 · 核心 |
| [IRI-indices](http://irimodel.org/indices/) | IRI 运行所需太阳/地磁指数文件发布页 | 🏷️ 官方 |
| [GIRO-portal](https://giro.uml.edu/) | GIRO 全球电离层测高仪观测网门户（IRTAM 等数据入口） | 🏷️ 官方 |
| [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code) | ICTP 官方 NeQuick 2 电离层电子密度模型 Fortran 源码申请页 | 🏷️ 官方 |

### 详细说明

#### [IRI-2026-package](https://irimodel.org/IRI-2026/)

irimodel.org 上标注日期最新的 IRI Fortran 发行目录，工作组持续更新的气候态电离层国际标准模型入口。做与最新文献对齐的 Ne/Te/离子成分剖面时优先从这里取源码与系数。指数文件仍需按官网说明单独更新；Python/MATLAB 包装未必已跟上 2026，绑定前核对版本号。

#### [IRI-2007-package](https://irimodel.org/IRI-2007/)

官方保留的 IRI-2007 发行，便于复现该年代论文或对比模型演进。新项目应改用 IRI-2020/2026；仅当审稿或历史对比需要锁定旧物理选项时再下载本目录。

#### [IRI-2001-package](https://irimodel.org/IRI-2001/)

更早的官方 IRI 发行，主要用于历史复现。系数与选项与当代版本差异大，不适合作为现行 GNSS 电离层改正基准；对照阅读可看官网更新说明与 Bilitza 综述。

#### [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/)

irimodel 写明：除版本包外通常还要 COMMON FILES（若 zip 未打进包内）。缺公共系数时编译或运行常失败。搭本地 IRI 时与具体版本目录、最新 INDICES 一起下载；不要只克隆 GitHub 包装而漏官方公共文件。

#### [IRI-indices](http://irimodel.org/indices/)

官方指数文件入口（如 ap、IG、F10.7 相关序列）。IRI 按日期查内部指数，过期指数会让剖面偏离。业务或论文复现应定期更新本页文件；pyglow/第三方包装若自带指数，也要核对其时效。

#### [GIRO-portal](https://giro.uml.edu/)

UML 维护的 GIRO 门户，通向测高仪数据与 IRTAM 等实时同化产品相关入口。适合把测高仪峰值参数与 GNSS TEC/IRI 对比。主要是数据与服务门户，不是 GNSS 解算库；下载具体软件前在站内核对许可与程序页。

#### [NeQuick2-ICTP](https://t-ict4d.ictp.it/nequick2/source-code)

阿卜杜斯·萨拉姆国际理论物理中心 T/ICT4D 发布的 NeQuick 2 气候态电子密度模型，含 ITU 系数与太阳活动/modip 文件。面向穿电离层传播与 TEC 积分研究。源码需向维护者邮件申请；若做 Galileo 单频接收机改正，请改用 GSC 的 NeQuick G 官方实现以免版本混淆。

