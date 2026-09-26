# GITM · 全球电离层-热层三维物理模式（GITMCode）操作手册

目录：[`PROJECTS.json` → `GITM`](../../PROJECTS.json) · 上游 <https://github.com/GITMCode/GITM>（`aaronjridley/GITM` 为并行维护的镜像，本文只测 GITMCode）· 文档 <https://gitm.readthedocs.io> · main `c4fc315`（2026-09-04 16:50 EDT；`run_information.txt` 报 `main_c4fc315-20260904.0`，外置 Electrodynamics `main_756d8cb`）· 许可 **Apache-2.0** · 本机实跑 2026-09-26 05:26–05:34 EDT（Debian 13，GNU Fortran 14.2.0，Open MPI 5.0.7，8 核）

> 岗位：自己**跑**一个全球 3-D 热层-电离层物理模式（中性风/温度/成分 + 离子/电子密度/温度，由太阳 EUV、IMF、极区电势/极光驱动），拿到 Ne(lon,lat,alt,t) 去和 GNSS TEC、IRI、MSIS 对比。冲突时：**上游 readthedocs / `srcDoc/set_inputs.md` > 本文**。

## 1. 它解决什么 / 不做什么

**做：**

- 非静力平衡的全球或区域（可限经纬范围）3-D 模式，高度约 100–600+ km（本例网格 100.0–766.0 km，50 层，按 MSIS 标高自动分层）
- 驱动：F10.7（`f107.txt`）或 FISM 光谱、IMF/太阳风文件、SME/AE 指数 → 半球功率；高纬电势 Weimer05 / Heppner-Maynard / AMIE 等，极光 FTA / Fuller-Rowell / OVATION
- 输出 `3DALL`（40 个变量）/ `2DGEL`（电动力学）/ `1DALL` 等二进制块文件，`post_process.py` 合并成 `.bin`，装 PyITM 后可直出 NetCDF
- 1-D 模式（单柱）：改 `ModSize.f90` 为 `nLons=nLats=1` 重编即可，秒级出结果，适合教学/调参

**不做：**

- **不是**经验模型：不能像 [iri2020](./iri2020.md) / [pymsis](./pymsis.md) 一行调用出任意点；要编译、准备驱动文件、跑积分，数值依赖初始化时长
- 不从 GNSS 观测反演 TEC；不做数据同化（同化见教程 12）
- 低纬电动力学（dynamo）默认关闭（`#DYNAMO F`），默认 10°×20° 分辨率下不能指望赤道异常细节 → 低纬请看 [sami2py](./sami2py.md)
- 不带绘图 GUI；Python 工具在 `srcPython/`，不是 PyPI 包

| 同族页面 | 类型 | 何时选 |
| --- | --- | --- |
| **本文 GITM** | 全球 3-D 物理（Fortran+MPI） | 暴时热层-电离层耦合、自己控驱动 |
| [sami2py](./sami2py.md) | 低纬 2-D 磁子午面物理 | EIA/喷泉，单经度 |
| [pymsis](./pymsis.md) / [iri2020](./iri2020.md) | 经验气候 | 背景场、快速对照 |
| [kamodo](./kamodo.md) | 模式输出读取/飞越 | 已有 GITM 输出、要插值到卫星轨道 |
| [lompe](./lompe.md) | 极区局地电动力学反演 | 要**观测约束**的高纬电势/电流（可作 GITM 驱动思路对照） |

## 2. 安装（gfortran + MPI）

```bash
sudo apt-get install -y --no-install-recommends gfortran libopenmpi-dev openmpi-bin
mpif90 --version | head -1      # 本机：GNU Fortran (Debian 14.2.0-19) 14.2.0
mpirun --version | head -1      # 本机：mpirun (Open MPI) 5.0.7
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GITMCode/GITM.git && cd GITM
./Config.pl -install -earth -compiler=gfortran10   # gfortran>=10 用 gfortran10
make -j8                                           # 本机 real 1m1.3s
make rundir && mv run run3d                        # 生成运行目录（含 UAM.in、DataIn 链接）
```

