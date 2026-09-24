# goGPS_MATLAB · 低成本/多星座 GNSS 处理操作手册

目录：[`PROJECTS.json` → `goGPS_MATLAB`](../../PROJECTS.json) · 上游 <https://github.com/goGPS-Project/goGPS_MATLAB> · 站点 <https://gogps-project.github.io> · 许可 **GPL-3.0**（`source/LICENSE.txt`）· tip **`a990ed0`**（2025-05-28）· `Core.APP_VERSION = '1.0.1'` · 本机验证：clone 后 **824** 个 `.m`（`source/` 排除 thirdParty **427**）；`lambda_v3/` **仅** README（须自向 Curtin 申请 LAMBDA 3.0）；默认工程 ZIM3 RINEX3 day1 **2880** 历元；首见 G01 `C1C=25131594.344` @ 00:25:30 · **无 MATLAB → 未跑 GUI/PPP/NET**（禁止臆造坐标/固定率）· 2026-09-24 05:36 EDT · **质检复跑** 2026-09-24 05:41 EDT（tip **`a990ed0`**/`APP_VERSION=1.0.1`；824 `.m`/427 非 thirdParty；`lambda_v3` 仅 README；ZIM3 day1 **2880** 历元/`MARKER ZIM3`/`TRIMBLE NETR9`；G01 首见 C1C=**25131594.344** @ 00:25:30；`which matlab` 空→**未跑 GUI/PPP/NET**）

> 岗位：GReD / goGPS Project 的 **MATLAB** 观测处理——组合/非组合 LS、**PPP** 与 **NET**、永久站与低成本接收机。冲突时：**Wiki Installation/Command-language + 仓内 `goGPS.m` > 本文**。无 MATLAB → [rtklib](./rtklib.md) / [graphgnsslib](./graphgnsslib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)。

## 1. 用途与边界

**做：**

- 多星座、多频、多 tracking 的 RINEX 处理（自低频单频低成本起家，现已多系统）
- 两大 LS 引擎：**组合**（如无电离层）与 **非组合**（电离层作参数）
- 命令语言批处理：`LOAD` → `PREPRO` → `PPP` / `NET`；并行 `PAR`；导出/绘图 `EXPORT`/`SHOW`
- SEID/SID 电离层相关命令；多路径 `MPEST`；默认工程含 ZIM2/ZIMM/ZIM3 样例

**不做：**

