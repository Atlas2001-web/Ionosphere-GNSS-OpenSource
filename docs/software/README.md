# 软件操作手册索引

本目录共有 **37 篇**操作手册（合计 **8933** 行，`wc -l`，不含本索引）：命令、输入输出、坑、选型。不是教材正文。

概念课见 [`docs/tutorials/`](../tutorials/)。条目以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。

参数冲突时：**本机 `-h` / 上游 README > 本手册示例**。

---

## 并行写作状态（持续 QC 中）

| 角色 | 负责 | 勿抢 |
| --- | --- | --- |
| **软件手册质检**（本 bot） | 已短硬篇的**二遍质检补洞**（错 I/O、过时旗标、仍薄点）；优先 `georinex` / `rtklib` / `bnc` / `gfzrnx` / `pytecgg` | 勿大改「仍薄/缺篇」同事正在写的文件 |
| **软件用法讲解**（并行） | 写 **尚未短硬 / 缺篇** 新手册 | 勿重写下表已标「已短硬」全文（补丁可协调） |

**下一优先（质检二遍，按弱→强）：** 停写门槛已近——剩余主要是 **登记/环境受限**（`anubis` / `ionomoni` / `iono-scintillation` / `gfzrnx`）无本机真实 I/O 可补；**sh-gim** 保持边界。**已短硬入库 `pyglow` + `iri2016` + `apexpy`**。**已质检复跑** `gnss_lib_py` + `pyiri` + `pyirtam` + `fast`（stdout 对齐；LGDC 429 已记）。**用法讲解已入库** `diffionmap` + `cddis-highrate-downloader` + `msise00` + `awsgnssroutils` + `android_rinex` + `cosmic-crunch`。
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
| 36 | [diffionmap.md](./diffionmap.md) | 两幅 IONEX 并排对照（VS 图） | 179 | **已短硬** · tip `57ceb1d`；Py3 读 CODG/WHUC 12 图 mean≈24.84；IGRG mean≈13.367；Basemap 出图环境受限 |
| 37 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) | CDDIS 高采样 15 min 块批量下载 | 179 | **已短硬** · 本机 1.0.2；FTPS 登录+CWD+SIZE 706256；LIST/RETR 425 受限；Linux 无 CRX2RNX |

**状态图例：** `已短硬` = Round 已按 short-hard 改过且可作二遍质检；`登记受限` / `环境受限` = 无本机官方二进制或运行时，命令以官方/仓内为准、**禁止伪造 stdout**；`边界` = sh-gim 专有求解器未开源；`仍薄` = 尚无短硬或明显缺真实 I/O（当前 **0 篇**——新缺篇由「软件用法讲解」认领后改此表）。

每篇结构：**用途边界 → 安装 → 逐步命令+期望输出 → I/O 字段 → 参数 → 接到哪步 → ≥8 坑 → 选型**。

---

## 30 秒选型

| 你要… | 打开 |
| --- | --- |
| 读 RINEX 进 Python | [georinex.md](./georinex.md) |
| 改/拼/抽稀 RINEX | [gfzrnx.md](./gfzrnx.md) |
| 观测 QC 报告 | [anubis.md](./anubis.md) |
| 旧 CORS 缺站/日目录/TEQC 批壳 | [pinot.md](./pinot.md) |
| GNSS 产品下载 + 观测 QC + 粗 SPP | [fast.md](./fast.md) |
| 厂商 RAW→RINEX3/4 台网入库 | [autorino.md](./autorino.md) |
| Hatanaka `.crx` 官方压缩/恢复 | [rnxcmp.md](./rnxcmp.md) |
| Python 解 `.crx` / 脚本压缩（pip） | [hatanaka.md](./hatanaka.md)（官方 → [rnxcmp](./rnxcmp.md)） |
| Galileo NeQuick-G 模型（脚本） | [nequickg.md](./nequickg.md) |
| IRI-2012/2016 气候态（Python 包装） | [pyglow.md](./pyglow.md) |
| IRI-2016 官方驱动 → xarray | [iri2016.md](./iri2016.md) |
| 纯 Python IRI（无 Fortran） | [pyiri.md](./pyiri.md) |
| IRTAM 同化系数→网格 Ne（纯 Python） | [pyirtam.md](./pyirtam.md) |
| Android/多源 GNSS → NavData / 教学 WLS | [gnss_lib_py.md](./gnss_lib_py.md) |
| 校准 sTEC/vTEC | [pytecgg.md](./pytecgg.md) |
| 粗相对斜 TEC（无 DCB） | [gnss-tec.md](./gnss-tec.md) |
| ROTI / AATR / ΔTEC | [ionomoni.md](./ionomoni.md) · [oasis-roti.md](./oasis-roti.md) |
| 读 IONEX GIM | [ionex-gim.md](./ionex-gim.md) |
| 两幅 IONEX 并排对照 | [diffionmap.md](./diffionmap.md) |
| CDDIS 高采样（1 s / 15 min）批量 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) |
| 球谐 GIM 边界说明 | [sh-gim.md](./sh-gim.md) |
| NTRIP 脚本拉流 / 小 caster | [pygnssutils.md](./pygnssutils.md) |
| 多流 GUI / 录盘 | [bnc.md](./bnc.md) |
| 自建多用户 Caster | [bkg-ntripcaster.md](./bkg-ntripcaster.md) |
| RTK / 浮点 PPP | [rtklib.md](./rtklib.md) |
| PPP-AR | [pride-pppar.md](./pride-pppar.md) |
| Python 开放 PPP/PPP-RTK（CLAS/HAS） | [cssrlib.md](./cssrlib.md) |
| Galileo HAS 页 → RTCM/IGS SSR | [haslib.md](./haslib.md) |
| 轻量 Python 观测处理 / 自写估计器 | [laika.md](./laika.md) |
| 手机 GnssLogger → RINEX | [android_rinex.md](./android_rinex.md) |
| GENESIS COSMIC-1 **大气** L2→netCDF（非 ionPrf） | [cosmic-crunch.md](./cosmic-crunch.md) |
| AWS GNSS-RO 查/下（**calibratedPhase** / 大气三型） | [awsgnssroutils.md](./awsgnssroutils.md) |
| CDAAC **ionPrf / ionPhs**（pysat） | [pysatcdaac.md](./pysatcdaac.md) |
| 闪烁仿真（MATLAB） | [iono-scintillation.md](./iono-scintillation.md) |

