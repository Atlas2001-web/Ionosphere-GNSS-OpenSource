# ionFR · 电离层法拉第旋转 RM 预测（IGRF + IONEX）操作手册

目录：[`PROJECTS.json` → `ionFR`](../../PROJECTS.json) · 上游 <https://github.com/csobey/ionFR> · **GPL-3.0** · ★12 · master **`4fe4f12`**（2021-10-05 04:10 EDT，此后无提交）· 无 tag、不在 PyPI · 论文 Sotomayor-Beltran et al. 2013, A&A 552, A58。
本机验证 **2026-09-26 06:22–06:32 EDT**：CPython 3.13.5 venv，numpy 2.5.3、scipy 1.18.1、future 1.0.0，gcc（Debian 14.2）；IONEX 取自 AIUB 匿名 HTTPS。

> 岗位：给“射电源赤经赤纬 + 望远镜经纬度 + 日期 + 当天 IONEX 文件”，按 UT 每小时算一次：视线穿刺点（单层，高度取 IONEX 头）上的斜 TEC、IGRF 视线磁场，乘起来得到电离层 **旋转量度 RM（rad m⁻²）** 和不确定度，写进当前目录 `IonRM.txt`。源仰角 ≤ 0° 的小时不输出。
> 它是 2013 年的 Python 2 时代代码：**原样在 Python 3 + 新 SciPy 下跑不起来**，也只吃 **2 小时间隔（13 张图）** 的 IONEX。下面每个补丁都在本机跑过。

---

## 1. 它解决什么问题

线偏振射电信号穿过有磁场的电离层时，偏振角转动 Δχ = RM·λ²。LOFAR 这类低频望远镜 λ 大（150 MHz 时 λ≈2 m），1 rad m⁻² 的电离层 RM 就能让偏振角转约 4 rad，做脉冲星/射电源偏振、宇宙磁场 RM 合成时必须先扣掉。

ionFR 的公式（`ionFRM.py` 原文）：`IFR = 2.6e-17 × Totfield[G] × TECpath[m⁻²]`。常数 2.6e-17 就是 SI 的 2.63×10⁻¹³ rad m⁻² T⁻¹ 换成高斯（1 G = 10⁻⁴ T）；[spinifex](./spinifex.md) 写成 `−2.62e−6 × TECU × nT`，两者同一物理量，符号约定不同（§5）。

| 步骤 | 源码位置 | 做法 |
| --- | --- | --- |
| RA/Dec → 高度角/方位角 | `SiderealPackage/rdalaz.py` | 每整点 UT 算一次 |
| 穿刺点 | `PunctureIonosphereCoord/ippcoor_v1.py` | 球面几何，层高 = IONEX 头 `HGT1`（CODE 为 450 km） |
| VTEC | `IONEX/teccalc.py` | 13 张图 → 线性插成 25 张（奇数小时按 IONEX 手册“方法 3”左右平移 3 格 = 15°经度），再双线性插值 |
| 斜 TEC | `ionFRM.py` | VTEC / cos(穿刺点天顶角) |
| 磁场 | `IGRF/geomag70_linux` | 调 NOAA `geomag70.exe` + `IGRF13.COF`，取 X/Y/Z 投到视线 |

---

## 2. 安装（含本机验证过的 3 处补丁）

```bash
unset TMPDIR VIRTUAL_ENV; export HOME=/home/box
mkdir -p /workspace/scratch_ionfr && cd /workspace/scratch_ionfr
python3 -m venv venv && . venv/bin/activate
pip install --no-cache-dir numpy scipy future
git clone https://github.com/csobey/ionFR.git
cd ionFR/IGRF/geomag70_linux && gcc geomag70.c -o geomag70.exe -lm && cd ../..   # -lm 放最后，见坑 1
sed -i 's/^from scipy import pi/from math import pi/' ionFRM.py                     # 坑 2
sed -i 's/^from scipy import \*/import math\nfrom math import pi/' PunctureIonosphereCoord/ippcoor_v1.py   # 坑 3
```

