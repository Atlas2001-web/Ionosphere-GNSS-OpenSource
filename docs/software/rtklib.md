# RTKLIB

目录：[`PROJECTS.json` → `RTKLIB`](../../PROJECTS.json) · 上游 <https://github.com/tomojitakasu/RTKLIB> · 常用维护分支 <https://github.com/rtklibexplorer/RTKLIB>

## 用途

- 开源 **SPP / DGPS / RTK / PPP**（库 + GUI + CLI）。
- 主产品是**坐标时间序列**；电离层是改正或误差源，不是 TEC/ROTI 引擎。
- 事后：`rnx2rtkp`；原始日志：`convbin`；流转发：`str2str`。

## 安装

**Windows：** 从上游或 rtklibexplorer releases 取预编译，`bin` 加入 `PATH`。

**Linux（explorer 示例）：**

```bash
sudo apt install -y build-essential cmake git
git clone https://github.com/rtklibexplorer/RTKLIB.git
cd RTKLIB
# 按该仓库 README 编译，再 export PATH
rnx2rtkp -h | head
convbin -h | head
```

模式号与选项以**你编译的二进制** `-h` 为准（原版与 demo5/explorer 有差异）。

## 快速上手

```bash
# 1) UBX → RINEX
convbin -r ubx -o rover.obs -n rover.nav rover.ubx

# 2) 单点冒烟
rnx2rtkp -o out_spp.pos rover.obs rover.nav

# 3) 静态基线 RTK（-p 以 -h 为准）
rnx2rtkp -p 2 -m 10 -o out_rtk.pos rover.obs base.obs rover.nav

# 4) 浮点 PPP（需 SP3/CLK）
rnx2rtkp -o out_ppp.pos rover.obs rover.nav precise.sp3 precise.clk

# 5) 配置文件方式
rnx2rtkp -k my.conf -o out.pos rover.obs rover.nav

# 6) 看结果
head out_spp.pos
# 典型列：时间、ECEF/ENU、Q（解状态）、ns
```

**预期：** `.pos` 增长；Q 中 1=固定、2=浮点等（以手册为准）。无共视/无 SP3 时 PPP 失败属正常。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS/NAV；UBX/RTCM（经 convbin/str2str）；SP3/CLK/ANTEX；可选 IONEX |
| 输出 | `.pos`；可选 `.stat` |
| 不做 | STEC/ROTI 产品文件 |

## 常用参数

| 项 | 说明 |
|---|---|
| `-p` | 定位模式（以 `-h` 为准） |
| `-o` | 输出 `.pos` |
| `-m` | 高度截止角（度） |
| `-k conf` | 配置文件 |
| `convbin -r` | 原始格式 |
| `str2str` | NTRIP/TCP/串口转发 |

## 接到工作流哪一步

- 实时流：[bnc](./bnc.md)/[pygnssutils](./pygnssutils.md)
- 输入 QC：[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)
- 科研级 PPP-AR → [pride-pppar](./pride-pppar.md)
- 高 ROTI 失锁：[ionomoni](./ionomoni.md) · 教程 [06](../tutorials/06-iono-positioning.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 固定率极低 | 基线/多路径/共视；先 Anubis |
| PPP 不收敛 | 缺 SP3/CLK、天线、时长不足 |
| `-p` 行为怪 | 分支不同，重读 `-h` |
| 实时龄期大 | 先事后文件冒烟 |
| 想要 TEC 图 | 换 [pytecgg](./pytecgg.md) |
| 配置未生效 | 确认 `-k` 路径；GUI 与 CLI 配置勿混用 |

## 相关工具

[pride-pppar](./pride-pppar.md) · [bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [anubis](./anubis.md)

## 操作检查清单

1. `rnx2rtkp -h` / `convbin -h` 可用。  
2. 事后 SPP 能出非空 `.pos`。  
3. RTK：有共视、基线合理、Q 有固定/浮点变化。  
4. PPP：SP3/CLK 时间覆盖观测。  
5. 配置文件用 `-k` 且路径正确。  
6. 实时：先事后冒烟，再接流。  
7. 不要把 `.pos` 当成 TEC 产品。

## 预期 I/O 示例

```text
# .pos 示意（列以版本为准）
% GPST                  x-ecef      y-ecef      z-ecef   Q  ns
2024/01/01 00:00:00.000  ...         ...         ...     2  10
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
