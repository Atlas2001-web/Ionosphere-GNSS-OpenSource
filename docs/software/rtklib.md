# RTKLIB · 定位 CLI 操作手册

目录：[`PROJECTS.json` → `RTKLIB`](../../PROJECTS.json) · 原版 <https://github.com/tomojitakasu/RTKLIB> · explorer（推荐）<https://github.com/rtklibexplorer/RTKLIB>（原 demo5；**2025-07 起 demo5 分支退役，活动在 `main`，产品名常称 RTKLIB-EX**）

> 岗位：事后 SPP/RTK/浮点 PPP → `.pos`。本页旗标表与端到端输出验证自 **explorer `rnx2rtkp` EX 2.5.1**（`-?`）。Debian 包 `rtklib`（常见 2.4.3 b34）可 `apt` 冒烟，但 **`-h` 是 fix-and-hold，不是帮助**——帮助用 `-?`；`-p` 编号以本机为准。换二进制先重跑 `-?`。

## 1. 用途与边界

**做：** `rnx2rtkp` 事后定位；`convbin` 原始→RINEX；`str2str` 流转发；可选 GUI（RTKPOST/RTKNAVI）。主产品是**坐标时间序列**。

**不做：** STEC/VTEC/ROTI（→ [pytecgg](./pytecgg.md)/[oasis-roti](./oasis-roti.md)）；发表级 PPP-AR（→ [pride-pppar](./pride-pppar.md)）；多流录盘主力（→ [bnc](./bnc.md)）。电离层在此是改正/误差源，不是 GIM 产品。

## 2. 安装 / 编译（路径写死）

### 2.0 Debian/Ubuntu 快速冒烟（apt，版本旧）

```bash
sudo apt-get update && sudo apt-get install -y rtklib
which rnx2rtkp convbin
rnx2rtkp -? 2>&1 | head -n 40   # 注意：-h ≠ 帮助
```

短文件 SPP（本机 Debian 2.4.3 b34 真输出）：

```bash
mkdir -p ~/rtk_demo && cd ~/rtk_demo
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
curl -fsSL -o 14601736.18n \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n
rnx2rtkp -p 0 -sys G -m 5 -t -e -o out_spp.pos 14601736.18o 14601736.18n
```

```text
% program   : rnx2rtkp ver.2.4.3 b34
% obs start : 2018/06/22 06:17:30.0 GPST
2018/06/22 06:17:30.000  -4647152.8622   2562199.8251  -3526633.5232   5   5  ...
2018/06/22 06:17:45.000  -4647154.8149   2562203.2110  -3526633.2505   5   6  ...
2018/06/22 06:18:00.000  -4647175.3345   2562227.4574  -3526639.2208   5   6  ...
```

期望：`Q=5`（single）。教学/完整旗标仍推荐 §2.2 explorer。

### 2.1 Windows 预编译

1. 打开 <https://github.com/rtklibexplorer/RTKLIB/releases>
2. 解压 zip，把含 `rnx2rtkp.exe` 的目录加入用户 PATH
3. 新开 cmd：`rnx2rtkp -?` · `convbin -?`

### 2.2 Linux：explorer `main`（推荐 CMake）

```bash
sudo apt update
sudo apt install -y build-essential cmake git gfortran
# GUI 还要 Qt 开发包；只要 CLI 可稍后装
git clone https://github.com/rtklibexplorer/RTKLIB.git
cd RTKLIB
mkdir -p build && cd build
cmake ..
make -j"$(nproc)"
# 默认可执行文件进构建树；可选：
sudo make install   # 通常装到 /usr/local/bin
hash -r
rnx2rtkp -? | head
rnx2rtkp --version
```

### 2.3 Linux：只要 CLI 的旧 make（仍可用，README 标 DEPRECATED）

```bash
cd RTKLIB/app/consapp/rnx2rtkp/gcc && make -j"$(nproc)"
# 产出：./rnx2rtkp
cd ../../convbin/gcc && make -j"$(nproc)"
export PATH="/abs/path/to/RTKLIB/app/consapp/rnx2rtkp/gcc:/abs/path/to/RTKLIB/app/consapp/convbin/gcc:$PATH"
```

本手册验证：`app/consapp/rnx2rtkp/gcc` + `gfortran` 链接成功 → `rnx2rtkp RTKLIB EX 2.5.1`。

### 2.4 原版 tomojitakasu

```bash
git clone https://github.com/tomojitakasu/RTKLIB.git RTKLIB-official
# 同样走 app/consapp/<app>/gcc 或该仓 README
# 不要与 explorer 的 rnx2rtkp 混在同一 PATH 前缀
which -a rnx2rtkp
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `command not found` | PATH | `export PATH=...:$PATH`；`hash -r` |
| `cannot find -lgfortran` | 链了 Fortran 运行时 | `sudo apt install gfortran` |
| 两套行为不同 | PATH 里多个二进制 | `which -a rnx2rtkp`；只留一套 |
| `-p` 与网帖不符 | 分支差异 | 信本机 `-?` |

## 3. 端到端：测试数据 SPP → 读懂 `.pos` → 静态 RTK

数据：explorer 仓自带 `test/data/rinex/30400920.05o` + `.05n`（及基站 `07590920.*`）。以下为 **本机 EX 2.5.1 真实输出**。

### 3.1 SPP（单点）

```bash
RNX=rnx2rtkp   # 或绝对路径 .../gcc/rnx2rtkp
D=RTKLIB/test/data/rinex
mkdir -p out logs
$RNX -p 0 -m 15 -sys G -e -t \
  -o out/spp.pos \
  "$D/30400920.05o" "$D/30400920.05n"
