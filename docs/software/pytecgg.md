# PyTECGg

目录：[`PROJECTS.json` → `PyTECGg`](../../PROJECTS.json) · 上游 <https://github.com/viventriglia/PyTECGg> · 文档 <https://viventriglia.github.io/PyTECGg/> · GPL-3.0 · **作者 viventriglia（非本仓维护者）** · 本机验证 **1.3.0**

> 操作手册。祈使句。从 GNSS 观测重建并校准 TEC。API 以本机 `import pytecgg` 与上游 quickstart 为准。

## 1. 一句话用途

OBS+NAV → 几何无关组合 / 弧段 / 硬件偏差估计 → 校准 sTEC/vTEC（Polars DataFrame）。**不是**只读盘（→ [georinex](./georinex.md)），**不是** ROTI（→ [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)），**不是** GIM 球谐引擎（→ [sh-gim](./sh-gim.md) 边界）。

## 2. 安装（最少步骤）

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install pytecgg
python -c "import pytecgg, importlib.metadata as m; print(m.version('pytecgg'), pytecgg.__file__)"
python -c "from pytecgg.parsing import read_rinex_obs, read_rinex_nav; from pytecgg import GNSSContext; print('ok')"
```

| 现象 | 原因 | 修复命令 |
| --- | --- | --- |
| `No matching distribution` | Python ∉ 3.11–3.13 | `python3.12 -m venv .venv` 后重装 |
| 编译失败 / 缺 rustc | 无 wheel | 装 rustup 后 `pip install pytecgg` |
| 与旧教程 import 不符 | API 演进 | 对照上游 quickstart 改 import |

## 3. 端到端：解析 OBS/NAV + 摘要（本机真实跑通）

样本：`14601736.18o` + `14601736.18n`（短文件，验证解析链；完整校准需更长弧段）。

```bash
mkdir -p data && cd data
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
curl -fsSL -o 14601736.18n \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n

python - <<'PY'
from pathlib import Path
from pytecgg.parsing import read_rinex_obs, read_rinex_nav
from pytecgg import GNSSContext
from pytecgg.utils import summarise_rinex_data

obs_path = Path("14601736.18o")
nav_path = Path("14601736.18n")

df_obs, rec_pos, ver = read_rinex_obs(obs_path)
nav = read_rinex_nav(nav_path)
print("ver=", ver)
print("rec_pos=", rec_pos)
print("obs_shape=", df_obs.shape)
print("columns=", list(df_obs.columns))
print(df_obs.head(6))
print("observables=", sorted(df_obs["observable"].unique().to_list()))

ctx = GNSSContext(
    receiver_pos=rec_pos,
    receiver_name="stxx",
    rinex_version=ver,
    systems=["G", "E"],
    h_ipp=350_000,
)
print("ctx=", ctx.receiver_name, ctx.systems, ctx.h_ipp)
summarise_rinex_data(df_obs, nav)
PY
```

| 符号 | 含义 |
| --- | --- |
| `read_rinex_obs(path)` | → `(DataFrame, rec_pos_ecef, rinex_version)`；列 `epoch,sv,observable,value` |
| `read_rinex_nav(path)` | → `dict[str, DataFrame]`，键如 `GPS` |
| `receiver_pos` | 头近似 ECEF（m） |
| `receiver_name` | 站名；内部规范到小写≤4 字符 |
| `rinex_version` | 如 `2.11` |
| `systems` | `G/E/R/C` 或全名 |
| `h_ipp` | 薄壳高（m），默认 350000 |
| `summarise_rinex_data` | 打印时间覆盖、系统信号、星历覆盖 |

**本机真实 stdout（pytecgg 1.3.0，截断）：**

```text
ver= 2.11
rec_pos= (-4647137.583, 2562189.6255, -3526626.7006)
obs_shape= (135, 4)
columns= ['epoch', 'sv', 'observable', 'value']
shape: (6, 4)
┌─────────────────────────┬─────┬────────────┬──────────┐
│ epoch                   ┆ sv  ┆ observable ┆ value    │
│ 2018-06-22 06:17:30 UTC ┆ E07 ┆ C1         ┆ 2.5809e7 │
│ 2018-06-22 06:17:30 UTC ┆ E07 ┆ L1         ┆ 1.3563e8 │
│ 2018-06-22 06:17:30 UTC ┆ G03 ┆ C1         ┆ 2.2720e7 │
│ 2018-06-22 06:17:30 UTC ┆ G03 ┆ C2         ┆ 2.2720e7 │
└─────────────────────────┴─────┴────────────┴──────────┘
observables= ['C1', 'C2', 'L1', 'L2', 'P2']
ctx= stxx ['E', 'G'] 350000
=======================================================
GNSS RINEX DATA SUMMARY
=======================================================
Temporal Coverage (OBS)
   - Start:    2018-06-22 06:17:30+00:00
   - End:      2018-06-22 06:18:00+00:00
   - Sampling: 15.0s
Constellations Breakdown (OBS)
Sys  | SVs  | Total Records   | Available Signals
E    | 2    | 12              | C1, L1
G    | 6    | 63              | C1, C2, L1, L2, P2
R    | 5    | 60              | C1, C2, L1, L2
Ephemeris Coverage (NAV)
   - GPS     :   7 satellites have at least an ephemeris
```

短文件只有 GPS NAV、弧段极短——**够验证解析，不够稳定绝对 TEC**。完整校准按上游 calibration quickstart 用一日双频站+混合星历。

## 4. 可选进阶：校准入口（需长数据）

```python
# 函数名以你安装版本的文档为准；此处不编造 TEC 数值
# from pytecgg.tec_calibration import ...
# tec = calibrate_...(df_obs, nav, ctx)
# tec.write_parquet("out/stec.parquet")
```

缺双频对时先换站文件，不要硬跑。

## 5. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复命令 |
| --- | --- | --- | --- |
| 1 | `ModuleNotFoundError: pytecgg` | 错 venv | `source .venv/bin/activate; pip install pytecgg` |
| 2 | NAV 摘要无 Galileo | GPS-only NAV | `python -c "from pytecgg.parsing import read_rinex_nav; print(read_rinex_nav('BRDC.rnx').keys())"` |
| 3 | 无双频对 | OBS 缺 L2/C2 | 跑 `summarise_rinex_data`；换站 |
| 4 | `h_ipp` UserWarning | 薄壳高异常 | `GNSSContext(..., h_ipp=350_000)` |
| 5 | 把 GF 当绝对 TEC 发表 | 未走校准 | 按上游 calibration quickstart 跑完 |
| 6 | Hatanaka 失败 | 压缩/依赖 | `gunzip -c f.crx.gz > f.crx` 或换明文 |
| 7 | 与 georinex Dataset 混用 | Polars long vs xarray | 校准链只用 `pytecgg.parsing` |
| 8 | GPLv3 再分发顾虑 | 许可证义务 | 读上游 LICENSE |

## 6. 接到哪一步

- 教程 [02](../tutorials/02-gnss-dualfreq-tec.md) · [09](../tutorials/09-dcb-biases-deep.md) · [16](../tutorials/16-practice-one-day-tec.md)
- 读盘探活 → [georinex](./georinex.md)；预处理 → [gfzrnx](./gfzrnx.md)
- ROTI → [oasis-roti](./oasis-roti.md)；GIM 对照 → [ionex-gim](./ionex-gim.md)
- 数据门户 → [data-access](../data-access.md)