`Config.pl` 会去拉外置电动力学库 `GITMCode/Electrodynamics` 到 `ext/`，先试 SSH、失败自动退回 HTTPS。本机实录（节选）：

```text
Attempting to clone GITMCode/Electrodynamics with ssh:
Host key verification failed.
git clone with SSH failed. Trying HTTPS...
Cloning into 'ext/Electrodynamics'...
Configuring GITM for Earth!!
```

`make` 最后一行：`/…/GITM/src/GITM.exe has been created`（10 074 248 B）。`run3d/GITM.exe` 是指向 `src/GITM.exe` 的**符号链接**（见坑 6）。

## 3. 端到端

### 3.1 默认 3-D 例子：2002-12-21 00:00–00:05 UT，5 分钟，4 进程

默认 `UAM.in` 就是最小的全球例子：2×2 块 × 每块 9×9×50 格（`src/ModSize.f90`），即 10° 纬 × 20° 经；驱动为仓内 `imf20021221.dat`、`ae20021221.dat`、`f107.txt`、FISM 2002。

```bash
cd ~/iono_ops/GITM/run3d
time mpirun -np 4 ./GITM.exe
```

**本机 stdout（2026-09-26 05:28 EDT，节选，未删改行内容）：**

```text
 > Reading Inputs
 > init_grid
 > init_msis
 > init_iri
 > init_b0
 > Initializing IE Library
  => Weimer Initialized
  => FTA Initialized
Writing Output files (3DALL) at iStep :       1 2002 12 21  0  0  0
 > Starting Main Time Loop
iStep:       18, Time: 20021221 000102, WallTime:      0.07 min, Proj :      0.27
iStep:       34, Time: 20021221 000202, WallTime:      0.09 min, Proj :      0.14
iStep:       50, Time: 20021221 000302, WallTime:      0.12 min, Proj :      0.07
iStep:       66, Time: 20021221 000401, WallTime:      0.14 min, Proj :      0.03
Writing Output files (3DALL) at iStep :      82 2002 12 21  0  5  0
 No errors to report!
-> GITM                      took     9.7 seconds to complete
--> initialize               took     2.8 seconds to complete
--> advance                  took     6.8 seconds to complete
---> vertical_all            took     3.9 seconds to complete
---> horizontal_all          took     1.8 seconds to complete
real	0m9.997s
```

产物（`UA/data/`）：每个输出时刻 4 个块文件 `3DALL_t021221_000500.b0001…b0004`（各 2 993 328 B）+ 文本 `.header`，以及 `log00000002.dat`（逐步日志）、`run_information.txt`。

### 3.2 合并块文件 → `.bin`（或 NetCDF）

```bash
python3 -u post_process.py          # run3d/ 下；默认合并后删掉 .b000x
```

```text
Post Processing GITM files...
 -> Processing :  3DALL_t021221_000000.header
 -> Processing :  3DALL_t021221_000500.header
 -> All done!
```

得 `3DALL_t021221_000500.bin`（8 365 844 B）。要 NetCDF：先 `pip install --no-cache-dir netCDF4 git+https://github.com/GITMCode/PyITM.git`（本机 PyITM `087664a`，版本号 0.0.1），再 `python3 -u post_process.py -nc` → `3DALL_t021221_000500.nc`（8 557 451 B）。

### 3.3 用仓内 Python 读 `.bin`（无需 IDL）

