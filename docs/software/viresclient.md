# viresclient · ESA VirES Python 客户端操作手册

目录：[`PROJECTS.json` → `viresclient`](../../PROJECTS.json) · 上游 <https://github.com/ESA-VirES/VirES-Python-Client> · PyPI **`viresclient`** · 许可 **MIT** · 本机 **0.16.0**（tip `c00f81d` / ★**23**）· 验证（2026-09-24 07:22 EDT；**质检复跑 07:28 EDT**）：`pip`→CLI `--help`；无 ini → `show_configuration` **ERROR**；`SwarmRequest()`→**ValueError**（缺 URL）；`SwarmRequest(ows)` 可构造且 `available_collections` 通；`get_between`→**AuthenticationError**（WPS **403**）；`available_measurements("TEC")` 含 **Absolute_VTEC**；裸名 `TEC`→Exception；**无真实账号未落盘 xarray**

> **质检复跑通过（2026-09-26 05:02–05:04 EDT，viresclient 0.16.0 / tip `c00f81d`，Python 3.13 + pandas 3.0.6）**：无 ini `show_configuration` ERROR exit 1、`SwarmRequest()` ValueError、OWS MAG 10 min `AuthenticationError`（日志 WPS 403）、`available_measurements("TEC")` 前 8 项与 `Absolute_VTEC`、裸名 `TEC` Exception 逐字一致；`available_collections` 匿名可用（76 个）。**已修**：原文称 VirES 无匿名途径——实测 OWS 无 token 403，但 **VirES HAPI 匿名 200**（catalog 174 / `SW_` 147），新增 §3.4 真实 curl 与输出、失败表 3 行、本机记录 2 行；`--help | head -8` 期望改为真实前 8 行（不含 show_configuration）。未复跑：带 token 的 xarray 落盘、Aeolus。

> 岗位：从 **VirES for Swarm**（及 Aeolus）按需拉测值/模型/辅助量 → `pandas` / `xarray`。冲突时：**上游 README / ReadTheDocs > 本机 `viresclient -h` > 本文**。网页 GUI → <https://vires.services>；配方笔记本 → <https://notebooks.vires.services>。

## 1. 用途与边界

**做：**

- Python API：`SwarmRequest` / `AeolusRequest`；服务器端切片 + 模型评估
- CLI：`set_token` / `set_default_server` / `show_configuration` / `clear_credentials` / 上传相关子命令
- 常用 Swarm 产品：MAG/EFI/**TEC**/FAC/IBI…（见 `available_collections` / handbook）
- 输出：`ReturnedData.as_dataframe()` / `.as_xarray()`

**不做：**

- **本客户端不能免账号**——viresclient 走 OWS/WPS（`/ows`），无 token 一律 **403**；须在 <https://vires.services> 注册并复制 **access token**（本机未持凭证，**不臆造成功 stdout**）。
- **但 VirES 并非全无匿名入口**：**VirES HAPI**（`https://vires.services/hapi/`）**匿名可用**，catalog 174 个数据集（其中 `SW_` 147 个），能按时段/变量切 CSV/JSON——只要几个变量、不需模型评估时直接 curl，见 §3.4 与 [swarm-data](./swarm-data.md)。
- **不** 替代地面测高仪 / IONEX GIM → [ionosonde-data-downloader](./ionosonde-data-downloader.md) / [ionex-gim](./ionex-gim.md) / [geospacelab](./geospacelab.md)
- **不** 拉 IGS RINEX / CDDIS → [fast](./fast.md) / [cddis-highrate-downloader](./cddis-highrate-downloader.md) / [data-access](../data-access.md)
- **不** 做 ROTI/闪烁指标 → [oasis-roti](./oasis-roti.md) / [ismr-downloader](./ismr-downloader.md)

一句话：**有 token 后的 Swarm/Aeolus 科研切片客户端**（Langmuir/TEC 等进 xarray）；无 token 只想拿测值 → VirES HAPI（§3.4）。

