# 05 · 闪烁、S4、σφ、ROTI：和 TEC 图什么关系？

先问：**你关心的是「电子有多少」，还是「信号抖不抖」？**

- TEC / GIM → 柱含量多少（慢变背景 + 大尺度结构）；
- 闪烁指标 → 小尺度不规则性导致的**幅度/相位起伏**，直接影响跟踪与定位连续性。

两者相关，但**不是同一个量**。

---

## 闪烁是什么？

信号穿过电离层里的电子密度不规则体时，发生衍射/折射，到达接收机的电场幅度和相位快速起伏，称为**电离层闪烁（scintillation）**。

低纬（赤道异常区）日落后、高纬磁暴期间更常见。类比：夏天柏油路上的热湍流让远处景物发「晃」——闪烁是电波版的晃。

---

## S4 和 σφ

| 符号 | 测什么 | 直觉 |
|---|---|---|
| **S4** | 信号**强度**起伏的归一化程度 | 幅度抖得有多厉害 |
| **σφ**（sigma-phi） | 载波**相位**起伏的标准差 | 相位抖得有多厉害 |

专用闪烁接收机（高采样、专用固件）直接出 S4、σφ。普通测绘型接收机的 1 Hz 或更低采样，**不足以**完整替代专用闪烁观测，但还能从 TEC 变化率构造代理指标。

---

## ROT 与 ROTI

双频估出 STEC 后，可看它随时间的变化率：

- **ROT**（Rate of TEC）：TEC 的时间变化率；
- **ROTI**（ROT Index）：一段窗口内 ROT 的起伏强度（常见为标准差一类统计）。

人话：ROTI 高 → 这段时间 TEC「毛刺」多 → 往往和小尺度结构活跃有关，**常作闪烁活动的代理指标**，尤其在只有常规 GNSS 数据时。

注意：ROTI **≠** S4。相关可以很好，但物理与频段、采样、阈值都不同；写论文不要把二者混称为同一观测。

---

## 和 TEC 图的关系

```
平滑 VTEC / GIM  ──► 大尺度「有多少电子」
        │
        │  同一区域可以
        ▼
高 ROTI / 高 S4 ──► 小尺度「抖不抖」
```

- 赤道晚上：VTEC 可能仍高，同时 ROTI/S4 升高（气泡、不规则体）；
- 也可能 TEC 梯度大但闪烁未必强——要看不规则体谱与几何。

做空间天气监测时，常**两张图一起看**：TEC 图 + ROTI/闪烁图。

---

## 开源工具在本目录大致落在哪类

均在 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)，子类名大致是 **闪烁**、**闪烁/ROTI**：

| 方向 | 已核验条目举例 |
|---|---|
| ROTI 计算 / 演示 | `igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`Ionospheric-TEC-ROTI-Interactives`、`roti-gnss-ml` |
| 闪烁仿真 | `gnss-scintillation-simulator`、`gnss-scintillation-simulator_2-param` |
| 闪烁处理 / 指标 | `scintill-ai`、`BiScEF`、`scintkit`、`OASIS`、`IonoMoni`、`gnssutils` |
| 闪烁数据下载 | `ismr_downloader`（ISMR 一类） |

数据侧若需掩星或空间天气产品，再看 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)。

---

## 延伸阅读（本仓库）

- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md)
- TEC 基础：[01-ionosphere-tec-basics.md](./01-ionosphere-tec-basics.md)
- 下一讲：[06-iono-positioning.md](./06-iono-positioning.md)
