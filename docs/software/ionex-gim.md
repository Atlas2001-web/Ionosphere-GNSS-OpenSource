# ionex · 读 IONEX GIM 操作手册

目录：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex> · MIT · 本文件 [`ionex-gim.md`](./ionex-gim.md)

> 岗位：用 Python 包 **`ionex`** 读分析中心 IONEX（IGS/CODE/UPC/ESA…）VTEC 图。**只读**，不生成 GIM。球谐求解边界见 [sh-gim](./sh-gim.md)。绝对 TEC 校准见 [pytecgg](./pytecgg.md)（**viventriglia**）。API 以已安装包为准。

## 1. 用途与边界

**做：** `ionex.reader` 迭代每张 TEC 图；取历元、壳高、经纬网格、VTEC；与单站 TEC/IPP 对照、画图、插值（插值在库外）。

**不做：** 写回 IONEX / 球谐反演；算接收机 STEC → [pytecgg](./pytecgg.md)；读 RINEX → [georinex](./georinex.md)；ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。

一句话：**读壳层 VTEC 产品图**。

## 2. 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install "git+https://github.com/gnss-lab/ionex.git"
python -c "import ionex; print(ionex.__file__)"
python -m pip install numpy scipy matplotlib
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `git` 不可用 | 无 Git | 装 Git；或 zip 后 `pip install -e .` |
| `No module named ionex` | 错 venv | `which python`；重激活 |
| SSL/代理失败 | 网络 | 配代理或手工 clone |

## 3. 端到端：一张 IGS 图 → 历元字典 → 取值

### 3.1 文件必须是 IONEX 文本

```bash
mkdir -p data logs
# 例：igsg0490.23i —— 获取见 [data-access](../data-access.md)
head -n 5 data/igsg0490.23i
grep -n "END OF FILE" data/igsg0490.23i | tail -n 1
# 期望：首部含 IONEX VERSION / TYPE；绝不是 <!DOCTYPE html
```

### 3.2 读首张图（字段）

```bash
python - <<'PY'
import ionex
with open("data/igsg0490.23i") as f:
    m = next(ionex.reader(f))
print("epoch", m.epoch)
print("height_km", m.height)
print("lat", m.grid.latitude)   # lat1, lat2, dlat
print("lon", m.grid.longitude)  # lon1, lon2, dlon
print("tec_len", len(m.tec), "tec0", m.tec[0])
PY
```

| 属性 | 含义 | 注意 |
| --- | --- | --- |
| `epoch` | 图历元 `datetime` | 与观测对齐前统一时系 |
| `height` | 壳层高度 (km) | 报告写明；勿与 IPP 高混谈 |
| `grid.latitude` | `lat1,lat2,dlat` | **禁止写死 71×73** |
| `grid.longitude` | `lon1,lon2,dlon` | 注意 0–360 / −180–180 |
| `tec` | 一维 VTEC | 长度 = nlat×nlon；库多已按 EXPONENT 还原 |
| `rms`（若有） | RMS 图 | **勿当 TEC** |

### 3.3 全日图 → 最近邻历元

```bash
python - <<'PY'
import ionex
from datetime import datetime
maps = {}
with open("data/igsg0490.23i") as f:
    for m in ionex.reader(f):
        maps[m.epoch] = m
times = sorted(maps)
print("n_maps", len(times), "first", times[0], "last", times[-1])
t_obs = datetime(2023, 2, 18, 14, 5, 0)  # 改成你的时刻
t_map = min(times, key=lambda u: abs((u - t_obs).total_seconds()))
print("nearest", t_map, "dt_s", (t_map - t_obs).total_seconds())
print("tec0", maps[t_map].tec[0])
PY
```

**期望：** `n_maps` 常见 13/25；`|dt|` < 半个产品间隔。

### 3.4 头文件比例尺与 RMS

```bash
grep -E "EXPONENT|LAT1|LON1|HGT|INTERVAL|RMS|MAP" data/igsg0490.23i | head -n 40
```

