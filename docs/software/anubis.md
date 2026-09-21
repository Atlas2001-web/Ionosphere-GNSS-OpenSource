# Anubis

目录：[`PROJECTS.json` → `Anubis`](../../PROJECTS.json) · 官网 <https://gnutsoftware.com/software/anubis/> · 配置说明 <https://www.pecny.cz/gop/index.php/gnss/70-gnss-software/221-anubis-configuration> · 下载 <https://gnutsoftware.com/software/anubis/download> · Free 常见 GPL-3；Pro/RT 商业

> 操作手册。祈使句。本页只讲 **Anubis Free**（Linux 预编译常见）。键名以本机 `anubis -h` / `anubis -X` 与官方配置页为准。输出是 QC 报表，不是 TEC，不是定位解。

---

## 用途与边界

**用：**

- 对 RINEX 观测做 **QC**：完整性、缺口、多路径、SNR、周跳迹象、系统可用性。
- 产出可 `grep` 的 **XTR** 与结构化 **XML**。
- 数据中心日检、站网健康、TEC / ROTI / PPP **前门禁**。
- 论文「数据质量」附录材料。

**不用 / 边界：**

- **不做** 拼接 / 抽稀 / 改 RINEX → 先 [gfzrnx](./gfzrnx.md)（顺序：GFZRNX → Anubis → 科学软件）。
- **不做** 校准 TEC → [pytecgg](./pytecgg.md)（作者 **viventriglia**）。
- **不做** ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。
- **不做** 精密定位 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)。
- Free **没有** Pro 的实时流 / 高级编辑 / JSON 高等级功能——勿抄 Pro 文档操作 Free。

一句话：Anubis = **体检站**；QC 通过 ≠ 绝对 TEC 正确。

---

## 安装（多平台 + 报错）

### Linux（主线）

1. 打开下载页（可能需注册），取 **Free / Linux** 预编译或源码。  
2. 解压，`chmod +x anubis`，放入 `~/bin` 或 `/usr/local/bin`。  
3. 冒烟：

```bash
mkdir -p ~/bin
# 假设下载后文件名为 anubis
chmod +x anubis && mv anubis ~/bin/
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
anubis -h | head -n 40
anubis -V 2>/dev/null || true
anubis -X | head -n 60
```

**期望：** `-h` 含 `-x`/`-X`；`-X` 打出默认 XML（含 `gen`/`inp`/`out`/`qc` 等节点示意）。

### macOS / Windows

- Free 官方主推 Linux；其它平台用 **WSL2** 或按官网当前包。  
- XML 一律 **LF**；从 Windows 拷来的配置先 `dos2unix`。

### 安装期常见报错

| 现象 | 原因 | 修复 |
|---|---|---|
| `anubis: command not found` | PATH / 未 chmod | `which anubis`；`chmod +x` |
| 缺 `.so` | 动态库 | 用官网预编译；或按 README 装依赖 |
| `-X` 空或秒退 | 坏包 / 无执行位 | 重新下载；检查架构 x86_64 |
| XML 解析怪 | CRLF | `dos2unix qc/*.xml` |
| 文档键在 Free 不存在 | 抄了 Pro | 只信本机 `-X` 与 Free 说明 |

### 安装验收

```bash
test -x "$(command -v anubis)"
anubis -X > /tmp/anubis_default.xml
test -s /tmp/anubis_default.xml
wc -l /tmp/anubis_default.xml
```

---

## 快速冒烟（10 分钟）

```bash
mkdir -p qc logs out_qc
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok

# 用编辑器改 <inp> 的 OBS/NAV、<out> 的 xtr/xml 为绝对路径
# 或下一节用 CLI 覆盖，少改 XML

anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/abs/data/SITE0010.24o \
  :inp:rinexn=/abs/data/brdc0010.24n \
  :out:xtr=/abs/out_qc/SITE0010.xtr \
  :out:log=/abs/logs/anubis_SITE0010.log \
  2>&1 | tee logs/anubis_smoke.log

ls -la out_qc/SITE0010.xtr logs/anubis_SITE0010.log
grep -E 'Summary|Completeness|MP|gap|SNR|MPTH' out_qc/SITE0010.xtr | head -n 40
```

