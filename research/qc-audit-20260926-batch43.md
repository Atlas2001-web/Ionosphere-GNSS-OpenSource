# QC audit — 2026-09-26 batch 43 (same-project pairs, borderline categories, leftovers)

Base: origin/main 16e982f (batch 42). Catalog **1032 → 1029** (3 pure-duplicate removals, no adds). Evidence read 2026-09-26 03:27–03:40 ET via curl / WebFetch / `gh api`.

## Task 0 — entries newer than batch 42
None: HEAD = origin/main = 16e982f, `project_count` 1032, no project appended after batch 42. Nothing to QC.

## Task 1 — same-project pairs
| pair | evidence | decision |
|---|---|---|
| BKG-NtripCaster (igs.bkg.bund.de/ntrip/bkgcaster) vs Caster-source-FTP (igs.bkg.bund.de/root_ftp/NTRIP/software/caster/) | Product page: "Beginning on September 2024, the product is distributed free of charge … including the source code … The software can be downloaded here" → link is exactly the FTP dir. FTP dir holds only ntripcaster-2.0.48/2.0.49 tar.bz2 + .sha256, CHANGES, ntripcaster_manual.html (same product, same licence field) | **REMOVED `Caster-source-FTP`** (download location of the same software, not a separate product). Kept `BKG-NtripCaster` (core, featured, canonical page URL); its analysis_zh now names the FTP URL, latest 2.0.49 (2026-06-10), sha256/CHANGES/manual. `docs/software/bkg-ntripcaster.md` already uses the FTP URLs; no doc refs to the removed name |
| SPOCC (gnss.gfz.de/services/spocc) vs GFZ-SPOCC-news (gfz.de section news) vs IGSMAIL-SPOCC (IGSMAIL-8560, 2025-01-24) | All three describe the one GFZ software. News page = release narrative ending "Further information is available at https://gnss.gfz.de/services/spocc"; IGSmail = release announcement pointing to the same service page. Neither is code, docs, or a distinct product | **REMOVED `GFZ-SPOCC-news` and `IGSMAIL-SPOCC`**; `SPOCC` analysis_zh now cites both as release records. `docs/software/spocc.md` §10 side note updated (the news/IGSmail links in that manual stay as sources) |
| gpsd (gitlab.com/gpsd/gpsd) vs gpsd-website (gpsd.io) | gpsd.io is the project's documentation site (install, hardware list, FAQ, news); GitLab is the code | **Kept both**, distinguished: gpsd desc_zh = "软件本体（GitLab 开发主仓）…"; gpsd-website desc_zh = "项目官网（文档站，非代码仓）…源码见 gpsd 条目"; gpsd-website `language` `C` → `null` (website entry, not code; batch-42 convention for non-code entries) |

Extra finding (SPOCC licence): the service page now lists documents "SPOCC Scientific License" v1.0 and "SPOCC GDPR" (`/storage/documents/27UynYL85VJ8io5amHvP4Qynjgjyhkt2pmnNAkXx.pdf`). PDF text: non-transferable licence, access to git.gfz-potsdam.de/gnss/spocc only after signed terms + registration, ENTITY must contribute to IGS/IAG services, operational weighting of non-IGS products not allowed. `license` `null` → `SPOCC Scientific License v1.0 (proprietary; signed terms + registration, IGS/IAG contributors only)`; desc_zh says 登记许可. (docs/software/spocc.md §2 already documents the same licence.)

## Task 2 — borderline categories
- **polaris** (PointOneNav/polaris): README = "C and C++ libraries for interacting with the Point One Navigation RTK Network to receive GNSS RTK corrections" (RTCM 10403, API key). `tools-learning / RTK网络客户端` → **`gnss-positioning / RTK客户端`** (existing label: rtk_client, TouchRTKStation, ELT_RTKBase). `language` `""` → `C/C++` (GitHub bytes: Starlark 112k build files, C 92k, C++ 47k). analysis_zh rewritten from README.
- **gnss2tws-green** (jzshhh/gnss2tws_green): GitHub description "open-source Matlab tool for inferring daily terrestrial water storage changes using GNSS vertical data" — software, not a dataset. `tools-learning / 数据集` → **`gnss-positioning / 大地测量/GNSS`** (existing geodetic-application subcategory holding GAMIT/GLOBK, groops, GARPOS, gnatss).
- pymsis / Python-NRLMSISE-00 / NCAR-GLOW: left (no thermosphere/neutral-atmosphere category; the `中性大气`/`NRLMSISE`/`气辉模型` subcategories they use are already inside ionosphere).
- 56 ionosphere data portals: not touched.

## Task 3 — leftovers
- **IRI-COMMON-FILES**: `license` `null` → `IRI permissive (AS IS + attribution)`. Evidence: IRI-2020 `00readme.txt` lists CCIR%%/URSI%% as package components and says they were published at COMMON_FILES for ≤2016 and are included in 00_iri.zip from IRI-2020; all 24 ccir11–22/ursi11–22 `.asc` in `00_ccir-ursi.zip` are **byte-identical** (cmp) to those in IRI-2020 `00_iri.zip`, whose directory licence `00_iri-License.txt` covers "the Software and associated documentation files".
- **MathWorks-ionex_reader**: not set. curl → Akamai 403; WebFetch renders the page (Bhuvnesh, v1.0.0, 2 Sep 2024) but the "View License" modal is empty; `api.mathworks.com/community/v1/files/172149` 404. Licence text never read, so still blank.

## Regeneration / validation
- Before edits, a dry run of `research/merge_routine_20260926c` regenerate_lists / regenerate_categories / regenerate_readme produced no diff.
- After edits: PROJECTS.json diff = 3 removed objects; BKG-NtripCaster analysis; SPOCC desc/analysis/license; gpsd desc; gpsd-website desc/language; polaris category/subcategory/language/analysis; gnss2tws-green category/subcategory; IRI-COMMON-FILES license; counts. Regenerated lists 01/03/04/05/09, categories.md, README counts. docs/software/spocc.md side note edited by hand.
- JSON valid. project_count 1029 = len(projects). counts_by_category {ionosphere 298, troposphere 49, gnss-data 138, gnss-positioning 106, orbit-clock 31, navigation-ins 73, gnss-sdr 76, mobile-apps 32, tools-learning 57, gnss-datasets 169}. provenance {official 341, academic_lab 355, personal_community 333}. Counts match the data. No duplicate URLs or names. No remaining references to the removed names in docs/lists/README/NOTES.

## Leftovers
- MathWorks-ionex_reader licence (File Exchange licence modal not readable without a browser session).
- Batch-42 leftovers unchanged: gps-qzss-sdr-sim → parent Yuta811x/gnss-sdr-sim, gnssFGO archived-parent commits, ESA-UGI / IMSP-MGS / IONOLAB language `unknown`.
- tools-learning `RTK网络客户端` subcategory is now empty (it had only polaris).
