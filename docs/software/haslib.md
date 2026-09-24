# HASlib · Galileo HAS 解码（SBF/BINEX → SSR）操作手册

目录：[`PROJECTS.json` → `HASlib`](../../PROJECTS.json) · 上游 <https://github.com/nlsfi/HASlib> · 许可 **EUPL-1.2** · PyPI 包名 **`galileo_has_decoder` 1.0.2** · 本机验证：`Tests/galileo_ssr003.sbf` → RTCM SSR，`-x 3000 -v 1` 解出 **11** 条 HAS（2026-09-24 EDT）

> 岗位：把 E6 能力接收机录到的 **Galileo C/Nav 页**（SBF / BINEX；文件 / 串口 / TCP）收齐、解码成 HAS PPP 改正，再写成 **RTCM3 SSR** 或 **IGS SSR**（文件 / TCP / PPP Wizard）。冲突时：**本机 `python HAS_Converter.py -h` / 仓内 README > 本文**。

## 1. 用途与边界

**做：**

- 读 Septentrio **SBF** 或 **BINEX** 中的 Galileo C/Nav，拼页 → HAS 消息
- 输出 **RTCM3 SSR**（`outFormat=2`）或 **IGS SSR**（`=1`）；可落盘或 TCP（默认端口 **6947**）
- 库入口 `galileo_has_decoder.conv.HAS_Converter`；CLI 壳 `HAS_Converter.py`
- 仓内 `Tests/TestRecordings.zip`（FGI Otaniemi PolarX5）可回归

**不做：**

- **不是** PPP/PPP-RTK 解算引擎 → 改正交给 [cssrlib](./cssrlib.md) / [rtklib](./rtklib.md) / PPP Wizard
- **不是** 通用 NTRIP 拉流工具 → [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md)（可上游喂 TCP/文件）
- **不** 产 STEC/ROTI/GIM → [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md)
- Julia 包装 `HASlib.jl`、官方 `HASlibTestSuite` 另见 PROJECTS；主路径仍以 **nlsfi/HASlib** 为准
- 未做运行时认证：HAS SiS ICD 条款自核；作者声明非运营级

一句话：HASlib = **芬兰 NLS/FGI 的 Galileo HAS 解码器**（原始页 → SSR 字节流）。

| 术语 | 含义 |
| --- | --- |
| HAS / C/Nav | Galileo High Accuracy Service；E6-B 页拼成改正消息 |
| SBF / BINEX | Septentrio 二进制 / 通用二进制交换；本库两种输入 |
| RTCM3 SSR / IGS SSR | 输出状态空间改正封装；`SSR` 类内存用 **HAS 符号约定**，写出时由 output 类换算 |
| `modeIn` 1–6 | 文件 SBF/BINEX、串口 SBF/BINEX、TCP SBF/BINEX |
| `modeOut` 1–4 | TCP / 文件 / PPPWiz 文件 / PPPWiz 流 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/nlsfi/HASlib.git
cd HASlib
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip wheel
# setup.py 写 serial；实际要 pyserial。setuptools≥81 去掉 pkg_resources → 钉 <81
python -m pip install 'setuptools<81' numpy reedsolo galois pyserial
python setup.py bdist_wheel
python -m pip install dist/galileo_has_decoder-1.0.2-py3-none-any.whl
python -W ignore -c "import importlib.metadata as m; from galileo_has_decoder import conv; print(m.version('galileo_has_decoder'), conv.HAS_Converter)"
# 期望：1.0.2 <class '...HAS_Converter'>
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pkg_resources'` | setuptools 过新 | `pip install 'setuptools<81'` |
| `No module named 'serial'` | 装了错包名 `serial` | `pip install pyserial` |
| `galileo`/`reedsolo` 缺 | 未装依赖 | `pip install numpy reedsolo galois pyserial` |

## 3. 端到端：测试 SBF → RTCM SSR（本机真跑）

数据：`Tests/TestRecordings.zip` → `galileo_ssr003.sbf`（较小；`galileo_ssr000.sbf` ~52 MB 亦可）。摘要行要 **`-v ≥1`**。

### 3.1 解压 + CLI

```bash
cd ~/iono_ops/HASlib && source .venv/bin/activate
unzip -o Tests/TestRecordings.zip -d Tests
python -W ignore HAS_Converter.py \
  -s ./Tests/galileo_ssr003.sbf -t /tmp/haslib_rtcm.out -f RTCM -x 3000 -v 1
ls -la /tmp/haslib_rtcm.out
python - <<'PY'
from pathlib import Path
b = Path('/tmp/haslib_rtcm.out').read_bytes()
print('nbytes', len(b), 'n_D3_preamble', b.count(b'\xd3'), 'head', b[:8].hex())
PY
```

**本机 stdout / 结果（2026-09-24 EDT，`galileo_has_decoder` 1.0.2）：**

```text
--- Set up converter ---
Reading HAS messages from a SBF file and converting to RTCM 3.0 messages. Output will be written to a file named /tmp/haslib_rtcm.out.
...
Creating Orbit Message
Creating Code Bias Message
Creating Clock Message
...
Out of 3000 messages, 520 were C/Nav messages. 11 HAS messages have successfully been decoded and converted.

# ls / 校验
nbytes 9780 n_D3_preamble 32 head d302034213671890
```

