# Catalog QC audit — 2026-09-24 batch 18

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24j (`dac5829`) + docs commits: **870** entries; `desc_zh`==`one_liner_zh` **176**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only (Septentrio official vs Swift personal_community); HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine/目录新收录 entries (routine-2026-09-24j fourteen names present); do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **176** before → **141** after |
| Empty `license` | ~169+ (unchanged; no invent) |
| Empty `language` | ~34+ (unchanged; no invent) |
| HTTP leftovers | **6** |
| `project_count` | **870** (unchanged by QC) |

### Prior QC integrity (after pull)
Sample Chinese QC (GFZRNX OL≠DZ / m_gim-PANXIONG academic_lab / libsbp personal_community / piksi_tools polish) intact. Septentrio `SbfMixer` remains `official`. Routine-2026-09-24j fourteen names all present (azarashi / QZQSM / libswiftnav / NavAI / ionFR / gps-fpga / gnsshat / ublox8-qzss-almanac-converter / …).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS upgrades still fail for known leftovers (http_code=000 / ERR). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Provenance spot-checks (verify-only)
| Name | Detail |
|---|---|
| SbfMixer | KEEP `official` — github.com/septentrio-gnss/SbfMixer — owner type Organization (Septentrio manufacturer); consistent with sibling Septentrio entries |
| libsbp | KEEP `personal_community` — swift-nav vendor OSS; categories.md maps 公司开源 → personal_community (batch17) |
| piksi_tools | KEEP `personal_community` — swift-nav vendor; same policy as libsbp / swift-nav-pygnss / pynex |
| swift-nav-pygnss | KEEP `personal_community` — swift-nav vendor; no flip |
| pynex | KEEP `personal_community` — swift-nav archived tooling; personal_community |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **0** (verify-only keeps; Septentrio=official vs Swift=personal_community consistent)
- Chinese rewrites: **35** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **35**
- `project_count` unchanged by this QC: **870**
- `lists/*.md` surgically synced (01, 08); README badges already at 870

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `rewrite_zh` | SbfMixer | one_liner_zh, desc_zh |
| 2 | `rewrite_zh` | igs-roti | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | GNSSClock | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | ESA-UGI | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | IMSP-MGS | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | IONOLAB-TEC-Software | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | IRI-2001-package | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | IRI-2007-package | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | IRI-2012-package | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | IRI-2016-package | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | IRI-2020-package | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | IRI-Plas-SPIM-IZMIRAN | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | ionex-downloader | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | IonKit-NH-tanggdut | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | ionospheric-tec-forecasting-IISC | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | Ionospheric-TEC-Kriging-Turkiye | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | IRTS_SDK | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | Klobuchar-study-code | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | KOH2-ionosphere | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | M_ISSION | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | MathWorks-ionex_reader | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | NeQuick2-MLF2 | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | NeQuickG-ESSR | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | NHPC-TrueHeight | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | Okoh-MATLAB-ROT-ROTI | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | Okoh-MATLAB-TEC-from-RINEX | one_liner_zh, desc_zh |
| 27 | `rewrite_zh` | PHaRLAP | one_liner_zh, desc_zh |
| 28 | `rewrite_zh` | PMGC-SimVP | one_liner_zh, desc_zh |
| 29 | `rewrite_zh` | pyFIRI2018 | one_liner_zh, desc_zh |
| 30 | `rewrite_zh` | quakeion | one_liner_zh, desc_zh |
| 31 | `rewrite_zh` | RIM | one_liner_zh, desc_zh |
| 32 | `rewrite_zh` | ROM-SAF-ROPP | one_liner_zh, desc_zh |
| 33 | `rewrite_zh` | SAMI3-3.22-Zenodo | one_liner_zh, desc_zh |
| 34 | `rewrite_zh` | ScintPi-1.0-Software | one_liner_zh, desc_zh |
| 35 | `rewrite_zh` | SegmentsComputation | one_liner_zh, desc_zh |

Chinese rewrite names: ESA-UGI, GNSSClock, IMSP-MGS, IONOLAB-TEC-Software, IRI-2001-package, IRI-2007-package, IRI-2012-package, IRI-2016-package, IRI-2020-package, IRI-Plas-SPIM-IZMIRAN, IRTS_SDK, IonKit-NH-tanggdut, Ionospheric-TEC-Kriging-Turkiye, KOH2-ionosphere, Klobuchar-study-code, M_ISSION, MathWorks-ionex_reader, NHPC-TrueHeight, NeQuick2-MLF2, NeQuickG-ESSR, Okoh-MATLAB-ROT-ROTI, Okoh-MATLAB-TEC-from-RINEX, PHaRLAP, PMGC-SimVP, RIM, ROM-SAF-ROPP, SAMI3-3.22-Zenodo, SbfMixer, ScintPi-1.0-Software, SegmentsComputation, igs-roti, ionex-downloader, ionospheric-tec-forecasting-IISC, pyFIRI2018, quakeion

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch18.json`.
Keep audits: `research/_qc_batch18_prov_keep.json`.

## Counts after sync
- `project_count`: **870**
- `counts_by_category`: `{"ionosphere": 245, "troposphere": 40, "gnss-data": 130, "gnss-positioning": 100, "orbit-clock": 20, "navigation-ins": 64, "gnss-sdr": 66, "mobile-apps": 24, "tools-learning": 53, "gnss-datasets": 128}`
- `provenance_counts`: `{"official": 251, "academic_lab": 316, "personal_community": 303}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **141**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 19)
1. Empty licenses/languages — do not invent SPDX; only fill when high-confidence.
2. **6 HTTP URLs** — HTTPS still unreachable for known leftovers; leave HTTP.
3. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈141) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: SpatioTECformer / Swarm-VIP-Dynamic / swarm-vip-dynamic-models / synthetic_ionospheric_tomography_isl / vtec / WA_ion_model_PPP / geoveil-mp / SoftGPS-CU-Boulder / CCAR-GNSS-SDR-Book / Anubis-Free-Download / GFZRNX-UserGuide / NGS-ADJUST / NGS-NCAT / VDATUM / mid-star identical under ionosphere & gnss-datasets portals.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.

