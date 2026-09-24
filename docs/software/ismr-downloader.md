# ismr_downloader · ISMR 闪烁监测数据 CLI 下载操作手册

目录：[`PROJECTS.json` → `ismr_downloader`](../../PROJECTS.json) · 上游 <https://github.com/GEGE-UNESP/ismr_downloader> · PyPI **`ismr-downloader`** · 许可 **MIT** · 本机 **0.2.0**（tip `cca68e4`）· 验证：`pip install` → `--help`；无凭证拒下；假账号 `--insecure` 打到 `api-ismrquerytool…/user/token` → **HTTP 400**；无 `--insecure` → **SSLCertVerificationError**；网页 `curl -sk` **200**（2026-09-24 EDT）· **全量落盘需网页注册账号（本机未持凭证，不臆造成功 stdout）** · **质检复跑通过**（`--help`；缺邮箱/缺站 exit **1**；SSL `CERTIFICATE_VERIFY_FAILED`；`--insecure` 假账号 token **400**；curl token JSON `User not found…`；tip `cca68e4`；2026-09-24 05:03 EDT）

> 岗位：从 **ISMR Query Tool API** 按站/时段批量拉 **ISMR / 1min-ISMR / SBF / RINEX**。冲突时：**上游 README / 本机 `-h` > [data-access](../data-access.md) 配方 > 本文**。网页 Query Tool 常超时/证书翻车——**以本 CLI 为主路径**。

## 1. 用途与边界

**做：**

- CLI `ismr-downloader`：邮箱密码鉴权 → Bearer token（缓存 `.token.json`）→ 分块并行下载
- 数据类型：`ismr` | `ismr1min` | `sbf` | `rinex`
- 长区间按 `--max-days` 切块；限流 `--max-req`；缺段写入 `logs/no_data_*.csv`

**不做：**

