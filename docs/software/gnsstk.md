# GNSSTK · C++ GNSS 基础库操作手册

目录：[`PROJECTS.json` → `gnsstk`](../../PROJECTS.json) · 库 <https://github.com/SGL-UT/gnsstk> · 配套 CLI <https://github.com/SGL-UT/gnsstk-apps> · 归档前身 [GPSTk](https://github.com/SGL-UT/GPSTk) · **LGPL-3.0** · 本机：**库 v15.3.1** tip `55ea334` + **apps v15.1.1** tip `1aeb7d2` · `RinSum` BAHR → **120** 历元；`timeconvert` → GPS week **2437** · 2026-09-24 04:45 EDT · **质检复跑通过**（同 I/O，2026-09-24 04:50 EDT）

> 岗位：UT ARL/SGL 的 **C++ GNSS 核**（时间、坐标、RINEX、星历、大气延迟、PPP 数据流等）+ 可选 **gnsstk-apps** CLI。冲突时：**仓内 `INSTALL.md` / `./build.sh -h` / 本机 `RinSum --help` > 本文**。老文档里的 **GPSTk** 一律改指向本页两仓；日常 Python 读 RINEX → [georinex](./georinex.md)；QC 批处理 → [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)/[teqc](./teqc.md)。

## 1. 用途与边界

**做：**

- **库**：`CommonTime` / `CivilTime` / `GPSWeekSecond`；`Rinex3ObsStream` 读写；星历插值；对流层/电离层延迟模型；GDS 处理链（含库内 PPP 组件）
- **apps（另仓）**：`RinSum` / `RinDump` / `RinEdit` / `timeconvert` / `poscvt` / `PRSolve` / `mergeRinNav` 等
- 给自研 C++ 科研软件当底座；CLI 做 RINEX 摘要、抽列、时间换算

**不做：**

- **不是** 一键发表级 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- **不是** 厂商 RAW→RINEX 主力（TEQC 翻译器更全）→ [teqc](./teqc.md) / [autorino](./autorino.md)
- **不是** Python pandas 速读 → [georinex](./georinex.md) / [gnsspy](./gnsspy.md)
- **不是** 归档仓 GPSTk——新工程只 clone **gnsstk** + **gnsstk-apps**
- 库仓 **不含** 原 GPSTk 时代全部 apps（已拆仓）；只装库则没有 `RinSum`

一句话：GNSSTK = **C++ GNSS 底座**；要命令行摘要请再装 **gnsstk-apps**。

| 术语 | 含义 |
| --- | --- |
| GPSTk | 历史名；GitHub 仓已归档，API/文档仍常出现 |
| core / ext | `build.sh` 默认只编 core；`-e` 才加 ext（及可选 SWIG） |
| `RinSum` | apps：扫 OBS 头+历元表，验头是否 VALID |
| `Rinex3ObsStream` | 库：RINEX 2/3 OBS 流式读写类（名字带 3，仍可读 2.x） |
| SOVERSION | 本机 `libgnsstk.so.15`；主版本变了才需重编依赖方 |

## 2. 安装

### 2.1 依赖

```bash
sudo apt-get install -y build-essential cmake
# 可选：SWIG/Python 绑定（本手册冒烟未开 -e）
cmake --version   # 本机 3.31.6
g++ --version     # 本机 14.2.0
```

### 2.2 编库 → `~/.local/gnsstk`

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 -b stable https://github.com/SGL-UT/gnsstk.git
cd gnsstk
./build.sh -c -i "$HOME/.local/gnsstk" -- -DCMAKE_BUILD_TYPE=Release
# 期望末行：GNSSTk build done.
export PATH="$HOME/.local/gnsstk/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.local/gnsstk/lib:${LD_LIBRARY_PATH:-}"
ls "$HOME/.local/gnsstk/lib/libgnsstk.so"*
# 本机：libgnsstk.so.15.3.1
```

### 2.3 编 apps（CLI）

```bash
cd ~/iono_ops
git clone --depth 1 -b stable https://github.com/SGL-UT/gnsstk-apps.git
cd gnsstk-apps
# -P 指向已装库；装到同一前缀
./build.sh -c -i "$HOME/.local/gnsstk" -P "$HOME/.local/gnsstk" \
  -- -DCMAKE_BUILD_TYPE=Release
