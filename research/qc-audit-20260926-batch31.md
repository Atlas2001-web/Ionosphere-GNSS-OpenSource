# Catalog QC audit — 2026-09-26 batch 31

## Scope
- Repo: `Atlas2001-web/Ionosphere-GNSS-OpenSource` (`main`), baseline `da0e077` (after concurrent routine-s `9011da3` → **998** entries)
- No prior batch31 audit / `swds-api-downloader.md` existed → this is batch 31
- Race policy: append-only; no projects added/removed; peer stashes left intact

## Task 1 — GNSS_OSI_download (status honesty)
- DNS: Google DoH + Cloudflare DoH `gnss.osi.ie` → **Status 3 (NXDOMAIN)**, SOA `osi.ie` (gn.gov.ie); Python `gethostbyname` fails
- New official page `https://gnss.tailte.ie/download-rinex.php`: external fetch OK ("Active GNSS Station Data"; banner: RINEX 3 migration from **2026-09-28**, site temporarily unavailable); from this box curl → TLS `unexpected eof` (000)
- Schema has no status/notes key → edited only existing fields: `desc_zh`, `one_liner_zh`, `analysis_zh` (repo `url` unchanged)
- `lists/03-gnss-data.md` regenerated via `research/merge_routine_20260924s.regenerate_lists` (diff = only the OSI lines)
- `docs/software/gnss-osi-download.md`: one-line note on new host + 9/28 outage (peer `4738040` already swapped portal links)

## Task 2 — newest entries scan (idx 953–997 incl. routine-p/q/r; routine-s just landed by peer)
| Check | Result |
|---|---|
| OL==DZ | all `official_site` data-portal walls → **skip** |
| nyx (only code-host in routine-q/r) | `gh repo view` AGPL-3.0 / Rust = catalog already → **0** |
| HTTP URLs | none in newest window |
| Provenance | no high-confidence flip (CSN-Chile `academic_lab` plausible: U. de Chile) |

Catalog field changes beyond Task 1: **0** → Task 3 fallback executed.

## Task 3 — manual
- `docs/software/swds-api-downloader.md` (238 lines): real runs of `-h` (exit 1), missing `-p` (exit 3), long-flag comma bug (exit 2), README example → `SwdsError` host; root cause TLS chain incomplete + `/api/*` **404**; unittest 16 / 3 errors; working alternative `embracedata.inpe.br` (magnetometer `sjc23apr.17m`, IONEX `INPE2660.26I` real downloads)
- `docs/software/README.md` index updated (149 manuals)

## Counts
- `project_count`: **998** (unchanged by this batch)
- Chinese rewrites: 1 entry (3 fields) · license/language/HTTPS/provenance: 0

## Leftovers
1. Portal OL==DZ walls — skip unless policy changes
2. routine-s (+15, `9011da3`) not yet QC'd — next batch
3. GNSS_OSI_download: re-check new Tailte form after RINEX3 migration (≥ 2026-09-28)
