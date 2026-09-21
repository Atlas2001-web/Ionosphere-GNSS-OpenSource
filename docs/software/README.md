# 软件操作手册索引

本目录是**操作手册**（命令、I/O、坑），不是教材。链接以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。

**事实边界：** PyTECGg = [viventriglia](https://github.com/viventriglia/PyTECGg)；SH-GIM = 本仓维护者自有，**球谐求解器未开源**（见 [sh-gim.md](./sh-gim.md)）。

---

## 30 秒选型

| 你要… | 打开 |
|---|---|
| 读 RINEX 进 Python | [georinex.md](./georinex.md) |
| 改/拼/抽稀 RINEX | [gfzrnx.md](./gfzrnx.md) |
| 观测 QC 报告 | [anubis.md](./anubis.md) |
| 校准 sTEC/vTEC | [pytecgg.md](./pytecgg.md) |
| ROTI / AATR | [ionomoni.md](./ionomoni.md) · [oasis-roti.md](./oasis-roti.md) |
| 读 IONEX GIM | [ionex-gim.md](./ionex-gim.md) |
| 球谐 GIM 边界 | [sh-gim.md](./sh-gim.md) |
| NTRIP 脚本拉流 | [pygnssutils.md](./pygnssutils.md) |
| 多流 GUI / 录盘 | [bnc.md](./bnc.md) |
| 自建 Caster | [bkg-ntripcaster.md](./bkg-ntripcaster.md) |
| RTK / 浮点 PPP | [rtklib.md](./rtklib.md) |
| PPP-AR | [pride-pppar.md](./pride-pppar.md) |
| 闪烁仿真 | [iono-scintillation.md](./iono-scintillation.md) |

---

## 工作流

**A · 一日 TEC**  
[data-access](../data-access.md) → [georinex](./georinex.md) →（可选 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [pytecgg](./pytecgg.md) → [ionex-gim](./ionex-gim.md) 对照 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[16](../tutorials/16-practice-one-day-tec.md)

**B · 不规则体 / 磁暴**  
RINEX → [ionomoni](./ionomoni.md) 或 [oasis-roti](./oasis-roti.md) → 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)；高 ROTI 时段对照 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md) 固定率

**C · 实时差分 / 实验室 CORS**  
[pygnssutils](./pygnssutils.md) 或 [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)；落盘后再走 A/B

**D · 发表级坐标 / ZTD**  
QC（[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [rtklib](./rtklib.md) 冒烟 → [pride-pppar](./pride-pppar.md) + 精密产品

**E · 理解 GIM（非端到端自建）**  
[ionex-gim](./ionex-gim.md) 读产品；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表 `mosgim` / `m_gim` 等

---

## 手册一览

| 文件 | 一行说明 |
|---|---|
| [georinex.md](./georinex.md) | RINEX/SP3 → xarray |
| [gfzrnx.md](./gfzrnx.md) | RINEX 检查/拼接/抽稀 |
| [anubis.md](./anubis.md) | QC → XTR/XML |
| [pytecgg.md](./pytecgg.md) | 校准 TEC（viventriglia） |
| [ionomoni.md](./ionomoni.md) | STEC/ROTI/AATR（C++） |
| [oasis-roti.md](./oasis-roti.md) | ROTI/ΔTEC/SIDX（Python） |
| [ionex-gim.md](./ionex-gim.md) | 读 IONEX |
| [sh-gim.md](./sh-gim.md) | 维护者球谐仓边界 |
| [pygnssutils.md](./pygnssutils.md) | NTRIP CLI / 小 caster |
| [bnc.md](./bnc.md) | BKG 多流客户端 |
| [bkg-ntripcaster.md](./bkg-ntripcaster.md) | BKG Caster 播发 |
| [rtklib.md](./rtklib.md) | RTK / PPP CLI |
| [pride-pppar.md](./pride-pppar.md) | PPP-AR |
| [iono-scintillation.md](./iono-scintillation.md) | MATLAB 闪烁仿真 |

每篇固定结构：用途与边界 → 安装(多平台+报错) → 快速到完整工作流 → 输入输出与字段表 → 常用参数 → 接到 tutorials 哪步 → ≥12 可操作坑 → 同类选型 → 检查清单/附录。

---

## 不要做的事

- 不要把未校准相对 TEC 当绝对产品发表。
- 不要期望 SH-GIM clone 后出全球球谐解。
- 不要把 ROTI 当硬件 S4。
- 不要在未 QC 的坏站上硬跑 PPP/TEC。
- 参数冲突时：**以上游 `-h` / README 为准**。

## 维护备忘

- 上游 CLI 选项偶发更名：以本机 `-h` 覆盖本文示例。
- 新增软件文：沿用上表结构；在本索引补一行；`PROJECTS.json` 先有条目。
- 许可与商业档（Anubis Pro、GFZRNX 例行业务等）以官网 EULA 为准，本文不替代法务。

## 文件体量约定

每篇**主要工具**操作手册目标约 **600–1000** 行：密集命令、I/O 字段表、完整工作流、≥12 可操作坑、同类选型；禁止问答注水、禁止教师式长文注水、禁止薄桩。索引本身约 **80–150** 行。尚未扩写的短文将按同标准后续批次补齐。
