# 08 · 怎么按研究问题在本仓库找软件

> 本仓库是**链接索引（curated index）**：你在这里读分类、读中文分析、复制上游 URL，然后去上游克隆并遵守**上游许可证**。不要把第三方源码拷进本仓。  
> 本讲教你「按问题找门」，而不是把 611 个条目背下来。

先记住总口号：

1. 用一句话写清问题；  
2. 打开 [`docs/categories.md`](../categories.md) 确认类别；  
3. 打开对应 `lists/*.md`，按**子类**扫表，读「详细中文分析」；  
4. 需要数据时看 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) + [`docs/data-access.md`](../data-access.md)；  
5. 机器检索：在 [`PROJECTS.json`](../../PROJECTS.json) 里搜 `name` / `subcategory` / `category`。

---

## 1. 仓库里都有什么？（地图）

| 路径 | 作用 |
|---|---|
| `lists/01-ionosphere.md` … `lists/10-gnss-datasets.md` | 人读的分类表 + 中文分析 |
| `PROJECTS.json` | 机器可读的全量条目（约 611） |
| `docs/categories.md` | 类别定义与边界 |
| `docs/data-access.md` | 数据门户注册方式徽章怎么读 |
| `docs/tutorials/` | 你正在读的课堂讲义 |
| 根 `README.md` | 标记含义、分类一览、精选表 |
| `CONTRIBUTING.md` | 如何贡献新条目（给人看，不是自动登记机器人） |

**类比：** 本仓像「博物馆导览册」。展品在各上游「博物馆」里；导览册告诉你展厅怎么走、哪件值得先看，但你不能把青铜器搬进导览册装订线。

---

## 2. 标记（markers）怎么读？

根 README 中的标记是**目录层元数据**，帮你判断「这是谁家的、要不要优先读、维护者关系如何」。常见含义：

| 标记 | 含义（人话） |
|:---:|---|
| 🏷️ 官方 | 政府/机构/联盟官方发行，协议与发布页通常更正式 |
| 🏷️ 高校实验室 | 大学课题组维护，论文与代码常一起长 |
| 🏷️ 个人社区 | 个人或小团队/社区，质量参差，但常有黑科技 |
| 🚩 | **维护者自有**公开仓库：本目录**只收录链接，不写长分析**（例：`SH-GIM`） |
| 🔀 | 维护者已 fork：表中列上游；fork 地址见项目页 |
| ★ | 维护者 GitHub 星标种子（便于追溯收藏来源） |
| 核心 | 建议优先阅读的入口级条目 |

`PROJECTS.json` 里还有机器用 `markers` 字段（如 `core`、`starred`、`batch-2026-09-17` 等），与 README 表格是同一套策展信息的不同投影。你写脚本过滤时用 JSON；你肉眼逛列表时看 Markdown 徽章。

### 2.1 常见误解

- **误解：** 「核心 = 唯一正确。」  
  **纠正：** 核心 = 入门优先；课题特殊时非核心条目可能更合适。  
- **误解：** 「🚩 表示质量差。」  
  **纠正：** 🚩 表示**维护者自有、目录不写长文**，避免自卖自夸式详述；不是质量判决。  
- **误解：** 「有 ★ 就一定比官方更好。」  
  **纠正：** ★ 是收藏种子标记，不是 GitHub star 排行榜。

---

## 3. 「注册」在本目录指什么？

这里有两件容易混的事：

### 3.1 数据门户注册（你要用数据时）

许多 GNSS/空间天气数据需要账号，例如 NASA Earthdata、GIRO 门户等。读法见 [`docs/data-access.md`](../data-access.md) 的**注册方式徽章**：

| 徽章概念 | 人话 |
|---|---|
| `form_register` 一类 | 网页自助注册，常即时可用 |
| 其它申请制 | 可能要表单、审核、机构邮箱 |

条目里的 `registration_zh` 是**原创短提示**，不是官网原文拷贝；政策会变，以下载页为准。

### 3.2 向本目录贡献条目（你要加软件时）

读 [`CONTRIBUTING.md`](../../CONTRIBUTING.md)：提交的是**核对过的链接与元数据**，不是把代码塞进 git。本讲后文「贡献」指这件事。

**没有**「在网页点注册才能浏览 lists」这种门槛——克隆/在线阅读即可。

---

## 4. 每次都适用的五步检索法（请练到肌肉记忆）

