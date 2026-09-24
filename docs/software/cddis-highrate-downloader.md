# cddis-highrate-downloader · CDDIS 高采样 GNSS 批量下载操作手册

目录：[`PROJECTS.json` → `cddis-highrate-downloader`](../../PROJECTS.json) · 上游 <https://github.com/cemalialtuntas/cddis-highrate-downloader> · 许可 **MIT** · 版本 **1.0.2**（tip `ad648ea`）· 本机验证：`pip install -e` → `cddis-download`；FTPS 登录 `gdc.cddis.eosdis.nasa.gov` 成功；`CWD /gnss/data/highrate/2026/260/26d/00` 成功；`SIZE BRST00FRA_S_20262600000_15M_01S_MO.crx.gz` = **706256**；`LIST`/`RETR` 本机 **425 Bad IP**（PASV 数据通道受限，未落盘）（2026-09-24 EDT）

> 岗位：按站 / DOY / 小时批量拉 CDDIS **1 s 高采样**（15 min 块）观测。冲突时：**上游 README / Earthdata 路径说明 > 本文**。日采样 30 s → [data-access](../data-access.md) + [fast](./fast.md)；CRX→RNX → [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)。

## 1. 用途与边界

**做：**

- 交互 CLI `cddis-download`：站名、年、DOY、子目录 `YYt`、小时、是否解压/转 RNX
- FTPS 匿名登录 `gdc.cddis.eosdis.nasa.gov`，路径 `/gnss/data/highrate/YYYY/DDD/YYt/HH/`
- 跳过已有 `.crx` / `.rnx`；失败重连；可选 `gzip` 解压 + 调 `CRX2RNX`

**不做：**

- **不是** Earthdata HTTPS 客户端——源码走 **FTPS**；归档政策/鉴权以 NASA 当前页为准（见 [data-access](../data-access.md)）
- **不** 拉日文件 `gnss/data/daily` 或 IONEX → [fast](./fast.md) / [ionex-gim](./ionex-gim.md)
- **不** 内置 Linux `CRX2RNX` 二进制（仓内仅 `CRX2RNX.exe`）→ 转 RNX 用 [rnxcmp](./rnxcmp.md)
- CLI **仅交互 `input()`**，无 argparse；自动化需自包 `CDDISFTPClient` 或改脚本

一句话：按站批量下 CDDIS **high-rate 15 min 块**（闪烁/同震常用）。

| 术语 | 含义 |
| --- | --- |
| `YYt` | 子目录：两位年 + 类型；`d`=Hatanaka 观测（例 2026 → `26d`） |
| `HH` | 小时子目录 `00`…`23` |
| 长名 | `XXXXMRCCC_K_YYYYDDDHHMM_15M_01S_MO.crx.gz` |
| 短期窗 | 近约 **6 个月** 保留逐文件；更早多为 **按站 tar**（工具按小时 LIST，对 tar 年代不友好） |
| `downloads/` | 默认落盘根：`downloads/<站>/<年>/<DOY>/<HH>/` |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/cemalialtuntas/cddis-highrate-downloader.git
cd cddis-highrate-downloader
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
cddis-download  # 无参即进交互；先 Ctrl+C 确认入口存在
python -c "import importlib.metadata as m; print(m.version('cddis-highrate-downloader'))"
# 期望：1.0.2
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `cddis-download: not found` | 未装入当前 venv | `which python`；重 `pip install -e .` |
| `CRX2RNX not found`（Linux） | 包内只有 `.exe` | 转 RNX 改用 [rnxcmp](./rnxcmp.md) 的 `CRX2RNX` |
| 依赖报错 | 仅需 `python-dotenv`（实际下载路径几乎不用） | `pip install -r requirements.txt` |

## 3. 端到端：路径约定 → 校验 → 下载（本机部分真跑）

### 3.1 官方目录（先认清再填 CLI）

据 NASA Earthdata *High-Rate (Sub-Hourly)* 页：

```text
/gnss/data/highrate/YYYY/DDD/YYt/HH/<files>
# 例（Hatanaka 观测，2026 DOY 260 零时）：
/gnss/data/highrate/2026/260/26d/00/BRST00FRA_S_20262600000_15M_01S_MO.crx.gz
```

| CLI 提示 | 填什么 | 例 |
| --- | --- | --- |
| station | RINEX3 站名或空=全站 | `BRST00FRA` |
| year | 四位年 | `2026` |
| DOY | `001` 或 `260-262` | `260` |
| subfolder | **`YYt`**，不是随意 `24d` | 年 2026 观测 → **`26d`** |
| hour | `00` / `00-03` / 空=全部 | `00` |

**坑：** 对 **6 个月以前** 的日期，逐小时目录常已撤成 **tar**；本工具 `list_hour_subfolders` 会报空。旧数据改 HTTPS+Earthdata 下 tar，或换 GFZ highrate（见 [data-access](../data-access.md)）。

### 3.2 本地校验（不触网）

```bash
source ~/iono_ops/cddis-highrate-downloader/.venv/bin/activate
python - <<'PY'
from cddis_downloader.downloader import validate_doy, validate_hour, CDDISFTPClient
from cddis_downloader.utils import get_crx2rnx_path, check_crx2rnx
print("doy", validate_doy("1-3"))
print("hour", validate_hour("00-02"))
print("bad", validate_doy("400"))          # 期望 [] 并打印范围提示
print("crx2rnx", get_crx2rnx_path(), "exists", get_crx2rnx_path().exists())
print("check", check_crx2rnx())            # Linux 常 False
c = CDDISFTPClient(); print("connect", c.connect()); c.close()
PY
```

