# ionex（读 IONEX GIM）

目录：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex> · 文件名 [`ionex-gim.md`](./ionex-gim.md)

> 操作手册。祈使句。本包**只读**分析中心 IONEX；不生成 GIM。SH-GIM：维护者自有仓，**球谐求解器未开源**——见 [sh-gim](./sh-gim.md)，此处不展开求解。PyTECGg = **viventriglia**。

---

## 用途与边界

**用：**

- 用 Python 包 **`ionex`** 读取 IGS / CODE / UPC / ESA 等 **IONEX** 全球电离层图（GIM）。
- 按历元取出 VTEC 格网，与自站 STEC/VTEC、穿刺点对照、画图、插值。
- 教学与实验：教程 [03](../tutorials/03-gim-ionex.md)、[18](../tutorials/18-lab-compare-gims.md)。

**不用 / 边界：**

- **不生成** GIM / 不写回 IONEX。
- **不算** 接收机 STEC → [pytecgg](./pytecgg.md)（viventriglia）。
- **不替代** 球谐建模；公开自建请看列表 `mosgim` / `mosgim2` / `m_gim` 等；[sh-gim](./sh-gim.md) 仅说明公开/专有边界。
- **不读** RINEX → [georinex](./georinex.md)。
- **不做** ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。

一句话：ionex = **读分析中心壳层 VTEC 图**。

---

## 安装（多平台 + 报错）

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
# 推荐 editable 自源码（上游若未稳定发 PyPI）
pip install -e "git+https://github.com/gnss-lab/ionex.git#egg=ionex"
# 或：
# git clone https://github.com/gnss-lab/ionex.git
# cd ionex && pip install -e .
python -c "import ionex; print(ionex.__file__)"
pip install numpy scipy matplotlib netCDF4
```

### Windows（PowerShell）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e "git+https://github.com/gnss-lab/ionex.git#egg=ionex"
python -c "import ionex; print(ionex.__file__)"
```

需 Git for Windows。若公司防火墙拦 `git+https`：先手动 clone 再 `pip install -e .`。

### 安装期常见报错

| 现象 | 处理 |
|---|---|
| `git` 不是内部或外部命令 | 装 Git；或下载 zip 再 `pip install -e` |
| `egg=ionex` 语法错 | 检查引号；zsh/PowerShell 引号规则不同 |
| `No module named ionex` | 确认激活 venv；`pip show ionex` |
| SSL / 代理失败 | 配 `HTTPS_PROXY`；改用手工 clone |
| 旧 setuptools 报错 | `pip install -U pip setuptools wheel` |

### 安装验收

```bash
python - <<'PY'
import ionex, inspect
print("ionex ok", ionex.__file__)
print("reader", hasattr(ionex, "reader"))
PY
```

---

## 快速冒烟（10 分钟）

```bash
# 0) 文件必须是 IONEX 文本，不是 HTML 登录页
head -n 20 data/igsg0490.23i
grep -n "END OF FILE" data/igsg0490.23i | tail
# 期望：首行附近有 IONEX VERSION / TYPE；文件末有 END OF FILE

python - <<'PY'
import ionex
from datetime import datetime
with open("data/igsg0490.23i") as f:
    m = next(ionex.reader(f))
print("epoch", m.epoch)
print("height", m.height)
print("lat", m.grid.latitude)
print("lon", m.grid.longitude)
print("tec_len", len(m.tec))
PY
```

**期望：** `epoch` 为 datetime；`tec` 一维长度 = 纬度点数 × 经度点数（先算再断言）。

**失败：** `UnicodeDecodeError` / 解析异常 / 首行 `<!DOCTYPE` → 重新按 [data-access](../data-access.md) 鉴权下载。

---

## 完整工作流

### 工作流 A：读全日 GIM → 建历元字典 → 最近邻对照

教程 [03](../tutorials/03-gim-ionex.md)。

