# hatanaka · Python Hatanaka CRX↔RNX 操作手册

目录：[`PROJECTS.json` → `hatanaka`](../../PROJECTS.json) · 上游 <https://github.com/valgur/hatanaka> · PyPI `hatanaka` · 捆绑 GSI RNXCMP（本机 **4.1.0**）· MIT（捆绑二进制另循 GSI 条款，须引用 Hatanaka 2008）· 本机验证 **hatanaka 2.8.1**（2026-09-24 ET）：`rinex-decompress` / `rinex-compress` + API 对上游 `sample.crx` 实跑；与 [georinex](./georinex.md) 1.16.2 联读 · **质检复跑**（2026-09-26 01:04 EDT，新 venv Python 3.13.5，PyPI 最新仍 **2.8.1**/捆 **4.1.0**，georinex 1.16.2 + xarray 2026.7.0）：§3.1–3.5 全部逐字复现（`BYTE_MATCH_GOLDEN_RNX=yes`、1346/1228 B、`.crx.gz` 与 golden 一致、`plain.crx.gz` **534** B 魔数 `1f 8b`、`plain2.crx` 头 `ver.4.1.0`+当前 **UTC** 时刻且观测体与 golden 逐行一致、`demo.10d`、API 四行、georinex `L1C G07 133174968.818`）；坑 7/8/10 与伪 CRX `ValueError`（exit **1**）复现；修坑 6：NAV 仅 `-c none` 报 already compressed，默认直接出 `.gz`

> 岗位：在 **Python / pip 环境**把 Compact RINEX（`.crx` / `.##d`）与明文 RINEX（`.rnx` / `.##o`）互转，并可叠 gzip/bz2/Z。冲突时：**本机 `rinex-decompress -h` / 上游 README > 本文**。  
> **官方 GSI 二进制（RNXCMP 4.2.0、RINEX 4.02 / CRINEX 3.1）→ [rnxcmp.md](./rnxcmp.md)**，本文不重复官方安装与 `RNX2CRX`/`CRX2RNX` 旗标细则。

## 1. 用途与边界

**做：**

- CLI：`rinex-decompress` / `rinex-compress`（可叠加 `.gz` / `.bz2` / `.Z` / `.zip`）
- API：`crx2rnx` / `rnx2crx` / `decompress` / `compress` / `*_on_disk`
- 短名 `.##o`↔`.##d`、长名 `.rnx`↔`.crx` 的路径推导
- 为 [georinex](./georinex.md) 提供 `.crx` 读取依赖（`pip install hatanaka`）

**不做：**

- **不是** GSI 官方发行渠道 → [rnxcmp](./rnxcmp.md)（本机捆 4.1.0，**落后**官网 4.2.0）
- **不是** 读进 xarray / 算 TEC / QC / 拼接 → [georinex](./georinex.md) / [pytecgg](./pytecgg.md)（viventriglia）/ [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)
- **不是** 通用归档器：只服务 **观测** CompactRINEX；NAV 头无 `OBSERVATION DATA` 时跳过 Hatanaka——`-c none` 报 *already compressed*，默认只做 gzip
- **sh-gim** 边界短说明见 [sh-gim](./sh-gim.md)，本文不扩写

一句话：hatanaka = **Python 便利封装 + 捆绑 RNXCMP**；钉版本 / RINEX 4.02 用 [rnxcmp](./rnxcmp.md)。

| 术语 | 含义 |
| --- | --- |
| Compact RINEX / CRINEX | Hatanaka 差分压缩观测格式 |
| `rinex-decompress` / `rinex-compress` | 本包装的高层 CLI（推荐） |
| `crx2rnx` / `rnx2crx` | 同名入口，指向 **捆绑** 二进制（≠ 你 PATH 里的 GSI 4.2.0） |
| `rnxcmp_version` | 捆绑 RNXCMP 版本字符串（本机 `4.1.0`） |

## 2. 安装

```bash
cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install hatanaka
# 与 georinex 联用时：
python -m pip install georinex hatanaka netCDF4 xarray numpy

python -c "import hatanaka; print(hatanaka.__version__, hatanaka.rnxcmp_version)"
# 本机：2.8.1 4.1.0

rinex-decompress --version
rinex-decompress --rnxcmp-version
rinex-compress -h | head -n 15
```

**本机：**

```text
2.8.1
4.1.0
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python 过旧 | 换 3.8+（本机 3.13） |
| `ModuleNotFoundError: hatanaka` | 错 venv | `which python`；重装进当前环境 |
| 要 RINEX 4.02 / CRINEX 3.1 | 捆绑 4.1.0 不够 | 改用 [rnxcmp](./rnxcmp.md) GSI **4.2.0** |
| 系统已有 `CRX2RNX` 但脚本仍调捆版 | console_scripts 优先 venv | `which crx2rnx`；官方流程显式调 GSI 路径 |

## 3. 端到端：公开 `sample.crx` → RNX → 再压缩（本机真跑）

样本：上游测试文件（亦随 wheel 分发）。

```bash
mkdir -p ~/iono_ops/hatanaka-demo/{data,e2e} && cd ~/iono_ops/hatanaka-demo
curl -fsSL -o data/sample.crx \
  https://raw.githubusercontent.com/valgur/hatanaka/master/hatanaka/test/data/sample.crx
