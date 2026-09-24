# MRTKLIB · 现代化 GNSS 定位库操作手册

目录：[`PROJECTS.json` → `MRTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/h-shiono/MRTKLIB> · 文档 <https://h-shiono.github.io/MRTKLIB/> · 许可 **BSD-2-Clause**（含 Takasu / Cabinet Office / JAXA / GSI / Everett 等多方版权声明）· tip **`8e09166`** / **v0.7.10**（2026-09-22）· 本机：CMake+LAPACK → `mrtk`；仓内 GSI 样例 SPP **120**×Q=5 首点 **35.160868346°N 139.613825769°E**（与 apt `rnx2rtkp` 2.4.3 b34 **逐字段一致**）；RTK **120**×Q=**1** 首点 **35.160880512°N 139.613834411°E h=74.5858** · **2026-09-24 06:25 EDT**

> 岗位：统一 CLI **`mrtk`** 做事后/实时 SPP·RTK·PPP·PPP-AR·CLAS PPP-RTK，以及 MADOCA / Galileo HAS / IGS 产品改正。冲突时：**仓内 README / `docs/guide` / `mrtk post --help` > 本文**。经典 CLI → [rtklib](./rtklib.md)；武大 GREAT → [great-pvt](./great-pvt.md)；GA pea → [ginan](./ginan.md)。

**与 [rtklib.md](./rtklib.md) 的差别：** `rtklib.md` 覆盖官方树 + **rtklibexplorer**（原 demo5→`main`，常称 RTKLIB-EX）的 **`rnx2rtkp`/`convbin`/`str2str`**。MRTKLIB **不是**「再 fork 一份 flat RTKLIB」：C11 模块化 + `mrtk_ctx_t` 去全局、CMake、TOML；引擎吸收 **MALIB / MADOCALIB / CLASLIB** 与部分 demo5 算法，入口是 **`mrtk post` / `mrtk run`**（帮助里仍可见 `rnx2rtkp(MRTKLIB …)` 程序名）。低成本博客流程优先 explorer；亚太 CLAS/MADOCA/HAS 一体优先本文。

## 1. 用途与边界

**做：**

- 事后：`mrtk post`（mode 0..7：single→ppp-static）
- 实时：`mrtk run`（rtkrcv 系；CLAS 1ch/2ch、MADOCA、HAS、IGS-RTS）
- 改正：QZSS L6E/L6D、Galileo HAS（`.has`）、IGS SP3/CLK + Bias-SINEX OSB PPP-AR、CSSR→RTCM3 等子命令
- 工具：`convert`/`relay`/`dump`/`l6extract`/`cssr2rtcm3`…

**不做：**

- **不是** Debian `apt install rtklib` 的同名替代说明 → 版本与 `-h` 语义见 [rtklib](./rtklib.md)（两边 **`post`/`rnx2rtkp` 的 `-h` 都是 fix-and-hold，帮助用 `-?`/`--help`**）
- **不是** 仅 demo5 低成本优化树 → explorer 仍见 [rtklib](./rtklib.md)
- **不是** STEC 产品引擎 → [pytecgg](./pytecgg.md)；闪烁 → [oasis-roti](./oasis-roti.md)
- 本机 **未**拉公网 L6/HAS 流、**未**跑全日 MADOCA/CLAS 收敛曲线 → 改正类 E2E 以官方 quickstart + 自备 `.l6`/`.has` 为准，**禁止臆造**固定率

一句话：MRTKLIB = **面向下一代多 GNSS / QZSS 增强的现代化定位库**（统一 `mrtk`）。

| 术语 | 含义 |
| --- | --- |
| `mrtk` | 统一二进制（本机构在 `build/mrtk`） |
| `mrtk post` | 事后（同源 `rnx2rtkp`） |
| `mrtk run` | 实时（同源 `rtkrcv`） |
| TOML `-k` | `conf/madocalib/*`、`conf/claslib/*`、`conf/has/*`、`conf/igs/*` |
| Q | `.pos` 质量：1 fix / 2 float / 5 single / 6 ppp… |

## 2. 安装 / 编译

### 2.1 依赖

```bash
sudo apt-get update
sudo apt-get install -y cmake g++ liblapack-dev libblas-dev
# LAPACK 推荐；ILP64 OpenBLAS 勿用（需 LP64）
```

### 2.2 构建

```bash
git clone https://github.com/h-shiono/MRTKLIB.git
cd MRTKLIB
git rev-parse --short HEAD    # 本机 8e09166
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/mrtk --version
# mrtk (MRTKLIB ver.0.7.10 git v0.7.10)
./build/mrtk --help | head
```

可选：`cmake --install build` 把 `mrtk` 装进前缀。文档站用 MkDocs（与定位二进制无关）。

## 3. 端到端（本机 · 仓内 GSI 样例）

数据：`tests/data/rtklib/rinex/07590920.05[on]`（流动 0759）+ `30400920.05[on]`（基准 3040），2005-04-02 约 1 h、30 s。

### 3.1 SPP

```bash
mkdir -p /tmp/mrtk_smoke
./build/mrtk post -p 0 -sys G -f 1 -m 10 -o /tmp/mrtk_smoke/spp.pos \
  tests/data/rtklib/rinex/07590920.05o \
  tests/data/rtklib/rinex/07590920.05n
grep -v '^%' /tmp/mrtk_smoke/spp.pos | awk 'NF>=6{n++; q[$6]++} END{print "epochs",n; for(k in q) print "Q"k,q[k]}'
head -3 /tmp/mrtk_smoke/spp.pos | tail -1
```

**本机：** **120** 历元全 **Q=5**；首历元  
`1316 518400.000  35.160868346  139.613825769  83.8246  5  7 …`  
同文件 apt **`rnx2rtkp ver.2.4.3 b34`** 首行 **一致**（交叉验证通过）。

### 3.2 相对定位（kinematic）

```bash
./build/mrtk post -p 2 -sys G -f 2 -m 15 -o /tmp/mrtk_smoke/rtk.pos \
  tests/data/rtklib/rinex/07590920.05o \
  tests/data/rtklib/rinex/30400920.05o \
  tests/data/rtklib/rinex/07590920.05n \
  tests/data/rtklib/rinex/30400920.05n
grep -v '^%' /tmp/mrtk_smoke/rtk.pos | awk 'NF>=6{n++; q[$6]++} END{print "epochs",n; for(k in q) print "Q"k,q[k]}'
```

**本机：** **120** 历元全 **Q=1**（fix）；首历元  
`35.160880512  139.613834411  74.5858`，ratio≈**24.7**；头注释 `% ref pos : 35.132071656 139.624297984 80.1175`。

### 3.3 改正类（需自备产品；本机未跑）

```bash
# MADOCA-PPP（示例骨架；.l6 自备）
./build/mrtk post -k conf/madocalib/rnx2rtkp.toml obs.obs nav.nav l6e.l6 -o madoca.pos
# CLAS PPP-RTK
./build/mrtk post -k conf/claslib/rnx2rtkp.toml obs.obs nav.nav clas.l6 -o clas.pos
# Galileo HAS
./build/mrtk post -k conf/has/ppp_gal_has.toml obs.obs nav.nav corr.has -o has.pos
# 实时（配置见 conf/*/rtkrcv*.toml）
./build/mrtk run -s -o conf/claslib/rtkrcv.toml
```

逐步说明见上游 `docs/guide/quickstart-madoca-ppp.md` / `quickstart-clas.md` / `quickstart-gal-has.md`。

## 4. 关键选项（`mrtk post`）

| 项 | 作用 |
| --- | --- |
| `-k` / `--config` | TOML（或旧 conf）；CLI 覆盖文件 |
| `-p MODE` | 0 single … 2 kinematic … 6/7 ppp-* |
| `-sys G,R,E,…` | 星座 |
| `-f N` | 相对定位频率数 |
| `-o FILE` | 输出 `.pos`（默认 stdout） |
| `-ts`/`-te`/`-ti` | 时间窗 / 采样 |
| `-h` | **fix-and-hold AR**（不是帮助） |
| `-?` / `--help` | 帮助 |
| `-e`/`-a`/`-n` | ECEF / ENU 基线 / NMEA |

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| 经典/explorer CLI 对照 | [rtklib](./rtklib.md) |
| 武大 GREAT XML PPP/RTK | [great-pvt](./great-pvt.md) |
| GA pea / YAML | [ginan](./ginan.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| 仅 CLAS/MADOCA 官方原树 | [claslib](./claslib.md) / [madocalib](./madocalib.md) |
| Python 开放 SSR 教学 | [cssrlib](./cssrlib.md) · HAS 页解码 [haslib](./haslib.md) |
| 工作流 D | QC → MRTKLIB 冒烟/增强 →（可选）PRIDE；教程 [06](../tutorials/06-iono-positioning.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `mrtk post -h` 行为怪 | `-h`=fix-and-hold | 帮助用 `mrtk post --help` 或 `-?` |
| 2 | CMake 找不到 LAPACK / 数值怪 | 未装或 ILP64 | `apt install liblapack-dev`；换 LP64 BLAS |
| 3 | 把 MRTKLIB 当 apt `rtklib` | 不同发行 | 用 `./build/mrtk --version`；对照 [rtklib](./rtklib.md) |
| 4 | CLAS 配置在日本外乱飘 | CLAS 覆盖日本 | 全球改 MADOCA/HAS/IGS；读 quickstart 表 |
| 5 | 实时 RSS 曾近 GB | 旧版 `rtcm_t` 内嵌大块 | 升 **≥0.7.9**（懒分配）；看 release notes |
| 6 | kinematic 固定率骤降 | v0.6.10–0.7.7 周跳回归 | 用 **≥0.7.8**（本机 v0.7.10） |
| 7 | BDS-3 B2b MSM 全丢 | 旧信号表空槽 | 用 **≥0.7.10** |
| 8 | TOML 与 CLI `-p` 不一致 | CLI 覆盖文件 | 改一种来源；先 `grep mode conf/...` |
| 9 | 与 explorer `.pos` 差大 | 权重/周跳/改正轴不同 | 同 OBS 先两边 `-p 0` 对齐再比 RTK |
| 10 | 期望 Python `import mrtklib` | 无官方 pip 绑定 | 脚本调 CLI；或 [pyrtklib](./pyrtklib.md)（仅 2.4.3） |
| 11 | `mrtk run` 无流 | 挂载/口令/NTRIP 未配 | 先 `post` 离线冒烟；NTRIP 见 `docs/guide/ntrip.md` |
| 12 | 把 Q=1 当全球 PPP-AR | 样例是短基线相对 | PPP-AR 走 `conf/madocalib/*_pppar*.toml`+产品 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| CLAS/MADOCA/HAS/IGS 一体、现代 CMake | **本文 MRTKLIB** |
| 日常/explorer 低成本 RTK CLI | [rtklib](./rtklib.md) |
| 武大 GREAT | [great-pvt](./great-pvt.md) |
| GA 精密 pea | [ginan](./ginan.md) |
| Python 绑 2.4.3 C | [pyrtklib](./pyrtklib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |

## 8. 相关

[rtklib](./rtklib.md) · [great-pvt](./great-pvt.md) · [ginan](./ginan.md) · [pride-pppar](./pride-pppar.md) · [madocalib](./madocalib.md) · [claslib](./claslib.md) · [cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [pyrtklib](./pyrtklib.md) · [README](./README.md)

- DOI：[10.5281/zenodo.20373746](https://doi.org/10.5281/zenodo.20373746)
- 直播看板（CLAS）：<https://live.pntmoni.com/>
