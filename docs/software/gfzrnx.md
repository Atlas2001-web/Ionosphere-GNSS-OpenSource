# GFZRNX · RINEX 检查 / 转换 / 拼接操作手册

目录：[`PROJECTS.json` → `GFZRNX`](../../PROJECTS.json) · 产品页 <https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox> · 用户手册 <https://gnss.git-pages.gfz-potsdam.de/gfzrnx/> · 下载/许可 <https://gnss.gfz-potsdam.de/services/gfzrnx>

> 本文面向电离层/GNSS 流水线中的 **RINEX 预处理岗**。参数以本机 `gfzrnx -h` 与上游 Users Guide 为准；版本号常见为 2.2.x（以当前上游文档为准）。路径均为占位符。

## 1. 用途与边界

### 1.1 一句话

GFZRNX 是德国地学研究中心（GFZ）发布的 **命令行 RINEX 工具箱**：检查、修复、版本转换（2↔3↔4）、拼接/切分、抽稀、系统/观测量筛选、头编辑、元数据提取、统计与表格化输出。无 GUI。

### 1.2 支持的数据类型

- 观测文件 OBS（`.YYo` / `*_MO.rnx` 等）
- 导航文件 NAV（单系统或 mixed）
- 气象文件 MET
- 输入可覆盖 RINEX 2.x / 3.x / 4.x；输出主版本通常落到该主版本的最新标准号（手册表：2→2.11、3→3.05、4→4.01，以当前上游为准）

### 1.3 应该用

- 进 [georinex](./georinex.md) / [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md) 前：统一采样率、系统、观测类型
- 小时文件拼日文件；日文件按小时切分；1 Hz → 30 s 抽稀
- RINEX-2 老站网文件改名为 RINEX-3/4 长名，便于流水线归档
- 批量头字段修补（`-crux` / `-cx_updins`）与元数据抽取（`-meta`）
- 给 [anubis](./anubis.md) / [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md) 喂「干净、命名规范」的 OBS

### 1.4 不应该用

- 算 STEC/vTEC/ROTI/闪烁指数 → 用下游专用工具
- 写站网 QC 报表（多站图表）→ [anubis](./anubis.md)
- 实时 NTRIP/串口探活 → [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md)
- 精密定位 PPP-AR → [pride-pppar](./pride-pppar.md)
- 当 TEQC 的「万能 QC GUI」用——本工具是批处理 CLI，不是交互分析平台

### 1.5 许可边界（必读）

- 科学伙伴许可：科研/教学、非例行场景常可免费——须在下载页登记
- 商业许可：例行生产、业务化流水线需收费许可
- **以当前 EULA / 下载页为准**；本手册不解释法律条款
- 可执行文件名因平台而异：`gfzrnx_lx`、`gfzrnx_osx`、`gfzrnx.exe` 等；下文统一写 `gfzrnx`

### 1.6 与本仓库其它软件的分工

| 工具 | 角色 | 相对 GFZRNX |
| --- | --- | --- |
| georinex | 读 RINEX→xarray | GFZRNX 清洗后交给它 |
| anubis | 站网 QC 报表 | 可并行；GFZRNX 偏格式/切片 |
| rtklib | RTK/PPP 引擎 | 吃处理后的 OBS/NAV |
| pride-pppar | PPP-AR | 常依赖 gfzrnx 做多日拼接 |
| pytecgg | 校准 TEC | OBS 须先统一采样与双频类型 |


## 2. 多平台安装

### 2.1 前置条件

- 已在 <https://gnss.gfz-potsdam.de/services/gfzrnx> 完成许可申请并下载对应平台二进制
- Linux x86_64 / Windows / macOS / SunOS 均有发布包（以下载页列表为准）
- 无需编译源码（闭源二进制分发）；需要写权限的临时目录

### 2.2 Linux（推荐主线）

