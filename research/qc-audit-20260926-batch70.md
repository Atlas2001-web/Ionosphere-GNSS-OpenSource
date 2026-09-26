# 目录 QC 审计 — 2026-09-26 第 70 批

基线：`7196386`（第 69 批），1027 个项目，provenance 330/212/485，RETIRED_URLS 56。
开工时 HEAD = origin/main = 7196386，工作区干净；本批进行中 peer 陆续推送 7486a6e（scintillation-networks + data-access E34）、aa378fc（pysatspaceweather / ocbpy / crx2rnx 复跑）、7fdf64c（ro-missions-data + E35）、e1b7a6f（unicore-driver）、f05f01c（hwm14 + ionfr），均已在 origin，本地无未推送 peer 提交。
本批不增删项目；7 个 http-only 条目 URL 未动；已有手册未改；docs/software、docs/data-access.md 中旧主机名行未动。

## Task 0：他人自 7196386 以来的改动

`git diff 7196386 HEAD -- PROJECTS.json`：无（peer 提交只动 docs）。无新增 / 改动条目需 QC。

对照 peer 新手册 / 复跑：
| 手册 | 目录条目 | 结论 |
|---|---|---|
| scintillation-networks.md | **ISMR-Query-Tool** | 条目写「若打不开请用 HTTP 或项目组当前公布地址」；手册与本机复测：http 只 301 到 https，https 证书链不全（curl exit 60），首页 SPA + Cloudflare Turnstile，要 UNESP 账号 → analysis_zh、registration_zh 改写（registration 保持 `form_register`） |
| scintillation-networks.md | eSWua-TEC、IONORING、ismr_downloader、CEDAR Madrigal | 无矛盾，未改 |
| ro-missions-data.md | COSMIC-GNSS-RO-Data、COSMIC-CDAAC、ROM SAF、awsgnssroutils | 无矛盾（ROM SAF「无电离层产品、下载要登录」与手册一致），未改 |
| unicore-driver.md | **UnicoreDriver** | 条目写「依赖 Eigen 与 Boost」；手册坑 11：CMake `find_package(Eigen3 REQUIRED)` 但源码未用 Eigen → 改为「依赖 Boost（CMake 要求 Eigen3，但源码未用到）」，其余字段保留 |
| hwm14.md | hwm14、hwm93 | Apache-2.0 / ★7、hwm93 2022 归档一致，未改 |
| ionfr.md | ionFR | GPL-3.0、★12、IGRF + IONEX 一致，未改 |
| pysatspaceweather / ocbpy / crx2rnx 复跑 | 同名条目 | 条目为概述文字，无矛盾，未改 |

## Task 1：新手册 docs/software/jpl-gps-timeseries.md

- 选题：**JPL-GPS-Time-Series**（sideshow.jpl.nasa.gov/post，门户类，匿名 HTTPS 静态文件）；ls、README 索引、peer 未跟踪文件均无相关手册。避开 SDR/反射/RTKLIB/GREAT/Gkit/bias/时间传递/二进制转换/账号服务。
- 本机实跑 2026-09-26 06:27–06:37 EDT，单站 ALGO（`.series` + `.resid`）、四张表、方法 PDF、几个 Range 尾部请求，合计约 25 MB。
- 实测数字：2860 站（table1 与 point/ 列表一致）；ALGO 12085 行 1992-08-29 → 2026-09-19，缺 362 天，同日两行 7 天；1822 个 `.series` mtime 2026-09-25 16:03 PT（Last-Modified 23:03 GMT）→ 约 6–7 天延迟；table2 速度 E −16.460 / N 2.536 / U 3.229 mm/yr，2013 起直线 E −16.54 / N 2.52 / U 3.20；table1 XYZ 速度旋 ENU 与 table2 一致；ALGO 阶跃 2 个；AB12 数据停在 2019-04-30、WUHN 到 2026-08-17、WUH2 404。
- 上游问题（写进坑表）：仍是 IGS14（参考历元 2026-01-01）；表内位置单位 mm；残差后缀 `.resid`；PDF wget 命令缺尾斜杠（301 后 `-np` 父目录变 `post/`）；table2 纬经度只 6 位小数（与 XYZ 差 2.1 cm）；PDF 称 σ>5 mm 剔除但 ALGO 有 54 个历元 σ>5 mm；首页「31 satellites / over 2000 receivers」过时；旧 README 写 repro2011b 与拼错的 ftp 路径；http 20 s / ftp 15 s 超时；站名大小写敏感。
- 目录条目 **JPL-GPS-Time-Series** 按实测改写 analysis_zh，新增 `registration=open` + registration_zh。
- docs/software/README.md：索引加第 257 行 + 速查表一行；首行计数 256 → 257 篇、58590 → 58778 行。

## 重新生成

用 origin/main 的 `research/merge_routine_20260926c.py` 中 `regenerate_lists / regenerate_categories / regenerate_readme`（驱动脚本先断言 project_count、counts_by_category、provenance_counts 与条目一致）。改前 dry-run（HEAD 版 PROJECTS.json 于临时目录）：零 diff。改后只动 `lists/06-navigation-ins.md`（UnicoreDriver）与 `lists/10-gnss-datasets.md`（ISMR-Query-Tool、JPL-GPS-Time-Series）。

## 合计

- 改动条目 3：ISMR-Query-Tool（analysis_zh + registration_zh）、UnicoreDriver（analysis_zh）、JPL-GPS-Time-Series（analysis_zh + registration）。
- 新手册 1：docs/software/jpl-gps-timeseries.md（188 行）。
- 1027 个项目；provenance 330/212/485；counts_by_category 不变（gnss-datasets 220、navigation-ins 72 …）；RETIRED_URLS 56。
