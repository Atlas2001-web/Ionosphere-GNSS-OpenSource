# crx2rnx · Rust Hatanaka CRX→RNX 操作手册

目录：[`PROJECTS.json` → `crx2rnx`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/crx2rnx> · crates.io **`crx2rnx` 2.7.0** · tip **`765ddeb`**（release tag `v2.7.0` / `4c49ba6`）· **MPL-2.0** · 基于 GeoRust/`rinex` **0.22.0** · 本机验证 **rustc 1.98.1** + `cargo install crx2rnx`（2026-09-24 05:07 EDT）：AJAC/ACOR/ESBC `.crx(.gz)` 实解；ACOR 与 GSI 观测值字节级一致；AJAC V2 丢星已记

> 岗位：把 Compact RINEX（`.crx` / `.##d` / `.crx.gz`）解成明文 OBS，便于 Rust/现代 CLI 流水线。冲突时：**本机 `crx2rnx -h` / 上游 README > 本文**。  
> **同名陷阱：** PATH 里的 `crx2rnx` 经常是 [hatanaka](./hatanaka.md) 捆绑的 **GSI RNXCMP** 二进制（旗标 `-f/-s/-d`），**不是**本文 Rust CLI。官方可引用压缩/恢复 → [rnxcmp](./rnxcmp.md)；Python 封装 → [hatanaka](./hatanaka.md)。

## 1. 用途与边界

**做：**

- CLI：`crx2rnx <filepath>` —— CRINEX **V1 / V3** → 明文 RINEX
- 原生读 `.crx.gz`（输出仍是**明文** `.rnx` / `.##O`，不回写 gzip）
- 长名保持 / `-s` 合成短名；`-o` / `--prefix` 自定义输出

**不做：**

- **不是** GSI 官方 RNXCMP（`RNX2CRX`/`CRX2RNX`）→ [rnxcmp](./rnxcmp.md)
- **不是** Python `hatanaka` / 其捆绑的同名 `crx2rnx` → [hatanaka](./hatanaka.md)
- **不压缩**（RNX→CRX 另见 crates.io `rnx2crx`，本文不覆盖）
- **不**读进 xarray / 改头 / 拼日 → [georinex](./georinex.md) / [rinexmod](./rinexmod.md) / [gfzrnx](./gfzrnx.md)
- **不保证**与 GSI 输出**整文件字节相等**：会改写 `PGM / RUN BY / DATE` 为 `rs-rinex v0.22.0`；**V2 CRINEX 本机样例有丢星**（见 §3.5 / 坑表）

一句话：nav-solutions **`crx2rnx` = Rust 仅解压 CLI**；生产钉官方兼容优先 [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md)。

| 易混工具 | 是什么 | 典型识别 |
| --- | --- | --- |
| **本文** `~/.cargo/bin/crx2rnx` | Rust，clap，`-q/-s/-o/--prefix` | `crx2rnx -V` → `crx2rnx 2.7.0` |
| GSI `CRX2RNX` | 官方 C，[rnxcmp](./rnxcmp.md) | `-h` 含 `[version : ver.4.2.0]`；`-f/-s/-d` |
| hatanaka 捆 `crx2rnx` | 同 GSI 接口，常 4.1.0 | `pip show hatanaka`；`-h` 无 clap |

| 术语 | 含义 |
| --- | --- |
| CRINEX V1 / V3 | 大致对应 RINEX 2.xx / 3.xx+（与 GSI CRINEX 1.0/3.0 叙述同族） |
| `-s`（本文） | **Prefer V2 short filename**（长名→`AAAA DDD0.YYO`） |
| `-s`（GSI/hatanaka） | **skip strange epochs** —— **完全不同** |
| `rs-rinex` | 写出时写入头的程序名（本机 `v0.22.0`） |

## 2. 安装

```bash
# 推荐 rustup（系统 apt rustc 1.85 常不够；MSRV 标 1.89）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1

cargo install crx2rnx
# 或钉锁：cargo install crx2rnx --locked

which -a crx2rnx
crx2rnx -V
# 期望：/home/.../.cargo/bin/crx2rnx
#       crx2rnx 2.7.0

crx2rnx -h
```

**本机 `crx2rnx -h`（2026-09-24 EDT）：**

```text
CRINEX files decompression tool

Usage: crx2rnx [OPTIONS] <filepath>

Arguments:
  <filepath>  Input RINEX file

Options:
  -q                        Make the tool quiet
  -s                        Prefer V2 (short) filename
  -o <filename>             Define custom output name instead of standard convention.
      --prefix <directory>  Define custom output location (folder) that must exist.
  -h, --help                Print help (see more with '--help')
  -V, --version             Print version
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `package ... requires rustc 1.89` | 旧 toolchain | `. "$HOME/.cargo/env"`；`rustup update` |
| `crx2rnx -V` 失败 / 帮助像 GSI | PATH 命中 hatanaka 捆版 | `hash -r`；显式 `~/.cargo/bin/crx2rnx -V` |
| 只要官方压缩+恢复 | 工具选错 | [rnxcmp](./rnxcmp.md) |
| 要 pip / georinex 依赖 | 场景不同 | [hatanaka](./hatanaka.md) |

源码构建：`git clone https://github.com/nav-solutions/crx2rnx && cargo build --all-features -r`（上游 README）。Release 页本机 **无**预编译 asset（`assets: []`），以 `cargo install` 为准。

## 3. 端到端（本机真跑）

样例来自 nav-solutions/`ionex` 子模 `data/CRNX/`（与 ionex-rs 手册同源）。工作目录：`~/iono_ops/crx2rnx-demo`。

```bash
mkdir -p ~/iono_ops/crx2rnx-demo/{data,e2e} && cd ~/iono_ops/crx2rnx-demo
# 若已有 ionex-rs data：
cp ~/iono_ops/ionex-rs/data/CRNX/V1/AJAC3550.21D data/
cp ~/iono_ops/ionex-rs/data/CRNX/V3/ACOR00ESP_R_20213550000_01D_30S_MO.crx data/
cp ~/iono_ops/ionex-rs/data/CRNX/V3/ESBC00DNK_R_20201770000_01D_30S_MO.crx.gz data/
head -n 2 data/AJAC3550.21D
# 期望：COMPACT RINEX FORMAT；绝不是 <!DOCTYPE html
```

### 3.1 V1 短名 `AJAC3550.21D` → `.21O`

```bash
cd e2e
cp ../data/AJAC3550.21D .
~/.cargo/bin/crx2rnx AJAC3550.21D
ls -la AJAC3550.21D AJAC3550.21O
head -n 2 AJAC3550.21O
wc -c AJAC3550.21D AJAC3550.21O
```

**本机：**

```text
Decompressed AJAC3550.21O
 9185 AJAC3550.21D
 9620 AJAC3550.21O
     2.11           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE
rs-rinex v0.22.0    IGN-RGP             20211222 00:07:07UTCPGM / RUN BY / DATE
```

georinex **1.16.2** 探活（Rust 输出）：`sizes {'time': 2, 'sv': 17}`。  
同文件经 GSI `CRX2RNX` 4.2.0：`sv: 26`，body **≠** Rust（见 §3.5）——V2 勿当官方替代。

### 3.2 V3 长名 ACOR → `.rnx`（数值对齐 GSI）

```bash
cp ../data/ACOR00ESP_R_20213550000_01D_30S_MO.crx .
~/.cargo/bin/crx2rnx ACOR00ESP_R_20213550000_01D_30S_MO.crx
# Decompressed ACOR00ESP_R_20213550000_01D_30S_MO.rnx
wc -c ACOR00ESP_R_20213550000_01D_30S_MO.crx ACOR00ESP_R_20213550000_01D_30S_MO.rnx
head -n 2 ACOR00ESP_R_20213550000_01D_30S_MO.rnx
```

**本机：** `58801` → `182225` B；头 `3.04` / `rs-rinex v0.22.0`；**25** 历元。

georinex（`tlim` 前 1 min）：`{'time': 3, 'sv': 38}`；与 GSI 4.2.0 同窗：

```text
C1C G07 rust=23818653.24 gsi=23818653.24 eq=True
L1C G07 rust=125167854.812 gsi=125167854.812 eq=True
C1C G08 / L1C G08 同样 eq=True；C1C finite 72=72
```

（整文件仍因空格/`PGM` 行 **byte 不等**：Rust 182225 B vs GSI 154166 B。）

### 3.3 `-s` 短名 / gzip / `-o` / `--prefix` / `-q`

```bash
~/.cargo/bin/crx2rnx -s ACOR00ESP_R_20213550000_01D_30S_MO.crx
# Decompressed ACOR3550.21O

cp ../data/ESBC00DNK_R_20201770000_01D_30S_MO.crx.gz .
~/.cargo/bin/crx2rnx ESBC00DNK_R_20201770000_01D_30S_MO.crx.gz
# Decompressed ESBC00DNK_R_20201770000_01D_30S_MO.rnx
# 本机：4032656 → 34573249 B；头 3.05

~/.cargo/bin/crx2rnx -q -o /tmp/crx2rnx_out.txt AJAC3550.21D
# （无 "Decompressed …" 行）；/tmp/crx2rnx_out.txt = 9620 B

mkdir -p /tmp/crx2rnx_pref
~/.cargo/bin/crx2rnx --prefix /tmp/crx2rnx_pref AJAC3550.21D
# Decompressed /tmp/crx2rnx_pref/AJAC3550.21O
```

### 3.4 参数速查

| 旗标 | 作用（本机） |
| --- | --- |
| `<filepath>` | 必填；`.crx` / `.##d` / `.crx.gz` |
| `-q` | 安静（不打印 `Decompressed …`） |
| `-s` | V3 长名 → V2 短名输出（**≠** GSI `-s`） |
| `-o <filename>` | 强制输出路径（覆盖命名逻辑） |
| `--prefix <dir>` | 输出目录，**必须已存在** |
| `-V` / `--version` | `crx2rnx 2.7.0` |
| `-h` / `--help` | 帮助（exit 0） |

无 GSI 的 `-f`（强制覆盖提示）/`-d`（删输入）/`-e`（差分重初始化）/`stdin` 管道模式。

### 3.5 与 GSI / hatanaka 的差异（勿混）

| 维度 | 本文 Rust 2.7.0 | GSI RNXCMP 4.2.0 | hatanaka 捆 4.1.0 |
| --- | --- | --- | --- |
| 语言/装法 | `cargo install` | GSI tar 二进制 | `pip install hatanaka` |
| 压缩 | **无**（另 crate） | `RNX2CRX` | `rinex-compress` |
| `-s` | 短文件名 | skip strange epochs | 同 GSI |
| `PGM` 行 | 改成 `rs-rinex v0.22.0` | 保留原程序名 | 同 GSI |
| ACOR V3 观测值 | 与 GSI **一致**（本机） | 基准 | 与 GSI body 一致（AJAC） |
| AJAC V2 | georinex **17** SV；G07 C1 **nan** | **26** SV；C1 G07=25091572.3 | 与 GSI body 相等 |
| hatanaka `sample.crx` | **panic** `datime parsing` | / `rinex-decompress` OK | OK |

## 4. 输入 / 输出

| 输入 | 默认输出 |
| --- | --- |
| `AAAA DDD0.YYD` / `*.##d` | 同 stem `*.##O` |
| `*_*_MO.crx` | `*_*_MO.rnx` |
| `*.crx.gz` | 明文 `*.rnx`（去 `.gz`） |
| `-s` + 长名 | 短名 `AAAA DDD0.YYO` |
| `-o` / `--prefix` | 自定义 |

写出头会嵌入 `rs-rinex`；比较兼容性请比观测值或 [georinex](./georinex.md)，勿 `cmp` 整文件。

## 5. 接到哪步

- CDDIS/IGS `.crx.gz` → **本文**或 [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md) → [georinex](./georinex.md) → [gnss-tec](./gnss-tec.md)/[pytecgg](./pytecgg.md)
- 改头/长短名规范化 → [rinexmod](./rinexmod.md)（常叠 Hatanaka；默认捆版≠本文）
- 官方可引用归档压缩 → [rnxcmp](./rnxcmp.md)
- 数据入口 → [data-access](../data-access.md)

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `crx2rnx -h` 像 GSI（`-f/-s/-d`） | PATH 命中 hatanaka 捆版 | `~/.cargo/bin/crx2rnx -V`；venv 先 `deactivate` |
| 2 | 以为 `-s` = skip 坏历元 | **旗标语义不同** |  salvage → [rnxcmp](./rnxcmp.md) `-s`；短名才用本文 `-s` |
| 3 | AJAC 等 V2 解完 SV 变少 / 测值 nan | `rinex` 写回 V2 不完整（本机 17≠26） | 生产 V2 → GSI/`hatanaka`；本文优先 V3 |
| 4 | `sample.crx`（hatanaka 测试）panic `datime parsing` | 解析器拒该头/历元格式 | 换 nav-solutions `data/CRNX` 样例；或改用 hatanaka |
| 5 | `--prefix /tmp/no_such` panic `i/o: output error` | 目录必须预先存在 | `mkdir -p` 后再跑 |
| 6 | `KUNZ00CZE.crx` → `00CCC_R_..._00U_...rnx` | 非标准长名时文件名合成怪异 | 用 `-o` 显式命名 |
| 7 | `cmp` Rust `.rnx` ≠ GSI `.rnx` | `PGM` 改写 + 空白格式 | 比对观测字段（如 ACOR C1C）或 georinex |
| 8 | 想 RNX→CRX | 本工具**只解压** | [rnxcmp](./rnxcmp.md) `RNX2CRX` / hatanaka `rinex-compress` / crate `rnx2crx` |
| 9 | `.crx.gz` 解完仍想 `.rnx.gz` | 只写明文 | 自行 `gzip` 输出 |
| 10 | 系统 `rustc 1.85` 装失败 | MSRV | rustup stable（本机 1.98.1） |
| 11 | 无参调用卡住（venv 环境） | 命中 GSI 捆版等 stdin | 看 `which crx2rnx`；Rust 版缺参直接 Usage |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust/cargo 流水线只解压 CRX | **本文 crx2rnx** |
| 官方可引用、双向压缩、RINEX 4.02 | **[rnxcmp](./rnxcmp.md)** |
| pip / 脚本 / georinex 读 `.crx` | **[hatanaka](./hatanaka.md)** |
| 改头 / 长短名 | [rinexmod](./rinexmod.md) |
| 读进 xarray | [georinex](./georinex.md) |

## 8. 相关

[rnxcmp](./rnxcmp.md) · [hatanaka](./hatanaka.md) · [rinexmod](./rinexmod.md) · [georinex](./georinex.md) · [ionex-rs](./ionex-rs.md) · [gfzrnx](./gfzrnx.md) · [data-access](../data-access.md) · [README](./README.md)
