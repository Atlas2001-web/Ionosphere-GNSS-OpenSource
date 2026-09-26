# QC audit — 2026-09-26 batch 60

- Base: batch 59 ended at `b4736a8` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Checked against origin/main `5fcce61`. Two peer commits landed after b4736a8, both docs-only (no PROJECTS.json change):
  - `9680c78`: viresclient + ionosonde-data-downloader QC rerun.
  - `5fcce61`: gim-product-portals manual + data-access E27.
- No unpushed peer commits on HEAD. Working tree clean at start; peer stashes untouched.

## Task 0 — catalog entries changed since b4736a8

`git diff b4736a8 origin/main -- PROJECTS.json` is empty → nothing new to QC. Whole-catalog sanity: no duplicate URL or name. Seven entries are still non-HTTPS (CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN, MACCS); all predate this batch and were left as they are.

One correctness fix came out of the Task 1 testing, on `geomagindices` (routine 2026-09-24g):
- **desc_zh / one_liner_zh / analysis_zh:** these described a working Ap/Kp/F10.7 downloader. Verified on the box with PyPI 1.5.1 (= main `1c76774`):
  - The NGDC FTP daily source is gone (550). The library silently falls back to monthly means with no Kp column: 2024-05-11 returns Ap 24, while the GFZ definitive value is 271.
  - The 45-day forecast URL returns 404.
  - The bundled 20-year forecast has the Ap and F10.7 columns swapped.
  - The order in which the two monthly sources are merged depends on PYTHONHASHSEED.
  - The text was rewritten to say this (analysis 296 chars) and to point to the GFZ API alternative. The old line "README 自述 2018 后读取器待补" was folded into these findings.
- **Other fields confirmed:**
  - URL HTTPS 200.
  - License MIT and language Python match the GitHub API.
  - ★17.
  - Provenance `personal_community` (space-physics is an individual-maintainer org).
  - Subcategory `数据接口` is consistent with digisondeindices, swds-api-downloader and Ionosonde-Data-Downloader.
- **Totals unchanged:** 1028; provenance 330/214/484.
- **Regeneration:** used `research/merge_routine_20260926c.py` `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main, run with PYTHONDONTWRITEBYTECODE=1.
  - The dry run on the untouched data gave zero diff.
  - After the edit only `lists/01-ionosphere.md` changed (2 lines). categories.md and README.md stayed byte-identical.

## Task 1 — fallback manual

New file: `docs/software/geomagindices.md` (188 lines). Before writing it I confirmed there was no manual, no index row and no peer untracked file. The package is a data client used by msise00; its existing manual only mentions it as a dependency.

Verified 2026-09-26 05:09–05:13 EDT on CPython 3.13.5. Install was the PyPI wheel into a /tmp venv (`--no-cache-dir`), no clone. Every run used `timeout 120` in a `ulimit -u` subshell set to user threads + 400.
- **Past dates → monthly means:**
  - 2015-03-17 → the 2015-04 row, Ap 11 / F10.7 129.05. Both values match `ap_monyr.ave` and the SWPC JSON.
  - A 5-element date_range gives 5 identical rows and retries NGDC 5 times.
  - `smoothdays=81` turns into a 3-month trailing mean: f107s 168.42 = mean(155.19, 161.7, 188.37); Aps 15.0.
- **45-day forecast:** the URL returns 404. A runtime rename to `45-day-forecast.txt` (set in both `web` and `dataio`) works: 27Sep26 Ap 10 / F10.7 95 and 05Oct26 Ap 15 / 110, matching the raw file.
- **20-year table:**
  - 2030-01 gives "Ap 73.5 / f107 12.2"; the raw row has F10.7 73.5 and Ap 12.2, so the columns are swapped.
  - A past date queried together with a far-future date gets the 2016 forecast value.
  - Dates after 2030-10 are clamped to the last row.
- **PYTHONHASHSEED 0–5 for 2026-09-20:** 3 runs give NaN at 2026-10-01 and 3 give 2026-08 Ap 9 / F10.7 116.22.
- **tz-aware datetime:** raises TypeError.
- **GFZ Kp JSON API alternative (tiny fetches):**
  - 2024-05-10/11: Ap 105 / 271, Fobs 223.4 / 213.7, Fadj 227.9 / 218.0.
  - 3-hourly Kp peaks at 9.000 at 2024-05-11 00Z (ap 400).
  - GFZ timestamps mark the start of each interval; the old reader placed values at midpoints.
- **Index:** docs/software/README.md was clean. Added row 221 and one selection row, and updated the header to 221 manuals / 50801 lines (tracked `wc -l` + new file).
- **Not touched:** old-hostname lines in docs/software and docs/data-access.md.

## Hygiene

- **Temp files:** `/tmp/b60` (venv, package cache inside the venv, test scripts, f45.txt) was deleted at the end.
- **Disk:** df -h / was 19G available (85%) at start.
