# gnss-osi-download · 爱尔兰 Tailte/OSI Active GNSS RINEX 下载操作手册

目录：[`PROJECTS.json` → `GNSS_OSI_download`](../../PROJECTS.json) · 上游 <https://github.com/jdesbonnet/GNSS_OSI_download> · 数据门户 <https://gnss.tailte.ie/download-rinex.php> · 许可 **MIT** · tip **`0aeb83a`**（2024-11-25）· ★**1** · **无 PyPI** · 单文件 `osi_gnss_download.py` · 本机验证（2026-09-24 07:29 EDT）：`-h` 全旗标 OK；`--list-stations` / 下载 → **`requests.exceptions.ConnectionError`**（`NameResolutionError: Failed to resolve 'gnss.osi.ie'`）；**未落盘** `RINEX_*.zip` · **质检复跑**（2026-09-25 23:36 EDT）：tip **`0aeb83a`** 未变；requests **2.34.2**/bs4 **4.15.0**；Google DoH `gnss.osi.ie` → **Status 3 = NXDOMAIN（全球域名已撤，不是本机 DNS 墙）**；`tailte.ie` **200**；候选 `gnss.tailte.ie` 解析 **137.191.226.156** 但 HTTPS **TLS EOF**/HTTP 超时 → 脚本**事实失效**

> 岗位：从 **Tailte Éireann**（原 Ordnance Survey Ireland / OSI）Active GNSS 网网页表单拉 **近 30 日** RINEX ZIP。冲突时：**门户 T&C / 上游 README > 本文**。下载前须在 <https://gnss.tailte.ie/download-rinex.php> 同意条款。上游自述 **2024-11-20** 可用。

## 1. 用途与边界

**做：**

1. **`--list-stations`**：抓首页 `<select name="station0">` 打印站 ID + 名称
2. **按站·日·小时窗下载**：会话 cookie + 隐藏域 `as_sfid` → POST 筛选 → GET `/?download` → `RINEX_{stnid}_{date}_{HH}_{HH}.zip`
3. **`--debug`**：打印响应状态 / cookie / 正文前缀
4. **`--user-agent`**：覆盖默认 `GNSS_OSI_download v1.0`

**不做：**

- **不是** 全球 IGS/CDDIS 批下 → [gampii-good](./gampii-good.md) / [fast](./fast.md) / [data-access](../data-access.md)
- **不是** EarthScope API → [earthscope-sdk](./earthscope-sdk.md)
- **不是** 解压 Hatanaka / 读 RINEX → [hatanaka](./hatanaka.md) / [georinex](./georinex.md)
- **不** 提供账号密码流——门户靠浏览器会话 + 表单 token；脚本模拟公开表单
- **仅近 ~30 日**；更早数据门户不可用（脚本明文提示）

一句话：**爱尔兰国家 CORS 近实时 RINEX 的个人向爬虫式 CLI**；硬编码的 `gnss.osi.ie` **已 NXDOMAIN**，现状只能验证帮助与失败栈。

> **质检结论（硬）**：上游 2024-11 后无提交，`BASE_URL` 仍指旧域名。机构改名 Tailte Éireann 后旧子域撤销；新门户地址/表单是否仍含 `as_sfid`/`station0` **本机不可达、未验证**——改 `BASE_URL` 前先浏览器确认，**勿**假设表单兼容。

| 术语 | 含义 |
| --- | --- |
| Tailte / OSI | 爱尔兰测绘机构；站网原名 OSI Active GNSS |
| `as_sfid` | 首页隐藏字段；无此 token POST 会失败 |
| `station0` | 表单站选择控件名；例 **`glw1`**（Galway） |
| 30 日窗 | README + `-h` + 无数据文案均强调 |
| `gnsss.osi.ie` | 源码无数据提示里的 **三 s 笔误**（应为 `gnss.osi.ie`） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/jdesbonnet/GNSS_OSI_download.git
cd GNSS_OSI_download
git rev-parse --short HEAD   # 期望 0aeb83a
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install requests beautifulsoup4
# Ubuntu 也可：sudo apt-get install python3-requests python3-bs4
python3 osi_gnss_download.py -h
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'bs4'` | 未装 BeautifulSoup；**连 `-h` 都崩**（顶层 import） | `pip install beautifulsoup4` |
| `NameResolutionError` / `ConnectionError` | `gnss.osi.ie` **全球 NXDOMAIN**（DoH Status 3） | 换 DNS **无用**；需确认新门户后改 `BASE_URL`——见 §3.2 |
| 无 console 脚本入口 | 设计为单文件 | 始终 `python3 osi_gnss_download.py …` |
| argparse 不强制 `--station-id`/`--date` | 源码未 `required=True` | 缺参也会去 GET 首页→同样网络错误 |

## 3. 端到端（本机真跑）

### 3.1 帮助（离线可复现）

```bash
cd ~/iono_ops/GNSS_OSI_download
source .venv/bin/activate
python3 osi_gnss_download.py -h
```

**本机 stdout（节选）：**

```text
usage: osi_gnss_download.py [-h] [--list-stations] [--station-id STATION_ID]
                            [--date DATE] [--start-hour START_HOUR]
                            [--end-hour END_HOUR] [--user-agent USER_AGENT]
                            [--debug]

Download GNSS RINEX files from https://gnss.osi.ie. Please agree to T&C on
site first.

