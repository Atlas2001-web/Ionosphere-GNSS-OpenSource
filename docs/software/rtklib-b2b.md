# RTKLIB-B2b · 北斗 PPP-B2b 解码与定位（RTKLIB 扩展）操作手册

目录：[`PROJECTS.json` → `RTKLIB-B2b`](../../PROJECTS.json) · 上游 <https://github.com/UCAS-Liuchunbo/RTKLIB-B2b> · Gitee 镜像见 README · tip **`df40c0c`**（2026-04-01）· 版本宏 **`VER_RTKLIB "v1.0"`** / **`PATCH_LEVEL "20250305"`** · README 宣称 **GPLv3**（仓内**无** `LICENSE` 文件，商用先核实）· 本机：CMake Release + gcc **14.2.0** → `bin/{postdecoder,postppp,rtdecoder,rtppp}`（**848360 / 1447560 / 1528192 / 1549200** B）；`postdecoder -U` 解 `Unicore_2024360.B2bBin`（**15905080** B）→ `.B2bssr` **49998353** B，sha256=`6d3bc81bf054…` **与** `example_out.zip` 参考 **逐字节一致**；头计数 MASK=**3602** / CLOCK=**86410** / ORBIT_URAI=**13420** / DIFF_CODE_BIAS=**13294** · **未**拉 Zenodo OBS → **未跑**全日 `postppp` 坐标 · **2026-09-24 06:30 EDT**

> 岗位：从司南 / 和芯二进制流解 PPP-B2b，并接入 RTKLIB 系事后/实时 PPP。冲突时：**仓内 `manual/RTKLIB-B2b_UserManual.pdf` / `example/*/note.txt` / 源码 > 本文**。嵌经典 2.4.3 的研究包 → [b2blib](./b2blib.md)；BNC/SBF 插件切片 → [rtppp-b2b](./rtppp-b2b.md)；明文/导出 → [navdecoder](./navdecoder.md)；Python CSSR → [cssrlib](./cssrlib.md)；通用 CLI → [rtklib](./rtklib.md)。

**与 [rtklib.md](./rtklib.md) 的差别：** `rtklib.md` 讲的是官方/explorer 通用 `rnx2rtkp`/`str2str`。**本仓不是**「再编一份 EX」：新增 **`B2b.c` / `B2b.h`**、接收机 **`STRFMT_SINO=20` / `STRFMT_UNICORE=21`**、星历选项 **`EPHOPT_B2b=5`（`brdc+PPP-B2b`）**，入口是 **`postdecoder` / `postppp` / `rtdecoder` / `rtppp`**，不是 stock 同名工具集。也**不是** [b2blib](./b2blib.md)（VS 嵌入 + 已展开 `.dat`）或 [rtppp-b2b](./rtppp-b2b.md)（缺 BNC 头无法独立链）。

## 1. 用途与边界

**做：**

- **解码：** 司南（`-S`）/ 和芯 Unicore（`-U`）专有 PPP-B2b 二进制 → BNC 风格 ASCII SSR（`.B2bssr`）
- **定位：** 事后 `postppp`、实时 `rtppp`；BDS-only 或 GPS+BDS；`prcopt.sateph=5`
- **模式：** 事后 / 实时解码与 PPP；Linux 实时更友好（README 表）
- **样例：** `example/postdecoder/Unicore_2024360.B2bBin`；更多 OBS/回放见 Zenodo DOI（README）

**不做：**

- **不是** stock RTKLIB / explorer 低成本 RTK 主树 → [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md)
- **不是** 仅嵌库的 B2bLIB（已拆 `.dat` + 硬编码路径）→ [b2blib](./b2blib.md)
- **不是** 只产改正、依赖 BNC 私有头的 RTPPP 切片 → [rtppp-b2b](./rtppp-b2b.md)
- **不是** Galileo HAS / QZSS CLAS·MADOCA → [haslib](./haslib.md)/[claslib](./claslib.md)/[madocalib](./madocalib.md)
- 本机**无** Zenodo 事后 OBS → **禁止臆造** WUH2/GAMG `.pos` 收敛坐标；以 `example_out.zip` 与自备数据为准
- 许可：README 徽章 GPLv3，但 **无 LICENSE 文件** → 产品嵌入前联系作者 / 补齐许可证文本

一句话：RTKLIB-B2b = **可编的 B2b 解码+PPP 工具包**（司南/和芯二进制进、SSR/坐标出）。