wc -l out/spp.pos
head -n 12 out/spp.pos
```

**终端进度行含义：** `processing : 2005/04/02 00:00:30 Q=5` → 正在处理该历元；`Q=5` 表示当前解类型为 single（见下表）。

**真实文件头 + 首行数据：**

```text
% program   : rnx2rtkp ver.EX 2.5.1
% inp file  : .../30400920.05o
% inp file  : .../30400920.05n
% obs start : 2005/04/02 00:00:00.0 GPST (week1316 518400.0s)
% obs end   : 2005/04/02 00:59:30.0 GPST (week1316 521970.0s)
%
% (x/y/z-ecef=WGS84,Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp,ns=# of satellites)
%  GPST                      x-ecef(m)      y-ecef(m)      z-ecef(m)   Q  ns   sdx(m)   sdy(m)   sdz(m)  sdxy(m)  sdyz(m)  sdzx(m) age(s)  ratio
2005/04/02 00:00:00.000  -3978242.2255   3382841.5580   3649902.4074   5   7   4.5201   5.5463   4.4294  -4.4441   3.8489  -3.3337   0.00    0.0
```

### 3.2 逐字段解码（上表第一行数据）

| 字段 | 本行值 | 含义 |
| --- | --- | --- |
| 日期时间 | `2005/04/02 00:00:00.000` | 解的历元；因 `-t` 为 `yyyy/mm/dd hh:mm:ss.ss`；默认时间系 GPST（`-u` 改 UTC） |
| x-ecef | `-3978242.2255` | WGS84 ECEF X (m)；因加了 `-e`。不加 `-e` 则是 lat/lon/height |
| y-ecef | `3382841.5580` | ECEF Y (m) |
| z-ecef | `3649902.4074` | ECEF Z (m) |
| Q | `5` | 解状态：1 fix / 2 float / 3 sbas / 4 dgps / **5 single** / 6 ppp |
| ns | `7` | 所用卫星数 |
| sdx/sdy/sdz | `4.52…` | 坐标标准差 (m) |
| sdxy/sdyz/sdzx | 协方差项 | 用于误差椭圆等 |
| age | `0.00` | 差分龄期 (s)；SPP 为 0 |
| ratio | `0.0` | 模糊度固定 ratio；SPP 无 AR → 0 |

### 3.3 静态 RTK（rover + base）

```bash
$RNX -p 3 -m 15 -sys G -e -t \
  -o out/rtk.pos \
  "$D/07590920.05o" "$D/30400920.05o" \
  "$D/07590920.05n" "$D/30400920.05n"
# 文件顺序：第 1 个 OBS = rover，第 2 个 OBS = base，其后 NAV…
grep -v '^%' out/rtk.pos | head -n 5
```

**真实片段：**

```text
2005/04/02 00:00:00.000  -3976219.7132   3382373.1680   3652512.9438   2   7  ...  ratio 0.0
2005/04/02 00:01:00.000  ...                                                         Q=2
2005/04/02 00:01:30.000  -3976219.4191   3382372.5427   3652512.5819   1   7  ...  ratio 40.1
```

解读：前几历元 `Q=2`（float）→ `00:01:30` 起 `Q=1`（fix），`ratio` 从 0 跳到 ~40。固定后 `sdx` 从米级掉到毫米级——这是短基线静态 RTK 的正常收敛，不是“文件坏了”。

### 3.4 统计 Q 分布

```bash
python - <<'PY'
from collections import Counter
q=Counter()
with open("out/rtk.pos") as f:
    for line in f:
        if line.startswith("%") or not line.strip(): continue
        parts=line.split()
        # -e -t 时：日期 时间 x y z Q ns ...
        q[parts[5]] += 1
print(dict(q))
PY
```

## 4. `rnx2rtkp` 全旗标表（EX 2.5.1 `-?`）

| 旗标 | 作用 | 默认 |
| --- | --- | --- |
| `-?` | 打印帮助 | |
| `-k file` | 从 conf 读选项；**命令行覆盖 conf** | off |
| `-o file` | 输出 `.pos`；省略则 stdout | stdout |
| `-ts ds ts` | 起始 `y/m/d` + `h:m:s` | OBS 起点 |
| `-te de te` | 结束日时 | OBS 终点 |
| `-ti tint` | 输出间隔秒 | 全历元 |
| `-p mode` | 0 single · 1 dgps · 2 kinematic · 3 static · 4 static-start · 5 moving-base · 6 fixed · 7 ppp-kine · 8 ppp-static · 9 ppp-fixed | **2**（注意默认是 kinematic！SPP 必须显式 `-p 0`） |
| `-m mask` | 高度截止角（度） | 15 |
| `-sys s[,s…]` | G/R/E/J/C/I | 帮助写 G\|R；本机构建里未指定时源码会扩到多系统——**以你跑出的行为为准** |
| `-f freq` | 相对定位频率数 1/2/3 | 2 |
| `-v thres` | AR 检验阈值；`0.0`=不做 AR | 3.0 |
| `-b` | 反向滤波 | off |
| `-c` | 前后向组合 | off |
| `-i` | 瞬时 AR | off |
| `-h` | fix-and-hold AR | off |
| `-bl bl,std` | 基线长约束 | |
| `-e` | 输出 ECEF xyz | 默认 lat/lon/h |
| `-a` | 输出 ENU 基线 | |
| `-n` | NMEA GGA | off |
| `-g` | lat/lon 用度分秒 | 默认小数度 |
| `-t` | 时间用日历格式 | 默认 GPS 秒 |
| `-u` | 时间 UTC | 默认 GPST |
| `-d col` | 时间小数位 | 3 |
| `-s sep` | 字段分隔符 | 空格 |
| `-r x y z` | 基站（或 fixed 模式流动站）ECEF | 单点均值 |
| `-l lat lon hgt` | 同上，地理坐标 | |
| `-y level` | 0 off / 1 states / 2 residuals → `.stat` | 0 |
| `-x level` | debug trace | 0 |
| `--rover` / `--base` | 多站名列表 | |
| `--version` | 打印版本 | |

输入文件规则：最多 16 个；**第一个 OBS = rover**；相对模式**第二个 OBS = base**；至少一个 NAV；SP3 扩展名 `.sp3`/`.eph`；路径可用通配符（shell 下请加引号）。

### 4.1 `convbin` 最小例

```bash
convbin -r ubx -o rover.obs -n rover.nav rover.ubx
# -r：原始格式；-o OBS；-n NAV
head -n 3 rover.obs   # 期望 RINEX VERSION / TYPE
```

### 4.2 配置文件固化

```bash
rnx2rtkp -k conf/my_rtk.conf -o out/exp.pos rover.obs base.obs rover.nav
# 每次只改 conf 里一个键（pos1-posmode / pos1-elmask / pos1-ionoopt…）
```

## 5. 接到哪一步

| 场景 | 动作 | 链接 |
| --- | --- | --- |
| 电离层与定位 | 本页 SPP/RTK | [06](../tutorials/06-iono-positioning.md) |
| 磁暴日固定率 | RTK Q 序列 + ROTI | [20](../tutorials/20-storm-tec-analysis.md) · [oasis-roti](./oasis-roti.md) |
| 实时 | 先事后冒烟，再 [bnc](./bnc.md) 转发 + `str2str`/`rtkrcv` | 路径 C |
| 发表坐标 | 冒烟后换 | [pride-pppar](./pride-pppar.md) |
| 只要 TEC | 离开本页 | [pytecgg](./pytecgg.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `.pos` 几乎空 / 退出非 0 | 无 NAV、OBS 是 HTML、路径错 | `head` 输入；查 stderr；换 NAV 日 |
| 2 | 自称 RTK 但 Q 全是 5 | 没传 base 或 `-p` 仍是 single | 确认第 2 个 OBS；`-p 3` |
| 3 | 固定率崩 | 基线过长 / 无共视 / 截止角过高 | 查时间重叠；`-m 10`；换短基线 |
| 4 | PPP 不收敛 | 缺 SP3/CLK 或日期错一天 | `head`/`tail` 产品时间；加长观测 |
| 5 | 死记 `-p` 跨分支 | 原版/EX 文档混贴 | 每次 `-?`；归档 `rnx2rtkp -? > logs/help.txt` |
| 6 | 天线高系统差 | ARP/天线高未设 | conf 里天线参数；或先冒烟再精密 |
| 7 | 实时乱跳先调 AR | 流龄期/网络 | 先修 caster；`age` 列；退回文件模式 |
| 8 | 把 `.pos` 当 TEC | 链选错 | → pytecgg |
| 9 | GUI 勾选与 CLI conf 不一致 | 两套来源 | 只信磁盘上的 `-k` 文件 |
| 10 | 旧 `.pos` 被追加弄脏 | 同名输出 | 跑前 `rm` 或换 `-o` |
| 11 | 列解析脚本升级后错位 | 头注释变了 | 重读 `%` 头；按列名解析 |
| 12 | `no common satellites` | 时间/系统无交集 | georinex 对两端 `gtime`/time；`-sys` 对齐 |
| 13 | PATH 里官方与 EX 混用 | 两个 `rnx2rtkp` | `which -a`；删旧或改顺序 |
| 14 | 磁暴对照却同时改了全部参数 | 实验不干净 | 只留电离层相关旋钮 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 教学/工程 RTK、PPP 冒烟 | **RTKLIB / EX** |
| PPP-AR | **PRIDE-PPPAR** |
| 多流录盘 | **BNC** |
| TEC/ROTI | **pytecgg / oasis-roti / ionomoni** |

## 8. 相关

[pride-pppar](./pride-pppar.md) · [bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)
