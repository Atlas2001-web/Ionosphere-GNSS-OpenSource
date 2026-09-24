# ionex · gnss-lab Python IONEX 读入操作手册

目录：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex> · tip **`8783a71`**（tag 文案 **ionex-v0.2**，2020-07-25）· **MIT** · **无 PyPI 发行**（须 git/`pip install git+…`）· 本机验证（**2026-09-24 06:42 EDT**）：venv + `pip install git+https://github.com/gnss-lab/ionex.git` → **0.2**；`tests/test_data/ionex_file.00i` → **12** 图；首 **2000-01-01 01:00:00** / 末 **23:00:00**；壳高 **450** km；网格 **71×73**（`tec_len` **5183**）；`tec0`=**9.8** / mid=**31.8**；`tec` 含 **287** 个 `None`；`m.rms`→**NotImplementedError**；**未臆造生产 GIM TEC**

> 岗位：用轻量 Python 包 **`ionex`** 读分析中心 IONEX（IGS/CODE/UPC…）壳层 VTEC 图。冲突时：**已安装包 API / 仓内 `tests/` / 本机冒烟 > 本文**。  
> 早期 R3 短硬同包另见 [ionex-gim](./ionex-gim.md)（**勿改**）；Rust 读写 → [ionex-rs](./ionex-rs.md)；RINEX → [georinex](./georinex.md)；粗斜 TEC → [gnss-tec](./gnss-tec.md)。

## 1. 用途与边界

**做：**

- `ionex.reader(path_or_file)` 迭代每张 `IonexMap`（`epoch` / `height` / `grid` / `tec`）
- 路径字符串或已打开的文本文件对象均可
- 教学/对照：与单站 TEC、多中心同日图并排（插值在库外）

**不做：**

- **不是** Rust crate `ionex` → [ionex-rs](./ionex-rs.md)（可写回；格点键索引）
- **不是** 本目录历史篇名 [ionex-gim](./ionex-gim.md) 的替代重写目标——同包；新短硬以 **本文文件名** 为准，旧篇保留交叉
- **不是** 写回 IONEX / 球谐建图 → [sh-gim](./sh-gim.md) 边界 + lists 其它 GIM
- **不是** 从 RINEX 算 STEC → [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)
- **无** RMS 图实现（访问 `rms` 抛 `NotImplementedError`）

一句话：`ionex` = **Python 只读 IONEX 网格**；嵌入 Rust 服务用 ionex-rs，生成 GIM 另寻求解器。

| | **本文 `ionex`（Python）** | [ionex-rs](./ionex-rs.md) | [ionex-gim](./ionex-gim.md) |
| --- | --- | --- | --- |
| 栈 | CPython 包 | Rust crate `ionex` | **同 Python 包**的旧手册文件名 |
| 写回 | **否** | `format` 可 | 否 |
| 安装 | `git+https://…`（无 PyPI） | `cargo add ionex` | 同左包 |
| 本机样例 | `ionex_file.00i` **12** 图 / tec0 **9.8** | CKMG **9.2** TECU | 同测试文件 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv ionex-venv && source ionex-venv/bin/activate
python -m pip install -U pip
# 无 PyPI 轮子：
python -m pip install "git+https://github.com/gnss-lab/ionex.git"
python -c "import ionex; from importlib.metadata import version; print(version('ionex'), ionex.__file__)"
# 期望：0.2  + …/site-packages/ionex/__init__.py

git clone --depth 1 https://github.com/gnss-lab/ionex.git ionex-src
cd ionex-src && git rev-parse --short HEAD   # 本机：8783a71
ls tests/test_data/ionex_file.00i
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `pip install ionex` 失败 | **未上 PyPI** | 用 `git+https://…` 或 `pip install -e .` |
| `No module named ionex` | 错 venv | `which python`；重激活 |
| `TypeError: 'IonexV1' is not an iterator` | `next(reader(...))` | `for m in …` 或 `next(iter(…))` |

## 3. 端到端：测试 IONEX → 历元字典（本机真跑）

```bash
cd ~/iono_ops/ionex-src   # 或任意含测试文件的目录
source ~/iono_ops/ionex-venv/bin/activate
head -n 2 tests/test_data/ionex_file.00i
# 期望首行含：IONEX VERSION / TYPE

python - <<'PY'
import ionex
path = "tests/test_data/ionex_file.00i"
maps = {m.epoch: m for m in ionex.reader(path)}
times = sorted(maps)
m0 = maps[times[0]]
lat1, lat2, dlat = m0.grid.latitude
lon1, lon2, dlon = m0.grid.longitude
nlat = int(round((lat2 - lat1) / dlat)) + 1
nlon = int(round((lon2 - lon1) / dlon)) + 1
h = m0.height
h_km = getattr(h, "hgt1", h)
tec = list(m0.tec)
finite = [t for t in tec if t is not None]
print("n_maps", len(times))
print("first", times[0], "last", times[-1])
print("shell_km", h_km, "lat", m0.grid.latitude, "lon", m0.grid.longitude)
print("nlat", nlat, "nlon", nlon, "tec_len", len(tec), "match", nlat * nlon == len(tec))
print("tec0", tec[0], "tec_mid", tec[len(tec)//2])
print("tec_min", min(finite), "tec_max", max(finite), "n_none", len(tec) - len(finite))
PY
```

