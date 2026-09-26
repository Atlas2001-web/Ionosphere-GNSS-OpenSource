# UNR NGL 匿名 GNSS 坐标时间序列 / 5 分钟对流层 / MIDAS 速度——P090 实测

目录：[`PROJECTS.json` → `UNR-NGL`](../../PROJECTS.json) · 入口 <https://geodesy.unr.edu/> · [Plug and Play 数据产品页](https://geodesy.unr.edu/PlugNPlayPortal.php) · 本机验证 **2026-09-26 06:21–06:26 EDT**（匿名，未注册；只下小文件，合计约 4 MB）

> 岗位：回答“某个 GNSS 站的每日坐标、5 分钟坐标、5 分钟天顶延迟 / 水汽、速度、阶跃，不登录去哪拿、路径怎么拼、字段是什么”。样例站 **P090**（美国内华达 Reno，EarthScope 站），样例日 **2024-05-11（年积日 132，大磁暴日）**。
>
> 冲突时：以站点页 `NGLStationPages/stations/<SSSS>.sta` 里的链接为准；**Plug and Play 页上写的直链多数已 404**（见第 7 节）。数字只代表 2026-09-26 这一次。

## 1. 用途与边界

**做：** Nevada Geodetic Laboratory（NGL，内华达大学 Reno）用 GipsyX 对全球 GNSS 站做 PPP 后的公开产品：24 h 最终解 / 快速解（tenv3、tenv、txyz2）、5 分钟坐标（kenv）、5 分钟对流层（SINEX TRO：ZTD、湿延迟、梯度、PWV、加权平均温度）、MIDAS 速度、阶跃（设备变更 + 地震）库、站点清单。全部 HTTPS 匿名，纯静态文件，`curl` 即可。

**不做：** 原始 RINEX（只有 MAGNET 网在 `/magnet/rinex/`，其余回 IGS / 区域网，见 [cors-networks](./cors-networks.md)）；电离层 TEC（NGL 不发布）；实时流。

**结论先说：**

| 产品 | 路径（`T=https://geodesy.unr.edu/gps_timeseries/IGS20`） | 实测（P090，2026-09-26） |
| --- | --- | --- |
| 24 h 最终解 | `$T/tenv3/IGS20/SSSS.tenv3`（板块框架 `$T/tenv3/NA/SSSS.NA.tenv3`）；`$T/tenv/SSSS.tenv`；`$T/txyz/SSSS.txyz2` | 1379040 B，6759 天，2007-11-10 → **2026-09-12**（延迟 14 天） |
| 24 h 快速解 | `$T/rapids/IGS20/SSSS.tenv3` | 10608 B，51 天，2026-07-27 → **2026-09-24**（延迟 2 天），只保留约 60 天 |
| 5 min 坐标（快速） | `$T/rapids_5min/kenv/SSSS/SSSS.YYYY.kenv.zip`（最终版在 `$T/kenv/SSSS/`） | 469509 B，51 个日文件；最新 doy 267 只有 183 / 288 历元 |
| 5 min 对流层 | `$T/trop/SSSS/SSSS.YYYY.trop.zip`，内含每日 `SSSS.YYYY.DDD.trop.gz` | 2024 年 2226772 B，342 个日文件（缺 24 天）；**2026 年的 zip 还没有**（最新 2025，2026-01-10 生成） |
| MIDAS 速度 | `$T/midas/midas.IGS.txt`（板块：`midas.NA.txt` 等） | 5.4 MB；P090 E −20.29 / N −5.90 / U −0.82 mm/yr |
| 阶跃库 | `https://geodesy.unr.edu/NGLStationPages/steps.txt` | 7.4 MB，142578 行（其中地震型 118431 行）；P090 共 10 条 |
| 站点清单 | `https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt` | 23793 站；Dtend ≥ 2026-09-01 的 8313 站 |

## 2. 安装

只需要 `curl`、`awk`、Python 3 标准库（`zipfile`、`gzip`），不装第三方包。

## 3. 真命令 + 期望输出

### 3.1 一个站的全部小文件（`ngl.sh`）

