# 教学讲解：电离层与 GNSS（入门 → 精通）

本系列按**课堂进度**编写：先建立量纲，再动手出图，最后到层析/同化/论文复现与实验课。  
所有章节回链到 `lists/` 开源条目——**先懂问题，再克隆代码**。

> 维护者自有仓库（如 `SH-GIM`）只给链接、不展开细讲。

---

## 学习总览

```
入门 01–04、08        → 分清 TEC/GIM/模型，会在目录找工具
   ↓
进阶 05–07、09–10、13 → 闪烁、定位、DCB、GIM 流水线
   ↓
精通 11–12、14–17     → 层析/同化边界、事件复盘、论文落地、路线图
   ↓
实验 18+              → 用公开产品做对比实验
```

周计划见 [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md)。

---

## 入门

| 课 | 文稿 |
|:---:|---|
| 1 | [电离层与 TEC](./01-ionosphere-tec-basics.md) |
| 2 | [双频估 TEC](./02-gnss-dualfreq-tec.md) |
| 3 | [GIM 与 IONEX](./03-gim-ionex.md) |
| 4 | [IRI / NeQuick](./04-iri-nequick.md) |
| 8 | [怎么用本目录](./08-how-to-use-this-catalog.md) |

---

## 进阶

| 课 | 文稿 |
|:---:|---|
| 5 | [闪烁与 ROTI](./05-scintillation-roti.md) |
| 6 | [定位中的电离层](./06-iono-positioning.md) |
| 7 | [测高仪与掩星](./07-ionosonde-occultation.md) |
| 9 | [DCB / 硬件延迟](./09-dcb-biases-deep.md) |
| 10 | [从多站到 GIM](./10-build-gim-workflow.md) |
| 13 | [闪烁建模](./13-scintillation-modeling.md) |

---

## 精通与实战

| 课 | 文稿 |
|:---:|---|
| 11 | [层析基础](./11-tomography-basics.md) |
| 12 | [同化入门](./12-data-assimilation-intro.md) |
| 14 | [空间天气复盘](./14-space-weather-case.md) |
| 15 | [论文到开源](./15-from-paper-to-code.md) |
| 16 | [一日 TEC 实战](./16-practice-one-day-tec.md) |
| 17 | [总路线图](./17-roadmap-beginner-to-expert.md) |

---

## 实验课

| 课 | 文稿 |
|:---:|---|
| 18 | [三家 GIM 对比实验](./18-lab-compare-gims.md) |

---

## 和 lists/ 的关系

| 内容 | 去哪 |
|---|---|
| TEC/GIM/IRI/闪烁等软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| RINEX 与格式 | [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) |
| RTK/PPP | [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) |
| IONEX/掩星/测高仪数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 分类白话 | [`docs/categories.md`](../categories.md) |
| 下载注册 | [`docs/data-access.md`](../data-access.md) |

总表：[`PROJECTS.json`](../../PROJECTS.json)

---

## 阅读习惯

1. 先写清问题（出图 / 改正 / 闪烁 / 机制）  
2. 再对齐量纲（TECU、S4、ROTI…）  
3. 最后打开 list 克隆上游