仓内自带测试：LOFAR 核心看 08h37m05.6s+06d10m14.5s，2011-10-20，`test/codg2930.11i`（老 CODE 2 h 文件）。

```bash
mkdir -p ../run && cd ../run && cp ../ionFR/test/codg2930.11i .
rm -f IonRM.txt
python -u ../ionFR/ionFRM.py 08h37m05.6s+06d10m14.5s 52d54m54.6sn 6d52m11.7se 2011-10-20T00:00:00 codg2930.11i
```

本机结果与仓内 `test/IonRM.txt` 逐行比（13 行、小时列全等）：**TEC 列最大相对差 2.6e−12（即相同）**；磁场列最大差 0.0235 G、RM 列最大差 0.531 rad m⁻²（第 12 h：本机 1.5587 vs 仓内 2.0897）。只有 TEC 列相同，**磁场与 RM 不同**；仓内参考文件可能是换 IGRF13/改角度公式之前生成的（README 提到这两处更新），这只是推测，未核实。

---

## 3. 真实端到端：LOFAR 看脉冲星 B0329+54，平静日 vs 暴日

### 3.1 取 IONEX（匿名）+ 抽成 2 h

CDDIS 要 Earthdata 登录；AIUB 的 CODE 终版匿名可下（本机 HTTP 200）：

```bash
cd /workspace/scratch_ionfr/run
for d in 122 132; do curl -sfL -O https://download.aiub.unibe.ch/CODE/2024/COD0OPSFIN_2024${d}0000_01D_01H_GIM.INX.gz; done
gunzip -k COD0OPSFIN_2024*.INX.gz      # 解压后 1695739 / 1694767 B
grep -E 'MAPS IN FILE|INTERVAL|DHGT' COD0OPSFIN_20241320000_01D_01H_GIM.INX
```

```text
  3600                                                      INTERVAL            
    25                                                      # OF MAPS IN FILE   
   450.0 450.0   0.0                                        HGT1 / HGT2 / DHGT  
```

现在的 CODE 是 1 h、25 张图，ionFR 原样读会 `IndexError: index 26 is out of bounds`（坑 4）。本文用下面的脚本（存为 `thin_ionex_2h.py`）只保留 00, 02, …, 24 UT 的 TEC/RMS 图并改头：

```python
#!/usr/bin/env python3
"""把 1 h（25 张图）IONEX 抽成 ionFR 需要的 2 h（13 张图）：只保留 00,02,...,24 UT 的 TEC/RMS 图并重编号。"""
import sys
src, dst = sys.argv[1], sys.argv[2]
out, keep, in_header = [], True, True
for line in open(src):
    label = line[60:].strip()
    if in_header:
        if label == "# OF MAPS IN FILE":
            n = int(line[:6]); line = "%6d" % ((n + 1) // 2) + line[6:]
        elif label == "INTERVAL":
            line = "%6d" % (int(line[:6]) * 2) + line[6:]
        elif label == "END OF HEADER":
            in_header = False
        out.append(line); continue
    if label.startswith("START OF") and "MAP" in label:
        k = int(line[:6]); keep = (k % 2 == 1)
        if keep: line = "%6d" % ((k + 1) // 2) + line[6:]
    if keep: out.append(line)
    if label.startswith("END OF") and "MAP" in label and keep:
        out[-1] = "%6d" % ((k + 1) // 2) + line[6:]
    if label == "END OF FILE": out.append(line) if not keep else None
open(dst, "w").writelines(out)
```

```bash
python -u thin_ionex_2h.py COD0OPSFIN_20241220000_01D_01H_GIM.INX cod2h_122.inx
python -u thin_ionex_2h.py COD0OPSFIN_20241320000_01D_01H_GIM.INX cod2h_132.inx
grep -c 'START OF TEC MAP' cod2h_132.inx    # 13；RMS 图也是 13
```

### 3.2 运行

