# raPPPid · VieVS MATLAB PPP 操作手册

目录：[`PROJECTS.json` → `raPPPid`](../../PROJECTS.json) · 上游 <https://github.com/TUW-VieVS/raPPPid> · Wiki <https://vievswiki.geo.tuwien.ac.at/en/raPPPid> · 许可 **GPL-3.0** · tip **`28fd517`** / tag **v5.1**（2026-07-29）· `DEF.ver='5.1'` · 本机验证：clone 树 **633** 个 `.m`；`WORK/PARAMETERS` **9** 个预设 `.mat`；`Path.m` / `raPPPid.m` / `PPP_main.m`（476 行）齐全 · **无 MATLAB/Octave → 未跑 GUI/PPP 解算**（禁止臆造坐标/固定率）· 2026-09-24 05:27 EDT

> 岗位：TU Wien **VieVS PPP** 模块——GUI 驱动、多模型/多产品精密单点（浮点与 PPP-AR、手机/实时扩展）。冲突时：**Wiki + 仓内 `DEF.m` / `Path.m` > 本文**。无 MATLAB 时换 [pride-pppar](./pride-pppar.md) / [great-pvt](./great-pvt.md) / [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 多 GNSS **PPP / PPP-AR**（含 Decoupled Clock 等）；批处理与 Multi-Plot
- 自动拉观测/产品（`DownloadDaily30sIGS` 等）；预设参数 `.mat`
- 低成本/智能手机原始测量；实时/准实时扩展（见 Wiki RT）

**不做：**

- **不是** 无 MATLAB 的 CLI 引擎 → [pride-pppar](./pride-pppar.md) / [great-pvt](./great-pvt.md) / [rtklib](./rtklib.md) / [ginan](./ginan.md)
- **不是** STEC/ROTI 主链 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- 本页 **不能** 提供本机 PPP 坐标数字——质检机无 MATLAB

一句话：raPPPid = **VieVS 体系下的 MATLAB 精密单点定位包（强依赖商业 MATLAB）**。

| 术语 | 含义 |
| --- | --- |
| `raPPPid` | `WORK/raPPPid.m`：启动 GUI |
| `DEF.ver` | `CODE/COMMON/DEF.m` 版本串（本机 **5.1**） |
| `Path.DATA` / `Path.RESULTS` | 相对 `WORK/` 的数据与结果根 |
| `settings.mat` / `PARAMETERS/*.mat` | GUI 参数快照与官方预设 |

## 2. 安装（诚实：需要 MATLAB）

### 2.1 硬依赖

| 组件 | 说明 |
| --- | --- |
| **MATLAB**（较新版本） | **必需**；上游在 Windows 测得多，Linux 可用 |
| Parallel Toolbox（可选） | `bool_parfor`；无则关并行 |
| 网络 | 首次处理常自动下轨道/钟差/偏差/VMF 等 |
| CDDIS / IGS 镜像账号 | 部分源需 Earthdata 等（见 Wiki First launch） |

本机（Debian 共享 CI）：`which matlab` → 空；**Octave 不能当替代品**（GUI/`GUIDE`/大量工具箱）。

### 2.2 Clone（本机已做）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/TUW-VieVS/raPPPid.git
cd raPPPid && git rev-parse --short HEAD && git describe --tags --always
# 28fd517 / v5.1
rg -n "ver\s*=" CODE/COMMON/DEF.m
# ver = '5.1'
find CODE -name '*.m' | wc -l          # 633
ls WORK/PARAMETERS
ls DATA                                 # ANTEX BIASES … OBS ORBIT TROPO …
```

### 2.3 启动 GUI（有 MATLAB 的机器）

```matlab
cd('.../raPPPid/WORK')   % 必须 WORK，不是仓库根
raPPPid                  % 或 raPPPid()
```

期望命令窗打印版本横幅（含 `DEF.version`）并打开 GUI。若不在 `WORK/`：`Please change the Matlab work folder to raPPPid/WORK/`。

## 3. 端到端（上游 Wiki 流程；本机未解算）

下列步骤摘自 Wiki [First PPP](https://vievswiki.geo.tuwien.ac.at/en/raPPPid/Examples/my_first_PPP) 与 README。**期望图/坐标以你本机 MATLAB 为准，勿抄造数字。**

### 3.1 拉一日 IGS 观测

```matlab
% GUI 已启动、路径已 addpath 之后：
DownloadDaily30sIGS({'GRAZ00AUT'}, 001, 2020)
% host 可选 1=BKG 2=CDDIS 3=IGN 4=bdsmart；省略则轮询
% 或：CopyData2Folders() 拷本地 RINEX 进 DATA/OBS 树
```

### 3.2 GUI 首次浮点 PPP

1. File 面板 `...` 选 `DATA/OBS/.../GRAZ00AUT_R_20200010000_01D_30S_MO.rnx`（或长名）
2. 仅勾 GPS；L1/L2
3. 可加载 `WORK/PARAMETERS/pppar_code_mgex.mat` 等预设（AR 另见 Wiki）
4. **RUN** → 坐标简图；Single-Plot 面板加深图
5. `OpenResultsFolder()` 查看 `RESULTS/`

### 3.3 本机可复现的结构冒烟（无 MATLAB）

```bash
cd ~/iono_ops/raPPPid
test -f WORK/raPPPid.m && test -f WORK/Path.m && test -f CODE/PPP_main.m
ls WORK/PARAMETERS/*.mat | wc -l    # 9
head -n 5 DATA/COORDS/Coords.txt
wc -c DATA/OceanLoading.blq         # 本机 339510
```

| 预设 `.mat`（`WORK/PARAMETERS/`） | 用途（文件名示意） |
| --- | --- |
| `pppar_code_mgex.mat` / `pppar_code_rapid.mat` | CODE MGEX / rapid PPP-AR |
| `pppar_cnes.mat` | CNES 产品线 |
| `CNES_postprocessed_igs14.mat` / `_igs20.mat` | CNES 事后 + IGS14/20 |
| `DCM_WUM_rapid.mat` | Decoupled Clock + WUM rapid |
| `manually_TUG.mat` | TUG 手工产品 |
| `smartphone_postprocess.mat` / `_realtime.mat` | 手机事后/实时 |

| 输入 | 说明 |
| --- | --- |
| RINEX OBS（`DATA/OBS`） | 日文件；可用下载函数写入 |
| SP3/CLK/BIA/ATX/VMF… | 多数自动下载到 `DATA/*` |
| `settings` / 预设 `.mat` | 模型与估计开关 |

| 输出 | 含义 |
| --- | --- |
| `RESULTS/...` | 坐标序列、残差、固定状态等（以 GUI Export 为准） |
| 图窗 | Single / Multi-Plot |

## 4. 关键开关（GUI / settings）

| 项 | 作用 |
| --- | --- |
| GNSS / 频率勾选 | 系统与频点；教学先 GPS L1+L2 |
| Orbit/Clock 源 | IGS final / rapid / CNES / WUM… |
| Biases | DCB/OSB；AR 需匹配产品 |
| Ionosphere | 估计/约束/模型（见 Wiki Models） |
| Troposphere | VMF1/V3GR 等；网格自动下 |
| Ambiguity Fixing | 浮点 vs PPP-AR / DCM |
| Resets | 整点重置 → Multi-Plot 看收敛 |
| `bool_parfor` | 并行；无工具箱则关 |

## 5. 接到哪步

- 无 MATLAB / 批处理发表坐标 → [pride-pppar](./pride-pppar.md)；XML 滤波 → [great-pvt](./great-pvt.md)；轻量 → [rtklib](./rtklib.md)；GA → [ginan](./ginan.md)
- 重力+网解科研栈 → [groops](./groops.md)
- 产品/观测下载对照 → [data-access](../data-access.md) / [gampii-good](./gampii-good.md)
- 工作流 **D**：QC →（可选本文 MATLAB PPP）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `change ... to raPPPid/WORK/` | cwd 在仓库根 | `cd WORK` 再 `raPPPid` |
| 2 | `Path.DATA is not existing` | 动过目录树 / 错 Path | 恢复 `DATA/`；只改 `WORK/Path.m` |
| 3 | 下载 OBS 失败 | 镜像/账号 | `DownloadDaily30sIGS(..., host)` 试 1–4；CDDIS 配 Earthdata（Wiki First launch） |
| 4 | 缺轨道/钟差中途退出 | 自动下载被挡 | 查 `DATA/ORBIT`/`CLOCK`；换产品源或手动放入 |
| 5 | AR 不固定 / 乱跳 | 偏差产品与频点不配 | 换 `pppar_*.mat`；先浮点对照 |
| 6 | `parfor` / 并行报错 | 无 Parallel Toolbox | GUI 关并行；或装工具箱 |
| 7 | Linux 上 7-zip 路径错 | `Path.ZIP7` 指向 `7za.exe` | 装 `p7zip-full` 并改 `Path.m` 或用系统 `7z` |
| 8 | 把 Wiki 截图坐标当本机结果 | 环境不同 | **禁止**转载未复现数字；自跑再记 |
| 9 | 与 [pride-pppar](./pride-pppar.md) 差大 | 产品/天线/约束不同 | 同 SP3/CLK/ATX；比收敛后段 |
| 10 | 期望出 STEC | 软件是 PPP | TEC→[pytecgg](./pytecgg.md) |
| 11 | Octave 跑挂 | 非官方支持 | 装正版 MATLAB；或换 [rtklib](./rtklib.md) |
| 12 | 旧 clone 怪 bug | 未拉 v5.1 | `git pull`；仍坏则寄 `settings.mat`+RINEX 到 rapppid@geo.tuwien.ac.at |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| MATLAB GUI PPP / 教学改模型 | **本文 raPPPid**（需许可证） |
| 发表级 PPP-AR（Fortran/CLI） | [pride-pppar](./pride-pppar.md) |
| 武大 GREAT XML 滤波 | [great-pvt](./great-pvt.md) |
| 轻量 CLI | [rtklib](./rtklib.md) |
| 大地测量网解/重力 | [groops](./groops.md) |

## 8. 相关

[pride-pppar](./pride-pppar.md) · [great-pvt](./great-pvt.md) · [rtklib](./rtklib.md) · [ginan](./ginan.md) · [groops](./groops.md) · [glab-upc](./glab-upc.md) · [data-access](../data-access.md) · [README](./README.md)

- 论文：Glaner & Weber, 2023, *GPS Solutions* 27:174；学位论文 DOI 10.34726/hss.2022.73610
- Wiki TOC：Examples（first PPP / batch / PPP-AR / DCM / smartphone / RT）+ GUI 全页