options:
  -h, --help            show this help message and exit
  --list-stations       Obtain a list of station IDs and exit. (default:
                        False)
  --station-id STATION_ID
                        Station ID. … Example glw1 (Galway) (default: None)
  --date DATE           Date of data capture yyyy-mm-dd. Note: only last 30
                        days of data is available. (default: None)
  --start-hour START_HOUR
                        Start hour (UTC) 0 to 22 (default: 0)
  --end-hour END_HOUR   End hour (UTC) 1 to 23 (default: 24)
  --user-agent USER_AGENT
                        User-agent header … (default: GNSS_OSI_download v1.0)
  --debug               Output debugging info. (default: False)

Project website: https://github.com/jdesbonnet/GNSS_OSI_download
```

### 3.2 列站 / 下载（旧域名 NXDOMAIN）

```bash
python3 osi_gnss_download.py --list-stations
# 或（门户可达且已同意 T&C 时）
python3 osi_gnss_download.py --station-id=glw1 --date=YYYY-MM-DD --start-hour=00 --end-hour=06
```

**本机 stderr 尾（2026-09-24 07:29 EDT；`--list-stations` exit 1）：**

```text
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='gnss.osi.ie', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='gnss.osi.ie', port=443): Failed to resolve 'gnss.osi.ie' ([Errno -2] Name or service not known)"))
```

同机 `curl -sI -L --max-time 15 https://gnss.osi.ie/` → `http_code=000`。质检（2026-09-25 23:36 EDT）`--list-stations` 与 `--station-id=glw1 --date=2026-09-20 --start-hour=0 --end-hour=6` **同一栈、exit 1**、cwd 无 `*.zip`。

判因三步（真跑）：

```bash
getent hosts gnss.osi.ie; echo $?                       # 2（无记录）
curl -s 'https://dns.google/resolve?name=gnss.osi.ie&type=A'   # "Status":3 → NXDOMAIN（全球）
curl -sv --max-time 20 -o /dev/null https://gnss.tailte.ie/ 2>&1 | grep -i tls
# TLS alert, decode error / unexpected eof while reading（本机；候选新域未证实可用）
```

**禁止**臆造站表或 ZIP 大小。

### 3.3 门户可达时的期望流程（源码路径；非本机 stdout）

1. GET `https://gnss.osi.ie/` → 解析 `as_sfid`
2. POST 同 URL：`station0` / `date` / `start` / `end` / `submitSearchByStation=FIND DATA` / `as_sfid`
3. 若正文含 `No data available for your chosen station.` → 打印 30 日提示（文内链误写 `https://gnsss.osi.ie`）
4. 否则 GET `https://gnss.osi.ie/?download` → 写  
   `RINEX_{station}_{date}_{start:02d}_{end:02d}.zip`  
   例：`RINEX_glw1_2024-11-19_00_06.zip`
5. 成功打印：`Data successfully downloaded and saved as …`

## 4. 参数与 I/O

| 旗标 | 默认 | 说明 |
| --- | --- | --- |
| `--list-stations` | off | 列站后 `exit` |
| `--station-id` | None | 如 `glw1` |
| `--date` | None | `yyyy-mm-dd`；仅近 30 日 |
| `--start-hour` | `0` | UTC 0…22 |
| `--end-hour` | `24` | UTC 1…23；脚本 `int()` |
| `--user-agent` | `GNSS_OSI_download v1.0` | 写入请求头 |
| `--debug` | off | 响应调试 |

| 输出 | 说明 |
| --- | --- |
| `RINEX_*.zip` | 当前工作目录；内含门户打包的 RINEX |
| stdout 成功句 | `Data successfully downloaded…` |
| 无数据句 | 含 30 日说明 + 笔误域名 |

硬编码常量：`BASE_URL=https://gnss.osi.ie`；`FORM_ENDPOINT=/`；`DOWNLOAD_ENDPOINT=/?download`。

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| 解压 / CRX | [hatanaka](./hatanaka.md) / [rnxcmp](./rnxcmp.md) |
| 读进 Python | [georinex](./georinex.md) |
| 全球产品/观测 | [data-access](../data-access.md) / [gampii-good](./gampii-good.md) |
| EarthScope API | [earthscope-sdk](./earthscope-sdk.md) |
| QC | [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md) |

## 6. 常见坑（≥8）

1. **先打开门户点同意 T&C**——脚本不代替法律同意
2. **只要最近约 30 天**——更早日期会走「No data…」分支（门户可达时）
3. **旧域已撤**：`gnss.osi.ie` 全球 NXDOMAIN（非本机问题）；先 DoH 判全局 vs 本地，再谈换 DNS
4. **缺 `--station-id`/`--date`**：不会 argparse 报错，直接带着 `None` 去请求
5. **小时窗**：`end-hour` 默认 `24`；与 README 示例 `00`–`06` 对照
6. **相对路径落盘**：ZIP 写在 **cwd**，不在仓内固定 `out/`
7. **源码笔误** `gnsss.osi.ie`：无数据提示链；浏览器请用双 s
8. **表单改版**：缺 `as_sfid` → `Error: 'as_sfid' hidden field not found…`（需改选择器）
9. **勿当批处理框架**：无重试队列 / 多站循环——自行 shell `for`
10. **无 PyPI**：版本钉 tip SHA；勿 `pip install GNSS_OSI_download`

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 爱尔兰 Tailte 近 30 日 RINEX | **gnss-osi-download**（本页） |
| 多源 IGS/CORS GUI | [gdds](./gdds.md) |
| YAML 批下 | [gampii-good](./gampii-good.md) |
| EarthScope 官方 API | [earthscope-sdk](./earthscope-sdk.md) |
| CDDIS 15 min 高采样 | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
