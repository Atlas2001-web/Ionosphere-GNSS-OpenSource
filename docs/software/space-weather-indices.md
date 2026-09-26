# 空间天气指数直连（GFZ Kp/ap/Hp30 · NOAA SWPC JSON · Kyoto WDC Dst/AE · OMNI via CDAWeb HAPI）· 下载侧 操作手册

入口：[GFZ Kp](https://kp.gfz.de/en/data) · [SWPC services](https://services.swpc.noaa.gov/) · [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · [CDAWeb HAPI](https://cdaweb.gsfc.nasa.gov/hapi) · 本机验证 **2026-09-26 04:00–04:25 EDT**。四个源都**不需要登录**；只用了 curl 和系统 Python 3.13 标准库（`json` / `csv` / `urllib` / `statistics`），没有装第三方库。样例是 **2024-05-10 00 UT → 05-13 00 UT**（Gannon 超级磁暴）。临时文件放在 `/workspace/swwork`，用完即删。

> 岗位：不用 PySPEDAS，直接从 HTTP 拿 **Kp、ap、Hp30、F10.7、Dst、AE、SYM-H 和时移太阳风**，并且分清每个值当前处于哪种数据状态（实时 / 暂定 / 确定）。用 PySPEDAS 一行加载同样这批指数，见 [pyspedas](./pyspedas.md)；地磁台站分钟值见 [geomag-api](./geomag-api.md)。本文不重复这两篇。  
> 门槛总表：[data-access 决策表](../data-access.md#电离层与地磁门户决策表) · [E15 GFZ Kp](../data-access.md#dp-e15) · [E16 SWPC](../data-access.md#dp-e16) · [E17 Kyoto WDC](../data-access.md#dp-e17) · [E18 OMNI/HAPI](../data-access.md#dp-e18)。  
> 冲突时：**各源的 status 字段 / 页面标题 / 参数描述 > 本文**；数据状态会随时间升级，重跑前先看第 4 节。

## 1. 它解决什么，边界在哪

| 源 | 给什么 | 格式 | 状态怎么标 | 本文定位 |
| --- | --- | --- | --- | --- |
| **GFZ** `kp.gfz.de/app/json/` | Kp、ap、Ap、Cp、C9、Hp30/60、ap30/60、SN、Fobs/Fadj | JSON | `status`（Kp、ap、Cp、C9）/ `Apstatus` / `SNstatus`：`def` 或 `pre`；**Hp30、Fobs 没有状态字段** | Kp 的权威来源 |
| **SWPC** `services.swpc.noaa.gov` | 实时 Kp（1 min 估计值 / 3 h）、RTSW 太阳风 1 min（等离子体 + 磁场）、F10.7、Kyoto Dst 转发 | JSON | 全是实时估计值，不会升级；历史值要去 NCEI 归档 | 实时监测 |
| **Kyoto WDC** | Dst（小时值）、AE / AL / AU / AO（分钟值） | HTML `<pre>` / WDC 定宽文本 | **URL 路径**（`dst_final` / `dst_provisional` / `dst_realtime`）加页面标题 | Dst / AE 原始出处 |
| **OMNI**（CDAWeb HAPI） | 时移到弓激波鼻点的 1 min 太阳风，外加 SYM-H、AE（1 min）；OMNI2 小时值里有 Kp、Dst、F10.7 | CSV / JSON（HAPI 2.0） | 写在各参数 `description` 的年份区间里 | 事后分析、多量同表 |

**不覆盖**：SuperMAG（需要注册）、预报类产品（SWPC 的 forecast、Enlil）、PC 指数的细节。

## 2. 安装

```bash
curl --version | head -1; python3 -c "import json, csv, urllib.request, statistics; print('ok')"
```

## 3. 真实命令与输出

### 3.1 GFZ Kp / ap / Hp30 JSON（含 status）

```bash
curl -sL "https://kp.gfz.de/app/json/?start=2024-05-10T00:00:00Z&end=2024-05-12T21:00:00Z&index=Kp"
```

```text
{"Kp":[2.667,2.667,2.333,2.0,3.667,7.667,8.667,8.667,9.0,8.333,8.333,9.0,8.667,8.333,7.667,7.667,6.333,7.0,3.667,4.333,2.0,3.0,4.0,6.333],
 "datetime":["2024-05-10T00:00:00Z", … ,"2024-05-12T21:00:00Z"], "meta":{"license":"CC BY 4.0","source":"GFZ Potsdam"}, "status":["def", …]}
```

- **结束时刻是闭区间**：`end=…21:00` 会把 21 UT 那一档也包含进来，所以正好 24 个值。`datetime` 是区间的**起点**（GFZ 数据页原文：“Die Datums- und Zeitangabe bezieht sich immer auf den Startzeitpunkt”）。
- 其他指数，同一天 00–03 UT 的实测结果：
  - `ap` → `[12.0,12.0]`，带 `status`；`Ap` → `105.0`，带 `Apstatus`；`Cp` → `1.9`；`C9` → `8.0`。
  - `Hp30` → 7 个值 `[1.667,3.0,…]`，**没有** `status`；`ap30` → `[6.0,15.0,…]`；`Hp60` → 4 个值。
  - `SN` → `172.0`，带 `SNstatus:def`；`Fobs` → `223.4`；`Fadj` → `227.9`。
  - `index=xyz` → **HTTP 500 HTML 页**，不是 JSON 错误。
- `kp.gfz-potsdam.de` 会 301 到 `kp.gfz.de`，所以要加 `-L`。

**状态分段**（最近 40 天，在 08:00 UT 查询）：

```text
def 2026-08-17T00:00:00Z -> 2026-08-31T21:00:00Z 120
pre 2026-09-01T00:00:00Z -> 2026-09-26T06:00:00Z 203
```

- 加 `&status=def` 后只返回 120 个值，截止到 08-31 21 UT。定值是**按月**发布的（数据页写的是 “DOI-archive, monthly updated”）。
- 当前这一个 3 小时档（06–09 UT）在区间还没结束时就已经给出，标成 `pre`。实测里**没有出现 `now`** 这个状态。
- Hp30 最新一个值是 07:30 UT（值为 2.333），延迟不到 1 h。

### 3.2 SWPC JSON：实时 Kp、太阳风、F10.7

```bash
S=https://services.swpc.noaa.gov
curl -s $S/json/planetary_k_index_1m.json          # 200，27,925 B，358 行（约 6 h）
curl -s $S/products/noaa-planetary-k-index.json    # 200，4,484 B，58 行（7 天，3 h）
curl -s $S/json/rtsw/rtsw_wind_1m.json             # 200，2,670,019 B，3,610 行
curl -s $S/json/rtsw/rtsw_mag_1m.json              # 200，1,519,952 B，3,601 行
curl -s $S/json/f107_cm_flux.json                  # 200，123 行
curl -s $S/products/10cm-flux-30-day.json          # 200，30 行
curl -s $S/products/solar-wind/plasma-1-day.json   # 404（旧产品，已下线）
```

```text
planetary_k_index_1m   {"time_tag":"2026-09-26T07:54:00","kp_index":2,"estimated_kp":2.0,"kp":"2Z"}
noaa-planetary-k-index {"time_tag":"2026-09-26T03:00:00","Kp":4.0,"a_running":27,"station_count":8}
rtsw_wind_1m (第 1 行) {"time_tag":"2026-09-26T07:55:00","active":true,"source":"SOLAR1","proton_speed":470.1,"proton_density":2.58,…}
rtsw_mag_1m  (第 1 行) {"time_tag":"2026-09-26T07:55:00","active":true,"source":"SOLAR1","bt":6.2,"bz_gsm":…,…}
f107_cm_flux           2026-09-25 17:00 106.0 Morning / 20:00 105.0 Noon / 22:00 104.0 Afternoon
10cm-flux-30-day       {"time_tag":"2026-09-25T20:00:00","flux":105}
```

字段说明：
- **`kp` 字符串**：数字加一个字母，Z = 整数、M = 减 1/3、P = 加 1/3。实测对应关系：`4M` → 3.67，`2P` → 2.33，`0P` → 0.33。`kp_index` 是取整后的整数。
- **RTSW** 把**多颗卫星**混在同一个文件里，按时间倒序排列，用 `source` 和 `active` 区分。实测：SOLAR1 为 `active=true`，1,039 行；ACE 和 IMAP 为 `false`，各约 1,200–1,400 行。**必须先过滤 `active==true`**，否则同一分钟会有多条记录。
- **F10.7**：每天有 Morning、Noon、Afternoon 三次观测；30 天产品只保留 20 UT（Noon）这一次。GFZ 的 `Fobs` 在 2026-09-25 是 105.4，SWPC 的 Noon 值是 105。
- `products/kyoto-dst.json` 是 Kyoto 实时 Dst 的转发，168 行（7 天）。

**历史值**：SWPC JSON 只保留几天，要拿 2024-05 的值得去 NCEI 归档：

```bash
curl -s https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/annual_reports/daily_solar_indices_summaries/daily_geomagnetic_data/2024Q2_DGD.txt
# 200，10,710 B；最后 8 列是 "Estimated Planetary K"
# 2024 05 11   175  9 8 7 8 7 6 6 6   208  8 6 9 9-1-1 6 5   273   9.00  8.33  8.67  9.00  8.67  8.33  7.33  7.33
```

旧地址 `ftp.swpc.noaa.gov/pub/indices/old_indices/…` 连接失败（000），`www.swpc.noaa.gov/ftpdir/…` 返回 404。

### 3.3 Kyoto WDC：Dst（HTML）与 AE（WDC 文本）

**URL 规律**（2026-09-26 实测状态码）：

| 状态 | URL | 可用月份 |
| --- | --- | --- |
| final | `https://wdc.kugi.kyoto-u.ac.jp/dst_final/YYYYMM/index.html` | 到 **2020-12**（202101 起返回 404） |
| provisional | `…/dst_provisional/YYYYMM/index.html` | **2021-01 → 2026-07**（202608 返回 404） |
| realtime | `…/dst_realtime/YYYYMM/index.html` | **2026-08 起**；更早的月份返回 **403** |
| AE provisional | `…/ae_provisional/YYYYMM/aeYYMMDD.for.request`（`al…`、`au…`、`ao…` 同名，内容相同） | 202405 实测 200 |

**Dst 解析器 `kyoto_dst.py`**。数值是定宽排列，负数会粘在一起（如 `-33-131-157`），缺测写成 `9999`，会连写成 `99999999…`：

```python
import re, sys, urllib.request
def kyoto_dst(yyyymm, state='provisional'):          # state: final | provisional | realtime
    url = f'https://wdc.kugi.kyoto-u.ac.jp/dst_{state}/{yyyymm}/index.html'
    html = urllib.request.urlopen(url, timeout=60).read().decode('ascii', 'replace')
    pre = html.split('<pre class="data">')[1].split('</pre>')[0]
    label = re.search(r'Hourly Equatorial Dst Values \((\S+?)\s*\)', pre).group(1)
    out = {}
    for line in pre.splitlines():
        if not re.match(r'^\s?\d{1,2} ', line): continue
        day = int(line[:2])
        body = line[3:]
        # 3 groups x 8 values, each value right-aligned in 4 chars, 1 extra space between groups
        vals = [body[g*33 + i*4: g*33 + i*4 + 4] for g in range(3) for i in range(8)]
        for h, v in enumerate(vals):          # column "1" = 00-01 UT
            v = v.strip()
            if v and v != '9999':
                out[(day, h)] = int(v)
    return label, out
if __name__ == '__main__':
    label, d = kyoto_dst(sys.argv[1], sys.argv[2])
    k = min(d, key=d.get)
    print(label, 'hours', len(d), 'min', d[k], 'at day', k[0], 'hour', f'{k[1]:02d}-{k[1]+1:02d} UT')
```

```text
$ python3 kyoto_dst.py 202405 provisional
PROVISIONAL hours 744 min -406 at day 11 hour 02-03 UT
$ python3 kyoto_dst.py 202609 realtime
REAL-TIME hours 608 min -43 at day 25 hour 13-14 UT        # 25 天 × 24 + 8：当天 08 UT 之后都是 9999
$ python3 kyoto_dst.py 202012 final
FINAL hours 744 min -28 at day 22 hour 09-10 UT
```

5 月 10 日这一行解析出 `[…, 25, 66, -33, -131, -157, -277, -339, -308]`：SSC 之后的 +66 出现在 17–18 UT。

**AE 文本格式**：每行 400 字符。第 1–8 列是 `AEALAOAU`，第 13–18 列是 `yymmdd`，第 20–21 列是小时，第 22–23 列是 `AE` / `AL` / `AU` / `AO`，从第 35 列起是 60 个 `I6` 分钟值，最后一个是小时均值。文件末行写着 `[Created at Thu May 16 01:37:09 UTC 2024]`，说明这份暂定 AE 是事件后 6 天生成的快照；页面也注明 “still tentative … to be updated”。

### 3.4 OMNI 1 min via CDAWeb HAPI（info → data）

```bash
H=https://cdaweb.gsfc.nasa.gov/hapi
curl -s "$H/capabilities"                      # "HAPI": "2.0"，格式 csv / json / binary
curl -s "$H/info?dataset=OMNI_HRO_1MIN"        # 1400 "missing required parameter id"：HAPI 2.0 用 id=
curl -s "$H/info?id=OMNI_HRO_1MIN"             # 200，5,647 B；startDate 1981-01-01，stopDate 2026-09-03T00:39:00Z
curl -s "$H/data?id=OMNI_HRO_1MIN&time.min=2024-05-10T00:00:00Z&time.max=2024-05-13T00:00:00Z&parameters=Timeshift,BZ_GSM,flow_speed,AE_INDEX,SYM_H"
# 200，226,800 B，0.85 s，4,320 行（time.max 不包含在内）
# 2024-05-10T00:00:00.000Z,999999,9999.99,99999.9,118,6
# 2024-05-12T23:59:00.000Z,2446,2.46,798.6,539,-83
curl -s "$H/data?id=OMNI2_H0_MRG1HR&time.min=2024-05-10T00:00:00Z&time.max=2024-05-13T00:00:00Z&parameters=KP1800,DST1800"
# 72 行，首行 2024-05-10T00:30:00.000Z,27,12   ← 时间戳是半点（小时中点），KP1800 = Kp × 10
```

`info` 里的**填充值**（节选）：`Timeshift` / `RMS_Timeshift` 为 999999；`BX…BZ`、`F` 为 9999.99；`flow_speed`、`Vx…Vz` 为 99999.9；`proton_density` 为 999.99；`T` 为 9999999.0；`AE_INDEX`、`SYM_H` 为 99999；`IMF` / `PLS`（卫星 ID）为 99。

**时移说明**：官方文档（[HROdocum](https://omniweb.gsfc.nasa.gov/html/HROdocum.html)）原文是 “solar wind magnetic field and plasma data sets time-shifted to the Earth's bow shock nose”，时间戳是 “at start of average”。GSM 分量 “determined from post-shift GSE components”。`Timeshift` 列就是每分钟实际用到的传播时间。实测 2024-05-10–12：中位数 1,519 s，范围 −454 → 7,850 s；卫星 ID 全是 51（Wind），没有 ACE（71）。

**参数描述里写着的状态区间**（本身就是状态标签）：
- `SYM_H`：“from WDC Kyoto (1981/001-2026/243)”，即数据截止到 2026-08-31。
- `DST1800`：“Provisional Dst (2021/001-2026/212), Quick-look Dst (2026/213-2026/259)”，即暂定值到 07-31，quick-look 从 08-01 到 09-16。
- `AE_INDEX`：描述写 “Provisional 1990/001-2020/365”，**但 2024 年实际有值**（见坑 9）。

### 3.5 同一场暴的对比（`compare.py`，2024-05-10 00 UT → 05-13 00 UT；需要同目录下的 `kyoto_dst.py`）

```python
import json, csv, urllib.request, statistics as S, datetime as dt
from kyoto_dst import kyoto_dst
UA = {'User-Agent': 'Mozilla/5.0'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read().decode()
T0 = dt.datetime(2024, 5, 10, tzinfo=dt.timezone.utc)

# 1) Kp: GFZ JSON vs SWPC estimated planetary K (NCEI archive of DGD)
g = json.loads(get('https://kp.gfz.de/app/json/?start=2024-05-10T00:00:00Z&end=2024-05-12T21:00:00Z&index=Kp'))
gfz = g['Kp']
dgd = get('https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/annual_reports/'
          'daily_solar_indices_summaries/daily_geomagnetic_data/2024Q2_DGD.txt')
swpc = []
for day in ('10', '11', '12'):
    line = [l for l in dgd.splitlines() if l.startswith('2024 05 ' + day)][0]
    swpc += [float(x) for x in line.split()[-8:]]           # last 8 columns = Estimated Planetary K
d = [s - k for s, k in zip(swpc, gfz)]
print('Kp n', len(d), 'GFZ status', set(g['status']), '| max GFZ', max(gfz), 'max SWPC', max(swpc))
print('Kp SWPC-GFZ mean %.3f  MAE %.3f  max|d| %.3f  exact %d/24  within 1/3 %d/24' % (
      S.mean(d), S.mean(map(abs, d)), max(map(abs, d)), sum(abs(x) < 1e-6 for x in d), sum(abs(x) <= 0.34 for x in d)))
print('  largest (|d|, slot):', [(round(a, 3), i) for a, i in sorted(zip(map(abs, d), range(24)), reverse=True)[:3]])

# 2) Dst: Kyoto provisional vs OMNI2 hourly DST1800 vs hourly mean of OMNI 1-min SYM-H
label, ky = kyoto_dst('202405', 'provisional')
kyl = [ky[(10 + i // 24, i % 24)] for i in range(72)]
H = 'https://cdaweb.gsfc.nasa.gov/hapi/data?id='
o2 = list(csv.reader(get(H + 'OMNI2_H0_MRG1HR&time.min=2024-05-10T00:00:00Z&time.max=2024-05-13T00:00:00Z'
                         '&parameters=KP1800,DST1800').splitlines()))
om2 = [int(r[2]) for r in o2]
o1 = list(csv.reader(get(H + 'OMNI_HRO_1MIN&time.min=2024-05-10T00:00:00Z&time.max=2024-05-13T00:00:00Z'
                         '&parameters=Timeshift,BZ_GSM,flow_speed,AE_INDEX,SYM_H').splitlines()))
symh = [int(r[5]) for r in o1]
symh_h = [S.mean(symh[i*60:(i+1)*60]) for i in range(72)]
dd = [a - b for a, b in zip(om2, kyl)]
print('Dst Kyoto', label, 'min', min(kyl), '@h', kyl.index(min(kyl)), '| OMNI2 DST1800 min', min(om2), '| OMNI2-Kyoto max|d|', max(map(abs, dd)))
ds = [a - b for a, b in zip(symh_h, kyl)]
print('SYM-H(1h mean)-Dst: mean %.1f  MAE %.1f  max|d| %.1f  r=%.3f | SYM-H 1-min min %d @ %s' % (
      S.mean(ds), S.mean(map(abs, ds)), max(map(abs, ds)), S.correlation(symh_h, kyl), min(symh),
      o1[symh.index(min(symh))][0]))
kp2 = [int(r[1]) / 10 for r in o2][::3]
print('OMNI2 KP1800/10 vs GFZ: max|d| %.3f' % max(abs(a - b) for a, b in zip(kp2, gfz)))

# 3) AE: Kyoto provisional WDC file vs OMNI 1-min AE_INDEX
ae = []
for day in ('10', '11', '12'):
    txt = get(f'https://wdc.kugi.kyoto-u.ac.jp/ae_provisional/202405/ae2405{day}.for.request')
    for l in txt.splitlines():
        if l[:8] == 'AEALAOAU' and l[21:23] == 'AE':
            ae += [int(l[34 + 6*i: 40 + 6*i]) for i in range(60)]
oae = [int(r[4]) for r in o1]
dae = [a - b for a, b in zip(oae, ae) if a != 99999 and b != 99999]
print('AE n', len(ae), 'Kyoto max', max(ae), '| OMNI AE max', max(x for x in oae if x != 99999), '| identical', sum(x == 0 for x in dae), '/', len(dae))

# 4) fills & time shift in OMNI 1-min
fill = {'Timeshift': 999999, 'BZ_GSM': 9999.99, 'flow_speed': 99999.9}
for j, (k, f) in enumerate(fill.items(), start=1):
    print('OMNI fill', k, sum(float(r[j]) == f for r in o1), '/', len(o1))
ts = [int(r[1]) for r in o1 if int(r[1]) != 999999]
print('Timeshift s: median %d  min %d  max %d' % (S.median(ts), min(ts), max(ts)))
bz = [float(r[2]) for r in o1 if float(r[2]) != 9999.99]
print('BZ_GSM min %.2f  flow_speed max %.1f' % (min(bz), max(float(r[3]) for r in o1 if float(r[3]) != 99999.9)))
```

```text
$ python3 compare.py
Kp n 24 GFZ status {'def'} | max GFZ 9.0 max SWPC 9.0
Kp SWPC-GFZ mean 0.015  MAE 0.237  max|d| 0.997  exact 4/24  within 1/3 21/24
  largest (|d|, slot): [(0.997, 4), (0.67, 20), (0.663, 19)]
Dst Kyoto PROVISIONAL min -406 @h 26 | OMNI2 DST1800 min -406 | OMNI2-Kyoto max|d| 0
SYM-H(1h mean)-Dst: mean -6.2  MAE 11.0  max|d| 51.3  r=0.995 | SYM-H 1-min min -518 @ 2024-05-11T02:14:00.000Z
OMNI2 KP1800/10 vs GFZ: max|d| 0.033
AE n 4320 Kyoto max 4098 | OMNI AE max 4098 | identical 4320 / 4320
OMNI fill Timeshift 681 / 4320
OMNI fill BZ_GSM 681 / 4320
OMNI fill flow_speed 1478 / 4320
Timeshift s: median 1519  min -454  max 7850
BZ_GSM min -47.85  flow_speed max 1025.9
```

槽位 4 = 05-10 12 UT：GFZ 3.667，SWPC 2.67。

**同一流程的近期版本**（SWPC 7 天 3 h Kp 对比 GFZ `pre`，2026-09-19 00 → 09-26 03 UT，共 58 档）：SWPC−GFZ 均值 +0.184，MAE 0.288，max|d| 1.000，完全相同 16/58。

**解读**：
- **Kp**：SWPC 的估计值和 GFZ 定值整体无偏（+0.015），MAE 约 0.24，21/24 档相差不超过 1/3，最大差一整级。OMNI2 的 `KP1800` 与 GFZ 只差取整（≤0.033），也就是说 OMNI 转载的是 GFZ Kp。
- **Dst**：OMNI2 的 `DST1800` 与 Kyoto 暂定值**逐小时完全相同**。SYM-H 的小时均值和 Dst 相关系数 0.995，但主相附近最多差 51 nT；1 分钟 SYM-H 的最低值 −518 nT（02:14 UT）比小时 Dst 的最低值（−406）深 112 nT。
- **AE**：OMNI 的 `AE_INDEX` 与 Kyoto 暂定 AE 在 4,320 分钟里完全相同。

## 4. 数据三种状态：各源怎么标，什么时候升级

| 源 | 实时 / nowcast | 暂定 / quasi-definitive | 确定 | 本机看到的切换点（2026-09-26） |
| --- | --- | --- | --- | --- |
| GFZ Kp、ap、Cp、C9、SN | `pre`（当前 3 h 档在区间结束前就给出） | 同样是 `pre`（没有单独的中间态） | `def` | def 到 2026-08-31 21 UT，此后都是 pre；**按月**转定值 |
| GFZ Hp30 / Hp60、Fobs | 无状态字段 | — | — | Hp30 最新值是 07:30 UT，延迟不到 1 h |
| SWPC | 所有 JSON 都是 “estimated” | 无 | 无（归档里仍是估计值） | 1 min Kp 保留约 6 h；3 h Kp 保留 7 天 |
| Kyoto Dst | `dst_realtime`（REAL-TIME） | `dst_provisional`（PROVISIONAL） | `dst_final`（FINAL） | realtime ≥ 2026-08；provisional 为 2021-01 → 2026-07；final ≤ 2020-12 |
| Kyoto AE | `ae_realtime`（图 + `data_dir/`） | `ae_provisional`（注明 tentative） | `ae_final`（202405 返回 404） | 2024-05 的暂定 AE 生成于 2024-05-16 |
| OMNI（HAPI） | — | 写在参数描述里（Dst：Provisional 到 2026/212，Quick-look 为 2026/213–259） | 同上（Dst 确定值 1963–2014） | HRO 1 min stopDate 2026-09-03；plasma 数据截止 09-02 |

各源**都没有公布**确切的升级日期。上表是根据当天可访问的 URL 和字段反推的；以后重跑时，同一个时间窗的状态可能会变。

## 5. 输入与输出

- **时间约定**：
  - GFZ：区间起点（`YYYY-MM-DDThh:mm:ssZ`）。
  - SWPC：`time_tag` 没有 Z，实际是 UT。**Kyoto 转发 Dst 用的是小时起点**：SWPC 的 07:00 = −41，对应 Kyoto 实时页 26 日第 8 列（07–08 UT）= −41。
  - Kyoto：列号 “1” 表示 00–01 UT。
  - OMNI 1 min：平均区间起点；OMNI2 小时值：**半点**。
- **输出**：JSON 数组或对象（GFZ、SWPC）、`<pre>` 定宽文本（Kyoto Dst）、400 字符定宽行（Kyoto AE）、HAPI CSV（首列是 ISO 时间，后面各列按 `parameters` 的顺序排列）。
- **许可**：GFZ `meta.license` 为 “CC BY 4.0”；其他源请按各自官方页面致谢（本文没有逐一核对条款）。

## 6. 在工作流里接哪一步

- **路径 B · 不规则体 / 磁暴**（[README](./README.md#b--不规则体--磁暴)）：先用 Kp / Hp30 定暴时，用 SYM-H 和 Dst 定主相深度，用 OMNI 的 Bz 和 V 定驱动，用 AE 定亚暴；然后再去对 ROTI / TEC。脚本见 3.5。
- **路径 A · 一日 TEC**（[README](./README.md#a--一日-tec)）：用 Kp 和 F10.7 标注当天的背景是平静还是扰动；F10.7 取 GFZ `Fobs` 或 SWPC Noon 值。
- 需要在 Python 里统一成 tplot 变量时，换 [pyspedas](./pyspedas.md)；需要台站原始磁场时，看 [geomag-api](./geomag-api.md)。

## 7. 坑（现象 → 原因 → 修复）

1. **HAPI 返回 1400 “missing required parameter id”** → CDAWeb 实现的是 HAPI **2.0**，参数名是 `id=`、`time.min=`、`time.max=`（3.x 的 `dataset=` / `start=` 不认）→ 先看 `/capabilities` 的版本号。
2. **HAPI HTTP 200，但 CSV 里只有一段 JSON 错误** → 参数顺序和 `info` 里的顺序不一致（`BZ_GSM,…,Timeshift`）会得到 status 1411 “Parameter out of order”，而 HTTP 状态码照样是 200 → 按 `info` 的顺序写 `parameters`，并检查首行是不是时间戳。
3. **OMNI 的数值出现 999999、9999.99、99999.9** → 这些是填充值，不同列不一样 → 按 `info.parameters[].fill` 逐列替换成 NaN。2024-05-10–12 期间 Timeshift 和 Bz 有 681/4320 是填充，flow_speed 有 1478/4320。
4. **Kyoto Dst 用 `split()` 解析报错或错位** → 负数会粘连（`-33-131`），缺测会连写（`9999…`）→ 按列宽切：`line[3:]` 之后每组 8 个值、每个 4 字符，组间多 1 个空格（见 `kyoto_dst.py`）。
5. **Kyoto 旧月份的 realtime 页返回 403，新月份的 final 页返回 404** → 同一时间段只在一个状态目录下能打开 → 按 final → provisional → realtime 依次试，并把页面标题里的状态存下来。
6. **SWPC 太阳风里同一分钟有 2–3 条记录** → RTSW 把 SOLAR1、ACE、IMAP 混在一个文件里，而且按时间倒序 → 过滤 `active==true` 再排序。
7. **旧脚本里的 `products/solar-wind/plasma-1-day.json` 等返回 404** → 这些产品已下线（`products/` 目录里已经没有 `solar-wind/`）→ 改用 `json/rtsw/rtsw_{wind,mag}_1m.json`。
8. **想用 SWPC JSON 回看 2024 年的 Kp** → JSON 只保留几天，旧的 FTP / ftpdir 路径也失效了 → 用 NCEI 上的季度 `…/daily_geomagnetic_data/YYYYQn_DGD.txt`（最后 8 列）。注意其中 College 站的列用 `-1` 表示缺测，而且会粘连（`9-1-1`）。
9. **OMNI `AE_INDEX` 的描述写着只到 2020 年** → 实测 2024-05 有值，而且与 Kyoto 暂定 AE 逐分钟相同 → 描述已过时，但也要记住这些是**暂定**值，Kyoto 那边还可能再改。
10. **OMNI2 小时值和 Kyoto 的小时对不齐** → HAPI 给 OMNI2 打的是半点时间戳（`00:30`），Kyoto 用列号（“1” = 00–01），SWPC 转发 Dst 时标在小时起点 → 统一换算成“小时起点 UT”再比。
11. **拿 SYM-H 的最低值和 Dst 的最低值比，差了 112 nT** → 1 分钟最小值和小时均值不是同一个量 → 先对 SYM-H 做 60 分钟平均再比（MAE 11 nT，r=0.995）。
12. **GFZ 近期 Kp 被当成定值用了** → 近期值是 `pre`，而且 Hp30 根本没有状态字段 → 发表用的数据加 `&status=def`，并记录查询日期。
13. **GFZ 写错指数名得到 HTML 500** → 服务端没做参数校验 → 只用数据页列出的指数名：Kp、ap、Ap、Cp、C9、Hp30、Hp60、ap30、ap60、SN、Fobs、Fadj。

## 8. 选型对比

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 发表用的 Kp / ap | **GFZ** `&status=def` | 权威来源，有状态字段，CC BY 4.0 |
| 更细的活动时间分辨率（30 min） | GFZ **Hp30** | 延迟不到 1 h；没有状态字段 |
| 实时监测（Kp、太阳风、F10.7） | **SWPC JSON** | 分钟级更新；只有估计值；要过滤 `active` |
| 小时 Dst，并看清状态 | **Kyoto** 页面 | 状态写在路径和标题里；需要自己写定宽解析 |
| 1 min 太阳风 + SYM-H + AE 放在同一张表 | **OMNI HRO via HAPI** | 已时移到弓激波鼻点，一次请求拿齐；最新数据约滞后 3 周 |
| Kp、Dst、F10.7 小时级合表 | OMNI2 `OMNI2_H0_MRG1HR` | 与 GFZ / Kyoto 一致（实测 Dst 差 0，Kp 差 ≤0.033） |
| 在 Python 里一行加载 | [pyspedas](./pyspedas.md) | 背后是同样这些源 |
| 台站原始磁场、dB/dt | [geomag-api](./geomag-api.md) | 指数之外的原始数据 |
