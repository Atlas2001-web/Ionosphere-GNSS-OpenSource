# GNSS catalog exhaustive search log

- Generated: 2026-09-14 (executor subagent)
- Catalog size at write time: **255** projects in `PROJECTS.json`
- Additional verified finds: **54** → `research/more_finds.json`
- Search result JSON files under `/tmp/gh_search_results`: **148**

## Method

1. `gh search repos --topic …` for gnss, ionosphere, rinex, ppp, rtk, beidou, tec, ionex, scintillation, troposphere, rtklib, ntrip, gps, galileo, glonass, sbas, etc.
2. Keyword searches (sorted by stars, limit 30–100) covering TEC/IONEX/ROTI, troposphere ZTD/PWV/VMF, RINEX/NTRIP/RTCM, PPP/RTK/B2b/HAS, cycle slip, Chinese labs.
3. `user:` searches: i2Nav-WHU, GREAT-WHU, PrideLab, XiaoGongWei, zhufengGNSS, yxw027, Jin-Whu, IPNL-POLYU, h-shiono, UCAS-Liuchunbo, GYH-WHU, salmoshu, embrace-inpe, zhangwhu, MayHarryWang, …
4. Chinese queries: 电离层, 精密单点定位, 北斗 PPP, 周跳, 电离层层析, …
5. Dedup against live `PROJECTS.json` URLs; verify each keep with `gh api repos/{owner}/{repo}`; no invented URLs.

## Hit counts by query file

