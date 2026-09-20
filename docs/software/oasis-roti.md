# OASIS · 从 RINEX 算 ROTI / ΔTEC / SIDX

目录条目：[`PROJECTS.json` → `OASIS`](../../PROJECTS.json) · 上游 <https://github.com/giorgiopicanco/OASIS>  
PyPI 包名：**`pyOASIS`**

## 作用与场景

**它是什么**：面向电离层研究的开源 Python 工具箱（Open-Access System for Ionospheric Studies）。从多频 GNSS 观测做周跳/粗差处理、弧段几何无关（GF）leveling，再导出 **ROTI、ΔTEC、SIDX** 等指标。

**它解决什么**：你想对某站某日回答「晚上有没有赤道等离子体泡一类不规则体？」「磁暴时 TEC 扰动大不大？」——直接从 RINEX（加同日 SP3）跑出**按卫星的时间序列指标**，而不必从零实现 ROTI 定义。

**不负责**：专用闪烁接收机的 S4 / σφ 硬件指数；也不替代 GIM。高采样硬件闪烁仍看 ISMR 等数据源。

> 索引说明：目录中另有 `igs-roti`、`roti-gnss-ml` 等；本页**深讲 OASIS**（与本仓电离层扰动课最贴、流水线完整）。

## 术语｜人话

| 术语 | 人话 |
|---|---|
| ROTI | TEC 变化率在短窗口（常见 1 分钟）内的标准差——不规则体活动指标 |
| ΔTEC | 用不同平滑窗口差出来的 TEC 异常指数（上游：约 15 min 与 60 min 均值之差） |
| SIDX | 短时 \|ROT\| 均值一类指数，对突发扰动更敏感 |
| GF leveling | 把相位几何无关组合对齐到码/弧段，减弱模糊度台阶 |
| IPP | 穿刺点：信号穿过电离层壳层的地理位置 |
| SP3 | 精密星历；OASIS 用来插值卫星位置算 IPP 等 |

## 安装

上游要求 **Python ≥ 3.8**；依赖含 `numpy`、`pandas`、`georinex`、`astropy`、`pyproj` 等。

```bash
python3 -m pip install -U pip
python3 -m pip install pyOASIS
# 或以当前上游为准：克隆后 pip install -r requirements.txt
```

若走源码流水线（`main.py` + 各 `*_CALC.py`），请按仓库 README 取得示例 `INPUT/` 或自备 RINEX+SP3。

## 最小可跑命令

### 路线 A：按上游仓库脚本（推荐跟 README）

```bash
# 1) 将 OBS（如 data/sample.obs）与同日 MGEX SP3 放进 INPUT/
# 2) 在 main.py 中填写站名、年、DOY、输入输出路径（以当前上游为准）
python3 main.py
```

流水线模块（文件名以仓库为准）：

| 步骤 | 脚本 | 作用（人话） |
|---|---|---|
| 轨道 | `SP3_INTERPOLATE.py` | SP3 插值到观测历元 |
| 清洗 | `RNX_CLEAN.py` | 读 RINEX、IPP、初标周跳/缺口 → `.RNX1` |
| 精筛 | `RNX_SCREENING.py` | MW 残差等精化弧段 → `.RNX2` |
| 对齐 | `RNX_LEVELLING.py` | 弧段 GF leveling → `.RNX3` |
| 指标 | `ROTI_CALC.py` / `DTEC_CALC.py` / `SIDX_CALC.py` | 出 ROTI、ΔTEC、SIDX |

### 路线 B：仅确认包可导入

```bash
python3 -c "import pyOASIS; print('pyOASIS import ok')"
# 具体 API 入口若随版本变化，以当前上游文档与包内示例为准
```

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX v2/v3 观测（文档侧重 15/30 s）；MGEX **SP3** 精密轨道 |
| 中间 | 按站/星组织的 `.RNX1`→`.RNX3` 等（详见上游） |
| 输出 | 各卫星 leveled GF 序列；ROTI / ΔTEC / SIDX；示例图 |

支持重点：GPS、GLONASS（Galileo/BeiDou 上游标注为后续）。**不依赖 DCB 或全球 TEC 图**即可出上述指数（与绝对 STEC 标定场景不同）。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 缺 SP3 跑不下去 | 流水线要精密轨道 | 按 [data-access](../data-access.md) / CDDIS MGEX 下载同日产品 |
| 采样不是 15/30 s | 与设计假设不符 | 先抽稀/确认；高采样需自己评估窗口 |
| 只有单频 | 无法做双频 GF | 换双频站或换日 |
| ROTI 很高但未必闪烁 | ROTI≠S4 | 读 [05 课](../tutorials/05-scintillation-roti.md) 区分指标 |
| 许可 | CC BY-NC 4.0 | 商业用途先读上游 LICENSE |

## 接到电离层分析哪一步

- 指标含义与现象 → [05 · 闪烁与 ROTI](../tutorials/05-scintillation-roti.md) · [19 现象总览](../tutorials/19-phenomena-overview.md) · [21 赤道异常/气泡](../tutorials/21-equatorial-anomaly-bubbles.md)  
- RINEX 先读通 → [georinex](./georinex.md) · [02](../tutorials/02-gnss-dualfreq-tec.md)  
- 数据下载 → [数据怎么下](../data-access.md)

## 目录指针

- `PROJECTS.json`：`name=OASIS` · `url=https://github.com/giorgiopicanco/OASIS`  
- 相关：`OASIS-ohm1122`、`igs-roti`（本页不展开）
