# rnx2cggtts · RINEX→CGGTTS 2E 共视时间比对 CLI 操作手册

目录：[`PROJECTS.json` → `cggtts`](../../PROJECTS.json)（库）· crates.io **`rnx2cggtts` 1.0.2**（bin；仓库字段写 [georust/rinex](https://github.com/georust/rinex)→现重定向 [nav-solutions/rinex](https://github.com/nav-solutions/rinex)）· 生态库 [nav-solutions/cggtts](https://github.com/nav-solutions/cggtts)（crates **`cggtts` 4.x**；本机 tip **`fc75b91`**/仓内 **4.4.0**）· **MIT OR Apache-2.0** · 无独立 git tag/tip 仓（以 crates **1.0.2** 为准）· 本机验证 **`cargo +1.74.1 install rnx2cggtts --locked`**（2026-09-24 06:53 EDT）：ESBC OBS+NAV+GRG SP3 → **`ESBC-GPS-SPP-2h.ggs`** **187** 行 / TRACK **169** / SAT **24**；G15@024600 C1C REFSV=**258796.8 ns** / REFSYS=**480750.6 ns** / ELV=**70.8°** / TRKL=**960 s** / MJD=**59025**

> 岗位：把**同一接收机**的 RINEX 上下文（OBS+NAV+**强制 SP3**）经定位解算写成 **BIPM CGGTTS 2E** 轨文件，供远程站**共视时间比对**。冲突时：**本机 `rnx2cggtts -h` / crates README > 本文**。  
> 纯库解析/合成 CGGTTS → crates.io [`cggtts`](https://crates.io/crates/cggtts)（PROJECTS `cggtts`；**本目录优先不另开 `cggtts.md`**）。同生态 RINEX → [rinex](./rinex.md)/[rinex-cli](./rinex-cli.md)；读进 Python → [georinex](./georinex.md)；UBX→RINEX → [ubx2rinex](./ubx2rinex.md)。rinex-cli 的 `ppp --cggtts` 是**另一入口**（需对应 feature；crates **0.12.1** 常标 NOT AVAILABLE）。

## 1. 用途与边界

**做：**

- 加载 `-f`/`-d`：RINEX OBS（含 `.crx`）+ 广播 NAV + **明文 SP3**（见坑）
- 用 `gnss-rtk` 解接收机钟态 → 按 BIPM 调度写出 **CGGTTS 2E**（默认跟踪 **780 s + 3′** ≈ **16 min**）
- 可选：`-c` 解算 JSON、`--spp`/`--ppp`、星座踢除 `-G/-R/-E/-C/-J/-I/-S`、`-P` 预处理、`--apc`/`--apc-ecef`、`-o` 输出名、`-w` workspace

**不做：**

- **不是** TEC / 电离层产品 → [georinex](./georinex.md)/[pytecgg](./pytecgg.md)/[gnss-tec](./gnss-tec.md)
- **不是** 发表级 PPP 坐标引擎承诺 → [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
- **不是** 纯库 `cggtts`（无同名 bin）→ crates `cggtts` 4.x
- **不是** 仅 QC/改写 RINEX → [rinex-cli](./rinex-cli.md)/[gfzrnx](./gfzrnx.md)
- crates **1.0.2**：无 SP3 → 直接 `ERROR` 退出；无 NAV（有 SP3）→ **panic**；`.sp3.gz` → **panic**（`sp3` 未开 `flate2`）

一句话：`rnx2cggtts` = **OBS+NAV+SP3 → CGGTTS 2E 共视轨**；产物是时间比对文件，不是定位/TEC。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `rnx2cggtts` | Rust CLI | `rnx2cggtts -V` → `rnx2cggtts 1.0.2` |
| `cggtts` crate | 纯库 4.x | `cargo add cggtts`；无同名 bin |
| [rinex-cli](./rinex-cli.md) `ppp --cggtts` | 后处理 CLI 旁路 | 需 feature；接口≠本 bin |
| [rinex](./rinex.md) | RINEX 库 | 无 CGGTTS 调度写出 |

| 术语 | 含义 |
| --- | --- |
| CGGTTS 2E | BIPM 共视格式；本工具**只出 2E** |
| TRACK / TRKL | 一条轨；默认 TRKL=**960 s**（本机） |
| REFSV / REFSYS | 相对星钟 / 系统时差，单位 **0.1 ns** |
| APC | 天线相位中心；可从头 `APPROX POSITION` 或 `--apc*` |
| workspace | `-w` 下按主 OBS stem 建子目录 |

## 2. 安装

```bash
# crates 1.0.2（2023-12）锁依赖；本机 rustc 1.98.1 下
#   cargo install rnx2cggtts --locked  → time-0.3.30 E0282
#   cargo install rnx2cggtts           → arrow-arith 与新 chrono 冲突
# 可用路径：rustup 装 1.74.1（与发布同期）再 --locked
. "$HOME/.cargo/env"
rustup install 1.74.1
cargo +1.74.1 install rnx2cggtts --locked
which rnx2cggtts
rnx2cggtts -V
# 期望：…/.cargo/bin/rnx2cggtts
#       rnx2cggtts 1.0.2

rnx2cggtts -h
```

**锁文件关键依赖（crates 1.0.2 `Cargo.lock`）：** `rinex` **=0.15.2** · `cggtts` **4.1.1** · `gnss-rtk` **0.4.1** · `gnss-rs` **2.1.2** · `sp3` **1.0.6** · `clap` **4.4.11**。生态上写出侧对接 **`cggtts` 4.x**（crates 现最新 **4.4.0**）。

**本机 `rnx2cggtts -h`（2026-09-24 EDT，ANSI 已剥；节选）：**

```text
CGGTTS from RINEX Data generation tool

Usage: rnx2cggtts [OPTIONS]

Options:
  -f, --fp <FILE>           Input RINEX file. Can be any kind of RINEX or SP3…
  -d, --dir <DIRECTORY>     Load directory recursively…
  -w, --workspace <FOLDER>  Customize workspace location…
  -h, --help                Print help
  -V, --version             Print version

CGGTTS:
      --clk <NAME> / -u <NAME> / -s <NAME> / -o <FILENAME>

Antenna:
  -a, --apc <"lat, lon, alt" …> / --apc-ecef <"x, y, z" …>

Sky tracking & Common View:
  -t <DURATION>             default is 780s + 3' …
      --sv <SV>

Setup / Hardware:
      --rf-delay <rfdly> / --ref-delay <refdly>

Solver:
  -c, --cfg <FILE> / --spp / --ppp

Preprocessing:
  -G/-R/-E/-C/-J/-I/-S / -P <preprocessing>...
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `time` E0282 / `arrow-arith` E0034 | rustc 过新 | `cargo +1.74.1 install … --locked` |
| `SP3 must unfortunately be provided` | 未加载 SP3 | 加明文 `.SP3`（先 `gunzip`） |
| `.gz data requires --flate2` | `sp3` 未开压缩 feature | 解压 SP3 再 `-f` |
| panic `requires BRDC Navigation` | 有 SP3 无 NAV | 加同日 MN/`.??n` |

## 3. 端到端（本机 1.0.2 真跑；2026-09-24 06:53 EDT）

样例：ESBC（DNK）2020-06-25 = DOY **177** —— OBS/NAV 与 [rinex-cli](./rinex-cli.md) CGGTTS 例同源；SP3 = `GRG0MGXFIN_20201770000_01D_15M_ORB.SP3`（ionex-rs/`ubx2rinex` data）。工作目录：`~/iono_ops/rnx2cggtts-demo`。

```bash
mkdir -p ~/iono_ops/rnx2cggtts-demo/{data,ws,logs} && cd ~/iono_ops/rnx2cggtts-demo
cp ~/iono_ops/rinex-cli-demo/data/ESBC00DNK_R_20201770000_01D_{30S_MO.crx,MN.rnx}.gz data/
cp ~/iono_ops/ionex-rs/data/SP3/C/GRG0MGXFIN_20201770000_01D_15M_ORB.SP3.gz data/
gunzip -kf data/*.gz
# 解算配置（与 rinex-cli examples/CONFIG 同形）
printf '%s\n' '{' '    "method": "SPP",' '    "timescale": "GPST"' '}' > gpst_spp.json

export RUST_LOG=info
rnx2cggtts -w "$PWD/ws" \
  -f data/ESBC00DNK_R_20201770000_01D_30S_MO.crx \
  -f data/ESBC00DNK_R_20201770000_01D_MN.rnx \
  -f data/GRG0MGXFIN_20201770000_01D_15M_ORB.SP3 \
  --spp -c gpst_spp.json \
  -R -E -C -J -I -S \
  -o 'ESBC-GPS-SPP-2h.ggs'
# 日志关键行（真实）：
# workspace is "…/ws/ESBC00DNK_R_20201770000_01D_30S_MO"
# using reference position WGS84 (3582105.291m 532589.7313m 5232754.8054m)
#   (lat=55.49356°, lon=8.45682°)
# tracking duration set to 16 min
# …/ESBC-GPS-SPP-2h.ggs has been generated
```

### 3.1 输出文件

路径：`ws/ESBC00DNK_R_20201770000_01D_30S_MO/ESBC-GPS-SPP-2h.ggs`  
**19796 B / 187 行**；头 `VERSION = 2E`；`LAB = ESBC00DNK`；`COMMENTS = rnx2cggtts v1.0.2`；`X/Y/Z` = 头近似坐标。

| 量 | 本机 |
| --- | --- |
| TRACK 行（`G..`） | **169** |
| 唯一 SAT | **24**（G01…G32 子集） |
| 唯一 SAT×STTIME | **46** |
| FRC 计数 | C2W **41** / C1C **38** / C1W **37** / C2L **34** / C5Q **19** |
| STTIME 范围 | **024600–223000**（MJD **59025**） |
| TRKL | **960 s** |

**关键轨（G15 · STTIME=024600 · FRC=C1C）：**

```text
G15 99 59025 024600  960 708 2379     2587968    291     4807506    266  420   0   87    2  759   50 00 00 C1C 10
```

| 字段 | 原始 | 物理 |
| --- | --- | --- |
| ELV | 708 | **70.8°**（×0.1°） |
| REFSV | 2587968 | **258796.8 ns**（×0.1 ns） |
| REFSYS | 4807506 | **480750.6 ns**（×0.1 ns） |
| TRKL | 960 | **960 s** |

说明：本跑曾附带 `-P 'GPS;C1C'` 与 2 h 时间窗字符串；**星座踢除生效**（仅 `G*`），但 FRC/STTIME 仍覆盖全日多码——**勿假设 `-P` 已裁到 C1C/2 h**；以落盘 `.ggs` 为准。

### 3.2 失败边界（如实）

```bash
# 无 SP3
rnx2cggtts -f data/ESBC…MO.crx -f data/ESBC…MN.rnx --spp
# → ERROR rnx2cggtts: SP3 must unfortunately be provided at the moment

# demo.10o 单独
rnx2cggtts -f data/demo.10o --spp
# → 同上 ERROR（缺 SP3）

# OBS+SP3 无 NAV
rnx2cggtts -f …MO.crx -f …SP3 --spp -c gpst_spp.json -R -E -C -J -I -S
# → panic: rnx2cggtts requires BRDC Navigation Data to be provided!

# SP3 仍为 .gz
rnx2cggtts … -f …ORB.SP3.gz …
# → panic: .gz data requires --flate2 feature
```

## 4. 接到哪一步

| 上游 | 本工具 | 下游 |
| --- | --- | --- |
| [ubx2rinex](./ubx2rinex.md)/[georinex](./georinex.md) 落盘 OBS | 加 NAV+SP3 → `.ggs` | 两站交换 CGGTTS → 共视差（实验室流程；本仓无专用比对 CLI） |
| [rinex-cli](./rinex-cli.md) QC | 确认历元连续后再跑 | 勿把 `.ggs` 当 TEC |
| crates `cggtts` | 若要自写调度/解析 | `cargo add cggtts`；见 PROJECTS `cggtts` |

## 5. 坑（可操作）

1. **必须 SP3**：`main` 硬检查；README「NAV 即可」对 1.0.2 **不成立**。
2. **必须 NAV**：过了 SP3 检查后无 BRDC → **panic**（非温和 ERROR）。
3. **SP3 先 gunzip**：`.sp3.gz` 直接炸 `flate2`。
4. **OBS `.crx` OK**；`.crx.gz` 视 `rinex` feature，稳妥先解压。
5. **APC**：无头近似且未 `--apc*` → 解算起不来；ESBC 头 ECEF 本机已用。
6. **默认 16 min 轨**：短切片（如 ACOR **25** 历元）可能 **0** TRACK。
7. **`-t` 改跟踪长**：仅当你控制两端调度；非法串 → panic。
8. **`-P` 勿盲信**：以输出 FRC/STTIME 核对。
9. **rustc 1.98**：用 **1.74.1 + --locked**，勿强行升依赖。
10. **仓库字段 georust/rinex**：GitHub 已到 **nav-solutions/rinex**；独立 bin **未**随 tip 重发——以 crates **1.0.2** 为准。
11. **rinex-cli `--cggtts`**：另一条路径；本机 0.12.1 常不可用。
12. **产物 ≠ TEC/定位**：共视时间比对文件；电离层走 TEC 流水线。
13. **混站 `-d`**：README 不建议；优先逐文件 `-f`。
14. **日志洪泛**：`RUST_LOG=info` 全日可达 **10⁵** 行 WARN；成功以 `has been generated` 为准。
15. **测完**勿留后台 `rnx2cggtts`/解算进程。

## 6. 同类怎么选

| 需求 | 选 |
| --- | --- |
| RINEX→CGGTTS 2E CLI | **本文 `rnx2cggtts`** |
| 只解析/合成 CGGTTS | crates **`cggtts` 4.x**（库） |
| RINEX QC / filegen | [rinex-cli](./rinex-cli.md) |
| Python 读 OBS | [georinex](./georinex.md) |
| UBX→OBS | [ubx2rinex](./ubx2rinex.md) |
