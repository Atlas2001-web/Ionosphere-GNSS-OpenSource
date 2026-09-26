# quakeion · 震例 → USGS 目录 + CODE GIM + Kp/Dst 匿名下载与 ROT/ROTI 图 操作手册

目录：[`PROJECTS.json` → `quakeion`](../../PROJECTS.json) · 上游 <https://github.com/Gm015555/quakeion> · **MIT** · PyPI **0.1.1**（2026-07-09 01:33 EDT 上传，唯一版本）· main tip **`8c4d05f`**（2026-07-09 05:29 EDT，之后无提交）· ★0 / fork 0 / issue 0 · Python ≥3.9 · 本机实跑 **2026-09-26 06:08–06:17 EDT**（CPython 3.13.5 venv：numpy 2.5.3 / pandas 3.0.6 / matplotlib 3.11.2 / requests 2.34.2 / unlzw3 0.2.3）

> 一句话：给一个地名 + 年份，它去 **USGS FDSN** 查地震，挑最近的 3 个内置 IGS 站坐标，从 **CODE** 下载每天的 GIM（IONEX），在这几个点上插值出 TEC，算 ROT/ROTI 和逐日 σ 超限，再用 **GFZ Kp** + **京都 WDC Dst** 标地磁暴日，画 4 张 PNG。所有数据源都不要账号。
> **但 0.1.1 写死的 CODE 地址 `http://ftp.aiub.unibe.ch/CODE` 已不响应，不打补丁 GIM 一张也下不到**（见 §3）。
> 邻居：GIM 各中心路径/时延 → [gim-product-portals](./gim-product-portals.md)；Kp/Dst 等指数 → [pysatspaceweather](./pysatspaceweather.md)、[geomagindices](./geomagindices.md)；测站级 ROTI 要从 RINEX 算，不是本工具。

## 1. 它是什么 / 不是什么

| 是 | 不是 |
| --- | --- |
| 匿名数据拉取 + 画图脚手架：USGS 地震目录、CODE GIM、Kp、Dst，四个源都免登录 | **不是测站 TEC**：所谓“最近的站”只是 `stations.py` 里 48 个 IGS 站的近似坐标，TEC 是在 GIM 格网（2.5°×5°、1 h）上双线性插值 |
| ROT = 相邻历元 TEC 差 / 分钟；ROTI = ROT 的 4 点滑动标准差；每天单独算均值 ±1σ/±2σ 分级 | 不做前兆判断：只统计超限个数 |
| GIM 缓存到 `~/.quakeion/cache/gim_YYYY-MM-DD.inx`（解压后 IONEX，约 1.7 MB/天） | 不读 RINEX，不出 GeoTIFF/NetCDF（README 路线图里才有） |

## 2. 安装

```bash
python3 -m venv ~/qi && ~/qi/bin/pip install --no-cache-dir quakeion      # 依赖 requests numpy pandas matplotlib unlzw3
export MPLBACKEND=Agg                                                    # 无显示器时
```

- 可选 `quakeion[maps]` 会装 cartopy；本机没装，`report()` 的两张空间 ROTI 图照样能画（纯 matplotlib）。
- 上游 3 个测试文件不在 wheel 里；用 `gh api repos/Gm015555/quakeion/contents/tests/<f>.py` 拿下来跑：**29 passed in 1.05 s**（离线，只测 IONEX 解析、ROT/ROTI、参数构造）。

## 3. 必打补丁：换 CODE 地址

```python
import sys, quakeion as qi
sys.modules["quakeion.tec"].CODE_BASE = "https://download.aiub.unibe.ch/CODE"   # 301 到 Switch S3，requests 自动跟随
```

本机实测（06:08 EDT）：

```text
curl http://ftp.aiub.unibe.ch/CODE/            → TCP 80 能连上，但不回任何 HTTP（curl 25 s 超时；WebFetch 从另一网络也超时）
requests.get(旧地址, timeout=15)               → ReadTimeout 15.1 s
curl -L https://download.aiub.unibe.ch/CODE/2025/COD0OPSFIN_20253410000_01D_01H_GIM.INX.gz
                                               → 200，344715 B，2.5 s（落到 zhw-b.s3.cloud.switch.ch/aiub/CODE/...）
```

