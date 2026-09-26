# go-gnss-rtcm · go-gnss/rtcm（Go RTCM3 解析库）操作手册

目录：[`PROJECTS.json` → `go-gnss-rtcm`](../../PROJECTS.json) · 上游 <https://github.com/go-gnss/rtcm> · 最新标签 **`v0.0.9`** = master tip **`6948afc`**（2026-09-16 06:51 EDT；`Add frame deserialization from []byte`；上一版 v0.0.8 `74819e4` 2026-03-11）· **Apache-2.0** · ★**26** · go.mod **`go 1.22`** · 纯库 + 示例 `cmd/ntriplatency` · 本机 **go1.24.4**（**R10质检复跑** 2026-09-26 03:01–03:05 EDT）：centipede `VALDM` 真流 **53248 B / 358 帧**，类型计数与 pyrtcm **1.2.0** 全等；191 帧 MSM 的 NSat **逐帧一致**；358 帧**重编码逐字节一致**。

> 一句话：把 RTCM3 字节流切帧、校 CRC24Q、按消息号解成 Go struct，也能把 struct 编回字节。**不是 NTRIP 客户端**（同组织 [ntrip-go](./ntrip-go.md) 负责），**不是 RTK 解算器**，**不是 RINEX 转换器**；MSM 只给原始 DF 整数，米/dBHz 要自己乘。

## 1. 用途与边界

| 做 | 不做 |
| --- | --- |
| `Scanner` 从 `io.Reader` 逐帧读（坏前导/坏 CRC 自动逐字节跳过） | 连 caster、发 GGA（用 `go-gnss/ntrip`） |
| `DeserializeMessage`：**91** 个消息号（按 `message.go` switch 实数）→ 具体类型；其余 → `MessageUnknown{Payload}` | 定位 / 模糊度 / 差分改正（用 [rtklib](./rtklib.md)） |
| 每个类型都有 `Serialize()`；`EncapsulateMessage` 补帧头 + CRC | 写 RINEX（用 [rtcm3torinex](./rtcm3torinex.md) / `convbin`） |
| MSM 时间：`DF004` / `DF427` / `GlonassTimeMSM` 等 | MSM 自动算伪距/相位（只给 DF397/398/405… 整数） |

91 个消息号：观测 1001–1004、1009–1012；站/天线 1005–1008、1033；星历 1019/1020/1042/1044/1045/1046；辅助 1013/1029/1230；网络 RTK 1014–1017、1030–1032、1037–1039；坐标变换 1021–1027；FKP 1034/1035；SSR 1057–1060、1063–1066；MSM1–7 × GPS/GLO/GAL/SBAS/QZSS/BDS（1071–1127，共 42 个）。**没有** 1041（NavIC）、1131+（NavIC MSM）、4xxx 私有报文（落 `MessageUnknown`）。

同组织：`go-gnss/ntrip`（★62，NTRIP 客户端/服务端，本库 go.mod 依赖 v0.0.14，见 [ntrip-go](./ntrip-go.md)）；另有 `rinex`/`spartn`/`sinex`/`sbf` 小库（★0–5；前三个最后推送 2020–2022，`sbf` 2025-07）。

## 2. 安装

```bash
go get github.com/go-gnss/rtcm@v0.0.9     # 仅子包 rtcm3 有 API
# 依赖：bamiaux/iobit（位读写，读越界不报错）、go-restruct/restruct、go-gnss/ntrip（仅示例用）
git clone https://github.com/go-gnss/rtcm && cd rtcm && go test ./...
# ok  github.com/go-gnss/rtcm/rtcm3  0.109s   ← 本机 9 个 Test* 全 PASS，无子测试
```

系统 go1.24.4 满足 `go 1.22`，无需另装。测试覆盖：`data/*_frame.bin` **69** 个样帧的解→编往返、帧层、DF004/DF034/DF386/DF427 时间换算；**无**任何坏输入测试。

## 3. 端到端（本机真跑）

### 3.1 真实输入：centipede `VALDM` 录 40 s

```bash
timeout 40 curl -s -H 'Ntrip-Version: Ntrip/2.0' -u centipede:centipede \
  http://caster.centipede.fr:2101/VALDM -o valdm.rtcm
# 实录 2026-09-26 03:01:34–03:02:14 EDT；curl exit 124；53248 B，sha256 前 12 位 4b5f6ad03ea0
# 首字节 d3 00 b4（curl 已剥 HTTP/chunked）；末尾 11 B 为被 timeout 截断的残帧
# 1033 自报 "RTKBase Ublox_ZED-F9P" fw "2.3.4"（天线描述 ADVNULLANTENNA）
```