| 术语 | 含义 |
| --- | --- |
| VirES | Virtual environments for Earth Scientists（EOX 代 ESA 运维） |
| OWS | WPS 端点；请求用 `https://vires.services/ows`（配置里常写站点根 `https://vires.services`） |
| token | 网页账户 → Access Token；写入 `~/.viresclient.ini` |
| collection | 如 `SW_OPER_TECATMS_2F`（Swarm-A TEC） |
| measurement | 集合内变量；**不是**集合缩写本身（`TEC` 集合里是 `Absolute_VTEC`/`Absolute_STEC`…） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install 'viresclient==0.16.0'
viresclient --help | head -n 8
python -c "import importlib.metadata as m; print(m.version('viresclient'))"
# 期望（前 8 行里还看不到 show_configuration，要看全用 viresclient --help）：
# usage: viresclient [-h] <command> ...
#
# positional arguments:
#   <command>
#     set_token           Set an access token for the given server URL.
#     remove_server       Remove any stored configuration for the given server
#                         URL.
#     set_default_server  Set the default server URL.
# 0.16.0
```

源码：

```bash
git clone --depth 1 https://github.com/ESA-VirES/VirES-Python-Client.git
cd VirES-Python-Client
# tip 本机：c00f81d
python -m pip install -e .
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `viresclient: not found` | 未进 venv | `which python`；重装 |
| `Configuration file … does not exist` | 尚未 `set_token` | 先配 token（下节） |
| `No matching distribution` | Python 过旧 | 用 3.9+（本机 3.13 OK） |

## 3. 端到端：token → 探测 → 拉取（本机部分真跑；质检复跑 2026-09-24 07:28 EDT）

### 3.1 注册与写入 token（必须）

1. 打开 <https://vires.services> → 注册 / 登录  
2. 账户页复制 **Access Token**（勿提交到本仓库）  
3. 本机：

```bash
source ~/iono_ops/.venv/bin/activate
viresclient set_default_server https://vires.services
viresclient set_token https://vires.services 'YOUR_TOKEN_HERE'
viresclient show_configuration
# 期望类似：
# [default]
# url = https://vires.services
#
# [https://vires.services]
# token = …（脱敏）
```

清凭证：`viresclient clear_credentials`（删 `~/.viresclient.ini`）。

### 3.2 无配置 / 无 token（本机真 stdout）

```bash
# 无 ~/.viresclient.ini
viresclient show_configuration
# 期望：
# ERROR: Configuration file /home/…/.viresclient.ini does not exist!

python - <<'PY'
from viresclient import SwarmRequest
try:
    SwarmRequest()
except Exception as e:
    print(type(e).__name__ + ':', e)
PY
# 期望：
# ValueError: The URL must be provided when no default URL is configured.
```

显式 OWS、仍无 token：

```bash
python - <<'PY'
from viresclient import SwarmRequest
r = SwarmRequest("https://vires.services/ows")
r.set_collection("SW_OPER_MAGA_LR_1B")
r.set_products(measurements=["F"], sampling_step="PT60S")
try:
    r.get_between("2014-01-01T00:00", "2014-01-01T00:10")
except Exception as e:
    print(type(e).__name__ + ':', str(e).splitlines()[0])
PY
# 期望（节选）：
# AuthenticationError: Perhaps credentials are missing or invalid.
# （日志可含：ERROR WPS10Service: 403 POST https://vires.services/ows …）
```

### 3.3 测量名陷阱（本机真跑；假 token 亦可撞上）

