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

## GNSS 数据源类扩充（2026-09-14）

- 新增类别 `gnss-datasets` → `lists/10-gnss-datasets.md`
- 写入 `research/data_portals.json`，本轮合并新增 **51**
- 说明文档：`docs/data-access.md`（Earthdata/CDDIS、IGS 目录、注册徽章）
- 注册方式统计：{'open': 41, 'form_register': 9, 'email_register': 1}
- 未 git push

当前总条目：**422**（gnss-datasets=51）

## 例行检索合并（2026-09-14 例行：GNSS开源目录持续补全）

- 稿件：`research/routine_finds_20260914.json`（9 条核验候选）
- 本轮净增 **9**：MADOCALIB, CLASLIB, MALIB, APAS-TR, HASlib, GHASP-HAS-decoding, gnss-ppp-matlab-toolbox, Essential-GNSS, GNSSommelier
- 跳过：[]
- 重点：QZSS MADOCALIB/CLASLIB/MALIB、芬兰 HASlib、APAS-TR、EarthScope GNSSommelier、Essential GNSS（SourceForge）等
- 当前总条目：**431**
- 来源统计：official=109, academic_lab=89, personal_community=233

## 相似项目补录 batch2（2026-09-14）

- 新增 **20** 条（cssrlib/PocketSDR/PPP-Wizard/NTRIP/TEC/PWV 等）
- 当前条目：**468**
- 分类计数：{'ionosphere': 85, 'troposphere': 25, 'gnss-data': 81, 'gnss-positioning': 72, 'orbit-clock': 9, 'navigation-ins': 50, 'gnss-sdr': 56, 'mobile-apps': 11, 'tools-learning': 26, 'gnss-datasets': 53}
- 详见 `research/similar_finds.json`

## 例行检索补录（2026-09-16）

- 新增 **21** 条（RADIATE/mpsim/Gkit-Bias/autorino/rinexmod/FGO/ROS/RAIM 等）
- 当前条目：**489**
- 分类计数：{'ionosphere': 85, 'troposphere': 29, 'gnss-data': 86, 'gnss-positioning': 74, 'orbit-clock': 12, 'navigation-ins': 54, 'gnss-sdr': 57, 'mobile-apps': 11, 'tools-learning': 27, 'gnss-datasets': 54}
- 详见 `research/routine_finds_20260916.json`

## IONORING / eSWua TEC（2026-09-17）

- 用户提示补充：IONORING（意大利实时 TEC）+ eSWua-TEC 数据门户
- 新增：**2** → IONORING, eSWua-TEC
- 类别：`gnss-datasets` / 电离层产品；provenance=official
- 说明：公开的是监测产品与 Web 服务，不是开源处理代码仓

当前总条目：**491**

## 电离层全网补搜合并（2026-09-17）

- 四路并行：`batch_iono_models` / `batch_official_labs` / `batch_related_iono` / `batch_non_github`
- 原始候选约 128，交叉去重后新增 **120**（已与目录 URL 去重；跨批重复优先保留官方实验室条目）
- 标记：`batch-2026-09-17`
- 类别分布（本批）：{'gnss-data': 2, 'gnss-datasets': 4, 'ionosphere': 112, 'tools-learning': 2}
- 来源分布（本批）：{'personal_community': 20, 'academic_lab': 60, 'official': 40}

当前总条目：**611**

## 教学讲解入门→精通（2026-09-17）

- 新增 `docs/tutorials/`：**17** 课（01–08 入门与目录用法；09–17 进阶/精通/实战）
- 索引按「入门 / 进阶 / 精通·实战」组织，根 README 已链到教学目录
- 同步继续 gap-fill 搜索（见 `research/batch_gapfill_*`，若尚未生成则仍在跑）

## 教学加厚 + 实验课 18（2026-09-17）

- 加厚精通篇 12/14/15/16/17；新增实验课 `18-lab-compare-gims.md`（多分析中心 GIM 对比）
- `docs/tutorials/README.md` 按 入门 / 进阶 / 精通·实战 / 实验课 重组
- 补搜仍在进行（gap-fill）

