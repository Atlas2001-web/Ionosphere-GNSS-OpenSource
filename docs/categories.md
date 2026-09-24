# 分类说明

按「要解决什么问题」划分，不按编程语言。

典型路径：数据/格式（RINEX/RTCM）→ 质检 → 电离层 TEC/GIM/闪烁、对流层 ZTD/PWV，或精密定位 RTK/PPP（常配合轨道钟差）；车载/机器人再接 GNSS/INS。另线：GNSS-SDR、手机原始测量 App。

## 来源标记（provenance）

| 值 | 徽章 | 含义 |
|---|---|---|
| `official` | 🏷️ 官方 | 机构/国家实验室/国际联盟官网发行 |
| `academic_lab` | 🏷️ 高校实验室 | 大学或研究所课题组（非主管部门官网） |
| `personal_community` | 🏷️ 个人社区 | 个人、小团队或公司开源档 |

`host`：`github` / `gitlab` / `sourceforge` / `official_site` / `other`。有官方站时优先收录官方 URL。

## `ionosphere` — 电离层

电离层电子含量与扰动：STEC/VTEC、GIM、IRI/NeQuick、ROTI/闪烁与层析。

- 列表：[`lists/01-ionosphere.md`](../lists/01-ionosphere.md)
- 条目：**236**

## `troposphere` — 对流层

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT、PWV、GNSS-IR。

- 列表：[`lists/02-troposphere.md`](../lists/02-troposphere.md)
- 条目：**32**

## `gnss-data` — GNSS 数据与格式

RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka、质检与 IGS 产品下载。

- 列表：[`lists/03-gnss-data.md`](../lists/03-gnss-data.md)
- 条目：**111**

## `gnss-positioning` — 精密定位

SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 与因子图定位。

- 列表：[`lists/04-gnss-positioning.md`](../lists/04-gnss-positioning.md)
- 条目：**82**

## `orbit-clock` — 轨道与钟差

精密轨道、钟差与 UPD/OSB；多数能力在大型套件内，本类保持精简。

- 列表：[`lists/05-orbit-clock.md`](../lists/05-orbit-clock.md)
- 条目：**13**

## `navigation-ins` — 导航

GNSS 与 IMU（及视觉）松/紧组合，车载与机器人户外定位。

- 列表：[`lists/06-navigation-ins.md`](../lists/06-navigation-ins.md)
- 条目：**59**

## `gnss-sdr` — 软件接收机与信号

从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控。

- 列表：[`lists/07-gnss-sdr.md`](../lists/07-gnss-sdr.md)
- 条目：**59**

## `mobile-apps` — 移动与嵌入式应用

手机/嵌入式 GNSS 测试、原始测量记录与简易定位。

- 列表：[`lists/08-mobile-apps.md`](../lists/08-mobile-apps.md)
- 条目：**16**

## `tools-learning` — 学习资源与工具

awesome 列表、源码笔记、可见性可视化、SBAS/认证等学习工具。

- 列表：[`lists/09-tools-learning.md`](../lists/09-tools-learning.md)
- 条目：**31**

## `gnss-datasets` — GNSS 数据源

RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品入口。

- 列表：[`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md)
- 条目：**94**

## 与用户仓库的关系标记

| 标记 | 含义 |
|---|---|
| 🚩 自有 / owned | 维护者自有公开仓（仅链接） |
| 🔀 Fork / fork | 已 fork；表中仍列上游 URL |
| ★ Star / starred | 维护者 stars 中的种子 |
| 核心 / core | 推荐优先阅读的代表项目 |

> 私有仓不会出现在公开索引中。