| 术语 | 含义 |
| --- | --- |
| PPP-B2b | 北斗三号 B2b 精密改正服务 |
| `STRFMT_SINO` / `UNICORE` | 20 / 21；与 conf `prcopt.B2b_format` 对齐 |
| `EPHOPT_B2b` | `sateph=5`：广播 + B2b SSR（APC） |
| `postdecoder` | 事后二进制 → `.B2bssr` |
| `postppp` | 事后 PPP（conf + OBS/NAV/B2b） |
| `rtdecoder` / `rtppp` | 实时解码 / 实时 PPP（需流与 conf） |

## 2. 安装 / 编译

### 2.1 获取

```bash
git clone https://github.com/UCAS-Liuchunbo/RTKLIB-B2b.git
cd RTKLIB-B2b
git rev-parse --short HEAD   # 本机 df40c0c
```

仓内可能已有预编译 `bin/*` / `example/*/post*`（**架构未必匹配本机**）。以 CMake 现编为准。

### 2.2 CMake（本机）

```bash
sudo apt-get install -y cmake build-essential
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j"$(nproc)"
# 产出写入仓根 bin/：postdecoder postppp rtdecoder rtppp + lib/libB2bLib.a
ls -l bin/
./bin/postdecoder   # → Usage: postdecoder [-U|-S] -in ... [-out ...]
```

顶层 `CMakeLists.txt` 默认编四个 app + `src` 静态库；Windows 另有 `WIN32` 宏。细参见 `manual/*.pdf`。

## 3. 端到端（本机 · 解码冒烟）

### 3.1 `postdecoder`（和芯样例 · 与参考逐字节一致）

```bash
cd /path/to/RTKLIB-B2b
./bin/postdecoder -U \
  -in example/postdecoder/Unicore_2024360.B2bBin \
  -out /tmp/Unicore_2024360.B2bssr
# Decoding started... / Decoding completed!
wc -c /tmp/Unicore_2024360.B2bssr
# 49998353
sha256sum /tmp/Unicore_2024360.B2bssr
# 对照：
# unzip -p example/postdecoder/example_out.zip example_out/UNICORE_2024360.B2bSSR | sha256sum
head -20 /tmp/Unicore_2024360.B2bssr
```

**本机首块：**

```text
> MASK 2024 12 25 00 00 12.0 0 59 B2bSatPrn_59 @ 2024 12 25 00 00 17.0
...
> CLOCK 2024 12 25 00 00 12.0 0 11 B2bSatPrn_59 @ 2024 12 25 00 00 18.0
C23      1     2     1.3120     0.0000     0.0000
```

| 头类型 | 条数（本机） |
| --- | ---: |
| `> MASK` | **3602** |
| `> CLOCK` | **86410** |
| `> ORBIT_URAI` | **13420** |
| `> DIFF_CODE_BIAS` | **13294** |

输入 **15905080** B；耗时约 **1.6 s**（本机）。`-out` 省略时默认 `<input>.B2bSSR`。

### 3.2 `postppp`（需自备 OBS · 本机未跑坐标）

示例 conf（`example/postppp/conf/postppp_25065_wuh2.conf`）要点：

- `prcopt.mode=7`（ppp-kinematic）、`prcopt.navsys=33`（GPS+BDS）、**`prcopt.sateph=5`**
- **`prcopt.B2b_format=21`**（Unicore；司南为 **20**）
- `infile*` 指向作者机绝对路径 → **必须改成** Zenodo/自备 OBS+NAV+B2b 路径

```bash
# 伪流程（路径改成你的数据根）：
# ./bin/postppp -k example/postppp/conf/postppp_25065_wuh2.conf
# 或按 postppp -? / PDF：-in OBS NAV B2b -out out.pos …
# 参考图与 .pos 在 example/postppp/example_out.zip（本机未解压复算）
```

数据集：README Zenodo（实时回放 / 事后分析）。无 OBS 时**只报告解码 E2E**，勿填假 ECEF。

### 3.3 实时（骨架）

```bash
# rtdecoder / rtppp 读 conf（example/rtdecoder、example/rtppp）
# 需串口/NTRIP/回放源；缺 /dev/tty 或挂载时会 console/config 失败——先 postdecoder 离线冒烟
```

## 4. 关键选项

### 4.1 `postdecoder`

