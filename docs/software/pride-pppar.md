# PRIDE-PPPAR

目录：[`PROJECTS.json` → `PRIDE-PPPAR`](../../PROJECTS.json) · 上游 <https://github.com/PrideLab/PRIDE-PPPAR> · 支持 <http://pride.apm.ac.cn> · 产品（以 README 为准）`ftps://bdspride.com/wum/` · GPL-3.0

> 操作手册。祈使句。面向需要 **发表级坐标 / ZTD / PPP-AR 固定率** 的岗位。入口命令默认 `pdp3`。依据上游 README（常见 3.2.x）与 `pdp3 -H`；冲突时 **以本机 `-H` 为准**。

---

## 用途与边界

**用：**

- 多 GNSS **精密单点定位 + 模糊度固定（PPP-AR）**。
- 静态站坐标、ZTD/梯度序列、固定率评估；浮点对照（`-f`）。
- 系统：GPS / GLONASS / Galileo / BDS-2/3 / QZSS；全频点双频无电离层组合（`-frq`）。
- 高动态 / 高采样、LEO（`-m L`）、多日连续解（跨日整数约束）。
- 磁暴日看「固定率是否崩」——与 ROTI **对照**（本工具不产 ROTI）。

**不用 / 边界：**

- **不产** STEC/vTEC/ROTI/S4 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。
- **不做** 实时多用户 NTRIP → [bkg-ntripcaster](./bkg-ntripcaster.md)。
- 短基线快速 RTK → [rtklib](./rtklib.md) 往往更直接。
- RINEX 清洗主工具 → [gfzrnx](./gfzrnx.md)（多日常**依赖**它）。
- `-hion` 二阶电离层是**改正**，不是 TEC 反演；`res_` **不要**当 STEC 发表。

一句话：PRIDE = **后处理 PPP-AR 引擎**；电离层在此是误差源/改正项。

---

## 安装（多平台 + 报错）

### 前置

| 组件 | 用途 |
|---|---|
| bash | `pdp3` / `install.sh` |
| make + gcc/gfortran | **必需** |
| wget 或 curl | 拉产品 |
| python3 | 部分脚本 |
| gfzrnx | 多日拼接（强烈建议） |

### Linux

```bash
sudo apt update
sudo apt install -y build-essential gfortran make wget curl git python3
# install.sh 拒绝 /root* —— 用普通用户
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh
# 首次强烈建议跑 example/test.sh（提示选 Y）

echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.bashrc
source ~/.bashrc
pdp3 -V
pdp3 -H | head -n 40
ls ~/.PRIDE_PPPAR_BIN | head
```

**期望：** 版本如 `3.2.11`；`-H` 含 `Usage: pdp3 [options] <obs-file>`；BIN 含 `pdp3`、`lsq`、`tedit`、`arsig` 等。

### macOS

```bash
brew install gcc wget python3
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR && bash install.sh
echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.zshrc && source ~/.zshrc
pdp3 -V
```

用较新 tag/master（上游曾修 BSD `sed` 导致的 shebang 问题）。

### Windows

科研批处理推荐 **WSL2** 按 Linux 安装。OBS 放 WSL 家目录，避免 `/mnt/c/...` 慢路径与空格。

### gfzrnx

```bash
which gfzrnx || echo "WARN: 多日拼接可能失败 — 见 gfzrnx.md"
```

### 安装验收 / 报错

| 现象 | 原因 | 修复 |
|---|---|---|
| `unable to install ... /root` | root 家目录 | 换普通用户 |
| `gfortran: not found` | 缺编译器 | `apt install gfortran` |
| `pdp3: command not found` | PATH | `source ~/.bashrc`；`which pdp3` |
| example 失败 | 产品下载/编译 | 先隔离网络与 gfortran，勿直接换站 |
| 多日报缺 gfzrnx | 未装或未改名 | [gfzrnx](./gfzrnx.md) |

```bash
pdp3 -V
which pdp3
# 安装时 test.sh 退出 0 为佳
```

---

## 快速冒烟（官方 example）

```bash
cd /path/to/PRIDE-PPPAR/example
bash test.sh
```

**期望：** 年/年积日子目录出现 `pos_` / `kin_` / `ztd_` / `res_` / `amb_` 等（前缀以版本为准）；终端无收尾 `error:`。

