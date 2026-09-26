# ionex · 读 IONEX GIM 操作手册

目录：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex> · MIT · 本文件 [`ionex-gim.md`](./ionex-gim.md) · **新短硬同包** → [ionex.md](./ionex.md) · 本机验证 **ionex 0.2**（包内 `tests/test_data/ionex_file.00i`）· **质检复跑**（2026-09-26 01:05 EDT，新 venv Python 3.13.5，`git+` 装得 ionex **0.2**，上游 tip `8783a71` 2020-07-24 23:18 EDT 无更新）：§3.2 八行输出逐字一致（12 图、71×73=5183、tec0 9.8 / mid 31.8、nearest dt −3600 s）；`next(reader)` TypeError、`_rms None`、`m.rms` NotImplementedError 复现；修 §3.1 grep（原式 `LON1` 命中数据块头 + `head` 截断，给不出所示 END OF FILE 行）。真产品冒烟：AIUB `http://ftp.aiub.unibe.ch/CODE/2023/` 约 97 s 无响应（curl `000 0`），未测

> 岗位：用 Python 包 **`ionex`** 读分析中心 IONEX（IGS/CODE/UPC/ESA…）VTEC 图。**只读**，不生成 GIM。球谐求解边界见 [sh-gim](./sh-gim.md)。绝对 TEC 校准见 [pytecgg](./pytecgg.md)（**viventriglia**）。API 以已安装包为准。

## 1. 用途与边界

**做：** `ionex.reader(path)` 迭代每张 TEC 图；取历元、壳高、经纬网格、VTEC；与单站 TEC/IPP 对照、画图、插值（插值在库外）。

**不做：** 写回 IONEX / 球谐反演；算接收机 STEC → [pytecgg](./pytecgg.md)；读 RINEX → [georinex](./georinex.md)；ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。

一句话：**读壳层 VTEC 产品图**。

## 2. 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install "git+https://github.com/gnss-lab/ionex.git"
python -c "import ionex; print(ionex.__file__)"
# 可选：画图 / reshape
python -m pip install numpy matplotlib
# 冒烟用上游测试文件：
git clone --depth 1 https://github.com/gnss-lab/ionex.git ionex-src
ls ionex-src/tests/test_data/ionex_file.00i
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `git` 不可用 | 无 Git | 装 Git；或 zip 后 `pip install -e .` |
| `No module named ionex` | 错 venv | `which python`；重激活 |
| SSL/代理失败 | 网络 | 配代理或手工 clone |
| `TypeError: 'IonexV1' object is not an iterator` | 对 reader 直接 `next(...)` | 用 `for m in ionex.reader(path)` 或 `next(iter(...))` |

## 3. 端到端：一张 IONEX → 历元字典 → 取值

### 3.1 文件必须是 IONEX 文本

```bash
mkdir -p data logs
# 生产：按 [data-access](../data-access.md) 取 igsgDDD0.YYi 等；gzip 先 gunzip
# 冒烟：用包内测试文件（本机已跑）
cp ionex-src/tests/test_data/ionex_file.00i data/
head -n 5 data/ionex_file.00i
grep -E "IONEX VERSION|INTERVAL|HGT1 /|LAT1 /|LON1 /|EXPONENT|END OF FILE" data/ionex_file.00i
# 注：若写成 `LON1` 不带 ` /` 再接 `| head`，会命中每行 `LAT/LON1/LON2/DLON/H` 数据块头，head 截掉 END OF FILE
```

**本机真实首行 / 头字段（上面 grep 原样输出 7 行）：**

```text
     1.0            IONOSPHERE MAPS     GPS                 IONEX VERSION / TYPE
  7200                                                      INTERVAL
   450.0 450.0   0.0                                        HGT1 / HGT2 / DHGT
    87.5 -87.5  -2.5                                        LAT1 / LAT2 / DLAT
  -180.0 180.0   5.0                                        LON1 / LON2 / DLON
    -1                                                      EXPONENT
                                                            END OF FILE
```

**期望：** 首部含 `IONEX VERSION / TYPE`；绝不是 `<!DOCTYPE html`。

### 3.2 读全日图（正确 API）

**传路径字符串**。`ionex.reader` 返回可 `for` 迭代的 `IonexV1`，**不是**直接的 iterator——不要写 `next(ionex.reader(open(...)))`。

```bash
python - <<'PY'
import ionex
from datetime import datetime
path = "data/ionex_file.00i"
maps = {m.epoch: m for m in ionex.reader(path)}
times = sorted(maps)
m0 = maps[times[0]]
lat1, lat2, dlat = m0.grid.latitude
lon1, lon2, dlon = m0.grid.longitude
nlat = int(round((lat2 - lat1) / dlat)) + 1
nlon = int(round((lon2 - lon1) / dlon)) + 1
h = m0.height
h_km = getattr(h, "hgt1", h)  # 0.2 测试文件上 height 可能是 Height 命名元组
print("n_maps", len(times))
print("first", times[0])
print("last", times[-1])
print("height", h, "-> shell_km", h_km)
print("lat", m0.grid.latitude)
print("lon", m0.grid.longitude)
print("nlat", nlat, "nlon", nlon, "tec_len", len(m0.tec), "match", nlat * nlon == len(m0.tec))
print("tec0", m0.tec[0], "tec_mid", m0.tec[len(m0.tec) // 2])
t_obs = datetime(2000, 1, 1, 12, 0, 0)
t_map = min(times, key=lambda u: abs((u - t_obs).total_seconds()))
print("nearest", t_map, "dt_s", (t_map - t_obs).total_seconds())
PY
```

