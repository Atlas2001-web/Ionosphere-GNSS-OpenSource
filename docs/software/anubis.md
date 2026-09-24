# Anubis · GNSS 观测 QC（Free）操作手册

目录：[`PROJECTS.json` → `Anubis`](../../PROJECTS.json) · 官网 <https://gnutsoftware.com/software/anubis/> · 配置 <https://www.pecny.cz/gop/index.php/gnss/70-gnss-software/221-anubis-configuration> · 手册 PDF <https://gnutsoftware.com/themes/gnut/assets/files/anubis_manual.pdf> · 下载 <https://gnutsoftware.com/software/anubis/download> · Free 常见 GPL；**Pro/RT 商业，本页不写**

> 祈使句。只讲 **Anubis Free**（官网常见标称 **2.3**，Linux 预编译）。输出是 QC 报表，不是 TEC，不是定位解。

**质检机说明（Round6，2026-09-24 ET）：** 官网 Free 下载**需注册**；本机未拿到官方 Linux 二进制（社区 Windows `Anubis.exe` 为 32-bit PE，wine32 不可用；旧 2.2 源码 Linux 编译未链上 gzstream）。下列 CLI/XML/XTR **以官方 PDF Free 段、pecny 配置页、社区样例 `conf.cfg` 为准**，**不伪造**本机 `anubis` stdout。装上二进制后一律以本机 `anubis -h` / `-X` 覆盖本文。

## 1. 用途与边界

**做：**

- RINEX 观测 **QC**：完好率、缺口、多路径、SNR、周跳迹象、系统可用性
- 产出可 `grep` 的 **XTR** 与结构化 **XML**
- 站网日检、TEC / ROTI / PPP **前门禁**

**不做：**

- 拼接 / 抽稀 / 改 RINEX → [gfzrnx](./gfzrnx.md)（GFZRNX 需上游注册；勿臆造其 stdout）
- 校准 TEC → [pytecgg](./pytecgg.md)（作者 **viventriglia**）
- ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
- 精密定位 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- Free **无** Pro 的 Hatanaka 编解码主力、JSON 高档、实时流 / 编辑——勿抄 Pro 文档操作 Free

一句话：Anubis = **体检站**；QC 通过 ≠ 绝对 TEC 正确。

## 2. 安装

```bash
# 1) 打开下载页，注册后取 Free / Linux 预编译（或源码）
# 2) 解压，chmod，入 PATH
mkdir -p ~/bin
chmod +x anubis && mv anubis ~/bin/
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc

anubis -h | head -n 40
anubis -V 2>/dev/null || true
anubis -X | head -n 60   # 默认 XML → stdout
```

**期望（官方/`pecny`）：** `-h` 含 `-x`/`-X`；`-X` 打出默认配置（`gen`/`inp`/`out`/`qc` 等）。  
macOS/Windows Free 常另附条件 → **WSL2** 或按下载页。XML 一律 **LF**（`dos2unix`）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `command not found` | PATH / 未 chmod | `which anubis`；`chmod +x` |
| 缺 `.so` | 动态库 | 换官网静态/匹配发行版预编译 |
| `-X` 空或秒退 | 坏包 / 错架构 | 重下；确认 x86_64 |
| 文档键在 Free 不存在 | 抄了 Pro | 只信本机 `-X` |

```bash
test -x "$(command -v anubis)"
anubis -X > /tmp/anubis_default.xml && test -s /tmp/anubis_default.xml
```

## 3. 端到端（装上 Free 后照跑）

### 3.1 金样 XML → lite 日检

官方等价启动：`anubis -x cfg.xml` 或 `anubis < cfg.xml`。CLI 覆盖 XML（pecny）：

```text
:elem:subelem val          # 设元素值，如 :inp:rinexo
:elem:attribute=val        # 设属性，如 :out:verb=1
```

