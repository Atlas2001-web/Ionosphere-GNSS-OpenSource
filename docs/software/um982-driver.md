# UM982Driver · 和芯星通 UM982/UM980 扩展语句 Python 驱动操作手册

目录：[`PROJECTS.json` → `um982-driver`](../../PROJECTS.json) · 上游 <https://github.com/sunshineharry/UM982Driver>（与 PROJECTS `url` 一致；**默认分支是 `master`，不是 main**）· tip **`451364c`**（2025-04-03 09:30 EDT，`Merge pull request #3 … Update readme.md`，之后无提交）· **无 tag** · PyPI **`um982-driver` 0.2.1**（2024-08-26 06:02 EDT，仅 wheel；包内 `UM982.py` 与 master **逐字节相同**；另有 0.1.4）· **GPL-3.0**（GitHub LICENSE；PyPI 元数据 license 为空）· ★**39** / fork 20 · 纯 Python · 本机 CPython 3.13.5 + venv：pyserial 3.5 / pyproj 3.8.0 / numpy 2.5.3，对照 pynmeagps 1.1.7 / pynmea2 1.19.0，socat 虚拟串口 · 实测窗口 **2026-09-26 05:56–06:05 EDT**

规范依据：**Unicore Reference Commands Manual For N4 High Precision Products V2 EN R1.15**（2026-06 版，371 页，en.unicore.com 公开 PDF，5581479 B）：§7.5.1 报文头/CRC、§7.5.81 PVTSLN（表 7-151）、§7.5.21 BESTNAV（表 7-70）、§7.4.9 GPHPR（表 7-38）、§7.5.49 KSXT（表 7-107）、附录 1 CRC32 C 代码。

> 一句话：一个约 180 行的 `UM982.py`：后台线程 `readline()` 读串口，只认 **`#PVTSLNA`、`#BESTNAVA`、`$GNHPR`** 三种 ASCII 句，把最新值放进 `.fix`/`.vel`/`.orientation`，再用 pyproj 算 `.utmpos`。
> **本机无 UM982/UM980 接收机**：串口/接收机路径全部 **「未在真接收机测试」**，只用 socat 虚拟串口回放公开真实日志。人造输入标 **「合成」**。

## 1. 用途边界

| 做 | 不做 |
| --- | --- |
| `#PVTSLNA` → `fix`（海拔高、纬度、经度、三个标准差），校验 CRC32 | **不解 KSXT**：英文 README 让你开 `KSXT`，源码没有任何 KSXT 分支 |
| `#BESTNAVA` → `vel`（东/北/天速度 + 标准差），由地速×航迹角分解 | 不解二进制（`PVTSLNB`/`BESTNAVB`）、不解 NMEA 标准句（GGA/RMC 等全丢） |
| `$GNHPR` → `orientation`（航向/俯仰/横滚，°），校验 XOR | 不给解状态（NARROW_INT/PSRDIFF）、卫星数、时间戳、差分龄期 |
| WGS84 → UTM（pyproj，区号按首个定位自动选，之后不变） | **不发任何配置命令**：`config com2 …`/`PVTSLNA com2 0.05` 须你自己用串口工具或 UPrecise 发 |
| 附 ROS2 示例节点（发布 `/gps/fix`、`/gps/utmpos`）与未测试的 C 版（zip） | 包本身不依赖 ROS；示例节点依赖 rclpy + tf_transformations（未测） |

## 2. 安装

```bash
unset TMPDIR VIRTUAL_ENV PYTHONPATH PIP_CACHE_DIR    # 共享机器：清掉别人的环境变量
mkdir -p /tmp/um982-man/tmp && cd /tmp/um982-man
export TMPDIR=/tmp/um982-man/tmp PIP_CACHE_DIR=/tmp/um982-man/pipcache
python3 -m venv venv && . venv/bin/activate
pip install um982-driver==0.2.1          # 只会装 numpy + pyproj
python -c "import um982"
# → ModuleNotFoundError: No module named 'serial'      ← 本机真实输出
pip install pyserial                      # 必须手动补；注意不是 PyPI 上的 "serial"
python -c "import um982; print(um982.UM982Serial)"
# → <class 'um982.UM982.UM982Serial'>
```

