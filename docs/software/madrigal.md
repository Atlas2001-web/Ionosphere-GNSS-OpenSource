# Madrigal（CEDAR / EISCAT / SRI AMISR）· 找实验与下载 操作手册

目录：门户 <https://cedar.openmadrigal.org/> · 客户端 [MITHaystack/madrigalWeb](https://github.com/MITHaystack/madrigalWeb)（PyPI **madrigalWeb 3.3.8**，MIT）· 项目页 [OpenMadrigal](https://openmadrigal.org/) · 本机验证 **2026-09-26 03:15–03:25 EDT**；**质检复跑** 03:28–03:35 EDT：CPython 3.13.5 venv，`madrigalWeb 3.3.8` + `h5py 3.16.0` + `numpy 2.5.3`；TEC **13257658 B**/tec=**32.0**/dtec=**1.1**/valid=**2949**；isprint 45.06 TECU；PFISR **2817905 B**/popl **11.937** @310.6 km；`globalDownload` site **116355/134718 B**；错路径 **100 B** HTML；HEAD 2024-05-10 **155853792 B**。

> 岗位：把 **MIT Haystack 全球 GNSS TEC 图**和**非相干散射雷达（ISR）剖面**从 Madrigal 拉到本地 HDF5。它**不算 TEC**、不读 RINEX，也不做 ISR 反演。  
> 门户门槛与其它数据源的比较见 [data-access 决策表](../data-access.md#电离层与地磁门户决策表)：[E3 CEDAR](../data-access.md#dp-e3) · [E1 EISCAT](../data-access.md#dp-e1) · [E2 AMISR](../data-access.md#dp-e2)。  
> 冲突时：**本机 `help(madrigalWeb.madrigalWeb.MadrigalData)` / 上游 README > 本文**。

## 1. 它解决什么，边界在哪

Madrigal 是一套分布式数据库软件，每个机构各跑一台实例，接口完全相同（CGI 服务 + 相同的 HDF5 布局）。本文用到三台：

| 实例 | 基址（给 `MadrigalData` / curl 用） | 服务端版本（`getVersionService.py`） | 本文用的仪器码 kinst |
| --- | --- | --- | --- |
| CEDAR（MIT Haystack，NSF） | `https://cedar.openmadrigal.org` | 3.2 | **8000** World-wide GNSS Receiver Network（全球 TEC） |
| EISCAT | `https://madrigal.eiscat.se/madrigal` | 3.2 | 72 Tromsø UHF（另有 74 VHF、95 ESR） |
| SRI（AMISR） | `https://data.amisr.com/madrigal` | **2.6** | 61 PFISR（91 RISR-N） |

- **账号**：三台都不要账号。但下载 / isprint 必须填 `user_fullname` / `user_email` / `user_affiliation` 三个字段，服务端只记录、不校验（请写真实信息，方便数据方统计）。
- **管得到的**：列仪器 → 按时间找实验 → 列文件 → 整文件下载（HDF5），或者在服务端按参数 / 范围过滤后只取 ASCII 文本（isprint）。
- **管不到的**：
  - EISCAT 门户里的 L2（要 EGI Check-in）；
  - SuperDARN（去 [FRDR](../data-access.md#dp-e6)）；
  - IONEX 格式 GIM（去 [ionex-gim](./ionex-gim.md)）；
  - 从 RINEX 自己算 TEC（去 [gnss-tec](./gnss-tec.md)）。

## 2. 安装

```bash
python3 -m venv ~/iono_ops/mad-venv && . ~/iono_ops/mad-venv/bin/activate
pip install madrigalWeb h5py          # 本机几秒；venv 100 MB（大头是 numpy/h5py）
pip list | grep -iE 'madrigal|h5py|numpy'
# h5py        3.16.0
# madrigalWeb 3.3.8
# numpy       2.5.3
ls $VIRTUAL_ENV/bin | grep -i global
# globalCitation.py  globalDownload.py  globalIsprint.py
```

只用 curl 的话什么都不用装。读 HDF5 只需要 h5py。

## 3. 真实命令与输出

### 3.1 三台实例找实验、列文件（`find.py`）

```python
import madrigalWeb.madrigalWeb as mw, time
for url, kinst in [("https://cedar.openmadrigal.org", 8000),
                   ("https://madrigal.eiscat.se/madrigal", 72),
                   ("https://data.amisr.com/madrigal", 61)]:
    t0 = time.time()
    m = mw.MadrigalData(url)
    exps = m.getExperiments(kinst, 2024,5,10,0,0,0, 2024,5,17,23,59,59)
    exps.sort(key=lambda e: (e.startyear, e.startmonth, e.startday))
    print(url, "kinst", kinst, "n_exp", len(exps), "%.0f s" % (time.time()-t0))
    e = exps[0]
    print("  ", e.id, e.name, "%d-%02d-%02d" % (e.startyear, e.startmonth, e.startday), e.url)
    for f in m.getExperimentFiles(e.id)[:3]:
        print("    ", f.name.split("/")[-1], f.kindat, f.kindatdesc, f.category, f.status)
```

```text
https://cedar.openmadrigal.org kinst 8000 n_exp 9 28 s
   100011063 World-wide TEC from GPS/GLONASS 2024-05-09 https://cedar.openmadrigal.org/madtoc/experiments4/2024/gps/09may24
     gps240509g.002.hdf5 3500 TEC binned 1 degree by 1 degree by 5 min 1 final
     los_20240509.001.h5 3505 Line of sight TEC data 1 Final
     site_20240509.001.h5 3506 List of sites used in daily TEC data 1 Final
https://madrigal.eiscat.se/madrigal kinst 72 n_exp 1 6 s
   20021968 2024-05-16_manda@uhf 2024-05-16 https://madrigal.eiscat.se/madrigal/madtoc/experiments/2024/tro/16may24
     MAD6400_2024-05-16_manda_60@uhf.hdf5 6400 GUISDAP params 0 1 Final
     MAD6300_2024-05-16_manda_60@uhf.hdf5 6300 GUISDAP pp resolution 0 1 Final
https://data.amisr.com/madrigal kinst 61 n_exp 32 2 s
   30001786 MSWinds27H.v03 - D-region E-region F-region local measurements 2024-05-09 http://data.amisr.com/madrigal/madtoc/experiments0/2024/pfa/09may24d
     pfa20240509.004_bc_nenotr_01min.001.h5 1000301 Ne From Power - Barker/MPS Code (D-region) - 1 min 1 final
     pfa20240509.004_bc_nenotr_03min.001.h5 1000303 Ne From Power - Barker/MPS Code (D-region) - 3 min 1 final
     pfa20240509.004_bc_nenotr_05min.001.h5 1000305 Ne From Power - Barker/MPS Code (D-region) - 5 min 1 final
```

查询从 05-10 开始，结果里却有 05-09 开始的实验：查询按**时间重叠**匹配（见坑 3）。CEDAR 上 `getExperiments` 要 28 s，比另外两台慢一个量级。

### 3.2 下载 GNSS TEC 文件（instrument 8000）并读一个格点

要一个小样例，就挑早年的日文件：同一 kinst 下 2000-01-01 的 TEC 格网 13 MB，2010-01-01 的 24 MB，2003-10-30 的 49 MB，2024-05-10 的 **156 MB**（HEAD `Content-Length`=**155853792**）。

```bash
curl -L -o gps000101g.001.hdf5 -w "%{http_code} %{size_download}\n" \
 "https://cedar.openmadrigal.org/getMadfile.cgi?fileName=/opt/openmadrigal/madroot/experiments3/2000/gps/01jan00/gps000101g.001.hdf5&fileType=-2&user_fullname=Your+Name&user_email=you@example.org&user_affiliation=Your+Org"
# 200 13257658     （1.5 s；文件头 \x89HDF）
```

`fileName` 必须是 `getExperimentFiles` 返回的**服务器绝对路径**。把 `experiments3` 猜成 `experiments4` 时，同样回 **200**，但正文只有 100 B：`<p>fileName … not found<p>`（坑 1）。

`point.py`：取 42°N、72°W、2000-01-01 18:00 UT 这一格：

```python
import h5py, numpy as np, datetime as dt
f = h5py.File("gps000101g.001.hdf5", "r")
A = f["Data/Array Layout"]
lat, lon, ts = A["gdlat"][:], A["glon"][:], A["timestamps"][:]
tec, dtec = A["2D Parameters/tec"], A["2D Parameters/dtec"]
i = np.argmin(abs(lat - 42)); j = np.argmin(abs(lon - (-72)))
k = np.argmin(abs(ts - dt.datetime(2000,1,1,18,0,tzinfo=dt.timezone.utc).timestamp()))
print("grid", lat[i], lon[j], dt.datetime.fromtimestamp(int(ts[k]), dt.timezone.utc))
print("tec", tec[i, j, k], "dtec", dtec[i, j, k])
print("valid cells at this time:", int(np.isfinite(tec[:, :, k]).sum()))
T = f["Data/Table Layout"][:]          # 同一格在表布局里的原始行
m = (T["gdlat"]==lat[i]) & (T["glon"]==lon[j]) & (T["ut1_unix"]==ts[k])
print(T[m][["hour","min","gdlat","glon","tec","dtec","ut1_unix","ut2_unix"]])
```

```text
grid 42.0 -72.0 2000-01-01 18:00:00+00:00
tec 32.0 dtec 1.1
valid cells at this time: 2949
[(18., 2., 42., -72., 32., 1.1, 9.467496e+08, 9.467499e+08)]
```

- 这一时刻 64800 个格子里只有 2949 个有值。全天 `tec` 的有限值比例是 **0.043**。18:00 这一刻的有值格子里，56% 落在北美经度带（−170°～−50°），23% 落在欧洲（−20°～45°），82% 在北半球；其余格子都是 NaN。
- 表布局那一行的 `min` 是 2（完整为 18:02:30），而 `timestamps` 是 18:00:00：`timestamps` 用的是 `ut1_unix`（格子起点），`year…sec` 这几列是区间**中点**（坑 5）。

### 3.3 不下整文件：服务端 isprint 抽单格（2024-05-10 Gannon 暴日）

整文件 156 MB，但只要一个点时，在服务端过滤后只取文本：

```python
import madrigalWeb.madrigalWeb as mw
m = mw.MadrigalData("https://cedar.openmadrigal.org")
out = m.isprint("/opt/openmadrigal/madroot/experiments4/2024/gps/10may24/gps240510g.002.hdf5",
     "year,month,day,hour,min,sec,gdlat,glon,tec,dtec",
     "date1=05/10/2024 time1=18:00:00 date2=05/10/2024 time2=18:05:00 filter=gdlat,41.9,42.1 filter=glon,-72.1,-71.9",
     "Your Name", "you@example.org", "Your Org")
print(out)
```

```text
     2024         5        10        18         2        30     42.00     -72.00   4.50605e+01   2.27783e-01
     2024         5        10        18         7        30     42.00     -72.00   4.38668e+01   2.14246e-01
```

用时 12.8 s。`time2=18:05:00` 把从 18:05 开始的下一格也包了进来；只要一格就写 `18:04:59`。同一格同一时刻：2000-01-01 为 32.0 TECU，2024-05-10 为 45.06 TECU。

同样的请求用纯 curl（`parms` **要逐个重复**，写成一个逗号串会报错，见坑 6）：

```bash
curl -s -G "https://cedar.openmadrigal.org/isprintService.py" \
  --data-urlencode "file=/opt/openmadrigal/madroot/experiments4/2024/gps/10may24/gps240510g.002.hdf5" \
  $(for p in year month day hour min sec gdlat glon tec dtec; do echo "-d parms=$p"; done) \
  --data-urlencode "filters=date1=05/10/2024 time1=18:00:00 date2=05/10/2024 time2=18:04:59 filter=gdlat,41.9,42.1 filter=glon,-72.1,-71.9" \
  --data-urlencode "user_fullname=Your Name" --data-urlencode "user_email=you@example.org" \
  --data-urlencode "user_affiliation=Your Org"
#      2024         5        10        18         2        30     42.00     -72.00   4.50605e+01   2.27783e-01
```

### 3.4 ISR 文件：PFISR 5 min 电子密度（SRI 实例）

```bash
curl -L -o pfisr.h5 -w "%{http_code} %{size_download}\n" \
 "https://data.amisr.com/madrigal/getMadfile.cgi?fileName=/opt/madrigal/madrigal3/experiments0/2024/pfa/04may24c/pfa20240504.003_ac_nenotr_05min.001.h5&fileType=-2&user_fullname=Your+Name&user_email=you@example.org&user_affiliation=Your+Org"
# 200 2817905
```

`isr.py`：

```python
import h5py, numpy as np, datetime as dt
f = h5py.File("pfisr.h5", "r")
A = f["Data/Array Layout"]
for name in A:                                  # 组名末尾带空格
    g = A[name]; print(repr(name), "elm=%.1f azm=%.1f" % (g["1D Parameters/elm"][0], g["1D Parameters/azm"][0]))
g = A["Array with beamid=64016 "]
rng, ts, popl = g["range"][:], g["timestamps"][:], g["2D Parameters/popl"][:]
k = 40; col = popl[:, k]; i = np.nanargmax(col)
print(dt.datetime.fromtimestamp(int(ts[k]), dt.timezone.utc), "range %.1f km" % rng[i], "popl %.3f -> Ne %.3e m^-3" % (col[i], 10**col[i]))
```

```text
'Array with beamid=64016 ' elm=90.0 azm=14.0
'Array with beamid=64157 ' elm=77.5 azm=-154.3
'Array with beamid=64964 ' elm=66.1 azm=-34.7
'Array with beamid=65066 ' elm=65.6 azm=75.0
2024-05-04 14:58:54+00:00 range 310.6 km popl 11.937 -> Ne 8.650e+11 m^-3
```

`popl` 在元数据里写的是 `Log10(uncorrected electron density)`，单位 `lg(m-3)`：它是功率反推的**未做温度比修正**的 Ne，要 Ne/Te/Ti 就选 `_fit_` 文件。EISCAT 文件的下法完全相同（[E1](../data-access.md#dp-e1)：`MAD6400_…_60@uhf.hdf5`，7342985 B）。

### 3.5 批量：`globalDownload.py`

```bash
python $VIRTUAL_ENV/bin/globalDownload.py --url=https://cedar.openmadrigal.org --outputDir=gd \
  --user_fullname="Your Name" --user_email=you@example.org --user_affiliation="Your Org" \
  --format=hdf5 --startDate=05/10/2024 --endDate=05/10/2024 --inst=8000 --kindat=3506 --verbose
```

```text
Analyzed exp url https://cedar.openmadrigal.org/madtoc/experiments4/2024/gps/09may24
Analyzed exp url https://cedar.openmadrigal.org/madtoc/experiments4/2024/gps/10may24
2 files being downloaded
Downloading file 1 of 2: /opt/openmadrigal/madroot/experiments4/2024/gps/09may24/site_20240509.001.h5
Downloaded file gd/site_20240509.001.h5.hdf5
Downloading file 2 of 2: /opt/openmadrigal/madroot/experiments4/2024/gps/10may24/site_20240510.002.h5
Downloaded file gd/site_20240510.002.h5.hdf5
```

- 用时 33 s；两个文件分别为 116355 B 和 134718 B。
- 只要了一天，却下到两个文件（重叠匹配，坑 3），而且文件名被追加了 `.hdf5`（坑 7）。
- `site_…` 文件的表布局有 5648 行，列为 `gps_site, gdlatr, gdlonr, galtr`，例如 `b'0abi', 68.354, 18.816`，即当天参与 TEC 计算的接收机。
- `globalIsprint.py` 是它的过滤版（`--parms`、`--filter=gdlat,41.9,42.1`、`--format=Hdf5|netCDF4|ascii`）。本轮只看了 `--help`，没有实跑。

## 4. 输入与输出

| 输入 | 从哪来 |
| --- | --- |
| 实例基址 | 表 1；全部站点列表用 `https://cedar.openmadrigal.org/getMetadata?fileType=5`（CSV：站号、名称、主机……） |
| kinst（仪器码） | `getInstrumentsService.py`（CSV），或 `m.getAllInstruments()` |
| 实验 id → 文件绝对路径 | `getExperiments` → `getExperimentFiles`（`f.name`） |
| 三个用户字段 | 自填，不校验 |

HDF5 布局（两类文件都一样）：

```text
Data/Table Layout            (N,) compound   一行一条记录：year..sec(中点) recno kindat kinst ut1_unix ut2_unix + 参数列
Data/Array Layout/           重排后的数组
  TEC: gdlat(180) glon(360) timestamps(288)；2D Parameters/tec|dtec|gdalt 形状 (180, 360, 288) = (lat, lon, time)
  ISR: "Array with beamid=NNNNN "/ range(206) timestamps(76)；2D Parameters/popl|dpopl (206, 76) = (range, time)
Metadata/Data Parameters     助记符 / 描述 / 是否误差 / 单位（TEC 单位写作 "tec" = TECU）
Metadata/Experiment Parameters  仪器、kindat、起止时间、status（final / Preliminary）
```

TEC 格网的纬度从 −90 到 89，经度从 −180 到 179，步长 1°，时间步长 5 min（00:00 至 23:55）。文件里没有写明整数度是格心还是格边，**别自己加 0.5° 偏移**。

## 5. 参数

| 位置 | 参数 | 说明 |
| --- | --- | --- |
| `getExperiments(code, y,m,d,H,M,S, y,m,d,H,M,S, local=1)` | `code` | kinst；可给列表 |
| `getExperimentFiles(id)` | `.kindat` `.kindatdesc` `.category` `.status` | TEC：3500 为格网，3505 为 LOS，3506 为站表，另有 3507 ROTI；`category==1` 为默认文件 |
| `downloadFile(name, dest, fullname, email, affil, format=)` | `format` | 本文用 `"hdf5"` |
| `getMadfile.cgi` | `fileName` `fileType=-2` + 三字段 | `-2` = HDF5（本文只验证了这一种） |
| `isprint(file, parms, filters, …)` | `parms` | 逗号分隔的小写助记符，例如 `gdlat,glon,tec,dtec` |
| | `filters` | 空格分隔：`date1=MM/DD/YYYY time1=HH:MM:SS date2=… time2=… filter=<mnem>,<lo>,<hi>` |
| `globalDownload.py` | `--inst` `--kindat` `--startDate/--endDate MM/DD/YYYY` `--fileDesc` `--expName` `--tree` `--includeNonDefault` | 默认只下 default 文件；`--tree` 保留服务器目录结构 |

## 6. 在工作流里接哪一步

- **路径 A · 一日 TEC**（[README](./README.md#a--一日-tec)）：自算的站点 VTEC 或 GIM，用 Madrigal 格网同一格同一时刻交叉核对（例：3.3 节的 45.06 TECU）。
- **路径 B · 不规则体 / 磁暴**：3507 ROTI 与 ISR 剖面，对照 [pyspedas](./pyspedas.md) 取得的 SYM-H / Kp 时间轴；绘图可交给 [geospacelab](./geospacelab.md)，它内置 Madrigal TEC 产品。
- **路径 E · 理解 GIM**：拿 Madrigal 的「只在有站处有值」格网，对比 [ionex-gim](./ionex-gim.md) 的全球插值图。
- 同一门户的 HF spot 数据：[hamsci-lstid-detection](./hamsci-lstid-detection.md)。

## 7. 坑（现象 → 原因 → 修复）

1. **下到 100 B 的“文件”** → `fileName` 路径猜错（年份不同，目录可能是 `experiments3` 或 `experiments4`），服务端仍回 **200**，正文是 `<p>fileName … not found<p>` → 永远用 `getExperimentFiles` 返回的 `f.name`；下载后检查大小和 `\x89HDF` 文件头。
2. **近年的 TEC 日文件很大** → 2024-05-10 的格网 156 MB，2000 年的只有 13 MB → 只要点或小区域就用 isprint（3.3 节）；要整天先 `curl -I` 看 `Content-Length`。
3. **查一天得到两个实验** → 查询按时间重叠匹配，TEC 实验 `09may24` 的结束时间是 05-10 00:00 → 按 `e.startday` 再筛一遍；`globalDownload.py` 也会多下前一天的文件。
4. **CEDAR 很慢** → `getExperiments` 要 28–30 s（EISCAT 6 s，SRI 2 s）→ 把实验 / 文件清单缓存成 JSON，别在循环里反复查。
5. **时间差 2.5 min** → 表布局的 `year…sec` 是区间中点（18:02:30），`Array Layout/timestamps` 是 `ut1_unix`（18:00:00）→ 统一用 `ut1_unix` / `ut2_unix`。
6. **curl isprint 报 `Illegal parameter: year,month,…`** → 服务端要求每个参数单独一个 `parms=` → `-d parms=year -d parms=month …`（madrigalWeb 内部也是这样拼的）。
7. **`globalDownload.py` 改了文件名** → `site_20240510.002.h5` 被存成 `site_20240510.002.h5.hdf5` → 脚本里按 glob 找文件，或者加 `--tree`。
8. **h5py `KeyError`：ISR 波束组** → 组名是 `"Array with beamid=64016 "`，**末尾有空格** → 用 `for name in A` 枚举，别手敲组名。
9. **TEC 数组维度顺序** → `Layout Description` 写的是“每个时间一行”，实际形状是 `(180, 360, 288)` = (lat, lon, time) → 以 `.shape` 和轴长对照为准。
10. **大片 NaN 不是坏文件** → 这是分箱产品，只有被穿刺点覆盖的格子才有值（2000-01-01 全天有值比例为 0.043）→ 需要全球连续场就用 GIM，不要拿它当插值图。
11. **`popl` 不是 Ne** → 它是 log10 的、未做 Te/Ti 修正的功率密度 → 做物理比较用 `_fit_` 文件的 `ne`；换算时先 `10**popl`。
12. **Preliminary 与 final 并存** → 同一天会有 `gps…g.001`（Preliminary）、`.002`（final）、`.003`，category 也不同 → 选 `category==1` 且 status 为 final 的那一版，并在论文里写清版本号。
13. **SRI 实例较旧（2.6）** → 实验 URL 是 `http://`，路径 `/opt/madrigal/madrigal3/…` 与 CEDAR 不同 → 照样用 API 返回的路径；madrigalWeb 3.3.8 对 SRI 可用（本文实测）。

## 8. 选型对比

| 需求 | 选 | 不选的理由 |
| --- | --- | --- |
| 脚本化找实验 + 下几份文件 | **madrigalWeb**（Python） | 纯 curl 要自己解析 CSV |
| 服务器上只有 curl / 写进 shell 流水线 | **`getMadfile.cgi` / `isprintService.py`** | 功能一样，但参数编码要自己处理（坑 6） |
| 按仪器 + 日期范围整批下载 | **`globalDownload.py`** | 手写循环容易重复下载 |
| 只要一点 / 一小块 TEC | **isprint**（服务端过滤） | 整文件动辄 100 MB 以上 |
| 全球连续 VTEC 图（无空洞） | [ionex-gim](./ionex-gim.md) / CODE、CAS GIM | Madrigal 格网只在有站处有值 |
| 自己从 RINEX 算 TEC | [gnss-tec](./gnss-tec.md) | Madrigal 只给成品 |
| 空间天气一站式拉取 + 出图 | [geospacelab](./geospacelab.md) | 它封装了 Madrigal TEC，但隐藏了文件层细节 |
| EISCAT L2 原始分析 | EISCAT 门户（EGI Check-in） | Madrigal 只镜像 GUISDAP 结果 |
