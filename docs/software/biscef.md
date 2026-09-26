# BiScEF · 挪威测绘局闪烁数据交换格式（NetCDF4/HDF5）短硬手册

目录：[`PROJECTS.json` → `BiScEF`](../../PROJECTS.json) · 上游 <https://github.com/kartverket/BiScEF> · main **`90e6a2b`**（2026-06-16 09:35 EDT，“Leap seconds correction”）· 无 tag / 无 release / **不在 PyPI**（`pypi.org/pypi/biscef` 404）· **MIT** · ★2 · 本机实测 2026-09-26 04:52–05:03 EDT

> 岗位：给高纬 GNSS 闪烁监测数据（S4、σφ、谱斜率、ROTI、TEC）定一个**跨机构交换/归档的文件约定**。仓库主体是**格式说明 PDF**，外加 ISMR→BiScEF 转换脚本和画图脚本。冲突时：**格式说明 v1.1 PDF > 本机 `-h` > 本文**。

## 1. 用途边界

- 名字里写着 “Binary”，但它**不是自定义二进制格式**。规范第 1 页写明：`File format: NetCDF4 / HDF5`（文件同时是合法的 NetCDF4 和 HDF5）。没有自己的记录类型、魔数和长度字段；字节序由每个 HDF5 数据类型自己声明，样例都是小端。读文件直接用 h5py / netCDF4 / xarray，**仓库里没有“解码库”**。
- 仓库自带的 Python 脚本（没有 `setup.py`/requirements）只有三类：`Python/ismr2BiScEF/ismr2BiScEF.py`（Septentrio ISMR CSV → BiScEF，**只能单向编码**）、`Python/Plotting/Make{Data,Map,InterpolatedMap}Plots.py`（画图）、`ismr2BiScEF_old/`（旧版，里面还提交了 `.pyc`）。**没有 BiScEF→ISMR/CSV 导出，没有校验器。**
- 不做闪烁计算：S4/σφ 由接收机（PolaRx5S 的 sbf2ismr）算好，BiScEF 只负责装进文件。取原始 ISMR → [chain-scintillation](./chain-scintillation.md) / [ismr-downloader](./ismr-downloader.md)。

## 2. 版本事实（2026-09-26 核实）

| 项 | 值 |
| --- | --- |
| 默认分支 | `main` = `90e6a2b52429…`（2026-06-16 09:35 EDT）；共 65 个 commit，最早 2023-02-27；另有分支 `sikkerhet/clean-up`，对应开着的 PR #4（安全元数据清理，2026-07-29 06:25 EDT） |
| 许可 / 语言 | MIT；GitHub 统计 Python 100 %（100246 B）；`catalog-info.yaml` 里 `type: documentation` |
| 体积 | `git clone` 共 **2.0 GB**（137 个示例 `.nc`，覆盖 2023-01-13…15、02-14…16、03-02…03 三次事件，加上 PDF/ODT/演示稿） |
| 格式说明 | v1.0（2023-11-16）→ **v1.1（2024-04-02，只加了根属性 `License`）**；PDF 18 页 |
| 依赖 | ismr2BiScEF：pandas、h5py、numpy；MakeData/MapPlots 另要 matplotlib、**basemap**；Interpolated 版另要 cartopy、scipy、pyproj |
| 本机 | Python 3.13.5，numpy 2.3.5，h5py 3.16.0，pandas 3.0.6，netCDF4 1.7.4，pyfive 1.2.1，matplotlib 3.10.9，basemap 2.0.0 |

## 3. 安装（全部放在 /tmp）

```bash
export TMPDIR=/tmp/biscef-man/tmp PIP_CACHE_DIR=/tmp/biscef-man/pipcache
git clone https://github.com/kartverket/BiScEF.git     # 2.0 GB；只要脚本和 PDF 时，拷出需要的文件后把整个 clone 删掉
python3 -m venv venv && . venv/bin/activate
pip install numpy h5py netCDF4 pandas matplotlib basemap   # 本机 13 s；venv 380 MB
```

CLI 原文（`python ismr2BiScEF.py -h`）：

```text
usage: ismr2BiScEF.py [-h] [--config CONFIG] --recCode RECCODE
                      [--outputPath OUTPUTPATH]
                      filename [filename ...]
  --config CONFIG       Filename of configuration file (default: Info.cfg)
  --recCode RECCODE     Receiver code for the receiver that produced the input
                        data file(s) (default: XXXX)
  --outputPath OUTPUTPATH  Path in which to save the output data file(s) (default: ./)
NB: This script assumes that the file contains data from one day (or less), in
chronological order. The output file name will be based on the first timetag
encountered in the data.
```

