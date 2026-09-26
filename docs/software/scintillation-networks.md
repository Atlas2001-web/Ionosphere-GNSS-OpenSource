# 闪烁监测网（CHAIN 以外）· INGV eSWua / Madrigal / UNESP ISMR

入口：INGV eSWua 闪烁 web service <http://ws-eswua.rm.ingv.it/swit/scintillation/records/wsstation>（落地页 <http://www.eswua.ingv.it/ewphp/landing.php?doi=gnss>，接口说明 `web_service.php`）· Madrigal CEDAR `kinst=8010`「GNSS Scintillation Network」<https://cedar.openmadrigal.org/> · UNESP ISMR Query Tool <https://ismrquerytool.fct.unesp.br/> · 本机验证 **2026-09-26 06:19–06:27 EDT**（匿名：eSWua 全程无账号；Madrigal 只列元数据不下载；UNESP 与 LISN 只探首页）

> 岗位：拿 **S4 / σφ 这类 1 分钟闪烁指数**（不是 50 Hz 原始相位）。CHAIN 高纬 ISMR 见 [chain-scintillation.md](./chain-scintillation.md)，UNESP 账号版命令行见 [ismr-downloader.md](./ismr-downloader.md)，本文不重复这两篇。门槛总表 [电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E34](../data-access.md#dp-e34) · 冲突时以决策表和各站点当日实际返回为准。

---

## 1 用途与边界

| 做 | 不做 |
|---|---|
| eSWua：站表 JSON、按时间段取某站 1 分钟逐星记录（S4、σφ 1/3/10/30/60 s、TEC、仰角方位、IPP） | 不做 50 Hz 高频原始数据（eSWua / ISMR 都不公开给匿名用户） |
| Madrigal kinst 8010：列实验、文件和参数，说明怎么接 [madrigal.md](./madrigal.md) | 不代填 Madrigal 下载要的姓名 / 邮箱 / 单位 |
| UNESP ISMR / LISN：如实写出门槛 | 不注册 UNESP 账号，不绕 Cloudflare Turnstile |

**结论先说**

| 需求 | 走哪 | 门槛 |
|---|---|---|
| 欧洲 / 地中海 / 南北极 / 东南亚 / 非洲 / 南美多站 S4、σφ，要机器可读 | **eSWua web service** | 匿名 |
| 加拿大高纬 ISMR | [CHAIN](./chain-scintillation.md) | 匿名 |
| 巴西低纬（CIGALA / CALIBRA 网） | UNESP ISMR：[ismr-downloader](./ismr-downloader.md) | **要 UNESP 账号**（邮箱 + 密码） |
| 多网合并的 S4 / σφ HDF5（每日一个文件） | Madrigal kinst 8010 | 列表匿名；下载要填姓名/邮箱/单位 |
| 秘鲁 LISN | — | 本机探测不可达（http 超时，https 403） |

## 2 安装

不用装东西：`curl` 加标准库 Python（`urllib`、`json`）就够了。Madrigal 的下载客户端见 [madrigal.md](./madrigal.md)。

```bash
unset TMPDIR VIRTUAL_ENV LD_LIBRARY_PATH   # 本机习惯：清掉继承的环境变量
/usr/bin/python3 --version                 # 本机 3.x，只用标准库
```

## 3 真命令 + 期望输出

### 3.1 eSWua：站表、2024-05-10 暴时两站 2 小时、最新数据时延

```python
# eSWua（INGV）闪烁 web service：站表、2024-05-10 暴时两站 2 h、最新数据时延；Madrigal kinst 8010 只列参数
import json, urllib.request, collections, datetime as dt, statistics, time
W = 'http://ws-eswua.rm.ingv.it/swit/scintillation/records'   # 落地页给的 scintillation.php/… 会 302 到这里
def get(u, t=120):
    t0 = time.time()
    with urllib.request.urlopen(u, timeout=t) as r: b = r.read()
    return json.loads(b)['records'], len(b), time.time() - t0
st, nb, sec = get(f'{W}/wsstation')
print(f'wsstation: {len(st)} 站（{nb:,} B，{sec:.1f} s）；状态 {dict(collections.Counter(x["status"] for x in st))}；接收机 {dict(collections.Counter(x["instrument"] for x in st))}')
for code in ('nya1p', 'lam0p'):
    info = next(x for x in st if x['code'] == code)
    q = f'{W}/ws{code}?filter=dt,bt,2024-05-10%2022:00:00,2024-05-10%2023:59:00&size=20000'
    r, nb, sec = get(q)
    mins = sorted({x['dt'] for x in r}); sats = {x['PRN'] for x in r}
    good = [x for x in r if (x['elevation'] or 0) >= 30 and (x['locktimel1'] or 0) >= 240]
    s4 = [x['totals4l1'] for x in good if x['totals4l1'] is not None]; ph = [x['phi60l1slant'] for x in good if x['phi60l1slant'] is not None]
    top = max(good, key=lambda x: x['phi60l1slant'] or 0)
    print(f'\n{code} {info["name"]}（{float(info["lat"]):.1f}°N, {info["instrument"]}）2024-05-10 22:00–23:59 UT：{len(r)} 条，{len(r[0])} 个字段，{len(mins)} 个分钟，{len(sats)} 颗星（{nb:,} B，{sec:.1f} s）')
    print(f'  仰角≥30° 且 L1 锁定≥240 s（本文过滤）: {len(good)} 条；totalS4 L1 中位 {statistics.median(s4):.3f} 最大 {max(s4):.3f}；phi60 L1 中位 {statistics.median(ph):.3f} rad 最大 {max(ph):.3f} rad '
          f'@ {top["dt"]} {top["PRN"]}；phi60>0.5 rad 的条数 {sum(p > 0.5 for p in ph)}（本文阈值）')
print('\n字段样例（lam0p 第一条的键）:', ', '.join(sorted(r[0].keys())))
r, nb, sec = get(f'{W}/wslyb0p?filter=dt,ge,2026-09-26%2010:00:00&size=20000')
last = max(x['dt'] for x in r); mod = max(x['modified'] for x in r)
print(f'\n时延：lyb0p 2026-09-26 10:00 UT 以后 {len(r)} 条，最新 dt = {last}，最新 modified = {mod}（探测时刻 {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC）')
```

实测输出（2026-09-26 06:25–06:27 EDT）：

```text
wsstation: 42 站（15,700 B，0.4 s）；状态 {'Closed': 11, 'Active': 28, 'Installing': 3}；接收机 {'Septentrio PolaRx5S': 28, 'Novatel GSV4004': 8, 'Septentrio PolaRxS': 4, 'Novatel GPStation-6': 2}

nya1p Ny Alesund（78.9°N, Septentrio PolaRx5S）2024-05-10 22:00–23:59 UT：5181 条，75 个字段，120 个分钟，57 颗星（7,595,618 B，2.8 s）
  仰角≥30° 且 L1 锁定≥240 s（本文过滤）: 2332 条；totalS4 L1 中位 0.057 最大 0.220；phi60 L1 中位 0.103 rad 最大 0.652 rad @ 2024-05-10 22:29:00 R05；phi60>0.5 rad 的条数 11（本文阈值）

lam0p Lampedusa（35.5°N, Septentrio PolaRx5S）2024-05-10 22:00–23:59 UT：6084 条，75 个字段，120 个分钟，62 颗星（8,790,196 B，2.9 s）
  仰角≥30° 且 L1 锁定≥240 s（本文过滤）: 2419 条；totalS4 L1 中位 0.042 最大 0.983；phi60 L1 中位 0.033 rad 最大 1.055 rad @ 2024-05-10 22:20:00 R15；phi60>0.5 rad 的条数 2（本文阈值）

字段样例（lam0p 第一条的键）: PRN, averagel1, avg_c_n0_l2c, avg_c_n0_l5, avgccd_l2c, avgccd_l5, avgccdl1, avgcn2freqtec, azimuth, correctionS4_L2C, corrections4_l5, corrections4l1, dt, dtec0, dtec30_15, dtec45_30, dtec60_45, elevation, ipp_lat, ipp_lon, locktime_l2c, locktime_l5, locktimel1, modified, p_l2c, p_l5, phi01_l2c, phi01_l5, phi01l1, phi03_l2c, phi03_l5, phi03l1, phi10_l2c, phi10_l5, phi10l1, phi30_l2c, phi30_l5, phi30l1, phi60_l1_vert, phi60_l2_vert, phi60_l2c, phi60_l5, phi60_l5_vert, phi60l1slant, pl1, reserved, rxstate, s4_l1_slant, s4_l1_vert, s4_l2_slant, s4_l2_vert, s4_l5_slant, secondlocktime, si_l1_29, si_l1_30, si_l2c_43, si_l2c_44, si_l5_57, si_l5_58, sigmaccd_l2c, sigmaccd_l5, sigmaccdl1, stec, svid, t_l1, t_l2c, t_l5, tec0, tec15, tec30, tec45, totals4_l2c, totals4_l5, totals4l1, vtec

时延：lyb0p 2026-09-26 10:00 UT 以后 678 条，最新 dt = 2026-09-26 10:15:00，最新 modified = 2026-09-26 10:15:31（探测时刻 2026-09-26 10:26 UTC）
```

读法：
- 两站在 22:00–23:59 UT 的 120 个分钟都有数据，**每颗星每分钟一条**。PRN 字段带星座前缀（`G05`、`R15`…）。
- 高纬 nya1p 以相位闪烁为主：phi60 中位 0.103 rad，是 lam0p 的 3 倍。中纬 lam0p 出现了单条 S4 0.983 和 phi60 1.055 rad，是孤立尖峰。要不要当真，得看同星前后几分钟和锁定时间（本文未进一步判别）。
- 时延：探测时刻 10:26 UTC，最新一条是 10:15 UT，`modified` 在 10:15:31。和接口说明的“1 分钟分辨率、每 15 分钟更新”一致，也就是 **15 分钟一批**。

### 3.2 其他来源：Madrigal、UNESP、LISN

```bash
#!/usr/bin/env bash
# 其他 S4/σφ 来源：Madrigal kinst 8010 / SCINDA、UNESP ISMR Query Tool、LISN
M=https://cedar.openmadrigal.org
echo "Madrigal 闪烁类仪器: $(curl -s $M/getInstrumentsService.py | grep -c 'Scintillation') 个（其中 SCINDA $(curl -s $M/getInstrumentsService.py | grep -c 'SCINDA Scintillation Receiver,')）"
curl -s -m 90 "$M/getExperimentsService.py?code=8010&startyear=2024&startmonth=5&startday=10&starthour=0&startmin=0&startsec=0&endyear=2024&endmonth=5&endday=12&endhour=0&endmin=0&endsec=0&local=1" | cut -d, -f1,2 | sed 's|https://cedar.openmadrigal.org/madtoc/||'
f=$(curl -s -m 90 "$M/getExperimentFilesService.py?id=100184961" | cut -d, -f1)
echo "文件: ${f##*/}（kindat/说明: $(curl -s -m 90 "$M/getExperimentFilesService.py?id=100184961" | cut -d, -f3)）"
echo "参数（只列不下载）: $(curl -s -m 90 "$M/getParametersService.py?filename=$f" | cut -d'\' -f1 | tr '\n' ' ')"
curl -s -o /dev/null -m 30 -w '%{http_code} -> %{redirect_url}\n' http://ismrquerytool.fct.unesp.br/
curl -s -o /dev/null -m 30 https://ismrquerytool.fct.unesp.br/; echo "https 严格校验: curl exit $?（60 = 证书链不全）"
curl -sk -m 30 https://ismrquerytool.fct.unesp.br/ | grep -oE '<title>[^<]*|turnstile|<div id="root">' | tr '\n' ' '; echo "（-k 只看首页：SPA + Cloudflare Turnstile）"
for u in http://lisn.igp.gob.pe/ https://lisn.igp.gob.pe/; do echo "$(curl -s -o /dev/null -m 30 -w '%{http_code} %{time_total}s' $u) $u"; done
echo "ismr-downloader（PyPI）: $(/usr/bin/python3 -m pip index versions ismr-downloader 2>/dev/null | head -1)；需 --email/--password（UNESP 账号，见 ismr-downloader 手册）"
```

实测输出：

```text
Madrigal 闪烁类仪器: 56 个（其中 SCINDA 53）
100184967,experiments/2024/sci/10may24
100184961,experiments/2024/sci/11may24
100184964,experiments/2024/sci/12may24
文件: scin_20240511.001.hdf5（kindat/说明: Ionospheric scintillation）
参数（只列不下载）: YEAR MONTH DAY HOUR MIN SEC RECNO KINDAT KINST UT1_UNIX UT2_UNIX GPS_SITE SAT_ID GNSS_TYPE PIERCE_ALT GDLATR GDLONR AZM ELM S4_SCIN SIGMA_PHI S4_SCIN_LOS SIGMA_PHI_LOS GDLAT GLON BMONTH BDAY MD DAYNO BHM BHHMMSS EHHMMSS UTH B_UTH UT BEG_UT SLT FYEAR JULIAN_DATE SZEN SDWHT UT1 UT2 DUT21 DST KP AP AP3 F10.7 FBAR BXGSM BYGSM BZGSM BIMF BXGSE BYGSE BZGSE SWDEN SWSPD SWQ 
301 -> https://ismrquerytool.fct.unesp.br/
https 严格校验: curl exit 60（60 = 证书链不全）
turnstile <title>ISMR Query Tool <div id="root"> （-k 只看首页：SPA + Cloudflare Turnstile）
000 30.001500s http://lisn.igp.gob.pe/
403 2.287066s https://lisn.igp.gob.pe/
ismr-downloader（PyPI）: ismr-downloader (0.2.0)；需 --email/--password（UNESP 账号，见 ismr-downloader 手册）
```

## 4 输入 / 输出

| 来源 | 形态 | 采样 | 关键字段 |
|---|---|---|---|
| eSWua `ws<code>` | JSON `{"records":[…]}`，一条 = 一站 × 一星 × 一分钟，75 个字段（PolaRx5S） | 1 min；每 15 min 入库一批 | `dt`（UT，分钟起点）、`PRN`、`elevation`、`azimuth`、`ipp_lat/ipp_lon`、`totals4l1`（总 S4）、`corrections4l1`（噪声修正项）、`s4_l1_slant/vert`、`phi01l1…phi30l1`、`phi60l1slant`、`phi60_l1_vert`、L2C/L5 同名字段、`locktimel1`、`averagel1`（C/N0）、`tec0…tec45`、`stec/vtec`、`modified`（入库时间） |
| eSWua `wsstation` | JSON 站表，42 站 | — | `code`、`name`、`instrument`、`lat/lon`、`status`（Active / Closed / Installing）、`active_since/until`、`area`、`host_institution` |
| Madrigal kinst 8010 | 每日一个 `scin_YYYYMMDD.001.hdf5` | 本文未下载，未实测 | `GPS_SITE`、`SAT_ID`、`GNSS_TYPE`、`S4_SCIN`、`SIGMA_PHI`、`S4_SCIN_LOS`、`SIGMA_PHI_LOS`、`PIERCE_ALT`、`GDLATR/GDLONR`、`ELM/AZM` |
| UNESP ISMR | Septentrio ISMR CSV（格式同 CHAIN，见 [chain-scintillation.md](./chain-scintillation.md)） | 1 min / 星 | 需账号，本文未取数 |

## 5 参数（eSWua 查询串）

| 参数 | 例 | 说明 |
|---|---|---|
| `filter=dt,bt,A,B` | `dt,bt,2024-05-10%2022:00:00,2024-05-10%2023:59:00` | 闭区间；空格写成 `%20` |
| `filter=dt,eq,T` / `dt,ge,T` | `dt,ge,2026-09-26%2010:00:00` | 单个时刻 / 某时刻以后 |
| `size=N` | `size=20000` | **是硬上限**：结果超过 N 条时静默截断，不报错 |
| `order=dt,desc` | — | 不加 filter 时会全表排序，本机 61 s 后返回 502，不要单独用 |
| 过滤口径 | 仰角 ≥ 30°、`locktimel1` ≥ 240 s | 本文自选，用来剔除低仰角多路径和刚锁定的尖峰 |

## 6 接到哪一步

- 闪烁 / ROTI 入门：[教程 05](../tutorials/05-scintillation-roti.md)。eSWua 的 `phi60l1slant`、`totals4l1` 可以直接和自算 ROTI 放在同一张图上。
- 闪烁建模：[教程 13](../tutorials/13-scintillation-modeling.md)。用实测 S4 / σφ 给模型定标。
- 暴时对照：[教程 20](../tutorials/20-storm-tec-analysis.md)（2024-05-10/11）。
- 高纬补站：CHAIN（[chain-scintillation.md](./chain-scintillation.md)）加 eSWua 的 nya / lyb / thu / sod / pal，就能覆盖北极多个扇区。
- 仿真对照：[iono-scintillation.md](./iono-scintillation.md)，给定 S4 合成信号。

## 7 坑

| # | 现象 | 原因 | 修复 |
|---|---|---|---|
| 1 | `?size=1&order=dt,desc` 等 61 s 后 502 | 没有 filter 时服务端全表排序 | 永远带 `filter=dt,…` 时间窗 |
| 2 | 查“最新数据”得到 10:00，实际已有 10:15 | `size=5000` 把 08:00 以后的结果截断了，而且不报错 | 缩短时间窗，或检查返回条数是否正好等于 `size` |
| 3 | `status` 是 Active 但查不到今天的数据 | lam0p 标 Active，但本机最近有数据的一天是 2026-09-20；pru2p 在探测的几天都没数据 | 取数前先按日探一条 |
| 4 | 说明页写 39 个站端点，`wsstation` 返回 42 站 | 站表含 Installing / Closed，还有测试站 `tes0p` | 以 `wsstation` 为准，并过滤 `status` |
| 5 | 单条 S4≈1、phi60>1 rad 的孤立尖峰 | 低仰角、刚锁定、周跳 | 按本文口径过滤仰角和 `locktimel1`，再看同星连续性 |
| 6 | 同名字段有 `totals4l1` / `s4_l1_slant` / `corrections4l1` | 总 S4、修正后 S4、噪声修正项不是一个量 | 做对比时写明用的是哪一个；本文统计用 `totals4l1` |
| 7 | 落地页 `landing.php?doi=gnss` 抓下来是空壳 | 页面内容靠 JS 填充 | 直接用文档化的 `ws-eswua.rm.ingv.it/swit/scintillation/records/…` |
| 8 | UNESP https `curl` exit 60 | 服务器证书链不全；首页是 SPA + Cloudflare Turnstile | 数据走 [ismr-downloader](./ismr-downloader.md)（要账号）；不要用 `-k` 绕过登录 |
| 9 | Madrigal 下载报缺 user 字段 | CEDAR 要求填姓名 / 邮箱 / 单位 | 列表和参数可以匿名查；下载按 [madrigal.md](./madrigal.md) 自行填写 |
| 10 | `dt` 当成本地时间 | 全部是 UT；`modified` 同样是 UT | 统一按 UTC 解析 |
| 11 | GLONASS 星的 PRN 是 `R05` 而不是数字 | 多星座混排 | 按首字母分星座；GLONASS 频分，S4 阈值和 GPS 不能简单套用 |

## 8 选型

| 场景 | 选 |
|---|---|
| 匿名、多站、脚本化、近实时（15 min） | eSWua |
| 加拿大高纬原始 ISMR 文件 | [CHAIN](./chain-scintillation.md) |
| 巴西低纬，能接受注册 | [ismr-downloader](./ismr-downloader.md) |
| 多网合一的 HDF5，愿意填 Madrigal 用户信息 | Madrigal kinst 8010（[madrigal.md](./madrigal.md)） |
| 秘鲁 LISN | 本机不可达，暂不推荐 |
