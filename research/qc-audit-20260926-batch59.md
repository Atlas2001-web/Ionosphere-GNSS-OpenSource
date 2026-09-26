# QC audit — 2026-09-26 batch 59

- Base: batch 58 ended at `f2e4478` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Checked against origin/main `8ef1f24`. Two commits landed after f2e4478, both docs-only:
  - `422f6f6`: earthscope-gnsstools QC rerun plus redirect links.
  - `8ef1f24`: BiScEF manual.
- No unpushed peer commits on HEAD. Working tree was clean at start.

## Task 0 — catalog entries changed since f2e4478

`git diff f2e4478 origin/main -- PROJECTS.json` is empty, so there were no new or changed entries to QC.

One correctness fix came out of the Task 1 testing, on `digisondeindices` (added in routine 2026-09-26b):
- **analysis_zh:** it described the package as a working DIDBase client. Verified on the box, PyPI 2.1.0 (and master `2a37ab3`) still calls `lgdc.uml.edu/common/DIDBGetValues`, which returns HTTP 404. The package also omits `pytz` and `dask` from install_requires. The text was rewritten (261 chars) to say this and to point to the manual's fastchar/getbest patch; the CC BY-NC-SA 4.0 note is kept.
- **Other fields confirmed:**
  - URL HTTPS 200.
  - License MIT matches the GitHub API.
  - Language Python.
  - Provenance `personal_community` is correct (individual developer, per docs/categories.md).
  - Subcategory `数据接口` matches Ionosonde-Data-Downloader, ismr_downloader and swds-api-downloader.
  - desc_zh / one_liner_zh are still accurate for the design.
- **Totals unchanged:** 1028; provenance 330/214/484.
- **Regeneration:** `research/merge_routine_20260926c.py` `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main. A dry run on the untouched data gave zero diff. After the edit, only `lists/01-ionosphere.md` changed (one line); categories.md and README.md stayed byte-identical.

## Task 1 — fallback manual

New file: `docs/software/digisondeindices.md` (259 lines). Before writing it I confirmed there was no manual, no index row and no peer untracked file for it.

Verified 2026-09-26 05:01–05:07 EDT. Install was a PyPI wheel into a /tmp venv, no clone. Every tool run used `timeout 120` in a `ulimit -u` subshell. The limit was set to the current user thread count + 400, because a literal 512 is below the ~2700 threads the shared user already runs and made fork fail at once.
- **As shipped:** `ConnectionError` on the 404 URL.
- **Dependencies:** pytz missing; pandas 3.0.6 fails with `output array is read-only` (fixed by pinning `pandas<3`); dask missing for `open_mfdataset`.
- **Python version:** Python 3.11 cannot parse `io.py` (PEP 701 f-string), even though `python_requires` says >=3.7.
- **Endpoint change:** fastchar/getbest does not accept `hF`/`hF2`/`MUFD` and returns columns in request order. A runtime patch (`didb_fix.py`) replaces `web.download` and requests the parser's fixed column order. Values were checked against raw curl lines:
  - MHJ45 2022-01-25 05:00 UTC: foF2 2.0, MUF(D) 6.116, h`F 325.0, hmF2 308.9, B0 56.2, TEC 0.6 TECU → 6e15 m⁻².
- **Month stats:** January 2022 has 8633 rows.
- **Upstream bugs found:**
  - Refreshing the current month, or calling with `forcedownload=True`, crashes with `'NoneType' object has no attribute 'stem'` and leaves an orphan `.txt`. It keeps crashing until the cache files are purged.
  - The "prediction" check compares against local `datetime.today()`, so under TZ=America/New_York the last 4 h of UTC data are rejected.
  - Time arrays spanning two months fail with `InvalidIndexError`, because the boundary timestamp appears in both month files.
  - `nearest` has no tolerance: a query into a 115 min gap returns a record 58 min away.
  - Empty past months are cached permanently.
  - The F2 peak-height variable is named `hmF`, not `hmF2`.
  - The PyPI CLI has a `p.station` typo (fixed on master, not released).
- **Index:** docs/software/README.md was clean. Added row 219 and one selection row, and updated the header count to 219 manuals / 50111 lines (tracked `wc -l`).
- **Not touched:** old-hostname lines in docs/software and docs/data-access.md.

## Hygiene

- **Temp files:** `/tmp/b59dig` held the venv, sources, the package cache inside the venv, and the scripts. The list snapshot is at `/workspace/.b59_tmp_before.txt`. Both are deleted at the end.
- **Disk:** df -h / was 15G available (88%) at start.
