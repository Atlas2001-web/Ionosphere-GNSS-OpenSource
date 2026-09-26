# QC audit — 2026-09-26 batch 45 (vendor/company provenance policy, academic_lab-on-personal-account sweep idx 401+)

Base: origin/main 0a8a23a (batch 44). Catalog **1029 → 1029** (no adds, no removals). Evidence read 2026-09-26 ~03:40–04:10 ET via `gh api users/X` / `orgs` (461 GitHub owners) and `gh api repos/X/Y/readme` (116 READMEs).

## Task 0 — entries newer than batch 44
None. HEAD = origin/main = 0a8a23a, `project_count` 1029, and nothing was appended after batch 44.

## Task 1 — written company policy (docs/categories.md lines 13–15)
The written policy says company open-source releases are `personal_community` (公司开源档). `official` is for government agencies, national labs, international or non-profit consortia and official service sites. The doc itself is unchanged.

Official → personal_community (9):

| idx | project | org evidence (`gh api users/X`: name / blog / description) | before | after |
|---|---|---|---|---|
| 39 | gps-measurement-tools | google: "Google" / opensource.google / "Google ❤️ Open Source" | official | personal_community |
| 80 | septentrio_gnss_driver | septentrio-gnss: "Septentrio" / septentrio.com / "Leading manufacturer of high-precision GPS/GNSS and INS receivers." | official | personal_community |
| 469 | SbfMixer | septentrio-gnss (same) | official | personal_community |
| 470 | SbfParser | septentrio-gnss (same) | official | personal_community |
| 476 | Septentrio-PyDataLink | septentrio-gnss (same) | official | personal_community |
| 670 | ubxlib | u-blox: "u-blox" / u-blox.com / "u-blox is a Swiss company…" | official | personal_community |
| 864 | novatel_oem7_driver | novatel: "Hexagon \| NovAtel®" / novatel.com | official | personal_community (batch 44 had set official; that is reversed under the written policy) |
| 1020 | novatel_edie | novatel (same) | official | personal_community |
| 1021 | trimble_driver_ros | trimble-oss: "Trimble" / "Trimble Online Source Store" | official | personal_community |

Vendor orgs that were already personal_community and stay that way: swift-nav (6), sparkfun (2), PointOneNav, emlid, Aceinna, fixposition, SkydelSolutions (Safran), LORD-MicroStrain (HBK), Pix4D, MapIV, CS-SI, baidu, commaai, bolderflight, rokubun, swri-robotics and others.

Chinese text that said "官方" for a vendor was changed to factual vendor wording ("厂商发布/厂商开源"):
- Flipped entries: 39 desc and analysis; 80 desc; 470 one_liner and analysis; 670 desc, one_liner and analysis; 864 one_liner and analysis; 1020 one_liner and analysis; 1021 one_liner and analysis.
- Entries that were already personal_community: polaris (603), libsbp (656), swiftnav-ros2 (869), fixposition_driver (881), and novatel_gps_driver (865, which calls the NovAtel OEM7 driver "官方").

Kept official (government, national lab or consortium): nasa, NCAR (NSF NCAR/UCAR), noaa-ngs, NOAA-SWPC, GeoscienceAustralia, nlsfi, kartverket, asc-csa, QZSS-Strategy-Office, USNavalResearchLaboratory, NRL-Plasma-Physics-Division, EarthScope (GitHub and GitLab), KNMI-OSS, ESA-VirES, Swarm-DISC, lofar-astron (ASTRON), IAGA-VMOD, embrace-inpe, amisr, SPEDAS, SWMFsoftware, IonMetadataWorkingGroup, jaxa-snu.

## Task 2 — academic_lab on personal (User) GitHub accounts
Scope: 106 GitHub entries at idx ≥ 401 that are academic_lab and whose owner is `type == User`. Rule: keep academic_lab only when the README clearly names a university lab or group releasing the code. Otherwise flip to personal_community.

