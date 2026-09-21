# PRIDE-PPPAR · 多系统 PPP-AR 操作手册

目录：[`PROJECTS.json` → `PRIDE-PPPAR`](../../PROJECTS.json) · 上游 <https://github.com/PrideLab/PRIDE-PPPAR> · 支持/培训 <http://pride.apm.ac.cn> · 产品（以 README 为准）`ftps://bdspride.com/wum/` · GPL-3.0

> 面向需要 **发表级坐标 / ZTD / PPP-AR 固定率** 的岗位。默认入口命令为 `pdp3`。本文依据上游 README（常见 3.2.x，例如 3.2.11）与 `pdp3 -H` 整理；若本地帮助不一致，**以当前上游文档与本机 `-H` 为准**。

## 1. 用途与边界

### 1.1 一句话

PRIDE PPP-AR（武汉大学 GNSS 中心 Pride 实验室）是开源 **多 GNSS 精密单点定位 + 模糊度固定** 软件包。主流程脚本 `pdp3` 自动下载/组织精密产品并调用内部 Fortran 模块完成编辑、最小二乘与 AR。

### 1.2 能力清单（3.2 系）

- 系统：GPS / GLONASS / Galileo / BDS-2/3 / QZSS
- 全频点双频无电离层组合上的 PPP-AR（`-frq` 选频率）
- 高动态 / 高采样（文档称最高约 50 Hz）
- LEO 运动学定轨（`-m L`）
- 多日连续解（文档称最长约 108 天 @30 s，跨日整数约束减轻天界跳）
- 二阶电离层（CODE GIM）、VMF1/VMF3 对流层、MHM 多路径、AI 模糊度检验（默认）
- 产品：WUM0MGXRAP / RTS；可用 `-wcc` 走 Wuhan Combination Center 组合产品（以 `-H` 为准）

### 1.3 应该用

- 静态站坐标、地壳运动、测站速度场预处理
- ZTD/梯度时间序列（气象/大气水汽相关）
- 评估模糊度固定率、对照浮点解（`-f`）
- 磁暴日看「固定率崩了没有」——与 ROTI 产品对照（本工具不产出 ROTI）

### 1.4 不应该用

- 生产 STEC/vTEC/ROTI/S4 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
- 实时多用户 NTRIP 播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- 快速 RTK 基线（短基线固定）→ [rtklib](./rtklib.md) 往往更直接
- RINEX 格式清洗主工具 → [gfzrnx](./gfzrnx.md)（PRIDE 多日场景常**依赖**它）

### 1.5 电离层相关边界

- 默认用双频无电离层组合削弱一阶电离层
- `-hion` 可启用二阶项（需 GIM）——仍是**改正**，不是 TEC 反演产品
- `res_` 残差文件含多误差源，**不要**直接当 STEC 发布

### 1.6 依赖产品

- WUM 全频点轨道/钟差/相位偏差/ERP/四元数等（命名 WUM0MGXRAP / RTS）
- ANTEX、潮汐、leap second、sat_parameters 等 table 文件
- 广播星历（离线模式需自备）
- 地址以 GitHub README 当前行为准（历史上有过 FTP 变更）


## 2. 多平台安装

### 2.1 前置软件

| 组件 | 用途 | 备注 |
| --- | --- | --- |
| bash | 跑 `pdp3`/`install.sh` | macOS 用系统 bash/zsh 均可调用脚本 |
| make + gcc/gfortran | 编译 Fortran/C | **必需** |
| wget 或 curl | 拉产品 | 脚本内有回退逻辑（以版本为准） |
| python3 | 部分脚本/绘图 | 不用绘图可弱化 |
| gfzrnx | 多日拼接等 | 不装则相关功能受限 |

### 2.2 Linux 安装主线

```bash
# Debian/Ubuntu 示例
sudo apt update
sudo apt install -y build-essential gfortran make wget curl git python3

# 不要用 root 家目录安装：install.sh 拒绝 /root*
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh
# 按提示选择是否跑 example/test.sh（强烈建议首次选 Y）

# 安装位置
ls ~/.PRIDE_PPPAR_BIN | head
echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.bashrc
source ~/.bashrc
pdp3 -V
pdp3 -H | head -n 40
```

