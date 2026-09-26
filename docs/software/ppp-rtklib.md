# ppp_rtklib · 从 RTKLIB 2.4.2 抽出的 PPP 学习代码操作手册

目录：[`PROJECTS.json` → `ppp_rtklib`](../../PROJECTS.json) · 上游 <https://github.com/mulin33/ppp_rtklib> · **无 LICENSE 文件**（默认保留所有权利；源码头保留 Takasu RTKLIB 版权声明，原 RTKLIB 为 BSD-2-Clause）· tip **`c9f133c`**（2025-06-25）· ★4 · 内核 **RTKLIB 2.4.2**（`.pos` 头 `ver.2.4.2`）· 原生工程 **VS2015 `RTKLIB_242.vcxproj`**（Windows）· 本机：gcc **14.2.0** 改编译参数后 Linux 可编译 → 二进制 **238192** B；仓内 ALGO 2022-03-08 全天 → **2880** 历元全 Q=6，与仓内 Windows 结果 `result/ppp.pos` **逐行一致** · **2026-09-26 00:53–00:58 EDT**

> 岗位：**读懂 RTKLIB 的 PPP 流程**用的“拆出来的小代码”——一个 `main()`，参数写死在 C 里，只做静态 PPP、浮点解。它是 2023 年“GNSS 定位新技术及数据处理方法”课程作业（仓内 `软件说明.docx`），**不是生产 PPP 软件**。要可靠的 PPP 结果请用 [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md)。

## 1. 它解决什么问题

完整 RTKLIB 的 `rnx2rtkp` → `postpos.c` → `rtkpos.c` → `ppp.c` 调用链夹着 RTK、SBAS、实时流、配置解析等大量代码，初学者很难只看 PPP。作者把 PPP 相关函数按功能拆成 ~24 个 `.c`（合计约 **12.6k** 行），`main()` 只有“设参数 → 读文件 → 逐历元滤波 → 写 `.pos`”四步，便于单步调试。

| 术语 | 含义 |
| --- | --- |
| PPP（精密单点定位） | 只用**一台**接收机 + 精密轨道/钟差；静态几小时后可到厘米–分米级。`.pos` 中 **Q=6** |
| SP3 | 卫星精密轨道（本仓 `gfz22002.sp3`：GFZ，15 min 间隔） |
| CLK | RINEX 钟差文件（本仓 `gfz22002.clk`），给卫星钟差 |
| ATX | 天线相位中心文件（本仓 `igs14.atx`），卫星与接收机天线改正 |
| 消电离层组合（IFLC） | L1/L2 线性组合消去一阶电离层延迟；RTKLIB `ionoopt=IONOOPT_IFLC` |
| ZTD / 对流层 | 天顶对流层延迟：可用 Saastamoinen 模型（`TROPOPT_SAAS`）改正，或作为参数估计（`TROPOPT_EST`） |
| 模糊度 / float / fix | 载波整周数未知量；本代码**不做 PPP-AR**，永远是 float（Q=6，不会出 Q=1） |
| RTK / demo5 | 对比概念：RTK 需基准站双差；demo5 是 rtklibexplorer 的分支，本仓与其**无关**（demo5 见 [rtklib-explorer](./rtklib-explorer.md) / [pyrtklib-demo5](./pyrtklib-demo5.md)） |

## 2. 仓内有什么

| 路径 | 内容 |
| --- | --- |
| `code/ppp_rtklib/*.c *.h` | 源码（注释为 **GBK** 编码，Linux 下乱码需 `iconv`） |
| `code/ppp_rtklib/RTKLIB_242.vcxproj` / `Solution1.sln` | VS 工程；**编译清单不含 `r_clk.c`** |
| `code/ppp_rtklib/Debug/` | 作者提交的 `.obj`、`RTKLIB_242.exe`（Windows 可执行，Linux 不能跑） |
| `code/Data/` | `algo0670.22o`（ALGO 站 RINEX 2.11，30 s，5.9 MB）、`brdc0670.22n`、`gfz22002.sp3/.clk`、`igs14.atx` |
| `code/result/` | 作者 Windows 跑出的 `ppp.pos`（2890 行）、`ppp.trace`、`rtkplot.exe` |
| `PPP_process.xmind` / `软件说明.docx` | 流程脑图、课程作业说明 |

源文件分工（按函数名归纳）：

