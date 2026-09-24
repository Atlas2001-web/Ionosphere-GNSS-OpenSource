# rinex-cli · Rust RINEX/SP3 后处理 CLI 操作手册

目录：[`PROJECTS.json` 提及](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/rinex-cli>（旧镜像 gwbres/rtk-rs 以 **crates.io + nav-solutions tip** 为准）· crates.io **`rinex-cli` 0.12.1** · tip **`f4dd4c3`**（仓内 `Cargo.toml` **0.13.0**）· **MPL-2.0** · 本机验证 **rustc 1.98.1** + `cargo install rinex-cli --locked`（2026-09-24 05:21 EDT）：ACOR **25** 历元 HTML QC；ESBC `.crx.gz` **2880** 历元；`filegen` / `-P` / `--gzip` 实写

> 岗位：nav-solutions / GeoRust 生态的 **RINEX（+SP3）后处理 CLI**——默认出 **HTML QC 报告**，另有 `filegen`/`merge`/`diff`/`split`/`tbin` 文件操作与可选 `ppp`/`rtk`。冲突时：**本机 `rinex-cli -h` / 上游 README > 本文**。  
> **纯库** → crates.io [`rinex`](https://crates.io/crates/rinex) / [docs.rs/rinex](https://docs.rs/rinex)（本文写 CLI，不展开库 API）。Python 读进 xarray → [georinex](./georinex.md)；改头/长短名 → [rinexmod](./rinexmod.md)；官方 Hatanaka → [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)；同生态仅解压 CRX → [crx2rnx](./crx2rnx.md)。

## 1. 用途与边界

**做：**

- 默认（无子命令）：加载 `--fp`/`-d` → 综合 **RINEX-QC** HTML（`index.html`；`--sum` 仅摘要）
- 文件操作：`filegen`（预处理后写出，**保留输入形态** RNX/CRX/gzip）、`merge`、`diff`、`split`、`tbin`
- 预处理：`-G/-R/-E/-C/-J/-I/-S` 踢星座；`-P` 滤设计器（如 `GPS;C1C,L1C`）；`-z` 去零值
- 读 **`.rnx` / `.crx` / `.crx.gz`**（及帮助所列 NAV/CLK/SP3/IONEX/ANTEX…）；`filegen --gzip` / `--unzip`
- `ppp` / `rtk`：报告里追加定位章（需 OBS+NAV 等；配置 `-c`；`cggtts`/`kml`/`gpx` 视编译 feature）

**不做：**

- **不是** 纯库 `rinex` crate（嵌入式解析/写回）→ [docs.rs/rinex](https://docs.rs/rinex)
- **不是** Python xarray / pandas 科研读盘 → [georinex](./georinex.md) / [gnsspy](./gnsspy.md) / [gnsstools](./gnsstools.md)
- **不是** 官方 RNXCMP 双向 Hatanaka → [rnxcmp](./rnxcmp.md)；**不是** 仅 Rust 解压小工具 → [crx2rnx](./crx2rnx.md)
- **不是** 批量改头/长短名规范化 → [rinexmod](./rinexmod.md)
- **不是** 经典 TEQC / GFZRNX / Anubis 的替代承诺 → [teqc](./teqc.md) / [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md)
- crates.io **0.12.1** 本机：`tbin`/`split` 有 panic；短名 `demo.10o` 拒识；`--csv`/`--cggtts`/`--kml`/`--gpx` 显示 **NOT AVAILABLE**（需对应 feature / 更重构建）

一句话：`rinex-cli` = **Rust 侧 RINEX QC + 文件手术刀**（可选 PPP）；电离层/TEC 流水线仍接 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `rinex-cli` | Rust CLI，clap 子命令 | `rinex-cli -V` → `rinex-cli 0.12.1` |
| `rinex` crate | 纯库 | `cargo add rinex`；无同名 bin |
| [crx2rnx](./crx2rnx.md) | 同生态仅 CRX→RNX | `crx2rnx -V`；无 HTML QC |
| [georinex](./georinex.md) | Python 读 OBS | `python -m georinex` / API |
| [teqc](./teqc.md) / [gfzrnx](./gfzrnx.md) | 经典 C QC/编辑 | EOL teqc；GFZ 登记二进制 |

| 术语 | 含义 |
| --- | --- |
| 默认 opmode | 无子命令 → 综合报告（非 `filegen`） |
| Workspace | `$RINEX_WORKSPACE` 或 `-w`；否则本地 `WORKSPACE/`；会话目录 = 主文件 stem |
| `filegen` 保形 | 输入 `.crx` → 写出 `.crx`；`.rnx` → `.rnx`；可用 `--gzip`/`--unzip` 改 |
| RINEX-QC | 报告引擎标 **v0.0.2**（本机 HTML） |
| tip vs crates | tip `f4dd4c3` 标 **0.13.0**；演示里的 `cbin` 等以 tip/README 为准，**0.12.1 `-h` 无 `cbin`** |

## 2. 安装

```bash
# rustup（crates.io 元数据 rust-version 1.64；tip README MSRV 1.82；本机 1.98.1）
. "$HOME/.cargo/env"
rustc --version

# 推荐：crates.io 锁版本
cargo install rinex-cli --locked
which rinex-cli
rinex-cli -V
# 期望：…/.cargo/bin/rinex-cli
#       rinex-cli 0.12.1

rinex-cli -h

# tip（可选；本机 clone 验证 commit，未强制覆盖 bin）
# mkdir -p ~/iono_ops && cd ~/iono_ops
# git clone --depth 50 https://github.com/nav-solutions/rinex-cli.git
# cd rinex-cli && git log -1 --oneline   # f4dd4c3 upgrading (#44)
# cargo install --path . --locked
```

**本机 `rinex-cli -h`（2026-09-24 EDT，ANSI 已剥）：**

```text
RINEX post processing

Usage: rinex-cli [OPTIONS] [COMMAND]

Commands:
  filegen, --filegen  Parse, preprocess and generate new RINEX and/or SP3 data. …
  merge, -m, --merge  Merge a RINEX into another and dump result. …
  ppp                 Post Processed Positioning. …
  rtk                 Post Processed RTK. …
  split               Split input file(s) at specified Epoch
  diff                RINEX(A)-RINEX(B) substraction operation. …
  tbin                Time binning. Split files into a batch of equal duration.
  help                Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help (see more with '--help')
  -V, --version  Print version

Context:
      --fp <FILE>           Load a single file. …
  -d, --dir <DIRECTORY>     Directory recursivel loader. …
  -q, --quiet               Disable all terminal output. Disables automatic report opener …
  -w, --workspace <FOLDER>  Define custom workspace location. …
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `package … requires rustc …` | toolchain 过旧 | rustup stable（本机 1.98.1） |
| 无输出 / 以为失败 | 默认可能开浏览器；日志在 `RUST_LOG` | `-q`；`RUST_LOG=info` |
| `--csv` NOT AVAILABLE | 未开 `csv` feature | tip `default=["csv"]` 或 `cargo install --features csv` |
| 与 hatanaka 捆 `crx2rnx` 混淆 | 同名只解压 | 本文是 `rinex-cli`；解压小工具见 [crx2rnx](./crx2rnx.md) |

## 3. 端到端（本机 0.12.1 真跑；2026-09-24 05:21 EDT）

样例：nav-solutions/`ionex` 系 CRNX（与 [crx2rnx](./crx2rnx.md)/[ionex-rs](./ionex-rs.md) 同源）+ 已解 ACOR `.rnx`。工作目录：`~/iono_ops/rinex-cli-demo`。

```bash
mkdir -p ~/iono_ops/rinex-cli-demo/{data,ws} && cd ~/iono_ops/rinex-cli-demo
export RINEX_WORKSPACE="$PWD/ws"
# ACOR V3 短切片（25×30 s）与 ESBC 全日 .crx.gz
cp ~/iono_ops/crx2rnx-demo/e2e/ACOR00ESP_R_20213550000_01D_30S_MO.{rnx,crx} data/
cp ~/iono_ops/ionex-rs/data/CRNX/V3/ESBC00DNK_R_20201770000_01D_30S_MO.crx.gz data/
```

### 3.1 默认 QC：ACOR 明文 → HTML

```bash
export RUST_LOG=info
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx -f -q
# 全报告（非 --sum）约 565 KB HTML；摘要加 --sum
ls -la "$RINEX_WORKSPACE"/ACOR00ESP_R_20213550000_01D_30S_MO/
```

**本机日志（摘录）：**

```text
 INFO  rinex_cli] Position defined in dataset: (4594489.868, -678367.992, 4357065.87) [ECEF] (lat=43.36438°, lon=-8.39894°)
 INFO  rinex_cli::cli::workspace] session workspace is "…/ws/ACOR00ESP_R_20213550000_01D_30S_MO"
 INFO  rinex_cli::report] …/index.html report generated
