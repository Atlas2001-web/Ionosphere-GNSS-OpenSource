# tec-suite · RINEX → 逐星斜向 TEC（SIMuRG/gnss-lab）操作手册

目录：上游 <https://github.com/gnss-lab/tec-suite> · tip **`18465f9`**（2020-11-07，“Added l8c8 tec support”）· 版本字串 **v0.7.8** · **GPL-3.0-or-later**（`LICENSE` + `setup.py` “GPLv3+”）· 作者 Ilya Zhivetiev（[SIMuRG](https://simurg.space/) 团队用它给 SIMuRG / MosGIM 供数）· 本机验证 **2026-09-26 02:15–02:50 EDT**：CPython 3.11.16 + `future` 1.0.0 + `hatanaka`（提供 `crx2rnx`）；BKG 2024-08-22（DOY 235）WTZA（RINEX 2.11）与 MAS1（RINEX 3.04）单站全日；58 站批量 → 3073 个 `.dat`，交给 [mosgim2](./mosgim2.md) 建图；整平+扣 DCB 后与 CODE 终版 GIM 对比，WTZA 差 **+0.30±2.05 TECU**，MAS1 **−0.21±3.58 TECU**。

> 岗位：把 RINEX 观测 + 广播星历变成“每站每星一个文本文件”，列出历元、高度角/方位角、卫星 ECEF 与多种频率组合的**原始**斜 TEC。  
> 冲突时：**本机 `python tecs.py -v` / 上游 `docs/usage.rst` > 本文**。

## 1. 它解决什么、不解决什么

双频 GNSS 信号在电离层里的延迟与频率平方成反比，两频之差就能反推视线上的电子总量：

| 概念 | 一句话 | 在 tec-suite 里 |
| --- | --- | --- |
| **STEC**（斜 TEC） | 接收机→卫星视线上 1 m² 柱体内电子数，单位 TECU = 10¹⁶ e/m² | `tec.*` 列都是 STEC（TECU） |
| 码 TEC `tec.p1p2` | `K·(P2−P1)`，K = f1²f2²/(40.308(f1²−f2²))·10⁻¹⁶ ≈ **9.52 TECU/m**（GPS L1/L2） | 绝对量级对，但噪声几 TECU，且含 DCB |
| 相位 TEC `tec.l1l2` | `K·(λ1L1−λ2L2)`，毫 TECU 级平滑 | **含任意常数**（整周模糊度），负值很正常 |
| **DCB** | 卫星/接收机两频码硬件延迟差；1 ns ≈ **2.85 TECU** | **不扣**，要自己从 IONEX/Bias-SINEX 取 |
| **整平（leveling）** | 每段连续弧上把相位 TEC 平移到码 TEC 的加权均值 | **不做**，见 §4 脚本 |
| **VTEC / 薄壳 IPP** | 假设电子集中在高度 H（常取 450 km）的球壳；STEC×cos z′ = VTEC，穿刺点 IPP 处取值 | **不做**；只给 el/az 和卫星 XYZ，供下游算 |
| **GIM / IONEX** | 全球 VTEC 格网图（2.5°×5°，逐小时） | 不产出；下游 [mosgim2](./mosgim2.md) 用本工具的相位 TEC 建图 |

一句话：tec-suite = **RINEX 解析 + 广播星历算星位 + 组合出原始 STEC 的“数据准备”层**；绝对 TEC、VTEC、地图都在下游。

