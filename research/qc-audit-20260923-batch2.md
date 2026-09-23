# Catalog QC audit — 2026-09-23 batch 2

## Scope
- Repo: [Atlas2001-web/Ionosphere-GNSS-OpenSource](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource) (`main`)
- Baseline after batch 1 (`d9e4898`) + routine `fe8a9d0` (+15): **733** entries
- Goal: QC only (no new projects) — empty license/language, remaining HTTP, Chinese blurbs

## Pre-fix scan

| Issue class | Count / finding |
|---|---|
| Empty `license` | **202** (≈189 GitHub) |
| Empty `language` | **41** (≈37 GitHub) |
| HTTP (non-HTTPS) URLs | **6** (PPP-Wizard×2, eSWua, IONORING, Autoscala, ionosphere.cn) |
| Long `analysis_zh` (>280) | **3** (TITIPy, RINGO, IRI-Plas-SPIM-IZMIRAN) |
| Empty Chinese fields | **0** |
| HTTPS probe for leftover HTTP | all **fail** (connection); HTTP still **200** → leave |

## This batch — summary
- License fills via `gh api repos/{owner}/{repo}` `.license.spdx_id`: **22** (skip `null` / `NOASSERTION`)
- Language fills via same API `.language` (sane primaries only): **7**
- Chinese rewrites (`desc_zh` / `one_liner_zh` / `analysis_zh`): **20** entries
- HTTP upgrades: **0** (none verified)
- Entries touched (unique names): **42**
- `project_count` unchanged: **733**
- `lists/*.md` regenerated so language column reflects fills

## Touch log

