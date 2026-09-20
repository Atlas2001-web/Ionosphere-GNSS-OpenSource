# SH-GIM · 球谐全球电离层图（维护者自有，短述）

目录条目：[`PROJECTS.json` → `SH-GIM`](../../PROJECTS.json) · 上游 <https://github.com/Atlas2001-web/SH-GIM>  
关系：本索引维护者 **owned**（目录 🚩：只收录链接，**不写长分析**）  
许可：公开代码 MIT · 语言：MATLAB · 列表：[01 电离层](../../lists/01-ionosphere.md)

## 作用与场景

公开仓库提供面向 GNSS 观测构建 **GIM** 的 MATLAB 流程骨架：数据解包、轨道插值、P4 等预处理与辅助函数，便于理解「从站观测走向球谐 VTEC 产品」的工程拆分。

**重要限制（以上游 README 为准）：** 法方程组装与求解等关键组件为**专有、未包含在公开仓**；因此**不能**仅凭本公开仓端到端跑完球谐反演。完整求解请使用目录中其他开源 GIM（如 `mosgim` / `mosgim2` / `m_gim` 等）或自有授权版本，并与 IGS IONEX 对照。

## 安装

- 需 MATLAB；并行步骤可能依赖 Parallel Computing Toolbox。  
- 自行准备合规的 GNSS 观测、SP3 等；外部工具（如 GFZRNX、M_Map）按各自许可证单独安装。  
- 将仓库根目录设为 MATLAB 当前路径；按 `main_unpackdata.m` 注释修改本地数据路径（示例路径不可直接用）。

## 最小示例

```matlab
% 1. cd 到 SH-GIM 仓库根目录
% 2. 编辑 main_unpackdata.m 中的 packFilePath / stations_txt / unpack_outdir 等
main_unpackdata
```

公开仓默认串联主要预处理步骤；具体能跑到哪一步取决于你是否具备专有求解模块与输入数据。细节只信上游 README。

## 输入输出

| 方向 | 说明 |
|---|---|
| 输入 | 自备 GNSS 观测与轨道等（仓内**不含**原始 RINEX/SP3/结果图） |
| 公开输出 | 预处理相关中间结果（若脚本成功）；**不含**保证可用的完整球谐解 |
| 产品对照 | 科学分析请优先下载 IGS/分析中心 IONEX（见 [ionex-gim](./ionex-gim.md)、[data-access.md](../data-access.md)） |

## 常见坑

1. **期望「clone 就能出全球 TEC 图」**：公开说明已写明求解器未包含。  
2. **把本短文当完整教程**：目录政策是自有仓不展开。  
3. **路径未改**：脚本内示例目录必须换成你的数据位置。  
4. **与 PyTECGg 混淆**：[PyTECGg](./pytecgg.md) 是 viventriglia 的 Python TEC 校准库，不是本仓库。

## 接到哪一步分析

- 概念与工作流：[03 GIM/IONEX](../tutorials/03-gim-ionex.md)、[10 建 GIM 工作流](../tutorials/10-build-gim-workflow.md)。  
- 开源对照：列表中的 `mosgim`、`mosgim2`、`m_gim`、`M_GIM` 等。  
- 单站 TEC 输入侧：[georinex](./georinex.md)、[PyTECGg](./pytecgg.md)、[IonoMoni](./ionomoni.md)。
