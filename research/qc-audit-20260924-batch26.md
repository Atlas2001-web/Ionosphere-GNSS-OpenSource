# Catalog QC audit — 2026-09-24 batch 26

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after QC batch25 (`2222482`) + routine-p (`549a092`, +14 → 954) + concurrent docs link of **rinex2bin** (`4245b8f` → **955**)
- Goal: QC only (no new projects) — prefer newer ingestion rounds **i–p** (batch15–17 era through routine-p); Chinese polish on code-host; high-confidence provenance only; HTTPS re-probe 6 leftovers; rare SPDX only if gh real; **no** portal OL≠DZ walls; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve concurrent docs/WIP and fresh routine entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **138** (0 code-host; all official_site / data-portal walls) |
| Empty `license` | 169 total / **156** GitHub — sample re-probe null/NOASSERTION |
| Empty `language` | **34** — SoftGNSS-octave still gh=`Objective-C` (weak; leave) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| Newer rounds i–p GitHub software | **53** present; Chinese already OL≠DZ; lic/lang filled |
| Concurrent new entry | **rinex2bin** (nav-solutions) linked by docs commit; missing from `lists/03`; `provenance_counts.personal_community` stale **320** vs actual **321** |
| `project_count` | **955** |

### Prior QC integrity
Sample Chinese QC intact (pymsis, SoapySDR, NeoGPS, SoftGNSS-octave, nmea_navsat_driver official). Routine-p fourteen names present. Batch25 KEEP provenance set not re-opened.

### HTTPS probe (curl -sI -L --max-time 12/15)
Matching HTTPS still fail (`http_code=000`) including host/path variants; HTTP originals return **200**. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
- Newer i–p: **0** empty license/language among GitHub software
- Random sample **20**/156 empty-license GitHub hosts via `gh api … --jq .license.spdx_id` — **null** or **NOASSERTION** only (**0** fills)
- SoftGNSS-octave: gh language remains Objective-C only — **no invent**

### Provenance deep spot-audit (newer PC GitHub; stricter)
Flip threshold: clear Lab/Univ/Agency org **or** sibling consistency under an org already **official**. Fresh `gh api users/{owner}` only. Do **not** re-litigate batch25 KEEP set.

| Owner / name | Action | Evidence |
|---|---|---|
| nav-solutions (incl. new rinex2bin) | KEEP personal_community | Org bio GNSS FOSS (France); all 12 catalog siblings already PC |
| pothosware (Soapy* ×5 from routine-p + prior) | KEEP personal_community | Pothosware FOSS suite; no univ/lab |
| osqzss | KEEP personal_community | User Takuji Ebinuma; personal |
| swift-nav / novatel / Fixposition / Aceinna / bolderflight | KEEP personal_community | Commercial vendor orgs (policy) |
| swri-robotics | KEEP personal_community | batch25 KEEP; not re-opened |
| 107-systems / ublox-rs | KEEP personal_community | Community FOSS orgs |
| csobey, vincenthumphrey, DeepHorizons, Binabh, kristianpaul, stevemarple, AlvaroTena, nbtk, … | KEEP personal_community | Users; company/bio null or non-lab |
| **Sibling mixed-provenance among newer PC orgs** | **none** | All newer PC orgs internally consistent |

**Flips this batch: 0** (no Lab/Univ/Agency evidence among newer PC set)

### Chinese polish strategy
- **Skipped on purpose:** all **138** remaining identicals are portal / official_site walls
- **Polished:** concurrent newer code-host **rinex2bin** (tighten OL≠DZ + analysis after docs link-in)
- Routine-p Soapy* software Chinese already differentiated at ingest — left intact

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance flips: **0**; **28** newer-PC-org spot-audits kept
- Chinese rewrites: **1** (rinex2bin)
- Meta sync: `provenance_counts.personal_community` 320→**321** (match actual after rinex2bin)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **1** (rinex2bin fields) + meta counts
- `project_count` unchanged by this QC: **955** (entry added by concurrent docs commit, not by QC)
- `lists/03-gnss-data.md` surgically synced (rinex2bin under RINEX转换; header 132→133); README provenance badges synced (**298 / 336 / 321**)

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `rewrite_zh` | rinex2bin | one_liner_zh, desc_zh, analysis_zh |
| 2 | `meta` | provenance_counts | personal_community 320→321 |
| 3 | `lists` | 03-gnss-data | add rinex2bin table+detail; header 133 |
| 4 | `readme` | counts | 955; 社区 321 |

Chinese rewrite names: rinex2bin

Full machine log: `research/_qc_touch_log_20260924_batch26.json` (gitignored scratch).
Keep audits: `research/_qc_batch26_prov_keep.json`.

## Counts after sync
- `project_count`: **955**
- `counts_by_category`: unchanged by QC (gnss-data=133 includes rinex2bin)
- `provenance_counts`: `{"official": 298, "academic_lab": 336, "personal_community": 321}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **138**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 27)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals/weak blurbs. Remaining ~138 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language (20 empties re-sampled this batch: none).
3. **6 HTTP URLs** — HTTPS still unreachable (incl. variants); leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans scarce after org/sibling sweeps on i–p; new flips need fresh gh company=Univ/Lab or new routine owners. Vendor/FOSS orgs intentionally kept PC under current policy.
6. Guard against routine-merge / concurrent-docs races — rebase-before-push; never strip fresh routine entries or unrelated WIP when resolving races. Watch `provenance_counts` when docs commits link new catalog rows.
