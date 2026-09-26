# QC audit — 2026-09-26 batch 46 (generator drift fix, academic_lab-on-personal-account sweep idx 0–400, company orgs idx 0–400)

Base: origin/main aa9dcd5 (batch 45). Catalog **1029 → 1029** (no adds, no removals). Evidence read 2026-09-26 ~03:45–04:15 ET via `gh api users/X` (97 owners) and `gh api repos/X/Y/readme` (67 READMEs).

## Task 0 — entries newer than batch 45
None: HEAD = origin/main = aa9dcd5, `project_count` 1029, nothing appended after batch 45. No unpushed local commits.

## Task 1 — merge_routine_20260926c.py drift
Cause: all 10 finds in `research/routine_finds_20260926c.json` already exist in PROJECTS.json. For existing URLs, `main()` calls `_merge_fields.merge_project_fields`. Its provenance rule is "never downgrade" (personal_community 1 < academic_lab 2 < official 3). That rule treats stale finds values as upgrades and reverts QC decisions:
- smartphone-gnss-booster → academic_lab. Batch 35 had set personal_community.
- novatel_edie → official and trimble_driver_ros → official. Batch 45 had set both to personal_community under the company policy.

The text fields (desc/one_liner/analysis) were safe because the helper keeps existing non-trivial QC text, but the finds file still carried the pre-QC wording ("官方").

Fix (two independent layers):
1. **Finds JSON synced to current PROJECTS.json values.** 22 fields changed: provenance ×3, desc_zh ×10, one_liner_zh ×2, analysis_zh ×2, and url casing ×5 (Ryanf55, Smartphone-GNSS-Booster, UM982Driver, UnicoreDriver, BDS-RawScope).
2. **Script guard.** For existing URLs, `main()` now drops `provenance`, `category` and `subcategory` from the incoming record before merging, so QC owns those fields.

Each layer alone gives a zero diff. Checked by applying the old finds file through the guarded path: 0 changes for all 10 entries.

Verification:
- `python3 research/merge_routine_20260926c.py` prints `SKIP url` ×10, `ADDED 0`, `UPDATED 0`, then `SKIP_WRITE`.
- Before the PROJECTS edits, running `regenerate_lists` / `regenerate_categories` / `regenerate_readme` directly also produced no diff.

Other finds files (not changed; reported only). A dry run of `merge_project_fields` against current data shows the same rank-upgrade risk:
- provenance: routine_finds_20260918 (VARION, Cube), 20260920 (ubxlib), 20260923b (gnss_timeseries_viewers), 20260924 (ocbpy), 20260924g (aacgmv2, DD-cycle-slip-lab), 20260924s (GTrop, Mapping-Function…, TropDS, saga-utils), similar_finds (GNSSR_MERRByS_Python, GNSS_RR, DDM-Former, cssrlib, cssrlib-data, AETHER, …)
- licence: more_finds 21, new_finds 14
- language: web_finds 1 (gpsd-website)

Those old merge scripts must not be re-run as-is. The systemic fix would be to make `_merge_fields` keep an existing non-empty provenance.

## Task 2 — academic_lab on personal (User) GitHub accounts, idx 0–400
Scope: 126 academic_lab entries in idx 0–400. 18 are not on GitHub (official sites/UPC/UML/GitLab institute pages) and were left alone. The other 108 are on 83 GitHub owners; `gh api users/X` shows 54 User and 29 Organization. That leaves **66 entries on User accounts**, and every README was read.

Rule (same as batch 45): keep academic_lab only if the README clearly names a university lab, group or institute releasing the code. Otherwise use personal_community.