**期望：** `.xtr` 非空（通常 ≫1 KB）；能 `grep` 到 Summary / Completeness 类关键字（字样随版本）。  
**失败：** `cannot open` → 路径；空 xtr → OBS 坏或时间窗为空。

等价启动形式（以上游为准）：

```bash
anubis -x qc/anubis_qc.xml
anubis < qc/anubis_qc.xml
cat qc/anubis_qc.xml | anubis
```

---

## 完整工作流

### 工作流 A：金样 XML → 单站 lite 日检 → 门禁结论

```bash
# A1 导出并冻结金样
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok

# A2 在 XML 里设 qc 模式为 lite（键名以 -X 为准；常见为 qc 段 verbosity / 模式开关）
# 策略：全网 lite；问题站再 full

# A3 跑站日
SITE=SITE0010
OBS=/data/${SITE}.24o
NAV=/data/brdc0010.24n
anubis -x qc/anubis_qc.xml \
  :inp:rinexo="$OBS" \
  :inp:rinexn="$NAV" \
  :out:xtr=/data/qc/${SITE}.xtr \
  :out:xml=/data/qc/${SITE}_qc.xml \
  :out:log=/data/logs/anubis_${SITE}.log \
  2>&1 | tee logs/anubis_${SITE}.console

# A4 抽查
grep -E 'Summary|Completeness|MPTH|MP |gap|SNR' /data/qc/${SITE}.xtr | head -n 60
wc -c /data/qc/${SITE}.xtr
```

**门禁（项目自定义，非官方）：** 完好率过低 / MP 极端 / 事件窗长缺口 → **丢弃站日**，不要进 pytecgg / pdp3。把阈值写进协议。

### 工作流 B：thin → lite → full 阶梯

| 模式 | 用途 | NAV | 耗时 |
|---|---|---|---|
| thin | 头/元数据快扫 | 可选 | 短 |
| lite | 定量 QC、缺口/完整性日检 | 建议有 | 中 |
| full | 定性/综合定量 | 通常需要 | 长 |

```bash
# 全网：lite
for f in /data/rinex/*.rnx; do
  b=$(basename "$f" .rnx)
  anubis -x qc/anubis_lite.xml :inp:rinexo="$f" :inp:rinexn=/data/BRDC.rnx \
    :out:xtr=/data/qc/${b}.xtr :out:log=/data/logs/${b}.log \
    2>&1 | tee -a logs/batch_console.log || echo "FAIL $f" | tee -a logs/fail.list
done

# 问题站：改用 full 配置金样再跑
anubis -x qc/anubis_full.xml :inp:rinexo=/data/BAD.rnx :inp:rinexn=/data/BRDC.rnx \
  :out:xtr=/data/qc/BAD_full.xtr
```

### 工作流 C：与 GFZRNX 联用（清洗后再 QC）

```bash
gfzrnx -finp /data/raw.24o -fout /data/SITE_30s.24o -smp 30 -chk -kv -f \
  -errlog logs/gfzrnx_SITE.err
anubis -x qc/anubis_qc.xml \
  :inp:rinexo=/data/SITE_30s.24o \
  :inp:rinexn=/data/BRDC.rnx \
  :out:xtr=/data/qc/SITE_30s.xtr
# 抽稀后部分统计会变——阈值勿照搬 1 Hz 旧标准
```

### 工作流 D：与 georinex 交叉验缺口

```bash
python -m georinex.gtime /data/SITE0010.24o | tee logs/gtime_SITE.txt
# 对齐时间窗后，再解释 XTR 里的 gap 段
grep -i gap /data/qc/SITE0010.xtr | head
```

### 工作流 E：批量汇总 CSV

