# G-Nut/Anubis · 多系统 GNSS 观测质检（Free）

目录条目：[`PROJECTS.json` → `Anubis`](../../PROJECTS.json) · 官网 <https://gnutsoftware.com/software/anubis/>  
配置说明：<https://www.pecny.cz/gop/index.php/gnss/70-gnss-software/221-anubis-configuration> · 列表：[03 GNSS 数据](../../lists/03-gnss-data.md)

## 作用与场景

**它是什么**：**G-Nut/Anubis**——RINEX（专业版还含 RTCM 流）**质量检查（QC）** 工具。版本线：**Free / Pro / Real-Time**。本页只讲 **Anubis Free**（撰写时常见标称 **2.3**，Linux，GPL）。

**它解决什么**：在算 TEC/定位之前先问——数据全不全？多路径重不重？哪一系统老掉链？输出 **XTR / XML** 报告，而不是直接给 TEC。

**和 [GFZRNX](./gfzrnx.md) 分工：** GFZRNX **改**文件（拼接、抽稀）；Anubis **评**文件（QC）。常见顺序：GFZRNX → Anubis → 科学软件。

**何时用：** 站网日检、投稿前数据筛选。  
**何时不用：** 只要改采样/拼接 → GFZRNX；要 ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。

## 安装

1. 打开 [下载页](https://gnutsoftware.com/software/anubis/download)（可能需注册），取 **Free / Linux** 包或源码。  
2. 将 `anubis` 放入 `PATH`。  
3. 冒烟：

```bash
anubis -h | head
anubis -X | head    # 默认 XML 配置打到终端
```

> OS X / Windows 二进制在官网常标为另附条件；**以下载页为准**。

## 最小可跑命令

**导出配置并跑 QC**

```bash
anubis -X > anubis_qc.xml
# 编辑 <inp> 中 OBS/NAV 路径，<out> 中 xtr/xml 路径
anubis -x anubis_qc.xml
# 等价：anubis < anubis_qc.xml
```

命令行覆盖路径的骨架（键名以 `anubis -h` / 手册为准）：

```bash
anubis -x anubis_qc.xml \
  :inp:rinexo=data/site0010.24o \
  :inp:rinexn=data/brdc0010.24n
```

**模式概念（在 XML 的 QC 段切换）**

| 模式 | 人话 |
|---|---|
| thin | 偏头信息 / 元数据 |
| lite | 定量：缺口、完整性 |
| full | 定性/综合：更多算法相关 QC，可含 SPP 等 |

**出图（可选，社区脚本）**

```bash
# https://www.pecny.cz/sw/plots/anubis/ 取得 plot_anubis.pl（无官方支持）
perl plot_anubis.pl site0010.xtr
```

## 输入输出

| 方向 | Free 常见内容 |
|---|---|
| 输入 | RINEX 2/3 OBS + NAV；XML 或命令行配置 |
| 输出 | **XTR**（详细文本）、**XML**（汇总 QC）、日志 |
| Pro/RT 才强调 | RTCM3 流、编辑/翻译、组网仪表盘等（本页不展开） |

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 几乎无输出 | 路径/权限不对 | 先 `anubis -X` 对照；改用绝对路径 |
| 只想抽稀/拼接 | 工具选错 | 先 [gfzrnx](./gfzrnx.md) |
| Free 没有实时菜单 | 版本边界 | 实时看官网 RT 版说明 |
| 报告太长 | full 过细 | 先 lite/thin；grep XTR 关键段 |
| 仍怀念 TEQC | 历史习惯 | TEQC 已老；新站网更常见 Anubis + GFZRNX |

## 接到哪一步分析

- QC 后再算 TEC → [georinex](./georinex.md) · [02](../tutorials/02-gnss-dualfreq-tec.md)  
- 扰动指标 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [05](../tutorials/05-scintillation-roti.md)  
- 预处理 → [gfzrnx](./gfzrnx.md)  
- 数据来源 → [数据怎么下](../data-access.md)

## 目录指针

- `PROJECTS.json`：`Anubis` · 相关：`Anubis-Free-Download`、`plot-Anubis`、`GFZRNX`、`TEQC`
