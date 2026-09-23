# gnss-scintillation-simulator · 闪烁仿真操作手册

目录：[`PROJECTS.json` → `gnss-scintillation-simulator`](../../PROJECTS.json) · 上游 <https://github.com/cu-sense-lab/gnss-scintillation-simulator> · 相关仓 `gnss-scintillation-simulator_2-param`（强闪烁两参数版，本页点到为止） · MATLAB · CU Sense Lab

> 岗位：在给定 **S4、τ0、几何** 下合成 GPS 频段振幅/相位闪烁实现。主战场 MATLAB。**不是**从 RINEX 提 ROTI。参数以 `examples/Main.m` / `docs/` 为准。

## 1. 用途与边界

**做：** 相位屏 + 传播几何 → 复场 / 振幅 / 相位时序；服务跟踪环压力测试、航空可用性概念、教程 [13](../tutorials/13-scintillation-modeling.md)。

**不做：** RINEX→ROTI/ΔTEC → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)；硬件 S4/σφ → ISMR；把仿真绝对值当成某站某日实测发表。

| 需求 | 工具 |
| --- | --- |
| 可控仿真闪烁场 | **本页** |
| 实测 ROTI | OASIS / IonoMoni |
| 硬件 S4 | ISMR |

## 2. 安装

```bash
git clone https://github.com/cu-sense-lab/gnss-scintillation-simulator.git
cd gnss-scintillation-simulator
ls examples docs matlab | head
```

MATLAB：

```matlab
cd(".../gnss-scintillation-simulator")
addpath(genpath("matlab"))
% 读 examples/Main.m、examples/README.docx、docs/TechnicalManual.docx
% 子目录含第三方代码 —— 再分发前读各 LICENSE
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Undefined function` | 未 addpath | `addpath(genpath("matlab"))` |
| 缺工具箱 | Signal/Mapping 等 | 按报错安装 |
| `RXPos` 结果离谱 | 纬度写成度 | 例程常用 **弧度** |

## 3. 端到端：改 userInput → 跑 Main

### 3.1 路径

```matlab
cd examples
addpath(genpath("../matlab"))
```

### 3.2 编辑输入

```matlab
edit Main.m
```

| 字段 | 含义 | 注意 |
| --- | --- | --- |
| `dateTime` | `[Y M D h m s]` | 几何/星历相关 |
| `length` | 时长（常见 300/600/900 s） | 过长吃内存 |
| `RXPos` | `[lat, lon, h]` | **常为弧度** + 米 |
| `RXVel` | ENU 速度 (m/s) | 静止填 0 |
| `PRN` | GPS PRN | 与分析对象一致 |
| `frequencyNo` | 1=L1；2=L1+L2；3=L1+L2+L5 | 与下游频点一致 |
| `S4` / `tau0` | 地面 S4 与强度相关时间 | **一次只改一个** |
| `plotSign` | 是否出图 | 关图时查工作区变量 |

### 3.3 运行

```matlab
Main
```

典型链（名以仓库为准）：`ParaMapping` → `RunPropGeomCalc` → `RunGenScintFieldRealization` → `Scin_psi` / `Scin_amp` / `Scin_phi`。

**期望：** 工作区出现振幅/相位（或复场）时序；`plotSign` 开则出图。

### 3.4 对照与下游

- `example-data/` 实测转 `.mat`：**只比形态**，不比绝对值。
- 概念课：[13](../tutorials/13-scintillation-modeling.md)；实测指数仍走 OASIS/IonoMoni/[05](../tutorials/05-scintillation-roti.md)。
- 两参数强闪烁：姐妹仓 `gnss-scintillation-simulator_2-param`（输出常见 `Scin_amp`/`Scin_phi` @ 100 Hz）——**文档不要混仓**。

## 4. 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | `userInput`；可选例程 `.mat` |
| 输出 | 复场/振幅/相位；图；几何中间量 |
| 不输出 | ROTI 产品、IONEX、RINEX |

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 仿真概念 | §3 | [13](../tutorials/13-scintillation-modeling.md) |
| 与实测指数对照 | §3.4 | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [05](../tutorials/05-scintillation-roti.md) |
| 路径 B 旁路 | — | 不替代实测 ROTI |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | Undefined function | 未 addpath | `addpath(genpath("matlab"))` |
| 2 | 与站日 ROTI「对不上」 | 物理量不同 | 仿真≠实测指数 |
| 3 | 找 Python 包 | 本仓是 MATLAB | 用 MATLAB 或换工具 |
| 4 | 再分发侵权 | 子目录第三方许可 | 读各 LICENSE |
| 5 | 几何离谱 | `RXPos` 用了度 | 按例程改弧度 |
| 6 | 无法归因 | 一次改多个参数 | 只改 S4 或只改 τ0 |
| 7 | 内存爆 | 时长过长 | 缩 `length` |
| 8 | 当实测发表 | 误解 | 文中标明 simulation |
| 9 | 忽略平台速度 | 几何不完整 | 填 `RXVel` 或显式静止 |
| 10 | 频点不一致 | `frequencyNo` 错 | 与分析 L1/L2/L5 对齐 |
| 11 | 无图以为失败 | `plotSign` 关 | 查工作区变量 |
| 12 | 两仓文档混用 | 1-param vs 2-param | 分仓记录版本 |
| 13 | Parallel 假设 | 未装工具箱 | 关并行或安装 |
| 14 | 路径含空格 | addpath 失败 | 换无空格路径 |
| 15 | 旧 MATLAB 语法错 | 版本过旧 | 升版本或改语法 |
| 16 | 只截图不存变量 | 无法复现 | `save` 结果 `.mat` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 可控闪烁仿真 | **本页** |
| 实测 ROTI | OASIS / IonoMoni |
| 硬件 S4 | ISMR |

## 8. 相关

[oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [pytecgg](./pytecgg.md) · [rtklib](./rtklib.md) · [README](./README.md) · [13](../tutorials/13-scintillation-modeling.md) · [05](../tutorials/05-scintillation-roti.md) · [data-access](../data-access.md)
