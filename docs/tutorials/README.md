# 教学讲解：电离层与 GNSS（入门 → 精通）

本系列按**课堂进度**编写：先建立量纲，再动手出图，最后到层析/同化/论文复现。  
所有章节都回链到本仓库 `lists/` 里的开源条目——**先懂问题，再克隆代码**。

> 维护者自有仓库（如 `SH-GIM`）只给链接、不展开细讲。

---

## 怎么走完这条路

```
入门 01–04、08     →  分清 TEC/GIM/模型，会在目录里找工具
   ↓
进阶 05–07、09–10、13 → 闪烁、定位、DCB、自己理解 GIM 流水线
   ↓
精通 11–12、14–17   → 层析/同化边界、事件复盘、论文落地、一日实战与总图
```

更细的周计划见 [17 · 总路线图](./17-roadmap-beginner-to-expert.md)。

---

## 入门（先建立语言）

| 课 | 文稿 | 学完应能回答 |
|:---:|---|---|
| 1 | [01 电离层与 TEC](./01-ionosphere-tec-basics.md) | TEC / STEC / VTEC / TECU；GNSS 为何能测 |
| 2 | [02 双频估 TEC](./02-gnss-dualfreq-tec.md) | 几何无关组合、相位平滑、DCB 直觉 |
| 3 | [03 GIM 与 IONEX](./03-gim-ionex.md) | GIM 是什么；IONEX 里有什么；和工具怎么对号 |
| 4 | [04 IRI / NeQuick](./04-iri-nequick.md) | 经验模型 vs 实测；何时用哪一种 |
| 8 | [08 怎么用本目录](./08-how-to-use-this-catalog.md) | 按研究问题跳到正确的 `lists/*.md` |

---

## 进阶（能解释误差与流程）

| 课 | 文稿 | 学完应能回答 |
|:---:|---|---|
| 5 | [05 闪烁与 ROTI](./05-scintillation-roti.md) | S4、σφ、ROTI 与 TEC 图的关系 |
| 6 | [06 定位中的电离层](./06-iono-positioning.md) | 单频改正、双频消除、PPP/RTK 里怎么处理 |
| 7 | [07 测高仪与掩星](./07-ionosonde-occultation.md) | 和 GNSS TEC 各看什么高度 |
| 9 | [09 DCB / 硬件延迟](./09-dcb-biases-deep.md) | 为什么绝对 TEC 会整段平移 |
| 10 | [10 从多站到 GIM](./10-build-gim-workflow.md) | 选站→STEC→穿刺点→格网/球谐→验证 |
| 13 | [13 闪烁建模](./13-scintillation-modeling.md) | 监测指数 vs 传播/气候模型 |

---

## 精通与实战

| 课 | 文稿 | 学完应能回答 |
|:---:|---|---|
| 11 | [11 层析基础](./11-tomography-basics.md) | 为何病态；需要什么先验 |
| 12 | [12 同化入门](./12-data-assimilation-intro.md) | 背景场、观测算子、和 ML 预报的差别 |
| 14 | [14 空间天气复盘](./14-space-weather-case.md) | 按清单对比安静日/扰动日 TEC |
| 15 | [15 论文到开源](./15-from-paper-to-code.md) | 读论文四问；如何映射到本目录 |
| 16 | [16 一日 TEC 实战](./16-practice-one-day-tec.md) | 当天跑通「下载→出图」闭环 |
| 17 | [17 总路线图](./17-roadmap-beginner-to-expert.md) | 分阶段目标与 6 周节奏 |

---

## 和 `lists/` 的关系

| 讲的内容 | 主要去哪 |
|---|---|
| TEC / GIM / IRI / 闪烁 / 测高仪相关软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| RINEX 与格式工具 | [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) |
| RTK / PPP | [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) |
| IONEX / 掩星 / GIRO 等数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 分类白话 | [`docs/categories.md`](../categories.md) |
| 下载与注册 | [`docs/data-access.md`](../data-access.md) |

机器可读总表：[`PROJECTS.json`](../../PROJECTS.json)。

---

## 阅读习惯

1. **先写清问题**（出图 / 改正 / 闪烁 / 机制）  
2. **再对齐量纲**（TECU、S4、ROTI…）  
3. **最后才打开 list 克隆上游**

标记含义见根目录 [`README.md`](../../README.md)。