1. 下载例如 `gfzrnx_*_lx*` 压缩包或直接可执行文件（文件名以当前下载页为准）
2. 解压并重命名为 `gfzrnx`，赋予执行位
3. 放到 `~/bin` 或 `/usr/local/bin`，确保在 `PATH` 中
4. 冒烟：`gfzrnx -h | head`

```bash
# 示例：假设已下载到 ~/Downloads
mkdir -p ~/bin
cd ~/Downloads
# 实际压缩包名以下载页为准
tar -xf gfzrnx_*.tar.gz   # 若是 tar；或直接用已解压文件
chmod +x gfzrnx_lx        # 或实际可执行文件名
mv gfzrnx_lx ~/bin/gfzrnx
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
gfzrnx -h | head -n 20
which gfzrnx
```

**期望输出：** 打印 `***** USAGE: gfzrnx` 及 `-finp`/`-fout` 等选项列表；`which` 指向 `~/bin/gfzrnx`。

### 2.3 macOS

1. 下载 `*_osx*` 或 Apple Silicon 对应包（以当前上游为准）
2. 若 Gatekeeper 拦截：系统设置 → 隐私与安全性 → 仍要打开；或 `xattr -d com.apple.quarantine gfzrnx`
3. 同样放入 `~/bin` 并写入 `~/.zshrc` 的 `PATH`

```bash
chmod +x gfzrnx_osx
mv gfzrnx_osx ~/bin/gfzrnx
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
gfzrnx -h | head
```

### 2.4 Windows

1. 下载 `gfzrnx.exe`（或带版本后缀的 exe）
2. 放到如 `C:\Tools\gfzrnx\`，将该目录加入用户 PATH
3. 在 **cmd.exe** 或 PowerShell 中运行 `gfzrnx.exe -h`
4. 批处理示例见上游 Usage 页（循环 `-smp 30`）

```bat
@echo off
REM sample_30s.bat — 路径按本机修改
gfzrnx.exe -finp C:\data\XXXX0010.24o -fout C:\data_30\XXXX0010.24o -smp 30 -f
```

### 2.5 临时目录与环境

- 大文件拼接会占 RAM；磁盘临时区需足够空间
- 上游手册有 Temporary Directory 说明——若处理失败且日志提临时文件，检查 `TMPDIR`/`TEMP`
- 容器内：把二进制拷进镜像并 `chmod +x`；注意许可是否允许容器化例行跑批

### 2.6 与 PRIDE-PPPAR 联用时的命名约定

- PRIDE 多日处理常要求 PATH 中可直接调用名为 `gfzrnx` 的命令
- 下载后务必 `mv ... gfzrnx`（去掉平台后缀），否则 `pdp3` 可能找不到

### 2.7 安装验收清单

| 检查项 | 命令 | 通过标准 |
| --- | --- | --- |
| 可执行 | `which gfzrnx` | 非空路径 |
| 帮助 | `gfzrnx -h` | 含 `-finp`/`-fout` |
| 版本提示 | 帮助末尾 VERSION 行 | 与下载包一致 |
| 写权限 | 对测试目录 `touch` | 可创建输出 |


## 3. 完整逐步命令与期望输出

### 3.0 工作目录约定

```bash
mkdir -p ~/iono_ops/{raw,work,out,log}
cd ~/iono_ops
# raw/  : 原始 RINEX（可含 .gz / Hatanaka .YYd）
# work/ : 解压、中间件
# out/  : 交给下游的最终 OBS/NAV
# log/  : -errlog 与统计
```

### 3.1 解压与 Hatanaka（若需要）

GFZRNX 本身不是 Hatanaka 编解码器。先用 `CRX2RNX`/`RNX2CRX`（RNXCMP）或 `gunzip`：

```bash
# gzip
gunzip -k raw/SITE0010.24o.gz   # -k 保留压缩包（GNU gzip）

# Hatanaka → 普通 OBS（CRX2RNX 需已安装）
CRX2RNX raw/SITE0010.24d - > work/SITE0010.24o