**本机真实输出（ionex 0.2 + 测试文件，2026-09-24）：**

```text
n_maps 12
first 2000-01-01 01:00:00
last 2000-01-01 23:00:00
height Height(hgt1=450.0, hgt2=450.0, dhgt=0.0) -> shell_km 450.0
lat Latitude(lat1=87.5, lat2=-87.5, dlat=-2.5)
lon Longitude(lon1=-180.0, lon2=180.0, dlon=5.0)
nlat 71 nlon 73 tec_len 5183 match True
tec0 9.8 tec_mid 31.8
nearest 2000-01-01 11:00:00 dt_s -3600.0
```

| 属性 | 含义 | 注意 |
| --- | --- | --- |
| `epoch` | 图历元 `datetime` | 与观测对齐前统一时系 |
| `height` | 壳高；测试文件上可能是 `Height(hgt1,hgt2,dhgt)` | 取 `hgt1` 或 `float`；报告写 km |
| `grid.latitude` | `lat1,lat2,dlat` | **禁止写死 71×73**；用字段算 |
| `grid.longitude` | `lon1,lon2,dlon` | 注意 0–360 / −180–180 |
| `tec` | 一维 VTEC（**已按 EXPONENT 还原**） | 长度 = nlat×nlon |
| `rms` | RMS 图 | 本机测试文件 `_rms is None`；有图时 **勿当 TEC**；访问可能 `NotImplementedError` |

### 3.3 reshape + 库外双线性（纲要）

```python
import numpy as np
# nlat/nlon 按上表从 grid 计算；assert len(m.tec)==nlat*nlon
grid = np.asarray(m.tec, dtype=float).reshape(nlat, nlon)
# 再对 (lat,lon) 双线性；经度范围先统一
```

### 3.4 多中心同日对照

```bash
for f in data/*0490.23i data/ionex_file.00i; do
  test -f "$f" || continue
  python - <<PY
import ionex
path = "$f"
ms = list(ionex.reader(path))
print(path, "n", len(ms), "t0", ms[0].epoch, "tec0", ms[0].tec[0])
PY
done
```

与 [pytecgg](./pytecgg.md) 同日 `veq`：**比趋势与量级**，不强行相等。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IONEX 文本 | `.i` / 分析中心命名；gzip 先解压 |
| 产品类型 | 快速/最终/预报——日志标注 |

| 输出 | 说明 |
| --- | --- |
| `IonexMap` 迭代 | epoch / height / grid / tec |
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
| 3 | TECU 差 10× | 忽略 EXPONENT | 读头；本包 `tec` 多已还原，对照已知图 |
| 4 | 把 RMS 当 TEC | 图类型错 | 查 MAP 类型；测试文件无 RMS |
| 5 | 快速/最终混用未标注 | 产品混淆 | 写清产品 ID |
| 6 | 与 STEC 强行相等 | 对象不同 | 只比趋势量级 |
| 7 | 时间对不齐 | GPST/UTC 混用 | 统一再减 |
| 8 | 壳高 vs IPP 高混谈 | 概念混 | 各自声明 |
| 9 | 经度约定打架 | 0–360 vs ±180 | 插值前统一 |
| 10 | 末日缺图 | 文件截断 | 查 `END OF FILE` |
| 11 | 期望本包生成 GIM | 边界错 | → 开源求解器；[sh-gim](./sh-gim.md) 边界 |
| 12 | `next(reader(f))` TypeError | API 用法错 | `for m in ionex.reader(path)` |
| 13 | PyTECGg 作者写错 | 张冠李戴 | viventriglia |
| 14 | `list(reader)` 后无检查 | 静默空 | 先 `len` 与首尾历元 |
| 15 | gzip 当明文 | 魔数/后缀 | `file`；先 `gunzip` |
| 16 | 过 180° 经度跳变 | 未 unwrap | 插值前处理 |
| 17 | `m.rms` 抛 NotImplementedError | 无 RMS 图 | 先判 `_rms is None` |
| 18 | `height` 不是 float | 版本/文件把 Height 元组塞进属性 | `getattr(h,"hgt1",h)` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 读 IGS 等 IONEX | **ionex（本页）** |
| 单站校准 TEC | pytecgg（viventriglia） |
| 理解球谐仓边界 | sh-gim |
| 开源端到端建图 | lists 中 mosgim（[mosgim2 手册](./mosgim2.md)）/ m_gim 等 |

## 8. 相关

[ionex.md](./ionex.md) · [ionex-rs](./ionex-rs.md) · [sh-gim](./sh-gim.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [data-access](../data-access.md) · [README](./README.md)
