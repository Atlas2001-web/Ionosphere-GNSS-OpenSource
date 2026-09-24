# gnsstools · 轻量 RINEX/SP3 → pandas 操作手册

目录：[`PROJECTS.json` → `gnsstools`](../../PROJECTS.json) · 上游 <https://github.com/arthurdjn/gnsstools> · 许可 **MIT** · 本机验证 **0.0.1**（tip **`e496093`**，2026-09-24 EDT）· **PyPI 无可用发行**（`pip install gnsstools` → No matching distribution；`pypi.org/pypi/gnsstools/json` → **404**）

> 岗位：教学/原型向 **RINEX 2/3 OBS·NAV + SP3 → pandas**；附 `gnsstime` 与（依赖 Beilin `gnsstoolbox` 的）轨道实验壳。冲突时：**上游 README / 源码 `rinex.load` > 本文**。对照生产读库 → [georinex](./georinex.md)；对照另一 pandas 教学栈 → [gnsspy](./gnsspy.md)。**不是** EarthScope Go 库 `EarthScope-gnsstools`。

## 1. 用途与边界

**做：**

- 统一入口 `rinex.load(path)`：RINEX 2 OBS（`.**o`）、RINEX 3 OBS（`*O.rnx`）、RINEX 2/3 NAV、`.SP3`
- 返回带 MultiIndex `(System, PRN, Date)` 的 pandas 子类（OBS / NAV / SP3）
- `gnsstime`：doy / MJD / GPS 周秒等
- NAV：`df.select("G", prn, gnsstime(...))` → `GPS`/`Galileo`/… 对象（星历字段）
- 可选：未知类型时回退 **georinex**（若已安装）

**不做：**

- **不是** 生产级 RINEX→xarray / NetCDF / 时间切片主力 → [georinex](./georinex.md)
- **不是** RINEX 2↔3 转换 / 产品下载菜单 → [gnsspy](./gnsspy.md)
- **不是** Hatanaka `.crx` 官方工具 → [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md)（上游 README 标 Compact *WIP*）
- **不是** 发表级 PPP / 实时流 → [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md) / [pygnssutils](./pygnssutils.md)
- 卫星 `position()` / 完整定位链：**上游标 WIP**；本机 `NotImplementedError`

一句话：gnsstools = **轻量 pandas 读器 + 教学时间/星历壳**；大规模读切片用 georinex，转换/批处理用 gnsspy。

| 术语 | 含义 |
| --- | --- |
| `rinex.load` | 按头 `Type`/`Version` 分派 OBS2/OBS3/NAV/SP3 |
| `ObservationDataFrame` | OBS；列如 `C1`/`L1`/… + `Session` |
| `NavigationDataFrame` | NAV；多系统星历列（`sqrtA`/`IODE`/…） |
| `PositionDataFrame` | SP3；`Clock` + Shapely `POINT Z` + `Session` |
| `gnsstoolbox` | Jacques Beilin 教学库；`Orbit` 基类依赖（PyPI 名 `gnsstoolbox`） |

## 2. 安装

