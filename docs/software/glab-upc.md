# gLAB-UPC · ESA/UPC GNSS 教学处理套件操作手册

目录：[`PROJECTS.json` → `gLAB-UPC`](../../PROJECTS.json) · 官网 <https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite> · 下载 <https://gage.upc.edu/en/learning-materials/software-tools/glab-tool-suite-links/glab-download> · 直链 `gLAB_6.0.0_Linux.tgz`（~335 MB） · 许可 **核心/绘图 Apache-2.0；Qt GUI LGPL-3** · 本机验证 **v6.0.0**（官方预编译 `gLAB_linux`，built Nov 22 2024）+ 自编译 core（mirror tip `5d66623`）· 2026-09-24 04:30 EDT · **质检复跑通过**（OUTPUT 2880；H95=2.37/V95=4.63/3D95=4.75 m；PDOP95=1.00；~0.61 s）

> 岗位：教学向 **SPP/PPP/SBAS/DGNSS**、观测建模拆解、电离层模型切换（Klobuchar/NeQuick/IONEX/SBAS）。冲突时：**官方 SUM / `./gLAB_linux -help` > 本文**。生产 PPP-AR → [pride-pppar](./pride-pppar.md)；工程 RTK/PPP → [rtklib](./rtklib.md)；Python 开放 PPP → [cssrlib](./cssrlib.md)。GitHub `valgur/gLAB` 等仅为社区镜像，**许可以 UPC 发行包为准**。

## 1. 用途与边界

**做：**

- 厘米级观测建模教学：伪距/相位、对流层、电离层、天线、潮汐等可逐项开关
- **SPP**（广播星历）/ **PPP**（SP3+CLK+ANTEX）/ SBAS / DGNSS；多系统 GPS+GLO+GAL+BDS+QZSS
- 读 RINEX 2/3 OBS·NAV、SP3、CLK、ANTEX、IONEX、SINEX；文本 `OUTPUT`/`INFO` 便于画图与统计
- Linux x86_64 **预编译** `gLAB_linux` / `gLAB_linux_MultiThread` + `gLAB_GUI`；ARM 需 `make`

**不做：**

- **不是** 业务级实时多站引擎 → [bnc](./bnc.md) / [rtklib](./rtklib.md)
- **不是** 发表级 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- **不是** 校准 sTEC/vTEC 产品 → [pytecgg](./pytecgg.md)（gLAB 电离层是**定位改正**，不是 GIM 生产器）
- **不是** 把社区 git 镜像当唯一来源（缺 GUI/数据/许可文本时以官方 tgz 为准）

一句话：gLAB = **ESA/UPC 教学实验台**；把「每一项误差如何进方程」跑明白，再换生产引擎。

| 组件 | 角色 |
| --- | --- |
| `gLAB_linux` | 数据处理核心（DPC）CLI |
| `gLAB_linux_MultiThread` | 同核心多线程构建 |
| `gLAB_GUI` | Qt 图形前端（模板：SPP/PPP/SBAS…） |
| `graph.py` / `graph/` | 捆绑绘图（老包内嵌运行时，体积大） |

## 2. 安装

### 2.1 官方 Linux 包（推荐）

```bash
mkdir -p ~/iono_ops/glab && cd ~/iono_ops/glab
# 浏览器打开发布页，或直链（文件名随版本变；以下载页为准）
curl -fL -A 'Mozilla/5.0' -o gLAB_6.0.0_Linux.tgz \
  'https://server.gage.upc.edu/gLAB/src/LINUX/gLAB_6.0.0_Linux.tgz'
# 本机写作：335044237 bytes；质检复跑文件 350909925 bytes（同 URL，体积可随镜像变）
tar -xzf gLAB_6.0.0_Linux.tgz
cd gLAB
./gLAB_linux -help | head -5
# 期望：gLAB version v6.0.0, built on Nov 22 2024 ...
```

x86_64 一般**不用编译**。ARM / 要改 core：

