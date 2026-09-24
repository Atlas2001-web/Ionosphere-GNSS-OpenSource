# GSILIB · 国土地理院多 GNSS 基线/PPP 操作手册

目录：[`PROJECTS.json` → `GSILIB`](../../PROJECTS.json) · 门户 <https://terras.gsi.go.jp/geo_info/gsilib/gsilib.html> · 下载 <https://terras.gsi.go.jp/geo_info/gsilib/gsilib_download.html> · **ver.1.0.3**（`VER_RTKLIB`/`PROGRAM_NAME_VER`；2016-12-28 闰秒；2017-10-10 包内版本串补记）· 基线 **RTKLIB 2.4.2** + ANTTOOL · 许可 **BSD-2-Clause**（**ANTApp = GPL-3.0**）· 本机验证：拉 `GSILIB_ver.1.0.3.zip`（7 555 587 B，sha256₁₂=`63bea948a98b`）+ `ifb_correction.zip`；源码 **50**×`.c`（含 `isb.c` **377** 行）；Win PE `gsipost_gui.exe`/`gsiplot.exe` 为 **MZ**；**无 Wine32 / 无 Linux GUI 二进制 → 未跑基线固定解**；样例 IFB：georinex 读 `tr022562.14o` **1921** 历元 / **30** SV，G01 C1C=**24070092.563** · 2026-09-24 05:45 EDT · **质检复跑** 2026-09-24 06:12 EDT（zip **7555587**/sha₁₂=`63bea948a98b`；`.c` 含 `rcv/` **50**/顶层 **40**/`isb.c` **377**；MZ OK；IFB rover/base **1921**；G01 C1C=**24070092.563**/**24070770.680**；gloifb L1 **−0.0531**/L2 **−0.0877**；**无 Wine32 未跑基线解**）

> 岗位：GSI **异机种多星座短基线**（IFB/ISB、L2P–L2C ¼ 周、可选 photomask）与 RTKLIB 衍生后处理 GUI。冲突时：**门户 / `GSILIB_manual.pdf` / 包内 `readme_gsilib.txt` > 本文**。通用 CLI → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；GA YAML → [ginan](./ginan.md)。

## 1. 用途与边界

**做：**

- GPS / QZSS / GLONASS / Galileo 的 **L1/L2/L5** 后处理基线（`gsipost_gui`）与解/观测绘图（`gsiplot`）
- 相对原版 RTKLIB 2.4.2 的增量：**GLONASS IFB** 表/估计、**ISB** 表/估计、**L2P(Y)–L2C ¼ 周** 表/估计、**photomask** 仰角掩膜编辑 RINEX
- 官方解析例 ZIP：`ifb_correction` / `isb_estimation` / `isb_correction` / `l2c_data`（+ PDF 步骤）
- 源码 ANSI C；GUI 为 Embarcadero/Borland VCL（`.cbproj`）

**不做：**

- **不是** 开箱 Linux CLI——包内仅 **Windows PE** + DLL；门户写明 Win10 日文环境
- **不是** 现代实时 PPP-B2b / HAS / CLAS → [b2blib](./b2blib.md)/[haslib](./haslib.md)/[claslib](./claslib.md)
- **不是** 发表级全球 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- **不是** 把 `VER_RTKLIB "1.0.3"` 当成上游 RTKLIB 版本号——那是 **GSILIB 包版本**
- 本页 **不能** 提供本机固定率/基线残差——未跑 `gsipost_gui`

一句话：GSILIB = **GSI 面向公共测量的 RTKLIB 衍生多星座基线套件（Win 为主）**；Linux CI 通常只能验包、源码与样例 RINEX I/O。

| 术语 | 含义 |
| --- | --- |
| IFB | GLONASS 频道间偏差（异机种差分）；`gloifb.tbl` / `pos2-gloarmode=use IFB table` |
| ISB | 系统间偏差（异机种多星座）；`pos2-isb` + `out-isb*` |
| L2P–L2C / GL2 | GPS L2P(Y) 与 L2C 之间 ¼ 周相位差；`pos2-gpsl2bias` |
| photomask | 上空照片 → 仰角掩膜 → 编辑 RINEX 降多路径（独立 zip） |
| `gsipost_gui` / `gsiplot` | 后处理基线 GUI / 解与观测绘图（≈ RTKPOST / RTKPLOT） |

## 2. 安装 / 获取

### 2.1 下载（本机已通）

```bash
mkdir -p ~/iono_ops/gsilib && cd ~/iono_ops/gsilib
UA='Mozilla/5.0'
base='https://terras.gsi.go.jp/geo_info/gsilib'
curl -sL -A "$UA" -O "$base/GSILIB_ver.1.0.3.zip"
curl -sL -A "$UA" -O "$base/GSILIB_manual.pdf"
curl -sL -A "$UA" -O "$base/ifb_correction.zip"
# 可选：isb_estimation.zip isb_correction.zip l2c_data.zip ANTApp.zip photomask_ver.1.1.1.zip
unzip -qo GSILIB_ver.1.0.3.zip
unzip -qo ifb_correction.zip
ls GSILIB/bin/*.exe
# 期望：gsipost_gui.exe  gsiplot.exe
rg -n 'VER_RTKLIB|PROGRAM_NAME_VER' GSILIB/src/rtklib.h | head
# 期望：VER_RTKLIB "1.0.3" · PROGRAM_NAME_VER "GSILIB 1.0.3"
```