### Flipped academic_lab → personal_community (42)
| idx | project | owner (users/X: name; company) | README evidence |
|---|---|---|---|
| 15 | crz2rnx | zhufengGNSS (zigzag2015; —) | no README |
| 17 | DRCycleSlip | Jin-Whu (—; —) | no lab/group named |
| 43 | gstream | Jin-Whu (—; —) | no lab/group named |
| 297 | DiffIonMap | Jin-Whu (—; —) | no lab/group named |
| 354 | IonMap | Jin-Whu (—; —) | no lab/group named |
| 63 | PyRINEX | geumjin99 (Han Jinzhen; Sungkyunkwan University) | paper/DOI citation only |
| 87 | awsgnssroutils | gnss-ro (—; —) | README: maintained by Atmospheric and Environmental Research, Inc. (company), NASA-funded |
| 88 | BDS-3-PPP-B2b-DATA | zp-9696 (zhou ping; Chang‘an university) | mentions a decoder by Dr. Tao Jun (WHU), not the owner |
| 147 | APAS-TR | Birinci-S (sinanbirinci; —) | "developed for academic and research purposes"; paper citation only |
| 150 | CSSR-tool | MayHarryWang (Harry Wang; —) | paper citation (Wang & Jan) only |
| 221 | Urban-RTKLIB | MayHarryWang (Harry Wang; —) | paper citation (Wang & Jan) only |
| 155 | GAMP_PPPH | zhufengGNSS (zigzag2015; —) | no lab/group named |
| 161 | GNSS-Explorer | brucezhcw (brucezhcw; HKUST) | no lab/group named |
| 186 | MG_APP | XiaoGongWei (xiaogongwei; IGG) | "Copyright (C) 2016-2020 XiaoGongWei" |
| 194 | PPP | XiaoGongWei (xiaogongwei; IGG) | no lab/group named |
| 191 | Net_Diff | YizeZhang (—; Shanghai Astronomical Observatory) | "contact me (zhyize@163.com)" |
| 188 | MRTKLIB | h-shiono (hato.GNSS; —) | author Hayato Shiono; derived from JAXA/TOSHIBA MALIB |
| 189 | mrtklib-docker-ui | h-shiono (hato.GNSS; —) | no lab/group named |
| 210 | RTK | GYH-WHU (GYH; WHU) | no lab/group named |
| 220 | SPP_SPV | GYH-WHU (GYH; WHU) | no lab/group named |
| 222 | Analog-GPS-data-receiver | leaningktower (leaning_tower; UIUC) | no lab/group named |
| 227 | BeiDou_B1C | lnexenl (lnex; HKUST) | no lab/group named |
| 252 | gnsssdrgui | UHaider (Usman Haider; NUST) | GSoC 2017 project |
| 285 | AURORA | egavazzi (Etienne Gavazzi; UiT The Arctic University of Norway) | deprecated, points to egavazzi/AURORA.jl; no lab |
| 295 | csonde-gnss-ionosphere | csonde (Gergely Csonde; —) | TDK student-paper links (BME) |
| 301 | ED-AttConvLSTM | leeliangchao (Liangchao Li; China University of Geosciences (Beijing)) | paper artifact; no lab |
| 303 | EGNOSTools | DfAC (Lukasz K Bonenberg; EC Joint Research Centre (JRC) E.2) | no lab/group named |
| 312 | FIRI-2018 | AlexT1983 (—; —) | no lab/group named |
| 319 | geospacelab | JouleCai (Lei Cai, Ph.D.; University of Oulu) | no lab/group named |
| 322 | GIM_fusion_VLBI | arrueegg (Arno Rüegg; ETH Zürich) | no lab/group named |
| 331 | GNSS-Workshop-TEC | breid-phys (—; —) | no lab/group named |
| 333 | GNSS_TOM | sailvssea (Jesse YU; —) | no lab/group named |
| 343 | INPE-TEC-Maps-IONEX | Hollweg (Guilherme V. Hollweg; University of Michigan - Dearborn) | no lab/group named |
| 355 | iono-tomography | brianbreitsch (Brian; —) | no lab/group named |
| 356 | IonoBench | Mert-chan (—; —) | paper citation only |
| 357 | IonOccAnalysis | wonder2019WHU (—; —) | no lab/group named |
| 363 | ionosonde_volgatech | Vladimi-lan (Vladimir; —) | no README |
| 368 | ionospheric-tec-forecasting-IISC | codewithavra (codewithavra; —) | no lab/group named |
| 370 | Ionospheric-TEC-ROTI-Interactives | Tesfay-Tesfu (Tesfay Yemane Tesfu; UNIVAP, NASA) | no lab/group named |
| 372 | ionotec | sylvathle (Sylvain Blunier; European Space Agency) | no lab/group named |
| 373 | IonoTomo | Joshuaalbert (Joshua G Albert; Caltech) | no lab/group named |
| 397 | jvierine-ionosonde | jvierine (Juha Vierinen; —) | UNIS operates the prototype deployment; README names no lab releasing the code |

Text that implied an institutional release was reworded:
- 161 desc "HKUST 方向" → "个人仓（作者属 HKUST）"
- 222 desc "UIUC 相关业余项目" → "个人业余项目（作者属 UIUC）"
- 227 desc "HKUST 方向" → "个人试验仓（作者属 HKUST）"
- 220 one_liner "武大相关…教学" → "个人课程实验"
- 147 one_liner "土耳其高校" → "土耳其研究者的"
- 357 one_liner "（武大相关）" → "（个人仓）"
- 363 one_liner adds "（个人仓）"
- 303 desc "JRC 相关个人仓" → "作者任职 JRC 的个人仓"
- 194 desc "MG-APP 作者相关" → "MG-APP 作者的个人练习仓"
- 295 analysis "匈牙利相关学位论文" → "BME（匈牙利）学生论文配套个人代码"

