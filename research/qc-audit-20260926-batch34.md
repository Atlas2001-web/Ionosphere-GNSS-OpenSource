# QC audit — batch 34 (2026-09-26)

Scope: the 28 entries added in 3cf61b1 (+13) and c28928e (+15), idx 998–1025. Catalog total 1036 after concurrent routine 26c (+10, dd88974, not QCed here); this batch adds/removes nothing.

## desc_zh
- All 28 had `desc_zh == one_liner_zh` (routine default). Rewrote all 28 as short, distinct, usage-oriented lines, checked against upstream READMEs (gh api) and portal pages / verified analysis_zh.

## license / language (gh repo view + gh api languages + LICENSE files)
- 14 GitHub repos: all recorded licenses/languages match. NOASSERTION cases read: ChaosMagPy LICENSE = MIT (gallery examples LGPL-3.0) → MIT kept; MIPS LICENSE = BSD 2-clause → BSD-2-Clause kept. LPI is C+R, primary R → kept.
- ROM SAF: `portal-terms` → `CC-BY-4.0` (site footer: "ROM SAF products are licensed under CC BY 4.0 by EUMETSAT").

## URLs
- All reachable (curl -sIL): 200, except USGS Geomagnetism (403 to curl, 200 in browser/WebFetch; kept). MACCS stays http:// (https fails to connect). romsaf.org redirects to rom-saf.eumetsat.int (catalog URL already canonical).

## ROM SAF re-classification
- Evidence (rom-saf.eumetsat.int home + product_archive.php + product_documents.php): NRT/offline/CDR/ICDR products = bending angle, refractivity, dry temperature, 1D-Var T/q/p/surface pressure, tropopause height, gridded monthly means; ATBDs cover only these. No ionospheric (Ne/TEC) product anywhere.
- Before: `gnss-datasets` / `电离层产品`. After: `troposphere` / `GNSS掩星/RO` (existing category; subcategory label reused from awsgnssroutils). one_liner_zh, analysis_zh (removed "对流层与电离层剖面" claim; neutral-atmosphere/NWP/climate), registration_zh updated.
- Other RO entries, not changed: COSMIC-CDAAC and COSMIC-GNSS-RO-Data = `gnss-datasets`/`掩星` (CDAAC also serves ionospheric profiles, so mixed); awsgnssroutils = `gnss-datasets`/`GNSS掩星/RO`; ROM-SAF-ROPP = `ionosphere`/`GNSS掩星处理`; cosmic-crunch / pysatCDAAC = `gnss-data`.

## Duplicates
- None by normalized URL or name. Near-neighbours kept separate: CEDAR Madrigal (cedar.openmadrigal.org data instance) vs OpenMadrigal (software home); RAL Ionosonde vs UKSSDC home; BGS data service vs BGS-INTERMAGNET (imag-data).

## Provenance
- No changes (no high-confidence contrary evidence).

## Regeneration
- `research/merge_routine_20260926c.regenerate_lists (identical generator to 26b)` + `regenerate_categories` + `regenerate_readme`: only troposphere/gnss-datasets counts (47→48, 170→169) and the ROM SAF block moved.

## Leftovers
- ROM-SAF-ROPP sits in `ionosphere` though ROPP is mainly neutral-atmosphere RO processing (it does include an ionospheric correction step); not in scope, not changed.
- Non-SPDX license strings kept: USGS `USGov public resource`, BGS `academic non-commercial`, `portal-terms`.
