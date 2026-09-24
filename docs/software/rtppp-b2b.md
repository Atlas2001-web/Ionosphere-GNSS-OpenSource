# RTPPP_B2b · 北斗 PPP-B2b 实时改正接口（BNC/SBF）操作手册

目录：[`PROJECTS.json` → `RTPPP_B2b`](../../PROJECTS.json) · 上游 <https://github.com/floating0516/RTPPP_B2b> · tip **`9864c66`**（2025-12-12 merge master→main）· **无 SPDX / 无 LICENSE**（商用先联系作者）· 依赖 **Qt5 + BNC 头**（`bnccore.h` / `GPSDecoder.h` / `satObs.h` / `clock_orbit_rtcm.h` / `bnctime.h` / `rtkdefine.h`）· 本机验证：clone 深 1；源 **~5.0 k** LOC（`PPPB2bDecoder` 979 + `SBFDecoder` 370 + `SBFcoDecoder` 336 + `bncsate` 504 + 头/`rtklib.h`）；自检 CRC-16-CCITT 空缓冲→**0**、`01 02 03`→**0x6131**；MT **1–7**；**缺 BNC/Qt 工程 → 未链接可执行文件、未喂二进制 SBF** · 2026-09-24 05:45 EDT

> 岗位：把 Septentrio **SBF 块 4242（BDSRawB2b）** 解成 RTCM 风格轨道/钟差，嵌入 **BNC** 类实时 PPP 管线。冲突时：**仓内 `README_zh.md` / `README_en.md` / 源码路径 > 本文**。嵌 RTKLIB 事后 B2b → [b2blib](./b2blib.md)；Python 明文/导出 → [navdecoder](./navdecoder.md)；HAS → [haslib](./haslib.md)；Python CSSR → [cssrlib](./cssrlib.md)；QZSS → [madocalib](./madocalib.md)。

## 1. 用途与边界

**做：**

- `SBFDecoder`：同步字 `0x24 0x40`、长度/类型、**CRC-16-CCITT**，转发帧
- `PPPB2bDecoder`：4242 负载 → LDPC → 解析 **MT1–7**（掩码/轨道/DCB/钟差等）→ 缓冲 → `t_orbCorr` / `t_clkCorr`
- `SBFcoDecoder`：B2b 导航比特 **LDPC**（BCNV3，GF(2⁶) 扩展最小和）
- `bncsate`：与 BNC 卫星状态/UI 相关的 Qt 部件（非独立 PPP 引擎）

**不做：**

- **不是** 开箱 `cmake && make` 的 CLI——无 CMake/Makefile，无样例 `.sbf`，缺 BNC 私有头则**无法**本仓单独链接
- **不是** 完整 PPP 滤波器——只产改正；解算接 BNC / [rtklib](./rtklib.md) / [b2blib](./b2blib.md) / [cssrlib](./cssrlib.md)
- **不是** 明文 `BDSRawB2b` CSV（NavDecoder 那种）——输入是 **二进制 SBF 流**
- **不是** Galileo HAS / QZSS CLAS·MADOCA → [haslib](./haslib.md)/[claslib](./claslib.md)/[madocalib](./madocalib.md)
- 许可空白 → 科研可试；产品嵌入前联系作者

一句话：RTPPP_B2b = **面向 BNC 的 SBF→PPP-B2b 改正插件源码切片**；CI 机通常验 API/CRC/缺头清单，完整实时链需自备 BNC 树 + 接收机/回放。

| 术语 | 含义 |
| --- | --- |
| SBF 4242 | Septentrio `BDSRawB2b` 块类型号 |
| MT1…MT7 | B2b 消息：掩码、轨道、码偏差、钟差等（源码 `case 1…7`） |
| LDPC / BCNV3 | B2b 导航比特纠错；`decode_LDPC_navbitsRaw` |
| `t_orbCorr` / `t_clkCorr` | 项目内 RTCM3 风格改正；经信号/`ClockOrbit` 发出 |
| BNC | BKG NTRIP Client；本仓头文件假定已嵌入其工程 |

## 2. 安装 / 嵌入

### 2.1 获取

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/floating0516/RTPPP_B2b.git
cd RTPPP_B2b && git rev-parse --short HEAD   # 本机 9864c66
ls *.cpp *.h *.md
```

| 文件 | 角色（本机） |
| --- | --- |
| `SBFDecoder.{h,cpp}` | SBF 帧同步/CRC/分发 |
| `PPPB2bDecoder.{h,cpp}` | B2b 解析与改正发出（QObject） |
| `SBFcoDecoder.{h,cpp}` | LDPC |
| `bncsate.{h,cpp}` | BNC 侧卫星 UI/状态 |
| `rtklib.h` | 随仓裁剪/配套头（**不能**替代完整 RTKLIB 源） |
| `README_zh.md` / `README_en.md` | 数据流与关键函数说明 |

### 2.2 缺头探针（本机）

```bash
cd ~/iono_ops/RTPPP_B2b
python3 - <<'PY'
from pathlib import Path
import re
need=set(); local={p.name for p in Path('.').iterdir()}
for p in list(Path('.').glob('*.h'))+list(Path('.').glob('*.cpp')):
    need |= set(re.findall(r'#include\s*"([^"]+)"', p.read_text(errors='replace')))