`MakeDataPlots.py -h` 的选项有 `-G/-R/-E/-C/-S`、`--plot_ts_simple`、`--plot_ts_box`、`--plot_sky`、`--plot_heat_sigPhi`、`--elevationCutoff`（默认 5），和 PDF 第 10 页一致。

## 4. 例子与真实输出

读取用 h5py（仓库画图脚本也是 h5py）。下面是自写的汇总脚本 `summ.py` 的核心几行，完整输出贴在后面：

```python
with h5py.File(fn) as f: d = {k: f[k][()] for k in f}
off = 315964800 + d['GPSWeek'].astype('i8')*604800 + d['TOW'] - d['UNIXTime']   # GPS−UNIX 秒；规范要求 UTC 时应为 18
```

```text
$ python summ.py ev/FINHEL020230113.nc ev/GRLQAQ320230115.nc ev/NORNYA220230113.nc ev/NORTRO220230113.nc
FINHEL020230113.nc ver=1.0 rx=HEL0 n=82601 vars=65 epochs=1440 sats=130 {C:26245, E:13787, G:17535, J:1348, R:13914, S:9772}
  time 2023-01-13T00:01:09Z .. 2023-01-14T00:00:09Z step=60.0s monotonic=True
  GPS(week,tow)-UNIXTime offsets: {-9: 82601}
  S4s1: nan=468 zero=0 >0:82133 median=0.125 p99=0.429 max=0.946
  S4cors1: nan=468 zero=0 >0:82133 median=0.099 p99=0.315 max=0.736
  Phi60s1: nan=1877 zero=0 >0:80724 median=0.057 p99=0.313 max=4.434
  el>=20: S4s1>0.3 10  Phi60s1>0.3 rad 16
GRLQAQ320230115.nc ver=0.1 rx=QAQ3 n=0 vars=65 ... EMPTY: all datasets length 0
NORNYA220230113.nc ver=1.0 rx=NYA2 n=42341 vars=35 epochs=1440 sats=80 {E:12831, G:16414, R:13096}
  GPS(week,tow)-UNIXTime offsets: {0: 42341}
  S4s1: nan=93 zero=41999 >0:234 median=0.086 p99=1.910 max=1.984
  Phi60s1: nan=0 zero=6345 >0:35974 median=0.084 p99=0.380 max=3.042
NORTRO220230113.nc ver=1.0 rx=TRO2 n=43260 vars=35 epochs=1440 sats=80 {E:13305, G:16624, R:13331}
  time 2023-01-13T00:00:30Z .. 2023-01-13T23:59:30Z step=60.0s monotonic=False
  GPS(week,tow)-UNIXTime offsets: {0: 43260}
  S4s1: nan=255 zero=42588 >0:402 median=0.074 p99=0.356 max=1.394
  S4cors1: nan=0 zero=0 >0:43245 median=0.217 p99=2.081 max=52.265
  Phi60s1: nan=0 zero=2445 >0:40810 median=0.068 p99=0.435 max=3.100
  ROTI1Hz: nan=5856 zero=0 >0:37404 median=1.493 p99=8.858 max=55.186
  el>=20: S4s1>0.3 5  Phi60s1>0.3 rad 814
real 0m0.367s        # 4 个文件合计；单文件全量读入 0.024–0.038 s
```

（中位数/p99 只统计 >0 的值；为了省地方，S4s2/Phi60s2 行没贴。）

**公开挪威数据（免账号）**：Zenodo 记录 10.5281/zenodo.15045918（2024 年 5 月磁暴，40 多台接收机，CC-BY-4.0；`Data.zip` 868539224 B，363 个条目，其中 NOR 的 `.nc` 69 个）。用 HTTP Range（`remotezip`）只抽 3 个文件，没有整包下载：

```text
NORTRO220240511.nc ver=1.0 rx=TRO2 n=42823 vars=35 epochs=1440 sats=78 {E:12959, G:16575, R:13289}
  GPS(week,tow)-UNIXTime offsets: {0: 42823}
  Phi60s1: nan=0 zero=3291 >0:39526 median=0.098 p99=0.666 max=3.083
  ROTI1Hz: nan=5934 zero=0 >0:36889 median=1.923 p99=13.649 max=93.408
  el>=20: S4s1>0.3 25  Phi60s1>0.3 rad 2238          # 同站 05-10：247（磁暴日约 9 倍）
CANGIL20240511.nc ver=1.1 rx=gil n=12881 ... {G:12881}  GPS(week,tow)-UNIXTime offsets: {-9: 12881}
```