**本机 stdout（节选）：**

```text
doy ['001', '002', '003']
hour ['00', '01', '02']
DOY must be between 01-366.
bad []
crx2rnx .../CRX2RNX exists False
Error: CRX2RNX not found in package directory.
check False
connect True
```

### 3.3 交互下载（管道示例）

```bash
cd ~/iono_ops/cddis-highrate-downloader   # 输出相对 cwd 的 downloads/
printf 'BRST00FRA\n2026\n260\n26d\n00\ny\nn\n' | cddis-download
# 期望成功时：
#   Processing DOY: 260
#   Processing hours: ['00']
#   Downloaded: BRST00FRA_S_….crx.gz
#   Extracted: …
#   All operations completed.
```

**本机（2026-09-24 EDT）：** 登录与 `CWD …/26d/00` 正常；`SIZE` 证实文件 **706256** 字节；但 `LIST`/`RETR` 报 **`425 Security: Bad IP connecting`**（沙箱 PASV 数据通道），CLI 表现为 `No hour subfolders found`。换家宽/机房或改走 **HTTPS+Earthdata**（下节）即可继续。

### 3.4 API 直下单文件（绕过 LIST）

当能 `RETR` 但交互卡在 LIST 时：

```python
from cddis_downloader.downloader import CDDISFTPClient
c = CDDISFTPClient(); assert c.connect()
base = "/gnss/data/highrate/2026/260/26d"
name = "BRST00FRA_S_20262600000_15M_01S_MO.crx.gz"
c.download_file(base, "00", name, f"/tmp/{name}")
c.close()
```

### 3.5 HTTPS + Earthdata 备援（推荐生产）

工具本身不封装；与 [data-access](../data-access.md) 菜谱一致：

```bash
# ~/.netrc 配 Earthdata 后：
curl -L -n -C - -o BRST_hr.crx.gz \
  "https://cddis.nasa.gov/archive/gnss/data/highrate/2026/260/26d/00/BRST00FRA_S_20262600000_15M_01S_MO.crx.gz"
gzip -dc BRST_hr.crx.gz > BRST_hr.crx
# Linux 转 RNX（仓内无 CRX2RNX 时）：
CRX2RNX BRST_hr.crx          # 来自 rnxcmp；见 [rnxcmp](./rnxcmp.md)
```

GFZ 匿名 HTTPS 备份：`https://isdc-data.gfz.de/gnss/data/highrate/`。

## 4. 接到哪步

- 下完 CRX → [hatanaka](./hatanaka.md)/[rnxcmp](./rnxcmp.md) → [georinex](./georinex.md) 探活
- 闪烁 / ROTI → [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)；教程 [05](../tutorials/05-scintillation-roti.md)
- 日采样或产品树总览 → [data-access](../data-access.md)·[fast](./fast.md)
- IONEX 对照 → [ionex-gim](./ionex-gim.md)·[diffionmap](./diffionmap.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `No hour subfolders` 但网页有数 | `subfolder` 填成旧年的 `24d` | 年 2026 用 **`26d`**（`YY`+`d`） |
| 2 | 半年前日期永远空 | 已收成 **tar**，无 `YYt/HH` | 改下 `*.tar`（HTTPS）或换近 6 个月 DOY |
| 3 | `425 Bad IP connecting` | FTPS PASV 数据通道被 NAT/防火墙改写 | 换网络；或改 **HTTPS+`.netrc`** |
| 4 | `550 Failed to change directory` | DOY/子目录不存在 | 先 `CWD` 探 `/gnss/data/highrate/YYYY/DDD/YYt` |
| 5 | Linux 无法转 RNX | 仅捆 `CRX2RNX.exe` | `CRX2RNX` 出自 [rnxcmp](./rnxcmp.md)；或 `pip` [hatanaka](./hatanaka.md) |
| 6 | 站过滤为空 | 短名 `BRST` 对不上长名 | 用完整 `BRST00FRA`（`startswith`） |
| 7 | 自动化卡在 `input()` | 无 CLI 旗标 | `printf '…\n' \| cddis-download` 或调 `CDDISFTPClient` |
| 8 | 把 high-rate 当 30 s 日文件 | 树不同 | daily → `/gnss/data/daily/`；本工具只 highrate |
| 9 | 体量爆盘 | 全站×96 块/日 | 先单站单小时；限速 |
| 10 | README「无需账号」vs 401/空目录 | 政策与 FTPS 行为在变 | 跟 [data-access](../data-access.md) Earthdata 步骤 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| CDDIS **1 s / 15 min** 批量（FTPS 交互） | **本文 cddis-highrate-downloader** |
| 日采样 / 星历 / 产品 | [fast](./fast.md) · [data-access](../data-access.md) |
| CRX↔RNX | [rnxcmp](./rnxcmp.md) · [hatanaka](./hatanaka.md) |
| 读 IONEX / 两图对照 | [ionex-gim](./ionex-gim.md) · [diffionmap](./diffionmap.md) |

- 仓库：<https://github.com/cemalialtuntas/cddis-highrate-downloader>
- 路径说明：<https://www.earthdata.nasa.gov/data/space-geodesy-techniques/gnss/high-rate-sub-hourly-data-product>
- 兄弟：[data-access](../data-access.md) · [fast](./fast.md) · [rnxcmp](./rnxcmp.md) · [hatanaka](./hatanaka.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [diffionmap](./diffionmap.md)
