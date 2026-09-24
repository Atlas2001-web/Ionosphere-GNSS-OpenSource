# Catalog QC audit — 2026-09-24 batch 16

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-20260924i (+14) + docs QC commits: **856** entries; `desc_zh`==`one_liner_zh` **234**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy (coordinator):** preserve freshly ingested routine/目录新收录 entries (verified all 14 from 20260924i still present); do not strip or overwrite non-QC additions; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **234** before → **198** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |
| `project_count` | **856** (unchanged by QC; includes routine-i +14) |

### Prior QC integrity (after pull)
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / rinexmod / sami3_gitm / BDS-3-PPP-B2b-DATA / gnssr4river / OASIS / AETHER / SAMI2 / sp3 OL≠DZ) intact. `geoveil-cn0` provenance academic_lab intact. Routine-20260924i fourteen names all present.

### HTTPS probe (curl -sI -L --max-time 12)
Catalog HTTP URLs answer on HTTP (`200` where live); matching HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| EGNOSTools | personal_community→academic_lab; DfAC company EC Joint Research Centre (JRC) E.2 |
| Microsat-gps-sim / MyIonosphere_Library / Nequick-ITUR / UNB3m / Get_IPP / Easy4B2b / RTKNAVI-BH | KEEP — empty bio/company → keep personal_community |
| NeQuickJRC | KEEP — mgfernan GNSS expert / tech transfer personal → keep personal_community |
| GNSSRTK | KEEP — SupakunZ personal fullstack → keep personal_community |
| roti-gnss-ml / HASlib.jl / gps-qzss-sdr-sim / gri-iono / GPSMAXIM2769b- | KEEP — personal/community / commercial employment ≠ lab → keep personal_community |
| pytiegcm / cosmic-crunch | KEEP — NASA alum / available-for-hire ≠ current lab org → keep personal_community |
| ionopy / mitiono / OpATOM / Smart-UAV-Return-GNSS-Station / pysatCDAAC / AURORA / AlexandraKoulouri×2 / TEC-ROTI-Interactives / SubionosphericVLF / iono-tomography / 317Lab / FIRI-2018 / GNSS_TOM / Drift-X / CARP / plot-Anubis | KEEP — already academic_lab — confirmed |
| swds-api-downloader / BiScEF | KEEP — already official — confirmed (INPE Embrace / Kartverket) |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **1** → academic_lab; **35** spot-audits kept/confirmed
- Chinese rewrites: **36** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0** (EGNOSTools list marker only, following provenance)
- HTTPS upgrades: **0**
- Entries touched (unique names): **36**
- `project_count` unchanged by this QC: **856**
- `lists/*.md` surgically synced (01–04, 06–07); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | EGNOSTools | personal_community→academic_lab; DfAC @ EC JRC E.2 |
| 2 | `rewrite_zh` | Microsat-gps-sim | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | MyIonosphere_Library | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | NeQuickJRC | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | Nequick-ITUR | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | SubionosphericVLFInversionAlgorithms.jl | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | iono-tomography | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | ionopy | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | mitiono | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | GNSSRTK | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | OpATOM | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | UNB3m | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | Smart-UAV-Return-GNSS-Station | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | pysatCDAAC | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | pytiegcm | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | real-time-ionospheric-maps-Kalman | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | roti-gnss-ml | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | GPSMAXIM2769b- | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | AURORA | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | Ionospheric-Scintillation-Maps-and-PDOP | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | Ionospheric-TEC-ROTI-Interactives | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | swds-api-downloader | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | Easy4B2b | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | HASlib.jl | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | RTKNAVI-BH | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | gps-qzss-sdr-sim | one_liner_zh, desc_zh |
| 27 | `rewrite_zh` | 317Lab-tomography | one_liner_zh, desc_zh |
| 28 | `rewrite_zh` | FIRI-2018 | one_liner_zh, desc_zh |
| 29 | `rewrite_zh` | Get_IPP | one_liner_zh, desc_zh |
| 30 | `rewrite_zh` | gri-iono | one_liner_zh, desc_zh |
| 31 | `rewrite_zh` | Drift-X | one_liner_zh, desc_zh |
| 32 | `rewrite_zh` | CARP-Average-Profile | one_liner_zh, desc_zh |
| 33 | `rewrite_zh` | BiScEF | one_liner_zh, desc_zh |
| 34 | `rewrite_zh` | GNSS_TOM | one_liner_zh, desc_zh |
| 35 | `rewrite_zh` | plot-Anubis | one_liner_zh, desc_zh |
| 36 | `rewrite_zh` | cosmic-crunch | one_liner_zh, desc_zh |
| 37 | `rewrite_zh` | EGNOSTools | one_liner_zh, desc_zh |

Chinese rewrite names: 317Lab-tomography, AURORA, BiScEF, CARP-Average-Profile, Drift-X, EGNOSTools, Easy4B2b, FIRI-2018, GNSSRTK, GNSS_TOM, GPSMAXIM2769b-, Get_IPP, HASlib.jl, Ionospheric-Scintillation-Maps-and-PDOP, Ionospheric-TEC-ROTI-Interactives, Microsat-gps-sim, MyIonosphere_Library, NeQuickJRC, Nequick-ITUR, OpATOM, RTKNAVI-BH, Smart-UAV-Return-GNSS-Station, SubionosphericVLFInversionAlgorithms.jl, UNB3m, cosmic-crunch, gps-qzss-sdr-sim, gri-iono, iono-tomography, ionopy, mitiono, plot-Anubis, pysatCDAAC, pytiegcm, real-time-ionospheric-maps-Kalman, roti-gnss-ml, swds-api-downloader

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch16.json`.
Keep audits: `research/_qc_batch16_prov_keep.json`.

## Counts after sync
- `project_count`: **856**
- `counts_by_category`: `{"gnss-data": 128, "gnss-datasets": 127, "gnss-positioning": 98, "gnss-sdr": 65, "ionosphere": 244, "mobile-apps": 22, "navigation-ins": 64, "orbit-clock": 18, "tools-learning": 50, "troposphere": 40}`
- `provenance_counts`: `{"official": 245, "academic_lab": 315, "personal_community": 296}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **198**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 17)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈198) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: GFZRNX / GNSSNexus-rinex / Essential-GNSS / BDSSDR / FlyCat-SDR-GPS / CDAAC_COSMIC-TEC_Data-Research / FARR / GIM_fusion_VLBI / GIRO-IRTAM / GNSS-Workshop-TEC / HamSCI-ionosonde / hfpytrace / IBP-Model / Ion-Phys-Toolkit / ionex-analyzer / Ionex_Parser / IonKit-NH / IonoBench / IonOccAnalysis / mid-star identical under ionosphere & gnss-sdr.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path; rebase-before-push; never strip fresh routine entries when resolving races.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
