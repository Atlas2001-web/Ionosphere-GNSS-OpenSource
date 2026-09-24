# B2bLIB · 北斗 PPP-B2b C/C++ 解码库操作手册

目录：[`PROJECTS.json` → `B2bLIB`](../../PROJECTS.json) · 上游 <https://github.com/GCCLib/B2bLIB> · tip **`fe7c4c0`**（2025-05 上传）· 同济相关 **GCC**（GNSS+ under Complex Conditions）· 嵌入 **RTKLIB 2.4.3 b34** · 许可**未 SPDX 标明**（商用先联系作者）· 本机验证：Linux 自写 `gcc/makefile` → `rnx2rtkp`；WUH2 2024-08-24 00:00–00:05 ×30 s + MT1–4 → **9** 历元 **Q=6** PPP · 末 ECEF ≈ (−2267750.19, 5009154.81, 3221294.23) m · 相对头近似坐标 Δ≈4.5 m · 2026-09-24 04:54 EDT

> 岗位：把北斗 **PPP-B2b** 广播改正（掩码/轨道/DCB/钟差）接到 RTKLIB 系事后 PPP。冲突时：**仓内 `manual/B2bLIB User manual.pdf` / 源码路径 > 本文**。Galileo HAS → [haslib](./haslib.md)；Python Compact SSR/BDS → [cssrlib](./cssrlib.md)；双增强对照 → PROJECTS `NavDecoder`；通用 CLI → [rtklib](./rtklib.md)；QZSS MADOCA → [madocalib](./madocalib.md)。

## 1. 用途与边界

**做：**

- 解码 PPP-B2b **MT1–4**（PRN 掩码 / 轨道 / DCB / 钟差），按历元匹配后改正广播星历
- `pos1-sateph = brdc+B2b`（`EPHOPT_B2b = 5`）驱动 PPP
- 读 **RINEX 4** 广播星历（`readRinex4Nav`，GPS LNAV + BDS CNAV1）
- 仓内 `testdata/`：WUH2 一日 OBS + `brd42370.24p` + 四类 `.dat` + `PPPB2b.conf`
- 结构：消息解码（`B2bLIB.c`）+ 处理（改过的 `postpos.c` / `ppp.c` / `ephemeris.c`）

**不做：**

- **不是** 官方运营保证——手册免责；改正可见性随地域/仰角变化
- **不是** Galileo HAS 解码 → [haslib](./haslib.md)；**不是** QZSS CLAS → [claslib](./claslib.md)
- **不是** 发表级多站 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- **不是** 开箱 Linux CLI：上游手册以 **Visual Studio 2022** 为主；Linux 须自备 makefile 并改硬编码路径
- 许可空白 → 科研可试；产品嵌入前联系 GCC / 作者

一句话：B2bLIB = **可嵌入 RTKLIB 的北斗 PPP-B2b 研究解码包**。

| 术语 | 含义 |
| --- | --- |
| PPP-B2b / MT1–4 | 北斗三号 B2b 精密改正：掩码、轨道、DCB、钟差 |
| `brdc+B2b` | conf 星历模式 5；匹配失败则回退纯广播 |
| `PrnMask*.dat` 等 | 已展开的文本改正样例（非原始 B2b 比特流） |
| Q=6 | RTKLIB PPP 浮点解（非 fix） |
| `readRinex4Nav` | 专读 RINEX4 多星座导航；路径在 `main` 硬编码 |

## 2. 安装

### 2.1 上游意图（Windows）

手册 §5：VS2022 建工程，加入 `src/*.c` + `B2bLIB.h` / `B2bMSG.h` / `rtklib.h`；调试参数示例：

```text
-k ..\..\testdata\PPPB2b.conf ..\..\testdata\WUH22370.24o -o ..\..\testdata\PPP.pos
```

并在 `main` / `inputobs` 中改 **RINEX4 导航** 与 **四类 B2b `.dat`** 的绝对/相对路径（默认 `D:\B2bLIB\testdata\...`）。

### 2.2 Linux 最小可跑（本机）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/GCCLib/B2bLIB.git
cd B2bLIB && git rev-parse --short HEAD   # 本机 fe7c4c0

# 解压样例
cd testdata && for z in *.zip; do unzip -o -q "$z"; done && cd ..

# 1) 改 RINEX4 导航路径（rnx2rtkp.c）
sed -i 's|strcpy(rinex4NavfilePath, "../../testdata/brd42370.24p");|strcpy(rinex4NavfilePath, "'"$PWD"'/testdata/brd42370.24p");|' src/rnx2rtkp.c

