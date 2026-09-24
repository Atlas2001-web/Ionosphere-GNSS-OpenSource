# DiffIonMap · 两幅 IONEX 并排对照操作手册

目录：[`PROJECTS.json` → `DiffIonMap`](../../PROJECTS.json) · 上游 <https://github.com/Jin-Whu/DiffIonMap> · 许可 **unknown** · tip **`57ceb1d`**（2016-08-31，README 仍写 IonMap）· 本机验证：Py3 轻移植后读 `CODG0010.00I`/`WHUC0010.00I`（ionex 测试文件改名）→ 同 DOY 成组、12 张图、TEC mean≈24.84；另读 RTKLIB `IGRG3380.10I` → 13 张、mean≈13.367 TECU（2026-09-24 EDT）

> 岗位：把**两家分析中心 / 两套产品**的同 DOY IONEX 拉齐，**并排**画全球/区域 VTEC 图做肉眼对照。冲突时：**仓内源码 / `configure.ini` > 本文**。读单文件进 Python → [ionex-gim](./ionex-gim.md)；下载入口 → [data-access](../data-access.md)。

## 1. 用途与边界

**做：**

- `configure.ini` 配两路目录 + 四字符 `code` + 输出目录
- `retrieveIONEX` 按 `CODGddd0.YYi` 短名扫同 DOY；`retrievegroup` 取交集
- `ReadIONEX` 读 TEC MAP（遇 `START OF RMS MAP` 停）；`IONEXPlot` 用 **Basemap** 左右并排出 PNG

**不做：**

- **不是** 格点相减 ΔTEC 产品生成器——标题是 `CODG VS WHUC At …`，色标各自 `vmin=0,vmax=100`，**没有** `A−B` 图层
- **不** 下载 IONEX → [data-access](../data-access.md)；现代只读 API → [ionex-gim](./ionex-gim.md)
- **不** 写回 IONEX / 球谐建图 → [sh-gim](./sh-gim.md) 边界
- 上游是 **Python 2** + **Basemap**（久未更新）；本机无 Py2/Basemap 时只能做读路径冒烟（见 §3）

一句话：DiffIonMap = **两幅 IONEX 并排对照制图**（极简、停更）；要数值差分请自减或用 [ionex-gim](./ionex-gim.md)。

| 术语 | 含义 |
| --- | --- |
| `ioncode1/2` | 文件名前缀，如 `CODG`/`IGSG`/`WHUC` |
| 短名 | `CODGddd0.YYi`（DOY 后常为 `0`；正则靠「任意一字」吃掉它） |
| `retrievegroup` | 两路 `OrderedDict` 按 DOY 键求交 |
| `EXPONENT` | 写入时 `value * 10**exponent`；读后已是 TECU |
| VS 图 | 左右两幅原图，非差分图 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/Jin-Whu/DiffIonMap.git
cd DiffIonMap
# 上游无 setup.py；工作目录即包根（import ReadIONEX）
# 依赖（以源码 import 为准）：
#   Python 2.7 时代：numpy + matplotlib + basemap
# 现代：先自备 Py3 语法修补（print/map/except），再：
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip numpy matplotlib
# Basemap 已停止维护，conda-forge 偶可装；装不上则只能跑读路径（§3.2）
# conda install -c conda-forge basemap   # 可选
python -c "import numpy; print('numpy', numpy.__version__)"
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `print '…'` SyntaxError | 源码是 Py2 | 全面加 `print(...)`，或 `2to3 -w *.py` |
| `No module named mpl_toolkits.basemap` | 无 Basemap | conda-forge 装；或只跑读路径 |
| `map object is not subscriptable` | Py3 `map` 返回迭代器 | `list(map(...))`（`lat_range`/`lon_range`） |

## 3. 端到端：配置 → 扫文件 → 读图（本机真跑）

### 3.1 准备两路同 DOY 短名

经典短名：**`{CODE}{DOY}0.{YY}I`**（例 `CODG0010.00I`）。正则：`code + r'(\d\d\d).\.\d+I'`——第三个 `\d\d\d` 后的 `.` 匹配 DOY 后的 `0`。

```bash
mkdir -p /tmp/diffion_e2e/{codg,whuc,igrg,out}
# 冒烟：ionex 包测试文件改名成两路同 DOY（内容相同 → 自差为 0）
cp ionex-src/tests/test_data/ionex_file.00i /tmp/diffion_e2e/codg/CODG0010.00I
cp ionex-src/tests/test_data/ionex_file.00i /tmp/diffion_e2e/whuc/WHUC0010.00I
# 真产品样例（RTKLIB 仓内 IGS 组合图）
cp RTKLIB/test/data/sp3/igrg3380.10i /tmp/diffion_e2e/igrg/IGRG3380.10I
```

生产数据：按 [data-access](../data-access.md) 取 CDDIS/CAS/CODE IONEX，解压后放进两目录，**文件名必须带四字符 code + DOY**。

### 3.2 `configure.ini` + 读路径冒烟

```ini
; IonMap configure file  （行序写死：第 3–7 行被按位置解析，勿插注释行）
[path]
ionfilepath1 = /tmp/diffion_e2e/codg
ioncode1 = CODG
ionfilepath2 = /tmp/diffion_e2e/whuc
ioncode2 = WHUC
result = /tmp/diffion_e2e/out
```

