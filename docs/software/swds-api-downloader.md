# swds-api-downloader · INPE/EMBRACE Space Weather Data Share API 下载样例操作手册

目录：[`PROJECTS.json` → `swds-api-downloader`](../../PROJECTS.json) · 上游 <https://github.com/embrace-inpe/swds-api-downloader> · 许可 **MIT** · tip **`f4a4f40`**（2019-04-02）· ★**4** · README 徽章 **1.0.3** · **无 PyPI** · 纯标准库（`urllib`/`getopt`），`requirements.txt` 只有 `coverage==4.5.2`（跑测试用）· 本机验证（2026-09-26 00:31–00:35 EDT，Python **3.13.5**）：`-h` / 缺 `-p` / 长旗标 bug 均复现；真实下载 → **`SwdsError: The variable host is not a valid URL`**（exit **1**）；根因 = 硬编码 host 已 **302→HTTPS**、证书链缺中间证书，`-k` 绕过后 `/api/auth/login/` 与 `/api/files/` 均 **404** → **API 已下线，脚本事实失效**；替代：公开目录 **<https://embracedata.inpe.br/>**（证书正常，`sjc23apr.17m` 与 `INPE2660.26I` 实拉成功）· **质检复跑**（2026-09-26 00:42–00:43 EDT）：tip `f4a4f40` 未变；exit **1/3/2/1**、`helpers.py:101` 漏逗号、`login`/`files` **404**、`Verify return code: 21`、unittest **16** 跑 **3** errors、`sjc23apr.17m` **66747** B/**1045** 行/止于 17:20、`INPE2660.26I` **1264319** B/144 图——全部复现；修 2 处：门户 200 需 `-k`、`error.log` 实为建空文件

> 岗位：给 EMBRACE/INPE（巴西空间天气计划）账号用户写的 **API 批下样例**——按 application/station/resolution 等整数 ID 查文件表、带 Bearer token 下载。冲突时：**上游 README / INPE 公告 > 本文**。

## 1. 用途与边界

**做（设计上）：**

1. `POST {host}/api/auth/login/`（表单 `username`/`password`）→ JSON `token`
2. `GET {host}/api/files/?application=…&start_date=…&end_date=…` + `Authorization: Bearer <token>` → 文件 JSON 列表（每项含 `url`）
3. 逐个 `GET url` → 按 URL 第 8 段起的路径落盘到 `-p` 目录；失败写 `./error.log`

**不做：**

- **不是** GNSS 观测（RINEX）下载器 → [gampii-good](./gampii-good.md) / [fast](./fast.md) / [data-access](../data-access.md)
- **不是** 闪烁 ISMR 下载 → [ismr-downloader](./ismr-downloader.md)（UNESP）
- **不** 解析磁力计 / IONEX / 闪烁文件 → IONEX 见 [ionex-gim](./ionex-gim.md)
- **不** 注册账号；无重试、无断点续传、无并发

一句话：**2019 年的官方 API 调用示范，接口已 404；今天要数据请直接走 embracedata 目录（§4）。**

| 术语 | 含义 |
| --- | --- |
| SWDS | Space Weather Data Share，EMBRACE 数据共享 API |
| `application` | 数据类别整数 ID；README 示例 `1`=磁力计（`./tmp/magnetometer/`），`settings.py` 默认 `2`+`swfilter 7`=全天空成像仪（`./tmp/imager/`）|
| 其余 ID | station / resolution / swfilter / swtype / network / equipment；**ID 对照表仓内没有**，原在门户里查 |
| `error.log` | `log_config()` 在**当前工作目录**追加 ERROR 级日志 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/embrace-inpe/swds-api-downloader.git
cd swds-api-downloader
git log -1 --format='%h %ci'     # 期望 f4a4f40 2019-04-02 10:08:40 -0300
python3 swds-downloader.py -h    # 无第三方依赖
```

凭据只能写进 `settings.py`（无环境变量 / 无 CLI 旗标）：

```python
USERNAME = 'you@example.org'   # 用户名或邮箱
PASSWORD = '********'
```

> 别把填了密码的 `settings.py` 提交回 git；`.gitignore` 不含它。

## 3. 端到端（本机真跑）

### 3.1 帮助

```bash
python3 swds-downloader.py -h; echo "exit=$?"
```

```text
2026-09-26 04:31:38 INFO: 
    -h -H --help = Show the helper text with the avaliables options
    ** Filters
    -a --app = An integer Application ID (Required)
    -s --station = An integer Station ID (Optional)
    -r --resolution = An integer  Resolution ID (Optional)
    -f --swfilter = An integer  SwFilter ID (Optional)
    -t --swtype = An integer  SwType ID (Optional)
    -n --network = An integer  Network ID (Optional)
    -q --equipment = An integer  Equipment ID (Optional)
    ** Dates
    -i --start_date = A string with format yyyy-mm-dd (Required)
    -e --end_date = A string with format yyyy-mm-dd (Required)
    ** Path to save the files
    -p --path = A string with the a absolute path to save the files (Required)
