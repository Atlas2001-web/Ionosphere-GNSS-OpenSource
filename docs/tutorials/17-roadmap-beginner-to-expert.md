# 17 · 总路线图：从入门到精通

> 把 01–16、18 收成一张**可执行进度表**。按周推进即可；不必一天读完。  
> 精通不是读完所有 `lists/`，而是能：判断问题类型、10 分钟内找到候选上游、说清主要误差源。  
> 本课假设你可能零基础：下面先翻译「入门/上手/进阶/精通」到底长什么样，再给你每周交付物与自测量表。

---

## 0. 先别被「精通」吓到（人话版）

把本系列想成学做菜：

| 阶段 | 厨艺类比 | 电离层/GNSS 里你能做什么 |
|---|---|---|
| **入门** | 认识盐糖油、会看说明书 | 分清 STEC/VTEC/TECU；能打开一张 IONEX 图；知道 IRI 模型≠当天实测 |
| **上手** | 能按菜谱炒一盘蛋炒饭 | 独立出一张 GIM 图；跑通单站 STEC；会查 data-access 注册 |
| **进阶** | 知道火候与替代食材 | 讲清 DCB；能搭区域 VTEC 思路；懂闪烁指数与定位差异 |
| **精通·实战** | 能复盘一次失败宴席并写出改进单 | 复盘磁暴；论文能落到开源；知道层析/同化的边界与坑 |

**精通不是什么**（请先读，避免自我PUA）：

- 不是背完几百个电离层条目；  
- 不是把 `SH-GIM` 当唯一标准答案；  
- 不是会训一个 TEC 网络就宣称「取代物理」；  
- 不是无视许可证与数据政策；  
- 不是一天读完 01–18。

**精通是**：

- **选题时**方向不歪（该用改正模型 / 实测 GIM / 闪烁监测 / 物理模式中的哪类）；  
- **找工具时**十分钟内在 `PROJECTS.json` / `lists/` 有候选；  
- **出图后**能指出 DCB、映射、数据空洞、分析中心差异等误差源；  
- **读论文时**能落到公开数据与开源替代（见 [15](./15-from-paper-to-code.md)）。

---

## 1. 零基础术语速查（路线图用得到的）

读进度表前，把这些词钉住。详细课里还有展开；这里只够「看懂本课表格」。

| 词 | 超短解释 | 哪课深讲 |
|---|---|---|
| TEC | 信号路径上电子「雾」的柱含量 | [01](./01-ionosphere-tec-basics.md) |
| STEC | 斜路径上的 TEC（星到站） | [01](./01-ionosphere-tec-basics.md)、[02](./02-gnss-dualfreq-tec.md) |
| VTEC | 折成竖直方向的 TEC；GIM 常画它 | [01](./01-ionosphere-tec-basics.md)、[03](./03-gim-ionex.md) |
| TECU | TEC 的单位 | [01](./01-ionosphere-tec-basics.md) |
| GIM / IONEX | 全球电离层地图 / 其常用文件格式 | [03](./03-gim-ionex.md) |
| DCB | 硬件延迟差，常让 TEC「整段平移」 | [09](./09-dcb-biases-deep.md) |
| ROTI / S4 | 「抖不抖」与幅度闪烁指数 | [05](./05-scintillation-roti.md) |
| IRI / NeQuick | 经验气候模型，不是当天实况摄像头 | [04](./04-iri-nequick.md) |
| 层析 / 同化 | 三维反演；把观测喂进模式的流程 | [11](./11-tomography-basics.md)、[12](./12-data-assimilation-intro.md) |

**厨房类比回顾**：STEC 是斜着看雾的厚度；VTEC 是竖直厚度；GIM 是气象局发的雾厚填色图；DCB 是尺子两端粘的橡皮泥；ROTI 是雾是否在翻滚。

---

## 2. 阶段目标一览（对照表）

