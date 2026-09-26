# SH-GIM · 维护者球谐 GIM 仓边界手册

目录：[`PROJECTS.json` → `SH-GIM`](../../PROJECTS.json) · 上游 <https://github.com/Atlas2001-web/SH-GIM> · 维护者 **owned** · 公开代码 MIT · MATLAB

> **边界手册，不是端到端求解教程。** 公开仓提供流程骨架；法方程组装与求解等关键组件为**专有、未包含在公开仓**。以上游 README 的 public-release note 为准。

> **质检复跑通过**（2026-09-26 04:27–04:30 EDT）：上游 `main` `c92e3d0`（2026-08-15，"Initial public source release (solver withheld)"），MIT（Copyright 2024-2026 Atlas2001-web），GitHub 语言 MATLAB。README 首段的 public-release note、§3 列的文件（`main_unpackdata.m`、`Step1–3.m`、`GET_NE.m`、`functions/`、`sub_functions/`、`tests/`）、`main_unpackdata.m` 第 50–52 行的 `packFilePath`/`stations_txt`/`unpack_outdir` 示例路径（`D:\`/`E:\`，坑 3）、`parfor`（坑 7）、README 提到的 GFZRNX / M_Map 都核对属实。补充：求解器位置是占位函数 `Get_SHBackground.m`，一调用就抛 `Get_SHBackground:ProprietaryComponent`；本机无 MATLAB，用 GNU Octave 9.4.0 跑 `tests/` 6 个检查脚本，只有 `check_build_time_continuous_constraints`、`check_get_ipp_kent_geo2mag_consistency` 通过，其余 4 个因 MATLAB 专有函数（`java`、`matlab_executable_statements` 等）在 Octave 下失败。无修正；`main_unpackdata` 流程未跑（需 MATLAB 和自备数据，环境受限）。

## 1. 用途与边界

**公开仓能帮你：** 理解「站观测 → 球谐 VTEC 产品」的工程拆分；阅读预处理脚本结构；在自备数据时练习解包/轨道插值/组合等**公开**步骤。

**公开仓不能：** `git clone` 后跑出全球球谐最终解；在 issue 索要专有求解器；把中间 `.mat` 当正式 GIM 发表。

**不要与 [pytecgg](./pytecgg.md) 混淆作者：** PyTECGg = **viventriglia**；SH-GIM = 本仓维护者。

完整求解请用：lists / `PROJECTS.json` 中其它开源 GIM（如 mosgim、m_gim 等），或自有授权版本；科学对照用 IGS IONEX → [ionex-gim](./ionex-gim.md)。

一句话：**公开 = 预处理骨架；专有 = 法方程/求解；产品对照 = IONEX。**

## 2. 环境（仅公开部分）

- MATLAB；并行步骤可能需 Parallel Computing Toolbox  
- 自备合规 GNSS 观测、SP3 等（仓内**不含**原始数据与结果图）  
- 外部工具（GFZRNX、M_Map 等）各自安装、各自许可证  
- 将仓库根目录设为 MATLAB 当前路径

```matlab
% cd 到 SH-GIM 仓库根
pwd
```

## 3. 公开可达步骤（能跑到哪取决于专有模块）

上游可见结构（文件名以当前 README 为准）：`main_unpackdata.m`、`Step1.m` / `Step2.m` / `Step3.m`、`GET_NE.m`、`functions/`、`sub_functions/`、`tests/`。

```matlab
% 编辑 main_unpackdata.m 中 packFilePath / stations_txt / unpack_outdir 等
% 示例路径不可直接用
main_unpackdata
```

**期望（公开环境）：** 可能生成预处理中间结果；**不保证**完整球谐解与最终 GIM。成功标准：能用自己的话复述「缺了求解器」。失败标准：以为跑完 Step3 就有全球 GIM。

### 与教程 [10](../tutorials/10-build-gim-workflow.md) 对照

| 教程 10 概念 | 公开仓可能对应 | 专有？ |
| --- | --- | --- |
| 数据准备/解包 | `main_unpackdata` | 否（需自备数据） |
| 轨道/几何 | Step/functions 中部分 | 视版本 |
| 组合/预处理 | P4 等 | 部分公开 |
| 法方程组装 | — | **是（未开源）** |
| 求解/约束 | — | **是** |
| 写 IONEX | — | 通常专有或自写 |
| 对照 IGS | [ionex-gim](./ionex-gim.md) | 不依赖本仓 |

## 4. 输入 / 输出

| 方向 | 说明 |
| --- | --- |
| 输入 | 自备观测与轨道等 |
| 公开输出 | 预处理中间量（若成功） |
| 不含 | 保证可用的完整球谐解 |
| 科学对照 | IGS IONEX（[ionex-gim](./ionex-gim.md)） |

概念词（非「可复现求解器开关表」）：GIM、球谐、P4、法方程、薄壳/IPP。本文**故意不**把未开源求解器写成可复现参数表。

## 5. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| 概念 GIM | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) |
| 读产品 | [ionex-gim](./ionex-gim.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 单站 TEC | [georinex](./georinex.md) · [pytecgg](./pytecgg.md) |
| 开源端到端 | lists 中 mosgim（[mosgim2 手册](./mosgim2.md)）/ m_gim 等 |
| 索引路径 E | [README](./README.md) |

路径 E：本页讲边界，不是端到端工站。A/B/D 不依赖 SH-GIM。

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | clone 不出全球 TEC 图 | **预期内** | 改用开源 GIM 或读 IONEX |
| 2 | 把本页当完整求解教程 | 边界误解 | 停；读 README 专有声明 |
| 3 | 未改脚本示例路径 | 路径仍是作者机器 | 改自己的绝对路径 |
| 4 | 与 PyTECGg 作者混淆 | 张冠李戴 | PyTECGg=viventriglia |
| 5 | 中间 `.mat` 当最终产品 | 产品形态错 | 对照 IGS IONEX |
| 6 | issue 索要专有求解器 | 不尊重边界 | 停止索要 |
| 7 | 无 Parallel Toolbox | 并行步失败 | 关并行或装工具箱 |
| 8 | 不与 IGS 对照谈精度 | 无基准 | [ionex-gim](./ionex-gim.md) |
| 9 | 公开预处理输出称「官方 GIM」 | 表述不实 | 改表述 |
| 10 | 外部工具许可未核 | GFZRNX/M_Map | 各遵各许可 |
| 11 | 数据政策未核 | 限制站网 | 先读数据条款 |
| 12 | 论文写「开源 SH-GIM 完整反演」 | 若只用公开仓则不实 | 用合规表述模板 |
| 13 | 期望 pip 安装 | 这是 MATLAB 仓 | 用 MATLAB |
| 14 | 混用旧 Step 与新布局 | 版本漂移 | `git pull` 后重读 README |
| 15 | 以为 owned=仓内含全部机密 | owned≠全开源 | 再读 public-release note |
| 16 | 跳过教程 10 硬跑 | 缺概念 | 先读 [10](../tutorials/10-build-gim-workflow.md) |

## 7. 论文表述（合规）

**可用：**「参考 SH-GIM 公开仓库的预处理流程骨架；球谐法方程求解使用××（开源 GIM / 授权模块）；产品与 IGS IONEX 对照。」

**禁用：**「使用开源 SH-GIM 完成全球球谐 GIM 反演」（若未使用完整求解器）。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 理解边界 / 预处理骨架 | **SH-GIM 公开仓** |
| 开源端到端建图 | mosgim / m_gim 等 |
| 读现成产品 | ionex-gim |
| 单站校准 TEC | pytecgg（viventriglia） |

```text
只要读现成图？ → ionex-gim
要单站 TEC？ → pytecgg
要开源端到端建图？ → mosgim / m_gim 等
只想理解维护者拆分？ → SH-GIM 公开仓（本页）
想要未开源求解器？ → 停止；尊重边界
```

## 9. 相关

[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [README](./README.md) · [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) · [data-access](../data-access.md)
