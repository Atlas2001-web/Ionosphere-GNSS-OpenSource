# GFZRNX

目录：[`PROJECTS.json` → `GFZRNX`](../../PROJECTS.json) · 产品页 <https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox> · 手册 <https://gnss.git-pages.gfz-potsdam.de/gfzrnx/> · 下载 <https://gnss.gfz-potsdam.de/services/gfzrnx>

> 操作手册。祈使句。RINEX 检查/拼接/抽稀/筛选/改版。**本机未安装官方二进制**（需登记下载）。下列 `-h` 节选来自 Users Guide 2.2 Fast Help；装上后以本机 `gfzrnx -h` 覆盖。

## 1. 一句话用途

RINEX 2/3/4 OBS·NAV·MET 批处理手术刀。**不算** TEC/ROTI/定位。进 [georinex](./georinex.md) / [pytecgg](./pytecgg.md) / [rtklib](./rtklib.md) / [anubis](./anubis.md) 前，用它统一采样与系统。

许可：科研伙伴许可通常可教学科研（须登记）；例行生产/商业另议。以下载页 EULA 为准。

## 2. 安装（最少步骤）

1. 打开 <https://gnss.gfz-potsdam.de/services/gfzrnx> 登记并下载对应平台包（如 `gfzrnx_lx64-*`）。
2. 放入 PATH：

```bash
mkdir -p ~/bin
chmod +x gfzrnx_lx64-*
mv gfzrnx_lx64-* ~/bin/
ln -sf ~/bin/gfzrnx_lx64-* ~/bin/gfzrnx
export PATH="$HOME/bin:$PATH"
gfzrnx -h | head -n 40
```

| 现象 | 原因 | 修复命令 |
| --- | --- | --- |
| `command not found` | 未改名/未入 PATH | `ln -sf ~/bin/gfzrnx_lx64-* ~/bin/gfzrnx; hash -r` |
| macOS 无法打开 | Gatekeeper | `xattr -d com.apple.quarantine ~/bin/gfzrnx` |
| PRIDE 找不到命令 | 文件名带 `_lx` | 链接名必须恰好是 `gfzrnx` |

**手册 Fast Help 节选（非本机二进制）：**

```text
gfzrnx -h
***** USAGE: gfzrnx
 [-h] / [-help]
 [-finp <file list>]   input rinex file(s) (std. STDIN)
 [-fout <file>]        output (std. STDOUT); ::RX2:: / ::RX3:: / ::RX4:: = auto name
 [-f]                  force overwrite
 [-smp num[:eps]]      sampling seconds
 [-chk] [-kv]          check / keep version
```

## 3. 端到端骨架：检查 + 30 s 抽稀 + 只留 GPS L1/L2

> **本机未执行**（无二进制）。登记安装后替换路径；不要发明统计数字。

```bash
mkdir -p work out log
head -n 5 work/SITE0010.24o   # 必须是 RINEX，不是 HTML

gfzrnx -finp work/SITE0010.24o \
  -fout out/SITE0010_chk.24o \
  -chk -kv -f

gfzrnx -finp out/SITE0010_chk.24o \
  -fout out/SITE0010_30s.24o \
  -smp 30 -kv -f

gfzrnx -finp out/SITE0010_30s.24o \
  -fout out/SITE0010_G_L1L2.24o \
  -satsys G -obs_types L1C,L2W,C1C,C2W -kv -f

gfzrnx -finp out/SITE0010_G_L1L2.24o -stk_obs | head -n 40
```

| 参数 | 含义 |
| --- | --- |
| `-finp` | 输入文件列表；多文件=拼接候选 |
| `-fout` | 输出；`::RX3::` 等触发自动长名 |
| `-chk` | 形式检查/修复；更新统计头 |
| `-kv` | 保持输入主版本 |
| `-smp 30` | 抽稀到 30 s；可选 `-smp 30:0.5` |
| `-smp_lli_shift` | 抽稀时平移 LLI |
| `-satsys G` | 系统筛选 |
| `-obs_types …` | 观测类型白名单（必须存在于头） |
| `-f` | 允许覆盖 |
| `-stk_obs` | 观测统计打到 stdout |
| `-vo 3` | 输出版本 3 |
| `-splice_direct` | 大拼接省内存直写 |

**期望（质检）：** `-chk` 后头含更新的 `TIME OF FIRST/LAST OBS`；`-smp 30` 后 `INTERVAL`≈30；`-stk_obs` 打印各类型计数。类型名写错→空文件——先读头。

## 4. 可选进阶：小时文件拼日

```bash
gfzrnx -finp work/SITE001{a..x}.24o \
  -fout out/SITE0010.24o -kv -f
# Windows cmd 不膨胀 {a..x} → 用 Git Bash/WSL 或显式列表
```

## 5. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复命令 |
| --- | --- | --- | --- |
| 1 | 输出未更新 | 忘 `-f` | 命令末尾加 `-f` |
| 2 | `{a..x}` 原样残留 | cmd 不膨胀 | `gfzrnx -finp a.24o b.24o c.24o …` |
| 3 | ROTI 结果烂 | 先 `-smp 30` 毁 1 Hz | `gfzrnx -finp raw.obs -fout chk.obs -chk -kv -f`（不抽稀） |
| 4 | 空输出 | `-obs_types` 与头不符 | `gfzrnx -finp f.obs -stk_obs \| head` |
| 5 | STDIN 拼接失败 | STDIN 仅单文件 | `-finp f1 f2 f3` |
| 6 | 自动长名错国家码 | 未给国家码 | `gfzrnx -finp in.obs -fout out/::RX3::00,CHN -vo 3 -f` |
| 7 | 临时目录满 | 大拼接缓存 | 加 `-splice_direct` 或清 `TMPDIR` |
| 8 | 本机无 `gfzrnx` | 未登记下载 | 走官网登记；勿用不明来源二进制 |

## 6. 接到哪一步

- 抽稀后读盘 → [georinex](./georinex.md) → [pytecgg](./pytecgg.md)
- QC → [anubis](./anubis.md)；定位 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- 高频闪烁 → [oasis-roti](./oasis-roti.md)（**禁止**先抽稀）
- 教程 → [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md)；数据 → [data-access](../data-access.md)