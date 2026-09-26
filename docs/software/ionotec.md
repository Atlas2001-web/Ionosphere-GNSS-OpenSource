# ionotec · RINEX 2 → 整平 VTEC（带 IPP）轻量 Python 库 操作手册

目录：上游 <https://github.com/sylvathle/ionotec>（Sylvain Blunier / Chilean-Complexity-Cluster，★6）· PyPI **`ionotec` 0.0.15**（2026-03-16 上传）· **MIT** · 本机验证 **2026-09-26 03:31–03:40 EDT**：CPython 3.11.16 venv，georinex 1.16.2 / xarray 2026.7.0 / pandas 3.0.6 / numpy 2.4.6；BKG 2024-08-22（DOY 235）WTZA RINEX 2.11 全天 + CAS 日 DSB，与 CODE 终版 GIM 对比：el>30° 差 **−1.69±2.79 TECU**，补上 C1C−C1W 后 **−1.39±1.34 TECU**（§4）。

> **质检复跑通过**（2026-09-26 03:43–03:47 EDT）。
> - 环境：独立 uv venv，ionotec 0.0.15 / georinex 1.16.2 / xarray 2026.7.0 / pandas 3.0.6 / numpy 2.4.6，与原文一致；PyPI 上传日 2026-03-16、MIT（`License-Expression: MIT`，LICENSE 首行 Copyright 2022 Chilean-Complexity-Cluster）、上游 HEAD `8e54598` 均核对无误。
> - 逐字复现：BKG 三个文件字节数（525200/53336/60593）和 CODE GIM 355254 B；§3 stdout（13221 行、30 星、`br_gps` 5.90983524013795、前 3 行逐位一致），35 个产物、`wtza.feather` 704986 B，每星 253–545 行，G18 缺失；§4 `vs_gim.py` 五行输出全部逐位一致（el>30° −1.69/2.79/3.26，相关 −0.92，补 C1C−C1W 后 −1.39/1.34/1.93）；坑 1 的 sed 补丁同命令重跑 `br_gps` 17.90929817、el>30° −2.31/1.38/2.69、相关 −0.01，与 §4 末逐位一致；坑 5 的 `FileNotFoundError`（`getBias_fromfile`）复现；§8 的 VTEC 中位 23.6、四分位 17.2–32.2、IPP 纬度 30.5–66.7°、经度 −15.5–41.8°、最低仰角 0.0008 rad 复现。
> - 修正：耗时本次 5.9 s（原 4.4 s），§9 改为 4–6 s；其余无改动。
> - 未复跑：坑 2（RINEX 3 KeyError）、坑 4（换导航文件复用旧星位）、坑 10（上游 main `ValueError`）和 GLONASS 路径；venv 用 uv 硬链接装，占用数字与原文 pip `--no-cache-dir` 的 696 MB 不可比。

> 岗位：给一个测站的 RINEX 2 观测 + 广播星历 + Bias-SINEX，一次调用出“每星每分钟一行”的 **STEC（码/相位/整平后）+ VTEC + 穿刺点经纬度**，存成 feather。  
> 版本注意：PyPI 0.0.15 的代码**不等于**上游任何一个 git 提交；上游 main `8e54598`（2026-08-28，“Major modification”，作者自注“All still needs to be heavily tested”）API 已变，本机用同一脚本在 `gnss.compute_position` 报 `ValueError: Length of new names must be 1, got 2`。**本文只写 PyPI 0.0.15**。冲突时：本机 `site-packages/ionotec/tec.py` > 上游 README > 本文。

## 1. 它解决什么（术语先讲清）

