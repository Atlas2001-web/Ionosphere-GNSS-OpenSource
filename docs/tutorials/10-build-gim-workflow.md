# 10 · 从多站 GNSS 到 GIM：一条能落地的流水线

目标：不是背「球谐阶数」，而是能画出**自己的区域/全球电子含量图**该经过哪些站，并且知道每一步会引入什么误差。学完本讲，你应能在白板上画出流程，并在本仓库 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) 里对上工具名。

先修建议：[02-gnss-dualfreq-tec.md](./02-gnss-dualfreq-tec.md)、[03-gim-ionex.md](./03-gim-ionex.md)、[09-dcb-biases-deep.md](./09-dcb-biases-deep.md)。

---

## 总流程图（先把这个背下来）

```
连续跟踪站 RINEX
    → 质量检查 / 周跳
    → 每站每星 STEC（处理 DCB）
    → 穿刺点 IPP + 映射函数 → VTEC 采样
    → 空间表示（格网插值 或 球谐/其他基函数）
    → 时间滑动或逐时段解算
    → 写出 IONEX / 自有格网
    → 和 IGS GIM / 测高仪 / 掩星交叉验证
```

类比：做菜不是「把菜扔进锅」。选菜（站网）、洗净（QC）、切配（STEC）、调味（DCB/映射）、摆盘（空间模型）、尝味（和官方产品比）——缺一步，盘子上可能好看但不可吃。

---

## 每一步在干什么

### 1. 选站与数据

- **全球**：IGS 及合作站；入口见 `IGS-Data-Access`、`IGS-Products`、`EarthScope-gnsstools`。  
- **区域**：各国 CORS、陆态网等（注意申请与引用）。  
- **时间分辨率**：科学分析常用 30 s 或更高采样；出图可以先 15 min / 1 h 一帧，降低算力。  
- **空间密度**：站太稀，插值会「编造」结构；站太密但质量不齐，噪声会灌进图。

数据入口：[`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)、[`docs/data-access.md`](../data-access.md)。产品对照常用 `CDDIS-IONEX`、`JPL-IONEX-Rapid`、`DLR-IMPC`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC`、`ROB-European-TEC`、`INPE-TEC-Maps-IONEX`。

### 2. 单站 TEC

用 `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software` 等，从双频观测量到 STEC。先求「能复现文献图的量级与日变形态」，再抠绝对标定（见 [09-dcb-biases-deep.md](./09-dcb-biases-deep.md)）。

质检可配合 `TEQC`、`GFZRNX`、`georinex`（[`lists/03-gnss-data.md`](../../lists/03-gnss-data.md)）。

### 3. 穿刺点与薄壳映射

常用简化：假设电子集中在某一高度薄壳（如 350–450 km），把斜路径 TEC 映射成天顶方向 VTEC，并把贡献记在穿刺点（IPP）经纬度上。

课堂必须说的局限：

- 真实电离层有厚度、有倾斜梯度；  
- **低高度角**路径长、映射误差大，所以高度角截止（如 15°–20°）很常见；  
- 壳高选错，会系统性扭歪赤道异常等结构。

### 4. 空间模型怎么选

| 做法 | 适合 | 代价 | 目录可对号 |
|---|---|---|---|
| 格网 + 插值（IDW/Kriging 等） | 区域网、实现快 | 边界与稀疏区易假结构 | `Ionospheric-TEC-Kriging-Turkiye` 等思路可参考 |
| 球谐展开 GIM | 全球/大区域、与 IGS 传统接近 | 阶次截断与 Gibbs 假振荡 | `SH-GIM`、`mosgim`、`mosgim2`、`m_gim` / `M_GIM` |
| 其他基函数 / 层析 | 研究型三维 | 病态、要先验 | 见 [11-tomography-basics.md](./11-tomography-basics.md) |

维护者仓库 `SH-GIM` 属于球谐路线之一（目录只给链接）。学习时以公开 IGS 产品与通用读写库（`ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer`）为主即可。

### 5. 时间维

可以逐小时独立解，也可以滑动窗口、Kalman 式递推。时间太粗会糊掉 TID；太细又会被噪声主导。入门先固定 1 h 或 2 h，能画出地方时结构再说。

### 6. 输出与互操作

若要和社区交换，优先学会写/读 **IONEX**（见 [03-gim-ionex.md](./03-gim-ionex.md)）。自有二进制格式可以，但别人难复现你的论文图。

---

## 验证清单（精通的人天天做）

- [ ] 和 CODE/JPL/CAS/WHU 等 GIM 的差分直方图（均值、标准差）  
- [ ] 安静日日变化是否合理（地方时：白天高、夜里低；低纬是否有赤道异常双峰）  
- [ ] 磁暴日是否出现「假空洞」（往往是映射/数据空洞，不是物理真洞）  
- [ ] 与测高仪 foF2、掩星电子密度积分是否**同向**变化（见 [07-ionosonde-occultation.md](./07-ionosonde-occultation.md)）  
- [ ] 换高度角截止、换壳高，图是否「面目全非」——若是，说明你的结构不稳健  

---

## 常见误区

1. **「插值很漂亮 = 物理真实」** — 稀疏区的平滑色块可能是算法填的。  
2. **「和某家 GIM 差 8 TECU 就是我错了」** — 先查 DCB 基准与时间对齐；分析中心之间本身就有差异（`UWM-IGS-Iono-Combination` 一类工作就是在谈组合）。  
3. **「全球球谐阶数越高越好」** — 过高会拟合噪声，并在数据空洞处振荡。  
4. **「只用一个安静日调参」** — 扰动日才会暴露映射与站网漏洞。  
5. **「物理模式输出可以直接当 GIM」** — `TIE-GCM` / `GEMINI3D` / `pytiegcm` 是正演/研究工具，验证用可以，替代观测产品要非常谨慎。

---

## 迷你练习

1. 只下载一天 `CDDIS-IONEX`，用 `ionex` 画出中国区 VTEC，描述赤道异常是否可见。  
2. 选 5–10 个 IGS 站，跑通单站 STEC，把 IPP 投到地图上——你的采样点是否「围住」了你想画的区域？  
3. 把壳高从 350 km 改到 450 km，同一套 STEC 的 VTEC 图差在哪里？写三句话结论。

完整「一日闭环」见 [16-practice-one-day-tec.md](./16-practice-one-day-tec.md)。

---

## 本仓库工具落点

| 步骤 | 条目（`PROJECTS.json` 核验） |
|---|---|
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX` |
| 读写 IONEX | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer`、`ionex-downloader` |
| 球谐/GIM 实现 | `SH-GIM`、`mosgim`、`mosgim2`、`m_gim`、`M_GIM` |
| 官方/业务产品 | `CDDIS-IONEX`、`GFZ-Global-Ionosphere-Maps`、`DLR-IMPC`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC` |
| 物理对照 | `TIE-GCM`、`pytiegcm`、`GEMINI3D` |

---

## 延伸阅读

- [03-gim-ionex.md](./03-gim-ionex.md) · [09-dcb-biases-deep.md](./09-dcb-biases-deep.md) · [11-tomography-basics.md](./11-tomography-basics.md) · [16-practice-one-day-tec.md](./16-practice-one-day-tec.md)
