# DMSP SSIES / SSUSI 与 TIMED GUVI 公开数据：SPDF、CDAWeb HAPI、Madrigal、JHU/APL 路径与真实文件读取（2024-05-11）

入口：[SPDF dmsp/](https://spdf.gsfc.nasa.gov/pub/data/dmsp/) · [SPDF timed/guvi/](https://spdf.gsfc.nasa.gov/pub/data/timed/guvi/) · [CDAWeb HAPI](https://cdaweb.gsfc.nasa.gov/hapi/catalog) · [CEDAR Madrigal](https://cedar.openmadrigal.org/)（下载方法见 [madrigal](./madrigal.md)） · [SSUSI（JHU/APL）](https://ssusi.jhuapl.edu/) · [GUVI（JHU/APL）](https://guvitimed.jhuapl.edu/data_products) · 本机验证 **2026-09-26 06:06–06:12 EDT**（匿名，未注册任何账号，未提交任何表单；UTC = EDT + 4 h）

> 岗位：回答“DMSP 的原位等离子体（SSIES-3）、DMSP 远紫外成像（SSUSI）和 TIMED GUVI 不登录去哪拿、哪年有、什么格式、怎么读”。给出 2024-05-11（X5.8 耀斑 + 大磁暴当天）F18 一轨的 SSIES、SSUSI 极光 / 电离层 EDR，以及 GUVI 光谱仪 L1C 的真实读取输出。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E32](../data-access.md#dp-e32) · Madrigal 通用下载 [E3](../data-access.md#dp-e3) / [madrigal](./madrigal.md)
>
> 冲突时：以 SPDF 目录和文件内元数据为准（只代表 2026-09-26 这一次）；“质量 good = 标志 1 或 6”取自 CDF 的变量属性，统计口径（中位数、|磁纬| 范围）是**本文口径**。

## 1. 用途与边界

**做：** 各仪器的公开路径、年份覆盖、单个文件的格式和读取方法；Madrigal 上 DMSP 有哪些文件（只列，下载方法链接 [madrigal](./madrigal.md)，不重复）；CDAWeb HAPI 能拿什么、拿不到什么。

**不做：** Madrigal 的下载参数与 isprint（→ [madrigal](./madrigal.md) §3）；SSJ 粒子、SSM 磁强计的物理分析；SSUSI/GUVI 反演算法；TIMED SEE（太阳 EUV，见 [solar-flare-data](./solar-flare-data.md) 的 LISIRD 路径）。

**结论先说：**

| 数据 | 公开路径（匿名） | 格式 | 覆盖（本次目录） | 本次实测 |
| --- | --- | --- | --- | --- |
| **DMSP SSIES-3 热等离子体** | SPDF `dmsp/dmspfNN/ssies/ssies-3rl/thermal-plasma-cdf/YYYY/`，一轨一个文件 `dmsp-fNN_ssies-3_thermal-plasma_YYYYMMDDhhmm_v01.cdf` | **NASA CDF**（`.cdf`） | F16 2003–2025、F17 2006–2025、F18 2009–2025，**2015–2021 缺**；F18 最后一个文件 2025-08-01 23:23 | F18 01:07 轨：6100 条 1 s，dens good 86.1% |
| 同上（Madrigal） | CEDAR kinst **8100**，每天两套实验：`experiments3/…`（`dms_YYYYMMDD_NNs1/s4/e`）和 `experiments4/…`（`dms_ut_YYYYMMDD_NN.002.hdf5`，带质量标志） | HDF5（Madrigal 格式） | 2024-05-11：6 + 3 个文件 | 只列不下；下载要填 `user_fullname/email/affiliation` 三个字段，见 [madrigal](./madrigal.md) |
| 同上（CDAWeb HAPI） | `cdaweb.gsfc.nasa.gov/hapi/data?id=DMSP-F18_SSIES-3_THERMAL-PLASMA…` | CSV / JSON | 2009-10-22 至 2025-08-01 | 31 个参数（含 Time），**没有质量标志和经纬度**，数值被取整 |
| **DMSP SSUSI** | SPDF `dmsp/dmspfNN/ssusi/data/{edr-aurora,edr-iono,edr-day-limb,edr-night-limb,l1b,sdr-disk,sdr-limb,sdr2-disk,spect-l1b}/YYYY/DDD/` | EDR-aurora **HDF5**；EDR-iono **netCDF3 classic**（同为 `.nc`） | F16 2005–2016、F17 2006–2025、F18 2010–2025、F19 2014–2016 | F18 2024/132：14 轨；北半球功率 378.9 GW、南 1185.6 GW |
| **TIMED GUVI** | SPDF `timed/guvi/levels_v13/level1c/{imaging,spectrograph}/YYYY/DDD/` | HDF5（`.nc`） | **成像模式只到 2007**；光谱仪模式 2002 至 **2026/075** | 2024/132：14 轨 L1C 光谱仪；408×6 盘面辐亮度 |
| GUVI 成像期产品（CDAWeb） | HAPI `TIMED_EDP_GUVI`、`TIMED_L1CDISK_GUVI@0` | CSV | 2002-01 至 2007-10 / 2001-10 至 2007-12 | 只做了 info 查询 |
| JHU/APL 官网 | `ssusi.jhuapl.edu`、`guvitimed.jhuapl.edu/data_fetch_*` | 网页选择年 / 日后下载 | — | 都是 **JavaScript 页面**，curl 只拿到空壳；门槛**未验证**，脚本化用 SPDF |

## 2. 安装

`curl`；Python 3 + `cdflib`（读 NASA CDF）+ `h5py`（读 HDF5）+ `scipy.io`（读 netCDF3 classic，系统 scipy 自带）。本机 `/usr/bin/python3` 没有 netCDF4 / h5py / cdflib，装到临时目录；**用 `--no-deps`**，否则 pip 会往临时目录里再装一份更新的 numpy，和系统 scipy 冲突。

```bash
/usr/bin/python3 -m pip install -q --no-deps --target ./pylib h5py cdflib   # 本机：h5py 3.16.0，cdflib 1.3.14，numpy 用系统 2.2.4
PYTHONPATH=./pylib /usr/bin/python3 -c "import h5py, cdflib, scipy.io, numpy; print(h5py.__version__, cdflib.__version__, numpy.__version__)"
```

## 3. 真命令 + 期望输出

### 3.1 目录覆盖、Madrigal 列表、HAPI、JHU/APL、下载 4 个文件（`dl.sh`）

```bash
#!/usr/bin/env bash
# DMSP SSIES/SSUSI 与 TIMED GUVI 的公开路径：SPDF 目录覆盖、Madrigal 列表、CDAWeb HAPI、JHU/APL；再下 4 个 2024-05-11 真实文件
S=https://spdf.gsfc.nasa.gov/pub/data
yrs(){ curl -s -m 60 "$1" | grep -o 'href="[0-9]\{4\}/"' | cut -c7-10 | tr '\n' ' '; }
echo "## SPDF 年份覆盖"
for f in 16 17 18; do echo "F$f SSIES-3 CDF : $(yrs $S/dmsp/dmspf$f/ssies/ssies-3rl/thermal-plasma-cdf/)"; done
for f in 16 17 18 19; do echo "F$f SSUSI EDR-aurora: $(yrs $S/dmsp/dmspf$f/ssusi/data/edr-aurora/)"; done
echo "F18 SSUSI 产品: $(curl -s $S/dmsp/dmspf18/ssusi/data/ | grep -o 'href="[a-z0-9-]*/"' | cut -d'"' -f2 | tr '\n' ' ')"
echo "GUVI v13 L1C imaging     : $(yrs $S/timed/guvi/levels_v13/level1c/imaging/)"
echo "GUVI v13 L1C spectrograph: $(yrs $S/timed/guvi/levels_v13/level1c/spectrograph/) 最新 DOY: $(curl -s $S/timed/guvi/levels_v13/level1c/spectrograph/2026/ | grep -o 'href="[0-9]*/"' | tail -1)"
echo "F18 SSIES 2024 年文件数: $(curl -s $S/dmsp/dmspf18/ssies/ssies-3rl/thermal-plasma-cdf/2024/ | grep -c '\.cdf"')；2024-05-11: $(curl -s $S/dmsp/dmspf18/ssies/ssies-3rl/thermal-plasma-cdf/2024/ | grep -o 'plasma_20240511[0-9]*' | sort -u | wc -l) 个；2025 最后: $(curl -s $S/dmsp/dmspf18/ssies/ssies-3rl/thermal-plasma-cdf/2025/ | grep -o 'plasma_[0-9]*' | sort -u | tail -1)"
echo "F18 SSUSI EDR-aurora 2024/132: $(curl -s $S/dmsp/dmspf18/ssusi/data/edr-aurora/2024/132/ | grep -c '\.nc"') 个；GUVI L1C spect 2024/132: $(curl -s $S/timed/guvi/levels_v13/level1c/spectrograph/2024/132/ | grep -o 'REV[0-9]*_Av[0-9-]*r[0-9]*\.nc' | sort -u | wc -l) 个"
echo "## Madrigal（CEDAR，kinst 8100）2024-05-11 实验与文件（只列不下）"
M=https://cedar.openmadrigal.org
curl -s -m 90 "$M/getExperimentsService.py?code=8100&startyear=2024&startmonth=5&startday=11&starthour=0&startmin=0&startsec=0&endyear=2024&endmonth=5&endday=11&endhour=23&endmin=59&endsec=59&local=1" | awk -F, '$8==2024 && $9==5 && $10==11 {print $1, $2}' | while read id url; do
  echo "exp $id ${url#*madtoc/}"; curl -s -m 90 "$M/getExperimentFilesService.py?id=$id" | awk -F, '{n=split($1,a,"/"); print "   " a[n] " | " $3}'; done
echo "## CDAWeb HAPI"
H=https://cdaweb.gsfc.nasa.gov/hapi
curl -s $H/catalog | grep -o '"id":"[^"]*\(DMSP\|GUVI\|SSUSI\)[^"]*"' | wc -l | sed 's/^/DMSP|GUVI|SSUSI 数据集个数: /'
for id in DMSP-F18_SSIES-3_THERMAL-PLASMA TIMED_EDP_GUVI TIMED_L1CDISK_GUVI@0; do curl -s "$H/info?id=$id" | grep -o '"st[a-z]*Date":"[^"]*"' | tr '\n' ' ' | sed "s/^/$id: /"; echo; done
curl -s "$H/data?id=DMSP-F18_SSIES-3_THERMAL-PLASMA&time.min=2024-05-11T01:20:00Z&time.max=2024-05-11T01:20:03Z&parameters=temp,dens"
curl -s "$H/data?id=DMSP-F18_SSIES-3_THERMAL-PLASMA&time.min=2024-05-11T01:20:00Z&time.max=2024-05-11T01:20:03Z&parameters=dens,temp" | grep -o '"message": "[^"]*"'
echo "## JHU/APL"
for u in https://ssusi.jhuapl.edu/ https://guvitimed.jhuapl.edu/data_products https://guvitimed.jhuapl.edu/data_fetch_l3_on2_netcdf_new; do echo "$(curl -s -o /tmp/j.html -m 30 -w '%{http_code} %{size_download} B' $u) $u :: $(sed 's/<[^>]*>/ /g' /tmp/j.html | tr -s ' \n' ' ' | grep -o 'You need to enable JavaScript\|select the year and day then press display' | head -1)"; done; rm -f /tmp/j.html
echo "## 下载 4 个文件"
g(){ curl -s -O -w "%{http_code} %{size_download} B  %{filename_effective}\n" "$1"; }
g $S/dmsp/dmspf18/ssies/ssies-3rl/thermal-plasma-cdf/2024/dmsp-f18_ssies-3_thermal-plasma_202405110107_v01.cdf
g $S/dmsp/dmspf18/ssusi/data/edr-aurora/2024/132/dmspf18_ssusi_edr-aurora_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc
g $S/dmsp/dmspf18/ssusi/data/edr-iono/2024/132/dmspf18_ssusi_edr-iono_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc
g $S/timed/guvi/levels_v13/level1c/spectrograph/2024/132/TIMED_GUVI_L1C-2-disk-SPECT_2024132002517-2024132020153_REV121644_Av13-01r001.nc
```

实测输出（06:11 EDT，空目录，约 47 s）：

```text
## SPDF 年份覆盖
F16 SSIES-3 CDF : 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2022 2023 2024 2025 
F17 SSIES-3 CDF : 2006 2007 2008 2009 2012 2013 2014 2022 2023 2024 2025 
F18 SSIES-3 CDF : 2009 2010 2011 2012 2013 2014 2022 2023 2024 2025 
F16 SSUSI EDR-aurora: 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 
F17 SSUSI EDR-aurora: 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 
F18 SSUSI EDR-aurora: 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 
F19 SSUSI EDR-aurora: 2014 2015 2016 
F18 SSUSI 产品: edr-aurora/ edr-day-limb/ edr-iono/ edr-night-limb/ l1b/ sdr-disk/ sdr-limb/ sdr2-disk/ spect-l1b/ 
GUVI v13 L1C imaging     : 2002 2003 2004 2005 2006 2007 
GUVI v13 L1C spectrograph: 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026  最新 DOY: href="075/"
F18 SSIES 2024 年文件数: 5408；2024-05-11: 14 个；2025 最后: plasma_202508012323
F18 SSUSI EDR-aurora 2024/132: 14 个；GUVI L1C spect 2024/132: 14 个
## Madrigal（CEDAR，kinst 8100）2024-05-11 实验与文件（只列不下）
exp 100351417 experiments3/2024/dms/11may24
   dms_20240511_16s1.001.hdf5 | F16 1 sec values (ion drift / magnetometer / electron density)
   dms_20240511_17s1.001.hdf5 | F17 1 sec values (ion drift / magnetometer / electron density)
   dms_20240511_18s1.001.hdf5 | F18 1 sec values (ion drift / magnetometer / electron density)
   dms_20240511_16s4.001.hdf5 | F16 4 sec values (plasma temp / O+ fract / vehicle pot)
   dms_20240511_17s4.001.hdf5 | F17 4 sec values (plasma temp / O+ fract / vehicle pot)
   dms_20240511_18e.001.hdf5 | F18 flux/energy values
exp 100240270 experiments4/2024/dms/11may24
   dms_ut_20240511_16.002.hdf5 | F16 UT SSIES-3 DMSP with quality flags
   dms_ut_20240511_17.002.hdf5 | F17 UT SSIES-3 DMSP with quality flags
   dms_ut_20240511_18.002.hdf5 | F18 UT SSIES-3 DMSP with quality flags
## CDAWeb HAPI
DMSP|GUVI|SSUSI 数据集个数: 20
DMSP-F18_SSIES-3_THERMAL-PLASMA: "startDate":"2009-10-22T16:31:30Z" "stopDate":"2025-08-01T23:23:56Z" 
TIMED_EDP_GUVI: "startDate":"2002-01-07T05:53:28Z" "stopDate":"2007-10-04T23:20:59Z" 
TIMED_L1CDISK_GUVI@0: "startDate":"2001-10-18T06:10:25Z" "stopDate":"2007-12-10T22:52:41Z" 
2024-05-11T01:20:00.000Z,2562,142273
2024-05-11T01:20:01.000Z,2508,139595
2024-05-11T01:20:02.000Z,2568,141609
"message": "HAPI error 1411: Parameter out of order"
## JHU/APL
200 1548 B https://ssusi.jhuapl.edu/ :: You need to enable JavaScript
200 30488 B https://guvitimed.jhuapl.edu/data_products :: You need to enable JavaScript
200 20664 B https://guvitimed.jhuapl.edu/data_fetch_l3_on2_netcdf_new :: You need to enable JavaScript
## 下载 4 个文件
200 665748 B  dmsp-f18_ssies-3_thermal-plasma_202405110107_v01.cdf
200 3375676 B  dmspf18_ssusi_edr-aurora_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc
200 889276 B  dmspf18_ssusi_edr-iono_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc
200 524755 B  TIMED_GUVI_L1C-2-disk-SPECT_2024132002517-2024132020153_REV121644_Av13-01r001.nc
```

读法：

- SSIES CDF 在 SPDF 上 **2015–2021 年整段缺**（三颗星都缺）。这几年要去 Madrigal 找（本文没有逐年核对 Madrigal 在这几年的覆盖）。
- HAPI 同一请求把参数顺序从 `temp,dens` 换成 `dens,temp` 就报 `1411 Parameter out of order`：参数必须按 `info` 里的顺序写。
- HAPI 返回 `2562,142273`，文件里是 2561.758 K、142273.1 cm⁻³（见 3.2 的交叉核对）：**HAPI CSV 把数值取整了**，而且不提供 `densqual` 等质量标志和 `glat/glon`。

### 3.2 读 4 个文件（`read.py`）

```python
# 读 4 个真实文件：SSIES-3（NASA CDF）、SSUSI EDR-aurora（HDF5）、SSUSI EDR-iono（netCDF3 classic）、GUVI L1C 光谱仪（HDF5）
import glob, numpy as np, cdflib, h5py, scipy.io, datetime as dt
def magic(fn): return {b'\xcd\xf3\x00\x01': 'NASA CDF v3', b'\x89HDF': 'HDF5 (netCDF4)', b'CDF\x01': 'netCDF3 classic'}.get(open(fn, 'rb').read(4), '?')
for fn in sorted(glob.glob('*.cdf') + glob.glob('*.nc')): print(f'{magic(fn):16s} {fn}')

print('\n== DMSP F18 SSIES-3（SPDF CDF，一轨一个文件）')
c = cdflib.CDF(glob.glob('dmsp-f18_ssies-3*.cdf')[0])
t = cdflib.cdfepoch.to_datetime(c.varget('Epoch')); dtv = np.diff(t).astype('timedelta64[ms]').astype(float) / 1e3
print(f'记录 {len(t)}，{str(t[0])[:19]} → {str(t[-1])[:19]} UTC，步长中位 {np.median(dtv):.0f} s')
for v, q in (('dens', 'densqual'), ('temp', 'tempqual'), ('vy', 'vyqual')):
    x, fl = c.varget(v), c.varget(q); good = np.isin(fl, (1, 6)) & (x > -9e5)
    print(f'{v:5s} 质量 good(1/6) {good.mean() * 100:5.1f}%  good 中位 {np.median(x[good]):10.1f} {c.varattsget(v)["UNITS"]}  范围 {x[good].min():.3g} … {x[good].max():.3g}')
alt, glat, mlat = c.varget('alt'), c.varget('glat'), c.varget('mlat')
print(f'高度 {alt.min():.0f}–{alt.max():.0f} km；地理纬度 {glat.min():.1f}…{glat.max():.1f}；磁纬 {mlat.min():.1f}…{mlat.max():.1f}')

print('\n== DMSP F18 SSUSI EDR-aurora（HDF5，一轨一个文件）')
a = h5py.File(glob.glob('*edr-aurora*.nc')[0])
print(f'YEAR/DOY {a["YEAR"][()]:.0f}/{a["DOY"][()]:.0f}  扫描 {a["LATITUDE"].shape[0]}  网格 {a["UT_N"].shape}')
for h in ('NORTH', 'SOUTH'):
    b = a[f'{h}_GEOMAGNETIC_LATITUDE'][:]; m = a[f'MODEL_{h}_GEOMAGNETIC_LATITUDE'][:]
    print(f'{h}: 有数据={a[f"{h}_DATA"][()]}  半球功率 {a[f"HEMISPHERE_POWER_{h}"][()]:.1f} GW  赤道向边界点 {b.size}（|磁纬| {np.abs(b).min():.1f}–{np.abs(b).max():.1f}°）  模型边界最低 |磁纬| {np.abs(m).min():.1f}°')

print('\n== DMSP F18 SSUSI EDR-iono（netCDF3 classic → scipy.io）')
f = scipy.io.netcdf_file(glob.glob('*edr-iono*.nc')[0], 'r', mmap=False)
nm, hm = f.variables['nmf2'][:], f.variables['hmf2'][:]; ok = (nm > 0) & (hm > 0)
print(f'{f.data_product_type.decode()}：{nm.size} 个沿轨网格，NmF2>0 的 {ok.sum()} 个；NmF2 中位 {np.median(nm[ok]):.3g} cm⁻³，hmF2 中位 {np.median(hm[ok]):.0f} km；ed_cube {f.variables["ed_cube"].shape}；bubble 表 {f.variables["bubble"].shape[0]} 行')

print('\n== TIMED GUVI L1C 光谱仪（HDF5）')
g = h5py.File(glob.glob('TIMED_GUVI*.nc')[0])
at = {k: (v.decode() if isinstance(v, bytes) else v) for k, v in g.attrs.items()}
print(f'{at["DATA_PRODUCT_TYPE"]} / {at["SCAN_TYPE"]} / {at["SCAN_MODE"]}，版本 {at["DATA_PRODUCT_VERSION"]}-{at["DATA_PRODUCT_REVISION"]}')
x = g['DISK_INTENSITY_DAY'][:]; td = g['TIME_DAY'][:]
print(f'DISK_INTENSITY_DAY {x.shape}（nAlongDay × nchan），TIME_DAY {td.min():.0f}–{td.max():.0f} s（当日秒）；6 通道正值中位（R）:', np.round(np.nanmedian(np.where(x > 0, x, np.nan), axis=0), 1))
```

实测输出：

```text
HDF5 (netCDF4)   TIMED_GUVI_L1C-2-disk-SPECT_2024132002517-2024132020153_REV121644_Av13-01r001.nc
NASA CDF v3      dmsp-f18_ssies-3_thermal-plasma_202405110107_v01.cdf
HDF5 (netCDF4)   dmspf18_ssusi_edr-aurora_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc
netCDF3 classic  dmspf18_ssusi_edr-iono_2024132T012000-2024132T030151-REV075111_vA8.2.0r000.nc

== DMSP F18 SSIES-3（SPDF CDF，一轨一个文件）
记录 6100，2024-05-11T01:07:27 → 2024-05-11T02:49:20 UTC，步长中位 1 s
dens  质量 good(1/6)  86.1%  good 中位    68078.1 Ions/cc  范围 6.99e+03 … 1.07e+06
temp  质量 good(1/6)  68.7%  good 中位     2402.4 deg k  范围 504 … 6.94e+03
vy    质量 good(1/6)  84.9%  good 中位     -145.7 m/s  范围 -2e+03 … 1.99e+03
高度 848–867 km；地理纬度 -81.2…81.2；磁纬 -66.0…75.5

== DMSP F18 SSUSI EDR-aurora（HDF5，一轨一个文件）
YEAR/DOY 2024/132  扫描 278  网格 (363, 363)
NORTH: 有数据=1  半球功率 378.9 GW  赤道向边界点 170（|磁纬| 50.2–73.6°）  模型边界最低 |磁纬| 61.8°
SOUTH: 有数据=1  半球功率 1185.6 GW  赤道向边界点 49（|磁纬| 63.4–68.5°）  模型边界最低 |磁纬| 61.9°

== DMSP F18 SSUSI EDR-iono（netCDF3 classic → scipy.io）
3D Ionosphere EDR：18 个沿轨网格，NmF2>0 的 18 个；NmF2 中位 1.75e+06 cm⁻³，hmF2 中位 423 km；ed_cube (18, 24, 30)；bubble 表 22 行

== TIMED GUVI L1C 光谱仪（HDF5）
SDR binned spectrograph data / SPECTROGRAPH / STARE，版本 0110-001
DISK_INTENSITY_DAY (408, 6)（nAlongDay × nchan），TIME_DAY 1523–7306 s（当日秒）；6 通道正值中位（R）: [7323.  6840.7  846.5  854.7  922.   260.2]
```

交叉核对（同一 CDF，01:20:00–01:20:04 UTC 的原始值）：`dens` = 142273.1 / 139595.1 / 141609.1 / 137311.1 / 140763.1 cm⁻³，`densqual` 全为 1，`temp` = 2561.758 / 2508.094 / 2567.932 / 2482.348 / 2567.033 K。和 HAPI 的前 3 行对得上，只是 HAPI 取了整。

读法：

- **SSIES-3**：一轨约 101 min（01:07:27–02:49:20），1 s 一条；F18 高度 848–867 km。离子密度 `dens` 的 good 比例 86%，离子温度 `temp` 只有 69%：**用之前先按 `*qual` 过滤**（1、6 = good，2、7 = fair，其他 = warn，取自 CDF 变量属性）。
- **SSUSI EDR-aurora**：南半球功率 1185.6 GW、北半球 378.9 GW（大磁暴期间）；北半球观测到的极光边界最低到 |磁纬| 50.2°，而文件里的模型边界最低只到 61.8°。**暴时别拿模型边界代替观测边界**。
- **SSUSI EDR-iono** 是 netCDF3 classic，h5py 打不开，要用 `scipy.io.netcdf_file`；18 个沿轨网格的 NmF2 中位 1.75e6 cm⁻³、hmF2 中位 423 km。
- **GUVI L1C 光谱仪**：`DISK_INTENSITY_DAY` 是 408×6，但 `nchan` 维只有序号 0–5，**文件里没有写每个通道是哪条谱线**，要看 JHU/APL 的 SDR 格式文档（[GUVI_Spectrographic_SDR_Format_v1.1.3.doc](https://guvitimed.jhuapl.edu/sites/default/files/data/documents/GUVI_Spectrographic_SDR_Format_v1.1.3.doc)，本文未下载核对）。时间 `TIME_DAY` 是当日秒，`TIME_EPOCH_DAY` 是毫秒。

## 4. 输入 / 输出

| 文件 | 时间变量 | 关键变量 | 填充 / 质量 |
| --- | --- | --- | --- |
| SSIES-3 CDF | `Epoch`（CDF_EPOCH，用 `cdflib.cdfepoch.to_datetime`） | `dens`（ions/cc）、`temp`、`te`、`vx/vy/vz`（m/s）、`fraco`、`glat/glon/mlat/mlt/alt/sza` | 填充 −999999；`densqual` 等 1、6 = good |
| SSUSI EDR-aurora | `YEAR`、`DOY`、`TIME`（扫描平均时刻）、`UT_N/UT_S` 网格 | `HEMISPHERE_POWER_NORTH/SOUTH`（GW）、`NORTH_/SOUTH_GEOMAGNETIC_LATITUDE`（边界）、`MODEL_*`、363×363 网格 | `NORTH_DATA` 0/1；`DATA_QUALITY_GLOBAL` |
| SSUSI EDR-iono | `time`、`grid_time` | `nmf2`、`hmf2`、`ed_cube`（18×24×30）、`bubble` | `dqi` 位掩码 |
| GUVI L1C 光谱仪 | `TIME_DAY`（当日秒）、`TIME_EPOCH_DAY`（ms） | `DISK_INTENSITY_DAY/NIGHT`（R，×6 通道）、`PIERCEPOINT_*` | 负值 / 0 当无效（本文取正值） |

## 5. 参数（路径拼装）

| 项 | 取值 | 说明 |
| --- | --- | --- |
| `dmspfNN` | f16、f17、f18（SSIES + SSUSI）、f19（只有 SSUSI 2014–2016） | 目录里还有 f06–f15（SSJ 等） |
| SSIES 文件时间戳 | 轨道起点 `YYYYMMDDhhmm` | 文件名以 20240511 开头的有 14 个 |
| SSUSI 文件名 | `dmspfNN_ssusi_<产品>_YYYYDDDThhmmss-YYYYDDDThhmmss-REVnnnnnn_vA8.2.0r000.nc` | 起止时刻 + 轨道号 |
| GUVI 文件名 | `TIMED_GUVI_L1C-2-disk-SPECT_YYYYDDDhhmmss-YYYYDDDhhmmss_REVnnnnnn_Av13-01r001.nc` | `levels_v13` = 数据版本 13 |
| HAPI | `id`、`time.min`、`time.max`、`parameters`（按 info 顺序） | `format=json` 可选 |
| Madrigal | kinst 8100 | 服务端 CGI 与下载见 [madrigal](./madrigal.md) |

## 6. 接到哪一步

- 耀斑 / 磁暴期间的顶部电离层密度、极光边界，和 GNSS TEC 对照：TEC 观测见 [cors-networks](./cors-networks.md)、[gnss-obs-mirrors](./gnss-obs-mirrors.md)；驱动见 [solar-flare-data](./solar-flare-data.md)（同一天 01:10–01:39 UT 的 X5.8 正好落在本文 F18 01:07 这一轨里）。
- 地基雷达 / 全球 TEC 图同在 Madrigal：[madrigal](./madrigal.md)、data-access [E3](../data-access.md#dp-e3)。
- 地磁指数：[geomagindices](./geomagindices.md)。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 同样是 `.nc`，h5py 打开 EDR-iono 报错 | SSUSI EDR-aurora 是 HDF5，EDR-iono 是 netCDF3 classic（文件头 `CDF\x01`） | 先看前 4 字节；classic 用 `scipy.io.netcdf_file` |
| 2 | 把 SSIES 的 `.cdf` 当 netCDF 读失败 | 这是 NASA CDF（头 `\xcd\xf3\x00\x01`），不是 netCDF | 用 `cdflib` |
| 3 | 2015–2021 年 SSIES 目录不存在 | SPDF 上三颗星这段都没有 | 这几年去 Madrigal kinst 8100 找（覆盖未逐年核对） |
| 4 | 想找 2008 年以后的 GUVI 成像数据 | SPDF 上 GUVI 成像 L1C 只到 2007，之后只有光谱仪模式 | 2008 年后用光谱仪 L1C，或改用 SSUSI |
| 5 | HAPI 报 `1411 Parameter out of order` | `parameters` 必须按 info 里的顺序 | 先 GET `info`，按顺序拼 |
| 6 | HAPI 数值和文件对不上（小数没了） | HAPI CSV 输出取整（2561.758 → 2562） | 要全精度、要质量标志和位置，就下载 CDF |
| 7 | HAPI 里找不到 `densqual`、`glat` | HAPI 只暴露 31 个参数（含 Time），不含质量和支持变量 | 同上 |
| 8 | 离子温度一半不能用 | `tempqual` good 只有 69%（本轨） | 每个变量用自己的 `*qual` 过滤 |
| 9 | 暴时极光边界比模型低 10° 以上 | 模型边界是统计模型；本轨观测 50.2° vs 模型 61.8° | 用观测边界，模型只做缺测填补 |
| 10 | GUVI 6 个通道不知道是什么 | 文件的 `nchan` 维只有序号 | 查 JHU/APL SDR 格式文档，别凭印象对应 |
| 11 | curl JHU/APL 下载页拿不到文件链接 | 页面由 JavaScript 生成 | 脚本化走 SPDF（同一批文件）；官网门槛本文未验证 |
| 12 | Madrigal 下载要填姓名、邮箱、单位 | Madrigal 下载接口要求这三个字段（服务端只记录） | 按 [madrigal](./madrigal.md) 填真实信息；本文只列文件不下载 |
| 13 | Madrigal 同一天有两个 DMSP 实验 | `experiments3`（1 s / 4 s / 粒子）和 `experiments4`（SSIES-3 带质量标志）两套 | 要质量标志用 `dms_ut_…002.hdf5` |
| 14 | pip 装 h5py 后 scipy 报 numpy 版本冲突 | `--target` 目录里被装了一份新的 numpy | `--no-deps`，用系统 numpy |

## 8. 选型

- **原位离子密度 / 温度 / 漂移**：SPDF SSIES-3 CDF（全精度 + 质量标志）；2015–2021 年去 Madrigal；只要快速看几分钟的曲线用 CDAWeb HAPI。
- **极光边界、半球功率、夜侧 NmF2/hmF2**：SPDF SSUSI EDR。
- **热层 O/N₂、日侧远紫外**：GUVI 光谱仪 L1C（2002 至今）或 SSUSI；GUVI 成像产品只到 2007。
- **和地基雷达、TEC 图一起分析**：Madrigal（[madrigal](./madrigal.md)）。
