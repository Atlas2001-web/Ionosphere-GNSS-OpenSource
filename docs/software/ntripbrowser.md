# ntripbrowser · NTRIP 源表浏览 CLI/API 操作手册

目录：[`PROJECTS.json` → `ntripbrowser`](../../PROJECTS.json) · 上游 <https://github.com/emlid/ntripbrowser> · PyPI **`ntripbrowser` 4.0.0** · tip **`3730867`** · 许可 **BSD-3-Clause** · Python ≥3.11 · 依赖 `pycurl`/`cchardet`/`geopy`/`texttable`/`pager` · 本机验证（2026-09-24 05:45 EDT）：`get_mountpoints` → rtk2go STR **764** / igs-ip STR **384** / centipede STR **1269**；巴黎 50 km 过滤 **14** 站（`IPGP` dist≈**0.71** km）；**VALDM** 在表；**未订流**

> 岗位：拉 NTRIP caster **sourcetable**，CLI 表格查看 / Python 字典化挂载点（可选按坐标裁切）。冲突时：**本机 `ntripbrowser -h` / 上游 README > 本文**。订流/录 RTCM → [ntripstreams](./ntripstreams.md)/[ntrip-client](./ntrip-client.md)/[pygnssutils](./pygnssutils.md)；生产 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)；多流 GUI → [bnc](./bnc.md)。

## 1. 用途与边界

**做：**

- CLI：`ntripbrowser <host> [-p 2101] [-t SEC] [-c LAT LON] [-M KM]`
- API：`NtripBrowser(...).get_mountpoints()` → `{cas,net,str}` 字典列表
- 并行试 `http://host:port/`、`/sourcetable.txt`、https 同路径（`pycurl` multi）
- 可选：相对观测点距离列 + `maxdist` 裁剪

**不做：**

- **不是** NTRIP 订户 / 拉 RTCM 改正流（本页**未**订流）
- **不是** caster 服务端 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** RTCM 帧解码 → [pyrtcm](./pyrtcm.md)
- **不是** 精密定位引擎

一句话：`ntripbrowser` = **源表发现与就近筛选**；真正吃流换别的客户库。

| 术语 | 含义 |
| --- | --- |
| STR / CAS / NET | sourcetable 三类行；本工具解析为 `str`/`cas`/`net` |
| Mountpoint | 订流名（如 `VALDM`、`ABMF00GLP0`） |
| Distance | `-c` 给定后相对观测点的 km（geopy） |

## 2. 安装

```bash
# 系统：libcurl + OpenSSL 头（pycurl）
sudo apt-get install -y libssl-dev libcurl4-openssl-dev

pip install 'ntripbrowser==4.0.0'
# 或：git clone https://github.com/emlid/ntripbrowser.git && cd ntripbrowser && pip install -e .
ntripbrowser -h
# Parse NTRIP sourcetable ；位置参数 url；-p/-t/-c/-M
python -c "import ntripbrowser; print('ok', ntripbrowser.__file__)"
```

本机：`pip show` → **4.0.0**；editable tip **`3730867`**。

## 3. 端到端（本机真跑；2026-09-24 05:45 EDT）

### 3.1 CLI 拉公开源表

```bash
ntripbrowser rtk2go.com -p 2101 -t 15 | head
ntripbrowser www.igs-ip.net -p 2101 -t 15 | head
ntripbrowser caster.centipede.fr -p 2101 -t 15 | head
```

成功时可见 `success = http://…:2101/`（或 `…/sourcetable.txt`），随后 STR 行或 texttable。挂载数随时间变，以当日探针为准。

### 3.2 Python API 计数（推荐写进脚本）

```python
from ntripbrowser import NtripBrowser

for host in ("rtk2go.com", "www.igs-ip.net", "caster.centipede.fr"):
    r = NtripBrowser(host, port=2101, timeout=20).get_mountpoints()
    print(host, {k: len(v) for k, v in r.items()})
```

**本机：**

| caster | cas | net | str |
| --- | ---: | ---: | ---: |
| `rtk2go.com` | 0 | 1 | **764** |
| `www.igs-ip.net` | 2 | 4 | **384** |
| `caster.centipede.fr` | 1 | 1 | **1269** |

样例字段：`Mountpoint`/`ID`/`Format`/`Format-Details`/`Carrier`/`Nav-System`/`Country`/`Latitude`/`Longitude`/…；未给 `-c` 时 `Distance` 常为 `None`。