```bash
python - <<'PY'
import ionex
from datetime import datetime, timedelta
path = "data/igsg0490.23i"
maps = {}
with open(path) as f:
    for m in ionex.reader(f):
        maps[m.epoch] = m
times = sorted(maps)
print("n_maps", len(times), "first", times[0], "last", times[-1])

t_obs = datetime(2023, 2, 18, 14, 5, 0)  # 改成你的观测时刻（注意时间系）
t_map = min(times, key=lambda u: abs((u - t_obs).total_seconds()))
dt = (t_map - t_obs).total_seconds()
print("nearest", t_map, "dt_s", dt)
m = maps[t_map]
print("height_km", m.height, "tec0", m.tec[0])
PY
```

**期望：** `n_maps` 通常为 13/25 等（视产品间隔）；`|dt|` 小于半个产品间隔。

### 工作流 B：格网 reshape + 双线性插值（库外）

```bash
python - <<'PY'
import ionex
import numpy as np
from datetime import datetime

def grid_shape(m):
    # 以文件内 grid 为准，禁止写死 71×73
    lats = np.asarray(m.grid.latitude, dtype=float)
    lons = np.asarray(m.grid.longitude, dtype=float)
    # 不同实现可能给起止+步长或显式向量——先打印
    print("lat repr", lats[:5], "...", "len?", getattr(lats, "shape", None))
    print("lon repr", lons[:5], "...")
    return lats, lons

with open("data/igsg0490.23i") as f:
    m = next(ionex.reader(f))

# 头文件 EXPONENT / 比例尺：读原始 IONEX 注释；tec 值可能已是 TECU 或需乘因子
# 操作：打开文件搜 EXPONENT
lats, lons = grid_shape(m)
# 若 latitude/longitude 是标量起止，按 IONEX 头 LAT1/LAT2/DLAT 计算：
# nlat = int(round((lat2-lat1)/dlat))+1 等——以你读到的对象字段为准

tec = np.asarray(m.tec, dtype=float)
print("tec_len", tec.size)

# 示例：若已能确定 nlat, nlon：
# assert tec.size == nlat * nlon
# grid = tec.reshape(nlat, nlon)

def bilinear(grid, lat_axis, lon_axis, lat, lon):
    # lat_axis, lon_axis 单调；lon 注意 0–360 / -180–180 一致
    lat = float(lat); lon = float(lon)
    # 将 lon 折算到轴范围…
    i = np.searchsorted(lat_axis, lat) - 1
    j = np.searchsorted(lon_axis, lon) - 1
    i = np.clip(i, 0, len(lat_axis) - 2)
    j = np.clip(j, 0, len(lon_axis) - 2)
    x0, x1 = lat_axis[i], lat_axis[i+1]
    y0, y1 = lon_axis[j], lon_axis[j+1]
    q11, q21 = grid[i, j], grid[i+1, j]
    q12, q22 = grid[i, j+1], grid[i+1, j+1]
    tx = 0 if x1 == x0 else (lat - x0) / (x1 - x0)
    ty = 0 if y1 == y0 else (lon - y0) / (y1 - y0)
    return (q11*(1-tx)*(1-ty) + q21*tx*(1-ty) + q12*(1-tx)*ty + q22*tx*ty)

print("implement reshape using header; then call bilinear")
PY
```

教程 [18](../tutorials/18-lab-compare-gims.md) 要求：插值代码自管；断言 `len(tec)==nlat*nlon`。

### 工作流 C：与 PyTECGg VTEC 对照（量级 / 日变化）

```bash
# 1) pytecgg 产出 tec_calibrated.parquet（见 pytecgg 手册；作者 viventriglia）
# 2) 同日 IONEX
# 3) 对每个历元：站天顶 veq 或穿刺点 VTEC vs GIM 插值
```

```bash
python - <<'PY'
# 伪流程：读 parquet 中 vtec/veq 与时间；对每个时刻取 maps 最近邻；插值 IPP 或站 lat/lon
print("比趋势与量级，不要求像素级相等")
print("GIM=壳层 VTEC；观测含斜向几何与残留偏差")
PY
```

### 工作流 D：多分析中心互比

```bash
# 同日 igsg / codg / uqrg …（文件名以 data-access 为准）
for f in data/*0490.23i; do
  echo "== $f"
  python - <<PY
import ionex, sys
path = "$f"
with open(path) as fh:
    ms = list(ionex.reader(fh))
print(path, "n", len(ms), "t0", ms[0].epoch, "t1", ms[-1].epoch, "tec0", ms[0].tec[0])
PY
done
```