# 管道直喂 gfzrnx（STDIN 仅单文件）
crx2rnx raw/SITE0010.24d - | gfzrnx -fout work/SITE0010_chk.24o -chk -kv
```

**期望：** `work/SITE0010.24o` 以 `     3.05           OBSERVATION DATA` 或 `     2.11` 类头行开头。

### 3.2 正式检查写出（`-chk`）

```bash
gfzrnx -finp work/SITE0010.24o \
  -fout out/SITE0010_chk.24o \
  -chk -kv \
  -errlog log/SITE0010_chk.errlog
```

**期望 STDERR / errlog 样例（结构示意）：**

```text
DATE/TIME     | C | EPOCH/FILE  | SITE | T | MESSAGE
--------------+---+-------------+------+---+------------------------------------------------
2024-01-01 .. | N | .. 00:00:00 | SITE | O | file duration set to 86400 s
2024-01-01 .. | W | .. 00:00:00 | SITE | O | no MARKER NAME in header / taken from file name
```

*判据：* 无 `E`(Error) 级则通常可进入下一步；`W` 需人工读一遍（缺 MARKER、缺接收机类型等）。

### 3.3 抽稀到 30 s（电离层常用）

```bash
gfzrnx -finp out/SITE0010_chk.24o \
  -fout out/SITE0010_30s.24o \
  -smp 30 -kv -f \
  -errlog log/SITE0010_smp.errlog

# 抽稀时若需把 LLI 挪到采样历元：
# gfzrnx ... -smp 30 -smp_lli_shift
wc -l out/SITE0010_30s.24o
```

**期望：** 文件显著变小；头中 INTERVAL 相关信息与 30 一致（视输入头是否写入）。用下游 `georinex` 读入后 `ds.time.diff` 众数约为 30 s。

### 3.4 小时文件拼日文件

```bash
# bash 通配：a..x = 24 个小时文件（RINEX-2 惯例）
gfzrnx -finp work/SITE001{a..x}.24o \
  -fout out/SITE0010.24o \
  -kv -f \
  -errlog log/SITE0010_splice.errlog

# 内存紧张：
gfzrnx -finp work/SITE001{a..x}.24o -fout out/SITE0010.24o -kv -f -splice_direct

# 尝试加速追加（秒数为各分片标称时长，如 3600）：
# gfzrnx ... -try_append 3600
```

**期望：** 单日文件；日志中 notice 提示 duration≈86400；用 `-stk_epo 3600` 看 24 行非空。

### 3.5 按系统与观测类型筛选（双频 TEC 前置）

```bash
# 只要 GPS L1C/L2W + 对应码（按站实际信号改）
gfzrnx -finp out/SITE0010_30s.24o \
  -fout out/SITE0010_G_L1L2.24o \
  -satsys G \
  -ot L1C,L2W,C1C,C2W \
  -kv -f

# 多系统：GPS+Galileo+BDS
gfzrnx -finp out/SITE0010_30s.24o \
  -fout out/SITE0010_GEC.24o \
  -satsys GEC \
  -ot L1C,L2W,C1C,C2W+E:L1C,L5Q,C1C,C5Q+C:L2I,L6I,C2I,C6I \
  -kv -f
```

**期望：** 头 `# / TYPES OF OBSERV` 或 `SYS / # / OBS TYPES` 仅含所选类型；空类型默认剔除（除非 `-kaot`）。

### 3.6 RINEX-2 → RINEX-3 并自动命名

```bash
# MARKER 已是 9 字符风格时：
gfzrnx -finp out/SITE0010_G_L1L2.24o -fout out/::RX3:: -vo 3 -f

# 仅有 4 字符站名时，补 monument/receiver/ISO：
gfzrnx -finp out/SITE0010_G_L1L2.24o \
  -fout out/::RX3::00,CHN \
  -vo 3 -sei in -f

# 批量 4→9 映射文件：
# gfzrnx -finp ... -fout out/::RX3:: -4to9 four2nine.conf -vo 3
```

