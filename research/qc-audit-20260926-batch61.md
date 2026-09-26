# QC audit — 2026-09-26 batch 61

- Base: batch 60 ended at `84999e9` (1028 projects, provenance official/academic_lab/personal_community = 330/214/484).
- Checked against origin/main `c44e5f6`. Six peer commits landed after 84999e9, all docs-only (no PROJECTS.json, lists or `_merge_fields.py` change): `fbe4caa`, `d75fcc9`, `f60e4b8`, `09e8d38`, `e8d1e03`, `c44e5f6`.
- No unpushed peer commits on HEAD. Working tree clean at start; peer stashes untouched.
- Box time 05:13–05:40 EDT.

## Task 0 — catalog entries changed since 84999e9

`git diff 84999e9 origin/main -- PROJECTS.json` is empty, so there was nothing new to QC. Whole-catalog check: no duplicate URL or name (1028).

## Task 1 — non-HTTPS URLs

The only `http://` values in PROJECTS.json are the `url` fields of the seven known entries. No other field (homepage, docs or data link, or text) contains `http://`.

Method: `curl -sSL --max-time 20` on the http URL and on its https twin, then compared the `<title>` and the body. Every https attempt was retried 3× and also tried with `--http1.1` and `-4`. Also ran `openssl s_client` and a second vantage (WebFetch).

| Entry | http (live?) | https |
| --- | --- | --- |
| CNES-PPP-WIZARD-Realtime-Products | 200, "Index of /products/REAL_TIME", 6.3 MB listing | TLS handshake aborted (curl 35 `unexpected eof`) |
| eSWua-TEC | 200, "eSWua landing page" | curl 35 |
| IONORING | 200, "IONORING" | curl 35 |
| PPP-Wizard | 200, "The PPP-Wizard Project" | curl 35; WebFetch 500 |
| Autoscala-INGV | 200, "Software Download" | curl 35 |
| Beihang-Ionosphere-CN | 200, "Ionosphere and Space Weather" | curl 35; WebFetch 500 |
| MACCS | 200, "Magnetometer Array for Cusp and Cleft Studies" | curl 35; WebFetch 500 |

- **Result:** none switched; all seven http sites are alive.
- **Handshake detail:** on port 443 the TCP connection opens, then the server closes it before sending a certificate (`CONNECTED` → `unexpected eof`).
- **Controls:** example.com, ingv.it, cnes.fr, augsburg.edu and github.com all returned https 200 from the same box.
- **Caveat about the box's network:** `www.spaceweather.gc.ca` returned https 200 on some attempts and failed on others (curl 35). The six hosts above failed on every attempt, 3/3 each, and the WebFetch vantage agreed. Recheck these seven next batch.

## Task 2 — fallback manual: `docs/software/lisird.md` (190 lines)

- **Why LISIRD:** it is a catalog entry (gnss-datasets/地磁空间天气, official) with no manual.
  - Other space-weather portals are already covered: CDAWeb/OMNI/Kyoto/GFZ/SWPC → space-weather-indices; INTERMAGNET/USGS/MACCS/THEMIS → geomag-api; Madrigal → madrigal; ICON/GOLD → icon-gold-data.
  - SuperMAG needs a registered user name, so it cannot be verified without an account.
- **What was verified end-to-end** (curl + stdlib Python, 2026-09-26 05:10–05:30 EDT; tiny fetches):
  - LaTiS `catalog.json` lists 281 datasets. `.das`/`.dds` give units and missing values. `.info` returns 500 (no such writer).
  - Penticton F10.7 near-noon values for 2024-05-08…11 are 227.1/233.2/223.4/213.7. They are identical to GFZ `Fobs`. For 2026-09-25, LISIRD gives 105.4 = GFZ 105.4, while SWPC gives the integer 105.
  - Column selection, numeric filters, `format_time`, `last()`, and the `csv/json/jsond/txt` formats all work. Full `penticton_radio_flux.csv` is 1,150,736 B.
  - `noaa_radio_flux` stopped updating on 2018-04-30 (2024 queries return an empty 200).
  - `fism_daily_hr.dds` returns 400 "Limit exceeded … allowed 25000000". An exact-float `wavelength=121.5` returns an empty table. FISM time is `yyyyDDD`.
  - GOES-18 XRS longwave peaks at 3.88e-4 W/m² at 2024-05-10 06:54 UT (X3.9).
  - HAPI is version 2.0 with 29 datasets and CSV only. The 3.x `dataset/start/stop` syntax returns 1400, and `format=json` returns 1409.
  - F10.7 timestamps come out at xx:43 because LISIRD uses the DRAO `fluxjulian` column.
  - End-to-end script `f107.py`: 101 rows; 2024-05-10 F10.7obs 223.4; 81-day centred mean 176.2.
- **Catalog text fix (LISIRD):**
  - `analysis_zh` was a generic one-liner. It now names the key datasets, the two interfaces and their limits, and anonymous access (249 chars).
  - `registration_zh` said "部分服务需注册". The tests showed both LaTiS and HAPI work anonymously, and the field now says so.
  - Provenance was left `official`, in line with sibling mission/data-centre portals such as THEMIS GMAG (SSL Berkeley) and CODE.
- **Index:** `docs/software/README.md` has a new row 226, a 30-second selector row, and updated totals (226 manuals / 51936 lines).

## Regeneration

- Used `research/merge_routine_20260926c.py` `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main, run with PYTHONDONTWRITEBYTECODE=1.
- The dry run on the untouched data gave zero diff.
- After the LISIRD edit only `lists/10-gnss-datasets.md` changed (1 line). categories.md and README.md stayed byte-identical.
- Totals unchanged: 1028; provenance 330/214/484. No duplicate removed, so RETIRED_URLS is unchanged.
