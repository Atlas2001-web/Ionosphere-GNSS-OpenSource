# geomagindices：按时刻取 Ap / F10.7 / Kp 的 Python 小库（1.5.1 日值源已失效，实测只剩月均）

入口：[GitHub space-physics/geomagindices](https://github.com/space-physics/geomagindices) · [PyPI 1.5.1](https://pypi.org/project/geomagindices/) · 替代源 [GFZ Kp API](https://kp.gfz.de/en/data) · 本机验证 **2026-09-26 05:09–05:13 EDT**（CPython 3.13.5 venv）

> **质检复跑通过（2026-09-26 05:51–05:56 EDT，提交 `59d7961`）**：CPython 3.13.15 venv，pandas 3.0.6 / numpy 2.5.3 / requests 2.34.2。§3.1–3.4、§3.6 输出逐字一致：2015-03-17 返回 2015-04-01 Ap 11 / F10.7 129.05；2024-05 返回 24 / 188.37；smooth 168.42 / 15.0；45 天旧 URL 仍 404（196 B），新 URL 返回 10/95、15/110；2030 那行 73.5/12.2 两列互换；GFZ Ap 271 / Fobs 213.7。NGDC 那步 curl 报 `(9) Server denied you to change to the given directory`。§3.5 的 seed→结果映射换路径后变了，已改为实测结果并注明原因。
>
> 岗位：给模型（[msise00](./msise00.md)、IRI/HWM 类）按时刻自动喂 **Ap、F10.7（可平滑）、Kp**。**结论先说：1.5.1 原样装上能跑、不报错，但给的是错的数。** 3 h Kp/Ap 日值读的是 NGDC FTP 目录，现已下线（550）；库会**静默退回月均**，按“最近的月初”取值，Kp 列直接消失。2024-05-11（Gannon 磁暴，GFZ 定值 Ap **271**）它返回 **Ap 24 / F10.7 188.37**，都是 2024-05 的月均。
> 指数直连下载和数据状态（def/pre）见 [space-weather-indices](./space-weather-indices.md)；PySPEDAS 一行载 OMNI/Kp 见 [pyspedas](./pyspedas.md)。本文只讲这个库本身和怎么绕开。

## 1. 它做什么，边界

| 项 | 内容 |
|---|---|
| 版本 | PyPI **1.5.1**（2024-12-19 22:09 UTC 上传）；GitHub main **`1c76774`**（2024-12-26，只删 badge）；MIT；★17；Zenodo DOI |
| 依赖 | `python-dateutil pandas requests numpy`，`requires_python >=3.9`；本机装到 pandas 3.0.6 / numpy 2.5.3 / requests 2.34.2，**无漏依赖** |
| 唯一 API | `get_indices(time, smoothdays=None, forcedownload=False) -> pandas.DataFrame` |
| CLI | `python -m geomagindices DATE [-s SMOOTHDAYS]`（没有 console script） |
| 数据源（按时刻分支） | 过去 → NGDC FTP 年文件（**已死**）→ 失败退回 SWPC 月均 F10.7 JSON + GFZ FTP `ap_monyr.ave` 月均 Ap；今天起 45 天内 → SWPC 45 天预报（**URL 已 404**）；再往后 → 包内自带 NASA MSFC **2016-05** 20 年预报表（到 2030-10） |
| 缓存 | **写死在包目录** `site-packages/geomagindices/data/`；系统级安装没写权限会失败 |
| 不做 | Dst/AE/SYM-H、Hp30、太阳风；定值/暂定状态；时区处理 |

## 2. 安装（venv 放 /tmp，用完即删）

```bash
python3 -m venv /tmp/b60/v
/tmp/b60/v/bin/pip install --no-cache-dir geomagindices==1.5.1
```

## 3. 真实命令与输出

### 3.1 过去时刻：静默退回月均（错值）

```bash
python -m geomagindices 2015-03-17T12:00
```
```
geomagindies: downloading ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP/2015 => …/geomagindices/data/2015
geomagindies: downloading https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json => …/data/observed-solar-cycle-indices.json
geomagindies: downloading ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-ap/ap_monyr.ave => …/data/ap_monyr.ave
              Ap    f107
2015-04-01  11.0  129.05
```

- 第一行下载实际失败（NGDC `CWD GEOMAGNETIC_DATA` → `550 Failed to change directory`，curl 复现），被 `except ConnectionError` 吞掉，**没有任何警告**。拼写 `geomagindies` 是上游原样。
- 3 月 17 日（圣帕特里克磁暴）离 4 月 1 日比离 3 月 1 日近，于是给的是 **4 月**月均：Ap 11（`ap_monyr.ave` 2015 行第 4 列）、F10.7 129.05（SWPC JSON `2015-04`）。
- 两个月均文件共 **512287 B + 5130 B**，首跑约 3 s。

### 3.2 时间数组、平滑

```python
import datetime as dt, pandas as pd, geomagindices as gi
t = pd.date_range("2024-05-09", "2024-05-13", freq="1D").to_pydatetime()
print(gi.get_indices(t))
print(gi.get_indices(dt.datetime(2024, 5, 11), smoothdays=81))
```
```
              Ap    f107
2024-05-01  24.0  188.37     ← 5 行一模一样（NGDC 年文件被重试 5 次，每个时刻一次）
…
              Ap    f107   f107s   Aps
2024-05-01  24.0  188.37  168.42  15.0
```

- `smoothdays` 的换算是 `天数 / (index[1]-index[0])`。退回月均后，81 天就变成 **3 个月**的**向后**滚动平均：f107s = (155.19+161.7+188.37)/3 = 168.42，Aps = (11+10+24)/3 = 15.0。这和惯用的 81 天**居中** F10.7A 不是一回事。
- `numpy.datetime64` 输入可以用；**带时区的 datetime 不行**：`TypeError: can't compare offset-naive and offset-aware datetimes`（`web.py:38`）。

### 3.3 近未来：URL 404；运行时改名即可

原样查明天：`ConnectionError: Could not download https://services.swpc.noaa.gov/text/45-day-ap-forecast.txt`（curl 实测 404、196 B）。SWPC 现在的文件叫 `45-day-forecast.txt`，格式不变。两个模块各持有一份 URL，两处都要改：

```python
import datetime as dt, geomagindices as gi
NEW = "https://services.swpc.noaa.gov/text/45-day-forecast.txt"
gi.web.URL45dayfcast = NEW; gi.dataio.URL45dayfcast = NEW
print(gi.get_indices([dt.datetime(2026, 9, 27, 6), dt.datetime(2026, 10, 5, 6)]))
```
```
geomagindies: downloading https://services.swpc.noaa.gov/text/45-day-forecast.txt => …/data/45-day-forecast.txt
              Ap   f107 resolution
2026-09-27  10.0   95.0          w
2026-10-05  15.0  110.0          w
```

与原文件（`:Issued: 2026 Sep 26 0000 UTC`，1539 B）的 `27Sep26 010` / `05Oct26 015`、F10.7 `27Sep26 095` / `05Oct26 110` 一致。缓存 1 天内不重下。“今天”用的是本机本地时间 `datetime.today()`。

### 3.4 远未来：包内 2016 预报表，Ap/F10.7 互换

```python
print(gi.get_indices([dt.datetime(2030, 1, 1), dt.datetime(2019, 12, 15)]))
print(gi.get_indices(dt.datetime(2035, 6, 1)))
```
```
                              Ap  f107 resolution
2030-01-01 02:37:40.799998  73.5  12.2          m
2019-12-01 16:55:11.999997  69.9   9.0          m
                              Ap  f107 resolution
2030-10-01 20:37:40.799998  70.1   9.4          m
```

- `May2016Rpt.txt` 该行是 `2030.0003 JAN 78.4 73.5 68.0 16.3 12.2 8.4`：50 % 分位 **F10.7 = 73.5、Ap = 12.2**。`read20yearfcast` 取第 3、6 列却命名为 `["Ap","f107"]`，**两列互换**。
- **过去**的 2019-12-15 也拿到了 2016 年的**预报**值：同一次调用里只要混有远未来时刻，预报表就和月均表拼在一起，`nearest` 选中了预报那一行。
- 2030-10 之后没有外推，一律返回最后一行，不报错。

### 3.5 月均合并顺序随进程随机

`load()` 把两个月均文件赋给一个空 DataFrame，**谁先赋值谁定 index**。F10.7 JSON 先：1749-01…2026-08（3332 行）；`ap_monyr.ave` 先：1932-01…2026-12（1140 行，含 `.` 缺测）。而文件列表来自 `list(set(...))`，顺序取决于 `PYTHONHASHSEED`：

```bash
for s in 0 1 2 3 4 5; do PYTHONHASHSEED=$s python -c \
 "import datetime as dt,geomagindices as gi;r=gi.get_indices(dt.datetime(2026,9,20));print(r.index[0].date(),r.values.tolist())"; done
```
```
seed0 2026-10-01 [[nan, nan]]
seed1 2026-08-01 [[9.0, 116.22]]
seed2 2026-08-01 [[9.0, 116.22]]
seed3 2026-10-01 [[nan, nan]]
seed4 2026-08-01 [[9.0, 116.22]]
seed5 2026-10-01 [[nan, nan]]
```

同一行代码，一半进程给 NaN，一半给 8 月的值。哪个 seed 给哪种结果还跟**安装路径**有关：`set` 里放的是完整缓存路径（`web.py:65` `list(set(flist))`）。venv 在 `/tmp/b60` 时 seed 0–2 给 NaN、3–5 有值；在 `/tmp/qc64` 时变成 seed 0/3/5 给 NaN。

### 3.6 真要日值 / 3 h 值：直连 GFZ（本机实跑）

```python
import requests, pandas as pd
def gfz(index, start, end):
    r = requests.get("https://kp.gfz.de/app/json/",
                     params={"start": start, "end": end, "index": index}, timeout=20)
    r.raise_for_status(); j = r.json()
    return pd.Series(j[index], index=pd.to_datetime(j["datetime"]), name=index)
t0, t1 = "2024-05-10T00:00:00Z", "2024-05-11T23:59:59Z"
print(pd.concat([gfz("Kp", t0, t1), gfz("ap", t0, t1)], axis=1).loc["2024-05-10T15":"2024-05-11T06"])
print(pd.concat([gfz("Ap", t0, t1), gfz("Fobs", t0, t1), gfz("Fadj", t0, t1)], axis=1))
```
```
                              Kp     ap
2024-05-10 15:00:00+00:00  7.667  179.0
2024-05-10 18:00:00+00:00  8.667  300.0
2024-05-10 21:00:00+00:00  8.667  300.0
2024-05-11 00:00:00+00:00  9.000  400.0
2024-05-11 03:00:00+00:00  8.333  236.0
2024-05-11 06:00:00+00:00  8.333  236.0
                              Ap   Fobs   Fadj
2024-05-10 00:00:00+00:00  105.0  223.4  227.9
2024-05-11 00:00:00+00:00  271.0  213.7  218.0
```

- GFZ 的时间戳是 3 h 区间的**起点**；geomagindices 原来的日值读法把时间标在**中点**（01:30、04:30…）。换源时别混。
- 每次请求只拉一个指数、一个时段，数据几百字节；匿名，CC BY 4.0。`Apstatus` 的 `def`/`pre` 含义见 [space-weather-indices](./space-weather-indices.md)。
- 喂 msise00 时，用 `indices={'f107':…,'f107s':…,'Ap':…}` 覆盖它内部调用的 geomagindices（见 [msise00](./msise00.md)）。

## 4. 字段

| 列 | 何时出现 | 含义 |
|---|---|---|
| `Ap` | 总是 | 日值源活着时是 3 h ap（列名却叫 Ap）；现在是**月均 Ap**；预报分支是预报日 Ap / 2016 表（被错当成 F10.7 的那列） |
| `Kp` | 只有日值源（已死） | 原始值 ÷10 |
| `f107` | 总是 | 观测 F10.7（sfu），日值源时整天 8 个 3 h 格重复同一值；现在是 SWPC 月均（`f10.7`，<0 置 NaN） |
| `f107s` `Aps` | 给了 `smoothdays` | 向后滚动平均，窗口 = 天数 ÷ 首两行间隔 |
| `resolution` | 日值 `d`、45 天 `w`、20 年 `m` | **月均退回路径不带这一列**，所以没法据此判断拿到的是不是月均 |
| index | — | 选中的数据时刻（**不是**你问的时刻），必须检查 |

## 5. 坑（现象 → 原因 → 修复）

1. **过去日期拿到 Ap 十几、没有 Kp 列** → NGDC FTP `KP_AP` 目录下线，异常被吞后退回月均 → 用 3.6 直连 GFZ；判断依据是 index 落在月初、并且没有 `Kp` 列。
2. **明天、未来 45 天：`ConnectionError …45-day-ap-forecast.txt`** → SWPC 改名 → 用 3.3 的双处改 URL。
3. **远未来 F10.7 只有 10 左右** → `read20yearfcast` 列名互换 → 自己交换两列，或直接读 `May2016Rpt.txt` 第 4 列（F10.7）、第 7 列（Ap）。
4. **过去日期返回带 `resolution m` 的奇怪时刻** → 同一调用混了远未来时刻，预报表参与了 nearest → 过去、未来分开调用。
5. **同一脚本时而 NaN 时而有值** → 月均合并顺序依赖 `set` 迭代顺序 → 设 `PYTHONHASHSEED=0` 之类只能让结果稳定，不能让它正确，而且换个安装路径结果又会变；近期日期别用本库。
6. **`TypeError: offset-naive and offset-aware`** → 内部拿本地 naive `today()` 比较 → 传 UTC naive datetime；本机若不在 UTC，“今天”的分界会按本地时间偏几小时。
7. **时间数组很慢、日志刷屏** → 每个过去时刻都重试一次 NGDC 年文件（失败的不缓存）→ 本库不适合批量。
8. **`forcedownload=True` 不刷新月均** → 退回路径只看文件年龄（30 天），忽略 `force` → 手动删 `data/` 下的 `observed-solar-cycle-indices.json` / `ap_monyr.ave`。
9. **`PermissionError`** → 缓存在包目录 → 装进自己的 venv；清理就删 `…/site-packages/geomagindices/data/` 下除 `May2016Rpt.txt`、`__init__.py` 外的文件。
10. **2026 当年 `ap_monyr.ave` 行尾是 `.`** → 未来月份缺测，`genfromtxt` 读成 NaN，属正常。

## 6. 选型

| 需求 | 选 |
|---|---|
| 真实 3 h Kp/ap、日 Ap、F10.7（定值/暂定） | GFZ API（3.6）或 [space-weather-indices](./space-weather-indices.md) |
| 只要粗略月均 F10.7/Ap 当气候态输入 | 本库原样可用，但要自己核 index 和 3.5 的 NaN |
| 未来 45 天预报 | 本库 + 3.3 补丁，或直接读 SWPC `45-day-forecast.txt` |
| 多源空间天气统一对象 | pysatSpaceWeather / [pyspedas](./pyspedas.md) |

## 7. 本机记录

- 2026-09-26 05:09–05:13 EDT。venv 与缓存放在 `/tmp/b60`，连同测试脚本已全部删除。
- 请求：NGDC FTP 失败尝试约 15 次（每次 <1 s）、SWPC JSON 1 次（512 KB）、GFZ `ap_monyr.ave` 1 次、SWPC 45 天预报 2 次、GFZ JSON API 6 次（每次 <300 B）。
- 上游问题（未提 issue；上游已开 #5 f107 缺值、#6 新数据源，自 2022 未动）：NGDC 源失效且静默退回、45 天 URL 404、20 年表列互换、月均合并顺序随机、混合时刻串表、时区比较、`force` 对月均无效、`resolution` 列缺失、`geomagindies` 拼写。
