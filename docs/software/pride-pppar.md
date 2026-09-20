# PRIDE-PPPAR · 多星座 PPP 模糊度固定

目录条目：[`PROJECTS.json` → `PRIDE-PPPAR`](../../PROJECTS.json) · 上游 <https://github.com/PrideLab/PRIDE-PPPAR>  
支持 / FAQ：<http://pride.apm.ac.cn> · 产品（WUM）：`ftps://bdspride.com/wum/`（以仓库 README 当前地址为准） · 列表：[04 定位](../../lists/04-gnss-positioning.md)

## 作用与场景

**它是什么**：武大 GNSS 中心 PRIDE 实验室开源的 **多星座 PPP / PPP-AR** 软件包（Fortran + Shell，GPL-3.0）。仓库常见版本线 **3.2.x**（以你检出的 tag / `pdp3 -V` 为准）。

**它解决什么**：对单站（或连续多天）RINEX 做**事后精密单点定位**，并尽量 **固定模糊度**，输出坐标/轨迹、对流层 ZTD、残差等。支持 GPS / GLONASS / Galileo / BDS-2·3 / QZSS；可高采样、多天、二阶电离层（GIM）等（见上游 README 能力表）。

**何时用：** 形变、气象、发表级坐标序列。  
**何时先用 [RTKLIB](./rtklib.md)：** 入门 PPP/RTK、流转换、快速验证。  
**不负责：** 不产出 ROTI/TEC 图；电离层在此主要是改正与残差。

## 安装

依赖：bash、make、**gfortran**、gcc、wget/curl。建议普通用户家目录安装（安装脚本一般拒绝 `/root`）。

```bash
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh
# 二进制多在 ~/.PRIDE_PPPAR_BIN/ ；按提示加入 PATH
pdp3 -V    # 或 pdp3 -H
```

可选：仓库 `gui/` 轻量界面（见上游说明）。

## 最小可跑命令

路径与站名为占位符。首次建议用仓库 `example/` 按安装提示跑通。

**静态 PPP-AR**

```bash
pdp3 -m S data/site0010.24o
# 显式时间窗 / 站名（格式以 pdp3 -H 为准）
# pdp3 -m S -n site -s 2024/001/00:00:00 -e 2024/001/23:59:30 data/site0010.24o
```

**动态 / 浮点对照**

```bash
pdp3 -m K data/rover0010.24o     # 动态（默认亦常为 K）
pdp3 -m S -f data/site0010.24o   # -f：关闭 AR，只做浮点 PPP
```

**系统与频率（进阶，务必用 -H 核对字母）**

```bash
pdp3 -m S -sys GREC3 -frq "G12 E15 C26" data/site0010.24o
# 或 -cfg 指向 table/config_template 的副本
pdp3 -cfg /path/to/config data/site0010.24o
```

定位模式（`-m`）：**S** 静态 · **P** 分段常值 · **K** 动态 · **F** 坐标固定 · **L** LEO。另有 `-wcc` 等产品开关（以当前脚本帮助为准）。

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX 观测（2/3/4）；广播星历；精密轨道/钟差/bias/ERP/姿态等（WUM0MGXRAP 等，**以当前上游为准**） |
| 输出 | 按 `年/年积日` 目录：常见 `kin_` 轨迹、`pos_`/`static` 坐标、`ztd_` 对流层、`res_` 残差、`amb_` 模糊度等；可用 `plotkin.sh` 等脚本绘图 |

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 产品下载失败 | FTPS/网络或 URL 变更 | 核对 README 当前地址；手动下载到约定目录 |
| AR 固定率低 | 缺 bias、频点与 OSB 不一致 | 先 `-f` 浮点跑通；核对 `-frq`；换开阔测站 |
| 与 RTKLIB 差很大 | 产品、天线、潮汐模型不同 | 对齐 ANTEX/框架；读 [06 课](../tutorials/06-iono-positioning.md) |
| 多天不连续 | 日界模糊度/产品未对齐 | 见上游多天与 DOCB 说明 |
| 编译失败 | 无 gfortran / 装在 /root | 装编译器；换普通用户目录 |

## 接到哪一步分析

- 定位误差中的电离层 → [06 · 电离层与定位](../tutorials/06-iono-positioning.md)  
- 入门 PPP/RTK → [rtklib](./rtklib.md)  
- 自算 STEC 对照 → [02](../tutorials/02-gnss-dualfreq-tec.md) · [georinex](./georinex.md)  
- 产品与 RINEX → [数据怎么下](../data-access.md)

## 目录指针

- `PROJECTS.json`：`PRIDE-PPPAR` · 相关：`RTKLIB`、`pypride`