**画图脚本**：`MakeDataPlots.py -G --plot_ts_simple --plot_sky` 跑 NORTRO2 出 12 张 PNG，用时 8.1 s；FINHEL0 出 9 张，8.6 s；GRLQAQ3（空文件）退出码 1，`ValueError: min() iterable argument is empty`。

**编码往返（ISMR→BiScEF）**：把 FINHEL0 的 62 个 Septentrio 列按默认 `Varnames` 顺序导出成 ISMR CSV（82601 行，69268138 B），再用 `ismr2BiScEF.py --config Info.cfg --recCode HEL0` 转回来，耗时 1.9 s，得到 9441926 B（gzip）。原文件是 24835596 B，**两者不逐字节一致**（写入器不同、压缩不同，本来就不该指望一致）。按值比较：

```text
orig vars 65 rt vars 68   only rt ['S4uncors1','S4uncors2','S4uncors3']
exact 59                                   # 原 S4s# ≡ 新 S4uncors#，NaN 位置也一致
diff Latitude/Longitude max 0.0099°/0.0314° # IPP 重算（WGS-84 a 当球半径，SLM 350 km）
diff Phi10s1/Phi30s1/Phi60s1  各 2 个值 → NaN   # 脚本把 s1 的 σφ > 2 rad 置 NaN
UNIXTime rt-orig [-27]                     # 新脚本 GPS−18 s；FMI 原文件是旧脚本的 GPS+9 s
dtype: 8 个整型 int64→int32，Sept_sbf2ismrversion int64→float32
S4s1 rt: zeros 15115 = u<c 11673 + u==c 2974 + 输入 NaN 468（nan_to_num 把 NaN 变成 0）
```

## 5. 交叉检查

没有自定义二进制布局可以拿 `struct` 去对，所以分三层做：

1. **自写 struct 解析 HDF5 超级块**：读签名 `\x89HDF\r\n\x1a\n`，然后按 v0 布局 `<QQQ` 从偏移 24 读 base / free-space / EOF 三个地址。7 个真实文件（4 个样例 + 3 个 Zenodo）全部是 `sbver=0 sizeof_off=8 sizeof_len=8 base=0`，**EOF 地址 = 文件大小**。
2. **三个互相独立的读取器逐值比较**：h5py（libhdf5）、netCDF4（libnetcdf-C）、pyfive（纯 Python，用 struct+zlib 自己解析 HDF5，不链接 libhdf5）。对每个变量逐元素比较，NaN 位置也要一致：

| 文件 | 变量 | 比较的值个数 | 不一致 |
| --- | ---: | ---: | ---: |
| FINHEL020230113 | 65 | 10738130 | 0 |
| NORNYA220230113 / NORTRO220230113 | 35 / 35 | 2963870 / 3028200 | 0 / 0 |
| NORTRO220240510 / 0511（Zenodo） | 35 / 35 | 2981230 / 2997610 | 0 / 0 |
| CANGIL20240511（Zenodo） | 28 | 721336 | 0 |

根属性个数三者一致（netCDF4 会隐藏 `_NCProperties`，所以 FIN 少 1 个）。
3. **按规范写的一致性检查器**（`conform.py`：必需属性/数据集、`Description` 属性、维度尺度、SVID 取值范围、时间基准）。库和规范、样例和规范之间的不一致，汇总如下：

| 项 | 规范 v1.0/1.1 | 实测 |
| --- | --- | --- |
| UNIXTime 基准 | “Seconds since Jan 01 1970. (UTC)” | NOR：GPS−UNIX = **0 s**（其实是 GPS 时，晚了 18 s）；FIN、CAN：**−9 s**（旧 ismr2BiScEF 的 bug，晚了 27 s）；新脚本：+18 s（正确，但闰秒写死） |
| `S4s#` | 修正后的 S4 | NOR 的 Description 写 “Total S4”，但 TRO2 有 42588/43260 个值为 0，而 S4cors1 中位 0.217；FIN 写 “Corrected”，却没有 `S4uncors`，无法验证 |
| 缺测值 | 未定义 | NOR 用 **−1**（TRO2 的 S4 有 15 个、Phi60 有 5 个）；FIN 用 NaN，并带 `_FillValue` |
| 维度尺度 | 所有数据集都挂 UNIXTime | NOR 有 34 个数据集没挂 DIMENSION_LIST（netCDF4 仍按名字认出 `UNIXTime` 维） |
| 取值 | 方位/仰角，单位度 | NYA2 有 1 个仰角 = 167.0、2 个方位 > 360（最大 5899.5） |
| 版本/类型 | `"1.0"`、UNIXTime int64 | GRLQAQ320230115：`"0.1"`、float32、数据集名写成 `GPSweek`、0 行 |
| 排序 | 未要求 | NOR 按卫星分块（TRO2 时间倒退 164 次），(t, SVID) 有重复：TRO2 2 条、NYA2 36 条 |

