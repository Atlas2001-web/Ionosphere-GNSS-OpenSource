# GNSSommelier（EarthScope）· IGS 分析中心产品检索与下载 CLI/库 操作手册

目录：[`PROJECTS.json`](../../PROJECTS.json) → `GNSSommelier` · 仓库 <https://github.com/EarthScope/GNSSommelier> · 本机验证 **2026-09-26 04:47–05:00 EDT**

> 这个工具只负责 **PPP 辅助产品的“找 + 下 + 解压 + 记账”**：给它一个日期和产品名（ORBIT / CLOCK / ERP / BIA / IONEX / VMF …），它会按 YAML 里登记的 16 个中心配置去列目录、按 IGS 长文件名做匹配、下载并解压到 `base-dir/YYYY/DDD/products/`，每个文件旁边再写一份 `*_lock.json`（URL + sha256 + 大小）。它**不处理 RINEX 观测**（`RINEX_OBS` 虽然在产品表里，但按站点下载未实现，见上游 issue 分支 `17-daily-station-specific-rinex…`），**不做定位**；PPP 解算由另一个包 `pride-ppp` 调 PRIDE-PPPAR 的 `pdp3`（本篇未测，见 [pride-pppar](./pride-pppar.md)）。
> 邻居：单中心/固定 URL 的脚本类下载器见 [gampii-good](./gampii-good.md)、[gdds](./gdds.md)、[gnss-downloader](./gnss-downloader.md)；各中心真实路径与账号规则见 [data-access](../data-access.md)。

## 1. 版本事实

| 项 | 值（2026-09-26 核实） |
| --- | --- |
| 仓库 | EarthScope/GNSSommelier，**Apache-2.0**，★14、fork 2、open issues 5；main = tag **v0.0.1** = `039d239`（2026-08-11 21:54 EDT） |
| 结构 | uv workspace 四个包：`gpm-specs`（YAML 规格）、`gnss-product-management`（库，import 名 `gnss_product_management`）、`gpm-cli`（**0.1.0**，入口 `gnssommelier`）、`pride-ppp` |
| PyPI | **四个包都不在 PyPI**（`pypi.org/pypi/<name>/json` 全部 404）。INSTALL.md 写的 `pip install gnss-product-management` **跑不通** |
| Python | ≥3.10（本机 CPython 3.13.5）；依赖 typer 0.27.2、pydantic 2.13.5、fsspec 2026.9.0、paramiko 5.0.0 |
| 中心配置 | `gpm-specs/.../configs/centers/` 实有 **16 个 YAML**：BKG CAS CDDIS COD ESA EUREF GFZ GRGS IGS JPL KASI NGII NRCan TUG VMF WUM。README 写的是“18 个”，表里列了 17 个（含已停用的 SIO），**以目录为准** |
| 产品名 | `RINEX_OBS RINEX_NAV RINEX_MET ORBIT CLOCK ERP BIA ATTOBX IONEX SINEX TROP LEAP_SEC SAT_PARAMS VMF OROGRAPHY ATTATX`。**README 里的 `GIM` 不是合法产品名**，要写 `IONEX` |

## 2. 安装（不 clone，下源码包）

```bash
mkdir -p ~/gs && cd ~/gs
curl -sL -o src.tgz https://codeload.github.com/EarthScope/GNSSommelier/tar.gz/refs/tags/v0.0.1   # ~15.7 MB，解开 38 MB
tar xzf src.tgz && cd GNSSommelier-0.0.1
uv venv -p 3.13 ../venv && . ../venv/bin/activate
# 源码包里没有 .git，setuptools-scm 取不到版本 → 必须给假版本，否则构建失败
export SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
uv pip install ./packages/gpm-specs ./packages/gnss-product-management ./packages/gpm-cli
gnssommelier --help          # 子命令：search / download / probe / config
```

