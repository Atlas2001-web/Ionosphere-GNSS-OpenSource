# Cube · 精密测量院 GPS 钟差/DCK + PPP-AR 操作手册

目录：[`PROJECTS.json` → `Cube`](../../PROJECTS.json) · 上游 <https://github.com/liush18/Cube> · tip **`cfec2cc`**（`cube 1.0`；2021-10-19；**无 tag**）· 许可 **BSD-2-Clause**（继承 RTKLIB；头注 APM/CAS）· ★**30** · C · 本机验证（2026-09-24 06:36–06:37 EDT）：源 **98**×`.c` + **11**×`.h`；PDF **826097** B；`data/apm21440.list` **70** 站 / `apm21440_ppp.list` **145** 行（路径皆 `F:\…`）；Linux 试编（`-DEXPORT=`、无 `WIN32`/`MKL`）**30** OK / **68** FAIL——主因头文件 `base\base.h` 反斜杠（**16+**）及 POSIX/`dirent`；**无样例 OBS/SP3/CLK 落盘 → 未跑网解/PPP stdout，不臆造钟差/固定率**

> 岗位：**服务端** GPS 钟差 / 解耦钟（DCK）估计 + **用户端** IF PPP / IRC·DCK PPP-AR（RTKLIB 二次开发）。冲突时：**上游 README / `doc/Cube Users Guide_1.0.pdf` / `script/*.conf` > 本文**。  
> **勿与** 本目录 [rtklib](./rtklib.md)/[rtklib-explorer](./rtklib-explorer.md)/[mrtklib](./mrtklib.md)/[pyrtklib](./pyrtklib.md) 混改——Cube 是独立 fork 仓。多 AC 钟差合成 → [clkcomb](./clkcomb.md)；武大 UPD → [great-pvt](./great-pvt.md)（GREAT-UPD 另篇）；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)。

## 1. 用途与边界

**做：**

- **Network（`pos1-posmode=net`）**：无差 IF 钟差；可选 **SCB**；**DCK**（`cmn-dck=on`）
- **User PPP**：IF PPP；PPP-AR（IRC / DCK）；输出坐标、ZTD、模糊度、残差等格式化文件
- 配置：`script/conf_net.conf` / `conf_ppp.conf`；批跑壳 `server.py` / `user.py`（硬编码 `Cube.exe`）
- 站表模板：`data/apm21440*.list`（GPS 周 **2144** / DOY **038** 风格路径）

**不做：**

- **不是** 开箱 Linux/macOS 二进制——官方实验平台 **Windows + VS2019**；网解依赖 **Intel MKL**
- **不是** 多星座——README/PDF：**仅 GPS** 伪距+相位
- **不是** 仓内带 RINEX/SP3/CLK 样例——`data/` 只有 list；产品路径写死 `F:\products\…`
- **不是** 官方 IGS 钟差产品本身；亦非 [clkcomb](./clkcomb.md) 多 AC 加权合成
- 本机 **不能** 提供钟差残差/固定率数字——未链出可执行文件、无观测落盘

一句话：Cube = **APM/CAS 基于 RTKLIB 的 GPS 钟差（含 DCK）与 PPP-AR 研究代码**；Linux CI 通常止于源码/PDF/配置探活。

| 术语 | 含义 |
| --- | --- |
| DCK | Decoupled Clock；`cmn-dck=on` → `dckPost` / `userPostPos_dp` |
| IRC | Integer-Recovered Clock（用户端 PPP-AR） |
| SCB / RCB | 卫星/接收机码偏差开关（`-scb`/`-rcb`） |
| `Cube.exe` | 官方入口；`main.c` 无参时 `system("pause")`（Win） |

