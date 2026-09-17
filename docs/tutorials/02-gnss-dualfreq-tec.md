# 02 · 双频 GNSS 怎么估 TEC（几何无关、平滑、DCB）

先问：**你手里有什么？**

- 有双频 RINEX 观测 → 可以估 **STEC**；
- 只有单频 → 做不了几何无关 TEC，只能用模型改正（见 [06](./06-iono-positioning.md)）。

本讲讲「从观测到 STEC」的**直觉步骤**，公式少而精，重点是你知道每一步在干什么。

---

## 几何无关组合：把「距离」减掉

伪距 \(P_1, P_2\)（或载波相位）在频率 \(f_1, f_2\) 上。电离层延迟 \(\propto 1/f^{2}\)，几何距离、对流层、钟差等对两频近似相同。

构造**几何无关（geometry-free）组合**后，几何项相消，剩下主要是电离层（+ 偏差）：

\[
P_{GF} = P_1 - P_2 \propto \mathrm{STEC} + \mathrm{偏差项}
\]

人话：两个频率的伪距相减，卫星有多远、对流层有多厚，大体消掉了；差里主要是「这条斜路径上的电子」和仪器偏差。

载波相位也有对应的几何无关组合，噪声通常比伪距小得多，但带有**整周模糊度**，周跳时会跳变。

---

## 相位平滑：伪距稳、相位准

实务里常见做法：

1. 用**伪距几何无关组合**定 TEC 的绝对水平（但噪声大、多路径明显）；
2. 用**相位几何无关组合**看相对变化（平滑、精密）；
3. 在无周跳弧段里，用相位对伪距做**载波平滑**，得到更干净的 STEC 时间序列。

类比：伪距像粗糙但有刻度的尺子；相位像细密但不知道零点的千分尺。平滑 = 用千分尺描变化，用尺子钉绝对高度。

---

## DCB / IFB：为什么必须管

几何无关组合里，除了 STEC，还有：

- **卫星 DCB**（Differential Code Bias）：卫星端两个频率码延迟差；
- **接收机 DCB / IFB**（Inter-Frequency Bias）：接收机端类似偏差。

它们会**伪装成 TEC**。不管偏差，你的「TEC」可能系统性偏高或偏低好几 TECU，区域对比、建 GIM、和 IRI 比都会歪。

实务直觉：

- 用公开的 **DCB / OSB** 产品改正卫星端（IGS 分析中心等）；
- 接收机端常在估计里当未知数，或用已知好的参考策略约束；
- 不同码类型（C1C、C1W…）偏差定义不同，RINEX 观测类型要和偏差产品对齐。

本目录里与偏差相关的条目可在轨道/钟差与电离层工具中交叉查找（例如 `Gkit-Bias` 一类）；数据侧见 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) 与 [`docs/data-access.md`](../data-access.md)。

---

## 从 RINEX 到 STEC：步骤直觉（不堆公式）

把流水线想成七步：

1. **读观测**  
   解析 RINEX（可用 `georinex` 等，见 [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md)），取出双频伪距与相位、时间、卫星号。

2. **粗差与周跳**  
   相位跳了，几何无关相位序列会断。先修周跳或分段处理。

3. **组几何无关组合**  
   伪距 / 相位分别做 \(f_1,f_2\) 差，得到与 STEC 成比例的观测量。

4. **相位平滑伪距**  
   在连续弧段上降低伪距噪声。

5. **改正 DCB（及必要的频率相关项）**  
   卫星 DCB 优先用产品；接收机偏差按软件策略估计或标定。

6. **换算到 TECU**  
   用频率因子把「米」量纲的组合值换成 TECU，得到 **STEC(t)**。

7. **（可选）映射到 VTEC**  
   用薄壳 + 穿刺点（IPP）把 STEC 映到 VTEC，再网格化 → 通向 GIM（见 [03](./03-gim-ionex.md)）。

课堂提醒：不同软件在第 2、5、7 步的默认假设不同，**不要混用结果却不看 README**。

---

## 本目录里可对号的工具（已核验）

| 你想做的事 | 可点名的条目（名称以 `PROJECTS.json` 为准） | 列表 |
|---|---|---|
| RINEX → TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX` | [`01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 读/写观测 | `georinex`、`rinex` 等 | [`03-gnss-data.md`](../../lists/03-gnss-data.md) |
| 质量检查 | `TEQC` 等 | [`03-gnss-data.md`](../../lists/03-gnss-data.md) |

克隆请去**上游 URL**，不要把第三方源码拷进本索引仓。

---

## 延伸阅读（本仓库）

- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) — TEC 估计子类
- [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) — RINEX / QC
- [`docs/data-access.md`](../data-access.md) — 观测与偏差产品从哪下
- 下一讲：[03-gim-ionex.md](./03-gim-ionex.md)
