# EPOS GLASS API（欧洲 GNSS 台站元数据 + RINEX 文件检索）· 下载侧 操作手册

入口：[GLASS Framework（OCA 节点）](https://gnssdata-epos.oca.eu/GlassFramework/) · 接口说明 [`webresources/application.wadl`](https://gnssdata-epos.oca.eu/GlassFramework/webresources/application.wadl) · 目录条目 `EPOS-GLASS-API`（portal-terms，official）。
本机验证 **2026-09-26 05:29–05:40 EDT**，只用 curl、系统 Python 3 标准库和 `crx2rnx`（rinex-cli 系 Rust 版），不需要账号。样例站 **GRAS00FRA**（Calern，EPN/IGS/RGP）和 **SOPH00FRA**（Sophia Antipolis，RENAG）。

> 岗位：**先在欧洲 EPN/RENAG/RGP 等网里查“哪些站、哪天有文件、文件在哪”**，拿到带 md5 的下载 URL，再去原数据中心下载。  
> 本文**不讲** IGS 全球镜像（见 [gnss-obs-mirrors](./gnss-obs-mirrors.md)）、美国 CORS（见 [noaa-ncn-data](./noaa-ncn-data.md)）、GUI 下载器（见 [gdds](./gdds.md)）。GLASS **不存文件**，只做检索。

## 1. 节点事实（实测）

| 项 | 值 |
| --- | --- |
| 版本 | `tools/version` → `GlassFramework-3.4.1.255`；`tools/build` → nodetype `Glass Data Node`，库名 `gnss-europe`，build_date `2026-07-02T15:32:52+0000` |
| 服务器 | Payara Server 6.2025.4（出错时回 Payara 的 HTML 错误页，不是 JSON） |
| 接口说明 | 只有 Jersey 自动生成的 WADL（55696 B）；`/swagger/`、`webresources/openapi.json`、`swagger.json` 都是 404 |
| 规模 | `stations/v2/list/station?format=json` 列出 **2462** 站（210 KB，4.2 s） |
| 账号/限速 | 免账号、免 key；本次约 40 次请求没遇到限速或 429 |
| 单次延迟 | 元数据请求约 0.9–1.2 s；网络级列表（294 站）3.6 s |

## 2. 安装

```bash
# 只要 curl + python3；解 .crx.gz 再装 Hatanaka 解压器（见 hatanaka.md / crx2rnx.md）
curl --version | head -1; python3 -V
B=https://gnssdata-epos.oca.eu/GlassFramework/webresources
```

## 3. 逐步命令 + 实测输出

### 3.1 查一个站（4 字符或 9 字符站名都行）

```bash
curl -s "$B/stations/v2/marker/GRAS/short/json" | python3 -c \
 'import json,sys;s=json.load(sys.stdin)[0];c=s["location"]["coordinates"];print(s["marker"],s["name"],s["network"]["name"],s["date_from"],c["lat"],c["lon"],c["altitude"],c["x"],c["y"],c["z"])'
# GRAS00FRA Observatoire de Calern - OCA EPN & IGS & RGP 1995-02-10 00:00:00 43.7547 6.9206 1319.31 4581690.8363 556114.933 4389360.8603
```

- 路径格式 `stations/v2/<维度>/<值>/<short|full>/<json|csv|xml>`；维度有 `marker`、`name`、`network`、`agency`、`country`、`city`、`receiver`、`antenna`、`radome` 等。
- `short/csv` 首行：`name, marker, marker_long_name, date_from, date_to, x, y, z, lat, lon, altitude, city, state, country, agencies ,networks`（逗号后带空格）。
- `full/json` 多出 `local_ties`、`monument` 以及 **`rinex_files_dates`**。后者是该站每个有文件的日期拼成的一个长字符串，GRAS 从 1996 年起，响应很大，只在需要时取。
- 未知站：`200 []`，不是 404。

### 3.2 按区域 / 网络找站

```bash
curl -s "$B/stations/v2/station/bbox/6.5/43.5/7.5/44.0?format=json" | python3 -c \
 'import json,sys;print([s["marker"] for s in json.load(sys.stdin)])'
# ['NICE00FRA', 'SOPH00FRA', 'GRAC00FRA', 'EZEV00FRA', 'FAYE00FRA', 'GRAS00FRA']
curl -s "$B/stations/v2/network/RGP/short/json" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))'
# 294
```

- bbox 参数顺序是 **minLon/minLat/maxLon/maxLat**。`combination/short/json?minLat=43.5&maxLat=44&minLon=6.5&maxLon=7.5` 返回同样 6 站。
- `combination`：`network=RENAG` 109 站，`country=France` 324 站。
- 站名清单：`stations/v2/list/station?format=json` 只有 `marker`（4 字符）、`name`、`date_to`、`marker_long_name` 四个字段，最轻。

### 3.3 按站 + 日期查 RINEX 文件（主力）

```bash
curl -s "$B/files/station-marker/GRAS00FRA/json?epoch_start=2026-09-20&epoch_end=2026-09-21" | python3 -c '
import json,sys
for f in json.load(sys.stdin):
    print(f["reference_date"],f["name"],f["file_size"],f["md5_checksum"],f["data_center"]["acronym"]); print("  ",f["url"])'
# 2026-09-20 00:00:00 GRAS00FRA_R_20262630000_01D_30S_MO.crx.gz 2596725 04422924ecd26903ee000a5424236643 EPN HDC
#    https://epncb.oma.be/pub/RINEX/2026/263/GRAS00FRA_R_20262630000_01D_30S_MO.crx.gz
# 2026-09-21 00:00:00 GRAS00FRA_R_20262640000_01D_30S_MO.crx.gz 2621387 c95f6d1fc82b67b87299d65df2d3ace6 EPN HDC
#    https://epncb.oma.be/pub/RINEX/2026/264/GRAS00FRA_R_20262640000_01D_30S_MO.crx.gz
```

- `epoch_start`/`epoch_end` 是**闭区间的日**：`2026-09-20..2026-09-20` 返回 1 个文件，`..09-21` 返回 2 个。
- 每条文件记录的字段：`name`、`url`、`file_size`、`md5_checksum`（压缩包）、`md5_uncompressed`、`file_type{format,sampling_window,sampling_frequency}`、`reference_date`、`published_date`、`creation_date`、`revision_date`、`relative_path`、`status`、`data_center{acronym,hostname,protocol,data_center_structure}`。
- 把 `json` 换成 `csv` 可得一行一文件的表，最后一列是 `url`。
- 不带日期时从最早的文件开始：`?page=1&perpage=3` 返回 `GRAS0010.96D.Z`（1996-01-01）等 RINEX 2 老文件。
- 同一接口对 RENAG 站返回 RENAG 自己的地址：SOPH00FRA 2026-09-20 → `https://renag.resif.fr/pub/rinex3/2026/263/SOPH00FRA_R_20262630000_01D_30S_MO.crx.gz`（1705454 B）。

### 3.4 下载 + 校验 + 解压

```bash
U=https://renag.resif.fr/pub/rinex3/2026/263/SOPH00FRA_R_20262630000_01D_30S_MO.crx.gz
curl -sS -o SOPH.crx.gz "$U" && md5sum SOPH.crx.gz
# c4a29edae6c1fbc21f8634d2dc2c8e51  SOPH.crx.gz        ← 与 GLASS 的 md5_checksum 一致
zcat SOPH.crx.gz > s.crx && crx2rnx -q -o s.rnx s.crx && grep -c '^> ' s.rnx
# 2880                                                  ← 30 s 全天；解压后 15428334 B
```

- RENAG 这一个 1.7 MB 文件本机下了 36.9 s（约 46 KB/s），批量下载要留时间。EPN 的 GRAS 文件 `curl -I` 返回 200，`Content-Length: 2596725`，与 GLASS 记录一致。
- SOPH 文件头：RINEX 3.05 Mixed，G 16 / R 16 / E 12 个观测类型，注释行 `DOI: 10.15778/resif.rg`、`CC-BY-4.00 DATA Licence`。

### 3.5 其他用得上的接口

| 调用 | 实测 |
| --- | --- |
| `files/name/<文件名>/json` | 按文件名查回同一条记录（含 md5、url） |
| `files/info?marker_long_name=GRAS00FRA&date_from=2026-09-20&date_to=2026-09-21` | 2 条，字段 `file_name`、`file_status`、`errors`、`acronym`、`reference_date`，可看文件校验状态 |
| `files/combination/marker=GRAS00FRA&reference_date=2026-09-10/json` | `reference_date` 是**起始日**：返回 09-10 起的 13 个文件（到 09-22） |
| `log/GRAS00FRA` | IGS 站点日志 v2.0 纯文本，23192 B（Content-Type 是 octet-stream） |
| `log/geodesyml/GRAS00FRA` | **zip**（5115 B），内含 `GRAS00FRA.xml`（49883 B），要先 `unzip` |
| `files/highrate/station-marker/GRAS00FRA/json?...` | GRAS 返回 `[]`；按发布日查 2026-09-25 的高频文件也是 `[]`，本节点这次没查到高频文件 |

## 4. 坑（全部实测）

1. **`files/combination` 里的 `date_from`/`date_to` 被忽略**：`marker=GRAS00FRA&date_from=2026-09-20&date_to=2026-09-20` 会从 1996 年起吐全部历史，80 s 超时时已收到 3.1 MB 还没完。按日期查请用 §3.3 的 `epoch_start`/`epoch_end`，或者给 `reference_date`。**所有请求都加 `-m`**。
2. **`perpage`、`limit` 对台站接口无效**：`combination?network=RENAG&perpage=5` 仍返回 109 站；bbox `limit=2` 仍返回 6 站。`files/station-marker` 的 `page/perpage` 是生效的。
3. **全站 dump 不可用**：`stations/v2/station/short/json` 返回 `[]`，同时 `tools/cacheStatus` 显示 `Size: 0  Initializing:  Reading the Cache File`。要全表就用 `list/station`（2462 站）或按 network/country 分批。
4. **`satelliteSystem` 过滤不可信**：`combination?network=RENAG&satelliteSystem=GALILEO` 返回 `[]`，但 RENAG 的 SOPH 文件里明明有 Galileo 观测。
5. **`files/rinex_count/<站>` 始终 400**：不带参数、带 `Date_From/Date_To`、再加 `date_type/file_type` 都是 Payara 的 400 HTML。参数格式没有文档，放弃这个接口，改用 §3.3 数条数。
6. **不要调 `stations-json-dictionary/*`**：GET 这个接口会返回 `Success on updating cache!`，也就是触发了服务器缓存重建。WADL 里还有 `t0-manager/*`（addNode、deleteDataCenter…），这是节点管理接口，不要碰。
7. **network 字段是拼接的字符串**，例如 `"EPN & IGS & RGP"`；要逐网判断请用 `network_array`。`agency.name` 里可能带 `\n\n`。
8. **时延**：2026-09-26 05:30 EDT 时，GRAS 最新的一个文件是 2026-09-22（DOY 265），`creation_date 2026-09-25 04:14:13`；DOY 263 的 `published_date` 是 09-23 07:19:49。也就是从观测日到能查到大约 2–3 天。服务器时间字段没有标时区。
9. WADL 里的 `base` 写的是 `http://`，脚本一律用 `https://`。

## 5. 故障排查

| 现象 | 原因 / 处理 |
| --- | --- |
| 返回一页 Payara HTML、状态 400/404 | 路径或参数不对（例如 `size` 不是 `short/full`、`format` 不是 `json/csv/xml`）。对照 WADL 检查 |
| `200 []` | 站名不存在，或日期窗里没有文件。先用 `stations/v2/marker/<4字符>` 确认站名全称 |
| 请求挂很久 | 多半某个过滤参数被忽略了（坑 1），立刻 Ctrl-C，改用 `epoch_*` |
| md5 对不上 | 数据中心可能已重新发布文件（看 `revision_date`），重新查一次 GLASS |

## 6. 与其他手册的分工

- 拿到 `.crx.gz` 之后的解压和质检：[hatanaka](./hatanaka.md) / [crx2rnx](./crx2rnx.md) / [gnss-qc](./gnss-qc.md) / [anubis](./anubis.md)。
- 同样是 EPN 站，但走 IGS 全球镜像：[gnss-obs-mirrors](./gnss-obs-mirrors.md)。
- 改写 RINEX 头：[rinexmod](./rinexmod.md)。
