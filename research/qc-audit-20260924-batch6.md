# Catalog QC audit — 2026-09-24 batch 6

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 5 + routine commit (+13): **760** entries
- Goal: QC only (no new projects) — SPDX fills, provenance verification, Chinese blurbs, HTTPS probe
- Prefer dedicated catalog-only commit so parallel docs agents do not bury attribution

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **~568** before → **540** after |
| Empty `license` | **169** (≈156 GitHub) |
| Empty `language` | **34** (API null / quirky primaries) |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### Language scan (gh api `.language`)
Remaining empties are API `null` or quirky primaries (PostScript / Grammatical Framework / Roff / HTML / OpenEdge ABL / Starlark). **No fills.**

### SPDX scan (gh api `.license.spdx_id`, skip null/NOASSERTION)
Full scan of **156** empty-license GitHub repos: **0** new SPDX hits (all null/NOASSERTION). Non-GitHub empty licenses left untouched (no high-confidence SPDX page reads this batch).

### Provenance spot-checks (gh api `users/{owner}`)
| Name | Detail |
|---|---|
| libRSF | personal_community→academic_lab; TUC-ProAut / TU Chemnitz ProAut |
| Multi_Sensor_Fusion | personal_community→academic_lab; 2013fangwentao / WHU GNSS Research Center |
| gici-open | personal_community→academic_lab; chichengcn / Shanghai Jiao Tong University |
| GLIO | personal_community→academic_lab; XikunLiu-huskit / PolyU IPNL |
| NaveGo | personal_community→academic_lab; rodralez / National University of Technology (adjunct prof) |
| Loose-GNSS-IMU | personal_community→academic_lab; aaronboda24 / York University |
| raw-gnss-fusion | personal_community→academic_lab; JonasBchrt / UKCEH & Cardiff University |
| POSGO | personal_community→academic_lab; lizhengnss / WHU GNSS Research Center |
| SoftGNSS | personal_community→academic_lab; TMBOC / SJTU School of Aeronautics & Astronautics |
| GPSMilemeterIMUEKFLocation | personal_community→academic_lab; gilbertz / Shanghai Jiao Tong University |
| LEOGPS | personal_community→academic_lab; sammmlow / Stanford University |
| FE-GUT | personal_community→academic_lab; zhaoqj23 / Tsinghua University |
| BDS-3-B1C-B2a-SDR-receiver | personal_community→academic_lab; lyf8118 / BISTU School of Automation |
| geode | personal_community→academic_lab; demiangomez / OSU Division of Geodetic Science |
| gps | personal_community→academic_lab; psas / Portland State Aerospace Society |
| GPSPACE | personal_community→official; CGS-GIS / Natural Resources Canada (NRCan) Canadian Geodetic Survey |
| IndirectEKFIMUGPS | personal_community→academic_lab; hgpvision / Harbin Institute of Technology |
| imugpslocalization | personal_community→academic_lab; ydsf16 / BUAA affiliation |
| eagleye | KEEP — MapIV org — company OSS bucket, keep personal_community |
| gnss-ins-sim | KEEP — Aceinna org — company OSS bucket, keep personal_community |
| PyGPSClient | KEEP — semuconsulting org — consulting, keep personal_community |
| pyubx2 | KEEP — semuconsulting — keep personal_community |
| pygnssutils | KEEP — semuconsulting — keep personal_community |
| RTKLIB | KEEP — tomojitakasu personal — leave personal_community |
| PocketSDR | KEEP — tomojitakasu personal — leave personal_community |
| GPSTest | KEEP — barbeau personal — leave personal_community |
| ahrs | KEEP — Mayitzin personal — leave personal_community |
| pynmea2 | KEEP — Knio personal — leave personal_community |
| ignav | KEEP — Erensu loc=WHU only (weak) — leave personal_community |
| AgOpenNtripCaster | KEEP — already audited batch5 — keep personal_community |

