# QC audit — 2026-09-26 batch 51 (category/subcategory audit, text artifacts)

Base: `2a18cfc` (batch 50 ended at `e3656b0`; `2a18cfc` is a peer docs commit — docs/data-access.md, docs/software/* — no catalog change). Project total 1029 unchanged; provenance 331/214/484 unchanged; no entries added or removed; no duplicates found (no RETIRED_URLS change).

## Task 0 — entries newer than e3656b0

None. The only newer commit (`2a18cfc`) touches docs only.

## Task 1 — category/subcategory audit (whole catalog)

Method: dumped all 1029 entries by category/subcategory with desc_zh/analysis_zh; checked each against docs/categories.md blurbs and against same-kind siblings. Subcategories are free text in the generator (`regenerate_lists` groups by `subcategory`), so merging into an existing sibling needs no code change. No new subcategory names were created. `中性大气` already existed.

Result: **206 entries reclassified**. **42 changed category**, 164 changed subcategory only. Distinct (category, subcategory) groups went from 317 to 178; singleton groups went from 190 to 46.

| category | before | after |
|---|---:|---:|
| ionosphere | 298 | 273 |
| troposphere | 49 | 48 |
| gnss-data | 138 | 137 |
| gnss-positioning | 106 | 108 |
| orbit-clock | 31 | 31 |
| navigation-ins | 73 | 72 |
| gnss-sdr | 76 | 76 |
| mobile-apps | 32 | 32 |
| tools-learning | 57 | 57 |
| gnss-datasets | 169 | 195 |
| **total** | 1029 | 1029 |

### Cross-category moves

| idx | name | from | to | reason |
|---:|---|---|---|---|
| 28 | gLAB | gnss-data/处理/教学 | gnss-positioning/教学/PPP套件 | gLAB mirror; official gLAB-UPC/gLAB-Download in gnss-positioning/教学/PPP套件 |
| 82 | swds-api-downloader | gnss-data/下载 | ionosphere/数据接口 | space-weather data API downloader; sibling geomagindices |
| 910 | pysatCDF | gnss-data/CDF读取 | ionosphere/工具 | pysat CDF reader; pysat family in ionosphere/工具, not GNSS format |
| 47 | nmea-msgs | gnss-data/RTCM/NTRIP | navigation-ins/ROS驱动 | ROS NMEA msgs, not RTCM/NTRIP; same org as nmea_navsat_driver |
| 85 | UNAVCO-Preprocessing | gnss-data/预处理索引 | tools-learning/机构软件门户 | software navigation page; sibling UNAVCO-Software-Portal |
| 145 | VMF-Data-Server-TropProducts | gnss-datasets/对流层 | troposphere/VMF产品 | TU Wien VMF product directory; siblings VMF3/VMF1-GNSS-Products in troposphere/VMF产品 |
| 469 | SbfMixer | ionosphere/工具 | gnss-data/接收机驱动 | Septentrio receiver data tool, no ionosphere function |
| 476 | Septentrio-PyDataLink | ionosphere/工具 | gnss-data/接收机驱动 | Septentrio receiver data link tool, no ionosphere function |
| 872 | ISGI | ionosphere/地磁指数 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 886 | SWS-Geophysical | ionosphere/地磁地球物理 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 888 | SWPC-WSA-Enlil | ionosphere/太阳风预报 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 891 | SpaceWeather-Canada | ionosphere/国家空间天气 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 898 | SIDC | ionosphere/太阳空间天气 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 899 | SILSO | ionosphere/太阳黑子指数 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 900 | Kyoto-Dst-Realtime | ionosphere/Dst指数 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 901 | Kyoto-Kp-Index | ionosphere/Kp历史 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 902 | SWPC-GOES-Xray | ionosphere/GOES-X射线 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 903 | SWPC-Solar-Cycle | ionosphere/太阳周 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 904 | SWS-Solar | ionosphere/太阳活动 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 905 | GFZ-Kp-Data | ionosphere/Kp数据API | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 930 | SWPC-ACE-RTSW | ionosphere/太阳风实时 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 931 | LISIRD | ionosphere/太阳辐照 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 932 | BGS-INTERMAGNET-Data | ionosphere/地磁数据 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 933 | NGDC-GOES-Satellite | ionosphere/GOES存档 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 940 | SDO-GSFC | ionosphere/太阳观测 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 941 | SOHO-NASA | ionosphere/太阳观测 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 942 | CCMC-DONKI | ionosphere/空间天气事件 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 943 | Helioviewer | ionosphere/太阳可视化 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 944 | Kyoto-AE-Realtime | ionosphere/AE指数 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 945 | SWPC-Real-Time-Solar-Wind | ionosphere/太阳风实时 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 946 | SWPC-GOES-Proton-Flux | ionosphere/GOES质子 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 958 | SWPC-Solar-Synoptic-Map | ionosphere/太阳观测 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 959 | SWPC-Solar-Geophysical-Event-Reports | ionosphere/空间天气事件 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 974 | CCMC-ISWA | ionosphere/空间天气分析 | gnss-datasets/地磁空间天气 | space-weather/solar/geomagnetic data portal, not ionosphere software; siblings NOAA-SWPC, BoM-SWS, GFZ-Kp-Index, OMNIWeb already in gnss-datasets/地磁空间天气 |
| 956 | NOAA-EMM | ionosphere/地磁模型 | tools-learning/地磁模型 | geomagnetic model portal; sibling NOAA-WMM-Portal |
| 660 | NTRIP_ROS | navigation-ins/车载与机器人 | gnss-data/ROS NTRIP客户端 | ROS NTRIP client; sibling ntrip_client-MicroStrain |
| 536 | GVINS-Dataset | navigation-ins/数据集 | tools-learning/数据集 | dataset; tools-learning/数据集 holds awesome-gins-datasets, UrbanNavDataset |
| 848 | piksi_tools | tools-learning/接收机工具 | gnss-data/接收机驱动 | Piksi receiver config/log tool; sibling libsbp in gnss-data |
| 876 | SWPC-Services | tools-learning/空间天气API | gnss-datasets/地磁空间天气 | SWPC machine-readable data directory; sibling NOAA-SWPC in gnss-datasets/地磁空间天气 |
| 584 | EasyGNSS | tools-learning/可视化 | gnss-positioning/RTK客户端 | RTKLIB touch GUI based on RTKBase/TouchRTKStation; siblings TouchRTKStation, ELT_RTKBase |
| 657 | msise00 | troposphere/大气模型 | ionosphere/中性大气 | NRLMSISE-00 wrapper; same model as Python-NRLMSISE-00/pymsis (ionosphere); thermosphere, not troposphere delay |
| 737 | hwm14 | troposphere/大气模型 | ionosphere/中性大气 | thermosphere wind model; hwm93 in ionosphere; not troposphere delay |

### Subcategory-only moves (same category)

| idx | name | category | from | to | reason |
|---:|---|---|---|---|---|
| 35 | gnsspy | gnss-data | RINEX/工具包 | RINEX读写 | obs read/write toolkit |
| 38 | gnsstools | gnss-data | RINEX/SP3 | RINEX读写 | singleton RINEX/SP3; RINEX/SP3 reader |
| 653 | doris-rinex | gnss-data | RINEX/SP3/格式 | RINEX读写 | singleton; parser like nav-solutions rinex |
| 79 | RTStreamHub | gnss-data | NTRIP/实时流转发 | RTCM/NTRIP | singleton NTRIP/实时流转发 |
| 833 | go-gnss-spartn | gnss-data | Galileo HAS | RTCM/NTRIP | SPARTN, not Galileo HAS; sibling pyspartn |
| 34 | GNSSommelier | gnss-data | IGS产品下载 | 下载 | singleton IGS产品下载; product downloader like GDDS |
| 654 | cddis-highrate-downloader | gnss-data | 下载与质检 | 下载 | singleton 下载与质检; pure downloader |
| 683 | earthscope-sdk | gnss-data | 数据接口 | 下载 | singleton 数据接口; data-access SDK |
| 691 | GNSS_OSI_download | gnss-data | 数据下载 | 下载 | singleton 数据下载 |
| 81 | sp3 | gnss-data | SP3/轨道钟差格式 | 产品读写 | singleton SP3/轨道钟差格式; sibling gnssanalysis |
| 42 | GPSTk | gnss-data | 基础库(归档) | 基础库 | singleton 基础库(归档); archived predecessor of gnsstk |
| 847 | nav-solutions-gnss | gnss-data | Rust定义 | 基础库 | singleton Rust定义; sibling gnss-protos |
| 897 | ublox-rs | gnss-data | UBX-Rust | 基础库 | singleton UBX-Rust; sibling pyubx2 |
| 780 | pcc-explorer | gnss-data | 元数据/SDR | 天线模型 | antenna PCC tool misfiled under 元数据/SDR |
| 781 | atx-scanner | gnss-data | RINEX/工具包 | 天线模型 | ANTEX tool; sibling IGS-Antenna-WG |
| 857 | ublox8-qzss-almanac-converter | gnss-data | 历书转换 | 接收机协议 | singleton 历书转换; same function as ubx-mga-rinex-ephemeris |
| 65 | pysatCDAAC | gnss-data | 掩星/CDAAC解析 | 掩星格式转换 | singleton 掩星/CDAAC解析; RO data handling like cosmic-crunch |
| 664 | GeoNet-NZ-Geodetic | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 665 | IBGE-RBMC | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 674 | NRCan-CACS | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 675 | Japan-MIRAI-Archive | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 676 | Korea-GNSS-Data | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 677 | Spain-IGN-ERGNSS | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 694 | NOAA-UFCORS | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 696 | IBGE-RBMC-API | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 705 | BEV-APOS | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 707 | GeoNet-Data-API | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 724 | SWEPOS-RINEX | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 725 | RENAG | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 743 | OS-Net-DataHub | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 744 | PositioNZ | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 745 | NSGI-RINEX | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 747 | TU-Delft-GNSS-Data | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 950 | CSN-Chile-GPS | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 951 | SIRGAS-Stations | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 953 | EUREF-EPN-Data-Access | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 965 | EUREF-EPN-StationList | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 967 | SIRGAS-Weekly-Solutions | gnss-datasets | 区域CORS | CORS区域网 | 区域CORS is a name variant of CORS区域网 |
| 706 | GFZ-ISDC-Data-HTTPS | gnss-datasets | IGS数据中心 | IGS综合 | IGS数据中心 duplicates IGS综合 (GFZ-ISDC there) |
| 963 | KASI-GNSS-Data-Center | gnss-datasets | IGS数据中心 | IGS综合 | IGS数据中心 duplicates IGS综合 |
| 968 | Earthdata-GNSS | gnss-datasets | 数据中心 | IGS综合 | 数据中心 = CDDIS/Earthdata; siblings CDDIS-GNSS-Archive, CDDIS-Highrate-GNSS |
| 969 | Earthdata-Daily-30s-GNSS | gnss-datasets | 数据中心 | IGS综合 | same as above |
| 859 | LINZ-Geodetic | gnss-datasets | 国家大地测量 | 国家CORS | singleton 国家大地测量; national geodetic/CORS services |
| 915 | ROB-GNSS-be | gnss-datasets | 国家GNSS门户 | 国家CORS | singleton 国家GNSS门户; national GNSS network portal |
| 926 | ASG-EUPOS-Services | gnss-datasets | NRTK服务 | 国家CORS | singleton NRTK服务; sibling ASG-EUPOS |
| 661 | Kyoto-WDC-Geomagnetism | gnss-datasets | 空间天气辅助 | 地磁空间天气 | geomagnetic index/data centre; siblings GFZ-Kp-Index, USGS/BGS geomagnetism |
| 662 | INTERMAGNET | gnss-datasets | 空间天气辅助 | 地磁空间天气 | magnetometer network; siblings USGS/BGS/MACCS/TGO |
| 663 | SuperMAG | gnss-datasets | 空间天气辅助 | 地磁空间天气 | magnetometer network; siblings USGS/BGS/MACCS/TGO |
| 678 | AMBER-Magnetometers | gnss-datasets | 空间天气辅助 | 地磁空间天气 | magnetometer network; siblings USGS/BGS/MACCS/TGO |
| 679 | FMI-IMAGE | gnss-datasets | 空间天气辅助 | 地磁空间天气 | magnetometer network; siblings USGS/BGS/MACCS/TGO |
| 680 | CARISMA | gnss-datasets | 空间天气辅助 | 地磁空间天气 | magnetometer network; siblings USGS/BGS/MACCS/TGO |
| 873 | NASA-CDAWeb | gnss-datasets | 空间物理数据 | 地磁空间天气 | singleton 空间物理数据; sibling NASA-SPDF |
| 875 | UKSSDC | gnss-datasets | 日地物理归档 | 地磁空间天气 | singleton 日地物理归档; sibling NASA-SPDF |
| 885 | SWS-World-Data-Centre | gnss-datasets | WDC数据 | 地磁空间天气 | singleton WDC数据; sibling BoM-SWS |
| 919 | OMNIWeb-Data-Explorer | gnss-datasets | OMNI查询 | 地磁空间天气 | singleton OMNI查询; sibling NASA-OMNIWeb |
| 760 | UNR-NGL | gnss-datasets | IGS产品下载 | 坐标产品 | station time-series/coordinates, not IGS product download |
| 761 | JPL-GPS-Time-Series | gnss-datasets | IGS产品下载 | 坐标产品 | station coordinate time series |
| 87 | awsgnssroutils | gnss-datasets | GNSS掩星/RO | 掩星 | GNSS掩星/RO duplicates 掩星 (COSMIC-CDAAC) |
| 117 | GIRO-DIDBase | gnss-datasets | 地磁空间天气 | 电离层产品 | ionosonde database; sibling RAL Ionosonde (UKSSDC) in 电离层产品 |
| 667 | ISMR-Query-Tool | gnss-datasets | 闪烁/ISMR | 电离层产品 | singleton 闪烁/ISMR; scintillation data = ionosphere product |
| 147 | APAS-TR | gnss-positioning | 多星座PPP | PPP | singleton 多星座PPP |
| 162 | gnss-ppp-matlab-toolbox | gnss-positioning | PPP后处理工具 | PPP | singleton PPP后处理工具 |
| 196 | ppp-tools | gnss-positioning | PPP脚本 | PPP | singleton PPP脚本 |
| 179 | HASPPP | gnss-positioning | PPP/HAS | PPP-RTK/HAS | singleton PPP/HAS |
| 149 | CLASLIB | gnss-positioning | QZSS CLAS PPP-RTK | PPP/PPP-RTK | singleton QZSS CLAS; sibling cssrlib |
| 157 | Ginan-GA-portal | gnss-positioning | PPP套件 | PPP/改正数 | singleton PPP套件; sibling ginan |
| 846 | rt-navi | gnss-positioning | 实时PVT | PVT | singleton 实时PVT |
| 174 | GREAT-PVT | gnss-positioning | PVT/精密定位 | SPP/RTK/PPP | singleton PVT/精密定位 |
| 173 | GraphGNSSLib | gnss-positioning | 因子图RTK | 因子图 | singleton 因子图RTK; siblings GraphGNSSLib_LEO |
| 692 | sidereon-python | gnss-positioning | 定位引擎绑定 | 多功能引擎 | singleton; binding of sidereon |
| 710 | IGP-TUDelft | gnss-positioning | 形变/多源联合 | 大地测量/GNSS | singleton 形变/多源联合 |
| 170 | goGPS_MATLAB | gnss-positioning | 相对定位/PPP | 相对定位 | singleton; sibling goGPS_Java |
| 238 | gnss-baseband | gnss-sdr | 软件接收机 | FPGA相关器 | FPGA correlator cores |
| 923 | SoapyHackRF | gnss-sdr | HackRF插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 924 | SoapyPlutoSDR | gnss-sdr | Pluto插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 934 | SoapyUHD | gnss-sdr | UHD插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 935 | SoapyRTLSDR | gnss-sdr | RTL-SDR插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 936 | SoapyRemote | gnss-sdr | 远程Soapy | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 937 | SoapyAirspy | gnss-sdr | Airspy插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 938 | SoapySDRPlay3 | gnss-sdr | SDRplay插件 | SDR抽象 | SoapySDR module singleton; SoapySDR in SDR抽象 |
| 843 | LANS-AFS-SIM | gnss-sdr | 月面导航仿真 | 信号仿真 | singleton; signal generator |
| 251 | GNSSFirehose | gnss-sdr | 软件接收机 | 射频前端 | RF sampling front-end, not software receiver |
| 263 | GPSMAXIM2769b- | gnss-sdr | 软件接收机 | 射频前端 | front-end hardware design |
| 262 | GPSL1-MMT-DPEmodule | gnss-sdr | 多路径抑制/直接定位 | 直接位置估计 | singleton; sibling GPSL1-DPEmodule |
| 844 | PocketSDR-AFS | gnss-sdr | 月面软件接收机 | 软件接收机 | singleton; software receiver |
| 907 | TEC-Maps-of-Nepal | ionosphere | 区域TEC | GIM | singleton 区域TEC; regional map like Ionospheric-TEC-Kriging-Turkiye |
| 380 | IRI-2020-package | ionosphere | IRI官方模型 | IRI模型 | IRI官方模型 vs IRI模型 split (IRI-2016/2026 packages in IRI模型) |
| 383 | IRI-Fortran | ionosphere | IRI官方模型 | IRI模型 | same |
| 314 | Galileo-NeQuick-G | ionosphere | NeQuick-G官方 | NeQuick官方 | merge NeQuick-G官方 into NeQuick官方 (official NeQuick releases) |
| 418 | NeQuickG-ESSR | ionosphere | NeQuick-G官方 | NeQuick官方 | same |
| 372 | ionotec | ionosphere | TEC计算 | TEC估计 | singleton TEC计算 |
| 688 | Heki-GNSS-TEC-Software | ionosphere | TEC/层析 | TEC估计 | singleton TEC/层析; primarily GNSS STEC |
| 335 | gps-tec-cnn-lstm-attention | ionosphere | TEC估计 | TEC预报/ML | desc/analysis is DL TEC forecasting, not TEC estimation |
| 345 | Ion-Phys-Toolkit | ionosphere | TEC估计 | TEC预报/ML | desc/analysis is DL TEC forecasting, not TEC estimation |
| 432 | PMGC-SimVP | ionosphere | TEC估计 | TEC预报/ML | desc/analysis is DL TEC forecasting, not TEC estimation |
| 487 | TEC-forecast-F107 | ionosphere | TEC估计 | TEC预报/ML | desc/analysis is DL TEC forecasting, not TEC estimation |
| 488 | TEC-MoLLM | ionosphere | TEC估计 | TEC预报/ML | desc/analysis is DL TEC forecasting, not TEC estimation |
| 776 | hwm93 | ionosphere | 模型 | 中性大气 | thermosphere wind model; HWM14 sibling |
| 921 | Python-NRLMSISE-00 | ionosphere | NRLMSISE | 中性大气 | NRLMSISE singleton; MSIS neutral atmosphere |
| 320 | Get_IPP | ionosphere | 穿刺点IPP | 工具 | singleton 穿刺点IPP; MyIonosphere_Library (IPP) in 工具 |
| 673 | DARNtids | ionosphere | TID/扰动 | 工具 | singleton TID/扰动; TID tools (hamsci_LSTID_detection, lstid_processing) in 工具 |
| 868 | pysatNASA | ionosphere | 空间数据接口 | 工具 | singleton 空间数据接口; pysat family in 工具 |
| 909 | pysatMissions | ionosphere | 任务规划 | 工具 | singleton 任务规划; pysat family in 工具 |
| 395 | ismr_downloader | ionosphere | 闪烁数据 | 数据接口 | singleton 闪烁数据; download client |
| 500 | viresclient | ionosphere | SWARM/LEO TEC | 数据接口 | singleton SWARM/LEO TEC; data-access client like madrigalWeb |
| 396 | ITU-R-iono-tropo-software | ionosphere | 传播模型 | 模型 | singleton 传播模型; propagation model software |
| 464 | SAMI3-3.22-Zenodo | ionosphere | 物理模式 | 模型 | singleton 物理模式; siblings SAMI3-* |
| 877 | CCMC-Home | ionosphere | 空间天气模型 | 模型 | singleton 空间天气模型; siblings CCMC-SAMI3, HAO-TGCM-portal |
| 908 | NCAR-GLOW | ionosphere | 气辉模型 | 模型 | singleton 气辉模型; ionization/airglow model like AURORA, transcar |
| 325 | GIRO-portal | ionosphere | 测高仪/同化 | 电离层产品 | singleton 测高仪/同化; ionosonde data portal |
| 871 | SWS-BOM-Satellite | ionosphere | 闪烁与TEC | 电离层产品 | singleton 闪烁与TEC; ionosphere product navigation |
| 884 | SWS-HF-Systems | ionosphere | 电离层HF | 电离层产品 | singleton 电离层HF; ionosphere product navigation |
| 887 | SWPC-D-RAP | ionosphere | D区吸收 | 电离层产品 | singleton D区吸收; ionosphere product page like NOAA-SWPC-GloTEC |
| 286 | Autoscala-INGV | ionosphere | 测高仪自动缩放 | 电离层工具 | singleton 测高仪自动缩放; ionosonde tools SAO-Explorer etc. |
| 854 | ionFR | ionosphere | 法拉第旋转 | 电离层工具 | singleton 法拉第旋转; siblings RMextract, spinifex (Faraday rotation) |
| 878 | NeoGPS | mobile-apps | Arduino解析 | Arduino-NMEA | singleton Arduino解析 |
| 646 | SparkFun_u-blox_GNSS_v3 | mobile-apps | 嵌入式/Arduino | 嵌入式 | embedded singleton; siblings ubxlib, SparkFun Unicore |
| 851 | QZQSM | mobile-apps | QZSS嵌入式 | 嵌入式 | embedded singleton; siblings ubxlib, SparkFun Unicore |
| 856 | gnsshat | mobile-apps | 树莓派GNSS | 嵌入式 | embedded singleton; siblings ubxlib, SparkFun Unicore |
| 879 | UbxGps | mobile-apps | UBX通信 | 嵌入式 | embedded singleton; siblings ubxlib, SparkFun Unicore |
| 880 | bolderflight-ublox | mobile-apps | uBlox驱动 | 嵌入式 | embedded singleton; siblings ubxlib, SparkFun Unicore |
| 517 | eagleye | navigation-ins | 车载定位 | GNSS/INS | singleton 车载定位; GNSS/IMU |
| 527 | GNSS_INS_Integrations_Comparisons | navigation-ins | GNSS/INS对比 | GNSS/INS | singleton GNSS/INS对比 |
| 525 | gnss_comm | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 534 | GVINS-HKUST | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 537 | IC-GVINS | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 550 | msckfvioGPS | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 714 | OpenVINS | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 752 | OKVIS2-X | navigation-ins | GNSS/视觉/INS | GNSS/INS/视觉 | GNSS/视觉/INS is a name variant of GNSS/INS/视觉 |
| 555 | pyins | navigation-ins | INS建模 | INS工具包 | singleton INS建模 |
| 528 | gnss_ros_standardization | navigation-ins | ROS2原始观测 | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 558 | rtklib_ros_bridge | navigation-ins | ROS/RTKLIB | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 566 | ublox_driver | navigation-ins | GNSS/视觉/INS | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 869 | swiftnav-ros2 | navigation-ins | ROS2驱动 | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 881 | fixposition_driver | navigation-ins | 视觉RTK | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 893 | nmea_navsat_driver | navigation-ins | ROS-NMEA | ROS驱动 | ROS driver/interface; singleton subcat or fits ROS驱动 |
| 515 | BDS-3-PPP-B2b_IMU_LiDAR | navigation-ins | B2b组合导航 | 多传感器融合 | singleton B2b组合导航; IMU/LiDAR fusion |
| 518 | FE-GUT | navigation-ins | FGO/GNSS-UWB | 多传感器融合 | singleton FGO/GNSS-UWB; GNSS/UWB fusion |
| 862 | IERS-EOP-PC | orbit-clock | EOP产品 | EOP与参考系 | singleton EOP产品; sibling IERS-Datacenter |
| 572 | Gkit-Bias | orbit-clock | DCB/UPD/IFCB/OSB | OSB/偏差估计 | singleton; sibling MCOSB |
| 912 | satellite-js | orbit-clock | SGP4-JS | SGP4传播 | SGP4 singletons merged |
| 913 | dSGP4 | orbit-clock | 可微SGP4 | SGP4传播 | SGP4 singletons merged |
| 914 | sgp4-rs | orbit-clock | SGP4-Rust | SGP4传播 | SGP4 singletons merged |
| 916 | BIPM-WebTAI-FTP | orbit-clock | 时标FTP | 时标产品 | singleton 时标FTP; sibling BIPM-Time-FTP |
| 961 | nyx | orbit-clock | 轨道动力学 | 轨道确定/基础库 | singleton 轨道动力学; siblings Orekit, GMAT |
| 571 | clkcomb | orbit-clock | 钟差/相位偏差合成 | 轨道钟差综合 | singleton; combination software like SPOCC |
| 858 | ESSP-EGNOS-User-Support | tools-learning | SBAS用户支持 | SBAS | singleton SBAS用户支持; sibling EGNOS-GSC-User-Support |
| 918 | NGDC-Geomagnetism | tools-learning | 地磁门户 | 地磁模型 | singleton 地磁门户; sibling NOAA-WMM-Portal |
| 592 | HTDP | tools-learning | 坐标框架/地壳运动 | 坐标转换 | singleton 坐标框架/地壳运动; epoch/frame transformation, used with NGS-NCAT |
| 608 | VDATUM | tools-learning | 垂直基准 | 坐标转换 | singleton 垂直基准; vertical datum transformation, used with NCAT/HTDP |
| 587 | gAGE-Software-Tools | tools-learning | 高校工具门户 | 机构软件门户 | singleton 高校工具门户; sibling institutional software portals |
| 613 | GMR-Water | troposphere | GNSS-IR水位 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 615 | GNSS_RR | troposphere | GNSS-IR/RR | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 616 | gnssIR-matlab-v3 | troposphere | 反射测量 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 617 | gnssIR-python | troposphere | 反射测量 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 619 | gnssr-synth | troposphere | 反射测量 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 622 | gnssrefl | troposphere | 反射测量/PWV相关 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 623 | gnssrlowcost | troposphere | 反射测量 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 627 | mphw | troposphere | GNSS-IR硬件 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 628 | mpsim | troposphere | GNSS-IR/多路径仿真 | GNSS-IR | ground-based GNSS-IR singletons/variants merged |
| 636 | UNB3m | troposphere | 经验模型 | 大气模型 | singleton 经验模型; sibling GTrop |
| 786 | ITU-Rpy | troposphere | 大气延迟/InSAR | 大气模型 | ITU-R attenuation model, not InSAR; sibling lowtran |
| 952 | EUREF-EPN-Troposphere | troposphere | EPN对流层 | 对流层产品 | singleton EPN对流层 |
| 624 | GNSSRMERRByS | troposphere | 反射测量 | 星载GNSS-R | MERRByS spaceborne; siblings GNSSR_MERRByS_Python |

### Main themes

- **Space-weather, solar and geomagnetic portals (26 entries) moved from ionosphere to gnss-datasets/地磁空间天气.** These are Kyoto AE/Dst/Kp, GFZ-Kp-Data, ISGI, BGS-INTERMAGNET, the SWPC GOES/solar-wind/solar-cycle/WSA-Enlil/event-report pages, SIDC, SILSO, SDO, SOHO, LISIRD, Helioviewer, Space Weather Canada, CCMC DONKI/ISWA, and SWS Geophysical/Solar. They are official_site data portals with no ionosphere-software content. Before this batch, each sat in its own one-entry subcategory, while identical siblings were already in gnss-datasets: NOAA-SWPC, NOAA-SWPC-Planetary-K, GFZ-Kp-Index (the same GFZ Kp service as GFZ-Kp-Data), BoM-SWS, NASA-OMNIWeb, NRCAN F10.7. SWPC-Services (tools-learning) moved with them. Inside gnss-datasets, the six magnetometer-network portals (Kyoto WDC, INTERMAGNET, SuperMAG, AMBER, IMAGE, CARISMA) moved from 空间天气辅助 to 地磁空间天气, where USGS/BGS/MACCS/THEMIS/TGO already were.
- **Thermosphere models, which batches 42 and 43 flagged as borderline.** msise00 (NRLMSISE-00) and hwm14 were in troposphere/大气模型. The same models' other wrappers (pymsis, Python-NRLMSISE-00, hwm93) were in ionosphere. The troposphere blurb covers neutral-atmosphere *delay* and GNSS meteorology, not thermospheric density or wind. All five now sit together in the existing ionosphere/中性大气 subcategory, following the batch 42/43 precedent that the ionosphere category is the home for upper-atmosphere models. NCAR-GLOW moved to ionosphere/模型 next to AURORA and transcar. docs/categories.md still has no explicit thermosphere home (see leftovers).
- **Software filed in the wrong domain:** SbfMixer and Septentrio-PyDataLink are Septentrio receiver tools with no ionosphere function, so they moved from ionosphere/工具 to gnss-data/接收机驱动. piksi_tools moved there too. pysatCDF and swds-api-downloader are space-physics tools, so they moved to ionosphere. gLAB (mirror) moved to gnss-positioning next to gLAB-UPC and gLAB-Download. EasyGNSS is an RTKLIB touch GUI, so it moved to gnss-positioning/RTK客户端. nmea-msgs moved to navigation-ins/ROS驱动 and NTRIP_ROS to gnss-data/ROS NTRIP客户端. GVINS-Dataset moved to tools-learning/数据集. UNAVCO-Preprocessing moved to tools-learning/机构软件门户. NOAA-EMM moved to tools-learning/地磁模型. VMF-Data-Server-TropProducts moved to troposphere/VMF产品.
- **Name-variant subcategories merged:** 区域CORS→CORS区域网, GNSS/视觉/INS→GNSS/INS/视觉, IGS数据中心/数据中心→IGS综合, GNSS掩星/RO→掩星, IRI官方模型→IRI模型, NeQuick-G官方→NeQuick官方, 反射测量/GNSS-IR variants→GNSS-IR, the Soapy plugin singletons→SDR抽象, SGP4-*→SGP4传播.
- **Misfiled within the ionosphere category:** five deep-learning TEC *forecast* repos moved from TEC估计 to TEC预报/ML.

### Borderline (reported, not moved)

- About 30 ionosphere-specific official portals remain in the ionosphere category, while similar pages sit in gnss-datasets/电离层产品. In ionosphere: DLR-IMPC, NOAA GloTEC, ROB TEC/IONEX, ESA TIO/IONMON/SWE, NICT WDC/ionosonde, GFZ/UWM GIM pages, Beihang, SWS-HF/Satellite, GIRO-portal, CCMC-Home. In gnss-datasets/电离层产品: CDDIS-IONEX, IONORING, eSWua-TEC, JPL-IONEX-Rapid. This is a long-standing split and needs a policy call. The clearest candidates are ROB-IONEX-Products and NOAA-SWPC-GloTEC-Data, which are pure download directories.
- ionosphere has two generic subcategories, 工具 (45) and 电离层工具 (19), that overlap. Ionosonde tools are split between them.
- gnss-datasets/空间天气辅助 still mixes ionospheric radar/ISR data (SuperDARN, OpenMadrigal; CEDAR Madrigal sits in 电离层产品) with NSTB-WAAS-Test-Team, which is SBAS test data rather than space weather.
- gps-measurement-tools (gnss-data) vs google-gnss-logger (mobile-apps/原始测量); CSNO-TARC(-Differential) under 偏差产品; swift-nav-pygnss (tools-learning/Python工具); gnssFGO (因子图融合) vs 因子图紧组合; RTK/PPP vs PPP/RTK vs SPP/RTK/PPP synonyms in gnss-positioning; CORS区域网 vs 国家CORS overlap.
- 46 singleton subcategories remain, mostly in tools-learning and gnss-positioning. No sibling fits them clearly.

## Task 2 — text artifacts

- Regex scan of desc_zh/analysis_zh/one_liner_zh across all 1029 entries: `。。`, `[，、；：]。`, `。[，；、：]`, empty `（）`/`()`, leading `；，。、：`, doubled `，，`/`、、`/`；；`, trailing separators, space before CJK punctuation, `（，`/`，）`, double spaces, analysis not ending in `。`/`）`. **0 hits.**
- Scan for ASCII `,;.` between CJK characters and for English words or runs. The hits were proper names, quoted titles and technical tokens, which are legitimate. The exceptions are the curator/English filler left over after batch 50. **15 entries fixed:**
  - `官方 portal；` removed: EGNOS-GSC-User-Support, NSTB-WAAS-Test-Team, GSC-Programme-Reference-Documents, Earthdata-MGEX, Navipedia, USCG-NAVCEN, GPS.gov, ENRI-Japan, ICAO-PBN.
  - `portal-terms；` removed: FAA-WAAS, GLONASS-IAC. `属门户服务（portal-terms）；` removed: NOAA-UFCORS.
  - Provenance curator notes removed: `按 catalog 政策记为个人社区（…）；` in AgOpenNtripCaster and baidu-ntripcaster, and `（按目录政策属公司开源档）` in gps-measurement-tools.
- Random spot-check of 30 entries (seed 51: idx 15, 26, 58, 60, 66, 233, 331, 344, 363, 395, 473, 498, 503, 523, 528, 568, 613, 701, 711, 737, 752, 792, 813, 827, 897, 919, 949, 962, 978, 1028): grammar clean. The only artifacts found were FAA-WAAS and USCG-NAVCEN, which led to the catalog-wide portal fix above.

## Regeneration and checks

- `merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme` dry-run on untouched data gave a zero diff. The same functions were run after the edits.
- PROJECTS.json is valid JSON with the canonical dump format. The diff touches only `category` (42), `subcategory` (204), `analysis_zh` (15 entries) and `counts_by_category`.
- All 10 list files have header count equal to row count, and every URL appears exactly once across the lists (1029 rows). README badges/table and docs/categories.md counts match `counts_by_category`. project_count is 1029. Provenance is 331/214/484, unchanged.