which RinSum timeconvert
# 本机 apps tip 1aeb7d2 / 标称 Ver 15.1.1；链到 lib 15.3.1 可跑
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 只有 `libgnsstk` 无 `RinSum` | 未编 apps | clone `gnsstk-apps` 并 `-P` 指库 |
| `error while loading shared libraries: libgnsstk.so.15` | 未 export `LD_LIBRARY_PATH` | `export LD_LIBRARY_PATH=$HOME/.local/gnsstk/lib:$LD_LIBRARY_PATH` |
| 仍在用 `SGL-UT/GPSTk` | 归档仓 | 改两新仓；旧脚本对照 README 迁移说明 |

## 3. 端到端（本机真跑）

### 3.1 库：时间冒烟

```bash
cd ~/iono_ops/gnsstk/examples
export GNSSTK_INSTALL="$HOME/.local/gnsstk"
export LD_LIBRARY_PATH="$GNSSTK_INSTALL/lib:$LD_LIBRARY_PATH"
g++ -O2 -I"$GNSSTK_INSTALL/include/gnsstk" -L"$GNSSTK_INSTALL/lib" \
  -o time_example_1 time_example_1.cpp -lgnsstk
./time_example_1
```

**本机摘要（2026-09-24 04:45 EDT）：**

```text
Hello world!
   The current civil time is 09/24/2026 08:45:09 UTC
   The current year is 2026
   The current day of year is 267
   The current full GPS week is 2437
   The current Modified Julian Date is 61307.364688578 UTC
```

### 3.2 库：RINEX 读历元

样例：仓内 `examples/bahr1620.04o`（RINEX 2.10，BAHR，2004-06-10 约 1 h）。

```bash
# 最小计数（自写；API 同 Rinex3ObsStream_example_1.cpp）
g++ -O2 -I"$GNSSTK_INSTALL/include/gnsstk" -L"$GNSSTK_INSTALL/lib" \
  -o rinex_count -x c++ - -lgnsstk <<'CPP'
#include <iostream>
#include "Rinex3ObsStream.hpp"
#include "Rinex3ObsHeader.hpp"
#include "Rinex3ObsData.hpp"
using namespace gnsstk;
int main(int argc, char** argv){
  Rinex3ObsStream rin(argv[1]);
  Rinex3ObsHeader head; rin >> head;
  std::cout << "marker=" << head.markerName << " ver=" << head.version << "\n";
  Rinex3ObsData data; int n=0; while (rin >> data) ++n;
  std::cout << "epochs=" << n << "\n";
}
CPP
./rinex_count bahr1620.04o
# 本机：marker=BAHR ver=2.1 epochs=120
```

### 3.3 apps：`RinSum` + `timeconvert` + `RinDump`

```bash
RinSum bahr1620.04o | head -n 40
# 期望：header is VALID；120 epochs；G05/G06/… 表

timeconvert -c "09 24 2026 08:45:00"
# 期望：FullGPSweek 2437；Year DayOfYear 2026 267；MJD 61307.364583333

RinDump bahr1620.04o G05 L1C | head -n 15
# 期望：1274 345600.000 G05 -24427464.594 …
```

**本机 `RinSum` 关键字段：** Marker `BAHR`；Rec ASHTECH Z-XII3；首历元 `2004/06/10 00:00:00`；末 `00:59:30`；**120** 历元（100%）；GPS L1C 合计 939 点。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS 2/3 | `RinSum`/`RinDump`/`Rinex3ObsStream`；头无效会直接报 |
| 时间字符串 | `timeconvert -c "MM DD YYYY HH:MM:SS"`（月日年，**非** ISO） |
| C++ `#include` | 装后在 `include/gnsstk/`；链接 `-lgnsstk` |

| 输出 | 说明 |
| --- | --- |
| `RinSum` 文本 | 头摘要 + 卫星×观测类型表 |
| `RinDump` 表 | 每行：GPS week、sow、PRN、观测值 |
| `libgnsstk.so` | 自研程序运行时依赖 |
| 不输出 | 厂商二进制翻译器全集、发表级 SINEX/STEC 产品 |