## This batch — summary
- License fills via `gh api` `.license.spdx_id`: **0**
- Language fills: **0**
- Provenance fixes: **18** (17→academic_lab, 1→official); **12** spot-audits kept
- Chinese rewrites: **32** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0** (no bulk policy)
- HTTPS upgrades: **0**
- Entries touched (unique names): **33**
- `project_count` unchanged: **760**
- `lists/*.md` surgically synced (03–04, 06–08); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | libRSF | personal_community→academic_lab; TUC-ProAut / TU Chemnitz ProAut |
| 2 | `provenance` | Multi_Sensor_Fusion | personal_community→academic_lab; 2013fangwentao / WHU GNSS Research Center |
| 3 | `provenance` | gici-open | personal_community→academic_lab; chichengcn / Shanghai Jiao Tong University |
| 4 | `provenance` | GLIO | personal_community→academic_lab; XikunLiu-huskit / PolyU IPNL |
| 5 | `provenance` | NaveGo | personal_community→academic_lab; rodralez / National University of Technology (adjunct prof) |
| 6 | `provenance` | Loose-GNSS-IMU | personal_community→academic_lab; aaronboda24 / York University |
| 7 | `provenance` | raw-gnss-fusion | personal_community→academic_lab; JonasBchrt / UKCEH & Cardiff University |
| 8 | `provenance` | POSGO | personal_community→academic_lab; lizhengnss / WHU GNSS Research Center |
| 9 | `provenance` | SoftGNSS | personal_community→academic_lab; TMBOC / SJTU School of Aeronautics & Astronautics |
| 10 | `provenance` | GPSMilemeterIMUEKFLocation | personal_community→academic_lab; gilbertz / Shanghai Jiao Tong University |
| 11 | `provenance` | LEOGPS | personal_community→academic_lab; sammmlow / Stanford University |
| 12 | `provenance` | FE-GUT | personal_community→academic_lab; zhaoqj23 / Tsinghua University |
| 13 | `provenance` | BDS-3-B1C-B2a-SDR-receiver | personal_community→academic_lab; lyf8118 / BISTU School of Automation |
| 14 | `provenance` | geode | personal_community→academic_lab; demiangomez / OSU Division of Geodetic Science |
| 15 | `provenance` | gps | personal_community→academic_lab; psas / Portland State Aerospace Society |
| 16 | `provenance` | GPSPACE | personal_community→official; CGS-GIS / Natural Resources Canada (NRCan) Canadian Geodetic Survey |
| 17 | `provenance` | IndirectEKFIMUGPS | personal_community→academic_lab; hgpvision / Harbin Institute of Technology |
| 18 | `provenance` | imugpslocalization | personal_community→academic_lab; ydsf16 / BUAA affiliation |
| 19 | `rewrite_zh` | RTKLIB | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 20 | `rewrite_zh` | GPSTest | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 21 | `rewrite_zh` | imu_x_fusion | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 22 | `rewrite_zh` | RTKLIB-explorer | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 23 | `rewrite_zh` | Multi_Sensor_Fusion | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 24 | `rewrite_zh` | PyGPSClient | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 25 | `rewrite_zh` | rtkbase | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 26 | `rewrite_zh` | imugpslocalization | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 27 | `rewrite_zh` | NaveGo | desc_zh, analysis_zh; short human Chinese QC |
| 28 | `rewrite_zh` | PocketSDR | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 29 | `rewrite_zh` | ignav | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 30 | `rewrite_zh` | GLIO | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 31 | `rewrite_zh` | libRSF | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 32 | `rewrite_zh` | gici-open | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 33 | `rewrite_zh` | Loose-GNSS-IMU | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 34 | `rewrite_zh` | pyubx2 | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 35 | `rewrite_zh` | rtklib-py | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 36 | `rewrite_zh` | SoftGNSS | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 37 | `rewrite_zh` | POSGO | desc_zh, analysis_zh; short human Chinese QC |
| 38 | `rewrite_zh` | LEOGPS | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 39 | `rewrite_zh` | geode | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 40 | `rewrite_zh` | GPSPACE | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 41 | `rewrite_zh` | gps-sdr-sim | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 42 | `rewrite_zh` | FE-GUT | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 43 | `rewrite_zh` | ahrs | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 44 | `rewrite_zh` | raw-gnss-fusion | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 45 | `rewrite_zh` | BeagleSDRGPS | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 46 | `rewrite_zh` | TightlyCoupledINSGNSS | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 47 | `rewrite_zh` | IndirectEKFIMUGPS | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 48 | `rewrite_zh` | BDS-3-B1C-B2a-SDR-receiver | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 49 | `rewrite_zh` | GPSMilemeterIMUEKFLocation | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |
| 50 | `rewrite_zh` | libgnss++ | one_liner_zh, desc_zh, analysis_zh; short human Chinese QC |

Chinese rewrite names: BDS-3-B1C-B2a-SDR-receiver, BeagleSDRGPS, FE-GUT, GLIO, GPSMilemeterIMUEKFLocation, GPSPACE, GPSTest, IndirectEKFIMUGPS, LEOGPS, Loose-GNSS-IMU, Multi_Sensor_Fusion, NaveGo, POSGO, PocketSDR, PyGPSClient, RTKLIB, RTKLIB-explorer, SoftGNSS, TightlyCoupledINSGNSS, ahrs, geode, gici-open, gps-sdr-sim, ignav, imu_x_fusion, imugpslocalization, libRSF, libgnss++, pyubx2, raw-gnss-fusion, rtkbase, rtklib-py

Full machine log: `research/_qc_touch_log_20260924_batch6.json`.

## Counts after sync
- `project_count`: **760**
- `counts_by_category`: `{"gnss-data": 111, "gnss-datasets": 111, "gnss-positioning": 83, "gnss-sdr": 59, "ionosphere": 239, "mobile-apps": 19, "navigation-ins": 60, "orbit-clock": 13, "tools-learning": 31, "troposphere": 34}`
- `provenance_counts`: `{"official": 214, "academic_lab": 247, "personal_community": 299}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **540**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 7)
1. **~169 empty licenses** — almost all GitHub null/NOASSERTION; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈540) — continue short human polish on misleading software one-liners (avoid portal walls).
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge / parallel-agent overwrites of QC fields (SPDX / provenance / Chinese).
7. More professor/lab personal-account spot-audits only when org/bio is clear.