| kind | query/file | hits |
|---|---|---:|
| chinese | `zh_87186605b71126f06923c06c7380bbc0` | 30 |
| chinese | `zh_de495a23` | 30 |
| chinese | `zh_2a1e2ad4` | 19 |
| chinese | `zh_330424774d06a59344c544dea6c32542` | 19 |
| chinese | `zh_32d93ce9` | 0 |
| chinese | `zh_3f6f1668` | 0 |
| chinese | `zh_7782d63b3ae3d3984a6467fec868628d` | 0 |
| chinese | `zh_94d4043b4276ae269eb6b582f2b683c6` | 0 |
| gap-keyword | `PPPLib` | 13 |
| gap-keyword | `GAMP_PPP` | 2 |
| gap-keyword | `ROTI_calculation` | 1 |
| gap-keyword | `BDS_B2b_PPP` | 0 |
| gap-keyword | `BeiDou_BDS_PPP_OR_RTK` | 0 |
| gap-keyword | `GPT2_OR_GPT3_GNSS` | 0 |
| gap-keyword | `IGS_download_GNSS_OR_CDDIS` | 0 |
| gap-keyword | `Net_Diff_GNSS_OR_PPP` | 0 |
| gap-keyword | `PWV_GNSS_estimation` | 0 |
| gap-keyword | `RAIM_GNSS` | 0 |
| gap-keyword | `S4_scintillation` | 0 |
| gap-keyword | `VMF1_OR_VMF3_GNSS` | 0 |
| gap-keyword | `ZTD_estimation_GNSS` | 0 |
| gap-keyword | `ambiguity_resolution_GNSS_LAMBDA` | 0 |
| gap-keyword | `cycle_slip_GNSS_OR_RINEX` | 0 |
| gap-keyword | `gnss_downloader_rinex` | 0 |
| gap-keyword | `multipath_GNSS_detection` | 0 |
| gap-keyword | `scintillation_monitor_GNSS` | 0 |
| gap-keyword | `tropospheric_delay_GNSS` | 0 |
| gap2-keyword | `user_whigg` | 30 |
| gap2-keyword | `ionospheric_scintillation` | 20 |
| gap2-keyword | `gnssrefl` | 18 |
| gap2-keyword | `PPP_B2b` | 10 |
| gap2-keyword | `user_salmoshu` | 10 |
| gap2-keyword | `user_hshiono` | 9 |
| gap2-keyword | `user_IPNLPOLYU` | 8 |
| gap2-keyword | `rinex_download` | 7 |
| gap2-keyword | `user_GYHWHU` | 7 |
| gap2-keyword | `user_embraceinpe` | 4 |
| gap2-keyword | `user_zhangwhu` | 3 |
| gap2-keyword | `CLAS_MADOCA` | 2 |
| gap2-keyword | `user_MayHarryWang` | 2 |
| gap2-keyword | `user_UCASLiuchunbo` | 2 |
| gap2-keyword | `CDDIS_download` | 1 |
| gap2-keyword | `IGS_product_download` | 1 |
| gap2-keyword | `BDSPPP` | 0 |
| gap2-keyword | `FetchData_GNSS` | 0 |
| gap2-keyword | `GNSS_ROTI` | 0 |
| gap2-keyword | `OSB_GNSS` | 0 |
| gap2-keyword | `PWV_precipitable_water_GNSS` | 0 |
| gap2-keyword | `ZTD_GNSS_OR_troposphere` | 0 |
| gap2-keyword | `isb_dcb_gnss` | 0 |
| gap2-keyword | `phase_bias_UPD_GNSS` | 0 |
| gap2-keyword | `scintillation_GNSS_OR_GPS_S4` | 0 |
| keyword | `kw_NTRIP_caster` | 50 |
| keyword | `kw_PPP_RTK` | 33 |
| keyword | `kw_software_defined_GNSS_receiver` | 9 |
| keyword | `kw_BeiDou_PPP` | 2 |
| keyword | `kw_GREAT_IFCB` | 1 |
| keyword | `kw_ANTEX_SP3_GNSS` | 0 |
| keyword | `kw_DCB_estimation_GNSS` | 0 |
| keyword | `kw_GAMP_GNSS_PPP` | 0 |
| keyword | `kw_GNSS_INS_tightly_coupled` | 0 |
| keyword | `kw_GNSS_meteorology_PWV` | 0 |
| keyword | `kw_Hatanaka_CRX2RNX` | 0 |
| keyword | `kw_IGS_product_download_GNSS` | 0 |
| keyword | `kw_MG_APP_GNSS` | 0 |
| keyword | `kw_NeQuick_ionosphere` | 0 |
| keyword | `kw_Net_Diff_GNSS` | 0 |
| keyword | `kw_PPPH_GNSS` | 0 |
| keyword | `kw_PPP_AR_GNSS` | 0 |
| keyword | `kw_ROTI_scintillation` | 0 |
| keyword | `kw_RTCM_GNSS_decoder` | 0 |
| keyword | `kw_SINEX_GNSS` | 0 |
| keyword | `kw_VMF_mapping_function` | 0 |
| keyword | `kw_ambiguity_resolution_LAMBDA_GNSS` | 0 |
| keyword | `kw_cycle_slip_GNSS` | 0 |
| keyword | `kw_ionospheric_tomography_GNSS` | 0 |
| keyword | `kw_troposphere_GNSS_ZTD` | 0 |
| targeted | `gnss_imu` | 50 |
| targeted | `gnss_rtk` | 50 |
| targeted | `gnss_sdr` | 50 |
| targeted | `ntrip_caster` | 50 |
| targeted | `ntrip_client` | 50 |
| targeted | `rtklib` | 50 |
| targeted | `total_electron_content` | 50 |
| targeted | `ublox_gnss` | 47 |
| targeted | `precise_point_positioning` | 45 |
| targeted | `rinex_parser` | 16 |
| targeted | `gnss_ppp` | 12 |
| targeted | `gnss_ins_fusion` | 10 |
| targeted | `nequick` | 10 |
| targeted | `rtcm_parser` | 10 |
| targeted | `software_defined_gnss` | 10 |
| targeted | `rinex_reader` | 9 |
| targeted | `gnss_ionosphere` | 8 |
| targeted | `android_gnss_raw` | 5 |
| targeted | `gnss_ambiguity_resolution` | 3 |
| targeted | `gnss_cycle_slip` | 2 |
| targeted | `gnss_meteorology` | 2 |
| targeted | `hatanaka_compression` | 2 |
| targeted | `ionex_reader` | 2 |
| targeted | `cors_ntrip` | 1 |
| targeted | `roti_gnss` | 1 |
| targeted | `vmf_mapping` | 1 |
| targeted | `zenith_tropospheric_delay` | 1 |
| targeted | `beidou_bds_gnss` | 0 |
| targeted | `dcb_bias_gnss` | 0 |
| targeted | `galileo_has_gnss` | 0 |
| targeted | `gim_ionosphere` | 0 |
| targeted | `gnss_troposphere` | 0 |
| targeted | `iri2016_OR_iri2020` | 0 |
| targeted | `scintillation_index_gnss` | 0 |
| targeted | `sp3_orbit_gnss` | 0 |
| topic | `galileo` | 100 |
| topic | `gnss` | 100 |
| topic | `gps` | 100 |
| topic | `ionosphere` | 100 |
| topic | `navigation` | 100 |
| topic | `ppp` | 100 |
| topic | `rtk` | 100 |
| topic | `rinex` | 82 |
| topic | `ntrip` | 74 |
| topic | `glonass` | 69 |
| topic | `bds` | 50 |
| topic | `beidou` | 44 |
| topic | `beidou` | 44 |
| topic | `rtklib` | 42 |
| topic | `tec` | 42 |
| topic | `troposphere` | 38 |
| topic | `scintillation` | 13 |
| topic | `scintillation` | 13 |
| topic | `sbas` | 9 |
| topic | `gnss-ins` | 7 |
| topic | `ionex` | 4 |
| topic | `gnss-rtk` | 2 |
| topic | `ppp-rtk` | 1 |
| topic | `gnss-meteorology` | 0 |
| topic | `gnss-ppp` | 0 |
| topic | `ionosphere-tomography` | 0 |
| user | `g_user_whigg` | 50 |
| user | `g_user_yxw027` | 50 |
| user | `g_user_zhufengGNSS` | 50 |
| user | `g_user_GREATWHU` | 21 |
| user | `g_user_JinWhu` | 19 |
| user | `g_user_i2NavWHU` | 19 |
| user | `g_user_gnsslab` | 17 |
| user | `g_user_XiaoGongWei` | 8 |
| user | `g_user_ChangChuntao` | 2 |
| user | `g_user_PrideLab` | 2 |