| 阶段 | 你能做到 | 对应课文 | 目录动作（真实条目名） |
|---|---|---|---|
| **入门** | 分清 STEC/VTEC/TECU；读懂 IONEX 图；模型≠实测 | [01](./01-ionosphere-tec-basics.md)–[04](./04-iri-nequick.md)、[08](./08-how-to-use-this-catalog.md) | 浏览 `lists/01`、`lists/10`；跑通 [16](./16-practice-one-day-tec.md) 路线 A（`CDDIS-IONEX` + `ionex`/`ionex_reader`/`ionex-rs`） |
| **上手** | 独立出 GIM 图；单站 STEC；会查注册 | [03](./03-gim-ionex.md)、[09](./09-dcb-biases-deep.md)、[16](./16-practice-one-day-tec.md) | 克隆 `ionex` / `gnss-tec` / `pygnss-tec` 等；数据走 `IGS-Data-Access`、`NASA-Earthdata-Login` |
| **进阶** | 讲清 DCB；区域 VTEC 流程；闪烁与定位 | [05](./05-scintillation-roti.md)–[07](./07-ionosonde-occultation.md)、[10](./10-build-gim-workflow.md)、[13](./13-scintillation-modeling.md) | 对照 `DLR-IMPC`、`igs-roti`、`Okoh-MATLAB-ROT-ROTI`；测高/掩星见 `GIRO-DIDBase`、`COSMIC-CDAAC` |
| **精通·实战** | 复盘磁暴；论文落地；层析/同化边界 | [11](./11-tomography-basics.md)–[12](./12-data-assimilation-intro.md)、[14](./14-space-weather-case.md)–[15](./15-from-paper-to-code.md)、[18](./18-lab-compare-gims.md) | 多源交叉；写差异表；量化分析中心差 |

完整课表见 [README.md](./README.md)。

---

## 3. 建议 8 周节奏（可压缩可拉长）

下面每一周都有：**阅读、动手、交付物、自测门槛**。打勾再进入下一周。

### 第 1 周 · 认量纲 + 第一张图

| 项 | 内容 |
|---|---|
| 阅读 | [01](./01-ionosphere-tec-basics.md)、[03](./03-gim-ionex.md)、[08](./08-how-to-use-this-catalog.md)；扫 `docs/data-access.md` |
| 动手 | [16](./16-practice-one-day-tec.md) **路线 A**：`CDDIS-IONEX` 下一天，用 `ionex`/`ionex_reader`/`ionex-rs` 出图 |
| **交付物** | ① 一张带 TECU 色标与日期的 VTEC 图；② 十行笔记（工具 `name`、文件名、一个疑问） |
| **自测门槛** | 口头解释 STEC vs VTEC；指出图上单位；说出数据来自哪个分析中心/产品代次 |

### 第 2 周 · 双频直觉 + DCB 叙事

| 项 | 内容 |
|---|---|
| 阅读 | [02](./02-gnss-dualfreq-tec.md)、[09](./09-dcb-biases-deep.md)、[04](./04-iri-nequick.md) |
| 动手 | 路线 A 加分：同日两家 GIM 瞄一眼差多少（为第 18 课热身）；或跑 `iri2020`/`PyIRI`/`NeQuick2-ICTP` 与 GIM 同点对比「模型 vs 实测」 |
| **交付物** | 半页：「为什么 TEC 会整段平移」+ 一张模型/GIM 对照草图（或文字表） |
| **自测门槛** | 能说出几何无关组合消掉了什么、没消掉什么；能区分「绝对 TECU」与「相对变化」何时较真 DCB |

### 第 3 周 · 单站 STEC（路线 B）

| 项 | 内容 |
|---|---|
| 阅读 | 重读 [02](./02-gnss-dualfreq-tec.md)、[09](./09-dcb-biases-deep.md)；[16](./16-practice-one-day-tec.md) 路线 B |
| 动手 | `IGS-Data-Access`/`CDDIS-GNSS-Archive` 下一站日；`georinex`/`GFZRNX` + `TEQC`/`Anubis`；`gnss-tec`/`pygnss-tec`/`tec-suite`/`Seemala-GPS-TEC` 等估 STEC |
| **交付物** | STEC 曲线图 + 与 GIM 插值差异的**两条原因假设** |
| **自测门槛** | 写明高度角截止；能解释「低仰角更散」；不把常数偏差直接叫「算法失败」 |

### 第 4 周 · 闪烁、定位、互补观测

| 项 | 内容 |
|---|---|
| 阅读 | [05](./05-scintillation-roti.md)、[06](./06-iono-positioning.md)、[07](./07-ionosonde-occultation.md)、[13](./13-scintillation-modeling.md) |
| 动手 | 看一张 ROTI 图（`igs-roti` 或 `Okoh-MATLAB-ROT-ROTI`）；用一句话向「做定位的同学」解释闪烁为何让人难受 |
| **交付物** | 对照表：VTEC / ROTI / S4 / foF2 / 掩星剖面各回答什么问题（五行即可） |
| **自测门槛** | 能区分「平均雾厚」与「翻滚/闪烁」；不说「TEC 高就一定闪烁」 |

