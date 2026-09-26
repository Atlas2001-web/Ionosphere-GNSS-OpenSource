# QC audit — batch 36 (2026-09-26)

- Catalog total: 1036 (unchanged since batch 35 / 7950c54); no entries past idx 1035 → no new-ingestion QC.
- Systematic `gh api repos/OWNER/REPO` + `/languages` sweep of all 525 GitHub entries in idx 0–699 and 951–997 (idx 649 GeoPack checked via its base repo).
  - 404 / deleted: none. Archived repos were not changed.
  - Moved/renamed: none. Owner case normalised to GitHub `full_name`:
    - 170 GNSSRTK: `SupakunZ/GNSS_RTK` → `supakunz/GNSS_RTK`
    - 653 SparkFun_u-blox_GNSS_v3: `SparkFun/SparkFun_u-blox_GNSS_v3` → `sparkfun/SparkFun_u-blox_GNSS_v3`
  - Language: no entry where the recorded language is missing from the repo's languages, except these two, left as-is:
    - 464 roti-gnss-ml: Python (GitHub counts it as Jupyter Notebook; the notebooks are Python)
    - 648 ATom: MATLAB (the code ships as a zip, so GitHub finds no languages; the manual says MATLAB)
  - License: no contradictions with GitHub SPDX. Spot-read LICENSE for NOASSERTION entries that have a recorded value (Cube → RTKLIB BSD-2, qzsl6tool BSD-2, AlouetteApp MIT, dvoacap-python MIT, SparkFun v3 code MIT / hardware CC BY-SA): all consistent, kept.
- Lists regenerated via `research/merge_routine_20260926c.regenerate_lists/regenerate_categories/regenerate_readme`. Diff touches only the 2 URL cells + detail headers. Counts unchanged.
- Leftovers: 31 entries in scope have an empty `language` (e.g. awesome lists, data repos, gnsstk-apps). They were left blank, not guessed. Several licenses are blank or non-SPDX where GitHub says NOASSERTION (gLAB, gnsstk, ginan, RTKLIB fork, Kamodo `NASA-Open`, tiegcm, HTDP, …). These weren't contradictions, so they were left for a dedicated license-fill pass.
