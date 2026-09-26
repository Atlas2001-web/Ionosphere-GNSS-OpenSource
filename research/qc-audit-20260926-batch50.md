# QC audit — 2026-09-26 batch 50 (process filler catalog-wide; caveat-first desc idx 843–961; provenance by written policy)

Base: origin/main `155904b` (batch 49). Catalog **1029 → 1029**. No projects were added or removed.
Provenance official/academic_lab/personal_community **332/238/459 → 331/214/484** (26 changes, see Task 3).
Evidence read 2026-09-26 ~04:10–05:00 ET: `gh api orgs/{ros-drivers,esa,space-physics,geospace-code,pysat}` and `gh api repos/X/Y/readme` for dSGP4, 8 pysat repos, 2 geospace-code repos and 14 space-physics repos.

## Task 0: entries newer than 155904b
None. At the start HEAD = origin/main = 155904b and `project_count` was 1029.

## Task 1: process filler removed (268 entries, catalog-wide)
What was removed (the sentence or clause only; every other fact was kept):
- `收录前已(用) HTTP (200) 核验…` in all its variants (~150 entries, mostly portals idx 3–160, 836–1009) and the stock tail that went with it, `使用请遵守上游许可/条款与引用要求`.
- Boilerplate: `具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验`, `使用前请核验上游页面与许可条款`,
  `仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线`, `请对照上游页面核实最新访问方式与许可`, `详见上游页面`, `页面/软件页/公开仓 HTTP 200`.
- Generic `X以仓库/上游/文档/站点/页面/说明为准` clauses where X names no specific source (e.g. `许可条款以仓库为准`, `注册与商用条款以上游为准`).
  Where the clause names a *specific* authority, it was kept (e.g. crz2rnx `长期以国土地理院官方 RNXCMP 为准`, gLAB `以 UPC gAGE 页面为准`, BNC `以 BNC 主页文档为准`).
- Generic `(使用|下载|引用)请遵守/遵循 X 条款/政策/规定` compliance tails. Operational advice (高频/批量/脚本抓取…), real access requirements (Earthdata 账号, 注册, 非商业) and citation instructions (引用请注明…) were kept.
- Curator wording: `与已收录(的) X` → `与 X`; `本条/本目录/已单独收录/目录中已有/作为…收录` were rewritten as plain statements (e.g. GIRO-GAMBIT, GIRO-IRTAM, UMLCAR-Downloads, SAMI3-Zenodo, sidereon-python, swift-nav-pygnss, SoftGNSS-octave, hwm93, ITU-Rpy, NOAA-NCN, clkcomb, IonKit-NH/OASIS fork notes).
- Real facts that sat inside filler parentheses were kept as their own sentences: SWPC-Real-Time-Solar-Wind / Solar-Synoptic-Map (页面现多跳转到 spaceweather.gov),
  GA-GNSS-Networks (旧路径 301 到本 URL), ILRS (美国政府停摆期间可能暂停更新), CCMC-ISWA (iswa.ccmc 旧地址跳转到本 URL).
- Duplicate sentences dropped: GPS-Galileo sim (idx 260, time-system sentence repeated) and the cubesat sim (idx 268, orbit-simplification sentence repeated).
- rtcm2ionex desc would have become too thin after removal, so it was rewritten from the entry's own analysis: `把实时 RTCM VTEC 消息落盘为 IONEX 格网`.

Examples (before → after):
1. BoM-SWS analysis tail: `…而不是裸爬页面。收录前已用 HTTP 核验页面可访问；使用请遵守上游条款与引用要求。具体路径与权限以站点当前说明为准，脚本下载建议做断点续传与校验。` → `…而不是裸爬页面。`
2. CAS-BDsmart-Pub: `具体子目录以站点为准；论文引用请标明 CAS 产品标识、日期与文件长名。收录前已用 HTTP 核验…` → `论文引用请标明 CAS 产品标识、日期与文件长名。`
3. GIRO-IRTAM: `已收录 IRTAM 系数读取器压缩包与 PyIRTAM，本条补齐官方产品可视化/服务入口。` → `系数读取可用 IRTAM 读取器压缩包或 PyIRTAM；本页是官方产品可视化/服务入口。`
4. GA-GNSS-Networks: `…而非文件 API。收录前已 HTTP 核验（旧路径会 301 到本 URL）。` → `…而非文件 API。旧路径会 301 跳转到本 URL。`
5. ntrip_client-MicroStrain: `依赖 ROS 工作区；非通用桌面 NTRIP 客户端，许可条款以仓库为准。` → `依赖 ROS 工作区；非通用桌面 NTRIP 客户端。`