`setup.py` 的 `install_requires` 写的是 `numpy, pyproj`（numpy 实际没用到），漏了 pyserial；仓库 `requirements.txt` 倒是写了 `pyproj pyserial`。import 名是 `um982`，不是 `um982_driver`。

接收机侧（README 原文，**未在真接收机测试**）：`config com2 921600` / `PVTSLNA com2 0.05` / `KSXT com2 0.05` / `GPHPR com2 0.05` / `BESTNAVA com2 0.05`。`GPHPR` 命令输出的句首是 `$GNHPR`（手册 §7.4.9 示例），与源码匹配；**GPHPR 仅 UM982/UMD982 支持**，UM980 单天线没有姿态。

## 3. 例子与真实输出

**数据来源（均为公开真实接收机输出）：**

| 代号 | 来源 | 内容 |
| --- | --- | --- |
| A | [JHua07/Hardware-Projects](https://github.com/JHua07/Hardware-Projects) `RTK_Trans/all.log`（最后改动 `a65d8ac`，2025-07-29 06:00 EDT；仓库无许可证，仅本地测试、不转载） | Unicore UM98x，成都，GPS 周 2368 秒 291726–292347（2025-05-28 05:01:48–05:12:09 EDT），15.8 MB：PVTSLNA/BESTNAVA/KSXT/GNGGA 各 **622** 句，NARROW_INT，无 GNHPR（heading_type=NONE） |
| B | 同仓 `1.log`（`8046ec7`，738 行，数据 2025-08-05 04:54 EDT，PSRDIFF）+ `rover.log`（104 BESTNAVA） | 首行是半句（录制从中间开始） |
| C | 手册 R1.15 示例：PVTSLNA、BESTNAVA、`$GNHPR`、`$GNHPR2`、KSXT（跨页折行按原样拼接） | CRC 全部通过 |
| D | [satpulse](./satpulse.md) `gps/lib/uncmsg/nav_test.go` 的 UM980 BESTNAVA；[pynmeagps](./pynmeagps.md) `tests/unicore_nmea.log` 的 `$GNHPR2` | 各 1 句 |

真实 GNHPR 只有 C/D 的 3 句（其中 2 句是 `$GNHPR2`）——姿态路径的实测样本很薄。

### 3.1 离线：直接调用模块级解析函数（不开串口）

```python
from um982.UM982 import (nmea_expend_crc, nmea_crc, PVTSLN_solver,
                         BESTNAV_solver, GNHPR_solver)
for line in open("readme_cfg.log", encoding="ascii"):   # A 中只留 PVTSLNA/BESTNAVA/KSXT，1866 行
    line = line.strip()
    if line.startswith("#PVTSLNA") and nmea_expend_crc(line):
        print("fix", PVTSLN_solver(line))
    elif line.startswith("#BESTNAVA") and nmea_expend_crc(line):
        print("vel", tuple(round(v, 4) for v in BESTNAV_solver(line)))
```

```text
vel (0.0081, -0.0094, -0.015, 0.0278, 0.0278, 0.0488)
fix (526.4542, 30.76613181582, 103.98802962088, 0.0325, 0.0113, 0.0127)
vel (0.0101, -0.0097, -0.0188, 0.0235, 0.0235, 0.0413)
fix (526.4501, 30.76613182121, 103.98802965694, 0.0324, 0.0113, 0.0126)
...                                   # 共 1244 行（622 fix + 622 vel），0.14 s
```

对应原句（A 第 1 历元）：`#PVTSLNA,88,GPS,FINE,2368,291726000,0,0,18,34;NARROW_INT,526.4542,30.76613181582,103.98802962088,0.0325,0.0113,0.0127,1.000,PSRDIFF,…`。`fix` 顺序是 **（高, 纬, 经, 高σ, 纬σ, 经σ）**——高度在前。

### 3.2 socat 虚拟串口回放（06:00:49 EDT）

```bash
socat pty,raw,echo=0,link=/tmp/um982-man/ttyA pty,raw,echo=0,link=/tmp/um982-man/ttyB &
# 写端按 92160 B/s（≈921600 波特 8N1）把 readme_cfg.log（CRLF，491687 B）写进 ttyA
python replay.py readme_cfg.log 92160 12       # 读端：UM982Serial("/tmp/um982-man/ttyB", 921600)
```

```text
init ok 0.031 s fix=(526.4611, 30.76613183643, 103.98802962111, 0.0324, 0.0113, 0.0126) vel=(0.003079115235178296, -0.0011870338531368451, 0.0085, 0.0216, 0.0216, 0.038) ori=None utm=(403153.7887781414, 3404121.4600051586)
thread alive True samples 596 distinct fix 265 distinct vel 265 last fix (526.4813, 30.76613147383, 103.98803010626, 0.0308, 0.01, 0.012) utm (403153.8348465053, 3404121.41939887) vel (0.004802132279786306, -0.0028808897180271206, 0.013, 0.0142, 0.0142, 0.0223) ori None
real 0m12.280s   user 0m0.801s
```

采样到的 265 个 `fix` 全部能在文件 622 个 PVTSLN 里找到，最后一个等于文件末句；驱动跟得上 921600 波特（离线 `read_frame` 19.7 µs/行，解析函数 4.9 µs/句）。`ori=None`：数据里没有 GNHPR——README 示例循环里的 `heading, pitch, roll = um982_driver.orientation` 此时直接 `TypeError`。

同一套回放换成 B 的 `1.log` 原样（首行半句，第一句 PVTSLNA 在第 75 行）：

```text
  File ".../um982/UM982.py", line 148, in __init__
    bestpos_hgt, bestpos_lat, bestpos_lon, bestpos_hgtstd, bestpos_latstd, bestpos_lonstd = self.fix
TypeError: cannot unpack non-iterable NoneType object          # 构造 0.009 s 即崩
```

### 3.3 加一层看门狗再用（自写包装，已实跑）

```python
import threading, time, serial
from um982 import UM982Serial
from um982.UM982 import create_utm_trans, utm_trans

class SafeUM982(UM982Serial):
    """不在构造里硬读 10 行；坏句只计数不杀线程；记录最后更新时间"""
    def __init__(self, port, baud, timeout=1.0):
        threading.Thread.__init__(self, daemon=True)
        self.ser = serial.Serial(port, baud, timeout=timeout)
        self.isRUN = True; self.fix = self.vel = self.orientation = self.utmpos = None
        self.transformer = None; self.t_fix = None; self.errors = 0
    def run(self):
        while self.isRUN:
            try:
                old = self.fix
                self.read_frame()
            except (ValueError, IndexError, UnicodeDecodeError):
                self.errors += 1; continue
            except (serial.SerialException, OSError, TypeError):
                break                                   # 掉线或 stop() 关口
            if self.fix is not None and self.fix is not old:
                self.t_fix = time.monotonic()
                if self.transformer is None:
                    self.transformer = create_utm_trans(self.fix[1], self.fix[2])
                self.utmpos = utm_trans(self.transformer, self.fix[2], self.fix[1])
```

回放 A 前 600 行、每 50 行插一帧合成 RTCM 样式二进制（共 12 帧），3 s 后再 kill socat：

```text
alive True errors 12 fix (526.469, 30.76613172331, 103.98802979909, 0.0296, 0.0103, 0.012) age 1.28 s utm (403153.80569850956, 3404121.447314224)
断开后 alive False age 2.8 s
```

原版遇到第 1 帧 RTCM 线程就死；包装版计 12 次错继续跑，`t_fix` 让上层能判断数据陈旧。UTM 1–9 区的错（§7 坑 4）包装没修。

## 4. 交叉检查（独立实现，06:00 EDT）

自写解析器 `indep.py`，不 import um982：按手册表 7-49/7-151/7-70/7-38 逐字段命名；CRC32 用两种独立写法（逐位 0xEDB88320 移位、`~zlib.crc32(data, 0xFFFFFFFF)`，即初值 0、无末异或），两者对每句都相等；NMEA 用 XOR；UTM 用 Karney 6 阶 Krüger 级数自写。

| 项目 | 样本 | 结果 |
| --- | --- | --- |
| 校验判定（驱动 `nmea_expend_crc`/`nmea_crc` vs 自写） | A+B+C+D 共 15800 句 Unicore ASCII + 33587 句 NMEA | **49387/49387 一致**，全部为真 |
| PVTSLN 6 字段 | 634 句 | max\|Δ\| = **0** |
| BESTNAV 6 输出（含 vE=地速·sin 航迹、vN=地速·cos 航迹） | 745 句 | max\|Δ\| = **0** |
| GNHPR 航向/俯仰/横滚；pynmeagps 同句 | 3 句 | 0；pynmeagps 值相同（pynmea2 1.19.0 报 `Unknown sentence type GNHPR`） |
| 驱动 UTM（pyproj EPSG:32648）vs 自写 Krüger | 634 点 | \|ΔE\| ≤ 2.5×10⁻⁹ m，\|ΔN\| ≤ 2.3×10⁻⁹ m |
| PVTSLN 纬经高 vs 同历元 GGA（pynmea2 / pynmeagps，UTC=GPS 秒−18 s 对齐） | A 622 历元，GGA 质量 4 | 纬经差 ≤ 3.3×10⁻¹¹°（GGA 分精度），高差 0：**PVTSLN 高度=海拔高（MSL）** |
| PVTSLN 速度段 vs 同历元 BESTNAV | 633 历元 | north/east 差 ≤ 0.0001 m/s；**第 3 个量 ≠ 地速**（最大差 0.2798 m/s，可为负），而是精确等于 **−vert_spd**（633/633） |

与手册不符（接收机/手册问题，非驱动）：表 7-151 把 PVTSLN 第 21 字段写成 `psrvel_ground`「水平地速」，真实输出是**向下为正的垂直速度**。驱动不读这一段，不受影响；自己扩展时别照手册用。

## 5. 错误用例（全部「合成」，由 A 的真句改写；需要合法 CRC 的用自写 CRC 重签）

| 输入 | 驱动行为 |
| --- | --- |
| 坏 CRC（末位改）/ 截断无 `*` / CRC 只剩 4 位 / 空行 | **静默丢弃**，`fix` 保持旧值（无计数、无日志） |
| CRC 大写 | 正常接受（驱动 `lower()` 比较） |
| 字段空（hgt=`""`）/ 非数字（`3O.7661`），CRC 合法 | `ValueError` → **后台线程死亡**，主线程继续读旧值 |
| 字段 `NaN`，CRC 合法 | 静默写入 `fix=(526.4542, nan, …)` |
| 字段截短到 5 个，CRC 合法 | `IndexError` → 线程死亡 |
| 未知语句（`#AGRICA`、`$GNGGA`） | 静默忽略 |
| `$GNHPR2`（HEADING2 模式，D 的真句） | **被当成 GNHPR**：`orientation=(88.364, -0.0873, 0.0)`（`startswith("$GNHPR")`） |
| `$GPHPR` 句首（合法校验） | 静默忽略 |
| 混入 RTCM3 二进制（`D3 00 13 …`，单独一行或粘在句首） | `readline().decode('utf-8')` 抛 `UnicodeDecodeError` → 线程死亡 |
| 构造时前 10 行没有 PVTSLNA | `TypeError: cannot unpack non-iterable NoneType`（已打开的串口不关） |
| 空输入（pty 对端打开但不写） | 构造函数**永久阻塞**（5 s 后仍卡在 `readline`，串口无 timeout） |
| 串口断开（回放中 kill socat） | 线程 `SerialException: device reports readiness to read but returned no data`，2 s 后 `is_alive()=False`，`fix` 冻结在旧值 |
| `stop()` | 关串口时线程仍在 `readline` → `TypeError: 'NoneType' object cannot be interpreted as an integer`（线程内 traceback） |

## 6. I/O：字段与单位

| 属性 | 元组顺序 | 来源字段（手册） | 单位 |
| --- | --- | --- | --- |
| `fix` | hgt, lat, lon, hgtσ, latσ, lonσ | PVTSLN 字段 3–8：`bestpos_hgt`（海拔高）/`bestpos_lat`/`bestpos_lon`/`bestpos_hgtstd`/`bestpos_latstd`/`bestpos_lonstd` | m（MSL）, °, °, m, m, m（手册表 7-151 未写 σ 单位；对照 BESTNAV 表 7-70 为 m） |
| `vel` | vE, vN, vU, **horσ, horσ**, verσ | BESTNAV 字段 27 `hor spd`、28 `trk gnd`（相对真北）、29 `vert spd`（向上为正）、31 `Horspd std`、30 `Verspd std` | m/s（航迹角 °） |
| `orientation` | heading, pitch, roll | `$GNHPR` 第 3–5 字段；航向 = 主天线→从天线基线方向，0–360° | ° |
| `utmpos` | E, N | pyproj，`epsg:326{区号}` / `epsg:327{区号}` | m |
| 输入 | ASCII 行，`\n` 或 `\r\n` 结尾；Unicore 头 10 字段 + `;` + 数据 + `*` + 8 位小写十六进制 CRC32（不含 `#`） | 表 7-49 / §7.5.1 | — |

索引写死在源码里（`parts[3+7]` 等）：按 `,` 切整句，`;` 两侧粘成一个元素。R1.15 头部恰为 10 字段，所以对得上；报文头若改版（字段数变）会静默错位。

## 7. 坑

1. **pip 装完 import 就崩**：缺 pyserial（见 §2）。
2. **构造函数只读 10 行**：前 10 行没有 PVTSLNA（开机、配置了其他高频句、从半句开始）即 `TypeError`；没有数据则永久阻塞。先确认接收机已在输出再实例化，或自己加 timeout 重试。
3. **UM980 / 单天线用不了 README 示例**：没有 `$GNHPR`，`orientation` 永远是 `None`，示例解包崩。
4. **UTM 区号 1–9 全错**：源码拼 `f"epsg:326{zone}"`，4 区得 `epsg:3264`。实测檀香山 (21.3069°, −157.8583°) → `WGS 84 / SCAR IMW ST17-20`，E/N=(−17621339.8, 1855278.7)，正确 UTM 为 (618417.1, 2356542.5)；安克雷奇 → `epsg:3266`，塔希提（南半球 6 区）→ `epsg:3276`。经度 −180°～−126°（阿拉斯加、夏威夷、南太平洋）静默给出垃圾坐标。10–60 区正确（悉尼 56S、成都 48N 与自写一致）。
5. UTM 区只在构造时按首个定位定一次，跨区行驶不切换；不处理挪威/斯瓦尔巴特殊区。
6. **`vel` 第 4、5 个都是水平速度 σ**（源码返回 `vel_hor_std, vel_hor_std`），不是东/北 σ；ROS2 示例把它当东/北 σ 用。
7. **`$GNHPR2` 覆盖 `$GNHPR`**：开了 HEADING2 的多基线设备，姿态会被第二基线悄悄替换。
8. **任何异常都杀后台线程且不告诉你**：坏数字、RTCM 二进制、串口掉线后 `fix` 冻结，主程序继续用旧值；属性里没有时间戳。至少轮询 `is_alive()`，或把 `read_frame` 包上 try。
9. 同一串口别混 RTCM 输出（改正数回传口常见），`decode('utf-8')` 碰到非法 UTF-8 字节（RTCM 帧头 0xD3 后接 0x00 即是）就崩。
10. `fix` 与 `vel` 来自不同语句、可能差一个历元；只取最新值，高频下会丢句（回放 622 历元只采到 265 个不同值，这是采样频率所限，不是解析丢句）。
11. ROS2 示例（**未测**，无 ROS 环境）：参数默认波特率写成 `961200`（应为 921600）；`NavSatFix.position_covariance[0]` 放的是纬度 σ²（ENU 顺序应为东向）；航向（北起顺时针）直接当 ROS yaw（东起逆时针）用；`package.xml` 许可证写 `TODO`。
12. **GPL-3.0 对分发的影响（简述，非法律意见）**：只在自己机器上用、不分发，无额外义务；把 import 了本包的程序（含 ROS 节点、机器人系统镜像）**对外分发**，一般要以 GPL-3.0 兼容条款提供整个衍生作品的源码；单纯走网络提供服务不触发（不是 AGPL）。PyPI 元数据未写许可证，以仓库 LICENSE 为准。

## 8. 未测

- 真 UM982/UM980 串口、实际 20 Hz（0.05 s）输出、README 配置命令是否被固件接受：**未在真接收机测试**。
- 双天线真实 `$GNHPR` 连续流（只有 3 句样本）；RTK 固定下姿态精度。
- ROS2 示例节点（`colcon build`/发布话题）、`appendix/UM982DriverC.zip` 的 C 版本。
- 高于 921600 波特、USB 串口掉线重连、Windows 串口名。

## 9. 选型

| 需求 | 用 |
| --- | --- |
| UM982 双天线 → Python 里拿位置/速度/姿态三元组，自己能兜异常 | **本驱动**（或只借它的 CRC/解析函数，自己管串口） |
| 通用 NMEA；Unicore 专有句 | [pynmeagps](./pynmeagps.md)（`$GNHPR`/`$GNHPR2` 有字段名，`$KSXT` 只给 `field_01…`） · [pynmea2](./pynmea2.md)（GNHPR 报未知、KSXT 报 ParseError） · Rust：[nmea-parser](./nmea-parser.md) / [nmea-rs](./nmea-rs.md) · C：[minmea](./minmea.md) / [libnmea](./libnmea.md) |
| NovAtel OEM `#…A`/二进制日志（外形相似，但 Unicore N4 头字段不同，未测能否互解） | [novatel-edie](./novatel-edie.md) |
| Go 里读 Unicore BESTNAV/PPPNAV 并做授时 | [satpulse](./satpulse.md)（`uncmsg` 包） |
| 守护进程多客户端共享 GNSS | [gpsd](./gpsd.md) |
| u-blox 接收机 | [pyubx2](./pyubx2.md) · ROS：[ublox-dgnss](./ublox-dgnss.md) / [ublox-driver](./ublox-driver.md) |
| 其他厂 ROS 驱动 | [septentrio-gnss-driver](./septentrio-gnss-driver.md) · [swiftnav-ros2](./swiftnav-ros2.md) |
| 原始观测后处理 RTK/PPK | [rtklib](./rtklib.md) |

30 秒结论：UM982 + 双天线、经度不在 −180°～−126° 的项目，想十分钟拿到 `fix/vel/orientation`，用它；上线前补 pyserial、把 `read_frame` 包 try、加 `is_alive()` 看门狗、别在 1–9 区用 `utmpos`。UM980 单天线或需要解状态/时间戳，直接用 pynmeagps 读 NMEA + 自己按手册拆 `#PVTSLNA`（本篇 §4 的独立解析器几十行）。
