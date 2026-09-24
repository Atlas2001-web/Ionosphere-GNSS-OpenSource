# Catalog QC audit — 2026-09-24 batch 24

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24o (`ca7ce02`): **940** entries; `desc_zh`==`one_liner_zh` **134**
- Goal: QC only (no new projects) — polish new routine-o **software** identicals; provenance spot-audit with fresh gh evidence only; HTTPS re-probe; rare SPDX only if gh real; **no** forced OL≠DZ on pure data-portal walls; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine-2026-09-24o entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **134** before → **129** after |
| Empty `license` | unchanged (gh probes null/NOASSERTION — no invent) |
| Empty `language` | unchanged (~30; gh null or weak PostScript/Roff/HTML/Starlark/GF/OpenEdge — skipped) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| `project_count` | **940** (unchanged by QC) |

### Prior QC integrity (after pull through routine-o)
Sample Chinese QC intact (OL≠DZ): NeoGPS, SoftGNSS-octave, geoveil-mp, lowtran, pysatNASA. Batch23 provenance flips intact. Routine-2026-09-24o (+14) present and preserved (5 software polished; 9 portals left identical intentionally).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed **all 156** empty-license GitHub hosts via `gh api repos/... --jq .license.spdx_id` — **null** or **NOASSERTION** only (0 fills). Empty-language repos: null or weak (PostScript/Roff/HTML/Starlark/GF/OpenEdge ABL); no strong-language fills.

### Provenance deep spot-audit
Fresh gh evidence only on routine-o owners + residual PC keep sweep. Flip threshold: clear Lab/Univ/Agency org or company. **No flips** this batch (orphans scarce after batch22/23 sweeps).

| Name | Action | Evidence |
|---|---|---|
| SWxTREC/pymsis | ALREADY **academic_lab** | org = Space Weather Technology, Research and Education Center; blog colorado.edu/spaceweather (CU Boulder) |
| DeepHorizons/Python-NRLMSISE-00 | KEEP personal_community | user Joshua Milas; company/bio null; Rochester NY personal |
| pothosware/SoapySDR | KEEP personal_community | Pothosware community FOSS org (pothosware.com); not univ/lab |
| pothosware/SoapyHackRF | KEEP personal_community | same community org |
| pothosware/SoapyPlutoSDR | KEEP personal_community | same community org |
| Erensu/ignav | KEEP personal_community | loc=WHU only (batch6/7/21/22/23) — not re-opened |
| pjalesSSTL/GNSSRMERRByS | KEEP personal_community | company=Surrey Satellite Technology Ltd. vendor (batch21) |
| daniestevez/galileo-osnma | KEEP personal_community | company/bio null; personal researcher Madrid |
| swri-robotics | KEEP personal_community | prior vendor-adjacent keep (batch22) |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **0**; **9** spot-audits kept / already-correct
- Chinese rewrites: **5** entries (`desc_zh` ≠ `one_liner_zh`) — routine-2026-09-24o GitHub software only
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **5**
- `project_count` unchanged by this QC: **940**
- `lists/*.md` surgically synced (01, 07); README provenance badges unchanged (288 / 336 / 316)

### Chinese polish strategy
- **Primary:** 5 new routine-2026-09-24o **software** identicals (NRLMSIS family + SoapySDR stack)
- **Skipped on purpose:** 9 new portal walls (ASG-EUPOS, ASG-EUPOS-Services, CROPOS, SWEPOS-Portal, GSI-Terras-GEONET, SWPC-ACE-RTSW, LISIRD, BGS-INTERMAGNET-Data, NGDC-GOES-Satellite) + remaining ~120 older portal identicals

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `rewrite_zh` | pymsis | one_liner_zh, desc_zh |
| 2 | `rewrite_zh` | Python-NRLMSISE-00 | one_liner_zh, desc_zh |
| 3 | `rewrite_zh` | SoapySDR | one_liner_zh, desc_zh |
| 4 | `rewrite_zh` | SoapyHackRF | one_liner_zh, desc_zh |
| 5 | `rewrite_zh` | SoapyPlutoSDR | one_liner_zh, desc_zh |

Chinese rewrite names: Python-NRLMSISE-00, SoapyHackRF, SoapyPlutoSDR, SoapySDR, pymsis

Full machine log: `research/_qc_touch_log_20260924_batch24.json` (gitignored scratch).
Keep audits: `research/_qc_batch24_prov_keep.json`.

## Counts after sync
- `project_count`: **940**
- `counts_by_category`: unchanged by QC (see PROJECTS.json)
- `provenance_counts`: `{"official": 288, "academic_lab": 336, "personal_community": 316}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **129**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 25)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals. Remaining ~129 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language (156+30 probed this batch: none).
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans scarce after org/sibling sweeps; new flips need fresh gh evidence or new routine owners.
6. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
