# Catalog QC audit — 2026-09-24 batch 15

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch14 race cleanup + routine-20260924h re-apply: **842** entries; `desc_zh`==`one_liner_zh` **258**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy (coordinator):** preserve freshly ingested routine/目录新收录 entries; do not strip or overwrite non-QC additions; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **258** before → **220** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |
| `project_count` | **842** (unchanged by QC) |

### Prior QC integrity (after pull)
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / rinexmod / sami3_gitm / BDS-3-PPP-B2b-DATA / gnssr4river / OASIS OL≠DZ) intact. Prior provenance upgrades through batch14 still present.

### HTTPS probe (curl -sI -L --max-time 12)
Catalog HTTP URLs answer on HTTP (`200`); matching HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| geoveil-cn0 | personal_community→academic_lab; miluta7 company National CEnter for Cartography (Bucharest public mapping agency) |
| sp3 / gnss-protos | KEEP — nav-solutions community org → keep personal_community |
| RNXQCE / BDS-3-PPP-B2b_IMU_LiDAR / Easy4PTK / Muf_Muncher / GRID / ppp_rtklib / ntcmg / rtcm2ionex / MyIonosphere_Library | KEEP — empty bio/company → keep personal_community |
| EGNOS_SDK_Core | KEEP — EPSILON Group commercial → keep personal_community |
| AETHER / COSMIC-IONPRF-Ne-TEC / t-fors / gpssnrpy / clkcomb / gnss-ppp-matlab-toolbox / TEC-MoLLM / pynasonde | KEEP — already academic_lab — confirmed (Chang'an / EgSA / INGV / Larson / ETH / Delft / Tsinghua / ERAU) |
| SAMI2 / IPE / gcmprocpy / Kamodo-core / EarthScope-gnsstools | KEEP — already official — confirmed |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **1** → academic_lab; **25** spot-audits kept/confirmed
- Chinese rewrites: **38** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **38**
- `project_count` unchanged by this QC: **842**
- `lists/*.md` surgically synced (01–07, 09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | geoveil-cn0 | personal_community→academic_lab; miluta7 @ National Center for Cartography |
| 2 | `rewrite_zh` | COSMIC-IONPRF-Ne-TEC | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | sp3 | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | t-fors | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | transcar | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | AETHER | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | BDS-3-PPP-B2b_IMU_LiDAR | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | EarthScope-gnsstools | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | Global-TEC-forecasting-DL | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | RNXQCE | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | SAMI2 | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | SAMI3-GITM-python | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | TEC_calculation_RINEX3 | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | TEC_gradient_computation | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | gcmprocpy | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | gnss-scintillation-simulator_2-param | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | gpssnrpy | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | mat_gemini | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | mosgim | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | EGNOS_SDK_Core | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | Easy4PTK | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | FIRI.jl | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | IPE | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | Muf_Muncher | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | DRCycleSlip | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | EasyGNSS | one_liner_zh, desc_zh |
| 27 | `rewrite_zh` | GRID | one_liner_zh, desc_zh |
| 28 | `rewrite_zh` | IonMap | one_liner_zh, desc_zh |
| 29 | `rewrite_zh` | pynasonde | one_liner_zh, desc_zh |
| 30 | `rewrite_zh` | gnss-ppp-matlab-toolbox | one_liner_zh, desc_zh |
| 31 | `rewrite_zh` | clkcomb | one_liner_zh, desc_zh |
| 32 | `rewrite_zh` | geoveil-cn0 | one_liner_zh, desc_zh |
| 33 | `rewrite_zh` | gnss-protos | one_liner_zh, desc_zh |
| 34 | `rewrite_zh` | IonCast-Heliolab2025 | one_liner_zh, desc_zh |
| 35 | `rewrite_zh` | Kamodo-core | one_liner_zh, desc_zh |
| 36 | `rewrite_zh` | ntcmg | one_liner_zh, desc_zh |
| 37 | `rewrite_zh` | rtcm2ionex | one_liner_zh, desc_zh |
| 38 | `rewrite_zh` | ppp_rtklib | one_liner_zh, desc_zh |
| 39 | `rewrite_zh` | TEC-MoLLM | one_liner_zh, desc_zh |

Chinese rewrite names: AETHER, BDS-3-PPP-B2b_IMU_LiDAR, COSMIC-IONPRF-Ne-TEC, DRCycleSlip, EGNOS_SDK_Core, EarthScope-gnsstools, Easy4PTK, EasyGNSS, FIRI.jl, GRID, Global-TEC-forecasting-DL, IPE, IonCast-Heliolab2025, IonMap, Kamodo-core, Muf_Muncher, RNXQCE, SAMI2, SAMI3-GITM-python, TEC-MoLLM, TEC_calculation_RINEX3, TEC_gradient_computation, clkcomb, gcmprocpy, geoveil-cn0, gnss-ppp-matlab-toolbox, gnss-protos, gnss-scintillation-simulator_2-param, gpssnrpy, mat_gemini, mosgim, ntcmg, ppp_rtklib, pynasonde, rtcm2ionex, sp3, t-fors, transcar

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch15.json`.
Keep audits: `research/_qc_batch15_prov_keep.json`.

## Counts after sync
- `project_count`: **842**
- `counts_by_category`: `{"ionosphere": 244, "troposphere": 39, "gnss-data": 126, "gnss-positioning": 97, "orbit-clock": 16, "navigation-ins": 64, "gnss-sdr": 62, "mobile-apps": 22, "tools-learning": 47, "gnss-datasets": 125}`
- `provenance_counts`: `{"official": 238, "academic_lab": 314, "personal_community": 290}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **220**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 16)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈220) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: Microsat-gps-sim / MyIonosphere_Library / NeQuickJRC / Nequick-ITUR / SubionosphericVLFInversionAlgorithms.jl / iono-tomography / ionopy / mitiono / GNSSRTK / OpATOM / UNB3m / Smart-UAV-Return-GNSS-Station / pysatCDAAC / pytiegcm / real-time-ionospheric-maps-Kalman / roti-gnss-ml / GPSMAXIM2769b- / AURORA / Ionospheric-Scintillation-Maps-and-PDOP / Ionospheric-TEC-ROTI-Interactives / swds-api-downloader / mid-star identical under ionosphere & gnss-sdr.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path; rebase-before-push; never strip fresh routine entries when resolving races.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