B0329+54：RA 03h32m59.37s，Dec +54°34′43.6″；LOFAR 核心 52°54′54.6″N 6°52′11.7″E。在 52.9°N 这颗源是拱极星，24 小时都有输出。2024-05-01（DOY 122）是平静日，2024-05-11（DOY 132）是 Gannon 大磁暴次日。

```bash
for d in 122:2024-05-01 132:2024-05-11; do doy=${d%%:*}; day=${d#*:}; rm -f IonRM.txt
  python -u ../ionFR/ionFRM.py 03h32m59.37s+54d34m43.6s 52d54m54.6sn 6d52m11.7se ${day}T00:00:00 cod2h_${doy}.inx > geomag_${doy}.log 2>&1
  mv IonRM.txt IonRM_${doy}.txt; done
```

每天约 3.6 s（本机墙钟 3.59 s / 3.69 s）。stdout 只有 geomag70 每小时打印一次的横幅（每天 192 行非空），结尾是 ` Processed 1 lines`；结果全在 `IonRM.txt`。

### 3.3 本机输出

`IonRM_132.txt` 原样前 3 行（无表头；列 = 小时 UT、斜 TEC [m⁻²]、视线磁场 [G]、RM [rad m⁻²]、RM 不确定度 [rad m⁻²]）：

```text
00 3.513642032494135e+17 0.08391575852980704 0.7666098345332916 0.09584958103405845
01 3.205136128736384e+17 0.09109637044077297 0.7591382970508341 0.1120169301413616
02 2.8747013347519645e+17 0.10589512978778697 0.7914838644561777 0.10358809182966908
```

换成可读单位（sTEC ÷ 1e16 = TECU；Bpar 为 DOY 132 的值；每 3 h 摘一行，本机 Python 打印）：

```text
UT_h  sTEC_0501_TECU  sTEC_0511_TECU  Bpar_G  RM_0501_rad_m2  RM_0511_rad_m2  RMerr_0511_rad_m2
   0           22.96           35.14  0.0839          0.4987          0.7666            0.0958
   3           24.34           19.33  0.1280          0.7132          0.6434            0.1304
   6           24.90           12.07  0.2300          1.3252          0.7220            0.1102
   9           24.90           12.16  0.3354          2.0469          1.0603            0.1660
  12           22.57           14.85  0.3724          2.1855          1.4381            0.1269
  15           24.79           21.29  0.3150          2.1562          1.7440            0.1627
  18           32.33           15.41  0.2022          1.9152          0.8104            0.1324
  21           34.47           15.88  0.1091          1.1114          0.4503            0.1165
0501: RM min 0.4987 @UT0  max 2.3288 @UT11  mean 1.4806 rad m^-2; sTEC mean 26.25 TECU
0511: RM min 0.3721 @UT22  max 1.8420 @UT14  mean 0.9479 rad m^-2; sTEC mean 17.65 TECU
```

读法：两天几何相同（Bpar 只差 IGRF 日期），RM 的差别几乎全来自 TEC。5 月 11 日白天欧洲上空是**负暴**，06–12 UT 斜 TEC 只有平静日的一半左右（12.07 vs 24.90 TECU），日均 RM 从 1.48 降到 0.95 rad m⁻²。RM 峰值出现在源最高（B 视线分量最大，~12 UT）且 TEC 较大的时段，不一定在 TEC 峰值时刻。

### 3.4 和 spinifex 对照（同源同站同日、同一 CODE 文件）

spinifex 2.0（`get_rm_from_skycoord`，`prefix="cod", server="cddis"`，预先放好 AIUB 的 DOY 132/133 文件，所以没有联网登录；安装与取数：`pip install --no-cache-dir spinifex`，`mkdir -p ionex_files && for d in 132 133; do curl -sfL -O --output-dir ionex_files https://download.aiub.unibe.ch/CODE/2024/COD0OPSFIN_2024${d}0000_01D_01H_GIM.INX.gz; done`）。脚本 `rm_b0329.py`：