不打补丁时：每天 4 个候选 URL，每个 `timeout=120` 读超时 → 一天约 8 分钟后打印 `WARNING: no GIM available`；`report()` 默认 ±15 天 = 31 天，算下来要空等约 4 小时才报 `RuntimeError: Could not download any Global Ionosphere Maps`。

**坑：** `import quakeion.tec as T` 拿到的是**函数** `tec`，不是模块（`__init__.py` 里 `from .tec import tec` 把同名属性覆盖了）。`T.CODE_BASE = ...` 不报错也不生效，本机就这样白等了 100 s。必须用 `sys.modules["quakeion.tec"]`。

## 4. 最小可复现（每步都是本机真实输出）

### 4.1 查地震（USGS FDSN，geojson）

```python
eq = qi.earthquakes(region="japan", min_mag=7.0, start="2025-01-01", end="2025-12-31")
```
```text
                              time  latitude  longitude  depth_km  magnitude                                     place          id
0 2025-12-08 14:15:09.896000+00:00   40.9984   142.1836     40.72        7.6  2025 Aomori Prefecture, Japan Earthquake  us6000rtdt
```

`region` 可用名字（`qi.REGIONS` 共 19 个框，含 `world`）或 `(min_lat, max_lat, min_lon, max_lon)`；也可 `lat/lon/radius_km`（默认 500 km）。默认 `limit=500`，按时间倒序。

### 4.2 震中 TEC（±1 天 = 3 个 GIM 文件）

```python
tec = qi.tec((40.9984, 142.1836, "2025-12-08T14:15:09Z"), window_days=1)
r = qi.rot(tec); ro = qi.roti(r); ex = qi.exceedance(ro)
```
```text
  downloaded GIM for 2025-12-07 (COD0OPSFIN_20253410000_01D_01H_GIM.INX.gz)
  downloaded GIM for 2025-12-08 (COD0OPSFIN_20253420000_01D_01H_GIM.INX.gz)
  downloaded GIM for 2025-12-09 (COD0OPSFIN_20253430000_01D_01H_GIM.INX.gz)
(72, 1)
2025-12-07 00:00:00+00:00  24.34
2025-12-07 12:00:00+00:00   6.39
2025-12-08 00:00:00+00:00  21.88
2025-12-08 12:00:00+00:00   7.31
ROT max 0.131  ROTI max 0.082        (TECU/min)
exceed 1σ/2σ 21 3
```

缓存目录 3 个文件：1694119 / 1694605 / 1694119 B。传元组时 `attrs['magnitude']`、`place` 是 `None`；传 `eq.iloc[0]` 才带震级。

### 4.3 地磁暴筛查

```python
k = qi.kp("2025-12-07", "2025-12-09");  qi.storm_days(k)        # Kp ≥ 5
d = qi.dst("2025-12-07", "2025-12-09"); qi.dst_storm_days(d)    # Dst ≤ −50 nT
```
```text
kp rows 17  first 2025-12-07 00:00  last 2025-12-09 00:00  storm []
dst rows 73 min -12.0 storm []
```

Kp 走 `https://kp.gfz-potsdam.de/app/json/`（现 301 到 `kp.gfz.de`，requests 自动跟随），失败才退到 NOAA SWPC（只有近一个月）。Dst 依次试京都 `dst_final` → `dst_provisional` → `dst_realtime`：2025-12 的 final 是 404，用的是 provisional。

### 4.4 一键出图

```python
qi.report("japan 2025", min_mag=7.0, window_days=1, outdir="out")
```
```text
Selected: M7.6  2025 Aomori Prefecture, Japan Earthquake  (2025-12-08 14:15:09.896000+00:00)
  station: TSKB  Tsukuba, Japan  |  573 km
  station: USUD  Usuda, Japan  |  635 km
  station: SHAO  Shanghai, China  |  2176 km
  storm days (Kp>=5): none
  storm days (Dst<=-50 nT): none
  ...（ROTI 一轮同上）
Figures written:
  out/japan_2025_rot_timeseries.png        295382 B
  out/japan_2025_roti_timeseries.png       313586 B
  out/japan_2025_roti_map_eventday.png     174915 B
  out/japan_2025_roti_map_daybefore.png    191484 B
```

第二次调用全部命中缓存（10 s 内完成）。默认 `window_days=15` 要下 31 天 GIM，约 11 MB 压缩、缓存 52 MB。

### 4.5 旧短名和快速产品

