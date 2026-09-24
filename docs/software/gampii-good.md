# GAMPII-GOOD · GNSS 观测与产品下载器（GOOD）操作手册

目录：[`PROJECTS.json` → `GAMPII-GOOD`](../../PROJECTS.json) · 上游 <https://github.com/zhouforme0318/GAMPII-GOOD> · 许可 **GPL-3.0**（`LICENSE`）· tip **`479aa14`**（2024-02-25，README「version 3.1」）· 二进制入口 **`run_GOOD`** · 本机验证（2026-09-24 EDT）：CMake Release 编译通过；无参用法 exit **255**；WHU FTP `mixed3` BRDC + HTTPS ANTEX 实拉成功 · ★≈124 · **质检复跑通过**（无参 Usage exit **255**；缺 YAML exit **0**；BRDC/brdm **11371068** B；`igs14.atx` **23412643** / `igs20.atx` **61300492**；重跑 `has existed!`；tip `479aa14`；2026-09-24 04:59 EDT）

> 岗位：用 **一份 YAML** 批量拉 IGS/MGEX/CORS 观测、广播星历、精密 sp3/clk、EOP、ORBEX、DCB/OSB、SINEX、GIM/ROTI、对流层、ANTEX——专为 **GAMP II / PPP 流水线备数**。冲突时：**仓内 `README` / `doc/GOOD v3.1 Users Guide.pdf` / 本机 stdout > 本文**。门户总表 → [data-access](../data-access.md)；GUI 多模块 → [gdds](./gdds.md)；下载+QC+粗 SPP → [fast](./fast.md)。

## 1. 用途与边界

**做：**

1. **观测**：IGS 日/时/高采样（RINEX 2 短名）；MGEX 日/时/高采样（RINEX 3 长名）；`igm`=IGS∪MGEX（MGEX 站优先）；CUT / 香港 CORS（30s/5s/1s）/ NGS·NOAA / EPN / PBO / 智利 CSN
2. **广播星历**：单系统或 `mixed3`/`mixed4`；日或时；`igs`/`dlr`/`ign`/`gop`/`wrd` 等组合源
3. **精密产品**：多 AC final/rapid/ultra（`cod`/`igs`/`gfz_m`/`whu_u`/`cnt`…）；可选前后日、合并三日 sp3
4. **其它**：EOP、ORBEX、DCB/DSB、OSB、周解 SINEX、GIM、ROTI、对流层、ANTEX
5. **镜像**：`ftpArch: cddis | ign | whu`（底层 `wget`；Linux 上 `wget`/`gzip` 走 PATH，`crx2rnx` 走 `3partyDir`）
6. **已下跳过**：同名文件存在则 `has existed!`，不重复拉

**不做：**

