# georinex · 把 RINEX 读进 Python

目录条目：[`PROJECTS.json` → `georinex`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/georinex>

## 作用与场景

**它是什么**：Python 库，把 RINEX 观测（OBS）、导航（NAV）以及 SP3 精密星历读成内存里的 `xarray.Dataset`，也可批量转成 NetCDF4/HDF5。

**它解决什么**：你刚下到一堆 `.obs` / `.rnx` / `.crx.gz`，想在 Python 里看「有哪些历元、哪些卫星、有没有 L1/L2」，而不是先写自己的文本解析器。电离层流程里，它常作为 **RINEX → 抽双频观测 → 再算 STEC/ROTI** 的第一步。

**不负责**：不直接输出 STEC/TEC 产品；不算定位；不替代质检工具（GFZRNX/Anubis 等）。

## 术语｜人话

| 术语 | 人话 |
|---|---|
| RINEX OBS | 观测文件：每个历元各卫星的伪距、载波相位等 |
| RINEX NAV | 导航/广播星历：卫星轨道与钟差的「广播版」 |
| epoch（历元） | 一次时间戳上的观测快照 |
| observation types | 观测量代号，如 `C1C`（码）、`L1C`/`L2W`（相位）；RINEX 3 更规范 |
| Hatanaka / `.crx` | 观测文件的差分压缩格式；georinex 可借助 `hatanaka` 无缝读取 |
| SP3 | 精密星历/钟差文件（分析中心产品，比广播更准） |
| `xarray.Dataset` | 带坐标的多维表：可按 `time`、`sv` 索引 |

## 安装

上游要求 **Python ≥ 3.10**（以 `pyproject.toml` 的 `requires-python` 为准）。

```bash
python3 -m pip install -U pip
python3 -m pip install georinex
# 可选：自检（需测试依赖）
# python3 -m pip install 'georinex[tests]' && python3 -m pytest
```

可复现骨架（建议在虚拟环境里）：

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install 'georinex==*'   # 锁定版本时改成具体号，如 ==1.x.y
python3 -c "import georinex as gr; print(gr.__file__)"
```

## 最小可跑示例

路径用占位符；请换成你自己的文件。**不要**假设本仓附带了真实测站数据。

### 1）读 OBS，看历元与卫星

```python
import georinex as gr

# 以当前上游文档为准：统一入口是 gr.load
obs = gr.load("data/sample.obs")   # 也可 .rnx / .yyo / .crx.gz 等

print(obs)                 # 看有哪些数据变量与坐标
print(obs.time.values[:5]) # 前几个历元时间
print(obs.sv.values)       # 卫星列表，如 G01、E05
# 若存在某观测量（名称随文件头而变）：
# print(obs["L1C"].sel(sv="G01").values[:10])
```

只读一段时间、只保留某些系统或观测量，可减小内存（参数名以当前上游为准）：

```python
obs = gr.load(
    "data/sample.obs",
    tlim=["2023-02-18T12:00", "2023-02-18T13:00"],
    use="G",          # 例：只要 GPS；亦常见 use=['G','E']
    # meas="L1C",     # 例：只要某类观测量（CLI 里对应 -m）
)
```

### 2）读 NAV 或 SP3

```python
nav = gr.load("data/sample.nav")   # 广播星历
# sp3 = gr.load("data/sample.sp3") # 精密星历（上游支持 SP3-a/c/d）
print(nav)
```

### 3）命令行快速窥视

```bash
python3 -m georinex.read data/sample.obs
python3 -m georinex.gtime data/sample.obs    # 只看时间轴，排错用
# 批量转 NetCDF（后缀规则以当前上游为准）
# python3 -m georinex.rinex2hdf5 data "*o" -o data
```

## 输入 / 输出

| 方向 | 类型 | 说明 |
|---|---|---|
| 输入 | RINEX 2 / 3 / 4 OBS、NAV；`.gz` / `.Z` / `.bz2` / `.zip`；Hatanaka `.crx(.gz)`；已转换的 `.nc`；SP3 | 纯文本流亦可（高级用法） |
| 内存输出 | `xarray.Dataset` | 便于按时间/卫星切片、转 DataFrame、画图 |
| 文件输出 | NetCDF4（HDF5 子集） | 大文件建议先转 `.nc` 再反复读 |

读结果时先看：坐标维（`time`、`sv` 等）、数据变量是否覆盖你要的双频相位/伪距、属性里是否有近似测站坐标（`position` 一类，视文件头而定）。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| RINEX 2 与 3 观测量名字对不上 | 版本与头文件定义不同 | 先 `print(obs)` / 看头；按文件实际代号选列 |
| `.crx.gz` 读失败 | 缺 Hatanaka 依赖或损坏 | 确认 `hatanaka` 已随包安装；先解压试读 |
| 缺 L2 / 缺某 `meas` | 接收机未记或被过滤 | 换站/换天；`use`/`meas` 不要滤掉唯一可用频点 |
| 内存爆 | 整天多系统高采样整文件载入 | 用 `tlim`、`use`、`meas`；或先转 NetCDF 再窗口读 |
| 时间和预期差几秒～整小时 | GPS 时 / UTC / 地方时混淆 | 用 `gtime` 看轴；与 IONEX、GIM 对齐前统一到 UTC 或 GPS 时 |
| OBS3 很慢 | 大文件 + 全观测量 | 缩小系统与观测量；考虑先抽样或转 `.nc` |

## 接到电离层 / GNSS 哪一步

1. 用本页把 OBS 读通 →  
2. [02 · 双频 GNSS 怎么估 TEC](../tutorials/02-gnss-dualfreq-tec.md)（几何无关、DCB 预告）→  
3. 需要全球图对照时 → [03 · GIM / IONEX](../tutorials/03-gim-ionex.md) 与 [ionex-gim.md](./ionex-gim.md) →  
4. 数据从哪下 → [数据怎么下](../data-access.md)

扰动指标流水线也可把 georinex 当底层读盘（例如 OASIS 依赖 georinex）→ [oasis-roti.md](./oasis-roti.md)。

## 目录指针

- `PROJECTS.json`：`name=georinex`  
- `url=https://github.com/geospace-code/georinex`
