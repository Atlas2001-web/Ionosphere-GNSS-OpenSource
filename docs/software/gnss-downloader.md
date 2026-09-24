# gnss-downloader · PyQt5 NASA/WHU FTP GNSS 下载操作手册

目录：[`PROJECTS.json` → `gnss-downloader`](../../PROJECTS.json) · 上游 <https://github.com/Mereithhh/gnss-downloader> · 官网 <https://www.mereith.com/gnss> · **无 SPDX 许可文件**（仓内无 `LICENSE`）· tip **`e6d0d84`**（2020-05-07；Release **V3.0** / 2020-05-06）· 本机验证（2026-09-24 EDT）：无下载 CLI；`core.gps_downloader` 横幅实跑；WHU FTP **230**+CWD 通、NLST/RETR **425**；`SIZE brdc0010.24n.gz`=**57792**、`ABPO00MDG_R_20240010000_01D_GN.rnx.gz`=**29294**；`cddis.nasa.gov` 不可达；`gdc.cddis…` 明文 FTP **530** 须加密；无头缺 PyQt5 · ★≈23

> 岗位：带界面从 **WHU / NASA(CDDIS)** 按日拉 IGS 日采样观测/导航与 igs/igu/igr sp3。冲突时：**上游 README / Release 说明 / 本机 stdout > 本文**。无头批下 → [gampii-good](./gampii-good.md) / [fast](./fast.md) / [data-access](../data-access.md)；多模块 GUI → [gdds](./gdds.md)；CDDIS 1 s → [cddis-highrate-downloader](./cddis-highrate-downloader.md)。**勾选 NASA 源涉及 CDDIS 时先读** [data-access](../data-access.md)「共用：Earthdata / `.netrc`」。

## 1. 用途与边界

**做：**

1. **PyQt5 GUI**（`code/gnss-downloader.py`）：勾选文件类型、起止日、站名或按卫星号查表、源服务器、保存路径 → 检索 → 下载（可暂停）
2. **数据源**：`武汉` → `igs.gnsswhu.cn`；`NASA` → `cddis.nasa.gov`（源码硬编码**明文匿名 FTP**，路径 `/pub/gps/data/daily/` · `/pub/gps/products/`）
3. **类型**：RINEX3 `o.rnx`/`n.rnx`/`m.rnx`；RINEX2 `_o`/`_n`/`_m` / `.o`/`.n`/`.m`；产品 `igs`/`igu`/`igr`（按周目录筛 sp3）
4. **站选择**：全站；手动四字站码；或「按卫星号」查捆 `lib/db.json`（预计算最大观测时长站表）
5. **库级调用**：`core.gps_downloader(selector, save_path).run()` / `.gui(ui)`（无 argparse）

**不做：**

- **不是** 正式下载 CLI——无 `-h`；仓内 `code/cli.py` 是 **星历 RINEX + MongoDB** 分析稿（`rinex_selector` / georinex / pymongo），**无 `__main__`、不接 FTP 下载**
- **不是** 多模块 CORS/时序/解压 GUI → [gdds](./gdds.md)
- **不是** YAML/CMake 批下载 → [gampii-good](./gampii-good.md)；也 **不是** 下载+QC+粗 SPP → [fast](./fast.md)
- **不是** CDDIS high-rate 15 min → [cddis-highrate-downloader](./cddis-highrate-downloader.md)
- **不** 实现 Earthdata / FTPS / `.netrc`——勾 NASA 在现行 CDDIS 政策下通常失败（见 §3.3）
- **不** 解压 Hatanaka / 读进 Python → [hatanaka](./hatanaka.md)/[rnxcmp](./rnxcmp.md)/[georinex](./georinex.md)

一句话：**2020 年个人向 PyQt 日文件下载器**；教学点选尚可，流水线请换 GOOD/FAST/data-access。

