# digisondeindices：GIRO DIDBase 测高仪参数 → xarray 的 Python 客户端（2.1.0 已失效，附运行时补丁）

入口：[GitHub sunipkm/digisondeindices](https://github.com/sunipkm/digisondeindices) · [PyPI 2.1.0](https://pypi.org/project/digisondeindices/) · [GIRO DIDBase](https://giro.uml.edu/didbase/) · [Rules of the Road](https://giro.uml.edu/didbase/RulesOfTheRoad.html) · 本机验证 **2026-09-26 05:01–05:07 EDT**（Python 3.13.5）

> 岗位：按“时间 + URSI 站码”取 Digisonde 标定参数（foF2、MUF(D)、hmF2、B0、TEC、CS…），直接拿到 `xarray.Dataset`。**结论先说：PyPI 2.1.0 原样装上就用不了**：它请求的 `lgdc.uml.edu/common/DIDBGetValues` 已 404，并且漏了两个依赖。本文给出一个不改安装包的运行时补丁（`didb_fix.py`），把请求改写到 `fastchar/getbest`；补丁后的列对齐已和 curl 原始行逐值核对过。
> fastchar 接口本身（参数名、CS 阈值、站表、SAO 门槛、磁暴个例）见 [giro-ionosonde](./giro-ionosonde.md)，本文不重复。多国测高仪年度批量下载见 [ionosonde-data-downloader](./ionosonde-data-downloader.md)；Kp/Dst 见 [space-weather-indices](./space-weather-indices.md)。

## 1. 它做什么，边界

| 项 | 内容 |
|---|---|
| 版本 | PyPI **2.1.0**（2024-11-15 上传）；GitHub master **`2a37ab3`**（2026-04-24，只改了 `cli()` 里的 `p.station`→`a.station`，未发版）；MIT；★2；无 tag |
| 唯一 API | `get_indices(time, station, forcedownload=False, *, dmuf=3000, tzaware=False) -> xarray.Dataset` |
| 下载粒度 | **按整月**请求（一个时刻也拉整月，约 1–1.3 MB 文本/月/站，~1.5 s），转成 NetCDF 缓存后删文本 |
| 缓存位置 | **写死在包目录** `site-packages/digisondeindices/data/`，文件名 `{站}_{年}_{月}_{dmuf}.nc`；系统级安装没写权限就会失败，所以要装进自己的 venv |
| 返回 | 14 个变量：`CS foF2 foF1 MUFD foE hF hF2 hmE hmF hmF1 yF2 yF1 B0 TEC`，各带 `units`/`description`；`TEC` 已从 TECU 换成 m⁻²（×1e16） |
| 不做 | 电离图、SAO 描迹/剖面、站表查询、CS 过滤（要自己做） |
| 数据许可 | GIRO：CC BY-NC-SA 4.0，非商业，须致谢站点数据提供方（数据集 `attrs['Acknowledgement']` 里有原文） |

## 2. 安装（venv 放 /tmp，用完即删）

```bash
python3 -m venv /tmp/b59dig/venv
/tmp/b59dig/venv/bin/pip install digisondeindices==2.1.0 pytz dask "pandas<3"
```

三个额外包都是必须的，本机逐个撞出来：

| 缺什么 | 现象（本机原样） | 原因 |
|---|---|---|
| `pytz` | `import digisondeindices` → `ModuleNotFoundError: No module named 'pytz'` | `base.py` import 了 pytz，但 `install_requires` 没写 |
| `pandas<3` | 转换时 `ValueError: output array is read-only`（`io.py` 第 53 行 `ds['TEC'] *= 1e16`） | pandas 3.0（本机默认装到 3.0.6）的 copy-on-write 让数组只读；2.3.3 正常 |
| `dask` | `ImportError: chunk manager 'dask' is not available` | `io.load` 用 `xarray.open_mfdataset`，需要 dask |

另外，`io.py` 第 57/61 行的 f-string 在 `{}` 里换了行，这只有 **Python ≥ 3.12**（PEP 701）才能解析。本机实测 3.11.16 `compile` 报 `SyntaxError line 57 unterminated string literal`，3.12.14 通过；而 `setup.cfg` 写的是 `python_requires >= 3.7`。

本机最终环境：digisondeindices 2.1.0、numpy 2.5.3、pandas 2.3.3、xarray 2026.7.0、netCDF4 1.7.4、dask 2026.8.0。PyPI 包与 master 只差上面那一行 CLI（`diff -r` 实测）。包里的 `cli()` 没有注册 console script，所以没有命令行入口。

## 3. 真实命令与输出

### 3.1 原样调用：必失败

```python
import datetime as dt, digisondeindices as didbase
print('version', didbase.__version__)
try:
    ds = didbase.get_indices(dt.datetime(2022, 1, 25, 5, 0, 0), 'MHJ45')
except Exception as e:
    print(type(e).__name__, ':', e)
```

```text
version 2.1.0
ConnectionError : https://lgdc.uml.edu/common/DIDBGetValues?ursiCode=MHJ45&charName=hmE,foE,hmF1,foF1,hmF2,foF2,hF,hF2,yF1,yF2,B0,TEC,MUFD&DMUF=3000&fromDate=2022.01.01+00:00:00&toDate=2022.02.01+00:00:00
```

直接 curl 这个 URL 得到 `404 776 B`，内容是 Tomcat 的 “The requested resource [/common/DIDBGetValues] is not available”。

### 3.2 为什么不能只换主机路径

把同样的参数原封不动发给 `fastchar/getbest`（`curl`，MHJ45 2022-01-25 00–01 UT）：

```text
200 3215
# STATUS: WARNING (Unknown characteristic name: hF)
# STATUS: WARNING (Unknown characteristic name: hF2)
# STATUS: WARNING (Unknown characteristic name: MUFD)
2022-01-25T00:00:00.000Z  80  110.0 //   --- __    --- __   --- __  298.1 //  3.525 //    --- __   74.3 //  61.5 //    2.5 //
```

有两个坑：

1. getbest 不认 `hF`、`hF2`、`MUFD` 这三个名字，要写成 `` h`F ``、`` h`F2 ``、`MUF(D)`，反引号在 URL 里编码成 `%60`。
2. getbest 的输出列序**跟请求顺序走**。而 `io.convert_csv` 按写死的列序解析：`CS foF2 foF1 MUFD foE hF hF2 hmE hmF hmF1 yF2 yF1 B0 TEC`。请求顺序不对，变量名就会**静默错位**，不报任何错。

所以补丁必须按解析器的列序重排 `charName`。日期格式 `2022.01.01+00:00:00` getbest 照收。

### 3.3 运行时补丁 `didb_fix.py`（原样）

```python
# didb_fix.py —— 给 digisondeindices 2.1.0 打运行时补丁（不改安装包）
import time
from pathlib import Path
import digisondeindices as didbase
from digisondeindices import web

NEW = 'https://lgdc.uml.edu/fastchar/getbest'
# 必须与 io.convert_csv 写死的列序一致；h`F 的反引号编码成 %60
ORDER = 'foF2,foF1,MUF(D),foE,h%60F,h%60F2,hmE,hmF2,hmF1,yF2,yF1,B0,TEC'
CACHE = Path(didbase.__file__).parent / 'data'     # 包目录里的缓存（写死，改不了）
_orig = web.download

def _download(url, fn):
    kv = dict(p.split('=', 1) for p in url.split('?', 1)[1].split('&'))
    kv['charName'] = ORDER
    url = NEW + '?' + '&'.join(f'{k}={v}' for k, v in kv.items())
    t = time.time(); _orig(url, fn)
    print(f'  GET {kv["ursiCode"]} {kv["fromDate"][:10]}..{kv["toDate"][:10]} -> {fn.name} {fn.stat().st_size} B {time.time()-t:.1f} s')

web.download = _download

def purge(station, year, month, dmuf=3000):
    """删掉某站某月缓存（当月刷新 / forcedownload 前必须先删，见坑 5）"""
    for ext in ('.nc', '.txt'):
        (CACHE / f'{station}_{year:04d}_{month:02d}_{dmuf}{ext}').unlink(missing_ok=True)
```

`web.downloadfile` 是通过模块全局名调用 `download` 的，所以替换 `web.download` 就能生效。

### 3.4 端到端 `demo.py`（原样，缓存清空后首跑）

```python
import datetime as dt, numpy as np, xarray as xr
import didb_fix
import digisondeindices as didbase
from digisondeindices import web
from digisondeindices.base import todatetime

# [1] 单时刻：返回的是长度 1 的 time 维，不是标量
ds = didbase.get_indices(dt.datetime(2022, 1, 25, 5, 0, 0), 'MHJ45').load()
print('[1]', ds.attrs['Location'], '|', ds.attrs['Instrument'])
for v in ('CS', 'foF2', 'MUFD', 'hF', 'hmF', 'B0', 'TEC'):
    print(f'    {v:4s} {ds[v].values[0]!s:>8} {ds[v].attrs["units"]:5s} {ds[v].attrs["description"]}')
# [2] 非整点：method="nearest"，没有容差
ds = didbase.get_indices('2022-01-25T05:02:31', 'MHJ45').load()
print('[2] ask 05:02:31 -> got', str(ds.time.values[0])[:19], 'foF2', ds.foF2.values[0])
# [3] 跨月：库内 sel 会因月界重复时刻报错；绕过：自己拿文件、去重
times = todatetime(['2022-01-31T23:55', '2022-02-01T00:05'], False)
try:
    didbase.get_indices(list(times), 'MHJ45')
except Exception as e:
    print('[3] get_indices 跨月 ->', type(e).__name__, e)
fl = web.downloadfile(times, 'MHJ45', False, 3000)
raw = xr.open_mfdataset(fl, combine='by_coords')
ds = raw.drop_duplicates('time').sel(time=times, method='nearest', tolerance=np.timedelta64(10, 'm')).load()
print('[3] 去重后', [str(t)[11:16] for t in ds.time.values], 'foF2', ds.foF2.values, '| 合并行数', raw.sizes['time'])
# [4] 整月统计（缓存里的 nc 可直接当数据集用）
jan = xr.open_dataset(fl[0]).load()
cs = jan.CS.values
print('[4] 2022-01 行数', jan.sizes['time'], '| 首/末', str(jan.time.values[0])[:16], str(jan.time.values[-1])[:16],
      '| CS>=50且!=55', int(((cs >= 50) & (cs != 55)).sum()), '| CS=0', int((cs == 0).sum()), '| foF2 中位', float(jan.foF2.median()))
# [5] 无数据站：不报错，返回空集
e = didbase.get_indices(dt.datetime(2024, 5, 11, 12), 'BC840')
print('[5] BC840 2024-05 ->', dict(e.sizes))
print('[cache]', sorted(p.name for p in didb_fix.CACHE.iterdir()))
```

```text
  GET MHJ45 2022.01.01..2022.02.01 -> MHJ45_2022_01_3000.txt 1331079 B 1.5 s
[1] GEO ( 42.6 N   288.5 E ), URSI-Code MHJ45, MILLSTONE HILL | Ionosonde, Model: [DPS-4D]
    CS         90 %     Autoscaling confidence score (from 0 to 100, 999 if manual scaling, -1 if unknown)
    foF2      2.0 MHz   F2 layer critical frequency
    MUFD    6.116 MHz   Maximum usable frequency for ground distance 3000 km
    hF      325.0 km    Minimum virtual height of F trace
    hmF     308.9 km    Peak height F2-layer
    B0       56.2 km    IRI thickness parameter
    TEC  6000000000000000.0 m^-2  Total electron content
[2] ask 05:02:31 -> got 2022-01-25T05:05:00 foF2 2.075
  GET MHJ45 2022.02.01..2022.03.01 -> MHJ45_2022_02_3000.txt 1233285 B 1.4 s
[3] get_indices 跨月 -> InvalidIndexError Reindexing only valid with uniquely valued Index objects
[3] 去重后 ['23:55', '00:05'] foF2 [4.225 4.225] | 合并行数 16631
[4] 2022-01 行数 8633 | 首/末 2022-01-01T00:00 2022-02-01T00:00 | CS>=50且!=55 7726 | CS=0 227 | foF2 中位 3.95
  GET BC840 2024.05.01..2024.06.01 -> BC840_2024_05_3000.txt 535 B 0.7 s
[5] BC840 2024-05 -> {'time': 0}
[cache] ['BC840_2024_05_3000.nc', 'MHJ45_2022_01_3000.nc', 'MHJ45_2022_02_3000.nc']
```

**核对列对齐**：用 curl 直接取 getbest（`charName=foF2,MUF(D),h%60F,hmF2,B0,TEC`，2022-01-25 05:00–05:06），原始行是：

```text
2022-01-25T05:00:00.000Z  90  2.000 //  6.116 // 325.0 //  308.9 //  56.2 //    0.6 //
2022-01-25T05:05:00.000Z  90  2.075 //  6.123 // 287.5 //  324.3 //  58.4 //    0.9 //
```

和 [1]、[2] 逐值一致：TEC 0.6 TECU = 6e15 m⁻²；变量 `hmF` 就是 hmF2。跨月那两个 foF2 都是 4.225，也用原始行核过（23:50 4.200、23:55 4.225、00:00 4.225、00:05 4.225、00:10 4.200），不是去重出错。

### 3.5 当月数据 / 本地时区（`demo_now.py`，原样）

```python
import datetime as dt
import didb_fix, digisondeindices as didbase
now = lambda: dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
for i in (1, 2, 3):
    if i == 3: didb_fix.purge('PQ052', 2026, 9); print('  purge PQ052 2026-09')
    t = now()
    try:
        d = didbase.get_indices(t, 'PQ052').load()
        print(f'[now.{i}] ask {t:%H:%M:%S}Z -> {str(d.time.values[0])[11:16]}Z foF2 {d.foF2.values[0]} CS {d.CS.values[0]}')
    except Exception as e:
        print(f'[now.{i}] ask {t:%H:%M:%S}Z ->', type(e).__name__, e)
```

```text
== TZ=UTC
  GET PQ052 2026.09.01..2026.10.01 -> PQ052_2026_09_3000.txt 1124696 B 1.5 s
[now.1] ask 09:06:36Z -> 09:00Z foF2 6.975 CS 95
  GET PQ052 2026.09.01..2026.10.01 -> PQ052_2026_09_3000.txt 1124696 B 1.4 s
[now.2] ask 09:06:38Z -> AttributeError 'NoneType' object has no attribute 'stem'
  purge PQ052 2026-09
  GET PQ052 2026.09.01..2026.10.01 -> PQ052_2026_09_3000.txt 1124696 B 1.4 s
[now.3] ask 09:06:39Z -> 09:00Z foF2 6.975 CS 95
== TZ=America/New_York
[now.1] ask 09:06:41Z -> RuntimeError DIDBase package does not allow prediction retrieval.
[now.2] ask 09:06:41Z -> RuntimeError DIDBase package does not allow prediction retrieval.
  purge PQ052 2026-09
[now.3] ask 09:06:41Z -> RuntimeError DIDBase package does not allow prediction retrieval.
```

09:06 UTC = 05:06 EDT。PQ052（Pruhonice）当天最新一条是 09:00Z。`forcedownload=True` 走的是同一条崩溃路径：本机对 MHJ45 2022-01 实测同样是 `AttributeError 'NoneType' object has no attribute 'stem'`，并留下一个孤儿 `.txt`。

## 4. 字段

| 变量 | 单位 | getbest 名 | 说明 |
|---|---|---|---|
| `CS` | % | （自动附带） | ARTIST 置信度 0–100；999 = 人工；-1 = 未知。整条记录一个值。阈值怎么选见 [giro-ionosonde 4.4](./giro-ionosonde.md) |
| `foF2` `foF1` `foE` | MHz | 同名 | 临界频率 |
| `MUFD` | MHz | `MUF(D)` | 距离 D = `dmuf` km（默认 3000）时的 MUF |
| `hF` `hF2` | km | `` h`F `` `` h`F2 `` | 最小虚高 |
| `hmE` `hmF` `hmF1` | km | `hmE` `hmF2` `hmF1` | 峰高。**`hmF` 就是 hmF2**，库里的列名写错了，README 却写成 hmF2 |
| `yF2` `yF1` | km | 同名 | 抛物层半厚度 |
| `B0` | km | 同名 | IRI 厚度参数 |
| `TEC` | m⁻² | `TEC`（TECU） | 测高仪推算的 TEC，库内已 ×1e16 |
| attrs | — | 头部 | `Station` `DMUF` `Location`（东经 0–360）`Instrument` `Source` `Acknowledgement` |

四类情况各长什么样：
- 缺值：每个参数后面的 URSI 限定/描述字母（`//`、`__`）被丢弃，`---` 变成 NaN。
- 没判出的电离图：不出行，在数据里看不到。
- 整站整月无数据：getbest 返回 `# STATUS: ERROR (No measurement data…)`，库给出 0 行数据集，但**不会告诉你原因**。
- 未来时刻：抛 `RuntimeError`。

## 5. 坑（现象 → 原因 → 修复）

1. **`ConnectionError: …/common/DIDBGetValues…`** → 旧接口已下线（404）→ 用 3.3 的 `didb_fix`；也可以等上游修（截至 `2a37ab3` 仍是旧 URL）。
2. **补丁后值对不上、字段张冠李戴** → getbest 按请求顺序出列，而解析器用固定列序 → `charName` 必须严格等于 `ORDER`。改 `ORDER` 就会错位，而且不会报错。
3. **`ModuleNotFoundError: pytz` / `output array is read-only` / `chunk manager 'dask'`** → 漏依赖或 pandas 3 → `pip install pytz dask "pandas<3"`。
4. **Python 3.11 及以下 `SyntaxError`（io.py:57）** → PEP 701 写法 → 用 Python ≥ 3.12。
5. **当月第二次查询、或 `forcedownload=True`：`AttributeError: 'NoneType' object has no attribute 'stem'`，之后每次都这样** → 缓存 `.nc` 过期后，库重新下 `.txt`，但 `convert_csv` 看到 `.nc` 已存在就直接 `return None`；`None` 进了文件列表，而且 `.txt` 残留，以后 `http_download` 见到它就直接跳过 → 查当月数据或强制刷新前先 `didb_fix.purge(站, 年, 月)`（同时删 `.nc` 和 `.txt`）。
6. **本地时区在 UTC 以西时，最近几小时报 `does not allow prediction retrieval`**（EDT 下最近 4 h 都算“未来”）→ `web.downloadfile` 用本地时间的 `datetime.today()` 去和 UTC 时刻比 → 用 `TZ=UTC python …` 运行；或者只查 4 h 以前的数据。`tzaware=True` 只管把输入换算成 UTC，救不了这个比较。
7. **跨月的时间数组：`InvalidIndexError: Reindexing only valid with uniquely valued Index objects`** → 每月请求的 toDate 取下月 1 日 00:00 且包含端点，于是月界那一刻在两个文件里各出现一次 → 按 3.4 [3] 的做法：`web.downloadfile` + `open_mfdataset` + `drop_duplicates('time')`。
8. **返回的时刻和问的不一样** → `sel(method='nearest')` 没有容差：MHJ45 2022-01-11 有 115 min 缺口，问 00:57 照样返回 01:55 那一条 → 一定要检查返回的 `time`，或者像 [3] 那样自己加 `tolerance`。
9. **单个时刻也拉 1 MB+、整月文本** → 按月缓存是设计如此 → 批量时按站按月串行即可，第二次命中缓存不再请求。LGDC 是单台 Tomcat，别并发（[pyirtam](./pyirtam.md) 遇过 429）。
10. **空数据集被缓存成“永久无数据”** → 过去月份的 `.nc`（空集约 14 KB，大于 1000 B 的有效性阈值）只在“请求时刻晚于文件 mtime”时才刷新，而过去月份永远不满足 → 怀疑数据后来补上了，就 `purge` 掉再拉。
11. **`PermissionError` / 缓存找不到** → 缓存写死在包目录 → 装进用户自己的 venv。清理就删 `…/site-packages/digisondeindices/data/`。
12. **`datetime.utcfromtimestamp` DeprecationWarning（3.12+）** → 上游旧写法，不影响结果。

## 6. 选型

| 需求 | 选 |
|---|---|
| 在 Python 里按时刻拿 xarray，打补丁可以接受 | 本库 + `didb_fix` |
| 不想依赖一个 ★2、已失效的包 | 直接 `curl`/`requests` 调 fastchar，解析见 [giro-ionosonde](./giro-ionosonde.md) 3.4（标准库就够） |
| 澳洲 SWS / 日本 NICT 测高仪 | [ionosonde-data-downloader](./ionosonde-data-downloader.md) |
| 全球 foF2/hmF2 同化图 | [pyirtam](./pyirtam.md) |

## 7. 本机记录

- 2026-09-26 05:01–05:07 EDT。venv 放在 `/tmp/b59dig`，下载缓存在 venv 的包目录里；两者连同临时脚本已全部删除。
- 请求总数约 15 次（每次 ≤ 1.3 MB，~1.5 s）；外加若干次 curl 探测，每次窗口 ≤ 1 个月。
- 上游问题（未提 issue）：DIDBGetValues 404、列序依赖、漏 pytz/dask、pandas 3 只读、`python_requires` 与 PEP 701 不符、缓存 `None` 崩溃、本地时区比较、月界重复、`hmF` 命名、PyPI 2.1.0 CLI 的 `p.station`（master 已修，未发版）。
