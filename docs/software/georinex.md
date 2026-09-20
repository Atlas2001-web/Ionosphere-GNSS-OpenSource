# georinex

目录：[`PROJECTS.json` → `georinex`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/georinex> · MIT

## 用途

- 把 RINEX OBS/NAV（及常见 gzip / Hatanaka）读成 **xarray.Dataset**。
- 探活：时间覆盖、卫星列表、双频观测量是否成对。
- **不做**校准 TEC、ROTI、RTK、QC PDF。
- 电离层链的「读盘第一棒」。

## 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip georinex hatanaka
python -c "import georinex as gr; print(gr.__file__)"
```

要求：Python ≥ 3.10（以 PyPI 为准）。`.crx` 需 `hatanaka`（或系统 `CRX2RNX`）。

## 快速上手

```bash
# 1) 时间范围
python -m georinex.gtime data/sample.obs

# 2) 读 OBS
python -c "import georinex as gr; obs=gr.load('data/sample.obs'); print(obs); print(list(obs.data_vars)[:12])"

# 3) 过滤（省内存）
python -c "import georinex as gr; obs=gr.load('data/sample.obs', use='G', tlim=('2024-01-01','2024-01-01T06:00')); print(obs.sizes)"

# 4) NAV + NetCDF 缓存
python -c "import georinex as gr; nav=gr.load('data/brdc.n'); obs=gr.load('data/sample.obs'); obs.to_netcdf('data/sample.nc'); print(nav, gr.load('data/sample.nc').sizes)"
```

**预期：** Dataset 含 `time`/`sv`；变量名随 RINEX2/3 变化（`L1` vs `L1C`）。空文件或半截 gzip → 报错或 dims=0。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX 2/3/4 OBS、NAV；`.gz`；Hatanaka `.crx`；可选 SP3；已有 `.nc` |
| 输出 | `xarray.Dataset`；可选 NetCDF |
| 不做 | IONEX、ROTI、pos、校准 TEC |

## 常用参数

| API / CLI | 作用 |
|---|---|
| `gr.load(..., use=, tlim=, meas=)` | 系统、时间窗、观测量过滤 |
| `python -m georinex.gtime` | 只看时间覆盖 |
| `obs.to_netcdf` / `gr.load(.nc)` | 缓存加速 |

RINEX3 变量名带跟踪码；过滤时勿照抄 RINEX2 名。先 `print(list(obs.data_vars))`。

## 接到工作流哪一步

- 上游：[data-access](../data-access.md)；可选清洗 [gfzrnx](./gfzrnx.md)、QC [anubis](./anubis.md)
- 下游：校准 TEC [pytecgg](./pytecgg.md)；ROTI [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)；定位 [rtklib](./rtklib.md)
- 教程：[02](../tutorials/02-gnss-dualfreq-tec.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| `.crx` 读失败 | `pip install hatanaka` 或先转 RINEX |
| 1 Hz 内存爆 | `tlim`/`use`/`meas`；或 [gfzrnx](./gfzrnx.md) `-smp` |
| 变量名 KeyError | 先打印 `data_vars` |
| 相对 TEC 当绝对 | 用 [pytecgg](./pytecgg.md) |
| 坏 `.nc` 缓存 | 删 nc，从原始重读 |
| GPST/UTC 对不齐 | 明确时间系后再对 IONEX/事件 |
| 半截下载 | `gunzip -t` / 核对大小后再 load |

## 相关工具

[gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md)

## 操作检查清单

1. `import georinex` 成功。  
2. `gtime` 打印非空时间范围。  
3. `load` 后 `time`/`sv` 维 > 0。  
4. 双频任务：`data_vars` 中 L1/L2（或 L1C/L2W 等）成对。  
5. 大文件先 `tlim`/`use` 再全量。  
6. `.crx` 已装 `hatanaka`。  
7. 缓存 `.nc` 与源文件同源；源更新则删 nc。

## 预期 I/O 示例

```text
# gtime 示意
2024-01-01T00:00:00 … 2024-01-01T23:59:30

# print(obs) 示意
<xarray.Dataset>
Dimensions:  (time: 2880, sv: 32)
Data variables: L1C, L2W, C1C, C2W, …
```

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