## 教学详写（用户反馈过浅后重写，2026-09-17）

- 用户明确要求：零基础可懂、极详细、类比+词表+步骤+误区+习题
- 已详写推送批次：01（约1.5万字）、05–08（各约0.8–0.9万字）
- 02–04、09–18 仍在按同样标准重写中

## 14–18 详写批次（2026-09-17）

- 14–18 均重写为约 0.86–0.94 万字零基础详讲
- 02 已加厚至约 1.4 万字；03、04 仍在重写
- 12、13 已加厚

## Gap-fill 合并（2026-09-17）

- 来源：`research/batch_gapfill_20260917.json`
- 新增 **36** 条（IRI 封装、IONEX/TEC、闪烁/Septentrio、SBAS、层析、掩星、SAMI2 等）
- 目录总量见 README / PROJECTS.json

## 03/04 详写收尾（2026-09-17）

- `03-gim-ionex.md` ≈10938 字；`04-iri-nequick.md` ≈10577 字
- 至此 `docs/tutorials/` 01–18 均已按零基础详讲标准重写（普遍 0.8–1.5 万字级）

## 现象分析加厚批次（2026-09-17）

- 加厚 01–03、05–08（现象分析视角 + 操作清单）
- 新增现象课草稿推进中：19 概述、20 磁暴 TEC（21–23 续写）

## 现象分析 19–23 收官（2026-09-17）

- 新增/定稿：19 概述、20 磁暴 TEC、21 赤道异常与气泡、22 TID、23 耀斑与日食
- README 学习路径改为：入门（建模概念）→ 现象分析 → 精通·实战
- 01–08 同步加入现象向读图/质控段落

## 原理细讲批次（2026-09-17）

- 05 闪烁/ROTI：Fresnel、S4/σφ 符号拆解、ROTI≠S4、赤道vs高纬驱动、整夜分析剧本（约 3.0 万字）
- 09 DCB：几何无关组合硬件延迟、星/站 DCB、基准约束、5 TECU 数值例、绝对/相对适用边界（约 2.6 万字）
- 01–03、20–21 同步加厚进行中；22–23 待续

## 01/02 原理细讲收官（2026-09-17）

- 01 ≈23869 字：等离子体频率、Appleton–Hartree→一阶群延迟逐符号、40.3 系数、L1/L2 数值例、薄壳映射
- 02 ≈24061 字：码/相位观测方程、几何无关组合手算 α≈9.52、平滑与周跳、DCB 量纲换算、迷你 RINEX→VTEC
- 03/22 同步加厚中；04、23 待续加厚

## 04/20–23 原理细讲收官（2026-09-17）

- 04 ≈23102 字：IRI 求 Ne(h)、气候vs天气、F10.7/Ap 进参数、NeQuick-G/Az、残差法庭 α/β/γ
- 20–23 现象机制加厚至约 1.6 万字/课（磁暴因果链、EIA/EPB、TID、耀斑/日食光化学时间线）
- 核心原理课 01–05、09、20–23 本轮细讲批次完成

## 公式渲染与配图修复（2026-09-17）

- 教程全文：将 `\(...\)` / `\[...\]` 改为 GitHub 可渲染的 `$...$` / `$$...$$`
- 新增 `docs/tutorials/images/` 自制示意图 6 张（CC0），来源见 `images/SOURCES.md`
- 已嵌入：01（大气分层、延迟–频率、薄壳）、02（几何无关）、03（薄壳）、20（暴日残差）、21（EIA 双峰）
- `docs/tutorials/README.md` 增加「阅读说明（公式与图片）」

## 公式二次修复（2026-09-17）

