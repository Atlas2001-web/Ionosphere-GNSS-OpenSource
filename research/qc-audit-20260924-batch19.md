# Catalog QC audit — 2026-09-24 batch 19

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch18 (`b954ef1`): **870** entries; `desc_zh`==`one_liner_zh` **141**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine/目录新收录 entries (routine-2026-09-24j names present); do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **141** before → **111** after |
| Empty `license` | unchanged (no invent) |
| Empty `language` | unchanged (no invent) |
| HTTP leftovers | **6** |
| `project_count` | **870** (unchanged by QC) |

### Prior QC integrity (after pull)
Sample Chinese QC (GFZRNX OL≠DZ / m_gim-PANXIONG academic_lab / libsbp personal_community / piksi_tools polish / SbfMixer official+polish) intact. Routine-2026-09-24j software names present (azarashi / QZQSM / libswiftnav / NavAI / ionFR / gps-fpga / gnsshat / ublox8-qzss-almanac-converter).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS upgrades still fail for known leftovers (http_code=000 / ERR). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

Priority HTTPS spot-checks (alive): SpatioTECformer / Swarm-VIP-Dynamic / swarm-vip-dynamic-models / geoveil-mp / NGS-NCAT / VDATUM → 200.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Provenance spot-checks (verify-only)
| Name | Detail |
|---|---|
| SoftGPS-CU-Boulder | KEEP `academic_lab` — CU Boulder RF & SatNav SoftGNSS companion |
| CCAR-GNSS-SDR-Book | KEEP `academic_lab` — CU Boulder CCAR book support |
| Swarm-VIP-Dynamic | KEEP `official` — KNMI-OSS GitLab agency OSS |
| swarm-vip-dynamic-models | KEEP `official` — KNMI-OSS libs; BSD-3 |
| NGS-ADJUST | KEEP `official` — NOAA/NGS PC_PROD freeware |
| NGS-NCAT | KEEP `official` — NOAA/NGS NCAT |
| VDATUM | KEEP `official` — NOAA VDatum |
| GFZRNX-UserGuide | KEEP `official` — GFZ gfzrnx docs |
| Anubis-Free-Download | KEEP `personal_community` — G-Nut vendor free tier (公司开源→personal_community) |
| geoveil-mp | KEEP `personal_community` — personal MIT library |
| libswiftnav | KEEP `personal_community` — swift-nav vendor OSS (same as libsbp) |
| SpatioTECformer | KEEP `personal_community` — personal research GitHub |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **0** (verify-only keeps)
- Chinese rewrites: **30** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **30**
- `project_count` unchanged by this QC: **870**
- `lists/*.md` surgically synced (01, 03, 04, 07, 08, 09); README badges already at 870

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `rewrite_zh` | SpatioTECformer | one_liner_zh, desc_zh |
| 2 | `rewrite_zh` | Swarm-VIP-Dynamic | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | swarm-vip-dynamic-models | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | synthetic_ionospheric_tomography_isl | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | vtec | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | WA_ion_model_PPP | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | geoveil-mp | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | SoftGPS-CU-Boulder | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | CCAR-GNSS-SDR-Book | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | Anubis-Free-Download | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | GFZRNX-UserGuide | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | NGS-ADJUST | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | NGS-NCAT | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | VDATUM | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | IRI2020_parameters | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | OASIS-ohm1122 | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | SAMI3-3.22-CCMC-mirror | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | azarashi | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | QZQSM | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | libswiftnav | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | NavAI | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | ionFR | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | gps-fpga | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | gnsshat | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | ublox8-qzss-almanac-converter | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | GPS-Velocity-Viewer | one_liner_zh, desc_zh |
| 27 | `rewrite_zh` | NGS-GPS-Toolbox | one_liner_zh, desc_zh |
| 28 | `rewrite_zh` | gLAB-Download | one_liner_zh, desc_zh |
| 29 | `rewrite_zh` | Caster-source-FTP | one_liner_zh, desc_zh |
| 30 | `rewrite_zh` | RNXCMP-LICENSE | one_liner_zh, desc_zh |

Chinese rewrite names: Anubis-Free-Download, CCAR-GNSS-SDR-Book, Caster-source-FTP, GFZRNX-UserGuide, GPS-Velocity-Viewer, IRI2020_parameters, NGS-ADJUST, NGS-GPS-Toolbox, NGS-NCAT, NavAI, OASIS-ohm1122, QZQSM, RNXCMP-LICENSE, SAMI3-3.22-CCMC-mirror, SoftGPS-CU-Boulder, SpatioTECformer, Swarm-VIP-Dynamic, VDATUM, WA_ion_model_PPP, azarashi, gLAB-Download, geoveil-mp, gnsshat, gps-fpga, ionFR, libswiftnav, swarm-vip-dynamic-models, synthetic_ionospheric_tomography_isl, ublox8-qzss-almanac-converter, vtec

Full machine log (gitignored-ish research): `research/_qc_touch_log_20260924_batch19.json`.
Keep audits: `research/_qc_batch19_prov_keep.json`.

## Counts after sync
- `project_count`: **870**
- `counts_by_category`: `{"ionosphere": 245, "troposphere": 40, "gnss-data": 130, "gnss-positioning": 100, "orbit-clock": 20, "navigation-ins": 64, "gnss-sdr": 66, "mobile-apps": 24, "tools-learning": 53, "gnss-datasets": 128}`
- `provenance_counts`: `{"official": 251, "academic_lab": 316, "personal_community": 303}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **111**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 20)
1. Empty licenses/languages — do not invent SPDX; only fill when high-confidence.
2. **6 HTTP URLs** — HTTPS still unreachable for known leftovers; leave HTTP.
3. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈111) — continue short human polish on remaining software; **skip portal walls** (ESA-TIO-*, DLR-IMPC*, GIRO-*, NOAA-SWPC-GloTEC*, ROB-*, Beihang, Autoscala, CCMC-*, HAO-TGCM, NICT-*, UMLCAR-Downloads, UWM-*, UNAVCO-Preprocessing, EUREF-IP-Ntrip-overview, gpsd-website, GA-Positioning-Services, gAGE-Software-Tools, NGS-PC-PROD, UNAVCO-Software-Portal, VMF-TUWien-Home, ESA-SWE-*, GFZ-Global-Ionosphere-Maps, etc.). Suggested software leftovers if still identical: mid-star ionosphere code hosts + any new routine identicals.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
