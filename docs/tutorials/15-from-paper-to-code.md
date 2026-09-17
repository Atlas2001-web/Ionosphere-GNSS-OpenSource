# 15 · 从论文到开源：别只收藏 PDF

> 前置：[08 用目录](./08-how-to-use-this-catalog.md) · [17 路线图](./17-roadmap-beginner-to-expert.md)  
> 精通标志：合上任意一篇 TEC/GIM/闪烁方法论文，能填完「落地四问 + 差异表」，并在 `PROJECTS.json` 里点出可替代工具名。  
> 本课目标：把「读过」变成「能动手复现量级与形态」——不是追求小数点与作者完全一致。

---

## 0. 为什么「收藏 PDF」几乎等于没读

研究生常见文件夹：`papers/iono/` 里躺着 200 个 PDF，文件名还是 `ScienceDirect_……pdf`。问他这篇用什么数据、有没有代码，答案经常是「好像有个 GitHub，我标黄了」。

本课把阅读改成**可检查的工序**。类比：

- PDF 是菜谱照片；  
- `PROJECTS.json` / `lists/` 是你家附近能买到的厨具清单；  
- 你的笔记本是试做记录：哪一步换成了公开数据、哪一步做不到。

成功标准不是「复现到论文图 3 每个像素」，而是：

1. 说清输入观测是什么；  
2. 找到（或不存在）开源实现；  
3. 用公开 IGS 站/公开 IONEX 做出**同量级、同形态**的结果；  
4. 诚实写下「我无法复现的部分」。

---

## 1. 落地四问（合上 PDF 前必须口头答出）

把下面四问抄到笔记扉页。每读一篇方法文，合上前先答；答不上就翻回「Data / Methods」。

### 问 1：观测是什么？

逼自己从下列选项里**勾选 + 写文件级细节**：

| 观测类型 | 你在论文里要找到的线索 | 本仓库常见入口 |
|---|---|---|
| RINEX 观测/导航 | 站名、采样率、系统（GPS/多模） | `IGS-Data-Access`、`CDDIS-GNSS-Archive`、`georinex`、`GFZRNX` |
| IONEX / GIM | 分析中心、最终/快速、时间分辨率 | `CDDIS-IONEX`、`JPL-IONEX-Rapid`、`ROB-IONEX-Products`、`ionex` |
| 测高仪 | 站、foF2/剖面、SAO 等格式 | `GIRO-DIDBase`、`GIRO-portal`、`SAO-Explorer` |
| 掩星 | 任务（如 COSMIC）、产品级 | `COSMIC-CDAAC`、`COSMIC-GNSS-RO-Data`、`awsgnssroutils` |
| 闪烁接收机 / ISMR | S4、σφ、采样 | 见 `lists/01-ionosphere.md` 闪烁相关；`ismr_downloader` 等 |
| 业务 TEC 图 | 近实时产品名 | `DLR-IMPC`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC`、`eSWua-TEC`、`IONORING` |

**类比**：问 1 是「这道菜主料是牛、鸡还是豆腐？」主料没搞清，后面算法讨论全是空中楼阁。

### 问 2：算法核心开源吗？

到论文首页、补充材料、作者页、Zenodo、GitHub 搜。结果只允许归入四类之一（写进笔记）：

1. **有可运行仓**：有 README、有最小例子、许可证清晰。  
2. **有脚本但不可复现**：只有画图，缺数据管道或关键参。  
3. **「可应要求提供」**：邮件彩票；教学上当作**暂不可复现**。  
4. **完全闭源**：只能找本目录「同任务替代品」。

本仓库**不内嵌**第三方源码；克隆请去上游 URL。维护者自有如 `SH-GIM`：目录只收录链接，学球谐 GIM 时优先对照公开 IGS 产品与通用库。

### 问 3：评价能否用公开 IGS 站复现？

很多论文用「合作站网 / 内部 CORS / 未公开飞机数据」。你要问：

- 评价指标（RMSE、相关、分类准确率）是否依赖私有真值？  
- 若把输入换成 `IGS-Products` / `IGS-Data-Access` 公开站，实验叙事是否还成立？  
- 若不能完全复现，你能否改成「同类公开实验」并在文中降级表述？

**诚实降级句式**：

> 「原文使用区域加密站网；本文用 IGS 公开站重复其处理链，仅比较相对变化与形态，不声称数值完全一致。」

### 问 4：本仓库有没有同任务替代品？

打开 [`PROJECTS.json`](../../PROJECTS.json) 或 [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) / [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)，按任务关键词搜：

| 任务 | 可搜的真实 `name` 示例 |
|---|---|
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`tec-example` |
| 读/画 IONEX | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer`、`ionex-downloader`、`ionex_formatter` |
| ROTI | `igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`Ionospheric-TEC-ROTI-Interactives` |
| 经验模型 | `IRI-2020-package`、`iri2020`、`PyIRI`、`NeQuick2-ICTP`、`Galileo-NeQuick-G`、`NequickG` |
| 物理/模式接口 | `TIE-GCM`、`pytiegcm`、`GITM`、`sami2py`、`Kamodo` |
| 层析相关 | `IonoTomo`、`GNSS_TOM`、`Geometric-Matrix-For-Ionospheric-Tomogrphy`、`synthetic_ionospheric_tomography_isl` |
| RINEX/质检 | `georinex`、`GFZRNX`、`TEQC`、`Anubis`、`RNXCMP` |
| 数据门户 | `CDDIS-IONEX`、`IGS-Data-Access`、`NASA-Earthdata-Login` |

问 4 的交付物是：**至少写出 1 个数据前端替代 + 1 个算法/产品对比替代**（名称必须与 `PROJECTS.json` 的 `name` 一致）。

---

## 2. 推荐动作顺序（流水线）

把阅读变成这条单向流水线，尽量别跳步：

```
① 读 Data / Methods（先别读 Introduction 抒情）
    ↓
