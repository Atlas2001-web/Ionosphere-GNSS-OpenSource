# ntripstreams · NTRIP 协议通信操作手册

目录：[`PROJECTS.json` → `ntripstreams`](../../PROJECTS.json) · 上游 <https://github.com/stenseng/ntripstreams> · PyPI **`ntripstreams` 0.3.5** · tip **`889ffb9`** · MIT · Python ≥3.10 · 依赖 `bitstring`≥4.4 · 本机验证 0.3.5（CLI 拉 **rtk2go** / **igs-ip** 公开 sourcetable；`NtripStream.requestSourcetable` API；无订户时未订流；`Rtcm3` 解上游 `tests/data` 样帧 + `AgPartner_2.rtcm3` 251 帧；1029 编码；`crc24q`/`crcNmea`）· 2026-09-24 04:53 EDT · **质检复跑通过**（rtk2go **767**/STR**765**；igs-ip **391**/STR**384**/status **200**；无订户订流 `ConnectionError` HTTP **400**；AgPartner_2 **251** 帧/nTypes **19**；1005/1077 CRC；`nmea_crc 47`；tip `889ffb9`；2026-09-24 04:59 EDT）

> 岗位：Python **asyncio NTRIP 客户/服务端握手** + 内置 **RTCM 3 帧编解码（部分消息）**。冲突时：**上游 README / `ntripstreams -h` / 本机 `help(NtripStream)` > 本文**。更完整 CLI/多协议录流 → [pygnssutils](./pygnssutils.md)；生产多用户 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)；多流 GUI 录盘 → [bnc](./bnc.md)；NMEA 专用编解码 → [pynmeagps](./pynmeagps.md)；深度 RTCM3/MSM → [pyrtcm](./pyrtcm.md)。

## 1. 用途与边界

**做：**

- CLI `ntripstreams <url>`：拉 caster **sourcetable**（只读，通常无需口令）
- CLI `-m MOUNT -u/-p`：订挂载点流；`-s` 以上传端推流；`-1` 走 NTRIP 1.x
- 库 `NtripStream`：`requestSourcetable` / `requestNtripStream` / `getRtcmFrame` / `requestNtripServer` / `sendRtcmFrame`
- 库 `Rtcm3`：帧级 `decodeRtcmFrame`；遗留观测 1001–1004 / 1009–1012 与 MSM 1071–1127 字段解析；`encodeRtcmMessage` **目前仅 1029**；`messageDescription` / `constellation` / `msmSignalTypes` / `mjd`
- `crc24q`（RTCM CRC-24Q）、`crcNmea`（NMEA XOR）

**不做：**

- **不是** 多协议一站式录流 CLI（NMEA/UBX/RTCM/SPARTN 混流）→ [pygnssutils](./pygnssutils.md)（`gnssstreamer` / `gnssntripclient`）
- **不是** 生产多挂载点高并发 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** 多流 GUI / 运维录盘主力 → [bnc](./bnc.md)
- **不是** 完整 RTCM3 生态（1005 ARP 坐标等大量类型仅「认类型名」，字段解码覆盖有限）→ 深解用 [pyrtcm](./pyrtcm.md)
- **不是** NMEA 专用结构化读写 → [pynmeagps](./pynmeagps.md)（本包仅提供 `crcNmea`）
- **不是** 定位 / TEC / PPP → 落盘后走 [rtklib](./rtklib.md) / [georinex](./georinex.md) / [pytecgg](./pytecgg.md)

一句话：ntripstreams = **轻量 asyncio NTRIP 握手 + 够用的 RTCM3 帧工具**；电离层产品仍在「流落盘 → RINEX/改正」之后。