curl -fsSL -o data/sample.rnx \
  https://raw.githubusercontent.com/valgur/hatanaka/master/hatanaka/test/data/sample.rnx
# 可选：.crx.gz
curl -fsSL -o data/sample.crx.gz \
  https://raw.githubusercontent.com/valgur/hatanaka/master/hatanaka/test/data/sample.crx.gz
head -n 2 data/sample.crx
# 期望：首行含 COMPACT RINEX FORMAT；绝不是 <!DOCTYPE html
```

### 3.1 解压 `.crx` → `.rnx`

```bash
cp data/sample.crx e2e/sample.crx
rm -f e2e/sample.rnx
rinex-decompress e2e/sample.crx
# 真实 stdout：Created e2e/sample.rnx
cmp -s e2e/sample.rnx data/sample.rnx && echo BYTE_MATCH_GOLDEN_RNX=yes
wc -c e2e/sample.crx e2e/sample.rnx
head -n 2 e2e/sample.rnx
```

**本机：**

```text
Created e2e/sample.rnx
BYTE_MATCH_GOLDEN_RNX=yes
1346 e2e/sample.crx
1228 e2e/sample.rnx
     3.01           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE
G    7 L1C L2P C1P C2P C1C S1P S2P                          SYS / # / OBS TYPES
```

已是明文时：

```text
e2e/sample.rnx is already decompressed
```

（exit 0）

### 3.2 解压 `.crx.gz`（Hatanaka + gzip 一步）

```bash
cp data/sample.crx.gz e2e/fromgz.crx.gz
rinex-decompress e2e/fromgz.crx.gz
# Created e2e/fromgz.rnx ；本机与 golden .rnx 字节一致
```

### 3.3 压缩：默认再 gzip / 仅 CRX

```bash
cp data/sample.rnx e2e/plain.rnx
rinex-compress e2e/plain.rnx
# Created e2e/plain.crx.gz （本机 534 B；magic 1f 8b）

cp data/sample.rnx e2e/plain2.rnx
rinex-compress -c none e2e/plain2.rnx
# Created e2e/plain2.crx
head -n 2 e2e/plain2.crx
```

**本机 `plain2.crx` 头：**

```text
3.0                 COMPACT RINEX FORMAT                    CRINEX VERS   / TYPE
RNX2CRX ver.4.1.0                       24-Sep-26 07:56     CRINEX PROG / DATE
```

与 golden `sample.crx` **不必**整文件相等：`CRINEX PROG / DATE` 会写成捆绑 **4.1.0** + 当前时刻（golden 为 `ver.4.0.8` / `08-Apr-21`）。观测体应一致。

短名：`demo.10o` → `rinex-compress -c none` → `demo.10d`（本机确认）。

### 3.4 Python API

```bash
python - <<'PY'
from pathlib import Path
import hatanaka
from hatanaka import crx2rnx, rnx2crx, decompress, compress