库没有自带的文本/CSV 导出，上面的 ISMR 往返就是唯一能做的文本对照。

## 6. 错误用例（全部为「合成」，底板是 NORTRO220230113.nc）

| 输入（合成） | h5py | netCDF4 | pyfive |
| --- | --- | --- | --- |
| 空文件 0 B | OSError file signature not found | OSError −51 Unknown file format | InvalidHDF5File |
| 截断 50 % / 4 KiB | OSError truncated file（报出 stored_eof） | OSError −101 HDF error | ValueError / struct.error |
| 坏魔数（第 4 字节改成 X） | signature not found | −51 | InvalidHDF5File |
| EOF 地址 ×10 | OSError truncated file | −101 | **静默读出全部 35 个变量** |
| EOF 地址改为 1000 | OSError addr overflow | −101 | **静默读出** |
| 1 MiB 随机字节 | signature not found | −51 | InvalidHDF5File |
| 文件中段 4 KiB 被破坏（gzip 块内） | OSError filter returned failure | RuntimeError HDF error | zlib error −3 |
| 全部改写成大端（`>f4`/`>i8`） | 读出，值与小端版相同 | 同 | 同 |
| 语义错：版本 `"9.9"`、缺必需属性、SVID 长度 100 而 UNIXTime 43260、σφ 取负 | **三者都静默接受** | | |

三个读取器都没有崩溃（没有段错误）。ismr2BiScEF 用合成 ISMR 输入：空文件 → `ERROR: No GPSWeek in data.` rc=1；输入文件不存在 → 报的也是这句（有误导）；随机字节 → `UnicodeDecodeError` 回溯；末行截断 → **静默写入**（4 行）；TOW 写成 `abc` → **被强制转成 0**，UNIXTime 变成 1673135982（整整早了 5 天），rc=0；`--recCode` 不在接收机表里 → `KeyError` 回溯。

## 7. I/O（格式字段表，v1.1）

| 类 | 名称（# = 1/2/3 号信号） | 类型 | 单位 | 必需 |
| --- | --- | --- | --- | --- |
| 根属性 | BiScEFVersion、ReceiverType、ReceiverCode、ReceiverLongitude/Latitude、ReceiverSamplingRate、PhaseHighPassFilterFreqCutoff/Type、ElevationCutoff | str/float | °E、°N、Hz、Hz、° | 是 |
| 根属性 | SLMHeight | float | m | 有 IPP 经纬度时必需 |
| 根属性 | ReceiverFWVersion、ReceiverIdNum、ReceiverHeight、ReceiverCoord[3]、AntennaType/SerialNo、Constellations、SignalStatement、Agency、Country、Contact、DOI、License、Comment | — | m（高/坐标） | 否 |
| 时间 | **UNIXTime**（唯一维度） | int64[] | s，UTC | 是 |
| 时间 | GPSWeek、TOW | int[] | 周、s | 否 |
| 几何 | SVID、Azimuth、Elevation | int/float[] | —、°、° | 是 |
| 几何 | Longitude、Latitude（IPP） | float[] | °E、°N | 否 |
| 每信号 | AvgCN0s# | float[] | dB-Hz | 否 |
| 每信号 | S4s#（修正后）、S4uncors#、S4cors# | float[] | 无量纲 | 否 |
| 每信号 | Phi01/03/10/30/60s#（σφ） | float[] | rad | 否 |
| 每信号 | AvgCCDs#、SigmaCCDs#；lockts# | float/int[] | m；s | 否 |
| 每信号 | SIs#、SInums#；ps#、plows#、pmids#、phighs#（谱斜率）；Ts#（1 Hz 处谱密度） | float[] | —；—；rad²/Hz | 否 |
| 组合 | TEC45/30/15、TECtow、TECtow_uncal、dTEC6045/4530/3015/15tow；locktTEC；CN0TEC；ROTIFullHz、ROTI1Hz | float/int[] | TECU；s；dB-Hz；TECU/min（样例写法） | 否 |
| Septentrio | Sept_Rxstate、Sept_sbf2ismrversion | int[] | — | 否 |

