# gnss-scintillation-simulator · 闪烁仿真

目录：[`PROJECTS.json` → `gnss-scintillation-simulator`](../../PROJECTS.json) · 上游 <https://github.com/cu-sense-lab/gnss-scintillation-simulator> · 姐妹仓 `gnss-scintillation-simulator_2-param`（两参数版，本页点到为止） · MATLAB · CU Sense Lab · 质检机：**无 MATLAB/Octave**，命令与期望以仓库树 + `docs/TechnicalManual.docx` / `examples/Main.m` 为准（**不臆造控制台输出**）

> 岗位：在给定 **S4、τ0、几何** 下合成 GPS 频段振幅/相位闪烁实现。主战场 MATLAB。**不是**从 RINEX 提 ROTI。参数以 `examples/Main.m`、`docs/TechnicalManual.docx`、`examples/README.docx` 为准。

---

## 1. 用途与边界

**做：**

- 相位屏 + 传播几何 → 复场 / 振幅 / 相位时序（技术手册：约 **100 Hz**）
- 跟踪环压力测试、航空可用性概念、教程 [13](../tutorials/13-scintillation-modeling.md)

**不做：**

- RINEX→ROTI/ΔTEC → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
- 硬件 S4/σφ → ISMR
- 把仿真绝对值当成某站某日实测发表
- 校准 TEC → [pytecgg](./pytecgg.md)（viventriglia）

| 需求 | 工具 |
| --- | --- |
| 可控仿真闪烁场 | **本页** |
| 实测 ROTI | OASIS / IonoMoni |
| 硬件 S4 | ISMR |

---

## 2. 安装与仓库树（以 clone 为准）

```bash
git clone https://github.com/cu-sense-lab/gnss-scintillation-simulator.git
cd gnss-scintillation-simulator
ls
# 期望顶层：README.md  docs/  example-data/  examples/  matlab/
ls examples docs matlab | head
```

| 路径 | 内容 |
| --- | --- |
| `examples/Main.m` | 主入口：填 `userInput` → `ParaMapping` / `RunPropGeomCalc` / `RunGenScintFieldRealization` |
| `examples/SetPath4GPS.m` / `SetPath4PhaseScreenModel.m` | 相位屏例程路径（指向 `GPS_ToolBox_Libraries`） |
| `examples/GenerateGPSPhaseScreenRealization.m` 等 | 交互式相位屏/谱例程（`input(...)`） |
| `matlab/` | Ispectrum、PropCodes、Scintillation、IGRF、轨道与坐标变换等 |
| `docs/TechnicalManual.docx` | 配置与执行说明（必读） |
| `docs/PropagationTheory.pdf` / `Carrano_et_al-2016-Radio_Science.pdf` | 理论/文献 |
| `example-data/*.mat` | 实测转 mat（HongKong / Peru）；**只比形态** |

**打包事实（clone 后核对，勿跳过）：**

1. `TechnicalManual.docx` 写：程序目录含 `Main` 与名为 **`Libraries`** 的支撑函数目录。
2. 公开仓顶层是 **`matlab/`**，不是 `Libraries/`；`examples/Main.m` 用 `path2Libraries = [pwd '/Libraries']` 并 `addpath` `PropGeomCalc` / `GenScintFieldRealization` / `GPS_CoordinateXforms` / `IGRF_Compston` / `Utilities`。
3. 对本机 clone 查 `ParaMapping.m` / `RunGenScintFieldRealization.m`：若**找不到**，说明 Main 依赖的 Libraries **未随公开树完整发布**——先读手册与作者渠道补齐，或改用 `SetPath4*` + `GenerateGPSPhaseScreenRealization.m`；**不要假装 Main 已可一键跑通**。
4. 子目录含 MATLAB Central / Wavelab / IGRF 等——再分发前读各 `LICENSE.txt`。

MATLAB 侧（有许可证的机器）：

```matlab
cd(".../gnss-scintillation-simulator")
% 先按 TechnicalManual / Main.m 核对 Libraries 是否存在
cd examples
edit Main.m
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Undefined function 'ParaMapping'` | Libraries 未放入 / 路径错 | 对照手册补齐；或改 `addpath` |
| 其它 `Undefined function` | 未 addpath | 按 Main.m / SetPath4*.m；可试 `addpath(genpath("../matlab"))` |
| 缺工具箱 | Signal / Mapping / Parallel | 按报错安装；关并行 |
| `RXPos` 结果离谱 | 纬度写成度 | Main.m 注释：**弧度** + 高度米 |

---

## 3. 端到端：编辑 userInput → 跑 Main（上游约定）

字段与调用链摘自 **`examples/Main.m`** 与 **`docs/TechnicalManual.docx`**。质检机无 MATLAB，下列「期望」**不是**本机控制台抓取。

### 3.1 路径

```matlab
cd examples   % Main.m 假定 pwd == examples（Libraries 为 examples/Libraries）
% 确认 Libraries 子目录存在后再跑
```

### 3.2 编辑输入（Main.m 默认值）