---

## 完整工作流

### 工作流 A：单日静态 PPP-AR（联网自动产品）

```bash
mkdir -p ~/pride_work && cd ~/pride_work
# OBS 已 QC；建议先 gfzrnx -chk（及需要的拼接/改名）

pdp3 -m S SITE0010.24o
```

**期望终端片段：**

```text
:: Processing time range: 2024-01-01 00:00:00 <==> 2024-01-01 23:59:30
:: Positioning mode: S
:: AR switch: A
:: RINEX observation file: .../SITE0010.24o
```

**期望产物：** `~/pride_work/2024/001/`（年/年积日）下非空 `pos_`、`ztd_` 等。

```bash
cd ~/pride_work/2024/001
ls -l
wc -l pos_* ztd_* 2>/dev/null | tail
head -n 40 pos_*
```

### 工作流 B：浮点对照 + 与 RTKLIB 交叉

```bash
cd ~/pride_work
pdp3 -m S    SITE0010.24o   # AR on
pdp3 -m S -f SITE0010.24o   # float
# 另用 rtklib rnx2rtkp 浮点 PPP（见 rtklib.md）
```

**期望：** 静态站固定解更稳；浮点噪声更大。两者都炸 → 查产品/天线/近似坐标，不单怪 AR。

### 工作流 C：系统与频率实验

```bash
pdp3 -m S -sys G   -frq "G12"         SITE0010.24o
pdp3 -m S -sys GE  -frq "G12 E15"     SITE0010.24o
pdp3 -m S -sys GE3 -frq "G12 E15 C26" SITE0010.24o
# 默认频率串示例（-H）："G12 R12 E15 C26 J12"
# BDS：2=B1I, 6=B3I, 1=B1C, 5=B2a … 以 -H 为准
```

**期望：** 卫星数↑通常有助连续弧；缺 OSB 的频点会在日志提示——改 `-frq`。

### 工作流 D：多日

```bash
pdp3 -s 2024/1 -e 2024/3 -m S SITE0010.24o
# 目录类似 2024/001-003；需要 gfzrnx 保证跨日连续性
# ≥108 天：脚本拒绝（以版本为准）
```

### 工作流 E：动态 / 宽松编辑

```bash
pdp3 -m K ROVE0010.24o
pdp3 -m K -l -c 10 ROVE0010.24o   # 高动态差数据
```

**期望：** `kin_` 连续；严格编辑删光时加 `-l` 后点数回升。

### 工作流 F：对流层 / 二阶电离层 / MHM / WCC

```bash
pdp3 -m S -z S -h P60 -r STO -p V3 SITE0010.24o
pdp3 -m S -hion SITE0010.24o          # 需 GIM
pdp3 -m S -mp SITE0010.24o            # 需恒星日量级多文件同目录
pdp3 -m S -wcc SITE0010.24o           # Wuhan Combination Center 产品
```

### 工作流 G：配置文件

```bash
cp ~/.PRIDE_PPPAR_BIN/config_template ./config_ops
# 编辑（合法枚举以手册为准），例如：
#   Interval=30  Strict editing=YES  ZTD model=STO
#   HTG model=PWC:60  Iono 2nd=NO  Multipath=NO
#   Ambiguity duration=600  Cutoff elevation=10
#   Truncate at midnight=NO
# 禁用问题星：在 +GNSS satellites 表用 # 注释 PRN

pdp3 -cfg ./config_ops -m S -c 15 -v SITE0010.24o 2> run.verbose.log
```

### 工作流 H：磁暴日固定率诊断

```bash
# 安静日与磁暴日各跑 pdp3 -m S
# 并行 oasis-roti / ionomoni 出 ROTI
# 将 AR 成功率、模糊度重置与 ROTI 高峰对齐（教程 20）
```

**勿做：** 把 `res_` 当 STEC 曲线发表。

### 工作流 I：离线产品

1. 按 v3.2 手册附录投放 SP3/CLK/OSB/ERP/ORBEX/ANTEX/广播星历到 Product/table 约定位置。  
2. 确认日期与站名齐全。  
3. 再 `pdp3`；仍联网则查脚本 `OFFLINE` 语义（高级；默认常见 OFFLINE=NO, USECACHE=YES）。