```

**本机 HTML 关键数字（`ACOR_full.html` / 全文解析）：**

| 字段 | 值 |
| --- | --- |
| Timescale | **GPST** |
| ECEF / LLH | **4594489.868**, **−678367.992**, **4357065.870** m → **43.364381°N**, **8.398935°W**, **66.876** m |
| 接收机 | **LEICA GR50** SN **1833574** FW **4.50/7.710** |
| 天线 | **LEIAT504 LEIS** / 高 **3.046** m |
| 时窗 | **2021-12-21T00:00:00 → 00:12:00 GPST**；时长 **12 min**；采样 **30 s**（0.033 Hz） |
| 历元 | **25**（与 `grep -c '^>'` 一致；无 gap） |
| GPS SV | **G01,G07,G08,G10,G16,G18,G21,G23,G26,G30**（**10**）；信号 L1/L2/L5 |
| GAL / GLO / BDS | E：**8**；R：**6**；C：**14**（C05…C58） |

### 3.2 Gzip CRX：ESBC 全日摘要

```bash
rinex-cli --fp data/ESBC00DNK_R_20201770000_01D_30S_MO.crx.gz --sum -f -q
# 全日全报告 HTML 本机约 71 MB（plots）；首次可先 --sum
```

**本机：**

```text
 INFO  rinex_cli] Position defined in dataset: (3582105.291, 532589.7313, 5232754.8054) [ECEF] (lat=55.49356°, lon=8.45682°)
 INFO  rinex_cli::report] …/ESBC00DNK_R_20201770000_01D_30S_MO/index.html report generated