## 2. 安装（Linux，源码运行）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/gnss-lab/tec-suite && cd tec-suite
git log -1 --format='%h %ci'          # 本机：18465f9 2020-11-07 15:22:06 +0800
python3 -m venv ~/iono_ops/ts-venv && . ~/iono_ops/ts-venv/bin/activate
pip install future hatanaka           # future 是唯一 Python 依赖；hatanaka 提供 crx2rnx 命令
python tecs.py -v
# tecs v0.7.8
# Python 3.11.16 (main, Sep  1 2026, 14:18:37) [Clang 22.1.3 ]
```

上游 Release 另有 PyInstaller 打包的 `tec-suite-v0.7.8-linux64.tgz`（2020 年），同样只认 RINEX ≤3.03；本文全部用源码 + 下面两处**本地补丁**（上游 2020 年后未维护，不打补丁对现代 RINEX 3 会丢数据，原因见 §7 坑 2、3）：

```bash
cd ~/iono_ops/tec-suite
# 补丁 1：让 RINEX 3.04/3.05 观测文件按 3.03 解析
sed -i 's/^        3.03: Obs303$/        3.03: Obs303,\n        3.04: Obs303,\n        3.05: Obs303/' tecs/rinex/__init__.py
# 补丁 2：同一频段有多个码（L2L/L2W）时跳过空值，而不是永远取字母序第一个
sed -i '58s/            if ot in ot_set:/            if ot in ot_set and rec[ot][0]:/' tecs/gtb/tools.py
git diff --stat    # 2 files changed, 4 insertions(+), 2 deletions(-)
```

## 3. 端到端 A：单站 RINEX 2（WTZA，本机真跑）

数据：BKG IGS 镜像（本机 CDDIS/IGN FTP 425，BKG HTTPS 可用）。

```bash
mkdir -p ~/iono_ops/ts-demo/{obs,nav} && cd ~/iono_ops/ts-demo
B=https://igs.bkg.bund.de/root_ftp/IGS
curl -sfO --output-dir obs $B/obs/2024/235/wtza2350.24d.gz      # 525200 B，GPS-only，C1 P1 P2 L1 L2
curl -sfO --output-dir nav $B/BRDC/2024/235/brdc2350.24n.gz
cat > tecs.cfg <<'CFG'
obsDir = obs
navDir = nav
outDir = tec
recFields = 'datetime, el, az, tec.l1l2, tec.p1p2, tec.c1p2, validity'
datetimeFormat = '%Y-%m-%dT%H:%M:%S'
samplingInterval = 30
navPriorityGPS = brdc, auto
navIgnoreAbsence = False
logLevel = WARNING
CFG
python ~/iono_ops/tec-suite/tecs.py -c $PWD/tecs.cfg -q     # -c 必须绝对路径（坑 1）
```

真实 stdout：

```text
Trying to find observation files...done (1).
obs/wtza2350.24d.gz [1/1]: 
- reading...done.
- processing...
done.
Total processing time:  0.071 min.
```

```bash
ls tec/2024/235/wtza | wc -l                     # 31（每颗 GPS 星一个文件）
head -16 tec/2024/235/wtza/wtza_G11_235_24.dat
```

```text
# Created on 2026-09-26 06:24:00 
# Sources: obs/wtza2350.24d.gz, nav/brdc2350.24n.gz
# Satellite: G11
# Interval: 30.0
# Sampling interval: 30.0
# Site: wtza
# Position (L, B, H): 12.878902346936105, 49.144225165605334, 665.8970150351524
# Position (X, Y, Z): 4075578.4, 931852.75, 4801569.98
# datetime format: %Y-%m-%dT%H:%M:%S
# Columns: datetime, el, az, tec.l1l2, tec.p1p2, tec.c1p2, validity
# (A19,1X,F10.5,1X,F11.5,1X,F21.3,1X,F10.3,1X,F10.3,1X,I7)
2024-08-22T00:00:00   35.09715    61.81888              -104.014     36.824     27.963       0
2024-08-22T00:00:30   35.01917    61.57219              -103.989     36.348     26.697       0
2024-08-22T00:01:00   34.93987    61.32662              -103.962     37.538     27.221       0
```

（“Created on” 是 box 的 UTC 钟，= 02:24 EDT。）读法：`tec.l1l2` −104 是相位 TEC + 任意常数；`tec.p1p2` 36.8 是码 TEC，含 DCB；两者**逐历元差分**才有意义，或按 §4 整平。

`--save-coordinates` 只写站坐标、不算 TEC（0.003 min）：`coordinates.txt` → `wtza; 12.878902346936105; 49.144225165605334`（经度 0–360°、纬度）。

## 4. 端到端 B：整平 → 扣 DCB → 薄壳 VTEC → 对比 CODE GIM（本机真跑）

tec-suite 停在原始 STEC。下面 44 行脚本补齐下游三步，并在 IPP 处与 CODE 终版 GIM `COD0OPSFIN_20242350000_01D_01H_GIM.INX`（IONEX 头里带 GPS 卫星 DCB 与测站 C1W−C2W DCB）逐点比。

步骤：① 按 >35 s 断档或 |ΔL|>1 TECU 切弧；② 每弧 `offset = Σw(P−L)/Σw`，w = sin²el（el>10°），`STEC = L + offset`；③ `STEC += 2.854·(DCB_sat + DCB_rcv)`（IONEX 定义 DCB = b(P1)−b(P2)，而 `tec.p1p2` 用 P2−P1，所以是**加**）；④ H = 450 km 薄壳 `VTEC = STEC·cos z′`，`sin z′ = R/(R+H)·sin z`；⑤ 按 el/az 求 IPP，时间线性 + 空间双线性插 GIM；el>30°、每 5 min 取样。

```python
# level_vs_gim.py — 用法: python level_vs_gim.py <站输出目录> <CODE IONEX> <STA>
# 输入列须为: datetime, el, az, tec.l1l2, tec.p1p2（前 5 列）
import sys, glob, numpy as np, datetime as dt
d, inx, sta = sys.argv[1], sys.argv[2], sys.argv[3].upper()
L = open(inx).read().splitlines(); maps, ep, dcb, sd = [], [], {}, {}
for i, s in enumerate(L):
    lab = s[60:].strip()
    if lab == 'PRN / BIAS / RMS': dcb[s[3:6]] = float(s[6:16])
    elif lab == 'STATION / BIAS / RMS' and s[3] == 'G': sd[s[6:10]] = float(s[26:36])
    elif lab == 'START OF TEC MAP':
        ep.append(dt.datetime(*map(int, L[i+1][:36].split()))); g, j = [], i + 2
        while len(g) < 71:
            v = ''.join(L[j+1:j+6]); g.append([int(v[k:k+5]) * 0.1 for k in range(0, 365, 5)]); j += 6
        maps.append(np.array(g))
    elif lab == 'START OF RMS MAP': break
