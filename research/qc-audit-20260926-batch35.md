# QC audit — batch 35 (2026-09-26)

Scope: round-23 entries idx 1026–1035 (routine 26c: AeroRust nmea … BDS-RawScope); no newer entries existed. Plus ROM-SAF-ROPP category review. Adds/removes nothing; total stays 1036.

## desc_zh
- All 10 had `desc_zh == one_liner_zh`. Rewrote all 10 as short, distinct usage lines, checked against upstream READMEs (gh api).

## license / language (gh api repos + languages + LICENSE files)
- All 10 recorded licenses/languages match. NOASSERTION cases read: AeroRust nmea LICENSE.txt + Cargo.toml = Apache-2.0; SparkFun LICENSE.md = MIT for code (CC BY-SA 4.0 hardware) → MIT kept. smartphone-gnss-booster primary language C (vendored RTKLIB JNI; Kotlin app) → kept as GitHub reports.

## URLs
- All 200 (curl -L). Normalised 5 to GitHub canonical owner/repo case: Ryanf55/trimble-gsof-wireshark, taroz/Smartphone-GNSS-Booster, sunshineharry/UM982Driver, zltan-whu/UnicoreDriver, sinyl-labs/BDS-RawScope (norm_url lowercases, so dedupe unaffected).

## Provenance
- smartphone-gnss-booster: academic_lab → personal_community. Personal `taroz` account, README names no lab/institution; aligns with the 5 other taroz entries (gtsam_gnss, MatRTKLIB, GNSS-SDRLIB, TouchRTKStation, gsdc2023, ge-gnss-visibility all personal_community).

## Duplicates
- None by normalized URL or name across 1036 entries.

## ROM-SAF-ROPP → troposphere / GNSS掩星/RO
- Evidence (rom-saf.eumetsat.int/ropp/ + ROPP Overview v12.0 romsaf_ropp_ov.pdf): stated aim "pre-process RO data … plus RO-specific components to assist with the assimilation of these data in NWP systems". Modules: UTILS, IO, PP (excess phase → L1/L2 bending angle → ionospherically corrected bending angle/refractivity/dry temperature), APPS (tropopause & PBL height), FM (refractivity/bending-angle forward models + TL/AD), 1DVAR (T/q/p). Ionosphere appears as the correction step, plus an add-on electron-density 1D-Var tool (ROPP-11) and AVHIRO2 retrieval (ROPP-12).
- Decision: predominantly neutral atmosphere → moved from `ionosphere`/`GNSS掩星处理` to `troposphere`/`GNSS掩星/RO` (next to ROM SAF). one_liner_zh / analysis_zh rewritten (keeps mention of the Ne 1D-Var tools; dropped "开源" claim); desc_zh tweaked.
- License string `ROM SAF scientific (registration)` → `ROM SAF licence (registration, no redistribution)` per romsaf_ropp_licence.pdf (free, internal use, no redistribution; not SPDX).
- Tutorials 07 (table column) and 08 (list pointer) updated so they no longer point ROPP to list 01.

## Counts
- ionosphere 302→301, troposphere 48→49; provenance academic_lab 356→355, personal_community 336→337.

## Regeneration
- `research/merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme`.

## Leftovers
- Other RO entries unchanged: COSMIC-CDAAC / COSMIC-GNSS-RO-Data (`gnss-datasets`/`掩星`), awsgnssroutils (`gnss-datasets`/`GNSS掩星/RO`), cosmic-crunch / pysatCDAAC (`gnss-data`).
- Non-SPDX license strings still present (USGS, BGS, portal-terms, ROM SAF licence).
