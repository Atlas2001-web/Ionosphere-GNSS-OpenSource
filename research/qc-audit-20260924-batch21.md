# Catalog QC audit — 2026-09-24 batch 21

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24l (`50ae363`): **898** entries; `desc_zh`==`one_liner_zh` **113** (batch20 left 99 @884; +14 routine identicals)
- Goal: QC only (no new projects) — **provenance deep spot-audit** primary; polish new routine-l **software** identicals; HTTPS re-probe; rare SPDX only if gh real; **no** forced OL≠DZ on pure data-portal walls; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine-2026-09-24l entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **113** before → **107** after |
| Empty `license` | unchanged (gh probes null/NOASSERTION — no invent) |
| Empty `language` | unchanged (~30; gh null or weak HTML/PostScript/Starlark/Roff/GF — skipped) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| `project_count` | **898** (unchanged by QC) |

### Prior QC integrity (after pull through routine-l)
Sample Chinese QC intact (OL≠DZ): GFZRNX, m_gim-PANXIONG, libsbp, iri2016, geoveil-cn0. Batch20 provenance keeps intact until this batch's targeted flips. Routine-2026-09-24l (+14) present and preserved (6 software polished; 8 portals left identical intentionally).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail (http_code=000 / ERR) while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed empty/weak-license code hosts via `gh api repos/... --jq .license.spdx_id` — **null** or **NOASSERTION** on empties. No SPDX fills. Empty-language repos returned null or weak languages; skipped.

### Provenance deep spot-audit
Flip only with clear gh bio/org evidence or mixed-org sibling consistency:

| Name | Action | Evidence |
|---|---|---|
| lowtran | personal_community→**academic_lab** | space-physics org bio "Space Physics modeling and analysis"; 11/12 siblings already academic_lab |
| DiffIonMap | personal_community→**academic_lab** | Jin-Whu (Wuhan Univ naming); siblings DRCycleSlip/gstream/IonMap already academic_lab |
| pysatNASA | personal_community→**academic_lab** | pysat org; siblings pysat/pysatCDAAC/pysatModels/pysatSpaceWeather already academic_lab (overrides batch20 verify-keep) |
| cddis-highrate-downloader | personal_community→**academic_lab** | cemalialtuntas company=Yildiz Technical University; siblings GIRAS-GPS-Solutions/NearRealTimeGNSSIR already academic_lab |
| RinexReader | personal_community→**academic_lab** | aaronboda24 company=York University; sibling Loose-GNSS-IMU already academic_lab |
| snapshot-gnss-algorithms | personal_community→**academic_lab** | JonasBchrt company=UKCEH; Cardiff University; sibling raw-gnss-fusion already academic_lab |
| geoveil-mp | personal_community→**academic_lab** | miluta7 company=National CEnter for Cartography (Bucharest); same evidence as geoveil-cn0 batch15 |
| ignav | KEEP personal_community | Erensu loc=WHU only (weak) — prior batch6/7 |
| novatel_gps_driver | KEEP personal_community | SWRI community ROS; vendor-adjacent (batch20) |
| pygnsslab | KEEP personal_community | PyGnssLab community "software lab" branding |
| GDDS | KEEP personal_community | LECUT personal user |
| Geodesy.jl | KEEP personal_community | JuliaGeo community org |
| gnatss | KEEP personal_community | seafloor-geodesy community org |
| SpatioTECformer | KEEP personal_community | research1011 personal |
| GNSSRMERRByS | KEEP personal_community | pjalesSSTL company=SSTL vendor |
| gpsd | KEEP personal_community | gpsd community project |
| ntrip-core | KEEP personal_community | GreenForge Labs commercial |
| NeoGPS / UbxGps / SoftGNSS-octave | KEEP personal_community | personal Arduino/SDR ports |
| bolderflight-ublox / fixposition_driver / python-openimu | KEEP personal_community | vendor OSS drivers (同 libsbp 政策) |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **7** → academic_lab; **16** spot-audits kept
- Chinese rewrites: **6** entries (`desc_zh` ≠ `one_liner_zh`) — routine-2026-09-24l GitHub software only
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **13** (7 provenance + 6 Chinese; no overlap)
- `project_count` unchanged by this QC: **898**
- `lists/*.md` surgically synced (01, 02, 03, 04, 06, 07, 08); README badges already at 898 from routine-l

### Chinese polish strategy
- **Primary:** 6 new routine-2026-09-24l **software** identicals (Arduino/UBX/ROS/SoftGNSS/OpenIMU)
- **Skipped on purpose:** 8 new portal walls (SWS-*, SWPC-*, CelesTrak, ESA-Satellite-Navigation, SpaceWeather-Canada) + remaining ~99 older portal identicals

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | lowtran | personal_community→academic_lab |
| 2 | `provenance` | DiffIonMap | personal_community→academic_lab |
| 3 | `provenance` | pysatNASA | personal_community→academic_lab |
| 4 | `provenance` | cddis-highrate-downloader | personal_community→academic_lab |
| 5 | `provenance` | RinexReader | personal_community→academic_lab |
| 6 | `provenance` | snapshot-gnss-algorithms | personal_community→academic_lab |
| 7 | `provenance` | geoveil-mp | personal_community→academic_lab |
| 8 | `rewrite_zh` | NeoGPS | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | UbxGps | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | bolderflight-ublox | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | fixposition_driver | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | SoftGNSS-octave | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | python-openimu | one_liner_zh, desc_zh |

Chinese rewrite names: NeoGPS, SoftGNSS-octave, UbxGps, bolderflight-ublox, fixposition_driver, python-openimu

Full machine log: `research/_qc_touch_log_20260924_batch21.json`.
Keep audits: `research/_qc_batch21_prov_keep.json`.

## Counts after sync
- `project_count`: **898**
- `counts_by_category`: unchanged by QC (see PROJECTS.json)
- `provenance_counts`: `{"official": 266, "academic_lab": 323, "personal_community": 309}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **107**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 22)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals. Remaining ~107 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language.
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further mixed-org orphans are scarce after this deep audit; new flips need fresh gh bio/company evidence.
6. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
