# GNSS-Correction-RTKLIB 操作手册（dGPS/PPK 教程 + RTKLIB 批处理脚本）

> 仓库：<https://github.com/bpurinton/GNSS-Correction-RTKLIB> · 作者 Ben Purinton（Potsdam 大学）· **GPL-3.0** · ★24 · tip **`891cad8`**（2021-04-14，此后无提交）· 默认分支 `master`
> 本页实测：2026-09-26 01:00–01:05 EDT，本机 Debian `rtklib 2.4.3.b34`（`/usr/bin/rnx2rtkp`）+ `teqc 2019Feb25` + Python 3.13。
> **质检复跑**（2026-09-26 01:10–01:20 EDT，另起目录重 clone）：3.1 头 12 行、1156/1156/1047、trace `outlier rejected` **79578** / `large residual` **2552**；3.2 rejionno 100→**2585**、1000→**2590**/2583、timeinterp off→**1155**、sdu 中位 0.0515/最大 55.8154、17:36:08 两行；3.3 IGN `425`、NGS brdc **288538** B、**1778** 站目录；3.4 teqc 头 3 行与 MS01 **551**/521 末行；3.5 **15685801** B（仓内 `.19o` 多 62639 个 CR）+ PPK 0 行差；坑 3 sed 与 `FileNotFoundError`、坑 8 **1648.0112**、坑 10 **78** 历元，全部逐字复现。改 4 处：工作树实为 **58 MB**（含 `.git` 89 MB）；1156 历元的节奏是**每 5 s 留 2 个**（相邻间隔 1 s×675、4 s×468），trace 里没有 `gap` 行；NGS brdc 与仓内 brdc 不是同一文件，2590 行中 **35** 行末位差 1e-4（第 2000 行一致）；补坑 11 teqc 接 `| head` 被截断。耗时本机 4.6 s（负载 ≈37，不可比）。

## 1. 它是什么 / 解决什么问题

一句话：**一份“野外手持 GNSS 接收机数据 → 用 RTKLIB 做事后差分（PPK）→ 得到厘米～分米级坐标”的教程包**，附一个把整条链自动化的 Python 脚本。它本身**不是新算法**，核心计算全交给 RTKLIB 的 `rnx2rtkp`。

仓库里真正有用的三样东西：

| 路径 | 内容 | 用途 |
|---|---|---|
| `example_gui/` | 流动站 `BP01_leicaR2.obs`（Leica，1 Hz，2019-02-26）、基准站 `UNSA00ARG_R_20190570000_01D_30S_MO.19o`（阿根廷 Salta IGS 站，30 s）、`brdc0570.19n`、`igr20422.sp3`/`igu20422_18.sp3`、作者 GUI 处理结果 `BP01_leicaR2.pos` | **可直接复现的一组完整 PPK 输入 + 参考输出** |
| `scripts/rnx2rtkp_options.conf` | RTKPOST 2.4.2 导出的 100 行配置（kinematic、L1+L2、15° 截止角、精密星历） | 命令行 `rnx2rtkp -k` 直接吃 |
| `scripts/dGPS_PPK_RTKPOST.py` | 376 行：Leica `.m00` → teqc 转 RINEX → FTP 下载基准站/星历 → `rnx2rtkp` → `.csv` + UTM `.shp` | 批处理模板（Windows 写死，见坑 3） |
| `docs/*.md/.pdf` | 两份手册：Trimble 野外采集、RTKPOST GUI 逐步截图 | 新手看图操作 |

**名词速查**

