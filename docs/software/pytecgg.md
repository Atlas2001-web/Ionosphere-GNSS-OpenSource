# PyTECGg · 校准 TEC 操作手册

目录：[`PROJECTS.json` → `PyTECGg`](../../PROJECTS.json) · 上游 <https://github.com/viventriglia/PyTECGg> · 文档 <https://viventriglia.github.io/PyTECGg/> · GPL-3.0 · Python+Rust

> **作者：viventriglia 等（不是本索引维护者自有项目）。** 勿与维护者 MATLAB [SH-GIM](./sh-gim.md) 混淆。参数以上游文档 / API 为准。

## 1. 用途与边界

### 1.1 一句话

从 RINEX OBS/NAV 做几何无关组合、弧段整平、偏差估计与校准，输出校准 **sTEC/vTEC** 与站天顶 **veq** 等（Polars DataFrame）。

### 1.2 应该用

- 需要有绝对意义的 TEC 时序 / IPP
- 可编程批处理；多星座（G/E/C/R）；RINEX 2/3/4、Hatanaka
- 路径 A 核心工具

### 1.3 不应该用

- 只探活 → [georinex](./georinex.md)
- ROTI 一体机 → [ionomoni](./ionomoni.md)/[oasis-roti](./oasis-roti.md)
- 全球球谐求解 → 开源 GIM；见 [sh-gim](./sh-gim.md) 边界
- 把未校准相对 TEC 当产品发表

### 1.4 作者边界（必读）

| 项目 | 作者关系 |
| --- | --- |
| PyTECGg | **viventriglia** |
| SH-GIM | 本仓维护者；求解器未开源 |
| georinex | geospace-code |

## 2. 多平台安装

### 2.1 要求

官方标明 Python **3.11–3.13**（以当前文档为准）；多数平台有 wheel。

### 2.2 pip

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip pytecgg
python -c "import pytecgg; print(pytecgg.__file__)"
```

### 2.3 源码 / Rust

无 wheel 时需 Rust 工具链按上游编译。Docker Batch 见上游。

### 2.4 报错表

| 现象 | 处理 |
| --- | --- |
| No matching distribution | 换 3.11–3.13 |
| 编译失败 | 装 Rust；或等 wheel |
| Hatanaka 失败 | 按上游补依赖 |
| GPLv3 顾虑 | 读 LICENSE 再集成 |

## 3. 完整逐步命令与期望输出

### 3.1 准备双频 OBS + 混合 NAV

```bash
# 确认不是 HTML；gtime 非空
head -n 8 data/SITE.rnx
python -m georinex.gtime data/SITE.rnx
```

### 3.2 最小校准脚本

```python
from pathlib import Path
from pytecgg.parsing import read_rinex_nav, read_rinex_obs
from pytecgg import GNSSContext
from pytecgg.satellites import prepare_ephemeris, satellite_coordinates, calculate_ipp
from pytecgg.linear_combinations import calculate_linear_combinations
from pytecgg.tec_calibration import (
    extract_arcs, calculate_tec, calculate_vertical_equivalent,
)

NAV_PATH = Path("BRDC00IGS_R_20240910000_01D_MN.rnx")
OBS_PATH = Path("YOUR00XXX_R_20240910000_01D_30S_MO.rnx")

nav_dict = read_rinex_nav(NAV_PATH)
df_obs, rec_pos, rinex_version = read_rinex_obs(OBS_PATH)
ctx = GNSSContext(
    receiver_pos=rec_pos,
    receiver_name=OBS_PATH.name[:4].lower(),
    rinex_version=rinex_version,
    h_ipp=350_000,
    systems=["G", "E"],
)

