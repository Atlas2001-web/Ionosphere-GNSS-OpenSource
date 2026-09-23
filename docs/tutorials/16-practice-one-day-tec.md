# 16 · 一日实战：从下载到一张 TEC 图

> 目标：用**公开数据 + 目录内工具**，当天跑通最小闭环。  
> 不追求发论文精度；追求「图能解释、差异说得清」。  
> 建议先扫：[08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md)、[`docs/data-access.md`](../data-access.md)。  
> 成功标志：收工时至少有一张带日期、单位（TECU）、色标与上游工具名的图，以及半页「坑与解释」。

---

## 0. 今天你在做什么（人话版）

把电离层想成「地球外层大气里的电子雾」。今天你要做的事只有一件：

**拿到公开测量或公开地图 → 用开源工具打开 → 画出雾有多厚 → 用三句话解释图。**

三条路线难度递增，**只选一条做主线**（可在余量加第二家 GIM 或路线 C 的一小截）：

| 路线 | 一句话 | 适合谁 | 预计净工作 |
|---|---|---|---|
| **A** | 只读别人做好的全球地图（GIM/IONEX） | 上午入门、下午要交差 | 2–4 小时 |
| **B** | 从单个测站原始观测估 STEC | 已会读 IONEX，想碰 RINEX | 4–7 小时 |
| **C** | 扰动日 vs 安静日差分 + 可选 ROTI | 想讲空间天气故事 | 在 A 通了之后 +1–3 小时 |

**类比**：A 是看天气预报图；B 是自己架温度计；C 是对比「台风天 vs 前天」并讨论阵风（ROTI）。

---

## 1. 开工前 15 分钟清单（08:30–08:45）

- [ ] 能打开 `lists/01-ionosphere.md`、`lists/10-gnss-datasets.md`、`PROJECTS.json`  
- [ ] Python 或 Matlab 环境可用（随上游工具；不会两边都装）  
- [ ] 已读 [`docs/data-access.md`](../data-access.md) 里 Earthdata/CDDIS 注册说明  
- [ ] 今天主路线已选定：A / B / C（写在笔记第一行）  
- [ ] 磁盘有数 GB 空闲；网络能访问数据中心  
- [ ] 笔记本模板已建：`日期 / 路线 / 工具名 / 命令 / 截图文件名 / 翻车记录`

**卡住规则**：任一下载/编译卡超过 **40 分钟**，立刻降级——换更简单的上游 `examples/`（如 `tec-example`），或退回路线 A。不要在编译选项里度过中午。

---

## 2. 全天时间盒总表（可打印）

| 时段 | 时钟（示例） | 所有人 | 路线 A 主线 | 路线 B 主线 | 路线 C 主线 |
|---|---|---|---|---|---|
| T0 | 08:30–08:45 | 开工清单 | 同左 | 同左 | 同左 |
| T1 | 08:45–09:30 | 注册与下载通路 | 拿 1 天 IONEX | 确认 Earthdata + 选站 | 选定暴日+安静日 |
| T2 | 09:30–11:00 | — | 读 IONEX 出第一张图 | 下 RINEX+导航并 QC | 下两天 GIM |
| T3 | 11:00–12:00 | 午餐前存档 | 日变化/第二历元 | 跑通 STEC 曲线 | 做出差分图 |
| 午休 | 12:00–13:00 | 离开屏幕 | — | — | — |
| T4 | 13:00–15:00 | — | 两中心对比（加分） | 高度角/DCB 叙事 | 叠 Kp/SYM-H |
| T5 | 15:00–16:00 | — | 写解释三句话 | 与 GIM 插值比 | 可选 ROTI |
| T6 | 16:00–17:00 | 收工检查表 | 交图+笔记 | 交图+笔记 | 交半页结论 |

时区只是示例；核心是**时间盒**，不是必须从 8:30 开始。

---

## 3. 路线 A（最快）：只读 GIM —— 小时级实验手册

### 3.1 目标与成功标准

- 画出全球或中国区 **VTEC** 填色图；  
- 色标单位 **TECU**；图上有**日期、分析中心、文件名或产品代次**；  
- 能用三句话解释：色标范围为啥这样取、图上最显眼结构是啥、是否像「赤道异常双峰/中纬日变」。

**成功**：看得出大尺度结构，而不是噪声雪花。  
**失败**：只有一张无单位、无日期、色标拉伸到夸张对比的「艺术图」。