- **dGPS / 差分**：两台接收机同时观测同一批卫星，一台在已知点（基准站），一台在待测点（流动站）。两者误差（卫星钟、轨道、大部分电离层/对流层延迟）高度相关，做差后大幅抵消。
- **PPK（Post-Processed Kinematic，事后动态）**：野外只记录原始观测，回办公室再和基准站数据一起解算。对比 RTK（实时，需要电台/NTRIP 链路），PPK 不需要实时通信，适合偏远地区（本仓例子就在安第斯高原）。
- **CORS（Continuously Operating Reference Station）**：长期连续运行、坐标精确已知的基准站网络，公开发布 RINEX。本仓用的 UNSA 是 IGS 站；美国可用 NOAA NGS CORS。你不必自己架基准站。
- **基线**：流动站到基准站的距离。越短越好：误差相关性随距离下降。本例基线约 **140 km**（RINEX 头坐标算出，流动站 −25.93°、基准站 −24.73°），这是整组数据**始终只有浮点解**的主因。
- **Q（解的质量）**：RTKLIB `.pos` 第 5 列。1=fix（整周模糊度固定，cm 级）、2=float（浮点，dm 级）、5=single（单点，m 级）。
- **ratio**：模糊度检验比值，≥ `pos2-arthres`（本配置 3）才判 fix。
- **精密星历 sp3**：IGS 事后轨道。`igu`=超快速（每 6 h 发布，含预报）、`igr`=快速（约 1 天后）、`igs/igp`=最终（约 2 周后）。

## 2. 安装

```bash
# RTKLIB 命令行（Debian/Ubuntu 包即可跑本仓例子）
sudo apt install rtklib          # 提供 rnx2rtkp / convbin / pos2kml ...
rnx2rtkp -? 2>&1 | head -3       # 注意：-? 才是帮助，-h 是 fix-and-hold

# 仓库（工作树约 58 MB、连 .git 约 89 MB：样例数据 + 手册截图）
git clone --depth 1 https://github.com/bpurinton/GNSS-Correction-RTKLIB
cd GNSS-Correction-RTKLIB

# 只有想跑 Python 批处理脚本时才需要
python3 -m venv .venv && . .venv/bin/activate
pip install gnsscal hatanaka numpy
sudo apt install python3-gdal    # 脚本 from osgeo import ogr, osr；venv 里用 pip 装 GDAL 常因版本不匹配失败
```

本机状态：`gnsscal`/`osgeo` 均未安装（`ModuleNotFoundError`），因此**没有整跑 `dGPS_PPK_RTKPOST.py`**；下面的 E2E 是按脚本里的同一条命令手工逐步执行的。

## 3. 端到端实测（仓内样例，本机真实输出）

### 3.1 用仓内配置原样跑 PPK

```bash
cd example_gui && mkdir -p out
rnx2rtkp -k ../scripts/rnx2rtkp_options.conf -o out/BP01_ppk.pos \
  BP01_leicaR2.obs UNSA00ARG_R_20190570000_01D_30S_MO.19o brdc0570.19n igr20422.sp3 2>/dev/null
```

输入顺序与脚本一致：**流动站 obs → 基准站 obs → 广播星历 → sp3**。耗时约 3.6 s。输出头（节选，原样）：

```
% program   : RTKLIB ver.2.4.3
% obs start : 2019/02/26 16:54:31.0 GPST (week2042 233671.0s)
% obs end   : 2019/02/26 17:46:01.0 GPST (week2042 236761.0s)
% pos mode  : Kinematic
% freqs     : L1+2
% ionos opt : Broadcast
% tropo opt : Saastamoinen
% ephemeris : Precise
% navi sys  : GPS GLONASS Galileo
% antenna1  :                       ( 0.0000  0.0000  1.5200)
% antenna2  :                       ( 0.0000  0.0000  0.1300)
% ref pos   :-24.727456635, -65.407643440, 1257.9336
```

统计（`grep -v '^%' | awk`）：

```
out/BP01_ppk.pos epochs=1156 Q2=1156 sdu<0.5m=1047
BP01_leicaR2.pos epochs=2590 Q2=2590 sdu<0.5m=2584     # 作者 RTKPOST 2.4.2 GUI 结果（仓内）
```

**同一配置、同一数据，Debian 2.4.3 只出了 1156 个历元，作者 GUI 出了 2590 个。** 用 `-x 2` 打 trace 看：`outlier rejected` **79578** 次、`large residual` 2552 次，典型行 `outlier rejected (sat= 27- 32 L1 v=422.070)`。解出的历元呈“每 5 秒只剩 2 个”的规律：相邻历元间隔 1 s 出现 675 次、4 s 出现 468 次（如 `17:06:51, :55, :56, 07:00, :01, :05…`）。

