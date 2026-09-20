# 分类说明

按「你要解决什么问题」划分，**不按编程语言**。徽章与计数与列表页一致。

## 分类一览

| 分类 | 一句话 | 列表 | 数 |
|---|---|---|---:|
| 电离层 | STEC/VTEC、GIM、闪烁与层析 | [01](../lists/01-ionosphere.md) | 232 |
| 对流层 | ZTD/PWV、VMF/GPT、GNSS-IR | [02](../lists/02-troposphere.md) | 32 |
| GNSS 数据与格式 | RINEX/RTCM、质检、产品下载 | [03](../lists/03-gnss-data.md) | 101 |
| 精密定位 | SPP / RTK / PPP / 网络 RTK | [04](../lists/04-gnss-positioning.md) | 76 |
| 轨道与钟差 | 精密轨道、钟差、UPD/OSB（多集成套件） | [05](../lists/05-orbit-clock.md) | 13 |
| 导航 | GNSS/INS、视觉组合 | [06](../lists/06-navigation-ins.md) | 55 |
| 软件接收机 | IQ→PVT、信号仿真 | [07](../lists/07-gnss-sdr.md) | 58 |
| 移动应用 | 手机原始测量、嵌入式 | [08](../lists/08-mobile-apps.md) | 14 |
| 学习工具 | awesome、笔记、可视化 | [09](../lists/09-tools-learning.md) | 29 |
| **数据源门户** | RINEX / IONEX / CORS / 实时流 | [10](../lists/10-gnss-datasets.md) | 68 |

工作流直觉（无流程图）：**数据与格式** 是上游 → 电离层 / 对流层 / 精密定位 并行 → 轨道钟差喂定位 → 导航做组合；另线是 **GNSS-SDR** 与 **手机 App**。

数据怎么下 → [`data-access.md`](./data-access.md)。

## 来源徽章（provenance）

`PROJECTS.json` 的 `provenance` 在列表里显示为：

| 值 | 徽章 | 含义 |
|---|---|---|
| `official` | 🏷️ 官方 | 政府机构、国家实验室、国际联盟或官方服务 |
| `academic_lab` | 🏷️ 高校实验室 | 大学/研究所课题组（非主管部门官网） |
| `personal_community` | 🏷️ 个人社区 | 个人、小型社区或公司开源档 |

`host`：`github` / `gitlab` / `sourceforge` / `official_site` / `other`。

> 同一上游若有 GitHub 镜像，目录优先保留**官方站点** URL。

## 与维护者仓库的关系

| 标记 | 含义 |
|---|---|
| 🚩 自有 / owned | 维护者自有公开仓（仅链接，不展开） |
| 🔀 Fork / fork | 已 fork；表中仍列**上游** URL |
| ★ Star / starred | 出现在维护者 GitHub stars 中的种子 |
| 核心 / core | 建议优先阅读的代表项目 |

> 私有仓库（如 `SH-GIM-proprietary`）**不会**出现在公开索引中。
