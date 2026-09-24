# Catalog QC audit — 2026-09-24 batch 10

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch9 `ed6763d` (+ local docs `8f9ff22`): **788** entries; `desc_zh`==`one_liner_zh` **437**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / featured / core software); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **437** before → **402** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000` / FAIL). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, PPP-Wizard, eSWua-TEC, IONORING, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch9 integrity
Sample Chinese QC (KF-GINS / PRIDE-PPPAR / georinex / HASlib / MADOCALIB / TEQC / pyglow / PPP-Wizard OL≠DZ) intact. Prior provenance upgrades (carvig / B2bLIB / PyTECGg → academic_lab) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| HASPPP | personal_community→academic_lab; ZhangRunzhi20 company UCAS; PhD NTSC of CAS |
| PPP_AR | personal_community→academic_lab; heiwa0519 company CUMT; student bio GNSS |
| OSNMA | personal_community→academic_lab; Algafix company KU Leuven |
| MAPS | personal_community→academic_lab; GCCLib PI Zhetao Zhang / 同济大学（同 B2bLIB） |
| ntrip_client-MicroStrain | KEEP — LORD-MicroStrain commercial → personal_community |
| SatellitePosition | KEEP — LStudioLoren / BDStar commercial |
| SoftGNSS-python | KEEP — perrysou company field is IIT spaceweather URL only |
| GNSS_IMU | KEEP — rtklibexplorer / RTK Consultants LLC |
| ntrip-go | KEEP — go-gnss community org |
| KalmanFilters.jl | KEEP — JuliaGNSS community org |
| pyRTKLib-RINEX | KEEP — alainmuls / SatNavam CommV |
| satpulse / gps-sdr-sim-assistant / galileo-sdr-sim / IonoMoni / tisyang pair / gnss-baseband / GGOS-Tropo-RTKLIB / ESP32-SDR-GPS / PyGPS | KEEP — empty or personal bios |
| Kamodo / Wheel-GINS / NavLab-DPE-SDR / geospacelab / apexpy / GVINS-Dataset / gps / PPPLib / RTKLIB-Manual-CN / MobileGNSS-SPP | already official or academic_lab |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **4** → academic_lab; **27** spot-audits kept/confirmed
- Chinese rewrites: **35** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **35** (4 also provenance)
- `project_count` unchanged: **788**
- `lists/*.md` surgically synced (01–09); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | HASPPP | provenance; personal_community→academic_lab; ZhangRunzhi20 company UCAS; PhD NTSC of CAS |
| 2 | `provenance` | PPP_AR | provenance; personal_community→academic_lab; heiwa0519 company China University of Mining and Technology; student bio GNSS |
| 3 | `provenance` | OSNMA | provenance; personal_community→academic_lab; Algafix company KU Leuven |
| 4 | `provenance` | MAPS | provenance; personal_community→academic_lab; GCCLib PI Zhetao Zhang / 同济大学（同 B2bLIB 批次证据） |
| 5 | `rewrite_zh` | GVINS-Dataset | one_liner_zh, desc_zh; short human Chinese QC |
| 6 | `rewrite_zh` | ntrip_client-MicroStrain | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | gps | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | IRI-2026-package | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | IRI-COMMON-FILES | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | IRI-MATLAB-FileExchange | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | NeQuick2-ICTP | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | ntripcaster-libev | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | gps-sdr-sim-assistant | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | satpulse | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | SatellitePosition | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | galileo-sdr-sim | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | ntrip-go | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | Kamodo | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | ESP32-SDR-GPS | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | KalmanFilters.jl | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | RTKLIB-Manual-CN | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | OSNMA | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | pyRTKLib-RINEX | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | PPPLib | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | cors-relay | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | geospacelab | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | PyGPS | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | Wheel-GINS | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | NavLab-DPE-SDR | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | HASPPP | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | SoftGNSS-python | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | GGOS-Tropo-RTKLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | gnss-baseband | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | MobileGNSS-SPP | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | PPP_AR | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | apexpy | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | IonoMoni | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | GNSS_IMU | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | MAPS | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: ESP32-SDR-GPS, GGOS-Tropo-RTKLIB, GNSS_IMU, GVINS-Dataset, HASPPP, IRI-2026-package, IRI-COMMON-FILES, IRI-MATLAB-FileExchange, IonoMoni, KalmanFilters.jl, Kamodo, MAPS, MobileGNSS-SPP, NavLab-DPE-SDR, NeQuick2-ICTP, OSNMA, PPPLib, PPP_AR, PyGPS, RTKLIB-Manual-CN, SatellitePosition, SoftGNSS-python, Wheel-GINS, apexpy, cors-relay, galileo-sdr-sim, geospacelab, gnss-baseband, gps, gps-sdr-sim-assistant, ntrip-go, ntrip_client-MicroStrain, ntripcaster-libev, pyRTKLib-RINEX, satpulse

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch10.json`.
Keep audits: `research/_qc_batch10_prov_keep.json`.

## Counts after sync
- `project_count`: **788**
- `counts_by_category`: `{"gnss-data": 117, "gnss-datasets": 122, "gnss-positioning": 88, "gnss-sdr": 59, "ionosphere": 240, "mobile-apps": 20, "navigation-ins": 60, "orbit-clock": 13, "tools-learning": 34, "troposphere": 35}`
- `provenance_counts`: `{"official": 226, "academic_lab": 268, "personal_community": 294}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **402**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 11)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈402) — continue short human polish on remaining high-star software (avoid portal walls). Suggested leftovers: cssrlib-data, SoftGNSS-python siblings already done — next: pygnsslab / BeiDou_B1C / GNSS-VHDL / HTDP / TEC-calculation-MATLAB / geodezyx / polaris / awesome-gnss-hdkarimi (lists only if useful) / remaining NTRIP family / more ionosphere tools (IonoMoni done) / GPSBabel / Seemala-GPS-TEC software-facing only.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear.
