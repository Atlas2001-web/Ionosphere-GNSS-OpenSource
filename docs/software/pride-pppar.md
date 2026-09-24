# PRIDE-PPPAR · 多系统 PPP-AR 操作手册

目录：[`PROJECTS.json` → `PRIDE-PPPAR`](../../PROJECTS.json) · 上游 <https://github.com/PrideLab/PRIDE-PPPAR> · 支持 <http://pride.apm.ac.cn> · 产品（README）`ftps://bdspride.com/wum/` · GPL-3.0

> 祈使句。岗位：发表级坐标 / ZTD / PPP-AR。入口 **`pdp3`**。冲突时 **本机 `pdp3 -H` > 官方 PDF > 本文**。

**质检机（Round6，2026-09-24 ET）：** 本机已编装 **v3.2.11**（`~/.PRIDE_PPPAR_BIN`）。下列 `-V`/`-H`、会话头、产品失败日志为**实跑**；`pos_`/`amb_` 头摘自上游 `example/results_ref`（**非**本机解算坐标/固定率——本机因 WUM FTPS TLS 失败未出解）。**禁止**臆造固定率或坐标精度数字。GFZRNX：多日常依赖；需上游注册，**不贴臆造 gfzrnx stdout**。

## 1. 用途与边界

**做：**

- 多 GNSS **PPP + 模糊度固定（PPP-AR）**；浮点对照（`-f`）
- 静态坐标、ZTD/梯度、固定率评估；系统 GPS/GLO/GAL/BDS-2/3/QZSS；`-frq` 选双频无电离层组合
- 高动态 / LEO（`-m L`）/ 多日（跨日整数约束）；磁暴日看固定率是否崩（与 ROTI **对照**，本工具不产 ROTI）

**不做：**

- STEC/vTEC/ROTI/S4 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
- 实时多用户 NTRIP → [bkg-ntripcaster](./bkg-ntripcaster.md)
- 短基线 RTK 主力 → [rtklib](./rtklib.md)
- RINEX 清洗主工具 → [gfzrnx](./gfzrnx.md)
- `-hion` 是二阶电离层**改正**，不是 TEC 反演；`res_` **勿**当 STEC 发表

一句话：PRIDE = **后处理 PPP-AR 引擎**；电离层在此是误差源/改正项。

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| bash + make + **gcc/gfortran** | 必需 |
| wget 或 curl | 拉产品 |
| python3 | 部分脚本 |
| **bc** | `pdp3` 校验截止角等（缺则报 `invalid cutoff elevation`） |
| gfzrnx | 多日拼接（强烈建议；需注册） |

### Linux（本机已通）

```bash
sudo apt update
sudo apt install -y build-essential gfortran make wget curl git python3 bc
# install.sh 拒绝 /root* —— 用普通用户
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh          # 首次建议例程选 Y；无人值守可回 N
echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.bashrc
source ~/.bashrc
pdp3 -V
pdp3 -H | head -n 40
ls ~/.PRIDE_PPPAR_BIN | head
```

**本机实跑（3.2.11）：**

```text
© GNSS Research Center of Wuhan University, 2023
  GNSS PPP & PPP-AR data processing with PRIDE PPP-AR version 3.2.11
```

`which pdp3` → `~/.PRIDE_PPPAR_BIN/pdp3`；BIN 含 `pdp3` `lsq` `tedit` `arsig` `spp` `mhm` `config_template` 等。

### macOS / Windows

- macOS：`brew install gcc wget python3`；较新 tag（曾修 BSD `sed` shebang）。
- 科研批处理：用 **WSL2**；OBS 放 WSL 家目录，避 `/mnt/c` 与空格。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `unable to install ... /root` | root 家目录 | 换普通用户 |
| `gfortran: not found` | 缺编译器 | `apt install gfortran` |
| `pdp3: command not found` | PATH | `source ~/.bashrc` |
| `invalid cutoff elevation` | 缺 **bc** | `apt install bc` |
| 多日报缺 gfzrnx | 未装 | 见 [gfzrnx](./gfzrnx.md) |

