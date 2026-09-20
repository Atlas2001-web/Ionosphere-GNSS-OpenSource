# gnss-scintillation-simulator

目录：[`PROJECTS.json` → `gnss-scintillation-simulator`](../../PROJECTS.json) · 上游 <https://github.com/cu-sense-lab/gnss-scintillation-simulator> · 相关 `gnss-scintillation-simulator_2-param`（本页不展开）

## 用途

- CU Sense Lab **GPS 频段闪烁仿真**（主 MATLAB）。相位屏/传播理论 → 复场、振幅、相位时序；附香港等例程数据。
- 在可控 **S4、相关时间** 下**合成闪烁**，服务接收机算法/航空可用性/教学。
- **不是**从 RINEX 提取 ROTI。

| 需求 | 工具 |
|---|---|
| RINEX → ROTI/ΔTEC | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| 硬件 S4/σφ | ISMR 等 |
| 可控仿真闪烁场 | **本页** |

## 安装

1. 安装 MATLAB（工具箱以例程报错为准）。
2. 克隆：

```bash
git clone https://github.com/cu-sense-lab/gnss-scintillation-simulator.git
cd gnss-scintillation-simulator
```

3. MATLAB 中把 `matlab/` 子目录加入路径；例程在 `examples/`。入口以 `examples/Main.m`、`examples/README.docx`、`docs/TechnicalManual.docx` 为准。

## 快速上手

```matlab
cd examples
% 按仓库说明 addpath（若有 SetPath4GPS.m 等则先运行）
edit Main.m      % 查看并修改 userInput
Main             % 运行
```

`Main.m` 典型字段（**以你克隆的文件为准**）：

| 字段 | 含义 |
|---|---|
| `userInput.dateTime` | `[年 月 日 时 分 秒]` |
| `userInput.length` | 时长（常见 300/600/900 s） |
| `userInput.RXPos` | `[纬(rad), 经(rad), 高(m)]` |
| `userInput.RXVel` | 东/北/天速度 (m/s) |
| `userInput.PRN` | GPS PRN |
| `userInput.frequencyNo` | 1=L1；2=L1+L2；3=L1+L2+L5 |
| `userInput.S4` / `tau0` | 地面 S4 与强度相关时间 |
| `userInput.plotSign` | 是否出图 |

调用链概览：`ParaMapping` → `RunPropGeomCalc` → `RunGenScintFieldRealization` → `Scin_psi` / `Scin_amp` / `Scin_phi`。

例程数据：`example-data/` 中 Septentrio 转 `.mat`（香港、秘鲁等），可与仿真形态对照。

**预期：** 生成振幅/相位时序与图；路径未加全会报函数找不到。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | `userInput` 几何与闪烁参数；可选例程 `.mat` |
| 输出 | 闪烁复场/振幅/相位；例程图；中间几何量 |
| 文档 | `docs/PropagationTheory.pdf`、`TechnicalManual.docx`、相关论文 PDF |

## 常用参数

见上表 `userInput.*`。改 S4/tau0/几何时一次只动一个变量，便于对照。

## 接到工作流哪一步

- 概念：[05](../tutorials/05-scintillation-roti.md)·[21](../tutorials/21-equatorial-anomaly-bubbles.md)
- 建模课：[13](../tutorials/13-scintillation-modeling.md)
- 实测指标：[oasis-roti](./oasis-roti.md)·[ionomoni](./ionomoni.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 找不到函数 | 对 `matlab/` 递归 `addpath` |
| 和 ROTI「对不上」 | 物理量不同；见 [05](../tutorials/05-scintillation-roti.md) |
| 没有 Python 包 | 项目定位就是 MATLAB |
| 许可混杂 | 含 MATLAB Central/Wavelab 等；再分发前读子目录 LICENSE |
| 纬度用了度 | `RXPos` 常为弧度——核对例程 |

## 相关工具

[oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)

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