| 术语 | 一句话 | 在 ionotec 里 |
| --- | --- | --- |
| **STEC**（斜 TEC） | 接收机→卫星视线上 1 m² 柱内电子数；1 TECU = 10¹⁶ e/m² | `STEC_slp`（码）、`STEC_sll`（相位，内存中）、`STEC_sl`（整平+扣卫星 DCB 后） |
| 码 STEC | `α·(P2−C1)`，α = f1²f2²/(40.3·(f1²−f2²))；噪声几 TECU，含 DCB | **用的是 P2−C1，不是 P2−P1**（§7 坑 1） |
| 相位 STEC | `α·(λ1L1−λ2L2)`，毫 TECU 级平滑，但含整周模糊度常数 | 先按跳变切段，再整平 |
| **整平（leveling / baseline）** | 每段连续弧把相位 STEC 平移到码 STEC 的 sin²(el) 加权均值 | `add_baseline()`；只信 >50 min 的段，短段靠斜率“粘”到邻段 |
| **DCB / DSB** | 卫星、接收机两个码的硬件延迟差；1 ns ≈ **2.85 TECU**（GPS L1/L2） | 卫星：读 Bias-SINEX 里 `DSB … C1W C2W`（GLONASS `C1P C2P`）；接收机：自己估 |
| 接收机 DCB 估计 | 假设同一时刻各星 VTEC 应相同，求使“各星 VTEC 方差之和”最小的常数 | `compute_receiver_bias()`，el>30° 数据；结果写 `receiver_bias.csv`（TECU） |
| **IPP**（电离层穿刺点） | 视线与高度 h 的薄球壳的交点 | h 默认 **400 km**；输出 `lat`/`lon` |
| **VTEC** / 映射函数 | 薄壳假设下 `VTEC = STEC·cos χ`，`sin χ = R/(R+h)·cos el`（单层映射函数） | `VTEC` 列，已减接收机 DCB |

一句话：ionotec = **georinex 读数 + 广播星历算星位 + 切段整平 + 卫星/接收机 DCB + 单层映射**，一条龙到单站 VTEC。不产出 GIM，不做多站联合，不写 IONEX。

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3.11 -m venv ionotec-venv && . ionotec-venv/bin/activate
pip install --no-cache-dir ionotec      # 拉 georinex、pandas、scipy、pyarrow、matplotlib、cartopy…
pip show ionotec | head -2              # Name: ionotec / Version: 0.0.15
du -sh ionotec-venv                     # 本机 696M（cartopy/matplotlib/pyarrow 占大头）
```

- 上游 README 让你 `pip install xarray==0.20.1`；本机 xarray **2026.7.0** + georinex 1.16.2 能正常读 RINEX 2，**不必降级**（georinex 只打 `FutureWarning`）。
- 没有 CLI；`import ionotec.tec` 时就会在**启动脚本所在目录**建 `output/` 并打印 `Output directory: …`（坑 3）。

## 3. 端到端 A：WTZA 一整天（本机真跑）

数据（本机 CDDIS / IGN FTP 返回 425，BKG HTTPS 可用；CAS 日 DSB 在 BKG 的 `products/<GPS周>/` 而不是 `products/mgex/`）：

```bash
mkdir -p ~/iono_ops/ionotec-demo/data && cd ~/iono_ops/ionotec-demo
B=https://igs.bkg.bund.de/root_ftp/IGS
curl -sfO --output-dir data $B/obs/2024/235/wtza2350.24d.gz          # 525200 B，RINEX 2.11 Hatanaka，C1 P1 P2 L1 L2…，30 s
curl -sfO --output-dir data $B/BRDC/2024/235/brdc2350.24n.gz         # 53336 B
curl -sfO --output-dir data $B/products/2328/CAS0OPSRAP_20242350000_01D_01D_DCB.BIA.gz   # 60593 B
gunzip -k data/brdc2350.24n.gz data/CAS0OPSRAP_20242350000_01D_01D_DCB.BIA.gz   # DSB 文件必须解压（纯文本逐行 split）
```

`.24d.gz` 观测直接喂即可（georinex 调 `hatanaka` 解 CRX）；导航 `.gz` 与解压版本机都能读。脚本 `run_ionotec.py`：

```python
import time, sys
t0 = time.time()
from ionotec import tec
obs = sys.argv[1]
st = tec.tec([obs], ["data/brdc2350.24n"], "data/CAS0OPSRAP_20242350000_01D_01D_DCB.BIA")
st.compute_vtec()
df = st.df_obs
print("station:", st.station, "rows:", len(df), "sats:", df["sv"].nunique())
print("br_gps (TECU):", st.br_gps)
print(df.head(3).to_string())
print(f"elapsed {time.time()-t0:.1f} s")
```

```bash
python -u run_ionotec.py data/wtza2350.24d.gz
```

真实 stdout：

```text
Output directory: /workspace/scratch_ionotec_spinifex/ionotec_run/output
Successfully created the directory /workspace/scratch_ionotec_spinifex/ionotec_run/output/GNSS/
station: wtza rows: 13221 sats: 30
br_gps (TECU): 5.90983524013795
                      sv        lat       lon  elevation   cos_chi    STEC_sll   STEC_slp    STEC_sl       VTEC        br
