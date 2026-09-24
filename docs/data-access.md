# GNSS 数据怎么下

配合 [`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md)。本页只答三件事：**要什么 → 去哪下 → 要不要注册**。

![STEC / VTEC 产品从观测来（本仓库自制）](./tutorials/images/fig-stec-vtec-shell.png)

想先看现象长什么样？→ [README 现象画廊](../README.md)

## 一屏决策

| 你想要 | 优先门户 | 注册 |
|---|---|:---:|
| 全球 RINEX / 广播星历 | [CDDIS](https://cddis.nasa.gov/archive/gnss/) · [BKG root_ftp](https://igs.bkg.bund.de/root_ftp/) · [GFZ ISDC HTTPS](https://isdc-data.gfz.de/gnss/) · [ESA GSSC](https://gssc.esa.int/) | Earthdata / 视中心 |
| SP3 / CLK / 偏差 | CDDIS `gnss/products/` · [IGS files](https://files.igs.org/pub/) · GFZ ISDC · [CODE HTTPS](https://www.aiub.unibe.ch/download/) · [CAS `pub/`](https://data.bdsmart.cn/pub/) | 同左 / 多开放 |
| GIM / IONEX | CDDIS `gnss/products/ionex/` · CODE · [CAS ionex](https://data.bdsmart.cn/pub/product/iono/ionex/) · [UPC rapid](https://chapman.upc.es/tomion/rapid/) · JPL | 视源（后两者常匿名） |
| 高采样率（闪烁 / 同震） | [CDDIS high-rate](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) · GFZ `/gnss/highrate/` · `cddis-highrate-downloader` | Earthdata / 开放 |
| 区域 CORS（美/新西兰/巴西） | [NOAA CORS](https://geodesy.noaa.gov/CORS/) · [CORS AWS](https://noaa-cors-pds.s3.amazonaws.com/index.html) · [GeoNet API](https://data.geonet.org.nz/) · [IBGE RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [EarthScope GAGE](https://gage-data.earthscope.org/archive/gnss) | 视网络 |
| 区域 CORS（欧/亚太/加） | [EPN `/pub/obs/`](https://epncb.oma.be/pub/obs/) · [GA](https://data.gnss.ga.gov.au/) · [CACS](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php) · [MIRAI](https://go.gnss.go.jp/mirai/miraiarchive/) · [韩国](https://www.gnssdata.or.kr/) · [BEV Geoportal](https://data.bev.gv.at/) | 开放 / 网页注册 |
| 欧洲站元数据 / 程序化 | [EPOS GNSS](https://gnss-epos.eu/) · [GLASS API](https://gnssdata-epos.oca.eu/GlassFramework/) · [M3G](https://gnss-metadata.eu/landing/m3g) | 视节点 |
| 实时 RTCM / SSR | BKG / IGS RTS（NTRIP；[igs-ip.net](https://www.igs-ip.net/) 偶发超时） | 账号或挂载点 |
| 掩星 RO | [CDAAC](https://cdaac-www.cosmic.ucar.edu/) · [ROM SAF](https://rom-saf.eumetsat.int/) · [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | 账号 / 开放 |
| 地磁 / 空间天气 | [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · [INTERMAGNET](https://intermagnet.org/) · [SuperMAG](https://supermag.jhuapl.edu/) · [GFZ Kp](https://kp.gfz.de/en/) · [SWPC](https://www.spaceweather.gov/) | 开放 / 注册 |
| 区域 TEC 现报 | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 开放（CC BY） |
| 闪烁 ISMR | [ISMR Query Tool](https://ismrquerytool.fct.unesp.br/) · [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader) | 网页注册 |
| 测高仪 | [GIRO / DIDBase](https://giro.uml.edu/didbase/) | 网页注册 |
| 对流层格网 | [VMF](https://vmf.geo.tuwien.ac.at/) → `trop_products/` | 多开放 |

逐站细节与注册字段 → [`10-gnss-datasets.md`](../lists/10-gnss-datasets.md)。

## 注册徽章（列表里怎么读）

| 字段 | 列表显示 | 含义 |
|---|---|---|
| `open` | 开放下载 | 可直接拉，无需个人账号 |
| `form_register` | 网页注册 | 自助开账号（如 Earthdata），一般即时 |
| `email_register` | 邮件申请 | 发邮件说明用途后开通 |
| `account_approval` | 账号审批 | 人工审核，可能数日 |
| `institution_only` | 机构限定 | 合作机构；个人多走镜像 / 公开子集 |
| `unknown` | 未确认 | 页可开，门槛未完全核验 |

`registration_zh` 是原创短提示，不是网站原文。**政策以当前下载页为准。**

## 共用：Earthdata / `.netrc`（CDDIS 菜谱复用）

无 Earthdata 授权时，`https://cddis.nasa.gov/archive/gnss/...` 常返回 **401**（正常，不是挂了）。匿名 FTP 已停，请走 **HTTPS**（或 `ftps://gdc.cddis.eosdis.nasa.gov/`）。

| 步 | 做什么 |
|---:|---|
| 1 | [Earthdata Login](https://urs.earthdata.nasa.gov/) 免费注册并验证邮箱 |
| 2 | 打开 [CDDIS GNSS 归档](https://cddis.nasa.gov/archive/gnss/)，登录；在 URS「Applications」授权 **CDDIS** / **NASA GES DISC** |
| 3 | 浏览器能列目录后，脚本用同一账号 + `.netrc`；限速、断点续传（`-C -` / `--continue`） |
| 4 | 路径对照：[GNSS holdings](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/GNSS_data_holdings.html) · [high-rate 说明](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) |

```bash
# ~/.netrc  （权限务必 600；勿提交仓库）
machine urs.earthdata.nasa.gov login YOUR_USER password YOUR_PASS
chmod 600 ~/.netrc
```

若下到的是 HTML 登录页而不是 `.gz`/`.rnx`：重走步骤 2，确认应用已授权。

---

## 用法菜谱（我要 X → 门户 → 怎么下 → 坑）

### 日采样 RINEX OBS/NAV（CDDIS）

**我要什么**：全球 IGS/MGEX 日文件观测（OBS）与广播星历（NAV），约 30 s。

**去哪**：[CDDIS archive/gnss](https://cddis.nasa.gov/archive/gnss/) · 持有说明见 [GNSS holdings](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/GNSS_data_holdings.html)。镜像： [BKG root_ftp](https://igs.bkg.bund.de/root_ftp/) · [GFZ ISDC `/gnss/data/daily/`](https://isdc-data.gfz.de/gnss/data/daily/)。

**怎么下**：

| 类型 | 路径模式 |
|---|---|
| OBS | `gnss/data/daily/YYYY/DDD/`（常 `.crx.gz` / `.rnx.gz`；子目录按类型） |
| NAV / brdc | 同日目录或 `brdc` 子树 |

```bash
# 先配好上文 .netrc；YYYY=年 DDD=年积日 STATION=站四字码（按当日实际文件名改）
curl -L -n -C - -o obs.crx.gz \
  "https://cddis.nasa.gov/archive/gnss/data/daily/2023/049/23d/XXXX0490.23d.Z"
# 无凭证时上述 URL 返回 401 → 属预期
```

**账号/配额坑**：Earthdata + URS 授权；匿名 401；下到 HTML 登录页 = 未授权应用；大批量须限速与断点续传；旧匿名 FTP 已死。

### SP3 / CLK / bias

**我要什么**：精密轨道（SP3）、钟差（CLK）、码偏差 / OSB（bias）。

**去哪**：CDDIS `gnss/products/WWWW/`（`WWWW` = GPS 周）· [IGS files/pub](https://files.igs.org/pub/) · [GFZ ISDC products](https://isdc-data.gfz.de/gnss/products/) · [CODE download](https://www.aiub.unibe.ch/download/)（跳转到 [S3 列表](https://code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php)）· [CAS pub](https://data.bdsmart.cn/pub/)。

**怎么下**：

```bash
# CDDIS：GPS 周目录（需 .netrc）；文件名约自 GPS 周 2238 起用长名
curl -L -n -C - -o igs.sp3.gz \
  "https://cddis.nasa.gov/archive/gnss/products/2250/IGS0OPSFIN_20230490000_01D_15M_ORB.SP3.gz"
# bias / DCB 常在 gnss/products/bias/ 等子树（以当日目录为准）

# 开放镜像示例（无需 Earthdata）
curl -L -C - -o code.sp3 \
  "https://www.aiub.unibe.ch/download/CODE/..."   # 在 S3 列表点选具体对象后替换
```

**账号/配额坑**：CDDIS 同 Earthdata；CODE/CAS/GFZ HTTPS 多开放；勿用已停的 CODE 旧 FTP；`files.igs.org` 大文件可能限速；长/短文件名混用时以目录列表为准。对照 [IGS Products](https://igs.org/products/) · [Data Access](https://igs.org/data-access/)。

### GIM / IONEX

**我要什么**：全球电离层图（VTEC 格网，IONEX）。

**去哪**：CDDIS `gnss/products/ionex/YYYY/DDD/` · CODE · [CAS ionex](https://data.bdsmart.cn/pub/product/iono/ionex/) · [UPC TOMION rapid](https://chapman.upc.es/tomion/rapid/)。

**怎么下**：

```bash
# CDDIS 正式 IGS 综合（需 .netrc；文件名按当日调整）
curl -L -n -C - -o igs.INX.gz \
  "https://cddis.nasa.gov/archive/gnss/products/ionex/2023/049/IGS0OPSFIN_20230490000_01D_02H_GIM.INX.gz"

# CAS 开放最终产品（示例：进目录后复制具体文件 URL）
curl -L -C - -O "https://data.bdsmart.cn/pub/product/iono/ionex/..."

# UPC 快速格网：按年目录匿名拉
curl -L -C - -O "https://chapman.upc.es/tomion/rapid/..."
```

读文件见 [ionex-gim](./software/ionex-gim.md) · 教程 [03](./tutorials/03-gim-ionex.md)。

**账号/配额坑**：CDDIS 401/HTML 登录页同前；CAS/UPC 常匿名；UPC 覆盖与时延不及正式库，大批量限速；事后分析优先 CDDIS/CAS 最终，近实时可试 CAS [`product/rts/iono/`](https://data.bdsmart.cn/pub/product/rts/iono/)。

### 高采样率 GNSS（闪烁 / 同震）

**我要什么**：1 Hz 或更高采样 RINEX（非日采样 30 s）。

**去哪**：[CDDIS high-rate 说明](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html)（实体在 archive）· GFZ [`/gnss/highrate/`](https://isdc-data.gfz.de/gnss/) · 工具 `cddis-highrate-downloader`。

**怎么下**：

```bash
# 路径概念：gnss/data/highrate/YYYY/DDD/…（子目录按小时/站；以 holdings 与说明页为准）
curl -L -n -C - -o hr.crx.gz \
  "https://cddis.nasa.gov/archive/gnss/data/highrate/2023/049/..."
# 批量优先专用脚本，避免手写全站嵌套目录
```

**账号/配额坑**：Earthdata；体量大 → 必限速/断点；先用说明页确认时段与站是否入库；GFZ highrate 匿名 HTTPS 可作备份。

### 区域 CORS：NOAA（美国）

**我要什么**：美国 CORS 事后 RINEX。

**去哪**：[NOAA CORS](https://geodesy.noaa.gov/CORS/) · 交互裁剪 [UFCORS](https://geodesy.noaa.gov/UFCORS/) · **大批量** [NODD S3 `noaa-cors-pds`](https://noaa-cors-pds.s3.amazonaws.com/index.html)。

**怎么下**：

```bash
# 对象键：rinex/YYYY/DDD/ssss/ssssDDD0.YYo.gz（站四字码小写）
curl -L -C - -o 1lsu0490.23o.gz \
  "https://noaa-cors-pds.s3.amazonaws.com/rinex/2023/049/1lsu/1lsu0490.23o.gz"
# 列前缀（可选）
aws s3 ls s3://noaa-cors-pds/rinex/2023/049/1lsu/ --no-sign-request
```

**账号/配额坑**：S3 公开、无需 NOAA 账号；目录 URL 本身常 404，必须落到具体对象键；网页 CORS/UFCORS 适合少站，批量勿爬门户 HTML。

### 区域 CORS：GeoNet（新西兰）

**我要什么**：新西兰站网日/小时 RINEX（含 1 Hz 树）。

**去哪**：[GeoNet 大地说明](https://www.geonet.org.nz/data/types/geodetic) · 目录 API [data.geonet.org.nz](https://data.geonet.org.nz/) · 日文件 [`/v1/data/gnss/rinex/`](https://data.geonet.org.nz/v1/data/gnss/rinex/) · 1 Hz [`rinex1Hz`](https://data.geonet.org.nz/v1/data/gnss/rinex1Hz/) · 批量亦见 [AWS Open Data](https://www.geonet.org.nz/data/access/aws)。

**怎么下**：

```bash
# 列某日目录（GET；链接常指向 geonet-open-data S3）
curl -L -C - -O \
  "https://data.geonet.org.nz/v1/data/gnss/rinex/2023/049/200400NZL_R_20230490000_01D_30S_MO.rnx.gz"
# 或先打开目录页复制具体文件 URL：
# https://data.geonet.org.nz/v1/data/gnss/rinex/2023/049/
```

**账号/配额坑**：开放，读 Data Policy；**根路径对 HEAD 常 405，用 GET**；RINEX 2 已弃用，优先 RINEX 3；旧兼容端点计划 2026 年底退役。

### 区域 CORS：EPN（欧洲）+ IBGE（巴西备选）

**我要什么**：欧洲 EPN 事后观测；或巴西 RBMC。

**去哪**：

- EPN：[中央局](https://epncb.oma.be/) · 观测 [`/pub/obs/`](https://epncb.oma.be/pub/obs/)（按站；旧 `/ftp/obs/` 会跳转）
- IBGE：[geoftp RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [API 文档](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1)

**怎么下**：

```bash
# EPN：进 /pub/obs/<STATION>/ 复制日文件 URL 后
curl -L -C - -O "https://epncb.oma.be/pub/obs/...."

# IBGE：geoftp 目录树，或按 API 文档的 rinex2/rinex3/1s 端点（用 GET）
curl -L -C - -O \
  "https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/...."
```

**账号/配额坑**：EPN 事后多开放，批量前对照中央局站状态；IBGE API 文档页对 HEAD 可能 405，用 GET；礼貌限速；NTRIP 实时另见 EUREF-IP，勿与事后 `/pub/obs/` 混用。

### 实时 NTRIP（BKG / IGS RTS）

**我要什么**：实时 RTCM 观测流或 SSR 改正（IGS RTS）。

**去哪**：NTRIP 源表与账号入口优先 [igs-ip.net](https://www.igs-ip.net/)（本环境探测偶发超时）· BKG / IGS RTS 挂载点 · 归档侧 [BKG root_ftp](https://igs.bkg.bund.de/root_ftp/) 不是实时流。客户端可用 BKG NtripClient、[`pygnssutils`](./software/pygnssutils.md) 等。

**怎么下**：

```bash
# 1) 在 caster 网页或源表取得：host、port、mountpoint、user、password
# 2) 示例（占位符须换成你的挂载点；勿把密码写进仓库）
# ntripclient / BKG 工具：
#   ntripclient -h <caster> -p <port> -m <MOUNT> -u USER -c PASS -D out.rtcm
# pygnssutils 等：按软件短文配置 NTRIP 源后写盘或转发
```

**账号/配额坑**：多数挂载点要账号或机构权限；`igs-ip.net` 偶发超时 → 换时段或 BKG 备用 caster；裸打开 `igs.bkg.bund.de/` 常 404，归档用 `root_ftp`；实时流 ≠ 事后 RINEX 归档。

### 掩星 RO（CDAAC / AWS）

**我要什么**：掩星 excess phase / 电子密度剖面等 Level-1b/2。

**去哪**：[CDAAC](https://cdaac-www.cosmic.ucar.edu/)（ionPhs / ionPrf 等）· [ROM SAF](https://rom-saf.eumetsat.int/) · 开放桶工具 [awsgnssroutils](https://github.com/gnss-ro/aws-opendata)。

**怎么下**：

```bash
# AWS 公开数据（推荐脚本化；勿依赖 registry.opendata.aws/gnss* 深链，常 404）
pip install awsgnssroutils
# 按仓库 README：查询任务/中心 → 下载 Level-1b/2

# CDAAC：浏览器登录后选任务与产品类型再下（账号制）
```

**账号/配额坑**：CDAAC / 多数 ROM SAF 要注册；AWS 路径开放但 API 以工具为准；处理包 ROPP 与产品页分开找。

### 地磁 / 空间天气（Kp / SWPC）

**我要什么**：地磁 Kp（或相关指数）与空间天气产品，给 GNSS/电离层事件对齐。

**去哪**：[GFZ Kp](https://kp.gfz.de/en/) · [SWPC](https://www.spaceweather.gov/) · 备份指数 [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/)。

**怎么下**：

```bash
# GFZ Kp JSON（开放；分清确定值 / 预报）
curl -s "https://kp.gfz.de/app/json/?start=2023-02-18T00:00:00Z&end=2023-02-19T00:00:00Z&index=Kp"
# SWPC：https://www.spaceweather.gov/ → Products（K 指数、GloTEC 等）点选下载或 JSON
```

**账号/配额坑**：多开放；`kp.gfz-potsdam.de` 会跳到 `kp.gfz.de`；`swpc.noaa.gov` 多跳到 `spaceweather.gov`，`spaceweather.noaa.gov` 仍不可靠；勿把 GFZ Kp 与 SWPC K 指数混用不标注；批量礼貌访问。

### 开放产品镜像快径（CODE / GFZ / CAS）

**我要什么**：少账号摩擦的 SP3/CLK/IONEX/日文件备份。

**去哪**：

| 源 | 入口 | 典型内容 |
|---|---|---|
| CODE | [aiub download](https://www.aiub.unibe.ch/download/) → [S3 列表](https://code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php) | `CODE/`、`ionex/`、`CODE_MGEX/` |
| GFZ ISDC | [isdc-data.gfz.de/gnss/](https://isdc-data.gfz.de/gnss/) | `/data/daily/`、`/highrate/`、产品树 |
| CAS BDsmart | [pub 根](https://data.bdsmart.cn/pub/) | [ionex](https://data.bdsmart.cn/pub/product/iono/ionex/) · [rts/iono](https://data.bdsmart.cn/pub/product/rts/iono/) · bias/SSR |

**怎么下**：浏览器打开上表目录 → 复制对象 URL → `curl -L -C - -O "<url>"`（均无需 Earthdata）。

**账号/配额坑**：CODE 旧 FTP 已停；GFZ 旧 FTP 已迁 HTTPS；CAS RTS 仅近实时试验；门户说明 [isdc.gfz.de](https://isdc.gfz.de/)（`gfz-potsdam.de` 会跳转）。

---

## 其他门户快查（未展开菜谱）

| 门户 | 入口 | 路径或下一步 | 注册 | 注意 |
|---|---|---|---|---|
| **BKG IGS** | [root_ftp](https://igs.bkg.bund.de/root_ftp/) | 归档目录树；裸域名常 404 | 归档多开放；NTRIP 视挂载点 | 实时见上节 NTRIP |
| **ESA GSSC** | [gssc.esa.int](https://gssc.esa.int/) | 门户检索 → 数据集页 | 门户账号；部分集合另申请 | 勿假设全站开放 |
| **EarthScope** | [GAGE archive](https://gage-data.earthscope.org/archive/gnss) · [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk) | SDK（PyPI）拉 API | EarthScope / GAGE | 原 UNAVCO 页仍可开，新工作以 GAGE + SDK 为准 |
| **GA GNSS** | [data.gnss.ga.gov.au](https://data.gnss.ga.gov.au/) | 门户 / 官方 API | 多开放；个别 API 视密钥 | 勿用旧 ga.gov.au 深链 |
| **NRCan CACS** | [CACS 选站页](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php) | 网页选站 → 打包 | 多开放 | 旧 `webapp.csrs.nrcan.gc.ca` 会跳转 |
| **Japan MIRAI** | [miraiarchive](https://go.gnss.go.jp/mirai/miraiarchive/) | 年积日 RINEX 3/4；页内有 wget/curl 例 | GO!GNSS 注册 + HTTPS 基本认证 | 含 QZSS；相对传统 GEONET 更易脚本化 |
| **Korea GNSS** | [gnssdata.or.kr](https://www.gnssdata.or.kr/) | 登录 → 选站/时段 → ZIP | 网页注册 | 单次跨度常有上限 |
| **BEV APOS** | [产品说明](https://www.bev.gv.at/en/Services/Products/Austrian-POsitioning-Service.html) · [Geoportal](https://data.bev.gv.at/) | STAC：`/download/RINEX/RDH1/30S/stac/by_date/catalog.json` | APOS-PP 免费（CC BY 4.0） | 德语深链 `…/APOS.html` 常 403 |
| **Spain ERGNSS** | [datos-geodesia ERGNSS](https://datos-geodesia.ign.es/ERGNSS/) | HTTPS 公开目录树 | 开放 | 限速 |
| **RENAG** | [renag.resif.fr](https://renag.resif.fr/) | 站网/政策/产品（DOI `10.15778/resif.rg`） | 视 RESIF | 先读数据政策 |
| **SWEPOS** | [RINEX DOI 页](https://www.lantmateriet.se/en/geodata/gps-geodesy-and-swepos/lantmateriets-doi-objects/swepos-rinex-data/) | FTP/SFTP 日文件（DOI `10.23701/c5tc-ew52`，CC0） | 按站方说明 | 实时权限另见条款 |
| **HK SatRef** | [RINEX 说明](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 按页取事后 RINEX | 多开放 | 注意采样率与保留期 |
| **EPOS / GLASS / M3G** | [EPOS GNSS](https://gnss-epos.eu/) · [GLASS](https://gnssdata-epos.oca.eu/GlassFramework/) · [M3G](https://gnss-metadata.eu/landing/m3g) | GLASS JSON；M3G REST | 视节点 | 欧洲程序化优先 GLASS |
| **VMF** | [vmf.geo.tuwien.ac.at](https://vmf.geo.tuwien.ac.at/) | [`trop_products/`](https://vmf.geo.tuwien.ac.at/trop_products/) | 多开放 | 选对 VMF1/VMF3 |
| **GIRO / DIDBase** | [giro.uml.edu/didbase](https://giro.uml.edu/didbase/) | 查询站/时段 → 图 | 网页注册 | 旧 quick-request URL 已 404 |
| **INTERMAGNET** | [intermagnet.org](https://intermagnet.org/) | Data → 准实时/存档 | 视产品 | 先读条件再脚本 |
| **SuperMAG** | [supermag.jhuapl.edu](https://supermag.jhuapl.edu/) | 界面 / API | 网页注册 | 引用含原始台站 |
| **eSWua / IONORING** | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | Download Tool / REST；近实时地图 | 开放（CC BY；DOI `10.13127/eswua/tec`） | 区域 TEC，非 GNSS 原始归档 |
| **ISMR** | [Query Tool](https://ismrquerytool.fct.unesp.br/) · [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader) | 网页或脚本 | 网页注册 | 站点偶发超时/证书问题 |
| **CSNO TARC** | [csno-tarc.cn](https://www.csno-tarc.cn/) · [差分英文页](https://www.csno-tarc.cn/en/data/differential) | 测试评估 / 差分 | 浏览多开放 | 与 IGS OSB 基准可能不同 |
| **SOPAC**（可选镜像） | [sopac-csrc.ucsd.edu](https://sopac-csrc.ucsd.edu/) · [garner `/pub/`](https://garner.ucsd.edu/pub/) | 历史 IGS DC / 产品树 | 多开放 | **探测常超时**；关键周与 CDDIS/BKG/GFZ 交叉校验 |

## 相关教程与软件

下完数据后常接：

| 目标 | 去哪 |
|---|---|
| 双频 STEC / 一日练习 | [02](./tutorials/02-gnss-dualfreq-tec.md) · [16](./tutorials/16-practice-one-day-tec.md) |
| 读 GIM / IONEX | [03](./tutorials/03-gim-ionex.md) · [ionex-gim](./software/ionex-gim.md) |
| 目录怎么用 | [08](./tutorials/08-how-to-use-this-catalog.md) |
| RINEX 读盘 / QC | [georinex](./software/georinex.md) · [anubis](./software/anubis.md) |
| 软件短文总索引 | [software/README](./software/README.md) · [tutorials/README](./tutorials/README.md) |
