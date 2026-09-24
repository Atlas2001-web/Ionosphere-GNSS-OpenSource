# earthscope-sdk · EarthScope GAGE/SAGE API Python SDK 操作手册

目录：[`PROJECTS.json` → `earthscope-sdk`](../../PROJECTS.json) · 上游 <https://gitlab.com/earthscope/public/earthscope-sdk> · 文档 <https://docs.earthscope.org/sdk> · 许可 **Apache-2.0** · PyPI **1.9.2** · tip **`4ba8870`** · GitLab ★**4** · 捆 CLI **earthscope-cli 1.2.0** · 本机验证（2026-09-24 07:29 EDT）：`pip install` → `earthscope_sdk` **1.9.2**；`EarthScopeClient()` 可建；`get_profile`/`plan()`/`fetch()` → **`NoRefreshTokenError`**；`es user get-profile` → *No tokens found…*；`client.data` 无 `[arrow]` → **`ModuleNotFoundError: pyarrow`**；装 `[arrow]` 后可见 `gnss_observations` / `gnss_ephemeris_positions` / `gnss_instantaneous_positions`；**无账号未落盘 Arrow 表**

> 岗位：以官方 SDK/CLI 访问 EarthScope（原 UNAVCO/IRIS → **GAGE/SAGE**）用户档案、GNSS 观测切片与 dropoff。冲突时：**上游 docs.earthscope.org / README > 本文**。免费账号注册：<https://www.earthscope.org/user>。

## 1. 用途与边界

**做：**

1. **`EarthScopeClient` / `AsyncEarthScopeClient`**：同步/异步；可用 `with` 自动 `close()`
2. **`client.user`**：`get_profile` / `get_user_id` / 临时 AWS 凭证（直连 S3）
3. **`client.data`**（需 **`earthscope-sdk[arrow]`**）：`gnss_observations` / `gnss_ephemeris_positions` / `gnss_instantaneous_positions` → **QueryPlan** → `.plan()` / `.fetch()` → **PyArrow Table**
4. **`client.discover`**：`list_*_datasources`（站/网/会话/流）
5. **`client.dropoff`**：对象上传/列表/历史（数据投递）
6. **同机 CLI `es`**：`login` / `logout` / `user get-profile` / `user get-refresh-token`；与 SDK **共用** `~/.earthscope` 凭证

**不做：**

- **不是** 匿名公开 FTP/RINEX 批下 → [gampii-good](./gampii-good.md) / [fast](./fast.md) / [gdds](./gdds.md) / [data-access](../data-access.md)
- **不是** CDDIS high-rate → [cddis-highrate-downloader](./cddis-highrate-downloader.md)
- **不是** Swarm/Aeolus VirES → [viresclient](./viresclient.md)
- **不** 解析本地 RINEX 文本 → [georinex](./georinex.md)；本 API 直接给观测切片
- **无 refresh token 时禁止臆造** Arrow 行数 / TEC / 站坐标

一句话：**官方账号门禁的 GAGE GNSS API 客户端**；本机无登录时只验证安装、CLI 与鉴权失败路径。

| 术语 | 含义 |
| --- | --- |
| QueryPlan | `gnss_observations(...)` 先返回计划对象（`unplanned`）；`.plan()`/`.fetch()` 才打 API |
| Device Code / SSO | `es login` 打开 `login.earthscope.org/activate?user_code=…` |
| `ES_OAUTH2__REFRESH_TOKEN` | 远程机注入 refresh token 的环境变量（敏感） |
| session_name | 观测会话名（教程常用 `"A"`） |
| edid / 4charid | EarthScope 站标识 / 四字符站码 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv es-sdk && source es-sdk/bin/activate
python -m pip install -U pip
# 基础（用户/发现/dropoff）
python -m pip install 'earthscope-sdk==1.9.2'
# GNSS 观测切片需要 Arrow 额外依赖
python -m pip install 'earthscope-sdk[arrow]'
# CLI（若未随依赖装上）
python -m pip install 'earthscope-cli==1.2.0'
es --version
# 期望：earthscope-cli/1.2.0 earthscope-sdk/1.9.2
python -c "import earthscope_sdk as es; print(es.__version__)"
# 期望：1.9.2
```

源码可编辑安装（对照 tip）：

```bash
git clone --depth 1 https://gitlab.com/earthscope/public/earthscope-sdk.git
cd earthscope-sdk
git rev-parse --short HEAD   # 本机 4ba8870
python -m pip install -e '.[arrow]'
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pyarrow'` 访问 `client.data` | 未装 `[arrow]` | `pip install 'earthscope-sdk[arrow]'` |
| `NoRefreshTokenError` / *No tokens found* | 未 `es login` | 浏览器 Device Code 登录；或设 `ES_OAUTH2__REFRESH_TOKEN` |
| `NoAccessTokenError` | 有配置无 access | `es user refresh-access-token` 或重新 `es login` |
| Python &lt; 3.10 | `requires-python >=3.10` | 换 3.10+ venv |

## 3. 端到端（本机真跑）

### 3.1 CLI 版本与未登录档案

```bash
es --version
es user get-profile
```

**本机 stdout：**

```text
earthscope-cli/1.2.0 earthscope-sdk/1.9.2
No tokens found for profile. To resolve, re-authenticate.
```

登录（有浏览器时；**本机未完成**，勿抄假 user_code）：

```bash
es login
# 期望打开 https://login.earthscope.org/activate?user_code=XXXX-XXXX
# 成功后：Successful login! Access token expires at …
es user get-profile
```

