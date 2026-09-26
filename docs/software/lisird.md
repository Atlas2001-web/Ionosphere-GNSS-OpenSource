# LISIRD（LASP 太阳辐照数据中心）· F10.7 / Lyman-α / FISM2 EUV / GOES XRS 直连下载 操作手册

入口：门户 <https://lasp.colorado.edu/lisird/> · LaTiS 接口 `https://lasp.colorado.edu/lisird/latis/dap/` · HAPI `https://lasp.colorado.edu/lisird/hapi/` · 本机验证 **2026-09-26 05:10–05:30 EDT**，只用 curl 和系统 Python 3.13 标准库（`csv` / `urllib` / `statistics`），不装第三方库。样例时段是 **2024-05-08 → 05-12**（Gannon 超级磁暴，05-10 06:54 UT 有 X3.9 耀斑）。

> 岗位：给电离层工作拿**太阳侧输入**：F10.7（IRI / NeQuick / 经验 TEC 模式要用）、Lyman-α（D/E 区）、FISM2 EUV 光谱（热层 / 电离层物理模式）、GOES XRS 1 min（耀斑引起的 TEC 突增 SFE）。  
> 本文**不讲** Kp/Dst/太阳风（见 [space-weather-indices](./space-weather-indices.md)），也不讲地磁台数据（见 [geomag-api](./geomag-api.md)）。  
> 以本机实测和 `.das` / `.dds` 元数据为准；LASP 改接口后本文可能过时。

## 1. 它解决什么，边界在哪

| 接口 | 基址 | 数据集数 | 输出 | 适合 |
| --- | --- | --- | --- | --- |
| **LaTiS**（主力） | `/lisird/latis/dap/<id>.<suffix>?<选择>` | **281**（`catalog.json`） | `csv` `json` `jsond` `txt` `das` `dds` | 选列、按时间 / 数值过滤、改时间格式、`last()` 取最新 |
| **HAPI 2.0** | `/lisird/hapi/{catalog,info,data}` | **29** | 只有 CSV | 已有 HAPI 客户端（pyspedas / hapiclient）时顺手用；**没有 F10.7、GOES、FISM** |

- **账号**：两个接口都**不用账号、不用 key**。没观察到限速；单次请求有样本上限（见 §7 坑 3）。
- **电离层常用数据集**（都在 LaTiS 里）：

| id | 内容 | 时间列格式 | 实测最新（05:20 EDT 拉取） |
| --- | --- | --- | --- |
| `penticton_radio_flux` | DRAO F10.7，每日三测（observed / adjusted） | Julian Date | 2026-09-25 22:43 UT |
| `penticton_radio_flux_nearest_noon` | 每日一条，取当地正午那一次 | Julian Date | 同上当天 19:43 条 |
| `noaa_radio_flux` | NOAA 转发 F10.7 | 日期 | **2018-04-30 起停更**，别用 |
| `composite_lyman_alpha` | 复合 Lyman-α（W/m²），`type` = 数据来源 | `days since 1947-01-01T12:00`（日中心） | 2026-09-24 |
| `fism_daily_bands` / `fism_daily_hr` | FISM2 日均：23 个波段（photons/cm²/s）/ 0.1 nm 光谱（W/m²/nm） | `yyyyDDD` | 2026267（= 09-24） |
| `noaa_goes18_xrs_1m` / `noaa_goes19_xrs_1m` | GOES XRS 1 min（shortwave 0.05–0.4 nm / longwave 0.1–0.8 nm，W/m²） | `seconds since 2000-01-01 12:00:00` | 2026-09-24 23:59 |
| `noaa_goes1[6-9]_euvs_1d` | GOES EUVS 日均谱线（含 1216 Å Lyman-α） | — | — |

## 2. 安装

不用装。查询串里有 `>`、`<`、`'`、`()`，shell 里必须把整个 URL 放进双引号；本文命令带 `-g`（关掉 curl 的 `[]{}` 通配）只是保险，实测不加 `-g` 结果相同。在 Python 里拼 URL 时要把 `>` / `<` 编码成 `%3E` / `%3C`。

## 3. 真实命令与输出

```bash
B=https://lasp.colorado.edu/lisird/latis/dap
```

### 3.1 看有哪些数据集、字段和单位

```bash
curl -s $B/catalog.json | python3 -c "import json,sys;print(len(json.load(sys.stdin)['datasets']['datasets']))"
# 281
curl -s $B/penticton_radio_flux.dds
# Dataset { Sequence { Float64 time; Structure { Float64 observed_flux; Float64 adjusted_flux; } unknown; } samples; } penticton_radio_flux;
curl -s $B/penticton_radio_flux.das      # 单位与缺测值
#   time: units "Julian Date"
#   observed_flux / adjusted_flux: missing_value "0.0"; units "solar flux unit (SFU)"
```