**期望：** 打印版本号（如 `3.2.11`）；`-H` 显示 `Usage: pdp3 [options] <obs-file>`；`~/.PRIDE_PPPAR_BIN` 含 `pdp3`、`lsq`、`tedit`、`arsig` 等。

### 2.3 macOS

```bash
# 需 gfortran（可用 brew 或专用安装包，以当前环境为准）
brew install gcc wget python3   # gcc 公式通常带 gfortran
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh
# install.sh 会尝试写入 ~/.bash_profile；zsh 用户请同步：
echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.zshrc
source ~/.zshrc
pdp3 -V
```

*注意：* 2026-08 上游曾修过 macOS BSD `sed` 导致的 shebang 替换崩溃——请用较新 tag/master。

### 2.4 Windows

- 上游提供 Windows / GUI 相关说明与产品下载地址更新记录——**以当前仓库 README/GUI 包为准**
- 科研批处理更推荐 WSL2：在 WSL 内按 Linux 主线安装
- 路径避免空格与非 ASCII；OBS 放到 WSL 文件系统侧（`~/data`）而非 `/mnt/c/...` 慢路径

### 2.5 安装 gfzrnx（多日强烈建议）

```bash
# 见 gfzrnx.md：下载后改名为 gfzrnx 并入 PATH
which gfzrnx || echo "WARN: gfzrnx missing — multi-day splice may fail"
```

### 2.6 离线 / 缓存相关环境语义

- `pdp3.sh` 顶部只读变量含 `OFFLINE` / `USECACHE` / `USERTS`（源码默认常见 OFFLINE=NO, USECACHE=YES）
- 改这些变量属于高级维护——普通用户优先用命令行与 config；不确定则保持默认并以手册为准

### 2.7 验收

| 项 | 命令 | 通过 |
| --- | --- | --- |
| 版本 | `pdp3 -V` | 打印 3.2.x |
| 帮助 | `pdp3 -H` | 含 `-m/-sys/-frq` |
| example | 安装时 test.sh | 退出 0，生成结果文件 |
| PATH | `which pdp3` | 指向 `~/.PRIDE_PPPAR_BIN` |


## 3. 完整逐步命令与期望输出

### 3.0 目录与配置准备

```bash
mkdir -p ~/pride_work && cd ~/pride_work
# 将 RINEX OBS 放到此项目目录或子目录
# 复制配置模板（路径以安装仓为准）
cp ~/.PRIDE_PPPAR_BIN/config_template ./config_site
# 或从源码树：
# cp /path/to/PRIDE-PPPAR/table/config_template ./config_site
```

### 3.1 跑官方 example（第一次必做）

```bash
cd /path/to/PRIDE-PPPAR/example
bash test.sh
# 或安装脚本结束时选 Y
```

**期望：** 在示例年/年积日子目录生成 `kin_`/`pos_`/`ztd_`/`res_`/`amb_` 等（前缀以版本为准）；终端无红色 `error:` 收尾。

### 3.2 单日静态 PPP-AR（联网自动下产品）

```bash
cd ~/pride_work
# 假设观测为 RINEX2 日文件
pdp3 -m S SITE0010.24o
```

**期望终端片段：**

```text
:: Processing time range: 2024-01-01 00:00:00 <==> 2024-01-01 23:59:30
:: Processing interval: 30
:: Site name: SITE
:: Positioning mode: S
:: AR switch: A
:: Frequency combination: ...
:: RINEX observation file: /home/you/pride_work/SITE0010.24o
```

**期望产物路径：** `~/pride_work/2024/001/`（年/年积日）；内含定位与对流层序列。

### 3.3 浮点对照解

```bash
pdp3 -m S -f SITE0010.24o
# 比较固定解与浮点解坐标差、残差 RMS
```

### 3.4 动态模式

