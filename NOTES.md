# NOTES — 编纂与核验说明

生成日期：2026-09-14  
条目数：**207**

## 来源

1. 既有 PROJECTS.json（55，电离层较完整）
2. research/seed_urls.json（282：awesome-gnss + Navigation-Learning）
3. 人工核验：GitHub API / 官方站点（VMF、RNXCMP、BNC、Anubis、EGNOS Toolkit）
4. 维护者 stars / forks（SH-GIM、PyTECGg、georinex）

## 过滤

- 不收录私有库与虚构 URL
- Navigation-Learning 中与 GNSS/PNT 无关的纯 SLAM/深度学习列表已过滤
- Fork 去重为上游 canonical URL，fork 关系写入 markers

## 分类计数

| category | count |
|---|---:|
| ionosphere | 37 |
| troposphere | 15 |
| gnss-data | 30 |
| gnss-positioning | 51 |
| orbit-clock | 2 |
| navigation-ins | 16 |
| gnss-sdr | 45 |
| mobile-apps | 4 |
| tools-learning | 10 |
| **total** | **210** |

## 稀疏领域

对流层独立 GitHub 项目偏少（标准码在 TU Wien）；轨道/钟差/DCB 多集成于大型套件，故不硬凑数量。

## 质量修订（2026-09-14）

- 重写 Navigation-Learning 模板分析 **59** 条；删除 404/非 GNSS **3** 条（CSolgaard/GNSS-IR、iliasam/gps_rf_frontend_sim、aipixel/GPS-Gaussian）
- 纠正 SupakunZ/GNSS_RTK → `gnss-positioning`；若干 SDR/INS 条目归入 `gnss-sdr` / `navigation-ins`
- 剔除全文复制粘贴的 README对照 / IGS交叉检查 结尾套话
- 当前条目：**207**

## 质量修订（2026-09-14）

- 重写 Navigation-Learning 模板分析 **59** 条；删除 404/非 GNSS **3** 条（CSolgaard/GNSS-IR、iliasam/gps_rf_frontend_sim、aipixel/GPS-Gaussian）
- 纠正 SupakunZ/GNSS_RTK → `gnss-positioning`；误放的 SDR/INS 条目分别归入 `gnss-sdr` / `navigation-ins`
- 剔除全文复制粘贴的 README对照 / IGS交叉检查 结尾套话
- 当前条目：**207**

## 增量合并（2026-09-14）

- 自 `research/missing_meta.json` 与补充 gh 检索合并新增 **48** 条
- 当前条目：**255**
- 分类计数：{'ionosphere': 49, 'troposphere': 13, 'gnss-data': 44, 'gnss-positioning': 36, 'orbit-clock': 3, 'navigation-ins': 38, 'gnss-sdr': 51, 'mobile-apps': 10, 'tools-learning': 11}
- 详见 `research/new_finds.json`

## 二次穷尽检索合并（2026-09-14）

- 自 `research/more_finds.json` 合并新增 **54** 条（武大 GREAT/i2Nav、B2b/HAS、闪烁、质检、NTRIP 等）
- 当前条目：**309**
- 分类计数：{'ionosphere': 52, 'troposphere': 13, 'gnss-data': 56, 'gnss-positioning': 55, 'orbit-clock': 6, 'navigation-ins': 48, 'gnss-sdr': 53, 'mobile-apps': 11, 'tools-learning': 15}
- 检索日志：`research/search_log.md`
- 未改写既有 analysis；`new_finds.json` 保留前次合并结果

## Web/官方扩充（2026-09-14）

- 写入 `research/web_finds.json`：**42** 条经 curl/Web 核验的官方/高校/社区站点条目（原创中文简介）
- 合并入 `PROJECTS.json` 净增 **42**（309→351；原已有 BNC/RNXCMP/VMF/Anubis/EGNOS 等仅富化）
- 全量补齐 `provenance` + `host`；列表/README 显示 🏷️ 官方 / 高校实验室 / 个人社区
- ntripserver / ntripclient / rtcm3torinex 改挂 RTCM-Ntrip 官方 wiki
- 新增代表：IRI 官方、Galileo NeQuick G、gLAB-UPC、BKG Caster、TEQC、GFZRNX、SPOCC、EarthScope gnsstools、gpsd、HTDP、GA Ginan 门户等
- **未 git push**

来源统计：official=44, academic_lab=81, personal_community=226  
当前总条目：**351**

## IRI/RELATED LINKS 深挖（2026-09-14）

- 源页：https://irimodel.org/ （含 RELATED LINKS、各 Fortran 目录、IRTAM）
- 研究稿：`research/iri_related_finds.json`
- 新增 **9**：PyIRTAM, iricore, pyIRI2016, ionex_reader, ionex_formatter, mgfernan-pygnss, IRTAM-Coefficient-Reader-Fortran, GAMBIT-Database-Reader-Java, SAO-Explorer
- 去掉重复 NeQuick2-ICTP 首页条目（保留 source-code）
- RELATED LINKS 网页服务（MIT/IPS/Kyoto/SPENVIS/ESA SWE）均跳过，见 finds 的 skipped
- 当前总条目：**371**；电离层：**78**
- **未 git push**

