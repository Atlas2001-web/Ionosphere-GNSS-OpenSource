# 目录 QC 审计 — 2026-09-26 第 69 批

基线：`0bf6dd9`（第 68 批），1026 个项目，provenance 330/212/484，RETIRED_URLS 56。
开工时本地 HEAD 已被快进到 origin 的 peer 提交（5a9c19d allsky-imager-data、49bcf93 um980-rtklib-pipeline、620d040 cors-networks/ublox8 复跑、624c562 目录新收录 **binex**（+1）、f809df0/94f975d inscar+polan），本地无未推送 peer 提交。
本批不增删项目；7 个 http-only 条目 URL 未动；已有手册未改；docs/software、docs/data-access.md 中旧主机名行未动。

## Task 0：他人自 0bf6dd9 以来的改动

`git diff 0bf6dd9 origin/main -- PROJECTS.json`：只有 624c562 新增的 **binex**。

- **binex**（nav-solutions/binex）：gh 实测 ★5、MPL-2.0、Rust、未归档；crates.io max_version 0.5.2（main 的 Cargo.toml 已是 0.6.0，未发布）；README 的「增强 CRC 未支持 / 小端缺数据集 / MD5 未验证」与 analysis_zh、docs/software/binex.md 一致。唯一改动：subcategory **RINEX读写 → 格式编解码**（BINEX 是二进制交换格式，不是 RINEX；同组已有 rinex2bin），类别 gnss-data 不变，其余字段保留。
- **iricore**：analysis_zh 写「1.9.0 已能通过 OARR 传入 foF2 等用户值」，没有任何字段说 OARR 用户输入未实现 → 未改。

对照 peer 新手册：
| 手册 | 目录条目 | 结论 |
|---|---|---|
| allsky-imager-data.md | THEMIS GMAG、PySPEDAS、gsit | 无矛盾，未改 |
| um980-rtklib-pipeline.md | um980-rtklib-pipeline | GPL-3.0、★1、不用 convbin、rnx2rtkp 与手册一致，未改 |
| inscar.md | inscar | 只算理论谱、不读实测数据、MIT、★7 一致，未改 |
| polan.md | POLAN | Fortran、MIT、★11、虚高→真高一致，未改 |
| cors-networks.md（复跑） | **IBGE-RBMC** | 条目写「多数产品需在 IBGE 相关系统注册后获取」+ `registration=form_register`，与手册/data-access E30「RBMC geoftp 匿名、84 站」矛盾 → analysis_zh 改写，registration → `open`，registration_zh 改写 |
| ublox8-qzss-almanac-converter.md（复跑） | 同名条目 | 一致，未改 |

## Task 1：新手册 docs/software/unr-ngl.md

- 选题：**UNR-NGL**（geodesy.unr.edu，门户类，匿名 HTTPS 静态文件）；ls、README 索引、peer 未跟踪文件均无相关手册。避开了 SDR/反射/RTKLIB/GREAT/Gkit/bias/时间传递/二进制转换/账号服务。
- 本机实跑 2026-09-26 06:21–06:26 EDT，单站 P090，合计下载约 4 MB（站点页、tenv3 最终/快速、2024 trop zip、2026 5 min kenv zip；DataHoldings/MIDAS/steps 走管道过滤）。
- 实测数字：tenv3 6759 天（2007-11-10 → 2026-09-12，缺 123 天）；快速解 51 天到 2026-09-24；MIDAS E −20.29 / N −5.90 / U −0.82 mm/yr（首末差分 E −20.2 / N −5.6）；2024-132 trop 288 历元，ZTD 1971.9–1984.4 mm、PWV 6.11–8.06 mm；2024 年 trop 342 个日文件；5 min 快速 kenv 51 个日文件，最新 doy 267 只有 183 历元；DataHoldings 23793 站，8313 站 Dtend ≥ 2026-09-01；steps.txt 142578 行；ALGO、BJFS 路径同样 200。
- 发现的上游问题（写进手册坑表）：
  1. Plug and Play 页给的 `gps_timeseries/tenv3/IGS14/…`、`tenv3/plates/…`、`txyz/IGS14/…`、`qa/…` 直链全部 404；真实路径在 `gps_timeseries/IGS20/…`（从 `.sta` 站点页抄）。
  2. `http://geodesy.unr.edu` 80 端口挂起（15 s 超时 0 字节），而 README_trop2 / steps_readme / midas.readme 仍写 http。
  3. README_trop2 的 zgrep 一行命令给 290 行而非所称 288 行（带出结束标记）。
  4. trop 文件 `TROP/DESCRIPTION` 字段名（TRODRY TROWET）与数据表头（TROTOT … TRWET）不一致；站坐标标签 `IGS14_` 而 INPUT 写 IGS20；README 自己警告梯度两列互换。
  5. README 称 trop 每周更新，但 2026 年 zip 未生成（最新 2025.trop.zip 生成于 2026-01-10）。
  6. 站名大小写敏感（小写 404）；DataHoldings 经度 0–360。
- 目录条目 **UNR-NGL** 按实测改写 analysis_zh（产品清单、IGS14 直链 404、IGS20 路径、http 不响应、约 2 周延迟、手册指针），新增 `registration=open` + registration_zh。
- docs/software/README.md：索引加第 251 行 + 速查表一行；首行计数 250 → 251 篇、57278 → 57450 行。

## 重新生成

用 origin/main 的 `research/merge_routine_20260926c.py` 中 `regenerate_lists / regenerate_categories / regenerate_readme`（驱动脚本先断言 project_count、counts_by_category、provenance_counts 与条目一致）。改前 dry-run：零 diff。改后只动 `lists/03-gnss-data.md`（binex 移组）与 `lists/10-gnss-datasets.md`（IBGE-RBMC、UNR-NGL 文本）。

## 合计

- 改动条目 3：binex（subcategory）、IBGE-RBMC（analysis_zh + registration）、UNR-NGL（analysis_zh + registration）。
- 新手册 1：docs/software/unr-ngl.md（172 行）。
- 1027 个项目；provenance 330/212/485；counts_by_category 不变（gnss-data 138、gnss-datasets 220 …）；RETIRED_URLS 56。