```bash
cd ~/iono_ops/DiffIonMap && source .venv/bin/activate
# 若仍是 Py2 源码，先做最小 Py3 修补后再跑：
python - <<'PY'
import sys, numpy as np
sys.path.insert(0, ".")
import ReadIONEX  # 需已 Py3 化

f1 = ReadIONEX.retrieveIONEX("/tmp/diffion_e2e/codg", "CODG")
f2 = ReadIONEX.retrieveIONEX("/tmp/diffion_e2e/whuc", "WHUC")
print("codg", list(f1.keys()), "whuc", list(f2.keys()))
print("common_doy", list(ReadIONEX.retrievegroup([f1, f2]).keys()))
r = ReadIONEX.ReadIONEX(f1["001"]); assert r.read()
d = r.ionexdata; t = list(d.keys()); m0 = d[t[0]]
print("code", d.code, "n_maps", len(t), "first", t[0], "last", t[-1])
print("shape", m0.value.shape, "mean_TECU", round(float(np.nanmean(m0.value)), 2))
# IGRG 真图
f3 = ReadIONEX.retrieveIONEX("/tmp/diffion_e2e/igrg", "IGRG")
r2 = ReadIONEX.ReadIONEX(f3["338"]); assert r2.read()
d2 = r2.ionexdata; t2 = list(d2.keys()); m2 = d2[t2[0]]
print("igrg n", len(t2), "first", t2[0], "mean", round(float(np.nanmean(m2.value)), 3))
PY
```

**本机 stdout（2026-09-24 EDT，Py3 修补后）：**

```text
codg ['001'] whuc ['001']
common_doy ['001']
code CODG n_maps 12 first 2000-01-01 01:00:00 last 2000-01-01 23:00:00
shape (71, 73) mean_TECU 24.84
igrg n 13 first 2010-12-04 00:00:00 mean 13.367
```

| 字段 | 含义 |
| --- | --- |
| `common_doy` | 两路都能扫到的 DOY；空 → 文件名/code 不对 |
| `n_maps` 12 | 测试文件 2 h 间隔全日图 |
| `shape (71,73)` | 由 `LAT1/2/DLAT`×`LON1/2/DLON` 算出 |
| `mean 13.367` | IGRG 2010-338 首图平均 TECU（真产品） |

### 3.3 完整出图（需 Basemap）

```bash
# 配好 configure.ini 后：
python main.py
# 期望：All done! ；result/ 下多张
#   CODG-VS-WHUC-At-YYYY-mm-dd-HH-MM-SS.png
```

本机 **无 Basemap** → 未跑通 PNG；读路径已验证。有 Basemap 时色标固定 0–100 TECU，高纬冬至可能一片深色属正常。

### 3.4 若要真正的 ΔTEC（库外一行）

上游不提供。读完两份同历元 `value` 后：

```python
delta = map_a.value - map_b.value   # 同 shape；跨产品先对齐网格
print(float(np.nanmean(delta)), float(np.nanmax(np.abs(delta))))
```

同文件自减本机 `self_diff_absmax = 0.0`。跨 AC 差分叙事见教程 [18](../tutorials/18-lab-compare-gims.md)/[20](../tutorials/20-storm-tec-analysis.md)。

## 4. 接到哪步

- 只读一张图 / 现代 API → [ionex-gim](./ionex-gim.md)
- 下载 IONEX / 高采样 → [data-access](../data-access.md) · 高采样工具 [cddis-highrate-downloader](./cddis-highrate-downloader.md)
- 多 GIM 对照课 → [18](../tutorials/18-lab-compare-gims.md)；磁暴 ΔVTEC → [20](../tutorials/20-storm-tec-analysis.md)
- 球谐边界 → [sh-gim](./sh-gim.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `print '…'` / `e.message` 炸 | Py2 源码 | 改 `print(...)`；`str(e)` |
| 2 | `retrieveIONEX` 返回空 | 文件名不是 `CODGddd0.YYi` | `mv … CODG0010.24I`（注意 DOY 后的 `0`） |
| 3 | `common_doy` 空 | 两路 DOY 键不一致 | 确认两边都是同三位数 DOY |
| 4 | 以为出了差分图 | 实际是 VS 并排 | 看标题 `VS`；要 Δ 自减 `value` |
| 5 | `ImportError: basemap` | 依赖停更 | conda-forge；或只跑 §3.2 |
| 6 | `configure` 读失败 | 行序被打乱 | 保持第 3–7 行 `path/code/path/code/result` |
| 7 | 色标饱和 / 一片蓝 | 写死 `vmax=100` | 改 `IONEXPlot.py` 的 `vmin/vmax` |
| 8 | 只读到 TEC、无 RMS | 遇 RMS MAP 即 `break` | 预期行为；RMS 勿当 TEC |
| 9 | Py3 `lat_range` 异常 | `map` 未 `list()` | `lat_range = list(map(float, …))` |
| 10 | 跨快速/最终未标注 | 产品混淆 | 文件名/头写清 AC+产品档 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 两幅 IONEX **并排**出 PNG（极简） | **本文 DiffIonMap** |
| 读 IONEX → 网格 / 插值 | [ionex-gim](./ionex-gim.md) |
| 数值 ΔTEC / 风暴分析 | 自减 + [20](../tutorials/20-storm-tec-analysis.md) |
| 数据从哪下 | [data-access](../data-access.md) |

- 仓库：<https://github.com/Jin-Whu/DiffIonMap>
- 兄弟：[ionex-gim](./ionex-gim.md) · [data-access](../data-access.md) · [cddis-highrate-downloader](./cddis-highrate-downloader.md) · [sh-gim](./sh-gim.md) · 教程 [03](../tutorials/03-gim-ionex.md)/[18](../tutorials/18-lab-compare-gims.md)/[20](../tutorials/20-storm-tec-analysis.md)
