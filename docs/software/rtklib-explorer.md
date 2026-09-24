# RTKLIB-explorer · 低成本 GNSS 优化 fork（demo5→EX）操作手册

目录：[`PROJECTS.json` → `RTKLIB-explorer`](../../PROJECTS.json) · 上游 <https://github.com/rtklibexplorer/RTKLIB> · 博客/教程 <http://rtkexplorer.com/> · 手册 PDF <https://rtkexplorer.com/pdfs/manual_demo5.pdf> · tip **`06e8644`**（2026-08-31）· 产品串 **`rnx2rtkp RTKLIB EX 2.5.1`**（`VER_RTKLIB="EX"` / `PATCH_LEVEL="2.5.1"`）· 许可 **BSD-2-Clause**（`license.txt`，含 Takasu 版权）· 本机：`app/consapp/rnx2rtkp/gcc` + gcc **14.2.0** + `-lgfortran` → 二进制 **1115480** B；短样 SPP 3×Q=5；GSI 样例 SPP **120**×Q5 首点 **35.160874653°N 139.613828332°E h=70.5104**；RTK **115** 历元 Q1=**102**/Q2=**13**，首 fix **35.160872533°N 139.613836865°E h=69.8576** ratio≈**50.4** · **2026-09-24 06:30 EDT**

> 岗位：低成本板卡（尤其 u-blox 单/双/三频）事后/实时 RTK 与浮点 PPP 的**活跃社区 fork**。冲突时：**仓内 `readme.txt` / `-?` / rtkexplorer 博客 > 本文**。官方树总览与 PATH 陷阱总表仍见 [rtklib](./rtklib.md)；现代化 CLAS/MADOCA/`mrtk` → [mrtklib](./mrtklib.md)；Python 绑 2.4.3 → [pyrtklib](./pyrtklib.md)；基站整机 → [rtkbase](./rtkbase.md)。

**与 [rtklib.md](./rtklib.md) 的差别：** `rtklib.md` 同时覆盖 **apt 2.4.3 b34**、**tomojitakasu 原版**与 explorer，是「家族总入口」。**本页只钉 explorer/`main`（原 demo5）**：版本串是 **`EX 2.5.1`** 不是 `2.4.3 b34`；默认 makefile 开 **`NFREQ=4` `NEXOBS=3`** 与全星座宏；同 OBS 的 SPP/RTK 数值**不必**与 apt 或 [mrtklib](./mrtklib.md) 逐字段一致（权重/周跳/模糊度策略不同）。不要把本页当 MRTKLIB 或 B2b 专用树说明。

## 1. 用途与边界

**做：**

- 事后：`rnx2rtkp`（SPP / DGPS / kinematic / static / PPP…）
- 转换/转发：`convbin`、`str2str`；可选 Qt/Embarcadero GUI（RTKPOST/RTKNAVI…）
- 低成本场景：F9P 等配置见 `data/config/`（`f9p_*.conf`、都市基准 PPC/UrbanNav）
- Linux CLI：推荐 CMake；旧 `app/consapp/*/gcc` make 仍可用（README 标 DEPRECATED）

**不做：**

- **不是** Debian `apt install rtklib` 的同名二进制 → apt 仍是 **2.4.3 b34**，见 [rtklib](./rtklib.md) §2.0
- **不是** MRTKLIB（统一 `mrtk` + TOML + CLAS/MADOCA/HAS）→ [mrtklib](./mrtklib.md)
- **不是** 北斗 PPP-B2b 专用解码树 → [rtklib-b2b](./rtklib-b2b.md) / [b2blib](./b2blib.md)
- **不是** 发表级 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- 本机**未**重跑 PPC/UrbanNav 全基准计分 → 博客分数以 upstream readme 为准，**禁止臆造**都市固定率

一句话：RTKLIB-explorer = **面向低成本接收机的 RTKLIB-EX（原 demo5）**，日常 RTK 首选社区树。

| 术语 | 含义 |
| --- | --- |
| demo5 / EX | 历史分支名 demo5；**2025-07 起活动在 `main`**，CLI 常印 `RTKLIB EX` |
| `NFREQ=4` | 本机 gcc makefile 默认可到四频槽（对照 apt 常见 2） |
| Q | `.pos`：1 fix / 2 float / 5 single / 6 ppp… |
| `-h` | **fix-and-hold AR**（不是帮助） |

