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
| 掩星 RO | [CDAAC](https://cdaac-www.cosmic.ucar.edu/) · [data.cosmic](https://data.cosmic.ucar.edu/gnss-ro/) · [ROM SAF](https://rom-saf.eumetsat.int/)（[决策表](#电离层与地磁门户决策表)）· [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | 开放 / ROM SAF 产品库须注册（AWS 镜像开放） |
| 地磁 / 空间天气 | [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · [INTERMAGNET](https://intermagnet.org/) · [SuperMAG](https://supermag.jhuapl.edu/) · [GFZ Kp](https://kp.gfz.de/en/) · [SWPC](https://www.spaceweather.gov/) · 台站分钟 / 秒值：USGS · BGS · NRCan · THEMIS GMAG · MACCS · TGO → [决策表](#电离层与地磁门户决策表) | 开放 / 注册 |
| 区域 TEC 现报 | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 开放（CC BY） |
| 闪烁 ISMR | [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader)（主）· [Query Tool](https://ismrquerytool.fct.unesp.br/)（辅，常超时） | 网页注册 |
| 测高仪 | [GIRO / DIDBase](https://giro.uml.edu/didbase/) · [RAL / UKSSDC](https://www.ukssdc.ac.uk/ionosondes/) | 网页注册 |
| ISR / SuperDARN / 区域台链 | [CEDAR Madrigal](https://cedar.openmadrigal.org/) · [EISCAT](https://portal.eiscat.se/) · [SRI AMISR](https://data.amisr.com/database/) · [FRDR SuperDARN](https://www.frdr-dfdr.ca/repo/collection/superdarn) · [子午工程](https://www.meridianproject.ac.cn/) · [PITHIA 编目](https://esc.pithia.eu/) → [决策表](#电离层与地磁门户决策表) | Madrigal / FRDR 开放；EISCAT 门户、子午工程须登录 |
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

**账号/配额坑**：`data.cosmic` 匿名开放（ionPhs/ionPrf 等）；旧「必须 CDAAC 网页账号」已过时；ROM SAF 产品库须注册登录（未登录 `login.php` 回 401），其中性大气产品在 AWS `gnss-ro-data/contributed/v1.1/romsaf/` 可匿名拉，见[决策表 E5](#dp-e5)；AWS 工具**没有** `ionPhs` 文件名——电离层 excess phase 用 CDAAC 直链，AWS 侧重 `calibratedPhase` 等三型；勿把 registry 深链写进脚本；处理包 ROPP 与产品页分开找。

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

## 电离层与地磁门户决策表

第 21–22 轮收录的 14 个门户（ISR / SuperDARN / 测高仪 / 地磁 / 掩星 / 编目）。「实测」列里的命令都在 2026-09-26 跑过，结果是当时的真实返回；✗ 表示拿不到数据文件，并写出卡在哪一道门。

| 门户 | 账号 / 门槛 | 格式 | 时间分辨率 · 时延 | 实测 |
|---|---|---|---|:---:|
| [EISCAT Portal](https://portal.eiscat.se/) | 门户 L2 下载须 **EGI Check-in + 加入 EISCAT VO**（首页提示 "You are not identified through EGI Check-in"）；计划 / 实时图公开。**绕行**：[EISCAT Madrigal](https://madrigal.eiscat.se/madrigal/) 匿名（只填姓名 / 邮箱 / 单位字段） | HDF5（Madrigal；GUISDAP params / pp 两类文件） | 按实验战役，非连续；样例积分 60 s（文件名 `_60`） | ✅ Madrigal（[E1](#dp-e1)） |
| [SRI AMISR](https://data.amisr.com/database/) | 开放；数据走 SRI Madrigal `data.amisr.com/madrigal`（同样填三字段） | HDF5 | PFISR/RISR 同一实验给 1 / 3 / 5 min 积分多个版本；PFISR 常开长时低占空比模式（2024-05 共 94 个实验） | ✅（[E2](#dp-e2)） |
| [CEDAR Madrigal](https://cedar.openmadrigal.org/) | 开放；下载须填姓名 / 邮箱 / 单位（不校验，但请写真实信息） | HDF5（`fileType=-2`；也可出 ASCII） | 全球 TEC 1°×1°×5 min 日文件；另有 LOS TEC、ROTI；先出 `Preliminary`，后补 `final` | ✅（[E3](#dp-e3)） |
| [子午工程数据中心](https://www.meridianproject.ac.cn/) | **注册登录**：[注册](https://soc.meridianproject.ac.cn/sso/register?lang=zh_CN) → [数据检索](https://dcstatus.meridianproject.ac.cn/#/sjfw/sjjs?checkLogin=true&lang=cn)（SPA，`checkLogin=true`）；批量 = 在线提交「离线服务申请」 | 按设备（DOI 清单含 GNSS RINEX 观测 / 星历、垂直 TEC、闪烁指数、ISR 拟合参量等） | 视设备 | ✗ 数据（无账号）；DOI 清单 ✅（[E4](#dp-e4)） |
| [ROM SAF](https://rom-saf.eumetsat.int/) | 产品库**须注册登录**（`/login.php` → **401**；[注册页](https://rom-saf.eumetsat.int/registration.php) 200）；CC BY 4.0。**绕行**：AWS `gnss-ro-data` 桶 `contributed/v1.1/romsaf/` 匿名 | netCDF4（AWS 镜像） | 每次掩星一个文件；NRT / 离线 / CDR（2001-09～2016-12）/ ICDR（2017 起）；**只有中性大气，无电子密度 / TEC** | ✅ AWS（[E5](#dp-e5)） |
| [FRDR SuperDARN](https://www.frdr-dfdr.ca/repo/collection/superdarn) | 单文件 HTTPS **匿名**；整包 Globus Transfer 须 Globus 账号；用前读顶层 README（致谢 / 联系 PI / 1 年禁用期） | `rawacf.bz2`（dmap）；早年 `dat` | 按年分数据集（每年一个 DOI）；文件按雷达 × 时段切块；**时延约 1～2 年**（2023 RAWACF 于 2025-09-18 发布） | ✅（[E6](#dp-e6)） |
| [PITHIA e-Science](https://esc.pithia.eu/) | 浏览 / 检索公开；登记资源（提供方）须 EGI Check-in（`/authorised/dashboard/` → 302 到 `aai.egi.eu`） | 元数据 XML（PITHIA 本体 2.2）；**不存数据**，跳转提供方 | 不适用 | ✅ 元数据（[E7](#dp-e7)） |
| [USGS Geomagnetism](https://www.usgs.gov/programs/geomagnetism/data) | Web 服务无需账号。门户页 `www.usgs.gov` 对无 UA 的 curl 回 **403**（加浏览器 UA 为 200）；`geomag.usgs.gov/ws` 无 UA 也 200 | IAGA-2002 / JSON | 1 s、1 min 等；实时：07:12 UTC 查到的最新值为 07:09（约 3 min） | ✅（[E8](#dp-e8)） |
| [NRCan 地磁](https://geomag.nrcan.gc.ca/data-donnee/sd-en.php) | 无需账号（FDSN，网络码 `C2`）；非商业，发表须致谢 NRCan | miniSEED（dataselect）；台站表为 text | 通道 `UF?` = 1 min，`LF?` = 1 s；位置码 `R0` 实时（最近 2 h 查询返回 61440 B） | ✅（[E9](#dp-e9)） |
| [BGS Geomag](https://geomag.bgs.ac.uk/data_service/data/home.html) | 本站写明 1 s / 1 min「on application」，仅学术非商业。**实际可用**：BGS 运营的 [GIN Web 服务](https://imag-data.bgs.ac.uk/GIN_V1/GINServices)（INTERMAGNET 节点）匿名拿 ESK/LER/HAD | IAGA-2002 | `samplesPerDay=minute` 或 `second`；`best-avail`。实测最近 2 天全是 99999，没看到准实时值 | ✅（[E10](#dp-e10)） |
| [MACCS](http://space.augsburg.edu/maccs/) | 开放（仅 HTTP，JSP 表单给直链）；更高分辨率须发邮件 `maccs@augsburg.edu`；发表前联系 PI | IAGA-2002（地磁本地坐标 XYZ，F 填 88888） | 0.5 s 平均（0.125 s 采样），日文件约 12 MB；时延 ≤1 天（09-26 已有 09-25 的文件） | ✅（[E11](#dp-e11)） |
| [THEMIS GMAG](https://themis.ssl.berkeley.edu/gmag/) | 开放 HTTPS；SPDF 同路径镜像 | CDF（L2） | FYKN 样例一天 86400 点 = 1 s；L2 时延约 9 天（09-26 时最新为 09-17） | ✅（[E12](#dp-e12)） |
| [TGO 特罗姆瑟](https://flux.phys.uit.no/geomag.html) | 图和 K 指数公开；**ASCII 数字数据要密码**：挪威站向 TGO 要、丹麦 / 格陵兰站向 DTU Space 要（见 [Data access](https://flux.phys.uit.no/div/DataAccess.html)）；GFZ 站为 CC BY-NC 4.0 | ASCII / IAGA-2002 | 1 min、10 s；K 指数 3 h | K 指数 ✅；ASCII ✗（[E13](#dp-e13)） |
| [RAL 测高仪 (UKSSDC)](https://www.ukssdc.ac.uk/ionosondes/) | **须注册**（免费、自动）：[userreg.pl](https://www.ukssdc.ac.uk/cgi-bin/wdcc1/userreg.pl)；之后用户名为注册邮箱。未登录时 `/dpsdata/` 与 `cost_database.pl` 均为 **401** | 原始 DPS 电离图文件（SAO-Explorer 读）+ URSI 标定参数 | 常规 1 h 一张电离图（可申请加密探测）；Chilton 序列承接 1931 年起的 Slough | ✗（[E14](#dp-e14)） |

要登录才能拿数据的：EISCAT 门户（Madrigal 可绕行）、子午工程、ROM SAF 产品库（AWS 可绕行）、TGO ASCII、UKSSDC/RAL。要「申请」的：BGS 本站高分辨率（GIN 可绕行）。

### 逐门户实测命令

<a id="dp-e1"></a>**E1 EISCAT（Madrigal 镜像）**

```bash
curl -L -o eiscat.h5 "https://madrigal.eiscat.se/madrigal/getMadfile.cgi?fileName=/opt/madrigal/experiments/2024/tro/16may24/MAD6400_2024-05-16_manda_60@uhf.hdf5&fileType=-2&user_fullname=Your+Name&user_email=you@example.org&user_affiliation=Your+Org"
# 实测：HTTP 200，7342985 B，文件头 \x89HDF
```

门户 L2 要走 EGI Check-in：先注册 [EGI Check-in](https://aai.egi.eu/)，再按门户首页 "THIS GUIDE" 申请加入 EISCAT VO（人工批准），批准后才能在 Schedule and L2 Data 下载。

<a id="dp-e2"></a>**E2 SRI AMISR（SRI Madrigal）**

```bash
curl -L -o pfisr.h5 "https://data.amisr.com/madrigal/getMadfile.cgi?fileName=/opt/madrigal/madrigal3/experiments0/2024/pfa/04may24c/pfa20240504.003_ac_nenotr_05min.001.h5&fileType=-2&user_fullname=Your+Name&user_email=you@example.org&user_affiliation=Your+Org"
# 实测：HTTP 200，2817905 B，application/x-hdf5
```

`getVersionService.py` 报 SRI 为 2.6，CEDAR / EISCAT 为 3.2；madrigalWeb 3.3.8 对三者都能 `getExperiments` / `getExperimentFiles`。

<a id="dp-e3"></a>**E3 CEDAR Madrigal（madrigalWeb 或 curl）**

```bash
pip install madrigalWeb
python - <<'PY'
import madrigalWeb.madrigalWeb as mw
m = mw.MadrigalData("https://cedar.openmadrigal.org")
exps = m.getExperiments(8000, 2024,5,10,0,0,0, 2024,5,10,23,59,59)   # 8000 = World-wide GNSS Receiver Network
f = [x for x in m.getExperimentFiles(exps[-1].id) if "site_" in x.name][-1]
m.downloadFile(f.name, "site_20240510.h5", "Your Name", "you@example.org", "Your Org", format="hdf5")
PY
# 实测：2 个实验（09may24、10may24），site_20240510.002.h5 = 134718 B，HDF5
# 等价 curl：https://cedar.openmadrigal.org/getMadfile.cgi?fileName=<上面的 f.name>&fileType=-2&user_fullname=…&user_email=…&user_affiliation=…
```

同一天的 TEC 格网 `gps240510g.00N.hdf5` 较大，先用 `getExperimentFilesService.py?id=<实验号>` 看清单再选文件。

<a id="dp-e4"></a>**E4 子午工程**

```bash
curl -sL "https://www.meridianproject.ac.cn/sjj/" | grep -oE '10\.12176/[0-9.]+-V[0-9]+' | sort -u | wc -l
# 实测：1161（DOI 前缀 10.12176，CSTR 前缀 14804.11）
```

拿数据文件的步骤：① 在 [soc 注册页](https://soc.meridianproject.ac.cn/sso/register?lang=zh_CN) 开账号 → ② 登录后进 dcstatus「数据检索」按设备 / 台站 / 时段筛选下载 → ③ 大批量走「批量下载」（离线服务申请）→ ④ 发表时按[数据政策](https://www.meridianproject.ac.cn/sjzc/)写 DOI + CSTR `31122.02.MSP`，并向子午工程中心报送成果。本轮没有账号，**没有**验证文件格式和下载接口。

<a id="dp-e5"></a>**E5 ROM SAF（AWS 开放镜像）**

```bash
curl -O "https://gnss-ro-data.s3.amazonaws.com/contributed/v1.1/romsaf/metop/atmosphericRetrieval/2006/10/27/atmosphericRetrieval_metop_romsaf_2305.0010_metopa-G01-200610271102.nc"
# 实测：HTTP 200，17477 B，文件头 \x89HDF（netCDF4）
# 列目录：https://gnss-ro-data.s3.amazonaws.com/?list-type=2&delimiter=/&prefix=contributed/v1.1/romsaf/
```

门户产品库：[registration.php](https://rom-saf.eumetsat.int/registration.php) 注册 → 登录后在 Product Archive 选产品。未登录时 `login.php` 回 401。

<a id="dp-e6"></a>**E6 FRDR SuperDARN（HTTPS 单文件）**

```bash
curl -L -O "https://www.frdr-dfdr.ca/repo/files/7/published/publication_443/submitted_data/2014/01/20140115.1201.00.cve.rawacf.bz2"
# 实测：302 → g-0758ab.cd4fe.0ec8.data.globus.org，HTTP 200，1029 B（BZh）；解压 76654 B，dmap 头含 radar.revision.major
# 同集 README：…/submitted_data/2014RAWACF.readme.txt（200，20102 B）
```

列目录：`/repo/files/...` 目录本身不能浏览。文件清单在 `https://www.frdr-dfdr.ca/cache/7/publication_<item>/file_sizes/file_sizes.json`（根目录），子目录用 `file_sizes-<sha256(相对路径，例如 "2014/01")>.json`。2014 RAWACF 的 item 为 443，全集约 4.8 TB；常规文件（如 `20140101.0000.01.ade.a.rawacf.bz2`）约 26 MB，先挑小时段试。

<a id="dp-e7"></a>**E7 PITHIA e-Science**

```bash
curl -s "https://esc.pithia.eu/data-collections/DataCollection_DIAS_Network/xml/" | grep -c '&lt;DataCollection'
# 实测：HTTP 200，29264 B，页内嵌转义后的 <DataCollection xmlns=…> 元数据
```

只拿到元数据；数据要按集合页的 API / 链接去提供方（如 DIAS、DIDBase）。

<a id="dp-e8"></a>**E8 USGS Geomag Web 服务**

```bash
curl -s "https://geomag.usgs.gov/ws/data/?id=BOU&starttime=2024-05-10T00:00:00Z&endtime=2024-05-10T00:09:00Z&elements=H,D,Z,F&sampling_period=60&type=variation&format=iaga2002"
# 实测：HTTP 200，2201 B；首行 " Format                 IAGA-2002 …"；末行 2024-05-10 00:09:00.000 131  20786.50 -20.52 46381.01 51335.22
# format=json 同样 200；sampling_period=1 给 1 s；不带时间参数时返回当天 UTC（未来时刻为 null）
```

<a id="dp-e9"></a>**E9 NRCan（Earthquakes Canada FDSN）**

```bash
curl -o ott.mseed "https://www.earthquakescanada.nrcan.gc.ca/fdsnws/dataselect/1/query?net=C2&sta=OTT&loc=R0&cha=UFX&starttime=2024-05-10T00:00:00&endtime=2024-05-10T01:00:00"
# 实测：HTTP 200，512 B，application/vnd.fdsn.mseed，记录头 "000001D OTT  R0UFXC2"
# 台站表：…/fdsnws/station/1/query?net=C2&level=station&format=text （200；ALE、BLC、FCC、MEA、OTT…）
```

miniSEED 可用 ObsPy `read()` 读（本轮没装 ObsPy，只核了记录头）。

<a id="dp-e10"></a>**E10 BGS（GIN Web 服务）**

```bash
curl -o esk.txt "https://imag-data.bgs.ac.uk/GIN_V1/GINServices?Request=GetData&format=IAGA2002&testObsys=0&observatoryIagaCode=ESK&samplesPerDay=minute&dataStartDate=2024-05-10&dataDuration=1&publicationState=best-avail&orientation=native"
# 实测：HTTP 200，104157 B，1467 行，Station Name "Eskdalemuir, United Kingdom"
# samplesPerDay=second（LER）：200，6136388 B
```

<a id="dp-e11"></a>**E11 MACCS**

```bash
# 表单 retrieveiaga2002.jsp 返回直链；直链模式 IAGA2002/<IAGA>/<YYYY>/<iaga>YYYYMMDDv_l1_half_sec.sec
curl -O "http://space.augsburg.edu/maccs/IAGA2002/IGL/2024/igl20240510v_l1_half_sec.sec"
# 实测：HTTP 200，Content-Length 12270078；头 "Station Name  Igloolik, Nunavut, Canada"，"Data Interval Type  Averaged 0.5-Second"
```

站码对照：表单值 CD / CY / CH / GH / IG / NA / PG / PB / RB（IG → IGL）。

<a id="dp-e12"></a>**E12 THEMIS GMAG**

```bash
curl -O "https://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/fykn/2024/thg_l2_mag_fykn_20240510_v01.cdf"
# 实测：HTTP 200，1770138 B，魔数 cdf30001；cdflib 读出 thg_mag_fykn_time 86400 点，间隔约 1.0 s
# 镜像：https://spdf.gsfc.nasa.gov/pub/data/themis/thg/l2/mag/<站>/<YYYY>/
```

<a id="dp-e13"></a>**E13 TGO**

```bash
curl -s "https://flux.phys.uit.no/Kindice/k_tro2a.txt"
# 实测：HTTP 200，183 B；首行 "K-Indices for Tromso"，列最近一周（如 "20 sep. 2026 4221 0003"）
# ASCII 数据（无密码）：
curl -s "https://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tro2a&year=2024&month=5&day=10&res=1min&pwd=&format=iagaUnix&comps=DHZ&getdata=+Get+Data+"
# 实测：HTTP 200 但正文只有 "User error  - please contact magnar.g.johnsen@uit.no"（53 B）
```

拿密码：挪威站数据向 TGO 申请，丹麦 / 格陵兰站向 DTU Space 申请（[Data access](https://flux.phys.uit.no/div/DataAccess.html)）；然后把密码填进 `pwd=`。不想申请的话，北欧多数台站在 IMAGE 数据库也有，通常延迟几个月。

<a id="dp-e14"></a>**E14 RAL 测高仪（UKSSDC）**

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://www.ukssdc.ac.uk/dpsdata/"
# 实测：401（返回 Data Access Registration 页）；/cgi-bin/digisondes/cost_database.pl 同为 401
```

步骤：① 填 [userreg.pl](https://www.ukssdc.ac.uk/cgi-bin/wdcc1/userreg.pl)（姓名、邮箱、UK / 非 UK、用户类型，加一道人机验证；自动开通）→ ② 用注册邮箱作用户名登录 `/dpsdata/`（原始数字数据）或 [Prompt Ionospheric Database](https://www.ukssdc.ac.uk/prompt_database.html)（自动标定参数表 / 绘图 / POLAN / 下载 SAO-Explorer 原始文件）。本轮没有注册，没有验证文件。

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
