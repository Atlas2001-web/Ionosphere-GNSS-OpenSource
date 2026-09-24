# Catalog QC audit — 2026-09-24 batch 4

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 3 (`62d17dc`) + later docs commits on `main`: **733** entries
- Goal: QC only (no new projects) — Chinese blurbs, provenance, GitHub SPDX fills, HTTP probe

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **~597** (mostly portals) |
| Empty `license` | **180** (≈167 GitHub) |
| Empty `language` | **34** (API null / quirky primaries) |
| Empty `markers` | **337** (do not invent) |
| `featured` missing `core` | **1** (SH-GIM `owned` special — leave) |
| Invalid provenance enum | **0** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -I -L --max-time 15)
All six HTTPS upgrades **fail** (connection / http_code=000). Leave HTTP.

### Provenance spot-checks (gh api)
| Name | Owner | Verdict |
|---|---|---|
| nmea-msgs | ros-drivers (ROS device drivers org) | **personal→official** |
| FAST | ChangChuntao (`aircas.ac.cn` / AIRCAS CAS) | **personal→academic_lab** |
| PPPH-UAV / MAPS / pygnsslab / student repos | User or community branding | keep `personal_community` |

## This batch — summary
- License fills via `gh api` `.license.spdx_id`: **9** (skip null/NOASSERTION; no quirky language fills)
- Language fills: **0** (remaining empties are API null or quirky PostScript/HTML/Roff/Starlark/Grammatical Framework/OpenEdge ABL)
- Provenance fixes: **2**
- Chinese rewrites: **22** entries
- Marker fills: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **31**
- `project_count` unchanged: **733**
- `lists/*.md` surgically synced (01–04, 06–09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `meta_fill` | GNSSClock | license; gh api repos → license='LGPL-2.1' |
| 2 | `meta_fill` | GNSSTimeServer | license; gh api repos → license='MIT' |
| 3 | `meta_fill` | IndirectEKFIMUGPS | license; gh api repos → license='MIT' |
| 4 | `meta_fill` | gnss2tws-green | license; gh api repos → license='GPL-3.0' |
| 5 | `meta_fill` | gnssIR-matlab-v3 | license; gh api repos → license='MIT' |
| 6 | `meta_fill` | gnssIR-python | license; gh api repos → license='MIT' |
| 7 | `meta_fill` | gnssr-synth | license; gh api repos → license='MIT' |
| 8 | `meta_fill` | gnssrlowcost | license; gh api repos → license='MIT' |
| 9 | `meta_fill` | gnsssdrgui | license; gh api repos → license='GPL-3.0' |
| 10 | `provenance` | nmea-msgs | provenance; personal_community→official; ros-drivers = ROS device drivers org (ros.org/wiki/sig/Drivers) |
| 11 | `provenance` | FAST | provenance; personal_community→academic_lab; ChangChuntao @ airacas.ac.cn = AIRCAS / Chinese Academy of Sciences |
| 12 | `rewrite_zh` | FGI-GSRx | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 13 | `rewrite_zh` | GDDS | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 14 | `rewrite_zh` | GraphGNSSLib | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 15 | `rewrite_zh` | KF-GINS | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 16 | `rewrite_zh` | MG_APP | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 17 | `rewrite_zh` | PPPLib | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 18 | `rewrite_zh` | ginan | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 19 | `rewrite_zh` | gps-sdr-sim | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 20 | `rewrite_zh` | eagleye | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 21 | `rewrite_zh` | gici-open | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 22 | `rewrite_zh` | gnss-ins-sim | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 23 | `rewrite_zh` | OSNMA | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 24 | `rewrite_zh` | ED-AttConvLSTM | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 25 | `rewrite_zh` | GREAT-MSF | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 26 | `rewrite_zh` | MAPS | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 27 | `rewrite_zh` | UNB3m | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 28 | `rewrite_zh` | BUAA-RINEX-Convertor | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 29 | `rewrite_zh` | goGPS_Java | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 30 | `rewrite_zh` | GNSS-REFLECTOMETRY-PROCESSING | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 31 | `rewrite_zh` | GPSL1-DPEmodule | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 32 | `rewrite_zh` | nmea-msgs | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 33 | `rewrite_zh` | FAST | desc_zh, analysis_zh; short human Chinese QC |

## Counts after sync
- `project_count`: **733**
- `counts_by_category`: `{"gnss-data": 111, "gnss-datasets": 94, "gnss-positioning": 82, "gnss-sdr": 59, "ionosphere": 236, "mobile-apps": 16, "navigation-ins": 59, "orbit-clock": 13, "tools-learning": 31, "troposphere": 32}`
- `provenance_counts`: `{"personal_community": 317, "academic_lab": 221, "official": 195}`
- `updated`: **2026-09-24**
- Remaining empty license: **171**
- Remaining empty language: **34**
- Remaining HTTP: CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN
- Remaining empty markers: ~337
- `desc_zh` == `one_liner_zh`: ~577
- `core` without `featured`: ~68

## Top remaining issues (batch 5)
1. **~171 empty licenses** — many GitHub repos truly null/NOASSERTION; continue SPDX-only; optional non-GitHub license pages.
2. **~34 empty languages** — data/awesome-lists or API null/quirky; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈577) — polish only misleading portal/software one-liners.
5. **`core` vs `featured` drift** (~68 core without featured) — decide policy before bulk flip; SH-GIM stays owned special.
6. More provenance spot-audits (Baidu caster, AgOpenGPS-Official, professor User accounts, ION Metadata WG) — verify only.
