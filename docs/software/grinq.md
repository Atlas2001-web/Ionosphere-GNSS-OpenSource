# grinq · 多数据中心 RINEX 日文件批量下载 操作手册

目录：[`PROJECTS.json` → `grinq`](../../PROJECTS.json) · 上游 <https://github.com/PJarrin/grinq>（MIT，Zenodo DOI 10.5281/zenodo.22228489，setup.py `0.0.1`，tip `d0891d2`，2026-09-17 04:52 EDT）· 本机验证 **2026-09-26 05:43–05:51 EDT**，Python 3.11 venv，`uv pip install ./grinq`（源码 tarball，未 clone）。

> **质检复跑通过（2026-09-26 06:07–06:09 EDT）**：Python 3.11 uv venv，源码 tarball `d0891d2`，numpy 1.26.4，earthscope-sdk 1.6.1，venv 361 MB。§2 漏装 `requests` 的报错、§4 七个落盘文件的字节数（glps 593531/622511、mdo1 2383548、POTS 6393064、DLF1 3383327、AUCK 7903579 且 2880 历元、ALIC 32500 B 的 S3 网页 `gzip -t` not in gzip format）、重复下载时的 “exists” 提示，以及坑 3、4、5、7、9、`-c foo`、站名 5 位、unavco `ImportError` 的原文都逐字复现。本机没有 lftp，坑 5 由源码 `clone.py:15-26` 核实。坑 6（`-P`）、坑 8、坑 10、ergnss/renag/noanet/euref 没重跑。
>
> 岗位：给定**中心名 + 站名 + 年积日区间**，把 RINEX 2 短名或 RINEX 3 长名**日文件**拉到 `DIR/年/年积日/`。它**不解 Hatanaka**、不做质检（QC 脚本要另行注册拿 Anubis），也不查站点是否存在。
> 同类比较：只要 IGS 站、想知道哪个镜像全、哪个快 → [gnss-obs-mirrors](./gnss-obs-mirrors.md)；美国 CORS → [noaa-ncn-data](./noaa-ncn-data.md)；欧洲 EPN/RENAG 带 md5 → [epos-glass-api](./epos-glass-api.md)；门户门槛见 [data-access](../data-access.md)。
> 冲突时：**本机 `grinq_get_rinex.py -h` / 上游源码 > 本文**。

## 1. 做什么 / 不做什么

| 脚本 | 作用 | 本机结论 |
| --- | --- | --- |
| `grinq_get_rinex.py` | 逐日逐站拼 URL 下载日文件 | **能用**（要先补装 `requests`，见 §2） |
| `grinq_ftp_mirror_sync.py` | 包一层 `lftp mirror` 做目录镜像 | **原样不能用**：找不到系统 lftp、`-P` 参数传错（§6 坑 5、6） |
| `grinq_make_qc.py` | 调 Anubis 出 QC 统计 | 未测：Anubis 要注册下载 |

中心表写在包内 `grinq/info/data_center.dat`（21 行）。`-h` 自称“open access”的有 cddis、sopac、ngs、ign、renag、sonel、ergnss、euref、gfz、gink、ramsac、ibge、noanet、cacsa、argn、nzealand；要账号的有 unavco（EarthScope token）、ramsac_hr；表里还有 wuhan，但下载分支里没有它，选了也什么都不做。

## 2. 安装（本机真跑）

```bash
uv venv -p python3.11 venv
uv pip install -p venv/bin/python ./grinq     # 或 pip install git+https://github.com/PJarrin/grinq.git
venv/bin/python venv/bin/grinq_get_rinex.py -c sopac -syr 2018 -eyr 2018 -sd 1 -ed 1 -dir Rinex -site glps
# 实际：
#   File ".../grinq/lib/download.py", line 238, in via_url
#     import requests
# ModuleNotFoundError: No module named 'requests'
uv pip install -p venv/bin/python requests     # 本机装到 2.34.2 后正常
```

- **setup.py 没写 `requests`**，所有 HTTP(S) 中心都靠它 → 必须手动补装。
- 依赖钉得很旧（`numpy<=1.26.4`、`matplotlib<=3.8.0`、`tqdm==4.59.0`），Python 3.13 上 numpy 1.26 无轮子，用 3.11/3.12。
- 依赖会拉最新 `earthscope-sdk`（本机 1.6.1，连带 boto3/awscrt，venv 共 358 MB），但代码要的是 0.2.1 的接口：
  `ImportError: cannot import name 'DeviceCodeFlowSimple' from 'earthscope_sdk.auth.device_code_flow'`。不用 unavco 就无所谓；要用就 `pip install earthscope-sdk==0.2.1`。

