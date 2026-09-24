# GFZRNX

目录：[`PROJECTS.json` → `GFZRNX`](../../PROJECTS.json) · 产品页 <https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox> · 用户手册 <https://gnss.git-pages.gfz-potsdam.de/gfzrnx/> · 下载/许可 <https://gnss.gfz.de/services/gfzrnx>

> 操作手册。祈使句。面向电离层/GNSS 流水线的 **RINEX 预处理**。参数以本机 `gfzrnx -h` 与上游 Users Guide 为准（常见 2.2.x）。路径为占位符。可执行文件名因平台而异（`gfzrnx_lx` / `gfzrnx_osx` / `gfzrnx.exe`）；下文统一写 `gfzrnx`。
>
> **本 QC 环境未安装官方二进制**（须在 <https://gnss.gfz.de/services/gfzrnx> **登记下载**）。下文命令与 `-h` 节选来自 Users Guide / 已捕获帮助文本；装上后以本机 `gfzrnx -h` 覆盖。**不要编造本机统计数字。**

---

## 用途与边界

**用：**

- 检查、修复、版本转换（2↔3↔4）、拼接/切分、抽稀、系统/观测量筛选、头编辑、元数据提取、统计与表格化。
- 进 [georinex](./georinex.md) / [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md) 前：统一采样、系统、观测类型。
- 小时→日拼接；日→小时切分；1 Hz→30 s 抽稀；RINEX-2 短名→RINEX-3/4 长名。
- 给 [anubis](./anubis.md) / [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md) 喂干净 OBS。

**不用 / 边界：**

- **不算** STEC/vTEC/ROTI → 下游专用工具。
- **不做** 站网 QC PDF/图表主力 → [anubis](./anubis.md)（本工具偏格式/切片；`-stk_*` 仅辅助）。
- **不做** 实时 NTRIP → [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md)。
- **不做** PPP-AR → [pride-pppar](./pride-pppar.md)（但多日常**依赖**本工具）。
- 不是 TEQC 式交互 GUI——纯批处理 CLI。

**许可（必读）：** 科学伙伴许可常可科研/教学使用（须登记）；例行生产/商业常需收费许可。**以当前 EULA / 下载页为准。**

一句话：GFZRNX = **RINEX 手术刀**。

---

## 安装（多平台 + 报错）

### 前置

- 在下载页完成许可申请并取对应平台二进制。
- 无需自编译（闭源二进制）；需要可写临时目录。

### Linux

```bash
mkdir -p ~/bin ~/Downloads && cd ~/Downloads
# 实际包名以下载页为准
tar -xf gfzrnx_*.tar.gz 2>/dev/null || true
chmod +x gfzrnx_lx
mv gfzrnx_lx ~/bin/gfzrnx
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
gfzrnx -h | head -n 25
which gfzrnx
```

**期望：** 打印 `USAGE: gfzrnx` 及 `-finp`/`-fout`；`which` 指向 `~/bin/gfzrnx`。

### macOS

```bash
chmod +x gfzrnx_osx
mv gfzrnx_osx ~/bin/gfzrnx
# Gatekeeper：系统设置 → 仍要打开；或
xattr -d com.apple.quarantine ~/bin/gfzrnx 2>/dev/null || true
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
gfzrnx -h | head
```

### Windows

```bat
REM 将 gfzrnx.exe 放入 C:\Tools\gfzrnx\ 并加入用户 PATH
gfzrnx.exe -h
gfzrnx.exe -finp C:\data\XXXX0010.24o -fout C:\data_30\XXXX0010.24o -smp 30 -f
```

### 与 PRIDE 联用

PRIDE 多日常要求 PATH 中命令名恰为 `gfzrnx`（去掉 `_lx` 后缀）。

### 安装验收

| 检查 | 命令 | 通过 |
|---|---|---|
| 可执行 | `which gfzrnx` | 非空 |
| 帮助 | `gfzrnx -h` | 含 `-finp`/`-fout` |
| 写权限 | `touch out/.w` | 可写 |

| 现象 | 原因 | 修复 |
|---|---|---|
| `command not found` | 未改名/未入 PATH | `mv gfzrnx_lx ~/bin/gfzrnx` |
| 临时目录满 | 大拼接 | 清 `TMPDIR`；加 `-splice_direct` |
| 许可疑虑 | 业务化跑批 | 核对 EULA |

---

## 快速冒烟（5 分钟）