```bash
python - <<'PY'
from viresclient import SwarmRequest
r = SwarmRequest("https://vires.services/ows")
r.set_collection("SW_OPER_TECATMS_2F")
print(r.available_measurements("TEC")[:8])
# 期望含：
# ['GPS_Position', 'LEO_Position', 'PRN', 'L1', 'L2', 'P1', 'P2', 'S1', ...]
# 以及 Absolute_VTEC / Absolute_STEC 等——没有裸名 'TEC'
try:
    r.set_products(measurements=["TEC"], sampling_step="PT60S")
except Exception as e:
    print(type(e).__name__ + ':', str(e).splitlines()[0][:160])
PY
# 期望：
# Exception: Measurement 'TEC' not available for collection 'TEC'. Check available with SwarmRequest.available_measurements(TEC)
```

### 3.4 无 token 的替代：VirES HAPI（匿名，本机真跑 2026-09-26 05:03 EDT）

同一服务器上：OWS 无 token 直接 403，HAPI 匿名 200。

```bash
curl -s -o /dev/null -w 'OWS %{http_code}\n' "https://vires.services/ows?service=WPS&request=GetCapabilities"
curl -s -w '  HTTP %{http_code}\n' "https://vires.services/hapi/capabilities"
curl -s "https://vires.services/hapi/catalog" | python3 -c "import sys,json;c=[x['id'] for x in json.load(sys.stdin)['catalog']];print('catalog',len(c),'SW_',sum(x.startswith('SW_') for x in c))"
curl -s "https://vires.services/hapi/info?dataset=SW_OPER_TECATMS_2F" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['startDate'],d['stopDate'],d.get('x_maxTimeSelection'))"
curl -s -w '# HTTP %{http_code} %{size_download} B\n' "https://vires.services/hapi/data?dataset=SW_OPER_TECATMS_2F&parameters=PRN,Absolute_VTEC,Elevation_Angle&start=2016-01-01T00:00:00Z&stop=2016-01-01T00:00:20Z&format=csv"
```

```text
OWS 403
{"HAPI": "3.0", "status": {"code": 1200, "message": "OK"}, "outputFormats": ["csv", "json", "binary", "x_binary"]}  HTTP 200
catalog 174 SW_ 147
2013-11-25T10:59:54Z 2026-09-20T23:59:59Z P5D
2016-01-01T00:00:01.000Z,8,3.4900060223,23.250534995986733
2016-01-01T00:00:01.000Z,13,2.9273573878,53.465606836477754
2016-01-01T00:00:01.000Z,15,6.27390252,56.59416258351794
2016-01-01T00:00:01.000Z,30,2.640739938,27.087393924322857
…（共 80 行：19 个历元；PRN 8/13/15/30 各 19 行 + PRN 10 仅 4 行；列序 = Timestamp,PRN,Absolute_VTEC,Elevation_Angle，无表头）
2016-01-01T00:00:19.000Z,30,2.5500180043,27.182748392841035
# HTTP 200 4802 B
```

磁场同样可取：`dataset=SW_OPER_MAGA_LR_1B&parameters=F&start=2014-01-01T00:00:00Z&stop=2014-01-01T00:00:03Z` → `2014-01-01T00:00:00.000Z,22867.48` 起 3 行。HAPI 的限制：**没有模型评估/auxiliaries**（CHAOS、QDLat 要走 viresclient+token）；单次时长有上限（TECATMS `x_maxTimeSelection`=P5D，超了 `1408 too much time or data requested` HTTP 400）；变量名同样不能写 `TEC`（`1407 … invalid parameter TEC`，HTTP 404）。更多数据集/对账见 [swarm-data](./swarm-data.md)。

有真实 token 后的最小 Swarm TEC 切片（**模板**；本机未跑通落盘）：

```python
from viresclient import SwarmRequest

request = SwarmRequest()  # 依赖 set_default_server + set_token
request.set_collection("SW_OPER_TECATMS_2F")
request.set_products(
    measurements=["Absolute_VTEC", "Absolute_STEC", "Elevation_Angle"],
    auxiliaries=["QDLat", "QDLon"],
    sampling_step="PT60S",
)
data = request.get_between("2016-01-01T00:00", "2016-01-01T01:00")
ds = data.as_xarray()
print(ds)
# 成功时：xarray.Dataset，维含 Timestamp；变量含 Absolute_VTEC 等
# （具体数值随服务器与滤波变化——以本机为准，勿抄本文臆造）
```