- 根因：GitHub 同一行多个带 `\` 的 `$...$` 易错位露源码（测验「答」行尤甚）
- 处理：单位改 Unicode（m⁻²、10¹⁶）；多公式「答」改 `$$` 块；题干减少行内公式密度

## 公式全库加固（2026-09-17）

- 扫描全部 `docs/tutorials/[0-9]*.md`：凡同一行 ≥2 个带 `\` 的 `$...$` 一律处理
- 表格行：复杂行内公式改为 Unicode/纯文本，避免一行多 `$` 触发 GitHub 错位
- 正文：多公式合并为单个 `$...$`（中间中文用 `\text{}`）或保持已有 `$$` 块
- 验收：风险行计数归零后再推送

## 公式误修回滚与重做（2026-09-17）

- 发现问题：此前「合并同行多 `$`」时把中文塞进 `\text{}`，造成巨型行内公式在 GitHub 整段露源码
- 纠正：全库拆开含 `\text{}` 的行内 `$...$`——**中文回正文，短公式单独留**；单位优先 Unicode；同行至多一个带 `\` 的行内公式
- 验收：`\text{` 行内 = 0；同行多 `$`+`\` = 0

- 复查：截图处巨型 `$...\text{中文}...$` 已拆；测验 `$$` 内中文 `\text{}` 改为正文

## 公式彻底去行内 LaTeX（2026-09-17）

- 用户截图：` $E=90^\circ,\quad\cos E=0$ ` 一类行内公式在 GitHub 仍露源码
- 处理：全库教程 **行内 `$...$` 凡含 `\` 一律转 Unicode/纯文本**；剩余简单 `$E$` 改为 `*E*`
- 复杂公式只保留独立 `$$...$$` 块；禁止中文进 `\text{}`；禁止一行多个带 `\` 的行内公式

- 根因补刀：课文「阅读提示」里写了字面量 `$$`，GitHub 当成公式块起点，后面整段测验被吞、行内公式全露源码；已改为全角 `＄＄`，并再次清零行内带 `\` 的 `$...$`

## 公式回滚纠偏（2026-09-17）

- 前几轮「全库 Unicode / 替换 $$」把正文改乱（全角 ＄＄、公式碎片）
- 已将 `docs/tutorials/` **回滚到 fcc8426**（GitHub `$`/`$$` 可读的版本），仅保留几何直觉 B 条的明文角度写法
- 不再做全库暴力替换；后续只定点修露源码行

## 例行检索补录（2026-09-18）

- 稿件：`research/routine_finds_20260918.json`（9 条核验候选）
- 本轮净增 **9**：GSILIB, VARION, Cube, ATom-TUWien, OpATOM, geoveil-mp, geoveil-cn0, ntrip-caster-go, SparkFun_u-blox_GNSS_v3
- 跳过：pppx（学术非商用二进制发行，非 OSI 开源）、SouthPAN-GNSS-Receiver-Documentation（已归档文档仓）、INTOMO/SNACS（无公开源码或页面不可核验）
- 当前条目：**656**
- 分类计数：{'ionosphere': 232, 'troposphere': 31, 'gnss-data': 92, 'gnss-positioning': 76, 'orbit-clock': 13, 'navigation-ins': 54, 'gnss-sdr': 57, 'mobile-apps': 12, 'tools-learning': 29, 'gnss-datasets': 60}
- 来源统计：{'official': 160, 'academic_lab': 196, 'personal_community': 300}

## 例行检索补录（2026-09-21）

- 新增 **14** 条（earthscope-sdk/gnssanalysis/PyGNSSFix/ntrip-core/esp32-xbee/Heki/gnssFGO/UFCORS/OPUS 等）
- 当前条目：**706**
- 分类计数：{'ionosphere': 235, 'troposphere': 32, 'gnss-data': 108, 'gnss-positioning': 78, 'orbit-clock': 13, 'navigation-ins': 57, 'gnss-sdr': 58, 'mobile-apps': 16, 'tools-learning': 29, 'gnss-datasets': 80}
- 详见 `research/routine_finds_20260921.json`

## 例行检索补录（2026-09-23）

- 新增 **15** 条（RINGO/M3G/EPOS-GLASS/IBGE-PPP/CSRS-PPP/OPUS-Projects/ncat-lib/BEV-APOS/TITIPy 等）
- 当前条目：**721**
- 分类计数：{'ionosphere': 237, 'troposphere': 32, 'gnss-data': 109, 'gnss-positioning': 80, 'orbit-clock': 13, 'navigation-ins': 57, 'gnss-sdr': 58, 'mobile-apps': 16, 'tools-learning': 30, 'gnss-datasets': 89}
- 详见 `research/routine_finds_20260923.json`
- 来源统计（本轮新增）：official 11 · academic_lab 2 · personal_community 2

## 例行检索补录（2026-09-23b）

- 新增 **15** 条（RINGO/M3G/EPOS-GLASS/IBGE-PPP/CSRS-PPP/OPUS-Projects/ncat-lib/BEV-APOS/TITIPy 等）
- 当前条目：**733**
- 分类计数：{'ionosphere': 236, 'troposphere': 32, 'gnss-data': 111, 'gnss-positioning': 82, 'orbit-clock': 13, 'navigation-ins': 59, 'gnss-sdr': 59, 'mobile-apps': 16, 'tools-learning': 31, 'gnss-datasets': 94}
- 详见 `research/routine_finds_20260923b.json`

## 例行检索补录（2026-09-24）

- 新增 **14** 条（AUSPOS/APREF/GA-RINEX-API/SouthPAN/CDDIS-DCB/RMextract/ocbpy/VN-DGNSS 等）
- 当前条目：**747**
- 分类计数：{'ionosphere': 238, 'troposphere': 33, 'gnss-data': 111, 'gnss-positioning': 83, 'orbit-clock': 13, 'navigation-ins': 59, 'gnss-sdr': 59, 'mobile-apps': 18, 'tools-learning': 31, 'gnss-datasets': 102}
- 详见 `research/routine_finds_20260924.json`

## 2026-09-24 — Catalog QC batch 5

- Commit landing catalog edits: `dd221d6` (also bundled docs/software pinot+autorino manuals from parallel work)
- SPDX license fills: **11** (9 restore after routine-merge wipe + tec_forecast MIT, VINS-GPS-Wheel GPL-3.0)
- Provenance: **6** upgrades (nmea-msgs/FAST restore; GraphGNSSLib, Net_Diff, GNSS-Metadata-Standard, raPPPid); Baidu/AgOpenGPS kept `personal_community` per categories.md
- Chinese rewrites: **31** short human blurbs (`desc_zh` ≠ `one_liner_zh`)
- Language fills: **0** (null/quirky only); HTTPS upgrades: **0** (6 leftovers still fail)
- Entries touched: **43**; `project_count` **747**; provenance_counts official=205 academic_lab=227 personal_community=315
- Audit: `research/qc-audit-20260924-batch5.md`

## 例行检索补录（2026-09-24b）

- 新增 **13** 条（IGN-RGP/OS-Net/PositioNZ/NSGI/OKVIS2-X/lowtran 等）
- 当前条目：**760**
- 分类计数：{'ionosphere': 239, 'troposphere': 34, 'gnss-data': 111, 'gnss-positioning': 83, 'orbit-clock': 13, 'navigation-ins': 60, 'gnss-sdr': 59, 'mobile-apps': 19, 'tools-learning': 31, 'gnss-datasets': 111}
- 详见 `research/routine_finds_20260924b.json`

## 例行检索补录（2026-09-24c）

- 新增 **14** 条（RAMSAC/QZSS/GSI-SFTP/INEGI/UNR-NGL/GipsyX/galileo-osnma 等）
- 当前条目：**774**
- 分类计数：{'ionosphere': 239, 'troposphere': 34, 'gnss-data': 112, 'gnss-positioning': 85, 'orbit-clock': 13, 'navigation-ins': 60, 'gnss-sdr': 59, 'mobile-apps': 19, 'tools-learning': 32, 'gnss-datasets': 121}
- 详见 `research/routine_finds_20260924c.json`

## 例行检索补录（2026-09-24d）

- 新增 **14** 条（minmea/GPS.js/asv-gnss/gnssSNR/deep_gnss/TUSAGA/pcc-explorer 等）
- 当前条目：**788**
- 分类计数：{'ionosphere': 240, 'troposphere': 35, 'gnss-data': 117, 'gnss-positioning': 88, 'orbit-clock': 13, 'navigation-ins': 60, 'gnss-sdr': 59, 'mobile-apps': 20, 'tools-learning': 34, 'gnss-datasets': 122}
- 详见 `research/routine_finds_20260924d.json`

## 例行检索补录（2026-09-24e）

- 新增 **14** 条（VINS-Fusion/LimeGPS/Orekit/FAA-WAAS/EGNOS-GSC/ITU-Rpy 等）
- 当前条目：**802**
- 分类计数：{'ionosphere': 240, 'troposphere': 37, 'gnss-data': 117, 'gnss-positioning': 89, 'orbit-clock': 14, 'navigation-ins': 63, 'gnss-sdr': 61, 'mobile-apps': 21, 'tools-learning': 36, 'gnss-datasets': 124}
- 详见 `research/routine_finds_20260924e.json`

## 例行检索补录（2026-09-24f）

- 新增 **14** 条（RobustGNSS/PrNet/igrf/rinex-adapter/GSC-OSNMA/Earthdata-MGEX 等）
- 当前条目：**816**
- 分类计数：{'ionosphere': 242, 'troposphere': 37, 'gnss-data': 119, 'gnss-positioning': 94, 'orbit-clock': 14, 'navigation-ins': 63, 'gnss-sdr': 61, 'mobile-apps': 22, 'tools-learning': 39, 'gnss-datasets': 125}
- 详见 `research/routine_finds_20260924f.json`

## 例行检索补录（2026-09-24g）

- 新增 **14** 条（tudatpy/orbdetpy/Navipedia/NAVCEN/RAIM/rinex-masker/aacgmv2 等）
- 当前条目：**830**
- 分类计数：{'ionosphere': 244, 'troposphere': 39, 'gnss-data': 120, 'gnss-positioning': 95, 'orbit-clock': 16, 'navigation-ins': 63, 'gnss-sdr': 62, 'mobile-apps': 22, 'tools-learning': 44, 'gnss-datasets': 125}
- 详见 `research/routine_finds_20260924g.json`

## 例行检索补录（2026-09-24h）

- 新增 **12** 条（fusioncore/ELT_RTKBase/pysbf2/libnmea/ENRI/ICAO-PBN/go-gnss-rtcm 等）
- 当前条目：**842**
- 分类计数：{'ionosphere': 244, 'troposphere': 39, 'gnss-data': 126, 'gnss-positioning': 97, 'orbit-clock': 16, 'navigation-ins': 64, 'gnss-sdr': 62, 'mobile-apps': 22, 'tools-learning': 47, 'gnss-datasets': 125}
- 详见 `research/routine_finds_20260924h.json`

## 例行检索补录（2026-09-24i）

- 新增 **14** 条（IGS Tropo/Bias/MGEX/Antenna/RF WG、NRCan-TRX、BIPM-Time-FTP、LANS-AFS-SIM/PocketSDR-AFS、rt-navi 等）
- 当前条目：**856**
- 分类计数：{'ionosphere': 244, 'troposphere': 40, 'gnss-data': 128, 'gnss-positioning': 98, 'orbit-clock': 18, 'navigation-ins': 64, 'gnss-sdr': 65, 'mobile-apps': 22, 'tools-learning': 50, 'gnss-datasets': 127}
- 详见 `research/routine_finds_20260924i.json`

## 例行检索补录（2026-09-24j）

- 新增 **14** 条（azarashi/QZQSM/libswiftnav/NavAI/ionFR/gps-fpga/gnsshat、ESSP-EGNOS、LINZ、IERS、NOAA-WMM 等）
- 当前条目：**870**
- 分类计数：{'ionosphere': 245, 'troposphere': 40, 'gnss-data': 130, 'gnss-positioning': 100, 'orbit-clock': 20, 'navigation-ins': 64, 'gnss-sdr': 66, 'mobile-apps': 24, 'tools-learning': 53, 'gnss-datasets': 128}
- 详见 `research/routine_finds_20260924j.json`

## 例行检索补录（2026-09-24k）

- 新增 **14** 条（novatel/max2771/RTKLIB-PPK/pysatNASA/swiftnav-ros2、SWS闪烁、ISGI/CDAWeb/SSCWeb/UKSSDC/SWPC/CCMC 等）
- 当前条目：**884**
- 分类计数：{'ionosphere': 249, 'troposphere': 41, 'gnss-data': 130, 'gnss-positioning': 101, 'orbit-clock': 20, 'navigation-ins': 67, 'gnss-sdr': 67, 'mobile-apps': 24, 'tools-learning': 55, 'gnss-datasets': 130}
- 详见 `research/routine_finds_20260924k.json`

## 例行检索补录（2026-09-24l）

- 新增 **14** 条（NeoGPS/UbxGps/bolderflight-ublox、fixposition、SoftGNSS-octave、OpenIMU、SWS/SWPC/CelesTrak/ESA/Canada 等）
- 当前条目：**898**
- 分类计数：{'ionosphere': 254, 'troposphere': 41, 'gnss-data': 130, 'gnss-positioning': 101, 'orbit-clock': 21, 'navigation-ins': 69, 'gnss-sdr': 68, 'mobile-apps': 27, 'tools-learning': 56, 'gnss-datasets': 131}
- 详见 `research/routine_finds_20260924l.json`

## 例行检索补录（2026-09-24m）

- 新增 **14** 条（ublox-ros/nmea_navsat、MicroNMEA/107-Arduino、gpsdo/ublox-rs、SIDC/SILSO、Kyoto Dst/Kp、SWPC/SWS/GFZ Kp 等）
- 当前条目：**912**
- 分类计数：{'ionosphere': 262, 'troposphere': 41, 'gnss-data': 131, 'gnss-positioning': 101, 'orbit-clock': 21, 'navigation-ins': 71, 'gnss-sdr': 68, 'mobile-apps': 29, 'tools-learning': 57, 'gnss-datasets': 131}
- 详见 `research/routine_finds_20260924m.json`

## 例行检索补录（2026-09-24n）

- 新增 **14** 条（pymap3d、TEC-Maps-of-Nepal、NCAR-GLOW、pysat*、SGP4 多语言、dSGP4、ROB/BIPM/UNR/NGDC/OMNIWeb 等）
- 当前条目：**926**
- 分类计数：{'ionosphere': 265, 'troposphere': 41, 'gnss-data': 132, 'gnss-positioning': 101, 'orbit-clock': 26, 'navigation-ins': 71, 'gnss-sdr': 68, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 134}
- 详见 `research/routine_finds_20260924n.json`

## 例行检索补录（2026-09-24o）

- 新增 **14** 条（pymsis/NRLMSISE、SoapySDR 族、ASG-EUPOS/CROPOS/SWEPOS/Terras、ACE/LISIRD/BGS/GOES 等）
- 当前条目：**940**
- 分类计数：{'ionosphere': 271, 'troposphere': 41, 'gnss-data': 132, 'gnss-positioning': 101, 'orbit-clock': 26, 'navigation-ins': 71, 'gnss-sdr': 71, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 139}
- 详见 `research/routine_finds_20260924o.json`

## 例行检索补录（2026-09-24p）

- 新增 **14** 条（SoapyUHD/RTLSDR/Remote/Airspy/SDRPlay3、SRGI Ina-CORS、SDO/SOHO/DONKI/Helioviewer、AE/RTSW/GOES-Proton、CDDIS 轨道钟差等）
- 当前条目：**954**
- 分类计数：{'ionosphere': 278, 'troposphere': 41, 'gnss-data': 132, 'gnss-positioning': 101, 'orbit-clock': 27, 'navigation-ins': 71, 'gnss-sdr': 76, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 140}
- 详见 `research/routine_finds_20260924p.json`

## 例行检索补录（2026-09-24q）

- 新增 **14** 条（ReNEP/GNSSNet/CSN-Chile/SIRGAS stations、EPN tropo/data-access、VMF1/VMF3、EMM/PSMSL、SWPC synoptic/events、IVSOPAR、nyx 等）
- 当前条目：**969**
- 分类计数：{'ionosphere': 281, 'troposphere': 44, 'gnss-data': 133, 'gnss-positioning': 101, 'orbit-clock': 29, 'navigation-ins': 71, 'gnss-sdr': 76, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 146}
- 详见 `research/routine_finds_20260924q.json`

## 例行检索补录（2026-09-24r）

- 新增 **14** 条（CZEPOS/KASI/GA networks、EPN stationlist/coordinates、SIRGAS weekly、Earthdata GNSS/30s、ILRS/IVSCC、GLOSS/IOC、ISWA、ESA OPS-GN 等）
- 当前条目：**983**
- 分类计数：{'ionosphere': 282, 'troposphere': 44, 'gnss-data': 133, 'gnss-positioning': 101, 'orbit-clock': 32, 'navigation-ins': 71, 'gnss-sdr': 76, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 156}
- 详见 `research/routine_finds_20260924r.json`

## 例行检索补录（2026-09-24s）

- 新增 **15** 条（GAMIT/GLOBK、NASA GMAT、qzsl6tool、CSA AlouetteApp、NRL/HamSCI TID 工具、GTrop/TropDS/映射函数高程改正、anywhere-sdr 等）
- 当前条目：**998**
- 分类计数：{'ionosphere': 288, 'troposphere': 47, 'gnss-data': 135, 'gnss-positioning': 103, 'orbit-clock': 33, 'navigation-ins': 71, 'gnss-sdr': 77, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 156}
- 详见 `research/routine_finds_20260924s.json`

## 例行检索补录（2026-09-26）

- 新增 **13** 条（EISCAT/AMISR 非相干散射雷达门户、CEDAR Madrigal、子午工程、ROM SAF、FRDR SuperDARN、PITHIA eSC；pyDARN/RST、ppigrf、Lompe、LPI、inscar）
- 当前条目：**1011**
- 分类计数：{'ionosphere': 294, 'troposphere': 47, 'gnss-data': 135, 'gnss-positioning': 103, 'orbit-clock': 33, 'navigation-ins': 71, 'gnss-sdr': 77, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 163}
- 详见 `research/routine_finds_20260926.json`

## 例行检索补录（2026-09-26b）

- 新增 **15** 条（USGS/NRCan/BGS 地磁数据、MACCS、THEMIS GMAG、TGO 磁力计链、RAL 测高仪；PySPEDAS、MagPy、ChaosMagPy、resolvedvelocities、MIPS、BAFIM、digisondeindices、isr-raw）
- 当前条目：**1026**
- 分类计数：{'ionosphere': 302, 'troposphere': 47, 'gnss-data': 135, 'gnss-positioning': 103, 'orbit-clock': 33, 'navigation-ins': 71, 'gnss-sdr': 77, 'mobile-apps': 29, 'tools-learning': 59, 'gnss-datasets': 170}
- 详见 `research/routine_finds_20260926b.json`

## 例行检索补录（2026-09-26c）

- 新增 **10** 条（AeroRust nmea、NovAtel EDIE、Trimble GSOF ROS 驱动/Wireshark 插件、和芯星通 UM980/UM982 驱动与 PPK 流水线、SparkFun Unicore 库、smartphone-gnss-booster、BDS-RawScope）
- 当前条目：**1035**
- 分类计数：{'ionosphere': 302, 'troposphere': 47, 'gnss-data': 140, 'gnss-positioning': 103, 'orbit-clock': 33, 'navigation-ins': 73, 'gnss-sdr': 77, 'mobile-apps': 32, 'tools-learning': 59, 'gnss-datasets': 170}
- 详见 `research/routine_finds_20260926c.json`

## 例行检索补录（2026-09-26d）

- 新增 **1** 条（binex：nav-solutions Rust BINEX 编解码库，补齐 docs/software/binex.md 对应目录条目）
- 当前条目：**1027**
- 分类计数：{'ionosphere': 246, 'troposphere': 47, 'gnss-data': 138, 'gnss-positioning': 108, 'orbit-clock': 31, 'navigation-ins': 72, 'gnss-sdr': 76, 'mobile-apps': 32, 'tools-learning': 57, 'gnss-datasets': 220}
- 详见 `research/routine_finds_20260926d.json`