M = np.array(maps)                                    # [25, 71(87.5..-87.5), 73(-180..180)]
def gim(t, la, lo):
    x = (t - ep[0]).total_seconds() / 3600; k = min(int(x), 23); w = x - k
    fi, fj = (87.5 - la) / 2.5, ((lo + 180) % 360) / 5; i0, j0 = int(fi), int(fj); a, b = fi - i0, fj - j0
    g = (1 - w) * M[k] + w * M[k + 1]
    return (1-a)*(1-b)*g[i0, j0] + (1-a)*b*g[i0, j0+1] + a*(1-b)*g[i0+1, j0] + a*b*g[i0+1, j0+1]
K, RE, H, out = 2.854, 6371.0, 450.0, []            # K: TECU/ns
for f in sorted(glob.glob(d + '/*_G*.dat')):
    hdr = [l for l in open(f) if l.startswith('# Position (L, B, H)')][0]
    lon0, lat0 = [np.radians(float(v)) for v in hdr.split(':')[1].split(',')[:2]]
    prn = 'G' + f.split('_')[-3][1:]
    a = np.genfromtxt(f, comments='#', dtype=None, encoding='utf-8', usecols=range(5))
    t = np.array([dt.datetime.fromisoformat(x) for x in a['f0']]); el, az, Lt, Pt = a['f1'], a['f2'], a['f3'], a['f4']
    sec = np.array([(x - t[0]).total_seconds() for x in t])
    br = np.r_[0, np.where((np.diff(sec) > 35) | (abs(np.diff(Lt)) > 1))[0] + 1, len(t)]
    for s0, s1 in zip(br[:-1], br[1:]):
        m = slice(s0, s1); ok = el[m] > 10
        if ok.sum() < 40: continue
        w = np.sin(np.radians(el[m][ok])) ** 2
        stec = Lt[m] + np.sum(w * (Pt[m][ok] - Lt[m][ok])) / w.sum() + K * (dcb[prn] + sd[sta])   # 整平 + 扣 DCB
        z = np.radians(90 - el[m]); zp = np.arcsin(RE / (RE + H) * np.sin(z)); vtec = stec * np.cos(zp)
        psi, A = z - zp, np.radians(az[m])
        la = np.arcsin(np.sin(lat0) * np.cos(psi) + np.cos(lat0) * np.sin(psi) * np.cos(A))
        lo = lon0 + np.arcsin(np.sin(psi) * np.sin(A) / np.cos(la))
        for k in np.where(el[m] > 30)[0][::10]:
            out.append((vtec[k], gim(t[m][k], np.degrees(la[k]), np.degrees(lo[k]))))