| 字段 | Main.m 默认 / 含义 | 注意 |
| --- | --- | --- |
| `dateTime` | `[2014 01 02 10 00 00]` | `[Y M D h m s]` |
| `length` | `300` | 秒；手册常见 300/600/900 |
| `RXPos` | `[0.3876 1.9942 59.6780]'` | `[lat,lon,h]`，lat/lon **弧度**，h 米 |
| `RXVel` | `[100 0 0]'` | ENU m/s；静止填全 0（手册） |
| `PRN` | `1` | GPS PRN 0–32 |
| `plotSign` | `1` | 1=出图；0=只看工作区 |
| `frequencyNo` | `3` | 1=L1；2=L1+L2；3=L1+L2+L5 |
| `S4` | `0.8` | 地面 S4（0~1） |
| `tau0` | `0.7` | 强度相关时间（秒）；**一次只改一个** |

### 3.3 运行与调用链

```matlab
Main
```

1. `[U_mapped, rhoFVeff_mapped] = ParaMapping(userInput);`
2. 若 `sum(RXVel)~=0`：`satGEOM = RunPropGeomCalc(userInput, rhoFVeff_mapped);`
3. `[Scin_psi, Scin_amp, Scin_phi] = RunGenScintFieldRealization(...);`

**上游文档期望（TechnicalManual，非本机抓取）：** 工作区出现 `Scin_amp` / `Scin_phi`（及 `Scin_psi`）；约 **100 Hz**；`plotSign=1` 时出图。

```matlab
save("run_S4_0p8_tau0_0p7.mat", "userInput", "Scin_amp", "Scin_phi", "Scin_psi")
```

### 3.4 星历下载失败（手册要点）

若 `ExtractRINEXeph` 失败：到程序目录**手动解压**已下载的 `brdc****.**n`，再重跑。

### 3.5 相位屏旁路（仓内已有脚本）

```matlab
cd examples
SetPath4PhaseScreenModel   % 脚本内 GPS_ToolBox_Libraries ——按本机改指向 ../matlab
GenerateGPSPhaseScreenRealization
% 按提示 input；回车用默认
```

`examples/README.docx`：先 SetPath，再跑 Generate*。

### 3.6 对照与下游

- `example-data/` 实测 `.mat`：**只比形态**
- 概念课：[13](../tutorials/13-scintillation-modeling.md)；实测指数 → OASIS/IonoMoni/[05](../tutorials/05-scintillation-roti.md)
- 两参数版：姐妹仓 `_2-param`——**文档不要混仓**

---

## 4. 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | `userInput`；可选例程 `.mat`；广播星历 |
| 输出 | `Scin_psi` / `Scin_amp` / `Scin_phi`；图；几何中间量 |
| 不输出 | ROTI、IONEX、RINEX、校准 TEC |

---

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 仿真概念 | §3 | [13](../tutorials/13-scintillation-modeling.md) |
| 与实测指数对照 | §3.6 | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [05](../tutorials/05-scintillation-roti.md) |
| 路径 B 旁路 | — | **不替代**实测 ROTI |

---

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `Undefined function 'ParaMapping'` | 公开树无完整 Libraries | 对照手册补齐；或 §3.5 |
| 2 | 其它 Undefined function | 未 addpath | 按 Main.m / SetPath4*.m |
| 3 | 与站日 ROTI「对不上」 | 物理量不同 | 仿真≠实测指数 |
| 4 | 找 Python 包 | 本仓是 MATLAB | 用 MATLAB 或换工具 |
| 5 | 再分发侵权 | 第三方许可 | 读各 LICENSE |
| 6 | 几何离谱 | RXPos 用了度 | 改弧度 |
| 7 | 无法归因 | 一次改多参数 | 只改 S4 或只改 τ0 |
| 8 | 内存爆 | 时长过长 | 缩 length（先 300） |
| 9 | 当实测发表 | 误解 | 文中标明 simulation |
| 10 | 忽略平台速度 | 几何不完整 | 填 RXVel 或 `[0 0 0]'` |
| 11 | 频点不一致 | frequencyNo 错 | 与 L1/L2/L5 对齐 |
| 12 | 无图以为失败 | plotSign 关 | 查工作区 Scin_* |
| 13 | 两仓文档混用 | 1-param vs 2-param | 分仓记录版本 |
| 14 | 星历解压失败 | 自动 gunzip 失败 | 手动解压 brdc 后重跑 |
| 15 | 路径含空格 / Windows 反斜杠 | addpath 失败 | 无空格路径；`fullfile` |
| 16 | 只截图不存变量 | 无法复现 | `save` 结果 `.mat` |

---

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 可控闪烁仿真（多参数） | **本页** |
| 简化两参数压力测试 | **姐妹仓 `_2-param`** |
| 实测 ROTI | OASIS / IonoMoni |
| 硬件 S4 | ISMR |

---

## 8. 相关

[oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [pytecgg](./pytecgg.md) · [rtklib](./rtklib.md) · [README](./README.md) · [13](../tutorials/13-scintillation-modeling.md) · [05](../tutorials/05-scintillation-roti.md) · [data-access](../data-access.md)