| 项 | 作用 |
| --- | --- |
| `-U` | Unicore（UM980 等） |
| `-S` | SinoGNSS / 司南（K803W 等） |
| `-in path` | 输入 B2b 二进制（必填） |
| `-out path` | 输出 SSR；默认 `<in>.B2bSSR` |

### 4.2 `postppp`（摘）

| 项 | 作用 |
| --- | --- |
| `-k conf` | 读 `postppp_*.conf` |
| `-in …` | OBS/NAV/B2b 等输入列表（以二进制 `-?`/PDF 为准） |
| `-out file` | `.pos` |
| `-s` / `-m` | `navsys` / `mode`（源码可覆盖） |
| conf `sateph=5` | 启用 B2b |
| conf `B2b_format` | **20** 司南 / **21** 和芯 |

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| 通用 RTKLIB / explorer | [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md) |
| 嵌 2.4.3 + `.dat` 研究包 | [b2blib](./b2blib.md) |
| BNC 内 SBF→改正 | [rtppp-b2b](./rtppp-b2b.md) |
| Sept/Unicore 明文导出 | [navdecoder](./navdecoder.md) |
| Python CSSR/BDS 教学 | [cssrlib](./cssrlib.md) |
| 工作流 D | 解码冒烟 →（Zenodo）postppp → 对照 PRIDE/精密产品；教程 [06](../tutorials/06-iono-positioning.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 预编译 `bin/postdecoder` 无法运行 | 异架构/旧 ABI | 本机 `cmake --build`；`readelf -h bin/postdecoder` |
| 2 | `-U/-S` 反了，SSR 空/乱 | 接收机格式码不符 | Unicore→`-U`/`B2b_format=21`；司南→`-S`/`20` |
| 3 | `postppp` 立刻失败 | conf 内 `/home/book/...` 死路径 | 改 `infile*`/`outfile` 为本地 Zenodo 路径 |
| 4 | 当 stock `rnx2rtkp` 用 | 入口已换名 | 用 `postppp`/`rtppp`；通用 RTK 回 [rtklib](./rtklib.md) |
| 5 | 与 [b2blib](./b2blib.md) 混数据 | `.dat` 文本 ≠ 厂商二进制 | B2bLIB 走其 `testdata`；本仓走 `-in *.B2bBin` |
| 6 | 以为有 SPDX 文件 | README 有徽章、根目录无 LICENSE | 产品前补许可证或联系作者 |
| 7 | `rtppp`/`rtdecoder` 报 tty/config | 无串口/无 conf | 先 `postdecoder`；实时再配 `example/*/conf` |
| 8 | `sateph` 仍为 0/1 | 未开 B2b | conf 设 **`prcopt.sateph=5`** |
| 9 | 与 EX/apt `.pos` 对拍失败 | 引擎/改正轴不同 | 只比同仓参考 zip；勿用 explorer SPP 数值 |
| 10 | 把 MT 日志当本仓输出 | 那是 NavDecoder/其它工具 | 本仓 ASCII 头是 `> MASK`/`> CLOCK`/… |
| 11 | 缺 PDF 不会配天线/潮汐 | conf 引用 atx/blq | 用 `example/postppp/conf` 自带 `igs20_*.atx`/`ocnload_*.blq` |
| 12 | 期望开箱全球 cm 级 | 服务可见性/仰角/区域依赖 | 读 PDF 与论文 DOI；先复现 example_out |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 司南/和芯二进制 → SSR + 可编 PPP | **本文 RTKLIB-B2b** |
| VS 嵌入 + 展开 `.dat` 短样 PPP | [b2blib](./b2blib.md) |
| BNC 工程内 SBF 4242 | [rtppp-b2b](./rtppp-b2b.md) |
| 日志/SSR/SP3 导出脚本 | [navdecoder](./navdecoder.md) |
| 低成本 RTK（非 B2b） | [rtklib-explorer](./rtklib-explorer.md) |
| Python 教学 SSR | [cssrlib](./cssrlib.md) |

## 8. 相关

[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md) · [b2blib](./b2blib.md) · [rtppp-b2b](./rtppp-b2b.md) · [navdecoder](./navdecoder.md) · [cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [madocalib](./madocalib.md) · [pride-pppar](./pride-pppar.md) · [README](./README.md)

- 论文 DOI（README）：[10.1088/1361-6501/ae58c8](https://doi.org/10.1088/1361-6501/ae58c8)
- 数据：README 内 Zenodo 链接（实时回放 / 事后分析）