- **不是** 无 MATLAB 的 CLI 引擎 → [rtklib](./rtklib.md) / [graphgnsslib](./graphgnsslib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 运动载体动态定位（README：**尚不支持** moving receivers）
- **不是** 把 Octave 当官方运行时（GUI / 新版语法 / 工具箱）
- 本页 **无** 本机 PPP 坐标——质检机无 MATLAB

一句话：goGPS_MATLAB = **GPL 的 MATLAB GNSS 实验室引擎（强依赖商业 MATLAB + 可选 LAMBDA）**。

| 术语 | 含义 |
| --- | --- |
| `goGPS` | `source/goGPS.m`：启动 GUI / Core 单例 |
| `Core.APP_VERSION` | 本机 **1.0.1** |
| `settings_PPP.ini` | 默认 PPP 工程配置（`data/project/default/config/`） |
| LAMBDA v3 | 模糊度固定库；**不可再分发**，须自向 Curtin 申请 |
| goGPS_Java | 同项目 JVM 实现 → PROJECTS.json `goGPS_Java`（非本文） |

## 2. 安装（诚实：需要 MATLAB）

### 2.1 硬依赖

| 组件 | 说明 |
| --- | --- |
| **MATLAB ≥ R2016a** | **必需**；上游避免专有 toolbox / mex |
| GUI Layout Toolbox | GUI 必需；仓内已捆 `source/utility/thirdParty/guiLayoutToolbox/`，首次仍可能提示安装 |
| LAMBDA 3.0（可选，AR） | <http://gnss.curtin.edu.au/research/lambda.cfm> → 解压到 `source/positioning/lambda/lambda_v3/` |
| aria2（可选） | 加速自动下载；Debian：`sudo apt-get install -y aria2` |
| Google Maps API（可选） | 地图底图；无 key 则关相关图 |

本机：`which matlab` → 空；**Octave ≠ 替代品**。

### 2.2 Clone（本机已做）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/goGPS-Project/goGPS_MATLAB.git
cd goGPS_MATLAB && git rev-parse --short HEAD
# a990ed0
find . -name '*.m' | wc -l                                 # 824
find source -name '*.m' ! -path '*/thirdParty/*' | wc -l    # 427
rg -n "APP_VERSION" source/obj/Core.m
# APP_VERSION = '1.0.1';
ls source/positioning/lambda/lambda_v3/
# 仅 LAMBDA_v3_README.txt → 未放入正版 LAMBDA 前不要开 AR
ls data/project/default/config/
# parallel_settings_PPP.ini settings_BSL.ini settings_NET.ini settings_PPP.ini
ls data/project/default/RINEX/ | head
```

### 2.3 启动 GUI（有 MATLAB 的机器）

Wiki 目录名写 `goGPS/`；当前仓库入口是 **`source/`**：

```matlab
cd('.../goGPS_MATLAB/source')   % 不是仓库根
goGPS                           % 或 goGPS('.../path/to.ini')
```

期望：彩色 header + GUI。缺 GUI Layout 时按提示装。工作目录勿停在仓库根，否则相对 `data/` 路径会裂。

## 3. 端到端

### 3.1 GUI / 命令语言 PPP（上游流程；本机未解算）

配置见 `data/project/default/config/settings_PPP.ini`（`version="1.0b9"` 为**配置文件**世代，与 `APP_VERSION` 不同）。样例站 **ZIM3/ZIM2/ZIMM**，会话窗默认 2021-01-01…04。

有 MATLAB 时的最小命令思路（具体关键字以 Wiki Command-language 为准）：

```text
LOAD
PREPRO
PPP
EXPORT
```

或 GUI：选 default PPP 工程 → 检查 Resources（SP3/CLK/ATX 自动下）→ 跑 PPP。
**坐标/固定率以你本机为准，禁止抄造。**

`flag_ppp_amb_fix` 在默认 ini 为 **0**；要 AR 须合法放入 LAMBDA v3 并改 ini。

### 3.2 本机可复现：树冒烟 + 样例 RINEX 探活（无 MATLAB）

```bash
cd ~/iono_ops/goGPS_MATLAB
test -f source/goGPS.m && test -f source/obj/Core.m
test -f source/positioning/lambda/lambda_v3/LAMBDA_v3_README.txt
# 样例 RINEX3（ZIM3 / Trimble NETR9）
python3 - <<'PY'
from pathlib import Path
p = Path('data/project/default/RINEX/ZIM300CHE_R_20210010000_01D_30S_MO.rnx')
lines = p.read_text(errors='replace').splitlines()
epochs = [l for l in lines if l.startswith('>')]
print('epochs', len(epochs), 'bytes', p.stat().st_size)
first = None
for j, l in enumerate(lines):
    if not l.startswith('>'):
        continue
    k = j + 1
    while k < len(lines) and not lines[k].startswith('>'):
        if lines[k].startswith('G01'):
            first = (l.strip(), lines[k][3:19].strip())
            break
        k += 1
    if first:
        break
print('first G01', first)
PY
# 期望：epochs 2880；first G01 @ 00:25:30；C1C=25131594.344
```

**本机结果（质检复跑 2026-09-24 05:41 EDT）：** day1 **2880** 历元（30 s；文件 **18271978** B）；`MARKER ZIM3`；`REC TRIMBLE NETR9`；G01 首见 `C1C=25131594.344` @ `> 2021  1  1  0 25 30`。同目录另有 `zim2*.21o` / `zimm*.21o` 短名日文件。

可选：用 [georinex](./georinex.md) 再探 —— 本机曾读 ZIM3 GPS **2880** 历元 / **31** SV（全量读较慢，CI 可用上面纯解析）。

### 3.3 I/O 表

| 输入 | 说明 |
| --- | --- |
| RINEX OBS（`data/project/.../RINEX`） | 长名或短名；支持多星座多频 |
| SP3/CLK/ATX/IONO/… | `flag_download=1` 时按 `remote_resource.ini` 拉 |
| `settings_*.ini` | 工程全部旋钮 |
| LAMBDA v3 目录 | 仅 AR |

| 输出 | 含义 |
| --- | --- |
| `out/` / `out_net/` | 坐标、ZTD/GRAD、残差、质量旗（由 `flag_out_*` 控制） |
| 图窗 | `SHOW` / GUI 绘图 |

## 4. 关键开关（`settings_PPP.ini` 摘）

| 项 | 作用 |
| --- | --- |
| `sss_date_start/stop` | 会话时间；样例 2021-01-01…04 |
| `obs_name` | 接收机文件名模式（含 `${YYYY}${DOY}` 等） |
| `preferred_iono` / `selected_iono_center` | GIM 优先级；默认 code |
| `flag_ppp_amb_fix` | PPP AR；默认 0 |
| `net_amb_fix_approach` | 网解固定策略 |
| `flag_solid_earth` / `flag_ocean_load` / `flag_atm_load`… | 地球物理改正 |
| `ppp_reweight_mode` | 抗差/再加权 |
| `flag_download` | 缺产品时自动下 |

## 5. 接到哪步

- 无 MATLAB / 要 C 基线或 FGO → [rtklib](./rtklib.md) / [graphgnsslib](./graphgnsslib.md)
- 发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；VieVS MATLAB GUI → [rapppid](./rapppid.md)
- CNES 整数 PPP 产品旁路 → [ppp-wizard](./ppp-wizard.md)
- 工作流 **D**：QC →（可选本文）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)
- JVM 嵌入 → PROJECTS.json `goGPS_Java`（无本手册）

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `goGPS` 找不到 / 路径错乱 | cwd 在仓库根 | `cd source` 再 `goGPS` |
| 2 | GUI Layout 报错 | 工具箱未注册 | 装 GUI Layout；或依赖仓内 `thirdParty/guiLayoutToolbox` |
| 3 | AR 菜单灰 / 固定失败 | `lambda_v3` 只有 README | 向 Curtin 申请 LAMBDA 3.0 并放入该目录 |
| 4 | Octave 一跑就挂 | 非支持运行时 | 装正版 MATLAB ≥2016a；或换 [rtklib](./rtklib.md) |
| 5 | 自动下载 SP3 失败 | 镜像/Earthdata/防火墙 | 配 `credentials`（见 `credentials.example.txt`）；或手动放 `data/` 树 |
| 6 | 期望动态车载解 | 软件只做永久站 | 换 [rtklib](./rtklib.md) / [graphgnsslib](./graphgnsslib.md) |
| 7 | `flag_ppp_amb_fix=1` 仍浮点 | LAMBDA 未就位或频点不足 | 先确认 `lambda_v3` 源码；双频+偏差产品 |
| 8 | 把 Wiki 截图坐标当本机结果 | 环境不同 | **禁止**转载未复现数字 |
| 9 | 与 [rtklib](./rtklib.md) 差大 | 引擎/权重/产品不同 | 同 OBS+SP3+CLK；比收敛后段 |
| 10 | 许可与 MATLAB 混谈 | GPL 管的是 goGPS 源码 | MATLAB 另需 MathWorks 许可；分发遵 GPL-3.0 |
| 11 | `settings` `1.0b9` ≠ `APP_VERSION` | 配置世代 vs 软件版本 | 以 `Core.APP_VERSION` 为准报版本 |
| 12 | 旧 beta 分支文档路径 | Wiki 仍写 `goGPS/` 目录名 | 以当前树 `source/` + `data/` 为准 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| MATLAB 下改算法 / 低成本站 PPP·NET | **本文 goGPS_MATLAB**（需 MATLAB 许可证） |
| 无 MATLAB 的 RTK/PPP CLI | [rtklib](./rtklib.md) |
| ROS+Ceres FGO | [graphgnsslib](./graphgnsslib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| VieVS MATLAB PPP GUI | [rapppid](./rapppid.md) |

## 8. 相关

[rtklib](./rtklib.md) · [graphgnsslib](./graphgnsslib.md) · [pride-pppar](./pride-pppar.md) · [rapppid](./rapppid.md) · [ppp-wizard](./ppp-wizard.md) · [ginan](./ginan.md) · [great-pvt](./great-pvt.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · [README](./README.md)

- Wiki：Installation / Settings / Command-language / How-to-create-a-new-project
- 姊妹：`goGPS_Java`（PROJECTS.json）
