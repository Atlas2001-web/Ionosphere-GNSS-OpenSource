# SbfParser · Septentrio SBF 流/文件解析操作手册

目录：[`PROJECTS.json` → `SbfParser`](../../PROJECTS.json) · 上游 <https://github.com/septentrio-gnss/SbfParser> · PyPI **`sbf-parser` 1.0.3** · tip **`ea84256`**（2025-08-06）· 许可 **BSD-3-Clause**（`LICENSE`；`pyproject.toml` 误标 MIT）· 本机：`sbf_files/receiver_status.sbf` / `log_0000.sbf` / `all_blocks_0000.sbf` / ExtEvent 往返 / 512 B 分块；交叉 HASlib `Tests/galileo_ssr003.sbf` → **GALRawCNAV=11774** · 2026-09-24 05:06 EDT

> 岗位：Septentrio **SBF** 文件或字节流 → `(块名, 字段 dict)`；可 `encode` 回字节。冲突时：**本机 `help(sbf_parser.read)` / 仓 README / mosaic 参考手册 PDF > 本文**。HAS 页→SSR → [haslib](./haslib.md)；ISMR **下载** → [ismr-downloader](./ismr-downloader.md)；u-blox 对照 → [pyubx2](./pyubx2.md)。**无 console entry point**。

## 1. 用途与边界

**做：**

- Cython 解析：`read(path)` / `load(fobj)` / `parse(bytes)`；流式 `SbfParser().parse(chunk)`
- tip 块表 **116** 项（对照仓内 mosaic-X5 v4.14.10.1 Reference Guide），含 `MeasEpoch`、`GALRawCNAV`、`ReceiverStatus`、`ExtEvent` 等
- `encode` 回写已实现块；`payload` 可无损保留原帧（`payload_priority`）
- 混流中的 ASCII/残帧可标为 `Replie` / `Transmission` / `Description` / `Snmp` / `BadSBF` / `Unknown`

**不做：**

- **不是** Galileo HAS 拼页/SSR 引擎 → [haslib](./haslib.md)（本库只把 `GALRawCNAV` 等拆开）
- **不是** ISMR/S4/σφ 产品链；tip **`BLOCKNAMES` 无 `ISM*`、无块号 4086**（PROJECTS 文案超前）。ISMR 文件仍走 [ismr-downloader](./ismr-downloader.md)
- **不是** RINEX 转换 / PPP / ROTI → [autorino](./autorino.md) / [rtklib](./rtklib.md) / [oasis-roti](./oasis-roti.md)
- **不是** UBX → [pyubx2](./pyubx2.md)；纯 Python SBF 备选 → 目录 **pysbf2**（尚无短硬手册）

一句话：SbfParser = **官方生态 SBF↔结构化字典**；电离层产品在抽块之后。

| 术语 | 含义 |
| --- | --- |
| SBF | Septentrio Binary Format；同步头常为 `$@`（`24 40`） |
| 迭代第 1 项 / `blockName` | 已解析块名；未知/损坏见 `BadSBF` 等 |
| `blockType` | `SBF`（结构展开）/ `RawSBF`（如部分 `Commands`）/ `Unknown`… |
| `TOW` / `WNc` | 周内 ms / 连续周 |
| `payload` | 块原始 `bytearray` |
| `SbfParser` | 默认 **1 MB** 缓冲的流式解析器；跨 `parse` 保状态 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip wheel
python -m pip install 'sbf-parser==1.0.3'
python - <<'PY'
import importlib.metadata as m, sbf_parser
print(m.version('sbf_parser'), sbf_parser.__version__, sbf_parser.__all__)
print('entry_points', list(m.distribution('sbf_parser').entry_points))
PY
# 期望：
# 1.0.3 1.0 ['read', 'load', 'parse', 'encode', 'SbfParser', 'replace_header_time']
# entry_points []
```

源码（样例 SBF 在仓内）：

```bash
git clone --depth 1 https://github.com/septentrio-gnss/SbfParser.git
cd SbfParser
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip wheel 'Cython>=0.29' setuptools
python -m pip install -e .
git rev-parse --short HEAD   # 期望：ea84256
ls sbf_files/
# receiver_status.sbf  log_0000.sbf  all_blocks_0000.sbf  large_0000.sbf  jamming.sbf
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'sbf_parser'` | PyPI 名连字符、import 下划线；或未进 venv | `pip install sbf-parser`；`source .venv/bin/activate` |
| 编译失败 | 缺 Cython/头文件/编译器 | `pip install Cython setuptools wheel`；装 `python3-dev` `build-essential` |
| `sbf-parser: command not found` | **无 CLI** | 只用库 API |

## 3. 端到端（本机 1.0.3 / tip `ea84256`）

下列 stdout 均来自本机实跑；路径相对克隆根目录。

### 3.1 单块 `ReceiverStatus`

```bash
cd ~/iono_ops/SbfParser && source .venv/bin/activate
python - <<'PY'
from sbf_parser import read
for name, info in read('sbf_files/receiver_status.sbf'):
    print(name)
    print({k: v for k, v in info.items() if k != 'payload'})
    print('payload_len', len(info['payload']))