# 2) 改四类 B2b 路径（postpos.c；两处 forward/backward 一并替换）
TD="$PWD/testdata"
sed -i \
  -e "s|D:\\\\\\\\B2bLIB\\\\\\\\testdata\\\\\\\\PrnMask20240824.dat|$TD/PrnMask20240824.dat|g" \
  -e "s|D:\\\\\\\\B2bLIB\\\\\\\\testdata\\\\\\\\OrbCorr20240824.dat|$TD/OrbCorr20240824.dat|g" \
  -e "s|D:\\\\\\\\B2bLIB\\\\\\\\testdata\\\\\\\\DcbCorr20240824.dat|$TD/DcbCorr20240824.dat|g" \
  -e "s|D:\\\\\\\\B2bLIB\\\\\\\\testdata\\\\\\\\ClkCorr20240824.dat|$TD/ClkCorr20240824.dat|g" \
  src/postpos.c

# 3) 兼容：BOOL / initB2b 返回类型（gcc）
printf '%s\n' '#pragma once' 'typedef int BOOL;' '#define TRUE 1' '#define FALSE 0' > gcc_b2b_compat.h
sed -i 's/extern initB2b(nav_t\* navs);/extern void initB2b(nav_t* navs);/' src/B2bLIB.h
# 若 B2bLIB.c 仍写 `extern initB2b(` → 改成 `extern void initB2b(`；`BOOL isture` → `int isture`

mkdir -p gcc && cd gcc
cat > makefile <<'MAKE'
SRC=../src
CFLAGS=-std=c99 -O2 -Wall -Wno-unused-but-set-variable -Wno-unused-variable -Wno-implicit-int \
  -I$(SRC) -DTRACE -DNFREQ=3 -include ../gcc_b2b_compat.h
LDLIBS=-lm -lrt -lpthread
OBJS=rnx2rtkp.o B2bLIB.o rtkcmn.o rinex.o rtkpos.o postpos.o solution.o \
  lambda.o geoid.o sbas.o preceph.o pntpos.o ephemeris.o options.o \
  ppp.o ppp_ar.o rtcm.o rtcm2.o rtcm3.o rtcm3e.o ionex.o tides.o
all: rnx2rtkp
rnx2rtkp: $(OBJS); $(CC) -o $@ $(OBJS) $(LDLIBS)
%.o: $(SRC)/%.c; $(CC) -c $(CFLAGS) -o $@ $<
MAKE
make -j"$(nproc)"
./rnx2rtkp -? | head -3
# 期望：usage: rnx2rtkp [option]... file file [...]
```

勿链入 `rcvraw.o`/`stream.o`（会缺厂商 `input_*` 符号）；RINEX 事后 PPP 不需要它们。

## 3. 端到端：WUH2 5 分钟 PPP-B2b（本机真跑）

```bash
cd ~/iono_ops/B2bLIB
./gcc/rnx2rtkp -ts 2024/08/24 00:00:00 -te 2024/08/24 00:05:00 -ti 30 \
  -k testdata/PPPB2b.conf \
  testdata/WUH22370.24o \
  -o /tmp/b2b_ppp.pos
rg -c '   6  ' /tmp/b2b_ppp.pos
tail -3 /tmp/b2b_ppp.pos
```

**本机结果（tip `fe7c4c0`，2026-09-24 04:54 EDT）：**

```text
% program   : RTKLIB ver.2.4.3
% pos mode  : PPP Static
% navi sys  : GPS BDS
processing … Q=0 → Q=6（约 00:01:30 起）

