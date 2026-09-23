# 软件操作手册索引

本目录共有 **14 篇**操作手册（合计约 3810 行）：命令、输入输出、坑、选型。不是教材正文。

概念课见 [`docs/tutorials/`](../tutorials/)。条目以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。

参数冲突时：**本机 `-h` / 上游 README > 本手册示例**。

---

## 全部手册（点开即用）

| # | 手册 | 做什么 | 行数 |
| ---: | --- | --- | ---: |
| 1 | [georinex.md](./georinex.md) | RINEX → xarray / Python | 272 |
| 2 | [gfzrnx.md](./gfzrnx.md) | RINEX 检查 / 拼接 / 抽稀 | 414 |
| 3 | [anubis.md](./anubis.md) | 观测 QC → XTR/XML | 393 |
| 4 | [pytecgg.md](./pytecgg.md) | 校准 sTEC/vTEC（作者 viventriglia） | 468 |
| 5 | [ionomoni.md](./ionomoni.md) | STEC / ROTI / AATR（C++） | 172 |
| 6 | [oasis-roti.md](./oasis-roti.md) | ROTI / ΔTEC / SIDX（Python） | 173 |
| 7 | [ionex-gim.md](./ionex-gim.md) | 读 IONEX GIM | 181 |
| 8 | [sh-gim.md](./sh-gim.md) | 维护者球谐仓**边界**（求解器未开源） | 124 |
| 9 | [pygnssutils.md](./pygnssutils.md) | NTRIP CLI / 小 caster | 250 |
| 10 | [bnc.md](./bnc.md) | BKG 多流客户端 | 272 |
| 11 | [bkg-ntripcaster.md](./bkg-ntripcaster.md) | BKG Caster 播发 | 182 |
| 12 | [rtklib.md](./rtklib.md) | RTK / PPP CLI | 272 |
| 13 | [pride-pppar.md](./pride-pppar.md) | PPP-AR | 440 |
| 14 | [iono-scintillation.md](./iono-scintillation.md) | MATLAB 闪烁仿真 | 197 |

每篇结构：**用途边界 → 安装 → 逐步命令+期望输出 → I/O 字段 → 参数 → 接到哪步 → ≥8 坑 → 选型**。

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
| 球谐 GIM 边界说明 | [sh-gim.md](./sh-gim.md) |
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

[ionex-gim](./ionex-gim.md) 读产品；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表里其它 GIM 工具 → 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 事实边界（归属说明，不是目录）

下面两行**不是**「只有这两个软件」，只是容易写错归属的提醒：

| 项目 | 关系 |
| --- | --- |
| [PyTECGg](./pytecgg.md) | 作者 **viventriglia**（不是本仓维护者自有） |
| [SH-GIM](./sh-gim.md) | 本仓维护者自有；**球谐求解器未开源** |
| 本目录其它手册 | 操作说明；许可与 EULA 以上游为准 |

---


最近质检（ops）：Round2 已按 short-hard 重写 **bnc** / **georinex** / **iono-scintillation**（BNC REQC 真跑、georinex 1.16.2 真输出、闪烁仓 Libraries 打包边界；MATLAB 未在质检机运行）；此前 **gfzrnx** / **rtklib** / **pytecgg**。行数以本表 `wc -l` 为准。

## 推荐阅读顺序（新人）

1. 本页「全部手册」表 + [data-access](../data-access.md)
2. [georinex](./georinex.md) 冒烟
3. 路径 A：[pytecgg](./pytecgg.md) + 教程 02/16
4. 路径 B：[oasis-roti](./oasis-roti.md) 或 [ionomoni](./ionomoni.md) + 教程 05
5. 需要定位再 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
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

## 工具依赖速览

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

## 与 tutorials 对照

| 教程 | 优先手册 |
| --- | --- |
| 02 / 16 | georinex · pytecgg |
| 03 / 10 / 18 | ionex-gim · sh-gim(边界) |
| 05 / 13 / 21 | oasis-roti · ionomoni · iono-scintillation |
| 06 / 20 | rtklib · pride-pppar · ionomoni |
| 09 | pytecgg |

---

## 体量与文风

- 常规工具文：稠密操作优先；已全面 QUALITY 改写，多数 120–450 行
- SH-GIM：短边界说明优先（准确 > 凑行）
- 本索引：先列全手册，再写路径
- 禁止问答注水、禁止为凑行数复读

---

## 相关

[data-access](../data-access.md) · [categories](../categories.md) · [tutorials](../tutorials/README.md) · [`PROJECTS.json`](../../PROJECTS.json)