```bash
#!/usr/bin/env bash
# 用法：bash ngl.sh P090     （站名必须大写 4 字符）
S=${1:-P090}; B=https://geodesy.unr.edu; T=$B/gps_timeseries/IGS20
g(){ curl -sS -m 60 -o "$2" -w "%{http_code} %{size_download} B %{time_total}s  $2\n" "$1"; }
g $B/NGLStationPages/stations/$S.sta        $S.sta
g $T/tenv3/IGS20/$S.tenv3                   $S.tenv3        # 24 h 最终解
g $T/rapids/IGS20/$S.tenv3                  $S.rapid.tenv3  # 24 h 快速解
g $T/trop/$S/$S.2024.trop.zip               $S.2024.trop.zip
g $T/rapids_5min/kenv/$S/$S.2026.kenv.zip   $S.2026.kenv.zip
curl -sS -m 60 $B/NGLStationPages/DataHoldings.txt | awk -v s=$S 'NR==1||$1==s'
curl -sS -m 60 $T/midas/midas.IGS.txt | awk -v s=$S '$1==s{printf "MIDAS %s E %.2f N %.2f U %.2f mm/yr (±%.2f %.2f %.2f) steps=%s\n",$1,$9*1e3,$10*1e3,$11*1e3,$12*1e3,$13*1e3,$14*1e3,$24}'
curl -sS -m 60 $B/NGLStationPages/steps.txt | awk -v s=$S '$1==s'
```

期望输出（2026-09-26 06:24 EDT）：

```text
200 18017 B 0.328169s  P090.sta
200 1379040 B 0.846828s  P090.tenv3
200 10608 B 0.378056s  P090.rapid.tenv3
200 2226772 B 0.649537s  P090.2024.trop.zip
200 469509 B 0.530804s  P090.2026.kenv.zip
Sta  Lat(deg)   Long(deg) Hgt(m)  X(m)           Y(m)         Z(m)          Dtbeg      Dtend      Dtmod      NumSol StaOrigName
P090  39.5728   240.2001 1503.649 -2447197.9166 -4273073.8497  4042495.2532 2007-11-10 2026-09-12 2026-09-22   6759
MIDAS P090 E -20.29 N -5.90 U -0.82 mm/yr (±0.17 0.15 0.59) steps=9
P090  18MAR02  1  Elevation_Cutoff_Changed
P090  20AUG03  1  Antenna_Type_Changed
P090  20AUG03  1  Receiver_Make_and_Model_Changed
P090  08APR26  2    57.544    13.153  5.1 nn00385392
P090  19JUL06  2   575.440   465.105  7.1 ci38457511
P090  20MAY15  2   288.403   229.929  6.5 nn00725272
P090  21JUL08  2   162.181   121.258  6.0 nc73584926
P090  24DEC05  2   512.861   453.729  7.0 nc75095651
P090  24DEC09  2   114.815    80.506  5.7 nn00888580
P090  26APR14  2   114.815    73.008  5.7 nn00914068
```

同样的路径对 ALGO（2348652 B）、BJFS（1930452 B）也都是 200。

### 3.2 读三种文件（`read.py`，只用标准库）

```python
import sys, gzip, io, zipfile, datetime as dt
S = sys.argv[1] if len(sys.argv) > 1 else "P090"
D0 = dt.date(1858, 11, 17)
def tenv3(fn):
    R = [l.split() for l in open(fn) if not l.startswith("site")]
    mjd = [int(r[3]) for r in R]
    enu = [[int(r[i]) + float(r[i + 1]) for i in (7, 9, 11)] for r in R]
    print(f"{fn}: {len(R)} 天, {D0+dt.timedelta(mjd[0])} → {D0+dt.timedelta(mjd[-1])}, "
          f"缺 {mjd[-1]-mjd[0]+1-len(set(mjd))} 天, 整数部分组合 {len({(r[7],r[9],r[11]) for r in R})} 种")
    return R, mjd, enu
R, mjd, enu = tenv3(f"{S}.tenv3"); tenv3(f"{S}.rapid.tenv3")
yr = (mjd[-1] - mjd[0]) / 365.25
print("首末差分速率 mm/yr: E %.1f N %.1f U %.1f" % tuple((enu[-1][k]-enu[0][k])/yr*1e3 for k in range(3)))
for r, x in zip(R, enu):
    if r[1] in ("24MAY10", "24MAY11"):
        print(r[1], "dE %.4f dN %.4f dU %.4f m  sigU %s" % (x[0]-enu[0][0], x[1]-enu[0][1], x[2]-enu[0][2], r[16]))
z = zipfile.ZipFile(f"{S}.2024.trop.zip")
days = sorted(int(n.split(".")[2]) for n in z.namelist())
print(f"trop 2024: {len(days)} 个日文件, 缺 {366-len(days)} 天")
txt = gzip.decompress(z.read(f"{S}.2024.132.trop.gz")).decode()
blk = txt.split("+TROP/SOLUTION")[1].split("-TROP/SOLUTION")[0].splitlines()
rows = [l.split() for l in blk if l.startswith(" ")]
ztd = [float(r[2]) for r in rows]; pwv = [float(r[9]) for r in rows]
print(f"2024-132: {len(rows)} 历元, ZTD {min(ztd)}–{max(ztd)} mm, PWV {min(pwv)}–{max(pwv)} mm, 坐标系标签",
      [l.split()[7] for l in txt.splitlines() if l.startswith(f" {S}  A    1 P")])
k = zipfile.ZipFile(f"{S}.2026.kenv.zip")
last = sorted(k.namelist())[-1]
n = len(gzip.decompress(k.read(last)).decode().splitlines()) - 1
print(f"rapid 5 min: {len(k.namelist())} 个日文件, 最新 {last} {n} 历元 / 288")
```