| 术语 | 含义 |
| --- | --- |
| `selector` | `source`=`wuhan`\|`nasa`；`filetype` 列表；`times`=`[ISO起,ISO止]`；`stations` 四字码或空=全站 |
| 日路径 | `/pub/gps/data/daily/YYYY/DDD/YYt/`（`t`∈`n/m/o`） |
| 产品路径 | `/pub/gps/products/<GPS周>/` |
| 默认落盘 | GUI：`./下载数据`；库 `run()`：**先 `rmtree(save_path)` 再重建** |
| `db.json` | 卫星号 `01`…`32` → 推荐站码列表（自动选站） |

## 2. 安装

### 2.1 Release 预编译（上游推荐）

```bash
# Release V3.0 资产 GNSS.zip（≈39 MB，2020-05-06；说明：批量日期/类型 bugfix）
# https://github.com/Mereithhh/gnss-downloader/releases/tag/V3.0
# 另有百度网盘链（README）；Mac 版 README 称「即将推出」——截至 tip 仍无 macOS Release
unzip GNSS.zip -d ~/iono_ops/gnss-downloader-bin
# 按包内说明启动可执行文件（Windows 向为主；无显示器服务器同样无法用 GUI）
```

### 2.2 源码（需桌面 + PyQt5）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/Mereithhh/gnss-downloader.git
cd gnss-downloader
git rev-parse --short HEAD   # 期望 e6d0d84
cd code
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install 'PyQt5' tqdm   # README：PyQt5 / tqdm / Python 3.5+
# 必须在 code/ 启动（相对 ./lib/db.json、favicon）
python gnss-downloader.py
```

**本机（2026-09-24 EDT）：** 默认 Python **无** `PyQt5`（`ModuleNotFoundError`）；无头环境未起主窗——**不臆造 GUI stdout**。可执行文件打包上游写可用 `pyinstaller` / `Nuitka`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'PyQt5'` | 未装 GUI 依赖 | `pip install PyQt5`；需显示服务器 |
| `无法读取db.json` | 不在 `code/` 或缺 `lib/` | `cd …/code`；确认 `lib/db.json` |
| 多次下载异常 | 上游 README Attention | **关软件再开**再下一轮 |
| `cli.py` 当下载入口 | 误读文件名 | 下载走 GUI 或 `core.gps_downloader` |

## 3. 端到端：界面 → 库横幅 → FTP 探针（本机真跑）

### 3.1 界面操作（有显示器时）

1. `python gnss-downloader.py` → 主窗（英化后标题 **`GNSS-Downloader   v2.0 by Mereith.`**）
2. **Select FileType**：默认勾 `GN.rnx(3.x)` + `igs.sp3`；可加观测/气象/igu/igr
3. **Select Time**：From/To（ISO 日）；起 > 止会拒下
4. **Select Stations**：`Input by my self`（空格分隔四字码）或 `Select by gps number…`（`01`…`32`）或默认全站
5. **Source Server**：武汉（国内快）/ NASA（源码写 “best”，但见 §3.3）
6. **Save Path** → **Start**；进度条 + 信息栏；**Pause** 可挂起 RETR 循环
7. About：背景图 `lib/support.jpg`（无额外版本字符串控件）

### 3.2 库级横幅（无 GUI；本机真 stdout）

```bash
cd ~/iono_ops/gnss-downloader/code
python3 - <<'PY'
from core import gps_downloader
sel = {
    'source': 'wuhan',
    'filetype': ['n.rnx'],
    'times': ['2024-01-01', '2024-01-01'],
    'stations': ['ABPO'],
}
gps_downloader(sel, '/tmp/gnss_dl_smoke').run()
PY
```

**本机 stdout（2026-09-24 EDT，节选）：**

```text
['2024-01-01']
------------------------------------
-  欢迎使用gps数据下载All in One.  -
------------------------------------
数据源:   igs.gnsswhu.cn
时间:     2024-01-01
文件类型: n.rnx
观测站:   ABPO
共:       1 组数据
------------------------------------

已搜索到0个文件，开始下载
```