联网失败最小序：`curl -I` 产品主机 → 看日志哪类 404 → 手动放入 Product directory → 重跑。

---

## 输入 / 输出与参数表

### `pdp3` 常用选项

| 选项 | 含义 | 典型 |
|---|---|---|
| `-m S/P/K/F/L` | 静态/分段/动态/固定/LEO | `-m S` |
| `-f` | 关 AR（浮点） | 对照 |
| `-sys` | 系统子集 `GREC23J` | `GE3` |
| `-frq` | 频率对 | `"G12 E15 C26"` |
| `-cfg` | 配置文件 | `./config_ops` |
| `-s` / `-e` | 起止 | `2024/001` |
| `-n` | 4 字符站名 | `SITE` |
| `-i` | 处理间隔秒 | `30` |
| `-c` | 截止高度角° | `10`/`15` |
| `-l` | 宽松编辑 | 高动态 |
| `-hion` | 二阶电离层 | 需 GIM |
| `-mp` | MHM 多路径 | 需多日 |
| `-wcc` | WCC 产品 | RAP 缺失时 |
| `-z`/`-h`/`-r`/`-p` | ZTD/HTG/钟/映射 | 见 `-H` |
| `-v` | 详细 AR/LSQ | 排障 |
| `-twnd` | 非标准时间窗 | 怪 RINEX |
| `-toff` / `-aoff` | 关潮汐 / 宽巷 APC | 见 `-H` |

### 定位模式

| 码 | 模式 | 备注 |
|---|---|---|
| S | Static | 连续跟踪站首选 |
| P | Piece-wise | 如 `P300 0.001` |
| K | Kinematic | 流动站 |
| F | Fixed | 坐标固定估大气 |
| L | LEO | 需姿态/专用 table |

### 频率编号（摘自 `-H`，以本机为准）

| 系统 | 1 | 2 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| G | L1 | L2 | L5 | — | — | — |
| R | L1 | L2 | — | — | — | — |
| E | E1 | — | E5a | E6 | E5b | E5 |
| C | B1C | B1I | B2a | B3I | B2b | B2 |
| J | L1 | L2 | L5 | L6 | — | — |

### 结果文件前缀（以版本为准）

| 前缀 | 内容 | 下游 |
|---|---|---|
| `pos_` | 位置 | 坐标序列 |
| `kin_` | 动态轨迹 | 可转 CSV |
| `ztd_` | 对流层 | 气象交叉 |
| `res_` | 残差 | QC；**非 TEC** |
| `amb_` | 模糊度 | 固定率 |

### 工作目录规则

- 单日：`项目/年/年积日/`
- 多日（<108 天）：`年/起始-结束/`
- ≥108 天：拒绝

### 与 GFZRNX / Anubis 契约

| 前置 | 要求 |
|---|---|
| OBS | 头完整；MARKER 可用；近似坐标非零 |
| 采样 | 与 `-i` 一致或更密 |
| 命名 | 多日优先 RINEX3 |
| Anubis | 无大段空洞、无异常钟跳再进 |

```bash
gfzrnx -finp SITE0010.24o -meta basic:txt
gfzrnx -finp SITE0010.24o -stk_obs | head
```

---

## 接到 tutorials / 工作流哪一步

| 场景 | 本手册 | 链接 |
|---|---|---|
| 路径 D 精密定位 | A/B | [gfzrnx](./gfzrnx.md) → [anubis](./anubis.md) → **pdp3** → [06](../tutorials/06-iono-positioning.md) |
| 磁暴固定率 | H | [20](../tutorials/20-storm-tec-analysis.md) + ROTI 工具 |
| DCB / OSB 理解 | C | [09](../tutorials/09-dcb-biases-deep.md) |
| 旁路浮点 | B | [rtklib](./rtklib.md) |
| TEC 链 | **并行**共用清洗 OBS | 勿接 `res_` 当 STEC |

---

## 可操作坑（现象 → 原因 → 修复）

1. **root 安装被拒**  
   原因：`install.sh` 拒绝 `/root*`。  
   修复：普通用户重装。

2. **编译失败**  
   原因：无 gfortran。  
   修复：`gfortran --version`；装 build-essential。