② 用四问填表（观测 / 开源 / 公开可复现性 / 目录替代）
    ↓
③ 在 lists/ 与 PROJECTS.json 搜 TEC、IONEX、ROTI、IRI、tomography…
    ↓
④ 克隆上游「最小例子」或 examples/（不要一上来改核心算法）
    ↓
⑤ 先复现「量级与形态」，再追小数点与颜色条
    ↓
⑥ 写差异表：论文设定 vs 你用的开源/公开数据
    ↓
⑦ 决定：可引用为基线 / 只能启发 / 放弃复现
```

**量级与形态**人话：

- 量级：下午赤道 VTEC 是十几还是上百 TECU？别差一个数量级。  
- 形态：有没有双峰？夜侧是否更低？暴时差分符号对不对？  
- 小数点：色标差 0.5 TECU、相关差 0.02——留到你确认 DCB/映射/站网一致之后。

---

## 3. 差异表模板（每篇论文一张）

直接复制：

```markdown
## 论文卡片：<短标题 / 年份>

| 项 | 论文 | 我的公开替代 | 差距说明 |
|---|---|---|---|
| 观测 | | | |
| 时间范围 | | | |
| 预处理 | | | |
| 核心算法 | | | |
| 开源情况 | | | |
| 评价真值 | | | |
| DCB/映射 | | | |
| 我能复现 | 形态 / 量级 / 数值 / 不能 | | |
| 目录工具 | name1, name2, … | | |
| 一句话结论 | | | |
```

填表示例（虚构叙事，教你格式）：

| 项 | 论文 | 我的公开替代 | 差距说明 |
|---|---|---|---|
| 观测 | 某国 120 站 CORS | IGS 公开站子集 | 站密度低，空间细节必差 |
| 核心算法 | 自研克里金 + 神经网络 | 先用 `gnss-tec`+`ionex` 建基线 | ML 部分无代码 |
| 评价真值 | 作者自有测高仪 | `GIRO-DIDBase` 邻近站 | 站位不同，只比趋势 |
| DCB | 未详述 | 按 [09](./09-dcb-biases-deep.md) 处理并写明 | 绝对 TEC 不可对打 |

---

## 4. 常见坑与绕法（加长版）

### 坑 A：数据不公开

**症状**：Methods 写 “data available upon request”，邮件石沉大海。  
**绕法**：用 `IGS-Data-Access` / `CDDIS-GNSS-Archive` 做**同类**实验；文中明确「非完全复现」。  
**不要**：假装自己复现了原文数值。

### 坑 B：仓库只有画图脚本

**症状**：GitHub 里全是 `plot_fig3.py`，输入是作者处理好的 `.mat`。  
**绕法**：用 `gnss-tec` / `pygnss-tec` / `tec-suite` / `Seemala-GPS-TEC` 补齐前端；用 `ionex` 家族读公开 GIM 当对照。  
**不要**：把画图脚本的 RMSE 当成你复现了算法。

### 坑 C：把 ML 预报仓当成物理同化

**症状**：标题有 “forecast / deep learning / transformer”，你却在笔记写「做了数据同化」。  
**绕法**：回读 [12](./12-data-assimilation-intro.md)：同化有背景场、观测算子、误差协方差叙事；纯预报网络是另一条线。目录里如 `DeepPredTEC`、`Global-TEC-forecasting-DL`、`SpatioTECformer`、`TEC-MoLLM` 等，先当**预报/学习基线**，别和 `TIE-GCM`/`pytiegcm` 混称。  
**检查**：输入特征有没有「未来泄漏」？评价时段是否与训练重叠？

### 坑 D：忽略 DCB / 映射函数

**症状**：你的 STEC 和论文差「几乎整天平行的一条常数」。  
**绕法**：先读 [09](./09-dcb-biases-deep.md)、[02](./02-gnss-dualfreq-tec.md)；确认码类型、卫星 DCB 产品、接收机未知数、薄壳高度。  
**口诀**：差分/ROTI 常可对常数脱敏；绝对 TECU 必须较真。

### 坑 E：高度角与质检被一笔带过

**症状**：低仰角把图炸花，你以为算法不行。  
**绕法**：`TEQC` / `Anubis` / 上游 QC；设高度角截止（常见 15°–30° 教学起点）；记录数据中断。读写可用 `georinex`、`GFZRNX`。

### 坑 F：许可证与数据政策

**症状**：把限制分发的产品塞进公开仓库。  
**绕法**：遵守各门户条款；本目录只索引链接。教学作业交「图与笔记」，不要上传需登录才能拿的原始大包（除非作业平台另有规定）。

### 坑 G：把维护者自有仓当唯一标准答案

**症状**：只克隆 `SH-GIM`，认为球谐 GIM「只有这一家」。  
**绕法**：对照 `CDDIS-IONEX` 多家分析中心 + 通用库 `ionex`/`mosgim`/`m_gim` 等；目录对维护者自有条目只收录链接、不写长分析。

---

## 5. 迷你 Notebook / 实验笔记模板

下面是一个「论文落地」笔记本大纲。你可以用 Jupyter、纯 Markdown 或实验室 Wiki——结构比工具重要。

```markdown
# 落地笔记：<论文短名>

