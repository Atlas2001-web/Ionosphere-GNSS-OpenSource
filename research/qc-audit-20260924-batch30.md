# Catalog QC audit — 2026-09-24 batch 30

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch29 (`05c95eb`) + concurrent catalog/docs (`92138c0` routine-r → **983**; `3875eec`/`414a037` gnss-rtk): **983** catalog entries
- Goal: Phase A catalog QC on routine-r (+ weak code-host); if zero → Phase B short-hard manuals for remaining download/portal clients
- **Race policy:** leave concurrent untracked alone (`matrtklib.md`, `urban-rtklib.md`; `gnss-rtk.md` already committed by peer); do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push; **NO inventing catalog projects**

## Path taken
**Phase A = 0** high-confidence catalog field changes → **Phase B** short-hard manuals (`earthscope-sdk` + `GNSS_OSI_download` → `gnss-osi-download.md`).

## Phase A — pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields (code-host) | **0** |
| `desc_zh` == `one_liner_zh` code-host | **0** |
| routine-r portals OL==DZ | **14** — all `official_site` (CZEPOS…ESA-OPS-GN) — **skip portal walls** |
| Empty `license` (code-host sample) | gh still `null` / `NOASSERTION` on empty catalog slots — **0** fills (cssrlib/IonKit-NH/IRTS_SDK/vtec/awesome-gnss-barbeau already had real SPDX) |
| Empty `language` (code-host sample) | null or weak (Jupyter/HTML/PostScript/…) only — **0** fills |
| HTTP leftovers | **6** — HTTPS probe all `http_code=000` / connect fail — leave HTTP |
| Provenance | routine-r all `official` (appropriate for agency portals); no high-confidence flip |

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still unreachable: CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language sample (`gh api`)
Mereithhh/gnss-downloader, ohm1122/ionex-downloader, LECUT/GDDS, valgur/hatanaka, nlsfi/HASlibTestSuite, SGL-UT/gnsstk{,-apps}, zp-9696/BDS-3-PPP-B2b-DATA, AgOpenGPS-Official/AgOpenNtripCaster, Jin-Whu/DRCycleSlip, GCCLib/B2bLIB, baidu/ntripcaster, LORD-MicroStrain/ntrip_client → null/NOASSERTION/weak lang only. Confirmed already-filled: cssrlib MIT, IonKit-NH GPL-3.0, IRTS_SDK GPL-3.0, vtec MIT, awesome-gnss-barbeau Apache-2.0. **No invent.**

## Phase B — manuals

| Manual | Upstream | Real I/O |
|---|---|---|
| `docs/software/earthscope-sdk.md` | gitlab earthscope/public/earthscope-sdk · PyPI **1.9.2** · tip **`4ba8870`** · ★**4** · CLI **1.2.0** | `es --version`; `es user get-profile` → *No tokens…*; `EarthScopeClient` OK; `get_profile`/`plan()`/`fetch()` → **NoRefreshTokenError**; bare `client.data` needs **`[arrow]`**; QueryPlan lazy `unplanned`; **no token → no Arrow rows** |
| `docs/software/gnss-osi-download.md` | jdesbonnet/GNSS_OSI_download · tip **`0aeb83a`** · ★**1** · MIT · no PyPI | `-h` full flags; `--list-stations` / download → **ConnectionError** `NameResolutionError: gnss.osi.ie`; curl HTTPS `000`; **no ZIP** |

Candidates preferred: earthscope-sdk, GNSS_OSI_download, swds-api-downloader. Chose **earthscope-sdk** + **GNSS_OSI_download** (honest E2E without inventing data). **swds-api-downloader** deferred: empty creds + host `urlopen` fails from this network (`SwdsError: host is not a valid URL`).

Avoid-list respected (no SDR / reflectometry / RTKLIB family / GREAT / Gkit / bias / time-transfer / binary conversion). Peer `gnss-rtk` left alone (already on main).

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance flips: **0**
- Chinese rewrites: **0**
- HTTPS upgrades: **0**
- Catalog field changes: **0** → no `fix(catalog)` commit
- Manuals added: **2**
- `project_count` unchanged: **983**
- Concurrent WIP preserved (untracked left alone): `docs/software/matrtklib.md`, `docs/software/urban-rtklib.md`

## Counts after
- `project_count`: **983**
- Catalog commit: **no**
- Docs commit: **yes** (`docs(software): short-hard manual for earthscope-sdk + gnss-osi-download`)

## Top remaining issues (batch 31)
1. Portal OL==DZ walls (~165) — skip unless policy changes
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language
3. **6 HTTP URLs** — leave until TLS works
4. Manual fallback leftover: `swds-api-downloader` (INPE SWDS credentials + host reachability)
5. Guard races — rebase-before-push; never strip concurrent docs WIP (`matrtklib` / `urban-rtklib`)
