# Ionosphere-GNSS-OpenSource

**电离层 · GNSS · 导航（PNT）开源软件精选索引**  
Curated open-source catalog for Ionosphere / TEC / GIM · GNSS processing · Navigation / PNT

[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Projects](https://img.shields.io/badge/verified%20projects-55-blue.svg)](./PROJECTS.json)

> **这是链接索引（curated index），不是把所有代码塞进一个仓库。**  
> This repository collects **verified public URLs** and short bilingual descriptions. Clone the upstream projects you need separately.

---

## 目录 / Contents

- [亮点：SH-GIM](#亮点自有项目-sh-gim)
- [如何使用本仓库](#如何使用本仓库)
- [分类一览](#分类一览)
- [1. 电离层 / Ionosphere](#1-电离层--ionosphere)
- [2. GNSS 数据与格式](#2-gnss-数据与格式--gnss-data--formats)
- [3. GNSS 精密定位](#3-gnss-精密定位--ppp--rtk)
- [4. 导航 / INS](#4-导航--ins--pnt)
- [5. 可视化与教育](#5-可视化与教育)
- [与 Atlas2001-web 的关系](#与-atlas2001-web-的关系)
- [仓库结构](#建议仓库结构)
- [贡献](#贡献)
- [免责声明](#免责声明)

---

## 亮点：自有项目 SH-GIM

| | |
|---|---|
| **项目** | [Atlas2001-web/SH-GIM](https://github.com/Atlas2001-web/SH-GIM) |
| **一句话** | 基于球谐展开的全球电离层映射（GIM）MATLAB 源码 / MATLAB spherical-harmonic global ionospheric mapping |
| **语言** | MATLAB |
| **许可** | MIT |
| **定位** | 本索引在「电离层 / GIM」类别下的 **旗舰自有项目** |

若你从事 GIM / TEC 球谐建模，建议优先阅读 SH-GIM，并对照同目录下的 MosGIM2、IONEX 工具与 TEC 重建库（PyTECGg、gnss-tec、tec-suite 等）。

---

## 如何使用本仓库

1. 浏览下方分类表，或打开 `lists/*.md` 查看完整列表  
2. 机器可读清单见 [`PROJECTS.json`](./PROJECTS.json)  
3. 分类定义见 [`docs/categories.md`](./docs/categories.md)  
4. 需要某项目时，请前往其 **上游 URL** 克隆/引用，遵守其许可证  

### 标记说明

| 标记 | 含义 |
|:---:|---|
| 🚩 自有 | Atlas2001-web 原创公开仓库 |
| 🔀 Fork | 用户已 fork（上游仍列于表中） |
| ★ Star | 来自维护者 GitHub 星标的精选种子 |

---

## 分类一览

| 分类 | 文件 | 数量 |
|---|---|---:|
| 电离层 / Ionosphere | [lists/01-ionosphere.md](./lists/01-ionosphere.md) | 29 |
| GNSS 数据与格式 | [lists/02-gnss-data.md](./lists/02-gnss-data.md) | 6 |
| GNSS 精密定位 | [lists/03-gnss-positioning.md](./lists/03-gnss-positioning.md) | 10 |
| 导航 / INS | [lists/04-navigation-ins.md](./lists/04-navigation-ins.md) | 7 |
| 可视化与教育 | [lists/05-tools-learning.md](./lists/05-tools-learning.md) | 3 |
| **合计** | [`PROJECTS.json`](./PROJECTS.json) | **55** |

---

## 1. 电离层 / Ionosphere

完整列表 → [lists/01-ionosphere.md](./lists/01-ionosphere.md)（下表为精选摘要）

| 项目 | 简介 | 语言 | 标记 |
|---|---|---|---|
| [SH-GIM](https://github.com/Atlas2001-web/SH-GIM) | 基于球谐展开的全球电离层映射（GIM）MATLAB 实现 | MATLAB | 🚩 自有 |
| [PyTECGg](https://github.com/viventriglia/PyTECGg) | 多星座 GNSS TEC 重建与校准（Python + Rust 核心） | Python | 🔀 Fork |
| [IonoMoni](https://github.com/qiliu2025/IonoMoni) | 多星座 ROTI/AATR/STEC/VTEC 电离层监测 | C++ | ★ Star |
| [gnssutils](https://github.com/ljlamarche/gnssutils) | 地基 GNSS 闪烁数据处理工具 | Python | ★ Star |
| [mosgim2](https://github.com/PadArt/mosgim2) | 基于相位差法的 GNSS 全球电离层图（GIM）构建 | Python | ★ Star |
| [M_GIM](https://github.com/zcytju/M_GIM) | 电离层 GIM 相关 MATLAB/工具实现 | — | ★ Star |
| [GNSS.IonosphereMaps](https://github.com/gurkanguldas/GNSS.IonosphereMaps) | GNSS 电离层图生成与处理 | — | ★ Star |
| [INPE-TEC-Maps-IONEX](https://github.com/Hollweg/INPE-TEC-Maps-IONEX) | INPE TEC 图 / IONEX 相关工具 | — | ★ Star |
| [INX_Editor](https://github.com/1acheng/INX_Editor) | IONEX 文件编辑与处理工具 | — | ★ Star |
| [vtec](https://github.com/mfkiwl/vtec) | 垂直 TEC（VTEC）相关计算工具 | — | ★ Star |
| [Get_IPP](https://github.com/Chenjiajun01/Get_IPP) | 电离层穿刺点（IPP）计算 | — | ★ Star |
| [tec_forecast](https://github.com/mauriciodev/tec_forecast) | TEC 预报相关开源项目 | — | ★ Star |

---

## 2. GNSS 数据与格式 / GNSS Data & Formats

完整列表 → [lists/02-gnss-data.md](./lists/02-gnss-data.md)

| 项目 | 简介 | 语言 | 标记 |
|---|---|---|---|
| [georinex](https://github.com/geospace-code/georinex) | Python RINEX 2/3/4 与 SP3 高速读写，可转 HDF5/NetCDF | Python | 🔀 Fork |
| [gnsspy](https://github.com/GNSSpy-Project/gnsspy) | GNSS 数据 Python 工具包（RINEX、SPP、可视化等） | Python | ★ Star |
| [rinex (GNSSNexus)](https://github.com/GNSSNexus/rinex) | Rust RINEX/SP3 解析与处理工具套件 | Rust |  |
| [FAST](https://github.com/ChangChuntao/FAST) | GNSS 数据下载与处理辅助工具 FAST | — | ★ Star |
| [gLAB](https://github.com/valgur/gLAB) | gLAB（UPC）GNSS 精密分析工具的社区镜像/源码 | — | ★ Star |
| [gnsstk](https://github.com/SGL-UT/gnsstk) | 原 GPSTk 后续：开源 GNSS 算法与数据处理库 | C++ |  |

---

## 3. GNSS 精密定位 / PPP · RTK

完整列表 → [lists/03-gnss-positioning.md](./lists/03-gnss-positioning.md)

| 项目 | 简介 | 语言 | 标记 |
|---|---|---|---|
| [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | 经典开源 GNSS 定位软件包（SPP/RTK/PPP 等） | C | ★ Star |
| [RTKLIB (rtklibexplorer)](https://github.com/rtklibexplorer/RTKLIB) | 面向低成本接收机优化的 RTKLIB 分支（尤适 u-blox） | C |  |
| [PRIDE-PPPAR](https://github.com/PrideLab/PRIDE-PPPAR) | 武汉大学多星座 PPP 模糊度固定开源软件 | C | ★ Star |
| [Ginan](https://github.com/GeoscienceAustralia/ginan) | 澳大利亚地球科学署 GNSS 分析中心软件（PPP/POD/大气） | C++ |  |
| [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | 多星座多频 GNSS 观测处理（PPP / 网平差） | MATLAB | ★ Star |
| [GREAT-PVT](https://github.com/GREAT-WHU/GREAT-PVT) | 武汉大学 GREAT 精密定位与导航软件 | C++ | ★ Star |
| [raPPPid](https://github.com/TUW-VieVS/raPPPid) | 维也纳 VieVS 的 PPP 模块（MATLAB） | MATLAB |  |
| [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH) | GAMP PPP 相关开源实现 | — | ★ Star |
| [GROOPS](https://github.com/groops-devs/groops) | 重力场与 GNSS 等地球观测处理软件包 GROOPS | — | ★ Star |
| [GPSPACE](https://github.com/CGS-GIS/GPSPACE) | 加拿大 NRCan GPSPACE（原 CSRS-PPP 引擎源码归档） | — |  |

---

## 4. 导航 / INS · PNT

完整列表 → [lists/04-navigation-ins.md](./lists/04-navigation-ins.md)

| 项目 | 简介 | 语言 | 标记 |
|---|---|---|---|
| [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS) | 武汉大学 i2Nav 开源 GNSS/INS 组合导航 | — | ★ Star |
| [GINav](https://github.com/kaichen686/GINav) | GNSS/INS 组合导航开源软件 GINav | — | ★ Star |
| [ignav](https://github.com/Erensu/ignav) | 惯性/GNSS 导航相关开源项目 | — | ★ Star |
| [gici-open](https://github.com/chichengcn/gici-open) | GNSS/INS/Camera 因子图融合导航库（GICI） | C++ |  |
| [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF) | GREAT 多传感器融合（GNSS/INS 等） | C++ |  |
| [pyins](https://github.com/nmayorov/pyins) | Python INS 建模与 GNSS 辅助卡尔曼滤波 | Python |  |
| [GPSTest](https://github.com/barbeau/gpstest) | Android GNSS 测试与可视化应用 | — | ★ Star |

---

## 5. 可视化与教育

完整列表 → [lists/05-tools-learning.md](./lists/05-tools-learning.md)

| 项目 | 简介 | 语言 | 标记 |
|---|---|---|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | GNSS 干涉反射测量（GNSS-IR）Python 软件 | Python |  |
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | 导航相关学习资料与示例 | — | ★ Star |
| [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) | 软件定义 GPS 信号仿真器（教学/研究常用） | C |  |

---

## 与 Atlas2001-web 的关系

| 仓库 | 关系 | 公开链接 |
|---|---|---|
| **SH-GIM** | 自有 · 旗舰 | https://github.com/Atlas2001-web/SH-GIM |
| **PyTECGg** | Fork（上游 viventriglia/PyTECGg） | https://github.com/Atlas2001-web/PyTECGg |
| **georinex** | Fork（上游 geospace-code/georinex） | https://github.com/Atlas2001-web/georinex |
| SH-GIM-proprietary | 私有 | *不在本公开索引中列出* |

星标种子中的电离层 / GNSS / 导航项目已优先收录，并经 HTTP 可访问性核验。

---

## 建议仓库结构

```text
Ionosphere-GNSS-OpenSource/
├── README.md                 # 本文件（中文优先总览）
├── PROJECTS.json             # 机器可读项目清单
├── CONTRIBUTING.md           # 贡献指南
├── NOTES.md                  # 编纂说明与核验记录
├── docs/
│   └── categories.md         # 分类定义
└── lists/
    ├── 01-ionosphere.md
    ├── 02-gnss-data.md
    ├── 03-gnss-positioning.md
    ├── 04-navigation-ins.md
    └── 05-tools-learning.md
```

---

## 建议的 GitHub 仓库元信息

| 字段 | 建议值 |
|---|---|
| **Repository name** | `Ionosphere-GNSS-OpenSource` |
| **Description** | 电离层/GNSS/导航开源软件精选索引 · Curated index of ionosphere, GNSS & PNT open-source projects |
| **Topics** | `ionosphere`, `tec`, `gim`, `gnss`, `ppp`, `rtk`, `rinex`, `pnt`, `awesome-list` |
| **Visibility** | Public |

---

## 贡献

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。欢迎提交 PR 增补**已核验**的开源项目。

---

## 免责声明

- 本仓库仅提供第三方项目链接与简介，不对其代码质量、许可证合规或科研结论负责。  
- 使用任何上游软件前请自行阅读其 LICENSE 与文档。  
- 未核验存在的 URL 不会收录；若链接失效请提 Issue。  
- 私有/专有仓库不会出现在公开 README 中。

---

## English summary

This is a **Chinese-first curated link catalog** of open-source software for ionospheric science (TEC/GIM/IRI/scintillation), GNSS data formats, precise positioning (PPP/RTK), and navigation (INS/GNSS-INS). It highlights **[SH-GIM](https://github.com/Atlas2001-web/SH-GIM)** and marks forks/stars from Atlas2001-web. See `PROJECTS.json` for the machine-readable list.