Deliberately left: `现状（2026-09-26 复核）` (a dated status line), technical "verify against spec/samples" advice (DO-229, 标准算例, 示波器, 样例核验),
and the owned-repo template (SH-GIM).

## Task 2: caveat-first desc_zh rewritten (41 entries, idx 843–961)
Each desc_zh now says first what the tool is and what it provides, and keeps at most one short caveat. The longer caveats were already in analysis_zh, so none were lost.
Rewritten: 843 LANS-AFS-SIM, 844 PocketSDR-AFS, 845 namuru-gps, 846 rt-navi, 847 nav-solutions-gnss, 848 piksi_tools, 849 swift-nav-pygnss, 852 libswiftnav,
854 ionFR, 855 gps-fpga, 856 gnsshat, 857 ublox8-qzss-almanac-converter, 864 novatel_oem7_driver, 865 novatel_gps_driver, 866 max2771_fx2lp, 867 GNSS-Correction-RTKLIB,
868 pysatNASA, 869 swiftnav-ros2, 878 NeoGPS, 879 UbxGps, 880 bolderflight-ublox, 881 fixposition_driver, 882 SoftGNSS-octave, 892 ublox-ros, 895 107-Arduino-NMEA-Parser,
896 gpsdo, 897 ublox-rs, 906 pymap3d, 907 TEC-Maps-of-Nepal, 908 NCAR-GLOW, 909 pysatMissions, 910 pysatCDF, 911 python-sgp4, 912 satellite-js, 913 dSGP4, 914 sgp4-rs,
921 Python-NRLMSISE-00, 922 SoapySDR, 923 SoapyHackRF, 924 SoapyPlutoSDR, 961 nyx.
Examples:
- rt-navi: `工程 PoC 非测地 PPP-AR；单串口单接收机` → `以 U-Blox 为测量源、接同组织 PVT 解算器的 Rust 实时导航 PoC；单接收机，非测地级 PPP-AR`
- pysatNASA: `多源空间天气对齐好用；依赖 pysat 与上游政策，不是 GNSS 解算库` → `pysat 的 NASA 空间科学仪器数据扩展，便于多源空间天气数据对齐；不是 GNSS 解算库`
- gpsdo: `实验室时频参考输出；定时应用，非定位解算` → `基于 Arduino 的 GPS 驯服振荡器，输出 10 MHz 等实验室参考频率；属定时应用`

## Task 3: provenance by written policy (docs/categories.md)
| idx | project | before → after | evidence |
|---|---|---|---|
| 47, 893 | nmea-msgs, nmea_navsat_driver | official → personal_community | org `ros-drivers` = "ROS device drivers", ROS SIG mailing list; no government or official body |
| 913 | dSGP4 | academic_lab → official | repo is in the `esa` org (European Space Agency); README lists authors on ESA ACT team pages (Acciarini, Izzo); it names Oxford AI4Science only as where the project *originated* |
| 24, 906 | georinex, pymap3d | academic_lab → personal_community | org `geospace-code` ("GNSS and other geospace analysis programs"); no university or lab named in the org or READMEs |
| 65, 446–448, 868, 909, 910 | pysat, pysatCDAAC, pysatModels, pysatSpaceWeather, pysatNASA, pysatMissions, pysatCDF | academic_lab → personal_community | org `pysat` (gmail and Slack contact); READMEs say "the pysat team" and name no lab or institute |
| 365, 387, 388, 390, 433, 496, 657, 750, 776, 801, 802, 823, 908, 1018 | space-physics repos (ionosphereAI, iri2016, iri2020, iri90, POLAN, transcar, msise00, lowtran, hwm93, igrf, wmm2020, geomagindices, NCAR-GLOW, isr-raw) | academic_lab → personal_community | org `space-physics` ("Space Physics modeling and analysis"); no README names a releasing lab. transcar names individual Fortran authors, and msise00/hwm93 name the original NASA model sources, so these are community wrappers |

Wording aligned: nmea-msgs desc `ROS 官方驱动组维护` → `ROS 社区驱动组（ros-drivers）维护`; dSGP4 analysis now says it was released by ESA ACT members in the ESA GitHub org.

## Validation
- PROJECTS.json parses; 1029 projects; `provenance_counts` = 331/214/484, which matches the data. `counts_by_category` is unchanged.
- Lists, categories.md and README were regenerated with `merge_routine_20260926c.py`'s regenerate_lists / regenerate_categories / regenerate_readme. A dry run on the unmodified data gave zero diff first.
- The diff touches only desc_zh / one_liner_zh / analysis_zh / provenance / provenance_counts in PROJECTS.json, the matching list lines and badges, and the README provenance line.