```bash
sudo apt-get install -y make gcc
cd ~/iono_ops/glab/gLAB
make -j"$(nproc)"              # → gLAB_linux
make -f Makefile_multithread -j"$(nproc)"
```

### 2.2 仅核心源码（社区镜像，可选）

```bash
git clone --depth 1 https://github.com/valgur/gLAB.git ~/iono_ops/glab-mirror
cd ~/iono_ops/glab-mirror/core
make -j"$(nproc)"              # 本机 tip 5d66623 → ./gLAB_linux
./gLAB_linux -help | head -2
# 期望：gLAB version v6.0.0, built on <本机构建日>
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `curl` 403 / 空文件 | 缺 UA 或链过期 | 加 `-A Mozilla/5.0`；回下载页拷当前 href |
| 旧 4.x `make` 链错误 `multiple definition of messagestr` | 新 gcc 默认 `-fno-common` | **改用 6.x 包**或镜像 core；勿死磕 4.2 |
| `./gLAB_GUI` 缺库 | 缺 Qt/显示 | 教学先用 CLI；GUI 按 SUM 装依赖 |
| 把 `valgur/gLAB` 当官方发布 | 镜像无完整 graph 运行时 | 发行/引用以 UPC tgz + 许可文件为准 |

## 3. 端到端：广播 SPP（本机真跑）

数据：PRIDE 示例站 **abmf** 2020-001（RINEX3 OBS + 混合 NAV）。

```bash
OBS=~/iono_ops/data/abmf0010.20o
NAV=~/iono_ops/data/brdm0010.20p
GLAB=~/iono_ops/glab/gLAB/gLAB_linux

"$GLAB" \
  -input:obs "$OBS" \
  -input:nav "$NAV" \
  -output:file ~/iono_ops/glab_e2e/spp_abmf.txt

wc -l ~/iono_ops/glab_e2e/spp_abmf.txt
grep -c '^OUTPUT' ~/iono_ops/glab_e2e/spp_abmf.txt
grep -n 'SPP Summary' ~/iono_ops/glab_e2e/spp_abmf.txt | head
```

**本机（官方 `gLAB_linux` v6.0.0，2026-09-24 04:30 EDT）：**

```text
INFO gLAB version v6.0.0, built on Nov 22 2024 23:58:23
INFO Processing with broadcast products
OUTPUT 行数：2880
Epochs_processed / with_solution：2880 / 2880（Avail% 100）
Horizontal 95 PE：2.37 m · Vertical 95 PE：4.63 m · 3D 95 PE：4.75 m
PDOP 95：1.00 · 总耗时 ~0.62 s
```

`OUTPUT` 列定义见 `./gLAB_linux -messages`。摘要块：`INFO --------------------- SPP Summary ---------------------`。

### 3.1 电离层开关（教学对照）

```bash
"$GLAB" -input:obs "$OBS" -input:nav "$NAV" \
  -model:iono no -output:file spp_iono_off.txt

"$GLAB" -input:obs "$OBS" -input:nav "$NAV" \
  -model:iono Klobuchar -output:file spp_klob.txt

"$GLAB" -input:obs "$OBS" -input:nav "$NAV" \
  -input:inx CODG0010.20I -model:iono IONEX \
  -output:file spp_ionex.txt

"$GLAB" -input:obs "$OBS" -input:nav "$NAV" \
  -model:iono NeQuick -output:file spp_neq.txt
```

`-model:iono` 合法值（v6.0.0）：`no` · `Klobuchar` · `BeiDou` · `IONEX` · `FPPP` · `NeQuick` · `SBAS`。多写时**最后一次**生效。

### 3.2 PPP 模板（有精密产品时）

```bash
"$GLAB" \
  -input:obs "$OBS" \
  -input:sp3 igs20864.sp3 \
  -input:clk igs20864.clk \
  -input:ant igs14.atx \
  -filter:meas carrierphase \
  -filter:nav static \
  -output:file ppp_abmf.txt