r = np.array(out); dv = r[:, 0] - r[:, 1]
print(f'{sta}: DCB_rcv={sd[sta]} ns  n={len(r)}  VTEC={r[:,0].mean():.2f}  GIM={r[:,1].mean():.2f}  '
      f'diff mean={dv.mean():.2f} std={dv.std():.2f} RMS={np.sqrt((dv**2).mean()):.2f} TECU')
```

```bash
pip install numpy
python level_vs_gim.py tec/2024/235/wtza COD0OPSFIN_20242350000_01D_01H_GIM.INX wtza
python level_vs_gim.py tec/2024/235/mas1 COD0OPSFIN_20242350000_01D_01H_GIM.INX mas1   # MAS1 见 §5
```

```text
WTZA: DCB_rcv=-5.21 ns  n=1481  VTEC=25.56  GIM=25.27  diff mean=0.30 std=2.05 RMS=2.07 TECU
MAS1: DCB_rcv=7.451 ns  n=1564  VTEC=44.90  GIM=45.11  diff mean=-0.21 std=3.58 RMS=3.59 TECU
```

同一脚本把 `K` 设成 0（不扣 DCB）时 WTZA 变成 `VTEC=38.12 GIM=25.27 差 mean=12.85 std=11.21 RMS=17.05`——**DCB 不扣，偏 13 TECU 且按卫星乱跳**。剩下 2–3.6 TECU 的离散来自：码噪声/多路径进整平常数、单层映射函数与 CODE 的修正 MSLM 不同、GIM 本身 2.5°×5°/1 h 平滑、以及未做日固系旋转插值。

## 5. 端到端 C：RINEX 3.04 多系统（MAS1）与 58 站批量

```bash
B=https://igs.bkg.bund.de/root_ftp/IGS/obs/2024/235
# 文件名改小写：输出目录/站名取文件名前 4 字符（坑 7）
curl -sf $B/MAS100ESP_R_20242350000_01D_30S_MO.crx.gz -o obs/mas100esp_r_20242350000_01d_30s_mo.crx.gz
curl -sfO --output-dir nav https://igs.bkg.bund.de/root_ftp/IGS/BRDC/2024/235/brdc2350.24g.gz   # GLONASS 频点号必需
```

未打补丁 1 时：`- reading...[ERROR] unknown rinex version: 3.04 (obs/MAS100ESP_R_...crx.gz)`，该站整站跳过。打补丁后 MAS1（GPS+GLO 导航）输出 G 32 / R 26 个文件（与 WTZA 同跑共 `Total processing time:  0.199 min.`）。只放 `brdc*.24n/g` 时会提示 `Can't find any navigation file for the 'E'/'C'/'S'`，这几个系统没有文件。

批量：BKG 同日 19 个 RINEX 2（`*.24d.gz`）+ 39 个 RINEX 3.04（`*_30S_MO.crx.gz`），挑的都是 mosgim2 内置站名表里的站、全球分布。`recFields = 'datetime, sat.x, sat.y, sat.z, tec.l1l2'`（mosgim2 要求的格式）。tec-suite 单进程、纯 Python，本机把 58 个文件拆成 7 组各自一个进程/各自 `outDir`，每组 `real 0m59s–1m14s`；合并后 **58 站目录 / 3073 个 `.dat` / 331 MB**。