**步骤 1：一句话问题**  
坏例子：「我想做电离层。」  
好例子：「从 RINEX 估 STEC 并画某站 ROTI。」 / 「下载某日 CODE GIM 并在 Python 绘图。」 / 「跑 Galileo 单频 NeQuick-G 改正。」

**步骤 2：选大厅（category）**  
- 电离层物理/TEC/GIM/模型/闪烁 → `ionosphere` → `lists/01-ionosphere.md`  
- 读 RINEX/质检/NTRIP → `gnss-data` → `lists/03-gnss-data.md`  
- RTK/PPP 工程 → `gnss-positioning` → `lists/04-gnss-positioning.md`  
- 下载数据产品 → `gnss-datasets` → `lists/10-gnss-datasets.md`  

不确定就打开 [`docs/categories.md`](../categories.md)。

**步骤 3：扫子类（subcategory）**  
`01-ionosphere.md` 很长，请用编辑器搜索子类标题：如「TEC 估计」「IONEX/TEC 图」「IRI 模型」「闪烁/ROTI」「测高仪」等。

**步骤 4：读中文分析，点上游 URL**  
看语言、许可、是否核心、输入输出是什么。然后离开本仓，去上游。

**步骤 5：数据与软件配对**  
没有 RINEX，TEC 程序空转；没有 IONEX，读图程序空转。数据侧永远记得 `lists/10` + `data-access.md`。

---

## 5. 场景 A：想估 TEC（RINEX → STEC/VTEC）

| 步骤 | 去哪 |
|---|---|
| 概念 | [01](./01-ionosphere-tec-basics.md)、[02](./02-gnss-dualfreq-tec.md)；偏差深挖 [09](./09-dcb-biases-deep.md) |
| 软件 | `lists/01-ionosphere.md` → 子类 **TEC 估计**（`gnss-tec`、`tec-suite`、`pygnss-tec`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`…） |
| 读 RINEX / QC | `lists/03-gnss-data.md`（`georinex`、`TEQC`、`Anubis`…） |
| 观测数据 | `lists/10-gnss-datasets.md`（`CDDIS-GNSS-Archive` 等） |

**工作例（口述版）：**  
「我要某站一天的 VTEC 曲线」→ 下载 RINEX → `georinex` 确认有双频观测 → `gnss-tec` 或 `pygnss-tec` 估 TEC → 画图。若绝对值与公开 GIM 差一截，先读第 09 讲 DCB，而不是先改物理常数泄愤。

---

## 6. 场景 B：想读 / 画 / 做 TEC 图（GIM、IONEX）

| 步骤 | 去哪 |
|---|---|
| 概念 | [03-gim-ionex.md](./03-gim-ionex.md) |
| 读图软件 | `01-ionosphere` → **IONEX/TEC 图**（`ionex`、`ionex-rs`、`ionex_reader`、`INX_Editor`、`DiffIonMap`…） |
| 自己建图 | 同列表 → **GIM / GIM/球谐映射**（如 `mosgim`；`SH-GIM` 为 🚩 仅收录） |
| 下载产品 | `10-gnss-datasets` → `CDDIS-IONEX`、`JPL-IONEX-Rapid` 等；说明见 [`data-access.md`](../data-access.md) |

**工作例：**  
「只想快速看全球 VTEC 动画」→ 下 IONEX → `ionex` 读取 → 绘图。不必先建站网解算。

**工作例：**  
「想研究建图算法」→ 读 `mosgim` 等；若看到 `SH-GIM`，记住 🚩：去上游看，本仓不写长分析。

---

## 7. 场景 C：想跑 IRI / NeQuick / NeQuick-G

| 步骤 | 去哪 |
|---|---|
| 概念 | [04-iri-nequick.md](./04-iri-nequick.md) |
| 软件 | `01-ionosphere` → **IRI 模型 / IRI/NeQuick / NeQuick-G 官方**（`IRI-Fortran`、`IRI-2026-package`、`IRI-COMMON-FILES`、`PyIRI`、`iri2020`、`NeQuick2-ICTP`、`Galileo-NeQuick-G`、`NequickG`…） |
| 注意 | IRI 常需 COMMON 系数与指数文件，条目分析里会写；NeQuick-G 是改正算法叙事，勿与科研 NeQuick2 开关混用 |

**工作例：**  
「课程要画某经纬点 \(N_e(h)\)」→ `IRI-2026-package` + `IRI-COMMON-FILES`（或 `PyIRI`/`iri2020` 封装）→ 输出廓线。  
「单频定位改正」→ `Galileo-NeQuick-G`，不要误下成只为气候学对比的包还抱怨电文参数对不上。

---

## 8. 场景 D：想下 GNSS / 电离层数据

| 步骤 | 去哪 |
|---|---|
| 门户与注册 | [`docs/data-access.md`](../data-access.md) |
| 条目表 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 例 | 观测：`CDDIS-GNSS-Archive`；GIM：`CDDIS-IONEX`；掩星：`COSMIC-CDAAC`；测高：`GIRO-DIDBase` |

**工作例：**  
先完成 Earthdata（或对应门户）注册 → 再谈脚本下载。很多人卡在「软件会了但 403」，其实是账号与授权，不是 Python 锅。批量下载也可看 `FAST` 等工具是否符合你的源。

---

## 9. 场景 E：想看闪烁 / ROTI

| 步骤 | 去哪 |
|---|---|
| 概念 | [05-scintillation-roti.md](./05-scintillation-roti.md) |
| 软件 | `01-ionosphere` → **闪烁**、**闪烁/ROTI**（`igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`Ionospheric-TEC-ROTI-Interactives`、`roti-gnss-ml`、`gnss-scintillation-simulator`、`scintill-ai`、`BiScEF`、`scintkit`、`OASIS`、`IonoMoni`、`gnssutils`、`ismr_downloader`…） |
| 若需先有 TEC | 先走场景 A |

