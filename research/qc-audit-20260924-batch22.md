# Catalog QC audit — 2026-09-24 batch 22

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after routine-2026-09-24m (`96dd91c`): **912** entries; `desc_zh`==`one_liner_zh` **121** (batch21 left 107 @898; +14 routine-m identicals)
- Goal: QC only (no new projects) — polish new routine-m **software** identicals; provenance spot-audit personal_community with Lab/Univ/Agency gh evidence; HTTPS re-probe; rare SPDX only if gh real; **no** forced OL≠DZ on pure data-portal walls; no core/featured bulk flip
- Dedicated catalog-only commit
- **Race policy:** preserve freshly ingested routine-2026-09-24m entries; do not strip concurrent new projects; `git pull --rebase origin main` before push; never force-push

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **121** before → **115** after |
| Empty `license` | unchanged (gh probes null/NOASSERTION — no invent) |
| Empty `language` | unchanged (~30; gh null or weak PostScript/Roff/HTML/Starlark/GF — skipped) |
| HTTP leftovers | **6** (HTTPS still unreachable) |
| `project_count` | **912** (unchanged by QC) |

### Prior QC integrity (after pull through routine-m)
Sample Chinese QC intact (OL≠DZ): NeoGPS, SoftGNSS-octave, geoveil-mp, lowtran, pysatNASA. Batch21 provenance flips intact. Routine-2026-09-24m (+14) present and preserved (6 software polished; 8 portals left identical intentionally).

### HTTPS probe (curl -sI -L --max-time 12)
Matching HTTPS still fail (http_code=000) while HTTP originals return 200. Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

### SPDX / language
Probed empty-license GitHub hosts via `gh api repos/... --jq .license.spdx_id` — **null** or **NOASSERTION**. No SPDX fills. Empty-language repos returned null or weak languages; skipped.

### Provenance deep spot-audit
Batch-probed all **234** personal_community GitHub owners for company/bio Lab/Univ/Agency signals. Flip only with clear gh evidence:

| Name | Action | Evidence |
|---|---|---|
| grinq | personal_community→**academic_lab** | PJarrin company=Géoazur, IRD; bio Postdoctoral Researcher … GNSS & Geodesy |
| ionex_reader | personal_community→**academic_lab** | bbrawar company=Indian Institute of Technology Indore |
| max2771_fx2lp | personal_community→**academic_lab** | jmfriedt company=FEMTO-ST; bio Associate professor Franche-Comte University / FEMTO-ST (overrides batch20 keep) |
| SAMI3-3.22-CCMC-mirror | personal_community→**academic_lab** | sylee918 company=@NASA/GSFC @CUA; bio Postdoc NASA/GSFC & CUA; sibling SAMI3-3.22-Zenodo already academic_lab |
| ErickShepherd/cosmic-crunch | KEEP personal_community | NASA GSFC **alum** only — not current affiliation |
| ajayraghASL/Ionex_Parser | KEEP personal_community | Augsense Lab commercial (batch17) |
| oscimp/gnss-sdr-1pps | KEEP personal_community | OscillatorIMP PIA community (batch11/12) |
| aldebaran1/gsit | KEEP personal_community | research bio only; company null — weak |
| perrysou/SoftGNSS-python | KEEP personal_community | company field is IIT spaceweather URL only |
| Gm015555/quakeion | KEEP personal_community | commercial company; MS IST alum |
| timduly4/pyglow | KEEP personal_community | Spire Global commercial |
| nav-solutions/* | KEEP personal_community | community org France (prior) |
| Erensu/ignav | KEEP personal_community | loc=WHU only (batch6/7/21) |
| PyGnssLab / seafloor-geodesy / swri-robotics | KEEP personal_community | community / vendor-adjacent (batch20/21) |
| CS-SI/Orekit | KEEP personal_community | CS GROUP commercial OSS |
| SkydelSolutions/NeQuick2-MLF2 | KEEP personal_community | Safran Trusted 4D vendor OSS |
| inigodelportillo/ITU-Rpy | KEEP personal_community | SES Satellites commercial |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **4** → academic_lab; **15** spot-audits kept
- Chinese rewrites: **6** entries (`desc_zh` ≠ `one_liner_zh`) — routine-2026-09-24m GitHub software only
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **10** (4 provenance + 6 Chinese; no overlap)
- `project_count` unchanged by this QC: **912**
- `lists/*.md` surgically synced (01, 03, 06, 07, 08, 09); README provenance badges synced (274 / 327 / 311)

### Chinese polish strategy
- **Primary:** 6 new routine-2026-09-24m **software** identicals (ROS/Arduino/GPSDO/Rust-UBX)
- **Skipped on purpose:** 8 new portal walls (SIDC, SILSO, Kyoto-Dst/Kp, SWPC-GOES-Xray, SWPC-Solar-Cycle, SWS-Solar, GFZ-Kp-Data) + remaining ~107 older portal identicals

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | grinq | personal_community→academic_lab |
| 2 | `provenance` | ionex_reader | personal_community→academic_lab |
| 3 | `provenance` | max2771_fx2lp | personal_community→academic_lab |
| 4 | `provenance` | SAMI3-3.22-CCMC-mirror | personal_community→academic_lab |
| 5 | `rewrite_zh` | ublox-ros | one_liner_zh, desc_zh |
| 6 | `rewrite_zh` | nmea_navsat_driver | one_liner_zh, desc_zh |
| 7 | `rewrite_zh` | MicroNMEA | one_liner_zh, desc_zh |
| 8 | `rewrite_zh` | 107-Arduino-NMEA-Parser | one_liner_zh, desc_zh |
| 9 | `rewrite_zh` | gpsdo | one_liner_zh, desc_zh |
| 10 | `rewrite_zh` | ublox-rs | one_liner_zh, desc_zh |

Chinese rewrite names: 107-Arduino-NMEA-Parser, MicroNMEA, gpsdo, nmea_navsat_driver, ublox-ros, ublox-rs

Full machine log: `research/_qc_touch_log_20260924_batch22.json` (gitignored scratch).
Keep audits: `research/_qc_batch22_prov_keep.json`.

## Counts after sync
- `project_count`: **912**
- `counts_by_category`: unchanged by QC (see PROJECTS.json)
- `provenance_counts`: `{"official": 274, "academic_lab": 327, "personal_community": 311}`
- `updated`: **2026-09-24**
- Remaining empty license/language: unchanged (no invent)
- Remaining HTTP: 6
- `desc_zh` == `one_liner_zh`: **115**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 23)
1. **Chinese polish for software still scarce** unless a new routine brings code-host identicals. Remaining ~115 identicals are almost all official_site / data-portal walls — skip OL≠DZ boilerplate.
2. Empty licenses/languages — fill only when `gh` returns real SPDX / non-weak language.
3. **6 HTTP URLs** — HTTPS still unreachable; leave HTTP until servers support TLS.
4. **`core` vs `featured` drift** — decide policy before bulk flip.
5. Further personal_community Lab/Univ orphans are scarce after owner-wide company/bio sweep; new flips need fresh gh evidence or new routine owners.
6. Guard against routine-merge overwrites — rebase-before-push; never strip fresh routine entries when resolving races.
