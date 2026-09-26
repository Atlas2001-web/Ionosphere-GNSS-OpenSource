# Catalog QC audit — 2026-09-26 batch 32

## Scope
- routine-s `9011da3` (+15, idx 983–997); catalog = **998** (no newer entries past 998)
- Verified via `gh repo view --json licenseInfo,primaryLanguage` + `gh api repos/*/license` + README / tree reads; GAMIT site via curl

## Changes (PROJECTS.json, 20 lines)
| Entry | Fields |
|---|---|
| all 15 | `desc_zh` rewritten (was identical to `one_liner_zh`) |
| GAMIT/GLOBK | `url` http → https (`https://geoweb.mit.edu/gg/` 200, title "GAMIT/GLOBK") |
| GTrop | `license` "unspecified" → null (GitHub: no license file) |
| hamsci_LSTID_detection | `analysis_zh`: "统计与频谱方法" → actual pipeline (distance-time heatmap → edge detection → sinusoid fit, T 1–4.5 h) |
| Qelaro | `analysis_zh`: add SPP (Klobuchar/NeQuick-G), LAMBDA; GUI = NestJS web + FastAPI |
| TropDS | `analysis_zh`: acceptance venue = Journal of Geodesy (2026-06-01, per repo News) |

Lists regenerated via `research/merge_routine_20260924s.regenerate_lists` → only 01/02/04 lines for GAMIT/GTrop/hamsci/Qelaro/TropDS changed.

## Checked, no change
- License: qzsl6tool / AlouetteApp / dvoacap-python show GitHub `NOASSERTION`, but LICENSE files explicitly state BSD-2-Clause / MIT / MIT → catalog values kept. Others match gh SPDX.
- Language: AlouetteApp gh primary = Jupyter Notebook; app itself is Python/Dash → kept `Python`.
- Provenance: all plausible (GMAT/NRL/CSA official; HamSCI academic_lab; saga-utils = IIT space-weather student, kept academic_lab). No flips.
- Dedupe: no URL/name duplicates. AlouetteApp vs `Alouette_ISIS_extract` (idx 285) = related but distinct repos (app vs extraction pipeline) → not merged.

## Counts
- project_count 998 (unchanged) · entries touched 15 · desc_zh 15 · url 1 · license 1 · analysis_zh 3 · provenance 0 · dups 0

## Leftovers
- GAMIT/GLOBK `license` "scientific distribution (request)" and `language` "Fortran/C" are non-SPDX free text (pre-existing convention; left)