| 符号 | 含义 |
| --- | --- |
| sourcetable | caster 公开挂载点表；行以 `CAS;`/`NET;`/`STR;` 开头，以 `ENDSOURCETABLE` 结束 |
| `NtripStream` | 单连接异步客户/服务端状态机 |
| `getRtcmFrame` | 缓冲对齐 preamble `0xD3`，CRC-24Q 校验后返回完整帧 |
| MSM | Multiple Signal Message（1071–1127） |
| `Bedrock_Solutions_NtripClient/0.3.5` | 本机 User-Agent 字符串（包内硬编码名前缀） |
| env | `NTRIP_URL` / `NTRIP_MOUNTPOINT` / `NTRIP_USER` / `NTRIP_PASSWORD` / `NTRIP_LOGFILE` |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv ntripstreams-demo/.venv
source ntripstreams-demo/.venv/bin/activate
python -m pip install -U pip
python -m pip install 'ntripstreams==0.3.5'
python -c "import importlib.metadata as m; print(m.version('ntripstreams'))"
# 期望：0.3.5
ntripstreams -h
python -c "from ntripstreams import NtripStream, Rtcm3; print(NtripStream, Rtcm3)"
```

纯库轮子（`py3-none-any`）；本机另需出网才能拉公开 sourcetable。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'ntripstreams'` | 未激活 venv | `source …/.venv/bin/activate` |
| `bitstring` 报 `=name` 标签错 | 旧 bitstring | 钉 `ntripstreams==0.3.5`（要求 `bitstring>=4.4,<5`） |
| CLI 无输出 / 卡住 | caster 拒连或慢 | 先 `ntripstreams http://igs-ip.net:2101`；超时用 `timeout 30` |

## 3. 端到端（本机 0.3.5 真跑；质检复跑 2026-09-24 04:59 EDT）

本机**无 NTRIP 订户口令**：下列含 **公开 sourcetable** + **本地 API/样帧**；订流在无认证时会 400（见 §3.4 / 坑表）。stdout **摘自实跑**，挂载点数随 caster 变化，勿当金样。

### 3.1 CLI：拉公开 sourcetable

```bash
source ~/iono_ops/ntripstreams-demo/.venv/bin/activate
# 摘前几行可 head；精确计数请整表落盘（避免 BrokenPipe，见坑 #13）
ntripstreams http://rtk2go.com:2101 | head -5
ntripstreams http://rtk2go.com:2101 > /tmp/rtk2go_st.txt
wc -l /tmp/rtk2go_st.txt; grep -c '^STR;' /tmp/rtk2go_st.txt
ntripstreams http://igs-ip.net:2101 | head -8
ntripstreams http://igs-ip.net:2101 > /tmp/igsip_st.txt
wc -l /tmp/igsip_st.txt; grep -c '^STR;' /tmp/igsip_st.txt
```

**本机 stdout（摘录）：**

```text
STR;aamakinen;Evijarvi;RTCM 3.2;1005(1), 1077(1), 1084(1), 1097(1), 1127(1), 1230(1);2;GPS+GLO+GAL+BeiDou;SNIP;FIN;63.36;23.36;1;0;SNIP;none;B;N;6880;
STR;AgPartner_2;Bendorzyn;RTCM 3.3;1004(1), 1005(10), 1007(31), 1008(10), 1012(1), 1033(10), 1042(4), 1046(1), 1075(1), 1077(1), 1085(1), 1087(1), 1095(1), 1097(1), 1107(1), 1125(1), 1127(1), 1230(31);2;GPS+GLO+GAL+BeiDou+SBAS;SNIP;POL;52.70;19.57;1;0;SNIP;none;B;N;19700;
…
767
CAS;igs-ip.net;2101;IGS-IP;BKG;0;DEU;50.12;8.69;0.0.0.0;0;http://igs-ip.net/home
CAS;rtcm-ntrip.org;2101;NtripInfoCaster;BKG;0;DEU;50.12;8.69;0.0.0.0;0;http://rtcm-ntrip.org/home
NET;EUREF;EUREF;B;N;https://igs.bkg.bund.de/root_ftp/NTRIP/streams/streamlist_euref-ip.htm;…
NET;IGS;IGS;B;N;https://igs.bkg.bund.de/root_ftp/NTRIP/streams/streamlist_igs-ip.htm;…
STR;ABMF00GLP0;Les-Abymes;RTCM 3.3;1006(30),1007(30),1008(30),1013(30),1019,1020,1033(30),1042,1045,1046,1074(1),1084(1),1094(1),1104(1),1114(1),1124(1),1230(30);2;GPS+GLO+GAL+BDS+QZS+SBAS;IGS;GLP;16.26;-61.53;0;0;SEPT POLARX5;none;B;N;10400;rgp-ip.ign.fr:2101/ABMF00GLP7(1)
STR;ABPO00MDG0;Antananarivo;RTCM 3.2;1076(1);2;GPS;IGS;MDG;-19.02;47.23;0;0;SEPT POLARX5;none;B;N;3800;…
384
```