`.info` 后缀**不存在**（500 `Unsupported Writer suffix: info`）。元数据看 `.das`，结构看 `.dds`。

### 3.2 F10.7：一日三测 / 近正午

```bash
curl -sg "$B/penticton_radio_flux_nearest_noon.csv?time>=2024-05-08&time<2024-05-12&format_time(yyyy-MM-dd'T'HH:mm)"
```
```
time (yyyy-MM-dd'T'HH:mm),observed_flux (solar flux unit (SFU)),adjusted_flux (solar flux unit (SFU))
2024-05-08T19:43,227.1,231.4
2024-05-09T19:43,233.2,237.7
2024-05-10T19:43,223.4,227.9
2024-05-11T19:43,213.7,218.0
```
200，218 B，约 4 s。和 GFZ `https://kp.gfz.de/app/json/?start=2024-05-08T00:00:00Z&end=2024-05-11T23:59:59Z&index=Fobs` 返回的 `[227.1,233.2,223.4,213.7]` **逐值一致**。2026-09-25 同样一致：LISIRD 近正午 105.4 = GFZ Fobs 105.4（SWPC JSON 只给整数 105）。

选列 + 按数值过滤：
```bash
curl -sg "$B/penticton_radio_flux.csv?time,adjusted_flux&time>=2024-05-10&time<2024-05-11&format_time(yyyy-MM-dd'T'HH:mm:ss)"
# time (yyyy-MM-dd'T'HH:mm:ss),adjusted_flux (solar flux unit (SFU))
# 2024-05-10T16:43:40,218.8
# 2024-05-10T19:43:40,227.9
# 2024-05-10T22:43:40,235.4
curl -sg "$B/penticton_radio_flux.csv?time>=2024-05-10&time<2024-05-11&adjusted_flux>230"
# time (Julian Date),observed_flux ...,adjusted_flux ...
# 2460441.447,230.8,235.4
curl -sg "$B/penticton_radio_flux.csv?last()&format_time(yyyy-MM-dd'T'HH:mm)"
# 2026-09-25T22:43,103.9,104.4          ← 当天观测次日凌晨（EDT）已上架
```
全量 `penticton_radio_flux.csv`（不带条件）：200，**1,150,736 B**，4 s。整段历史一次拉下来也没问题。

### 3.3 同一段数据的四种输出

```bash
curl -sg "$B/penticton_radio_flux.json?time>=2024-05-10&time<2024-05-11"
# {"penticton_radio_flux": {"samples": [{"time": 2460441.197, "observed_flux": 214.5, "adjusted_flux": 218.8}, ...]}}
curl -sg "$B/penticton_radio_flux.jsond?time>=2024-05-10&time<2024-05-11"
# "metadata": {"time": {"units": "milliseconds since 1970-01-01"}, ...}, "parameters": ["time","observed_flux","adjusted_flux"],
# "data": [[1715359420800,214.5,218.8], [1715370220800,223.4,227.9], [1715381020800,230.8,235.4]]
curl -sg "$B/penticton_radio_flux.txt?time>=2024-05-10&time<2024-05-11"
# 2460441.197, 214.5, 218.8               ← 无表头
```
`json` 保留原始时间单位（这里是 Julian Date）；`jsond` 换成 Unix 毫秒，并附带单位 / 缺测值元数据，写程序时用 `jsond` 最省事。

### 3.4 Lyman-α、FISM2 EUV、GOES XRS

```bash
curl -sg "$B/composite_lyman_alpha.csv?time>=2024-05-08&time<2024-05-12&format_time(yyyy-MM-dd)"
# time (yyyy-MM-dd),irradiance (W/m^2),uncertainty (W/m^2),type
# 2024-05-10,0.00926592480391264,9.265925036743283E-4,7
curl -sg "$B/fism_daily_bands.csv?time,E0_05_0_4,E105_0_121_0&time>=2024-05-09&time<2024-05-12"
# time (yyyyDDD),E0_05_0_4 (photons/cm^2/s),E105_0_121_0 (photons/cm^2/s)
# 2024130,20628.277373819925,3.690860428146341E10       ← 2024130 = 05-09（闰年）
# 2024131,18865.49585601732,3.696312923840948E10
# 2024132,16900.972484725058,3.80190217155359E10
curl -sg "$B/fism_daily_hr.csv?time>=2024-05-10&time<2024-05-11&wavelength>=121&wavelength<122"
# time (yyyyDDD),wavelength (nm),irradiance (W/m^2/nm),uncertainty (unitless)
# 2024131,121.55,0.05847474932670593,0.03326164186000824   ← 10 行，Lyman-α 峰在 121.55 nm 这一格；15.6 s
curl -sg "$B/noaa_goes18_xrs_1m.csv?time,longwave,longwave_flag&time>=2024-05-10T06:50&time<2024-05-10T06:58&format_time(yyyy-MM-dd'T'HH:mm)"
# 2024-05-10T06:54,0.00038827845,0         ← 峰值 3.88e-4 W/m² = X3.9，flag 0 = 正常
```

