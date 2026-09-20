# RTKLIB · 开源 RTK / PPP 解算

目录条目：[`PROJECTS.json` → `RTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/tomojitakasu/RTKLIB>  
社区常用维护分支：<https://github.com/rtklibexplorer/RTKLIB>（低成本接收机优化，文档与发行包较新）

## 作用与场景

**它是什么**：经典开源 GNSS 定位程序包——库 + 一批 GUI/命令行工具。能做单点、差分 RTK、事后静态/动态，以及 **PPP（精密单点定位）**。

**它解决什么**：你已有 RINEX（或接收机原始流），想得到**坐标时间序列**或评估电离层对定位的影响，而不是只看 TEC 图。教研、低成本板卡、快速验证算法时常从 RTKLIB 入手。

**和 PRIDE-PPPAR 比一句**：PRIDE-PPPAR（武大 PRIDELab）更偏**科研级多星座 PPP 模糊度固定**与形变/气象产品；学习曲线更陡。入门定位、RTK、流转换优先 RTKLIB；要发表级 PPP-AR 再考虑 PRIDE-PPPAR（见计划索引）。

**不负责**：不专门产出 ROTI/TEC 图；电离层在此是**改正模型或残差**，不是主产品。

## 术语｜人话

| 术语 | 人话 |
|---|---|
| RTK | 用附近基准站差分，快速定到厘米级（实时或事后） |
| PPP | 不用近距离基站，靠精密星历/钟差（及改正产品）单站精密定位 |
| `rnx2rtkp` | 事后解算命令行：读 RINEX → 输出位置解 |
| `convbin` | 把接收机原始二进制转成 RINEX |
| `str2str` | 流转发（串口/TCP/NTRIP 等） |
| SP3 / CLK | 精密轨道与钟差产品（PPP 常用） |
| 解算模式 | Single / DGPS / Kinematic / Static / PPP-Kinematic / PPP-Static 等 |

## 安装

任选其一（以你系统与上游发行说明为准）：

1. **Windows**：从 [tomojitakasu/RTKLIB](https://github.com/tomojitakasu/RTKLIB) 或 [rtklibexplorer/RTKLIB/releases](https://github.com/rtklibexplorer/RTKLIB/releases) 下载预编译包，把 `bin` 加入 `PATH`。  
2. **Linux（explorer / demo5 系）**：按该仓库 README 用 CMake 编译 CLI；或使用发行版/社区包（若有）。  
3. 确认命令可用：

```bash
rnx2rtkp -h | head
convbin -h | head
```

> 具体二进制名、选项字母随分支略有差异；下文骨架标「以当前上游手册为准」。

## 最小可跑命令流

路径均为占位符。

### A. 原始数据 → RINEX（可选）

```bash
# 以当前上游文档为准
convbin -r ubx -o data/rover.obs -n data/rover.nav data/rover.ubx
```

### B. 事后单点 / 静态（快速冒烟）

```bash
rnx2rtkp -p 3 -o data/out_static.pos data/rover.obs data/rover.nav
# -p 模式编号：常见 0=单点 … 与 PPP/静态对应关系请查你所用版本的 -h 或手册
```

### C. 事后 PPP 骨架（需精密产品）

```bash
# 准备：rover OBS/NAV + 同日 SP3 + CLK（从 CDDIS 等下载，见 data-access）
rnx2rtkp -p 7 \
  -o data/out_ppp.pos \
  data/rover.obs data/rover.nav \
  data/igs16801.sp3 data/igs16801.clk
# -p 7 常对应 PPP-Static 一类；请用 rnx2rtkp -h 核对你二进制中的模式表
```

### D. 差分 RTK 事后（流动站 + 基准站）

```bash
rnx2rtkp -p 2 -o data/out_rtk.pos \
  data/rover.obs data/base.obs data/rover.nav
```

### E. GUI 路线

打开 **RTKPOST**（事后）或 **RTKNAVI**（实时）：选模式 → 指定观测/星历/选项文件 → Execute。适合第一次摸选项含义。

## 输入 / 输出

| 方向 | 典型文件 | 说明 |
|---|---|---|
| 输入 | OBS/NAV（RINEX 2/3）、SP3、CLK、ANTEX、有时 IONEX | PPP 强烈依赖精密产品与天线模型 |
| 输出 | `.pos` 等位置解、轨迹；可用 **RTKPLOT** 看 | 列含义见文件头注释（时间、xyz/blh、Q 等） |

读 `.pos`：先看解算质量标志与标准差；电离层相关实验可对比「开/关电离层改正」或不同 GIM 输入时坐标残差变化（进阶）。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| PPP 漂或收敛极慢 | 缺 SP3/CLK、产品与观测日期不一致 | 核对 GPS 周 / DOY；产品与测站天线名匹配 |
| RTK 固定不了 | 基线太长、共视差、周跳多 | 换近站；检查采样率与截止高度角 |
| 选项文件与 CLI 行为不一致 | GUI 另存的 `.conf` 未加载 | 明确 `-k` 配置文件或完整写出关键选项 |
| 分支混用文档 | demo5 / 原版选项号不同 | **以你手中二进制的 `-h` 为准** |
| 只想要 TEC | 用错工具 | 回 [georinex](./georinex.md) / [02 课](../tutorials/02-gnss-dualfreq-tec.md) |

## 接到电离层分析哪一步

- 定位误差里的电离层 → [06 · 电离层与定位](../tutorials/06-iono-positioning.md)  
- 需要自算 STEC 再对比 → [02](../tutorials/02-gnss-dualfreq-tec.md) · [georinex](./georinex.md)  
- 产品与 RINEX 下载 → [数据怎么下](../data-access.md)  
- 实时改正流可与 [BNC](./bnc.md) 搭配

## 目录指针

- `PROJECTS.json`：`name=RTKLIB` · `url=https://github.com/tomojitakasu/RTKLIB`  
- 相关：`RTKLIB-explorer`、`PRIDE-PPPAR`
