# QC audit — 2026-09-26 batch 44 (provenance consistency, idx 0–400 fact audit, empty-subcategory check)

Base: origin/main 2726225 (batch 43). Catalog **1029 → 1029** (no adds, no removals). Evidence read 2026-09-26 ~03:35–03:55 ET via `gh api` (users/orgs, repos, readme, languages, GraphQL `isArchived/archivedAt`).

## Task 0 — entries newer than batch 43
None: HEAD = origin/main = 2726225, `project_count` 1029, nothing appended after batch 43.

## Task 1 — provenance consistency by GitHub owner
462 GitHub owners; 4 had mixed provenance. All resolved:

| owner | `gh api users/…` evidence | before | after |
|---|---|---|---|
| Erensu | User "SuJingLan", location "WHU,China"; carvig and ignav READMEs name no lab ("基于RTKLIB开发的INS/GNSS组合导航算法库") | carvig academic_lab / ignav personal_community | **carvig → personal_community**; desc_zh "武大相关：…" → "WHU 个人开发者基于 RTKLIB 扩展的 C 语言 INS/GNSS/视觉车载组合导航" |
| perrysou | User Yang Su (company field = IIT space-weather page); saga-utils README names no lab | saga-utils academic_lab / SoftGNSS-python personal_community | **saga-utils → personal_community** (the text already says it is IIT graduate-student code) |
| pjalesSSTL | User "Philip Jales SSTL", company Surrey Satellite Technology Ltd.; both repos say "Provided by Surrey Satellite Technology Ltd." (a company, not a university) | GNSSR_MERRByS_Python academic_lab / GNSSRMERRByS personal_community | **GNSSR_MERRByS_Python → personal_community** (categories.md: company releases = 个人社区) |
| novatel | Organization "Hexagon \| NovAtel®", blog novatel.com; both entries' text already say NovAtel official | novatel_oem7_driver personal_community / novatel_edie official | **novatel_oem7_driver → official** (matches novatel_edie and the vendor-org convention: septentrio-gnss, u-blox, trimble-oss = official) |

Borderline (reported, not changed):
- Vendor orgs are not labelled the same way: swift-nav (6 entries), sparkfun (2) and PointOneNav/polaris are personal_community, while septentrio-gnss, u-blox, trimble-oss and novatel are official. categories.md says company releases count as 个人社区. One policy call is needed, then a bulk fix.
- geode (demiangomez): OSU faculty, but README says "developed by Demian Gomez and contributors" → kept academic_lab.
- B2bLIB (GCCLib, PI Zhetao Zhang): ResearchGate says Tongji, Google Scholar says Hohai → kept "同济相关".

## Task 2 — fact audit idx 0–400 (53 entries)
Sample: all 276 GitHub entries in idx 0–400 were checked with GraphQL for archived/fork/licence/language/rename. Then 42 random entries (seed 44) plus 11 flagged ones were read against GitHub description/README.

