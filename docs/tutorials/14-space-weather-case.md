# 14 · 空间天气复盘课：如何「读」一次磁暴里的 TEC

不编造某日具体数字；给你一套**可重复的复盘步骤**。精通标志：能独立按清单出对比图并写半页结论。

## 步骤清单

1. **选事件**：从 NOAA/SWPC 或文献常用事件表选一次 CME/磁暴（记下 SYM-H、Kp、耀斑等级）。
2. **下产品**：
   - IGS GIM（`CDDIS-IONEX`）安静日 vs 扰动日
   - 可选：`DLR-IMPC` 近实时 TEC/ROTI，ESA TIO 产品
3. **画差分**：扰动日 − 安静日（或减去 27 天前），看增强/耗空出现在哪一地方时扇区。
4. **对照驱动**：太阳风速、Bz、SYM-H 时间序列与 TEC 响应的先后。
5. **多源互证**：有条件加测高仪 foF2、掩星电子密度、ROTI。
6. **写结论模板**：
   - 响应是否全球一致？
   - 主效应在日侧还是夜侧？
   - 产品差异是否大于物理信号？（分析中心之间常有数 TECU 差）

## 本仓库入口

- 数据：[`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)、[`docs/data-access.md`](../data-access.md)
- 软件：IONEX 读写与绘图相关 → `lists/01-ionosphere.md`
- 模式对照：`TIE-GCM` 等（可选）

## 延伸阅读

- [16 一日 TEC 实战](./16-practice-one-day-tec.md) · [15 论文到代码](./15-from-paper-to-code.md)
