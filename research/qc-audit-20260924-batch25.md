# Catalog QC audit — 2026-09-24 batch 25

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after QC batch24 (`ea1e59a`) + later docs-only commits: **940** entries; `desc_zh`==`one_liner_zh` **129** (all portal walls)
- Goal: QC only (no new projects) — no new routine since routine-o; provenance spot-audit with fresh gh evidence; HTTPS re-probe 6 leftovers; rare SPDX only if gh real; **no** forced OL≠DZ on portal walls; no core/featured bulk flip; small honest batch OK
- Dedicated catalog-only commit
- **Race policy:** preserve concurrent docs/WIP and any fresh routine entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **129** (0 code-host; all official_site / data-portal) |
| Empty `license` | 169 total / **156** GitHub — probed; null/NOASSERTION only |
| Empty `language` | **34** — probed GitHub hosts; null or weak (PostScript/Roff/HTML/Starlark/GF/OpenEdge) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| New routine since batch24 | **none** (count still 940) |
| `project_count` | **940** (unchanged by QC) |

### Prior QC integrity
Sample Chinese QC intact (OL≠DZ): pymsis, SoapySDR, NeoGPS, SoftGNSS-octave, geoveil-mp. Batch24 Chinese polish intact. No new routine-p ingest to polish.

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail (`http_code=000`) while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed **156** empty-license GitHub hosts via `gh api repos/... --jq .license.spdx_id` — **null** or **NOASSERTION** only (**0** fills). Empty-language GitHub hosts: null or weak languages only; **0** strong-language fills.

### Provenance deep spot-audit
Fresh gh evidence only. Flip threshold: clear Lab/Univ/Agency org **or** sibling consistency under the same org. Vendor / FOSS community orgs kept.

| Name | Action | Evidence |
|---|---|---|
| ros-drivers/nmea_navsat_driver | personal_community→**official** | org = ROS device drivers SIG (`ros.org/wiki/sig/Drivers`); sibling `nmea-msgs` already **official** |
| gnsscusdr/CU-SDR-Collection | KEEP personal_community | User; company/blog/bio null — “CU” name alone insufficient |
| SkydelSolutions/NeQuick2-MLF2 | KEEP personal_community | Safran Trusted 4D Canada Inc. vendor |
| AgOpenGPS-Official/AgOpenNtripCaster | KEEP personal_community | DIY AgOpenGPS community org |
| oscimp/gnss-sdr-1pps | KEEP personal_community | OscillatorIMP FOSS org; no univ/lab |
| PointOneNav/polaris | KEEP personal_community | Point One Navigation vendor |
| seafloor-geodesy/gnatss | KEEP personal_community | Seafloor Geodesy community org |
| CS-SI/Orekit | KEEP personal_community | CS GROUP commercial aerospace vendor |
| MapIV | KEEP personal_community | MAP IV Inc. (map4.jp) |
| rokubun | KEEP personal_community | Rokubun commercial GNSS company |
| go-gnss | KEEP personal_community | Community Go GNSS FOSS org |
| PyGnssLab | KEEP personal_community | community software-lab branding (batch21–23) |
| barbeau | KEEP personal_community | company=Google; personal user |
| Erensu/ignav | KEEP personal_community | loc=WHU only (batch6/7/21–24) |
| pjalesSSTL/GNSSRMERRByS | KEEP personal_community | SSTL vendor (batch21/24) |
| swri-robotics | KEEP personal_community | prior vendor-adjacent keep (batch22/24) |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **1** → official; **15** spot-audits kept
- Chinese rewrites: **0** (no code-host identicals; portal walls skipped on purpose)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **1**
- `project_count` unchanged by this QC: **940**
- `lists/*.md` surgically synced (06); README provenance badges synced (**289 / 336 / 315**)

### Chinese polish strategy
- **Skipped on purpose:** all **129** remaining identicals are portal / official_site walls (no new routine software this cycle)

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | nmea_navsat_driver | personal_community→official |

Chinese rewrite names: *(none)*

Full machine log: `research/_qc_touch_log_20260924_batch25.json` (gitignored scratch).
Keep audits: `research/_qc_batch25_prov_keep.json`.

## Counts after sync
- `project_count`: **940**
- `counts_by_category`: unchanged by QC (see PROJECTS.json)
- `provenance_counts`: `{"official": 289, "academic_lab": 336, "personal_community": 315}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **129**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 26)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals. Remaining ~129 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language (156+~30 probed this batch: none).
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans scarce after org/sibling sweeps; new flips need fresh gh evidence or new routine owners. Vendor orgs (CS-SI/Orekit, Aceinna, Swift-Nav, etc.) intentionally kept PC under current policy.
6. Guard against routine-merge / concurrent-docs races — rebase-before-push; never strip fresh routine entries or unrelated WIP when resolving races.