**工作例：**  
只有 RINEX → TEC → ROT → ROTI（`Okoh-MATLAB-ROT-ROTI` / `igs-roti`）。  
有 ISMR → `ismr_downloader` + 处理条目。  
写论文时写「代理指标」，别把 ROTI 叫成 S4。

---

## 10. 场景 F：定位里处理电离层

| 步骤 | 去哪 |
|---|---|
| 概念 | [06-iono-positioning.md](./06-iono-positioning.md) |
| 定位套件 | `lists/04-gnss-positioning.md`（`RTKLIB`、`gLAB-UPC`、`PRIDE-PPPAR`、`ginan`、`pyrtklib`…） |
| 单频模型源码 | `01-ionosphere` 中 `Klobuchar-study-code`、`Galileo-NeQuick-G` 等 |

**工作例：**  
教学 SPP + Klobuchar → 模型条目 + `RTKLIB`/`gLAB-UPC`。  
科研 PPP → 选套件读其电离层选项；若只要 TEC，回到场景 A，勿在 PPP 迷宫失踪。

---

## 11. 场景 G：测高仪或掩星

概念见 [07-ionosonde-occultation.md](./07-ionosonde-occultation.md)。

- 软件偏 `lists/01-ionosphere.md`：`Autoscala-INGV`、`SAO-Explorer`、`POLAN`、`ROM-SAF-ROPP`、`cosmic-crunch`…  
- 数据偏 `lists/10-gnss-datasets.md`：`GIRO-DIDBase`、`COSMIC-CDAAC`、`COSMIC-GNSS-RO-Data`…  
- 解析辅助：`pysatCDAAC`、`awsgnssroutils` 等。

---

## 12. 三个「完整点餐」示范（把场景串起来）

### 点餐 1：我想要 TEC 图

1. 问：自己建，还是用现成 GIM？  
2. 现成：`CDDIS-IONEX` / `JPL-IONEX-Rapid` → `ionex` 读 → 画。  
3. 自建：场景 A 多站 TEC → `mosgim` 等 GIM 方向（进阶见第 10 讲）。  
4. 概念锚点：第 03 讲。

### 点餐 2：我想要 IRI

1. 问：要官方 Fortran、Python 封装，还是在线？  
2. 官方链：`IRI-Fortran` / `IRI-2026-package` + `IRI-COMMON-FILES`。  
3. 封装：`PyIRI`、`iri2020` 等。  
4. 在线参考条目如 `CCMC-IRI-online`（若列表中有，以 `PROJECTS.json` 为准）。  
5. 概念锚点：第 04 讲；验证时可拉测高仪/掩星/GNSS（第 07 讲）。

### 点餐 3：我想要闪烁

1. 问：有没有专用闪烁数据？  
2. 无：场景 A → ROTI 工具。  
3. 有：`ismr_downloader` + `scintkit` / `OASIS` / `IonoMoni` / `BiScEF`…  
4. 要仿真：`gnss-scintillation-simulator` 等。  
5. 概念锚点：第 05 讲；定位失败解释连第 06 讲。

---

