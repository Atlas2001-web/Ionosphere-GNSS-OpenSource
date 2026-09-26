# QC audit — 2026-09-26 batch 48 (fact audit idx 401–750)

Base: origin/main `d28347a` (batch 47). Catalog **1029 → 1029** (no adds, no removals, RETIRED_URLS unchanged).
Provenance official/academic_lab/personal_community **333/237/459 → 333/237/459** (unchanged; provenance for idx ≥ 401 was swept in batch 45 and is not re-litigated here).
Evidence read 2026-09-26 ~03:55–04:40 ET via `gh api graphql` (archived/fork/pushedAt/licence/language), `gh api repos/X/Y/readme`, `users/X`, `contents`.

## Task 0 — entries newer than d28347a
None: HEAD = origin/main = d28347a at start, `project_count` 1029, nothing appended.

## Task 1 — fact audit idx 401–750

### Bulk metadata (251 GitHub entries)
- Licence: no SPDX mismatch between catalog and GitHub.
- Archived repos without a dated note → note added to analysis_zh "仓库已于 YYYY-MM 归档（只读）":
  SegmentsComputation (2021-09; replaces English "archived"), gnssIR-python (2020-11), gnssr-synth (2025-03),
  gnssrlowcost (2025-03), ubxlib (2024-11; README: u-blox discontinued the project).
- Forks: NeQuickJRC (text already says community mirror), GREAT-MSF (fork inside GREAT-WHU org), gnssFGO
  (rwth-irt original confirmed archived; text already says so) — no change.
- Language: learning_rtklib `""` → `C++` (C++ RTKLIB examples; GitHub "OpenEdge ABL" is misdetected data).
  Left alone: heuristic mismatches (Fortran-core Python wrappers, notebook-heavy Python, GraphGNSSLib_LEO C/C++),
  zip-only repos (UNB3m, ATom), awesome/notes repos with no code.

### README reads (86 entries) — fixes where README contradicts or the text was vague
Wrong / misleading descriptions:
- **vtec** (mfkiwl): catalog said a narrow STEC→VTEC helper; README is a full C++/LibTorch global SH GIM system with
  DCB estimation, cycle-slip detection, IONEX output → desc/one_liner/analysis rewritten.
- **awesome-gins-datasets** (i2Nav): catalog said a list of public datasets; README is i2Nav's own 1617 s vehicle
  dataset with 4 MEMS IMUs + RTK + truth → desc/one_liner/analysis rewritten.
- **tec-suite**: catalog said it builds regional/global TEC maps; README: reconstructs slant TEC per station/arc
  → desc/one_liner/analysis rewritten.
- **tidd**: analysis said "低轨 GPS / 在轨 GPS TEC"; README: sTEC d/dt from GPS satellites observed by ground
  receivers, TIDs from tsunamis/earthquakes/explosions (JPL/Sapienza/UCLA) → one_liner and analysis fixed.
- **MyIonosphere_Library**: text said "需自备观测读取"; README: reads a RINEX observation directory by time span
  (GPS/Galileo/GLONASS/BeiDou/SBAS) → desc and analysis fixed.
