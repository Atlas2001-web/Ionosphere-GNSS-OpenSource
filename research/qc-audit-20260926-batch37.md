# QC audit — 2026-09-26 batch 37 (license-fill pass, GitHub entries)

Base: ec78009 (1036 projects). Task 0: no entries past idx 1035 — nothing to QC.

Scope: GitHub-hosted entries whose `license` was blank/null/`unknown`/`NOASSERTION`/`see upstream*`/vague. 201 candidates found; this batch handled 44 (priority: named candidates + GitHub NOASSERTION repos whose license file needed human reading). Evidence read via `gh api repos/X/license` and `gh api repos/X/contents/<path>` on 2026-09-26.

Convention notes: catalog uses bare `GPL-2.0`/`GPL-3.0`/`LGPL-3.0` for plain-version texts; `-or-later` used only where the file says "or (at your option) any later version". RTKLIB-family BSD-2 + bundled-binary clause → `BSD-2-Clause` (existing majority convention). Custom licences get short descriptive strings. No `language` changes (all 44 already had a language; blank-language entries left).

| idx | name | before | after | evidence |
|---|---|---|---|---|
| 5 | [baidu-ntripcaster](https://github.com/baidu/ntripcaster) | `'NOASSERTION'` | `GPL-2.0-or-later` | LICENSE: "GNU General Public License ... either version 2 of the License, or (at your option) any later version" (BKG 2004-2008 + Baidu 2018 notices) |
| 29 | [gLAB](https://github.com/valgur/gLAB) | `''` | `Apache-2.0 + LGPL-3.0 (GUI)` | LICENSE: "The gLAB's GUI ... is licensed under the GNU LESSER GENERAL PUBLIC LICENSE version 3" / "The processing core (gLAB_linux) and graphical tool (graph.py) is licensed under the Apache License, Version 2.0" — reused existing catalog string |
| 38 | [gnsstk](https://github.com/SGL-UT/gnsstk) | `''` | `LGPL-3.0` | LICENSE.md: "The source code provided by the GNSSTk is distributed under the GNU LGPL, Version 3." |
| 39 | [gnsstk-apps](https://github.com/SGL-UT/gnsstk-apps) | `''` | `LGPL-3.0` | LICENSE.md: "The source code provided by the GNSSTk is distributed under the GNU LGPL, Version 3." |
| 44 | [GPSTk](https://github.com/SGL-UT/GPSTk) | `''` | `LGPL-3.0` | LICENSE.md: "The source code provided by the GPSTk is distributed under the GNU LGPL, Version 3." |
| 47 | [hatanaka](https://github.com/valgur/hatanaka) | `''` | `MIT (Python wrapper) + GSI terms (RNXCMP, cite Hatanaka 2008)` | LICENSE: RNXCMP part "Geospatial Information Authority of Japan Website Terms of Use ... is applied" + "Hatanaka Python library / MIT License / Copyright (c) 2021 Martin Valgur" |
| 53 | [ntrip_client-MicroStrain](https://github.com/LORD-MicroStrain/ntrip_client) | `'NOASSERTION'` | `MIT` | LICENSE: "ROS NTRIP Client is licensed under the MIT License" |
| 107 | [cssrlib-data](https://github.com/hirokawa/cssrlib-data) | `'NOASSERTION'` | `MIT` | LICENSE: "MIT License / Copyright (c) 2022 Rui Hirokawa" |
| 158 | [ginan](https://github.com/GeoscienceAustralia/ginan) | `''` | `Apache-2.0` | LICENSE.md: "Copyright 2020 Geoscience Australia / Licensed under the Apache License, Version 2.0" |
| 173 | [gps_pvt](https://github.com/fenrir-naru/gps_pvt) | `''` | `BSD-3-Clause` | LICENSE: "BSD 3-Clause License / Copyright (c) 2022, M.Naruoka (fenrir)" (applies to files without own statement) |
| 174 | [GPSPACE](https://github.com/CGS-GIS/GPSPACE) | `''` | `MIT` | Licence.txt: "computer program source code of the GPSPACE software is covered under Crown Copyright, Government of Canada, and is distributed under the MIT License." |
| 186 | [MALIB](https://github.com/JAXA-SNU/MALIB) | `'see upstream (RTKLIB-derived)'` | `BSD-2-Clause` | LICENSE.txt: "The MALIB software package is distributed under the following BSD 2-clause license." |
| 190 | [MRTKLIB](https://github.com/h-shiono/MRTKLIB) | `''` | `BSD-2-Clause` | LICENSE: "The MRTKLIB software package is distributed under the following BSD 2-clause license." |
| 214 | [RTKLIB](https://github.com/tomojitakasu/RTKLIB) | `''` | `BSD-2-Clause` | readme.txt §LICENSE: "The RTKLIB software package is distributed under the following BSD 2-clause license ... and additional two exclusive clauses" (extra clause only covers bundled Windows binaries; catalog convention BSD-2-Clause). No LICENSE file (GitHub API 404). |
| 216 | [RTKLIB-explorer](https://github.com/rtklibexplorer/RTKLIB) | `''` | `BSD-2-Clause` | license.txt: "The RTKLIB software package is distributed under the following BSD 2-clause license." |
| 218 | [RTKNAVI-BH](https://github.com/cigit001/RTKNAVI-BH) | `'NOASSERTION'` | `BSD-2-Clause` | LICENSE: "RTKNAVI-BH ... This software is distributed under the following BSD 2-clause license." |
| 240 | [gnss-baseband](https://github.com/j-core/gnss-baseband) | `''` | `BSD-2-Clause` | LICENSE: "Copyright (c) 2020, CoreSemi Pte Ltd." two-condition BSD text (wording extended to "source, binary, netlist or hardware instantiated forms") |
| 243 | [GNSS-matlab](https://github.com/danipascual/GNSS-matlab) | `''` | `GPL-3.0-or-later (source/)` | root LICENSE: "You may find a specific licence files in each directory."; source/LICENSE: "GNU General Public License ... either version 3 of the License, or (at your option) any later version" (+ COPYING.txt GPLv3); other dirs are PRN .mat data/docs |
| 252 | [GNSS-VHDL](https://github.com/danipascual/GNSS-VHDL) | `''` | `GPL-3.0-or-later` | root LICENSE.txt: "applies only to this directory and all subdirectories ... GNU General Public License ... either version 3 of the License, or (at your option) any later version" |
| 253 | [GNSSFirehose](https://github.com/pmonta/GNSS_Firehose) | `''` | `TAPR-OHL-1.0 (hardware) + GPL-2.0 (HDL/firmware) + CC-BY-SA-3.0 (docs)` | LICENSE: "hardware design files ... TAPR Open Hardware License, version 1.0" / "HDL, firmware, software ... GPL version 2" / "documentation ... Creative Commons BY-SA 3.0" |
| 275 | [PocketSDR](https://github.com/tomojitakasu/PocketSDR) | `'NOASSERTION'` | `BSD-2-Clause` | LICENSE.txt: "The PocketSDR package is distributed under the following BSD 2-clause license." |
| 284 | [ALBUS_ionosphere](https://github.com/twillis449/ALBUS_ionosphere) | `''` | `GPL-2.0-or-later` | LICENSE: ASTRON/MeqTree and NRC notices: "GNU General Public License ... either version 2 of the License, or (at your option) any later version" |
| 335 | [GNSS_TOM](https://github.com/sailvssea/GNSS_TOM) | `'unknown'` | `LGPL-3.0` | LICENSE.md: "The source code provided by the GNSS_TOM is distributed under the GNU LGPL, Version 3." (analysis_zh "许可为 NOASSERTION" → "许可为 LGPL-3.0") |
| 378 | [IonTools](https://github.com/rumkex/IonTools) | `''` | `BSD-3-Clause` | LICENSE.md: "This software is distributed under the Modified BSD License." + 3-clause text |
| 396 | [iricore](https://github.com/MIST-Experiment/iricore) | `'see upstream'` | `MIT` | LICENSE: "MIT License / Copyright (c) 2022 Vadym Bidula" (portions Michael Hirsch) |
| 402 | [Kamodo](https://github.com/nasa/Kamodo) | `'NASA-Open'` | `NASA-1.3` | LICENSE: "NASA OPEN SOURCE AGREEMENT VERSION 1.3" → SPDX NASA-1.3 |
| 403 | [Kamodo-core](https://github.com/nasa/Kamodo-core) | `'NASA-Open'` | `NASA-1.3` | LICENSE: "NASA OPEN SOURCE AGREEMENT VERSION 1.3" → SPDX NASA-1.3 |
| 420 | [NeQuick2-MLF2](https://github.com/SkydelSolutions/nequick2-mlf2) | `'unknown'` | `EUPL-1.2` | LICENSE: "protected by European Union Copyright as stated in the terms and conditions of the European Union Public Licence v. 1.2" + full EUPL v1.2 text |
| 432 | [OASIS](https://github.com/giorgiopicanco/OASIS) | `''` | `CC-BY-NC-4.0` | LICENSE: "Creative Commons Legal Code / CC BY-NC 4.0 International" |
| 433 | [OASIS-ohm1122](https://github.com/ohm1122/OASIS) | `''` | `CC-BY-NC-4.0` | LICENSE (fork): "Creative Commons Legal Code / CC BY-NC 4.0 International" |
| 460 | [RIM](https://github.com/SWMFsoftware/RIM) | `'unknown'` | `Apache-2.0` | LICENSE.txt: "Copyright (C) 2002 Regents of the University of Michigan ... Licensed under the Apache License, Version 2.0" (analysis_zh "许可字段不清晰" → "许可为 Apache-2.0（密歇根大学版权）") |
| 499 | [tidd](https://github.com/vc1492a/tidd) | `'NOASSERTION'` | `Apache-2.0` | license.txt: "Copyright 2020 the California Institute of Technology. Licensed under the Apache License, Version 2.0" |
| 500 | [TIE-GCM](https://github.com/NCAR/tiegcm) | `'NCAR-academic'` | `NCAR TIE-GCM academic research licence (non-commercial, no operational use)` | LICENSE: "NCAR TIE-GCM OPEN SOURCE ACADEMIC RESEARCH LICENSE AGREEMENT ... for research, academic, and non-profit purposes only" / "No Sales ... may not be used for operational purposes" — custom, descriptive string |
| 501 | [transcar](https://github.com/space-physics/transcar) | `'NOASSERTION'` | `Apache-2.0` | LICENSE.txt: "Licensed under the Apache License, Version 2.0" |
| 538 | [gtsam](https://github.com/borglab/gtsam) | `''` | `BSD-3-Clause` | LICENSE: "GTSAM is released under the simplified BSD license, reproduced in the file LICENSE.BSD"; LICENSE.BSD actually carries 3 clauses incl. "3. Neither the name of the copyright holder ..." → BSD-3-Clause (file text wins over label; bundled 3rd-party libs have own licences) |
| 541 | [GVINS-Dataset](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset) | `'NOASSERTION'` | `CC-BY-NC-SA-4.0` | LICENSE: "Attribution-NonCommercial-ShareAlike 4.0 International" (analysis_zh "许可字段为 NOASSERTION" → "许可为 CC BY-NC-SA 4.0（非商业）") |
| 549 | [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl) | `''` | `MIT` | LICENSE.md: "The package Tracking is licensed under the MIT License. Copyright (c) 2017-2021: Soeren Schoenbrod" (package name typo upstream; MIT text) |
| 555 | [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS) | `''` | `academic non-commercial (Penn MSCKF_VIO terms, no redistribution)` | LICENSE.txt: Penn Software MSCKF_VIO notice: "modifications ... for their internal research and academic purposes only" / "shall not distribute Software or Modifications to any third parties without the prior written approval of Penn" |
| 558 | [NaveGo](https://github.com/rodralez/NaveGo) | `''` | `LGPL-3.0` | LICENSE: "GNU LESSER GENERAL PUBLIC LICENSE Version 3, 29 June 2007" (verbatim) |
| 563 | [rtklib_ros_bridge](https://github.com/MapIV/rtklib_ros_bridge) | `'NOASSERTION'` | `BSD-3-Clause` | LICENSE: "Copyright (c) 2019, Map IV, Inc." 3-clause BSD ("Neither the name of the Map IV, Inc. nor ...") |
| 599 | [HTDP](https://github.com/noaa-ngs/HTDP) | `'other (NOAA/NGS)'` | `USGov (17 USC 105; royalty-free licence outside US)` | License.txt: "Software code created by U.S. Government employees is not subject to copyright in the United States (17 U.S.C. §105) ... grants to Recipient a royalty-free, nonexclusive license ... outside of the United States" |
| 603 | [Muf_Muncher](https://github.com/mooxle/Muf_Muncher) | `'see upstream README'` | `MIT` | LICENSE: "MIT License / Copyright (c) 2026 Max Sammet (DA6MAX)" |
| 634 | [mphw](https://github.com/ufrgs-gnss-lab/mphw) | `'NOASSERTION'` | `BSD-2-Clause (MATLAB) + GPL-2.0 (Arduino) + CC-BY-SA-3.0 (docs)` | root LICENSE: "different types of content have different licences"; code/matlab/LICENSE "BSD 2-Clause License"; code/ardu/LICENSE "GNU GENERAL PUBLIC LICENSE Version 2"; docs/LICENSE "Creative Commons Attribution-ShareALike 3.0 Unported" |
| 653 | [SparkFun_u-blox_GNSS_v3](https://github.com/sparkfun/SparkFun_u-blox_GNSS_v3) | `'MIT-style (SparkFun code)'` | `MIT` | LICENSE.md: "SparkFun code, firmware, and software is released under the MIT License" (hardware CC BY-SA 4.0; library repo is code) → MIT |

analysis_zh edits (to stop contradicting the new license): idx 335, 460, 541 (single-sentence replacement, noted above).

Lists regenerated via `research/merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme`: only `许可：` detail lines (44) + 3 analysis lines changed; categories/README unchanged. Counts: 1036 projects, counts_by_category unchanged.

## Leftovers (not changed)

- claslib (151): README license section covers only "CLASLIB version 0.6.0 and earlier" (BSD-2 + clauses); no LICENSE file for current 0.7.x/0.8.x → kept.
- Rampump/NTRIPcaster (656): LICENSE titled "Apache License Version 2.0" but text is not verbatim (altered definitions) → kept `NOASSERTION` pending closer review.
- ~155 entries with blank/`unknown`/`see upstream README` license where GitHub detects no license file (NONE): need README license-section check before setting null (e.g. AgOpenNtripCaster, crz2rnx, goGPS_Java/MATLAB, GraphGNSSLib, taroz/GNSS-SDRLIB, SignalSim, Beagle_SDR_GPS, IonoMoni, NequickG, pytiegcm, SAMI3, carvig, ignav, GVINS, UrbanNavDataset, GTrop-style repos, HAS-decoding, ionopy, SpatioTECformer, MCOSB, GMR-Water …).
- Remaining catalog `NOASSERTION`: NTRIPcaster-python (656, above) and GNSS_MobileCalculator (665; GitHub now reports no license file → candidate for null after README check).
- Blank `language`: gnsstk-apps (GitHub: PostScript, ambiguous), RTKNAVI-BH, GAMP_PPPH (GitHub: Grammatical Framework, misdetected), PPPLib, awesome/data repos — left blank.