**期望：** 历元数可能不同；VTEC 有系统差属常见。记录产品 ID（快速/最终）。

### 工作流 E：头文件比例尺与 RMS 图

```bash
grep -E "EXPONENT|MAP|RMS|LAT|LON|HGT|INTERVAL|BASE RADIUS" data/igsg0490.23i | head -n 40
```

- **EXPONENT**：决定 tec 整数如何还原 TECU。  
- **RMS map**：勿当 TEC 使用。  
- **height**：壳层高度（常见 450 km 等）——与 pytecgg `h_ipp` 不必强行相同，但报告时写明。

### 工作流 F：数据门户下载自检

```bash
# 下载后立刻：
file data/igsg0490.23i
head -n 3 data/igsg0490.23i
# 若 HTML：
grep -i "<html\|Earthdata\|login" data/igsg0490.23i && echo "BAD DOWNLOAD"
```

CDDIS / Earthdata：按 [data-access](../data-access.md) 配置 `.netrc`；失败不要喂给 `ionex.reader`。

---

## 输入 / 输出与字段表

### 输入

| 项 | 说明 |
|---|---|
| IONEX 文本 | `.i` / `.inx` / 分析中心命名 |
| 产品类型 | 快速 / 最终 / 预报——日志写清 |
| 时间系 | 与观测对照前统一 |

### reader 产出 map 对象（典型属性）

| 属性 | 含义 | 注意 |
|---|---|---|
| `epoch` | 图历元 datetime | 最近邻 / 插值时间基准 |
| `height` | 壳层高度 | 报告写明 |
| `grid.latitude` / `longitude` | 格网定义 | **禁止写死维数** |
| `tec` | 一维 VTEC 格网值 | 查 EXPONENT |
| （若有）RMS | 误差图 | 勿当 TEC |

### 不做的输出

自建球谐系数、IONEX 写回、接收机 DCB、ROTI。

---

## 常用参数

本包以 **`ionex.reader(fileobj)` 迭代** 为主，几乎无复杂 CLI。

| 项 | 操作 |
|---|---|
| 打开方式 | `with open(path) as f:` 文本模式 |
| 迭代 | `for m in ionex.reader(f):` |
| 单张 | `next(ionex.reader(f))` |
| 比例尺 | 读文件头 EXPONENT |
| 产品标注 | 文件名 + 分析中心 + 快速/最终 |

画图 / 插值：`numpy` / `scipy` / `matplotlib` 在库外完成。

---

## 接到 tutorials / 工作流哪一步

| 场景 | 链接 |
|---|---|
| GIM 读写入门 | [03](../tutorials/03-gim-ionex.md) |
| 多 GIM 实验对照 | [18](../tutorials/18-lab-compare-gims.md) |
| 与一日 TEC 对照 | [16](../tutorials/16-practice-one-day-tec.md) · [pytecgg](./pytecgg.md) |
| 理解自建流程边界 | [10](../tutorials/10-build-gim-workflow.md) · [sh-gim](./sh-gim.md) |
| 磁暴日背景场 | [20](../tutorials/20-storm-tec-analysis.md) |
| 数据获取 | [data-access](../data-access.md) · CDDIS `gnss/products/ionex/` |
| 索引路径 A/E | [software README](./README.md) |

---

## 可操作坑（≥12）

