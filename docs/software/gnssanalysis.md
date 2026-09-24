# gnssanalysis · GA SP3/CLK/Bias-SINEX 产品工具箱操作手册

目录：[`PROJECTS.json` → `gnssanalysis`](../../PROJECTS.json) · 上游 <https://github.com/GeoscienceAustralia/gnssanalysis> · PyPI **`gnssanalysis 0.0.60`** · tag **`0.0.60`=`d0c3642`**（main tip **`95116fd`** / **0.0.61.dev1** 未发 PyPI）· **Apache-2.0** · ★**43** · Python 3 · 本机验证（2026-09-24 07:21–07:23 EDT；**质检复跑 07:29 EDT**：`orbq` G01 3D_RMS=**0.06236**/AVG 3D=**0.01553**；`clkq` G01 RMS=**0.6795** m；`igs_merged.sp3` **474205** B/sha₁₂=`ef2d95ceb516`；`pytest` **32 passed**）：`pip install gnssanalysis`→**0.0.60**；CLI `diffutil`/`orbq`/`clkq`/`sp3merge`/`gnss-filename`/`snxmap`/`log2snx`/`trace2mongo`；仓内 fixture + clkcomb `example/products` 真 I/O；`pytest tests/test_clk.py tests/test_sp3.py` **32 passed**；**未臆造** 新产品日 SP3/CLK/Bias 数

> 岗位：Geoscience Australia 开源 **Python 产品 I/O + 比较/合并 CLI**（SINEX / SP3 / CLK / IONEX / BSX·BIA / ERP / RINEX / TROP + Ginan 专有 TRACE 等）。冲突时：**上游 README / `--help` / 源码 > 本文**。  
> 多 AC 钟差合成 → [clkcomb.md](./clkcomb.md)；GFZ 综合登记墙 → [spocc.md](./spocc.md)；码 OSB 网解 → [gkit-bias.md](./gkit-bias.md)/[mcosb.md](./mcosb.md)；Rust SP3 库 → [sp3.md](./sp3.md)；产品下载门禁 → [data-access.md](../data-access.md)。**库+CLI ≠ POD/PPP 引擎；≠ 实时 SSR 解码** → [great-podflt.md](./great-podflt.md)/[rt-clk-service.md](./rt-clk-service.md)/[ginan.md](./ginan.md)。

## 1. 用途与边界

**做：**

- **库**：`gnssanalysis.gn_io.sp3` / `clk` / `bia` / `sinex` / `ionex` / `rinex` / … 读写与辅助变换
- **CLI**：`diffutil`（按扩展名自动选 `sp3`/`clk`/…）、`orbq`（双 SP3 RAC/XYZ RMS）、`clkq`（双 CLK 统计，单位 **m**）、`sp3merge`（多 SP3 拼接，可选灌 CLK）、`gnss-filename`（IGS 长名推断）、`snxmap`（SINEX 站网 HTML）、`log2snx`、`trace2mongo`
- 压缩：`.gz` / `.Z`（LZW）路径多数可直接喂 CLI

**不做：**

- **不是** 多 AC 加权综合引擎 → [clkcomb.md](./clkcomb.md)/[spocc.md](./spocc.md)
- **不是** UPD/IFCB/OSB **估计器** → [great-upd.md](./great-upd.md)/[great-ifcb.md](./great-ifcb.md)/[gkit-bias.md](./gkit-bias.md)/[mcosb.md](./mcosb.md)
- **不是** 精密定轨 / 实时 SSR → [great-podflt.md](./great-podflt.md)/[rt-clk-service.md](./rt-clk-service.md)
- **不** 自带 Earthdata；本手册**未**跑 `gn_download` 拉新日产品

一句话：**GA 官方产品读写与差分质检箱**；接到「下载产品 → 对齐/合并/比差 → PPP」链的中段。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** gnssanalysis | pip 库 + 多 CLI | `pip show gnssanalysis`；`orbq --help` |
| [sp3.md](./sp3.md) | Rust 纯库 | crates `sp3`；无 `orbq` |
| [gnsstools.md](./gnsstools.md) | 轻量 Python SP3/OBS | 无 `diffutil`/`clkq` |
| [clkcomb.md](./clkcomb.md) | 多 AC 合成 CLI | `./bin/clkcomb comb.ini` |
| Ginan | 同机构 PPP/POD | `pea`；本包可读其 TRACE/PEA |