```bash
python3 -u - <<'PY'
import sys, numpy as np
sys.path.insert(0, '../srcPython')                  # GITM/srcPython
from gitm_routines import read_gitm_one_file
d = read_gitm_one_file('UA/data/3DALL_t021221_000500.bin', [0, 1, 2, 3, 15, 34, 36])  # 必须给变量号列表
print('time', d['time'], '| nLons,nLats,nAlts =', d['nLons'], d['nLats'], d['nAlts'], '| nVars =', d['nVars'])
print('vars[0:4] =', d['vars'][0:4], '... vars[15] =', d['vars'][15], 'vars[34] =', d['vars'][34])
lon = np.degrees(d[0][:, 0, 0]); lat = np.degrees(d[1][0, :, 0]); alt = d[2][0, 0, :] / 1e3
print('Longitude[deg] (incl. ghost cells):', np.round(lon, 1))
print('Altitude[km] first/last real cell: %.1f / %.1f' % (alt[2], alt[-3]))
k = np.argmin(abs(alt - 300)); print('nearest alt index to 300 km: k=%d alt=%.1f km' % (k, alt[k]))
for i, name, unit in [(3, 'Rho', 'kg/m3'), (15, 'Temperature', 'K'), (34, '[e-]', 'm-3'), (36, 'iTemperature', 'K')]:
    x = d[i][2:-2, 2:-2, k]                          # 去掉每侧 2 个 ghost cell
    print('%-13s @%.0fkm [%s]: min=%.3e max=%.3e mean=%.3e' % (name, alt[k], unit, x.min(), x.max(), x.mean()))
i = np.argmin(abs(lon - 180)); j = np.argmin(abs(lat + 25))
ne = d[34][i, j, 2:-2]; a = alt[2:-2]
print('column lon=%.1f lat=%.1f: NmF2[e- m-3]=%.3e at hmF2[km]=%.1f' % (lon[i], lat[j], ne.max(), a[ne.argmax()]))
PY
```

**本机 stdout：**

```text
Reading file : UA/data/3DALL_t021221_000500.bin
time 2002-12-21 00:05:00 | nLons,nLats,nAlts = 22 22 54 | nVars = 40
vars[0:4] = ['Longitude', 'Latitude', 'Altitude', 'Rho'] ... vars[15] = Temperature vars[34] = [e-]
Longitude[deg] (incl. ghost cells): [-30. -10.  10.  30.  50.  70.  90. 110. 130. 150. 170. 190. 210. 230.
 250. 270. 290. 310. 330. 350. 370. 390.]
Altitude[km] first/last real cell: 100.0 / 766.0
nearest alt index to 300 km: k=29 alt=302.4 km
Rho           @302km [kg/m3]: min=1.765e-11 max=3.683e-11 mean=2.475e-11
Temperature   @302km [K]: min=7.954e+02 max=1.342e+03 mean=1.068e+03
[e-]          @302km [m-3]: min=1.015e+11 max=2.448e+12 mean=6.842e+11
iTemperature  @302km [K]: min=8.015e+02 max=1.686e+03 mean=1.132e+03
column lon=170.0 lat=-25.0: NmF2[e- m-3]=1.690e+12 at hmF2[km]=338.0
```

交叉核对：同一时刻的 NetCDF（PyITM）读 `e-[0,2:-2,2:-2,29]` 得 `z[29][km]=302.4  e- @z29 [/m3]: min=1.015e+11 max=2.448e+12 mean=6.842e+11`，与 `.bin` 完全一致；NetCDF 里坐标 `lon` 为 degrees_east、`z` 为 km，但数据变量 `Altitude` 仍是 **m**（`302415.6…`）。

![GITM 3DALL：302 km [e-] 全球图（左）与 lon=170° lat=−25° 的 Ne 剖面（右），2002-12-21 00:05 UT](./img/gitm-ne-302km-20021221.png)

### 3.4 1-D 单柱：42°N 288°E，30 分钟（1 进程，1.1 s）

```bash
cd ~/iono_ops/GITM
sed -i 's/nLons = 9/nLons = 1/; s/nLats = 9/nLats = 1/' src/ModSize.f90 && make -j8
make rundir && mv run run1d && cd run1d
# UAM.in 改三处：#GRID → 1 / 1 / 42.0 / 42.0 / 288.0 / 288.0；#SAVEPLOTS 输出类型 3DALL→1DALL；#TIMEEND 分钟 05→30
mpirun -np 1 ./GITM.exe
```

