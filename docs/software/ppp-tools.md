# ppp-tools · 时间实验室向 RINEX→PPP 脚本集操作手册

目录：[`PROJECTS.json` → `ppp-tools`](../../PROJECTS.json) · 上游 <https://github.com/aewallin/ppp-tools> · master **`e77e351`**（2026-03-08 04:07 EDT，“update readme”）· **无 tag / 无 PyPI / 无 setup.py** · **GPL-2.0** · ★**121** · Python 125232 B + Batchfile 2926 B · 实测 2026-09-26 05:05–05:18 EDT（CPython 3.13.5，RTKLIB **2.4.2 p13** `71db0ff`，gcc 14.2.0）

> 岗位：VTT MIKES（芬兰）时间实验室 Anders Wallin 的**胶水脚本**：下 RINEX（实验室 FTP/HTTPS）+ 下 IGS/CODE 轨道钟差 → 解压/Hatanaka → 调**外部** PPP 引擎 → 统一成 `results/<站>/<站>.<MJD>.<rapid|final>.<引擎>.txt`（逐历元 lat/lon/h/**接收机钟 ns**/ZTD）→ 两站钟差相减做时间传递。**本身不解算**。冲突时：上游源码 > 本文。  
> 易混：[ppp-rtklib.md](./ppp-rtklib.md) 是 **mulin33/ppp_rtklib**（RTKLIB PPP 学习代码），**不是**本仓库里的 `ppp_rtklib.py`。

## 1. 用途与边界

| 模块 | 做什么 | 外部依赖 | 本文状态 |
| --- | --- | --- | --- |
| `ppp_rtklib.py` | `run(station, dt)` → 调 `rnx2rtkp`（`common/rtklib_opts1.conf`，ppp-static、combined、GPS-only） | RTKLIB `rnx2rtkp` | **实测**（需 2 处修补，见 §3） |
| `ppp_glab.py` | 同上，调 `gLAB_linux`，并按站延迟改钟 | ESA gLAB（README 写 v5.5.1） | 未测 |
| `ppp_gpsppp.py` | 调 NRCan 系 `gpspace`（GPSPACE），RINEX 3 先用 `gfzrnx` 转 2.11 | GPSPACE + gfzrnx | 未测 |
| `igs_ftp.py` | 拼 CODE/IGS rapid/final 产品名并 `wget` | `wget` 3.2（PyPI） | 实测：rapid 分支 URL 已坏（§5 E1） |
| `station.py` | `Station` 类 + MIKES/PTB 站定义（含 `ref_dly/cab_dly/int_dly_p1/p2` 延迟） | `wget` | 实测 `mi05.get_rinex` 可下（8543352 B） |
| `bipm_ftp.py` | 下 Circular-T / UTCr（`ftp2.bipm.org`） | ftplib、pytz、numpy | 未测 |
| `ppp_common.py` | 结果文件读写、两站 `diff_stations()` | — | 实测（写、读、`diff_stations`，§3b） |

**不做：** 不含 PPP 算法；无 CLI、无 `--help`、无参数解析（见 §2）；不出 CGGTTS（→ [rnx2cggtts.md](./rnx2cggtts.md)/[cggtts.md](./cggtts.md)）；不做 PPP-AR（RTKLIB 2.4.2 PPP 只有浮点解，Q=6）；不做实时——**未在真接收机测试**，只处理日文件。

## 2. 安装

没有打包，直接 clone，**把仓库根当工作目录**（`station.get_rinex()` 用 `os.getcwd()`，`run()` 用 `prefixdir`，两者须相同）。

```bash
export TMPDIR=/tmp/ppptools-man PIP_CACHE_DIR=/tmp/ppptools-man/pipcache
cd /tmp/ppptools-man
git clone https://github.com/aewallin/ppp-tools.git          # e77e351
python3 -m venv venv && venv/bin/pip install numpy pytz wget matplotlib hatanaka
#   实装：numpy 2.5.3 / pytz 2026.4 / wget 3.2 / matplotlib 3.11.2 / hatanaka 2.8.1
git clone https://github.com/tomojitakasu/RTKLIB.git           # 默认分支 master = v2.4.2-p13 (71db0ff, 2018-01-30)
make -C RTKLIB/app/rnx2rtkp/gcc                                # 约 20 s，出 rnx2rtkp 2261808 B
mkdir -p bin && ln -s $PWD/RTKLIB/app/rnx2rtkp/gcc/rnx2rtkp bin/ \
  && ln -s $PWD/venv/bin/crx2rnx bin/CRX2RNX                   # 脚本写死大写 CRX2RNX
export PATH=$PWD/bin:$PATH
```

