# RNXCMP · Hatanaka Compact RINEX 操作手册

目录：[`PROJECTS.json` → `RNXCMP`](../../PROJECTS.json) · 官网 <https://terras.gsi.go.jp/ja/crx2rnx.html> · 许可 [LICENSE.txt](https://terras.gsi.go.jp/ja/crx2rnx/LICENSE.txt)（GSI Website Terms；改/再分发须引用 Hatanaka 2008）· 本机验证 **RNXCMP 4.2.0** Linux gcc 64-bit（2026-09-24 ET）：`RNX2CRX`/`CRX2RNX` 对 georinex 样例 `14601736.18o` 压缩→恢复实跑；**质检复跑**确认 body 相等、`gzip`≈1830 B、`-h` exit 1

> 岗位：IGS/台网 **观测文件 ASCII 差分压缩**（`.yyo`/`.rnx` ↔ `.yyd`/`.crx`），常再套 `gzip` 成 `.crx.gz` / `.yyd.gz`。冲突时：**本机 `RNX2CRX -h` / 包内 `docs/RNXCMP.txt` > 本文**。

## 1. 用途与边界

**做：**

- `RNX2CRX`：RINEX OBS **2.xx / 3.xx / 4.00–4.01 / 4.02+** → Compact RINEX（Hatanaka）
- `CRX2RNX`：Compact RINEX → 原 RINEX OBS（版本随 CRINEX 头还原）
- 前端壳 `RNX2CRZ` / `CRZ2RNX`（需 **csh**）：多文件 + 默认再 `gzip`（可用 `-Z` 改 UNIX `compress`）
- 命名约定：短名 `*.yyo`↔`*.yyd`；长名 `*O.rnx`/`*o.rnx`↔`*O.crx`/`*o.crx`

**不做：**

- **不是** 通用归档器：只服务 **观测** CompactRINEX；NAV/MET 等前端仅做 gzip/跳过 CRX 步
- **不是** RINEX 拼接/抽稀/改采样 → [gfzrnx](./gfzrnx.md)
- **不是** QC 报表 → [anubis](./anubis.md)；旧 TEQC 批壳 → [pinot](./pinot.md)（其 `crnx2rnx.py` 外包本工具）
- **不是** TEC/定位 → [gnss-tec](./gnss-tec.md) / [rtklib](./rtklib.md)
- Python 绑定/便捷解压 → [hatanaka](./hatanaka.md)（`pip install hatanaka`）；其捆绑二进制版本可能落后官网，**RINEX 4.02 / CRINEX 3.1 仍以本文 GSI 4.2.0 为准**

一句话：RNXCMP = **GSI 官方 Hatanaka 压缩/恢复**；IGS 交换事实标准。

| 术语 | 含义 |
| --- | --- |
| Compact RINEX / CRINEX / Hatanaka | 观测值差分编码的 ASCII 压缩格式 |
| CRINEX 1.0 / 3.0 / 3.1 | 分别对应 RINEX 2.xx / 3.xx+4.00–4.01 / **4.02+**（3.1 含 pico-second） |
| `RNX2CRX` / `CRX2RNX` | 核心二进制（包内大写名；部分镜像小写 `rnx2crx`） |
| `RNX2CRZ` / `CRZ2RNX` | csh 前端：CRX + gzip（或 `.Z`）一步 |

版本对应（4.2.0）：

```text
RINEX 2.xx          ↔ CRINEX 1.0
RINEX 3.xx          ↔ CRINEX 3.0
RINEX 4.00 / 4.01   ↔ CRINEX 3.0
RINEX 4.02+         ↔ CRINEX 3.1   ← 必须用 RNXCMP ≥4.2.0
```

## 2. 安装

