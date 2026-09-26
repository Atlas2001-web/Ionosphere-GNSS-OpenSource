# COSMIC-2 以外的掩星数据 · CDAAC（MetOp / Spire / GRACE / CHAMP / GeoOptics）+ ROM SAF

入口：UCAR CDAAC 公开树 <https://data.cosmic.ucar.edu/gnss-ro/> · ionPrf 格式说明 <https://cdaac-www.cosmic.ucar.edu/cdaac/cgi_bin/fileFormats.cgi?type=ionPrf> · AWS 镜像 <https://gnss-ro-data.s3.amazonaws.com/index.html> · ROM SAF <https://rom-saf.eumetsat.int/> · 本机验证 **2026-09-26 06:28–06:31 EDT**（匿名：CDAAC 全树和 AWS 列表无账号；ROM SAF 产品库只探到登录提示）

> 岗位：COSMIC-2 以外任务的**电离层**掩星产品去哪拿、哪些任务根本没有电子密度剖面、ionPrf 怎么读。COSMIC-2 的 ionPrf / podTc2 目录、时延和质量筛选见 [cosmic2-ro.md](./cosmic2-ro.md)，本文不重复。门槛总表 [电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E35](../data-access.md#dp-e35) · 冲突时以决策表和 CDAAC 当日目录为准。

---

## 1 用途与边界

| 做 | 不做 |
|---|---|
| 盘点 CDAAC 各任务 level2 年份范围，以及样本日有没有 `ionPrf` | 不讲 COSMIC-2（见 [cosmic2-ro.md](./cosmic2-ro.md)） |
| 读 ionPrf：CHAMP 2003-10-29 万圣节暴、GRACE 2014-03-01 | 不注册 ROM SAF，不从商业渠道买 Spire 数据 |
| 读 MetOp-C `podTec`（2024-05-11 暴日链路 TEC） | 不做 Abel 反演，也不做中性大气 atmPrf 分析 |

**结论先说**

| 任务 | CDAAC 有 ionPrf（Ne 剖面）？ | 电离层可用 | 门槛 |
|---|---|---|---|
| MetOp-A/B/C | **没有**（level2 只有中性大气） | level1b `podTec`：定轨天线向上看的链路 TEC | 匿名 |
| Spire（NOAA 采购部分） | **没有** | level1b `podTec`，2024-05-11 一天 433 MB | 匿名 |
| PlanetiQ（NOAA） | **没有** | — | 匿名 |
| GRACE（2007–2017） | **有** | ionPrf | 匿名 |
| CHAMP（2001–2008） | **有** | ionPrf（repro2016） | 匿名 |
| GeoOptics（NOAA，2020–2021） | **有** | ionPrf | 匿名 |
| **GRACE-FO** | CDAAC 树上没有这个任务（`gracefo/` 404） | 本文没找到匿名来源 | — |
| ROM SAF | 只有中性大气产品 | AWS 上有 champ / cosmic1 / grace / metop 镜像（中性大气） | 产品库**须登录**；AWS 镜像匿名 |

## 2 安装

不用 netCDF4。ionPrf 和 podTec 都是 netCDF3 classic，`scipy.io.netcdf_file` 就能读。

```bash
unset TMPDIR VIRTUAL_ENV LD_LIBRARY_PATH
/usr/bin/python3 -c "import scipy, numpy; print(scipy.__version__, numpy.__version__)"   # 本机 numpy 2.2.4 + scipy
```

## 3 真命令 + 期望输出

### 3.1 CDAAC 任务盘点、GRACE-FO、AWS、ROM SAF

```bash
#!/usr/bin/env bash
# CDAAC 公开树：各任务 level2 年份范围、样本日有没有 ionPrf；GRACE-FO；AWS gnss-ro-data；ROM SAF 门槛
B=https://data.cosmic.ucar.edu/gnss-ro
L(){ curl -s -m 60 "$B/$1" | grep -oE 'href="[^"?]*"' | sed 's/href=//;s/"//g' | grep -v '^\.\./'; }
echo "CDAAC 任务目录: $(L '' | tr -d / | tr '\n' ' ')"
for m in metopa/postProc metopb/postProc metopc/postProc spire/noaa/nrt planetiq/noaa/postProc geoopt/noaa/postProc champ/repro2016 grace/postProc; do
  ys=$(L $m/level2/); y=$(echo "$ys" | tail -1); d=$(L $m/level2/$y | tail -1)
  echo "$m  level2 $(echo "$ys" | head -1 | tr -d /)–${y%/}  样本 ${y}${d%/}: $(L $m/level2/$y$d | sed 's/_.*//' | sort -u | tr '\n' ' ')"
done
for p in metopc/postProc/level1b/2024/132/ spire/noaa/nrt/level1b/2024/132/; do
  echo "$p → $(curl -s -m 60 $B/$p | sed 's/<[^>]*>/ /g' | grep -oE 'podTec\S+ +\S+ +\S+ +\S+' | awk '{print $1, $4}')"; done
echo "Spire NOAA nrt 2024 天目录: $(L spire/noaa/nrt/level2/2024/ | head -1 | tr -d /)–$(L spire/noaa/nrt/level2/2024/ | tail -1 | tr -d /)，共 $(L spire/noaa/nrt/level2/2024/ | wc -l) 天"
for m in gracefo gracefoc; do echo "$(curl -s -o /dev/null -w '%{http_code}' $B/$m/) $B/$m/"; done
S="https://gnss-ro-data.s3.amazonaws.com/?list-type=2&delimiter=/&prefix="
for p in contributed/v1.1/ucar/metop/ contributed/v1.1/ucar/spire/ contributed/v1.1/romsaf/; do
  echo "AWS $p: $(curl -s "$S$p" | grep -o '<Prefix>[^<]*' | sed "s|<Prefix>$p||" | grep . | tr '\n' ' ')"; done
echo "ROM SAF 产品归档页: $(curl -s -m 30 https://rom-saf.eumetsat.int/product_archive.php | sed 's/<[^>]*>/ /g; s/&nbsp;/ /g' | grep -oE 'Please +login +or +register +first' | head -1)"
```

实测输出：

```text
CDAAC 任务目录: champ cnofs cosmic1 cosmic2 fid geoopt gpsmet gpsmetas grace gridded kompsat5 metopa metopb metopc paz planetiq publications sacc spire tdx tsx 
metopa/postProc  level2 2016–2021  样本 2021/331: atmPrf bfrPrf echPrf er5Prf gfsPrf wetPf2 wetPrf 
metopb/postProc  level2 2016–2026  样本 2026/090: atmPrf bfrPrf echPrf er5Prf gfsPrf wetPf2 wetPrf 
metopc/postProc  level2 2019–2026  样本 2026/090: atmPrf bfrPrf echPrf er5Prf gfsPrf wetPf2 wetPrf 
spire/noaa/nrt  level2 2020–2026  样本 2026/268: atmPrf avnPrf bfrPrf echPrf sktPlt/ spectr/ wetPf2 
planetiq/noaa/postProc  level2 2023–2024  样本 2024/305: atmPrf avnPrf bfrPrf echPrf wetPf2 
geoopt/noaa/postProc  level2 2020–2021  样本 2021/259: atmPrf bfrPrf echPrf er5Prf gfsPrf ionPrf wetPf2 wetPrf 
champ/repro2016  level2 2001–2008  样本 2008/279: atmPrf bfrPrf ecmPrf gfsPrf ionPrf wetPf2 
grace/postProc  level2 2007–2017  样本 2017/334: atmPrf bfrPrf eraPrf gfsPrf ionPrf wetPrf 
metopc/postProc/level1b/2024/132/ → podTec_postProc_2024_132.tar.gz 36M
spire/noaa/nrt/level1b/2024/132/ → podTec_nrt_2024_132.tar.gz 433M
Spire NOAA nrt 2024 天目录: 016–366，共 351 天
404 https://data.cosmic.ucar.edu/gnss-ro/gracefo/
404 https://data.cosmic.ucar.edu/gnss-ro/gracefoc/
AWS contributed/v1.1/ucar/metop/: atmosphericRetrieval/ calibratedPhase/ refractivityRetrieval/ 
AWS contributed/v1.1/ucar/spire/: atmosphericRetrieval/ calibratedPhase/ refractivityRetrieval/ 
AWS contributed/v1.1/romsaf/: champ/ cosmic1/ grace/ metop/ 
ROM SAF 产品归档页: Please  login   or  register   first
```

样本日取的是各任务 level2 的**最后一天**。只看一天有局限，但 MetOp-C 的 2024/132 我也逐个列过：level2 只有 atmPrf / bfrPrf / echPrf / er5Prf / gfsPrf / wetPf2 / wetPrf，level1b 只有 atmPhs / leoClk / leoOrb / podTec。

### 3.2 下载三个日包

```bash
B=https://data.cosmic.ucar.edu/gnss-ro
curl -s -O -w "%{http_code} %{size_download} %{time_total}s\n" $B/champ/repro2016/level2/2003/302/ionPrf_repro2016_2003_302.tar.gz
curl -s -O -w "%{http_code} %{size_download} %{time_total}s\n" $B/grace/postProc/level2/2014/060/ionPrf_postProc_2014_060.tar.gz
curl -s -O -w "%{http_code} %{size_download} %{time_total}s\n" $B/metopc/postProc/level1b/2024/132/podTec_postProc_2024_132.tar.gz
# 实测：
# 200 703381 0.85s     → 117 个成员，如 ionPrf_CHAM.2003.302.00.44.G01_2016.2430_nc
# 200 362978 0.75s     → 72 个成员，如 ionPrf_GRC1.2014.060.00.41.G29_2010.2640_nc
# 200 37274050 1.85s   → 398 个成员，如 podTec_MTPC.2024.132.23.43.0027.G02.00_2023.1110_nc
```

### 3.3 读 ionPrf 和 podTec（直接从 tar 里读，不解包）

```python
# 读 ionPrf（CHAMP 2003-10-29 万圣节暴、GRACE 2014-03-01）和 MetOp-C podTec（2024-05-11）；只用 scipy.io.netcdf_file（netCDF3 classic）
import glob, tarfile, io, datetime as dt, numpy as np
from scipy.io import netcdf_file
GPS0 = dt.datetime(1980, 1, 6)
def members(tgz):
    with tarfile.open(tgz) as t:
        for m in t.getmembers():
            yield m.name, netcdf_file(io.BytesIO(t.extractfile(m).read()), 'r', mmap=False)
def s(x): return x.decode() if isinstance(x, bytes) else x
for tgz in ('ionPrf_repro2016_2003_302.tar.gz', 'ionPrf_postProc_2014_060.tar.gz'):
    rows = []
    for name, d in members(tgz):
        a = d._attributes; z = d.variables['MSL_alt'][:].copy(); ne = d.variables['ELEC_dens'][:].copy()
        rows.append((name, a['edmax'], a['edmaxalt'], a['topalt'], a['critfreq'], a['edmaxlat'], z.size, ne.max(), z[ne.argmax()], s(a['mission'])))
    ok = [r for r in rows if 150 <= r[2] <= 500 and r[2] < r[3] - 10]   # 本文口径：峰高在 150–500 km 且不贴着剖面顶
    e = np.array([r[1] for r in ok]); h = np.array([r[2] for r in ok])
    print(f'{tgz}: {len(rows)} 条剖面（{rows[0][9]}），每条 {min(r[6] for r in rows)}–{max(r[6] for r in rows)} 层；本文口径可用 {len(ok)} 条')
    print(f'  NmF2(edmax) 中位 {np.median(e):,.0f} 最大 {e.max():,.0f} el/cm³；hmF2 中位 {np.median(h):.0f} km；foF2(critfreq) 最大 {max(r[4] for r in ok):.2f} MHz')
    bad = [r for r in rows if abs(r[7] - r[1]) > 1]
    print(f'  全局属性 edmax 与剖面 max(ELEC_dens) 不一致: {len(bad)} 条' + (f'，这些剖面的原始最大值所在高度 {sorted(round(r[8]) for r in bad)} km' if bad else ''))
name, d = next(members('ionPrf_repro2016_2003_302.tar.gz'))
a = d._attributes; z = d.variables['MSL_alt'][:]; ne = d.variables['ELEC_dens'][:]; tec = d.variables['TEC_cal'][:]
t = GPS0 + dt.timedelta(seconds=float(a['edmaxtime']))
print(f'\n样例 {name}: 变量 {list(d.variables)}；时间 {t:%Y-%m-%d %H:%M:%S} UT（edmaxtime 是 GPS 秒，未减闰秒）；峰点 {a["edmaxlat"]:.2f}°N {a["edmaxlon"]:.2f}°E，LT {a["edmaxlct"]:.2f} h')
print(f'  edmax {a["edmax"]:,.0f} el/cm³ @ {a["edmaxalt"]:.1f} km；critfreq {a["critfreq"]:.3f} MHz；复核 8.98e-3*sqrt(edmax) = {8.98e-3*np.sqrt(a["edmax"]):.3f} MHz')
for hh in (100, 200, 300, 326, 390):
    i = np.abs(z - hh).argmin(); print(f'  MSL_alt {z[i]:6.1f} km  ELEC_dens {ne[i]:10,.0f}  TEC_cal {tec[i]:6.2f} TECU')
el = []; oh = []; tm = []; n = 0
for name, d in members('podTec_postProc_2024_132.tar.gz'):
    n += 1; el.append(d.variables['elevation'][:].copy()); oh.append(d.variables['occheight'][:].copy()); tm.append(d.variables['TEC'][:].copy())
el, oh, tm = map(np.concatenate, (el, oh, tm))
print(f'\npodTec_postProc_2024_132（MetOp-C）: {n} 条链路弧，{el.size:,} 个 1 Hz 点；elevation {el.min():.1f}…{el.max():.1f}°，负仰角点 {int((el < 0).sum())}；occheight 为 -999 填充的点 {int((oh == -999).sum()):,}；TEC {np.nanmin(tm):.1f}…{np.nanmax(tm):.1f} TECU（相对值，需加 leveling_offset + DCB）')
```

实测输出：

```text
ionPrf_repro2016_2003_302.tar.gz: 117 条剖面（CHAMP），每条 196–301 层；本文口径可用 66 条
  NmF2(edmax) 中位 543,098 最大 3,371,960 el/cm³；hmF2 中位 333 km；foF2(critfreq) 最大 16.49 MHz
  全局属性 edmax 与剖面 max(ELEC_dens) 不一致: 6 条，这些剖面的原始最大值所在高度 [6, 21, 61, 67, 69, 80] km
ionPrf_postProc_2014_060.tar.gz: 72 条剖面（GRACE），每条 169–330 层；本文口径可用 66 条
  NmF2(edmax) 中位 884,731 最大 3,123,072 el/cm³；hmF2 中位 327 km；foF2(critfreq) 最大 15.87 MHz
  全局属性 edmax 与剖面 max(ELEC_dens) 不一致: 0 条

样例 ionPrf_CHAM.2003.302.00.44.G01_2016.2430_nc: 变量 ['MSL_alt', 'GEO_lat', 'GEO_lon', 'OCC_azi', 'TEC_cal', 'ELEC_dens']；时间 2003-10-29 00:42:05 UT（edmaxtime 是 GPS 秒，未减闰秒）；峰点 51.81°N 7.40°E，LT 1.19 h
  edmax 92,245 el/cm³ @ 326.3 km；critfreq 2.727 MHz；复核 8.98e-3*sqrt(edmax) = 2.727 MHz
  MSL_alt  100.9 km  ELEC_dens      6,465  TEC_cal  10.44 TECU
  MSL_alt  200.4 km  ELEC_dens     16,893  TEC_cal  12.61 TECU
  MSL_alt  299.9 km  ELEC_dens     62,729  TEC_cal  17.29 TECU
  MSL_alt  326.3 km  ELEC_dens     92,245  TEC_cal  16.10 TECU
  MSL_alt  390.3 km  ELEC_dens     85,951  TEC_cal   4.59 TECU

podTec_postProc_2024_132（MetOp-C）: 398 条链路弧，586,366 个 1 Hz 点；elevation 10.0…89.9°，负仰角点 0；occheight 为 -999 填充的点 586,366；TEC -1.3…80.1 TECU（相对值，需加 leveling_offset + DCB）
```

读法：
- `critfreq` 就是 `8.98e-3·√edmax`（edmax 单位 el/cm³，结果 MHz），可以直接当 foF2 和测高仪比（[教程 07](../tutorials/07-ionosonde-occultation.md)）。
- CHAMP 暴日 117 条里只有 66 条过了本文口径（峰高在 150–500 km，且不贴着剖面顶），GRACE 平静日是 72 条过 66 条。暴时剖面质量明显更差。
- 6 条 CHAMP 剖面的原始最大值落在 6–80 km（下层反演发散），全局属性 `edmax` 没取这些点。所以**用 `edmax/edmaxalt`，不要直接取 `max(ELEC_dens)`**。
- MetOp-C 的 podTec 仰角全在 10–90°，没有负仰角点，`occheight` 全是 −999：这是**LEO 以上（约 820 km）的顶部 TEC**，不是掩星切向链路，不能拿来做 Ne 剖面。

## 4 输入 / 输出

| 产品 | 路径模式 | 单文件 | 关键变量 / 属性 |
|---|---|---|---|
| ionPrf（CHAMP） | `champ/repro2016/level2/YYYY/DDD/ionPrf_repro2016_YYYY_DDD.tar.gz` | `ionPrf_CHAM.YYYY.DDD.HH.MM.Gnn_2016.2430_nc` | 维度 `MSL_alt`（196–301 层）；变量 `MSL_alt`(km)、`GEO_lat/GEO_lon`、`OCC_azi`、`TEC_cal`(TECU，LEO 以下)、`ELEC_dens`(el/cm³)；属性 `edmax/edmaxalt/edmaxlat/edmaxlon/edmaxlct/edmaxtime`、`critfreq`、`topalt`、`botalt`、`hscale`、`inverter`=gmrion、`creation_time` |
| ionPrf（GRACE） | `grace/postProc/level2/YYYY/DDD/ionPrf_postProc_YYYY_DDD.tar.gz` | `ionPrf_GRC1.…_nc` | 同上 |
| ionPrf（GeoOptics） | `geoopt/noaa/postProc/level2/YYYY/DDD/` | 2021/259 日包 320 KB | 同上（本文未解读） |
| podTec（MetOp / Spire） | `metop?/postProc/level1b/YYYY/DDD/podTec_postProc_…`、`spire/noaa/nrt/level1b/…/podTec_nrt_…` | 每条 LEO–GNSS 弧一个文件；1 Hz | `time`(GPS 秒)、`TEC`(TECU，相对值)、`elevation`、`caL1_SNR/pL2_SNR`、`x/y/z_LEO`、`x/y/z_GPS`、`leveling_offset`；属性 `gpsdcb/leodcb`、`leveling_err`、`tecmax`、`lat_tecmax` 等 |
| AWS gnss-ro-data | `contributed/v1.1/{ucar,romsaf,jpl,eumetsat}/<mission>/…` | 逐掩星 netCDF | 只有 calibratedPhase / refractivityRetrieval / atmosphericRetrieval，**没有电离层**（见 [awsgnssroutils.md](./awsgnssroutils.md)） |

## 5 参数

| 项 | 取值 | 说明 |
|---|---|---|
| 任务目录 | `metopa/b/c/postProc`、`spire/noaa/nrt`、`grace/postProc`、`champ/repro2016`、`geoopt/noaa/postProc` | 各任务的处理级别目录不一样，要逐个 `curl` 看 |
| DDD | 年积日，三位 | 2024-05-11 = 132，2003-10-29 = 302 |
| 本文筛选口径 | `150 ≤ edmaxalt ≤ 500` 且 `edmaxalt < topalt − 10` | 本文自选；COSMIC-2 的更完整筛法见 [cosmic2-ro.md](./cosmic2-ro.md) |
| 时间 | `edmaxtime` 等是 GPS 秒（1980-01-06 起） | 本文换算未扣闰秒，和全局属性 year…second 对得上；要秒级精度自己核对 |

## 6 接到哪一步

- 测高仪 / 掩星对比：[教程 07](../tutorials/07-ionosonde-occultation.md)。`critfreq` 对 foF2，`edmaxalt` 对 hmF2。
- 历史暴对比：CHAMP 2003 万圣节暴、GRACE 2007–2017，用来补 COSMIC-2（2019 年以后）之前的年份。
- 批量下载 AWS 中性大气产品：[awsgnssroutils.md](./awsgnssroutils.md)。本地大批量处理：[cosmic-crunch.md](./cosmic-crunch.md)。
- COSMIC-2 ionPrf：[cosmic2-ro.md](./cosmic2-ro.md)，同一段读代码可以直接复用。

## 7 坑

| # | 现象 | 原因 | 修复 |
|---|---|---|---|
| 1 | 在 MetOp / Spire 目录里找不到 ionPrf | CDAAC 对这几个任务只做中性大气 level2 | 电离层只有 level1b `podTec`；要 Ne 剖面就用 CHAMP / GRACE / GeoOptics / COSMIC |
| 2 | 把 MetOp podTec 当掩星 TEC | 仰角全部为正，`occheight` 全是 −999 | 当顶部 TEC（LEO 以上）用，或者用来做 LEO 以上等离子层研究 |
| 3 | podTec 的 TEC 有负值 | 是相对 TEC | 绝对值 = TEC + `leveling_offset` + GNSS DCB + LEO DCB（变量说明原文） |
| 4 | `max(ELEC_dens)` 落在 6–80 km | 下层 Abel 反演发散 | 用全局属性 `edmax/edmaxalt` 并加高度筛选 |
| 5 | 找 `gracefo/` 返回 404 | CDAAC 公开树没有 GRACE-FO | 本文未找到匿名的 GRACE-FO 电离层剖面，别再在 CDAAC 上找 |
| 6 | Spire podTec 一天 433 MB | 星座规模大 | 先按需挑时段；本文没下 Spire 的包 |
| 7 | Spire NOAA 2024 年只有 351 个天目录（016–366） | 2024 年目录从 016 开始，原因本文未核实 | 选研究日之前先列目录 |
| 8 | ROM SAF 产品归档页显示 “Please login or register first” | 产品库要账号 | 中性大气产品走 AWS `contributed/v1.1/romsaf/` 镜像（[E5](../data-access.md#dp-e5)）；ROM SAF 不提供 Ne 剖面 |
| 9 | 装 netCDF4 失败 | 其实不需要 | ionPrf / podTec 是 netCDF3 classic，用 `scipy.io.netcdf_file` 读 |
| 10 | 日包只能整包下，没有单文件 URL | CDAAC 树只放 `.tar.gz` | 用 `tarfile` 在内存里逐个读（见 3.3），不用落盘解包 |
| 11 | 字符串属性是 bytes | scipy 返回 `b'CHAMP'` | 用 `.decode()` |

## 8 选型

| 需求 | 选 |
|---|---|
| 2019 年以后的低纬 Ne 剖面 | [cosmic2-ro.md](./cosmic2-ro.md) |
| 2001–2017 年的历史 Ne 剖面 | CHAMP repro2016 / GRACE postProc ionPrf（本文） |
| 2024 暴日有 LEO 视角的 TEC | MetOp-B/C podTec（每天约 36 MB）；Spire podTec 量大（每天约 433 MB） |
| 中性大气（折射率、温湿） | AWS gnss-ro-data + [awsgnssroutils.md](./awsgnssroutils.md) |
| GRACE-FO 电离层 | 本文没找到匿名来源 |
