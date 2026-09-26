# QC audit — 2026-09-26 batch 58

- Base: batch 57 ended at `6ed4509` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Checked against origin/main `3f48521` (commits since 6ed4509: `8f18d4a` swarm-data, `3111f75` data-access hosts, `a569f50` gnss-rtcm-ts, `3f48521` chain-scintillation — all docs-only).

## Task 0 — catalog entries changed since 6ed4509

`git diff 6ed4509 HEAD -- PROJECTS.json` is empty, so there were no new or changed entries to QC. PROJECTS.json is untouched in this batch and was not regenerated. Counts are still **1028** and **330/214/484**.

Spot-checked the entry the new manual covers, `GNSSommelier`:
- URL is HTTPS and returns 200.
- License Apache-2.0 matches the GitHub API; language is Python.
- Provenance `official` is correct (EarthScope org repo, per docs/categories.md).
- Subcategory `下载` matches its siblings (GDDS, gnss-downloader, cddis-highrate-downloader).
- desc_zh "跨十余分析中心" fits the 16 center YAMLs.

No edit needed.

## Task 1 — fallback manual

New file: `docs/software/gnssommelier.md` (EarthScope GNSSommelier, IGS product search/download CLI and library). Before writing it I confirmed there was no existing manual, no index entry and no peer untracked file for it.

Verified on the box, 2026-09-26 04:47–05:00 EDT:
- **Install:** source tarball of tag v0.0.1 (`039d239`), no git clone. The packages are not on PyPI, and the build needs `SETUPTOOLS_SCM_PRETEND_VERSION`.
- **Connectivity:** `probe` reached 11 of 16 servers.
- **search:** ORBIT FIN returned IGS (via BKG) and JPL. IONEX returned 9 results, all through CDDIS FTPS, and the same anonymous listing failed when re-run 5 minutes later.
- **download:** JPL FIN SP3, 1293754 B, 289 epochs, 60 satellites (G31+E29); the lock.json sha256 matched the local file. JPL ERP, 422 B.
- **Error cases:** `GIM`, bad date format, bad `--where`, missing base-dir.
- **Bugs recorded in the manual:**
  - `AAA=` filter has no effect.
  - The `uri` field repeats its scheme prefix.
  - The local cache match ignores `--sources`.
  - BKG IONEX path returns 404; JPL IONEX points at the wrong directory.
  - `search --to` caused a runaway thread storm (`can't start new thread`) and had to be killed. The manual warns against running it on shared machines.
- **Not tested:** CDDIS authenticated download, pride-ppp, resolve_dependencies.

Index: docs/software/README.md was clean, so I added table row 217 and one selection-table row.

No lines in docs/software old-hostname content or docs/data-access.md were touched.
