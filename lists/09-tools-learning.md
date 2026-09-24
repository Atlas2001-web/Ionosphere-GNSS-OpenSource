# 学习资源与工具 / Tools & Learning
> **59** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。

## 数据集

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset) | 香港/东京等城市峡谷 GNSS/INS/视觉基准集 | Python | 606 | 🏷️ 高校实验室 |
| [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets) | awesome-gins-datasets：车载 GNSS/INS 数据集列表 | — | 280 | 🏷️ 高校实验室 核心 |
| [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green) | gnss2tws-green：GNSS 垂直位移反演陆地水储量 | MATLAB | 33 | 🏷️ 高校实验室 |

### 详细说明

#### [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：606 · 宿主：github

香港理工 IPNL 等发布的城市峡谷多传感器数据，含真值，是 GNSS/INS/视觉融合算法常用基准。适合算法评测与论文对比。本身不是解算软件；使用请遵守数据集许可与引用要求。

#### [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets)  
*🏷️ 高校实验室 核心*

语言：— · 许可：— · 星标约：280 · 宿主：github

汇总适合车载 GNSS/INS 组合导航评测的公开数据集与说明入口，减少四处搜数据的时间成本。适合写论文基线、算法对比与课程大作业选题。本身不是解算软件；引用各数据集时要核对许可协议、传感器时间同步与标定文件是否齐全，缺失标定会严重扭曲融合精度结论。

#### [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：GPL-3.0 · 星标约：33 · 宿主：github

开源 MATLAB 工具 GNSS2TWS：利用 GNSS 测站日尺度垂直位移，经格林函数等方法推断陆地水储量（TWS）变化，服务水文大地测量。适合已有精密坐标时间序列、做气候水文交叉的研究者。不是导航定位解算器；空间平滑、负载模型与参考框架假设必须按配套论文核对。输入坐标序列质量决定反演可信度。站点分布稀疏时，反演空间分辨率会明显下降。

