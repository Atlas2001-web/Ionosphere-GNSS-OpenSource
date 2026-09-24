# viresclient · ESA VirES Python 客户端操作手册

目录：[`PROJECTS.json` → `viresclient`](../../PROJECTS.json) · 上游 <https://github.com/ESA-VirES/VirES-Python-Client> · PyPI **`viresclient`** · 许可 **MIT** · 本机 **0.16.0**（tip `c00f81d` / ★**23**）· 验证（2026-09-24 07:22 EDT；**质检复跑 07:28 EDT**）：`pip`→CLI `--help`；无 ini → `show_configuration` **ERROR**；`SwarmRequest()`→**ValueError**（缺 URL）；`SwarmRequest(ows)` 可构造且 `available_collections` 通；`get_between`→**AuthenticationError**（WPS **403**）；`available_measurements("TEC")` 含 **Absolute_VTEC**；裸名 `TEC`→Exception；**无真实账号未落盘 xarray**

> 岗位：从 **VirES for Swarm**（及 Aeolus）按需拉测值/模型/辅助量 → `pandas` / `xarray`。冲突时：**上游 README / ReadTheDocs > 本机 `viresclient -h` > 本文**。网页 GUI → <https://vires.services>；配方笔记本 → <https://notebooks.vires.services>。

## 1. 用途与边界

**做：**

- Python API：`SwarmRequest` / `AeolusRequest`；服务器端切片 + 模型评估
- CLI：`set_token` / `set_default_server` / `show_configuration` / `clear_credentials` / 上传相关子命令
- 常用 Swarm 产品：MAG/EFI/**TEC**/FAC/IBI…（见 `available_collections` / handbook）
- 输出：`ReturnedData.as_dataframe()` / `.as_xarray()`

**不做：**

- **不** 免账号——须在 <https://vires.services> 注册并复制 **access token**（本机未持凭证，**不臆造成功 stdout**）
- **不** 替代地面测高仪 / IONEX GIM → [ionosonde-data-downloader](./ionosonde-data-downloader.md) / [ionex-gim](./ionex-gim.md) / [geospacelab](./geospacelab.md)
- **不** 拉 IGS RINEX / CDDIS → [fast](./fast.md) / [cddis-highrate-downloader](./cddis-highrate-downloader.md) / [data-access](../data-access.md)
- **不** 做 ROTI/闪烁指标 → [oasis-roti](./oasis-roti.md) / [ismr-downloader](./ismr-downloader.md)

一句话：**有 token 后的 Swarm/Aeolus 科研切片客户端**（Langmuir/TEC 等进 xarray）。

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
# 期望：
# usage: viresclient [-h] <command> ...
# ...
#     set_token           Set an access token for the given server URL.
#     show_configuration  Print the configuration to standard output.
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
