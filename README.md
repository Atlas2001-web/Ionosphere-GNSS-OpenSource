# Ionosphere-GNSS-OpenSource

**电离层 · 对流层 · GNSS · 导航（PNT）开源软件精选索引**  
Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation

[![Projects](https://img.shields.io/badge/verified%20projects-491-blue.svg)](./PROJECTS.json)
[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

> **这是链接索引（curated index），不是代码大合集。**  
> 所有条目均为已核对的公开 URL；需要时请前往**上游仓库**克隆并遵守其许可证。

---

## 如何使用

1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  
2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  
3. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json) · 相似项目检索：[`research/similar_finds.json`](./research/similar_finds.json)  
4. 克隆上游，不要把第三方源码拷进本仓库

### 标记

| 标记 | 含义 |
|:---:|---|
| 🏷️ 官方 | 政府/机构/联盟官方发行 |
| 🏷️ 高校实验室 | 大学课题组维护 |
| 🏷️ 个人社区 | 个人或小团队/社区 |
| 🚩 | 维护者自有公开仓库（仅收录链接，不写详细介绍） |
| 🔀 | 维护者已 fork（表中列上游；fork 地址见项目页） |
| ★ | 维护者 GitHub 星标种子 |
| 核心 | 建议优先阅读 |

来源统计：官方 **114** · 高校实验室 **113** · 个人社区 **264**

---

## 分类一览

| 分类 | 适合谁 | 列表 | 数量 |
|---|---|---|---:|
| **电离层** `ionosphere` | 研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与… | [01-ionosphere.md](./lists/01-ionosphere.md) | 85 |
| **对流层** `troposphere` | 中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，… | [02-troposphere.md](./lists/02-troposphere.md) | 29 |
| **GNSS 数据与格式** `gnss-data` | RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与… | [03-gnss-data.md](./lists/03-gnss-data.md) | 86 |
| **精密定位** `gnss-positioning` | SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优… | [04-gnss-positioning.md](./lists/04-gnss-positioning.md) | 74 |
| **轨道与钟差** `orbit-clock` | 精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。 | [05-orbit-clock.md](./lists/05-orbit-clock.md) | 12 |
| **导航** `navigation-ins` | GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。 | [06-navigation-ins.md](./lists/06-navigation-ins.md) | 54 |
| **软件接收机与信号** `gnss-sdr` | 从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。 | [07-gnss-sdr.md](./lists/07-gnss-sdr.md) | 57 |
| **移动与嵌入式应用** `mobile-apps` | 手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。 | [08-mobile-apps.md](./lists/08-mobile-apps.md) | 11 |
| **学习资源与工具** `tools-learning` | awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。 | [09-tools-learning.md](./lists/09-tools-learning.md) | 27 |
| **GNSS 数据源** `gnss-datasets` | 需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。 | [10-gnss-datasets.md](./lists/10-gnss-datasets.md) | 56 |
| **合计** | | [`PROJECTS.json`](./PROJECTS.json) | **491** |

---

## 电离层 / Ionosphere

研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

完整列表与逐项分析 → [01-ionosphere.md](./lists/01-ionosphere.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现（维护者自有，此处不展开） | 🏷️ 个人社区 · 🚩 |
| [Galileo-NeQuick-G](https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code) | 欧盟 GSC 发布的 Galileo 单频电离层改正 NeQuick G 官方 C 源码 | 🏷️ 官方 · 核心 |
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | 由 RINEX 载波/伪距重建斜路径 TEC | 🏷️ 高校实验室 · 核心 |
| [ionex](https://github.com/gnss-lab/ionex) | Python 读取 IONEX 电离层图文件 | 🏷️ 高校实验室 · 核心 |
| [ionex-rs](https://github.com/nav-solutions/ionex) | Rust 实现的 IONEX 解析与处理 | 🏷️ 个人社区 · 核心 |
| [IRI-2026-package](https://irimodel.org/IRI-2026/) | IRI-2026 官方 Fortran 最新源码包目录 | 🏷️ 官方 · 核心 |
| [IRI-COMMON-FILES](https://irimodel.org/COMMON_FILES/) | 各版 IRI 共用的系数/公共文件目录（官网明确要求另下） | 🏷️ 官方 · 核心 |
| [IRI-Fortran](https://irimodel.org/) | COSPAR/URSI 官方 IRI 经验电离层模型 Fortran 源码与系数包 | 🏷️ 官方 · 核心 |

## 对流层 / Troposphere

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

完整列表与逐项分析 → [02-troposphere.md](./lists/02-troposphere.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | GNSS-IR：反射信号估水位/土壤湿度/雪深 | 🏷️ 高校实验室 · 核心 |
| [mpsim](https://github.com/ufrgs-gnss-lab/mpsim) | UFRGS 开源 GNSS 多路径前向仿真器（Matlab/Octave，近地表反射测量） | 🏷️ 高校实验室 · 核心 |
| [RADIATE](https://github.com/TUW-VieVS/RADIATE) | 维也纳科技大学 VieVS 开源对流层射线追踪（微波/光学，基于数值天气模式） | 🏷️ 高校实验室 · 核心 |
| [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc) | 由 GPT/VMF 等计算 GNSS STD/SWD 与模型 ZTD | 🏷️ 个人社区 · 核心 |
| [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes) | TU Wien 官方 VMF1/VMF3/GPT/GMF 源码与格网目录 | 🏷️ 官方 · 核心 |

## GNSS 数据与格式 / GNSS Data I/O

RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。

完整列表与逐项分析 → [03-gnss-data.md](./lists/03-gnss-data.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [Anubis](https://gnutsoftware.com/software/anubis/) | G-Nut/Anubis：多 GNSS RINEX/RTCM 质量检查（Free 开源） | 🏷️ 个人社区 · 核心 |
| [autorino](https://github.com/IPGP/autorino) | IPGP 开源：自动拉取主流厂商接收机原始数据并转为 RINEX3/4 | 🏷️ 高校实验室 · 核心 |
| [BKG-NtripCaster](https://igs.bkg.bund.de/ntrip/bkgcaster) | BKG 专业 NtripCaster：GPL 开源实时 GNSS 流播发服务器 | 🏷️ 官方 · 核心 |
| [BNC](https://igs.bkg.bund.de/ntrip/bnc) | BKG 开源多流 Ntrip 客户端：收 RTCM 并可做实时 PPP | 🏷️ 官方 · 核心 |
| [caster](https://github.com/Node-NTRIP/caster) | 支持 NTRIP V1/V2 的 Node.js caster 库 | 🏷️ 个人社区 · 核心 |
| [FAST](https://github.com/ChangChuntao/FAST) | GNSS 数据下载、质量分析、SPP 与选站 | 🏷️ 个人社区 · ★ Star · 核心 |
| [georinex](https://github.com/geospace-code/georinex) | 高速 Python RINEX 2/3 NAV/OBS/SP3 读入与 HDF5 转换 | 🏷️ 高校实验室 · 🔀 Fork · ★ Star · 核心 |
| [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software) | GNSS 观测多路径分析 Python 软件 | 🏷️ 个人社区 · 核心 |

## 精密定位 / Precise Positioning

SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

完整列表与逐项分析 → [04-gnss-positioning.md](./lists/04-gnss-positioning.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [B2bLIB](https://github.com/GCCLib/B2bLIB) | 北斗 PPP-B2b 服务研究用的 C/C++ 库 | 🏷️ 个人社区 · 核心 |
| [CLASLIB](https://github.com/QZSS-Strategy-Office/claslib) | 日本内阁府 QZSS 官方 CLAS 厘米级增强测试库（Compact SSR/PPP-RTK） | 🏷️ 官方 · 核心 |
| [cssrlib](https://github.com/hirokawa/cssrlib) | Python 开源 PPP/PPP-RTK 工具包（CLAS/HAS/BDS PPP/IGS SSR） | 🏷️ 高校实验室 · 核心 |
| [ginan](https://github.com/GeoscienceAustralia/ginan) | Geoscience Australia 精密定位与改正数工具包 | 🏷️ 官方 · 核心 |
| [gLAB-UPC](https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite) | UPC gAGE 官方 gLAB：ESA 合同支持的 GNSS 处理与教学套件 | 🏷️ 高校实验室 · 核心 |
| [gnss_lib_py](https://github.com/Stanford-NavLab/gnss_lib_py) | Stanford NAV Lab：GNSS 解析、分析与可视化 | 🏷️ 高校实验室 · 核心 |
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | goGPS MATLAB：低成本 GNSS 增强定位 | 🏷️ 高校实验室 · ★ Star · 核心 |
| [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | 因子图优化的 GNSS 定位与 RTK | 🏷️ 个人社区 · 核心 |

## 轨道与钟差 / Orbit & Clock

精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。

完整列表与逐项分析 → [05-orbit-clock.md](./lists/05-orbit-clock.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [Gkit-Bias](https://github.com/LiZhengXiao99/Gkit-Bias) | 面向全频点 PPP-AR 的开源卫星端偏差估计（DCB/UPD/IFCB 与 OSB 转换） | 🏷️ 个人社区 · 核心 |
| [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE) | 武大 GREAT 团队精密卫星钟差估计软件 | 🏷️ 高校实验室 · 核心 |
| [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD) | 武大 GREAT 开源多星座 UPD（未校准相位延迟）估计软件 | 🏷️ 高校实验室 · 核心 |
| [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT) | GREAT 多星座实时滤波精密定轨（POD）模块 | 🏷️ 高校实验室 · 核心 |
| [SPOCC](https://gnss.gfz.de/services/spocc) | GFZ SPOCC：多 GNSS 精密轨道与钟差加权综合软件 | 🏷️ 官方 · 核心 |

## 导航 / Navigation & INS

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

完整列表与逐项分析 → [06-navigation-ins.md](./lists/06-navigation-ins.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gici-open](https://github.com/chichengcn/gici-open) | GNSS/INS/相机紧组合开源库 GICI | 🏷️ 个人社区 · 核心 |
| [GINav](https://github.com/kaichen686/GINav) | MATLAB GNSS 与 GNSS/INS 组合算法 | 🏷️ 个人社区 · ★ Star · 核心 |
| [GIOW-release](https://github.com/i2Nav-WHU/GIOW-release) | 全轮角/里程计辅助的 GNSS/INS/ODO 组合导航算法发布版 | 🏷️ 高校实验室 · 核心 |
| [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim) | GNSS+INS 轨迹与传感器仿真 | 🏷️ 个人社区 · 核心 |
| [GraphRTK-INS](https://github.com/GREAT-WHU/GraphRTK-INS) | 武大 GREAT 因子图模块：RTK 与惯导紧组合 | 🏷️ 高校实验室 · 核心 |
| [gtsam](https://github.com/borglab/gtsam) | GTSAM 平滑与建图因子图库 | 🏷️ 高校实验室 · 核心 |
| [imu_x_fusion](https://github.com/cggos/imu_x_fusion) | 基于 ESKF/IEKF/UKF 的 IMU+GNSS/里程计松组合 | 🏷️ 个人社区 · 核心 |
| [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS) | 基于 EKF 的 GNSS/INS 组合导航 | 🏷️ 高校实验室 · 核心 |

## 软件接收机与信号 / GNSS-SDR

从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。

完整列表与逐项分析 → [07-gnss-sdr.md](./lists/07-gnss-sdr.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [FGI-GSRx](https://github.com/nlsfi/FGI-GSRx) | 芬兰 FGI 多星座 MATLAB 软件接收机 | 🏷️ 官方 · 核心 |
| [gnss-sdr](https://github.com/gnss-sdr/gnss-sdr) | 开源 GNSS 软件定义接收机 | 🏷️ 高校实验室 · 核心 |
| [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) | GPS L1 基带信号仿真（SDR 回放） | 🏷️ 个人社区 · 核心 |
| [PocketSDR](https://github.com/tomojitakasu/PocketSDR) | Tomoji Takasu 开源 GNSS 软件接收机（多星座多频 SDR） | 🏷️ 个人社区 · 核心 |

## 移动与嵌入式应用 / Mobile Apps

手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

完整列表与逐项分析 → [08-mobile-apps.md](./lists/08-mobile-apps.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [GPSTest](https://github.com/barbeau/gpstest) | 开源 Android GNSS 测试与原始测量记录 | 🏷️ 个人社区 · ★ Star · 核心 |

## 学习资源与工具 / Tools & Learning

awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。

完整列表与逐项分析 → [09-tools-learning.md](./lists/09-tools-learning.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets) | 武大 i2Nav 整理的车载 GNSS/INS 融合公开数据集列表 | 🏷️ 高校实验室 · 核心 |
| [awesome-gnss](https://github.com/barbeau/awesome-gnss) | 开源 GNSS 软件与资源社区列表 | 🏷️ 个人社区 · 核心 |
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | 导航定位开源项目解读与学习笔记（中文） | 🏷️ 个人社区 · ★ Star · 核心 |

## GNSS 数据源 / GNSS Datasets

需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。

完整列表与逐项分析 → [10-gnss-datasets.md](./lists/10-gnss-datasets.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [BKG-IGS-Data-Center](https://igs.bkg.bund.de/) | BKG IGS 数据中心：欧洲侧 GNSS 数据与 NTRIP 入口 | 🏷️ 官方 · 核心 |
| [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/) | 中科院 CAS 电离层 IONEX 产品（data.bdsmart.cn） | 🏷️ 官方 · 核心 |
| [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/) | NASA CDDIS：IGS 全球 GNSS 观测与产品主归档之一 | 🏷️ 官方 · 核心 |
| [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/) | CDDIS IONEX 目录：IGS 及各分析中心全球电离层图 | 🏷️ 官方 · 核心 |
| [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html) | CODE/AIUB 分析中心主页：精密轨道钟差与电离层等产品介绍 | 🏷️ 官方 · 核心 |
| [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/) | COSMIC CDAAC：GNSS 无线电掩星大气/电离层产品 | 🏷️ 官方 · 核心 |
| [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss) | EarthScope GAGE GNSS 归档：北美及合作站观测数据 | 🏷️ 官方 · 核心 |
| [ESA-GSSC](https://gssc.esa.int/) | ESA GNSS Science Support Centre：科学数据与产品门户 | 🏷️ 官方 · 核心 |

---

## 许可

本**目录**以 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 贡献；各上游软件许可证以其仓库为准。
