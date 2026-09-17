# 16 · 一日实战：从下载到一张 TEC 图

目标：用**公开数据 + 目录内工具**，当天跑通最小闭环。不追求发论文精度；追求「图能解释、差异说得清」。

建议先扫：[08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md)、[`docs/data-access.md`](../data-access.md)。

---

## 开工前 15 分钟清单

- [ ] 已能打开本仓库 `lists/01-ionosphere.md` 与 `PROJECTS.json`  
- [ ] 已准备 Python 或 Matlab 环境（随你选的上游工具）  
- [ ] 已阅读数据中心注册说明（CDDIS / Earthdata 等，见 data-access）  
- [ ] 明确今天走路线 A、B 还是 C（下面三选一为主，勿并行贪多）  

---

## 路线 A（最快）：只读 GIM

适合：上午入门、下午要出一张图交差。

1. 在 [`docs/data-access.md`](../data-access.md) 与 `CDDIS-IONEX`（或 `JPL-IONEX-Rapid`、`ROB-IONEX-Products`）说明下，拿到**某日** IONEX。  
2. 用 `ionex`、`ionex-rs` 或 `ionex_reader` 加载；也可用 `ionex-downloader` 辅助拉取（以各仓库 README 为准）。  
3. 画出全球或中国区 **VTEC** 填色图，色标单位 **TECU**，写上日期与分析中心。  
4. 再读相邻两小时，看日变化是否「东边升起」——地方时结构是否合理。  
5. （加分）同一时刻对比两家分析中心，做差分直方图。

**成功标准**：图上看得出赤道异常双峰或中纬日变，而不是噪声雪花；你能用三句话解释色标范围为何如此选取。

---

## 路线 B（进阶）：单站 STEC

适合：已会读 IONEX，想碰 RINEX。

1. 下载某 **IGS** 站一天观测 + 导航（入口：`IGS-Data-Access`、`IGS-Products`；读写可参考 `georinex`、`GFZRNX`）。  
2. 质检：`TEQC` 或上游工具自带 QC；记下数据中断与明显毛刺。  
3. 用 `gnss-tec`（或 `pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`）估各卫星 **STEC** 时间序列。  
4. 处理周跳与高度角截止；讨论是否应用 DCB（必读 [09-dcb-biases-deep.md](./09-dcb-biases-deep.md)）。  
5. 把穿刺点 VTEC 与同时刻 IGS GIM 插值比较（GIM 用路线 A 的库）。  

**成功标准**：能解释「为什么和 GIM 差一截常数 / 低高度角更散」，而不是只说「差不多」。

---

## 路线 C（选做）：扰动对照

适合：想碰空间天气叙事。

1. 选一个已知空间天气日（步骤见 [14-space-weather-case.md](./14-space-weather-case.md)）。  
2. 对路线 A 做安静日差分；可选叠 `GFZ-Kp-Index` / `NOAA-SWPC` 时间线。  
3. 有余力再看 ROTI：`igs-roti` 或 `Okoh-MATLAB-ROT-ROTI`。  

**成功标准**：半页结论里同时出现「驱动」「TEC 形态」「产品局限」三句话。

---

## 时间盒建议（一天）

| 时段 | 建议 |
|---|---|
| 0.5 h | 注册/下载通了没有 |
| 1–2 h | 路线 A 出图 |
| 2–3 h | 路线 B 单站（若 A 已通） |
| 1 h | 写笔记：命令、坑、图文件名 |
| 余量 | 路线 C 或第二家 GIM 对比 |

卡住超过 40 分钟：先换更简单的上游例子（`tec-example`、各库 `examples/`），不要深挖编译选项。

---

## 工具索引（名称已核验）

| 步骤 | 去哪 |
|---|---|
| 找软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 找数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 注册下载 | [`docs/data-access.md`](../data-access.md) |
| 不会选工具 | [08-how-to-use-this-catalog.md](./08-how-to-use-this-catalog.md) |
| 读观测 | `georinex`、`GFZRNX`、`TEQC` → [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md) |
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`… |
| 读 IONEX | `ionex`、`ionex-rs`、`ionex_reader`、`ionex-analyzer` |
| 业务 TEC 对照 | `DLR-IMPC`、`ESA-TIO-NRT-TEC`、`NOAA-SWPC-GloTEC` |

克隆请去**上游 URL**。本仓是索引，不内嵌第三方源码。

---

## 常见翻车点

1. **导航文件与观测日期不一致** — STEC 时间轴错乱。  
2. **没设高度角截止** — 低仰角把图「炸」花。  
3. **色标单位写成 TEU / 任意拉伸** — 审阅直接退回。  
4. **DCB 未说明就比较绝对值** — 见 [09](./09-dcb-biases-deep.md)。  
5. **一天内并行三个路线** — 通常三个都半成品。  

---

## 收工检查表

- [ ] 至少一张带日期、单位、色标的图  
- [ ] 笔记里写了所用上游仓库名（与 `PROJECTS.json` 一致）  
- [ ] 写了至少一个「和预期不符」及你的解释  
- [ ] 下一步指向 [10-build-gim-workflow.md](./10-build-gim-workflow.md) 或 [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md)  

---

## 延伸阅读

- [10-build-gim-workflow.md](./10-build-gim-workflow.md) · [14-space-weather-case.md](./14-space-weather-case.md) · [17-roadmap-beginner-to-expert.md](./17-roadmap-beginner-to-expert.md)
