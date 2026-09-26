# QC audit — 2026-09-26 batch 53 (subcategory cleanup: near-duplicate ionosphere pairs, ionosphere/工具, 空间天气辅助, one-entry groups)

Base: `8071230` (batch 52 end; `origin/main` had no newer commits at start). Project total 1029 unchanged; provenance 331/214/484 unchanged; no entries added or removed. The only PROJECTS.json field changed is `subcategory` (78 lines). No move crosses categories, so `counts_by_category` is unchanged.

## Task 0 — entries newer than 8071230

None. HEAD was `origin/main` = `8071230` with a clean tree; nothing to QC.

## Task 1 — near-duplicate ionosphere pairs

- `GIM/球谐映射` (8) + `GIM` (5) → **`GIM`** (13). GIM is the clearer name: the group also holds kriging, Kalman, VLBI-fusion and SBAS VTEC-map code, which are not spherical-harmonic methods.
- `闪烁` (16) + `闪烁/ROTI` (8) → **`闪烁/ROTI`** (23). The clearer name was kept because ROTI tools were split across both groups (igs-roti, Ionospheric-TEC-ROTI-Interactives, roti-gnss-ml were in 闪烁). SuperSID, a VLF SID monitor rather than a scintillation tool, went to `工具` next to the other VLF tools.
- `TEC预报` (5) + `TEC预报/ML` (12) → **`TEC预报/ML`** (16). All four remaining entries are ML/DL forecasters. t-fors, a TID forecaster, went to `TID`.
- `IRI/NeQuick` (9) + `IRI模型` (19) + `NeQuick官方` (3): split into IRI and NeQuick, since each has ≥3 entries.
  - **`IRI模型`** (26): IRI wrappers and ports (iri2016, iri2020, iri90, IRI2020_parameters, PyIRI, FIRI.jl), plus FIRI-2018 from 模型 for consistency with pyFIRI2018 and FIRI.jl.
  - **`NeQuick`** (7): the three official pages (Galileo-NeQuick-G, NeQuick2-ICTP, NeQuickG-ESSR), the three community ports (Nequick-ITUR, NequickG, NeQuickJRC) and NeQuick2-MLF2 from 模型. `NeQuick` replaces `NeQuick官方` because community ports are not official. NTCM-G and Klobuchar stay in 模型.

## Task 1 — ionosphere/工具 (42 → 31)

- New **`雷达/ISR`** (8). The generator groups by free-text subcategory, so no code change was needed.
  - From 工具: pyDARN, SuperDARN RST, LPI, BAFIM, isr-raw, resolvedvelocities.
  - From 模型: MIPS (ISR performance simulator) and inscar (IS spectrum theory). Both are radar-specific, not ionosphere models.
  - DARNtids stays in TID and madrigalWeb in 数据接口.
- `TID` (4 → 7): IonKit-NH (from 工具), tidd (from TEC估计; it detects TIDs and does not estimate TEC), t-fors (from TEC预报).
- `TEC估计`: Get_IPP and MyIonosphere_Library (IPP/GFLC building blocks; sibling gsit).
- `模型`: gcmprocpy, pytiegcm, SAMI3-GITM-python. These are model-output companions of TIE-GCM and SAMI3/GITM (siblings TIE-GCM, sami3_gitm, mat_gemini).
- pysat family (6: pysat, pysatModels, pysatSpaceWeather, pysatNASA, pysatMissions, pysatCDF): **left in 工具**. `数据接口` fits pysatSpaceWeather/pysatCDF/pysatNASA but not pysatModels (model-data comparison) or pysatMissions (mission planning). Splitting the family, or creating a `pysat生态` subcategory, would not clearly improve on the current placement.
- **Boston-College-ISR-Ionospheric-Studies: not moved to 雷达/ISR.** Here "ISR" is Boston College's *Institute for Scientific Research*, not incoherent-scatter radar. The page describes research on scintillation, tomography and GNSS TEC. It stays in 工具 as a leftover.

## Task 1 — gnss-datasets/空间天气辅助 (6) dissolved