### 3.2 解码 + 计数 + 取字段（`main.go`，完整可编）

```go
package main

import (
	"fmt"
	"io"
	"math/bits"
	"os"
	"sort"

	"github.com/go-gnss/rtcm/rtcm3"
)

const c = 299792458.0

func ids(mask uint64, n int) (out []int) { // MSB = ID 1
	for i := 0; i < n; i++ {
		if mask&(1<<uint(n-1-i)) != 0 {
			out = append(out, i+1)
		}
	}
	return
}

func main() {
	f, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	sc := rtcm3.NewScanner(f)
	count, total, unknown, msmDone := map[int]int{}, 0, 0, false
	for {
		msg, err := sc.NextMessage()
		if err == io.EOF {
			break
		} else if err != nil {
			fmt.Println("error:", err)
			break
		}
		total++
		count[msg.Number()]++
		if _, ok := msg.(rtcm3.MessageUnknown); ok {
			unknown++
		}
		switch m := msg.(type) {
		case rtcm3.Message1005:
			if count[1005] == 1 {
				fmt.Printf("1005 sta=%d ECEF=(%.4f, %.4f, %.4f) m\n", m.ReferenceStationId,
					float64(m.ReferencePointX)*1e-4, float64(m.ReferencePointY)*1e-4, float64(m.ReferencePointZ)*1e-4)
			}
		case rtcm3.Message1006:
			fmt.Printf("1006 sta=%d ECEF=(%.4f, %.4f, %.4f) m H=%.4f m\n", m.ReferenceStationId,
				float64(m.ReferencePointX)*1e-4, float64(m.ReferencePointY)*1e-4, float64(m.ReferencePointZ)*1e-4,
				float64(m.AntennaHeight)*1e-4)
		case rtcm3.Message1077:
			if msmDone {
				continue
			}
			msmDone = true
			h, sd, gd := m.MsmHeader, m.SatelliteData, m.SignalData
			sats := ids(h.SatelliteMask, 64)
			fmt.Printf("1077 first: epoch(DF004)=%d ms t=%s nsat=%d nsig=%d ncell=%d\n", h.Epoch,
				m.Time().UTC().Format("15:04:05.000"), bits.OnesCount64(h.SatelliteMask),
				bits.OnesCount32(h.SignalMask), bits.OnesCount64(h.CellMask))
			fmt.Printf("  sats=%v sigIDs=%v\n", sats, ids(uint64(h.SignalMask), 32))
			fmt.Printf("  G%02d raw: ms=%d ext=%d rough=%d rate=%d\n", sats[0], sd.RangeMilliseconds[0],
				sd.Extended[0], sd.Ranges[0], sd.PhaseRangeRates[0])
			fmt.Printf("  cell0 raw: finePR=%d finePh=%d lock=%d half=%v cnr=%d finerate=%d\n",
				gd.Pseudoranges[0], gd.PhaseRanges[0], gd.PhaseRangeLocks[0], gd.HalfCycles[0], gd.Cnrs[0], gd.PhaseRangeRates[0])
			rough := float64(sd.RangeMilliseconds[0]) + float64(sd.Ranges[0])/1024
			pr := (rough + float64(gd.Pseudoranges[0])/(1<<29)) * c / 1000
			fmt.Printf("  cell0 PR=%.3f m CNR=%.4f dBHz (hand-scaled)\n", pr, float64(gd.Cnrs[0])/16)
		}
	}
	keys := []int{}
	for k := range count {
		keys = append(keys, k)
	}
	sort.Ints(keys)
	fmt.Printf("frames=%d unknown=%d\n", total, unknown)
	for _, k := range keys {
		fmt.Printf("%d:%d ", k, count[k])
	}
	fmt.Println()
}
```

### 3.3 真实 stdout（`go run . valdm.rtcm`）