## 6. 配置参数与输出字段

| 变量 | 本文取值 | 作用 / 注意 |
| --- | --- | --- |
| `obsDir` | `obs` | 可逗号分隔多目录；认 `*.YYo/.YYd(.Z/.gz)` 与长名 `.rnx/.crx(.gz)` |
| `navDir` | `nav` 或 `nav/n, nav/g` | GPS 用 `n`，GLONASS 用 `g`（频点号）；Galileo 需混合导航 `BRDC00IGS_R_..._MN.rnx.gz` |
| `outDir` | `tec` | 输出到 `outDir/YYYY/DDD/<站>/`，日志 `outDir/tecs.log` |
| `recFields` | 见 §3 / §5 | 列与顺序；字段名写错直接退出：`CfgError: Cfg: wrong format value: <tec.l1l2x>` |
| `datetimeFormat` | `%Y-%m-%dT%H:%M:%S` | mosgim2 硬编码这个格式 |
| `samplingInterval` | 30 | 秒；0 = 全读；小于文件间隔时写 “(not used)” |
| `navPriorityGPS/GLO/GEO` | `brdc, auto` | 按 4 字符站名找导航文件的优先顺序 |
| `navIgnoreAbsence` | False | True 时缺导航也出 TEC，但 el/az 写 0（GLONASS 仍必须有） |
| `logLevel` | WARNING | 控制台只打 WARNING 以上；DEBUG 写日志文件 |

| 输出列 | 含义 | 单位 |
| --- | --- | --- |
| `datetime` / `tsn` / `hour` | 历元字符串 / 当日秒÷间隔 / 小时小数 | — |
| `el`, `az` | 高度角、方位角（需导航） | ° |
| `sat.x/y/z`，`site.x/y/z`，`site.l/b/h` | 卫星/测站 ECEF、测站经纬高 | m / °（经度 0–360） |
| `tec.l1l2`（`l1l5`,`l2l5`,`l2l6`,`l2l7`,`l6l7`） | 相位 STEC + 任意常数 | TECU |
| `tec.p1p2`（`c1p2`,`c1c2`,`c1c5`,`c2c5`,`c2c6`,`c2c7`,`c6c7`） | 码 STEC（含 DCB） | TECU |
| `tec.l1c1`, `tec.l2c2` | 单频相位−码（含 2×电离层+模糊度） | TECU |
| `validity` | 位掩码：该历元缺了头里声明的哪些观测（0 = 全齐；LLI1=1、LLI2=2、C1=4、L1=8、L2=16、P1=32、P2=64…） | int |
| 文件头 `# Position (X, Y, Z)` | 测站坐标（取自 RINEX 头） | m，mosgim2 从这里读站位 |

