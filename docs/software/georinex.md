# georinex

目录：[`PROJECTS.json` → `georinex`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/georinex> · MIT · 本机验证 **1.16.2**

> 操作手册。祈使句。把 RINEX 读进 Python。以本机 `python -m georinex.time -h` / `python -m georinex.read -h` 为准。**1.16.x 模块名是 `georinex.time`，不是旧文 `georinex.time`。**

## 1. 一句话用途

读 RINEX OBS/NAV（含 `.gz` / Hatanaka `.crx`）→ `xarray.Dataset`；探时间覆盖；按系统/观测量过滤；可选落 NetCDF。**不算**校准 TEC（→ [pytecgg](./pytecgg.md)，作者 viventriglia）、ROTI（→ [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)）、定位（→ [rtklib](./rtklib.md)）、拼日抽稀（→ [gfzrnx](./gfzrnx.md)）、QC 报表（→ [anubis](./anubis.md)）。

## 2. 安装（最少步骤）

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install georinex hatanaka netCDF4 xarray numpy
python -c "import georinex as gr; print(gr.__version__, gr.__file__)"
python -m georinex.time -h | head
python -m georinex.read -h | head -n 25
```

| 现象 | 原因 | 修复命令 |
| --- | --- | --- |
| `No matching distribution` | Python < 3.10 | `python3.11 -m venv .venv` 后重装 |
| `ModuleNotFoundError: hatanaka` | 未装 Hatanaka | `pip install hatanaka` |
| `No module named georinex.time` | 旧文档模块名 | `python -m georinex.time FILE` |
| 可 import、CLI 无模块 | 激活错 venv | `which python; source .venv/bin/activate` |

## 3. 端到端（本机真实跑通）

样本：上游 [`demo.10o`](https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/demo.10o)（RINEX 2.11，2 历元）。

```bash
mkdir -p data && cd data
curl -fsSL -o demo.10o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/demo.10o
head -n 5 demo.10o
# 期望：首行含 RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
```

### 3.1 时间探活

```bash
python -m georinex.time demo.10o
```

| 参数 | 含义 |
| --- | --- |
| `demo.10o` | 位置参数：RINEX 路径 |
| `-glob …`（可选） | 多文件通配 |

**本机真实 stdout（georinex 1.16.2）：**

```text
filename: start, stop, number of times, interval
demo.10o: 2010-03-05T00:00:00 2010-03-05T00:00:30 2 30.0
['2010-03-05T00:00:00.000' '2010-03-05T00:00:30.000']
```

| 字段 | 含义 |
| --- | --- |
| `start` / `stop` | 首末历元 |
| `number of times` | 历元数（此处 2） |
| `interval` | 推断采样秒（30.0） |
| 末行列表 | 每个历元 ISO 时间 |

### 3.2 过滤读取并写 NetCDF

```bash
rm -f demo_G.nc
python -m georinex.read demo.10o -u G -m L1 C1 -o demo_G.nc
```

| 旗标 | 含义 |
| --- | --- |
| 位置参数 | 输入 RINEX |
| `-u` / `--use` | 系统字母：`G C E S J R I` |
| `-m` / `--meas` | 观测量白名单 |
| `-o` / `--out` | 写出 NetCDF4；组名 `OBS` |
| `-t T0 T1` | 时间窗 |
| `-useindicators` | 载入 SSI/LLI |
| `-strict` | 关闭投机预分配 |
| `-interval N` | 每隔 N 秒取历元 |
| `-v` | 冗长 |

**本机真实 stdout（截断 FutureWarning）：**

```text
saving OBS: demo_G.nc
<xarray.Dataset> Size: 456B
Dimensions:  (time: 2, sv: 10)
Coordinates:
  * time     (time) datetime64[ns] 2010-03-05 2010-03-05T00:00:30
  * sv       (sv) <U3 'G07' 'G09' 'G12' 'G13' ... 'G21' 'G26' 'G31' 'G32'
Data variables:
    L1       (time, sv) float64 1.188e+08 1.322e+08 ... 1.143e+08 1.331e+08
    C1       (time, sv) float64 2.223e+07 2.516e+07 ... 2.175e+07 2.533e+07
Attributes:
    version:          2.11
    interval:         30.0
    rinextype:        obs
    fast_processing:  1
    time_system:      GPS
    filename:         demo.10o
    rxmodel:          ASHTECH UZ-12
    position:         [4789028.4701, 176610.0133, 4195017.031]
```

| 字段 | 含义 |
| --- | --- |
| `time` / `sv` | 历元 × 卫星 |
| `L1` / `C1` | 相位(周) / 伪距(m)；RINEX3 常为 `L1C`/`C1C`——先 `print` 再写 `-m` |
| `attrs.position` | 头 APPROX POSITION XYZ |
| `attrs.interval` | 头 INTERVAL |

读回（注意组名）：

```bash
python - <<'PY'
import xarray as xr
ds = xr.open_dataset("demo_G.nc", group="OBS")
print(dict(ds.sizes), list(ds.data_vars))
print("L1 G07 t0", float(ds["L1"].sel(sv="G07").isel(time=0)))
PY
```

本机：`sizes {'time': 2, 'sv': 10}`；`L1 G07 t0 118767195.326`。

### 3.3 API 等价

```python
import georinex as gr
obs = gr.load("demo.10o", use={"G"}, meas=["L1", "C1"])
print(obs)
```

`load` 关键参数：`use`、`meas`、`tlim=(t0,t1)`、`useindicators`、`interval`、`out=`。

## 4. 可选进阶：只保留双频相位

```bash
python -m georinex.read YOUR.rnx -u G -m L1C L2W \
  -t 2024-01-01 2024-01-01T06:00:00 -o out/G_L1L2.nc
```

观测量名必须以 `list(obs.data_vars)` 为准。

## 5. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复命令 |
| --- | --- | --- | --- |
| 1 | `No module named georinex.time` | 旧模块名 | `python -m georinex.time FILE` |
| 2 | `KeyError: 'L1'` | RINEX2/3 命名不同 | `python -c "import georinex as gr; print(list(gr.load('FILE').data_vars))"` |
| 3 | `sizes time:0` | 空窗/坏文件/过滤过狠 | `python -m georinex.time FILE`；放宽 `-u/-m/-t` |
| 4 | `OBS already in …nc` | 目标 nc 已有 OBS 组 | `rm -f out.nc` 后重跑 |
| 5 | `head` 见 `<html` | 下载成登录页 | 重做 Earthdata/CDDIS 鉴权后再 `curl` |
| 6 | `.crx` 读失败 | 无 hatanaka | `pip install hatanaka` |
| 7 | OOM / 被 kill | 1 Hz 全日进内存 | 加 `-u G -m L1C L2W -t …` 或先 `gfzrnx -smp 30` |
| 8 | `use='GPS'` 空结果 | 系统码是单字母 | `-u G` 或 `use={"G"}` |
| 9 | `gr.load("*.nc")` 炸 | 该版本不把 nc 当 RINEX | `xr.open_dataset("f.nc", group="OBS")` |
| 10 | 下游 TEC 离谱 | 把相对相位差当绝对 TEC | 换 [pytecgg](./pytecgg.md) |

## 6. 接到哪一步

- 双频 TEC → [02](../tutorials/02-gnss-dualfreq-tec.md) → [pytecgg](./pytecgg.md)
- 一日练习 → [16](../tutorials/16-practice-one-day-tec.md)
- 拼日/抽稀 → [gfzrnx](./gfzrnx.md)；QC → [anubis](./anubis.md)
- 数据来源 → [data-access](../data-access.md)