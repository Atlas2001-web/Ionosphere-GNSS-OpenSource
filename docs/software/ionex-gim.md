# IONEX / GIM · 用 Python `ionex` 读全球电离层图

目录条目：[`PROJECTS.json` → `ionex`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/ionex>

## 作用与场景

**GIM（Global Ionospheric Map）** 是分析中心发布的全球垂直 TEC 格网；交换格式多为 **IONEX**（`.inx` / 常见命名如 `igsgDDD0.YYi`）。

**本页主讲**：轻量 Python 模块 **`ionex`（gnss-lab）**——把 IONEX **读进 Python**，按历元取出 TEC 格网，便于和自己的 STEC/穿刺点结果对照、画图或插值。

**它解决什么**：你已经会下 CODE/IGS/UPC 等 GIM，但打开文件是一大坨文本；需要「按时间拿出一张图」的几行代码。

**不负责**：不生成 GIM；不算接收机 STEC；不替代球谐建模软件。

### SH-GIM（仅指针，不展开）

本仓维护者另有 MATLAB 球谐 GIM 实现 [`SH-GIM`](https://github.com/Atlas2001-web/SH-GIM)，目录已收录但**此处不介绍安装与源码**。需要请直接看该仓库 README。

## 术语｜人话

| 术语 | 人话 |
|---|---|
| IONEX | 电离层交换格式：多张「世界 TEC 地图」按时间排列 |
| GIM | 全球电离层图产品（常以 IONEX 发布） |
| TEC / VTEC | 垂直方向电子柱含量（格网点上的值） |
| 格网 | 经纬度步长（如 2.5°×5°）+ 参考高度壳层 |
| epoch | 这一张图对应的时刻 |

## 安装

上游 README 推荐 editable 安装（PyPI 情况以当前上游为准）：

```bash
python3 -m pip install -U pip
python3 -m pip install -e "git+https://github.com/gnss-lab/ionex.git#egg=ionex"
python3 -c "import ionex; print('ok')"
```

依赖很少（`setup.py` 中 `install_requires` 为空）；建议 Python 3。

## 最小可跑示例

文件请自行从 CDDIS `gnss/products/ionex/` 等下载（见 [data-access](../data-access.md)）。占位路径：

```python
import ionex

# 以当前上游文档为准：ionex.reader → 迭代 IonexMap
with open("data/sample.inx") as f:
    for ionex_map in ionex.reader(f):
        print(ionex_map.epoch)   # datetime
        print(ionex_map.height)  # 壳层高度
        tec = ionex_map.tec      # 一维 list：按纬向切片拼成的 TEC
        # grid 定义纬度/经度起止与步长（属性名见上游：grid.latitude / grid.longitude）
        print(ionex_map.grid)
        break  # 先看第一张图
```

对照自站 TEC 时：取与穿刺点时间最近的一张图 → 按经纬度在 `tec` 格网中插值（插值需自写或用 scipy；本库只负责读入）。

## 输入 / 输出

| 方向 | 说明 |
|---|---|
| 输入 | IONEX 文本（路径或已打开的 file 对象） |
| 输出 | 迭代得到的 `IonexMap`：`epoch`、`tec`、`height`、`grid` |
| 异常 | 未知类型/版本、文件截断、单图解析错误（见上游 `IONEXError` 等） |

`tec` 的排布：一维列表，由多个「固定经度上的纬度剖面」拼接；起止步长读 `grid`。**不要假设**它已是 `numpy` 二维阵——需要时自行 `reshape`。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 与自算 STEC 差一截 | DCB、映射函数、壳层高度、时间未对齐 | 先读 [03 课](../tutorials/03-gim-ionex.md)；统一时间系统 |
| 文件读到一半报错 | 下载不完整或非 IONEX | 核对 CDDIS 校验；确认是 `*.inx` 而非 HTML 错误页 |
| 只想「看一眼全球图」 | 可先用分析中心网页预览 | 本库适合可编程对照 |
| 需要写 IONEX / 更高阶 | `ionex` 只读 | 另寻 `ionex_formatter` 等目录条目 |

## 接到电离层分析哪一步

- 概念与对照方法 → [03 · GIM / IONEX](../tutorials/03-gim-ionex.md)  
- 自站双频 STEC → [02](../tutorials/02-gnss-dualfreq-tec.md) · [georinex](./georinex.md)  
- 下载门户 → [数据怎么下](../data-access.md) · 列表中的 CDDIS-IONEX 等

## 目录指针

- `PROJECTS.json`：`name=ionex` · `url=https://github.com/gnss-lab/ionex`  
- 相关：`ionex-analyzer`、`ionex_formatter`、`SH-GIM`（不展开）