## 5. 常用参数（apps）

| 工具 / 旗标 | 作用 |
| --- | --- |
| `RinSum --obs f` | 显式指定 OBS（也可位置参数） |
| `RinSum --brief` | 缩短输出 |
| `RinSum --start` / `--stop` | 时段裁剪 |
| `RinSum --exSat G24` | 排除星/系统 |
| `RinDump <file> [sat] <oi…>` | 抽列；`oi` 如 `L1C` `C1C`；可加 `ELE`/`AZI`（需星历） |
| `timeconvert -c` / `-y` / `-f` / `-m` | 民用 / 年积日 / GPS week-sow / MJD |
| `./build.sh -e` | 编 ext（更重；日常核库可不加） |
| `./build.sh -P <prefix>` | **apps** 找已装 gnsstk |

## 6. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| Python 快速读 OBS | [georinex](./georinex.md) / [gnsspy](./gnsspy.md) |
| RINEX 手术刀 / 现代 QC | [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md) |
| 经典翻译+QC（EOL） | [teqc](./teqc.md) |
| PPP / RTK 引擎 | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [glab-upc](./glab-upc.md) |
| 观测入库前批壳 | [pinot](./pinot.md) / [autorino](./autorino.md) |

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `RinSum: command not found` | 只装了库 | 编 `gnsstk-apps` 并把 `bin` 进 `PATH` |
| 2 | 启动即缺 `libgnsstk.so.15` | 动态库路径 | `export LD_LIBRARY_PATH=$HOME/.local/gnsstk/lib:$LD_LIBRARY_PATH` |
| 3 | `timeconvert` 报 not a valid time | `-c` 格式错成 `2026,09,24,…` | 用 `"09 24 2026 08:45:00"`（月 日 年） |
| 4 | 编 apps 找不到 gnsstk | 未传前缀 | `./build.sh -P "$HOME/.local/gnsstk" -i "$HOME/.local/gnsstk"` |
| 5 | 还在 clone `GPSTk` | 仓已归档 | `git clone …/gnsstk` + `…/gnsstk-apps` |
| 6 | 期望 apps 与库小版本完全一致 | 稳定分支节奏不同 | 同 major（`.so.15`）可链；发版以各自 `ChangeLog` 为准 |
| 7 | `#include <Rinex3ObsStream.hpp>` 失败 | include 路径 | `-I$HOME/.local/gnsstk/include/gnsstk` |
| 8 | 把 `RinSum` 当 Anubis XTR | 工具定位不同 | 深度 QC → [anubis](./anubis.md)；本工具偏摘要/抽列 |
| 9 | `build.sh -e` 卡在 SWIG | Python/SWIG 版本挑剔 | 先去掉 `-e` 只编 C++；绑定另开 |
| 10 | 示例读不到 `bahr1620.04o` | 不在 `examples/` | `cd ~/iono_ops/gnsstk/examples` |
| 11 | 当 Python 包 `import gnsstk` | 未编/未装 SWIG 轮 | C++/`RinSum`；或按 `PYTHON.md` 开 `-e` |
| 12 | Debug 构建极慢/巨大 | 默认带 sanitizer 等 | Release：`-- -DCMAKE_BUILD_TYPE=Release` |

## 8. 选型

| 需求 | 选 |
| --- | --- |
| C++ 嵌 GNSS 时间/RINEX/模型 | **gnsstk（本页）** |
| CLI 扫 OBS / 抽相位列 | **gnsstk-apps**（`RinSum`/`RinDump`） |
| Python 科研读档 | [georinex](./georinex.md) |
| 厂商二进制→RINEX + 经典 QC | [teqc](./teqc.md)（EOL）或 [autorino](./autorino.md)+[anubis](./anubis.md) |
| 精密定位产品 | [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md) |

## 9. 相关

[teqc](./teqc.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [rtklib](./rtklib.md) · [glab-upc](./glab-upc.md) · [README](./README.md)
