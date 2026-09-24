# 学习资源与工具 / Tools & Learning
> **31** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

awesome 列表、源码笔记、可见性可视化、SBAS/认证等学习工具。

## 数据集

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset) | 香港/东京等城市峡谷 GNSS/INS/视觉基准集 | Python | 606 | 🏷️ 高校实验室 |
| [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets) | 武大 i2Nav 整理的车载 GNSS/INS 融合公开数据集列表 | — | 280 | 🏷️ 高校实验室 核心 |
| [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green) | 由 GNSS 垂直位移反演陆地水储量 GNSS2TWS | MATLAB | 33 | 🏷️ 个人社区 |

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
*🏷️ 个人社区*

语言：MATLAB · 许可：GPL-3.0 · 星标约：33 · 宿主：github

开源 MATLAB 工具 GNSS2TWS：利用 GNSS 测站日尺度垂直位移，经格林函数等方法推断陆地水储量（TWS）变化，服务水文大地测量。适合已有精密坐标时间序列、做气候水文交叉的研究者。不是导航定位解算器；空间平滑、负载模型与参考框架假设必须按配套论文核对。输入坐标序列质量决定反演可信度。站点分布稀疏时，反演空间分辨率会明显下降。

## 资源列表

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [awesome-gnss-barbeau](https://github.com/barbeau/awesome-gnss) | Sean Barbeau 维护的开源 GNSS 软件与资源 awesome 列表 | — | 599 | 🏷️ 个人社区 核心 |
| [awesome-gnss-hdkarimi](https://github.com/hdkarimi/awesome-gnss) | hdkarimi：GNSS/RNSS 开源工具、数据与慕课的 awesome 列表 | — | 50 | 🏷️ 个人社区 |

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
| [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility) | Google Earth 鱼眼可见性分析 | MATLAB | 137 | 🏷️ 个人社区 |
| [gnss_timeseries_viewers](https://github.com/kmaterna/gnss_timeseries_viewers) | gnss_timeseries_viewers：PBO/UNR 坐标时序分析绘图 | Python | 36 | 🏷️ 高校实验室 |
| [EasyGNSS](https://github.com/whigg/EasyGNSS) | 面向低成本 GNSS 的图形界面辅助工具 | Python | 4 | 🏷️ 高校实验室 |
| [GPS-Velocity-Viewer](https://www.unavco.org/software/visualization/GPS-Velocity-Viewer/GPS-Velocity-Viewer.html) | UNAVCO GPS 速度场在线可视化查看器 | web | — | 🏷️ 官方 |

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
| [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos/) | SourceForge EGNOS Toolkit：SBAS/EGNOS 消息与接收算法工具 | C/C++ | — | 🏷️ 个人社区 |

### 详细说明

#### [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos/)  
*🏷️ 个人社区*

语言：C/C++ · 许可：EUPL · 星标约：— · 宿主：sourceforge

基于 EGNOS SDK 的 Linux/UNIX 移植，处理 SISNET、EMS 文件并实现用户端 SBAS 算法，许可 EUPL。托管于 SourceForge，更新偏旧。现代多星座 SBAS/HAS 研究需结合新文档与其他开源栈。

## 机构软件门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GA-Positioning-Services](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/services-and-tools) | Geoscience Australia 定位服务与工具门户（SouthPAN/AUSPOS/数据中心） | various | — | 🏷️ 官方 |
| [NGS-PC-PROD](https://geodesy.noaa.gov/PC_PROD/) | NGS PC Software 门户：HTDP 等大地测量桌面程序入口 | various | — | 🏷️ 官方 |
| [UNAVCO-Software-Portal](https://www.unavco.org/software/) | UNAVCO/EarthScope 软件门户：TEQC、预处理、GAMIT 链接与可视化 | various | — | 🏷️ 官方 |

### 详细说明

#### [GA-Positioning-Services](https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/services-and-tools)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

澳大利亚定位项目服务总览，含 SouthPAN、GNSS 数据中心与 AUSPOS 在线处理等入口。多数为在线服务而非本地开源库，与 Ginan 开源套件互补。查找国家级数据流、改正服务与在线 PPP 时可作为官方导航页。使用前请核验上游页面与许可条款。

#### [NGS-PC-PROD](https://geodesy.noaa.gov/PC_PROD/)  
*🏷️ 官方*

语言：various · 许可：USGov public resource · 星标约：— · 宿主：official_site

NOAA/NGS 大地测量 PC 软件汇总页，链向 HTDP 等可下载程序与文档，是做美国基准与地壳运动相关计算时的官方起点。具体程序许可与源码可用性因条目而异，例如 HTDP 源码已在 GitHub noaa-ngs 组织发布。使用前请核验上游页面与许可条款。

#### [UNAVCO-Software-Portal](https://www.unavco.org/software/)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

GAGE/EarthScope 软件总入口，分数据处理、数据管理、可视化与大地测量工具。可找到 TEQC、Hatanaka/GNSSTK 预处理说明、GAMIT 链接及 GPS Velocity Viewer 等。多数条目指向外部维护方；GAMIT 等为学术许可而非宽松 OSS，下载前请仔细阅读许可条款。

## 高校工具门户

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gAGE-Software-Tools](https://gage.upc.edu/en/learning-materials/software-tools) | UPC gAGE 软件工具页：gLAB 套件与 gAGEbuntu 入口 | various | — | 🏷️ 高校实验室 |

### 详细说明

#### [gAGE-Software-Tools](https://gage.upc.edu/en/learning-materials/software-tools)  
*🏷️ 高校实验室*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

gAGE 组学习材料下的软件工具汇总，指向 gLAB Tool Suite 与 gAGEbuntu Live 环境，是教学实验的一站式入口，便于课程统一环境。具体许可以各下载页为准；Live 镜像体积较大，需预留足够磁盘空间。使用前请核验上游页面与许可条款。

## 轨迹/航点转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSBabel](https://www.gpsbabel.org/) | GPSBabel：多品牌接收机航点/轨迹/路线格式互转与过滤 | C++ | — | 🏷️ 个人社区 |

### 详细说明

#### [GPSBabel](https://www.gpsbabel.org/)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL · 星标约：— · 宿主：other

成熟的开源 GPS 数据转换器，支持大量消费级接收机与地图软件之间的航点、轨迹互转，并提供去重与简化。对测绘级 RINEX/载波相位无助，但野外勘察与 GIS 衔接很实用。主站提供文档与下载；SourceForge 镜像偶发屏蔽时可改用官网通道。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 坐标框架/地壳运动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HTDP](https://github.com/noaa-ngs/HTDP) | NOAA/NGS HTDP：跨历元与参考框架的水平时变坐标变换 | Fortran | 33 | 🏷️ 官方 |

### 详细说明

#### [HTDP](https://github.com/noaa-ngs/HTDP)  
*🏷️ 官方*

语言：Fortran · 许可：other (NOAA/NGS) · 星标约：33 · 宿主：github

美国国家大地测量局官方开源的 Horizontal Time-Dependent Positioning，Fortran 实现地壳运动模型下的坐标时间归算与框架变换。配套用户指南与 NGS 工具页。GNSS 测站坐标比较、CORS 历元统一常用；不处理原始观测，也不是 PPP 软件。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 因子图教程

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ion_gnss25_fg_code_examples](https://github.com/watsonryan/ion_gnss25_fg_code_examples) | ION GNSS+ 2025 因子图教程示例（基于 GTSAM：里程计/测距/GNSS 伪距） | Python | 7 | 🏷️ 个人社区 |

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
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | 导航定位开源项目解读与学习笔记（中文） | — | 2417 | 🏷️ 个人社区 ★ 核心 |
| [learning_rtklib](https://github.com/libing64/learning_rtklib) | RTKLIB 学习相关材料 | — | 163 | 🏷️ 个人社区 |
| [RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN) | RTKLIB 中文手册解读与源码解析笔记 | — | 54 | 🏷️ 高校实验室 |

### 详细说明

#### [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning)  
*🏷️ 个人社区 ★ 核心*

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

## HF传播态势

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Muf_Muncher](https://github.com/mooxle/Muf_Muncher) | 自托管欧洲 HF 传播看板（测高仪 MUF/foF2、空间天气与 POTA） | HTML | 5 | 🏷️ 个人社区 |

### 详细说明

#### [Muf_Muncher](https://github.com/mooxle/Muf_Muncher)  
*🏷️ 个人社区*

语言：HTML · 许可：see upstream README · 星标约：5 · 宿主：github

把两座欧洲测高仪的 MUF(D)、foF2、偶发 E 与 NOAA 空间天气、POTA 激活性汇总成一页 glance-and-go 看板，偏业余无线电运营。相邻域里少见的“开源+可自建”传播态势工具。不是射线追踪引擎；数据源与站点配置面向中欧，搬到其它区域要改接入。

## 网平差

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NGS-ADJUST](https://geodesy.noaa.gov/PC_PROD/ADJUST/) | NGS ADJUST 套件：GPS 项目蓝簿提交用最小二乘平差（无源免费） | Win32 binaries | — | 🏷️ 官方 |

### 详细说明

#### [NGS-ADJUST](https://geodesy.noaa.gov/PC_PROD/ADJUST/)  
*🏷️ 官方*

语言：Win32 binaries · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

美国 NGS 发布的 ADJUST 及配套 CHKOBS 等 Windows 工具，用于水平/GPS 观测平差与蓝簿数据检查。提供可执行包，不提供源码。面向向 NGS 提交工程的美国用户；一般科研 PPP 或国际测区处理不必依赖本套件。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 教材与工具索引

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NGS-GPS-Toolbox](https://geodesy.noaa.gov/gps-toolbox/) | NOAA/NGS《GPS Toolbox》专栏历史代码索引（源码已改向作者索取） | various | — | 🏷️ 官方 |

### 详细说明

#### [NGS-GPS-Toolbox](https://geodesy.noaa.gov/gps-toolbox/)  
*🏷️ 官方*

语言：various · 许可：varies by article · 星标约：— · 宿主：official_site

国家大地测量局汇集的 GPS Solutions 期刊工具箱文章目录，涵盖 RINEX 类库、模糊度、Klobuchar、轨道插值等经典小品。2024-09 后站点不再直接托管源码，需联系作者或期刊。适合文献溯源与教学对照，不宜当作持续维护的软件发行渠道。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 坐标转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ncat-lib](https://github.com/noaa-ngs/ncat-lib) | NGS NCAT Java 库：离线坐标/基准转换 | Java | 21 | 🏷️ 官方 |
| [NGS-NCAT](https://geodesy.noaa.gov/NCAT/) | NOAA/NGS NCAT：大地坐标与参考框架转换工具 | web/service | — | 🏷️ 官方 |

### 详细说明

#### [ncat-lib](https://github.com/noaa-ngs/ncat-lib)  
*🏷️ 官方*

语言：Java · 许可：USGov (17 USC 105 / NOAA terms) · 星标约：21 · 宿主：github

NGS 公开的 NCAT（NGS Coordinate Conversion and Transformation Tool）底层 Java 转换模块库，可用 Ant 构建 jar，在无网络环境下做坐标与基准转换（NADCON/VERTCON 格网需另从 NCAT 站点下载）。美国政府雇员作品在美不受版权限制（17 U.S.C. §105），并对外提供免版税非独占许可（仓库 SPDX 标为 NOASSERTION/other）。与已收录的 NGS-NCAT 网页工具互补（网页 vs 可嵌入库）。不是 GNSS 观测解算器。

#### [NGS-NCAT](https://geodesy.noaa.gov/NCAT/)  
*🏷️ 官方*

语言：web/service · 许可：USGov public resource · 星标约：— · 宿主：official_site

国家大地测量局坐标转换与变换工具，支持多种美国大地基准与框架之间的点位转换。以 Web/服务形式提供，便于把 GNSS 成果归算到所需基准。不是观测处理软件；与 HTDP、VDATUM 等 NGS 工具链互补，做美国测区成果交付时常一起查阅。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 认证/完好性

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [OSNMA](https://github.com/Algafix/OSNMA) | Galileo OSNMA 协议 Python 实现 | Python | 52 | 🏷️ 个人社区 |

### 详细说明

#### [OSNMA](https://github.com/Algafix/OSNMA)  
*🏷️ 个人社区*

语言：Python · 许可：EUPL-1.2 · 星标约：52 · 宿主：github

实现 Galileo 开放业务消息认证（OSNMA），用于抗欺骗研究与接收机试验。适合安全/完好性方向。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## RTK网络客户端

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [polaris](https://github.com/PointOneNav/polaris) | Point One RTK 网络服务通信软件 | — | 33 | 🏷️ 个人社区 |

### 详细说明

#### [polaris](https://github.com/PointOneNav/polaris)  
*🏷️ 个人社区*

语言：— · 许可：MIT · 星标约：33 · 宿主：github

与 Point One 的 RTK 网络服务通信的开源客户端侧代码，便于接云端改正。服务本身非开源；适合对接其生态。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## SWARM教程

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Swarm_notebooks](https://github.com/Swarm-DISC/Swarm_notebooks) | ESA Swarm 科学分析 Jupyter 笔记本（含 TEC/Langmuir 示例） | Jupyter Notebook | 10 | 🏷️ 官方 |

### 详细说明

#### [Swarm_notebooks](https://github.com/Swarm-DISC/Swarm_notebooks)  
*🏷️ 官方*

语言：Jupyter Notebook · 许可：MIT · 星标约：10 · 宿主：github

部署在 VirES VRE 上的官方示例笔记本集合，含 EFIx_LP_1B、TECxTMS_2F 等演示，适合跟着学 Swarm 电离层产品字段与绘图。教学与快速原型友好。依赖 viresclient 与在线环境；不是独立算法库。

## 垂直基准

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [VDATUM](https://vdatum.noaa.gov/) | NOAA VDatum：垂直基准面转换工具集 | Java/app | — | 🏷️ 官方 |

### 详细说明

#### [VDATUM](https://vdatum.noaa.gov/)  
*🏷️ 官方*

语言：Java/app · 许可：USGov public resource · 星标约：— · 宿主：official_site

NOAA 垂直基准转换软件与服务，连接椭球高、大地水准面与潮汐等垂直基准，海岸带与 GNSS 高程应用中常用。以官方发布包与 Web 服务为准；与水平框架工具 HTDP、NCAT 分工不同，高程与平面归算请分别选用对应工具。使用前请核验上游页面与许可条款。