```bash
mkdir -p qc logs out_qc
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok

# 路径一律绝对；OBS/NAV 换成你的站日
anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/ABS/data/SITE0010.24o \
  :inp:rinexn=/ABS/data/brdc0010.24n \
  :out:xtr=/ABS/out_qc/SITE0010.xtr \
  :out:xml=/ABS/out_qc/SITE0010_qc.xml \
  :out:log=/ABS/logs/anubis_SITE0010.log \
  2>&1 | tee logs/anubis_smoke.log

ls -la out_qc/SITE0010.xtr
grep -E 'TOTSUM|Summary|Completeness|GAPLST|MPTH|=GPSM|=GPSSUM' out_qc/SITE0010.xtr | head -n 40
```

**期望：** `.xtr` 非空（通常 ≫1 KB）；能 `grep` 到 `=TOTSUM` / 分系统 `=GPSSUM` 等（字样随版本）。  
**失败：** `cannot open` → 路径；空 xtr → OBS 坏或时间窗为空。

### 3.2 模式阶梯（官方预置；Free 可用 QC）

| 预置 | 用途 | NAV |
| --- | --- | --- |
| `--thin` | 头/元数据快扫 | 可选 |
| `--lite` | 定量 QC、缺口/完好率 | 建议有 |
| `--full` | 定性+综合定量 | 通常需要 |
| `--summ` | 摘要向 XML | 建议有 |

```bash
# 全网 lite；问题站再 full（旗标名以本机 -h 为准）
anubis --lite -x qc/anubis_lite.xml \
  :inp:rinexo=/ABS/SITE.rnx :inp:rinexn=/ABS/BRDC.rnx \
  :out:xtr=/ABS/qc/SITE.xtr :out:log=/ABS/logs/SITE.log
```

### 3.3 GFZRNX 清洗后再 QC

```bash
# gfzrnx：上游需注册；此处不贴臆造 stdout —— 见 gfzrnx.md
# 抽稀后完好率阈值勿照搬 1 Hz
anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/ABS/SITE_30s.24o :inp:rinexn=/ABS/BRDC.rnx \
  :out:xtr=/ABS/qc/SITE_30s.xtr
```

### 3.4 批量汇总

```bash
echo "station,xtr_bytes,has_totsum" > qc_summary.csv
for xtr in /ABS/qc/*.xtr; do
  st=$(basename "$xtr" .xtr)
  sz=$(wc -c < "$xtr")
  hs=$(grep -c '=TOTSUM\|Summary' "$xtr" || true)
  echo "$st,$sz,$hs" >> qc_summary.csv
done
```

### 3.5 门禁一页纸（项目自定，非官方）

```text
站日: SITE YYYY/DDD | 模式: lite
=TOTSUM %Ratio / %Rt>10: …（从 XTR 抄）
缺口 GAPLST: 无 / 有（UTC）
MP 备注: …
门禁: PASS → pytecgg / pdp3 | FAIL → 换站或修数据
```

## 4. 输入 / 输出与字段

### CLI（官方 PDF / pecny；以本机 `-h` 为准）

| 项 | 含义 |
| --- | --- |
| `-h` / `--help` | 帮助 |
| `-V` | 版本 |
| `-X` | 默认配置 → stdout |
| `-x file` | 按 XML 运行 |
| `-z file` | 写出最终配置（若提供） |
| `--thin` / `--lite` / `--full` / `--summ` | 模式预置 |
| `:inp:rinexo=` / `:inp:rinexn=` | 覆盖 OBS/NAV |
| `:out:xtr=` / `:out:xml=` / `:out:log=` | 输出 |
| `:out:verb=N` | 日志详细度 |
| `:qc:sec_*=` | 各 XTR 段 verbosity |

### XML 主段

| 段 | 作用 |
| --- | --- |
| `gen` | 时间窗、星座、采样、`rec` 站列表 |
| `sys` / `gnss` | 系统/观测过滤 |
| `inp` | `rinexo` / `rinexn`（必填类） |
| `out` | `xtr` / `xml` / `log` |
| `qc` | `sec_sum`/`sec_gap`/`sec_mpx`… |
| `site` | 站元数据（可选） |

