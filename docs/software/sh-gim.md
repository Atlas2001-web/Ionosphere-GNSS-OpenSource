# SH-GIM · 维护者球谐 GIM 仓边界手册

目录：[`PROJECTS.json` → `SH-GIM`](../../PROJECTS.json) · 上游 <https://github.com/Atlas2001-web/SH-GIM> · 维护者 **owned** · 公开代码 MIT · MATLAB

> **边界手册，不是端到端求解教程。** 公开仓提供流程骨架；法方程组装与求解等关键组件为**专有、未包含在公开仓**。参数与结构以上游 README 为准。

---

## 1. 用途与边界

### 1.1 一句话

公开仓帮助理解「站观测 → 球谐 VTEC 产品」的工程拆分；**不能**仅凭公开仓跑完全球球谐反演。

### 1.2 何时打开本页

- 想了解维护者工程拆分与公开/专有边界
- 对照教程 [10](../tutorials/10-build-gim-workflow.md) 的概念步骤
- **不要**期望 `git clone` 后立刻出全球 TEC 图

### 1.3 应该用（公开部分）

- 阅读 `main_unpackdata.m`、`Step1/2/3.m`、`GET_NE.m`、`functions/` 等结构
- 练习解包、轨道插值、P4 等预处理思路（在你自备数据且环境允许时）

### 1.4 不应该用

- 把本页当完整球谐求解器文档
- 在 issue 索要专有求解器二进制
- 把中间 `.mat` 当最终 GIM 产品发表
- 与 [pytecgg](./pytecgg.md)（作者 **viventriglia**）混淆作者关系

### 1.5 完整求解请用

- 目录其它开源 GIM：`mosgim` / `mosgim2` / `m_gim` 等（见 `PROJECTS.json` / lists）
- 或自有授权版本
- 科学对照：IGS/分析中心 IONEX → [ionex-gim](./ionex-gim.md)

---

## 2. 安装（仅公开部分）

- 需 MATLAB；并行步骤可能要 Parallel Computing Toolbox
- 自备合规 GNSS 观测、SP3 等（仓内**不含**原始数据与结果图）
- 外部工具（GFZRNX、M_Map 等）各自安装、各自许可证
- 将仓库根目录设为 MATLAB 当前路径

```matlab
% cd 到 SH-GIM 仓库根目录
pwd
```

---

## 3. 公开可达步骤（能跑到哪取决于专有模块）

```matlab
% 1. 编辑 main_unpackdata.m 中 packFilePath / stations_txt / unpack_outdir 等
%    示例路径不可直接用
main_unpackdata
```

可见结构（据 README）：`main_unpackdata.m`、`Step1.m`/`Step2.m`/`Step3.m`、`GET_NE.m`、`functions/`、`sub_functions/`、`tests/`。

**期望（公开环境）：** 可能生成预处理中间结果；**不保证**完整球谐解与最终 GIM。

---

## 4. 输入 / 输出

| 方向 | 说明 |
| --- | --- |
| 输入 | 自备观测与轨道等 |
| 公开输出 | 预处理中间量（若成功） |
| 不含 | 保证可用的完整球谐解 |
| 科学对照 | IGS IONEX（[ionex-gim](./ionex-gim.md)） |

---

## 5. 概念参数（非「可复现求解器开关表」）

| 概念 | 说明 |
| --- | --- |
| GIM | 全球电离层图，常以 IONEX 交换 |
| 球谐 | 用球谐函数表示 VTEC 空间场 |
| P4 等 | 几何无关/电离层组合预处理常见符号 |
| 法方程 | 最小二乘组装；**公开仓不含完整求解器** |
| 薄壳/IPP | 映射与穿刺点几何 |

本文**故意不**把未开源求解器写成可复现参数表。

---