```

| 字段 | 值 |
| --- | --- |
| 接收机 | **SEPT POLARX5** SN **3047937** FW **5.2.0** |
| 时窗 | **2020-06-25T00:00:00 → 23:59:30 GPST**；**23 h 59 min 30 s**；**30 s** |
| 历元 | 信号兼容行 **0/2880** 分母 → **2880** 历元（30 s×日） |
| GPS SV | **31**（G01–G32 缺 G23）；GAL **22**；GLO **23**；BDS **29**；QZSS **3** |

### 3.3 `filegen`：保形写出 / gzip / 滤星座 / `-P`

```bash
# 明文 → OBSERVATIONS/*.rnx（本机命名 PPU 合成 15M + 2359 时戳，见坑）
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx filegen
# → …/OBSERVATIONS/ACOR00ESP_R_20213552359_15M_30S_MO.rnx  (179531 B；历元仍 25)

# 输入 .crx → 输出仍 .crx（保形）
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.crx filegen
# → …/ACOR00ESP_R_20213552359_15M_30S_MO.crx  (42322 B)

# 强制 gzip
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx filegen --gzip
# → …/ACOR00ESP_R_20213552359_15M_30S_MO.rnx.gz  (47375 B)

# 仅 GPS + 自定义名（-o 必须在子命令前）
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx \
  -R -E -C -J -I -S -o ACOR_GPS_only.rnx filegen
# → ACOR_GPS_only.rnx 51611 B；头 SYS 仅 G，12 观测类型；历元 25

# 滤设计器：仅 C1C+L1C
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx \
  -P 'GPS;C1C,L1C' -o ACOR_L1.rnx filegen
```

**本机 `ACOR_L1.rnx` 头与首历元（可复现）：**

```text
G    2 C1C L1C                                              SYS / # / OBS TYPES
> 2021 12 21 00 00  0.0000000  0 10
G01  24600158.420   129274705.78406
G07  23818653.240   125167854.81207
G08  20980381.160   110252666.62308
…
```

G07 **C1C=23818653.240** 与 [crx2rnx](./crx2rnx.md) ACOR/GSI 对照一致。

### 3.4 边界实况：`tbin` / `split` / 短名 / `ppp` 旗标位置

```bash
# 0.12.1：Duration 解析后仍 panic "duration is required"（arg 名 interval 与 CLI 不一致）
rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx tbin '5 min'
# panic: duration is required

rinex-cli --fp data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx \
  split '2021-12-21T00:06:00 GPST'
# panic: failed to determine Observation file suffix

rinex-cli --fp data/demo.10o --sum -q -f
# WARN non supported file format "…/demo.10o"
# panic: failed to determine a context name

# 全局旗标必须在子命令前
rinex-cli --fp data/ACOR….rnx -q ppp     # OK 位置
rinex-cli --fp data/ACOR….rnx ppp -q     # error: unexpected argument '-q'
```

`ppp`/`rtk` 需 OBS+NAV（及可选 SP3/CLK）与 `-c` 配置；上游 `demos/GPS_ONLY.md` 有完整例。本手册以 QC/`filegen` 为主，**未**在此机跑通全日 PPP 解（耗时长；feature/`--static` 与 tip 演示可能不一致）。

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `--fp` / `-d` | 加载文件或递归目录（默认 depth **5**） |
| （无子命令） | 写 `$WS/<stem>/index.html`（`-o` 可改报告名） |
| `--sum` / `-f` | 仅摘要 / 强制重生成报告 |
| `-w` / `RINEX_WORKSPACE` | 产品根目录 |
| `-q` | 安静 + 禁止自动开浏览器 |
| `filegen` | 写出到 `<stem>/OBSERVATIONS/` |
| `merge` / `diff` | 第二文件为位置参 |
| `-G…-S` / `-P` / `-z` | 星座踢除 / 滤设计器 / 去零 |
| `--gzip` / `--unzip` / `-s` | 压明文 / 强制明文 / 短文件名（file ops） |
| `ppp` `-c` | 定位配置 JSON；解写入报告章 |

| 本机产物（ACOR） | 大小 / 要点 |
| --- | --- |
| `index.html`（`--sum`） | ≈7.5 KB |
| 全报告 HTML | ≈565 KB（ACOR）；ESBC 全日 ≈71 MB |
| `filegen` `.rnx` / `.crx` / `.rnx.gz` | 179531 / 42322 / 47375 B |
| `ACOR_L1.rnx` | SYS **G 2**（C1C L1C）；首历元 **10** SV |

## 5. 接到哪步

```text
归档 .crx.gz / .rnx
  → rinex-cli（本文）HTML QC / filegen 滤星座·观测
  →（可选）crx2rnx / rnxcmp / hatanaka 只解压
  →（可选）rinexmod 改头
  → georinex / gnsspy / gnsstools
  → gnss-tec / pytecgg / anubis / gfzrnx
