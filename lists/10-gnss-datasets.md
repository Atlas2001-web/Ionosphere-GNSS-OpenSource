# GNSS 数据源 / GNSS Datasets

[![68](https://img.shields.io/badge/portals-68-teal.svg)](../PROJECTS.json) · RINEX · SP3/CLK · IONEX · CORS · 实时流

> 怎么下？→ [`docs/data-access.md`](../docs/data-access.md) · 表内含**注册方式** · 🏷️ 多为官方门户

## CORS区域网

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss) | EarthScope GAGE GNSS 归档：北美及合作站观测数据 | 网页注册 | 🏷️ 官方 核心 精选 |
| [EarthScope-Home](https://www.earthscope.org/) | EarthScope 主页：原 UNAVCO/IRIS 合并后的地球科学联盟入口 | 开放下载 | 🏷️ 官方 |
| [EUREF-EPN-CB](https://www.epncb.oma.be/) | EUREF EPN 中央局：欧洲参考站网数据与产品 | 开放下载 | 🏷️ 官方 核心 精选 |
| [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/) | EPN 观测数据 FTP/Web 目录 | 开放下载 | 🏷️ 官方 |
| [GA-GNSS-Data](https://data.gnss.ga.gov.au/) | Geoscience Australia GNSS 数据门户（AUSCORS 等） | 开放下载 | 🏷️ 官方 核心 精选 |
| [HongKong-SatRef](https://www.geodetic.gov.hk/en/satref/satref.htm) | 香港 SatRef：卫星定位参考站网介绍 | 开放下载 | 🏷️ 官方 |
| [HongKong-SatRef-RINEX](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 香港 SatRef RINEX 数据说明与下载 | 开放下载 | 🏷️ 官方 |
| [IGN-Geodesie](https://geodesie.ign.fr/) | 法国 IGN 大地测量门户（RGP 等相关入口） | 开放下载 | 🏷️ 官方 |
| [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/) | NOAA CORS 数据目录树 | 开放下载 | 🏷️ 官方 |
| [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/) | NOAA NGS CORS：美国连续运行参考站网数据门户 | 开放下载 | 🏷️ 官方 核心 精选 |
| [SIRGAS-Home](https://www.sirgas.org/en/) | SIRGAS：拉丁美洲大地参考架与 GNSS 网门户 | 开放下载 | 🏷️ 官方 |
| [SONEL](https://www.sonel.org/) | SONEL：全球海平面观测网（含 GNSS 并址站） | 开放下载 | 🏷️ 官方 |
| [UNAVCO-GPS-GNSS-Data](https://www.unavco.org/data/gps-gnss/gps-gnss.html) | UNAVCO 遗留 GNSS 数据页（导向 EarthScope/GAGE） | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 打开归档后按提示创建或登录 EarthScope/GAGE 账号；部分公开子集可直接浏览，批量接口以站内说明为准。

GAGE 数据系统上的 GNSS 归档入口，承接原 UNAVCO 测站 RINEX 等产品，广泛用于构造、火山、水文与电离层研究。北美及合作网密度高、时间跨度长。登录与接口策略可能调整，编写脚本前应用浏览器确认当前权限模型与路径。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EarthScope-Home](https://www.earthscope.org/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 机构主页公开。数据下载转入 GAGE/EarthScope 数据系统，按目标集合可能要求免费账号。

EarthScope 联盟门户，汇总地球物理与大地测量设施、项目与数据政策信息。具体 GNSS 文件检索在 GAGE 数据系统完成。历史上 UNAVCO 品牌页面多会重定向到此处。寻找 RINEX 时请优先使用 gage-data.earthscope.org 归档链接。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [EUREF-EPN-CB](https://www.epncb.oma.be/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** EPN 中央局网站公开。观测数据多经公开 FTP/HTTPS 目录；实时流另见 EUREF-IP，可能需 NTRIP 账号。

欧洲 EPN 中央局官方门户，提供测站信息、观测文件与产品相关入口，是欧洲大地参考框架网的核心数据枢纽。适合区域 PPP、形变与电离层研究。实时流与事后文件渠道分离；使用高采样数据时注意存储容量并遵循 EPN 引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 观测 FTP/HTTPS 镜像目录通常匿名可读；请温和限速，勿独占连接。

EPN 测站观测文件目录，便于按站名直接下载 RINEX，是欧洲区域研究的高频访问路径。目录组织相对稳定，但测站列表会增减。批量下载前应对照中央局站点状态页，剔除长期停测或仅测试用途的测站。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GA-GNSS-Data](https://data.gnss.ga.gov.au/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** Geoscience Australia GNSS 数据门户公开检索下载；若个别 API 需密钥，按站内开发者说明申请。

澳大利亚地球科学局 GNSS 数据服务，覆盖澳新等区域参考站观测与相关产品的检索下载，是亚太用户重要区域网来源。旧版 ga.gov.au 深链可能失效，请优先使用本数据域名与官方 API 文档，并关注站网元数据更新。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [HongKong-SatRef](https://www.geodetic.gov.hk/en/satref/satref.htm)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** SatRef 介绍页公开；RINEX 下载见站内 RINEX 链接，按地政总署现行开放政策获取。

香港地政总署卫星定位参考站网说明页，属于高密度城市 CORS 的典型代表，适合华南与香港本地增强、教学及城市电离层个例。实时播发与事后 RINEX 渠道通常不同；投入商用或再分发前请阅读官方使用条款。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [HongKong-SatRef-RINEX](https://www.geodetic.gov.hk/en/rinex/rinex.htm)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** RINEX 说明与下载入口公开，按页面指示获取；若改用专用域名以跳转后站点为准。

说明如何获取 SatRef 事后 RINEX 观测数据，是区域电离层与对流层案例研究的便捷来源。需注意采样率、文件保留期限与站名规则。若进行大量自动下载，应遵守网站礼貌访问规范并优先在本地缓存。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGN-Geodesie](https://geodesie.ign.fr/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 大地测量门户公开。法国 CORS/RGP 等数据下载入口以站内现行链接为准，部分服务需账号。

法国国家地理与森林信息研究所大地测量站点，导向国家 GNSS 连续运行网与产品信息，可作为欧洲区域网的补充数据源。历史上 IGS 数据中心 FTP 主机可能不稳定，获取文件时优先使用本页给出的当前方式与镜像说明。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 数据树一般可直接 HTTPS 访问拉取公开 RINEX；若返回错误码，改用 CORS 主站工具。

CORS 观测文件目录树入口，便于按测站、年份与年积日批量抓取公开 RINEX。面向自动化流水线。请控制并发与请求频率，遵守 NOAA 使用政策，并在本地做好缓存与校验，以免重复冲击服务器。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 门户与多数观测文件可公开获取；使用 CORS 数据探索/批量工具时按 NOAA 提示，一般无需审批。

美国国家大地测量局 CORS 官方入口，提供测站元数据、RINEX 观测与相关产品链接，是北美高精度定位与电离层研究常用网络。站点数量多、跨度长。处理前务必核对天线变更日志与站点活跃状态，避免使用已关闭测站而未更新元数据。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [SIRGAS-Home](https://www.sirgas.org/en/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** SIRGAS 官网公开。成员国站数据获取方式各异，按站内 Data/Products 或国家中心链接申请。

SIRGAS 官方网站介绍拉丁美洲及周边大地参考框架与 GNSS 站网组织方式，是该区域地壳运动与电离层研究的入口级资源。具体 RINEX 往往分散在各成员国数据中心，需要从本站再跳转，并分别遵守各国获取规则。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [SONEL](https://www.sonel.org/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** SONEL 门户公开；潮位/GNSS 共存站数据按数据集页面获取，部分需注册。

全球海平面观测组织门户，许多验潮站与 GNSS 并址，服务于海洋大地测量、垂直基准与海平面变化研究。数据偏沿海场景。GNSS 文件有时并不直接托管，而是链到各国 CORS 或数据中心，需要二次跳转并分别注册。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [UNAVCO-GPS-GNSS-Data](https://www.unavco.org/data/gps-gnss/gps-gnss.html)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 遗留说明页可公开访问，常重定向或链到 EarthScope 数据系统；按新门户完成注册后下载。

原 UNAVCO 的 GPS/GNSS 数据说明页，主要用于旧文档与书签兼容，并导向 EarthScope/GAGE 新流程。新的数据工作应以 EarthScope 归档为准。若遇到失效深链，请改用 gage-data.earthscope.org。TEQC 等软件说明仍可能保留在 unavco 域名下。

## GNSS掩星/RO

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | AWS 开放数据 GNSS 掩星元数据查询与下载工具（含电离层产品入口） | 未确认 | 🏷️ 高校实验室 |

### 详细说明

#### [awsgnssroutils](https://github.com/gnss-ro/aws-opendata)  
*🏷️ 高校实验室*

注册：`unknown`（未确认） · 宿主：github · 来源：academic_lab

面向 AWS Registry of Open Data 上的 GNSS 无线电掩星库：提供 awsgnssroutils 查询/筛选/下载接口，覆盖 CDAAC、JPL、ROM SAF 等多处理中心的 Level-1b/2 产品。做 COSMIC/COSMIC-2 电离层 excess phase、电子密度剖面或与辐射探测共址研究时很省事。仓库体量大、含重整格式流水线；日常用 pip 装 awsgnssroutils 即可，不必整仓克隆。

## IGS产品下载

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [CODE-AIUB-Product-Download](https://www.aiub.unibe.ch/download/) | AIUB/CODE 产品 HTTPS 下载浏览器（含 CODE/ionex/ionosphere 等目录） | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [CODE-AIUB-Product-Download](https://www.aiub.unibe.ch/download/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** HTTPS 文件浏览器公开，可按目录逐文件下载；原 FTP 已停用，无需账号。

伯尔尼大学天文研究所 CODE 分析中心的官方产品文件浏览器。可进入 CODE、CODE_MGEX、ionex、ionosphere 等目录获取最终/快速/超快速轨道钟差与 IONEX 等。FTP 已弃用，请改用本 HTTPS 入口；与已收录的 CODE AC 介绍页互补，本条聚焦可下载产品树。

## IGS综合

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [BKG-IGS-Data-Center](https://igs.bkg.bund.de/) | BKG IGS 数据中心：欧洲侧 GNSS 数据与 NTRIP 入口 | 开放下载 | 🏷️ 官方 核心 精选 |
| [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/) | NASA CDDIS：IGS 全球 GNSS 观测与产品主归档之一 | 网页注册 | 🏷️ 官方 核心 精选 |
| [CDDIS-Highrate-GNSS](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) | CDDIS 高采样 GNSS 数据说明 | 网页注册 | 🏷️ 官方 |
| [ESA-GSSC](https://gssc.esa.int/) | ESA GNSS Science Support Centre：科学数据与产品门户 | 网页注册 | 🏷️ 官方 核心 精选 |
| [GFZ-ISDC](https://isdc.gfz-potsdam.de/) | GFZ ISDC：波茨坦地球科学研究数据中心门户 | 网页注册 | 🏷️ 官方 |
| [IGS-Data-Access](https://igs.org/data-access/) | IGS 数据访问页：全球数据中心与获取方式一览 | 开放下载 | 🏷️ 官方 |
| [IGS-Files-CDN](https://files.igs.org/) | IGS files.igs.org 文件分发入口 | 开放下载 | 🏷️ 官方 核心 精选 |
| [IGS-Home](https://igs.org/) | 国际 GNSS 服务（IGS）官网：产品、工作组与数据中心总入口 | 开放下载 | 🏷️ 官方 核心 精选 |
| [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/) | NASA Earthdata 统一登录：CDDIS 等地球科学数据下载的前置账号 | 网页注册 | 🏷️ 官方 核心 精选 |
| [SOPAC-CSRC](https://sopac-csrc.ucsd.edu/) | SOPAC/CSRC：Scripps 轨道与永久阵列中心门户 | 开放下载 | 🏷️ 官方 |
| [SOPAC-Garner-Pub](https://garner.ucsd.edu/pub/) | SOPAC garner 公共目录：产品与相关文件树 | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [BKG-IGS-Data-Center](https://igs.bkg.bund.de/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 门户公开。文件与 NTRIP 服务按子页说明；实时挂载点账号或访问策略以 BKG Ntrip 页面为准。

德国联邦制图与大地测量局维护的 IGS 数据中心门户，同时提供文件下载与实时播发相关入口，是欧洲用户常用镜像与 caster 起点。实时 NTRIP 与事后文件通道彼此独立，配置账号时不要把 caster 凭证与 HTTPS 下载混用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 先注册 Earthdata，再打开本归档目录并授权 CDDIS。批量可用 https 或 ftps://gdc.cddis.eosdis.nasa.gov/，凭证即 Earthdata 账号。

IGS 核心数据中心，提供日/小时 RINEX、广播星历、精密 SP3/CLK、IONEX 与偏差等产品。目录按年积日或 GPS 周组织，文件多为压缩格式。适合全球网事后处理与电离层研究。匿名 FTP 已停用，必须 Earthdata 登录；大流量请限速，并核对长文件名规范与校验信息。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-Highrate-GNSS](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html)  
*🏷️ 官方*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 说明页公开可读；下载归档文件需 NASA Earthdata 账号并授权 CDDIS。

NASA CDDIS 对高采样率（high-rate）GNSS 观测产品的官方说明页，解释目录组织与用途，是闪烁/同震等高频应用找数据的路标。下载实体文件仍走 CDDIS 归档并需 Earthdata；可与 cddis-highrate-downloader 软件条目搭配。

#### [ESA-GSSC](https://gssc.esa.int/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 访问门户后按提示注册 ESA GSSC 账号；部分数据集需在用户中心额外申请权限再下载。

欧空局 GNSS 科学支持中心，提供面向科研的 GNSS 数据与产品检索下载，并镜像部分 IGS 内容。适合已有欧洲科研账号体系的用户。权限通常分层，登录后仍可能对部分集合只读或需追加申请；请遵守 ESA 数据政策与引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-ISDC](https://isdc.gfz-potsdam.de/)  
*🏷️ 官方*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 在 ISDC 注册科学用户账号，审核或激活后按数据集页面申请下载权限。

亥姆霍兹德国地学研究中心综合科学数据中心，提供 GNSS 及多种地球物理产品的统一检索入口。欧洲大地测量与重力/GNSS 组合研究常用。完成注册后仍需按具体集合申请授权，并非所有子库都对个人用户立即完全开放。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-Data-Access](https://igs.org/data-access/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 页面公开。列出各全球/区域数据中心链接；各中心自身可能要求 Earthdata 或其他账号。

集中列出 IGS 各数据中心镜像地址与访问提示，方便按网络条件选择就近源。本页不托管观测文件本体。各中心登录门槛不同，例如 CDDIS 需要 Earthdata。镜像同步偶有延迟，关键周产品可在两个中心交叉校验大小与时间戳。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-Files-CDN](https://files.igs.org/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** HTTPS 目录通常可直接浏览/下载；若遇限流或变更，改走 IGS Data Access 列出的各数据中心。

IGS 提供的 files.igs.org 文件分发入口，常用于获取站点日志、天线、产品列表或镜像文件树，是对 CDDIS/BKG 等归档的补充入口。目录结构会调整，下载前对照 IGS Data Access 说明；大文件请限速并校验。

#### [IGS-Home](https://igs.org/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 网站公开浏览。具体数据下载跳转到各数据中心；部分工作组邮件列表需另行订阅。

IGS 官方门户，链向产品规范、分析中心、全球/区域数据中心以及实时服务说明。站点本身通常不直接托管海量 RINEX。适合查阅标准文件名、站点日志格式与政策文件。实际观测与产品下载请转到 CDDIS、BKG、ESA GSSC 等归档系统。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 在 Earthdata Login 用邮箱自助注册并完成验证。首次访问 CDDIS 等受保护应用时，用同一账号登录并点击授权。

NASA 地球科学数据统一身份入口。下载 CDDIS GNSS 观测与产品前需先在此注册免费账号，浏览器与脚本（常配 .netrc）均可使用。本站不存储 GNSS 文件，只负责认证与应用授权；请按提示勾选 CDDIS 等应用。注意保管密码与令牌，切勿写入公开仓库或日志。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [SOPAC-CSRC](https://sopac-csrc.ucsd.edu/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 主页公开。数据产品多经 garner.ucsd.edu 等路径提供；按站内 Data 链接访问，若需账号依提示注册。

加州大学圣地亚哥分校 SOPAC 门户，历史上长期作为 IGS 数据中心之一，提供轨道产品与永久阵列相关服务入口。适合查找 SOPAC 特色产品与工具。部分古老 FTP 主机名已变更，应优先采用本页当前链接及 garner 公共目录。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [SOPAC-Garner-Pub](https://garner.ucsd.edu/pub/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 公共目录通常可直接浏览下载；若部分子树受限，回到 SOPAC 主页查看替代获取方式。

SOPAC 侧公开文件树，常包含产品文件与辅助资料，可作为 CDDIS 之外的对照镜像。目录权限与层级会随运维调整。对关键 GPS 周产品，建议与另一 IGS 数据中心交叉检查文件大小、修改时间与校验结果。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## NTRIP服务商/CRS

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [ntrip-catalog](https://github.com/Pix4D/ntrip-catalog) | Pix4D 开源 NTRIP 服务商目录（含坐标参考系 CRS 元数据，CC0） | 未确认 | 🏷️ 个人社区 |

### 详细说明

#### [ntrip-catalog](https://github.com/Pix4D/ntrip-catalog)  
*🏷️ 个人社区*

注册：`unknown`（未确认） · 宿主：github · 来源：personal_community

以 JSON 维护多家 NTRIP 服务的挂载点与 CRS 信息，站点 ntrip-catalog.org 提供检索。解决 RTCM/NTRIP 握手不携带参考框架信息的问题，便于应用按位置匹配改正坐标系。属开放数据目录而非 caster 实现；条目完整性依赖社区贡献与服务商变更。

## PPP-B2b数据

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [BDS-3-PPP-B2b-DATA](https://github.com/zp-9696/BDS-3-PPP-B2b-DATA) | 公开一周 BDS-3 PPP-B2b 试验数据 | 未确认 | 🏷️ 个人社区 |

### 详细说明

#### [BDS-3-PPP-B2b-DATA](https://github.com/zp-9696/BDS-3-PPP-B2b-DATA)  
*🏷️ 个人社区*

注册：`unknown`（未确认） · 宿主：github · 来源：personal_community

公开约一周的 BDS-3 PPP-B2b 相关数据，方便复现解码与定位试验。适合写论文或调试 B2bLIB/RTKLIB-B2b 时当标准输入。不是通用数据中心；长期业务请接 IGS/CDDIS 或自建接收。

## PPP/PPP-RTK样例

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [cssrlib-data](https://github.com/hirokawa/cssrlib-data) | CSSRlib 配套样例脚本与数据集 | 未确认 | 🏷️ 高校实验室 |

### 详细说明

#### [cssrlib-data](https://github.com/hirokawa/cssrlib-data)  
*🏷️ 高校实验室*

注册：`unknown`（未确认） · 宿主：github · 来源：academic_lab

为 CSSRlib 提供样例脚本与试验观测/改正数据，方便本地或 Colab 复现 CLAS、HAS、BDS PPP 等开放服务流程。适合跟着官方教程跑通改正接入与定位。不是长期产品归档；业务数据请接 IGS 或各服务官方中心，并注意样例时段与电文版本。

## 偏差产品

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [CAS-BDsmart-Pub](https://data.bdsmart.cn/pub/) | CAS 数据发布根：DCB/GIM/SSR 等相关产品入口 | 开放下载 | 🏷️ 官方 |
| [CSNO-TARC](https://www.csno-tarc.cn/) | 中国卫星导航系统管理办公室测试评估研究中心（TARC） | 开放下载 | 🏷️ 官方 |
| [CSNO-TARC-Differential](https://www.csno-tarc.cn/en/data/differential) | TARC 差分数据英文页 | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [CAS-BDsmart-Pub](https://data.bdsmart.cn/pub/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 公共根目录可浏览 bias/iono 等子树，一般无需账号即可拉取已公开产品。

中科院相关 GNSS 产品的 HTTPS 发布根目录，常见子树包括多星座码偏差、全球电离层图以及实时 SSR 转存等。适合把偏差与 GIM 放在同一流水线下载。具体子目录以站点为准；论文引用请标明 CAS 产品标识、日期与文件长名。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CSNO-TARC](https://www.csno-tarc.cn/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 测试评估门户公开浏览；部分精密产品或差分数据子页可能需注册，按页面按钮操作。

北斗及相关 GNSS 服务的测试评估门户，发布性能监测、差分信息等入口，中文北斗应用与服务监测场景常用。公开浏览内容与需申请下载的内容可能并存。再分发或商用前应阅读版权条款；涉及合作网数据时以站内最新公告为准，勿臆造未公开接口。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [CSNO-TARC-Differential](https://www.csno-tarc.cn/en/data/differential)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 差分/相关数据英文页可公开访问；若下载按钮要求登录，按站内注册后重试。

TARC 面向国际用户的差分与相关数据说明页面，便于获取北斗监测类产品线索。页面内容会随服务更新。其产品体系与 IGS 码偏差/OSB 并不完全等同，若与 IGS 产品融合使用，必须注意信号定义、基准与时间系统差异。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 区域CORS

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [GeoNet-NZ-Geodetic](https://www.geonet.org.nz/data/types/geodetic) | 新西兰 GeoNet 大地测量/GNSS 数据 | 开放下载 | 🏷️ 官方 |
| [IBGE-RBMC](https://www.ibge.gov.br/en/geosciences/geodetic-network/2421-rbmc.html) | 巴西 IBGE RBMC 连续 GNSS 网 | 网页注册 | 🏷️ 官方 |

### 详细说明

#### [GeoNet-NZ-Geodetic](https://www.geonet.org.nz/data/types/geodetic)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 说明页公开；按子链进入具体 GNSS 产品目录下载，遵守 GeoNet 许可与署名要求。

GeoNet 大地测量数据说明入口，链向新西兰 GNSS 等产品的获取方式，是西南太平洋区域研究常用门户。具体 RINEX/产品树以其子链为准；使用请遵守 GeoNet 数据许可。

#### [IBGE-RBMC](https://www.ibge.gov.br/en/geosciences/geodetic-network/2421-rbmc.html)  
*🏷️ 官方*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 阅读 RBMC 页后的下载/服务链接；多数产品需在 IBGE 相关系统注册后获取，以站点当前流程为准。

巴西国家地理统计局 RBMC 连续监测网介绍页，是获取巴西 CORS/RINEX 的官方入口之一。南美电离层与低纬闪烁研究常用。实际文件下载常转到 IBGE 数据服务子站，请按页面当前链接注册或检索。

## 地磁空间天气

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [BoM-SWS](https://www.sws.bom.gov.au/) | 澳大利亚 BoM 空间天气服务（SWS） | 开放下载 | 🏷️ 官方 |
| [CelesTrak-SpaceData](https://celestrak.org/SpaceData/) | CelesTrak SpaceData：空间天气与相关辅助数据镜像 | 开放下载 | 🏷️ 官方 |
| [GFZ-Kp-Index](https://kp.gfz-potsdam.de/en/) | GFZ Kp 地磁指数官方发布 | 开放下载 | 🏷️ 官方 |
| [GIRO-DIDBase](https://giro.uml.edu/didbase/) | GIRO DIDBase：全球电离层测高仪数据库 | 网页注册 | 🏷️ 官方 核心 精选 |
| [NASA-OMNIWeb](https://omniweb.gsfc.nasa.gov/) | NASA OMNIWeb：太阳风与地磁指数多源合并数据 | 开放下载 | 🏷️ 官方 |
| [NASA-SPDF](https://spdf.gsfc.nasa.gov/) | NASA SPDF：空间物理数据设施总入口 | 开放下载 | 🏷️ 官方 |
| [NOAA-SWPC](https://www.swpc.noaa.gov/) | NOAA 空间天气预测中心（SWPC） | 开放下载 | 🏷️ 官方 |
| [NOAA-SWPC-Planetary-K](https://www.swpc.noaa.gov/products/planetary-k-index) | NOAA SWPC 行星 K 指数产品 | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [BoM-SWS](https://www.sws.bom.gov.au/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 澳大利亚空间天气服务站公开浏览；部分区域电离层图/预报可直接查看，深度存档按页内说明。

澳大利亚气象局空间天气服务网站，提供电离层状态、高频传播与相关预报产品，对亚太地区 GNSS 用户具有区域参考价值。产品更新频率不一。若需自动抓取，请遵守站点条款，优先使用其标明的数据服务而不是裸爬页面。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [CelesTrak-SpaceData](https://celestrak.org/SpaceData/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 空间数据镜像区公开下载，无需账号。

CelesTrak 提供的空间天气及相关辅助数据集合，方便与卫星轨道、可见性工具链衔接使用。它不是 IGS 官方数据中心。关键地磁或太阳指数建议同时对照 NOAA、GFZ 等一手发布源，以免镜像更新延迟影响事件分析。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-Kp-Index](https://kp.gfz-potsdam.de/en/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** Kp 指数页面与数据接口通常公开，可直接下载或调用，无需账号。

GFZ 官方发布的行星 Kp 等地磁活动指数，是空间天气研究以及 GNSS 闪烁、ROTI 扰动分析中常用的外部驱动参数，通常开放获取。使用时注意时间分辨率以及确定值与预报值的区别，论文中应明确写出来源机构与产品版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GIRO-DIDBase](https://giro.uml.edu/didbase/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 在 GIRO/DIDBase 按提示注册科研账号，验证后查询下载测高仪图与参数；详细步骤以 UML 门户为准。

麻省大学洛厄尔分校维护的测高仪观测数据库入口，提供虚高图与临界频率等特性参数，常与 GNSS TEC 及 IRTAM 同化产品对照。空间天气与模型验证常用。一般需要注册；请按站内要求引用，并留意测站时间覆盖可能存在空洞。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NASA-OMNIWeb](https://omniweb.gsfc.nasa.gov/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** OMNIWeb 查询界面公开，按表单选择参数与时段生成下载，通常无需登录。

NASA/GSFC 的 OMNIWeb 接口提供太阳风等离子体、行星际磁场与地磁指数等合并时间序列，广泛用于 GNSS 相关空间天气统计分析。通过网页表单交互取数。若需要高时间分辨率，请正确选择 OMNI 高分辨或低分辨数据集。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NASA-SPDF](https://spdf.gsfc.nasa.gov/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** SPDF 门户公开；多数太阳层/磁层数据可匿名下载，少数集合按页内说明注册。

NASA 空间物理数据设施总入口，托管太阳风、磁层与相关日地物理数据，可与 GNSS 电离层扰动机制研究结合。门类非常广泛。使用具体任务数据时请遵循页面给出的 DOI 与致谢（acknowledge）要求，便于结果可复现。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-SWPC](https://www.swpc.noaa.gov/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 预报与产品公开浏览下载，一般无需注册。

美国 NOAA 空间天气预测中心门户，提供耀斑、质子事件、地磁活动等业务产品，常用来解释 GNSS 定位异常与电离层扰动时段。实时导向强。科研归档时应保存所用产品副本，并注意业务产品可能事后修订。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-SWPC-Planetary-K](https://www.swpc.noaa.gov/products/planetary-k-index)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 行星 K 指数产品页公开，图表与数据文件可直接取用。

SWPC 发布的行星 K 指数产品页，便于把地磁活动快速叠加到 GNSS ROTI 或闪烁时间轴上做事件分析。与 GFZ Kp 密切相关但发布节奏与文件格式可能不同，对比研究时必须分别注明来源，避免混用造成时间轴错位。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 实时流

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [IGS-RTS](https://igs.org/rts/) | IGS 实时服务（RTS）：实时轨道钟差/SSR 流说明 | 开放下载 | 🏷️ 官方 核心 精选 |

### 详细说明

#### [IGS-RTS](https://igs.org/rts/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 说明公开。接入实时流需配置 NTRIP 客户端，并按各 caster 要求申请挂载点或账号。

说明 IGS 实时轨道钟差及 SSR 播发框架、参与分析中心与应用场景，面向实时 PPP 与完整性监测。本页通常不直接推送数据流，需经 BKG 等 NTRIP caster 接入。流可用性与消息版本会更新，上线前应核对挂载点表和解码库兼容性。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## 对流层

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/) | TU Wien VMF 对流层格网数据目录（与 /codes 源码区分） | 开放下载 | 🏷️ 官方 核心 精选 |

### 详细说明

#### [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 对流层格网产品目录通常可直接下载；若某预报子集要求注册，按 TU Wien 站点提示填写后再取。

维也纳工大 VMF 服务的对流层产品目录树，提供 VMF1/VMF3 等格网，供 PPP 与 VLBI 映射函数使用。本条强调数据产品，源码实现见同站 /codes（软件类另收）。选用时注意格网版本与气象模型匹配；业务系统还需确认更新节奏与文献引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## 掩星

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/) | COSMIC CDAAC：GNSS 无线电掩星大气/电离层产品 | 网页注册 | 🏷️ 官方 核心 精选 |
| [COSMIC-GNSS-RO-Data](https://data.cosmic.ucar.edu/gnss-ro/) | COSMIC GNSS-RO 公开数据目录 | 开放下载 | 🏷️ 官方 |

### 详细说明

#### [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 在 CDAAC 站点注册用户，验证邮箱后登录下载掩星产品；部分集合也可经 Earthdata 相关入口获取。

COSMIC/FORMOSAT 等任务的无线电掩星数据中心门户，提供中性大气与电离层电子密度廓线等产品，常与地基 GNSS TEC 联合分析。空间天气与气象交叉研究几乎必用。注册通常免费，但须遵守引用与使用协议；不同处理级别不可混用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [COSMIC-GNSS-RO-Data](https://data.cosmic.ucar.edu/gnss-ro/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 公开数据树，多数文件可直接拉取；若个别路径要求认证，改回 CDAAC 登录通道。

面向 GNSS 无线电掩星的公开数据目录树，便于使用直链或镜像方式批量拉取文件，适合流水线化预处理。目录层级会随任务与版本变化，下载脚本应用清单或校验和验证完整性，避免漏文件或版本混杂。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 电离层产品

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/) | 中科院 CAS 电离层 IONEX 产品（data.bdsmart.cn） | 开放下载 | 🏷️ 官方 核心 精选 |
| [CAS-BDsmart-RTS-Iono](https://data.bdsmart.cn/pub/product/rts/iono/) | 中科院 BDsmart 实时电离层产品目录（RTS IONEX 等） | 开放下载 | 🏷️ 官方 |
| [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html) | CDDIS 大气产品页：电离层 IONEX 与对流层产品索引说明 | 开放下载 | 🏷️ 官方 |
| [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/) | CDDIS IONEX 目录：IGS 及各分析中心全球电离层图 | 网页注册 | 🏷️ 官方 核心 精选 |
| [CNES-PPP-WIZARD-Realtime-Products](http://www.ppp-wizard.net/products/REAL_TIME) | CNES PPP-WIZARD 实时产品目录（含实时轨道钟差/偏差及电离层相关输出） | 开放下载 | 🏷️ 官方 |
| [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) | INGV eSWua 数据库：地中海/欧洲/全球 TEC 现报与预报产品入口 | 开放下载 | 🏷️ 官方 核心 精选 |
| [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/) | IGS 电离层工作组：GIM/IAAC 与产品活动入口 | 开放下载 | 🏷️ 官方 |
| [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 意大利 INGV 基于 RING 网的实时 TEC 监测与地图发布页 | 开放下载 | 🏷️ 官方 核心 精选 |
| [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/) | JPL 快速 IONEX 发布目录：日更新全球电离层图 | 开放下载 | 🏷️ 官方 核心 精选 |
| [UPC-gAGE-FastPPP-Products](https://gage.upc.edu/en/gage-products/fast-ppp-products) | UPC gAGE Fast-PPP 产品页：STEC/IONEX/钟差等申请说明 | 邮件申请 | 🏷️ 高校实验室 |
| [UPC-IONEX-Archive](https://cabrera.upc.edu/upc_ionex_GPSonly-RINEXv3/) | UPC 电离层 IONEX 归档目录（分年） | 开放下载 | 🏷️ 高校实验室 |
| [UPC-IONO4HAS-Products](https://server.gage.upc.edu/iono4has/products.html) | UPC IONO4HAS：面向 HAS 的电离层产品状态页 | 开放下载 | 🏷️ 高校实验室 |
| [WHU-IGS-Ionosphere-AC](https://panda.whu.edu.cn/yjpt/IGSdlcfxzx.htm) | 武汉大学 IGS 电离层分析中心：GIM/DCB/ROTI 产品说明 | 开放下载 | 🏷️ 高校实验室 核心 精选 |

### 详细说明

#### [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** HTTPS 公共产品区，通常可直接下载 CAS GIM；若个别子目录受限，从 pub 根目录逐级进入。

中国科学院相关团队发布的多 GNSS GIM HTTPS 目录，用于接替旧 FTP，提供快速与最终等 IONEX 产品。东亚与全球电离层研究常用来源之一。同步到 IGS 数据中心可能存在时延差；请将脚本迁移到新域名，勿再依赖已宣布停用的旧 FTP。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CAS-BDsmart-RTS-Iono](https://data.bdsmart.cn/pub/product/rts/iono/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 公开 HTTP 目录，通常无需注册即可列举/下载实时电离层产品。

与已收录的 CAS 最终/快速 IONEX 目录配套的实时（RTS）电离层产品树，面向近实时 GIM/SSR 相关用户。适合 PPP-RTK/实时监测试验；事后精密分析仍建议使用最终 IONEX 与多 AC 交叉验证。

#### [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 说明页公开可读；下载对应 ionex/trop 等目录文件时需 Earthdata 授权。

汇总 IGS 电离层 GIM（IONEX）与对流层相关产品在 CDDIS 的存放说明，并解释新旧文件名对应关系。面向 TEC/ZTD 用户快速定位路径。实际数据文件仍在 archive 树中按日或周存放。Rapid 与 Final 时延不同，引用时应注明分析中心与产品类型。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/)  
*🏷️ 官方 核心 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** Earthdata 登录并授权 CDDIS 后，按年/年积日目录下载 IONEX（.INX/.Z/.gz）。

存放 IGS 综合与各电离层分析中心的 GIM、ROTI 等 IONEX 文件，按年份与年积日组织。是 GNSS 电离层事后研究最常用入口之一。下载需登录；注意 Final、Rapid 与预测产品的时延及格网分辨率差异，并结合码偏差/OSB 产品一起使用以免系统差。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CNES-PPP-WIZARD-Realtime-Products](http://www.ppp-wizard.net/products/REAL_TIME)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 产品目录公开可浏览下载；使用请遵循 CNES PPP-WIZARD 站点说明。

CNES PPP-WIZARD 示范系统的 REAL_TIME 产品树，可检索实时流配套文件；CNES 亦通过 IGS-RTS 播发实时 SSR。已收录门户首页，本条补齐可枚举的实时产品路径，便于脚本对接。

#### [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 数据与 Web 服务按 eSWua 说明开放；许可 CC BY 4.0。请引用 DOI 10.13127/eswua/tec；联系 eswua@ingv.it。

INGV「电子空间天气高层大气」数据库中的 TEC 专题（DOI:10.13127/eswua/tec，CC BY 4.0）。计算中心接入 RING、EUREF 与 IGS 实时/事后观测，7×24 产出地中海、欧洲与全球 TEC 产品。地中海现报（nc_med）即 IONORING 思路的产品化：RING NTRIP 实时流、10 分钟、0.1° 网格、LOWESS、无背景模型以免抹平不规则；另有地中海 30 分钟短期预报、欧洲 TEC/梯度图、全球 NeQuick2 同化现报，以及基于自回归神经网络与预报 Kp 的 24 小时全球预报。站点提供 Download Tool、Web Service 指南与可用性地图；示例 REST 如 `http://ws-eswua.rm.ingv.it/tecdb.php/records/wsnc_med?filter=dt,eq,YYYY-MM-DD%20HH:MM:SS`，返回 JSON 网格点（lat/lon/tec）。适合需要意大利/地中海高分辨率实时 TEC 或程序化拉图的用户；不是 GNSS 原始观测归档（RING 原始站数据另循 RING/INGV 渠道）。收录前已核验落地页可访问；使用请按页面引用元数据与 CC BY 4.0。

#### [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 工作组页面公开浏览；IONEX 产品下载走 CDDIS 等数据中心。

介绍 IGS 电离层联合产品机制、各分析中心角色以及相关会议与试点活动。适合了解 CODE、JPL、UPC、CAS、WHU 等 IAAC 分工。页面不直接存储 IONEX 文件。综合产品与单中心产品在精度和时延上不同，研究中应分开评估与引用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 实时地图页公开浏览。历史网格、预报与 REST 接口见 eSWua TEC（CC BY 4.0）；引用 DOI 10.13127/eswua/tec 及 Cesaroni et al. 2021。

意大利国家地球物理与火山学研究所（INGV）上层大气物理组维护的实时电离层 TEC 监测页。系统利用 RING（Rete Integrata Nazionale GNSS）约 40 个测站的双频观测，在 IPP 上估计 VTEC 后用 LOWESS 插值，生成覆盖约 35°N–48°N、5°E–20°E 的 0.1°×0.1° 网格图，约每 10 分钟刷新，典型时延低于 1 分钟。论文（Remote Sensing 2021）与 IGS GIM、比利时 ROB 欧洲图对比，RMSE 约 2–3 TECu，并讨论了 2017 年 X9.3 耀斑与随后地磁暴期间的区域响应，以及用于单点定位改正时相对 Klobuchar/GIM 的改善。本页主要展示最新地图与近 24 小时动画，不是开源处理软件仓库；算法与产品说明见论文。批量历史产品与 Web 服务请转到同组的 eSWua TEC 数据库（DOI:10.13127/eswua/tec）。收录时已 HTTP 核验页面可访问；使用与引用请遵守 INGV/论文要求。

#### [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 目录通常可直接 HTTPS 浏览下载；若遇机构网络限制可改走 CDDIS 镜像中的 JPL 产品。

JPL 侧快速电离层图公开目录，文件为 IONEX 风格，适合需要较短时延 GIM 的科研与监测。其结果与 IGS 综合 Final 存在差异，不可直接等同。部分机构网络可能拦截 sideshow 域名；重要任务建议同时备份 CDDIS 路径中的同系列产品。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [UPC-gAGE-FastPPP-Products](https://gage.upc.edu/en/gage-products/fast-ppp-products)  
*🏷️ 高校实验室*

注册：`email_register`（邮件申请） · 宿主：official_site · 来源：academic_lab

**如何获取：** 阅读产品说明后，按页面提示向 info.gage 邮箱说明用途，获准后再访问受保护的产品服务器。

说明 Fast-PPP 相关精密产品组成，包括模糊度小数、精密 STEC、IONEX 与卫星钟差，并给出建议引用文献。面向高精度电离层与 PPP 研究用户。产品服务器通常需要邮件开通，并非完全匿名开放；获权后请遵守学术使用约定。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [UPC-IONEX-Archive](https://cabrera.upc.edu/upc_ionex_GPSonly-RINEXv3/)  
*🏷️ 高校实验室*

注册：`open`（开放下载） · 宿主：official_site · 来源：academic_lab

**如何获取：** 公开目录索引，一般可直接下载分年 IONEX；若服务器限速请错峰或改用 IGS 镜像中的 UPC 产品。

UPC 提供的分年 IONEX 归档，包含长期时间序列以及最新快速文件入口，服务 GNSS 电离层与相关高精度应用研究。适合明确需要 UPC 单中心解的用户。请与 IGS 综合产品区分使用；目录旁文档说明格式约定与处理设定，引用时写明版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [UPC-IONO4HAS-Products](https://server.gage.upc.edu/iono4has/products.html)  
*🏷️ 高校实验室*

注册：`open`（开放下载） · 宿主：official_site · 来源：academic_lab

**如何获取：** 产品状态页一般可打开；历史库与实时文件若要求登录，按页内 Archive 链接与提示注册。

展示与 Galileo HAS 相关的电离层产品链接及当日运行状态，便于开展监测与对比实验。内容偏研究原型，不宜简单等同于 IGS 标准综合 GIM。格式细节见站内说明；长期归档可能与公开 IONEX 目录并存，下载前确认许可范围。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [WHU-IGS-Ionosphere-AC](https://panda.whu.edu.cn/yjpt/IGSdlcfxzx.htm)  
*🏷️ 高校实验室 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：academic_lab

**如何获取：** 介绍页公开。页内给出 FTP 产品地址（事后/实时 IONEX、DCB、ROTI）；用 FTP 客户端按路径拉取，若主机暂不可达可改 CDDIS 镜像。

武汉大学卫星导航定位技术研究中心作为 IGS 电离层分析中心的产品介绍页，覆盖事后与实时 GIM、多系统码偏差以及 ROTI 图。对中文用户较友好。自建 FTP 主机偶发不可达时，可改用 IGS 数据中心中的 WHU 文件，并区分实时与事后时延。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## 空间天气辅助

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [INTERMAGNET](https://www.intermagnet.org/) | INTERMAGNET 全球地磁台网数据 | 网页注册 | 🏷️ 官方 |
| [Kyoto-WDC-Geomagnetism](https://wdc.kugi.kyoto-u.ac.jp/) | 京都 WDC：Kp/Dst 等地磁指数 | 开放下载 | 🏷️ 官方 核心 精选 |
| [SuperMAG](https://supermag.jhuapl.edu/) | SuperMAG 全球地磁合并数据 | 网页注册 | 🏷️ 高校实验室 |

### 详细说明

#### [INTERMAGNET](https://www.intermagnet.org/)  
*🏷️ 官方*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 按官网 Data 页面说明申请/下载；不同产品开放程度不同，请先读条件再脚本抓取。

国际实时地磁台网门户，提供参与台站的准实时与存档地磁数据入口，常与 GNSS TEC/ROTI 做空间天气对照。数据政策与台站列表以官网为准；部分产品需按说明注册或经成员机构渠道。

#### [Kyoto-WDC-Geomagnetism](https://wdc.kugi.kyoto-u.ac.jp/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 网页公开浏览与下载；部分历史产品按页面说明引用即可，批量抓取请遵守站点礼貌与条款。

京都 WDC for Geomagnetism 提供 Kp、Dst 等经典地磁指数与相关数据服务，是空间天气与电离层扰动研究的常用外部驱动入口。门户以网页/文件服务为主；下载与引用规则见站点说明。本条收录「数据怎么拿」，不是 GNSS 观测归档。

#### [SuperMAG](https://supermag.jhuapl.edu/)  
*🏷️ 高校实验室*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：academic_lab

**如何获取：** 在 SuperMAG 网站注册账号后按界面下载/API 说明使用，遵守引用与再分发条款。

JHU/APL SuperMAG 汇集全球地磁台站并提供统一坐标与多种指数/绘图服务，便于做高纬扰动与 GNSS 闪烁对照。网页注册后按条款使用；引用需遵循 SuperMAG 与原始台站要求。

## 轨道钟差

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html) | CODE/AIUB 分析中心主页：精密轨道钟差与电离层等产品介绍 | 开放下载 | 🏷️ 官方 核心 精选 |
| [GFZ-GNSS-Services](https://gnss.gfz.de/services) | GFZ GNSS 服务页：产品与在线服务入口 | 开放下载 | 🏷️ 官方 |
| [GFZ-ISDC-GNSS-Products](https://isdc.gfz-potsdam.de/gnss-products/) | GFZ ISDC GNSS 产品专页 | 网页注册 | 🏷️ 官方 |
| [IGS-MGEX](https://igs.org/mgex/) | IGS MGEX：多 GNSS 试验网与多星座产品介绍 | 开放下载 | 🏷️ 官方 |
| [IGS-Products](https://igs.org/products/) | IGS 产品页：轨道、钟差、ERP、偏差、电离层等规范说明 | 开放下载 | 🏷️ 官方 核心 精选 |

### 详细说明

#### [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 介绍页公开。CODE 产品多经 AIUB FTP/HTTPS 或 IGS 数据中心获取；按页内当前下载说明操作。

伯尔尼大学天文研究所 CODE 分析中心门户，概述精密轨道、钟差、ERP、电离层图与偏差等产品线，是全球 PPP 与电离层研究常用源。具体 FTP/HTTPS 主机名可能调整，下载时优先遵循本页与 IGS 镜像的当前链接，并核对文件完整性。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [GFZ-GNSS-Services](https://gnss.gfz.de/services)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 服务列表公开浏览；各服务若需账号会在子页说明。

列出 GFZ 与 GNSS 相关的在线服务及产品入口，包括精密产品综合等跳转。适合先浏览服务再进入具体下载系统。各子服务的鉴权方式可能不同，请按子页说明分别配置，不要共用一套凭据硬试所有接口。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-ISDC-GNSS-Products](https://isdc.gfz-potsdam.de/gnss-products/)  
*🏷️ 官方*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：official

**如何获取：** 先有 ISDC 账号，再在 GNSS 产品页按提示获取或申请具体产品。

聚焦 GFZ 发布的 GNSS 相关产品说明与获取入口，可与 gnss.gfz.de 服务页交叉对照。适合寻找 GFZ 轨道钟差及衍生产品。产品列表会随项目扩展，下载前应阅读各集合的许可文本、引用格式与embargo 说明。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-MGEX](https://igs.org/mgex/)  
*🏷️ 官方*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** MGEX 说明页公开。多星座产品文件经 IGS 数据中心分发，下载门槛随中心而定。

介绍 IGS 多星座试验跟踪网以及轨道、钟差、偏差、天线等实验产品，开展 Galileo、BDS、QZSS 精密应用前应阅读。数据文件仍从标准 IGS 产品目录获取。各星座产品成熟度随时间变化，论文引用请标明 MGEX 与具体分析中心版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [IGS-Products](https://igs.org/products/)  
*🏷️ 官方 核心 精选*

注册：`open`（开放下载） · 宿主：official_site · 来源：official

**如何获取：** 产品说明公开。下载请按页内链接进入 CDDIS 等归档，并遵守对应登录要求。

定义 IGS 轨道、钟差、ERP、偏差与大气等产品类型、时延等级以及长文件名规则，是科研引用与脚本命名的权威参考。文件本体存放在各数据中心。务必注意约 GPS 周 2238 前后的命名切换，旧流水线需要同步适配新模式。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 闪烁/ISMR

| 项目 | 一句话 | 注册方式 | 标记 |
|---|---|---|---|
| [ISMR-Query-Tool](https://ismrquerytool.fct.unesp.br/) | UNESP ISMR 闪烁数据查询工具 | 网页注册 | 🏷️ 高校实验室 精选 |

### 详细说明

#### [ISMR-Query-Tool](https://ismrquerytool.fct.unesp.br/)  
*🏷️ 高校实验室 精选*

注册：`form_register`（网页注册） · 宿主：official_site · 来源：academic_lab

**如何获取：** 在查询工具网页按提示注册/登录后检索下载；政策以 UNESP 页面为准，失败时核对是否需 HTTP 或新域名。

圣保罗州立大学等维护的 ISMR Query Tool，用于查询/获取 GNSS 闪烁监测接收机（ISMR）相关数据，服务低纬闪烁与 CIGALA/CALIBRA 一类研究。站点曾变更域名或证书，若打不开请用 HTTP 或项目组当前公布地址；配合仓内 ismr_downloader 软件条目使用。