## 3. 端到端

### 3.1 官方 example（首次必做）

```bash
cd /path/to/PRIDE-PPPAR/example
bash test.sh
# 或安装结束选 Y
```

**期望：** 年/年积日子目录出现 `pos_` / `kin_` / `ztd_` / `res_` / `amb_` 等；终端无收尾 `error:`。上游附带 `results_ref/` 可对照**文件名与头结构**（勿把参考坐标当本机解）。

### 3.2 单日静态 PPP-AR（联网产品）

```bash
mkdir -p ~/pride_work && cd ~/pride_work
# OBS 已 QC；需要时先 gfzrnx（注册后自备，勿臆造输出）
pdp3 -m S -c 10 /path/to/abmf0010.20o
```

**本机实跑会话头（example `abmf0010.20o`，2026-09-24）：**

```text
:: Processing time range: 2020-01-01 00:00:00.000 <==> 2020-01-01 23:59:30.000
:: Processing interval: 30
:: Site name: abmf
:: Positioning mode: S
:: AR switch: A
:: Frequency combination: G12 R12 E15 C26 J12
:: Configuration file: .../.PRIDE_PPPAR_BIN/config_template
:: RINEX observation file: .../abmf0010.20o
===> ProcessSingleSession from 2020 001 to 2020 001 ...
```

**本机产品失败（FTPS TLS / 目录拒绝——环境相关，作排障样本）：**

```text
error: PrepareProducts: failed to download satellite orbit product: WUM0MGXRAP_20200010000_01D_05M_ORB.SP3.gz
:: please download from ftp://igs.ign.fr/pub/igs/products/mgex/2086/WUM0MGXRAP_20200010000_01D_05M_ORB.SP3.gz to .../2020/product//common for processing
error: PrepareProducts failed
```

`-wcc` 同日亦可能：`Wuhan Combination Center no satellite orbit product`。处置：手投 SP3/CLK/OSB/ERP/OBX 到 `年/product/common`，或换可达镜像 / 近期站日；成功后再验收 `pos_`/`ztd_`。

**成功后抽查（路径以跑通为准）：**

```bash
cd ~/pride_work/2020/001
ls -l
wc -l pos_* ztd_* amb_* 2>/dev/null
head -n 40 pos_*
```

### 3.3 上游 `results_ref` 头结构（非本机解）

`example/results_ref/static-24h-fixed/` 含：`pos_` `ztd_` `amb_` `res_` `htg_` `rck_` `stt_` `cst_` `log_`。`pos_` 头字段示例（摘自上游参考，**勿抄作本机坐标成果**）：

```text
abmf                                                        STATION
Static      10.000000 10.000000 10.000000                   POS MODE/PRIORI (meter)
YES                                                         OBS STRICT EDITING
2020  1  1  0  0  0.00                                      OBS FIRST EPOCH
2020  1  1 23 59 30.00                                      OBS LAST EPOCH
   30.00                                                    OBS INTERVAL (sec)
WUM0MGXRAP_20200010000_01D_05M_ORB.SP3                      SAT ORBIT
...
YES  GPS    40  GAL    24  BDS2    2  BDS3   22  QZSS    0  AMB FIXING
```

### 3.4 浮点对照 / 系统频率 / 多日 / 动态

```bash
pdp3 -m S    SITE0010.24o      # AR on
pdp3 -m S -f SITE0010.24o      # float
# 另用 rtklib 浮点 PPP 交叉（见 rtklib.md）

pdp3 -m S -sys G   -frq "G12"         SITE0010.24o
pdp3 -m S -sys GE  -frq "G12 E15"     SITE0010.24o
pdp3 -m S -sys GE3 -frq "G12 E15 C26" SITE0010.24o
# 默认频率串（本机 -H）："G12 R12 E15 C26 J12"

pdp3 -s 2024/1 -e 2024/3 -m S SITE0010.24o   # 需 gfzrnx；≥108 天拒绝
pdp3 -m K -l -c 10 ROVE0010.24o              # 高动态差数据加 -l
```