stdout 结构同 3.1（`Writing Output files (1DALL)` 每 5 分钟一次），`real 0m1.095s`。输出名是 `1DALL_t021221_000500`、`…_001002`、`…_001503`、`…_002001`、`…_002503`、`…_003000`——**时间戳不齐整**（见坑 5）。

`post_process.py` 对 1DALL 会崩（坑 4），直接读原始块：每个块 = 54 条 Fortran 记录（50 层 + 上下各 2 ghost），每条 **51** 个 float64，前 40 个与 header 变量表同序（`output_common.f90` 中 `nVars = 13+nSpeciesTotal+nSpecies+nIons+nSpecies+5 = 51`，后 11 个未赋值）。

```bash
python3 -u - <<'PY'
import struct, numpy as np
b = open('UA/data/1DALL_t021221_003000.b0001', 'rb').read(); rows = []; p = 0
while p < len(b):
    n = struct.unpack('<i', b[p:p+4])[0]; rows.append(np.frombuffer(b[p+4:p+4+n], '<f8')); p += n + 8
A = np.array(rows); print('records x values =', A.shape)
alt = A[2:-2, 2] / 1e3; T = A[2:-2, 15]; ne = A[2:-2, 34]
print('Longitude[deg]=%.1f Latitude[deg]=%.1f' % (np.degrees(A[0, 0]), np.degrees(A[0, 1])))
for k in [0, 10, 20, 30, 40, 49]:
    print('Altitude[km]=%6.1f  Temperature[K]=%7.1f  [e-][m-3]=%.3e' % (alt[k], T[k], ne[k]))
print('NmF2[m-3]=%.3e hmF2[km]=%.1f' % (ne.max(), alt[ne.argmax()]))
PY
```

```text
records x values = (54, 51)
Longitude[deg]=288.0 Latitude[deg]=42.0
Altitude[km]= 100.0  Temperature[K]=  178.7  [e-][m-3]=4.752e+09
Altitude[km]= 122.0  Temperature[K]=  381.9  [e-][m-3]=1.489e+09
Altitude[km]= 198.5  Temperature[K]=  902.1  [e-][m-3]=1.440e+10
Altitude[km]= 356.6  Temperature[K]= 1005.1  [e-][m-3]=4.436e+11
Altitude[km]= 562.1  Temperature[K]= 1010.4  [e-][m-3]=1.105e+11
Altitude[km]= 766.0  Temperature[K]= 1010.3  [e-][m-3]=5.841e+10
NmF2[m-3]=4.537e+11 hmF2[km]=338.0
```

00:30 UT 在 288°E 约为地方时 19:42，冬至傍晚：NmF2 比 3.3 节白天柱（1.690e12）低约 3.7 倍，合理。

## 4. `UAM.in` 关键参数（本例实际值）

