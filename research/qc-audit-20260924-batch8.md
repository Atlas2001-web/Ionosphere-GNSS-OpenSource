# Catalog QC audit — 2026-09-24 batch 8

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 7 (`ad4c9f9`): **774** entries; `desc_zh`==`one_liner_zh` **504**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / featured / core software); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **504** before → **469** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000` / FAIL). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch7 integrity
Sample Chinese QC (KF-GINS / PRIDE-PPPAR / georinex OL≠DZ) intact. Prior provenance upgrades still present.

### Provenance spot-checks (gh api `users/{owner}`)
| Name | Detail |
|---|---|
| Navigation-Learning | personal_community→academic_lab; LiZhengXiao99 / 长安大学硕士研究生 |
| Gkit-Bias | personal_community→academic_lab; same author LiZhengXiao99 |
| CU-SDR-Collection | KEEP — gnsscusdr empty |
| imu_x_fusion | KEEP — cggos / CGSAI company |
| TightlyCoupledINSGNSS | KEEP — benzenemo empty |
| syncgpslidarimucam | KEEP — nkliuhui empty |
| ge-gnss-visibility | KEEP — taroz personal researcher |
| GNSS-GPS-SDR | KEEP — JiaoXianjun no university |
| GNSS-DSP-tools | KEEP — pmonta personal |
| SignalSim | KEEP — globsky empty |
| Full_Stack_GPS_Receiver | KEEP — hamsternz / Hamsterworks |
| rtkbase | KEEP — Stefal empty |
| ahrs | KEEP — Mayitzin / Neeno company |
| gps-sdr-sim | KEEP — osqzss personal Japan |
| RTKLIB-explorer | KEEP — rtklibexplorer / RTK Consultants LLC |
| gnss_gpu | KEEP — rsasaki0109 / MAP IV company |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **2** → academic_lab; **14** spot-audits kept
- Chinese rewrites: **35** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **35** (2 also provenance)
- `project_count` unchanged: **774**
- `lists/*.md` surgically synced (01–09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | Navigation-Learning | provenance; personal_community→academic_lab; LiZhengXiao99 / 长安大学硕士研究生 |
| 2 | `provenance` | Gkit-Bias | provenance; personal_community→academic_lab; LiZhengXiao99 / 长安大学硕士研究生 |
| 3 | `rewrite_zh` | HASlib | one_liner_zh, desc_zh; short human Chinese QC |
| 4 | `rewrite_zh` | MADOCALIB | one_liner_zh, desc_zh; short human Chinese QC |
| 5 | `rewrite_zh` | CLASLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 6 | `rewrite_zh` | mpsim | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | RADIATE | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | autorino | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | Gkit-Bias | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | BKG-NtripCaster | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | RTCM-Ntrip-Software | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | TEQC | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | gLAB-UPC | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | Galileo-NeQuick-G | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | IRI-Fortran | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | SPOCC | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | GSILIB | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | Navigation-Learning | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | awesome-gnss-barbeau | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | awesome-gins-datasets | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | GNSS_Multipath_Analysis_Software | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | pyglow | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | pynmeagps | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | GNSSTimeServer | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | ntrip-cpp | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | learning_rtklib | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | GNSS-GPS-SDR | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | ntripcaster-docker-bkg | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | ge-gnss-visibility | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | rtklib_ros_bridge | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | GraphRTK-INS | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | MRTKLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | RTKLIB-B2b | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | GIOW-release | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | gnss-tec | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | goGPS_Java | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | MALIB | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: BKG-NtripCaster, CLASLIB, GNSS-GPS-SDR, GNSSTimeServer, GNSS_Multipath_Analysis_Software, GIOW-release, Gkit-Bias, GSILIB, Galileo-NeQuick-G, GraphRTK-INS, HASlib, IRI-Fortran, MADOCALIB, MALIB, MRTKLIB, Navigation-Learning, RADIATE, RTCM-Ntrip-Software, RTKLIB-B2b, SPOCC, TEQC, awesome-gins-datasets, awesome-gnss-barbeau, autorino, gLAB-UPC, ge-gnss-visibility, gnss-tec, goGPS_Java, learning_rtklib, mpsim, ntrip-cpp, ntripcaster-docker-bkg, pyglow, pynmeagps, rtklib_ros_bridge

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch8.json`.
Keep audits: `research/_qc_batch8_prov_keep.json`.

## Counts after sync
- `project_count`: **774**
- `counts_by_category`: `{"gnss-data": 112, "gnss-datasets": 121, "gnss-positioning": 85, "gnss-sdr": 59, "ionosphere": 239, "mobile-apps": 19, "navigation-ins": 60, "orbit-clock": 13, "tools-learning": 32, "troposphere": 34}`
- `provenance_counts`: `{"official": 224, "academic_lab": 255, "personal_community": 295}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **469**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 9)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈469) — continue short human polish on remaining high-star / core software (avoid portal walls).
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
