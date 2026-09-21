# Anubis · G-Nut Free QC 操作手册

目录：[`PROJECTS.json` → `Anubis`](../../PROJECTS.json) · 官网 <https://gnutsoftware.com/software/anubis/> · 配置说明 <https://www.pecny.cz/gop/index.php/gnss/70-gnss-software/221-anubis-configuration> · 下载 <https://gnutsoftware.com/software/anubis/download> · Free 常见 GPL-3；Pro/RT 商业

> 面向 **RINEX 质量检查** 的岗位。本页只讲 **Anubis Free**（Linux 常见）。输出 XTR/XML，不是 TEC，不是定位引擎。键名以本机 `anubis -h` 与官方配置文档为准。

## 1. 用途与边界

### 1.1 一句话

Anubis（G-Nut）对 GNSS 观测做 QC：完整性、缺口、多路径、SNR、周跳迹象、系统可用性，产出可 grep 的报表。

### 1.2 应该用

- 数据中心日检 / 站网健康
- TEC、ROTI、PPP 前的门禁
- 论文「数据质量」附录材料

### 1.3 不应该用

- 拼接/抽稀/改 RINEX → [gfzrnx](./gfzrnx.md)（顺序：GFZRNX → Anubis → 科学软件）
- 校准 TEC → [pytecgg](./pytecgg.md)（作者 viventriglia）
- ROTI → [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)
- 精密定位 → [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
- Free 文档里写 Pro 功能

### 1.4 与电离层工作的关系

QC 通过 ≠ 绝对 TEC 正确。Anubis 只告诉你「这站这天能不能进流水线」。

## 2. 多平台安装

### 2.1 步骤

1. 打开下载页（可能需注册），取 Free/Linux 预编译或源码。
2. `chmod +x anubis`，放入 `PATH`。
3. 冒烟：

```bash
anubis -h | head -n 40
anubis -X | head -n 50
```

**期望：** 帮助与默认 XML 打出。

### 2.2 报错表

| 现象 | 处理 |
| --- | --- |
| 缺 `.so` | 用官方预编译或按 README 装依赖 |
| `-X` 空 | 重新下载；检查执行位 |
| Windows 换行怪 | 配置 XML 用 LF；`dos2unix` |
| 与 Pro 键混淆 | 只信 Free 文档 |

## 3. 完整逐步命令与期望输出

### 3.1 导出金样 XML

```bash
mkdir -p qc logs
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok
```

编辑 `<inp>` OBS/NAV、`<out>` xtr/xml；**绝对路径更稳**。

### 3.2 单站日运行

```bash
anubis -x qc/anubis_qc.xml 2>&1 | tee logs/anubis_smoke.log
# 或 stdin：anubis < qc/anubis_qc.xml
ls -la *.xtr *.xml 2>/dev/null | head
grep -E 'MP|gap|SNR|Summary|Completeness' *.xtr | head -n 40
```

**期望：** 非空 `.xtr`；终端有摘要。

### 3.3 CLI 覆盖路径（键名以 `-h` 为准）

```bash
anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/abs/data/site0010.24o \
  :inp:rinexn=/abs/data/brdc0010.24n \
  2>&1 | tee logs/anubis_site0010.log
```

### 3.4 模式阶梯 thin → lite → full

在 XML 切换（键名以手册为准）：

| 模式 | 用途 | 耗时 |
| --- | --- | --- |
| thin | 元数据快扫 | 短 |
| lite | 缺口/完整性日检 | 中 |
| full | 综合定量/定性 | 长 |

网检策略：全网 lite → 问题站 full。

### 3.5 批量日检

```bash
for f in /abs/data/*.24o; do
  b=$(basename "$f")
  anubis -x qc/anubis_qc.xml :inp:rinexo="$f" \
    2>&1 | tee "logs/anubis_${b}.log" || echo FAIL "$f"
done
grep FAIL logs/anubis_*.log || true
```

### 3.6 与 GFZRNX 联用

```bash
gfzrnx -finp data/raw.24o -fout data/site_30s.24o -smp 30 -chk -kv -f
anubis -x qc/anubis_qc.xml :inp:rinexo=/abs/data/site_30s.24o
```

### 3.7 门禁：进 TEC / PPP

```bash
# 若 Completeness 极低或 MP 极端 → 跳过科学软件
# 通过 → georinex 探活 → pytecgg / pride-pppar
```

### 3.8 社区绘图（无官方支持承诺）

```text
https://www.pecny.cz/sw/plots/anubis/
# plot_anubis.pl 等指向 XTR
```

### 3.9 与 georinex 交叉验缺口

```bash
python -m georinex.gtime data/site0010.24o
# 对齐时间窗后再比 XTR gap
```

## 4. 参数与文件字段表

### 4.1 CLI

| 项 | 说明 |
| --- | --- |
| `-X` | 打印默认 XML |
| `-x file` | 按配置运行 |
| `:inp:rinexo=` | 覆盖 OBS |
| `:inp:rinexn=` | 覆盖 NAV |

### 4.2 输入

| 类型 | 说明 |
| --- | --- |
| RINEX OBS | 2/3（4 看版本） |
| RINEX NAV | 建议提供 |
| XML | 配置 |

### 4.3 输出

| 类型 | 说明 |
| --- | --- |
| XTR | 主报表 |
| XML | 结构化结果 |
| 日志 | 进度/错误 |

### 4.4 XTR 常搜关键字

`Summary`、`Completeness`、`gap`、`MP`、`SNR`、`slip`/`cs`（字样随版本）。

### 4.5 明确不输出

STEC、ROTI、`.pos`、IONEX。

## 5. 接到电离层 / GNSS 哪一步

| 场景 | 链接 |
| --- | --- |
| 手册索引 | [README](./README.md) |
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
| TEC 课 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 闪烁课 | [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) |
| 磁暴 | [20](../tutorials/20-storm-tec-analysis.md) |
| 定位课 | [06](../tutorials/06-iono-positioning.md) |
| GIM 课 | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) |
| DCB | [09](../tutorials/09-dcb-biases-deep.md) |