### 3.2 小时级步骤

#### 08:45–09:30　打通下载

1. 打开 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)，定位：  
   - `CDDIS-IONEX`（主推）  
   - 备选：`JPL-IONEX-Rapid`、`ROB-IONEX-Products`、`GFZ-Global-Ionosphere-Maps`、`UPC-IONEX-Archive`、`WHU-IGS-Ionosphere-AC`  
2. 按 [`docs/data-access.md`](../data-access.md) 完成 `NASA-Earthdata-Login`（若走 CDDIS）。  
3. 选一个**安静日**（教学日）：例如你熟悉的无大暴日期；记下 YYYY、年积日 DDD。  
4. 下载该日至少一家最终或快速 IONEX（文件名近年可能是长名，含 `GIM`/`INX` 字样——以目录实况为准）。  
5. 校验：文件能解压；大小不是 0；用文本方式偷看头部是否有 `EPOCH OF CURRENT MAP` 之类字段（IONEX 特征）。

**故障排除 A1**

| 现象 | 可能原因 | 你该做 |
|---|---|---|
| 401/403 | 未登录或未授权 CDDIS | 重走 Earthdata 授权；检查 `.netrc` |
| 空目录 | 日期/路径写错 | 对照 IGS 产品说明；换 `BKG-IGS-Data-Center` 等镜像思路（仍用本目录条目） |
| 文件是 `.gz` 打不开 | 未解压 | `gunzip` / 上游工具自动解压选项 |
| 不知道选哪家 | 选择焦虑 | **先 CODE 或 IGS 综合/你目录里第一家能下的**，先出图再对比 |

#### 09:30–11:00　读入并出第一张图

1. 安装/克隆其一：`ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer`（以各 README 为准）。  
2. 辅助拉取可用 `ionex-downloader`。  
3. 加载 IONEX → 选一个历元（如 12:00 UTC）→ 画填色图。  
4. 色标：先用自动范围，再人工改成「整数 TECU、不要过多小数」。  
5. 标题模板：`VTEC [TECU] | 2024-xx-xx 12:00 UTC | AC=CODE | file=...`

**故障排除 A2**

| 现象 | 可能原因 | 你该做 |
|---|---|---|
| 库报错找不到模块 | 环境没激活 | 新建 venv；按 README 装依赖 |
| 图全蓝或全红 | 读错层/单位错 | 确认是 TEC 地图不是误差图；查单位因子 |
| 经纬度颠倒 | 行列索引反了 | 画海岸线或国界对照；打印 `lon.min/max` |
| 中国区是空的 | 裁剪范围写反 | 检查经度 0–360 与 −180–180 |

#### 11:00–12:00　看日变化是否「东边升起」

1. 再读相邻两小时历元（如 10:00 与 14:00 UTC）。  
2. 问：高 TEC 结构是否大致随地方时东移？赤道附近是否有双峰迹象？  
3. 若完全乱跳：可能读错历元索引，或下载了损坏文件。

#### 13:00–15:00　加分：两家分析中心

1. 同日再下第二家（例如 JPL / CAS / WHU——以 `CDDIS-IONEX` 实有文件为准）。  
2. 插值到同一经纬网，画 A、B、A−B。  
3. 统计差分均值与 RMSE（教学用即可）。  
4. 详细实验课见 [18](./18-lab-compare-gims.md)。

#### 15:00–16:00　写三句话解释（必须交）

模板：

1. 「色标从 a–b TECU，是因为……」  
2. 「图上最显眼的是……（赤道异常/中纬日侧等）」  
3. 「我信任/怀疑这张图，因为……（产品代次/空洞/与第二家一致性）」

### 3.3 路线 A 收工检查

- [ ] 至少一张合规图  
- [ ] 工具名与 `PROJECTS.json` 一致  
- [ ] 笔记有下载路径与翻车记录  

---

## 4. 路线 B（进阶）：单站 STEC —— 小时级实验手册

### 4.1 目标与成功标准

- 得到某 IGS 站一天各卫星 **STEC**（或穿刺点 VTEC）时间序列；  
- 能解释与同时刻 GIM 插值的差异（常数偏差？低高度角更散？）；  
- 笔记中出现高度角截止与 DCB 相关讨论（详见 [09](./09-dcb-biases-deep.md)）。

