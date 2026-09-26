# ESA Swarm 电离层产品：swarm-diss HTTPS 直取（LP / TEC / IPIR / IBI / EEF）+ VirES HAPI 匿名

入口：[swarm-diss 网页](https://swarm-diss.eo.esa.int/) · [Swarm Product Handbook](https://swarmhandbook.earth.esa.int/) · [VirES](https://vires.services/) · [VirES HAPI](https://vires.services/hapi/) · 本机验证 **2026-09-26 04:34–04:47 EDT**

> 岗位：不注册、不用 token，从 ESA Swarm 分发服务器的 **HTTPS 网页接口**拿 Swarm 电离层文件（ZIP 里是 CDF），用 cdflib 读 Langmuir 探针 Ne/Te 和各自的 flag，并认清 TEC（绝对/相对、仰角门限）、IPIR（含极盖斑块 PCP_flag）、IBI（等离子体泡）、EEF（赤道电场）这几个 L2 产品；真实个例是 Swarm B 在 2024-05-11（Kp 9）的沿轨 Ne 与平静日 05-08 对比。有 token 的 VirES 客户端见 [viresclient](./viresclient.md)（那篇写的是 OWS/WPS 必须 token；本文补充：**VirES HAPI 匿名可用**）；用 LP + TEC 算 RODI/ROTI 等不规则体指数、以及 LP 0701 改名的补丁见 [titipy](./titipy.md)（它用的是 Swarm A 同一天，本文不重复其指数计算）；COSMIC-2 剖面见 [cosmic2-ro](./cosmic2-ro.md)；地基测高仪见 [giro-ionosonde](./giro-ionosonde.md)；Kp/Dst 见 [space-weather-indices](./space-weather-indices.md)。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E24](../data-access.md#dp-e24)（swarm-diss HTTPS）· [E25](../data-access.md#dp-e25)（VirES HAPI）
>
> 冲突时：以 Swarm Product Handbook 各产品页和 CDF 文件本身为准；本文标明“本文自定”的过滤阈值都不是官方值。ESA 随时可能改分发策略（FTP 早已不收匿名）。

## 1. 它解决什么，边界在哪

| 能做 | 怎么做 | 边界 |
|---|---|---|
| 匿名列目录 | `https://swarm-diss.eo.esa.int/?do=list&maxfiles=10000&pos=0&file=<URL 编码路径>` → JSON（name/size/mtime） | 目录大（~4700 文件）时一次 10–30 s；`/swarm/` 直接路径 403 |
| 匿名下载 | `https://swarm-diss.eo.esa.int/?do=download&file=<URL 编码路径>` | 只有网页这套 `?do=` 接口；FTP 匿名 530 |
| 一次拿全目录清单 | 每个产品目录旁的 `<产品>.txt`（如 `TEC.txt`，~1 MB，全部相对路径） | 只有路径，没有大小/时间 |
| LP 等离子体 Ne/Te（2 Hz / 1 Hz） | `Level1b/Latest_baselines/EFIx_LP`、`EFIxLPI` | Ne 用 `N_ion`（旧名 `Ne`）；`N_elec` 另一套估计，负值多 |
| TEC、IPIR、IBI、EEF（每天一个文件） | `Level2daily/Latest_baselines/{TEC/TMS, IPD/IRR, IBI/TMS, EEF/TMS}` | PCP 不单独成产品：在 IPIR 的 `PCP_flag` 里 |
| 近实时（约 40 min） | `Fast/Level1b/EFIx_LP`、`Fast/Level2/TEC`（直接 `.cdf`，不打包） | 只有部分产品；`SW_FAST_` 前缀，按段不按天 |
| 服务器端切片、不下整天 | VirES HAPI `https://vires.services/hapi/data?...`（匿名，CSV/JSON/binary） | 单次时长上限：LP 2.5 天（`P2DT12H`）、TEC 5 天；没有模型评估 |
| 模型残差、多卫星合并、磁坐标 | VirES OWS/WPS + [viresclient](./viresclient.md) | **要 token**（vires.services 注册）；本文没注册 |

## 2. 安装

下载只要 `curl`。读 CDF 用 `cdflib`（纯 Python，不需要 NASA CDF C 库）：

```bash
python3 -m venv venv && venv/bin/pip -q install cdflib numpy
venv/bin/python -c "import cdflib,numpy,sys;print(sys.version.split()[0],cdflib.__version__,numpy.__version__)"
# 3.13.5 1.3.14 2.5.3
```

## 3. 真实命令与输出

### 3.1 门槛：HTTPS、FTP、VirES OWS、VirES HAPI（`access.sh`，原样）

```bash
#!/usr/bin/env bash
# 门槛：HTTPS 列表/下载匿名；FTP 拒绝匿名；VirES OWS/WPS 要 token；VirES HAPI 匿名
set -u
H=https://swarm-diss.eo.esa.int
echo "--- HTTPS 列表 API（JSON）"
curl -s -w '  HTTP %{http_code} %{size_download} B\n' "$H/?do=list&maxfiles=10000&pos=0&file=swarm" | python3 -c "import sys,json;t=sys.stdin.read();j=json.loads(t[:t.rindex('}')+1]);print('  ',[x['name'] for x in j['results']]);print(t[t.rindex('}')+1:].rstrip())"
echo "--- 目录清单 .txt（每个产品一份，含全部文件相对路径）"
curl -s -o TEC.txt -w '  TEC.txt HTTP %{http_code} %{size_download} B\n' "$H/?do=download&file=swarm%2FLevel2daily%2FLatest_baselines%2FTEC.txt"
echo "  行数 $(wc -l < TEC.txt)；首行 $(head -1 TEC.txt)"; rm -f TEC.txt
echo "--- 直接路径（不经 ?do=）"
curl -s -o /dev/null -w '  %{http_code}  /swarm/\n' "$H/swarm/"
echo "--- FTP 匿名"
curl -s -m 30 -v ftp://swarm-diss.eo.esa.int/ 2>&1 | grep -E '^< (220-This|331|530)'
echo "--- VirES OWS（viresclient 用的）无 token"
curl -s -w '  HTTP %{http_code}\n' "https://vires.services/ows?service=WPS&request=GetCapabilities"
echo "--- VirES HAPI 无 token"
curl -s -w '  HTTP %{http_code}\n' "https://vires.services/hapi/capabilities"
curl -s "https://vires.services/hapi/catalog" | python3 -c "import sys,json;c=[x['id'] for x in json.load(sys.stdin)['catalog']];s=[x for x in c if x.startswith('SW_')];print('  catalog',len(c),'个，其中 SW_',len(s),'；举例',[x for x in s if any(k in x for k in ('EFIB_LP','TECB','IPDB','IBIB','EEFB'))])"
curl -s "https://vires.services/hapi/info?dataset=SW_OPER_TECBTMS_2F" | python3 -c "import sys,json;d=json.load(sys.stdin);print('  TECBTMS info: stop',d['stopDate'],'cadence',d.get('cadence'),'x_maxTimeSelection',d.get('x_maxTimeSelection'));print('  参数',[p['name'] for p in d['parameters']])"
curl -s -w '  HTTP %{http_code} %{size_download} B\n' "https://vires.services/hapi/data?dataset=SW_OPER_EFIB_LP_1B&parameters=Latitude,Longitude,N_ion,Flags_N_ion&start=2024-05-11T16:00:00Z&stop=2024-05-11T16:00:02Z&format=csv"
curl -s -w '  HTTP %{http_code}\n' "https://vires.services/hapi/data?dataset=SW_OPER_EFIB_LP_1B&parameters=Ne&start=2024-05-11T16:00:00Z&stop=2024-05-11T16:00:02Z&format=csv"
```

输出（原样）：

```text
--- HTTPS 列表 API（JSON）
   ['Advanced', 'Fast', 'Level1b', 'Level2daily', 'Level2longterm', 'Multimission']
  HTTP 200 1000 B
--- 目录清单 .txt（每个产品一份，含全部文件相对路径）
  TEC.txt HTTP 200 1038220 B
  行数 14030；首行 TEC/TMS/Sat_A/SW_OPER_TECATMS_2F_20131125T000000_20131125T235959_0502.ZIP
--- 直接路径（不经 ?do=）
  403  /swarm/
--- FTP 匿名
< 220-This is a private system - No anonymous login
< 331 User anonymous OK. Password required
< 530 Login authentication failed
--- VirES OWS（viresclient 用的）无 token
Forbidden  HTTP 403
--- VirES HAPI 无 token
{"HAPI": "3.0", "status": {"code": 1200, "message": "OK"}, "outputFormats": ["csv", "json", "binary", "x_binary"]}  HTTP 200
  catalog 174 个，其中 SW_ 147 ；举例 ['SW_FAST_EFIB_LP_1B', 'SW_FAST_TECBTMS_2F', 'SW_OPER_EEFBTMS_2F', 'SW_OPER_EFIB_LP_1B', 'SW_OPER_IBIBTMS_2F', 'SW_OPER_IPDBIRR_2F', 'SW_OPER_TECBTMS_2F']
  TECBTMS info: stop 2026-09-20T23:59:59Z cadence PT1S x_maxTimeSelection P5D
  参数 ['Timestamp', 'Latitude', 'Longitude', 'Radius', 'GPS_Position', 'LEO_Position', 'PRN', 'L1', 'L2', 'P1', 'P2', 'S1', 'S2', 'Absolute_STEC', 'Absolute_VTEC', 'Elevation_Angle', 'Relative_STEC', 'Relative_STEC_RMS', 'DCB', 'DCB_Error']
2024-05-11T16:00:00.197Z,8.5277053,-76.86320169999999,483458.0389614415,20
2024-05-11T16:00:00.696Z,8.496124499999999,-76.8640207,482504.61334791593,20
2024-05-11T16:00:01.197Z,8.4644172,-76.8648431,481973.81769634085,20
2024-05-11T16:00:01.696Z,8.432836499999999,-76.8656625,482329.57865890703,20
  HTTP 200 302 B
{"HAPI": "3.0", "status": {"code": 1407, "message": "Bad request - unknown dataset parameter - invalid parameter Ne"}}  HTTP 404
```

结论：
- **swarm-diss HTTPS：匿名可列、可下**；同一台机器的 FTP（Pure-FTPd）写明 “No anonymous login”，要 ESA 账号。
- **VirES OWS/WPS（viresclient 走的）：403**，要 token；**VirES HAPI：匿名 200**，147 个 `SW_` 数据集，含 LP/TEC/IPIR/IBI/EEF。HAPI 返回值与 CDF 逐位一致（见 3.4 末行对账）。

### 3.2 下载一天：Swarm B 2024-05-11 + 平静日 05-08（`fetch.sh`，原样）

```bash
#!/usr/bin/env bash
# swarm-diss HTTPS（匿名）：Swarm B 2024-05-11 的 LP / LPI / TEC / IPIR / IBI / EEF 各一天 + 平静日 2024-05-08 的 LPI
set -u
D='https://swarm-diss.eo.esa.int/?do=download&file='
L1=swarm%2FLevel1b%2FLatest_baselines; L2=swarm%2FLevel2daily%2FLatest_baselines
for p in \
  $L1%2FEFIx_LP%2FSat_B%2FSW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701.CDF.ZIP \
  $L1%2FEFIxLPI%2FSat_B%2FSW_OPER_EFIBLPI_1B_20240511T000000_20240511T235959_0701.CDF.ZIP \
  $L1%2FEFIxLPI%2FSat_B%2FSW_OPER_EFIBLPI_1B_20240508T000000_20240508T235959_0701.CDF.ZIP \
  $L2%2FTEC%2FTMS%2FSat_B%2FSW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.ZIP \
  $L2%2FIPD%2FIRR%2FSat_B%2FSW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.ZIP \
  $L2%2FIBI%2FTMS%2FSat_B%2FSW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.ZIP \
  $L2%2FEEF%2FTMS%2FSat_B%2FSW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.ZIP ; do
  f=${p##*%2F}
  curl -s -o "$f" -w "%{http_code} %{size_download} B %{time_total} s  $f\n" "$D$p"
done
echo "--- ZIP 内容"
for z in *.ZIP; do unzip -oq "$z"; python3 -c "import zipfile,sys;[print('  ',sys.argv[1][:22],i.filename,i.file_size) for i in zipfile.ZipFile(sys.argv[1]).infolist()]" "$z"; done
```

输出（原样；7 个 ZIP 共 ~85 MB，用完即删）：

```text
200 12429396 B 3.831815 s  SW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701.CDF.ZIP
200 6363147 B 2.599774 s  SW_OPER_EFIBLPI_1B_20240511T000000_20240511T235959_0701.CDF.ZIP
200 6571749 B 3.215049 s  SW_OPER_EFIBLPI_1B_20240508T000000_20240508T235959_0701.CDF.ZIP
200 43119937 B 8.611927 s  SW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.ZIP
200 10770088 B 3.168888 s  SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.ZIP
200 1785659 B 1.943631 s  SW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.ZIP
200 4277231 B 2.907300 s  SW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.ZIP
--- ZIP 内容
   SW_OPER_EEFBTMS_2F_202 SW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.HDR 5526
   SW_OPER_EEFBTMS_2F_202 SW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.cdf 4360240
   SW_OPER_EEFBTMS_2F_202 SW_OPER_REPB_DQC___20260210T131952_EEFBTMS_2F20240511T000000.EEF 1402
   SW_OPER_EFIBLPI_1B_202 SW_OPER_EFIBLPI_1B_20240508T000000_20240508T235959_0701_MDR_EFILPI.cdf 6725531
   SW_OPER_EFIBLPI_1B_202 SW_OPER_EFIBLPI_1B_20240508T000000_20240508T235959_0701.HDR 20672
   SW_OPER_EFIBLPI_1B_202 SW_OPER_REPB_DQC___20250724T033043_EFIBLPI_1B20240508T000000.EEF 1574
   SW_OPER_EFIBLPI_1B_202 SW_OPER_EFIBLPI_1B_20240511T000000_20240511T235959_0701_MDR_EFILPI.cdf 6518285
   SW_OPER_EFIBLPI_1B_202 SW_OPER_EFIBLPI_1B_20240511T000000_20240511T235959_0701.HDR 20673
   SW_OPER_EFIBLPI_1B_202 SW_OPER_REPB_DQC___20250724T051831_EFIBLPI_1B20240511T000000.EEF 1574
   SW_OPER_EFIB_LP_1B_202 SW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701_MDR_EFI_LP.cdf 12768372
   SW_OPER_EFIB_LP_1B_202 SW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701.HDR 20659
   SW_OPER_EFIB_LP_1B_202 SW_OPER_REPB_DQC___20250724T051830_EFIB_LP_1B20240511T000000.EEF 1574
   SW_OPER_IBIBTMS_2F_202 SW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.cdf 1987700
   SW_OPER_IBIBTMS_2F_202 SW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.HDR 33981
   SW_OPER_IBIBTMS_2F_202 SW_OPER_REPB_DQC___20260808T005155_IBIBTMS_2F20240511T000000.EEF 1603
   SW_OPER_IPDBIRR_2F_202 SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.HDR 2653
   SW_OPER_IPDBIRR_2F_202 SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.cdf 10822640
   SW_OPER_TECBTMS_2F_202 SW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.cdf 43268691
   SW_OPER_TECBTMS_2F_202 SW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.HDR 8733
   SW_OPER_TECBTMS_2F_202 SW_OPER_REPB_DQC___20260808T172556_TECBTMS_2F20240511T000000.EEF 1603
```

每个 ZIP = `.cdf`（数据）+ `.HDR`（XML 头：处理器版本、输入文件清单）+ 多数还有一个 `SW_OPER_REPB_DQC___…EEF`（**这个 .EEF 是 Earth Explorer File 格式的数据质量报告，不是 EEF 电场产品**）。IPIR 的 ZIP 没有 DQC 报告。

### 3.3 版本、基线与时延（`latency.py`，原样）

```python
# 各产品 Sat_B 最新文件：数据结束时间 vs 服务器 mtime（= 发布时延），以及 2024-05-11 文件的 mtime（重处理痕迹）
import json, re, urllib.request, urllib.parse, datetime as dt
def ls(path):
    u = 'https://swarm-diss.eo.esa.int/?do=list&maxfiles=10000&pos=0&file=' + urllib.parse.quote(path, safe='')
    return [x for x in json.loads(urllib.request.urlopen(u, timeout=300).read())['results'] if not x['is_dir']]
now = dt.datetime.now(dt.timezone.utc)
print('查询时刻', f'{now:%Y-%m-%d %H:%M}Z', f'= {(now - dt.timedelta(hours=4)):%H:%M} EDT')
for p in ('Level1b/Latest_baselines/EFIx_LP/Sat_B', 'Level1b/Latest_baselines/EFIxLPI/Sat_B',
          'Level2daily/Latest_baselines/TEC/TMS/Sat_B', 'Level2daily/Latest_baselines/IPD/IRR/Sat_B',
          'Level2daily/Latest_baselines/IBI/TMS/Sat_B', 'Level2daily/Latest_baselines/EEF/TMS/Sat_B',
          'Fast/Level1b/EFIx_LP/Sat_B', 'Fast/Level2/TEC/Sat_B'):
    r = sorted(ls('swarm/' + p), key=lambda x: x['name'])
    last = r[-1]; m = re.search(r'_(\d{8}T\d{6})_(\d{8}T\d{6})_(\d{4})', last['name'])
    end = dt.datetime.strptime(m.group(2), '%Y%m%dT%H%M%S').replace(tzinfo=dt.timezone.utc)
    mt = dt.datetime.fromtimestamp(last['mtime'], dt.timezone.utc)
    old = [x for x in r if '20240511T' in x['name']]
    o = f"{dt.datetime.fromtimestamp(old[0]['mtime'], dt.timezone.utc):%Y-%m-%d}" if old else '—'
    print(f"{p.replace('Level1b/Latest_baselines/','L1b/').replace('Level2daily/Latest_baselines/','L2/'):24s} {len(r):5d} 文件 | 最新 {m.group(1)}..{m.group(2)} v{m.group(3)} {last['size']:>11,} B "
          f"| mtime {mt:%m-%d %H:%M}Z | 数据结束→上架 {(mt-end).total_seconds()/3600:6.1f} h | 2024-05-11 文件 mtime {o}")
```

输出（原样）：

```text
查询时刻 2026-09-26 08:43Z = 04:43 EDT
L1b/EFIx_LP/Sat_B         4669 文件 | 最新 20260922T000000..20260922T235959 v0702  13,031,670 B | mtime 09-26 00:27Z | 数据结束→上架   72.5 h | 2024-05-11 文件 mtime 2025-07-29
L1b/EFIxLPI/Sat_B         4669 文件 | 最新 20260922T000000..20260922T235959 v0702   6,655,055 B | mtime 09-26 00:27Z | 数据结束→上架   72.5 h | 2024-05-11 文件 mtime 2025-07-29
L2/TEC/TMS/Sat_B          4680 文件 | 最新 20260920T000000..20260920T235959 v0502  40,285,594 B | mtime 09-25 14:03Z | 数据结束→上架  110.1 h | 2024-05-11 文件 mtime 2026-08-30
L2/IPD/IRR/Sat_B          7534 文件 | 最新 20260907T000000..20260907T235959 v0302  11,354,671 B | mtime 09-17 05:28Z | 数据结束→上架  221.5 h | 2024-05-11 文件 mtime 2024-05-24
L2/IBI/TMS/Sat_B          4663 文件 | 最新 20260920T000000..20260920T235959 v0502   1,778,191 B | mtime 09-25 14:04Z | 数据结束→上架  110.1 h | 2024-05-11 文件 mtime 2026-08-29
L2/EEF/TMS/Sat_B          4677 文件 | 最新 20260921T000000..20260921T235959 v0502   4,417,025 B | mtime 09-25 13:37Z | 数据结束→上架   85.6 h | 2024-05-11 文件 mtime 2026-02-10
Fast/Level1b/EFIx_LP/Sat_B   548 文件 | 最新 20260925T193806..20260926T064905 v0702   6,263,702 B | mtime 09-26 07:22Z | 数据结束→上架    0.6 h | 2024-05-11 文件 mtime —
Fast/Level2/TEC/Sat_B      383 文件 | 最新 20260925T193806..20260926T064905 v0101  19,237,703 B | mtime 09-26 07:31Z | 数据结束→上架    0.7 h | 2024-05-11 文件 mtime —
```

| 产品 | 文件名样式 | 当前基线/版本（09-26） | 实测上架时延 | Handbook 写的 |
|---|---|---|---|---|
| LP 2 Hz | `SW_OPER_EFIx_LP_1B_<起>_<止>_<BBVV>.CDF.ZIP` | 0701（2013-12-02..2025-12-12）、**0702**（2025-12-13 起） | ~3 天 | — |
| LP 1 Hz 插值 | `SW_OPER_EFIxLPI_1B_…_0701/0702.CDF.ZIP` | 同上 | ~3 天 | — |
| TEC | `SW_OPER_TECxTMS_2F_…_0502.ZIP` | 0502 | ~4.6 天 | 6 min |
| IPIR | `SW_OPER_IPDxIRR_2F_…_0302.ZIP` | 0302（目录里**同时还留着** 0301：2014-07..2023-02） | ~9 天 | 10 min |
| IBI | `SW_OPER_IBIxTMS_2F_…_0502.ZIP` | 0502 | ~4.6 天 | 6 min |
| EEF | `SW_OPER_EEFxTMS_2F_…_0502.ZIP` | 0502 | ~3.6 天 | — |
| FAST LP / TEC | `SW_FAST_EFIx_LP_1B_…_0702_MDR_EFI_LP.cdf`、`SW_FAST_TECxTMS_2F_…_0101.cdf` | 0702 / 0101 | **~40 min** | — |

- 版本号 `BBVV`：前两位基线（processor baseline），后两位文件版本。`Latest_baselines` = 每一天“当前最新基线”的文件，**不保证全任务同一基线**（LP 在 2025-12-13 切到 0702）。
- Handbook 的 “Latency 6 min/10 min” 是处理耗时，不是 OPER 文件上架时间。
- 2024-05-11 的 TEC/IBI 文件 mtime 是 2026-08，EEF 2026-02，LP 2025-07：同名同版本号的文件被**重新生成过**；要复现就记下 mtime 或 HDR 里的 `Creation_Date`。

### 3.4 LP：变量、flag、沿轨 Ne 与磁暴特征（`cdfvars.py` + `ne.py`，原样）

`cdfvars.py` 列出每个 CDF 的变量（原样）：

```python
# 列出每个 CDF 的变量：名字、形状、单位、说明（前 70 字）
import glob, cdflib
for f in sorted(glob.glob('*.cdf')):
    c = cdflib.CDF(f); info = c.cdf_info()
    print(f'== {f}\n   zVariables {len(info.zVariables)}；全局属性:', ', '.join(list(c.globalattsget().keys())[:8]))
    for v in info.zVariables:
        a = c.varattsget(v); sh = c.varinq(v).Dim_Sizes; n = c.varinq(v).Last_Rec + 1
        print(f"   {v:22s} rec={n:<7d} dim={sh!s:8s} unit={str(a.get('UNITS',''))[:10]:10s} {str(a.get('CATDESC',a.get('DESCRIPTION','')))[:70]}")
```

输出（原样）：

```text
== SW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.cdf
   zVariables 15；全局属性: Created, File_Name, File_Description, Creator, Creator_Software, Creator_Version, Profile_Length, Coef_L2_Length
   Timestamp              rec=29      dim=[]       unit=-          Timestamp of magnetic equator crossing, UTC
   Latitude               rec=29      dim=[]       unit=degrees    Geocentric latitude of magnetic equator crossing
   Longitude              rec=29      dim=[]       unit=degrees    Longitude of magnetic equator crossing
   EEJ_meast              rec=29      dim=[81]     unit=A/km       Height-integrated magnetic eastward current profile (qlats = [-20:0.5:
   EEJ_mnorth             rec=29      dim=[81]     unit=A/km       Height-integrated magnetic northward current profile (qlats = [-20:0.5
   EEF                    rec=29      dim=[]       unit=mV/m       Equatorial electric field estimate
   RelErr                 rec=29      dim=[]       unit=-          Quality indicator of EEF estimate; relative error between modeled and 
   Flags                  rec=29      dim=[]       unit=-          Flags
   Timestamp_Track        rec=29      dim=[3000]   unit=-          Timestamp along track
   Latitude_Track         rec=29      dim=[3000]   unit=degrees    Latitude along track
   Longitude_Track        rec=29      dim=[3000]   unit=degrees    Longitude along track
   Radius_Track           rec=29      dim=[3000]   unit=km         Radius along track
   Ksq_Track              rec=29      dim=[6000]   unit=A/km       Surface current corresponding to Sq magnetic signal (NE)
   Keej_Track             rec=29      dim=[6000]   unit=A/km       Surface current corresponding to EEJ magnetic signal (NE)
   Length_Track           rec=29      dim=[]       unit=-          Length of each track
== SW_OPER_EFIBLPI_1B_20240508T000000_20240508T235959_0701_MDR_EFILPI.cdf
   zVariables 25；全局属性: TITLE, CREATOR, File_Name, File_Description, Notes, Mission, File_Class, File_Type
   Timestamp              rec=86388   dim=[]       unit=-          Time stamp
   SyncStatus             rec=86388   dim=[]       unit=-          Synchronization status
   Latitude               rec=86388   dim=[]       unit=deg        Geocentric latitude
   Longitude              rec=86388   dim=[]       unit=deg        Geocentric longitude
   Radius                 rec=86388   dim=[]       unit=m          Distance from the Earth's center
   U_orbit                rec=86388   dim=[1]      unit=m/s        Spacecraft velocity in the ITRF
   N_ion                  rec=86388   dim=[]       unit=cm-3       Plasma density estimated from the ion current
   dN_ion                 rec=86388   dim=[]       unit=cm-3       Suggested calibration correction of N_ion
   N_ion_error            rec=86388   dim=[]       unit=cm-3       Statistical error of the ion density estimate
   N_elec                 rec=86388   dim=[]       unit=cm-3       Plasma density estimated from the electron current
   N_elec_error           rec=86388   dim=[]       unit=cm-3       Statistical error of the electron density estimate
   T_elec                 rec=86388   dim=[]       unit=K          Plasma electron temperature
   T_elec_error           rec=86388   dim=[]       unit=K          Error estimate of plasma electron temperature (Te)
   dT_elec                rec=86388   dim=[]       unit=cm-3       Suggested calibration correction od T_elec
   Vs                     rec=86388   dim=[]       unit=V          Spacecraft potential
   Vs_error               rec=86388   dim=[]       unit=V          Error estimate of spacecraft potential (Vs)
   Flags_LP               rec=86388   dim=[]       unit=-          Flags indicating the source/method of LP measurements (Ni, Te, Vs)
   Flags_N_ion            rec=86388   dim=[]       unit=-          Flags characterizing the ion density estimate
   Flags_N_elec           rec=86388   dim=[]       unit=-          Flags characterizing the electron density estimate
   Flags_T_elec           rec=86388   dim=[]       unit=-          Flags characterizing the electron temperature measurement
   Flags_Vs               rec=86388   dim=[]       unit=-          Flags characterizing the spacecraft potential measurement
   Gamma1                 rec=86388   dim=[]       unit=deg        Sun inclination angle related to right-side solar-panel normal angle
   Gamma2                 rec=86388   dim=[]       unit=deg        Sun inclination angle related to left-side solar-panel normal angle
   Flagbits1              rec=86388   dim=[]       unit=-          Detailed indication of the source and anomalies
   Flagbits2              rec=86388   dim=[]       unit=-          Detailed indication of the source and anomalies
== SW_OPER_EFIBLPI_1B_20240511T000000_20240511T235959_0701_MDR_EFILPI.cdf
   zVariables 25；全局属性: TITLE, CREATOR, File_Name, File_Description, Notes, Mission, File_Class, File_Type
   Timestamp              rec=86388   dim=[]       unit=-          Time stamp
   SyncStatus             rec=86388   dim=[]       unit=-          Synchronization status
   Latitude               rec=86388   dim=[]       unit=deg        Geocentric latitude
   Longitude              rec=86388   dim=[]       unit=deg        Geocentric longitude
   Radius                 rec=86388   dim=[]       unit=m          Distance from the Earth's center
   U_orbit                rec=86388   dim=[1]      unit=m/s        Spacecraft velocity in the ITRF
   N_ion                  rec=86388   dim=[]       unit=cm-3       Plasma density estimated from the ion current
   dN_ion                 rec=86388   dim=[]       unit=cm-3       Suggested calibration correction of N_ion
   N_ion_error            rec=86388   dim=[]       unit=cm-3       Statistical error of the ion density estimate
   N_elec                 rec=86388   dim=[]       unit=cm-3       Plasma density estimated from the electron current
   N_elec_error           rec=86388   dim=[]       unit=cm-3       Statistical error of the electron density estimate
   T_elec                 rec=86388   dim=[]       unit=K          Plasma electron temperature
   T_elec_error           rec=86388   dim=[]       unit=K          Error estimate of plasma electron temperature (Te)
   dT_elec                rec=86388   dim=[]       unit=cm-3       Suggested calibration correction od T_elec
   Vs                     rec=86388   dim=[]       unit=V          Spacecraft potential
   Vs_error               rec=86388   dim=[]       unit=V          Error estimate of spacecraft potential (Vs)
   Flags_LP               rec=86388   dim=[]       unit=-          Flags indicating the source/method of LP measurements (Ni, Te, Vs)
   Flags_N_ion            rec=86388   dim=[]       unit=-          Flags characterizing the ion density estimate
   Flags_N_elec           rec=86388   dim=[]       unit=-          Flags characterizing the electron density estimate
   Flags_T_elec           rec=86388   dim=[]       unit=-          Flags characterizing the electron temperature measurement
   Flags_Vs               rec=86388   dim=[]       unit=-          Flags characterizing the spacecraft potential measurement
   Gamma1                 rec=86388   dim=[]       unit=deg        Sun inclination angle related to right-side solar-panel normal angle
   Gamma2                 rec=86388   dim=[]       unit=deg        Sun inclination angle related to left-side solar-panel normal angle
   Flagbits1              rec=86388   dim=[]       unit=-          Detailed indication of the source and anomalies
   Flagbits2              rec=86388   dim=[]       unit=-          Detailed indication of the source and anomalies
== SW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701_MDR_EFI_LP.cdf
   zVariables 25；全局属性: TITLE, CREATOR, File_Name, File_Description, Notes, Mission, File_Class, File_Type
   Timestamp              rec=172776  dim=[]       unit=-          Time stamp
   SyncStatus             rec=172776  dim=[]       unit=-          Synchronization status
   Latitude               rec=172776  dim=[]       unit=deg        Position in ITRF - Latitude
   Longitude              rec=172776  dim=[]       unit=deg        Position in ITRF - Longitude
   Radius                 rec=172776  dim=[]       unit=m          Position in ITRF - Radius
   U_orbit                rec=172776  dim=[]       unit=m/s        Spacecraft velocity in the ITRF
   N_ion                  rec=172776  dim=[]       unit=cm-3       Plasma density estimated from the ion current
   dN_ion                 rec=172776  dim=[]       unit=cm-3       Suggested calibration correction of N_ion
   N_ion_error            rec=172776  dim=[]       unit=cm-3       Statistical error of the ion density estimate
   N_elec                 rec=172776  dim=[]       unit=cm-3       Plasma density estimated from the electron current
   N_elec_error           rec=172776  dim=[]       unit=cm-3       Statistical error of the electron density estimate
   T_elec                 rec=172776  dim=[]       unit=K          Plasma electron temperature
   T_elec_error           rec=172776  dim=[]       unit=K          Error estimate of plasma electron temperature (Te)
   dT_elec                rec=172776  dim=[]       unit=cm-3       Suggested calibration correction od T_elec
   Vs                     rec=172776  dim=[]       unit=V          Spacecraft potential
   Vs_error               rec=172776  dim=[]       unit=V          Error estimate of spacecraft potential (Vs)
   Flags_LP               rec=172776  dim=[]       unit=-          Flags indicating the source/method of LP measurements (Ni, Te, Vs)
   Flags_N_ion            rec=172776  dim=[]       unit=-          Flags characterizing the ion density estimate
   Flags_N_elec           rec=172776  dim=[]       unit=-          Flags characterizing the electron density estimate
   Flags_T_elec           rec=172776  dim=[]       unit=-          Flags characterizing the electron temperature measurement
   Flags_Vs               rec=172776  dim=[]       unit=-          Flags characterizing the spacecraft potential measurement
   Gamma1                 rec=172776  dim=[]       unit=deg        Sun inclination angle related to right-side solar-panel normal angle
   Gamma2                 rec=172776  dim=[]       unit=deg        Sun inclination angle related to left-side solar-panel normal angle
   Flagbits1              rec=172776  dim=[]       unit=-          Detailed indication of the source and anomalies
   Flagbits2              rec=172776  dim=[]       unit=-          Detailed indication of the source and anomalies
== SW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.cdf
   zVariables 10；全局属性: File_Name, File_Description, Mission, File_Class, File_Type, Validity_Start, Validity_Stop, File_Version
   Timestamp              rec=86400   dim=[]       unit=ms         Time stamp in UTC
   Latitude               rec=86400   dim=[]       unit=degree     Geographic latitude
   Longitude              rec=86400   dim=[]       unit=degree     Geographic longitude
   Radius                 rec=86400   dim=[]       unit=m          Geographic radius
   Bubble_Index           rec=86400   dim=[]       unit=-          Plasma Bubble Index
   Bubble_Probability     rec=86400   dim=[]       unit=-          Detection probability of the plasma bubble
   Flags_Bubble           rec=86400   dim=[]       unit=-          Flags related to the plasma bubble index
   Flags_F                rec=86400   dim=[]       unit=-          Flags_F passed through from MAGx_L1_B
   Flags_B                rec=86400   dim=[]       unit=-          Flags_B passed through from MAGx_L1_B
   Flags_q                rec=86400   dim=[]       unit=-          Flags_q passed through from MAGx_L1_B
== SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.cdf
   zVariables 29；全局属性: Description, Website, Funding, Contact, Product, Creator, Creator_Version, Creation_Date
   Timestamp              rec=86400   dim=[]       unit=-          CDF_EPOCH of the measurement.
   Latitude               rec=86400   dim=[]       unit=deg        Position in ITRF - Latitude.
   Longitude              rec=86400   dim=[]       unit=deg        Position in ITRF - Longitude.
   Radius                 rec=86400   dim=[]       unit=m          Position in ITRF - Radius.
   Ne                     rec=86400   dim=[]       unit=cm^-3      Plasma density, directly copied from the Langmuir probe files.
   Background_Ne          rec=86400   dim=[]       unit=cm^-3      Background density, as calculated from Ne using a percentile filter of
   Foreground_Ne          rec=86400   dim=[]       unit=cm^-3      Foreground density, as calculated from ndens using a percentile filter
   Te                     rec=86400   dim=[]       unit=K          Electron temperature, directly copied from the Langmuir probe files.
   PCP_flag               rec=86400   dim=[]       unit=-          The polar cap patch flag:  0 if the plasma density measurement occurre
   Grad_Ne_at_100km       rec=86400   dim=[]       unit=cm^-3/m    The electron density gradient in a running window calculated via linea
   Grad_Ne_at_50km        rec=86400   dim=[]       unit=cm^-3/m    The electron density gradient in a running window calculated via linea
   Grad_Ne_at_20km        rec=86400   dim=[]       unit=cm^-3/m    The electron density gradient in a running window calculated via linea
   Grad_Ne_at_PCP_edge    rec=86400   dim=[]       unit=cm^-3/m    The linear electron density gradient calculated over the edges of a pa
   ROD                    rec=86400   dim=[]       unit=cm^-3/s    Rate Of change of Density
   RODI10s                rec=86400   dim=[]       unit=cm^-3/s    Rate Of change of Density Index (RODI) is the standard deviation of RO
   RODI20s                rec=86400   dim=[]       unit=cm^-3/s    Rate Of change of Density Index (RODI) is the standard deviation of RO
   delta_Ne10s            rec=86400   dim=[]       unit=cm^-3      Derived by subtracting Ne by its median filtered value in 10 seconds. 
   delta_Ne20s            rec=86400   dim=[]       unit=cm^-3      Derived by subtracting Ne by its median filtered value in 20 seconds. 
   delta_Ne40s            rec=86400   dim=[]       unit=cm^-3      Derived by subtracting Ne by its median filtered value in 40 seconds. 
   Num_GPS_satellites     rec=86400   dim=[]       unit=-          Total number of tracked GPS satellites above 20 degrees.
   mVTEC                  rec=86400   dim=[]       unit=TECU       Median of VTEC from all available GPS satellites above 30 degrees.
   mROT                   rec=86400   dim=[]       unit=TECU/s     Median of Rate Of change of TEC (ROT) from all available GPS satellite
   mROTI10s               rec=86400   dim=[]       unit=TECU/s     Median of Rate Of change of TEC Index (ROTI) from all available GPS sa
   mROTI20s               rec=86400   dim=[]       unit=TECU/s     Median of Rate Of change of TEC Index (ROTI) from all available GPS sa
   IBI_flag               rec=86400   dim=[]       unit=-          Plasma Bubble Index, copied from the level-2 Ionospheric Bubble Index 
   Ionosphere_region_flag rec=86400   dim=[]       unit=-          0: equator, 1: mid-latitudes; 2: auroral oval; 3: polar cap.
   IPIR_index             rec=86400   dim=[]       unit=-          The numeric index for plasma fluctuations and irregularities: 0-3 low,
   Ne_quality_flag        rec=86400   dim=[]       unit=-          Quality flag for the Ne data and the derived data from Ne, e.g., backg
   TEC_STD                rec=86400   dim=[]       unit=TECU       STD of VTEC from all GPS satellites.
== SW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.cdf
   zVariables 20；全局属性: File_Name, File_Description, Mission, File_Class, File_Type, Validity_Start, Validity_Stop, File_Version
   Timestamp              rec=465715  dim=[]       unit=ms         Time stamp in UTC
   Latitude               rec=465715  dim=[]       unit=degree     Geographic latitude
   Longitude              rec=465715  dim=[]       unit=degree     Geographic longitude
   Radius                 rec=465715  dim=[]       unit=km         Geographic radius
   GPS_Position           rec=465715  dim=[3]      unit=km         X-,Y-,Z-coordinates (WGS84) of the GPS satellite
   LEO_Position           rec=465715  dim=[3]      unit=m          X-,Y-,Z-coordinates (WGS84) of the LEO satellite
   PRN                    rec=465715  dim=[]       unit=-          GPS satellite PRN
   L1                     rec=465715  dim=[]       unit=m          GPS L1 carrier phase observation
   L2                     rec=465715  dim=[]       unit=m          GPS L2 carrier phase observation
   P1                     rec=465715  dim=[]       unit=m          GPS P1 code phase observation
   P2                     rec=465715  dim=[]       unit=m          GPS P2 code phase observation
   S1                     rec=465715  dim=[]       unit=-          GPS signal-to-noise ratio or raw signal strength on L1
   S2                     rec=465715  dim=[]       unit=-          GPS signal-to-noise ratio or raw signal strength on L2
   Absolute_STEC          rec=465715  dim=[]       unit=TECU       Absolute slant TEC
   Absolute_VTEC          rec=465715  dim=[]       unit=TECU       Absolute vertical TEC
   Elevation_Angle        rec=465715  dim=[]       unit=degree     Elevation Angle
   Relative_STEC          rec=465715  dim=[]       unit=TECU       Relative slant TEC
   Relative_STEC_RMS      rec=465715  dim=[]       unit=TECU       Root mean square error of relative slant TEC
   DCB                    rec=1       dim=[]       unit=TECU       GPS receiver differential code bias
   DCB_Error              rec=1       dim=[]       unit=TECU       Error of the GPS receiver differential code bias
```

`ne.py`（原样）：

```python
# Swarm B LP：flag 统计 + 过滤 + 沿轨 Ne（2024-05-11 磁暴日 vs 2024-05-08 平静日，EFIxLPI 1 Hz）
import collections, numpy as np, cdflib
LP  = 'SW_OPER_EFIB_LP_1B_20240511T000000_20240511T235959_0701_MDR_EFI_LP.cdf'
LPI = {d: f'SW_OPER_EFIBLPI_1B_2024{d}T000000_2024{d}T235959_0701_MDR_EFILPI.cdf' for d in ('0508', '0511')}
c = cdflib.CDF(LP)
print('== 2 Hz LP 05-11：记录数', len(c.varget('Timestamp')), '| 时间范围', *cdflib.cdfepoch.encode(c.varget('Timestamp')[[0, -1]]))
for v in ('Flags_LP', 'Flags_N_ion', 'Flags_N_elec', 'Flags_T_elec', 'Flags_Vs'):
    print(f'   {v:13s}', sorted(collections.Counter(c.varget(v).tolist()).items()))
ni, fn = c.varget('N_ion'), c.varget('Flags_N_ion'); ne, fe = c.varget('N_elec'), c.varget('Flags_N_elec')
te, ft = c.varget('T_elec'), c.varget('Flags_T_elec')
print('   N_ion  全部  min/中位/max %.0f / %.0f / %.0f cm^-3' % (ni.min(), np.median(ni), ni.max()))
print('   N_elec 全部  min %.0f，负值 %d 个，NaN %d 个；Flags 30/40（低增益/不可用）占 %.1f%%' % (np.nanmin(ne), (ne < 0).sum(), np.isnan(ne).sum(), 100 * np.isin(fe, [30, 40]).mean()))
print('   T_elec 全部  min %.0f max %.0f K；Flags_T_elec∈{20,21} 后 p1/中位/p99 = %.0f / %.0f / %.0f K' % (te.min(), te.max(), *np.percentile(te[np.isin(ft, [20, 21])], [1, 50, 99])))
print('   dN_ion NaN %d（= 该区域没有 ISR 标定），N_ion_error 全 NaN：%s' % (np.isnan(c.varget('dN_ion')).sum(), bool(np.isnan(c.varget('N_ion_error')).all())))
ok = np.isin(fn, [20, 21])       # 本文过滤：去掉 22/23（检测到尖峰）；本日没有 10/19/30/40
print('   过滤 Flags_N_ion∈{20,21}：保留 %d / %d（%.2f%%）' % (ok.sum(), ok.size, 100 * ok.mean()))
def load(f):
    c = cdflib.CDF(f); t = c.varget('Timestamp'); lat = c.varget('Latitude'); lon = c.varget('Longitude')
    ut = (t / 1000 % 86400) / 3600; lt = (ut + lon / 15) % 24
    return dict(ut=ut, lat=lat, lon=lon, lt=lt, asc=np.gradient(lat) > 0, n=c.varget('N_ion'),
                ok=np.isin(c.varget('Flags_N_ion'), [20, 21]), r=c.varget('Radius'))
D = {d: load(f) for d, f in LPI.items()}
for d, x in D.items():
    eq = np.abs(x['lat']) < 5
    print(f"== LPI 2024-{d[:2]}-{d[2:]}：{x['n'].size} 点，过滤后 {x['ok'].sum()}；升交 LT {np.median(x['lt'][eq & x['asc']]):.2f} h，降交 LT {np.median(x['lt'][eq & ~x['asc']]):.2f} h；"
          f"高度 {np.median(x['r'])/1e3 - 6371.2:.0f} km（半径−6371.2）")
print('== 纬度带中位 N_ion（1e3 cm^-3），全天所有经度；比值 = 05-11 / 05-08')
for node, nm in ((False, '降轨 ≈11 LT（白天）'), (True, '升轨 ≈23 LT（夜间）')):
    print(f'-- {nm}\n   纬度带     05-08    05-11   比值')
    for b in range(-70, 70, 10):
        m = [np.median(x['n'][x['ok'] & (x['asc'] == node) & (x['lat'] >= b) & (x['lat'] < b + 10)]) for x in D.values()]
        print(f'   {b:+4d}..{b+10:+4d} {m[0]/1e3:7.0f} {m[1]/1e3:8.0f} {m[1]/m[0]:6.2f}')
# 美洲扇区单轨：白天降轨，赤道穿越经度最接近 −75°
print('== 美洲扇区单轨（白天降轨，赤道穿越经度最接近 −75°），每 10° 纬度取 ±1° 中位 N_ion（1e3 cm^-3）')
for d, x in D.items():
    i_eq = np.where((~x['asc']) & (np.abs(x['lat']) < 0.5) & x['ok'])[0]
    k = i_eq[np.argmin(np.abs(((x['lon'][i_eq] + 180) % 360 - 180) + 75))]
    sel = (np.abs(x['ut'] - x['ut'][k]) < 0.4) & (~x['asc']) & x['ok']
    row = []
    for L in range(50, -51, -10):
        m = sel & (np.abs(x['lat'] - L) < 1)
        row.append(f"{np.median(x['n'][m])/1e3:5.0f}" if m.any() else '  ---')
    print(f"   {d}: 赤道 UT {x['ut'][k]:5.2f} h 经度 {x['lon'][k]:7.1f}  | 纬度 +50…−50: " + ' '.join(row))
# 与 VirES HAPI 匿名返回的首行对账（access.sh：2024-05-11T16:00:00.197Z N_ion=483458.0389614415 Flags 20）
t = c.varget('Timestamp'); i = int(np.argmin(np.abs(t - cdflib.cdfepoch.compute_epoch([2024, 5, 11, 16, 0, 0, 197]))))
print('== 对账：CDF', cdflib.cdfepoch.encode(t[i]), 'N_ion %.10f Flags_N_ion %d' % (ni[i], fn[i]))
```

输出（原样）：

```text
== 2 Hz LP 05-11：记录数 172776 | 时间范围 2024-05-11T00:00:00.197 2024-05-11T23:59:59.696
   Flags_LP      [(1, 169905), (5, 1529), (9, 1342)]
   Flags_N_ion   [(20, 86740), (21, 84487), (22, 483), (23, 1066)]
   Flags_N_elec  [(21, 139168), (30, 14807), (40, 18801)]
   Flags_T_elec  [(20, 85776), (21, 82121), (22, 1394), (23, 1946), (30, 980), (40, 559)]
   Flags_Vs      [(20, 162924), (30, 9852)]
   N_ion  全部  min/中位/max 2275 / 97197 / 2109473 cm^-3
   N_elec 全部  min -1373893，负值 16320 个，NaN 249 个；Flags 30/40（低增益/不可用）占 19.5%
   T_elec 全部  min -5493074 max 2440964 K；Flags_T_elec∈{20,21} 后 p1/中位/p99 = 1858 / 3571 / 6309 K
   dN_ion NaN 57091（= 该区域没有 ISR 标定），N_ion_error 全 NaN：True
   过滤 Flags_N_ion∈{20,21}：保留 171227 / 172776（99.10%）
== LPI 2024-05-08：86388 点，过滤后 86340；升交 LT 23.17 h，降交 LT 11.17 h；高度 516 km（半径−6371.2）
== LPI 2024-05-11：86388 点，过滤后 85762；升交 LT 22.91 h，降交 LT 10.91 h；高度 516 km（半径−6371.2）
== 纬度带中位 N_ion（1e3 cm^-3），全天所有经度；比值 = 05-11 / 05-08
-- 降轨 ≈11 LT（白天）
   纬度带     05-08    05-11   比值
    -70.. -60     112       70   0.62
    -60.. -50     141       97   0.69
    -50.. -40     177      118   0.67
    -40.. -30     220      168   0.76
    -30.. -20     276      325   1.18
    -20.. -10     415      624   1.50
    -10..  +0     903      844   0.93
     +0.. +10    1079      791   0.73
    +10.. +20     987      512   0.52
    +20.. +30     652      195   0.30
    +30.. +40     400      120   0.30
    +40.. +50     262       82   0.31
    +50.. +60     199       61   0.31
    +60.. +70     175       56   0.32
-- 升轨 ≈23 LT（夜间）
   纬度带     05-08    05-11   比值
    -70.. -60      34       64   1.88
    -60.. -50      55       69   1.24
    -50.. -40      40       75   1.85
    -40.. -30      75      125   1.66
    -30.. -20      80      475   5.92
    -20.. -10      87      319   3.66
    -10..  +0     374      130   0.35
     +0.. +10     608      255   0.42
    +10.. +20     747      227   0.30
    +20.. +30     534      216   0.40
    +30.. +40     319      209   0.66
    +40.. +50     243       87   0.36
    +50.. +60     190       58   0.30
    +60.. +70     187       60   0.32
== 美洲扇区单轨（白天降轨，赤道穿越经度最接近 −75°），每 10° 纬度取 ±1° 中位 N_ion（1e3 cm^-3）
   0508: 赤道 UT 16.93 h 经度   -86.7  | 纬度 +50…−50:   230   317   425   683  1000  1359   948  1519   384   116    74
   0511: 赤道 UT 16.04 h 经度   -77.1  | 纬度 +50…−50:    44    64    76   150   489   323   311   273   221   279   148
== 对账：CDF 2024-05-11T16:00:00.197 N_ion 483458.0389614415 Flags_N_ion 20
```

读法：
- **用哪个密度**：`N_ion`（离子电流导出，旧名 `Ne`）。`N_elec` 当天 16,320 个负值、19.5% 带 30/40（低增益/不可用），不要直接用。`T_elec` 原始值从 −5.5e6 到 2.4e6 K，**必须**按 `Flags_T_elec∈{20,21}` 过滤，之后 p1–p99 = 1858–6309 K。
- **Flags_N_ion**（Handbook 表 6-4）：10 = 名义 + 有标定偏差 + 有随机误差；19/21 = 该区域无标定偏差（对应 `dN_ion` 为 NaN）；20 = 有标定、无随机误差；22/23 = 检测到人工尖峰；30 = 低增益探针；40 = 不可用。本文过滤（**本文自定**）：只留 20/21，当天保留 99.10%。`Flags_LP`：1 高增益、5 混合增益、9 = 该时刻做了扫描，数值是上一秒复制。`Flagbits1/2` 是逐位的详细错误，Handbook 说一般用 `Flags_*` 就够了。
- **轨道**：Swarm B 高 ~516 km，降轨 ≈11 LT（白天）、升轨 ≈23 LT（夜间），05-08→05-11 只漂了 ~0.25 h LT，可以直接比。
- **磁暴特征（05-11 相对 05-08，全经度纬度带中位）**：
  - 白天：北半球（夏季）+20° 以北 N_ion 只剩 **0.30–0.32 倍**（负相磁暴），南半球 −20..−10° 反而 **1.50 倍**，赤道 0.73–0.93。
  - 夜间：赤道 ±20° 降到 **0.30–0.42 倍**，南半球 −30..−20° 升到 **5.9 倍**，−20..−10° 3.7 倍（南半球冬季夜间的增强带；IBI 当晚在美洲扇区南纬 36–42° 也报了“确认泡”，见 3.6）。
  - 美洲扇区单轨（白天，~16 UT）：05-08 是典型双驼峰（北峰 1359k、南峰 1519k），05-11 峰全没了，+50°N 从 230k 掉到 **44k（−81%）**。
- HAPI 首行与 CDF 对账：`N_ion 483458.0389614415`、Flags 20，逐位相同。

### 3.5 TEC：绝对/相对 TEC、仰角门限、DCB（`tec.py`，原样）

```python
# Swarm B TECxTMS_2F 2024-05-11：绝对/相对 STEC、仰角门限、DCB、隐含映射高度
import numpy as np, cdflib
c = cdflib.CDF('SW_OPER_TECBTMS_2F_20240511T000000_20240511T235959_0502.cdf')
t = c.varget('Timestamp'); prn = c.varget('PRN'); el = c.varget('Elevation_Angle')
sa, va, sr = c.varget('Absolute_STEC'), c.varget('Absolute_VTEC'), c.varget('Relative_STEC')
rms = c.varget('Relative_STEC_RMS'); R = c.varget('Radius'); lat = c.varget('Latitude'); lon = c.varget('Longitude')
print('记录', t.size, '| 历元', np.unique(t).size, '| PRN 数', np.unique(prn).size, '| 每历元链路中位', int(np.median(np.unique(t, return_counts=True)[1])))
print('Radius：UNITS 属性写 %s，但数值中位 %.1f → 实为 m' % (c.varattsget('Radius')['UNITS'], np.median(R)))
R = R / 1e3   # 换成 km
print('DCB = %.3f ± %.3f TECU（每天一个值）' % (float(c.varget('DCB')), float(c.varget('DCB_Error'))))
print('仰角：最小 %.1f°，p50 %.1f°；>=50° 的链路 %.1f%%' % (el.min(), np.median(el), 100 * (el >= 50).mean()))
print('Absolute_STEC 最小 %.2f、负值 %d；Relative_STEC 范围 %.1f..%.1f TECU；Relative_STEC_RMS 中位 %.2f' % (sa.min(), (sa < 0).sum(), sr.min(), sr.max(), np.median(rms)))
# 同一连续弧：Absolute_STEC − Relative_STEC 应为常数（相对 TEC = 载波相位，差一个整弧常数）
arcs = []
for p in np.unique(prn):
    i = np.where(prn == p)[0]; brk = np.where(np.diff(t[i]) > 60_000)[0]   # >60 s 视为断弧（本文自定）
    for seg in np.split(i, brk + 1):
        if seg.size >= 300: arcs.append(np.std(sa[seg] - sr[seg]))
print('弧段(>=300 点) %d 条：弧内 std(Abs_STEC − Rel_STEC) 中位 %.2e、最大 %.2e TECU → 相对 TEC 只差一个整弧常数' % (len(arcs), np.median(arcs), np.max(arcs)))
# 隐含的单层映射高度：M = Abs_STEC/Abs_VTEC = 1/sqrt(1-(R cosE/(R+h))^2) → h
m = (el > 15) & (va > 1)
M = sa[m] / va[m]; h = R[m] * np.cos(np.radians(el[m])) / np.sqrt(1 - 1 / M**2) - R[m]
print('由 Abs_STEC/Abs_VTEC 反推单层高度（卫星以上）：中位 %.0f km（p5–p95 %.0f–%.0f）' % (np.median(h), *np.percentile(h, [5, 95])))
# 每历元 VTEC：推荐仰角 ≥ 50°（handbook）
ut = (t / 1000 % 86400) / 3600; lt = (ut + lon / 15) % 24
for cut in (20, 50):
    s = el >= cut
    ue, inv = np.unique(t[s], return_inverse=True)
    med = np.array([np.median(v) for v in np.split(va[s][np.argsort(inv)], np.cumsum(np.bincount(inv))[:-1])])
    lte = lt[s][np.unique(inv, return_index=True)[1]]
    day = (lte > 8) & (lte < 14); night = (lte > 20) | (lte < 2)
    print(f'仰角 ≥{cut}°：有 VTEC 的历元 {ue.size}（{100*ue.size/86400:.0f}% 的秒）；每历元中位 VTEC：白天(8–14 LT) 中位 {np.median(med[day]):.1f}、夜间(20–02 LT) {np.median(med[night]):.1f}、全天 p99 {np.percentile(med,99):.1f} TECU')
# 与 IPIR 的 mVTEC（>30°）对一下
ip = cdflib.CDF('SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.cdf')
ti, mv = ip.varget('Timestamp'), ip.varget('mVTEC')
s = el >= 30; ue, inv = np.unique(t[s], return_inverse=True)
med30 = np.array([np.median(v) for v in np.split(va[s][np.argsort(inv)], np.cumsum(np.bincount(inv))[:-1])])
j = np.searchsorted(ti, ue); ok = (j < ti.size) & (np.abs(ti[np.minimum(j, ti.size-1)] - ue) < 500) & np.isfinite(mv[np.minimum(j, ti.size-1)])
d = med30[ok] - mv[j[ok]]
print('自算 VTEC(≥30° 中位) − IPIR mVTEC：N=%d，中位差 %.3f TECU，|差|p95 %.3f' % (ok.sum(), np.median(d), np.percentile(np.abs(d), 95)))
```

输出（原样）：

```text
记录 465715 | 历元 86400 | PRN 数 31 | 每历元链路中位 5
Radius：UNITS 属性写 km，但数值中位 6886798.1 → 实为 m
DCB = -7.183 ± 0.900 TECU（每天一个值）
仰角：最小 19.9°，p50 37.8°；>=50° 的链路 26.4%
Absolute_STEC 最小 -1.74、负值 4；Relative_STEC 范围 -12.5..176.3 TECU；Relative_STEC_RMS 中位 0.83
弧段(>=300 点) 365 条：弧内 std(Abs_STEC − Rel_STEC) 中位 3.72e-10、最大 3.28e-09 TECU → 相对 TEC 只差一个整弧常数
由 Abs_STEC/Abs_VTEC 反推单层高度（卫星以上）：中位 193 km（p5–p95 185–197）
仰角 ≥20°：有 VTEC 的历元 86400（100% 的秒）；每历元中位 VTEC：白天(8–14 LT) 中位 9.7、夜间(20–02 LT) 6.6、全天 p99 57.5 TECU
仰角 ≥50°：有 VTEC 的历元 72251（84% 的秒）；每历元中位 VTEC：白天(8–14 LT) 中位 11.2、夜间(20–02 LT) 8.3、全天 p99 59.9 TECU
自算 VTEC(≥30° 中位) − IPIR mVTEC：N=86400，中位差 0.222 TECU，|差|p95 1.301
```

读法：
- 一行 = 一个历元 × 一条 Swarm→GPS 链路（1 Hz，每历元 ~5 条），是**卫星轨道以上**（~516 km 以上，主要是顶部电离层 + 等离子体层）的 TEC，不能和地面 GIM 的 VTEC 直接比数。
- **Relative_STEC**：载波相位 L1/L2 组合，精确但每条连续弧差一个未知常数；**Absolute_STEC**：把相位弧拉到伪距上（levelling）并扣掉 GPS 发射端 DCB（`AUX_DCB_2F`）和接收机 DCB（文件里的 `DCB`，当天 −7.183 ± 0.900 TECU）。实测弧内 `Absolute_STEC − Relative_STEC` 的 std 只有 1e-10 量级：两者就差一个整弧常数。
- **Absolute_VTEC** = Absolute_STEC ÷ 映射函数。用比值反推，若按单层薄壳解释，壳高约在卫星以上 190 km（p5–p95 185–197）——实际映射细节没在文件里写明，**别自己按 400 km 薄壳再映射一次**。
- **仰角**：文件里最低 19.9°（产品本身已切 ~20°）；Handbook 建议用 Absolute_VTEC 时取 **仰角 ≥ 50°**。≥50° 时 84% 的秒还有值，白天/夜间中位 VTEC 11.2 / 8.3 TECU；只用 ≥20° 会偏低（9.7 / 6.6）。IPIR 的 `mVTEC` 用的是 ≥30°，自算 ≥30° 中位与它差 0.22 TECU。
- `Radius` 的 UNITS 属性写 km，**数值是米**。

### 3.6 IPIR（含 PCP）、IBI、EEF（`l2.py`，原样）

```python
# Swarm B 2024-05-11：IPIR（含 PCP_flag）、IBI、EEF 的关键字段统计
import collections, numpy as np, cdflib
cnt = lambda x: sorted(collections.Counter(np.asarray(x).tolist()).items())
ip = cdflib.CDF('SW_OPER_IPDBIRR_2F_20240511T000000_20240511T235959_0302.cdf')
g = {v: ip.varget(v) for v in ('Timestamp', 'Latitude', 'Longitude', 'Ne', 'IPIR_index', 'Ionosphere_region_flag', 'PCP_flag', 'Ne_quality_flag', 'IBI_flag', 'RODI10s', 'mROTI10s', 'Num_GPS_satellites')}
print('== IPIR IPDBIRR_2F 0302：', g['Ne'].size, '点（1 Hz）；Ne NaN', np.isnan(g['Ne']).sum())
print('   Ionosphere_region_flag', cnt(g['Ionosphere_region_flag']))
print('   IPIR_index           ', cnt(g['IPIR_index']))
print('   PCP_flag             ', cnt(g['PCP_flag']))
print('   Ne_quality_flag      ', cnt(g['Ne_quality_flag']))
print('   IBI_flag             ', cnt(g['IBI_flag']))
names = {0: '赤道', 1: '中纬', 2: '极光椭圆', 3: '极盖'}
for r in range(4):
    m = g['Ionosphere_region_flag'] == r
    hi = m & (g['IPIR_index'] >= 6)
    print(f"   区域 {r} {names[r]:4s}: {m.sum():6d} 点，IPIR>=6（高）{hi.sum():5d}（{100*hi.sum()/max(m.sum(),1):4.1f}%），RODI10s 中位 {np.nanmedian(g['RODI10s'][m]):8.0f} cm^-3/s，mROTI10s 中位 {np.nanmedian(g['mROTI10s'][m]):.4f} TECU/s")
k = np.nanargmax(np.where(np.isfinite(g['RODI10s']), g['RODI10s'], -1))
print('   RODI10s 最大 %.0f cm^-3/s @ %s  lat %.1f lon %.1f  IPIR_index %d  区域 %d' % (g['RODI10s'][k], cdflib.cdfepoch.encode(g['Timestamp'][k]), g['Latitude'][k], g['Longitude'][k], g['IPIR_index'][k], g['Ionosphere_region_flag'][k]))
ib = cdflib.CDF('SW_OPER_IBIBTMS_2F_20240511T000000_20240511T235959_0502.cdf')
bi, fb, pb = ib.varget('Bubble_Index'), ib.varget('Flags_Bubble'), ib.varget('Bubble_Probability')
print('== IBI IBIBTMS_2F：Bubble_Index', cnt(bi), '| Flags_Bubble', cnt(fb))
if (bi == 1).any():
    t, la, lo = ib.varget('Timestamp'), ib.varget('Latitude'), ib.varget('Longitude')
    i = np.where(bi == 1)[0]; seg = np.split(i, np.where(np.diff(i) > 60)[0] + 1)
    print('   bubble 段数（间隔 >60 s 断开）', len(seg))
    for s in seg[:8]:
        ut = (t[s[0]] / 1000 % 86400) / 3600
        print('   %s  %3d s  lat %5.1f..%5.1f lon %6.1f  LT %.1f  prob max %.1f  Flags_Bubble %s' % (cdflib.cdfepoch.encode(t[s[0]])[:19], s.size, la[s].min(), la[s].max(), lo[s[0]], (ut + lo[s[0]] / 15) % 24, pb[s].max(), sorted(set(fb[s].tolist()))))
ee = cdflib.CDF('SW_OPER_EEFBTMS_2F_20240511T000000_20240511T235959_0502.cdf')
t, lo, E, RE, F = (ee.varget(v) for v in ('Timestamp', 'Longitude', 'EEF', 'RelErr', 'Flags'))
lt = ((t / 1000 % 86400) / 3600 + lo / 15) % 24; daym = (lt > 6) & (lt < 18)
print('== EEF EEFBTMS_2F：%d 次磁赤道穿越（白天 %d、夜间 %d）；Flags %s' % (E.size, daym.sum(), (~daym).sum(), cnt(F)))
print('   白天 EEF 中位 %.3f mV/m、RelErr 中位 %.2f；夜间 EEF 中位 %.3f、RelErr 中位 %.2f' % (np.median(E[daym]), np.median(RE[daym]), np.median(E[~daym]), np.median(RE[~daym])))
good = RE < 1  # 本文自定：RelErr<1 才看
print('   EEF 全部 中位 %.3f mV/m（范围 %.2f..%.2f）；RelErr<1 的 %d 次 中位 %.3f mV/m' % (np.median(E), E.min(), E.max(), good.sum(), np.median(E[good])))
for i in range(0, E.size, 4):
    ut = (t[i] / 1000 % 86400) / 3600
    print('   %s lon %7.1f LT %4.1f  EEF %+6.2f mV/m  RelErr %.2f' % (cdflib.cdfepoch.encode(t[i])[:19], lo[i], (ut + lo[i] / 15) % 24, E[i], RE[i]))
```

输出（原样）：

```text
== IPIR IPDBIRR_2F 0302： 86400 点（1 Hz）；Ne NaN 12
   Ionosphere_region_flag [(0, 28866), (1, 35014), (2, 9633), (3, 12887)]
   IPIR_index            [(1, 625), (2, 6338), (3, 23616), (4, 31147), (5, 17841), (6, 5277), (7, 1272), (8, 284)]
   PCP_flag              [(0, 85343), (1, 745), (4, 300), (99999, 12)]
   Ne_quality_flag       [(10000, 43511), (19000, 14215), (20000, 28662), (99999, 12)]
   IBI_flag              [(-1, 70743), (0, 13204), (1, 2452), (99999, 1)]
   区域 0 赤道  :  28866 点，IPIR>=6（高） 1601（ 5.5%），RODI10s 中位      376 cm^-3/s，mROTI10s 中位 0.0043 TECU/s
   区域 1 中纬  :  35014 点，IPIR>=6（高） 2251（ 6.4%），RODI10s 中位      458 cm^-3/s，mROTI10s 中位 0.0093 TECU/s
   区域 2 极光椭圆:   9633 点，IPIR>=6（高） 1405（14.6%），RODI10s 中位      885 cm^-3/s，mROTI10s 中位 0.0180 TECU/s
   区域 3 极盖  :  12887 点，IPIR>=6（高） 1576（12.2%），RODI10s 中位      608 cm^-3/s，mROTI10s 中位 0.0155 TECU/s
   RODI10s 最大 166902 cm^-3/s @ 2024-05-11T12:00:14.197  lat -19.4 lon 162.8  IPIR_index 8  区域 0
== IBI IBIBTMS_2F：Bubble_Index [(-1, 70744), (0, 13130), (1, 2526)] | Flags_Bubble [(0, 13130), (1, 523), (2, 2003), (16, 5694), (32, 65050)]
   bubble 段数（间隔 >60 s 断开） 28
   2024-05-11T04:00:07  104 s  lat -42.4..-35.9 lon  -78.0  LT 22.8  prob max 0.9  Flags_Bubble [1]
   2024-05-11T04:15:14    1 s  lat  14.9.. 14.9 lon  -79.1  LT 23.0  prob max 0.0  Flags_Bubble [2]
   2024-05-11T04:21:50   40 s  lat  40.0.. 42.4 lon  -79.5  LT 23.1  prob max 0.0  Flags_Bubble [2]
   2024-05-11T05:38:46  160 s  lat -27.9..-16.4 lon -101.9  LT 22.9  prob max 0.7  Flags_Bubble [1, 2]
   2024-05-11T05:46:21  136 s  lat   0.9..  9.4 lon -102.5  LT 22.9  prob max 0.2  Flags_Bubble [2]
   2024-05-11T05:52:42  277 s  lat  25.0.. 42.5 lon -103.1  LT 23.0  prob max 0.0  Flags_Bubble [2]
   2024-05-11T10:19:48   13 s  lat -40.7..-36.1 lon -173.1  LT 22.8  prob max 0.0  Flags_Bubble [2]
   2024-05-11T10:22:06    1 s  lat -32.0..-32.0 lon -173.1  LT 22.8  prob max 0.0  Flags_Bubble [2]
== EEF EEFBTMS_2F：29 次磁赤道穿越（白天 15、夜间 14）；Flags [(0, 29)]
   白天 EEF 中位 -0.028 mV/m、RelErr 中位 0.96；夜间 EEF 中位 1.475、RelErr 中位 0.99
   EEF 全部 中位 -0.004 mV/m（范围 -6.38..9.37）；RelErr<1 的 16 次 中位 0.232 mV/m
   2024-05-11T00:12:29 lon   160.9 LT 10.9  EEF  -0.11 mV/m  RelErr 1.33
   2024-05-11T04:08:24 lon   -78.4 LT 22.9  EEF  +6.66 mV/m  RelErr 1.03
   2024-05-11T07:19:41 lon  -126.2 LT 22.9  EEF  +4.26 mV/m  RelErr 1.02
   2024-05-11T10:31:04 lon  -173.9 LT 22.9  EEF  -2.41 mV/m  RelErr 0.81
   2024-05-11T13:42:10 lon   138.4 LT 22.9  EEF  -4.73 mV/m  RelErr 1.01
   2024-05-11T16:51:35 lon    90.8 LT 22.9  EEF  +9.37 mV/m  RelErr 1.01
   2024-05-11T20:01:09 lon    43.2 LT 22.9  EEF  +8.44 mV/m  RelErr 1.53
   2024-05-11T23:11:52 lon    -4.4 LT 22.9  EEF  -0.56 mV/m  RelErr 1.02
```

读法：
- **IPIR** `IPIR_index`：0–3 低、4–5 中、≥6 高（Handbook）。05-11 高值比例：极光椭圆 14.6%、极盖 12.2%、中纬 6.4%、赤道 5.5%；RODI10s 最大 1.67e5 cm⁻³/s 在 12:00 UT 西太平洋 −19.4°（夜间）。`Ionosphere_region_flag` 0 赤道 / 1 中纬 / 2 极光椭圆 / 3 极盖。`PCP_flag` 0 不在斑块、1 斑块边缘（无漂移数据时分不出前后沿）、2 前沿、3 后沿、4 斑块内部：当天 745 点边缘、300 点内部。`Ne_quality_flag` 是 10000/19000/20000 这类编码（对应 LP 的 10/19/20 放大 1000 倍，本文推断）。**99999 = 填充值**，统计前要去掉。
- **IBI** `Bubble_Index`：1 泡、0 平静、−1 未分析；`Flags_Bubble`：0 平静、1 确认、2 未确认、4 未滤波残差大峰、8 时间缺口、16 峰太多、32 不在赤道段/无效纬度或 LT。`Bubble_Index=1` 的 2526 点里只有 523 点是“确认”（Flags 1），其余 2003 点“未确认”。IBI 是用**磁场**信号找泡的，南纬 36–42° 那段“确认泡”发生在磁暴夜间的中纬增强带，更像磁暴结构而不是经典赤道泡，解读要谨慎。
- **EEF**：每次磁赤道穿越一个值（29 次 = 白天 15 + 夜间 14）。赤道电急流是白天现象，**夜间那 14 个值不要当真**；当天白天 EEF 中位 −0.03 mV/m、RelErr 中位 0.96（RelErr ≈ 1 表示模型几乎没拟合上），磁暴日的 EEF 质量很差。附带 81 点的 EEJ 电流剖面（QD 纬度 −20..+20，0.5° 步长）。

## 4. 目录与文件名

```text
https://swarm-diss.eo.esa.int/#swarm/                 （网页；脚本用 ?do=list / ?do=download）
├── Level1b/{Latest_baselines,Entire_mission_data}/   EFIx_LP EFIxLPI LP_x_CA MAGx_LR MAGx_HR GPSx_RO MODx_SC …（每项旁有 <项>.txt 清单）
├── Level2daily/{Latest_baselines,Entire_mission_data}/ TEC/TMS IPD/IRR IBI/TMS EEF/TMS FAC AEJ AOB MIT PPI TIX NIX DNS …
├── Level2longterm/                                   MCO MIO MLI CFW …（磁场模型）
├── Fast/{Level1b,Level2}/                            FAST 近实时（Level2 只有 AEJ AOB FAC TEC）
├── Advanced/Plasma_Data/                             16 Hz 面板密度、2 Hz LP 扩展、TII 横向漂移 等科研数据集
└── Multimission/
```

文件名：`SW_<OPER|FAST>_<产品 10 字符>_<起始 UTC>_<结束 UTC>_<BBVV>.<CDF.ZIP|ZIP|cdf>`；产品 10 字符里第 4 个字符是卫星（A/B/C），例如 `EFIB_LP_1B`、`TECBTMS_2F`、`IPDBIRR_2F`。Level1b 的 ZIP 叫 `.CDF.ZIP`，Level2 的叫 `.ZIP`。

## 5. 关键变量速查

| 产品 | 变量 | 单位 | 注意 |
|---|---|---|---|
| EFIx_LP_1B / EFIxLPI_1B | `N_ion`、`N_elec`、`T_elec`、`Vs` | cm⁻³、K、V | 2 Hz 原始 / 1 Hz 整秒插值；0701 起 `Ne→N_ion`、`Te→T_elec`、`Flags_Ne→Flags_N_ion` |
| 同上 | `dN_ion`、`dT_elec` | cm⁻³、K | 相对 ISR 的建议标定修正，NaN = 该区域无标定；`dT_elec` 的 UNITS 属性误写成 cm-3 |
| 同上 | `Flags_LP`、`Flags_N_ion`、`Flags_N_elec`、`Flags_T_elec`、`Flags_Vs`、`Flagbits1/2` | — | 见 3.4 |
| TECxTMS_2F | `Absolute_STEC`、`Absolute_VTEC`、`Relative_STEC`、`Relative_STEC_RMS`、`Elevation_Angle`、`PRN`、`DCB` | TECU、° | `Radius` 实为 m；`GPS_Position` km、`LEO_Position` m |
| IPDxIRR_2F | `Ne`、`Background_Ne`、`Foreground_Ne`、`RODI10s/20s`、`delta_Ne10s/20s/40s`、`mVTEC`、`mROTI10s/20s`、`IPIR_index`、`PCP_flag`、`Ionosphere_region_flag`、`IBI_flag`、`Ne_quality_flag` | cm⁻³、TECU | 1 Hz；99999 填充 |
| IBIxTMS_2F | `Bubble_Index`、`Bubble_Probability`、`Flags_Bubble` | — | 1 Hz；磁场法 |
| EEFxTMS_2F | `EEF`、`RelErr`、`Flags`、`EEJ_meast`、`EEJ_mnorth` | mV/m、A/km | 每次赤道穿越一行 |

## 6. 在工作流里接哪一步

- [A · 一日 TEC](./README.md#a--一日-tec)：Swarm TEC 给的是**卫星以上**的 TEC，可以当“地面 GIM − 顶部”的分解约束；LP 的 `N_ion` 是 ~460–516 km 的原位值，适合校验 IRI/NeQuick 顶部。
- [B · 不规则体 / 磁暴](./README.md#b--不规则体--磁暴)：3.4 的纬度带比值就是磁暴正/负相的沿轨证据；IPIR（RODI/mROTI/IPIR_index）、IBI、PCP_flag 直接给不规则体标签；要自己从 LP/TEC 算指数用 [titipy](./titipy.md)；地面对应用 [oasis-roti](./oasis-roti.md) 或 [giro-ionosonde](./giro-ionosonde.md)。
- 批量：先下 `<产品>.txt` 清单，按日期 grep，再逐个 `?do=download`；只要几个变量/几小时就用 VirES HAPI。

## 7. 坑（现象 → 原因 → 修复）

1. **FTP 登录 530** → swarm-diss 的 FTP 明确 “No anonymous login” → 不想注册就用 HTTPS `?do=download`；脚本里别写匿名 FTP（Handbook 页面上仍列着 ftp:// 链接）。
2. **`https://swarm-diss.eo.esa.int/swarm/...` 403** → 没有静态文件树，只有 PHP 文件管理器接口 → 用 `?do=list&file=` 和 `?do=download&file=`，路径里的 `/` 编码成 `%2F`。
3. **老脚本读 `Ne`/`Te`/`Flags_Ne` 报 KeyError（HAPI 报 1407 unknown parameter）** → LP 基线 0701 起改名 → 用 `N_ion`/`T_elec`/`Flags_N_ion`/`Flags_T_elec`（[titipy](./titipy.md) 也要这个补丁）；IPIR 里仍叫 `Ne`。
4. **`N_elec` 有大量负值、`T_elec` 到 ±百万 K** → 没按 flag 过滤；`N_elec` 低增益/不可用占 ~20% → 密度用 `N_ion` 并留 `Flags_N_ion∈{20,21}`（本文自定，去掉尖峰 22/23）；温度留 `Flags_T_elec∈{20,21}`。
5. **Latest_baselines 里同一天有两个版本（IPIR 0301 和 0302）** → 目录不是“每天唯一文件” → 按日期分组取最大 `BBVV`；LP 在 2025-12-13 从 0701 切到 0702，长序列要注意跨基线。
6. **以为 L2 产品 6–10 min 就上架** → Handbook 写的是处理时延；OPER 文件实测 3–9 天后才出现（IPIR 最慢） → 要近实时用 `Fast/`（LP、TEC ~40 min），其余等。
7. **ZIP 里的 `.EEF` 当成电场产品** → 那是 Earth Explorer File 格式的 DQC 质量报告 → 电场在 `EEFxTMS_2F` 的 `.cdf` 里。
8. **TEC 文件 `Radius` 当 km 用，结果高度离谱** → UNITS 属性写 km，数值是 m（LP 文件是 m 且写 m）→ 读完先看数量级再用；`dT_elec` 的 UNITS 也写错成 cm-3。
9. **拿 Swarm Absolute_VTEC 和地面 GIM 比，差好几倍** → Swarm TEC 只积分卫星以上；低仰角映射误差大 → 只比“顶部 TEC”，并按 Handbook 取仰角 ≥ 50°；别自己再套 400 km 薄壳。
10. **把 IBI 的 `Bubble_Index=1` 全当成等离子体泡** → 其中大部分是 `Flags_Bubble=2`（未确认），磁暴时中纬结构也会触发 → 只取 `Flags_Bubble==1`，并结合 LP 密度看。
11. **EEF 夜间也有值** → 文件对每次磁赤道穿越都给值，但赤道电急流只在白天有意义；磁暴日 RelErr ≈ 1 → 只用白天（6–18 LT）且 RelErr 小的点（阈值本文未定）。
12. **统计里混进 99999** → IPIR 各 flag 的填充值 → 先 `!= 99999`。
13. **脚本叫 `inspect.py`，一 import cdflib 就循环导入报错** → 和 Python 标准库 `inspect` 重名，numpy 导入时被劫持 → 别用标准库模块名给脚本命名（本机实测踩到）。
14. **VirES HAPI 一次请求太长被拒** → `x_maxTimeSelection`：LP `P2DT12H`（2.5 天）、TEC `P5D` → 按天循环；数据条款见 `https://vires.services/data_terms`。
15. **同名同版本文件内容变了** → 2024-05-11 的 TEC/IBI 在 2026-08 被重新生成（mtime、HDR `Creation_Date`、DQC 报告日期都变了）→ 复现实验要记录 mtime 或存 HDR。

## 8. 选型对比

| 需求 | 选这个 | 不选这个 |
|---|---|---|
| 整天整颗卫星的原始 CDF，免注册 | **swarm-diss HTTPS `?do=`**（本文 E24） | FTP（要账号） |
| 几小时、几个变量，免注册 | **VirES HAPI**（本文 E25） | 下整天 ZIP |
| 模型残差、磁坐标、多卫星合并 | [viresclient](./viresclient.md)（要 token） | HAPI（没有模型） |
| RODI/ROTI/ROTEI 自己算 | [titipy](./titipy.md) | IPIR 现成值（窗口固定 10/20 s） |
| 近实时（< 1 h） | `Fast/` 目录或 HAPI `SW_FAST_*` | OPER（3–9 天） |
| 垂直剖面 | [cosmic2-ro](./cosmic2-ro.md) / [giro-ionosonde](./giro-ionosonde.md) | Swarm（只有轨道高度原位值） |