```bash
mkdir -p ~/iono_ops/{raw,work,out,log} && cd ~/iono_ops
# 准备一个非空 OBS 到 work/SITE0010.24o

gfzrnx -finp work/SITE0010.24o \
  -fout out/SITE0010_chk.24o \
  -chk -kv -f \
  -errlog log/SITE0010_chk.errlog

head -n 5 out/SITE0010_chk.24o
grep -E '^\S+.*(E|W|N) ' log/SITE0010_chk.errlog | head || head log/SITE0010_chk.errlog
gfzrnx -finp out/SITE0010_chk.24o -stk_obs | head -n 30
```

**期望：** 输出非空；头含 `OBSERVATION DATA`；errlog 无 `E` 级（`W` 需人工读）。

---

## 完整工作流

### 工作流 0：解压 / Hatanaka

GFZRNX **不是** Hatanaka 编解码器。

```bash
gunzip -k raw/SITE0010.24o.gz
CRX2RNX raw/SITE0010.24d - > work/SITE0010.24o
# 管道（STDIN 仅单文件）
crx2rnx raw/SITE0010.24d - | gfzrnx -fout work/SITE0010_chk.24o -chk -kv
```

### 工作流 A：检查 + 30 s 抽稀 + GPS 双频（TEC 常用）

```bash
gfzrnx -finp work/SITE0010.24o \
  -fout out/SITE0010_chk.24o -chk -kv -f -errlog log/chk.err

gfzrnx -finp out/SITE0010_chk.24o \
  -fout out/SITE0010_30s.24o -smp 30 -kv -f -errlog log/smp.err
# 需要平移 LLI：加 -smp_lli_shift

gfzrnx -finp out/SITE0010_30s.24o \
  -fout out/SITE0010_G_L1L2.24o \
  -satsys G -ot L1C,L2W,C1C,C2W -kv -f
# 真实信号名以头 SYS / # / OBS TYPES 为准——先 -stk_obs
```

**期望：** 体积↓；下游 `georinex` 读入后 `time` 间隔众数≈30 s；头观测类型仅所选。

### 工作流 B：小时文件拼日

```bash
# bash：a..x = 24 小时（RINEX-2）
gfzrnx -finp work/SITE001{a..x}.24o \
  -fout out/SITE0010.24o -kv -f -errlog log/splice.err
# 内存紧：
gfzrnx -finp work/SITE001{a..x}.24o -fout out/SITE0010.24o -kv -f -splice_direct
gfzrnx -finp out/SITE0010.24o -stk_epo 3600 | head
```

**期望：** 时长≈86400 s；`stk_epo` 约 24 行有数据。Windows cmd **不**展开 `{a..x}`——改用显式列表或 Git Bash/WSL。

### 工作流 C：RINEX-2 → RINEX-3 长名

```bash
gfzrnx -finp out/SITE0010_G_L1L2.24o -fout out/::RX3:: -vo 3 -f
# 仅 4 字符站名时补 monument/国家码：
gfzrnx -finp out/SITE0010_G_L1L2.24o -fout out/::RX3::00,CHN -vo 3 -sei in -f
# 批量 4→9：-4to9 four2nine.conf
```

**期望文件名示意：** `SITE00CHN_R_20240010000_01D_30S_GO.rnx`（真实字段随历元/时长变）。  
**警告：** `-sei in` 会丢掉文件名标称区间外的观测——先备份。

### 工作流 D：切分 / 统计 / 元数据 / 头编辑

```bash
# 1 小时片；fout 须 ::RX2:: 或 ::RX3::；n 为 60 倍数
gfzrnx -finp out/SITE0010.24o -fout out/::RX3::00,CHN -split 3600 -vo 3 -f

gfzrnx -finp out/SITE0010_30s.24o -stk_obs > log/stk_obs.txt
gfzrnx -finp out/SITE0010_30s.24o -stk_epo 3600 > log/stk_epo.txt
gfzrnx -finp out/SITE0010_30s.24o -meta basic:txt
gfzrnx -finp out/SITE0010_30s.24o -meta full:json > log/meta.json

# 头编辑（crux 语法见 Users Guide）
gfzrnx -finp out/SITE0010_30s.24o -fout out/SITE0010_hdr.24o \
  -crux work/site.crux -hded -kv -f
```

### 工作流 E：NAV 混合 / 比较 / 表格 / 批处理

