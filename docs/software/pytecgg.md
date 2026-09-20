# PyTECGg

目录：[`PROJECTS.json` → `PyTECGg`](../../PROJECTS.json) · 上游 <https://github.com/viventriglia/PyTECGg> · 文档 <https://viventriglia.github.io/PyTECGg/> · GPL-3.0

> **作者：viventriglia 等（不是本索引维护者自有项目）。** 勿与维护者 MATLAB [SH-GIM](./sh-gim.md) 混淆。

## 用途

- 从 RINEX OBS/NAV 做几何无关组合、弧段整平、偏差估计与校准，输出校准 **sTEC/vTEC** 与站天顶 **veq** 等（Polars DataFrame）。
- 可编程批处理；多星座（G/E/C/R）；RINEX 2/3/4、Hatanaka。
- **用：** 需要有绝对意义的 TEC 时序/IPP。  
- **不用：** 只探活 → [georinex](./georinex.md)；ROTI 一体机 → [ionomoni](./ionomoni.md)；全球球谐求解 → 其他开源 GIM / 见 [sh-gim](./sh-gim.md) 边界。

## 安装

官方标明 **Python 3.11–3.13**（以当前文档为准）；多数平台有 wheel。

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip pytecgg
python -c "import pytecgg; print(pytecgg.__file__)"
```

源码编译需 Rust 工具链。Docker Batch 见上游。

## 快速上手

```python
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg import GNSSContext
from pytecgg.satellites import prepare_ephemeris, satellite_coordinates, calculate_ipp
from pytecgg.linear_combinations import calculate_linear_combinations
from pytecgg.tec_calibration import (
    extract_arcs, calculate_tec, calculate_vertical_equivalent,
)

NAV_PATH = Path("BRDC00IGS_R_20240910000_01D_MN.rnx")
OBS_PATH = Path("YOUR00XXX_R_20240910000_01D_30S_MO.rnx")

nav_dict = read_rinex_nav(NAV_PATH)
df_obs, rec_pos, rinex_version = read_rinex_obs(OBS_PATH)
ctx = GNSSContext(
    receiver_pos=rec_pos,
    receiver_name=OBS_PATH.name[:4].lower(),
    rinex_version=rinex_version,
    h_ipp=350_000,
    systems=["G", "E"],
)

ephem_dict = prepare_ephemeris(nav_dict, ctx)
df_lc = calculate_linear_combinations(df_obs, ctx, selection_mode="availability")
df_coords = satellite_coordinates(df_lc["sv"], df_lc["epoch"], ephem_dict)
df_arcs = extract_arcs(df_lc, ctx, min_arc_length=120).join(
    df_coords, on=["sv", "epoch"], how="left"
)
df_geom = calculate_ipp(df_arcs, ctx, min_elevation=20)

df_calibrated = calculate_tec(
    df_geom, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30,
)
df_veq = calculate_vertical_equivalent(
    df_calibrated, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30,
)
print(df_calibrated.columns)
print(df_calibrated.select(["stec", "vtec"]).describe())
df_calibrated.write_parquet("tec_calibrated.parquet")
df_calibrated.write_csv("tec_calibrated.csv")
```

**预期：** 出现 `stec`/`vtec`/`veq`/`bias` 等列。API 细节以上游 0→2 文档为准。

与同日 GIM 对照：[ionex-gim](./ionex-gim.md)（比日变化与量级，不要求像素一致）。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS/NAV（含压缩）；`GNSSContext` |
| 输出 | Polars DataFrame（stec/vtec/veq/bias/…）；parquet/csv |
| 不做 | 全球球谐反演；ROTI 主产品 |

## 常用参数

| 项 | 说明 |
|---|---|
| `h_ipp` | 薄壳高度（m）；常用 350 km |
| `systems` | 星座列表 |
| `min_arc_length` | 最短弧段 |
| `min_elevation` | 截止高度角（度） |
| `max_polynomial_degree` / `batch_size_epochs` | 校准多项式与批大小 |
| `selection_mode` | 线性组合选择策略 |

## 接到工作流哪一步

- 路径 A 核心；教程 [02](../tutorials/02-gnss-dualfreq-tec.md)·[09](../tutorials/09-dcb-biases-deep.md)·[16](../tutorials/16-practice-one-day-tec.md)
- 前处理：[georinex](./georinex.md)/[anubis](./anubis.md)
- 网格对照：[ionex-gim](./ionex-gim.md)；不规则体：[ionomoni](./ionomoni.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 未校准当绝对 TEC | 必须跑校准步骤 |
| 无 wheel / 版本不符 | 换 3.11–3.13；或装 Rust |
| 与 SH-GIM 作者混淆 | PyTECGg=viventriglia；SH-GIM=维护者 |
| 弧段被剔光 | 降 `min_arc_length` / 截止角 |
| 导航不覆盖 | 换混合 NAV 或匹配 DOY |
| GPLv3 | 再分发前读 LICENSE |
| Hatanaka 依赖缺失 | 按上游说明补依赖 |

## 相关工具

[georinex](./georinex.md) · [ionex-gim](./ionex-gim.md) · [ionomoni](./ionomoni.md) · [sh-gim](./sh-gim.md)

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