1. **把 HTML 登录页当 IONEX** — `head` 先看。  
2. **写死 71×73** — 只信文件头 / `grid`。  
3. **忽略 EXPONENT** — TECU 错一个数量级。  
4. **把 RMS 当 TEC** — 检查 MAP 类型。  
5. **快速/最终混用却不标注** — 论文/报告必写产品 ID。  
6. **与 STEC 强行逐点相等** — 只比趋势与量级。  
7. **时间系混乱** — GPST/UTC 写明再减。  
8. **壳层高度与 IPP 高度混谈** — 各自声明。  
9. **经度 0–360 与 −180–180 混用** — 插值前统一。  
10. **日界文件缺最后一张图** — 查 `END OF FILE` 与历元列表。  
11. **期望本包生成 GIM** — 错；去开源求解器或授权工具。  
12. **把 SH-GIM clone 当可跑全球解** — 求解未开源。  
13. **PyTECGg 作者写成维护者** — 正确为 viventriglia。  
14. **大文件一次性 `list(reader)` 后无检查** — 先 `len` 与首尾历元。  
15. **插值越界静默外推** — `clip` 并记日志。  
16. **多中心互比不统一掩膜** — 先统一海陆/纬度带再统计。

---

## 同类选型

| 需求 | 选 |
|---|---|
| 读 IONEX → Python 对象 | **ionex（本页）** |
| 校准站 TEC | **pytecgg**（viventriglia） |
| 自建开源球谐 | mosgim / m_gim 等（列表） |
| 维护者工程边界 | **sh-gim**（不承诺求解） |
| 只画官方图 | 分析中心现成图；仍建议本地可读文件复现 |

---

## 操作检查清单

1. `import ionex` 成功。  
2. 样例文件 `head` 非 HTML。  
3. `END OF FILE` 存在。  
4. `next(reader)` 出 epoch/tec。  
5. reshape 前断言长度。  
6. 记录 EXPONENT 与产品 ID。  
7. 对照实验写明时间系与壳层高度。  
8. 不把 RMS 当 TEC。  
9. 不宣称像素级等于站 VTEC。  
10. 参数/API 以本机源码与上游 README 为准。

---

## 附录 A · 期望 I/O

```text
epoch 2023-02-18 00:00:00
height 450.0
tec_len 5113   # 示例，以实文件为准
n_maps 13
```

---

## 附录 B · 最小回归脚本

```bash
#!/usr/bin/env bash
set -euo pipefail
f=${1:?ionex file}
head -n 2 "$f" | grep -qi ionex
grep -q "END OF FILE" "$f"
python - <<PY
import ionex, sys
with open(sys.argv[1]) as fh:
    m = next(ionex.reader(fh))
assert m.epoch is not None
assert len(m.tec) > 0
print("PASS", m.epoch, len(m.tec))
PY
"$f"
```

---

## 附录 C · 头字段速查命令

```bash
awk '/END OF HEADER/{exit} {print}' data/igsg0490.23i | head -n 80
```

---

## 附录 D · 与 pytecgg 对照表模板

| 时刻 | 站 veq/vtec | GIM 插值 | 差 | 产品 |
|---|---|---|---|---|
| | | | | igsg final |

填表比画「好看但不标注产品」的图更重要。

---

## 附录 E · 下载失败识别

| `head` 所见 | 动作 |
|---|---|
| `IONEX VERSION` | 好 |
| `<!DOCTYPE html>` | 鉴权 / cookie |
| `Access Denied` | Earthdata 登录 |
| 空文件 | 重下 |

---

## 附录 F · 时间插值（两张图之间）

```bash
python - <<'PY'
# 取 t0,t1 两张 map，对 tec 向量线性插值权重 w=(t-t0)/(t1-t0)
# 再 reshape 后空间插值；注意跨文件日界
print("time interpolate then bilinear")
PY
```

---

## 附录 G · 地图绘制最小例

```bash
python - <<'PY'
# reshape 成功后：
# plt.pcolormesh(lons, lats, grid, shading="auto")
# plt.colorbar(label="TECU"); plt.title(str(epoch))
print("use matplotlib after reshape")
PY
```

---

## 附录 H · 与 sh-gim 的一句话边界

- **ionex-gim**：读别人的图。  
- **sh-gim**：公开预处理骨架；**法方程求解专有未开源**；不能指望 clone 后出全球解。

---

## 附录 I · 批处理多日

```bash
for f in data/igsg*.i; do
  python -c "import ionex,sys; print(sys.argv[1], sum(1 for _ in ionex.reader(open(sys.argv[1]))))" "$f"
done
```

---

## 附录 J · 科学报告必写项