```text
2016-04-15 → 候选 COD0OPSFIN_…gz / CODG1060.16I.Z / COD0OPSRAP_… / CORG1060.16I.Z → 实际命中 CODG1060.16I.Z（unlzw3 解 .Z），25 张图，格网 71×73
2026-09-24 → 最终产品还没出，命中 COD0OPSRAP_20262670000_01D_01H_GIM.INX.gz（快速），25 张图
```

## 5. 输出字段

| 函数 | 返回 | 列 / 单位 |
| --- | --- | --- |
| `earthquakes()` | DataFrame，新→旧 | `time`(UTC) `latitude` `longitude` `depth_km` `magnitude` `place` `id` |
| `tec()` | DataFrame，索引 UTC，默认 60 min 步长 | `tec`（TECU）；`attrs` 存 lat/lon/event_time/magnitude/place |
| `rot()` / `roti()` | 同索引 | `rot` / `roti`（TECU/min） |
| `exceedance()` | 原列 + | `day_mean` `s1_low` `s1_high` `s2_low` `s2_high` `sigma_class`(0/1/2)；`attrs['n_exceed_1sigma'/'n_exceed_2sigma']` |
| `kp()` / `dst()` | 3 h / 1 h | `kp` / `dst`（nT） |
| `report()` | dict | `event` `files` `catalog` |

## 6. 坑

| # | 现象 | 原因 | 处理 |
| ---: | --- | --- | --- |
| 1 | GIM 全下不到，长时间无输出 | `CODE_BASE` 旧 HTTP 地址挂起，每 URL 等 120 s | §3 补丁 |
| 2 | 改了 `CODE_BASE` 没用 | `quakeion.tec` 属性被函数覆盖 | 用 `sys.modules["quakeion.tec"]` |
| 3 | 3 个“站”的曲线几乎一样 | 同一 GIM 格网插值；TSKB 与 USUD 相距约 150 km，本机一天内 TEC 差最大 0.76 TECU，ROT 相关系数 0.997 | 别把它当 3 个独立观测 |
| 4 | 最后一天的 Kp 只有 00:00 一个值 | `kp(start, end)` 把 end 当 `end 00:00` 发给 GFZ（本机 07–09 只回 17 行，应为 24） | 自己调时把 end 加一天；`analyze()` 里暴日筛查也受影响，最后一天的磁暴可能漏标 |
| 5 | 近期日期一直用快速产品 | 缓存文件名只有日期，不分 FIN/RAP；一旦存了快速版就不会再换 | 最终产品出来后（CODE 约 3–4 天）删掉 `~/.quakeion/cache/gim_<日期>.inx` |
| 6 | 缓存越堆越大 | `~/.quakeion/cache` 不清理，1.7 MB/天 | 定期删；或临时设 `HOME` |
| 7 | `report("venezuela")` 能用，`report("peru 2007")` 用的是南美大框 | 地名只查 19 个框 + 4 个别名，选的是框内当年**最大**震级 | 精确事件直接传 `qi.tec(eq.iloc[i])` / `qi.analyze(event=...)` |
| 8 | 暴日判定和文献不一致 | 阈值写死：Kp ≥ 5、Dst ≤ −50 nT；`dst_storm_days(threshold=-30)` 可改，`analyze()` 不暴露参数 | 自己调 `storm_days` / `dst_storm_days` |
| 9 | 老月份 Dst 拿不到 | 京都 final 只到有定稿的年份；`dst_realtime/202507/` 本机 403 | 看报错，必要时改用 [pysatspaceweather](./pysatspaceweather.md) |

## 7. 选型

| 需求 | 用 |
| --- | --- |
| 快速看某次大地震前后 GIM 尺度 TEC/ROTI + 暴日标注，不想注册任何账号 | **本工具**（打 §3 补丁） |
| 测站级 ROTI（1 Hz/30 s RINEX） | 从 RINEX 自算；不是本工具 |
| 多中心 GIM 对比、时延 | [gim-product-portals](./gim-product-portals.md) |

## 8. 参考

- 仓库：<https://github.com/Gm015555/quakeion> · PyPI：<https://pypi.org/project/quakeion/>
- USGS FDSN event：<https://earthquake.usgs.gov/fdsnws/event/1/>
- CODE 下载：<https://download.aiub.unibe.ch/CODE/>（301 到 S3，无目录索引）
- GFZ Kp：<https://kp.gfz.de/> · 京都 WDC Dst：<https://wdc.kugi.kyoto-u.ac.jp/>