“入口脚本 `--help` 原文”：**不存在**。`python ppp_rtklib.py --help` 忽略参数直接跑 `__main__`：

```text
  File ".../ppp_rtklib.py", line 272, in <module>
    station1 = station.usno
AttributeError: module 'station' has no attribute 'usno'
```

`example1.py` 仍是 Python 2（`print "..."` → `SyntaxError`），且 `import ppp_nrcan`（仓内无此文件）；其余 17 个 `.py` 在 3.13 下 `py_compile` 通过。

## 3. 例子：WTZR 2026-08-04 全天 PPP（真实数据）

数据（BKG 免账号 HTTPS）：`WTZR00DEU_R_20262160000_01D_30S_MO.crx.gz`（RINEX 3.04，Leica GR50，LEIAR25.R3；IGS 最终钟含该站 `AR WTZR`）+ `WTZR..._MN.rnx.gz`；产品 `IGS0OPSFIN_20262160000_01D_15M_ORB.SP3.gz` / `_30S_CLK.CLK.gz` / `IGS0OPSFIN_20262140000_07D_01D_ERP.ERP.gz`（IGS20 最终）。

脚本只认老短名，故**手工摆放**（`download()`/`get_rinex()` 见文件已存在即跳过）：

```bash
cd ppp-tools; mkdir -p stations/WTZR products/CODE_rapid
cp WTZR00DEU_R_20262160000_01D_30S_MO.crx.gz stations/WTZR/WTZR2160.26D.Z   # gzip 内容，.Z 名也能 gunzip
zcat IGS0OPSFIN_..._30S_CLK.CLK.gz > products/CODE_rapid/COD24302.CLK_R      # 周 2430 周二
zcat IGS0OPSFIN_..._15M_ORB.SP3.gz > products/CODE_rapid/COD24302.EPH_R
zcat IGS0OPSFIN_..._ERP.ERP.gz     > products/CODE_rapid/COD24302.ERP_R
```

**修补 1**（否则 rnx2rtkp 读不到 ATX 直接退出）：`common/rtklib_opts1.conf` 里写死 `/home/anders/Desktop/ppp-tools/common/igs14.atx`：

```bash
sed -i 's#/home/anders/Desktop/ppp-tools/common/igs14.atx#'$PWD'/common/igs20.atx#' common/rtklib_opts1.conf
```

**修补 2**：`run()` 不传广播星历（`navfile` 被注释），RTKLIB 2.4.2 报 `no nav data`。用驱动脚本把 NAV 拼进命令串（命令是字符串拼接 + `shell=True`）：

```python
import sys, os, datetime
sys.path.insert(0, "/tmp/ppptools-man/ppp-tools"); os.chdir("/tmp/ppptools-man/ppp-tools")
import station, ppp_rtklib
ppp_rtklib.rtklib_binary = "rnx2rtkp /tmp/ppptools-man/WTZR_MN.rnx"
wtzr = station.Station(); wtzr.name = wtzr.receiver = "WTZR"
wtzr.ftp_server = "https://example.invalid"; wtzr.ftp_dir = "/"
wtzr.rinex_filename = wtzr.rinex4                      # -> WTZR2160.26D.Z
ppp_rtklib.run(wtzr, datetime.datetime(2026, 8, 4, 12), rapid=False, prefixdir=os.getcwd())
```

真实 stdout（05:11:29–05:11:32 EDT，墙钟 **3.90 s**；RTKLIB 的 `processing :` 进度行略）：

```text
download start  2026-09-26 09:11:29.195556
download Done  2026-09-26 09:11:29.195591
 run start: 2026-09-26 09:11:29
   Station: WTZR
       DOY: 216
     RINEX: /tmp/ppptools-man/ppp-tools/stations/WTZR/WTZR2160.26D.Z
       CLK: /tmp/ppptools-man/ppp-tools/products/CODE_rapid/COD24302.CLK_R
unzipping:  /bin/gunzip -f /tmp/ppptools-man/ppp-tools/temp/WTZR2160.26D.Z
Hatanaka uncompress:  CRX2RNX /tmp/ppptools-man/ppp-tools/temp/WTZR2160.26D
input  /tmp/ppptools-man/ppp-tools/temp/WTZR2160.26O
   run end: 2026-09-26 09:11:32
   elapsed: 3.70 s
clk len= 5760
pos len= 2880
2880
 wrote results to  /tmp/ppptools-man/ppp-tools/results/WTZR/WTZR.61256.final.rtklib.txt
```

