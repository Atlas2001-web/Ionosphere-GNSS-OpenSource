# SH-GIM

目录：[`PROJECTS.json` → `SH-GIM`](../../PROJECTS.json) · 上游 <https://github.com/Atlas2001-web/SH-GIM> · 维护者 **owned** · 公开代码 MIT · MATLAB

## 用途

- 公开仓提供面向 GNSS 观测构建 GIM 的 MATLAB **流程骨架**：解包、轨道插值、P4 等预处理与辅助函数。
- 用于理解「站观测 → 球谐 VTEC 产品」的工程拆分，并对照教程 [10](../tutorials/10-build-gim-workflow.md)。

### 重要限制（以上游 README 为准）

> 法方程组装与求解等关键组件为**专有、未包含在公开仓**；**不能**仅凭公开仓端到端跑完球谐反演。

完整求解请用目录其他开源 GIM（`mosgim` / `mosgim2` / `m_gim` 等）或自有授权版本，并与 IGS IONEX 对照。

### 何时打开本页

- 想了解维护者工程拆分与公开/专有边界。
- **不要**期望 clone 后立刻出全球 TEC 图。

## 安装（仅公开部分）

- 需 MATLAB；并行步骤可能要 Parallel Computing Toolbox。
- 自备合规 GNSS 观测、SP3 等（仓内**不含**原始数据与结果图）。
- 外部工具（GFZRNX、M_Map 等）各自安装、各自许可证。
- 将仓库根目录设为 MATLAB 当前路径。

## 快速上手（仅公开可达）

```matlab
% 1. cd 到 SH-GIM 仓库根目录
% 2. 编辑 main_unpackdata.m 中 packFilePath / stations_txt / unpack_outdir 等
%    示例路径不可直接用
main_unpackdata
```

公开仓默认串联主要预处理步骤；**能跑到哪一步取决于你是否具备专有求解模块与输入数据**。细节只信上游 README。

可见结构（据 README）：`main_unpackdata.m`、`Step1.m`/`Step2.m`/`Step3.m`、`GET_NE.m`、`functions/`、`sub_functions/`、`tests/`。

**预期（公开环境）：** 可能生成预处理中间结果；**不保证**完整球谐解与最终 GIM 产品。

## 输入 / 输出

| 方向 | 说明 |
|---|---|
| 输入 | 自备观测与轨道等 |
| 公开输出 | 预处理中间量（若成功） |
| 不含 | 保证可用的完整球谐解 |
| 科学对照 | 优先 IGS/分析中心 IONEX（[ionex-gim](./ionex-gim.md)） |

## 常用参数

公开脚本内路径与开关以仓库文件为准；本文不把未开源求解器写成可复现参数表。

| 概念 | 说明 |
|---|---|
| GIM | 全球电离层图，常以 IONEX 交换 |
| 球谐 | 用球谐函数表示 VTEC 空间场 |
| P4 等 | 几何无关/电离层组合预处理常见符号 |
| 法方程 | 最小二乘组装；**公开仓不含完整求解器** |
| 薄壳/IPP | 映射与穿刺点几何 |

## 接到工作流哪一步

- 概念：[03](../tutorials/03-gim-ionex.md)·[10](../tutorials/10-build-gim-workflow.md)
- 开源端到端：列表 `mosgim`/`mosgim2`/`m_gim`
- 单站 TEC：[georinex](./georinex.md)·[pytecgg](./pytecgg.md)·[ionomoni](./ionomoni.md)
- 产品读入：[ionex-gim](./ionex-gim.md)

路径 E：本页讲边界，不是端到端工站。

## 常见问题

| 现象 | 处理 |
|---|---|
| clone 不出全球 TEC 图 | 预期内：求解器未开源 |
| 把本页当完整求解教程 | 停；改用开源 GIM 或授权版 |
| 未改脚本示例路径 | 编辑为真实路径 |
| 与 PyTECGg 作者混淆 | PyTECGg=viventriglia |
| 把中间 `.mat` 当最终产品发表 | 不要 |
| issue 索要专有求解器二进制 | 请尊重上游边界 |
| 无 Parallel Toolbox | 关掉并行段或装工具箱 |
| 不与 IGS IONEX 对照 | 先对照再谈精度 |

## 相关工具

[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md)

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
