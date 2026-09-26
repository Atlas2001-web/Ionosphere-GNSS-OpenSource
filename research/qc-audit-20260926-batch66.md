# QC audit — 2026-09-26 batch 66 (catalog vs today's manuals)

Base: origin/main `59d7961` (batch 65 `f5fb35b` + 2 peer docs commits: ublox8-qzss-almanac-converter manual, crx2rnx/geomagindices QC re-run).

## Task 0 — entries changed by others since f5fb35b
`git diff f5fb35b origin/main -- PROJECTS.json research/_merge_fields.py` is empty. Nothing to QC.

## Task 1 — catalog vs manuals written today
Scope: every `docs/software/*` file added or modified on 2026-09-26 (`git log --after=2026-09-26T00:00Z --diff-filter=AM`). That is 136 paths, of which 116 are `.md` manuals; the rest are assets. The peer's ublox8-qzss-almanac-converter manual landed during this batch and was added, giving **117 manuals**. 112 of them map to catalog entries, **133 distinct entries** in all (some manuals cover several). The other 5 (chain-scintillation, gnss-qc, hifitime, sinex, swarm-data) have no entry. For each entry I compared desc_zh, analysis_zh, registration/registration_zh, and subcategory with the manual's tested findings: the header/verdict lines, the pitfall sections, and the install/access sections. Manuals were not edited.

**Changed: 19 entries (25 fields).** Each edit is short and states only what the manual verified:

| idx | entry | contradiction (manual) | fix |
|---|---|---|---|
| 29 | gnss-downloader | CDDIS rejects anonymous plain FTP (530); WHU NLST 425 → "0 found" | analysis notes that the NASA source fails and WHU can come back empty |
| 74 | rtcm (TS) | MSM 1071–1137 sat/signal fields decoded wrong; stale since 2021 | analysis: framing and non-MSM messages are OK, MSM values are unusable, project stale |
| 58 | prx | not a "3.05 → CSV viewer": computes sat pos/clock/corrections; `prx` entry point TypeError; auto-download mostly broken | desc + analysis rewritten |
| 632 | STD_SWD_Calc | `import CalcSwd` → IndentationError; CDDIS FTPS download fails silently | analysis appended; "Python 包" → "Python 脚本" |
| 81 | swds-api-downloader | login/files API 404, broken TLS chain; data now in embracedata tree | desc + analysis rewritten |
| 116 | GIRO-DIDBase | characteristics are anonymous via fastchar/getbest; only SAO needs an account; DIDBGetValues 404 | registration form_register → **mixed**; registration_zh + analysis |
| 680 | OpenMadrigal | no account on the Madrigal sites; name/email/affiliation are logged only | registration form_register → **open**; registration_zh |
| 670 | madrigalWeb | same finding; "部分实验需注册" was wrong | analysis sentence |
| 706 | TITIPy | FTPS needs an ESA account, but HTTPS on the same server is anonymous | analysis sentence |
| 637 | VARION | Python 2.7 only ("2.7+" was wrong) | analysis sentence |
| 711 | spinifex | on PyPI (2.0); "pip 安装 GitLab 主仓" was misleading | analysis sentence |
| 391 | iricore | manual: OARR user input works in 1.9.0 (catalog line "未实现 OARR" outdated); no Linux wheel | analysis sentence |
| 56 | pinot | core QC still calls TEQC (+qc), so it does not replace TEQC | analysis rewritten |
| 361 | Ionosonde-Data-Downloader | SWS/NICT work; GIRO path uses DIDBGetValues (404) | analysis rewritten |
| 203 | pyRTKLib-RINEX | it wraps rnx2rtkp, and the tip does not run unpatched (sys.exit(6), KeyError 'Tropo', TypeError) | analysis rewritten |
| 101 | COSMIC-GNSS-RO-Data | all COSMIC-2 products on data.cosmic.ucar.edu anonymous; only the old cdaac-www login/tar is 401 | registration_zh |
| 144 | VMF-Data-Server-TropProducts | only the current-year FC is password-protected (401); OP/EI and past FC are open | registration_zh |
| 1004 | MACCS | IAGA-2002 0.5 s files come straight from the form with no account ("数据需申请" was wrong) | desc + analysis; URL untouched (http-only entry kept as http) |
| 18 | EarthScope-gnsstools | RTCM3 only decodes to JSON via gnss-inspect, with no RTCM→RINEX | analysis clause |

Checked and consistent (examples): digisondeindices, geomagindices, GNSS_OSI_download, DARNtids, grinq, SPOCC, tudatpy, CDDIS-IONEX, CAS-BDsmart, galileo-osnma, GAMIT/GLOBK, ublox8-qzss-almanac-converter (new peer manual), crx2rnx, viresclient, Meridian, LISIRD, NOAA NCN/CORS/UFCORS, EPOS-GLASS-API, lstid_processing, hamsci_LSTID_detection. The remaining entries had no tested finding that contradicts their text; generic "注意/局限" wording was left alone.

Not changed (not a contradiction, only a missing detail): GNSSommelier (BKG IONEX 404, JPL IONEX dir misconfigured), ppp-tools (CODE rapid auto-download broken), gps_pvt (segfault with --weight on Ruby 3.3.8), iri2020 (bundled indices end 2023). A later pass could add these.

## Task 2
Skipped: Task 1 produced 19 changes.

## Regeneration and checks
- Used `regenerate_lists` / `regenerate_categories` / `regenerate_readme` from origin/main `research/merge_routine_20260926c.py` (PYTHONDONTWRITEBYTECODE=1). The dry run on untouched `59d7961` gave zero diff.
- After the edits, regeneration touched only `lists/01,02,03,04,10` (analysis text). No count or subcategory changes.
- Totals: 1026 projects, provenance 330/212/484, RETIRED_URLS 56 (no removals). The 7 http-only URLs were not touched.
