# QC audit — 2026-09-26 batch 62

- Base: batch 61 ended at `875cb2e` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Checked against origin/main `2e9dfa0`. One peer commit landed after 875cb2e: `2e9dfa0` (pymsis + iri2020 manuals). It is docs-only (docs/software + img); it does not touch PROJECTS.json, lists or `_merge_fields.py`.
- No unpushed peer commits on HEAD. Working tree clean at start; peer stashes (stash@{0..9}) untouched.
- Box time 05:21–05:45 EDT.

## Task 0 — catalog entries changed since 875cb2e

`git diff 875cb2e origin/main -- PROJECTS.json` is empty, so there was nothing new to QC. The catalog still has 1028 entries.

## Task 1 — HTTPS recheck of the seven http-only entries

One `curl --max-time 20` attempt per https twin, with the http URL fetched for comparison:

| Entry | https | http |
| --- | --- | --- |
| CNES-PPP-WIZARD-Realtime-Products | curl 35 `unexpected eof while reading` (TLS abort) | 200 |
| eSWua-TEC | curl 35 | 200 |
| IONORING | curl 35 | 200 |
| PPP-Wizard | curl 35 | 200 |
| Autoscala-INGV | curl 35 | 200 |
| Beihang-Ionosphere-CN | curl 35 | 200 |
| MACCS | curl 35 | 200 |

- **Result:** none switched; this matches batch 61.
- **Controls:** from the same box, www.ingv.it returned https 200, www.augsburg.edu 200 and www.cnes.fr 301. So the box's TLS works; the failure is on these specific hosts.

## Task 2 — fallback manual: `docs/software/noaa-ncn-data.md` (216 lines)

- **Why this one:** none of `NOAA-CORS-AWS`, `NOAA-NCN-API`, `NOAA-CORS-Data-Tree` or `NOAA-UFCORS` had a manual.
  - `noaa-cors-pds` and `ncn-api` did not appear anywhere in docs/software. corsdata was only used in passing, for single files in gdds/varion.
  - All four are anonymous GNSS-archive interfaces. CDAWeb/OMNI, INTERMAGNET/BGS and Madrigal are already covered by space-weather-indices, geomag-api and madrigal.
- **Verified end-to-end** (curl + stdlib Python, tiny fetches):
  - **NCN API:** `cors?id=1lsu` returns 1×53 fields in NAD 83(2011) @2010.0. `ncors` returns the 9 nearest stations; for a point by P041 the first hit is 65.84 m away.
  - **API error handling:** an unknown id returns `200 []`, a missing id returns `200 {"error":…}`, and `x=y=z=0` returns an HTML 500.
  - **S3 layout and paging:** ListObjectsV2 works anonymously. Day 2026-268 has 1605 station prefixes, so paging is needed.
  - **S3 vs corsdata:** P041 2024-001 `.24d.gz` (1769574 B), `brdc0010.24n.gz`, `.24S` and `brdc2680.26n.gz` have identical md5 on both. Download time was 0.14 s from S3 vs 1.0 s from corsdata.
  - **File content:** `.24o.gz` has 2880 epochs at 30 s. The `.S` SUM row shows 94%, MP1/MP2 0.33/0.26 m.
  - **Latency:** 1LSU hourly files land about 15 min after the hour and daily files about 5 h after day end. EarthScope-sourced P041 daily files take about 1.5 days; before that there are only 72 hourly keys.
  - **coord_20 file:** gives ITRF2020 and NAD 83 positions. The NAD 83 values match the API digit for digit, and the ITRF2020 position differs from them by 1.6 m.
  - **UFCORS:** an anonymous curl POST returns a zip. A 1 h request gives 121 epochs. The output is GPS-only unless `GPS=on&GLO=on` is sent. A bad station still returns HTTP 200, with a `text/html` error page.
  - **Batch script:** `ncn_get.py` returned OK×3 with Size checks and flagged MISSING for `zzzz`.
- **Pitfalls documented:**
  - The 2026 S3 XML adds `ChecksumAlgorithm`/`ChecksumType` elements between ETag and Size. An adjacent-field regex then silently lists zero files.
  - S3 keys are case-sensitive: an uppercase station directory returns 404.
  - corsdata lacks the `.24o.gz` that S3 has for P041 2024-001.
  - Rust `crx2rnx` 2.7.0 output is not byte-identical to the official `.o.gz` (24.7 MB vs 15.4 MB, satellites re-ordered). Both have 2880 epochs.
- **Catalog text fixes** (from these tests; provenance/category/subcategory unchanged):
  - `NOAA-NCN-API`:
    - `analysis_zh` rewritten (249 chars). It now names the two endpoints, the NAD 83 datum and the error behaviour.
    - `registration` set to `open` (was absent), with a `registration_zh`.
  - `NOAA-CORS-AWS`:
    - `analysis_zh` rewritten (316 chars). It now covers the key layout, the file types, hourly latency, the md5 match with corsdata, coord/station_log and paging.
    - `registration` set to `open` (was absent), with a `registration_zh`.
  - `NOAA-UFCORS`:
    - `analysis_zh` rewritten (258 chars). It now covers the form fields, the scripted POST, GPS-only by default and the 200-on-error behaviour.
    - `registration_zh` now says no login is needed and curl POST works.
- **Index:** `docs/software/README.md` has a new row 229, a 30-second selector row and a 最近新增 line. Totals are now 229 manuals / 52613 lines.

## Regeneration

- Used `research/merge_routine_20260926c.py` `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main, run with PYTHONDONTWRITEBYTECODE=1.
- The dry run on the untouched data gave zero diff.
- After the edits only `lists/10-gnss-datasets.md` changed (3 analysis lines). categories.md and README.md stayed byte-identical.
- Totals unchanged: 1028; provenance 330/214/484. No duplicate removed, so RETIRED_URLS is unchanged.