## 2. 安装

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -U pip
pip install gnssanalysis
python -c "import gnssanalysis; print(gnssanalysis.__version__)"
# → 0.0.60
which diffutil orbq clkq sp3merge gnss-filename
```

| 组件 | 本机 |
| --- | --- |
| Python | **3.13.5**（GCC 14.2.0） |
| PyPI | **0.0.60**（依赖含 `click`/`pandas`/`hatanaka`/`plotly`/`boto3` 等） |
| 源码对照 | clone tip **`95116fd`**；发版 tag **`d0c3642`** |

## 3. 端到端（本机真跑）（质检复跑 2026-09-24 07:29 EDT）

数据：① 包内 `tests/test_datasets/*_test_data.py` 抽出的短 fixture；② [clkcomb](./clkcomb.md) 仓 `example/products/`（`igs20863`/`cod20863` SP3+CLK）；③ [mcosb](./mcosb.md) 样例 `ECU0MGXFIN_20240180000_01D_01D_OSB.BIA`。

### 3.1 `diffutil` 同文件自比

```bash
diffutil -i igs_bench.sp3 igs_bench.sp3
# INFO … invoking 'sp3' command based on the extension …
# INFO::diffutil [OK] estimates diffs within the extracted STDs
# INFO::diffutil [ALL OK]
# EXIT 0
```

无 `-i` → click 报缺参，exit **2**。也可显式：`diffutil -i a.sp3 b.sp3 sp3`。

### 3.2 `orbq`：IGS vs COD 日轨道（clkcomb 样例）

```bash
orbq -i igs20863.sp3 cod20863.sp3
# G01  R_RMS=0.03814  A_RMS=0.04756  C_RMS=0.01296  3D_RMS=0.06236
# （星座摘要 --satellite false）
# AVG  R=0.00865  A=0.00971  C=0.00749  3D_RMS=0.01553
# RMS  R=0.01047  A=0.0122   C=0.00778  3D_RMS=0.01787
# EXIT 0
```

`.SP3.gz` 可直读：同文件自比 AVG/RMS 全 **0.0**（本机 `GRG0MGXFIN_20201770000_…ORB.SP3.gz`）。

### 3.3 `clkq`：钟差差（单位 m）

**Fixture**（包内截断 IGS vs GFZ rapid）：

```bash
clkq -i igs_rapid.clk gfz_rapid.clk
# G01  AVG=-0.6795  STD=0.0075  RMS=0.6795
# GNSS G  AVG=-0.6905  STD=0.0387  RMS=0.6915
```

**clkcomb 全日**（`igs20863.clk` vs `cod20863.clk`）：

```text
G01  AVG=8.1336  STD=0.1779  RMS=8.1355
GNSS G  AVG=8.0811  STD=0.1666  RMS=8.0829
```

（未做额外 `--norm`；数量级含参考钟尺度，**对比用相对差**，勿当绝对秒。）

### 3.4 `sp3merge`：两日拼一日文件

**必须** 重复 `-s`（`multiple=True`）；空格并列第二路径 → `Got unexpected extra argument` exit **2**。

```bash
sp3merge -s igs20863.sp3 -s igs20864.sp3 -o igs_merged.sp3
# EXIT 0；写出 #dP… N_EPOCHS=192（由 c→d 写出版本告警）
# 474205 B / sha₁₂=ef2d95ceb516 / epochs=192 / SV=32 / EOF×1
```

### 3.5 `gnss-filename`

```bash
gnss-filename igs20863.sp3 igs20863.clk
# IGS0OPSFIN_20200010000_00U_15M_ORB.SP3
# IGS0OPSFIN_20200010000_01D_30S_CLK.CLK
```

短名 `igs20863.sp3` 会 WARN「Failed to get timespan from filename」，长名里 `00U` 等字段可能不准——以文件内容为准。

### 3.6 Python API

```python
from gnssanalysis.gn_io import sp3, clk, bia
df = sp3.read_sp3("igs20863.sp3")   # shape (3072, 12)；index J2000×PRN；96 历元×32 星
# G01 首历元 EST X/Y/Z/CLK = 9888.347661, -19617.63715, -14892.695413, -247.874423
# 文件 253150 B / sha₁₂=e46f1547082c
cdf = clk.read_clk("igs20863.clk")  # (161861, 2)；G01 2880 行；首 EST=-2.478744e-04 s
bdf = bia.read_bia("ECU0MGXFIN_20240180000_01D_01D_OSB.BIA")
# 641 行 OSB；G01 C1C VAL=9.8409 ns（71071 B / sha₁₂=1906d7287261）
```

写出：`sp3.write_sp3` / `gen_sp3_header`+`gen_sp3_content`（合并见 `sp3.sp3merge`）。

### 3.7 单测冒烟

```bash
git clone --depth 1 https://github.com/GeoscienceAustralia/gnssanalysis.git
cd gnssanalysis && pip install -e . && pytest tests/test_clk.py tests/test_sp3.py -q
# 32 passed in ~2.6 s（本机；另有 NumPy timedelta DeprecationWarning）
```

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | `.sp3` / `.SP3` / `.gz` / `.Z` | `orbq`/`diffutil`/`sp3merge`/`read_sp3` |
| 入 | `.clk` / `.CLK` | `clkq`/`diffutil clk`/`read_clk` |
| 入 | `.bia` / `.bsx` | **库** `bia.read_bia`（CLI 无独立 bias 差分；`clkq -b` 可挂 BIA） |
| 入 | `.snx` / `.ssc` | `snxmap`、`diffutil sinex` |
| 出 | 合并 SP3 | `sp3merge -o` |
| 出 | 表 | `orbq`/`clkq` 默认 TSV；`--format json` |
| 出 | HTML | `snxmap -o` |

## 5. 参数（高频）

| 工具 | 关键选项 |
| --- | --- |
| `diffutil` | `-i f1 f2`（恰 2 个）；子命令 `sp3`/`clk`/`sinex`/`ionex`/…；`--passthrough`；`-a/--atol`；`-p/--plot` |
| `orbq` | `-i a b`；`-h ecf\|eci` Helmert；`-r 'G18'` 拒星；`--satellite/--constellation` |
| `clkq` | `-i a b`；`-b bia1 bia2`；`-n/--norm`；`-r`；`-p` 出图路径 |
| `sp3merge` | **`-s path` 可重复**；`-c` CLK；`-o`；`--nodata-to-nan` |
| `gnss-filename` | `--default`/`--override` PROPERTY VALUE；`-c` 打印旧名 |

## 6. 接到哪步

```text
[data-access] 拉 SP3/CLK/BIA
    → gnssanalysis（本稿）：读/比/拼/长名
    → 多 AC 合成 [clkcomb] / 登记综合 [spocc]
    → 偏差估计 [gkit-bias]/[mcosb] / UPD·IFCB [great-upd]/[great-ifcb]
    → PPP/POD [pride-pppar]/[ginan]/[great-pvt]/[great-podflt]
```

电离层链：产品对齐后仍走 TEC/GIM 教程；本工具**不**产 TEC。

## 7. 坑（≥8）

1. **`sp3merge -s a b` 非法**：须 `-s a -s b`；并列路径 → exit **2** `unexpected extra argument`。
2. **无 `-i`/`-s`**：`orbq`/`clkq`/`sp3merge`/`diffutil` 均 exit **2**（click）。
3. **非 IGS 长名**：`igs_bench.sp3` 等触发 filename regex WARN + timespan 失败；内容仍可读。
4. **SP3-c 读入**：`Reading an older SP3 file version 'c'`；`sp3merge` 写出改为 **d**。
5. **`clkq` 单位是米**（帮助原文），不是秒；与 `read_clk` 的秒估计勿混。
6. **`compare_clk`/`sisre` 弃用警告**：CLI 仍可用；新代码应跟 `diff_clk` / `calculate_sisre`。
7. **缺 STD 时**：`tol can not be None if STD info is missing, skipping`——`diffutil` 仍可能 `[ALL OK]`，勿当严格 σ 检验。
8. **立方样条**：有 nodata 且未开 offline-sat-removal 时 WARN，可能崩插值。
9. **`DataFrame.head()` + `attrs`**：部分环境下打印 MultiIndex SP3 帧会因 `attrs` 比较抛 `ValueError`；用 `iloc`/列选择，勿依赖 `repr`。
10. **PyPI ≠ main**：装 **0.0.60**；main **0.0.61.dev1** 仅源码。
11. **`trace2mongo`/`log2snx`**：依赖 Mongo / 站 log 树与 rclone 镜像；本手册未冒烟落库。
12. **Bias CLI 弱**：完整 OSB 表用 `bia.read_bia`；估计仍看 [gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md)。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| Python 读 SP3/CLK/BIA + 官方差分 CLI | **gnssanalysis（本文）** |
| Rust 仅 SP3 解析/插值 | [sp3.md](./sp3.md) |
| 多 AC 加权综合 CLK | [clkcomb.md](./clkcomb.md) |
| GFZ VCE 综合（登记） | [spocc.md](./spocc.md) |
| 估 OSB/UPD/IFCB | [mcosb.md](./mcosb.md)/[gkit-bias.md](./gkit-bias.md)/[great-upd.md](./great-upd.md) |
| 实时 SSR 钟轨 | [rt-clk-service.md](./rt-clk-service.md) |
| 下载门禁说明 | [data-access.md](../data-access.md) |

**下一优先（同族）：** **GREAT-MSF**（武大 GREAT PPP/RTK+INS 融合；★~150；GREAT 族尚缺手册；勿抢 `cggtts`/`rinex2bin`/`viresclient` WIP；勿建 gnssrefl/mpsim）。
