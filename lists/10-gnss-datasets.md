# GNSS 数据源 / GNSS Datasets
> 共 **94** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

## GNSS掩星/RO

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) | AWS 开放数据 GNSS 掩星元数据查询与下载工具（含电离层产品入口） | Python | 21 | 🏷️ 高校实验室 |

### 详细说明

#### [awsgnssroutils](https://github.com/gnss-ro/aws-opendata)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：21 · 宿主：github

面向 AWS Registry of Open Data 上的 GNSS 无线电掩星库：提供 awsgnssroutils 查询/筛选/下载接口，覆盖 CDAAC、JPL、ROM SAF 等多处理中心的 Level-1b/2 产品。做 COSMIC/COSMIC-2 电离层 excess phase、电子密度剖面或与辐射探测共址研究时很省事。仓库体量大、含重整格式流水线；日常用 pip 装 awsgnssroutils 即可，不必整仓克隆。

## PPP-B2b数据

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BDS-3-PPP-B2b-DATA](https://github.com/zp-9696/BDS-3-PPP-B2b-DATA) | 公开一周 BDS-3 PPP-B2b 试验数据 | — | 10 | 🏷️ 个人社区 |

### 详细说明

#### [BDS-3-PPP-B2b-DATA](https://github.com/zp-9696/BDS-3-PPP-B2b-DATA)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：10 · 宿主：github

公开约一周的 BDS-3 PPP-B2b 相关数据，方便复现解码与定位试验。适合写论文或调试 B2bLIB/RTKLIB-B2b 时当标准输入。不是通用数据中心；长期业务请接 IGS/CDDIS 或自建接收。

## IGS综合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BKG-IGS-Data-Center](https://igs.bkg.bund.de/) | BKG IGS 数据中心：欧洲侧 GNSS 数据与 NTRIP 入口 | data-portal | — | 🏷️ 官方 核心 |
| [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/) | NASA CDDIS：IGS 全球 GNSS 观测与产品主归档之一 | data-portal | — | 🏷️ 官方 核心 |
| [CDDIS-Highrate-GNSS](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) | CDDIS 高采样 GNSS 数据说明 | data-portal | — | 🏷️ 官方 |
| [ESA-GSSC](https://gssc.esa.int/) | ESA GNSS Science Support Centre：科学数据与产品门户 | data-portal | — | 🏷️ 官方 核心 |
| [GFZ-ISDC](https://isdc.gfz-potsdam.de/) | GFZ ISDC：波茨坦地球科学研究数据中心门户 | data-portal | — | 🏷️ 官方 |
| [IGS-Data-Access](https://igs.org/data-access/) | IGS 数据访问页：全球数据中心与获取方式一览 | data-portal | — | 🏷️ 官方 |
| [IGS-Files-CDN](https://files.igs.org/) | IGS files.igs.org 文件分发入口 | data-portal | — | 🏷️ 官方 核心 |
| [IGS-Home](https://igs.org/) | 国际 GNSS 服务（IGS）官网：产品、工作组与数据中心总入口 | data-portal | — | 🏷️ 官方 核心 |
| [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/) | NASA Earthdata 统一登录：CDDIS 等地球科学数据下载的前置账号 | data-portal | — | 🏷️ 官方 核心 |
| [SOPAC-CSRC](https://sopac-csrc.ucsd.edu/) | SOPAC/CSRC：Scripps 轨道与永久阵列中心门户 | data-portal | — | 🏷️ 官方 |
| [SOPAC-Garner-Pub](https://garner.ucsd.edu/pub/) | SOPAC garner 公共目录：产品与相关文件树 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BKG-IGS-Data-Center](https://igs.bkg.bund.de/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

德国联邦制图与大地测量局维护的 IGS 数据中心门户，同时提供文件下载与实时播发相关入口，是欧洲用户常用镜像与 caster 起点。实时 NTRIP 与事后文件通道彼此独立，配置账号时不要把 caster 凭证与 HTTPS 下载混用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IGS 核心数据中心，提供日/小时 RINEX、广播星历、精密 SP3/CLK、IONEX 与偏差等产品。目录按年积日或 GPS 周组织，文件多为压缩格式。适合全球网事后处理与电离层研究。匿名 FTP 已停用，必须 Earthdata 登录；大流量请限速，并核对长文件名规范与校验信息。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-Highrate-GNSS](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NASA CDDIS 对高采样率（high-rate）GNSS 观测产品的官方说明页，解释目录组织与用途，是闪烁/同震等高频应用找数据的路标。下载实体文件仍走 CDDIS 归档并需 Earthdata；可与 cddis-highrate-downloader 软件条目搭配。

#### [ESA-GSSC](https://gssc.esa.int/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧空局 GNSS 科学支持中心，提供面向科研的 GNSS 数据与产品检索下载，并镜像部分 IGS 内容。适合已有欧洲科研账号体系的用户。权限通常分层，登录后仍可能对部分集合只读或需追加申请；请遵守 ESA 数据政策与引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-ISDC](https://isdc.gfz-potsdam.de/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

亥姆霍兹德国地学研究中心综合科学数据中心，提供 GNSS 及多种地球物理产品的统一检索入口。欧洲大地测量与重力/GNSS 组合研究常用。完成注册后仍需按具体集合申请授权，并非所有子库都对个人用户立即完全开放。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-Data-Access](https://igs.org/data-access/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

集中列出 IGS 各数据中心镜像地址与访问提示，方便按网络条件选择就近源。本页不托管观测文件本体。各中心登录门槛不同，例如 CDDIS 需要 Earthdata。镜像同步偶有延迟，关键周产品可在两个中心交叉校验大小与时间戳。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-Files-CDN](https://files.igs.org/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IGS 提供的 files.igs.org 文件分发入口，常用于获取站点日志、天线、产品列表或镜像文件树，是对 CDDIS/BKG 等归档的补充入口。目录结构会调整，下载前对照 IGS Data Access 说明；大文件请限速并校验。

#### [IGS-Home](https://igs.org/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IGS 官方门户，链向产品规范、分析中心、全球/区域数据中心以及实时服务说明。站点本身通常不直接托管海量 RINEX。适合查阅标准文件名、站点日志格式与政策文件。实际观测与产品下载请转到 CDDIS、BKG、ESA GSSC 等归档系统。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NASA 地球科学数据统一身份入口。下载 CDDIS GNSS 观测与产品前需先在此注册免费账号，浏览器与脚本（常配 .netrc）均可使用。本站不存储 GNSS 文件，只负责认证与应用授权；请按提示勾选 CDDIS 等应用。注意保管密码与令牌，切勿写入公开仓库或日志。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [SOPAC-CSRC](https://sopac-csrc.ucsd.edu/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

加州大学圣地亚哥分校 SOPAC 门户，历史上长期作为 IGS 数据中心之一，提供轨道产品与永久阵列相关服务入口。适合查找 SOPAC 特色产品与工具。部分古老 FTP 主机名已变更，应优先采用本页当前链接及 garner 公共目录。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [SOPAC-Garner-Pub](https://garner.ucsd.edu/pub/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

SOPAC 侧公开文件树，常包含产品文件与辅助资料，可作为 CDDIS 之外的对照镜像。目录权限与层级会随运维调整。对关键 GPS 周产品，建议与另一 IGS 数据中心交叉检查文件大小、修改时间与校验结果。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 地磁空间天气

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BoM-SWS](https://www.sws.bom.gov.au/) | 澳大利亚 BoM 空间天气服务（SWS） | data-portal | — | 🏷️ 官方 |
| [CelesTrak-SpaceData](https://celestrak.org/SpaceData/) | CelesTrak SpaceData：空间天气与相关辅助数据镜像 | data-portal | — | 🏷️ 官方 |
| [GFZ-Kp-Index](https://kp.gfz-potsdam.de/en/) | GFZ Kp 地磁指数官方发布 | data-portal | — | 🏷️ 官方 |
| [GIRO-DIDBase](https://giro.uml.edu/didbase/) | GIRO DIDBase：全球电离层测高仪数据库 | data-portal | — | 🏷️ 官方 核心 |
| [NASA-OMNIWeb](https://omniweb.gsfc.nasa.gov/) | NASA OMNIWeb：太阳风与地磁指数多源合并数据 | data-portal | — | 🏷️ 官方 |
| [NASA-SPDF](https://spdf.gsfc.nasa.gov/) | NASA SPDF：空间物理数据设施总入口 | data-portal | — | 🏷️ 官方 |
| [NOAA-SWPC](https://www.swpc.noaa.gov/) | NOAA 空间天气预测中心（SWPC） | data-portal | — | 🏷️ 官方 |
| [NOAA-SWPC-Planetary-K](https://www.swpc.noaa.gov/products/planetary-k-index) | NOAA SWPC 行星 K 指数产品 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BoM-SWS](https://www.sws.bom.gov.au/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

澳大利亚气象局空间天气服务网站，提供电离层状态、高频传播与相关预报产品，对亚太地区 GNSS 用户具有区域参考价值。产品更新频率不一。若需自动抓取，请遵守站点条款，优先使用其标明的数据服务而不是裸爬页面。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [CelesTrak-SpaceData](https://celestrak.org/SpaceData/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CelesTrak 提供的空间天气及相关辅助数据集合，方便与卫星轨道、可见性工具链衔接使用。它不是 IGS 官方数据中心。关键地磁或太阳指数建议同时对照 NOAA、GFZ 等一手发布源，以免镜像更新延迟影响事件分析。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-Kp-Index](https://kp.gfz-potsdam.de/en/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GFZ 官方发布的行星 Kp 等地磁活动指数，是空间天气研究以及 GNSS 闪烁、ROTI 扰动分析中常用的外部驱动参数，通常开放获取。使用时注意时间分辨率以及确定值与预报值的区别，论文中应明确写出来源机构与产品版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GIRO-DIDBase](https://giro.uml.edu/didbase/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

麻省大学洛厄尔分校维护的测高仪观测数据库入口，提供虚高图与临界频率等特性参数，常与 GNSS TEC 及 IRTAM 同化产品对照。空间天气与模型验证常用。一般需要注册；请按站内要求引用，并留意测站时间覆盖可能存在空洞。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NASA-OMNIWeb](https://omniweb.gsfc.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NASA/GSFC 的 OMNIWeb 接口提供太阳风等离子体、行星际磁场与地磁指数等合并时间序列，广泛用于 GNSS 相关空间天气统计分析。通过网页表单交互取数。若需要高时间分辨率，请正确选择 OMNI 高分辨或低分辨数据集。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NASA-SPDF](https://spdf.gsfc.nasa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NASA 空间物理数据设施总入口，托管太阳风、磁层与相关日地物理数据，可与 GNSS 电离层扰动机制研究结合。门类非常广泛。使用具体任务数据时请遵循页面给出的 DOI 与致谢（acknowledge）要求，便于结果可复现。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-SWPC](https://www.swpc.noaa.gov/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国 NOAA 空间天气预测中心门户，提供耀斑、质子事件、地磁活动等业务产品，常用来解释 GNSS 定位异常与电离层扰动时段。实时导向强。科研归档时应保存所用产品副本，并注意业务产品可能事后修订。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-SWPC-Planetary-K](https://www.swpc.noaa.gov/products/planetary-k-index)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

SWPC 发布的行星 K 指数产品页，便于把地磁活动快速叠加到 GNSS ROTI 或闪烁时间轴上做事件分析。与 GFZ Kp 密切相关但发布节奏与文件格式可能不同，对比研究时必须分别注明来源，避免混用造成时间轴错位。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 电离层产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/) | 中科院 CAS 电离层 IONEX 产品（data.bdsmart.cn） | data-portal | — | 🏷️ 官方 核心 |
| [CAS-BDsmart-RTS-Iono](https://data.bdsmart.cn/pub/product/rts/iono/) | 中科院 BDsmart 实时电离层产品目录（RTS IONEX 等） | data-portal | — | 🏷️ 官方 |
| [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html) | CDDIS 大气产品页：电离层 IONEX 与对流层产品索引说明 | data-portal | — | 🏷️ 官方 |
| [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/) | CDDIS IONEX 目录：IGS 及各分析中心全球电离层图 | data-portal | — | 🏷️ 官方 核心 |
| [CNES-PPP-WIZARD-Realtime-Products](http://www.ppp-wizard.net/products/REAL_TIME) | CNES PPP-WIZARD 实时产品目录（含实时轨道钟差/偏差及电离层相关输出） | data-portal | — | 🏷️ 官方 |
| [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) | INGV eSWua 数据库：地中海/欧洲/全球 TEC 现报与预报产品入口 | data-portal | — | 🏷️ 官方 核心 |
| [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/) | IGS 电离层工作组：GIM/IAAC 与产品活动入口 | data-portal | — | 🏷️ 官方 |
| [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 意大利 INGV 基于 RING 网的实时 TEC 监测与地图发布页 | data-portal | — | 🏷️ 官方 核心 |
| [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/) | JPL 快速 IONEX 发布目录：日更新全球电离层图 | data-portal | — | 🏷️ 官方 核心 |
| [UPC-Chapman-TOMION-Rapid](https://chapman.upc.es/tomion/rapid/) | UPC Chapman：TOMION/IONEX 快速电离层产品下载 | data-portal | — | 🏷️ 高校实验室 |
| [UPC-gAGE-FastPPP-Products](https://gage.upc.edu/en/gage-products/fast-ppp-products) | UPC gAGE Fast-PPP 产品页：STEC/IONEX/钟差等申请说明 | data-portal | — | 🏷️ 高校实验室 |
| [UPC-IONEX-Archive](https://cabrera.upc.edu/upc_ionex_GPSonly-RINEXv3/) | UPC 电离层 IONEX 归档目录（分年） | data-portal | — | 🏷️ 高校实验室 |
| [UPC-IONO4HAS-Products](https://server.gage.upc.edu/iono4has/products.html) | UPC IONO4HAS：面向 HAS 的电离层产品状态页 | data-portal | — | 🏷️ 高校实验室 |
| [WHU-IGS-Ionosphere-AC](https://panda.whu.edu.cn/yjpt/IGSdlcfxzx.htm) | 武汉大学 IGS 电离层分析中心：GIM/DCB/ROTI 产品说明 | data-portal | — | 🏷️ 高校实验室 核心 |

### 详细说明

#### [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

中国科学院相关团队发布的多 GNSS GIM HTTPS 目录，用于接替旧 FTP，提供快速与最终等 IONEX 产品。东亚与全球电离层研究常用来源之一。同步到 IGS 数据中心可能存在时延差；请将脚本迁移到新域名，勿再依赖已宣布停用的旧 FTP。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CAS-BDsmart-RTS-Iono](https://data.bdsmart.cn/pub/product/rts/iono/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

与已收录的 CAS 最终/快速 IONEX 目录配套的实时（RTS）电离层产品树，面向近实时 GIM/SSR 相关用户。适合 PPP-RTK/实时监测试验；事后精密分析仍建议使用最终 IONEX 与多 AC 交叉验证。

#### [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

汇总 IGS 电离层 GIM（IONEX）与对流层相关产品在 CDDIS 的存放说明，并解释新旧文件名对应关系。面向 TEC/ZTD 用户快速定位路径。实际数据文件仍在 archive 树中按日或周存放。Rapid 与 Final 时延不同，引用时应注明分析中心与产品类型。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

存放 IGS 综合与各电离层分析中心的 GIM、ROTI 等 IONEX 文件，按年份与年积日组织。是 GNSS 电离层事后研究最常用入口之一。下载需登录；注意 Final、Rapid 与预测产品的时延及格网分辨率差异，并结合码偏差/OSB 产品一起使用以免系统差。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CNES-PPP-WIZARD-Realtime-Products](http://www.ppp-wizard.net/products/REAL_TIME)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CNES PPP-WIZARD 示范系统的 REAL_TIME 产品树，可检索实时流配套文件；CNES 亦通过 IGS-RTS 播发实时 SSR。已收录门户首页，本条补齐可枚举的实时产品路径，便于脚本对接。

#### [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec)  
*🏷️ 官方 核心*

语言：data-portal · 许可：CC-BY-4.0 · 星标约：— · 宿主：official_site

INGV eSWua 数据库 TEC 专题（DOI:10.13127/eswua/tec，CC BY 4.0）。接入 RING/EUREF/IGS 观测，持续产出地中海、欧洲与全球 TEC 现报/短期预报（含 NeQuick2 同化与 24h 预报），并提供 Download Tool 与 REST 示例。适合意大利/地中海高分辨率实时 TEC 或程序化拉图；不是 GNSS 原始观测归档。引用请按页面元数据与 CC BY 4.0。

#### [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

介绍 IGS 电离层联合产品机制、各分析中心角色以及相关会议与试点活动。适合了解 CODE、JPL、UPC、CAS、WHU 等 IAAC 分工。页面不直接存储 IONEX 文件。综合产品与单中心产品在精度和时延上不同，研究中应分开评估与引用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

INGV 基于 RING 网（约 40 站）的意大利区域实时 VTEC 监测页：IPP 估计后 LOWESS 插值，约 0.1° 网格、~10 分钟刷新。本页主要展示最新地图与近 24 小时动画，不是开源处理仓库；批量历史与 Web 服务请用同组 eSWua-TEC。使用与引用遵守 INGV/相关论文要求。

#### [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

JPL 侧快速电离层图公开目录，文件为 IONEX 风格，适合需要较短时延 GIM 的科研与监测。其结果与 IGS 综合 Final 存在差异，不可直接等同。部分机构网络可能拦截 sideshow 域名；重要任务建议同时备份 CDDIS 路径中的同系列产品。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [UPC-Chapman-TOMION-Rapid](https://chapman.upc.es/tomion/rapid/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

加泰罗尼亚理工 gAGE 在 chapman.upc.es 上的 TOMION rapid 目录，按年提供可匿名拉取的快速电离层格网/相关产品，常被射电天文与 GNSS 工具（如 Spinifex）作为免账号 IONEX 源。覆盖与延迟不及 CDDIS 正式库全面；大批量请遵守站点礼貌爬取，最终产品以 UPC/IGS 说明为准。

#### [UPC-gAGE-FastPPP-Products](https://gage.upc.edu/en/gage-products/fast-ppp-products)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

说明 Fast-PPP 相关精密产品组成，包括模糊度小数、精密 STEC、IONEX 与卫星钟差，并给出建议引用文献。面向高精度电离层与 PPP 研究用户。产品服务器通常需要邮件开通，并非完全匿名开放；获权后请遵守学术使用约定。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [UPC-IONEX-Archive](https://cabrera.upc.edu/upc_ionex_GPSonly-RINEXv3/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

UPC 提供的分年 IONEX 归档，包含长期时间序列以及最新快速文件入口，服务 GNSS 电离层与相关高精度应用研究。适合明确需要 UPC 单中心解的用户。请与 IGS 综合产品区分使用；目录旁文档说明格式约定与处理设定，引用时写明版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [UPC-IONO4HAS-Products](https://server.gage.upc.edu/iono4has/products.html)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

展示与 Galileo HAS 相关的电离层产品链接及当日运行状态，便于开展监测与对比实验。内容偏研究原型，不宜简单等同于 IGS 标准综合 GIM。格式细节见站内说明；长期归档可能与公开 IONEX 目录并存，下载前确认许可范围。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [WHU-IGS-Ionosphere-AC](https://panda.whu.edu.cn/yjpt/IGSdlcfxzx.htm)  
*🏷️ 高校实验室 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

武汉大学卫星导航定位技术研究中心作为 IGS 电离层分析中心的产品介绍页，覆盖事后与实时 GIM、多系统码偏差以及 ROTI 图。对中文用户较友好。自建 FTP 主机偶发不可达时，可改用 IGS 数据中心中的 WHU 文件，并区分实时与事后时延。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## 偏差产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CAS-BDsmart-Pub](https://data.bdsmart.cn/pub/) | CAS 数据发布根：DCB/GIM/SSR 等相关产品入口 | data-portal | — | 🏷️ 官方 |
| [CSNO-TARC](https://www.csno-tarc.cn/) | 中国卫星导航系统管理办公室测试评估研究中心（TARC） | data-portal | — | 🏷️ 官方 |
| [CSNO-TARC-Differential](https://www.csno-tarc.cn/en/data/differential) | TARC 差分数据英文页 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [CAS-BDsmart-Pub](https://data.bdsmart.cn/pub/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

中科院相关 GNSS 产品的 HTTPS 发布根目录，常见子树包括多星座码偏差、全球电离层图以及实时 SSR 转存等。适合把偏差与 GIM 放在同一流水线下载。具体子目录以站点为准；论文引用请标明 CAS 产品标识、日期与文件长名。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CSNO-TARC](https://www.csno-tarc.cn/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

北斗及相关 GNSS 服务的测试评估门户，发布性能监测、差分信息等入口，中文北斗应用与服务监测场景常用。公开浏览内容与需申请下载的内容可能并存。再分发或商用前应阅读版权条款；涉及合作网数据时以站内最新公告为准，勿臆造未公开接口。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [CSNO-TARC-Differential](https://www.csno-tarc.cn/en/data/differential)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

TARC 面向国际用户的差分与相关数据说明页面，便于获取北斗监测类产品线索。页面内容会随服务更新。其产品体系与 IGS 码偏差/OSB 并不完全等同，若与 IGS 产品融合使用，必须注意信号定义、基准与时间系统差异。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 轨道钟差

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html) | CODE/AIUB 分析中心主页：精密轨道钟差与电离层等产品介绍 | data-portal | — | 🏷️ 官方 核心 |
| [GFZ-GNSS-Services](https://gnss.gfz.de/services) | GFZ GNSS 服务页：产品与在线服务入口 | data-portal | — | 🏷️ 官方 |
| [GFZ-ISDC-GNSS-Products](https://isdc.gfz-potsdam.de/gnss-products/) | GFZ ISDC GNSS 产品专页 | data-portal | — | 🏷️ 官方 |
| [IGS-MGEX](https://igs.org/mgex/) | IGS MGEX：多 GNSS 试验网与多星座产品介绍 | data-portal | — | 🏷️ 官方 |
| [IGS-Products](https://igs.org/products/) | IGS 产品页：轨道、钟差、ERP、偏差、电离层等规范说明 | data-portal | — | 🏷️ 官方 核心 |

### 详细说明

#### [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

伯尔尼大学天文研究所 CODE 分析中心门户，概述精密轨道、钟差、ERP、电离层图与偏差等产品线，是全球 PPP 与电离层研究常用源。具体 FTP/HTTPS 主机名可能调整，下载时优先遵循本页与 IGS 镜像的当前链接，并核对文件完整性。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [GFZ-GNSS-Services](https://gnss.gfz.de/services)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

列出 GFZ 与 GNSS 相关的在线服务及产品入口，包括精密产品综合等跳转。适合先浏览服务再进入具体下载系统。各子服务的鉴权方式可能不同，请按子页说明分别配置，不要共用一套凭据硬试所有接口。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GFZ-ISDC-GNSS-Products](https://isdc.gfz-potsdam.de/gnss-products/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

聚焦 GFZ 发布的 GNSS 相关产品说明与获取入口，可与 gnss.gfz.de 服务页交叉对照。适合寻找 GFZ 轨道钟差及衍生产品。产品列表会随项目扩展，下载前应阅读各集合的许可文本、引用格式与embargo 说明。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGS-MGEX](https://igs.org/mgex/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

介绍 IGS 多星座试验跟踪网以及轨道、钟差、偏差、天线等实验产品，开展 Galileo、BDS、QZSS 精密应用前应阅读。数据文件仍从标准 IGS 产品目录获取。各星座产品成熟度随时间变化，论文引用请标明 MGEX 与具体分析中心版本。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [IGS-Products](https://igs.org/products/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

定义 IGS 轨道、钟差、ERP、偏差与大气等产品类型、时延等级以及长文件名规则，是科研引用与脚本命名的权威参考。文件本体存放在各数据中心。务必注意约 GPS 周 2238 前后的命名切换，旧流水线需要同步适配新模式。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## IGS产品下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CODE-AIUB-Product-Download](https://www.aiub.unibe.ch/download/) | AIUB/CODE 产品 HTTPS 下载浏览器（含 CODE/ionex/ionosphere 等目录） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [CODE-AIUB-Product-Download](https://www.aiub.unibe.ch/download/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

伯尔尼大学天文研究所 CODE 分析中心的官方产品文件浏览器。可进入 CODE、CODE_MGEX、ionex、ionosphere 等目录获取最终/快速/超快速轨道钟差与 IONEX 等。FTP 已弃用，请改用本 HTTPS 入口；与已收录的 CODE AC 介绍页互补，本条聚焦可下载产品树。

## 掩星

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/) | COSMIC CDAAC：GNSS 无线电掩星大气/电离层产品 | data-portal | — | 🏷️ 官方 核心 |
| [COSMIC-GNSS-RO-Data](https://data.cosmic.ucar.edu/gnss-ro/) | COSMIC GNSS-RO 公开数据目录 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

COSMIC/FORMOSAT 等任务的无线电掩星数据中心门户，提供中性大气与电离层电子密度廓线等产品，常与地基 GNSS TEC 联合分析。空间天气与气象交叉研究几乎必用。注册通常免费，但须遵守引用与使用协议；不同处理级别不可混用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [COSMIC-GNSS-RO-Data](https://data.cosmic.ucar.edu/gnss-ro/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

面向 GNSS 无线电掩星的公开数据目录树，便于使用直链或镜像方式批量拉取文件，适合流水线化预处理。目录层级会随任务与版本变化，下载脚本应用清单或校验和验证完整性，避免漏文件或版本混杂。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## PPP/PPP-RTK样例

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cssrlib-data](https://github.com/hirokawa/cssrlib-data) | CSSRlib 配套样例脚本与数据集 | Python | 44 | 🏷️ 高校实验室 |

### 详细说明

#### [cssrlib-data](https://github.com/hirokawa/cssrlib-data)  
*🏷️ 高校实验室*

语言：Python · 许可：NOASSERTION · 星标约：44 · 宿主：github

为 CSSRlib 提供样例脚本与试验观测/改正数据，方便本地或 Colab 复现 CLAS、HAS、BDS PPP 等开放服务流程。适合跟着官方教程跑通改正接入与定位。不是长期产品归档；业务数据请接 IGS 或各服务官方中心，并注意样例时段与电文版本。

## CORS区域网

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss) | EarthScope GAGE GNSS 归档：北美及合作站观测数据 | data-portal | — | 🏷️ 官方 核心 |
| [EarthScope-Home](https://www.earthscope.org/) | EarthScope 主页：原 UNAVCO/IRIS 合并后的地球科学联盟入口 | data-portal | — | 🏷️ 官方 |
| [EUREF-EPN-CB](https://www.epncb.oma.be/) | EUREF EPN 中央局：欧洲参考站网数据与产品 | data-portal | — | 🏷️ 官方 核心 |
| [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/) | EPN 观测数据 FTP/Web 目录 | data-portal | — | 🏷️ 官方 |
| [GA-GNSS-Data](https://data.gnss.ga.gov.au/) | Geoscience Australia GNSS 数据门户（AUSCORS 等） | data-portal | — | 🏷️ 官方 核心 |
| [HongKong-SatRef](https://www.geodetic.gov.hk/en/satref/satref.htm) | 香港 SatRef：卫星定位参考站网介绍 | data-portal | — | 🏷️ 官方 |
| [HongKong-SatRef-RINEX](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 香港 SatRef RINEX 数据说明与下载 | data-portal | — | 🏷️ 官方 |
| [IGN-Geodesie](https://geodesie.ign.fr/) | 法国 IGN 大地测量门户（RGP 等相关入口） | data-portal | — | 🏷️ 官方 |
| [NOAA-CORS-AWS](https://noaa-cors-pds.s3.amazonaws.com/index.html) | NOAA CORS on AWS：NCN RINEX 的 S3/NODD 分发 | data-portal | — | 🏷️ 官方 |
| [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/) | NOAA CORS 数据目录树 | data-portal | — | 🏷️ 官方 |
| [NOAA-NCN-API](https://geodesy.noaa.gov/web_services/ncn-api.shtml) | NOAA NCN API：CORS 站元数据与最近站查询 | data-portal | — | 🏷️ 官方 |
| [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/) | NOAA NGS CORS：美国连续运行参考站网数据门户 | data-portal | — | 🏷️ 官方 核心 |
| [SIRGAS-Home](https://www.sirgas.org/en/) | SIRGAS：拉丁美洲大地参考架与 GNSS 网门户 | data-portal | — | 🏷️ 官方 |
| [SONEL](https://www.sonel.org/) | SONEL：全球海平面观测网（含 GNSS 并址站） | data-portal | — | 🏷️ 官方 |
| [UNAVCO-GPS-GNSS-Data](https://www.unavco.org/data/gps-gnss/gps-gnss.html) | UNAVCO 遗留 GNSS 数据页（导向 EarthScope/GAGE） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GAGE 数据系统上的 GNSS 归档入口，承接原 UNAVCO 测站 RINEX 等产品，广泛用于构造、火山、水文与电离层研究。北美及合作网密度高、时间跨度长。登录与接口策略可能调整，编写脚本前应用浏览器确认当前权限模型与路径。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EarthScope-Home](https://www.earthscope.org/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EarthScope 联盟门户，汇总地球物理与大地测量设施、项目与数据政策信息。具体 GNSS 文件检索在 GAGE 数据系统完成。历史上 UNAVCO 品牌页面多会重定向到此处。寻找 RINEX 时请优先使用 gage-data.earthscope.org 归档链接。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [EUREF-EPN-CB](https://www.epncb.oma.be/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲 EPN 中央局官方门户，提供测站信息、观测文件与产品相关入口，是欧洲大地参考框架网的核心数据枢纽。适合区域 PPP、形变与电离层研究。实时流与事后文件渠道分离；使用高采样数据时注意存储容量并遵循 EPN 引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EPN 测站观测文件目录，便于按站名直接下载 RINEX，是欧洲区域研究的高频访问路径。目录组织相对稳定，但测站列表会增减。批量下载前应对照中央局站点状态页，剔除长期停测或仅测试用途的测站。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GA-GNSS-Data](https://data.gnss.ga.gov.au/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

澳大利亚地球科学局 GNSS 数据服务，覆盖澳新等区域参考站观测与相关产品的检索下载，是亚太用户重要区域网来源。旧版 ga.gov.au 深链可能失效，请优先使用本数据域名与官方 API 文档，并关注站网元数据更新。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [HongKong-SatRef](https://www.geodetic.gov.hk/en/satref/satref.htm)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

香港地政总署卫星定位参考站网说明页，属于高密度城市 CORS 的典型代表，适合华南与香港本地增强、教学及城市电离层个例。实时播发与事后 RINEX 渠道通常不同；投入商用或再分发前请阅读官方使用条款。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [HongKong-SatRef-RINEX](https://www.geodetic.gov.hk/en/rinex/rinex.htm)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

说明如何获取 SatRef 事后 RINEX 观测数据，是区域电离层与对流层案例研究的便捷来源。需注意采样率、文件保留期限与站名规则。若进行大量自动下载，应遵守网站礼貌访问规范并优先在本地缓存。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [IGN-Geodesie](https://geodesie.ign.fr/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

法国国家地理与森林信息研究所大地测量站点，导向国家 GNSS 连续运行网与产品信息，可作为欧洲区域网的补充数据源。历史上 IGS 数据中心 FTP 主机可能不稳定，获取文件时优先使用本页给出的当前方式与镜像说明。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-CORS-AWS](https://noaa-cors-pds.s3.amazonaws.com/index.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NOAA Open Data Dissemination（NODD）把 NCN/CORS RINEX 放到公开 S3 桶 noaa-cors-pds，可用 HTTPS/AWS 工具按年积日/站名批量拉取，常比官网树更适合云端脚本。与 geodesy.noaa.gov/corsdata 同源产品、不同分发通道。大流量请注意带宽与对象键命名约定。

#### [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CORS 观测文件目录树入口，便于按测站、年份与年积日批量抓取公开 RINEX。面向自动化流水线。请控制并发与请求频率，遵守 NOAA 使用政策，并在本地做好缓存与校验，以免重复冲击服务器。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-NCN-API](https://geodesy.noaa.gov/web_services/ncn-api.shtml)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国国家大地测量局提供的 NOAA CORS Network（NCN）Web API，可按站名取属性、或按 ECEF 坐标查最近参考站，服务 Data Explorer 等应用。返回元数据而非 RINEX 本体；下载观测请配合 corsdata/AWS NODD/UFCORS。须遵守 NGS 服务条款与合理访问频率。

#### [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国国家大地测量局 CORS 官方入口，提供测站元数据、RINEX 观测与相关产品链接，是北美高精度定位与电离层研究常用网络。站点数量多、跨度长。处理前务必核对天线变更日志与站点活跃状态，避免使用已关闭测站而未更新元数据。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [SIRGAS-Home](https://www.sirgas.org/en/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

SIRGAS 官方网站介绍拉丁美洲及周边大地参考框架与 GNSS 站网组织方式，是该区域地壳运动与电离层研究的入口级资源。具体 RINEX 往往分散在各成员国数据中心，需要从本站再跳转，并分别遵守各国获取规则。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [SONEL](https://www.sonel.org/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

全球海平面观测组织门户，许多验潮站与 GNSS 并址，服务于海洋大地测量、垂直基准与海平面变化研究。数据偏沿海场景。GNSS 文件有时并不直接托管，而是链到各国 CORS 或数据中心，需要二次跳转并分别注册。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [UNAVCO-GPS-GNSS-Data](https://www.unavco.org/data/gps-gnss/gps-gnss.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

原 UNAVCO 的 GPS/GNSS 数据说明页，主要用于旧文档与书签兼容，并导向 EarthScope/GAGE 新流程。新的数据工作应以 EarthScope 归档为准。若遇到失效深链，请改用 gage-data.earthscope.org。TEQC 等软件说明仍可能保留在 unavco 域名下。

## 实时流

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IGS-RTS](https://igs.org/rts/) | IGS 实时服务（RTS）：实时轨道钟差/SSR 流说明 | data-portal | — | 🏷️ 官方 核心 |

### 详细说明

#### [IGS-RTS](https://igs.org/rts/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

说明 IGS 实时轨道钟差及 SSR 播发框架、参与分析中心与应用场景，面向实时 PPP 与完整性监测。本页通常不直接推送数据流，需经 BKG 等 NTRIP caster 接入。流可用性与消息版本会更新，上线前应核对挂载点表和解码库兼容性。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## NTRIP服务商/CRS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ntrip-catalog](https://github.com/Pix4D/ntrip-catalog) | Pix4D 开源 NTRIP 服务商目录（含坐标参考系 CRS 元数据，CC0） | Python | 14 | 🏷️ 个人社区 |

### 详细说明

#### [ntrip-catalog](https://github.com/Pix4D/ntrip-catalog)  
*🏷️ 个人社区*

语言：Python · 许可：CC0-1.0 · 星标约：14 · 宿主：github

以 JSON 维护多家 NTRIP 服务的挂载点与 CRS 信息，站点 ntrip-catalog.org 提供检索。解决 RTCM/NTRIP 握手不携带参考框架信息的问题，便于应用按位置匹配改正坐标系。属开放数据目录而非 caster 实现；条目完整性依赖社区贡献与服务商变更。

## 对流层

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/) | TU Wien VMF 对流层格网数据目录（与 /codes 源码区分） | data-portal | — | 🏷️ 官方 核心 |

### 详细说明

#### [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

维也纳工大 VMF 服务的对流层产品目录树，提供 VMF1/VMF3 等格网，供 PPP 与 VLBI 映射函数使用。本条强调数据产品，源码实现见同站 /codes（软件类另收）。选用时注意格网版本与气象模型匹配；业务系统还需确认更新节奏与文献引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

## 空间天气辅助

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [AMBER-Magnetometers](https://magnetometers.bc.edu/) | BC AMBER 等磁强计网络数据中心 | data-portal | — | 🏷️ 高校实验室 |
| [CARISMA](https://www.carisma.ca/) | 加拿大 CARISMA 地磁阵列数据门户 | data-portal | — | 🏷️ 高校实验室 |
| [FMI-IMAGE](https://space.fmi.fi/image/) | FMI IMAGE 北欧地磁台链数据 | data-portal | — | 🏷️ 官方 |
| [INTERMAGNET](https://www.intermagnet.org/) | INTERMAGNET 全球地磁台网数据 | data-portal | — | 🏷️ 官方 |
| [Kyoto-WDC-Geomagnetism](https://wdc.kugi.kyoto-u.ac.jp/) | 京都 WDC：Kp/Dst 等地磁指数 | data-portal | — | 🏷️ 官方 核心 |
| [OpenMadrigal](https://openmadrigal.org/) | OpenMadrigal/CEDAR 分布式空间天气数据库 | data-portal | — | 🏷️ 高校实验室 |
| [SuperDARN-VT](https://vt.superdarn.org/) | VT SuperDARN 高频雷达/对流数据入口 | data-portal | — | 🏷️ 高校实验室 |
| [SuperMAG](https://supermag.jhuapl.edu/) | SuperMAG 全球地磁合并数据 | data-portal | — | 🏷️ 高校实验室 |

### 详细说明

#### [AMBER-Magnetometers](https://magnetometers.bc.edu/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Boston College 维护的 AMBER 等磁强计网络数据中心，提供 ASCII 日文件与日绘图，服务低纬/非洲扇区空间天气与电流体系研究，可与 GNSS ROTI/闪烁对照。门户含 Downloads 浏览；使用请遵守站点引用与数据政策。本条是地磁辅助数据，不是 GNSS 观测归档。

#### [CARISMA](https://www.carisma.ca/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CARISMA（Canadian Array for Realtime Investigations of Magnetic Activity）地磁阵列门户，服务加拿大扇区磁暴/亚暴与磁场脉动研究，可与北美 GNSS 电离层扰动对照。站点介绍获取途径；详细下载规则以其数据政策为准。

#### [FMI-IMAGE](https://space.fmi.fi/image/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

FMI 的 IMAGE（International Monitor for Auroral Geomagnetic Effects）地磁台网门户，覆盖北欧高纬，提供研究用磁情指数与台站数据入口，常与极光区 GNSS TEC/闪烁联合分析。网页公开；具体 FTP/文件服务与引用格式见站内文档。

#### [INTERMAGNET](https://www.intermagnet.org/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

国际实时地磁台网门户，提供参与台站的准实时与存档地磁数据入口，常与 GNSS TEC/ROTI 做空间天气对照。数据政策与台站列表以官网为准；部分产品需按说明注册或经成员机构渠道。

#### [Kyoto-WDC-Geomagnetism](https://wdc.kugi.kyoto-u.ac.jp/)  
*🏷️ 官方 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

京都 WDC for Geomagnetism 提供 Kp、Dst 等经典地磁指数与相关数据服务，是空间天气与电离层扰动研究的常用外部驱动入口。门户以网页/文件服务为主；下载与引用规则见站点说明。本条收录「数据怎么拿」，不是 GNSS 观测归档。

#### [OpenMadrigal](https://openmadrigal.org/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

OpenMadrigal 项目主页，介绍分布式 Madrigal 数据库（CEDAR、ISR TEC 等）及开源服务器/客户端。科研上常作非相干散射雷达与 GNSS TEC 产品的交叉验证入口。具体实验数据在各成员站（如 cedar.openmadrigal.org）；Python 访问见 madrigalWeb。

#### [SuperDARN-VT](https://vt.superdarn.org/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

Virginia Tech SuperDARN 门户是国际高频雷达网的重要节点，提供极区/亚极区电离层对流与散射相关产品入口，常与 GNSS TEC/TID、地磁扰动联合使用。数据政策与镜像站点以社区现行说明为准；配合 DARNtids 等开源工具做 TID 分析。

#### [SuperMAG](https://supermag.jhuapl.edu/)  
*🏷️ 高校实验室*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

JHU/APL SuperMAG 汇集全球地磁台站并提供统一坐标与多种指数/绘图服务，便于做高纬扰动与 GNSS 闪烁对照。网页注册后按条款使用；引用需遵循 SuperMAG 与原始台站要求。

## 区域CORS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BEV-APOS](https://www.bev.gv.at/Services/Produkte/Grundlagenvermessung/APOS.html) | BEV APOS：奥地利 CORS；RINEX 事后免费 | data-portal | — | 🏷️ 官方 |
| [GeoNet-Data-API](https://data.geonet.org.nz/) | GeoNet Data API：新西兰 GNSS RINEX 机器接口 | data-portal | — | 🏷️ 官方 |
| [GeoNet-NZ-Geodetic](https://www.geonet.org.nz/data/types/geodetic) | 新西兰 GeoNet 大地测量/GNSS 数据 | data-portal | — | 🏷️ 官方 |
| [IBGE-RBMC](https://www.ibge.gov.br/en/geosciences/geodetic-network/2421-rbmc.html) | 巴西 IBGE RBMC 连续 GNSS 网 | data-portal | — | 🏷️ 官方 |
| [IBGE-RBMC-API](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1) | 巴西 RBMC REST API（RINEX 按站下载） | data-portal | — | 🏷️ 官方 |
| [Japan-MIRAI-Archive](https://go.gnss.go.jp/mirai/miraiarchive/) | 日本 MIRAI HTTPS RINEX 归档（含 QZSS） | data-portal | — | 🏷️ 官方 |
| [Korea-GNSS-Data](https://www.gnssdata.or.kr/) | 韩国多机构 CORS 事后 RINEX 门户 | data-portal | — | 🏷️ 官方 |
| [NOAA-UFCORS](https://geodesy.noaa.gov/UFCORS/) | NGS UFCORS：按需裁剪美国 CORS RINEX | data-portal | — | 🏷️ 官方 |
| [NRCan-CACS](https://webapp.csrs.nrcan.gc.ca/geod/data-donnees/cacs-scca.php) | 加拿大 CACS 连续 GNSS 网 RINEX 门户 | data-portal | — | 🏷️ 官方 |
| [RENAG](https://renag.resif.fr/) | RENAG：法国国家永久 GNSS 网数据与元数据门户 | data-portal | — | 🏷️ 官方 |
| [Spain-IGN-ERGNSS](https://datos-geodesia.ign.es/ERGNSS/) | 西班牙 IGN ERGNSS 公开 GNSS 数据目录 | data-portal | — | 🏷️ 官方 |
| [SWEPOS-RINEX](https://www.lantmateriet.se/en/geodata/gps-geodesy-and-swepos/lantmateriets-doi-objects/swepos-rinex-data/) | SWEPOS：瑞典国家 GNSS 参考网 RINEX 开放数据 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BEV-APOS](https://www.bev.gv.at/Services/Produkte/Grundlagenvermessung/APOS.html)  
*🏷️ 官方*

语言：data-portal · 许可：CC-BY-4.0 (APOS-PP) · 星标约：— · 宿主：official_site

奥地利联邦计量与测量局（BEV）运营的 Austrian Positioning Service。APOS-PP 提供约 40 站 GPS/GLO/GAL/BDS 的 RINEX（1 s / 30 s）事后数据，经 Geoportal 免费下载且无需注册，许可为 CC BY 4.0；实时 RTK/DGPS/RAW 为收费或需注册服务。站网按 EUREF Class A 维护，坐标参考 ETRS89。适合中欧区域 CORS 对照与教学；实时改正不在免费范围内。英文产品说明页见 BEV 官网 English 栏目。

#### [GeoNet-Data-API](https://data.geonet.org.nz/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GeoNet 面向自动化拉取的稳定 Data API（data.geonet.org.nz）：浏览/下载原始数据与产品；GNSS RINEX 位于 /v1/data/gnss/rinex/（另有 1 Hz 路径）。支持 gzip Accept-Encoding。旧兼容端点计划于 2026 年底退役，脚本应迁移到 /v1/data/。数据自由开放，使用前需阅读 Data Policy/Disclaimer 并引用数据集 DOI。与已收录的 GeoNet 大地测量说明页互补（门户介绍 vs 机器接口）。

#### [GeoNet-NZ-Geodetic](https://www.geonet.org.nz/data/types/geodetic)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GeoNet 大地测量数据说明入口，链向新西兰 GNSS 等产品的获取方式，是西南太平洋区域研究常用门户。具体 RINEX/产品树以其子链为准；使用请遵守 GeoNet 数据许可。

#### [IBGE-RBMC](https://www.ibge.gov.br/en/geosciences/geodetic-network/2421-rbmc.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

巴西国家地理统计局 RBMC 连续监测网介绍页，是获取巴西 CORS/RINEX 的官方入口之一。南美电离层与低纬闪烁研究常用。实际文件下载常转到 IBGE 数据服务子站，请按页面当前链接注册或检索。

#### [IBGE-RBMC-API](https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IBGE 服务数据文档中的 RBMC API（v1），提供 rinex2/rinex3 及 1 秒高采样等端点，便于脚本化拉取巴西连续监测网。与已收录的 RBMC 介绍页互补，本条专指可编程接口。遵守 IBGE 服务条款与礼貌访问；端点路径/版本以文档为准。

#### [Japan-MIRAI-Archive](https://go.gnss.go.jp/mirai/miraiarchive/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

日本内阁府 GO!GNSS 门户的 MIRAI 归档，提供按年积日组织的 RINEX 3/4 观测与导航文件（含 Hatanaka 压缩），可用 wget/curl 批量拉取，并提供日文件 list。相对 GSI GEONET 传统申请制，该入口对注册用户更友好，适合日本及周边电离层案例。须注册账号；QZSS L1C/B 等细节见页面说明。

#### [Korea-GNSS-Data](https://www.gnssdata.or.kr/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

韩国 GNSS 数据服务门户汇聚国土地理院、海洋定位、气象与科研等机构参考站，提供事后 RINEX 打包下载（单次跨度常有上限）。适合朝鲜半岛及周边区域电离层/定位验证。需网页注册登录；具体可下载台站与保留策略以站点现行说明为准。

#### [NOAA-UFCORS](https://geodesy.noaa.gov/UFCORS/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国 NGS 提供的 User Friendly CORS 网页服务，可按站与时段请求部分日、跨日拼接或降采样的 RINEX，免手工拼 CORS 目录。与已收录的 CORS 数据树/AWS 桶互补，偏交互取数。属门户服务（portal-terms）；大批量科研抓取仍建议用 NODD/S3 或 corsdata 目录并限速。

#### [NRCan-CACS](https://webapp.csrs.nrcan.gc.ca/geod/data-donnees/cacs-scca.php)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

加拿大自然资源部 CSRS 门户提供的 Canadian Active Control System 数据入口，可按站选取并下载 RINEX 观测与元数据，亦分发部分精密星历/钟差选项。北美高纬与极区电离层、地壳形变研究常用。收录前已 HTTP 核验页面可访问；批量下载请遵守 NRCan 礼貌访问与引用要求。

#### [RENAG](https://renag.resif.fr/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

法国 RÉNAG（Réseau National GNSS permanent）官方站点，挂靠 RESIF，提供永久站信息、数据政策、可用性/质量说明、实时与产品入口（doi:10.15778/resif.rg）。科研用户可由此定位法国开放 GNSS 观测。具体下载协议与许可证以站方/RESIF 声明为准，不是解算软件。

#### [Spain-IGN-ERGNSS](https://datos-geodesia.ign.es/ERGNSS/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

西班牙国家地理研究所大地测量数据服务器上的 ERGNSS 目录，提供国家连续 GNSS 网相关文件的开放索引（亦可见 EUREF/IGS 等并列目录）。西欧中纬电离层与区域网研究可作补充源。目录型 HTTPS 访问；子目录结构与文件命名以站点为准，批量抓取请限速。

#### [SWEPOS-RINEX](https://www.lantmateriet.se/en/geodata/gps-geodesy-and-swepos/lantmateriets-doi-objects/swepos-rinex-data/)  
*🏷️ 官方*

语言：data-portal · 许可：CC0-1.0 · 星标约：— · 宿主：official_site

瑞典测绘局 Lantmäteriet 运营的 SWEPOS 连续运行参考站观测数据门户（DOI 10.23701/c5tc-ew52），提供日文件 RINEX 2/3，FTP/SFTP 开放获取并标注 CC0。需按站方说明注册后访问。适合北欧区域网与科研对照；实时流/精密产品权限另见 SWEPOS 服务条款。

## 闪烁/ISMR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ISMR-Query-Tool](https://ismrquerytool.fct.unesp.br/) | UNESP ISMR 闪烁数据查询工具 | data-portal | — | 🏷️ 高校实验室 核心 |

### 详细说明

#### [ISMR-Query-Tool](https://ismrquerytool.fct.unesp.br/)  
*🏷️ 高校实验室 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

圣保罗州立大学等维护的 ISMR Query Tool，用于查询/获取 GNSS 闪烁监测接收机（ISMR）相关数据，服务低纬闪烁与 CIGALA/CALIBRA 一类研究。站点曾变更域名或证书，若打不开请用 HTTP 或项目组当前公布地址；配合仓内 ismr_downloader 软件条目使用。

## 在线解算

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [CSRS-PPP](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php?locale=en) | NRCan CSRS-PPP：官方免费在线精密单点定位 | data-portal | — | 🏷️ 官方 |
| [IBGE-PPP-API](https://servicodados.ibge.gov.br/api/docs/ppp?versao=1) | IBGE-PPP REST：巴西在线精密单点定位 API | data-portal | — | 🏷️ 官方 |
| [NGS-OPUS](https://www.ngs.noaa.gov/OPUS/) | NGS OPUS 在线静态精密定位服务 | data-portal | — | 🏷️ 官方 |
| [NGS-OPUS-Projects](https://geodesy.noaa.gov/OPUS-Projects/OpusProjects.shtml) | NGS OPUS Projects：多站控制网在线处理 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [CSRS-PPP](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php?locale=en)  
*🏷️ 官方*

语言：data-portal · 许可：Open Government Licence - Canada · 星标约：— · 宿主：official_site

NRCan 加拿大大地测量处长期运营的 CSRS-PPP Web 服务：提交 RINEX 后返回位置/轨迹、对流层天顶延迟与接收机钟差等产品，支持静态/动态与多参考框架。数据与产品适用 Open Government Licence – Canada；使用需登录免费账户。2026 年起对部分历史观测切换 IGS Repro3 产品（见服务更新页）。引擎本身不开源，但属广泛引用的官方免费科学服务；批量可用官方脚本接口（申请发放）。与 IBGE-PPP（下游封装）及本地开源 PPP 套件互补。

#### [IBGE-PPP-API](https://servicodados.ibge.gov.br/api/docs/ppp?versao=1)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

巴西 IBGE 公开的 PPP REST API：上传 RINEX（含 Hatanaka）后由后端调用 NRCan CSRS-PPP，返回 SIRGAS2000/ITRF 坐标与不确定度。适合南美区域事后 PPP 批处理；配额、字段与授权条款以 IBGE 文档为准，不是本地开源引擎。

#### [NGS-OPUS](https://www.ngs.noaa.gov/OPUS/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

NGS Online Positioning User Service：用户上传双频静态观测，由 NGS 处理返回 ITRF/NAD83 等坐标与质量报告，广泛用于北美控制点检核。免费科学/工程门户，不是开源解算源码。文件长度、天线型号与共享选项以现行 OPUS 说明为准；动态/实时需求请改用其他服务。

#### [NGS-OPUS-Projects](https://geodesy.noaa.gov/OPUS-Projects/OpusProjects.shtml)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

美国国家大地测量局（NGS）OPUS Projects 5.x：面向多测站、多时段控制网的在线管理与处理（PAGES 套件），可视化会话并与国家空间参考系统（NSRS）约束平差。创建项目通常需完成官方培训并注册为项目管理者；若要入库 NGS IDB 还需项目跟踪号与 WinDesc 点之记。属官方免费科学/测绘服务（非 OSI 源码发行）。与已收录的单站 OPUS 互补；NSRS 数据元切换节点请关注 NGS 公告。

## 元数据

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [M3G](https://gnss-metadata.eu/landing/m3g) | EUREF/EPOS M3G：多网 GNSS 站元数据与 API | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [M3G](https://gnss-metadata.eu/landing/m3g)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

比利时皇家天文台（ROB）为 EPOS/EPN 及加密网维护的 Metadata Management and Distribution System for Multiple GNSS Networks。支持 IGS 风格站点日志上传校验、网络/DOI/名义数据供给与许可等元数据分发；公开 REST API（文档见 gnss-metadata.eu 与 m3g-rob.github.io）。科研侧常用来程序化拉取欧洲参考站元数据。系统本体未必整仓开源；数据访问遵循站方声明许可。DOI: 10.24414/ROB-GNSS-M3G。

## 国际联盟

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EPOS-GNSS](https://gnss-epos.eu/) | EPOS GNSS TCS：欧洲 GNSS 数据与产品门户 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EPOS-GNSS](https://gnss-epos.eu/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EPOS GNSS Thematic Core Service 官方门户，汇总欧洲 GNSS 观测、坐标时间序列、速度场与应变等产品入口，并链向 Data/Products Gateway、M3G 与各节点（ROB、INGV、UGA-CNRS、SGO-EPND 等）。适合从科研工作流入口定位欧洲开源/开放 GNSS 资产。具体下载权限与许可以各节点与数据集声明为准；程序化访问优先看配套 GLASS API。

## 数据接口

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EPOS-GLASS-API](https://gnssdata-epos.oca.eu/GlassFramework/) | EPOS GLASS API：欧洲 GNSS RINEX/元数据 REST | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EPOS-GLASS-API](https://gnssdata-epos.oca.eu/GlassFramework/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

由 UBI、ROB、CNRS-OCA、INGV 等在 EPOS 框架下开发的 GLASS Framework API（OCA 节点实例），提供 GNSS 台站、高采样/常规 RINEX 元数据及下载 URL 等 REST 接口（JSON/XML/CSV 等）。开发说明见 GlassFramework/about.html；Swagger 亦可经 EPOS GNSS 门户进入。适合脚本化检索欧洲节点观测而不必手工翻 FTP。账号/配额与站级许可以节点策略为准；不是定位解算器。

## IGS数据中心

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GFZ-ISDC-Data-HTTPS](https://isdc-data.gfz.de/gnss/) | GFZ ISDC GNSS HTTPS 归档（新旧 FTP 迁移） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [GFZ-ISDC-Data-HTTPS](https://isdc-data.gfz.de/gnss/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

德国地学研究中心（GFZ）Information System and Data Center 的 GNSS HTTPS 数据根：/gnss/data/daily、/highrate 等目录提供日文件与高采样观测及产品树，匿名 HTTPS 浏览下载。IGSMail 等通告已推动从旧 FTP 迁移至此主机（旧 FTP 计划关停）。与已收录的 isdc.gfz-potsdam.de 门户页互补——本条指向可直接 wget/curl 的数据树。使用请遵守 GFZ/ISDC 数据政策并引用相应 DOI。
