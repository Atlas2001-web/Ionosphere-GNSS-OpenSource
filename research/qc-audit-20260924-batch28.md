# Catalog QC audit — 2026-09-24 batch 28

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch27 audit + concurrent docs/`routine-q`: **969** entries (`681b890` +14 portals/nyx)
- Goal: QC only (no new projects) — newer rounds **i–q**; Chinese polish on code-host; high-confidence provenance only; HTTPS re-probe 6 leftovers; rare SPDX/language only if `gh` real; **no** portal OL≠DZ walls; no core/featured bulk
- Dedicated catalog commit **only if** high-confidence field changes
- **Race policy:** preserve concurrent docs WIP (`docs/software/gnssrefl.md`, `mpsim.md`, `great-podflt.md` QC edits); do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Path taken
Catalog field change found (**nyx** Chinese) → finish catalog QC; **skip** short-hard manual fallback lane this batch.

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **152** → after polish **151** (0 code-host; all `official_site` portals + was 1 github `nyx`) |
| Empty `license` | 169 total / GitHub still null/NOASSERTION on sample (ginan/gnsstk/…); **q** github `nyx` already AGPL-3.0 |
| Empty `language` | **34** / GitHub weak-or-null; **q** `nyx` already Rust |
| HTTP leftovers | **6** (HTTPS still unreachable: `http_code=000`) |
| Newer i–p GitHub software | already OL≠DZ / lic/lang filled (batch27) |
| Newer **q** | 14 entries: 13 `official_site` portal identicals (skip) + **1** github `nyx` OL==DZ (**fixed**) |
| Meta drift | **none** — `project_count` 969; provenance 310/337/322; lists/README badges already synced by routine-q |
| `project_count` | **969** |

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS + host/path variants still fail (`http_code=000` / connect error). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
- Sample re-probe: GeoscienceAustralia/ginan, SGL-UT/{gnsstk,gnsstk-apps,GPSTk}, Mereithhh/gnss-downloader, ohm1122/ionex-downloader, LECUT/GDDS, valgur/hatanaka, nlsfi/HASlibTestSuite → **null** / **NOASSERTION** / weak PostScript only — **0** fills
- `nyx`: already **AGPL-3.0** / **Rust** (gh confirmed) — no invent

### Provenance
| Owner / name | Action | Evidence |
|---|---|---|
| **nyx-space** / nyx | KEEP personal_community | Org bio FOSS astrodynamics; company=null; not Lab/Univ/Agency |
| nav-solutions / pothosware / Erensu / pjalesSSTL | KEEP | batch25–27; not re-opened without new evidence |

**Flips this batch: 0**

### Chinese polish
| Name | Change |
|---|---|
| **nyx** | `desc_zh` differentiated from `one_liner_zh` (was identical ingest blurb) |

Portal walls among q (ReNEP, GNSSNet-Hungary, CSN-Chile-GPS, SIRGAS, EUREF×2, VMF1/3, NOAA-EMM, PSMSL, SWPC×2, IVS-IVSOPAR): **skipped** on purpose.

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance flips: **0**
- Chinese rewrites: **1** (`nyx`)
- Meta sync: **none needed** (routine-q already matched)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **1**
- `project_count` unchanged: **969**
- Catalog commit: **yes** (real field change)
- Concurrent WIP preserved (unstaged / untracked left alone): `docs/software/gnssrefl.md`, `mpsim.md`, README/great-podflt WIP from parallel agent

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | Chinese polish | nyx | `desc_zh` ← orbit/OD/mission-analysis boundary blurb; `one_liner_zh` kept |

Chinese rewrite names: `nyx`

## Counts after
- `project_count`: **969**
- `counts_by_category`: ionosphere=281, troposphere=44, gnss-data=133, gnss-positioning=101, orbit-clock=29, navigation-ins=71, gnss-sdr=76, mobile-apps=29, tools-learning=59, gnss-datasets=146
- `provenance_counts`: `{"official": 310, "academic_lab": 337, "personal_community": 322}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **151** (all `official_site`)
- `core` / `featured` policy: unchanged

## Top remaining issues (batch 29)
1. Portal OL==DZ walls (~151) — skip boilerplate unless policy changes.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language.
3. **6 HTTP URLs** — HTTPS still unreachable; leave until TLS works.
4. Manual fallback lane candidates still missing docs: `earthscope-sdk`, `viresclient`, `GNSS_OSI_download` (osi DNS fail here), `Ionosonde-Data-Downloader`, `swds-api-downloader`.
5. Guard races — rebase-before-push; never strip routine-q+ or parallel docs WIP.