| 块 | 行（顺序即含义） | 本例值 | 说明 |
| --- | --- | --- | --- |
| `#TIMESTART` / `#TIMEEND` | 年 月 日 时 分 秒 | 2002 12 21 00 00 00 → 00 05 00 | UT；重启时**不要改开始时间** |
| `#GRID` | nBlocksLon, nBlocksLat, LatStart, LatEnd, LonStart, LonEnd | 2, 2, −90, 90, 0, 0 | 总格数 = 块数 × `ModSize.f90` 的 nLons/nLats；Lon 0/0 = 全球；1-D 时 LatStart/LonStart 即站点 |
| `ModSize.f90`（编译期） | nLons, nLats, nAlts, nBlocksMax | 9, 9, 50, 1 | 改了必须重 `make`；nBlocksMax=1 ⇒ 进程数 = 块数（坑 3） |
| `#SAVEPLOTS` | DtRestart[s], nOutputTypes, 类型, DtPlot[s] | 7200, 1, `3DALL`, 300 | 其他类型：3DNEU/3DION/2DGEL/1DALL… |
| `#ELECTRODYNAMICS` | 极光模型, DtAurora[s], 电势模型, DtPotential[s] | `FTA`, 60, `weimer05`, 60 | 可选 fre/pem/ovation/amie；hepmay/amie/zero |
| `#MHD_INDICES` | IMF/太阳风文件 | `UA/DataIn/Examples/imf20021221.dat` | 自下：`srcPython/omni_download_write_swmf.py 20021221 20021222 -swmf` |
| `#SME_INDICES` | AE 文件, onset 文件, 是否换算 HP | `ae20021221.dat`, none, T | 自下：`srcPython/supermag_download_ae.py`（需 SuperMAG 账号，本文未测） |
| `#NGDC_INDICES` | F10.7 文件 | `UA/DataIn/f107.txt` | 2019 年后需自备；也可用 `#F107` 直接给 f107、f107a |
| `#EUV_DATA` | 用 FISM?, 文件 | T, `fismflux_daily_2002.dat` | 1990–2018 推荐 FISM |
| `#DYNAMO` | UseDynamo, 高纬边界, 迭代数… | F, 45.0, 500 … | 低纬电动力学，高分辨率才开 |
| `#APEX` | T/F | T | 地球必须开（其他行星没有 Apex） |
| `#MSISOBC` | 下边界 O 偏移半年?, 扁率% | T, 0.0 | 下边界条件取 MSIS |
| `#AUSMSOLVER` | T/F | T | AUSM+-up 求解器 |
| `#DEBUG` | 级别, 监视 CPU, stdout 间隔[s], barrier | 0, 0, 60.0, F | 查问题时级别调到 ≥1 |

`log00000002.dat` 列（本例末行 iStep 82）：`F107=177.9 F107A=149.5 By=5.5 Bz=-6.4 Vx=533.7 … HPn=174.6 HPs=183.5 CPCPn=109.3 CPCPs=100.5 SubsolarLon=3.120 SubsolarLat=-0.410 SubsolarVTEC=55.050`。单位核对：CPCP 在 `get_potential.f90` 里 /1000 → **kV**；VTEC 按 `calc_tec.f90` 注释为 **TECU**；Subsolar 经纬是**弧度**（−0.410 rad = −23.5°，冬至）；HP 单位代码未标注，本文未核。

## 5. 怎么读结果

- **`.bin` 里经纬是弧度、高度是米**；密度 m⁻³，`Rho` kg m⁻³，温度 K，速度 m s⁻¹。
- 每个维度两侧各 **2 个 ghost cell**：18 格变 22、50 层变 54，纬度会出现 −105°/105°、经度 −30°/390°。统计前一律 `[2:-2]`。
- 默认 5 分钟只是冒烟测试：初值来自 MSIS/IRI，物理量远未稳态，**不要拿来做科学结论**；研究用通常先跑 1–2 天 spin-up 再重启（`#RESTART`）。
- 3-D 图上 302 km 的 Ne 高值带在南北两侧各有一条（左图 lat≈+25°/−20°、lon 120–220°），位置是 00 UT 的日下区；10°×20° 格太粗，不能称为赤道异常的定量结果。
- 与 GNSS 对比：自己沿高度积分 `[e-]` 得 VTEC（单位换 TECU），或用 [kamodo](./kamodo.md) 飞越；MSIS/IRI 基准见 [pymsis](./pymsis.md) / [iri2020](./iri2020.md)。

