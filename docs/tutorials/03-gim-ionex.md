# 03 · GIM 是什么？IONEX 文件里有什么？

先问：**你要的是「一张全球/区域电子含量图」，还是「某一站–星的 STEC 时间序列」？**

- 只要站星 STEC → 上一讲的双频估计够用；
- 要空间连续的 VTEC 场、给别人插值用 → 你面对的是 **GIM**，交换格式常常是 **IONEX**。

---

## GIM：全球（或区域）电离层图

**GIM（Global Ionosphere Map）**：把离散测站估到的 TEC 信息，建成随时间变化的空间图，格网点上通常给 **VTEC**。

谁在做？IGS 及各分析中心（CODE、JPL、UPC、WHU…）例行发布；也有研究组自己的区域 GIM。

类比：气象上的「气温格点图」。单站温度计是 STEC/VTEC 采样；GIM 是插值/建模后的场。

---

## IONEX 文件里有什么（读头就够入门）

**IONEX** 是电离层图的常见交换格式（文本）。打开一个文件，你会看到大致这些块：

1. **头段**  
   - 时间跨度、时间间隔（如 1 h / 2 h）  
   - 经纬度格网定义（起止、步长）  
   - 高度假设（薄壳高度，常见约 450 km 量级，以文件为准）  
   - 指数、基线、分析中心标识等

2. **数据段**  
   - 每个历元一张（或一层）**VTEC 格网**  
   - 数值单位通常是 **0.1 TECU** 量级的整数编码（读软件会还原；以规范与头说明为准）

3. **有时还有**  
   - RMS 格网、差分码偏差相关信息等（视产品而定）

人话：IONEX ≈ 「按时间切片的 VTEC 网格表」+ 足够让你正确解码的元数据。

下载入口示例（本目录已收录）：`CDDIS-IONEX`、`JPL-IONEX-Rapid` 等，见 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)；怎么注册 CDDIS 见 [`docs/data-access.md`](../data-access.md)。

---

## 球谐 vs 格网：两种「建图语言」

| 思路 | 直觉 | 常见产物 |
|---|---|---|
| **格网 GIM** | 直接在经纬网格上给 VTEC | IONEX 格网点 |
| **球谐 / 函数展开** | 用一组全球基函数的系数描述 VTEC 场，需要时再合成到格网 | 系数文件或再导出 IONEX |

球谐像用「少数几个旋钮」描写全球平滑结构，适合全球尺度、存储紧；格网更直观，插值方便，区域加密也常见。

很多流水线是：GNSS STEC → 在穿刺点约束下解球谐或局部基 → 输出格网 IONEX。

---

## 和本目录工具怎么对上号

下面名称均已在 `PROJECTS.json` 中核对：

| 需求 | 条目举例 | 说明 |
|---|---|---|
| **读 IONEX** | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer` | 解析格网、做图或插值 |
| **写 / 整理 IONEX** | `ionex_formatter`、`INX_Editor`、`rtcm2ionex` | 格式化或从其他源生成 |
| **下 IONEX** | `ionex-downloader`；数据源 `CDDIS-IONEX` | 工具 vs 数据门户分开看 |
| **GIM / 球谐建图类** | `mosgim`、`mosgim2`、`m_gim`、`M_GIM`、`GNSS.IonosphereMaps` 等 | 见电离层列表「GIM/球谐映射」等子类 |
| **维护者自有** | `SH-GIM` | 🚩 仅点名：球谐 GIM 的 MATLAB 实现；目录不展开长文 |

读图用 `ionex` 一类；自己从 STEC 建图用 GIM/球谐类；官方产品先下 IONEX 再读——三者不要混成「一个按钮」。

---

## 课堂小练习（思路）

1. 从 CDDIS 拉某一天的 IGS 综合 GIM（IONEX）。  
2. 用 `ionex`（或 `ionex-rs`）读出某经纬点全日 VTEC。  
3. 若你有同站双频 STEC，映射成 VTEC 后对比：差多少 TECU？低仰角时段差是否更大？

---

## 延伸阅读（本仓库）

- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) — IONEX/TEC 图、GIM/球谐映射
- [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) — CDDIS-IONEX 等
- [`docs/data-access.md`](../data-access.md)
- 下一讲：[04-iri-nequick.md](./04-iri-nequick.md)