**期望文件名样例：** `SITE00CHN_R_20240010000_01D_30S_GO.rnx`（真实历元/时长决定字段；`-sei in` 用标称日界）。

### 3.7 版本强制与标准符合输出

```bash
# 保持输入主版本：-kv
# 强制主版本 3：-vo 3
# 强制「完全标准符合」输出：-vosc 3
gfzrnx -finp work/old.12o -fout out/old_rx3.rnx -vosc 3 -f
```

### 3.8 切分（split）

```bash
# 切成 1 小时片；fout 必须用 ::RX2:: 或 ::RX3::；n 须为 60 的倍数
gfzrnx -finp out/SITE0010.24o \
  -fout out/::RX3::00,CHN \
  -split 3600 -vo 3 -f
```

**期望：** `out/` 下约 24 个小时文件；每个时长字段为 `01H`。

### 3.9 统计与可用性时间图

```bash
gfzrnx -finp out/SITE0010_30s.24o -stk_obs > log/SITE0010_stk_obs.txt
gfzrnx -finp out/SITE0010_30s.24o -stk_epo 3600 > log/SITE0010_stk_epo.txt
# 只要统计不要 RINEX 体：-stk_only
head -n 40 log/SITE0010_stk_obs.txt
```

**期望：** 各系统/PRN/观测类型计数表；`stk_epo` 为 ASCII 时间可用性图。

### 3.10 元数据提取

```bash
gfzrnx -finp out/SITE0010_30s.24o -meta basic:txt  > log/SITE0010_meta_basic.txt
gfzrnx -finp out/SITE0010_30s.24o -meta full:json > log/SITE0010_meta_full.json
```

### 3.11 头编辑（crux）

```bash
# 仅改头：-hded + -crux
cat > work/site.crux <<'EOF'
# 具体语法以 Users Guide「crux」章节为准；以下为结构示意
# SITE update MARKER NAME / REC / ANT ...
EOF
gfzrnx -finp out/SITE0010_30s.24o -fout out/SITE0010_hdr.24o \
  -crux work/site.crux -hded -kv -f
# 命令行快速补丁：
# gfzrnx ... -cx_updins "....." 
```

### 3.12 文件比较与表格化

```bash
# 两文件同主版本比较
gfzrnx -finp out/A.rnx out/B.rnx -fdiff

# 表格输出（便于 awk/pandas）
gfzrnx -finp out/SITE0010_30s.24o -tab -tab_sep "," > log/SITE0010_tab.csv
```

### 3.13 导航文件：混合命名与筛选

```bash
# 多 NAV 拼接为 mixed，并强制 _MN 命名
gfzrnx -finp work/*_GN.rnx work/*_EN.rnx \
  -fout out/::RX3::00,CHN -nav_mixed -vo 3 -f

# 只要最新星历记录：
# gfzrnx -finp brdc.rnx -fout out/brdc_latest.rnx -nav_latest -kv
```

### 3.14 批处理骨架（GNU parallel 可选）

```bash
ls raw/*.24o | while read -r f; do
  b=$(basename "$f" .24o)
  gfzrnx -finp "$f" -fout "out/${b}_30s.24o" -smp 30 -chk -kv -f \
    -errlog "log/${b}.errlog" || echo "FAIL $b" >> log/fail.list
done
```

### 3.15 成功判据汇总

| 步骤 | 成功信号 | 失败信号 |
| --- | --- | --- |
| 检查 | 写出非空；errlog 无 E | 空文件 / Error 行 |
| 抽稀 | 体积↓；历元间隔≈目标 | 仍为 1 Hz |
| 拼接 | 时长≈86400 s | 缺小时、间隙大 |
| 筛类型 | 头类型列表匹配 | 下游缺 L2 |
| 改名 | 长名符合 RINEX3 | 仍用短名导致归档乱 |