| # | Action | Name | Fields / detail |
|---|---|---|---|
| 1 | `meta_fill` | GNSSSDRHACKRF | license; gh api repos → license='MIT' language=None |
| 2 | `meta_fill` | gps-qzss-sdr-sim | license; gh api repos → license='MIT' language=None |
| 3 | `meta_fill` | hardware | license, language; gh api repos → license='CERN-OHL-S-2.0' language='Makefile' |
| 4 | `meta_fill` | multi-channel-gnss | license; gh api repos → license='MIT' language=None |
| 5 | `meta_fill` | Geometric-Matrix-For-Ionospheric-Tomogrphy | license, language; gh api repos → license='GPL-3.0' language='C++' |
| 6 | `meta_fill` | Get_IPP | language; gh api repos → license=None language='C++' |
| 7 | `meta_fill` | GNSS.IonosphereMaps | license, language; gh api repos → license='Apache-2.0' language='Java' |
| 8 | `meta_fill` | INX_Editor | license; gh api repos → license='GPL-3.0' language=None |
| 9 | `meta_fill` | IonKit-NH | license; gh api repos → license='GPL-3.0' language=None |
| 10 | `meta_fill` | IonKit-NH-tanggdut | license; gh api repos → license='GPL-3.0' language=None |
| 11 | `meta_fill` | IonTools | language; gh api repos → license='NOASSERTION' language='C++' |
| 12 | `meta_fill` | IRI2020_parameters | license, language; gh api repos → license='BSD-2-Clause' language='MATLAB' |
| 13 | `meta_fill` | vtec | license; gh api repos → license='MIT' language=None |
| 14 | `meta_fill` | WA_ion_model_PPP | language; gh api repos → license=None language='C++' |
| 15 | `meta_fill` | gnatss | license; gh api repos → license='BSD-3-Clause' language='Python' |
| 16 | `meta_fill` | Analog-GPS-data-receiver | license; gh api repos → license='MIT' language='C' |
| 17 | `meta_fill` | BDS-3-B1C-B2a-SDR-receiver | license; gh api repos → license='GPL-2.0' language='MATLAB' |
| 18 | `meta_fill` | ESP32-SDR-GPS | license; gh api repos → license='MIT' language='C' |
| 19 | `meta_fill` | GNSS-DSP-tools | license; gh api repos → license='MIT' language='Python' |
| 20 | `meta_fill` | GNSS-GPS-SDR | license; gh api repos → license='GPL-2.0' language='Python' |
| 21 | `meta_fill` | gnss-rcv | license; gh api repos → license='MIT' language='Rust' |
| 22 | `meta_fill` | gnss-RX | license; gh api repos → license='BSD-3-Clause' language='MATLAB' |
| 23 | `meta_fill` | gps | license; gh api repos → license='GPL-3.0' language='Python' |
| 24 | `meta_fill` | meta-gnss-sdr | license; gh api repos → license='MIT' language='C' |
| 25 | `meta_fill` | oresat-gps-software | license; gh api repos → license='GPL-3.0' language='Python' |
| 26 | `rewrite_zh` | TITIPy | analysis_zh; short human Chinese QC |
| 27 | `rewrite_zh` | RINGO | analysis_zh; short human Chinese QC |
| 28 | `rewrite_zh` | IRI-Plas-SPIM-IZMIRAN | analysis_zh; short human Chinese QC |
| 29 | `rewrite_zh` | IonTools | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 30 | `rewrite_zh` | Fast_GNSS_ReceiverMATLAB | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 31 | `rewrite_zh` | POSGO | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 32 | `rewrite_zh` | OpenRTK | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 33 | `rewrite_zh` | GNSS-SDRLIB | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 34 | `rewrite_zh` | gnsstk-apps | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 35 | `rewrite_zh` | IRI-MATLAB-FileExchange | analysis_zh; short human Chinese QC |
| 36 | `rewrite_zh` | IBGE-PPP-API | analysis_zh; short human Chinese QC |
| 37 | `rewrite_zh` | IGP-TUDelft | analysis_zh; short human Chinese QC |
| 38 | `rewrite_zh` | FARR | analysis_zh; short human Chinese QC |
| 39 | `rewrite_zh` | FAST | desc_zh, one_liner_zh; short human Chinese QC |
| 40 | `rewrite_zh` | Net_Diff | desc_zh, one_liner_zh; short human Chinese QC |
| 41 | `rewrite_zh` | gnss-sdr | desc_zh, one_liner_zh; short human Chinese QC |
| 42 | `rewrite_zh` | nmea-msgs | desc_zh, one_liner_zh; short human Chinese QC |
| 43 | `rewrite_zh` | laika | desc_zh, one_liner_zh; short human Chinese QC |
| 44 | `rewrite_zh` | GNSS.IonosphereMaps | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |
| 45 | `rewrite_zh` | Geometric-Matrix-For-Ionospheric-Tomogrphy | desc_zh, one_liner_zh, analysis_zh; short human Chinese QC |

## Counts after sync
- `project_count`: **733**
- `counts_by_category`: `{"ionosphere": 236, "troposphere": 32, "gnss-data": 111, "gnss-positioning": 82, "orbit-clock": 13, "navigation-ins": 59, "gnss-sdr": 59, "mobile-apps": 16, "tools-learning": 31, "gnss-datasets": 94}`
- `provenance_counts`: `{"official": 194, "academic_lab": 217, "personal_community": 322}`
- Remaining empty license ≈ **180**; empty language ≈ **34**
- Remaining HTTP: CNES-PPP-WIZARD-Realtime-Products, eSWua-TEC, IONORING, PPP-Wizard, Autoscala-INGV, Beihang-Ionosphere-CN

## Top remaining issues (batch 3)
1. **~180 empty licenses** — many GitHub repos truly have no LICENSE / `NOASSERTION`; continue only where SPDX exists; optional non-GitHub license pages.
2. **~34 empty languages** — leftovers are often data portals, awesome-lists, or API `language: null`; do not invent.
3. **6 HTTP URLs** — PPP-Wizard, eSWua, IONORING, Autoscala, Beihang ionosphere.cn still lack working HTTPS; keep until canonical HTTPS appears (optional `url_note`).
4. Mild Chinese sameness (`desc_zh` == `one_liner_zh`) still common for portals — polish only when misleading.
5. GitHub primary-language quirks (PostScript / HTML / OpenEdge ABL etc.) skipped this batch — manual review if needed.