- **不是** QC / SPP / PPP 解算 → [fast](./fast.md) / [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [glab-upc](./glab-upc.md)；GAMP 学习源码另见 `GAMP_PPPH`（无本手册）
- **不是** PyQt 点选 GUI → [gdds](./gdds.md)；也 **不是**「`-t` 类型名」式 Python CLI → [fast](./fast.md)
- **不是** 数据门户说明总表 → [data-access](../data-access.md)
- **不是** 专用 CDDIS 1 s / 15 min 块工具 → [cddis-highrate-downloader](./cddis-highrate-downloader.md)
- **无** `-h`/`--help`（唯一 CLI：`run_GOOD <yaml>`；参数全在 YAML）
- **不** 内置 Earthdata 登录——`cddis` 镜像常需自备账号/证书或改 `whu`/`ign`

一句话：GOOD = **C++ / CMake / YAML 驱动的 GNSS 观测+产品下载器**（SDUST UNIQ；GAMP II 配套）。

| 术语 | 含义 |
| --- | --- |
| `mainDir` | 数据根；子目录均相对它拼接 |
| `procTime` | `1 y m d ndays` / `2 y doy ndays` / `3 week dow ndays` |
| `ftpArch` | `cddis` / `ign` / `whu` |
| `l2s4*` | 长名=0 / 短名=1 / 长短都要=2 |
| `3partyDir` | 第三方工具子目录；Linux 至少要有可执行 `crx2rnx` |
| `printInfoWget` | `1`→`wget -r` 打印进度；`0`→`-qr` |

## 2. 安装 / 编译

依赖：`cmake`≥3.10、`g++`（C++14）、系统 `wget`/`gzip`；yaml-cpp **已捆** `thirdparty/yaml-cpp-0.7.0`。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/zhouforme0318/GAMPII-GOOD.git
cd GAMPII-GOOD
mkdir -p build && cd build
cmake ../ -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
# 产物：../bin/run_GOOD（EXECUTABLE_OUTPUT_PATH=仓根/bin）
ls -la ../bin/run_GOOD
# 仓内另有预编译 dataset_Linux/run_GOOD_V3.1（ELF64）；本文以源码编译为准
```

**本机（2026-09-24 EDT）**：`cmake` 3.31.6 + g++ 14.2 → `bin/run_GOOD`（≈1.2 MB）链接成功；yaml-cpp 子工程有 CMake `<3.10` deprecation，可忽略。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `yaml-cpp` 找不到 | 用了旧 `CMakeLists_Linux.txt`（`find_package`） | 用根目录现行 `CMakeLists.txt`（`add_subdirectory(thirdparty/…)`） |
| 观测下完仍是 `.crx` | `3partyDir/crx2rnx` 缺失或无执行位 | `chmod +x …/crx2rnx`；可用 [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md) 补 |
| Windows | 需 MSVC + VS Code CMake 套件 | 见上游 README §1.4；跑 `.\bin\Release\run_GOOD.exe .\dataset_Win\GOOD_cfg.yaml` |

## 3. 端到端：用法 → YAML → 真下载（本机实跑；质检复跑 2026-09-24 04:59 EDT）

### 3.1 无参 / 坏配置（期望输出）

```bash
./bin/run_GOOD
# 期望 stdout（ANSI 紫色，本文去色）与 exit：
# * Usage: run_GOOD GOOD_cfg.yaml
# exit 255（main 返回 -1）

./bin/run_GOOD /path/to/missing.yaml
# 期望：
# GAMP II: intelliGent Analysis system for Multi-sensor integrated navigation and Positioning v2.0
# ===================================================================================================
# * Now, we are running GAMP II - GOOD (GNSS Observations and prOducts Downloader)
# *** ERROR(Config::ReadCfgYaml): Failed to read the configuration file. Please check the path and format of the configuration file!
# exit 0（读配置失败后直接 return，不置错误码）
```

### 3.2 最小可跑 YAML（NAV mixed3 + ANTEX）

复制 `dataset_Linux/` 脚手架，**务必改 `mainDir` 为你的绝对路径**，并保证 `mainDir/3partyDir/crx2rnx` 存在：

```yaml
mainDir       : /workspace/iono_ops/good_smoke   # ← 改成你的路径
obsDir        : obs
navDir        : nav
orbDir        : orb
clkDir        : clk
eopDir        : eop
obxDir        : obx
biaDir        : bia
snxDir        : snx
ionDir        : ion
ztdDir        : ztd
tblDir        : tbl
logDir        : log
3partyDir     : thirdparty_Linux

procTime      : 2  2024  1  1          # 类型2：年 + DOY + 天数 → 2024-001 共 1 天
minusAdd1day  : 0
merge_sp3files: 0
printInfoWget : 1

ftpDownloading:
  opt4ftp: 1
  ftpArch: whu
getObs:
  opt4obs: 0
  obsType: daily
  obsFrom: mgex
  obsList: site_one.list
  sHH4obs: 00
  nHH4obs: 1
  l2s4obs: 1
getNav:
  opt4nav: 1
  navType: daily
  navSys : mixed3
  navFrom: igs
  navList: site_one.list
  sHH4nav: 00
  nHH4nav: 1
  l2s4nav: 2                 # 长短名都落盘
getOrbClk: { opt4oc: 0, ocFrom: igs, sHH4oc: 00, nHH4oc: 1, l2s4oc: 2 }
getEop:    { opt4eop: 0, eopFrom: igs, sHH4eop: 00, nHH4eop: 1, l2s4eop: 2 }
getObx:    { opt4obx: 0, obxFrom: all }
getDsb:    { opt4dsb: 0, dsbFrom: all }
getOsb:    { opt4osb: 0, osbFrom: cas }
getSnx:    { opt4snx: 0, l2s4snx: 2 }
getIon:    { opt4ion: 0, ionFrom: cod, l2s4ion: 2 }
getRoti:   { opt4rot: 0 }
getTrp:    { opt4trp: 0, trpFrom: igs, trpList: site_trp.list, l2s4trp: 2 }
getAtx:    { opt4atx: 1 }
```

```bash
# 从仓根跑（路径按你的 mainDir）
./bin/run_GOOD /workspace/iono_ops/good_smoke/GOOD_cfg.yaml
```

**本机真跑关键 stdout（去色；中间夹大量 `wget` 进度条，WHU FTP LIST 曾重试）：**

```text
GAMP II: intelliGent Analysis system for Multi-sensor integrated navigation and Positioning v2.0
===================================================================================================
* Now, we are running GAMP II - GOOD (GNSS Observations and prOducts Downloader)

--2026-09-24 04:51:15--  ftp://igs.gnsswhu.cn/pub/gps/data/daily/2024/brdc
… PASV … LIST … Error in server response … Retrying.   # 可多次
… successfully download broadcast ephemeris file BRDC00IGS_R_20240010000_01D_MN.rnx
… successfully download IGS ANTEX file igs14.atx
… successfully download IGS ANTEX file igs20.atx
```

**落盘（本机 `ls`/`wc -c`）：**

| 路径 | 字节 | 说明 |
| --- | ---: | --- |
| `nav/2024/001/BRDC00IGS_R_20240010000_01D_MN.rnx` | 11371068 | RINEX 3.04 MIXED NAV；头 `PGM / RUN BY`=`MergeMNfile.tcl IGS` |
| `nav/2024/001/brdm0010.24p` | 11371068 | 短名副本；与长名 **字节相同**（`l2s4nav: 2`） |
| `tbl/igs14.atx` | 23412643 | HTTPS `files.igs.org` |
| `tbl/igs20.atx` | 61300492 | 同上；ANTEX 1.4 |
| `log/log.txt` | （小） | `url -> local OK` 审计行 |

重跑同一 YAML（质检复跑同文；字节未变）：

```text
*** INFO(FtpUtil::GetNav): broadcast ephemeris file BRDC00IGS_R_20240010000_01D_MN.rnx or brdm0010.24p has existed!
*** INFO(FtpUtil::GetAntexIGS): IGS ANTEX file igs14.atx has existed!
*** INFO(FtpUtil::GetAntexIGS): IGS ANTEX file igs20.atx has existed!
```

打开观测时：把 `getObs.opt4obs` 置 `1`，`obsList` 指向站列表（每行四字符站名，如仓内 `site_mgex.list`），`obsFrom: mgex`，`obsType: daily`。全目录 `obsList: all` 体量极大，慎用。

## 4. 输入 / 输出速查

| 方向 | 内容 |
| --- | --- |
| **入** | 唯一 CLI 参数：YAML 路径；站列表文件（相对 `mainDir`）；系统 `wget`/`gzip`；`3partyDir/crx2rnx` |
| **出** | `obs/YYYY/DOY/<SRC>/…`、`nav/YYYY/DOY/…`、`orb`/`clk`/`eop`/`obx`/`bia`/`snx`/`ion`/`ztd`/`tbl`；`log/log.txt` |
| **压缩** | 远端 `.gz`/`.Z` → 本地 `gzip -d`；CRINEX → `crx2rnx` |
| **审计** | `printInfoWget:1` 时 stderr/stdout 混有 wget；`log.txt` 记 `OK`/`failed` |

## 5. 关键 / YAML 要点

完整键见仓内 `dataset_Linux/GOOD_cfg.yaml` 注释。常用开关：

| 键 | 作用 |
| --- | --- |
| `ftpDownloading.opt4ftp` | 总开关；`0` 则什么都不下 |
| `getObs.obsFrom` | `igs`/`mgex`/`igm`/`cut`/`hk`/`ngs`/`epn`/`pbo`/`chi` |
| `getObs.obsType` | IGS/MGEX：`daily`/`hourly`/`highrate`；港 CORS：`30s`/`5s`/`1s` |
| `getOrbClk.ocFrom` | 可 `+` 叠多中心，如 `igs+gfz_m`；`cnt`=CNES 实时离线文件 |
| `minusAdd1day` | 精密轨道钟前后各多一天 |
| `merge_sp3files` | 合并连续三日 sp3 |

详细字段表与截图：`doc/GOOD v3.1 Users Guide.pdf`。

## 6. 接到哪一步（vs GDDS / data-access / FAST）

| 需求 | 优先 |
| --- | --- |
| **YAML/CLI 无头批量** 观测+多 AC 产品（GAMP/PPP 备数） | **本文 GOOD** |
| 点选 IGS/CORS/时序、带地图 | [gdds](./gdds.md)（无 CLI；本机 GUI 常受限） |
| 下载 **且** QC/粗 SPP/选站 | [fast](./fast.md) |
| 「去哪下 / 要不要注册」总表 | [data-access](../data-access.md) |
| CDDIS high-rate 15 min | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 下完 → 读 RINEX / PPP | [georinex](./georinex.md) → [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)/[glab-upc](./glab-upc.md) |
| CRX↔RNX | [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md) |

路径 A 一日 TEC：`data-access` →（可选 **GOOD** / [fast](./fast.md) / [gdds](./gdds.md)）→ [georinex](./georinex.md) → …

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 只打印 `* Usage: run_GOOD GOOD_cfg.yaml`，exit 255 | argc≠2 | 必须恰好一个 YAML 路径；**无** `-h` |
| 2 | `Failed to read the configuration file` 且 exit 0 | 路径错/YAML 坏；失败不改 exit | 查绝对路径与缩进；勿依赖 exit code |
| 3 | `mainDir` 仍指向 `/home/zhouforme/...` | 上游样例路径 | 改成你的绝对路径后再跑 |
| 4 | WHU `PASV … LIST … Error in server response` 后重试 | FTP 数据通道不稳（与 [gdds](./gdds.md) WHU NLST 同类） | 等重试；或换 `ftpArch: ign`；产品也可直链 HTTPS（ANTEX 已走 `files.igs.org`） |
| 5 | CDDIS 401 / 空目录 | 无 Earthdata | 换 `whu`/`ign`；或按 [data-access](../data-access.md) 配账号后再试 cddis |
| 6 | 观测停在 `.crx`/解压失败 | `crx2rnx` 不在 `mainDir/3partyDir` 或无 `+x` | 从 `dataset_Linux/thirdparty_Linux/` 拷贝并 `chmod +x` |
| 7 | `obsList: all` 把磁盘打满 | 整目录镜像 | 先写 `site_*.list` 几站；确认 `ndays` |
| 8 | 已下文件仍想换源 | 同名即跳过 | 删目标文件或改输出子目录后再跑 |
| 9 | `getOrbClk` 开了但缺前后日 | `minusAdd1day:0` | PPP 惯用置 `1`；超快产品再配 `sHH4oc`/`nHH4oc` |
| 10 | 把 GOOD 当解算器 | 边界混淆 | 解算接 GAMP/PRIDE/RTKLIB；GOOD **只下载** |
| 11 | `printInfoWget:1` 刷屏 | 设计如此 | 批处理改 `0`；看 `log/log.txt` |
| 12 | 旧 `CMakeLists_Linux.txt` 编不过 | 依赖系统 yaml-cpp | 用根 `CMakeLists.txt` |

## 8. 选型与链接

| 你要… | 用 |
| --- | --- |
| GAMP/PPP **YAML 批下载** 观测+产品 | **本文 GAMPII-GOOD** |
| GUI 多模块 / 时序 | [gdds](./gdds.md) |
| 下载+QC+SPP 一体 | [fast](./fast.md) |
| 源站/注册说明 | [data-access](../data-access.md) |
| high-rate 专用 | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |

- 仓库：<https://github.com/zhouforme0318/GAMPII-GOOD>
- 用户指南 PDF：仓内 `doc/GOOD v3.1 Users Guide.pdf`
- 兄弟：[data-access](../data-access.md) · [fast](./fast.md) · [gdds](./gdds.md) · [cddis-highrate-downloader](./cddis-highrate-downloader.md) · [georinex](./georinex.md) · [pride-pppar](./pride-pppar.md) · [rnxcmp](./rnxcmp.md)