- **PRIDE-GeoDataLogger**: repo holds only APKs (zip contains v2 APK), no source → desc and analysis say so.
- **EasyGNSS** (whigg): desc tied the project to "IGG,CAS" (only the account's profile); README: Raspberry Pi +
  RTKLIB touch GUI based on RTKBase/TouchRTKStation, links to NChebbah/EasyGNSS (404) → desc/analysis rewritten.
- **GINS / GVINS-WHU** (zhangwhu, no README): scene claims ("遮挡环境…") unsupported; now describe repo contents
  (GINS: RTKLIB-derived C + PSINS; GVINS: ic_gvins tree + HKUST gnss_comm).
- **gnssIR-matlab-v3**: analysis said soil moisture; README: "These codes do not calculate soil moisture".
- **cddis-highrate-downloader**: analysis said Earthdata account needed; README: anonymous FTP, no credentials.
- **GPSMilemeterIMUEKFLocation**: README uses iPhone GPS + compass + accelerometer integration instead of an odometer.
- **ignav**: "面向嵌入/固件移植" unsupported → README feature list (loose/tight SPP/PPP/RTK, NHC/ZUPT, Linux only).
- **PyGPS**: README says unmaintained since 2020-08, merged into gsit → note added.
- **Navigation-Learning**: GitHub description now says undergrad notes, no longer updated → desc/analysis.
- **mitiono**: input is Septentrio SBF/NMEA, not generic "GPS 接收机数据".
- **gpssnrpy**: English word "complementary" in analysis → 互补; input RINEX 2.11.
Vague desc_zh made specific (README-based): KOH2-ionosphere, scintill-ai, TEC-calculation-MATLAB (STEC/VTEC/DCB/ROTI),
tec_forecast (next-day GIM, GPS Solut 2023), BDS-3-PPP-B2b_IMU_LiDAR (MSCKF), GREAT-PIFGO (PPP & PPP/INS FGO),
Multi_Sensor_Fusion ("武大 GNSS 中心相关" → thesis-based wording), geodezyx, GNSS-REFLECTOMETRY-PROCESSING (UPC RSLab/MIR DDMs),
learning_rtklib.

Checked OK (no change): mgfernan-pygnss (README lists ionex_diff vs NeQuick), NeQuickJRC, ntcmg, POLAN, pygnss-tec,
pynasonde, PyTECGg, rtcm2ionex, scintkit, Septentrio-PyDataLink, TEC-forecast-F107, TEC-MoLLM, TEC_gradient_computation,
tec_prediction-ONERA, transcar, eagleye, FE-GUT, gici-open (SJTU contact), GLIO, gnss-ins-sim, GNSS_INS_Integrations_Comparisons,
ImuGpsGuiding, imugpslocalization, IndirectEKFIMUGPS, INSTINCT, Loose-GNSS-IMU, NaveGo, RTK-Visual-Inertial-Navigation,
Smart-UAV-Return, TGINS, clkcomb, Gkit-Bias, MCOSB, gnss2tws-green, OSNMA, GIRAS, gnssr-raspberry, NearRealTimeGNSSIR,
pwv_kpno, docker-gnsssdr, msise00, androidGnss, esp32-xbee (README itself says "official firmware" for the Ardusimple device),
gnssFGO, TITIPy, gsit, IGP-TUDelft, GRITI, navsu, GraphGNSSLib_LEO, hwm14, Virtual-Network-DGNSS, lowtran, ICAMS, Cube,
kshana, GNSS_RR, M_ISSION, PPP-RTK-Ionosphere (no README), mosgim etc.

### desc_zh identical to one_liner_zh
Code entries in idx 401–750 (and catalog-wide, non-official_site): **0**. The 12 identical pairs in this range are all
official_site portals (NICT, NOAA, ROB, UWM, GA) and are left as is. Near-identical (desc ⊂ one_liner): SH-GIM (maintainer's
own entry), NTRIPcaster-python, doris-rinex — acceptable, not changed.

## Regeneration / validation
- Pre-edit dry run of merge_routine_20260926c `regenerate_lists/categories/readme`: zero diff. main() not run.
- PROJECTS.json: 50 changed lines (desc_zh 20, analysis_zh 25, one_liner_zh 4, language 1). Lists 01/02/03/06/08/09 changed
  only in the matching one-liner / language / analysis rows. README and categories.md unchanged.
- JSON valid; project_count 1029 = len(projects) = Σcounts_by_category = Σprovenance_counts; no duplicate URLs or names.

## Leftovers
- EasyGNSS may be a re-upload of a deleted NChebbah/EasyGNSS; original not locatable — kept.
- vtec (mfkiwl) README has no author; mfkiwl hosts many copies — original source not found.
- Provenance borderlines from batch 45 (kristinemlarson, cemalialtuntas, AILocAR, TGINS, NaveGo, OSNMA) unchanged.
- idx 751–1028 not yet fact-audited.