| 文件 | 作用 |
| --- | --- |
| `ppp_main.c` | 入口：写死参数与文件路径 |
| `ppp_process.c` | `prcopt_default`/`solopt_default`、`importData()` 读文件、`process()`→`procpos()` 逐历元 |
| `ppp.c` | PPP 卡尔曼滤波（状态更新、残差、相位偏差） |
| `pntpos.c` | SPP 初值 |
| `preceph.c` / `r_sp3.c` / `rinex.c` | 精密星历钟差插值 / 读 SP3 / 读 RINEX OBS/NAV/CLK |
| `r_atx.c` / `setpcv.c` | 读 ATX、给卫星与接收机设置天线参数 |
| `error_model.c` | `tropmodel` / `tropmapf` / `ionmodel` / `windupcorr` |
| `ephemeris.c` `sort.c` `satsysno.c` `coordinate.c` `time_string.c` `matrix.c` | 广播星历、去重排序、卫星编号、坐标与时间、矩阵 |
| `solution.c` / `outhead.c` / `trace.c` | 写 `.pos`、文件头、调试日志 |

## 3. 在 Linux 上编译（本机实测）

仓库只提供 VS 工程；Linux 下需要四处处理：缺 POSIX 头、GCC 14 把隐式声明当错误、`r_clk.c` 与 `rinex.c` 重复定义 `readrnxc`、`ppp_main.c` 路径用 Windows 反斜杠。**不改原仓**，在副本里做：

```bash
git clone https://github.com/mulin33/ppp_rtklib.git        # ~153 MB（含 .obj/.exe/数据）
mkdir -p build/src build/result && cd build
cp ../ppp_rtklib/code/ppp_rtklib/*.[ch] src/
ln -s ../ppp_rtklib/code/Data Data
rm src/r_clk.c                                              # VS 工程也不编它
sed -i 's#\.\.\\\\Data\\\\#../Data/#g; s#\.\.\\\\result\\\\#../result/#g' src/ppp_main.c
cd src
ls *.c | xargs -P4 -I{} gcc -c -O2 -w -fpermissive \
  -include dirent.h -include sys/stat.h -include sys/time.h {}
gcc -o ../ppp_rtklib *.o -lm -lpthread
```

本机：gcc 14.2.0，编译 < 3 s，`ppp_rtklib` **238192** B。`-w` 只是压掉大量旧式警告；`-fpermissive` 让 GCC 14 把隐式函数声明/指针类型不符降级为警告（原代码 `&stas` 传给 `sta_t*` 参数，地址相同，不影响结果）。

## 4. 端到端实跑

必须在 `src/` 里运行（路径相对 `../Data`、`../result`）：

```bash
cd build/src
time ../ppp_rtklib > ../run.out 2>&1; echo exit=$?
tr '\r' '\n' < ../run.out | iconv -f GBK -t UTF-8 -c | head -3
tr '\r' '\n' < ../run.out | iconv -f GBK -t UTF-8 -c | tail -4
```

```text
real	0m3.959s
exit=0
processing : 2022/03/08 00:00:00 Q=0
processing : 2022/03/08 00:00:30 Q=6
processing : 2022/03/08 00:01:00 Q=6
processing : 2022/03/08 23:59:30 Q=6预处理错误!
---------------input file success!---------------

---------------数据处理成功!---------------
```

“processing” 行共 2880 条（1 条 Q=0 + 2879 条 Q=6）。最后那句“预处理错误!”是**假警报**（坑 5）。输出：

```text
% program   : RTKLIB ver.2.4.2
% inp file  : ../Data/algo0670.22o
% inp file  : ../Data/brdc0670.22n
% inp file  : ../Data/gfz22002.sp3
% inp file  : ../Data/gfz22002.clk
% obs start : 2022/03/08 00:00:00.0 GPST (week2200 172800.0s)
% obs end   : 2022/03/08 23:59:30.0 GPST (week2200 259170.0s)
%  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio
2022/03/08 00:00:00.000   45.955798875  -78.071376955   204.5710   6   7   2.0254   1.5442   3.5624  -0.3914  -0.4585   1.0064   0.00    0.0
2022/03/08 00:00:30.000   45.955798860  -78.071376411   205.2238   6   7   1.4316   1.0900   2.5167  -0.2707  -0.3169   0.7086   0.00    0.0
...
2022/03/08 23:59:30.000   45.955799491  -78.071373844   206.9226   6   7   0.0206   0.0176   0.0390   0.0033  -0.0015  -0.0108   0.00    0.0
```

**与作者 Windows 结果对拍：**

```bash
diff <(grep -v '^%' ../result/ppp.pos) <(grep -v '^%' ../../ppp_rtklib/code/result/ppp.pos) | grep -c '^<'
# 0      ← 2880 行数据完全一致（仅头部路径分隔符不同）
```