## 0. 元信息
- PDF 路径/DOI：
- 阅读日期：
- 我的科学目标（一句话）：

## 1. 落地四问
1. 观测：
2. 开源：
3. 公开 IGS 可复现性：
4. 目录替代（PROJECTS.json name）：

## 2. 环境
- Python/Matlab/Fortran：
- 克隆的上游 URL 与 commit（若有）：
- 用到的本仓库工具名：

## 3. 数据清单
| 文件 | 来源条目名 | 日期 | 备注 |
|---|---|---|---|

## 4. 最小实验步骤
1. …
2. …
3. 出图文件名：

## 5. 结果（只写我看到的）
- 量级：
- 形态：
- 与论文 Fig.X 异同：

## 6. 差异表
（粘贴第四节模板）

## 7. 下一步
- [ ] 需要补 DCB 课（09）
- [ ] 需要一日实战（16）
- [ ] 需要事件复盘（14）
- [ ] 放弃复现，仅作启发
```

**强制规则**：第 5 节禁止出现「论文说升高 23%，故我也是 23%」——除非你的图独立支持。

---

## 6. 按论文类型的快速指路

| 你读到的论文类型 | 先克隆/先下载 | 先读本系列哪课 |
|---|---|---|
| 单站/多站 TEC 估计 | `gnss-tec` 等 + IGS RINEX | [02](./02-gnss-dualfreq-tec.md)、[09](./09-dcb-biases-deep.md)、[16](./16-practice-one-day-tec.md) |
| GIM 产品对比/融合 | `CDDIS-IONEX` + `ionex` | [03](./03-gim-ionex.md)、[18](./18-lab-compare-gims.md) |
| 建区域地图 | 多站 TEC + [10] 流程 | [10](./10-build-gim-workflow.md) |
| 闪烁/ROTI | `igs-roti` 等 | [05](./05-scintillation-roti.md)、[13](./13-scintillation-modeling.md) |
| IRI/NeQuick 对照 | `iri2020` / `NeQuick2-ICTP` 等 | [04](./04-iri-nequick.md) |
| 磁暴个案 | GIM + `GFZ-Kp-Index` + `NOAA-SWPC` | [14](./14-space-weather-case.md) |
| 层析 | 先读病态性，再碰开源 | [11](./11-tomography-basics.md) |
| 同化/预报 | 先分清同化 vs ML | [12](./12-data-assimilation-intro.md) |

---

## 7. 课堂小测验

**Q1.** 论文说 “code available upon request”，四问第 2 题你应填哪一类？  
<details><summary>参考答案</summary>
归入「可应要求提供 / 教学上暂不可复现」。同时启动问 4 找目录替代，不要空等邮件。
</details>

**Q2.** 你的 TEC 曲线与论文几乎平行但差 8 TECU，最优先检查什么？  
<details><summary>参考答案</summary>
DCB/偏差基准、映射与薄壳高度、码类型是否一致。见第 09 课。不要先改神经网络超参。
</details>

**Q3.** 为什么本课强调「先复现量级与形态」？  
<details><summary>参考答案</summary>
公开数据与作者私有链不可避免有差；若量级/形态都不对，小数点无意义。先证明管道没装反，再追精度。
</details>

**Q4.** 把 `DeepPredTEC` 类仓库写进报告「完成了电离层同化」，错在哪？  
<details><summary>参考答案</summary>
名称与方法叙事通常是预报/学习，不等于经典数据同化（背景场+观测算子+误差协方差）。应按第 12 课重新归类。
</details>

**Q5.** 差异表里「我能复现」一栏只写「能」，为什么不合格？  
<details><summary>参考答案</summary>
必须分级：形态 / 量级 / 数值 / 不能。含糊的「能」无法指导你下一步是改 DCB 还是该放弃。
</details>

---

## 8. 小练习（本课作业）

找你最近读的一篇 TEC/GIM/闪烁论文，在本仓库完成：

1. **落地四问**全文作答（各不少于两句）。  
2. **1 个**可替代其数据前端的工具（`PROJECTS.json` 的 `name`）。  
3. **1 个**可替代其产品对比的数据源条目名。  
4. **1 句**「我无法复现的部分」（必须诚实；禁止写「几乎全部复现」却交不出图）。  
5. （加分）按第五节模板交一份迷你笔记 + 一张你自己跑出来的图。

---

## 9. 和一日实战、路线图的衔接

- 四问答完却不会出图 → 马上去 [16](./16-practice-one-day-tec.md)，把「能找工具」变成「今天出图」。  
- 需要事件叙事 → [14](./14-space-weather-case.md)。  
- 需要多周安排 → [17](./17-roadmap-beginner-to-expert.md)。  
- 需要量化分析中心差 → [18](./18-lab-compare-gims.md)。

---

## 10. 下一课

[16 一日实战](./16-practice-one-day-tec.md)：选路线 A/B/C，按小时推进，带着四问里选出的工具名开工。

---

## 11. 「十分钟检索」示范（跟做一遍）

假设论文标题含 “regional VTEC map using GNSS”。你在仓库根目录的心理动作应是：

1. 打开 `lists/01-ionosphere.md`，扫 TEC / GIM 子区，记下 `gnss-tec`、`ionex`、`mosgim` 等候选。  
2. 打开 `lists/10-gnss-datasets.md`，记下 `CDDIS-IONEX`、`IGS-Data-Access`。  
3. 打开 `docs/data-access.md`，确认 Earthdata 是否要注册。  
4. 回论文 Methods：他们用的是薄壳还是层析？若是薄壳建图，进 [10](./10-build-gim-workflow.md)；若声称层析，进 [11](./11-tomography-basics.md) 先泼冷水。  
5. 克隆**一个**上游最小例子，先跑作者 README 的 hello-world，再换你的公开日。

计时：真正熟练后，步骤 1–3 应在 10 分钟内完成。若做不到，先练 [08](./08-how-to-use-this-catalog.md)，不要在论文 Introduction 里继续盘旋。

**检索口诀**：任务词 → lists → 条目 `name` → data-access → 上游 README → 公开日试跑。
