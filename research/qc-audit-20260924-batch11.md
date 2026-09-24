# Catalog QC audit — 2026-09-24 batch 11

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch10 `3ca7107` (+ routine `22f81ef` +14 and intervening docs): **802** entries; `desc_zh`==`one_liner_zh` **402**
- Goal: QC only (no new projects) — Chinese polish primary (high-star / software-facing); provenance verify-only; HTTPS probe; no SPDX/language invent; no core/featured bulk flip
- Dedicated catalog-only commit

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty Chinese fields | **0** |
| `desc_zh` == `one_liner_zh` | **402** before → **367** after |
| Empty `license` | **169** |
| Empty `language` | **34** |
| HTTP leftovers | **6** |

### HTTPS probe (curl -sI -L --max-time 15)
All six HTTPS upgrades still **fail** (`http_code=000` / FAIL). Leave HTTP:
CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN.

### SPDX / language
No new high-confidence SPDX or language fills (null/NOASSERTION / data-portal primaries left untouched).

### Batch10 integrity
Sample Chinese QC (HASPPP / PPP_AR / OSNMA / MAPS / ntrip-go / cssrlib / PocketSDR OL≠DZ) intact. Prior provenance upgrades (HASPPP / PPP_AR / OSNMA / MAPS → academic_lab) still present.

### Provenance spot-checks (gh api `users/{owner}` + public affiliation)
| Name | Detail |
|---|---|
| BeiDou_B1C | personal_community→academic_lab; lnexenl company HKUST; bio Ph.D student at HKUST |
| GPSL1-DPEmodule | personal_community→academic_lab; Sergio-Vicenzo company The Hong Kong Polytechnic University; bio PhD student PolyU |
| gnss2tws-green | personal_community→academic_lab; jzshhh company Sun Yat-Sen University |
| ImuGpsGuiding | personal_community→academic_lab; JackJu-HIT company HIT; bio 哈尔滨工业大学控制科学与工程硕士 |
| GNSS-Explorer | personal_community→academic_lab; brucezhcw company HKUST |
| pygnsslab | KEEP — org bio open-source software lab; no university/agency → keep personal_community |
| polaris | KEEP — Point One Navigation commercial org → keep personal_community |
| rtcm-rs | KEEP — empty bio/company → keep |
| hatanaka | KEEP — empty bio/company → keep |
| beidou-sdr-sim | KEEP — empty bio/company → keep |
| gnss-RX | KEEP — empty bio/company → keep |
| ALBUS_ionosphere | KEEP — personal radio astronomer; no university/agency field → keep |
| PPP-RTK-Beechan | KEEP — company Sichuan Jiuzhou Electric Group commercial → keep personal_community |
| M_GIM-zcytju | KEEP — empty bio/company → keep |
| FlyDog-SDR-GPS | KEEP — community hardware org → keep personal_community |
| GPSGALSSS | KEEP — personal blog; no university → keep |
| gnss-signal-simulator-rs | KEEP — personal; company home → keep |
| msckfvioGPS | KEEP — empty bio/company → keep |
| STM32Primer2-GNSS-Tracker | KEEP — personal hobbyist → keep |
| tec_forecast | KEEP — PhD in bio but no company/org affiliation field → keep |
| awesome-gnss-hdkarimi | KEEP — personal FOSS curator → keep |
| ntrip-client | KEEP — community org France; no agency/university → keep |
| ntrip-catalog | KEEP — Pix4D commercial → keep personal_community |
| ntrip-caster-go | KEEP — empty bio/company → keep |
| GNSSRMERRByS | KEEP — Surrey Satellite Technology Ltd commercial → keep |
| gnss-sdr-1pps | KEEP — OscillatorIMP PIA community org; affiliation not a clear university/agency catalog class → keep |
| gnssgo | KEEP — company Explore Data Technology Ltd commercial → keep |
| PW_from_GPS | KEEP — industry researcher; no university company → keep |
| pylgrim | KEEP — company secjur commercial → keep |
| BUAA-RINEX-Convertor | KEEP — empty bio/company (BUAA only in project name) → keep |
| GHASP-HAS-decoding | KEEP — empty bio/company despite known researcher name → keep until org field clear |
| GPSBabel | KEEP — long-running community software; not university/agency → keep personal_community |

