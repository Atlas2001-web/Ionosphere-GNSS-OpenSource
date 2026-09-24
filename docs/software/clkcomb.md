# clkcomb · 多 GNSS 钟差/相位偏差合成操作手册

目录：[`PROJECTS.json` → `clkcomb`](../../PROJECTS.json) · 上游 <https://github.com/YuanxinPan/clkcomb> · tip **`2ee1d3c`**（无 tag；`master`）· **BSD-3-Clause** · ★**3** · C++11 · 本机验证（2026-09-24 06:32–06:33 EDT）：`g++ 14.2.0` + `make` → `bin/clkcomb` **6070552** B；`example/` GPS 浮点合成 exit **0**；`cmb20863.clk` **7372807** B/**92160** 行 = `example/output/`（`cmp`/`sha256` 齐）；iter#3 权 **cod 23.56% / emr 9.91% / esa 14.06% / gfz 15.03% / grg 18.81% / jpl 18.63%**；AS G01 首历元 **−2.479022980922E−04**；`plot_clkdif.sh` 因缺 `python` 命令未出图（本机仅 `python3`+matplotlib **3.10.1**）；**未臆造** 相位钟/BIA 合成 stdout；CDDIS/`download.sh` **Earthdata 门禁**未下新日

> 岗位：**多分析中心（AC）精密钟差（+可选相位偏差）加权合成** → 综合 CLK/CLS/DIF。冲突时：**上游 README / `comb.ini` 注释 / 源码 > 本文**。  
> 闭源定位引擎 → [PPPx_bin](https://github.com/YuanxinPan/PPPx_bin)（**不在本条目**）。下游 PPP-AR → [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)/[ginan](./ginan.md)/[ppp-wizard](./ppp-wizard.md)；产品门户 → [data-access](../data-access.md)「SP3 / CLK / bias」。

## 1. 用途与边界

**做：**

- 读多 AC 的 **SP3 + CLK**（可选 **BIA / ATT / SNX / BRDC**），按 `comb.ini` 做钟差（+相位偏差）组合
- 写综合 **`cmbWWWWD.clk`**、摘要 **`.cls`**、逐星差 **`.dif`**、过程 **`.log`**
- 仓内 `scripts/download.sh`：按年积日拉 CDDIS/镜像产品（**需账号**，见下）
- 仓内 `scripts/plot_clkdif.sh`：对 `.dif`/`.log` 出 PNG（依赖 `python`+matplotlib）
- 可选 `bin/att`、`make -C src/utils` → `*2snx`（站钟/偏差转 SINEX 辅助；本手册主路径不覆盖）

**不做：**

- **不是** PPP/PPP-AR 解算引擎 → [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)/[ginan](./ginan.md)
- **不是** 官方 IGS 综合产品本身（输出前缀默认 `cmb`，自研综合）
- **不是** 实时 SSR/NTRIP 播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)/[haslib](./haslib.md)
- **不** 自带 Earthdata 凭证；无 `products/` 或次日 SP3 → 直接 `error:` 退出
- 本机 **未跑** `phase clock = true`（example 无 `.bia`）→ **不臆造** 相位钟/BIA 输出

一句话：**离线多 AC 钟差/偏差合成器**；电离层产品链在「综合 CLK → PPP」之后，本工具不产 TEC。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** clkcomb | 开源合成 CLI | `./bin/clkcomb comb.ini` |
| PPPx | 同作者闭源定位 | 二进制包；**禁止**当本仓功能 |
| IGS 最终 CLK | 官方综合产品 | CDDIS `igsWWWWD.clk*`；本工具可读为参考轨道 AC |
| [groops](./groops.md) | 重力/GNSS 网解框架 | XML 流水线；可写钟，≠本 CLI |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++`（C++11）+ GNU `make` | 必需 |
| `unzip` | example `products.zip` |
| `python` → matplotlib（可选） | `plot_clkdif.sh`（脚本查的是 **`python`**，不是 `python3`） |
| Earthdata / CDDIS 凭证（可选） | `scripts/download.sh` 拉新产品 |

### Linux（本机已通）

```bash
sudo apt install -y build-essential make unzip   # 本机已有 g++ 14.2.0
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/YuanxinPan/clkcomb.git
cd clkcomb
git rev-parse --short HEAD   # 本机：2ee1d3c
make                         # → bin/clkcomb、bin/att、bin/libmods.a
ls -la bin/clkcomb           # 本机：6070552 B
./bin/clkcomb a b            # → usage clkcomb [comb.ini]  ；exit 1
```

Windows：上游 `src/vc++/clkcomb.sln`（VS≥2013）；**官方未测**，本机未编。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `read_config: no such file: -h` | **无** `-h`/`--help`；参数当 ini 路径 | 用 `comb.ini`；多参打印 `usage` |
| 根目录裸跑缺 `./products/` | 默认读 cwd `comb.ini` | 进 `example/` 或改 `path` |
| `plot_clkdif.sh` → `python3 (with matplotlib) needs…` | 脚本测 `python -V`，Debian 常无 `python` | `sudo apt install python-is-python3` 或改脚本调用 `python3` |

## 3. 端到端（本机真跑；2026-09-24 06:32 EDT）

### 3.1 官方 example（GPS 浮点；推荐首跑）

上游 README 写 `cd example/clkcomb/`——**仓库实际是 `example/`**（无嵌套 `clkcomb/`）。

```bash
cd ~/iono_ops/clkcomb/example
[ ! -d products ] && unzip products.zip
# products/：21 文件；cod/emr/esa/gfz/grg/jpl/igs × clk+sp3，另各 AC 次日 *20864.sp3；≈132 M
../bin/clkcomb comb.ini
```

**本机实跑 stdout（节选）：**

```text
===============start of config===============
[session]
time    : 2086 3 (GPSWeek)
length  : 86370
interval: 30
...
system   : G
...
name:  cod emr esa gfz grg jpl
combined orbit: igs
...
================end of config================
(…) read products of igs...
(…) read products of cod...
…
    constellation:    1
    satellite    :   32
    epoch        : 2880
