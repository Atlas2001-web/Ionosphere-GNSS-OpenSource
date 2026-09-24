# GDDS · IGS/CORS/产品/时序多模块 GNSS 下载操作手册

目录：[`PROJECTS.json` → `GDDS`](../../PROJECTS.json) · 上游 <https://github.com/LECUT/GDDS> · 许可 **GPL-3.0**（`src/LICENSE`；用户手册另有非商业免责声明，冲突时以 LICENSE + 上游为准）· tip **`2a8543c`**（2024-04-11）· 界面自报 **GDDS V1.2** / ECUT · 本机验证（2026-09-24 EDT）：无 CLI；源码可解析；**开放 HTTPS** 镜像实拉 NOAA CORS brdc/`p041` + ITRF PSD；WHU FTP 登录/CWD 通、LIST/RETR **425**；CDDIS HTTPS **401**（无 Earthdata）；未起 GUI（缺 QtWebEngine/无头限制）· **质检复跑通过**（tip `2a8543c`；NOAA/ITRF 字节对齐；CDDIS 401；WHU login/CWD 通——本机复跑 **NLST 成功**，原文 425 为环境相关）

> 岗位：点选式拉取 **全球 IGS 观测/导航、分析中心产品、区域 CORS、坐标时序**，并带 `.Z/.gz/CRINEX` 解压。冲突时：**本机界面 / 上游 README·User Manual > 本文**。无头流水线 → [fast](./fast.md) / [data-access](../data-access.md)；CDDIS 1 s 块 → [cddis-highrate-downloader](./cddis-highrate-downloader.md)。

## 1. 用途与边界

**做：**

1. **Global IGS Data**：日/高采样观测与导航（RINEX 2/3）；镜像 `WHU(China)` / `IGN(France)` / `ESA(Europe)` / `KASI(Korea)` / `SIO(USA)` / `CDDIS(USA)`
2. **Post-Processing Product**：IGS 与 CODE/JPL/GFZ/EMR/ESA/CAS/WHU/GRG/MIT 等 sp3/clk/erp/snx/atx/ionex/BIAS（按中心勾选）
3. **Regional CORS Data**：`USA CORS` / `Europe EPN` / `Spain CORS` / `Japan JPN` / `Hong Kong CORS` / `Curtin University` / `Australia APREF CORS`
4. **Time Series Product**：`EQDSC(China)` / `NGL(USA)` / `SOPAC(USA)` / `UNAVCO(USA)` / `IERS`（含 ITRF PSD 等）
5. **Custom Download**：自拼 URL 模板
6. **Data Decompression**：`.gz` / `.Z`（`unlzw3`）/ CRINEX→RINEX（捆 `crx2rnx`）
7. 地图选站：内嵌 Flask(`127.0.0.1:5000`) + `QWebEngineView` 百度地图页

**不做：**