```bash
mkdir -p ~/iono_ops/rnxcmp && cd ~/iono_ops/rnxcmp
# 读 LICENSE / README 后再下（GSI 条款 + 引用要求）
curl -fsSL -O https://terras.gsi.go.jp/ja/crx2rnx/LICENSE.txt
curl -fsSL -O https://terras.gsi.go.jp/ja/crx2rnx/RNXCMP_4.2.0_Linux_gcc_64bit.tar.gz
tar xzf RNXCMP_4.2.0_Linux_gcc_64bit.tar.gz
chmod +x RNXCMP_4.2.0_Linux_gcc_64bit/RNX2CRX RNXCMP_4.2.0_Linux_gcc_64bit/CRX2RNX
export PATH="$HOME/iono_ops/rnxcmp/RNXCMP_4.2.0_Linux_gcc_64bit:$PATH"
RNX2CRX -h | tail -n 3
# 期望： [version : ver.4.2.0]
# 可选源码包（含 docs/RNXCMP.txt 与 front-end-tools）：
curl -fsSL -O https://terras.gsi.go.jp/ja/crx2rnx/RNXCMP_4.2.0_src.tar.gz
tar xzf RNXCMP_4.2.0_src.tar.gz
# 自编译（若无匹配二进制）：
#   cd RNXCMP_4.2.0_src/source
#   gcc -std=c99 -O2 rnx2crx.c -o RNX2CRX
#   gcc -std=c99 -O2 crx2rnx.c -o CRX2RNX
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Permission denied` | tar 里二进制无执行位 | `chmod +x RNX2CRX CRX2RNX` |
| `csh: command not found` | 前端脚本是 csh | `sudo apt install csh`；或只用核心二进制 + `gzip` |
| 需要 Python API 而非 CLI | 应用场景不同 | 见 [hatanaka](./hatanaka.md)；4.02 仍用本文二进制 |
| Mac/Win | 架构包不同 | 下对应 `MacOS_clang_*` / `Windows_mingw_*` |

## 3. 端到端：短 OBS → `.18d` → 恢复（本机真跑）

样本：georinex 测试 OBS（RINEX **2.11** Mixed）。数值为 **RNXCMP 4.2.0** 本机输出。

### 3.1 取数 + 压缩

```bash
mkdir -p ~/iono_ops/data/rnxcmp_demo && cd ~/iono_ops/data/rnxcmp_demo
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
head -n 1 14601736.18o
# 期望：含 RINEX VERSION / TYPE；绝不是 <!DOCTYPE html

RNX2CRX 14601736.18o -f
ls -la 14601736.18o 14601736.18d
head -n 3 14601736.18d
wc -c 14601736.18o 14601736.18d
```

**本机 stdout / 结果（2026-09-24 ET）：**

```text
# head -n 3 14601736.18d
1.0                 COMPACT RINEX FORMAT                    CRINEX VERS   / TYPE
RNX2CRX ver.4.2.0                       24-Sep-26 07:57     CRINEX PROG / DATE
     2.11           OBSERVATION DATA    Mixed(MIXED)        RINEX VERSION / TYPE
# （CRINEX PROG / DATE 时间戳随本机时钟变；版本串须含 ver.4.2.0）

# wc -c
7386 14601736.18o
5522 14601736.18d
# 再 gzip（IGS 常见落盘形态）
# gzip -c 14601736.18d > 14601736.18d.gz  → 本机 1830 bytes（gzip 头含 mtime，勿钉死绝对字节）
```

| 参数 | 作用 |
| --- | --- |
| `[file]` | 输入路径；省略则 stdin/stdout |
| `-` | 强制写 stdout（可重定向到任意名） |
| `-f` | 输出已存在时**不询问**直接覆盖 |
| `-e N` | 每 N 历元重置差分初值（利于丢包后局部恢复，文件变大） |
| `-s` | 遇异常历元告警并跳过（默认停并 error） |
| `-d` | 成功（exit 0/2）后删输入；stdin 输入时无效 |
| `-h` | 帮助（注意：帮助路径常以 **exit 1** 结束） |

默认输出名：输入符合 `*.yyo` → `*.yyd`；`*O.rnx` → `*O.crx`。不合约定时用 `RNX2CRX in - > out.crx`。

### 3.2 恢复 + 校验

```bash
CRX2RNX 14601736.18d - > 14601736_restored.18o
# 或：CRX2RNX 14601736.18d -f   → 写回 14601736.18o（会覆盖，慎用）

python - <<'PY'
from pathlib import Path
def body(p):
    raw = Path(p).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    lines = raw.decode().splitlines()
    i = next(n for n, l in enumerate(lines) if "END OF HEADER" in l)
    return [l.rstrip() for l in lines[i:]]
a, b = body("14601736.18o"), body("14601736_restored.18o")
print("obs_body_equal", a == b, "nlines", len(a))
PY
```

**本机：** `obs_body_equal True nlines 92`。头行固定宽度右侧空格可能被修剪；比内容请 `rstrip` 或只比 `END OF HEADER` 之后。

`CRX2RNX` 旗标与上表相同（无 `-e`）：`-` / `-f` / `-s` / `-d` / `-h`。

### 3.3 长名 + 管道 gzip（常见 IGS）

