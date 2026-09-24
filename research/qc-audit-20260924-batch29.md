# Catalog QC audit — 2026-09-24 batch 29

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch28 (`d31cd1c` nyx) + concurrent docs (sp3 / rt-clk-service / gnssanalysis / …): **969** catalog entries
- Goal: Phase A catalog QC on round-18 / routine-q (Chinese / SPDX / HTTPS / provenance); if zero → Phase B short-hard manuals for data-download / portal-client tools lacking docs
- **Race policy:** preserve concurrent docs WIP (`radiate.md`, `rtklib-py.md`, merge_routine_r); do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Path taken
**Phase A = 0** high-confidence catalog field changes → **Phase B** short-hard manuals (`viresclient` + `Ionosonde-Data-Downloader`).

## Phase A — pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields (newer github i–q) | **0** |
| `desc_zh` == `one_liner_zh` code-host | **0** (only `official_site` portals remain ≈151; skipped) |
| routine-q portals OL==DZ | **13** — skip portal walls |
| routine-q github `nyx` | already OL≠DZ / AGPL-3.0 / Rust (batch28) |
| Empty `license` (code-host sample) | gh still `null` / `NOASSERTION` — **0** fills |
| Empty `language` (code-host sample) | only weak/meta (Starlark/HTML/Roff/PostScript) or null — **0** fills |
| HTTP leftovers | **6** — HTTPS probe all `http_code=000` / connect fail — leave HTTP |
| Provenance | no new high-confidence flip evidence |

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still unreachable: CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language sample (`gh api`)
Mereithhh/gnss-downloader, ohm1122/ionex-downloader, LECUT/GDDS, valgur/hatanaka, nlsfi/HASlibTestSuite, GeoscienceAustralia/ginan, SGL-UT/gnsstk{,-apps}, zp-9696/BDS-3-PPP-B2b-DATA, PointOneNav/polaris → null/NOASSERTION/weak lang only. **No invent.**

## Phase B — manuals

| Manual | Upstream | Real I/O |
|---|---|---|
| `docs/software/viresclient.md` | ESA-VirES/VirES-Python-Client · PyPI **0.16.0** · tip **`c00f81d`** · ★**23** | `--help`; no ini error; no-token `AuthenticationError`/WPS **403**; `available_measurements("TEC")`; fake measurement name exception; **no real token → no xarray** |
| `docs/software/ionosonde-data-downloader.md` | bzossi/Ionosonde-Data-Downloader · tip **`ea80896`** · ★**2** · no PyPI | Aus Townsville **2010** shape **(8760,5)** fof2 **5.3**; Japan Kokubunji **2020** auto **(35136,4)** fof2 **2.86**; needs **lxml**; OMNI2 `delim_whitespace` TypeError on pandas 2.x |

Candidates verified in `PROJECTS.json` with no prior manual: earthscope-sdk, viresclient, GNSS_OSI_download, Ionosonde-Data-Downloader, swds-api-downloader. Chose **viresclient** + **Ionosonde-Data-Downloader** (runnable without paid API; OSI DNS / SWDS / EarthScope token deferred).

Avoid-list respected (no SDR / reflectometry / RTKLIB family / GREAT / Gkit / bias / time-transfer / binary conversion).

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance flips: **0**
- Chinese rewrites: **0**
- HTTPS upgrades: **0**
- Catalog field changes: **0** → no `fix(catalog)` commit
- Manuals added: **2**
- `project_count` unchanged: **969**
- Concurrent WIP preserved (stashed then restore after push): `radiate.md`, `rtklib-py.md`, `research/merge_routine_20260924r.py`

## Counts after
- `project_count`: **969**
- Catalog commit: **no**
- Docs commit: **yes** (`docs(software): short-hard manual for viresclient + ionosonde-data-downloader`)

## Top remaining issues (batch 30)
1. Portal OL==DZ walls (~151) — skip unless policy changes
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language
3. **6 HTTP URLs** — leave until TLS works
4. Manual fallback leftovers: `earthscope-sdk`, `GNSS_OSI_download`, `swds-api-downloader` (token/DNS/API gates)
5. Guard races — rebase-before-push; never strip concurrent docs WIP
