# Catalog QC audit — 2026-09-24 batch 17

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch16 (`614c6af`): **856** entries; `desc_zh`==`one_liner_zh` **198**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy (coordinator):** preserve freshly ingested routine/目录新收录 entries (verified all 14 from 20260924i still present); do not strip or overwrite non-QC additions; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **198** before → **162** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |
| `project_count` | **856** (unchanged by QC) |

### Prior QC integrity (after pull)
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / rinexmod / sami3_gitm / BDS-3-PPP-B2b-DATA / gnssr4river / OASIS / AETHER / SAMI2 / EGNOSTools OL≠DZ) intact. `geoveil-cn0` provenance academic_lab intact. Routine-20260924i fourteen names all present (incl. LANS-AFS-SIM / PocketSDR-AFS / namuru-gps / rt-navi / nav-solutions-gnss / piksi_tools / swift-nav-pygnss).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS upgrades still **fail** (`http_code=000` / ERR). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| m_gim-PANXIONG | personal_community→academic_lab; PANXIONG-CN company=Tsinghua University (same author as Ion-Phys-Toolkit) |
| GIM_fusion_VLBI | KEEP — arrueegg company=ETH Zürich PhD → already academic_lab |
| hfpytrace | KEEP — shibaji7 Research Associate ERAU → already academic_lab |
| Ion-Phys-Toolkit | KEEP — PANXIONG-CN Tsinghua → already academic_lab |
| IRI_TID | KEEP — w2naf company=University of Scranton → already academic_lab |
| gnssr-raspberry | KEEP — ITC-Water-Resources Faculty ITC → already academic_lab |
| ismr_downloader | KEEP — GEGE-UNESP org → already academic_lab |
| ATom-TUWien / FARR / IBP-Model / HamSCI-ionosonde / IonOccAnalysis / IonoBench / GNSS-Workshop-TEC / nleht-fdtd / pypride / tec-example / SAMI3-4.00 / SbfMixer / GFZRNX | KEEP — already academic_lab or official — confirmed |
| BDSSDR / FlyCat / CDAAC_COSMIC / ionex-analyzer / Ionex_Parser / IonKit-NH / GNSSNexus-rinex / Essential-GNSS / osqzss×3 / nav-solutions×2 / Klobuchar.jl / scintillation-mitigation | KEEP — empty bio or community/commercial ≠ lab → keep personal_community |
| piksi_tools / swift-nav-pygnss / libsbp / pynex | KEEP — swift-nav vendor OSS; categories.md maps 公司开源档→personal_community (Septentrio historical official left as-is) |
| GIRO-IRTAM | KEEP academic_lab; **skipped Chinese** (data-portal wall) |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **1** → academic_lab; **39** spot-audits kept/confirmed
- Chinese rewrites: **36** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0** (m_gim-PANXIONG list badge only, following provenance)
- HTTPS upgrades: **0**
- Entries touched (unique names): **36**
- `project_count` unchanged by this QC: **856**
- `lists/*.md` surgically synced (01–04, 07, 09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | m_gim-PANXIONG | personal_community→academic_lab; PANXIONG-CN @ Tsinghua |
| 2 | `rewrite_zh` | GFZRNX | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | GNSSNexus-rinex | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | Essential-GNSS | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | BDSSDR | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | FlyCat-SDR-GPS | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | CDAAC_COSMIC-TEC_Data-Research | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | FARR | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | GIM_fusion_VLBI | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | GNSS-Workshop-TEC | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | HamSCI-ionosonde | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | hfpytrace | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | IBP-Model | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | Ion-Phys-Toolkit | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | ionex-analyzer | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | Ionex_Parser | one_liner_zh, desc_zh |
| 17 | `rewrite_zh` | IonKit-NH | one_liner_zh, desc_zh |
| 18 | `rewrite_zh` | IonoBench | one_liner_zh, desc_zh |
| 19 | `rewrite_zh` | IonOccAnalysis | one_liner_zh, desc_zh |
| 20 | `rewrite_zh` | piksi_tools | one_liner_zh, desc_zh |
| 21 | `rewrite_zh` | swift-nav-pygnss | one_liner_zh, desc_zh |
| 22 | `rewrite_zh` | PocketSDR-AFS | one_liner_zh, desc_zh |
| 23 | `rewrite_zh` | rt-navi | one_liner_zh, desc_zh |
| 24 | `rewrite_zh` | nav-solutions-gnss | one_liner_zh, desc_zh |
| 25 | `rewrite_zh` | LANS-AFS-SIM | one_liner_zh, desc_zh |
| 26 | `rewrite_zh` | namuru-gps | one_liner_zh, desc_zh |
| 27 | `rewrite_zh` | Klobuchar.jl | one_liner_zh, desc_zh |
| 28 | `rewrite_zh` | IRI_TID | one_liner_zh, desc_zh |
| 29 | `rewrite_zh` | SAMI3-4.00 | one_liner_zh, desc_zh |
| 30 | `rewrite_zh` | ismr_downloader | one_liner_zh, desc_zh |
| 31 | `rewrite_zh` | nleht-fdtd-ionosphere | one_liner_zh, desc_zh |
| 32 | `rewrite_zh` | pypride | one_liner_zh, desc_zh |
| 33 | `rewrite_zh` | ATom-TUWien | one_liner_zh, desc_zh |
| 34 | `rewrite_zh` | tec-example | one_liner_zh, desc_zh |
| 35 | `rewrite_zh` | ionospheric-scintillation-mitigation | one_liner_zh, desc_zh |
| 36 | `rewrite_zh` | gnssr-raspberry | one_liner_zh, desc_zh |
| 37 | `rewrite_zh` | m_gim-PANXIONG | one_liner_zh, desc_zh |

Chinese rewrite names: ATom-TUWien, BDSSDR, CDAAC_COSMIC-TEC_Data-Research, Essential-GNSS, FARR, FlyCat-SDR-GPS, GFZRNX, GIM_fusion_VLBI, GNSS-Workshop-TEC, GNSSNexus-rinex, HamSCI-ionosonde, IBP-Model, IRI_TID, Ion-Phys-Toolkit, IonKit-NH, IonOccAnalysis, Ionex_Parser, IonoBench, Klobuchar.jl, LANS-AFS-SIM, PocketSDR-AFS, SAMI3-4.00, gnssr-raspberry, hfpytrace, ionex-analyzer, ionospheric-scintillation-mitigation, ismr_downloader, m_gim-PANXIONG, namuru-gps, nav-solutions-gnss, nleht-fdtd-ionosphere, piksi_tools, pypride, rt-navi, swift-nav-pygnss, tec-example

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch17.json`.
Keep audits: `research/_qc_batch17_prov_keep.json`.

## Counts after sync
- `project_count`: **856**
- `counts_by_category`: `{"gnss-data": 128, "gnss-datasets": 127, "gnss-positioning": 98, "gnss-sdr": 65, "ionosphere": 244, "mobile-apps": 22, "navigation-ins": 64, "orbit-clock": 18, "tools-learning": 50, "troposphere": 40}`
- `provenance_counts`: `{"official": 245, "academic_lab": 316, "personal_community": 295}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **162**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 18)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈162) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: SbfMixer / igs-roti / GNSSClock / Anubis-Free-Download / CCAR-GNSS-SDR-Book / ESA-UGI / IMSP-MGS / IONOLAB-TEC-Software / IRI-*-package / IRI-Plas-SPIM / mid-star identical under ionosphere & gnss-datasets portals / GFZRNX-UserGuide companion docs.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path; rebase-before-push; never strip fresh routine entries when resolving races.
7. Optional: revisit swift-nav vendor OSS vs Septentrio `official` policy consistency (libsbp/pynex/piksi) if categories.md is amended.
