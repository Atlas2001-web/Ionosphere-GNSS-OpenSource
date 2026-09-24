# 软件操作手册索引

本目录共有 **67 篇**操作手册（合计 **15536 行**，`wc -l`，不含本索引）：命令、输入输出、坑、选型。不是教材正文。

概念课见 [`docs/tutorials/`](../tutorials/)。条目以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。

参数冲突时：**本机 `-h` / 上游 README > 本手册示例**。

---

## 并行写作状态（持续 QC 中）

| 角色 | 负责 | 勿抢 |
| --- | --- | --- |
| **软件手册质检**（本 bot） | 已短硬篇的**二遍质检补洞**（错 I/O、过时旗标、仍薄点）；优先 `georinex` / `rtklib` / `bnc` / `gfzrnx` / `pytecgg` | 勿大改「仍薄/缺篇」同事正在写的文件 |
| **软件用法讲解**（并行） | 写 **尚未短硬 / 缺篇** 新手册 | 勿重写下表已标「已短硬」全文（补丁可协调） |

**下一优先（质检二遍，按弱→强）：** **用法讲解新入库** `crx2rnx`（crates.io **2.7.0**/tip `765ddeb`；Rust 仅解压；ACOR C1C G07=23818653.24=GSI；AJAC V2 丢星 17≠26；同名≠hatanaka 捆版；交叉 rnxcmp/hatanaka/rinexmod/georinex）。 **用法讲解新入库** `navdecoder`+`gnss-multipath-analysis`（NavDecoder `7947333`：HAS 801×data collected + B2b SSR 532；gnssmultipath **2.2.0**/`806c3d9`：NMBUS C1C RMS≈1.273/wRMS≈1.093 周跳47）。前序  **用法讲解新入库** `gnss-downloader`（Mereithhh tip `e6d0d84`/V3.0；无下载 CLI；WHU 230+CWD、NLST 425；SIZE brdc=57792 / ABPO GN=29294；NASA 明文不可用→data-access Earthdata；交叉 gdds/gampii-good/fast）。 **用法讲解新入库** `DRCycleSlip`（tip `f57d74d`；三频组合注入–探测；BAKO G24 历元700→(23,18,17)；无 PyPI；硬编码 Windows 路径；交叉 cycle-slip-correction/georinex/anubis）。前序 **已质检复跑** `ismr-downloader`（0.2.0/`cca68e4`；缺参 exit 1；SSL + token **400**；登记门禁未落盘）。前序 **已质检复跑** `ntripstreams`+`gampii-good`（rtk2go STR765 / igs-ip STR384 / 订流 400；AgPartner_2 251；GOOD BRDC 11371068 B + atx skip）。前序 **已质检复跑** `claslib`+`b2blib`（dump 3601 / 3580 GGA；WUH2 9×Q=6）。前序 **用法讲解新入库** `ntripstreams`（0.3.5/`889ffb9`；NTRIP asyncio；rtk2go STR765 / igs-ip STR384；无订户订流 400；Rtcm3 样帧+AgPartner_2 251 帧；1029；交叉 pygnssutils/bkg-ntripcaster/bnc/pynmeagps/pyrtcm）。前序 **用法讲解新入库** `pyspartn`（1.1.0/`8fc58f8`；SPARTN 编解码；**无接收机/无 L-band**；传输层往返；OCB/GAD 样例解密；d9s 3007 帧；**无 CLI**→gnssstreamer；交叉 pyubx2/pynmeagps/pygpsclient/haslib/pyrtcm）。前序 **用法讲解新入库** `pyrtcm`（1.2.0/`5d66c7a`；RTCM3 编解码；README 1005 往返；RTCM3.log 11 帧；MSM `parse_msm`；**无 CLI**→gnssstreamer；交叉 pygnssutils/pyubx2/pynmeagps）。前序 **用法讲解新入库** `pyubx2`（1.3.6/`4abbfa6`；UBX 编解码；**无接收机**构造/样例；CFG-MSG/NAV-PVT/ACK 往返；上游 NAV 样例+mon_span 109 帧；**无 CLI**→gnssstreamer；交叉 pygnssutils/pygpsclient/pynmeagps/pyrtcm）。 停写门槛已近——剩余主要是 **登记/环境受限**（`anubis` / `ionomoni` / `iono-scintillation` / `gfzrnx`）无本机真实 I/O 可补；**sh-gim** 保持边界。**已质检复跑** `rinexmod`+`pyubx2`+`ionex-rs`+`madocalib`+`aacgmv2`+`gnsstk`+`teqc`+`pyrtcm` · **质检新短硬** `kamodo`（26.9.2；ΣH=9.1183）· **已短硬入库 `pyglow` + `iri2016` + `apexpy` + `msise00`**。**用法讲解已入库** `ionex-rs` + `madocalib` + `glab-upc` + `pynmeagps` + `gdds` + `gps-measurement-tools` + `pygpsclient`+ `cycle-slip-correction` + `diffionmap` + `cddis-highrate-downloader`。**已质检复跑** `glab-upc` + `pynmeagps` + `gdds` + `gps-measurement-tools` + `pygpsclient` + `gnss_lib_py` + `pyiri` + `pyirtam`+ `fast` + `diffionmap` + `cddis-highrate-downloader`（stdout 对齐；CDDIS LIST 425 已记）。**质检新短硬** `geospacelab`（0.14.8；OMNI SYM_H=-234 + Madrigal TEC max=114）。**用法讲解新入库** `gnsspy`（3.0.1；demo.10o→pandas G07 L1=118767195.326；converter 2→3；无 PyPI）。**已质检复跑** `gnsspy`（3.0.1/`e6879bf`；22×9/2×14；converter 2→3 OK；3→2 回写 Length mismatch 坑已补）。**用法讲解新入库** `gnsstools`（0.0.1/`e496093`；OBS/NAV/SP3 真 I/O；无 PyPI）。**用法讲解/原理课加厚入库** `aacgmv2`（2.7.1；mlat≈50.53 / mlon≈−4.09 / mlt≈10.09 @40N80W 250km）。**用法讲解新入库** `claslib` + `b2blib`（CLAS `1e3a75d`/0.8.4：dump header 3601 + test1 3580 GGA；B2b `fe7c4c0`：WUH2 5 min 9×Q=6）。**用法讲解新入库** `gnsstk` + `teqc`（库 15.3.1/`55ea334`；teqc 2019Feb25 +qc MP12≈0.20）。**用法讲解新入库** `rinexmod`（4.2.1；demo.10o→demo064a.10o MARKER MRKR→DEMO / AGENCY→IPGP；长名 DEMO00FRA…rnx.gz；hatanaka 时钟偏移坑已记）。
**sh-gim：** 保持短边界，禁止注水扩写。  
**停写条件：** 剩余皆 PASS，或仅剩 sh-gim 边界 / 登记受限且无进一步真实 I/O 增益。

---

## 全部手册 + 质检状态