| caster | 本机行数要点（2026-09-24） |
| --- | --- |
| `http://rtk2go.com:2101` | **767** 行：`STR` **765** + `NET` 1 + `ENDSOURCETABLE` |
| `http://igs-ip.net:2101` | **391** 行：`CAS` 2 + `NET` 4 + `STR` **384** + `ENDSOURCETABLE` |

### 3.2 库：`requestSourcetable`（asyncio）

```bash
python - <<'PY'
import asyncio
from ntripstreams import NtripStream

async def main():
    ns = NtripStream()
    lines = await ns.requestSourcetable("http://igs-ip.net:2101")
    strs = [x for x in lines if x.startswith("STR;")]
    print("lines", len(lines), "STR", len(strs), "status", ns.ntripResponseStatusCode)
    print("first", lines[0][:72])
    print("ABMF", [x for x in lines if "ABMF00GLP0" in x][0][:96])
    print("last", lines[-1])

asyncio.run(main())
PY
```

**本机 stdout：**

```text
lines 391 STR 384 status 200
first CAS;igs-ip.net;2101;IGS-IP;BKG;0;DEU;50.12;8.69;0.0.0.0;0;http://igs-ip.net/home
ABMF STR;ABMF00GLP0;Les-Abymes;RTCM 3.3;1006(30),1007(30),1008(30),1013(30),1019,1020,1033(30),1042,1045,
last ENDSOURCETABLE
```

rtk2go 同 API：**767** 行 / `STR` **765** / `status 200`。

### 3.3 本地：构造请求头 + `Rtcm3` 解码样帧

```bash
# 上游样帧（clone 一次即可）
git clone --depth 1 https://github.com/stenseng/ntripstreams.git ~/iono_ops/ntripstreams

python - <<'PY'
from ntripstreams import NtripStream, Rtcm3, crc24q, crcNmea
from bitstring import BitStream
import json, time, os, glob

ns = NtripStream()
ns.setRequestSourceTableHeader("http://igs-ip.net:2101")
print(ns.ntripRequestHeader.decode("ISO-8859-1").splitlines()[0])
print([ln for ln in ns.ntripRequestHeader.decode("ISO-8859-1").splitlines() if ln.startswith("User-Agent")][0])

r = Rtcm3()
print("mjd_now", r.mjd(time.time()), "mjd_20150323", r.mjd(1427124600))
print("const", r.constellation(1077), r.constellation(1124), r.messageDescription(1005))

root = os.path.expanduser("~/iono_ops/ntripstreams/tests/data")
fix = json.load(open(os.path.join(root, "rtcm3_samples.json")))
hex1005 = fix["aamakinen"]["sample_frames_hex"]["1005"]
hex1077 = fix["aamakinen"]["sample_frames_hex"]["1077"]
for label, hx in (("1005", hex1005), ("1077", hex1077)):
    frame = BitStream(bytes.fromhex(hx))
    crc_ok = crc24q(frame[:-24]) == frame[-24:].uint
    mt, data = r.decodeRtcmFrame(frame)
    extra = ""
    if mt in range(1071, 1128):
        sigs = r.msmSignalTypes(mt, data[0][10])
        extra = f" sigs={sigs}"
    print(label, "mt", mt, "crc_ok", crc_ok, "bytes", len(frame) // 8, extra)

path = sorted(glob.glob(os.path.join(root, "samples", "*.rtcm3")))[0]
raw = open(path, "rb").read()
i = n = 0
types = {}
while i < len(raw):
    if raw[i] != 0xD3:
        i += 1
        continue
    length = ((raw[i + 1] & 0x03) << 8) | raw[i + 2]
    flen = 3 + length + 3
    if i + flen > len(raw):
        break
    payload = BitStream(raw[i + 3 : i + 3 + length])
    mt = payload.peek("uint:12")
    types[mt] = types.get(mt, 0) + 1
    r.decodeRtcmMessage(payload)
    n += 1
    i += flen
print(os.path.basename(path), "bytes", len(raw), "frames", n, "nTypes", len(types))

enc = r.encodeRtcmMessage(1029, {"refStationId": 7, "string": "HELLO NTRIP", "utfChars": 11, "charBytes": 11})
print("enc1029_hex", enc.tobytes().hex())
body = BitStream(b"GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
print("nmea_crc", crcNmea(body).hex)
PY
```