### 3.2 放宽创新量门限后复现作者结果

```bash
sed 's/^pos2-rejionno.*/pos2-rejionno      =1000/' ../scripts/rnx2rtkp_options.conf > out/rej1000.conf
rnx2rtkp -k out/rej1000.conf -o out/rej1000.pos \
  BP01_leicaR2.obs UNSA00ARG_R_20190570000_01D_30S_MO.19o brdc0570.19n igr20422.sp3 2>/dev/null
```

实测历元数：`rejionno=30` → 1156；`=100` → 2585；`=1000` → **2590**（与仓内 `.pos` 一致）；把 `misc-timeinterp` 关掉 → 1155。

```
out/rej1000.pos epochs=2590 Q2=2590 sdu<0.5m=2583
sdu median 0.0515 max 55.8154
```

同一历元对比（本机 vs 仓内 GUI）：

```
2019/02/26 17:36:08.000, -25.933309354, -65.876859742, 1683.4641,  2,  8,  0.0174,  0.0214,  0.0509, ...   # 本机 2.4.3
2019/02/26 17:36:08.000, -25.933309655, -65.876856816, 1683.5259,  2,  8,  0.0174,  0.0215,  0.0509, ...   # 仓内 2.4.2 GUI
```

水平差约 0.3 m、高程差约 6 cm，量级在浮点解正常范围内；**两边都没有一个 fix**（140 km 基线 + 30 s 基准站采样）。

### 3.3 广播星历改从 NOAA NGS 下载（替代脚本里的 IGN FTP）

```bash
curl -sS --list-only ftp://igs.ensg.ign.fr/pub/igs/data/2019/057/     # 本机：curl: (19) RETR response: 425
curl -sS -O https://geodesy.noaa.gov/corsdata/rinex/2019/057/brdc0570.19n.gz && gunzip -f brdc0570.19n.gz
ls -l brdc0570.19n                                                   # 288538 B
rnx2rtkp -k rej1000.conf -o ngsbrdc.pos ../BP01_leicaR2.obs \
  ../UNSA00ARG_R_20190570000_01D_30S_MO.19o brdc0570.19n ../igr20422.sp3 2>/dev/null
grep -vc '^%' ngsbrdc.pos                                            # 2590；NGS brdc 与仓内 brdc 字节不同，与 3.2 比有 35 行末位差 1e-4（如 sde 0.0641/0.0642），第 2000 行逐位相同
```

NGS 目录 `https://geodesy.noaa.gov/corsdata/rinex/2019/057/` 当天列出 **1778** 个站目录，站文件名形如 `zdc1/zdc10570.19d.gz`（Hatanaka 压缩）。CDDIS 在本机返回 `425 Bad IP`，不要依赖。

### 3.4 脚本前两步：Leica `.m00` → RINEX → PPK（`example_python/`）

```bash
teqc +obs MS01.obs +nav MS01.nav ../GNSS-Correction-RTKLIB/example_python/MS01_6610_0226_161513.m00
# ! Notice ! '...m00' @ 2019 Feb 26 15:32:36.000: poss. incr. of sampling int. OR data gap of 83.000 seconds
grep -E "ANT #|DELTA|FIRST" MS01.obs
#  -Unknown-           LEIAS10         NONE                    ANT # / TYPE
#          1.8760        0.0000        0.0000                  ANTENNA: DELTA H/E/N
#   2019     2    26    15    17    8.0000000     GPS         TIME OF FIRST OBS
G=../GNSS-Correction-RTKLIB/example_gui
rnx2rtkp -k $G/out/rej1000.conf -o MS01.pos MS01.obs \
  $G/UNSA00ARG_R_20190570000_01D_30S_MO.19o $G/brdc0570.19n $G/igr20422.sp3 2>/dev/null
```