---

## 工作流路径 A–E

### A · 一日 TEC

[data-access](../data-access.md) →（可选 [fast](./fast.md) 下载·QC / [autorino](./autorino.md) 入库 / [android_rinex](./android_rinex.md) 手机日志 / [pinot](./pinot.md) 旧批壳）→ [georinex](./georinex.md) →（可选 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)/[gnss-tec](./gnss-tec.md) 粗相对 TEC）→ [pytecgg](./pytecgg.md) → [ionex-gim](./ionex-gim.md) 对照 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[09](../tutorials/09-dcb-biases-deep.md)/[16](../tutorials/16-practice-one-day-tec.md)

### B · 不规则体 / 磁暴

高采样备数（可选 [cddis-highrate-downloader](./cddis-highrate-downloader.md)）→ RINEX → [ionomoni](./ionomoni.md) 或 [oasis-roti](./oasis-roti.md) → 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)/[21](../tutorials/21-equatorial-anomaly-bubbles.md)；高 ROTI 时段对照 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md) 固定率；仿真概念见 [iono-scintillation](./iono-scintillation.md)·[13](../tutorials/13-scintillation-modeling.md)

### C · 实时差分 / 实验室 CORS

[pygnssutils](./pygnssutils.md) 或 [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)；落盘后再走 A/B

### D · 发表级坐标 / ZTD

