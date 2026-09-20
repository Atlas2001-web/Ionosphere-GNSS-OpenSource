# 软件怎么用（入门索引）

本目录把「目录里收录的软件」翻成**能动手的短文**：作用与场景 → 安装 → 最小示例 → 输入输出 → 常见坑 → 接到哪一步分析。

不是源码大全，也不替代上游手册。链接与分类以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。条目 URL 均已按 `PROJECTS.json` 核验可访问。

## 已写

| 软件 | 一句话 | 文档 | 目录类 |
|---|---|---|---|
| **georinex** | 把 RINEX/SP3 读进 Python（xarray），TEC/PPP 前处理 | [georinex.md](./georinex.md) | [03](../../lists/03-gnss-data.md) |
| **pygnssutils** | Python NTRIP 客户端 / 简易单挂载点 caster | [pygnssutils.md](./pygnssutils.md) | [03](../../lists/03-gnss-data.md) |
| **BNC** | BKG 多流 NTRIP 客户端：拉流、落盘、实时 PPP | [bnc.md](./bnc.md) | [03](../../lists/03-gnss-data.md) |
| **BKG NtripCaster** | 自建 NTRIP 播发（多挂载点、权限与源表） | [bkg-ntripcaster.md](./bkg-ntripcaster.md) | [03](../../lists/03-gnss-data.md) |
| **GFZRNX** | RINEX 检查、拼接、抽稀与格式整理 | [gfzrnx.md](./gfzrnx.md) | [03](../../lists/03-gnss-data.md) |
| **Anubis** | 多系统 GNSS 观测质检（G-Nut Free QC） | [anubis.md](./anubis.md) | [03](../../lists/03-gnss-data.md) |
| **IonoMoni** | 单站 STEC/VTEC、ROTI、AATR 监测（C++） | [ionomoni.md](./ionomoni.md) | [01](../../lists/01-ionosphere.md) |
| **OASIS** | 从 RINEX 算 ROTI / ΔTEC / SIDX 等扰动指标 | [oasis-roti.md](./oasis-roti.md) | [01](../../lists/01-ionosphere.md) |
| **PyTECGg** | 多星座 TEC 重建与校准（作者 viventriglia，非维护者自有） | [pytecgg.md](./pytecgg.md) | [01](../../lists/01-ionosphere.md) |
| **ionex（GIM）** | 用 Python `ionex` 读 IONEX 全球电离层图 | [ionex-gim.md](./ionex-gim.md) | [01](../../lists/01-ionosphere.md) |
| **gnss-scintillation-simulator** | MATLAB 闪烁相位/振幅仿真（相位屏） | [iono-scintillation.md](./iono-scintillation.md) | [01](../../lists/01-ionosphere.md) |
| **RTKLIB** | 开源 RTK / PPP：事后定位、差分、流转发 | [rtklib.md](./rtklib.md) | [04](../../lists/04-gnss-positioning.md) |
| **PRIDE-PPPAR** | 多星座 PPP 模糊度固定（科研级事后精密定位） | [pride-pppar.md](./pride-pppar.md) | [04](../../lists/04-gnss-positioning.md) |
| **SH-GIM** | 球谐 GIM（维护者自有；**仅短述**，求解器未开源） | [sh-gim.md](./sh-gim.md) | [01](../../lists/01-ionosphere.md) |

## 怎么接到本仓教程

| 你想做 | 先读软件文 | 再读教程 / 数据 |
|---|---|---|
| 打开观测文件 | [georinex](./georinex.md) | [02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md) · [数据怎么下](../data-access.md) |
| 检查 / 拼接 / 抽稀 RINEX | [GFZRNX](./gfzrnx.md) / [Anubis](./anubis.md)（QC） | [data-access](../data-access.md) |
| 拉实时差分流 | [pygnssutils](./pygnssutils.md) / [BNC](./bnc.md) | [data-access](../data-access.md) |
| 自建 NTRIP 播发 | [BKG NtripCaster](./bkg-ntripcaster.md) | [data-access](../data-access.md) · [BNC](./bnc.md) |
| 自算 / 校准 TEC | [PyTECGg](./pytecgg.md) | [02](../tutorials/02-gnss-dualfreq-tec.md) · [09 DCB](../tutorials/09-dcb-biases-deep.md) |
| 对照官方全球 TEC 图 | [ionex-gim](./ionex-gim.md) | [03 GIM/IONEX](../tutorials/03-gim-ionex.md) |
| 看闪烁 / 不规则体指标 | [IonoMoni](./ionomoni.md) / [OASIS](./oasis-roti.md) | [05 闪烁与 ROTI](../tutorials/05-scintillation-roti.md) |
| 仿真闪烁信号 | [闪烁仿真](./iono-scintillation.md) | [05](../tutorials/05-scintillation-roti.md) · [13 闪烁建模](../tutorials/13-scintillation-modeling.md) |
| 做定位或要精密产品配合 | [RTKLIB](./rtklib.md) / [PRIDE-PPPAR](./pride-pppar.md) | [06 电离层与定位](../tutorials/06-iono-positioning.md) |
| 了解球谐 GIM 工程边界 | [SH-GIM](./sh-gim.md)（短） | [10 建 GIM 工作流](../tutorials/10-build-gim-workflow.md) |

## 写法约定

- 中文；固定六节：**作用与场景 / 安装 / 最小示例 / 输入输出 / 常见坑 / 接到哪一步分析**。
- 不复制上游长 README；不放流程图；不改 `PROJECTS.json` 批量字段。
- 函数名与 CLI 以核实过的上游为准；版本差异处标明「以当前上游文档为准」。
