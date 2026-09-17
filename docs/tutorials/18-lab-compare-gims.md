# 18 · 实验课：三家 GIM 比一比

> 前置：[03](./03-gim-ionex.md)、[16](./16-practice-one-day-tec.md)  
> 目标：同一天、同一时刻，比较至少两个 IGS 分析中心的 GIM，量化「产品差」有多大。

---

## 为什么要做这个实验

读论文或做同化时，人们常把某一个 IONEX 当真理。先亲眼看看：**分析中心之间本来就有数 TECU 的差别**。没有这个数感，后面谈「改进了 1 TECU」很容易自嗨。

---

## 步骤

1. 选一个安静日 + 一个扰动日（日期写进笔记）。  
2. 从 `CDDIS-IONEX` 下载至少两家（如 CODE、JPL、CAS 等，以当日实际文件名为准）。  
3. 用本仓库 IONEX 工具读取，插值到同一组经纬网点。  
4. 画：A 图、B 图、A−B 差分图。  
5. 统计：差分的 RMSE、均值、绝对值 >5 TECU 的面积比例。

## 讨论题

- 安静日与扰动日，哪一天中心间差异更大？  
- 差异主要出现在高纬、赤道，还是数据稀疏区？  
- 若你用 GIM 做「真值」评估自建算法，该如何表述不确定性？

## 工具与数据

- [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) · [`docs/data-access.md`](../data-access.md)  
- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) 中 IONEX 读写条目  

## 交什么

两张差分图 + 一张表（RMSE/均值）+ 八句结论。然后可以进入 [14](./14-space-weather-case.md) 做事件复盘。