Accuracy fix: 397 jvierine-ionosonde desc "社区活跃的电离图处理与测高仪相关脚本集合" → "基于 USRP 的 Python 软件定义跳频测高仪，可垂直/斜向探测并出电离图". The README describes a frequency-hopping radar or ionosonde built on UHD/USRP.

### Kept academic_lab: the README names the lab, group or institute (18)
- FAST (20): "by AIR, Chinese Academy of Sciences"
- GAMPII-GOOD (21): UNIQ navigation lab, SDUST
- MAPS (46) and B2bLIB (148): GCCLib group account, following the batch 44/45 precedent
- gnss-ppp-matlab-toolbox (162): "Copyright … Delft University of Technology"
- GraphGNSSLib (173): IPNL, PolyU
- POSGO (193): Satellite POD and Navigation Augmentation Group, WHU
- PRIDE-PPPAR (202): PRIDE Lab / GNSS Research Center, WHU
- RTKLIB-B2b (213): "Copyright … Chunbo Liu / APM, CAS"
- GNSS-matlab (241) and GNSS-VHDL (250): UPC RSLab
- GPSL1-DPEmodule (261) and GPSL1-MMT-DPEmodule (262): PolyU AAE / IPNL, PNT Signal Processing Group
- ionex_reader (352): IIT Indore Space Technology & Radio Cosmology Group
- Ionospheric-TEC-Kriging-Turkiye (369): IONOLAB Research Group
- Already checked in earlier batches: geode (23, batch 44), PPPH-UAV (200, batch 44), SoftGNSS (276, batch 45)

### Borderline, kept academic_lab (reported, not changed)
- **PPP_AR (198, heiwa0519):** the README names no lab. Kept for owner consistency with TGINS (562), whose README gives the author's department (安徽理工大学空间信息与测绘工程学院) and which batch 45 kept as borderline. The desc "中国矿业大学方向" was not supported by any README and now reads "TGINS 作者（安徽理工大学测绘学院）的…".
- **meta-gnss-sdr (267, carlesfernandez):** © is the individual (Carles Fernández-Prades), with national-grant funding. The same owner's docker-gnsssdr is © CTTC and was kept in batch 45.
- **RTStreamHub (79) and HASPPP (179), ZhangRunzhi20:** core developer e-mail is ntsc.ac.cn. Per the batch 45 precedent, an institutional e-mail with no lab named stays borderline.
- **BDS-3-B1C-B2a-SDR-receiver (223, lyf8118):** authors give colorado.edu e-mails; no lab named.
- **IRI_TID (391, w2naf):** batch 45 borderline, unchanged.

Owner consistency after the flips: only heiwa0519 would have been mixed, and it was resolved as above. There are 0 owners with mixed provenance among the flipped owners.

### Company orgs, idx 0–400
- The 29 Organization owners of academic_lab entries plus 14 more owners of official/academic entries were checked with `gh api users/X`.
- No company org holds official or academic_lab in idx 0–400. The official owners are government bodies, agencies or consortia (EarthScope Consortium, Geoscience Australia, NCAR, QZSS Strategy Office, CSA, Kartverket, NASA, NLS Finland, CGS-GIS/NRCan, JAXA-SNU, embrace-inpe, NOAA-SWPC, ION SDR Metadata WG); ros-drivers was already noted as borderline in batch 45.
- I scanned personal_community entries in idx 0–400 for "官方". No hit calls a company release "官方". The hits are "官方镜像/官方下载" references to upstream agencies, and AgOpenGPS-Official is the community project's own org name.
- awsgnssroutils (87) is a company release (AER Inc.) and was flipped under the company policy; its text has no "官方" wording.

## Validation
- JSON valid. project_count 1029 = len(projects) = Σcounts_by_category = Σprovenance_counts. No duplicate URLs or names.
- counts_by_category unchanged.
- PROJECTS.json diff: provenance ×42, desc_zh ×7, one_liner_zh ×4, analysis_zh ×1, provenance_counts ×2.
- Regenerated with the fixed generator's functions. Lists 01/03/04/07/10 changed only in badge rows plus 1 analysis line; the README provenance line changed; categories.md is unchanged. `main()` remains a no-op after the edits.
- provenance (official / academic_lab / personal_community): **333 / 284 / 412 → 333 / 242 / 454**.

## Leftovers
- Other routine_finds / *finds JSON files still carry stale provenance/licence values (listed in Task 1). Their merge scripts must not be re-run without the same guard, or `_merge_fields` needs a policy change.
- Borderline academic e-mail or department-only cases (above) need a policy call.
- The 18 non-GitHub academic_lab entries in idx 0–400 were not re-reviewed; they are institutional sites.
