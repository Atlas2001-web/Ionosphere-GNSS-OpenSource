# georinex · RINEX → xarray 操作手册

目录：[`PROJECTS.json` → `georinex`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/georinex> · MIT · 依赖 xarray / numpy · 本机验证 **1.16.2**

> 岗位：把 RINEX OBS/NAV 读进 Python。本页对照 **georinex 1.16.x**（`python -m georinex.read -h`）。CLI 模块名是 **`georinex.time`**，不是旧文档里的 `georinex.gtime`。

## 1. 用途与边界

**做：** RINEX 2/3/4 OBS·NAV（含常见 `.gz` / Hatanaka `.crx`）→ `xarray.Dataset`；时间探活；按系统/时间/观测量过滤；写出 NetCDF 供重复实验。

**不做：** 校准 TEC（→ [pytecgg](./pytecgg.md)，作者 **viventriglia**）；ROTI（→ [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)）；定位（→ [rtklib](./rtklib.md)）；QC 报表（→ [anubis](./anubis.md)）；拼日/抽稀正式产品（→ [gfzrnx](./gfzrnx.md)）。

一句话：读与切片，不是科学产品引擎。

## 2. 安装

```bash
cd ~/work
python3 -m venv .venv && source .venv/bin/activate   # Windows: py -3.11 -m venv .venv && .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install georinex hatanaka netCDF4 xarray numpy
python -c "import georinex as gr; print(getattr(gr,'__version__','?'), gr.__file__)"
python -m georinex.time -h | head
python -m georinex.read -h | head -n 25
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python < 3.10 | 换 3.10+ |
| `ModuleNotFoundError: hatanaka` | 未装 Hatanaka 绑定 | `pip install hatanaka`；或系统装 `CRX2RNX` 并预转换 |
| `Microsoft Visual C++` / netCDF4 编译失败 | 缺预编译 wheel | `pip install netCDF4`（优先 wheel）；Conda：`conda install -c conda-forge netcdf4` |
| 可 import、CLI 无模块 | 激活了错的 venv | `which python`；重新 `source .venv/bin/activate` |

## 3. 端到端：最小 OBS → Dataset → NetCDF

下面用本机造的 **3 历元 / 2 星 / RINEX 2.11** 文件跑通。数值为 **真实 georinex 1.16.2 输出**（不是示意）。



### 3.0 备选样本：上游 demo.10o（本机 1.16.2 真跑）

```bash
curl -fsSL -o data/demo.10o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/demo.10o
python -m georinex.time data/demo.10o
```

真实 stdout：

```text
filename: start, stop, number of times, interval
demo.10o: 2010-03-05T00:00:00 2010-03-05T00:00:30 2 30.0
['2010-03-05T00:00:00.000' '2010-03-05T00:00:30.000']
```

```bash
rm -f data/demo_G.nc
python -m georinex.read data/demo.10o -u G -m L1 C1 -o data/demo_G.nc
```

真实尾部：`saving OBS: .../demo_G.nc`；`Dimensions: (time: 2, sv: 10)`；`L1`/`C1`；`rxmodel: ASHTECH UZ-12`。

读回：

```bash
python -c "import xarray as xr; ds=xr.open_dataset('data/demo_G.nc', group='OBS'); print(dict(ds.sizes), list(ds.data_vars)); print(float(ds['L1'].sel(sv='G07').isel(time=0))); ds.close()"
```

本机：`{'time': 2, 'sv': 10}`；`L1 G07 t0 118767195.326`。

### 3.1 准备最小文件（或换成你的站文件）

路径占位：`data/mini.24o`。内容要点：头含 `# / TYPES OF OBSERV`，历元行后每个观测量占 **16 列**（F14.3 + LLI + SSI）。完整样例可自造；真实站文件从 [data-access](../data-access.md) 取。

```bash
mkdir -p data logs
head -n 8 data/mini.24o
# 期望：首行含 RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
file data/mini.24o
```

### 3.2 时间探活（坏文件最先死在这里）

```bash
python -m georinex.time data/mini.24o
```

**真实输出（本机 1.16.2）：**

```text
filename: start, stop, number of times, interval
mini.24o: 2024-01-01T00:00:00 2024-01-01T00:01:00 3 30.0
['2024-01-01T00:00:00.000' '2024-01-01T00:00:30.000'
 '2024-01-01T00:01:00.000']
```

| 字段 | 含义 |
| --- | --- |
| `start` / `stop` | 首末历元（文件时间系，此处 GPS） |
| `number of times` | 历元个数（此处 3） |
| `interval` | 推断采样秒（此处 30.0） |
| 末行列表 | 每个历元的 ISO 时间 |

空文件 / HTML 伪下载：无有效行或抛解码错 → 先修数据，不要改 georinex。

### 3.3 全量 `gr.load` 并读懂 Dataset

```bash
python - <<'PY'
import georinex as gr
obs = gr.load("data/mini.24o")
print(obs)
print("sizes", dict(obs.sizes))
print("vars", list(obs.data_vars))
print("sv", list(map(str, obs.sv.values)))
print("C1 G01", obs["C1"].sel(sv="G01").values)
PY
```

**真实输出（节选）：**

```text
<xarray.Dataset> Size: 240B
Dimensions:  (time: 3, sv: 2)
Coordinates:
  * time     (time) datetime64[ns] ... 2024-01-01 ... 2024-01-01T00:01:00
  * sv       (sv) <U3 'G01' 'G02'
Data variables:
    C1       (time, sv) float64 ...
    L1       (time, sv) float64 ...
    C2       (time, sv) float64 ...
    L2       (time, sv) float64 ...
Attributes:
    version:          2.11
    interval:         30.0
    rinextype:        obs
    time_system:      GPS
    filename:         mini.24o
    position:         [1113190.6473, -4842354.8842, 3984621.3094]
sizes {'time': 3, 'sv': 2}
vars ['C1', 'L1', 'C2', 'L2']
sv ['G01', 'G02']
C1 G01 [20234567.123 20234600.111 20234650.555]
```

| 名 | 含义 | 操作注意 |
| --- | --- | --- |
| `time` | 历元坐标 | 与 IONEX/事件对齐前先统一 GPST/UTC |
| `sv` | 卫星 ID（`G01`…） | 过滤后仍是出现过的星 |
| `C1`/`L1`/… | 伪距(m) / 相位(cycle) | RINEX3 常为 `C1C`/`L1C`/`L2W`——**先 print 再写 meas** |
| `attrs.version` | 文件版本 | 2.11 vs 3.xx 决定变量命名 |
| `attrs.position` | 头里 APPROX POSITION XYZ | 粗坐标，不是精密解 |
| `attrs.interval` | 头 INTERVAL | 与 `diff(time)` 交叉核对 |

### 3.4 过滤：`use` / `meas` / `tlim`（每个参数）

```bash
python - <<'PY'
import georinex as gr
obs = gr.load(
    "data/mini.24o",
    use="G",                          # 只保留 GPS；可传集合 {"G","E"}
    meas=["C1", "L1", "C2", "L2"],  # 白名单；RINEX3 改成文件真实名
    tlim=("2024-01-01", "2024-01-01T00:00:45"),  # [start, stop)
)
print(obs)
print(dict(obs.sizes))  # 期望 time:2（00:00 与 00:00:30）
PY
```

**真实结果：** `Dimensions: (time: 2, sv: 2)`，变量仍为 `C1 L1 C2 L2`。

| 参数 | 作用 | 错用后果 |
| --- | --- | --- |
| `use` | 系统字母 G/E/C/R/J/I/S | 写成 `"GPS"` → 空或 KeyError |
| `meas` | 只载入这些观测量 | 名字不在文件里 → 缺变量 / KeyError |
| `tlim` | 时间窗 | 顺序反或越界 → `time: 0` |
| `interval` | 读时每隔 N 秒取历元 | 非正式抽稀；对外分发用 gfzrnx `-smp` |
| `useindicators` | 载入 LLI/SSI | 默认常关；做周跳迹象分析再开 |
| `fast` | RINEX2 预分配加速 | 异常时改 `False`（CLI：`-strict`） |
| `verbose` | 日志 | CLI：`-v` |

### 3.5 CLI 等价路径（旗标逐项）

```bash
python -m georinex.read data/mini.24o \
  -u G \
  -m C1 L1 C2 L2 \
  -t 2024-01-01 2024-01-01T00:00:45 \
  -o data/mini_G.nc \
  -v
```

| 旗标 | 对应 API | 作用 |
| --- | --- | --- |
| `rinexfn`（位置参数） | `gr.load(path)` | 输入路径 |
| `-u` / `--use` | `use=` | 系统过滤 |
| `-m` / `--meas` | `meas=` | 观测量白名单 |
| `-t` / `--tlim` | `tlim=` | 两个时间戳 |
| `-o` / `--out` | 写出 NetCDF | 目录或文件 |
| `-v` | `verbose=True` | 打每个历元进度 |
| `-p` / `--plot` | 画图 | 需图形环境 |
| `-useindicators` | `useindicators=True` | LLI/SSI |
| `-strict` | 关闭投机预分配 | 慢但稳 |
| `-interval N` | `interval=N` | 读时抽稀秒 |

**真实 CLI 尾部：** `saving OBS: .../out.nc` 后打印与 `gr.load` 相同的 Dataset 摘要。

读回缓存用 **xarray**（`gr.load(.nc)` 在部分版本会报 `No data of known format`）：

```bash
python - <<'PY'
import xarray as xr
ds = xr.open_dataset("data/mini_G.nc")  # 若报错试 group="OBS"
print(dict(ds.sizes), list(ds.data_vars))
print("finite L1", float((__import__("numpy").isfinite(ds["L1"]).mean())))
ds.close()
PY
```

### 3.6 接到下游

- 校准 TEC：把**原始 RINEX**（不是 nc）交给 [pytecgg](./pytecgg.md)（viventriglia）
- 清洗/抽稀：先 [gfzrnx](./gfzrnx.md)，再回来探活
- QC：[anubis](./anubis.md) → 通过后再 load
- 定位：[rtklib](./rtklib.md)

教程：[02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md)

## 4. 输入 / 输出速查

| 输入 | 形态 |
| --- | --- |
| OBS | `.obs` `.##o` `.rnx` `.rnx.gz` `.crx` `.crx.gz` |
| NAV | `.nav` `.##n` 混合 NAV |
| 缓存 | `.nc`（用 xarray 读回更稳） |

NAV：`nav = gr.load("brdc.rnx")` → **先 `print(nav)`** 再取字段；georinex 不算卫星 ECEF 轨迹。

明确不输出：IONEX、ROTI、`.pos`、校准 STEC/VTEC。

## 5. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复命令 / 动作 |
| --- | --- | --- | --- |
| 1 | `KeyError: 'L1'` / 缺 `L1C` | RINEX2/3 命名不同 | `print(list(obs.data_vars))` 再写 `meas=` |
| 2 | `sizes time:0 sv:0` | 空窗 / 坏文件 / 滤光过狠 | `python -m georinex.time FILE`；放宽 `tlim`/`use` |
| 3 | `KeyError: system type {'G'}` | 头里无该系统的 `SYS / # / OBS TYPES` | 查头；或不要 `use=` 先全量 |
| 4 | OOM / 被 kill | 1 Hz 全日进内存 | 加 `use`/`tlim`/`meas`；或 `gfzrnx -smp 30` |
| 5 | `.crx` 读失败 | 无 hatanaka | `pip install hatanaka` 或 `CRX2RNX in.crx` |
| 6 | `head` 见 `<html` | 下载成登录页 | 重走 Earthdata/CDDIS 鉴权 |
| 7 | `gunzip: not in gzip format` | 扩展名假 `.gz` | 改名或直接当明文 RINEX 读 |
| 8 | nc 与源不一致 | 源更新后未重建 | `rm data/*.nc` 后重跑 read |
| 9 | `use='GPS'` 失败 | 系统码是单字母 | `use="G"` |
| 10 | 周跳分析全空 | 未载 LLI | `useindicators=True` 或 `-useindicators` |
| 11 | 下游 TEC 离谱 | 把相对相位差当绝对 TEC | 换 [pytecgg](./pytecgg.md) |
| 12 | Windows 路径炸 | 反斜杠进普通字符串 | `pathlib.Path` 或原始字符串 |
| 13 | CLI `No module named georinex.gtime` | 旧文档模块名 | 用 `python -m georinex.time` |
| 14 | `gr.load("*.nc")` ValueError | 该版本不把 nc 当 RINEX | `xr.open_dataset` |

## 6. 选型（一行）

| 需求 | 选 |
| --- | --- |
| Python → xarray | **georinex** |
| 拼日/抽稀/改版本 | **gfzrnx** |
| QC 报表 | **anubis** |
| 校准 TEC | **pytecgg**（viventriglia） |

## 7. 相关

[gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [rtklib](./rtklib.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [ionex-gim](./ionex-gim.md)
