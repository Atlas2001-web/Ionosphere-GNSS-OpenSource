# Ionosphere-GNSS-OpenSource

**电离层 · 对流层 · GNSS · 导航（PNT）开源软件与数据入口精选索引**  
Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation — software **and** data portals

[![Projects](https://img.shields.io/badge/verified%20projects-678-blue.svg)](./PROJECTS.json)
[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Data portals](https://img.shields.io/badge/gnss%20datasets-68-teal.svg)](./lists/10-gnss-datasets.md)

> **这是链接索引（curated index），不是代码大合集。**  
> 所有条目均为已核对的公开 URL；需要时请前往**上游**克隆/下载并遵守其许可证与数据政策。

---

## 三条路径（先选路，再点进列表）

| 路径 | 你现在的目标 | 先打开 |
|:---:|---|---|
| **A. 学概念** | 弄清 TEC、双频、GIM、闪烁在说什么 | [教程目录](./docs/tutorials/README.md) → 从 `01-ionosphere-tec-basics.md` 起 |
| **B. 下数据** | 要 RINEX / SP3 / IONEX / CORS / 实时流 / 地磁指数 | [数据获取说明](./docs/data-access.md) → [10-gnss-datasets.md](./lists/10-gnss-datasets.md) |
| **C. 选软件** | 要算 TEC、PPP/RTK、NTRIP、SDR、手机原始观测 | 下方分类表 → 对应 `lists/*.md` |

一分钟自测：只有观测文件、还没有产品 → **B**；已有 RINEX、要 STEC/VTEC → **C** 的电离层列表；连术语都不熟 → **A**。

---

## 如何使用

1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  
2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  
3. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json)  
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
| 核心 / 精选 | 建议优先阅读 |

来源统计：官方 **166** · 高校实验室 **200** · 个人社区 **312**

---

## 分类一览

| 分类 | 适合谁 | 列表 | 数量 |
|---|---|---|---:|
| **电离层** `ionosphere` | STEC/VTEC、GIM、IRI/NeQuick、ROTI/闪烁/层析 | [01-ionosphere.md](./lists/01-ionosphere.md) | 232 |
| **对流层** `troposphere` | ZTD/PWV、VMF/GPT、GNSS-IR、中性大气模式 | [02-troposphere.md](./lists/02-troposphere.md) | 32 |
| **GNSS 数据与格式** `gnss-data` | RINEX/SP3/CLK、RTCM/NTRIP、下载与质检 | [03-gnss-data.md](./lists/03-gnss-data.md) | 101 |
| **精密定位** `gnss-positioning` | SPP/RTK/PPP、网络 RTK、因子图 | [04-gnss-positioning.md](./lists/04-gnss-positioning.md) | 76 |
| **轨道与钟差** `orbit-clock` | 精密轨道、钟差、UPD/OSB 产品链 | [05-orbit-clock.md](./lists/05-orbit-clock.md) | 13 |
| **导航** `navigation-ins` | GNSS/IMU/视觉组合、车载与机器人 | [06-navigation-ins.md](./lists/06-navigation-ins.md) | 55 |
| **软件接收机与信号** `gnss-sdr` | IQ→PVT、信号仿真与 Docker 试用 | [07-gnss-sdr.md](./lists/07-gnss-sdr.md) | 58 |
| **移动与嵌入式应用** `mobile-apps` | 手机原始测量、嵌入式记录与简易定位 | [08-mobile-apps.md](./lists/08-mobile-apps.md) | 14 |
| **学习资源与工具** `tools-learning` | awesome、笔记、可视化、SBAS 学习 | [09-tools-learning.md](./lists/09-tools-learning.md) | 29 |
| **GNSS 数据源** `gnss-datasets` | 观测/产品/CORS/实时流/空间天气数据门户 | [10-gnss-datasets.md](./lists/10-gnss-datasets.md) | 68 |
| **合计** | | [`PROJECTS.json`](./PROJECTS.json) | **678** |

---

## 本轮增量（精选）

**软件：** millipede-caster · ntripbrowser · NTRIPcaster-python · Caster_Project · NtripCore · ntripCaster-go · doris-rinex · cddis-highrate-downloader · docker-gnsssdr · libsbp · msise00 · GNSS_MobileCalculator · androidGnss · NTRIP_ROS  

**数据门户 / 下载说明：** Kyoto-WDC-Geomagnetism · INTERMAGNET · SuperMAG · GeoNet-NZ-Geodetic · IBGE-RBMC · IGS-Files-CDN · ISMR-Query-Tool · CDDIS-Highrate-GNSS  

完整分析见对应 `lists/*.md`。贡献方式见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 许可

本目录文本与结构化元数据以 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 奉献至公有领域。各上游软件与数据仍遵循其自有许可与获取条款。