```python
import numpy as np, astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from spinifex import get_rm
lofar = EarthLocation(lat=(52+54/60+54.6/3600)*u.deg, lon=(6+52/60+11.7/3600)*u.deg, height=0*u.m)
src = SkyCoord("03h32m59.37s", "+54d34m43.6s", frame="icrs")
times = Time("2024-05-11T00:00:00") + np.arange(0, 24, 3)*u.hour
rm = get_rm.get_rm_from_skycoord(loc=lofar, times=times, source=src, prefix="cod", server="cddis", output_directory="ionex_files")
print("UT     elev_deg  B_par_nT  RM_rad_m2  RMerr_rad_m2")
for i, t in enumerate(times):
    print(f"{t.iso[11:16]}  {rm.elevation[i]:7.2f} {rm.b_parallel[i,0]:9.1f}  {rm.rm[i]:.4f}   {rm.rm_error[i]:.4f}")
```

本机 stdout（`python -u rm_b0329.py 2>err.log`）：

```text
UT     elev_deg  B_par_nT  RM_rad_m2  RMerr_rad_m2
00:00    17.59   -8360.6  0.7686   0.0984
03:00    24.54  -11734.5  0.5893   0.1027
06:00    41.84  -21667.7  0.6884   0.1065
09:00    65.39  -32735.3  1.0163   0.1285
12:00    87.54  -37108.4  1.4432   0.1308
15:00    62.11  -31709.6  1.5904   0.1349
18:00    39.15  -20291.7  0.8216   0.1351
21:00    22.97  -10937.8  0.4818   0.1066
```

| UT | ionFR RM | spinifex RM | 差 | 说明 |
| ---: | ---: | ---: | ---: | --- |
| 00 | 0.7666 | 0.7686 | −0.3% | 偶数小时：ionFR 用原图 |
| 06 | 0.7220 | 0.6884 | +4.9% | 同上 |
| 12 | 1.4381 | 1.4432 | −0.4% | 同上 |
| 18 | 0.8104 | 0.8216 | −1.4% | 同上 |
| 03 | 0.6434 | 0.5893 | +9.2% | 奇数小时：ionFR 用平移插值图（原 1 h 图被抽掉） |
| 15 | 1.7440 | 1.5904 | +9.7% | 同上 |

视线磁场大小一致（12 UT：ionFR 0.3724 G = 37236 nT，spinifex |B_par| = 37108 nT）；spinifex 的 B_par 为负、RM 为正，ionFR 的 B 和 RM 都为正——两者 RM 同号。只比了 RM 与 B 这两列、8 个时刻，**不是全字段一致**。

### 3.5 2025 年以后的日期（换 IGRF-14）

IGRF13.COF 只到 2025.00，更晚的日期会让 geomag70 死循环（坑 6）。NCEI 的 IGRF-14 COF 可直接替换（在 `/workspace/scratch_ionfr` 下执行）：

```bash
cd /workspace/scratch_ionfr
curl -sfL -O https://www.ncei.noaa.gov/sites/default/files/2025-01/IGRF14_0.zip && python3 -m zipfile -e IGRF14_0.zip ionFR/IGRF/geomag70_linux/
sed -i 's/IGRF13\.COF/IGRF14.COF/g' ionFR/ionFRM.py
```

本机用 CODE 2026 DOY 250（2026-09-07，同样抽 2 h）：24 行全部输出，RM 0.582–1.7378 rad m⁻²；12 UT 斜 TEC 38.37 TECU、B 0.1406 G、RM 1.4029 rad m⁻²。同一 DOY 132 输入下 IGRF-14 与 IGRF13 的 RM 最大差 0.0021 rad m⁻²、B 最大差 0.00042 G。

---

## 4. 参数与输出字段

命令：`ionFRM.py <RA±DEC> <纬度> <经度> <日期> <IONEX 文件>`，恰好 5 个参数。