## 3. 参数

| 参数 | 含义 | 备注 |
| --- | --- | --- |
| `-c` | 中心名（见 §1） | 不在表里：`ValueError: Center 'foo' not found in file: data_center.dat` |
| `-syr -eyr -sd -ed` | 起止年、起止年积日（全部必填） | 内部转 MJD 连续循环，可跨年；起点晚于终点时**静默什么都不做**，退出码 0 |
| `-dir` | 本地根目录 | 自动建 `DIR/YYYY/DDD/`；`-hrate` 时为 `DIR/SITE/YYYY/DDD/` |
| `-site` / `-ilist` | 单站 / 站表文件（一行一站，`#` 注释） | 只收 4 位（RINEX 2）或 9 位（RINEX 3）；5 位报 `Invalid site code length` |
| `-rename` | 下完把 RINEX 3 长名改成 2 短名 | **只改文件名**，内容仍是 CRINEX 3（§6 坑 4） |
| `-hrate` | 1 Hz 高采样 | 代码里只有 unavco、sopac、ramsac_* 有分支，且只收 4 位站名 |
| `-token` | EarthScope token json | unavco 必填 |
| `-login 'user pass'` | 受限中心账号 | **一用就崩**（§6 坑 3） |

## 4. 实测：哪些中心能匿名拿到（2026 年积日 200，外加 SOPAC 2018 老数据）

```bash
G="venv/bin/python venv/bin/grinq_get_rinex.py"
$G -c sopac -syr 2017 -eyr 2018 -sd 365 -ed 1 -dir Rinex -site glps    # 跨年两天
$G -c ngs   -syr 2026 -eyr 2026 -sd 200 -ed 200 -dir Rinex -site mdo1
$G -c gfz   -syr 2026 -eyr 2026 -sd 200 -ed 200 -dir Rinex -site POTS00DEU
```

| 中心 | 站 | 结果 | 落盘文件 / 字节 |
| --- | --- | --- | --- |
| sopac（http，不是 https） | glps | ✅ | `glps0010.18d.Z` 593531、`glps3650.17d.Z` 622511（CRINEX 1.0，teqc 2017Jul18） |
| ngs | mdo1 | ✅（先 404 `.d.Z` 再拿到 `.d.gz`） | `mdo12000.26d.gz` 2383548，RINEX 2.11，30 s |
| gfz | POTS00DEU | ✅ | `POTS00DEU_R_…_01D_30S_MO.crx.gz` 6393064（JAVAD TRE_3，C/E/G/I/J…） |
| gink（Kadaster） | DLF100NLD | ✅ | `.crx.gz` 3383327 |
| nzealand（GeoNet） | AUCK00NZL | ✅ | `.rnx.gz` 7903579（**不是** crx），2880 历元 = 30 s 满一天 |
| euref（BKG） | ACOR00ESP | ✅ | `.crx.gz` 2880857 |
| noanet | AGNI00GRC | ✅ | `.crx.gz` 2104240 |
| renag | AGDE00FRA / agde | ✅ | `.crx.gz` 2591781 / `agde2000.26d.Z` 1870420 |
| ergnss | ACOR00ESP 目录存在 | 路径格式对（目录可列） | 未落盘，同 EUREF 数据 |
| argn（GA） | ALIC00AUS | ❌ **假成功** | 32500 字节的 **AWS S3 网页** 存成 `.crx.gz`，`gzip -t`: not in gzip format |
| ramsac | igm1 | ❌ | 服务器根 `wilkilen.fcaglp.unlp.edu.ar/gnss/rinex2/RAMSAC/` 本身 404 |
| cacsa | algo | ❌ | `SSLError(SSLEOFError … UNEXPECTED_EOF_WHILE_READING)`，curl 同样连不上 |
| ign / sonel / cddis（FTP） | smne / ABMF00GLP | 本机不通 | `425 Security: Bad IP connecting.`——本机出口 NAT 让 FTP 数据连接换了 IP，**是本机网络问题**，不能据此判上游坏 |

站名选错时（EUREF 当天没有 WTZR、NOA 没有 ANAV、RENAG 没有 MARS），输出就是一串 404，别误判成中心挂了——先 `curl` 列目录确认。

输出长这样（每个候选名试一次，命中即停）：

```
 -- Looking for rinex in sopac data center
     -- Error: 404 Client Error: Not Found for url: http://garner.ucsd.edu/pub/rinex/2018/001/zzzz0010.18d.Z
     -- If any file was fetched, try checking firewall permissions
     ...（再试 .18d.gz、.18o.gz）
```