`ns` 范围 5–10；`result/ppp.trace` **13.7 MB**（`tracelevel(3)`）。

### 4.1 精度核查：默认参数高程偏 ~6 m

IGS 站点 API（`network.igs.org/api/public/stations/?name=ALGO`）给 ALGO 概略坐标 `45.9558004 -78.0713676 200.829 m`（只精确到 ~0.1 m）。对末历元：

| 方案 | 末历元 高程 (m) | dN / dE / dU (m) |
| --- | ---: | --- |
| ppp_rtklib **默认**（`ionoopt=0` 不改电离层、`tropopt=0` 不改对流层） | 206.9226 | −0.101 / −0.483 / **+6.093** |
| ppp_rtklib + `IONOOPT_IFLC` + `TROPOPT_SAAS` | 200.7503 | +0.016 / −0.317 / **−0.079** |
| ppp_rtklib + `IONOOPT_IFLC` + `TROPOPT_EST` | 208.4716 | −0.129 / −0.324 / **+7.642**（坑 7） |
| apt `rnx2rtkp` 2.4.3，`ppp-static` dual-freq + est-ztd，同数据 | 201.0324 | +0.021 / −0.300 / +0.203 |
| [pyrtklib-demo5](./pyrtklib-demo5.md)（EX 2.5.0）同配置 | 201.0317 | +0.021 / −0.300 / +0.202 |

结论：`软件说明.docx` 说结果“均在厘米级”，看的是 `sdn/sde/sdu`（滤波器**形式**精度，末历元 2–4 cm），**不是真误差**；默认配置真实高程偏差约 6 m。改两行即可回到分米内（dE≈−0.3 m 各方案一致，多半来自参考坐标本身是概略值）。

改法（在 `ppp_main.c` 的 `prcopt.navsys = SYS_ALL;` 后加）：

```c
prcopt.ionoopt = IONOOPT_IFLC;   /* 消电离层组合 */
prcopt.tropopt = TROPOPT_SAAS;   /* Saastamoinen 模型；EST 在本仓不可用 */
```

## 5. 参数表

### 5.1 `ppp_main.c` 里能改的量

| 代码 | 仓内值 | 说明 |
| --- | --- | --- |
| `prcopt.mode` | `PMODE_PPP_STATIC`（=7） | 本仓 2.4.2 编号：6 PPP-kinematic、7 PPP-static、8 PPP-fixed |
| `prcopt.navsys` | `SYS_ALL` | 系统掩码；实际可用受 SP3/CLK 覆盖限制 |
| `prcopt.sateph` | `EPHOPT_PREC` | 用 SP3/CLK；改 BRDC 就不是 PPP 了 |
| `prcopt.glomodear` | 0 | GLONASS AR 关（本来也不做 AR） |
| `solopt.timef` | 1 | 时间写成 `yyyy/mm/dd hh:mm:ss` |
| `solopt.posf` | `SOLF_LLH` | 输出纬经高；`SOLF_XYZ` 为 ECEF |
| `fopt.satantp/rcvantp` | `igs14.atx` | 卫星/接收机天线文件 |
| `fopt.obs/nav/sp3/clk` | 见 `code/Data/` | **四个都必须给**，缺一个 `importData` 失败 |
| `outfile` / `traceopen` / `tracelevel` | `../result/ppp.pos` / `ppp.trace` / 3 | 输出与调试日志 |

### 5.2 `ppp_process.c` 中 `prcopt_default` 关键默认

| 字段 | 默认 | 影响 |
| --- | --- | --- |
| `nf` | 2 | L1+L2 |
| `elmin` | 15° | 截止高度角 |
| `ionoopt` | 0（off） | **不改电离层**→ 高程大偏差 |
| `tropopt` | 0（off） | **不改对流层** |
| `modear` | 1 | 对 PPP 无效（未实现 AR） |
| `err[]` | `{100, 0.003, 0.003, 0, 1}` | 观测噪声模型 |
| `thresslip` | 0.05 m | 周跳（几何无关组合）阈值 |
| `maxinno` / `maxgdop` | 30 / 30 | 新息与 GDOP 剔除门限 |

### 5.3 `.pos` 列

| 列 | 含义 |
| --- | --- |
| `GPST` | 日期 + 时间 |
| `latitude/longitude/height` | WGS84 纬经度与**椭球高**（m） |
| `Q` | 本程序只会出 6（PPP）；首历元屏显 Q=0 表示尚未有解 |
| `ns` | 卫星数 |
| `sdn/sde/sdu`、`sdne/sdeu/sdun` | 形式标准差/协方差（m） |
| `age` / `ratio` | PPP 下恒为 0.00 / 0.0 |

