# MatRTKLIB · MATLAB 调 RTKLIB/MALIB + GT 操作手册

目录：[`PROJECTS.json` → `MatRTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/taroz/MatRTKLIB> · tip **`69bcbd3`**（2025-03-08）· ★**100** · 许可 **MIT** · 语言 **MATLAB** · 本机（**2026-09-25 23:32–23:33 EDT** 质检复跑）：浅克隆；`+rtklib` **90**×`.m`+**90**×`.mexa64`（另捆 `.mexw64`/`.mexmaca64` 各 **90**）；`+gt` **48**×`.m`；`examples/` **35**×`.m`；`examples/data/static/rover.obs` **3488603** B / `base.obs` **3457028** B；`rover_rtk.pos` **301** 历元 **全 Q=1**，首行 **35.134699011°N 136.977575483°E h=104.8619** m @ **2024/06/24 08:20:00**；`examples/data/kinematic/rover.obs` **25495653** B；`rover_1Hz_rtk.pos` **531** 历元（Q1=**142**/Q2=**389**）；`src/RTKLIB`→**JAXA-SNU/MALIB**（未 `--recurse` 则空）；`which matlab` 空；Octave **9.4.0**：`xyz2llh`→undefined；`ldd +rtklib/xyz2llh.mexa64`→**libmx.so/libmex.so not found** · **未执行** MEX 解算 · **未臆造** 新坐标

> 岗位：在 **MATLAB** 中用 `rtklib.*`（MEX）调用 RTKLIB/MALIB，并用 `gt.*` 做 RINEX/解算结果分析与作图。冲突时：**仓内 README / `doc/manual.md` / 已提交 `.pos` > 本文**。  
> C CLI → [rtklib](./rtklib.md)；demo5/EX → [rtklib-explorer](./rtklib-explorer.md)；纯 Python PPK → [rtklib-py](./rtklib-py.md)；pybind C → [pyrtklib](./pyrtklib.md)；现代 `mrtk` → [mrtklib](./mrtklib.md)；另一 MATLAB 引擎 → [gogps-matlab](./gogps-matlab.md)。

**姊妹页差别：**

| 手册 | 本质 |
| --- | --- |
| [rtklib.md](./rtklib.md) | C CLI（`rnx2rtkp`/`convbin`） |
| [rtklib-explorer.md](./rtklib-explorer.md) | demo5→EX C 叉 |
| [rtklib-py.md](./rtklib-py.md) | **纯 Python** demo5-PPK |
| [pyrtklib.md](./pyrtklib.md) | Python 调官方 C（PyPI） |
| [mrtklib.md](./mrtklib.md) | 现代 C 树 + `mrtk` |
| [gogps-matlab.md](./gogps-matlab.md) | goGPS 整机 MATLAB |
| **本文 MatRTKLIB** | **MATLAB MEX 桥 + GT 分析层**（非 goGPS） |

## 1. 用途与边界

**做：**

- `rtklib.<func>`：几乎一函数一 MEX（`pntpos`/`rtkpos`/`readrnxobs`/`xyz2llh`…），向量化 I/O
- `gt.Gobs` / `Gnav` / `Gsol` / `Gpos` / `Grtk` / `Gopt` / `Gsat` / `Gtime`…：读写 RINEX、组合、残差、绘图
- `examples/`：含 `Example1_visualization_RINEX_observation.m`、`Example2_PPK_analysis.m`、`Example3_Positioning_error_analysis.m` 及步进/残差/编辑等共 **35** 脚本
- 可选 `compile.m`：自备 `mex -setup` 后重编（`-DENAGLO -DENAGAL -DENAQZS -DENACMP -DENAIRN -DNFREQ=7`，可选 `-DOBS_100HZ`）

**不做 / 本机限制：**

- **不是**无 MATLAB 的生产 CLI → [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md)
- **不是** goGPS PPP/NET 整机 → [gogps-matlab](./gogps-matlab.md)
- **不是** [rtklib-py](./rtklib-py.md) / [pyrtklib](./pyrtklib.md)
- **Octave 不能替代**：`.mexa64` 依赖 MATLAB `libmx`/`libmex`；`+rtklib/*.m` 多为帮助桩
- 本机无 MATLAB → **只盘点**仓内 `.obs`/`.pos`；**禁止**写成「本机 MEX 新跑」

一句话：MatRTKLIB = **科研向 MATLAB↔MALIB/RTKLIB 桥**；没许可证就别指望冒烟出解。

| 术语 | 含义 |
| --- | --- |
| `rtklib.*` | `+rtklib` 包：MEX 入口 |
| `gt.*` | `+gt`：**GNSS Tools** 类库 |
| MALIB | 子模块 `src/RTKLIB`（README：2025-01 起后端由 RTKLIB 切到 MALIB） |
| `.mexa64/.mexw64/.mexmaca64` | Linux / Win64 / Apple Silicon 预编译 |

## 2. vs 族内工具

| | **本文** | [rtklib](./rtklib.md) | [rtklib-explorer](./rtklib-explorer.md) | [rtklib-py](./rtklib-py.md) | [pyrtklib](./pyrtklib.md) | [mrtklib](./mrtklib.md) | [gogps-matlab](./gogps-matlab.md) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 运行时 | MATLAB+MEX | C CLI | C EX | 纯 Python | Python+C | C `mrtk` | MATLAB |
| 场景 | 教学/改示例+图 | 通用 | 低成本 RTK | 读 demo5 | 脚本调 C | SSR 现代树 | 站网 PPP/NET |
| 本机 | 盘点+Octave 负测 | apt/源码 | GSI 实跑 | 40 历元 | F9P | SPP/RTK | 无 MATLAB |

## 3. 安装

```bash
git clone --recursive https://github.com/taroz/MatRTKLIB.git
cd MatRTKLIB && git rev-parse --short HEAD   # 69bcbd3
# 已有仓缺后端：git submodule update --init --recursive
```

MATLAB：

```matlab
addpath('/path/to/MatRTKLIB');   % 仓库根；不要只加 +rtklib
% 预编译 MEX 已按平台提交；一般不必 compile.m
% 自编：mex -setup → compile.m（OneDrive/Dropbox 同步中易失败）
```

**Octave 负测（本机）：**

```bash
octave --eval "addpath(genpath('.')); xyz2llh([1 2 3])"
# → xyz2llh undefined
ldd +rtklib/xyz2llh.mexa64 | head -4
# libmx.so => not found ; libmex.so => not found
```

## 4. 端到端（有 MATLAB；本机仅参考解盘点）

```matlab
cd examples
Example1_visualization_RINEX_observation
Example2_PPK_analysis
Example3_Positioning_error_analysis
% 另有 estimate_position_*_step_by_step / compute_* / edit_rinex_* 等
```

**仓内参考解（只读校验，非本机 MEX stdout）：**

```text
examples/data/static/rover_rtk.pos
  301 epochs, Q=1 × 301
  2024/06/24 08:20:00.000  35.134699011  136.977575483  104.8619  Q=1  ns=42

examples/data/kinematic/rover_1Hz_rtk.pos
  531 epochs, Q1=142 / Q2=389
  first Q1: 2023/07/11 06:04:32.000  35.165360854  136.881409534  41.4069
```

无 MATLAB：换 [rtklib](./rtklib.md) / [rtklib-py](./rtklib-py.md) 对同一 RINEX；勿伪造 MEX 解。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS/NAV | `gt.Gobs`/`Gnav` 或 `rtklib.readrnx*` |
| 选项 | `gt.Gopt` / 示例 conf（RTKLIB 习惯） |
| 真值 | `examples/data/**/reference*`、`*_position.txt` |

| 输出 | 说明 |
| --- | --- |
| `gt.Gsol` / `.pos` | RTKLIB 风格解 |
| 图 | `plot` / 天空图等（需 MATLAB 图形） |
| KML | `convert_solution_to_kml.m` 等示例 |

## 6. 编译开关速查

| 项 | 值 |
| --- | --- |
| 星座宏 | `ENAGLO GAL QZS CMP IRN` |
| `NFREQ` | **7** |
| `OBS_100HZ` | `compile.m` 可选 |
| `TRACE` | 调试迹 |
| 后端 | **MALIB** 子模块 |

## 7. 接到哪步

1. 无 MATLAB → [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md) / [rtklib-py](./rtklib-py.md)  
2. Python↔C → [pyrtklib](./pyrtklib.md)  
3. CLAS/MADOCA/HAS → [mrtklib](./mrtklib.md)  
4. MATLAB 站网 → [gogps-matlab](./gogps-matlab.md)  
5. 观测准备 → [georinex](./georinex.md) / [anubis](./anubis.md)

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | Octave 调 MEX 失败 | 绑 MATLAB 运行时 | 装 MATLAB；或换 [rtklib-py](./rtklib-py.md) |
| 2 | `invalid call to script xyz2llh.m` | `.m` 是帮助桩 | 确认同名 `.mex*` 在 path |
| 3 | `libmx.so not found` | 无 MATLAB 共享库 | 从 MATLAB 启动 |
| 4 | 与 goGPS API 混用 | 同语言不同工程 | `rtklib`/`gt` ≠ goGPS `Core` |
| 5 | `compile` 缺头文件 | 子模块空 | `git submodule update --init --recursive` |
| 6 | 文档仍写死 RTKLIB 2.4.3 路径 | 后端已切 MALIB | 读 README Updates（2025-01） |
| 7 | OneDrive 下 mex 失败 | 同步锁文件 | 停同步或拷本地盘 |
| 8 | 只 `addpath('+rtklib')` | 包路径语义 | `addpath` **仓库根** |
| 9 | 把仓内 `.pos` 当本机新解 | 无 MATLAB | 写明「仓内参考」 |
| 10 | 与 [pyrtklib](./pyrtklib.md) 混名 | 生态不同 | pip 包 ≠ 本仓 |
| 11 | 当实时 NTRIP 引擎 | 示例偏事后 | 实时 → [rtklib](./rtklib.md) `str2str` / [rtkbase](./rtkbase.md) |
| 12 | 32 位 OS | 无预编译 | 自 mex；上游主维 64 位 |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| MATLAB 调 RTKLIB + 图/改示例 | **本文 MatRTKLIB** |
| 无 MATLAB 读 demo5-PPK | [rtklib-py](./rtklib-py.md) |
| 生产/低成本 CLI | [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md) |
| Python 调 C | [pyrtklib](./pyrtklib.md) |
| MATLAB 站网 PPP/NET | [gogps-matlab](./gogps-matlab.md) |
| 开放 SSR 现代树 | [mrtklib](./mrtklib.md) |

## 10. 相关

[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md) · [rtklib-py](./rtklib-py.md) · [pyrtklib](./pyrtklib.md) · [mrtklib](./mrtklib.md) · [gogps-matlab](./gogps-matlab.md) · [georinex](./georinex.md) · [README](./README.md)
