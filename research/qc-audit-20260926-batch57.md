# QC audit — 2026-09-26 batch 57: label/wording consistency

Base: `ef99854` (batch 56) → origin/main `a4923a2` (peer docs commit for prx; no catalog changes). 1028 projects, provenance 330/214/484. No projects added or removed, and no provenance or category labels changed.

## Task 0: entries newer than ef99854

None. The only commit after it is `a4923a2` (docs/software/prx.md + docs/software/README.md), which does not touch PROJECTS.json.

## Task 1: '官方' / '个人' / '实验室' self-label consistency

Scanned desc_zh, one_liner_zh and analysis_zh across all 1028 entries.

| Scan | Hits | Self-label (changed) | Kept (refers to something else) |
|---|---:|---:|---:|
| '官方' in personal_community + academic_lab | 82 hits / 62 entries | 17 entries, 18 fields (19 hits) | 63 hits (e.g. `非官方 Git 镜像`, `官方 RNXCMP`, `官方 ICD 测试向量`, `CDAAC 官方文档`, `基于官方协议`) |
| '个人'/'社区' about itself in official | 11 hits / 10 entries | 0 | 11 (CCMC = Community Coordinated Modeling Center; `社区镜像`/`社区包装` = third-party copies; `个人用户`/`个人申请` = licence audience) |
| '个人仓' about itself in academic_lab | 1 | 1 (text fixed, label kept) | 0 |
| '实验室发布/课题组发布' about itself in personal_community | 0 claims (39 hits for '实验室/课题组' all mean target users, e.g. `适合实验室信号源`, or describe origin, e.g. GRID, GNSS-REFLECTOMETRY-PROCESSING, saga-utils) | 0 | all |

Total: **20 replacements in 19 fields across 18 entries** (19 PROJECTS.json lines; 12 rendered list lines).

### Vendor releases → 厂商发布 (personal_community)
- novatel_edie one_liner: `NovAtel 官方 OEM7 日志编解码 SDK` → `NovAtel 厂商发布的 OEM7 日志编解码 SDK` (batch-56 regression)
- novatel_oem7_driver desc: `NovAtel 官方 OEM7/SPAN ROS 驱动` → `NovAtel 厂商发布的 …`
- swiftnav-ros2 desc: `Swift Navigation 官方 ROS 2 驱动` → `… 厂商发布的 ROS 2 驱动`
- fixposition_driver desc: `Fixposition 官方 ROS 驱动` → `Fixposition 厂商发布的 ROS 驱动`

### Community → '官方' removed (personal_community)
- AgOpenNtripCaster desc: `AgOpenGPS 官方组织维护` → `AgOpenGPS 社区项目组织维护`
- esp32-xbee desc + analysis: `Ardusimple WiFi NTRIP Master 官方 ESP32 固件` → `… 的配套 ESP32 固件（…，个人开发者维护）`; analysis now names the maintainer, nebkat. The README calls it "the official firmware for the Ardusimple WiFi NTRIP Master", but the repo is a personal account, not a vendor release.

### Lab releases → 课题组发布 (academic_lab)
- gnsstk-apps desc: `GNSSTK 官方配套 CLI 应用集` → `UT Austin ARL SGL 课题组发布的 GNSSTK 配套 CLI 应用集`
- gLAB-Download one_liner: `UPC gLAB 官方源码…` → `UPC gAGE 课题组发布的 gLAB 源码…`
- gLAB-UPC analysis: `官方下载含 Linux 源码包` → `课题组发布的下载包含 Linux 源码包` (kept `GitHub 上多为非官方镜像`)
- GIRO-GAMBIT analysis: `…官方主页` → `…的 GIRO 课题组发布主页`
- GIRO-IRTAM analysis: `本页是官方产品可视化/服务入口` → `本页是 GIRO 课题组发布的产品可视化/服务入口`
- ScintPi-1.0-Software analysis (×2): `ScintPi 1.0 官方采集/可视化软件` → `德州大学达拉斯分校课题组发布的 ScintPi 1.0 采集/可视化软件`; `仪器配套官方软件存档` → `课题组发布的仪器配套软件存档`
- UMLCAR-Downloads analysis: `大气研究中心官方下载索引` → `大气研究中心（UMLCAR）课题组发布的下载索引`
- RADIATE analysis: `官方亦有校内 Git 镜像` → `课题组亦有校内 Git 镜像`
- madrigalWeb analysis: `…的官方 Python 客户端` → `MIT Haystack 课题组发布的 Python 客户端，用于访问…`
- pyDARN one_liner: `SuperDARN 官方社区维护的…` → `SuperDARN 数据分析工作组发布的…`
- SuperDARN RST analysis: `SuperDARN 标准数据产品的官方处理链` → `SuperDARN 课题组生成标准数据产品所用的处理链`

### academic_lab text says 个人仓
- GraphGNSSLib_LEO_V1.2 desc: `（作者个人仓版本）` → `（作者账号首发版，实验室组织版另见 PolyU-TASLAB）`. The label stays academic_lab: the README lists the authors (Yixin Gao, Weisong Wen) as from PolyU's TAS Laboratory, and the technical and commercial contacts are both TAS Lab.

### Kept / flagged (not changed)
- UWM-IGS-Iono-Combination `追踪官方组合策略`: means the IGS combination strategy, not this site.
- UnicoreDriver `基于官方协议`, OSNMA `官方 ICD 测试向量`, iricore `官方 Fortran IRI`: these point to other official things.
- GRID (personal_community, mmurrian): a README-only page describing the UT Austin Radionavigation Lab's commercial GRID receiver. The text describes the product's origin and does not claim the repo is a lab release. Kept.
- tec_forecast desc `深度学习实验室` uses 实验室 to mean "experiment playground", not a provenance claim. Kept.

## Validation
- JSON valid; project_count 1028 = len(projects); counts_by_category unchanged; provenance 330/214/484 unchanged.
- Regenerated with origin/main `research/merge_routine_20260926c.py` `regenerate_lists/regenerate_categories/regenerate_readme`. docs/categories.md and README.md came out byte-identical, so the page-header blurbs are unchanged.
- List header count = table rows for all 10 lists (sum 1028); every URL appears once in PROJECTS.json and once in list tables.
- Diff limited to the 19 intended fields: 19 PROJECTS.json lines + 12 list lines. desc_zh-only edits don't render in the lists.
