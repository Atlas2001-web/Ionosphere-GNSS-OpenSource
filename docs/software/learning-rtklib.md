# learning_rtklib（libing64）· RTKLIB 中文学习笔记 + 6 个 C++ 调用示例 操作手册

目录：[`PROJECTS.json` → `learning_rtklib`](../../PROJECTS.json) · 上游 <https://github.com/libing64/learning_rtklib> · **无 LICENSE 文件**（GitHub API `license=null`）；它依赖的 RTKLIB 为 **BSD-2-Clause**（Takasu `readme.txt`）· tip **`e326a4b`**（2020-08-22，此后无提交；★163，非 fork）· 仓库 53 MB（大部分是样例数据）· 本机 gcc **14.2.0** / cmake **3.31.6** · **2026-09-26 01:06–01:09 EDT** 实跑：按其 README 用 tomojitakasu/RTKLIB master `71db0ff`（**2.4.2 p13**）编出 `librtklib.a`，6 个示例全部编译、全部 exit 0；同一源码树的 `rnx2rtkp` 在仓内数据上 SPP **900**×Q5、RTK **115**×Q1，且与示例程序输出逐位一致。

> 岗位：**读 RTKLIB 的入门台阶**——看中文笔记理解 RINEX / 卫星位置 / SPP / RTK / PPP，再用最短的 C++ 程序直接调 `readrnxt`、`satpos`、`pntpos`、`rtkpos` 看中间结果。

## 0. 先说清它是什么、不是什么

| 常见误解 | 实际（tip `e326a4b`） |
| --- | --- |
| “带中文注释的 RTKLIB 源码 fork” | **不含任何 RTKLIB 源码**，也不是 GitHub fork。只有 `README.md`（中文笔记，477 行）+ 6 个 `*_example.cpp`（共 670 行）+ `data/` + `doc/GPSbasics.pdf` |
| 自带 `rnx2rtkp` | 没有。README §8.1 让你去 clone **tomojitakasu/RTKLIB** 自己编静态库；`rnx2rtkp` 也得从那棵树编 |
| 能跟最新 RTKLIB 一起用 | 示例写死了 2.4.2 的结构体字段（`nav->lam`、`sta->marker`、`FREQ1`），对 2.4.3/demo5/EX **编译不过**（坑 3） |
| 讲了差分 DGPS | README §5 只写了 “TODO”，`dpp_example.cpp` 不存在 |

要“RTKLIB 本体怎么用” → [rtklib](./rtklib.md)；要低成本接收机改进版 → [rtklib-explorer](./rtklib-explorer.md)；要 Python 调用 → [pyrtklib](./pyrtklib.md) / [pyrtklib-demo5](./pyrtklib-demo5.md)。

## 1. 名词

| 术语 | 含义 |
| --- | --- |
| 静态库 `librtklib.a` | 把 RTKLIB 的 `.c` 编成一个归档文件，示例程序链接它就能调用所有 `extern` 函数 |
| `obs_t` / `nav_t` / `sta_t` | RTKLIB 的观测数组、星历（广播+精密）、测站头信息结构体 |
| `readrnxt` | 读 RINEX（O/N），可按时间段截取；`rcv=1` 流动站，`rcv=2` 基准站 |
| `satpos` / `peph2pos` | 求某时刻卫星位置与钟差（广播或精密） |
| `pntpos` | 单历元 SPP（伪距最小二乘），米级 |
| `rtkpos` | RTK/PPP 的逐历元滤波入口；RTK 需两台接收机观测 |
| LAMBDA | 整周模糊度搜索算法（`lambda.c`）；成功即 “fix”（Q=1） |
| `nav->lam` | 2.4.2 中每颗卫星每频的**波长**数组；示例必须手动赋值，否则载波相位全错 |
| trace | 编库时加 `-DTRACE`，运行时 `traceopen()`/`tracelevel()` 打出内部调试日志 |

## 2. 仓库导航（笔记 → 示例 → RTKLIB 源码）

行号取自本机 tomojitakasu/RTKLIB `71db0ff`（2.4.2 p13）。