time                                                                                                                     
2024-08-22 10:05:00  G06  56.082771 -6.495965   0.132233  0.360627 -100.394839  85.781270  70.716398  23.370987  5.909835
2024-08-22 10:06:00  G06  56.011709 -6.066985   0.138933  0.362823 -100.353706  87.731926  70.757531  23.528229  5.909835
2024-08-22 10:07:00  G06  55.939882 -5.649104   0.145646  0.365115 -100.414003  88.512188  70.697234  23.654856  5.909835
elapsed 4.4 s
```

产物（`find output -type f`）：`output/GNSS/2024/G01…G32.feather`（广播星历算出的每分钟卫星 ECEF，32 个，每个 ~43 KB）、`output/GNSS/record_processing.csv`（`2024-08-22,60,0`）、`output/TEC/2024/wtza.feather`（704986 B）、`output/TEC/2024/receiver_bias.csv`（`wtza,5.90983524013795,`）。

读法：`STEC_sll` −100 是相位 STEC + 任意常数；`STEC_slp` 85.8 是码 STEC；整平+扣卫星 DSB 后 `STEC_sl` 70.7；再减接收机偏差 5.91 TECU、乘 `cos_chi` 0.36 得 VTEC 23.4。`elevation` 是**弧度**（0.13 rad ≈ 7.6°）。全天 30 颗 GPS、每星 253–545 行、1 min 一行；观测里有 31 颗，**G18 整星被丢**（未查原因，推测是没有 >50 min 的“健康段”）。

## 4. 端到端 B：与 CODE 终版 GIM 在 IPP 处对比（本机真跑）

与 [tec-suite](./tec-suite.md) §4 同一天、同一站、同一 CODE 文件，便于横比。脚本 `vs_gim.py`（时间线性 + 空间双线性插 GIM；el>30° 时每 5 min 取样）：

```python
# vs_gim.py — ionotec feather 与 CODE IONEX 在 IPP 处逐点比较
import sys, numpy as np, pandas as pd, datetime as dt
fea, inx = sys.argv[1], sys.argv[2]
L = open(inx).read().splitlines(); maps, ep = [], []
for i, s in enumerate(L):
    lab = s[60:].strip()
    if lab == 'START OF TEC MAP':
        ep.append(dt.datetime(*map(int, L[i+1][:36].split()))); g, j = [], i + 2
        while len(g) < 71:
            v = ''.join(L[j+1:j+6]); g.append([int(v[k:k+5]) * 0.1 for k in range(0, 365, 5)]); j += 6
        maps.append(np.array(g))
    elif lab == 'START OF RMS MAP': break
M = np.array(maps)
def gim(t, la, lo):
    x = (t - ep[0]).total_seconds() / 3600; k = min(int(x), 23); w = x - k
    fi, fj = (87.5 - la) / 2.5, ((lo + 180) % 360) / 5; i0, j0 = int(fi), int(fj); a, b = fi - i0, fj - j0
    g = (1 - w) * M[k] + w * M[k + 1]
    return (1-a)*(1-b)*g[i0, j0] + (1-a)*b*g[i0, j0+1] + a*(1-b)*g[i0+1, j0] + a*b*g[i0+1, j0+1]
d = pd.read_feather(fea)
d['GIM'] = [gim(t.to_pydatetime(), la, lo) for t, la, lo in zip(d.time, d.lat, d.lon)]
for name, m in [('all el', d.elevation > -1), ('el>30deg', d.elevation > np.radians(30))]:
    s = d[m]; s5 = s[s.time.dt.minute % 5 == 0] if name != 'all el' else s
    dv = s5.VTEC - s5.GIM
    print(f'{name:9s} n={len(s5):5d} VTEC={s5.VTEC.mean():.2f} GIM={s5.GIM.mean():.2f} '
          f'diff mean={dv.mean():.2f} std={dv.std():.2f} RMS={np.sqrt((dv**2).mean()):.2f} TECU')