（脚本里的时间是 `utcnow()`，即 UTC；上面 09:11 UTC = 05:11 EDT。）结果文件：

```text
# Year	Month	Day	Hour	Min	Sec	Lat(deg)	Lon(deg)	Height(m)	Clock(ns)	ZTD(m)
2026	8	4	0	0	0	49.144201	12.878916	666.034700	-131498.307000	2.335900
2026	8	4	0	0	30	49.144201	12.878916	666.034700	-131498.297000	2.335800
...
2026	8	4	23	59	30	49.144201	12.878916	666.034700	-131490.451000	2.260600
# end
```

引擎原始 `temp/out.txt`：2880 历元全 Q=6（PPP 浮点），ns=9，`antenna1 : LEIAR25.R3 LEIT (0.0000 0.0000 0.0710)`；全天均值 XYZ **4075580.2184 / 931854.1675 / 4801568.3556 m**；接收机钟约 −131.5 µs，日漂 +7.9 ns。

### 3b. 时间传递用法：MI05 − WTZR 双差（2026-09-20，IGS rapid）

用仓内**原样**站定义 `station.mi05`（VTT MIKES，Septentrio PolaRx5TR，`https://monitor.mikes.fi/ftp/GNSS/MI05/RINEX_v3_24h/`，免账号；`station.mi05.get_rinex()` 05:15 EDT 实下 `MI052630.26o.gz` 8543352 B，RINEX 3.04）+ 上面的 WTZR 定义；产品 `IGS0OPSRAP_20262630000_01D_05M_CLK/15M_ORB/01D_ERP` 摆成 `COD24370.*_R`；NAV 用 WTZR 的 `_MN`：

```python
for s in (station.mi05, wtzr):
    ppp_rtklib.run(s, dt, rapid=True, prefixdir=os.getcwd())
t, d = ppp_common.diff_stations(os.getcwd(), station.mi05, wtzr, dt, "rapid", "rtklib")
```

真实输出（05:16:33–05:16:41 EDT，墙钟 7.59 s，两站各 3.60/3.66 s）：

```text
/tmp/ppptools-man/ppp-tools/stations/MI05/MI052630.26o.gz  already exists, not downloading
 wrote results to  .../results/MI05/MI05.61303.rapid.rtklib.txt
 wrote results to  .../results/WTZR/WTZR.61303.rapid.rtklib.txt
read 2880 points from MI05.61303.rapid.rtklib.txt
read 2880 points from WTZR.61303.rapid.rtklib.txt
diff MI05 - WTZR : 2880 points
MI05-WTZR n=2880 mean=107.971 ns std=4.394 ns p2p=20.786 ns
first 2026-09-20 00:00:00 112.437 last 2026-09-20 23:59:30 102.987
```

这是**未改正**原始差：`mi05` 定义了 `ref_dly=5.092`、`cab_dly=96.2`、`int_dly_p1/p2=20.17/18.18 ns`，按 `station.py` 公式应再加 −96.2 − 23.246 + 5.092 = **−114.354 ns**，但 rtklib 分支不做（坑 8）。同日 WTZR 对 IGS rapid `AR WTZR`（288 点）：均值 **−0.363 ns**、σ **0.199 ns**。

## 4. 交叉检查（独立来源）

| 对比 | 参照 | 结果 |
| --- | --- | --- |
| 坐标 | EPN CODE 日解 SINEX `COD0EPNFIN_20262160000_01D_01D_SOL.SNX.gz`（BKG EUREF），WTZR 估值 4075580.2124 / 931854.1691 / 4801568.3499 m | ΔXYZ **+6.1 / −1.6 / +5.7 mm**；ΔENU **−3.0 / −0.5 / +7.9 mm**；3D **8.5 mm** |
| 接收机钟 | IGS 最终钟 `AR WTZR`（5 min，288 点） | ppp-tools − IGS：均值 **−0.014 ns**，σ **0.310 ns**，min/max **−1.677/+0.586 ns**（峰峰 2.263 ns） |
| 包装层保真 | `temp/out.txt.stat` 原值 | 结果文件 Clock 与 `$CLK` **后向滤波**值逐点相等（最大绝对差 0）；前向−后向 均值 0.223 ns、σ 0.526 ns、max 2.337 ns |