### 3.5 对流层 / 二阶电离层 / MHM / 配置

```bash
pdp3 -m S -z S -h P60 -r STO -p V3 SITE0010.24o
pdp3 -m S -hion SITE0010.24o     # 需 GIM
pdp3 -m S -mp SITE0010.24o       # 需恒星日量级多文件同目录
pdp3 -m S -wcc SITE0010.24o      # WCC 产品

cp ~/.PRIDE_PPPAR_BIN/config_template ./config_ops
# 常见键（本机模板）：Interval / Strict editing / ZTD model / HTG model /
#   Iono 2nd / Multipath / Ambiguity duration / Cutoff elevation / Truncate at midnight
# 问题星：在 +GNSS satellites 表用 # 注释
pdp3 -cfg ./config_ops -m S -c 15 -v SITE0010.24o 2> run.verbose.log
```

### 3.6 磁暴日固定率诊断

安静日与磁暴日各跑 `pdp3 -m S`；并行 oasis-roti / ionomoni 出 ROTI；把 AR 成功率与 ROTI 高峰对齐（教程 20）。**勿**把 `res_` 当 STEC。

### 3.7 离线产品

按手册附录把 SP3/CLK/OSB/ERP/ORBEX/ANTEX/广播星历放到 Product/table 约定位置 → 再 `pdp3`。联网失败最小序：`curl -I` 产品主机 → 读哪类 404/TLS → 手投 `年/product/common` → 重跑。

## 4. 输入 / 输出与参数（摘自本机 `-H`）

| 选项 | 含义 | 典型 |
| --- | --- | --- |
| `-m S/P/K/F/L` | 静态/分段/动态/固定/LEO | `-m S`（默认实为 K，静态请显式 `-m S`） |
| `-f` | 关 AR | 对照 |
| `-sys` | `GREC23J` 子集 | `GE3` |
| `-frq` | 频率对 | `"G12 E15 C26"` |
| `-cfg` | 配置文件 | `./config_ops` |
| `-s` / `-e` | 起止 | `2024/001` |
| `-n` | 4 字符站名 | `SITE` |
| `-i` | 处理间隔秒 | `30` |
| `-c` | 截止高度角° | `10`/`15`（需 bc） |
| `-l` | 宽松编辑 | 高动态 |
| `-hion` | 二阶电离层 | 需 GIM |
| `-mp` | MHM | 需多日 |
| `-wcc` | WCC 产品 | RAP 缺失时 |
| `-z`/`-h`/`-r`/`-p` | ZTD/HTG/钟/映射 | 见 `-H` |
| `-v` | 详细 AR/LSQ | 排障 |
| `-twnd` / `-toff` / `-aoff` | 时间窗/潮汐/宽巷 APC | 见 `-H` |
| `-x 1/2/3` | 固定方法：rounding / LAMBDA ratio / LAMBDA+AI | 见 `-H` 默认 |

频率编号（`-H`）：G:L1/L2/L5；R:L1/L2；E:E1/E5a/E6/E5b/E5；C:B1C/B1I/B2a/B3I/B2b/B2；J:L1/L2/L5/L6。

| 前缀 | 内容 | 注意 |
| --- | --- | --- |
| `pos_` / `kin_` | 位置 / 轨迹 | 坐标序列 |
| `ztd_` | 对流层 | 气象交叉 |
| `res_` | 残差 | **非 TEC** |
| `amb_` | 模糊度 | 固定率 |

工作目录：单日 `年/年积日/`；多日（<108）`年/起始-结束/`。

## 5. 接到哪一步