PY
```

**本机 stdout：**

```text
ReceiverStatus
{'TOW': 49638143, 'WNc': 2368, 'CPULoad': 1, 'ExtError': 2, 'UpTime': 10000000, 'RxState': 20000000, 'RxError': 40000000, 'N': 2, 'SBLength': 4, 'CmdCount': 64, 'Temperature': 128, 'AGCState': [{'FrontendID': 1, 'Gain': 2, 'SampleVar': 4, 'BlankingStat': 8}, {'FrontendID': 16, 'Gain': 32, 'SampleVar': 64, 'BlankingStat': 128}], 'blockType': 'SBF', 'blockName': 'ReceiverStatus'}
payload_len 40
```

| 字段 | 本样例 |
| --- | --- |
| `TOW` / `WNc` | 49638143 ms / 周 2368 |
| `N` + `AGCState` | 2 路前端 AGC 子块 |
| `Temperature` | 128（样例填充；实机才是温度） |
| `payload_len` | 40（与文件等长） |

### 3.2 清单：`log_0000.sbf` + `MeasEpoch`

```bash
python - <<'PY'
from collections import Counter
from sbf_parser import read
c, tows = Counter(), []
meas = None
for name, info in read('sbf_files/log_0000.sbf'):
    c[name] += 1
    if 'TOW' in info:
        tows.append(info['TOW'])
    if meas is None and name == 'MeasEpoch' and info.get('N1', 0) > 0:
        t1 = info['Type_1'][0]
        meas = (info['TOW'], info['N1'], {k: t1[k] for k in
                ('RxChannel', 'Type', 'SVID', 'CN0', 'LockTime', 'Doppler', 'N2')})
print('n_blocks', sum(c.values()), 'n_types', len(c))
print('top5', c.most_common(5))
print('TOW_minmax', (min(tows), max(tows)))
print('MeasEpoch TOW/N1', meas[0], meas[1])
print('Type_1[0]', meas[2])
PY
```

**本机结果：**

```text
n_blocks 748 n_types 49
top5 [('GALRawINAV', 114), ('GLORawCA', 108), ('BDSRaw', 64), ('GLOAlm', 24), ('GEORawL1', 24)]
TOW_minmax (200465000, 212552000)
MeasEpoch TOW/N1 212541000 45
Type_1[0] {'RxChannel': 1, 'Type': 0, 'SVID': 20, 'CN0': 69, 'LockTime': 229, 'Doppler': -23902778, 'N2': 1}
```

`all_blocks_0000.sbf`：本机 **281** 块 / **64** 类。`large_0000.sbf`（~42 MB）：**309374** 块 / **81** 类，约 **1.15 s**（~36 MB/s，机器相关）。

### 3.3 流式分块（应等于整读）

```bash
python - <<'PY'
from sbf_parser import SbfParser
raw = open('sbf_files/log_0000.sbf', 'rb').read()
p, n = SbfParser(), 0
for i in range(0, len(raw), 512):
    for _ in p.parse(raw[i:i+512]):
        n += 1
print('chunked_n', n)   # 期望：748
PY
```

### 3.4 `encode` ↔ `parse`（`ExtEvent`）

```bash
python - <<'PY'
from sbf_parser import encode, parse
status, blob = encode({
    'blockName': 'ExtEvent',
    'TOW': 123456789, 'WNc': 2120, 'Source': 1, 'Polarity': 0,
    'Offset': 0.005, 'RxClkBias': 0.0, 'PVTAge': 0,
})
print(status, len(blob), blob[:8].hex())
for name, info in parse(blob):
    print(name, {k: info[k] for k in info if k != 'payload'})