### Flipped academic_lab → personal_community (54, idx ≥ 401)
| idx | project | owner (users/X) | README evidence |
|---|---|---|---|
| 402 | KOH2-ionosphere | asparuhkamburov (—; no company) | no lab/group named |
| 403 | LongwaveModePropagator.jl | fgasdia (Forrest Gasdia; no company) | no lab/group named |
| 404 | m_gim-PANXIONG | PANXIONG-CN (Pan Xiong; Tsinghua University) | no lab/group named |
| 410 | mitiono | sabrinastronomy (Sabrina Berger-Marcelo; no company) | no lab/group named |
| 428 | OASIS | giorgiopicanco (giorgiopicanco; no company) | no lab/group named |
| 439 | PyIRI | victoriyaforsythe (Victoriya V. Forsythe; no company) | no lab/group named |
| 441 | PyIRTAM | victoriyaforsythe (Victoriya V. Forsythe; no company) | no lab/group named |
| 443 | pynasonde | shibaji7 (Shibaji Chakraborty; ERAU) | no lab/group named |
| 445 | PyRayHF | victoriyaforsythe (Victoriya V. Forsythe; no company) | no lab/group named |
| 449 | PyTECGg | viventriglia (Vincenzo Ventriglia; @INGV) | no lab/group named |
| 454 | real-time-ionospheric-maps-Kalman | AlexandraKoulouri (Alexandra Koulouri; Tampere University) | no lab/group named |
| 463 | SAMI3-3.22-CCMC-mirror | sylee918 (Sang-Yun Lee; @NASA/GSFC @CUA) | no lab/group named |
| 466 | SAMI3-GITM-python | abukowski21 (Aaron Bukowski; no company) | no lab/group named |
| 471 | scintill-ai | viventriglia (Vincenzo Ventriglia; @INGV) | no lab/group named |
| 479 | SubionosphericVLFInversionAlgorithms.jl | fgasdia (Forrest Gasdia; no company) | no lab/group named |
| 484 | t-fors | viventriglia (Vincenzo Ventriglia; @INGV) | no lab/group named |
| 487 | TEC-forecast-F107 | hekaixuan-atm (—; no company) | no lab/group named |
| 488 | TEC-MoLLM | PANXIONG-CN (Pan Xiong; Tsinghua University) | no lab/group named |
| 518 | FE-GUT | zhaoqj23 (Qijia Zhao; Tsinghua University) | no lab/group named |
| 521 | GINS | zhangwhu (zhuh; no company) | no lab/group named |
| 529 | GPSMilemeterIMUEKFLocation | gilbertz (Zhao Guoqi; Shanghai Jiao Tong University) | no lab/group named |
| 535 | GVINS-WHU | zhangwhu (zhuh; no company) | no lab/group named |
| 540 | ImuGpsGuiding | JackJu-HIT (鞠柏贤; HIT) | no lab/group named |
| 541 | imugpslocalization | ydsf16 (ydsf16; BUAA) | no lab/group named |
| 542 | IndirectEKFIMUGPS | hgpvision (hgpvision; Harbin Institute of Technology) | no lab/group named |
| 547 | KF-GINS-Py | salmoshu (Winchell Hu; no company) | no lab/group named |
| 549 | Loose-GNSS-IMU | aaronboda24 (Aaron Boda; York University) | no lab/group named |
| 556 | raw-gnss-fusion | JonasBchrt (Jonas Beuchert; UK Centre for Ecology & Hydrology; Cardiff University) | no lab/group named |
| 557 | RTK-Visual-Inertial-Navigation | xiaohong-huang (xiaohonghuang; South China University of Technology) | no lab/group named |
| 559 | salsa | yxw027 (—; no company) | no lab/group named |
| 572 | Gkit-Bias | LiZhengXiao99 (李郑骁; 长安大学硕士研究生) | no lab/group named |
| 578 | rt-clk-service | DoubleString (JunTao; no company) | no lab/group named |
| 584 | EasyGNSS | whigg (—; IGG,CAS) | no lab/group named |
| 589 | gnss2tws-green | jzshhh (Zhongshan Jiang; Sun Yat-Sen University) | no lab/group named |
| 597 | Navigation-Learning | LiZhengXiao99 (李郑骁; 长安大学硕士研究生) | no lab/group named |
| 604 | RTKLIB-Manual-CN | salmoshu (Winchell Hu; no company) | no lab/group named |
| 609 | DDM-Former | daixinzhao (DZ; no company) | no lab/group named |
| 615 | GNSS_RR | lasteine (—; no company) | no lab/group named |
| 620 | gnssr4river | lroineau (—; ANCT) | no lab/group named |
| 626 | ICAMS | ymcmrs (Yunmeng Cao; Central South University) | no lab/group named |
| 639 | VARION | giorgiosavastano (Giorgio Savastano; no company) | no lab/group named |
| 640 | Cube | liush18 (—; no company) | no lab/group named |
| 643 | geoveil-mp | miluta7 (Miluță Flueraș; National CEnter for Cartography) | no lab/group named |
| 644 | geoveil-cn0 | miluta7 (Miluță Flueraș; National CEnter for Cartography) | no lab/group named |
| 690 | grinq | PJarrin (Paul Jarrin; Géoazur, IRD) | no lab/group named |
| 718 | gnss_timeseries_viewers | kmaterna (—; no company) | no lab/group named |
| 736 | ocbpy | aburrell (Angeline Burrell; Naval Research Laboratory) | no lab/group named |
| 775 | snapshot-gnss-algorithms | JonasBchrt (Jonas Beuchert; UK Centre for Ecology & Hydrology; Cardiff University) | no lab/group named |
| 818 | aacgmv2 | aburrell (Angeline Burrell; Naval Research Laboratory) | no lab/group named |
| 820 | DD-cycle-slip-lab | VimsRocz (—; no company) | no lab/group named |
| 866 | max2771_fx2lp | jmfriedt (Jean-Michel Friedt; FEMTO-ST) | no lab/group named |
| 984 | GTrop | sun1753814280 (—; no company) | no lab/group named |
| 985 | Mapping-Function-Height-Correction-Models | Sardingfish (Jason Ding; PolyU) | no lab/group named |
| 986 | TropDS | Sardingfish (Jason Ding; PolyU) | no lab/group named |