## 2. 安装 / 编译

### 2.1 依赖（CLI）

```bash
sudo apt-get update
sudo apt-get install -y build-essential git gfortran
# CMake 全量（含 Qt GUI）再装 cmake + Qt5/6 开发包；只要 rnx2rtkp 可走 §2.3
```

### 2.2 CMake（上游推荐）

```bash
git clone https://github.com/rtklibexplorer/RTKLIB.git
cd RTKLIB
git rev-parse --short HEAD   # 本机 06e8644
mkdir -p build && cd build
cmake ..
make -j"$(nproc)"
# 可选：make test / make install
```

### 2.3 仅 CLI 旧 make（本机验证路径）

```bash
cd RTKLIB/app/consapp/rnx2rtkp/gcc
make -j"$(nproc)"
./rnx2rtkp --version
# rnx2rtkp RTKLIB EX 2.5.1
./rnx2rtkp -? 2>&1 | head
```

本机 makefile 关键宏：`-DENAGLO -DENAQZS -DENAGAL -DENACMP -DENAIRN -DNFREQ=4 -DNEXOBS=3`。

### 2.4 Windows

Release 页预编译 zip；把含 `rnx2rtkp.exe` 的目录加入 PATH。GUI 走 Embarcadero 工程或 Qt（见 `readme.txt`）。

## 3. 端到端（本机）

### 3.1 短文件 SPP（georinex 样例）

```bash
EX=./app/consapp/rnx2rtkp/gcc/rnx2rtkp   # 相对仓根；或绝对路径
mkdir -p /tmp/ex_smoke && cd /tmp/ex_smoke
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
curl -fsSL -o 14601736.18n \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n
"$EX" -p 0 -sys G -m 5 -t -e -o out_ex.pos 14601736.18o 14601736.18n
head -12 out_ex.pos
```

**本机 EX：** 头 `% program   : rnx2rtkp ver.EX 2.5.1`；3 历元全 **Q=5**；首历元 ECEF  
`−4647138.1296  2562188.0337  −3526626.0207`。

**同命令 apt `ver.2.4.3 b34`：** 首历元  
`−4647152.8622  2562199.8251  −3526633.5232`（**≠ EX**）。归档必须写清 `% program` 行。

### 3.2 GSI 仓内样例 SPP / RTK（借 MRTKLIB 测试数据）

```bash
GS=/path/to/MRTKLIB/tests/data/rtklib/rinex   # 或自备同名 0759/3040
"$EX" -p 0 -sys G -f 1 -m 10 -o gsi_spp.pos \
  "$GS"/07590920.05o "$GS"/07590920.05n
"$EX" -p 2 -sys G -f 2 -m 15 -o gsi_rtk.pos \
  "$GS"/07590920.05o "$GS"/30400920.05o \
  "$GS"/07590920.05n "$GS"/30400920.05n
grep -v '^%' gsi_spp.pos | awk 'NF>=6{n++;q[$6]++} END{print n; for(k in q) print "Q"k,q[k]}'
```

**本机：**

| 模式 | 历元 | 质量 | 首历元（摘） |
| --- | ---: | --- | --- |
| SPP `-p 0` | **120** | 全 Q=**5** | **35.160874653** 139.613828332 **70.5104** |
| RTK `-p 2` | **115** | Q1=**102** Q2=**13** | 首行为 Q=2；首 **Q=1**：**35.160872533** 139.613836865 **69.8576** ratio≈**50.4** |

对照：同 OBS 上 apt SPP 首点 **35.160868346 / 139.613825769 / 83.8246**（与 EX **不一致**）；[mrtklib](./mrtklib.md) 同文件 SPP 对齐 apt、RTK 可到 **120**×Q1——**不要**用 EX 数值去对拍 MRTKLIB 文档里的字段。

### 3.3 都市 / F9P 配置（本机未跑全基准）

```bash
# 仓内 data/config/：f9p_ppk.conf、f9p_urban.conf、septentrio_urban.conf…
# PPC / UrbanNav 数据集与计分见 rtkexplorer 博客；CRX 解压需 PATH 中有 crx2rnx
```

## 4. 关键选项（`rnx2rtkp`）

