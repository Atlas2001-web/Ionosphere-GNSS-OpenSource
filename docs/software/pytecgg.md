# PyTECGg

目录：[`PROJECTS.json` → `PyTECGg`](../../PROJECTS.json) · 上游 <https://github.com/viventriglia/PyTECGg> · 文档 <https://viventriglia.github.io/PyTECGg/> · GPL-3.0 · Python + Rust 核心 · Polars · **作者 viventriglia（非本仓维护者）** · 本机验证 **1.3.0**

> 操作手册。祈使句。**作者：viventriglia 等（不是本仓维护者自有项目）。** 勿与维护者 [SH-GIM](./sh-gim.md) 混淆。API 以上游文档 / 本机 `import pytecgg` 为准。

---

## 用途与边界

**用：**

- 从 RINEX OBS + NAV 做几何无关组合、弧段整平、硬件偏差估计与校准。
- 输出校准 **sTEC / vTEC**、站天顶 **veq**、弧段 **bias**（Polars DataFrame → parquet/csv）。
- 可编程批处理；GPS / Galileo / BeiDou / GLONASS；RINEX 2/3/4；内置 Hatanaka。
- 路径 A（一日 TEC）核心工具；教程 [02](../tutorials/02-gnss-dualfreq-tec.md) / [09](../tutorials/09-dcb-biases-deep.md) / [16](../tutorials/16-practice-one-day-tec.md)。

**不用 / 边界：**

- **不是**「只读盘探活」→ [georinex](./georinex.md)。
- **不是** ROTI / AATR 一体机 → [ionomoni](./ionomoni.md) / [oasis-roti](./oasis-roti.md)。
- **不是** 全球球谐 GIM 求解 → 开源 GIM；[sh-gim](./sh-gim.md) 仅边界（求解器未开源）。
- **不要**把未跑 `calculate_tec` 的相对 GF 当绝对 TEC 发表。
- **不要**把 parquet 当成 IONEX 交给 GIM 同化链。

一句话：PyTECGg = **校准绝对 TEC**；作者 viventriglia。

---

## 安装（多平台 + 报错）

### 共同要求

- Python **3.11–3.13**（以当前 PyPI / 文档为准）。
- 独立 venv；多数平台有 wheel；无 wheel 需 Rust 工具链按上游编译。

### Linux / macOS

```bash
cd ~/iono_ops
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install pytecgg polars
python -c "import pytecgg; print(pytecgg.__file__)"
python -c "from pytecgg.parsing import read_rinex_obs, read_rinex_nav; print('parsing_ok')"
```

### Windows（PowerShell）

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install pytecgg polars
python -c "import pytecgg; print(pytecgg.__file__)"
```

### 源码 / 无 wheel

按上游 README：装 Rust（`rustup`）后 `pip install -e .`。Docker Batch 见上游 Batch Processing 页。

### 安装期常见报错

| 现象 | 原因 | 修复 |
|---|---|---|
| `No matching distribution` | Python ∉ 3.11–3.13 | `python3.12 -m venv .venv` 重装 |
| 编译失败 / 缺 rustc | 无预编译 wheel | 装 rustup 后重装；或等官方 wheel |
| Hatanaka 相关失败 | 压缩依赖或文件坏 | 换普通 `.rnx`；`gunzip -t` |
| 可 import 但旧脚本炸 | API 演进 | 对照上游 quickstart 改 import |
| GPLv3 合规顾虑 | 再分发义务 | 读 LICENSE；商业集成先确认 |

### 安装验收

```bash
python -c "import pytecgg; from pytecgg import GNSSContext; print('ok')"
```

---

### 本机真实冒烟（pytecgg 1.3.0，短文件只验证解析）

样本：georinex 测试对 `14601736.18o` + `14601736.18n`（弧段极短，**不够校准**）。

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

df_obs, rec_pos, ver = read_rinex_obs(Path("14601736.18o"))
nav = read_rinex_nav(Path("14601736.18n"))
print("ver=", ver)
print("rec_pos=", rec_pos)
print("obs_shape=", df_obs.shape)
print("columns=", list(df_obs.columns))
print(df_obs.head(6))
print("observables=", sorted(df_obs["observable"].unique().to_list()))
ctx = GNSSContext(receiver_pos=rec_pos, receiver_name="stxx",
                  rinex_version=ver, systems=["G", "E"], h_ipp=350_000)
print("ctx=", ctx.receiver_name, ctx.systems, ctx.h_ipp)
summarise_rinex_data(df_obs, nav)
PY
```