## 2. 获取 / 官方安装（Windows）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/liush18/Cube.git
cd Cube && git rev-parse --short HEAD   # cfec2cc
ls src script data doc
# 98 .c / 11 .h；Users Guide 826097 B
```

按 PDF §3（VS Community 2019）：

1. 新建工程，拷入 `src/`，Additional Include = `.\src`
2. Character Set = **Multi-Byte**；预处理器：`_CRT_SECURE_NO_WARNINGS` `WIN32`（网解再加 `MKL`）
3. 链接：`winmm.lib` `ws2_32.lib`；网解启用 **Intel MKL Parallel**
4. 产物习惯名 **`Cube.exe`**（`script/*.py` 亦如此调用）

### Linux 本机试编（诚实失败）

```bash
# 仅探活：清空 EXPORT=__declspec，不定义 WIN32/MKL
mkdir -p build_linux && cd build_linux
printf '%s\n' '#undef EXPORT' '#define EXPORT' > export_fix.h
# 对全部 98 个 .c：gcc -c -I../src -include export_fix.h …
# 本机：ok=30 fail=68；未链接出 Cube
```

| 失败类（本机） | 含义 |
| --- | --- |
| `#include "base\base.h"` | Win 反斜杠路径；Linux 需改 `/` 或统一 include |
| `DIR` / `gettimeofday` | 非 WIN32 分支缺 `dirent.h`/`sys/time.h` 等 |
| 其余网解/user 连锁 | 上头失败后无法继续 |

**结论：** 上游声明「C 易移植」，但 **当前 tip 未提供 Makefile/CMake**；移植需改 include 分隔符 + POSIX 头 +（网解）MKL/LAPACK。本手册不提供半成品补丁包。

## 3. 配置与数据布局（仓内真值）

### 3.1 网解 `conf_net.conf`（节选本机）

| 键 | 样例值 | 含义 |
| --- | --- | --- |
| `pos1-posmode` | `net` | 网解 |
| `cmn-dck` | `on` | DCK |
| `net-estclk` | `on` | 估卫星钟 |
| `net-week`/`net-dow` | `2144` / `0` | GPS 周/日内 |
| `file-obsfile` | `F:\%Y\%n\apm%W%D.list` | 站表 |
| `file-sp3file` | `F:\products\%W\igs%W%D.sp3` | IGS SP3 |
| `file-atxfile` | `F:\products\igs14_2118.atx` | ANTEX |

### 3.2 用户 PPP `conf_ppp.conf`

| 键 | 样例值 |
| --- | --- |
| `pos1-posmode` | `ppp-kine` |
| `pos2-armode` | `on` |
| `net-estclk` | `off`（用外部钟） |
| `file-clkfile` | `F:\products\%W\apm%W%D.clk`（自产或 IGS） |
| `file-obsfile` | `F:\%Y\%n\apm%W%D_ppp.list` |

### 3.3 站表

```bash
wc -l data/apm21440.list data/apm21440_ppp.list
# 70 / 145
head -1 data/apm21440.list
# F:\2021\038\21o\NRC100CAN_R_20210380000_01D_30S_MO.21o
```

PDF Table 1：站基准可配（例 **NRC1**）；CODE P1-C1 DCB；IGS 最终轨道/ERP；对流层随机游走 ~**1e−7 m²/s** + NMF。

### 3.4 批跑壳（Win 路径）

```text
# script/server.py
Cube.exe -conf conf_net.conf -week %04d -dow %d

# script/user.py
Cube.exe -conf conf_ppp.conf -ts YYYY/MM/DD 00:00:00 -te YYYY/MM/DD 23:59:30
```

CLI 另认：`-inh`/`-rcb`/`-scb`/`-obs`/`-clk`/`-eratio1`（见 `src/main.c`）。

## 4. 端到端（本机边界）

| 步骤 | 本机结果 |
| --- | --- |
| clone tip `cfec2cc` | OK |
| 清点源码 98/11、PDF、list 70/145 | OK |
| 读 `conf_*.conf` / `main.c` 开关 | OK |
| VS+MKL 出 `Cube.exe` | **未跑**（无 Windows 工具链） |
| 网解/PPP 数值 stdout | **未跑**（无 OBS/产品；**不臆造**） |

## 5. 坑

1. **无 Linux 开箱** —— 反斜杠 include + Win API + MKL；勿期望 `make && ./Cube`。
2. **`data/` 非数据** —— 仅 list；须自备 RINEX3 日文件与 IGS SP3/ERP/ATX/DCB。
3. **`F:\` 盘符** —— conf/list/py 全是作者机器路径；移植先全局替换。
4. **仅 GPS** —— 多星座需求改用 [great-pvt](./great-pvt.md)/[ginan](./ginan.md)/[pride-pppar](./pride-pppar.md)。
5. **与 rtklib 族页隔离** —— 勿把 Cube 补丁写进 [rtklib](./rtklib.md) 正文。

## 6. 与相近工具

| 需求 | 选 |
| --- | --- |
| 通用 RTK/PPP CLI | [rtklib](./rtklib.md) |
| 多 AC 钟差加权合成 | [clkcomb](./clkcomb.md) |
| 武大精密 PVT / UPD 链 | [great-pvt](./great-pvt.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| Win 异机种基线（GSI） | [gsilib](./gsilib.md) |
| 本仓 | GPS 钟差/DCK 算法研读（Win+MKL） |

## 7. 本机未跑 / 边界

- **未** 安装 Intel MKL / Visual Studio
- **未** 下载 list 所指 2021 DOY 038 观测与 `igs21440.sp3`
- **未** 产出 `.clk` / ZTD / 模糊度文件——故无残差表

## 8. 参考

- 上游 <https://github.com/liush18/Cube>
- `doc/Cube Users Guide_1.0.pdf`
- 交叉：[clkcomb](./clkcomb.md) · [great-pvt](./great-pvt.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [ginan](./ginan.md) · [gsilib](./gsilib.md) · [groops](./groops.md) · [data-access](../data-access.md)