Notes on README content: OASIS says "Developed by Giorgio Picanço (Ph.D.)". grinq says "implemented by Paul Jarrin". gnssr4river names only author Lubin Roineau. KOH2-ionosphere CITATION.cff lists only A. Kamburov. GINS and GVINS (zhangwhu) and SAMI3 (sylee918, a personal mirror of the NRL/CCMC code) have no README. t-fors names an EU Horizon project, not a university lab. The PyIRI, PyIRTAM and PyRayHF READMEs name no institution.

Text that implied an institutional release was reworded to name the individual. The affiliation stays in brackets where the profile states it:
- desc_zh: 443, 449, 488, 518, 521, 529, 540, 541, 542, 549, 556, 557, 572, 584, 589, 597.
- one_liner_zh: 535 (drops "武大方向"), 639 (drops "Sapienza"), 640 (drops "精密测量院", which the README does not support).
- analysis_zh: 639 VARION ("罗马一大开源" → Savastano personal repo, method from Sapienza papers); 718 ("伯克利相关维护者" → kmaterna).

### Owner-consistency extension (9, idx < 401)
After the flips above, 10 owners had mixed provenance, because their idx < 401 entries were still academic_lab. The same README check was applied to those entries. None of them names a lab, so they were flipped. The exception is TMBOC/SoftGNSS: its README names the "School of Aeronautics & Astronautics, Shanghai Jiao Tong University", so it stays academic_lab, and TMBOC's Robust-GNSS-FG-GMM-TD (804) was kept academic_lab to match. 366's desc "Tampere 研究代码" → "Tampere 研究者个人仓代码".

| idx | project | owner | README |
|---|---|---|---|
| 71 | RinexReader | aaronboda24 (Aaron Boda; York University) | no lab/group named |
| 105 | cssrlib-data | hirokawa (Rui Hirokawa; no company) | no lab/group named |
| 201 | PPPLib | yxw027 (—; no company) | no lab/group named |
| 280 | AETHER | LiZhengXiao99 (李郑骁; 长安大学硕士研究生) | no lab/group named |
| 284 | apexpy | aburrell (Angeline Burrell; Naval Research Laboratory) | no lab/group named |
| 313 | FIRI.jl | fgasdia (Forrest Gasdia; no company) | no lab/group named |
| 339 | hfpytrace | shibaji7 (Shibaji Chakraborty; ERAU) | no lab/group named |
| 345 | Ion-Phys-Toolkit | PANXIONG-CN (Pan Xiong; Tsinghua University) | no lab/group named |
| 366 | Ionospheric-Scintillation-Maps-and-PDOP | AlexandraKoulouri (Alexandra Koulouri; Tampere University) | no lab/group named |

After this, there are 0 GitHub owners with mixed provenance.

### Kept academic_lab: the README names the lab or institute
- PMGC-SimVP: CAS AIR / UCAS affiliation in the licence section.
- cssrg-kmitl ×3: CSSRG Laboratory, KMITL. The account is the lab.
- tec_prediction: ONERA DELTA project.
- tidd: JPL / Sapienza / UCLA collaboration.
- PRIDE-GeoDataLogger: Pride Lab, WHU.
- GLIO and GNSS_INS_Integrations_Comparisons: IPNL PolyU.
- GraphGNSSLib_LEO: TAS Lab PolyU.
- gici-open: SJTU author list and contact.
- Multi_Sensor_Fusion: WHU thesis.
- clkcomb: WHU repro3.
- GIRAS: Yildiz Technical University.
- ATom: TU Wien dissertation.
- docker-gnsssdr: © CTTC.
- gnssFGO: RWTH IRT.
- TITIPy: INGV / ESA INTENS.
- GRITI: NSF grant to Penn State.
- Virtual-Network-DGNSS: © UC Regents.
- J-kroeger ×4: IfE, Leibniz University Hannover.
- GMR-Water: CUMTB team contact.
- MCOSB: GCC group account; same precedent as B2bLIB in batch 44.