1. 分析中心与产品名。  
2. 快速/最终。  
3. 壳层高度。  
4. 时间系。  
5. 插值方法。  
6. 与站 TEC 差的统计（RMSE/中位数），非单点炫图。

---

## 附录 K · 相关工具

[pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · data-access


---

## 附录 L · 逐步：从下载到第一张图数值

1. 按 data-access 下载某日 `igsgDDD0.YYi`。  
2. `head` / `file` / `grep END OF FILE`。  
3. `import ionex`；`next(reader)`。  
4. 打印 epoch、height、len(tec)。  
5. `awk` 头：LAT/LON/DLAT/DLON/EXPONENT。  
6. 计算 nlat、nlon；`assert len(tec)==nlat*nlon`。  
7. `reshape`；抽查中纬度海洋点 TECU 是否在合理季节范围。  
8. 保存 `logs/gim_smoke.txt`。  
9. 再读第二分析中心文件做差。  
10. 与 pytecgg 同日 veq 比日变化（viventriglia）。

---

## 附录 M · 合理 TECU 粗检（非严格）

```text
中纬静日白天 VTEC 常见数十 TECU 量级；夜间更低
赤道可能更高；磁暴可显著抬升或复杂再分布
若出现 1e5 或全 0：先查 EXPONENT 与是否误读 RMS
```

---

## 附录 N · 错误栈对照

| 异常 | 动作 |
|---|---|
| `StopIteration` | 文件无图；坏文件 |
| `ValueError` 解析 | HTML/截断 |
| `AssertionError` reshape | 维数算错 |
| `KeyError` 自写代码 | 打印 `dir(m)` |

---

## 附录 O · dir(m) 探活

```bash
python - <<'PY'
import ionex
with open("data/igsg0490.23i") as f:
    m = next(ionex.reader(f))
print([a for a in dir(m) if not a.startswith("_")])
print(type(m.grid), dir(m.grid))
PY
```

上游改字段名时以此为准。

---

## 附录 P · 验收表

| 项 | 通过标准 |
|---|---|
| 安装 | import 成功 |
| 文件 | 非 HTML + EOF |
| 读取 | n_maps>0 |
| 维数 | assert 通过 |
| 标注 | 产品 ID 写入日志 |
| 对照 | 差分解释合理 |

---

## 附录 Q · 不要做的事

- 不要用本包「生成」IONEX。  
- 不要把 SH-GIM 公开仓当完整求解器。  
- 不要隐瞒快速产品当最终产品。  
- 不要在未统一经度定义时发表插值图。

---

## 附录 R · 相关工具（复述）

[pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [oasis-roti](./oasis-roti.md)


---

## 附录 S · 与教程 03 逐步对齐

1. 打开 [03](../tutorials/03-gim-ionex.md) 的数据准备节。  
2. 按 data-access 下载同日 IONEX。  
3. 本页「快速冒烟」全过。  
4. 完成 reshape 断言。  
5. 画一张 pcolormesh（可交作业）。  
6. 记录产品 ID 与 EXPONENT。  
7. 可选：换 codg 再画差图（接 [18](../tutorials/18-lab-compare-gims.md)）。

---

## 附录 T · 与教程 18 实验室清单

| 步 | 命令 / 产物 | 勾选 |
|---|---|---|
| 两家 IONEX | `ls data/*DDD*` | |
| 同时段 | 打印双方 times | |
| 同网格插值 | 自写脚本 | |
| 差分统计 | RMSE/中位数 | |
| 结论 | 趋势一致？偏差量级？ | |

---

## 附录 U · 一页纸验收

1. `import ionex`。  
2. 非 HTML。  
3. EOF。  
4. n_maps>0。  
5. reshape assert。  
6. 产品标注。  
7. 时间系统明。  
8. 未把 RMS 当 TEC。  
9. SH-GIM 未误用为求解器。  
10. PyTECGg 作者写为 viventriglia。

---

## 附录 V · 命令速查

```bash
head -n 20 file.i
grep "END OF FILE" file.i
python -c "import ionex; print(next(ionex.reader(open('file.i'))).epoch)"
grep EXPONENT file.i
```

---

## 附录 W · 相关工具（终）

[pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)