## 资源列表

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [awesome-gnss-barbeau](https://github.com/barbeau/awesome-gnss) | awesome-gnss：GNSS 开源资源列表 | — | 599 | 🏷️ 个人社区 核心 |
| [awesome-gnss-hdkarimi](https://github.com/hdkarimi/awesome-gnss) | awesome-gnss-hdkarimi：GNSS/RNSS 开源与慕课策展列表 | — | 50 | 🏷️ 个人社区 |

### 详细说明

#### [awesome-gnss-barbeau](https://github.com/barbeau/awesome-gnss)  
*🏷️ 个人社区 核心*

语言：— · 许可：Apache-2.0 · 星标约：599 · 宿主：github

Sean Barbeau 维护的 awesome 列表，覆盖 App、桌面工具、库与文献入口，本目录大量种子来源之一。适合定期浏览查新。本身不含算法实现。

#### [awesome-gnss-hdkarimi](https://github.com/hdkarimi/awesome-gnss)  
*🏷️ 个人社区*

语言：— · 许可：MIT · 星标约：50 · 宿主：github

策展 GNSS/RNSS 相关开源软件、数据、工具与慕课入口的 awesome 列表，帮助新人快速摸清领域版图。与 barbeau/awesome-gnss（现名 awesome-gnss-barbeau）是不同策展；链接时效性需自行点击验证。

## 高程/大地水准面

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [earth-gravitational-model](https://github.com/barbeau/earth-gravitational-model) | earth-gravitational-model：WGS84→EGM84 海拔转换（Android 向） | Java | 18 | 🏷️ 个人社区 |

### 详细说明

#### [earth-gravitational-model](https://github.com/barbeau/earth-gravitational-model)  
*🏷️ 个人社区*

语言：Java · 许可：LGPL-2.1 · 星标约：18 · 宿主：github

基于 GeoTools 大地水准面模型的轻量 Java 库，方便 Android 海拔转换。测地学严密应用请用专业大地水准面产品与更新格网。

## 可视化

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility) | ge-gnss-visibility：Google Earth 可见性分析 | MATLAB | 137 | 🏷️ 个人社区 |
| [gnss_timeseries_viewers](https://github.com/kmaterna/gnss_timeseries_viewers) | gnss_timeseries_viewers：PBO/UNR 坐标时序分析绘图 | Python | 36 | 🏷️ 高校实验室 |
| [EasyGNSS](https://github.com/whigg/EasyGNSS) | EasyGNSS：低成本 GNSS 图形界面辅助工具 | Python | 4 | 🏷️ 高校实验室 |
| [GPS-Velocity-Viewer](https://www.unavco.org/software/visualization/GPS-Velocity-Viewer/GPS-Velocity-Viewer.html) | GPS-Velocity-Viewer：UNAVCO GNSS 速度场在线可视化 | web | — | 🏷️ 官方 |

### 详细说明

#### [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：137 · 宿主：github

在任意位置生成虚拟鱼眼天顶图并判断 GNSS 可见性，城市遮挡研究直观。需要 Google Earth 相关环境。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [gnss_timeseries_viewers](https://github.com/kmaterna/gnss_timeseries_viewers)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：36 · 宿主：github

伯克利相关维护者发布的 Python 包，专注 GNSS 坐标时间序列：读 PBO/UNR 等产品、估计斜率/季节项/阶跃，并做堆叠图。依赖 Poetry/conda 环境与 EarthScope 相关 CLI。用于形变时序分析，不处理原始 RINEX 观测。

#### [EasyGNSS](https://github.com/whigg/EasyGNSS)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：4 · 宿主：github

为低成本 GNSS 接收机提供简易图形界面，降低配置、查看星空与状态的门槛。适合教学演示、业余爱好者台站与快速连通性检查。精密解算与质检能力有限；深入分析请导出 RINEX 后接入 RTKLIB、Anubis 或 georinex 流水线。

#### [GPS-Velocity-Viewer](https://www.unavco.org/software/visualization/GPS-Velocity-Viewer/GPS-Velocity-Viewer.html)  
*🏷️ 官方*

语言：web · 许可：site terms · 星标约：— · 宿主：official_site

面向 GNSS 测站速度场的浏览器可视化工具，便于快速查看区域形变矢量。属于机构托管的 Web 应用而非本地库；科研制图仍常导出后用 GMT/Python。适合教学演示与数据探索，不能替代时间序列精密分析或网平差软件。使用前请核验上游页面与许可条款。

## SBAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EGNOS-GSC-User-Support](https://egnos.gsc-europa.eu/) | EGNOS GSC：欧洲静地导航重叠系统用户支持 | data-portal | — | 🏷️ 官方 |
| [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos/) | SourceForge EGNOS Toolkit：SBAS/EGNOS 消息与接收算法工具 | C/C++ | — | 🏷️ 个人社区 |
| [FAA-WAAS](https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/waas) | FAA WAAS：美国广域增强系统官方介绍 | data-portal | — | 🏷️ 官方 |
| [ICAO-PBN](https://www.icao.int/safety/pbn/Pages/Overview.aspx) | ICAO PBN：基于性能导航官方概述入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EGNOS-GSC-User-Support](https://egnos.gsc-europa.eu/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心（GSC）EGNOS 用户支持站点，汇总服务状态、文档与用户资源（原 ESSP 入口现多导向此域）。官方 portal；与 EGNOS SDK/Toolkit 代码条目互补。适合 SBAS 服务调研，EDAS 等实时数据接口往往需要注册，条款以站内说明为准。

#### [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos/)  
*🏷️ 个人社区*

语言：C/C++ · 许可：EUPL · 星标约：— · 宿主：sourceforge

基于 EGNOS SDK 的 Linux/UNIX 移植，处理 SISNET、EMS 文件并实现用户端 SBAS 算法，许可 EUPL。托管于 SourceForge，更新偏旧。现代多星座 SBAS/HAS 研究需结合新文档与其他开源栈。

#### [FAA-WAAS](https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/waas)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

联邦航空局关于 WAAS 的官方导航页，说明广域增强架构、服务与相关 GNSS 导航服务入口。portal-terms；与 NSTB 测试数据页互补。偏航空完好性与服务说明，不是 RINEX 下载站；技术细节与运行状态请再循 FAA/NAVCEN 相关链接核实。

#### [ICAO-PBN](https://www.icao.int/safety/pbn/Pages/Overview.aspx)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

国际民航组织关于 Performance-Based Navigation（PBN）的概述页，链向航空导航性能与相关文件框架，常与 GNSS/SBAS 完好性运行要求对照。官方 portal；偏规章与运行概念，不是接收机开源代码。具体 SARPs/手册下载遵循 ICAO 分发规则。

## 机构软件门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ENRI-Japan](https://www.enri.go.jp/eng/index.html) | ENRI：日本电子航法研究所（航空 CNS）门户 | data-portal | — | 🏷️ 官方 |
| [GA-Positioning-Services](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/services-and-tools) | Geoscience Australia 定位服务与工具门户（SouthPAN/AUSPOS/数据中心） | various | — | 🏷️ 官方 |
| [GPS.gov](https://www.gps.gov/) | GPS.gov：美国 GPS 系统官方公众信息站 | data-portal | — | 🏷️ 官方 |
| [ISRO-IRNSS-NavIC](https://www.isro.gov.in/IRNSS_Programme.html) | ISRO NavIC：印度区域导航系统官方计划页 | data-portal | — | 🏷️ 官方 |
| [NGS-PC-PROD](https://geodesy.noaa.gov/PC_PROD/) | NGS-PC-PROD：NOAA/NGS 大地测量 PC 软件门户（含 HTDP 等） | various | — | 🏷️ 官方 |
| [UNAVCO-Software-Portal](https://www.unavco.org/software/) | UNAVCO-Software-Portal：EarthScope/GAGE 软件总入口（TEQC 等） | various | — | 🏷️ 官方 |
| [USCG-NAVCEN](https://www.navcen.uscg.gov/) | NAVCEN：美国海岸警卫队导航与 GNSS 门户 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [ENRI-Japan](https://www.enri.go.jp/eng/index.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

ENRI 是日本在航空交通管理与通信导航监视（ATM/CNS）领域的国家级研究机构英文门户，涵盖电子航法与相关 GNSS/增强研究入口。官方 portal；适合查日方航空导航与完好性研究方向。具体报告与数据分发条款以各子页为准，非 CORS 下载站。

#### [GA-Positioning-Services](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/services-and-tools)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

澳大利亚定位项目服务总览，含 SouthPAN、GNSS 数据中心与 AUSPOS 在线处理等入口。多数为在线服务而非本地开源库，与 Ginan 开源套件互补。查找国家级数据流、改正服务与在线 PPP 时可作为官方导航页。使用前请核验上游页面与许可条款。

#### [GPS.gov](https://www.gps.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GPS.gov 是美国面向公众的 GPS 系统官方站点，汇总政策、现代化进展与用户资源入口。官方 portal；与 FAA WAAS、NAVCEN 等互补。技术 ICD 细节多链向其他 .gov 文档，下载、引用与再分发请遵循各目标页条款。

#### [ISRO-IRNSS-NavIC](https://www.isro.gov.in/IRNSS_Programme.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

印度空间研究组织关于 IRNSS（NavIC）区域导航系统的官方计划页，说明服务区、系统目标与计划背景，是了解 NavIC 信号与服务范围的起点。本页不是观测数据下载站；接收机 ICD、开放数据与授权渠道需另循 ISRO 文档。适合多星座与南亚 PNT 调研索引。

#### [NGS-PC-PROD](https://geodesy.noaa.gov/PC_PROD/)  
*🏷️ 官方*

语言：various · 许可：USGov public resource · 星标约：— · 宿主：official_site

NOAA/NGS 大地测量 PC 软件汇总页，链向 HTDP 等可下载程序与文档，是做美国基准与地壳运动相关计算时的官方起点。具体程序许可与源码可用性因条目而异，例如 HTDP 源码已在 GitHub noaa-ngs 组织发布。使用前请核验上游页面与许可条款。

#### [UNAVCO-Software-Portal](https://www.unavco.org/software/)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

GAGE/EarthScope 软件总入口，分数据处理、数据管理、可视化与大地测量工具。可找到 TEQC、Hatanaka/GNSSTK 预处理说明、GAMIT 链接及 GPS Velocity Viewer 等。多数条目指向外部维护方；GAMIT 等为学术许可而非宽松 OSS，下载前请仔细阅读许可条款。

#### [USCG-NAVCEN](https://www.navcen.uscg.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

USCG Navigation Center 官网，发布航海航标、差分 GPS/导航服务公告与相关 GNSS 用户信息入口。官方 portal；偏海事与公共导航服务，不是 CORS RINEX 下载站。运行状态、用户通告与服务变更以站内最新公告为准。

## 高校工具门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gAGE-Software-Tools](https://gage.upc.edu/en/learning-materials/software-tools) | gAGE-Software-Tools：UPC gAGE 教学工具页（gLAB / gAGEbuntu） | various | — | 🏷️ 高校实验室 |

### 详细说明

#### [gAGE-Software-Tools](https://gage.upc.edu/en/learning-materials/software-tools)  
*🏷️ 高校实验室*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

gAGE 组学习材料下的软件工具汇总，指向 gLAB Tool Suite 与 gAGEbuntu Live 环境，是教学实验的一站式入口，便于课程统一环境。具体许可以各下载页为准；Live 镜像体积较大，需预留足够磁盘空间。使用前请核验上游页面与许可条款。

## 轨迹/航点转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSBabel](https://www.gpsbabel.org/) | GPSBabel：航点/轨迹/路线多格式互转与过滤 | C++ | — | 🏷️ 个人社区 |

### 详细说明

#### [GPSBabel](https://www.gpsbabel.org/)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL · 星标约：— · 宿主：other

成熟的开源 GPS 数据转换器，支持大量消费级接收机与地图软件之间的航点、轨迹互转，并提供去重与简化。对测绘级 RINEX/载波相位无助，但野外勘察与 GIS 衔接很实用。主站提供文档与下载；SourceForge 镜像偶发屏蔽时可改用官网通道。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 坐标框架/地壳运动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HTDP](https://github.com/noaa-ngs/HTDP) | HTDP：NOAA/NGS 水平时变坐标与框架变换 | Fortran | 33 | 🏷️ 官方 |

### 详细说明

#### [HTDP](https://github.com/noaa-ngs/HTDP)  
*🏷️ 官方*

语言：Fortran · 许可：other (NOAA/NGS) · 星标约：33 · 宿主：github

美国国家大地测量局官方开源的 Horizontal Time-Dependent Positioning，Fortran 实现地壳运动模型下的坐标时间归算与框架变换。配套用户指南与 NGS 工具页。GNSS 测站坐标比较、CORS 历元统一常用；不处理原始观测，也不是 PPP 软件。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 因子图教程

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ion_gnss25_fg_code_examples](https://github.com/watsonryan/ion_gnss25_fg_code_examples) | ion_gnss25_fg_code_examples：ION GNSS+ 2025 因子图教程 | Python | 7 | 🏷️ 个人社区 |

### 详细说明

#### [ion_gnss25_fg_code_examples](https://github.com/watsonryan/ion_gnss25_fg_code_examples)  
*🏷️ 个人社区*

语言：Python · 许可：see upstream README · 星标约：7 · 宿主：github

配套 ION GNSS+ 2025 因子图教程的 Python 示例，基于 GTSAM 演示多机器人里程计、测距约束及单历元/动态 GNSS 伪距定位。适合学习 FGO 与 GNSS 因子建模。教学代码而非生产定位库；运行需自备 GTSAM Python 绑定与依赖环境。

## PNT仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [kshana](https://github.com/ashfordeOU/kshana) | kshana：开源 PNT 韧性/完好性仿真框架 | Rust | 6 | 🏷️ 个人社区 |

### 详细说明

#### [kshana](https://github.com/ashfordeOU/kshana)  
*🏷️ 个人社区*

语言：Rust · 许可：AGPL-3.0 · 星标约：6 · 宿主：github

覆盖轨道、参考架、DOP、GNSS/INS、ARAIM/SBAS 保护级等的仿真框架，带跨语言绑定。适合完好性与韧性研究。AGPL；项目较新，接口可能变化。

## 课程笔记

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | Navigation-Learning：导航开源项目中文笔记 | — | 2417 | 🏷️ 高校实验室 ★ 核心 |
| [learning_rtklib](https://github.com/libing64/learning_rtklib) | learning_rtklib：RTKLIB 学习笔记 | — | 163 | 🏷️ 个人社区 |
| [RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN) | RTKLIB-Manual-CN：中文手册与源码导读 | — | 54 | 🏷️ 高校实验室 |
| [gnss_tutorials](https://github.com/rokubun/gnss_tutorials) | gnss_tutorials：Rokubun Python/Jupyter GNSS 教程 | Jupyter Notebook | 13 | 🏷️ 个人社区 |
| [DD-cycle-slip-lab](https://github.com/VimsRocz/Double_difference_relative_positioning) | DD-cycle-slip-lab：双差定位与周跳教学实验 | MATLAB | 7 | 🏷️ 高校实验室 |

### 详细说明

#### [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning)  
*🏷️ 高校实验室 ★ 核心*

语言：— · 许可：— · 星标约：2417 · 宿主：github

系统整理 RTKLIB/GAMP/GREAT/Ginan/GINav/GICI 等源码阅读笔记与开源清单，中文学习路径非常完整。适合入门导航软件。笔记非上游文档，实现细节以各项目为准。

#### [learning_rtklib](https://github.com/libing64/learning_rtklib)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：163 · 宿主：github

围绕 RTKLIB 的学习材料/笔记向仓库，降低读 C 代码的门槛。与 Navigation-Learning 互补。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：54 · 宿主：github

系统梳理 RTKLIB 工具使用、算法要点与工程阅读路径的中文笔记，降低中文读者入门与源码导读成本。适合自学、培训与课题组内部分享。不是可执行定位库；内容可能落后于最新 RTKLIB 或 demo5 分支，关键公式与编译选项请回对官方手册与当前源码。

#### [gnss_tutorials](https://github.com/rokubun/gnss_tutorials)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：MIT · 星标约：13 · 宿主：github

Rokubun 编写的 GNSS 数据处理 Jupyter 教程，覆盖从观测到基础解算的示范流程。MIT 许可；与 android_rinex 同机构，适合入门与课堂教学演示。内容随课程版本变化，生产流水线请改用仍在维护的库，并补齐自有质控步骤。

#### [DD-cycle-slip-lab](https://github.com/VimsRocz/Double_difference_relative_positioning)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：7 · 宿主：github

面向双差（DD）相对定位与周跳探测的 Matlab 练习，附带城市环境静态多站 GPS 样例。MIT 许可；适合课程实验理解周跳与相对定位基础。非生产 RTK 引擎，数据与习题步骤绑定仓库说明文档。 细节以官方页面或仓库 README 为准。

## HF传播态势

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Muf_Muncher](https://github.com/mooxle/Muf_Muncher) | Muf_Muncher：自托管欧洲 HF 传播看板（MUF/foF2/POTA） | HTML | 5 | 🏷️ 个人社区 |

### 详细说明

#### [Muf_Muncher](https://github.com/mooxle/Muf_Muncher)  
*🏷️ 个人社区*

语言：HTML · 许可：see upstream README · 星标约：5 · 宿主：github

把两座欧洲测高仪的 MUF(D)、foF2、偶发 E 与 NOAA 空间天气、POTA 激活性汇总成一页 glance-and-go 看板，偏业余无线电运营。相邻域里少见的“开源+可自建”传播态势工具。不是射线追踪引擎；数据源与站点配置面向中欧，搬到其它区域要改接入。

## 网平差

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NGS-ADJUST](https://geodesy.noaa.gov/PC_PROD/ADJUST/) | NGS-ADJUST：NGS 蓝簿 GPS 网最小二乘平差套件（无源免费） | Win32 binaries | — | 🏷️ 官方 |

### 详细说明

#### [NGS-ADJUST](https://geodesy.noaa.gov/PC_PROD/ADJUST/)  
*🏷️ 官方*

语言：Win32 binaries · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

美国 NGS 发布的 ADJUST 及配套 CHKOBS 等 Windows 工具，用于水平/GPS 观测平差与蓝簿数据检查。提供可执行包，不提供源码。面向向 NGS 提交工程的美国用户；一般科研 PPP 或国际测区处理不必依赖本套件。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 教材与工具索引

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Navipedia](https://gssc.esa.int/navipedia/index.php/Main_Page) | Navipedia：ESA GSSC 的 GNSS 参考百科 | data-portal | — | 🏷️ 官方 |
| [NGS-GPS-Toolbox](https://geodesy.noaa.gov/gps-toolbox/) | NGS-GPS-Toolbox：NGS《GPS Toolbox》专栏历史代码索引 | various | — | 🏷️ 官方 |

### 详细说明

#### [Navipedia](https://gssc.esa.int/navipedia/index.php/Main_Page)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心维护的 Navipedia，按主题整理卫星导航概念、系统与算法条目，是公开可编辑风格的 GNSS 参考 Wiki。官方 portal；适合教学查阅与概念对照，条目深度不一，工程实施与接口开发仍应回到 ICD 与正式标准原文核对。

#### [NGS-GPS-Toolbox](https://geodesy.noaa.gov/gps-toolbox/)  
*🏷️ 官方*

语言：various · 许可：varies by article · 星标约：— · 宿主：official_site

国家大地测量局汇集的 GPS Solutions 期刊工具箱文章目录，涵盖 RINEX 类库、模糊度、Klobuchar、轨道插值等经典小品。2024-09 后站点不再直接托管源码，需联系作者或期刊。适合文献溯源与教学对照，不宜当作持续维护的软件发行渠道。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 坐标转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [geodesy-js](https://github.com/chrisveness/geodesy) | geodesy-js：浏览器/Node 可用的 JS 大地测量库 | JavaScript | 1227 | 🏷️ 个人社区 |
| [pymap3d](https://github.com/geospace-code/pymap3d) | 纯 Python 三维坐标转换：ECEF/ENU/ECI 等（geospace） | Python | 445 | 🏷️ 个人社区 |
| [Geodesy.jl](https://github.com/JuliaGeo/Geodesy.jl) | Geodesy.jl：Julia 坐标与大地测量变换库 | Julia | 114 | 🏷️ 个人社区 |
| [ncat-lib](https://github.com/noaa-ngs/ncat-lib) | NGS NCAT Java 库：离线坐标/基准转换 | Java | 21 | 🏷️ 官方 |
| [NGS-NCAT](https://geodesy.noaa.gov/NCAT/) | NGS-NCAT：NOAA/NGS 大地坐标与参考框架在线转换 | web/service | — | 🏷️ 官方 |
| [NRCan-TRX](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/trx.php) | NRCan-TRX：加拿大 CSRS 在线大地坐标/高程转换 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [geodesy-js](https://github.com/chrisveness/geodesy)  
*🏷️ 个人社区*

语言：JavaScript · 许可：MIT · 星标约：1227 · 宿主：github

chrisveness 维护的 JS 大地测量工具集，覆盖常见椭球上的距离、方位与坐标变换，浏览器与 Node 可用。MIT 许可；填补 Web 前端坐标计算缺口。偏通用大地测量，不处理 RINEX/RTK 观测；高精度应用请核对方位约定与椭球参数。

#### [pymap3d](https://github.com/geospace-code/pymap3d)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-2-Clause · 星标约：445 · 宿主：github

geospace-code 维护的纯 Python（可选 Numpy）三维坐标转换库，覆盖 ECEF、ENU、ECI 等常用地空坐标系，BSD-2-Clause，星数高、文档清晰。服务 GNSS/轨道/空间天气几何计算，不做观测解算。API 稳定、依赖少，适合脚本与教学。与精密测地库（如 PROJ）分工不同，偏空间物理常用约定。

#### [Geodesy.jl](https://github.com/JuliaGeo/Geodesy.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：114 · 宿主：github

JuliaGeo 的坐标系统与点位变换库，支持常见大地测量坐标转换。MIT 许可；填补目录 Julia 生态缺口。偏通用大地测量而非 GNSS 观测处理，完整解算请另接 Julia 或其他语言的 GNSS 专用库。 细节以官方页面或仓库 README 为准。

#### [ncat-lib](https://github.com/noaa-ngs/ncat-lib)  
*🏷️ 官方*

语言：Java · 许可：USGov (17 USC 105 / NOAA terms) · 星标约：21 · 宿主：github

NGS 公开的 NCAT（NGS Coordinate Conversion and Transformation Tool）底层 Java 转换模块库，可用 Ant 构建 jar，在无网络环境下做坐标与基准转换（NADCON/VERTCON 格网需另从 NCAT 站点下载）。美国政府雇员作品在美不受版权限制（17 U.S.C. §105），并对外提供免版税非独占许可（仓库 SPDX 标为 NOASSERTION/other）。与已收录的 NGS-NCAT 网页工具互补（网页 vs 可嵌入库）。不是 GNSS 观测解算器。

#### [NGS-NCAT](https://geodesy.noaa.gov/NCAT/)  
*🏷️ 官方*

语言：web/service · 许可：USGov public resource · 星标约：— · 宿主：official_site

国家大地测量局坐标转换与变换工具，支持多种美国大地基准与框架之间的点位转换。以 Web/服务形式提供，便于把 GNSS 成果归算到所需基准。不是观测处理软件；与 HTDP、VDATUM 等 NGS 工具链互补，做美国测区成果交付时常一起查阅。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [NRCan-TRX](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/trx.php)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

自然资源部 CSRS 在线工具，支持加拿大常用大地基准与高程系统之间的坐标转换，常与 CSRS-PPP 成果后处理衔接。面向工程与科研用户的浏览器表单，无需自建 PROJ 管线即可完成官方参数转换。参数与历元选择会影响结果，跨海或旧历元需核对说明。收录前已 HTTP 200 核验；请遵守 NRCan 服务条款。

## 认证/完好性

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [galileo-osnma](https://github.com/daniestevez/galileo-osnma) | galileo-osnma：嵌入式友好的 Galileo OSNMA Rust 库 | Rust | 88 | 🏷️ 个人社区 |
| [OSNMA](https://github.com/Algafix/OSNMA) | OSNMA：Galileo 开放业务认证 Python 实现 | Python | 52 | 🏷️ 高校实验室 |
| [gal-osnma-sim](https://github.com/galileoz/gal-osnma-sim) | gal-osnma-sim：Galileo OSNMA 开源仿真器 | C | 31 | 🏷️ 个人社区 |
| [GSC-OSNMA-Service](https://www.gsc-europa.eu/galileo/services/galileo-open-service-navigation-message-authentication-osnma) | GSC OSNMA：Galileo 导航电文认证官方服务页 | data-portal | — | 🏷️ 官方 |
| [GSC-Programme-Reference-Documents](https://www.gsc-europa.eu/electronic-library/programme-reference-documents) | GSC 参考文件：Galileo/EGNOS ICD 与计划文档 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [galileo-osnma](https://github.com/daniestevez/galileo-osnma)  
*🏷️ 个人社区*

语言：Rust · 许可：Apache-2.0 · 星标约：88 · 宿主：github

daniestevez 维护的 Galileo OSNMA 协议 Rust 库，校验导航电文密码学签名，支持 no_std 与静态栈分配，并有嵌入式演示 crate。与 Algafix/OSNMA（EUPL、偏仿真/工具链）互补，侧重可嵌入接收机路径。Apache-2.0/MIT；需自备公钥/ Merkle 材料与实时电文源，星级与文档见 crates.io/docs.rs。

#### [OSNMA](https://github.com/Algafix/OSNMA)  
*🏷️ 高校实验室*

语言：Python · 许可：EUPL-1.2 · 星标约：52 · 宿主：github

实现 Galileo 开放业务消息认证（OSNMA），用于抗欺骗研究与接收机试验。适合安全/完好性方向。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [gal-osnma-sim](https://github.com/galileoz/gal-osnma-sim)  
*🏷️ 个人社区*

语言：C · 许可：MIT · 星标约：31 · 宿主：github

galileoz 的 Galileo OSNMA 仿真工具，用于生成/演练开放服务导航电文认证场景，便于测试认证链路。MIT 许可；与 Algafix/OSNMA、daniestevez/galileo-osnma 形成仿真—实现互补。偏研究与联调，非飞行级密钥管理；密钥材料与配置步骤以仓库文档为准，勿与生产公钥混用。

#### [GSC-OSNMA-Service](https://www.gsc-europa.eu/galileo/services/galileo-open-service-navigation-message-authentication-osnma)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GSC 关于 Galileo Open Service Navigation Message Authentication（OSNMA）的官方服务页，说明认证服务目标、状态与开发者资源入口。与 Algafix/OSNMA、galileo-osnma 代码条目互补；密钥与测试向量获取路径以站内指引为准，实施须遵循 GSC 条款。

#### [GSC-Programme-Reference-Documents](https://www.gsc-europa.eu/electronic-library/programme-reference-documents)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲 GNSS 服务中心电子图书馆中的 Programme Reference Documents，集中链向 Galileo/EGNOS 接口控制文件与计划级参考文档。官方 portal；做接收机/OSNMA/HAS 开发前的权威文档入口。具体 PDF 版本与下载条款以页面为准，需遵守欧盟文件分发条件。

## RTK网络客户端

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [polaris](https://github.com/PointOneNav/polaris) | polaris：Point One RTK 网络服务通信客户端 | — | 33 | 🏷️ 个人社区 |

### 详细说明

#### [polaris](https://github.com/PointOneNav/polaris)  
*🏷️ 个人社区*

语言：— · 许可：MIT · 星标约：33 · 宿主：github

与 Point One 的 RTK 网络服务通信的开源客户端侧代码，便于接云端改正。服务本身非开源；适合对接其生态。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## SWARM教程

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Swarm_notebooks](https://github.com/Swarm-DISC/Swarm_notebooks) | Swarm_notebooks：ESA Swarm 科学分析 Jupyter 示例 | Jupyter Notebook | 10 | 🏷️ 官方 |

### 详细说明

#### [Swarm_notebooks](https://github.com/Swarm-DISC/Swarm_notebooks)  
*🏷️ 官方*

语言：Jupyter Notebook · 许可：MIT · 星标约：10 · 宿主：github

部署在 VirES VRE 上的官方示例笔记本集合，含 EFIx_LP_1B、TECxTMS_2F 等演示，适合跟着学 Swarm 电离层产品字段与绘图。教学与快速原型友好。依赖 viresclient 与在线环境；不是独立算法库。

## 垂直基准

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [VDATUM](https://vdatum.noaa.gov/) | VDATUM：NOAA 椭球高↔大地水准面/潮汐垂直基准转换 | Java/app | — | 🏷️ 官方 |

### 详细说明

#### [VDATUM](https://vdatum.noaa.gov/)  
*🏷️ 官方*

语言：Java/app · 许可：USGov public resource · 星标约：— · 宿主：official_site

NOAA 垂直基准转换软件与服务，连接椭球高、大地水准面与潮汐等垂直基准，海岸带与 GNSS 高程应用中常用。以官方发布包与 Web 服务为准；与水平框架工具 HTDP、NCAT 分工不同，高程与平面归算请分别选用对应工具。使用前请核验上游页面与许可条款。

## 接收机工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [piksi_tools](https://github.com/swift-nav/piksi_tools) | piksi_tools：Swift Navigation Piksi 接收机 Python 工具 | Python | 36 | 🏷️ 个人社区 |

### 详细说明

#### [piksi_tools](https://github.com/swift-nav/piksi_tools)  
*🏷️ 个人社区*

语言：Python · 许可：LGPL-3.0 · 星标约：36 · 宿主：github

面向 Swift Navigation Piksi 系列的 Python 工具，覆盖配置、日志与常见现场操作，许可证 LGPL-3.0。与 libsbp 消息生态配合，适合已有 Piksi/SBP 设备的工程调试。非通用多品牌 RTK 套件；协议与固件版本需匹配。仓库仍可访问且许可证明确，补齐厂商工具链条目。

## Python工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [swift-nav-pygnss](https://github.com/swift-nav/pygnss) | swift-nav-pygnss：Swift Navigation Python GNSS 实用库 | Python | 24 | 🏷️ 个人社区 |

### 详细说明

#### [swift-nav-pygnss](https://github.com/swift-nav/pygnss)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：24 · 宿主：github

Swift Navigation 维护的 Python GNSS 实用集合，MIT 许可，近年仍有推送。与同组织的 libsbp、piksi_tools 互补，侧重脚本化处理而非完整 PPP 引擎。名称在目录中写作 swift-nav-pygnss，避免与 pygnssutils 等已收录项目混淆。接口随 SBP/固件演进出变更，集成前请读示例与版本说明。

## SBAS用户支持

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ESSP-EGNOS-User-Support](https://egnos-user-support.essp-sas.eu/) | ESSP EGNOS 用户支持站：状态、历史与帮助台入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [ESSP-EGNOS-User-Support](https://egnos-user-support.essp-sas.eu/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲卫星服务商（ESSP）运营的 EGNOS 用户支持门户，提供系统介绍、实时/历史状态、订阅与 7×24 帮助台。与已收录的 EGNOS GSC 门户互补：GSC 偏官方产品与文档，本站偏运行支持与用户服务。登录后可管理订阅；公开页亦可浏览状态摘要。收录前已 HTTP 核验；使用请遵守 ESSP/EUSPA 条款。

## 基准与框架

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [LINZ-Geodetic-System](https://www.linz.govt.nz/guidance/geodetic-system) | LINZ 大地测量系统指南：NZGD 等基准与框架说明 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [LINZ-Geodetic-System](https://www.linz.govt.nz/guidance/geodetic-system)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

LINZ 关于新西兰大地测量系统的指导页，解释基准、框架与使用注意，服务测绘与 GNSS 成果归算用户。偏文档与概念，不替代 PositioNZ 观测下载。与 LINZ-Geodetic 产品页成对：一为服务入口，一为系统说明。收录前已 HTTP 核验；工程采用请对照最新官方通告。

## 地磁模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NOAA-WMM-Portal](https://www.ngdc.noaa.gov/geomag/WMM/) | NOAA/NCEI 世界磁场模型（WMM）官方门户 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [NOAA-WMM-Portal](https://www.ngdc.noaa.gov/geomag/WMM/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国 NCEI 发布的 World Magnetic Model 官方页，提供模型说明、系数与计算入口，支撑磁航向、磁偏角及部分电离层/地磁应用。与已收录的 wmm2020 软件包装互补：本页为权威发布与文档源头。模型有年限与更新周期，工程中勿混用过期系数。收录前已 HTTP 核验；请遵守 NOAA 数据使用说明。

## 航天器态势

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NASA-SSCWeb](https://sscweb.gsfc.nasa.gov/) | NASA SSCWeb：航天器轨道/星下点与坐标服务 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [NASA-SSCWeb](https://sscweb.gsfc.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Satellite Situation Center Web（SSCWeb）提供航天器轨道、星下点与相关坐标查询，便于空间任务与地面 GNSS/电离层观测的几何对照。与 CDAWeb/SPDF 同属 NASA 空间数据体系。收录前已 HTTP 核验；查询结果用于科研时请注明服务与历元。

## 空间天气API

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SWPC-Services](https://services.swpc.noaa.gov/) | NOAA SWPC 机器可读服务目录（JSON/NetCDF/产品） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [SWPC-Services](https://services.swpc.noaa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

SWPC 对外提供的服务根目录，索引 experimental、json、netcdf、products 等机器可读空间天气产品路径。便于脚本拉取指数、通量与相关产品，与已收录的 GloTEC 等具体产品页互补。目录本身无文档正文，具体端点以子路径为准。收录前已 HTTP 核验；高频抓取请遵守 NOAA 使用政策。

## ESA导航

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ESA-Satellite-Navigation](https://www.esa.int/Applications/Satellite_navigation) | ESA 卫星导航应用总入口：Galileo/EGNOS/NAVISP 等 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [ESA-Satellite-Navigation](https://www.esa.int/Applications/Satellite_navigation)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲航天局卫星导航应用门户，汇总 Galileo、EGNOS、NAVISP、月球导航等项目新闻与介绍。偏政策与工程进展导航，具体 ICD/服务细节仍走 GSC 等站点。与已收录的 GSC 产品页形成官方叙事互补。收录前已 HTTP 核验；引用请注明 ESA 页面与日期。

## GPS驯服钟

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gpsdo](https://github.com/dfannin/gpsdo) | gpsdo：Arduino GPS 驯服振荡器（10 MHz 等） | C++ | 44 | 🏷️ 个人社区 |

### 详细说明

#### [gpsdo](https://github.com/dfannin/gpsdo)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：44 · 宿主：github

基于 Arduino 的 GPS Disciplined Oscillator 项目，输出 10 MHz 等参考频率，MIT 许可。服务实验室时间/频率同步，属 GNSS 定时应用而非定位解算。硬件锁相与天线质量决定稳定度。适合业余无线电与测试台时钟源。

## 地磁门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NGDC-Geomagnetism](https://www.ngdc.noaa.gov/geomag/geomag.shtml) | NOAA NCEI 地磁学门户：模型、数据与服务入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [NGDC-Geomagnetism](https://www.ngdc.noaa.gov/geomag/geomag.shtml)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NCEI Geomagnetism 主页，汇总地磁模型、数据、制图与监测服务入口；已收录 WMM 门户可由此发现更多地磁产品。对磁航向与部分电离层/空间天气应用有关。请遵守 NOAA 数据使用说明。收录前已用 HTTP 核验页面或仓库可访问；使用请遵守上游许可证与引用要求。
