# 17 · 总路线图：从入门到精通

把 01–16 收成一张**可执行进度表**。按周推进即可；不必一天读完。精通不是读完所有 `lists/`，而是能判断问题类型、10 分钟内找到候选上游、并说清主要误差源。

---

## 阶段目标一览

| 阶段 | 你能做到 | 对应课文 | 目录动作 |
|---|---|---|---|
| **入门** | 分清 STEC/VTEC/TECU；能读懂 IONEX 图；知道模型≠实测 | [01](./01-ionosphere-tec-basics.md)–[04](./04-iri-nequick.md)、[08](./08-how-to-use-this-catalog.md) | 浏览 `lists/01`、`lists/10`；跑通路线 A |
| **上手** | 独立出一张 GIM 图；单站 STEC 曲线；会查 data-access | [03](./03-gim-ionex.md)、[09](./09-dcb-biases-deep.md)、[16](./16-practice-one-day-tec.md) | 克隆 `ionex` / `gnss-tec` 等 |
| **进阶** | 讲清 DCB；搭区域 VTEC 流程；懂闪烁指数与定位差异 | [05](./05-scintillation-roti.md)–[07](./07-ionosonde-occultation.md)、[10](./10-build-gim-workflow.md)、[13](./13-scintillation-modeling.md) | 对照 `DLR-IMPC`、`igs-roti`、测高仪/掩星 |
| **精通·实战** | 复盘磁暴；读论文能落到开源；理解层析/同化边界 | [11](./11-tomography-basics.md)–[12](./12-data-assimilation-intro.md)、[14](./14-space-weather-case.md)–[15](./15-from-paper-to-code.md) | 多源交叉验证；写差异表 |

完整课表与学习成果见 [README.md](./README.md)。

---

## 建议 6 周节奏（可压缩可拉长）

1. **第 1 周**：01–04 + [16](./16-practice-one-day-tec.md) 路线 A 出图  
2. **第 2 周**：02、09 + 单站 STEC（路线 B）；死磕高度角与 DCB 叙事  
3. **第 3 周**：05–06、13；看一次闪烁/ROTI 图；用一句话向定位同学解释  
4. **第 4 周**：07、10；写半页「我的 GIM 流程」并列出验证清单  
5. **第 5 周**：14 事件复盘 + 可选模式对照（`TIE-GCM` / `pytiegcm`）  
6. **第 6 周**：11–12 选读 + 15 论文对照；回看本路线图打勾  

若只有两周：做完「入门 + 上手 + 一次路线 A/B」，进阶以后当工具书查。

---

## 能力检查表（打勾再用「精通」自称）

### 概念

- [ ] 能区分 STEC / VTEC / TECU，并指出 GIM 格网通常是哪种  
- [ ] 能说明几何无关组合消掉了什么、没消掉什么  
- [ ] 能解释薄壳映射在低高度角为何容易出事  

### 偏差与产品

- [ ] 能说出卫星 DCB 与接收机 DCB 各何时致命  
- [ ] 能解释为何两家 IGS 分析中心 GIM 可差数 TECU  
- [ ] 知道去 `CDDIS-IONEX`、`IGS-Products`、`DLR-IMPC` 等找什么  

### 实操

- [ ] 独立完成 [16](./16-practice-one-day-tec.md) 路线 A  
- [ ] 独立完成路线 B，并写出与 GIM 差异的原因假设  
- [ ] 在 `PROJECTS.json` 里按任务名搜到至少三个候选上游  

### 进阶判断

- [ ] 能判断问题该用：改正模型 / 实测 GIM / 物理模式 / 闪烁监测 中的哪一类  
- [ ] 能指出层析与同化各自最容易被误解的一点（[11](./11-tomography-basics.md)、[12](./12-data-assimilation-intro.md)）  
- [ ] 读一篇论文能填完 [15](./15-from-paper-to-code.md) 的差异表  

---

## 精通不是什么

- 不是背完 197 个电离层条目；  
- 不是把 `SH-GIM` 当唯一标准答案；  
- 不是会训一个 TEC 网络就宣称「取代物理」；  
- 不是无视许可证与数据政策。  

精通是：

- **选题时**方向不歪；  
- **找工具时**十分钟内有候选；  
- **出图后**能指出 DCB、映射、数据空洞、分析中心差异等误差源；  
- **读论文时**能落到公开数据与开源替代。  

---

## 按问题跳转（急救）

| 我的问题 | 先读 |
|---|---|
| TEC 符号都看不懂 | [01-ionosphere-tec-basics.md](./01-ionosphere-tec-basics.md) |
| 双频怎么估 | [02-gnss-dualfreq-tec.md](./02-gnss-dualfreq-tec.md) |
| 数字整段平移 | [09-dcb-biases-deep.md](./09-dcb-biases-deep.md) |
| 想建图 | [10-build-gim-workflow.md](./10-build-gim-workflow.md) |
| 今天就要出图 | [16-practice-one-day-tec.md](./16-practice-one-day-tec.md) |
| 闪烁 / 失锁 | [05](./05-scintillation-roti.md)、[13](./13-scintillation-modeling.md)、[06](./06-iono-positioning.md) |
| 磁暴复盘 | [14-space-weather-case.md](./14-space-weather-case.md) |
| 论文难落地 | [15-from-paper-to-code.md](./15-from-paper-to-code.md) |
| 不会用本仓库 | [08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md) |

---

## 下一步

- 回 [教学目录 README](./README.md) 按入门 / 进阶 / 精通·实战跳转  
- 数据与分类：[`docs/data-access.md`](../data-access.md)、[`docs/categories.md`](../categories.md)  
- 软件表：[`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) · 总表 [`PROJECTS.json`](../../PROJECTS.json)
