# RTKLIB

目录：[`PROJECTS.json` → `RTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/tomojitakasu/RTKLIB> · 常用维护分支 <https://github.com/rtklibexplorer/RTKLIB>（demo5 / explorer）

> 操作手册。祈使句。**模式号 `-p`、解状态 Q 值以你编译的二进制 `-h` / 手册为准**——原版与 explorer 有差异。

---

## 用途与边界

**用：**

- 开源 **SPP / DGPS / RTK / 静态 / 运动学 / 浮点 PPP**（库 + GUI + CLI）。
- 主产品：**坐标时间序列**（`.pos`）与相关统计。
- 事后：`rnx2rtkp`；原始日志转 RINEX：`convbin`；流转发：`str2str`；实时：`rtkrcv`。
- 评估电离层扰动对**固定率 / 残差**的影响（对照 ROTI 高值时段）。

**不用 / 边界：**

- **不是** STEC/VTEC/ROTI 产品引擎 → [pytecgg](./pytecgg.md)（viventriglia）、[oasis-roti](./oasis-roti.md)、[ionomoni](./ionomoni.md)。
- **不是** 发表级 PPP-AR 首选 → [pride-pppar](./pride-pppar.md)。
- **不是** NTRIP 多流录盘主力 → [bnc](./bnc.md)；脚本单流 → [pygnssutils](./pygnssutils.md)。
- 电离层在 RTKLIB 里是**改正模型或误差源**，不是科研 GIM。SH-GIM 边界见 [sh-gim](./sh-gim.md)。

一句话：RTKLIB = **定位与流工具箱**；要 TEC 图请换链。

---

## 安装（多平台 + 报错）

### Windows

1. 从 tomojitakasu 或 rtklibexplorer **Releases** 取预编译 zip。  
2. 解压，把 `bin`（或含 `rnx2rtkp.exe` 的目录）加入用户 `PATH`。  
3. 新开 cmd：

```bat
rnx2rtkp -h
convbin -h
str2str -h
```

### Linux（explorer / demo5 源码示例）

```bash
sudo apt update
sudo apt install -y build-essential git make gcc g++
git clone https://github.com/rtklibexplorer/RTKLIB.git
cd RTKLIB
# 按该仓库当前 README 进入 app/ 或对应目录 make
# 示意（路径随分支变化，以 README 为准）：
# cd app/consis && make
# 或官方文档写明的 cmake/make 流程
export PATH="$PWD/bin:$PATH"   # 按实际产出目录改
hash -r
rnx2rtkp -h | head
convbin -h | head
```

### macOS

```bash
xcode-select --install
brew install gcc make git   # 若需要
# 同 Linux：clone explorer 后按 README 编译
```

### Docker / 无编译环境

优先用发行包或单位已编译二进制；不要在未理解分支差异时混用多个 `rnx2rtkp`。

### 安装期常见报错

| 现象 | 处理 |
|---|---|
| `rnx2rtkp: command not found` | PATH；`which rnx2rtkp` |
| 编译 `undefined reference` | 缺库；装 `build-essential`；清再 make |
| Windows 智能屏幕拦截 | 解除锁定 / 单位白名单 |
| GUI 能开 CLI 没有 | 确认 `bin` 入 PATH，不是只装了 GUI 快捷方式 |
| 两套 RTKLIB 行为不同 | `which -a rnx2rtkp`；删掉旧版或改 PATH 顺序 |
| `-p` 与文档不符 | **重读本机 `-h`**，不要死记网络旧帖 |

### 安装验收

```bash
command -v rnx2rtkp convbin
rnx2rtkp -h | head -n 40
# 记录：分支名、编译日期、帮助里的 positioning mode 列表
```

---

## 快速冒烟（10 分钟）

准备：rover OBS+NAV；RTK 再加 base OBS。路径占位。

```bash
# 0) 输入自检
head -n 5 rover.obs base.obs rover.nav
python -m georinex.gtime rover.obs 2>/dev/null || gfzrnx -finp rover.obs -meta epo 2>/dev/null || true

# 1) 原始日志 → RINEX（若已是 RINEX 跳过）
convbin -r ubx -o rover.obs -n rover.nav rover.ubx
# 期望：生成非空 rover.obs / rover.nav

# 2) SPP 冒烟（最简）
rnx2rtkp -o out_spp.pos rover.obs rover.nav
wc -l out_spp.pos
head -n 5 out_spp.pos
# 期望：.pos 行数随历元增长；有头注释与数据行

# 3) 静态 RTK 示意（-p 以 -h 为准！）
rnx2rtkp -p 2 -m 15 -o out_rtk.pos rover.obs base.obs rover.nav
grep -v '^%' out_rtk.pos | head
```

**冒烟失败：** 空 `.pos`、立刻退出码非 0、或全是 Q=0 —— 查共视、时间对齐、文件是否 HTML。

---

## 完整工作流

### 工作流 A：事后 SPP → 看电离层活跃日残差

教程：[06](../tutorials/06-iono-positioning.md)。

```bash
mkdir -p out logs
rnx2rtkp -o out/spp.pos -m 10 rover.obs rover.nav 2> logs/spp.err
# 可选：配置文件
# rnx2rtkp -k conf/spp.conf -o out/spp.pos rover.obs rover.nav
wc -l out/spp.pos
awk 'BEGIN{c=0} !/^%/ {c++} END{print c}' out/spp.pos
```

**期望：** 数据行 > 0；日志无 `no navigation data` 一类致命错。

对照同日 ROTI（[oasis-roti](./oasis-roti.md)）：高 ROTI 时段 SPP 噪声变大属预期，不是 RTKLIB「坏了」。

### 工作流 B：短基线静态 RTK

```bash
# B1 确认时间重叠与共视（可用 georinex / anubis）
# B2 跑 RTK（示例旗标，核对 -h）
rnx2rtkp -p 2 -m 15 -o out/rtk.pos \
  rover.obs base.obs rover.nav 2> logs/rtk.err

# B3 统计 Q（列位置随版本变——先 head 看列名）
head -n 30 out/rtk.pos
# 典型注释含 Q: 1=fix, 2=float, 5=single ...（以文件头为准）

python - <<'PY'
from collections import Counter
q=Counter()
with open("out/rtk.pos") as f:
    for line in f:
        if line.startswith("%") or not line.strip():
            continue
        parts=line.split()
        # 许多版本 Q 在 ECEF 三列之后；若失败请按文件头改索引
        if len(parts) >= 6:
            try: q[parts[5]] += 1
            except Exception: pass
print(dict(q))
PY
```

**期望：** 短基线晴朗电离层下固定占比合理；赤道夜间 / 磁暴日固定率下降 → 对照教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)。

### 工作流 C：浮点 PPP（事后）

```bash
# 需要与观测日匹配的 SP3 + CLK；天线模型按手册
ls precise.sp3 precise.clk
rnx2rtkp -o out/ppp.pos rover.obs rover.nav precise.sp3 precise.clk 2> logs/ppp.err
# 或 -k conf/ppp.conf
wc -l out/ppp.pos
tail -n 5 out/ppp.pos
```

**期望：** 收敛后坐标稳定；缺产品 / 时长过短 → 不收敛。发表级模糊度固定走 [pride-pppar](./pride-pppar.md)。

### 工作流 D：convbin 批量 + QC 后再定位

```bash
for ubx in raw/*.ubx; do
  b=$(basename "$ubx" .ubx)
  convbin -r ubx -o "rinex/${b}.obs" -n "rinex/${b}.nav" "$ubx"
done
# QC
# anubis ...
# 再 rnx2rtkp
```

### 工作流 E：实时流（先事后、后实时）

```bash
# E1 用 BNC/pygnssutils 确认能拉流并落盘
# E2 str2str 转发示例（端口与路径自定）
str2str -in ntrip://user:pass@caster:2101/MOUNT -out tcpsvr://:2102
# E3 rtkrcv 或 RTKNAVI 订该端口
# 失败时：立刻退回文件模式 rnx2rtkp，排除流龄期问题
```

实时 PPP 无匹配 SSR 时关掉 PPP，只验流。

### 工作流 F：配置文件固化实验

```bash
cp conf/template.conf conf/my_rtk.conf
# 编辑：pos1-posmode, elev mask, ionoopt, tropopt, anttype...
rnx2rtkp -k conf/my_rtk.conf -o out/exp001.pos rover.obs base.obs rover.nav
# 每次只改一个旋钮；日志与 conf 一并归档
```

---

## 输入 / 输出与字段表

### 输入

| 类型 | 说明 |
|---|---|
| RINEX OBS | rover 必需；RTK 加 base |
| RINEX NAV | 广播星历；PPP 可加精密产品 |
| SP3 / CLK | PPP |
| ANTEX / 天线参数 | 精密处理 |
| UBX/RTCM/原始 | 经 `convbin` / `str2str` |
| 可选 IONEX | 作电离层改正输入（仍非 TEC 产品输出） |

### 输出 `.pos`（常见列，以文件头为准）

| 列 / 标记 | 含义 | 操作注意 |
|---|---|---|
| 时间 | GPST 等 | 与 ROTI/TEC 对齐时统一时间系 |
| x/y/z 或 e/n/u | 坐标 | 看头：ECEF 还是 ENU |
| `Q` | 解状态 | 1 固定 / 2 浮点 / … 以头注释为准 |
| `ns` | 卫星数 | 过少不可信 |
| sdn/sde/… | 标准差 | 用于粗滤 |

可选 `.stat`：残差与内部状态，排障用。

### 不做的输出

校准 STEC、ROTI 序列、IONEX GIM、闪烁 S4。

---

## 常用参数

| 项 | 说明 |
|---|---|
| `-p` | 定位模式编号（**必查 `-h`**） |
| `-o` | 输出 `.pos` |
| `-m` | 高度截止角（度） |
| `-k conf` | 配置文件 |
| `-sys` | 系统过滤（若支持） |
| `convbin -r` | 原始格式：ubx/rtcm3/… |
| `str2str -in/-out` | 流 URL |
| ionoopt / tropopt | 多在 conf；模型选择影响 PPP/RTK |

GUI（RTKNAVI / RTKPOST）与 CLI 配置**不要混用同一实验的「口头参数」**——以实际写入的 conf 为准。

---

## 接到 tutorials / 工作流哪一步

| 场景 | 步骤 | 链接 |
|---|---|---|
| 电离层与定位 | 本页工作流 A/B | [06](../tutorials/06-iono-positioning.md) |
| 磁暴日固定率 | B + ROTI 对照 | [20](../tutorials/20-storm-tec-analysis.md) · [05](../tutorials/05-scintillation-roti.md) |
| 实时差分实验 | E + BNC | [bnc](./bnc.md) · 路径 C |
| 发表级坐标 | RTKLIB 冒烟后换 | [pride-pppar](./pride-pppar.md) |
| 输入 QC | 定位前 | [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) |
| 只要 TEC | 离开本页 | [pytecgg](./pytecgg.md) · [02](../tutorials/02-gnss-dualfreq-tec.md) |

---

## 可操作坑（≥12）

1. **死记 `-p` 数字跨分支** — 每次新二进制先 `-h`。  
2. **无共视硬跑 RTK** — 先时间重叠与星座交集。  
3. **基线过长当短基线静态** — 固定率崩；改策略或 PPP。  
4. **PPP 缺 SP3/CLK 或日期错一天** — 不收敛。  
5. **天线高 / ARP 未设** — 高程系统差。  
6. **实时龄期爆炸却先调模糊度参数** — 先修网络与 caster。  
7. **把 `.pos` 当 TEC** — 错链；去 pytecgg。  
8. **混用 GUI 勾选与 CLI 旧 conf** — 归档 conf 哈希。  
9. **高多路径站** — 先 Anubis；别只降截止角。  
10. **NAV 与 OBS 不同日** — 夜班文件拼接错误。  
11. **Windows 与 Linux 换行 / 路径** — conf 内路径用正斜杠或按手册。  
12. **磁暴日与静日比固定率却改了全部参数** — 只留电离层相关变量。  
13. **str2str 权限绑定低端口** — 用 2102 等高端口。  
14. **explorer 与原版文档混贴** — 选定分支，只看该分支文档。  
15. **输出被旧文件追加弄脏** — 跑前删或换 `-o` 名。  
16. **忽略头注释改列解析脚本** — 升级 RTKLIB 后重看头。

---

## 同类选型

| 需求 | 选 |
|---|---|
| 教学 / 工程 RTK、快速 PPP 冒烟 | **RTKLIB** |
| PPP-AR、精密科研坐标 | **PRIDE-PPPAR** |
| 多流录盘 GUI | **BNC** |
| 脚本拉一流 | **pygnssutils** |
| TEC / ROTI | **pytecgg / oasis-roti / ionomoni** |

---

## 操作检查清单

1. `rnx2rtkp`/`convbin` 在 PATH。  
2. 记录分支与 `-h` 模式表。  
3. SPP 非空 `.pos`。  
4. RTK：共视、基线、Q 分布合理。  
5. PPP：产品时间覆盖。  
6. conf 与日志同目录归档。  
7. 实时前先事后冒烟。  
8. 不把输出当 TEC。  
9. 高 ROTI 时段单独标记。  
10. 参数以本机手册为准。

---

## 附录 A · `.pos` 头示意

```text
% program   : RTKLIB demo5
% ...
% (x/y/z-ecef=0,e/n/u-baseline=1,... Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp)
%  GPST                  x-ecef(m)      y-ecef(m)      z-ecef(m)   Q  ns
%  2024/01/01 00:00:00.000  ...
```

列索引以**你的文件头**为准，勿照抄旧博客。

---

## 附录 B · 最小回归

```bash
#!/usr/bin/env bash
set -euo pipefail
rnx2rtkp -o /tmp/spp_smoke.pos "$1" "$2"
test -s /tmp/spp_smoke.pos
grep -v '^%' /tmp/spp_smoke.pos | head -n 1
echo PASS
```

用法：`./smoke.sh rover.obs rover.nav`。

---

## 附录 C · 与 ROTI 对照流程

```bash
# 1) 出 pos
rnx2rtkp -k conf/rtk.conf -o out/storm.pos rover.obs base.obs rover.nav
# 2) 出 ROTI（工具链见 oasis-roti / ionomoni 手册）
# 3) 按时间对齐画 Q 与 ROTI；只报告相关，不宣称因果除非实验设计支持
```

---

## 附录 D · conf 关键项备忘（名称随版本）

| 概念 | 常见键（示意） | 操作 |
|---|---|---|
| 模式 | pos1-posmode | 与 `-p` 一致 |
| 截止角 | pos1-elmask | 15–20 常见起点 |
| 电离层 | pos1-ionoopt | 改时记日志 |
| 对流层 | pos1-tropopt | PPP 敏感 |
| 动力学 | pos1-dynamics | 静态/运动 |
| 模糊度 | pos2-* | 别一次全改 |

---

## 附录 E · convbin 期望

```text
$ convbin -r ubx -o rover.obs -n rover.nav rover.ubx
# 退出码 0；ls -l rover.obs 显示合理字节；head 见 RINEX VERSION
```

失败：格式旗标错、文件截断、权限。

---

## 附录 F · 错误日志关键词

| 日志 | 动作 |
|---|---|
| no common satellites | 查时间 / 系统 |
| no navigation data | NAV 路径 / 日 |
| point positioning error | 先 SPP 单独跑 |
| age of differential | 流延迟 |
| authenticity / license N/A | 忽略网络谣传；RTKLIB 开源 |

---

## 附录 G · 目录推荐布局

```text
exp/2024-01-01/
  raw/ conf/ rinex/ out/ logs/
  README.txt   # 分支、命令、数据来源
```

---

## 附录 H · 何时离开 RTKLIB

- 需要校准 TEC 图与 IPP → pytecgg。  
- 需要开源球谐解 → 列表 mosgim 等；非 SH-GIM 公开仓。  
- 需要多流合规录盘 → BNC。  
- 需要 AR 产品级 → PRIDE-PPPAR。

---

## 相关工具

[pride-pppar](./pride-pppar.md) · [bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [pytecgg](./pytecgg.md)


---

## 附录 I · 逐步排障树

```text
.pos 空或几乎空
  ├─ rnx2rtkp 退出码非 0 → 读 logs/*.err 第一处 error
  ├─ no navigation data → 换 NAV / 查日界
  ├─ OBS 是 HTML → 重新下载
  └─ 有数据但 Q 全 single
        ├─ 声称 RTK → 查是否传入 base.obs
        ├─ 基线过长 / 共视差 → 缩时段或换站
        └─ 截止角过高 → 降到 10–15 再比

PPP 不收敛
  ├─ SP3/CLK 覆盖？ `head`/`tail` 产品时间
  ├─ 观测时长 < 1–2 h？加长
  ├─ 天线/PCV？先关精密天线选项冒烟
  └─ 仍差 → 换 PRIDE-PPPAR 做对照
```

---

## 附录 J · 与 georinex 联合确认输入

```bash
python - <<'PY'
import georinex as gr
ro = gr.load("rover.obs", use="G")
ba = gr.load("base.obs", use="G")
print("rover", ro.time.values[0], ro.time.values[-1], ro.sizes)
print("base ", ba.time.values[0], ba.time.values[-1], ba.sizes)
# 粗算重叠
import numpy as np
t0 = max(ro.time.values[0], ba.time.values[0])
t1 = min(ro.time.values[-1], ba.time.values[-1])
print("overlap_ok", t0 < t1, t0, t1)
PY
rnx2rtkp -p 2 -o out/rtk.pos rover.obs base.obs rover.nav
```

---

## 附录 K · 批量多日 SPP

```bash
#!/usr/bin/env bash
set -euo pipefail
for day in 001 002 003; do
  rnx2rtkp -o "out/spp_${day}.pos" \
    "rinex/ROVI${day}0.24o" "rinex/brdc${day}0.24n" \
    2> "logs/spp_${day}.err" || echo "FAIL $day" | tee -a logs/fail.txt
done
wc -l out/spp_*.pos
```

---

## 附录 L · 质量门禁（交付前）

| 门禁 | 阈值（按项目改） |
|---|---|
| SPP 行数 | > 100 |
| RTK 固定占比 | 短基线静日 > 50%（示例） |
| 卫星数中位 | ≥ 8 |
| 日志 fatal | 0 |
| conf 已归档 | 是 |

不达标：停止出图，先修数据。

---

## 附录 M · 命令速查卡

```bash
rnx2rtkp -h
convbin -h
str2str -h
rtkrcv -h   # 若已编译
rnx2rtkp -o out.pos rover.obs rover.nav
rnx2rtkp -k my.conf -o out.pos rover.obs base.obs rover.nav
convbin -r ubx -o a.obs -n a.nav a.ubx
str2str -in file://a.rtcm3 -out tcpsvr://:2102
```

---

## 附录 N · 期望成功输出（SPP）

```text
%  GPST                  x-ecef(m)      y-ecef(m)      z-ecef(m)   Q  ns
2024/01/01 00:00:00.000  -3960000.123   3340000.456   3700000.789   5  10
2024/01/01 00:00:30.000  -3960000.111   3340000.444   3700000.777   5  11
```

---

## 附录 O · 安全与合规

- NTRIP 账号勿写入公开 git；用环境变量或本地 conf（gitignore）。  
- 数据再分发遵守提供方条款。  
- 不要对未授权 caster 做压测。

---

## 附录 P · 版本记录模板

```text
date:
rtklib_branch:
commit_or_release:
uname:
command:
input_files:
output:
notes:
```

每跑关键实验填一行。


---

## 附录 Q · 静态 vs 运动学检查

```bash
# 静态：接收机固定，pos 应收敛到亚米～厘米级（视模式）
# 运动学：不要用静态模式硬套车载数据
rnx2rtkp -k conf/static.conf -o out/static.pos rover.obs base.obs rover.nav
rnx2rtkp -k conf/kinematic.conf -o out/kine.pos rover.obs base.obs rover.nav
# 比较 residuals / Q；车载用 kinematic
```

---

## 附录 R · 电离层选项对照实验（可重复）

```bash
for opt in off brdc ionex; do
  # 在 conf 中切换 ionoopt；或按你分支支持的 CLI
  cp conf/base.conf conf/iono_${opt}.conf
  # 编辑 conf/iono_${opt}.conf …
  rnx2rtkp -k conf/iono_${opt}.conf -o out/iono_${opt}.pos \
    rover.obs base.obs rover.nav 2> logs/iono_${opt}.err
done
# 只改电离层项；其余锁定；结果表归档
```

---

## 附录 S · 相关工具（复述）

[bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [pride-pppar](./pride-pppar.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md)


---

## 附录 T · 一页纸验收

1. `which rnx2rtkp` 指向预期分支。  
2. SPP `.pos` 非空。  
3. RTK 有 base 且 Q 有变化。  
4. PPP 产品日匹配。  
5. conf + 日志已归档。  
6. 未把输出标成 TEC。  
7. 教程 [06](../tutorials/06-iono-positioning.md) 对照完成。  
8. 高 ROTI 时段已标记。  
9. NTRIP 密钥未入 git。  
10. `-h` 已保存到 `logs/rnx2rtkp_help.txt`。

```bash
rnx2rtkp -h > logs/rnx2rtkp_help.txt
convbin -h > logs/convbin_help.txt
```

完成以上再宣布「RTKLIB 链路通」。
