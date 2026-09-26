# QC audit — batch 54 (2026-09-26)

Base: `7bea565` (1029 projects, provenance 331/214/484, 157 groups, 32 singletons).

## Task 0 — entries newer than 7bea565
None: `origin/main` == `7bea565`; no catalog entries added since batch 53.

## Task 1 — canonical URL pass (catalog-wide, 1029 URLs)
Method: GitHub URLs (680) via `gh api repos/OWNER/REPO` → compare `html_url`; non-GitHub (349) via `curl -sIL --max-time 20` (8 parallel); non-2xx rechecked with GET.

**41 URL changes** on kept entries (2 GitHub + 39 non-GitHub) + 1 pure-duplicate removal.

### GitHub (2)
No renamed/transferred repos. 2 owner/repo **case** fixes to the canonical `html_url` (norm_url-equal → NOT added to RETIRED_URLS, since the lowercase norm would retire the new URL too):
- fixposition_driver: `https://github.com/Fixposition/fixposition_driver` → `https://github.com/fixposition/fixposition_driver`
- LPI: `https://github.com/ilkkavir/lpi` → `https://github.com/ilkkavir/LPI`

### Non-GitHub (39; all 301 permanent redirects to the same resource)
| # | entry | before | after |
|---|---|---|---|
| 1 | CNES-PPP-WIZARD-Realtime-Products | http://www.ppp-wizard.net/products/REAL_TIME | http://www.ppp-wizard.net/products/REAL_TIME/ |
| 2 | EUREF-EPN-Obs-FTP | https://epncb.oma.be/ftp/obs/ | https://epncb.oma.be/pub/obs/ |
| 3 | ROB-IONEX-Products | https://gnss.be/SpaceWeather/Products/IONEX | https://gnss.be/SpaceWeather/Products/IONEX/ |
| 4 | IGS-Bias-Calibration-WG | https://igs.org/wg/bias/ | https://igs.org/wg/bias-and-calibration/ |
| 5 | GFZ-ISDC | https://isdc.gfz-potsdam.de/ | https://isdc.gfz.de/ |
| 6 | GFZ-ISDC-GNSS-Products | https://isdc.gfz-potsdam.de/gnss-products/ | https://isdc.gfz.de/gnss-products/ |
| 7 | GFZ-Kp-Index | https://kp.gfz-potsdam.de/en/ | https://kp.gfz.de/en/ |
| 8 | GFZ-Kp-Data | https://kp.gfz-potsdam.de/en/data | https://kp.gfz.de/en/data |
| 9 | AMBER-Magnetometers | https://magnetometers.bc.edu/ | https://sites.bc.edu/magnetometers/ |
| 10 | OpenMadrigal | https://openmadrigal.org/ | https://cedar.openmadrigal.org/openmadrigal |
| 11 | TU-Wien-VMF-GPT-codes | https://vmf.geo.tuwien.ac.at/codes | https://vmf.geo.tuwien.ac.at/codes/ |
| 12 | CODE-AIUB-Product-Download | https://www.aiub.unibe.ch/download/ | https://download.aiub.unibe.ch/ |
| 13 | ENRI-Japan | https://www.enri.go.jp/eng/index.html | https://www.enri.go.jp/en/index.html |
| 14 | EUREF-EPN-CB | https://www.epncb.oma.be/ | https://epncb.oma.be/ |
| 15 | EUREF-EPN-Data-Access | https://www.epncb.oma.be/_networkdata/data_access/ | https://epncb.oma.be/_networkdata/data_access/ |
| 16 | EUREF-EPN-StationList | https://www.epncb.oma.be/_networkdata/stationlist.php | https://epncb.oma.be/_networkdata/stationlist.php |
| 17 | EUREF-EPN-Coordinates | https://www.epncb.oma.be/_productsservices/coordinates/ | https://epncb.oma.be/_productsservices/coordinates/ |
| 18 | EUREF-EPN-Troposphere | https://www.epncb.oma.be/_productsservices/troposphere/ | https://epncb.oma.be/_productsservices/troposphere/ |
| 19 | AUSPOS | https://www.ga.gov.au/scientific-topics/positioning-navigation/geodesy/auspos | https://www.ga.gov.au/scientific-topics/positioning-navigation/positioning-australia/geodesy/auspos |
| 20 | HAO-TGCM-portal | https://www.hao.ucar.edu/modeling/tgcm | https://www.hao.ucar.edu/modeling/tgcm/ |
| 21 | ICAO-PBN | https://www.icao.int/safety/pbn/Pages/Overview.aspx | https://www.icao.int/safety/pbn/pbn-overview |
| 22 | INTERMAGNET | https://www.intermagnet.org/ | https://intermagnet.org/ |
| 23 | NOAA-EMM | https://www.ngdc.noaa.gov/geomag/EMM/ | https://www.ncei.noaa.gov/products/enhanced-magnetic-model |
| 24 | NOAA-WMM-Portal | https://www.ngdc.noaa.gov/geomag/WMM/ | https://www.ncei.noaa.gov/products/world-magnetic-model |
| 25 | NGDC-Geomagnetism | https://www.ngdc.noaa.gov/geomag/geomag.shtml | https://www.ncei.noaa.gov/products/geomagnetic-data |
| 26 | NGDC-GOES-Satellite | https://www.ngdc.noaa.gov/stp/satellite/goes/ | https://www.ncei.noaa.gov/products/goes-1-15/space-weather-instruments |
| 27 | PSMSL | https://www.psmsl.org/ | https://psmsl.org/ |
| 28 | NOAA-SWPC | https://www.swpc.noaa.gov/ | https://www.spaceweather.gov/ |
| 29 | SWPC-ACE-RTSW | https://www.swpc.noaa.gov/products/ace-real-time-solar-wind | https://www.spaceweather.gov/products/ace-real-time-solar-wind |
| 30 | SWPC-D-RAP | https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap | https://www.spaceweather.gov/products/d-region-absorption-predictions-d-rap |
| 31 | SWPC-GOES-Proton-Flux | https://www.swpc.noaa.gov/products/goes-proton-flux | https://www.spaceweather.gov/products/goes-proton-flux |
| 32 | SWPC-GOES-Xray | https://www.swpc.noaa.gov/products/goes-x-ray-flux | https://www.spaceweather.gov/products/goes-x-ray-flux |
| 33 | NOAA-SWPC-Planetary-K | https://www.swpc.noaa.gov/products/planetary-k-index | https://www.spaceweather.gov/products/planetary-k-index |
| 34 | SWPC-Real-Time-Solar-Wind | https://www.swpc.noaa.gov/products/real-time-solar-wind | https://www.spaceweather.gov/products/solar-wind |
| 35 | SWPC-Solar-Geophysical-Event-Reports | https://www.swpc.noaa.gov/products/solar-and-geophysical-event-reports | https://www.spaceweather.gov/products/solar-and-geophysical-event-reports |
| 36 | SWPC-Solar-Cycle | https://www.swpc.noaa.gov/products/solar-cycle-progression | https://www.spaceweather.gov/products/solar-cycle-progression |
| 37 | SWPC-Solar-Synoptic-Map | https://www.swpc.noaa.gov/products/solar-synoptic-map | https://www.spaceweather.gov/products/solar-synoptic-map |
| 38 | SWPC-WSA-Enlil | https://www.swpc.noaa.gov/products/wsa-enlil-solar-wind-prediction | https://www.spaceweather.gov/products/wsa-enlil-solar-wind-prediction |
| 39 | UNAVCO-Software-Portal | https://www.unavco.org/software/ | https://www.unavco.org/software/software.html |