说明：构造打印横幅后 `run()` 连 WHU、对 `/pub/gps/data/daily/2024/001/24n` 做 `NLST`；本机 **NLST→425**，故「已搜索到 **0** 个」——**不是**站不存在。GUI 路径同样依赖 `nlst`，同网会一样空检索。

### 3.3 FTP / CDDIS 探针（证明网络与策略；非 GUI 落盘）

```bash
python3 - <<'PY'
from ftplib import FTP
# WHU
ftp = FTP(); ftp.connect('igs.gnsswhu.cn', timeout=30)
print(ftp.getwelcome().splitlines()[0])
print('login', ftp.login())
ftp.cwd('/pub/gps/data/daily/2024/001/24n'); print('cwd', ftp.pwd())
try:
    print('nlst', ftp.nlst()[:3])
except Exception as e:
    print('nlst', type(e).__name__, e)
for name in ['brdc0010.24n.gz', 'ABPO00MDG_R_20240010000_01D_GN.rnx.gz']:
    try: print('SIZE', name, ftp.size(name))
    except Exception as e: print('SIZE', name, type(e).__name__, e)
ftp.quit()
# NASA 旧主机（工具硬编码）
try:
    FTP().connect('cddis.nasa.gov', timeout=20)
except Exception as e:
    print('cddis.nasa.gov', type(e).__name__, e)
# 现行 GDC 明文
ftp2 = FTP(); ftp2.connect('gdc.cddis.eosdis.nasa.gov', timeout=30)
print(ftp2.getwelcome().splitlines()[0])
try: ftp2.login()
except Exception as e: print('gdc login', type(e).__name__, e)
PY
```

**本机结果（2026-09-24 EDT）：**

```text
220 Welcome to IGS data center of WUHAN university.
login 230 Login successful.
cwd /pub/gps/data/daily/2024/001/24n
nlst error_temp 425 Security: Bad IP connecting.
SIZE brdc0010.24n.gz 57792
SIZE ABPO00MDG_R_20240010000_01D_GN.rnx.gz 29294
cddis.nasa.gov OSError [Errno 101] Network is unreachable
220-**********************************************************************
gdc login error_perm 530 Anonymous sessions must use encryption.
```

对照：[data-access](../data-access.md)——CDDIS 匿名 FTP 已停；HTTPS/`ftps://gdc.cddis.eosdis.nasa.gov/` + Earthdata `.netrc`。本工具 **未**实现该路径；勾 NASA 在 2026 年环境基本不可用。家宽若 PASV 正常，WHU 源仍可能实下。

## 4. 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | 起止 ISO 日、文件类型勾选、站码或卫星号、源 `wuhan`/`nasa`、保存目录 |
| 输出布局 | `<save>/<YYYY-MM-DD>/data|product/<原名>` |
| 典型文件 | `*GN*.rnx*` / `*MO*.rnx*` / `brdc*.*n*` / `igsWWWD.sp3*` 等（以镜像当日命名为准） |
| 日志 | GUI 信息栏 + 进度条；库 `run()` 仅打印横幅与「已搜索到 N 个」 |
| 破坏性 | `run()`（非 GUI）若目标目录已存在会 **整树删除** |

下游：观测/导航 → [georinex](./georinex.md)/[hatanaka](./hatanaka.md)；sp3 → [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)；门户菜谱 → [data-access](../data-access.md)。

## 5. 参数（界面 / selector，无 CLI 旗标）

| 字段 | 取值 | 备注 |
| --- | --- | --- |
| `source` | `wuhan` / `nasa` | GUI 单选；改 `host`+前缀 |
| `filetype` | `o.rnx` `n.rnx` `m.rnx` `_n` `_m` `_o` `igs` `igu` `igr` | 与勾选框一一对应 |
| `times` | `[start, end]` ISO 日 | 含端点逐日展开 |
| `stations` | `['abpo',…]` 或 `[]` | 子串匹配文件名；空=不过滤 |
| 保存路径 | 任意可写目录 | GUI 默认 `cwd/下载数据` |