s = d[d.elevation > np.radians(30)]
per = (s.VTEC - s.GIM).groupby(s.sv).mean()
print('per-sat mean diff (el>30): min %.2f (%s) max %.2f (%s)' % (per.min(), per.idxmin(), per.max(), per.idxmax()))
if len(sys.argv) > 3:   # 可选：与 C1C−C1W 卫星 DSB 做相关（坑：ionotec 用 P2−C1 却只扣 C1W−C2W）
    q = {}
    for l in open(sys.argv[3]):
        p = l.split()
        if len(p) > 8 and p[0] == 'DSB' and p[3] == 'C1C' and p[4] == 'C1W' and len(p[2]) == 3: q[p[2]] = float(p[8])
    x = np.array([q.get(k, np.nan) for k in per.index]); ok = ~np.isnan(x)
    print('corr(per-sat diff, C1C-C1W DSB) = %.2f over %d sats' % (np.corrcoef(per.values[ok], x[ok])[0, 1], ok.sum()))
    s = s.copy(); s['fix'] = s.VTEC + 2.854 * s.sv.map(q) * s.elevation.map(lambda e: np.cos(np.arcsin(6371/(6771)*np.cos(e))))
    s5 = s[s.time.dt.minute % 5 == 0]; dv = s5.fix - s5.GIM
    print(f'el>30deg +C1C-C1W fix n={len(s5)} diff mean={dv.mean():.2f} std={dv.std():.2f} RMS={np.sqrt((dv**2).mean()):.2f} TECU')