Notes:
- 4 trailing-slash-only changes (ppp-wizard REAL_TIME, ROB IONEX, TU-Wien VMF codes, HAO TGCM) are norm_url-equal → not retired. The other 35 old URLs + the removed ESSP URL (36) were added to `RETIRED_URLS` in `research/_merge_fields.py` (17 → 53 keys).
- AIUB: `www.aiub.unibe.ch/download/` 301 → `download.aiub.unibe.ch/` 301 → `code.aiub.unibe.ch/s3_script/aiub_s3_bucket_listing.php`; used the stable permanent host `download.aiub.unibe.ch/`, not the PHP script path.
- UNAVCO portal: 301 to `http://…/software/software.html`, then 302 http→https for the same page → used the https final URL.
- SWPC: `www.swpc.noaa.gov` now 301 → `www.spaceweather.gov` (same pages, title "NOAA / NWS Space Weather Prediction Center"); 11 entries. `services.swpc.noaa.gov` (SWPC-Services) does not redirect → unchanged.
- NGDC → NCEI: EMM/WMM/geomag/GOES pages 301 to NCEI product pages; `ngdc.noaa.gov/stp/iono/` does not redirect → unchanged.
- OpenMadrigal: `openmadrigal.org/` 301 → `cedar.openmadrigal.org/openmadrigal` (title "OpenMadrigal"); distinct from CEDAR Madrigal (`cedar.openmadrigal.org/`).
- host fields unchanged and consistent (non-GitHub all `official_site`; GitHub `github`).

