# 19. 电离层现象总览（图优先）

先看图，再点进专题课。配图均为本仓自绘示意（CC0），**不是**实测 GIM 产品。

![现象速览](./images/fig-phenomena-gallery.png)

## 常见现象 → 图 → 专课

| 现象 | 你在图上应看到什么 | 图 | 专课 |
|---|---|---|---|
| 日夜 / EIA | 白天高、夜间低；低纬双侧驼峰 | [日夜 TEC](./images/fig-tec-day-night.png) · [EIA](./images/fig-eia-twin-crests.png) | [21](./21-equatorial-anomaly-bubbles.md) |
| 气泡 / 闪烁 | TEC 被“挖空”的细长耗空 | [气泡](./images/fig-scintillation-bubbles.png) | [05](./05-scintillation-roti.md) · [21](./21-equatorial-anomaly-bubbles.md) |
| TID | 残差场里斜向波前随时间推进 | [TID](./images/fig-tid-wavefront.png) | [22](./22-tid-traveling-disturbances.md) |
| 磁暴 | 扰动减去宁静后的正/负残差斑 | [磁暴残差](./images/fig-storm-quiet-residual.png) | [20](./20-storm-tec-analysis.md) |
| 耀斑 | 短时间尖峰抬升 | [耀斑](./images/fig-flare-sudden-ionize.png) | [23](./23-flare-eclipse-special.md) |
| 高度结构 | D/E/F 层 Ne 剖面 | [Ne](./images/fig-ne-profile-layers.png) | [01](./01-ionosphere-tec-basics.md) |

## 读图口诀

1. **先定时空**：地方时、纬度、磁情指数  
2. **再分几何 vs 天气**：映射/仰角别当成空间天气  
3. **最后才归因**：喷泉、穿透电场、重力波、耀斑 EUV/X  

再生配图：`python3 scripts/make_phenomena_figs.py`