3. **产品 FTPS/下载失败**  
   原因：防火墙、证书、地址变更、日期未发布。  
   修复：读 README 现址；试 `-wcc`；改离线投放。

4. **多日失败喊缺工具**  
   原因：无 `gfzrnx`。  
   修复：安装并改名为 `gfzrnx` 入 PATH。

5. **大量缺测 / AR 起不来**  
   原因：`-frq` 选了站上没有的频点。  
   修复：`gfzrnx -stk_obs`；改频率串。

6. **截止角过高导致 AR 崩**  
   原因：如 `-c 30` 高纬冬季星不足。  
   修复：降到 10–15 对比。

7. **车载点数被删光**  
   原因：严格编辑。  
   修复：`-l` 或配置 `Strict editing=NO`。

8. **`-mp` 建模失败**  
   原因：缺恒星日量级数据。  
   修复：补文件或去掉 `-mp`。

9. **把 `res_` 当 TEC 发表**  
   原因：残差含轨道钟差对流层多路径。  
   修复：TEC 走 pytecgg。

10. **固定率 0 但浮点也跳**  
    原因：产品/天线/坐标问题，不单是 AR。  
    修复：先 `-f` 与 anubis；查 ANTEX、近似坐标。

11. **固定率 0 仅暴日**  
    原因：电离层扰动。  
    修复：叠 ROTI；降系统到 G/GE 对比。

12. **PATH 新终端失效**  
    原因：未 source。  
    修复：写入 bashrc/zshrc；`which pdp3`。

13. **时间戳非标准秒退**  
    原因：怪 RINEX 时间标签。  
    修复：`-twnd`；或 gfzrnx 规范后再跑。

14. **RINEX4 / 新 BDS 旧版挂**  
    原因：软件过旧。  
    修复：升到当前 3.2.x。

15. **AI 检验与旧论文不一致**  
    原因：3.2 默认机器学习检验。  
    修复：对照 CHANGELOG/配置复现旧设置。

16. **Windows 路径空格/权限怪**  
    原因：原生路径坑。  
    修复：WSL + Linux 路径。

---

## 同类选型

| 需求 | 优先 |
|---|---|
| 多系统 PPP-AR、ZTD | **PRIDE-PPPAR** |
| 快速基线 RTK | RTKLIB |
| 浮点 PPP 验证 | RTKLIB 或 `pdp3 -f` |
| TEC/ROTI | pytecgg / oasis / ionomoni |
| 实时改正流 | pygnssutils / BNC |

文献：Geng et al., GPS Solutions, 2019；仓库 `doc/` 下 v3.2 manual；`pride@whu.edu.cn`。

---

## 操作检查清单

1. `pdp3 -V` 符合预期；`which pdp3` 正确。  
2. OBS 已 QC；目标频点存在。  
3. 产品可下载或离线齐全。  
4. example 或短时段冒烟通过。  
5. 固定 + 浮点对照。  
6. `pos_`/`ztd_` 非空并抽查头。  
7. 磁暴日准备 ROTI 图。  
8. 移交：`pos_`/`ztd_`/`amb_` + 完整命令 + 版本 + 产品日标识。  
9. 冲突时：**`pdp3 -H` > 官方 PDF > 本文**。

---

## 附录 · 场景卡片

```bash
# 静态一日
pdp3 -m S -c 10 SITE0010.24o
# 只 GPS
pdp3 -m S -sys G -frq "G12" SITE0010.24o
# ZTD + VMF3
pdp3 -m S -z S -p V3 SITE0010.24o
# 分段
pdp3 -m P300 0.001 SITE0010.24o
# 详细日志
pdp3 -m S -v SITE0010.24o 2> run.verbose.log
```

### 日志关键字

| 关键词 | 处置 |
|---|---|
| `/root` install | 换用户 |
| `time span too long` | 缩短 `-s/-e` |
| `mhm model failed` | 补数据或去 `-mp` |
| 产品 `404` | 查日期/镜像/`-wcc` |
| OSB unavailable | 改 `-frq` |
| `processing failed` | 向上找第一条 `error:` |

---

## 相关

[README](./README.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [rtklib](./rtklib.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md) · [09](../tutorials/09-dcb-biases-deep.md)
