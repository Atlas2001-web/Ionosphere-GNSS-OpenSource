# SuperDARN 数据获取（FRDR · SuperDARN Canada Globus · BAS 镜像 · VT）· 下载侧 操作手册

入口：[FRDR SuperDARN 合集](https://www.frdr-dfdr.ca/repo/collection/superdarn) · [superdarn.ca/data-access](https://superdarn.ca/data-access) · [BAS 镜像 API](https://api.bas.ac.uk/superdarn/mirror/v3/) · [VT Data Download](https://vt.superdarn.org/data-download) · 本机验证 **2026-09-26 03:35–03:55 EDT**。只用了 curl、`bzip2`、`sha1sum` 和系统 Python 3（`bz2` / `struct`）；另在临时 venv 里装了 `pydarnio 2.1`，**只用来核对记录数**。样例是 3 个 FRDR 小文件（6 KB / 15 KB / 161 KB），用完即删。

> 岗位：把 SuperDARN **原始文件（RAWACF / 老 DAT）**拉到本地并验完整性，或者搞清楚 FITACF / MAP 应该去哪里申请。本文**不讲**读图和画图（RTI、扇形图、对流图 → [pydarn](./pydarn.md)），也不讲 RST 处理链的安装。  
> 门槛总表：[data-access 决策表](../data-access.md#电离层与地磁门户决策表) · [E6 FRDR SuperDARN](../data-access.md#dp-e6)；高纬 ISR / TEC 另见 [madrigal](./madrigal.md)。  
> 冲突时：**数据集自带的 readme / LICENSE / CITATION 与 SuperDARN Rules of the Road > 本文**。

## 1. 它解决什么，边界在哪

| 路线 | 数据级别 | 账号 / 门槛（实测或页面原文） | 能否脚本化 | 本文定位 |
| --- | --- | --- | --- | --- |
| **FRDR**（加拿大联邦数据仓储） | **只有 RAWACF**（2007–2023），2005–2006 为 RAWACF/DAT，1993–2004 只有 DAT | 单文件 HTTPS **无需账号**；批量用 Globus（要 Globus 账号 + Globus Connect Personal 端点） | 能：用未公开的 `file_sizes.json` 列目录，再 `curl -L` | **主路线，全部实测** |
| **SuperDARN Canada Globus 镜像**（USask） | FITACF（`fitacf_30` / `fitacf_25`）、MAP，以及全部数据 | Globus 账号 + 个人端点 + 发邮件给 superdarn@usask.ca 申请 → 被拉进 Globus group，并接受 Rules of the Road | Globus CLI 可以，但**未测** | 需要 FITACF / MAP 或最新数据时用 |
| superdarn.ca/data-download 网页表单 | FITACF 3.0，只含 5 部加拿大雷达（sas / cly / inv / rkn / pgr） | 网页表单（日期 + 雷达）；用 curl 访问只拿到 JS 挑战页 | 否（未找到公开端点） | 少量加拿大雷达的 fit 文件 |
| **BAS 镜像**（英国南极调查局） | RAWACF / DAT（`/sddata/…`） | 发邮件到 bassuperdarndata@bas.ac.uk，提供主机地址、用户名和 SSH 公钥 → 只读 rsync / sftp / scp；**目录 API 公开** | sftp 部分**未测**（没有账号）；API 实测 | 查校验和、全量同步 |
| NSSC 镜像（superdarn.nssdc.ac.cn） | — | 首页只有 `/login`，需要账号 | 未测 | 仅列出 |
| **VT Data Download**（vt.superdarn.org） | FitACF3 / FitACF / FitEX / Map2 / Grid2 | 页面写着 "Log in to access this tool"，每天限 15 次（"Downloads remaining today: 0 / 15"），还要勾选 PI 验证声明 | 否（需登录） | 零星下载 fit / map |

**数据级别**：IQ → **RAWACF**（雷达端生成的自相关函数）→ **FITACF**（RST `make_fit` 拟合出速度、谱宽、功率）→ **GRID / MAP**（RST 多雷达网格化与对流拟合）。FRDR 上**没有** FITACF、GRID 或 MAP。自己从 RAWACF 做需要 [RST](https://github.com/SuperDARN/rst)（doi 10.5281/zenodo.801458）。pyDARN 文档原话："pyDARN does not provide an interface for downloading data"。

## 2. 安装

```bash
curl --version | head -1; bzip2 --help 2>&1 | head -1; sha1sum --version | head -1
python3 -c "import bz2, struct, json; print('ok')"      # 3.4 的纯 Python dmap 读取器只需标准库
# 可选，只用来核对记录数：
python3 -m venv /tmp/sdv && /tmp/sdv/bin/pip install -q pydarnio    # 实测 pydarnio 2.1 + darn-dmap 0.8.2 + numpy 2.5.3，约 102 MB
```

Globus 批量传输需要 Globus 账号，并安装 [Globus Connect Personal](https://www.globus.org/globus-connect-personal) 来建立本机端点（也可以用 `globus-cli`）。本文**没有**用任何账号测试 Globus。

## 3. 真实命令与输出

### 3.1 FRDR：年份 × 数据级别 → item 号

合集页 `https://www.frdr-dfdr.ca/repo/collection/superdarn` 共有 **31 个数据集**，每页 20 条，第 2 页加 `?offset=20&order=DESC&sort=2`。数据集页的源码里 `setItem('N')` 就是 item 号，第一个 `10.20383/…` 是 DOI。

| 年 | 级别 | item | 大小（页面） | DOI |
| --- | --- | --- | --- | --- |
| 1993 | DAT | 466 | 0.006 TB | 10.20383/102.0471 |
| 1994 → 2004 | DAT | 465 → 455（逐年减 1） | — | — |
| 2005 / 2006 | RAWACF/DAT | 452 / 451 | — | — |
| 2007 → 2016 | RAWACF | 450 → 441 | — | — |
| 2014 | RAWACF | 443 | 4.79 TB | 10.20383/102.0448 |
| 2017 / 2018 | RAWACF | 284 / 285 | — | 2017：10.20383/101.0289 |
| 2019 / 2020 / 2021 / 2022 | RAWACF | 553 / 568 / 672 / 888 | — | — |
| **2023** | RAWACF | **1302** | **6.32 TB** | 10.20383/103.01307 |

2023 年数据集的缓存 `lastModified` 是 **2025-09-18**，可见 FRDR 大约滞后两年（pyDARN 文档也说 FRDR 发布最多要两年，近期数据要走镜像）。

### 3.2 列目录：未公开的 `file_sizes.json`

> ⚠️ **未公开接口**：这是从站点自己的 `/repo/static/js/files.js` 反推出来的，FRDR 没有文档，随时可能变。

```bash
I=1302; B="https://www.frdr-dfdr.ca/cache/7/publication_$I/file_sizes"
curl -s "$B/file_sizes.json" | python3 -c "import json,sys;d=json.load(sys.stdin);[print(x['type'],x['name'],x['size']) for x in d['contents']]"
# 子目录：file_sizes-<sha256(相对路径)>.json，相对路径形如 "2023" 或 "2023/05"
h=$(printf '2023/05' | sha256sum | cut -d' ' -f1)
curl -s "$B/file_sizes-$h.json" -o ls_202305.json
```

实测输出：
- **根目录（2023）**：目录 `2023`，以及 `2023RAWACF.readme.txt`（19,540 B）、`CITATION.txt`（138 B）、`LICENSE.txt`（13,308 B）。1993 的根目录还多一个 `frdr-dfdr-checksums.txt`（502,917 B，FRDR 在 2021 年自动生成）。
- **`2023/05`**：**13,113** 项，其中 `202305.hashes` 为 985,180 B、13,112 行（格式为 `sha1␣␣文件名`）。最小的几个文件是 `20230503.1013.38.cve.rawacf.bz2` 821 B、`20230520.1349.35.cve…` 5,263 B、`20230509.1834.01.cve.rawacf.bz2` 6,474 B；**中位数** `20230513.1001.00.fhw.rawacf.bz2` 为 **33,121,580 B**。
- 该月共有 26 个雷达代码，文件数从多到少为 sas 896、rkn 818、inv 815、cly 799、pgr 764、fir 750、bpk 723、cve/cvw 各 622，其余约 350–390。
- **`1993/09`**：105 项，`199309.hashes` 为 6,451 B；最小的数据文件是 `1993092915ta.dat.bz2`（15,343 B）。

对完整 URL 取 sha256，或者只对 `"05"` 取，都会 404，只能对**相对路径**取。

### 3.3 单文件 HTTPS 下载（302 → Globus HTTPS）

```bash
P="https://www.frdr-dfdr.ca/repo/files/7/published/publication_1302/submitted_data/2023/05"
curl -sI "$P/20230509.1834.01.cve.rawacf.bz2" | grep -iE "^HTTP|^location"
#  HTTP/2 302
#  location: https://g-0758ab.cd4fe.0ec8.data.globus.org/7/published/publication_1302/submitted_data/2023/05/20230509.1834.01.cve.rawacf.bz2
for f in 20230509.1834.01.cve.rawacf.bz2 20230504.2130.30.sas.a.rawacf.bz2 202305.hashes; do curl -sL -O "$P/$f"; done
sha1sum 2023050*.bz2; grep -E '20230509.1834.01.cve|20230504.2130.30.sas.a' 202305.hashes
bzip2 -tv 2023050*.bz2
```

| 文件 | 大小 | sha1（本地 = `202305.hashes`） | `bzip2 -t` | 解压后 |
| --- | --- | --- | --- | --- |
| `20230509.1834.01.cve.rawacf.bz2` | 6,474 B | `b9bd3d7560e22a499f28c5bbdf6bd5615489ef33` ✔ | ok | 38,294 B |
| `20230504.2130.30.sas.a.rawacf.bz2` | 164,611 B | `5322874b0464d63b58b1263799668e0bcc970aac` ✔ | ok | 174,954 B |
| `1993092915ta.dat.bz2`（item 466） | 15,343 B | `31fd417c39b6a6c692bb60b7f8c636bb65a00cda` ✔（`199309.hashes`） | ok | 61,440 B |

**目录 URL 不能浏览**（它本身也会 302）。批量下载的做法是：用 3.2 取得清单，再逐个 `curl -L`。

### 3.4 文件格式：bz2 + DMap；纯 Python 头部窥视（`dmap_peek.py`）

DMap 按记录存储。每条记录以 4 个小端 int32 开头（code、size、标量数、数组数）。标量是“名字（以 NUL 结尾）+ 类型字节 + 值”，类型 9 是字符串。数组是“名字 + 类型 + 维数 + 各维长度（int32）+ 数据”。

```python
import bz2, struct, sys
SZ = {1:1, 2:2, 3:4, 4:4, 8:8, 10:8, 16:1, 17:2, 18:4, 19:8}
FMT = {1:'b', 2:'h', 3:'i', 4:'f', 8:'d', 10:'q', 16:'B', 17:'H', 18:'I', 19:'Q'}
def cstr(b, o):
    e = b.index(b'\0', o); return b[o:e].decode('ascii', 'replace'), e + 1
def records(b):
    o = 0
    while o + 16 <= len(b):
        code, size, ns, na = struct.unpack_from('<iiii', b, o)
        p = o + 16; sc = {}; arr = {}
        for _ in range(ns):
            name, p = cstr(b, p); t = b[p]; p += 1
            if t == 9: v, p = cstr(b, p)
            else: v = struct.unpack_from('<' + FMT[t], b, p)[0]; p += SZ[t]
            sc[name] = v
        for _ in range(na):
            name, p = cstr(b, p); t = b[p]; p += 1
            nd = struct.unpack_from('<i', b, p)[0]; p += 4
            dims = struct.unpack_from('<%di' % nd, b, p); p += 4 * nd
            n = 1
            for d in dims: n *= d
            if t == 9:
                for _ in range(n): _, p = cstr(b, p)
            else: p += n * SZ[t]
            arr[name] = dims
        yield code, size, sc, arr
        o += size
raw = bz2.decompress(open(sys.argv[1], 'rb').read())
recs = list(records(raw))
c, s, sc, arr = recs[0]
print("bytes", len(raw), "records", len(recs), "first record size", s, "scalars", len(sc), "arrays", len(arr))
for k in ("stid", "time.yr", "time.mo", "time.dy", "time.hr", "time.mt", "time.sc", "bmnum", "tfreq", "cp", "nrang", "mplgs", "origin.command", "combf"):
    if k in sc: print(" ", k, "=", sc[k])
print("  arrays:", {k: v for k, v in arr.items()})
last = recs[-1][2]
print("last record time %02d:%02d:%02d" % (last["time.hr"], last["time.mt"], last["time.sc"]), "beams", sorted({r[2]["bmnum"] for r in recs}))
```

```text
$ python3 dmap_peek.py 20230509.1834.01.cve.rawacf.bz2
bytes 38294 records 1 first record size 38294 scalars 49 arrays 6
  stid = 207   time = 2023-05-09 18:34:01   bmnum = 1   tfreq = 14713   cp = -151   nrang = 100   mplgs = 23
  origin.command = normalscan -sb 0 -eb 19 -fast -di -stid cve -nt 3 -dt 11
  arrays: {'ptab': (8,), 'ltab': (2, 24), 'slist': (100,), 'pwr0': (100,), 'acfd': (2, 23, 100), 'xcfd': (2, 23, 100)}
last record time 18:34:01 beams [1]

$ python3 dmap_peek.py 20230504.2130.30.sas.a.rawacf.bz2
bytes 174954 records 6 first record size 29159 scalars 47 arrays 6
  stid = 5   time = 2023-05-04 21:30:30   bmnum = 0   tfreq = 10800   cp = 157   nrang = 75   mplgs = 23
  origin.command = Borealis v0.6.1-6-g6f8560a NormalSound
  combf = Converted from Borealis file: /borealis_nfs/borealis_data/daily/20230504.2130.30.sas.0.rawacf.hdf5 record 1683235830051 ...
  arrays: {'ptab': (8,), 'ltab': (2, 24), 'pwr0': (75,), 'slist': (75,), 'acfd': (2, 23, 75), 'xcfd': (2, 23, 75)}
last record time 21:30:45 beams [0, 1, 2, 3, 4, 5]
```

（为了排版，上面把 `time.*` 这几行合并成了一行，其余照实际输出。）对 1993 年的 `.dat.bz2` 运行同一脚本会**报错**：DAT 是 DMap 之前的老格式，解压后是 61,440 B，不是 DMap。要用 RST 的转换工具（如 `dattorawacf`，**未测**），见坑 12。

**用 pydarnio 核对记录数**（只做这一件事）：

```python
import pydarnio, time
t = time.time(); r = pydarnio.read_rawacf("20230504.2130.30.sas.a.rawacf.bz2")   # 直接读 .bz2
print(type(r).__name__, len(r[0]), len(r[0][0]), round(time.time() - t, 2))
```

实测 sas 这个文件返回 `tuple`，**6** 条记录，每条 53 个键（= 47 个标量 + 6 个数组），耗时 0.01–0.02 s；cve 为 1 条记录、55 个键。两者都和 `dmap_peek.py` 一致。

### 3.5 FRDR Globus 与 Zip（只读页面，未执行）

- 数据集页上的 “Download with Globus” 按钮指向 `https://globus.frdr.ca/file-manager?origin_id=2d9df608-a085-4abc-8103-13d1ea6d49eb&origin_path=/7/published/publication_443/submitted_data`（这是 2014 年的例子）。页面说明 “requires a Globus account and installing software”，登录走 `auth.globus.org` OAuth。你需要在 File Manager 里把自己的 Globus Connect Personal 端点设为目标端。
- “Download as Zip” 是向 `/repo/download/request` 发 POST（带 `item_id`），页面 JS 里的 `downloadZipLimit` 是 160,000,000,000（160 GB），而整年数据有 4–6 TB。本文**没有**触发这个请求。

### 3.6 其他路线（一条命令一个结果）

```bash
curl -s https://api.bas.ac.uk/superdarn/mirror/v3/radars | head -c 300      # 200，3,019 B JSON：各雷达的 hdw.dat 文件及其 checksum（如 id 7 = hdw.dat.cve）
curl -s https://api.bas.ac.uk/superdarn/mirror/v3/files/1734977             # {"id":1734977,"filename":"1993092914g.dat.bz2","checksum":"f98040…"}
curl -sI https://api.bas.ac.uk/superdarn/mirror/v3 | head -1                # 301（base 必须带尾部斜杠）
curl -s -A Mozilla/5.0 https://vt.superdarn.org/data-download | grep -o 'Log in to access this tool'
curl -s -A Mozilla/5.0 https://superdarn.nssdc.ac.cn/ | grep -o 'href="/login"'
```

- BAS 的根路径还列出了 `/files`、`/files/:id`、`/files/blacklisted`、`/transferred/files/{ok,alarm,old,small,compression/…,blacklisted,notregular,nomatch}` 等路由。
- **不要**直接拉不带过滤的 `/files`，它返回 **354,360,370 B**（约 354 MB）的 JSON，而且 `?radar=` 这类参数会被忽略（坑 10）。从中流式 grep 到：`20230504.2130.30.sas.a` 的 id 是 2889329，checksum 与 FRDR 一致；`20230509.1834.01.cve` 的 id 是 2934753，checksum 为 `969d43e3…`，**与 FRDR 的 `b9bd3d…` 不同**（坑 9）。
- superdarn.ca 用 curl 访问会返回 JS 挑战页，要用浏览器看。页面上的 Globus 步骤是：
  1. 申请 Globus 账号；
  2. 安装 Globus Connect Personal 并激活端点；
  3. 发邮件给 superdarn@usask.ca（或填表），写明 Globus 用户名、要的数据类型（FITACF / MAP / everything）、单位和联系邮箱；
  4. 接受 group 邀请和 Rules of the Road；
  5. 在 File Manager 里找到集合 “SuperDARN Mirror”，目录按 `fitacf_30` / `fitacf_25` / `map` / 年 / 月组织。页面还说明**目录列表常超时，重试即可**；宽波束数据只能通过 Globus 获取。

## 4. 输入与输出

- **文件名**：`YYYYmmdd.HHMM.SS.<rad>.rawacf.bz2`，Borealis 雷达多一个通道字母，如 `….sas.a.rawacf.bz2`。老数据是 `YYYYMMDDHH<站字母>[a].dat.bz2`。每个文件**名义上**是一部雷达的 2 小时数据（readme 原文），实际上也可能很短（坑 8）。
- **校验文件**：每个月目录下有 `YYYYMM.hashes`（sha1）；1993 年另有 FRDR 生成的 `frdr-dfdr-checksums.txt`。
- **随数据集附带**：`<YYYY>RAWACF.readme.txt`（字段表、PI 名单、QA 流程）、`CITATION.txt`、`LICENSE.txt`。
- **雷达硬件文件**：hdw.dat 在 [github.com/SuperDARN/hdw](https://github.com/SuperDARN/hdw)（BAS 的 `/radars` 也有带 checksum 的副本）。
- **下游**：RAWACF 用 RST `make_fit` 生成 FITACF，再交给 [pydarn](./pydarn.md) 读图。

## 5. 参数

| 位置 | 参数 | 取值 / 说明 |
| --- | --- | --- |
| FRDR 文件 URL | `publication_<item>` | 按 3.1 的表取 item |
| | `submitted_data/<YYYY>/<MM>/<file>` | 月份两位数 |
| FRDR 清单 | `file_sizes.json` / `file_sizes-<sha256(相对路径)>.json` | 相对路径形如 `2023`、`2023/05`（**未公开**） |
| curl | `-L` | 必须加，用来跟随 302 |
| 合集页 | `offset=20&order=DESC&sort=2` | 分页 |
| BAS API | `/files/:id`、`/radars` | base 以 `/v3/` 结尾；**避免**不带过滤的 `/files` |
| VT 表单 | Date · Hemisphere · File Type（FitACF3 / FitACF / FitEX / Map2 / Grid2）· Radar | 需登录，15 次/天 |

## 6. 在工作流里接哪一步

- **路径 B · 不规则体 / 磁暴**（[README](./README.md#b--不规则体--磁暴)）：磁暴期间用高纬对流（MAP）和 HF 回波（FITACF）去对照 GNSS ROTI / TEC 斑块；原始 RAWACF 先按本文取，再用 RST 做 fit，然后交给 [pydarn](./pydarn.md) 画图。
- **路径 A · 一日 TEC**（[README](./README.md#a--一日-tec)）：一般用不上；只有需要中纬 TID 的 HF 旁证时，才按日期和雷达挑单个文件。
- ISR 剖面和 Madrigal TEC 见 [madrigal](./madrigal.md)；地磁时间轴见 [geomag-api](./geomag-api.md)。

## 7. 坑（现象 → 原因 → 修复）

1. **找不到列目录的 API** → FRDR 没有公开接口 → 用 3.2 的 `file_sizes.json`，子目录对相对路径取 sha256；对完整路径或只对 `"05"` 取都会 404。它**未公开**，失效时回到网页或 Globus。
2. **打开目录 URL 得到 302，而不是文件列表** → FRDR 文件端不支持浏览目录 → 先取清单，再逐个下载。
3. **`curl -O` 得到的只是几百字节的 HTML 或空文件** → 下载地址先 302 到 `*.data.globus.org` → 加 `-L`。
4. **一个“小测试”下了几十 GB** → 整年 4–6 TB，月中位文件约 33 MB → 用清单里的 `size` 挑最小的文件，测完就删。
5. **在 FRDR 上找不到 fitacf 或 map** → FRDR 只发布 RAWACF 和老 DAT → FITACF / MAP 去 SuperDARN Canada 的 Globus group 或 VT（需登录）申请，或者用 RST 自己从 RAWACF 生成。
6. **最新一年的数据不在 FRDR** → 发布滞后约 1–2 年（2023 年数据 2025-09-18 才上线）→ 近期数据走镜像（Globus / BAS）。
7. **许可证自相矛盾** → 2023 的 `LICENSE.txt` 是 CC BY 4.0（2014 的页面也链接到 CC BY 4.0），但 2023 的 readme 写 CC BY-NC 4.0，1993 的 `LICENSE.txt` 也是 CC BY-NC 4.0，Rules of the Road 还写明 “not to be used for commercial purposes” → **按更严的非商业条款执行**。
8. **某些时段缺文件，或者文件里只有 1 条记录** → readme 说明：discretionary（自选）模式的数据**禁发一年**，损坏文件和黑名单文件（投运前数据、禁发期数据）会被直接剔除；有的文件只截到一个扫描片段（cve 那个 6 KB 文件只有 1 条记录、1 个波束）→ 用之前数一下记录数；想知道自选模式的细节就联系该雷达 PI。
9. **同名文件在两个镜像的 sha1 不一样** → 实测 `20230509.1834.01.cve.rawacf.bz2` 在 FRDR 是 `b9bd3d…`，在 BAS 是 `969d43e3…`（而 sas.a 那个文件两边一致）→ **只用同一来源自己的 hashes 校验**，不要跨镜像混用；混用时以 readme 描述的 QA 流程为准，有疑问就问 PI 组。
10. **BAS `/files` 卡住或把磁盘写满** → 不带过滤时会返回 354 MB 的 JSON，查询参数被忽略 → 按 id 查 `/files/:id`，或者流式 `grep` 而不落盘；base 不带尾部斜杠会返回 301。
11. **文件名里多了 `.a.`** → Borealis 雷达转换产物带通道字母，`combf` 里记录了原始 HDF5 文件名 → 通配时写 `*.sas*.rawacf.bz2`，不要写死成 `*.sas.rawacf.bz2`。
12. **1993–2006 年的文件用 DMap 读取器报错** → `.dat` 是 DMap 之前的老格式 → 用 RST 转换（未测），或者只用 2005 年以后的 RAWACF。
13. **`pydarnio.SDarnRead` 报 AttributeError** → pydarnio 2.1 换了 API → 用 `pydarnio.read_rawacf(path)`，它直接读 `.bz2`，返回 tuple，默认 `mode='lax'`。
14. **superdarn.ca 用 curl 访问得到一段脚本** → 站点有 JS 反爬挑战 → 用浏览器阅读；不要绕过它，这个站本来就不提供脚本下载入口。
15. **以为 FRDR 的 Globus 按钮点开就能批量下载** → 要有 Globus 账号，并安装 Globus Connect Personal 作为目标端点；SuperDARN Canada 镜像还要额外人工审批 group → 提前几天发申请邮件。

## 8. 选型对比

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 历史 RAWACF，几个文件 | **FRDR HTTPS** + `file_sizes.json` | 无账号，有 sha1，有 DOI |
| 历史 RAWACF，整月或整年 | FRDR **Globus**（或 BAS rsync） | TB 级数据只能批量传；两者都要账号 |
| FITACF / MAP，全网 | **SuperDARN Canada Globus group** | 官方镜像，按 `fitacf_30` / `map` / 年 / 月组织；需邮件申请 |
| 少量 FITACF3 / Map2 / Grid2 | VT Data Download | 需登录，15 次/天 |
| 加拿大 5 部雷达的 FITACF 3.0 | superdarn.ca 网页表单 | 只能用浏览器 |
| 最近几个月的数据 | Globus / BAS 镜像 | FRDR 滞后 1–2 年 |
| 核对某个文件的 checksum 或 hdw.dat | BAS API `/files/:id`、`/radars` | 公开，无需账号 |
| 读图、画 RTI / 对流图 | [pydarn](./pydarn.md) | 本文不讲 |

### 数据使用规则（Rules of the Road，原文摘录自 2023 readme）

- **PI 联系**："When data from an individual radar or radars are used, users must contact the principal investigator(s) of those radar(s) to obtain the appropriate acknowledgement information and to offer collaboration, where appropriate." PI 名单和邮箱见 readme，例如 cve/cvw/ice/icw → Dartmouth（Simon Shepherd）；sas/cly/inv/pgr/rkn → USask（glenn.hussey@usask.ca）；fir → BAS（gchi@bas.ac.uk）；fhe/fhw/gbr/kap → VT（mikeruo@vt.edu）。
- **标准致谢**："The authors acknowledge the use of SuperDARN data. SuperDARN is a collection of radars funded by national scientific funding agencies of Australia, Canada, China, France, Italy, Japan, Norway, South Africa, United Kingdom and the United States of America."
- **禁发期**："some data are embargoed for use by designated Principal Investigators for a period of one year."（readme 还说明 discretionary 时段的数据一年后放出。）
- **开放与限制**：开放数据政策，事先不需要许可，但 "strongly encouraged to establish early contact with any Principal Investigator"；"The SuperDARN Executive Council … must be notified before data are redistributed through another database. The data are not to be used for commercial purposes."
- **数据集引用**（2023 `CITATION.txt`）："Super Dual Auroral Radar Network, -. (2025). SuperDARN 2023 RAWACF. Federated Research Data Repository. https://doi.org/10.20383/103.01307"
- **推荐论文**：Greenwald 1995（doi:10.1007/BF00751350）、Chisham 2007（doi:10.1007/s10712-007-9017-8）、Nishitani 2019（doi:10.1186/s40645-019-0270-5）。按雷达生成的致谢文本和 PI 联系表，用 VT 的 [Data Acknowledgement Tool](https://vt.superdarn.org/data-acknowledgement) 和 [Data Validation Tool](https://vt.superdarn.org/data-usage)。