## This batch — summary
- License fills: **0**
- Language fills: **0**
- Provenance fixes: **5** → academic_lab; **27** spot-audits kept/confirmed
- Chinese rewrites: **35** entries (`desc_zh` ≠ `one_liner_zh`)
- Marker / featured flips: **0**
- HTTPS upgrades: **0**
- Entries touched (unique names): **35** (5 also provenance)
- `project_count` unchanged by this QC: **802**
- `lists/*.md` surgically synced (01-ionosphere.md, 02-troposphere.md, 03-gnss-data.md, 04-gnss-positioning.md, 05-orbit-clock.md, 06-navigation-ins.md, 07-gnss-sdr.md, 09-tools-learning.md, 10-gnss-datasets.md); `sync_readme_counts.py` preserve-mode

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `provenance` | BeiDou_B1C | provenance; personal_community→academic_lab; lnexenl company HKUST; bio Ph.D student at HKUST |
| 2 | `provenance` | GPSL1-DPEmodule | provenance; personal_community→academic_lab; Sergio-Vicenzo company The Hong Kong Polytechnic University; bio PhD student PolyU |
| 3 | `provenance` | gnss2tws-green | provenance; personal_community→academic_lab; jzshhh company Sun Yat-Sen University |
| 4 | `provenance` | ImuGpsGuiding | provenance; personal_community→academic_lab; JackJu-HIT company HIT; bio 哈尔滨工业大学控制科学与工程硕士 |
| 5 | `provenance` | GNSS-Explorer | provenance; personal_community→academic_lab; brucezhcw company HKUST |
| 6 | `rewrite_zh` | pygnsslab | one_liner_zh, desc_zh; short human Chinese QC |
| 7 | `rewrite_zh` | BeiDou_B1C | one_liner_zh, desc_zh; short human Chinese QC |
| 8 | `rewrite_zh` | GNSS-VHDL | one_liner_zh, desc_zh; short human Chinese QC |
| 9 | `rewrite_zh` | HTDP | one_liner_zh, desc_zh; short human Chinese QC |
| 10 | `rewrite_zh` | TEC-calculation-MATLAB | one_liner_zh, desc_zh; short human Chinese QC |
| 11 | `rewrite_zh` | geodezyx | one_liner_zh, desc_zh; short human Chinese QC |
| 12 | `rewrite_zh` | polaris | one_liner_zh, desc_zh; short human Chinese QC |
| 13 | `rewrite_zh` | GPSBabel | one_liner_zh, desc_zh; short human Chinese QC |
| 14 | `rewrite_zh` | Seemala-GPS-TEC | one_liner_zh, desc_zh; short human Chinese QC |
| 15 | `rewrite_zh` | cssrlib-data | one_liner_zh, desc_zh; short human Chinese QC |
| 16 | `rewrite_zh` | rtcm-rs | one_liner_zh, desc_zh; short human Chinese QC |
| 17 | `rewrite_zh` | hatanaka | one_liner_zh, desc_zh; short human Chinese QC |
| 18 | `rewrite_zh` | Urban-RTKLIB | one_liner_zh, desc_zh; short human Chinese QC |
| 19 | `rewrite_zh` | GITM | one_liner_zh, desc_zh; short human Chinese QC |
| 20 | `rewrite_zh` | TIE-GCM | one_liner_zh, desc_zh; short human Chinese QC |
| 21 | `rewrite_zh` | gnssIR-matlab-v3 | one_liner_zh, desc_zh; short human Chinese QC |
| 22 | `rewrite_zh` | Cube | one_liner_zh, desc_zh; short human Chinese QC |
| 23 | `rewrite_zh` | beidou-sdr-sim | one_liner_zh, desc_zh; short human Chinese QC |
| 24 | `rewrite_zh` | viresclient | one_liner_zh, desc_zh; short human Chinese QC |
| 25 | `rewrite_zh` | tec-suite | one_liner_zh, desc_zh; short human Chinese QC |
| 26 | `rewrite_zh` | hardware | one_liner_zh, desc_zh; short human Chinese QC |
| 27 | `rewrite_zh` | gnss-RX | one_liner_zh, desc_zh; short human Chinese QC |
| 28 | `rewrite_zh` | GPSL1-DPEmodule | one_liner_zh, desc_zh; short human Chinese QC |
| 29 | `rewrite_zh` | gnss2tws-green | one_liner_zh, desc_zh; short human Chinese QC |
| 30 | `rewrite_zh` | ALBUS_ionosphere | one_liner_zh, desc_zh; short human Chinese QC |
| 31 | `rewrite_zh` | PPP-RTK-Beechan | one_liner_zh, desc_zh; short human Chinese QC |
| 32 | `rewrite_zh` | mphw | one_liner_zh, desc_zh; short human Chinese QC |
| 33 | `rewrite_zh` | gnss-scintillation-simulator | one_liner_zh, desc_zh; short human Chinese QC |
| 34 | `rewrite_zh` | LongwaveModePropagator.jl | one_liner_zh, desc_zh; short human Chinese QC |
| 35 | `rewrite_zh` | Aether-IT-model | one_liner_zh, desc_zh; short human Chinese QC |
| 36 | `rewrite_zh` | jvierine-ionosonde | one_liner_zh, desc_zh; short human Chinese QC |
| 37 | `rewrite_zh` | tec_forecast | one_liner_zh, desc_zh; short human Chinese QC |
| 38 | `rewrite_zh` | gnssIR-python | one_liner_zh, desc_zh; short human Chinese QC |
| 39 | `rewrite_zh` | ImuGpsGuiding | one_liner_zh, desc_zh; short human Chinese QC |
| 40 | `rewrite_zh` | GNSS-Explorer | one_liner_zh, desc_zh; short human Chinese QC |