```bash
pdp3 -m K ROVE0010.24o
# 高动态且数据差：加 -l（loose-edit）关闭严格编辑
pdp3 -m K -l ROVE0010.24o
```

### 3.5 多日处理

```bash
# 从 2024/001 到 2024/003（语法以 -H 为准）
pdp3 -s 2024/1 -e 2024/3 -m S SITE0010.24o
# 工作目录将类似 2024/001-003
# 需要 gfzrnx 准备跨日观测连续性
```

### 3.6 系统与频率选择

```bash
# 只要 GPS+Galileo+BDS-3
pdp3 -m S -sys GE3 -frq "G12 E15 C26" SITE0010.24o

# 默认频率串示例（-H）："G12 R12 E15 C26 J12"
# BDS：2=B1I, 6=B3I, 1=B1C, 5=B2a 等——以 -H 表格为准
```

### 3.7 时间窗、采样、站名

```bash
pdp3 -m S \
  -s 2024/001 00:00:00 -e 2024/001 12:00:00 \
  -i 30 -n SITE \
  SITE0010.24o

# 非标准时间标签文件可试 -twnd（时间窗容差）
# pdp3 -twnd 0.05 ...
```

### 3.8 对流层 / 钟差 / 潮汐 / 二阶电离层

```bash
# ZTD 模型 -z ；HTG -h ；接收机钟 -r ；ISB -isb ；映射函数 -p
pdp3 -m S -z S -h P60 -r STO -p V3 SITE0010.24o

# 二阶电离层
pdp3 -m S -hion SITE0010.24o

# 关掉某些潮汐改正 -toff（取值见 -H）
# pdp3 -m S -toff SOLID ...
```

### 3.9 MHM 多路径与 WCC 产品

```bash
# 多路径模型：需至少一恒星日量级的观测在同目录（各星座恒星日长度不同，见 -H）
pdp3 -m S -mp SITE0010.24o

# 使用 Wuhan Combination Center 产品
pdp3 -m S -wcc SITE0010.24o
```

### 3.10 自定义配置文件

```bash
cp ~/.PRIDE_PPPAR_BIN/config_template ./config_site
# 编辑关键项：
#   Frequency combination / Interval / Product directory
#   Strict editing / ZTD model / HTG model / Iono 2nd
#   Ambiguity duration / Cutoff elevation / Truncate at midnight
#   +GNSS satellites 列表中用 # 注释掉某 PRN
pdp3 -cfg ./config_site -m S SITE0010.24o
```

### 3.11 截断高程角与详细 AR 日志

```bash
pdp3 -m S -c 15 -v SITE0010.24o
```

### 3.12 离线模式操作要点

1. 按手册附录把 SP3/CLK/OSB/ERP/ORBEX/ANTEX/广播星历放到 Product/table 目录约定位置
2. 确认日期与站名文件齐全
3. 再调用 `pdp3`；若脚本仍尝试联网，检查 `OFFLINE` 与文档「非联网求解」章节（以当前手册 PDF 为准）

### 3.13 结果文件怎么验收

```bash
# 进入年积日目录
cd ~/pride_work/2024/001
ls -l
# 常见前缀（以版本为准）：
#   pos_  位置
#   kin_  动态轨迹
#   ztd_  对流层
#   res_  残差
#   amb_  模糊度相关
wc -l pos_* ztd_* 2>/dev/null | tail
head -n 30 pos_* | head
```

**成功判据：** 文件非空；时间戳覆盖任务时段；固定解模式下日志无大量 AR 失败且坐标跳动异常（静态站）。

### 3.14 与浮点/RTKLIB 交叉验证小流程

```bash
pdp3 -m S    SITE0010.24o   # AR on
pdp3 -m S -f SITE0010.24o   # float
# 另用 rtklib rnx2rtkp 做浮点 PPP 对照（见 rtklib.md）
```


## 4. 参数与文件字段表

### 4.1 `pdp3` 常用命令行选项