| 参数 | 格式 | 例 | 注意 |
| --- | --- | --- | --- |
| RA±DEC | `HHhMMmSS.Ss±DDdMMmSS.Ss` | `03h32m59.37s+54d34m43.6s` | 正赤纬也要写 `+` |
| 纬度 | `DDdMMmSS.Ss` + `n`/`s` | `52d54m54.6sn` | 末字母决定南北，不能写负号 |
| 经度 | `DDdMMmSS.Ss` + `e`/`w` | `6d52m11.7se` | 同上 |
| 日期 | `YYYY-MM-DDT00:00:00` | `2024-05-11T00:00:00` | 只用日期部分，内部循环 0–23 h UT |
| IONEX | 路径 | `cod2h_132.inx` | 必须当天、13 张图（2 h）、5°经度×2.5°纬度格网（行格式写死） |

`IonRM.txt`（空格分隔，无表头，**追加写**）：

| 列 | 含义 | 单位 | 备注 |
| ---: | --- | --- | --- |
| 1 | 小时 | UT，`00`–`23` | 源仰角 ≤ 0° 的小时不写 |
| 2 | 斜 TEC | m⁻²（÷1e16 = TECU） | VTEC/cos(穿刺点天顶角) |
| 3 | 视线磁场 | 高斯 G | 用 `abs(X)`、`abs(Y)`、`abs(Z)` 按视线几何组合；本例 24 行全为正（源在北方低仰角时理论上可为负，未测） |
| 4 | RM | rad m⁻² | `2.6e-17 × 列3 × 列2` |
| 5 | RM 不确定度 | rad m⁻² | 只来自 IONEX RMS 图；不含 IGRF 误差 |

中间文件：`ionFR/IGRF/geomag70_linux/input.txt`、`output.txt` 写在**安装目录**里（不是当前目录）。

---

## 5. 结果怎么读

- 北半球 RM 为正 = 视线磁场指向观测者（README 定义）。README 说**南半球**结果要乘 −1；源码里磁场分量都取了绝对值，这个符号处理本文**未验证**。
- 同一代码里东向分量 Y 的投影项与北向 X 项符号不对称（`+Y·sin z·sin A` vs `−X·sin z·cos A`，且都取了绝对值）；欧洲 Y 很小，本例与 spinifex 在偶数小时相差 ≤5%。磁偏角大的台站是否受影响**未验证**。
- 不确定度列量级 0.1 rad m⁻²，和 RM 本身（0.4–2.3）比不小；低仰角时 1/cos 放大 TEC，RM 与误差一起变大。
- 抽 2 h 的代价：奇数小时变成平移插值，本例比 spinifex 用原 1 h 图时偏大约 9%。需要逐小时精度的新数据，优先 [spinifex](./spinifex.md)。

---