9 条 Q=6 解（30 s 间隔，UTC）
首：2024/08/24 00:00:42  -2267752.5891  5009150.8753  3221299.2815  Q=6  ns=17
末：2024/08/24 00:04:42  -2267750.1948  5009154.8089  3221294.2304  Q=6  ns=16
头近似坐标：(-2267749, 5009154, 3221290)；末历元 ECEF Δ≈4.5 m（短弧浮点，正常）
```

| 输入 | 说明 |
| --- | --- |
| `WUH22370.24o` | WUH2 混合 OBS（RINEX 3.05）；DOY 237 = 2024-08-24 |
| `brd42370.24p` | RINEX4 导航（`main` 内读，**不必**再当 argv） |
| `PrnMask/OrbCorr/DcbCorr/ClkCorr20240824.dat` | MT1–4；`postpos` **每历元 fopen** |
| `PPPB2b.conf` | `pos1-sateph=brdc+B2b`，`pos1-navsys=33`（GPS+BDS），PPP-static |

| 输出字段 | 含义 |
| --- | --- |
| Q=6 | PPP 浮点 |
| ns | 所用卫星数 |
| x/y/z-ecef | WGS84 ECEF（conf `out-solformat=xyz`） |
| 时间 | conf `out-timesys=utc` → UTC |

全日解把 `-te` 去掉即可；注意每历元重读 ~23 MB `ClkCorr*.dat`，I/O 会很慢——生产应改成一次载入（上游研究代码未做）。

## 4. 关键 API / 旗标

| 符号 / 旗标 | 作用 |
| --- | --- |
| `readB2bType1…4` | 读掩码/轨道/DCB/钟差到 `nav->b2bsat` |
| `satpos_B2b` / `ephpos_B2b` | 应用 B2b 改正后的卫星位置/钟 |
| `initB2b` | 初始化 B2b 状态 |
| `satSlot2Sat` / `sat2Slot` | B2b 槽位 ↔ RTKLIB `sat` |
| `-k` / `-o` / `-ts`/`-te`/`-ti` | 同 RTKLIB `rnx2rtkp` |
| `pos1-sateph=brdc+B2b` | 打开 B2b 星历模式 |

## 5. 接到哪步

- 改正字节/字段理解 → 对照 [cssrlib](./cssrlib.md) BDS PPP 样例；HAS 对照 [haslib](./haslib.md)
- 另一 B2b 引擎：PROJECTS `RTKLIB-B2b` / `RTPPP_B2b` / `NavDecoder`（本目录未单独短硬时以 PROJECTS 为准）
- 通用事后 PPP → [rtklib](./rtklib.md)；发表级 → [pride-pppar](./pride-pppar.md)
- QZSS 开放 PPP → [madocalib](./madocalib.md) / [claslib](./claslib.md)
- 工作流 **D**：QC → 开放改正（本文/HAS/CLAS）→ [pride-pppar](./pride-pppar.md)；数据 [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 启动即 segfault / 无改正 | `D:\B2bLIB\…` 路径在 Linux 无效且 `fopen` 未判空 | 按 §2.2 `sed` 改成本机 `testdata` 绝对路径 |
| 2 | `READ Rinex4nav Ephemeris ERROR` | `rinex4NavfilePath` 仍指向 `../../testdata/...` | 改 `rnx2rtkp.c` 中 `strcpy(rinex4NavfilePath, …)` |
| 3 | `unknown type name 'BOOL'` | MSVC 类型；gcc 无 | `-include` 兼容头或把 `BOOL` 改 `int` |
| 4 | `initB2b` implicit-int / 冲突 | 头文件缺 `void` | `extern void initB2b(nav_t*);` 两端对齐 |
| 5 | 链接缺 `input_ubx` / `input_bnx` | 链了 `rcvraw`/`stream` 未链厂商源 | 事后 PPP：**不要**链这两个 `.o` |
| 6 | 极慢（每秒级历元） | 每历元 `fopen` 整份 `ClkCorr`（~23 MB） | 先 `-te` 截短窗；或改源码一次载入 |
| 7 | 头里 `% ephemeris :` 空白 | 选项名打印未覆盖 `brdc+B2b` | 可忽略；以 conf 与 Q=6 为准 |
| 8 | 当 HAS/CLAS 库用 | 星座/电文不同 | HAS→[haslib](./haslib.md)；CLAS→[claslib](./claslib.md) |
| 9 | 与系统 `rnx2rtkp` 混淆 | 同名不同叉 | `./gcc/rnx2rtkp`；勿覆盖 apt RTKLIB |
| 10 | 商用发货被问许可 | 仓内无 SPDX | 联系 GCC / README 作者后再嵌入 |
| 11 | 只有 OBS argv、忘改 B2b 路径 | 改正不在命令行，在源码字符串 | 必须改 `postpos.c` 四路径 |
| 12 | 期望 Q=1 固定 | 样例/短弧为 PPP 浮点 | Q=6 即成功路径；AR 另开 `pos2-armode` 并自验 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 北斗 PPP-B2b ↔ RTKLIB C 嵌入 | **本文 B2bLIB** |
| Galileo HAS 页→RTCM/IGS SSR | [haslib](./haslib.md) |
| Python 多系统开放 PPP/PPP-RTK | [cssrlib](./cssrlib.md) |
| QZSS CLAS / MADOCA 官方库 | [claslib](./claslib.md) / [madocalib](./madocalib.md) |
| 通用事后引擎 | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) |

## 8. 相关

[haslib](./haslib.md) · [cssrlib](./cssrlib.md) · [claslib](./claslib.md) · [madocalib](./madocalib.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [data-access](../data-access.md) · [README](./README.md)

- 手册 PDF：仓内 `manual/B2bLIB User manual.pdf`（扫描版；§5 Compile/Run、§6 验证）
- 样例数据日：2024-08-24（GPS week 2328）站 **WUH2**
