# Catalog QC audit — 2026-09-24 batch 9

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine `5ce7c94` (+14 over batch8 `e2256e2`): **788** entries; `desc_zh`==`one_liner_zh` **469**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / featured / core software); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **469** before → **437** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000` / FAIL). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch8 integrity (after routine +14)
Sample Chinese QC (KF-GINS / PRIDE-PPPAR / georinex / HASlib / MADOCALIB / TEQC / pyglow OL≠DZ) intact. Prior provenance upgrades (Navigation-Learning / Gkit-Bias → academic_lab) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| carvig | personal_community→academic_lab; Erensu / location WHU,China (SuJingLan) |
| B2bLIB | personal_community→academic_lab; GCCLib PI Zhetao Zhang / 同济大学副教授 (ResearchGate) |
| PyTECGg | personal_community→academic_lab; viventriglia company @INGV; SoftwareX INGV coauthors |
| gpsd | KEEP — GitLab gpsd FOSS daemon, no agency/university org |
| MatRTKLIB | KEEP — taroz / Taro Suzuki personal |
| gnss_gpu | KEEP — rsasaki0109 / MAP IV company |
| CU-SDR-Collection | KEEP — gnsscusdr empty |
| syncgpslidarimucam | KEEP — nkliuhui empty |
| NequickG | KEEP — tpl2go empty |
| NavDecoder | KEEP — NavSesne empty |
| pinot | KEEP — purpleskyfall personal |
| OASIS | KEEP — giorgiopicanco PhD bio, no current institution |
| caster | KEEP — Node-NTRIP community org |
| SparkFun_u-blox_GNSS_v3 | KEEP — SparkFun company (commercial → personal_community) |
| GNSSFirehose | KEEP — pmonta personal |
| ublox_dgnss | KEEP — aussierobots company |
| STM32-GNSS | KEEP — SimpleMethod personal |
| STD_SWD_Calc | KEEP — zohrehadavi empty |
| ionex-rs | KEEP — nav-solutions community org |
| gps-sdr | KEEP — gps-sdr legacy personal |
| gnss-sdr-monitor | KEEP — acebrianjuan personal |
| RTPPP_B2b | KEEP — floating0516 / Li He empty affiliation |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **3** → academic_lab; **19** spot-audits kept
- Chinese rewrites: **32** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **32** (3 also provenance)
- `project_count` unchanged: **788**
- `lists/*.md` surgically synced (01–08); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | carvig | provenance; personal_community→academic_lab; Erensu / WHU,China |
| 2 | `provenance` | B2bLIB | provenance; personal_community→academic_lab; GCCLib / 同济大学 Zhetao Zhang |
| 3 | `provenance` | PyTECGg | provenance; personal_community→academic_lab; viventriglia @INGV |
| 4 | `rewrite_zh` | PPP-Wizard | one_liner_zh, desc_zh; short human Chinese QC |
| 5 | `rewrite_zh` | syncgpslidarimucam | one_liner_zh, desc_zh; short human Chinese QC |
| 6 | `rewrite_zh` | carvig | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | gpsd | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | MatRTKLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | iri2016 | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | gnss_gpu | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | CU-SDR-Collection | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | PyIRI | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | NequickG | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | NavDecoder | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | B2bLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | pinot | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | GREAT-UPD | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | GREAT_PODFLT | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | GREAT-PCE | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | OASIS | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | ionex | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | RTPPP_B2b | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | STD_SWD_Calc | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | ionex-rs | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | caster | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | PyTECGg | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | GEMINI3D | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | gnss-sdr-monitor | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | gps-sdr | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | GNSSFirehose | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | GAMP_PPPH | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | ublox_dgnss | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | SparkFun_u-blox_GNSS_v3 | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | STM32-GNSS | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | GNSS_INS_Integrations_Comparisons | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: B2bLIB, CU-SDR-Collection, GAMP_PPPH, GEMINI3D, GNSSFirehose, GNSS_INS_Integrations_Comparisons, GREAT-PCE, GREAT-UPD, GREAT_PODFLT, MatRTKLIB, NavDecoder, NequickG, OASIS, PPP-Wizard, PyIRI, PyTECGg, RTPPP_B2b, STD_SWD_Calc, STM32-GNSS, SparkFun_u-blox_GNSS_v3, carvig, caster, gnss-sdr-monitor, gnss_gpu, gps-sdr, gpsd, ionex, ionex-rs, iri2016, pinot, syncgpslidarimucam, ublox_dgnss

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch9.json`.
Keep audits: `research/_qc_batch9_prov_keep.json`.

## Counts after sync
- `project_count`: **788**
- `counts_by_category`: `{"gnss-data": 117, "gnss-datasets": 122, "gnss-positioning": 88, "gnss-sdr": 59, "ionosphere": 240, "mobile-apps": 20, "navigation-ins": 60, "orbit-clock": 13, "tools-learning": 34, "troposphere": 35}`
- `provenance_counts`: `{"official": 226, "academic_lab": 264, "personal_community": 298}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **437**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 10)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈437) — continue short human polish on remaining high-star / core software (avoid portal walls). Suggested: ntrip_client-MicroStrain, GVINS-Dataset, gps (PSAS), deep_gnss / snapshot-gnss-algorithms (new routine), remaining core ionosphere packages (IRI-2026-package / NeQuick2-ICTP only if software-facing), more GREAT/RTKLIB-family leftovers.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
