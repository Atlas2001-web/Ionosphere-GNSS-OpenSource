# Catalog QC audit — 2026-09-24 batch 7

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 6 + docs + routine 20260924c (+14): **774** entries
- Goal: QC only (no new projects) — Chinese polish primary; provenance verify-only; HTTPS probe; SPDX mostly exhausted
- Dedicated catalog-only commit; parallel docs/tutorial dirty trees left untouched

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **~540** before → **504** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX fills (spot-check ginan/goGPS_MATLAB/gnsstk/MG_APP/TGINS → null/NOASSERTION). Empty languages left untouched.

### Batch6 integrity (post routine-merge)
All 18 batch6 provenance upgrades still present (merge-preserve held). Sample Chinese QC (gici-open / RTKLIB-style OL≠DZ) intact.

### Provenance spot-checks (gh api `users/{owner}`)
| Name | Detail |
|---|---|
| TGINS | personal_community→academic_lab; heiwa0519 / China University of Mining and Technology |
| RTK-Visual-Inertial-Navigation | personal_community→academic_lab; xiaohong-huang / South China University of Technology (Ph.D. Candidate) |
| GAMPII-GOOD | personal_community→academic_lab; zhouforme0318 / Shandong University of Science and Technology |
| Analog-GPS-data-receiver | personal_community→academic_lab; leaningktower / UIUC affiliation |
| GINav | KEEP — kaichen686 no clear org/bio |
| VINS-GPS-Wheel | KEEP — Wallong empty |
| nav_matlab | KEEP — yandld industry (外企) |
| GNSS_Multipath_Analysis_Software | KEEP — paarnes no org/bio |
| pyglow | KEEP — timduly4 / Spire Global company |
| eagleye | KEEP — MapIV company OSS |
| gnss-ins-sim | KEEP — Aceinna company OSS |
| carvig | KEEP — Erensu loc=WHU only (weak) |
| libgnss++ | KEEP — rsasaki0109 / MAP IV company |
| rinex | KEEP — nav-solutions not clear university lab |
| android_rinex | KEEP — rokubun company |
| learning_rtklib | KEEP — libing64 / 元戎启行 company |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **4** → academic_lab; **12** spot-audits kept
- Chinese rewrites: **36** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **36**
- `project_count` unchanged: **774**
- `lists/*.md` surgically synced (01–04, 06–08); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | TGINS | provenance; personal_community→academic_lab; heiwa0519 / China University of Mining and Technology (student, GNSS research bio) |
| 2 | `provenance` | RTK-Visual-Inertial-Navigation | provenance; personal_community→academic_lab; xiaohong-huang / South China University of Technology (Ph.D. Candidate SLAM) |
| 3 | `provenance` | GAMPII-GOOD | provenance; personal_community→academic_lab; zhouforme0318 / Shandong University of Science and Technology (GAMP/GAMP II) |
| 4 | `provenance` | Analog-GPS-data-receiver | provenance; personal_community→academic_lab; leaningktower / UIUC affiliation |
| 5 | `rewrite_zh` | KF-GINS | one_liner_zh, desc_zh; short human Chinese QC |
| 6 | `rewrite_zh` | OB_GINS | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | gnss-ins-sim | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | eagleye | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | gps-measurement-tools | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | PRIDE-PPPAR | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | ginan | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | goGPS_MATLAB | desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | GREAT-PVT | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | GREAT-MSF | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | georinex | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | gnss_lib_py | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | gnssrefl | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | cssrlib | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | FGI-GSRx | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | gnsstk | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | pyrtklib | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | gnss_comm | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | ublox_driver | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | KF-GINS-Matlab | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | android_rinex | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | pyrtcm | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | pygnssutils | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | bluetooth_gnss | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | GNSS-DSP-tools | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | rinex | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | septentrio_gnss_driver | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | pysat | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | PyAPS | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | VINS-GPS-Wheel | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | nav_matlab | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | MG_APP | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | TGINS | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | RTK-Visual-Inertial-Navigation | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | GAMPII-GOOD | one_liner_zh, desc_zh; short human Chinese QC |
| 40 | `rewrite_zh` | Analog-GPS-data-receiver | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: Analog-GPS-data-receiver, FGI-GSRx, GAMPII-GOOD, GNSS-DSP-tools, GREAT-MSF, GREAT-PVT, KF-GINS, KF-GINS-Matlab, MG_APP, OB_GINS, PRIDE-PPPAR, PyAPS, RTK-Visual-Inertial-Navigation, TGINS, VINS-GPS-Wheel, android_rinex, bluetooth_gnss, cssrlib, eagleye, georinex, ginan, gnss-ins-sim, gnss_comm, gnss_lib_py, gnssrefl, gnsstk, goGPS_MATLAB, gps-measurement-tools, nav_matlab, pygnssutils, pyrtcm, pyrtklib, pysat, rinex, septentrio_gnss_driver, ublox_driver

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch7.json`.
Keep audits: `research/_qc_batch7_prov_keep.json`.

## Counts after sync
- `project_count`: **774**
- `counts_by_category`: `{"gnss-data": 112, "gnss-datasets": 121, "gnss-positioning": 85, "gnss-sdr": 59, "ionosphere": 239, "mobile-apps": 19, "navigation-ins": 60, "orbit-clock": 13, "tools-learning": 32, "troposphere": 34}`
- `provenance_counts`: `{"official": 224, "academic_lab": 253, "personal_community": 297}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **504**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 8)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈504) — continue short human polish on misleading software one-liners (avoid portal walls).
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path held through 20260924c.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