```text
1077 first: epoch(DF004)=543713000 ms t=07:01:35.000 nsat=11 nsig=2 ncell=20
  sats=[1 2 3 4 6 9 11 17 19 28 31] sigIDs=[2 16]
  G01 raw: ms=77 ext=0 rough=717 rate=743
  cell0 raw: finePR=72331 finePh=-511535 lock=649 half=false cnr=752 finerate=-378
  cell0 PR=23293972.930 m CNR=47.0000 dBHz (hand-scaled)
1005 sta=0 ECEF=(4151313.6403, 380499.3117, 4811408.2782) m
1006 sta=0 ECEF=(4151313.6403, 380499.3117, 4811408.2782) m H=0.0000 m
frames=358 unknown=0
1004:39 1005:4 1006:1 1008:4 1012:39 1019:11 1020:28 1033:4 1042:9 1046:27 1077:39 1087:38 1097:38 1107:38 1127:38 1230:1
```

- 首个 MSM 是 1077：**11 星 / 2 信号 / 20 格**；信号 ID 2、16 = **1C、2L**（F9P L1C/A + L2C）。
- 伪距按 $\rho = \dfrac{c}{1000}\left(N_{\mathrm{ms}} + \dfrac{r}{1024} + \Delta\rho \cdot 2^{-29}\right)$（单位 m；$N_{\mathrm{ms}}$=DF397，$r$=DF398，$\Delta\rho$=DF405）自己拼；CNR = DF408 × 2⁻⁴ dBHz。
- `t=07:01:35` UTC 与录流时间（07:01 UTC）一致——但这是 `Time()` 拿**当前系统时钟**推周（见坑 3）。
- 1005/1006 的 `sta=0`、天线高 0 m、ECEF 与上次录流相同：站方配置如此，与 pyrtcm 一致。

### 3.4 交叉核对（pyrtcm 1.2.0，同一文件）

| 项 | go-gnss/rtcm | pyrtcm | 结论 |
| --- | --- | --- | --- |
| 总帧 / 类型计数 | 358；16 种（见上） | 358；16 种逐项同数 | 一致 |
| MSM NSat（1077×39 + 1087/1097/1107/1127×38） | 11/8/9/**0**/8 | 同，**191 行 diff 为空** | 一致 |
| 1005 ECEF | 4151313.6403, 380499.3117, 4811408.2782 m | …, 4811408.2782000005 m | 一致（f64 表示差） |
| 1077 首星 G01 | ms=77，rough=717，rate=743 | DF397=77，DF398=0.7001953125（=717/1024），DF399=743 | 一致 |
| 首格 1C | fine=72331，Ph=−511535，lock=649，cnr=752，rate=−378 | DF405=0.00013473（×2²⁹=72331），DF406=−0.00023820，DF407=649，DF408=47.0，DF404=−0.0378 | 一致 |
| 首格伪距 | 23293972.930 m（手算） | 由 DF397+DF398+DF405 算得 23293972.930 m | 一致 |

与 [rtcm-rs](./rtcm-rs.md) 同一挂载点：1005 ECEF 相同；**1107（NSat=0 空 MSM）本库正常解出**，rtcm-rs 0.11.0 解成 `Corrupt`。

### 3.5 编码往返

- **真实**：358 帧逐帧 `DeserializeMessage` → `EncapsulateMessage(m).Serialize()`，**358/358 与原帧逐字节相同**（含 CRC）。
- **合成** 1005（sta=2003，GPS/GLO/GAL=true，X/Y/Z=1114104.5999/−4850731.7456/3975942.1549 m，字段填 0.1 mm 整数）：

```text
synthetic 1005 frame 25B crc=4813921 (0x497461) hex=d300133ed7d30382980edeef34b4bd13300941d8a06d497461
decode err=<nil>/<nil> equal=true X=11141045999
X=1e12 m: frame 25B, decoded X=-5825462.2720 m          ← 超 38 bit 量程，静默回绕
pyrtcm parse（默认校 CRC）: 1005 2003 1 1 1 1114104.5999 -4850731.7456 3975942.1549
```

struct 是整数字段，`==` 往返为 true（rtcm-rs 用 f64 米要容差比）；超量程回绕到 −5825462.272 m 与 rtcm-rs 相同。

## 4. 错误用例（本机，VALDM 真帧改造；合成标注）

