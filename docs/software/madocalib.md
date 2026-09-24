# MADOCALIB · QZSS MADOCA-PPP 测试库操作手册

目录：[`PROJECTS.json` → `MADOCALIB`](../../PROJECTS.json) · 上游 <https://github.com/QZSS-Strategy-Office/madocalib> · 官方门户 <https://qzss.go.jp/> · tip **`0089f7d`** · **VER_MADOCALIB 2.1**（基于 RTKLIB 2.4.3 b34）· 许可 **BSD-2-Clause + 附加条款** · 本机验证：Linux `make` → `rnx2rtkp`；样例站 **MIZU** 2025-04-01 00:00–00:59 ×30 s + L6E PRN204/206 → **118** 历元 **Q=6** PPP · 末历元 ≈ 39.135150522°N 141.132871426°E 117.20 m · 2026-09-24 04:39 EDT · **质检复跑通过**（同 I/O，2026-09-24 04:42 EDT）

> 岗位：内阁府 QZSS **MADOCA-PPP** 事后参考实现（Compact SSR / L6 → PPP、PPP-AR、可选电离层改正）。冲突时：**仓内 `readme.txt` / `MADOCALIB_manual_ver006.pdf` / `./rnx2rtkp -?` > 本文**。通用 RTK/PPP CLI → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；Python 开放 PPP-RTK → [cssrlib](./cssrlib.md)；Galileo HAS 解码 → [haslib](./haslib.md)。

## 1. 用途与边界

**做：**

- 读 RINEX OBS/NAV + **QZSS L6** 归档（IS-QZSS-MDC-003/004），跑 **PPP / PPP-AR**
- `rnx2rtkp`（MADOCA 分支）：`-k conf`、`-ant`、`-mdciono`、`-ionocorr`
- `cssr2ssr`：Compact SSR → 传统 SSR 文件（另有 Linux makefile）
- 样例：`sample_data/exec_ppp.bat` 等（Windows 批；Linux 等价命令见 §3）
- 可选 **MADOCALIB_GUI**（PyInstaller，主要面向 Windows）

**不做：**

- **不是** 运营级实时保证——官方免责：不保证有效性/可靠性
- **不是** 通用未改 RTKLIB → [rtklib](./rtklib.md)；勿混用两套 `bin`
- **不是** 校准 sTEC/GIM 产品 → [pytecgg](./pytecgg.md) / [ionex-gim](./ionex-gim.md)（此处电离层是 **PPP 改正**）
- **不是** Galileo HAS 页解码 → [haslib](./haslib.md)；CLAS/HAS Python 试验 → [cssrlib](./cssrlib.md)
- **不是** 发表级多站 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)

一句话：MADOCALIB = **QZSS 官方 MADOCA-PPP 用户端参考实现**；验证算法与 ICD，不是坐标生产厂。

| 术语 | 含义 |
| --- | --- |
| MADOCA-PPP | QZSS Multi-GNSS Advanced Orbit and Clock Augmentation PPP |
| L6E / L6D | 轨道钟差等 Compact SSR / 电离层相关归档（样例分目录） |
| `%HU` 小时码 | `A=0` … `X=23`（大写）；`2025091A.204.l6` = 2025 DOY091 时 0 PRN204 |
| Q=6 | 解状态 PPP（浮点）；Q=1 才是 fix |
| `VER_MADOCALIB` | `src/rtklib.h` 中版本宏；本机 **2.1** |

## 2. 安装（Linux 自编译）

`bin/*.exe` 为 Windows 预编译。Linux（≥2.0 起提供 makefile）：

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/QZSS-Strategy-Office/madocalib.git
cd madocalib/app/consapp/rnx2rtkp/gcc
make -j"$(nproc)"
./rnx2rtkp -? | head -5
# 期望：usage: rnx2rtkp [option]... file file [...]
# 可选：cd ../../cssr2ssr/gcc && make -j"$(nproc)"
```

本机产物：`app/consapp/rnx2rtkp/gcc/rnx2rtkp`（~2.6 MB，2026-09-24）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 直接跑 `bin/rnx2rtkp.exe` | Linux 不认 PE | 走 `app/consapp/rnx2rtkp/gcc` 的 `make` |
| `error : no input file` | 无参启动 | 属正常；用 `-?` 看帮助或给 OBS/NAV/L6 |
| 缺 `-lm`/`-lrt` | 极简容器 | `sudo apt-get install -y build-essential` |

## 3. 端到端：MIZU 1 小时 MADOCA PPP（本机真跑）

数据已在 `sample_data/data/`（RINEX + `l6_is-qzss-mdc-004/2025/091/` + `igs20.atx`）。Windows 用 `exec_ppp.bat`；Linux：

```bash
cd ~/iono_ops/madocalib/sample_data
mkdir -p result_e2e
BIN=../app/consapp/rnx2rtkp/gcc/rnx2rtkp
CONF=../app/consapp/rnx2rtkp/gcc_mingw/sample.conf
OBS=./data/rinex/MIZU00JPN_R_20250910000_01D_30S_MO.rnx
NAV=./data/rinex/BRDM00DLR_S_20250910000_01D_MN.rnx
# 时 0 → 小时码 A；PRN 204/206
L6E1=./data/l6_is-qzss-mdc-004/2025/091/2025091A.204.l6
L6E2=./data/l6_is-qzss-mdc-004/2025/091/2025091A.206.l6
ANT=./data/igs20.atx