再跑一次同样命令：`   - glps0010.18d.Z exists. Not downloading rinex.`（只看 `DIR/YYYY/DDD/` 下有没有同名文件，不校验大小）。

## 5. 它拼的文件名（`lib/read.py`）

- 4 位站：`ssssDDD0.YYd.Z` → `.YYd.gz` → `.YYo.gz`；ergnss/ramsac 用大写站名，ibge 另走 zip 再转 Hatanaka。
- 9 位站：`SITE_{R,S,T}_YYYYDDD0000_01D_{30S,15S}_MO.crx.gz`，共 6 个候选；nzealand 换成 `.rnx.gz`。只找日文件，不找小时文件、不找 `_MN` 导航文件。
- CDDIS 路径 `gnss/data/daily/YYYY/DDD/YYd/`；cacsa `YYDDD/YYd/`；ign 加 `data_30/`；其它 `根/YYYY/DDD/`。

## 6. 坑（全部本机复现）

1. **漏装 requests**：见 §2。
2. **退出码永远 0**：404、SSL 错、FTP 425 都只打印；脚本化必须自己检查 `DIR/YYYY/DDD/` 里有没有文件、`gzip -t` 能否通过。
3. **`-login` 必崩**：`_, _, host, r_path = read.get_center(...)` 解 4 个值，函数返回 5 个 → `ValueError: too many values to unpack (expected 4)`。ramsac_hr 又强制要 `-login`，所以这个中心实际不可用。
4. **`-rename` 不是格式转换**：`DLF100NLD_…crx.gz` 被改名成 `dlf12000.26d.gz`，解开第一行仍是 `3.0 COMPACT RINEX FORMAT`。GAMIT 需要真正的 RINEX 2 时还得自己转。
5. **镜像脚本找不到 lftp**：`get_path_lftp()` 只在设置了 `CONDA_PREFIX` 时才去 PATH 找，否则直接 `RuntimeError: No lftp found`（README 说系统 lftp 也行，实际不行）。
6. **镜像脚本 `-P` 传错**：`clone.mirror(user, passw, url, remote_dir, ldir, remote_dir, …)` 第 6 个位置参数本该是并行数。用假 lftp 截到的命令是 `mirror -P /pub/data/2026/200 --verbose … --include data_30 /pub/data/2026/200 M`，`-P` 后面本应是并行数（默认 10），这里却塞进了远端路径（真 lftp 未测）。成败只写进当前目录的 `clone_YYYYMMDD.log`（`Mirror completed` / `Mirror failed`），终端**无论成败都打印 `-- Cloned N seconds`**，别只看这一行。
7. **ARGN 假成功**：`data_center.dat` 把主机写成 `https://ga-gnss-data-rinex-v1.s3.amazonaws.com/index.html#public`，`#` 后面是 URL 片段不发给服务器，结果每个文件都拿到同一张 S3 网页。正确地址是 `https://…s3.amazonaws.com/public/daily/2026/200/ALIC00AUS_R_20262000000_01D_30S_MO.crx.gz`（curl `-I` 返回 200）。
8. **RENAG 候选名越试路径越乱**：RINEX 3 分支在循环里反复切 `r_path`，第二个候选变成 `/pub/rinex3x3/2026/20/`，第三个 `/pub/rinex3x3x3/2026/`。只有第一个候选（`_R_…_30S_`）是对的，站点只有 15 s 或 `_S_` 文件时找不到。
9. **`-hrate` 配 9 位站名**：`UnboundLocalError: … 'lrinex'`；配表外中心（如 cddis）：`UnboundLocalError: … 'path_hr'`。
10. **错误信息误导**：CDDIS 分支把任何异常（含 `425 Bad IP`）都打印成 `No such file or directory`，并写进 `dwnl_error_YYYYMMDD.log` 当成 “Not found”。日志和临时文件都落在**当前目录**，不在 `-dir` 下；HTTP 中心失败不写日志。
11. `sopac` 用明文 http；`https://garner.ucsd.edu` 在本机 curl 报证书错误（exit 60），所以别自己改成 https。

## 7. 接到哪一步

下载 → [hatanaka](./hatanaka.md) / [crx2rnx](./crx2rnx.md) 解 CRINEX → [georinex](./georinex.md) 读 → [gnss-tec](./gnss-tec.md) 等算 TEC。需要校验和的欧洲站用 [epos-glass-api](./epos-glass-api.md)；只要 IGS 站用 [gnss-obs-mirrors](./gnss-obs-mirrors.md) 更省事。

## 8. 选型一句话

grinq 的价值是 `data_center.dat` 里二十来个国家/区域网的**路径格式**，拿来参考或打补丁后批量备数合适；原样用于生产要先修 §6 的 1、3、5–8。