| 输入 | `DeserializeFrameBytes` | `Scanner.NextMessage` 循环 | panic? |
| --- | --- | --- | --- |
| 原文件 | — | 358 帧，`io.EOF` | 否 |
| 1 字节分块 `iotest.OneByteReader` / `HalfReader` | — | 358 / 358，与整文件同 | 否 |
| 首帧 CRC 末字节翻转 | `invalid CRC` | 357 帧：**坏帧静默跳过**，无任何回报 | 否 |
| 首帧载荷翻 1 bit | `invalid CRC` | 同上 | 否 |
| 最后完整帧截掉一半 | `data is smaller than frame length` | 357 帧，残帧结束时只给 `io.EOF` | 否 |
| 帧前 `HTTP/1.1 200 OK\r\n\r\n\x00\xff\xd3` 垃圾 | `invalid preamble`（不自动找） | 358 帧（逐字节重同步） | 否 |
| 假 `d3 03 ff`（宣称 1023 B）+ 整文件 | — | 358 帧 | 否 |
| 假 `d3 03 ff` + 末 3 帧（本机 613 B） | — | **0 帧，直接 `io.EOF`**：`Peek(1028)` 撞 EOF，后面 3 个好帧全丢 | 否 |
| 1 字节载荷 | `DeserializeMessage` → `invalid rtcm message: no message number` | — | 否 |
| 1005 载荷截到 8 B | 返回 `Message1005` + err `runtime error: index out of range [0] with length 0`（restruct 内部 recover） | — | 否 |
| 1077 载荷截到 20 B | **err=nil**，nsat=11（本文件首帧），各星 ms 全 0，CellMask=0，信号数组空 | — | 否 |
| 零卫星 1077（**合成**，22 B 头） | 成帧→扫描 1 帧；err=nil，nsat=0，重编码相同 | — | 否 |
| 12 星×6 信号=72 格 1077（**合成**，超规范 64） | err=nil，CellMask=0，信号空，重编码≠原文 | — | 否 |

对照 rtcm-rs：两者坏 CRC 都静默丢；本库遇假长度头**在流中间不受影响**（逐字节回退），只在流尾丢帧（rtcm-rs 同）；本库 MSM 截断**不报错、默默给 0**；rtcm-rs 解不出时至少返回 `Message::Corrupt`，本库更需自检。

## 5. 输入 / 输出

| API | 作用 |
| --- | --- |
| `NewScanner(io.Reader) Scanner` | 内部 `bufio.Reader`（4096 B），够装最大帧 1029 B |
| `Scanner.NextFrame() (Frame, error)` / `NextMessage() (Message, error)` | 读到合法帧为止；错误只剩 I/O 错（含 `io.EOF`） |
| `DeserializeFrame(*bufio.Reader)` / `DeserializeFrameBytes([]byte)` | 单帧；后者不找同步、要求首字节 0xD3 |
| `DeserializeMessage(payload) (Message, error)` | 按号分派；MSM 分支**永远 err=nil** |
| `EncapsulateMessage(Message)` / `EncapsulateByteArray` → `Frame.Serialize()` | 加 D3 头 + CRC24Q |
| `Crc24q([]byte) uint32`、`MessageNumber(payload)` | 工具函数 |
| `Observation` 接口：`Time()`、`SatelliteCount()` | 观测类（含 MSM、1001–1004、1009–1012） |

| 字段 | 单位 / 换算 |
| --- | --- |
| 1005/1006 `ReferencePointX/Y/Z`（int64） | 0.1 mm → ×10⁻⁴ 得 m；`AntennaHeight` 同 |
| MSM `RangeMilliseconds` / `Ranges` | 整 ms / 2⁻¹⁰ ms |
| MSM7 `Pseudoranges` / `PhaseRanges` | 2⁻²⁹ ms / 2⁻³¹ ms（MSM4 为 2⁻²⁴ / 2⁻²⁹） |
| MSM7 `Cnrs` / `PhaseRangeRates`（信号） | 2⁻⁴ dBHz / 10⁻⁴ m/s；星级 rate 为 1 m/s |
| MSM 星/信号 ID | 不给列表，由 `SatelliteMask`（64 bit，MSB=1 号）、`SignalMask`（32 bit）、`CellMask` 自解 |

## 6. 坑