crx = Path("data/sample.crx").read_bytes()
rnx = Path("data/sample.rnx").read_bytes()
print(hatanaka.__version__, hatanaka.rnxcmp_version)
out = crx2rnx(crx)
print("crx2rnx", len(out), "eq_golden", out == rnx)
back = rnx2crx(out)
print("rnx2crx", len(back), "line0", back.decode().splitlines()[0][:40])
print("decompress_gz", len(decompress(Path("data/sample.crx.gz").read_bytes())))
print("compress_gz_magic", compress(rnx, compression="gz")[:2])
PY
```

**本机：** `2.8.1 4.1.0`；`crx2rnx 1228 eq_golden True`；`decompress_gz 1228`；`compress_gz_magic b'\x1f\x8b'`。

| API / 旗标 | 作用 |
| --- | --- |
| `rinex-decompress` `[files]` | 解 Hatanaka 与/或 gzip/bz2/Z/zip |
| `-s` / `--skip-strange-epochs` |  Salvage 异常历元（对应官方 `-s`） |
| `-d` / `--delete` | 成功后删输入（本机：`Deleted e2e/delme.crx`） |
| `rinex-compress -c {gz,bz2,Z,none}` | 额外常规压缩；默认 **gz** |
| `-e N` / `--reinit-every-nth` | 每 N 历元重置差分（对应官方 `-e`） |
| `--version` / `--rnxcmp-version` | 包装版本 / 捆绑 RNXCMP |
| `crx2rnx(content)` / `rnx2crx(content)` | 纯字节↔字节 |
| `decompress_on_disk(path)` / `compress_on_disk(path)` | 写旁路文件并返回 `Path` |

退出码：`0` 成功 · `1` 错误 · `2` 警告（与 RNXCMP 一致）。

### 3.5 接到 georinex

```bash
python - <<'PY'
import georinex as gr
obs = gr.load("data/sample.crx")   # 内部走 hatanaka
print("georinex", getattr(gr, "__version__", "?"), dict(obs.sizes))
print("vars", list(obs.data_vars))
print("L1C G07", float(obs["L1C"].sel(sv="G07").isel(time=0)))
PY
python -m georinex.time data/sample.crx
```

**本机（georinex 1.16.2）：**

```text
georinex 1.16.2 {'time': 1, 'sv': 8}
vars ['L1C', 'L2P', 'C1P', 'C2P', 'C1C', 'S1P', 'S2P', 'S1C']
L1C G07 133174968.818
filename: start, stop, number of times, interval
sample.crx: 2010-03-05T00:00:30 2010-03-05T00:00:30 1
['2010-03-05T00:00:30.000']
```

（可能出现 xarray `FutureWarning` / 空切片 `Mean of empty slice`——与 hatanaka 无关，见 [georinex](./georinex.md) 坑表。）

## 4. 输入 / 输出速查

| 输入 | 输出（常见） |
| --- | --- |
| `*.crx` / `*.##d` | `*.rnx` / `*.##o` |
| `*.crx.gz` / `*.##d.gz` | 明文 OBS |
| `*.rnx` / `*.##o` + `-c none` | `*.crx` / `*.##d` |
| 同上 + 默认 | `*.crx.gz` / `*.##d.gz` |

路径含糊（如裸 `.rnx` 且未读内容）时，`get_compressed_path(..., is_obs=True)` 需显式 `is_obs`。

## 5. 接到哪步

- IGS/CDDIS 下载 `.crx.gz` → **本文**或 [rnxcmp](./rnxcmp.md) → [georinex](./georinex.md) 探活 → [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)（viventriglia）
- 台网入库压缩策略、官方可引用流程 → [rnxcmp](./rnxcmp.md)；编排 → [autorino](./autorino.md) / [pinot](./pinot.md)
- 数据入口 → [data-access](../data-access.md)

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ModuleNotFoundError: hatanaka`（georinex 读 `.crx`） | 未装绑定 | `pip install hatanaka` |
| 2 | RINEX 4.02 压坏 / 旧工具拒读 CRINEX 3.1 | 捆绑 **4.1.0** | 换 [rnxcmp](./rnxcmp.md) **4.2.0** |
| 3 | 重压后 `cmp` ≠ 原 `.crx` | `CRINEX PROG / DATE` 版本与时间戳变了 | 比观测体或只验 `crx2rnx` 往返 |
| 4 | `ValueError: file is too short to be a valid RINEX file` | 伪 `.crx` / HTML | `head` 查 `COMPACT RINEX`；重下 |
| 5 | `... is already decompressed` | 输入已是明文 | 正常 skip；勿当失败 |
| 6 | NAV 上 `rinex-compress -c none` 显示 `... is already compressed`、不产出新文件 | 头无 `OBSERVATION DATA`，跳过 CRX | 正常；默认 `-c gz` 时 NAV 只 gzip：`Created nav.rnx.gz` / `brdc0010.20n.gz`（本机） |
| 7 | `-v` 报 `unrecognized arguments` | 本 CLI **无** `-v` | 用 `--version` / `--rnxcmp-version` |
| 8 | `-d` 后源 `.crx` 消失 | 设计如此 | 流水线先备份；或去掉 `-d` |
| 9 | `which crx2rnx` 指向 venv 捆版，却以为是 GSI 4.2.0 | 同名入口 | `crx2rnx -h` 看 version；官方流程用 [rnxcmp](./rnxcmp.md) 绝对路径 |
| 10 | `get_compressed_path('a.rnx')` ValueError | 未指定是否观测 | `is_obs=True` 或先读文件头 |
| 11 | `HatanakaException: ... truncated ...` | 截断/坏 CRX | 换源；salvage 试 `-s`（后续历元仍可能废） |
| 12 | 只解压到内存却期望落盘 | `crx2rnx` 返回 bytes | 用 `decompress_on_disk` / CLI |

## 7. 选型（一行）

| 需求 | 选 |
| --- | --- |
| pip / 脚本 / georinex 依赖 | **本文 hatanaka** |
| 官方可引用、RINEX 4.02、钉 GSI 版 | **[rnxcmp](./rnxcmp.md)** |
| 读进 xarray | [georinex](./georinex.md)（先装 hatanaka） |
| 拼日/抽稀 | [gfzrnx](./gfzrnx.md) |

## 8. 相关

[rnxcmp](./rnxcmp.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [pinot](./pinot.md) · [autorino](./autorino.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · [README](./README.md)
