# gnss-scintillation-simulator · 闪烁相位/振幅仿真（深讲）

目录条目：[`PROJECTS.json` → `gnss-scintillation-simulator`](../../PROJECTS.json) · 上游 <https://github.com/cu-sense-lab/gnss-scintillation-simulator>  
相关：`gnss-scintillation-simulator_2-param`（两参数版，本页不展开） · 列表：[01 电离层](../../lists/01-ionosphere.md)

## 作用与场景

**它是什么**：CU Sense Lab 的 **GPS 频段电离层闪烁仿真**工具箱（主要 **MATLAB**）。基于相位屏/传播理论，生成闪烁下的复信号场、振幅与相位时间序列，并附带香港等地例程数据。

**它解决什么**：在可控 **S4、相关时间** 等条件下**合成闪烁**，服务接收机算法、航空可用性或教学——而不是从 RINEX 提取 ROTI。

**分工：**

| 需求 | 更合适的工具 |
|---|---|
| 从 RINEX 算 ROTI / ΔTEC | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| 硬件 S4 / σφ 监测产品 | ISMR 等数据源；目录中的监测类软件 |
| 可控仿真闪烁场 | **本仓库（本页）** |

**不负责：** RINEX 批处理质检；也不替代 GIM。

## 安装

1. 安装 **MATLAB**（常规数值与绘图；具体工具箱以例程报错为准）。  
2. 克隆：

```bash
git clone https://github.com/cu-sense-lab/gnss-scintillation-simulator.git
cd gnss-scintillation-simulator
```

3. 在 MATLAB 中把 `matlab/` 各子目录加入路径；例程在 `examples/`。根 README 很短——**入口以 `examples/Main.m`、`examples/README.docx`、`docs/TechnicalManual.docx` 为准**。

## 最小可跑命令（MATLAB）

```matlab
cd examples
% 按仓库说明 addpath（若有 SetPath4GPS.m 等则先运行）
edit Main.m      % 查看并修改 userInput
Main             % 运行
```

`Main.m` 中典型可调字段（**名称以你克隆的文件为准**）：

| 字段 | 含义 |
|---|---|
| `userInput.dateTime` | `[年 月 日 时 分 秒]` |
| `userInput.length` | 时长（例程常见 300/600/900 s） |
| `userInput.RXPos` | ``[纬(rad), 经(rad), 高(m)]`` |
| `userInput.RXVel` | 东/北/天速度 (m/s) |
| `userInput.PRN` | GPS PRN |
| `userInput.frequencyNo` | 1=L1；2=L1+L2；3=L1+L2+L5 |
| `userInput.S4` / `tau0` | 地面 S4 与强度相关时间 |
| `userInput.plotSign` | 是否出图 |

调用链概览（便于对照源码）：`ParaMapping` → `RunPropGeomCalc` → `RunGenScintFieldRealization` → `Scin_psi / Scin_amp / Scin_phi`。

**例程数据：** `example-data/` 中 Septentrio 闪烁接收机转成的 `.mat`（香港、秘鲁等）。变量说明见该目录 README，可用于「仿真 vs 实测形态」对比。

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | `userInput` 几何与闪烁参数；可选例程 `.mat` |
| 输出 | 闪烁复场 / 振幅 / 相位；例程图；中间几何量 |
| 文档 | `docs/PropagationTheory.pdf`、`TechnicalManual.docx`、Carrano 等论文 PDF |

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 找不到函数 | 路径未加全 | 对 `matlab/` 递归 `addpath`；以实际目录树为准 |
| 和 ROTI「对不上」 | 物理量不同 | ROTI 来自 TEC 变化率；本工具直接仿真信号起伏 → [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) |
| 没有 Python 包 | 项目定位就是 MATLAB | 实测指标用 OASIS / IonoMoni |
| 许可混杂 | 含 MATLAB Central / Wavelab 等子集 | 再分发前读各子目录 LICENSE |

## 接到哪一步分析

- 闪烁与 ROTI 概念 → [05](../tutorials/05-scintillation-roti.md) · [21 赤道异常/气泡](../tutorials/21-equatorial-anomaly-bubbles.md)  
- 闪烁建模课 → [13 · 闪烁建模](../tutorials/13-scintillation-modeling.md)  
- 实测指标 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)

## 目录指针

- `PROJECTS.json`：`gnss-scintillation-simulator` · 相关：`gnss-scintillation-simulator_2-param`、`OASIS`、`IonoMoni`