print('MISSING', sorted(need-local))
PY
# 期望 MISSING 含：GPSDecoder.h bnccore.h bnctime.h rtkdefine.h satObs.h
# （PPPB2bDecoder.h 另 extern "C" #include "clock_orbit_rtcm.h"）
```

### 2.3 嵌进 BNC（上游意图；路径以你的 BNC 树为准）

1. 准备可编译的 **BNC** 源码树（含 `bnccore`、`GPSDecoder`、`clock_orbit_rtcm` 等）
2. 将本仓 `.cpp/.h` 加入其 Qt `.pro` / CMake，并保证 **Qt5 Core/Widgets** 已链
3. 在流处理路径对 SBF 输入调用 `SBFDecoder::Decode(buf,len,errmsg)`
4. 订阅 `PPPB2bDecoder` 的 `newOrbCorrections` / `newClkCorrections`（或 `ClockOrbit` 注入点）接到你的 PPP
5. **无**官方逐步截图——以源码 `#include` 与 BNC 版本文档为准

### 2.4 本机不可链接时的最小自检（CRC + MT 清单）

```bash
cd ~/iono_ops/RTPPP_B2b
python3 - <<'PY'
import re
src=open('SBFDecoder.cpp').read()
nums=[int(x,0) for x in re.findall(r'0x[0-9a-fA-F]+',
      re.search(r'CRC_16CCIT_LookUp\[256\] = \{([^}]+)\}', src, re.S).group(1))]
assert len(nums)==256
def crc(b: bytes) -> int:
    c=0
    for x in b:
        c=((c<<8)&0xFFFF) ^ nums[((c>>8)^x)&0xFF]
    return c
print('crc_empty', crc(b''))
print('crc_010203', hex(crc(bytes([1,2,3]))))
print('sync', hex(0x24), hex(0x40), 'type_BDSRawB2b', 4242)
print('MT', sorted({int(x) for x in re.findall(r'^\s*case\s+(\d+)\s*:', open('PPPB2bDecoder.cpp').read(), re.M)}))
PY
# 期望：crc_empty 0 · crc_010203 0x6131 · MT [1,2,3,4,5,6,7]
```

## 3. 端到端

### 3.1 源码/API 探针（本机已跑）

**结果（tip `9864c66`，2026-09-24 05:45 EDT）：**

| 探针 | 值 |
| --- | --- |
| tip | **`9864c66`**（2025-12-12 +0800） |
| LOC（四 `.cpp`+头/`rtklib.h`） | ≈ **5030** 行 |
| SBF sync | `0x24 0x40`（`$` `@`） |
| B2b 块类型 | **4242** |
| CRC 空 / `01 02 03` | **0** / **0x6131** |
| `case` MT | **1–7** |
| 缺头 | `GPSDecoder.h` `bnccore.h` `bnctime.h` `rtkdefine.h` `satObs.h` + `clock_orbit_rtcm.h` |
| 可执行 PPP 解 | **无**（未嵌 BNC） |

### 3.2 有 BNC + SBF 回放时（推荐路径；本机无流）

1. 接收机开 **BDSRawB2b (4242)** 输出，或录制 `.sbf` 回放
2. BNC 侧启用嵌入后的 SBF→B2b 解码（以你的工程菜单/配置为准）
3. 日志中应出现类似 `MT1 MASK` / `MT2 ORBIT` / `MT4 CLOCK` / `BDS ORB` / `BDS CLK`（源码 `slotMessage` 字符串）
4. 将发出的轨道/钟差接到实时 PPP；区域/仰角决定 B2b 可见性

### 3.3 旁路对照（有明文样例时）

Septentrio **文本** `BDSRawB2b` 导出 → [navdecoder](./navdecoder.md) `decode_B2B_sept.py`（仓内样例可出 `.ssr`/`.log`）。  
事后嵌 RTKLIB → [b2blib](./b2blib.md)（WUH2 样例 Q=6）。  
**二者输入格式 ≠ 本仓二进制 SBF**，只作改正语义对照。

## 4. I/O 与关键 API

