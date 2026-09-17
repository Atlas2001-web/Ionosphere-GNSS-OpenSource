# 04 · IRI / NeQuick / NeQuick-G：模型解决什么问题？

先问：**你缺的是「某一时刻真实天空的电子含量」，还是「没有实测时也能给的气候态/广播改正」？**

- 要尽量贴当天实况 → 优先 GNSS TEC、GIM、测高仪/掩星同化产品；
- 要可重复的经验背景、教学演示、单频广播改正、或与实测对比的「参考气候」→ **IRI / NeQuick** 这类经验模型上场。

---

## 经验模型在干什么？

它们根据长期观测统计（太阳活动、地磁、地方时、纬度等），给出电离层**电子密度廓线**或衍生的 TEC，回答的是：

> 「在这种太阳/地磁条件下，平均来说电离层长什么样？」

不是数值天气预报式的「下一小时同化预报」（虽然可以和同化系统联用），而是**经验气候 + 驱动指数**。

---

## IRI、NeQuick、NeQuick-G 分工直觉

| 名称 | 你记住什么 | 典型用途 |
|---|---|---|
| **IRI**（International Reference Ionosphere） | COSPAR/URSI 参考电离层；给 \(N_e(h)\) 等参数的「标准肖像」 | 科研对比、教学、驱动其他应用；版本如 IRI-2016/2020/2026 |
| **NeQuick** | 由电子密度廓线可积出 TEC；ITU 等场景常见 | 传播预测、TEC 气候估计 |
| **NeQuick-G** | Galileo **单频电离层改正**采用的版本；输入与 Galileo 广播消息相关 | 接收机/仿真里的单频改正；官方 C 源码 |

人话：

- IRI ≈ 「电离层百科全书式的经验标准」；
- NeQuick ≈ 「方便算路径 TEC / 传播的廓线模型」；
- NeQuick-G ≈ 「给 Galileo 单频用户用的那一套 NeQuick」。

本目录已收录（名称已核验）：`IRI-Fortran`、`IRI-2026-package`、`IRI-COMMON-FILES`、`iri2020`、`iri2016`、`PyIRI`；`NeQuick2-ICTP`、`NequickG`、`Galileo-NeQuick-G`、`NeQuickG-ESSR` 等。详见 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)。

---

## 和实测 TEC / GIM 的区别

| | 经验模型（IRI/NeQuick） | GNSS 实测 TEC / GIM |
|---|---|---|
| 数据根 | 历史统计 + 指数驱动 | 当天（或近实时）双频观测 |
| 空间表现 | 平滑的气候态结构 | 含天气尺度扰动、风暴响应（视产品） |
| 输出 | 常含**高度廓线** \(N_e(h)\) | GNSS 直接给的是**柱总量** STEC/VTEC |
| 失效模式 | 磁暴、强 ESA 等偏离气候时偏差大 | 测站空洞、DCB、映射误差 |

类比：IRI 像「该季节该纬度的平均天气预报图」；GIM 像「今天的实况分析图」。

---

## 何时用模型？何时用实测？

**更倾向模型：**

- 单频定位需要广播式改正（Klobuchar / NeQuick-G）；
- 做教学、算法基准、或需要完整 \(N_e(h)\) 而你没有廓线观测；
- 历史时段没有足够 GNSS 网，只能给气候背景。

**更倾向实测 / GIM：**

- 写论文对比「当天 TEC」；
- 评估空间天气事件；
- 同化、建高分辨率区域图、闪烁研究的背景场。

**常见组合：** 用 IRI/NeQuick 作背景或对照，用 GNSS GIM/STEC 作真值近似；差异本身就是课题。

---

## 使用时注意

1. IRI 常需**系数/公共文件**与指数（F10.7、Ap 等）——官网包与 `IRI-COMMON-FILES`、`IRI-indices` 一类条目要配齐。  
2. NeQuick-G 跟 Galileo 接口参数走，和科研用 NeQuick2 输入不一定相同。  
3. 模型 TEC 与 GIM TEC 比，先统一：时间、坐标、是否含等离子体层、薄壳高度假设。

---

## 延伸阅读（本仓库）

- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) — IRI 模型、IRI/NeQuick、NeQuick-G 官方
- 定位改正语境：[06-iono-positioning.md](./06-iono-positioning.md)
- 下一讲：[05-scintillation-roti.md](./05-scintillation-roti.md)