The scopes overlap, but by sibling consistency the entries fit 电离层产品 better than 地磁空间天气:
- SuperDARN-VT and FRDR SuperDARN Collection → 电离层产品 (ionospheric radar data; siblings EISCAT Portal, SRI ISR Database).
- OpenMadrigal → 电离层产品 (sibling CEDAR Madrigal).
- NOAA-NGDC-Ionosphere and PITHIA e-Science Centre → 电离层产品 (ionosphere/thermosphere data catalogues; siblings NOAA-NCEI-TEC-Archive, NICT-WDC).
- Meridian Project Data Center → 地磁空间天气 (multi-instrument hub; siblings UKSSDC, NASA-SPDF).

## Task 1 — one-entry groups (46 → 32)

Fourteen one-entry groups were moved into existing siblings; they are marked T4-singleton in the table below.

**The remaining 32 one-entry groups were left** because no sibling clearly fits:
- gnss-data:
  - FAST (下载/处理): download + QC + SPP + station selection.
  - geode (自动化处理): full framework.
  - GNSS-Metadata-Standard (元数据/SDR).
  - gps-measurement-tools (Android原始观测): logger + analysis, not a RINEX converter.
  - azarashi (QZSS-DCR).
- gnss-datasets:
  - BDS-3-PPP-B2b-DATA (PPP-B2b数据) and cssrlib-data (PPP/PPP-RTK样例): sample data; no dataset-sample group exists.
- gnss-positioning:
  - gnss_gpu (城市峡谷), gnss_lib_py (解析/分析), NavAI (多路径AI).
  - pyRTKLib-RINEX (处理/绘图): not an RTKLIB binding, despite the name.
  - libswiftnav (GNSS算法库).
  - GNSS-Correction-RTKLIB (PPK教程): manual/tutorial.
- gnss-sdr: gnss-sdr-monitor (监控).
- navigation-ins: gtsam (因子图库), python-openimu (IMU驱动).
- orbit-clock:
  - cggtts (时间比对): software, whereas the 时标产品 siblings are BIPM portals.
  - CelesTrak-NORAD-GP (轨道根数): data, whereas SGP4传播 holds software.
  - ILRS (SLR).
- tools-learning:
  - GPSBabel (轨迹/航点转换), kshana (PNT仿真), Muf_Muncher (HF传播态势).
  - NGS-ADJUST (网平差), swift-nav-pygnss (Python工具), LINZ-Geodetic-System (基准与框架), NASA-SSCWeb (航天器态势), gpsdo (GPS驯服钟).
- troposphere:
  - GGOS-Tropo-RTKLIB (VMF/GGOS产品): code, whereas VMF产品 holds data directories.
  - GNSS-REFLECTOMETRY-PROCESSING (GNSS-R处理): airborne MIR, not spaceborne.
  - RADIATE (射线追踪/NWM), STD_SWD_Calc (ZTD/ZWD/VMF), gnssvod (GNSS-VOD).

## All moves (78; 0 cross-category)

Per task: T1-GIM 8, T1-IRI 7, T1-NeQuick 7, T1-TEC预报 4, T1-TID 1, T1-闪烁 15, T2-TEC估计 2, T2-TID 2, T2-工具 1, T2-模型 3, T2-雷达/ISR 8, T3-空间天气辅助 6, T4-singleton 14

