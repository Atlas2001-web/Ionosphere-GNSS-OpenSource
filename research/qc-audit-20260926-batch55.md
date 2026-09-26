# Catalog QC batch 55 (2026-09-26)

Base: `f387e6d` (the categories agent's blurb/CAT_META resync on top of batch 54 `cbfefa0`). Lists were regenerated with the updated `research/merge_routine_20260926c.py` (`regenerate_lists` / `regenerate_categories` / `regenerate_readme`). A dry-run on the unchanged data gave zero diff. Page headers, blurbs and `docs/categories.md` are unchanged.

## Task 0: entries newer than cbfefa0
None. `f387e6d` only touched list blurbs, `docs/categories.md` and CAT_META. No projects were added or removed.

## Task 1: old hostnames in catalog text
Scanned every non-`url` field of PROJECTS.json (`desc_zh`, `one_liner_zh`, `analysis_zh`, `registration_zh`, etc.) for the batch-54 old hosts and paths: swpc.noaa.gov, www.epncb.oma.be, /ftp/obs, ngdc.noaa.gov, isdc/kp.gfz-potsdam.de, aiub /download, AUSPOS path, ICAO Overview.aspx, ENRI /eng, igs.org/wg/bias, magnetometers.bc.edu, openmadrigal.org, unavco /software, www.intermagnet, www.psmsl, essp-sas. The schema has no `docs_url` or `data_url` fields, and `host` holds a hosting type, not a hostname.

**1 fix:**
- GFZ-ISDC-Data-HTTPS `analysis_zh`: changed "与 isdc.gfz-potsdam.de 门户页互补" to "与 isdc.gfz.de 门户页互补". The old host returns 301 to `https://isdc.gfz.de/`.

**Kept (checked, not the same resource or no redirect):**
- NOAA-SWPC-GloTEC `registration_zh`: `services.swpc.noaa.gov` returns 200 and does not redirect.
- SPOCC `analysis_zh`: `git.gfz-potsdam.de/gnss/spocc` returns 302 to that host's own sign-in page. There is no redirect to gfz.de, and the service page names no newer host. Kept because it is doubtful.
- AUSPOS, GA-Positioning-Services, GA-GNSS-Networks: "AUSPOS" appears only as a service name.
- OpenMadrigal: the text mentions `cedar.openmadrigal.org`, which is the current host.

**Other hosts and paths named in text (46), cheap curl check:** all return 200 except the following.
- `irimodel.org`: 406 (bot filter).
- `system.asgeupos.pl`: times out on http and https from the box.
- `garner.ucsd.edu`, `ionosphere.cn`, `gpsmet.geod.bme.hu`: fail on https but return 200 on http.

The ISDC paths `/gnss/data/daily/` and `/gnss/data/highrate/` return 200. No changes were made from this check.

### Old hostnames still in docs/README (not edited; owned by other agents)
README.md, NOTES.md and CONTRIBUTING.md: none. docs:
- `docs/data-access.md` L14, L96, L108, L321: `www.aiub.unibe.ch/download/…`. It still works via 301 to download.aiub.unibe.ch, which then goes to S3. L302, L451: `kp.gfz-potsdam.de` (301 to kp.gfz.de).
- `docs/software/ionex-gim.md` L5, `ionotec.md` L140, `mosgim2.md` L107, `spinifex.md` L48 and L226, `tec-suite.md` L170: `www.aiub.unibe.ch/download/CODE/…`. Suggested replacement: `download.aiub.unibe.ch/CODE/…`, verified 200.
- `docs/software/space-weather-indices.md` L45: `kp.gfz-potsdam.de`. L94: `www.swpc.noaa.gov/ftpdir/…` is a deliberate "old address 404" note; keep it.
- `docs/software/madrigal.md` L3: `https://openmadrigal.org/` (301 to cedar.openmadrigal.org/openmadrigal).
- `docs/software/teqc.md` L3, L43, L55: `www.unavco.org/software/data-processing/teqc/…`. These are deep legacy TEQC pages, not the portal URL that batch 54 changed. Not checked further.

## Task 2: synonym subcategory merges (steering list)
This replaced the singleton re-review. **27 subcategory moves**, all within the same category. Only the PROJECTS.json `subcategory` field was changed.

| category | from | to | n | reason |
|---|---|---|---|---|
| gnss-data | 接收机接口 | 接收机驱动 | 2 | gpsd and gpsd-website: gpsd is a multi-receiver driver daemon, the same scope as the vendor drivers |
| troposphere | VMF产品 | 对流层产品 | 3 | TU Wien VMF1/VMF3/grid product directories are tropospheric product portals, like IGS-Troposphere-WG and EPN-Troposphere |
| troposphere | VMF/GGOS产品 | ZTD/ZWD/VMF | 1 | GGOS-Tropo-RTKLIB is code that computes delays from VMF grids, the same as STD_SWD_Calc (two singletons merged) |
| orbit-clock | VLBI/EOP | EOP与参考系 | 2 | IVS portals produce EOP and reference-frame products alongside the IERS portals |
| gnss-datasets | IGS产品下载 | IGS综合 | 2 | CODE-AIUB download and Earthdata-MGEX are IGS data/product centres, the same as CDDIS, SOPAC garner and files.igs.org |
| gnss-datasets | 国家CORS | CORS区域网 | 12 | CORS区域网 already holds national networks (SWEPOS-RINEX, RENAG, NSGI…) |
| gnss-datasets | NTRIP服务商/CRS | 实时流 | 3 | RAMSAC-NTRIP and TUSAGA-Aktif are the same kind as NSGI-NTRIP; ntrip-catalog lists NTRIP services |
| tools-learning | 资源列表 | 教材与工具索引 | 2 | awesome lists are tool indexes, alongside Navipedia and NGS-GPS-Toolbox |

**Kept distinct:**
- gnss-data RINEX读写 / RINEX工具 / RINEX转换: libraries vs CLI toolboxes vs raw→RINEX converters.
- gnss-data 接收机协议: libsbp and the UBX-MGA converters are protocol libraries, not drivers.
- gnss-positioning PPP / PPP/改正数 / PPP/PPP-AR (and PPP/PPP-RTK): float engines vs SSR/B2b correction decoders vs ambiguity-resolution engines.
- troposphere VMF/GPT官方代码: official code, distinct from product portals.

## Totals
- Projects **1028**, provenance **330/214/484**, category counts unchanged.
- Groups 160 → **152**, singletons 32 → **30**.
- Lists: header count = number of rows in every file, 1028 rows in total, every URL appears exactly once, no duplicate `##` subheadings.