- 不设 `SETUPTOOLS_SCM_PRETEND_VERSION` 时报错结尾是 `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_<DIST> form cannot match`（本机实测）。
- 用 git clone + `uv sync --all-packages` 也可以（上游推荐做法），本篇为省盘没有用。
- 需要 PPP 的话再装 `./packages/pride-ppp`，并把 PRIDE-PPPAR 的 `pdp3` 放进 `$PATH`。

## 3. 配置

```bash
mkdir -p /data/gnss-products                         # 必须先建好目录！
gnssommelier config set base-dir /data/gnss-products
gnssommelier config show
```

- 配置文件是 `~/.config/gnssommelier/config.toml`，可以用环境变量 `GNSS_CONFIG` 指向别的文件。可设置的键有 `base_dir`、`centers`、`max_connections`（默认 4）、`log_level`（默认 WARNING）。
- **`base-dir` 目录不存在时，`search` / `download` 直接抛 `AssertionError: Base directory not found: …`**，`config set` 不会替你建目录（实测）。
- `config show` 在 set 之后 Source 列仍显示 `default`，但值已经写进 toml，属于显示 bug。
- CDDIS 需要 Earthdata 账号：在 `~/.netrc` 加一行 `machine cddis.nasa.gov login <user> password <pass>`，注册地址是 <https://urs.earthdata.nasa.gov/>。本机**没有账号，CDDIS 认证下载未测**。

## 4. 端到端命令与本机实测输出

### 4.1 连通性体检（先跑这个）

```bash
gnssommelier probe --json probe.json      # 不带 --date/--product = 只测服务器；本机用时 63 s
```

本机结果是 16 个服务器地址里 **11 个 CONNECTED、5 个 UNREACHABLE**：

| 状态 | 服务器 |
| --- | --- |
| HTTPS 可列目录 | EUREF `epncb.oma.be`（98 项）、IGS `files.igs.org`（15）、BKG `igs.bkg.bund.de`（21）、JPL `sideshow.jpl.nasa.gov`（6）、VMF `vmf.geo.tuwien.ac.at`（26） |
| FTP 能连上但根目录为空（`root directory empty or inaccessible`） | CDDIS/TUG `gdc.cddis.eosdis.nasa.gov`（FTPS，0.2 s）、ESA `gssc.esa.int`、WUM `igs.gnsswhu.cn`、IGS `igs.ign.fr`、NRCan、GRGS（后两个都是 60 s 才返回） |
| UNREACHABLE | COD `ftp.aiub.unibe.ch`（**等满 60 s 超时**）、CAS `ftp.gipp.org.cn`、KASI、NGII（上游注明只在韩国境内可达）、GFZ `sftp://isdc-data.gfz.de` |

结论：在海外云主机上，**优先用 `--sources JPL`、`--sources BKG` 这类 HTTPS 中心**；只要把 COD 留在候选里，每次查询都会多卡 60 s。

### 4.2 检索（search）

```bash
gnssommelier search ORBIT --date 2025-01-02 --where TTT=FIN \
  --sources IGS --sources BKG --sources JPL --json s1.json
```

```
  Center     Quality   Filename                                 Local   Server
  IGS        FIN       IGS0OPSFIN_20250020000_01D_15M_ORB.SP…     —     https
  JPL        FIN       JPL0OPSFIN_20250020000_01D_05M_ORB.SP…     —     https
╭─ Search summary ─╮
│ ✓ 2/2   ·   6.9s │
```

