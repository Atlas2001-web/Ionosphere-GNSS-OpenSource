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
| 高采样率（闪烁 / 同震） | [CDDIS high-rate](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) · GFZ `/gnss/data/highrate/` · `cddis-highrate-downloader` | Earthdata / 开放 |
| 区域 CORS（美/新西兰/巴西） | [NOAA CORS](https://geodesy.noaa.gov/CORS/) · [CORS AWS](https://noaa-cors-pds.s3.amazonaws.com/index.html) · [GeoNet API](https://data.geonet.org.nz/) · [IBGE RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [EarthScope GAGE](https://gage-data.earthscope.org/archive/gnss) | 视网络 |
| 区域 CORS（欧/亚太/加） | [EPN `/pub/obs/`](https://epncb.oma.be/pub/obs/) · [GA](https://data.gnss.ga.gov.au/) · [CACS](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php) · [MIRAI](https://go.gnss.go.jp/mirai/miraiarchive/) · [韩国](https://www.gnssdata.or.kr/) · [BEV Geoportal](https://data.bev.gv.at/) | 开放 / 网页注册 |
| 欧洲站元数据 / 程序化 | [EPOS GNSS](https://gnss-epos.eu/) · [GLASS API](https://gnssdata-epos.oca.eu/GlassFramework/) · [M3G](https://gnss-metadata.eu/landing/m3g) | 视节点 |
| 实时 RTCM / SSR | `products.igs-ip.net:2101` · [igs-ip.net](https://www.igs-ip.net/)（NTRIP；后者偶发超时） · [注册](https://register.rtcm-ntrip.org/cgi-bin/registration.cgi) | 挂载点账号 |
| 掩星 RO | [CDAAC](https://cdaac-www.cosmic.ucar.edu/) · [data.cosmic](https://data.cosmic.ucar.edu/gnss-ro/) · [ROM SAF](https://rom-saf.eumetsat.int/) · [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | 开放 / 视源 |
| 地磁 / 空间天气 | [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · [INTERMAGNET](https://intermagnet.org/) · [SuperMAG](https://supermag.jhuapl.edu/) · [GFZ Kp](https://kp.gfz.de/en/) · [SWPC](https://www.spaceweather.gov/) | 开放 / 注册 |
| 区域 TEC 现报 | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 开放（CC BY） |
| 闪烁 ISMR | [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader)（主）· [Query Tool](https://ismrquerytool.fct.unesp.br/)（辅，常超时） | 网页注册 |
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

**浏览器 cookie ≠ 脚本凭证**：网页登录只服务浏览器；`curl`/`wget`/批量脚本须用同一 Earthdata 账号写进 `~/.netrc`（或工具支持的 token），不能指望 cookie 自动带上。

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

# CODE 开放镜像（无需 Earthdata；须带年份子目录）
curl -L -C - -o COD0OPSFIN_20230490000_01D_05M_ORB.SP3.gz \
  "https://www.aiub.unibe.ch/download/CODE/2023/COD0OPSFIN_20230490000_01D_05M_ORB.SP3.gz"
# 目录：https://code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php?path=CODE/2023
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

# CAS 开放最终产品（年/年积日；长名 IONEX）
curl -L -C - -O \
  "https://data.bdsmart.cn/pub/product/iono/ionex/2023/049/CAS0OPSFIN_20230490000_01D_30M_GIM.INX.gz"

# UPC 快速格网：按年目录匿名拉
curl -L -C - -O "https://chapman.upc.es/tomion/rapid/..."
```

读文件见 [ionex-gim](./software/ionex-gim.md) · 教程 [03](./tutorials/03-gim-ionex.md)。

**账号/配额坑**：CDDIS 401/HTML 登录页同前；CAS/UPC 常匿名；UPC 覆盖与时延不及正式库，大批量限速；事后分析优先 CDDIS/CAS 最终，近实时可试 CAS [`product/rts/iono/`](https://data.bdsmart.cn/pub/product/rts/iono/)。

### 高采样率 GNSS（闪烁 / 同震）

**我要什么**：1 Hz 或更高采样 RINEX（非日采样 30 s）。

**去哪**：[CDDIS high-rate 说明](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html)（实体在 archive）· GFZ [`/gnss/data/highrate/`](https://isdc-data.gfz.de/gnss/data/highrate/) · 工具 `cddis-highrate-downloader`。

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

- EPN：[中央局](https://epncb.oma.be/) · 观测 [`/pub/obs/`](https://epncb.oma.be/pub/obs/)（现为 `YYYY/DDD/`，会落到 `/pub/RINEX/`；旧 `/ftp/obs/` 会跳转）
- IBGE：[geoftp RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [API 文档](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1)

**怎么下**：

```bash
# EPN：路径 /pub/obs/YYYY/DDD/ → 实际落到 /pub/RINEX/YYYY/DDD/（站长名 RINEX 3）
curl -L -C - -O \
  "https://epncb.oma.be/pub/obs/2023/049/ACOR00ESP_R_20230490000_01D_30S_MO.crx.gz"

# IBGE geoftp：dados_RINEX3/YYYY/DDD/<站长名>...
curl -L -C - -O \
  "https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/2023/049/ALMA00BRA_R_20230490000_01D_15S_MO.crx.gz"

# IBGE API（HEAD 常 405，用 GET；站四字码小写 + 年 + 年积日）
curl -L -C - -o alma_2022_001.crx.gz \
  "https://servicodados.ibge.gov.br/api/v1/rbmc/dados/rinex3/alma/2022/1"
```

**账号/配额坑**：EPN 事后多开放，批量前对照中央局站状态；旧按站目录 `/pub/obs/<STATION>/` 已不存在（404）；IBGE API 文档/接口对 HEAD 可能 405，用 GET；礼貌限速；NTRIP 实时另见 EUREF-IP，勿与事后 `/pub/obs/` 混用。

### 实时 NTRIP（BKG / IGS RTS）

**我要什么**：实时 RTCM 观测流或 SSR 改正（IGS RTS）。

**去哪**：

| 角色 | caster（文档/实测） | 端口 | 说明 |
|---|---|---|---|
| IGS RTS **产品**（SSR） | `products.igs-ip.net` | **2101**（亦常见 **443** TLS） | 挂载点例：`SSRA02IGS0`、`BCEP00BKG0` |
| IGS **观测** | `igs-ip.net` / `www.igs-ip.net` | 2101 / 443 | **偶发超时**；换时段或区域 relay |
| EUREF 区域 | `euref-ip.net` | 2101 / 443 | 欧洲站网实时；≠ 事后 EPN `/pub/obs/` |

注册：[BKG 表单](https://register.rtcm-ntrip.org/cgi-bin/registration.cgi) · 总览 [IGS RTS User Access](https://igs.org/rts/user-access/)（含 CDDIS/CAS/GA/UCAR 等区域 caster）。归档 [BKG root_ftp](https://igs.bkg.bund.de/root_ftp/) **不是**实时流。客户端 → [`bnc`](./software/bnc.md) · [`pygnssutils`](./software/pygnssutils.md) · [`rtklib`](./software/rtklib.md)（勿在本页重写操作）。

**怎么下**：

```bash
# 0) 拉源表（无需账号；确认 caster 可达）
curl -s --max-time 15 "http://products.igs-ip.net:2101/" | head
# 期望：以 CAS; / NET; / STR; 开头的 NTRIP 源表行；HTTPS 根路径对普通浏览器常 501

# 1) 注册后取得 user/password；在源表选挂载点（例 SSRA02IGS0）
# 2) 客户端（口令用环境变量；勿写进仓库）
# BNC GUI：Host=products.igs-ip.net  Port=2101  Mountpoint=SSRA02IGS0  → 见 docs/software/bnc.md
# pygnssutils：
#   gnssntripclient --server products.igs-ip.net --port 2101 --https 0 \
#     --mountpoint SSRA02IGS0 --ntripuser "$NTRIP_USER" --ntrippassword "$NTRIP_PASS" \
#     --datatype RTCM --ntripversion 2.0
# RTKLIB str2str / RTKNAVI：ntrip://USER:PASS@products.igs-ip.net:2101/SSRA02IGS0
```

**账号/配额坑**：无账号订受保护挂载点 → 401/403；`igs-ip.net` 超时 → 换 `products.igs-ip.net`（只做产品）或 [RTS User Access](https://igs.org/rts/user-access/) 列出的区域 relay；源表空/连不上 = 网络或 caster 维护，不是挂载点名写错的唯一解释；裸开 `igs.bkg.bund.de/` 常 404，归档用 `root_ftp`；实时流 ≠ 事后 RINEX。

### 掩星 RO（CDAAC / AWS）

**我要什么**：掩星 excess phase / 电子密度剖面等 Level-1b/2。

**去哪**：[CDAAC 门户](https://cdaac-www.cosmic.ucar.edu/) · **直链树** [data.cosmic.ucar.edu/gnss-ro](https://data.cosmic.ucar.edu/gnss-ro/)（COSMIC-1/2 等，**无需登录**）· [ROM SAF](https://rom-saf.eumetsat.int/) · AWS 工具 [awsgnssroutils](https://github.com/gnss-ro/aws-opendata)（PyPI 同名）。

**怎么下**：

```bash
# A) CDAAC 公开目录（例：COSMIC-1 事后 Level-1b ionPhs 日包）
curl -L -C - -O \
  "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/postProc/level1b/2019/049/ionPhs_postProc_2019_049.tar.gz"
# 路径模式：…/<mission>/{postProc|nrt}/level1b|level2/YYYY/DDD/<product>_….tar.gz

# B) AWS Registry（推荐批量；勿依赖 registry.opendata.aws/gnss* 深链，常 404）
pip install awsgnssroutils
python - <<'PY'
from awsgnssroutils.database import RODatabaseClient, setdefaults
setdefaults(metadata_root="./ro_meta", data_root="./ro_out", version="v1.1")
rodb = RODatabaseClient()
occs = rodb.query(missions="cosmic2", datetimerange=("2021-02-18","2021-02-19"))
# 类型仅 {ucar|jpl|romsaf}_{calibratedPhase|refractivityRetrieval|atmosphericRetrieval}
occs.download("ucar_calibratedPhase", data_root="./ro_out", keep_aws_structure=False)
PY
```

**账号/配额坑**：`data.cosmic` 匿名开放（ionPhs/ionPrf 等）；旧「必须 CDAAC 网页账号」已过时；ROM SAF 多数仍要注册；AWS 工具**没有** `ionPhs` 文件名——电离层 excess phase 用 CDAAC 直链，AWS 侧重 `calibratedPhase` 等三型；勿把 registry 深链写进脚本；处理包 ROPP 与产品页分开找。

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

**我要什么**：少账号摩擦的 SP3/CLK/IONEX/日文件备份（免 Earthdata）。

**去哪**：

| 源 | 列表入口 | 文件名模式（例，2023-049） |
|---|---|---|
| CODE | [S3 列表 `CODE/2023`](https://code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php?path=CODE/2023) | `CODE/YYYY/COD0OPSFIN_<YYYYDDD>0000_01D_05M_ORB.SP3.gz` |
| GFZ ISDC | [data/daily](https://isdc-data.gfz.de/gnss/data/daily/) · [products/final](https://isdc-data.gfz.de/gnss/products/final/) | `…/YYYY/DDD/<站>_…MO.crx.gz`；`…/final/wWWWW/GFZ0OPSFIN_…ORB.SP3.gz` |
| CAS BDsmart | [ionex](https://data.bdsmart.cn/pub/product/iono/ionex/) · [rts/iono](https://data.bdsmart.cn/pub/product/rts/iono/) | `…/ionex/YYYY/DDD/CAS0OPSFIN_<YYYYDDD>0000_01D_30M_GIM.INX.gz` |

**怎么下**：

```bash
# CODE SP3（须含年份目录；www.aiub → download.aiub → Switch S3）
curl -L -C - -O \
  "https://www.aiub.unibe.ch/download/CODE/2023/COD0OPSFIN_20230490000_01D_05M_ORB.SP3.gz"

# GFZ 日观测（匿名 HTTPS）
curl -L -C - -O \
  "https://isdc-data.gfz.de/gnss/data/daily/2023/049/POTS00DEU_R_20230490000_01D_30S_MO.crx.gz"
# GFZ 精密轨道（2023-049 → GPS 周 w2249）
curl -L -C - -O \
  "https://isdc-data.gfz.de/gnss/products/final/w2249/GFZ0OPSFIN_20230490000_01D_15M_ORB.SP3.gz"

# CAS 最终 GIM
curl -L -C - -O \
  "https://data.bdsmart.cn/pub/product/iono/ionex/2023/049/CAS0OPSFIN_20230490000_01D_30M_GIM.INX.gz"
```

**账号/配额坑**：均无需 Earthdata；CODE 旧 FTP 已停，裸 `…/CODE/<文件>`（无年份）→ 404；GFZ 产品在 `products/final|rapid|iono/wWWWW/`，不是扁平 `products/WWWW/`；CAS RTS 仅近实时试验；门户说明 [isdc.gfz.de](https://isdc.gfz.de/)（`gfz-potsdam.de` 会跳转）。

### 闪烁 ISMR（`ismr_downloader` 优先）

**我要什么**：低纬 GNSS 闪烁监测（ISMR）指标/相关观测。

**去哪**：[`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader)（PyPI：`ismr-downloader`）· 网页辅：[ISMR Query Tool](https://ismrquerytool.fct.unesp.br/)（常超时/证书失败，勿当主路径）。

**怎么下**：

```bash
# 1) 在 Query Tool 网页注册，取得邮箱/密码（勿写入仓库）
# 2) 安装
pip install ismr-downloader
# 3) 拉取（证书异常时加 --insecure；类型 ismr|ismr1min|sbf|rinex）
ismr-downloader \
  --email "$ISMR_EMAIL" --password "$ISMR_PASSWORD" \
  --stations PRU2 \
  --start 2023-02-18 --end 2023-02-18 \
  --data-type ismr \
  --insecure
# 亦可用 .env：ISMR_EMAIL / ISMR_PASSWORD / ISMR_STATIONS / ISMR_START / ISMR_END / DATA_TYPE
# ismr-downloader --env .env --insecure
```

**账号/配额坑**：须先网页注册；Query Tool 打不开时仍用本脚本（同一 API）；`--insecure` 仅作证书急救；工具自带限流；缺数据写入 `logs/no_data_*.csv`。

### 区域 CORS：GA（澳大利亚，可选）

**我要什么**：澳大利亚（及 APREF 相关）事后 RINEX，可脚本化。

**去哪**：[GA GNSS Data Centre](https://data.gnss.ga.gov.au/) · API：[RINEX File Query](https://data.gnss.ga.gov.au/docs/rinex-file-query/v1.0/web-api-access.html)。

**怎么下**：

```bash
# 按站+时段查文件（JSON 含限时签名 fileLocation）
curl -s "https://data.gnss.ga.gov.au/api/rinexFiles?stationId=ALIC&startDate=2023-02-18T00:00:00Z&endDate=2023-02-19T00:00:00Z&filePeriod=01D&fileType=obs&rinexVersion=3"
# 再：curl -L -C - -OJ "<fileLocation>"
# 对象键示意：…/ALIC00AUS_R_20230490000_01D_30S_MO.crx.gz
```

**账号/配额坑**：开放站匿名可查；签名 URL 会过期，勿写死 `fileLocation`；旧 `ga.gov.au` 深链勿用；批量礼貌限速。

### 区域 CORS：ERGNSS（西班牙）

**我要什么**：西班牙国家网事后 RINEX（日 30 s；亦有小时树）。

**去哪**：[datos-geodesia ERGNSS](https://datos-geodesia.ign.es/ERGNSS/) · 日文件 `diario_30s/` · 小时 `horario_30s/` / `horario_1s/`。

**怎么下**：

```bash
# 路径：diario_30s/YYYY/YYYYMMDD/<站长名>_…MO.crx.gz（日历日，非年积日）
curl -L -C - -O \
  "https://datos-geodesia.ign.es/ERGNSS/diario_30s/2023/20230218/ACOR00ESP_R_20230490000_01D_30S_MO.crx.gz"
```

**账号/配额坑**：开放匿名；目录用 `YYYYMMDD`，文件名里仍带年积日；礼貌限速；小时树按 `HH/` 再下钻，勿与日目录混用。

### 区域 CORS：BEV APOS（奥地利 STAC）

**我要什么**：奥地利 APOS 事后 30 s RINEX（CC BY 4.0）。

**去哪**：[BEV Geoportal](https://data.bev.gv.at/) · STAC [`…/RINEX/RDH1/30S/stac/by_date/catalog.json`](https://data.bev.gv.at/download/RINEX/RDH1/30S/stac/by_date/catalog.json) · 直链树 `…/rinex3/YYYY/DDD/<站>/`。

**怎么下**：

```bash
# A) STAC：catalog → 年 collection → 年积日 collection → 站 item → assets.href
curl -s "https://data.bev.gv.at/download/RINEX/RDH1/30S/stac/by_date/30S_date_2024/30S_date_2024_280/30S_date_2024_280_GRAZ.json"
# B) 已知站/日时直链（例 GRAZ，2024-280）
curl -L -C - -O \
  "https://data.bev.gv.at/download/RINEX/RDH1/30S/rinex3/2024/280/GRAZ/GRAZ00AUT_R_20242800000_01D_30S_MO.crx.gz"
```

**账号/配额坑**：`data.bev.gv.at` 匿名可下；`bev.gv.at` 英文产品深链常进 403 页——用 Geoportal/STAC/上述直链；APOS-PP 免费条款见门户。

### 对流层格网（VMF）

**我要什么**：VMF1/VMF3 格网（PPP / 对流层延迟）。

**去哪**：[VMF](https://vmf.geo.tuwien.ac.at/) → [`trop_products/`](https://vmf.geo.tuwien.ac.at/trop_products/) · 常用 `GRID/1x1/VMF3/VMF3_OP/` 或 `GRID/2.5x2/VMF1/`。

**怎么下**：

```bash
# VMF3 业务产品：GRID/1x1/VMF3/VMF3_OP/YYYY/VMF3_YYYYMMDD.H{00|06|12|18}
curl -L -C - -O \
  "https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/2023/VMF3_20230218.H00"
```

**账号/配额坑**：多开放；文件名是**日历日**不是年积日；先分清 VMF1 vs VMF3、OP vs FC/EI；站文件在 `GNSS/` 子树，勿与 GRID 混用。

---

## 其他门户快查（未展开菜谱）

| 门户 | 入口 | 路径或下一步 | 注册 | 注意 |
|---|---|---|---|---|
| **BKG IGS** | [root_ftp](https://igs.bkg.bund.de/root_ftp/) | 归档目录树；裸域名常 404 | 归档多开放；NTRIP 视挂载点 | 实时：`products.igs-ip.net:2101` 等，见上节 NTRIP |
| **ESA GSSC** | [gssc.esa.int](https://gssc.esa.int/) | 门户检索 → 数据集页 | 门户账号；部分集合另申请 | 勿假设全站开放 |
| **EarthScope** | [GAGE archive](https://gage-data.earthscope.org/archive/gnss) · [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk) | SDK（PyPI）拉 API | EarthScope / GAGE | 原 UNAVCO 页仍可开，新工作以 GAGE + SDK 为准 |
| **GA GNSS** | [data.gnss.ga.gov.au](https://data.gnss.ga.gov.au/) · [RINEX API](https://data.gnss.ga.gov.au/docs/rinex-file-query/v1.0/web-api-access.html) | 见上节「区域 CORS：GA」 | 多开放；个别 API 视密钥 | 签名 URL 短时有效；勿用旧 ga.gov.au 深链 |
| **NRCan CACS** | [CACS 选站页](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php) | 网页选站 → 打包 | 多开放 | 旧 `webapp.csrs.nrcan.gc.ca` 会跳转 |
| **Japan MIRAI** | [miraiarchive](https://go.gnss.go.jp/mirai/miraiarchive/) | 路径 `/rinex/daily/YYYY/DOY/yyd|yyp/`（页内 curl 例）；匿名拉文件/list → **401** | GO!GNSS 注册 + Basic Auth | 含 QZSS；无账号勿写菜谱步骤；本轮未验证持账下载 |
| **Korea GNSS** | [gnssdata.or.kr](https://www.gnssdata.or.kr/) | 登录 → 选站/时段 → ZIP | 网页注册 | 须登录；无匿名文件树，本轮未展开菜谱 |
| **BEV APOS** | [Geoportal](https://data.bev.gv.at/) · STAC catalog | 见上节「区域 CORS：BEV」 | APOS-PP 免费（CC BY 4.0） | `bev.gv.at` 英文深链常 403；用 `data.bev.gv.at` |
| **Spain ERGNSS** | [datos-geodesia ERGNSS](https://datos-geodesia.ign.es/ERGNSS/) | 见上节「区域 CORS：ERGNSS」 | 开放 | 目录 `YYYYMMDD`；礼貌限速 |
| **RENAG** | [renag.resif.fr](https://renag.resif.fr/) | 站网/政策/产品（DOI `10.15778/resif.rg`） | 视 RESIF | 门户可开；无稳定匿名文件树，本轮未验证直链 |
| **SWEPOS** | [RINEX DOI 页](https://www.lantmateriet.se/en/geodata/gps-geodesy-and-swepos/lantmateriets-doi-objects/swepos-rinex-data/) | FTP/SFTP 日文件（DOI `10.23701/c5tc-ew52`，CC0） | 按站方说明 | DOI 页可开；FTP 凭证/主机本轮未核到可复现 200 |
| **HK SatRef** | [RINEX 说明](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 网页选站下载（无稳定匿名文件树） | 多开放 | 说明页 200；无脚本直链可核，勿猜旧 downv/geodex |
| **EPOS / GLASS / M3G** | [EPOS GNSS](https://gnss-epos.eu/) · [GLASS](https://gnssdata-epos.oca.eu/GlassFramework/) · [M3G](https://gnss-metadata.eu/landing/m3g) | GLASS JSON；M3G REST | 视节点 | 欧洲程序化优先 GLASS |
| **VMF** | [vmf.geo.tuwien.ac.at](https://vmf.geo.tuwien.ac.at/) | 见上节「对流层格网（VMF）」 | 多开放 | 日历日文件名；分清 OP/FC |
| **GIRO / DIDBase** | [giro.uml.edu/didbase](https://giro.uml.edu/didbase/) | 查询站/时段 → 图 | 网页注册 | 旧 quick-request URL 已 404 |
| **INTERMAGNET** | [intermagnet.org](https://intermagnet.org/) | Data → 准实时/存档 | 视产品 | 先读条件再脚本 |
| **SuperMAG** | [supermag.jhuapl.edu](https://supermag.jhuapl.edu/) | 界面 / API | 网页注册 | 引用含原始台站 |
| **eSWua / IONORING** | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | Download Tool / REST；近实时地图 | 开放（CC BY；DOI `10.13127/eswua/tec`） | 区域 TEC，非 GNSS 原始归档 |
| **ISMR** | [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader) · [Query Tool](https://ismrquerytool.fct.unesp.br/) | 见上节「闪烁 ISMR」 | 网页注册 | Query Tool 常超时；脚本为主 |
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