```

```bash
curl -sfL -O --output-dir data https://www.aiub.unibe.ch/download/CODE/2024/COD0OPSFIN_20242350000_01D_01H_GIM.INX.gz   # 355254 B；-L 必须
gunzip -k data/COD0OPSFIN_20242350000_01D_01H_GIM.INX.gz
python -u vs_gim.py output/TEC/2024/wtza.feather data/COD0OPSFIN_20242350000_01D_01H_GIM.INX data/CAS0OPSRAP_20242350000_01D_01D_DCB.BIA
```

```text
all el    n=13221 VTEC=24.57 GIM=26.59 diff mean=-2.01 std=2.51 RMS=3.22 TECU
el>30deg  n= 1325 VTEC=24.47 GIM=26.16 diff mean=-1.69 std=2.79 RMS=3.26 TECU
per-sat mean diff (el>30): min -7.25 (G19) max 2.36 (G23)
corr(per-sat diff, C1C-C1W DSB) = -0.92 over 30 sats
el>30deg +C1C-C1W fix n=1325 diff mean=-1.39 std=1.34 RMS=1.93 TECU
```

结论（只针对这 1 站 1 天）：

- 原样输出比 CODE 低 ~1.7 TECU，逐星偏差从 −7.3 到 +2.4 TECU；这个逐星偏差与 CAS 的卫星 **C1C−C1W** DSB 相关系数 **−0.92**——因为码 STEC 用的是 `P2−C1`，库却只扣了 `C1W−C2W`（坑 1）。
- 自己补上 `+2.854·DSB(C1C−C1W)·cos χ` 后离散从 2.79 降到 **1.34 TECU**；剩下 −1.4 TECU 的系统差来自接收机偏差估计（方差最小法假设各星 VTEC 同值）、h=400 km（CODE 用 450 km 修正映射）以及 GIM 本身的平滑。
- 实测坑 1 的补丁（把 `P2−C1` 改成 `P2−P1`，其余不动，同命令重跑）：`br_gps` 从 5.91 变 **17.91 TECU**，对比输出为

```text
all el    n=13221 VTEC=24.00 GIM=26.59 diff mean=-2.58 std=1.56 RMS=3.01 TECU
el>30deg  n= 1325 VTEC=23.85 GIM=26.16 diff mean=-2.31 std=1.38 RMS=2.69 TECU
per-sat mean diff (el>30): min -4.29 (G03) max 1.16 (G29)
corr(per-sat diff, C1C-C1W DSB) = -0.01 over 30 sats
```

  逐星相关消失、离散 1.38 TECU；此时脚本第 5 行（再补 C1C−C1W）不再适用，忽略。系统差 −2.3 TECU 仍在，来自接收机偏差估计与映射高度。
- 横比：tec-suite + 自写整平脚本同条件得 **+0.30±2.05 TECU**（它用 `P2−P1`，接收机 DCB 直接取 CODE IONEX 头）。

## 5. 参数与输出字段

`tec.tec(list_f_obs, f_nav, f_sat_bias, outfolder="output", resolution=60, h=400000)`

| 参数 | 类型 / 默认 | 说明（以 0.0.15 源码为准） |
| --- | --- | --- |
| `list_f_obs` | list[str] | 同一测站、按时间顺序的观测文件；头信息取**第 2 个**文件（只有 1 个时取第 1 个） |
| `f_nav` | list[str] | GPS `*.YYn`、GLONASS `*.YYg`；按文件内中间历元的日期登记“已处理” |
| `f_sat_bias` | str | Bias-SINEX（CAS `…DCB.BIA`），找 `DSB <PRN> C1W C2W`（R 星 `C1P C2P`）第 9 列（ns） |
| `outfolder` | `"output"` | **不生效**：实际目录由 `stations.py` 按 `sys.argv[0]` 所在目录定死 |
| `resolution` | 60 | **不生效**：`__init__` 里写死 `self.resolution = 60`（秒），观测按 60 s 取均值 |
| `h` | 400000 | 薄壳高度（m），影响 IPP 与 `cos_chi` |

| 输出列（`wtza.feather`） | 含义 | 单位 |
| --- | --- | --- |
| `time` | 历元（UTC 标注的 GPS 时间，按分钟重采样） | datetime64 |
| `sv` | 卫星号 `G01`/`R07` | — |
| `lat`, `lon` | IPP 大地纬度/经度（h 高度） | ° |
| `elevation` | 高度角，**弧度**；不设截止角，最低到 ~0 | rad |
| `STEC_slp` | 码 STEC，`α(P2−C1)` | TECU |
| `STEC_sl` | 整平后相位 STEC + 卫星 DSB(C1W−C2W) | TECU |
| `VTEC` | `(STEC_sl − br)·cos χ` | TECU |

`receiver_bias.csv`：`station,br_gps,br_glonass`，单位 TECU（不是 ns）；同站重跑会覆盖该行。内存对象 `st.df_obs` 还有 `cos_chi`、`STEC_sll`、`br` 三列。

## 6. 与相邻手册怎么选

| 需求 | 选 |
| --- | --- |
| RINEX 2 单站，一次调用拿到整平+DCB+VTEC+IPP | **ionotec**（本文） |
| RINEX 2/3，只要原始逐星 STEC 文本，自己整平/建图 | [tec-suite](./tec-suite.md)（再接 [mosgim2](./mosgim2.md)） |
| 只要库函数算相位/伪距 TEC，自己拼后续 | [gnss-tec](./gnss-tec.md) |
| 多系统 RINEX 3、带周跳检测和 DCB 的完整单站校准 | [pytecgg](./pytecgg.md) |
| 读/画 GIM 做对照 | [ionex](./ionex.md) · [ionex-gim](./ionex-gim.md) |

## 7. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 逐星 VTEC 偏差 −7…+2 TECU，与卫星 C1C−C1W DSB 相关 −0.92 | 码 STEC 用 `P2−C1`（C1=C1C），只扣了 `C1W−C2W` | 观测里有 P1 时把 `C1` 改成 `P1`（本机实测，见 §4 末）：`sed -i "s/\['P2'\] - df_gps_temp\['C1'\]/['P2'] - df_gps_temp['P1']/" $(python -c "import ionotec,os;print(os.path.dirname(ionotec.__file__))")/tec.py` |
| 2 | RINEX 3 文件（如 `MAS100ESP_R_…_MO.crx.gz`）报 `KeyError: 'P2'` | 只认 RINEX 2 观测名 `P1 P2 C1 L1 L2`，RINEX 3 是 `C1C C2W L1C…` | 换 RINEX 2 文件：`curl -sfO $B/obs/2024/235/wtza2350.24d.gz`；RINEX 3 站点用 [pytecgg](./pytecgg.md) |
| 3 | 输出跑到了奇怪的地方 / 多个作业互相覆盖 | `output/` 固定建在 `sys.argv[0]` 所在目录（`python -c` 时是当前目录），`outfolder` 参数无效 | 每个作业一个目录并在里面跑脚本：`mkdir job1 && cp run_ionotec.py job1/ && cd job1 && python -u run_ionotec.py …` |
| 4 | 换了导航文件重跑，卫星位置/高度角没变 | `output/GNSS/record_processing.csv` 记着该日 `G_res=60`，直接复用旧的 `Gxx.feather` | `rm -rf output/GNSS` 后重跑 |
| 5 | `FileNotFoundError: … 'nobias.BIA'`（在 `getBias_fromfile`） | 构造时只打印“bias file location not found, will take 0”，真正用时 `open()` 崩 | 先下载并解压：`gunzip -k CAS0OPSRAP_20242350000_01D_01D_DCB.BIA.gz` |
| 6 | 找不到 CAS DSB（BKG `products/mgex/2328/` 404） | BKG 把 CAS 日 DSB 放在 `products/<GPS周>/` | `curl -sfO $B/products/2328/CAS0OPSRAP_20242350000_01D_01D_DCB.BIA.gz` |
| 7 | 低仰角 VTEC 噪声大、画图毛刺多 | 不设截止角，`elevation` 最低 0.0008 rad | 读结果时过滤：`d = d[d.elevation > np.radians(20)]` |
| 8 | 仰角当度数用，结果全错 | `elevation` 列是弧度 | `np.degrees(d.elevation)` |
| 9 | 某颗星整星缺失（本例 G18） | 只整平 >50 min 的健康段，没有就整弧丢弃 | 不修；需要全部星用 [tec-suite](./tec-suite.md) 的原始 STEC 自己整平 |
| 10 | 装了上游 main（`pip install git+…`）后同脚本报 `ValueError: Length of new names must be 1, got 2` | main `8e54598` 大改、未发 PyPI | 固定版本：`pip install --no-cache-dir ionotec==0.0.15` |

## 8. 怎么读结果

- 看单站日变化：`d.groupby(d.time.dt.floor('15min')).VTEC.median()`；WTZA 当日 VTEC 中位 23.6 TECU、四分位 17.2–32.2 TECU。
- 看空间：`lat`/`lon` 是 IPP，不是测站；400 km 壳上 WTZA 的 IPP 覆盖纬度 30.5–66.7°、经度 −15.5–41.8°（含 0° 仰角）。
- 绝对值信度：本例 el>30° 与 CODE 差 −1.7 TECU（补 C1C−C1W 后 −1.4±1.3 TECU）；**接收机偏差是按“同刻各星 VTEC 一致”估的**，赤道异常区/强梯度时这个假设会偏。
- 要多站地图：ionotec 只到单站；把多站 feather 合并后自己插值，或走 [tec-suite](./tec-suite.md) → [mosgim2](./mosgim2.md)。
- 原理：[02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md)、[09 DCB](../tutorials/09-dcb-biases-deep.md)、[16 一日 TEC 实践](../tutorials/16-practice-one-day-tec.md)。

## 9. 许可与诚实局限

- MIT（`LICENSE`，Copyright 2022 Chilean-Complexity-Cluster）。
- 只验证了 **1 站（WTZA）1 天、GPS-only**；GLONASS 路径（需 `*.YYg` 导航、内置频点号表）未测。
- PyPI 0.0.15 与 git 不对应；上游 main 自称未充分测试，本机同脚本不能跑。
- 固定 60 s 重采样、h 与映射函数单层、不做周跳修复（只按跳变切段粘接），不输出 RMS/质量标志。
- 单站全天 GPS-only 本机 4–6 s（两次实测 4.4 / 5.9 s，其中大半是 import）；venv 696 MB 偏重（cartopy 只在 `graph` 子模块用）。
