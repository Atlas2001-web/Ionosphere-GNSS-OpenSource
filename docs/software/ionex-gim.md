# ionex（读 IONEX GIM）

目录：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex>

## 用途

- 用 Python 包 **`ionex`** 读取分析中心 **IONEX** 全球电离层图（GIM）。
- 按历元取出 VTEC 格网，便于与自站 STEC/穿刺点对照、画图、插值。
- **不做：** 生成 GIM；不算接收机 STEC；不替代球谐建模。
- SH-GIM 边界见 [sh-gim](./sh-gim.md)（短述，不在此展开求解）。

## 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e "git+https://github.com/gnss-lab/ionex.git#egg=ionex
# 或：git clone … && pip install -e .
python -c "import ionex; print(ionex.__file__)"
pip install numpy scipy matplotlib   # 画图/插值常用
```

## 快速上手

```bash
# 0) 文件自检（必须是 IONEX，不是 HTML 登录页）
head -n 5 data/igsg0490.23i
grep -n "END OF FILE" data/igsg0490.23i | tail
```

```python
import ionex
from datetime import datetime

# 1) 读一张图
with open("data/igsg0490.23i") as f:
    m = next(ionex.reader(f))
print(m.epoch, m.height, m.grid.latitude, m.grid.longitude, len(m.tec))

# 2) 建历元索引
maps = {}
with open("data/igsg0490.23i") as f:
    for m in ionex.reader(f):
        maps[m.epoch] = m
times = sorted(maps)
print(len(times), times[0], times[-1])

# 3) 最近邻历元
t_obs = datetime(2023, 2, 18, 14, 5, 0)
t_map = min(times, key=lambda u: abs((u - t_obs).total_seconds()))
print(t_obs, t_map, (t_map - t_obs).total_seconds())
```

格网 reshape / 双线性插值：按 `grid` 的 lat/lon 步长计算 `nlat,nlon`，断言 `len(tec)==nlat*nlon` 再 reshape；插值在库外完成（教程 [03](../tutorials/03-gim-ionex.md)/[18](../tutorials/18-lab-compare-gims.md)）。

**预期：** `epoch` 为 datetime；`tec` 为一维格网值；地球数据门户若下到 HTML，`reader` 会解析失败——先 `head` 自检。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | IONEX 文本（`.i` / `.inx` 等）；IGS/CODE/UPC 等产品 |
| 输出 | 迭代得到的 map 对象（epoch/height/grid/tec） |
| 不做 | 写回 IONEX；球谐反演 |

## 常用参数

本包以 **reader 迭代** 为主，几乎无复杂 CLI。注意：

| 项 | 说明 |
|---|---|
| 产品类型 | 快速/最终勿混用却不标注 |
| `tec` 单位 | 头文件比例尺（常见 0.1 TECU） |
| `grid` | 勿写死 71×73；只从文件读 |
| RMS 图 | 勿把 RMS map 当 TEC |

## 接到工作流哪一步

- 路径 A/E：与 [pytecgg](./pytecgg.md) VTEC 对照；教程 [03](../tutorials/03-gim-ionex.md)/[18](../tutorials/18-lab-compare-gims.md)
- 数据：[data-access](../data-access.md) · CDDIS `gnss/products/ionex/`
- 自建求解边界：[sh-gim](./sh-gim.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 解析失败 | `head` 是否 HTML；检查 Earthdata 登录下载 |
| reshape 报错 | 用文件内 dlat/dlon 算维度 |
| 与 STEC「对不上」 | GIM=壳层 VTEC；观测=斜向+DCB；比趋势勿强行相等 |
| 混用快速/最终 | 日志写清产品 ID |
| 想生成 GIM | 本包不负责；看开源 GIM 列表 |

## 相关工具

[pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md) · [georinex](./georinex.md)

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