**成功**：不是「和 GIM 差不多」四个字，而是「差在哪、为何可能」。

### 4.2 小时级步骤

#### 08:45–09:30　选站与权限

1. 数据入口：`IGS-Data-Access`、`IGS-Products`、`CDDIS-GNSS-Archive`、`BKG-IGS-Data-Center`。  
2. 选一个数据连续的公开站（教学站名以你能下到的为准；常用 IGS 站即可）。  
3. 同一天的**观测 + 导航**都要；日期必须一致。

#### 09:30–11:00　下载、解压、质检

1. 读写：`georinex`、`GFZRNX`；压缩：`RNXCMP` / `crx2rnx` / `hatanaka` 等（按文件类型）。  
2. 质检：`TEQC` 或 `Anubis`；记下中断、周跳嫌疑、多路径脏时段。  
3. 笔记强制记录：采样间隔、系统、大概可见卫星数。

**故障排除 B1**

| 现象 | 可能原因 | 你该做 |
|---|---|---|
| 只有观测没有导航 | 下错目录 | 回同日导航树 / brdc |
| 时间轴错乱 | 导航日与观测日不一致 | 重新配对 |
| 全是空值 | Hatanaka 未还原 | 先 `crx2rnx` 再读 |
| 质检吓死人 | 短时中断常见 | 记录即可；先保证有连续弧段 |

#### 11:00–12:00 & 13:00–15:00　估 STEC

1. 任选：`gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`tec-example`。  
2. 先跑上游最小例子，再换你的站日。  
3. 设置高度角截止（教学起点 15°–30°）。  
4. 处理周跳：相位弧段断开要分段；不要假装一条光滑圣线。  
5. 讨论 DCB：绝对值要较真；若只看变化，写明「未改正接收机 DCB，仅解释相对变化」。

**故障排除 B2**

| 现象 | 可能原因 | 你该做 |
|---|---|---|
| STEC 负得离谱 | 符号/单位/未处理偏差 | 查上游默认单位；对照 [02][09] |
| 毛刺如刺猬 | 低高度角/周跳 | 提高截止角；分段 |
| 每颗星差一个常数 | 正常-ish | 映射+DCB+模糊度常数叙事 |
| 程序要商业 Matlab 工具箱 | 环境不匹配 | 换 Python 系 `gnss-tec`/`pygnss-tec` |

#### 15:00–16:00　与 GIM 比较

1. 用路线 A 的库读同日 IONEX。  
2. 在穿刺点（IPP）位置与时刻插值 GIM VTEC，与你的估计比。  
3. 写差异假设（至少两条）：DCB 基准、映射函数、GIM 平滑、多路径……

### 4.3 路线 B 收工检查

- [ ] STEC/VTEC 曲线图  
- [ ] 高度角策略写明  
- [ ] 与 GIM 差异的原因假设（不是「误差」一词打发）  

---

## 5. 路线 C（选做）：扰动对照 —— 小时级实验手册

### 5.1 目标与成功标准

- 完成「暴日 − 对照日」差分 GIM；  
- 半页结论同时出现：**驱动、TEC 形态、产品局限**；  
- 可选：ROTI 与 VTEC 是否同步的一句判断。

完整方法论见 [14](./14-space-weather-case.md)。本课只给「一天内能做完」的压缩版。

### 5.2 小时级步骤

#### 08:45–09:30　钉事件

1. 用 `NOAA-SWPC`、`GFZ-Kp-Index`、`NOAA-SWPC-Planetary-K` 选已知扰动日。  
2. 选对照：事件前安静日，或 ~27 天前；标题写 `Storm−Quiet(Q)` 或 `Storm−Rot27(R)`。

#### 09:30–12:00　两天 GIM + 差分

1. 对两天重复路线 A 下载与读入。  
2. 同分析中心、同格网插值后相减。  
3. 出差分图；色标对称（正负 TECU）通常更易读。

#### 13:00–15:00　时间轴

1. 区域平均 VTEC 曲线 + Kp 或 SYM-H（来源写条目名）。  
2. 太阳风可选 `NASA-OMNIWeb`。  
3. 问：谁先动？有无延迟？

#### 15:00–16:00　可选 ROTI

1. `igs-roti` 或 `Okoh-MATLAB-ROT-ROTI` 或 `Ionospheric-TEC-ROTI-Interactives`。  
2. 分面板对比，不硬叠。  
3. 写一句同步/不同步。

### 5.3 路线 C 结论六句模板

1. 事件与对照类型……  
2. 差分主瓣位置与符号……  
3. 相对地磁指数的时间关系……  
4. 两家 GIM 是否同向（若做了）……  
5. ROTI 与 VTEC……  
6. 局限：产品代次/平滑/未用测高仪……

---

## 6. 工具索引（名称已核验，勿臆造）

| 步骤 | 去哪 / 用啥 |
|---|---|
| 找软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 找数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 注册下载 | [`docs/data-access.md`](../data-access.md)、`NASA-Earthdata-Login` |
| 不会选工具 | [08](./08-how-to-use-this-catalog.md) |
| 读观测 | `georinex`、`GFZRNX`、`TEQC`、`Anubis` → [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) |
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`tec-example` |
| 读 IONEX | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer`、`ionex-downloader` |
| 业务 TEC 对照 | `DLR-IMPC`、`DLR-IMPC-Products`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC`、`eSWua-TEC`、`IONORING` |
| 地磁/空间天气 | `GFZ-Kp-Index`、`NOAA-SWPC`、`NOAA-SWPC-Planetary-K`、`NASA-OMNIWeb` |
| ROTI | `igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`Ionospheric-TEC-ROTI-Interactives` |

