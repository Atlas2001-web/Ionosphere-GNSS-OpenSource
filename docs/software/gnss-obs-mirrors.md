# IGS / MGEX 观测数据匿名镜像：BKG、CAS、SOPAC、GA 同日同站到达率与完整性实测（CDDIS 需 Earthdata）

入口：[BKG root_ftp/IGS/obs](https://igs.bkg.bund.de/root_ftp/IGS/obs/) · [CAS data/igs](https://data.bdsmart.cn/pub/data/igs/) · [SOPAC garner rinex](http://garner.ucsd.edu/pub/rinex/) · [GA S3 public/daily](https://ga-gnss-data-rinex-v1.s3.amazonaws.com/index.html) · [GA 说明](https://data.gnss.ga.gov.au/docs/home/gnss-data.html) · [CDDIS（需 Earthdata）](https://cddis.nasa.gov/archive/gnss/data/daily/) · 本机验证 **2026-09-26 05:10–05:20 EDT**（全部匿名 HTTP(S)，无注册、无表单）

> 岗位：回答“IGS 日观测（RINEX 3 长名 `…_01D_30S_MO.crx.gz`）不登录去哪拿、哪个镜像齐、到得快、内容是不是同一份”。选一组 24 个全球 IGS 站，对 2024-05-11（DOY 132，历史日）和 2026-09-25（DOY 268，探测前一天）在各镜像上逐站比对。**只管镜像这一侧**：解 Hatanaka 见 [crx2rnx](./crx2rnx.md) / [hatanaka](./hatanaka.md)；读 RINEX 见 [georinex](./georinex.md)；CDDIS 1 s 高采样见 [cddis-highrate-downloader](./cddis-highrate-downloader.md)；GUI 下载器见 [gnss-downloader](./gnss-downloader.md)；GIM 门户见 [gim-product-portals](./gim-product-portals.md)。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E28](../data-access.md#dp-e28)
>
> 冲突时：以镜像当时的目录列表为准（只代表 2026-09-26 这一次）；“到达率 / 上架延迟 / 完整性”的定义都是**本文自选**，见 §3.1 下方。

## 1. 用途与边界

**做：** 各匿名镜像的日观测目录路径；同一组站的到达率（24 站命中数）、完整性（解 Hatanaka 后历元数）、同一文件跨镜像是否同一份数据；`Last-Modified` 上架延迟；登录门槛。

**不做：** 高采样 / 小时文件；导航文件；产品（→ [gim-product-portals](./gim-product-portals.md)）；区域 CORS（NOAA、EPN、GeoNet、RBMC、SONEL 见 [cors-networks](./cors-networks.md)；CACS 等见 [data-access](../data-access.md)）。

**结论先说：**

| 镜像 | 日观测目录（匿名） | 本次状态 | 备注 |
| --- | --- | --- | --- |
| **BKG** | `https://igs.bkg.bund.de/root_ftp/IGS/obs/YYYY/DDD/` | 200 | 24/24（2024）、22/24（2026，缺的两站各镜像都缺）；**会重新压缩、重发文件**，gz 字节数与别处不同 |
| **CAS** | `https://data.bdsmart.cn/pub/data/igs/YYYY/DDD/` | 200 | 24/24、22/24；上架中位 0.4 h |
| **SOPAC** | `http://garner.ucsd.edu/pub/rinex/YYYY/DDD/` | 200（**只 http**；https 000、FTP PASV 超时） | 24/24、22/24；目录最全（1041 / 1410 个日文件，含非 IGS 站和旧短名 `.d.Z`）；最快（中位 0.3 h） |
| **GA** | `https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/YYYY/DDD/` | 200（S3 ListObjectsV2，1000 条/页须翻页） | 22/24、21/24：**缺 CHPI、TSK2**；APREF 区域站很多 |
| IGN | `https://igs.ign.fr/pub/igs/data/YYYY/DDD/` | **不通**（https TLS EOF / 5 s 断；http 40 s 超时；FTP 匿名 530） | |
| WHU | `http://igs.gnsswhu.cn/pub/gps/data/daily/YYYY/DDD/YYd/` | **不通**（http 502；FTP 425） | |
| KASI | `https://nfs.kasi.re.kr/gps/data/daily/YYYY/DDD/YYd/` | **不通**（https/ftp 000） | |
| GFZ ISDC | `https://isdc-data.gfz.de/gnss/data/daily/YYYY/DDD/` | 200 | **只有 GFZ 自家网 49 站**，不是 IGS 全镜像 |
| ESA GSSC | `https://gssc.esa.int/gnss/data/daily/…` | 404（FTP 21 端口拒连） | 未找到可用匿名路径 |
| **CDDIS** | `https://cddis.nasa.gov/archive/gnss/data/daily/YYYY/DDD/YYd/` | **302 到 urs.earthdata.nasa.gov** | **需 Earthdata 账号**（免费但要注册），本文不走 |

## 2. 安装

`curl`、`gzip`、Python 3（标准库即可，脚本不依赖第三方包）；解 Hatanaka 用 Rust `crx2rnx` 2.7.0（本机 `~/.cargo/bin/crx2rnx`，装法见 [crx2rnx](./crx2rnx.md)）。本机 Python 用 `/usr/bin/python3`。

```bash
curl --version | head -1; crx2rnx --version; /usr/bin/python3 --version
```

## 3. 真命令 + 期望输出

### 3.1 到达率 + 跨镜像字节数 + 上架延迟（`obs.py`）

站组（本文自选，24 站，覆盖各洲与两极）：ALIC BRUX CHPI DARW FAIR GODE HOB2 KIRU KOKB MAS1 MCM4 NKLG NYA1 POTS SGOC TSK2 URUM WTZR YELL ZIM2 HRAO JFNG KOUR MIZU。

```python
# 同一天、同一组 24 个 IGS 站，在各匿名镜像上的到达率 / 完整性 / 上架时刻
import re, time, urllib.request, urllib.error, statistics, datetime as dt
from concurrent.futures import ThreadPoolExecutor
SET = "ALIC BRUX CHPI DARW FAIR GODE HOB2 KIRU KOKB MAS1 MCM4 NKLG NYA1 POTS SGOC TSK2 URUM WTZR YELL ZIM2 HRAO JFNG KOUR MIZU".split()
PAT = re.compile(r'([A-Z0-9]{4})(\d\d)([A-Z]{3})_([RSU])_(\d{7})0000_01D_(\d\d[SM])_MO\.crx\.gz')
def dirs(y, d):
    return {'BKG':  f'https://igs.bkg.bund.de/root_ftp/IGS/obs/{y}/{d:03d}/',
            'CAS':  f'https://data.bdsmart.cn/pub/data/igs/{y}/{d:03d}/',
            'SOPAC': f'http://garner.ucsd.edu/pub/rinex/{y}/{d:03d}/',
            'GA':   f'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/{y}/{d:03d}/',
            'IGN':  f'https://igs.ign.fr/pub/igs/data/{y}/{d:03d}/',
            'WHU':  f'http://igs.gnsswhu.cn/pub/gps/data/daily/{y}/{d:03d}/{y%100:02d}d/',
            'KASI': f'https://nfs.kasi.re.kr/gps/data/daily/{y}/{d:03d}/{y%100:02d}d/'}
def get(url, t=40):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'curl/8'}), timeout=t) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return type(e).__name__, ''
def listing(name, url):
    t0 = time.time()
    if name == 'GA':   # S3 ListObjectsV2 分页
        base = 'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/?list-type=2&prefix=' + url.split('.com/')[1]
        txt, tok, st = '', None, None
        while True:
            st, x = get(base + ('&continuation-token=' + urllib.parse.quote(tok) if tok else ''))
            txt += x; m = re.search(r'<NextContinuationToken>([^<]+)', x)
            if not m: break
            tok = m.group(1)
    else:
        st, txt = get(url)
    return st, sorted(set(m.group(0) for m in PAT.finditer(txt))), time.time() - t0
def head(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'curl/8'}), timeout=40) as r:
            return int(r.headers.get('Content-Length', -1)), r.headers.get('Last-Modified')
    except Exception as e: return None, None
import urllib.parse
for y, d in [(2024, 132), (2026, 268)]:
    day_end = dt.datetime(y, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(days=d)
    print(f'\n##### {y}/{d:03d}（数据日结束 {day_end:%Y-%m-%d %H:%M} UTC）  探测时刻 {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC')
    L = {}
    print('镜像 | HTTP | 列表秒 | 日文件(01D MO crx.gz)总数 | 24 站命中 | 缺')
    for name, url in dirs(y, d).items():
        st, files, sec = listing(name, url)
        by = {}
        for f in files:
            if f[:4] in SET: by.setdefault(f[:4], []).append(f)
        L[name] = (url, by)
        miss = [s for s in SET if s not in by]
        print(f'{name} | {st} | {sec:.1f} | {len(files)} | {len(by)}/24 | {" ".join(miss) if len(miss) < 24 else "全缺"}')
    # 同文件跨镜像大小 + Last-Modified
    live = [n for n in L if L[n][1]]
    jobs = [(n, s, f) for n in live for s, fs in L[n][1].items() for f in fs if '_01D_30S_' in f]
    with ThreadPoolExecutor(12) as ex:
        res = dict(zip([(n, f) for n, s, f in jobs], ex.map(lambda j: head(L[j[0]][0] + j[2]), jobs)))
    sizes = {}
    for (n, f), (sz, lm) in res.items(): sizes.setdefault(f, {})[n] = (sz, lm)
    same = sum(1 for f, v in sizes.items() if len(v) > 1 and len({x[0] for x in v.values()}) == 1)
    multi = sum(1 for v in sizes.values() if len(v) > 1)
    print(f'30S 文件跨镜像：在 ≥2 个镜像上出现 {multi} 个，其中字节数完全一致 {same} 个')
    for f, v in sorted(sizes.items()):
        if len({x[0] for x in v.values()}) > 1: print('  大小不一致', f, {k: x[0] for k, x in v.items()})
    print('镜像 | 30S 文件数 | 中位上架延迟 h（Last-Modified − 日结束） | 最晚 h')
    for n in live:
        lat = []
        for (m, f), (sz, lm) in res.items():
            if m == n and lm:
                t = dt.datetime.strptime(lm, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=dt.timezone.utc)
                lat.append((t - day_end).total_seconds() / 3600)
        if lat: print(f'{n} | {len(lat)} | {statistics.median(lat):.1f} | {max(lat):.1f}')
        else: print(f'{n} | 0 | 无 Last-Modified | -')
```

输出（原样，2026-09-26 09:12 UTC = 05:12 EDT）：

```text

##### 2024/132（数据日结束 2024-05-12 00:00 UTC）  探测时刻 2026-09-26 09:12 UTC
镜像 | HTTP | 列表秒 | 日文件(01D MO crx.gz)总数 | 24 站命中 | 缺
BKG | 200 | 1.7 | 354 | 24/24 | 
CAS | 200 | 3.0 | 398 | 24/24 | 
SOPAC | 200 | 0.8 | 1041 | 24/24 | 
GA | 200 | 5.5 | 938 | 22/24 | CHPI TSK2
IGN | URLError | 5.3 | 0 | 0/24 | 全缺
WHU | 502 | 0.4 | 0 | 0/24 | 全缺
KASI | URLError | 5.0 | 0 | 0/24 | 全缺
30S 文件跨镜像：在 ≥2 个镜像上出现 24 个，其中字节数完全一致 0 个
  大小不一致 ALIC00AUS_R_20241320000_01D_30S_MO.crx.gz {'BKG': 7140275, 'CAS': 6776099, 'SOPAC': 6776099, 'GA': 6776099}
  大小不一致 BRUX00BEL_R_20241320000_01D_30S_MO.crx.gz {'BKG': 5110856, 'CAS': 5182002, 'SOPAC': 5182002, 'GA': 5185315}
  大小不一致 CHPI00BRA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3249857, 'CAS': 3292141, 'SOPAC': 3292141}
  大小不一致 DARW00AUS_R_20241320000_01D_30S_MO.crx.gz {'BKG': 7796577, 'CAS': 7399009, 'SOPAC': 7399009, 'GA': 7399009}
  大小不一致 FAIR00USA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3669958, 'CAS': 3489315, 'SOPAC': 3489315, 'GA': 3491425}
  大小不一致 GODE00USA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3026091, 'CAS': 2868980, 'SOPAC': 2868980, 'GA': 2870734}
  大小不一致 HOB200AUS_R_20241320000_01D_30S_MO.crx.gz {'BKG': 6381969, 'CAS': 6053832, 'SOPAC': 6053832, 'GA': 6053832}
  大小不一致 HRAO00ZAF_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3693368, 'CAS': 3510372, 'SOPAC': 3510372, 'GA': 3512635}
  大小不一致 JFNG00CHN_R_20241320000_01D_30S_MO.crx.gz {'BKG': 5783122, 'CAS': 5783122, 'SOPAC': 5783122, 'GA': 5502475}
  大小不一致 KIRU00SWE_R_20241320000_01D_30S_MO.crx.gz {'BKG': 4889843, 'CAS': 4901211, 'SOPAC': 4901211, 'GA': 4965841}
  大小不一致 KOKB00USA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3673356, 'CAS': 3491180, 'SOPAC': 3491180, 'GA': 3493504}
  大小不一致 KOUR00GUF_R_20241320000_01D_30S_MO.crx.gz {'BKG': 4703150, 'CAS': 4400786, 'SOPAC': 4400786, 'GA': 4460183}
  大小不一致 MAS100ESP_R_20241320000_01D_30S_MO.crx.gz {'BKG': 4535311, 'CAS': 4238839, 'SOPAC': 4238839, 'GA': 4296429}
  大小不一致 MCM400ATA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 2362239, 'CAS': 2241404, 'SOPAC': 2241404, 'GA': 2242693}
  大小不一致 MIZU00JPN_R_20241320000_01D_30S_MO.crx.gz {'BKG': 7029461, 'CAS': 6676340, 'SOPAC': 6676340, 'GA': 6680233}
  大小不一致 NKLG00GAB_R_20241320000_01D_30S_MO.crx.gz {'BKG': 6044272, 'CAS': 6044272, 'SOPAC': 6044272, 'GA': 5738076}
  大小不一致 NYA100NOR_S_20241320000_01D_30S_MO.crx.gz {'BKG': 3164129, 'CAS': 2988084, 'SOPAC': 2988084, 'GA': 2989867}
  大小不一致 POTS00DEU_R_20241320000_01D_30S_MO.crx.gz {'BKG': 6710473, 'CAS': 6815794, 'SOPAC': 6815794, 'GA': 6818900}
  大小不一致 SGOC00LKA_R_20241320000_01D_30S_MO.crx.gz {'BKG': 9680630, 'CAS': 9325471, 'SOPAC': 9325471, 'GA': 9327957}
  大小不一致 TSK200JPN_R_20241320000_01D_30S_MO.crx.gz {'BKG': 2202208, 'CAS': 2089321, 'SOPAC': 2089321}
  大小不一致 URUM00CHN_R_20241320000_01D_30S_MO.crx.gz {'BKG': 8146460, 'CAS': 7807382, 'SOPAC': 7807382, 'GA': 7807635}
  大小不一致 WTZR00DEU_R_20241320000_01D_30S_MO.crx.gz {'BKG': 3758992, 'CAS': 3782487, 'SOPAC': 4040864, 'GA': 3849264}
  大小不一致 YELL00CAN_R_20241320000_01D_30S_MO.crx.gz {'BKG': 2624790, 'CAS': 2492460, 'SOPAC': 2492460, 'GA': 2493827}
  大小不一致 ZIM200CHE_R_20241320000_01D_30S_MO.crx.gz {'BKG': 2200215, 'CAS': 2327337, 'SOPAC': 2327337, 'GA': 2328716}
镜像 | 30S 文件数 | 中位上架延迟 h（Last-Modified − 日结束） | 最晚 h
BKG | 24 | 56.6 | 8244.3
CAS | 24 | 460.5 | 460.5
SOPAC | 24 | 0.3 | 137.1
GA | 22 | 1.3 | 1753.2

##### 2026/268（数据日结束 2026-09-26 00:00 UTC）  探测时刻 2026-09-26 09:12 UTC
镜像 | HTTP | 列表秒 | 日文件(01D MO crx.gz)总数 | 24 站命中 | 缺
BKG | 200 | 1.7 | 330 | 22/24 | KOKB JFNG
CAS | 200 | 2.2 | 427 | 22/24 | KOKB JFNG
SOPAC | 200 | 0.6 | 1410 | 22/24 | KOKB JFNG
GA | 200 | 5.5 | 1023 | 21/24 | KOKB TSK2 JFNG
IGN | URLError | 5.3 | 0 | 0/24 | 全缺
WHU | 502 | 0.2 | 0 | 0/24 | 全缺
KASI | URLError | 5.0 | 0 | 0/24 | 全缺
30S 文件跨镜像：在 ≥2 个镜像上出现 22 个，其中字节数完全一致 0 个
  大小不一致 ALIC00AUS_R_20262680000_01D_30S_MO.crx.gz {'BKG': 6598256, 'CAS': 6264306, 'SOPAC': 6264306, 'GA': 6264306}
  大小不一致 BRUX00BEL_R_20262680000_01D_30S_MO.crx.gz {'BKG': 5261131, 'CAS': 4974013, 'SOPAC': 4974013, 'GA': 4977150}
  大小不一致 CHPI00BRA_R_20262680000_01D_30S_MO.crx.gz {'BKG': 3783048, 'CAS': 3590018, 'SOPAC': 3590018, 'GA': 3592185}
  大小不一致 DARW00AUS_R_20262680000_01D_30S_MO.crx.gz {'BKG': 7232965, 'CAS': 6868082, 'SOPAC': 6868082, 'GA': 6868082}
  大小不一致 FAIR00USA_R_20262680000_01D_30S_MO.crx.gz {'BKG': 3796744, 'CAS': 3610696, 'SOPAC': 3610696, 'GA': 3612632}
  大小不一致 GODE00USA_R_20262680000_01D_30S_MO.crx.gz {'BKG': 3135821, 'CAS': 2968002, 'SOPAC': 2968002, 'GA': 2969720}
  大小不一致 HOB200AUS_R_20262680000_01D_30S_MO.crx.gz {'BKG': 5987141, 'CAS': 5680510, 'SOPAC': 5680510, 'GA': 5680510}
  大小不一致 HRAO00ZAF_R_20262680000_01D_30S_MO.crx.gz {'BKG': 3437243, 'CAS': 3263002, 'SOPAC': 3263002, 'GA': 3265113}
  大小不一致 KIRU00SWE_R_20262680000_01D_30S_MO.crx.gz {'BKG': 5113687, 'CAS': 4786644, 'SOPAC': 4786644, 'GA': 4850484}
  大小不一致 KOUR00GUF_R_20262680000_01D_30S_MO.crx.gz {'BKG': 5035200, 'CAS': 4702646, 'SOPAC': 4702646, 'GA': 4768126}
  大小不一致 MAS100ESP_R_20262680000_01D_30S_MO.crx.gz {'BKG': 4683373, 'CAS': 4381184, 'SOPAC': 4381184, 'GA': 4438634}
  大小不一致 MCM400ATA_R_20262680000_01D_30S_MO.crx.gz {'BKG': 4659725, 'CAS': 4421975, 'SOPAC': 4421975, 'GA': 4424646}
  大小不一致 MIZU00JPN_R_20262680000_01D_30S_MO.crx.gz {'BKG': 6588096, 'CAS': 6257976, 'SOPAC': 6257976, 'GA': 6261656}
  大小不一致 NKLG00GAB_R_20262680000_01D_30S_MO.crx.gz {'BKG': 6408722, 'CAS': 6408722, 'SOPAC': 6408722, 'GA': 6081701}
  大小不一致 NYA100NOR_S_20262680000_01D_30S_MO.crx.gz {'BKG': 3614392, 'CAS': 3408710, 'SOPAC': 3408710, 'GA': 3410703}
  大小不一致 POTS00DEU_R_20262680000_01D_30S_MO.crx.gz {'BKG': 6102507, 'CAS': 5827964, 'SOPAC': 5827964, 'GA': 5831030}
  大小不一致 SGOC00LKA_R_20262680000_01D_30S_MO.crx.gz {'BKG': 6538342, 'CAS': 6205190, 'SOPAC': 6205190, 'GA': 6208923}
  大小不一致 TSK200JPN_R_20262680000_01D_30S_MO.crx.gz {'BKG': 2185219, 'CAS': 2075411, 'SOPAC': 2075411}
  大小不一致 URUM00CHN_R_20262680000_01D_30S_MO.crx.gz {'BKG': 7237781, 'CAS': 6926012, 'SOPAC': 6926012, 'GA': 6924735}
  大小不一致 WTZR00DEU_R_20262680000_01D_30S_MO.crx.gz {'BKG': 4180347, 'CAS': 4180347, 'SOPAC': 4180347, 'GA': 3960524}
  大小不一致 YELL00CAN_R_20262680000_01D_30S_MO.crx.gz {'BKG': 3285072, 'CAS': 3134441, 'SOPAC': 3134441, 'GA': 3136167}
  大小不一致 ZIM200CHE_R_20262680000_01D_30S_MO.crx.gz {'BKG': 4559599, 'CAS': 4335018, 'SOPAC': 4335018, 'GA': 4337749}
镜像 | 30S 文件数 | 中位上架延迟 h（Last-Modified − 日结束） | 最晚 h
BKG | 22 | 9.0 | 9.0
CAS | 22 | 0.4 | 4.6
SOPAC | 22 | 0.3 | 4.6
GA | 21 | 0.3 | 5.3
```

**本文定义：**

- **到达率** = 该镜像目录里能找到的站组日文件数 / 24（任意采样间隔，`01D_*_MO.crx.gz`）。
- **上架延迟** = HTTP `Last-Modified` − 数据日结束（24:00 UTC）。**注意**：它记录的是镜像上这个文件最后一次写入的时间，重发 / 重压缩会把它推后（BKG 2024 年文件“最晚 8244 h”就是 2025-04 重发；CAS 2024 年全是 460 h，是整批灌入的时间）。**只有“前一天”的数据（DOY 268）才能看出真实到达速度。**
- 字节数不一致**不等于**数据不同，见 §3.2。

**读法（DOY 268，探测前一天）：** SOPAC / GA / CAS 中位 0.3–0.4 h 就到了，最晚 4.6–5.3 h；BKG 全部 22 个文件 `Last-Modified` 都是 9.0 h（整批同一时刻写入）。22/24 是因为 KOKB、JFNG 在**所有**镜像上都还没有（站点本身没交），不是镜像的问题；GA 另缺 TSK2（GA 这两天都没有 TSK2、CHPI）。

### 3.2 同站同日 4 个镜像：是不是同一份数据（`cmpfile.sh`）

拉 3 个站 × 4 个镜像（2024/132，共约 50 MB，测完即删）：

```bash
for s in WTZR00DEU YELL00CAN NKLG00GAB; do f=${s}_R_20241320000_01D_30S_MO.crx.gz
  for m in BKG:https://igs.bkg.bund.de/root_ftp/IGS/obs/2024/132 CAS:https://data.bdsmart.cn/pub/data/igs/2024/132 \
           SOPAC:http://garner.ucsd.edu/pub/rinex/2024/132 GA:https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/2024/132; do
    n=${m%%:*}; u=${m#*:}; curl -s -m 120 -o $n.$f -w "$n %{http_code} %{size_download} %{time_total}s $f\n" $u/$f; done; done
```

本机实测：12 个全 200；耗时 SOPAC 0.7 s/个、GA 2.0–2.2 s、BKG 4.5–8.6 s、CAS 4.6–10.2 s（从美东机房测，仅供参考）。

```bash
#!/usr/bin/env bash
# 同一站同一天、4 个镜像的文件：gz 字节 → 解压后 CRX md5 → CRINEX 程序/日期 → 解 Hatanaka 后历元数、首末历元、观测段 md5（跳过头）
for f in *.crx.gz; do
  c="${f%.gz}"; r="${f%.crx.gz}.rnx"; gzip -dc "$f" > "$c"
  prog=$(sed -n 2p "$c" | cut -c1-60 | tr -s ' ')
  if crx2rnx -q -o "$r" "$c" >/dev/null 2>&1; then
    ep=$(grep -c '^>' "$r"); t1=$(grep '^>' "$r" | tail -1 | cut -c3-21)
    body=$(sed '1,/END OF HEADER/d' "$r" | md5sum | cut -c1-10)
  else ep="crx2rnx崩溃"; t1="-"; body="-"; fi
  printf '%-46s gz=%8d crx=%s | %-38s | epochs=%s last=%s body=%s\n' "$f" "$(stat -c %s "$f")" "$(md5sum < "$c" | cut -c1-10)" "$prog" "$ep" "$t1" "$body"
done
```

输出（原样）：

```text
BKG.NKLG00GAB_R_20241320000_01D_30S_MO.crx.gz  gz= 6044272 crx=72be61ae09 | RNX2CRX ver.4.1.0 12-May-24 00:43      | epochs=2880 last=2024 05 11 23 59 30 body=7344736a59
BKG.WTZR00DEU_R_20241320000_01D_30S_MO.crx.gz  gz= 3758992 crx=404615cf84 | RNX2CRX ver.4.1.0 20-Apr-25 11:38      | epochs=2880 last=2024 05 11 23 59 30 body=b3b96e2337
BKG.YELL00CAN_R_20241320000_01D_30S_MO.crx.gz  gz= 2624790 crx=0ee130516b | RNX2CRX ver.4.1.0 14-May-24 08:41      | epochs=2880 last=2024 05 11 23 59 30 body=6dd1110039
CAS.NKLG00GAB_R_20241320000_01D_30S_MO.crx.gz  gz= 6044272 crx=72be61ae09 | RNX2CRX ver.4.1.0 12-May-24 00:43      | epochs=2880 last=2024 05 11 23 59 30 body=7344736a59
CAS.WTZR00DEU_R_20241320000_01D_30S_MO.crx.gz  gz= 3782487 crx=26ad9a5d17 | RNX2CRX ver.4.0.7 12-05-24 00:06       | epochs=crx2rnx崩溃 last=- body=-
CAS.YELL00CAN_R_20241320000_01D_30S_MO.crx.gz  gz= 2492460 crx=c0969a6284 | RNX2CRX ver.4.0.8 12-May-24 00:11      | epochs=2880 last=2024 05 11 23 59 30 body=6dd1110039
GA.NKLG00GAB_R_20241320000_01D_30S_MO.crx.gz   gz= 5738076 crx=72be61ae09 | RNX2CRX ver.4.1.0 12-May-24 00:43      | epochs=2880 last=2024 05 11 23 59 30 body=7344736a59
GA.WTZR00DEU_R_20241320000_01D_30S_MO.crx.gz   gz= 3849264 crx=26ad9a5d17 | RNX2CRX ver.4.0.7 12-05-24 00:06       | epochs=crx2rnx崩溃 last=- body=-
GA.YELL00CAN_R_20241320000_01D_30S_MO.crx.gz   gz= 2493827 crx=c0969a6284 | RNX2CRX ver.4.0.8 12-May-24 00:11      | epochs=2880 last=2024 05 11 23 59 30 body=6dd1110039
SOPAC.NKLG00GAB_R_20241320000_01D_30S_MO.crx.gz gz= 6044272 crx=72be61ae09 | RNX2CRX ver.4.1.0 12-May-24 00:43      | epochs=2880 last=2024 05 11 23 59 30 body=7344736a59
SOPAC.WTZR00DEU_R_20241320000_01D_30S_MO.crx.gz gz= 4040864 crx=102c0ae385 | RNX2CRX ver.4.1.0 12-May-24 00:15      | epochs=2880 last=2024 05 11 23 59 30 body=b3b96e2337
SOPAC.YELL00CAN_R_20241320000_01D_30S_MO.crx.gz gz= 2492460 crx=c0969a6284 | RNX2CRX ver.4.0.8 12-May-24 00:11      | epochs=2880 last=2024 05 11 23 59 30 body=6dd1110039
```

读法：

- **NKLG**：4 份解压后 CRX 完全一样（`72be61ae09`），只是 GA 用了别的 gzip 压缩级别（5,738,076 vs 6,044,272 B）。
- **YELL**：BKG 那份是 2024-05-14 08:41 重新压缩的（RNX2CRX 4.1.0），其余三份是 05-12 00:11 的原版（4.0.8）；**解压后观测段 md5 相同**（`6dd1110039`）。
- **WTZR**：3 个版本——BKG（2025-04-20 重压）、SOPAC（05-12 00:15）、CAS=GA（RNX2CRX **4.0.7**，头里日期写成 `12-05-24 00:06`）。BKG 与 SOPAC 解压后观测段 md5 相同（`b3b96e2337`）。**CAS/GA 这一版让 Rust crx2rnx 2.7.0 panic（`datime parsing`）**：把第 2 行日期手工改成 `12-May-24 00:06` 后能解，观测段 md5 同样是 `b3b96e2337`，与 BKG 解出的 RINEX 只差头里 8 行（`PGM / RUN BY / DATE` 秒数、`GLONASS SLOT / FRQ #` 排列顺序）。
- **完整性**：能解开的 10 份全部 2880 历元（30 s × 24 h），末历元 23:59:30。本次抽检没有发现哪个镜像少历元。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| 日期 | `YYYY/DDD`（年积日 3 位）；WHU/KASI/CDDIS 多一层 `YYd/` |
| 站名 | RINEX 3 长名 9 位 `SSSSMRCCC`（如 `NYA100NOR`），类型 `_R_`（接收机）/ `_S_`（流）；NYA1 这两天是 `_S_` |
| 采样 | IGS 日文件多数 `30S`；部分站只有 `15S`（CAS 目录里 AC23/AC24 是 15S） |

| 输出 | 说明 |
| --- | --- |
| `*_01D_30S_MO.crx.gz` | Hatanaka 压缩 + gzip；解压 `gzip -dc` 后 `crx2rnx` |
| SOPAC 目录 | 同时有旧短名 `ssssDDD0.YYd.Z`（Unix compress） |

## 5. 参数（选镜像时要看的量）

| 量 | BKG | CAS | SOPAC | GA |
| --- | --- | --- | --- | --- |
| 2024/132 日文件总数 | 354 | 398 | 1041 | 938 |
| 2026/268 日文件总数（探测时） | 330 | 427 | 1410 | 1023 |
| 24 站命中（2024 / 2026） | 24 / 22 | 24 / 22 | 24 / 22 | 22 / 21 |
| 前一天上架中位 / 最晚（h） | 9.0 / 9.0 | 0.4 / 4.6 | 0.3 / 4.6 | 0.3 / 5.3 |
| 列目录耗时（s） | 1.7 | 2.2–3.0 | 0.6–0.8 | 5.5（翻页） |
| 协议 | HTTPS | HTTPS | 只 HTTP | HTTPS（S3） |

## 6. 接到哪一步

| 下一步 | 去哪 |
| --- | --- |
| 解 Hatanaka | [crx2rnx](./crx2rnx.md)（注意坑 6）· [hatanaka](./hatanaka.md) |
| 读 RINEX / 算 TEC | [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [gnss-tec](./gnss-tec.md) |
| 与 GIM 对比 | [gim-product-portals](./gim-product-portals.md) · [ionex-gim](./ionex-gim.md) |
| 1 s 高采样（需 Earthdata） | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 下载总表 | [data-access E28](../data-access.md#dp-e28) |

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | CDDIS 下回来是 HTML | 302 到 Earthdata 登录 | 匿名场景换 BKG / CAS / SOPAC / GA；要 CDDIS 就注册 Earthdata 并配 `.netrc` |
| 2 | 同名文件各镜像字节数全不一样 | 各镜像重新 gzip / 重新 Hatanaka 压缩 | 比**解压后**内容，最好比解 Hatanaka 后跳过头部的观测段 |
| 3 | 同名文件头部不同 | BKG 会重发（WTZR 2025-04-20、YELL 2024-05-14），头里 `PGM` 秒数、GLONASS 槽位顺序可能变 | 可复现实验记录镜像 + CRINEX PROG/DATE 行 |
| 4 | 用 `Last-Modified` 算延迟得出几百小时 | 重发 / 整批灌入会刷新时间 | 只对“前一天”数据看延迟；历史日不要用 |
| 5 | GA 列表只拿到 1000 个 | S3 ListObjectsV2 分页 | 跟 `NextContinuationToken` 翻页 |
| 6 | CAS/GA 的 WTZR 让 crx2rnx panic `datime parsing` | RNX2CRX 4.0.7 写的 `CRINEX PROG / DATE` 日期是 `12-05-24 00:06`（数字月），Rust 解析器不认 | 换镜像（BKG/SOPAC 版能解）；或改第 2 行日期为 `12-May-24 00:06`；或用 C 版 RNXCMP |
| 7 | SOPAC https 连不上 | garner 只开 http；FTP PASV 40 s 超时 | 用 `http://garner.ucsd.edu/pub/rinex/` |
| 8 | GA 缺 CHPI、TSK2 | GA 是 APREF 区域中心，不收全部 IGS 站 | 缺站去 SOPAC / CAS 补 |
| 9 | 以为 GFZ ISDC 是 IGS 镜像 | 日目录只有 GFZ 自家 49 站 | IGS 全站用别的镜像 |
| 10 | 所有镜像都缺某站 | 站点当天没交数据（DOY 268 的 KOKB、JFNG） | 不是镜像问题；换天或换站 |
| 11 | IGN / WHU / KASI 下不到 | 本次 TLS EOF、502 / 425、000 超时 | 以 BKG / CAS / SOPAC / GA 为主，换天再试 |
| 12 | NYA1 找不到 `_R_` 文件 | 这两天只有 `_S_`（流数据生成） | 匹配站名时不要写死 `_R_` |

## 8. 选型

| 需求 | 选 | 不选 |
| --- | --- | --- |
| 最快拿到前一天 IGS 日观测 | **SOPAC**（http）或 CAS | BKG（本次 9 h） |
| 最全（含非 IGS 站） | SOPAC | GFZ ISDC |
| 澳洲 / 亚太区域站 | GA S3 | — |
| 欧洲访问稳定、结构清楚 | BKG | IGN（本次不通） |
| 需要 1 s / CDDIS 独有 | CDDIS（Earthdata） | 匿名镜像 |
| 验证“同一份数据” | 比解 Hatanaka 后观测段 md5 | 比 gz 字节数 |
