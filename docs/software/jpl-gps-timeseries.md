# JPL GNSS 时间序列（sideshow `post/`）匿名下载：坐标时序 / 残差 / 速度与阶跃表——ALGO 实测

目录：[`PROJECTS.json` → `JPL-GPS-Time-Series`](../../PROJECTS.json) · 入口 <https://sideshow.jpl.nasa.gov/post/series.html> · 数据目录 <https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/> · 方法说明 [GNSS_Time_Series.pdf](https://sideshow.jpl.nasa.gov/post/tables/GNSS_Time_Series.pdf)（8 页）· 本机验证 **2026-09-26 06:27–06:37 EDT**（匿名，只下单站 ALGO + 4 张表 + 方法 PDF，合计约 25 MB）

> 岗位：回答“JPL（GipsyX）给某个 GNSS 站算的每日坐标时序、速度、阶跃和季节项，不登录去哪拿、文件名怎么拼、每列是什么”。样例站 **ALGO**（加拿大 Algonquin，IGS 站）。
>
> 冲突时：以目录列表和文件内容为准，**不以 `series.html` 首页文字为准**（首页还写“31 颗卫星、2000 多台接收机”，表里实际 2860 站）。数字只代表 2026-09-26 这一次。

## 1. 用途与边界

**做：** JPL 大地测量组用 GipsyX 做 PPP（NNR 轨道钟差 → 转 IGS14）后发布的全球约 2860 站日解：编辑后时序 `*.series`、残差 `*.resid`、四张汇总表（XYZ 位置速度、经纬高位置速度、阶跃、季节项）、每站一张 JPG 图。全部 HTTPS 匿名静态文件，`curl` 即可。

**不做：** 原始 RINEX（回 IGS / CDDIS / 区域网，见 [gnss-obs-mirrors](./gnss-obs-mirrors.md)、[cors-networks](./cors-networks.md)）；亚日（5 分钟）坐标、对流层产品（同类需求见 [unr-ngl](./unr-ngl.md)）；IGS20 框架（**仍是 IGS14**，见坑 1）。

**结论先说：**

| 产品 | 路径（`P=https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post`，`W=https://sideshow.jpl.nasa.gov/post`） | 实测（2026-09-26） |
| --- | --- | --- |
| 编辑后时序 | `$P/point/SSSS.series` | 2860 个；ALGO 2477425 B，12085 行，1992-08-29 → **2026-09-19** |
| 残差时序 | `$P/resid/SSSS.resid`（**不是** `.series`） | 2860 个；ALGO 与 `.series` 同行数同字节数 |
| XYZ 位置 + 速度 | `$W/tables/table1.html`（HTML 里的 `<pre>` 文本） | 463562 B；2860 站；IGS14，参考历元 2026-01-01；**单位 mm** |
| 纬经高 + NEU 速度 | `$W/tables/table2.html` | 463647 B；GRS80 |
| 阶跃 | `$W/tables/table3.html` | 808045 B；ALGO 2 个（1994.1302、2012.9665） |
| 季节项 | `$W/tables/table4.html` | 926882 B；年项 AC1/AS1、半年项 AC2/AS2 |
| 单站图 | `$W/plots/SSSS.jpg`（站点页 `$W/links/SSSS.html` 只包这张图） | ALGO 188944 B |
| 旧快照 | `…/repro2018a/raw/position/envseries/`（`.series/.resid/.model/.sum/_E/N/V.png`） | 2951 站，停在 2019–2020，**不再更新** |

更新：1822 个 `.series` 的 mtime 是 2026-09-25 16:03（**美西时间**，HEAD `Last-Modified: Fri, 25 Sep 2026 23:03:17 GMT` = 19:03 EDT），数据末日 2026-09-19，即约 **6–7 天延迟、每周左右整体重算**。

## 2. 安装

只需要 `curl`、`sed`、`awk`、Python 3 标准库，不装第三方包。

## 3. 真命令 + 期望输出

### 3.1 单站全部小文件 + 表格行（`jpl.sh`）