Fixes:
- **gnss-sdr-1pps** (oscimp): README says the main purpose is **two-antenna direction-of-arrival spoofing detection plus jamming detection and cancellation** (B210/XTRX, λ/2 spacing), with 1-PPS output added. It is a set of patches against gnss-sdr v0.0.18/v0.0.20. The old text only described it as a 1-PPS add-on. desc_zh, one_liner_zh and analysis_zh were rewritten; language `""` → `C++` (patches to C++ source).
- **LEOGPS**: desc said "斯坦福相关", but the README only names author Samuel Y. W. Low, not a lab → desc rewritten, provenance academic_lab → personal_community. analysis_zh now adds the README scope: GPS L1/L2 only, RINEX 2.xx, CODE EPH/CLK, GPS time output.
- Individual accounts wrongly marked academic_lab (the README names no lab) → personal_community: **HPRTK** (yxw027, anonymous user, README is 2 lines), **MobileGNSS-SPP** (salmoshu, engineer's RTKLIB-based smartphone SPP), **cssrlib** (hirokawa, Rui Hirokawa, engineer), **COSMIC-IONPRF-Ne-TEC** (HassanNooreldeen, individual researcher).
- **cssrlib** language `Jupyter Notebook` → `Python` (pip package; notebooks are tutorials).
- Archived repos (GraphQL `isArchived`) whose text did not say so. A dated "仓库已于 YYYY-MM 归档（只读）" note was added:
  - baidu-ntripcaster (2019-05)
  - gps-sdr-sim (2025-01)
  - IonoTomo (2020-11)
  - iri90 (2022-08)
  - ionex-analyzer (2023-04; replaces "维护不确定")
  - **GPSPACE**: analysis rewritten from the README: CGS operational use from the 1990s to 2018-08, CSRS-PPP backend from 2003, then replaced; support ceased; released under MIT as an archived repo.
- GPSTk and BeagleSDRGPS already say they are archived.

Checked OK (no change): caster, geode, gLAB mirror, gnss-downloader, gnsspy, gnsstk, gnsstools, gps-measurement-tools, ntripstreams, septentrio_gnss_driver, B2bLIB, gnatss, gnss-rtk (AGPL-3.0 confirmed), gnssgo, goGPS_Java, GREAT-PVT, groops, PPPH-UAV (Hacettepe assoc. prof., GPS Solut paper), rtklib-py, RTKNAVI-BH, FlyDog-SDR-GPS, galileo-sdr-sim, gnss-baseband, gnss-sdr-monitor, GNSS-SDRLIB, GNSS-VHDL (README: developed for UPC RSLab), GPSGALSSS, oresat hardware, apexpy, BiScEF, Geometric-Matrix…, geospacelab, gnss-scintillation-simulator, Ionospheric-VTEC-Forecasting, IPE, ismr_downloader, Kamodo-core (LICENSE = NOSA 1.3), hfpytrace (GitHub bytes MATLAB-heavy from bundled pharlap_lib; package is Python), Ionort-raytrace (Fortran solver + MATLAB GUI, as the text says).
- Language-heuristic mismatches left alone: gnsstk-apps (PostScript), GAMP_PPPH (Grammatical Framework), IRI_TID (OpenEdge ABL), and notebook-heavy Python repos.
- Forks noted earlier (MALIB, RTKLIB-explorer, gps-qzss-sdr-sim) are unchanged.

## Task 3 — empty subcategory
`tools-learning / RTK网络客户端` has 0 entries. The generator (`regenerate_lists` in merge_routine_20260926c.py) builds headings only from subcategories that are present in the data; nothing is hard-coded. A pre-edit dry run produced no diff, and `rg RTK网络客户端 lists/ docs/ README.md` finds nothing. No fix was needed.

## Regeneration / validation
- Dry run of merge_routine_20260926c regenerate_lists/categories/readme before edits: no diff.
- After edits: PROJECTS.json has 26 changed lines (provenance ×10, desc ×3, analysis ×9, language ×2, one_liner ×1, provenance_counts). Regenerated lists 01/02/03/04/06/07 (badge/one-liner/analysis rows only) and the README provenance counts line. categories.md is unchanged.
- JSON valid. project_count 1029 = len(projects) = Σcounts_by_category = Σprovenance_counts. No duplicate URLs or names.
- counts_by_category unchanged {ionosphere 298, troposphere 49, gnss-data 138, gnss-positioning 106, orbit-clock 31, navigation-ins 73, gnss-sdr 76, mobile-apps 32, tools-learning 57, gnss-datasets 169}.
- provenance 341/355/333 → **342/347/340**.

## Leftovers
- Vendor-org provenance policy (swift-nav/sparkfun/PointOneNav vs septentrio/u-blox/trimble-oss/novatel).
- More individual-account academic_lab entries probably exist outside idx 0–400; a catalog-wide users/X sweep is worth doing.
- MathWorks-ionex_reader licence; gps-qzss-sdr-sim parent; gnssFGO; ESA-UGI / IMSP-MGS / IONOLAB language `unknown` (from batches 42/43).