**本机 stdout：**

```text
GET / HTTP/1.1
User-Agent: NTRIP Bedrock_Solutions_NtripClient/0.3.5
mjd_now 61307 mjd_20150323 57104
const GPS BEIDOU Stationary RTK Reference Station ARP
1005 mt 1005 crc_ok True bytes 25 
1077 mt 1077 crc_ok True bytes 226  sigs=['L1C', 'L2L']
AgPartner_2.rtcm3 bytes 48814 frames 251 nTypes 19
enc1029_hex 405007ef7b3e8b0b0b48454c4c4f204e54524950
nmea_crc 47
```

（`enc1029` 中间 MJD/UTC 字段随墙钟变；上例前缀 `405007` + 后缀 ASCII `HELLO NTRIP` 稳定。`nmea_crc 47` 对齐经典 GGA 句尾 `*47`。）

### 3.4 订流（需口令；本机无订户）

```bash
# 典型：rtk2go 常要求合法邮箱作用户名；口令用环境变量，勿进 git
export NTRIP_USER='you@example.com'
export NTRIP_PASSWORD='your_pass'
ntripstreams http://rtk2go.com:2101 -m aamakinen -u "$NTRIP_USER" -p "$NTRIP_PASSWORD" -v
```

**本机无口令时** `requestNtripStream(..., "aamakinen")` → **`ConnectionError: … HTTP/1.1 400`**（日志 `Response error 400!`）。sourcetable 仍可匿名拉。有订户后再用 `-v` 看解码行；深度 MSM/1005 坐标建议旁路 [pyrtcm](./pyrtcm.md)。

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `ntripstreams URL` | GET `/` → 打印 sourcetable |
| `ntripstreams URL -m M …` | GET `/M` 订流；可重复 `-m` |
| `-s` | 服务端上传模式（`requestNtripServer`） |
| `-1` | NTRIP 1.x |
| `-l FILE` / `-v` | 日志文件 / 提高啰嗦等级 |
| `NtripStream.requestSourcetable(url) → list[str]` | 异步拉全表 |
| `requestNtripStream(url, mount, user=, passwd=)` | 客户订流 |
| `getRtcmFrame() → (BitStream, …)` | 下一完整 CRC-OK 帧 |
| `requestNtripServer` / `sendRtcmFrame` | 上传端 |
| `Rtcm3.decodeRtcmFrame` / `decodeRtcmMessage` | 解帧 / 解载荷 |
| `encodeRtcmMessage(1029, dict)` | 目前唯一定稿编码类型 |
| `crc24q` / `crcNmea` | RTCM / NMEA 校验 |

| `STR;` 字段（节选） | 含义 |
| --- | --- |
| 挂载名 | 如 `ABMF00GLP0` / `aamakinen` |
| 格式 | `RTCM 3.x` / `CMR+` 等 |
| 消息列表 | `1005(10),1077(1),…`（括号多为周期秒） |
| 纬经 | 概略位置；`0.00;0.00` 可能未填 |

环境变量可替 CLI 缺省；**命令行优先于环境变量**。