- **EXPONENT**：整数→TECU 幂次；笔记写清。  
- **RMS map**：误差，不是 TEC。  
- 快速/最终/预报：报告写产品 ID。

### 3.5 reshape + 库外双线性（纲要）

```python
import numpy as np
# nlat = int(round((lat2-lat1)/dlat))+1 ；nlon 同理 —— 以 grid 字段算
# assert len(m.tec)==nlat*nlon
# grid = np.asarray(m.tec).reshape(nlat, nlon)
# 再对 (lat,lon) 双线性；经度范围先统一
```

教程 [03](../tutorials/03-gim-ionex.md) · [18](../tutorials/18-lab-compare-gims.md)。

### 3.6 与 pytecgg / 多中心

同日单站 `veq` vs GIM 插值：**比趋势与量级**。多中心：

```bash
for f in data/*0490.23i; do
  python - <<PY
import ionex
path="$f"
with open(path) as fh:
    ms = list(ionex.reader(fh))
print(path, "n", len(ms), "t0", ms[0].epoch, "tec0", ms[0].tec[0])
PY
done
```

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IONEX 文本 | `.i` / 分析中心命名；gzip 先解压 |
| 产品类型 | 快速/最终/预报——日志标注 |

| 输出 | 说明 |
| --- | --- |
| `IonexMap` 迭代 | epoch/height/grid/tec |
| 不输出 | 自建球谐、写回 IONEX、ROTI、DCB |

## 5. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| GIM 读图 | [03](../tutorials/03-gim-ionex.md) |
| 多 GIM 对照 | [18](../tutorials/18-lab-compare-gims.md) |
| 一日 TEC 对照 | [16](../tutorials/16-practice-one-day-tec.md) · [pytecgg](./pytecgg.md) |
| 自建边界 | [10](../tutorials/10-build-gim-workflow.md) · [sh-gim](./sh-gim.md) |
| 磁暴背景场 | [20](../tutorials/20-storm-tec-analysis.md) |
| 下载 | [data-access](../data-access.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 解析炸 / 首行 HTML | 下载成登录页 | `head`；重走 Earthdata |
| 2 | reshape 失败 | 写死 71×73 | 用 `grid` 算维数 |
| 3 | TECU 差 10× | 忽略 EXPONENT | 读头；对照已知图 |
| 4 | 把 RMS 当 TEC | 图类型错 | 查 MAP 类型 |
| 5 | 快速/最终混用未标注 | 产品混淆 | 写清产品 ID |
| 6 | 与 STEC 强行相等 | 对象不同 | 只比趋势量级 |
| 7 | 时间对不齐 | GPST/UTC 混用 | 统一再减 |
| 8 | 壳高 vs IPP 高混谈 | 概念混 | 各自声明 |
| 9 | 经度约定打架 | 0–360 vs ±180 | 插值前统一 |
| 10 | 末日缺图 | 文件截断 | 查 `END OF FILE` |
| 11 | 期望本包生成 GIM | 边界错 | → 开源求解器；[sh-gim](./sh-gim.md) 边界 |
| 12 | clone SH-GIM 当可跑全球解 | 求解器未开源 | 读边界页 |
| 13 | PyTECGg 作者写错 | 张冠李戴 | viventriglia |
| 14 | `list(reader)` 后无检查 | 静默空 | 先 `len` 与首尾历元 |
| 15 | gzip 当明文 | 魔数/后缀 | `file`；先 `gunzip` |
| 16 | 过 180° 经度跳变 | 未 unwrap | 插值前处理 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 读 IGS 等 IONEX | **ionex（本页）** |
| 单站校准 TEC | pytecgg |
| 理解球谐仓边界 | sh-gim |
| 开源端到端建图 | lists 中 mosgim / m_gim 等 |

## 8. 相关

[sh-gim](./sh-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · [README](./README.md)