- 这里的 `Center` 是**产品的 AAA（出品机构）**，`--sources` 限定的是**托管服务器所在的中心**，两者不是一回事。上例中 IGS 那一行其实是从 BKG 的 `root_ftp/IGS/products/2347/` 找到的；只写 `--sources IGS` 时要走 `igs.ign.fr`，本机列目录失败，结果为空。
- `--where` 的键就是 IGS 长文件名里的字段：`TTT`（FIN/RAP/ULT）、`SMP`（15M/05M/30S）、`LEN`、`PPP`。写 `--where AAA=IGS` 在本机**一条结果都没有**（AAA 过滤没生效），要按机构筛选的话请在 JSON 里自己过滤。
- `--json` 里 `uri` 字段显示成 `https://https://…`、`ftps://ftp://…`（前缀重复），这是显示/序列化 bug，不影响下载。
- `search IONEX --date 2025-01-02`（不限中心）用了 60.5 s，找到 9 条，**全部来自 CDDIS FTPS**：COD FIN/RAP（01H）、ESA FIN（02H）/RAP（01H、02H）、IGS FIN/RAP、JPL FIN/RAP。**5 分钟后在同一台机器上重跑，CDDIS 列目录失败**（`Retry failed listing gnss/products/ionex/2025/002/`），`curl --ssl-reqd` 匿名 NLST 也拿到空列表。所以匿名访问 CDDIS 时好时坏，正式使用要配好 `.netrc`。

### 4.3 下载（download）

```bash
gnssommelier download ORBIT --date 2025-01-02 --where TTT=FIN --sources JPL --dry-run   # 先预览
gnssommelier download ORBIT --date 2025-01-02 --where TTT=FIN --sources JPL
gnssommelier download ERP   --date 2025-01-02 --where TTT=FIN --sources JPL
```

实测结果：ORBIT 用 2.0 s，状态 `will download` → `✓ 1/1`；ERP 用 1.6 s。落盘情况：

```
/data/gnss-products/2025/002/products/JPL0OPSFIN_20250020000_01D_05M_ORB.SP3            1293754 B（已自动解 .gz）
/data/gnss-products/2025/002/products/JPL0OPSFIN_20250020000_01D_05M_ORB.SP3_lock.json   415 B
/data/gnss-products/2025/002/products/JPL0OPSFIN_20250020000_01D_01D_ERP.ERP             422 B
```

- SP3 自查：头部写 `#cP2025  1  2 … 289 u+U IGS20 FIT JPL`，共 **289 个历元**（00:00 到次日 00:00，5 min 间隔）、**60 颗卫星（G 31 + E 29）**。ERP 是 `version 2` 格式，数据行为 `60677.50  142559  304926  463679 …`。
- lock.json 的字段：`name`、`timestamp`（UTC）、`url`、`hash`（`sha256:3b29fda0…`，和本地 `sha256sum` 一致）、`size`、`sink`、`alternatives`。
- **每个产品只下排名第一的那一条**（代码里是 `found[0]`）；想要特定机构，就用 `--sources` 限定服务器，再配合 `SMP` 等过滤。
- 已经下过的文件会显示 `cached`，不会重复下载。坑：`download ORBIT --sources IGS`（不带 TTT）时，把本地已有的 **JPL** 文件当成命中，报 `cached`，Center/Quality 两列还显示成 `{3}` 和 `[A-Z]{3}` 这种正则原文。也就是说本地缓存匹配**不看 `--sources`**。
- 多产品 dry-run：`download ERP IONEX CLOCK BIA --where TTT=FIN --sources JPL --sources BKG` → ERP 来自 JPL，CLOCK 为 `IGS0OPSFIN_…_01D_30S_…`（BKG），**IONEX 和 BIA 都是 not found**（BKG 配置里的 `root_ftp/IGS/products/ionex/2025/002/` 实际返回 HTTP 404）。CLOCK 30S 文件较大，本机没有真下。
- 退出码：全部找到并下完为 0，有 not found 为 1，适合在脚本里判断。

### 4.4 按产品探测（probe 的检索模式）

```bash
gnssommelier probe --date 2025-01-02 --center JPL --product ORBIT --product IONEX --product ERP
```

本机 0.7 s 返回：JPL ERP FOUND、ORBIT FOUND、**IONEX NOT FOUND**（`jpl_config.yaml` 把 IONEX 指向 sideshow `pub/jpligsac/{GPSWEEK}/`、按长文件名匹配，但该目录 2347 周里没有 GIM 文件；JPL 长名 IONEX 实际要经 CDDIS 拿）。

### 4.5 Python API