| 组件 | 本机探针（2026-09-24） |
| --- | --- |
| `GSILIB_ver.1.0.3.zip` | **7 555 587** B · sha256₁₂=`63bea948a98b` |
| `GSILIB_manual.pdf` | **2 260 378** B（日文；基于 RTKLIB 2.4.2 manual） |
| `bin/gsipost_gui.exe` | **8 180 224** B · MZ · 串含 `GSILIB 1.0.3` |
| `bin/gsiplot.exe` | **8 371 712** B · MZ |
| 伴生 DLL | `libblas`/`liblapack` + MinGW `libgcc`/`libgfortran`/`libquadmath` |
| `src/**/*.c` | 含 `rcv/` **50**（顶层 `src/*.c`=**40**）；新增向 `isb.c` / `H23func.c` / `mbs.c` 等 |

### 2.2 Windows 运行（上游意图）

1. 解压后运行 `GSILIB/bin/gsipost_gui.exe`（同目录保留 DLL）
2. 载入 OBS/NAV（或官方解析例 ZIP）+ 编辑选项（≈ RTKPOST）
3. 执行 → `gsiplot.exe` 看解/观测
4. 细节：`GSILIB_manual.pdf` §2；IFB/ISB/L2C 步骤见各 `*.pdf` + `*.zip`

### 2.3 Linux 诚实边界

```bash
# 预编译 GUI 为 PE；本机 wine 提示缺 wine32 → 未跑解算
file GSILIB/bin/gsipost_gui.exe   # MZ executable
# 源码可参考移植 CUI（无官方 makefile）；工程量≈自建 RTKLIB + 合并 isb/IFB 补丁
# 实践建议：异机种实验在 Win 跑 GSILIB；Linux 产线用 rtklib / pride-pppar / ginan
```

## 3. 端到端

### 3.1 样例 I/O：IFB 异机种基线数据（本机真跑；无 GUI 解）

官方 `ifb_correction.zip`：Trimble NetR9 ↔ LEICA GR25，2014-09-13，30 s，RINEX **3.02** Mixed（`GSICONV 1.0.0`）。

```bash
cd ~/iono_ops/gsilib/ifb_correction   # 解压后目录名以 zip 内为准
python3 - <<'PY'
import georinex as gr, numpy as np, warnings
warnings.filterwarnings('ignore')
obs = gr.load('tr022562.14o', use='G')
print('rover', dict(obs.sizes))
print(np.datetime_as_string(obs.time.values[0], unit='s'), '→',
      np.datetime_as_string(obs.time.values[-1], unit='s'))
sv = list(map(str, obs.sv.values))
i = sv.index('G01')
print('G01 C1C', float(obs['C1C'].isel(sv=i, time=0)))
print('G01 L1C', float(obs['L1C'].isel(sv=i, time=0)))
h = gr.rinexheader('tr022562.14o')
print('MARKER', (h.get('MARKER NAME') or '').strip())
print('REC', (h.get('REC # / TYPE / VERS') or '')[:48])
PY
```

**本机结果（2026-09-24 05:45 EDT；质检复跑 06:12 EDT 对齐）：**

