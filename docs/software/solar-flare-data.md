# 耀斑驱动数据匿名获取：GOES XRS（NCEI science / 运行 / SWPC JSON）与 SDO EVE、FISM2（LISIRD）——2024-05-11 X5.8 实测

入口：[NCEI GOES-R XRS L2](https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/data/) · [XRS L2 ReadMe](https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/docs/GOES-R_XRS_L2_Data_ReadMe.pdf) · [SWPC 事件表归档](https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/solar_event_reports/) · [SWPC JSON goes/](https://services.swpc.noaa.gov/json/goes/) · [LISIRD LaTiS](https://lasp.colorado.edu/lisird/latis/dap/) · [EVE data access](https://lasp.colorado.edu/eve/data_access/) · 本机验证 **2026-09-26 05:59–06:06 EDT**（匿名，未注册任何账号；UTC = EDT + 4 h）

> 岗位：回答“分析耀斑 TEC 突增（[教程 23](../tutorials/23-flare-eclipse-special.md#3-耀斑突然电离因果链)）时，X 射线 / EUV 驱动数据不登录去哪拿、用哪颗星哪个版本、时间怎么对齐”。以 2024-05-11 X5.8（01:10 起、01:23 峰，AR 3664）为例：先查耀斑表，再拉 GOES-16 与 GOES-18 的 science（`sci_`）和运行（`dn_`）两个版本，再拉 FISM2 与 EVE 看 EUV 增强。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E31](../data-access.md#dp-e31) · 相关：[地磁 / 空间天气（Kp / SWPC）](../data-access.md#地磁--空间天气kp--swpc)、[E16 SWPC JSON](../data-access.md#dp-e16)
>
> 冲突时：卫星 / 版本差异以 NCEI XRS L2 ReadMe 与 User's Guide（v2-2-1，2025-12-15）为准；“耀斑前均值 = 00:40–01:05 UT 平均”“峰只在 01:05–02:00 里找”“×0.7 换算成旧口径等级”都是**本文口径**。

## 1. 用途与边界

**做：** 耀斑表去哪查；GOES XRS 1 s / 1 min / 耀斑汇总的匿名路径；GOES-16 与 GOES-18、science 与运行版、SWPC 实时 JSON 的差别；SWPC 0.7 缩放因子的来历；FISM2 与 SDO EVE 的 EUV 时间序列怎么拿，一次真实个例的数值。

**不做：** TEC 本身的解算（→ [教程 23](../tutorials/23-flare-eclipse-special.md)、[realtime-iono-products](./realtime-iono-products.md)）；Kp / Dst 等地磁指数（→ [geomagindices](./geomagindices.md)、[geomag-api](./geomag-api.md)）；SUVI 图像、SEISS 粒子；JSOC 的 AIA 图像。

**结论先说：**

| 要什么 | 去哪（匿名） | 格式 / 时间分辨 | 本次实测 |
| --- | --- | --- | --- |
| **耀斑表（先查这个）** | SWPC 编辑事件表 `ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/solar_event_reports/YYYY/MM/YYYYMMDDevents.txt`（近期也在 `ftp.swpc.noaa.gov/pub/indices/events/`） | 文本，每行一事件，`XRA 1-8A` 为 X 射线耀斑 | 2024-05 X 级 XRA 21 行；05-11：X5.8（01:10/01:23/01:39，G16，AR 3664）和 X1.5 |
| **XRS science 版（做研究用这个）** | NCEI `…/goes/goesNN/l2/data/xrsf-l2-{flx1s,avg1m,flsum}_science/YYYY/MM/sci_xrsf-l2-*_gNN_dYYYYMMDD_v2-2-1.nc` | netCDF4（HDF5），1 s / 1 min / 耀斑事件 | G16 1 s 峰 5.865e-4 W/m² @ 01:22:50；flsum 给 X5.8 |
| XRS 运行版 | 同一树去掉 `_science` 后缀，文件前缀 `dn_` | 同上 | G16 1 s 峰 5.938e-4（比 sci 高 1.2%，按 1 s 截断成 X5.9） |
| 实时（近 7 天） | SWPC `services.swpc.noaa.gov/json/goes/{primary,secondary}/xrays-{6-hour,1-day,3-day,7-day}.json`；耀斑 `xray-flares-7-day.json` | JSON，1 min | 现在 **primary = GOES-18、secondary = GOES-19**；7 天 9978 条/通道（少 102 min） |
| **FISM2**（经验模型谱） | LISIRD LaTiS `lasp.colorado.edu/lisird/latis/dap/fism_flare_hr.csv?…`（0.1 nm，60 s）、`fism_flare_bands`（23 个光化学波段，**300 s**） | CSV / JSON / netCDF，时间为儒略日 | 0.05–0.4 nm ×72、29–32 nm ×1.46、30.4 nm 峰 01:20:03；最新只到 **2026-09-18 23:59** |
| **SDO EVE**（实测） | LISIRD `sdo_eve_diodes_l2b`、`sdo_eve_lines_l2b`、`sdo_eve_bands_l2b`；原始文件 `lasp.colorado.edu/eve/data_access/` | CSV，60 s（L2B 经 LaTiS），时间为 TAI 秒 | ESP 0.1–7 nm ×16.1 @ 01:23:30；**λ < 37 nm 的 29 条谱线 26 条全程 −1**（MEGS-A 2014 年起缺） |

GOES-16 与 GOES-18 版本差别（本次 2024-05-11 同一耀斑）：

| 项 | GOES-16 | GOES-18 | 说明 |
| --- | --- | --- | --- |
| 当时角色 | primary（事件表 `Obs` 列 = G16） | secondary | primary/secondary 是 SWPC 的**运行指派**，文件里没有这个字段；看事件表的 `Obs` 列或 SWPC JSON 的 `satellite` |
| science 1 min 峰 → 等级 | 5.821e-4 → **X5.8** | 5.760e-4 → **X5.7** | 官方等级按 primary 的 1 min 值截断 |
| 同日第二个 X 级（flsum） | sci X1.5 / dn X1.5 | **sci X1.4** / dn X1.5 | 版本不同，等级可跨 0.1 |
| NCEI science 覆盖 | 2017-02-07 至 **2025-04-07**（任务合并文件 `…_s20170209_e20250406_v2-2-1.nc`） | 2022-06-17 至今 | 2025-04 以后用 G18 / G19 |
| 缩放因子 | 无（真实 W/m²） | 无 | 0.7 / 0.85 只存在于 GOES 8–15 的运行数据 |

## 2. 安装

`curl`；Python 3 + `h5py`（XRS 文件是 netCDF4 = HDF5；本机 `/usr/bin/python3` 没有 netCDF4/h5py，装到临时目录，不动系统）。FISM2 / EVE 走 LaTiS 的 CSV，只用标准库。

```bash
/usr/bin/python3 -m pip install -q --target ./pylib h5py    # 本机实测装到 h5py 3.16.0（连带 numpy 2.5.3 进 ./pylib）
PYTHONPATH=./pylib /usr/bin/python3 -c "import h5py; print(h5py.__version__)"
```

## 3. 真命令 + 期望输出

### 3.1 先查耀斑表，再拉 12 个 XRS 文件（`get.sh`）

```bash
#!/usr/bin/env bash
# 1) 先查耀斑表（SWPC 编辑事件表，NCEI 归档）；2) 拉 GOES-16/18 XRS L2：sci_（science）与 dn_（运行）各 3 个产品
E=https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/solar_event_reports/2024/05
for d in $(seq -w 1 31); do curl -s $E/202405${d}events.txt | awk -v d=$d '/XRA/ && / X[0-9]/{print "2024-05-"d, $0}'; done | tee xflares.txt | grep -c XRA | sed 's/^/2024-05 X 级 XRA 事件数: /'
grep -E '2024-05-11' xflares.txt
B=https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes
for s in 16 18; do for p in flx1s avg1m flsum; do
  curl -s -o sci_xrsf-l2-${p}_g${s}_d20240511_v2-2-1.nc -w "%{http_code} %{size_download} B  sci g$s $p\n" $B/goes$s/l2/data/xrsf-l2-${p}_science/2024/05/sci_xrsf-l2-${p}_g${s}_d20240511_v2-2-1.nc
  curl -s -o dn_xrsf-l2-${p}_g${s}_d20240511_v2-2-1.nc  -w "%{http_code} %{size_download} B  dn  g$s $p\n" $B/goes$s/l2/data/xrsf-l2-${p}/2024/05/dn_xrsf-l2-${p}_g${s}_d20240511_v2-2-1.nc
done; done
echo "GOES-16 science 任务合并文件: $(curl -s $B/goes16/l2/data/xrsf-l2-flsum_science/ | grep -o 'sci_xrsf-l2-flsum_g16_s[0-9]*_e[0-9]*_v[0-9-]*\.nc' | sort -u)"
echo "GOES-18 science 最新日文件: $(curl -s $B/goes18/l2/data/xrsf-l2-flx1s_science/2026/09/ | sed 's/<[^>]*>/ /g' | grep '\.nc' | tail -1 | tr -s ' ')"
echo "GOES-18 运行   最新日文件: $(curl -s $B/goes18/l2/data/xrsf-l2-flx1s/2026/09/ | sed 's/<[^>]*>/ /g' | grep '\.nc' | tail -1 | tr -s ' ')"
```

实测输出（06:04 EDT，空目录）：

```text
2024-05 X 级 XRA 事件数: 21
2024-05-11 1680 +     0110   0123      0139  G16  5   XRA  1-8A      X5.8    6.4E-01   3664
2024-05-11 1860 +     1115   1144      1205  G16  5   XRA  1-8A      X1.5    2.6E-01   3664
200 3420163 B  sci g16 flx1s
200 3274832 B  dn  g16 flx1s
200 302286 B  sci g16 avg1m
200 303335 B  dn  g16 avg1m
200 43623 B  sci g16 flsum
200 44743 B  dn  g16 flsum
200 3393999 B  sci g18 flx1s
200 3212796 B  dn  g18 flx1s
200 301758 B  sci g18 avg1m
200 302878 B  dn  g18 avg1m
200 43293 B  sci g18 flsum
200 44413 B  dn  g18 flsum
GOES-16 science 任务合并文件: sci_xrsf-l2-flsum_g16_s20170209_e20250406_v2-2-1.nc
GOES-18 science 最新日文件:  sci_xrsf-l2-flx1s_g18_d20260925_v2-2-1.nc 2026-09-26 04:17 3.4M 
GOES-18 运行   最新日文件:  dn_xrsf-l2-flx1s_g18_d20260925_v2-2-1.nc 2026-09-26 04:16 2.9M 
```

读法：事件表 `Begin/Max/End` 为 UT；`Obs` = G16 表示当时 SWPC 用 GOES-16 定级；`6.4E-01` 是积分通量（J/m²）。05-08 有一条同起止时间的重复编辑记录（600 与 620），21 行不等于 21 个不同耀斑。ReadMe 写 science 版“延迟三天”，但本次 NCEI 目录里 GOES-18 的 9 月 25 日 science 和运行文件都在 09-26 04:16–04:17 上架（目录页时间未标时区），即约 1 天。

### 3.2 两颗星 × 两个版本 × 1 s / 1 min（`xrs.py`）

```python
# GOES-16 / GOES-18 XRS 2024-05-11 X5.8 耀斑：science(sci_) vs 运行(dn_)，1 s vs 1 min，flsum 耀斑表
import h5py, numpy as np, datetime as dt
T0 = dt.datetime(2000, 1, 1, 12)
def t(x): return T0 + dt.timedelta(seconds=float(x))
def cls(f):   # SWPC 口径：截断而非四舍五入
    for L, b in (('X', 1e-4), ('M', 1e-5), ('C', 1e-6), ('B', 1e-7), ('A', 1e-8)):
        if f >= b: return f'{L}{int(f / b * 10) / 10:.1f}'
w0, w1 = dt.datetime(2024, 5, 11, 1, 0), dt.datetime(2024, 5, 11, 2, 0)
for s in (16, 18):
    print(f'===== GOES-{s}')
    for ver in ('sci', 'dn'):
        for p in ('flx1s', 'avg1m'):
            f = h5py.File(f'{ver}_xrsf-l2-{p}_g{s}_d20240511_v2-2-1.nc')
            tt = np.array([t(x) for x in f['time'][:]]); m = (tt >= w0) & (tt < w1)
            b = f['xrsb_flux'][:][m]; fl = f['xrsb_flags'][:][m] if 'xrsb_flags' in f else f['xrsb_flag'][:][m]
            ok = (b > 0) & (fl == 0); i = np.argmax(np.where(ok, b, -1))
            pc = f['xrsb_primary_chan'][:][m] if 'xrsb_primary_chan' in f else None
            pcs = '' if pc is None else f' primary_chan 取值 {sorted(set(pc.tolist()))}（峰值时 B{pc[i]}）'
            print(f'{ver:3s} {p}: N={m.sum():5d} 好数据 {ok.sum():5d}  XRS-B 峰 {b[i]:.3e} W/m² @ {tt[m][i]:%H:%M:%S}  → {cls(b[i])}；×0.7 → {cls(0.7 * b[i])}{pcs}')
    for ver in ('sci', 'dn'):
        f = h5py.File(f'{ver}_xrsf-l2-flsum_g{s}_d20240511_v2-2-1.nc')
        st = [x.decode() if isinstance(x, bytes) else x for x in f['status'][:]]
        fc = [x.decode() if isinstance(x, bytes) else x for x in f['flare_class'][:]]
        for k in range(len(st)):
            tk = t(f['time'][k])
            if w0 <= tk < w1: print(f'  {ver} flsum {tk:%H:%M} {st[k]:12s} {fc[k]:5s} xrsb={f["xrsb_flux"][k]:.3e} id={f["flare_id"][k]}')
        print(f'  {ver} flsum 全天 EVENT_PEAK 数 = {st.count("EVENT_PEAK")}；X 级 = {[c for s_, c in zip(st, fc) if s_ == "EVENT_PEAK" and c.startswith("X")]}')
    g = h5py.File(f'sci_xrsf-l2-flx1s_g{s}_d20240511_v2-2-1.nc'); print(f'  sci 文件: date_created={g.attrs["date_created"].decode() if isinstance(g.attrs["date_created"], bytes) else g.attrs["date_created"]} L1b={g.attrs["L1b_system_environment"].decode()}')
    g = h5py.File(f'dn_xrsf-l2-flx1s_g{s}_d20240511_v2-2-1.nc'); print(f'  dn  文件: date_created={g.attrs["date_created"].decode() if isinstance(g.attrs["date_created"], bytes) else g.attrs["date_created"]} L1b={g.attrs["L1b_system_environment"].decode()}')
```

实测输出：

```text
===== GOES-16
sci flx1s: N= 3600 好数据  3600  XRS-B 峰 5.865e-04 W/m² @ 01:22:50  → X5.8；×0.7 → X4.1 primary_chan 取值 [1, 2]（峰值时 B2）
sci avg1m: N=   60 好数据    60  XRS-B 峰 5.821e-04 W/m² @ 01:23:00  → X5.8；×0.7 → X4.0
dn  flx1s: N= 3600 好数据  3600  XRS-B 峰 5.938e-04 W/m² @ 01:22:50  → X5.9；×0.7 → X4.1 primary_chan 取值 [1, 2]（峰值时 B2）
dn  avg1m: N=   60 好数据    60  XRS-B 峰 5.893e-04 W/m² @ 01:23:00  → X5.8；×0.7 → X4.1
  sci flsum 01:10 EVENT_START        xrsb=9.801e-06 id=202405110110
  sci flsum 01:23 EVENT_PEAK   X5.8  xrsb=5.821e-04 id=202405110110
  sci flsum 01:38 EVENT_END          xrsb=2.862e-04 id=202405110110
  sci flsum 全天 EVENT_PEAK 数 = 11；X 级 = ['X5.8', 'X1.5']
  dn flsum 01:10 EVENT_START        xrsb=9.801e-06 id=202405110110
  dn flsum 01:23 EVENT_PEAK   X5.8  xrsb=5.893e-04 id=202405110110
  dn flsum 01:38 EVENT_END          xrsb=2.900e-04 id=202405110110
  dn flsum 全天 EVENT_PEAK 数 = 11；X 级 = ['X5.8', 'X1.5']
  sci 文件: date_created=2025-12-05T18:31:58.678Z L1b=SCI
  dn  文件: date_created=2025-12-04T18:56:13.192Z L1b=OE
===== GOES-18
sci flx1s: N= 3600 好数据  3600  XRS-B 峰 5.801e-04 W/m² @ 01:22:49  → X5.8；×0.7 → X4.0 primary_chan 取值 [1, 2]（峰值时 B2）
sci avg1m: N=   60 好数据    60  XRS-B 峰 5.760e-04 W/m² @ 01:23:00  → X5.7；×0.7 → X4.0
dn  flx1s: N= 3600 好数据  3600  XRS-B 峰 5.800e-04 W/m² @ 01:22:49  → X5.7；×0.7 → X4.0 primary_chan 取值 [1, 2]（峰值时 B2）
dn  avg1m: N=   60 好数据    60  XRS-B 峰 5.759e-04 W/m² @ 01:23:00  → X5.7；×0.7 → X4.0
  sci flsum 01:10 EVENT_START        xrsb=9.714e-06 id=202405110110
  sci flsum 01:23 EVENT_PEAK   X5.7  xrsb=5.760e-04 id=202405110110
  sci flsum 01:38 EVENT_END          xrsb=2.837e-04 id=202405110110
  sci flsum 全天 EVENT_PEAK 数 = 10；X 级 = ['X5.7', 'X1.4']
  dn flsum 01:10 EVENT_START        xrsb=9.714e-06 id=202405110110
  dn flsum 01:23 EVENT_PEAK   X5.7  xrsb=5.759e-04 id=202405110110
  dn flsum 01:38 EVENT_END          xrsb=2.839e-04 id=202405110110
  dn flsum 全天 EVENT_PEAK 数 = 10；X 级 = ['X5.7', 'X1.5']
  sci 文件: date_created=2026-01-16T09:39:14.843Z L1b=SCI
  dn  文件: date_created=2026-01-16T06:49:33.181Z L1b=OE
```

读法：

- **1 s 与 1 min**：G16 science 1 s 峰 5.865e-4 @ 01:22:50，1 min 峰 5.821e-4 @ 01:23:00（1 min 值低 0.75%）。官方等级用 1 min 值，所以研究定级读 `avg1m` 或 `flsum`，TEC 对时用 `flx1s`。
- **science 与运行**：G16 运行版比 science 高约 1.2%（1 s 5.938e-4 vs 5.865e-4），1 s 值截断后成 X5.9；G18 两版几乎相同（5.800e-4 vs 5.801e-4），但第二个耀斑 flsum 给 X1.4（sci）/ X1.5（dn）。ReadMe 说明：science 版用随时间变化的暗电流和新定标，运行版用固定暗电流，两者“一般不相同”。
- **primary_chan**：峰值时 XRS-B 由 B2（高通量传感器）给出；B 通道在 1e-4 W/m² 切换，所以 X 级耀斑一定跨了 B1→B2。用合并好的 `xrsb_flux`，不要自己拿 `xrsb1_flux` 算峰。
- **×0.7**：把 GOES-R 值乘 0.7 得到“按 GOES 8–15 运行口径会报出的等级”：X5.8 → X4.0/X4.1（本文换算）。User's Guide 的例子是 GOES-15 运行报 X2.5 相当于 GOES-R 的 X3.6（1/0.7 ≈ 1.43）。和旧耀斑统计对比时要先统一口径。
- 两版文件的 `date_created` 都在 2025-12 至 2026-01：**运行版 `dn_` 在 NCEI 上也被重新生成过**（文件名同为 `v2-2-1`），`L1b_system_environment` 一个是 `SCI`，一个是 `OE`。

### 3.3 SWPC 实时 JSON：现在谁是 primary（`swpc.py`）

```python
# SWPC 实时 JSON：primary / secondary 现在是哪颗星（只保留近 7 天）
import json, urllib.request, collections
for k in ('primary', 'secondary'):
    d = json.load(urllib.request.urlopen(f'https://services.swpc.noaa.gov/json/goes/{k}/xrays-7-day.json'))
    print(k, len(d), '条', d[0]['time_tag'], '→', d[-1]['time_tag'], dict(collections.Counter((x['satellite'], x['energy']) for x in d)))
    print('   字段:', list(d[-1].keys()))
d = json.load(urllib.request.urlopen('https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json'))
print('xray-flares-7-day:', len(d), '条；最大:', max((x for x in d if x['max_xrlong']), key=lambda x: x['max_xrlong'])['max_class'], '；max_xrlong 为 null 的', sum(x['max_xrlong'] is None for x in d), '条（进行中）', '；卫星', sorted({x['satellite'] for x in d}))
```

实测输出（06:04 EDT）：

```text
primary 19956 条 2026-09-19T10:03:00Z → 2026-09-26T09:59:00Z {(18, '0.05-0.4nm'): 9978, (18, '0.1-0.8nm'): 9978}
   字段: ['time_tag', 'satellite', 'flux', 'observed_flux', 'electron_correction', 'electron_contaminaton', 'energy']
secondary 19956 条 2026-09-19T10:02:00Z → 2026-09-26T09:59:00Z {(19, '0.05-0.4nm'): 9978, (19, '0.1-0.8nm'): 9978}
   字段: ['time_tag', 'satellite', 'flux', 'observed_flux', 'electron_correction', 'electron_contaminaton', 'energy']
xray-flares-7-day: 33 条；最大: C3.7 ；max_xrlong 为 null 的 1 条（进行中） ；卫星 [18]
```

JSON 里 `flux` 是扣除电子污染后的值，`observed_flux` 是原始值；字段名 `electron_contaminaton` 原文就拼错了。JSON 只保留 7 天，**2024 年个例只能走 NCEI 文件**。

### 3.4 EUV：FISM2 与 SDO EVE（`euv.py`）

```python
# 2024-05-11 X5.8：LISIRD LaTiS 匿名拉 FISM2 flare bands + SDO EVE ESP 二极管 / 谱线，算增强比与峰时
import urllib.request, csv, io, datetime as dt, statistics
L = 'https://lasp.colorado.edu/lisird/latis/dap/'
W = '&time>=2024-05-11T00:30&time<2024-05-11T02:30'
def get(ds, cols):
    u = f'{L}{ds}.csv?{cols}{W}'
    with urllib.request.urlopen(u, timeout=120) as r: b = r.read()
    rows = list(csv.reader(io.StringIO(b.decode())))
    print(f'{ds}: {len(rows) - 1} 行, {len(b):,} B')
    return rows[0], rows[1:]
jd = lambda x: dt.datetime(2024, 5, 11) + dt.timedelta(days=float(x) - 2460441.5)
tai = lambda x: dt.datetime(1958, 1, 1) + dt.timedelta(seconds=float(x) - 37)   # TAI−UTC = 37 s（2017 起）
def ratio(name, tt, v, pre=(dt.datetime(2024, 5, 11, 0, 40), dt.datetime(2024, 5, 11, 1, 5))):
    ok = [(t, x) for t, x in zip(tt, v) if x > 0]
    base = statistics.mean(x for t, x in ok if pre[0] <= t < pre[1])
    tp, xp = max(((t, x) for t, x in ok if pre[1] <= t < dt.datetime(2024, 5, 11, 2, 0)), key=lambda p: p[1])   # 峰只在 01:05–02:00 里找
    print(f'  {name:18s} 耀斑前均值 {base:.3e}  峰 {xp:.3e} @ {tp:%H:%M:%S}  增强 ×{xp / base:.2f}')
h, r = get('fism_flare_bands', 'time,E0_05_0_4,E0_8_1_8,E3_2_7_0,E7_0_15_5,E15_5_22_4,E29_0_32_0,E54_0_65_0,E97_5_98_7')
tt = [jd(x[0]) for x in r]; print(f'  时间步 {(tt[1] - tt[0]).total_seconds():.0f} s，首 {tt[0]:%H:%M:%S} 末 {tt[-1]:%H:%M:%S}（单位 photons/cm²/s）')
for j in range(1, len(h)): ratio(h[j].split(' ')[0], tt, [float(x[j]) for x in r])
h, r = get('fism_flare_hr', 'time,wavelength,irradiance&wavelength>30.3&wavelength<30.5')
for wl in sorted({x[1] for x in r}):
    sub = [x for x in r if x[1] == wl]; tt = [jd(x[0]) for x in sub]
    ratio(f'FISM2 {wl} nm', tt, [float(x[2]) for x in sub])
print(f'  fism_flare_hr 时间步 {(tt[1] - tt[0]).total_seconds():.0f} s（W/m²/nm，0.1 nm 分辨）')
h, r = get('sdo_eve_diodes_l2b', 'time,diodeQuad,diode171,diode304,diode366')
tt = [tai(x[0]) for x in r]; print(f'  时间步 {(tt[1] - tt[0]).total_seconds():.0f} s，首 {tt[0]:%H:%M:%S} 末 {tt[-1]:%H:%M:%S}（W/m²；diodeQuad = ESP 0.1–7 nm）')
for j in range(1, len(h)): ratio(h[j].split(' ')[0], tt, [float(x[j]) for x in r])
h, r = get('sdo_eve_lines_l2b', 'time')
with urllib.request.urlopen(f'{L}sdo_eve_lines_l2b.csv?{W[1:]}', timeout=120) as q: rows = list(csv.reader(io.StringIO(q.read().decode())))
names = [c.split(' ')[0] for c in rows[0][1:]]
fill = {n: sum(float(x[i + 1]) < 0 for x in rows[1:]) for i, n in enumerate(names)}
short = [n for n in names if n.count('_') >= 2 and n.split('_')[-1].isdigit() and int(n.split('_')[-1]) < 370]
print(f'  EVE L2B 谱线 {len(names)} 条；λ < 37 nm 的 {len(short)} 条中全程为 −1（缺测）的 {sum(fill[n] == len(rows) - 1 for n in short)} 条；例 He_II_304 缺 {fill.get("He_II_304")}/{len(rows) - 1}，Fe_XVI_335 缺 {fill.get("Fe_XVI_335")}/{len(rows) - 1}')
```

实测输出：

```text
fism_flare_bands: 24 行, 4,637 B
  时间步 300 s，首 00:30:00 末 02:25:00（单位 photons/cm²/s）
  E0_05_0_4          耀斑前均值 3.319e+05  峰 2.396e+07 @ 01:25:00  增强 ×72.18
  E0_8_1_8           耀斑前均值 1.166e+08  峰 5.704e+08 @ 01:25:00  增强 ×4.89
  E3_2_7_0           耀斑前均值 1.257e+09  峰 1.612e+09 @ 01:25:00  增强 ×1.28
  E7_0_15_5          耀斑前均值 2.138e+09  峰 7.042e+09 @ 01:25:00  增强 ×3.29
  E15_5_22_4         耀斑前均值 1.042e+10  峰 1.199e+10 @ 01:19:59  增强 ×1.15
  E29_0_32_0         耀斑前均值 1.132e+10  峰 1.657e+10 @ 01:19:59  增强 ×1.46
  E54_0_65_0         耀斑前均值 7.783e+09  峰 9.476e+09 @ 01:19:59  增强 ×1.22
  E97_5_98_7         耀斑前均值 9.488e+09  峰 1.788e+10 @ 01:19:59  增强 ×1.88
fism_flare_hr: 240 行, 11,021 B
  FISM2 30.35 nm     耀斑前均值 5.225e-03  峰 7.890e-03 @ 01:20:03  增强 ×1.51
  FISM2 30.45 nm     耀斑前均值 1.101e-03  峰 1.697e-03 @ 01:20:03  增强 ×1.54
  fism_flare_hr 时间步 60 s（W/m²/nm，0.1 nm 分辨）
sdo_eve_diodes_l2b: 120 行, 12,139 B
  时间步 60 s，首 00:29:30 末 02:28:30（W/m²；diodeQuad = ESP 0.1–7 nm）
  diodeQuad          耀斑前均值 7.070e-04  峰 1.138e-02 @ 01:23:30  增强 ×16.09
  diode171           耀斑前均值 1.273e-03  峰 1.480e-03 @ 01:24:30  增强 ×1.16
  diode304           耀斑前均值 1.139e-03  峰 1.429e-03 @ 01:24:30  增强 ×1.25
  diode366           耀斑前均值 1.585e-04  峰 2.054e-04 @ 01:53:30  增强 ×1.30
sdo_eve_lines_l2b: 120 行, 1,716 B
  EVE L2B 谱线 213 条；λ < 37 nm 的 29 条中全程为 −1（缺测）的 26 条；例 He_II_304 缺 120/120，Fe_XVI_335 缺 0/120
```

读法（时间都已换成 UTC）：

- 软 X 射线端（FISM2 0.05–0.4 nm ×72、0.8–1.8 nm ×4.9；EVE ESP 0.1–7 nm ×16）峰在 01:23–01:25，和 XRS 同步。这一段主要在 D/E 区沉积。
- 30.4 nm 等 EUV 峰更早（FISM2 01:20:03；FISM2 波段 29–32 nm 01:19:59）但增幅只有 ×1.2–1.5。F 区 TEC 突增主要由这一段驱动，所以 **TEC 突增的起跳时刻按 EUV 对齐，不要只按 XRS 峰对齐**。EVE ESP 304 二极管峰在 01:24:30，和 FISM2 相差约 4 min：FISM2 是由 GOES XRS 等代理量推出来的模型，不是实测。
- `fism_flare_bands` 在 LISIRD 是 **300 s** 一点，`fism_flare_hr` 是 60 s；做分钟级对时用 `_hr`。
- EVE 谱线：MEGS-A（5–37 nm）2014 年起无数据，2024 年 λ < 37 nm 的谱线里只有 Fe XVI 33.5/36.1 nm 和 Mg IX 36.8 nm 有值（MEGS-B 覆盖），He II 30.4 nm 全是 −1。30.4 nm 只能用 ESP 304 二极管（宽带）或 FISM2。
- ESP 366 二极管在窗口开头就有 2.9e-4 的尖峰（没有限定窗口时它被当成“峰”），限定窗口后也只有 ×1.30，峰在 01:53:30。这个通道噪声大，别用它。

### 3.5 LISIRD 数据更新到哪天（`lat.sh`）

```bash
#!/usr/bin/env bash
# LISIRD 各数据集最新时刻（LaTiS 必须带时间下限；last() 取末条）
L=https://lasp.colorado.edu/lisird/latis/dap
for d in fism_flare_bands fism_flare_hr fism_daily_hr; do
  echo "$d 末条: $(curl -s -m 90 "$L/$d.csv?time&time>=2026-09-01&last()" | tail -1)"
done
for day in 2026-09-26 2026-09-25 2026-09-24; do
  echo "sdo_eve_diodes_l2b $day 12:00–12:05: $(curl -s -m 60 "$L/sdo_eve_diodes_l2b.csv?time,diodeQuad&time>=${day}T12:00&time<${day}T12:05" | tail -n +2 | wc -l) 行"
done
echo "不带时间下限: $(curl -s -m 60 "$L/fism_flare_hr.csv?time&last()" | tr -d '\n' | cut -c1-120)"
```

实测输出（06:05 EDT）：

```text
fism_flare_bands 末条: 2461302.496527778
fism_flare_hr 末条: 2461302.4993402776
fism_daily_hr 末条: 2026267
sdo_eve_diodes_l2b 2026-09-26 12:00–12:05: 0 行
sdo_eve_diodes_l2b 2026-09-25 12:00–12:05: 0 行
sdo_eve_diodes_l2b 2026-09-24 12:00–12:05: 5 行
不带时间下限: time (Julian Date)2461302.4993402776
```

儒略日 2461302.4993 = **2026-09-18 23:59 UTC**：FISM2 flare 落后约 7 天；`fism_daily_hr` 到 2026267（09-24）；EVE L2B 到 09-24。实时耀斑监测只能用 SWPC JSON。

## 4. 输入 / 输出

| 数据 | 关键变量 | 时间基准 | 填充值 |
| --- | --- | --- | --- |
| XRS `flx1s` / `avg1m` | `xrsa_flux`、`xrsb_flux`（W/m²，primary 合并）、`xrsb_flags`（0 = good）、`xrsb_primary_chan` | `time` = 2000-01-01 12:00 UTC 起的秒，**不计闰秒** | −9999 |
| XRS `flsum` | `status`（EVENT_START/PEAK/END）、`flare_class`、`flare_id`（YYYYMMDDHHMM）、`integrated_flux` | 同上 | `''` / −9999 |
| SWPC JSON | `time_tag`（ISO Z）、`satellite`、`flux`、`observed_flux`、`energy`（`0.1-0.8nm` = XRS-B） | UTC | — |
| FISM2（LaTiS） | `irradiance`（W/m²/nm）或波段光子通量（photons/cm²/s） | 儒略日 | — |
| EVE L2B（LaTiS） | `diodeQuad`、`diode304`…（W/m²）；谱线名如 `He_II_304`（数字为 Å） | TAI 秒，自 1958-01-01（减 37 s 得 UTC） | −1 |

## 5. 参数（查询 / 选择）

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| 卫星 `gNN` | g16（至 2025-04-07）、g17（至 2023-01-10）、g18（2022-06-17 起）、g19（2024-09-20 起） | 来自 ReadMe 表 1 |
| 版本前缀 | `sci_`（目录 `_science`）/ `dn_`（L2 运行）/ `ops_`（L1b 运行） | 研究用 `sci_` |
| 版本号 | `v2-2-1`（2025-12-15 发布） | 历史版本 2-2-0、2-1-0、2-0-1；2-0-1 修正 1 s 时间戳 0.516 s |
| LaTiS 查询 | `ds.csv?col1,col2&time>=…&time<…`；`&last()`；可把 `.csv` 换成 `.json`/`.nc` | `.das` 等元数据请求不带时间时报 `requires a minimum time selection` |
| 耀斑前均值窗口 | 00:40–01:05 UT | **本文自选** |

## 6. 接到哪一步

- 耀斑 TEC 突增分析（[教程 23 §3](../tutorials/23-flare-eclipse-special.md#3-耀斑突然电离因果链)、[耀斑套清单](../tutorials/23-flare-eclipse-special.md#耀斑套清单)）：XRS `flx1s` 定峰、FISM2/EVE 定 EUV 起跳，再和 1 s–30 s 采样的 GNSS TEC 画在同一时间轴上（观测数据见 [cors-networks](./cors-networks.md)、[gnss-obs-mirrors](./gnss-obs-mirrors.md)；近实时 TEC 见 [realtime-iono-products](./realtime-iono-products.md)）。
- 地磁背景（同一天正是 2024-05-10/11 大磁暴）：[geomagindices](./geomagindices.md)、data-access [地磁 / 空间天气](../data-access.md#地磁--空间天气kp--swpc)。
- 模型输入：FISM2 波段可直接喂 TIE-GCM / GITM 类模型（`fism_flare_bands` 就是这 23 个波段）。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 同一耀斑 G16 说 X5.8、G18 说 X5.7 | 两星定标不同；官方等级只按当时 primary 定 | 引用等级时写明卫星；对比用同一颗星 |
| 2 | 1 s 峰截断成 X5.9，事件表是 X5.8 | 等级定义用 1 min 平均值，且截断不四舍五入 | 定级用 `avg1m` / `flsum`；1 s 只用来对时 |
| 3 | science 与运行版数值不同（G16 差 1.2%），flsum 等级能差 0.1 | 暗电流处理与定标不同 | 研究一律用 `sci_…_science`；运行版只做实时参考 |
| 4 | 和 2017 年前耀斑比，GOES-R 的等级“偏大” | GOES 8–15 运行数据被 SWPC 乘了 0.7（B）/0.85（A）去对齐 GOES-7；GOES-R 不乘 | 统一口径：GOES-R 值 ×0.7 对比旧运行等级，或改用重处理过的 GOES 8–15 science 数据（同为真实 W/m²） |
| 5 | XRS-A 与旧星比大约 41% | ReadMe 注意事项 1：GOES-R / GOES-15 的 XRS-A 比约 1.41，原因未明（B 通道没有这个差） | 用 XRS-B 定级；A/B 比值（温度）跨代不可直接比 |
| 6 | 自己用 `xrsb1_flux` 算出 X 级耀斑峰被截平 | B1 是低通量传感器，1e-4 W/m² 以上切到 B2 | 用合并好的 `xrsb_flux`，并看 `xrsb_primary_chan` |
| 7 | 文件里找不到“primary/secondary” | 这是 SWPC 的运行指派，随时间变（本次实时 primary 是 GOES-18、secondary 是 GOES-19） | 历史看事件表 `Obs` 列；实时看 JSON 的 `satellite` |
| 8 | GOES-16 2025-04 以后没数据 | science 覆盖到 2025-04-07 | 换 g18 / g19 |
| 9 | 时间差 37 s 或 0.5 s | XRS `time` 不计闰秒；EVE LaTiS 用 TAI；v2-0-1 以前 1 s 时间戳偏 0.516 s | 按第 4 节换算；只用 v2-2-1 |
| 10 | EVE 30.4 nm 谱线全是 −1 | MEGS-A 2014 年起失效，λ < 37 nm 谱线基本无值 | 用 ESP `diode304` 或 FISM2 |
| 11 | FISM2 峰比 EVE 早 4 min | FISM2 是代理模型，不是实测 | 定时刻用实测（XRS / ESP），FISM2 用来要谱形 |
| 12 | `fism_flare_bands` 只有 5 min 一点 | LISIRD 上这个数据集就是 300 s | 分钟级用 `fism_flare_hr`（60 s） |
| 13 | 昨天的 FISM2 查不到 | 本次 flare 版只到 2026-09-18 23:59 UTC（约 7 天延迟） | 实时用 SWPC JSON；FISM2 用于事后分析 |
| 14 | 2024 年的 SWPC JSON 找不到 | JSON 只保留 7 天 | 历史走 NCEI 文件 |
| 15 | ReadMe 说 science 延迟 3 天，实际 1 天 | 文档与实际不符（本次 09-25 文件 09-26 04:17 已在） | 以目录为准，不要按 3 天写死 |
| 16 | `import netCDF4` 失败 | 系统 Python 没装 | `pip install --target ./pylib h5py`，用 h5py 读（netCDF4 即 HDF5） |

## 8. 选型

- **耀斑定级、对比多个耀斑**：NCEI `xrsf-l2-flsum_science` + `avg1m_science`，写明卫星。
- **TEC 突增对时**：`flx1s_science`（1 s）+ EVE ESP（60 s）；FISM2 `fism_flare_hr` 要谱形。
- **实时监测**：SWPC JSON `primary/xrays-6-hour.json` + `xray-flares-latest.json`。
- **和 2017 年前的耀斑比**：GOES 8–15 重处理 science 数据（NCEI GOES 1–15 页面），或把 GOES-R ×0.7，不要直接混用。
