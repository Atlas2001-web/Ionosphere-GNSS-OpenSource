# NavDecoder · PPP-B2b + Galileo HAS 电文解码操作手册

目录：[`PROJECTS.json` → `NavDecoder`](../../PROJECTS.json) · 上游 <https://github.com/NavSesne/NavDecoder>（org 拼写 **NavSesne**）· tip **`7947333`** · **无 SPDX / 无 LICENSE**（商用先联系 `lwzhao@nuist.edu.cn`）· 依赖 **Python3 + numpy + bitstruct + tqdm + galois + python-dateutil**；Septentrio B2b 另需仓内 **`libldpc.so_lx`（Linux ELF）** · 本机验证：截短 SEPT DOY135/2024 样例 → HAS 页解码 **801**×`data collected` + log **1.1 MB**（含轨道改正表）；B2b → **`.ssr` 532** 行 CLOCK/ORBIT + **`.log` 7346** 行 + stub 导航下仍写出 `.sp3` 头 · 2026-09-24 05:03 EDT

> 岗位：把接收机落盘的 **北斗 PPP-B2b** / **Galileo HAS** 原始电文解成可检视的改正日志，并可导出 **BNC 风格 SSR** 与 **SP3/CLK**（有真实广播星历时）。冲突时：**仓内 `ReadMe.md` / 脚本顶栏配置 > 本文**。嵌 RTKLIB 的 B2b C 库 → [b2blib](./b2blib.md)；Galileo HAS→RTCM/IGS → [haslib](./haslib.md)；Python Compact SSR 教学 → [cssrlib](./cssrlib.md)；QZSS MADOCA → [madocalib](./madocalib.md)。

## 1. 用途与边界

**做：**

- Septentrio **`GALRawCNAV`** 文本 → `decode_HAS_sept.py`（Reed-Solomon 组页 + HAS Compact SSR）
- Septentrio **`BDSRawB2b`** 文本 → `decode_B2B_sept.py`（LDPC + B2b MT）
- Unicore **`PPPB2bInfo`** ASCII → `decode_B2B_UM982.py`（明文改正，无 LDPC）
- 改正写出 **`.ssr`（BNC universal）**、**`.sp3` / 评估日志**；仓内 `download/` 拉 BRDC / MGEX 轨道钟
- 样例：`test_data/SEPT1350.24__SBF_*.txt.7z`（DOY **135** = 2024-05-14）

**不做：**