### 第 5 周 · 建图流程

| 项 | 内容 |
|---|---|
| 阅读 | [10](./10-build-gim-workflow.md) |
| 动手 | 根据第 10 课清单，写出你的「多站→STEC→IPP→VTEC→地图」步骤；列出验证项（与 `CDDIS-IONEX` 对比、闭合差、留一站等） |
| **交付物** | 半页「我的区域 VTEC/GIM 流程」+ 验证清单（≥5 条） |
| **自测门槛** | 能画出流水线框图；知道薄壳映射在低高度角容易出事 |

### 第 6 周 · 空间天气复盘 + 产品差

| 项 | 内容 |
|---|---|
| 阅读 | [14](./14-space-weather-case.md)、[18](./18-lab-compare-gims.md) |
| 动手 | 一次事件差分复盘；完成 18 课至少两家 GIM 对比；可选 `GFZ-Kp-Index`/`NOAA-SWPC` 时间轴；可选 `TIE-GCM`/`pytiegcm` 模式对照 |
| **交付物** | 差分图 + 时间轴 + 十句结论；一张中心间 RMSE/均值表 |
| **自测门槛** | 结论含「驱动 / 形态 / 产品局限」；不把分析中心差写成新物理 |

### 第 7 周 · 三维与同化边界 + 论文落地

| 项 | 内容 |
|---|---|
| 阅读 | [11](./11-tomography-basics.md)、[12](./12-data-assimilation-intro.md)、[15](./15-from-paper-to-code.md) |
| 动手 | 选一篇近读论文填「落地四问 + 差异表」；在 `PROJECTS.json` 点出 ≥2 个替代 `name` |
| **交付物** | 论文卡片一份；一句「我无法复现的部分」 |
| **自测门槛** | 能指出层析病态性直觉；能区分经典同化叙事与纯 ML 预报仓 |

### 第 8 周 · 总复盘与自评

| 项 | 内容 |
|---|---|
| 阅读 | 本课全文；回看 [README](./README.md) |
| 动手 | 把下面「能力检查表」全部过一遍；缺啥补哪周 |
| **交付物** | 自测量表打分表（见第 5 节）+ 下一步 30 天计划（三件小事即可） |
| **自测门槛** | 概念/偏差/实操/进阶四块均达到「及格」；宣称精通前先过「良好」 |

**若只有两周**：做完「入门 + 上手」——即第 1–3 周压缩版（路线 A 必做，路线 B 尽力）+ 本课检查表概念栏。进阶以后当工具书查。

**若只有六周**：合并第 7–8 周；第 4 周闪烁可改为「选读 + 一句话」。

---

## 4. 能力检查表（打勾再用「精通」自称）

### 4.1 概念

- [ ] 能区分 STEC / VTEC / TECU，并指出 GIM 格网通常是哪种  
- [ ] 能说明几何无关组合消掉了什么、没消掉什么  
- [ ] 能解释薄壳映射在低高度角为何容易出事  
- [ ] 能一句话说清 IRI/NeQuick 与 GNSS 实测 GIM 的差别  

### 4.2 偏差与产品