| # | 手册 | 做什么 | 行数 | 状态 |
| ---: | --- | --- | ---: | --- |
| 1 | [georinex.md](./georinex.md) | RINEX → xarray / Python | 305 | **已短硬** R2+R7二遍 · 本机 1.16.2（补 NAV 实跑 I/O） |
| 2 | [gfzrnx.md](./gfzrnx.md) | RINEX 检查 / 拼接 / 抽稀 | 423 | **已短硬** R1+R8 guide [`099bf63`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/099bf63) · **登记受限**（无本机官方二进制；`-sifl` 坑已补；**禁臆造 stdout**） |
| 3 | [anubis.md](./anubis.md) | 观测 QC → XTR/XML | 239 | **已短硬** R6 [`8fe8b6d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/8fe8b6d) · **登记受限**（Free 需注册；无本机 Linux 二进制） |
| 4 | [pytecgg.md](./pytecgg.md) | 校准 sTEC/vTEC（作者 viventriglia） | 593 | **已短硬** R1+R8二遍 [`ff674b4`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/ff674b4) · 本机 1.3.0（ABMF 全日 `calculate_tec`/`veq` 实跑） |
| 5 | [ionomoni.md](./ionomoni.md) | STEC / ROTI / AATR（C++） | 219 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · **登记受限**（官方主推 Win；Linux 无开箱二进制） |
| 6 | [oasis-roti.md](./oasis-roti.md) | ROTI / ΔTEC / SIDX（Python） | 224 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · 本机 pyOASIS 1.0.3 |
| 7 | [ionex-gim.md](./ionex-gim.md) | 读 IONEX GIM | 200 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · 本机 ionex 0.2 |
| 8 | [sh-gim.md](./sh-gim.md) | 维护者球谐仓**边界**（求解器未开源） | 124 | **边界** · 保持短；禁止扩写成端到端求解教程 |
| 9 | [pygnssutils.md](./pygnssutils.md) | NTRIP CLI / 小 caster | 361 | **已短硬** R5 [`37ac39b`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/37ac39b) · 本机 1.2.7 |
| 10 | [bnc.md](./bnc.md) | BKG 多流客户端 | 274 | **已短硬** R2+R7二遍 · 本机 BNC 2.13.7（REQC 实跑 / NTRIP 标操作步骤） |
| 11 | [bkg-ntripcaster.md](./bkg-ntripcaster.md) | BKG Caster 播发 | 379 | **已短硬** R4 [`bfcd626`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/bfcd626) · 本机 2.0.49 |
| 12 | [rtklib.md](./rtklib.md) | RTK / PPP CLI | 287 | **已短硬** R1+R7二遍 · apt 2.4.3 b34 / EX 2.5.1（PATH 陷阱已写清） |
| 13 | [pride-pppar.md](./pride-pppar.md) | PPP-AR | 289 | **已短硬** R6 [`8fe8b6d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/8fe8b6d) · 本机 3.2.11（`-V`/`-H`/会话头实跑；WUM FTPS 未出解） |
| 14 | [cssrlib.md](./cssrlib.md) | Python PPP / PPP-RTK（CLAS/HAS/BDS） | 243 | **已短硬** R9二遍 · 本机 1.2.1（`nav.t` 坑已补；SPP 60 历元复跑；CLAS/HAS 未跑完） |
| 15 | [gnss-tec.md](./gnss-tec.md) | RINEX → 相对斜 TEC | 198 | **已短硬** R9二遍 · 本机 1.1.1（stdout 对齐脚本；type N NAV 坑） |
| 16 | [pinot.md](./pinot.md) | “not only TEQC” QC/预处理批壳 | 287 | **已短硬** R9二遍 · orderfile/sitecheck/metacheck/subnet/low2upper 复跑；qualitycheck 无 Linux teqc |
| 17 | [autorino.md](./autorino.md) | 厂商 RAW 拉取 → RINEX3/4 | 246 | **已短硬** R9二遍 · 本机 2.4.2 cfgfile_check 复跑；check_rnx `figure_saver` 实错已记；convert 环境受限 |
| 18 | [iono-scintillation.md](./iono-scintillation.md) | MATLAB 闪烁仿真 | 197 | **已短硬** R2 [`246103d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/246103d) · **环境受限**（质检机无 MATLAB；不臆造控制台） |
| 19 | [rnxcmp.md](./rnxcmp.md) | GSI 官方 Hatanaka CRX 压缩/恢复 | 200 | **已短硬** R10质检 · 本机 RNXCMP **4.2.0** 复跑（body 相等；gzip≈1830；`-h` exit 1）；Python 见 [hatanaka](./hatanaka.md) |
| 20 | [hatanaka.md](./hatanaka.md) | Python Hatanaka CRX↔RNX（pip） | 251 | **已短硬** · 本机 hatanaka **2.8.1** / 捆 RNXCMP 4.1.0；`rinex-decompress`/`compress`+georinex 实跑；官方二进制 → [rnxcmp](./rnxcmp.md) |
| 21 | [nequickg.md](./nequickg.md) | Galileo NeQuick-G（Python 社区） | 203 | **已短硬** R10质检 · Py3 移植后 vTEC+Medium 行0/全表36 复跑；`Validation.py` map/plt 坑已补；官方 C 登记受限 |
| 22 | [haslib.md](./haslib.md) | Galileo HAS 解码（SBF/BINEX→SSR） | 170 | **已短硬** R11质检 · 本机 `galileo_has_decoder` **1.0.2**；`-x 3000 -v 1` → 11 HAS；RTCM 9780 / IGS 9800；`-m`/`-h` 坑已补 |
| 23 | [laika.md](./laika.md) | comma.ai 轻量 Python GNSS | 194 | **已短硬** R11质检 · 本机 0.0.1；`slac1700.18o` 2880 历元+PDOP 3.298… 复跑；pytest 17；Earthdata 未跑 |
| 24 | [android_rinex.md](./android_rinex.md) | GnssLogger / 手机原始测量 → RINEX3 | 220 | **已短硬** · 本机 clone `8ea7ab7`；样例 → `nex9_lab.17o` 1379 历元；georinex 1.16.2 探活 |
| 25 | [cosmic-crunch.md](./cosmic-crunch.md) | JPL GENESIS COSMIC-1 大气 L2 ASCII→netCDF4 | 222 | **已短硬** · 本机 2.1.2；`get --test` 10×`.L2.txt.gz` + convert/`--netcdf4` 10×`.nc`；非 CDAAC ionPrf |
| 26 | [pyglow.md](./pyglow.md) | 上层大气气候态（IRI/HWM/IGRF） | 204 | **已短硬** · 本机 tip 1988757 / Py3.8；IRI-2016 ne(250km)=854889；缺 igrf2015 静默退出坑已记 |
| 27 | [iri2016.md](./iri2016.md) | IRI-2016 官方 Fortran→xarray | 170 | **已短硬** · 本机 1.12.0/`ca523ad` / Py3.11；ne@250km=8.55e11 m⁻³；与 pyglow cm⁻³ 对照 |
| 28 | [gnss_lib_py.md](./gnss_lib_py.md) | Stanford NAV Lab：观测/导航 → NavData / WLS | 200 | **已短硬** · 本机 gnss-lib-py **1.1.0**；混合 OBS→126 测值/5 历元；AndroidDerived2023 冒烟 |
| 29 | [pyiri.md](./pyiri.md) | 纯 Python IRI（无 Fortran 绑定） | 182 | **已短硬** · 本机 PyIRI **0.1.7**；单点 2020-04-01 NmF2/vTEC 实跑；对照 pyglow/iri2016 |
| 30 | [awsgnssroutils.md](./awsgnssroutils.md) | AWS Open Data GNSS-RO 查询/下载（calibratedPhase 等） | 245 | **已短硬** · 本机 1.2.7；cosmic1 Phase 2636→3 文件；cosmic2 仅 atm 对照；开放 S3 / rotcol 门禁 |
| 31 | [pyirtam.md](./pyirtam.md) | 纯 Python IRTAM 系数→网格 Ne（对接 PyIRI） | 177 | **已短硬** · 本机 PyIRTAM **0.0.7**；LGDC 2024-06-01 02:15 四系数 + run_PyIRTAM 实跑 |
| 32 | [fast.md](./fast.md) | GNSS 下载 / QC / 广播星历 SPP / 选站 | 215 | **已短硬** · 本机 tip **3.01.01**；ABPO satNum + 1h SPP Δ≈0.69 m；FTP 下载本机失败已记 |
| 33 | [apexpy.md](./apexpy.md) | Apex / 准偶极磁坐标（Apex/QD/MLT） | 174 | **已短硬** · 本机 2.1.1/`eed96cf`；geo2apex(40N,80W,250km)→alat≈50.70；CLI 14 位时间坑 |
| 34 | [msise00.md](./msise00.md) | NRLMSISE-00 中性大气 → xarray | 166 | **已短硬** · 本机 **1.11.1**/`e4ab457`；Tn@250km=1009.87 K；CLI `-w` 需 netCDF4 |
| 35 | [pysatcdaac.md](./pysatcdaac.md) | pysat 生态 CDAAC/COSMIC（ionPrf/ionPhs） | 293 | **已短硬** · 本机 0.0.5；ionprf 2019-01-01 59→53；ionphs 下 144、load 维冲突改 netCDF4 |
| 36 | [diffionmap.md](./diffionmap.md) | 两幅 IONEX 并排对照（VS 图） | 179 | **已短硬** · tip `57ceb1d`；Py3 读 CODG/WHUC 12 图 mean≈24.84；IGRG mean≈13.367；Basemap 出图环境受限 · **质检复跑通过** |
| 37 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) | CDDIS 高采样 15 min 块批量下载 | 179 | **已短硬** · 本机 1.0.2；FTPS 登录+CWD+SIZE 706256；LIST/RETR 425 受限；Linux 无 CRX2RNX · **质检复跑通过** |
| 38 | [cycle-slip-correction.md](./cycle-slip-correction.md) | 周跳探测改正 CLI（EMBRACE/INPE） | 183 | **已短硬** · tip `c465dd4`；无 PyPI；现代钉+BAKO 3.03 40 历元；不写回 RINEX |
| 39 | [gps-measurement-tools.md](./gps-measurement-tools.md) | Google GNSS Logger + MATLAB 伪距/WLS | 203 | **已短硬** · tip `ab1aebb`；demo→android_rinex→georinex 223 历元；MATLAB 环境受限 · **质检复跑通过** |
| 40 | [pygpsclient.md](./pygpsclient.md) | NMEA/UBX/RTCM/NTRIP 桌面 GUI | 224 | **已短硬** · 本机 **1.7.6**/`69b84cf`；pyrinexconv O1677/N55037；无 tkinter GUI 受限 · **质检复跑通过** |
| 41 | [gdds.md](./gdds.md) | IGS/CORS/产品/时序多模块 GUI 下载 | 242 | **已短硬** · tip `2a8543c`；无 CLI；NOAA/ITRF 实拉；WHU CWD 通、NLST 时好时坏（写作 425/质检成功）；CDDIS 401；Earthdata 硬编码须自换 · **质检复跑通过** |
| 42 | [geospacelab.md](./geospacelab.md) | 日地数据管理/可视化（OMNI·指数·TEC map） | 256 | **已短硬** · 本机 **0.14.8**；OMNI SYM_H min=-234；Madrigal TEC 13×180×360 @06:30 max=114；需 cartopy+config |
| 43 | [glab-upc.md](./glab-upc.md) | UPC gAGE 教学 GNSS（SPP/PPP/电离层模型） | 202 | **已短硬** · 官方 v6.0.0 `gLAB_linux`；abmf SPP 2880 历元 3D95≈4.75 m；旧 4.x gcc 链失败已记 · **质检复跑通过** |
| 44 | [pynmeagps.md](./pynmeagps.md) | NMEA 0183 编解码库 | 213 | **已短硬** · 本机 **1.1.7**/`4322c38`；GGA 往返+文件流；交叉 [pygpsclient](./pygpsclient.md)/[pygnssutils](./pygnssutils.md) · **质检复跑通过** |
| 45 | [gnsspy.md](./gnsspy.md) | Python GNSS 读写/分析（pandas + RINEX 2↔3） | 228 | **已短硬** · 本机 **3.0.1**/`e6879bf`；质检复跑 demo.10o→22×9/2历元/14SV G07 L1=118767195.326；converter 2→3 OK（XYZ Y/Z=0；3→2 回写 `read_obsFile` Length mismatch）；**无 PyPI**；对照 [georinex](./georinex.md) · **质检复跑通过** |
| 46 | [ionex-rs.md](./ionex-rs.md) | Rust IONEX 解析/写回（nav-solutions） | 170 | **已短硬** · tip `bcb9171`；CKMG 129575/9.2 TECU/807703 B · **质检复跑通过** |
| 47 | [madocalib.md](./madocalib.md) | QZSS MADOCA-PPP 官方测试库（事后 PPP） | 165 | **已短硬** · VER **2.1**/`0089f7d`；MIZU 118×Q=6 · **质检复跑通过** |
| 48 | [aacgmv2.md](./aacgmv2.md) | AACGM-v2 地磁坐标（mlat/mlon/MLT） | 209 | **已短硬** · **2.7.1**/`5f85579`；mlat≈50.53 · **质检复跑通过** |
| 49 | [gnsstools.md](./gnsstools.md) | 轻量 Python：RINEX/SP3 → pandas / 轨道壳 | 253 | **已短硬** · tip **`e496093`** / **0.0.1**；OBS E7 C1=28344990.66=georinex；SP3 G01 xyz km；**无 PyPI**；对照 [georinex](./georinex.md)/[gnsspy](./gnsspy.md) |
| 50 | [rinexmod.md](./rinexmod.md) | RINEX 头/元数据修改与长短名规范化 | 241 | **已短硬** · **4.2.1**；demo→demo064a.10o MARKER/AGENCY/REC/ANT；长名+gz · **质检复跑通过** |
| 51 | [pyubx2.md](./pyubx2.md) | u-blox UBX 编解码库 | 244 | **已短硬** · **1.3.6**/`4abbfa6`；CFG-MSG/NAV-PVT/ACK 往返；NAV-PVT 53.4507228；mon_span 109 · **质检复跑通过** |
| 53 | [kamodo.md](./kamodo.md) | NASA CCMC 模式输出函数化（SWMF_IE/IRI/GITM…） | 166 | **已短硬** · **kamodo-ccmc 26.9.2**/core **26.8.7**；SWMF_IE Σ_H(12h,0E,70N)=**9.1183** S；phi=−1.7879 kV |
| 52 | [pyrtcm.md](./pyrtcm.md) | RTCM3 编解码库（含 MSM） | 286 | **已短硬** · **1.2.0**/`5d66c7a`；1005 往返；RTCM3.log 11 帧；MSM3 `parse_msm` · **质检复跑通过** |
| 54 | [gnsstk.md](./gnsstk.md) | C++ GNSS 基础库（原 GPSTk）+ apps CLI | 208 | **已短硬** · 库 **15.3.1**/`55ea334` + apps **15.1.1**/`1aeb7d2`；`RinSum` BAHR 120 历元；`timeconvert` week 2437 · **质检复跑通过** |
| 55 | [teqc.md](./teqc.md) | 经典 Translate/Edit/QC（**EOL 2019Feb25**） | 197 | **已短硬** · 静态 `teqc`；demo.18o `+qc` 3 历元 MP12≈0.20 · **质检复跑通过**；后继 [gfzrnx](./gfzrnx.md)/[anubis](./anubis.md)/[rnxcmp](./rnxcmp.md) |
| 56 | [pyspartn.md](./pyspartn.md) | SPARTN 精密改正电文编解码 | 322 | **已短硬** · 本机 **1.1.0**/`8fc58f8`；**无接收机/无 L-band**；传输层 OCB-GPS 往返；GAD nSF=228；d9s 3007 帧；**无 CLI**→[pygnssutils](./pygnssutils.md)；交叉 [pyubx2](./pyubx2.md)/[pynmeagps](./pynmeagps.md)/[pygpsclient](./pygpsclient.md)/[haslib](./haslib.md)/[pyrtcm](./pyrtcm.md) |
| 57 | [gampii-good.md](./gampii-good.md) | GAMP II 配套：GNSS 观测/产品 YAML 下载器（GOOD） | 244 | **已短硬** · tip **`479aa14`** / v3.1；CMake 实编；WHU BRDC mixed3 11 371 068 B + igs14/igs20.atx；无参 Usage exit 255 · **质检复跑通过**（2026-09-24 04:59 EDT） |
| 58 | [ntripstreams.md](./ntripstreams.md) | NTRIP 协议通信（asyncio + RTCM3 帧） | 286 | **已短硬** · 本机 **0.3.5**/`889ffb9`；rtk2go STR**765**/igs-ip STR**384** sourcetable；无订户订流 HTTP 400；`Rtcm3` aamakinen 1005/1077 CRC + AgPartner_2 **251** 帧；1029 编码；交叉 [pygnssutils](./pygnssutils.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[bnc](./bnc.md)/[pynmeagps](./pynmeagps.md)/[pyrtcm](./pyrtcm.md) · **质检复跑通过**（2026-09-24 04:59 EDT；坑 #13 `head` BrokenPipe） |
| 59 | [claslib.md](./claslib.md) | QZSS CLAS Compact SSR→OSR/VRS/PPP-RTK | 182 | **已短硬** · tip **`1e3a75d`**/084/0.8.4；dump header **3601**；test1 **3580** GGA ≈36.1036°N 140.0863°E · **质检复跑通过** |
| 60 | [b2blib.md](./b2blib.md) | 北斗 PPP-B2b C/C++ 解码（嵌 RTKLIB） | 188 | **已短硬** · tip **`fe7c4c0`**；WUH2 5 min **9**×Q=6；首/末 ECEF 对齐 · **质检复跑通过** |
| 61 | [ismr-downloader.md](./ismr-downloader.md) | ISMR Query Tool API 闪烁监测数据 CLI 下载 | 226 | **已短硬** · 本机 **0.2.0**/`cca68e4`；`--help`；假账号 token 400；SSL 需 `--insecure`；**登记门禁未落盘**（交叉 [data-access](../data-access.md)） · **质检复跑通过**（2026-09-24 05:03 EDT） |
| 62 | [drcycleslip.md](./drcycleslip.md) | 三频周跳探测/修复教学（DRCycleSlip） | 197 | **已短硬** · tip **`f57d74d`**；无 PyPI；`search`/`find` + BAKO G24 注入历元 **700→(23,18,17)**；对照 [cycle-slip-correction](./cycle-slip-correction.md)/[georinex](./georinex.md)/[anubis](./anubis.md) |
| 63 | [gnss-downloader.md](./gnss-downloader.md) | PyQt5 NASA/WHU FTP 日采样 GNSS 下载 | 233 | **已短硬** · tip **`e6d0d84`**/V3.0；无下载 CLI；WHU SIZE brdc **57792**；NLST 425；NASA 明文失效→[data-access](../data-access.md) |
| 64 | [navdecoder.md](./navdecoder.md) | PPP-B2b + Galileo HAS 电文解码（Sept/Unicore） | 184 | **已短硬** · tip **`7947333`**；HAS 截短 **801**×data collected + log 轨道表；B2b **`.ssr` 532**；交叉 [b2blib](./b2blib.md)/[haslib](./haslib.md)/[cssrlib](./cssrlib.md)/[madocalib](./madocalib.md) |
| 65 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) | 观测多路径/周跳/SNR 分析（gnssmultipath） | 161 | **已短硬** · PyPI **2.2.0**/tip **`806c3d9`**；NMBUS C1C RMS≈**1.273**/wRMS≈**1.093**；周跳 **47**；交叉 [georinex](./georinex.md)/[gfzrnx](./gfzrnx.md)/[teqc](./teqc.md)/[rtklib](./rtklib.md) |
| 66 | [crx2rnx.md](./crx2rnx.md) | Rust Hatanaka CRX→RNX 解压 CLI（nav-solutions） | 238 | **已短硬** · crates.io **2.7.0**/tip **`765ddeb`**；ACOR C1C=GSI；AJAC V2 丢星；同名≠[hatanaka](./hatanaka.md) 捆版；交叉 [rnxcmp](./rnxcmp.md)/[rinexmod](./rinexmod.md)/[georinex](./georinex.md) |
| 67 | [sbfparser.md](./sbfparser.md) | Septentrio SBF 官方 Cython 解析（sbf-parser） | 252 | **已短硬** · PyPI **1.0.3**/tip **`ea84256`**；receiver_status TOW=**49638143**；log_0000 **748**/49；ExtEvent 往返；HAS样例 GALRawCNAV=**11774**；无 ISM/4086；交叉 [haslib](./haslib.md)/[ismr-downloader](./ismr-downloader.md)/[pyubx2](./pyubx2.md) |

**状态图例：** `已短硬` = Round 已按 short-hard 改过且可作二遍质检；`登记受限` / `环境受限` = 无本机官方二进制或运行时，命令以官方/仓内为准、**禁止伪造 stdout**；`边界` = sh-gim 专有求解器未开源；`仍薄` = 尚无短硬或明显缺真实 I/O（当前 **0 篇**——新缺篇由「软件用法讲解」认领后改此表）。

每篇结构：**用途边界 → 安装 → 逐步命令+期望输出 → I/O 字段 → 参数 → 接到哪步 → ≥8 坑 → 选型**。

---

## 30 秒选型

| 你要… | 打开 |
| --- | --- |
| 读 RINEX 进 Python | [georinex.md](./georinex.md) |
| RINEX → pandas / 2↔3 转换（教学） | [gnsspy.md](./gnsspy.md) |
| 轻量 RINEX/SP3 → pandas（教学；无 PyPI） | [gnsstools.md](./gnsstools.md) |
| C++ GNSS 时间/RINEX 库 + RinSum | [gnsstk.md](./gnsstk.md) |
| 经典 TEQC 翻译/编辑/QC（EOL） | [teqc.md](./teqc.md) |
| 分信号码多路径 + 周跳报告 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) |
| 改/拼/抽稀 RINEX | [gfzrnx.md](./gfzrnx.md) |
| 观测 QC 报告 | [anubis.md](./anubis.md) |
| 周跳探测改正试验（RINEX 3.01–3.03） | [cycle-slip-correction.md](./cycle-slip-correction.md) |
| 三频周跳注入–探测教学（Python） | [drcycleslip.md](./drcycleslip.md) |
| 旧 CORS 缺站/日目录/TEQC 批壳 | [pinot.md](./pinot.md) |
| GNSS 产品下载 + 观测 QC + 粗 SPP | [fast.md](./fast.md) |
| 厂商 RAW→RINEX3/4 台网入库 | [autorino.md](./autorino.md) |
| 批量改 RINEX 头 / 长短名 / 压缩约定 | [rinexmod.md](./rinexmod.md) |
| Hatanaka `.crx` 官方压缩/恢复 | [rnxcmp.md](./rnxcmp.md) |
| Python 解 `.crx` / 脚本压缩（pip） | [hatanaka.md](./hatanaka.md)（官方 → [rnxcmp](./rnxcmp.md)） |
| Rust CLI 仅解压 `.crx`/`.crx.gz`（非 GSI 同名） | [crx2rnx.md](./crx2rnx.md) |
| Galileo NeQuick-G 模型（脚本） | [nequickg.md](./nequickg.md) |
| IRI-2012/2016 气候态（Python 包装） | [pyglow.md](./pyglow.md) |
| IRI-2016 官方驱动 → xarray | [iri2016.md](./iri2016.md) |
| 纯 Python IRI（无 Fortran） | [pyiri.md](./pyiri.md) |
| IRTAM 同化系数→网格 Ne（纯 Python） | [pyirtam.md](./pyirtam.md) |
| AACGM-v2 磁坐标 / MLT | [aacgmv2.md](./aacgmv2.md) |
| CCMC 模式输出函数化 / 飞越 | [kamodo.md](./kamodo.md) |
| Apex / QD / MLT 磁坐标 | [apexpy.md](./apexpy.md) |
| NRLMSISE-00 中性大气 | [msise00.md](./msise00.md) |
| Android/多源 GNSS → NavData / 教学 WLS | [gnss_lib_py.md](./gnss_lib_py.md) |
| 校准 sTEC/vTEC | [pytecgg.md](./pytecgg.md) |
| 粗相对斜 TEC（无 DCB） | [gnss-tec.md](./gnss-tec.md) |
| ROTI / AATR / ΔTEC | [ionomoni.md](./ionomoni.md) · [oasis-roti.md](./oasis-roti.md) |
| 读 IONEX GIM | [ionex-gim.md](./ionex-gim.md) |
| Rust 读/写 IONEX | [ionex-rs.md](./ionex-rs.md) |
| 两幅 IONEX 并排对照 | [diffionmap.md](./diffionmap.md) |
| CDDIS 高采样（1 s / 15 min）批量 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) |
| IGS/CORS/产品/时序 GUI 多模块下载 | [gdds.md](./gdds.md) |
| 轻量 PyQt 点选 WHU/NASA 日文件（2020） | [gnss-downloader.md](./gnss-downloader.md) |
| GAMP/PPP YAML 批下载观测+产品（GOOD） | [gampii-good.md](./gampii-good.md) |
| 球谐 GIM 边界说明 | [sh-gim.md](./sh-gim.md) |
| NTRIP 脚本拉流 / 小 caster | [pygnssutils.md](./pygnssutils.md) |
| asyncio NTRIP 握手 / 轻量 RTCM 帧 | [ntripstreams.md](./ntripstreams.md) |
| 多流 GUI / 录盘 | [bnc.md](./bnc.md) |
| 自建多用户 Caster | [bkg-ntripcaster.md](./bkg-ntripcaster.md) |
| RTK / 浮点 PPP | [rtklib.md](./rtklib.md) |
| PPP-AR | [pride-pppar.md](./pride-pppar.md) |
| QZSS MADOCA-PPP 官方参考 | [madocalib.md](./madocalib.md) |
| QZSS CLAS Compact SSR→OSR/VRS/PPP-RTK | [claslib.md](./claslib.md) |
| 北斗 PPP-B2b（嵌 RTKLIB） | [b2blib.md](./b2blib.md) |
| Sept/Unicore 流 → B2b/HAS 日志+SSR/SP3 | [navdecoder.md](./navdecoder.md) |
| Python 开放 PPP/PPP-RTK（CLAS/HAS） | [cssrlib.md](./cssrlib.md) |
| Galileo HAS 页 → RTCM/IGS SSR | [haslib.md](./haslib.md) |
| 码多路径 / 周跳报告与出图 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) |
| 轻量 Python 观测处理 / 自写估计器 | [laika.md](./laika.md) |
| 手机 GnssLogger → RINEX | [android_rinex.md](./android_rinex.md) |
| Google Logger 套件 / 手机原始测量规范 | [gps-measurement-tools.md](./gps-measurement-tools.md) |
| 板卡 GUI 联调 / NTRIP（tkinter） | [pygpsclient.md](./pygpsclient.md) |
| 教学 SPP/PPP / 误差项拆解（UPC gLAB） | [glab-upc.md](./glab-upc.md) |
| NMEA 0183 编解码（Python） | [pynmeagps.md](./pynmeagps.md) |
| u-blox UBX 编解码（Python） | [pyubx2.md](./pyubx2.md) |
| RTCM3 编解码（Python，含 MSM） | [pyrtcm.md](./pyrtcm.md) |
| SPARTN 编解码（Python；PPP-RTK 改正） | [pyspartn.md](./pyspartn.md) |
| 空间天气多源拉取/作图（OMNI·TEC map） | [geospacelab.md](./geospacelab.md) |
| GENESIS COSMIC-1 **大气** L2→netCDF（非 ionPrf） | [cosmic-crunch.md](./cosmic-crunch.md) |
| AWS GNSS-RO 查/下（**calibratedPhase** / 大气三型） | [awsgnssroutils.md](./awsgnssroutils.md) |
| CDAAC **ionPrf / ionPhs**（pysat） | [pysatcdaac.md](./pysatcdaac.md) |
| 闪烁 ISMR（UNESP API 批量） | [ismr-downloader.md](./ismr-downloader.md) |
| Septentrio SBF 块解析（官方 Cython） | [sbfparser.md](./sbfparser.md) |
| 闪烁仿真（MATLAB） | [iono-scintillation.md](./iono-scintillation.md) |

---

## 工作流路径 A–E

### A · 一日 TEC

[data-access](../data-access.md) →（可选 [gampii-good](./gampii-good.md) / [fast](./fast.md) / [gdds](./gdds.md) / [gnss-downloader](./gnss-downloader.md) 下载·QC / [autorino](./autorino.md) 入库 / [rinexmod](./rinexmod.md) 改头 / [android_rinex](./android_rinex.md) 手机日志 / [pinot](./pinot.md) 旧批壳）→（可选 [gnsspy](./gnsspy.md) 2↔3）→ [georinex](./georinex.md) →（可选 [cycle-slip-correction](./cycle-slip-correction.md)/[drcycleslip](./drcycleslip.md) 周跳试验）→（可选 [gnss-multipath-analysis](./gnss-multipath-analysis.md) 多路径）→（可选 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)/[gnss-tec](./gnss-tec.md) 粗相对 TEC）→ [pytecgg](./pytecgg.md) → [ionex-gim](./ionex-gim.md) 对照 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[09](../tutorials/09-dcb-biases-deep.md)/[16](../tutorials/16-practice-one-day-tec.md)

### B · 不规则体 / 磁暴

ISMR 备数（可选 [ismr-downloader](./ismr-downloader.md)）· SBF 块解析（可选 [sbfparser](./sbfparser.md)）· 高采样（可选 [cddis-highrate-downloader](./cddis-highrate-downloader.md)）→ RINEX → [ionomoni](./ionomoni.md) 或 [oasis-roti](./oasis-roti.md)；暴时指数/TEC 产品图可选 [geospacelab](./geospacelab.md) → 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)/[21](../tutorials/21-equatorial-anomaly-bubbles.md)；高 ROTI 时段对照 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md) 固定率；仿真概念见 [iono-scintillation](./iono-scintillation.md)·[13](../tutorials/13-scintillation-modeling.md)

### C · 实时差分 / 实验室 CORS

[pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md) / [pyrtcm](./pyrtcm.md) / [pyspartn](./pyspartn.md) / [pyubx2](./pyubx2.md) / [pynmeagps](./pynmeagps.md) / [pygpsclient](./pygpsclient.md) 或 [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)；落盘后再走 A/B；手机 Logger 见 [gps-measurement-tools](./gps-measurement-tools.md)+[android_rinex](./android_rinex.md)

### D · 发表级坐标 / ZTD

QC（[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [rtklib](./rtklib.md) 冒烟 →（开放服务教学 [cssrlib](./cssrlib.md)；QZSS CLAS [claslib](./claslib.md)；QZSS MADOCA [madocalib](./madocalib.md)；B2b [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md)）→ [pride-pppar](./pride-pppar.md) + 精密产品 → 教程 [06](../tutorials/06-iono-positioning.md)

### E · 理解 GIM（非端到端自建）

[ionex-gim](./ionex-gim.md) 读产品（Rust → [ionex-rs](./ionex-rs.md)）；[diffionmap](./diffionmap.md) 两图并排；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表里其它 GIM 工具 → 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 事实边界（归属说明，不是目录）

下面两行**不是**「只有这两个软件」，只是容易写错归属的提醒：

| 项目 | 关系 |
| --- | --- |
| [PyTECGg](./pytecgg.md) | 作者 **viventriglia**（不是本仓维护者自有） |
| [SH-GIM](./sh-gim.md) | 本仓维护者自有；**球谐求解器未开源** |
| 本目录其它手册 | 操作说明；许可与 EULA 以上游为准 |

---

最近新增（用法讲解）：**sbfparser**（1.0.3/`ea84256`；receiver_status TOW 49638143；log 748/49；ExtEvent 往返；HAS GALRawCNAV 11774；tip 无 ISM 块；交叉 haslib/ismr-downloader/pyubx2；下一优先 pysbf2）。最近新增（用法讲解）：**crx2rnx**（2.7.0/`765ddeb`；Rust CRX→RNX；ACOR C1C G07=23818653.24=GSI；AJAC V2 17≠26 SV；PATH 同名陷阱；交叉 rnxcmp/hatanaka/rinexmod/georinex）。最近新增（用法讲解）：**navdecoder**（`7947333`；HAS 截短 801×data collected + B2b SSR 532；交叉 b2blib/haslib/cssrlib/madocalib）+ **gnss-multipath-analysis**（2.2.0/`806c3d9`；NMBUS C1C RMS≈1.273/wRMS≈1.093 周跳47；交叉 georinex/gfzrnx/teqc/rtklib）。最近新增（质检）：**ismr-downloader 质检复跑通过**（缺参 exit 1；SSL；token 400；tip `cca68e4`）。最近新增（质检）：**ntripstreams/gampii-good 质检复跑通过**（rtk2go 767/STR765；igs-ip 391/STR384；订流 400；AgPartner_2 251；GOOD BRDC 11371068 B + igs14/20.atx skip）。最近新增（用法讲解）：**gnss-downloader**（`e6d0d84`/V3.0；无下载 CLI；WHU SIZE 57792；NLST 425；NASA 明文失效；交叉 gdds/gampii-good/fast/data-access）。最近新增（用法讲解）：**DRCycleSlip**（tip `f57d74d`；无 PyPI；search/find 组合；BAKO G24 注入 700→(23,18,17) deltaN≈-1.23/1.13/-1.10；硬编码 Windows 路径坑；对照 cycle-slip-correction/georinex/anubis）。最近新增（用法讲解）：**ismr-downloader**（0.2.0/`cca68e4`；API token 400 探针；SSL+注册门禁；交叉 data-access ISMR）。最近新增（质检）：**claslib/b2blib 质检复跑通过**（CLAS dump header 3601 + test1 3580 GGA；B2b WUH2 9×Q=6 首末 ECEF 对齐；tow 漂移坑已补）。最近新增（用法讲解）：**claslib**（`1e3a75d`/0.8.4；ssr2osr dump header 3601 + test1 3580 GGA ≈36.1036N 140.0863E；交叉 cssrlib/madocalib/rtklib）+ **b2blib**（`fe7c4c0`；WUH2 5 min 9×Q=6；Linux makefile+硬编码路径坑；交叉 haslib/cssrlib/claslib/madocalib/rtklib）。最近新增（用法讲解）：**ntripstreams**（0.3.5/`889ffb9`；rtk2go STR765 / igs-ip STR384；无订户 400；AgPartner_2 251 帧；1029；交叉 pygnssutils/bkg-ntripcaster/bnc/pynmeagps/pyrtcm）。最近新增（用法讲解）：**gampii-good**（tip `479aa14`/v3.1；CMake `run_GOOD`；WHU BRDC `BRDC00IGS_R_20240010000_01D_MN.rnx` 11371068 B + `igs14.atx`/`igs20.atx`；无参 Usage exit 255；对照 gdds/fast/data-access）。最近新增（用法讲解）：**pyspartn**（1.1.0/`8fc58f8`；SPARTN 传输层往返；GAD SF005=152 nSF=228；d9s 3007=OCB1692+HPAC1127+GAD188；无接收机/无 L-band；无 CLI→gnssstreamer；交叉 pyubx2/pynmeagps/pygpsclient/haslib/pyrtcm）。最近新增（质检）：**gnsstk/teqc/pyrtcm 质检复跑通过**（BAHR 120；teqc MP12≈0.20 EOL 边界确认；RTCM 1005/11 帧/MSM3）。最近新增（质检）：**rinexmod/pyubx2/ionex-rs/madocalib/aacgmv2 质检复跑通过** + **kamodo 短硬入库**（ccmc 26.9.2；SWMF_IE ΣH=9.1183；demo064a；UBX NAV-PVT 53.4507228）。最近新增（用法讲解）：**pyrtcm**（1.2.0/`5d66c7a`；1005 往返 llh≈32.07N 34.77E；RTCM3.log 11 帧；MSM `parse_msm` 8×20；无 CLI→gnssstreamer；交叉 pygnssutils/pyubx2/pynmeagps）。最近新增（用法讲解）：**gnsstk**（库 15.3.1/`55ea334`+apps `1aeb7d2`；BAHR RinSum 120 历元）+ **teqc**（2019Feb25；demo.18o +qc MP12≈0.20；EOL→gfzrnx/anubis/rnxcmp）。最近新增（用法讲解）：**pyubx2**（1.3.6/`4abbfa6`；UBX SET/POLL/ACK 往返；NAV-PVT 53.4507228；mon_span 109；无 CLI→gnssstreamer）。最近新增（用法讲解）：**rinexmod**（4.2.1；demo.10o→demo064a.10o MARKER MRKR→DEMO / AGENCY IPGP / REC TRIMBLE NETR9；长名 DEMO00FRA…rnx.gz；默认 Hatanaka 样例时钟偏移坑；交叉 georinex/autorino/hatanaka）。最近新增（用法讲解）：**gnsstools**（0.0.1/`e496093`；OBS E7 C1=28344990.66=georinex；NAV select G02；SP3 G01；**无 PyPI**/无 setup.py）。最近新增（用法讲解）：**aacgmv2**（2.7.1/`5f85579`；mlat≈50.53/mlon≈−4.09/mlt≈10.09；需 python3-dev；交叉 apexpy）。最近新增（质检）：**gnsspy 质检复跑通过**（3.0.1/`e6879bf`；demo.10o→22×9/2历元/14SV；G07 L1=118767195.326=georinex；converter 2→3 OK / XYZ Y/Z=0；3→2 回写 `read_obsFile` Length mismatch；无 PyPI；`.crx`→first-line ValueError）。最近新增（用法讲解）：**gnsspy**（3.0.1/`e6879bf`；demo.10o pandas 22×9；G07 L1=C georinex；converter 2→3；无 PyPI；`.gz` 读坑）。最近新增（质检）：**glab-upc/pynmeagps/gdds 质检复跑通过**（gLAB 2880/3D95=4.75；pynmea *5D；GDDS WHU NLST 时好时坏）+ **geospacelab**（0.14.8；OMNI/WDC/GFZ + Madrigal TEC；SYM_H=-234；TEC@06:30 max=114）+ **gps-measurement-tools/pygpsclient 质检复跑通过**。最近新增（用法讲解）：**ionex-rs**（crates.io 0.1.0/`bcb9171`；CKMG 129575 点/9.2 TECU/往返）+ **madocalib**（VER 2.1/`0089f7d`；MIZU 118 历元 Q=6）+ **glab-upc**（官方 v6.0.0；abmf SPP 2880 历元 3D95≈4.75 m）+ **pynmeagps**（1.1.7/；GGA 往返）+ **gdds**（`2a8543c`；无 CLI；NOAA brdc/p041+ITRF PSD；WHU FTP 425；CDDIS 401；Earthdata 硬编码）+ **gps-measurement-tools**（`ab1aebb`；demo→android_rinex 223 历元/L1C 全 0；相位样例 nonzero）+ **pygpsclient**（1.7.6；pyrinexconv O1677/N55037；无 tkinter）+ **cycle-slip-correction**（`c465dd4`；无 PyPI；BAKO 3.03 40 历元+PDF；官方 2019 pin 失败改现代钉）+ **diffionmap**（`57ceb1d`；CODG/WHUC 读路径+IGRG mean；Basemap 受限）+ **cddis-highrate-downloader**（1.0.2；FTPS SIZE 706256；RETR 425）+ **msise00**（1.11.1；Tn@250km）+ **pysatCDAAC**（0.0.5；ionprf 59→53；ionphs 144 下、load 维冲突）+ **pyirtam**（0.0.7；LGDC 四系数+IRI/IRTAM NmF2/vTEC）+ **fast**（3.01.01；ABPO satNum+1h SPP；FTP 下载失败记坑）+ **awsgnssroutils**（1.2.7；Phase 3 文件+atm 对照；S3 开放/rotcol 门禁）+ **gnss_lib_py**（1.1.0 NavData/OBS）+ **pyiri**（0.1.7 单点 NmF2/vTEC）。最近新增（质检）：**iri2016**（1.12.0；xarray 剖面+foF2/TEC；与 pyglow 同点对照）+ **pyglow**（Py3.8/`1988757`；IRI-2016/2012 剖面+IGRF/HWM14 实跑；`igrf2015` 静默退出坑）。最近新增（用法讲解）：**cosmic-crunch**（2.1.2；GENESIS L2 10 文件实拉+netCDF groups 探活；边界≠CDAAC ionPrf）。最近质检（R11）：**haslib**（1.0.2；11 HAS；RTCM/IGS 字节；`-m`/`HAS_Decoder.py` 帮助坑）+ **laika**（2880 历元/PDOP/pytest 17 复跑）。最近新增（质检）：**hatanaka**（2.8.1/`rinex-decompress`+georinex 实跑）+ **R10 质检** `rnxcmp`（gzip/CRLF/`-h`）/`nequickg`（Medium 全表 + `map`/plt 坑）。最近新增（用法讲解）：**android_rinex**（GnssLogger→RINEX；1379 历元+georinex 探活）+ **haslib**（1.0.2 SBF→RTCM 11 HAS）+ **laika**（slac1700.18o 实跑；Earthdata 未跑）；前序 **rnxcmp**（GSI RNXCMP 4.2.0 实跑）+ **nequickg**（Py3 移植后 Medium 校验行实跑；官方 C 登记受限）；前序 **pinot**（orderfile/sitecheck/metacheck 实跑）+ **autorino**（2.4.2 cfgfile_check 实跑；convert 环境受限）；前序 **cssrlib**（1.2.1 SPP）+ **gnss-tec**（1.1.1）。最近质检（ops）：**R9 二遍**已补 `cssrlib`（`nav.t`）/`gnss-tec`（stdout+type N）/`pinot`（subnet/low2upper 复跑）/`autorino`（check_rnx `figure_saver` 实错）。**R8 二遍**已补 `pytecgg`（ABMF 全日 veq 实跑；作者 viventriglia）/`gfzrnx`（`-sifl` guide-only，无官方二进制 stdout）。**R7 二遍**已补 `georinex`（NAV 实跑）/`rtklib`（apt↔EX PATH）/`bnc`（REQC vs NTRIP 标签）。Round6：**anubis**（登记受限）+ **pride-pppar**（3.2.11 实跑头；FTPS 未出解）；**sh-gim 未扩**。Round5：**pygnssutils**；Round4：**bkg-ntripcaster**；Round3：**ionex-gim** / **oasis-roti** / **ionomoni**；Round2：**bnc** / **georinex** / **iono-scintillation**；Round1：**gfzrnx** / **rtklib** / **pytecgg**。行数以本表 `wc -l` 为准。

## 推荐阅读顺序（新人）

1. 本页「全部手册」表 + [data-access](../data-access.md)
2. [georinex](./georinex.md) 冒烟
3. 路径 A：[pytecgg](./pytecgg.md) + 教程 02/16
4. 路径 B：[oasis-roti](./oasis-roti.md) 或 [ionomoni](./ionomoni.md) + 教程 05
5. 需要定位再 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
6. 实时课再 [pygnssutils](./pygnssutils.md)/[ntripstreams](./ntripstreams.md)/[pyrtcm](./pyrtcm.md)/[pyspartn](./pyspartn.md)/[pyubx2](./pyubx2.md)/[pynmeagps](./pynmeagps.md)/[pygpsclient](./pygpsclient.md)/[bnc](./bnc.md)；教学定位拆解见 [glab-upc](./glab-upc.md)
7. GIM 课 [ionex-gim](./ionex-gim.md) / Rust [ionex-rs](./ionex-rs.md)；SH-GIM 仅边界；CLAS → [claslib](./claslib.md)；MADOCA → [madocalib](./madocalib.md)；B2b → [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md)；多路径 QC → [gnss-multipath-analysis](./gnss-multipath-analysis.md)

---

## 不要做的事

- 不要把未校准相对 TEC 当绝对产品发表。
- 不要期望 SH-GIM clone 后出全球球谐解。
- 不要把 ROTI 当硬件 S4。
- 不要在未 QC 的坏站上硬跑 PPP/TEC。
- 不要把 PPP 残差当 STEC 产品。
- 不要把 Free/Pro、公开/专有功能写混。
- 不要把口令提交进 git。
- 参数冲突时以上游帮助为准。
- 并行写作者：勿同时全文重写同一 `docs/software/*.md`；先改本页状态再动手。

---

## 工具依赖速览

```text
data-access
   ├─ autorino (厂商 RAW→RINEX3/4 入库)
   ├─ rinexmod (RINEX 头/长短名/压缩规范化；autorino 伴生)
   ├─ android_rinex (手机 GnssLogger→RINEX3)
   ├─ cosmic-crunch (GENESIS 大气 RO L2→netCDF；电离层 RO→data-access/CDAAC)
   ├─ awsgnssroutils (AWS RO 三型查/下；电离层用 calibratedPhase；Ne→CDAAC)
   ├─ pysatcdaac (CDAAC ionPrf/ionPhs→pysat；Ne 用 ionprf；ionphs 建议 netCDF4)
   ├─ teqc (EOL 翻译/编辑/QC；后继 gfzrnx/anubis/rnxcmp)
   ├─ gnsstk (C++ 库 + RinSum/RinDump；原 GPSTk)
   ├─ pinot (旧 TEQC 批壳 / 缺站日目录)
   ├─ gampii-good (GAMP II YAML 观测/产品下载 GOOD)
   ├─ fast (下载/QC/粗 SPP/选站)
   ├─ gdds (IGS/CORS/产品/时序 GUI 下载)
   ├─ gnss-downloader (PyQt WHU/NASA 日文件；2020；无下载 CLI)
   ├─ rnxcmp (官方 Hatanaka CRX)
   ├─ hatanaka (Python CRX↔RNX / georinex 依赖)
   ├─ crx2rnx (Rust 仅解压 CRX；≠ GSI/hatanaka 同名)
   ├─ gfzrnx (可选清洗)
   ├─ anubis (门禁)
   ├─ georinex (探活)
   ├─ gnsspy (pandas 读 / RINEX 2↔3；无 PyPI)
   ├─ gnsstools (轻量 RINEX/SP3→pandas；无 PyPI；对照 georinex/gnsspy)
   ├─ cycle-slip-correction (R3 周跳试验；不写回 OBS)
   ├─ drcycleslip (三频注入–探测教学；不写回 OBS)
   ├─ gnss-tec / pytecgg (路径 A；粗相对→校准)
   ├─ oasis-roti / ionomoni (路径 B)
   ├─ ionex-gim (对照)
   ├─ ionex-rs (Rust IONEX 读写)
   ├─ diffionmap (两幅 IONEX 并排 VS)
   ├─ cddis-highrate-downloader (CDDIS high-rate 15 min)
   ├─ geospacelab (OMNI/指数/Madrigal TEC 产品图)
   ├─ pyglow (IRI 气候态对照)
   ├─ iri2016 (IRI-2016 → xarray)
   ├─ pyiri / pyirtam (纯 Python IRI / IRTAM)
   ├─ apexpy (Apex/QD/MLT 磁坐标)
   ├─ aacgmv2 (AACGM-v2 / MLT；交叉 apexpy)
   ├─ kamodo (CCMC 模式场函数化；SWMF_IE)
   ├─ msise00 (NRLMSISE-00 中性大气)
   ├─ gps-measurement-tools (GnssLogger 采集；→ android_rinex)
   ├─ pygpsclient (板卡 GUI / NTRIP；捆 pygnssutils)
   ├─ pynmeagps (NMEA 编解码；pygpsclient/pygnssutils 底层)
   ├─ pyubx2 (UBX 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ pyrtcm (RTCM3 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ pyspartn (SPARTN 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ glab-upc (教学 SPP/PPP；官方 UPC gLAB)
   ├─ pygnssutils / ntripstreams / bnc / bkg-ntripcaster (路径 C)
   └─ cssrlib / claslib / b2blib / haslib / madocalib / laika / rtklib / pride-pppar (路径 D)
sh-gim：仅路径 E 边界，不串进 A/B 主链
iono-scintillation：概念/仿真旁路，不替代实测 ROTI
```

---

## 与 tutorials 对照

| 教程 | 优先手册 |
| --- | --- |
| 02 / 16 | georinex · gnsspy · gnsstools · gnsstk · teqc · rinexmod · hatanaka · crx2rnx · gnss-tec · pytecgg |
| 03 / 10 / 18 | ionex-gim · ionex-rs · diffionmap · sh-gim(边界) · pyglow |
| 04 | iri2016 · pyglow · pyiri · pyirtam · apexpy · aacgmv2 · msise00 · nequickg · kamodo |
| 05 / 13 / 21 | oasis-roti · ionomoni · iono-scintillation · geospacelab |
| 06 / 20 | cssrlib · haslib · madocalib · laika · gnss_lib_py · android_rinex · gps-measurement-tools · pygpsclient · pynmeagps · pyubx2 · pyrtcm · pyspartn · ntripstreams · glab-upc · rtklib · pride-pppar · ionomoni |
| 09 | pytecgg |

---

## 体量与文风

- 常规工具文：稠密操作优先；已全面 QUALITY 改写，多数 120–450 行
- SH-GIM：短边界说明优先（准确 > 凑行）
- 本索引：先列全手册 + 状态，再写路径
- 禁止问答注水、禁止为凑行数复读、禁止臆造未捕获的 stdout

---

## 相关

[data-access](../data-access.md) · [categories](../categories.md) · [tutorials](../tutorials/README.md) · [`PROJECTS.json`](../../PROJECTS.json)