```bash
#!/usr/bin/env bash
# 用法：bash jpl.sh ALGO   （站名大写 4 字符）
S=${1:-ALGO}; W=https://sideshow.jpl.nasa.gov/post; P=https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post
g(){ curl -sS -m 60 -o "$2" -w "%{http_code} %{size_download} B %{time_total}s  $2\n" "$1"; }
g $P/point/$S.series  $S.series      # 编辑后时序（去粗差）
g $P/resid/$S.resid   $S.resid       # 残差时序
for t in 1 2 3 4; do curl -sS -m 60 $W/tables/table$t.html | sed 's/<[^>]*>//g' > t$t.txt; done
grep -hE 'frame|epoch' t1.txt
grep -hE "^$S " t1.txt t2.txt
echo "breaks: $(grep -c "^$S " t3.txt)"; grep -E "^$S A[CS]1" t4.txt
echo "sites: $(grep -c ' POS ' t1.txt)"
curl -sS -m 60 $P/point/ | sed "s/<[^>]*>/ /g" | awk "/\\.series /{print \$2}" | sort | uniq -c | sort -k2 | tail -3   # 文件 mtime（美西时间）
```

期望输出（2026-09-26 06:31 EDT）：

```text
200 2477425 B 0.806309s  ALGO.series
200 2477425 B 0.608832s  ALGO.resid
The reference frame is IGS14.
The reference epoch is January 1, 2026.
ALGO POS   918129037.536 -4346071346.443  4561977936.643   0.276   0.693   0.685
ALGO VEL         -16.018          -3.815           4.085   0.030   0.075   0.075
ALGO POS    45.955801000   -78.071373000      200975.194   0.309   0.232   0.935
ALGO VEL           2.536         -16.460           3.229   0.033   0.025   0.102
breaks: 2
ALGO AC1           0.234           0.401          -0.623   0.222   0.167   0.679
ALGO AS1           0.482           0.022          -2.361   0.218   0.164   0.665
sites: 2860
      4 2026-09-11
     17 2026-09-17
   1822 2026-09-25
```

前两行 table1（XYZ，mm），后两行 table2（纬度、经度、高 mm；速度 N/E/V mm/yr）。把 table1 的 XYZ 速度旋到站心得 E −16.461 / N 2.537 / U 3.23，与 table2 一致。

### 3.2 只看末几行判断某站是否还在更新（Range 请求，几百字节）

```bash
P=https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point
for s in P090 BJFS AB12 WUHN WUH2; do c=$(curl -sS -m 30 -r -400 -o tail.tmp -w "%{http_code}" $P/$s.series); echo "$s $c $(tail -1 tail.tmp | awk 'NF==17{printf "%s-%02d-%02d",$12,$13,$14}')"; done; rm -f tail.tmp
```

```text
P090 206 2026-09-19
BJFS 206 2026-09-19
AB12 206 2019-04-30
WUHN 206 2026-08-17
WUH2 404
```

AB12 文件 mtime 是 2026-07-08，但数据停在 **2019-04-30**——mtime 不等于最后观测日（坑 6）。WUH2 不在 JPL 站表里（404），武汉只有 WUHN。

### 3.3 读文件（`read.py`，只用标准库）

```python
import sys, math, datetime as dt, collections
S = sys.argv[1] if len(sys.argv) > 1 else "ALGO"
J2K = dt.datetime(2000, 1, 1, 12)          # GPS 时
R = [l.split() for l in open(f"{S}.series")]
t = [float(r[0]) for r in R]; enu = [[float(r[i]) for i in (1, 2, 3)] for r in R]
d = [dt.date(*map(int, r[11:14])) for r in R]
dup = [k for k, v in collections.Counter(d).items() if v > 1]
print(f"{S}.series: {len(R)} 行, {d[0]} → {d[-1]}, 缺 {(d[-1]-d[0]).days+1-len(set(d))} 天, 同日两行 {len(dup)} 天")
r = R[-1]; s = float(r[10])
print("末行: 十进制年", r[0], "| J2000 秒", r[10], "→", J2K + dt.timedelta(seconds=s),
      "| 2000+s/365.25d =", round(2000 + s / 31557600, 8))
print("时刻分布:", collections.Counter(f"{int(x[14]):02d}:{int(x[15]):02d}" for x in R).most_common(3))
sel = [(a, b) for a, b in zip(t, enu) if a > 2013]
def slope(k):
    x = [a for a, _ in sel]; y = [b[k] for _, b in sel]; mx = sum(x)/len(x); my = sum(y)/len(y)
    return sum((p-mx)*(q-my) for p, q in zip(x, y)) / sum((p-mx)**2 for p in x) * 1e3
print("2013 起最小二乘 mm/yr: E %.2f N %.2f U %.2f" % tuple(slope(k) for k in range(3)))
near = min(zip(t, enu), key=lambda z: abs(z[0]-2026.0)); print("最接近 2026.0 的点:", near[0], [round(v*1e3, 1) for v in near[1]], "mm")
Q = [l.split() for l in open(f"{S}.resid")]
rv = [abs(float(q[3])) for q in Q]; print(f"{S}.resid: {len(Q)} 行, |U 残差| 中位 {sorted(rv)[len(rv)//2]*1e3:.1f} mm, 最大 {max(rv)*1e3:.1f} mm")
# table1 XYZ(mm) → 纬经高 vs table2
X, Y, Z = [float(v)/1e3 for v in next(l for l in open("t1.txt") if l.startswith(S+" POS")).split()[2:5]]
a = 6378137.0; f = 1/298.257222101; e2 = f*(2-f); p = math.hypot(X, Y); la = math.atan2(Z, p*(1-e2))
for _ in range(8):
    N = a/math.sqrt(1-e2*math.sin(la)**2); h = p/math.cos(la)-N; la = math.atan2(Z, p*(1-e2*N/(N+h)))
lat2 = float(next(l for l in open("t2.txt") if l.startswith(S+" POS")).split()[2])
print("table1 XYZ→纬度 %.9f  table2 纬度 %.9f  差 %.1f cm" % (math.degrees(la), lat2, (lat2-math.degrees(la))*111195*100))
```

