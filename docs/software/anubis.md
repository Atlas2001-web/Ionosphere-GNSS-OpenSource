# Anubis（G-Nut Free QC）

目录：[`PROJECTS.json` → `Anubis`](../../PROJECTS.json) · 官网 <https://gnutsoftware.com/software/anubis/> · 配置 <https://www.pecny.cz/gop/index.php/gnss/70-gnss-software/221-anubis-configuration> · Free 常见 GPL；Pro/RT 商业

## 用途

- GNSS **质量检查（QC）**；本页只讲 **Anubis Free**（常见标称 2.3，Linux）。
- 回答：数据全不全？缺口在哪？多路径重不重？哪系统老掉链？
- 输出 **XTR / XML**——**不是** TEC，**不是** 精密定位引擎。
- 与 GFZRNX：**GFZRNX 改文件，Anubis 评文件**。顺序：GFZRNX（必要时）→ Anubis → 科学软件。

## 安装

1. 打开 [下载页](https://gnutsoftware.com/software/anubis/download)（可能需注册），取 Free/Linux 包或源码。
2. 将 `anubis` 放入 `PATH`。
3. 冒烟：

```bash
anubis -h | head
anubis -X | head
```

OS X / Windows 二进制条件以官网为准。

## 快速上手

```bash
# 1) 导出默认 XML
anubis -X > anubis_qc.xml
# 编辑 <inp> OBS/NAV、<out> xtr/xml 路径

# 2) 运行
anubis -x anubis_qc.xml
# 或：anubis < anubis_qc.xml

# 3) CLI 覆盖路径（键名以 -h/手册为准）
anubis -x anubis_qc.xml \
  :inp:rinexo=data/site0010.24o \
  :inp:rinexn=data/brdc0010.24n

# 4) 扫 XTR
grep -E 'MP|gap|SNR|Summary' site0010.xtr | head

# 5) 批量日检骨架
for f in data/*.24o; do
  anubis -x anubis_qc.xml :inp:rinexo="$f" || echo "FAIL $f"
done
```

QC 模式（在 XML 中切换，键名以手册为准）：**thin**（偏元数据）→ **lite**（缺口/完整性）→ **full**（更综合，更慢）。

社区绘图：https://www.pecny.cz/sw/plots/anubis/ （`plot_anubis.pl`，无官方支持承诺）。

**预期：** 生成 `.xtr` 与 `.xml`；终端有进度/摘要。

## 输入 / 输出

| 方向 | Free 常见 |
|---|---|
| 输入 | RINEX 2/3 OBS+NAV；XML/CLI |
| 输出 | XTR、XML、日志 |
| Pro/RT | RTCM 流等（本页不展开） |

## 常用参数

| 项 | 说明 |
|---|---|
| `-X` | 打印默认 XML |
| `-x file` | 按配置运行 |
| `:inp:rinexo=` / `:inp:rinexn=` | 覆盖输入路径 |
| XML qc 模式 | thin / lite / full |

## 接到工作流哪一步

- TEC → [georinex](./georinex.md) · [pytecgg](./pytecgg.md) · [02](../tutorials/02-gnss-dualfreq-tec.md)
- 扰动 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)
- 预处理 → [gfzrnx](./gfzrnx.md)
- 定位 → [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)

几乎所有路径 A/B/D 的「体检站」。

## 常见问题

| 现象 | 处理 |
|---|---|
| Free/Pro 功能混谈 | 以官网档位为准 |
| 路径写相对路径失败 | 换绝对路径或固定 cwd |
| 只要拼接抽稀 | 用 [gfzrnx](./gfzrnx.md) |
| XTR 太大 | 先 lite；grep 关键字段 |
| 与 georinex 缺口不一致 | 对齐时间窗后再比 |
| Windows 换行破坏 XML | 用 LF |

## 相关工具

[gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md)

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