```bash
echo "station,xtr_bytes,has_summary,fail_log" > qc_summary.csv
for xtr in /data/qc/*.xtr; do
  st=$(basename "$xtr" .xtr)
  sz=$(wc -c < "$xtr")
  hs=$(grep -c -E 'Summary|Completeness' "$xtr" || true)
  fl=0
  grep -q FAIL "logs/anubis_${st}.log" 2>/dev/null && fl=1 || true
  echo "$st,$sz,$hs,$fl" >> qc_summary.csv
done
column -t -s, qc_summary.csv | head
```

### 工作流 F：进 TEC / PPP 前的一页结论

```text
站日: SITE 2024/001
模式: lite
Completeness: ...（从 XTR 抄）
MP 备注: ...
缺口: 无 / 有（UTC 时段）
门禁: PASS → pytecgg 或 pdp3
      FAIL → 换站或修数据
```

---

## 输入 / 输出与字段表

### CLI（本机 `-h` 为准）

| 项 | 含义 |
|---|---|
| `-h` / `--help` | 帮助 |
| `-V` | 版本（若提供） |
| `-X` | 默认配置打到 stdout |
| `-x file` | 按 XML 运行 |
| `-z file` | 写出配置（若提供） |
| `:inp:rinexo=路径` | 覆盖 OBS |
| `:inp:rinexn=路径` | 覆盖 NAV |
| `:out:xtr=路径` | XTR 输出 |
| `:out:xml=路径` | XML QC 输出 |
| `:out:log=路径` | 日志 |
| `:out:verb=N` | 日志详细度 |
| `:qc:…` | 覆盖 QC 段属性（键以 `-X` 为准） |

常见长选项别名（教程 PDF，以二进制为准）：`--rinexo`=`:inp:rinexo`，`--xtr`=`:out:xtr`。

### XML 主结构

| 段 | 作用 |
|---|---|
| `gen` | 时间窗、星座、采样、站点列表 |
| `sys` / `gnss` | 系统/观测类型过滤 |
| `nav` | 导航数据处理 |
| `inp` | `rinexo` / `rinexn`（必填类） |
| `out` | `xtr` / `xml` / `log` |
| `qc` | 模式与各段 verbosity |
| `site` | 站元数据（若用） |

星座三字母常见：`GPS` `GLO` `GAL` `BDS` `SBS` `QZS`（以配置页为准）。

### 输入文件

| 类型 | Free 注意 |
|---|---|
| RINEX OBS 2/3 | 主输入；4 看版本 |
| RINEX NAV | full/定性建议提供；lite 也建议带 |
| `.gz` | Free≥2.1 常可读 gzip；Hatanaka 多在 Pro——Free 先 `CRX2RNX` |

### 输出

| 类型 | 内容 |
|---|---|
| XTR | 主报表：分节、可 grep；含完好率/MP/SNR/gap 等 |
| XML | 标准 QC 摘要交换 |
| log | 进度与错误 |

### XTR 常搜关键字

`Summary`、`Completeness`、`gap`、`MP` / `MPTH`、`SNR`、`slip` / `cs`（字样随版本）。先 `grep -n` 再读上下文。

### 明确不输出

STEC、ROTI、`.pos`、IONEX、校准 `veq`。

---

## 接到 tutorials / 工作流哪一步

| 场景 | 本手册 | 下游 |
|---|---|---|
| 路径 A TEC | 工作流 A/F | [pytecgg](./pytecgg.md) · 教程 [16](../tutorials/16-practice-one-day-tec.md) |
| 路径 B 扰动 | 事件日前 full | [oasis-roti](./oasis-roti.md) · [20](../tutorials/20-storm-tec-analysis.md) |
| 路径 D 坐标 | 坏站剔除 | [pride-pppar](./pride-pppar.md) · [06](../tutorials/06-iono-positioning.md) |
| 清洗后复检 | 工作流 C | 确认 gfzrnx 未切坏 |
| 索引 | — | [README](./README.md) |

