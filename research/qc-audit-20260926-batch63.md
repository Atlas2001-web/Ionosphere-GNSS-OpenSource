# QC audit — 2026-09-26 batch 63

- Base: batch 62 ended at `3466b2d` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Peer commits after 3466b2d, all already on origin/main and on local HEAD when I started:
  - `8423f82` darntids/tidd QC
  - `ee3b05a` pymsis/iri2020 QC
  - `ec64284` ntrip-core manual
- All three are docs/software only. None touches PROJECTS.json, lists/ or `_merge_fields.py`.
- No unpushed peer commits on HEAD. Working tree was clean at start. Peer stashes stash@{0..9} were left untouched.
- Box time 05:29–05:45 EDT.

## Task 0 — catalog entries changed since 3466b2d

`git diff 3466b2d origin/main -- PROJECTS.json` is empty, so there was nothing new to QC. The catalog still has 1028 entries.

The seven http-only entries were skipped as instructed; they were already confirmed HTTPS-broken twice.

## Task 1 — fallback manual: `docs/software/epos-glass-api.md` (125 lines)

**Why this one:** `EPOS-GLASS-API` (subcategory 数据接口) had no manual, and `gnssdata-epos` / `GlassFramework` appear nowhere in docs/software. It is an anonymous European GNSS-archive client interface. Other portals I considered are already covered or need accounts:

| Portal | Already covered by / blocker |
| --- | --- |
| INTERMAGNET/BGS | geomag-api |
| OMNIWeb, Kyoto | space-weather-indices |
| Madrigal | madrigal |
| GA | gnss-obs-mirrors |
| NOAA | noaa-ncn-data |
| SuperMAG | account |

**Verified end-to-end** with curl and stdlib Python, tiny fetches:

- **Node facts:**
  - `tools/version` returns GlassFramework-3.4.1.255; the database is `gnss-europe`.
  - The only API description is the WADL (55696 B). Swagger/OpenAPI URLs return 404.
  - `list/station` lists 2462 stations.
- **Station lookups:**
  - GRAS/GRAS00FRA metadata works in short/full and json/csv.
  - bbox 6.5/43.5/7.5/44.0 returns 6 stations. network=RGP returns 294, RENAG 109, France 324.
- **File lookups:**
  - `files/station-marker/GRAS00FRA?epoch_start=2026-09-20&epoch_end=…` treats the dates as an inclusive day range (1 file for a single day, 2 for two days).
  - Each record has md5, file size and the original data-centre URL (EPN HDC or RENAG).
  - An EPN HEAD request gives a Content-Length that matches the GLASS record (2596725).
- **Download and decode:**
  - SOPH00FRA 2026-263 downloaded from RENAG: 1705454 B, and the md5 `c4a29edae6c1…` matches GLASS.
  - `crx2rnx` gives 2880 epochs, RINEX 3.05 G/R/E.
  - The header carries a CC-BY-4.0 licence and DOI 10.15778/resif.rg.
- **Site logs:** `log/<marker>` returns the IGS sitelog text. `log/geodesyml/<marker>` returns a zip containing an XML file.
- **Problems found (documented in the manual):**
  - `files/combination` ignores `date_from`/`date_to` and streams the full history: 3.1 MB still arriving when curl's 80 s timeout hit.
  - `perpage` and `limit` are ignored on station endpoints.
  - The full station dump returns `[]` while the cache is still initialising.
  - `satelliteSystem=GALILEO` returns `[]` for RENAG.
  - `files/rinex_count` always returns 400.
  - Highrate queries returned `[]`.
  - Data becomes queryable about 2–3 days after the observation day.
- **One side effect caused during testing:** a single GET to `stations/v2/stations-json-dictionary/network` returned `Success on updating cache!`, which means it triggers a server cache rebuild. I did not repeat it, and the manual warns readers off it and off the `t0-manager/*` admin endpoints.

**Catalog fix:**
- `EPOS-GLASS-API` `analysis_zh` rewritten from the tests (295 chars). It now covers the node and version, what the endpoints return, WADL-only documentation, ignored parameters, and that GLASS only indexes files that live at other data centres.
- `registration` set to `open` (was absent), with a `registration_zh` covering the anonymous API and the per-data-centre licence (RENAG CC-BY-4.0 + DOI).

**Index:** `docs/software/README.md` has a new row 231, a 30-second selector row and a 最近新增 line. Totals are now 231 manuals / 52960 lines.

## Regeneration

- Used `research/merge_routine_20260926c.py` `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main, run with PYTHONDONTWRITEBYTECODE=1.
- The dry run on the untouched data gave zero diff.
- After the edit only `lists/10-gnss-datasets.md` changed (1 analysis line).
- Totals unchanged: 1028; provenance 330/214/484. No duplicate removed, so RETIRED_URLS is unchanged.
