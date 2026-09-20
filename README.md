# Ionosphere-GNSS-OpenSource

**电离层 · GNSS · 导航开源索引**（链接精选，不是代码大合集）

[![Projects](https://img.shields.io/badge/verified%20projects-692-blue.svg)](./PROJECTS.json)
[![CC0](https://img.shields.io/badge/catalog-CC0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Datasets](https://img.shields.io/badge/data%20portals-77-teal.svg)](./lists/10-gnss-datasets.md)

<p align="center">
  <img src="./docs/tutorials/images/fig-phenomena-gallery.png" alt="Ionosphere phenomena gallery" width="920"/>
</p>

<p align="center"><sub>上图为本仓自绘示意（日夜 TEC · 气泡闪烁 · TID · Ne 剖面）· CC0 · 非实测产品图</sub></p>

---

## 三条路（先选路）

| | 目标 | 入口 |
|:---:|---|---|
| **A** | 弄懂 TEC / 闪烁 / 磁暴长什么样 | [教程](./docs/tutorials/README.md) · [现象课 19–23](./docs/tutorials/19-phenomena-overview.md) |
| **B** | 下载 RINEX / IONEX / CORS / 实时流 | [数据怎么下](./docs/data-access.md) · [数据源列表](./lists/10-gnss-datasets.md) |
| **C** | 选开源软件动手算 | 下方分类表 · [`PROJECTS.json`](./PROJECTS.json) |

---

## 现象一眼看懂（少字多图）

| 现象 | 图 | 课文 |
|---|---|---|
| 日夜 TEC + EIA | ![](./docs/tutorials/images/fig-tec-day-night.png) | [21 赤道异常](./docs/tutorials/21-equatorial-anomaly-bubbles.md) |
| 等离子体气泡 / 闪烁 | ![](./docs/tutorials/images/fig-scintillation-bubbles.png) | [05 闪烁](./docs/tutorials/05-scintillation-roti.md) · [21](./docs/tutorials/21-equatorial-anomaly-bubbles.md) |
| TID 行波 | ![](./docs/tutorials/images/fig-tid-wavefront.png) | [22 TID](./docs/tutorials/22-tid-traveling-disturbances.md) |
| 磁暴残差 | ![](./docs/tutorials/images/fig-storm-quiet-residual.png) | [20 磁暴](./docs/tutorials/20-storm-tec-analysis.md) |
| 耀斑突增 | ![](./docs/tutorials/images/fig-flare-sudden-ionize.png) | [23 耀斑日食](./docs/tutorials/23-flare-eclipse-special.md) |
| 赤道喷泉 / EIA | ![](./docs/tutorials/images/fig-fountain-eia.png) | [21 赤道异常](./docs/tutorials/21-equatorial-anomaly-bubbles.md) |
| 磁暴多相位 TEC | ![](./docs/tutorials/images/fig-storm-phases-tec.png) | [20 磁暴](./docs/tutorials/20-storm-tec-analysis.md) |
| S4 闪烁 | ![](./docs/tutorials/images/fig-s4-scint.png) | [05 闪烁](./docs/tutorials/05-scintillation-roti.md) |
| 极光椭圆 | ![](./docs/tutorials/images/fig-aurora-oval.png) | [20 磁暴/空间天气](./docs/tutorials/20-storm-tec-analysis.md) |
| 日食 TEC 洞 | ![](./docs/tutorials/images/fig-eclipse-tec-hole.png) | [23 耀斑日食](./docs/tutorials/23-flare-eclipse-special.md) |
| 穿透电场 | ![](./docs/tutorials/images/fig-penetrating-efield.png) | [20 磁暴](./docs/tutorials/20-storm-tec-analysis.md) |
| Ne 高度剖面 | ![](./docs/tutorials/images/fig-ne-profile-layers.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) |
| IPP 穿刺点 | ![](./docs/tutorials/images/fig-ipp-pierce-point.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) |
| Chapman Ne 廓线 | ![](./docs/tutorials/images/fig-chapman-ne.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) · [19](./docs/tutorials/19-phenomena-overview.md) |
| Dst / Kp 时间线 | ![](./docs/tutorials/images/fig-dst-kp-timeline.png) | [20 磁暴](./docs/tutorials/20-storm-tec-analysis.md) |
| 双频 → TEC | ![](./docs/tutorials/images/fig-dualfreq-tec.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) · [02](./docs/tutorials/02-gnss-dualfreq-tec.md) |
| 薄壳映射 M(E) | ![](./docs/tutorials/images/fig-mapping-function.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) |
| ROTI 图示意 | ![](./docs/tutorials/images/fig-roti-map-schematic.png) | [21 赤道异常](./docs/tutorials/21-equatorial-anomaly-bubbles.md) · [19](./docs/tutorials/19-phenomena-overview.md) |
| 相位闪烁时序 | ![](./docs/tutorials/images/fig-phase-scint-time.png) | [21](./docs/tutorials/21-equatorial-anomaly-bubbles.md) · [05](./docs/tutorials/05-scintillation-roti.md) |
| TEC 水平梯度 | ![](./docs/tutorials/images/fig-tec-gradient.png) | [22 TID](./docs/tutorials/22-tid-traveling-disturbances.md) |
| GNSS 频段 | ![](./docs/tutorials/images/fig-gnss-freq-bands.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) |
| DCB 偏差伪装 | ![](./docs/tutorials/images/fig-bias-dcb.png) | [01](./docs/tutorials/01-ionosphere-tec-basics.md) · [02](./docs/tutorials/02-gnss-dualfreq-tec.md) |

配图再生：`python3 scripts/make_phenomena_figs.py` · `python3 scripts/make_supplement_figs.py` · `python3 scripts/make_geom_figs.py` · 来源登记：[SOURCES.md](./docs/tutorials/images/SOURCES.md)

---

## 软件 / 数据分类

| 分类 | 列表 | 数 |
|---|---|---:|
| 电离层 | [01](./lists/01-ionosphere.md) | 234 |
| 对流层 | [02](./lists/02-troposphere.md) | 32 |
| GNSS 数据与格式 | [03](./lists/03-gnss-data.md) | 102 |
| 精密定位 | [04](./lists/04-gnss-positioning.md) | 76 |
| 轨道与钟差 | [05](./lists/05-orbit-clock.md) | 13 |
| 导航 | [06](./lists/06-navigation-ins.md) | 56 |
| 软件接收机 | [07](./lists/07-gnss-sdr.md) | 58 |
| 移动应用 | [08](./lists/08-mobile-apps.md) | 15 |
| 学习工具 | [09](./lists/09-tools-learning.md) | 29 |
| **数据源门户** | [10](./lists/10-gnss-datasets.md) | 77 |
| **合计** | [PROJECTS.json](./PROJECTS.json) | **692** |

标记：🏷️ 官方 / 高校实验室 / 个人社区 · 来源约 官方 172 · 高校 206 · 社区 314

---

## 许可

目录文本与元数据 [CC0](https://creativecommons.org/publicdomain/zero/1.0/)。上游软件与数据仍按各自条款。