| README 节（共 477 行） | 示例 | 读的数据（相对 `build/`） | 调到的 RTKLIB 函数 → 源文件:行 |
| --- | --- | --- | --- |
| §2 RINEX 格式/命名/解析 | `rinex_example.cpp` | `../data/07590920.05o/n`（GSI 0759，2005-04-02） | `readrnxt` → `rinex.c:1486` |
| §3 广播星历算卫星位置 | `satpos_example.cpp` | `../data/rinex/daej229a0*.20n`（DAEJ，2020-08-16） | `satpos` → `ephemeris.c:673`（内部 `eph2pos` `:181`） |
| §4 单点定位 | `spp_example.cpp` | `../data/rinex/daej229a00.20o/n` | `pntpos` → `pntpos.c:539` |
| §6 RTK | `rtk_example.cpp` | 流动站 `07590920.05o` + 基准 `30400920.05o` | `rtkinit`/`rtkpos` → `rtkpos.c:1776`；AR `lambda` → `lambda.c:164` |
| §7.1 精密轨道算卫星位置 | `ppp_satpos_example.cpp` | `../data/sp3/igr2119*.sp3/.clk` + DAEJ | `readsp3` → `preceph.c:253`；`readrnxc` → `rinex.c:1579`；`peph2pos` → `preceph.c:597` |
| §7.2 PPP | `ppp_example.cpp` | 同上 | `rtkpos`（mode=PPP）→ `pppos` → `ppp.c:1015` |
| §9 常用函数签名、§10 宏 | —— | —— | 摘自 `rtklib.h`：`SOLQ_*`、`PMODE_*`、`SOLF_*`、`TIMES_*` |

读法建议：先看 README 对应节的输出样例 → 打开 `.cpp` 看它设置了哪些 `prcopt_t` 字段 → 跳到上表源文件行号读函数本体 → 用 trace（坑 6）核对内部步骤。

`data/` 另含 `highrate/`（DAEJ 2020-07-06 四个 15 min 高频段）、`bahr1620.04o/n`、`sp3/` 下 igr2119x 的 `.sp3/.clk/.erp/.sum/.cls`，示例未全部用到。

## 3. 构建

### 3.1 编 RTKLIB 2.4.2 静态库（README §8.1，改为装到用户目录）

```bash
git clone --depth 1 https://github.com/tomojitakasu/RTKLIB ~/iono_ops/src/RTKLIB-tomoji   # master = 2.4.2 p13
cd ~/iono_ops/src/RTKLIB-tomoji/src
# 把 README §8.1 的 CMakeLists.txt 原样存到这里（文件清单含 qzslex.c、ppp_ar.c，只有 2.4.2 有）
mkdir -p build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/iono_ops/opt/rtklib242 && make -j8 && make install
```

本机输出：

```
[100%] Built target rtklib
-- Installing: /home/box/iono_ops/opt/rtklib242/lib/librtklib.a
-- Installing: /home/box/iono_ops/opt/rtklib242/include/rtklib.h
```

（cmake 3.31 会对 `cmake_minimum_required(VERSION 3.1)` 给 Deprecation Warning，可忽略。）

### 3.2 编 6 个示例

```bash
git clone --depth 1 https://github.com/libing64/learning_rtklib ~/iono_ops/src/learning_rtklib
cd ~/iono_ops/src/learning_rtklib && mkdir -p build && cd build
P=$HOME/iono_ops/opt/rtklib242
cmake .. -DCMAKE_CXX_FLAGS="-I$P/include" -DCMAKE_EXE_LINKER_FLAGS="-L$P/lib" && make
```

```
[ 16%] Built target rinex_example
[ 33%] Built target satpos_example
[ 50%] Built target spp_example
[ 66%] Built target rtk_example
[ 83%] Built target ppp_satpos_example
[100%] Built target ppp_example
```

`find_package(Eigen3)` 找不到也不影响（示例没用 Eigen）。

### 3.3 编同一棵树的 `rnx2rtkp`

```bash
cd ~/iono_ops/src/RTKLIB-tomoji/app/rnx2rtkp/gcc && make      # 仅 rcsid 未使用等警告
./rnx2rtkp -? 2>&1 | sed -n 2p                                 #  usage: rnx2rtkp [option]... file file [...]
```

产物 2261824 B，头部写 `rnx2rtkp ver.2.4.2`。

## 4. 端到端实跑（本机）

### 4.1 六个示例（必须在 `build/` 里运行）

