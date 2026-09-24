# TEQC · Translate / Edit / Quality Check 操作手册

目录：[`PROJECTS.json` → `TEQC`](../../PROJECTS.json) · 官网 <https://www.unavco.org/software/data-processing/teqc/teqc.html> · 教程 HTML <https://www.unavco.org/software/data-processing/teqc/tutorial/tutorial.html> · PDF <https://www.unavco.org/software/data-processing/teqc/doc/UNAVCO_Teqc_Tutorial.pdf> · **闭源免费二进制** · **EOL：终版 2019Feb25** · 本机：CentOS x86_64 **静态**包 → `teqc +qc` demo.18o → **3** 历元 / MP12≈**0.20** m · 2026-09-24 04:42 EDT

> 岗位：经典 **翻译 / 编辑 / 质检** 三合一 CLI（读厂商二进制与 RINEX 2.x）。冲突时：**本机 `teqc +help` / 官方 Tutorial > 本文**。**新工程优先** [gfzrnx](./gfzrnx.md)（切拼抽）+ [anubis](./anubis.md)（现代 QC）+ [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)（CRX）；批壳仍绑 TEQC 时见 [pinot](./pinot.md)。

## 1. 用途与边界

**做（终版仍能做）：**

- **Translate**：Trimble DAT/RT17、Septentrio SBF、Javad/Topcon、Leica、Ashtech、u-blox UBX 等 → RINEX OBS/NAV/MET 或 BINEX（能力随固件年代衰减）
- **Edit**：改头（`-O.mo` 等）、时间窗（`-st`/`+dh`）、拼接、抽稀（`-O.dec`）、滤星
- **Quality check**：`+qc` / `+qcq`；qc-lite（无 NAV）或 qc-full（有 NAV）；ASCII 时序图 + `*.YYS` 报告；可选 COMPACT 图文件

**不做 / EOL 诚实边界：**

- **已停更**：2019-02-25 终版后无功能更新；**不支持 RINEX 3/4 为主格式**（教程写明无 RINEX 3.00 计划）
- **源码不公开**（厂商 NDA）；只有多平台 zip 二进制
- **不是** 现代多系统 XTR/XML QC → [anubis](./anubis.md)
- **不是** RINEX 3/4 拼接抽稀主力 → [gfzrnx](./gfzrnx.md)
- **不是** Hatanaka 官方实现 → [rnxcmp](./rnxcmp.md)

一句话：TEQC = **历史标准预处理瑞士军刀**；新站用它读旧档可以，建新流水线请并行迁移。

| 术语 | 含义 |
| --- | --- |
| T / E / Q | Translate / Edit / Quality check，可单独或组合 |
| qc-lite / qc-full | 无星历 vs 有 NAV/二进制星历（可算位置/高度角） |
| `+` / `-` 前缀 | 大体：`+` 打开输出/功能，`-` 输入配置或关闭；头编辑 `-O.*` 与 `+O.*` 常等价 |
| `*.YYS` | qc 短/长报告文件（年两位 + `S`） |
| MP1/MP2、IOD | 多路径组合、电离层变化率（周跳敏感） |

## 2. 安装（Linux 二进制）

无安装包：下载 zip → 解压 → `PATH`。

```bash
mkdir -p ~/iono_ops/teqc ~/bin && cd ~/iono_ops/teqc
# 静态链（CentOS 构建）；若崩再试动态 teqc_CentOSLx86_64d.zip
curl -fsSL -o teqc_CentOSLx86_64s.zip \
  "https://www.unavco.org/software/data-processing/teqc/development/teqc_CentOSLx86_64s.zip"
unzip -o teqc_CentOSLx86_64s.zip
chmod +x teqc
cp -f teqc ~/bin/teqc
export PATH="$HOME/bin:$PATH"
teqc +version
# 期望：
# executable:  teqc
# version:     teqc  2019Feb25
# build:       Linux …|gcc -static|Linux 64|=+
```

