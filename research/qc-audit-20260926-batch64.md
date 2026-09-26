# QC audit — 2026-09-26 batch 64

- Base: batch 63 ended at `48a470a` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- At start, HEAD = origin/main = `48a470a`. Origin later moved to `3efff8e` (docs/software only), and I rebased onto it; regenerating after the rebase gave zero diff. Working tree was clean. No unpushed peer commits on HEAD. I left peer stashes stash@{0..9} alone.
- Box time 05:36–06:00 EDT.

## Task 0: catalog entries changed since 48a470a

`git diff 48a470a origin/main -- PROJECTS.json` is empty, so I had nothing to QC. The only peer commit since then, `3efff8e` (gitm + lompe manuals), landed during this batch. It touches docs/software only, and I rebased onto it before pushing. I skipped the 7 http-only entries as instructed.

## Task 1: moved / deprecated / archived GitHub repos

### DARNtids (tip from 软件手册质检)

- `w2naf/DARNtids` is not archived. Its README starts with "⚠️ DEPRECATED REPOSITORY … migrated and is no longer maintained. New repository: https://github.com/w2naf-academia/DARNtids".
- `w2naf-academia/DARNtids` has tip `6effcd0` (pushed 2026-09-01 13:34 EDT). It is not a fork, has GPL-3.0 and Python, and ★2. PyPI `darntids` 0.2.0 lists it as Homepage/Repository. Its README credits N. A. Frissell, with thesis work at the University of Scranton (Tholley 2023, Guerra 2025).
- The owner is a GitHub "Organization" with no name or bio, used as Frissell's academic account. The work is university research-group code, so per docs/categories.md `academic_lab` stays. This matches the old w2naf entry and the w2naf/IRI_TID entry.
- Entry changes: `url` → `https://github.com/w2naf-academia/DARNtids`, `stars_approx` 4 → 2. License and language are unchanged. I rewrote `analysis_zh`: MSTID toolkit, PyPI darntids, the old repo is deprecated, the current repo uses HDF5 instead of pickle, and it is not a RINEX chain.
- I added the old URL to RETIRED_URLS.
- docs/software/darntids.md line 3 and pitfall 9, plus the docs/software/README.md row 222, used to say that PROJECTS still pointed at the old URL. I reworded them. No hostname lines were touched.

### Sweep of all 680 GitHub URLs (GraphQL, batches of 50; REST readme for candidates)

| Category | Count | Action |
| --- | ---: | --- |
| (a) renamed/transferred (`nameWithOwner` ≠ URL) | 0 | no case-only differences either |
| (b) archived=true | 18 | all 18 already say 归档/archived/只读/弃用 in analysis_zh, so no edits |
| (c) README says deprecated/moved | 3 | DARNtids (above), GPSTk, gnssIR_python |
| (d) 404 / not resolvable | 0 | — |

Archived (b): baidu/ntripcaster, SGL-UT/GPSTk, CGS-GIS/GPSPACE, jks-prv/Beagle_SDR_GPS, osqzss/gps-sdr-sim, matador96/ionex-analyzer, Joshuaalbert/IonoTomo, space-physics/iri90, yujieqing/SegmentsComputation, kristinemlarson/gnssIR_python, purnelldj/gnssr_synth, purnelldj/gnssr_lowcost, u-blox/ubxlib, space-physics/hwm93, osqzss/LimeGPS, Mictronics/pluto-gps-sim, swift-nav/pynex, osqzss/bladeGPS.

README check (c) covered 196 repos: those pushed before 2024, or with "deprecat"/"moved" in the description. rumkex/IonTools has an empty README. Hits:

- **GPSTk** (`SGL-UT/GPSTk`, archived): "THIS PROJECT HAS BEEN MOVED … GPSTk was renamed to GNSSTK and split into … gnsstk and gnsstk-apps". The successor comes from the same org and is a straight rename. It is already in the catalog (`gnsstk`, plus `gnsstk-apps`), so I **removed GPSTk as a pure duplicate** and retired its URL. gnss-data 137 → 136.
- **gnssIR-python** (`kristinemlarson/gnssIR_python`, archived): "gnssIR_python has been deprecated. Please use gnssrefl instead". The successor is by the same author and continues the same GNSS-IR code. It is already in the catalog (`gnssrefl`), so I **removed gnssIR-python as a pure duplicate** and retired its URL. troposphere 48 → 47. `gnssIR-matlab-v3` is a separate MATLAB line and not deprecated, so it stays.
- swift-nav/pynex ("pyNEX (ARCHIVED)") and CGS-GIS/GPSPACE (released as an archived repo on purpose) have no successor. Both are already noted as archived.
- Hits for "please use …" in Aceinna/python-openimu, XiaoGongWei/MG_APP, kristinemlarson/gpssnrpy and yujieqing/Geometric-Matrix… are usage instructions, not deprecation.

Because the sweep found more than DARNtids, I did not write the fallback manual.

## Regeneration and checks

- Used the `regenerate_lists` / `regenerate_categories` / `regenerate_readme` functions from origin/main `research/merge_routine_20260926c.py`, run with PYTHONDONTWRITEBYTECODE=1. The dry run on untouched `48a470a` data gave zero diff.
- After the edits I regenerated, then ran `merge_routine_20260926c.py` itself (ADDED 0 / UPDATED 0 / SKIP_WRITE), then regenerated again. The diff hash was the same before and after, so the merge script adds nothing and the output is idempotent.
- RETIRED_URLS: 53 → 56. No catalog URL is retired, and `is_retired()` is True for all three old URLs. No duplicate norm_url and no duplicate names.
- Totals: 1026 (1028 − 2). Provenance 330/212/484; both removed entries were academic_lab. Counts: ionosphere 247, troposphere 47, gnss-data 136, gnss-positioning 108, orbit-clock 31, navigation-ins 72, gnss-sdr 76, mobile-apps 32, tools-learning 57, gnss-datasets 220.
