# PyTECGg · 多星座 TEC 重建与校准（Python + Rust）

目录条目：[`PROJECTS.json` → `PyTECGg`](../../PROJECTS.json) · 上游 <https://github.com/viventriglia/PyTECGg>  
**作者：viventriglia 等**（**不是**本索引维护者自有项目；维护者仅 fork/星标关系见目录标记）  
许可：GPLv3 · 安装：`pip install pytecgg` · 文档：<https://viventriglia.github.io/PyTECGg/>  
列表：[01 电离层](../../lists/01-ionosphere.md)

## 作用与场景

从 RINEX 观测/导航出发，做几何无关组合、弧段整平、偏差估计与校准，输出校准后的 sTEC / vTEC，以及站天顶 **vertical equivalent（veq）** 等。适合：

- 研究组要**可编程、可批处理**的 TEC 流水线；
- 多星座（G/E/C/R）与 RINEX 2/3/4、Hatanaka 压缩；
- 结果留在 Polars DataFrame 里继续统计/画图。

**何时用：** 「RINEX → 有绝对意义的 TEC 时序 / IPP」。  
**何时不用：** 只探活文件 → [georinex](./georinex.md)；单站 ROTI/AATR 一体机 → [ionomoni](./ionomoni.md)；全球球谐 GIM 求解 → [sh-gim](./sh-gim.md) / mosgim 等。

## 安装

官方标明 **Python 3.11–3.13**；多数平台有预编译 wheel。

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install pytecgg
```

强制源码编译需本机 Rust 工具链（见上游 Installation）。

## 最小示例

按官方 quickstart 思路精简（路径换成你的文件；完整预处理链见上游文档 0→2）。

```python
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg import GNSSContext

NAV_PATH = Path("BRDC00IGS_R_20240910000_01D_MN.rnx")
OBS_PATH = Path("YOUR00XXX_R_20240910000_01D_30S_MO.rnx")

nav_dict = read_rinex_nav(NAV_PATH)
df_obs, rec_pos, rinex_version = read_rinex_obs(OBS_PATH)
rec_name = OBS_PATH.name[:4].lower()

ctx = GNSSContext(
    receiver_pos=rec_pos,
    receiver_name=rec_name,
    rinex_version=rinex_version,
    h_ipp=350_000,       # 薄壳高度 (m)，常用 350 km
    systems=["G", "E"],
)
```

完成弧段整平与 IPP 等预处理得到 `df_final` 后（步骤见上游 preprocessing 文档）：

```python
from pytecgg.tec_calibration import calculate_tec, calculate_vertical_equivalent

df_calibrated = calculate_tec(
    df_final,
    ctx=ctx,
    max_polynomial_degree=3,
    batch_size_epochs=30,
)
df_veq = calculate_vertical_equivalent(
    df_calibrated,
    ctx=ctx,
    max_polynomial_degree=3,
    batch_size_epochs=30,
)
# 关注列：stec, vtec, veq, bias, ele, azi, ...
```

批量容器方案见上游 Docker Batch Calibrator。若上游参数名有微调，以当前官方文档为准。

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS/NAV（含压缩）；`GNSSContext`（接收机坐标、IPP 高度、星座列表） |
| 输出 | Polars DataFrame：校准 sTEC/vTEC、硬件偏差、veq；可再导出 CSV/Parquet |
| 辅助 | 文档提供 RING/EUREF OBS、BKG 导航星历下载工具函数 |

## 常见坑

1. **未校准 vs 已校准**：几何无关组合只有相对变化；对比绝对 TEC 前必须完成校准。  
2. **Python 版本**：过旧解释器可能无合适 wheel。  
3. **GPLv3**：与闭源商业流程链接时需法律评估。  
4. **薄壳与映射**：`h_ipp`、多项式次数、batch 长度会影响 vTEC/veq。  
5. **作者归属**：引用与 issue 请指向 **viventriglia/PyTECGg** 与其论文/预印本，勿与本仓维护者自有 MATLAB 工具混淆。

## 接到哪一步分析

- 教程：[02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md)、[09 DCB](../tutorials/09-dcb-biases-deep.md)、[16 一日 TEC 实操](../tutorials/16-practice-one-day-tec.md)。  
- 前处理读盘也可先用 [georinex](./georinex.md) 做 QC。  
- 网格产品：校准 VTEC/IPP 可与 CDDIS IONEX、或 [ionex-gim](./ionex-gim.md) / 自建 GIM 对照（注意偏差定义）。  
- 同一事件可再跑 [IonoMoni](./ionomoni.md) 的 ROTI，做「TEC 结构 + 不规则体」双视角。
