# Catalog QC batch 56 (2026-09-26)

Base: `b684b57` (a peer docs commit on top of batch 55 `38248f0`). Lists were regenerated with the current origin/main `research/merge_routine_20260926c.py` (`regenerate_lists` / `regenerate_categories` / `regenerate_readme`, including the f387e6d CAT_META blurbs). A dry-run on the unchanged data gave zero diff. Page headers, blurbs, `docs/categories.md` and README are unchanged.

## Task 0: entries newer than 38248f0
None. `b684b57` only touched `docs/software/` (the EarthScope gnsstools manual). PROJECTS.json and lists had no changes.

## Task 1: text-shape audit of the Chinese fields (all 1028 entries)

Length distribution before the edits (min / 5% / median / 95% / max, in characters):

| field | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|
| desc_zh | 12 | 21 | 33 | 54 | 84 |
| one_liner_zh | 12 | 20 | 32 | 49 | 67 |
| analysis_zh | 38 | 72 | 134 | 240 | 345 |

After the edits: one_liner max is 60, desc_zh min is 15, and the shortest analysis_zh (not counting the owned SH-GIM stub) is 57.

What the scans found:
- **Too long:** 3 one_liner_zh over 60 characters. No desc_zh was over 150. No field looked like pasted README text: no install steps or feature bullets. The few `pip install` / `git clone` mentions sit inside Chinese sentences and were kept.
- **Mostly English:** none. Fields with a high share of Latin letters turned out to be product names, formats and acronyms (RINEX/NTRIP/…). Paper titles and repo taglines in quotes were kept as proper nouns (GTrop, M_GIM, OASIS). Two leftover English common words were translated: "Broadcaster" and "minimal release".
- **Too thin:** 2 desc_zh under 15 characters (the third short one was also fixed) and 9 analysis_zh that were only generic phrases.
- **Repeated boilerplate:** no sentence appears in 5 or more entries, except bare license tags such as "MIT 许可" and "Apache-2.0", which are facts and were kept. The filler sentence "选用前建议先跑通作者提供的最小示例" appeared in 4 entries and was removed. One entry repeated the same sentence twice (oresat).

**Edits: 22 field edits across 20 entries.**

| issue type | count | entries |
|---|---:|---|
| over-long one_liner_zh tightened | 3 | Ionort-raytrace, pyIRI2016, novatel_edie |
| thin desc_zh / one_liner fleshed out | 3 fields (2 entries) | CSNO-TARC-Differential (desc + one_liner), go-gnss-rtcm (desc) |
| thin analysis_zh fleshed out from upstream README (gh api) | 9 | raw-gnss-fusion, geode, IndirectEKFIMUGPS, Loose-GNSS-IMU, OSNMA, gnss-sdr-monitor, galileo-sdr-sim, ge-gnss-visibility, TightlyCoupledINSGNSS |
| boilerplate / duplicated filler removed | 4 | Analog-GPS-data-receiver, Microsat-gps-sim, syncgpslidarimucam, oresat-gps-software (also dropped its duplicated 星上存储配额 sentence) |
| leftover English common words translated | 3 fields (2 entries) | ntripcaster-libev (one_liner + analysis), Ion-Phys-Toolkit (analysis) |

Examples (before → after):
1. Ionort-raytrace one_liner: `Ionort-raytrace：INGV IONORT 三维 HF 射线追踪（MATLAB 界面 + 预编译 Fortran 求解器）` (67) → `Ionort-raytrace：INGV IONORT 三维 HF 射线追踪（MATLAB + Fortran）`
2. novatel_edie one_liner: `NovAtel 厂商发布的 EDIE 编解码 SDK：OEM7 接收机日志/命令的 C++ 与 Python 解析与格式转换` (62) → `novatel_edie：NovAtel 官方 OEM7 日志编解码 SDK（C++/Python）`
3. CSNO-TARC-Differential desc: `TARC 差分数据英文页` → `中国卫星导航系统管理办公室测试评估研究中心（TARC）差分数据英文说明页` (the organization name comes from the page title; the page is a JS app with no readable text)
4. raw-gnss-fusion analysis: `便于复现论文设定的原始测量与融合流水线。适合研究起步。不是开箱商用导航软件。` → an ICRA 2023 paper companion: a factor graph fuses raw GNSS carrier phase with IMU and lidar and needs no base station. The repo has three parts (GTSAM+GPSTk demo, dataset instructions, results) and runs on Python 3.7 with GPSTk 8.
5. OSNMA analysis: `实现 Galileo 开放业务消息认证（OSNMA），用于抗欺骗研究与接收机试验。适合安全/完好性方向。` → OSNMAlib verifies the public key, TESLA keys, MACK and ADKD 0/4/12 tags. It passes the ICD test vectors, supports cold/warm/hot start, JSON output and TTFAF, and can sync time via NTP. Note that the public key changed from ID 1 to ID 2 in 2025-12.
6. gnss-sdr-monitor analysis: `给 gnss-sdr 用的实时 GUI 监视器，看通道与 PVT 状态更直观。依赖 GNSS-SDR 主程序。` → a Qt GUI that receives the Monitor and PVT serialized streams over UDP and shows C/N0, Doppler, the constellation and a map. Both outputs must be enabled in the GNSS-SDR config.
7. oresat-gps-software analysis: `…星上算力与存储配额会限制可开日志级别。星上存储配额会限制可长期开启的日志等级。选用前建议先跑通作者提供的最小示例。` → `…星上算力与存储配额会限制可长期开启的日志等级。`
8. ntripcaster-libev one_liner: `ntripcaster：libev 高性能 NTRIP Broadcaster` → `ntripcaster：基于 libev 的高性能 NTRIP 播发器`

Noted, not changed: many data-portal entries use the same text for desc_zh and one_liner_zh. That is allowed by the schema, so it was left alone.

## Validation
- PROJECTS.json parses. 1028 projects. Provenance 330/214/484. 152 (category, subcategory) groups. `counts_by_category` and `provenance_counts` match the data.
- Every list header count equals its table row count: 247/48/137/108/31/72/76/32/57/220. Each of the 1028 URLs appears exactly once across the lists.
- The diff only touches the edited rows and detail paragraphs. No page header or blurb line changed, and `docs/categories.md` and README are untouched.
- No projects were added or removed. No URL, category, subcategory or provenance changed.
