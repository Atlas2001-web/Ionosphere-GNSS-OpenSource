# QC audit — 2026-09-26 batch 38 (license via README/metadata/headers, no-LICENSE-file GitHub entries)

Base: d98944a (1036 projects). Task 0: no entries past idx 1035 — nothing to QC.

Scope: 50 of the 150 GitHub entries with license blank/`unknown`/`NOASSERTION`/`see upstream*` (named candidates first, then idx order 10–203). For each: README licence section, package metadata (setup.py/pyproject/package.xml/package.json/pom.xml/build.gradle), headers of up to 8 main source files, and LICENCE/COPYING variants anywhere in the tree (bundled third-party licences ignored). Evidence read via `gh api` on 2026-09-26.

Conventions (as batch 37): bare `GPL-3.0`/`GPL-2.0` unless "or (at your option) any later version" is stated → `-or-later`; RTKLIB-derived repos get `BSD-2-Clause` only if they carry RTKLIB's licence text (none of these do); no licence anywhere → `null` (as GTrop, batch 32); custom/conflicting → short descriptive string. No language/url/desc changes.

Result: 11 SPDX, 7 descriptive/compound, 32 null.

| idx | name | before | after | evidence |
|---|---|---|---|---|
| 0 | [AgOpenNtripCaster](https://github.com/AgOpenGPS-Official/AgOpenNtripCaster) | `''` | `README: MIT (badge says GPL-3.0; no LICENSE file)` | README (docs/README.md) §License: "MIT License - See [LICENSE](./LICENSE) file for details." but badge "License-GNU_GPL_v3" and no LICENSE file in tree (GitHub license API: none) → conflicting, descriptive |
| 10 | [BUAA-RINEX-Convertor](https://github.com/Jia-le-wang/BUAA-RINEX-Convertor) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 16 | [crz2rnx](https://github.com/zhufengGNSS/crz2rnx) | `''` | `GSI RNXCMP licence (no source modification without GSI consent; AS-IS free redistribution)` | Repo content is RNXCMP 4.0.4 only; RNXCMP_4.0.4_src/docs/LICENSE.txt: "The source codes and related documents of the RNXCMP software may not be changed without the consent of Geographical Survey Institute" / "Redistributions ... are made AS IS accompanied with this license document at no charge" |
| 18 | [DRCycleSlip](https://github.com/Jin-Whu/DRCycleSlip) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 23 | [GDDS](https://github.com/LECUT/GDDS) | `''` | `GPL-3.0` | src/LICENSE (all code under src/): verbatim "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"; no or-later statement |
| 28 | [GHASP-HAS-decoding](https://github.com/borioda/HAS-decoding) | `'see upstream README'` | null | No LICENSE; README, source headers (only "@author: daniele") and manual/GHASP_user_manual_Feb23.pdf contain no licence text |
| 30 | [gnss-downloader](https://github.com/Mereithhh/gnss-downloader) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 32 | [gnss-multipath-detector](https://github.com/EvgeniiMunin/gnss-multipath-detector) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 48 | [MAPS](https://github.com/GCCLib/MAPS) | `''` | null | README silent; headers only attribute third-party copyright (Craymer, Glaner, ...); no project licence |
| 49 | [nmea-msgs](https://github.com/ros-drivers/nmea_msgs) | `''` | `BSD (package.xml; clause variant unspecified)` | package.xml: "<license>BSD</license>" (no LICENSE file, msg-only package; clause variant not stated) |
| 65 | [PyRINEX](https://github.com/geumjin99/PyRINEX) | `''` | `Apache-2.0` | README: "## License / Apache License 2.0"; pyproject.toml: license = { text = "Apache-2.0" } |
| 70 | [READ_GNSS](https://github.com/dzd9798/READ_GNSS) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 76 | [RNXQCE](https://github.com/cuizilu/RNXQCE) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 88 | [uNavTools](https://github.com/IvAn190/uNavTools) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 150 | [B2bLIB](https://github.com/GCCLib/B2bLIB) | `''` | null | RTKLIB-derived; files keep "Copyright (C) ... T.TAKASU, All rights reserved." only; RTKLIB licence text not carried; README silent |
| 151 | [CLASLIB](https://github.com/QZSS-Strategy-Office/claslib) | `'see upstream (derived RTKLIB/GSILIB)'` | `BSD-2-Clause (v0.6.0 and earlier per README; later versions unstated)` | README "# License / ## CLASLIB Version 0.6.0 and earlier": "CLASLIB version 0.6.0 and earlier is distributed under the following BSD 2-clause license ... and additional two exclusive clauses"; no statement for 0.7.x/0.8.x (relnotes 0.6.1–0.8.4 and manual-claslib.pdf silent); readme_rtklib.txt carries RTKLIB's own BSD-2 notice for the RTKLIB part |
| 155 | [Easy4PTK](https://github.com/alxanderjiang/Easy4PTK) | `''` | null | README silent; src/*.py headers only "#Copyright 2025-, by Zhuojun Jiang ... Wuhan University of Technology" (no licence grant) |
| 157 | [GAMP_PPPH](https://github.com/zhufengGNSS/GAMP_PPPH) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence (only bundled pthreads-w32 COPYING files) |
| 163 | [GNSS-Explorer](https://github.com/brucezhcw/GNSS-Explorer) | `''` | null | RTKLIB-derived; files keep "Copyright (C) ... T.TAKASU, All rights reserved." only; RTKLIB licence text not carried; README silent |
| 170 | [GNSSRTK](https://github.com/supakunz/GNSS_RTK) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 171 | [goGPS_Java](https://github.com/goGPS-Project/goGPS_Java) | `''` | `LGPL-3.0-or-later` | README: "The Java code is released under an LGPL license."; src/main/java/org/gogpsproject/GoGPS.java header: "GNU Lesser General Public License ... either version 3 of the License, or (at your option) any later version"; src/main/resources/license-lgpl.txt = LGPL v3 text |
| 172 | [goGPS_MATLAB](https://github.com/goGPS-Project/goGPS_MATLAB) | `''` | `GPL-3.0` | source/LICENSE.txt: verbatim "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"; file headers say "The licence of this file can be found in source/licence.md" (file absent); README silent → GPL-3.0 (no or-later wording found) |
| 175 | [GraphGNSSLib](https://github.com/weisongwen/GraphGNSSLib) | `''` | `GPL-3.0` | README §7 License: "The source code is released under [GPLv3](http://www.gnu.org/licenses/) license." |
| 182 | [HPRTK](https://github.com/yxw027/HPRTK) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 188 | [MG_APP](https://github.com/XiaoGongWei/MG_APP) | `''` | `GPL-3.0` | README Appendix A: "MG-APP are distributed under the terms of the version 3 of the GNU General Public License (GPLv3). See the file COPYING." (+ commercial licences on request); Licences/COPYING = GPLv3 |
| 192 | [NavDecoder](https://github.com/NavSesne/NavDecoder) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 193 | [Net_Diff](https://github.com/YizeZhang/Net_Diff) | `''` | null | Binary (MATLAB Runtime) distribution; README, readme.txt and "A guide to use Net_Diff.pdf" contain no licence |
| 197 | [PPP-RTK-Beechan](https://github.com/MichaelBeechan/PPP-RTK) | `''` | null | No README/LICENSE; RTKLIB/CLASLIB files carry only copyright lines (isb.c alone says "Released under the BSD 2-clause License" for that GSI file) → not repo-wide |
| 200 | [PPP_AR](https://github.com/heiwa0519/PPP_AR) | `''` | null | RTKLIB-derived; files keep "Copyright (C) ... T.TAKASU, All rights reserved." only; RTKLIB licence text not carried; README silent |
| 201 | [ppp_rtklib](https://github.com/mulin33/ppp_rtklib) | `''` | null | RTKLIB-derived; files keep "Copyright (C) ... T.TAKASU, All rights reserved." only; RTKLIB licence text not carried; README silent |
| 202 | [PPPH-UAV](https://github.com/BerkayBahadur/PPPH-UAV) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 203 | [PPPLib](https://github.com/yxw027/PPPLib) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 215 | [RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b) | `''` | `GPL-3.0` | README §License: "This project is licensed under the [GNU General Public License v3.0]... under the terms of GPLv3" (referenced LICENSE file not present; RTKLIB-derived files keep T.Takasu copyright headers) |
| 227 | [BeagleSDRGPS](https://github.com/jks-prv/Beagle_SDR_GPS) | `''` | `LGPL-2.0-or-later (KiwiSDR code) + GPL-3.0-or-later (GPS receiver code)` | No root licence; main.cpp / rx/rx_cmd.cpp: "GNU Library General Public License ... either version 2 of the License, or (at your option) any later version" (Copyright John Seamons); gps/gps.cpp: "GNU General Public License ... either version 3 of the License, or (at your option) any later version" (Andrew Holme). Repo archived. |
| 250 | [GNSS-SDRLIB](https://github.com/taroz/GNSS-SDRLIB) | `''` | `GPL-2.0-or-later` | README License: "Copyright (C) 2014 Taro Suzuki ... the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version" |
| 277 | [SignalSim](https://github.com/globsky/SignalSim) | `''` | null | README: "commercial licensing available for advanced features" / "only available with commercial license" — no licence stated for the published code; no LICENSE file, source headers without notice |
| 363 | [IonoMoni](https://github.com/qiliu2025/IonoMoni) | `''` | `GPL-3.0` | README §License: "IonoMoni is released as open-source software under the GNU General Public License, version 3 (GPLv3)." |
| 364 | [ionopy](https://github.com/spaceml-org/ionopy) | `'see upstream README'` | null | No LICENSE; README (only Acknowledgements) and ionopy/*.py carry no licence |
| 421 | [NequickG](https://github.com/tpl2go/NequickG) | `''` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 455 | [pytiegcm](https://github.com/asher-pembroke/pytiegcm) | `'unknown'` | `MIT` | setup.py: license='MIT' (only licence statement in repo; no LICENSE file) |
| 468 | [SAMI3-3.22-CCMC-mirror](https://github.com/sylee918/SAMI3) | `'unknown'` | null | No README/LICENSE; sami3-3.22.f90 and module headers carry no copyright/licence (CCMC mirror of NRL SAMI3 3.22) |
| 483 | [SpatioTECformer](https://github.com/research1011/SpatioTECformer) | `'see upstream README'` | `no licence granted (README: research use, contact author)` | README.markdown §License: "This project is intended for research purposes and is not distributed under a specific license. Contact the author for usage permissions." |
| 521 | [carvig](https://github.com/Erensu/carvig) | `''` | null | README silent; no LICENSE; RTKLIB-style rtkcmn.cc and carvig.h headers carry no copyright/licence |
| 540 | [GVINS-WHU](https://github.com/zhangwhu/GVINS) | `''` | `GPL-3.0-or-later` | No README; ic_gvins/* headers (e.g. ROS/fusion_ros.cc): "GNU General Public License ... either version 3 of the License, or (at your option) any later version" (i2Nav, WHU); gnss_comm-main/LICENSE = GPLv3 |
| 543 | [ignav](https://github.com/Erensu/ignav) | `''` | null | README silent; no LICENSE; RTKLIB-style rtkcmn.cc and carvig.h headers carry no copyright/licence |
| 584 | [MCOSB](https://github.com/GCCLib/MCOSB) | `'see upstream README'` | null | No LICENSE/COPYING anywhere in tree; README has no licence/copyright wording; first 8 main source files and package metadata carry no licence |
| 614 | [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset) | `''` | null | README "## License" section contains only contact persons, no licence; no LICENSE file |
| 620 | [GMR-Water](https://github.com/GRseRG-CUMTB/GMR-Water) | `'see upstream README'` | null | No top-level licence; README and doc/manual.pdf silent; only bundled third-party licences under lib/ (bspline, mpsim) |
| 656 | [NTRIPcaster-python](https://github.com/Rampump/NTRIPcaster) | `'NOASSERTION'` | `Apache-2.0 (README; LICENSE file is a non-verbatim variant)` | README: "This project is licensed under the [Apache License 2.0](LICENSE)."; LICENSE titled Apache 2.0 but word-diff vs apache.org text shows altered definitions and an MIT-style grant ("modify, merge, publish, distribute ... sell copies") → descriptive |
| 665 | [GNSS_MobileCalculator](https://github.com/RogerioDoCarmo/GNSS_MobileCalculator) | `'NOASSERTION'` | null | No LICENSE (GitHub now: none); README (pt-BR) silent; only AOSP-copied GpsTime.java carries Apache header — not a project licence |

analysis_zh edits (to stop contradicting the new value):
- 363 IonoMoni: "文档与许可信息需自行确认；" → "README 声明以 GPLv3 发布；"
- 364 ionopy: "许可证未在 GitHub 标 SPDX，使用前请读仓库说明；" → "仓库与 README 均未声明许可证，使用或再分发前应先联系作者；"
- 614 UrbanNavDataset: "使用请遵守数据集许可与引用要求。" → "仓库未声明许可（README 的 License 节只列联系人），使用请遵守引用要求并事先与作者确认。"

Lists regenerated via `research/merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme`: only `许可：` detail lines + 3 analysis lines changed (entries going ""→null render "—" both ways, so no list diff); categories/README unchanged. Counts: 1036 projects, counts_by_category unchanged.

## Leftovers
- 100 remaining blank/`unknown`/`see upstream README` GitHub entries (idx 206 pyRTKLib onward: RTK, RTKLIB derivatives, SDR sims, iono ML repos, GINS/TGINS, UNB3m, ICAMS, ntrip-caster-go, GGOS-Tropo-RTKLIB, …) still need the same README/header pass.
- 0 AgOpenNtripCaster: README text (MIT) vs badge (GPL-3.0) conflict — kept descriptive until upstream adds a LICENSE.
- 172 goGPS_MATLAB: headers cite missing source/licence.md; re-check if it appears.