上游 README 写 `pip install gnsstools`，**本机 2026-09-24 不可用**。仓内 **无** `setup.py` / `pyproject.toml`，用 clone + `PYTHONPATH`。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
# 勿死跟仓内 requirements.txt（numpy==1.16.6 / pandas==1.0.5，现代 Python 装不上）
python -m pip install pandas numpy shapely gpstime gnsstoolbox
git clone --depth 1 https://github.com/arthurdjn/gnsstools.git
export PYTHONPATH="$HOME/iono_ops/gnsstools:$PYTHONPATH"
python -c "import gnsstools; print(gnsstools.__version__, gnsstools.__file__)"
# 期望：0.0.1  .../gnsstools/gnsstools/__init__.py
```

样例数据在作业压缩包（不在仓根 `data/`）：

```bash
cd ~/iono_ops/gnsstools
unzip -qo assignments/DujardinArthurGNSS.zip 'notebooks/data/*' -d /tmp/gnsstools_samples
ls /tmp/gnsstools_samples/notebooks/data/
# edf1285b.18o  BRDC00IGS_R_20182850000_01D_MN.rnx  COM20225_15M.SP3
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution: gnsstools` | PyPI JSON 404 | clone + `PYTHONPATH`（上表） |
| `ModuleNotFoundError: gnsstoolbox` | `import gnsstools` 必拉 `Orbit` | `pip install gnsstoolbox`（另需 `gpsdatetime`） |
| `ModuleNotFoundError: gpstime` | `orbits/orbit.py` import | `pip install gpstime` |
| `neither setup.py nor pyproject.toml` | 无包装元数据 | 不要 `pip install .`；用 `PYTHONPATH` |
| `SyntaxWarning: invalid escape` | `obs2.py`/`sp3.py` 等旧正则 | 可忽略；不影响本页读数 |

## 3. 端到端：样例 OBS / NAV / SP3（本机真跑）

数据：上游 zip 内 `edf1285b.18o`、`BRDC00IGS_R_20182850000_01D_MN.rnx`、`COM20225_15M.SP3`。数值为 **本机 tip `e496093` / 0.0.1**（2026-09-24 EDT），非示意。

### 3.1 `gnsstime` 冒烟

```bash
export PYTHONPATH="$HOME/iono_ops/gnsstools:$PYTHONPATH"
python - <<'PY'
from gnsstools import gnsstime, __version__
print(__version__)
d = gnsstime(2018, 10, 12, 0, 40, 15)
print(d, "doy", d.doy, "mjd", float(d.mjd), "weeks0", d.weeks0)
PY
```

**本机 stdout：**

```text
0.0.1
2018-10-12 00:40:15 doy 285 mjd 58403.02795138889 weeks0 2022
```

### 3.2 RINEX 2 OBS → DataFrame

`rinex.load` **总会 `print(header)`**（见坑）。下面用 `redirect_stdout` 只展示断言数字。

```bash
python - <<'PY'
import io
from contextlib import redirect_stdout
from gnsstools import rinex
path = "/tmp/gnsstools_samples/notebooks/data/edf1285b.18o"
buf = io.StringIO()
with redirect_stdout(buf):
    df = rinex.load(path)