### 3.2 SDK：建客户端 + 鉴权失败

```bash
python - <<'PY'
from earthscope_sdk import EarthScopeClient
with EarthScopeClient() as client:
    print("client OK", type(client).__name__)
    print("attrs", [a for a in ("user", "discover", "dropoff", "data") if hasattr(client, a)])
    try:
        print(client.user.get_profile())
    except Exception as e:
        print(type(e).__name__ + ":", e)
PY
```

**本机 stdout（节选）：**

```text
client OK EarthScopeClient
attrs ['user', 'discover', 'dropoff', 'data']
NoRefreshTokenError: No refresh token was found. Please re-authenticate.
```

`get_user_id()` 同类：`NoAccessTokenError: No access token was found. Please re-authenticate.`

### 3.3 GNSS 观测 QueryPlan（无 token → plan/fetch 失败）

```bash
python - <<'PY'
from datetime import datetime, timezone
from earthscope_sdk import EarthScopeClient

with EarthScopeClient() as client:
    plan = client.data.gnss_observations(
        start_datetime=datetime(2025, 7, 20, 21, tzinfo=timezone.utc),
        end_datetime=datetime(2025, 7, 21, 3, tzinfo=timezone.utc),
        station_name="AC60",
        session_name="A",
    )
    print("lazy:", plan)  # 尚未打 API
    try:
        plan.plan()
    except Exception as e:
        print("plan():", type(e).__name__, e)
    try:
        table = plan.fetch()
        print(table)
    except Exception as e:
        print("fetch():", type(e).__name__, e)
PY
```

**本机 stdout：**

```text
lazy: GnssObservationsQueryPlan(unplanned)
plan(): NoRefreshTokenError No refresh token was found. Please re-authenticate.
fetch(): NoRefreshTokenError No refresh token was found. Please re-authenticate.
```

登录后官方教程形态（**有 token 时**；本机未跑，勿当本机数字）：

```python
table = client.data.gnss_observations(
    start_datetime=..., end_datetime=...,
    station_name="AC60", session_name="A",
).fetch()
# → PyArrow Table；可用 polars.from_arrow(table)
```

缺参时的真实 TypeError（本机）：

```text
TypeError: ... missing 2 required keyword-only arguments: 'start_datetime' and 'end_datetime'
```

### 3.4 discover（同样要 token）

```python
client.discover.list_station_datasources()
# → NoRefreshTokenError: No refresh token was found. Please re-authenticate.
```

## 4. 关键字段 / 参数（观测切片）

| 参数 | 说明 |
| --- | --- |
| `start_datetime` / `end_datetime` | **必填** `datetime`（建议带 tz） |
| `system` | `G/R/E/J/C/I/S` 或列表 |
| `satellite` / `obs_code` | 星号 / 观测码（如 `"7"` / `"1C"`） |
| `field` | `range` `phase` `doppler` `snr` `slip` `flags` `fcn` |
| `station_name` / `station_edid` | 站名或 edid |
| `session_name` / `network_name` | 会话 / 网名 |
| `roll` / `sample_interval` | 可选时间窗控制 |
| Plan 方法 | `.plan()` `.fetch()` `.group_by_day()` `.group_by_station()` `.with_timeout()` |

远程注入（摘要；**勿提交 token**）：

```bash
export ES_OAUTH2__REFRESH_TOKEN='<from: es user get-refresh-token>'
# 或 ~/.earthscope/config.toml → [profile.default] oauth2.refresh_token = "…"
```

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| 传统 IGS/CDDIS 文件备数 | [data-access](../data-access.md) / [gampii-good](./gampii-good.md) |
| RINEX → xarray | [georinex](./georinex.md) |
| Swarm TEC | [viresclient](./viresclient.md) |
| 测高仪 foF2 | [ionosonde-data-downloader](./ionosonde-data-downloader.md) |
| 爱尔兰国家网 RINEX 脚本 | [gnss-osi-download](./gnss-osi-download.md) |

## 6. 常见坑（≥8）

1. **无账号**：先 <https://www.earthscope.org/user>，再 `es login`
2. **`client.data` 缺 pyarrow**：必须 `[arrow]`；1.x 仍可硬依赖部分校验库，以 `pyproject` extras 为准
3. **懒计划**：`gnss_observations(...)` 打印 `unplanned` **不算**下载成功；以 `.fetch()` 为准
4. **同机凭证**：CLI 与 SDK 共享；容器需显式传 refresh token
5. **refresh token = 密码**：勿进 git / 聊天记录
6. **API 单会话/时长限制**：SDK 用 QueryPlan 扇出；大跨度用 `.group_by_day()` 控内存
7. **`es login` 无头环境**：Device Code 仍可在另一台浏览器完成；或预置 env
8. **勿与 CDDIS Earthdata `.netrc` 混为一谈**：两套账号体系
9. **本手册无 Arrow 行数**：无 token → **禁止伪造**观测 stdout
10. **dropoff / AWS**：需已登录且有相应权限；本机未测上传

## 7. 选型

| 需求 | 选 |
| --- | --- |
| EarthScope 官方切片 / 用户 API | **earthscope-sdk**（本页） |
| 全球 IGS 文件 FTP/HTTPS | [gampii-good](./gampii-good.md) / [data-access](../data-access.md) |
| ESA Swarm | [viresclient](./viresclient.md) |
| 国家 CORS 网页表单脚本 | [gnss-osi-download](./gnss-osi-download.md) |