"$BIN" -ts 2025/04/01 00:00:00 -te 2025/04/01 00:59:30 -ti 30 \
  -k "$CONF" -o ./result_e2e/20250401000000.pos -ant "$ANT" \
  "$OBS" "$NAV" "$L6E1" "$L6E2"
```

**本机结果（VER 2.1 / tip `0089f7d`，2026-09-24 04:39 EDT）：**

```text
% program    : MADOCALIB ver.2.1
% pos mode   : PPP Kinematic
% ionos opt  : Iono-Free LC
% ephemeris  : Broadcast+SSR APC
% amb mode   : OFF
% ionocorr   : off
历元数：118（grep -c '^2025/' …pos）
首解：2025/04/01 00:01:00  Q=6  ns=10  h≈117.97（00:00:00/00:00:30 为 Q=0，未写入 .pos）
末解：2025/04/01 00:59:30  Q=6  ns=19
        39.135150522  141.132871426  117.2037
        sdn/sde/sdu ≈ 0.026 / 0.045 / 0.055 m
```

PPP-AR：换 `sample_pppar.conf`（`pos2-armode` 开）。带 MADOCA 电离层：`sample_pppar_iono.conf` + `-ionocorr` / `-mdciono`（L6D，见手册与 bat `exec_pppar_ion.bat`）。

### 3.1 帮助与关键旗标

```bash
../app/consapp/rnx2rtkp/gcc/rnx2rtkp -? 2>&1 | rg 'mdciono|ionocorr|-ant|-k'
```

| 旗标 | 作用 |
| --- | --- |
| `-k file` | 读 conf（CLI 覆盖 conf） |
| `-ant file` | 接收机 ANTEX（样例 `igs20.atx`） |
| `-mdciono file` | 最多 3 个 L6D 电离层归档 |
| `-ionocorr` | 应用 MADOCA 电离层改正 |
| `-ts/-te/-ti` | 时段与采样 |

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS/NAV | 样例 MIZU + BRDM；多系统位掩码见 conf `pos1-navsys` |
| L6E `*.l6` | 按年/年积日/小时码/PRN；缺时 SSR 不足 → 难收敛 |
| ANTEX | `-ant`；与 conf 内 `file-rcvantfile` 一致 |
| conf | `sample.conf` / `sample_pppar.conf` / `sample_pppar_iono.conf` |

| 输出 | 说明 |
| --- | --- |
| `*.pos` | RTKLIB 风格解；头含 `MADOCALIB ver.x` |
| Q / ns / sd* | 质量与卫星数、标准差 |
| 不输出 | 发表级 SINEX、STEC 产品、实时 SLA |

## 5. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| 对照通用 PPP CLI | [rtklib](./rtklib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| Python CLAS/HAS/BDS PPP | [cssrlib](./cssrlib.md) |
| Galileo HAS 页→SSR | [haslib](./haslib.md) |
| 定位与电离层课 | [06](../tutorials/06-iono-positioning.md) |
| 观测 QC 后再进 PPP | [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `bin/rnx2rtkp.exe` 无法执行 | Windows PE | `cd app/consapp/rnx2rtkp/gcc && make` |
| 2 | L6 读不到 / 改正空 | 小时码错（0 点不是 `0`） | 用 `A`…`X`：`ls data/l6_is-qzss-mdc-004/2025/091/2025091A.*` |
| 3 | 只有 Q=0 或无解 | 缺 L6/NAV 或时段外 | 核对 `-ts/-te` 与 `*.l6` 小时；先拷官方 bat 参数 |
| 4 | 把 Q=6 当固定解 | Q=6=PPP 浮点 | 看头 `amb mode`；AR 用 `sample_pppar.conf`，Q=1 才是 fix |
| 5 | 无天线 PCV / 高程偏 | 未 `-ant` | 加 `-ant ./data/igs20.atx` |
| 6 | 与库存 RTKLIB 结果死磕 | 分支+MDC 消息不同 | 只和同版 MADOCALIB / 官方样例比 |
| 7 | 离子改正无效 | 只用了 L6E 或 conf 关 | 换 `sample_pppar_iono.conf` + `-ionocorr`/`-mdciono` L6D |
| 8 | `003`/`004` 目录混用 | ICD 版本不同 | 样例 PPP 用 `l6_is-qzss-mdc-004`；对照手册版本 |
| 9 | GUI 在 Linux 打不开 | `madocalib_gui.exe` 为 Win 包 | 用 CLI；GUI 仅可选前端 |
| 10 | 野卡 `%Y%n%HU` 在 bash 展开坏 | 批处理变量语法 | Linux 写死 `2025091A.204.l6` 或自写循环 |
| 11 | 当 STEC 产品发表 | 边界错 | PPP 残差/改正 ≠ [pytecgg](./pytecgg.md) 校准 TEC |
| 12 | 多 PRN L6 漏文件 | 单星归档不够 | 按 bat 同时喂 204/206（或手册所列 PRN） |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| QZSS MADOCA 官方事后参考 | **MADOCALIB（本页）** |
| 通用开源 RTK/PPP CLI | [rtklib](./rtklib.md) |
| 论文级 PPP-AR / 产品链 | [pride-pppar](./pride-pppar.md) |
| Python 读 CLAS/HAS/BDS | [cssrlib](./cssrlib.md) |
| 只解码 Galileo HAS 页 | [haslib](./haslib.md) |

## 8. 相关

[cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [glab-upc](./glab-upc.md) · [README](./README.md)
