# QC audit — batch 33 (2026-09-26)

- Catalog total: 998 (unchanged since batch 32 / 0d38536); no entries past idx 997 → no new-ingestion QC.
- Sampled 42 older entries (idx 700–950) for desc_zh/analysis_zh claims against READMEs (GRITI/PSU, ELT_RTKBase ZED-X20P, VN-DGNSS UCR + GPS L1/BDS B1/GAL E1, ionFR IGRF/IONEX, RMextract→Spinifex, LimeGPS archived, pynex archived, gnssSNR, NeRC, etc.): no factual errors found.
- Systematic `gh api repos/*` sweep of all 135 GitHub entries in idx 700–950 (license/language/moved):
  - License: no mismatches (NOASSERTION entries left as-is, LICENSE files already checked earlier).
  - Language fixed (repo contains zero bytes of the recorded language):
    - 758 GalileoHack: Kotlin → Java (Java 151k, Processing 7k)
    - 791 TouchRTKStation: C → Python (100% Python/Batch/Shell)
    - 792 gsdc2023: Python → MATLAB (100% MATLAB)
    - 797 FresnelMaps: Python → MATLAB (100% MATLAB)
  - Left as-is (linguist byte-count artifacts; recorded language is the user-facing interface): igrf, wmm2020, aacgmv2, NCAR-GLOW, pysatCDF, tudatpy, PrNet, E2EPrNet, GraphGNSSLib_LEO, libswiftnav (Pawn), gpsdo (Arduino), Robust-GNSS-FG-GMM-TD (vendored code excluded → Shell), SoftGNSS-octave (Objective-C = .m misdetect).
- Lists regenerated via `research/merge_routine_20260924s.regenerate_lists`; diff touches only the 4 language cells + detail lines.
- Leftovers: wmm2020 license string `public-domain` is non-SPDX (LICENSE.txt says US-gov public domain; kept).
