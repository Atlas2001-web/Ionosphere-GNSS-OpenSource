# 分类说明

按「要解决什么问题」划分，不按编程语言。

常见用法：先用数据/格式工具读写 RINEX/RTCM 并质检，再做电离层（TEC/GIM/闪烁）、对流层（ZTD/PWV）或精密定位（RTK/PPP，常配合轨道钟差）；车载/机器人再接 GNSS/INS。另有 GNSS-SDR、手机原始测量 App，以及只提供数据/产品下载的「GNSS 数据源」门户（含电离层产品与空间天气）。

## 来源标记（provenance）

每条项目在 `PROJECTS.json` 中带有 `provenance` 字段，列表里显示为徽章：

| 值 | 徽章 | 含义 |
|---|---|---|
| `official` | 🏷️ 官方 | 政府机构、国家实验室、国际联盟或官方服务站点维护的发行（如 ESA/GSC、BKG、NOAA/NGS、GSI、IGS 工具、TU Wien VMF、GFZ、EarthScope/UNAVCO 等） |
| `academic_lab` | 🏷️ 高校实验室 | 大学或研究所课题组发布、但并非国家测绘/航天主管部门官网的软件（如 UPC gAGE、武大 GREAT、CU Boulder SoftGPS 配套页等） |
| `personal_community` | 🏷️ 个人社区 | 个人开发者、小型社区团队或公司开源档（含 Anubis Free、多数 GitHub 个人仓等） |

另有 `host` 字段标明托管位置：`github` / `gitlab` / `sourceforge` / `official_site` / `other`。

> 同一上游若存在 GitHub 镜像，目录优先保留**官方站点** URL，并在分析中注明镜像。

## `ionosphere` — 电离层

电离层研究软件：GNSS 双频 TEC 估计、GIM/IONEX 处理、TEC 预报（含机器学习）、闪烁/ROTI、TID、层析、掩星与法拉第旋转。也收录 IRI/NeQuick 等电离层模型、MSIS/HWM 中性大气模型、测高仪与雷达/ISR 工具、HF 射线追踪和磁坐标库；电离层产品与空间天气数据门户已移至「GNSS 数据源」。

- 列表文件：[`lists/01-ionosphere.md`](../lists/01-ionosphere.md)
- 当前条目数：**246**

## `troposphere` — 对流层

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

- 列表文件：[`lists/02-troposphere.md`](../lists/02-troposphere.md)
- 当前条目数：**47**

## `gnss-data` — GNSS 数据与格式

RINEX/SP3/CLK/ANTEX 读写与转换、RTCM/NTRIP、Hatanaka 压缩、质量检查/多路径分析、接收机驱动与协议、数据下载脚本——所有解算的上游。

- 列表文件：[`lists/03-gnss-data.md`](../lists/03-gnss-data.md)
- 当前条目数：**138**

## `gnss-positioning` — 精密定位

SPP、DGPS、RTK/PPK、PPP/PPP-AR/PPP-RTK（含 PPP-B2b、Galileo HAS、MADOCA 改正数）、网络 RTK 客户端、RAIM 完好性，以及因子图等现代优化定位。

- 列表文件：[`lists/04-gnss-positioning.md`](../lists/04-gnss-positioning.md)
- 当前条目数：**108**

## `orbit-clock` — 轨道与钟差

精密轨道确定、卫星钟差与相位偏差（UPD/OSB）产品生成，另含 SGP4/轨道根数传播、EOP/VLBI、SLR 与时间比对工具。独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简。

- 列表文件：[`lists/05-orbit-clock.md`](../lists/05-orbit-clock.md)
- 当前条目数：**31**

## `navigation-ins` — 导航

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

- 列表文件：[`lists/06-navigation-ins.md`](../lists/06-navigation-ins.md)
- 当前条目数：**72**

## `gnss-sdr` — 软件接收机与信号

从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。

- 列表文件：[`lists/07-gnss-sdr.md`](../lists/07-gnss-sdr.md)
- 当前条目数：**76**

## `mobile-apps` — 移动与嵌入式应用

手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

- 列表文件：[`lists/08-mobile-apps.md`](../lists/08-mobile-apps.md)
- 当前条目数：**32**

## `tools-learning` — 学习资源与工具

学习资源与通用工具：awesome 列表、课程笔记与教材索引、机构软件门户、坐标转换与基准、可视化、地磁模型，以及 SBAS/认证完好性学习工具。

- 列表文件：[`lists/09-tools-learning.md`](../lists/09-tools-learning.md)
- 当前条目数：**57**

## `gnss-datasets` — GNSS 数据源

数据与产品门户（非软件）：IGS/CORS 观测数据、轨道钟差与偏差产品、实时流、坐标与参考框架。也收录电离层产品（GIM/TEC 图、测高仪数据）以及地磁/空间天气数据门户。

- 列表文件：[`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md)
- 当前条目数：**220**

## 与用户仓库的关系标记

| 标记 | 含义 |
|---|---|
| 🚩 自有 / owned | 维护者自有公开仓库（仅链接，不写详细介绍） |
| 🔀 Fork / fork | 维护者已 fork，表中仍列**上游** URL |
| ★ Star / starred | 出现在维护者 GitHub stars 中的种子 |
| 核心 / core | 本目录推荐优先阅读的代表性项目 |

> 私有仓库（如 `SH-GIM-proprietary`）**不会**出现在公开索引中。
