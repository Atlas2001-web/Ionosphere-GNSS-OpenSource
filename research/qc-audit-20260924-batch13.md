# Catalog QC audit — 2026-09-24 batch 13

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch12 `792c82b` + docs + routine `c4dc8a4` (+14): **830** entries; `desc_zh`==`one_liner_zh` **331**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **331** before → **296** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 12)
All six catalog HTTP URLs answer on HTTP (`200`); matching HTTPS upgrades still **fail** (`http_code=000`). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch12 integrity
Sample Chinese QC (HASPPP / BeiDou_B1C / GPSBabel / cssrlib / PocketSDR / ImuGpsGuiding / RTStreamHub / PPPH-UAV / meta-gnss-sdr / FlyDog-SDR-GPS / VARION OL≠DZ) intact. Prior provenance upgrades (HASPPP / PPP_AR / OSNMA / MAPS / BeiDou_B1C / GPSL1-DPEmodule / gnss2tws-green / ImuGpsGuiding / GNSS-Explorer / RTStreamHub / PPPH-UAV / gnsssdrgui / meta-gnss-sdr / docker-gnsssdr / INPE-TEC-Maps-IONEX → academic_lab) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| rt-clk-service | personal_community→academic_lab; DoubleString bio Ph.D candidate Wuhan University |
| IonoTomo | personal_community→academic_lab; Joshuaalbert company Caltech; bio radio interferometry researcher |
| Ionospheric-Scintillation-Maps-and-PDOP | personal_community→academic_lab; AlexandraKoulouri company Tampere University |
| COSMIC-IONPRF-Ne-TEC | personal_community→academic_lab; HassanNooreldeen company Egyptian Space Agency; bio Space Weather researcher |
| ED-AttConvLSTM | personal_community→academic_lab; leeliangchao company China University of Geosciences (Beijing); bio Ph.D Student |
| GPSL1-MMT-DPEmodule | personal_community→academic_lab; Sergio-Vicenzo company The Hong Kong Polytechnic University; bio PhD student |
| ionotec | personal_community→academic_lab; sylvathle company European Space Agency; bio Research Fellow space radiations |
| scintill-ai | personal_community→academic_lab; viventriglia company @INGV |
| NearRealTimeGNSSIR | personal_community→academic_lab; cemalialtuntas company Yildiz Technical University; bio Researcher GNSS-IR |
| Ionospheric-TEC-ROTI-Interactives | personal_community→academic_lab; Tesfay-Tesfu company UNIVAP, NASA; bio Space Physics PhD |
| Smart-UAV-Return-GNSS-Station | personal_community→academic_lab; citec-spbu org (St Petersburg University CITEC) |
| gnatss | KEEP — Seafloor Geodesy community org; no university/agency → keep personal_community |
| sidereon | KEEP — empty bio/company → keep personal_community |
| GNSS-REFLECTOMETRY-PROCESSING | KEEP — empty company; personal telecom → keep personal_community |
| INX_Editor / pygnss-tec / SuperSID / gnss-rcv / gnssrlowcost / GDDS | KEEP — empty bio/company → keep personal_community |
| gps-sdr-simulink | KEEP — Samsung Semiconductor commercial → keep personal_community |
| QuadSPP | KEEP — personal FOSS curator → keep personal_community |
| RAIM_PANG_NAV | KEEP — Sichuan Jiuzhou Electric commercial → keep personal_community |
| pyspartn / ubx2rinex | KEEP — semuconsulting / nav-solutions community orgs → keep personal_community |
| GNSSommelier | KEEP — already official (EarthScope) — confirmed |
| GREAT-PIFGO / PyLap / pysatSpaceWeather / tec_prediction-ONERA / DeepPredTEC / pyrtklib_demo5 / KF-GINS-Py / ionosonde_volgatech / GNSSR_MERRByS_Python / Ionort-raytrace / GIRAS-GPS-Solutions / HPRTK / salsa | KEEP — already academic_lab — confirmed |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **11** → academic_lab; **28** spot-audits kept/confirmed
- Chinese rewrites: **35** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **39**
- `project_count` unchanged by this QC: **830**
- `lists/*.md` surgically synced (01–07); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | rt-clk-service | provenance; personal_community→academic_lab; DoubleString bio Ph.D candidate Wuhan University |
| 2 | `provenance` | IonoTomo | provenance; personal_community→academic_lab; Joshuaalbert company Caltech; bio radio interferometry researcher |
| 3 | `provenance` | Ionospheric-Scintillation-Maps-and-PDOP | provenance; personal_community→academic_lab; AlexandraKoulouri company Tampere University |
| 4 | `provenance` | COSMIC-IONPRF-Ne-TEC | provenance; personal_community→academic_lab; HassanNooreldeen company Egyptian Space Agency; bio Space Weather researcher |
| 5 | `provenance` | ED-AttConvLSTM | provenance; personal_community→academic_lab; leeliangchao company China University of Geosciences (Beijing); bio Ph.D Student |
| 6 | `provenance` | GPSL1-MMT-DPEmodule | provenance; personal_community→academic_lab; Sergio-Vicenzo company The Hong Kong Polytechnic University; bio PhD student |
| 7 | `provenance` | ionotec | provenance; personal_community→academic_lab; sylvathle company European Space Agency; bio Research Fellow space radiations |
| 8 | `provenance` | scintill-ai | provenance; personal_community→academic_lab; viventriglia company @INGV |
| 9 | `provenance` | NearRealTimeGNSSIR | provenance; personal_community→academic_lab; cemalialtuntas company Yildiz Technical University; bio Researcher GNSS-IR |
| 10 | `provenance` | Ionospheric-TEC-ROTI-Interactives | provenance; personal_community→academic_lab; Tesfay-Tesfu company UNIVAP, NASA; bio Space Physics PhD |
| 11 | `provenance` | Smart-UAV-Return-GNSS-Station | provenance; personal_community→academic_lab; citec-spbu org (St Petersburg University CITEC) |
| 12 | `rewrite_zh` | tec_prediction-ONERA | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | GNSSR_MERRByS_Python | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | sidereon | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | GREAT-PIFGO | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | gnatss | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | HPRTK | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | Ionort-raytrace | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | GNSS-REFLECTOMETRY-PROCESSING | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | INX_Editor | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | pygnss-tec | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | SuperSID | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | gps-sdr-simulink | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | GNSSommelier | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | QuadSPP | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | RAIM_PANG_NAV | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | gnss-rcv | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | PyLap | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | pysatSpaceWeather | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | salsa | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | gnssrlowcost | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | GDDS | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | pyrtklib_demo5 | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | DeepPredTEC | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | ionosonde_volgatech | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | KF-GINS-Py | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | GIRAS-GPS-Solutions | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | rt-clk-service | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | IonoTomo | one_liner_zh, desc_zh; short human Chinese QC |
| 40 | `rewrite_zh` | pyspartn | one_liner_zh, desc_zh; short human Chinese QC |
| 41 | `rewrite_zh` | ubx2rinex | one_liner_zh, desc_zh; short human Chinese QC |
| 42 | `rewrite_zh` | ED-AttConvLSTM | one_liner_zh, desc_zh; short human Chinese QC |
| 43 | `rewrite_zh` | GPSL1-MMT-DPEmodule | one_liner_zh, desc_zh; short human Chinese QC |
| 44 | `rewrite_zh` | scintill-ai | one_liner_zh, desc_zh; short human Chinese QC |
| 45 | `rewrite_zh` | NearRealTimeGNSSIR | one_liner_zh, desc_zh; short human Chinese QC |
| 46 | `rewrite_zh` | ionotec | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: DeepPredTEC, ED-AttConvLSTM, GDDS, GIRAS-GPS-Solutions, GNSS-REFLECTOMETRY-PROCESSING, GNSSR_MERRByS_Python, GNSSommelier, GPSL1-MMT-DPEmodule, GREAT-PIFGO, HPRTK, INX_Editor, IonoTomo, Ionort-raytrace, KF-GINS-Py, NearRealTimeGNSSIR, PyLap, QuadSPP, RAIM_PANG_NAV, SuperSID, gnatss, gnss-rcv, gnssrlowcost, gps-sdr-simulink, ionosonde_volgatech, ionotec, pygnss-tec, pyrtklib_demo5, pysatSpaceWeather, pyspartn, rt-clk-service, salsa, scintill-ai, sidereon, tec_prediction-ONERA, ubx2rinex

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch13.json`.
Keep audits: `research/_qc_batch13_prov_keep.json`.

## Counts after sync
- `project_count`: **830**
- `counts_by_category`: `{"ionosphere": 244, "troposphere": 39, "gnss-data": 120, "gnss-positioning": 95, "orbit-clock": 16, "navigation-ins": 63, "gnss-sdr": 62, "mobile-apps": 22, "tools-learning": 44, "gnss-datasets": 125}`
- `provenance_counts`: `{"official": 236, "academic_lab": 309, "personal_community": 285}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **296**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 14)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈296) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: GNSSPositioning / multi-channel-gnss / SbfParser / GVINS-WHU / rinexmod / RTK / Alouette_ISIS_extract / ionosphereAI / POLAN / MCOSB / gnssr-synth / pwv_kpno / READ_GNSS / uNavTools / mrtklib-docker-ui / csonde-gnss-ionosphere / PyRayHF / tidd / Swarm_notebooks / DDM-Former / crz2rnx / gnss-sdr-rs.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
