# QC audit — 2026-09-26 batch 49 (fact audit idx 751–1028; EasyGNSS provenance note)

Base: origin/main `5502c35` (batch 48). Catalog **1029 → 1029**. No projects added or removed, and RETIRED_URLS is unchanged.
Provenance official/academic_lab/personal_community **333/237/459 → 332/238/459** (one change, see below).
Evidence read 2026-09-26 ~04:00–05:00 ET: `gh api graphql` (archived, archivedAt, fork, pushedAt, licence, language) for all 152 GitHub
entries in range, `gh api repos/X/Y/readme` (152 READMEs fetched, ~85 read for this audit), `contents`/`git/trees`/`languages`/`commits`, and `users/X` for 34 owners.
The NRCan TRX page was read via WebFetch, and HTTP/HTTPS was checked with curl.

## Task 0: entries newer than 5502c35
None. At the start HEAD = origin/main = 5502c35, `project_count` was 1029 and nothing had been appended.

## Task 1: fact audit idx 751–1028 (278 entries: 152 GitHub, 126 official_site)

### Bulk metadata (152 GitHub entries)
- **Licence:** there is no real mismatch. The 14 entries GitHub reports as NOASSERTION were checked against their LICENSE files and match the catalog:
  OKVIS2-X BSD-3, J-kroeger ×4 GPL-3.0, PocketSDR-AFS BSD-2, qzsl6tool BSD-2, AlouetteApp MIT, dvoacap-python MIT, ChaosMagPy MIT,
  MIPS BSD-2, AeroRust nmea Apache-2.0, SparkFun Unicore MIT for code, and wmm2020 public domain (US Gov).
- **Archived repos:** each now carries a dated note "仓库已于 YYYY-MM 归档（只读）" in analysis_zh:
  hwm93 (2022-08, which had no note before; the note that it needs a Fortran compiler/f2py was added too), LimeGPS (2025-01), pluto-gps-sim (2021-03),
  bladeGPS (2025-01) and pynex (2021-07). The last four replace the English word "archived".