---

## 可操作坑（现象 → 原因 → 修复）

1. **`cannot open` / 找不到输入**  
   原因：相对路径、cwd 不对。  
   修复：全部改绝对路径；或 `cd` 到约定目录再跑。

2. **空 xtr / 几乎无 Summary**  
   原因：OBS 损坏、时间窗为空、过滤过严。  
   修复：`head`/`georinex.gtime`；放宽 `gen` 时间；回滚金样 XML。

3. **XML 解析失败**  
   原因：CRLF、手工改坏标签。  
   修复：`dos2unix`；`cp qc/anubis_qc.xml.ok qc/anubis_qc.xml`。

4. **把 Anubis 当拼接工具**  
   原因：边界混淆。  
   修复：改文件用 [gfzrnx](./gfzrnx.md)。

5. **Free 上使用 Pro 键（json/实时/编辑）**  
   原因：文档档位混用。  
   修复：只保留 `-X` 里存在的键。

6. **QC 通过就当绝对 TEC 正确**  
   原因：误解门禁。  
   修复：Anubis 只决定去留；绝对值走 pytecgg。

7. **批量忽略 FAIL**  
   原因：无汇总。  
   修复：工作流 E；`grep FAIL logs/`。

8. **缺 NAV 跑 full**  
   原因：定性 QC 需要星历。  
   修复：补 BRDC；或先 lite。

9. **Hatanaka `.YYd` 直接喂 Free**  
   原因：Free 对 crx 支持有限。  
   修复：`CRX2RNX` 后再 QC。

10. **1 Hz 与 30 s 共用同一完好率阈值**  
    原因：抽稀改变统计。  
    修复：按采样分阈值表。

11. **只看终端不看 XTR**  
    原因：摘要不全。  
    修复：强制 `grep Summary` 入笔记。

12. **输出覆盖未分站日**  
    原因：同名 xtr 互踩。  
    修复：`out/qc/YYYY/DDD/SITE.xtr`。

13. **与 georinex 缺口对不上**  
    原因：时间窗/系统过滤不一致。  
    修复：先对齐窗与系统再比。

14. **高 MP 时段的 ROTI 峰全算电离层**  
    原因：环境多路径。  
    修复：XTR MP 节与 ROTI 同时引用。

15. **只读目录写不出**  
    原因：`:out:` 无写权限。  
   修复：改到可写盘；`df -h`。

16. **键名抄旧教程**  
    原因：版本演进。  
    修复：每次 `anubis -X` diff 金样。

---

## 同类选型

| 需求 | 选 |
|---|---|
| QC 报表 XTR/XML | **Anubis Free** |
| 改/拼/抽稀 RINEX | gfzrnx |
| Python 读盘 | georinex |
| 实时流 QC | Anubis Pro/RT 或其它链 |
| 科学 TEC/ROTI | pytecgg / oasis / ionomoni |

---

## 操作检查清单

1. `anubis -h` / `-X` 可用；金样 `.ok` 已存。  
2. OBS/NAV 路径绝对；gzip 完整。  
3. 模式选定 thin/lite/full。  
4. xtr `wc -c` 合理；grep 到 Summary。  
5. 门禁结论写入笔记（PASS/FAIL + 理由）。  
6. FAIL 站不进 PPP/TEC。  
7. 版本号与命令行记入实验记录。  
8. 冲突时：**本机 `-h`/`-X` > 上游页 > 本手册**。

---

## 附录 · 命令一页纸

```bash
anubis -h
anubis -X > qc/anubis_qc.xml
cp qc/anubis_qc.xml qc/anubis_qc.xml.ok
anubis -x qc/anubis_qc.xml :inp:rinexo=/ABS/OBS :inp:rinexn=/ABS/NAV :out:xtr=/ABS/OUT.xtr
grep -E 'Summary|Completeness|MP|gap|SNR' /ABS/OUT.xtr | head
```

---

## 相关

[README](./README.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)
