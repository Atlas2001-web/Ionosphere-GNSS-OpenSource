# QC audit — 2026-09-26 batch 52 (ionosphere-product portals, overlapping subcategories)

Base: `45549b4` (batch 51 end; `origin/main` had no newer commits at start). Project total 1029 unchanged; provenance 331/214/484 unchanged; no entries added or removed; only `category`, `subcategory` and `counts_by_category` changed in PROJECTS.json.

## Task 0 — entries newer than 45549b4

None. No commits after 45549b4 at start; nothing to QC.

## Task 1 — ionosphere-product portals → gnss-datasets

Policy (decided for this batch, consistent with batch 51's space-weather move): data/product download portals and product web pages go to gnss-datasets; software/code stays in ionosphere. TEC/GIM/IONEX/scintillation/ionosonde products → `gnss-datasets/电离层产品` (siblings CDDIS-IONEX, JPL-IONEX-Rapid, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG). Multi-domain space-weather hubs → `gnss-datasets/地磁空间天气` (siblings NOAA-SWPC, CCMC-DONKI, CCMC-ISWA).

**Kept in ionosphere (online model/tool or software pages, sibling consistency):**

- CCMC-IRI-online (ionosphere/IRI模型): online IRI model runner; siblings are the irimodel.org IRI packages.
- CCMC-SAMI3 (ionosphere/模型): CCMC model page with runs-on-request; siblings SAMI3-3.22-Zenodo, SAMI3 mirror.
- HAO-TGCM-portal (ionosphere/模型): TGCM/TIE-GCM model software docs/releases.
- IRI-COMMON-FILES, IRI-indices (ionosphere/IRI模型): input files required by the IRI Fortran packages, part of the model distribution.
- GAMBIT-Database-Reader-Java, IRTAM-Coefficient-Reader-Fortran (ionosphere/IRI模型): reader code (zip), not portals.
- UMLCAR-Downloads, SAO-Explorer, Drift-X, NHPC-TrueHeight, CARP-Average-Profile, Autoscala-INGV: ionosonde software download pages → ionosphere/测高仪 (Task 2).
- IMSP-MGS, ESA-UGI, IONOLAB-TEC-Software, Heki-GNSS-TEC-Software, PHaRLAP, ITU-R-iono-tropo-software, IRI-Plas-SPIM-IZMIRAN: software distributed via official sites.
- Boston-College-ISR-Ionospheric-Studies: research-group intro page, neither product page nor software; left in ionosphere/工具 (leftover, see below).
- IRTS_SDK: SDK code; it was the only software in ionosphere/电离层产品, moved to ionosphere/数据接口 next to madrigalWeb/viresclient.

## Task 2 — overlapping subcategories

- ionosphere `电离层工具` (19) merged into dominant `工具`; entries that clearly fit something more specific were redistributed first. Two new ionosphere subcategories were created, each with ≥3 entries (the generator groups by free-text subcategory, so no code change): `测高仪` (13: ionosonde/topside-sounder software) and `TID` (4: DARNtids, lstid_processing, hamsci_LSTID_detection, psws-drf-tid-tools). Ionort-raytrace and Raytrace-Model → HF射线追踪; Ionosonde-Data-Downloader → 数据接口; swarm-vip-dynamic-models → 模型. After Task 1, ionosphere/电离层工具 lost NICT-Ionosonde-Data to gnss-datasets. ionosphere/工具: 45 → 42.
- NSTB-WAAS-Test-Team: gnss-datasets has no SBAS subcategory. Moved to the existing tools-learning/SBAS next to FAA-WAAS and ESSP-EGNOS-User-Support.
- gnss-positioning: `RTK/PPP` (RTKLIB, RTKLIB-explorer) and `PPP/RTK` (gnss-rtk, laika) → dominant `SPP/RTK/PPP` (8 → 12); `PPP-AR` (PRIDE-PPPAR, PPP_AR) → `PPP/PPP-AR` (5 → 7). `PPP/PPP-RTK` vs `PPP-RTK/HAS` are different scopes (CLAS/CSSR vs Galileo HAS), so both kept.
- CSNO-TARC and CSNO-TARC-Differential: this is the BDS test/assessment centre (performance monitoring, differential info), not a bias product. Both moved from gnss-datasets/偏差产品 to gnss-datasets/轨道钟差, where the other system-operator portals sit (GLONASS-IAC, QZSS-Official, QZSS-Public-Archives).

## Task 3 — docs/categories.md

docs/categories.md lists no subcategories. It holds only category blurbs and counts, and `regenerate_categories` rewrites it. No subcategory edit was needed; only the regenerated counts changed.

## All moves (68; 27 cross-category, 41 subcategory-only)

| idx | name | from | to | reason |
|---:|---|---|---|---|
| 103 | CSNO-TARC | gnss-datasets/偏差产品 | gnss-datasets/轨道钟差 | T2: BDS system test/assessment (monitoring) portal, not a bias product; siblings GLONASS-IAC, QZSS-Official, QZSS-Public-Archives |
| 104 | CSNO-TARC-Differential | gnss-datasets/偏差产品 | gnss-datasets/轨道钟差 | T2: BDS system test/assessment (monitoring) portal, not a bias product; siblings GLONASS-IAC, QZSS-Official, QZSS-Public-Archives |
| 163 | gnss-rtk | gnss-positioning/PPP/RTK | gnss-positioning/SPP/RTK/PPP | T2: RTK/PPP synonym merged into dominant multi-mode name |
| 181 | laika | gnss-positioning/PPP/RTK | gnss-positioning/SPP/RTK/PPP | T2: RTK/PPP synonym merged into dominant multi-mode name |
| 198 | PPP_AR | gnss-positioning/PPP-AR | gnss-positioning/PPP/PPP-AR | T2: PPP-AR synonym merged into PPP/PPP-AR |
| 202 | PRIDE-PPPAR | gnss-positioning/PPP-AR | gnss-positioning/PPP/PPP-AR | T2: PPP-AR synonym merged into PPP/PPP-AR |
| 212 | RTKLIB | gnss-positioning/RTK/PPP | gnss-positioning/SPP/RTK/PPP | T2: RTK/PPP synonym merged into dominant multi-mode name |
| 214 | RTKLIB-explorer | gnss-positioning/RTK/PPP | gnss-positioning/SPP/RTK/PPP | T2: RTK/PPP synonym merged into dominant multi-mode name |
| 283 | Alouette_ISIS_extract | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 286 | Autoscala-INGV | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 287 | Beihang-Ionosphere-CN | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 289 | Boston-College-ISR-Ionospheric-Studies | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 290 | CARP-Average-Profile | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 298 | DLR-IMPC | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 299 | DLR-IMPC-Products | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 300 | Drift-X | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 304 | ESA-IONMON | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 305 | ESA-SWE-Registration | ionosphere/电离层产品 | gnss-datasets/地磁空间天气 | T1: multi-domain space-weather hub; siblings NOAA-SWPC, CCMC-DONKI, CCMC-ISWA in gnss-datasets/地磁空间天气 |
| 306 | ESA-SWE-SSA | ionosphere/电离层产品 | gnss-datasets/地磁空间天气 | T1: multi-domain space-weather hub; siblings NOAA-SWPC, CCMC-DONKI, CCMC-ISWA in gnss-datasets/地磁空间天气 |
| 307 | ESA-TIO-Forecast-TEC | ionosphere/TEC预报 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 308 | ESA-TIO-NRT-TEC | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 309 | ESA-TIO-Services | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 321 | GFZ-Global-Ionosphere-Maps | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 323 | GIRO-GAMBIT | ionosphere/IRI模型 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 324 | GIRO-IRTAM | ionosphere/IRI模型 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 325 | GIRO-portal | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 337 | HamSCI-ionosonde | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 342 | IMSP-MGS | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 353 | IonKit-NH | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 361 | Ionort-raytrace | ionosphere/工具 | ionosphere/HF射线追踪 | T2: HF ray-tracing code; siblings PHaRLAP, PyLap, PyRayHF |
| 362 | Ionosonde-Data-Downloader | ionosphere/工具 | ionosphere/数据接口 | T2: data downloader; siblings digisondeindices, ismr_downloader |
| 363 | ionosonde_volgatech | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 364 | ionosphere-plotting | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 374 | IonTools | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 394 | IRTS_SDK | ionosphere/电离层产品 | ionosphere/数据接口 | T1: SDK (software) left alone in ionosphere/电离层产品 after portals moved; client for ionosphere.cn service like madrigalWeb/viresclient |
| 397 | jvierine-ionosonde | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 420 | NHPC-TrueHeight | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 421 | NICT-Ionosonde-Data | ionosphere/电离层工具 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 422 | NICT-WDC-Ionosphere-SpaceWeather | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 423 | nleht-fdtd-ionosphere | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 424 | NOAA-NCEI-TEC-Archive | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 425 | NOAA-SWPC-GloTEC | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 426 | NOAA-SWPC-GloTEC-Data | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 433 | POLAN | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 443 | pynasonde | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 444 | pypride | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 453 | Raytrace-Model | ionosphere/工具 | ionosphere/HF射线追踪 | T2: HF ray-tracing code; siblings PHaRLAP, PyLap, PyRayHF |
| 456 | ROB-European-TEC | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 457 | ROB-IONEX-Products | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 468 | SAO-Explorer | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 482 | swarm-vip-dynamic-models | ionosphere/电离层工具 | ionosphere/模型 | T2: empirical in-situ climatology model |
| 497 | UMLCAR-Downloads | ionosphere/电离层工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 498 | UWM-CDRSK-IGS-Validation | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 499 | UWM-IGS-Iono-Combination | ionosphere/IONEX/TEC图 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 673 | DARNtids | ionosphere/工具 | ionosphere/TID | T2: TID detection tools (4 entries, new subcat ≥3) |
| 712 | GRITI | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 713 | spinifex | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 735 | RMextract | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 794 | NSTB-WAAS-Test-Team | gnss-datasets/空间天气辅助 | tools-learning/SBAS | T2: WAAS test-team portal; siblings FAA-WAAS, ESSP-EGNOS-User-Support in tools-learning/SBAS (no SBAS subcat in gnss-datasets) |
| 854 | ionFR | ionosphere/电离层工具 | ionosphere/工具 | T2: 电离层工具 merged into dominant 工具 |
| 871 | SWS-BOM-Satellite | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 877 | CCMC-Home | ionosphere/模型 | gnss-datasets/地磁空间天气 | T1: multi-domain space-weather hub; siblings NOAA-SWPC, CCMC-DONKI, CCMC-ISWA in gnss-datasets/地磁空间天气 |
| 884 | SWS-HF-Systems | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 887 | SWPC-D-RAP | ionosphere/电离层产品 | gnss-datasets/电离层产品 | T1: ionosphere data/product portal; siblings CDDIS-IONEX, GIRO-DIDBase, WHU-IGS-Ionosphere-AC, IGS-Ionosphere-WG in gnss-datasets/电离层产品 |
| 979 | AlouetteApp | ionosphere/工具 | ionosphere/测高仪 | T2: ionosonde/topside-sounder processing or hardware software (13 entries, new subcat ≥3) |
| 987 | lstid_processing | ionosphere/工具 | ionosphere/TID | T2: TID detection tools (4 entries, new subcat ≥3) |
| 988 | hamsci_LSTID_detection | ionosphere/工具 | ionosphere/TID | T2: TID detection tools (4 entries, new subcat ≥3) |
| 989 | psws-drf-tid-tools | ionosphere/工具 | ionosphere/TID | T2: TID detection tools (4 entries, new subcat ≥3) |

## Counts

| category | before | after |
|---|---:|---:|
| gnss-data | 137 | 137 |
| gnss-positioning | 108 | 108 |
| navigation-ins | 72 | 72 |
| ionosphere | 273 | 247 |
| tools-learning | 57 | 58 |
| gnss-datasets | 195 | 220 |
| troposphere | 48 | 48 |
| gnss-sdr | 76 | 76 |
| mobile-apps | 32 | 32 |
| orbit-clock | 31 | 31 |
| **total** | 1029 | 1029 |

(category, subcategory) groups 178 → 175; one-entry groups 46 → 46.

## Regeneration and checks

- A dry run of `merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme` on the untouched data gave a zero diff. The same functions were run after the edits.
- PROJECTS.json is valid JSON in the canonical dump format. The diff touches only `category` (27), `subcategory` (57) and `counts_by_category` (3 values).
- All 10 list files have header count equal to row count, and every URL appears exactly once across the lists (1029 rows, same set as PROJECTS.json). README badges/table and docs/categories.md counts match. project_count is 1029. Provenance is 331/214/484.

## Leftovers

- Remaining near-duplicate ionosphere subcategory pairs, not in scope this batch: GIM vs GIM/球谐映射, 闪烁 vs 闪烁/ROTI, TEC预报 vs TEC预报/ML, IRI/NeQuick vs IRI模型.
- ionosphere/工具 (42) still mixes generic space-physics libraries: pysat family, SuperDARN/ISR tools (pyDARN, RST, Lompe, LPI, BAFIM, isr-raw, resolvedvelocities), and Faraday-rotation tools (spinifex, RMextract, ionFR). A `雷达/ISR` subcategory (≥3) is a possible future split.
- Boston-College-ISR-Ionospheric-Studies is a research-group page with no obvious home.
- gnss-datasets/空间天气辅助 (6) and 地磁空间天气 overlap in scope (SuperDARN, Madrigal, Meridian, PITHIA vs space-weather hubs).
- 46 singleton groups remain (unchanged).