### 3.5 HAPI（29 个数据集，2.0 语法）

```bash
H=https://lasp.colorado.edu/lisird/hapi
curl -s $H/capabilities                  # {"HAPI":"2.0",...,"outputFormats":["csv"]}
curl -s "$H/info?id=composite_lyman_alpha"
# parameters: time(isotime) / irradiance(W/m^2, fill -9999.0) / uncertainty / type; startDate 1947-02-14, stopDate 2026-09-24
curl -s "$H/data?id=composite_lyman_alpha&time.min=2024-05-08T00:00:00Z&time.max=2024-05-12T00:00:00Z"
# 2024-05-10T12:00:00.000Z,0.00926592480391264,9.265925036743283E-4,7    ← 与 LaTiS 同值；HAPI 把日值标在当天 12:00（`.das`：`days since 1947-01-01T12:00`，本来就是日中心）
```
HAPI 3 的写法 `dataset=…&start=…&stop=…` 返回 400 `code 1400`；加 `format=json` 返回 400 `code 1409 unsupported output format`。

### 3.6 端到端：F10.7 当日值 + 81 天居中均值（`f107.py`）

```python
import csv, io, urllib.request, statistics
B = "https://lasp.colorado.edu/lisird/latis/dap/"
q = "penticton_radio_flux_nearest_noon.csv?time,observed_flux,adjusted_flux&time>=2024-03-21&time<2024-06-30&format_time(yyyy-MM-dd)"
with urllib.request.urlopen(B + q.replace(">", "%3E").replace("<", "%3C"), timeout=60) as r:
    rows = list(csv.reader(io.StringIO(r.read().decode())))
hdr, data = rows[0], rows[1:]
obs = {d: float(o) for d, o, a in data if float(o) > 0}      # 0.0 = 缺测
print(hdr); print(len(data), "rows", data[0][0], "->", data[-1][0])
c = "2024-05-10"; days = sorted(obs); i = days.index(c); win = days[i-40:i+41]
print(c, "F10.7obs", obs[c], "81d-mean", round(statistics.mean(obs[d] for d in win), 1), "n", len(win))
```
```
['time (yyyy-MM-dd)', 'observed_flux (solar flux unit (SFU))', 'adjusted_flux (solar flux unit (SFU))']
101 rows 2024-03-21 -> 2024-06-29
2024-05-10 F10.7obs 223.4 81d-mean 176.2 n 81
```
（`timeout 120 python3 f107.py`，4.7 s。）IRI 的 F10.7A 用 81 天均值，NRLMSIS 同时要当日值和 81 天均值；按模型文档确认要 observed 还是 adjusted。

## 4. 查询语法速查（LaTiS）

| 写法 | 作用 | 备注 |
| --- | --- | --- |
| `?time,adjusted_flux` | 只要这些列 | 逗号分隔，放在最前 |
| `time>=2024-05-10&time<2024-05-11` | 时间范围 | ISO 日期或 `2024-05-10T06:50`；按 UTC 理解；`<` 不含端点 |
| `adjusted_flux>230`、`wavelength>=121` | 按数值过滤 | 浮点**不要用 `=`**（`wavelength=121.5` 返回空表） |
| `format_time(yyyy-MM-dd'T'HH:mm)` | 改时间列格式 | Java SimpleDateFormat 语法，字面 T 要加单引号 |
| `last()` | 只要最后一条 | 查上架时间、做监测 |
| 后缀 `.csv/.json/.jsond/.txt` | 输出格式 | `.das/.dds` 取元数据；`.info` 不存在 |

## 5. 输入与输出