| 输入 | 说明 |
| --- | --- |
| SBF 字节流 | 帧头 sync+CRC；关注 type **4242** |
| BNC 运行时 | `BNC_CORE`、站 ID、时钟模型对象 |

| 输出 | 含义 |
| --- | --- |
| `ppp_ssr_orbit` / `ppp_ssr_clock` / mask | 内部 SSR 缓冲 |
| `t_orbCorr` / `t_clkCorr` | RTCM 风格改正列表 |
| Qt signals | `newOrbCorrections` / `newClkCorrections` |

| API | 作用 |
| --- | --- |
| `SBFDecoder::Decode` | 同步、CRC、分帧 |
| `PPPB2bDecoder::input` | 识别 4242 → `decode_b2b_payload` |
| `SBFcoDecoder::decode_LDPC_navbitsRaw` | 仅要纠错净荷时也可单用 |
| `emitCorrections` | MT2/MT4 等触发发出 |

## 5. 接到哪步

- 事后 B2b↔RTKLIB → [b2blib](./b2blib.md)；多厂商明文解码 → [navdecoder](./navdecoder.md)
- HAS / CSSR 教学 → [haslib](./haslib.md) / [cssrlib](./cssrlib.md)；MADOCA → [madocalib](./madocalib.md)
- 多流 GUI 录盘 → [bnc](./bnc.md)；SBF 块解析旁路 → [sbfparser](./sbfparser.md)/[pysbf2](./pysbf2.md)
- 工作流 **C/D**：实时改正（本文）→ PPP 引擎；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `fatal error: bnccore.h` | 本仓不是完整 BNC | 把源码放进 BNC 树或补齐头/库路径 |
| 2 | 无 CMake、不知如何跑 | 上游只给插件切片 | 按 §2.3 嵌工程；或改用 [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md) |
| 3 | CRC 总失败 | 缓冲未按 SBF 对齐 / 截断帧 | 确认 sync `$@`；CRC 覆盖 `[4..len)`（见 `SBFDecoder.cpp`） |
| 4 | 有 SBF 无改正 | 未开 4242 或非 B2b 频点 | 接收机配置 `BDSRawB2b`；查 type 日志 |
| 5 | 喂 NavDecoder 的 `.txt` | 那是 CSV 明文，不是二进制 SBF | 用 [navdecoder](./navdecoder.md)；或先转真正 SBF |
| 6 | `QObject` / signals 链接错 | 未开 Qt MOC | `.pro` 把头加入 `HEADERS` 并跑 moc |
| 7 | 当完整 RTKLIB 用 | 仅有裁剪 `rtklib.h` | 解算用系统 [rtklib](./rtklib.md) 或 [b2blib](./b2blib.md) |
| 8 | MT5–7 无 ORB/CLK 日志 | 源码对 5–7 处理弱/占位 | 以 MT1/2/4 为主；读 `b2b_parsecorr` 分支 |
| 9 | 期望全球实时可用 | B2b 有服务区/仰角限制 | 查可见 PRN；勿与 IGS RTS 混谈 |
| 10 | 商用审计失败 | 无 LICENSE | 联系 GitHub 作者后再嵌入 |
| 11 | 与 [b2blib](./b2blib.md) 改正数值差 | 输入形态/历元/IOD 匹配不同 | 同日同站对照 IODN/IODP；勿直接比浮点 |
| 12 | `winsock` 分支干扰 Linux | 随仓 `rtklib.h` 含 Win 路径 | 在 BNC/Linux 构建里用工程自带平台头，勿混编译 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| BNC 内实时 SBF→B2b 改正接口 | **本文 RTPPP_B2b** |
| 事后 RINEX + B2b `.dat`→PPP | [b2blib](./b2blib.md) |
| Sept/Unicore 明文 → SSR/SP3 | [navdecoder](./navdecoder.md) |
| Galileo HAS→RTCM/IGS | [haslib](./haslib.md) |
| Python 多系统开放 PPP | [cssrlib](./cssrlib.md) |
| QZSS MADOCA 官方库 | [madocalib](./madocalib.md) |

## 8. 相关

[b2blib](./b2blib.md) · [navdecoder](./navdecoder.md) · [haslib](./haslib.md) · [cssrlib](./cssrlib.md) · [madocalib](./madocalib.md) · [bnc](./bnc.md) · [sbfparser](./sbfparser.md) · [pysbf2](./pysbf2.md) · [rtklib](./rtklib.md) · [data-access](../data-access.md) · [README](./README.md)

- README 关键函数行号以仓内为准（文件曾扁平在仓库根，注释里仍写 `SBF/` 前缀）
- 姊妹条目：PROJECTS `RTKLIB-B2b` / `B2bLIB` / `NavDecoder`