**本机真实 stdout（截断）：**

```text
ver= 2.11
rec_pos= (-4647137.583, 2562189.6255, -3526626.7006)
obs_shape= (135, 4)
columns= ['epoch', 'sv', 'observable', 'value']
observables= ['C1', 'C2', 'L1', 'L2', 'P2']
ctx= stxx ['E', 'G'] 350000
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

短样本只够冒烟解析。下方为**本机真实全日校准**（同一套 API）。

### 本机真实校准（ABMF 全日 OBS + GPS NAV → stec/vtec/veq）

样本来源：Anubis 发行包内公开站日 `abmf0012.19o` + `abmf0012.19n`（ABMF / 2019-01-01 / 30 s；**GPS-only NAV**）。  
本机 **pytecgg 1.3.0**；作者 **viventriglia**。勿把下列 TECu 当气候学参考——站日/校准相关。

```bash
# 准备（路径按本机放置）
mkdir -p data out
# abmf0012.19o / .19n → data/

python - <<'PY'
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg import GNSSContext
from pytecgg.satellites import prepare_ephemeris, satellite_coordinates, calculate_ipp
from pytecgg.linear_combinations import calculate_linear_combinations
from pytecgg.tec_calibration import (
    extract_arcs, calculate_tec, calculate_vertical_equivalent,
)
from pytecgg.utils import summarise_rinex_data
import polars as pl

OBS = Path("data/abmf0012.19o")
NAV = Path("data/abmf0012.19n")
nav_dict = read_rinex_nav(NAV)
df_obs, rec_pos, ver = read_rinex_obs(OBS)
print("ver=", ver)
print("rec_pos=", rec_pos)
print("obs_shape=", df_obs.shape)
summarise_rinex_data(df_obs, nav_dict)

# NAV 仅 GPS → systems 必须对齐，否则坐标/弧段空
ctx = GNSSContext(
    receiver_pos=rec_pos, receiver_name="abmf",
    rinex_version=ver, h_ipp=350_000, systems=["G"],
)
ephem = prepare_ephemeris(nav_dict, ctx)
df_lc = calculate_linear_combinations(df_obs, ctx, selection_mode="availability")
df_coords = satellite_coordinates(df_lc["sv"], df_lc["epoch"], ephem)
df_arcs = extract_arcs(df_lc, ctx, min_arc_length=120).join(
    df_coords, on=["sv", "epoch"], how="left"
)
df_geom = calculate_ipp(df_arcs, ctx, min_elevation=20)
df_cal = calculate_tec(df_geom, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30)
df_veq = calculate_vertical_equivalent(
    df_cal, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30
)
want = ["epoch", "sv", "ele", "bias", "stec", "vtec", "veq"]
# 正午窗展示（夜间/弧段边缘可能非物理负值——须对照 GIM / 滤弧）
mid = df_veq.filter(
    (pl.col("epoch") >= pl.datetime(2019, 1, 1, 12, 0, 0, time_zone="UTC"))
    & (pl.col("epoch") < pl.datetime(2019, 1, 1, 12, 0, 30, time_zone="UTC"))
    & pl.col("stec").is_not_null()
)
print(mid.select(want).head(6))
print(
    df_veq.filter(
        (pl.col("epoch") >= pl.datetime(2019, 1, 1, 12, 0, 0, time_zone="UTC"))
        & (pl.col("epoch") < pl.datetime(2019, 1, 1, 12, 30, 0, time_zone="UTC"))
        & pl.col("stec").is_not_null()
    ).select(["stec", "vtec", "veq", "bias"]).describe()
)
out = Path("out/abmf0012_tec.parquet")
df_veq.write_parquet(out)
print("calibrated_shape=", df_veq.shape)
print("wrote", out, out.stat().st_size)
PY
```

**本机真实 stdout（截断；pytecgg 1.3.0）：**

```text
ver= 2.11
rec_pos= (2919786.448, -5383745.178, 1774604.734)
obs_shape= (744358, 4)
Temporal Coverage (OBS)
   - Start:    2019-01-01 00:00:00+00:00
   - End:      2019-01-01 23:59:30+00:00
   - Sampling: 30.0s