- **不** 替代网页注册——账号须在 [ISMR Query Tool](https://ismrquerytool.fct.unesp.br/) 申请（见 [data-access](../data-access.md)「闪烁 ISMR」）
- **不** 做 S4/σφ 科学产品或 ROTI——下完后自做质控/解析；ROTI → [oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)；仿真概念 → [iono-scintillation](./iono-scintillation.md)
- **不** 拉 IGS/CDDIS 通用观测 → [fast](./fast.md)/[cddis-highrate-downloader](./cddis-highrate-downloader.md)/[gdds](./gdds.md)
- **不** 解析 Septentrio SBF 块 → 厂商/社区解析器（如 SbfParser）；本工具只负责从 API 取文件

一句话：**有账号后的 ISMR 批量备数 CLI**；补强 data-access 配方（网页易挂）。

| 术语 | 含义 |
| --- | --- |
| ISMR | Ionospheric Scintillation Monitoring Receiver 输出（闪烁监测） |
| API_BASE | `https://api-ismrquerytool.fct.unesp.br/api/v1` |
| token | `POST …/user/token` → `access_token` + `expires_at`；落盘 `.token.json` |
| bundle | 成功响应里的打包下载元数据（`url`/`filename`） |
| `--insecure` | 关闭 TLS 证书校验（证书链不完整时急救） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install 'ismr-downloader==0.2.0'
ismr-downloader --help | head -n 5
python -c "import importlib.metadata as m; print(m.version('ismr-downloader'))"
# 期望：
# usage: ismr-downloader [-h] [--email EMAIL] [--password PASSWORD] [-f]
#                        [--token-file TOKEN_FILE] [--stations STATIONS]
#                        [--start START] [--end END]
#                        [--data-type {ismr,sbf,rinex,ismr1min}] [--overwrite]
#                        [--max-workers MAX_WORKERS] [--max-days MAX_DAYS]
# 0.2.0
```

源码/开发：

```bash
git clone --depth 1 https://github.com/GEGE-UNESP/ismr_downloader.git
cd ismr_downloader
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ismr_downloader --help
# tip 本机：cca68e4
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python &lt; 3.10 | 换 3.10+ |
| `ismr-downloader: not found` | 未进 venv / 未装入口 | `which python`；重 `pip install ismr-downloader` |
| 包名混淆 | 仓名 `ismr_downloader` vs PyPI `ismr-downloader` | **pip 用连字符**；`python -m ismr_downloader` 用下划线模块 |

## 3. 端到端：注册 → 鉴权探针 → 拉取（本机部分真跑）

### 3.1 账号（必须）

1. 打开 <https://ismrquerytool.fct.unesp.br/>（本机 `curl -sk` → **HTTP 200**；无 `-k` 常因证书链失败）
2. 按站点流程注册，取得 **邮箱 + 密码**（政策以 UNESP 页为准；密码复杂度由 API 校验）
3. **勿把凭证写入本仓库**；用环境变量或本机 `.env`

```bash
# .env 示例（本地，gitignore）
# ISMR_EMAIL=you@example.com
# ISMR_PASSWORD='…'
# DATA_TYPE=ismr
# ISMR_STATIONS=PRU2,MOR3
# ISMR_START=2023-02-18
# ISMR_END=2023-02-18
```

### 3.2 无凭证 / 缺参（本机真 stdout）

```bash
source ~/iono_ops/.venv/bin/activate
ismr-downloader --stations MOR3 --start 2025-11-24T00:00:00 --end 2025-11-24T00:30:00 --data-type ismr
# 期望：
# Email and password must be provided (via CLI or .env).

ismr-downloader --email a@b.com --password 'Notreal1!' --start 2025-01-01 --end 2025-01-01 --insecure
# 期望：
# At least one station must be provided (via CLI or .env).
```

### 3.3 TLS 与假账号鉴权（本机真跑；API 可达；质检复跑 2026-09-24 05:03 EDT）

```bash
# 无 --insecure：证书校验失败（节选）
ismr-downloader \
  --email fake@example.com --password 'Notreal1!' \
  --stations MOR3 --start 2025-11-24T00:00:00 --end 2025-11-24T00:30:00 \
  --data-type ismr --force-auth
# 期望尾部含：
# requests.exceptions.SSLError: … api-ismrquerytool.fct.unesp.br …
# … [SSL: CERTIFICATE_VERIFY_FAILED] … unable to get local issuer certificate …

# 有 --insecure + 假账号：打到 token 接口 → 400（用户不存在）
ismr-downloader \
  --email fake@example.com --password 'Notreal1!' \
  --stations MOR3 --start 2025-11-24T00:00:00 --end 2025-11-24T00:30:00 \
  --data-type ismr --insecure --force-auth
# 期望：
# INFO: Requesting new token from API
# … HTTPError: 400 Client Error: Bad Request for url:
#   https://api-ismrquerytool.fct.unesp.br/api/v1/user/token
```

等价直探针（确认 API 活着，非登录成功）：

```bash
curl -sk -X POST 'https://api-ismrquerytool.fct.unesp.br/api/v1/user/token' \
  -H 'Content-Type: application/json' \
  -d '{"email":"fake@example.com","password":"Notreal1!"}'
# 期望 JSON 含："User not found with email fake@example.com."
```

### 3.4 有账号后的拉取模板（结构真；成功 stdout 待持凭证复跑）

```bash
export ISMR_EMAIL='…' ISMR_PASSWORD='…'   # 你的注册账号
ismr-downloader \
  --email "$ISMR_EMAIL" --password "$ISMR_PASSWORD" \
  --stations PRU2 \
  --start 2023-02-18 --end 2023-02-18 \
  --data-type ismr \
  --output-dir ~/iono_ops/ismr_data \
  --logs-dir ~/iono_ops/ismr_logs \
  --insecure --force-auth
# 成功时期望（上游行为，非本机落盘）：
#   INFO: Requesting new token from API / New token acquired …
#   INFO: [ISMR] Downloading <filename> (… → …)
#   downloads/ 下出现 API 返回的 filename；logs/run_*.log + downloaded_files_*.txt
# 无数据时段：logs/no_data_*.csv（404 记入）
```

`.env` 方式：

```bash
ismr-downloader --env ~/.config/ismr/.env --insecure
```

Docker（上游镜像，未在本机复跑）：`yingyangtongxue/ismr-downloader:latest`，挂载工作目录并传 `ISMR_EMAIL`/`ISMR_PASSWORD`。

## 4. I/O

| | |
| --- | --- |
| **输入** | 注册邮箱/密码；站名（如 `PRU2`,`MOR3`）；UTC 日期或 ISO 时段；`--data-type` |
| **鉴权** | `POST /api/v1/user/token` → Bearer；缓存 `--token-file`（默认 `.token.json`） |
| **下载** | `GET`：`…/data/download/{ismr\|sbf\|rinex}` 或 `…/products/download/1min-ismr`；查询参数 `station,start,end` |
| **输出** | `--output-dir`（默认 `downloads/`）下由 API 给出的 `filename`；并行默认 5 |
| **日志** | `logs/run_*.log`、`downloaded_files_*.txt`、`no_data_*.csv` |
| **本机未完成** | **持凭证全量落盘**（登记门禁）；成功文件名/字节以你首次实拉为准 |

仅日期时：`YYYY-MM-DD` → 当日 `00:00:00`–`23:59:59`（UTC 语义以上游为准）。

## 5. 参数（高频）

| 参数 | 作用 | 默认/注意 |
| --- | --- | --- |
| `--email` / `--password` | 鉴权 | 或 `ISMR_EMAIL` / `ISMR_PASSWORD` |
| `-f` / `--force-auth` | 忽略缓存 token | 凭证变更时用 |
| `--token-file` | token 缓存路径 | `.token.json` / `$ISMR_TOKEN_FILE` |
| `--stations` | 逗号分隔站 | 或 `ISMR_STATIONS` |
| `--start` / `--end` | 时段 | 或 `ISMR_START` / `ISMR_END` |
| `--data-type` | `ismr\|sbf\|rinex\|ismr1min` | 或 `DATA_TYPE`（默认 ismr） |
| `--output-dir` | 落盘根 | `downloads` / `$ISMR_OUTPUT_DIR` |
| `--logs-dir` | 日志根 | `logs` |
| `--max-workers` | 并行 | 默认 **5** |
| `--max-days` | 每块最大天数 | 默认 **15** |
| `--max-req` | 每分钟请求上限 | 默认 **30** |
| `--overwrite` | 覆盖已存在文件 | 默认跳过 |
| `--insecure` | 关 TLS 校验 | 证书急救；生产慎用 |
| `-e` / `--env` | `.env` 路径 | 默认 `.env` |

## 6. 接到哪步

| 上游/旁路 | 下一步 |
| --- | --- |
| 配方总览 | [data-access.md](../data-access.md)「闪烁 ISMR」 |
| 拉到 `.ismr` / 相关观测后 | 自建质控；ROTI/ΔTEC → [oasis-roti](./oasis-roti.md)；C++ 链 → [ionomoni](./ionomoni.md) |
| 需要高采样 RINEX 对照 | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 闪烁物理/仿真概念 | [iono-scintillation](./iono-scintillation.md) · 教程 [05](../tutorials/05-scintillation-roti.md)/[13](../tutorials/13-scintillation-modeling.md)/[21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 暴时背景指数 | [geospacelab](./geospacelab.md) |

工作流 **B（不规则体）**：本工具备 ISMR →（可选高采样 RINEX）→ ROTI/监测工具 → 教程对照。

## 7. 坑（≥8）

1. **网页 Query Tool 常挂/超时**——以 CLI+API 为主；网页只负责注册与偶发浏览。
2. **TLS 证书链不完整**——无 `--insecure` 常见 `CERTIFICATE_VERIFY_FAILED`；急救加 `--insecure`，勿当长期安全策略。
3. **必须先注册**——假邮箱 API 回 400 `User not found`；未登录不能匿名下。
4. **密码规则严**——API 要求长度/大小写/符号/数字；本地随意短密码会先被校验拒绝。
5. **站名写错 ≈ 长期 404**——记入 `no_data_*.csv`，不像“网络挂了”；先核 Query Tool 站表。
6. **日期只给日**——自动扩成全日；跨日大窗记得 `--max-days`，避免单请求过大。
7. **限流 429**——默认约 30 req/min；连续两次 429 会 `SystemExit`；降 `--max-workers`/`--max-req`。
8. **503 维护**——工具直接退出并打 critical；勿死循环猛刷。
9. **`.token.json` 含密钥**——勿提交 Git；换机/换密用 `--force-auth`。
10. **已存在文件默认跳过**——重下加 `--overwrite`。
11. **包名**：pip `ismr-downloader` ≠ import/模块 `ismr_downloader`。
12. **SBF/RINEX 类型**——仍走同一账号体系；下完解析另接工具，本 CLI 不解读内容。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| UNESP/INCT 等低纬 **ISMR 闪烁监测文件**批量 | **本工具** |
| 网页点选偶发下载 | Query Tool 网页（辅；易超时） |
| IGS/CDDIS 普通或高采样 GNSS | [fast](./fast.md) / [gdds](./gdds.md) / [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 观测 → ROTI/ΔTEC | [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md) |
| 闪烁仿真（非实测） | [iono-scintillation](./iono-scintillation.md) |

**维护者备注：** 持有效账号复跑一节 3.4，把真实 `filename`/字节与 `logs/` 摘要补进质检行；勿用虚构成功 stdout。