## 6. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `mpif90: command not found`（本机装 MPI 前） | GITM 链接用 `mpif90`，只有 gfortran 不够 | `sudo apt-get install -y libopenmpi-dev openmpi-bin` |
| 2 | `Config.pl` 打印 `Host key verification failed.` | 先用 SSH 拉 Electrodynamics；无 SSH key 时失败后会自动改 HTTPS（本机成功）；若 HTTPS 也不通则 `ext/` 为空 | `git clone https://github.com/GITMCode/Electrodynamics.git ext/Electrodynamics` 后重跑 `./Config.pl -install -earth -compiler=gfortran10` |
| 3 | `mpirun -np 2` 跑默认 2×2 块：`Stopping execution! iProc= 0 with msg=Error allocating Fang arrays in aurora`，exit 215 | 进程数与块数（nBlocksLon×nBlocksLat=4）不符 | `mpirun -np 4 ./GITM.exe` |
| 4 | 1DALL 跑 `post_process.py`：`struct.error: unpack requires a buffer of 320 bytes` | 1-D 块文件每条记录写 51 个值，header 只列 40 个；后处理按 header 读 | 用 3.4 节的原始读法（前 40 列有效）；或输出改 `3DALL` 后再合并 |
| 5 | 脚本写死 `1DALL_t021221_001000` 找不到文件 | 输出时刻落在超过 DtPlot 的第一个时间步，文件名是 `001002`、`001503` | `ls UA/data/1DALL_t021221_0010*` / Python 用 `sorted(glob.glob(...))` |
| 6 | 改 `ModSize.f90` 重编后，老运行目录也变成 1-D | `run*/GITM.exe` 是指向 `src/GITM.exe` 的符号链接 | 重编前先固化：`cp --remove-destination src/GITM.exe run3d/GITM.exe` |
| 7 | `read_gitm_one_file(f)` → `TypeError: 'int' object is not subscriptable` | 默认参数 `vars_to_read=-1` 的分支写错（`vars_to_read[0]`） | `read_gitm_one_file(f, list(range(40)))` |
| 8 | `post_process.py -nc` → `ImportError: >> PyITM is required for NetCDF post-processing!` | NetCDF 写出依赖 PyITM（非 PyPI） | `pip install --no-cache-dir netCDF4 git+https://github.com/GITMCode/PyITM.git` |
| 9 | 统计出纬度 −105°、经度 390° 或极值异常 | 包含 ghost cell | `x = d[34][2:-2, 2:-2, 2:-2]` |
| 10 | 经纬看起来是 −0.5…6.8 | `.bin` 坐标为弧度、高度为 m | `np.degrees(d[0])`、`d[2]/1e3` |

## 7. 许可与诚实边界

- Apache-2.0（`LICENSE`）；引用：README 徽章给出 Zenodo DOI 10.5281/zenodo.7509933，模式论文 Ridley et al. 2006（doi:10.1016/j.jastp.2006.01.008，见 `srcDoc/gitm.bib`）。
- **实跑**：gfortran 14.2 + Open MPI 5.0.7 优化编译（非 debug）；默认 3-D 5 分钟 4 进程；1-D 30 分钟 1 进程；`.bin` 与 PyITM NetCDF 两条读取路径。
- **未实跑**：`srcTests/auto_test/run_all_tests.sh`（会重新编译并把日志与 `ref_solns/` diff）、`srcTests/test.Short`（需 8 进程并下载 OMNI）；dynamo 开启、高分辨率、`#RESTART`、HDF5、Mars/Venus 等；SuperMAG/OMNI 下载脚本；`gitm_plot_*.py` 绘图脚本；与观测 TEC 的比对。
- 5 分钟冒烟数值只代表"能跑通、单位对"，不代表 2002-12-21 的真实电离层。

## 8. 链接

- 教程：[12 数据同化入门（物理模式层）](../tutorials/12-data-assimilation-intro.md) · [15 从论文到代码](../tutorials/15-from-paper-to-code.md) · [20 磁暴与 TEC](../tutorials/20-storm-tec-analysis.md) · [04 IRI/NeQuick 与背景模型](../tutorials/04-iri-nequick.md)
- 兄弟：[pymsis](./pymsis.md) · [iri2020](./iri2020.md) · [sami2py](./sami2py.md) · [kamodo](./kamodo.md) · [lompe](./lompe.md) · [apexpy](./apexpy.md) · [pyspedas](./pyspedas.md)（OMNI/IMF 驱动时间线）