Constellations Breakdown (OBS)
Sys  | SVs  | Total Records   | Available Signals
E    | 18   | 262,680         | C1, C5, C7, C8, ... L1, L5, L7, L8, ...
G    | 31   | 306,076         | C1, C5, ... L1, L2, L5, P2, ...
R    | 23   | 175,602         | C1, ... L1, L2, P2, ...
Ephemeris Coverage (NAV)
   - GPS     :  31 satellites have at least an ephemeris

# midday 12:00 UTC（同历元 veq 跨星一致 ≈ 7.03）
epoch                   sv   ele        bias         stec       vtec      veq
2019-01-01 12:00:00 UTC G02  58.825002  -125.825077  7.876722   6.863228  7.029813
2019-01-01 12:00:00 UTC G05  38.483241   -56.288202  7.242082   4.854883  7.029813
2019-01-01 12:00:00 UTC G06  21.25371    -33.299955  15.745012  7.376916  7.029813
2019-01-01 12:00:00 UTC G13  80.526885   -57.547431  6.630081   6.548894  7.029813
2019-01-01 12:00:00 UTC G15  55.737224  -101.827595  10.119652  8.558109  7.029813
2019-01-01 12:00:00 UTC G29  38.971903   -64.14152   10.5795    7.150975  7.029813

# midday 12:00–12:30 describe（有限浮点；非全 null）
statistic  stec       vtec      veq       bias
count      344.0      344.0     344.0     344.0
mean       10.39672   7.45036   7.067332  -86.194448
50%        9.229433   7.576288  7.070261  -64.14152
min        6.509608   4.854099  6.963713  -146.473557
max        23.719208  11.478164 7.132936  -33.299955

calibrated_shape= (20216, 24)   # 含 bias/stec/vtec/veq
wrote out/abmf0012_tec.parquet 2110609
# 全日 null_stec=1698/20216；null_veq=0/20216
```

**读数要点（成功判据，勿抄数字当真值）：**

1. 列齐 `bias`/`stec`/`vtec`/`veq`；同历元 `veq` 跨星相同（上表 7.029813）。  
2. 正午窗 `stec/vtec/veq` 为正有限浮点；全日 parquet 非空。  
3. **GPS-only NAV** → `systems=["G"]`；OBS 里的 E/R 被丢掉是预期。要多系统换混合 BRDC。  
4. 夜间/弧段边缘可能出现负 `stec`（本机全日约四成负样）——先滤 `id_arc_valid`/`ele`，再和同日 [ionex-gim](./ionex-gim.md) 对照；**禁止**把未质控数写进论文。  
5. 无全日双频 OBS+覆盖 NAV 时：只跑上一节短文件解析，并在笔记写明「校准链未实跑」。


## 快速冒烟（10 分钟）

准备同日 OBS + 混合 NAV。先确认不是 HTML 登录页。

```bash
head -n 8 data/SITE.rnx
file data/SITE.rnx data/BRDC.rnx
# 期望：含 RINEX VERSION / TYPE；不要出现 <!DOCTYPE html>

python - <<'PY'
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg.utils import summarise_rinex_data

OBS = Path("data/SITE.rnx")
NAV = Path("data/BRDC.rnx")
nav = read_rinex_nav(NAV)
df_obs, rec_pos, ver = read_rinex_obs(OBS)
print("rec_pos", rec_pos)
print("rinex_version", ver)
print("obs rows", df_obs.height, "cols", df_obs.columns)
summarise_rinex_data(df_obs, nav)
PY
```

**期望：** ECEF 非全零；`summarise` 打出时间覆盖、各系统 SV 数、Available Signals、NAV 覆盖。  
**失败：** 空表 / 解析异常 → 先 [gfzrnx](./gfzrnx.md) `-chk` 或换完整日文件。

可选下载（网络可达、以上游函数为准）：

```python
from pathlib import Path
from pytecgg.utils import download_obs_euref, download_nav_bkg
download_obs_euref(station_code="BRUX", year=2025, doys=[1], output_path=Path("data"))
download_nav_bkg(year=2025, doys=[1], output_path=Path("data"))
```

---

## 完整工作流

### 工作流 A：单站一日 → 校准 stec/vtec/veq（路径 A 主链）

对应教程 [16](../tutorials/16-practice-one-day-tec.md)。建议前门禁：[anubis](./anubis.md) lite；可选 [gfzrnx](./gfzrnx.md) `-smp 30`。

```bash
mkdir -p out logs
python - <<'PY'
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg import GNSSContext
from pytecgg.satellites import prepare_ephemeris, satellite_coordinates, calculate_ipp
from pytecgg.linear_combinations import calculate_linear_combinations
from pytecgg.tec_calibration import (
    extract_arcs, calculate_tec, calculate_vertical_equivalent,
)

