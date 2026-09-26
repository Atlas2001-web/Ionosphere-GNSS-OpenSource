# 近实时电离层 TEC 产品：NOAA GloTEC / US-TEC 归档、DLR IMPC、UPC 实时 GIM、CODE 预报、CAS RTS、BoM SWS 的匿名获取与同历元对比

入口：[SWPC GloTEC](https://www.swpc.noaa.gov/products/glotec) · [GloTEC 数据目录](https://services.swpc.noaa.gov/products/glotec/) · [NCEI TEC 归档说明](https://www.ncei.noaa.gov/products/space-weather/ionospheric-program/total-electron-content) · [DLR IMPC NRT TEC](https://impc.dlr.de/products/total-electron-content/near-real-time-tec/near-real-time-tec-maps-global) · [UPC 实时](https://chapman.upc.es/tomion/real-time/quick/last_results/) · [CAS RTS](https://data.bdsmart.cn/pub/product/rts/iono/) · [BoM SWS TEC](https://www.sws.bom.gov.au/Satellite/2/1) · 本机验证 **2026-09-26 05:17–05:50 EDT**（匿名 curl，无注册、无表单）

> 岗位：回答“现在这一刻的全球 / 区域 TEC 去哪不登录拿、什么格式、多久更新一次、历史能往回拿多远、谁要账号”。最后把 4 个产品放到同一历元（2026-09-26 09:15 UTC）同一网格上两两比较。**只管近实时这一侧**：事后最终 / 快速 GIM 见 [gim-product-portals](./gim-product-portals.md)；读 IONEX 见 [ionex-gim](./ionex-gim.md)；Kp/Dst 等指数见 [space-weather-indices](./space-weather-indices.md)；闪烁见 [chain-scintillation](./chain-scintillation.md)。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E29](../data-access.md#dp-e29)
>
> 冲突时：以各服务当时的目录 / 文件元数据为准（只代表 2026-09-26 这一次）；“时延 = 上架时刻 − 图历元”“面积加权均差 / RMS”都是**本文口径**；各产品之间没有谁是真值。

## 1. 用途与边界

**做：** 各近实时产品的匿名路径、格式、更新间隔、实测时延、历史深度、登录门槛；同历元多产品比较。

**不做：** 最终 / 快速 GIM（→ [gim-product-portals](./gim-product-portals.md)）；ROTI / 闪烁指数产品（DLR 也有，但本文只测 TEC）；预报模型原理。

**结论先说：**

| 产品 | 匿名路径 | 格式 / 格网 | 更新 | 实测时延 | 历史 | 登录 |
| --- | --- | --- | --- | --- | --- | --- |
| **NOAA SWPC GloTEC** | `services.swpc.noaa.gov/products/glotec/geojson_2d_urt/` + 索引 `geojson_2d_urt.json` | GeoJSON，72×72 格心（2.5°×5°），`tec`/`anomaly`/`hmF2`/`NmF2`/`quality_flag` | 10 min | 21–24 min | 滚动 31 天（4464 个） | 无 |
| GloTEC 日 netCDF | `…/glotec/netcdf_2d_urt/GloTEC_TEC_YYYY_MM_DD.nc` | netCDF，约 14 MB/天；当天文件滚动增长 | 当天滚动（09:30 UTC 已更新） | — | 2025-05-12 起（503 个，连续） | 无 |
| **NCEI 归档** GloTEC / US-TEC | `archive.data.noaa.gov/satellite-spaceweather/SWPC/Models/{GLOTEC,USTEC}/…`（S3 列表可匿名） | 每天一个 tar.gz：GloTEC 约 280 MB，US-TEC 0.3–42 MB（文本 + PNG） | 每天 | GloTEC 次日 18:32 UTC 入库 | GloTEC 2025-02-24 起；**US-TEC 2004-10-14 至 2023-11-15（已停）** | 无 |
| **DLR IMPC** 全球 NRT TEC | `data.impc.dlr.de/tec-nowcast/DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL/latest/` | JSON（8.1 MB，含 73×73 节点 VTEC + 2.6 万 IPP）、HDF5（717 KB）、PNG、webm | 15 min | 2.6 min（09:15 图 09:17:38 生成） | **只有 latest 匿名**；历史目录 302 到 DLR SSO 登录 | 历史需账号 |
| **UPC 实时 usrg** | `chapman.upc.es/tomion/real-time/quick/last_results/usrgDDD0.YYi.Z` | IONEX（Unix compress），2.5°×5° | 15 min | 约 4–6 min | 当日文件从 00:00 累积；`archive.usrg/` 从 2019 年起（快照 / 动画 / 测站目录） | 无 |
| **CODE 预报** | `download.aiub.unibe.ch/CODE/COD0OPSP0D/P1D/P4D_…_01H_GIM.INX.gz` | IONEX，1 h | 每天 06:21 UTC | P1D 提前约 18 h | 源站根目录只留最近几天 | 无 |
| **CAS RTS** | `data.bdsmart.cn/pub/product/rts/iono/YYYY/DDD/` | IONEX 5 min：CAS1/CNE0/IGS0/IGS1/NRC0/UPC1/WHU0 `OPSRTS` | 每天一个文件（次日 00:30） | 约 0.5 h（按天） | 2021 年起；**DOY 268 探测时仍为空** | 无 |
| **BoM SWS** | `www.sws.bom.gov.au/Images/Satellite/Total%20Electron%20Content/…/TECGlobalMap.png` 等 | **只有 PNG 图** | 两次查看 Last-Modified 为 09:15:03 / 09:35:02，间隔未测准 | — | 无历史 | 数值 API 需 API key，且 API 不含 TEC |
| SWPC 旧 US-TEC 文本 | `services.swpc.noaa.gov/text/us-tec-total-electron-content.txt` | — | — | — | — | 404（已下线；历史见 NCEI） |

## 2. 安装

`curl`、`gzip`（`.Z` 用 `gzip -dc` 解）、`tar`、Python 3 + numpy（本机 `/usr/bin/python3`，numpy 2.2.4）。GeoJSON / JSON 用标准库 `json`；本文没读 netCDF / HDF5（本机无 netCDF4 / h5py）。

```bash
curl --version | head -1; /usr/bin/python3 -c "import numpy, json; print(numpy.__version__)"
```

## 3. 真命令 + 期望输出

### 3.1 可达性、最新历元、历史深度（`rtprobe.sh`）

```bash
#!/usr/bin/env bash
# 近实时电离层产品：匿名可达性、最新历元、上架时刻、历史深度（只列目录 / HEAD，不下大文件）
now(){ date -u '+%F %H:%M:%S UTC'; }
lm(){ curl -sI -m 30 "$1" | grep -i '^last-modified' | tr -d '\r' | cut -c16-; }
echo "## NOAA SWPC GloTEC（探测 $(now)）"
S=https://services.swpc.noaa.gov/products/glotec
curl -s -m 30 $S/geojson_2d_urt.json -o idx.json
/usr/bin/python3 -c "import json;d=json.load(open('idx.json'));print('geojson 索引', len(d), '条', d[0]['time_tag'], '→', d[-1]['time_tag'])"
t=$(/usr/bin/python3 -c "import json;print(json.load(open('idx.json'))[-1]['url'])"); echo "最新 $t  Last-Modified: $(lm https://services.swpc.noaa.gov$t)"
curl -s -m 30 $S/netcdf_2d_urt/ | grep -o 'GloTEC_TEC_[0-9_]*\.nc' | sort -u | awk 'NR==1{f=$0} {n++; l=$0} END{print "netCDF 日文件", n, "个", f, "→", l}'
echo "今天的 nc（滚动更新）Last-Modified: $(lm $S/netcdf_2d_urt/GloTEC_TEC_$(date -u +%Y_%m_%d).nc)"
echo "## NCEI 长期归档（S3 列表，匿名）"
A='https://archive.data.noaa.gov/satellite-spaceweather?list-type=2&prefix='
for p in SWPC/Models/GLOTEC/glotec/2025/02/ SWPC/Models/GLOTEC/glotec/2026/09/ SWPC/Models/USTEC/ustec/2004/10/ SWPC/Models/USTEC/ustec/2023/11/; do
  curl -s -m 30 "$A$p" | grep -o '<Key>[^<]*</Key><LastModified>[^<]*\|<Size>[^<]*' | sed 's/<[^>]*>/ /g' | paste - - | sed -n '1p;$p' | sed "s#SWPC/Models/##"; done
echo "旧 SWPC US-TEC 文本: $(curl -s -o /dev/null -w '%{http_code}' https://services.swpc.noaa.gov/text/us-tec-total-electron-content.txt)"
echo "## DLR IMPC（探测 $(now)）"
D=https://data.impc.dlr.de/tec-nowcast/DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL
curl -s -m 30 $D/latest/ | sed 's/<[^>]*>/ /g' | grep -E '_latest_' | awk '{print $1,$2,$3,$4}'
curl -s -m 30 -r 0-400 $D/latest/DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_latest_D.json | grep -o '"filename":"[^"]*"\|"created":"[^"]*"'
echo "历史目录: $(curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}' $D/ | cut -c1-80)"
echo "## UPC 实时 usrg / CODE 预报 / CAS RTS"
curl -s -m 30 https://chapman.upc.es/tomion/real-time/quick/last_results/ | sed 's/<[^>]*>/ /g' | grep '26i.Z' | awk '{print "UPC", $1, $2, $3, "(CEST)", $4}'
curl -s -m 60 'https://zhw-b.s3.cloud.switch.ch/aiub?prefix=CODE/COD0OPSP' | grep -o '<Key>[^<]*INX.gz</Key><LastModified>[^<]*' | sed 's/<\/Key><LastModified>/ /;s/<Key>CODE\///' | tail -3
for d in 267 268; do printf "CAS RTS %s: " $d; curl -s -m 30 https://data.bdsmart.cn/pub/product/rts/iono/2026/$d/ | sed 's/<[^>]*>/ /g' | grep INX | awk '{printf "%s %s %s %s; ", $1,$2,$3,$4}'; echo; done
echo "CAS RTS 年份: $(curl -s -m 30 https://data.bdsmart.cn/pub/product/rts/iono/ | grep -o 'href="20[0-9]*/"' | sed 's/href=//;s/"//g' | tr '\n' ' ')"
echo "## BoM SWS"
for f in Global%20Overview/TECGlobalMap.png Australasia%20Overview/TECRegionalMap.png; do echo "$f  Last-Modified: $(lm "https://www.sws.bom.gov.au/Images/Satellite/Total%20Electron%20Content/$f")"; done
echo "API 无 key: $(curl -s -m 30 -X POST -H 'Content-Type: application/json' -d '{}' https://sws-data.sws.bom.gov.au/api/v1/get-k-index)"
```

输出（原样，2026-09-26 09:37 UTC = 05:37 EDT）：

```text
## NOAA SWPC GloTEC（探测 2026-09-26 09:37:08 UTC）
geojson 索引 4464 条 2026-08-26T09:15:00Z → 2026-09-26T09:05:00Z
最新 /products/glotec/geojson_2d_urt/glotec_icao_20260926T090500Z.geojson  Last-Modified: Sat, 26 Sep 2026 09:28:27 GMT
netCDF 日文件 503 个 GloTEC_TEC_2025_05_12.nc → GloTEC_TEC_2026_09_26.nc
今天的 nc（滚动更新）Last-Modified: Sat, 26 Sep 2026 09:30:52 GMT
## NCEI 长期归档（S3 列表，匿名）
 GLOTEC/glotec/2025/02/glotec_2025_02_24.tar.gz  2026-01-08T16:19:21.000Z	 292917582
 GLOTEC/glotec/2025/02/glotec_2025_02_28.tar.gz  2026-01-08T16:28:12.000Z	 295045134
 GLOTEC/glotec/2026/09/glotec_2026_09_01.tar.gz  2026-09-02T18:32:21.000Z	 279757439
 GLOTEC/glotec/2026/09/glotec_2026_09_24.tar.gz  2026-09-25T18:32:01.000Z	 280938717
 USTEC/ustec/2004/10/ustec_2004_10_14.tar.gz  2026-01-13T22:45:45.000Z	 3958296
 USTEC/ustec/2004/10/ustec_2004_10_31.tar.gz  2026-01-13T22:45:25.000Z	 4321394
 USTEC/ustec/2023/11/ustec_2023_11_01.tar.gz  2026-01-14T03:27:32.000Z	 41886965
 USTEC/ustec/2023/11/ustec_2023_11_15.tar.gz  2026-01-14T03:27:41.000Z	 266903
旧 SWPC US-TEC 文本: 404
## DLR IMPC（探测 2026-09-26 09:37:14 UTC）
历史目录: 000 -> 
## UPC 实时 usrg / CODE 预报 / CAS RTS
UPC usrg2690.09.50.26i.Z 2026-09-26 11:34 (CEST) 16K
UPC usrg2690.26i.Z 2026-09-26 11:34 (CEST) 421K
COD0OPSP4D_20262710000_01D_01H_GIM.INX.gz 2026-09-24T12:44:29.398Z
COD0OPSP4D_20262720000_01D_01H_GIM.INX.gz 2026-09-25T06:20:19.657Z
COD0OPSP4D_20262730000_01D_01H_GIM.INX.gz 2026-09-26T06:21:20.842Z
CAS RTS 267: CAS1OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 502K; CNE0OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 422K; IGS0OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 447K; IGS1OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 447K; NRC0OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 503K; UPC1OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 447K; WHU0OPSRTS_20262670000_01D_05M_GIM.INX.gz 2026-09-25 00:30 488K; 
CAS RTS 268: 
CAS RTS 年份: 2021/ 2022/ 2023/ 2024/ 2025/ 2026/ 
## BoM SWS
Global%20Overview/TECGlobalMap.png  Last-Modified: Sat, 26 Sep 2026 09:35:02 GMT
Australasia%20Overview/TECRegionalMap.png  Last-Modified: Sat, 26 Sep 2026 09:36:03 GMT
API 无 key: {"errors":[{"code":21,"message":"Missing API key"}]}
```

注意这次 DLR 两行是空的 / `000`：09:37–09:45 UTC 之间 `data.impc.dlr.de` 连续 5 s 连接失败。**20 分钟前（09:17 UTC）同样的请求是通的**，当时的原样输出：

```text
Index of /tec-nowcast/DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL/latest
DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_latest_D.h5     2026-09-26 09:17  717K
DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_latest_D.json   2026-09-26 09:17  8.1M
DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_latest_I.png    2026-09-26 09:17  1.6M
DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_latest_V.webm   2026-09-26 09:05  3.1M
"filename":"DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL_2026-09-26T09-10-30_2026-09-26T09-15-00_269_D.json"
"created":"2026-09-26T09:17:38.687560"
历史目录 …/DLR_GNSS_GCG_L4_VTEC-NTCM-SCM_NC_GLOBAL/ → 302 https://sso.eoc.dlr.de/eoc/auth/oidc/oidcAuthorize?…client_id=impc-data-provisioning…
```

UPC 另一处细节（同次探测）：`last_results/usrg2690.09.50.26i.Z` 这个单图文件里只有一张 **09:30** 的图（`EPOCH OF FIRST/LAST MAP` 都是 09:30），09:34 UTC 上架——**文件名里的时刻不是图历元**。

### 3.2 各产品数据结构（本机拿到的样本）

- GloTEC GeoJSON 顶层：`time_tag`、`product: "GloTEC Total Electron Content"`、`cadence: 10`、`metadata.variables`（tec TECU 0–300、hmF2 km 200–600、NmF2 el/m³）；5184 个点 = 72 × 72，第一个点 `[-177.5, -88.75]`，`tec 8.25, anomaly 1.07, hmF2 334.5, NmF2 2.82e11, quality_flag 0`。
- DLR JSON：`metadata.details`（壳高 **400 km**、`delta_lat 2.5`、`delta_lon 5`、积分时间 270 s、`license: impc.dlr.de/terms-and-conditions`）；`data.grid` 5329 点 = 73 × 73 节点（−90…90、−180…180），属性 `vtec_assimilated_tecu`、`vtec_rms_tecu`、`vtec_model_tecu`；`data.ipps` 25,967 个穿刺点（含 `station`、`prn`、`azimuth`、`elevation`）。
- US-TEC 归档（`ustec_2023_11_15.tar.gz`，266,903 B，本机拉过）：`202311152345_TEC.txt`/`_ERR.txt`/两张 PNG；文本头 `Units: TEC: TECU x 10`、`Longitude, Latitude: degrees x 10`、`Missing data: 0`、`Cadence: 15 minutes`，这一天只剩 23:45 一个历元（产品末日）。

### 3.3 同历元 09:15 UTC 四产品对比（`rt.py`）

样本：GloTEC `glotec_icao_20260926T091500Z.geojson`（2,502,092 B）、DLR `latest_D.json`（09:17 拿到的 09:15 图，8,452,186 B）、UPC `usrg2690.26i.Z`（538,597 B）、CODE `COD0OPSP0D_20262690000_01D_01H_GIM.INX.gz`（199,644 B）。

```python
# 同一历元 2026-09-26 09:15 UTC：GloTEC / DLR IMPC / UPC 实时 / CODE 当日预报 放到同一 2.5°×5° 节点网格上两两比较
import subprocess, json, datetime as dt, numpy as np
T = dt.datetime(2026, 9, 26, 9, 15)
LAT = np.arange(87.5, -87.6, -2.5); LON = np.arange(-180, 180.1, 5)        # 71×73 节点（IONEX 惯例）
W = np.cos(np.radians(LAT))[:, None] * np.ones((1, LON.size))
def ionex_maps(path):
    txt = subprocess.run(['gzip', '-dc', path], capture_output=True).stdout.decode('ascii', 'replace').splitlines()  # .Z 是 Unix compress，Python gzip 模块读不了
    maps, grid, row, vals, ex, cur = {}, None, -1, [], -1, None
    for l in txt:
        lab = l[60:].strip()
        if lab == 'EXPONENT': ex = int(l[:60])
        elif lab == 'START OF TEC MAP': grid = np.full((71, 73), np.nan); row = -1
        elif lab == 'EPOCH OF CURRENT MAP' and grid is not None:
            cur = dt.datetime(*[int(float(x)) for x in l[:36].split()])
        elif lab == 'LAT/LON1/LON2/DLON/H' and grid is not None:
            if row >= 0: grid[row] = vals[:73]
            row += 1; vals = []
        elif lab == 'END OF TEC MAP':
            grid[row] = vals[:73]; grid[grid == 9999] = np.nan; maps[cur] = grid * 10.0 ** ex; grid = None
        elif lab.startswith('START OF RMS'): break
        elif grid is not None and row >= 0:
            vals += [float(l[k:k + 5]) for k in range(0, len(l.rstrip()), 5)]
    return maps
def glotec(path):
    d = json.load(open(path)); f = d['features']
    lon = np.array([x['geometry']['coordinates'][0] for x in f]); lat = np.array([x['geometry']['coordinates'][1] for x in f])
    tec = np.array([x['properties']['tec'] for x in f]); q = np.array([x['properties']['quality_flag'] for x in f])
    la, lo = np.unique(lat), np.unique(lon)                      # 格心 −88.75…88.75 / −177.5…177.5
    G = np.full((la.size, lo.size), np.nan); G[np.searchsorted(la, lat), np.searchsorted(lo, lon)] = tec
    # 双线性插到节点：经度周期延拓
    lo2 = np.r_[lo[-1] - 360, lo, lo[0] + 360]; G2 = np.c_[G[:, -1], G, G[:, 0]]
    tmp = np.array([np.interp(LON, lo2, r) for r in G2])        # (72, 73)
    out = np.array([np.interp(LAT[::-1], la, tmp[:, j]) for j in range(LON.size)]).T[::-1]
    return d['time_tag'], la.size, lo.size, out, np.bincount(q)
def dlr(path):
    d = json.load(open(path)); f = d['data']['grid']['features']
    lon = np.array([x['geometry']['coordinates'][0] for x in f]); lat = np.array([x['geometry']['coordinates'][1] for x in f])
    a = np.array([x['properties']['vtec_assimilated_tecu'] for x in f]); m = np.array([x['properties']['vtec_model_tecu'] for x in f])
    la, lo = np.unique(lat), np.unique(lon)
    A = np.full((la.size, lo.size), np.nan); M = A.copy()
    A[np.searchsorted(la, lat), np.searchsorted(lo, lon)] = a; M[np.searchsorted(la, lat), np.searchsorted(lo, lon)] = m
    sel = np.isin(la, LAT)
    return d['metadata']['temporal_coverage'] if 'temporal_coverage' in d['metadata'] else d['metadata']['details']['temporal_coverage'], \
        la.size, lo.size, A[sel][::-1], M[sel][::-1], len(d['data']['ipps']['features']), \
        len({x['properties']['station'] for x in d['data']['ipps']['features']})
gt, gnla, gnlo, GL, qc = glotec('g0915.geojson')
tc, dnla, dnlo, DA, DM, nipp, nsta = dlr('d.json')
U = ionex_maps('usrg.Z'); C = ionex_maps('codp0d.gz')
t0, t1 = T.replace(minute=0), T.replace(minute=0) + dt.timedelta(hours=1)
CP = C[t0] * 0.75 + C[t1] * 0.25                                    # CODE 1 h 预报图时间线性插到 09:15
P = {'GloTEC': GL, 'DLR(assim)': DA, 'DLR(model)': DM, 'UPC usrg': U[T], 'CODE P0D': CP}
print('产品 | 原始格网 | 历元 | 备注')
print(f'GloTEC | {gnla}×{gnlo} 格心 | {gt} | quality_flag 计数 {dict(enumerate(qc.tolist()))}；双线性插到节点')
print(f'DLR IMPC | {dnla}×{dnlo} 节点 | {tc["start_time"]}–{tc["end_time"]} | IPP {nipp} 个 / 测站 {nsta} 个；取 71×73 子集')
print(f'UPC usrg | 71×73 | {T} | 当日文件已有 {len(U)} 张图（{min(U):%H:%M}–{max(U):%H:%M}）')
print(f'CODE P0D | 71×73 | 09:00/10:00 线性插值 | 当日预报 {len(C)} 张图')
def wm(x): ok = np.isfinite(x); return np.sum((x * W)[ok]) / np.sum(W[ok])
print('\n全球面积加权均值 / 最大值（TECU）')
for k, v in P.items(): print(f'{k} | {wm(v):.2f} | {np.nanmax(v):.1f}')
print('\n两两差（行 − 列）：面积加权均差 / 面积加权 RMS（TECU；本文口径）')
ks = list(P); print('     | ' + ' | '.join(ks))
for a in ks:
    r = []
    for b in ks:
        if a == b: r.append('—'); continue
        d = P[a] - P[b]; r.append(f'{wm(d):+.2f} / {np.sqrt(wm(d * d)):.2f}')
    print(a, '| ' + ' | '.join(r))
```

输出（原样）：

```text
产品 | 原始格网 | 历元 | 备注
GloTEC | 72×72 格心 | 2026-09-26T09:15:00Z | quality_flag 计数 {0: 3865, 1: 188, 2: 172, 3: 154, 4: 145, 5: 660}；双线性插到节点
DLR IMPC | 73×73 节点 | 2026-09-26T09:10:30–2026-09-26T09:15:00 | IPP 25967 个 / 测站 621 个；取 71×73 子集
UPC usrg | 71×73 | 2026-09-26 09:15:00 | 当日文件已有 38 张图（00:00–09:15）
CODE P0D | 71×73 | 09:00/10:00 线性插值 | 当日预报 25 张图

全球面积加权均值 / 最大值（TECU）
GloTEC | 23.45 | 76.7
DLR(assim) | 19.96 | 69.1
DLR(model) | 19.14 | 61.3
UPC usrg | 21.75 | 87.4
CODE P0D | 23.16 | 79.0

两两差（行 − 列）：面积加权均差 / 面积加权 RMS（TECU；本文口径）
     | GloTEC | DLR(assim) | DLR(model) | UPC usrg | CODE P0D
GloTEC | — | +3.49 / 6.79 | +4.31 / 7.35 | +1.70 / 6.20 | +0.29 / 4.19
DLR(assim) | -3.49 / 6.79 | — | +0.82 / 3.75 | -1.79 / 7.33 | -3.20 / 6.00
DLR(model) | -4.31 / 7.35 | -0.82 / 3.75 | — | -2.61 / 7.99 | -4.03 / 6.68
UPC usrg | -1.70 / 6.20 | +1.79 / 7.33 | +2.61 / 7.99 | — | -1.42 / 5.13
CODE P0D | -0.29 / 4.19 | +3.20 / 6.00 | +4.03 / 6.68 | +1.42 / 5.13 | —
```

**对齐方式（本文做法）：** 目标网格 71×73 节点（87.5…−87.5 / 2.5°，−180…180 / 5°）。GloTEC 是格心（差半格），双线性插到节点，经度周期延拓；DLR 取节点子集；UPC 直接用；CODE 预报只有整点图，09:00 与 10:00 按 0.75/0.25 线性插值。DLR 壳高 400 km，UPC/CODE 450 km，GloTEC 是 3D 同化后积分，**壳高不同本身就带来差异**，这里不做换算。

**读法：** 这一刻（SWPC 行星 Kp：06 UT 档 2.67，03 UT 档 4.0，轻度扰动后回落；非强磁暴）全球面积加权均值 19.1–23.5 TECU；GloTEC 与 CODE 预报最接近（均差 +0.29、RMS 4.19）；DLR 同化值整体偏低 3–3.5 TECU；DLR 同化 vs 自家背景模型 RMS 3.75，说明同化改动幅度。GloTEC 有 1,319 / 5,184 个格点 `quality_flag` 非 0（本文没解释 flag 含义，未在上游文档里核到定义，比较时没有剔除）。

## 4. 输入 / 输出

| 产品 | 输入参数 | 输出 |
| --- | --- | --- |
| GloTEC | 时刻 → `glotec_icao_YYYYMMDDTHHMM00Z.geojson`（分钟为 05/15/…/55） | 单时刻 GeoJSON；日 netCDF |
| NCEI 归档 | 年/月 → `glotec_YYYY_MM_DD.tar.gz` / `ustec_YYYY_MM_DD.tar.gz` | tar.gz |
| DLR | 无参数，只有 `latest` | JSON / HDF5 / PNG / webm |
| UPC | 年积日 → `usrgDDD0.YYi.Z` | IONEX（当日累积）+ 单图文件 |
| CODE | 年积日 → `COD0OPSP0D/P1D/P4D_YYYYDDD0000_01D_01H_GIM.INX.gz` | IONEX |
| CAS RTS | 年/年积日 → `XXX?OPSRTS_YYYYDDD0000_01D_05M_GIM.INX.gz` | IONEX 5 min |
| BoM | 无 | PNG（全球 / 澳洲区域；另有中值图、扰动图） |

## 5. 参数：选产品看的量（本次实测）

| 量 | GloTEC | DLR | UPC usrg | CODE P0D | CAS RTS | BoM |
| --- | --- | --- | --- | --- | --- | --- |
| 历元间隔 | 10 min | 15 min（内部 5 min） | 15 min | 1 h | 5 min | 未测准 |
| 时延 | 21–24 min | 2.6 min | 4–6 min | 提前（预报） | 按天，次日 00:30 | — |
| 数值数据 | ✅ | ✅（latest） | ✅ | ✅ | ✅ | ❌ 只有 PNG |
| 匿名历史 | 31 天 geojson + 2025-05 起日 nc + NCEI | ❌（需 SSO） | 当日累积；历史见 [gim-product-portals](./gim-product-portals.md) | 最近几天 | 2021 起 | ❌ |
| 09:15 全球均值 | 23.45 | 19.96 | 21.75 | 23.16 | — | — |

## 6. 接到哪一步

| 下一步 | 去哪 |
| --- | --- |
| 事后精确对比（最终 GIM） | [gim-product-portals](./gim-product-portals.md) |
| 读 IONEX | [ionex-gim](./ionex-gim.md) · [ionex](./ionex.md) |
| 同期地磁指数 | [space-weather-indices](./space-weather-indices.md) |
| 用自己的测站算 TEC 对比 | [gnss-obs-mirrors](./gnss-obs-mirrors.md) → [pytecgg](./pytecgg.md) |
| 下载总表 | [data-access E29](../data-access.md#dp-e29) |

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | GloTEC 某时刻文件 404 | 比时间标签晚 21–24 min 才上架 | 先读索引 `geojson_2d_urt.json` 取最后一条 |
| 2 | 找不到一个月前的 GloTEC GeoJSON | 只滚动保留 31 天 | 用日 netCDF（2025-05-12 起）或 NCEI 归档 |
| 3 | NCEI 一天 280 MB | GloTEC 归档是全量 3D tar | 只要 2D TEC 用 SWPC 日 netCDF（约 14 MB） |
| 4 | 找 US-TEC 实时文本 404 | US-TEC 已停，最后一天 2023-11-15 | 历史去 NCEI `USTEC/ustec/YYYY/MM/` |
| 5 | DLR 历史目录跳登录页 | 只有 `latest/` 匿名，历史要 DLR SSO 账号 | 自己每 15 min 存一份 latest；或注册（本文没注册） |
| 6 | DLR 一会儿通一会儿不通 | 09:17 通，09:37–09:45 连续 5 s 超时 | 加重试；不要把单次失败当“下线” |
| 7 | GloTEC 与 IONEX 网格差半格 | GloTEC 是格心（±88.75 / ±177.5），IONEX 是节点 | 插值后再比；经度要周期延拓 |
| 8 | DLR 比别人低几 TECU | 壳高 400 km vs 450 km，方法也不同 | 标明壳高；不要当误差 |
| 9 | UPC `usrg…09.50…` 里是 09:30 的图 | 单图文件名的时刻不是历元 | 以文件内 `EPOCH OF CURRENT MAP` 为准 |
| 10 | Python `gzip` 打不开 UPC `.Z` | UPC `.Z` 是真 Unix compress（魔数 `1f 9d`）；而 CAS 镜像上的 `.Z` 其实是 gzip（`1f 8b`） | 统一用 `gzip -dc` 或按魔数分支 |
| 11 | CAS RTS 前一天目录为空 | DOY 268 在次日 09:4x UTC 仍未上架；DOY 267 文件只有平时 1/4 大小 | 取前两天；检查图数 |
| 12 | BoM 想要数值 | 网页只给 PNG；数值 API 需 API key 且不含 TEC | 数值用 GloTEC / UPC / DLR |
| 13 | 把某一家当真值 | 这些都是模型 / 同化产品 | 只做相对比较；真值用独立测站（[gnss-obs-mirrors](./gnss-obs-mirrors.md)） |
| 14 | GloTEC `quality_flag` 非 0 占 25% | 本文未核到 flag 定义 | 使用前查 SWPC 产品说明；本文未剔除 |

## 8. 选型

| 需求 | 选 | 不选 |
| --- | --- | --- |
| 最新全球 TEC 数值、最快 | DLR `latest`（约 3 min）/ UPC usrg（约 5 min） | GloTEC（约 22 min） |
| 近 1 个月逐 10 min 全球 + hmF2/NmF2 | GloTEC GeoJSON | DLR（历史需账号） |
| 2025 年以来日文件 | GloTEC netCDF | — |
| 2004–2023 北美 | NCEI US-TEC 归档 | SWPC 实时（已停） |
| 明天的全球图 | CODE P1D | 实时产品 |
| IGS RTS 各中心 5 min 解码 IONEX | CAS RTS | — |
| 给公众看图 | BoM PNG / DLR PNG | — |