每个数据集都必须带 `Description` 属性，有物理单位的还要带 `Unit`。S4 修正关系是 S4 = √(S4uncor² − S4cor²)，被开方数为负时置 0。SVID 沿用 Septentrio 编号：1–37 G、38–61/63–68 R、71–106 E、120–140/198–215 S、141–180/223–245 C、181–187 J、191–197/216–222 I。推荐文件名 `[国家 alpha-3][4 字符接收机码][yyyymmdd].nc`。

## 8. 坑

1. **不同机构的时间基准不同**：NOR = GPS 时（比 UTC 晚 18 s），FMI/UNB（旧脚本）= 晚 27 s，新脚本才是 UTC。拼接多个网络之前，每个文件都先算一遍 `315964800+week·604800+TOW−UNIXTime`，按结果对齐。新脚本把闰秒写死成 18 s，拿它转 2017 年以前的数据会差 1 s 以上。
2. **历元标签不一致**：NOR 的 TOW%60 = 30（标在分钟中点），FIN/CAN 的 TOW%60 = 0。做逐分钟比较前要统一。
3. **S4 字段含义要看 Description**：NOR 样例里 `S4s1` 写的是 “Total”，但 98 % 为 0；FIN 写的是 “Corrected”。新脚本输出 `S4uncors#`，并把 NaN、u ≤ c 的情况都写成 **0**。所以 0 不等于“无闪烁”，要连同 `S4uncors`/`S4cors` 一起判断。
4. **缺测值有 −1、NaN、0 三种写法**：统计 σφ/S4 前先把 <0 和 NaN 剔掉。
5. ismr2BiScEF 会**悄悄把 s1 的 Phi01–Phi60 大于 2 rad 的值置 NaN**（s2、s3 不处理，规范也没写）。强闪烁研究要留意。
6. NOR 文件按卫星排序、有重复的 (t, SVID)，个别方位/仰角是坏值。先 `argsort(UNIXTime)` 并去重。
7. MakeDataPlots **把 PNG 写到输入文件旁边**（不是当前目录），而且依赖 basemap；遇到空文件直接崩。
8. ismr2BiScEF 的坑：`ReceiverInfoFile` 按当前目录解析；`if ".gz" in fname == True` 是链式比较，这个判断永远为假（pandas 靠扩展名推断压缩，gz 输入**未测**）；输出文件名取首行日期，用 `"w"` 模式直接覆盖同名文件；坏 TOW 被静默当成 0。
9. 仓库 2.0 GB，只需要脚本时不要整仓 clone（可以只拉 PDF + `Python/`）。

## 9. 未测

ismr2BiScEF 的 `.gz` 输入；UNB_Info_Novatel.cfg（NovAtel GSV4004B 列序）；`MakeMapPlots.py`/`MakeInterpolatedMapPlots.py` 的实际出图（只跑了 `-h`，没装 cartopy）；`ismr2BiScEF_old/`；xarray 直接打开；Zenodo 包里的其余 360 个文件。

## 10. 选型

| 需求 | 去哪 |
| --- | --- |
| 读写或交换多机构闪烁**文件**（HDF5/NetCDF4，自描述、带元数据） | 本篇（读用 h5py/netCDF4；写用 ismr2BiScEF 或自己按表写） |
| 拿原始 ISMR 62 列、自己做 S4/σφ 过滤 | [chain-scintillation](./chain-scintillation.md) · [ismr-downloader](./ismr-downloader.md) |
| 从 SBF 原始块自己出指标 | [sbfparser](./sbfparser.md) · [pysbf2](./pysbf2.md) · [septentrio-gnss-driver](./septentrio-gnss-driver.md) |
| 从 RINEX 算 ROTI（不需要闪烁接收机） | [oasis-roti](./oasis-roti.md) |
| 按给定 S4/τ0 合成闪烁 | [iono-scintillation](./iono-scintillation.md) |
| 概念 | [05 闪烁与 ROTI](../tutorials/05-scintillation-roti.md) · [13 闪烁建模](../tutorials/13-scintillation-modeling.md) |