磁场示例见上游 README（`SW_OPER_MAGA_LR_1B` + `F`/`B_NEC` + `CHAOS-Core`）。

## 4. 常用标志 / 字段

| API / CLI | 作用 |
| --- | --- |
| `set_collection(...)` | 单一集合（多集合见文档 `set_collections`） |
| `set_products(measurements=, models=, auxiliaries=, sampling_step=)` | 变量与抽样；`PT10S`/`PT60S` 等 ISO-8601 |
| `get_between(start_time, end_time)` | 拉取；返回 `ReturnedData` |
| `available_measurements("TEC")` 等 | 查合法变量名 |
| `viresclient set_token SERVER TOKEN` | 写入 ini |
| `viresclient set_default_server URL` | 无参 `SwarmRequest()` 需要 |

## 5. 失败排查

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `AuthenticationError` / WPS **403** | 无 token / token 失效 | 网页重发 token → `set_token` |
| `ValueError: The URL must be provided…` | 无 default server | `set_default_server https://vires.services` 或构造时传 OWS URL |
| `Measurement 'TEC' not available` | 把集合名当测量名 | `available_measurements("TEC")` → 用 `Absolute_VTEC` 等 |
| WPS **400** + 长时间重试 | URL 写成站点根而非 `/ows`，或请求非法 | 用 `…/ows`；缩小时段；先查 available_* |
| 仅网页能下、脚本 403 | token 绑错站点（Swarm vs Aeolus） | Swarm → `vires.services`；Aeolus → `aeolus.services` |
| 没有 token，也不需要模型 | viresclient 必须 token | 改用匿名 VirES HAPI `https://vires.services/hapi/data?dataset=…&parameters=…&start=…&stop=…&format=csv`（§3.4） |
| HAPI `1408 too much time or data requested`（HTTP 400） | 超 `x_maxTimeSelection`（TEC P5D） | 按 `/hapi/info` 的上限分段 |
| HAPI `1407 … invalid parameter`（HTTP 404） | 变量名错（如 `TEC`） | 查 `/hapi/info?dataset=…` 的 `parameters` |
| 想清掉本机密钥 | — | `viresclient clear_credentials` |

## 6. 交叉

- 空间天气多源图：[geospacelab](./geospacelab.md)
- 地面测高仪参数：[ionosonde-data-downloader](./ionosonde-data-downloader.md)
- GNSS TEC 观测链：[gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) / [ionex-gim](./ionex-gim.md)
- 数据入口总表：[data-access](../data-access.md)
- 教程：[04](../tutorials/04-iri-nequick.md) / [05](../tutorials/05-scintillation-roti.md) / [20](../tutorials/20-storm-tec-analysis.md)

## 7. 本机记录

| 项 | 值 |
| --- | --- |
| PyPI | **0.16.0** |
| tip | **`c00f81d`** |
| 星标 | **23** |
| 无 ini `show_configuration` | `ERROR: Configuration file … does not exist!` |
| 无 default `SwarmRequest()` | `ValueError: The URL must be provided…` |
| 无 token + OWS MAG 10 min | `AuthenticationError`（WPS **403**） |
| `available_measurements("TEC")` 前几项 | `GPS_Position`, `LEO_Position`, `PRN`, `L1`, `L2`, `P1`, `P2`, `S1`… |
| 假测量名 `TEC` | `Exception: Measurement 'TEC' not available for collection 'TEC'` |
| 成功 xarray | **未跑**（无真实 token） |
| OWS GetCapabilities 无 token | **403** |
| VirES HAPI 匿名 | catalog **174**（`SW_` **147**）；TECATMS 20 s → **80 行 / 4802 B**，首行 PRN 8 VTEC **3.4900060223** |
