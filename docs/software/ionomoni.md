# IonoMoni · 单站 STEC/ROTI/AATR 操作手册

目录：[`PROJECTS.json` → `IonoMoni`](../../PROJECTS.json) · 上游 <https://github.com/qiliu2025/IonoMoni> · C++ / CMake

> 面向 **单站电离层监测时间序列与批量站日** 的岗位。产物常见 STEC/VTEC、ROTI、AATR。不是硬件 S4，不是全球球谐求解器。

## 1. 用途与边界

### 1.1 一句话

C++ 配置驱动：RINEX → STEC/VTEC / ROTI / AATR 等。

### 1.2 与 OASIS

同属扰动指标；IonoMoni 偏 C++/XML；OASIS 偏 Python 脚本链。交叉验证看趋势。

### 1.3 应该用

- 磁暴/不规则体个例时序
- 批量站日产品
- 与 PPP 固定率对照

### 1.4 不应该用

- 替代完整 DCB 绝对 TEC 产品链（看配置能力；深度校准见 pytecgg）
- 全球 GIM
- 硬件闪烁指数

## 2. 安装

```bash
git clone https://github.com/qiliu2025/IonoMoni.git
cd IonoMoni
cmake --list-presets 2>/dev/null || true
cmake --preset <your-preset>    # 名称以仓库为准
cmake --build build --config Release
./bin/IonoMoni -h 2>/dev/null || ls build bin
```

依赖：CMake、C++ 编译器；其它以 README/`CMakeLists.txt` 为准。

### 报错

| 现象 | 处理 |
| --- | --- |
| preset 找不到 | `--list-presets`；读 README |
| 链接失败 | 装依赖库 |
| 可执行不在 bin/ | 在 build/ 查找 |

## 3. 完整逐步命令与期望输出

### 3.1 配置

```bash
cp config/example.xml config/my_site.xml
# 编辑：站坐标、OBS/NAV 路径、频率、截止角、输出目录（示例路径不可用）
```

### 3.2 运行

```bash
./bin/IonoMoni config/my_site.xml 2>&1 | tee logs/ionomoni_run.log
ls output/
```

### 3.3 期望

写出 stec/roti/aatr 等序列；缺文件则日志报错退出。

### 3.4 绘图（若提供 plot/）

```bash
# 名称以仓库为准
python plot/PythonScripts/plot_roti.py
```

### 3.5 批量站日

```bash
for xml in config/sites/*.xml; do
  ./bin/IonoMoni "$xml" 2>&1 | tee logs/$(basename "$xml").log || echo FAIL "$xml"
done
```

### 3.6 与 OASIS 对照

同站日；比趋势；记录两边窗口定义。

### 3.7 与 pytecgg 对照

绝对 TEC 形态用 pytecgg；IonoMoni 侧重监测指数与时序产品（以配置为准）。

### 3.8 高 ROTI → 定位

同窗跑 RTKLIB/PRIDE，解释固定率。

### 3.9 QC 前门禁

Anubis lite 通过再批量。

## 4. 参数与字段

| 项 | 说明 |
| --- | --- |
| 观测/星历路径 | 必须覆盖 |
| 测站坐标 | 错则 IPP/高度角全错 |
| 截止角 | 过低噪声；过高弧段少 |
| 系统/频率 | 与数据一致 |
| ROTI 窗口 | 常见 1 min；改窗勿硬比 |
| 输出目录 | 绝对路径更稳 |

### I/O

| 方向 | 内容 |
| --- | --- |
| 输入 | 双频 OBS；NAV/精密星历；XML |
| 输出 | STEC/VTEC、ROTI、AATR；日志；可选图 |
| 不做 | 全球 GIM；硬件 S4 |

## 6x. 坑（≥12）

1. cmake preset 找不到  
2. 输出空 — 双频/覆盖/截止角  
3. 与 OASIS 量级差 — 窗口/周跳不同  
4. 当 S4 用 — 错  
5. 站坐标错  
6. 1 Hz 太大 — 先 gfzrnx 抽稀  
7. XML 相对路径 + crontab  
8. 未 QC 坏站  
9. 改窗与文献硬比  
10. 只跑单频  
11. 输出目录无写权限  
12. 把 VTEC 当 GIM 栅格发表  
13. 并行打满盘  
14. 时间系混用  
15. 星历日不匹配  
16. 混淆 IonoMoni 与 OASIS 作者/许可  

## 7. 选型

| 需求 | 选 |
| --- | --- |
| C++ 批监测 | **IonoMoni** |
| Python 链 | OASIS |
| 校准 TEC | pytecgg |

## 8. 场景卡片

磁暴个例、赤道夜间、站网日批、与 PPP 对照。

## 5. 接到电离层 / GNSS 哪一步


| 场景 | 链接 |
| --- | --- |
| 索引 | [README](./README.md) |
| 数据 | [data-access](../data-access.md) |
| 读盘 | [georinex](./georinex.md) |
| 清洗 | [gfzrnx](./gfzrnx.md) |
| QC | [anubis](./anubis.md) |
| TEC | [pytecgg](./pytecgg.md) |
| ROTI | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| GIM | [ionex-gim](./ionex-gim.md) · [sh-gim](./sh-gim.md) |
| 实时 | [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 定位 | [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) |
| 闪烁仿真 | [iono-scintillation](./iono-scintillation.md) |
| 02/16 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 05/13/21 | [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 06/20 | [06](../tutorials/06-iono-positioning.md) · [20](../tutorials/20-storm-tec-analysis.md) |
| 03/10/18 | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 09 | [09](../tutorials/09-dcb-biases-deep.md) |


## 6. 可操作坑（≥12）

（工具专用坑见上节列表；通用坑见附录 A。）

## 7. 同类怎么选

见第 7 节表格。

## 8. 场景卡片

见第 8 节。

## 9–15. 运维短章

命令一页纸、端到端剧本、日志关键字、接口契约、安全合规、失败矩阵、移交模板 —— 结构同 [pride-pppar](./pride-pppar.md)/[pygnssutils](./pygnssutils.md)。

## 16. 快速失败矩阵

| 症状 | 先查 |
| --- | --- |
| not found | PATH/venv/build |
| 空输出 | 覆盖/过滤/配置 |
| 鉴权 | 口令/ACL |
| OOM | 切窗/抽稀 |
| NaN | 双频/弧段/星历 |
| 量级差 | 窗口/单位/时间系 |

## 17. 移交模板

`DATE/HOST/VERSION/CMD/INPUT_SHA/CONFIG/LOG/OK|FAIL/NEXT/NOTES`

## 18. 检查表

边界、安装、冒烟、日志、产物、下游、版本、无越界解读。


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