| 项 | 作用 |
| --- | --- |
| `-k file` | 读 conf；**CLI 覆盖文件** |
| `-p MODE` | 0 single … 2 kinematic … 7/8/9 ppp-*（以本机 `-?` 为准） |
| `-sys G,R,…` | 星座 |
| `-f N` | 相对定位频率数 |
| `-m elev` | 截止高度角（°） |
| `-v thres` | AR 检验阈值（0=关） |
| `-h` | **fix-and-hold**（不是帮助） |
| `-?` / `--version` | 帮助 / `rnx2rtkp RTKLIB EX 2.5.1` |
| `-o` `-t` `-e`/`-a`/`-n` | 输出 / 时间戳 / ECEF·ENU·NMEA |

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| 家族总入口 / apt PATH | [rtklib](./rtklib.md) |
| 现代化 CLAS/MADOCA/`mrtk` | [mrtklib](./mrtklib.md) |
| Python 绑 2.4.3 | [pyrtklib](./pyrtklib.md)（另有 `pyrtklib_demo5` 绑 EX，见 PROJECTS） |
| Pi/SBC 基站 Web | [rtkbase](./rtkbase.md) |
| 北斗 B2b 专用树 | [rtklib-b2b](./rtklib-b2b.md) |
| 工作流 | QC → EX 冒烟 →（可选）PRIDE；教程 [06](../tutorials/06-iono-positioning.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `rnx2rtkp -h`「坏了」 | `-h`=fix-and-hold | 帮助用 `-?`；版本用 `--version` |
| 2 | `.pos` 头写 `2.4.3 b34` | PATH 命中 apt | `which -a rnx2rtkp`；调用 gcc 树绝对路径；看 `% program` |
| 3 | 与文档/同事 ECEF 对不上 | EX≠apt≠MRTKLIB 权重 | 先比 `% program`；同 OBS 先两边 `-p 0` |
| 4 | 仍 clone `demo5` 分支 | 分支已退役 | 用 **`main`**；旧脚本改 remote/branch |
| 5 | `make` 缺 gfortran | sofa/IERS 链 | `apt install gfortran` |
| 6 | GUI/`cmake` 缺 Qt | 未装开发包 | 只要 CLI 走 §2.3；GUI 按 readme 装 Qt 模块 |
| 7 | CRX 解压失败 | 缺 `crx2rnx` | 装 [rnxcmp](./rnxcmp.md)/[crx2rnx](./crx2rnx.md)；Linux 命令名常小写 |
| 8 | 把 EX 当 MRTKLIB | 入口/改正轴不同 | CLAS/HAS 一体用 [mrtklib](./mrtklib.md) |
| 9 | RTK 固定率低于博客 | 配置/数据非基准集 | 用 `data/config` 对应 conf + 官方数据集；勿抄都市分数 |
| 10 | 与 [rtkbase](./rtkbase.md) 混二进制 | 镜像可能捆不同 RTKLIB | 在 RTKBase 主机 `rnx2rtkp --version` 核对 |
| 11 | `pyrtklib` 期望 EX API | PyPI 绑 **2.4.3** | 用 [pyrtklib](./pyrtklib.md) 或 PROJECTS `pyrtklib_demo5` |
| 12 | 实时安全当担保 | AS IS、非认证 | 生产前自做故障注入；关键链路勿只靠社区 fork |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 低成本/u-blox 日常 RTK、活跃文档 | **本文 explorer / EX** |
| apt 快速冒烟 / 官方树对照 | [rtklib](./rtklib.md) |
| CLAS/MADOCA/HAS 一体现代 CLI | [mrtklib](./mrtklib.md) |
| Python 调 C 核心 | [pyrtklib](./pyrtklib.md) |
| 基站+Web+NTRIP 一键 | [rtkbase](./rtkbase.md) |
| 北斗 PPP-B2b 接收机二进制解码+PPP | [rtklib-b2b](./rtklib-b2b.md) |

## 8. 相关

[rtklib](./rtklib.md) · [mrtklib](./mrtklib.md) · [pyrtklib](./pyrtklib.md) · [rtkbase](./rtkbase.md) · [rtklib-b2b](./rtklib-b2b.md) · [great-pvt](./great-pvt.md) · [ginan](./ginan.md) · [pride-pppar](./pride-pppar.md) · [README](./README.md)

- 博客：<https://rtklibexplorer.wordpress.com/>
- Benchmarks 说明：仓内 `readme.txt`（PPC / UrbanNav；本机未复跑计分）