| 选项 | 含义 | 典型 |
| --- | --- | --- |
| `-m S/P/K/F/L` | 静态/分段/动态/固定/LEO | `-m S` |
| `-f` | 关闭 AR（浮点） | 对照实验 |
| `-sys` | 系统子集 `GREC23J` | `GE3` |
| `-frq` | 各系统频率对 | `"G12 E15 C26"` |
| `-cfg` | 配置文件 | `./config_site` |
| `-s`/`-e` | 起止日期时间 | `2024/001` |
| `-n` | 4 字符站名 | `SITE` |
| `-i` | 处理间隔秒 | `30` |
| `-c` | 截止高度角° | `10`/`15` |
| `-l` | 宽松编辑 | 高动态 |
| `-hion` | 二阶电离层 | 需 GIM |
| `-mp` | MHM 多路径 | 需多日数据 |
| `-wcc` | WCC 组合产品 | RAP 缺失时 |
| `-z`/`-h`/`-r` | ZTD/HTG/钟差模型 | 见 `-H` |
| `-p` | 映射函数 G/N/V1/V3 | `V3` |
| `-v` | 详细 AR/LSQ 输出 | 排障 |
| `-twnd` | 非标准时间窗 | 怪 RINEX |

### 4.2 定位模式速查

| 码 | 模式 | 备注 |
| --- | --- | --- |
| S | Static | 连续跟踪站默认首选 |
| P | Piece-wise | 可带长度与约束，默认常 P300 0.001 |
| K | Kinematic | 流动站；默认模式之一 |
| F | Fixed | 坐标固定估大气等 |
| L | LEO | 需姿态/专用 table 脚本 |

### 4.3 频率编号（摘自 `-H`，以本机为准）

| 系统 | 1 | 2 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- |
| G | L1 | L2 | L5 | — | — | — |
| R | L1 | L2 | — | — | — | — |
| E | E1 | — | E5a | E6 | E5b | E5 |
| C | B1C | B1I | B2a | B3I | B2b | B2 |
| J | L1 | L2 | L5 | L6 | — | — |

### 4.4 `config_template` 关键字段

| 字段 | 作用 |
| --- | --- |
| Frequency combination | 无电离层频率对 |
| Interval | 处理采样 |
| Product directory | 精密产品根目录 |
| Strict editing | 高动态差数据改 NO |
| RCK/ISB/ZTD/HTG model | 随机模型 |
| Iono 2nd | 二阶电离层 YES/NO |
| Tides | SOLID/OCEAN/POLE 或 NON |
| Multipath | MHM YES/NO |
| Ambiguity duration | 可固定弧段最短时间 |
| AI Ambiguity validation | SVM 检验开关 |
| Cutoff elevation | AR 用截止角 |
| Truncate at midnight | 是否午夜截断模糊度 |
| +GNSS satellites | PRN 方差表；`#` 禁用 |

### 4.5 结果文件（常见前缀，以版本为准）

| 前缀 | 内容 | 下游用途 |
| --- | --- | --- |
| `pos_` | 位置解 | 坐标时间序列 |
| `kin_` | 动态轨迹 | 可转 CSV（上游脚本） |
| `ztd_` | 对流层延迟 | 气象交叉 |
| `res_` | 残差 | QC；非 TEC 产品 |
| `amb_` | 模糊度 | 固定率分析 |

### 4.6 工作目录规则

- 单日：`项目目录/年/年积日/`
- 多日且 <108 天：`年/起始年积日-结束年积日/`
- ≥108 天：脚本报错拒绝


## 5. 接到电离层 / GNSS 哪一步

### 5.1 位置

- 前：数据 [data-access](../data-access.md) → 清洗 [gfzrnx](./gfzrnx.md) → QC [anubis](./anubis.md)
- 中：本工具出坐标/ZTD/固定率
- 旁路对照：浮点 PPP [rtklib](./rtklib.md)
- 电离层扰动对照：[ionomoni](./ionomoni.md) / [oasis-roti](./oasis-roti.md)
- 教程：[06 电离层与定位](../tutorials/06-iono-positioning.md)、[20 磁暴 TEC](../tutorials/20-storm-tec-analysis.md)、[09 DCB](../tutorials/09-dcb-biases-deep.md)