(…) align clock datum...
(…) construct reference clock...
    reference AC: jpl
    null: G04 -> cod
(…) iterative combination...
(…) iter #1...
    weight: cod  16.67%
    …
(…) iter #3...
    weight: cod  23.56%
    weight: emr   9.91%
    weight: esa  14.06%
    weight: gfz  15.03%
    weight: grg  18.81%
    weight: jpl  18.63%
(…) write cls file...
    -> cmb20863.cls
(…) write clk file...
    -> cmb20863.clk
```

**本机产物：**

| 文件 | 大小 / 行 | 核对 |
| --- | --- | --- |
| `cmb20863.clk` | **7372807** B / **92160** 行 | `cmp` = `output/cmb20863.clk`；sha256₁₂=`cbc64b862c58` |
| `cmb20863.cls` | **4064** B / **91** 行 | `cmp` = ref；权表 cod **23.56%** |
| `2020-001.log` | **63993** B / **2568** 行 | 历元计数表 + iter |
| `2020-001.dif` | **16035840** B / **552960** 行 | `satclk <ac> <PRN> <epo> <ns>` |

CLK 头摘录（本机）：

```text
AS G01  2020 01 01 00 00  0.000000  2   -2.479022980922E-04  4.842866254529E-12
```

### 3.2 可视化（本机未出图）

```bash
bash ../scripts/plot_clkdif.sh 2020-001.dif 2020-001.log
# 本机：python3 (with matplotlib) needs to be installed  → exit 1（无 `python` 命令）
# 修复后可对照 example/output/G*.png（仓内预置；非本机新绘）
```

### 3.3 缺产品 / 用法门禁（真报错）

```bash
# 仓库根、无 products/：
./bin/clkcomb
# …print config… → error: RinexSp3::read: no such file: ./products/igs20863.sp3  ；exit 1

./bin/clkcomb -h
# error: read_config: no such file: -h  ；exit 1