克隆请去**上游 URL**。本仓是索引，不内嵌第三方源码。

---

## 7. 通用翻车点（三条路线共用）

1. **导航文件与观测日期不一致** — STEC 时间轴错乱。  
2. **没设高度角截止** — 低仰角把图炸花。  
3. **色标单位写成 TEU / 任意拉伸** — 审阅退回。  
4. **DCB 未说明就比较绝对值** — 见 [09](./09-dcb-biases-deep.md)。  
5. **一天内并行三条路线** — 通常三个半成品。  
6. **把预报 IONEX 当最终产品写进结论** — 代次必须标注。  
7. **UTC 与地方时混用** — 「东边升起」会讲反。  
8. **工具名凭记忆拼写** — 必须与 `PROJECTS.json` 的 `name` 一致。

---

## 8. 课堂小测验

**Q1.** 路线 A 出图后发现赤道是「一个馒头」而不是双峰，一定是数据错了吗？  
<details><summary>参考答案</summary>
不一定。可能是地方时/季节/平滑导致双峰不明显，或色标范围不当。先换历元、查第二家 GIM，再怀疑读库错误。
</details>

**Q2.** 路线 B 与 GIM 差一截近乎常数的 TECU，下一步最该读哪课？  
<details><summary>参考答案</summary>
[09 DCB](./09-dcb-biases-deep.md)。先分清「绝对水平」与「相对变化」目标。
</details>

**Q3.** 卡在编译某 TEC 工具 50 分钟，正确策略是？  
<details><summary>参考答案</summary>
触发 40 分钟规则：换 `tec-example` 或路线 A，先出图。编译细节留到有导师/文档的第二日。
</details>

**Q4.** 路线 C 只交了暴日 GIM、没有对照，为什么不合格？  
<details><summary>参考答案</summary>
看不出相对什么变化；无法区分气候背景与暴扰。必须有对照日与差分叙事。
</details>

---

## 9. 收工检查表（17:00）

- [ ] 至少一张带日期、单位、色标的图  
- [ ] 笔记写了所用上游仓库名（与 `PROJECTS.json` 一致）  
- [ ] 写了至少一个「和预期不符」及你的解释  
- [ ] 主路线成功标准已自评（A/B/C 见上文）  
- [ ] 下一步指向 [10-build-gim-workflow.md](./10-build-gim-workflow.md)、[14](./14-space-weather-case.md)、[17](./17-roadmap-beginner-to-expert.md) 或 [18](./18-lab-compare-gims.md)

---

## 10. 延伸阅读

- [10-build-gim-workflow.md](./10-build-gim-workflow.md) · [14-space-weather-case.md](./14-space-weather-case.md) · [15-from-paper-to-code.md](./15-from-paper-to-code.md) · [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md) · [18-lab-compare-gims.md](./18-lab-compare-gims.md)

**相关软件**：[`georinex`](../software/georinex.md) · [`pytecgg`](../software/pytecgg.md) · [`ionex-gim`](../software/ionex-gim.md) · [`anubis`](../software/anubis.md)
