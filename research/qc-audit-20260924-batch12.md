# Catalog QC audit — 2026-09-24 batch 12

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch11 `6ab0a71` + docs + routine `dae51f3` (+14): **816** entries; `desc_zh`==`one_liner_zh` **367**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **367** before → **331** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 12)
All six catalog HTTP URLs answer on HTTP (`200`); matching HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch11 integrity
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / ImuGpsGuiding OL≠DZ) intact. Prior provenance upgrades (HASPPP / PPP_AR / OSNMA / MAPS / BeiDou_B1C / GPSL1-DPEmodule / gnss2tws-green / ImuGpsGuiding / GNSS-Explorer → academic_lab) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| RTStreamHub | personal_community→academic_lab; ZhangRunzhi20 company University of Chinese Academy of Sciences; bio Ph.D NTSC/CAS |
| PPPH-UAV | personal_community→academic_lab; BerkayBahadur company Hacettepe University; bio Associate Professor Geomatics |
| gnsssdrgui | personal_community→academic_lab; UHaider company NUST |
| meta-gnss-sdr | personal_community→academic_lab; carlesfernandez company CTTC; bio Senior Researcher |
| docker-gnsssdr | personal_community→academic_lab; carlesfernandez company CTTC; bio Senior Researcher |
| INPE-TEC-Maps-IONEX | personal_community→academic_lab; Hollweg company University of Michigan - Dearborn; bio Researcher/Adjunct Lecturer |
| FlyDog-SDR-GPS | KEEP — community hardware org FlyDog SDR; no university/agency → keep personal_community |
| GPSGALSSS | KEEP — empty company; personal bio → keep personal_community |
| gnss-signal-simulator-rs | KEEP — company home; personal → keep personal_community |
| msckfvioGPS | KEEP — empty bio/company → keep personal_community |
| STM32Primer2-GNSS-Tracker | KEEP — hobbyist org Nijiura Maids Association → keep personal_community |
| gnss-sdr-1pps | KEEP — OscillatorIMP PIA community org; not clear university/agency class → keep |
| awesome-gnss-hdkarimi | KEEP — personal FOSS curator; company empty → keep personal_community |
| ntrip-client | KEEP — nav-solutions community org France; no agency/university → keep |
| ntrip-caster-go | KEEP — empty bio/company → keep personal_community |
| M_GIM-zcytju | KEEP — empty bio/company → keep personal_community |
| gnssgo | KEEP — company Explore Data Technology Ltd commercial → keep personal_community |
| PW_from_GPS | KEEP — industry researcher; no university company → keep personal_community |
| pylgrim | KEEP — company secjur commercial → keep personal_community |
| BUAA-RINEX-Convertor | KEEP — empty bio/company (BUAA only in project name) → keep |
| GHASP-HAS-decoding | KEEP — empty bio/company despite known researcher name → keep until org field clear |
| GNSSRMERRByS | KEEP — Surrey Satellite Technology Ltd commercial → keep personal_community |
| mosgim2 | KEEP — empty bio/company (PadArt) → keep personal_community |
| gnss_ros_standardization | KEEP — empty bio/company → keep personal_community |
| GNSSSDRHACKRF | KEEP — empty bio/company → keep personal_community |
| BNS | KEEP — already official (BKG) — confirmed |
| BNC-source-FTP | KEEP — already official (BKG FTP) — confirmed |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **6** → academic_lab; **21** spot-audits kept/confirmed
- Chinese rewrites: **36** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **37** (6 also provenance; docker-gnsssdr provenance-only)
- `project_count` unchanged by this QC: **816**
- `lists/*.md` surgically synced (01–09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | RTStreamHub | provenance; personal_community→academic_lab; ZhangRunzhi20 company University of Chinese Academy of Sciences; bio Ph.D NTSC/CAS |
| 2 | `provenance` | PPPH-UAV | provenance; personal_community→academic_lab; BerkayBahadur company Hacettepe University; bio Associate Professor Geomatics |
| 3 | `provenance` | gnsssdrgui | provenance; personal_community→academic_lab; UHaider company NUST |
| 4 | `provenance` | meta-gnss-sdr | provenance; personal_community→academic_lab; carlesfernandez company CTTC; bio Senior Researcher |
| 5 | `provenance` | docker-gnsssdr | provenance; personal_community→academic_lab; carlesfernandez company CTTC; bio Senior Researcher |
| 6 | `provenance` | INPE-TEC-Maps-IONEX | provenance; personal_community→academic_lab; Hollweg company University of Michigan - Dearborn; bio Researcher/Adjunct Lecturer |
| 7 | `rewrite_zh` | FlyDog-SDR-GPS | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | GPSGALSSS | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | gnss-signal-simulator-rs | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | msckfvioGPS | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | STM32Primer2-GNSS-Tracker | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | gnss-sdr-1pps | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | awesome-gnss-hdkarimi | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | BNS | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | ntrip-client | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | M_GIM-zcytju | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | ntrip-caster-go | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | BNC-source-FTP | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | gnssgo | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | PW_from_GPS | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | pylgrim | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | BUAA-RINEX-Convertor | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | GHASP-HAS-decoding | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | GNSSRMERRByS | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | PPP | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | oresat-gps-software | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | PRIDE-GeoDataLogger | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | sami2py | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | GINS | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | gnss_ros_standardization | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | gstream | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | APAS-TR | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | GNSSSDRHACKRF | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | RTStreamHub | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | PPPH-UAV | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | gnsssdrgui | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | meta-gnss-sdr | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | mosgim2 | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | GREAT-IFCB | one_liner_zh, desc_zh; short human Chinese QC |
| 40 | `rewrite_zh` | VARION | one_liner_zh, desc_zh; short human Chinese QC |
| 41 | `rewrite_zh` | PyRINEX | one_liner_zh, desc_zh; short human Chinese QC |
| 42 | `rewrite_zh` | INPE-TEC-Maps-IONEX | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: APAS-TR, BNC-source-FTP, BNS, BUAA-RINEX-Convertor, FlyDog-SDR-GPS, GHASP-HAS-decoding, GINS, GNSSRMERRByS, GNSSSDRHACKRF, GPSGALSSS, GREAT-IFCB, INPE-TEC-Maps-IONEX, M_GIM-zcytju, PPP, PPPH-UAV, PRIDE-GeoDataLogger, PW_from_GPS, PyRINEX, RTStreamHub, STM32Primer2-GNSS-Tracker, VARION, awesome-gnss-hdkarimi, gnss-sdr-1pps, gnss-signal-simulator-rs, gnss_ros_standardization, gnssgo, gnsssdrgui, gstream, meta-gnss-sdr, mosgim2, msckfvioGPS, ntrip-caster-go, ntrip-client, oresat-gps-software, pylgrim, sami2py

Full machine log (gitignored if configured): `research/_qc_touch_log_20260924_batch12.json`.
Keep audits: `research/_qc_batch12_prov_keep.json`.

## Counts after sync
- `project_count`: **816**
- `counts_by_category`: `{"ionosphere": 242, "troposphere": 37, "gnss-data": 119, "gnss-positioning": 94, "orbit-clock": 14, "navigation-ins": 63, "gnss-sdr": 61, "mobile-apps": 22, "tools-learning": 39, "gnss-datasets": 125}`
- `provenance_counts`: `{"official": 233, "academic_lab": 290, "personal_community": 293}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **331**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 13)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈331) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: tec_prediction-ONERA / GNSSR_MERRByS_Python / sidereon / GREAT-PIFGO / gnatss / HPRTK / Ionort-raytrace / GNSS-REFLECTOMETRY-PROCESSING / INX_Editor / pygnss-tec / SuperSID / gps-sdr-simulink / GNSSommelier / QuadSPP / RAIM_PANG_NAV / gnss-rcv / PyLap / pysatSpaceWeather / salsa / gnssrlowcost / GDDS / pyrtklib_demo5 / DeepPredTEC / ionosonde_volgatech / KF-GINS-Py.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear (e.g. borioda/GHASP-HAS-decoding kept pending company field).