```bash
cd ~/iono_ops/src/learning_rtklib/build
for e in rinex_example satpos_example spp_example rtk_example ppp_satpos_example ppp_example; do ./$e > /tmp/lr_$e.txt; echo "$e exit=$? lines=$(wc -l < /tmp/lr_$e.txt)"; done
```

| 程序 | exit | 输出行数 | 墙时 | 关键结果 |
| --- | --- | ---: | ---: | --- |
| rinex_example | 0 | 1127 | 0.01 s | `nav : n=162`，`obs : n=948` |
| satpos_example | 0 | 1320 | 0.02 s | 每 30 s 一组卫星 ECEF + 钟差 |
| spp_example | 0 | 919 | 0.38 s | 900 历元 ECEF 解 |
| rtk_example | 0 | 72 | 0.08 s | 70 行 “pos:” 全部是 fix（`stat==SOLQ_FIX` 分支） |
| ppp_satpos_example | 0 | 9002 | 0.55 s | 广播 vs 精密卫星位置并列 |
| ppp_example | 0 | 902 | 0.62 s | 900 行：每历元一行 PPP-static ECEF（行首数字是观测序号/总观测数 8486） |

节选（与 README 样例逐字相同的部分不再重复）：

```
# rinex_example
nav : n=162
2005/04/02 02:00:00.000 :  1    2005/04/02 02:00:00 2005/04/02 00:19:36 140 396  0
obs : n=948
2005/04/02 00:00:00.000 :  3  1  55923622.160  43647388.242  24767686.375  24767684.822  0 0

# satpos_example（列：PRN 秒 X Y Z[m] 钟差[ns]）
2020.000000,8.000000,16.000000,0.000000,0.000000,0.000000
01      0  -13573837.896    9929603.849   20232286.958      33959.136

# spp_example（年,月,日,时,分,秒,X,Y,Z,Vx,Vy,Vz）末行
2020,8,16,0,14,59,-3120047.624719,4084621.937701,3764035.372603,0.000000,0.000000,0.000000,

# rtk_example（流动站−基准站 ECEF 差，m）
station pos: -3978242.434800,3382841.171500,3649902.766700
(0,17)/1987, type: 0, pos: 2022.774943,-468.630735,2610.284897
(1153,15)/1987, type: 0, pos: 2022.778256,-468.637599,2610.281396

# ppp_example 末行
8476/8486, pos: -3120046.546458,4084621.475280,3764033.497483
```

### 4.2 用本树 `rnx2rtkp` 跑同样数据（交叉验证）

```bash
cd ~/iono_ops/src/learning_rtklib/data
R=~/iono_ops/src/RTKLIB-tomoji/app/rnx2rtkp/gcc/rnx2rtkp
$R -p 0 -o /tmp/lrout/daej_spp.pos rinex/daej229a00.20o rinex/daej229a00.20n 2>/dev/null
$R -p 2 -f 2 -o /tmp/lrout/rtk.pos 07590920.05o 30400920.05o 07590920.05n 2>/dev/null
```

SPP（900 行全部 Q=5）：

```
% program   : rnx2rtkp ver.2.4.2
% obs start : 2020/08/16 00:00:00.0 GPST (week2119      0.0s)
% obs end   : 2020/08/16 00:14:59.0 GPST (week2119    899.0s)
2119      0.000   36.399441964  127.374476315   127.9834   5   9   5.3448   3.5840  13.4603   0.7523  -3.4395  -6.0647   0.00    0.0
```

加 `-e` 输出 ECEF 后，第 1 s 历元为 `-3120047.6510 4084622.7768 3764034.8790`，与 `spp_example` 的 `2020,8,16,0,0,1,-3120047.650995,4084622.776844,3764034.879003` 一致。

RTK（115 行全部 Q=1）：

```
% ref pos   : 35.132063648  139.624300357    75.4015
1316 518400.000   35.160872529  139.613836777    69.8714   1   7   0.0058   0.0044   0.0136   0.0022  -0.0047  -0.0055   0.00   24.9
1316 518430.000   35.160872522  139.613836807    69.8647   1   7   0.0059   0.0046   0.0136   0.0024  -0.0046  -0.0054   0.00   40.8
```

把基准站改成 RINEX 头坐标 `-r -3978242.4348 3382841.1715 3649902.7667` 并加 `-e`，首历元“流动站−基准”= `2022.7749 -468.6307 2610.2849`，与 `rtk_example` 首行 `2022.774943,-468.630735,2610.284897` 一致。Debian 2.4.3 b34 的 `/usr/bin/rnx2rtkp` 同命令也给 115×Q1、首行完全相同。

