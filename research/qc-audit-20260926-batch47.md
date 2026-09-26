# QC audit — 2026-09-26 batch 47

Base: origin/main `12438e6` (batch 46). Catalog **1029** projects (unchanged; no adds/removes).
Provenance official/academic_lab/personal_community: **333/242/454 → 333/237/459**.

## Task 0 — entries newer than 12438e6
None: origin/main == 12438e6 at start, no peer catalog commits, no new entries to QC.

## Task 1 — merge rule hardened at the root (`research/_merge_fields.py`)

Problem: `prefer_enrichment_value` "upgraded" provenance by rank, replaced weak licences with any
concrete one and short blurbs with longer ones, so re-running an old merge script re-applied stale
finds values (provenance from 20260923b/20260924/20260924g/20260924s/similar_finds, licences from
routine_finds_20260916 / similar_finds / new_finds, gpsd-website language from web_finds).

New rule (documented in the module docstring):
- For an entry that **already exists** in PROJECTS.json, `PROTECTED_FIELDS` = provenance, category,
  subcategory, license, language, desc_zh, one_liner_zh, analysis_zh, url, host are **fill-gap only**.
  Gap = key missing or blank string. No rank upgrades, no "stronger licence", no "richer blurb".
- Explicit JSON `null` is a QC verdict (convention since batch 41: `license: null` = verified none /
  not determinable, `language: null` = site/data), so it is kept — e.g. PPP-Wizard / GMR-Water /
  MCOSB licence null must not be refilled with "see upstream README"; gpsd-website language null must
  not become "C" again.
- Placeholder values ("see upstream README", "unspecified", NOASSERTION, …) never fill anything.
- New entries are untouched by the rule (scripts still build them with full values from finds).
- New `RETIRED_URLS` + `is_retired(url)`: 17 URLs QC removed, merged or rewrote (all catalog URLs in
  PROJECTS.json history that are no longer present), so stale finds cannot re-add them.
- Interface kept: `merge_project_fields(existing, incoming, *, fields=None) -> list[str]`,
  `prefer_enrichment_value(field, old, new)`, `ENRICHMENT_FIELDS`, `FILL_IF_EMPTY_FIELDS`; added
  `PROTECTED_FIELDS`, `set_if_empty`, `is_retired`. Checked with a test: a stale record for an existing
  URL (different provenance/licence/language/category/blurbs) changed nothing; a new URL was appended
  with full values.

Scripts that went around `_merge_fields`, now guarded:
- `apply_web_expansion.py`: `ENRICH` dict, `URL_REWRITE` and the hard-coded gLAB block wrote fields
  directly (e.g. EGNOS-Toolkit licence EUPL-1.1 → "EUPL", language C → "C/C++", analysis reverted).
  Now `set_if_empty` for PROTECTED_FIELDS; `is_retired` stops Caster-source-FTP / GFZ-SPOCC-news /
  IGSMAIL-SPOCC coming back (merged in batch 43). Other issue, left as is: if it ever writes, its
  CAT_META has no `gnss-datasets` and it re-sorts the catalog. It is legacy, so use a merge_routine
  script for new ingestion.
- `_merge_missing.py` (reads its embedded list and writes new_finds.json): `is_retired` stops
  ionex-downloader coming back (empty repo, removed in 0472f42).

### Verification (sandbox copy under /tmp, git diff after each run; shared clone not written)
Before the fix, 9 scripts changed PROJECTS.json/lists/README: merge_routine_20260916 (4 licences + 1),
20260923b, 20260924, 20260924g, 20260924s (provenance/licence), merge_similar_batch2 (11),
apply_web_expansion (3 re-adds + EGNOS-Toolkit), _merge_missing (15 updates + re-add).
After the fix, **every script gives zero diff** (PROJECTS.json, lists/, README.md, docs/, NOTES.md,
research/*.json), run against the final batch-47 state:
merge_data_portals, merge_routine_20260916, 20260921, 20260923, 20260923b, 20260924, 20260924b–s
(18 scripts), 20260926, 20260926b, 20260926c, merge_similar_batch2, apply_web_expansion,
_merge_missing — 30/30 zero-change.
No merge script reads these finds files (nothing to guard): routine_finds_20260914/18/20,
more_finds.json, iri_page_finds.json, iri_related_finds.json. Any future script must go through
`merge_project_fields` / `set_if_empty` / `is_retired`.

## Task 2 — non-GitHub academic_lab review (18 at idx 0–400 + 30 at 401+)
Hosting page / record checked for a named university / institute group. Flipped only where the page
names none (high confidence):

| idx | name | evidence | change |
|---|---|---|---|
| 429 | Okoh-MATLAB-ROT-ROTI | Zenodo 7913105: one creator, no affiliation, no lab | → personal_community |
| 435 | pyFIRI2018 | personal Bitbucket (ozolotov, user); README cites papers, names no lab | → personal_community |
| 444 | pypride | personal GitLab (gofrito, user); README: "Forked version of … from Dima", no institute | → personal_community |
| 464 | SAMI3-3.22-Zenodo | Zenodo 7895858 creator Joe Huba, affiliation **Syntek Technologies** (company) | → personal_community; one-liner "NRL …" → "SAMI3 …"; analysis "(Syntek/NRL) … 官方源码包" → names Syntek as the Zenodo affiliation, "源码包" |
| 474 | Seemala-GPS-TEC | personal Blogspot; no institute on page (location Navi Mumbai) | → personal_community; analysis dropped unsupported "波士顿学院 ISR" |

Kept (group or institute named): 430 Okoh TEC-from-RINEX (Space Environment Research Laboratory,
NASRDA), 473 ScintPi (UT Dallas creators), 503 Zenodo VTEC SBAS (Tampere University), 311 FARR (README:
NJIT + Boston University, NASA LWS grant), 423 nleht-fdtd (README: done at Stanford University,
WIRED), 340 IBP-Model (IAP Kühlungsborn GitLab), 358 IONOLAB (Ionosphere Research Laboratory,
Hacettepe Univ.), 287 ionosphere.cn (STAR Labs @BUAA), 58 plot-Anubis (pecny.cz = Geodetic
Observatory Pecný), UPC gAGE ×7, WHU, CU Boulder ×2, BC ×2, UML/GIRO ×6, UWM ×2, UNR NGL, TU Delft,
MIT GAMIT, Hokkaido (Heki), JHU/APL SuperMAG, UNESP ISMR, CARISMA, VT SuperDARN, OpenMadrigal, CSN
(U. Chile), MACCS (Augsburg), TGO (UiT). FARR/ScintPi/Zenodo-VTEC name universities, not a named
group. They are borderline, so they stay as they are.

## Regeneration
Lists/README regenerated with merge_routine_20260926c's `regenerate_lists` / `regenerate_categories` /
`regenerate_readme`. Its `main()` skips writing when nothing merges, so these were called directly.
Diff: README provenance line, lists/01-ionosphere.md (5 badges + 2 texts). docs/categories.md
unchanged (category counts unchanged).