NAV = Path("data/BRDC00IGS_R_20240910000_01D_MN.rnx")
OBS = Path("data/YOUR00XXX_R_20240910000_01D_30S_MO.rnx")

nav_dict = read_rinex_nav(NAV)
df_obs, rec_pos, rinex_version = read_rinex_obs(OBS)
ctx = GNSSContext(
    receiver_pos=rec_pos,
    receiver_name=OBS.name[:4].lower(),
    rinex_version=rinex_version,
    h_ipp=350_000,          # 米；典型薄壳 350 km
    systems=["G", "E"],     # 可加 "C","R"；须 NAV 覆盖
)

ephem = prepare_ephemeris(nav_dict, ctx)
df_lc = calculate_linear_combinations(
    df_obs, ctx,
    selection_mode="availability",  # 或 "quality"
)
df_coords = satellite_coordinates(df_lc["sv"], df_lc["epoch"], ephem)
df_arcs = extract_arcs(
    df_lc, ctx,
    min_arc_length=120,     # 历元数；过严会剔光
).join(df_coords, on=["sv", "epoch"], how="left")
df_geom = calculate_ipp(df_arcs, ctx, min_elevation=20)

df_cal = calculate_tec(
    df_geom, ctx=ctx,
    max_polynomial_degree=3,
    batch_size_epochs=30,
)
df_veq = calculate_vertical_equivalent(
    df_cal, ctx=ctx,
    max_polynomial_degree=3,
    batch_size_epochs=30,
)

want = ["epoch", "sv", "id_arc_valid", "ele", "azi", "bias", "stec", "vtec", "veq"]
have = [c for c in want if c in df_veq.columns]
print(df_veq.select(have).head())
print(df_veq.select([c for c in ["stec", "vtec", "veq"] if c in df_veq.columns]).describe())