期望输出：

```text
ALGO.series: 12085 行, 1992-08-29 → 2026-09-19, 缺 362 天, 同日两行 7 天
末行: 十进制年 2026.71594323 | J2000 秒 843091050.00 → 2026-09-19 11:57:30 | 2000+s/365.25d = 2026.71594323
时刻分布: [('11:57', 11805), ('13:27', 64), ('10:27', 20)]
2013 起最小二乘 mm/yr: E -16.54 N 2.52 U 3.20
最接近 2026.0 的点: 2025.99862632 [-4.2, -4.6, 3.1] mm
ALGO.resid: 12085 行, |U 残差| 中位 3.9 mm, 最大 92.8 mm
table1 XYZ→纬度 45.955800812  table2 纬度 45.955801000  差 2.1 cm
```

2013 年后的简单直线斜率（E −16.54 / N 2.52 / U 3.20）与 table2 速度（E −16.460 / N 2.536 / U 3.229）相差 < 0.1 mm/yr；ALGO 只有两个阶跃，直线够用。阶跃多的站（例如 AB07 有 12 个，含 2020.5558 的 dN −184 mm）必须用 table2/table3，不能自己拉直线。

## 4. 输入 / 输出（字段）

- **`.series` / `.resid`**（17 列，空格分隔，无表头；PDF 第 7 页）：1 十进制年；2–4 东 / 北 / 垂直（**m**）；5–7 σE/σN/σV（m）；8–10 E-N、E-V、N-V 相关系数；11 J2000 秒；12–17 年 月 日 时 分 秒。
  - 十进制年 = `2000 + J2000秒 / (365.25×86400)`，**零点是 2000-01-01 12:00**，不是日历年初（旧 README 写明 365.25 天/年、GPS 时）。
  - J2000 秒直接加到 2000-01-01 12:00 就等于 12–17 列（同一时标，不用管闰秒）。
  - `.series` 的 ENU 以参考历元 2026-01-01 附近为零点（ALGO 最接近 2026.0 的点 −4.2 / −4.6 / 3.1 mm，差的是季节项和噪声）；`.resid` = 观测 − 模型（线性 + 阶跃 + 季节）。
- **table1**：`SSSS POS X Y Z SX SY SZ`、`SSSS VEL VX VY VZ …`，位置和误差都是 **mm**（ALGO X = 918129037.536 mm）。
- **table2**：`SSSS POS 纬度(°) 经度(°) 高(mm) SN SE SV`、`SSSS VEL N E V`（mm/yr）；表头印成 `N E V`，POS 行实际是纬、经、高；经度 −180…180。
- **table3**：`SSSS 阶跃时刻(十进制年) dN dE dV σN σE σV`（mm）。
- **table4**：`SSSS AC1|AS1|AC2|AS2 N E V σ…`（mm），年项 `AC1·cos(2πt)+AS1·sin(2πt)`，半年项 `AC2·cos(4πt)+AS2·sin(4πt)`，t 为十进制年。
- 表中参数误差按 PDF 已 **×20** 放大（“与一 σ 降采样结果一致”）。

## 5. 参数（路径拼装）

