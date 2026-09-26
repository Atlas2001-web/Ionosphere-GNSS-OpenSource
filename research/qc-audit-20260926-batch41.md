# QC audit — 2026-09-26 batch 41 (non-GitHub licence pass + blank-language fill)

Base: origin/main 33124e7 (batch 40 38e6db3 + peer docs commit "short-hard manual for doris-rinex"). Catalog **1035** projects, unchanged (no adds/removals). Evidence read 2026-09-26 (ET).

## Task 0 — entries newer than batch 40
None: `project_count` is still 1035 and no project was appended after 38e6db3 (only a docs commit landed). Nothing to QC.

## Task 1 — non-GitHub code hosts (GitLab / GitLab instances / SourceForge / Bitbucket / Trac-SVN / FTP / download dirs / Zenodo / File Exchange)
Scope: every entry whose URL is not github.com and whose `language` is not `data-portal` (95 entries). Pure portals skipped. Checks: GitLab API `/projects/<enc>?license=true` + `/languages` and shallow clones; SourceForge REST `/rest/p/<proj>` + `svn ls/cat/export`; Bitbucket API + raw files; Trac `export/HEAD` raw source on software.rtcm-ntrip.org; BKG FTP tarball; irimodel.org dir listings; Zenodo API `/api/records/<id>` + zip contents; MathWorks FEX download zip. Conventions as batches 37–40.

