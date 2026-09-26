# GIM / IONEX 产品门户：各分析中心匿名下载路径、新旧文件名、时延与 2024-05-11 多中心对 CODE 实测

入口：[CODE/AIUB](https://download.aiub.unibe.ch/CODE/) · [CAS 汇总镜像](https://data.bdsmart.cn/pub/product/iono/ionex/) · [UPC TOMION](https://chapman.upc.es/tomion/) · [ESA Navigation Office](http://navigation-office.esa.int/products/gnss-products/) · [JPL sideshow iono_daily](https://sideshow.jpl.nasa.gov/pub/iono_daily/) · [CDDIS ionex（需 Earthdata）](https://cddis.nasa.gov/archive/gnss/products/ionex/) · 本机验证 **2026-09-26 05:00–05:10 EDT**（全部匿名 curl，无注册、无表单）

> 岗位：回答“某天某中心的 GIM 去哪匿名拿、叫什么名字、出来要等多久、各家差多少”。**只管门户这一侧**：读 IONEX 的 Python API 见 [ionex-gim](./ionex-gim.md)（同包 [ionex](./ionex.md)、Rust 版 [ionex-rs](./ionex-rs.md)）；自建 GIM 见 [sh-gim](./sh-gim.md)、[mosgim2](./mosgim2.md)；单站 TEC 见 [pytecgg](./pytecgg.md)；近实时 TEC 产品另见 [realtime-iono-products](./realtime-iono-products.md)。本文不重复这些。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E27](../data-access.md#dp-e27)
>
> 冲突时：文件内容以解压后 IONEX 头 `PGM / RUN BY / DATE` 为准（同名文件不同源可能是不同版本，见坑 3）；时延以本页实测列表时间为准，只代表 2026-09 这一周；“均差 / RMS / 面积加权 / 公共历元”这些统计口径都是**本文自选**，不是任何中心的官方精度。

## 1. 用途与边界

**做：** 各分析中心（CODE、UPC、ESA、JPL、CAS、WHU、NRCan/EMR、IGS 综合）IONEX 的匿名 HTTPS 路径；旧短名 ↔ 新长名对照；最终 / 快速 / 预报 / 实时各档的实测上架时延；同一天各中心 VTEC 图逐格点对 CODE 的均差与 RMS。

**不做：** IONEX 解析库用法（→ [ionex-gim](./ionex-gim.md)）；DCB / 硬件延迟；自建球谐；GloTEC / US-TEC 这类区域近实时产品（→ [realtime-iono-products](./realtime-iono-products.md)）。

**结论先说：**

| 中心 | 匿名可用的路径（本机 200） | 备注 |
| --- | --- | --- |
| **CAS 汇总镜像** | `https://data.bdsmart.cn/pub/product/iono/ionex/YYYY/DDD/` | **一个目录里有 CAS/COD/EMR/ESA/IGS/JPL/UPC（+2024 年 WHU 旧短名）**，有索引页，最省事；但**没有 CODE 最终的 2026 文件**、**2026 年未见 WHU**、IGS 最终 2026 未见 |
| CODE（AIUB） | `https://download.aiub.unibe.ch/CODE/YYYY/`（最终）· `…/CODE/`（快速 / 预报） | 301 到 Switch S3，**无索引页**，须给全名；S3 桶 `?prefix=` 列表可用 |
| UPC | `https://chapman.upc.es/tomion/rapid/YYYY/DDD_YYMMDD.15min/`（`.Z`）· 实时 `…/real-time/quick/last_results/` | 实时 usrg 每 15 min 更新 |
| ESA | `http://navigation-office.esa.int/products/gnss-products/WWWW/`（GPS 周目录） | 与镜像上的**同名文件内容不同**（重处理版） |
| JPL | `https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_final/yYYYY/` · `IONEX_rapid/` | **有匿名源**；README 写明 JPLG/JPLH/JPLR/JPLQ 加了 2 TECU 偏置 |
| NRCan（EMR） | 只在 CAS 镜像拿到 `EMR0OPSFIN_…_01H` | 未找到 NRCan 自家匿名 IONEX 路径，未臆造 |
| WHU | CAS 镜像 2024 年有 `whug/whrg` 旧短名 | `igs.gnsswhu.cn` http 502 / FTP 425，本次不可用 |
| CDDIS | `cddis.nasa.gov/archive/gnss/products/ionex/` | **需 Earthdata 登录**（302 到 urs.earthdata.nasa.gov），本文不走 |

**本次不通（2026-09-26 05:0x EDT）：** IGN `igs.ign.fr`（https TLS EOF / http 40 s 超时）；BKG `root_ftp/IGS/products/` 只有 `dcb/ glo_orbits/ mgex/ orbits/`，无 ionex 目录（`…/ionex/2024/132/` 404）；KASI `nfs.kasi.re.kr` https/ftp 均 000；ESA GSSC `ftp://gssc.esa.int` 21 端口拒连、`https://gssc.esa.int/gnss/products/ionex/…` 404。

## 2. 安装

只要 `curl`、`gzip`（`.Z` 也能用 `gzip -dc` 解）、Python 3 + numpy（对比脚本）。本机用 `/usr/bin/python3`（numpy 2.2.4）；共享机上裸 `python3` 指向别的 venv。

```bash
curl --version | head -1; gzip --version | head -1
/usr/bin/python3 -c "import numpy; print(numpy.__version__)"
```

## 3. 真命令 + 期望输出

### 3.1 门户探测、同名文件跨源比对、时延（`probe.sh`）

```bash
#!/usr/bin/env bash
# 各门户匿名探测（只 HEAD/列目录/拉 2024-05-11 一天）
M=https://data.bdsmart.cn/pub/product/iono/ionex          # CAS 镜像：各中心 IONEX 汇总
echo "## 1) CAS 镜像 2024/132 文件名（长名 + 旧短名并存）"
curl -s -m 40 $M/2024/132/ | grep -o 'href="[A-Za-z0-9_]*\.[^"?/]*"' | sed 's/href=//;s/"//g' | tr '\n' ' '; echo
echo "## 2) 同一文件在各源站 vs 镜像：解压后 md5"
get(){ curl -sL -m 60 -o "$1" -w "%{http_code} %{size_download} B  $1\n" "$2"; }
get cod_aiub.gz https://download.aiub.unibe.ch/CODE/2024/COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz
get cod_cas.gz  $M/2024/132/COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz
get jpl_side.gz https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_final/y2024/JPL0OPSFIN_20241320000_01D_02H_GIM.INX.gz
get jpl_cas.gz  $M/2024/132/JPL0OPSFIN_20241320000_01D_02H_GIM.INX.gz
get upc_chap.Z  https://chapman.upc.es/tomion/rapid/2024/132_240511.15min/UPC0OPSFIN_20241320000_01D_02H_GIM.INX.Z
get upc_cas.gz  $M/2024/132/UPC0OPSFIN_20241320000_01D_02H_GIM.INX.gz
get esa_nav.gz  http://navigation-office.esa.int/products/gnss-products/2313/ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz
get esa_cas.gz  $M/2024/132/ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz
for f in cod_aiub.gz cod_cas.gz jpl_side.gz jpl_cas.gz upc_chap.Z upc_cas.gz esa_nav.gz esa_cas.gz; do
  printf '%s  %s  ' "$(gzip -dc $f | md5sum | cut -c1-12)" "$f"; gzip -dc $f | sed -n 2p | cut -c41-60; done
echo "## 3) 旧短名：CODE 源站已不给"
curl -sIL -m 30 -o /dev/null -w '%{http_code} CODG1320.24I.Z @AIUB\n' https://download.aiub.unibe.ch/CODE/2024/CODG1320.24I.Z
echo "## 4) 时延：CODE 源站（S3 LastModified 为 UTC）"
curl -s -m 60 'https://zhw-b.s3.cloud.switch.ch/aiub?prefix=CODE/COD0OPS&max-keys=1000' |
  grep -o '<Key>[^<]*_GIM.INX.gz</Key><LastModified>[^<]*' | sed 's/<\/Key><LastModified>/ /;s/<Key>CODE\///' | tail -8
for d in 264 265; do printf "FIN $d: "; curl -sIL -m 30 "https://download.aiub.unibe.ch/CODE/2026/COD0OPSFIN_2026${d}0000_01D_01H_GIM.INX.gz" |
  grep -i '^HTTP\|^last-modified' | tail -2 | tr -d '\r' | tr '\n' ' '; echo; done
echo "## 5) 时延：CAS 镜像 2026/264（2026-09-21）各中心上架时刻（列表时间，未标时区）"
curl -s -m 40 $M/2026/264/ | sed 's/<[^>]*>/ /g' | grep -E 'INX' | awk '{print $1,$2,$3}'
echo "## 6) JPL 自家说明 + UPC 实时"
curl -s -m 40 https://sideshow.jpl.nasa.gov/pub/iono_daily/README.txt | grep -E 'JPL[GHQR]\*|latency|bias added' | head -12
curl -s -m 40 https://chapman.upc.es/tomion/real-time/quick/last_results/ | sed 's/<[^>]*>/ /g' | grep 'i.Z'; date -u '+now %F %H:%M UTC'
echo "## 7) CDDIS（对照）"
curl -sL -m 40 -o /dev/null -w '%{http_code} -> %{url_effective}\n' https://cddis.nasa.gov/archive/gnss/products/ionex/2024/132/ | cut -c1-70
```

输出（原样，2026-09-26 05:06–05:07 EDT）：

```text
## 1) CAS 镜像 2024/132 文件名（长名 + 旧短名并存）
CAS0OPSFIN_20241320000_01D_30M_GIM.INX.gz CAS0OPSRAP_20241320000_01D_30M_GIM.INX.gz CAS0OPSRTS_20241320000_01D_05M_GIM.INX.gz COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz COD0OPSRAP_20241320000_01D_01H_GIM.INX.gz EMR0OPSFIN_20241320000_01D_01H_GIM.INX.gz ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz ESA0OPSRAP_20241320000_01D_01H_GIM.INX.gz ESA0OPSRAP_20241320000_01D_02H_GIM.INX.gz IGS0OPSFIN_20241320000_01D_02H_GIM.INX.gz IGS0OPSRAP_20241320000_01D_02H_GIM.INX.gz JPL0OPSFIN_20241320000_01D_02H_GIM.INX.gz JPL0OPSRAP_20241320000_01D_02H_GIM.INX.gz UPC0OPSFIN_20241320000_01D_02H_GIM.INX.gz UPC0OPSRAP_20241320000_01D_01H_GIM.INX.gz UPC0OPSRAP_20241320000_01D_02H_GIM.INX.gz UPC0OPSRAP_20241320000_01D_15M_GIM.INX.gz c1pg1320.24i.Z c2pg1320.24i.Z carg1320.24i.Z casg1320.24i.Z irtg1320.24i.Z p1_casg1320.24i.Z p2_casg1320.24i.Z p5_casg1320.24i.Z uadg1320.24i.Z uhrg1320.24i.Z upcg1320.24i.Z uprg1320.24i.Z uqrg1320.24i.Z usrg1320.24i.Z whrg1320.24i.Z whug1320.24i.Z 
## 2) 同一文件在各源站 vs 镜像：解压后 md5
200 358273 B  cod_aiub.gz
200 358273 B  cod_cas.gz
200 121564 B  jpl_side.gz
200 133723 B  jpl_cas.gz
200 126627 B  upc_chap.Z
200 116402 B  upc_cas.gz
200 211978 B  esa_nav.gz
200 211419 B  esa_cas.gz
b5ac0fdcad7d  cod_aiub.gz  15-MAY-24 21:25     
b5ac0fdcad7d  cod_cas.gz  15-MAY-24 21:25     
9f44aee08588  jpl_side.gz  14-may-2024 01:59   
9f44aee08588  jpl_cas.gz  14-may-2024 01:59   
5239b740ee76  upc_chap.Z  13 May 2024 01:55   
5239b740ee76  upc_cas.gz  13 May 2024 01:55   
5e862be91610  esa_nav.gz  10-JAN-25 09:41     
066a57930071  esa_cas.gz  15-MAY-24 18:05     
## 3) 旧短名：CODE 源站已不给
404 CODG1320.24I.Z @AIUB
## 4) 时延：CODE 源站（S3 LastModified 为 UTC）
COD0OPSP4D_20262700000_01D_01H_GIM.INX.gz 2026-09-24T11:55:46.811Z
COD0OPSP4D_20262710000_01D_01H_GIM.INX.gz 2026-09-24T12:44:29.398Z
COD0OPSP4D_20262720000_01D_01H_GIM.INX.gz 2026-09-25T06:20:19.657Z
COD0OPSP4D_20262730000_01D_01H_GIM.INX.gz 2026-09-26T06:21:20.842Z
COD0OPSRAP_20262650000_01D_01H_GIM.INX.gz 2026-09-24T11:31:46.849Z
COD0OPSRAP_20262660000_01D_01H_GIM.INX.gz 2026-09-25T06:20:19.906Z
COD0OPSRAP_20262670000_01D_01H_GIM.INX.gz 2026-09-26T06:21:21.059Z
COD0OPSRAP_20262680000_01D_01H_GIM.INX.gz 2026-09-26T06:21:20.921Z
FIN 264: HTTP/2 200  last-modified: Fri, 25 Sep 2026 17:57:23 GMT 
FIN 265: HTTP/2 301  HTTP/2 404  
## 5) 时延：CAS 镜像 2026/264（2026-09-21）各中心上架时刻（列表时间，未标时区）
CAS0OPSFIN_20262640000_01D_30M_GIM.INX.gz 2026-09-24 16:58
CAS0OPSRAP_20262640000_01D_30M_GIM.INX.gz 2026-09-23 19:19
COD0OPSP0D_20262640000_01D_01H_GIM.INX.gz 2026-09-25 06:18
COD0OPSP1D_20262640000_01D_01H_GIM.INX.gz 2026-09-25 06:18
COD0OPSRAP_20262640000_01D_01H_GIM.INX.gz 2026-09-24 11:22
EMR0OPSFIN_20262640000_01D_01H_GIM.INX.gz 2026-09-23 10:34
ESA0OPSFIN_20262640000_01D_02H_GIM.INX.gz 2026-09-25 16:01
ESA0OPSRAP_20262640000_01D_01H_GIM.INX.gz 2026-09-22 07:50
ESA0OPSRAP_20262640000_01D_02H_GIM.INX.gz 2026-09-22 07:50
IGS0OPSRAP_20262640000_01D_02H_GIM.INX.gz 2026-09-23 04:18
JPL0OPSFIN_20262640000_01D_02H_GIM.INX.gz 2026-09-24 02:01
JPL0OPSRAP_20262640000_01D_02H_GIM.INX.gz 2026-09-22 06:58
UPC0OPSFIN_20262640000_01D_02H_GIM.INX.gz 2026-09-24 16:40
UPC0OPSRAP_20262640000_01D_01H_GIM.INX.gz 2026-09-24 16:40
UPC0OPSRAP_20262640000_01D_02H_GIM.INX.gz 2026-09-24 16:40
UPC0OPSRAP_20262640000_01D_15M_GIM.INX.gz 2026-09-24 16:40
## 6) JPL 自家说明 + UPC 实时
		no bias added
	JPLG* files
		50 hours latency
		2 TECU bias added
		no bias added
	JPLH* files
		50 hours latency
		2 TECU bias added
	JPLQ* files	
		7 hours	latency
		2 TECU bias added	
	JPLR* files
      usrg2690.09.00.26i.Z   2026-09-26 11:04     16K  &nbsp;  
      usrg2690.26i.Z   2026-09-26 11:04    412K  &nbsp;  
now 2026-09-26 09:07 UTC
## 7) CDDIS（对照）
200 -> https://urs.earthdata.nasa.gov/oauth/authorize?client_id=gDQnv1
```

读法：

- **镜像 vs 源站**：COD、JPL、UPC 解压后 md5 一致（压缩包字节数可以不同：JPL 121,564 vs 133,723 B，UPC `.Z` vs `.gz`）；**ESA 不一致**——Navigation Office 上是 2025-01-10 重处理版（头里 300 站），CAS 镜像是 2024-05-15 原版（275 站）。
- **时延**（本文口径：上架时刻 − 该数据日结束 24:00 UTC）：见 §5 表。

### 3.2 2024-05-11（DOY 132，强磁暴日）各中心最终图对 CODE（`cmp.py`）

先把 8 个中心最终图（+ ESA 源站版）拉到当前目录（共约 2.6 MB）：

```bash
M=https://data.bdsmart.cn/pub/product/iono/ionex/2024/132
for f in COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz CAS0OPSFIN_20241320000_01D_30M_GIM.INX.gz \
         EMR0OPSFIN_20241320000_01D_01H_GIM.INX.gz ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz \
         IGS0OPSFIN_20241320000_01D_02H_GIM.INX.gz JPL0OPSFIN_20241320000_01D_02H_GIM.INX.gz \
         UPC0OPSFIN_20241320000_01D_02H_GIM.INX.gz whug1320.24i.Z; do
  curl -s -m 60 -O -w "%{http_code} %{size_download} $f\n" $M/$f; done
curl -s -o esa_nav.gz http://navigation-office.esa.int/products/gnss-products/2313/ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz
```

本机实测：8 个全 200，大小 358,273 / 692,711 / 331,791 / 211,419 / 187,068 / 133,723 / 116,402 / 199,125 B。

对比脚本（纯 numpy 解析 IONEX，遇到 `START OF RMS MAP` 即停；`9999` 置 NaN；乘 `10**EXPONENT`）：

```python
import gzip, re, sys, glob, datetime as dt
import numpy as np
def read_ionex(path):
    op = gzip.open if path.endswith(('.gz', '.Z')) else open
    txt = op(path, 'rt', errors='replace').read().splitlines()
    hdr, i = {}, 0
    for i, l in enumerate(txt):
        lab = l[60:].strip()
        if lab == 'END OF HEADER': break
        if lab in ('EXPONENT', 'INTERVAL', '# OF MAPS IN FILE', 'LAT1 / LAT2 / DLAT', 'LON1 / LON2 / DLON',
                   'HGT1 / HGT2 / DHGT', 'PGM / RUN BY / DATE', 'MAPPING FUNCTION', '# OF STATIONS'):
            hdr[lab] = l[:60].strip()
    ex = int(hdr.get('EXPONENT', '-1'))
    la1, la2, dla = map(float, hdr['LAT1 / LAT2 / DLAT'].split())
    lo1, lo2, dlo = map(float, hdr['LON1 / LON2 / DLON'].split())
    nla, nlo = int(round((la2 - la1) / dla)) + 1, int(round((lo2 - lo1) / dlo)) + 1
    maps, cur, grid, row, vals = {}, None, None, -1, []
    for l in txt[i + 1:]:
        lab = l[60:].strip()
        if lab == 'START OF TEC MAP': grid = np.full((nla, nlo), np.nan); row = -1
        elif lab == 'EPOCH OF CURRENT MAP' and grid is not None:
            y, mo, d, h, mi, s = [int(float(x)) for x in l[:36].split()]
            cur = dt.datetime(y, mo, d, h, mi, s)
        elif lab == 'LAT/LON1/LON2/DLON/H' and grid is not None:
            if row >= 0: grid[row] = vals[:nlo]
            row += 1; vals = []
        elif lab == 'END OF TEC MAP':
            grid[row] = vals[:nlo]; grid[grid == 9999] = np.nan
            maps[cur] = grid * 10.0 ** ex; grid = None
        elif lab.startswith('START OF RMS'): break
        elif grid is not None and row >= 0:
            vals += [float(l[k:k + 5]) for k in range(0, len(l.rstrip()), 5)]
    return hdr, (la1, la2, dla, lo1, lo2, dlo), maps
files = {'COD': 'COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz', 'CAS': 'CAS0OPSFIN_20241320000_01D_30M_GIM.INX.gz',
         'EMR': 'EMR0OPSFIN_20241320000_01D_01H_GIM.INX.gz', 'ESA': 'ESA0OPSFIN_20241320000_01D_02H_GIM.INX.gz',
         'ESA(nav-office)': 'esa_nav.gz', 'IGS': 'IGS0OPSFIN_20241320000_01D_02H_GIM.INX.gz',
         'JPL': 'JPL0OPSFIN_20241320000_01D_02H_GIM.INX.gz', 'UPC': 'UPC0OPSFIN_20241320000_01D_02H_GIM.INX.gz',
         'WHU': 'whug1320.24i.Z'}
D = {k: read_ionex(v) for k, v in files.items()}
print('中心 | 程序/日期 | 图数 | 间隔 s | 格网 | 首图 | 末图 | 站数')
for k, (h, g, m) in D.items():
    t = sorted(m)
    print(k, '|', h.get('PGM / RUN BY / DATE', '')[:40], '|', len(m), '|', h.get('INTERVAL'), '|',
          '%g..%g/%g x %g..%g/%g' % g, '|', t[0].strftime('%H:%M'), '|', t[-1].strftime('%m-%d %H:%M'), '|', h.get('# OF STATIONS', '-'))
hc, gc, mc = D['COD']
lat = np.arange(gc[0], gc[1] + gc[2] / 2, gc[2]); w = np.cos(np.radians(lat))[:, None] * np.ones((1, 73))
print('\n对 CODE（中心 − CODE，TECU；共同历元 × 71×73 格点；本文统计口径）')
print('中心 | 共同历元 | 格点对数 | 均差 | RMS | 面积加权均差 | 面积加权RMS | |差|p95 | 全球均值(中心) | 全球均值(CODE)')
for k, (h, g, m) in D.items():
    if k == 'COD': continue
    assert g == gc, (k, g)
    ep = sorted(set(m) & set(mc))
    a = np.stack([m[e] for e in ep]); b = np.stack([mc[e] for e in ep]); d = a - b
    ww = np.broadcast_to(w, d.shape); ok = np.isfinite(d)
    mw = np.sum((d * ww)[ok]) / np.sum(ww[ok]); rw = np.sqrt(np.sum((d * d * ww)[ok]) / np.sum(ww[ok]))
    print(f"{k} | {len(ep)} | {ok.sum()} | {np.nanmean(d):+.2f} | {np.sqrt(np.nanmean(d*d)):.2f} | {mw:+.2f} | {rw:.2f} | "
          f"{np.nanpercentile(abs(d),95):.2f} | {np.nansum(a*ww)/np.sum(ww[np.isfinite(a)]):.2f} | {np.nansum(b*ww)/np.sum(ww):.2f}")
# 逐时段（仅 2 h 公共历元，用 IGS 为例）与最大差格点
print('\n逐 UT（中心 − CODE 的面积加权 RMS，TECU）')
cols = [k for k in D if k != 'COD']
print('UT | ' + ' | '.join(cols))
for e in sorted(mc):
    if e.hour % 4 or e.minute: continue
    r = []
    for k in cols:
        m = D[k][2]
        if e in m:
            d = m[e] - mc[e]; ok = np.isfinite(d); r.append('%.2f' % np.sqrt(np.sum((d*d*w)[ok]) / np.sum(w[ok])))
        else: r.append('-')
    print(e.strftime('%m-%d %H'), '| ' + ' | '.join(r))
k = 'JPL'; m = D[k][2]; ep = sorted(set(m) & set(mc))
d = np.stack([m[e] - mc[e] for e in ep]); i = np.unravel_index(np.nanargmax(abs(d)), d.shape)
print(f"\n最大 |JPL−CODE| {d[i]:+.1f} TECU @ {ep[i[0]]:%H:%M} UT lat {lat[i[1]]:.1f} lon {-180+5*i[2]:.0f}；"
      f"JPL {m[ep[i[0]]][i[1],i[2]]:.1f} CODE {mc[ep[i[0]]][i[1],i[2]]:.1f}")
# 插值对齐演示：把 CODE 的 01:00 与 2 h 产品在 00/02 线性插值比较
e1 = dt.datetime(2024, 5, 11, 1); mi = D['IGS'][2]
lin = 0.5 * (mi[e1 - dt.timedelta(hours=1)] + mi[e1 + dt.timedelta(hours=1)])
dd = lin - mc[e1]; print(f"对齐示例：IGS 00/02 UT 线性插到 01 UT 再减 CODE 01 UT：RMS {np.sqrt(np.nanmean(dd*dd)):.2f}；"
      f"IGS 在 00 UT 直接减 CODE 00 UT：RMS {np.sqrt(np.nanmean((mi[e1-dt.timedelta(hours=1)]-mc[e1-dt.timedelta(hours=1)])**2)):.2f}；"
      f"错一小时（IGS 02 UT − CODE 01 UT）：RMS {np.sqrt(np.nanmean((mi[e1+dt.timedelta(hours=1)]-mc[e1])**2)):.2f}")
```

输出（原样）：

```text
中心 | 程序/日期 | 图数 | 间隔 s | 格网 | 首图 | 末图 | 站数
COD | ADDNEQ2 V5.5        AIUB                 | 25 | 3600 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 235
CAS | BDSMART-IONO1.0     AIR/CAS              | 49 | 1800.0 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | -
EMR | Run_GlbDaily        NRCan/CGS            | 25 | 3600 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 217
ESA | PAR2IONEX           ESA/ESOC             | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 275
ESA(nav-office) | PAR2IONEX           ESA/ESOC             | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 300
IGS | cmpcmb v1.2          GRL/UWM             | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 338
JPL | GIM V3.0            JPL - GNISD          | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 250
UPC | map2ionex           UPC-IonSAT           | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 238
WHU | GIMAS V1.1          GRC,WHU              | 13 | 7200 | 87.5..-87.5/-2.5 x -180..180/5 | 00:00 | 05-12 00:00 | 229

对 CODE（中心 − CODE，TECU；共同历元 × 71×73 格点；本文统计口径）
中心 | 共同历元 | 格点对数 | 均差 | RMS | 面积加权均差 | 面积加权RMS | |差|p95 | 全球均值(中心) | 全球均值(CODE)
CAS | 25 | 129575 | -1.69 | 5.86 | -2.17 | 6.71 | 11.90 | 27.42 | 29.59
EMR | 25 | 129410 | -2.34 | 13.57 | -3.82 | 15.77 | 28.80 | 25.78 | 29.59
ESA | 13 | 67379 | -2.15 | 7.73 | -2.67 | 8.88 | 16.50 | 27.03 | 29.70
ESA(nav-office) | 13 | 67379 | -2.26 | 7.86 | -2.78 | 9.05 | 17.00 | 26.92 | 29.70
IGS | 13 | 67379 | +0.32 | 3.25 | +0.09 | 3.30 | 6.70 | 29.79 | 29.70
JPL | 13 | 67379 | +0.62 | 4.71 | +0.87 | 4.99 | 9.60 | 30.57 | 29.70
UPC | 13 | 67379 | +0.34 | 7.38 | -0.61 | 7.54 | 15.80 | 29.09 | 29.70
WHU | 13 | 67379 | +0.63 | 4.15 | +0.62 | 4.40 | 8.40 | 30.32 | 29.70

逐 UT（中心 − CODE 的面积加权 RMS，TECU）
UT | CAS | EMR | ESA | ESA(nav-office) | IGS | JPL | UPC | WHU
05-11 00 | 7.75 | 21.60 | 14.12 | 14.17 | 4.20 | 6.21 | 9.19 | 6.48
05-11 04 | 7.06 | 20.55 | 10.80 | 11.15 | 3.67 | 5.51 | 8.28 | 4.61
05-11 08 | 6.96 | 15.65 | 6.47 | 6.55 | 3.42 | 5.11 | 7.65 | 4.42
05-11 12 | 5.57 | 13.96 | 8.14 | 8.32 | 3.38 | 5.05 | 6.75 | 4.68
05-11 16 | 6.04 | 10.85 | 7.63 | 7.93 | 2.87 | 4.69 | 6.23 | 3.71
05-11 20 | 4.90 | 10.79 | 6.24 | 6.48 | 2.15 | 3.72 | 4.55 | 2.98
05-12 00 | 6.50 | 15.32 | 9.99 | 10.42 | 3.76 | 3.60 | 11.64 | 3.09

最大 |JPL−CODE| -47.9 TECU @ 06:00 UT lat -60.0 lon 170；JPL 4.3 CODE 52.2
对齐示例：IGS 00/02 UT 线性插到 01 UT 再减 CODE 01 UT：RMS 6.32；IGS 在 00 UT 直接减 CODE 00 UT：RMS 4.48；错一小时（IGS 02 UT − CODE 01 UT）：RMS 9.07
```

**时间 / 格网对齐（本文做法）：**

- 9 个文件格网全是 87.5…−87.5 / 2.5° × −180…180 / 5°（71×73），脚本里 `assert` 了，**不用插值**；若遇到别的格网（例如 JPLH/JPLR 的 2°），先插到同一网格再比。
- 采样不同：CODE/EMR 1 h（25 图）、CAS 30 min（49 图）、ESA/IGS/JPL/UPC/WHU 2 h（13 图）。**只取与 CODE 历元完全相同的图**（2 h 产品 13 个历元，1 h/30 min 产品 25 个）。首末图都含（00:00 与次日 00:00）。
- 为什么不插值：对齐示例一行显示，把 IGS 00/02 UT 线性插到 01 UT 再减 CODE，RMS 6.32 TECU，比同历元直接相减的 4.48 大；错一小时（IGS 02 UT − CODE 01 UT）是 9.07。磁暴日 TEC 变化快，时间插值误差会冒充“中心差异”。
- 统计：均差 = 中心 − CODE；“面积加权”用 cos(纬度) 权重（高纬格点在经纬网里过密）。都是本文口径。

**结果摘要（2024-05-11，中心 − CODE，TECU，面积加权）：**

| 中心 | 均差 | RMS | 说明 |
| --- | --- | --- | --- |
| IGS 综合 | +0.09 | 3.30 | 最接近（IGS 综合本来就含 CODE） |
| WHU | +0.62 | 4.40 | |
| JPL | +0.87 | 4.99 | JPL README 称加了 2 TECU 偏置；单格点最大差 −47.9（06 UT，60°S 170°E：JPL 4.3 / CODE 52.2） |
| CAS | −2.17 | 6.71 | 30 min 产品，25 个公共历元 |
| UPC | −0.61 | 7.54 | |
| ESA | −2.67 | 8.88 | Navigation Office 重处理版 −2.78 / 9.05，与镜像版几乎一样 |
| EMR | −3.82 | 15.77 | 最大；UT 00 时 RMS 21.6；文件含 91 个 9999 缺测 |

各中心差异随 UT 变化：多数中心 05-11 00 UT 最大、20 UT 附近最小（JPL 最小在 05-12 00 UT，UPC 在 05-12 00 UT 反弹到 11.64；见逐 UT 表）。这只是一天、一个强磁暴日的结果，**不能当作各中心常规精度排名**。

## 4. 输入 / 输出（新旧文件名）

**长名规则**：`AAA0OPSTTT_YYYYDDD0000_01D_SSS_GIM.INX.gz`，`AAA` 中心、`TTT` = FIN/RAP/PnD/RTS、`SSS` = 图间隔（30M/01H/02H/15M/05M）。**旧短名**：`xxxgDDD0.YYi.Z`（第 4 字母 `g`，`.Z` 为 Unix compress）。

| 中心 | 最终（旧 → 新） | 快速（旧 → 新） | 其他档（本机见到的名字） |
| --- | --- | --- | --- |
| CODE | `codg` → `COD0OPSFIN_…_01H` | `corg` → `COD0OPSRAP_…_01H` | 预报 `COD0OPSP0D/P1D/P4D_…_01H`；旧 `c1pg/c2pg` 仍在 CAS 镜像 |
| IGS 综合 | `igsg` → `IGS0OPSFIN_…_02H` | `igrg` → `IGS0OPSRAP_…_02H` | |
| JPL | `jplg` → `JPL0OPSFIN_…_02H` | `jprg` → `JPL0OPSRAP_…_02H` | sideshow 另有 `JPLG/JPLH/JPLQ/JPLR*.YYI.gz`（大写短名，gzip） |
| ESA | `esag` → `ESA0OPSFIN_…_02H` | `esrg` → `ESA0OPSRAP_…_02H` | 快速另有 `_01H` 版 |
| UPC | `upcg` → `UPC0OPSFIN_…_02H` | `uprg` → `UPC0OPSRAP_…_02H` | `uhrg` ↔ `…RAP_01H`，`uqrg` ↔ `…RAP_15M`；实时 `usrg`、`uadg` 仍是短名 |
| NRCan | `emrg` → `EMR0OPSFIN_…_01H` | `ehrg`（2022 年可见；2026 未见 EMR 快速） | |
| CAS | `casg` → `CAS0OPSFIN_…_30M` | `carg` → `CAS0OPSRAP_…_30M` | `CAS0OPSRTS_…_05M`（2022/2024 见，2026 目录未见）；预报 `p1_/p2_/p5_casg`；`irtg` 未核对含义 |
| WHU | `whug` | `whrg` | 2024 仍只有短名；2026 镜像未见 |

**改名时间点不统一（CAS 镜像实测）**：CODE 旧名最后见于 2022/330，2023/001 起只有长名；IGS 在 2023/001 新旧并存；JPL 长名在 2023/200 与 2023/300 之间才出现；WHU 到 2024/132 仍是旧名。**写下载脚本时按中心 + 日期分支，不要全局替换。**

| 输出 | 说明 |
| --- | --- |
| IONEX 1.0 文本（gzip/compress） | 头 + TEC 图 + （多数有）RMS 图；单位 0.1 TECU（`EXPONENT -1`） |
| 本文 cmp.py 输出 | 每中心头信息表 + 对 CODE 的均差/RMS/p95 + 逐 UT RMS |

## 5. 参数：产品档次与实测时延

本文口径：上架时刻 − 数据日结束（24:00 UTC）。CODE 用 S3 `LastModified`（UTC）；其余用 CAS 镜像 2026/264（2026-09-21）目录列表时间（镜像时间未标时区，与 S3 对照看接近 UTC；镜像时间 ≥ 源站时间）。

| 档次 | 文件 | 实测时延 | 来源 |
| --- | --- | --- | --- |
| 实时 | UPC `usrg2690.26i.Z` | 09:00 UT 的图 09:04 UT 已在（列表 11:04 CEST） | UPC `real-time/quick/last_results/` |
| 预报 | CODE `P1D_2026270`（09-27） | 09-26 06:21 UTC 上架，**提前约 18 h** | AIUB S3 |
| 预报 | CODE `P0D_2026269`（当天） / `P4D` 到 DOY 273 | 当天 06:21 UTC | AIUB S3 |
| 快速 | CODE `RAP_2026268` | 6.4 h | AIUB S3 |
| 快速 | JPL RAP / ESA RAP | 7.0 h / 7.8 h | 镜像（JPL README 写 7 h） |
| 快速 | IGS RAP | 28 h | 镜像 |
| 快速 | CAS RAP | 43 h | 镜像 |
| 最终 | EMR FIN | 35 h（2026/266 同为 35 h） | 镜像 |
| 最终 | JPL FIN | 50 h（README 写 50 h） | 镜像 |
| 最终 | UPC FIN（与 RAP 同时上架） | 65 h（2026/266 是 30 h，波动大） | 镜像 |
| 最终 | CAS FIN | 65 h | 镜像 |
| 最终 | ESA FIN | 88 h | 镜像 |
| 最终 | CODE FIN | 90 h（DOY 264 → 09-25 17:57 UTC；265 起 404） | AIUB |
| 最终 | IGS FIN | 2026 年镜像目录未见，未测 | — |

## 6. 接到哪一步

| 下一步 | 去哪 |
| --- | --- |
| 读 IONEX / 取格点值 | [ionex-gim](./ionex-gim.md) · [ionex](./ionex.md) · [ionex-rs](./ionex-rs.md) |
| 多 GIM 对照课 | [18](../tutorials/18-lab-compare-gims.md) · [03](../tutorials/03-gim-ionex.md) |
| 磁暴 TEC 背景 | [20](../tutorials/20-storm-tec-analysis.md) · 同一磁暴的 [swarm-data](./swarm-data.md)、[chain-scintillation](./chain-scintillation.md) |
| 自建 GIM 对标 | [sh-gim](./sh-gim.md) · [mosgim2](./mosgim2.md) |
| 下载总表 | [data-access E27](../data-access.md#dp-e27) |

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `CODG1320.24I.Z` 404 | CODE 2023 起只发长名，源站不留旧名 | 用 `COD0OPSFIN_YYYYDDD0000_01D_01H_GIM.INX.gz` |
| 2 | `download.aiub.unibe.ch/CODE/2024/` 404 | 301 到 Switch S3，无索引页 | 给全名 + `curl -L`；列目录用 `https://zhw-b.s3.cloud.switch.ch/aiub?prefix=CODE/COD0OPS` |
| 3 | 同名 ESA 文件两处内容不同 | Navigation Office 放的是 2025-01-10 重处理版（300 站），镜像是 2024-05-15 原版（275 站） | 记录来源 URL + 头 `PGM / RUN BY / DATE`；复现实验固定来源 |
| 4 | 同一产品两处字节数不同 | 压缩方式不同（JPL gzip 两种、UPC `.Z` vs `.gz`） | 比**解压后** md5，不比大小 |
| 5 | 时延算错几小时 | 列表时区不同：UPC 是 CEST（列表 11:04 = 09:04 UTC）、JPL sideshow 是美西时间（JPLR 23:58 ↔ 镜像 06:58）、S3 是 UTC | 先确认时区再减 |
| 6 | 1 h 与 2 h 产品直接逐图相减错位 | 采样 30M/01H/02H/15M 不同 | 只取公共历元；插值会额外引入误差（RMS 4.48 → 6.32） |
| 7 | 均差符号 / 大小随口径变 | 等经纬网高纬格点过密 | 标明是否 cos(纬度) 加权（EMR 不加权 −2.34，加权 −3.82） |
| 8 | 统计里混进离谱值 | EMR 文件有 9999 缺测（本日 91 个） | 9999 → NaN 再统计 |
| 9 | TEC 值读成 RMS | IONEX 在 TEC 图后接 RMS 图，块结构一样 | 解析到 `START OF RMS MAP` 停，或按块类型分开 |
| 10 | JPL 系统性偏高 | README 写 JPLG/JPLH/JPLR/JPLQ “2 TECU bias added” | 对比时注明；不要当作物理差异 |
| 11 | CDDIS 返回 HTML 登录页 | 需 Earthdata 账号 | 匿名场景用 CAS 镜像 / 源站 |
| 12 | IGN / BKG / WHU / KASI / GSSC 下不到 | 本次 TLS EOF、超时、502/425、21 端口拒连或目录不存在 | 以 CAS 镜像 + 源站为主；这些镜像换天再试 |
| 13 | 找不到 2026 年 CODE 最终 / IGS 最终 / WHU | CAS 镜像不全 | CODE 最终去 AIUB；IGS / WHU 最终本次无匿名源 |
| 14 | 把一天的对比当“精度排名” | 2024-05-11 是强磁暴日，差异偏大 | 只作示例；要排名需多天 + 独立参考（如 JASON VTEC） |
| 15 | 同样叫 `.Z`，有的 Python `gzip` 能开有的不能 | CAS 镜像上的 `.Z` 实际是 gzip（魔数 `1f 8b`），UPC 源站 `.Z` 是真 Unix compress（`1f 9d`） | 统一用 `gzip -dc`（两种都能解）；或按魔数分支 |

## 8. 选型

| 需求 | 选 | 不选 |
| --- | --- | --- |
| 一次拿全各中心某日 IONEX | **CAS 镜像**目录 | 逐个源站 |
| CODE 最终 / 快速 / 预报 | AIUB `download.aiub.unibe.ch/CODE/` | 旧 `ftp.aiub.unibe.ch`、旧短名 |
| 最快拿到当天全球图 | UPC 实时 `usrg`（约 5 min）；CODE `P0D/P1D` 预报 | 最终产品 |
| 当天快速后处理 | CODE RAP（约 6 h）、JPL/ESA RAP（约 7–8 h） | CAS RAP（约 2 d） |
| 引用最稳定的最终产品 | IGS / CODE 最终（注意 CODE 约 4 d） | 预报 |
| JPL 1 h / 2° 高分辨 | sideshow `JPLH`（最终 50 h）/ `JPLR`（7 h） | 镜像（没有） |
| 读 IONEX | [ionex-gim](./ionex-gim.md) | 本页 |
