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

## CDDIS / Earthdata（最常用）

无 Earthdata 授权时，`.../archive/gnss/data/daily/` 等常返回 **401**（正常）。匿名 FTP 已停，请走 **HTTPS**（或 `ftps://gdc.cddis.eosdis.nasa.gov/`）。

| 步 | 做什么 |
|---:|---|
| 1 | [Earthdata Login](https://urs.earthdata.nasa.gov/) 免费注册并验证邮箱 |
| 2 | 打开 [CDDIS GNSS 归档](https://cddis.nasa.gov/archive/gnss/)，登录；在 URS「Applications」授权 **CDDIS** / **NASA GES DISC** 等相关应用 |
| 3 | 浏览器能列目录后，脚本用同一账号 + `.netrc`；**限速**、断点续传（`-C -` / `--continue`） |
| 4 | 路径对照：[GNSS holdings](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/GNSS_data_holdings.html) · [high-rate 说明](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) |

### `.netrc` + curl / wget

```bash
# ~/.netrc  （权限务必 600；勿提交仓库）
machine urs.earthdata.nasa.gov login YOUR_USER password YOUR_PASS
```

```bash
chmod 600 ~/.netrc
# 例：某日 IGS 综合 IONEX（路径按当日目录名调整）
curl -L -n -C - -o igs.INX.gz \
  "https://cddis.nasa.gov/archive/gnss/products/ionex/2023/049/IGS0OPSFIN_20230490000_01D_02H_GIM.INX.gz"
# 或
wget --auth-no-challenge --continue --load-cookies cookies.txt \
  --save-cookies cookies.txt --keep-session-cookies \
  "https://cddis.nasa.gov/archive/gnss/products/ionex/2023/049/..."
```

若下到的是 HTML 登录页而不是 `.gz`/`.rnx`：重走步骤 2，确认应用已授权。读 GIM 见 [ionex-gim](./software/ionex-gim.md)。

### CDDIS 路径模式

| 类型 | 路径概念 | 内容 |
|---|---|---|
| OBS | `gnss/data/daily/YYYY/DDD/` | RINEX（常 `.crx.gz`）；子目录按类型/频率 |
| NAV | 同日或 `brdc` | 广播星历 |
| 高采样 | `gnss/data/highrate/YYYY/DDD/` 等 | 见 high-rate 说明页；可用 `cddis-highrate-downloader` |
| SP3 / CLK | `gnss/products/WWWW/` | 精密轨道 / 钟差（`WWWW` = GPS 周） |
| IONEX | `gnss/products/ionex/YYYY/DDD/` | GIM（VTEC 格网） |
| bias / DCB | `gnss/products/bias/` 等 | 码偏差、OSB |

约 GPS 周 2238 起多用长文件名（如 `IGS0OPSFIN_…_GIM.INX.gz`）。对照 [IGS Products](https://igs.org/products/) · [Data Access](https://igs.org/data-access/)。

## 其他门户（入口 / 路径 / 注册 / 注意）

| 门户 | 入口 | 路径或下一步 | 注册 | 注意 |
|---|---|---|---|---|
| **BKG IGS** | [root_ftp](https://igs.bkg.bund.de/root_ftp/) | 归档目录树；裸 `igs.bkg.bund.de/` 常 404 | 归档多开放；NTRIP 视挂载点 | 实时优先 [igs-ip.net](https://www.igs-ip.net/)（本环境探测偶发超时）/ BKG NTRIP |
| **IGS files** | [files.igs.org/pub/](https://files.igs.org/pub/) | 站志、天线、部分产品树 | 多开放 | 大文件限速；目录会调整 |
| **ESA GSSC** | [gssc.esa.int](https://gssc.esa.int/) | 门户检索 → 数据集页下载 | 门户账号；部分集合另申请 | 权限按数据集，勿假设全站开放 |
| **GFZ ISDC** | [isdc-data.gfz.de/gnss/](https://isdc-data.gfz.de/gnss/) | `/gnss/data/daily/`、`/highrate/`、产品树 | 匿名 HTTPS 为主 | 旧 FTP 已迁至此；门户说明见 [isdc.gfz.de](https://isdc.gfz.de/)（`gfz-potsdam.de` 会跳转） |
| **CODE / AIUB** | [aiub download](https://www.aiub.unibe.ch/download/) → [S3 列表](https://code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php) | `CODE/`、`ionex/`、`CODE_MGEX/` 等 | 开放（旧 FTP 已停） | 最终/快速/超快速与 IONEX 同一浏览器入口 |
| **CAS BDsmart** | [pub 根](https://data.bdsmart.cn/pub/) | [`product/iono/ionex/`](https://data.bdsmart.cn/pub/product/iono/ionex/) · [`product/rts/iono/`](https://data.bdsmart.cn/pub/product/rts/iono/) · bias/SSR 子树 | 开放 | 事后分析用最终 IONEX；RTS 仅近实时试验 |
| **CDDIS high-rate** | [说明页](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) | 实体仍在 CDDIS archive | Earthdata | 闪烁/同震；配合专用下载脚本 |
| **NOAA CORS** | [CORS](https://geodesy.noaa.gov/CORS/) · [corsdata](https://geodesy.noaa.gov/corsdata/) · [UFCORS](https://geodesy.noaa.gov/UFCORS/) | 目录树按年/站；UFCORS 交互裁剪 | 多开放 | 大批量优先 [NODD S3 `noaa-cors-pds`](https://noaa-cors-pds.s3.amazonaws.com/index.html)（按年积日/站名对象键） |
| **GeoNet NZ** | [说明](https://www.geonet.org.nz/data/types/geodetic) · [API](https://data.geonet.org.nz/) | RINEX：[`/v1/data/gnss/rinex/`](https://data.geonet.org.nz/v1/data/gnss/rinex/)（另有 1 Hz） | 开放；读 Data Policy | 根路径对 HEAD 可能 405，用 GET；旧兼容端点计划 2026 年底退役 |
| **IBGE RBMC** | [geoftp RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [API 文档](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1) | geoftp 目录或 API `rinex2`/`rinex3`/1 s | API 文档公开（HEAD 或 405，用 GET） | 礼貌限速；端点以文档版本为准 |
| **EarthScope** | [GAGE archive](https://gage-data.earthscope.org/archive/gnss) · [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk) | 归档常跳登录；SDK（PyPI）拉 API | EarthScope / GAGE 账号 | 原 UNAVCO 页仍可开，新工作以 GAGE + SDK 为准 |
| **EUREF EPN** | [中央局](https://epncb.oma.be/) · [obs](https://epncb.oma.be/pub/obs/) | `/pub/obs/` 按站；旧 `/ftp/obs/` 会跳到此 | 事后多开放；NTRIP 另见 EUREF-IP | 批量前对照中央局站状态；高采样注意容量 |
| **GA GNSS** | [data.gnss.ga.gov.au](https://data.gnss.ga.gov.au/) | 门户检索 / 官方 API（勿用旧 ga.gov.au 深链） | 多开放；个别 API 视密钥 | 澳新区域主源；站网元数据会更新 |
| **NRCan CACS** | [CACS 选站页](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/cacs-scca.php) | 网页选站 → 打包 RINEX/元数据 | 多开放 | 旧 `webapp.csrs.nrcan.gc.ca` 会跳转到本 URL |
| **Japan MIRAI** | [miraiarchive](https://go.gnss.go.jp/mirai/miraiarchive/) | 年积日 RINEX 3/4（含 Hatanaka）；页内有 wget/curl 例 | GO!GNSS 网页注册 + HTTPS 基本认证 | 含 QZSS 监测站；相对传统 GEONET 申请更易脚本化 |
| **Korea GNSS** | [gnssdata.or.kr](https://www.gnssdata.or.kr/) | 登录 → 事后数据页选站/时段 → ZIP | 网页注册（회원가입） | 单次跨度常有上限；保留策略以站内为准 |
| **BEV APOS** | [产品说明](https://www.bev.gv.at/en/Services/Products/Austrian-POsitioning-Service.html) · [Geoportal](https://data.bev.gv.at/) | STAC 例：`/download/RINEX/RDH1/30S/stac/by_date/catalog.json`（亦有 `01S`、`by_stat`） | APOS-PP 免费无注册（CC BY 4.0）；实时另注册 | 德语深链 `…/APOS.html` 常 403；用英文页或 Geoportal |
| **Spain ERGNSS** | [datos-geodesia ERGNSS](https://datos-geodesia.ign.es/ERGNSS/) | HTTPS 公开目录树 | 开放 | 限速；并列目录可见 EUREF/IGS 等 |
| **RENAG** | [renag.resif.fr](https://renag.resif.fr/) | 站网/政策/产品入口（DOI `10.15778/resif.rg`） | 视 RESIF 声明 | 先读数据政策再下；非解算软件 |
| **SWEPOS** | [RINEX DOI 页](https://www.lantmateriet.se/en/geodata/gps-geodesy-and-swepos/lantmateriets-doi-objects/swepos-rinex-data/) | FTP/SFTP 日文件 RINEX 2/3（DOI `10.23701/c5tc-ew52`，CC0） | 按站方说明注册后取 | 实时流权限另见 SWEPOS 条款 |
| **HK SatRef** | [RINEX 说明](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 按页指示取事后 RINEX | 多开放 | 注意采样率与保留期限；大批量礼貌限速 |
| **EPOS / GLASS / M3G** | [EPOS GNSS](https://gnss-epos.eu/) · [GLASS](https://gnssdata-epos.oca.eu/GlassFramework/) · [M3G](https://gnss-metadata.eu/landing/m3g) | GLASS：站/元数据/RINEX URL（JSON 等）；M3G：站点日志与 REST | 视节点许可 | 程序化欧洲观测优先 GLASS，勿臆造未公开接口 |
| **CDAAC** | [cdaac-www.cosmic.ucar.edu](https://cdaac-www.cosmic.ucar.edu/) | 注册后下 ionPhs / ionPrf 等 | CDAAC 账号 | 电离层 excess phase / Ne 剖面 |
| **ROM SAF** | [rom-saf.eumetsat.int](https://rom-saf.eumetsat.int/) | 产品与 [ROPP](https://rom-saf.eumetsat.int/ropp/) | 多需注册 | 处理包与产品页面分开找 |
| **AWS GNSS-RO** | [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | `pip install awsgnssroutils` 查/下多中心 Level-1b/2 | 开放（AWS 公开桶） | `registry.opendata.aws/gnss*` 深链常 404；以工具与仓库说明为准 |
| **VMF** | [vmf.geo.tuwien.ac.at](https://vmf.geo.tuwien.ac.at/) | [`trop_products/`](https://vmf.geo.tuwien.ac.at/trop_products/) | 多开放 | 选对 VMF1/VMF3 与气象模型 |
| **GIRO / DIDBase** | [giro.uml.edu/didbase](https://giro.uml.edu/didbase/) | 查询站/时段 → 下载测高仪图 | 网页注册 | 旧 quick-request URL 已 404；与 GNSS TEC 对齐时间与穿透点 |
| **Kyoto WDC** | [wdc.kugi.kyoto-u.ac.jp](https://wdc.kugi.kyoto-u.ac.jp/) | Kp / Dst 等指数页 | 多开放 | 批量遵守礼貌访问 |
| **INTERMAGNET** | [intermagnet.org](https://intermagnet.org/) | Data 页 → 准实时/存档 | 视产品 | 先读条件再脚本抓 |
| **SuperMAG** | [supermag.jhuapl.edu](https://supermag.jhuapl.edu/) | 注册后按界面 / API | 网页注册 | 引用含原始台站 |
| **GFZ Kp** | [kp.gfz.de/en](https://kp.gfz.de/en/) | 确定值 / 预报分清；可下或调接口 | 开放 | `kp.gfz-potsdam.de` 会跳到本域；勿与 SWPC K 指数混用不标注 |
| **SWPC** | [spaceweather.gov](https://www.spaceweather.gov/) | Products（K 指数、GloTEC 等） | 开放 | `swpc.noaa.gov` 现多跳转到本站；`spaceweather.noaa.gov` 仍不可靠 |
| **eSWua / IONORING** | [eSWua TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) · [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | eSWua：Download Tool / REST；IONORING：近实时地图 | 开放（CC BY 4.0；DOI `10.13127/eswua/tec`） | 区域 TEC 产品，不是 GNSS 原始观测归档 |
| **UPC TOMION** | [chapman rapid](https://chapman.upc.es/tomion/rapid/) | 按年匿名拉快速格网 | 开放 | 覆盖/时延不及 CDDIS 正式库；大批量限速 |
| **ISMR** | [Query Tool](https://ismrquerytool.fct.unesp.br/) | 网页查询；或 [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader) | 网页注册 | 站点偶发超时/证书问题（本轮探测仍失败）；打不开时优先脚本条目 |
| **CSNO TARC** | [csno-tarc.cn](https://www.csno-tarc.cn/) · [差分英文页](https://www.csno-tarc.cn/en/data/differential) | 测试评估 / 差分入口 | 浏览多开放；部分产品视注册 | 与 IGS OSB 信号定义可能不同，融合时核对基准 |
| **SOPAC**（可选镜像） | [sopac-csrc.ucsd.edu](https://sopac-csrc.ucsd.edu/) · [garner `/pub/`](https://garner.ucsd.edu/pub/) | 历史 IGS DC / 产品树 | 多开放 | **本轮探测超时**；关键周请与 CDDIS/BKG/GFZ 交叉校验 |

## 相关教程与软件

下完数据后常接：

| 目标 | 去哪 |
|---|---|
| 双频 STEC / 一日练习 | [02](./tutorials/02-gnss-dualfreq-tec.md) · [16](./tutorials/16-practice-one-day-tec.md) |
| 读 GIM / IONEX | [03](./tutorials/03-gim-ionex.md) · [ionex-gim](./software/ionex-gim.md) |
| 目录怎么用 | [08](./tutorials/08-how-to-use-this-catalog.md) |
| RINEX 读盘 / QC | [georinex](./software/georinex.md) · [anubis](./software/anubis.md) |
| 软件短文总索引 | [software/README](./software/README.md) · [tutorials/README](./tutorials/README.md) |