Chinese rewrite names: ALBUS_ionosphere, Aether-IT-model, BeiDou_B1C, Cube, GITM, GNSS-Explorer, GNSS-VHDL, GPSBabel, GPSL1-DPEmodule, HTDP, ImuGpsGuiding, LongwaveModePropagator.jl, PPP-RTK-Beechan, Seemala-GPS-TEC, TEC-calculation-MATLAB, TIE-GCM, Urban-RTKLIB, beidou-sdr-sim, cssrlib-data, geodezyx, gnss-RX, gnss-scintillation-simulator, gnss2tws-green, gnssIR-matlab-v3, gnssIR-python, hardware, hatanaka, jvierine-ionosonde, mphw, polaris, pygnsslab, rtcm-rs, tec-suite, tec_forecast, viresclient

Full machine log (gitignored): `research/_qc_touch_log_20260924_batch11.json`.
Keep audits: `research/_qc_batch11_prov_keep.json`.

## Counts after sync
- `project_count`: **802**
- `counts_by_category`: `{"gnss-data": 117, "gnss-datasets": 124, "gnss-positioning": 89, "gnss-sdr": 61, "ionosphere": 240, "mobile-apps": 21, "navigation-ins": 63, "orbit-clock": 14, "tools-learning": 36, "troposphere": 37}`
- `provenance_counts`: `{"official": 230, "academic_lab": 276, "personal_community": 296}`
- `updated`: **2026-09-24**
- Remaining empty license: **169**
- Remaining empty language: **34**
- Remaining HTTP: same 6
- `desc_zh` == `one_liner_zh`: **367**
- `core` / `featured` policy: unchanged (no bulk flip)

## Top remaining issues (batch 12)
1. **~169 empty licenses** — GitHub null/NOASSERTION dominant; optional non-GitHub LICENSE page reads only when high-confidence SPDX exists.
2. **~34 empty languages** — data/awesome-lists or quirky API primaries; do not invent.
3. **6 HTTP URLs** — PPP-Wizard×2, eSWua, IONORING, Autoscala, Beihang ionosphere.cn; HTTPS still unreachable.
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh` ≈367) — continue short human polish on remaining software (avoid portal walls). Suggested leftovers: FlyDog-SDR-GPS / GPSGALSSS / gnss-signal-simulator-rs / msckfvioGPS / STM32Primer2-GNSS-Tracker / gnss-sdr-1pps / awesome-gnss-hdkarimi / BNS / ntrip-client / M_GIM-zcytju / ntrip-caster-go / BNC-source-FTP / gnssgo / PW_from_GPS / pylgrim / BUAA-RINEX-Convertor / GHASP-HAS-decoding / GNSSRMERRByS.
5. **`core` vs `featured` drift** — decide policy before bulk flip; SH-GIM stays owned special.
6. Guard against routine-merge overwrites (SPDX / provenance / Chinese) — `_merge_fields.py` preserve path.
7. More professor/lab personal-account spot-audits only when org/bio is clear (e.g. borioda/GHASP-HAS-decoding kept pending company field).