print(buf.getvalue().strip().splitlines()[0][:140])
print("shape", df.shape)
print("cols", list(df.columns))
print("E7 C1", float(df.loc[("E", 7, "2018-10-12 01:00:15"), "C1"]))
print("E7 L1", float(df.loc[("E", 7, "2018-10-12 01:00:15"), "L1"]))
PY
```

**本机关键输出：**

```text
OrderedDict({'Version': 2.11, 'Type': 'O', 'TypeName': 'OBSERVATION', 'System': 'M', 'SystemName': 'MIXED', 'PGM': 'GPP.eLL V3.02', 'RunBy': 'ESNG-ePTS', ...
shape (5745, 15)
cols ['C1', 'C2', 'C5', 'D1', 'D2', 'D5', 'L1', 'L2', 'L5', 'P1', 'P2', 'S1', 'S2', 'S5', 'Session']
E7 C1 28344990.66
E7 L1 148953923.97305
```

对照 [georinex](./georinex.md) 1.16.2 同文件：`C1` @ `E07` / `2018-10-12T01:00:15` = **28344990.66**（一致）。

### 3.3 RINEX 3 混合 NAV → `select`

NAV 读取时 stderr/stdout 会刷 `\r{cursor}` 进度（`nav.py`）；应用 `redirect_stdout` 或忽略。

```bash
python - <<'PY'
import io
from contextlib import redirect_stdout
from gnsstools import rinex, gnsstime
path = "/tmp/gnsstools_samples/notebooks/data/BRDC00IGS_R_20182850000_01D_MN.rnx"
with redirect_stdout(io.StringIO()):
    df = rinex.load(path)
print("shape", df.shape)
print("systems", df.index.get_level_values("System").value_counts().to_dict())
date = gnsstime(2018, 10, 12, 0, 40, 15)
sat = df.select("G", 2, date)
print(type(sat).__name__, sat.system, sat.prn)
print("sqrt_a", sat.sqrt_a, "e", sat.e, "iode", sat.iode)
print("af0", sat.sv_clock_bias)
try:
    sat.position(date)
except NotImplementedError as e:
    print("position:", e)
PY
```

**本机关键输出：**

```text
shape (7480, 48)
systems {'E': 5918, 'R': 1144, 'G': 418}
GPS G 2
sqrt_a 5153.57457924 e 0.0182396549499 iode 34.0
af0 -2.73766927421e-05
position: This method is currently not available. Make a PR if you wish to update gnsstools.
```

首行头（未重定向时）：`OrderedDict({'Version': 3.03, 'Type': 'N', ... 'PGM': 'MergeMNfile.tcl', 'RunBy': 'IGS', ...})`。

### 3.4 SP3 → Shapely 点

```bash
python - <<'PY'
import io
from contextlib import redirect_stdout
from gnsstools import rinex
path = "/tmp/gnsstools_samples/notebooks/data/COM20225_15M.SP3"
buf = io.StringIO()
with redirect_stdout(buf):
    df = rinex.load(path)
print("hdr", repr(buf.getvalue().strip()))
print("shape", df.shape, "epochs", df.index.get_level_values("Date").nunique(),
      "sv", df.index.droplevel("Date").nunique())
row = df.loc[("G", 1, "2018-10-12 00:00:00")]
pt = row["Position"]
print("clock", float(row["Clock"]), "xyz_km", pt.x, pt.y, pt.z)
PY
```

**本机关键输出：**

```text
hdr 'OrderedDict()'
shape (4947, 3) epochs 97 sv 51
clock -99.264764 xyz_km -17852.839089 -6014.552104 18675.30968
```

| 字段 | 含义（本文件） |
| --- | --- |
| `Clock` | SP3 钟差列（样例 G01 首历元 **-99.264764**） |
| `Position` | Shapely `POINT Z (X Y Z)`，单位与 SP3 正文一致（**km**） |
| `Session` | 历元序号 |

## 4. I/O 字段速查

| 产物 | 索引 | 主要列 |
| --- | --- | --- |
| OBS | `(System, PRN, Date)` | `C1`/`L1`/…、`Session`；头在 `df.attrs` |
| NAV | 同上 | `sqrtA`/`e`/`IODE`/`M0`/…（48 列）；`select` → 卫星对象 |
| SP3 | 同上 | `Clock`、`Position`、`Session`；头常为空 `OrderedDict()` |

输入：明文 RINEX/SP3 路径（整文件读入内存）。输出：pandas；**无 CLI**。

## 5. 参数 / API

| 符号 | 作用 |
| --- | --- |
| `rinex.load(filename)` | 自动分派；未知类型尝试 `georinex.load` |
| `gnsstime(y,m,d,H,M,S)` | 继承 `datetime`；支持 str/float 混入 |
| `date.doy` / `.mjd` / `.weeks0` | 年积日 / MJD / 自 GPS0 周数 |
| `df.select(const, prn, date)` | 最近星历 → `satellites.*` 实例 |
| `force` / `*args` | `load` 签名有，但主路径未深度使用 |

## 6. 接到哪步（vs georinex / gnsspy）

```text
样例/站日 RINEX·SP3
   ├─ 快速 pandas 探活 / 课堂 demos → gnsstools（本页）
   ├─ 生产切片 / NetCDF / Hatanaka 流水 → georinex (+ hatanaka)
   ├─ 2↔3 转换 / 交互菜单 / CLK·IONEX → gnsspy
   └─ TEC / 定位 / QC → gnss-tec·pytecgg / rtklib·pride / anubis
```

工作流：下载（[fast](./fast.md)/[gdds](./gdds.md)/[data-access](../data-access.md)）→（可选本页探活）→ [georinex](./georinex.md) 主读 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)。

## 7. 坑（≥8）

1. **`pip install gnsstools` 失败**：PyPI 无包；README 过时。
2. **无 `setup.py`**：`pip install .` 直接拒绝；必须 `PYTHONPATH`。
3. **`import gnsstools` 强依赖 `gnsstoolbox` + `gpstime`**：缺一即崩在 `orbits/orbit.py`。
4. **`requirements.txt` 钉死古代 numpy/pandas**：现代解释器请装当前 wheel，勿照抄 pin。
5. **`rinex.load` 无条件 `print(header)`**：脚本日志会被污染；重定向或改源码。
6. **NAV 刷屏 `\r{cursor}`**：大混合星历文件终端乱闪；重定向 stdout。
7. **`select(...).position()` → `NotImplementedError`**：卫星定位未完工；别当 PPP 引擎。
8. **SP3 `Position` 是 Shapely 几何**：不是 `(X,Y,Z)` 元组；取 `.x/.y/.z`；单位 **km**。
9. **SP3 头常为 `OrderedDict()`**：`df.attrs` 空；元数据别指望从 attrs 拿。
10. **Compact / `.crx` 未实现**：需预解压或改走 georinex/hatanaka。
11. **易与 EarthScope `gnsstools`（Go）混淆**：本页仅 `arthurdjn/gnsstools`。
12. **整文件读入**：GB 级 high-rate 会吃内存；生产请 georinex 限时间窗。

## 8. 选型

| 场景 | 选 |
| --- | --- |
| 课堂/脚本：OBS+NAV+SP3 → pandas，立刻看表 | **gnsstools** |
| 生产读、切片、NetCDF、gz/crx | **georinex** |
| RINEX 2↔3、IONEX/CLK、交互工具箱 | **gnsspy** |
| 官方 Hatanaka | **rnxcmp** / pip **hatanaka** |
| 定位 / TEC 产品 | **rtklib** / **pride-pppar** / **pytecgg** |