| 文件 | 探针 |
| --- | --- |
| `tr022562.14o`（rover） | **1921** 历元 / GPS **30** SV；`2014-09-13T07:00:00`→`23:00:00`；INTERVAL **30** s；MARKER **BL_0**；REC **NetR9**；G01 C1C=**24070092.563** / L1C=**126489232.973** |
| `le102562.14o`（base） | **1921** 历元 / GPS **31** SV；同窗；MARKER **1001**；REC **LEICA GR25**；G01 C1C=**24070770.680** / L1C=**126492813.647** |
| `le102562.14n` / `.14g` | GPS NAV **27**×time/**32** SV；GLO NAV **44**×time/**24** SV |
| `gloifb.tbl` | LEICA GR25 ↔ Trimble NetR9：L1 **−0.0531**、L2 **−0.0877** m/MHz |
| `ifb.conf` | `pos1-posmode=kinematic`；`pos1-navsys=5`（GPS+GLO）；`pos2-gloarmode=use IFB table`；`pos3-gloifbfile=D:\ifb_correction\gloifb.tbl`（**须改本地路径**） |

### 3.2 Windows 上跑 IFB 基线（有包之后；本机未跑）

1. `gsipost_gui`：rover=`tr022562.14o`，base=`le102562.14o` + `.14n`/`.14g`
2. 选项载入 `ifb.conf` 后把 `pos3-gloifbfile` 改成你的 `gloifb.tbl` 绝对路径
3. Execute → 用 `gsiplot` 打开 `.pos`
4. **勿**把未复现的 PDF 截图坐标当本机结果

### 3.3 旁路：同数据用开源引擎冒烟

```bash
# 例：系统 rtklib rnx2rtkp 浮点短弧（无 IFB 表语义）
# 细节见 rtklib.md；发表级多站 → pride-pppar / ginan
```

## 4. I/O 与关键参数

| 输入 | 说明 |
| --- | --- |
| RINEX OBS/NAV（2.x/3.x） | 样例为 3.02 Mixed；异机种需匹配时段 |
| `*.conf` | GSILIB 扩展了 `pos2-isb` / `pos2-gpsl2bias` / `pos2-gloarmode` / `pos3-gloifbfile` 等 |
| `gloifb.tbl` / ISB·GL2 表 | 机型对机型；FLAG 列见 PDF |
| photomask 掩膜 | 单独工具链产出，再喂编辑后的 OBS |

| 输出 | 含义 |
| --- | --- |
| `.pos` 等 | 与 RTKLIB 解格式同源（llh/xyz/… 由 `out-solformat`） |
| ISB/GL2 输出文件 | `out-isbout` / `out-gl2out` 控制 |
| `gsiplot` 图 | 解、残差、观测 |

| 参数（摘） | 作用 |
| --- | --- |
| `pos2-gloarmode` | `off` / `on` / `autocal` / **`use IFB table`** |
| `pos2-isb` | `off` / `table` / `est` / `est-P` / `est-L` / … |
| `pos2-gpsl2bias` | L2P–L2C：`off` / `table` / `est` |
| `pos1-l2cprior` | 观测量优先 L2P 或 L2C |
| `pos1-navsys` | 位掩码（样例 `5` = GPS+GLO） |

## 5. 接到哪步

- 要 Linux CLI / 现代 RTKLIB → [rtklib](./rtklib.md)
- 发表级坐标 / ZTD → [pride-pppar](./pride-pppar.md)；GA 工具箱 → [ginan](./ginan.md)
- 工作流 **D**：QC →（可选 Win 上 GSILIB 异机种试验）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)
- 读样例 RINEX → [georinex](./georinex.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | Linux 直接 `./gsipost_gui.exe` 失败 | PE + 缺 Wine32 | 换 Windows；或改用 [rtklib](./rtklib.md) |
| 2 | IFB 不生效 / 打不开表 | `pos3-gloifbfile=D:\…` 硬编码 | 改成本机 `gloifb.tbl` 绝对路径 |
| 3 | 把 `VER_RTKLIB 1.0.3` 当 RTKLIB 版 | 宏被改成 GSILIB 包版本 | 对外写 **GSILIB 1.0.3（based on RTKLIB 2.4.2）** |
| 4 | georinex `tlim` 早于 07:00 得 0 历元 | 样例首历元 **07:00** GPS | `tlim` 用 `2014-09-13T07:00:00` 起 |
| 5 | 与 apt RTKLIB 解差很大 | 缺 IFB/ISB/¼ 周选项 | 同 conf 语义；或接受异机种偏差 |
| 6 | ANTApp 改完要闭源分发 | ANTApp=GPL-3 | 遵循 GPL 或只用 BSD 主体（`gsipost`/`gsiplot`） |
| 7 | 期望 BDS/PPP-B2b | 包年代与目标是基线+四系统（无 B2b） | B2b → [b2blib](./b2blib.md)/[rtppp-b2b](./rtppp-b2b.md) |
| 8 | photomask 找不到 | 不在主 zip | 另下 `photomask_ver.1.1.1.zip` + `test_photomask.zip` |
| 9 | 手册英文搜不到 | 官方手册日文 | `pdftotext GSILIB_manual.pdf` 或对照 RTKLIB 2.4.2 manual |
| 10 | DLL 缺失 | 未与 exe 同目录 | 整包 `bin/` 一起拷 |
| 11 | 把 PDF 截图当本机 E2E | CI 无 GUI | 只报告已复现的 RINEX/表探针 |
| 12 | `navsys=5` 却无 Galileo | 位掩码未含 GAL | 按需改 `pos1-navsys`（见 conf 注释） |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 日本 GSI 异机种 IFB/ISB 官方参考（Win） | **本文 GSILIB** |
| Linux 通用 RTK/PPP CLI | [rtklib](./rtklib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| GA 现代化 pea/YAML | [ginan](./ginan.md) |

## 8. 相关

[rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [ginan](./ginan.md) · [georinex](./georinex.md) · [claslib](./claslib.md)（CLAS 亦源自 RTKLIB/GSILIB 系）· [data-access](../data-access.md) · [README](./README.md)

- 门户更新：2022-03-24（介绍）/ 2022-08-30（下载页；photomask 1.1.1）
- 主包历史：1.0.0（2015-01）→ 1.0.3（2016-12）→ 2017-10 版本串修正
