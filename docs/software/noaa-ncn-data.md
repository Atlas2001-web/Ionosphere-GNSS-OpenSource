# NOAA CORS 网（NCN）数据直连（NODD S3 · corsdata 目录树 · NCN 站点 API · UFCORS）· 下载侧 操作手册

入口：[NCN API](https://geodesy.noaa.gov/web_services/ncn-api.shtml) · [NODD S3 桶 `noaa-cors-pds`](https://noaa-cors-pds.s3.amazonaws.com/index.html) · [corsdata 目录树](https://geodesy.noaa.gov/corsdata/) · [UFCORS](https://geodesy.noaa.gov/UFCORS/) · 目录条目 `NOAA-NCN-API` / `NOAA-CORS-AWS` / `NOAA-CORS-Data-Tree` / `NOAA-UFCORS`（均 portal-terms，official）。
本机验证 **2026-09-26 05:21–05:40 EDT**。只用 curl、gzip 和系统 Python 3 标准库，没有 aws CLI，也不需要账号。样例站 **P041**（Boulder，EarthScope 转入）和 **1LSU**（NGS 自营）。

> **质检复跑通过（2026-09-26 06:02–06:05 EDT）**：§3.1–3.5、§3.7–3.9 的实测值全部复现：1LSU/P041 API 坐标、ncors 9 站及其距离、S3 列表三个键和 Size、S3/corsdata md5 相同（0.13 s / 1.04 s）、2880 历元、SUM 行、coord ITRF2020/NAD83、UFCORS zip（这次 297652 B，原文 297651）、`ncn_get.py` 输出、坑 1/2/6/7/8 的报错与 24737011 B。唯一更正在 §3.6 和坑 3：P041 2026-267/268 的日文件其实早已上桶（09-25 11:16Z / 09-26 03:16Z）；262 的日文件是日终后约 11 h 上桶，不是 1.5 天。原文“72 个小时文件”实为 69 个小时文件 + 3 个日文件。
>
> 岗位：给 TEC/ROTI、PPP 和 CORS 基线**拿美国 CORS 的 RINEX 和站坐标**。  
> 本文**不讲** IGS 全球站镜像（见 [gnss-obs-mirrors](./gnss-obs-mirrors.md)）、CDDIS 高频（见 [cddis-highrate-downloader](./cddis-highrate-downloader.md)）和 GUI 下载器（见 [gdds](./gdds.md)）。

## 1. 四个入口，各管什么

| 入口 | 地址 | 给什么 | 实测 |
| --- | --- | --- | --- |
| **NODD S3**（主力） | `https://noaa-cors-pds.s3.amazonaws.com/<key>` | RINEX 日/小时文件、brdc、IGS SP3、坐标文件、站点日志 | 1.7 MB 文件 0.14 s；可以 ListObjectsV2 列目录 |
| **corsdata 目录树** | `https://geodesy.noaa.gov/corsdata/rinex/...` | 与 S3 同名同内容（md5 一致） | 同一文件约 1.0 s；列一天的目录（1612 站）要 **22 s** |
| **NCN API** | `https://geodesy.noaa.gov/api/nde/{cors,ncors,meta}` | 站点属性 JSON、最近 9 站 | 约 1 s；只有元数据 |
| **UFCORS** | `POST https://geodesy.noaa.gov/UFCORS/ufcors` | 任意整点起、1–24 h、可降采样的 zip | 1 h 请求 1.6–1.8 s |

- **账号**：四个入口都不用账号、key 或 cookie。
- **格式**：NCN 归档是 **RINEX 2.11**，短文件名 `ssssDDDh.YYt`。本次看过的 S3 目录里只有短文件名，没见到 RINEX 3 长文件名。

## 2. 安装

```bash
# 只需要 curl + gzip + python3（标准库）。解 .d.gz 里的 Hatanaka 时再装 crx2rnx（见 hatanaka.md / crx2rnx.md）
curl --version | head -1; python3 -V
```

## 3. 逐步命令 + 实测输出

### 3.1 NCN API：按站名取属性

```bash
curl -s 'https://geodesy.noaa.gov/api/nde/cors?id=1lsu' | python3 -c \
 'import json,sys;s=json.load(sys.stdin)[0];print(s["corsId"],s["posDatum"],s["epoch"],s["x"],s["y"],s["z"],s["netAccHz"])'
# 1LSU NAD 83(2011) 2010.00 -113402.181 -5504362.817 3209404.367 0.54
```

- 返回的是**长度为 1 的数组**，共 53 个字段（`pid`、`lat/lon`、`ellipHeight`、`orthoHt`、`geoidHt`、`netAcc*`、`x/y/z`、`spc*`、`utm*`…），字段含义见 `api/nde/meta`。
- 站名不分大小写（`1lsu` 与 `P041` 都行）。
- 官网示例响应是旧值（x=−113402.172）；以实时返回为准。

### 3.2 NCN API：按 ECEF 找最近站

```bash
curl -s 'https://geodesy.noaa.gov/api/nde/ncors?x=-1283610&y=-4726470&z=4074900' | python3 -c \
 'import json,sys;[print(r["corsId"],r["distance"]) for r in json.load(sys.stdin)[:5]]'
# P041 65.84
# DSRC 7353.51
# TMG2 20259.55
# TMG0 20361.08
# TMGO 20361.38
```

固定返回 **9** 个站，按距离（米）升序。结果里会有 `TMG0 "OLD TABLE MOUNTN"` 这类老站，是否还在出数据要去 S3 查（§3.3）。

### 3.3 S3：列目录（ListObjectsV2）

```bash
B=https://noaa-cors-pds.s3.amazonaws.com
curl -s "$B/?list-type=2&delimiter=/&prefix=rinex/2024/001/p041/" | grep -o '<Key>[^<]*</Key><LastModified>[^<]*'
# 输出整理后（Size 另从 <Size> 取）：
# rinex/2024/001/p041/p0410010.24S ... 2024-02-03T04:05:50Z   (69562 B)
# rinex/2024/001/p041/p0410010.24d.gz  2024-01-02T11:16:56Z   (1769574 B)
# rinex/2024/001/p041/p0410010.24o.gz  2024-02-03T04:05:51Z   (4445474 B)
```

桶顶层：`rinex/`（1994–2026）、`coord/`、`station_log/`（2901 个键）、`raw/`（2008 起）、`Plots/`、`cors/`，另有一个 `index.html`。

| 路径 | 内容 |
| --- | --- |
| `rinex/YYYY/DDD/ssss/ssssDDD0.YYd.gz` | 日文件，Hatanaka + gzip |
| `rinex/YYYY/DDD/ssss/ssssDDD0.YYo.gz` | 日文件，**普通 RINEX** + gzip，不用 crx2rnx |
| `rinex/YYYY/DDD/ssss/ssssDDD0.YYS` | teqc `+qc` 摘要（历元数、MP12/MP21、周跳） |
| `rinex/YYYY/DDD/ssss/ssssDDD{a..x}.YY{d.gz,o.gz,S}` | 小时文件（a = 00–01 UT） |
| `rinex/YYYY/DDD/brdcDDD0.YY{n,g}.gz`、`igs*/igr*/igu*/IGS0OPS*.sp3.gz` | 当天广播星历与 IGS 轨道 |
| `coord/coord_20/ssss_20.coord.txt` | ITRF2020 与 NAD 83(2011) 坐标和速度（还有 `coord_00/08/14/93`） |
| `station_log/ssss.log.txt` | IGS 格式站点日志 |

### 3.4 下载并和 corsdata 对比

```bash
for b in $B https://geodesy.noaa.gov/corsdata; do
  curl -s -o t.gz -w "%{http_code} %{size_download}B %{time_total}s " $b/rinex/2024/001/p041/p0410010.24d.gz; md5sum t.gz; done
# 200 1769574B 0.144478s 561ec27bde2b98e0dca56b8ac719dfab  (S3)
# 200 1769574B 1.035611s 561ec27bde2b98e0dca56b8ac719dfab  (corsdata)
```

`brdc0010.24n.gz`（68963 B）、`p0410010.24S`（69562 B）、`brdc2680.26n.gz`（69108 B）两边的 md5 也一致。

### 3.5 看内容：.o.gz 与 .S

```bash
curl -s -O $B/rinex/2024/001/p041/p0410010.24o.gz && gunzip -c p0410010.24o.gz | grep -E 'RINEX VERSION|INTERVAL|TIME OF FIRST|REC #'
#      2.11           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE
# 3222767             SEPT POLARX5        5.5.0               REC # / TYPE / VERS
#     30.0000                                                 INTERVAL
#   2024     1     1     0     0    0.0000000     GPS         TIME OF FIRST OBS
gunzip -c p0410010.24o.gz | grep -c '^ 24  1  1'        # 2880（30 s 满天）
curl -s $B/rinex/2024/001/p041/p0410010.24S | grep '^SUM'
# SUM 2024:001 00:00 2024:001 23:59 24.00  30  48999  46138  94  0.33  0.26   2307
```

- `.24o.gz` 为 4445474 B，解压后 15397461 B，观测类型 20 种（L1 L2 C1 P2 P1 S1 S2 C2 L5 C5 S5 L6 C6 S6 L7 C7 S7 L8 C8 S8）。
- `.S` 的 SUM 行：预期 48999 条，实有 46138 条（94%），MP1 0.33 m，MP2 0.26 m，观测数/周跳比 2307。做 ROTI 之前可以先用它筛站。
- 2026 年 NGS 自营站 1LSU 的日文件是 **15 s**、GPS+GLO+GAL（`1lsu2680.26o.gz` 5821318 B）。

### 3.6 时延：小时文件与日文件

```bash
python3 ncn_get.py ...   # 见 §3.9；也可以直接列目录：
curl -s "$B/?list-type=2&prefix=rinex/2026/269/1lsu/" | grep -o '1lsu269i[^<]*</Key><LastModified>[^<]*'
# 1lsu269i.26S ... 2026-09-26T09:15:24Z  (i = 08–09 UT；在 09:24 UT 查询时已经在桶上)
```

| 文件 | 实测上桶时间 |
| --- | --- |
| 1LSU 小时文件 `268a` | 2026-09-25 01:15Z（整点后约 15 min） |
| 1LSU 日文件 `2680` | 2026-09-26 05:15Z（日终后约 5 h） |
| `brdc2680.26n.gz` | 2026-09-26 04:45Z |
| P041（EarthScope 转入）日文件 | 262（09-19）在 09-20 11:16Z 上桶，267（09-24）在 09-25 11:16Z，268（09-25）在 09-26 03:16Z，即日终后约 **3–11 h**。每天目录共 72 个键：69 个小时文件（缺 `x` = 23–24 UT）+ 3 个日文件（`.S/.d.gz/.o.gz`） |

corsdata 目录页显示的时间是**美东时间**（`1lsu2680` 显示 00:46，即 04:46Z），比 S3 早 2–30 分钟。

### 3.7 坐标：API 给 NAD 83，coord 文件给 ITRF2020

```bash
curl -s $B/coord/coord_20/p041_20.coord.txt | grep -A4 -E 'ITRF2020 POSITION|NAD_83 \(2011\) POSITION' | head -12
# 输出整理后：
# ITRF2020 POSITION (EPOCH 2020.0)   X = -1283634.388  Y = -4726427.883  Z = 4074797.963
# NAD_83 (2011) POSITION (EPOCH 2010.0) X = -1283633.473  Y = -4726429.204  Z = 4074798.089
```

NCN API 返回的 x/y/z 就是 NAD 83(2011)（P041 为 −1283633.473 / −4726429.204 / 4074798.089，与 coord 文件的 NAD 83 行逐位相同），和 ITRF2020 差约 **1.6 m**（ΔX/ΔY/ΔZ = 0.915/1.321/−0.126 m）。做 PPP 真值、IGS 框架比较或 TEC 硬件偏差时，要用 coord 文件里的 ITRF2020 值，并用速度外推到观测历元。

### 3.8 UFCORS：脚本化取任意时段

```bash
curl -s -o u.zip -w '%{http_code} %{content_type}\n' https://geodesy.noaa.gov/UFCORS/ufcors \
  --data 'yearday=2026%7C268&starttime=01:00&timezone=UTC&duration=1&siteselection=1lsu&epochInterval=30&GPS=on&GLO=on&SUBMIT=get+CORS+data+file'
# 200 application/zip        （297651 B，1lsu268.zip）
unzip -l u.zip   # 1lsu2680.26o 534694 | 1lsu2680.26n 288098 | 1lsu2680.26g 407399 | 1lsu.log.txt 28794 | README.txt
```

| 字段 | 取值 |
| --- | --- |
| `yearday` | `YYYY\|DDD`（竖线要编码成 `%7C`；网页端由 datepicker 按 `yy\|oo` 生成） |
| `starttime` / `timezone` | `00:00`…`23:00` / `UTC`、`GMT-5` 等 |
| `duration` | 1–24（小时） |
| `epochInterval` | `As Is`、1、5、15、30 |
| `GPS=on` / `GLO=on` / `GPS12=on` | 可选系统，站点可用项来自 `SelectSatSystems?siteselection=1lsu&date=09/25/2026`。**都不勾时只出 GPS**（实测 `G (GPS)`，194104 B） |
| `coordinatefile` / `datasheets` / `orbits` | `yes` 时额外打包坐标、datasheet、SP3 |

- 输出是**未压缩的 RINEX 2.11**。01:00 起 1 h 共 121 个历元，首尾两个整点都包含在内。
- 站不存在或没数据时，返回的**仍是 HTTP 200**，但内容是 `text/html` 错误页（"UFCORS Error … not available at this time … Error code: /cors/rinex/2026/268/zzzz"）。脚本要检查 Content-Type。

### 3.9 批量脚本（标准库，按 S3 Size 校验）

```python
#!/usr/bin/env python3
"""ncn_get.py YYYY DOY sta1 [sta2 ...]：从 NODD S3 下日文件 .d.gz + brdc，按 S3 Size 校验"""
import sys, re, os, urllib.request, urllib.parse
B = "https://noaa-cors-pds.s3.amazonaws.com"
def ls(prefix):
    out, tok = {}, None
    while True:
        q = {"list-type": "2", "prefix": prefix}
        if tok: q["continuation-token"] = tok
        t = urllib.request.urlopen(B + "/?" + urllib.parse.urlencode(q), timeout=30).read().decode()
        for c in re.findall(r"<Contents>(.*?)</Contents>", t):       # 不要假设 Key/Size 相邻（§6 坑 2）
            out[re.search(r"<Key>([^<]*)", c).group(1)] = int(re.search(r"<Size>(\d+)", c).group(1))
        m = re.search(r"<NextContinuationToken>([^<]*)<", t)
        if not m: return out
        tok = m.group(1)
y, d, stas = sys.argv[1], sys.argv[2].zfill(3), [s.lower() for s in sys.argv[3:]]
yy = y[2:]
want = [f"rinex/{y}/{d}/brdc{d}0.{yy}n.gz"] + [f"rinex/{y}/{d}/{s}/{s}{d}0.{yy}d.gz" for s in stas]
for k in want:
    sz = ls(k).get(k)
    if sz is None:
        print("MISSING", k); continue
    fn = os.path.basename(k)
    urllib.request.urlretrieve(f"{B}/{k}", fn)
    print("OK " if os.path.getsize(fn) == sz else "BAD", fn, sz)
```

```text
$ python3 ncn_get.py 2026 262 p041 1LSU zzzz
OK  brdc2620.26n.gz 69208
OK  p0412620.26d.gz 1956967
OK  1lsu2620.26d.gz 1284127
MISSING rinex/2026/262/zzzz/zzzz2620.26d.gz
```

## 4. 流量与礼貌

- S3 没有观察到限速（NODD 公开桶，匿名访问）。ListObjectsV2 每页最多 1000 个键；2026-268 一天有 1605 个站目录，267 有 1748 个，要翻页（脚本已处理）。
- corsdata 的日目录 HTML 很大，批量任务不要反复刮目录页；先读 `rinex/YYYY/DDD/YYYY.DDD.files.list`（2024-001 为 511599 B），或者直接列 S3。
- NCN API 和 UFCORS 都是单次请求约 1–2 s 的服务，不要并发轰炸；UFCORS 一次只能取一个站。

## 5. 接到哪一步

`.o.gz` → [georinex](./georinex.md) / [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) 算 TEC/ROTI；`.d.gz` → 先用 [hatanaka](./hatanaka.md) 或 [crx2rnx](./crx2rnx.md) 解压；质检 → 先看 `.S` 的 SUM 行，再用 [anubis](./anubis.md) / [gnss-qc](./gnss-qc.md)；坐标真值 → `coord_20` ITRF2020 + 速度。

## 6. 坑

1. **站名必须小写**：`rinex/2026/262/P041/p0412620.26d.gz` 返回 **404**，S3 键区分大小写。API 不区分大小写。
2. **S3 列表 XML 在 2026 年多了字段**：新对象在 `<ETag>` 和 `<Size>` 之间有 `<ChecksumAlgorithm>CRC64NVME</ChecksumAlgorithm><ChecksumType>`。按「Key…LastModified…ETag…Size 紧邻」写的正则对 2024 年的目录能用，对 2026 年的目录会**静默返回 0 个文件**，看上去像当天没数据。应该按 `<Contents>` 块逐个解析。
3. **日文件还没出 ≠ 没数据**：EarthScope 转入站（P041 等）日文件在日终后约 3–11 h 上桶（2026-262/267/268 实测）；NGS 自营站约 5 h。在这之前只能拿小时文件。P041 的小时文件缺最后一小时 `x`，所以数小时文件时，满天是 23 个而不是 24 个。
4. **corsdata 可能缺 .o.gz**：2024-001 的 P041 在 corsdata 上只有 `.24S` 和 `.24d.gz`，S3 上却多一个 `.24o.gz`（2024-02-03 补上）。以 S3 列表为准。
5. **API 坐标是 NAD 83(2011) @2010.0**（§3.7），不能当 ITRF 真值用。
6. **ncors 参数不合法时返回 HTML 500**：`x=0&y=0&z=0` 返回 Tomcat 500（`IllegalArgumentException: NaN`）；站名不存在时返回 `200 []`；缺 `id` 时返回 `200 {"error":"missing CORS ID value"}`。三种情况都要处理。
7. **UFCORS 出错也回 200**（§3.8）；默认只出 GPS。
8. **Rust `crx2rnx` 2.7.0 的输出和官方 `.o.gz` 字节不同**：同一个 `p0410010.24d` 解出 24737011 B（卫星按编号重排，空观测行补空格），官方 `.24o.gz` 解压后是 15397461 B。历元数都是 2880，但要做字节级比对时直接下 `.o.gz`。
9. 桶里有 `rinex//`（空段）和 `rinex/YYYY/hold_sum/` 这样的前缀，遍历年份时要过滤掉。`station_log/` 里还混着 `.1lsu.log.txt.swp` 之类的编辑器残留文件。

## 7. 相关

[gnss-obs-mirrors](./gnss-obs-mirrors.md)（IGS 站匿名镜像）· [gdds](./gdds.md)（GUI 里也拉 NOAA CORS）· [earthscope-sdk](./earthscope-sdk.md)（EarthScope 原始归档需 token）· [varion](./varion.md)（用 NGS MKEA 30 s 做 TEC 变化）· [data-access](../data-access.md)。