```

缺 SP3/CLK/ANTEX 时不要硬跑；先 SPP 冒烟。

### 3.3 配置文件

```bash
"$GLAB" -config | head -40
"$GLAB" -input:cfg my_spp.cfg   # 每行一条旗标；# 注释；CLI 覆盖 cfg
```

## 4. I/O 与关键参数

| 侧 | 形式 | 说明 |
| --- | --- | --- |
| 入 | `-input:obs` | RINEX OBS 2/3 |
| 入 | `-input:nav` | 广播 NAV；混合 RINEX3 常用 `.p` |
| 入 | `-input:sp3` / `:clk` / `:ant` | PPP |
| 入 | `-input:inx` | IONEX；配 `-model:iono IONEX` |
| 入 | `-input:sbas1f` / `:sbasdfmc` | SBAS |
| 出 | `-output:file` | `INFO`/`OUTPUT`/摘要 |

| 旗标 | 作用 |
| --- | --- |
| `-pre:sat` | 星座过滤（例 `-pre:sat -RSJCI0` 留 GPS+GAL） |
| `-pre:dec` | 抽稀秒 |
| `-filter:nav static\|kinematic` | 动力学 |
| `-filter:meas` | `pseudorange` / `carrierphase` |
| `-messages` | 输出列定义 |

## 5. 接到哪步

```text
RINEX OBS+NAV
  → gLAB SPP（本文）核对广播 / 电离层模型差异
  →（可选）SP3+CLK → gLAB PPP 教学
  → 正式坐标/ZTD → pride-pppar / rtklib
  → TEC 产品 → georinex → pytecgg；GIM → ionex-gim
```

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ERROR Opening RINEX observation file` | 路径错/未解压 | `ls -l "$OBS"`；改绝对路径 |
| 2 | `Receiver a priori position must be above Earth surface` | 头 `APPROX POSITION`≈0 | 换正常站文件或给近似坐标 |
| 3 | `Invalid PRN 'E' in line … navigation file` | RINEX4 分块 NAV 等方言 | 换 RINEX3 混合 NAV（`brdm*.*p`） |
| 4 | `Invalid date in line … observation file` | OBS 截断/非标 | 先 QC；换完整日文件 |
| 5 | 旧 4.2 `multiple definition of messagestr` | 新 gcc 与旧全局变量冲突 | 用官方 **6.x** 预编译/新 core |
| 6 | SPP 误差数十米且 Avail%≪100 | 星历日不匹配/滤星过狠 | 核对 DOY；默认 Klobuchar；放宽 `-pre:sat` |
| 7 | PPP 无 `OUTPUT` | 只给 OBS+NAV 却开 phase PPP | 补 `-input:sp3`+`-input:clk`+`-input:ant` |
| 8 | GUI 与批处理结果不同 | cfg 与模板不一致 | 同一 cfg；CLI 复跑对照 |
| 9 | 镜像 git 缺 `graph/` 大运行时 | 社区仓主打 core | 绘图用官方 tgz |
| 10 | 把 gLAB 残差当 STEC 产品 | 定位改正≠校准 TEC | TEC 走 [pytecgg](./pytecgg.md) |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 课堂 SPP/PPP、逐项误差 | **gLAB（本文）** |
| 生产 PPP-AR | [pride-pppar](./pride-pppar.md) |
| 轻量 CLI RTK/PPP | [rtklib](./rtklib.md) |
| Python 开放 PPP | [cssrlib](./cssrlib.md) |
| 校准 TEC / ROTI | [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) |
| 读 IONEX | [ionex-gim](./ionex-gim.md) |

相关：官方 Tool Suite · Download · Citations（NAVITEC 2018 DOI `10.1109/NAVITEC.2018.8642707`）· [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [cssrlib](./cssrlib.md) · 教程 [06](../tutorials/06-iono-positioning.md)/[10](../tutorials/10-build-gim-workflow.md)