## 6. 坑（现象 → 原因 → 修复）

1. **`clutter.c: error: unknown type name 'DIR'`** → 非 WIN32 分支用了 `opendir` 却没包含 `<dirent.h>` → 编译加 `-include dirent.h -include sys/stat.h -include sys/time.h`
2. **`error: implicit declaration of function 'ppp_process'` / `passing argument 7 of 'importData' from incompatible pointer type`** → 老代码缺原型，GCC 14 默认报错 → 加 `-fpermissive`（或 `-std=gnu89 -Wno-error=incompatible-pointer-types`）
3. **链接失败 `multiple definition of 'readrnxc'`** → `r_clk.c` 与 `rinex.c` 都定义了它，VS 工程并不编 `r_clk.c` → `rm src/r_clk.c`
4. **退出码 0、屏幕打印“input file success / 数据处理成功”，但 `result/` 空；当前目录多出名为 `..\result\ppp.pos` 的 192 B 文件** → `ppp_main.c` 写死 `"..\\Data\\..."`，Linux 把反斜杠当普通字符 → `sed -i 's#\.\.\\\\Data\\\\#../Data/#g; s#\.\.\\\\result\\\\#../result/#g' src/ppp_main.c`，并在 `src/` 下运行
5. **成功跑完也打印“预处理错误!”** → `process()` 声明返回 `int` 却没有 `return`，返回值是随机的（`ppp_process()` 同理）；“success”也是无条件打印 → 以 `.pos` 为准：`grep -vc '^%' ../result/ppp.pos`（本机 2880）
6. **结果高程比 IGS 坐标高约 6 m，而 sdu 只有 4 cm** → 默认 `ionoopt/tropopt=0`，未改电离层与对流层；sd* 是形式精度 → 在 `ppp_main.c` 加 `prcopt.ionoopt = IONOOPT_IFLC; prcopt.tropopt = TROPOPT_SAAS;` 重编
7. **改成 `TROPOPT_EST` 反而更差（dU≈+7.6 m）** → `ppp.c` 里 `udtrop_ppp(rtk)` 被注释掉，对流层参数从未初始化 → 用 `TROPOPT_SAAS`，或 `sed -i 's#/\*if (rtk->opt.tropopt>=TROPOPT_EST) {#if (rtk->opt.tropopt>=TROPOPT_EST) {#' src/ppp.c` 后手工去掉配对的 `}*/`（本机**未验证**此改法）
8. **中文注释乱码** → 源文件是 GBK → `iconv -f GBK -t UTF-8 src/ppp_process.c | less`
9. **每跑一次写 13.7 MB trace** → `tracelevel(3)` → `sed -i 's/tracelevel(3)/tracelevel(0)/' src/ppp_main.c`
10. **把 mode 数字搬到 demo5/EX 出错** → 本仓 `PMODE_PPP_STATIC=7`，EX（[pyrtklib-demo5](./pyrtklib-demo5.md)）是 8、7 为 PPP-kinematic → 永远写常量名，不写数字

## 7. 诚实边界

- **无许可证**：仓库没有 LICENSE，转载/再分发前需联系作者；源自 RTKLIB 的部分仍受原 BSD-2-Clause 约束。
- 只支持**静态 PPP 浮点解**；无 PPP-AR、无动态验证、无实时流、无配置文件，所有参数需改 C 重编。
- 仅随仓一天 ALGO 数据验证；换数据要自备同期 SP3/CLK（本机此前访问 CDDIS 返回 `425 Bad IP`，可改用 IGS BKG/ESA 等镜像，本页**未**演示下载）。
- 部分模型被注释掉（对流层估计、SBAS 对流层等），精度结论只适用于本页核查的配置。
- 作者仓含 `.obj`/`.exe`/`.pdb` 等构建产物，克隆 ~153 MB。

## 8. 交叉链接

- 完整 RTKLIB CLI（同类 PPP 可直接 `rnx2rtkp -p 7`）：[rtklib](./rtklib.md)；demo5/EX：[rtklib-explorer](./rtklib-explorer.md)
- Python 调 RTKLIB：[pyrtklib](./pyrtklib.md)（2.4.3）· [pyrtklib-demo5](./pyrtklib-demo5.md)（EX 2.5.0）
- 生产级 PPP / PPP-AR：[pride-pppar](./pride-pppar.md) · [ginan](./ginan.md) · Python PPP：[cssrlib](./cssrlib.md)
- RINEX 检查：[gfzrnx](./gfzrnx.md) · [georinex](./georinex.md)