## 4. 参数与文件字段表

### 4.1 核心 I/O 参数

| 参数 | 含义 | 注意 |
| --- | --- | --- |
| `-finp` | 输入文件列表 | 多文件=拼接；STDIN 仅单文件 |
| `-fout` | 输出路径 | `::RX2::`/`::RX3::`/`::RX4::` 自动命名 |
| `-f` | 允许覆盖 | 默认不覆盖已存在文件 |
| `-q` | 安静模式 | 少打日志 |
| `-errlog` | 日志追加到文件 | 默认仍可能打 STDERR |
| `-direct` | OBS 逐历元直通 | 无头统计、省内存 |

### 4.2 采样 / 时间窗

| 参数 | 含义 | 典型值 |
| --- | --- | --- |
| `-smp` | 抽稀间隔（秒） | 30（电离层）/ 1 / 300 |
| `-smp_nom` | 自动命名用标称采样 | 与 `-smp` 区分 |
| `-smp_lli_shift` | 抽稀时平移 LLI | 相位连续性敏感场景 |
| `-d` / `--duration` | 输出标称时长（秒） | 86400 / 3600 / 900 |
| `-epo_beg` | 首历元 | `2014-04-06_12:30:00` 等 |
| `-sei in|out` | 严格按文件名历元区间 | 名义改名必备 |
| `-split n` | 按 n 秒切开 | n 为 60 倍数 |

### 4.3 系统与观测

| 参数 | 含义 | 取值 |
| --- | --- | --- |
| `-satsys` | 保留系统 | `CEGIJRS` 字母子集 |
| `-ot` / `--obs_types` | 观测类型模式 | `G:L1C,L2W+E:...` |
| `-ots` | 输出类型排序 | 如 `CPLDS:frqasc` |
| `-prn` / `-no_prn` | PRN 白/黑名单 | `G1-32,E14` |
| `-kaot` | 保留全空类型 | 调试时用 |
| `-rsot n` | 删稀疏类型 | n=相对中位数百分比阈值 |

### 4.4 版本与命名

| 参数 | 含义 | 备注 |
| --- | --- | --- |
| `-vo` / `-vosc` | 输出主版本 / 标准符合 | 2|3|4 |
| `-kv` | 保持输入主版本号 | 预处理常开 |
| `-site` | 强制站名 | 头缺 MARKER 时 |
| `-4to9` | 4 字符→9 字符表 | 网络批量改名 |
| `-nomren23` | 快速打印 RINEX3 名 | 只 STDOUT 名字 |
| `-ant_rename` | 历史天线名→IGS 名 | 头规范化 |

### 4.5 统计 / 元数据 / 比较

| 参数 | 输出 |
| --- | --- |
| `-stk_obs` / `-stk_only` | 观测统计 |
| `-stk_epo n[:list]` | 可用性 ASCII 图 |
| `-meta type[:fmt]` | basic|full × json|xml|txt|dump |
| `-fdiff` | 两文件差分比较 |
| `-tab` (+ date/time/sep) | 表格化观测 |

### 4.6 系统字母速查

| 字母 | 系统 |
| --- | --- |
| G | GPS |
| R | GLONASS |
| E | Galileo |
| C | BDS |
| J | QZSS |
| I | IRNSS/NavIC |
| S | SBAS |

### 4.7 RINEX-2 / RINEX-3 文件名字段

| 风格 | 模式 | 例 |
| --- | --- | --- |
| R2 日文件 | `ssssDDD0.YYt` | `pots0070.15o` |
| R2 小时 | `ssssDDD[a-x].YYt` | `pots007a.15o` |
| R2 子小时 | `ssssDDD[a-x]mm.YYt` | `pots007a15.15o` |
| R3 | `SSSSMRCCC_S_YYYYDDDHHMM_NNN_FRQ_TT.FMT` | `POTS00DEU_R_20150070000_01D_30S_MO.rnx` |