## 13. 用 PROJECTS.json 做「机器检索」

不会写复杂程序也行：用编辑器打开 `PROJECTS.json`，搜索字符串。

建议搜索键：

- `"name": "gnss-tec"`  
- `"subcategory": "闪烁"`  
- `"category": "ionosphere"`  

字段直觉：

| 字段 | 用途 |
|---|---|
| `name` | 目录中的唯一称呼（本讲引用的就是它） |
| `url` | 上游地址，**以它为准** |
| `category` / `subcategory` | 大厅与房间 |
| `markers` | 核心/星标/批次等 |
| `desc_zh` / `analysis_zh` | 中文简介与分析 |
| `license` / `language` | 许可以语言 |

**同名不同源：** 只信 `url`。口头简称「那个 TEC 工具」不够。

---

## 14. 别踩的坑（索引仓十诫缩编）

1. **索引仓 ≠ 代码合集** — 只保留核对过的链接。  
2. **🚩 维护者自有** — 只收录、不写长分析（如 `SH-GIM`）。  
3. **同名不同源** — 以 `PROJECTS.json` 的 `url` 为准。  
4. **先数据后软件** — 没 RINEX/IONEX，再好的程序也空转。  
5. **先质量检查再科学故事** — `Anubis`/`TEQC` 能省一周自我怀疑。  
6. **许可在上游** — 本目录 CC0 不覆盖第三方代码许可。  
7. **核心不是教条** — 特殊课题请深挖子类。  
8. **注册政策会变** — 以官网为准，本仓提示仅导航。  
9. **教程里的条目名必须真实** — 不要发明仓库名；以 JSON 为准。  
10. **问题一句话写不清，就不要开始装环境** — 先写清输入/输出。

---

## 15. 常见误解

### 误解 A：「把 lists 当 pip 源安装」

**纠正：** 这里没有 `pip install 本仓库` 一键拿到全部电离层软件。去上游。

### 误解 B：「CONTRIBUTING 是数据账号注册」

**纠正：** 那是给目录贡献条目；数据账号见 `data-access.md`。

### 误解 C：「教程写过的名字以后永远存在」

**纠正：** 策展会更新；以当前 `PROJECTS.json` 与 lists 为准。

### 误解 D：「一个场景只能用一个软件」

**纠正：** 常是「读数工具 + 估 TEC + 画图 + 数据门户」组合拳。

### 误解 E：「我在本仓 git push 了上游补丁」

**纠正：** 请向**上游**贡献；本仓一般只更新链接与分析。用户要求无 git push 时，更不要乱推。

---

## 16. 自测题

1. 本仓库是代码大合集还是链接索引？  
2. 🚩 标记的正确理解是什么？  
3. 数据注册说明主要在哪个文档？  
4. 想估 TEC，软件列表与数据列表各看哪个文件？  
5. 想跑 NeQuick-G 单频改正，应优先哪个实名条目？  
6. 只有 RINEX 想做闪烁相关，为什么先 ROTI？  
7. `PROJECTS.json` 里应以哪个字段为准解决「同名」？  
8. 点餐「只要 TEC 图」时，为什么可以不先学 PPP？  
9. `core` / 核心标记的建议用法？  
10. 贡献新条目应先读什么文件？

---

## 17. 自测题参考答案

1. 链接索引。  
2. 维护者自有仓库，本目录只收链接、不写长分析。  
3. `docs/data-access.md`。  
4. 软件：`lists/01-ionosphere.md`；数据：`lists/10-gnss-datasets.md`（外加 QC 看 `03`）。  
5. `Galileo-NeQuick-G`（及相关官方条目）。  
6. 常规接收机难出正统 S4；ROTI 是可算的代理。  
7. `url`。  
8. 直接用 IONEX 产品 + 读图工具即可，目标是图不是坐标。  
9. 入门优先阅读，不是唯一真理。  
10. `CONTRIBUTING.md`。

---

## 18. 你离开本讲应能做的三件事

1. 把任意课题压成一句话，并指出该打开的 `lists/*.md`。  
2. 解释标记与注册（数据注册 vs 贡献目录）的区别。  
3. 独立完成「TEC 图 / IRI / 闪烁」三道点餐，且只引用真实条目名。

---

## 延伸阅读（本仓库）

