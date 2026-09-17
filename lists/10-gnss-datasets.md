# GNSS 数据源 / GNSS Datasets
> 共 **56** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

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
| [BKG-IGS-Data-Center](https://igs.bkg.bund.de/) | BKG IGS 数据中心：欧洲侧 GNSS 数据与 NTRIP 入口 | data-portal | — | 🏷️ 官方 · 核心 |
| [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/) | NASA CDDIS：IGS 全球 GNSS 观测与产品主归档之一 | data-portal | — | 🏷️ 官方 · 核心 |
| [ESA-GSSC](https://gssc.esa.int/) | ESA GNSS Science Support Centre：科学数据与产品门户 | data-portal | — | 🏷️ 官方 · 核心 |
| [GFZ-ISDC](https://isdc.gfz-potsdam.de/) | GFZ ISDC：波茨坦地球科学研究数据中心门户 | data-portal | — | 🏷️ 官方 |
| [IGS-Data-Access](https://igs.org/data-access/) | IGS 数据访问页：全球数据中心与获取方式一览 | data-portal | — | 🏷️ 官方 |
| [IGS-Home](https://igs.org/) | 国际 GNSS 服务（IGS）官网：产品、工作组与数据中心总入口 | data-portal | — | 🏷️ 官方 · 核心 |
| [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/) | NASA Earthdata 统一登录：CDDIS 等地球科学数据下载的前置账号 | data-portal | — | 🏷️ 官方 · 核心 |
| [SOPAC-CSRC](https://sopac-csrc.ucsd.edu/) | SOPAC/CSRC：Scripps 轨道与永久阵列中心门户 | data-portal | — | 🏷️ 官方 |
| [SOPAC-Garner-Pub](https://garner.ucsd.edu/pub/) | SOPAC garner 公共目录：产品与相关文件树 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [BKG-IGS-Data-Center](https://igs.bkg.bund.de/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

德国联邦制图与大地测量局维护的 IGS 数据中心门户，同时提供文件下载与实时播发相关入口，是欧洲用户常用镜像与 caster 起点。实时 NTRIP 与事后文件通道彼此独立，配置账号时不要把 caster 凭证与 HTTPS 下载混用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-GNSS-Archive](https://cddis.nasa.gov/archive/gnss/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IGS 核心数据中心，提供日/小时 RINEX、广播星历、精密 SP3/CLK、IONEX 与偏差等产品。目录按年积日或 GPS 周组织，文件多为压缩格式。适合全球网事后处理与电离层研究。匿名 FTP 已停用，必须 Earthdata 登录；大流量请限速，并核对长文件名规范与校验信息。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [ESA-GSSC](https://gssc.esa.int/)  
*🏷️ 官方 · 核心*

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

#### [IGS-Home](https://igs.org/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

IGS 官方门户，链向产品规范、分析中心、全球/区域数据中心以及实时服务说明。站点本身通常不直接托管海量 RINEX。适合查阅标准文件名、站点日志格式与政策文件。实际观测与产品下载请转到 CDDIS、BKG、ESA GSSC 等归档系统。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [NASA-Earthdata-Login](https://urs.earthdata.nasa.gov/)  
*🏷️ 官方 · 核心*

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
| [GIRO-DIDBase](https://giro.uml.edu/didbase/) | GIRO DIDBase：全球电离层测高仪数据库 | data-portal | — | 🏷️ 官方 · 核心 |
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
*🏷️ 官方 · 核心*

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
| [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/) | 中科院 CAS 电离层 IONEX 产品（data.bdsmart.cn） | data-portal | — | 🏷️ 官方 · 核心 |
| [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html) | CDDIS 大气产品页：电离层 IONEX 与对流层产品索引说明 | data-portal | — | 🏷️ 官方 |
| [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/) | CDDIS IONEX 目录：IGS 及各分析中心全球电离层图 | data-portal | — | 🏷️ 官方 · 核心 |
| [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec) | INGV eSWua 数据库：地中海/欧洲/全球 TEC 现报与预报产品入口 | data-portal | — | 🏷️ 官方 · 核心 |
| [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/) | IGS 电离层工作组：GIM/IAAC 与产品活动入口 | data-portal | — | 🏷️ 官方 |
| [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm) | 意大利 INGV 基于 RING 网的实时 TEC 监测与地图发布页 | data-portal | — | 🏷️ 官方 · 核心 |
| [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/) | JPL 快速 IONEX 发布目录：日更新全球电离层图 | data-portal | — | 🏷️ 官方 · 核心 |
| [UPC-gAGE-FastPPP-Products](https://gage.upc.edu/en/gage-products/fast-ppp-products) | UPC gAGE Fast-PPP 产品页：STEC/IONEX/钟差等申请说明 | data-portal | — | 🏷️ 高校实验室 |
| [UPC-IONEX-Archive](https://cabrera.upc.edu/upc_ionex_GPSonly-RINEXv3/) | UPC 电离层 IONEX 归档目录（分年） | data-portal | — | 🏷️ 高校实验室 |
| [UPC-IONO4HAS-Products](https://server.gage.upc.edu/iono4has/products.html) | UPC IONO4HAS：面向 HAS 的电离层产品状态页 | data-portal | — | 🏷️ 高校实验室 |
| [WHU-IGS-Ionosphere-AC](https://panda.whu.edu.cn/yjpt/IGSdlcfxzx.htm) | 武汉大学 IGS 电离层分析中心：GIM/DCB/ROTI 产品说明 | data-portal | — | 🏷️ 高校实验室 · 核心 |

### 详细说明

#### [CAS-BDsmart-Iono-Products](https://data.bdsmart.cn/pub/product/iono/ionex/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

中国科学院相关团队发布的多 GNSS GIM HTTPS 目录，用于接替旧 FTP，提供快速与最终等 IONEX 产品。东亚与全球电离层研究常用来源之一。同步到 IGS 数据中心可能存在时延差；请将脚本迁移到新域名，勿再依赖已宣布停用的旧 FTP。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-Atmospheric-Products](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

汇总 IGS 电离层 GIM（IONEX）与对流层相关产品在 CDDIS 的存放说明，并解释新旧文件名对应关系。面向 TEC/ZTD 用户快速定位路径。实际数据文件仍在 archive 树中按日或周存放。Rapid 与 Final 时延不同，引用时应注明分析中心与产品类型。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [CDDIS-IONEX](https://cddis.nasa.gov/archive/gnss/products/ionex/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

存放 IGS 综合与各电离层分析中心的 GIM、ROTI 等 IONEX 文件，按年份与年积日组织。是 GNSS 电离层事后研究最常用入口之一。下载需登录；注意 Final、Rapid 与预测产品的时延及格网分辨率差异，并结合码偏差/OSB 产品一起使用以免系统差。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [eSWua-TEC](http://www.eswua.ingv.it/ewphp/landing.php?doi=tec)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：CC-BY-4.0 · 星标约：— · 宿主：official_site

INGV「电子空间天气高层大气」数据库中的 TEC 专题（DOI:10.13127/eswua/tec，CC BY 4.0）。计算中心接入 RING、EUREF 与 IGS 实时/事后观测，7×24 产出地中海、欧洲与全球 TEC 产品。地中海现报（nc_med）即 IONORING 思路的产品化：RING NTRIP 实时流、10 分钟、0.1° 网格、LOWESS、无背景模型以免抹平不规则；另有地中海 30 分钟短期预报、欧洲 TEC/梯度图、全球 NeQuick2 同化现报，以及基于自回归神经网络与预报 Kp 的 24 小时全球预报。站点提供 Download Tool、Web Service 指南与可用性地图；示例 REST 如 `http://ws-eswua.rm.ingv.it/tecdb.php/records/wsnc_med?filter=dt,eq,YYYY-MM-DD%20HH:MM:SS`，返回 JSON 网格点（lat/lon/tec）。适合需要意大利/地中海高分辨率实时 TEC 或程序化拉图的用户；不是 GNSS 原始观测归档（RING 原始站数据另循 RING/INGV 渠道）。收录前已核验落地页可访问；使用请按页面引用元数据与 CC BY 4.0。

#### [IGS-Ionosphere-WG](https://igs.org/wg/ionosphere/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

介绍 IGS 电离层联合产品机制、各分析中心角色以及相关会议与试点活动。适合了解 CODE、JPL、UPC、CAS、WHU 等 IAAC 分工。页面不直接存储 IONEX 文件。综合产品与单中心产品在精度和时延上不同，研究中应分开评估与引用。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [IONORING](http://ionos.ingv.it/ionoring/ionoring.htm)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

意大利国家地球物理与火山学研究所（INGV）上层大气物理组维护的实时电离层 TEC 监测页。系统利用 RING（Rete Integrata Nazionale GNSS）约 40 个测站的双频观测，在 IPP 上估计 VTEC 后用 LOWESS 插值，生成覆盖约 35°N–48°N、5°E–20°E 的 0.1°×0.1° 网格图，约每 10 分钟刷新，典型时延低于 1 分钟。论文（Remote Sensing 2021）与 IGS GIM、比利时 ROB 欧洲图对比，RMSE 约 2–3 TECu，并讨论了 2017 年 X9.3 耀斑与随后地磁暴期间的区域响应，以及用于单点定位改正时相对 Klobuchar/GIM 的改善。本页主要展示最新地图与近 24 小时动画，不是开源处理软件仓库；算法与产品说明见论文。批量历史产品与 Web 服务请转到同组的 eSWua TEC 数据库（DOI:10.13127/eswua/tec）。收录时已 HTTP 核验页面可访问；使用与引用请遵守 INGV/论文要求。

#### [JPL-IONEX-Rapid](https://sideshow.jpl.nasa.gov/pub/iono_daily/IONEX_rapid/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

JPL 侧快速电离层图公开目录，文件为 IONEX 风格，适合需要较短时延 GIM 的科研与监测。其结果与 IGS 综合 Final 存在差异，不可直接等同。部分机构网络可能拦截 sideshow 域名；重要任务建议同时备份 CDDIS 路径中的同系列产品。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

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
*🏷️ 高校实验室 · 核心*

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
| [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html) | CODE/AIUB 分析中心主页：精密轨道钟差与电离层等产品介绍 | data-portal | — | 🏷️ 官方 · 核心 |
| [GFZ-GNSS-Services](https://gnss.gfz.de/services) | GFZ GNSS 服务页：产品与在线服务入口 | data-portal | — | 🏷️ 官方 |
| [GFZ-ISDC-GNSS-Products](https://isdc.gfz-potsdam.de/gnss-products/) | GFZ ISDC GNSS 产品专页 | data-portal | — | 🏷️ 官方 |
| [IGS-MGEX](https://igs.org/mgex/) | IGS MGEX：多 GNSS 试验网与多星座产品介绍 | data-portal | — | 🏷️ 官方 |
| [IGS-Products](https://igs.org/products/) | IGS 产品页：轨道、钟差、ERP、偏差、电离层等规范说明 | data-portal | — | 🏷️ 官方 · 核心 |

### 详细说明

#### [CODE-AIUB-Analysis-Center](https://www.aiub.unibe.ch/research/code___analysis_center/index_eng.html)  
*🏷️ 官方 · 核心*

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
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

定义 IGS 轨道、钟差、ERP、偏差与大气等产品类型、时延等级以及长文件名规则，是科研引用与脚本命名的权威参考。文件本体存放在各数据中心。务必注意约 GPS 周 2238 前后的命名切换，旧流水线需要同步适配新模式。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

## 掩星

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/) | COSMIC CDAAC：GNSS 无线电掩星大气/电离层产品 | data-portal | — | 🏷️ 官方 · 核心 |
| [COSMIC-GNSS-RO-Data](https://data.cosmic.ucar.edu/gnss-ro/) | COSMIC GNSS-RO 公开数据目录 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [COSMIC-CDAAC](https://cdaac-www.cosmic.ucar.edu/)  
*🏷️ 官方 · 核心*

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
| [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss) | EarthScope GAGE GNSS 归档：北美及合作站观测数据 | data-portal | — | 🏷️ 官方 · 核心 |
| [EarthScope-Home](https://www.earthscope.org/) | EarthScope 主页：原 UNAVCO/IRIS 合并后的地球科学联盟入口 | data-portal | — | 🏷️ 官方 |
| [EUREF-EPN-CB](https://www.epncb.oma.be/) | EUREF EPN 中央局：欧洲参考站网数据与产品 | data-portal | — | 🏷️ 官方 · 核心 |
| [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/) | EPN 观测数据 FTP/Web 目录 | data-portal | — | 🏷️ 官方 |
| [GA-GNSS-Data](https://data.gnss.ga.gov.au/) | Geoscience Australia GNSS 数据门户（AUSCORS 等） | data-portal | — | 🏷️ 官方 · 核心 |
| [HongKong-SatRef](https://www.geodetic.gov.hk/en/satref/satref.htm) | 香港 SatRef：卫星定位参考站网介绍 | data-portal | — | 🏷️ 官方 |
| [HongKong-SatRef-RINEX](https://www.geodetic.gov.hk/en/rinex/rinex.htm) | 香港 SatRef RINEX 数据说明与下载 | data-portal | — | 🏷️ 官方 |
| [IGN-Geodesie](https://geodesie.ign.fr/) | 法国 IGN 大地测量门户（RGP 等相关入口） | data-portal | — | 🏷️ 官方 |
| [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/) | NOAA CORS 数据目录树 | data-portal | — | 🏷️ 官方 |
| [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/) | NOAA NGS CORS：美国连续运行参考站网数据门户 | data-portal | — | 🏷️ 官方 · 核心 |
| [SIRGAS-Home](https://www.sirgas.org/en/) | SIRGAS：拉丁美洲大地参考架与 GNSS 网门户 | data-portal | — | 🏷️ 官方 |
| [SONEL](https://www.sonel.org/) | SONEL：全球海平面观测网（含 GNSS 并址站） | data-portal | — | 🏷️ 官方 |
| [UNAVCO-GPS-GNSS-Data](https://www.unavco.org/data/gps-gnss/gps-gnss.html) | UNAVCO 遗留 GNSS 数据页（导向 EarthScope/GAGE） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EarthScope-GAGE-GNSS-Archive](https://gage-data.earthscope.org/archive/gnss)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

GAGE 数据系统上的 GNSS 归档入口，承接原 UNAVCO 测站 RINEX 等产品，广泛用于构造、火山、水文与电离层研究。北美及合作网密度高、时间跨度长。登录与接口策略可能调整，编写脚本前应用浏览器确认当前权限模型与路径。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EarthScope-Home](https://www.earthscope.org/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EarthScope 联盟门户，汇总地球物理与大地测量设施、项目与数据政策信息。具体 GNSS 文件检索在 GAGE 数据系统完成。历史上 UNAVCO 品牌页面多会重定向到此处。寻找 RINEX 时请优先使用 gage-data.earthscope.org 归档链接。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。

#### [EUREF-EPN-CB](https://www.epncb.oma.be/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

欧洲 EPN 中央局官方门户，提供测站信息、观测文件与产品相关入口，是欧洲大地参考框架网的核心数据枢纽。适合区域 PPP、形变与电离层研究。实时流与事后文件渠道分离；使用高采样数据时注意存储容量并遵循 EPN 引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [EUREF-EPN-Obs-FTP](https://epncb.oma.be/ftp/obs/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EPN 测站观测文件目录，便于按站名直接下载 RINEX，是欧洲区域研究的高频访问路径。目录组织相对稳定，但测站列表会增减。批量下载前应对照中央局站点状态页，剔除长期停测或仅测试用途的测站。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [GA-GNSS-Data](https://data.gnss.ga.gov.au/)  
*🏷️ 官方 · 核心*

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

#### [NOAA-CORS-Data-Tree](https://geodesy.noaa.gov/corsdata/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

CORS 观测文件目录树入口，便于按测站、年份与年积日批量抓取公开 RINEX。面向自动化流水线。请控制并发与请求频率，遵守 NOAA 使用政策，并在本地做好缓存与校验，以免重复冲击服务器。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。

#### [NOAA-NGS-CORS](https://geodesy.noaa.gov/CORS/)  
*🏷️ 官方 · 核心*

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
| [IGS-RTS](https://igs.org/rts/) | IGS 实时服务（RTS）：实时轨道钟差/SSR 流说明 | data-portal | — | 🏷️ 官方 · 核心 |

### 详细说明

#### [IGS-RTS](https://igs.org/rts/)  
*🏷️ 官方 · 核心*

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
| [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/) | TU Wien VMF 对流层格网数据目录（与 /codes 源码区分） | data-portal | — | 🏷️ 官方 · 核心 |

### 详细说明

#### [VMF-Data-Server-TropProducts](https://vmf.geo.tuwien.ac.at/trop_products/)  
*🏷️ 官方 · 核心*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

维也纳工大 VMF 服务的对流层产品目录树，提供 VMF1/VMF3 等格网，供 PPP 与 VLBI 映射函数使用。本条强调数据产品，源码实现见同站 /codes（软件类另收）。选用时注意格网版本与气象模型匹配；业务系统还需确认更新节奏与文献引用要求。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。
