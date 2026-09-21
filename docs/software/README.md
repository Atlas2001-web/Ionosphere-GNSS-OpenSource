# 软件操作手册索引

本目录是**操作手册**（命令、I/O、坑、选型），不是教材正文。链接以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。概念课见 [`docs/tutorials/`](../tutorials/)。

**事实边界（必读）：**

| 项目 | 关系 |
| --- | --- |
| [PyTECGg](./pytecgg.md) | 作者 **viventriglia**（不是本索引维护者自有） |
| [SH-GIM](./sh-gim.md) | 本仓维护者自有；**球谐求解器未开源** |
| 本目录手册 | 操作说明；许可与 EULA 以上游为准 |

参数冲突时：**本机 `-h` / 上游 README > 本手册示例**。

---

## 30 秒选型

| 你要… | 打开 |
| --- | --- |
| 读 RINEX 进 Python | [georinex.md](./georinex.md) |
| 改/拼/抽稀 RINEX | [gfzrnx.md](./gfzrnx.md) |
| 观测 QC 报告 | [anubis.md](./anubis.md) |
| 校准 sTEC/vTEC | [pytecgg.md](./pytecgg.md) |
| ROTI / AATR / ΔTEC | [ionomoni.md](./ionomoni.md) · [oasis-roti.md](./oasis-roti.md) |
| 读 IONEX GIM | [ionex-gim.md](./ionex-gim.md) |
| 球谐 GIM 边界 | [sh-gim.md](./sh-gim.md) |
| NTRIP 脚本拉流 / 小 caster | [pygnssutils.md](./pygnssutils.md) |
| 多流 GUI / 录盘 | [bnc.md](./bnc.md) |
| 自建多用户 Caster | [bkg-ntripcaster.md](./bkg-ntripcaster.md) |
| RTK / 浮点 PPP | [rtklib.md](./rtklib.md) |
| PPP-AR | [pride-pppar.md](./pride-pppar.md) |
| 闪烁仿真（MATLAB） | [iono-scintillation.md](./iono-scintillation.md) |

---

## 工作流路径 A–E

### A · 一日 TEC

[data-access](../data-access.md) → [georinex](./georinex.md) →（可选 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [pytecgg](./pytecgg.md) → [ionex-gim](./ionex-gim.md) 对照 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[09](../tutorials/09-dcb-biases-deep.md)/[16](../tutorials/16-practice-one-day-tec.md)

### B · 不规则体 / 磁暴

RINEX → [ionomoni](./ionomoni.md) 或 [oasis-roti](./oasis-roti.md) → 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)/[21](../tutorials/21-equatorial-anomaly-bubbles.md)；高 ROTI 时段对照 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md) 固定率；仿真概念见 [iono-scintillation](./iono-scintillation.md)·[13](../tutorials/13-scintillation-modeling.md)

### C · 实时差分 / 实验室 CORS

[pygnssutils](./pygnssutils.md) 或 [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)；落盘后再走 A/B

### D · 发表级坐标 / ZTD

QC（[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [rtklib](./rtklib.md) 冒烟 → [pride-pppar](./pride-pppar.md) + 精密产品 → 教程 [06](../tutorials/06-iono-positioning.md)

### E · 理解 GIM（非端到端自建）

[ionex-gim](./ionex-gim.md) 读产品；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表 `mosgim` / `m_gim` 等 → 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 手册一览

| 文件 | 一行说明 | 典型体量 |
| --- | --- | --- |
| [georinex.md](./georinex.md) | RINEX → xarray | ~600–1000 |
| [gfzrnx.md](./gfzrnx.md) | RINEX 检查/拼接/抽稀 | ~600–1000 |
| [anubis.md](./anubis.md) | QC → XTR/XML | ~600–1000 |
| [pytecgg.md](./pytecgg.md) | 校准 TEC（viventriglia） | ~600–1000 |
| [ionomoni.md](./ionomoni.md) | STEC/ROTI/AATR（C++） | ~600–1000 |
| [oasis-roti.md](./oasis-roti.md) | ROTI/ΔTEC/SIDX（Python） | ~600–1000 |
| [ionex-gim.md](./ionex-gim.md) | 读 IONEX | ~600–1000 |
| [sh-gim.md](./sh-gim.md) | 维护者球谐仓**边界** | ~300–500 |
| [pygnssutils.md](./pygnssutils.md) | NTRIP CLI / 小 caster | ~600–1000 |
| [bnc.md](./bnc.md) | BKG 多流客户端 | ~600–1000 |
| [bkg-ntripcaster.md](./bkg-ntripcaster.md) | BKG Caster 播发 | ~600–1000 |
| [rtklib.md](./rtklib.md) | RTK / PPP CLI | ~600–1000 |
| [pride-pppar.md](./pride-pppar.md) | PPP-AR | ~600–1000 |
| [iono-scintillation.md](./iono-scintillation.md) | MATLAB 闪烁仿真 | ~600–1000 |

每篇固定结构（可增减附录）：**用途边界 → 安装 → 逐步命令+期望输出 → I/O 字段 → 参数 → 接到哪步 → ≥12 坑 → 选型**。

---

## 推荐阅读顺序（新人）

1. 本索引 + [data-access](../data-access.md)  
2. [georinex](./georinex.md) 冒烟  
3. 路径 A： [pytecgg](./pytecgg.md) + 教程 02/16  
4. 路径 B： [oasis-roti](./oasis-roti.md) 或 [ionomoni](./ionomoni.md) + 教程 05  
5. 需要定位时再 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)  
6. 实时课再 [pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)  
7. GIM 课 [ionex-gim](./ionex-gim.md)；SH-GIM 仅边界  