ephem_dict = prepare_ephemeris(nav_dict, ctx)
df_lc = calculate_linear_combinations(df_obs, ctx, selection_mode="availability")
df_coords = satellite_coordinates(df_lc["sv"], df_lc["epoch"], ephem_dict)
df_arcs = extract_arcs(df_lc, ctx, min_arc_length=120).join(
    df_coords, on=["sv", "epoch"], how="left"
)
df_geom = calculate_ipp(df_arcs, ctx, min_elevation=20)

df_calibrated = calculate_tec(
    df_geom, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30,
)
df_veq = calculate_vertical_equivalent(
    df_calibrated, ctx=ctx, max_polynomial_degree=3, batch_size_epochs=30,
)
print(df_calibrated.columns)
print(df_calibrated.select(["stec", "vtec"]).describe())
df_calibrated.write_parquet("tec_calibrated.parquet")
df_calibrated.write_csv("tec_calibrated.csv")
```

**期望：** 出现 `stec`/`vtec`/`veq`/`bias` 等列。API 以上游为准（版本演进时以文档为准）。

### 3.3 与 GIM 对照

```bash
# 读同日 IONEX，比日变化与量级，不要求像素一致
# → [ionex-gim](./ionex-gim.md) · 教程 [18](../tutorials/18-lab-compare-gims.md)
```

### 3.4 QC 前门禁

Anubis lite 通过再校准。

### 3.5 批处理骨架

```bash
for obs in data/*_MO.rnx; do
  python scripts/run_pytecgg.py --obs "$obs" --nav data/BRDC.rnx \
    --out out/$(basename "$obs").parquet \
    2>&1 | tee logs/$(basename "$obs").log || echo FAIL "$obs"
done
```

### 3.6 未校准 vs 校准对照

故意跳过 `calculate_tec` 校准步会得到相对量——**不要**当绝对产品。

### 3.7 弧段被剔光

降 `min_arc_length` / 截止角；先检查数据质量。

### 3.8 多星座

`systems=["G","E","C"]` 等；NAV 必须覆盖。

### 3.9 薄壳高度

`h_ipp=350_000`（m）常用；改高度会改 VTEC——写进笔记。

## 4. 参数与字段表

| 项 | 说明 |
| --- | --- |
| `h_ipp` | 薄壳高度（m） |
| `systems` | 星座列表 |
| `min_arc_length` | 最短弧段 |
| `min_elevation` | 截止角（度） |
| `max_polynomial_degree` / `batch_size_epochs` | 校准 |
| `selection_mode` | 线性组合策略 |

### I/O

| 方向 | 内容 |
| --- | --- |
| 输入 | RINEX OBS/NAV（含压缩）；`GNSSContext` |
| 输出 | Polars：stec/vtec/veq/bias/…；parquet/csv |
| 不做 | 全球球谐；ROTI 主产品 |

## 5. 接到哪一步


| 场景 | 链接 |
| --- | --- |
| 索引 | [README](./README.md) |
| 数据 | [data-access](../data-access.md) |
| 读盘 | [georinex](./georinex.md) |
| QC | [anubis](./anubis.md) |
| 清洗 | [gfzrnx](./gfzrnx.md) |
| ROTI | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| GIM | [ionex-gim](./ionex-gim.md) |
| SH-GIM 边界 | [sh-gim](./sh-gim.md) |
| 定位 | [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) |
| 02/09/16 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [09](../tutorials/09-dcb-biases-deep.md) · [16](../tutorials/16-practice-one-day-tec.md) |


路径 A 核心；教程 02/09/16。

## 6. 可操作坑（≥12）

1. 未校准当绝对 TEC  
2. 无 wheel / 版本不符 — 换 3.11–3.13 或装 Rust  
3. 与 SH-GIM 作者混淆  
4. 弧段被剔光  
5. 导航不覆盖  
6. GPLv3 再分发未读 LICENSE  
7. Hatanaka 依赖缺失  
8. 观测码名假设错误  
9. 接收机坐标用错  
10. 薄壳高度偷偷改却比文献  
11. 把 parquet 当 IONEX  
12. 跳过 Anubis  
13. UTC/GPST 混用  
14. 单频硬跑  
15. 批处理静默空文件  
16. API 0→2 变更却抄旧脚本 — 以上游文档为准  

## 7. 同类怎么选

| 需求 | 选 |
| --- | --- |
| 校准 TEC 可编程 | **PyTECGg（viventriglia）** |
| 只读盘 | georinex |
| 扰动指数 | OASIS/IonoMoni |
| 读 GIM | ionex-gim |
| 自建球谐 | 开源 GIM；SH-GIM 仅边界 |

## 8. 场景卡片

一日 TEC 练习、与 GIM 对照、DCB 概念课、磁暴日 TEC 时序。

## 9. 命令一页纸

```bash
pip install pytecgg
python -c "import pytecgg; print(pytecgg.__file__)"
# 然后跑 3.2 脚本
```

## 10. 端到端剧本

数据 → gtime → Anubis → 3.2 校准 → parquet → ionex 对照 → 笔记。

## 11–15. 日志 / 契约 / 合规 / 失败矩阵 / 移交

同系列手册；GPL-3.0 再分发谨慎；作者归属写清 viventriglia。

## A1. 操作时间盒（番茄钟）

25 min 安装验收；25 min example；25 min 自备数据；15 min 写复现包。

### A1.1 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 1 个假设

### A1.2 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 2 个假设

### A1.3 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 3 个假设

### A1.4 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 4 个假设

### A1.5 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 5 个假设

### A1.6 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 6 个假设

### A1.7 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 7 个假设

### A1.8 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 8 个假设

### A1.9 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 9 个假设

### A1.10 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 10 个假设

### A1.11 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 11 个假设

### A1.12 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 12 个假设

### A1.13 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 13 个假设

### A1.14 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 14 个假设

### A1.15 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 15 个假设

### A1.16 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 16 个假设

### A1.17 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 17 个假设

### A1.18 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 18 个假设

### A1.19 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 19 个假设

### A1.20 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 20 个假设

## A2. 输入/输出矩阵（扩）

| # | 输入 | 变换 | 输出 | 验收 |
| --- | --- | --- | --- | --- |

| 1 | 数据/配置 1 | 本工具步骤 1 | 产物 1 | size>0 + 关键字 |

| 2 | 数据/配置 2 | 本工具步骤 2 | 产物 2 | size>0 + 关键字 |

| 3 | 数据/配置 3 | 本工具步骤 3 | 产物 3 | size>0 + 关键字 |

| 4 | 数据/配置 4 | 本工具步骤 4 | 产物 4 | size>0 + 关键字 |

| 5 | 数据/配置 5 | 本工具步骤 5 | 产物 5 | size>0 + 关键字 |

| 6 | 数据/配置 6 | 本工具步骤 6 | 产物 6 | size>0 + 关键字 |

| 7 | 数据/配置 7 | 本工具步骤 7 | 产物 7 | size>0 + 关键字 |

| 8 | 数据/配置 8 | 本工具步骤 8 | 产物 8 | size>0 + 关键字 |

| 9 | 数据/配置 9 | 本工具步骤 9 | 产物 9 | size>0 + 关键字 |

| 10 | 数据/配置 10 | 本工具步骤 10 | 产物 10 | size>0 + 关键字 |

| 11 | 数据/配置 11 | 本工具步骤 11 | 产物 11 | size>0 + 关键字 |

| 12 | 数据/配置 12 | 本工具步骤 12 | 产物 12 | size>0 + 关键字 |

| 13 | 数据/配置 13 | 本工具步骤 13 | 产物 13 | size>0 + 关键字 |

| 14 | 数据/配置 14 | 本工具步骤 14 | 产物 14 | size>0 + 关键字 |

| 15 | 数据/配置 15 | 本工具步骤 15 | 产物 15 | size>0 + 关键字 |


## A3. 命令备忘录（复制区）

```bash
# 记录你的真实命令
# CMD1=
# CMD2=
# CMD3=
```


## A4. 对照实验设计

| 实验 | 变量 | 对照组 | 观测量 |
| --- | --- | --- | --- |
| E1 | 采样 | 1 Hz vs 30 s | 产物稳定性 |
| E2 | 系统 | G vs GREC | 完整性 |
| E3 | 窗口 | 默认 vs 加严 | 弧段数 |
| E4 | 截止角 | 10 vs 20 | 噪声 |
| E5 | 时间窗 | 全日 vs 事件窗 | 峰值对齐 |


## A5. 交付给同事的一页纸

1. 工具与版本
2. 一条成功命令
3. 输入样例路径
4. 输出样例路径
5. 三个坑
6. 下一工具链接


## A6. 与路径 A–E 的硬连接

- A TEC：data-access → georinex → anubis/gfzrnx → **pytecgg** → ionex-gim
- B 扰动：RINEX → **ionomoni/oasis** → 教程 05/20
- C 实时：pygnssutils/bnc → **bkg-ntripcaster** → rtklib
- D 坐标：anubis → rtklib → **pride-pppar**
- E GIM：ionex-gim；**sh-gim** 仅边界


## A7. 术语速查

| 术语 | 一句话 |
| --- | --- |
| RINEX | 观测交换格式 |
| RTCM | 实时差分电文 |
| NTRIP | 基于 HTTP 的差分传输 |
| STEC/VTEC | 斜/垂直电子含量 |
| ROTI | TEC 变化率指数 |
| S4 | 振幅闪烁指数（硬件） |
| IPP | 穿刺点 |
| DCB | 码偏差 |
| GIM/IONEX | 全球电离层图交换 |
| PPP-AR | 精密单点+模糊度固定 |
| QC | 质量检查 |
| SP3 | 精密轨道 |


## A8. 文件命名建议

```text
logs/TOOL_SITE_YYYYDDD.log
out/YYYY/DDD/SITE/...
qc/TOOL_config.ok
```


## A9. 回归命令清单

```bash
set -euo pipefail
# 1 help
# 2 example
# 3 assert
echo PASS
```


## A10. 结束语

参数冲突时信本机帮助。越界产品不要硬解释。先门禁后科学。


## B1. 岗位操作卡（每天开机）
1. 激活环境 / 确认 PATH
2. df -h 看磁盘
3. 拉取或确认输入数据
4. 跑最小冒烟
5. 开日批
6. 扫 FAIL 日志
7. 抽查 1 个产物
8. 更新实验笔记版本号

## B2. 命令×期望 对照（扩写 20 条）

| # | 你执行 | 期望看见 |
| --- | --- | --- |
| 1 | 步骤 1 命令 | 非空产物或明确错误 |
| 2 | 步骤 2 命令 | 非空产物或明确错误 |
| 3 | 步骤 3 命令 | 非空产物或明确错误 |
| 4 | 步骤 4 命令 | 非空产物或明确错误 |
| 5 | 步骤 5 命令 | 非空产物或明确错误 |
| 6 | 步骤 6 命令 | 非空产物或明确错误 |
| 7 | 步骤 7 命令 | 非空产物或明确错误 |
| 8 | 步骤 8 命令 | 非空产物或明确错误 |
| 9 | 步骤 9 命令 | 非空产物或明确错误 |
| 10 | 步骤 10 命令 | 非空产物或明确错误 |
| 11 | 步骤 11 命令 | 非空产物或明确错误 |
| 12 | 步骤 12 命令 | 非空产物或明确错误 |
| 13 | 步骤 13 命令 | 非空产物或明确错误 |
| 14 | 步骤 14 命令 | 非空产物或明确错误 |
| 15 | 步骤 15 命令 | 非空产物或明确错误 |
| 16 | 步骤 16 命令 | 非空产物或明确错误 |
| 17 | 步骤 17 命令 | 非空产物或明确错误 |
| 18 | 步骤 18 命令 | 非空产物或明确错误 |
| 19 | 步骤 19 命令 | 非空产物或明确错误 |
| 20 | 步骤 20 命令 | 非空产物或明确错误 |

## B3. 配置金样管理

```bash
mkdir -p config/ok
cp config/my.cfg config/ok/my.cfg.$(date +%Y%m%d)
# 坏了立刻回滚金样
```

## B4. 并行安全阀

```bash
# 错误示范：无限制 xargs -P 64
# 建议：
find data -name '*.rnx' | xargs -n 1 -P 2 -I{} bash -c 'run_one "{}"'
```

## B5. 质量抽检三板斧

1. `wc -c` / `ls -la`
2. `head` / `grep` 关键字
3. 画一张时序/散点看是否像噪声

## B6. 与空间天气事件对齐

```text
事件表(UTC) → 换算到 GPST → 裁剪 ROTI/TEC/固定率 → 同一张图
```
不要口算时差。

## B7. 论文材料最小集

- 软件名+版本
- 关键参数表
- 数据来源与 DOY
- QC 结论
- 与独立产品对照（GIM/另一工具）

## B8. 常见误用一句话回绝

| 误用 | 回绝 |
| --- | --- |
| 相对 TEC 当绝对 | 走 pytecgg |
| ROTI 当 S4 | 走 ISMR |
| QC 当科学正确 | QC 只是门禁 |
| 残差当 STEC | 走 TEC 工具 |
| clone SH-GIM 出全球解 | 求解器未开源 |

## B9. 环境变量与密钥

口令进 ENV；不进 git；日志脱敏；示例用 `change-me-now` 必须替换。

## B10. 结束检查脚本

```bash
#!/usr/bin/env bash
set -euo pipefail
echo TOOL_DONE
# test -s output_file
```

## B11. 微操作 1–30

1. 记录主机名
2. 记录工具版本
3. 创建 logs/
4. 创建 out/
5. 备份金样配置
6. 核对 DOY
7. 核对站名
8. 核对采样
9. 核对双频
10. 核对星历日
11. 跑 help
12. 跑 example
13. 跑自备最小窗
14. tee 日志
15. 检查出口码
16. 检查文件大小
17. grep 关键字
18. 画快速图
19. 标记 FAIL
20. 只改一个变量
21. 重跑成功路径
22. 写入笔记
23. 选下游工具
24. 交接复现包
25. 清理临时大文件
26. 轮转日志
27. 核对时间系
28. 核对许可
29. 核对引用
30. 停止越界解读

## B12. 相关工具（复述）

[README](./README.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [ionex-gim](./ionex-gim.md) · [sh-gim](./sh-gim.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [iono-scintillation](./iono-scintillation.md)


## C1. 工具专用验收口令

```bash
# 把下面替换成该工具真实验收命令后粘贴进 CI / 笔记
true
echo ACCEPTANCE_PLACEHOLDER_OK
```

## C2. 输入完整性 10 问

1. 文件是不是 HTML？
2. gzip 完整吗？
3. RINEX 头能 `head` 吗？
4. 时间覆盖到了吗？
5. 双频成对吗？
6. 星历同日吗？
7. 站坐标可信吗？
8. 采样与算法窗匹配吗？
9. 许可允许你的用途吗？
10. QC 过了吗？

## C3. 输出完整性 10 问

1. 文件非空？
2. 时间戳更新？
3. 关键列/关键字在？
4. 无全日 NaN？
5. 日志无 FATAL？
6. 与对照工具趋势同向？
7. 版本记录了吗？
8. 配置金样存了吗？
9. 下游格式对吗？
10. 越界解读删了吗？

## C4. 一页纸命令区（自填）

```bash
# INSTALL:
# SMOKE:
# PROD:
# GREP:
```

