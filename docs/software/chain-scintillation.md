# CHAIN（加拿大高纬电离层网）GISTM 闪烁/TEC 数据：ISMR 文件匿名下载与 S4、σφ 提取

入口：[CHAIN 首页](http://chain.physics.unb.ca/chain/) · [Data Download 说明](http://chain.physics.unb.ca/chain/pages/data_download) · [数据树（新）](https://www.chain-project.net/data/gps/ismr/) · [站表](http://chain.physics.unb.ca/chain/pages/stations/) · [数据政策](http://chain.physics.unb.ca/chain/pages/rules) · [Septentrio PolaRx5S User Manual（含 sbf2ismr 列定义）](https://ftp.space.dtu.dk/pub/bm/Septentrio/polarx5s_User_Manual_1%200%202%20(1).pdf) · 本机验证 **2026-09-26 04:48–05:00 EDT**

> 岗位：不注册，从 CHAIN 的公开数据树按小时拉 **ISMR**（Septentrio PolaRxS 的 `sbf2ismr` 输出，每星每分钟一行、62 列），按官方列定义读出 S4、σφ（Phi01/03/10/30/60）、锁定时间、C/N0、TEC，做仰角 + 锁定时间过滤，并用 Churchill（chuc）在 2024-05-10/11 磁暴与 05-08/09 平静夜对比，量化高纬相位闪烁。低纬 ISMR（UNESP，需账号）见 [ismr-downloader](./ismr-downloader.md)；闪烁仿真见 [iono-scintillation](./iono-scintillation.md)；接收机 RINEX 算 ROTI 见 [oasis-roti](./oasis-roti.md)；同一磁暴的卫星/测高仪视角见 [swarm-data](./swarm-data.md)、[giro-ionosonde](./giro-ionosonde.md)；Kp 见 [space-weather-indices](./space-weather-indices.md)。本文不重复这几篇。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E26](../data-access.md#dp-e26)
>
> 冲突时：列定义以 Septentrio 手册 sbf2ismr 一节为准（文件本身不带表头）；站点/仪器以 CHAIN 站表为准；本文的仰角、锁定时间、σφ/S4 分级阈值都标为“本文阈值”。

## 1. 它解决什么，边界在哪

| 能做 | 怎么做 | 边界 |
|---|---|---|
| 匿名下载 ISMR（1 min 闪烁指数 + TEC） | HTTPS 目录 `https://www.chain-project.net/data/gps/ismr/YYYY/DDD/HH/`；或匿名 FTP `ftp.chain-project.net`（用户 `ftp`，密码填邮箱） | 老地址 `chain.physics.unb.ca/data/gps/ismr/` 目录已空（2024 → 404）；FTP 时好时坏 |
| 站点、坐标、仪器型号 | 站表页（25 台 GISTM：15 台 PolaRxS/PolaRx5S + 10 台 NovAtel GSV4004B） | 2024 年的小时目录里只有 15 个 PolaRxS 站；GSV4004B 的 ISMR 只在 `nvismr/` 按站按年打包，最晚到 2019 |
| S4 / σφ / TEC / 锁定时间 | 按 62 列官方定义读（本文 3.3） | 文件无表头；列序依接收机/`sbf2ismr` 版本 |
| 50 Hz 原始相位/幅度 | 只在接收机二进制文件 `gps/data/raw/SSSS` | 本文不涉及 |
| RINEX 30 s / 1 s | `gps/data/daily/YYYY/DDD/YYo`（或 `YYd`）、`gps/data/highrate/` | 见 CHAIN 说明页 |
| 数据政策 | 开放科研使用；发表须引用 Jayachandran et al. (2009, Radio Sci. 44, RS0A03) 并告知 CHAIN | 高阶产品（同化 TEC 图）另有协议 |

**CHAIN 可用，所以没有切换到其他源**；用户列的备选（ISMR Query Tool、eSWua、LISN 等）本文未用。

## 2. 安装

只要 `curl`、`gzip` 和 Python 3 + numpy（本机 `/usr/bin/python3`，numpy 2.2.4）。读官方列定义需要 `pdftotext`（poppler-utils）。

## 3. 真实命令与输出

### 3.1 访问路径（`access.sh`，原样）

```bash
#!/usr/bin/env bash
# CHAIN 访问路径：HTTPS 目录（新）、旧 UNB 路径、匿名 FTP（用户名 ftp，密码填邮箱）
set -u
curl -s -o /dev/null -w 'HTTPS 新站   %{http_code}  https://www.chain-project.net/data/gps/ismr/2024/132/04/\n' https://www.chain-project.net/data/gps/ismr/2024/132/04/
curl -s -o /dev/null -w 'HTTP 旧域名  %{http_code} -> %{redirect_url}\n' http://www.chain-project.net/data/gps/ismr/
curl -s -o /dev/null -w 'UNB 老路径   %{http_code}  http://chain.physics.unb.ca/data/gps/ismr/2024/\n' http://chain.physics.unb.ca/data/gps/ismr/2024/
echo 'FTP 匿名列目录（前 5 行）：'; curl -s -m 90 --user 'ftp:your.name@example.org' ftp://ftp.chain-project.net/gps/ismr/2024/132/04/ | head -5
```

输出（原样；04:54 EDT 这一次 FTP 90 s 超时，什么也没列出来）：

```text
HTTPS 新站   200  https://www.chain-project.net/data/gps/ismr/2024/132/04/
HTTP 旧域名  301 -> https://chain-new.chain-project.net/data/gps/ismr/
UNB 老路径   404  http://chain.physics.unb.ca/data/gps/ismr/2024/
FTP 匿名列目录（前 5 行）：
```

两分钟前（04:52 EDT）同一 FTP 命令成功列出了目录（原样摘录前 5 行）：

```text
-r--r--r--    1 ftp      ftp         60481 May 11  2024 arcc24132e.ismr.gz
-r--r--r--    1 ftp      ftp         59878 May 11  2024 arvc24132e.ismr.gz
-r--r--r--    1 ftp      ftp         66579 May 11  2024 chuc24132e.ismr.gz
-r--r--r--    1 ftp      ftp        102396 May 12  2024 dawc24132e.ismr.gz
-r--r--r--    1 ftp      ftp         59842 May 11  2024 edmc24132e.ismr.gz
```

结论：**不需要登录**。说明页原文：“All CHAIN data is available via anonymous FTP or via Open Access Web requests … No username or password is required”（旧账号 2022-02 起停用）。脚本用 HTTPS 目录更稳；页面上写的 `http://www.chain-project.net/data` 会 301 到 `https://chain-new.chain-project.net/data/`，`https://www.chain-project.net/data/` 直接 200。

### 3.2 下载与文件结构（`fetch.sh`，原样）

```bash
#!/usr/bin/env bash
# CHAIN ISMR：匿名 HTTPS，按小时文件 <站3字母>c<YY><DDD><时字母a-x>.ismr.gz
# Churchill（chuc）：磁暴 2024-05-10 16 UT .. 05-11 07 UT（16 个小时文件）+ 平静日 2024-05-08 同一时段
set -u
B=https://www.chain-project.net/data/gps/ismr
H=(a b c d e f g h i j k l m n o p q r s t u v w x)
get() {  # $1=DOY $2=hour
  local f=chuc24$1${H[$2]}.ismr.gz
  curl -s -o $f -w "%{http_code} %{size_download} B  $1/$(printf %02d $2)/$f\n" "$B/2024/$1/$(printf %02d $2)/$f"
}
for h in $(seq 16 23); do get 131 $h; get 129 $h; done      # 05-10 与 05-08 的 16–23 UT
for h in $(seq 0 7);   do get 132 $h; get 130 $h; done      # 05-11 与 05-09 的 00–07 UT
echo "--- 合计 $(ls chuc*.gz | wc -l) 个，$(cat chuc*.gz | wc -c) B"
echo "--- 首行（原样）"; zcat chuc24131q.ismr.gz | head -1
echo "--- 每行列数分布"; zcat chuc*.gz | awk -F, '{print NF}' | sort | uniq -c
echo "--- 旧 UNB 路径与目录"
curl -s -o /dev/null -w '%{http_code}  http://chain.physics.unb.ca/data/gps/ismr/2024/\n' http://chain.physics.unb.ca/data/gps/ismr/2024/
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' http://www.chain-project.net/data/gps/ismr/
curl -s -o /dev/null -w 'https 老站 %{http_code}\n' -m 20 https://chain.physics.unb.ca/
curl -s $B/2024/132/04/ | grep -o '[a-z]\{4\}24132e.ismr.gz' | sort -u | tr '\n' ' '; echo
```

输出（原样；32 个小时文件共 1.97 MB，用完即删）：

```text
200 59417 B  131/16/chuc24131q.ismr.gz
200 58223 B  129/16/chuc24129q.ismr.gz
200 58632 B  131/17/chuc24131r.ismr.gz
200 54407 B  129/17/chuc24129r.ismr.gz
200 66835 B  131/18/chuc24131s.ismr.gz
200 55875 B  129/18/chuc24129s.ismr.gz
200 80478 B  131/19/chuc24131t.ismr.gz
200 70908 B  129/19/chuc24129t.ismr.gz
200 64098 B  131/20/chuc24131u.ismr.gz
200 57337 B  129/20/chuc24129u.ismr.gz
200 58534 B  131/21/chuc24131v.ismr.gz
200 50569 B  129/21/chuc24129v.ismr.gz
200 68778 B  131/22/chuc24131w.ismr.gz
200 60848 B  129/22/chuc24129w.ismr.gz
200 70101 B  131/23/chuc24131x.ismr.gz
200 61174 B  129/23/chuc24129x.ismr.gz
200 62255 B  132/00/chuc24132a.ismr.gz
200 55700 B  130/00/chuc24130a.ismr.gz
200 61262 B  132/01/chuc24132b.ismr.gz
200 57476 B  130/01/chuc24130b.ismr.gz
200 56605 B  132/02/chuc24132c.ismr.gz
200 56943 B  130/02/chuc24130c.ismr.gz
200 56552 B  132/03/chuc24132d.ismr.gz
200 52691 B  130/03/chuc24130d.ismr.gz
200 66579 B  132/04/chuc24132e.ismr.gz
200 65171 B  130/04/chuc24130e.ismr.gz
200 62518 B  132/05/chuc24132f.ismr.gz
200 59152 B  130/05/chuc24130f.ismr.gz
200 63157 B  132/06/chuc24132g.ismr.gz
200 59732 B  130/06/chuc24130g.ismr.gz
200 70336 B  132/07/chuc24132h.ismr.gz
200 63485 B  130/07/chuc24130h.ismr.gz
--- 合计 32 个，1965828 B
--- 首行（原样）
2313,489660,  2,       628, 48, 21,43.7, 0.106, 0.065, 0.022, 0.026, 0.030, 0.031, 0.031, -0.061, 0.213, 48.988, 0.072, 47.626, 0.078, 54.204, 0.074, 57.146, 0.127,13709,510,13700,30.2, 0.032, 2.908, 1.57, nan,   nan,   nan,   nan,   nan,   nan,   nan,   nan,    nan,   nan,  nan,   nan,   nan,  nan, nan,   nan,   nan,   nan,   nan,   nan,   nan,   nan,    nan,   nan,  nan,   nan,   nan,  nan,0.000063,     nan,     nan
--- 每行列数分布
  17791 62
--- 旧 UNB 路径与目录
404  http://chain.physics.unb.ca/data/gps/ismr/2024/
301 -> https://chain-new.chain-project.net/data/gps/ismr/
https 老站 000
arcc24132e.ismr.gz arvc24132e.ismr.gz chuc24132e.ismr.gz dawc24132e.ismr.gz edmc24132e.ismr.gz eurc24132e.ismr.gz fsic24132e.ismr.gz fsmc24132e.ismr.gz gjoc24132e.ismr.gz kugc24132e.ismr.gz mcmc24132e.ismr.gz rabc24132e.ismr.gz ranc24132e.ismr.gz repc24132e.ismr.gz sacc24132e.ismr.gz 
```

文件名：`<站 3 字母>c<YY><DDD><小时字母>.ismr.gz`，小时字母 `a`=00 UT … `x`=23 UT，放在 `YYYY/DDD/HH/` 下。每行 = 一颗卫星一分钟，逗号分隔，62 列，`nan` = 不适用/未知。

### 3.3 62 列官方定义 × 真实一行（`cols.sh`，原样）

```bash
#!/usr/bin/env bash
# 官方列定义（Septentrio PolaRx5S User Manual 1.0.2，sbf2ismr 一节）× CHAIN 真实文件一行（chuc 2024-05-10 23:25 UTC 的 G18）
set -u
curl -s -o sx.pdf -w 'manual HTTP %{http_code} %{size_download} B\n' "https://ftp.space.dtu.dk/pub/bm/Septentrio/polarx5s_User_Manual_1%200%202%20(1).pdf"
pdftotext -layout sx.pdf sx.txt && rm -f sx.pdf
grep -E '^Col [0-9]+:' sx.txt | head -62 > cols.txt; rm -f sx.txt
echo "官方列数 $(wc -l < cols.txt)"
zcat chuc24131x.ismr.gz | awk -F, '$3+0==18' | sort -t, -k14,14gr | head -1 > row.txt   # G18 在该小时 Phi60 最大的一行
python3 - <<'PY'
import re
names = [re.sub(r'^Col \d+:\s*', '', l.strip()) for l in open('cols.txt')]
vals = [v.strip() for v in open('row.txt').read().strip().split(',')]
print('真实行列数', len(vals))
for i, (n, v) in enumerate(zip(names, vals), 1):
    print(f'{i:2d} | {v:>9s} | {n[:95]}')
PY
rm -f cols.txt row.txt
```

输出（原样；左列列号，中间是 CHAIN 真实文件里 G18 在 2024-05-10 23:25 UTC 那一行的值，右列是手册原文）：

```text
manual HTTP 200 10799085 B
官方列数 62
真实行列数 62
 1 |      2313 | WN, GPS Week Number
 2 |    516360 | TOW, GPS Time of Week (seconds)
 3 |        18 | SVID (see numbering convention in the ’SBF Outline’ section of the Reference Guide)
 4 |       628 | Value of the RxState field of the ReceiverStatus SBF block
 5 |       248 | Azimuth (degrees)
 6 |        77 | Elevation (degrees)
 7 |      49.4 | Average Sig1 C/N0 over the last minute (dB-Hz)
 8 |     0.412 | Total S4 on Sig1 (dimensionless)
 9 |     0.034 | Correction to total S4 on Sig1 (thermal noise component only) (dimensionless)
10 |     1.178 | Phi01 on Sig1, 1-second phase sigma (radians)
11 |     1.854 | Phi03 on Sig1, 3-second phase sigma (radians)
12 |     2.878 | Phi10 on Sig1, 10-second phase sigma (radians)
13 |     2.959 | Phi30 on Sig1, 30-second phase sigma (radians)
14 |     3.136 | Phi60 on Sig1, 60-second phase sigma (radians)
15 |   -15.131 | AvgCCD on Sig1, average of code/carrier divergence (meters)
16 |     1.015 | SigmaCCD on Sig1, standard deviation of code/carrier divergence (meters)
17 |    50.965 | TEC at TOW-45s (TECU), taking calibration into account (see -C option)
18 |     1.914 | dTEC from TOW-60s to TOW-45s (TECU)
19 |    59.723 | TEC at TOW-30s (TECU), taking calibration into account (see -C option)
20 |     0.796 | dTEC from TOW-45s to TOW-30s (TECU)
21 |    51.717 | TEC at TOW-15s (TECU), taking calibration into account (see -C option)
22 |    -0.910 | dTEC from TOW-30s to TOW-15s (TECU)
23 |    89.929 | TEC at TOW (TECU), taking calibration into account (see -C option)
24 |   232.211 | dTEC from TOW-15s to TOW (TECU)
25 |      9680 | Sig1 lock time (seconds)
26 |       510 | sbf2ismr version number
27 |         1 | Lock time on the second frequency used for the TEC computation (seconds)
28 |      42.0 | Averaged C/N0 of second frequency used for the TEC computation (dB-Hz)
29 |     0.172 | SI Index on Sig1: (10*log10(Pmax)-10*log10(Pmin))/(10*log10(Pmax)+10*log10(Pmin)) (dimensionles
30 |    16.436 | SI Index on Sig1, numerator only: 10*log10(Pmax)-10*log10(Pmin) (dB)
31 |      2.94 | p on Sig1, spectral slope of detrended phase in the 0.1 to 25Hz range (dimensionless)
32 |      49.3 | Average Sig2 C/N0 over the last minute (dB-Hz)
33 |     0.539 | Total S4 on Sig2 (dimensionless)
34 |     0.034 | Correction to total S4 on Sig2 (thermal noise component only) (dimensionless)
35 |     1.513 | Phi01 on Sig2, 1-second phase sigma (radians)
36 |     2.395 | Phi03 on Sig2, 3-second phase sigma (radians)
37 |     3.681 | Phi10 on Sig2, 10-second phase sigma (radians)
38 |     3.816 | Phi30 on Sig2, 30-second phase sigma (radians)
39 |     4.051 | Phi60 on Sig2, 60-second phase sigma (radians)
40 |   -25.832 | AvgCCD on Sig2, average of code/carrier divergence (meters)
41 |     1.594 | SigmaCCD on Sig2, standard deviation of code/carrier divergence (meters)
42 |      9673 | Sig2 lock time (seconds)
43 |     0.228 | SI Index on Sig2 (dimensionless)
44 |    19.525 | SI Index on Sig2, numerator only (dB)
45 |      2.89 | p on Sig2, phase spectral slope in the 0.1 to 25Hz range (dimensionless)
46 |      54.2 | Average Sig3 C/N0 over the last minute (dB-Hz)
47 |     0.561 | Total S4 on Sig3 (dimensionless)
48 |     0.019 | Correction to total S4 on Sig3 (thermal noise component only) (dimensionless)
49 |     1.579 | Phi01 on Sig3, 1-second phase sigma (radians)
50 |     2.496 | Phi03 on Sig3, 3-second phase sigma (radians)
51 |     3.836 | Phi10 on Sig3, 10-second phase sigma (radians)
52 |     3.973 | Phi30 on Sig3, 30-second phase sigma (radians)
53 |     4.219 | Phi60 on Sig3, 60-second phase sigma (radians)
54 |   -26.625 | AvgCCD on Sig3, average of code/carrier divergence (meters)
55 |     1.724 | SigmaCCD on Sig3, standard deviation of code/carrier divergence (meters)
56 |      9680 | Sig3 lock time (seconds)
57 |     0.231 | SI Index on Sig3 (dimensionless)
58 |    22.194 | SI Index on Sig3, numerator only (dB)
59 |      2.87 | p on Sig3, phase spectral slope in the 0.1 to 25Hz range (dimensionless)
60 |  0.142957 | T on Sig1, phase power spectral density at 1 Hz (rad^2/Hz)
61 |  0.240911 | T on Sig2, phase power spectral density at 1 Hz (rad^2/Hz)
62 |  0.251248 | T on Sig3, phase power spectral density at 1 Hz (rad^2/Hz)
```

对 CHAIN 的 PolaRxS，**Sig1 = GPS L1C/A，Sig2 = L2C，Sig3 = L5**（手册：Sig1 是 GPS/GLONASS/SBAS/QZSS 的 L1CA、Galileo L1BC、北斗 B1；Sig2 是 L2C / E5a / B2；Sig3 是 L5 / E5b / B3）。关键列：

| 列 | 量 | 单位 | 用法 |
|---|---|---|---|
| 1–2 | WN、TOW | 周、秒 | **GPS 时**，UTC = GPS − 18 s；TOW 标的是这一分钟的**结束** |
| 3 | SVID | — | 1–37 = GPS（手册）；本站文件只有 GPS |
| 5–6 | 方位、仰角 | ° | 仰角过滤 |
| 7 | Sig1 C/N0（1 min 平均） | dB-Hz | 弱信号判断 |
| 8–9 | S4 总值、S4 热噪声修正 | — | S4 = √(S4总² − 修正²)，≤0 取 0（手册公式） |
| 10–14 | Phi01、Phi03、Phi10、Phi30、Phi60 | rad | 50 Hz 去趋势相位（6 阶 Butterworth 高通，默认 0.1 Hz）在 1/3/10/30/60 s 窗的标准差（60 s 以内取平均）；σφ 常指 **Phi60** |
| 15–16 | 码–载波发散均值、标准差 | m | 多径/电离层梯度 |
| 17–24 | TEC（TOW−45/−30/−15/0 s）与 dTEC | TECU | TEC 由**伪距**得、含接收机偏差（需 `-C` 校准）；dTEC 由**相位**得，精确但只是 15 s 变化量 |
| 25 | Sig1 锁定时间 | s | 锁定过滤 |
| 27–28 | 第二频率（TEC 用）锁定时间、C/N0 | s、dB-Hz | TEC/dTEC 质量看这两列 |
| 29–31 | SI、SI 分子、相位谱斜率 p | —、dB、— | |
| 32–45 / 46–59 | Sig2 / Sig3 的同组量 | | |
| 60–62 | Sig1/2/3 在 1 Hz 的相位谱强度 T | rad²/Hz | |

NovAtel GSV4004B 的 ISMR（CHAIN `nvismr/`）列更少，前几列排布相似但不能套用本表；本文没下它。

### 3.4 S4 / σφ 提取与磁暴个例（`scint.py`，原样）

```python
# CHAIN Churchill（chuc）ISMR：GPS L1CA，仰角 ≥30°、锁定 ≥240 s（本文阈值），S4 去热噪声，σφ(Phi60) 统计
import glob, gzip, numpy as np, datetime as dt
COL = dict(wn=1, tow=2, sv=3, az=5, el=6, cn0=7, s4=8, s4c=9, p01=10, p03=11, p10=12, p30=13, p60=14,
           tec=23, dtec=24, lock=25, lock2=27, cn02=28)
def load(files):
    rows = []
    for f in sorted(files):
        for ln in gzip.open(f, 'rt'):
            v = [x.strip() for x in ln.split(',')]
            rows.append([float(v[COL[k] - 1]) if v[COL[k] - 1] != 'nan' else np.nan for k in COL])
    a = np.array(rows); d = {k: a[:, i] for i, k in enumerate(COL)}
    gps0 = dt.datetime(1980, 1, 6)
    d['t'] = np.array([gps0 + dt.timedelta(weeks=w, seconds=s - 18) for w, s in zip(d['wn'], d['tow'])])  # GPS→UTC
    x = d['s4'] ** 2 - d['s4c'] ** 2; d['S4'] = np.where(x > 0, np.sqrt(np.clip(x, 0, None)), 0.0)        # 手册公式
    return d
S = load(glob.glob('chuc24131*.gz') + glob.glob('chuc24132*.gz'))   # 05-10 16 UT .. 05-11 08 UT
Q = load(glob.glob('chuc24129*.gz') + glob.glob('chuc24130*.gz'))   # 05-08 16 UT .. 05-09 08 UT
for nm, d in (('磁暴 05-10/11', S), ('平静 05-08/09', Q)):
    sv = d['sv']
    print(f"== {nm}：{len(sv)} 行，{d['t'][0]:%m-%d %H:%M}..{d['t'][-1]:%m-%d %H:%M} UTC；SVID 分布：GPS(1–37) {np.sum(sv<=37)}，"
          f"GLONASS(38–68) {np.sum((sv>=38)&(sv<=68))}，Galileo(71–106) {np.sum((sv>=71)&(sv<=106))}，SBAS(120–140) {np.sum((sv>=120)&(sv<=140))}，其他 {np.sum(sv>140)}")
def sel(d):
    g = d['sv'] <= 37
    m = g & (d['el'] >= 30) & (d['lock'] >= 240) & np.isfinite(d['p60'])
    print(f"   GPS {g.sum()} → 仰角≥30° {np.sum(g & (d['el']>=30))} → 再加锁定≥240 s {m.sum()}；Phi60 为 nan 的 GPS 行 {np.sum(g & np.isnan(d['p60']))}")
    return m
print('== 过滤（本文阈值：GPS L1CA，仰角 ≥ 30°，Sig1 锁定时间 ≥ 240 s）')
mS, mQ = sel(S), sel(Q)
def summ(d, m, nm):
    p, s = d['p60'][m], d['S4'][m]
    print(f"   {nm}: N={m.sum():5d}  Phi60 中位 {np.median(p):.3f} p95 {np.percentile(p,95):.3f} max {p.max():.3f} rad | "
          f">0.25 rad {100*np.mean(p>0.25):5.1f}%  >0.5 rad {100*np.mean(p>0.5):4.1f}% | S4(去噪) 中位 {np.median(s):.3f} p95 {np.percentile(s,95):.3f} max {s.max():.3f}  >0.2 {100*np.mean(s>0.2):.1f}%")
print('== 总体（σφ 阈值 0.25/0.5 rad、S4 0.2 为常用分级，本文采用）')
summ(Q, mQ, '平静'); summ(S, mS, '磁暴')
k = np.argmax(np.where(mS, S['p60'], -1))
print(f"   磁暴最大 Phi60 {S['p60'][k]:.3f} rad @ {S['t'][k]:%m-%d %H:%M} UTC（{(S['t'][k]-dt.timedelta(hours=4)):%m-%d %H:%M} EDT） G{int(S['sv'][k]):02d} "
      f"el {S['el'][k]:.0f}° az {S['az'][k]:.0f}°；同行 Phi01/03/10/30 = {S['p01'][k]:.3f}/{S['p03'][k]:.3f}/{S['p10'][k]:.3f}/{S['p30'][k]:.3f}，S4 {S['S4'][k]:.3f}，锁定 {S['lock'][k]:.0f} s")
r = S['p60'][mS] / S['p01'][mS]; rq = Q['p60'][mQ] / Q['p01'][mQ]
print(f"   Phi60/Phi01 中位：平静 {np.median(rq):.2f}，磁暴 {np.median(r):.2f}（>1 越多说明低频/折射性相位起伏越多）")
print('== 逐小时（UT 起点；每格 = N / Phi60 中位 / Phi60 max / >0.25 rad 占比 / S4 max）')
print('   UT   |            平静 05-08/09              |            磁暴 05-10/11')
for h in list(range(16, 24)) + list(range(0, 8)):
    cells = []
    for d, m in ((Q, mQ), (S, mS)):
        hh = m & np.array([t.hour == h for t in d['t']])
        p = d['p60'][hh]
        cells.append(f"{hh.sum():4d} {np.median(p):.3f} {p.max():.3f} {100*np.mean(p>0.25):5.1f}% {d['S4'][hh].max():.3f}" if hh.any() else '   0')
    print(f"   {h:02d}   | {cells[0]:37s} | {cells[1]}")
# 锁定时间过滤到底去掉了什么（全部 GPS 行）
g = S['sv'] <= 37; short = g & (S['lock'] < 240)
print(f"== 锁定 <240 s 的 GPS 行：{short.sum()}（仰角中位 {np.median(S['el'][short]):.0f}°）；其中 Phi60=nan {np.sum(np.isnan(S['p60'][short]))} 行，"
      f"S4 仍有值 {np.sum(np.isfinite(S['s4'][short]))} 行、S4(去噪) 中位 {np.median(S['S4'][short]):.3f}（保留行 {np.median(S['S4'][mS]):.3f}）")
big = mS & (S['p60'] > 2)
print(f"== Phi60 > 2 rad 的保留行：{big.sum()}，时刻 {sorted(set(f'{t:%H:%M}' for t in S['t'][big]))}")
low = (S['sv'] <= 37) & (S['el'] < 30) & (S['el'] >= 10) & (S['lock'] >= 240)
print(f"== 仰角 10–30° 的 GPS 行：{low.sum()}，Phi60 中位 {np.nanmedian(S['p60'][low]):.3f}、S4 中位 {np.nanmedian(S['S4'][low]):.3f}（多径/低仰角噪声抬高底噪）")
# TEC 列：未校准绝对 TEC（伪距）与 dTEC（相位）；第二频率锁定时间 col 27 也要 ≥240 s（本文阈值）
for nm, d, m in (('平静', Q, mQ), ('磁暴', S, mS)):
    m2 = m & (d['lock2'] >= 240)
    print(f"== {nm} TEC（col 23，未校准）：只按 L1 锁定 N={m.sum()}，dTEC(col 24)|值| p99 {np.nanpercentile(np.abs(d['dtec'][m]),99):.3f}、max {np.nanmax(np.abs(d['dtec'][m])):.1f} TECU；"
          f"再要求 col 27 ≥240 s → N={m2.sum()}，|dTEC| p99 {np.nanpercentile(np.abs(d['dtec'][m2]),99):.3f}、max {np.nanmax(np.abs(d['dtec'][m2])):.2f}；TEC p5/中位/p95 {np.nanpercentile(d['tec'][m2],5):.1f}/{np.nanmedian(d['tec'][m2]):.1f}/{np.nanpercentile(d['tec'][m2],95):.1f} TECU")
k = mS & (S['sv'] == 18) & (S['p60'] > 3)
print("== L2/L1 相位比：该行 Phi01 L1 → 应乘 f1/f2 = 1.283 得 L2（见 cols.out col 35）", np.round(S['p01'][k] * 1575.42 / 1227.60, 3))
```

输出（原样）：

```text
== 磁暴 05-10/11：8905 行，05-10 16:00..05-11 07:59 UTC；SVID 分布：GPS(1–37) 8905，GLONASS(38–68) 0，Galileo(71–106) 0，SBAS(120–140) 0，其他 0
== 平静 05-08/09：8886 行，05-08 16:00..05-09 07:59 UTC；SVID 分布：GPS(1–37) 8886，GLONASS(38–68) 0，Galileo(71–106) 0，SBAS(120–140) 0，其他 0
== 过滤（本文阈值：GPS L1CA，仰角 ≥ 30°，Sig1 锁定时间 ≥ 240 s）
   GPS 8905 → 仰角≥30° 4696 → 再加锁定≥240 s 4692；Phi60 为 nan 的 GPS 行 167
   GPS 8886 → 仰角≥30° 4692 → 再加锁定≥240 s 4692；Phi60 为 nan 的 GPS 行 164
== 总体（σφ 阈值 0.25/0.5 rad、S4 0.2 为常用分级，本文采用）
   平静: N= 4692  Phi60 中位 0.028 p95 0.048 max 0.215 rad | >0.25 rad   0.0%  >0.5 rad  0.0% | S4(去噪) 中位 0.052 p95 0.105 max 0.219  >0.2 0.1%
   磁暴: N= 4692  Phi60 中位 0.074 p95 0.441 max 3.136 rad | >0.25 rad  13.8%  >0.5 rad  3.7% | S4(去噪) 中位 0.063 p95 0.142 max 0.411  >0.2 1.2%
   磁暴最大 Phi60 3.136 rad @ 05-10 23:25 UTC（05-10 19:25 EDT） G18 el 77° az 248°；同行 Phi01/03/10/30 = 1.178/1.854/2.878/2.959，S4 0.411，锁定 9680 s
   Phi60/Phi01 中位：平静 1.54，磁暴 2.28（>1 越多说明低频/折射性相位起伏越多）
== 逐小时（UT 起点；每格 = N / Phi60 中位 / Phi60 max / >0.25 rad 占比 / S4 max）
   UT   |            平静 05-08/09              |            磁暴 05-10/11
   16   |  341 0.030 0.045   0.0% 0.168         |  348 0.030 0.045   0.0% 0.191
   17   |  308 0.026 0.047   0.0% 0.156         |  299 0.032 1.646  19.7% 0.275
   18   |  295 0.026 0.071   0.0% 0.147         |  296 0.215 2.502  37.8% 0.378
   19   |  322 0.027 0.082   0.0% 0.184         |  329 0.219 0.875  38.9% 0.258
   20   |  284 0.025 0.051   0.0% 0.174         |  269 0.168 0.730  27.5% 0.206
   21   |  228 0.026 0.049   0.0% 0.155         |  230 0.104 0.455   4.8% 0.171
   22   |  307 0.028 0.052   0.0% 0.217         |  313 0.065 0.271   0.6% 0.197
   23   |  291 0.028 0.050   0.0% 0.219         |  286 0.240 3.136  48.6% 0.411
   00   |  309 0.027 0.075   0.0% 0.155         |  312 0.082 0.430   6.7% 0.158
   01   |  297 0.029 0.081   0.0% 0.161         |  287 0.035 0.065   0.0% 0.137
   02   |  261 0.028 0.083   0.0% 0.124         |  269 0.056 0.177   0.0% 0.132
   03   |  280 0.036 0.215   0.0% 0.136         |  280 0.046 0.188   0.0% 0.138
   04   |  300 0.034 0.117   0.0% 0.166         |  300 0.064 0.380   2.7% 0.185
   05   |  302 0.036 0.161   0.0% 0.162         |  302 0.103 0.774   7.6% 0.142
   06   |  264 0.029 0.103   0.0% 0.145         |  263 0.066 0.837   4.9% 0.144
   07   |  303 0.027 0.120   0.0% 0.209         |  309 0.106 1.324  18.1% 0.192
== 锁定 <240 s 的 GPS 行：165（仰角中位 11°）；其中 Phi60=nan 165 行，S4 仍有值 165 行、S4(去噪) 中位 0.181（保留行 0.063）
== Phi60 > 2 rad 的保留行：3，时刻 ['18:37', '18:38', '23:25']
== 仰角 10–30° 的 GPS 行：4048，Phi60 中位 0.096、S4 中位 0.147（多径/低仰角噪声抬高底噪）
== 平静 TEC（col 23，未校准）：只按 L1 锁定 N=4692，dTEC(col 24)|值| p99 0.225、max 1.2 TECU；再要求 col 27 ≥240 s → N=4692，|dTEC| p99 0.225、max 1.23；TEC p5/中位/p95 18.0/35.6/52.1 TECU
== 磁暴 TEC（col 23，未校准）：只按 L1 锁定 N=4692，dTEC(col 24)|值| p99 2.291、max 232.2 TECU；再要求 col 27 ≥240 s → N=4682，|dTEC| p99 2.219、max 3.61；TEC p5/中位/p95 10.0/20.5/60.4 TECU
== L2/L1 相位比：该行 Phi01 L1 → 应乘 f1/f2 = 1.283 得 L2（见 cols.out col 35） [1.512]
```

读法：
- **站点**：Churchill（chuc，58.76°N、265.91°E，PolaRxS），极光带；对照是同一 UT 时段的 05-08/09（Kp 最大 2.0 / 2.3），磁暴是 05-10/11（05-10 Kp 8.7，SSC 约 17:05 UT）。
- **过滤（本文阈值）**：GPS L1C/A，仰角 ≥ 30°，Sig1 锁定 ≥ 240 s；两晚过滤后都是 4692 条，样本量相当。
- **闪烁清楚可见，而且以相位闪烁为主**：平静夜 Phi60 中位 0.028 rad、p95 0.048、最大 0.215，**没有一条 > 0.25 rad**；磁暴夜中位 0.074、p95 0.441，**13.8% > 0.25 rad、3.7% > 0.5 rad**，最大 3.136 rad（05-10 23:25 UTC = 19:25 EDT，G18，仰角 77°）。S4（去噪）只从 p95 0.105 升到 0.142，> 0.2 的只有 1.2%。高纬以相位闪烁为主、幅度闪烁弱，符合常识。
- **时间演变**：16 UT 与平静一样；**17 UT 起突然出现**（19.7% > 0.25 rad，与 SSC 对上），18–20 UT 与 23 UT 最强（28–49%），01–03 UT 平息，04–07 UT 再起（每小时 3–18%）。
- **Phi60/Phi01** 中位从 1.54 升到 2.28：长窗更大，磁暴时相位起伏有很大部分在 0.1–1 Hz 低频段。高纬 σφ 常被折射性（TEC 梯度）起伏抬高，不全是衍射性闪烁。
- **锁定时间**：这批文件里锁定 < 240 s 的 165 行 **Phi 已经是 nan**（sbf2ismr 不给），但 **S4 照样有值**，且中位 0.181，远高于保留行的 0.063。锁定过滤对 σφ 看似“没作用”，对 S4 是必须的。
- **仰角**：10–30° 的行 Phi60 中位 0.096、S4 中位 0.147，底噪明显抬高。
- **TEC**：G18 那一行第二频率锁定只有 1 s，dTEC = 232 TECU，是假值；要求 col 27 ≥ 240 s 后 |dTEC| 最大从 232 降到 3.61。同站同时段未校准 TEC 中位从 35.6 降到 20.5 TECU（−42%）：接收机偏差两晚相同，相对变化可参考，是负相磁暴迹象，与 [swarm-data](./swarm-data.md) 的 Ne 下降方向一致。
- **L2/L1 自洽**：Phi01 L1 1.178 × f1/f2（1.283）= 1.512，文件里 L2 是 1.513。相位起伏与频率成反比，说明列没读错。

## 4. 目录与文件名

```text
https://www.chain-project.net/data/
├── gps/ismr/YYYY/DDD/HH/<sss>c<YY><DDD><h>.ismr.gz          PolaRxS ISMR，按小时（本文）
├── gps/ismr/nvismr/<sss>c-YYYY-ismr.zip 与同名目录            GSV4004B 老 ISMR，按站按年（到 2019）
├── gps/data/daily/YYYY/DDD/YYo 或 YYd/                        30 s RINEX 2.11
├── gps/data/highrate/YYYY/DDD/                                1 s RINEX
├── gps/data/raw/SSSS/                                         接收机二进制（含 50 Hz）
└── cadi/ST/                                                   CADI 测高仪 md1/md2
```

## 5. 参数（本文阈值）

| 参数 | 值 | 依据 |
|---|---|---|
| 卫星 | GPS（SVID 1–37），Sig1 = L1C/A | 本站文件只有 GPS |
| 仰角 | ≥ 30° | 高纬常用 20–30°；10–30° 底噪明显抬高（3.4） |
| Sig1 锁定时间 | ≥ 240 s | 相位去趋势滤波需要收敛，惯用 240 s；本数据里对 S4 起作用 |
| TEC 用第二频率锁定 | col 27 ≥ 240 s | 否则 dTEC 出现上百 TECU 假值 |
| σφ 分级 | 0.25 rad（中等）、0.5 rad（强） | 常用分级，本文采用 |
| S4 分级 | 0.2 | 同上 |

## 6. 在工作流里接哪一步

- [B · 不规则体 / 磁暴](./README.md#b--不规则体--磁暴)：ISMR 是**接收机硬件**用 50 Hz 算的 S4/σφ，是 ROTI（[oasis-roti](./oasis-roti.md)，1 Hz/30 s RINEX）的对照真值；3.4 的逐小时表可以直接和 ROTI、Swarm IPIR（[swarm-data](./swarm-data.md)）、Kp 时间轴对齐。
- [A · 一日 TEC](./README.md#a--一日-tec)：ISMR 的 TEC 列未校准，只适合看相对变化；绝对 TEC 用 CHAIN 的 RINEX 自己算，或用 GIM。
- 批量：同一小时目录列出全部站 → 按站循环；一站一天 24 个文件，约 1.5 MB。

## 7. 坑（现象 → 原因 → 修复）

1. **`chain.physics.unb.ca/data/gps/ismr/2024/` 404、`https://chain.physics.unb.ca` 连不上** → 数据迁到 `chain-project.net`，老 UNB 目录只剩空壳，老站没有 HTTPS → 用 `https://www.chain-project.net/data/gps/ismr/…`。
2. **说明页的 `http://www.chain-project.net/data` 被 301** → 跳到 `chain-new.chain-project.net` → curl 加 `-L`，或直接用 `https://www.chain-project.net/data/`。
3. **FTP 一会儿能列、一会儿 90 s 超时** → 匿名 FTP（用户 `ftp`、密码填邮箱）不稳定 → 脚本走 HTTPS，FTP 只作备用。
4. **站表上 “Active” 的 GSV4004B 站（cbb、res、pon…）找不到 2024 文件** → 小时目录只有 PolaRxS 站，GSV4004B 的 ISMR 在 `nvismr/` 且到 2019 → 先列小时目录确认站在不在。
5. **ISMR 没表头，列错一位全错** → 62 列由 `sbf2ismr` 定义，`-n` 还能截短 → 按手册列号读，并用 L2/L1 Phi 比 ≈ 1.283 自检。
6. **时间差 18 s / 差一分钟** → WN/TOW 是 GPS 时，标的是该分钟**结束** → UTC = GPS − 18 s，统计区间是 [TOW−60, TOW)。
7. **直接把列 8 当 S4** → 那是含热噪声的总 S4 → 用 √(S4总² − 列9²)。
8. **以为锁定时间过滤没用** → 锁定 < 240 s 时 Phi 已被置 nan，但 S4 仍输出且偏高（中位 0.181 vs 0.063）→ S4 统计必须加锁定过滤。
9. **TEC 列出现几十上百 TECU 的跳变** → 第二频率刚重锁（col 27 = 1 s），伪距 TEC/相位 dTEC 未收敛；TEC 本身还含接收机偏差 → 过滤 col 27，TEC 只看相对变化，或用 `sbf2ismr -C` 校准。
10. **高纬 σφ 大就说“强闪烁”** → 60 s 窗的 Phi60 混有折射性低频起伏（磁暴时 Phi60/Phi01 = 2.28）→ 同时报 Phi01/Phi10 和谱斜率 p，别只报 Phi60；接近 π 的极值要人工看。
11. **低仰角把平均值拉高** → 多径与长路径，10–30° 行底噪就有 0.1 rad / 0.15 → 切仰角（本文 30°）并写明。
12. **拿 S4 判断高纬闪烁** → 高纬以相位闪烁为主，这次磁暴 S4 > 0.2 只有 1.2% → 相位看 σφ、幅度看 S4，分开报。
13. **`python3` 跑到别人的 venv** → 共享机上 PATH 被其他 venv 抢先（本机 `which python3` 指向 `/workspace/orbdetwork/venv`）→ 可复现脚本写明解释器（本文用 `/usr/bin/python3`）。
14. **发表时忘了引用** → CHAIN 数据政策要求引用 Jayachandran et al. 2009（doi 10.1029/2008RS004046），发表后告知 CHAIN。

## 8. 选型对比

| 需求 | 选这个 | 不选这个 |
|---|---|---|
| 加拿大高纬/极光带 1 min S4、σφ，免注册 | **CHAIN ISMR**（本文 E26） | — |
| 巴西/低纬 ISMR | [ismr-downloader](./ismr-downloader.md)（UNESP，需账号） | CHAIN |
| 只有普通 RINEX 的站也要闪烁指标 | [oasis-roti](./oasis-roti.md)（ROTI） | ISMR（要专用接收机） |
| 卫星原位不规则体 | [swarm-data](./swarm-data.md)（IPIR / IBI） | 地面单站 |
| 50 Hz 原始相位做谱分析 | CHAIN `gps/data/raw/` 二进制 | ISMR（已是 1 min 统计） |
| 仿真闪烁信号 | [iono-scintillation](./iono-scintillation.md) | 实测数据 |
