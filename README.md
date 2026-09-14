# Ionosphere-GNSS-OpenSource

**电离层 · 对流层 · GNSS · 导航（PNT）开源软件精选索引**  
Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation

[![Projects](https://img.shields.io/badge/verified%20projects-207-blue.svg)](./PROJECTS.json)
[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

> **这是链接索引（curated index），不是代码大合集。**  
> 所有条目均为已核对的公开 URL；需要时请前往**上游仓库**克隆并遵守其许可证。

---

## 亮点：自有项目 SH-GIM

| | |
|---|---|
| **项目** | [Atlas2001-web/SH-GIM](https://github.com/Atlas2001-web/SH-GIM) |
| **一句话** | 基于球谐展开的全球电离层映射（GIM）MATLAB 源码 |
| **语言 / 许可** | MATLAB · MIT |
| **定位** | 本索引「电离层 / GIM」类别下的**旗舰自有项目** |

从事 GIM / TEC 球谐建模时，建议优先阅读 SH-GIM，并对照 MosGIM2、PyTECGg、gnss-tec、tec-suite 与 IONEX 工具。

---

## 如何使用

1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  
2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  
3. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json) · 扩充研究稿：[`research/expanded_projects.json`](./research/expanded_projects.json)  
4. 克隆上游，不要把第三方源码拷进本仓库

### 标记

| 标记 | 含义 |
|:---:|---|
| 🚩 | Atlas2001-web 自有公开仓库 |
| 🔀 | 维护者已 fork（表中列上游；fork 地址见项目页） |
| ★ | 维护者 GitHub 星标种子 |
| 核心 | 建议优先阅读 |

---

## 分类一览

| 分类 | 适合谁 | 列表 | 数量 |
|---|---|---|---:|
| **电离层** `ionosphere` | 研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与… | [01-ionosphere.md](./lists/01-ionosphere.md) | 37 |
| **对流层** `troposphere` | 中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，… | [02-troposphere.md](./lists/02-troposphere.md) | 13 |
| **GNSS 数据与格式** `gnss-data` | RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与… | [03-gnss-data.md](./lists/03-gnss-data.md) | 31 |
| **精密定位** `gnss-positioning` | SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优… | [04-gnss-positioning.md](./lists/04-gnss-positioning.md) | 30 |
| **轨道与钟差** `orbit-clock` | 精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。 | [05-orbit-clock.md](./lists/05-orbit-clock.md) | 2 |
| **导航 / GNSS-INS** `navigation-ins` | GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。 | [06-navigation-ins.md](./lists/06-navigation-ins.md) | 27 |
| **软件接收机与信号** `gnss-sdr` | 从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。 | [07-gnss-sdr.md](./lists/07-gnss-sdr.md) | 48 |
| **移动与嵌入式应用** `mobile-apps` | 手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。 | [08-mobile-apps.md](./lists/08-mobile-apps.md) | 8 |
| **学习资源与工具** `tools-learning` | awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。 | [09-tools-learning.md](./lists/09-tools-learning.md) | 11 |
| **合计** | | [`PROJECTS.json`](./PROJECTS.json) | **207** |

---

## 电离层 / Ionosphere

研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

完整列表与逐项分析 → [01-ionosphere.md](./lists/01-ionosphere.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 球谐展开全球电离层图（GIM）MATLAB 实现 | 🚩 自有 · 核心 |
| [gnss-tec](https://github.com/gnss-lab/gnss-tec) | 由 RINEX 载波/伪距重建斜路径 TEC | 核心 |
| [PyIRI](https://github.com/victoriyaforsythe/PyIRI) | 国际参考电离层 IRI 的纯 Python 实现 | 核心 |
| [NequickG](https://github.com/tpl2go/NequickG) | Galileo NeQuick-G 电离层模型 Python 实现 | 核心 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python+Rust） | 🔀 Fork · ★ Star · 核心 |
| [OASIS](https://github.com/giorgiopicanco/OASIS) | 从 RINEX 计算 ROTI/ΔTEC/SIDX 等扰动指标 | 核心 |
| [iri2016](https://github.com/space-physics/iri2016) | IRI-2016 的 Python/MATLAB 接口 |  |

## 对流层 / Troposphere

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

完整列表与逐项分析 → [02-troposphere.md](./lists/02-troposphere.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | GNSS-IR：反射信号估水位/土壤湿度/雪深 | 核心 |
| [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc) | 由 GPT/VMF 等计算 GNSS STD/SWD 与模型 ZTD | 核心 |
| [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes) | TU Wien 官方 VMF1/VMF3/GPT 开源代码与格网 | 核心 |
| [PyAPS](https://github.com/insarlab/PyAPS) | 基于全球大气模式的大气相位屏（APS） |  |
| [ICAMS](https://github.com/ymcmrs/ICAMS) | 顾及对流层空间随机特性的 InSAR 大气改正工具箱 |  |
| [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products) | 基于 GGOS/VMF 产品在 RTKLIB 中解算对流层延迟 |  |
| [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS) | TechDemoSat-1 GNSS-R 数据处理示例（SSTL） |  |

## GNSS 数据与格式 / GNSS Data I/O

RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。

完整列表与逐项分析 → [03-gnss-data.md](./lists/03-gnss-data.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gps-measurement-tools](https://github.com/google/gps-measurement-tools) | Google GNSS Logger 与桌面分析套件 | 核心 |
| [georinex](https://github.com/geospace-code/georinex) | 高速 Python RINEX 2/3 NAV/OBS/SP3 读入与 HDF5 转换 | 🔀 Fork · ★ Star · 核心 |
| [FAST](https://github.com/ChangChuntao/FAST) | GNSS 数据下载、质量分析、SPP 与选站 | ★ Star · 核心 |
| [gnsstk](https://github.com/SGL-UT/gnsstk) | 原 GPSTk 演进来的 C++ GNSS 基础库 | 核心 |
| [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software) | GNSS 观测多路径分析 Python 软件 | 核心 |
| [rinex](https://github.com/nav-solutions/rinex) | Rust RINEX 解析/生成与 RINEX-Cli（含 SPP/PPP） | 核心 |
| [Anubis](https://gnutsoftware.com/software/anubis) | RINEX 2/3 质量检查（基础版开源） | 核心 |

## 精密定位 / Precise Positioning

SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

完整列表与逐项分析 → [04-gnss-positioning.md](./lists/04-gnss-positioning.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | 经典开源 GNSS 定位包（RTK/PPP 等） | ★ Star · 核心 |
| [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB) | 面向低成本接收机优化的 RTKLIB 分支 | 核心 |
| [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | 因子图优化的 GNSS 定位与 RTK | 核心 |
| [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR) | 武汉大学 PRIDELab 多星座 PPP 模糊度固定 | ★ Star · 核心 |
| [ginan](https://github.com/GeoscienceAustralia/ginan) | Geoscience Australia 精密定位与改正数工具包 | 核心 |
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | goGPS MATLAB：低成本 GNSS 增强定位 | ★ Star · 核心 |
| [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT) | 武汉大学 GREAT 组精密定位与导航软件 | ★ Star · 核心 |

## 轨道与钟差 / Orbit & Clock

精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。

完整列表与逐项分析 → [05-orbit-clock.md](./lists/05-orbit-clock.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [cggtts](https://github.com/nav-solutions/cggtts) | CGGTTS 远程时间比对解析与调度 |  |
| [rt-clk-service](https://github.com/DoubleString/rt-clk-service) | 实时 GNSS 钟差/轨道/UPD/IFPB 服务相关 |  |

## 导航 / GNSS-INS / Navigation & INS

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

完整列表与逐项分析 → [06-navigation-ins.md](./lists/06-navigation-ins.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gtsam](https://github.com/borglab/gtsam) | GTSAM 平滑与建图因子图库 | 核心 |
| [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim) | GNSS+INS 轨迹与传感器仿真 | 核心 |
| [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS) | 基于 EKF 的 GNSS/INS 组合导航 | 核心 |
| [gici-open](https://github.com/chichengcn/gici-open) | GNSS/INS/相机紧组合开源库 GICI | 核心 |
| [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS) | 基于优化的 GNSS/INS 组合导航 | ★ Star · 核心 |
| [GINav](https://github.com/kaichen686/GINav) | MATLAB GNSS 与 GNSS/INS 组合算法 | ★ Star · 核心 |
| [GVINS](https://github.com/HKUST-Aerial-Robotics/GVINS) | 紧耦合 GNSS-视觉-惯性系统 |  |

## 软件接收机与信号 / GNSS-SDR

从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。

完整列表与逐项分析 → [07-gnss-sdr.md](./lists/07-gnss-sdr.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) | GPS L1 基带信号仿真（SDR 回放） | 核心 |
| [gnss-sdr](https://github.com/gnss-sdr/gnss-sdr) | 开源 GNSS 软件定义接收机 | 核心 |
| [FGI-GSRx](https://github.com/nlsfi/FGI-GSRx) | 芬兰 FGI 多星座 MATLAB 软件接收机 | 核心 |
| [GNSS-SDRLIB](https://github.com/taroz/GNSS-SDRLIB) | 开源 GNSS 软件无线电库 GNSS-SDRLIB |  |
| [BeagleSDRGPS](https://github.com/jks-prv/Beagle_SDR_GPS) | KiwiSDR：BeagleBone 短波 SDR 与软件 GPS（已归档） |  |
| [multi-sdr-gps-sim](https://github.com/Mictronics/multi-sdr-gps-sim) | 多 SDR 平台的 GPS L1 实时 IQ 仿真 |  |
| [GNSS-matlab](https://github.com/danipascual/GNSS-matlab) | MATLAB 生成 GNSS PRN/二级码/无数据信号 |  |

## 移动与嵌入式应用 / Mobile Apps

手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

完整列表与逐项分析 → [08-mobile-apps.md](./lists/08-mobile-apps.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [GPSTest](https://github.com/barbeau/gpstest) | 开源 Android GNSS 测试与原始测量记录 | ★ Star · 核心 |
| [GPSLogger](https://github.com/BasicAirData/GPSLogger) | Android 开源 GPS 轨迹记录器 |  |
| [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer) | ESP8266/ESP32 的 GNSS 授时 NTP/PTP 服务器 |  |
| [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS) | STM32 u-blox GNSS 库（UBX，含 DMA） |  |
| [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare) | 安卓端用原始测量做定位的框架 |  |
| [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker) | STM32 Primer2 平台的 GNSS 轨迹记录器 |  |
| [esp32-gps](https://github.com/mrichar1/esp32-gps) | ESP32 GPS 控制：串口/蓝牙/RTK/NTRIP |  |

## 学习资源与工具 / Learning & Tools

awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。

完整列表与逐项分析 → [09-tools-learning.md](./lists/09-tools-learning.md)

| 项目 | 简介 | 标记 |
|---|---|---|
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | 导航定位开源项目解读与学习笔记（中文） | ★ Star · 核心 |
| [awesome-gnss](https://github.com/barbeau/awesome-gnss) | 开源 GNSS 软件与资源社区列表 | 核心 |
| [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset) | 亚洲城市峡谷多传感器定位数据集 |  |
| [learning_rtklib](https://github.com/libing64/learning_rtklib) | RTKLIB 学习相关材料 |  |
| [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility) | Google Earth 鱼眼可见性分析 |  |
| [OSNMA](https://github.com/Algafix/OSNMA) | Galileo OSNMA 协议 Python 实现 |  |
| [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green) | 由 GNSS 垂直位移反演陆地水储量 GNSS2TWS |  |

---

## 与 Atlas2001-web 的关系

- 🚩 **[SH-GIM](https://github.com/Atlas2001-web/SH-GIM)**：自有旗舰（GIM）
- 🔀 Fork：[PyTECGg](https://github.com/viventriglia/PyTECGg) → [Atlas2001-web/PyTECGg](https://github.com/Atlas2001-web/PyTECGg)；[georinex](https://github.com/geospace-code/georinex) → [Atlas2001-web/georinex](https://github.com/Atlas2001-web/georinex)
- ★ 大量电离层/GNSS 星标已作为种子纳入
- 私有 `SH-GIM-proprietary` **不收录**

## 仓库结构

```
Ionosphere-GNSS-OpenSource/
├── README.md
├── PROJECTS.json
├── NOTES.md / CONTRIBUTING.md
├── docs/categories.md
├── lists/01–09-*.md
└── research/
    ├── expanded_projects.json
    ├── category_plan.md
    └── seed_urls.json
```

## 贡献

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。提交新链接前请确认上游可公开访问，并写清分类与一句话用途。

## 免责声明

本目录仅供信息汇总，不构成对任何项目的背书。无线电信号仿真与发射请遵守当地法规。使用第三方软件的风险由用户自行承担。