### 4.8 历元参数格式（`-epo_beg`）

- `mjd` / `mjd_hhmmss`
- `wwwwd` / GPS 周+日内时
- `yyyyddd`、`yyyymmdd`、`yyyy-mm-dd`，均可 `_` 接 `hhmmss` 或 `hh:mm:ss`

### 4.9 日志列含义

| 列 | 含义 |
| --- | --- |
| C | N=Notice / W=Warning / E=Error |
| EPOCH/FILE | 出问题的历元 |
| SITE | 4 字符站 |
| T | 数据类型 |
| MESSAGE | 说明 |

### 4.10 输出主版本默认（手册表，以当前上游为准）

| 主版本 | 标准输出小版本 |
| --- | --- |
| 2 | 2.11 |
| 3 | 3.05 |
| 4 | 4.01 |


## 5. 接到电离层 / GNSS 哪一步

### 5.1 在目录流水线中的位置

- 数据获取 → [data-access](../data-access.md)
- **本工具：格式/采样/切片规范化**
- Python 读取 → [georinex](./georinex.md)
- 双频 TEC 基础 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)
- 校准 TEC → [pytecgg](./pytecgg.md) · 一日实践 [16](../tutorials/16-practice-one-day-tec.md)
- ROTI/闪烁 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · 教程 [05](../tutorials/05-scintillation-roti.md)
- 定位与电离层影响 → [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · 教程 [06](../tutorials/06-iono-positioning.md)
- GIM/IONEX → [ionex-gim](./ionex-gim.md) · 教程 [03](../tutorials/03-gim-ionex.md)

### 5.2 推荐最小链（单站一日 TEC）

1. CDDIS/其他源下载 OBS+NAV（见 data-access）
2. `gunzip` / `CRX2RNX`
3. `gfzrnx -chk -smp 30 -satsys G -ot ...` → `out/`
4. `georinex` 读入核对双频列
5. `pytecgg` 或自研 GF 组合算 STEC

### 5.3 推荐链（磁暴日 ROTI）

1. 保留 **1 s 或更高** 采样（不要先抽到 30 s）
2. `gfzrnx -chk -satsys G` 仅做检查与坏头修复
3. 交给 [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
4. 教程 [20](../tutorials/20-storm-tec-analysis.md) 做事件切片

### 5.4 推荐链（PPP-AR 前处理）

1. 多小时文件：`gfzrnx` 拼接 + RINEX3 命名
2. [anubis](./anubis.md) 看周跳/多路径粗况
3. `pdp3`（[pride-pppar](./pride-pppar.md)）

### 5.5 与 sibling 手册的交叉引用

- 读数组、选频率列：见 [georinex](./georinex.md)
- 实时流不是本工具：见 [pygnssutils](./pygnssutils.md)
- QC 报表：见 [anubis](./anubis.md)


## 6. 可操作坑（≥12）

1. **通配未展开：** Windows cmd 不会像 bash 展开 `SITE001{a..x}.24o`。改为显式列表或在 Git Bash/WSL 跑。
2. **忘记 `-f`：** 输出已存在时静默拒绝覆盖，误以为成功。先 `ls` 时间戳或统一加 `-f`。
3. **STDIN 多文件：** 管道只支持单文件输入；拼接必须 `-finp f1 f2 ...`。
4. **名义改名切数据：** `-sei in` / 名义 duration 会**丢掉**文件名区间外的观测。改名前先备份。
5. **ROTI 却抽稀到 30 s：** 高频相位闪烁信息被毁。ROTI 链禁止盲目 `-smp 30`。
6. **`-ot` 写错信号：** 站上是 `L2X` 却写 `L2W`，输出空相位。先 `-stk_obs` 或 `grep` 头里的 OBS TYPES。
7. **拼接内存爆：** 24×1 Hz 文件加默认统计很吃 RAM。加 `-splice_direct` 或先抽稀再拼。
8. **Hatanaka 直接喂错：** 把 `.YYd` 当普通 OBS 喂入会解析失败。先 `CRX2RNX`。
9. **MARKER 缺失：** 自动命名得到怪站名。用 `-site` 或先 `-crux` 写 MARKER NAME。
10. **`-vo` 与下游假设冲突：** 下游脚本写死 RINEX2 短名，你却输出 R3 长名。统一命名策略。
11. **LLI 在抽稀后异常：** 试 `-smp_lli_shift`；并在下游周跳探测参数上放宽验证。
12. **许可用于例行业务：** 科学许可跑 7×24 业务可能违规。上线前核对 EULA。
13. **PRIDE 找不到 gfzrnx：** 二进制仍叫 `gfzrnx_lx`。重命名并放进 PATH。
14. **比较苹果和橘子：** `-fdiff` 要求主版本相同。先都 `-vo 3` 再比。
15. **errlog 只追加：** 多次运行日志混在一起。按任务名分文件或每次 `>` 截断。
16. **国家码 XXX：** `::RX3::00,XXX` 能跑但不便归档。改成真实 ISO 三字母。


## 7. 同类怎么选

| 需求 | 优先 | 次选 | 勿选 |
| --- | --- | --- | --- |
| 格式转换/拼接/抽稀 | **GFZRNX** | gfzrnx+脚本 | 用 Python 手写解析 |
| 读入 xarray 算 TEC | georinex | pytecgg 内置读 | GFZRNX（它不算出 TEC） |
| 站网 QC PDF/图 | anubis | GFZRNX `-stk_*` | TEQC（停更） |
| 实时流 | pygnssutils/BNC | — | GFZRNX |
| PPP-AR | PRIDE-PPPAR | RTKLIB | GFZRNX |

### 7.1 决策口诀

- 「文件名/采样/系统不对」→ GFZRNX
- 「文件内容进数组」→ georinex
- 「质量报告给甲方」→ anubis
- 「要 TEC 数值」→ pytecgg / 自研
- 「要固定解坐标」→ pride-pppar

### 7.2 版本与文档追踪

- HTML/PDF：<https://gnss.git-pages.gfz-potsdam.de/gfzrnx/>
- 邮件列表：`gfzrnx-on@gfz-potsdam.de`（空邮加入，以官网为准）
- Bug：`gfzrnx_bug@gfz-potsdam.de`（附命令行与小样例）
- 不确定的开关 → 跑 `gfzrnx -h` 并以当前上游文档为准

### 7.3 操作检查清单（每次任务）

1. `gfzrnx -h` 可用
2. 输入已解压且非 Hatanaka 误喂
3. 明确：检查 / 抽稀 / 拼接 / 改名 中哪几步
4. errlog 路径按任务隔离
5. 抽稀策略已按 TEC vs ROTI 分支选择
6. `ls -l out/` 时间戳与体积合理
7. `head` 头字段与 `-stk_obs` 过眼
8. 下游工具试读 1 个文件再批量

## 8. 场景化命令卡片

### 8.1 仅检查不改采样

```bash
gfzrnx -finp IN.rnx -fout OUT.rnx -chk -kv -f -errlog LOG.err
```

### 8.2 IGS 日文件 → 30 s GPS 双频

```bash
gfzrnx -finp IN.rnx -fout OUT.rnx -smp 30 -satsys G \
  -ot L1C,L2W,C1C,C2W -kv -f -errlog LOG.err
```

### 8.3 子小时 15 min × 96 → 日文件

```bash
# 文件名模式因站而异；先 ls 再显式列出或用数组
files=(work/SITE001a{00,15,30,45}.24o work/SITE001b{00,15,30,45}.24o) # ...
gfzrnx -finp "${files[@]}" -fout out/SITE0010.24o -kv -f -splice_direct
```

### 8.4 只要元数据 JSON 入库

```bash
gfzrnx -finp IN.rnx -meta full:json > meta.json
```

### 8.5 与 gzip 管道

```bash
gfzrnx -finp IN.rnx -kv | gzip > OUT.rnx.gz
```

### 8.6 从 SEMISYS 拉 4to9（网络可用时）

```bash
curl -G http://semisys.gfz-potsdam.de/semisys/api/ \
  -d 'symname=1005' -d 'network=IGS,MGEX' -o IGS_MGEX_4to9.txt
# 端点可用性以 GFZ SEMISYS 当前文档为准
```

### 8.7 导航 ephemeris 过滤

```bash
gfzrnx -finp BRDC.rnx -fout BRDC_strict.rnx -nav_epo_strict -kv -f
gfzrnx -finp BRDC.rnx -fout BRDC_latest.rnx -nav_latest -kv -f
```

### 8.8 气象文件与 NWM 交叉（高级）

```bash
# 两输入：MET + 参考 NWM；细节见手册 -met_nwm
gfzrnx -finp site.rnx.met nwm_ref.txt -met_nwm -fout site_met_edit.rnx -f
```

### 8.9 直接模式大文件

```bash
gfzrnx -finp HUGE.rnx -fout HUGE_rx3.rnx -vo 3 -direct -f
```

### 8.10 观测类型映射导出

```bash
gfzrnx -out_obs_map > std_obs_map.txt
```


## 9. 输入质量门（进电离层前）

- 双频相位+伪距齐全（按所选 GNSS）
- 采样率满足产品：TEC 常用 30 s；ROTI 常用 ≤1 s
- 时间覆盖完整，接缝处无整小时空洞
- 头中 ANT/REC 与 ANTEX 可匹配（PPP 链）
- MARKER 坐标大致合理（非 0,0,0）

```bash
# 快速目视
head -n 80 out/SITE0010_30s.24o
gfzrnx -finp out/SITE0010_30s.24o -stk_obs | head -n 60
gfzrnx -finp out/SITE0010_30s.24o -meta basic:txt
```

### 9.1 常见头字段与下游关系

| 头字段 | 谁在意 |
| --- | --- |
| MARKER NAME / NUMBER | 命名、PPP 站名 |
| REC # / TYPE / VERS | DCB、PCO |
| ANT # / TYPE | ANTEX |
| APPROX POSITION XYZ | SPP 初值、IP P |
| SYS / # / OBS TYPES | TEC 选频 |
| INTERVAL | 抽稀核对 |
| TIME OF FIRST/LAST OBS | 事件切片 |

### 9.2 与教程章节对照

| 教程 | 本工具动作 |
| --- | --- |
| 02 双频 TEC | 筛双频类型、30 s |
| 05 ROTI | 保留高采样、只 -chk |
| 06 定位 | 拼接+改名给 PPP |
| 09 DCB | 保证信号标识正确 |
| 16 一日 TEC 实践 | 完整预处理卡片 8.2 |


## 10. 附录：命令速查一页纸

```bash
gfzrnx -h
gfzrnx -finp IN -fout OUT -chk -kv -f
gfzrnx -finp IN -fout OUT -smp 30 -kv -f
gfzrnx -finp H1 H2 ... -fout DAY -kv -f
gfzrnx -finp IN -fout DIR/::RX3::00,CHN -vo 3 -sei in -f
gfzrnx -finp IN -fout OUT -satsys G -ot L1C,L2W,C1C,C2W -kv -f
gfzrnx -finp IN -stk_obs
gfzrnx -finp IN -stk_epo 3600
gfzrnx -finp IN -meta full:json
gfzrnx -finp IN -fout DIR/::RX3::00,CHN -split 3600 -vo 3 -f
```

终注：开关语义若与本机 `-h` 冲突，**以当前上游文档与本机帮助为准**。