```bash
cp 14601736.18o TEST00XXX_R_20181730617_15S_15S_MO.rnx
RNX2CRX TEST00XXX_R_20181730617_15S_15S_MO.rnx -f
# → TEST00XXX_R_20181730617_15S_15S_MO.crx

gunzip -c 14601736.18d.gz | CRX2RNX > from_gz.18o
# 前端（需 csh；本机无 csh 未跑）：
#   RNX2CRZ -f 14601736.18o          → 14601736.18d.gz
#   CRZ2RNX -f 14601736.18d.gz       → 14601736.18o
```

`RNX2CRZ` 旗标（源码 help）：`-c` 输出到 cwd；`-d` 成功删输入；`-Z` 用 `compress`；`-g` 哑元（默认已是 gzip）；`-f` 强覆；`-q` 安静；`-v` 详细；`-h` 帮助。

### 3.4 退出码与字段

| exit | 含义 |
| ---: | --- |
| 0 | 成功 |
| 1 | 错误（含仅打印 `-h`） |
| 2 | 警告（仍可能写出） |

| CRINEX 头字段 | 含义 |
| --- | --- |
| `CRINEX VERS / TYPE` | Compact 版本（本样例 `1.0` ← RINEX 2.11） |
| `CRINEX PROG / DATE` | 程序名+版本与处理时刻 |
| 其后 | 原 RINEX 头原样嵌入 |

## 4. 接到哪步

- 下载 `.crx.gz` → `CRX2RNX`（或 `CRZ2RNX`）→ [georinex](./georinex.md) / [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)
- 台网入库前压缩 → 本工具；编排壳 → [pinot](./pinot.md) / [autorino](./autorino.md)（rinexmod 也可挂压缩）
- 数据入口 → [data-access](../data-access.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `The file xxx already exists. Overwrite?(n)` 后挂起 | 缺 `-f`，等交互 | `RNX2CRX in.yyo -f` |
| 2 | RINEX 4.02 压完丢失 pico-second / 旧工具拒读 | 应用了 &lt;4.2.0 或 CRINEX 3.1 | 换 **4.2.0+**；全链路统一版本 |
| 3 | `Permission denied` 执行二进制 | tar 未带 +x | `chmod +x RNX2CRX CRX2RNX` |
| 4 | `cmp` 原文件≠恢复文件（本机原 7386 B → 管道恢复 6423 B） | 头行尾空格 / **CRLF→LF**（样例含 `\r`） | 比 `END OF HEADER` 后 body（本机 `obs_body_equal True nlines 92`）；或两侧 `rstrip` + 统一换行 |
| 5 | 中间缺历元后数据全废 | 差分依赖连续弧 | 压缩用 `-e N`；恢复用 `-s`；并确认观测类型列表未变 |
| 6 | `RNX2CRZ` 直接失败 | 无 `csh` / 不在 PATH | `apt install csh`；或 `RNX2CRX`+`gzip -c` |
| 7 | 把 `.yyo.gz` 直接丢给 `RNX2CRX` | 核心工具吃明文 | `gzip -dc f.yyo.gz \| RNX2CRX > f.yyd` |
| 8 | 脚本里想直接读 `.crx` | 本工具是 CLI 二进制 | Python：[hatanaka](./hatanaka.md) / [georinex](./georinex.md)；钉版本时先 `CRX2RNX` |
| 9 | `RNX2CRX -h` 后脚本当失败 | 帮助路径 **exit 1**（本机确认） | 查版本用 `RNX2CRX -h \| tail` 并忽略该 exit；自动化勿把 `-h` 当冒烟成功条件 |
| 10 | 只装了 `pip install hatanaka`（捆 4.1.0）就处理 RINEX 4.02 | 捆绑 RNXCMP 可能落后 GSI | 4.02 / CRINEX 3.1 → 用本文 **4.2.0** 二进制；见 [hatanaka](./hatanaka.md) |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 官方可引用压缩 | **本文 RNXCMP** |
| Python 读 `.crx` / 脚本解压 | [hatanaka](./hatanaka.md)（可再接 [georinex](./georinex.md)） |
| 改内容/拼日 | [gfzrnx](./gfzrnx.md) |
| 批处理壳 | [pinot](./pinot.md) |

- 论文：Hatanaka, Y. (2008), *Bulletin of the GSI*, 55, 21–30 · <https://www.gsi.go.jp/ENGLISH/Bulletin55.html>
- 变更：<https://terras.gsi.go.jp/ja/crx2rnx/CHANGES.txt>
- 兄弟： [hatanaka](./hatanaka.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [pinot](./pinot.md) · [autorino](./autorino.md) · [data-access](../data-access.md)
