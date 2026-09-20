# PRIDE-PPPAR

目录：[`PROJECTS.json` → `PRIDE-PPPAR`](../../PROJECTS.json) · 上游 <https://github.com/PrideLab/PRIDE-PPPAR> · 支持 <http://pride.apm.ac.cn> · GPL-3.0

## 用途

- 武大 Pride 实验室 **PPP / PPP-AR**（`pdp3`）。
- 面向发表级坐标、ZTD、多系统模糊度固定；依赖精密轨道钟差等产品。
- 电离层主要是**改正与残差**，不是 TEC/ROTI 产品引擎。

## 安装

依赖：bash、make、**gfortran**、gcc、wget/curl。建议普通用户家目录（安装脚本常拒绝 `/root`）。

```bash
git clone https://github.com/PrideLab/PRIDE-PPPAR.git
cd PRIDE-PPPAR
bash install.sh
echo 'export PATH="$HOME/.PRIDE_PPPAR_BIN:$PATH"' >> ~/.bashrc
source ~/.bashrc
pdp3 -V
pdp3 -H | head
```

可选 GUI 见仓库说明。产品（WUM 等）地址以当前 README 为准。

## 快速上手

```bash
# 1) 官方 example（强烈建议先跑通）
# 按仓库 example/ 与安装提示操作

# 2) 静态 PPP-AR
pdp3 -m S data/site0010.24o

# 3) 动态
pdp3 -m K data/rover0010.24o

# 4) 强制浮点对照
pdp3 -m S -f data/site0010.24o

# 5) 系统/频率（示例字符串以 -H 为准）
pdp3 -m S -sys GREC3 -frq "G12 E15 C26" data/site0010.24o

# 6) 配置文件
cp table/config_template ./config_my
# 编辑天线、截止角、产品路径等
pdp3 -cfg ./config_my data/site0010.24o
```

**预期：** 按年/年积日生成结果目录；出现 `kin_`/`pos_`/`ztd_`/`res_` 等前缀（以版本为准）。产品下载失败则无解。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS；精密 SP3/CLK 等产品；`table/` 天线与潮汐表 |
| 输出 | 坐标、ZTD、残差、固定率相关文件 |
| 不做 | ROTI/STEC 标准产品 |

## 常用参数

| 选项 | 含义（助记，以 `-H` 为准） |
|---|---|
| `-m S/K/...` | 静态 / 动态等模式 |
| `-f` | 浮点（关 AR） |
| `-sys` / `-frq` | 系统与频率 |
| `-cfg` | 配置文件 |
| `-s` / `-e` / `-n` | 时间窗与站名（若版本支持） |

二阶电离层/GIM：按配置模板开关，自备 IONEX。

## 接到工作流哪一步

- 路径 D：先 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md) → [rtklib](./rtklib.md) 冒烟 → 本工具
- 磁暴日固定率对照：[ionomoni](./ionomoni.md) · 教程 [06](../tutorials/06-iono-positioning.md)/[20](../tutorials/20-storm-tec-analysis.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 编译失败 | 装 gfortran；勿用 root 装 |
| 产品下不来 | 网络/FTPS；核对 README 地址 |
| 固定率很低 | 先 QC；磁暴/闪烁时段对照 ROTI |
| RINEX4 | 查当前版本支持说明 |
| 把残差当 TEC 产品 | 改用 [pytecgg](./pytecgg.md) |
| example 没跑通就换站 | 先官方样例，再换数据 |

## 相关工具

[rtklib](./rtklib.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [ionomoni](./ionomoni.md) · [ionex-gim](./ionex-gim.md)

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