### 5.2 路径 D（目录推荐）：精密定位

1. 下载多系统 OBS + 确认 WUM 产品日期可用
2. `gfzrnx` 拼接/改名
3. `anubis` 粗看周跳
4. `pdp3 -m S` 与 `pdp3 -m S -f`
5. 磁暴日叠加 ROTI 图解释固定率

### 5.3 与 TEC 链的关系

TEC 链与 PPP 链**并行**：共用清洗后的 OBS，但产品目标不同。不要把 `res_` 接到 GIM 同化当 STEC。


## 6. 可操作坑（≥12）

1. **用 root 安装：** `install.sh` 拒绝 `/root*`。换普通用户。
2. **未装 gfortran：** `make` 失败。先 `gfortran --version`。
3. **example 没跑通就换站：** 先隔离环境/产品下载问题。
4. **产品 FTPS 失败：** 查防火墙、证书、README 是否改址；试 `-wcc`；或改离线投放。
5. **缺 gfzrnx 做多日：** 跨日拼接失败。按 [gfzrnx](./gfzrnx.md) 安装并改名。
6. **频率在站上不存在：** `-frq` 选了 L5 但接收机无 L5 → 大量缺测。先 `gfzrnx -stk_obs`。
7. **RINEX4/新 BDS 配置：** 用最新 3.2.x；旧版读新头会挂。
8. **把截止角调太高：** `-c 30` 在高纬冬季可见卫星不足，AR 崩。
9. **严格编辑杀高动态：** 车载/飞机加 `-l` 或配置 `Strict editing=NO`。
10. **MHM 数据不足：** `-mp` 需要恒星日量级多文件同目录，缺一天会建模失败。
11. **午夜截断设置不当：** 多日连续性差；阅读 `Truncate at midnight` 与 DOCB 说明。
12. **误读残差为 TEC：** 残差含轨道钟差对流层多路径。TEC 走专用软件。
13. **PATH 未生效：** 新开终端或 `source ~/.bashrc`；`which pdp3` 检查。
14. **Windows 路径空格：** 在 WSL 使用 Linux 路径。
15. **AI 检验与旧论文设置不一致：** 3.2 默认机器学习检验；复现旧结果需对照 CHANGELOG/配置。
16. **时间戳非标准：** 试 `-twnd`；仍失败则先 `gfzrnx` 规范时间标签。


## 7. 同类怎么选

| 需求 | 优先 | 次选 |
| --- | --- | --- |
| 多系统 PPP-AR、ZTD 序列 | **PRIDE-PPPAR** | 其它学术 PPP-AR |
| 快速基线 RTK/单频玩具 | RTKLIB | PRIDE（杀鸡） |
| 只要浮点 PPP 验证 | RTKLIB 或 `pdp3 -f` | — |
| TEC/ROTI | pytecgg/oasis/ionomoni | 不要用 PRIDE |
| 实时校正流 | pygnssutils/BNC | PRIDE（后处理） |

### 7.1 文献与手册

- 软件论文：Geng et al., GPS Solutions, 2019（PRIDE PPP-AR）
- 仓库 `doc/PRIDE PPP-AR v3.2 manual-en.pdf`（及中文版）
- CHANGELOG.md 跟版本行为变更
- 联系：pride@whu.edu.cn；站点 pride.apm.ac.cn / pride.whu.edu.cn

### 7.2 每次任务检查清单

1. `pdp3 -V` 与预期版本一致
2. OBS 已 QC / 频率存在
3. 产品日期可下载或离线齐全
4. 先 example 或短时段冒烟
5. 固定+浮点对照
6. 结果目录非空并抽查 `pos_`/`ztd_`
7. 磁暴日准备 ROTI 对照图

## 8. 场景卡片

### 8.1 静态站一日快速

```bash
pdp3 -m S -c 10 SITE0010.24o
```

### 8.2 只评估 GPS AR

```bash
pdp3 -m S -sys G -frq "G12" SITE0010.24o
```

### 8.3 对流层 STO + VMF3

```bash
pdp3 -m S -z S -p V3 SITE0010.24o
```