## more_finds.json summary

| category | count |
|---|---:|
| gnss-data | 12 |
| gnss-positioning | 19 |
| gnss-sdr | 2 |
| ionosphere | 3 |
| mobile-apps | 1 |
| navigation-ins | 10 |
| orbit-clock | 3 |
| tools-learning | 4 |
| **total** | **54** |

## Notable gaps still thin after search

- Standalone troposphere **ZTD/PWV estimators** on GitHub remain scarce (many live in Bernese/GAMIT/large suites or TU Wien VMF pages already cataloged).
- Dedicated **IGS/CDDIS product downloaders** with stars≥3 are rare; many are 0-star personal scripts (skipped unless institutional).
- **Net_Diff / ChangChuntao FetchData / MGEX** guessed paths returned 404; GAMP/PPPH already covered via `zhufengGNSS/GAMP_PPPH` / `yxw027/PPPLib`.
- Topic `navigation`/`gps`/`ppp` alone are extremely noisy (React nav, AWS troposphere, Minecraft BDS); strict GNSS keyword filters required.

## Top stars in more_finds (sample)

- ★280 [i2Nav-WHU/awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets) — 武大 i2Nav 整理的车载 GNSS/INS 融合公开数据集列表
- ★182 [IPNL-POLYU/pyrtklib](https://github.com/IPNL-POLYU/pyrtklib) — 港理工 IPNL 的 RTKLIB Python 绑定，可直接在脚本里调用核心解算
- ★137 [i2Nav-WHU/KF-GINS-Matlab](https://github.com/i2Nav-WHU/KF-GINS-Matlab) — KF-GINS 的 MATLAB 版：EKF 松/紧组合 GNSS/INS
- ★106 [semuconsulting/pynmeagps](https://github.com/semuconsulting/pynmeagps) — 解析/生成 NMEA 0183 语句的 Python 库，与 pyubx2 同系
- ★83 [GREAT-WHU/GraphRTK-INS](https://github.com/GREAT-WHU/GraphRTK-INS) — 武大 GREAT 因子图模块：RTK 与惯导紧组合
- ★78 [h-shiono/MRTKLIB](https://github.com/h-shiono/MRTKLIB) — 面向 PPP/PPP-AR/PPP-RTK（CLAS/MADOCA）的现代 GNSS 定位库
- ★75 [i2Nav-WHU/GIOW-release](https://github.com/i2Nav-WHU/GIOW-release) — 全轮角/里程计辅助的 GNSS/INS/ODO 组合导航算法发布版
- ★74 [UCAS-Liuchunbo/RTKLIB-B2b](https://github.com/UCAS-Liuchunbo/RTKLIB-B2b) — 基于 RTKLIB 的北斗 PPP-B2b 解码与定位工具包
- ★62 [LStudioLoren/SatellitePosition](https://github.com/LStudioLoren/SatellitePosition) — Python 实现卫星单点定位与 RTK 相对定位的学习项目
- ★54 [salmoshu/RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN) — RTKLIB 中文手册解读与源码解析笔记
- ★52 [Node-NTRIP/caster](https://github.com/Node-NTRIP/caster) — 支持 NTRIP V1/V2 的 Node.js caster 库
- ★50 [hdkarimi/awesome-gnss](https://github.com/hdkarimi/awesome-gnss) — GNSS/RNSS 开源工具、数据与课程的 awesome 列表
- ★47 [i2Nav-WHU/Wheel-GINS](https://github.com/i2Nav-WHU/Wheel-GINS) — 轮式惯导与 GNSS 组合的导航系统（IEEE TITS 相关）
- ★41 [salmoshu/MobileGNSS-SPP](https://github.com/salmoshu/MobileGNSS-SPP) — 面向智能手机的 EKF 单点定位优化实现
- ★40 [heiwa0519/PPP_AR](https://github.com/heiwa0519/PPP_AR) — 多星座 PPP 模糊度固定（PPP-AR）相关实现

## Merge result

- Re-read `PROJECTS.json` at 255, appended **54** from `more_finds.json` → **309** total.
- Regenerated `lists/*.md`, `README.md` counts/badge, `docs/categories.md`.
- Did **not** overwrite `research/new_finds.json` (prior 255 merge).
- Did **not** git push.


## Web expansion 2026-09-14

- web_finds.json: 36 candidates
- merged new: 36
- skipped: 0
- catalog total: 345
- provenance: {'personal_community': 226, 'official': 39, 'academic_lab': 80}


## Web expansion 2026-09-14

- web_finds.json: 42 candidates
- merged new: 6
- skipped: 36
- catalog total: 351
- provenance: {'personal_community': 226, 'official': 44, 'academic_lab': 81}


## Web expansion 2026-09-14

- web_finds.json: 42 candidates
- merged new: 0
- skipped: 42
- catalog total: 351
- provenance: {'personal_community': 226, 'official': 44, 'academic_lab': 81}


## Web expansion 2026-09-14

- web_finds.json: 42 candidates
- merged new: 0
- skipped: 42
- catalog total: 351
- provenance: {'personal_community': 226, 'official': 44, 'academic_lab': 81}


## Routine expansion 2026-09-14

- routine_finds: 9
- merged new: 9
- skipped: []
- total: 431
- provenance: {'personal_community': 233, 'official': 109, 'academic_lab': 89}

## Routine pass 2026-09-16

- Catalog size before: **468**; after merge: **489** (+21)
- Finds file: `research/routine_finds_20260916.json`
- Method: `gh api search/repositories` across scintillation/ROTI/DCB-UPD-OSB/VMF-GPT/PWV/cycle-slip/multipath/FGO/ANTEX-SP3/RINEX4/RAIM/NTRIP/HAS-B2b/CLAS/GNSS-IR/CORS/POD niches; WebSearch for agency pages (BKG/TU Wien/GFZ already saturated); primary README via `gh api repos/.../readme`
- Dedup against live `PROJECTS.json` URLs; verified each keep with `gh api repos/{owner}/{repo}`
- Highlights added: RADIATE (TU Wien ray-tracing), mpsim/GIRAS/GMR-Water (GNSS-IR), Gkit-Bias/MCOSB/clkcomb (bias/OSB), autorino/rinexmod (IPGP RINEX ops), FE-GUT & GNSS/INS FGO comparisons, ROS NTRIP/RTKLIB bridges, RAIM_PANG_NAV, GPSL1-MMT-DPE
- Skipped: pure RTKLIB mirrors, Deep-Navigation/MRTKLIB mirror, thin PWV notebooks, already-cataloged BNC/GREAT-PVT/raPPPid/IonoMoni/OASIS/scintkit
