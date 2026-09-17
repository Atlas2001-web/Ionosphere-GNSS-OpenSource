# 06 · 定位里怎么处理电离层？（单频 / 双频 / PPP / RTK）

先问：**你的接收机几个频率？你要米级还是厘米级？**

电离层在伪距上可以造成数米到数十米量级的误差（视 TEC 与仰角）。定位软件必须二选一或组合：**改正它、消掉它、或把它估出来**。

---

## 单频：模型改正

只有一个频率时，做不了几何无关消电离层，只能：

1. **广播模型**  
   - GPS：**Klobuchar**（8 参数，粗、快、嵌入导航电文）；  
   - Galileo：**NeQuick-G**（见 [04](./04-iri-nequick.md)）。  
2. **外源格网**  
   用 GIM/IONEX 在穿刺点插值 VTEC，再映射成延迟（需额外链路）。

本目录相关：`Klobuchar-study-code`、`Galileo-NeQuick-G`、`NequickG` 等 → [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)。

课堂预期：单频模型改正后，残差仍在，**不能指望到双频消电离层的水平**。

---

## 双频：消电离层组合

双频伪距（或相位）可组成**无电离层（ionosphere-free）组合**：一阶 \(1/f^{2}\) 项消掉，几何距离留下。

人话：两个频率加权相加/相减，让「雾」的一阶效应抵消，专门服务**精密测距**，而不是去估 TEC。

代价：

- 噪声被放大；
- 更高阶电离层项、差分偏差等仍可能残留；
- 你得到的是更好的距离，**不是**一张 TEC 图（估 TEC 要用几何无关，见 [02](./02-gnss-dualfreq-tec.md)）。

---

## RTK：差分把公共电离层削弱

短基线 RTK 中，流动站与基准站看天空几乎同一片电离层，**站间差分**后公共延迟大幅削弱。

- 基线短、电离层平静 → 残差小，模糊度好固定；
- 基线长或暴时 → 电离层残余变大，固定变难，需要网络 RTK、区域大气约束等。

电离层在这里是「差分后的残余敌人」，通常不单独输出 TEC 产品。

---

## PPP：估、消、或约束

精密单点定位常见策略（简讲）：

| 策略 | 直觉 |
|---|---|
| 双频无电离层组合 | 消一阶电离层，经典 PPP |
| 非差非组合 / 估 STEC | 把每颗星的电离层当参数估，可加 GIM 约束或随机游走 |
| 增强改正 | 用区域电离层/SSR 产品当先验 |

开源定位套件里电离层模块往往**嵌在大工程中**，而不是单独一个「iono.exe」。本目录可从 [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) 看：`RTKLIB`、`gLAB-UPC`、`PRIDE-PPPAR`、`ginan` 等。

---

## 选题时怎么选改正策略？

```
单频手持 / 教学演示  → Klobuchar 或 NeQuick-G
双频精密测距         → 无电离层组合（+ 必要的偏差产品）
短基线工程 RTK       → 差分；关注暴时残余
科研 PPP / 大气参数  → 估电离层或引入 GIM；同时可产出 TEC
只要 TEC 产品        → 走 01 列表 TEC/GIM 工具，不必先上全套 PPP
```

---

## 延伸阅读（本仓库）

- [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md)
- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) — 模型与 NeQuick-G
- [`docs/categories.md`](../categories.md)
- 下一讲：[07-ionosonde-occultation.md](./07-ionosonde-occultation.md)
