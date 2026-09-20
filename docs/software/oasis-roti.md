# OASIS（ROTI / ΔTEC / SIDX）

目录：[`PROJECTS.json` → `OASIS`](../../PROJECTS.json) · 上游 <https://github.com/giorgiopicanco/OASIS> · PyPI **`pyOASIS`**

## 用途

- Python 电离层工具箱：周跳/粗差、弧段 GF leveling，导出 **ROTI、ΔTEC、SIDX**。
- 回答「夜间有无泡状不规则体？」「磁暴 TEC 扰动大不大？」——从 RINEX+同日 SP3 出按卫星时序。
- **不做：** 硬件 S4/σφ；不替代 GIM。目录另有 `igs-roti` 等，本页深讲 OASIS。

| 术语 | 含义 |
|---|---|
| ROTI | TEC 变化率短窗（常见 1 min）标准差 |
| ΔTEC | 不同平滑窗 TEC 差（上游约 15 vs 60 min） |
| SIDX | 短时 \|ROT\| 均值类指数 |
| GF leveling | 相位 GF 对齐到码/弧段 |
| IPP | 穿刺点 |
| SP3 | 精密星历（算 IPP） |

## 安装

Python ≥ 3.8；依赖含 numpy、pandas、georinex、astropy、pyproj 等。

```bash
pip install -U pip pyOASIS
python -c "import pyOASIS; print('ok')"
# 或克隆后：pip install -r requirements.txt
```

源码流水线（`main.py` + `*_CALC.py`）按仓库 README 准备 `INPUT/` 或自备 RINEX+SP3。

## 快速上手

**路线 A：上游脚本（跟 README）**

```bash
# 1) OBS + 同日 MGEX SP3 放入 INPUT/
# 2) 在 main.py 填站名、年、DOY、路径
python3 main.py
```

| 步骤 | 脚本（名以仓库为准） | 作用 |
|---|---|---|
| 轨道 | `SP3_INTERPOLATE.py` | SP3 插到观测历元 |
| 清洗 | `RNX_CLEAN.py` | 读 RINEX、IPP、初标周跳 → `.RNX1` |
| 精筛 | `RNX_SCREENING.py` | MW 等 → `.RNX2` |
| 对齐 | `RNX_LEVELLING.py` | GF leveling → `.RNX3` |
| 指标 | `ROTI_CALC.py` / `DTEC_CALC.py` / `SIDX_CALC.py` | 出指标 |

**路线 B：只确认包可导入**

```bash
python -c "import pyOASIS; print('pyOASIS import ok')"
```

**预期：** 按卫星写出 leveled GF 与 ROTI/ΔTEC/SIDX；缺 SP3 会在轨道步失败。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX v2/v3 OBS（文档侧重 15/30 s）；MGEX SP3 |
| 中间 | `.RNX1`→`.RNX3` 等 |
| 输出 | leveled GF；ROTI/ΔTEC/SIDX；示例图 |

重点：GPS、GLONASS（Galileo/BeiDou 以上游标注为准）。不依赖 DCB/全球 TEC 图即可出上述指数。

## 常用参数

以 `main.py` / 各脚本内配置为准：站名、年、DOY、输入输出路径、采样与窗口。改窗口后勿与文献硬比数值。

## 接到工作流哪一步

- 路径 B；教程 [05](../tutorials/05-scintillation-roti.md)·[19](../tutorials/19-phenomena-overview.md)·[21](../tutorials/21-equatorial-anomaly-bubbles.md)
- 读盘：[georinex](./georinex.md)；另一套指标：[ionomoni](./ionomoni.md)
- 数据：[data-access](../data-access.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 缺 SP3 | 下同日 MGEX SP3 |
| 采样非 15/30 s | 先抽稀；高采样自评估窗口 |
| 只有单频 | 换双频站/日 |
| ROTI 高≠闪烁 | ROTI≠S4；见 [05](../tutorials/05-scintillation-roti.md) |
| 许可 CC BY-NC | 商业用途先读 LICENSE |
| 与 IonoMoni 数值差 | 算法窗口不同；比趋势 |

## 相关工具

[ionomoni](./ionomoni.md) · [georinex](./georinex.md) · [iono-scintillation](./iono-scintillation.md)

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
