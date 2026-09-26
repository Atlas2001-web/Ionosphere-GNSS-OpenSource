# NASA ICON 与 GOLD 数据获取（SPDF HTTPS · CDAWeb / CDAS REST · HAPI 覆盖实测 · GOLD SOC）· 下载与读取 操作手册

入口：[SPDF ICON](https://spdf.gsfc.nasa.gov/pub/data/icon/) · [SPDF GOLD](https://spdf.gsfc.nasa.gov/pub/data/gold/) · [CDAWeb](https://cdaweb.gsfc.nasa.gov/) · [CDAS REST](https://cdaweb.gsfc.nasa.gov/WebServices/REST/) · [CDAWeb HAPI](https://cdaweb.gsfc.nasa.gov/hapi) · [GOLD SOC 下载页](https://gold.cs.ucf.edu/data/search/) · [GOLD 数据产品指南 Rev5.2 PDF](https://spdf.gsfc.nasa.gov/pub/data/gold/documentation/GOLD_Public_Science_Data_Products_Guide_Rev5.2.pdf) · 本机验证 **2026-09-26 04:15–04:50 EDT**。所有入口都**不需要登录**。样例：ICON 取 **2021-11-04**（Kp 7+ 磁暴日）的 MIGHTI 红线矢量风整日文件（5.5 MB），IVM 只用 CDAS REST 拿 9 个变量的子集（4.3 MB，原文件 52 MB）；GOLD 取 **2024-05-11（2024/132）** 的 NMAX（3.95 MB）和 ON2（0.57 MB）。读取用临时 venv（`netCDF4` + `numpy` + `cdflib`），工作目录 `/workspace/igwork` 用完即删。

> 岗位：拿 NASA 两颗电离层–热层任务的数据：**ICON**（2019–2022，低倾角 LEO；IVM 离子漂移、MIGHTI 中性风 / 温度、FUV O/N₂ 与夜间 O⁺、EUV O⁺ 剖面）和 **GOLD**（2018 起，静止轨道 47.5°W 远紫外成像光谱仪；ON2、TDISK、NMAX、O2DEN、QEUV、TLIMB），并把质量标志、填充值和网格读对。用 PySPEDAS 统一加载 CDAWeb 数据集见 [pyspedas](./pyspedas.md)；COSMIC-2 电子密度剖面见 [cosmic2-ro](./cosmic2-ro.md)；Kp / Dst 等背景指数见 [space-weather-indices](./space-weather-indices.md)。本文不重复这几篇。  
> 门槛总表：[data-access 决策表](../data-access.md#电离层与地磁门户决策表) · [E21 ICON（SPDF / CDAWeb）](../data-access.md#dp-e21) · [E22 GOLD（SPDF / SOC / CDAWeb）](../data-access.md#dp-e22)。  
> 冲突时：**文件内的 Var_Notes / VAR_NOTES、GOLD 数据产品指南与发布说明、GOLD SOC 版本表 > 本文**；版本号会更新（ICON 在 2026 年仍在重处理），重跑前先列目录。

## 1. 它解决什么，边界在哪

| 任务 | 仪器 → L2 产品（SPDF 目录名） | 物理量 | 覆盖 |
| --- | --- | --- | --- |
| **ICON**（发射 2019-10-10；2019-12-15 进入主任务；**2022-11-25 15:00 UT 最后一次联络**后失联；NASA 2024-07-24 宣布任务结束） | IVM：`l2-7_ivm-a`（`ivm-b` 只有 2021-06-14～06-27） | 离子漂移（经向 / 纬向 / 场向）、离子密度、温度、成分，1 s | 轨道高度约 576–610 km，纬度 ±27°（样例日实测） |
| | MIGHTI：`l2-1_mighti-{a,b}_los-wind-{green,red}`、`l2-2_mighti_vector-wind-{green,red}`、`l2-3_mighti-{a,b}_temperature` | 视线风、合成矢量风（红线约 150–300 km，绿线约 90–300 km）、温度 | 切点纬度约 −15°～40°（样例日红线 q=1） |
| | FUV：`l2-4_fuv_day`、`l2-4_fuv_day-limb`、`l2-5_fuv_night` | 白天 O/N₂ 柱比、日间临边、夜间 135.6 nm O⁺ 剖面 | |
| | EUV：`l2-6_euv` | 日间 O⁺ 密度剖面 | |
| | 另有 `l0p`、`l1`、`l3`（`climatology/ ionosphere/ o-plus/ wind-temperature/`）、`l4`（`hme/ sami3/ tiegcm*`） | | |
| **GOLD**（静止轨道，SPDF 与 SOC 数据从 2018-10-05 起） | `level1c`（DAY / LIM / DLM / OCC / NI1 扫描）；`level2/{on2,tdisk,nmax,o2den,qeuv,tlimb}` | ON2 = O/N₂ 柱比（日面）；TDISK = 日面中性温度；NMAX = 夜间 F 峰电子密度（135.6 nm）；O2DEN = 恒星掩星 O₂ 密度剖面；QEUV = 太阳 EUV 代理；TLIMB = 临边温度 | 只看美洲–大西洋–西非半球：样例 ON2 经度 −114°～18°，NMAX −92°～13° |

**不覆盖**：ICON L0/L1 的读取、FUV/EUV 剖面的反演细节、GOLD L1C 光谱的使用（一天 95 个文件共约 2.85 GB，本轮没下）、GUVI 的实际读取（只核了目录，见第 8 节）。

## 2. 安装

```bash
python3 -m venv venv && venv/bin/pip -q install netCDF4 numpy cdflib    # 本机 venv 约 119 MB，用完删
```

ICON / GOLD 的 SPDF 原始文件都是 **netCDF-4**；CDAS REST 返回的子集是 **CDF**（用 `cdflib` 读）。

## 3. 真实命令与输出

### 3.1 SPDF 目录树与文件大小

```bash
curl -s https://spdf.gsfc.nasa.gov/pub/data/icon/        # documentation/ l0p/ l0p_ancillary/ l1/ l2/ l3/ l4/
curl -s https://spdf.gsfc.nasa.gov/pub/data/icon/l2/     # 000readme.txt + 14 个产品目录
curl -s https://spdf.gsfc.nasa.gov/pub/data/gold/        # documentation/ level0/ level1a/ level1anc/ level1b/ level1c/ level1d/ level2/
curl -s https://spdf.gsfc.nasa.gov/pub/data/gold/level2/ # nmax/ o2den/ on2/ qeuv/ tdisk/ tlimb/
```

路径模板（实测）：

```text
ICON  https://spdf.gsfc.nasa.gov/pub/data/icon/l2/<product>/<YYYY>/icon_<product>_<YYYYMMDD>_v<VV>r<RRR>.nc
      例 …/icon/l2/l2-2_mighti_vector-wind-red/2021/icon_l2-2_mighti_vector-wind-red_20211104_v06r000.nc
GOLD  https://spdf.gsfc.nasa.gov/pub/data/gold/level2/<product>/<YYYY>/gold_l2_<product>_<YYYY>_<DDD>_v<VV>_r<RR>_c<CC>.nc
      例 …/gold/level2/nmax/2024/gold_l2_nmax_2024_132_v05_r01_c01.nc
      L1C：…/gold/level1c/<YYYY>/<DDD>/GOLD_L1C_CHA_DAY_2024_132_08_10_v04_r01_c01.nc（每次扫描一个文件）
```

ICON 的 `l2/000readme.txt` 原文：SPDF 把文件名改成了全小写、日期从 `yyyy-mm-dd` 改成 `yyyymmdd`，并把 Epoch 维改成 unlimited（所以文件内 `File` 属性仍是 `ICON_L2-2_MIGHTI_Vector-Wind-Red_2021-11-04_v06r000.NC`）；还写着 `l2-4_fuv_day` 曾因 2021 年变量名错误暂停下载（2022-12-21 加注）。本轮该目录 200，2021-11-04 文件在列。

文件大小（目录列表实测，ICON 为 2021-11-04，GOLD 为 2024/132 → 2026/186）：

| 产品 | 单日文件 | 版本（文件名） |
| --- | --- | --- |
| ICON L2-7 IVM-A | 46–52 MB | v08r002（SPDF 时间戳 2026-03-19） |
| ICON L2-1 MIGHTI-A LOS 绿线 | 13 MB | v06r000 |
| ICON L2-2 MIGHTI 矢量风 绿 / 红 | 17 MB / 5.3 MB | v06r000（2026-04-07） |
| ICON L2-3 MIGHTI-A 温度 | 5.1 MB | v06r001 |
| ICON L2-4 FUV day / day-limb | 812 KB / 3.6 MB | v07r001（2026-03-31） |
| ICON L2-5 FUV night | 95 MB | v07r000 |
| ICON L2-6 EUV | — | v03r004（2022 年最后一个文件 20221125） |
| GOLD L2 NMAX | 3.8 MB → 4.5 MB | v05 r01 |
| GOLD L2 ON2 | 561 KB → 878 KB | v04 r02 |
| GOLD L2 TDISK | 499 KB → 774 KB | v05 r03 |
| GOLD L2 TLIMB / QEUV / O2DEN | 310–455 KB / 214–248 KB / 157 KB | v05 r01 / v03 r01 / v06 r01 |
| GOLD L1C（2024/132 全天） | 95 个文件，每个 20–85 MB，合计约 2850 MB | v04 r01（OCC 为 v05） |

GOLD SOC 下载页写的“一天典型大小”：L1C DAY 6 GB、LIM 500 MB、OCC 80 MB、NI1 1.5 GB、L1D 150 MB。

### 3.2 CDAWeb 和 HAPI：CDAWeb 有，HAPI 没有

```bash
curl -s -o cat.json -w "%{http_code} %{size_download}\n" https://cdaweb.gsfc.nasa.gov/hapi/catalog
python3 -c "
import json; c=json.load(open('cat.json'))['catalog']; print('total',len(c))
ic=[d['id'] for d in c if d['id'].upper().startswith('ICON')]; print('ICON',len(ic)); print(ic)
g=[d['id'] for d in c if 'GOLD' in d['id'].upper() or 'GUVI' in d['id'].upper() or 'TIMED' in d['id'].upper()]; print('GOLD/GUVI/TIMED',g)
"
```

```text
200 108011
total 3632
ICON 0
[]
GOLD/GUVI/TIMED ['TIMED_EDP_GUVI', 'TIMED_L1BV20_SABER', 'TIMED_L1CDISK_GUVI@0', 'TIMED_L1CDISK_GUVI@1', 'TIMED_L2A_SABER', 'TIMED_L3A_SEE', 'TIMED_WINDVECTORSNCAR_TIDI@0', 'TIMED_WINDVECTORSNCAR_TIDI@1', 'TIMED_WINDVECTORSNCAR_TIDI@2', 'TIMED_WINDVECTORSNCAR_TIDI@3']
```

直接问 `info`：

```text
curl -s "https://cdaweb.gsfc.nasa.gov/hapi/info?id=ICON_L2-7_IVM-A"  →  {"HAPI": "2.0", "status": {"code": 1406, "message": "Bad request - unknown dataset id"}}  [HTTP 400]
curl -s "https://cdaweb.gsfc.nasa.gov/hapi/info?id=GOLD_L2_NMAX"     →  同上 1406  [HTTP 400]
curl -s "https://cdaweb.gsfc.nasa.gov/hapi/info?id=TIMED_EDP_GUVI"   →  200；startDate 2002-01-07T05:53:28Z，stopDate 2007-10-04T23:20:59Z，29 个参数
```

CDAWeb 本身（CDAS REST 的数据集列表，`curl -s -H "Accept: application/json" https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/datasets`，2992 个数据集）里筛出的 ICON / GOLD（原样，按 ID 排序）：

```text
GOLD_L2_NMAX 2018-10-05 2026-07-06 | GOLD Peak Electron density NMAX L2 Daily Files - Richard Eastes (Unive
GOLD_L2_O2DEN 2018-10-19 2026-07-05 | GOLD O2DEN L2 Daily Fileof O2 density - Richard Eastes (University of 
GOLD_L2_ON2 2018-10-05 2026-07-05 | GOLD: O to N2 column ratio - Richard Eastes (University of Colorado/LA
GOLD_L2_TDISK 2018-10-05 2026-07-05 | GOLD TDISK Neutral Temperatures - Richard Eastes (University of Colora
ICON_L2-1_MIGHTI-A_LOS-WIND-GREEN 2019-12-06 2022-11-24 | Michelson Interferometer for Global High-resolution Thermospheric Imag
ICON_L2-1_MIGHTI-A_LOS-WIND-RED 2019-12-06 2022-11-24 | Michelson Interferometer for Global High-resolution Thermospheric Imag
ICON_L2-1_MIGHTI-B_LOS-WIND-GREEN 2019-12-06 2022-11-24 | Michelson Interferometer for Global High-resolution Thermospheric Imag
ICON_L2-1_MIGHTI-B_LOS-WIND-RED 2019-12-06 2022-11-24 | Michelson Interferometer for Global High-resolution Thermospheric Imag
ICON_L2-2_MIGHTI_VECTOR-WIND-GREEN 2019-12-06 2022-11-25 | MIGHTI - Cardinal Vector Winds - T. J. Immel (UC Berkeley>SSL)
ICON_L2-2_MIGHTI_VECTOR-WIND-RED 2019-12-06 2022-11-25 | MIGHTI - Cardinal Vector Winds - T. J. Immel (UC Berkeley>SSL)
ICON_L2-3_MIGHTI-A_TEMPERATURE 2019-12-06 2022-11-24 | ICON MIGHTI-A Level 2.3 Retrieved Temperature File - T. J. Immel (UC B
ICON_L2-3_MIGHTI-B_TEMPERATURE 2019-12-06 2022-11-24 | ICON MIGHTI-B Level 2.3 Retrieved Temperature File - T. J. Immel (UC B
ICON_L2-4_FUV_DAY 2019-11-16 2022-11-25 | ICON FUV Daytime: column density ratio of thermospheric atomic oxygen 
ICON_L2-4_FUV_DAY-LIMB 2019-11-16 2022-11-25 | ICON FUV Daytime Limb - T. J. Immel (UC Berkeley > SSL)
ICON_L2-5_FUV_NIGHT 2019-11-16 2022-11-25 | FUV Short Wavelength Channel - 135.6 Altitude Profiles (night) - T. J.
ICON_L2-6_EUV 2019-11-12 2022-11-25 | ICON EUV derived ionospheric data products - T. J. Immel (UC Berkeley>
ICON_L2-7_IVM-A 2019-11-15 2022-11-24 | ICON Ion Velocity Meter (IVM) Thermal Plasma Measurements - T. J. Imme
ICON_L2-7_IVM-B 2021-06-14 2021-06-27 | ICON IVM Thermal Plasma Measurements B - T. J. Immel (UC Berkeley>SSL)
```

结论：**CDAWeb 有 ICON 的 14 个 L2 数据集和 GOLD 的 4 个 L2 数据集（ON2 / NMAX / O2DEN / TDISK；没有 QEUV、TLIMB、L1C），HAPI 端点两者都没有**（目录 3632 个 ID 里 0 个，`info` 回 1406 / HTTP 400）。按 ID 取子集要走 **CDAS REST**（或 PySPEDAS / cdasws，它们底层也是这个接口）。

### 3.3 CDAS REST：只取 ICON IVM 的 9 个变量

```bash
V=ICON_L27_Ion_Velocity_Meridional,ICON_L27_Ion_Velocity_Zonal,ICON_L27_Ion_Density,ICON_L27_DM_Flag,ICON_L27_RPA_Flag,ICON_L27_Latitude,ICON_L27_Longitude,ICON_L27_Altitude,ICON_L27_Solar_Local_Time
curl -s -H "Accept: application/json" "https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/datasets/ICON_L2-7_IVM-A/data/20211104T000000Z,20211105T000000Z/$V?format=cdf"
```

```text
{"FileDescription":[{"Name":"https://cdaweb.gsfc.nasa.gov/tmp/wsU1FrVh/icon_l2-7s_ivm-a_20211104000000_20211104235959_cdaweb.cdf","MimeType":"application/x-cdf","StartTime":"2021-11-04T00:00:00.000Z","EndTime":"2021-11-05T00:00:00.000Z","Length":4307271,"LastModified":"2026-09-26T08:18:34.187Z"}],"Message":[],"Warning":[],"Status":[],"Error":[]}
```

再 `curl` 那个 `Name`（`/tmp/` 下的临时文件）→ `200 4307271`。ICON 数据集一共 108 个变量（`…/datasets/ICON_L2-7_IVM-A/variables`）。同样的接口对 GOLD 也可用：`GOLD_L2_ON2` 有 19 个变量（CDAWeb 额外加了 `on2_north_mv` / `on2_south_mv` 等虚拟变量），`…/GOLD_L2_ON2/data/20240511T000000Z,20240512T000000Z/on2?format=cdf` 返回 70,256 B 的 CDF；`…/orig_data/…` 则直接指回原始 netCDF（`https://cdaweb.gsfc.nasa.gov/sp_phys/data/gold/level2/on2/2024/gold_l2_on2_2024_132_v04_r02_c01.nc`，574,864 B）。

`ivm.py`（原样）：

```python
import cdflib, numpy as np
c = cdflib.CDF("ivm_subset.cdf")
info = c.cdf_info()
print("zVariables:", info.zVariables)
t = cdflib.cdfepoch.to_datetime(c.varget("Epoch_cdf"))           # CDF_EPOCH: the real time axis
print("Epoch_cdf records:", len(t), t[0], "->", t[-1], "| cadence s:", np.unique(np.round(np.diff(t).astype("timedelta64[ms]").astype(int) / 1000))[:4])
e = c.varget("Epoch")                                             # CDF_INT8, ms since 1970 (from the netCDF original)
print("Epoch (INT8 ms) records:", len(e), "| first 3:", e[:3].tolist(), "| equals Epoch_cdf for first N:",
      bool(np.all(np.abs(e[:len(t)] - (t - np.datetime64("1970-01-01")).astype("timedelta64[ms]").astype(np.int64)) <= 1)))
for k in ["ICON_L27_Ion_Velocity_Meridional", "ICON_L27_Ion_Density", "ICON_L27_DM_Flag", "ICON_L27_RPA_Flag"]:
    a = c.varattsget(k)
    print(k, "| UNITS", a.get("UNITS"), "| FILLVAL", a.get("FILLVAL"), "| VALIDMIN/MAX", a.get("VALIDMIN"), a.get("VALIDMAX"))
    print("   CATDESC:", str(a.get("CATDESC"))[:200])
    if "VAR_NOTES" in a: print("   VAR_NOTES:", str(a["VAR_NOTES"])[:400])
vm = c.varget("ICON_L27_Ion_Velocity_Meridional").astype(float); vz = c.varget("ICON_L27_Ion_Velocity_Zonal").astype(float)
ni = c.varget("ICON_L27_Ion_Density").astype(float); dm = c.varget("ICON_L27_DM_Flag"); rpa = c.varget("ICON_L27_RPA_Flag")
lat = c.varget("ICON_L27_Latitude"); alt = c.varget("ICON_L27_Altitude"); slt = c.varget("ICON_L27_Solar_Local_Time")
fill = c.varattsget("ICON_L27_Ion_Velocity_Meridional")["FILLVAL"]
print("DM_Flag values:", dict(zip(*[x.tolist() for x in np.unique(dm, return_counts=True)])))
print("RPA_Flag values:", dict(zip(*[x.tolist() for x in np.unique(rpa, return_counts=True)])))
isfill = lambda x: (x == fill) | ~np.isfinite(x) | (np.abs(x) > 1e30)
print("meridional drift fill: %d / %d" % (isfill(vm).sum(), len(vm)))
good = (dm == 0) & ~isfill(vm)
print("DM_Flag==0 & not fill: %d (%.1f%%)" % (good.sum(), 100 * good.mean()))
print("lat %.1f..%.1f ; alt %.1f..%.1f km ; SLT %.1f..%.1f h" % (lat.min(), lat.max(), alt.min(), alt.max(), slt.min(), slt.max()))
print("good meridional (vertical-ish) drift m/s: median %.1f p5 %.1f p95 %.1f" % (np.median(vm[good]), *np.percentile(vm[good], [5, 95])))
okn = (rpa == 0) & ~isfill(ni)
print("RPA_Flag==0 ion density cm^-3: n=%d median %.3e p95 %.3e" % (okn.sum(), np.median(ni[okn]), np.percentile(ni[okn], 95)))
day = good & (slt >= 10) & (slt <= 14); night = good & ((slt >= 22) | (slt <= 2))
print("meridional drift median: SLT 10-14 h %.1f m/s (n=%d) ; SLT 22-02 h %.1f m/s (n=%d)" % (np.median(vm[day]), day.sum(), np.median(vm[night]), night.sum()))
```

```text
zVariables: ['Epoch_cdf', 'time_base', 'ICON_L27_Ion_Velocity_Meridional', 'ICON_L27_Ion_Velocity_Zonal', 'ICON_L27_Ion_Density', 'ICON_L27_DM_Flag', 'ICON_L27_RPA_Flag', 'ICON_L27_Latitude', 'ICON_L27_Longitude', 'ICON_L27_Altitude', 'ICON_L27_Solar_Local_Time', 'Epoch']
Epoch_cdf records: 86397 2021-11-04T00:00:00.062000000 -> 2021-11-04T23:59:59.208000000 | cadence s: [1. 5.]
Epoch (INT8 ms) records: 172796 | first 3: [1635983999062, 1635984000062, 1635984001062] | equals Epoch_cdf for first N: False
ICON_L27_Ion_Velocity_Meridional | UNITS m/s | FILLVAL nan | VALIDMIN/MAX -500.0 500.0
   CATDESC: Meridional Ion Velocity
   VAR_NOTES: Ion velocity along local magnetic meridional direction, perpendicular to geomagnetic field and within local magnetic meridional plane. The local meridional vector maps to vertical at the magnetic equator, positive is up.   Velocity obtained using ion velocities relative to co-rotation in the instrument frame along with the corresponding unit vectors expressed in the instrument frame to express the
ICON_L27_Ion_Density | UNITS N/cc | FILLVAL nan | VALIDMIN/MAX 7000.0 3000000.0
   CATDESC: Ion density determined using RPA measurements.
   VAR_NOTES: Ion density uses measured currents and co-rotating atmosphere to determine density.
ICON_L27_DM_Flag | UNITS None | FILLVAL 9999 | VALIDMIN/MAX 0 7
   CATDESC: None
   VAR_NOTES: Drift meter quality flag. 0 - Good data. 1 - Data may have artifacts due to s/c operations. 2 - Data temporarily removed for photoemission. 3 - Not enough O+ to measure arrival angle.
ICON_L27_RPA_Flag | UNITS None | FILLVAL 9999 | VALIDMIN/MAX 0 3
   CATDESC: RPA Quality Flag
   VAR_NOTES: Status flag for RPA.  0 - All RPA parameters are good. Ion temperatures correspond to both O+ and H+.  1 - Ram Ion Velocities are not good. Other parameters good. Plasma is presumed to be co-rotating when fitting RPA curves that have an insufficient quantity of O+. Ion temperatures correspond to H+ only.  2 - Geophysical outputs may be impacted by spacecraft operations.
DM_Flag values: {0: 45933, 1: 16598, 3: 23866}
RPA_Flag values: {0: 66077, 1: 20040, 2: 280}
meridional drift fill: 8060 / 86397
DM_Flag==0 & not fill: 42373 (49.0%)
lat -27.1..27.1 ; alt 575.7..609.6 km ; SLT 0.0..24.0 h
good meridional (vertical-ish) drift m/s: median -2.5 p5 -31.6 p95 28.0
RPA_Flag==0 ion density cm^-3: n=66076 median 1.274e+05 p95 4.526e+05
meridional drift median: SLT 10-14 h 1.9 m/s (n=6741) ; SLT 22-02 h 2.1 m/s (n=8319)
```

要点：

- **`DM_Flag`**（漂移计，决定速度能不能用）：0 好；1 可能受航天器操作影响；2 为去光电子暂时移除；3 O⁺ 不足、测不了到达角。当天 0 / 1 / 3 分别 45933 / 16598 / 23866 点，再去掉 NaN 后可用速度只有 **42373 点（49.0 %）**。
- **`RPA_Flag`**（阻滞势分析器，决定密度 / 温度）：0 全好 66077；1 冲压方向速度不好（且离子温度只对应 H⁺）20040；2 受航天器操作影响 280。
- `Ion_Velocity_Meridional` 是**垂直于磁场、在磁子午面内**的分量，磁赤道处就是**垂直向上为正**；可用点中位数 −2.5 m/s，p5 / p95 为 −31.6 / 28.0 m/s。离子密度单位 `N/cc`（= cm⁻³），RPA_Flag=0 时中位数 1.27e5 cm⁻³。
- 填充值：速度和密度是 **NaN**（`FILLVAL nan`），标志是 **9999**。
- 时间轴用 **`Epoch_cdf`**（CDF_EPOCH，86397 条，1 s，偶有 5 s 间隔）。子集里另有一个 `Epoch`（CDF_INT8，毫秒，来自 netCDF 原件），它有 172796 条、比 `Epoch_cdf` 早 1 s 开始，逐条对不上——不要拿它当时间轴。

### 3.4 读 ICON MIGHTI 红线矢量风整日文件

```bash
S=https://spdf.gsfc.nasa.gov/pub/data; for u in icon/l2/l2-2_mighti_vector-wind-red/2021/icon_l2-2_mighti_vector-wind-red_20211104_v06r000.nc gold/level2/nmax/2024/gold_l2_nmax_2024_132_v05_r01_c01.nc gold/level2/on2/2024/gold_l2_on2_2024_132_v04_r02_c01.nc; do curl -s -O -w "%{http_code} %{size_download} %{time_total}s $(basename $u)\n" "$S/$u"; done
```

```text
200 5513380 1.021650s icon_l2-2_mighti_vector-wind-red_20211104_v06r000.nc
200 3952273 1.108317s gold_l2_nmax_2024_132_v05_r01_c01.nc
200 574864 0.869197s gold_l2_on2_2024_132_v04_r02_c01.nc
```

通用查看脚本 `dump.py`（原样）：

```python
import netCDF4, sys
ds = netCDF4.Dataset(sys.argv[1])
print("format:", ds.file_format, "| dims:", {k: len(v) for k, v in ds.dimensions.items()})
for k, v in ds.variables.items():
    print(f"var {k}{v.dimensions} {v.dtype} units={getattr(v,'units','-')!r} fill={getattr(v,'_FillValue','-')!r} | {getattr(v,'long_name', getattr(v,'CatDesc','-'))!r}"[:230])
print("n global attrs:", len(ds.ncattrs()))
for a in ds.ncattrs():
    s = repr(ds.getncattr(a))
    if len(sys.argv) > 2 or len(s) < 90: print(f"attr {a} = {s[:160]}")
```

MIGHTI 文件的要点（`dump.py` 输出摘录；另用 `v.ncattrs()` 查了变量属性）：

```text
format: NETCDF4 | dims: {'Epoch': 2219, 'ICON_L22_Altitude': 16, 'N_Flags': 34}
var Epoch('Epoch',) int64 units='-' fill=np.int64(-1) | 'Sample time, average of A and B measurements. Number of msec since Jan 1, 1970.'
var ICON_L22_Altitude('ICON_L22_Altitude',) float64 units='-' fill=np.float64(9.969209968386869e+36) | 'WGS84 altitude of each wind sample'
var ICON_L22_Latitude('Epoch', 'ICON_L22_Altitude') float64 units='-' fill=np.float64(9.969209968386869e+36) | 'WGS84 latitude of each wind sample'
var ICON_L22_Meridional_Wind('Epoch', 'ICON_L22_Altitude') float64 units='-' fill=np.float64(9.969209968386869e+36) | 'Meridional component of the horizontal wind. Positive Northward.'
var ICON_L22_Quality_Flags('Epoch', 'ICON_L22_Altitude', 'N_Flags') int64 units='-' fill=np.int64(-1) | 'Quality flags'
var ICON_L22_Wind_Quality('Epoch', 'ICON_L22_Altitude') float64 units='-' fill=np.float64(9.969209968386869e+36) | 'A quantification of the quality, from 0 (Bad) to 1 (Good)'
var ICON_L22_Zonal_Wind('Epoch', 'ICON_L22_Altitude') float64 units='-' fill=np.float64(9.969209968386869e+36) | 'Zonal component of the horizontal wind. Positive Eastward.'
var ICON_L22_Zonal_Wind_Error('Epoch', 'ICON_L22_Altitude') float64 units='-' fill=np.float64(9.969209968386869e+36) | 'Error in the zonal wind estimate.'
n global attrs: 45
attr Data_Level = 'L2.2'
attr Data_Version_Major = np.uint16(6)
attr File = 'ICON_L2-2_MIGHTI_Vector-Wind-Red_2021-11-04_v06r000.NC'
attr File_Date = 'Mon, 16 Feb 2026, 2026-02-16T07:11:21.745 UTC'
attr Generated_By = 'ICON SDC > ICON UIUC MIGHTI L2.2 Processor v6.03, B. J. Harding'
attr Rules_of_Use = 'Public Data for Scientific Use'
attr Time_Resolution = '30 - 60 seconds'
变量属性：ICON_L22_Zonal_Wind   Units='m/s'  Valid_Range=[-4000, 4000]  _FillValue=9.969209968386869e+36
          ICON_L22_Altitude     Units='km'   Var_Notes='… Altitude is defined using the WGS84 ellipsoid.'
          ICON_L22_Wind_Quality Var_Notes='… Currently, the quality can take values of 0 (Bad), 0.5 (Caution), or 1 (Good).'
```

（`units='-'` 是因为脚本找小写 `units`；ICON 用的是 ISTP 风格的大写 **`Units`**，见坑 6。）

`mighti.py`（原样）：

```python
import netCDF4, numpy as np, datetime as dt
ds = netCDF4.Dataset("icon_l2-2_mighti_vector-wind-red_20211104_v06r000.nc")
g = lambda k: np.ma.filled(ds[k][:].astype(float), np.nan)
alt = g("ICON_L22_Altitude"); u = g("ICON_L22_Zonal_Wind"); v = g("ICON_L22_Meridional_Wind")
q = g("ICON_L22_Wind_Quality"); lat = g("ICON_L22_Latitude"); lst = g("ICON_L22_Local_Solar_Time")
eu = g("ICON_L22_Zonal_Wind_Error"); flags = ds["ICON_L22_Quality_Flags"][:]
ep = ds["ICON_L22_UTC_Time"][:]
print("Epoch x Altitude:", u.shape, "| altitude grid km:", np.round(alt, 1).tolist())
print("time:", ep[0], "->", ep[-1], "| Epoch[0] ms:", int(ds["Epoch"][0]), "=", dt.datetime(1970,1,1) + dt.timedelta(milliseconds=int(ds["Epoch"][0])))
tot = u.size; fin = np.isfinite(u)
print("grid points %d ; finite zonal wind %d (%.1f%%) ; fill/masked %d" % (tot, fin.sum(), 100*fin.mean(), tot - fin.sum()))
vals, cnt = np.unique(q[np.isfinite(q)], return_counts=True)
print("Wind_Quality values:", dict(zip(vals.tolist(), cnt.tolist())), "; NaN quality:", int(np.isnan(q).sum()))
print("finite wind by quality: q=1 %d, q=0.5 %d, q=0 %d" % ((fin & (q == 1)).sum(), (fin & (q == 0.5)).sum(), (fin & (q == 0)).sum()))
notes = ds["ICON_L22_Quality_Flags"].Var_Notes
names = [n for n in notes if n.startswith("* ")]
fl = np.ma.filled(flags, 0)
raised = fl.reshape(-1, fl.shape[-1]).sum(0)
print("N_Flags described:", len(names))
for i in np.argsort(-raised)[:6]:
    print("  flag %2d raised at %6d points : %s" % (i, raised[i], names[i].split(":", 1)[1].strip() if i < len(names) else "?"))
good = fin & (q == 1)
print("lat range (good) %.1f..%.1f ; LST range %.1f..%.1f h" % (np.nanmin(lat[good]), np.nanmax(lat[good]), np.nanmin(lst[good]), np.nanmax(lst[good])))
for a0 in (200, 250):
    j = int(np.argmin(np.abs(alt - a0)))
    m = good[:, j]
    print("alt %.1f km: good samples %d ; zonal median %.1f m/s (p5 %.1f, p95 %.1f) ; merid median %.1f ; median zonal error %.1f m/s" % (
        alt[j], m.sum(), np.median(u[m, j]), *np.percentile(u[m, j], [5, 95]), np.median(v[m, j]), np.median(eu[m, j])))
```

```text
Epoch x Altitude: (2219, 16) | altitude grid km: [160.3, 171.2, 181.9, 192.6, 203.1, 213.5, 223.7, 233.8, 243.8, 253.7, 263.5, 273.1, 282.6, 292.0, 301.3, 310.5]
time: 2021-11-04 00:00:17.039Z -> 2021-11-04 23:59:31.628Z | Epoch[0] ms: 1635984017039 = 2021-11-04 00:00:17.039000
grid points 35504 ; finite zonal wind 19409 (54.7%) ; fill/masked 16095
Wind_Quality values: {0.0: 16095, 0.5: 3840, 1.0: 15569} ; NaN quality: 0
finite wind by quality: q=1 15569, q=0.5 3840, q=0 0
N_Flags described: 34
  flag 17 raised at   6499 points : (From L2.1 B) Not enough valid points in profile
  flag 12 raised at   5702 points : (From L1 B) SNR too low to reliably perform L1 processing
  flag 13 raised at   3724 points : (From L1 B) Proximity to South Atlantic Anomaly
  flag  1 raised at   3460 points : (From L1 A) Proximity to South Atlantic Anomaly
  flag 18 raised at   3374 points : (From L2.1 B) SNR too low after inversion
  flag  5 raised at   3280 points : (From L2.1 A) Not enough valid points in profile
lat range (good) -15.2..40.4 ; LST range 0.0..24.0 h
alt 203.1 km: good samples 962 ; zonal median -34.6 m/s (p5 -81.4, p95 29.9) ; merid median 16.0 ; median zonal error 11.2 m/s
alt 253.7 km: good samples 1130 ; zonal median -39.3 m/s (p5 -92.5, p95 72.5) ; merid median 11.6 ; median zonal error 12.6 m/s
```

要点：

- 网格是 **时间 × 高度**（2219 × 16）：红线 16 层，160.3～310.5 km（WGS84 椭球高），每层约 10 km；每个时间点的经纬度、地方时各自不同（二维变量）。
- **`Wind_Quality`** 只有 0 / 0.5 / 1 三个值：0 = 坏（16095 点，全部已被 `_FillValue` 掩掉）；0.5 = 慎用（3840 点，**风值仍是有限数**）；1 = 好（15569 点）。只用 `Wind_Quality == 1`，否则会混进 3840 个“慎用”值。
- **`Quality_Flags`** 是 时间 × 高度 × 34 的 0/1 数组，解释写在 `Var_Notes` 里：当天最常见的是 “L2.1 B 廓线有效点不足”（6499）、“L1 B 信噪比太低”（5702）、南大西洋异常附近（A 3460 / B 3724）。
- 样例值（q=1）：203 km 纬向风中位数 −34.6 m/s（p5 −81.4，p95 29.9），经向 16.0 m/s，纬向误差中位数 11.2 m/s；254 km 纬向 −39.3 m/s。

### 3.5 读 GOLD NMAX 与 ON2

`dump.py` 输出摘录（NMAX）：

```text
format: NETCDF4 | dims: {'nscans': 36, 'nmask': 4001, 'nlats': 100, 'nlons': 92, 'max_string_len': 50}
var nmax('nscans', 'nlats', 'nlons') float32 units='-' fill='-' | '-'
var nmax_dqi('nscans', 'nlats', 'nlons') int32 units='-' fill='-' | '-'
var latitude('nscans', 'nlats', 'nlons') float32 units='-' fill='-' | '-'
var time_utc('nscans', 'nlons', 'max_string_len') |S1 units='-' fill='-' | '-'
var hemisphere('nscans', 'max_string_len') |S1 units='-' fill='-' | '-'
attr Logical_source = 'GOLD_L2_NMAX'
attr Data_version = '05'
attr date_start = '2024-05-11T20:10:33Z'
attr date_end = '2024-05-12T00:38:21Z'
```

ON2 的差别：`dims: {'nscans': 12, 'nmask': 4001, 'nlats': 52, 'nlons': 46, …}`，`latitude('nlats', 'nlons')` 是**二维**，`time_utc('nscans', 'nlats', 'nlons', 'max_string_len')`，全局属性多了 `latitude_binning = 2`、`longitude_binning = 2`，`dqi = 131072`。

变量属性（`set_auto_mask(False)` 后逐个打印；只保留相关的键，值原样）：

```text
nmax      {'UNITS': 'electrons/cm^3', 'FILLVAL': nan, 'VALIDMIN': 0.0, 'VALIDMAX': 1e+09, 'CATDESC': 'Peak electron density', 'DEPEND_0': 'nscans', 'DEPEND_1': 'nlats', 'DEPEND_2': 'nlons'}
nmax_dqi  {'FILLVAL': -999999999, 'CATDESC': 'NMAX Pixel-level Data Quality Indicator. 0 indicates good data. See documentation for list of other values'}
on2       {'UNITS': ' ', 'FILLVAL': nan, 'VALIDMIN': 0.0, 'VALIDMAX': 5.0, 'CATDESC': 'Column density ratio of atomic oxygen to molecular nitrogen'}
latitude(ON2) {'UNITS': 'degrees', 'FILLVAL': nan, 'DEPEND_0': 'nscans', …}   ← 实际维度是 (nlats, nlons)，属性写错
```

注意：GOLD 用的是大写 **`FILLVAL`**，没有 netCDF 标准的 `_FillValue`，所以 `netCDF4` / `xarray` **不会自动掩膜**；好在数据填充值是 NaN，DQI 的填充值是 −999999999。

`gold.py`（原样）：

```python
import netCDF4, numpy as np, collections
def s(ds, k): return ["".join(x.astype(str)).strip() for x in ds[k][:].filled(b"") ] if np.ma.isMaskedArray(ds[k][:]) else ["".join(x.astype(str)).strip() for x in ds[k][:]]
for fn, var in (("gold_l2_nmax_2024_132_v05_r01_c01.nc", "nmax"), ("gold_l2_on2_2024_132_v04_r02_c01.nc", "on2")):
    ds = netCDF4.Dataset(fn); ds.set_auto_mask(False)
    x = ds[var][:]; dqi = ds[var + "_dqi"][:]; lat = ds["latitude"][:]; lon = ds["longitude"][:]; sza = ds["solar_zenith_angle"][:]
    hem = s(ds, "hemisphere"); ch = s(ds, "channel"); t0 = s(ds, "scan_start_time"); t1 = s(ds, "scan_stop_time")
    print("==", fn, "| shape", x.shape, "| lat/lon shape", lat.shape)
    print("   scans:", len(hem), "hemisphere", dict(collections.Counter(hem)), "channel", dict(collections.Counter(ch)))
    print("   first scan %s -> %s (%s) ; last scan %s -> %s (%s)" % (t0[0], t1[0], hem[0], t0[-1], t1[-1], hem[-1]))
    print("   file-level dqi per scan:", dict(collections.Counter(ds["dqi"][:].tolist())), "| global attr dqi:", ds.dqi)
    fin = np.isfinite(x)
    print("   %s: %d cells, finite %d (%.1f%%), NaN fill %d" % (var, x.size, fin.sum(), 100 * fin.mean(), (~fin).sum()))
    d = collections.Counter(dqi[fin].tolist()); print("   pixel dqi among finite:", dict(d.most_common(6)))
    print("   pixel dqi where NaN:", dict(collections.Counter(dqi[~fin].tolist()).most_common(4)))
    good = fin & (dqi == 0)
    print("   good (finite & dqi==0): %d ; median %.4g p5 %.4g p95 %.4g ; SZA of good %.1f..%.1f deg" % (good.sum(), np.median(x[good]), *np.percentile(x[good], [5, 95]), sza[good].min(), sza[good].max()))
    L = lat if lat.ndim == 3 else np.broadcast_to(lat, x.shape); O = lon if lon.ndim == 3 else np.broadcast_to(lon, x.shape)
    print("   lat of good %.1f..%.1f ; lon of good %.1f..%.1f" % (L[good].min(), L[good].max(), O[good].min(), O[good].max()))
    latc = lat[0] if lat.ndim == 3 else lat
    lonc = lon[0] if lon.ndim == 3 else lon
    print("   grid step (median over scan 0): lat %.2f deg, lon %.2f deg ; lat/lon identical in every scan: %s" % (
        np.nanmedian(np.abs(np.diff(latc, axis=0))), np.nanmedian(np.abs(np.diff(lonc, axis=1))),
        bool(lat.ndim == 2 or np.allclose(np.nan_to_num(lat[0]), np.nan_to_num(lat[-1])))))
    k, i, j = np.argwhere(good)[len(np.argwhere(good)) // 2]
    tt = "".join(ds["time_utc"][k, j].astype(str)) if ds["time_utc"].ndim == 3 else "".join(ds["time_utc"][k, i, j].astype(str))
    print("   example cell scan %d (%s) lat %.2f lon %.2f SZA %.1f time %s : %s = %.4g ; unc_ran %.3g" % (k, hem[k], L[k, i, j], O[k, i, j], sza[k, i, j], tt.strip(), var, x[k, i, j], ds[var + "_unc_ran"][k, i, j]))
```

```text
== gold_l2_nmax_2024_132_v05_r01_c01.nc | shape (36, 100, 92) | lat/lon shape (36, 100, 92)
   scans: 36 hemisphere {'N': 18, 'S': 18} channel {'CHA': 18, 'CHB': 18}
   first scan 2024-05-11T20:10:33Z -> 2024-05-11T20:20:45Z (N) ; last scan 2024-05-12T00:25:09Z -> 2024-05-12T00:38:21Z (S)
   file-level dqi per scan: {0: 36} | global attr dqi: 0
   nmax: 331200 cells, finite 76062 (23.0%), NaN fill 255138
   pixel dqi among finite: {128: 45867, 0: 17755, 65664: 6191, 196736: 3460, 65536: 938, 196608: 879}
   pixel dqi where NaN: {-999999999: 191400, 191: 20970, 160: 10430, 129: 9710}
   good (finite & dqi==0): 17755 ; median 8.379e+05 p5 4.15e+05 p95 1.691e+06 ; SZA of good 105.0..161.3 deg
   lat of good -53.6..51.6 ; lon of good -92.4..13.1
   grid step (median over scan 0): lat 0.76 deg, lon 1.19 deg ; lat/lon identical in every scan: False
   example cell scan 25 (S) lat -18.15 lon -24.25 SZA 148.7 time 2024-05-11T23:21:12.960Z : nmax = 5.996e+05 ; unc_ran 1.57e+05
== gold_l2_on2_2024_132_v04_r02_c01.nc | shape (12, 52, 46) | lat/lon shape (52, 46)
   scans: 12 hemisphere {'N': 6, 'S': 6} channel {'CHA': 12}
   first scan 2024-05-11T08:10:30Z -> 2024-05-11T08:21:31Z (N) ; last scan 2024-05-11T18:22:25Z -> 2024-05-11T18:33:26Z (S)
   file-level dqi per scan: {0: 10, 131072: 2} | global attr dqi: 131072
   on2: 28704 cells, finite 6618 (23.1%), NaN fill 22086
   pixel dqi among finite: {0: 5623, 196608: 581, 65536: 228, 131072: 186}
   pixel dqi where NaN: {-999999999: 18876, 1: 2462, 62: 290, 128: 279}
   good (finite & dqi==0): 5623 ; median 0.8957 p5 0.5518 p95 1.427 ; SZA of good 1.0..79.9 deg
   lat of good -61.6..55.6 ; lon of good -114.1..18.1
   grid step (median over scan 0): lat 2.52 deg, lon 3.01 deg ; lat/lon identical in every scan: True
   example cell scan 7 (S) lat -49.38 lon -56.46 SZA 68.5 time 2024-05-11T14:28:26Z : on2 = 0.7821 ; unc_ran 0.0231
```

要点：

- **扫描几何**：GOLD 在静止轨道上用狭缝南北交替扫描。NMAX 当天 36 次扫描（N / S 各 18，CHA / CHB 各 18），从 20:10 UT 到次日 00:38 UT（夜侧）；ON2 12 次扫描（N / S 各 6，只有 CHA），08:10–18:33 UT（日侧）。
- **网格**：NMAX 的 `latitude/longitude` 是 **扫描 × 纬 × 经** 三维，每次扫描不一样（`identical in every scan: False`），像元是狭缝几何投到地面的格子，中位间距约 0.76° × 1.19°，向圆盘边缘变大；ON2 是固定的**二维**网格（2×2 合并），中位间距约 2.5° × 3.0°。
- **填充值和 DQI**：NMAX 331200 格里只有 76062 格（23.0 %）是有限值；有限值里 **45867 格的 `nmax_dqi` = 128（“LBH contamination present”）**，只有 17755 格 DQI = 0。所以“非 NaN”≠“可用”，必须再筛 DQI == 0。ON2 有限 6618 格，DQI = 0 的 5623 格；位 16 / 17（65536 / 131072）表示 L1C 做过大平场改正。
- **真实值**：NMAX（DQI = 0）中位数 **8.38e5 el/cm³**（p5 4.15e5，p95 1.69e6），SZA 105.0°–161.3°（v05 从 SZA ≥ 105° 开始算，GOLD 2025-03-07 更新说明）；例：23:21:12.960 UT，(−18.15°, −24.25°)，NMAX = **5.996e5 el/cm³**，随机误差 1.57e5。ON2（DQI = 0）中位数 **0.896**；例：14:28:26 UT，(−49.38°, −56.46°)，SZA 68.5°，O/N₂ = **0.782 ± 0.023**。
- ON2 文件级 `dqi` 有 2 次扫描为 131072（“High background”），所以全局属性 `dqi` 也是 131072；这不代表整天都坏，要看逐扫描的 `dqi`。

### 3.6 GOLD SOC 与 ICON SDC

- `https://gold.cs.ucf.edu/data/search/`（200）：网页表单按日期和产品检索，结果是 **tar 包链接**；页面脚本 `mission-api.js` 里的单次上限是 L1C DAY 15 天、LIM / NI1 / OCC / DLM 32 天、L1D 65 天、L2 366 天。页面也写明 SPDF 有同样的数据（含 L1B）。
- SOC 的[版本表](https://gold.cs.ucf.edu/data/current-data-product-versions/)（2026-09-26 抓取）：L1C DAY/LIM/DLM/NI1 v04 r01、OCC v05 r01；L2 TDISK v05 r03（2026-01-21 发布）、TLIMB v05 r01、O2DEN v06 r01、ON2 v04 r02、QEUV v03 r01、NMAX v05 r01（2025-03-07）；**观测日期都到 7/5/26**。
- SOC [数据更新页](https://gold.cs.ucf.edu/data/data-updates/) 2026-06-09 条：2025-10 至 2026-03 期间部分产品有探测器高温增益损失造成的伪影（见发布说明 Rev 5.11、问题表 Rev 2.2）。
- ICON SDC `https://icon.ssl.berkeley.edu/Data` 200；本文只用 SPDF / CDAWeb 路径。

## 4. 时延与版本

| 数据 | 最新数据日 | 上架时间 | 距本次查询（2026-09-26） | 当前版本 |
| --- | --- | --- | --- | --- |
| ICON 全部 L2 | 2022-11-24 / 25（任务结束） | SPDF 时间戳 2025-03 至 2026-04（重处理） | 不再有新数据；**但版本仍在更新** | IVM v08r002 · MIGHTI v06r000/r001 · FUV v07r000/r001 · EUV v03r004 |
| GOLD L2（SPDF） | 2026/186 = 2026-07-05 | 2026-07-20 01:25（SPDF 列表时间） | 约 83 天 | NMAX v05 r01 c02 · ON2 v04 r02 c02 · TDISK v05 r03 c02 · O2DEN v06 r01 c01 |
| GOLD L1C（SPDF） | 2026/187 目录已存在 | — | 约 80 天 | v04 r01（OCC v05） |
| GOLD（SOC） | 7/5/26（版本表） | — | 与 SPDF 一致 | 同上 |
| GOLD（CDAWeb） | NMAX 到 2026-07-06（跨 UTC 午夜的夜侧扫描），其余到 2026-07-05 | — | 与 SPDF 一致 | CDAWeb 只做转发 |
| GUVI（CDAWeb / HAPI `TIMED_EDP_GUVI`） | 2007-10-04 | — | 历史数据 | — |

GOLD 文件名 `_cNN` 是“数据周期”：2024 年文件为 `c01`，2026 年的新文件多为 `c02`，同一天可能先后出现不同 c 号，脚本别写死。

## 5. 输入与输出

| 输入 | 输出 |
| --- | --- |
| SPDF ICON L2 日文件（`icon_<product>_<YYYYMMDD>_vVVrRRR.nc`，0.8–95 MB） | 时间 × 高度（MIGHTI）或 1 s 时间序列（IVM）；质量：`Wind_Quality` / `Quality_Flags`、`DM_Flag` / `RPA_Flag` |
| CDAS REST `…/datasets/<ID>/data/<start>,<stop>/<vars>?format=cdf` | 临时 CDF 子集（本例 4.3 MB）；`orig_data` 返回原文件 URL |
| SPDF GOLD L2 日文件（`gold_l2_<p>_<YYYY>_<DDD>_vVV_rRR_cCC.nc`，0.16–4.7 MB） | 扫描 × 纬 × 经 网格；`<var>_dqi` 像元级、`dqi` 扫描级 |

## 6. 在工作流里接哪一步

1. [B — 不规则体 / 磁暴](./README.md#b--不规则体--磁暴)：GOLD ON2 看磁暴后 O/N₂ 降低（负相暴），NMAX 看夜间赤道异常峰；ICON IVM 垂直漂移（`Ion_Velocity_Meridional`，磁赤道）配合 COSMIC-2 hmF2（[cosmic2-ro](./cosmic2-ro.md)），用 [space-weather-indices](./space-weather-indices.md) 的 Kp / Dst 标注暴时。
2. [A — 一日 TEC](./README.md#a--一日-tec)：GOLD NMAX 夜间峰密度可与 GNSS TEC / 测高仪 foF2 对照（foF2[MHz] ≈ 8.98e-3·√(NMAX[el/cm³])）。
3. 需要一行加载多个 CDAWeb 数据集时换 [pyspedas](./pyspedas.md)。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `hapi/info?id=ICON_L2-7_IVM-A` 或 `GOLD_L2_NMAX` 返回 1406 / HTTP 400 | CDAWeb 的 HAPI 目录（3632 个 ID）里没有 ICON 和 GOLD，虽然 CDAWeb 本身有 | 用 CDAS REST `…/cdasr/1/dataviews/sp_phys/datasets/<ID>/data/…`，或直接下 SPDF 文件 |
| 2 | 在 CDAWeb 找不到 GOLD QEUV / TLIMB / L1C | CDAWeb 只收了 4 个 GOLD L2（ON2 / NMAX / O2DEN / TDISK） | 其余走 SPDF `gold/level2/<p>/` 或 SOC |
| 3 | GOLD 数据停在 7 月初 | SPDF 与 SOC 都只到 2026-07-05，约 83 天时延；2025-10 至 2026-03 还有高温增益伪影 | 近实时需求别指望 GOLD 公开 L2；用前查 SOC 数据更新页和问题表 |
| 4 | ICON 结果和别人对不上 | 任务 2022 年结束，但 L2 在 2025–2026 年仍在重处理（IVM v08、MIGHTI v06、FUV v07） | 论文里写版本号（文件名 `vVVrRRR`）和下载日期；旧脚本里的 v05/v06 文件名要改 |
| 5 | ICON 文件名 `2021-11-04` 大写的写法 404 | SPDF 改成了小写和 `yyyymmdd`，文件内 `File` 属性仍是原名 | 按 SPDF 目录的实际文件名拼 URL |
| 6 | `xarray` 读 ICON / GOLD 没有单位、GOLD 不自动掩膜 | ICON 用 `Units`（大写），GOLD 用 `UNITS` / `FILLVAL`，都不是 CF 的 `units` / `_FillValue`；ICON 有 `_FillValue`（9.97e36），GOLD 没有 | 自己读 `Units`/`UNITS`；GOLD 用 `np.isfinite` + DQI 掩膜 |
| 7 | GOLD NMAX 非 NaN 值里混着坏数据 | 45867 个有限值的 `nmax_dqi` = 128（LBH 污染），数值照样给出 | 只用 `dqi == 0`（或按位检查，允许 65536 / 131072 平场位） |
| 8 | MIGHTI 风里有“慎用”值 | `Wind_Quality = 0.5` 的 3840 点没有被掩膜 | 只用 `Wind_Quality == 1`，看 `Quality_Flags` 找原因 |
| 9 | IVM 漂移大片不可用 | `DM_Flag = 3`（O⁺ 不足，多在夜间低密度）和 1（航天器操作）；速度与密度用的是两套标志 | 速度看 `DM_Flag == 0`，密度 / 温度看 `RPA_Flag == 0`；当天可用速度 49.0 % |
| 10 | CDAS 子集的时间轴长度和数据对不上 | 子集 CDF 同时有 `Epoch_cdf`（86397 条）和 INT8 的 `Epoch`（172796 条，早 1 s） | 用 `Epoch_cdf`；原始 netCDF 里的 `Epoch` 是 1970 起的毫秒 |
| 11 | GOLD 数组维度顺序和文档反了 | 指南写 `[NLONS, NLATS, NSCANS]`（IDL 顺序），Python 读出来是 `(nscans, nlats, nlons)` | 按 `ds[var].dimensions` 取，不按文档 |
| 12 | ON2 的 `latitude` 属性说依赖 `nscans` | 属性 `DEPEND_0 = 'nscans'` 写错，实际是 `(nlats, nlons)` 二维；NMAX 的经纬度才是逐扫描三维 | 以维度为准；NMAX 每次扫描单独取经纬度 |
| 13 | NMAX 数值偏差和“峰值密度”的物理意义 | NMAX 由 135.6 nm 夜辉按 Chapman 层反演，假设标高 50 km、忽略离子–离子复合与多次散射（指南 5.1） | 与 COSMIC-2 / 测高仪比较时当“模型依赖的估计”，看 `nmax_unc_mod` |
| 14 | MIGHTI 高度和 COSMIC-2 高度差一点 | MIGHTI 是 WGS84 椭球高；COSMIC-2 ionPrf 是平均海平面高 | 高精度对比时换算到同一基准 |

## 8. 选型对比

| 需求 | ICON | GOLD | COSMIC-2（[cosmic2-ro](./cosmic2-ro.md)） | GUVI（TIMED） |
| --- | --- | --- | --- | --- |
| 时间范围 | 2019-11～2022-11（已结束） | 2018-10～至今（公开数据滞后约 2.5 个月） | 2019-10～至今（约 5 h 后） | CDAWeb/HAPI `TIMED_EDP_GUVI` 2002-01～2007-10；SPDF `levels_v13/level2b/imaging/edr-{aur,iono,limb}` 2002–2007 |
| 电子密度 | EUV 日间 O⁺ 剖面、FUV 夜间 O⁺、IVM 原位密度 | NMAX 夜间峰密度（二维图） | ionPrf 全天剖面（±40°） | EDP 剖面（2002–2007） |
| 中性成分 / 温度 / 风 | FUV O/N₂、MIGHTI 风与温度 | ON2、TDISK、TLIMB、O2DEN | 无（ionPrf 只给 Ne） | 本轮未核 |
| 漂移 | IVM（原位） | 无 | 无 | 无 |
| 覆盖方式 | LEO 27° 倾角，逐轨 | 静止轨道，固定看美洲–大西洋 | 6 星，低纬全球 | 本轮未核 |
| HAPI | ❌ | ❌ | ❌（CDAAC 不走 HAPI） | ✅（EDP、L1C disk） |
| 最简下载 | SPDF 日文件 / CDAS REST 子集 | SPDF 日文件（L2 ≤ 5 MB） | CDAAC 日包 | CDAWeb HAPI |

背景指数（Kp / Dst / F10.7）用 [space-weather-indices](./space-weather-indices.md)；统一的 CDAWeb 加载器用 [pyspedas](./pyspedas.md)。