| idx | name | from | to | task | reason |
|---:|---|---|---|---|---|
| 4 | autorino | gnss-data/接收机下载/RINEX转换 | gnss-data/RINEX转换 | T4-singleton | vendor raw→RINEX conversion; siblings rtcm3torinex, ubx2rinex, trm2rinex-docker |
| 37 | gnsstk-apps | gnss-data/基础库应用 | gnss-data/基础库 | T4-singleton | apps split from GPSTk; siblings gnsstk, GPSTk |
| 154 | Essential-GNSS | gnss-positioning/经典定位库 | gnss-positioning/SPP/RTK/PPP | T4-singleton | C library with LSQ/EKF/RTK post-processing; siblings libgnss++, laika |
| 166 | gnssgo | gnss-positioning/RTKLIB移植 | gnss-positioning/SPP/RTK/PPP | T4-singleton | Go rewrite of RTKLIB 2.4.3; siblings RTKLIB, RTKLIB-explorer |
| 288 | BiScEF | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 296 | DeepPredTEC | ionosphere/TEC预报 | ionosphere/TEC预报/ML | T1-TEC预报 | all remaining TEC预报 entries are ML/DL forecasters; merged into dominant TEC预报/ML |
| 301 | ED-AttConvLSTM | ionosphere/TEC预报 | ionosphere/TEC预报/ML | T1-TEC预报 | all remaining TEC预报 entries are ML/DL forecasters; merged into dominant TEC预报/ML |
| 311 | FARR | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 312 | FIRI-2018 | ionosphere/模型 | ionosphere/IRI模型 | T1-IRI | FIRI-2018 MATLAB; siblings pyFIRI2018 and FIRI.jl now in IRI模型 |
| 313 | FIRI.jl | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 314 | Galileo-NeQuick-G | ionosphere/NeQuick官方 | ionosphere/NeQuick | T1-NeQuick | NeQuick官方 folded into NeQuick with the community ports |
| 316 | gcmprocpy | ionosphere/工具 | ionosphere/模型 | T2-模型 | TIE-GCM/SAMI3-GITM model-output companions; siblings TIE-GCM, sami3_gitm, mat_gemini in 模型 |
| 320 | Get_IPP | ionosphere/工具 | ionosphere/TEC估计 | T2-TEC估计 | IPP/GFLC building blocks of STEC/VTEC estimation; sibling gsit (TEC/ROTI/IPP) |
| 329 | gnss-scintillation-simulator_2-param | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 332 | GNSS.IonosphereMaps | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 340 | IBP-Model | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 341 | igs-roti | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 353 | IonKit-NH | ionosphere/工具 | ionosphere/TID | T2-TID | detects earthquake/tsunami/volcano TIDs from GNSS TEC; TID siblings |
| 367 | ionospheric-scintillation-mitigation | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 370 | Ionospheric-TEC-ROTI-Interactives | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 371 | Ionospheric-VTEC-Forecasting | ionosphere/TEC预报 | ionosphere/TEC预报/ML | T1-TEC预报 | all remaining TEC预报 entries are ML/DL forecasters; merged into dominant TEC预报/ML |
| 387 | iri2016 | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 388 | iri2020 | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 389 | IRI2020_parameters | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 390 | iri90 | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 404 | m_gim-PANXIONG | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 405 | M_GIM-zcytju | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 406 | M_ISSION | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 411 | mosgim | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 412 | mosgim2 | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 413 | MyIonosphere_Library | ionosphere/工具 | ionosphere/TEC估计 | T2-TEC估计 | IPP/GFLC building blocks of STEC/VTEC estimation; sibling gsit (TEC/ROTI/IPP) |
| 414 | Nequick-ITUR | ionosphere/IRI/NeQuick | ionosphere/NeQuick | T1-NeQuick | NeQuick implementations split from IRI (≥3 each); new NeQuick replaces NeQuick官方 (community ports are not official) |
| 415 | NeQuick2-ICTP | ionosphere/NeQuick官方 | ionosphere/NeQuick | T1-NeQuick | NeQuick官方 folded into NeQuick with the community ports |
| 416 | NeQuick2-MLF2 | ionosphere/模型 | ionosphere/NeQuick | T1-NeQuick | NeQuick-G rewrite; NeQuick-specific |
| 417 | NequickG | ionosphere/IRI/NeQuick | ionosphere/NeQuick | T1-NeQuick | NeQuick implementations split from IRI (≥3 each); new NeQuick replaces NeQuick官方 (community ports are not official) |
| 418 | NeQuickG-ESSR | ionosphere/NeQuick官方 | ionosphere/NeQuick | T1-NeQuick | NeQuick官方 folded into NeQuick with the community ports |
| 419 | NeQuickJRC | ionosphere/IRI/NeQuick | ionosphere/NeQuick | T1-NeQuick | NeQuick implementations split from IRI (≥3 each); new NeQuick replaces NeQuick官方 (community ports are not official) |
| 439 | PyIRI | ionosphere/IRI/NeQuick | ionosphere/IRI模型 | T1-IRI | IRI wrappers/ports merged into dominant IRI模型 (siblings pyIRI2016, iricore, pyFIRI2018) |
| 450 | pytiegcm | ionosphere/工具 | ionosphere/模型 | T2-模型 | TIE-GCM/SAMI3-GITM model-output companions; siblings TIE-GCM, sami3_gitm, mat_gemini in 模型 |
| 454 | real-time-ionospheric-maps-Kalman | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 459 | roti-gnss-ml | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 466 | SAMI3-GITM-python | ionosphere/工具 | ionosphere/模型 | T2-模型 | TIE-GCM/SAMI3-GITM model-output companions; siblings TIE-GCM, sami3_gitm, mat_gemini in 模型 |
| 470 | SbfParser | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 472 | scintkit | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 473 | ScintPi-1.0-Software | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 477 | SH-GIM | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 480 | SuperSID | ionosphere/闪烁 | ionosphere/工具 | T2-工具 | VLF sudden-ionospheric-disturbance monitor, not scintillation; VLF siblings SubionosphericVLFInversionAlgorithms.jl, nleht-fdtd in 工具 |
| 481 | Swarm-VIP-Dynamic | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 484 | t-fors | ionosphere/TEC预报 | ionosphere/TID | T1-TID | TID forecasting component; sibling TID tools DARNtids, lstid_processing |
| 491 | tec_forecast | ionosphere/TEC预报 | ionosphere/TEC预报/ML | T1-TEC预报 | all remaining TEC预报 entries are ML/DL forecasters; merged into dominant TEC预报/ML |
| 494 | tidd | ionosphere/TEC估计 | ionosphere/TID | T2-TID | sTEC-rate anomaly detection of TIDs; TID siblings (detector, not TEC estimation) |
| 503 | Zenodo-VTEC-map-generation-SBAS | ionosphere/GIM/球谐映射 | ionosphere/GIM | T1-GIM | GIM pair merged into clearer general name GIM (group also holds kriging/Kalman/VLBI-fusion/SBAS VTEC maps, not only spherical harmonics) |
| 556 | raw-gnss-fusion | navigation-ins/原始GNSS融合 | navigation-ins/多传感器融合 | T4-singleton | raw GNSS multi-sensor fusion research code; siblings MINS, GLIO |
| 583 | earth-gravitational-model | tools-learning/高程/大地水准面 | tools-learning/坐标转换 | T4-singleton | ellipsoid→geoid height conversion; sibling VDATUM |
| 593 | ion_gnss25_fg_code_examples | tools-learning/因子图教程 | tools-learning/课程笔记 | T4-singleton | tutorial code; siblings gnss_tutorials, DD-cycle-slip-lab |
| 605 | Swarm_notebooks | tools-learning/SWARM教程 | tools-learning/课程笔记 | T4-singleton | tutorial Jupyter notebooks; sibling gnss_tutorials |
| 681 | SuperDARN-VT | gnss-datasets/空间天气辅助 | gnss-datasets/电离层产品 | T3-空间天气辅助 | ionospheric radar data portal; siblings EISCAT Portal, SRI ISR Database (AMISR) |
| 682 | OpenMadrigal | gnss-datasets/空间天气辅助 | gnss-datasets/电离层产品 | T3-空间天气辅助 | Madrigal project page; sibling CEDAR Madrigal |
| 693 | gnssFGO | navigation-ins/因子图融合 | navigation-ins/多传感器融合 | T4-singleton | FGO fusion of GNSS with LiDAR/visual odometry; siblings GLIO, MINS, libRSF |
| 734 | NOAA-NGDC-Ionosphere | gnss-datasets/空间天气辅助 | gnss-datasets/电离层产品 | T3-空间天气辅助 | ionosphere(-thermosphere) data catalogue; siblings NOAA-NCEI-TEC-Archive, NICT-WDC-Ionosphere-SpaceWeather |
| 753 | gnss-vector-scintillation | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 837 | IGS-Bias-Calibration-WG | orbit-clock/偏差与校准 | orbit-clock/产品门户 | T4-singleton | bias product entry page; siblings CDDIS-Orbit-Clock-Products, ESA-Navigation-Support-Office |
| 838 | IGS-Multi-GNSS-WG | gnss-datasets/多系统扩展 | gnss-datasets/IGS综合 | T4-singleton | IGS organisation page; siblings IGS-Home, IGS-Data-Access |
| 840 | IGS-Reference-Frame-WG | gnss-datasets/参考框架 | gnss-datasets/坐标产品 | T4-singleton | station coordinates/frame WG (topic placement like IGS-Ionosphere-WG); siblings EUREF-EPN-Coordinates, UNR-NGL |
| 890 | ESA-Satellite-Navigation | tools-learning/ESA导航 | tools-learning/机构软件门户 | T4-singleton | agency navigation portal; siblings GPS.gov, ISRO-IRNSS-NavIC, USCG-NAVCEN |
| 917 | UNR-GPSNetMap | gnss-datasets/测站地图 | gnss-datasets/坐标产品 | T4-singleton | UNR NGL station map; sibling UNR-NGL |
| 990 | saga-utils | ionosphere/闪烁 | ionosphere/闪烁/ROTI | T1-闪烁 | scintillation pair merged into clearer 闪烁/ROTI (ROTI tools such as igs-roti, TEC-ROTI-Interactives, roti-gnss-ml sat in 闪烁) |
| 994 | Meridian Project Data Center | gnss-datasets/空间天气辅助 | gnss-datasets/地磁空间天气 | T3-空间天气辅助 | multi-instrument space-environment hub (magnetometers, lidar, radars, ionosondes); siblings UKSSDC, NASA-SPDF |
| 996 | FRDR SuperDARN Collection | gnss-datasets/空间天气辅助 | gnss-datasets/电离层产品 | T3-空间天气辅助 | ionospheric radar data portal; siblings EISCAT Portal, SRI ISR Database (AMISR) |
| 997 | PITHIA e-Science Centre | gnss-datasets/空间天气辅助 | gnss-datasets/电离层产品 | T3-空间天气辅助 | ionosphere(-thermosphere) data catalogue; siblings NOAA-NCEI-TEC-Archive, NICT-WDC-Ionosphere-SpaceWeather |
| 998 | pyDARN | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |
| 999 | SuperDARN RST | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |
| 1002 | LPI | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |
| 1003 | inscar | ionosphere/模型 | ionosphere/雷达/ISR | T2-雷达/ISR | ISR system simulator / IS spectrum theory library, radar-specific rather than ionosphere models; siblings LPI, BAFIM, isr-raw |
| 1014 | resolvedvelocities | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |
| 1015 | MIPS | ionosphere/模型 | ionosphere/雷达/ISR | T2-雷达/ISR | ISR system simulator / IS spectrum theory library, radar-specific rather than ionosphere models; siblings LPI, BAFIM, isr-raw |
| 1016 | BAFIM | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |
| 1018 | isr-raw | ionosphere/工具 | ionosphere/雷达/ISR | T2-雷达/ISR | SuperDARN/incoherent-scatter radar software; new 雷达/ISR (8 entries) |