QC（[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [rtklib](./rtklib.md) 冒烟 →（开放服务教学 [cssrlib](./cssrlib.md)）→ [pride-pppar](./pride-pppar.md) + 精密产品 → 教程 [06](../tutorials/06-iono-positioning.md)

### E · 理解 GIM（非端到端自建）

[ionex-gim](./ionex-gim.md) 读产品；[diffionmap](./diffionmap.md) 两图并排；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表里其它 GIM 工具 → 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 事实边界（归属说明，不是目录）

下面两行**不是**「只有这两个软件」，只是容易写错归属的提醒：

| 项目 | 关系 |
| --- | --- |
| [PyTECGg](./pytecgg.md) | 作者 **viventriglia**（不是本仓维护者自有） |
| [SH-GIM](./sh-gim.md) | 本仓维护者自有；**球谐求解器未开源** |
| 本目录其它手册 | 操作说明；许可与 EULA 以上游为准 |

---

最近新增（用法讲解）：**diffionmap**（`57ceb1d`；CODG/WHUC 读路径+IGRG mean；Basemap 受限）+ **cddis-highrate-downloader**（1.0.2；FTPS SIZE 706256；RETR 425）+ **msise00**（1.11.1；Tn@250km）+ **pysatCDAAC**（0.0.5；ionprf 59→53；ionphs 144 下、load 维冲突）+ **pyirtam**（0.0.7；LGDC 四系数+IRI/IRTAM NmF2/vTEC）+ **fast**（3.01.01；ABPO satNum+1h SPP；FTP 下载失败记坑）+ **awsgnssroutils**（1.2.7；Phase 3 文件+atm 对照；S3 开放/rotcol 门禁）+ **gnss_lib_py**（1.1.0 NavData/OBS）+ **pyiri**（0.1.7 单点 NmF2/vTEC）。最近新增（质检）：**iri2016**（1.12.0；xarray 剖面+foF2/TEC；与 pyglow 同点对照）+ **pyglow**（Py3.8/`1988757`；IRI-2016/2012 剖面+IGRF/HWM14 实跑；`igrf2015` 静默退出坑）。最近新增（用法讲解）：**cosmic-crunch**（2.1.2；GENESIS L2 10 文件实拉+netCDF groups 探活；边界≠CDAAC ionPrf）。最近质检（R11）：**haslib**（1.0.2；11 HAS；RTCM/IGS 字节；`-m`/`HAS_Decoder.py` 帮助坑）+ **laika**（2880 历元/PDOP/pytest 17 复跑）。最近新增（质检）：**hatanaka**（2.8.1/`rinex-decompress`+georinex 实跑）+ **R10 质检** `rnxcmp`（gzip/CRLF/`-h`）/`nequickg`（Medium 全表 + `map`/plt 坑）。最近新增（用法讲解）：**android_rinex**（GnssLogger→RINEX；1379 历元+georinex 探活）+ **haslib**（1.0.2 SBF→RTCM 11 HAS）+ **laika**（slac1700.18o 实跑；Earthdata 未跑）；前序 **rnxcmp**（GSI RNXCMP 4.2.0 实跑）+ **nequickg**（Py3 移植后 Medium 校验行实跑；官方 C 登记受限）；前序 **pinot**（orderfile/sitecheck/metacheck 实跑）+ **autorino**（2.4.2 cfgfile_check 实跑；convert 环境受限）；前序 **cssrlib**（1.2.1 SPP）+ **gnss-tec**（1.1.1）。最近质检（ops）：**R9 二遍**已补 `cssrlib`（`nav.t`）/`gnss-tec`（stdout+type N）/`pinot`（subnet/low2upper 复跑）/`autorino`（check_rnx `figure_saver` 实错）。**R8 二遍**已补 `pytecgg`（ABMF 全日 veq 实跑；作者 viventriglia）/`gfzrnx`（`-sifl` guide-only，无官方二进制 stdout）。**R7 二遍**已补 `georinex`（NAV 实跑）/`rtklib`（apt↔EX PATH）/`bnc`（REQC vs NTRIP 标签）。Round6：**anubis**（登记受限）+ **pride-pppar**（3.2.11 实跑头；FTPS 未出解）；**sh-gim 未扩**。Round5：**pygnssutils**；Round4：**bkg-ntripcaster**；Round3：**ionex-gim** / **oasis-roti** / **ionomoni**；Round2：**bnc** / **georinex** / **iono-scintillation**；Round1：**gfzrnx** / **rtklib** / **pytecgg**。行数以本表 `wc -l` 为准。

## 推荐阅读顺序（新人）

1. 本页「全部手册」表 + [data-access](../data-access.md)
2. [georinex](./georinex.md) 冒烟
3. 路径 A：[pytecgg](./pytecgg.md) + 教程 02/16
4. 路径 B：[oasis-roti](./oasis-roti.md) 或 [ionomoni](./ionomoni.md) + 教程 05
5. 需要定位再 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
6. 实时课再 [pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)
7. GIM 课 [ionex-gim](./ionex-gim.md)；SH-GIM 仅边界

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
   ├─ android_rinex (手机 GnssLogger→RINEX3)
   ├─ cosmic-crunch (GENESIS 大气 RO L2→netCDF；电离层 RO→data-access/CDAAC)
   ├─ awsgnssroutils (AWS RO 三型查/下；电离层用 calibratedPhase；Ne→CDAAC)
   ├─ pysatcdaac (CDAAC ionPrf/ionPhs→pysat；Ne 用 ionprf；ionphs 建议 netCDF4)
   ├─ pinot (旧 TEQC 批壳 / 缺站日目录)
   ├─ fast (下载/QC/粗 SPP/选站)
   ├─ rnxcmp (官方 Hatanaka CRX)
   ├─ hatanaka (Python CRX↔RNX / georinex 依赖)
   ├─ gfzrnx (可选清洗)
   ├─ anubis (门禁)
   ├─ georinex (探活)
   ├─ gnss-tec / pytecgg (路径 A；粗相对→校准)
   ├─ oasis-roti / ionomoni (路径 B)
   ├─ ionex-gim (对照)
   ├─ diffionmap (两幅 IONEX 并排 VS)
   ├─ cddis-highrate-downloader (CDDIS high-rate 15 min)
   ├─ pyglow (IRI 气候态对照)
   ├─ iri2016 (IRI-2016 → xarray)
   ├─ pyiri / pyirtam (纯 Python IRI / IRTAM)
   ├─ apexpy (Apex/QD/MLT 磁坐标)
   ├─ msise00 (NRLMSISE-00 中性大气)
   ├─ pygnssutils / bnc / bkg-ntripcaster (路径 C)
   └─ cssrlib / haslib / laika / rtklib / pride-pppar (路径 D)
sh-gim：仅路径 E 边界，不串进 A/B 主链
iono-scintillation：概念/仿真旁路，不替代实测 ROTI
```

---

## 与 tutorials 对照

| 教程 | 优先手册 |
| --- | --- |
| 02 / 16 | georinex · hatanaka · gnss-tec · pytecgg |
| 03 / 10 / 18 | ionex-gim · diffionmap · sh-gim(边界) · pyglow |
| 04 | iri2016 · pyglow · pyiri · pyirtam · apexpy · msise00 · nequickg |
| 05 / 13 / 21 | oasis-roti · ionomoni · iono-scintillation |
| 06 / 20 | cssrlib · haslib · laika · gnss_lib_py · android_rinex · rtklib · pride-pppar · ionomoni |
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