```
% obs start : 2019/02/26 15:17:08.0 GPST (week2042 227828.0s)
% obs end   : 2019/02/26 15:32:47.0 GPST (week2042 228767.0s)
% antenna1  :                       ( 0.0000  0.0000  1.8760)
epochs=551 Q2=551 sdu<0.5m=521
2019/02/26 15:32:47.000, -25.933886483, -65.877007902, 1682.0735,  2,  6,  0.0390,  0.0272,  0.0852, ...
```

MS01 与 BP01 同一天，可复用同一组基准站/星历，所以不需要下载即可验证 `.m00` 流程。天线高 1.876 m 由 teqc 从 Leica 文件写进 RINEX 头，`ant1-anttype=*` 让 RTKLIB 从头里读取。

### 3.5 CRINEX 基准站解压（脚本用 `hatanaka` 包）

```bash
gunzip -k UNSA00ARG_R_20190570000_01D_30S_MO.crx.gz
python -c "import hatanaka;print(hatanaka.decompress_on_disk('UNSA00ARG_R_20190570000_01D_30S_MO.crx'))"
# UNSA00ARG_R_20190570000_01D_30S_MO.rnx        (hatanaka 2.8.1；15685801 B)
```

仓内 `.19o` 是 CRLF 行尾（15748440 B），换成本机解压的 `.rnx` 跑 PPK，`.pos` 数据行 **0 行差异**。

## 4. `.pos` 输出字段（`out-fieldsep=,`，`out-solformat=llh`）

| 列 | 名称 | 单位 | 说明 |
|---|---|---|---|
| 1 | GPST | `YYYY/MM/DD hh:mm:ss.sss` | GPS 时（`out-timesys=gpst`），比 UTC 快 18 s（2019 年） |
| 2–3 | latitude / longitude | deg | WGS84 |
| 4 | height | m | **椭球高**（`out-height=ellipsoidal`），不是海拔 |
| 5 | Q | — | 1 fix / 2 float / 4 dgps / 5 single |
| 6 | ns | — | 参与解算卫星数 |
| 7–9 | sdn / sde / sdu | m | 北/东/天 1σ，筛点主要看 sdu |
| 10–12 | sdne / sdeu / sdun | m | 协方差项（带符号的平方根） |
| 13 | age | s | 差分龄期；本例出现 −16…−2 s 的负值（基准站 30 s 内插到 1 s 流动站），筛点不要用它 |
| 14 | ratio | — | 模糊度 ratio；本例一直约 1.0–1.1，远低于门限 3 |

注意 `.pos` 列间有对齐空格；用 pandas 读时 `skipinitialspace=True`。

## 5. 配置里最该懂的参数（`scripts/rnx2rtkp_options.conf`）

| 键 | 仓内值 | 含义 / 何时改 |
|---|---|---|
| `pos1-posmode` | `kinematic` | 流动站在动。只测静止点可改 `static`，同样数据误差更小 |
| `pos1-frequency` | `l1+l2+l5` | 实际样例只有 L1/L2，头显示 `L1+2` |
| `pos1-soltype` | `forward` | 改 `combined`（前向+后向平滑）通常更稳，PPK 事后处理不用白不用 |
| `pos1-elmask` | `15` | 截止高度角，低于此的卫星不用 |
| `pos1-ionoopt` | `brdc` | 用广播 Klobuchar 模型改正电离层；长基线可试 `dual-freq`（无电离层组合）或 `est-stec` |
| `pos1-tropopt` | `saas` | Saastamoinen 模型 |
| `pos1-sateph` | `precise` | 用 sp3；**必须提供 sp3 文件**，否则无解 |
| `pos1-navsys` | `13` | 1 GPS + 4 GLO + 8 GAL |
| `pos2-armode` | `continuous` | 模糊度连续估计 |
| `pos2-arthres` | `3` | ratio 门限 |
| `pos2-rejionno` | `30` | 创新量（观测残差）剔除门限，m。本机 2.4.3 需放大才能复现作者结果（3.2） |
| `pos2-maxage` | `30` | 允许的最大差分龄期 |
| `misc-timeinterp` | `on` | 把 30 s 基准站内插到流动站历元 |
| `ant1-postype` | `llh` 90/0/−6335367.6 | 流动站初值占位（北极点），动态模式下无所谓 |
| `ant2-postype` | `rinexhead` | 基准站坐标取 RINEX 头 `APPROX POSITION XYZ`——CORS 头坐标一般可信，自建基站要核对 |
| `ant1/2-anttype` | `*` | 从 RINEX 头读天线型号与 `DELTA H` |
| `out-height` | `ellipsoidal` | 要海拔改 `geodetic` 并设 `out-geoid` |