- **不是** CLI/批处理入口——无 `argparse`；自动化请用 [fast](./fast.md) 或 [data-access](../data-access.md) 菜谱
- **不是** QC / SPP / PPP → [fast](./fast.md) / [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 专用 CDDIS high-rate 15 min 工具 → [cddis-highrate-downloader](./cddis-highrate-downloader.md)
- **不** 读 RINEX 进 Python → [georinex](./georinex.md)；Hatanaka 官方工具 → [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)
- **不** 替代 Earthdata 正规 `.netrc` 流程——CDDIS 路径在 `Global_IGS_Data.py` **表单模拟登录且硬编码账号**，务必改成你自己的

一句话：GDDS = **PyQt5 多模块 GNSS 下载助手**（ECUT L-Team）；适合交互抓取，不适合无头 CI。

| 术语 | 含义 |
| --- | --- |
| 数据中心 | Global 模块下拉：`WHU(China)` … `CDDIS(USA)` |
| 产品根 URL | Post-Processing 下拉：`ftp://igs.gnsswhu.cn/pub/gps/products/` 等 |
| CORS Source | Regional 下拉：`USA CORS`/`Europe EPN`/… |
| 默认落盘 | 常见 `~/Desktop/Download`（可在界面改） |
| `crx2rnx` | 解压模块从 `slib/third party/` 临时拷到目标目录调用 |

## 2. 安装

### 2.1 预编译（手册推荐）

`bin/` 为 **分卷 zip**（`linux.zip`+`linux.z01`，`Windows.zip`+`Windows.z01`）：

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/LECUT/GDDS.git
cd GDDS/bin
zip -F linux.zip --out linux-full.zip
unzip linux-full.zip -d ~/iono_ops/gdds-bin
# 目录内可执行文件名一般为 GDDS（PyInstaller）；Windows 合并后运行 GDDS.exe
```

无显示器服务器上预编译 GUI **同样无法使用**。

### 2.2 源码

```bash
cd ~/iono_ops/GDDS/src
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
# 上游 requirements.txt 钉在 Py3.7/PyQt5==5.10 一代；现代环境需放宽并加 QtWebEngine
python -m pip install -r requirements.txt
python -m pip install PyQtWebEngine gnsscal unlzw3 requests-ftp
# 必须在 src/ 启动（相对 templates/static、slib）
python GDDS.py
```

**本机（2026-09-24 EDT）安装探活：**

```text
# Py3.13 + pip install PyQt5 PyQtWebEngine requests_ftp：
ModuleNotFoundError: cgi          # stdlib cgi 已移除，requests_ftp 导入失败
# 注入空 cgi 并设 Qt.AA_ShareOpenGLContexts 后仍缺完整桌面/OpenGL；无头 offscreen 未跑通主窗
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'PyQt5.QtWebEngineWidgets'` | 只装了 PyQt5 | `pip install PyQtWebEngine` |
| `No module named 'cgi'`（Py≥3.13） | `requests_ftp` 旧依赖 | 用 Py3.10/3.11；或 `legacy-cgi` / stub |
| 地图空白 | Flask/`QWebEngineView` 失败 | 查 `127.0.0.1:5000`；装齐 WebEngine |
| `GDDS.py: not found` | 不在 `src/` | `cd …/GDDS/src` |

## 3. 端到端：模块点选 + 开放镜像实拉

GDDS **没有** `-h` / 子命令。真源码冒烟只能开 GUI。下列命令验证 **同门类开放 URL**（与 Regional CORS / Time Series 界面路径同类），证明本机网络与落盘，**不是** GDDS GUI stdout。

### 3.1 界面操作（有显示器时）

1. `python GDDS.py` → 主窗标题 **`GDDS V1.2`**
2. **Global IGS Data**：时间、站（或地图）、类型、数据中心（**优先 WHU/IGN/ESA**）→ 输出目录 → Start
3. **Post-Processing Product**：分析中心 + Final/Rapid/Ultra + sp3/clk/… + 产品根
4. **Regional CORS Data**：如 `USA CORS` + 站 + DOY
5. **Time Series Product**：如 `IERS` + ITRF2014 PSD，或 `NGL`
6. **Data Decompression**：勾选 `.gz/.Z/*.crx` 解压

About：`GNSS Data Download Software (GDDS)` · `Version : 1.2` · `East China University of Technology (ECUT)`。

### 3.2 本机开放 HTTPS 实拉

```bash
mkdir -p /tmp/gdds_smoke && cd /tmp/gdds_smoke
curl -fsSL -o brdc0010.24n.gz \
  'https://geodesy.noaa.gov/corsdata/rinex/2024/001/brdc0010.24n.gz'
curl -fsSL -o p0410010.24d.gz \
  'https://geodesy.noaa.gov/corsdata/rinex/2024/001/p041/p0410010.24d.gz'
curl -fsSL -o ITRF2014-psd-gnss.dat \
  'https://itrf.ign.fr/ftp/pub/itrf/itrf2014/ITRF2014-psd-gnss.dat'
wc -c brdc0010.24n.gz p0410010.24d.gz ITRF2014-psd-gnss.dat
zcat brdc0010.24n.gz | head -n 6
```

**本机结果（2026-09-24 EDT）：**

```text
68963   brdc0010.24n.gz
1769574 p0410010.24d.gz
38601   ITRF2014-psd-gnss.dat

     2.11           N: GPS NAV DATA                         RINEX VERSION / TYPE
teqc  2019Feb25     CORS-ADM Account    20240105 15:45:13UTCPGM / RUN BY / DATE
Linux 2.4.21-27.ELsmp|Opteron|gcc|Linux 64|=+               COMMENT
     2.10           N: GPS NAV DATA                         COMMENT
rvacn.e(1404.07)                        2024-01-05T12:57 UTCCOMMENT
This file contains the validated broadcast navigation       COMMENT
```

### 3.3 WHU FTP 与 CDDIS 门禁

```bash
python3 - <<'PY'
from ftplib import FTP
ftp = FTP('igs.gnsswhu.cn', timeout=20)
print('login', ftp.login())
print('cwd', ftp.cwd('/pub/gps/data/daily/2024/001/24p/'))
try:
    print('nlst', ftp.nlst()[:3])
except Exception as e:
    print('nlst_fail', type(e).__name__, e)
PY

curl -sI --max-time 15 'https://cddis.nasa.gov/archive/gnss/data/daily/2024/001/' | head -n 5
```

**本机摘录：**

```text
login 230 Login successful.
cwd 250 Directory successfully changed.
# 写作时（同日早些）：
nlst_fail error_temp 425 Security: Bad IP connecting.
# 质检复跑（2026-09-24 EDT）：NLST 成功，例
# nlst ['ABMF00GLP_R_20240010000_01D_MN.rnx.gz', 'ABPO00MDG_R_20240010000_01D_MN.rnx.gz', ...]

HTTP/1.1 401 Unauthorized
```

生产环境 WHU/IGN 常可直接 FTP；**NLST/RETR 的 425 随出口 IP/PASV 而变**（同机也可能时好时坏）。CDDIS 必须 Earthdata（见 [data-access](../data-access.md)）。GDDS 勾选 CDDIS 时走源码内 **URS 表单登录**，不是 `~/.netrc`。

### 3.4 鉴权（必读）

| 源 | GDDS 行为 | 你应做的 |
| --- | --- | --- |
| WHU / IGN / ESA / KASI / SIO | 匿名 FTP/HTTP | 优先选这些做日常 |
| CDDIS | `Global_IGS_Data.py` **写死** Earthdata `username`/`password` 做 session POST | **改成你自己的账号**；勿把密码提交 git；更好： [data-access](../data-access.md) `.netrc` + `curl -n` / [fast](./fast.md) |
| NOAA CORS / ITRF / 部分时序 | 开放 HTTPS | 适合无账号冒烟 |

本手册 **不抄录** 仓内硬编码口令。登录失败时界面可能提示 *CDDIS website is under maintenance…*（异常被吞成该 Tip）。

## 4. I/O

| 方向 | 内容 |
| --- | --- |
| 输入 | 时间（年/DOY 或日历）、站名列表或地图多选、模块选项（30s/1s、RINEX2/3、Final/Rapid…） |
| 输出 | 各中心原样文件：`*.rnx.gz` / `*.crx.gz` / `*.*d.gz` / `*.sp3` / `*.clk` / `*.tenv3` 等 |
| 解压输出 | 去 `.gz`/`.Z` 后的 CRINEX/RINEX；`crx2rnx -f` → `*.rnx` |
| 日志 | 界面进度条 + 文本框（成功/失败列表） |

下游：观测 → [hatanaka](./hatanaka.md)/[georinex](./georinex.md)/[anubis](./anubis.md)；产品 → [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)；IONEX → [ionex-gim](./ionex-gim.md)。

## 5. 参数（界面字段，无 CLI）

| 模块 | 关键控件 | 取值例 |
| --- | --- | --- |
| Global IGS | 数据类型 | Observation / Meteorology / Obs & Met |
| Global IGS | 采样 | `30s` / `1s`（1s 走 highrate 树） |
| Global IGS | 数据中心 | `WHU(China)` … `CDDIS(USA)` |
| Post-Processing | 分析中心 | `IGS`/`CODE(Switzerland)`/`JPL`/`GFZ`/… |
| Post-Processing | 产品根 | `ftp://igs.gnsswhu.cn/pub/gps/products/` 等 |
| Regional CORS | CORS Source | `USA CORS` / `Europe EPN` / `Hong Kong CORS` / … |
| Time Series | Data Source | `EQDSC(China)` / `NGL(USA)` / `SOPAC` / `UNAVCO` / `IERS` |
| Time Series | ITRF | `ITRF 2020` / `2014` / `2008` |
| Custom | URL 模板 | 协议 + 域名 + 目录 + 文件名占位 |
| Decompression | 过滤器 | `*.Z *.gz` / `*.*d *.crx` |

## 6. 接到哪步

```text
GDDS(GUI 下载) 或 data-access/fast(无头)
   ├─ .Z/.gz/.crx → Data Decompression / hatanaka / rnxcmp
   ├─ OBS/NAV → georinex 探活 → gnss-tec / pytecgg / oasis-roti
   ├─ sp3/clk/bia → pride-pppar / rtklib / cssrlib
   └─ IONEX → ionex-gim / diffionmap
```

路径 A 一日 TEC：[data-access](../data-access.md) →（可选 GDDS/fast）→ [georinex](./georinex.md) → [pytecgg](./pytecgg.md)。

对照 [data-access](../data-access.md) 菜谱：门户/`.netrc`/curl 可脚本化；GDDS 是同一批镜像的 **GUI 封装**。与 **GAMPII-GOOD**（CMake/YAML 批下载观测+精密产品，无时序/地图）互补而非替代。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 无任何 CLI/`-h` | 设计为 PyQt 软件 | 脚本化改 [fast](./fast.md) 或自写 `curl` |
| 2 | CDDIS 全失败 / Tip「maintenance」 | 硬编码 Earthdata 失效或未授权 | 换自有账号；或 WHU；或 `.netrc`+[data-access](../data-access.md) |
| 3 | FTP `425 Bad IP`（时有时无） | PASV 数据通道被 NAT/防火墙改写 | 换网络/主动模式；改 HTTPS 源；同机可复跑验证 |
| 4 | Py3.13 `No module named cgi` | `requests_ftp` 旧 | Py3.10/3.11 或 `legacy-cgi` |
| 5 | `QtWebEngineWidgets` 导入失败 | 缺 PyQtWebEngine / OpenGL 上下文 | 装 WebEngine；注意 `AA_ShareOpenGLContexts` |
| 6 | 地图选站不可用 | 本地 Flask `:5000` 或百度页失败 | 改用站名列表手工输入 |
| 7 | high-rate 目录空 | 勾了 1s 但日期已打成 tar/策略变更 | 近日期或 [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 8 | 解压 CRX 失败 | `crx2rnx` 无执行权限 | `chmod +x`；或 [rnxcmp](./rnxcmp.md) |
| 9 | `requirements.txt` 装不上 | 钉死 PyQt5==5.10.1 / pywin32 | 按平台删 Windows 包、放宽版本 |
| 10 | 以为与 GAMPII-GOOD 相同 | GOOD 为 CMake/YAML 批处理 | 见 §8；流水线选 GOOD/FAST |
| 11 | 密码进了自己的 fork | 源码含明文口令 | 提交前清理；轮换 Earthdata 密码 |
| 12 | 分卷 zip 解压失败 | 只下了 `.zip` 未合并 `.z01` | `zip -F … --out` 再 `unzip` |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| GUI 多源点选（IGS+CORS+产品+时序） | **GDDS（本文）** |
| 无头下载 + QC + 粗 SPP | [fast](./fast.md) |
| YAML/CMake 批下载观测与精密产品（PPP 前站） | **GAMPII-GOOD**（<https://github.com/zhouforme0318/GAMPII-GOOD>） |
| CDDIS 1 s / 15 min 块 | [cddis-highrate-downloader](./cddis-highrate-downloader.md) |
| 只查门户与 `.netrc` 菜谱 | [data-access](../data-access.md) |
| 读 RINEX / 转 CRX | [georinex](./georinex.md) · [hatanaka](./hatanaka.md) · [rnxcmp](./rnxcmp.md) |

对照：**GDDS** 覆盖面宽（含时序与自定义 URL）但 GUI/镜像老化风险高；**GAMPII-GOOD** 偏 PPP 产品清单与可脚本配置；**FAST** 偏日常下载+质检一体。

## 9. 链接

- 上游：<https://github.com/LECUT/GDDS>
- 仓内说明：`README.md` · `src/tutorial/GDDS User Manual.pdf`
- 兄弟：[data-access](../data-access.md) · [fast](./fast.md) · [cddis-highrate-downloader](./cddis-highrate-downloader.md) · [georinex](./georinex.md) · [hatanaka](./hatanaka.md) · [rnxcmp](./rnxcmp.md) · [ionex-gim](./ionex-gim.md) · [README](./README.md) · [`PROJECTS.json`](../../PROJECTS.json)
