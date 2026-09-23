# GNSS 数据怎么下

配合 [`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md)。本页只答三件事：**要什么 → 去哪下 → 要不要注册**。

![STEC / VTEC 产品从观测来（本仓库自制）](./tutorials/images/fig-stec-vtec-shell.png)

想先看现象长什么样？→ [README 现象画廊](../README.md)

## 一屏决策

| 你想要 | 优先门户 | 注册 |
|---|---|:---:|
| 全球 RINEX / 广播星历 | [CDDIS](https://cddis.nasa.gov/archive/gnss/) · [BKG root_ftp](https://igs.bkg.bund.de/root_ftp/) · [GFZ ISDC HTTPS](https://isdc-data.gfz.de/gnss/) · [ESA GSSC](https://gssc.esa.int/) | Earthdata / 视中心 |
| SP3 / CLK / 偏差 | CDDIS `gnss/products/` · [IGS files](https://files.igs.org/pub/) · GFZ ISDC | 同左 |
| GIM / IONEX | CDDIS `gnss/products/ionex/` · CODE / UPC 等 | 视源 |
| 高采样率（闪烁 / 同震） | [CDDIS high-rate](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) · GFZ `/gnss/highrate/` · `cddis-highrate-downloader` | Earthdata / 开放 |
| 区域 CORS | [NOAA CORS](https://geodesy.noaa.gov/CORS/) · [GeoNet API](https://data.geonet.org.nz/) · [IBGE RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [EarthScope GAGE](https://gage-data.earthscope.org/archive/gnss) | 视网络 |
| 实时 RTCM / SSR | BKG / IGS RTS（NTRIP，常经 [igs-ip.net](https://www.igs-ip.net/)） | 账号或挂载点 |
| 掩星 RO | [CDAAC](https://cdaac-www.cosmic.ucar.edu/) · [ROM SAF](https://rom-saf.eumetsat.int/) · [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | 账号 / 开放 |
| 地磁 / 空间天气 | [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · [INTERMAGNET](https://www.intermagnet.org/) · [SuperMAG](https://supermag.jhuapl.edu/) · [SWPC](https://www.swpc.noaa.gov/) | 开放 / 注册 |
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
| **BKG IGS** | [root_ftp](https://igs.bkg.bund.de/root_ftp/) | 归档目录树；裸 `igs.bkg.bund.de/` 常 404 | 归档多开放；NTRIP 视挂载点 | 实时优先 [igs-ip.net](https://www.igs-ip.net/) / BKG NTRIP；caster 根地址可能 400，仍可作为已知主机 |
| **IGS files** | [files.igs.org/pub/](https://files.igs.org/pub/) | 站志、天线、部分产品树 | 多开放 | 大文件限速；目录会调整 |
| **ESA GSSC** | [gssc.esa.int](https://gssc.esa.int/) | 门户检索 → 数据集页下载 | 门户账号；部分集合另申请 | 权限按数据集，勿假设全站开放 |
| **GFZ ISDC** | [isdc-data.gfz.de/gnss/](https://isdc-data.gfz.de/gnss/) | `/gnss/data/daily/`、`/highrate/`、产品树 | 匿名 HTTPS 为主 | 旧 FTP 迁移至此；门户说明见 [isdc.gfz-potsdam.de](https://isdc.gfz-potsdam.de/) |
| **CDDIS high-rate** | [说明页](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) | 实体仍在 CDDIS archive | Earthdata | 闪烁/同震；配合专用下载脚本 |
| **NOAA CORS** | [CORS](https://geodesy.noaa.gov/CORS/) · [corsdata](https://geodesy.noaa.gov/corsdata/) | 目录树按年/站；也可用 User Friendly CORS | 多开放 | 大批量限速；`www.ngs.noaa.gov/CORS/` 同源入口 |
| **GeoNet NZ** | [说明](https://www.geonet.org.nz/data/types/geodetic) · [API](https://data.geonet.org.nz/) | RINEX：`/v1/data/gnss/rinex/`（另有 1 Hz） | 开放；读 Data Policy | 旧兼容端点计划 2026 年底退役；脚本迁 `/v1/data/` |
| **IBGE RBMC** | [geoftp RBMC](https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/) · [API 文档](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1) | geoftp 目录或 API `rinex2`/`rinex3`/1 s | API 文档公开 | 礼貌限速；端点以文档版本为准 |
| **EarthScope** | [GAGE archive](https://gage-data.earthscope.org/archive/gnss) · [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk) | 归档常跳登录；SDK（PyPI）拉 API | EarthScope / GAGE 账号 | 原 UNAVCO 页仍可开，新工作以 GAGE + SDK 为准 |
| **CDAAC** | [cdaac-www.cosmic.ucar.edu](https://cdaac-www.cosmic.ucar.edu/) | 注册后下 ionPhs / ionPrf 等 | CDAAC 账号 | 电离层 excess phase / Ne 剖面 |
| **ROM SAF** | [rom-saf.eumetsat.int](https://rom-saf.eumetsat.int/) | 产品与 [ROPP](https://rom-saf.eumetsat.int/ropp/) | 多需注册 | 处理包与产品页面分开找 |
| **AWS GNSS-RO** | [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | `pip install awsgnssroutils` 查/下多中心 Level-1b/2 | 开放（AWS 公开桶） | `registry.opendata.aws/gnss*` 深链常 404；以工具与仓库说明为准 |
| **VMF** | [vmf.geo.tuwien.ac.at](https://vmf.geo.tuwien.ac.at/) | [`trop_products/`](https://vmf.geo.tuwien.ac.at/trop_products/) | 多开放 | 选对 VMF1/VMF3 与气象模型 |
| **GIRO / DIDBase** | [giro.uml.edu/didbase](https://giro.uml.edu/didbase/) | 查询站/时段 → 下载测高仪图 | 网页注册 | 旧 quick-request URL 已 404；与 GNSS TEC 对齐时间与穿透点 |
| **Kyoto WDC** | [wdc.kugi.kyoto-u.ac.jp](https://wdc.kugi.kyoto-u.ac.jp/) | Kp / Dst 等指数页 | 多开放 | 批量遵守礼貌访问 |
| **INTERMAGNET** | [intermagnet.org](https://www.intermagnet.org/) | Data 页 → 准实时/存档 | 视产品 | 先读条件再脚本抓 |
| **SuperMAG** | [supermag.jhuapl.edu](https://supermag.jhuapl.edu/) | 注册后按界面 / API | 网页注册 | 引用含原始台站 |
| **SWPC** | [swpc.noaa.gov](https://www.swpc.noaa.gov/) · [spaceweather.gov](https://www.spaceweather.gov/) | Products（K 指数、GloTEC 等） | 开放 | `spaceweather.noaa.gov` 不可靠；勿与 GFZ Kp 混用不标注来源 |
| **ISMR** | [Query Tool](https://ismrquerytool.fct.unesp.br/) | 网页查询；或 [`ismr_downloader`](https://github.com/GEGE-UNESP/ismr_downloader) | 网页注册 | 站点偶发超时/证书问题；打不开时优先脚本条目 |

## 相关教程与软件

下完数据后常接：

| 目标 | 去哪 |
|---|---|
| 双频 STEC / 一日练习 | [02](./tutorials/02-gnss-dualfreq-tec.md) · [16](./tutorials/16-practice-one-day-tec.md) |
| 读 GIM / IONEX | [03](./tutorials/03-gim-ionex.md) · [ionex-gim](./software/ionex-gim.md) |
| 目录怎么用 | [08](./tutorials/08-how-to-use-this-catalog.md) |
| RINEX 读盘 / QC | [georinex](./software/georinex.md) · [anubis](./software/anubis.md) |
| 软件短文总索引 | [software/README](./software/README.md) · [tutorials/README](./tutorials/README.md) |