---

## 不要做的事

- 不要把未校准相对 TEC 当绝对产品发表。  
- 不要期望 SH-GIM clone 后出全球球谐解。  
- 不要把 ROTI 当硬件 S4。  
- 不要在未 QC 的坏站上硬跑 PPP/TEC。  
- 不要把 PPP 残差当 STEC 产品。  
- 不要把 Free/Pro、公开/专有功能写混。  
- 不要把口令提交进 git。  
- 参数冲突时以上游帮助为准。  

---

## 手册怎么写（维护备忘）

- 上游 CLI 选项偶发更名：以本机 `-h` 覆盖示例。  
- 新增软件文：先有 `PROJECTS.json` 条目；沿用结构；本索引补一行。  
- 许可与商业档（Anubis Pro、GFZRNX 例行业务等）以官网 EULA 为准。  
- **体量约定：** 常规工具文约 **600–1000** 稠密行（命令/I/O/坑优先，禁止注水）；SH-GIM 边界文约 **300–500**；本索引约 **200–400**。  
- 作者归属：PyTECGg=viventriglia；SH-GIM=维护者且求解未开源——写进文首。  

---

## 工具依赖速览（谁先谁后）

```text
data-access
   ├─ gfzrnx (可选清洗)
   ├─ anubis (门禁)
   ├─ georinex (探活)
   ├─ pytecgg (路径 A)
   ├─ oasis-roti / ionomoni (路径 B)
   ├─ ionex-gim (对照)
   ├─ pygnssutils / bnc / bkg-ntripcaster (路径 C)
   └─ rtklib / pride-pppar (路径 D)
sh-gim：仅路径 E 边界，不串进 A/B 主链
iono-scintillation：概念/仿真旁路，不替代实测 ROTI
```

---

## 与 tutorials 对照表

| 教程 | 优先手册 |
| --- | --- |
| 02 / 16 | georinex · pytecgg |
| 03 / 10 / 18 | ionex-gim · sh-gim(边界) |
| 05 / 13 / 21 | oasis-roti · ionomoni · iono-scintillation |
| 06 / 20 | rtklib · pride-pppar · ionomoni |
| 09 | pytecgg |

---

## 故障总入口

1. 选错路径 A–E → 回本页选型表  
2. 输入是 HTML/半截包 → data-access / 鉴权  
3. 工具边界外产物 → 换表内正确手册  
4. 仍败 → 按各手册「复现包」模板打包  

---

## 相关

[data-access](../data-access.md) · [categories](../categories.md) · [tutorials](../tutorials/README.md) · [`PROJECTS.json`](../../PROJECTS.json)


---

## 场景→手册速查（扩）

| 场景 | 手册顺序 |
| --- | --- |
| 课程第一次摸 RINEX | georinex → 教程 02 |
| 要交 TEC 作业 | anubis → pytecgg → ionex-gim |
| 夜间赤道扰动 | oasis-roti 或 ionomoni → 教程 05/21 |
| 磁暴周 | ionomoni + pride/rtklib 固定率 → 教程 20 |
| 实验室 RTK | pygnssutils → rtklib；多人播发再 bkg-ntripcaster |
| 多流运维课 | bnc |
| 理解 GIM 产品 | ionex-gim → 教程 03/18；sh-gim 仅边界 |
| 闪烁物理课 | iono-scintillation → 教程 13；实测仍回 oasis/ionomoni |

---

## 质量门禁（所有路径通用）

1. 输入不是 HTML / 半截压缩包  
2. 时间覆盖已知  
3. Anubis/目视 QC 通过（或记录例外）  
4. 工具版本写入笔记  
5. 不输出越界科学结论  

---

## 体量与文风

- 常规工具文：**600–1000** 稠密操作行  
- SH-GIM：**300–500**（边界准确优先）  
- 本索引：**200–400**  
- 禁止问答注水、禁止为凑行数复读同一段  

---

## 变更记录（维护者）

上游帮助变更时：先改对应工具文第 3/4 节命令与参数表，再改本索引选型句（若有）。不在本索引粘贴长命令。