| 场景 | 本页 | 链接 |
| --- | --- | --- |
| 路径 D | §3.2–3.4 | gfzrnx → anubis → **pdp3** → [06](../tutorials/06-iono-positioning.md) |
| 磁暴固定率 | §3.6 | [20](../tutorials/20-storm-tec-analysis.md) + ROTI |
| DCB/OSB | §3.4 `-frq` | [09](../tutorials/09-dcb-biases-deep.md) |
| 旁路浮点 | `-f` | [rtklib](./rtklib.md) |
| TEC 链 | **并行**共用清洗 OBS | 勿接 `res_` |

## 6. 坑（≥8）

1. **root 安装被拒** → 普通用户。  
2. **无 gfortran / 无 bc** → 装编译器与 bc。  
3. **产品 FTPS TLS / 404 / 目录拒绝** → 手投 IGN/镜像；试 `-wcc`；换日期。  
4. **多日缺 gfzrnx** → 注册安装并改名入 PATH。  
5. **`-frq` 选了站上没有的频点** → 自备观测类型表；改频率串。  
6. **截止角过高 AR 崩** → 对比 10–15°。  
7. **车载点数被删光** → `-l` 或 `Strict editing=NO`。  
8. **`-mp` 失败** → 补恒星日数据或去掉。  
9. **`res_` 当 TEC 发表** → 走 pytecgg。  
10. **固定率 0 且浮点也跳** → 先 `-f` + anubis；查 ANTEX/近似坐标/产品。  
11. **仅暴日固定率 0** → 叠 ROTI；降到 G/GE 对比。  
12. **PATH 新终端失效** → 写入 bashrc；`which pdp3`。  
13. **怪时间戳秒退** → `-twnd` 或 gfzrnx 规范。  
14. **RINEX4 / 新 BDS 旧版挂** → 升到当前 3.2.x。

## 7. 选型

| 需求 | 优先 |
| --- | --- |
| 多系统 PPP-AR、ZTD | **PRIDE-PPPAR** |
| 快速基线 RTK | RTKLIB |
| 浮点验证 | RTKLIB 或 `pdp3 -f` |
| TEC/ROTI | pytecgg / oasis / ionomoni |
| 实时改正流 | pygnssutils / BNC |

文献：Geng et al., GPS Solutions, 2019；仓内 `doc/`；`pride@whu.edu.cn`。

## 8. 检查清单

1. `pdp3 -V` 符合预期；`which pdp3` 正确；`bc` 可用。  
2. OBS 已 QC；目标频点存在。  
3. 产品可下载或离线齐全。  
4. example 或短时段冒烟通过。  
5. 固定 + 浮点对照；`pos_`/`ztd_` 非空并抽查头。  
6. 磁暴日准备 ROTI 图。  
7. 移交：`pos_`/`ztd_`/`amb_` + 完整命令 + 版本 + 产品日标识。  
8. 冲突时：**`pdp3 -H` > 官方 PDF > 本文**。

## 附录 · 场景卡片

```bash
pdp3 -m S -c 10 SITE0010.24o
pdp3 -m S -sys G -frq "G12" SITE0010.24o
pdp3 -m S -z S -p V3 SITE0010.24o
pdp3 -m P300 0.001 SITE0010.24o
pdp3 -m S -v SITE0010.24o 2> run.verbose.log
```

| 日志关键字 | 处置 |
| --- | --- |
| `/root` install | 换用户 |
| `invalid cutoff elevation` | 装 bc |
| `time span too long` | 缩短 `-s/-e` |
| `PrepareProducts` / TLS / 404 | 手投产品 / `-wcc` / 换镜像 |
| OSB unavailable | 改 `-frq` |
| `processing failed` | 向上找第一条 `error:` |

## 相关

[README](./README.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [rtklib](./rtklib.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md) · [09](../tutorials/09-dcb-biases-deep.md)
