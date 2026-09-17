# 09 · DCB / 硬件延迟：为什么 TEC 数字会「整段平移」

学完 [02-gnss-dualfreq-tec.md](./02-gnss-dualfreq-tec.md) 你会组几何无关组合，但跑出来的 STEC 常常和别人差一截**几乎整天平行的常数**。课堂里最常见的锅，就是 **DCB（Differential Code Bias，差分码偏差）** 以及它的亲戚：接收机 IFB、码类型不一致、参考基准没对齐。

本讲把偏差从「听说过」推到「知道该怎么改、什么时候可以假装不管」。

---

## 先建立直觉：尺子两端的橡皮泥

双频伪距里，接收机和卫星的硬件都会让两个频率的码延迟略有不同。几何无关组合把「路径几何」消掉了，却把这种**频率相关的硬件延迟差**留了下来。

人话：你量雾的厚度时，尺子两端各粘了一小段不知道多长的橡皮泥——测出来的「雾厚」会整体偏一截。这段橡皮泥，就是 DCB。

更狠一点：橡皮泥长度几乎不随时间变（短时段内），所以它会让你的 TEC 时间序列**整段平移**，而不是抖出毛刺。做扰动差分、ROTI 时，常数往往无所谓；谈「今天中午有 45 TECU」这种绝对数字时，就必须较真。

常见相关量：

| 名称 | 谁身上的 | 你什么时候会撞上 |
|---|---|---|
| 卫星 DCB | 卫星端两频码延迟差 | 用伪距估 TEC、和 IGS/分析中心产品比 |
| 接收机 DCB / IFB | 接收机端类似偏差 | 单站解、不同接收机混网、换机后跳变 |
| 相位模糊度 / 弧段常数 | 载波几何无关组合 | 相位 TEC 有未知常数，要连弧或钉到伪距 |
| OSB / UPD 等 | 更细的码/相位偏差产品 | PPP、多系统、精密定位场景更常见 |

---

## 几何无关组合里，偏差到底藏在哪

回顾：伪距几何无关组合大致满足

\[
P_{GF} = P_1 - P_2 \propto \mathrm{STEC} + b^{sat} + b_{rcv} + \varepsilon
\]

其中 \(b^{sat}\)、\(b_{rcv}\) 就是（换算到 TECU 或米之后的）卫星端与接收机端偏差贡献。相位组合更干净，但多一个**模糊度常数**；周跳会让这个常数换一段。

课堂纠错：

1. **「我已经双频了，所以没有偏差」** — 双频消的是几何与对流层等公共项，**不是**频率相关硬件延迟差。
2. **「DCB 会随 TEC 日变化扭来扭去」** — 短时段内更像慢变/常数；若你的「DCB」跟着地方时剧烈扭，多半是映射、多路径或弧段断裂被误吸收了。
3. **「所有码类型共用同一套 DCB」** — C1C、C1W、C2W… 定义不同。RINEX 观测类型必须和偏差产品对齐，否则等于用错尺子刻度。

---

## 为什么 GIM / IONEX 里也有 DCB

IGS 分析中心做全球 GIM 时，往往会**同时估**格网（或球谐）TEC 和一批卫星/接收机 DCB。地图和偏差是耦合解出来的：你固定某颗星/某台接收机为参考，其它偏差相对它漂。

所以：

- 下载的 IONEX 头或伴随产品里，常能看到 DCB 相关信息；
- 不同分析中心（CODE、JPL、CAS、UPC、WHU 等）的绝对 TEC 可以差数 TECU，部分来自**基准与估计策略**，不全是「谁更准」；
- 比对两家 GIM 时，先看形态与梯度，再抠绝对水平。

本仓库数据入口：`CDDIS-IONEX`、`JPL-IONEX-Rapid`、`ROB-IONEX-Products`、`GFZ-Global-Ionosphere-Maps`、`WHU-IGS-Ionosphere-AC`、`UWM-IGS-Iono-Combination`（见 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) 与 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)）。

---

## 处理流程（教学版五步）

1. **选观测量**  
   伪距几何无关：无模糊度、噪声大、多路径明显。相位平滑伪距或「相位 + 伪距钉绝对」更常用。