星座三字母常见：`GPS` `GLO` `GAL` `BDS` `SBS` `QZS`（以配置页为准）。

### 社区样例片段（`conf.cfg` 结构示意；路径需改）

```xml
<gen>
  <beg> "2019-01-01 00:00:00" </beg>
  <end> "2019-01-01 23:59:30" </end>
  <sys> GPS GLO GAL BDS SBS QZS </sys>
  <int> 30 </int>
</gen>
<inputs>
  <rinexo> SITE.19o </rinexo>
  <rinexn> SITE.19n </rinexn>
</inputs>
<outputs>
  <xtr> SITE.xtr </xtr>
  <xml> SITE.xqc </xml>
  <log> anubis.log </log>
</outputs>
```

### XTR 常搜关键字（官方 PDF 示例）

`=TOTSUM`、`=GPSSUM`/`=GALSUM`…、`GAPLST`/`PCSLST`、`=GPSM1C`（MP）、`RNXHDR`、`CLKJMP`。先 `grep -n` 再读上下文。

**不输出：** STEC、ROTI、`.pos`、IONEX、校准 `veq`。Free 对 **Hatanaka `.YYd`** 支持有限 → 先 `CRX2RNX`。`.gz` 在 Free≥2.1 常可读。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 A TEC | §3.1 / 3.5 | [pytecgg](./pytecgg.md) · 教程 [16](../tutorials/16-practice-one-day-tec.md) |
| 路径 B 扰动 | 事件日前 full | [oasis-roti](./oasis-roti.md) · [20](../tutorials/20-storm-tec-analysis.md) |
| 路径 D 坐标 | 坏站剔除 | [pride-pppar](./pride-pppar.md) · [06](../tutorials/06-iono-positioning.md) |
| 清洗后复检 | §3.3 | [gfzrnx](./gfzrnx.md) |
| 索引 | — | [README](./README.md) |

## 6. 坑（≥8）

1. **`cannot open`** — 相对路径/cwd → 绝对路径。  
2. **空 xtr / 无 `=TOTSUM`** — OBS 坏、时间窗空、过滤过严 → `head`/`georinex.gtime`；回滚 `.ok`。  
3. **XML 解析怪** — CRLF / 改坏标签 → `dos2unix`；`cp …xml.ok`。  
4. **当拼接工具用** — 改文件用 gfzrnx。  
5. **Free 上用 Pro 键（json/实时/编辑）** — 只留 `-X` 里有的键。  
6. **QC 通过当绝对 TEC** — Anubis 只决定去留。  
7. **批量忽略 FAIL** — 做 §3.4 汇总。  
8. **缺 NAV 跑 full** — 补 BRDC 或先 lite。  
9. **Hatanaka 直接喂 Free** — `CRX2RNX`。  
10. **1 Hz 与 30 s 共用完好率阈值** — 按采样分表。  
11. **高 MP 时段 ROTI 峰全算电离层** — XTR MP 与 ROTI 同引。  
12. **键名抄旧教程** — 每次 `anubis -X` diff 金样。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| QC 报表 XTR/XML | **Anubis Free** |
| 改/拼/抽稀 RINEX | gfzrnx |
| Python 读盘 | georinex |
| 实时流 QC | Anubis Pro/RT 或其它链 |
| TEC/ROTI | pytecgg / oasis / ionomoni |

## 8. 检查清单

1. 本机 `anubis -h`/`-X` 可用；金样 `.ok` 已存。  
2. OBS/NAV 绝对路径；gzip 完整。  
3. 模式 thin/lite/full 已选。  
4. xtr `wc -c` 合理；grep 到 `=TOTSUM`。  
5. 门禁写入笔记；FAIL 不进 PPP/TEC。  
6. 冲突时：**本机 `-h`/`-X` > 官方 PDF > 本手册**。

## 相关

[README](./README.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · 教程 [16](../tutorials/16-practice-one-day-tec.md) · [09](../tutorials/09-dcb-biases-deep.md)
