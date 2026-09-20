# 软件怎么用（入门索引）

本目录把「目录里收录的软件」翻成**能动手的短文**：它解决什么 → 怎么装 → 最小命令 → 结果长什么样 → 接到哪一课。

不是源码大全，也不替代上游手册。详细链接仍以 [`PROJECTS.json`](../../PROJECTS.json) 与分类列表为准。

## 已写

| 软件 | 一句话：它解决什么 | 文档 |
|---|---|---|
| **georinex** | 把 RINEX/SP3 读进 Python（`xarray`），方便抽观测、做 TEC 前处理 | [georinex.md](./georinex.md) |
| **RTKLIB** | 经典开源 RTK / PPP 解算：事后定位、差分、流转换 | [rtklib.md](./rtklib.md) |
| **BNC** | BKG 多流 NTRIP 客户端：拉实时差分/改正流，可落盘或实时 PPP | [bnc.md](./bnc.md) |
| **ionex（GIM）** | 用 Python `ionex` 读 IONEX 全球电离层图，对照 GIM | [ionex-gim.md](./ionex-gim.md) |
| **OASIS** | 从 RINEX 算 ROTI / ΔTEC / SIDX 等扰动指标 | [oasis-roti.md](./oasis-roti.md) |

## 计划（未写）

| 软件 / 主题 | 一句话：它解决什么 |
|---|---|
| GFZRNX / TEQC | 检查、拼接、抽稀 RINEX（质检与预处理流水线） |
| PRIDE-PPPAR | 多星座 PPP 模糊度固定（科研级事后精密定位） |
| 其他 IONEX 工具 | 下载器、分析器、写回 IONEX 等配套 |

## 怎么接到本仓教程

| 你想做 | 先读软件文 | 再读教程 / 数据 |
|---|---|---|
| 打开观测文件、看有哪些卫星与观测量 | [georinex](./georinex.md) | [02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md) · [数据怎么下](../data-access.md) |
| 对照官方全球 TEC 图 | [ionex-gim](./ionex-gim.md) | [03 GIM/IONEX](../tutorials/03-gim-ionex.md) |
| 看闪烁 / 不规则体指标 | [oasis-roti](./oasis-roti.md) | [05 闪烁与 ROTI](../tutorials/05-scintillation-roti.md) |
| 做定位或要精密轨道产品配合 | [rtklib](./rtklib.md) | [06 电离层与定位](../tutorials/06-iono-positioning.md) |
| 拉实时流 / 差分改正 | [bnc](./bnc.md) | [数据怎么下 · 实时](../data-access.md) |

## 写法约定

- 中文、短段落、表格、命令骨架；不抄上游 README 大段。
- 函数名与 CLI 以核实过的上游为准；不确定处标「以当前上游文档为准」。
- 不写 PyTECGg；SH-GIM 仅在 IONEX 文中极短指针，不展开安装。