路径角色：几乎所有 A/B/D 的「体检站」。

## 6. 可操作坑（≥12）

1. Free/Pro 功能混谈 — 以官网档位为准。
2. 相对路径失败 — 绝对路径或固定 cwd。
3. 把 Anubis 当拼接工具 — 改文件用 gfzrnx。
4. XTR 过大难读 — 先 lite；grep。
5. 与 georinex 缺口不一致 — 对齐窗再比。
6. CRLF 破坏 XML — dos2unix。
7. 缺 NAV — 补 BRDC。
8. QC 通过当绝对 TEC — 错。
9. 批量忽略 FAIL — grep FAIL。
10. 输出覆盖未备份 — 按站日分目录。
11. 键名抄旧教程 — 以本机 `-X` 为准。
12. 坏站硬跑 PPP — 先看 MP/完好率。
13. 只看终端不看 XTR — 不够。
14. Hatanaka 未转 — 先 CRX2RNX。
15. 只读目录写不出 — 改 out。
16. 时区读缺口 — 统一 GPST/UTC。

## 7. 同类怎么选

| 需求 | 选 |
| --- | --- |
| QC 报表 | **Anubis Free** |
| 改 RINEX | gfzrnx |
| 读 Python | georinex |
| 实时流 QC | Pro/RT 或其它链 |

## 8. 场景卡片

### 卡片 A · 新站首日

lite QC → 看完好率/MP → 决定是否纳入 TEC 网。

### 卡片 B · 磁暴日前夜

对事件窗涉及站跑 full → 标记缺口段 → 解释 ROTI/PPP 异常时引用。

### 卡片 C · 数据中心周报

批量 lite → FAIL 列表 → 人工抽 full。

## 9. 门禁阈值示例（自定义，非官方）

| 指标（示意） | 动作 |
| --- | --- |
| 完好率过低 | 丢弃站日 |
| MP 极端 | 丢弃或降权 |
| 长缺口跨事件 | 换站 |

把阈值写进项目协议，不要口头约定。

## 10. 附录：命令一页纸

```bash
anubis -h
anubis -X > qc/anubis_qc.xml
anubis -x qc/anubis_qc.xml
grep -E 'MP|gap|Summary' *.xtr | head
```

## 11. 端到端操作剧本

1. 安装验收  
2. `-X` 金样  
3. 官方/自备最小 OBS+NAV  
4. lite 通过  
5. 记录 XTR 摘要到笔记  
6. 交给 georinex/pytecgg 或 PPP  
7. 若科学结果荒谬，回看 XTR 时段

## 12. 日志关键字与处置

| 关键字 | 处置 |
| --- | --- |
| cannot open | 路径 |
| parse / xml | LF/键名 |
| empty | OBS 坏或窗错 |

## 13. XML 编辑实例（概念）