PY
```

**本机 stdout：**

```text
encoded 32 2440ecea24172000
ExtEvent {'TOW': 123456789, 'WNc': 2120, 'Source': 1, 'Polarity': 0, 'Offset': 0.004999999888241291, 'RxClkBias': 0.0, 'PVTAge': 0, 'blockType': 'SBF', 'blockName': 'ExtEvent'}
```

`Offset` 经 float32 往返微变属正常。

### 3.5 同一 SBF 交给 haslib 前先点货

```bash
# 路径换成你的 HASlib 克隆
python - <<'PY'
from collections import Counter
from sbf_parser import read
c = Counter(n for n, _ in read('~/iono_ops/HASlib/Tests/galileo_ssr003.sbf'.replace('~', __import__('os').path.expanduser('~'))))
print('n', sum(c.values()), 'GALRawCNAV', c['GALRawCNAV'], 'GALRawINAV', c['GALRawINAV'])
PY
# 本机（9632656 B）：n=64898 GALRawCNAV=11774 GALRawINAV=11960
```

HAS 拼页/SSR 仍用 [haslib](./haslib.md)（同文件 `-x 3000 -v 1` → 11 HAS）。

## 4. I/O 与参数

| API | 输入 | 输出 |
| --- | --- | --- |
| `read(path)` | 路径 | 迭代 `(name, dict)` |
| `load(fobj)` | **文件对象**（不要传 `bytes`） | 同上 |
| `parse(content)` | `bytes`/`bytearray` | 同上 |
| `SbfParser().parse(chunk)` | 分片 | 同上；状态保留 |
| `encode(block, payload_priority=1)` | 字段 dict | **`(status:str, bytes)`** |
| `replace_header_time` | 见库/utils | 改头 TOW |

| `payload_priority` | 行为 |
| --- | --- |
| `0` | 有 `payload` 即用 |
| `1`（默认） | 编码失败/未实现时回退 `payload` |
| `-2` / `-3` | 仅未实现 / 绝不使用 `payload` |

仓内脚本（非 entry point）：`utils/split_sbf_file.py`、`replace_header_time.py`、`benchmark.py`、`compare_with_ascii.py`；示例见 `example/`。

## 5. 接到哪步

| 上下游 | 接法 |
| --- | --- |
| [ismr-downloader](./ismr-downloader.md) `data-type=sbf` | 下载 PolaRx SBF → 本库点货/`MeasEpoch`；**ISMR 专用块 tip 未实现** |
| [haslib](./haslib.md) | 本库确认 `GALRawCNAV` → haslib → [cssrlib](./cssrlib.md)/[rtklib](./rtklib.md) |
| [pyubx2](./pyubx2.md) | 协议对照（UBX↔SBF）；**勿混用解析器** |
| pysbf2（PROJECTS 有、**无** `pysbf2.md`） | 纯 Python、可生成/混 NMEA·RTCM；官方 Cython 块表/性能 → **本篇** |
| 闪烁指数/仿真 | [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)/[iono-scintillation](./iono-scintillation.md) |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `pip install SbfParser` 失败 | PyPI 名为 **`sbf-parser`** | `pip install sbf-parser==1.0.3` |
| 2 | `import sbf-parser` | import 下划线 | `import sbf_parser` |
| 3 | `encode` 解包成 1 个值崩 | 返回 **`(status, bytes)`** | `status, blob = encode(...)` |
| 4 | `load(f.read())` TypeError | `load` 要 file object | `load(open(path,'rb'))` 或 `parse(data)` |
| 5 | `__version__=='1.0'` 与 PyPI 1.0.3 不一致 | 模块版本未同步 | 以 `importlib.metadata.version('sbf_parser')` 为准 |
| 6 | 许可 MIT 还是 BSD | `pyproject.toml` 误写 MIT | 以 `LICENSE` / PROJECTS：**BSD-3-Clause** |
| 7 | 流式丢大块/截断 | 缓冲默认 **1 MB** | 单块通常 ≤4096 B；更大需改 fork |
| 8 | `Commands` 几乎无字段 | `blockType='RawSBF'` | 当 `payload` 用，或 RxTools/sbf2ascii |
| 9 | 指望解 ISMR 4086 / S4 | tip **无 ISM 块** | 下载用 ismr-downloader；块解析另选工具 |
| 10 | 找 CLI | 无 entry_points | 写短脚本；utils 在仓内跑 |
| 11 | float 往返微差 | float32 | 容差比较 |
| 12 | 超大日志内存顶满 | `read` 一次读入 | `SbfParser` 分块，或 `split_sbf_file` |

## 7. 选型与链接

| 你要… | 用 |
| --- | --- |
| 官方 Cython、快、仓内样例 | **本文 SbfParser（sbf-parser）** |
| 纯 Python、与 pyubx2/pyrtcm 同栈 | **pysbf2**（semuconsulting；建议下一短硬） |
| 老 GPL 解析器 | `pysbf`（维护/许可自审） |
| SBF → HAS SSR | [haslib](./haslib.md) |
| UBX | [pyubx2](./pyubx2.md) |
| ISMR 批量下载 | [ismr-downloader](./ismr-downloader.md) |

- 上游：<https://github.com/septentrio-gnss/SbfParser>
- PyPI：<https://pypi.org/project/sbf-parser/>
- 参考：仓内 `mosaic-X5 Firmware v4.14.10.1 Reference Guide-2.pdf`
- 兄弟：[haslib](./haslib.md) · [ismr-downloader](./ismr-downloader.md) · [pyubx2](./pyubx2.md) · [cssrlib](./cssrlib.md) · [data-access](../data-access.md)