```bash
gfzrnx -finp work/*_GN.rnx work/*_EN.rnx \
  -fout out/::RX3::00,CHN -nav_mixed -vo 3 -f
gfzrnx -finp brdc.rnx -fout out/brdc_latest.rnx -nav_latest -kv -f

gfzrnx -finp out/A.rnx out/B.rnx -fdiff   # 须同主版本
gfzrnx -finp out/SITE0010_30s.24o -tab -tab_sep "," > log/tab.csv

ls raw/*.24o | while read -r f; do
  b=$(basename "$f" .24o)
  gfzrnx -finp "$f" -fout "out/${b}_30s.24o" -smp 30 -chk -kv -f \
    -errlog "log/${b}.errlog" || echo "FAIL $b" >> log/fail.list
done
```

### 工作流 F：ROTI 链（禁止盲目抽稀）

```bash
# 保留 1 s（或更高）；只检查/修头
gfzrnx -finp work/SITE_1Hz.24o -fout out/SITE_1Hz_chk.24o -chk -kv -f -satsys G
# 然后交给 oasis-roti / ionomoni——不要先 -smp 30
```

### 工作流 G：PPP-AR 前处理

```bash
gfzrnx -finp work/SITE001{a..x}.24o -fout out/SITE0010.24o -kv -f -splice_direct
gfzrnx -finp out/SITE0010.24o -fout out/::RX3::00,CHN -vo 3 -sei in -f
# → anubis → pdp3
```

---

## 输入 / 输出与参数表

### 核心 I/O

| 参数 | 含义 | 注意 |
|---|---|---|
| `-finp` | 输入列表 | 多文件=拼接；STDIN 仅单文件 |
| `-fout` | 输出 | `::RX2::`/`::RX3::`/`::RX4::` 自动命名 |
| `-f` | 允许覆盖 | 默认不覆盖——忘记则「假成功」 |
| `-q` | 安静 | |
| `-errlog` | 日志文件 | 多次运行会追加；按任务分文件 |
| `-direct` | 逐历元直通 | 省内存、少统计 |

### 采样 / 时间

| 参数 | 含义 | 典型 |
|---|---|---|
| `-smp` | 抽稀秒 | TEC 常用 30；ROTI 勿滥用 |
| `-smp_lli_shift` | 抽稀平移 LLI | 相位敏感场景 |
| `-d` / `--duration` | 标称时长秒 | 86400 / 3600 |
| `-epo_beg` | 首历元 | `2014-04-06_12:30:00` 等 |
| `-sei in\|out` | 严格按文件名区间 | 名义改名；会裁数据 |
| `-split n` | 按 n 秒切 | n=60 倍数 |

### 系统与观测

| 参数 | 含义 | 取值 |
|---|---|---|
| `-satsys` | 系统 | `G`/`E`/`C`/`R`/`J`/`I`/`S` 子集 |
| `-ot` | 观测类型 | `L1C,L2W` 或 `G:L1C,L2W+E:…` |
| `-prn` / `-no_prn` | 白/黑名单 | `G1-32,E14` |
| `-kaot` | 保留空类型 | 调试 |
| `-rsot n` | 删稀疏类型 | 相对中位数阈值 |

### 版本 / 命名 / 统计

| 参数 | 含义 |
|---|---|
| `-vo` / `-vosc` | 主版本 / 标准符合输出（2\|3\|4） |
| `-kv` | 保持输入主版本 |
| `-site` / `-4to9` / `-ant_rename` | 站名与天线规范化 |
| `-stk_obs` / `-stk_epo` / `-stk_only` | 统计与可用性图 |
| `-meta type[:fmt]` | `basic\|full` × `json\|xml\|txt\|dump` |
| `-fdiff` / `-tab` | 比较 / 表格化 |
| `-nav_mixed` / `-nav_latest` | NAV 处理 |

### 日志列

| 列 | 含义 |
|---|---|
| C | N=Notice / W=Warning / E=Error |
| MESSAGE | 说明 |

### 输出主版本默认（以上游为准）

2→2.11，3→3.05，4→4.01。

### 文件名速查

| 风格 | 例 |
|---|---|
| R2 日 | `pots0070.15o` |
| R2 小时 | `pots007a.15o` |
| R3 | `POTS00DEU_R_20150070000_01D_30S_MO.rnx` |

---

## 接到 tutorials / 工作流哪一步