| # | 现象 | 原因 | 对策 |
| ---: | --- | --- | --- |
| 1 | 坏帧、截断帧无声消失 | `Scanner` 把 `invalid preamble`/`invalid CRC` 吞掉逐字节重试，无跳过字节计数 | 自己包 `io.Reader` 计字节，与帧长和对比估丢包 |
| 2 | 截断/损坏的 MSM 解出一堆 0 | iobit 读越界不报错；MSM 分支硬编码 `nil` 错误（源码 TODO） | 用 `len(payload)` 与掩码推算长度自检；`len(SignalData.Pseudoranges)==popcount(CellMask)` |
| 3 | 回放旧文件时间错一周 | `Message10x7.Time()` / `DF004()` 用 `time.Now()` 推 GPS 周 | 回放用 `rtcm3.DF004Time(epoch, 录制时刻)` |
| 4 | 闰秒写死 18 s | `leap.go` 表截至 2016-12-31，`GpsLeapSeconds()` 不随时间 | 有新闰秒要升级库或自算 |
| 5 | 流尾假 0xD3 让最后几帧丢 | `Peek(len+5)` 撞 EOF 直接返回 | 文件模式可改用 `DeserializeFrameBytes` 逐偏移扫描（本文 §4 基线即此法） |
| 6 | 超量程值编码成功 | restruct 按位截断，无范围检查 | 编码前自检（DF025 为 38 bit 有符号，±13.7×10⁶ m） |
| 7 | 手搓 MSM 编码出错 | 改卫星列表不会重算掩码（README 自认） | 编码只做透传/过滤时同步改三个 mask |
| 8 | CellMask > 64 格被置 0 | 字段是 `uint64` | 规范本就限 ≤64；遇到按坏报文处理 |
| 9 | `MessageUnknown.Number()` 短载荷返回 0 | 要求 `len(Payload) >= 4`（源码） | 用 `rtcm3.MessageNumber(payload)` |
| 10 | 32 位平台掩码计数错 | 源码 `bits.OnesCount(uint(mask))`，`uint` 为 32 bit 时截断（源码推断，未测） | 部署 64 位 |
| 11 | `go get` 下载 ntrip/logrus/uuid | go.mod 依赖 go-gnss/ntrip（仅 `cmd/ntriplatency` 用） | 可忽略；`rtcm3` 包只 import `iobit`/`restruct`/根包 `leap.go`，不链进二进制 |
| 12 | 共享机器 `GOPATH` 被别的项目污染 | 本机环境继承了他人 `GOMODCACHE`，首次 `go get` 报 missing go.sum | 显式设 `GOPATH/GOMODCACHE/GOCACHE` 到自己目录 |
| 13 | 把帧尾三字节当十进制 CRC | `Frame.Crc` 是 uint32；本合成帧 `crc=4813921`=`0x497461`（hex 末 6 位） | 打印用 `%d`/`0x%X`，勿把 hex 字面当十进制 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Go 服务里解 RTCM3（监控、转发过滤、入库） | **本文 go-gnss/rtcm v0.0.9** |
| Go 里连 caster / 自建 caster | [ntrip-go](./ntrip-go.md)（同组织），配本库解帧 |
| Rust / no_std / 需要 MSM 解码报错 | [rtcm-rs](./rtcm-rs.md) |
| Python 快速看字段、DF 名对照、也能生成 | [pyrtcm](./pyrtcm.md)（本篇交叉核对基准）；取流 [pygnssutils](./pygnssutils.md) |
| RTCM3 → RINEX | [rtcm3torinex](./rtcm3torinex.md)、RTKLIB `convbin`（[rtklib](./rtklib.md)） |
| 录流 / 转发 | RTKLIB `str2str`（[rtklib](./rtklib.md)）、[bnc](./bnc.md)、[ntripclient](./ntripclient.md) |
| RTK / PPP 解算 | [rtklib](./rtklib.md) |
| SPARTN | [pyspartn](./pyspartn.md)（`go-gnss/spartn` 2020 年后未更，无手册） |

## 8. 未测 / 相关

未测：`cmd/ntriplatency` 连 GA caster（需账号）；SSR（1057–1066）、网络 RTK（1014–1017）、坐标变换（1021–1027）无真实流；32 位平台。

[rtcm-rs.md](./rtcm-rs.md) · [pyrtcm.md](./pyrtcm.md) · [ntrip-go.md](./ntrip-go.md) · [rtcm3torinex.md](./rtcm3torinex.md) · [rtklib.md](./rtklib.md) · [ntrip-client.md](./ntrip-client.md) · [ntripclient.md](./ntripclient.md) · [rtcm-ntrip-software.md](./rtcm-ntrip-software.md) · [README.md](./README.md)
