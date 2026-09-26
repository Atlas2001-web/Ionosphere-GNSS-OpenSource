# 目录 QC 审计 — 2026-09-26 第 68 批

基线：`c9ba1c4`（第 67 批），1026 个项目，provenance 330/212/484，RETIRED_URLS 56。
开工时本地 HEAD 被快进到 `ca79b96`（7 个 peer 提交，均已在 origin，只改 docs/software 与 docs/data-access.md；PROJECTS.json 未动）。
本批不增删项目；7 个 http-only 条目的 URL 未动；已有手册未改；docs/software、docs/data-access.md 中旧主机名行未动。

## Task 0：他人自 c9ba1c4 以来的改动
`git diff c9ba1c4 origin/main -- PROJECTS.json` 为空，无条目需要 QC。
顺带对照 peer 新手册（um982-driver、ocbpy、pysatspaceweather）：
- **um982-driver**：目录写「解析标准 NMEA 以及 PVTSLN、KSXT、GNHPR、BESTNAV」，手册实测只解 `#PVTSLNA` / `#BESTNAVA` / `$GNHPR`，不解 KSXT 和标准 NMEA → 重写 analysis_zh。
- ocbpy、pysatSpaceWeather：与手册无矛盾，未改。

## Task 1：第 67 批遗留（已对照手册核实）
| 条目 | 改动 | 手册依据 |
|---|---|---|
| SbfParser | 类别 ionosphere/闪烁/ROTI → **gnss-data/基础库**（与 pysbf、pysbf2 同组；主干无 ISMR/S4 块，放闪烁类不合适） | sbfparser.md |
| caster | 追加：Node 20 启动即崩（`parser.remove is not a function`），需 Node 16 | caster.md 坑 1 |
| laika | 追加：下载星历/改正需 Earthdata `.netrc`，离线读 RINEX/DOP 不需要；新增 `registration=form_register` + registration_zh | laika.md §2、坑 4 |
| pyglow | 追加：需 Python 3.8 + numpy 1.20.3（+gfortran），3.10+ 装不上 | pyglow.md 坑 1 |
| ntrip-cpp | 追加：caster 默认不编译，主干开 `NTRIP_BUILD_CASTER` 需修两处构建错误 | ntrip-cpp.md §2.2 |
| cddis-highrate-downloader | 改写「README 称匿名 FTP 无需账号」：匿名 FTPS 能登录/SIZE，但 LIST/RETR 报 425，不可靠；CDDIS HTTPS 需 Earthdata；半年前数据已成 tar。新增 `registration=mixed` + registration_zh | cddis-highrate-downloader.md 坑 2/3/10、§3.5 |

sbfparser.md 未提旧类别，无需改手册。

## Task 2：新手册 docs/software/quakeion.md
- 选题：quakeion（Gm015555，MIT，PyPI 0.1.1），匿名拉取 USGS 地震目录 / CODE GIM / GFZ Kp / 京都 Dst 的客户端，目录中无手册、README 索引无、无 peer 未跟踪文件。
- 本机实跑 2026-09-26 06:08–06:17 EDT：上游测试 29 passed；Aomori M7.6（2025-12-08）±1 天 3 个 CODE FIN GIM、TEC/ROT/ROTI、Kp 17 行、Dst 73 行、`report()` 4 张 PNG；2016 旧名 `.Z`、2026-09-24 RAP 均命中。
- 发现的上游问题：
  1. 写死的 `http://ftp.aiub.unibe.ch/CODE` TCP 能连但不回 HTTP（本机和 WebFetch 均超时），不打补丁 GIM 一张也下不到；改 `https://download.aiub.unibe.ch/CODE` 可用。
  2. `import quakeion.tec` 得到的是函数（`__init__` 覆盖），改 `CODE_BASE` 要用 `sys.modules["quakeion.tec"]`。
  3. `kp(start, end)` 只取到 end 当天 00:00，最后一天的暴日可能漏标。
  4. 缓存按日期不分 FIN/RAP，快速产品不会被替换。
- 目录条目 quakeion 按实测改写 analysis_zh（CODE 地址失效 + 补丁、“测站”只是坐标）。
- docs/software/README.md：新增索引第 246 行 + 选型行；总数 246 篇 / 56397 行。

## 字段统计
9 个条目，13 个字段：analysis_zh 7（caster、laika、pyglow、ntrip-cpp、cddis-highrate-downloader、um982-driver、quakeion；SbfParser 未改文字）、category 1、subcategory 1、registration 2、registration_zh 2，外加顶层 counts_by_category（ionosphere 247→246，gnss-data 136→137）。无 URL 变更。

## 再生成
用 origin/main `research/merge_routine_20260926c.py` 的 regenerate_lists / regenerate_categories / regenerate_readme；
改前 dry-run 零差异；改后动 lists/01、03、04、docs/categories.md、README.md（分类计数）。
总计 1026，provenance 330/212/484，RETIRED_URLS 56。