缺观测的组合写 **`0.000`**（不是 NaN）；下游要把 0 当缺测。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 一条修复命令 |
| --- | --- | --- | --- |
| 1 | `FileNotFoundError: [Errno 2] No such file or directory: ''` | `-c tecs.cfg` 相对路径，程序 `os.chdir(dirname(cfg))` 得到空串 | `python tecs.py -c $PWD/tecs.cfg` |
| 2 | `[ERROR] unknown rinex version: 3.04`，整站无输出 | 观测类只登记到 3.03 | §2 补丁 1（`sed … tecs/rinex/__init__.py`） |
| 3 | RINEX 3 站点 GPS G02/G13/G16/G19/G20/G21/G22 的 `tec.l1l2` 全天 0（MIZU 58 个文件中 11 个全零） | 头里同时有 `L2L L2W`，按字母序永远取 `L2L`；Block IIR 没有 L2C → 空值 | §2 补丁 2；打补丁后 MIZU 全零文件 11→4 |
| 4 | 补丁后仍有 R06/R10/R13/R23 全零（58 站共 174 个文件） | 这几颗 GLONASS 当日无 G2 观测（MIZU 07:06 历元 R06/R23 只有 C1C/C1P/D1），不是 bug | 不修；下游按 `tec != 0` 过滤：`awk '!/^#/ && $5!=0' f.dat` |
| 5 | `crx2rnx … [Errno 2] No such file or directory: 'crx2rnx'` | 读 `.crx`/`.YYd` 靠外部 `crx2rnx -` | `pip install hatanaka`（或编 GSI RNXCMP）后 `which crx2rnx` |
| 6 | Galileo 文件 `tec.l1l2` 全是 0.000 | E 星没有 L2 频点 | `recFields` 加 `tec.l1l5`，并放混合导航：`curl -sfO --output-dir nav/m …/BRDC00IGS_R_20242350000_01D_MN.rnx.gz` |
| 7 | RINEX 3 输出目录叫 `MAS1`，下游按小写站名匹配不上 | 站名 = 文件名前 4 字符原样 | 下载时改小写：`for f in obs/*; do mv "$f" "$(echo $f \| tr A-Z a-z)"; done` |
| 8 | 加了混合导航后 `No such label: C5P` 刷屏（MAS1 日志 31763 行）、北斗无输出 | 标签表没有 BDS-3 新码 | 不需要北斗时 `logLevel = ERROR`；需要则换工具（[pytecgg](./pytecgg.md)） |
| 9 | 批量跑一半 `OSError: [Errno 28] No space left on device` 崩溃 | 每站 ~6 MB 文本，58 站 331 MB；异常直接退出整组 | `df -h .` 先确认；把失败组剩余文件放新目录重跑 |
| 10 | 自己扣 DCB 后 MAS1 仍偏 −8.6 TECU | IONEX 里同一站有 G 与 E 两行 `STATION / BIAS / RMS`，后者覆盖 | 只取 `s[3]=='G'` 那行（§4 脚本已处理） |
| 11 | 用 GIM 插值得到负 VTEC | tec-suite 经度 0–360°，GIM 网格 −180…180 | `lon = (lon + 180) % 360 - 180` |

## 8. 怎么读结果、接到哪步

- 单星一条弧：`tec.l1l2` 曲线形状可信、绝对值不可信；出现 >1 TECU 的台阶多半是周跳，切弧。
- 要绝对 STEC：整平到 `tec.p1p2`，再加 `2.854×(DCB_sat+DCB_rcv)`（ns，取自 CODE IONEX 头或 Bias-SINEX）；要 VTEC 再乘 cos z′。§4 显示做完三步后与 CODE GIM 的均值偏差 ≤0.3 TECU。
- 要全球图：原样把 `datetime, sat.x, sat.y, sat.z, tec.l1l2` 交给 [mosgim2](./mosgim2.md)，它只用相位差、不需要 DCB。
- 读 GIM 做对照：[ionex](./ionex.md) / [ionex-gim](./ionex-gim.md)；两幅图并排：[diffionmap](./diffionmap.md)。
- 更完整的一站式单站校准（含 DCB、VTEC、多系统）：[pytecgg](./pytecgg.md)；只要粗相对 TEC：[gnss-tec](./gnss-tec.md)。
- 原理：教程 [02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md)、[09 DCB](../tutorials/09-dcb-biases-deep.md)、[16 一日 TEC 实践](../tutorials/16-practice-one-day-tec.md)。

## 9. 许可与诚实局限

- GPL-3.0-or-later：修改后再分发须开源同协议；本文两处 `sed` 补丁只在本地。
- 上游 2020-11 以后无提交；RINEX 3.04/3.05、BDS-3 新码、RINEX 4 均未登记。补丁 1 只是“按 3.03 解析”，本机 39 个 3.04 站未见解析错误，但未逐字段审计。
- 不做周跳探测/修复、整平、DCB、VTEC、IPP——全部在下游。GLONASS 需要导航文件取频点号。
- 纯 Python 单进程；本机 30 s 采样单站全日：WTZA（GPS-only）0.071 min；58 站 7 进程并行每组 8–9 站约 1–1.2 min。
- §4 的 VTEC 对比只有 2 站 1 天，且用的是本文自写的简化映射与插值，不代表 tec-suite 精度指标。