| idx | name | before | after | evidence |
|---|---|---|---|---|
| 19 | [EarthScope-gnsstools](https://gitlab.com/earthscope/gnsstools) | `''` | `Apache-2.0` | GitLab API license key `apache-2.0`; LICENSE = Apache 2.0 text; README "## License — Licensed under the Apache License, Version 2.0". Languages Go 97.6 % (Go correct) |
| 6 | [BKG-NtripCaster](https://igs.bkg.bund.de/ntrip/bkgcaster) | `GPL` | `GPL-3.0-or-later (README/source headers; bundled COPYING is GPLv2 text)` | ntripcaster-2.0.49.tar.bz2 (BKG FTP): README "License … either version 3 of the License, or (at your option) any later version"; src/commands.h same GPLv3+ header; but COPYING file is "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" → descriptive |
| 12 | [Caster-source-FTP](https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/) | `GPL` | same as 6 | same tarball |
| 56 | [ntripclient](https://software.rtcm-ntrip.org/wiki/ntripclient) | `GPL` | `GPL-2.0-or-later` | `export/HEAD/ntrip/trunk/ntripclient/README` + `ntripclient.c`: "either version 2 of the License, or (at your option) any later version" |
| 57 | [ntripserver](https://software.rtcm-ntrip.org/wiki/ntripserver) | `GPL` | `GPL-2.0-or-later` | `ntripserver.c` header (BKG 2019): "either version 2 of the License, or (at your option) any later version" |
| 80 | [rtcm3torinex](https://software.rtcm-ntrip.org/wiki/rtcm3torinex) | `GPL` | `GPL-2.0-or-later` | `rtcm3torinex/lib/rtcm3torinex.c`: "either version 2 of the License, or (at your option) any later version" |
| 9 | [BNS](https://software.rtcm-ntrip.org/wiki/BNS) | `GPL` | `GPL (version unspecified)` | Trac trunk/BNS has no LICENSE/COPYING; only `bnsabout.html`: "Developed under GNU General Public License …" (no version); .cpp headers silent |
| 42 | [gpsd](https://gitlab.com/gpsd/gpsd) | `BSD` | `BSD-2-Clause` | GitLab API `bsd-2-clause`; COPYING: "LICENSE (SPDX short identifier: BSD-2-Clause)" |
| 43 | [gpsd-website](https://gpsd.io/) | `BSD` | `BSD-2-Clause` | same project/COPYING |
| 156 | [Essential-GNSS](https://sourceforge.net/projects/gnsstk/) | `BSD-style` | `BSD-3-Clause` | SF REST license "BSD License"; svn trunk/src/gps.c etc.: "Redistribution and use … permitted provided … - The name(s) of the contributor(s) may not be used to endorse or promote products …" (3-clause form); no LICENSE file |
| 591 | [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos/) | `EUPL` / `C/C++` | `EUPL-1.1` / `C` | svn trunk/LICENSE "European Union Public Licence V.1.1"; COPYING "licenced under the EUPL V.1.1"; libegnos/Egnos.c "Licensed under the EUPL, Version 1.1 only". Tree: 18 .c, 15 .h, 0 C++ files → `C` |
| 597 | [GPSBabel](https://www.gpsbabel.org/) | `GPL` | `GPL-2.0-or-later` | gpsbabel.org: "distributed under the GNU Public License"; project source (GPSBabel/gpsbabel, linked from the site) COPYING = GPLv2, main.cc "either version 2 of the License, or (at your option) any later version" |
| 313 | [FARR](https://gitlab.com/longleywj/farr) | `GPL-3.0` | `GPL-3.0-or-later` | README "## License … either version 3 of the License, or (at your option) any later version"; app/main.cc "License: GNU General Public License v3.0 or later" |
| 426 | [nleht-fdtd-ionosphere](https://gitlab.com/nleht/fdtd) | `see upstream repository` | `no licence (README: copyright reserved, reference use only)` | GitLab API license null; no LICENSE; README "# License — The project is protected by copyright. It is not being currently actively developed and may be used only for reference." |
| 448 | [pypride](https://gitlab.com/gofrito/pypride) | `MIT (see upstream; classifiers also mention GPL)` | `MIT (pyproject license field; classifier says GPLv3+; no LICENSE file)` | pyproject.toml: `license = {text = "MIT"}` and `classifiers = ["License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"]`; no LICENSE; vex.py GPLv2+ header and IERS headers are third-party |
| 485 | [Swarm-VIP-Dynamic](https://gitlab.com/KNMI-OSS/spaceweather/swarm-vip-dynamic) | `see upstream repository` | `Apache-2.0` | no LICENSE; pyproject.toml `license = "Apache License v2.0"` (package metadata, like batch-40 gnssr-raspberry) |
| 379–382, 384 | IRI-2001/2007/2012/2016/2026-package | null | `IRI permissive (AS IS + attribution)` | each irimodel.org dir has its own licence file (00_iri2001_license.txt, 00_iri2007-license.txt, 00_iri2012_License.txt, 00_iri2016-License.txt; IRI-2026 dir ships 00_iri2016-License.txt): "Permission is hereby granted, free of charge … to use, copy, and modify the Software … IRI Working Group should be acknowledged …" — same text as IRI-2020 (already `IRI permissive (AS IS + attribution)`) |
| 388 | [IRI-MATLAB-FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model) | null | `BSD-2-Clause` | FEX download zips (versions 1–15, latest downloadable 2014-10) all carry license.txt "Copyright (c) 2014, Drew Compston … Redistribution and use … 1./2." (BSD 2-clause). v2.0.0 (2019) zip not fetchable from box; same author, page shows "View License" |
| 507 | [Zenodo-VTEC-map-generation-SBAS](https://doi.org/10.5281/zenodo.10058636) | `''` / `''` | `CC-BY-4.0` / `MATLAB` | Zenodo API license `cc-by-4.0`; VTEC_FORZENODO.zip = Main.m + lib/*.m (3 .m) + Data/TEC_HourMap.mat; README.txt "The files are distributed under CC4_BY license"; Main.m "% distributed under CC4-BY license" |
| 199 | [PPP-Wizard](http://www.ppp-wizard.net/) | `see upstream` | null | index/ssr/ppp/snapshot/upload/links pages: no download, no licence text; links.html only cites "An Open-source PPP Client Implementation for the CNES PPP-WIZARD Demonstrator" (ION GNSS+ 2015). HTTPS does not connect (curl 000) → URL stays http |
| 576 | [GFZ-SPOCC-news](https://www.gfz.de/en/section/space-geodetic-techniques/overview/details-section-news/veroeffentlichung-der-software-for-precise-orbit-and-clock-combination-spocc-1) | `open (GFZ release)` | null | news page + IGSMAIL-8560: "written in Python … provided in a Docker environment", no licence; gnss.gfz.de/services/spocc JS bundle: "Repository Access — Please log in to GFZ's GitLab using your GitHub credentials" (git.gfz-potsdam.de sign-in); GFZ GitLab API public search for spocc → [] |
| 585 | [SPOCC](https://gnss.gfz.de/services/spocc) | `open (GFZ release)` | null | same |

Language only:
- 477 [ScintPi-1.0-Software](https://doi.org/10.5281/zenodo.4905193): `unknown` → `binary (PyInstaller)`. ScintPi_Software.zip = Processing/plot_scintpi1.exe (strings "PyInstaller: …") + scintpi.tar with `scintpi_usb_v1`, `filezipper` (strings `_MEIPASS`) — no source. Style follows existing `binary (closed)` / `Windows/Exe`.

Verified, no change: gri-iono (GitLab API MIT; LICENSE MIT; "AGS Script" in GitLab languages is .asc data → Python kept), swarm-vip-dynamic-models (BSD-3-Clause), earthscope-sdk (Apache-2.0), spinifex (git.astron.nl API apache-2.0, Python 99.8 %), IBP-Model (igit.iap-kborn.de API MIT; Python package + notebooks), pyFIRI2018 (Bitbucket LICENSE.txt "Licensed under the Apache License, Version 2.0"; setup.py Apache classifier), IRI-2020/IRI-Fortran, BNC entries (GPL-3.0).

URL check (95 non-portal non-GitHub URLs, browser UA, -L): all 200 except sourceforge.net project pages and mathworks.com FEX pages (403 bot block to curl; SourceForge REST and WebFetch of the FEX pages succeed). http-only URLs: PPP-Wizard and Autoscala-INGV (iononet.ingv.it) — HTTPS does not connect, so left as http.

analysis_zh / desc_zh edits (to stop contradicting the new values):
- 156 Essential-GNSS: "许可证偏宽松 BSD 风格" → "源码头注释为 BSD 三条款许可".
- 199 PPP-Wizard: removed "申请软件包 / 获取方式与许可以官网说明为准"; now says the site only has method, products and monitoring pages, no software download or licence, contact CNES for code; site is HTTP only.
- 313 FARR: "（GitLab，GPL-3.0）" → "（GitLab，GPL-3.0-or-later）".
- 426 nleht-fdtd: "许可与构建说明以仓库为准" → README says copyright reserved, reference use only, no open-source grant, not actively developed.
- 448 pypride: "MIT/GPL 标注并存，以仓内为准" → explains pyproject MIT field vs GPLv3+ classifier, no LICENSE.
- 485 Swarm-VIP-Dynamic: desc "许可以 GitLab 说明为准" → "pyproject 标 Apache-2.0"; analysis likewise.
- 388 IRI-MATLAB-FileExchange: "下载与许可以 File Exchange 为准" → licence.txt BSD 2-clause; code calls the IRI web interface via curl (per FEX "Requires curl.exe" and release notes).
- 507 Zenodo-VTEC: desc + analysis now describe the actual zip (MATLAB + TEC_HourMap.mat, simplified paper code, VTEC only) and CC-BY-4.0.
- 591 EGNOS-Toolkit: "许可 EUPL" → "许可 EUPL v1.1（源码头注明仅限该版本）".
- 576 / 585 SPOCC: licence not published; code on GFZ GitLab behind GitHub-account login.
- 477 ScintPi: notes ZIP holds only PyInstaller executables, no source.

## Task 2 — blank `language`
Candidates: 37 entries with `''`/None/`unknown`. Evidence: `gh api repos/<r>/languages`, recursive git tree extension counts, README, zip listings.

Filled (11):
| idx | name | lang | evidence |
|---|---|---|---|
| 39 | gnsstk-apps | C++ | languages PostScript 2.28 MB (docs), C++ 1.34 MB, TeX/CMake rest; apps are C++ on gnsstk |
| 157 | GAMP_PPPH | C | tree 356 .c vs 88 .m; "Grammatical Framework" bytes are misdetected result files (.ippp/.stec/.resp) |
| 203 | PPPLib | C++ | {"C++":675432,"CMake":3878} |
| 218 | RTKNAVI-BH | C | {"C":2903621,"C++":408138,…} RTKLIB-based |
| 257 | gps-qzss-sdr-sim | C | {"C":241613,"Python":4147,"Makefile":2101} |
| 355 | IonKit-NH (ohm1122) | MATLAB | repo = IonKit-NH.zip (18 .m + sample RINEX/TEC data) + manual; README "a MATLAB-based toolkit"; zip blob sha identical to tanggdut |
| 356 | IonKit-NH-tanggdut | MATLAB | same zip |
| 432 | OASIS-ohm1122 | Python | {"Python":224167} |
| 487 | synthetic_ionospheric_tomography_isl | Jupyter Notebook | {"Jupyter Notebook":1498458} only; follows existing 19 `Jupyter Notebook` entries |
| 505 | vtec | C++ | {"C++":300466,"CMake":3300,"Shell":994} |
| 560 | raw-gnss-fusion | Python | HTML 4.1 MB = results-maps/*.html output; code = 2 .py (demo + util) |
(+ 507 Zenodo-VTEC → MATLAB, 591 EGNOS → C, 477 ScintPi → binary, listed in Task 1.)

Left blank (with reason): awesome-gins-datasets, awesome-gnss-barbeau, awesome-gnss-hdkarimi (lists; convention ''), learning_rtklib / Navigation-Learning / RTKLIB-Manual-CN (course notes; convention ''), BDS-3-PPP-B2b-DATA and BDS-3-PPP-B2b_IMU_LiDAR (data/Download.txt only), GRID and HASlibTestSuite (README only), GNSS_SDR_HACKRF (2 .conf), multi-channel-gnss (configs + submodules), gnss-sdr-1pps (gnss-sdr patch files + confs), INX_Editor (prebuilt binaries in zips), IRTS_SDK (prebuilt .dll/.so + 1 header + 1 example), PRIDE-GeoDataLogger (APK), UNB3m (zip with mixed Fortran/MATLAB), polaris (README: "C and C++ libraries", C 92 kB vs C++ 47 kB — ambiguous), CCMC-IRI-online / GIRO-portal / IRI-indices (service/data pages), ESA-UGI / IMSP-MGS (ESSR JS-rendered, registration-gated), IONOLAB-TEC-Software (login-gated).

## Accuracy fixes found during Task 2
- 355/356 IonKit-NH: `gh api repos/ohm1122/IonKit-NH --jq .parent.full_name` → `tanggdut/IonKit-NH`. Old text had the direction backwards (called tanggdut a "衍生整理版" and told users to diff against "上游 ohm1122"). desc_zh/one_liner_zh/analysis_zh of both rewritten: tanggdut = original (author Tang L.; cite Tang 2024 Earthquake Research Advances), ohm1122 = fork with identical zip.
- 180 HASlibTestSuite: `gh api repos/nlsfi/HASlibTestSuite` size 0, pushed 2022-09-30 07:37 ET; only file README.md = "# HASlibTestSuite1". Old text claimed an official regression suite with fixed samples. desc/one_liner/analysis rewritten as README-only placeholder (same treatment as GRID in batch 40). Removal candidate; not removed.

## Regeneration / validation
- JSON validated; project_count = len(projects) = 1035; counts_by_category and provenance_counts match data (unchanged).
- Dry-run of `research/merge_routine_20260926c` regenerate_lists/regenerate_categories/regenerate_readme before edits: no diff. Re-run after edits: only lists/01,03,04,05,06,07,09 changed; categories.md and README unchanged.
- PROJECTS.json diff: 26 `license`, 14 `language`, 15 `analysis_zh`, 5 `desc_zh`, 3 `one_liner_zh`.

## Leftovers
- 411 MathWorks-ionex_reader: licence still `''`: FEX page hides licence in a modal, and the download zip for this 2024 submission is not fetchable from the box (versions/1–40 404/403). Needs a browser check.
- ESA-UGI / IMSP-MGS / IONOLAB-TEC-Software: language `unknown`, ESSR/IONOLAB pages are JS-rendered or login-gated.
- IRI-COMMON-FILES (385): language `Fortran` but the dir holds only ccir/ursi .asc coefficient files; licence null (no licence file in that dir).
- PPP-Wizard language `C++` could not be verified (no software on site).
- Removal candidates: 180 HASlibTestSuite (README-only), 266 GRID (from batch 40). Duplicates via forks: OASIS-ohm1122 (fork of giorgiopicanco/OASIS, both listed), IonKit-NH ohm1122 (fork of tanggdut, both listed).