| 场景 | 本手册 | 下游 |
|---|---|---|
| 一日 TEC | A | georinex → [pytecgg](./pytecgg.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| ROTI / 磁暴 | F | [oasis-roti](./oasis-roti.md) · [05](../tutorials/05-scintillation-roti.md) / [20](../tutorials/20-storm-tec-analysis.md) |
| PPP-AR | G | [anubis](./anubis.md) → [pride-pppar](./pride-pppar.md) · [06](../tutorials/06-iono-positioning.md) |
| 读数组 | 清洗后 | [georinex](./georinex.md) |
| GIM 对照前 | A 保证双频 | [ionex-gim](./ionex-gim.md) |

---

## 可操作坑（现象 → 原因 → 修复）

1. **输出没更新却以为成功**  
   原因：忘记 `-f`，已存在文件未覆盖。  
   修复：查时间戳；统一加 `-f`。

2. **Windows 通配无文件**  
   原因：cmd 不展开 `{a..x}`。  
   修复：WSL/Git Bash；或显式文件列表。

3. **管道拼接失败**  
   原因：STDIN 只支持单文件。  
   修复：`-finp f1 f2 …`。

4. **改名后数据变短**  
   原因：`-sei in` 按文件名裁剪。  
   修复：备份原文件；确认标称区间。

5. **ROTI 结果糊成一片**  
   原因：先 `-smp 30` 毁掉高频。  
   修复：ROTI 链只用 `-chk`，不抽稀。

6. **`-ot` 后相位空**  
   原因：站上是 `L2X` 却写 `L2W`。  
   修复：先 `-stk_obs` / 读头 OBS TYPES。

7. **拼接 OOM**  
   原因：24×1 Hz + 默认统计。  
   修复：`-splice_direct`；或先抽稀再拼。

8. **`.YYd` 解析失败**  
   原因：Hatanaka 未转。  
   修复：`CRX2RNX`。

9. **自动命名怪站名**  
   原因：缺 MARKER。  
   修复：`-site` 或 `-crux`。

10. **PRIDE 找不到 gfzrnx**  
    原因：仍叫 `gfzrnx_lx`。  
    修复：改名并入 PATH。

11. **`-fdiff` 报错**  
    原因：主版本不同。  
    修复：先都 `-vo 3`。

12. **errlog 混在一起**  
    原因：追加同一文件。  
    修复：按任务名分 log。

13. **业务化跑批许可风险**  
    原因：科学许可范围。  
    修复：上线前读 EULA。

14. **LLI 抽稀后异常**  
    原因：标志未随采样移动。  
    修复：试 `-smp_lli_shift`。

15. **国家码 XXX 归档乱**  
    原因：占位 ISO。  
    修复：改真实三字母。

16. **下游脚本只认短名**  
    原因：突然改 R3 长名。  
    修复：统一命名策略或保留短名副本。

---

## 同类选型

| 需求 | 优先 | 勿选 |
|---|---|---|
| 格式/拼接/抽稀 | **GFZRNX** | 手写 Python 解析当生产 |
| 读入 xarray | georinex | GFZRNX（不算 TEC） |
| QC 报表 | anubis | 仅靠 `-stk_*` 交差 |
| PPP-AR | pride-pppar | GFZRNX |
| 实时流 | pygnssutils/BNC | GFZRNX |

---

## 操作检查清单

1. `gfzrnx -h` 可用；已改名为 `gfzrnx`。  
2. 输入已解压且非误喂 Hatanaka。  
3. 明确步骤：检查 / 抽稀 / 拼接 / 改名。  
4. TEC vs ROTI 抽稀策略已分支。  
5. errlog 按任务隔离；无未处理 `E`。  
6. `ls -l out/` 与 `-stk_obs` 过眼。  
7. 下游试读 1 文件再批量。  
8. 冲突时：**本机 `-h` > 上游手册 > 本文**。

---

## 附录 · 命令一页纸

```bash
gfzrnx -h
gfzrnx -finp IN -fout OUT -chk -kv -f
gfzrnx -finp IN -fout OUT -smp 30 -kv -f
gfzrnx -finp H1 H2 ... -fout DAY -kv -f -splice_direct
gfzrnx -finp IN -fout DIR/::RX3::00,CHN -vo 3 -sei in -f
gfzrnx -finp IN -fout OUT -satsys G -ot L1C,L2W,C1C,C2W -kv -f
gfzrnx -finp IN -stk_obs
gfzrnx -finp IN -stk_epo 3600
gfzrnx -finp IN -meta full:json
gfzrnx -finp IN -fout DIR/::RX3::00,CHN -split 3600 -vo 3 -f
```

---

## 相关

[README](./README.md) · [georinex](./georinex.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [pride-pppar](./pride-pppar.md) · [oasis-roti](./oasis-roti.md) · [rtklib](./rtklib.md) · [data-access](../data-access.md) · 教程 [16](../tutorials/16-practice-one-day-tec.md) · [02](../tutorials/02-gnss-dualfreq-tec.md)