- 符号：Clock(ns) 与 IGS `AR` 同号（和相加得 −262991.5 ns，相减 ≈ 0），即 **接收机钟 − IGST**；`ppp_common.diff_stations()` 注释写成 “IGST − Station”，**以实测为准**。
- 分时段均值：00 h +0.159、06 h −0.020、12 h −0.171、18 h +0.468、23 h −0.813 ns——日边界处发散，做连续时间传递不能直接拼日文件。
- gLAB / GPSPACE 与同日比对：未测。

## 5. 错误用例（合成）

均在上面环境里用同一驱动改一个条件（05:12 EDT 前后），退出码是 Python 进程的：

| # | 合成条件 | 表现 | 退出码 |
| --- | --- | --- | --- |
| E1 | 删 `COD24302.CLK_R` | 走 `get_CODE_rapid` 下载：`ValueError: unknown url type: 'ftp.aiub.unibe.chCODE/COD24302.CLK_R'`（服务器名缺 `http://`、旧文件名） | 1 |
| E2 | 删 `.EPH_R` | 同 E1（`...COD24302.EPH_R`） | 1 |
| E3 | 截断 `.crx`（前 3000000 B 再 gzip） | CRX2RNX 打印 `ERROR : The file seems to be truncated in the middle.`，流程**继续**：917 历元（约 7.6 h）写出结果文件 | **0（静默部分结果）** |
| E4 | 站名写错（`WTZX`，本地无文件） | 去 `https://example.invalid/...` 下载 → `URLError: Name or service not known` | 1 |
| E5 | 时间不重叠：DOY 214 产品冒充 216 | `clk len= 5760` / `pos len= 0` → `write_result_file` 里 `IndexError: list index out of range` | 1 |
| E6 | 引擎不在 PATH | `/bin/sh: 1: rnx2rtkp_missing: not found`，返回码被忽略，之后 `FileNotFoundError: .../temp/out.txt.stat` | 1 |
| E7 | 不打修补 2（原样） | `error : no nav data` → 同 E6 的 `FileNotFoundError` | 1 |
| E0 | 不打修补 1（原样） | `error : no sat ant pcv in /home/anders/Desktop/ppp-tools/common/igs14.atx` → 同上 | 1 |

规律：子进程（gunzip/CRX2RNX/rnx2rtkp）返回码**全部不检查**，错误只在之后解析文件时以 Python 异常冒出；唯一“成功”退出的是最危险的 E3。

## 6. I/O

| 方向 | 路径/格式 | 说明 |
| --- | --- | --- |
| 入 | `stations/<name>/<rinex_filename(dt)>` | 7 种短名模板 `rinex1..7`（`.yyO.Z`/`.yyo.Z`/`.yyd.Z`/`.yyD.Z`/`.yyD.gz`/`.yyo.gz`/`.yyO.gz`）；RINEX 3 内容可用，长文件名不认 |
| 入 | `products/CODE_rapid/CODwwwwd.{CLK_R,EPH_R,ERP_R}` | rtklib 分支写死 CODE rapid；`CODE_final` 用 `COD0OPSFIN_..._CLK.CLK_V2.gz` 等新名 |
| 入 | `common/rtklib_opts1.conf`、`common/igs{08,14,20}.atx` | 仓带；conf 内 ATX 路径须改 |
| 中间 | `temp/`（每次 `run()` 先清空） | `out.txt`（llh，12 位小数秒）、`out.txt.stat`（`$POS/$CLK/$TROP`） |
| 出 | `results/<name>/<receiver>.<MJD>.<rapid/final>.rtklib.txt` | 头部 `#` 运行日志；11 列 TSV：年 月 日 时 分 秒 lat lon h Clock(ns) ZTD(m) |

## 7. 坑