期望输出：

```text
P090.tenv3: 6759 天, 2007-11-10 → 2026-09-12, 缺 123 天, 整数部分组合 1 种
P090.rapid.tenv3: 51 天, 2026-07-27 → 2026-09-24, 缺 9 天, 整数部分组合 1 种
首末差分速率 mm/yr: E -20.2 N -5.6 U -0.4
24MAY10 dE -0.3385 dN -0.0903 dU -0.0193 m  sigU 0.003727
24MAY11 dE -0.3365 dN -0.0910 dU -0.0183 m  sigU 0.003829
trop 2024: 342 个日文件, 缺 24 天
2024-132: 288 历元, ZTD 1971.9–1984.4 mm, PWV 6.11–8.06 mm, 坐标系标签 ['IGS14_']
rapid 5 min: 51 个日文件, 最新 P090.2026.267.kenv.gz 183 历元 / 288
```

首末差分（E −20.2 / N −5.6）与 MIDAS（E −20.29 / N −5.90）同量级；垂直差分只有 −0.4 mm/yr，受季节项和阶跃影响，**速度请用 MIDAS**，不要用首末差分。

## 4. 输入 / 输出（字段）

- **tenv3**（23 列，[README](https://geodesy.unr.edu/gps_timeseries/readmes/README_tenv3.txt)）：站名、`YYMMMDD`、十进制年、MJD、GPS 周、周内日、参考经线（每 0.1°）、东 / 北 / 高各拆成“整数 m + 小数 m”两列（第 8–13 列）、天线高、σE/σN/σU（m）、三个相关系数、名义经纬高。**画图只用小数部分**；整数部分变化 = 跳变超过 10 m 或重名站。
- **kenv**（17 列，[README](https://geodesy.unr.edu/gps_timeseries/readmes/README_kenv.txt)）：`sec-J2000`（自 2000-01-01 12:00 起的 GPS 秒；实测 843393600 = 2026-09-23 00:00）、MJD、年月日、年积日、日内秒、相对参考点 ENU、相对日均值 ENU、σ。
- **trop**（SINEX TRO，[README](https://geodesy.unr.edu/gps_timeseries/readmes/README_trop2.txt)）：`TROTOT`（ZTD，mm）、`TRWET`（湿延迟，mm）、`TGETOT`/`TGNTOT`（梯度，mm）、`WVAPOR`（PWV，mm）、`MTEMP`（K），每列后跟 `_SIG`。VMF1 映射，截止高度角 7°，采样 300 s。
- **MIDAS**：第 9–11 列 ENU 速度（m/yr），12–14 不确定度，24 阶跃数，25–27 经纬高（[README](https://geodesy.unr.edu/velocities/midas.readme.txt)）。
- **steps.txt**：类型 1 = 设备变更（第 4 列事件名）；类型 2 = 可能的地震阶跃（第 4 列阈值距离 km、第 5 列震中距 km、震级、USGS 事件 ID）；类型 3 = 软件 / 产品变化。

## 5. 参数（路径拼装）

| 变量 | 规则 |
| --- | --- |
| `SSSS` | 4 字符站名，**必须大写**（`p090.sta`、`p090.tenv3` 都是 404） |
| 框架 | `tenv3/IGS20/` 全球框架；`tenv3/<板块>/SSSS.<板块>.tenv3`（NA、EU、PA…），只差水平趋势，垂直相同 |
| `YYYY` | trop / kenv 按年打 zip；zip 内是 `SSSS.YYYY.DDD.*.gz` |
| 延迟 | 最终解约 2 周；快速解约 1–2 天；5 min 快速解只保留约 60 天 |

## 6. 接到哪一步

- GNSS 站坐标 / 速度（形变、参考框架）：接 MIDAS 与 steps；原始观测回 [cors-networks](./cors-networks.md) / [gnss-obs-mirrors](./gnss-obs-mirrors.md)。
- 对流层：NGL 的 ZTD / PWV 可作为 [gtrop](./gtrop.md)、[tu-wien-vmf-gpt-codes](./tu-wien-vmf-gpt-codes.md) 模型值的对照（NGL 用 VMF1 映射函数）。
- 电离层研究：用 NGL 的站坐标做 TEC 处理时的固定坐标（[pytecgg](./pytecgg.md)、[gnss-tec](./gnss-tec.md)）；磁暴日（2024-05-10/11）P090 日解相差 ≤ 2 mm，坐标本身不受电离层暴影响，TEC 仍需自己算。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 按 Plug and Play 页写的 `gps_timeseries/tenv3/IGS14/SSSS.tenv3`、`tenv3/plates/NA/…`、`txyz/IGS14/…`、`qa/SSSS.qa.gz` 下载全是 404 | 上游页面没跟上 IGS20 目录改版（页面上方又写“全部为 IGS20”） | 用 `gps_timeseries/IGS20/…` 路径，或从站点页 `.sta` 抄链接 |
| 2 | `http://geodesy.unr.edu/…` 卡住 15 s 以上无响应 | 80 端口不响应；README_trop2、steps_readme、midas.readme 里仍写 http | 一律改 `https://`，并加 `curl -m` |
| 3 | 小写站名 404 | 路径大小写敏感 | 转大写 |
| 4 | README 的 `zgrep -A1000 -m1 '^[+-]TROP/SOLUTION' … \| tail -n+3` 得到 290 行，不是写的 288 行 | 把 `-TROP/SOLUTION` 和 `%=ENDTRO` 也带出来了 | 只保留以空格开头的行（`awk 'NF>=11'`） |
| 5 | 东西梯度和南北梯度对不上 | README 警告：NGL 的 tropo SINEX 格式错误，`TGNTOT` 与 `TGETOT` 两列（及其 σ）互换 | 用梯度前先互换两列 |
| 6 | trop 文件 `TROP/DESCRIPTION` 写 `TRODRY TROWET …`，而数据表头是 `TROTOT … TRWET` | 描述块与数据列不一致 | 以 `*SITE ___EPOCH____ TROTOT …` 表头为准；第 3 列是 ZTD 总延迟 |
| 7 | trop 文件站坐标标签是 `IGS14_`，但 INPUT 写 JPL/IGS20 轨道 | 标签遗留 | 需要坐标时取 tenv3/txyz2（IGS20），不要取 trop 头 |
| 8 | 找不到今年的 trop zip | README 说每周更新，但 2026 年 zip 尚未生成（最新 2025.trop.zip 生成于 2026-01-10） | 当年 5 分钟对流层暂时拿不到；历史年份可用 |
| 9 | 一年 trop 只有 342 天 | 缺测日直接没有文件（P090 2024 年缺 24 天，287–295 连缺 9 天） | 用 zip 文件名列表判断覆盖，不要假设连续 |
| 10 | DataHoldings 的经度是 240.2 | 按 0–360 存；tenv3 用 −119.8 | 减 360 |
| 11 | 最新的 5 分钟日文件历元不满 288 | 快速解当天数据未到齐（doy 267 只有 183） | 最后 1–2 天等补齐后再用 |
| 12 | `unzip -l` 列出的日期乱序 | zip 内条目不按年积日排序 | 自己 `sorted()` |
| 13 | 旧 IGS14 图 `tsplots/IGS14/…/P090.png` 仍返回 200 | 旧图没删，最后更新 2025-08-08 | 看图用 `gps_timeseries/IGS20/tsplots/…` |
| 14 | 首末差分速率与 MIDAS 差很多（尤其垂直） | 季节项、阶跃、缺测 | 用 MIDAS，或按 steps.txt 分段拟合 |

## 8. 选型

- **只要速度**：MIDAS 文件一次拿全球（5.4 MB），不必逐站下时序。
- **单站日坐标**：tenv3（最终）+ rapids（最近约 60 天）拼起来。
- **亚日形变 / 地震同震**：kenv 5 分钟（最终版按年 zip，快速版近 60 天）。
- **GNSS 水汽 / ZTD 对照**：trop zip（历史年份；当年暂无）。
- **需要原始 RINEX 自己解**：不在 NGL（MAGNET 除外），去 IGS / 区域网。