## 6. Python 脚本 `dGPS_PPK_RTKPOST.py` 实际做了什么

按源码顺序：

1. `glob` 找 `bd` 下所有 `*.m00` → `teqc +obs X.obs +nav X.nav X.m00`。
2. 读 obs 头 `TIME OF FIRST OBS` → `gnsscal` 算年积日与 GPS 周。
3. 从 `ftp://igs.ensg.ign.fr/pub/igs/data/YYYY/DOY/` 下载 `UNSA*30S*.crx.gz` 与 `brdcDOY0.YYn.Z`；从 `/pub/igs/products/WWWW/` 先下 `igrWWWWD.sp3.Z`，失败再下 `iguWWWWD_18.sp3.Z`。
4. `hatanaka.decompress_on_disk` 解压。
5. `rnx2rtkp -k conf -o X.pos rover base brdc sp3`。
6. 解析 `.pos`：跳过 `%` 行，从 `% ref pos` 取基准站坐标，写 `.csv`（加 UTM 北/东与**到基准站距离** `base_dist(m)`）和 `_wgs84_utm19s.shp`。

要改的只有第 30–52 行：`bd`、`base_stn`、`spatial_ref`（UTM WKT）、`utmzone`、`rtkconf`、`rnx2rtkp`、`teqc` 路径。

## 7. 坑（现象 → 原因 → 修复命令）

1. **历元数只有作者结果的一半，trace 满屏 `outlier rejected`**
   → Debian 2.4.3 下 `pos2-rejionno=30` 把 1 s 流动站 + 内插基准站的大量观测判为粗差（实测 1156 vs 2590）。
   → `sed -i 's/^pos2-rejionno.*/pos2-rejionno      =1000/' my.conf`（放宽门限意味着粗差也可能混进来，务必再按 sdu 筛点）。

2. **整段全是 Q=2，没有一个 fix**
   → 基线约 140 km、基准站 30 s；这类距离下 L1/L2 模糊度很难固定。不是软件坏了。
   → 选更近的 CORS（< 20–30 km 起步）或自架基站；已有数据只能筛：`grep -v '^%' X.pos | awk -F, '$9+0<0.5' > good.csv`。

3. **在 Linux 跑脚本报 `FileNotFoundError: [Errno 2] No such file or directory: 'rnx2rtkp -k ...'`**
   → 脚本 `subprocess.call(cmd, shell=False)` 传的是整串字符串，POSIX 上会把整串当可执行文件名；另有 `cmd.replace('/', '\\')` 把路径改成 Windows 反斜杠。
   → `sed -i -e "/cmd.replace('\/', '\\\\\\\\')/d" -e 's/subprocess.call(cmd, shell=False)/subprocess.call(cmd, shell=True)/' scripts/dGPS_PPK_RTKPOST.py`（再把第 30–52 行路径改成本机路径）。

4. **脚本卡在下载或报 `425`**
   → `igs.ensg.ign.fr` 匿名 FTP 在本机数据连接返回 `425`；CDDIS 返回 `425 Bad IP`。
   → 手工从 NGS 取：`curl -O https://geodesy.noaa.gov/corsdata/rinex/YYYY/DDD/brdcDDD0.YYn.gz`；站数据 `.../YYYY/DDD/ssss/ssssDDD0.YYd.gz`，再改脚本跳过 `download_corr_files`。

5. **`rnx2rtkp -h` 没出帮助，反而开始跑/报错**
   → RTKLIB 里 `-h` 是 fix-and-hold 模式开关。
   → `rnx2rtkp -? 2>&1 | less`。