## 5. 参数表

### 5.1 `rnx2rtkp`（2.4.2，本机 `-?` 摘录）

| 旗标 | 默认 | 说明 |
| --- | --- | --- |
| `-p mode` | 2 | 0 single / 1 dgps / 2 kinematic / 3 static / 4 moving-base / 5 fixed / 6 ppp-kinematic / 7 ppp-static |
| `-f freq` | 2 | 相对定位用频点：1 L1 / 2 L1+L2 / 3 L1+L2+L5 |
| `-m mask` | 15 | 截止高度角（°） |
| `-v thres` | 3.0 | ratio 阈值，0 = 不做 AR |
| `-e` / `-a` | llh | 输出 ECEF / ENU 基线 |
| `-r x y z` | 单点平均 | 基准站 ECEF（m）；不给就用基准站 SPP 平均（坑 5） |
| `-k file` | —— | 配置文件；命令行优先于文件 |
| `-ts/-te/-ti` | 全段 | 起止时间与间隔 |
| `-x level` | 0 | trace 级别 |
| 无 `-sys` | —— | 2.4.2 没有该旗标（坑 4） |

### 5.2 示例里写死的 `prcopt_t`

| 示例 | mode | nf | navsys | 其他 |
| --- | --- | --- | --- | --- |
| spp_example | `prcopt_default` 原样：mode 0 | 2 | GPS(1) | `elmin=0.261799`（15°）；stdout 开头打印全部选项；**唯一接受参数**：`spp_example <nav> <obs>` |
| rtk_example | `PMODE_KINEMA`(2) | 2 | GPS | `modear=2`（instantaneous AR）、`refpos=0`、`rb=sta.pos`（最后读入文件的头坐标，即基准站） |
| ppp_example | `PMODE_PPP_STATIC`(7) | 见源码 | GPS | `sateph=EPHOPT_PREC`，igr 精密轨道+钟差 |

除 `spp_example` 可传文件外，改参数 = 改 `.cpp` 重新 `make`，没有命令行开关。

## 6. 坑（现象 → 原因 → 一条修复命令）