## 6. 接到哪步

```text
偶发点选 → gnss-downloader(GUI, 优先 WHU)
无头 / PPP 备数 → gampii-good / fast / data-access(.netrc)
多源 CORS/时序/解压 → gdds
CDDIS 1s → cddis-highrate-downloader
落盘后 → hatanaka/rnxcmp → georinex → gnss-tec/pytecgg
```

路径 A：[data-access](../data-access.md) →（可选本文 / [gdds](./gdds.md) / [gampii-good](./gampii-good.md) / [fast](./fast.md)）→ [georinex](./georinex.md)。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 无 `-h` / 无下载子命令 | 设计为 GUI；`cli.py` 另用途 | 自动化改 [fast](./fast.md)/[gampii-good](./gampii-good.md) |
| 2 | 勾 NASA 全失败 | 硬编码 `cddis.nasa.gov` 明文 FTP | 改 WHU；或按 [data-access](../data-access.md) 自备 Earthdata HTTPS/FTPS |
| 3 | `530 … must use encryption` | GDC 拒匿名明文 | 本工具无 FTPS；换镜像或自写客户端 |
| 4 | 检索 0 文件 / `425 Bad IP` | PASV 数据通道被 NAT/防火墙改写 | 换网络；控制连接仍可 `SIZE` 验证文件在 |
| 5 | `run()` 清空目录 | `shutil.rmtree(save_path)` | 勿把贵重路径传给库 `run()`；GUI 路径不走该删除 |
| 6 | 多次下载怪 bug | 上游已知 | 每轮关闭重启进程 |
| 7 | 自动选站离谱 | `db.json` 静态、年代旧 | 改手动四字码 |
| 8 | 无头 `ModuleNotFoundError: PyQt5` | 未装或无显示 | 装 PyQt5+桌面；或只用探针/换工具 |
| 9 | 高采样 / IONEX / CLK | 类型表未覆盖 | [cddis-highrate-downloader](./cddis-highrate-downloader.md)/[gdds](./gdds.md)/[gampii-good](./gampii-good.md) |
| 10 | 许可不明 | 无 LICENSE | 商用/再分发前联系作者或改用 GPL/MIT 工具 |
| 11 | Release 停在 2020 | 镜像策略已变 | 先验 FTP；失败即切 GOOD/FAST |
| 12 | 与 GDDS/GOOD 混淆 | 同属「下载」类 | 见 §8 |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 最简 PyQt 点选 WHU 日文件（教学） | **gnss-downloader（本文）** |
| IGS+CORS+产品+时序多模块 GUI | [gdds](./gdds.md) |
| YAML 批下载观测+精密产品（PPP 前） | [gampii-good](./gampii-good.md) |
| 下载 + QC + 粗 SPP | [fast](./fast.md) |
| CDDIS 1 s / 15 min | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 门户 / Earthdata 菜谱 | [data-access](../data-access.md) |

对照：**gnss-downloader** 最轻、最旧、NASA 源已锈；**GDDS** 覆盖面宽；**GOOD/FAST** 适合无头与复现实验。

## 9. 链接

- 上游：<https://github.com/Mereithhh/gnss-downloader> · Release <https://github.com/Mereithhh/gnss-downloader/releases/tag/V3.0> · 官网 <https://www.mereith.com/gnss>
- 兄弟：[data-access](../data-access.md) · [gdds](./gdds.md) · [gampii-good](./gampii-good.md) · [fast](./fast.md) · [cddis-highrate-downloader](./cddis-highrate-downloader.md) · [georinex](./georinex.md) · [hatanaka](./hatanaka.md) · [README](./README.md) · [`PROJECTS.json`](../../PROJECTS.json)