2. **连弧与周跳**  
   相位跳了，TEC 会出台阶。先修周跳或分段；每段可以有自己的常数。

3. **估 / 改正偏差**  
   - 卫星 DCB：优先用公开产品改正；  
   - 接收机端：单站常当未知数与薄壳映射一起估；多站网可把卫星 DCB 当公共参数。  
   本目录与偏差相关的条目可查 `Gkit-Bias`；TEC 估计主线仍是 `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software` 等。

4. **对齐产品基准**  
   和 CODE/CAS/JPL 的 DCB 或 GIM 比时，问清楚：哪个卫星/接收机被约束为 0？单位是 ns 还是 TECU？对应哪一对码？

5. **按科学目标决定较真程度**  
   - 只谈变化、扰动、差分 TEC、ROTI → 常数 DCB 影响小；  
   - 谈绝对 TECU、跨站网融合、与 IRI 比绝对值 → 必须较真。

---

## 和定位的关系（别和 06 打架）

[06-iono-positioning.md](./06-iono-positioning.md) 里，PPP 常用无电离层组合（IF），本质是**绕开**一阶电离层，不是把 DCB 估成 TEC。你若目标是「电子含量科学」，走 TEC/GIM 路线；若目标是「位置」，IF/双频消电离层往往更直接。

两条路都碰偏差，但参数名字和约束习惯不同：

| 目标 | 典型思路 | 目录里可对号 |
|---|---|---|
| 科学 TEC / GIM | 显式估/改正 DCB，输出 STEC/VTEC | `gnss-tec`、`ionex`、`SH-GIM`、`mosgim` |
| 精密定位 | IF 组合、或估计电离层参数辅助模糊度 | `RTKLIB`、`gLAB`、`GAMPII-GOOD`、`PRIDE-PPPAR`、`PPP-RTK-Ionosphere` |

---

## 常见误区清单（请逐条打勾自测）

- [ ] 两台接收机同站同时段 STEC 差约 5 TECU 且整天平行 → 优先怀疑**接收机 DCB/IFB 或码类型**，不是「电离层真的差了 5」。
- [ ] 换了固件/天线后 TEC 跳一截 → 先查硬件延迟是否变了，再怀疑空间天气。
- [ ] 把伪距 TEC 和相位 TEC 绝对水平直接比 → 没处理模糊度/平滑策略时，比的是两套零点。
- [ ] 混用不同分析中心的卫星 DCB 与自家接收机估计 → 基准不一致会把误差灌进图。
- [ ] 低高度角「DCB」不稳定 → 多半是映射与多路径，别全推给硬件。

---

## 练习题（自测）

1. 两台接收机同一测站、同一时段，STEC 差了约 5 TECU 且几乎整天平行——更可能是什么？你准备怎么验证？  
2. 你只关心磁暴期间 TEC **相对**增强，DCB 估不准会致命吗？什么情况下仍会致命？  
3. 打开一份 IONEX，你如何快速判断它是否附带/隐含了 DCB 信息？  
4. 若 RINEX 里用的是 C1C/C2W，却套了另一对码的 DCB 产品，后果是什么？

---

## 本仓库工具落点（名称已用 `PROJECTS.json` 核验）

| 你想做的事 | 可点名的条目 | 列表 |
|---|---|---|
| RINEX → STEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software` | [`01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 偏差相关 | `Gkit-Bias` | 轨道/钟差与电离层交叉检索 |
| 读 GIM / IONEX | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer` | [`01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 产品与数据 | `CDDIS-IONEX`、`JPL-IONEX-Rapid`、`DLR-IMPC`、`IGS-Products` | [`10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |

克隆请去**上游 URL**，不要把第三方源码拷进本索引仓。数据怎么下见 [`docs/data-access.md`](../data-access.md)。

---

## 延伸阅读（本仓库）

- 上一讲深化：[02-gnss-dualfreq-tec.md](./02-gnss-dualfreq-tec.md)
- 建图：[03-gim-ionex.md](./03-gim-ionex.md) · [10-build-gim-workflow.md](./10-build-gim-workflow.md)
- 定位侧：[06-iono-positioning.md](./06-iono-positioning.md)
- 列表：[`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)
