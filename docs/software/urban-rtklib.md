# Urban-RTKLIB · 城市向 PPP/PPP-RTK（demo5 改版）操作手册

目录：[`PROJECTS.json` → `Urban-RTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/MayHarryWang/Urban-RTKLIB> · tip **`5d128ef`**（2025-10-13，几乎仅 README）· ★**25** · 许可 **无根 LICENSE**（`rtklib.h` 保留 Takasu 版权声明；引用 ION GNSS+ 2025 文）· 语言 **C/C++** · `VER_RTKLIB="demo5"` / `PATCH_LEVEL="b34i"` · 本机（**2026-09-25 23:32–23:33 EDT** 质检复跑）：`gcc/g++` **14.2.0**，CMake **3.31.6**；`find_package(GTSAM REQUIRED)`；安装 `libgtsam-dev` 后仍缺导出的 **`libCppUnitLite.a`** → **官方 CMake 失败**；去掉 GTSAM 试编 → `rtkcmn.c` 使用 **`insopt_t`**，公开头 **无完整 INS/FGO 类型**，`prcopt_t` 与默认初始化体不一致 → **目标 `cssr_rtklib_urban` 编不过**；`config/` **15**×`.conf`；增量源含 `fde.c`/`ppprtk.c`/`hascssr.c`/`mdccssr.c`/`bdscssr.c`/`gflib.c`/`quaternion.c`…；**无**仓内 RINEX；**无**二进制冒烟 · **未臆造** `.pos`

> 岗位：在 **RTKLIB demo5 b34i** 血统上做城市 **PPP / PPP-RTK / FDE**（文档还宣称 FGO/INS）。冲突时：**`config/*.conf` + `include/rtklib.h` + 论文 > 空 README**。  
> 官方树 → [rtklib](./rtklib.md)；低成本 EX → [rtklib-explorer](./rtklib-explorer.md)；现代 CLAS/HAS → [mrtklib](./mrtklib.md)；纯 Python → [rtklib-py](./rtklib-py.md)。

**姊妹页差别：**

| 手册 | 本质 |
| --- | --- |
| [rtklib.md](./rtklib.md) | 上游/发行 CLI |
| [rtklib-explorer.md](./rtklib-explorer.md) | demo5→**EX 2.5.x** |
| [mrtklib.md](./mrtklib.md) | 模块化 `mrtk` + TOML |
| [rtklib-py.md](./rtklib-py.md) | 纯 Python PPK 子集 |
| **本文 Urban-RTKLIB** | **城市/PPP-RTK/FDE 研究叉**；CMake 目标 `cssr_rtklib_urban`，`PROGNAME` 仍为 `rnx2rtkp` |

## 1. 用途与边界

**做（据头文件/源/配置；非本机跑通）：**

- 事后定位：`main.cpp` ≡ `rnx2rtkp` 用法（`-k conf -o out.pos obs…`）
- 模式扩展：`PMODE_PPP_RTK=10`，`PMODE_PPP_*_GRAPH=11/12`，`PMODE_INS_*=13…17`
- FDE：`FDEOPT_*`（code/phase/meas NIS）← `src/fde.c`
- SSR：`hascssr.c`（HAS）、`mdccssr*.c`/`mdciono.c`（MADOCA）、`bdscssr.c`（BDS）
- PPP-RTK：`ppprtk.c`；模糊度试验 `ppp_ar_dev*.c`；`config/` 含 kine/static/graph/INS/triple 等 **15** 套

**不做 / 本机硬限制：**

- **不是**可 `apt` 的发行版，也 **不是**已验证 EX 二进制 → [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md)
- **不是** [mrtklib](./mrtklib.md)
- 公开树 **不完整**：FGO 头被注释；`insopt_t` 等缺失；GTSAM **REQUIRED** 但源中几乎无 gtsam include
- **无样例观测** → 即使编过也无仓内 E2E
- README 几乎只有 citation → 操作靠 conf/头文件

一句话：Urban-RTKLIB = **论文配套城市 PPP/PPP-RTK 研究叉**；本机 = **编不过、无数据**。

| 术语 | 含义 |
| --- | --- |
| `cssr_rtklib_urban` | CMake 可执行名 |
| `rnx2rtkp` | `PROGNAME`（帮助/迹前缀） |
| `demo5`/`b34i` | 版本烙印（explorer 血统） |
| FDE | NIS 新息故障探测 |
| GRAPH 模式 | 头文件 FGO 位；公开树实现不完整 |

## 2. vs stock / explorer / mrtklib

| | **本文** | [rtklib](./rtklib.md) | [rtklib-explorer](./rtklib-explorer.md) | [mrtklib](./mrtklib.md) |
| --- | --- | --- | --- | --- |
| 血统 | demo5 **b34i** 改 | 官方 | demo5→EX | 重写式现代树 |
| 重点 | 城市 PPP-RTK/FDE/SSR | 通用 | 低成本机 | CLAS/MADOCA/HAS |
| 构建 | CMake+**GTSAM** | Make | Make | CMake/`mrtk` |
| 本机 | **无二进制** | apt/源码 | GSI 实跑 | SPP/RTK 实跑 |

## 3. 安装 / 构建（诚实）

```bash
git clone https://github.com/MayHarryWang/Urban-RTKLIB.git
cd Urban-RTKLIB && git rev-parse --short HEAD   # 5d128ef
sudo apt-get install -y cmake g++ libgtsam-dev libboost-timer-dev
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
# 本机：GTSAMConfig → 缺 libCppUnitLite.a → Configuring incomplete
```

**本机失败摘要：**

```text
1) find_package(GTSAM) → imported target 缺 libCppUnitLite.a
2) 注释 GTSAM 后 make → rtkcmn.c: unknown type name 'insopt_t'
   （公开 rtklib.h 与 .c 不同步；FGO include 被注释）
⇒ 无 cssr_rtklib_urban；无 -h；无 .pos
```

有作者完整私有树时：对齐其 GTSAM 前缀并确认 INS/FGO 头来源——**不要**假设 GitHub 默认树可复现论文图。

## 4. 端到端（配置级；无本机解）

设计意图（对齐 `main.cpp` 帮助）：

```bash
# 编通后（本机未达到）：
./cssr_rtklib_urban -k ../config/ppp_kine.conf -o urban.pos rover.obs base.obs rover.nav
./cssr_rtklib_urban -k ../config/ppprtksd_static_triple.conf -o out.pos ...
```

| conf（节选） | 意向 | 备注 |
| --- | --- | --- |
| `ppp_kine.conf` | PPP-kine（mode 7） | `fdeopt` 开 |
| `ppp_graph.conf` | mode **11** graph | FGO 位 |
| `ppprtksd_static_triple.conf` | `ppp-rtk` | PPP-RTK |
| `ppprtkins_graph.conf` | mode **17** INS-graph | 需完整 INS |
| `sample_pppar_iono.conf` | ppp-kine | 电离层试验 |

**本机 E2E：** 无二进制、无 RINEX → **无坐标/固定率**。要出解请用 [rtklib-explorer](./rtklib-explorer.md) / [mrtklib](./mrtklib.md)。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS/NAV | 同 `rnx2rtkp`；相对模式需 base |
| SP3/CLK/SSR | conf：`pos1-sateph=brdc+ssrapc|precise-com|…` |
| `-k conf` | `config/*.conf`（含扩展 `fdeopt` 等） |

| 输出 | 说明 |
| --- | --- |
| `.pos` | 解（含 `SOLQ_PPPRTK` 等扩展质量） |
| `.trace` | `-x` 调试 |
| FGO/INS | 头文件有开关；公开树未必链上 |

## 6. 参数速查（扩展）

| 键 / 宏 | 含义 |
| --- | --- |
| `pos1-posmode` | 0–9 经典；**10** PPP-RTK；**11–12** GRAPH；**13–17** INS |
| `pos1-fdeopt` | 0 off / 1–3 NIS 类（部分 conf 写 `on`） |
| `pos1-doppler_vel` | Doppler 速度辅助 |
| `pos1-sateph` | brdc / precise / brdc+ssrapc / precise-com… |
| `out-outdops` / `out-outvel` | 额外输出 |

## 7. 接到哪步

1. 先要可跑 RTK/PPP CLI → [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md)  
2. 开放 SSR 一体 → [mrtklib](./mrtklib.md) / [cssrlib](./cssrlib.md)  
3. 读算法 → [rtklib-py](./rtklib-py.md)  
4. 发表级 PPP-AR → [pride-pppar](./pride-pppar.md)  
5. 城市多路径机理（不同问题）→ [mpsim](./mpsim.md) / [gnssrefl](./gnssrefl.md)

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | CMake 缺 `libCppUnitLite.a` | Debian GTSAM 导出残缺 | 自编 GTSAM；或改 CMake |
| 2 | 去 GTSAM 仍编译挂 | 公开头缺 `insopt_t` | 向作者要完整树 |
| 3 | 当 explorer EX 用 | 无 release 二进制 | 另装 [rtklib-explorer](./rtklib-explorer.md) |
| 4 | 与 [mrtklib](./mrtklib.md) 混命令 | `mrtk` ≠ `rnx2rtkp` 壳 | 分清仓与 conf |
| 5 | README 几乎空 | 只有 citation | 读 `config/`+`rtklib.h` |
| 6 | 无样例 RINEX | 研究仓未附数据 | 自备城市 OBS+SSR |
| 7 | GRAPH/INS conf 必挂 | FGO 头注释、实现缺 | 先用非 graph conf |
| 8 | `fdeopt=on` vs 0–3 | conf 风格不统一 | 对照 `FDEOPT_*`/`options.c` |
| 9 | 许可不清 | 无根 LICENSE | 遵 Takasu 声明 + 引 ION 文；商用自审 |
| 10 | tip 几乎只动 README | 代码可能另渠 | 锁 **`5d128ef`** 并记录私有补丁 |
| 11 | 当 GNSS-IR/多路径仿真 | 定位叉 ≠ 反射 | → [gnssrefl](./gnssrefl.md)/[mpsim](./mpsim.md) |
| 12 | 期望本文给城市固定率 | 本机无二进制 | **禁止臆造**；有环境再填实测 |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 研究城市 PPP-RTK/FDE 源码与 conf | **本文（源码级）** |
| 今天就要 `.pos` | [rtklib-explorer](./rtklib-explorer.md) / [rtklib](./rtklib.md) / [mrtklib](./mrtklib.md) |
| CLAS/MADOCA/HAS 现代 CLI | [mrtklib](./mrtklib.md) |
| 读 demo5 算法 | [rtklib-py](./rtklib-py.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |

## 10. 相关

[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md) · [mrtklib](./mrtklib.md) · [rtklib-py](./rtklib-py.md) · [pyrtklib](./pyrtklib.md) · [cssrlib](./cssrlib.md) · [pride-pppar](./pride-pppar.md) · [mpsim](./mpsim.md) · [README](./README.md)