```python
from datetime import datetime, timezone
from pathlib import Path
from gnss_product_management import GNSSClient
c = GNSSClient.from_defaults(base_dir=Path("/data/gnss-products"))
d = datetime(2025, 1, 2, tzinfo=timezone.utc)
for r in c.query().for_product("ORBIT").on(d).where(TTT="FIN").sources("JPL", "BKG").search():
    print(r.center, r.quality, r.is_local, r.hostname, r.filename)
# 实测输出（第一行是本地缓存，center 显示成正则原文）：
# [a-zA-Z0-9]{3} FIN True  JPL0OPSFIN_20250020000_01D_05M_ORB.SP3
# IGS FIN False https IGS0OPSFIN_20250020000_01D_15M_ORB.SP3.gz
# JPL FIN False https JPL0OPSFIN_20250020000_01D_05M_ORB.SP3.gz
```

真正下载用 `c.download([r], sink_id="local")`。按依赖规格一次解析整套产品用 `c.resolve_dependencies("spec.yaml", d, sink_id="local")`，这需要自己写依赖 YAML，本篇未测。

## 5. 错误用例（实测）

| 输入 | 输出 / 退出码 |
| --- | --- |
| `search GIM …` | `Search failed: Product 'GIM' not found in ProductCatalog`，rc 1 |
| `--date 2025/01/02` | `Invalid --date: '2025/01/02'  (expected YYYY-MM-DD)` |
| `--where TTT` | `--where must be KEY=VALUE, got: 'TTT'` |
| base-dir 未建 | `AssertionError: Base directory not found` 并打印整段 traceback |
| 服务器列目录失败 | 黄字 `Retry failed listing <dir> on <host>`，**不报错**，只是结果变少，所以要看清是哪个中心没列出来 |

## 6. 坑（按严重度）

1. **`search … --to`（日期范围）千万别在共享机器上跑。** 本机跑 `search ORBIT --date 2025-01-01 --to 2025-01-03 --sources JPL`，刷出上千行 `Search failed for date …: can't start new thread`，3 分多钟都没结束，只能 kill。原因是日期线程池（≤8）里再嵌套列目录线程池（≤25），失败后还会重试。需要多天就在 shell 里循环 `--date`。
2. 不在 PyPI，要从源码装，而且必须设 `SETUPTOOLS_SCM_PRETEND_VERSION`（或者 git clone）。
3. 产品名是 `IONEX`，不是 README 里的 `GIM`；中心有 16 个，不是 18 个。
4. `--sources` 指的是托管服务器所在的中心，不是出品机构；`--where AAA=` 过滤无效。
5. 只要候选里有 COD（`ftp.aiub.unibe.ch`）或 NRCan/GRGS，每次都要多等约 60 s；FTP 在很多云主机上被墙或者列不出目录。
6. 匿名 CDDIS 时好时坏，正式用要配 Earthdata `.netrc`；GFZ 走 SFTP，本机不通。
7. 本地缓存命中不看 `--sources`，而且会把正则原文当 center 显示。
8. BKG 的 IONEX 路径配置有误（404）；JPL 的 IONEX 在 sideshow 上配错了目录，只能经 CDDIS 拿。
9. JSON 里的 `uri` 前缀重复，不要直接拿去喂 curl。

## 7. 选型

- 需要跨中心自动找 SP3/CLK/ERP/BIA，并且想留下可复现的 lock 记录（sha256）→ 用本工具，但要限定 HTTPS 中心。
- 已知固定 URL，只拉一两个中心 → 直接 curl（路径见 [data-access](../data-access.md)），或者用 [gampii-good](./gampii-good.md) / [gdds](./gdds.md)。
- 下 CDDIS 高频观测数据 → [cddis-highrate-downloader](./cddis-highrate-downloader.md)。
- 拿到产品后做 PPP → [pride-pppar](./pride-pppar.md)（本仓的 `pride-ppp` 包是它的 Python 封装，未测）。

未测清单：CDDIS 认证下载、`pride-ppp`、`resolve_dependencies`、`config init`/`validate`、VMF/ATX/OBX 产品下载。
