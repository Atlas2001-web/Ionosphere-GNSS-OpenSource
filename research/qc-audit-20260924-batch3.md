# Catalog QC audit — 2026-09-24 batch 3

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 2 (`45a4e54`): **733** entries
- Goal: QC only (no new projects) — short/weak Chinese blurbs, markers, provenance, URL residuals

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty `desc_zh` / `one_liner_zh` / `analysis_zh` | **0** |
| Very short `analysis_zh` (<55 chars) | **9** (thin polish candidates) |
| `desc_zh` == `one_liner_zh` | **621** (mostly portals; polish only when misleading/thin) |
| Repeated boilerplate sentence in `analysis_zh` | **11** (`使用前请核验上游页面与许可条款。` ×3) |
| Empty `markers` | **340** (batch tags optional; do not invent) |
| `featured=true` but missing `core` marker | **3** (+ SH-GIM owned special) |
| Invalid provenance enum | **0** |
| `personal_community` with Lab/Univ-ish login (spot-check) | **25** heuristic hits; **3** verified mis-tags |
| Exact / soft same-URL residuals | **0** |
| HTTP (non-HTTPS) leftovers | **6** (HTTPS still unreachable) |

### Provenance spot-checks (gh api)
| Name | Owner | Verdict |
|---|---|---|
| INSTINCT | UniStuttgart-INS (University of Stuttgart – Institute of Navigation) | **personal→academic_lab** |
| Ionospheric-VTEC-Forecasting | ICCT-ML-in-geodesy (IAG ICCT JSG T.29 / ETH IGP) | **personal→academic_lab** |
| groops | groops-devs (ITSG / TU Graz; ftp.tugraz.at) | **personal→academic_lab** |
| pygnsslab / greenforge-labs / DiffIonMap / etc. | community or personal | keep `personal_community` |

## This batch — summary
- Boilerplate dedupe (`analysis_zh`): **11**
- Provenance fixes: **3**
- Marker fills (`featured`→`core`): **3**
- Chinese rewrites (`desc_zh` / `one_liner_zh` / `analysis_zh`): **24** entries (overlap with provenance)
- URL / HTTPS changes: **0** (no duplicates; HTTPS probe still fails)
- Entries touched (unique names): **38**
- `project_count` unchanged: **733**
- `lists/*.md` surgically synced for touched entries: 01, 03–09 (ISMR-Query-Tool marker-only: list already showed 核心 via featured; `10-gnss-datasets.md` unchanged)

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `dedupe_zh` | BNC-source-FTP | analysis_zh; collapse repeated 使用前请核验… |
| 2 | `dedupe_zh` | gpsd-website | analysis_zh; collapse repeated 使用前请核验… |
| 3 | `dedupe_zh` | plot-Anubis | analysis_zh; collapse repeated 使用前请核验… |
| 4 | `dedupe_zh` | ITU-R-iono-tropo-software | analysis_zh; collapse repeated 使用前请核验… |
| 5 | `dedupe_zh` | GFZ-SPOCC-news | analysis_zh; collapse repeated 使用前请核验… |
| 6 | `dedupe_zh` | IGSMAIL-SPOCC | analysis_zh; collapse repeated 使用前请核验… |
| 7 | `dedupe_zh` | GA-Positioning-Services | analysis_zh; collapse repeated 使用前请核验… |
| 8 | `dedupe_zh` | gAGE-Software-Tools | analysis_zh; collapse repeated 使用前请核验… |
| 9 | `dedupe_zh` | GPS-Velocity-Viewer | analysis_zh; collapse repeated 使用前请核验… |
| 10 | `dedupe_zh` | NGS-PC-PROD | analysis_zh; collapse repeated 使用前请核验… |
| 11 | `dedupe_zh` | VDATUM | analysis_zh; collapse repeated 使用前请核验… |
| 12 | `provenance` | INSTINCT | provenance; personal_community→academic_lab; UniStuttgart-INS = University of Stuttgart Institute of Navigation (org blog ins.uni-stuttgart.de) |
| 13 | `provenance` | Ionospheric-VTEC-Forecasting | provenance; personal_community→academic_lab; ICCT-ML-in-geodesy = IAG ICCT Joint Study Group T.29 (space.igp.ethz.ch) |
| 14 | `provenance` | groops | provenance; personal_community→academic_lab; GROOPS / ITSG TU Graz (ftp.tugraz.at/pub/ITSG/groops; Mayer-Guerr et al. 2021) |
| 15 | `marker_fill` | cddis-highrate-downloader | markers; featured=true → add core |
| 16 | `marker_fill` | libsbp | markers; featured=true → add core |
| 17 | `marker_fill` | ISMR-Query-Tool | markers; featured=true → add core |
| 18 | `rewrite_zh` | INSTINCT | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 19 | `rewrite_zh` | esp32-gps | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 20 | `rewrite_zh` | HASlibTestSuite | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 21 | `rewrite_zh` | multi-sdr-gps-sim | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 22 | `rewrite_zh` | GINav | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 23 | `rewrite_zh` | GNSS-matlab | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 24 | `rewrite_zh` | LEOGPS | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 25 | `rewrite_zh` | Ionosonde-Data-Downloader | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 26 | `rewrite_zh` | Full_Stack_GPS_Receiver | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 27 | `rewrite_zh` | TEC-forecast-F107 | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 28 | `rewrite_zh` | SignalSim | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 29 | `rewrite_zh` | Raytrace-Model | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 30 | `rewrite_zh` | cggtts | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 31 | `rewrite_zh` | GNSS_Compare | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 32 | `rewrite_zh` | gnsstools | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 33 | `rewrite_zh` | DiffIonMap | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 34 | `rewrite_zh` | geode | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 35 | `rewrite_zh` | gps-tec-cnn-lstm-attention | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 36 | `rewrite_zh` | gnssutils | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 37 | `rewrite_zh` | gnss-downloader | one_liner_zh, analysis_zh; short human Chinese QC |
| 38 | `rewrite_zh` | groops | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 39 | `rewrite_zh` | Ionospheric-VTEC-Forecasting | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 40 | `rewrite_zh` | pyins | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 41 | `rewrite_zh` | UrbanNavDataset | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |

## Counts after sync
- `project_count`: **733**
- `counts_by_category`: `{"ionosphere": 236, "troposphere": 32, "gnss-data": 111, "gnss-positioning": 82, "orbit-clock": 13, "navigation-ins": 59, "gnss-sdr": 59, "mobile-apps": 16, "tools-learning": 31, "gnss-datasets": 94}`
- `provenance_counts`: `{"official": 194, "academic_lab": 220, "personal_community": 319}`
- `updated`: **2026-09-24**
- Remaining HTTP: CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN
- Remaining empty license / language: unchanged this batch (not in scope)
- Remaining empty markers: ~337 (only fill when justified)

## Top remaining issues (batch 4)
1. **~180 empty licenses** — continue GitHub SPDX fills where `.license.spdx_id` exists; skip null/NOASSERTION.
2. **~34 empty languages** — same API; do not invent for portals/awesome-lists.
3. **6 HTTP URLs** — keep until canonical HTTPS appears.
4. **Mild Chinese sameness** (`desc_zh` == `one_liner_zh` ≈600) — polish only misleading portal one-liners.
5. **`core` vs `featured` drift** (~68 `core` without `featured`) — decide policy before bulk flip.
6. More provenance spot-audits (ION Metadata WG, company orgs labeled Lab, etc.) — verify only.