## Counts

Category counts are unchanged: ionosphere 247, gnss-datasets 220, gnss-data 137, gnss-positioning 108, gnss-sdr 76, navigation-ins 72, tools-learning 58, troposphere 48, mobile-apps 32, orbit-clock 31; total 1029.

(category, subcategory) groups go from 175 to 157, and one-entry groups from 46 to 32. ionosphere subcategories go from 21 to 18; gnss-datasets from 23 to 19.

## Regeneration and checks

- A dry run of `merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme` on the untouched data gave a zero diff. The same functions were run again after the edits.
- PROJECTS.json is valid JSON in the canonical dump format. The diff touches only 78 `subcategory` lines.
- In the lists, the multiset of row and detail lines is identical before and after; entries only moved between groups. Section headers changed only for the merged, created and removed subcategories. README and docs/categories.md did not change because the counts did not change.
- All 10 list files have header count equal to row count. Every URL appears exactly once across the lists (1029 rows, the same set as PROJECTS.json). project_count is 1029 and provenance is 331/214/484.

## Leftovers

- Boston-College-ISR-Ionospheric-Studies is still in ionosphere/工具 (research-group page; ISR = Institute for Scientific Research).
- ionosphere/工具 (31) still contains:
  - the pysat family (6);
  - Faraday-rotation/radio-astronomy TEC tools: spinifex, RMextract, ionFR (ALBUS_ionosphere sits in TEC估计);
  - occultation tools COSMIC-IONPRF-Ne-TEC and IonOccAnalysis. With CDAAC_COSMIC-TEC (in TEC估计) these would give a possible 3-entry ionosphere `掩星` group;
  - coordinate libraries apexpy and ocbpy, while aacgmv2 sits in 模型.
- The 32 one-entry groups listed above remain.