| 变量 | 规则 |
| --- | --- |
| `SSSS` | 4 字符，**必须大写**（`algo.series` 404）；首页 `links/SSSS.html` 列出全部 2860 个 |
| 版本 | 只有 `repro2018a/post/` 在更新；`repro2011b/`、`repro2015a.TEST/`、`repro2018a/raw/` 和按地震命名的目录（`20120811_Iran/` 等）都是历史快照 |
| 协议 | 只用 `https://`；`http://sideshow.jpl.nasa.gov` 20 s 超时 0 字节；旧 README 里的 `ftp://` 15 s 连接超时 |
| 增量同步 | 服务器支持 `If-Modified-Since`（`curl -z 本地文件` 返回 304、0 字节）和 Range（206）；不支持 gzip 压缩传输 |

## 6. 接到哪一步

- 站坐标 / 速度对照：与 [unr-ngl](./unr-ngl.md) 的 MIDAS 速度（IGS20）互相核对，注意 JPL 是 **IGS14**，两框架差值不能当形变。
- 电离层 / TEC 处理要固定站坐标时：取 table1 XYZ（mm → m，再按速度外推到观测日），接 [pytecgg](./pytecgg.md)、[gnss-tec](./gnss-tec.md)。
- 原始观测：回 [gnss-obs-mirrors](./gnss-obs-mirrors.md)（CDDIS 要 Earthdata 账号，BKG/IGN 等匿名镜像见该页）。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 和 IGS20 / ITRF2020 坐标差几毫米到厘米 | table1/2 与 PDF 都写 **IGS14**；IGS 2022-11 已换 IGS20，JPL 这套 `repro2018a` 未换 | 跨产品对比先做框架转换，或都用同一框架的产品 |
| 2 | 残差文件按 `resid/SSSS.series` 下载 404 | 残差后缀是 `.resid`；首页 “Residuals” 只链到目录 | `resid/SSSS.resid` |
| 3 | PDF 的整目录 wget 命令拿到别的东西或多爬 | PDF 把 URL 写成 `…/post/point`（无尾斜杠），服务器 301 到 `point/`，`-np` 的父目录因而变成 `post/` | 目录 URL 加尾斜杠；只要少数站就逐站 `curl`，不要整目录爬（2860 × 约 1–2 MB） |
| 4 | table2 纬度和 XYZ 换算差 2 cm | table2 纬经度只给 6 位小数后补 `000`（约 ±5 cm），误差列却是 mm | 要厘米以下精度用 table1 XYZ 自己换算 |
| 5 | 把 table1 的 918129037.536 当米 | 表里位置单位是 **mm** | ÷1000 |
| 6 | 以为 mtime 新的文件就是活跃站 | 停测站的文件也会被重写：AB12 mtime 2026-07-08，数据只到 2019-04-30 | 读最后一行（Range `-r -400`）看末日 |
| 7 | 同一天出现两行，按日期做键时覆盖 | 部分日子的弧段不以 11:57:30 为中心（如 10:45 与 22:45），ALGO 7 天有两行 | 用第 11 列 J2000 秒做键 |
| 8 | 十进制年 2026.0 对不上 1 月 1 日 00:00 | 零点是 J2000（2000-01-01 12:00），且按 365.25 天/年 | 用第 11 列换算，不要用日历年分数 |
| 9 | PDF 说“形式误差 > 5 mm 的点剔除”，文件里仍有 σ 到 9.3 mm 的点 | ALGO 有 54 个历元 σ > 5 mm（多数在 1990 年代） | 自己按 σ 再筛一遍 |
| 10 | 首页写 “31 satellites”“over 2000 receivers” | 首页文字多年未改；表里 2860 站 | 以表和目录为准 |
| 11 | `raw/position/envseries/0000_README.format` 说的是 `repro2011b`、`ftp://…/JPL_GPS_Timeser/…` | 旧 README 拷贝未改，路径拼错且 ftp 已不可达 | 只用 `repro2018a/post/`；README 里仍有用的只有“GPS 时、365.25 天/年” |
| 12 | 找不到武汉 WUH2 等较新 IGS 站 | JPL 只处理自己的站表（2860 站），不是所有 IGS 站 | 查首页 `links/` 列表；没有就换 UNR NGL |
| 13 | `http://` 或 `ftp://` 卡住 | 只开 443 | 一律 `https://` 加 `curl -m` |

## 8. 选型

- **要 IGS14 下的 JPL 官方速度 / 阶跃 / 季节项**：四张表一次拿全（合计约 2.7 MB），不必逐站下时序。
- **单站日坐标时序**：`point/SSSS.series`；想看模型拟合好坏再下 `resid/SSSS.resid`。
- **要 IGS20、5 分钟坐标或 ZTD/PWV、更多站（约 2.4 万）**：用 [unr-ngl](./unr-ngl.md)。
- **要原始 RINEX 自己解**：不在这里，去 IGS / 区域网。