6. **`ModuleNotFoundError: No module named 'osgeo'`（或 `gnsscal`）**
   → 脚本依赖 GDAL Python 绑定与 `gnsscal`、`hatanaka`，本机默认都没有。
   → `sudo apt install python3-gdal && pip install gnsscal hatanaka`（venv 需 `--system-site-packages` 才看得到 apt 的 GDAL）。

7. **流动站高程整体偏了一个天线高（本例 1.52 m / 1.876 m 量级）**
   → 天线高没进 RINEX 头（`ANTENNA: DELTA H/E/N` 为 0）而配置用 `anttype=*` 从头里读。
   → `grep "DELTA H/E/N" rover.obs`；为 0 时在 conf 里写 `ant1-antdelu =1.876`（你的实际天线高）。

8. **`.pos` 高程和 DEM/海拔对不上几十米**
   → 输出是 WGS84 椭球高。实测同一历元 17:36:08：椭球高 1683.4641 m，改 `geodetic` 后 1648.0112 m，差 **35.45 m**（RTKLIB 内置大地水准面）。
   → `sed -i -e 's/^out-height.*/out-height =geodetic/' -e 's/^out-geoid.*/out-geoid =internal/' my.conf`。

9. **把 sp3 放错位置或漏掉，结果 0 个历元**
   → `pos1-sateph=precise` 必须有覆盖观测时段的 sp3；`igu` 文件名还带发布小时 `_18`。
   → 确认参数第 4 个是 sp3：`rnx2rtkp -k my.conf -o out.pos rover.obs base.YYo brdc.YYn igrWWWWD.sp3`。

10. **teqc 提示 `data gap of 83.000 seconds`**
    → Leica 文件里有多段测量（MDB survey starts/ends），不是转换错误。
    → 需要分段时用 teqc 时间窗（实测可用，输出 78 历元）：`teqc -st 20190226151708 -e 20190226152000 +obs part.obs MS01_6610_0226_161513.m00`。

11. **teqc 转出的 `.obs` 只有几十秒、PPK 只出 0 个历元**
    → 把 teqc 的 stderr/stdout 接进 `| head` 看提示：head 退出后 teqc 被 SIGPIPE 杀掉，文件截断（复跑实测 `obs end` 停在 15:17:59、47144 B，完整应为 633 历元/957123 B）。
    → 提示重定向到文件：`teqc +obs X.obs +nav X.nav X.m00 2> teqc.err; head teqc.err`。

## 8. 诚实的局限

- 仓库 2021 年后停更；脚本假设 Windows + Leica `.m00` + IGN FTP，**三点在今天的 Linux 上都要改**。
- 教程只讲 GPS/GLONASS/Galileo L1/L2 浮点 PPK，没有讨论 fix 策略、基线长度与精度关系、后向平滑等。
- 电离层只用广播模型（Klobuchar），对电离层研究**没有**新贡献；它是“用 RTKLIB 得坐标”的入门材料。
- teqc 官方已停止维护（UNAVCO 2019 版为最后版本），新项目用 `convbin`/`gfzrnx`。
- 本页没有整跑 Python 脚本（缺 GDAL 且 FTP 源不可达），只逐步复现了它调用的每条外部命令。

## 9. 交叉链接

- [rtklib.md](./rtklib.md)：`rnx2rtkp` 全部旗标、`-?` vs `-h`
- [rtklib-explorer.md](./rtklib-explorer.md)：demo5/EX 分支，低成本接收机 fix 率更好
- [pyrtklib-demo5.md](./pyrtklib-demo5.md)：Python 里直接调 RTKLIB `postpos`
- [teqc.md](./teqc.md) / [gfzrnx.md](./gfzrnx.md)：原始数据 → RINEX
- [hatanaka.md](./hatanaka.md) / [crx2rnx.md](./crx2rnx.md)：CORS 的 `.d`/`.crx` 解压
- [rtkbase.md](./rtkbase.md)：自架基准站
