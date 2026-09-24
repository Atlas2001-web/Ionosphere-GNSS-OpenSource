# Catalog QC audit — 2026-09-24 batch 20

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24k (`93e7920`): **884** entries; `desc_zh`==`one_liner_zh` **125** (batch19 left 111 @870; +14 routine identicals)
- Goal: QC only (no new projects) — diminishing Chinese returns; softish software/tool polish; provenance verify-only; HTTPS re-probe; rare SPDX only if gh real; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine-2026-09-24k entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **125** before → **99** after |
| Empty `license` | unchanged (no invent; gh probes returned null/NOASSERTION) |
| Empty `language` | unchanged (gh language null / weak HTML/CMake skipped) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| `project_count` | **884** (unchanged by QC) |

### Prior QC integrity (after pull)
Sample Chinese QC intact (OL≠DZ): GFZRNX, m_gim-PANXIONG, libsbp, piksi_tools, SbfMixer, SpatioTECformer, geoveil-mp, NGS-NCAT. Routine-2026-09-24j software names present (azarashi / QZQSM / libswiftnav / NavAI / ionFR / gps-fpga / gnsshat / ublox8-qzss-almanac-converter). Routine-2026-09-24k (+14) present and preserved (7 software polished; 7 portals left identical intentionally).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail (http_code=000 / ERR) while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed ~30 empty/weak-license code hosts via `gh api repos/... --jq .license.spdx_id` — all **null** or **NOASSERTION**. No SPDX fills. Empty-language repos mostly returned null language; skipped weak fills (HTML/CMake).

### Provenance spot-checks (verify-only)
| Name | Detail |
|---|---|
| novatel_oem7_driver | KEEP `personal_community` — Hexagon/NovAtel vendor OSS (同 libsbp 政策) |
| novatel_gps_driver | KEEP `personal_community` — SWRI community ROS driver |
| max2771_fx2lp | KEEP `personal_community` — personal research GitHub |
| GNSS-Correction-RTKLIB | KEEP `personal_community` — personal tutorial/scripts |
| pysatNASA | KEEP `personal_community` — pysat community org |
| swiftnav-ros2 | KEEP `personal_community` — Swift vendor ROS2 (同 libsbp) |
| gnssvod | KEEP `personal_community` — personal MIT tool |
| ginan | KEEP `official` — GeoscienceAustralia agency GitHub |
| Ginan-GA-portal | KEEP `official` — GA official program page |
| GPSPACE | KEEP `official` — NRCan/CGS-GIS agency GitHub |
| VMF-TUWien-Home | KEEP `official` — TU Wien VMF service |
| CCMC-IRI-online | KEEP `official` — NASA CCMC model page |
| NRCan-TRX | KEEP `official` — NRCan CSRS web tool |
| NGS-PC-PROD | KEEP `official` — NOAA/NGS PC_PROD |
| ITU-R-iono-tropo-software | KEEP `official` — ITU-R digital products |
| GIRO-IRTAM | KEEP `academic_lab` — UMass Lowell GIRO |
| UMLCAR-Downloads | KEEP `academic_lab` — UMLCAR lab downloads |
| gAGE-Software-Tools | KEEP `academic_lab` — UPC gAGE tools |
| Zenodo-VTEC-map-generation-SBAS | KEEP `academic_lab` — Tampere Zenodo supplement |
| goGPS_MATLAB | KEEP `academic_lab` — goGPS-Project academic suite |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **0** (verify-only keeps)
- Chinese rewrites: **26** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **26**
- `project_count` unchanged by this QC: **884**
- `lists/*.md` surgically synced (01, 02, 03, 04, 05, 06, 07, 09); README badges already at 884 from routine-k

### Chinese polish strategy (diminishing returns)
- **Primary:** 7 new routine-2026-09-24k **software** identicals (ROS drivers, SDR front-end, PPK tutorial, pysatNASA, gnssvod)
- **Secondary:** 19 softish software/tool residuals (portals that point at tools/code, not pure data walls)
- **Skipped on purpose:** pure portal walls (ESA-TIO-*, ESA-IONMON, DLR-IMPC*, ROB-*, Beihang, Autoscala left HTTP-only URL; CCMC-Home/SAMI3, HAO-TGCM, NICT-*, UWM-*, IERS-EOP-PC, LINZ-Geodetic-System, and new portals SWS-BOM-Satellite / ISGI / NASA-CDAWeb / NASA-SSCWeb / UKSSDC / SWPC-Services / CCMC-Home)

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `rewrite_zh` | novatel_oem7_driver | one_liner_zh, desc_zh |
| 2 | `rewrite_zh` | novatel_gps_driver | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | max2771_fx2lp | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | GNSS-Correction-RTKLIB | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | pysatNASA | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | swiftnav-ros2 | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | gnssvod | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | Ginan-GA-portal | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | gpsd-website | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | GFZ-SPOCC-news | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | IGSMAIL-SPOCC | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | UMLCAR-Downloads | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | NRCan-TRX | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | Zenodo-VTEC-map-generation-SBAS | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | Autoscala-INGV | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | ITU-R-iono-tropo-software | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | NGS-PC-PROD | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | gAGE-Software-Tools | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | UNAVCO-Software-Portal | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | UNAVCO-Preprocessing | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | EUREF-IP-Ntrip-overview | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | VMF-TUWien-Home | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | CCMC-IRI-online | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | GIRO-IRTAM | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | GIRO-GAMBIT | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | IRI-indices | one_liner_zh, desc_zh |

Chinese rewrite names: Autoscala-INGV, CCMC-IRI-online, EUREF-IP-Ntrip-overview, GFZ-SPOCC-news, GIRO-GAMBIT, GIRO-IRTAM, GNSS-Correction-RTKLIB, Ginan-GA-portal, IGSMAIL-SPOCC, IRI-indices, ITU-R-iono-tropo-software, NGS-PC-PROD, NRCan-TRX, UMLCAR-Downloads, UNAVCO-Preprocessing, UNAVCO-Software-Portal, VMF-TUWien-Home, Zenodo-VTEC-map-generation-SBAS, gAGE-Software-Tools, gnssvod, gpsd-website, max2771_fx2lp, novatel_gps_driver, novatel_oem7_driver, pysatNASA, swiftnav-ros2

Full machine log: `research/_qc_touch_log_20260924_batch20.json`.
Keep audits: `research/_qc_batch20_prov_keep.json`.

## Counts after sync
- `project_count`: **884**
- `counts_by_category`: `{"ionosphere": 249, "troposphere": 41, "gnss-data": 130, "gnss-positioning": 101, "orbit-clock": 20, "navigation-ins": 67, "gnss-sdr": 67, "mobile-apps": 24, "tools-learning": 55, "gnss-datasets": 130}`
- `provenance_counts`: `{"official": 258, "academic_lab": 316, "personal_community": 310}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **99**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 21) — honest diminishing returns
1. **Chinese polish mostly exhausted for software.** Remaining ~99 identicals are almost all `official_site` / `data-portal` walls (IGS/CDDIS/ESA/DLR/ROB/NOAA dataset portals + new 24k portals). Further OL≠DZ rewrites risk empty portal boilerplate — skip unless a new routine brings real software identicals.
2. Empty licenses/languages — do not invent SPDX; only fill when `gh` returns real SPDX (recent probe: all null/NOASSERTION on empty hosts).
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