out = Path("out/tec_calibrated.parquet")
df_veq.write_parquet(out)
df_veq.write_csv("out/tec_calibrated.csv")
print("wrote", out, out.stat().st_size)
PY
```

**期望（结构判据，勿抄 TECu 数字）：**

```text
# head() 应出现 epoch / sv / ele / bias / stec / vtec / veq 等列
# describe() 中 stec/vtec/veq 为有限浮点，非全 null
wrote out/tec_calibrated.parquet <nbytes>
```

**成功判据：** 列含 `stec`/`vtec`/`veq`/`bias`；同历元 `veq` 跨星接近；量级通常数～数十 TECu（**站日相关，禁止照抄示例**）。全日空表 / 仅相对 `gflc_*` = 失败。短样本（如 30 s 测试文件）只够冒烟解析，不够稳定绝对 TEC。本机已用 ABMF 2019-01-01 实跑过一次（见上文「本机真实校准」）；换站日须重跑并自记 I/O。

### 工作流 B：多日连续（避免午夜假跳）

上游建议：先拼接多日 OBS，再进 `extract_arcs`，让弧段跨日界。

```bash
gfzrnx -finp data/SITE_*_MO.rnx -fout data/SITE_multi.rnx -kv -f
# 把工作流 A 的 OBS/NAV 换成 multi / 多日 BRDC
```

### 工作流 C：与 GIM 对照

同日 IONEX → [ionex-gim](./ionex-gim.md)；站附近 GIM VTEC 与 `veq` 同图。教程 [18](../tutorials/18-lab-compare-gims.md)。  
**期望：** 平静日趋势同向、量级同阶。差 10× → 查单位、薄壳、是否未校准、时间系。

### 工作流 D：批处理骨架

```bash
mkdir -p out logs scripts
# 将工作流 A 收成 scripts/run_pytecgg_one.py（--obs --nav --out）
for obs in data/*_MO.rnx; do
  b=$(basename "$obs")
  python scripts/run_pytecgg_one.py --obs "$obs" --nav data/BRDC.rnx \
    --out "out/${b}.parquet" 2>&1 | tee "logs/${b}.log" \
    || echo "FAIL $obs" | tee -a logs/fail.list
done
test -f logs/fail.list && cat logs/fail.list || echo all_ok
```

### 工作流 E：未校准 vs 校准对照

停在 `calculate_linear_combinations` / `extract_arcs` 只看 `gflc_*` → 相对量。再跑 `calculate_tec`，看散点是否对齐到同一 `veq`。

---

## 输入 / 输出与字段表

### 输入

| 类型 | 说明 |
|---|---|
| RINEX OBS | 2/3/4；可 Hatanaka/gz（能力以上游为准） |
| RINEX NAV | 须覆盖所选 `systems`；推荐混合 BRDC |
| `GNSSContext` | ECEF、站名、版本、`h_ipp`、系统列表 |

### `GNSSContext`

| 字段 | 含义 | 典型 |
|---|---|---|
| `receiver_pos` | ECEF 米 | `read_rinex_obs` 返回 |
| `receiver_name` | 站标识 | 常取文件名 4 字符 |
| `rinex_version` | 版本串 | 解析返回 |
| `h_ipp` | 薄壳高度（m） | `350_000`；出 [250,500] km 可能警告 |
| `systems` | 星座 | `["G","E"]` 或全名 |

### 关键处理参数

| 函数 | 参数 | 含义 | 典型 |
|---|---|---|---|
| `calculate_linear_combinations` | `selection_mode` | 频点策略 | `availability` / `quality` |
| | `combinations` | 组合 | `gflc_phase` `gflc_code` `mw` |
| | `band_overrides` | 强制频带 | `{"G": ("L1","L5")}` |
| `extract_arcs` | `min_arc_length` | 最短弧历元 | 默认 30；30 s 日文件常用 120 |
| | `threshold_abs/std/jump` | 周跳阈值 | 见文档；噪声站可放宽 |
| | `max_gap` | 失锁间隙 | `None`=自动 |
| `calculate_ipp` | `min_elevation` | 截止角° | 15–20 |
| `calculate_tec` / veq | `max_polynomial_degree` | 多项式阶 | 3 |
| | `batch_size_epochs` | 偏差批长 | 30 |

### 输出列（校准后）

| 列 | 含义 | 用途 |
|---|---|---|
| `epoch` / `sv` | 时 / 星 | 索引 |
| `id_arc_valid` | 有效弧 ID | 过滤 null |
| `gflc_levelled` | 整平 GF | 中间量 |
| `ele` / `azi` | 高度角 / 方位角 | 门控、图 |
| `bias` | 硬件偏差（TECu） | 诊断 |
| `stec` | 校准斜向 TEC | IPP 产品 |
| `vtec` | 映射垂直 TEC | 与 GIM 比量级 |
| `veq` | 站天顶等效 VTEC | 单站时序首选 |

### 明确不输出

ROTI、S4、`.pos`、IONEX 网格、全球球谐系数。

---

## 接到 tutorials / 工作流哪一步

| 场景 | 本手册 | 上下游 |
|---|---|---|
| 路径 A 一日 TEC | 工作流 A | data-access → georinex → 可选 gfzrnx/anubis → **pytecgg** → ionex-gim |
| 双频 / DCB | A + E | 教程 [02](../tutorials/02-gnss-dualfreq-tec.md) / [09](../tutorials/09-dcb-biases-deep.md) |
| 一日练习 | A | [16](../tutorials/16-practice-one-day-tec.md) |
| 与 GIM 实验 | C | [18](../tutorials/18-lab-compare-gims.md) |
| 磁暴 TEC | A | [20](../tutorials/20-storm-tec-analysis.md)；ROTI 另走 oasis/ionomoni |
| SH-GIM | 不串主链 | [sh-gim](./sh-gim.md) 仅边界 |

---

## 可操作坑（现象 → 原因 → 修复）

1. **stec/vtec 与 GIM 差约 10× 或量级离谱**  
   原因：跳过 `calculate_tec`；相对 GF 当绝对。  
   修复：确认调用校准；用 `veq`；对照 [ionex-gim](./ionex-gim.md)。

2. **`extract_arcs` 后行数 0**  
   原因：`min_arc_length` 过严 / 截止角过高 / 周跳狂。  
   修复：试 `min_arc_length=30`、`min_elevation=10`；先 Anubis。

3. **`No matching distribution for pytecgg`**  
   原因：Python 版本不符。  
   修复：换 3.11–3.13 venv。

4. **混淆作者 / 指望 SH-GIM 出同样产品**  
   原因：归属写错。  
   修复：PyTECGg=viventriglia；SH-GIM=本仓维护者且求解未开源。

5. **多系统空结果 / 坐标失败**  
   原因：OBS 有 C/E，NAV 只有 GPS。  
   修复：混合 BRDC；`systems` 与 NAV 对齐；先 `summarise_rinex_data`。

6. **改了 `h_ipp` 却和文献硬比**  
   原因：薄壳高度改映射。  
   修复：笔记写死高度；对照实验保持一致。

7. **Hatanaka / gz 读失败**  
   原因：半截下载或依赖。  
   修复：`gunzip -t`；必要时 `CRX2RNX`。

8. **接收机坐标错**  
   原因：头 APPROX 为 0 或错站。  
   修复：`print(rec_pos)`；用测站真值覆盖。

9. **批处理静默空 parquet**  
   原因：未断言 `height` / 出口码。  
   修复：断言含 `stec`；维护 `fail.list`。

10. **把 parquet 当 IONEX**  
    原因：格式混淆。  
    修复：单站时序用 parquet；网格走 ionex-gim。

11. **UTC / GPST 与事件表错位**  
    原因：口算磁暴时刻。  
    修复：统一时间系再裁剪。

12. **单频硬跑**  
    原因：无双频对。  
    修复：看 Available Signals；换站。

13. **API 照抄旧博客**  
    原因：函数签名变。  
    修复：以上游当前 quickstart 为准。

14. **跳过 QC 坏站出假漂亮曲线**  
    原因：多路径被校准「抹平」。  
    修复：Anubis 门禁；高 MP 弃用。

15. **GPLv3 未读就嵌闭源**  
    原因：许可义务。  
    修复：读 LICENSE。

16. **`band_overrides` 点了站上没有的频**  
    原因：信号假设错。  
    修复：先 summarise；改 `availability`。

17. **全日校准后大量负 `stec` / 与 GIM 差很多**  
    原因：弧段边缘、低高度角、仅单系统 NAV、或未滤 `id_arc_valid`。  
    修复：先看正午窗；滤 `ele` 与有效弧；换混合 BRDC；对照 [ionex-gim](./ionex-gim.md)。**不要**直接发表未质控数。

18. **有 E/R 观测却 `systems=["G","E"]` 后坐标失败**  
    原因：手头 NAV 只有 GPS（如本机 ABMF `.19n`）。  
    修复：`summarise_rinex_data` 看 Ephemeris Coverage；`systems` 与 NAV 对齐，或下载混合 BRDC。

---

## 同类选型

| 需求 | 选 |
|---|---|
| 校准绝对 sTEC/vTEC | **PyTECGg（viventriglia）** |
| 读 RINEX→xarray | georinex |
| ROTI / AATR | oasis-roti / ionomoni |
| 读 GIM | ionex-gim |
| 自建球谐 | 开源 GIM；SH-GIM 仅边界 |
| 坐标 | rtklib / pride-pppar |

---

## 操作检查清单

1. `import pytecgg` 成功；Python 版本符合。  
2. OBS/NAV 非 HTML；summarise 有双频与星历覆盖。  
3. 可选 gfzrnx / Anubis 通过。  
4. 工作流 A 产出非空 `stec/vtec/veq`。  
5. `h_ipp` / `systems` / 截止角写入笔记。  
6. 与同日 GIM 量级对照一眼。  
7. 批处理有 FAIL 列表。  
8. 引用与 GPL 已处理。  
9. 冲突时：**上游文档 > 本手册**。

---

## 附录 · 最小回归

```bash
#!/usr/bin/env bash
set -euo pipefail
test -f "${1:?obs}" && test -f "${2:?nav}"
python - <<PY
from pathlib import Path
from pytecgg.parsing import read_rinex_obs, read_rinex_nav
obs, pos, ver = read_rinex_obs(Path("$1"))
nav = read_rinex_nav(Path("$2"))
assert obs.height > 0 and len(pos) == 3
print("PASS", obs.height, ver, pos)
PY
```

---

## 相关

[README](./README.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [ionex-gim](./ionex-gim.md) · [sh-gim](./sh-gim.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · 教程 [02](../tutorials/02-gnss-dualfreq-tec.md) · [09](../tutorials/09-dcb-biases-deep.md) · [16](../tutorials/16-practice-one-day-tec.md)
