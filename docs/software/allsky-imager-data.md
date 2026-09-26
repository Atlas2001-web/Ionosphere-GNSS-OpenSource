# 全天空成像仪数据匿名获取：THEMIS ASI、REGO（UCalgary / Berkeley）与 MANGO——2024-05-10/11 暴夜实测

入口：[UCalgary 开放数据 sort_by_project](https://data.phys.ucalgary.ca/sort_by_project/) · [Berkeley THEMIS thg/l1/asi](https://themis.ssl.berkeley.edu/data/themis/thg/l1/asi/) · [MANGO 数据服务器](https://data.mangonetwork.org/data/transport/mango/archive/) · 本机验证 **2026-09-26 06:15–06:18 EDT**（匿名，未注册任何账号；UTC = EDT + 4 h）

> 岗位：回答“极光 / 气辉全天空图像不登录去哪拿、每分钟 / 每夜有多少、文件怎么读、像素怎么定位”。以 2024-05-10/11 大磁暴夜为例：THEMIS 与 REGO 都选 Gillam（gill）站，MANGO 选 Capitol Reef（cfs，美国犹他）红线。分析场景对应 [教程 20 磁暴 TEC](../tutorials/20-storm-tec-analysis.md)（极光带扩展、SAR 弧）与 [教程 21 赤道异常与等离子体泡](../tutorials/21-equatorial-anomaly-bubbles.md)（630 nm 暗条纹 = 泡），现象总览见 [教程 19](../tutorials/19-phenomena-overview.md)。
>
> 门槛总表：[电离层与地磁门户决策表](../data-access.md#电离层与地磁门户决策表) · 本文命令块 [E33](../data-access.md#dp-e33) · 同一台站的磁强计见 [E12 THEMIS GMAG](../data-access.md#dp-e12)
>
> 冲突时：以各服务器当时的目录为准（只代表 2026-09-26 这一次）；“全图均值最亮时刻”“计数分位数”是**本文口径**，不是定标后的亮度。

## 1. 用途与边界

**做：** 三个网的匿名路径、文件粒度（每分钟 / 每小时 / 每夜）、格式（多帧 PGM、CDF、HDF5、IDL `.sav` skymap）、一夜的文件数、样本读取与定位。

**不做：** 绝对定标（Rayleigh）、拼图 / 投影算法、极光分类。Python 封装库 `pyaurorax`（PyPI 1.26.0）与 `asilib`（0.30.1）本次**没有安装测试**，只列出。

**结论先说：**

| 网 | 匿名路径 | 粒度 / 格式 | 2024-05-11 实测 |
| --- | --- | --- | --- |
| **THEMIS ASI**（白光，UCalgary） | `data.phys.ucalgary.ca/sort_by_project/THEMIS/asi/stream0/YYYY/MM/DD/<站>_themisNN/utHH/YYYYMMDD_HHMM_<站>_themisNN_full.pgm.gz` | 每分钟 1 个 gzip 多帧 PGM：20 帧 × 3 s，256×256，16 bit，约 2 MB | 11 个站目录；gill 03–08 UT 共 249 个文件（整小时目录 61 个 = 60 个分钟文件 + 1 个每小时 `…_HH_…_row2.pgm.gz`） |
| THEMIS ASI（Berkeley CDF） | `themis.ssl.berkeley.edu/data/themis/thg/l1/asi/<站>/YYYY/MM/thg_l1_as{f,t}_<站>_…_v01.cdf` | `asf` 每小时全帧 CDF（gill 本夜 27–124 MB/h）；`ast` 每日 32×32 缩略图（2.6 MB） | 24 个站目录；ast 4797 张，04:13–08:13 UT |
| **REGO**（630.0 nm，UCalgary） | `…/GO-Canada/REGO/stream0/YYYY/MM/DD/<站>_rego-NNN/utHH/YYYYMMDD_HHMM_<站>_rego-NNN_6300.pgm.gz` | 每分钟 20 帧 × 3 s（曝光 2 s），512×512，16 bit，约 7 MB | 3 个站（fsmi、gill、luck）；gill 04–08 UT 232 个文件 |
| 像素定位（skymap） | `…/THEMIS/asi/skymaps/<站>/<站>_YYYYMMDD/themis_skymap_…_v02.sav`；REGO 在 `…/REGO/skymap/` | IDL `.sav`（`scipy.io.readsav`） | gill 有 19 个版本，2024-05-11 应该用 `gill_20230922` |
| **MANGO**（美国，630 / 557.7 nm） | `data.mangonetwork.org/data/transport/mango/archive/<站>/{redline,greenline}/{level1,raw,quicklook}/YYYY/DDD/` | level1：每站每夜 1 个 HDF5（红线 96 帧 500×500 uint8，4 min 一帧，已带经纬度网格）；quicklook mp4 / webm | 8 个站有 2024/132 的 level1（红线 5、绿线 4，cfs 两者都有） |

## 2. 安装

`curl`；Python 3 + numpy（系统自带）、`cdflib`、`h5py`（装到临时目录，`--no-deps` 以免带进新 numpy）、`scipy.io.readsav`（系统 scipy）。PGM 用 30 行纯 Python 解析（见 3.2），不需要额外库。

```bash
/usr/bin/python3 -m pip install -q --no-deps --target ./pylib h5py cdflib
```

## 3. 真命令 + 期望输出

### 3.1 一夜的目录规模与样本下载（`night.sh`）

```bash
#!/usr/bin/env bash
# 2024-05-10/11 暴夜：THEMIS ASI / REGO（UCalgary + Berkeley）与 MANGO 的目录规模，再下 4 个样本
U=https://data.phys.ucalgary.ca/sort_by_project
n(){ curl -s -m 60 "$1" | grep -c "$2"; }
echo "## UCalgary 开放数据（stream0 = 原始全分辨率，每分钟一个 .pgm.gz）"
echo "THEMIS 2024-05-11 站目录: $(curl -s $U/THEMIS/asi/stream0/2024/05/11/ | grep -o 'href="[a-z]*_themis[0-9]*/"' | cut -d'"' -f2 | tr -d / | tr '\n' ' ')"
echo "REGO   2024-05-11 站目录: $(curl -s $U/GO-Canada/REGO/stream0/2024/05/11/ | grep -o 'href="[a-z]*_rego-[0-9]*/"' | cut -d'"' -f2 | tr -d / | tr '\n' ' ')"
for h in 03 04 05 06 07 08; do
  echo "UT$h  THEMIS gill: $(n $U/THEMIS/asi/stream0/2024/05/11/gill_themis19/ut$h/ 'href="2024.*pgm.gz"') 个  REGO gill: $(n $U/GO-Canada/REGO/stream0/2024/05/11/gill_rego-652/ut$h/ 'href="2024.*pgm.gz"') 个"
done

echo "## Berkeley THEMIS L1 CDF（asf = 每小时全帧，ast = 每日缩略图）"
curl -s https://themis.ssl.berkeley.edu/data/themis/thg/l1/asi/gill/2024/05/ | sed 's/<[^>]*>/ /g' | grep 20240511 | awk '{print "  "$1, $4}'
echo "## MANGO（data.mangonetwork.org）"
M=https://data.mangonetwork.org/data/transport/mango/archive
for s in $(curl -s $M/ | grep -o 'href="[a-z-]*/"' | cut -d'"' -f2 | tr -d /); do
  r=$(curl -s -m 30 $M/$s/redline/level1/2024/132/ | grep -o 'mango-[a-z-]*-level1-20240511.hdf5' | sort -u); g=$(curl -s -m 30 $M/$s/greenline/level1/2024/132/ | grep -o 'mango-[a-z-]*-level1-20240511.hdf5' | sort -u)
  [ -n "$r$g" ] && echo "  $s: ${r:-无红线} ${g:-无绿线}"
done
echo "## 下载样本"
g(){ curl -s -O -w "%{http_code} %{size_download} B %{time_total}s  %{filename_effective}\n" "$1"; }
g $U/THEMIS/asi/stream0/2024/05/11/gill_themis19/ut06/20240511_0600_gill_themis19_full.pgm.gz
g $U/GO-Canada/REGO/stream0/2024/05/11/gill_rego-652/ut06/20240511_0600_gill_rego-652_6300.pgm.gz
g https://themis.ssl.berkeley.edu/data/themis/thg/l1/asi/gill/2024/05/thg_l1_ast_gill_20240511_v01.cdf
g $M/cfs/redline/level1/2024/132/mango-cfs-redline-level1-20240511.hdf5
# skymap：选“生效日期 ≤ 观测日”的最后一个（本例 20240511）
S=$U/THEMIS/asi/skymaps/gill
d=$(curl -s $S/ | grep -o 'href="gill_[0-9]*/"' | grep -o '[0-9]\{8\}' | awk '$1<=20240511' | tail -1)
f=$(curl -s $S/gill_$d/ | grep -o 'href="themis_skymap[^"]*\.sav"' | cut -d'"' -f2)
echo "skymap 可选: $(curl -s $S/ | grep -o 'href="gill_[0-9]*/"' | wc -l) 个；选 gill_$d"
g "$S/gill_$d/$f"
```

实测输出（06:17 EDT，空目录，约 26 s）：

```text
## UCalgary 开放数据（stream0 = 原始全分辨率，每分钟一个 .pgm.gz）
THEMIS 2024-05-11 站目录: atha_themis02 fsim_themis08 fsmi_themis10 gako_themis20 gill_themis19 kapu_themis21 kuuj_themis13 pina_themis18 rank_themis12 snkq_themis10 tpas_themis05 
REGO   2024-05-11 站目录: fsmi_rego-798 gill_rego-652 luck_rego-654 
UT03  THEMIS gill: 1 个  REGO gill: 0 个
UT04  THEMIS gill: 49 个  REGO gill: 41 个
UT05  THEMIS gill: 61 个  REGO gill: 60 个
UT06  THEMIS gill: 61 个  REGO gill: 60 个
UT07  THEMIS gill: 61 个  REGO gill: 60 个
UT08  THEMIS gill: 16 个  REGO gill: 11 个
## Berkeley THEMIS L1 CDF（asf = 每小时全帧，ast = 每日缩略图）
  thg_l1_asf_gill_2024051104_v01.cdf 95M
  thg_l1_asf_gill_2024051105_v01.cdf 118M
  thg_l1_asf_gill_2024051106_v01.cdf 117M
  thg_l1_asf_gill_2024051107_v01.cdf 124M
  thg_l1_asf_gill_2024051108_v01.cdf 27M
  thg_l1_ast_gill_20240511_v01.cdf 2.6M
## MANGO（data.mangonetwork.org）
  blo: 无红线 mango-blo-greenline-level1-20240511.hdf5
  cfs: mango-cfs-redline-level1-20240511.hdf5 mango-cfs-greenline-level1-20240511.hdf5
  cvo: mango-cvo-redline-level1-20240511.hdf5 无绿线
  eio: mango-eio-redline-level1-20240511.hdf5 无绿线
  low: 无红线 mango-low-greenline-level1-20240511.hdf5
  mto: mango-mto-redline-level1-20240511.hdf5 无绿线
  new: 无红线 mango-new-greenline-level1-20240511.hdf5
  par: mango-par-redline-level1-20240511.hdf5 无绿线
## 下载样本
200 2062433 B 0.691543s  20240511_0600_gill_themis19_full.pgm.gz
200 6936968 B 0.671083s  20240511_0600_gill_rego-652_6300.pgm.gz
200 2744143 B 0.633629s  thg_l1_ast_gill_20240511_v01.cdf
200 16102350 B 0.603622s  mango-cfs-redline-level1-20240511.hdf5
skymap 可选: 19 个；选 gill_20230922
200 3539376 B 0.932140s  themis_skymap_gill_20230922-%2B_v02.sav
```

读法：UCalgary 目录按**日历日（UT）**分，北美夜晚在 UT 03–08 h；THEMIS 每个完整的 `utHH/` 里 61 个文件：60 个分钟文件，加 1 个每小时的 `YYYYMMDD_HH_<站>_themisNN_row2.pgm.gz`（按文件名是每小时一行的汇总，本文未解析）；REGO 没有这个文件，所以是 60 个。批量时按 `_HHMM_` 过滤。Berkeley `asf` 一小时 95–124 MB，一夜一站约 0.5 GB，先用 `ast` 缩略图挑时段。MANGO 每站红线 / 绿线不一定都有：本夜 8 个站里只有 cfs 两条线都有。

### 3.2 读样本与 skymap（`read.py`）

```python
# 读样本：UCalgary 多帧 PGM（THEMIS 白光 / REGO 630 nm）、Berkeley ast CDF、MANGO level1 HDF5
import gzip, glob, re, datetime as dt, numpy as np, cdflib, h5py
def pgm_frames(fn):
    b = gzip.open(fn).read(); i = 0; out = []
    while i < len(b):
        assert b[i:i + 2] == b'P5', b[i:i + 10]; i += 3; meta = {}
        while b[i:i + 1] == b'#':
            j = b.index(b'\n', i); m = re.match(rb'#"([^"]+)" (.*)', b[i:j]); i = j + 1
            if m: meta[m.group(1).decode()] = m.group(2).decode().strip()
        j = b.index(b'\n', i); w, h = map(int, b[i:j].split()); i = j + 1
        j = b.index(b'\n', i); mx = int(b[i:j]); i = j + 1
        nb = w * h * (2 if mx > 255 else 1)
        img = np.frombuffer(b[i:i + nb], '>u2' if mx > 255 else 'u1').reshape(h, w); i += nb
        out.append((meta, img))
    return out
for fn in sorted(glob.glob('*.pgm.gz')):
    fr = pgm_frames(fn); m0 = fr[0][0]
    ts = [dt.datetime.strptime(m['Image request start'][:19], '%Y-%m-%d %H:%M:%S') for m, _ in fr]
    st = np.stack([im for _, im in fr]).astype(float)
    print(f'{fn}: {len(fr)} 帧 {fr[0][1].shape[1]}×{fr[0][1].shape[0]} {m0.get("Pixel depth")}；{ts[0]:%H:%M:%S}→{ts[-1]:%H:%M:%S} 步长 {np.median(np.diff(ts)).total_seconds():.0f} s；'
          f'站 {m0.get("Site unique ID")}/{m0.get("Imager unique ID")} ({m0.get("Geodetic latitude", m0.get("Geographic latitude"))}, {m0.get("Geodetic Longitude", m0.get("Geographic longitude"))})；计数 中位 {np.median(st):.0f} / 99% {np.percentile(st, 99):.0f} / 最大 {st.max():.0f}；曝光 {re.search(r"MSEC=([0-9.]+)", m0.get("Exposure options", m0.get("Exposure Options", ""))).group(1)} ms')
c = cdflib.CDF('thg_l1_ast_gill_20240511_v01.cdf')
t = c.varget('thg_ast_gill_time'); a = c.varget('thg_ast_gill').astype(float)
t0 = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=float(t[0])); t1 = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=float(t[-1]))
mean = a.reshape(len(a), -1).mean(1); k = int(np.argmax(mean))
print(f'thg_l1_ast_gill_20240511_v01.cdf: {len(t)} 张 {a.shape[1]}×{a.shape[2]} 缩略图，{t0:%H:%M:%S}→{t1:%H:%M:%S} UTC，步长中位 {np.median(np.diff(t)):.0f} s；'
      f'全图均值最亮 {mean[k]:.0f} @ {dt.datetime(1970, 1, 1) + dt.timedelta(seconds=float(t[k])):%H:%M:%S}（中位 {np.median(mean):.0f}）')
f = h5py.File('mango-cfs-redline-level1-20240511.hdf5')
ut = f['UnixTime'][:]; im = f['ImageData']; msk = ~f['Mask'][:]   # 注意：Mask=True 是被遮掉的像素（仰角<15°），有效像素要取反
T = [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=float(x)) for x in ut[0]]
mv = np.array([im[i][msk].mean() for i in range(im.shape[0])]); k = int(np.argmax(mv))
el = f['Elevation'][:]; lat = f['Latitude'][:]; lon = f['Longitude'][:]; good = msk
nm = f['SiteInfo/Name'][()]; nm = nm.decode() if isinstance(nm, bytes) else nm
print(f'MANGO {nm} 红线 level1：{im.shape[0]} 帧 {im.shape[1]}×{im.shape[2]} {im.dtype}，{T[0]:%m-%d %H:%M}→{T[-1]:%H:%M} UTC，步长中位 {np.median(np.diff(ut[0])):.0f} s，每帧起止差（UnixTime[1]−[0]）{np.median(ut[1] - ut[0]):.0f} s；'
      f'掩膜内均值最亮 {mv[k]:.1f} @ {T[k]:%H:%M}（中位 {np.median(mv):.1f}）；投影高度 {f["Latitude"].attrs["Projection Altitude"]} km，有效像素（Mask 取反）覆盖 纬 {lat[good].min():.1f}…{lat[good].max():.1f}、经 {lon[good].min():.1f}…{lon[good].max():.1f}；站点 {f["SiteInfo/Coordinates"][:]}')
import scipy.io
sk = scipy.io.readsav(glob.glob('themis_skymap_gill_*.sav')[0])['skymap'][0]
el = sk['FULL_ELEVATION']; alt = sk['FULL_MAP_ALTITUDE']; la = sk['FULL_MAP_LATITUDE'][1, :-1, :-1]; lo = sk['FULL_MAP_LONGITUDE'][1, :-1, :-1]
ok = np.isfinite(el) & (el > 10)
print(f'skymap {sk["SITE_UID"].decode()}/{sk["IMAGER_UID"].decode()} 生成 {sk["GENERATION_INFO"][0][0].decode()}：FULL_ELEVATION {el.shape}，映射高度 {(alt / 1000).astype(int).tolist()} km；'
      f'110 km、仰角>10° 覆盖 纬 {np.nanmin(la[ok]):.1f}…{np.nanmax(la[ok]):.1f}、经 {np.nanmin(lo[ok]) - 360:.1f}…{np.nanmax(lo[ok]) - 360:.1f}（经度按 0–360 存）')
```

实测输出：

```text
20240511_0600_gill_rego-652_6300.pgm.gz: 20 帧 512×512 16 bits；06:00:00→06:00:57 步长 3 s；站 gill/rego-652 (56.376723, -94.643664)；计数 中位 601 / 99% 2256 / 最大 50553；曝光 2000.00 ms
20240511_0600_gill_themis19_full.pgm.gz: 20 帧 256×256 16 bits；06:00:00→06:00:57 步长 3 s；站 gill/themis19 (56.3539, -94.6557)；计数 中位 5042 / 99% 9632 / 最大 65535；曝光 999 ms
thg_l1_ast_gill_20240511_v01.cdf: 4797 张 32×32 缩略图，04:13:15→08:13:03 UTC，步长中位 3 s；全图均值最亮 7496 @ 07:07:36（中位 2394）
MANGO Capitol Reef Field Station 红线 level1：96 帧 500×500 uint8，05-11 04:12→10:32 UTC，步长中位 240 s，每帧起止差（UnixTime[1]−[0]）230 s；掩膜内均值最亮 128.6 @ 07:08（中位 108.3）；投影高度 250.0 km，有效像素（Mask 取反）覆盖 纬 31.6…44.8、经 -119.6…-102.7；站点 [  38.18519974 -111.17890167]
skymap gill/themis19 生成 Wed Nov 20 15:08:46 2024：FULL_ELEVATION (256, 256)，映射高度 [90, 110, 150] km；110 km、仰角>10° 覆盖 纬 52.0…61.0、经 -102.6…-86.3（经度按 0–360 存）
```

读法：

- **多帧 PGM**：一个 `.pgm.gz` 里串着 20 张 `P5` 图，每张带 `#"键" 值` 注释头，时间取 `Image request start`（UTC）。THEMIS 与 REGO 的注释键名不同：THEMIS 写 `Geodetic latitude` / `Geodetic Longitude`（大写 L），REGO 写 `Geographic latitude` / `longitude`，曝光键也有 `Exposure options` / `Exposure Options` 两种大小写。
- THEMIS 最大计数 65535，说明暴夜**饱和**；REGO 99% 分位 2256、最大 50553。
- **Berkeley ast** 与 **MANGO cfs** 的全图均值都在 **07:07–07:08 UT** 最亮（本文口径的粗指标）。Gillam 在加拿大，Capitol Reef 在北纬 38°，两地相距很远，只能说明同一时段两处都亮，不能直接当作同一结构。
- **MANGO level1** 的 `ImageData` 是 uint8，**没有单位属性**，不是 Rayleigh；`Mask` 为 True 的是**被遮掉的**像素（仰角 < 15°，图像值为 0），有效像素要取反。经纬度网格按 250 km 投影，覆盖北纬 31.6–44.8°、西经 119.6–102.7°。
- **skymap**：`FULL_MAP_LATITUDE/LONGITUDE` 是 3×257×257（90/110/150 km 三个高度，像素角点所以多 1），经度按 0–360 存。gill 在 110 km、仰角 > 10° 的覆盖是北纬 52.0–61.0°。

## 4. 输入 / 输出

| 文件 | 时间 | 图像 | 定位 |
| --- | --- | --- | --- |
| UCalgary `.pgm.gz` | 每帧注释 `Image request start` | `P5`，16 bit 大端，THEMIS 256×256 / REGO 512×512 | 另下 skymap `.sav` |
| Berkeley `thg_l1_ast` | `thg_ast_<站>_time`（Unix 秒） | `thg_ast_<站>` 32×32 uint16 | 自带行列号；精确定位用 skymap |
| Berkeley `thg_l1_asf` | 同上（每小时） | 256×256 全帧 | 同上 |
| MANGO level1 HDF5 | `UnixTime`（2×N：起、止） | `ImageData` N×500×500 uint8 | `Latitude/Longitude/Elevation/Azimuth` 500×500，`Projection Altitude` 250 km |
| skymap `.sav` | 生效日期在目录名里 | — | `FULL_ELEVATION/AZIMUTH`（256×256）、`FULL_MAP_LATITUDE/LONGITUDE`（3 高度） |

## 5. 参数（路径拼装）

| 项 | 取值 | 说明 |
| --- | --- | --- |
| 站 + 成像仪 ID | `gill_themis19`、`gill_rego-652` | 同一成像仪号可能出现在两个站：本夜 `fsmi_themis10` 与 `snkq_themis10`，要用“站 + 成像仪”一起识别 |
| `stream0` | 原始全分辨率 | 目录里还有 `stream1/2/3`、`rt-mosaic` 等（本次未测） |
| MANGO 站码 | cfs、cvo、eio、mto、par（红线）；blo、low、new、cfs（绿线） | 2024/132 实测有 level1 的站 |
| MANGO DDD | 年积日（UT） | 2024-05-11 = 132 |

## 6. 接到哪一步

- 磁暴夜极光带南扩、SAR 弧 → [教程 20](../tutorials/20-storm-tec-analysis.md)，与 GNSS TEC / ROTI 对照（观测数据见 [cors-networks](./cors-networks.md)；闪烁见 [chain-scintillation](./chain-scintillation.md)）。
- 630 nm 暗条纹（等离子体泡）→ [教程 21](../tutorials/21-equatorial-anomaly-bubbles.md)；MANGO 在美国中纬，低纬泡要看其他台站。
- 卫星侧极光边界（DMSP SSUSI）→ [dmsp-timed-data](./dmsp-timed-data.md)；同站磁强计 → data-access [E12](../data-access.md#dp-e12)。

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 当 PGM 读只得到第一帧 | 一个 `.pgm.gz` 串了 20 帧 | 循环解析 `P5` 头，直到文件尾（见 3.2） |
| 2 | REGO 取站名 / 纬度得到 None | 注释键名和 THEMIS 不同（`Geographic` vs `Geodetic`，大小写也不同） | 两种键都试 |
| 3 | 亮区数值全是 65535 | THEMIS 白光相机暴夜饱和 | 饱和像素单独标记，别拿来求均值 |
| 4 | MANGO 有效区域“全是 0” | `Mask=True` 是被遮掉的像素 | 用 `~Mask` |
| 5 | 把 MANGO `ImageData` 当亮度 | uint8、无单位属性，不是 Rayleigh | 只做相对比较；定标另找 |
| 6 | 定位偏差大 | 用了最新 skymap（2024-08-29 起生效），不是观测日当时那版 | 选目录日期 ≤ 观测日的最后一个（本例 gill_20230922） |
| 7 | skymap 经度看起来不对 | 按 0–360 存 | 减 360 转成 −180–180 |
| 8 | skymap 网格比图像多 1 行 1 列 | `FULL_MAP_*` 存的是像素角点（257×257） | 取中心要平均四角，或截掉末行末列 |
| 9 | 一夜下载几个 GB | Berkeley `asf` 100 MB/h/站，REGO 每分钟 7 MB | 先用 `ast` 缩略图 / MANGO quicklook 挑时段 |
| 10 | 同一成像仪号出现在两个站 | `themis10` 本夜同时出现在 fsmi 和 snkq | 用“站 + 成像仪”一起识别 |
| 11 | 北美一夜跨两个日期目录 | 目录按 UT 日历日 | 夜间 UT 03–12 h 基本落在次日目录 |
| 12 | MANGO 某站只有红线或只有绿线 | 各站配置不同（本夜 8 站只有 cfs 两者都有） | 先列 `redline/` 和 `greenline/` |
| 13 | THEMIS 每小时文件数是 61，不是 60 | 多一个 `_HH_…_row2.pgm.gz` 每小时文件 | 文件名按 `_HHMM_` 过滤 |
| 14 | SPDF 上找不到 THEMIS ASI L1 | `spdf…/themis/thg/l1/asi/` 返回 404 | 用 Berkeley 或 UCalgary |

## 8. 选型

- **加拿大 / 阿拉斯加极光，高时间分辨率**：UCalgary THEMIS（3 s 白光）+ REGO（3 s，630 nm）；skymap 一起下。
- **只想先看一夜有没有事件**：Berkeley `ast` 缩略图（每站每日约 2.6 MB）或 MANGO quicklook。
- **美国中纬 630 nm（SAR 弧、中纬 TID、强暴时的泡）**：MANGO level1（每站每夜 1 个 HDF5，自带经纬度网格）。
- **程序化批量**：可以试 `pyaurorax` / `asilib`（本文未测），或按第 5 节自己拼路径。
