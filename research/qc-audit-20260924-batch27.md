# Catalog QC audit — 2026-09-24 batch 27

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after QC batch26 (`c11a28c`): **955** entries; `desc_zh`==`one_liner_zh` **138** (all `official_site` portal walls)
- Goal: QC only (no new projects) — prefer newer ingestion rounds **i–p** / batch15–17 era; Chinese polish on code-host; high-confidence provenance only; HTTPS re-probe 6 leftovers; rare SPDX/language only if `gh` real; **no** portal OL≠DZ walls; no core/featured bulk flip
- Dedicated catalog-only commit **only if** high-confidence field changes
- **Race policy:** preserve concurrent docs/WIP and fresh routine entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push
- Concurrent unstaged WIP left alone: `docs/software/cggtts.md`

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **138** (0 code-host; all `official_site`) |
| Empty `license` | 169 total / **156** GitHub — sample+trunc-fix re-probe null/NOASSERTION |
| Empty `language` | **34** / **30** GitHub — null or weak/quirky only |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| Newer rounds i–p GitHub software | **53**; Chinese already OL≠DZ; lic/lang filled |
| Meta drift | **none** — `project_count` 955; provenance 298/336/321; category counts match lists headers |
| `project_count` | **955** |

### Prior QC integrity
Sample Chinese QC intact (rinex2bin, SoftGNSS-octave, pymsis, SoapySDR, NeoGPS, nmea_navsat_driver official). Routine-p fourteen names present. Batch25–26 KEEP provenance sets not re-opened for flip.

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS + host/path variants still fail (`http_code=000` / connect error). HTTP originals return **200**. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
- Newer i–p GitHub software: **0** empty license/language
- Probed **89** empty-license GitHub hosts via `gh api … --jq .license.spdx_id` (+ 5 truncated-name corrections: UrbanNavDataset, Navigation-Learning, gps_pvt, gps-sdr-sim-assistant, scintkit) — **null** or **NOASSERTION** only (**0** fills)
- Empty-language GitHub (**30**): mostly `null`; weak/quirky rejected (PostScript / Roff / HTML / OpenEdge ABL / Starlark); GAMP_PPPH primary=`Grammatical Framework` (bytes dominated by non-source; C/MATLAB present but policy = no invent) — **0** strong-language fills
- SoftGNSS-octave: gh language remains Objective-C — leave

### Provenance deep spot-audit (newer PC GitHub + mixed orgs; stricter)
Flip threshold: clear Lab/Univ/Agency org **or** sibling consistency under an org already **official**/**academic_lab**. Fresh `gh api users/{owner}` only. Do **not** re-litigate batch25–26 KEEP sets without new evidence.

| Owner / name | Action | Evidence |
|---|---|---|
| nav-solutions (incl. cggtts / rinex2bin siblings) | KEEP personal_community | Org bio GNSS FOSS (France); all catalog siblings PC |
| pothosware (Soapy* suite) | KEEP personal_community | Pothosware FOSS suite; no univ/lab |
| osqzss | KEEP personal_community | User Takuji Ebinuma; personal |
| swift-nav / novatel / Fixposition / Aceinna / bolderflight | KEEP personal_community | Commercial vendor orgs (policy) |
| swri-robotics | KEEP personal_community | batch25 KEEP; not re-opened |
| 107-systems / ublox-rs | KEEP personal_community | Community FOSS orgs |
| csobey, vincenthumphrey, DeepHorizons, Binabh, kristianpaul, stevemarple, AlvaroTena, nbtk, … | KEEP personal_community | Users; company/bio null or non-lab |
| PrideLab / i2Nav-WHU / SGL-UT | already academic_lab | Confirmed WHU / ARL:UT lab orgs — no flip needed |
| nlsfi | already official | National Land Survey of Finland — confirmed |
| **Erensu** (carvig=AL, ignav=PC) | KEEP mixed | User; company=null; loc=WHU only — insufficient for ignav flip (batch25+) |
| **pjalesSSTL** (Python=AL, GNSSRMERRByS=PC) | KEEP mixed | company=Surrey Satellite Technology Ltd. vendor — PC keep under vendor policy |
| **Sibling mixed-provenance among newer PC orgs** | **none** | All newer PC orgs internally consistent |

**Flips this batch: 0** (no new Lab/Univ/Agency evidence among candidates)

### Chinese polish strategy
- **Skipped on purpose:** all **138** remaining identicals are portal / `official_site` walls
- Newer i–p GitHub software (**53**): already OL≠DZ at ingest / prior QC — left intact
- Concurrent docs WIP on **cggtts**: catalog Chinese already differentiated; **no** invent polish; leave `docs/software/cggtts.md` unstaged

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance flips: **0**; **28** newer-PC-org spot-audits kept; 2 mixed-org KEEP; 4 Lab/Agency owners confirmed already correct
- Chinese rewrites: **0** (no code-host identicals; portal walls skipped)
- Meta sync: **none needed** (already matched)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **0**
- `project_count` unchanged: **955**
- Catalog commit: **none** (zero high-confidence field changes — no empty commit)
- Concurrent WIP preserved: `docs/software/cggtts.md`

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| — | *(none)* | — | zero high-confidence catalog field changes |

Chinese rewrite names: *(none)*

Keep notes: this audit file only.

## Counts after scan (unchanged)
- `project_count`: **955**
- `counts_by_category`: gnss-data=133, gnss-datasets=140, gnss-positioning=101, gnss-sdr=76, ionosphere=278, mobile-apps=29, navigation-ins=71, orbit-clock=27, tools-learning=59, troposphere=41
- `provenance_counts`: `{"official": 298, "academic_lab": 336, "personal_community": 321}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **138**
- `core` / `featured` policy: unchanged (no bulk flip)
- lists/01–10 headers and README badges (**955**; 官方 298 · 高校 336 · 社区 321) already match

## Top remaining issues (batch 28)
1. **Chinese polish for software scarce** unless a new routine brings code-host identicals/weak blurbs. Remaining ~138 identicals are almost all `official_site` / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language (89+30 probed this batch: none).
3. **6 HTTP URLs** — HTTPS still unreachable (incl. variants); leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans scarce after org/sibling sweeps on i–p; new flips need fresh gh company=Univ/Lab or new routine owners. Vendor/FOSS orgs intentionally kept PC. Mixed Erensu / pjalesSSTL left intentional.
6. Guard against routine-merge / concurrent-docs races — rebase-before-push; never strip fresh routine entries or unrelated WIP (`docs/software/cggtts.md` in flight). Watch `provenance_counts` when docs commits link new catalog rows.