## 5. 接到哪步

```text
公开 caster / 实验室 caster
  → ntripstreams 拉 sourcetable / 订 RTCM 流
  →（可选）Rtcm3 粗解码 或 pyrtcm 深解
  → 录盘 → georinex / rtklib / pytecgg
运维多流：bnc；自建 caster：bkg-ntripcaster
脚本化多协议：pygnssutils；NMEA 句：pynmeagps
```

路径 C（实时差分）：[pygnssutils](./pygnssutils.md) / **ntripstreams（本文）** / [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 订流 `HTTP/1.1 400` / `ConnectionError` | 无用户或 caster 拒匿名订流 | 配 `NTRIP_USER`/`PASSWORD`；rtk2go 常用邮箱作用户名 |
| 2 | sourcetable 空 / 超时 | 防火墙拦 2101 或 URL 缺端口 | 显式 `:2101`；先 `curl -v telnet://host:2101` 或换 `igs-ip.net` |
| 3 | `https://…` 失败 | TLS/端口与文档不符 | 多数公开 caster 仍是 **明文 2101**；仅文档写明 TLS 时用 `https` |
| 4 | MSM 解出 `sigs=['Res', …]` | 信号掩码首位为保留位 | 以 RINEX 码名为准；对照 `msmSignalTypes` 与 [pyrtcm](./pyrtcm.md) |
| 5 | `encodeRtcmFrame` 无 preamble/CRC | 上游注明 wrapper 未完成 | 自拼 `0xD3`+长度+载荷+`crc24q`；或改用 pyrtcm 编码 |
| 6 | `encodeRtcmMessage(1005, …)` → `None` | 仅 **1029** 已实现编码 | 只拿 1029 做冒烟；其它类型用外部工具生成 |
| 7 | `messageDescriptionText` 当函数调 | 它是 **dict**；可调用的是 `messageDescription(mt)` | `r.messageDescription(1005)` |
| 8 | User-Agent 含 `Bedrock_Solutions_…` | 包内历史客户端名 | 勿改期望字符串做兼容检测；以版本号为准 |
| 9 | 挂载名带前导 `/` | CLI/API 要 **无** 斜杠 | `-m ABMF00GLP0` 而非 `-m /ABMF00GLP0` |
| 10 | 口令进 git / 进手册 | 环境变量未隔离 | 只用 env/`chmod 600` conf；示例用占位符 |
| 11 | 与 pygnssutils 行为不一致 | 两套栈（asyncio 轻量 vs semuconsulting 全家桶） | 选型见 §7；勿混期望同一旗标 |
| 12 | 期望本库出固定解 / TEC | 职责仅协议+部分 RTCM | 改正进接收机或 PPP；TEC → [georinex](./georinex.md)/[pytecgg](./pytecgg.md) |
| 13 | `| head` 后 stderr `Broken pipe` / `BrokenPipeError` | CLI 写满 stdout 被 `head` 关管道 | 计数用重定向：`ntripstreams URL > /tmp/st.txt` 再 `wc`/`grep`；或 `… 2>/dev/null | head` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本里 asyncio 拉 sourcetable / 订一流 | **ntripstreams（本文）** |
| 多协议 CLI 录流 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 生产多用户 NTRIP caster | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 多流 GUI 运维录盘 | [bnc](./bnc.md) |
| RTCM3 深解（含 1005 llh、MSM 表） | [pyrtcm](./pyrtcm.md) |
| NMEA 0183 结构化读写 | [pynmeagps](./pynmeagps.md) |
| 桌面监视 / 灌板 | [pygpsclient](./pygpsclient.md) |
| RTK / PPP 解算 | [rtklib](./rtklib.md) |

相关：上游 README · [pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [bnc](./bnc.md) · [pynmeagps](./pynmeagps.md) · [pyrtcm](./pyrtcm.md) · [pygpsclient](./pygpsclient.md) · 教程 [06](../tutorials/06-iono-positioning.md) · [data-access 实时](../data-access.md#实时-rtcm--ssr--ntrip)
