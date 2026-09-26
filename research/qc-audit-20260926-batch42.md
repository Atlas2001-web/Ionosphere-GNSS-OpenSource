# QC audit — 2026-09-26 batch 42 (fork / near-duplicate audit + leftovers + category spot-check)

Base: origin/main ac78f8e (batch 41). Catalog **1035 → 1032** (3 pure-duplicate fork removals, no adds). Evidence read 2026-09-26 (ET) via `gh api` (GraphQL `isFork/parent/pushedAt`, REST `compare`, `branches`).

## Task 0 — entries newer than batch 41
None: HEAD = origin/main = ac78f8e, `project_count` 1035, no project appended after batch 41. Nothing to QC.

## Task 1 — fork / near-duplicate audit
Scope: all 683 github.com entries resolved via GraphQL (0 unresolved, 0 renamed-to-same-repo collisions). 9 are forks:

| idx (pre) | entry | parent | parent in catalog? | evidence | decision |
|---|---|---|---|---|---|
| 35 | GNSSNexus-rinex (GNSSNexus/rinex) | nav-solutions/rinex | yes (`rinex`) | compare main: ahead 0 / behind 133; fork created 2024-08-21, `pushed_at` 2024-08-20 (never pushed after forking); 0★; extra branches are upstream copies | **REMOVED** (pure duplicate). Nothing to merge: `rinex` entry is richer (126★, core, MPL-2.0 correct; the fork entry's `Apache-2.0` was wrong anyway) |
| 355 | IonKit-NH (ohm1122/IonKit-NH) | tanggdut/IonKit-NH | yes (`IonKit-NH-tanggdut`) | ahead 0 / behind 1; created 2024-05-25, pushed 2024-05-14 (never pushed); batch 41 already confirmed identical zip | **REMOVED**; original renamed `IonKit-NH-tanggdut` → `IonKit-NH` (suffix only existed to disambiguate), one_liner_zh rewritten, analysis_zh notes the unchanged ohm1122 fork. Original already carries `starred` / `user_relation: starred` |
| 432 | OASIS-ohm1122 (ohm1122/OASIS) | giorgiopicanco/OASIS | yes (`OASIS`) | ahead 0 / behind 28; created 2025-05-01, pushed 2025-04-30 (never pushed); 1★ vs 16★ | **REMOVED**; `OASIS` analysis_zh gains one sentence noting the fork. `user_relation`/`starred` NOT copied to OASIS (maintainer starred the fork, not upstream — would be a false claim). Two references in `docs/tutorials/05-scintillation-roti.md` dropped |
| 186 | MALIB (JAXA-SNU) | tomojitakasu/RTKLIB | yes | compare: no common ancestor (history rewritten); pushed 2026-01, MADOCA L6E work | keep both; desc already "RTKLIB 衍生的 MADOCA 工具包" |
| 216 | RTKLIB-explorer | tomojitakasu/RTKLIB | yes | no common ancestor; pushed 2026-09-22, 975★ (demo5) | keep both; desc already explains demo5 branch |
| 535 | GREAT-MSF | GREAT-WHU/GREAT-PVT | yes | head 4366a53 vs PVT 8bd3d23, compare: no common ancestor; GNSS/INS fusion product | keep both; desc explains (multi-sensor fusion vs PVT) |
| 257 | gps-qzss-sdr-sim (iGNSS) | Yuta811x/gnss-sdr-sim | **no** | ahead 0 / behind 22; created 2023-05-21, pushed 2023-03-13 (never pushed) | report only: parent Yuta811x/gnss-sdr-sim (7★, pushed 2024-01) is the canonical project |
| 422 | NeQuickJRC (mgfernan) | odrisci/NeQuickJRC | no | ahead **54** / behind 0, 135 files; pushed 2026-07 vs parent 2019-12 | fork is the better project; keep, nothing to report as canonical swap |
| 699 | gnssFGO (hz658832) | rwth-irt/gnssFGO | no | diverged: ahead 2 (Docker/doc PR, 2025-03) / behind 3 (parent "added new datasets for offline processing; added visual odom", "updated readme"); parent archived, description "official repo" | report only (borderline): archived official parent has 3 commits the fork lacks; current entry text says maintenance moved to the fork, which matches the fork being the live one |

Same-project, non-fork pairs checked (repo-name / display-name clustering): m_gim-PANXIONG vs M_GIM-zcytju, GVINS-HKUST vs GVINS-WHU, SoftGNSS vs SoftGNSS-octave, AETHER vs Aether-IT-model, awesome-gnss ×2, ntripcaster family, pygnss ×2 — all distinct projects (earlier batches concur). Website-vs-repo pairs of one project (gpsd vs gpsd-website, BKG-NtripCaster vs Caster-source-FTP, SPOCC vs GFZ-SPOCC-news vs IGSMAIL-SPOCC) point at different resources (repo / docs site / tarball dir / announcement) → not removed; listed as candidates below.

## Task 2 — leftovers
- IRI-COMMON-FILES (https://irimodel.org/COMMON_FILES/): `language` `Fortran` → `null`. Dir listing = 00_ccir-ursi.tar/.zip + ccir11–22.asc + ursi11–22.asc only (no code). Convention: data-only entries use null (IRI-indices on the same site, BDS-3-PPP-B2b-DATA).
- GRID (mmurrian/GRID) and HASlibTestSuite (nlsfi/HASlibTestSuite): still present, untouched.

## Task 3 — category spot-check
Stratified random sample of 60 (6 per category, seed 42) + keyword scans (tropo/neutral terms in ionosphere, iono terms in troposphere, non-portal entries in gnss-datasets, non-SDR text in gnss-sdr).

Fixed (clear-cut):
- LEOGPS (sammmlow/LEOGPS): `gnss-sdr / 星载导航` → `gnss-positioning / 相对定位`. It reads RINEX observations and estimates carrier-phase relative baselines between two formation-flying LEO satellites (topics: baseline, rinex, formation-flying, estimation) — no signal processing / receiver, unlike its old neighbours oresat-gps-hardware/software.

Borderline (reported, not moved):
- pymsis, Python-NRLMSISE-00 (ionosphere/中性大气, NRLMSISE) and NCAR-GLOW (气辉模型): thermosphere neutral density / airglow, not ionosphere proper, but no existing upper-atmosphere category (troposphere = lower-atmosphere delays).
- gnss2tws-green (tools-learning/数据集): software for GNSS vertical displacement → TWS inversion, not a dataset; no hydrology category.
- polaris (tools-learning/RTK网络客户端): Point One RTK network client SDK; could sit in gnss-positioning/RTK客户端.
- 56 ionosphere `data-portal` entries vs gnss-datasets/电离层产品: long-standing split, not changed.
- Sampled entries otherwise consistent.

## Regeneration / validation
- Dry-run of `research/merge_routine_20260926c` regenerate_lists/regenerate_categories/regenerate_readme before edits: no diff.
- After edits: PROJECTS.json diff = 3 removed objects, 1 rename + one_liner + analysis (IonKit-NH), 1 analysis (OASIS), 1 language (IRI-COMMON-FILES), 1 category/subcategory (LEOGPS), counts. Regenerated lists 01/03/04/07, categories.md, README counts; tutorial 05 name refs.
- JSON valid; project_count 1032 = len(projects); counts_by_category {ionosphere 298, troposphere 49, gnss-data 139, gnss-positioning 104, orbit-clock 33, navigation-ins 73, gnss-sdr 76, mobile-apps 32, tools-learning 59, gnss-datasets 169}; provenance {official 344, academic_lab 355, personal_community 333} match data; no duplicate URLs/names.

## Leftovers
- gps-qzss-sdr-sim: consider replacing with parent Yuta811x/gnss-sdr-sim (fork untouched since forking).
- gnssFGO: archived parent rwth-irt/gnssFGO has 3 commits (datasets, visual odom) not in hz658832 fork.
- Website/repo pairs (gpsd/gpsd-website, BKG-NtripCaster/Caster-source-FTP, SPOCC trio) — possible consolidation, needs owner decision.
- Batch-41 leftovers unchanged: MathWorks-ionex_reader licence, ESA-UGI / IMSP-MGS / IONOLAB language `unknown`, IRI-COMMON-FILES licence null.