**本机 stdout（0.2 / tip `8783a71`，2026-09-24 06:42 EDT）：**

```text
n_maps 12
first 2000-01-01 01:00:00 last 2000-01-01 23:00:00
shell_km 450.0 lat Latitude(lat1=87.5, lat2=-87.5, dlat=-2.5) lon Longitude(lon1=-180.0, lon2=180.0, dlon=5.0)
nlat 71 nlon 73 tec_len 5183 match True
tec0 9.8 tec_mid 31.8
tec_min 0.0 tec_max 117.60000000000001 n_none 287
```

头字段交叉：`INTERVAL 7200`、`# OF MAPS 12`、`HGT 450`、`EXPONENT -1`、有 `END OF FILE`。`tec` **已按 EXPONENT 还原**（勿再 `/10`）。

| 属性 | 含义 |
| --- | --- |
| `epoch` | `datetime`；对齐观测前统一时系 |
| `height` | 常为 `Height(hgt1,hgt2,dhgt)`；取 `hgt1` |
| `grid.latitude/longitude` | `*1,*2,d*`；**禁止写死 71×73** |
| `tec` | 一维 list；长度 = nlat×nlon；可含 **`None`** |
| `rms` | 本包未实现 → `NotImplementedError` |

库外 reshape：`np.asarray(..., dtype=float)` 前先处理 `None`（掩膜或填 NaN）。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IONEX **文本** | `.i` / 分析中心名；**gzip 先 `gunzip`** |
| `reader(file)` | `str` 路径或文本 file 对象 |

| 输出 | 说明 |
| --- | --- |
| `IonexMap` 流 | epoch / height / grid / tec |
| 不输出 | 写回、球谐、STEC、ROTI、RMS 图 |

## 5. 接到哪步

1. 下载产品 → [data-access](../data-access.md)  
2. 读图 → **本文**（旧文件名交叉 [ionex-gim](./ionex-gim.md)）  
3. Rust 服务/写回 → [ionex-rs](./ionex-rs.md)  
4. 两图并排 → [diffionmap](./diffionmap.md)  
5. 粗/校准 TEC → [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)；RINEX → [georinex](./georinex.md)  
6. 课：[03](../tutorials/03-gim-ionex.md) / [18](../tutorials/18-lab-compare-gims.md)

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `pip install ionex` 无分布 | 未上 PyPI | `git+https://github.com/gnss-lab/ionex.git` |
| 2 | 与 `cargo add ionex` 搞混 | 同名异栈 | Python→本文；Rust→[ionex-rs](./ionex-rs.md) |
| 3 | `next(reader(path))` TypeError | 返回可迭代非 iterator | `next(iter(…))` / `for` |
| 4 | reshape 炸 | 写死 71×73 | 用 `grid` 算 nlat/nlon |
| 5 | `min(tec)` TypeError | 含 `None` | 先滤 `finite` 或掩膜 |
| 6 | `m.rms` 崩 | 未实现 | 勿读；有 RMS 图换其它工具 |
| 7 | TECU 差 10× | 又乘 EXPONENT | 信任 `tec`；对照头 |
| 8 | 首行 HTML | 下载成登录页 | `head`；重走 Earthdata |
| 9 | gzip 当明文 | 未解压 | `file` / `gunzip` |
| 10 | 当本包生成 GIM | 边界错 | → 求解器；[sh-gim](./sh-gim.md) |
| 11 | 与 STEC 强行相等 | 对象不同 | 只比趋势量级 |
| 12 | 经度 0–360 vs ±180 | 约定打架 | 插值前统一 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Python 读 IGS 等 IONEX | **本文** |
| 旧手册文件名/交叉 | [ionex-gim](./ionex-gim.md) |
| Rust 解析/写回 | [ionex-rs](./ionex-rs.md) |
| 两中心差分可视化 | [diffionmap](./diffionmap.md) |
| RINEX→斜 TEC | [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) |

## 8. 相关

[ionex-gim](./ionex-gim.md) · [ionex-rs](./ionex-rs.md) · [georinex](./georinex.md) · [gnss-tec](./gnss-tec.md) · [pytecgg](./pytecgg.md) · [diffionmap](./diffionmap.md) · [sh-gim](./sh-gim.md) · [data-access](../data-access.md) · [README](./README.md)