1. **没有入口**：无 CLI/`--help`，所有模块 `__main__` 引用已不存在的站（`station.usno`、`station.ptb`）；要自己写驱动。
2. `rtklib_opts1.conf` 写死作者机器 ATX 路径 → 原样必挂（E0）。
3. `ppp_rtklib.run()` 不给 NAV → RTKLIB 2.4.2 `no nav data`（E7）；ERP 被复制却从未传给引擎。
4. `get_CODE_rapid` URL 拼接缺协议、文件名是 2022 前旧式 `CODwwwwd.CLK_R`，**rapid 自动下载已不可用**；AIUB 在本机两次超时（05:06 `download.aiub.unibe.ch` 列目录 >120 s、05:14 `http://ftp.aiub.unibe.ch` HEAD 25 s），CODE final 自动下载未测。
5. `rtklib` 分支只实现 CODE rapid（`rapid=` 参数只影响结果文件名），想用 IGS final 只能像 §3 冒名摆放。
6. **钟差取的是后向滤波值**（`$CLK` 反转后按序号取），坐标却是 combined；前后向差最大 2.3 ns。若 stat 前后向条数不等会错位（按源码推断，未测）。
7. 结果文件 lat/lon 只留 6 位小数（≈ 0.11 m 纬向 / 0.07 m 经向），**坐标别从结果文件取**，去 `temp/out.txt`（且下次 `run()` 会清空 `temp/`）。
8. **rtklib 分支不做站延迟改正**：`ref_dly/cab_dly/int_dly_p3()` 只在 glab/gpsppp 分支用；时间传递要自己减。
9. `diff_stations()` 注释的符号与实测相反（§4）；按 MJD+“rapid/final”字符串找文件，文件名和 `rapid=` 对不上就读不到。
10. 截断 RINEX 静默出半天结果、退出码 0（E3）——批处理要自己查历元数。
11. 配置 `pos2-armode=fix-and-hold` 在 2.4.2 PPP 无效（全 Q=6）；`navsys=1` 只用 GPS；IGS20 产品配 README 默认 igs14.atx 不一致（本文用仓带 igs20.atx）。
12. `Station.__init__` 里 `self.rinex3 = False`、`self.antex = True` **覆盖了同名方法**：`st.rinex_filename = st.rinex3` → `TypeError: 'bool' object is not callable`（实测）。绕开 `lambda d: station.Station.rinex3(st, d)` 后，小写 `.26d` 解压出 `.26o` 而脚本传 `.26O`——实测仍出 2880 解，因为 RTKLIB `expath()` 在 Linux 下把文件名 `tolower` 再匹配；换别的引擎（gLAB）会不会找到：未测。
13. `example1.py` 是 Python 2 且依赖不存在的 `ppp_nrcan`；README 的 GPSPACE 需要作者 fork 才有 IERS2010 代码。

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 实验室日常“下数据→PPP→两站钟差”，愿意自己修胶水 | **本篇**（先打 §3 两处修补，钟差可信到 ~0.3 ns 对 IGS） |
| 直接跑 RTKLIB PPP，不要包装层 | [rtklib.md](./rtklib.md)（本篇核心就是 `rnx2rtkp -k conf`） |
| PPP-AR / 多系统 / 发表级钟差 | [pride-pppar.md](./pride-pppar.md)、[glab-upc.md](./glab-upc.md) |
| BIPM 共视/CGGTTS 产品 | [rnx2cggtts.md](./rnx2cggtts.md) → [cggtts.md](./cggtts.md) |
| 多 AC 钟差综合 | [clkcomb.md](./clkcomb.md) |
| 时间尺度换算（GPST/TAI/UTC、MJD） | [hifitime.md](./hifitime.md) |
| PPS/PTP 授时硬件评估 | [satpulse.md](./satpulse.md)（未在真接收机测试的部分见该篇） |
| RINEX 3→2、拼接、Hatanaka | [gfzrnx.md](./gfzrnx.md)、[crx2rnx.md](./crx2rnx.md)、[hatanaka.md](./hatanaka.md) |
| 读 SINEX 做坐标比对 | [sinex.md](./sinex.md) |
| 学 RTKLIB PPP 源码（易混同名） | [ppp-rtklib.md](./ppp-rtklib.md) |

未测：gLAB 与 GPSPACE 分支、`bipm_ftp` Circular-T/UTCr 下载、`get_multiday_rinex`（gfzrnx 拼接）、LZ 文件改正、Circular-T 对比、CODE final 自动下载、实时/接收机路径（**未在真接收机测试**）。
