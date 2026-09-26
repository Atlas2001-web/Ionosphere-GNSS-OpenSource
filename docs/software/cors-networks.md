# 区域 CORS 网匿名数据：NOAA NGS、EPN、GeoNet、IBGE RBMC、SONEL 同日下载实测（EarthScope GAGE / CDDIS 需登录）

入口：[NOAA CORS S3 `noaa-cors-pds`](https://noaa-cors-pds.s3.amazonaws.com/index.html) · [EPN `/pub/RINEX/`](https://epncb.oma.be/pub/RINEX/) · [BKG EUREF 镜像](https://igs.bkg.bund.de/root_ftp/EUREF/obs/) · [GeoNet `/v1/data/gnss/rinex/`](https://data.geonet.org.nz/v1/data/gnss/rinex/) · [IBGE RBMC geoftp](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · SONEL `ftp://ftp.sonel.org/gps/data/` · 本机验证 **2026-09-26 05:45–05:58 EDT**（匿名，未注册任何账号；UTC = EDT + 4 h）

> 岗位：回答“某个区域 CORS 网的日观测不登录去哪拿、多少站、什么采样、什么命名、昨天的数据什么时候能拿到”。每网列 2024-05-11（2024/132，强磁暴日）和 2026-09-25（2026/268，探测前一天）两天的目录，每网真下 1 站 2024/132 日文件并数历元。IGS 全球站镜像（BKG / CAS / SOPAC / GA）另见 [gnss-obs-mirrors](./gnss-obs-mirrors.md)，本文只写区域网这一侧。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E30](../data-access.md#dp-e30)
>
> 冲突时：以各网当时的目录列表为准（只代表 2026-09-26 这一次）；“上架延迟 = Last-Modified − 日结束 00:00 UTC”“取按字母前 30 站”“完整 = 历元数达到 86400/采样间隔”都是**本文口径**。

## 1. 用途与边界

**做：** 各区域网匿名日观测的目录、命名、采样、站数；上架延迟；一站一天真下载 + 解 Hatanaka + 数历元；需要登录的网说清门槛。

**不做：** IGS 全球站多镜像比对（→ [gnss-obs-mirrors](./gnss-obs-mirrors.md)，GA 的 S3 `public/daily` 也在那里，2024/132 共 938 个日文件）；高采样 / 小时 / 1 Hz 文件；实时流（NTRIP）；坐标时序产品。

**结论先说：**

| 网 | 日观测目录（匿名） | 采样 / 命名 / 格式 | 2024/132 规模 | 上架延迟（本文口径） | 本次下载 |
| --- | --- | --- | --- | --- | --- |
| **NOAA NGS CORS**（美） | `https://noaa-cors-pds.s3.amazonaws.com/rinex/YYYY/DDD/ssss/` | 30 s；RINEX 2 **短名** `ssssDDD0.YYo.gz`（另有 `.YYd.gz`、`.YYS`） | 1740 个站目录 | 2026/268：中位 **2.8 h**，最晚 7.3 h（30 站） | 1LSU：2880 历元，完整 |
| **EUREF EPN**（欧） | `https://epncb.oma.be/pub/RINEX/YYYY/DDD/`（`/pub/obs/` 会跳过去） | 30 s；RINEX 3 长名 `…_01D_30S_MO.crx.gz` | 395 | 中央局最新目录只到 **266**（LM 09-26 04:00 UTC，≈ **52 h**）；BKG EUREF 镜像已有 268（267 个，LM 01:30 UTC ≈ 1.5 h） | ACOR：2880，完整 |
| **GeoNet**（新西兰） | `https://data.geonet.org.nz/v1/data/gnss/rinex/YYYY/DDD/`（链接指到 `geonet-open-data` S3） | 30 s；RINEX 3 长名但 **`.rnx.gz`（不是 crx）** | 186 | 中位 **0.2 h**（30/30） | AHTI：2880，完整 |
| **IBGE RBMC**（巴西） | `https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/YYYY/DDD/` | **15 s**；`…_01D_15S_MO.crx.gz`；另有 `rbmc/dados/` RINEX 2 单站 zip | 84 | 最新目录 267（87 个，LM 09-25 23:00 UTC ≈ **23 h**），268 尚 404 | ALMC：5760（15 s），完整 |
| **SONEL**（验潮站 GNSS，全球） | `ftp://ftp.sonel.org/gps/data/YYYY/DDD/`（只 FTP） | 30 s 为主（687 个 30S + 5 个 15S）；长名 crx.gz + 347 个 `.24d.Z` 旧短名 | 692 | 268 首文件 LM 01:40 UTC ≈ **1.7 h** | 019400JPN：2880，完整 |
| GA（澳） | 见 [gnss-obs-mirrors](./gnss-obs-mirrors.md) | 30 s 长名 | 938（S3 `public/daily`） | — | — |
| **EarthScope GAGE**（原 UNAVCO，美） | `https://gage-data.earthscope.org/archive/gnss/rinex/obs/YYYY/DDD/` | — | — | — | **302 到 `/login`，需 EarthScope 账号**，本文不走 |
| CDDIS | `https://cddis.nasa.gov/archive/gnss/data/daily/…` | — | — | — | **需 Earthdata 账号**（见 [gnss-obs-mirrors](./gnss-obs-mirrors.md)） |
| GSI GEONET（日） | `terras.gsi.go.jp` | — | — | — | 首页 200，但**未找到匿名下载链接**；门槛**未验证**（本文未测） |
| IGN RGP（法） | `https://rgp.ign.fr/DONNEES/diffusion/` | — | — | — | 本次 **503**（21 s），未测 |
| NRCan CACS（加） | CACS webapp / `ftp.geod.nrcan.gc.ca` | — | — | — | 本次 **000**（连不上），未测 |

西班牙 ERGNSS、奥地利 BEV APOS、GA 的下载命令见 data-access 已有小节：[GA](../data-access.md#区域-corsga澳大利亚可选) · [ERGNSS](../data-access.md#区域-corsergnss西班牙) · [BEV APOS](../data-access.md#区域-corsbev-apos奥地利-stac)（本次未重测）。

## 2. 安装

`curl`、`gzip`、Python 3 标准库（列目录 + 翻 S3 分页 + HEAD 取 Last-Modified）；解 Hatanaka 用 Rust `crx2rnx` 2.7.0（`~/.cargo/bin/crx2rnx`，见 [crx2rnx](./crx2rnx.md)）。**注意** Rust 版解不了 NOAA 的 CRINEX 1.0（坑 3），RINEX 2 的 `.d` 文件请用 C 版 RNXCMP `CRX2RNX` 或直接拿 S3 的 `.o.gz`。

```bash
curl --version | head -1; crx2rnx --version; /usr/bin/python3 --version
```

## 3. 真命令 + 期望输出

### 3.1 各网同日目录规模与上架延迟（`cors.py`）

```python
# 区域 CORS 网：同一天目录规模、按站到达、上架延迟（Last-Modified − 日结束）
import re, urllib.request, urllib.error, urllib.parse, datetime as dt, statistics, time
from concurrent.futures import ThreadPoolExecutor
UA = {'User-Agent': 'curl/8'}
def get(u, t=60):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t) as r: return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return type(e).__name__, ''
def lastmod(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, method='HEAD', headers=UA), timeout=40) as r:
            return r.headers.get('Last-Modified'), int(r.headers.get('Content-Length') or -1)
    except Exception: return None, None
def ftp_list(u):
    try:
        with urllib.request.urlopen(u, timeout=60) as r: return 200, r.read().decode('utf-8', 'replace')
    except Exception as e: return type(e).__name__, ''
def noaa(y, d):
    base = 'https://noaa-cors-pds.s3.amazonaws.com/'; q = f'?list-type=2&prefix=rinex/{y}/{d:03d}/&delimiter=/'
    st, pre, tok = None, [], None
    while True:
        st, x = get(base + q + ('&continuation-token=' + urllib.parse.quote(tok) if tok else ''))
        pre += re.findall(rf'<Prefix>rinex/{y}/{d:03d}/([a-z0-9]{{4}})/</Prefix>', x)
        m = re.search(r'<NextContinuationToken>([^<]+)', x)
        if not m: break
        tok = m.group(1)
    return st, sorted(set(pre)), lambda s: f'{base}rinex/{y}/{d:03d}/{s}/{s}{d:03d}0.{y%100:02d}o.gz'
def listing(url, pat):
    st, x = (ftp_list if url.startswith('ftp') else get)(url)
    return st, sorted(set(re.findall(pat, x)))
YY = lambda y: f'{y%100:02d}'
def nets(y, d):
    L3 = rf'([A-Z0-9]{{9}})_[RS]_{y}{d:03d}0000_01D_(\d\dS)_MO\.(crx|rnx)\.gz'
    return {
      'EPN': (f'https://epncb.oma.be/pub/RINEX/{y}/{d:03d}/', L3),
      'GeoNet': (f'https://data.geonet.org.nz/v1/data/gnss/rinex/{y}/{d:03d}/', L3),
      'IBGE RBMC': (f'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/{y}/{d:03d}/', L3),
      'SONEL': (f'ftp://ftp.sonel.org/gps/data/{y}/{d:03d}/', L3)}
for y, d in [(2024, 132), (2026, 268)]:
    end = dt.datetime(y, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(days=d)
    print(f'\n##### {y}/{d:03d}（日结束 {end:%Y-%m-%d %H:%M} UTC；探测 {dt.datetime.now(dt.timezone.utc):%H:%M} UTC）')
    print('网 | HTTP | 日观测文件（站） | 采样分布 | 示例')
    rows = {}
    t0 = time.time(); st, sts, mk = noaa(y, d)
    print(f'NOAA NGS（S3） | {st} | {len(sts)} 个站目录 | RINEX 2 短名 30 s（`ssssDDD0.YYo.gz`） | {" ".join(sts[:3])} …')
    rows['NOAA NGS'] = [mk(s) for s in sts]
    for n, (u, pat) in nets(y, d).items():
        st, fs = listing(u, pat)
        samp = {}
        for f in fs: samp[f[1]] = samp.get(f[1], 0) + 1
        ext = sorted({f[2] for f in fs})
        print(f'{n} | {st} | {len(fs)} | {samp} {ext} | {" ".join(f[0] for f in fs[:3])} …')
        pre = f'{u}' if not u.startswith('https://data.geonet') else f'https://geonet-open-data.s3-ap-southeast-2.amazonaws.com/gnss/rinex/{y}/{d:03d}/'
        rows[n] = [f'{pre}{f[0]}_{"S" if False else "R"}_{y}{d:03d}0000_01D_{f[1]}_MO.{f[2]}.gz' for f in fs]
    if (y, d) == (2026, 268):
        print('\n上架延迟（每网取按字母前 30 个站；Last-Modified − 日结束，h；本文口径）')
        for n, urls in rows.items():
            urls = urls[:30]
            with ThreadPoolExecutor(10) as ex: r = list(ex.map(lastmod, urls))
            lat = [(dt.datetime.strptime(lm, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=dt.timezone.utc) - end).total_seconds() / 3600 for lm, _ in r if lm]
            if lat: print(f'{n} | {len(lat)}/{len(urls)} 有 Last-Modified | 中位 {statistics.median(lat):.1f} | 最早 {min(lat):.1f} | 最晚 {max(lat):.1f}')
            else: print(f'{n} | 0/{len(urls)} 有 Last-Modified（HEAD 不给或 404）')
```

实测输出（2026-09-26 05:53 EDT 起跑）：

```text

##### 2024/132（日结束 2024-05-12 00:00 UTC；探测 09:53 UTC）
网 | HTTP | 日观测文件（站） | 采样分布 | 示例
NOAA NGS（S3） | 200 | 1740 个站目录 | RINEX 2 短名 30 s（`ssssDDD0.YYo.gz`） | 1lsu 1nsu 1ulm …
EPN | 200 | 395 | {'30S': 395} ['crx'] | ACOR00ESP ADAR00GBR AGRN00ITA …
GeoNet | 200 | 186 | {'30S': 186} ['rnx'] | 200400NZL 240600NZL AHTI00NZL …
IBGE RBMC | 200 | 84 | {'15S': 84} ['crx'] | ALMC00BRA AMTE00BRA APMA00BRA …
SONEL | 200 | 692 | {'30S': 687, '15S': 5} ['crx'] | 019400JPN 045700JPN 075000JPN …

##### 2026/268（日结束 2026-09-26 00:00 UTC；探测 09:53 UTC）
网 | HTTP | 日观测文件（站） | 采样分布 | 示例
NOAA NGS（S3） | 200 | 1627 个站目录 | RINEX 2 短名 30 s（`ssssDDD0.YYo.gz`） | 1lsu 1nsu 1ulm …
EPN | 404 | 0 | {} [] |  …
GeoNet | 200 | 206 | {'30S': 206} ['rnx'] | 240600NZL AHTI00NZL AKTO00NZL …
IBGE RBMC | 404 | 0 | {} [] |  …
SONEL | 200 | 321 | {'30S': 321} ['crx'] | 0BIS00SWE 0BRU00SWE 0FRL00SWE …

上架延迟（每网取按字母前 30 个站；Last-Modified − 日结束，h；本文口径）
NOAA NGS | 30/30 有 Last-Modified | 中位 2.8 | 最早 2.8 | 最晚 7.3
EPN | 0/0 有 Last-Modified（HEAD 不给或 404）
GeoNet | 30/30 有 Last-Modified | 中位 0.2 | 最早 0.1 | 最晚 0.3
IBGE RBMC | 0/0 有 Last-Modified（HEAD 不给或 404）
SONEL | 0/30 有 Last-Modified（HEAD 不给或 404）
```

读法：EPN / RBMC 的 2026/268 是 **404**（当天目录还没建），不是脚本错；它们各自的最新目录见 3.2。SONEL 走 FTP，urllib 的 HEAD 拿不到 Last-Modified，所以 0/30，用 3.2 的 `curl -I` 补。NOAA 的数是“站目录数”，不是文件数（每目录里有 `.o.gz`/`.d.gz`/`.S` 等多个文件）。

### 3.2 最新目录与需要登录的网（`lat.sh`）

```bash
#!/usr/bin/env bash
# 各网“最新一天”在哪、何时上架（2026-09-26 探测；Last-Modified 为 UTC）
lm(){ curl -sIL -m 30 "$1" | grep -i '^last-modified' | tail -1 | tr -d '\r' | cut -c16-; }
echo "EPN /pub/RINEX/2026/ 最新目录: $(curl -sL -m 40 https://epncb.oma.be/pub/RINEX/2026/ | grep -o 'href="[0-9]*/"' | tail -1)"
f=$(curl -sL -m 40 https://epncb.oma.be/pub/RINEX/2026/266/ | grep -o '[A-Z0-9]\{9\}_[RS]_20262660000_01D_30S_MO.crx.gz' | sort -u | head -1)
echo "  266 首站 $f  Last-Modified: $(lm https://epncb.oma.be/pub/RINEX/2026/266/$f)"
echo "EPN 经 BKG EUREF 镜像 2026/268: $(curl -s -m 40 https://igs.bkg.bund.de/root_ftp/EUREF/obs/2026/268/ | grep -o '[A-Z0-9]\{9\}_[RS]_20262680000_01D_30S_MO.crx.gz' | sort -u | wc -l) 个日文件；2024/132: $(curl -s -m 40 https://igs.bkg.bund.de/root_ftp/EUREF/obs/2024/132/ | grep -o '[A-Z0-9]\{9\}_[RS]_20241320000_01D_30S_MO.crx.gz' | sort -u | wc -l) 个"
g=$(curl -s -m 40 https://igs.bkg.bund.de/root_ftp/EUREF/obs/2026/268/ | grep -o '[A-Z0-9]\{9\}_[RS]_20262680000_01D_30S_MO.crx.gz' | sort -u | head -1)
echo "  BKG EUREF 268 首站 $g  Last-Modified: $(lm https://igs.bkg.bund.de/root_ftp/EUREF/obs/2026/268/$g)"
R=https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/2026
echo "RBMC 最新目录: $(curl -s -m 40 $R/ | sed 's/<[^>]*>/ /g' | grep -E '^ *[0-9]{3}/' | tail -1 | tr -s ' ')"
h=$(curl -s -m 40 $R/267/ | grep -o '[A-Z0-9]\{9\}_R_20262670000_01D_15S_MO.crx.gz' | sort -u | tee /tmp/rb.txt | head -1)
echo "  267: $(wc -l < /tmp/rb.txt) 个日文件；首站 $h  Last-Modified: $(lm $R/267/$h)"; rm -f /tmp/rb.txt
echo "SONEL FTP 2026/268 首个文件 Last-Modified: $(lm ftp://ftp.sonel.org/gps/data/2026/268/0BIS00SWE_S_20262680000_01D_30S_MO.crx.gz)"
echo "NOAA NGS 网页目录 1lsu 2024/132: $(curl -s -m 40 https://geodesy.noaa.gov/corsdata/rinex/2024/132/1lsu/ | grep -o 'href="1lsu[^"]*"' | sed 's/href=//;s/"//g' | tr '\n' ' ')（无 .o.gz；S3 有）"
echo "## 需要登录 / 不通"
echo "EarthScope GAGE: $(curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}' https://gage-data.earthscope.org/archive/gnss/rinex/obs/2024/132/ | cut -c1-90)"
echo "IGN RGP: $(curl -s -o /dev/null -m 30 -w '%{http_code} %{time_total}s' https://rgp.ign.fr/DONNEES/diffusion/)"
echo "NRCan CACS: $(curl -s -o /dev/null -m 30 -w '%{http_code} %{time_total}s' https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php)"
echo "SONEL 网站: $(curl -s -o /dev/null -m 30 -w '%{http_code} %{time_total}s' https://www.sonel.org/)"
```

实测输出（05:45 EDT 起跑，约 80 s）：

```text
EPN /pub/RINEX/2026/ 最新目录: href="266/"
  266 首站 AAER00FRA_R_20262660000_01D_30S_MO.crx.gz  Last-Modified: Sat, 26 Sep 2026 04:00:38 GMT
EPN 经 BKG EUREF 镜像 2026/268: 267 个日文件；2024/132: 287 个
  BKG EUREF 268 首站 AAER00FRA_R_20262680000_01D_30S_MO.crx.gz  Last-Modified: Sat, 26 Sep 2026 01:30:19 GMT
RBMC 最新目录:  267/ 2026-09-25 07:06 - &nbsp; 
  267: 87 个日文件；首站 ALMC00BRA_R_20262670000_01D_15S_MO.crx.gz  Last-Modified: Fri, 25 Sep 2026 23:00:02 GMT
SONEL FTP 2026/268 首个文件 Last-Modified: Sat, 26 Sep 2026 01:40:15 GMT
NOAA NGS 网页目录 1lsu 2024/132: 1lsu1320.24S 1lsu1320.24d.gz （无 .o.gz；S3 有）
## 需要登录 / 不通
EarthScope GAGE: 302 -> https://gage-data.earthscope.org/login?original_url=%2Farchive%2Fgnss%2Frinex%2Fobs
IGN RGP: 503 21.112384s
NRCan CACS: 000 5.008144s
SONEL 网站: 000 30.001828s
```

算延迟（本文口径，日结束 = 次日 00:00 UTC）：EPN 266 → 09-26 04:00 UTC 上架 ≈ 52 h；BKG EUREF 268 → 01:30 UTC ≈ 1.5 h；RBMC 267 → 09-25 23:00 UTC ≈ 23 h；SONEL 268 → 01:40 UTC ≈ 1.7 h。

### 3.3 每网 1 站 2024/132 真下载 + 历元数（`dl.sh`）

```bash
#!/usr/bin/env bash
# 每网拉 1 站 2024-05-11 日文件，解压，数历元（30 s 满日 = 2880；15 s = 5760）
g(){ curl -sL -m 180 -o "$1" -w "%{http_code} %{size_download} B %{time_total}s  $1\n" "$2"; }
g ngs_s3_1lsu.o.gz   https://noaa-cors-pds.s3.amazonaws.com/rinex/2024/132/1lsu/1lsu1320.24o.gz
g ngs_web_1lsu.d.gz  https://geodesy.noaa.gov/corsdata/rinex/2024/132/1lsu/1lsu1320.24d.gz
g epn_ACOR.crx.gz    https://epncb.oma.be/pub/RINEX/2024/132/ACOR00ESP_R_20241320000_01D_30S_MO.crx.gz
g geonet_AHTI.rnx.gz https://geonet-open-data.s3-ap-southeast-2.amazonaws.com/gnss/rinex/2024/132/AHTI00NZL_R_20241320000_01D_30S_MO.rnx.gz
g rbmc_ALMC.crx.gz   https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/2024/132/ALMC00BRA_R_20241320000_01D_15S_MO.crx.gz
g sonel_0194.crx.gz  ftp://ftp.sonel.org/gps/data/2024/132/019400JPN_R_20241320000_01D_30S_MO.crx.gz
for f in *.gz; do
  b=${f%.gz}; gzip -dc "$f" > "$b"
  case "$b" in
    *.crx) crx2rnx -q -o "$b.rnx" "$b" >/dev/null 2>&1 && r="$b.rnx" || r="" ;;
    *.d)   r="" ;;   # RINEX 2 Hatanaka（CRINEX 1.0）：试 Rust crx2rnx
    *)     r="$b" ;;
  esac
  [ "$b" = "${b%.d}" ] || { crx2rnx -q -o "$b.rnx" "$b" >/dev/null 2>&1 && r="$b.rnx"; }
  if [ -n "$r" ]; then
    v=$(head -1 "$r" | cut -c1-9 | tr -d ' ')
    if [ "${v%%.*}" = 3 ] || [ "${v%%.*}" = 4 ]; then ep=$(grep -c '^>' "$r"); last=$(grep '^>' "$r" | tail -1 | cut -c3-21)
    else ep=$(grep -cE '^ [0-9 ][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9].[0-9]{7}  0' "$r"); last=$(grep -E '^ [0-9 ][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9] [ 0-9][0-9].[0-9]{7}  0' "$r" | tail -1 | cut -c2-26); fi
    iv=$(grep -m1 'INTERVAL' "$r" | cut -c1-10 | tr -d ' ')
    printf '%-20s RINEX %-5s INTERVAL=%-6s epochs=%-5s last=%s\n' "$f" "$v" "$iv" "$ep" "$last"
  else printf '%-20s 解压/解 Hatanaka 失败\n' "$f"; fi
done
```

实测输出（在空目录里跑）：

```text
200 2702921 B 0.143396s  ngs_s3_1lsu.o.gz
200 1166877 B 1.557774s  ngs_web_1lsu.d.gz
200 2767966 B 1.929961s  epn_ACOR.crx.gz
200 2377532 B 2.159522s  geonet_AHTI.rnx.gz
200 3611388 B 2.466921s  rbmc_ALMC.crx.gz
226 2628008 B 2.112633s  sonel_0194.crx.gz
epn_ACOR.crx.gz      RINEX 3.04  INTERVAL=30     epochs=2880  last=2024 05 11 23 59 30
geonet_AHTI.rnx.gz   RINEX 3.05  INTERVAL=30.000 epochs=2880  last=2024 05 11 23 59 30
ngs_s3_1lsu.o.gz     RINEX 2.11  INTERVAL=30.000 epochs=2880  last=24  5 11 23 59 30.0000000
ngs_web_1lsu.d.gz    解压/解 Hatanaka 失败
rbmc_ALMC.crx.gz     RINEX 3.05  INTERVAL=15     epochs=5760  last=2024 05 11 23 59 45
sonel_0194.crx.gz    RINEX 3.02  INTERVAL=30     epochs=2880  last=2024 05 11 23 59 30
```

- 5 个网的日文件全部完整：30 s 网 2880 历元、RBMC 15 s 5760 历元，最后历元都到 23:59:30 / 23:59:45。
- NOAA 1LSU 的 RINEX 2 若用朴素正则（不看 flag 列）数历元会得 **2903**：多出的 23 条是每小时一条 flag 4（注释事件）记录。脚本只数 flag 0 的行。
- `ngs_web_1lsu.d.gz` 能下（200，1,166,877 B，CRINEX 1.0，`RNX2CRX ver.4.0.8 12-May-24`），但 Rust crx2rnx 2.7.0 直接 panic：`gnss-rs-2.6.0/src/sv/mod.rs:199:60: end byte index 1 is out of bounds for string of length 0`。
- NGS 网页目录 `geodesy.noaa.gov/corsdata/rinex/2024/132/1lsu/` 里**只有** `1lsu1320.24d.gz` 和 `1lsu1320.24S`，没有 `.o.gz`；S3 上的 `.o.gz` 的 LastModified 是 2024-06-13（事后补的），`.d.gz` 是 2024-05-12 02:15 UTC。

## 4. 输入 / 输出

| 网 | 输入 | 输出文件名例 | 解压链 |
| --- | --- | --- | --- |
| NOAA | 站四字码**小写** + 年 + DOY | `1lsu1320.24o.gz`（RINEX 2.11）/ `1lsu1320.24d.gz`（CRINEX 1.0） | `gzip -d`；`.d` 用 C 版 CRX2RNX |
| EPN | 9 字符站名 + 年 + DOY | `ACOR00ESP_R_20241320000_01D_30S_MO.crx.gz` | `gzip -d` → `crx2rnx` |
| GeoNet | 同上 | `AHTI00NZL_R_20241320000_01D_30S_MO.rnx.gz` | 只要 `gzip -d` |
| RBMC | 同上 | `ALMC00BRA_R_20241320000_01D_15S_MO.crx.gz` | `gzip -d` → `crx2rnx` |
| SONEL | 同上 | `019400JPN_R_20241320000_01D_30S_MO.crx.gz`、旧 `xxxx1320.24d.Z` | `gzip -d`（`.Z` 用 `uncompress`/`gzip -d`）→ `crx2rnx` |

## 5. 参数（选网时要看的量）

| 量 | 值（本次） | 说明 |
| --- | --- | --- |
| 站数（2024/132） | NOAA 1740 目录 · SONEL 692 · EPN 395 · GeoNet 186 · RBMC 84 | EPN 的 BKG 镜像只有 287 个 |
| 采样 | RBMC 15 s；其余 30 s（SONEL 有 5 个 15S） | 15 s 文件约大 30% |
| 上架延迟中位 | GeoNet 0.2 h < BKG EUREF 1.5 h ≈ SONEL 1.7 h < NOAA 2.8 h < RBMC ≈ 23 h < EPN 中央局 ≈ 52 h | 本文口径，单日单次 |
| 列目录方式 | NOAA：S3 ListObjectsV2（`list-type=2&prefix=…&delimiter=/`，1000 条/页）；其余：HTML/FTP 列表 | |

## 6. 接到哪一步

- 下载的 RINEX → [crx2rnx](./crx2rnx.md) 解 Hatanaka → [gnss-obs-mirrors](./gnss-obs-mirrors.md) 同样的完整性检查 → TEC 解算（见 [data-access 决策表](../data-access.md#电离层与地磁门户决策表)）。
- 全球 IGS 站、GA 区域站：[gnss-obs-mirrors](./gnss-obs-mirrors.md)；GIM 产品：[gim-product-portals](./gim-product-portals.md)；近实时 TEC：[realtime-iono-products](./realtime-iono-products.md)。
- 已有 data-access 小节（旧示例 2023/049）：[NOAA](../data-access.md#区域-corsnoaa美国) · [GeoNet](../data-access.md#区域-corsgeonet新西兰) · [EPN + IBGE](../data-access.md#区域-corsepn欧洲-ibge巴西备选)。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | NGS 网页目录里找不到 `.o.gz` | 网页 `corsdata/rinex/` 只放 `.d.gz`（CRINEX）和 `.S`；S3 的 `.o.gz` 是事后补的（本例 2024-06-13） | 批量用 S3 `noaa-cors-pds`；近实时只能拿 `.d.gz` |
| 2 | RINEX 2 数出 2903 个历元（> 2880） | 每小时一条 flag 4 注释事件也符合“时间行”格式 | 只数 epoch flag = 0 的行（第 29 列） |
| 3 | `crx2rnx` panic `end byte index 1 is out of bounds` | Rust crx2rnx 2.7.0（gnss-rs 2.6.0）处理 NOAA 的 CRINEX 1.0 出错 | RINEX 2 `.d` 用 C 版 RNXCMP `CRX2RNX`，或改拿 S3 `.o.gz` |
| 4 | GeoNet 文件喂给 crx2rnx 报错 | GeoNet 日文件是 `.rnx.gz`（未 Hatanaka 压缩），不是 `.crx.gz` | 只 `gzip -d`；按扩展名分流 |
| 5 | RBMC 历元数“多一倍” | RBMC 是 15 s（5760/天） | 按文件名 `_15S_` 算期望历元，或自己降采样到 30 s |
| 6 | EPN 昨天的目录 404 | 中央局 `/pub/RINEX/` 本次落后约 2 天（最新 266） | 急用走 BKG EUREF 镜像 `igs.bkg.bund.de/root_ftp/EUREF/obs/`（已有 268），但站数少（2024/132：287 vs 395） |
| 7 | RBMC 昨天的目录 404 | 本次 RBMC 约 1 天后上架（267 LM 09-25 23:00 UTC） | 事后分析没问题；近实时别指望 RBMC |
| 8 | NOAA 列目录只得 1000 个站 | S3 ListObjectsV2 每页 1000 条 | 循环带 `continuation-token`，直到没有 `NextContinuationToken` |
| 9 | 把 NOAA 的 1740 当文件数 | 列的是站目录前缀，每目录多个文件 | 统计文件要再列每个前缀，或直接按键名拼 URL 下 |
| 10 | SONEL 拿不到 Last-Modified / 网站打不开 | 只有 FTP；Python urllib 对 FTP 不给 LM；`www.sonel.org` 本次超时 | 用 `curl -I ftp://…`；数据走 `ftp.sonel.org`，不依赖网站 |
| 11 | 同一目录里长名、短名混杂 | SONEL 2024/132 既有长名 crx.gz 又有 347 个 `.24d.Z`；RBMC 另有 `rbmc/dados/` RINEX 2 zip | 正则只匹配你要的一种命名；别直接数目录行数当站数 |
| 12 | GeoNet 根路径 HEAD 405 | 旧 data-access 已记录：部分端点只接受 GET | 用 GET 列目录；文件本身在 S3 上 HEAD 正常（30/30 有 LM） |
| 13 | EarthScope GAGE 302 到 `/login` | EarthScope 档案下载要求登录（EarthScope 账号） | 本文不走；需要时去 EarthScope 注册，或改用 NOAA / IGS 镜像 |
| 14 | 以为 GSI GEONET 匿名能下 | 首页 200，但没找到匿名下载链接 | 本文**未验证**其门槛，别写进流水线 |

## 8. 选型

- 美国：**NOAA S3**（站最多，2.8 h）；EarthScope GAGE 只在需要它独有的站时再注册。
- 欧洲：事后分析用 **EPN 中央局**（395 站）；急用 **BKG EUREF 镜像**（1.5 h，站少）。
- 新西兰：**GeoNet**（0.2 h，最快，注意 `.rnx.gz`）。
- 巴西：**RBMC**（15 s，≈ 1 天）。
- 沿海 / 验潮站、全球补站：**SONEL** FTP。
- 澳大利亚与 IGS 全球站：[gnss-obs-mirrors](./gnss-obs-mirrors.md)。