```xml
<!-- 示意：真实键名以 -X 导出为准 -->
<!-- inp: rinexo / rinexn 绝对路径 -->
<!-- out: xtr / xml 路径 -->
<!-- qc mode: lite -->
```

一次只改一处；保留 `.ok` 金样。

## 14. 与 GFZRNX / georinex 接口契约

| 上游 | Anubis | 下游 |
| --- | --- | --- |
| 原始 RINEX | QC | 决定去留 |
| gfzrnx 清洗后 | QC | georinex / 科学 |
| — | XTR | 不进 TEC 数值计算 |

## 15. 安全与合规

- 遵守官网 EULA；Free/Pro 勿混用分发。
- 站坐标与数据政策按单位规定。
- 日志可能含路径与站名——分享前脱敏。

## 16. 快速失败矩阵

| 症状 | 先查 |
| --- | --- |
| 命令找不到 | PATH / venv |
| 空输出 | 时间覆盖 / 过滤过严 |
| 鉴权失败 | 用户口令 / ACL |
| OOM | 切窗 / 抽稀 / 降并行 |
| NaN 全日 | 双频 / 弧段 / 星历 |
| 与文献数值差一个量级 | 窗口定义 / 单位 / 时间系 |

## 17. 移交与复现信息模板

```text
DATE:
HOST:
TOOL_VERSION:
CMD:          # 口令打码
INPUT_SHA256:
CONFIG:
LOG:
RESULT: OK|FAIL
NEXT_TOOL:
NOTES:
```

## 18. 接到本仓库其它页的检查表

- [ ] 已读本手册用途边界
- [ ] 安装验收通过
- [ ] example/冒烟通过
- [ ] 日志已保留
- [ ] 产出非空
- [ ] 下游工具与格式已选定
- [ ] 版本号写入实验笔记
- [ ] 不把边界外产物当科学结论

| 场景 | 链接 |
| --- | --- |
| 手册索引 | [README](./README.md) |
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
| TEC 课 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 闪烁课 | [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) |
| 磁暴 | [20](../tutorials/20-storm-tec-analysis.md) |
| 定位课 | [06](../tutorials/06-iono-positioning.md) |
| GIM 课 | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) |
| DCB | [09](../tutorials/09-dcb-biases-deep.md) |

## 19. 逐步命令（扩写）：安装后 30 分钟必做

```bash
# A. 金样
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok

# B. 最小站日（路径改成你的）
anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/data/SITE00XXX_R_20240010000_01D_30S_MO.rnx \
  :inp:rinexn=/data/BRDC00IGS_R_20240010000_01D_MN.rnx \
  2>&1 | tee logs/anubis_SITE_001.log

# C. 抽查
grep -E 'Summary|Completeness|MPTH|MP|gap|SNR' *.xtr | head -n 60
wc -l *.xtr

# D. lite 全网骨架
for f in /data/rinex/*.rnx; do
  anubis -x qc/anubis_qc.xml :inp:rinexo="$f" \
    2>&1 | tee logs/anubis_$(basename "$f").log || echo FAIL "$f"
done
```

**期望输出（示意）：**

```text
... Anubis processing ...
writing SITE.xtr
Summary: Completeness ...
MP ...
DONE
```


## 20. 场景卡片（扩）

### 新站验收
lite → 记录完好率 → 决定是否进 TEC 网。

### 事件研究
事件日前对相关站 full → 缺口表进论文附录。

### 清洗后复检
gfzrnx `-smp 30` 后必须再 Anubis，确认没有切坏。

### 与 PPP 对照
PPP 固定率崩盘日 → 回看同日 XTR 的 MP/gap。


## 21. 配方与常用组合

| 配方 | 命令要点 |
| --- | --- |
| 快扫 | thin/lite |
| 问题站深挖 | full + grep MP/gap |
| 清洗后 | gfzrnx → anubis |
| 门禁脚本 | grep Completeness 自定义阈值 |


## 22. 输入抽样检查清单（跑主流程前）

```bash
# 通用
ls -la data/
head -n 20 data/* 2>/dev/null | head -n 40
file data/* 2>/dev/null | head
# 若是压缩包
gunzip -t data/*.gz 2>/dev/null || true
# 若是 RINEX
python -m georinex.gtime data/SITE.obs 2>/dev/null || true
```


## 23. 输出验收清单（跑完后）

- [ ] 目标文件存在
- [ ] `wc -c` 合理（非 0、非异常小）
- [ ] 日志无未处理 FATAL
- [ ] 抽查 3 个关键字段/关键字
- [ ] 时间覆盖符合任务窗
- [ ] 版本与命令已记入笔记