centipede 含 **`VALDM`**（`Gercourt-et-Drillancourt`，RTCM3，生成器串含 `Ublox_ZED-F9P`）——与 [ntrip-client](./ntrip-client.md)/[rtcm3torinex](./rtcm3torinex.md) 订流样例同挂载名。

### 3.3 按坐标裁切（巴黎 50 km）

```bash
ntripbrowser caster.centipede.fr -p 2101 -t 15 -c 48.85 2.35 -M 50
```

```python
r = NtripBrowser(
    "caster.centipede.fr", port=2101, timeout=20,
    coordinates=(48.85, 2.35), maxdist=50,
).get_mountpoints()
print(len(r["str"]), r["str"][0]["Mountpoint"], r["str"][0]["Distance"])
```

**本机：** `str` **14**；最近 **`IPGP`**（Paris）**Distance≈0.709** km（`Latitude=48.845`/`Longitude=2.356`）。

### 3.4 边界：本工具不订流

订 `VALDM`/MSM 请改 [ntrip-client](./ntrip-client.md) `simple-cli`、[ntripstreams](./ntripstreams.md) 或 [pygnssutils](./pygnssutils.md) `gnssstreamer`。无账号时各 caster 可能 **400/401/403**——属订流层，不是源表浏览失败。

## 4. I/O 与关键参数

| 接口 | 作用 |
| --- | --- |
| CLI `url` | caster 主机名或 URL（会剥 `http(s)://`） |
| `-p/--port` | 默认 **2101** |
| `-t/--timeout` | 秒；API 默认构造参数 `timeout=4`，公网建议 ≥15 |
| `-c LAT LON` | 观测点；启用 Distance |
| `-M/--maxdist` | km；需同时给坐标 |
| `get_mountpoints()` | 返回 `dict`：`cas`/`net`/`str` → `list[dict]` |

异常：`UnableToConnect` / `ExceededTimeoutError` / `NoDataReceivedFromCaster`（见 `ntripbrowser.exceptions`）。

## 5. 接到哪步

```text
ntripbrowser 列挂载
  → 选 Mountpoint
  → ntrip-client / ntripstreams / pygnssutils / BNC 订流
  → pyrtcm 解帧 或 rtcm3torinex→RINEX → georinex
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ImportError: pycurl` | 缺 libcurl 开发包 | `apt install libssl-dev libcurl4-openssl-dev` 后重装 pycurl |
| 2 | 长时间无输出 | 默认 timeout 偏短 / caster 慢 | `-t 20`；API `timeout=20` |
| 3 | CLI 刷屏 + pager | 大表走 texttable/pager | 管道 `| head` 或改用 API 只取 `len` |
| 4 | STR 数与他手册差几个 | 源表实时变化；CLI 可能重复命中多 URL | 以同日 `get_mountpoints` 字典计数为准 |
| 5 | `Distance` 全 `None` | 未传 coordinates | 加 `-c` / 构造参数 |
| 6 | 裁切后 cas/net 变 0 | `_trim_outlying` 一并裁 | 预期行为；要全表别加 `maxdist` |
| 7 | 当成订流客户端 | 产品只浏览源表 | 换 [ntrip-client](./ntrip-client.md) 等 |
| 8 | igs-ip 订流 401 | 需 IGS 账号 | 仅浏览源表可匿名；订流自行注册 |
| 9 | rtk2go 订流 400/空 | 无有效用户/口令策略 | 源表仍可拉；订流看 caster 政策 |
| 10 | `cchardet` 安装失败 | 旧 wheel/编译器 | 按上游 pin（4.0.0 已对 2.2.0a2+）；换 Python 3.11+ |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 快速看挂载 / 按距筛选 | **ntripbrowser（本文）** |
| Python asyncio 订流 + 部分 RTCM | [ntripstreams](./ntripstreams.md) |
| Rust 订流 + rtcm-rs | [ntrip-client](./ntrip-client.md) |
| 多协议 CLI / 小 caster | [pygnssutils](./pygnssutils.md) |
| 生产多用户 caster | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |

相关：[ntripstreams](./ntripstreams.md) · [ntrip-client](./ntrip-client.md) · [pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [bnc](./bnc.md) · [rtcm3torinex](./rtcm3torinex.md) · [pyrtcm](./pyrtcm.md)