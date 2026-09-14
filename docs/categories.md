# 分类说明（写给初学者）

本索引按「你要解决什么问题」划分，而不是按编程语言。下面用白话说明每一类在 GNSS 工作流里的位置。

```
数据下载/格式(RINEX,RTCM) ──► 质量检查
         │
         ├─► 电离层 TEC/GIM / 闪烁指标
         ├─► 对流层 ZTD/PWV / VMF
         └─► 精密定位 RTK/PPP ──► 轨道钟差产品
                    │
                    └─► GNSS/INS / 视觉组合导航

另线：GNSS-SDR（从无线电采样到伪距/相位）；手机 App（原始测量采集）
```


## `ionosphere` — 电离层

研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。

- 列表文件：[`lists/01-ionosphere.md`](../lists/01-ionosphere.md)
- 当前条目数：**52**

## `troposphere` — 对流层

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

- 列表文件：[`lists/02-troposphere.md`](../lists/02-troposphere.md)
- 当前条目数：**13**

## `gnss-data` — GNSS 数据与格式

RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。

- 列表文件：[`lists/03-gnss-data.md`](../lists/03-gnss-data.md)
- 当前条目数：**56**

## `gnss-positioning` — 精密定位

SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。

- 列表文件：[`lists/04-gnss-positioning.md`](../lists/04-gnss-positioning.md)
- 当前条目数：**55**

## `orbit-clock` — 轨道与钟差

精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。

- 列表文件：[`lists/05-orbit-clock.md`](../lists/05-orbit-clock.md)
- 当前条目数：**6**

## `navigation-ins` — 导航 / GNSS-INS

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

- 列表文件：[`lists/06-navigation-ins.md`](../lists/06-navigation-ins.md)
- 当前条目数：**48**

## `gnss-sdr` — 软件接收机与信号

从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。

- 列表文件：[`lists/07-gnss-sdr.md`](../lists/07-gnss-sdr.md)
- 当前条目数：**53**

## `mobile-apps` — 移动与嵌入式应用

手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

- 列表文件：[`lists/08-mobile-apps.md`](../lists/08-mobile-apps.md)
- 当前条目数：**11**

## `tools-learning` — 学习资源与工具

awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。

- 列表文件：[`lists/09-tools-learning.md`](../lists/09-tools-learning.md)
- 当前条目数：**15**

## 与用户仓库的关系标记

| 标记 | 含义 |
|---|---|
| 🚩 自有 / owned | 维护者自有公开仓库（仅链接，不写详细介绍） |
| 🔀 Fork / fork | 维护者已 fork，表中仍列**上游** URL |
| ★ Star / starred | 出现在维护者 GitHub stars 中的种子 |
| 核心 / core | 本目录推荐优先阅读的代表性项目 |

> 私有仓库（如 `SH-GIM-proprietary`）**不会**出现在公开索引中。