- 本系列目录：[README.md](./README.md)  
- [`docs/categories.md`](../categories.md)  
- [`docs/data-access.md`](../data-access.md)  
- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) · [`03-gnss-data.md`](../../lists/03-gnss-data.md) · [`04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) · [`10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)  
- [`PROJECTS.json`](../../PROJECTS.json) · [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

---

## 19. 现象路由表：我想分析 storm / EIA / TID / 闪烁 → 去哪？

前面场景 A–G 按「产品类型」找软件。科研里更常见的入口是：**「我要分析某某现象」**。下表把现象接到**列表文件 + 教程编号 + 最小工具链**。请从这里抄进开题报告的「数据与方法」草稿。

### 19.1 总路由（先看这张）

| 我说「我想分析…」 | 先读教程 | 主列表 | 常辅列表 | 典型实名入口（举例） |
|---|---|---|---|---|
| **磁暴 storm 的电离层响应** | [14](./14-space-weather-case.md)、[03](./03-gim-ionex.md)、[07](./07-ionosonde-occultation.md)、现象定位残差见 [06](./06-iono-positioning.md) §19+ | `lists/01-ionosphere.md` | `lists/10-gnss-datasets.md`、测高/掩星同 10+01 | `ionex`、`CDDIS-IONEX`、`GIRO-DIDBase`、`COSMIC-CDAAC`、TEC 估计诸条目 |
| **EIA 赤道电离异常** | [01](./01-ionosphere-tec-basics.md)、[03](./03-gim-ionex.md)、[07](./07-ionosonde-occultation.md) §21.2 | `01`（TEC/GIM） | `10`（IONEX/观测） | `ionex`、`mosgim`、`gnss-tec`、`CDDIS-IONEX`；两侧台站测高仪条目 |
| **TID 行进式扰动** | [01](./01-ionosphere-tec-basics.md)、[02](./02-gnss-dualfreq-tec.md)、[07](./07-ionosonde-occultation.md) §21.3；多站 TEC | `01` TEC 估计 | `03` QC、`10` 观测 | `gnss-tec` / `pygnss-tec` / `tec-suite` + 多站 RINEX；GIM 仅作背景 |
| **闪烁 / ROTI / 气泡夜** | [05](./05-scintillation-roti.md)（含一夜清单）、[06](./06-iono-positioning.md) 后果、[13](./13-scintillation-modeling.md) 建模 | `01` 子类 **闪烁**、**闪烁/ROTI** | `10`、`03` | `igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`ismr_downloader`、`scintkit`、`OASIS`、`IonoMoni`… |
| **暴时定位失败分诊** | [06](./06-iono-positioning.md) §19–22、[05](./05-scintillation-roti.md) | `04-gnss-positioning` | `01`、`03` | `RTKLIB`、`gLAB-UPC`、`PRIDE-PPPAR`、`ginan` + ROTI/GIM 对照 |
| **多仪器联合确认** | [07](./07-ionosonde-occultation.md) §20–26 Playbook | `01` + `10` | `03` | GIRO + COSMIC + CDDIS 组合拳 |

### 19.2 「一句话问题 → 路由」速查

把你的话换成下表左列，然后走右列。

| 一句话问题 | 路由 |
|---|---|
| 「暴日全球 TEC 怎么变？」 | 教程 03+14 → `10` 下 IONEX → `01` 读 `ionex` → 差分制图 |
| 「暴日某站 F2 峰抬升了吗？」 | 教程 07 → `10`/`01` 测高仪（`GIRO-DIDBase`…）→ 勿只用 GNSS TEC 替代 |
| 「今晚 EIA 双峰明显吗？」 | 教程 03+07§21.2 → 纬度剖面 VTEC（GIM 或多站） |
| 「这是不是 TID？」 | 教程 07§21.3 → 多站高采样 TEC → 估周期/方向/速度；GIM 太滑时常不够 |
| 「有没有闪烁？」 | 教程 05 → 有 ISMR 走 S4；仅 RINEX 走 ROTI 代理并写清 |
| 「为什么 RTK 固定不了，是不是电离层？」 | 教程 06§19 → 残差画像三型 → 再决定回 05 还是 03 |
| 「掩星能不能证明我的暴时故事？」 | 教程 07 Playbook → `COSMIC-CDAAC` 等 → 检查切点距离 |
| 「我想用模型对比暴/EIA」 | 教程 04 → IRI/NeQuick 条目；验证仍要回 07 的观测三角 |

### 19.3 现象 × 子类搜索词（在 `01-ionosphere.md` 里 Ctrl+F）

| 现象 | 建议搜索的子类/关键词 |
|---|---|
| storm 背景 TEC | TEC 估计、IONEX/TEC 图、GIM |
| storm 峰值 | 测高仪、IRI（对比用） |
| storm 廓线 | 掩星、RO |
| EIA | TEC、GIM、IONEX；（测高仪作锚） |
| TID | TEC 估计；（QC 在 lists/03） |
| 闪烁 | 闪烁、闪烁/ROTI、ismr |
| 定位后果 | 转到 `lists/04-gnss-positioning.md` |

### 19.4 推荐学习顺序（按现象兴趣）

**路径 Storm：**  
08（本路由）→ 03 GIM → 14 空间天气案例 → 07 Playbook → 06 残差分诊 →（可选）12 同化进阶。

**路径 EIA：**  
01 TEC 基础 → 03 GIM → 07§21.2 → 16 一日 TEC 实践 →（可选）10 建 GIM。

**路径 TID：**  
02 双频 TEC → 多站练习（自拟）→ 07§21.3 → 11 层析基础（进阶，理解三维限制）。

**路径 Scintillation：**  
05 全文（含一夜案例）→ 06 后果 → 13 建模 → 08 回表找仿真/ISMR 条目。

### 19.5 反模式（现象分析专用）

1. **拿全球 GIM 证明闪烁** — 分辨率与物理量都不对；回教程 05。  
2. **单站 TEC 振荡就写 TID** — 缺传播参数；回 07§21.3。  
3. **EIA 与闪烁混称** — 背景结构 vs 小尺度不规则体；两句分开写。  
4. **只有定位残差就写「确认闪烁」** — 残差是后果，指标在 05。  
5. **三仪器数字逼相等** — 先对齐定义；回 07§6 与 §22。

### 19.6 把路由写进笔记的填空模板

> 我的现象是 **[storm / EIA / TID / scintillation / 混合]**。  
> 我先读教程 **[编号]**，主列表 **[lists/..]**，辅列表 **[…]**。  
> 最小证据集是 **[仪器1 产品 + 仪器2 产品]**。  
> 确认等级目标是 **[提示 / 支持 / 确认]**。  
> 若分析定位后果，加读教程 **06** 并打开 **lists/04**。  
> 所用条目名以 `PROJECTS.json` 为准：**(列出)**。

---

## 20. 现象路由自测

1. 分析闪烁应先打开哪一讲？ROTI 子类在哪个 list？  
2. 「是不是 TID」为什么不能只靠单站？教程哪一节？  
3. EIA 主力产品是什么？闪烁指标如何正确表述？  
4. 暴时既想看峰高又想看全球 TEC，教程与数据如何分工？  
5. 定位固定失败时，路由上应同时打开哪两个 lists？  
6. 写出 Storm 与 Scintillation 两条推荐学习路径的第一步。  
7. 举一个「用 GIM 证明闪烁」为什么是反模式。  
8. 填空模板里「确认等级目标」三项是什么？

### 20.1 参考答案

1. 教程 05；`lists/01-ionosphere.md` 的闪烁/ROTI。  
2. 需多站传播证据；07§21.3。  
3. VTEC/GIM 纬度结构；闪烁是可能伴随而非 EIA 判据。  
4. 峰高→07+测高仪数据；全球 TEC→03+IONEX；联合→07 Playbook。  
5. `lists/04-gnss-positioning.md` +（对照）`lists/01-ionosphere.md`（及 03 QC）。  
6. Storm：08 路由后读 03；Scintillation：直接精读 05。  
7. GIM 平滑大尺度电子含量，不测量幅度/相位闪烁。  
8. 提示 / 支持 / 确认。

---

## 21. 与场景 A–G 的关系（避免两套地图打架）

- 场景 A–G：**按任务**（估 TEC、读 GIM、跑 IRI…）找门。  
- §19 现象路由：**按科学对象**（storm/EIA/TID/闪烁）找门。  
- 实际课题 = 两者相乘：例如「分析 EIA」→ 现象表指向 TEC/GIM → 再执行场景 A/B 的具体步骤。  
- 「分析闪烁夜的定位后果」→ 现象表 05+06 → 场景 E + 场景 F。

把本节当作封面索引；细节操作仍回各场景与各专题教程。

---

## 22. 增补后你应能做的三件事

1. 听到 storm/EIA/TID/闪烁任一词，能指出教程编号与 list 文件。  
2. 能写出最小证据集与确认等级，而不是只有软件名。  
3. 能把现象路由与场景 A–G 拼成一条不绕路的开题路径。