### Pure-duplicate removal (1)
- **ESSP-EGNOS-User-Support** (`https://egnos-user-support.essp-sas.eu/`, tools-learning/SBAS, official) now 301 → `https://egnos.gsc-europa.eu/` (title "EGNOS User Support Website"), which is already **EGNOS-GSC-User-Support** (same category/subcategory, official). Removed; old URL in RETIRED_URLS. tools-learning 58→57, official 331→330.

### Not changed (listed)
Temporary redirects (302/307) / login walls:
- `https://doi.org/10.5281/zenodo.{10058636,4905193,7711905,7895858,7913105}` — DOI 302 → Zenodo records (DOI is canonical; kept)
- `https://files.igs.org/` 302 → `/pub/`; `https://renag.resif.fr/` 302 → `/fr/`; `https://space.fmi.fi/image/` 302 → `…/www/index.php`; `https://ccmc.gsfc.nasa.gov/models/SAMI3~3.22` 302 → trailing slash
- `https://gage-data.earthscope.org/archive/gnss` 302 → login page
- `https://cddis.nasa.gov/archive/gnss/`, `…/products/ionex/` 401 → Earthdata login

Permanent redirects not applied:
- `https://glonass-iac.ru/en/` 301 → `/en/about_glonass/` (site root → sub-page; root kept)
- `https://apps.linz.govt.nz/ftp/positionz/` (PositioNZ) 301 → `https://elfi-new.linz.govt.nz/ftp/positionz/` (JS "ELFI Database Search" app on a transitional "-new" host; can't confirm same resource without JS) — kept; flagged for the dead-link patrol

Dead / error (for the dead-link patrol):
- `https://www.ibge.gov.br/en/geosciences/geodetic-network/2421-rbmc.html` 302 → `/en/pagina-404.html` (soft 404)
- `https://www.bev.gv.at/Services/Produkte/Grundlagenvermessung/APOS.html` HEAD: 302 loop → 403 page; GET: 200 (HEAD/bot issue)

HEAD-only failures, GET 200 (OK): igs.bkg.bund.de ×4 (HEAD 404), servicodados.ibge.gov.br ×2 + data.geonet.org.nz (405), gnss.git-pages.gfz-potsdam.de/gfzrnx (502 once), dst.defence.gov.au PHaRLAP (403 on HEAD).
Bot-blocked: mathworks.com File Exchange ×2 (403 on GET too).
Unreachable from box (curl 35 TLS handshake / 60 cert verify; not judged dead): gage.upc.edu ×4, geomag.bgs.ac.uk, imag-data.bgs.ac.uk, helioviewer.org, ivscc.gsfc.nasa.gov, sdo.gsfc.nasa.gov, sohowww.nascom.nasa.gov, srgi.big.go.id, asgeupos.pl ×2, NRCan webapp ×3, nsgi.nl ×2, spaceweather.gc.ca (35); garner.ucsd.edu, sopac-csrc.ucsd.edu, ismrquerytool.fct.unesp.br (60).
http URLs with no https redirect (unchanged): ppp-wizard.net root, eswua.ingv.it, ionos.ingv.it, iononet.ingv.it, ionosphere.cn, space.augsburg.edu/maccs.

## Task 2 — ionosphere/工具 leftovers (9 moves, 0 cross-category)
- new **法拉第旋转** (3): spinifex, RMextract, ionFR (all from 工具) — line-of-sight TEC + rotation measure / Faraday rotation for radio astronomy.
- new **掩星** (3): CDAAC_COSMIC-TEC_Data-Research (from TEC估计), COSMIC-IONPRF-Ne-TEC, IonOccAnalysis (from 工具) — all GNSS-RO ionosphere tools; all three in ionosphere.
- new **磁坐标** (3): apexpy, ocbpy (from 工具), aacgmv2 (from 模型).
- ionosphere 工具 31→24, 模型 35→34, TEC估计 25→24.

## Totals
- projects 1029 → **1028**; provenance **330/214/484**; tools-learning 57; other categories unchanged (ionosphere 247, gnss-datasets 220, …).
- groups 157 → **160**; singletons **32** (unchanged).
- Validation: JSON loads; project_count/counts_by_category/provenance_counts match data; every list header == row count; 1028 list rows == 1028 unique catalog URLs; no duplicate norm_url; no catalog URL is_retired. Regeneration dry-run on 7bea565 gave zero diff before the edits.