./bin/clkcomb a b
# usage clkcomb [comb.ini]  ；exit 1
```

### 3.4 拉新产品（门禁）

```bash
bash scripts/download.sh          # 打印 Usage；opt 0–3（浮点/固定 × GPS/GNSS）
bash scripts/download.sh 2020 1 0 # 需 CDDIS/Earthdata；HOST 默认 ftps://gdc.cddis.eosdis.nasa.gov
```

本机**无 Earthdata** → **未执行真实下载、未臆造新产品文件名列表**。开放镜像与账号坑见 [data-access](../data-access.md)「SP3 / CLK / bias」与「CODE / GFZ / CAS」；脚本内文件名偏 **短名** `acWWWWD.clk`，MGEX 长名分支另见脚本 `DownloadGNSS*`。

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | `comb.ini` | 会话、星座、AC 列表、路径模板 |
| 入 | `*_WWWD.sp3` / `.clk` | 各 AC；**参考轨道** AC（例 `igs`）亦需 SP3 |
| 入 | 次日 `*WWWD+1.sp3` | README：当日 SP3 无 24:00 历元时需要；example 已捆 `*20864.sp3` |
| 入 | `.bia` / `.att` / `.snx` / BRDC | 仅当 `phase clock` / `use att` / `combine staclk` / `align brdc` 打开 |
| 入 | `table/igs14.atx`（或 `cod.atx`） | PCO；example 指 `../table/igs14.atx` |
| 出 | `_PREFIX__WEEK__DOW_.clk` | 综合钟；RINEX CLK；例 `cmb20863.clk` |
| 出 | `.cls` | 权 + 相对综合均值（ps） |
| 出 | `_YEAR_-_DOY_.dif` / `.log` | 差分序列 / 过程 |

占位符：`_WEEK_` `_DOW_` `_YEAR_` `_YR_` `_DOY_` `_PREFIX_`（见 ini 注释）。

## 5. 参数（`comb.ini`）

| 节 / 键 | 本机 example | 含义 |
| --- | --- | --- |
| `[session] date` | `2020 001` | 年 + DOY → GPS 周 **2086** 星期 **3** |
| `length` / `interval` | `86370` / `30` | 秒；历元数 = length/interval+1 → **2880** |
| `[constellation] system` | `G`（根 ini 为 `GEC`） | 启用系统字母 |
| `prn` / `exclude` | G01–G32 等 | 参与/排除卫星 |
| `[ac] name` | `cod emr esa gfz grg jpl` | 参与合成的 AC |
| `combined orbit` | `igs` | 钟差归算用的参考轨道产品前缀 |
| `weight method` | `ac` | `ac` 或 `satellite` |
| `[product] path` | `./products/` | 产品目录 |
| `phase clock` | `false` | `true` 时读 bia、做相位钟/偏差合成 |
| `combine staclk` / `use att` | `false` | 站钟 / 姿态改正开关 |
| `*_pattern` | `_PREFIX__WEEK__DOW_.clk` 等 | 文件名模板 |
| `[table] atx` | `../table/igs14.atx` | ANTEX |
| `[output] product prefix` | `cmb` | 输出 AC 名 |
| `align brdc` | `false` | 是否对齐广播钟基准 |
| `cls`/`dif`/`log` pattern | 见 ini | 输出名 |

CLI：**唯一**实参 = ini 路径；省略则读 cwd `comb.ini`。

## 6. 接到哪一步

```text
[data-access] CDDIS/CODE/GFZ/CAS 拉 SP3+CLK(+BIA)
        ↓
   clkcomb comb.ini  →  cmb*.clk / .cls / .dif
        ↓
  pride-pppar / great-pvt / ginan / ppp-wizard / rtklib PPP
        ↓
   坐标 / ZTD / 固定率（本工具不产出）
```

电离层：综合钟改善 PPP 后处理；**不**替代 [pytecgg](./pytecgg.md)/GIM。理论见仓内 `doc/Pan_MSc_Thesis_2021.pdf` 与 README 论文列表（Geng et al. 2024 等）。

## 7. 坑（≥8）

1. **无 `-h`**：`-h`/`--help` 被当成 ini → `no such file`；多参才打印 `usage clkcomb [comb.ini]`。
2. **README 路径笔误**：写 `example/clkcomb/`，实为 **`example/`**。
3. **次日 SP3**：缺 `*WWWD+1.sp3` 且当日无 24:00 → 读轨道失败（example 已备 `20864`）。
4. **短名模板**：默认 `_PREFIX__WEEK__DOW_.clk`；MGEX 长名需改 pattern 或先改名；`download.sh` GNSS 分支用长名。
5. **CDDIS 门禁**：`download.sh` → Earthdata/FTPS；无账号勿臆造落盘。开放源见 [data-access](../data-access.md)。
6. **`phase clock=true` 无 bia**：配置校验/读盘失败；example **未开**，本机无相位钟 I/O。
7. **`plot_clkdif.sh` 要 `python`**：仅有 `python3` 时伪报缺 matplotlib。
8. **根 `comb.ini` vs example**：根默认 `system=GEC`、atx=`./table/…`；example 为 GPS-only + `../table/…`——勿混目录。
9. **参考轨道 AC**：`combined orbit = igs` 时必须有 `igs*.sp3`；缺则首条 `read products of igs` 即挂。
10. **≠ PPPx**：合成产物可喂 PPP；闭源 PPPx 不在本仓、本手册范围。
11. **Windows**：sln 未官方验证；优先 Linux/WSL。
12. **权随日变**：上表 **23.56%…** 仅 2020-001 GPS example；勿当全局常数。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 多 AC 钟差/偏差 **离线合成** | **clkcomb** | 专用；example 可复现 |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) | 消费 CLK/BIA，不负责多 AC 合成 |
| 武大 GREAT PPP/RTK | [great-pvt](./great-pvt.md) | XML 解算；可接综合钟 |
| GA YAML PPP/POD | [ginan](./ginan.md) | `pea`；产品链自管 |
| CNES 整数 PPP 产品 | [ppp-wizard](./ppp-wizard.md) | 门户产品；客户端另申请 |
| 网解/钟文件读写框架 | [groops](./groops.md) | 重；非本 CLI 替代 |
| 只要官方 IGS CLK | [data-access](../data-access.md) | 直接下 `igs*`/`IGS0*`，不必合成 |

**下一步候选（目录仍缺短硬）：** `GREAT-UPD`（武大多星座 UPD；接 PPP-AR 产品链）或 `Cube`（钟差/PPP-AR 二次开发）；避开已入库篇与并行 WIP。