### 8.4 LEO（需按 table 脚本准备）

```bash
pdp3 -m L -cfg config_leo LEO0010.24o
```

### 8.5 分段坐标 P 模式

```bash
pdp3 -m P300 0.001 SITE0010.24o
```

### 8.6 详细日志排障

```bash
pdp3 -m S -v SITE0010.24o 2> run.verbose.log
```

### 8.7 关闭宽巷 APC

```bash
pdp3 -m S -aoff SITE0010.24o
```

### 8.8 指定配置中的产品目录

```bash
sed -i 's|^Product directory.*|Product directory = /data/products|' config_site
pdp3 -cfg ./config_site -m S SITE0010.24o
```


## 9. 产品与 table 投放（离线提纲）

- 精密轨道/钟差/相位偏差：按日投放，命名跟随 WUM0MGX* 当前约定
- ERP、四元数、BIAS-SINEX（含 DOCB 块影响午夜重置）
- ANTEX：与观测天线名匹配
- oceanload / 固体潮参数：缺站可走自计算选项（版本 ≥3.0 叙述）
- 广播星历 RINEX NAV 或 RINEX4

具体子目录文件名以 **v3.2 用户手册附录 A** 为准（本文不复制过时路径）。

### 9.1 联网失败时的最小排障序

1. `ping`/`curl -I` 测试产品主机可达性（主机以 README 为准）
2. 看 `pdp3` 日志里哪一类文件 404
3. 手动下载该日文件放入 Product directory
4. 重跑同一命令（打开缓存时可能直接命中）

### 9.2 固定率低的分析序

1. 看 anubis 周跳与多路径
2. 查 ROTI/S4 是否暴涨
3. 降系统到 G 或 GE 对比
4. 浮点解是否也跳——轨道/钟差问题
5. 放宽/检查 OSB 是否缺某频点


## 10. 附录：与目录教程映射

| 教程 | 动作 |
| --- | --- |
| 06 定位 | 主案例跑 `pdp3 -m S` |
| 09 DCB | 理解 OSB/相位偏差产品为何必需 |
| 14/20 空间天气 | 固定率 vs ROTI |
| 16 一日实践 | 可并行做浮点 PPP 对照坐标 |

终注：选项表若与 `pdp3 -H` 冲突，**以当前上游与本机帮助为准**。

## 11. 端到端操作剧本（可直接照做）

### 11.1 剧本 A：连续跟踪站一日静态 PPP-AR

1. 确认 OBS 为完整 UTC 日、双频以上、采样 ≤30 s。  
2. `gfzrnx -finp RAW.rnx -fout SITE0010.24o -chk -smp 30 -kv -f`。  
3. `cd ~/pride_work && pdp3 -m S -c 10 SITE0010.24o`。  
4. 检查 `YYYY/DOY/pos_*` 与 `ztd_*` 非空。  
5. 再跑 `pdp3 -m S -f SITE0010.24o`，对比坐标差。  

**期望：** 静态站固定解坐标日内稳定（cm 级跳动视环境）；浮点解噪声更大。  
**失败：** 产品下载报错 → 换网络或 `-wcc`；无 `pos_` → 看终端 `error:` 行。

### 11.2 剧本 B：磁暴日固定率诊断

1. 选取 Dst 极小值日（教程 [20](../tutorials/20-storm-tec-analysis.md)）。  
2. 同站跑 `pdp3 -m S`（安静日）与磁暴日各一次。  
3. 并行用 [oasis-roti](./oasis-roti.md) 出 ROTI。  
4. 将 AR 成功率/模糊度重置次数与 ROTI 高峰时段对齐。  

**期望：** ROTI 高峰常伴随固定率下降或重初始化。  
**勿做：** 把 `res_` 当 STEC 曲线发表。

### 11.3 剧本 C：多系统频率实验

```bash
pdp3 -m S -sys G   -frq "G12"        SITE0010.24o
pdp3 -m S -sys GE  -frq "G12 E15"    SITE0010.24o
pdp3 -m S -sys GE3 -frq "G12 E15 C26" SITE0010.24o
```

