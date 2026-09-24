# Catalog QC audit — 2026-09-24 batch 5

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 4 (`99c1ad7`) + routine merge `ecfaec4` (+14) + docs commits: **747** entries
- Goal: QC only (no new projects) — SPDX license fills, provenance verification, Chinese blurbs, HTTPS probe
- Note: routine merge `ecfaec4` had reverted batch-4 SPDX fills and `nmea-msgs`/`FAST` provenance; batch 5 restores those verified fixes

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **~577** (mostly portals) |
| Empty `license` | **171** (≈158 GitHub) |
| Empty `language` | **34** (API null / quirky primaries) |
| HTTP leftovers | **6** |

### HTTPS probe (curl -I -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### Language scan (gh api `.language`)
Remaining empties are API `null` or quirky primaries (PostScript / Grammatical Framework / Roff / HTML / OpenEdge ABL / Starlark). **No fills.**

### Provenance spot-checks (gh api)
| Name | Owner | Verdict |
|---|---|---|
| nmea-msgs | ros-drivers | **restore personal→official** (batch4; reverted by routine merge) |
| FAST | ChangChuntao (`aircas.ac.cn`) | **restore personal→academic_lab** (batch4; reverted) |
| GraphGNSSLib | weisongwen (Asst Prof, PolyU) | **personal→academic_lab** |
| Net_Diff | YizeZhang (Shanghai Astronomical Observatory) | **personal→academic_lab** |
| GNSS-Metadata-Standard | IonMetadataWorkingGroup (ION GNSS SDR Metadata WG) | **personal→official** |
| raPPPid | TUW-VieVS (TU Wien VieVS) | **personal→academic_lab** |
| baidu-ntripcaster | baidu (Baidu Open Source org) | **keep personal_community** (`categories.md`: 公司开源档) |
| AgOpenNtripCaster | AgOpenGPS-Official (DIY community org) | **keep personal_community** (小型社区团队) |

### SPDX scan (gh api `.license.spdx_id`, skip null/NOASSERTION)
Of ~158 empty-license GitHub repos, only **2** new SPDX hits (`tec_forecast` MIT, `VINS-GPS-Wheel` GPL-3.0). Also **restore 9** batch-4 fills wiped by routine merge.

## This batch — summary
- License fills via `gh api` `.license.spdx_id`: **11** (9 restore + 2 new)
- Language fills: **0**
- Provenance fixes: **6** (2 restore + 4 new); 2 spot-audits kept
- Chinese rewrites: **31** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0** (no bulk policy)
- HTTPS upgrades: **0**
- Entries touched (unique names): **43**
- `project_count` unchanged: **747**
- `lists/*.md` surgically synced (01–04, 06, 08–09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `meta_fill` | GNSSClock | license; gh api → LGPL-2.1 (restore) |
| 2 | `meta_fill` | GNSSTimeServer | license; gh api → MIT (restore) |
| 3 | `meta_fill` | IndirectEKFIMUGPS | license; gh api → MIT (restore) |
| 4 | `meta_fill` | gnss2tws-green | license; gh api → GPL-3.0 (restore) |
| 5 | `meta_fill` | gnssIR-matlab-v3 | license; gh api → MIT (restore) |
| 6 | `meta_fill` | gnssIR-python | license; gh api → MIT (restore) |
| 7 | `meta_fill` | gnssr-synth | license; gh api → MIT (restore) |
| 8 | `meta_fill` | gnssrlowcost | license; gh api → MIT (restore) |
| 9 | `meta_fill` | gnsssdrgui | license; gh api → GPL-3.0 (restore) |
| 10 | `meta_fill` | tec_forecast | license; gh api → MIT |
| 11 | `meta_fill` | VINS-GPS-Wheel | license; gh api → GPL-3.0 |
| 12 | `provenance` | nmea-msgs | personal_community→official (restore) |
| 13 | `provenance` | FAST | personal_community→academic_lab (restore) |
| 14 | `provenance` | GraphGNSSLib | personal_community→academic_lab; Weisong Wen / PolyU |
| 15 | `provenance` | Net_Diff | personal_community→academic_lab; YizeZhang / SHAO |
| 16 | `provenance` | GNSS-Metadata-Standard | personal_community→official; ION Metadata WG |
| 17 | `provenance` | raPPPid | personal_community→academic_lab; TUW-VieVS |
| 18–48 | `rewrite_zh` | IC-GVINS, GVINS-HKUST, ppp-tools, cycle-slip-correction, gnss-multipath-detector, GPSLogger, prx, scintkit, rtcm, gps_pvt, GNSS_RR, iri2020, gtsam_gnss, GNSS-Metadata-Standard, ICAMS, raPPPid, gnsspy, ntripstreams, crx2rnx, gnss-rtk, RinexReader, GraphGNSSLib, gtsam, tightly-coupled-gnss-imu-fgo, kshana, earth-gravitational-model, GPSTk, FAST, nmea-msgs, baidu-ntripcaster, AgOpenNtripCaster | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |

Full machine log: `research/_qc_touch_log_20260924_batch5.json`.

## Counts after sync
- `project_count`: **747**
- `counts_by_category`: `{"gnss-data": 111, "gnss-datasets": 102, "gnss-positioning": 83, "gnss-sdr": 59, "ionosphere": 238, "mobile-apps": 18, "navigation-ins": 59, "orbit-clock": 13, "tools-learning": 31, "troposphere": 33}`
- `provenance_counts`: `{"official": 205, "academic_lab": 227, "personal_community": 315}`
- `updated`: **2026-09-24**
- Remaining empty license: **~169** (vast majority GitHub null/NOASSERTION)
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **~568**
- `core` without `featured` / featured policy: unchanged (no bulk flip)

## Top remaining issues (batch 6)
1. **~169 empty licenses** — almost all GitHub null/NOASSERTION; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈568) — continue short human polish on misleading software one-liners (avoid portal walls).
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites of QC fields (SPDX / provenance / Chinese) on next catalog merge.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