其它包名（同目录 `…/teqc/development/`）：`teqc_Lx86_64s.zip` / `teqc_Lx86_64d.zip`、Windows `teqc_*mingw*.zip`、macOS 等——以[官网 Executables](https://www.unavco.org/software/data-processing/teqc/teqc.html)为准。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 静态包崩溃 | 与新内核/环境不兼容 | 换 `…_64d.zip` 动态包（或反之） |
| 双击 `teqc.exe` 闪退 | 无 GUI | Windows 用 `cmd` 跑命令行 |
| `pinot` 的 `qualitycheck` 找不到 teqc | Linux PATH 无二进制 | 按上表把 `teqc` 放进 `PATH` |

## 3. 端到端：RINEX2 格式检查 → 改头 → 窗切 → qc-lite（本机真跑）

数据：georinex 测试 OBS（RINEX **2.11**，约 30 s，混合系统）。

```bash
mkdir -p ~/iono_ops/data/teqc_demo && cd ~/iono_ops/data/teqc_demo
curl -fsSL -o demo.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o

teqc +v demo.18o
# 期望 stderr：teqc: 'demo.18o' readable as RINEX V.2.11 format

teqc +meta demo.18o | head
# 本机：start 2018-06-22 06:17:30 … final 06:18:00；interval 15 s；4-char code demo

teqc -O.mo DEMO_SITE demo.18o > demo_edit.18o
grep 'MARKER NAME' demo_edit.18o
# 期望：DEMO_SITE … MARKER NAME

teqc +dh 1 demo.18o > demo_1h.18o   # 从文件起点起 +1 h 窗（本文件本身更短）

teqc +qc demo.18o 2>qc_err.txt | tee qc_out.txt | head -n 50
ls -la demo.18S
```

**本机 qc-lite 摘要（2019Feb25 静态，2026-09-24 04:42 EDT）：**

```text
Time of start of window : 2018 Jun 22  06:17:30.000
Time of  end  of window : 2018 Jun 22  06:18:00.000
Observation interval    : 15.0000 seconds
Total satellites w/ obs : 13
Poss. # of obs epochs   :      3
Epochs w/ observations  :      3
Moving average MP12     : 0.200706 m
Moving average MP21     : 0.220987 m
IOD slips               :      0
SUM …  .0125  15  …  mp1 0.20  mp2 0.22  o/slps 30
```

stderr 进度形如 `qc lite >>>>>…`；缺 GLONASS 槽频文件时出 Notice（qc-lite 可忽略）。有匹配 `*.YYn` 或 `-nav file` 时自动/显式进 **qc-full**。

### 3.1 翻译 / 拼接（旗标示例，来自官方 Tutorial + `+help`）

```bash
# Trimble DAT → OBS+NAV（需正确 GPS 周；可用 +meta/+mds 先探）
teqc -tr d -week 866 +nav out.96n in.dat > out.96o
# 或 RT17 流：-tr s

# 多段 OBS 合法拼接（勿用裸 cat）
teqc day1.18o day2.18o > splice.18o
teqc -phc day1.18o day2.18o > splice_clean.18o   # 少保留拼接后注释

# 抽稀到 30 s
teqc -O.dec 30 in.18o > out30.18o

# 显式时段
teqc -st 20180622061730 -e 20180622061800 in.18o > win.18o
```

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX 1/2 OBS·NAV·MET | 默认假设；`+v` 只验格式 |
| 厂商二进制 / BINEX | `-tr`/`-ash`/`-septentrio`/… 或部分可 `+mdf` 自识别 |
| NAV（qc-full） | `-nav a.n,b.n` 或同名 `*.YYo`→`*.YYn` 自动匹配 |

| 输出 | 说明 |
| --- | --- |
| stdout | 默认重写 RINEX；`+qc` 时改为短报告副本 |
| `*.YYS` | qc 报告（`+s`/`+l` 控制短/长段） |
| `*.ion`/`*.mp1`/… | `+plot` 时 COMPACT 图（需 `gt`/`qcview` 看） |
| 不输出 | RINEX 3/4 一等公民产品、Anubis 式 XTR |

## 5. 模式与旗标速查

| 旗标 | 模式 / 作用 |
| --- | --- |
| （无特殊）`teqc file` | 读入并重写出 RINEX（格式体检+规范化） |
| `+v` | 只验证，不喷 stdout 全文 |
| `+meta` / `+mds` | 元数据表 / 起止时间+字节短摘要 |
| `+qc` / `+qcq` | 质检；`+qcq` 无完整长报告 |
| `-nav file` | qc-full 星历；可逗号多文件 |
| `-O.mo 'NAME'` | 改 MARKER NAME |
| `-O.dec 30` | 历元抽稀 |
| `-st` / `-e` / `+dh` / `-dm` | 窗：起点、终点、从起点+Δ、从终点−Δ |
| `-tr d` / `-tr s` | Trimble DAT / RT17 |
| `+obs f` / `+nav f` | 翻译时把 OBS/NAV 写到命名文件 |
| `-week N` | 二进制缺周时指定起始 GPS 周 |
| `-config file` | 读配置文件（`++config` 可导出模板） |
| `+help` | 全帮助（很长，落 stderr） |

## 6. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| 新站 RINEX3/4 切拼抽 | [gfzrnx](./gfzrnx.md) |
| 现代多系统 QC 报告 | [anubis](./anubis.md) |
| CRX 压缩/恢复 | [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md) |
| 仍调用 teqc 的旧批壳 | [pinot](./pinot.md) |
| C++ 库级 RINEX 摘要 | [gnsstk](./gnsstk.md)（`RinSum`） |
| 厂商近实时→RINEX3/4 | [autorino](./autorino.md) |

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 新固件原始格式译烂/半空 | EOL，格式已漂移 | 换厂商工具或 [autorino](./autorino.md)；旧档才用 teqc |
| 2 | RINEX 3 长名进不来 | 设计停在 2.x | 先 [gfzrnx](./gfzrnx.md)/[georinex](./georinex.md) |
| 3 | `cat a.o b.o` 出的文件谁都不认 | RINEX 禁止裸拼接 | `teqc a.o b.o > ab.o` |
| 4 | qc 无位置/高度角 | 缺 NAV → qc-lite | 放同名 `*.YYn` 或 `-nav brdc.n` |
| 5 | 静态 Linux 包 segfault | 链接/内核组合 | 换 `teqc_CentOSLx86_64d.zip` |
| 6 | Windows 双击无窗口 | 纯 CLI | `cmd` 里跑 `teqc +version` |
| 7 | 翻译 OBS 日期错一周 | 二进制记录无周 | `teqc +meta file` 看提示后加 `-week N` |
| 8 | 把 MP/IOD 当发表级 TEC | qc 是质控组合量 | TEC 产品走 [pytecgg](./pytecgg.md) |
| 9 | `+qc` 多文件变成「一大段」报告 | 多 target 单次执行拼窗 | 要分日报告则循环单文件调用 |
| 10 | csh/DOS 里 stdout/stderr 糊一起 | 壳不能分重定向 | 加 `+out out.txt +err err.txt` |
| 11 | pinot `qualitycheck` 空结果 | PATH 无 Linux `teqc` | 本页 §2；或改 [anubis](./anubis.md) |
| 12 | 以为官网会继续发新版 | 已宣布 EOL | 终版保留下载；新链路见 §6 |

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 读 **2019 前** 厂商二进制 / 旧 RINEX2 质控 | **TEQC（本页）** |
| RINEX 3/4 切拼抽稀 | [gfzrnx](./gfzrnx.md) |
| 多系统 QC 报告（XTR/XML） | [anubis](./anubis.md) |
| Hatanaka CRX | [rnxcmp](./rnxcmp.md) |
| 库/CLI 摘要 OBS（开源） | [gnsstk](./gnsstk.md) |
| 旧台网批脚本已绑 teqc | [pinot](./pinot.md) + 本页二进制 |

## 9. 相关

[gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [rnxcmp](./rnxcmp.md) · [hatanaka](./hatanaka.md) · [pinot](./pinot.md) · [gnsstk](./gnsstk.md) · [autorino](./autorino.md) · [README](./README.md)
