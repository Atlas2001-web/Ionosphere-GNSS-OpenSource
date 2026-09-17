# 07 · 测高仪、GNSS TEC、掩星：各看什么？如何互补？

先问：**你要柱总量，还是高度廓线？要全球稀疏采样，还是某站上空精细结构？**

三种手段看的高度与物理量不同，合在一起才像「立体电离层」。

---

## 一张对比表

| | **测高仪（ionosonde）** | **GNSS TEC** | **GNSS 掩星（RO）** |
|---|---|---|---|
| 几何 | 地基垂直/斜向探测 | 卫星→地面（或 LEO）斜路径 | LEO 看 GNSS，信号掠过地球边缘 |
| 主要量 | 虚高、临界频率、**底部到 F 层峰值**一带的 \(N_e\) 信息 | **STEC/VTEC**（整柱，含上方） | **电子密度廓线**（约从对流层顶到 LEO 高度，视产品） |
| 高度强项 | F2 峰及以下结构清楚 | 柱积分，对峰上等离子体层也敏感 | 廓线连续，全球覆盖好但不均匀 |
| 时间 | 单站可连续 | 有网就连续 | 随轨道「切片」，单点过境短 |
| 局限 | 难直接给峰上全程；覆盖靠台站 | 无高度分辨；要 DCB/映射 | 反演假设、水平平滑；需专业产品链 |

---

## 测高仪：看「头顶剖开」

短波雷达向上打，回波频率与反射高度告诉你各层临界频率等。经典产品：离子图、\(f_oF2\)、\(h_mF2\) 等。

适合：单站暴时响应、层高变化、与 IRI 对比峰值参数。

本目录相关（已核验）：`GIRO-portal`、`GIRO-DIDBase`（数据）、`HamSCI-ionosonde`、`Ionosonde-Data-Downloader`、`Autoscala-INGV`、`SAO-Explorer`、`POLAN` 等 → 软件多在 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)，数据在 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)。

---

## GNSS TEC：看「整柱有多厚」

不分辨高度，但全球地基网密、时间连续，是 GIM 与空间天气监测的主力。

适合：区域/全球 VTEC 图、ROTI、与定位误差联动。

---

## 掩星：看「侧面切一刀的廓线」

COSMIC 等任务提供大量 \(N_e(h)\) 廓线，填测高仪空白洋面，也补 GNSS 柱总量缺高度的短板。

本目录：`COSMIC-CDAAC`、`COSMIC-GNSS-RO-Data`（数据）；`ROM-SAF-ROPP`、`cosmic-crunch`、`CDAAC_COSMIC-TEC_Data-Research`（处理/研究）等。

---

## 互补怎么用（课题级直觉）

```
测高仪  ──► 峰值高度/密度锚点（台站）
掩星    ──► 全球廓线形状与洋面采样
GNSS TEC──► 高时间分辨率柱总量与平面图
    │
    └─► 一起约束 IRI 同化、层析、暴时过程研究
```

写论文时务必写清：对比的是 \(N_e(h_mF2)\)、底部积分 TEC，还是 GNSS 整柱 TEC——**积分上限不同，数值本来就可差一截**。

---

## 延伸阅读（本仓库）

- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) — 测高仪工具、掩星处理、TEC
- [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) — GIRO、COSMIC、CDDIS
- [`docs/data-access.md`](../data-access.md)
- 下一讲：[08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md)