exit=1
```

（空行已压缩；时间戳是 logging 的本机时区，本机容器为 UTC = 00:31 EDT。`-h` 退出码是 **1** 不是 0。）

### 3.2 缺 `-p`

```bash
python3 swds-downloader.py -a 1 -i 2017-04-01 -e 2017-04-23; echo "exit=$?"
```

```text
2026-09-26 04:31:38 INFO: It needs a path to save. Use -p or --path to pass your custom path to save the files
exit=3
```

### 3.3 长旗标 bug

```bash
python3 swds-downloader.py --app 1 --start_date 2017-04-01 -e 2017-04-02 -p ./tmp/m; echo "exit=$?"
```

```text
2026-09-26 04:31:38 INFO: option --start_date not recognized
exit=2
```

源码 `src/utils/helpers.py` 里 `"equipment="` 与 `"start_date="` 之间**漏逗号**，被 Python 拼成一个 `"equipment=start_date="`：**`--equipment` 和 `--start_date` 都坏**。一律用短旗标 `-q` / `-i`。

### 3.4 README 原样示例（真实下载）

```bash
python3 swds-downloader.py -a 1 -i 2017-04-01 -e 2017-04-23 -r 1 -s 1 -p ./tmp/magnetometer/; echo "exit=$?"
```

```text
SwdsError: The variable host is not a valid URL e.g: "http://apidomain.com"
exit=1
```

- 构造函数先 `urlopen(host)` 探活，失败就报这句——**先于**凭据检查，所以空账号也是这条错
- 没有联网请求 `/api/*`，**没有数据文件落盘**；`log_config()` 仍会在 cwd 建一个 **0 B** 的 `error.log`（质检复测），里面无内容（`SwdsError` 走 `sys.exit`）

### 3.5 定位根因

```bash
H=http://www2.inpe.br/climaespacial/SpaceWeatherDataShare
curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -L --max-time 15 $H
curl -sk -o /dev/null -w '%{http_code}\n' --max-time 15 https://www2.inpe.br/climaespacial/SpaceWeatherDataShare/api/auth/login/
curl -sk -o /dev/null -w '%{http_code}\n' -X POST -d 'username=x&password=y' --max-time 15 https://www2.inpe.br/climaespacial/SpaceWeatherDataShare/api/auth/login/
python3 -c "import urllib.request as u; u.urlopen('$H', timeout=15)"
```

本机结果：

| 探测 | 结果 |
| --- | --- |
| `http://…/SpaceWeatherDataShare` | **302** → `https://…`，随后 curl `000`（`SSL certificate problem: unable to get local issuer certificate`）|
| `openssl s_client` | `CN=*.inpe.br`，issuer `RNP ICPEdu GR46 OV TLS CA 2025`，**Verify return code: 21**（服务器没发中间证书）|
| `-k` GET `/api/auth/login/`、`/api/files/` | **404** |
| `-k` POST login | **404** |
| Python `urlopen` | `URLError … CERTIFICATE_VERIFY_FAILED` → 被包装成上面的 `SwdsError` |
| `https://www2.inpe.br/climaespacial/portal/` | 校验证书 → `000`（同一 `unable to get local issuer certificate`）；`-k` → **200**（门户本身在，SWDS 路径没了；质检 2026-09-26 00:43 EDT 复测）|

结论：**两层墙**——TLS 链不全（可绕）+ API 路径 404（绕不过）。改 `host` 或关证书校验都拿不到文件，**不要**为此在代码里关 SSL 校验。

### 3.6 自带测试

```bash
python3 -m unittest discover 2>&1 | tail -3
```

```text
Ran 16 tests in 2.634s

FAILED (errors=3)
```

13 个离线用例（参数解析 / 变量校验 / query 拼接）通过；3 个联网用例 `test_get_files_list` / `test_login` / `test_token_format` 失败于同一个 `CERTIFICATE_VERIFY_FAILED → SwdsError`。`runtests.py` 另需 `pip install coverage`。

## 4. 能用的替代：embracedata 公开目录（本机实拉）

`https://embracedata.inpe.br/` 是 Apache 目录索引，证书校验正常（`ssl_verify_result=0`），**无需账号**。顶层：`amap/ callisto/ gtex/ imager/ ionex/ ionosonde/ ksa/ lidar/ magnetometer/ riometer/ scintillation/`。

```bash
# README 例子里那份磁力计文件
curl -s -o sjc23apr.17m -w '%{http_code} %{size_download}B\n' \
  https://embracedata.inpe.br/magnetometer/SJC/2017/sjc23apr.17m
head -5 sjc23apr.17m
```

```text
200 66747B
SAO JOSE DOS CAMPOS UNIVAP-01 <113> 1 Min. Reported data

 DD MM YYYY  HH MM   D(Deg)  H(nT)   Z(nT)   I(Deg)   F(nT)

 23 04 2017  00 00  -21.3892 18108.3 -14137.0 -37.9787 22973.1
```

该文件 **1045 行**，最后一行 `23 04 2017  17 20`——当天数据只到 17:20，不是完整 1440 分钟，用前自己查缺口。

```bash
# EMBRACE 区域 TEC 图（IONEX 1.0）
curl -s https://embracedata.inpe.br/ionex/2026/ | grep -o 'INPE[0-9]*\.26I' | sort -u | tail -1
curl -s -O https://embracedata.inpe.br/ionex/2026/INPE2660.26I
head -3 INPE2660.26I
```

```text
INPE2660.26I
     1.0            IONOSPHERE MAPS     GPS                 IONEX VERSION / TYPE
TECMAP App          EMBRACE / INPE      24-Sep-26 18:03     PGM / RUN BY / DATE 
  2026     9    23     0     0     0                        EPOCH OF FIRST MAP  
```

大小 **1264319 B**；头里 `INTERVAL 600`、`# OF MAPS IN FILE 144`（10 min 一幅）、`MAPPING FUNCTION NONE`。读法见 [ionex-gim](./ionex-gim.md)。

批量拉一个站一个年份（目录镜像；**本机 48 s 内未跑完即中断，未核对落盘数**——大目录请先用 `curl … | grep -o` 列文件名再逐个下）：

```bash
wget -r -np -nH -R 'index.html*' -A '*.17m' \
  https://embracedata.inpe.br/magnetometer/SJC/2017/
```

`scintillation/stations/` 下按年 `2013/`…`2026/`，附 `readme_scintillation.html`。

## 5. 参数与输出路径

| 短旗标 | 键 | 必需 | 备注 |
| --- | --- | --- | --- |
| `-a` | application | 是（逻辑上） | getopt 不强制；缺了照样发请求 |
| `-i` / `-e` | start_date / end_date | 是 | `yyyy-mm-dd`，不校验格式 |
| `-p` | 保存目录 | **强制** | 缺 → exit 3；自动补尾 `/` |
| `-s -r -f -t -n -q` | station / resolution / swfilter / swtype / network / equipment | 否 | 值为假（空/None）时不进 query |

- 无参数运行 → 读 `settings.SEARCH` + `PATH_TO_SAVE`（默认 `./tmp/imager/`）
- 落盘路径 = `-p` + 文件 URL 去掉前 7 段后的路径，如 README 示例 `./tmp/magnetometer/SJC/2017/sjc23apr.17m`
- 单文件超时 30 s；失败计数写 `error.log`，**进程仍 exit 0**

## 6. 坑

| # | 现象 | 原因 / 处理 |
| ---: | --- | --- |
| 1 | `SwdsError: … not a valid URL` | 构造时 `urlopen(host)` 失败；今天 = TLS 链不全 + API 404 |
| 2 | 以为是凭据问题 | host 检查在凭据检查**之前**；空账号也先报 host |
| 3 | `--start_date` / `--equipment` not recognized | 漏逗号 bug，用 `-i` / `-q` |
| 4 | `-h` exit 1 | 脚本里 `-h` 就是 `sys.exit(1)`；CI 别把它当失败 |
| 5 | 凭据泄露 | 只能写 `settings.py`；改完勿 commit |
| 6 | 整数 ID 不知道填什么 | 仓内无对照表；原门户已不可达 → 改用 §4 目录按名字找 |
| 7 | 部分文件失败但 exit 0 | 只看末尾 `Download failed:` 与 `error.log` |
| 8 | `error.log` 出现在奇怪位置 | 写在**当前工作目录**，不是 `-p` 目录 |
| 9 | 磁力计日文件不满一天 | 例 `sjc23apr.17m` 止于 17:20；按时间列核对 |
| 10 | 想关 SSL 校验硬跑 | 没用：路径 404；也不应在科研脚本里关校验 |

## 7. 选型

| 需求 | 用 |
| --- | --- |
| EMBRACE 磁力计 / 成像仪 / IONEX / 闪烁 / 测高仪文件 | **§4 embracedata 目录** + `wget`/`curl` |
| 巴西 ISMR 闪烁（UNESP） | [ismr-downloader](./ismr-downloader.md) |
| 全球测高仪 foF2 | [ionosonde-data-downloader](./ionosonde-data-downloader.md) |
| IONEX 读图 | [ionex-gim](./ionex-gim.md) |
| INPE 周跳工具（同组织） | [cycle-slip-correction](./cycle-slip-correction.md) |
| 本脚本 | 仅当 INPE 重新上线 SWDS API 时；先 `curl` 看 `/api/auth/login/` 是否不再 404 |