### Borderline, kept academic_lab (reported, not changed)
- **kristinemlarson** (gnssrefl, gnssIR_matlab_v3, gnssIR_python, gpssnrpy, FresnelMaps, FindSnowOutliers, gnssSNR, gpsonlySNR). Only gnssSNR and gpsonlySNR are signed "Kristine M. Larson, University of Colorado". The others give no affiliation; gnssrefl names University of Bonn / NASA support. Kept as one owner group.
- **cemalialtuntas**: NearRealTimeGNSSIR and cddis-highrate-downloader follow the GIRAS README (Yildiz TU).
- **AILocAR** ×4 (androidGnss, PrNet, E2EPrNet, NeRC): the account reads like a group, but the READMEs name no lab (paper authors Weng and Ling).
- **DTUSWx**/gnss-vector-scintillation: account name suggests DTU Space Weather; README names none.
- **w2naf**/DARNtids: migrated to w2naf-academia; README names no lab. Kept consistent with w2naf/IRI_TID (idx 391).
- **Academic e-mail or thesis in README, but no lab named**: ilkkavir ×2 (oulu.fi contact), inscar (UiT thesis), OSNMA (kuleuven.be contact, FWO funding), NaveGo (utn.edu.ar contact), TGINS (author's department at AUST), lompe (Trond Mohn / Research Council funding), OpATOM (docs on gpsmet.geod.bme.hu), ChaosMagPy (DTU Space CHAOS model; README is minimal).

### Personal_community under a university org → academic_lab?
None with high confidence. Borderline: **oscimp** (OscillatorIMP, a French PIA research-infrastructure project hosted at FEMTO-ST) is still personal_community.

### Other borderline items (not changed)
- **esa/dSGP4** (913): academic_lab under the ESA org. Under the written policy it could be official.
- **FrontierDevelopmentLab**/IonCast (346) and **spaceml-org**/ionopy (360): academic_lab. FDL is a public–private research programme with NASA/ESA.
- **ros-drivers** (nmea_msgs 47, nmea_navsat_driver 893): official, but this is a ROS community SIG, not a government or consortium body.
- **IRI-MATLAB-FileExchange** (385): official because irimodel.org links to it, but it is an individual upload (Drew Compston) on MathWorks.
- **celestrak.org** ×2: official. CelesTrak is run by T.S. Kelso.

## Generator dry run (important)
`python3 research/merge_routine_20260926c.py` is **not a no-op** on the current tree. Its finds file re-applies `provenance: academic_lab` to smartphone-gnss-booster (taroz), which undoes an earlier QC fix. It wrote PROJECTS.json, README.md and lists/08, and those writes were reverted immediately. Regeneration therefore used its `regenerate_lists` / `regenerate_categories` / `regenerate_readme` functions directly. Before edits that produced zero diff, and after edits it is idempotent. Do not rerun that script's `main()` without first fixing routine_finds_20260926c.json.

## Validation
- JSON valid. project_count 1029 = len(projects) = Σcounts_by_category = Σprovenance_counts. No duplicate URLs or names.
- counts_by_category unchanged: {ionosphere 298, troposphere 49, gnss-data 138, gnss-positioning 106, orbit-clock 31, navigation-ins 73, gnss-sdr 76, mobile-apps 32, tools-learning 57, gnss-datasets 169}.
- PROJECTS.json diff: provenance ×72, desc_zh ×20, one_liner_zh ×9, analysis_zh ×13, provenance_counts. Lists 01–10 changed only in badge and text rows, plus the README provenance line. categories.md is unchanged.
- provenance (official / academic_lab / personal_community): **342 / 347 / 340 → 333 / 284 / 412**.

## Leftovers
- The borderline items above need a policy call on individual researchers whose affiliation appears only in their profile or e-mail.
- The routine_finds_20260926c.json re-apply problem described in the generator section.
- idx < 401 academic_lab User-account entries from owners with no idx ≥ 401 entry were not re-swept. Batch 44 sampled them.
