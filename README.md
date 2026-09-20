# Ionosphere-GNSS-OpenSource

**电离层 · 对流层 · GNSS · 导航开源索引**  
软件 + 数据门户 · [678 项目](./PROJECTS.json) · [CC0](https://creativecommons.org/publicdomain/zero/1.0/)

> **链接索引，不是代码合集。** 条目均为已核对公开 URL；请到**上游**克隆/下载并遵守其许可与数据政策。

![大气分层与电离层高度量级（本仓库自制）](./docs/tutorials/images/fig-atmosphere-layers.png)

---

## 三条路径

| | 目标 | 入口 |
|:---:|---|---|
| **A · 学概念** | TEC、双频、GIM、闪烁 | [教程目录](./docs/tutorials/README.md) |
| **B · 下数据** | RINEX / IONEX / CORS / 实时流 | [数据说明](./docs/data-access.md) · [数据源列表](./lists/10-gnss-datasets.md) |
| **C · 选软件** | TEC · PPP/RTK · NTRIP · SDR | 下方分类 → `lists/*.md` |

术语不熟 → **A** · 只有观测、还没产品 → **B** · 已有 RINEX 要 STEC/VTEC → **C**

![STEC / VTEC 与薄壳几何（本仓库自制）](./docs/tutorials/images/fig-stec-vtec-shell.png)

---

## 分类一览

先扫 [分类说明](./docs/categories.md)，再进对应列表。机器可读：[PROJECTS.json](./PROJECTS.json)。

| 分类 | 适合谁 | 列表 | 数量 |
|---|---|---|---:|
| **电离层** | STEC/VTEC、GIM、IRI、ROTI/闪烁 | [01](./lists/01-ionosphere.md) | 232 |
| **对流层** | ZTD/PWV、VMF、GNSS-IR | [02](./lists/02-troposphere.md) | 32 |
| **GNSS 数据与格式** | RINEX/SP3、RTCM/NTRIP | [03](./lists/03-gnss-data.md) | 101 |
| **精密定位** | SPP/RTK/PPP | [04](./lists/04-gnss-positioning.md) | 76 |
| **轨道与钟差** | 精密轨道、钟差、UPD/OSB | [05](./lists/05-orbit-clock.md) | 13 |
| **导航** | GNSS/IMU/视觉组合 | [06](./lists/06-navigation-ins.md) | 55 |
| **软件接收机** | IQ→PVT、仿真 | [07](./lists/07-gnss-sdr.md) | 58 |
| **移动与嵌入式** | 手机原始测量 | [08](./lists/08-mobile-apps.md) | 14 |
| **学习资源** | awesome、可视化、SBAS | [09](./lists/09-tools-learning.md) | 29 |
| **GNSS 数据源** | 观测/产品/CORS/空间天气 | [10](./lists/10-gnss-datasets.md) | 68 |
| **合计** | | | **678** |

![频率愈高，一阶电离层延迟愈小（本仓库自制）](./docs/tutorials/images/fig-iono-delay-vs-freq.png)

---

## 标记

| 标记 | 含义 |
|:---:|---|
| 🏷️ 官方 / 高校 / 社区 | 来源类型 |
| 🚩 / 🔀 / ★ | 自有仓 · fork · 星标种子 |
| 核心 / 精选 | 建议优先看 |

来源：官方 166 · 高校 200 · 社区 312。贡献见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 许可

目录文本与元数据：[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)。上游软件与数据仍按其自有条款。