- **不是** 完整 PPP 引擎——解算接 [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [cssrlib](./cssrlib.md) / [b2blib](./b2blib.md)
- **不是** 官方 HASlib CLI（SBF→RTCM）→ [haslib](./haslib.md)；本仓主责 **页/改正解析与 SSR/SP3 导出**
- **不是** QZSS CLAS/MADOCA → [claslib](./claslib.md) / [madocalib](./madocalib.md)
- **不是** PyPI 包：无 `pip install navdecoder`；脚本级工具箱
- 百度网盘归档 SSR/RAW 需自取；许可空白 → 科研可试，产品嵌入前联系作者

一句话：NavDecoder = **多厂商原始流 → B2b/HAS 改正（日志 + SSR/SP3）的 Python 对照箱**。

| 术语 | 含义 |
| --- | --- |
| `GALRawCNAV` / `BDSRawB2b` | Septentrio 导出的逗号分隔明文块（非裸 SBF） |
| HAS page / mid / ms / pid | Galileo HAS 页：消息 ID、页数、页号；RS 组齐后再 `decode_cssr` |
| `libldpc.so_lx` | Linux x86_64 LDPC；Windows 预置 `libldpc.so`（实为非 ELF） |
| BNC `.ssr` | `> CLOCK` / `> ORBIT … B2B` 行；可喂 BNC / 自写读取 |
| stub NAV | 仅头、无星历的 RINEX NAV；能跑页解码，**不能**填满 SP3 卫星行 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/NavSesne/NavDecoder.git
cd NavDecoder && git rev-parse --short HEAD   # 本机 7947333

python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install numpy bitstruct tqdm galois python-dateutil py7zr
python - <<'PY'
import py7zr, os
os.chdir('test_data')
for z in ('SEPT1350.24__SBF_GALRawCNAV.txt.7z','SEPT1350.24__SBF_BDSRawB2b.txt.7z'):
    with py7zr.SevenZipFile(z) as a: a.extractall()
print('ok')
PY

readelf -h B2b_HAS_decoder/libldpc.so_lx | head -5
# 期望：Machine: Advanced Micro Devices X86-64
```

脚本顶栏改三处：`start_date`、`process_days`、路径模板（已相对 `test_data/`）。

## 3. 端到端 A：截短 HAS 页解码（本机真跑）

样例全日约 **62 万** 行 / **113 MB**。冒烟可截前 **5 万** 行；**完整 SP3** 仍要当日 ±1 天真实 BRDC（见坑）。

```bash
cd ~/iono_ops/NavDecoder
cp test_data/SEPT1350.24__SBF_GALRawCNAV.txt test_data/SEPT1350.24__SBF_GALRawCNAV.txt.fullbak
head -50000 test_data/SEPT1350.24__SBF_GALRawCNAV.txt.fullbak \
  > test_data/SEPT1350.24__SBF_GALRawCNAV.txt

mkdir -p test_data/eph
for doy in 134 135 136; do
  printf '%s\n' '     3.04           N: GNSS NAV DATA    M: MIXED            RINEX VERSION / TYPE' \
    '                                                            END OF HEADER' \
    > "test_data/eph/BRDC00IGS_R_2024${doy}0000_01D_MN.rnx"
done

python decode_HAS_sept.py
# stub NAV 时 write_sp3 可能 IndexError——页解码已完成
```

**本机结果（tip `7947333`，截短 50 k 行，2026-09-24 05:03 EDT）：**

```text
=============Saving sp3/ssr/log to dir: …/test_data/SEPT2024135_HAS
… data collected mid=21 ms=2 tow=183718 …
100%|██████████| 6690/6690  （约 29 s）
stdout 中 data collected 约 801 次
SEPT2024135_HAS.log ≈ 1.1 MB / 48288 行
  首条：##### Galileo HAS SSR: TOH 117 … mask_id=21
  随后 SatID / IODE / Radial·Along·Cross[m] 表（G/E 改正可见）
SEPT2024135_HAS.sp3  0 B（stub NAV → write_sp3 IndexError）
```

| 输入 | 说明 |
| --- | --- |
| `SEPT1350.24__SBF_GALRawCNAV.txt` | Septentrio HAS 页导出；列 tow,wn,prn,validity,nav hex |
| `test_data/eph/BRDC00IGS_R_2024ddd0000_01D_MN.rnx` | 前后日共 3 份；**真实星历**才有非空 SP3 |
| RS 生成矩阵 | `B2b_HAS_decoder/Galileo-HAS-SIS-ICD_1.0_Annex_B_….txt` |

| 输出 | 含义 |
| --- | --- |
| `SEPT{yyyy}{ddd}_HAS.log` | 页组装 + CSSR 展开（轨道/钟/码偏） |
| `…_HAS.ssr` / `.sp3` | BNC SSR / 精密轨道钟（依赖 NAV） |

## 4. 端到端 B：截短 PPP-B2b（本机真跑）

```bash
cd ~/iono_ops/NavDecoder
cp test_data/SEPT1350.24__SBF_BDSRawB2b.txt test_data/SEPT1350.24__SBF_BDSRawB2b.txt.FULL
head -20000 test_data/SEPT1350.24__SBF_BDSRawB2b.txt.FULL \
  > test_data/SEPT1350.24__SBF_BDSRawB2b.txt

for doy in 134 135 136; do
  printf '%s\n' '     4.00           N: GNSS NAV DATA    M: MIXED            RINEX VERSION / TYPE' \
    '                                                            END OF HEADER' \
    > "test_data/eph/BRD400DLR_S_2024${doy}0000_01D_MN.rnx"
done

python decode_B2B_sept.py
# 跑完后：mv …FULL …BDSRawB2b.txt
```

**本机结果（2 万行截短，同 tip）：**

```text
libldpc.so loaded successfully from: …/libldpc.so_lx
=============Saving …/SEPT2024135_B2b
SEPT2024135_B2b.log  7346 行（cssr_clk_sat C/G…；码偏表）
SEPT2024135_B2b.ssr   532 行  > CLOCK / > ORBIT … B2B
SEPT2024135_B2b.sp3   277 行  历元头齐全；stub NAV 时卫星 P 行可空
exit 0
```

Unicore：改跑 `decode_B2B_UM982.py`（ASCII `PPPB2bInfo`）；无 LDPC。

## 5. 关键配置 / 产物

| 项 | 作用 |
| --- | --- |
| `start_date` / `process_days` | 与文件名 DOY 对齐；错日 → `File not found` |
| `max_orbit_delay` / `max_clock_delay` | 改正时效门限（默认 300 s / 30 s） |
| `file_*_template` / `nav_file_template` / `corr_dir_template` | 输入与输出路径模板 |
| `down_NAV_data(...)` | 启动时尝试 WHU FTP 拉 BRDC；失败则用已有文件 |
| `.ssr` / `.sp3` / `.log` | 改正流 / 轨道钟 / 调试 |

## 6. 接到哪步

- HAS 页→RTCM/IGS 官方链 → [haslib](./haslib.md)；Python 多服务对照 → [cssrlib](./cssrlib.md)
- B2b 嵌入 RTKLIB PPP → [b2blib](./b2blib.md)；发表级 → [pride-pppar](./pride-pppar.md)
- QZSS → [claslib](./claslib.md) / [madocalib](./madocalib.md)
- 工作流 **D**：QC → 开放改正（本文 / [haslib](./haslib.md) / [b2blib](./b2blib.md) / [cssrlib](./cssrlib.md)）→ [pride-pppar](./pride-pppar.md)；数据 [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)

## 7. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ModuleNotFoundError: galois` | HAS RS 依赖未装 | `pip install galois bitstruct tqdm numpy python-dateutil` |
| 2 | `Failed to load libldpc` / B2b 无改正 | Linux 错用 Windows `libldpc.so` | 确认加载 `libldpc.so_lx`；`readelf -h` 须为 ELF64 |
| 3 | `File not found: SEPT…` | `start_date` 与文件名 DOY 不一致 | 样例固定 **2024-05-14** / DOY **135** |
| 4 | WHU FTP `RETR 425 Bad IP` | 数据连接被拒（常见于 NAT/共享出口） | 换镜像/Earthdata；或手动放入 `test_data/eph/` |
| 5 | `write_sp3` → `list index out of range` | NAV 无星历（stub/缺文件） | 放入真实 3 日 BRDC 后再跑；页解码 log 仍可用 |
| 6 | 全日跑数小时 / 内存涨 | 原始 txt 过大 `genfromtxt` | 先 `head` 截短验证；生产再全日 |
| 7 | 与 [haslib](./haslib.md) 字节对不上 | 输入形态不同（txt 页 vs SBF） | 同源接收机导出后再比；目标格式也不同（SSR/SP3 vs RTCM） |
| 8 | 当 CLAS/MADOCA 教程跑 | 星座/ICD 不同 | CLAS→[claslib](./claslib.md)；MADOCA→[madocalib](./madocalib.md) |
| 9 | `pip install NavDecoder` 失败 | 无包装 | `git clone` + venv；于仓根执行脚本 |
| 10 | Unicore 脚本读 Septentrio 文件 | 块格式不同 | Sept→`decode_B2B_sept.py`；UM→`decode_B2B_UM982.py` |
| 11 | 商用发货被问许可 | 仓内无 LICENSE | 联系作者邮件后再嵌入 |
| 12 | 期望 cm 级固定 PPP | 本工具只解码 | 改正接入 [b2blib](./b2blib.md)/[cssrlib](./cssrlib.md)/[pride-pppar](./pride-pppar.md) |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| Sept/Unicore 原始流 → B2b/HAS 日志+SSR/SP3 | **本文 NavDecoder** |
| Galileo HAS → RTCM/IGS SSR CLI | [haslib](./haslib.md) |
| B2b 嵌进 RTKLIB C PPP | [b2blib](./b2blib.md) |
| Python 多开放服务 PPP 教学 | [cssrlib](./cssrlib.md) |
| QZSS CLAS / MADOCA | [claslib](./claslib.md) / [madocalib](./madocalib.md) |

## 9. 相关

[b2blib](./b2blib.md) · [haslib](./haslib.md) · [cssrlib](./cssrlib.md) · [madocalib](./madocalib.md) · [claslib](./claslib.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [bnc](./bnc.md) · [data-access](../data-access.md) · [README](./README.md)

- 作者联系：`lwzhao@nuist.edu.cn` / `navsense_support@163.com`
- 样例日：2024-05-14（GPS week 2314）Septentrio 导出