## 24. 与上下游契约（扩）

| 上游 | Anubis | 下游 |
| --- | --- | --- |
| CDDIS/本地 RINEX | QC | 去留决策 |
| gfzrnx 输出 | QC | georinex/pytecgg/ppp |
| XTR | 不参与数值 TEC | 仅质控证据 |


## 25. 故障树（anubis）

```text
失败
 ├─ 安装/PATH → which / import / -h
 ├─ 输入文件 → head/file/gunzip -t/gtime
 ├─ 配置/旗标 → 与 -h 对照；回退金样配置
 ├─ 权限/磁盘 → ls -l / df -h
 ├─ 网络/鉴权 → 401/超时/证书
 └─ 算法窗/采样 → 与手册窗口定义核对
```


## 26. 日批与周报模板

```bash
#!/usr/bin/env bash
set -euo pipefail
DAY=$1
mkdir -p logs out/$DAY
# TODO: anubis 正式命令
echo "$DAY $(date -Is)" >> logs/anubis_batch_index.txt
```

周报字段：成功站日数、FAIL 列表、磁盘占用、上游版本。


## 27. 教学演示脚本（口述提纲）

1. 边界一句话  
2. 安装验收屏幕共享  
3. 跑通最小样例  
4. 故意弄坏一个输入并按坑表修  
5. 展示输出关键字  
6. 指向下一工具手册  


## 28. 性能与资源

| 项 | 建议 |
| --- | --- |
| CPU | 先单进程稳态，再并行 |
| 内存 | 1 Hz 全日警惕；先抽稀 |
| 磁盘 | 日志+产物预留 2× |
| 网络 | 产品下载失败要可离线重跑 |


## 29. 版本升级 checklist

1. 读上游 Release  
2. 备份金样配置  
3. 重装/替换二进制  
4. 跑最小回归  
5. diff `-h` 输出  
6. 更新自己的包装脚本  
7. 记版本号到 PROJECT 笔记  


## 30. 相关工具

见第 5 节与 [software README](./README.md)。参数冲突时：**本机帮助 > 上游 README > 本手册**。


## 31. 期望 I/O 对照表（站日级）

| 阶段 | 成功判据 | 失败样例 |
| --- | --- | --- |
| 安装 | `anubis -h` 有输出 | command not found |
| XML | `-X` 导出非空 | 空文件 |
| 运行 | xtr size>1k | cannot open |
| 抽查 | grep 到 Summary | 全空 grep |
| 门禁 | 笔记记录阈值结论 | 口头「好像行」 |

## 32. 批量结果汇总脚本骨架

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "station,logfile,fail_flag" > qc_summary.csv
for log in logs/anubis_*.log; do
  st=$(basename "$log" .log)
  if grep -q FAIL "$log"; then f=1; else f=0; fi
  echo "$st,$log,$f" >> qc_summary.csv
done
column -t -s, qc_summary.csv | head
```

## 33. 与 tutorials 的具体挂钩句

- 做 [16](../tutorials/16-practice-one-day-tec.md) 前：对本站日跑 lite，把 Summary 贴进实验笔记。
- 做 [20](../tutorials/20-storm-tec-analysis.md) 前：风暴日相关站 full，缺口表进附录。
- 做 [06](../tutorials/06-iono-positioning.md) 前：坏站别进 PPP。

## 34. 常见 XTR 误读

1. 把某一系统完好率低当成整站报废——先看任务是否需要该系统。  
2. 把高 MP 时段的 ROTI 峰当成「纯电离层」——可能是多路径。  
3. 抽样率变更后仍用旧阈值——抽稀会改变部分统计。  

## 35. 收尾检查

```bash
test -s qc/anubis_qc.xml.ok
ls *.xtr | head
grep -E 'Summary' *.xtr | head
echo ANUBIS_MANUAL_OK
```

## 36. 版本与引用

- 在论文/报告写明：Anubis Free 版本号、QC 模式、关键阈值。
- 引用与许可以官网为准。
- 本手册不替代 EULA。

## 37. 不要做的事（再强调）

- 不要把 XTR 数值当 TEC。
- 不要跳过 QC 直接发表 PPP/TEC。
- 不要混用 Pro 文档操作 Free。
- 不要在 CRLF XML 上浪费半天——先 dos2unix。

## 相关工具（复述）

[gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [README](./README.md)

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