- [ ] 能说出卫星 DCB 与接收机 DCB 各何时致命  
- [ ] 能解释为何两家 IGS 分析中心 GIM 可差数 TECU  
- [ ] 知道去 `CDDIS-IONEX`、`IGS-Products`、`DLR-IMPC`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC` 等找什么  
- [ ] 做评价时会写产品不确定性，而不是把单一 IONEX 当真理  

### 4.3 实操

- [ ] 独立完成 [16](./16-practice-one-day-tec.md) 路线 A  
- [ ] 独立完成路线 B，并写出与 GIM 差异的原因假设  
- [ ] 在 `PROJECTS.json` 里按任务名搜到至少三个候选上游  
- [ ] 完成 [18](./18-lab-compare-gims.md) 的差分统计表（至少两家中心）  

### 4.4 进阶判断

- [ ] 能判断问题该用：改正模型 / 实测 GIM / 物理模式 / 闪烁监测 中的哪一类  
- [ ] 能指出层析与同化各自最容易被误解的一点（[11](./11-tomography-basics.md)、[12](./12-data-assimilation-intro.md)）  
- [ ] 读一篇论文能填完 [15](./15-from-paper-to-code.md) 的差异表  
- [ ] 能按 [14](./14-space-weather-case.md) 清单复盘新事件（不抄论文数字）  

---

## 5. 自测量表（打分尺）

对第 4 节每一大块，用下面尺度自评（写日期）：

| 等级 | 含义 | 建议动作 |
|---|---|---|
| **0 未接触** | 词都不熟 | 回对应入门课，勿跳 |
| **1 听过** | 能认词，不能解释 | 重读该课「类比」节 + 做课内测验 |
| **2 及格** | 能向同学讲清直觉，出过至少一张相关图 | 可进下一周；保持笔记 |
| **3 良好** | 能独立排错（下载/单位/DCB/对照日），结论含局限 | 可自称「上手/进阶扎实」 |
| **4 精通可用** | 换新数据/新事件仍能按清单交付，并能指导别人避坑 | 才建议在简历写「熟悉 GNSS TEC 处理与 GIM 产品评估」 |

**板块及格线（教学建议）**：

- 入门结束：概念 ≥2，实操路线 A ≥2  
- 上手结束：偏差 ≥2，实操路线 B ≥2  
- 进阶结束：概念与偏差 ≥3，闪烁/建图相关 ≥2  
- 自称精通前：四大块均 ≥3，且 4.4 进阶判断 ≥3  

把结果复制到笔记：

```
自评日：YYYY-MM-DD
概念：_/4
偏差与产品：_/4
实操：_/4
进阶判断：_/4
本周补洞：________
```

---

## 6. 按问题跳转（急救柜）

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
| 分析中心谁准 | [18-lab-compare-gims.md](./18-lab-compare-gims.md) |
| 不会用本仓库 | [08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md) |

---

## 7. 每周「最小工具篮」（避免选择瘫痪）

不必一次克隆十个仓。按阶段只碰这些**真实 `name`**：

| 阶段 | 软件/库 | 数据 |
|---|---|---|
| 入门 | `ionex` 或 `ionex_reader` 或 `ionex-rs` | `CDDIS-IONEX`（+ `NASA-Earthdata-Login`） |
| 上手 | 上列 + `gnss-tec` 或 `pygnss-tec`；`georinex`；`TEQC` | `IGS-Data-Access`、`CDDIS-GNSS-Archive` |
| 进阶 | `igs-roti` 或 `Okoh-MATLAB-ROT-ROTI`；业务对照 `DLR-IMPC` | `GIRO-DIDBase` / `COSMIC-CDAAC`（按需） |
| 精通 | 上列 + 事件：`GFZ-Kp-Index`、`NOAA-SWPC`；模式可选 `pytiegcm` | 多家 IONEX；论文替代从 `PROJECTS.json` 搜 |

---

## 8. 课堂小测验

**Q1.** 「我把 lists/01 全部星标了」算精通吗？  
<details><summary>参考答案</summary>
不算。精通看的是判断、检索、误差叙事与可交付复盘/差异表，不是收藏数量。
</details>

**Q2.** 第 1 周交付物只有截图、没有单位和工具名，为何不及格？  
<details><summary>参考答案</summary>
无法复现、无法审阅。本路线图要求图上有 TECU/日期，笔记有 PROJECTS.json 一致的 name。
</details>

**Q3.** 只有两周时间，你应砍掉什么、保留什么？  
<details><summary>参考答案</summary>
保留入门+上手：路线 A 必做，路线 B 尽力；概念与 DCB 直觉。砍掉层析/同化深潜与完整磁暴论文级复盘（可留到以后当工具书）。
</details>

**Q4.** 自测「偏差与产品」已到 3，但从未做过两家 GIM 对比，分数可信吗？  
<details><summary>参考答案</summary>
不可信。请补做第 18 课；产品不确定性必须有亲自算过的数感。
</details>

**Q5.** 简历写「精通电离层同化」的最低证据是什么？  
<details><summary>参考答案</summary>
至少能画同化框图、区分同化与纯 ML 预报、指出主要误差/观测算子问题，并有公开数据小实验或认真差异表——而不是只跑过一个预测仓库。见第 12、15 课。
</details>

---

## 9. 下一站

- 回 [教学目录 README](./README.md) 按入门 / 进阶 / 精通·实战 / 实验课跳转  
- 本周若卡在「中心间到底差多少」→ [18-lab-compare-gims.md](./18-lab-compare-gims.md)  
- 数据与分类：[`docs/data-access.md`](../data-access.md)、[`docs/categories.md`](../categories.md)  
- 软件表：[`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) · 总表 [`PROJECTS.json`](../../PROJECTS.json)