## 6. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| 概念 GIM | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) |
| 读产品 | [ionex-gim](./ionex-gim.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 单站 TEC | [georinex](./georinex.md) · [pytecgg](./pytecgg.md) |
| 开源端到端 | lists 中 mosgim / m_gim 等 |
| 索引路径 E | [README](./README.md) |

路径 E：本页讲边界，不是端到端工站。

---

## 7. 可操作坑（≥12）

1. clone 不出全球 TEC 图 — **预期内**。  
2. 把本页当完整求解教程 — 停。  
3. 未改脚本示例路径。  
4. 与 PyTECGg 作者混淆 — PyTECGg=viventriglia。  
5. 中间 `.mat` 当最终产品发表。  
6. issue 索要专有求解器 — 请尊重边界。  
7. 无 Parallel Toolbox — 关并行或装工具箱。  
8. 不与 IGS IONEX 对照就谈精度。  
9. 把公开预处理输出当成「官方 GIM」。  
10. 外部工具许可未核（GFZRNX/M_Map）。  
11. 数据政策未核就用限制站网。  
12. 在论文写「使用 SH-GIM 开源求解」——若只用了公开仓，表述不实。  
13. 期望 Python 一键 pip — 这是 MATLAB 仓。  
14. 混用旧 Step 脚本与新目录布局。  
15. 把维护者 owned 当成「仓库含全部机密代码」。  
16. 跳过 [10](../tutorials/10-build-gim-workflow.md) 概念直接硬跑。  

---

## 8. 同类选型

| 需求 | 选 |
| --- | --- |
| 理解边界 / 预处理骨架 | **SH-GIM 公开仓** |
| 开源端到端球谐/GIM | mosgim / m_gim 等 |
| 读现成产品 | ionex-gim |
| 单站校准 TEC | pytecgg（viventriglia） |

---

## 9. 检查清单

- [ ] 已读上游 README 的专有组件声明  
- [ ] 不期望公开仓出完整球谐解  
- [ ] 作者关系：SH-GIM≠PyTECGg  
- [ ] 科学对照走 IONEX  
- [ ] 论文表述与实际使用的组件一致  

---

## 10. 教学 45 分钟建议

1. 画「观测 → 预处理 → 法方程 → IONEX」框图（15 min）  
2. 打开公开仓目录对照框图（15 min）  
3. 用 [ionex-gim](./ionex-gim.md) 读一张 IGS 图（15 min）  
强调：缺的那一块是求解器。

---

## 11. 与路径 A–E

- A/B/D：不依赖 SH-GIM  
- E：本页 + ionex-gim + 开源 GIM 列表  

---

## 12. 复现包（公开部分）

若只跑预处理：记录 MATLAB 版本、脚本名、输入 checksum、是否包含专有模块（应明确写「否」）。

---

## 13. 禁止清单

- 禁止声称公开仓可完整反演全球 GIM  
- 禁止索要未开源二进制并写进教程「标准步骤」  
- 禁止作者张冠李戴  

---

## 14. 相关工具

[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [README](./README.md) · 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 15. 版本与上游

- `git pull` 后重读 README 边界声明（可能更新）  
- MIT 仅覆盖公开代码；专有组件条款另议  
- 本手册冲突时以上游 README 为准


---

## 16. 公开目录导读（对照用）

打开仓库后建议按此顺序阅读（文件名以当前 README 为准）：

1. 根 README：专有组件声明（先读完再动手）  
2. `main_unpackdata.m`：解包入口与路径变量  
3. `Step1.m` / `Step2.m` / `Step3.m`：预处理阶段切分  
4. `GET_NE.m`：与电子密度/相关量有关的辅助（若存在）  
5. `functions/`、`sub_functions/`：可复用几何与组合函数  
6. `tests/`：有则先跑，建立「公开部分可测」预期  

阅读目标：能在白板上画出哪些框在公开仓、哪些框标注「专有」。

---

## 17. 与教程 10 的逐步对照

| 教程 10 概念步骤 | 公开仓可能对应 | 专有？ |
| --- | --- | --- |
| 数据准备/解包 | `main_unpackdata` | 否（需自备数据） |
| 轨道/几何 | Step/functions 中部分 | 视版本 |
| 组合/预处理 | P4 等 | 部分公开 |
| 法方程组装 | — | **是（未开源）** |
| 求解/约束 | — | **是** |
| 写 IONEX | — | 通常专有或自写 |
| 对照 IGS | 用 [ionex-gim](./ionex-gim.md) | 不依赖本仓 |

---

## 18. 最小「公开环境」验收

```matlab
% 仅验证你能打开脚本并理解路径变量，不验证全球解
edit main_unpackdata.m
% 确认：没有把示例路径当生产路径
% 确认：README 专有声明仍在
```

成功标准：你能用自己的话复述「缺了求解器」。失败标准：以为跑完 Step3 就有全球 GIM。

---

## 19. 论文/报告表述模板（合规）

**可用：**「参考 SH-GIM 公开仓库的预处理流程骨架；球谐法方程求解使用××（开源 GIM / 授权模块）；产品与 IGS IONEX 对照。」

**禁用：**「使用开源 SH-GIM 完成全球球谐 GIM 反演」（若未使用完整求解器）。

---

## 20. 选型决策树

```text
只要读现成图？ → ionex-gim
要单站 TEC？ → pytecgg
要开源端到端建图？ → mosgim / m_gim 等
只想理解维护者拆分？ → SH-GIM 公开仓（本页）
想要本仓未开源求解器？ → 停止；尊重边界
```

---

## 21. 常见问答（短答）

**Q: 为什么 clone 没有结果图？**  
A: 仓内不含结果；且求解器未开源。

**Q: 能 pip 安装吗？**  
A: 否，MATLAB。

**Q: 和 PyTECGg 谁好？**  
A: 不同问题。PyTECGg=单站校准 TEC（viventriglia）；SH-GIM=GIM 工程边界。

**Q: 课程作业要求「自建 GIM」怎么办？**  
A: 用开源 GIM 列表或简化二维插值教学案例；不要伪造 SH-GIM 完整解。

---

## 22. 检查清单（扩）

- [ ] README 专有声明已截图/摘录进笔记  
- [ ] 白板框图含「专有」红框  
- [ ] 至少用 ionex-gim 读过一张 IGS 图  
- [ ] 作者关系表已抄  
- [ ] 论文表述模板已选「可用」句  

---

## 23. 相关工具（复述）

[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [README](./README.md) · [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md)


---

## 24. 边界声明（再强调一次）

公开仓 = 预处理与工程骨架。  
专有仓外组件 = 法方程组装/求解等。  
科学产品对照 = IGS IONEX。  
作者 = 本仓维护者；PyTECGg = viventriglia。

若只能记住四句，记这四句。

---

## 25. 操作备忘（公开部分）

```text
[ ] git clone SH-GIM
[ ] 读 README 专有声明
[ ] MATLAB 路径设到仓库根
[ ] 编辑路径变量（勿用示例原样）
[ ] 能跑的预处理步骤记入笔记
[ ] 明确标注：未包含完整求解
[ ] 对照 ionex-gim 读 IGS 产品
```