- 输入：数据集 id + 选择条件，全在 URL 里。
- 输出：CSV 第一行是 `名字 (单位)` 表头；`txt` 不带表头。缺测：F10.7 是 `0.0`（`.das` 的 `missing_value`），HAPI 是 `-9999.0`（`info` 的 `fill`）。
- 时间：各数据集自带单位（Julian Date / `days since 1947-01-01T12:00` / `yyyyDDD` / `seconds since 2000-01-01 12:00:00`，以 `.das` 为准）。想统一，就加 `format_time(...)`；或者用 `jsond`（F10.7 实测换成 Unix 毫秒）。

## 6. 在工作流里接哪一步

- **路径 A · 一日 TEC**（[README](./README.md#a--一日-tec)）：用 F10.7（`penticton_radio_flux_nearest_noon`）和它的 81 天均值驱动 IRI（[iri2016](./iri2016.md) / [pyiri](./pyiri.md)）或 NeQuick，作为 GIM/TEC 的背景参考；Kp 另取（[space-weather-indices](./space-weather-indices.md)）。
- **耀斑 SFE / 日侧 TEC 突增**：GOES XRS 1 min 的 longwave 峰值时刻，对齐 1 Hz / 30 s 的 sTEC 变化率（[varion](./varion.md)、[gnss-tec](./gnss-tec.md)）。
- **物理模式驱动**：FISM2 光谱 / 波段 → SAMI2（[sami2py](./sami2py.md)）或热层模式的 EUV 输入。

## 7. 坑（现象 → 原因 → 修复）

1. **F10.7 时间是 xx:43，不是整点** → LISIRD 直接用 DRAO fluxtable 的 `fluxjulian` 列（3 位小数，与 `fluxtime` 整点 17/20/23 UT 并不严格对应），2024-05-10 三次观测分别换算成 16:43/19:43/22:43 UT → 按**日期**对齐就行，不要拿它做小时级对齐。
2. **`noaa_radio_flux` 查 2024 年返回空表（200，1 B）** → 该数据集 **2018-04-30 起停更** → 用 `penticton_radio_flux*`。
3. **`fism_daily_hr.dds` 返回 400 `Limit exceeded: requested 55248200 samples, allowed 25000000`** → 服务器单次上限 2500 万样本，连 `.dds` 都会展开整个数据集 → 大数据集一定要带时间 + 波长范围；结构改看 `catalog`（`/lisird/latis/catalog`）或 `fism_daily_bands.dds`。
4. **`wavelength=121.5` 返回空表** → FISM 格点在 x.x5 nm，浮点相等匹配不上 → 用 `>=`/`<` 区间。
5. **FISM 的 `2024131` 看成 5 月 11 日** → 时间是 `yyyyDDD`，2024 是闰年，131 = 05-10 → 用 `format_time(yyyy-MM-dd)` 或自己换算。
6. **命令行结果为空或报语法错** → URL 没加引号，shell 把 `<` / `>` 当重定向、把 `'` / `()` 当语法 → 整个 URL 加双引号（`-g` 可加可不加）；Python 中把 `<` / `>` 编码。
7. **HAPI 400 `code 1400` / `1409`** → 服务器是 HAPI **2.0**：参数必须写 `id` / `time.min` / `time.max`；只支持 CSV → 按 2.0 语法写，JSON 需求改走 LaTiS `jsond`。
8. **在 HAPI catalog 里找不到 F10.7 / GOES / FISM** → HAPI 只开放了 29 个数据集 → 这些数据走 LaTiS。
9. **F10.7 均值被拉低** → 缺测值是 `0.0` 而不是空值 → 先过滤 `> 0` 再求均值（`f107.py` 已处理）。
10. **`penticton_radio_flux.info` 500** → LaTiS 没有 `info` 这个 writer → 用 `.das` / `.dds`。

## 8. 选型对比

| 需求 | 用 | 理由 |
| --- | --- | --- |
| F10.7 日值（和 GFZ 一致、带 1 位小数） | **LISIRD** `penticton_radio_flux_nearest_noon` 或 GFZ `Fobs` | 两者逐值一致；LISIRD 还给 adjusted 和一日三测 |
| 实时 F10.7（分钟级监控） | SWPC JSON（[space-weather-indices](./space-weather-indices.md)） | SWPC 只给整数，但实时；LISIRD 次日上架 |
| EUV 光谱 / 波段、Lyman-α | **LISIRD** FISM2 / composite_lyman_alpha | 其它门户基本没有 |
| GOES XRS 1 min 历史 | **LISIRD** `noaa_goes1x_xrs_1m` | 一条 URL 按分钟切片，不用下 NetCDF 日文件 |
| 已经在用 pyspedas / HAPI 生态 | LISIRD HAPI（29 集）或 CDAWeb HAPI | 注意 LISIRD 这边是 HAPI 2.0，只有 CSV |
