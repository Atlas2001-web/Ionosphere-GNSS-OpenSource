# Catalog QC audit — 2026-09-24 batch 14

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch13 `64381ad`: **830** entries; `desc_zh`==`one_liner_zh` **296**
- Goal: QC only (no new projects) — Chinese polish primary (software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **296** before → **258** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 12)
All six catalog HTTP URLs answer on HTTP (`200`); matching HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch13 integrity
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / ImuGpsGuiding / RTStreamHub / PPPH-UAV / meta-gnss-sdr / FlyDog-SDR-GPS / VARION OL≠DZ) intact. Prior provenance upgrades (HASPPP / PPP_AR / OSNMA / MAPS / BeiDou_B1C / GPSL1-DPEmodule / gnss2tws-green / ImuGpsGuiding / GNSS-Explorer / RTStreamHub / PPPH-UAV / gnsssdrgui / meta-gnss-sdr / docker-gnsssdr / INPE-TEC-Maps-IONEX → academic_lab; batch13 eleven upgrades) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| BDS-3-PPP-B2b-DATA | personal_community→academic_lab; zp-9696 company Chang'an university; bio student graduated Chang'an University, LEO+GNSS |
| gnssr4river | personal_community→academic_lab; lroineau company ANCT (French public agency); bio Geomatics engineer |
| OASIS | personal_community→academic_lab; giorgiopicanco bio Geophysicist \| Ph.D. in Space Geophysics \| GNSS Data Processing \| Ionospheric Modeling |
| GNSSPositioning / multi-channel-gnss / gnssr-synth / READ_GNSS / uNavTools / gnss-sdr-rs / PPP-RTK-Ionosphere | KEEP — empty bio/company → keep personal_community |
| ntrip-catalog | KEEP — Pix4D SA commercial org catalog → keep personal_community |
| esp2822NMEAsim | KEEP — Ph.D. bio but company @RobotecAI commercial → keep personal_community |
| ion_gnss25_fg_code_examples | KEEP — PNT bio; no university/agency company → keep personal_community |
| ionosphere-plotting | KEEP — software engineer @ hospital; not academic GNSS lab → keep personal_community |
| sp3 | KEEP — nav-solutions community org → keep personal_community |
| SbfParser / Alouette_ISIS_extract / Swarm_notebooks / Septentrio-PyDataLink / sami3_gitm | KEEP — already official — confirmed |
| rinexmod / RTK / GVINS-WHU / ionosphereAI / POLAN / MCOSB / pwv_kpno / PyRayHF / tidd / DDM-Former / csonde-gnss-ionosphere / mrtklib-docker-ui / crz2rnx / awsgnssroutils / pysatModels / iri90 / CSSR-tool / GMR-Water / SPP_SPV / radionopy | KEEP — already academic_lab — confirmed |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **3** → academic_lab; **37** spot-audits kept/confirmed
- Chinese rewrites: **38** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **39**
- `project_count` unchanged by this QC: **830**
- `lists/*.md` surgically synced (01–07, 09–10); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | BDS-3-PPP-B2b-DATA | provenance; personal_community→academic_lab; zp-9696 Chang'an University |
| 2 | `provenance` | gnssr4river | provenance; personal_community→academic_lab; lroineau @ ANCT |
| 3 | `provenance` | OASIS | provenance; personal_community→academic_lab; giorgiopicanco Ph.D. Space Geophysics |
| 4 | `rewrite_zh` | GNSSPositioning | one_liner_zh, desc_zh; short human Chinese QC |
| 5 | `rewrite_zh` | multi-channel-gnss | one_liner_zh, desc_zh; short human Chinese QC |
| 6 | `rewrite_zh` | SbfParser | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | GVINS-WHU | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | rinexmod | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | RTK | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | Alouette_ISIS_extract | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | ionosphereAI | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | POLAN | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | MCOSB | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | gnssr-synth | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | pwv_kpno | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | READ_GNSS | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | uNavTools | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | mrtklib-docker-ui | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | csonde-gnss-ionosphere | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | PyRayHF | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | tidd | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | Swarm_notebooks | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | DDM-Former | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | crz2rnx | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | gnss-sdr-rs | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | awsgnssroutils | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | ntrip-catalog | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | pysatModels | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | Septentrio-PyDataLink | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | gnssr4river | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | iri90 | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | CSSR-tool | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | GMR-Water | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | PPP-RTK-Ionosphere | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | SPP_SPV | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | esp2822NMEAsim | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | ion_gnss25_fg_code_examples | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | ionosphere-plotting | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | radionopy | one_liner_zh, desc_zh; short human Chinese QC |
| 40 | `rewrite_zh` | sami3_gitm | one_liner_zh, desc_zh; short human Chinese QC |
| 41 | `rewrite_zh` | BDS-3-PPP-B2b-DATA | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: Alouette_ISIS_extract, BDS-3-PPP-B2b-DATA, CSSR-tool, DDM-Former, GMR-Water, GNSSPositioning, GVINS-WHU, MCOSB, POLAN, PPP-RTK-Ionosphere, PyRayHF, READ_GNSS, RTK, SPP_SPV, SbfParser, Septentrio-PyDataLink, Swarm_notebooks, awsgnssroutils, crz2rnx, csonde-gnss-ionosphere, esp2822NMEAsim, gnss-sdr-rs, gnssr-synth, gnssr4river, ion_gnss25_fg_code_examples, ionosphere-plotting, ionosphereAI, iri90, mrtklib-docker-ui, multi-channel-gnss, ntrip-catalog, pwv_kpno, pysatModels, radionopy, rinexmod, sami3_gitm, tidd, uNavTools

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch14.json`.
Keep audits: `research/_qc_batch14_prov_keep.json`.

## Counts after sync
- `project_count`: **830**
- `counts_by_category`: `{"ionosphere": 244, "troposphere": 39, "gnss-data": 120, "gnss-positioning": 95, "orbit-clock": 16, "navigation-ins": 63, "gnss-sdr": 62, "mobile-apps": 22, "tools-learning": 44, "gnss-datasets": 125}`
- `provenance_counts`: `{"official": 236, "academic_lab": 312, "personal_community": 282}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **258**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 15)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈258) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: RNXQCE / Easy4PTK / EGNOS_SDK_Core / Muf_Muncher / BDS-3-PPP-B2b_IMU_LiDAR / sp3 / CU-SDR-Collection related mid-tier identical / remaining identical under ionosphere & gnss-sdr / mid-star personal_community software still identical.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear (e.g. known researchers with empty GitHub bio left untouched this batch: borioda/PadArt).

## Correction note
Commit `adc81ec` raced with concurrent `routine-2026-09-24h` and briefly carried those
**+12** finds inside the QC commit (count 842) despite the message saying 830.
`80e859f` then landed the routine research artifacts (merge script + finds JSON + NOTES).
Follow-up `702daf5` strips the 12 entries from PROJECTS/lists/README so batch14 stays
QC-only at **830**. Re-apply via `research/merge_routine_20260924h.py` /
`research/routine_finds_20260924h.json` when ready for a dedicated routine merge.