- **Forks:** none in this range.
- **Language:** two changes, both with strong evidence.
  - Robust-GNSS-FG-GMM-TD: `MATLAB` → `C++`. The code is modified GTSAM/GPSTk C++ plus C++ examples, and MATLAB is used only for plots. GitHub shows "Shell" because 3rdparty/ is excluded.
  - SoftGNSS-octave: `Objective-C` → `MATLAB`. All files are Octave .m files, which GitHub misdetects.
  - Left as they are: PrNet (GitHub's MATLAB count comes from a bundled GNSS_opensource_software folder, and the package is Python), Python wrappers over Fortran/C
    (igrf, wmm2020, aacgmv2, NCAR-GLOW, pysatCDF, tudatpy), libswiftnav (GitHub says "Pawn", which is misdetected), gpsdo (Arduino = C++), and
    NeRC (no code yet; see below).

### README reads: wrong or misleading descriptions fixed
- **gsdc2023** (taroz): desc and one_liner said "十米级", but it is the Smartphone *Decimeter* Challenge. Now says 分米级, and gives the README facts
  (GTSAM FGO GNSS+IMU, public 1st / private 2nd, depends on gtsam_gnss).
- **positional**: said it shows satellite information. The README only covers location, compass and solar times → desc, one_liner and analysis rewritten.
- **NeRC** (AILocAR): the README title says "Coming Soon", and the repo holds only a README and a conda env file. The text now says the code is not yet released.
  "移动地平线" → 滑动时域 (moving horizon).
- **gal-osnma-sim**: was described as an OSNMA "scenario simulator". It is a gps-sdr-sim-style Galileo E1B/E1C baseband generator for
  HackRF, validated with GSC OSNMA test vectors → rewritten, with the RF-emission caution.
- **go-gnss/spartn**: implied a working SPARTN parser. The README says only frames are implemented, message definitions are TODO and the CRC is untested,
  and there has been no push since 2020-05 → rewritten.
- **NavAI**: "博士课题复现友好" is unsupported. The README says RLNav calls GMV's proprietary Position Engine via ctypes, and MLNav reads that
  engine's offline output, so the project cannot be fully reproduced without it → desc and analysis rewritten.
- **DD-cycle-slip-lab**: the "城市场景/城市环境" claim is not in the README. It is a five-station static GPS network exercise (AdvConc2019.mat).
- **NRCan-TRX**: the analysis said it converts between height systems and used "自然资源部" without a country. TRX actually converts NAD83(CSRS)↔ITRF (up to ITRF2020),
  handles projections and epoch propagation with the NAD83v80VG velocity grid, and does not do vertical datum conversion → desc, one_liner and analysis rewritten.
- **SoftGNSS-octave**: the README says it is a "hackish port" that works only as far as PRN acquisition, and that the fix is untested. This is now noted.
- **gnssSNR**: "RINEX 版本以说明为准" → reads RINEX 2.11 only, with at most 25 observable types (per README).
- **MicroNMEA**: parses only GGA and RMC (per README), which is now stated.
- **python-openimu**: covers the OpenIMU, OpenRTK and INS401 devices, not just the IMU.
- **gnssvod**: needs a pair of receivers (above and below the canopy). The author is Vincent Humphrey (MeteoSwiss).
- **GraphGNSSLib_LEO_V1.2** (Gao-tech1): LEO observations are simulated. It is the same software as PolyU-TASLAB/GraphGNSSLib_LEO:
  this repo was created in 2025-01 and the lab-org copy in 2025-11, the file trees are identical and 844 of about 940 blobs are the same.
  Because the file contents differ, this is **not** treated as a pure duplicate, and both entries are kept.
- **Robust-GNSS-FG-GMM-TD**: the dataset belongs to JRC and is not distributed (README).
- **RobustGNSS**: the README points to ICE for the updated implementation, which is now noted.
- **Lompe**: "卑尔根大学课题组开发" is not in the README → "Karl M. Laundal 等开发、Trond Mohn 基金会与挪威研究理事会资助".
- **UnicoreDriver**: the Chinese name "谭志良" was a guess → "Zhiliang Tan" as the README gives it.
- **EISCAT Portal**: typo in desc_zh ("查特罗姆瑟" → "查看特罗姆瑟").
- Vendor wording (batch-45 policy): novatel_gps_driver desc "官方 OEM7 驱动" → "NovAtel 厂商 OEM7 驱动", and pysbf2 "官方 ROS septentrio_gnss_driver" → "Septentrio 厂商的".

### Vague text made specific (README-based)
geomagindices (Ap/Kp/F10.7 pandas; README notes that the post-2018 readers are still missing), pyubxutils (ubxsave/ubxload/ubxsetrate/ubxbase/ubxcompare/
ubxsimulator), pysbf (C core, Python 2.7-era install, SBF v1.13.0 blocks, no updates since 2017), snapshot-gnss-algorithms (SnapperGPS SenSys'21, 12 ms
snapshots), azarashi (DCR-017/DCX-004; u-blox and Spresense input; Python ≥3.11), QZQSM (SPRESENSE L1S), TEC-Maps-of-Nepal (Kathmandu
University final-year project, UNAVCO + CODE DCB, IONEX output, GUI), dSGP4 (Acta Astronautica 2025, PyTorch, mldsgp4), go-gnss/rtcm (parse-only per
README, ntriplatency example).

### Filler removed
Process notes that are not about the software, in GitHub entries only: "细节以官方页面或仓库 README 为准/细节以仓库或官方页面说明为准"
(bladeGPS, Geodesy.jl, geomagindices, DD-cycle-slip-lab, libnmea, go-gnss-rtcm, pyubxutils, and pysbf, where it appeared twice) and
"收录前已…核验" (TEC-Maps-of-Nepal, dSGP4, novatel_oem7_driver, SoapyRTLSDR, SoapyAirspy, nyx, GMAT).

### Checked OK (no change), selection
GalileoHack (README: HackUPC 2024 ESA Challenge winner), OKVIS2-X (TUM/ETH authors), gnss-vector-scintillation, galileo-osnma, PPP-BayesTree
(GTSAM+GPSTk, USAF-cleared), deep_gnss (ION GNSS+ 2021), ICE, TouchRTKStation, EKF_IMU_GPS, FresnelMaps, FindSnowOutliers, gpsonlySNR, orbdetpy,
gnss-integrity-raim, ELT_RTKBase (based on Stefal/rtkbase; u-blox ZED-X20P confirmed), fusioncore, namuru-gps (UNSW NAMURU base), rt-navi,
swift-nav-pygnss, piksi_tools, swiftnav-ros2, ionFR, gps-fpga, gnsshat, ublox8-qzss-almanac-converter, max2771_fx2lp, GNSS-Correction-RTKLIB,
NeoGPS, UbxGps, bolderflight-ublox, ublox-rs, ublox-ros, nmea_navsat_driver, gpsdo, pymap3d, pymsis, Python-NRLMSISE-00, SoapySDR/Remote,
tudatpy (conda recommended), NCAR-GLOW, asv-gnss (SBF/ComNav/UBX confirmed), GTrop (author's CTrop exists), dvoacap-python (VE3NEA DVOACAP port),
saga-utils (IIT; S4/σφ/drift code present), hamsci_LSTID_detection (SWO2R team), inscar (UiT master thesis), smartphone-gnss-booster, um982-driver,
MagPy (cobs.geosphere.at), 977–1028 routine additions (detailed text already README-based).

### Provenance (range 751–1028)
- **UNR-GPSNetMap (917): official → academic_lab.** It is on the same host and run by the same lab (Nevada Geodetic Laboratory, University of Nevada, Reno) as
  UNR-NGL (760), which is academic_lab. Batch 47's non-GitHub review only looked at academic_lab entries, so this official one was missed.
- Company orgs in the range are all personal_community already (novatel, trimble-oss, sparkfun, swift-nav, Fixposition, Aceinna, CS-SI,
  pothosware, GNSSOEM, rokubun). All 34 non-personal GitHub owners were checked with `users/X`. User-account academic_lab entries are all
  covered by batch 45: kept are J-kroeger (IfE Hannover), TMBOC (SJTU), and Gao-tech1 (the README names the PolyU TAS Lab). The borderline ones (kristinemlarson,
  AILocAR, DTUSWx, ilkkavir, engeir, klaundal, ancklo) are unchanged.
- Other non-GitHub entries were reviewed, and the official/academic assignments are consistent. MACCS keeps its `http://` URL because HTTPS fails the TLS handshake
  (curl exit 35), as the analysis already says.

### desc_zh identical to one_liner_zh
Catalog-wide code entries (non-official_site): **0**.

## Task 2: EasyGNSS (idx 584)
`gh api repos/whigg/EasyGNSS` and its commits show the following. It is not a GitHub fork. It was created on 2019-06-01 UTC, which is after the last commit (2019-05-15). The history contains commits by
"Nassim Chebbah <…@ensg.eu>" and "Merge pull request #10 from NChebbah/final". NChebbah/EasyGNSS now returns 404, while the user NChebbah still exists (1 public repo).
The whigg account has more than 7000 public repos. analysis_zh now states this factually ("应是原仓 NChebbah/EasyGNSS（现已 404）的转存"), replacing "可能是转存".
Provenance stays personal_community.

## Regeneration / validation
- The pre-edit dry run of merge_routine_20260926c `regenerate_lists/categories/readme` gave zero diff. main() was not run.
- PROJECTS.json has 71 changed lines: analysis_zh 41, desc_zh 19, one_liner_zh 6, language 2, provenance 1 and provenance_counts 2. Lists 01–10 changed only in
  the matching rows. The README changed only in its provenance line (332/238/459). categories.md is unchanged. A second regeneration was idempotent.
- JSON is valid. project_count 1029 = len(projects) = Σcounts_by_category = Σprovenance_counts. There are no duplicate URLs or names.

## Leftovers
- ros-drivers (nmea-msgs 47, nmea_navsat_driver 893) is still official, and esa/dSGP4 (913) is still academic_lab. These are the batch-45 borderline cases, and they need a policy call.
- space-physics / geospace-code / pysat org entries are academic_lab across the catalog (Organization accounts, not a named university lab), and would need a
  catalog-wide policy decision.
- The process note "收录前已…核验…" is still in 93 analysis_zh in this range (160 catalog-wide), mostly on official_site entries. It is harmless but it is filler.
- desc_zh for many idx 843–961 entries is written as caveats ("非测地后处理"…) rather than as a description. It is accurate, so it was left as is.
- GraphGNSSLib_LEO (719) and GraphGNSSLib_LEO_V1.2 (829) are the same software in two repos. If a maintainer prefers one entry, retiring 829 needs a call,
  because the contents are not identical.
- NeRC should be re-checked when its code is released.