1. **`fatal error: rtklib.h: No such file or directory`** → 仓库 `CMakeLists.txt` 默认你已 `sudo make install` 到 `/usr/local`，`include_directories` 被注释掉 → `cmake .. -DCMAKE_CXX_FLAGS="-I$HOME/iono_ops/opt/rtklib242/include" -DCMAKE_EXE_LINKER_FLAGS="-L$HOME/iono_ops/opt/rtklib242/lib"`。
2. **程序 exit 0 却什么解都没有；`rinex_example` 打印 `nav : n=0` `obs : n=0`，`spp_example` 只打 19 行选项** → 数据路径写死为 `../data/...`，只在 `build/` 里运行才对，读不到文件也不报错 → `cd ~/iono_ops/src/learning_rtklib/build && ./spp_example`（或只对 spp：`./build/spp_example data/rinex/daej229a00.20n data/rinex/daej229a00.20o`，本机 900 行）。
3. **对 rtklib-explorer / 2.4.3 头文件编译报 `'struct nav_t' has no member named 'lam'`、`'FREQ1' was not declared`、`'struct sta_t' has no member named 'marker'`** → 示例按 2.4.2 API 写；新版本删了 `lam`、改名 `FREQL1`、`markerno` → 用 README 指定的 tomojitakasu master：`git clone --depth 1 https://github.com/tomojitakasu/RTKLIB ~/iono_ops/src/RTKLIB-tomoji`。
4. **`rnx2rtkp -p 0 -sys G …` 只打印 usage，没有 `.pos`（exit 仍为 0）** → 2.4.2 的 `rnx2rtkp` 不认 `-sys`（那是 demo5/EX 的旗标），遇到未知旗标就打印帮助 → 去掉 `-sys`，要限系统请用 conf：`echo "pos1-navsys =1" > gps.conf && $R -k gps.conf -p 0 rinex/daej229a00.20o rinex/daej229a00.20n`。
5. **同一 RTK 数据，自己算的坐标和示例/别人差 ~0.4 m 高程**（本机：默认 `69.8714` m，用头坐标 `70.2724` m） → 不给 `-r` 时 `rnx2rtkp` 用基准站 SPP 平均当基准，`rtk_example` 用 RINEX 头 APPROX → 固定基准：`$R -p 2 -f 2 -r -3978242.4348 3382841.1715 3649902.7667 07590920.05o 30400920.05o 07590920.05n`。
6. **`build/` 里突然多出 10 MB 的 `spp.trace`、2.6 MB 的 `ppp.trace`** → 库带 `-DTRACE` 编译，示例里 `traceopen()`+`tracelevel(4)` → 读完就删或改级别：`rm -f ~/iono_ops/src/learning_rtklib/build/*.trace`（要保留调试就把 `tracelevel(4)` 改成 `2` 再 `make`）。
7. **`spp_example` 第一行时间是 `2020,8,15,23,59,60`** → 该历元 `sol.time` 比 00:00:00 早不到 1 µs，示例用 `%.0lf` 打秒被四舍五入成 60，分/时/日不进位（改成 `%.3lf` 本机仍显示 `59,60.000`）；纯显示问题，坐标就是 00:00:00 历元 → 用 rnx2rtkp 的日历时间核对：`$R -p 0 -t rinex/daej229a00.20o rinex/daej229a00.20n 2>/dev/null | grep -v '^%' | head -1`（本机 `2020/08/16 00:00:00.000   36.399441964  127.374476315   127.9834   5   9 …`）。
8. **改了 `spp_example.cpp` 里毫不相关的一行（如打印格式）后重编，900 行解变成满屏 `ret: 0, msg:lack of valid sats ns=4`** → `pntpos_process()` 里 `sol_t sol;` 未初始化，而 2.4.2 `pntpos.c:321` 用 `sol->rr` 作迭代初值，栈上垃圾值随编译布局变化（本机原样编译碰巧为 0）→ 零初始化：`sed -i 's/^    sol_t sol;$/    sol_t sol = {};/' spp_example.cpp && make -C build`（本机修后恢复 900 行）。
9. **终端被 `processing : … Q=5` 刷屏上万字符** → `rnx2rtkp` 把进度写到 stderr 且不换行 → 追加 `2>/dev/null`：`$R -p 0 -o out.pos rinex/daej229a00.20o rinex/daej229a00.20n 2>/dev/null`。
10. **不加 sudo 执行 README 的 `make install`，报 Permission denied**（本机 `/usr/local/lib` 不可写） → README 用 `sudo make install` 装到系统目录；共享机器不宜 → `cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/iono_ops/opt/rtklib242 && make install`。

## 7. 诚实边界

- 无许可证：可读可本地跑，复制示例进自己的项目前先联系作者；RTKLIB 部分按 BSD-2-Clause。
- 2020-08 后停更；内容是个人学习记录，README 自己留着问题（“PMODE_KINEMA 和 PMODE_FIXED 怎么理解？”、DGPS “TODO”）。适合入门读函数调用顺序，不是 RTKLIB 的权威文档——权威以 RTKLIB 手册与源码为准。
- 只覆盖 GPS；样例数据是 2005 GSI（日本）和 2020 DAEJ（韩国大田），无北斗/Galileo 例子。
- 示例没有命令行参数、不写 `.pos`、`ppp_example` 只打印 ECEF，不做精度评估；本机未与 IGS 周解坐标对比，本文不给精度数字。
- 本机只验证了 tomojitakasu 2.4.2 p13；2.4.3 分支和 demo5/EX 需改代码（坑 3），未尝试移植。

## 8. 交叉链接

- RTKLIB 本体与配置：[rtklib](./rtklib.md) · 低成本改进版：[rtklib-explorer](./rtklib-explorer.md) · 多系统/增强版：[mrtklib](./mrtklib.md)
- 另一个 PPP 学习仓：[ppp-rtklib](./ppp-rtklib.md) · 纯 Python 重写：[rtklib-py](./rtklib-py.md)
- Python 绑定：[pyrtklib](./pyrtklib.md) · [pyrtklib-demo5](./pyrtklib-demo5.md) · 调 rnx2rtkp+出图脚本：[pyrtklib-rinex](./pyrtklib-rinex.md)
- RINEX 预检：[georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · 老式 QC：[teqc](./teqc.md)
