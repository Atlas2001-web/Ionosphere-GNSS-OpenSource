# COSMIC-2 电离层掩星数据直连（UCAR CDAAC：ionPrf 电子密度剖面 · podTc2 链路 TEC）· 下载与读取 操作手册

入口：[CDAAC 公开数据树](https://data.cosmic.ucar.edu/gnss-ro/cosmic2/) · [ionPrf 格式说明](https://cdaac-www.cosmic.ucar.edu/cdaac/cgi_bin/fileFormats.cgi?type=ionPrf) · [podTc2 格式说明](https://cdaac-www.cosmic.ucar.edu/cdaac/cgi_bin/fileFormats.cgi?type=podTc2) · [空间天气暂定发布说明 PDF](https://data.cosmic.ucar.edu/gnss-ro/cosmic2/provisional/spaceWeather/F7C2_SpWx_Provisional_Data_Release_1.pdf) · 本机验证 **2026-09-26 04:08–04:35 EDT**。样例日是 **2024 年第 132 天（2024-05-11，Gannon 超级磁暴主相）**：下载了 ionPrf 整个日包（27.9 MB），podTc2 只**流式取出日包的前 3 个文件**（从服务器实际读取 163,840 B，没有下载 919 MB 的整包）。读取用临时 venv 里的 `netCDF4` + `numpy`，工作目录 `/workspace/c2work` 用完即删。

> 岗位：直接从 CDAAC 的 HTTPS 树拿 **COSMIC-2（FORMOSAT-7）电离层产品**：`ionPrf`（每次掩星一条 Ne 剖面）和 `podTc2`（每条 LEO→GNSS 链路的 TEC、S4、仰角、两端 ECEF 坐标），并把 NmF2/hmF2、日覆盖、质量筛选做对。用 pysat 统一加载 COSMIC-1 ionPrf 见 [pysatcdaac](./pysatcdaac.md)；AWS `gnss-ro-data` 的中性大气产品查询见 [awsgnssroutils](./awsgnssroutils.md)；JPL 大气 L2 见 [cosmic-crunch](./cosmic-crunch.md)；掩星几何仿真见 [gmat](./gmat.md)。本文不重复这几篇。  
> 门槛总表：[data-access 决策表](../data-access.md#电离层与地磁门户决策表) · [E19 CDAAC COSMIC-2 电离层](../data-access.md#dp-e19) · [E20 AWS gnss-ro-data 镜像（无电离层）](../data-access.md#dp-e20) · 菜谱 [掩星 RO（CDAAC / AWS）](../data-access.md#掩星-rocdaac--aws)。  
> 冲突时：**CDAAC 格式说明页 / 发布说明 PDF / 文件里的 attribute > 本文**；目录名（`provisional` / `nrt` / `rapid` / `postProc`）会随发布调整，重跑前先列一次目录。

## 1. 它解决什么，边界在哪

| 产品 | 层级 | 内容 | COSMIC-2 实际所在目录（2026-09-26 实测） | 日包大小（实测） |
| --- | --- | --- | --- | --- |
| **ionPrf** | Level 2 | 一次掩星一条 Abel 反演电子密度剖面 `ELEC_dens`（el/cm³）+ 校准 TEC，全局属性里有 `edmax`/`edmaxalt` 等峰值信息 | **只在** `provisional/spaceWeather/level2/YYYY/DDD/ionPrf_prov1_YYYY_DDD.tar.gz`（2019/274 起到昨天）；`nrt/level2/…/ionPrf_nrt_…` → **404**；`postProc/level2/` 没有 ionPrf | 2020-001：13 MB；2024-132：27 MB（3608 个文件）；2026-268：19 MB |
| **podTc2** | Level 1b | 一条 POD / 掩星天线链路一个文件：1 Hz（有缺口）`TEC`、`S4`、`elevation`、`occheight`、LEO 和 GNSS 的 ECEF 坐标 | `nrt/level1b/…/podTc2_nrt_…`（年目录 2019 起，时延约 5 h）· `rapid/level1b/…/podTc2_rapid_…`（年目录 2022 起，时延约 1.7 天）· `postProc/level1b/2020/DDD/`（只有 2020，335 天）· `provisional/spaceWeather/level1b/`（只有 2019–2021、2023 的部分天） | nrt 2024-132：919 MB；nrt 2026-268：640 MB；rapid 2026-266：493 MB；postProc 2020-032：485 MB |

**不覆盖**：中性大气产品（`atmPrf`/`wetPf2`/`bfrPrf`，在 `nrt/level2/`，另见 [awsgnssroutils](./awsgnssroutils.md)）；IVM 离子速度计（`ivmL2m` 等，不是掩星）；闪烁产品 `scnLv2`/`scnPhs`（`rapid/` 下，本轮只列了目录）；把 podTc2 自己反演成 Ne。

## 2. 安装

```bash
python3 -m venv venv && venv/bin/pip -q install netCDF4 numpy   # 本机 venv 约 119 MB，用完删
curl --version | head -1
```

文件是 **netCDF-3 classic**（文件头是 `CDF\001`，本机 `od -c` 验证），所以 `scipy.io.netcdf_file` 或 `xarray` 也能读；用 `h5py` 读不了。

## 3. 真实命令与输出

### 3.1 目录树：按 级别 / 任务 / 产品 / 年 / 年积日 走

```bash
B=https://data.cosmic.ucar.edu/gnss-ro/cosmic2
curl -s "$B/" ; curl -s "$B/nrt/level2/2024/132/" ; curl -s "$B/provisional/spaceWeather/level2/2024/132/"   # nginx autoindex
```

实测结果整理（HTTP 码是 `curl -sI -L -w '%{http_code}'` 的返回）：

```text
gnss-ro/cosmic2/                          200  nrt/ postProc/ provisional/ rapid/ tools/     (repro/ → 404)
  nrt/level{0,1a,1b,2,3}/YYYY/DDD/          200  level1b/2024/132: conPhs_nrt_…(4G) leoOrb_nrt_…(2M) podTc2_nrt_2024_132.tar.gz(919M)
                                                 level2/2024/132: atmPrf avnPrf bfrPrf echPrf wetPf2 + sktPlt/ spectr/   ← 没有 ionPrf
  rapid/level{1b,2,3}/YYYY/DDD/ (2022–)     200  level1b: podTc2_rapid_…(682M) scn1c2 scnPhs ; level2: ivmL2m scnLv2
  postProc/level1b/2020/DDD/                200  podTc2_postProc_2020_DDD.tar.gz（只有 2020）
  postProc/level2/{2019..2022}/DDD/         200  只有 ivmL2m / ivmL2b / ivmLv2（IVM，不是掩星）；postProc/level2/2024/ → 404
  provisional/spaceWeather/level2/YYYY/DDD/ 200  ionPrf_prov1_YYYY_DDD.tar.gz（2019/274 → 最新）
  provisional/spaceWeather/level1b/         200  只有 2019/ 2020/ 2021/ 2023/；…/level1b/2024/ → 404
对照 COSMIC-1：gnss-ro/cosmic1/repro2013/level2/2013/001/ → 200（repro 目录只有 COSMIC-1 有）
```

路径模板：`https://data.cosmic.ucar.edu/gnss-ro/<mission>/<stream>/<level>/<YYYY>/<DDD>/<product>_<stream>_<YYYY>_<DDD>.tar.gz`；
`<stream>` 在文件名里会变短：`provisional/spaceWeather` → `prov1`（暂定发布第 1 版）、`postProc` 在 2019 年的 IVM 包里写成 `pp`。
包里的单文件名分别是 `ionPrf_C2E1.2024.132.00.07.G11_0001.0001_nc`（`C2E1`…`C2E6` = 6 颗卫星，`G`/`R` = GPS/GLONASS）和 `podTc2_C2E1.2024.132.00.01.0017.G27.02_0001.0001_nc`（`0017` = 弧段分钟数，`02` = 天线号）。

**日包还是单文件**：CDAAC 树上**只有日包 `.tar.gz`**，没有逐个文件的 URL；AWS 镜像是逐文件的，但**没有 ionPrf/podTc2**（见 3.2）。服务器返回 `accept-ranges: bytes`，但 gzip 流不能跳读，所以要“只拿几个文件”就用下面 3.4 的流式读取：读到需要的成员就断开。

**时延**（`curl -sI` 的 `last-modified`，GMT 换成 EDT）：

```text
ionPrf_prov1_2026_268.tar.gz  19,435,909 B   last-modified 2026-09-26 04:52:41 GMT = 00:52 EDT   → 当天(09-25)结束后约 5 h
podTc2_nrt_2026_268.tar.gz   671,126,813 B   last-modified 2026-09-26 04:52:41 GMT                → 同上
podTc2_rapid_2026_266.tar.gz 517,247,736 B   last-modified 2026-09-25 17:12:53 GMT = 13:12 EDT   → 09-23 结束后约 1.7 天
```

单文件内的 `creation_time` 也说明了 nrt 的处理节奏：2024-132 第一条 ionPrf（00:05 UT 的掩星）写的是 `11-MAY-24 00:56`，第一条 podTc2 写的是 `11-MAY-24 00:27`。

### 3.2 AWS `gnss-ro-data` 镜像：有 COSMIC-2，但只有中性大气

```bash
S="https://gnss-ro-data.s3.amazonaws.com/?list-type=2&delimiter=/"
curl -s "$S&prefix="                               # → contributed/ dynamo/ index.html（untarred/ 为空）
curl -s "$S&prefix=contributed/v1.1/ucar/cosmic2/"  # → atmosphericRetrieval/ calibratedPhase/ refractivityRetrieval/
curl -s "$S&prefix=contributed/v2.0/"               # → gnssro_cosmic2_ucar_{l1b,l2a,l2b}/ …（v2.0 按 年/月/日 分目录）
```

```text
contributed/v1.1/ucar/cosmic2/atmosphericRetrieval/2019/10/01/atmosphericRetrieval_cosmic2_ucar_0001.0001_cosmic2e1-G01-201910010125.nc
contributed/v2.0/gnssro_cosmic2_ucar_l1b/2019/10/02/gnssro_cosmic2_ucar_l1b_0001.0001_cosmic2e1-G01-201910020023.nc4   Size 1979798
```

对照表：

| | CDAAC `data.cosmic.ucar.edu` | AWS `gnss-ro-data` |
| --- | --- | --- |
| 目录粒度 | `<stream>/<level>/YYYY/DDD/` | v1.1：`contributed/v1.1/ucar/cosmic2/<type>/YYYY/MM/DD/`；v2.0：`contributed/v2.0/gnssro_cosmic2_ucar_{l1b,l2a,l2b}/YYYY/MM/DD/` |
| 打包 | 日包 `.tar.gz` | 每次掩星一个 `.nc` / `.nc4` |
| ionPrf / podTc2 | ✅（见 3.1） | ❌（只有 calibratedPhase / refractivityRetrieval / atmosphericRetrieval 三类） |
| 登录 | 无 | 无（S3 ListObjectsV2 匿名） |

### 3.3 需要登录吗：实测 HTTP 码

```bash
for u in …; do curl -s -o /dev/null -I -L -m 30 -w '%{http_code} %{url_effective}\n' "$u"; done
```

```text
200 …/cosmic2/provisional/spaceWeather/level2/2024/132/ionPrf_prov1_2024_132.tar.gz
200 …/cosmic2/nrt/level1b/2024/132/podTc2_nrt_2024_132.tar.gz
200 …/cosmic2/rapid/level1b/2024/132/podTc2_rapid_2024_132.tar.gz
200 …/cosmic2/nrt/level0/            200 …/cosmic2/nrt/level1a/        200 …/cosmic2/nrt/level0/2024/132/
404 …/cosmic2/repro/                 404 …/cosmic2/postProc/level2/2024/   404 …/cosmic2/nrt/level2/2024/132/ionPrf_nrt_2024_132.tar.gz
200 https://cdaac-www.cosmic.ucar.edu/                         （旧门户首页）
401 https://cdaac-www.cosmic.ucar.edu/cdaac/login/             （旧门户登录）
401 https://cdaac-www.cosmic.ucar.edu/cdaac/tar/rest.html      （旧门户 tar 下载接口）
200 https://cdaac-www.cosmic.ucar.edu/cdaac/cgi_bin/fileFormats.cgi?type=ionPrf   （格式说明，公开）
```

结论：`data.cosmic.ucar.edu` 下 COSMIC-2 的所有产品（含 level0）都**匿名 200**；只有旧门户 `cdaac-www` 的登录 / tar 接口是 **401**。不需要为这两个产品注册任何账号。

### 3.4 下载：ionPrf 整个日包，podTc2 只取 3 个文件

```bash
B=https://data.cosmic.ucar.edu/gnss-ro/cosmic2
curl -s -o ionPrf.tgz -w "%{http_code} %{size_download} %{time_total}\n" $B/provisional/spaceWeather/level2/2024/132/ionPrf_prov1_2024_132.tar.gz
tar tzf ionPrf.tgz | wc -l
```

```text
200 27856720 1.500741
3608
```

解开后 43 MB。podTc2 用 Python 标准库流式读取（`podhead.py`，原样）：

```python
import tarfile, urllib.request, sys
url = "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1b/2024/132/podTc2_nrt_2024_132.tar.gz"
class Count:
    def __init__(s, r): s.r, s.n = r, 0
    def read(s, k=-1):
        b = s.r.read(k); s.n += len(b); return b
r = Count(urllib.request.urlopen(url))
with tarfile.open(fileobj=r, mode="r|gz") as tf:
    for i, m in enumerate(tf):
        tf.extract(m, "pod")
        print(m.name, m.size)
        if i == 2: break
print("bytes pulled from server:", r.n)
```

```text
podTc2_C2E1.2024.132.00.01.0017.G27.02_0001.0001_nc 97452
podTc2_C2E1.2024.132.00.07.0011.G17.01_0001.0001_nc 66608
podTc2_C2E1.2024.132.00.09.0009.G30.01_0001.0001_nc 57392
bytes pulled from server: 163840
```

（Python 3.13 会给出 `DeprecationWarning`，提示 3.14 起 `extract` 默认要加 `filter=`；加上 `filter="data"` 即可。）包内成员按时间排序，所以这种方式只能拿到“一天最早的几个文件”，要某颗卫星或某个时段就得一直读到那里。

### 3.5 读一个 ionPrf：变量和全局属性

`dump1.py`（原样，后面 podTc2 也用它）：

```python
import netCDF4, sys
ds = netCDF4.Dataset(sys.argv[1])
print("format:", ds.file_format)
print("dims:", {k: len(v) for k, v in ds.dimensions.items()})
for k, v in ds.variables.items():
    print(f"var {k}{v.dimensions} {v.dtype} units={getattr(v,'units','-')!r} long={getattr(v,'long_name','-')!r}")
for a in ds.ncattrs():
    print(f"attr {a} = {ds.getncattr(a)!r}")
```

`venv/bin/python dump1.py ion/ionPrf_C2E1.2024.132.00.00.G21_0001.0001_nc`，输出（原样，只把 `np.float64(x)` / `np.int32(x)` 写成 x，并把 attr 排成多列）：

```text
format: NETCDF3_CLASSIC
dims: {'MSL_alt': 284}
var MSL_alt('MSL_alt',) float32 units='km' long='Mean sea level altitude of perigee point'
var GEO_lat('MSL_alt',) float32 units='degrees_north' long='Geographical latitude of perigee point'
var GEO_lon('MSL_alt',) float32 units='degrees_east' long='Geographical longitude of perigee point'
var OCC_azi('MSL_alt',) float32 units='deg' long='Azimuth angle of occ. plane with respect to north'
var TEC_cal('MSL_alt',) float32 units='TECU' long='Calibrated occultation TEC below LEO orbit'
var ELEC_dens('MSL_alt',) float32 units='el/cm3' long='Electron density'
occ_id 0   fiducial_id '    '   reference_sat_id -999   occulting_sat_id 21
year 2024  month 5  day 11  hour 0  minute 5  second 14.0   offset 0  shortlen 284  setting 0  icalib 1
botnum 1    bottime 1399420756.0  botlct 3.5649  botalt 62.796   botlat 17.087  botlon 53.657  botaz 87.83
topnum 284  toptime 1399421114.0  toplct 3.6902  topalt 533.770  toplat 21.258  toplon 54.045  topaz 86.45
edmaxtime 1399421114.0  edmaxlct 3.6902  edmaxalt 533.770  edmaxlat 21.258  edmaxlon 54.045  edmaxaz 86.45
smear 465.555  edmax 44169.83  critfreq 1.88682  tec0 0.33021  tec1 -999.0
edorbtime 1399421130.54  edorbalt 534.842  edorb 42645.52  hscale -999.0  topfit 0.023696  nmax 284
fileStamp 'C2E1.2024.132.00.00.G21'  inverter 'gmrion'  parmsfile 'parms8'  center 'UCAR/CDAAC'  mission 'COSEQ'  creation_time '11-MAY-24 00:56'
```

含义（格式说明页原文译述）：

| 名字 | 含义 | 单位 |
| --- | --- | --- |
| `MSL_alt` | 切点（perigee point）**平均海平面高度**，也是唯一维度 | km |
| `GEO_lat` / `GEO_lon` | 每个高度上切点的地理纬度 / 经度（沿剖面会移动） | deg |
| `OCC_azi` | 掩星平面相对正北的方位角 | deg |
| `TEC_cal` | LEO 轨道以下的校准掩星 TEC | TECU |
| `ELEC_dens` | 电子密度；有效范围 ±1e8，缺测 -999，**允许负值** | **el/cm³** |
| `edmax` / `edmaxalt` / `edmaxlat` / `edmaxlon` / `edmaxlct` / `edmaxtime` | 最大电子密度及其高度、位置、地方时（h）、GPS 秒 | el/cm³ / km / deg / h / s |
| `critfreq` | 峰值处的等离子体频率（≈ foF2） | MHz |
| `bot*` / `top*` | 剖面最底 / 最顶那一点的时间、地方时、高度、位置 | |
| `smear` | 切点从顶到底的水平漂移 | km |
| `tec0` / `tec1` | 底到顶的积分 TEC / 顶以上外推 TEC（-999 = 没算） | TECU |
| `edorb*` / `hscale` | 轨道高度处 Ne 估计 / 标高（只在 `icalib=0` 时用） | el/cm³ / km |
| `topfit` | 顶部附近的拟合残差 | TECU |
| `setting` | 1 = 下降掩星，0 = 上升掩星 | |
| `icalib` | 1 = 远端 TEC 校准，0 = 准校准 | |
| `year`…`second` | **`edmaxtime` 的**日历时间（不是文件名里的开始时间） | |

这条 G21 剖面的 `edmaxalt` 就等于 `topalt`（533.77 km）：峰落在剖面顶端，说明没有反演出 F2 峰（当地 03:41 LT 夜间），这是下面 3.7 的剔除对象之一。

### 3.6 edmax/edmaxalt vs 从剖面自己找 NmF2/hmF2；一天的数量和覆盖

`ionday.py`（原样）：

```python
import netCDF4, glob, numpy as np, collections, datetime as dt
files = sorted(glob.glob("ion/ionPrf_*"))
rows = []
for f in files:
    ds = netCDF4.Dataset(f)
    a = {k: ds.getncattr(k) for k in ds.ncattrs()}
    ne = ds["ELEC_dens"][:].astype(float); z = ds["MSL_alt"][:].astype(float)
    ds.close()
    ne = np.ma.filled(ne, np.nan)
    i = int(np.nanargmax(ne))
    rows.append(dict(f=f.split("/")[-1], sat=a["fileStamp"][:4], gnss=a["fileStamp"][-3], n=len(z),
        edmax=a["edmax"], edmaxalt=a["edmaxalt"], nm=ne[i], hm=z[i], zmin=np.nanmin(z), zmax=np.nanmax(z),
        top=a["topalt"], lat=a["edmaxlat"], lon=a["edmaxlon"], lct=a["edmaxlct"], critf=a["critfreq"],
        negfrac=np.mean(ne < 0), t=a["edmaxtime"]))
R = {k: np.array([r[k] for r in rows]) for k in rows[0]}
N = len(rows)
print("profiles:", N, "| per sat:", dict(sorted(collections.Counter(R["sat"]).items())),
      "| GNSS:", dict(collections.Counter(R["gnss"])))
print("levels/profile: min %d median %d max %d" % (R["n"].min(), np.median(R["n"]), R["n"].max()))
print("MSL_alt range km: bottom median %.1f, top median %.1f" % (np.median(R["zmin"]), np.median(R["zmax"])))
d_ne = np.abs(R["nm"] - R["edmax"]) / R["edmax"]; d_h = np.abs(R["hm"] - R["edmaxalt"])
print("edmax vs max(ELEC_dens): max rel diff %.2e ; edmaxalt vs MSL_alt[argmax]: max |diff| %.3f km" % (d_ne.max(), d_h.max()))
fo = 8.98e-6 * np.sqrt(R["edmax"] * 1e6)   # MHz, Ne in m^-3
print("critfreq vs 8.98*sqrt(edmax*1e6): max |diff| %.4f MHz" % np.abs(fo - R["critf"]).max())
print("lat range %.1f..%.1f  |lat|<=30: %.1f%%  |lat|<=45: %.1f%%" % (R["lat"].min(), R["lat"].max(),
      100*np.mean(np.abs(R["lat"]) <= 30), 100*np.mean(np.abs(R["lat"]) <= 45)))
print("lon range %.1f..%.1f  ; lon 30-deg bins:" % (R["lon"].min(), R["lon"].max()),
      np.histogram(R["lon"] % 360, bins=12, range=(0, 360))[0].tolist())
print("local time 3-h bins (0-3,...,21-24):", np.histogram(R["lct"], bins=8, range=(0, 24))[0].tolist())
t0 = dt.datetime(1980, 1, 6) + dt.timedelta(seconds=float(R["t"].min()))
t1 = dt.datetime(1980, 1, 6) + dt.timedelta(seconds=float(R["t"].max()))
print("edmaxtime as GPS-epoch seconds (no leap correction):", t0, "->", t1)
at_top = np.abs(R["edmaxalt"] - R["top"]) < 1e-6
low = R["edmaxalt"] < 150; high = R["edmaxalt"] > 500
neg = R["negfrac"] > 0
print("peak == topalt (profile top): %d ; hmF2<150 km: %d ; hmF2>500 km: %d ; any Ne<0: %d" % (at_top.sum(), low.sum(), high.sum(), neg.sum()))
good = ~at_top & ~low & ~high
print("kept by (not top, 150<=hm<=500): %d / %d (%.1f%%)" % (good.sum(), N, 100*good.mean()))
for lab, m in (("all", np.ones(N, bool)), ("kept", good)):
    print("%-4s NmF2 median %.3e el/cm3 = %.3e m^-3 ; p5-p95 %.2e..%.2e ; hmF2 median %.1f km p5-p95 %.1f..%.1f" % (lab,
        np.median(R["edmax"][m]), np.median(R["edmax"][m]) * 1e6, *np.percentile(R["edmax"][m], [5, 95]),
        np.median(R["edmaxalt"][m]), *np.percentile(R["edmaxalt"][m], [5, 95])))
ex = [i for i in range(N) if good[i]][0]
print("example kept:", R["f"][ex], "edmax %.1f edmaxalt %.2f | max(ELEC_dens) %.1f at MSL_alt %.2f | lat %.2f lon %.2f LT %.2f" % (
    R["edmax"][ex], R["edmaxalt"][ex], R["nm"][ex], R["hm"][ex], R["lat"][ex], R["lon"][ex], R["lct"][ex]))
print("example rejected:", R["f"][0], "edmaxalt %.2f topalt %.2f LT %.2f" % (R["edmaxalt"][0], R["top"][0], R["lct"][0]))
```

```text
profiles: 3608 | per sat: {np.str_('C2E1'): 650, np.str_('C2E2'): 582, np.str_('C2E3'): 552, np.str_('C2E4'): 572, np.str_('C2E5'): 661, np.str_('C2E6'): 591} | GNSS: {np.str_('G'): 1690, np.str_('R'): 1918}
levels/profile: min 247 median 327 max 424
MSL_alt range km: bottom median 47.4, top median 533.6
edmax vs max(ELEC_dens): max rel diff 2.65e+00 ; edmaxalt vs MSL_alt[argmax]: max |diff| 497.225 km
critfreq vs 8.98*sqrt(edmax*1e6): max |diff| 0.0051 MHz
lat range -40.5..40.4  |lat|<=30: 95.3%  |lat|<=45: 100.0%
lon range -179.6..180.0  ; lon 30-deg bins: [333, 332, 310, 216, 260, 291, 316, 323, 309, 297, 320, 301]
local time 3-h bins (0-3,...,21-24): [441, 381, 461, 473, 508, 456, 452, 436]
edmaxtime as GPS-epoch seconds (no leap correction): 2024-05-10 23:55:41 -> 2024-05-12 00:02:36
peak == topalt (profile top): 317 ; hmF2<150 km: 106 ; hmF2>500 km: 841 ; any Ne<0: 2502
kept by (not top, 150<=hm<=500): 2661 / 3608 (73.8%)
all  NmF2 median 8.924e+05 el/cm3 = 8.924e+11 m^-3 ; p5-p95 1.04e+05..2.43e+06 ; hmF2 median 395.5 km p5-p95 181.4..534.5
kept NmF2 median 9.327e+05 el/cm3 = 9.327e+11 m^-3 ; p5-p95 1.22e+05..2.43e+06 ; hmF2 median 362.8 km p5-p95 194.2..484.1
example kept: ionPrf_C2E1.2024.132.00.07.G11_0001.0001_nc edmax 83114.6 edmaxalt 183.84 | max(ELEC_dens) 83114.6 at MSL_alt 183.84 | lat 11.16 lon 44.03 LT 3.05
example rejected: ionPrf_C2E1.2024.132.00.00.G21_0001.0001_nc edmaxalt 533.77 topalt 533.77 LT 3.69
```

“最大差 2.65 倍 / 497 km”来自少数剖面，`ionmis.py`（原样）把它们找出来：

```python
import netCDF4, glob, numpy as np
files = sorted(glob.glob("ion/ionPrf_*"))
same = 0; mis = []
for f in files:
    ds = netCDF4.Dataset(f); a = {k: ds.getncattr(k) for k in ds.ncattrs()}
    ne = np.ma.filled(ds["ELEC_dens"][:].astype(float), np.nan); z = ds["MSL_alt"][:].astype(float); ds.close()
    i = int(np.nanargmax(ne))
    if abs(ne[i] - a["edmax"]) / a["edmax"] < 1e-5 and abs(z[i] - a["edmaxalt"]) < 1e-3: same += 1
    else:
        j = int(np.argmin(np.abs(z - a["edmaxalt"])))
        mis.append((f.split("/")[-1], a["edmax"], a["edmaxalt"], ne[j], ne[i], z[i], z.min(), z.max(), a["topalt"]))
print("identical (rel<1e-5, <1 m):", same, "/", len(files), "; differ:", len(mis))
zi = np.array([m[5] for m in mis]); zb = np.array([m[6] for m in mis])
print("in mismatches, raw argmax altitude: <120 km: %d ; 120-150: %d ; >=150: %d" % ((zi < 120).sum(), ((zi >= 120) & (zi < 150)).sum(), (zi >= 150).sum()))
print("in mismatches, Ne at edmaxalt equals edmax:", sum(abs(m[3] - m[1]) / m[1] < 1e-5 for m in mis))
for m in mis[:4]:
    print("  %s edmax %.0f @%.1f | raw max %.0f @%.1f km | alt %.1f..%.1f" % (m[0], m[1], m[2], m[4], m[5], m[6], m[7]))
# restrict argmax to >=150 km: does it reproduce edmax?
ok = 0
for f in files:
    ds = netCDF4.Dataset(f); a = {k: ds.getncattr(k) for k in ds.ncattrs()}
    ne = np.ma.filled(ds["ELEC_dens"][:].astype(float), np.nan); z = ds["MSL_alt"][:].astype(float); ds.close()
    m = z >= 150
    i = np.nanargmax(np.where(m, ne, -np.inf))
    ok += abs(ne[i] - a["edmax"]) / a["edmax"] < 1e-5 and abs(z[i] - a["edmaxalt"]) < 1e-3
print("argmax restricted to MSL_alt>=150 km reproduces edmax/edmaxalt:", ok, "/", len(files))
```

```text
identical (rel<1e-5, <1 m): 3571 / 3608 ; differ: 37
in mismatches, raw argmax altitude: <120 km: 37 ; 120-150: 0 ; >=150: 0
in mismatches, Ne at edmaxalt equals edmax: 37
  ionPrf_C2E1.2024.132.01.39.G21_0001.0001_nc edmax 39492 @532.3 | raw max 66886 @71.7 km | alt 69.9..533.3
  ionPrf_C2E1.2024.132.04.41.G27_0001.0001_nc edmax 37714 @81.3 | raw max 87072 @49.7 km | alt 1.8..534.9
  ionPrf_C2E1.2024.132.06.00.G32_0001.0001_nc edmax 303978 @82.1 | raw max 325618 @49.4 km | alt 49.4..535.8
  ionPrf_C2E1.2024.132.06.23.G02_0001.0001_nc edmax 340265 @98.6 | raw max 357559 @63.9 km | alt 1.0..534.1
argmax restricted to MSL_alt>=150 km reproduces edmax/edmaxalt: 3502 / 3608
```

**两种方法的结论（用上面的数字）**：

- **98.97 % 完全一致**：3608 条里 3571 条的 `edmax` 与 `max(ELEC_dens)`、`edmaxalt` 与对应 `MSL_alt` 在 1e-5 相对误差 / 1 m 以内相同。例：G11 剖面 `edmax` 83114.6 el/cm³ @ 183.84 km，自己找也是 83114.6 @ 183.84。
- **37 条不一致，全部是自己找的峰落在 <120 km**（D/E 区以下的反演噪声，例如 71.7 km 处 66886）；CDAAC 的 `edmax` 在这 37 条里都**仍等于剖面上 `edmaxalt` 那一点的值**，只是它不取最底部那段。
- 但 `edmax` 也不是“F2 峰”：简单地把搜索限制在 ≥150 km 只复现 3502/3608，因为 `edmax` 本身可以落在 81–99 km（上面第 2–4 行）或剖面顶端。**NmF2/hmF2 要自己加高度窗和“峰不在端点”的判定**，不能直接把 `edmax` 当 NmF2。
- `critfreq` 与 `8.98e-6·sqrt(edmax·1e6)` MHz 最大差 0.0051 MHz，证明 `edmax` 的单位是 el/cm³（换 m⁻³ 要 ×1e6）。

**一天的数量和覆盖**：2024-132 日包 3608 条（6 颗卫星各 552–661 条；GPS 1690、GLONASS 1918）；峰值点纬度 −40.5°～40.4°（95.3 % 在 ±30° 内，没有一条超过 ±45°，这是 24° 倾角轨道的结果）；经度 12 个 30° 格每格 216–333 条；地方时 8 个 3 h 格每格 381–508 条，基本均匀。另外 `dayedge.py`（原样）说明日包并不严格按 UTC 日切：

```python
import netCDF4, glob, datetime as dt
t0 = (dt.datetime(2024, 5, 11) - dt.datetime(1980, 1, 6)).total_seconds() + 18   # 00:00 UTC in GPS seconds (GPS-UTC = 18 s)
before = after = 0
for f in glob.glob("ion/ionPrf_*"):
    ds = netCDF4.Dataset(f); e = ds.edmaxtime; stamp = ds.fileStamp; ds.close()
    before += e < t0; after += e >= t0 + 86400
print("edmaxtime before 2024-05-11 00 UTC:", before, "; on/after 05-12 00 UTC:", after)
```

```text
edmaxtime before 2024-05-11 00 UTC: 8 ; on/after 05-12 00 UTC: 1
```

### 3.7 质量标志：ionPrf 没有，只能自己筛；podTc2 有几个

`attrs_union.py`（原样）把 3608 个文件的变量和属性取并集：

```python
import netCDF4, glob, collections
files = sorted(glob.glob("ion/ionPrf_*"))
attrs = collections.Counter(); vars_ = collections.Counter(); fmts = collections.Counter()
for f in files:
    ds = netCDF4.Dataset(f)
    attrs.update(ds.ncattrs()); vars_.update(ds.variables.keys()); fmts[ds.file_format] += 1
    ds.close()
print("files:", len(files), dict(fmts))
print("vars:", dict(vars_))
print("attrs not in every file:", {k: v for k, v in attrs.items() if v != len(files)})
print("n attrs:", len(attrs), "bad-like:", [k for k in attrs if 'bad' in k.lower() or 'qual' in k.lower() or 'flag' in k.lower()])
```

```text
files: 3608 {'NETCDF3_CLASSIC': 3608}
vars: {'MSL_alt': 3608, 'GEO_lat': 3608, 'GEO_lon': 3608, 'OCC_azi': 3608, 'TEC_cal': 3608, 'ELEC_dens': 3608}
attrs not in every file: {}
n attrs: 51 bad-like: []
```

- **ionPrf（prov1）没有任何 bad / quality / flag 属性**，51 个属性每个文件都一样。发布说明 PDF 也只写了“ionosonde foF2 日对比相关系数可达 0.97、未发现偏差”，没有给质控标志。
- 所以用 3.6 里的**自定义筛选**：去掉峰在剖面顶端（317 条）、`edmaxalt` < 150 km（106 条）、> 500 km（841 条），剩 **2661 / 3608（73.8 %）**；筛后 hmF2 中位数从 395.5 km 降到 362.8 km，p95 从 534.5 降到 484.1 km，NmF2 中位数 8.92e5 → 9.33e5 el/cm³。**阈值是本文自选的，不是 CDAAC 的**；磁暴期 hmF2 本来就高，500 km 上限可能误杀，按研究目的调。另有 2502 条剖面在某些高度出现负 Ne（格式允许负值），通常在底部，算积分量前要处理。
- podTc2 有 `podflag` / `attflag`（定轨 / 姿态是否可用，1 = 用了）、`leodcb_flag` / `gpsdcb_flag`、逐点的 `absolute_tec_indicator`，以及格式页没写的 `ion_occ_score`（见 3.8）。

### 3.8 读 podTc2：一条链路的 TEC、仰角、坐标

`dump1.py` 输出的变量部分（原样）和部分属性：

```text
format: NETCDF3_CLASSIC
dims: {'attribute_dimension': 1, 'time': 633}
var leveling_offset('attribute_dimension',) float64 units='TEC Units' long='Phase/code leveling offset:  Absolute TEC = relative TEC + leveling_offset + GNSS DCB + LEO DCB'
var time('time',) float64 units='s' long='Time of GPS measurement (GPS seconds)'
var TEC('time',) float64 units='TECU' long='Total Electron Content along LEO-GPS link'
var S4('time',) float32 units='Unitless' long='S4 scintillation index'
var RFI('time',) float32 units='Unitless' long='Radio Frequency Interference index'
var elevation('time',) float64 units='deg' long='Elevation angle of LEO-GPS link'
var occheight('time',) float64 units='km' long='Occultation perigee point height'
var caL1_SNR('time',) float32 units='volts/volt' long='Signal to Noise Ratio on the L1 channel, CA code'
var pL2_SNR('time',) float32 units='volts/volt' long='Signal to Noise Ratio on the L2 channel, L2L code'
var x_LEO('time',) float64 units='km' long='LEO x position (ECF) at time of signal reception'
var y_LEO('time',) float64 units='km' long='LEO y position (ECF) at time of signal reception'
var z_LEO('time',) float64 units='km' long='LEO z position (ECF) at time of signal reception'
var x_GPS('time',) float64 units='km' long='GPS x position (ECF) at time of signal transmission'
var y_GPS('time',) float64 units='km' long='GPS y position (ECF) at time of signal transmission'
var z_GPS('time',) float64 units='km' long='GPS z position (ECF) at time of signal transmission'
var absolute_tec_indicator('time',) int8 units='-' long='Vector indicating whether TEC is absolute or extrapolated relative TEC.  1 = absolute, 0 = relative'
attr leo_id = 1 · antenna_id = 1 · prn_id = 17 · conid = 'G' · L2C = 1 · attflag = 1 · podflag = 1 · ion_occ_score = 0
attr leodcb = 7.892 · leodcb_rms = 0.391 · gpsdcb = 9.445 · leveling_err = 0.138 · dcb_units = 'TECU' · calfile = 'mulCal_2020.161.001.01.G_nc'
attr tecmin = 21.344 · tecmax = 43.261 · elevmin = 20.128 · elevmax = 36.042 · tecsinmax = 12.558 · lat_elevmax 22.643 · lon_elevmax 61.233 · lct_elevmax 4.201
```

（全部 60 多个属性还包括 `arcTab_*`、`gobs_*`、`*_start` / `*_stop` / `*_tecmax` 的 LEO 高度 / 经纬度 / 地方时等，此处省略。）

`podread.py`（原样）检查三条链路，并用两端坐标重算仰角：

```python
import netCDF4, glob, numpy as np
for f in sorted(glob.glob("pod/podTc2_*")):
    ds = netCDF4.Dataset(f); g = lambda k: np.ma.filled(ds[k][:].astype(float), np.nan)
    t, tec, el, oh = g("time"), g("TEC"), g("elevation"), g("occheight")
    L = np.c_[g("x_LEO"), g("y_LEO"), g("z_LEO")]; G = np.c_[g("x_GPS"), g("y_GPS"), g("z_GPS")]
    d = G - L; rL = np.linalg.norm(L, axis=1); rng = np.linalg.norm(d, axis=1)
    el_calc = np.degrees(np.arcsin(np.sum(d * L, 1) / (rng * rL)))   # spherical: angle above plane normal to LEO radius
    abs_ind = ds["absolute_tec_indicator"][:]
    print(f.split("/")[-1])
    print("  n=%d  dt=%s s  GPS-sec %.0f..%.0f  prn=%s%d leo=%d antenna=%d  podflag=%d attflag=%d  ion_occ_score=%d" % (
        len(t), np.unique(np.diff(t))[:3], t[0], t[-1], ds.conid, ds.prn_id, ds.leo_id, ds.antenna_id, ds.podflag, ds.attflag, ds.ion_occ_score))
    print("  TEC %.2f..%.2f TECU (attr tecmin %.3f tecmax %.3f)  leveling_offset %.3f  leodcb %.3f gpsdcb %.3f leveling_err %.3f" % (
        np.nanmin(tec), np.nanmax(tec), ds.tecmin, ds.tecmax, float(ds["leveling_offset"][0]), ds.leodcb, ds.gpsdcb, ds.leveling_err))
    print("  elevation %.2f..%.2f deg ; recomputed from x/y/z (spherical) max |diff| %.3f deg" % (np.nanmin(el), np.nanmax(el), np.nanmax(np.abs(el - el_calc))))
    print("  occheight %.1f..%.1f km ; |r_LEO|-6371 = %.1f..%.1f km ; |r_GPS| %.0f km ; link range %.0f..%.0f km" % (
        np.nanmin(oh), np.nanmax(oh), rL.min() - 6371, rL.max() - 6371, np.linalg.norm(G, axis=1).mean(), rng.min(), rng.max()))
    print("  absolute_tec_indicator counts:", {int(k): int(v) for k, v in zip(*np.unique(abs_ind, return_counts=True))},
          " S4 %.3f..%.3f" % (np.nanmin(g("S4")), np.nanmax(g("S4"))))
    ds.close()
```

```text
podTc2_C2E1.2024.132.00.01.0017.G27.02_0001.0001_nc
  n=951  dt=[1. 2. 3.] s  GPS-sec 1399420917..1399421880  prn=G27 leo=1 antenna=2  podflag=1 attflag=1  ion_occ_score=1
  TEC 33.12..68.80 TECU (attr tecmin 33.118 tecmax 68.797)  leveling_offset 380479.881  leodcb -2.311 gpsdcb -15.311 leveling_err 0.200
  elevation -21.52..7.63 deg ; recomputed from x/y/z (spherical) max |diff| 0.000 deg
  occheight 59.1..399.5 km ; |r_LEO|-6371 = 536.2..540.0 km ; |r_GPS| 26375 km ; link range 24573..28094 km
  absolute_tec_indicator counts: {0: 12, 1: 939}  S4 0.103..0.254
podTc2_C2E1.2024.132.00.07.0011.G17.01_0001.0001_nc
  n=633  dt=[1. 2. 3.] s  GPS-sec 1399421245..1399421880  prn=G17 leo=1 antenna=1  podflag=1 attflag=1  ion_occ_score=0
  TEC 21.34..43.26 TECU (attr tecmin 21.344 tecmax 43.261)  leveling_offset 354082.083  leodcb 7.892 gpsdcb 9.445 leveling_err 0.138
  elevation 20.13..36.04 deg ; recomputed from x/y/z (spherical) max |diff| 0.000 deg
  occheight nan..nan km ; |r_LEO|-6371 = 537.5..538.7 km ; |r_GPS| 26354 km ; link range 21676..23180 km
  absolute_tec_indicator counts: {1: 633}  S4 0.053..0.126
podTc2_C2E1.2024.132.00.09.0009.G30.01_0001.0001_nc
  n=538  dt=[1. 2.] s  GPS-sec 1399421342..1399421880  prn=G30 leo=1 antenna=1  podflag=1 attflag=1  ion_occ_score=0
  TEC 18.05..28.89 TECU (attr tecmin 18.050 tecmax 28.886)  leveling_offset 353139.355  leodcb 7.892 gpsdcb -18.247 leveling_err 0.144
  elevation 30.77..47.47 deg ; recomputed from x/y/z (spherical) max |diff| 0.000 deg
  occheight nan..nan km ; |r_LEO|-6371 = 537.5..538.4 km ; |r_GPS| 26652 km ; link range 21154..22441 km
  absolute_tec_indicator counts: {1: 538}  S4 0.051..0.116
```

（第 2、3 个文件的 `occheight` 全是缺测，`np.nanmin` 另打了一行 `RuntimeWarning: All-NaN slice encountered`。）补充一段交互检查（G27 文件），命令与输出都是原样：

```bash
venv/bin/python -c "
import netCDF4, numpy as np, datetime as dt
ds=netCDF4.Dataset('pod/podTc2_C2E1.2024.132.00.01.0017.G27.02_0001.0001_nc')
oh=ds['occheight'][:]; el=ds['elevation'][:]
print('occheight valid', int((~np.ma.getmaskarray(oh)).sum()), 'of', len(el), '; elevation<0 count', int((el<0).sum()), '; fill', ds['occheight'].__dict__.get('_FillValue'))
m=~np.ma.getmaskarray(oh); print('elevation range where occheight valid %.2f..%.2f' % (el[m].min(), el[m].max()))
t=ds['time'][0]; print('time[0] GPS-sec', t, '-> GPS', dt.datetime(1980,1,6)+dt.timedelta(seconds=float(t)), '-> UTC (-18 s)', dt.datetime(1980,1,6)+dt.timedelta(seconds=float(t)-18))
ai=ds['absolute_tec_indicator'][:]; print('abs=0 at elevation', el[ai==0].min(), el[ai==0].max())
"
```

```text
occheight valid 316 of 951 ; elevation<0 count 690 ; fill -999.0
elevation range where occheight valid -21.52..-11.48
time[0] GPS-sec 1399420917.0 -> GPS 2024-05-11 00:01:57 -> UTC (-18 s) 2024-05-11 00:01:39
abs=0 at elevation -20.98075761615619 0.27994860078372563
```

字段怎么理解：

- **`TEC`**：沿 LEO→GNSS 整条链路的斜向 TEC（TECU）。`absolute_tec_indicator=1` 表示已按描述里的公式 `绝对 TEC = 相对 TEC + leveling_offset + GNSS DCB + LEO DCB` 调平并扣了 DCB；`0` 表示只是外推的相对 TEC（G27 文件里 12 个点，出现在弧段两端）。`leveling_offset` 是一个很大的数（3.5e5～3.8e5），**不要自己再加一次**：`TEC` 已经在 `tecmin`/`tecmax` 范围里（21–69 TECU）。
- **`elevation`**：从 LEO 看 GNSS 卫星的仰角（deg），用两端 ECEF 坐标按球形地球重算，三条链路**最大差 0.000°**。**正仰角**（天线 01，G17 20–36°、G30 31–47°）= LEO 轨道以上（顶部电离层 + 等离子体层）的 TEC；**负仰角**（天线 02，G27 最低 −21.5°）= 穿过下方电离层的掩星段。
- **`occheight`**：链路切点高度（km），只在掩星段有值（G27：仰角 ≤ −11.5° 的 316 个点，59–400 km），正仰角段全是 -999。
- **`x/y/z_LEO`、`x/y/z_GPS`**：ECEF（地固系）km，LEO 取接收时刻、GNSS 取发射时刻。|r_LEO|−6371 ≈ 536–540 km（COSMIC-2 轨道高度），|r_GPS| ≈ 26,350–26,650 km；GLONASS 链路变量名也叫 `*_GPS`。
- **`time`**：GPS 秒（1980-01-06 起），**减 18 s 才是 UTC**；间隔名义 1 s，但有 2–3 s 缺口。
- **`S4`**：星上 10 s 窗口算出的闪烁指数（发布说明：弧段开头偶有异常大的值，需要自己剔除）。

## 4. 输入与输出

| 输入 | 输出 |
| --- | --- |
| `…/provisional/spaceWeather/level2/YYYY/DDD/ionPrf_prov1_YYYY_DDD.tar.gz`（13–27 MB/天） | 每次掩星一个 `ionPrf_C2En.YYYY.DDD.HH.MM.Gnn_0001.0001_nc`（约 10 KB，netCDF-3），一维剖面 247–424 层 |
| `…/{nrt,rapid}/level1b/YYYY/DDD/podTc2_{nrt,rapid}_YYYY_DDD.tar.gz`（0.5–0.9 GB/天） | 每条链路一个 `podTc2_C2En.YYYY.DDD.HH.MM.UUUU.Gnn.TT_0001.0001_nc`（57–97 KB） |
| 本文脚本 | NmF2（el/cm³ 与 m⁻³）、hmF2（km，MSL）、峰值位置和地方时、自定义质量掩膜；链路 TEC / 仰角 / 切点高度 |

## 5. 参数

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| `<stream>` | `provisional/spaceWeather`（ionPrf）/ `nrt` / `rapid` / `postProc`（podTc2） | 见 3.1 表；COSMIC-2 没有 `repro` |
| `<level>` | `level1b`（podTc2）/ `level2`（ionPrf） | |
| `YYYY/DDD` | 年 / 三位年积日 | 2024-05-11 = `2024/132` |
| 高度窗（自选） | 150–500 km，且峰不在端点 | 用来从 `edmax` 得到可用的 NmF2/hmF2 |
| `absolute_tec_indicator` | 1 / 0 | 只用 1 的点做绝对 TEC |
| 仰角 | > 0 / < 0 | 顶部 TEC / 掩星段 |

## 6. 在工作流里接哪一步

1. [A — 一日 TEC](./README.md#a--一日-tec)：用 ionPrf 的 NmF2/hmF2 和 foF2（`critfreq`）去对照地基 TEC 图或测高仪；podTc2 正仰角段可以给 LEO 以上的 TEC（地基 TEC 里包含这一段，GIM 对比时要记得）。
2. [B — 不规则体 / 磁暴](./README.md#b--不规则体--磁暴)：像本例的 2024-05-11，按经度 / 地方时分箱看 hmF2 抬升和 NmF2 变化；podTc2 的 `S4` 和负仰角段看赤道闪烁。
3. 需要 COSMIC-1 或统一 pysat 接口时换 [pysatcdaac](./pysatcdaac.md)；要中性大气剖面换 [awsgnssroutils](./awsgnssroutils.md)。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `nrt/level2/…/ionPrf_nrt_…` 404 | COSMIC-2 的 ionPrf 只发布在 `provisional/spaceWeather/level2/`，文件名是 `ionPrf_prov1_…` | 用 3.1 的路径；换日期前先列目录 |
| 2 | 按 COSMIC-1 的习惯找 `repro` 或 `postProc` ionPrf，得到 404 | `cosmic2/repro/` 不存在（COSMIC-1 有 `repro2013`）；`cosmic2/postProc/level2/` 里只有 IVM；`postProc/level1b` 只有 2020 年的 podTc2 | COSMIC-2 电离层只有“nrt 式处理”的版本：ionPrf = prov1，podTc2 = nrt / rapid；在论文里写明版本和下载日期 |
| 3 | 同一天的 podTc2 在 `nrt` 和 `rapid` 下大小不同（919 vs 682 MB） | 两条独立处理流：nrt 约 5 h 出，rapid 约 1.7 天出（本轮 last-modified 实测）；本轮没有比较两者内容差异 | 实时监测用 nrt；事后分析二选一并固定，不要混用 |
| 4 | Ne 比模型大 100 万倍或小 100 万倍 | `ELEC_dens`、`edmax`、`edorb` 都是 **el/cm³**；IRI 等多用 m⁻³ | ×1e6 变 m⁻³；用 `critfreq` ≈ 8.98e-6·√(edmax·1e6) MHz 自检（实测差 ≤0.0051 MHz） |
| 5 | hmF2 和别的数据集差几十米到几百米 | `MSL_alt` 是**平均海平面（大地水准面）高度**，不是 WGS84 椭球高，也不是地心距；podTc2 的坐标则是 ECEF 地心 | 与椭球高数据对比时加大地水准面起伏（±100 m 量级），对 hmF2 一般可忽略，但不要把 `MSL_alt` 当地心半径 |
| 6 | 把 `edmax`/`edmaxalt` 当 NmF2/hmF2，得到 81 km 或 534 km 的“峰” | `edmax` 看起来是剖面去掉最底部一段后的最大值，并不判断是否为 F2 峰：317 条峰落在剖面顶端、106 条 <150 km | 加高度窗 + 端点判定（3.7：保留 73.8 %）；或自己在 150–500 km 内找峰 |
| 7 | 自己 `argmax(ELEC_dens)` 得到 50–70 km 的巨大值 | 37 条剖面最底部有反演噪声，比 F 区还大 | 至少排除 <120 km；`edmax` 在这 37 条里是对的 |
| 8 | 找不到坏廓线标志 | prov1 ionPrf 的 51 个属性里没有 bad / quality / flag | 自定义筛选（坑 6），并处理 2502 条剖面中的负 Ne |
| 9 | 一条剖面画在一个点上，与地面站配对差了几百公里 | 切点沿剖面漂移：`smear` 示例 465.6 km，`GEO_lat/lon` 每层都不同 | 配对用 `edmaxlat/edmaxlon`（峰处），或者逐层用 `GEO_lat/lon` |
| 10 | 时间差 18 s，或日统计多出几条 | `edmaxtime`、`time` 是 GPS 秒；`year…second` 是 edmaxtime 的日历时间而不是文件名时间；日包里有 8 条在前一天 23:5x UT、1 条在次日 | 减 18 s（GPS−UTC）；按 `edmaxtime` 自己切 UTC 日 |
| 11 | 把 podTc2 的 `leveling_offset`（约 3.5e5 TECU）加到 TEC 上 | `TEC` 已经是调平并扣 DCB 后的值（`absolute_tec_indicator=1`）；offset 只是说明用 | 直接用 `TEC`；只用 indicator=1 的点；2020 年的发布说明写的是“相对 TEC、无 DCB”，老文件先看属性 |
| 12 | podTc2 一天 0.5–0.9 GB，磁盘或带宽吃不消 | CDAAC 只有日包，没有单文件 URL；AWS 镜像没有这类产品 | 流式 `tarfile` 读到需要的成员就停（3.4：163,840 B 拿到 3 个文件） |
| 13 | 地方时分布均匀，但高纬度一条也没有 | COSMIC-2 轨道倾角 24°，峰值点只到 ±40.5° | 高纬度剖面用 COSMIC-1 / Spire / 其他任务（同一棵树的其他目录） |

## 8. 选型对比

| 需求 | 用什么 |
| --- | --- |
| COSMIC-2 Ne 剖面 / 链路 TEC 直连下载 + 读取 | **本手册 cosmic2-ro** |
| COSMIC-1 ionPrf / ionPhs 进 pysat | [pysatcdaac](./pysatcdaac.md) |
| AWS 上的中性大气 RO（calibratedPhase / refractivity / atmospheric） | [awsgnssroutils](./awsgnssroutils.md) |
| JPL COSMIC-1 大气 L2 | [cosmic-crunch](./cosmic-crunch.md) |
| 掩星几何（切点在哪） | [gmat](./gmat.md) |
| 门户门槛 / 登录情况总表 | [data-access 决策表 E19–E20](../data-access.md#dp-e19) |
