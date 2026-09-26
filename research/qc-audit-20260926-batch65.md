# QC audit 2026-09-26 batch 65

## Start state

- HEAD = origin/main = `8575497` (batch 64). Working tree clean, no untracked files, no unpushed peer commits. Peer stashes stash@{0..9} left untouched.
- Catalog at start: 1026 projects, provenance official/academic_lab/personal_community = 330/212/484, RETIRED_URLS 56.

## Task 0: peer changes since 8575497

- None. origin/main later moved to `d2d4fae` (peer QC of gitm/lompe) and then to `db500ae` (peer manuals iricore + ntcmg). Neither touched PROJECTS.json. I rebased onto both and resolved the manual-count line conflict in docs/software/README.md. No catalog entries changed, so there was nothing to QC.

## Task 1: repos not hosted on GitHub

Scope: every PROJECTS.json URL that is not on github.com and points at a code forge or a code deposit (24 entries). The 7 http-only entries were skipped.

| Host | Entries | Method | Result |
| --- | --- | --- | --- |
| gitlab.com | 9 (EarthScope-gnsstools, gpsd, FARR, gri-iono, nleht-fdtd-ionosphere, pypride, Swarm-VIP-Dynamic, swarm-vip-dynamic-models, earthscope-sdk) | REST `/api/v4/projects/:path?license=true` + GraphQL `archived` | All resolve at the same path (no renames). None archived. Last activity ranges from 2025-07 (nleht/fdtd) to 2026-09-26. |
| git.astron.nl (self-hosted GitLab) | spinifex | same | Same path, not archived, Apache-2.0, active 2026-09-24. |
| igit.iap-kborn.de (self-hosted GitLab) | IBP-Model | same | Same path, not archived, MIT. |
| bitbucket.org | pyFIRI2018 | `api.bitbucket.org/2.0/repositories` | Public, same path, last updated 2022-09-19. |
| sourceforge.net | Essential-GNSS (`gnsstk`), EGNOS-Toolkit (`libegnos`) | `/rest/p/<project>` | Both status active with no `moved_to_url`. Licenses BSD and EUPL match the catalog. |
| Zenodo DOIs | Okoh ROT/ROTI, Okoh TEC-from-RINEX, SAMI3-3.22, ScintPi-1.0, VTEC-map-SBAS | DataCite API (zenodo.org returns 403 to this box) | All CC-BY-4.0, which matches the catalog. Each record has a single version, so no newer DOI to switch to. |
| Other pages | GFZRNX guide, gpsd.io, GPSBabel, Seemala blog | HTTP | All 200. |

- License/language checks where the catalog value looked doubtful:
  - Swarm-VIP-Dynamic: GitLab reports no license because the repo has no LICENSE file; pyproject says "Apache License v2.0". The catalog already says this, so no change.
  - pypride: pyproject still says MIT while the classifier says GPLv3+, and there is still no LICENSE file. The catalog already notes the conflict, so no change.
  - MathWorks-ionex_reader: license field is empty. The File Exchange page only has a "View License" pop-up and the package download returned 404, so I could not verify it. Left empty; reported only.
- Result: **0 URL changes, 0 archived notes needed, 0 deprecations, 0 404s, 0 removals.** RETIRED_URLS unchanged at 56.

## Task 2: fallback manual, `docs/software/grinq.md`

- Target: `grinq` (PJarrin/grinq, MIT, tip `d0891d2`). It is an anonymous multi-centre RINEX daily-file downloader that had no manual, and it is not in any excluded area. I read the source from the GitHub tarball (332 KB) and installed it in a temporary Python 3.11 venv.
- Real downloads (DOY 200 of 2026, plus SOPAC 2017-365 and 2018-001), about 40 MB in total, all deleted afterwards:
  - Worked: sopac, ngs, gfz, gink, nzealand, euref, noanet, renag (RINEX 2 and 3).
  - Failed: argn saves an S3 HTML page as `.crx.gz` and reports success; ramsac returns 404 even at the server root; cacsa fails with an SSL EOF error.
  - FTP centres (ign, cddis): `425 Security: Bad IP connecting` from this box's NAT, so these are untested here and not blamed on upstream.
- Upstream bugs I reproduced:
  - `requests` is missing from install_requires.
  - `-login` raises ValueError (unpacks 4 values from a function that returns 5).
  - `-hrate` with a 9-char site, or with a centre that has no high-rate branch, raises UnboundLocalError.
  - For RENAG, the RINEX 3 remote path gets corrupted across candidate names (`rinex3x3/…/20/`).
  - The ARGN host contains an `index.html#public` fragment.
  - The mirror script cannot find a system lftp unless `CONDA_PREFIX` is set, and it passes the remote dir as lftp `-P` (caught with a fake lftp that printed its arguments).
  - Exit code is 0 on every failure.
  - `-rename` only renames the file; the content stays CRINEX 3.
  - Latest earthscope-sdk (1.6.1) lacks `DeviceCodeFlowSimple`.
- Catalog entry `grinq` changed to match the tests: desc_zh, analysis_zh and one_liner_zh rewritten; subcategory 质量检查 → 下载, because download is the working core and QC needs a registered Anubis binary. License MIT and language Python confirmed. Provenance stays personal_community (single researcher's personal repo).
- `docs/software/README.md`: count 235 → 238 and total lines 53910 → 54430 (after rebasing onto peers d2d4fae and db500ae, which added iricore + ntcmg); added row 238 and one task-index row.

## Regeneration and checks

- Used `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main `research/merge_routine_20260926c.py` with PYTHONDONTWRITEBYTECODE=1. The dry run on untouched `8575497` data gave zero diff.
- Regenerating again after the rebase gave zero further diff.
- After the grinq edit, the only regenerated change was `lists/03-gnss-data.md` (the entry moved to subcategory 下载). No count changes.
- Totals: 1026 projects, provenance 330/212/484, RETIRED_URLS 56.