**期望：** 卫星数↑通常有助于连续弧；若某频点缺 OSB，日志会提示，需改 `-frq`。

### 11.4 剧本 D：车载动态

```bash
pdp3 -m K -l -c 10 ROVE0010.24o
```

**期望：** `kin_` 轨迹连续；严格编辑导致大量删数据时，`-l` 后点数回升。  
**坑：** 无高采样 IMU 融合——本软件不是组合导航全方案。

### 11.5 剧本 E：ZTD 序列给气象对照

```bash
pdp3 -m S -z S -h P60 -p V3 SITE0010.24o
# 提取 ztd_ 与探空/辐射计对照（自备脚本）
```

**期望：** `ztd_` 平滑、无整米级跳变；天界处检查是否启用跨日产品对齐。

## 12. 日志关键字与处置

| 日志关键词（示意） | 处置 |
|---|---|
| `unable to install ... /root` | 换普通用户重装 |
| `time span too long` | 缩短 `-s/-e` |
| `preparing mhm model failed` | 补齐恒星日观测或去掉 `-mp` |
| `processing failed` | 向上翻看第一个 `error:` |
| 产品 `404` / `download` 失败 | 检查 FTPS 地址与日期是否已发布 |
| 频率/OSB unavailable | 改 `-frq` 或等对应偏差产品 |
| `no such directory` | `mkdir` 项目目录并在其下启动 `pdp3` |

## 13. 配置文件编辑实例

```bash
cp ~/.PRIDE_PPPAR_BIN/config_template ./config_ops
```

建议逐项改（值以手册合法枚举为准）：

```text
Interval               = 30
Strict editing         = YES
ZTD model              = STO
HTG model              = PWC:60
Iono 2nd               = NO
Multipath              = NO
Ambiguity duration     = 600
Cutoff elevation       = 10
Truncate at midnight   = NO
Verbose output         = YES
```

禁用问题星：

```text
#G04   1
```

然后：

```bash
pdp3 -cfg ./config_ops -m S SITE0010.24o
```

## 14. 与 GFZRNX / Anubis 的接口契约

| 前置产出 | 要求 |
|---|---|
| OBS | 头完整；MARKER 4 字符可用；近似坐标非零 |
| 采样 | 与 `-i` 一致或更密 |
| 命名 | 多日场景优先 RINEX3 长名 |
| Anubis 报告 | 无大段空洞、无异常钟跳再进 `pdp3` |

```bash
# 契约检查最小集
gfzrnx -finp SITE0010.24o -meta basic:txt
gfzrnx -finp SITE0010.24o -stk_obs | head
```

## 15. 结果后处理提示

```bash
cd ~/pride_work/2024/001
# 看位置文件头（天线、频率、模式等，3.x 起更丰富）
head -n 40 pos_* 
# 统计行数
wc -l kin_* pos_* ztd_* res_* 2>/dev/null
# 上游可能提供 kin→csv 的 python 脚本（以仓库 scripts/ 为准）
ls ~/.PRIDE_PPPAR_BIN/*.py
```

**移交物建议：** `pos_`/`ztd_`/`amb_` + 完整命令行 + `pdp3 -V` 输出 + 产品日标识。

## 16. 安全与合规

- 不要把产品镜像账号写进公开仓库。  
- GPL-3.0：衍生发行注意义务。  
- 引用软件论文与使用的产品（WUM/WCC）出处。  

## 17. 快速失败矩阵

| 现象 | 最先查 |
|---|---|
| 命令找不到 | PATH / 是否 source bashrc |
| 编译失败 | gfortran 版本与依赖 |
| 秒退 | OBS 路径、权限、时间跨度 |
| 长时间无进度 | 产品下载卡住；抓包或手动镜像 |
| 坐标炸 | 天线高、ANTEX、近似坐标、频点 |
| 固定率 0 | `-f` 是否误开；OSB；电离层扰动 |

终注：本手册不替代官方 PDF；**以当前上游文档与 `pdp3 -H` 为准**。