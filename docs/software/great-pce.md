# GREAT-PCE · 武大精密卫星钟差估计（PCE）操作手册

目录：[`PROJECTS.json` → `GREAT-PCE`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-PCE> · tip **`4cefa1b`**（无 git tag；`1. 增加百度网盘地址。` 2025-05-06）· **GPL-3.0** · ★**9** · C++/CMake · 本机验证（2026-09-24 06:47–06:49 EDT）：`g++ 14.2.0` + `cmake 3.31.6` → `src/build_Linux/Bin/GREAT_PCE` **158568** B + `Lib/libLib{GREAT,Gnut}.so`（**2143176** / **6820840** B）；本地补丁 `greldelay.cpp` 加 `#include <cmath>` + `std::log` 后方能通过 g++14；`-h`/`-V 1` → **`GREAT/CLK-LSQ [0.9.0]`**（`$Rev: 2448 $`，源码编于 **Sep 24 2026 10:49:01**）；缺 XML → `xconfig: not file read … File was not found` exit **1**；`doc/GREAT_PCE.xml`（Win `\` 路径、无 OBS/SP3）空跑 → 全日 **288** 历元 `select_obs failed` / `npar = 762` @ **0.000** s，末尾 `NPDException` abort exit **134**；仅落 `great_pcelsq.app_log` **85293** B（**非** XML 写的 `xml\pcelsq.log`）；**无** `result/clk_*` / `rec_*` → **未臆造** 钟差历元；算例数据仅 OneDrive/百度网盘门禁（本机 OneDrive **403**）；仓内 `sample_data/PCE_2020100/` 只有下载地址 txt

> 岗位：**精密卫星钟差估计（PCE）**（多星座双频无电离层组合；整体 LSQ / 仿实时 EPO）→ 服务轨道钟差产品链与 PPP。冲突时：**本机 `GREAT_PCE -h` / `doc/GREAT_PCE.xml` / `doc/GREAT_PCE_1.0.pdf` / 上游 README > 本文**。  
> 同链 UPD → [great-upd](./great-upd.md)；IFCB → [great-ifcb](./great-ifcb.md)；多 AC 钟差合成 → [clkcomb](./clkcomb.md)；产品门户 → [data-access](../data-access.md)「SP3 / CLK / bias」。下游 PPP → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)。**≠** [cube](./cube.md)（APM 钟差/PPP-AR）。

## 1. 用途与边界

**做：**

- 多 GNSS（**GPS / GLONASS / Galileo / BDS-2/3**）**精密卫星钟差**估计（双频无电离层组合 `IONO_FREE`）
- XML 驱动 CLI：`GREAT_PCE -x CONFIG.xml`；源码 CMake（LibGREAT + LibGnut + 捆 Eigen/zlib/pugixml/newmat）
- 两种估计模式：`<process lsq_mode="LSQ">` 整体解 / `"EPO"` 仿实时逐历元（PDF §7.1）
- 用户手册 `doc/GREAT_PCE_1.0.pdf`（**1250600** B）；模板 `doc/GREAT_PCE.xml`（**134** 站日网示例）

**不做：**

- **不是** UPD/WL/NL → [great-upd](./great-upd.md)；**不是** IFCB → [great-ifcb](./great-ifcb.md)
- **不是** PPP/PPP-AR 解算 → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)
- **不是** 多 AC 钟/偏差合成 → [clkcomb](./clkcomb.md)；也**不是** POD 主引擎（`GREAT_PODFLT` 另仓）
- GitHub tip **不带**可跑算例包（仅网盘链接）→ **禁止**拿空跑日志当真 CLK 产品
- 本机**未**自产全日网观测/精密轨道（OneDrive **403**；百度需交互；CDDIS 需 Earthdata）

一句话：**GREAT-PCE = 武大 GREAT 开源精密卫星钟差估计器**（与 UPD/IFCB 同产品链、估钟本体）。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** GREAT-PCE | 精密钟差估计 CLI | `GREAT_PCE -x …xml` → `clk_*` / `rec_*` |
| [great-upd](./great-upd.md) | UPD WL/EWL/NL | `GREAT-UPD -x …` → `upd_*` |
| [great-ifcb](./great-ifcb.md) | IFCB 频间钟差 | `GREAT-IFCB -x …` → `ifcb_*` |
| [clkcomb](./clkcomb.md) | 多 AC 钟/偏差合成 | `clkcomb comb.ini` |
| [cube](./cube.md) | APM 钟差/PPP-AR | Win+MKL；Linux 难编 |
| Gkit-Bias（长安） | DCB/UPD/IFCB→OSB | 另仓；本目录暂无篇 |
| 官方 IGS/分析中心 CLK | 现成产品 | CDDIS；本工具自产 `clk_*` |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++` + `cmake`≥3.0 + GNU `make` | 源码编译（本机采用；PDF 写 cmake3） |
| 捆在 `src/third-party/Eigen` | Linux 默认路径，无需另装 Eigen |
| OneDrive/百度算例包（可选） | `sample_data/PCE_2020100/`；见 §3.3 |
| CDDIS Earthdata / WHU（可选） | 自备网观测+SP3；见 [data-access](../data-access.md) |

### Linux 源码（本机已通；推荐）

```bash
sudo apt install -y build-essential cmake   # 本机已有 g++ 14.2.0 / cmake 3.31.6
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GREAT-WHU/GREAT-PCE.git
cd GREAT-PCE
git rev-parse --short HEAD   # 本机：4cefa1b

# g++14：greldelay.cpp 缺 cmath（否则 make 报 ‘log’ was not declared）
# 本机补丁（勿回推上游除非自提 PR）：
#   #include <cmath>  +  std::log(...)
sed -i '12a #include <cmath>' src/LibGnut/gmodels/greldelay.cpp
sed -i 's/ \* log(/ * std::log(/' src/LibGnut/gmodels/greldelay.cpp

cd src && mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)              # 产物在 ../build_Linux/（非 build/）
ls -la ../build_Linux/Bin/GREAT_PCE   # 本机：158568 B
# RPATH 已写 ${ORIGIN}/../Lib；或显式：
export LD_LIBRARY_PATH="$PWD/../build_Linux/Lib:${LD_LIBRARY_PATH:-}"
../build_Linux/Bin/GREAT_PCE -h
```

**本机 `-h`：**

```text
GREAT/CLK-LSQ [0.9.0] compiled: Sep 24 2026 10:49:01 ($Rev: 2448 $)

Usage: 

    -h|--help              .. this help                          
    -V int                 .. version                            
    -v int                 .. verbosity level                    
    -x file                .. configuration input file           
    --                     .. configuration from stdinp          
    -l file                .. log output file                    
    -X                     .. output default configuration in XML
```

可执行文件名是 **`GREAT_PCE`（下划线）**，不是 `GREAT-PCE`。仓内**无**预编译 `bin/Linux/`（与 [great-ifcb](./great-ifcb.md)/[great-upd](./great-upd.md) 不同）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `'log' was not declared` @ `greldelay.cpp` | g++14 + 缺 `<cmath>` | 加 `#include <cmath>` 与 `std::log` |
| `error while loading shared libraries: libLibGREAT.so` | 未走 RPATH/`LD_LIBRARY_PATH` | 从 `Bin/` 调，或 `export LD_LIBRARY_PATH=…/build_Linux/Lib` |
| `-x` 缺文件 exit **1** | `xconfig: not file read … File was not found` | 改路径 |
| 无真数据仍扫全日历元后 abort | `select_obs failed` → `NPDException` | 见 §3.2；**勿当成功** |
| 产物目录找不到 | 相对 **cwd**；且须先有样例树 | 在 `PCE_2020100/` 下跑 |

## 3. 端到端（本机真跑）

### 3.1 帮助 / 缺配置

```bash
export LD_LIBRARY_PATH=~/iono_ops/GREAT-PCE/src/build_Linux/Lib
BIN=~/iono_ops/GREAT-PCE/src/build_Linux/Bin/GREAT_PCE
$BIN -h                 # GREAT/CLK-LSQ [0.9.0] …  ；exit 0
$BIN -V 1               # 同上版本行  ；exit 0
$BIN -x /tmp/no_such_pce.xml
# → xconfig: not file read /tmp/no_such_pce.xml File was not found  ；exit 1
$BIN -X | head           # 倾倒默认 XML 骨架（gen/inputs/outputs/rec…） ；exit 0
```

### 3.2 缺样例输入的空跑（**陷阱**；本机真跑）

GitHub tip **没有**可跑的 `obs/`/`gnss/`/`model/`。用仓内 `doc/GREAT_PCE.xml`（Win `\` 分隔、指向 `obs\*.20o` / `gnss\com2100*.sp3` 等）在空目录跑：

```bash
rm -rf /tmp/great-pce-smoke && mkdir -p /tmp/great-pce-smoke && cd /tmp/great-pce-smoke
cp ~/iono_ops/GREAT-PCE/doc/GREAT_PCE.xml .
$BIN -x GREAT_PCE.xml
# stderr/stdout 含：
#   Error: Exception opening file gnss\com21003.sp3: std::exception
#   … Incomplete header identified. .. gnss\com21003.sp3
#   （OBS/ATX/NAV/DCB/… 同理；本机 Exception opening ×292）
#   Finish epoch 2020-04-09 00:00:00[GPS]: 0.002 … npar = 762
#   …（全日 288 历元，多数 0.000 s / select_obs failed）
#   Finish epoch 2020-04-09 23:55:00[GPS]: 0.000 … npar = 762
#   terminate called after throwing an instance of 'NPDException'
# exit 134（SIGABRT）
ls -la                    # GREAT_PCE.xml + great_pcelsq.app_log 85293 B + 空 tempfile_*
# 无 result/、无 xml/、无 clk_* / rec_*
tail -3 great_pcelsq.app_log
# → ###COMBINE_EQU  0.000 sec.
# → reference clock not valid: PTBB
```

**判据：** 有效产品应落在 `<outputs><satclk>` / `<recclk>`（样例名 `result/clk_2020100`、`result/rec_2020100`），且含钟差历元行（PDF §7.2 / IGS CLK 惯例）。**无这些文件 + abort = 失败**，尽管扫完了 288 个历元。XML 写 `<log> xml\pcelsq.log </log>`，本机实际主日志为 cwd **`great_pcelsq.app_log`**（源码硬编码 mask）。

### 3.3 官方算例路径（网盘；本机未跑）

`sample_data/PCE_2020100/PCE算例下载地址.txt`：

- OneDrive：`https://1drv.ms/u/c/afd61bb364b8e566/…` 密码 **`GREAT-PCE`**（本机 `curl` 跟到 live.com → **403**）
- 百度：`pan.baidu.com/s/1ZKAkIB1DFsWdGuLInlv9zg` 提取码 **`ibxa`**

解压后期望树：`gnss/` `obs/` `model/` `xml/` `result/` `log_tb/`（PDF 表 6.1）。Linux 须把 XML 里的 **`\` → `/`**（PDF §5.2）。

```bash
# 预期（有网盘包时；本机无包未执行）：
cd …/sample_data/PCE_2020100
# 编辑 xml/*.xml：路径分隔符改为 /
export LD_LIBRARY_PATH=…/src/build_Linux/Lib
…/src/build_Linux/Bin/GREAT_PCE -x xml/….xml
# 期望：result/clk_2020100、result/rec_2020100 非空；对照包内 result（若有）
```

### 3.4 自备数据（本机未拉）

PDF 表 5.1–5.2：RINEXO/N、SP3、SINEX、DCB、ATX、DE405、oceanload、poleut1。拉取见 [data-access](../data-access.md)。本机**未**用 CDDIS/WHU 新产品重跑全日 PCE。

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | XML | `<gen>` 时窗/`sys`/`rec`/`int`/`est`；`<receiver>` 坐标；`<gps|glo|gal|bds>`；`<process …>`；`<inputs>`；`<outputs>` |
| 入 | RINEX OBS | `<rinexo>`；RINEX 2.10–3.05（PDF） |
| 入 | RINEX NAV | `<rinexn>`（样例 `brdm1000.20p`） |
| 入 | SP3 | `<sp3>`（固定轨道估钟） |
| 入 | SINEX / DCB / ATX / BLQ / DE / poleut1 / leapsecond | 站坐标、偏差、天线、潮汐、行星历、EOP |
| 出 | `clk_YYYYDOY`（`<satclk>`） | 卫星钟差（PDF §7.2；IGS CLK 风格） |
| 出 | `rec_YYYYDOY`（`<recclk>`） | 接收机钟差 |
| 出 | 日志 | 本机 cwd **`great_pcelsq.app_log`**（≠ XML `xml\pcelsq.log` 字面） |

**无样例包时禁止抄写臆造 CLK AS/AR 行。**

## 5. 参数（XML / CLI）

| 键 / 旗标 | 本机样例（`doc/GREAT_PCE.xml`） | 含义 |
| --- | --- | --- |
| `-x file` | `GREAT_PCE.xml` | 配置（缺文件 exit 1） |
| `-h` / `-V` / `-X` | — | 帮助 / 版本 / 默认 XML 骨架 |
| `-v` / `-l` | — | 详细度；另路日志 |
| `<beg>`/`<end>`/`<int>` | 2020-04-09 全日 / **300** s | 时窗与采样 → 空跑 **288** 历元 |
| `<sys>` | `GPS GLO GAL BDS` | 多系统 |
| `<rec>` | **134** 站（ABMF…ZIM3） | 4 字符大写 |
| `<est>` | `LSQ` | 估计器标签 |
| `lsq_mode` | `LSQ`（可改 `EPO`） | 整体 vs 仿实时 |
| `obs_combination` | `IONO_FREE` | 无电离层组合 |
| `ref_clk` / `sig_ref_clk` | `PTBB` / `0.001` | 参考钟（空跑报 `reference clock not valid`） |
| `minimum_elev` | `7` | 截止高度角 ° |
| `slip_model` | `turboedit` | 周跳 |
| `<outputs><satclk>` | `result\clk_2020100` | 相对 **cwd**；Linux 改 `/` |

`-X` 默认骨架**不含**完整 `<process>`/`<satclk>`/`<sp3>`——勿当生产模板；用 `doc/GREAT_PCE.xml` 或网盘 `xml/`。

## 6. 接到哪一步

```text
[data-access] 拉全球网 OBS + 混合 NAV + SP3 + SINEX + DCB + ATX + 模型文件
        ↓
  GREAT-PCE  →  clk_YYYYDOY / rec_YYYYDOY
        ↓
  （可选）clkcomb 多 AC 综合 / UPD·IFCB 并行偏差链
        ↓
  great-pvt / pride-pppar / ginan / ppp-wizard
```

钟差产品消费端见 [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)；偏差链见 [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)。PCE **不**替代 TEC/GIM。

## 7. 坑（≥8）

1. **算例在网盘不在 Git**：tip 仅 txt 链接；OneDrive 本机 **403**；百度需交互——无包勿指望出 CLK。
2. **空输入扫全日后 `NPDException` exit 134**：288 历元 `npar=762` 全零秒 ≠ 成功；必须以 `result/clk_*` 验收。
3. **`great_pcelsq.app_log` 名不实**：XML 写 `xml\pcelsq.log`，本机落 cwd 硬编码 app log；且**未**自动建 `xml/`/`result/`。
4. **Win `\` 路径**：`doc/GREAT_PCE.xml` 含 **149** 处反斜杠；Linux 须改 `/`（PDF 明示）。
5. **`g++14` `greldelay.cpp`**：缺 `<cmath>` 编不过——本机已记补丁。
6. **二进制名 `GREAT_PCE`**：下划线；产物在 `src/build_Linux/` 不在 `build/`。
7. **`LD_LIBRARY_PATH` / RPATH**：`libLibGREAT.so` + `libLibGnut.so`；从 `Bin/` 调可走 `${ORIGIN}/../Lib`。
8. **参考钟 `PTBB`**：空跑末尾 `reference clock not valid: PTBB`——真跑须保证该站/星在网且有观测。
9. **≠ UPD ≠ IFCB ≠ clkcomb**：PCE 估钟；UPD/IFCB 估相位/频间偏差；clkcomb 综合多 AC。
10. **规模门禁**：模板 **134** 站 × 多系统 × 300 s——缺内存/线程时先砍 `<rec>` / 改 `num_threads`。
11. **`-X` 骨架过简**：缺生产级 inputs/outputs；用 doc 或网盘 XML。
12. **Cube / Gkit-Bias**：Cube 已有篇；Gkit-Bias（DCB/UPD/IFCB→OSB）另仓暂无手册。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 自建多星座 **精密钟差** | **GREAT-PCE** | 专用 PCE；有 PDF/XML |
| 自建 **UPD**（WL/EWL/NL） | [great-upd](./great-upd.md) | 同 GREAT 链；样例可复现 |
| 自建 **IFCB** | [great-ifcb](./great-ifcb.md) | 三频频间钟差 |
| 多 AC 钟/偏差合成 | [clkcomb](./clkcomb.md) | CLK/BIA 综合 |
| 武大 GREAT PPP | [great-pvt](./great-pvt.md) | 消费钟差/偏差 |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) | 消费 OSB/UPD/CLK |
| DCB/UPD/IFCB→OSB 一体 | Gkit-Bias（待手册） | 长安实现；对照用 |
| 只要分析中心 CLK | [data-access](../data-access.md) | 不必自估 |
| APM 钟差/DCK | [cube](./cube.md) | Win+MKL |

**下一步候选（目录仍缺短硬）：** `Gkit-Bias`（DCB/UPD/IFCB→OSB；`PROJECTS.json` featured）；**great-upd / great-ifcb / clkcomb / 本文已有**——勿重复；勿抢 `galileo-nequick-g` / `ionex` WIP。