## 6. 坑（现象 → 原因 → 一条修复命令；全部本机复现）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | README 的 `gcc -lm geomag70.c -o geomag70.exe` 报 `undefined reference to 'log'` / `'atan2'` | 新 ld 按顺序解析，`-lm` 必须在源文件后面 | `gcc geomag70.c -o geomag70.exe -lm` |
| 2 | `ImportError: cannot import name 'pi' from 'scipy'` | 新 SciPy 已删掉 `scipy.pi` | `sed -i 's/^from scipy import pi/from math import pi/' ionFRM.py` |
| 3 | 修了 2 后 `NameError: name 'pi' is not defined`（`ippcoor_v1.py` 第 41 行） | 靠 `from scipy import *` 带进 `pi` 和 `math`，新 SciPy 不再导出 | `sed -i 's/^from scipy import \*/import math\nfrom math import pi/' PunctureIonosphereCoord/ippcoor_v1.py` |
| 4 | 用现在的 CODE/IGS 文件 → `IndexError: index 26 is out of bounds for axis 0 with size 25` | 代码写死 13 张图、间隔 2 h；现行 GIM 为 1 h 25 张 | `python -u thin_ionex_2h.py IN.INX out_2h.inx`（§3.1 脚本） |
| 5 | 同一目录跑两次，`IonRM.txt` 变 26 行，画图出现重复小时 | 输出以追加模式 `'a'` 打开 | 每次先删：`rm -f IonRM.txt && python -u ionFRM.py …` |
| 6 | 2025 年以后的日期**卡死**，5 s 内刷出 790 MB 的 `Enter the date (1900.00 to 2025.00)` | IGRF13.COF 只到 2025.00，geomag70 在无输入时反复提示 | 换 IGRF-14：§3.5 的 `curl … IGRF14_0.zip` + `sed -i 's/IGRF13\.COF/IGRF14.COF/g' ionFRM.py` |
| 7 | 经度靠近 ±180°：168°E 时奇数小时 TEC=0、RM=0；175°E 直接 `IndexError: index 73 is out of bounds for axis 2 with size 73` | 奇数小时插值只填 `4 ≤ lon ≤ pointsLon-4` 的格点，边缘留 0；格点查找不跨日界线 | 这类台站（如新西兰）改用 spinifex：`pip install --no-cache-dir spinifex` |
| 8 | `url_download.py` / `ftpdownload.py` / `IONEX/IONEXFileNeeded.py` 报 `SyntaxError: Missing parentheses in call to 'print'`；即使修好，CDDIS 也要 Earthdata `.netrc` | Python 2 语法；CDDIS 取消了匿名 | 直接从 AIUB 取：`curl -sfL -O https://download.aiub.unibe.ch/CODE/2024/COD0OPSFIN_20241320000_01D_01H_GIM.INX.gz` |

---

## 7. 和相关工具怎么选

| 工具 | 状态 | 什么时候用 |
| --- | --- | --- |
| **ionFR** | 2021 后不再更新；Py2 遗留，需补丁；只吃 2 h IONEX | 复现 Sotomayor-Beltran 2013 及引用它的旧论文 |
| [spinifex](./spinifex.md) | ASTRON/CSIRO 在维护，PyPI 2.0；IGRF-14、1 h/15 min GIM、日固旋转插值、可选 IRI 剖面 | 新项目默认选它 |
| [RMextract](https://github.com/lofar-astron/RMextract) | GPL-3.0，★36，仓库自述已被 spinifex 取代（PROJECTS 同样标注） | 复现 LOFAR 旧流程；本文**未实跑** |

GIM 本身的来源与质量对比见 [ionex](./ionex.md)、[gim-product-portals](./gim-product-portals.md)、教程 [03 GIM/IONEX](../tutorials/03-gim-ionex.md)、[18 GIM 对比](../tutorials/18-lab-compare-gims.md)。IGRF 倾角的另一用法见 [hwm14](./hwm14.md) §3.3。

---

## 8. 许可与诚实局限

- **GPL-3.0**（`LICENSE`）。附带 NOAA geomag70 C 程序与 IGRF 系数（公共数据）。
- 本文实跑：仓内 2011 测试复现（TEC 列相同、B/RM 不同）；B0329+54 @ LOFAR 2024-05-01/05-11 全天；与 spinifex 8 个时刻对照；2026-09-07 换 IGRF-14；坑 1–8 全部复现；2 路并行（不同目录、同一安装）本次输出与串行逐值相同，但 `input.txt`/`output.txt` 共享，**不保证并行安全**。
- **未实跑 / 未验证**：南半球符号（README 要求 ×(−1)）；磁偏角大的台站；Python 2 原环境；`url_download.py` 带 Earthdata 登录下载；IGS `igsg` 等其他分析中心文件；不装 scipy 时是否能跑（补丁后源码已不再 import scipy，但未在无 scipy 环境测）。
- `thin_ionex_2h.py` 是本文写的变通脚本，不是上游代码；它丢掉奇数小时图，精度代价见 §3.4。
- 单层模型（450 km）+ 气候态 IGRF，不含等离子体层贡献；spinifex 文档里 `ionex_iri` 剖面模式对低仰角 RM 的修正（−14%～−18%）ionFR 没有。