定位章：ppp（OBS+NAV[+SP3]）或改走 rtklib / ginan
```

路径 A 可在 [georinex](./georinex.md) 前插入本文做 Rust QC；交叉 [teqc](./teqc.md)/[gfzrnx](./gfzrnx.md)/[anubis](./anubis.md)/[gnss-multipath-analysis](./gnss-multipath-analysis.md)。

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 无 stdout 以为挂了 | 默认开浏览器；info 在 tracing | `-q`；`RUST_LOG=info` |
| 2 | `ppp -q` / `filegen -o` 报 unexpected | 全局选项须在**子命令前** | `… -q -o name filegen` / `… -q ppp` |
| 3 | `demo.10o` panic context name | 短名/R2 被标 non supported | 用 RINEX3 长名或先 [rinexmod](./rinexmod.md)/[gfzrnx](./gfzrnx.md) |
| 4 | `tbin` panic `duration is required` | 0.12.1 CLI 与内部 `interval` 不一致 | 升级 tip 或改用外部按历元切；勿臆造已修好 |
| 5 | `split` panic file suffix | 0.12.1 文件后缀推断失败 | 同上；先 `filegen` 再外部切 |
| 6 | `filegen` 文件名 `…2359_15M…` | ProductionAttributes PPU/时戳合成怪 | 用 `-o`；内容历元仍正确（ACOR **25**） |
| 7 | `TIME OF LAST OBS` 写成 23:59:49 | 写回头字段不可靠 | 以记录历元/`grep '^>'` 为准 |
| 8 | ESBC 全报告 70 MB+ | 带图全日 | 先 `--sum`；磁盘预留 |
| 9 | `--csv`/`--cggtts` NOT AVAILABLE | feature 未编进本 bin | `cargo install --features …` 或下 release `rinex-cli-ppp` |
| 10 | 与 [crx2rnx](./crx2rnx.md) 分工不清 | 一个 QC/fileops，一个仅解压 | 只要 CRX→RNX 用 crx2rnx/GSI |
| 11 | tip 文档有 `cbin`，`-h` 没有 | **0.12.1** 命令集 ≠ tip 0.13 演示 | 以本机 `-h` 为准 |
| 12 | 库 API 当 CLI 用 | `rinex` 无同名可执行文件 | CLI 用本文；库看 docs.rs |
| 13 | PPP 无 NAV / 无 `-c` | 求解上下文不足 | 叠 `--fp` NAV；参考上游 `demos/` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust HTML QC + 滤星座/观测写回 | **本文 rinex-cli** |
| 纯库解析/嵌入 | [`rinex`](https://docs.rs/rinex) crate |
| Python → xarray / pandas | [georinex](./georinex.md) / [gnsspy](./gnsspy.md) / [gnsstools](./gnsstools.md) |
| 仅 CRX→RNX（Rust） | [crx2rnx](./crx2rnx.md) |
| 官方 Hatanaka 双向 | [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md) |
| 改头 / 长短名 | [rinexmod](./rinexmod.md) |
| 经典 QC / 拼接抽稀 | [teqc](./teqc.md) / [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md) |
| 生产 PPP | [rtklib](./rtklib.md) / [ginan](./ginan.md)（本文 `ppp` 为同栈试验刀） |

## 8. 相关

[georinex](./georinex.md) · [rinexmod](./rinexmod.md) · [hatanaka](./hatanaka.md) · [crx2rnx](./crx2rnx.md) · [rnxcmp](./rnxcmp.md) · [teqc](./teqc.md) · [gfzrnx](./gfzrnx.md) · [gnsspy](./gnsspy.md) · [gnsstools](./gnsstools.md) · [anubis](./anubis.md) · [ionex-rs](./ionex-rs.md) · [ntrip-client](./ntrip-client.md) · [docs.rs/rinex](https://docs.rs/rinex) · [README](./README.md)
