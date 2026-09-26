# 目录 QC 审计 — 2026-09-26 第 67 批

基线：`ca209df`（第 66 批；提交前快进到 `b2c8d5d`，其间两个 peer 提交只改 docs，PROJECTS.json 未动；iricore/ntcmg 新 QC 内容与目录不矛盾），1026 个项目，provenance 330/212/484，RETIRED_URLS 56。
本批不增删项目，只改文字/许可证字段；7 个 http-only 条目的 URL 未动；手册（docs/software）未改。

## Task 0：他人自 ca209df 以来的改动
`git diff ca209df origin/main -- PROJECTS.json` 为空，无需 QC。

## Task 1：第 66 批遗留的 analysis_zh 注意事项（先对照手册核实）
| 条目 | 追加内容 | 手册依据 |
|---|---|---|
| GNSSommelier | 不在 PyPI；BKG IONEX 路径 404；JPL IONEX 目录配错，基本只能走 CDDIS | docs/software/gnssommelier.md 实测 |
| ppp-tools | CODE rapid 自动下载坏了（拼出的 URL 不对），需手动下载 | ppp-tools 手册 §5 E1 |
| gps_pvt | Ruby 3.3.8 上加 `--weight` 会崩（exit 139） | gps_pvt 手册坑 5 |
| iri2020 | 自带 apf107/ig_rz 指数只到 2023，之后日期结果会悄悄出错 | iri2020 手册 |

未采纳：GNSSommelier「AAA= 过滤无效」——手册 QC 复跑写明 `--where AAA=` 可用，初稿结论没复现，故不写入目录。

## Task 2：2026-09-26 之前最后修改的手册 vs 目录
范围：121 份手册（120 份 09-24，1 份 09-23），通过手册抬头「PROJECTS.json → 名称」及 URL 映射到 135 个条目（119 份有对应条目）。只改明显矛盾，共 9 个条目：

1. **DiffIonMap**：只有 A/B 并排对比图，没有差值图；Python 2 代码（desc/analysis/one_liner）。
2. **gnss-protos**：只解 GPS/QZSS LNAV 子帧 1–3；crates.io 0.0.2，主干 0.1.0-beta；删去「rinex/rtk/ntrip 多协议底座」说法（analysis/one_liner）。
3. **GREAT_PODFLT**：license 由空改为 GPL-3.0（依据 doc/GREAT_PODFLT.pdf §2.2；仓库无 LICENSE 文件）。
4. **pysatCDAAC**：补充 ionphs 下载可用但 `Instrument.load` 失败，需 netCDF4 绕过。
5. **rt-clk-service**：重写为「最小 RTCM3 SSR NTRIP 解码演示，只打印到终端；硬编码 caster 连不上；不产出产品；无许可证」（原写成产品生成服务）。
6. **SbfParser**：主干没有 ISMR 4086/S4 块（手册称原文案超前）；PyPI 包名 sbf-parser。
7. **rtcm3torinex**：门户已标为过时（并入 BNC）；只接 NTRIP，不能离线读文件。
8. **RTPPP_B2b**：是 BNC 源码切片，无构建脚本，需 BNC 头文件 + Qt；把误写的「短报文 PPP」改为 PPP-B2b 实时定位。
9. **rinex**：纯库，CLI 在单独的 rinex-cli 仓库（desc/analysis/one_liner）。

### 无专属目录条目的手册（仅报告）
- binex.md：抬头引用了不存在的 `binex` 条目。
- rinex-cli.md：仅在 rinex 条目中提及。
- rnx2cggtts.md：只能映射到 cggtts / rinex 条目。

### 遗留（细节缺失但非矛盾，本批未改）
- SbfParser 建议改类到 gnss-data/基础库（现为电离层/闪烁/ROTI）。
- caster：Node 20 上崩，需 Node 16。
- laika：下载需要 Earthdata `.netrc`。
- pyglow：需 Python 3.8 + numpy 1.20.3。
- cddis-highrate-downloader：README 称无需账号，但实测 FTPS 425。
- ntrip-cpp：caster 需要 2 个构建补丁。
- IRI-MATLAB-FileExchange 手册坑 9 已过时（目录已是 BSD-2-Clause，手册未改）。

## 字段统计
13 个条目，21 个字段：analysis_zh 12、desc_zh 4、one_liner_zh 4、license 1。无 URL 变更。

## 再生成
用 origin/main `research/merge_routine_20260926c.py` 的 regenerate_lists / regenerate_categories / regenerate_readme；
改前 dry-run 零差异；改后只动 lists/01、03、04、05。总计 1026，provenance 330/212/484，RETIRED_URLS 56。
