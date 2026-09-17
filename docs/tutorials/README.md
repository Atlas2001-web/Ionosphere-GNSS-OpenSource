# 教学讲解：电离层与 GNSS（配合本仓库）

本系列用**课堂讲课**的方式，把电离层 / TEC / GIM / 经验模型 / 闪烁 / 定位改正 / DCB / 建图 / 层析与同化边界讲清楚，再落到本仓库 `lists/` 里的开源条目。

> 你要解决什么问题？先想清楚，再选工具。  
> 本系列**不替代**上游文档，也不塞公式墙；目标是：零基础读完，能在目录里找对软件，并知道主要误差从哪来。

路径设计：**入门 → 进阶 → 精通·实战**。不必一天读完；按阶段打勾即可。总进度表见 [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md)。

---

## 入门（01–04 · 08）

建立量纲与产品直觉：分清 STEC/VTEC、会读双频思路、会打开 IONEX、知道 IRI/NeQuick 与实测的边界，并学会在本仓库找软件。

| 次序 | 文稿 | 学完应能 |
|:---:|---|---|
| 1 | [01-ionosphere-tec-basics.md](./01-ionosphere-tec-basics.md) | 解释 TEC / STEC / VTEC / TECU；说明 GNSS 为何能测电子含量 |
| 2 | [02-gnss-dualfreq-tec.md](./02-gnss-dualfreq-tec.md) | 说出几何无关、相位平滑、DCB 的直觉步骤；从 RINEX 到 STEC 不迷路 |
| 3 | [03-gim-ionex.md](./03-gim-ionex.md) | 说明 GIM 是什么；IONEX 里有什么；球谐 vs 格网；和目录工具对号 |
| 4 | [04-iri-nequick.md](./04-iri-nequick.md) | 判断何时用 IRI/NeQuick/NeQuick-G，何时必须用实测 |
| 8 | [08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md) | 按「估 TEC / 读 IONEX / 跑 IRI / 下数据 / 看闪烁」找到正确 `lists/` |

**入门出口作业**：完成 [16-practice-one-day-tec.md](./16-practice-one-day-tec.md) **路线 A**（读一天 IONEX 出一张 VTEC 图）。

---

## 进阶（05–07 · 09–10 · 13）

从「会读产品」到「会处理偏差、建图、谈闪烁与定位」；互补观测（测高仪/掩星）开始进入视野。

| 次序 | 文稿 | 学完应能 |
|:---:|---|---|
| 5 | [05-scintillation-roti.md](./05-scintillation-roti.md) | 区分闪烁指数与 TEC 图；知道 ROTI/S4 大致数据需求 |
| 6 | [06-iono-positioning.md](./06-iono-positioning.md) | 说明单频改正、双频消电离层、PPP/RTK 里电离层怎么处理 |
| 7 | [07-ionosonde-occultation.md](./07-ionosonde-occultation.md) | 对比测高仪、GNSS TEC、掩星各看什么高度与物理量 |
| 9 | [09-dcb-biases-deep.md](./09-dcb-biases-deep.md) | 解释 TEC「整段平移」；按科学目标决定 DCB 较真程度 |
| 10 | [10-build-gim-workflow.md](./10-build-gim-workflow.md) | 画出多站→STEC→IPP→VTEC→GIM 流水线，并列出验证清单 |
| 13 | [13-scintillation-modeling.md](./13-scintillation-modeling.md) | 分清监测 vs 仿真；低纬/高纬不套同一规则 |

**进阶出口作业**：路线 B 单站 STEC + 写半页「我的区域 VTEC/GIM 流程」（对照第 10 课清单）。

---

## 精通·实战（11–12 · 14–17）

碰三维/同化的边界、空间天气复盘、论文落地，并用一日实战与总路线图收束。

| 次序 | 文稿 | 学完应能 |
|:---:|---|---|
| 11 | [11-tomography-basics.md](./11-tomography-basics.md) | 说明层析为何病态；列出先验与开源条目边界 |
| 12 | [12-data-assimilation-intro.md](./12-data-assimilation-intro.md) | 画出同化框图；区分经典同化与 ML 预报仓 |
| 14 | [14-space-weather-case.md](./14-space-weather-case.md) | 按清单复盘一次磁暴 TEC（差分 + 驱动 + 多源） |
| 15 | [15-from-paper-to-code.md](./15-from-paper-to-code.md) | 用「落地四问」把论文对到 `PROJECTS.json` 候选 |
| 16 | [16-practice-one-day-tec.md](./16-practice-one-day-tec.md) | 当天跑通公开数据→出图闭环（A/B/C） |
| 17 | [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md) | 按周推进并完成能力检查表 |

**精通出口作业**：一次事件复盘（14）+ 一篇论文差异表（15）+ 路线图自检打勾（17）。

---

## 和 `lists/` 的关系

| 本系列讲的 | 主要去哪份列表 |
|---|---|
| TEC 估计、GIM、IRI/NeQuick、闪烁/ROTI、层析、测高仪相关软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| RINEX 读写、质量检查、格式工具 | [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) |
| RTK / PPP 等定位套件（电离层改正常嵌在里面） | [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) |
| CDDIS IONEX、COSMIC 掩星、GIRO 测高、业务 TEC 等数据源 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 分类白话说明 | [`docs/categories.md`](../categories.md) |
| 怎么下载 IGS / Earthdata 等 | [`docs/data-access.md`](../data-access.md) |

机器可读总表：[`PROJECTS.json`](../../PROJECTS.json)。文中点名的项目名均应与该文件中的 `name` 字段一致。

---

## 怎么读才不懵

1. **先问问题**：画 TEC 图？改正单频伪距？研究赤道闪烁？复盘磁暴？  
2. **再建立量纲**：STEC、VTEC、TECU、S4、ROTI、DCB 各是什么量。  
3. **最后打开 list**：按子类挑上游仓库去克隆；先复现量级与形态，再追绝对精度。  

标记说明见仓库根 [`README.md`](../../README.md)（官方 / 高校实验室 / 个人社区；🚩 为维护者自有，目录只收录链接、不写长分析）。

---

## 延伸阅读（本仓库）

- [分类说明](../categories.md)
- [数据获取说明](../data-access.md)
- [电离层软件列表](../../lists/01-ionosphere.md)
- [总路线图 17](./17-roadmap-beginner-to-expert.md)


## 现象分析（必读，不只是建模）

建模告诉你「怎么算数」；现象分析告诉你「天上发生了什么、图上该怎么读」。

| 课 | 文稿 | 你学完能做什么 |
|:---:|---|---|
| 19 | [现象分析总览](./19-phenomena-overview.md) | 分清建模 vs 现象分析；安静/扰动；先看哪些观测量 |
| 20 | [磁暴与 TEC](./20-storm-tec-analysis.md) | 正/负相暴；GIM 差分图；地磁指数对齐 |
| 21 | [赤道异常与气泡](./21-equatorial-anomaly-bubbles.md) | EIA 双峰；气泡/羽状结构；TEC/ROTI 判读 |
| 22 | [TID 行进扰动](./22-tid-traveling-disturbances.md) | 波状 TEC 残差；周期/空间尺度直觉 |
| 23 | [耀斑与日食](./23-flare-eclipse-special.md) | 突增/日食空洞；高采样 GNSS 分析套路 |

> 21–23 若链接暂时 404，表示还在写入；19–20 已可用。01–08 已加入「现象向」质控与读图清单。

