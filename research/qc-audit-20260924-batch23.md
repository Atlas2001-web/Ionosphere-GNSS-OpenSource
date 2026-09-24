# Catalog QC audit — 2026-09-24 batch 23

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24n (`14d5989`): **926** entries; `desc_zh`==`one_liner_zh` **129**
- Goal: QC only (no new projects) — polish new routine-n **software** identicals; provenance spot-audit personal_community with Lab/Univ/Agency gh evidence (fresh only); HTTPS re-probe; rare SPDX only if gh real; **no** forced OL≠DZ on pure data-portal walls; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine-2026-09-24n entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **129** before → **120** after |
| Empty `license` | unchanged (gh probes null/NOASSERTION — no invent) |
| Empty `language` | unchanged (~30; gh null or weak — skipped) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| `project_count` | **926** (unchanged by QC) |

### Prior QC integrity (after pull through routine-n)
Sample Chinese QC intact (OL≠DZ): NeoGPS, SoftGNSS-octave, geoveil-mp, lowtran, pysatNASA. Batch22 provenance flips intact. Routine-2026-09-24n (+14) present and preserved (9 software polished; 5 portals left identical intentionally).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail (http_code=000) while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed empty-license GitHub hosts via `gh api repos/... --jq .license.spdx_id` — **null** or **NOASSERTION**. No SPDX fills. Empty-language repos returned null or weak languages; skipped.

### Provenance deep spot-audit
Fresh clear gh evidence only (do not re-audit batch22 keep set). Flip with org Lab/Univ or sibling consistency:

| Name | Action | Evidence |
|---|---|---|
| ublox-ros | personal_community→**academic_lab** | KumarRobotics org; kumarrobotics.org = Vijay Kumar Lab, University of Pennsylvania / GRASP |
| iricore | personal_community→**academic_lab** | MIST-Experiment org; blog physics.mcgill.ca/mist/ (McGill-led cosmology experiment) |
| sgp4-rs | personal_community→**academic_lab** | neuromorphicsystems org = International Centre for Neuromorphic Systems; blog westernsydney.edu.au/icns |
| NCAR-GLOW | personal_community→**academic_lab** | space-physics org; 12 siblings already academic_lab (batch21 lowtran policy) |
| pysatMissions | personal_community→**academic_lab** | pysat org; siblings already academic_lab |
| pysatCDF | personal_community→**academic_lab** | pysat org; siblings already academic_lab |
| pymap3d | personal_community→**academic_lab** | geospace-code org; sibling georinex already academic_lab |
| brandon-rhodes/python-sgp4 | KEEP personal_community | hobbyist astronomy maintainer; company null |
| shashwatak/satellite-js | KEEP personal_community | company=@waymo commercial |
| Binabh/TEC-Maps-of-Nepal | KEEP personal_community | personal user; no univ/lab signal |
| Erensu/ignav | KEEP personal_community | loc=WHU only (batch6/7/21/22) |
| perrysou/SoftGNSS-python | KEEP personal_community | IIT spaceweather URL only (batch22) |
| PyGnssLab | KEEP personal_community | community software-lab branding (batch21/22) |
| cryologger | KEEP personal_community | community research hardware org |
| TheGalfins/GNSS_Compare | KEEP personal_community | org description empty on gh |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **7** → academic_lab; **8** spot-audits kept
- Chinese rewrites: **9** entries (`desc_zh` ≠ `one_liner_zh`) — routine-2026-09-24n GitHub software only
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **14** (7 provenance + 9 Chinese; 5 overlap)
- `project_count` unchanged by this QC: **926**
- `lists/*.md` surgically synced (01, 03, 05, 06, 09); README provenance badges synced (279 / 335 / 312)

### Chinese polish strategy
- **Primary:** 9 new routine-2026-09-24n **software** identicals (coords / TEC map / GLOW / pysat / SGP4 family)
- **Skipped on purpose:** 5 new portal walls (ROB-GNSS-be, BIPM-WebTAI-FTP, UNR-GPSNetMap, NGDC-Geomagnetism, OMNIWeb-Data-Explorer) + remaining ~115 older portal identicals

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | ublox-ros | personal_community→academic_lab |
| 2 | `provenance` | iricore | personal_community→academic_lab |
| 3 | `provenance` | sgp4-rs | personal_community→academic_lab |
| 4 | `provenance` | NCAR-GLOW | personal_community→academic_lab |
| 5 | `provenance` | pysatMissions | personal_community→academic_lab |
| 6 | `provenance` | pysatCDF | personal_community→academic_lab |
| 7 | `provenance` | pymap3d | personal_community→academic_lab |
| 8 | `rewrite_zh` | pymap3d | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | TEC-Maps-of-Nepal | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | NCAR-GLOW | one_liner_zh, desc_zh |
| 11 | `rewrite_zh` | pysatMissions | one_liner_zh, desc_zh |
| 12 | `rewrite_zh` | pysatCDF | one_liner_zh, desc_zh |
| 13 | `rewrite_zh` | python-sgp4 | one_liner_zh, desc_zh |
| 14 | `rewrite_zh` | satellite-js | one_liner_zh, desc_zh |
| 15 | `rewrite_zh` | dSGP4 | one_liner_zh, desc_zh |
| 16 | `rewrite_zh` | sgp4-rs | one_liner_zh, desc_zh |

Chinese rewrite names: NCAR-GLOW, TEC-Maps-of-Nepal, dSGP4, pymap3d, pysatCDF, pysatMissions, python-sgp4, satellite-js, sgp4-rs

Full machine log: `research/_qc_touch_log_20260924_batch23.json` (gitignored scratch).
Keep audits: `research/_qc_batch23_prov_keep.json`.

## Counts after sync
- `project_count`: **926**
- `counts_by_category`: unchanged by QC (see PROJECTS.json)
- `provenance_counts`: `{"official": 279, "academic_lab": 335, "personal_community": 312}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **120**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 24)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals. Remaining ~120 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language.
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans scarce after org/sibling sweeps; new flips need fresh gh evidence or new routine owners.
6. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