| 输出字段 | 含义 |
| --- | --- |
| `Out of N messages` | 读入的导航块总数（含非 HAS） |
| `C/Nav messages` | 识别为 Galileo C/Nav 的块数（本机 520 / 3000） |
| `HAS messages … decoded` | 成功拼页并写出的 HAS 条数（本机 **11**） |
| `Creating Orbit/Code Bias/Clock` | 正在生成对应 SSR 子消息（`-v≥1`） |
| 文件头 `0xD3` | RTCM3 帧前导；本机 32 次 ≈ 多帧串联 |

IGS 格式同法：`-f IGS -t /tmp/haslib_igs.out`（本机同 `-x 3000` → **9800** bytes）。

### 3.2 库 API（等价）

```bash
python -W ignore - <<'PY'
from galileo_has_decoder.conv import HAS_Converter
c = HAS_Converter(
    source='./Tests/galileo_ssr003.sbf',
    target='/tmp/haslib_lib.out',
    outFormat=2,          # 2=RTCM3, 1=IGS；也可用 "RTCM"/"IGS"
    modeIn=1,             # 1=SBF 文件（.sbf 后缀可省略）
    modeOut=2,            # 2=文件
    mute=1,
)
c.convertX(1500, verbose=1)   # 或 convertAll(...)
print('done')
PY
```

### 3.3 旗标

| CLI / 参数 | 作用 |
| --- | --- |
| `-s` / `source` | 输入路径、串口名或 TCP 主机 |
| `-t` / `target` | 输出路径；纯数字/`localhost` 时默认当 TCP |
| `-f` / `outFormat` | `1`/`IGS` 或 `2`/`RTCM` |
| `-i` / `modeIn` | 1 SBF 文件 · 2 BINEX 文件 · 3/4 串口 · 5/6 TCP |
| `-o` / `modeOut` | 1 TCP · 2 文件 · 3 PPPWiz 文件 · 4 PPPWiz 流 |
| `-x` | 最多读 **N 条**导航消息（含非 C/Nav）；省略则 `convertAll` |
| `-v` | verbose；**≥1 才打印** `Out of … HAS …` 摘要 |
| `-p` | TCP 输出端口（默认 6947） |
| `-b` | 串口波特率（默认 115200） |
| `--skip` | 跳过文件开头比例（0–1） |
| `-m` / `--mute` | 抑制与 verbose 无关的设置横幅 |
| `convertX` 的 `compact`/`HRclk`/`lowerUDI` | SSR 打包细节（库级；CLI 未暴露） |

## 4. 接到哪步

- HAS 改正字节 → [cssrlib](./cssrlib.md) PPP/PPP-RTK 样例；或 [rtklib](./rtklib.md) SSR 链路
- 实时：接收机 SBF TCP/`-i 5` → 本工具 `-o 1` → 下游；NTRIP 编排见 [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md)
- 概念：教程 [06](../tutorials/06-iono-positioning.md)；数据入口 [data-access](../data-access.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `No module named 'pkg_resources'` | setuptools≥81 | `pip install 'setuptools<81'` |
| 2 | 无 `Out of … HAS …` 行，但文件有字节 | 默认 `verbose=0` 不打摘要 | 加 `-v 1` |
| 3 | `Mask not available, message discarded` | 缺掩码页，改正丢弃 | 正常；拉长 `-x` 或换 `galileo_ssr000.sbf` |
| 4 | `C/Nav` 很多但 HAS=0 | 页不齐 / 非运营模式数据 | 用仓内 Tests；升级到含 operational mode 的 ≥1.0.1 |
| 5 | 串口 `Source_Error` | 未设 `modeIn` 3/4 | `-i 3`（SBF）或 `-i 4`（BINEX）并设 `-b` |
| 6 | `No module named 'serial'` | 依赖名是 pyserial | `pip install pyserial` |
| 7 | 下游 PPP 改正符号反 | SSR 内存是 HAS 符号约定 | 用库自带 writer；自写转换对照 README 1.0.2 说明 |
| 8 | 当定位引擎用 | 本库只解码 | 接 [cssrlib](./cssrlib.md) / [rtklib](./rtklib.md) |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| SBF/BINEX → RTCM/IGS SSR | **本文 HASlib** |
| Python 开放 PPP + HAS 试验 | [cssrlib](./cssrlib.md) |
| CLI 事后 RTK/PPP | [rtklib](./rtklib.md) |
| NTRIP 拉流/小 caster | [pygnssutils](./pygnssutils.md) |

- HAS SiS ICD：<https://www.gsc-europa.eu/sites/default/files/sites/all/files/Galileo_HAS_SIS_ICD_v1.0.pdf>
- 论文（引用）：ION GNSS+ 2022 · 仓内 `galileo_has.pdf`
- 测试套件：<https://github.com/nlsfi/HASlibTestSuite>
- 兄弟：[cssrlib](./cssrlib.md) · [rtklib](./rtklib.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [pride-pppar](./pride-pppar.md) · [data-access](../data-access.md)
