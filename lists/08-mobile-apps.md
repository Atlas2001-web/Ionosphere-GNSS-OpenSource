# 移动与嵌入式应用 / Mobile Apps
> **29** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

## Android

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTest](https://github.com/barbeau/gpstest) | GPSTest：Android GNSS 测试与原始测量记录 | Kotlin | 2402 | 🏷️ 个人社区 ★ 核心 |
| [GPSLogger](https://github.com/BasicAirData/GPSLogger) | GPSLogger：安卓开源轨迹与传感器记录器 | Java | 504 | 🏷️ 个人社区 |
| [bluetooth_gnss](https://github.com/ykasidit/bluetooth_gnss) | bluetooth_gnss：蓝牙外接 GNSS/RTK Android 应用 | Java | 123 | 🏷️ 个人社区 |
| [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare) | 手机原始测量定位框架（GPS/Galileo 等） | Java | 73 | 🏷️ 个人社区 |
| [positional](https://github.com/mtrewartha/positional) | positional：Android 位置与卫星信息简易 App | Kotlin | 61 | 🏷️ 个人社区 |
| [GalileoHack](https://github.com/griush/GalileoHack) | GalileoHack：多星座 GNSS 可见性 Android 演示 App | Kotlin | 34 | 🏷️ 个人社区 |
| [PRIDE-GeoDataLogger](https://github.com/PrideLab/PRIDE-GeoDataLogger) | PRIDE-GeoDataLogger：手机多频 GNSS+IMU 采集工具 | — | 22 | 🏷️ 高校实验室 |

### 详细说明

#### [GPSTest](https://github.com/barbeau/gpstest)  
*🏷️ 个人社区 ★ 核心*

语言：Kotlin · 许可：Apache-2.0 · 星标约：2402 · 宿主：github

多星座双频、SBAS、精度评估与 NMEA/原始测量日志，常与 Google 分析套件联用，是手机 GNSS 测试常用入口。适合设备能力摸底与采集。不是测地接收机替代品；原始测量可用性随芯片/ROM 而异。

#### [GPSLogger](https://github.com/BasicAirData/GPSLogger)  
*🏷️ 个人社区*

语言：Java · 许可：GPL-3.0 · 星标约：504 · 宿主：github

记录 GPS 轨迹与辅助传感器信息，户外测绘、运动轨迹常用。不做载波相位精密定位；原始测量科研请看 GnssLogger/GPSTest。

#### [bluetooth_gnss](https://github.com/ykasidit/bluetooth_gnss)  
*🏷️ 个人社区*

语言：Java · 许可：GPL-2.0 · 星标约：123 · 宿主：github

通过蓝牙连接外置接收机，在 Android 上使用 NTRIP 做 RTK/差分，已上架应用商店，野外测绘与兴趣玩家常用。适合手机加蓝牙板卡的移动作业。不是原始测量科研 Logger（见 GPSTest、gps-measurement-tools），精密测地仍取决于外置设备、天线与差分服务稳定性。蓝牙链路时延与丢包会表现为固定解不稳定。

#### [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare)  
*🏷️ 个人社区*

语言：Java · 许可：Apache-2.0 · 星标约：73 · 宿主：github

在 Android 上从原始测量解算位置，支持 GPS/Galileo 等，便于算法上机对比。适合教学与原型 App。维护节奏一般；长期采数与设备兼容性测试仍常搭配 GPSTest 等工具。

#### [positional](https://github.com/mtrewartha/positional)  
*🏷️ 个人社区*

语言：Kotlin · 许可：GPL-3.0 · 星标约：61 · 宿主：github

轻量 Android 应用，展示当前位置、坐标与相关卫星/定位信息，适合教学演示与野外快速查看。GPL-3.0；与 GPSTest、GNSS_Compare 相比功能更简洁。非原始测量记录器，科研级 RINEX/原始观测量请另用 GnssLogger 类工具。

#### [GalileoHack](https://github.com/griush/GalileoHack)  
*🏷️ 个人社区*

语言：Kotlin · 许可：MIT · 星标约：34 · 宿主：github

HackUPC 2024 ESA 挑战获奖的开源 Android GNSS Tracker，展示手机所见各星座卫星并对比 GNSS 与网络定位。MIT，有 Play 商店包。偏教学演示与可视化，非精密定位或原始测量导出工具；芯片与 Android 版本影响可见卫星。

#### [PRIDE-GeoDataLogger](https://github.com/PrideLab/PRIDE-GeoDataLogger)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：22 · 宿主：github

PRIDE 团队面向智能手机的多频 GNSS 与 IMU 采集工具，便于把手机原始测量送入后续 PPP 或科学研究流程。适合手机大地测量、城市峡谷与行人导航试验。手机天线相位中心与占空比限制明显；采集前应规划时间同步、姿态记录与导出格式，以便对接 PRIDE-PPPAR 或自研脚本。

## 嵌入式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [micropyGPS](https://github.com/inmcm/micropyGPS) | micropyGPS：MicroPython 板载 NMEA 0183 解析 | Python | 391 | 🏷️ 个人社区 |
| [ubxlib](https://github.com/u-blox/ubxlib) | u-blox 官方嵌入式 C 库（GNSS/蜂窝 API） | C | 358 | 🏷️ 官方 |
| [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer) | GNSSTimeServer：ESP 系 GNSS 授时服务器 | C | 232 | 🏷️ 个人社区 |
| [esp32-xbee](https://github.com/nebkat/esp32-xbee) | ESP32 NTRIP/UART 桥接固件（Ardusimple） | C | 119 | 🏷️ 个人社区 |
| [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS) | STM32-GNSS：STM32 上的 UBX 库 | C | 89 | 🏷️ 个人社区 |
| [satpulse](https://github.com/jclark/satpulse) | satpulse：跨平台 GNSS 授时与接收机 GUI | Go | 63 | 🏷️ 个人社区 |
| [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker) | STM32Primer2-GNSS-Tracker：Primer2 平台 GNSS 轨迹记录 | C | 31 | 🏷️ 个人社区 |
| [esp32-gps](https://github.com/mrichar1/esp32-gps) | ESP32 上整合 GPS、蓝牙与 NTRIP/RTK 转发 | Python | 23 | 🏷️ 个人社区 |
| [Cryologger-GVT](https://github.com/cryologger/glacier-velocity-tracker) | Cryologger GVT：面向 PPP 的开源冰川 GNSS 测速仪 | C++ | 19 | 🏷️ 个人社区 |
| [GNSSClock](https://github.com/stevemarple/GNSS_Clock) | GNSSClock：Arduino 上读 NMEA/PPS 的 GNSS 时钟 | C++ | 2 | 🏷️ 个人社区 |

### 详细说明

#### [micropyGPS](https://github.com/inmcm/micropyGPS)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：391 · 宿主：github

inmcm 的 MicroPython NMEA 解析库，面向 PyBoard 等嵌入式板，支持常见 GNSS 语句与状态提取。MIT 许可，适合教学与低成本物联网定位原型。非桌面级全功能解析器；内存与句子覆盖以仓库说明为准，复杂差分或原始观测量请另选链路处理。

#### [ubxlib](https://github.com/u-blox/ubxlib)  
*🏷️ 官方*

语言：C · 许可：Apache-2.0 · 星标约：358 · 宿主：github

u-blox 官方开源的可移植 C 库，面向 MCU/RTOS 场景提供 GNSS 与蜂窝等产品统一 API，作为各平台 SDK 的附加层。Apache-2.0。适合嵌入式原始测量/配置联调；不是精密定位引擎，PC 端解析更常见 pyubx2 等工具。

#### [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer)  
*🏷️ 个人社区*

语言：C · 许可：MIT · 星标约：232 · 宿主：github

以太网/WiFi GNSS 授时服务器：以 GPS/北斗/GLONASS/Galileo 为时间源，对外提供 NTP、RDATE、PTP，硬件基于 ESP8266/ESP32 与 Arduino 生态。适合实验室、业余台站本地时间同步。精度受模块、天线与网络抖动限制，达不到电信机房原子钟等级；天线与固件选项对照上游说明。

#### [esp32-xbee](https://github.com/nebkat/esp32-xbee)  
*🏷️ 个人社区*

语言：C · 许可：GPL-3.0 · 星标约：119 · 宿主：github

Ardusimple WiFi NTRIP Master 的官方 ESP-IDF 固件（GPL-3.0），把 ESP32 UART 桥接到 WiFi，提供 NTRIP Client/Server/Caster 与 TCP/UDP、Web 配置界面。适合低成本基站/流动站差分链路。硬件引脚默认面向其板卡；通用 ESP32 需改 GPIO。不是精密定位解算器。

#### [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：89 · 宿主：github

面向 STM32 的 u-blox GNSS 库，支持 UBX 协议与 DMA，作者称在 NEO-M8、MAX-M8、NEO-M9N 等模块上验证。适合嵌入式读取 NMEA/UBX、配置接收机。库本身不做高精度解算；若要 RTK，需模块固件支持并另接 NTRIP/电台改正数。不同 u-blox 固件协议细节仍有差异，注意版本。

#### [satpulse](https://github.com/jclark/satpulse)  
*🏷️ 个人社区*

语言：Go · 许可：MIT · 星标约：63 · 宿主：github

Go 实现的跨平台 GNSS 工具，强调 PPS/PTP/NTP 授时、RINEX/RTCM 与接收机评估配置，可在树莓派等设备上做时间同步与简易定位。适合时间服务器与精密授时爱好者。不是测地 PPP 引擎；差分与 RTK 能力取决于所接接收机与 NTRIP，可与 bluetooth_gnss、GNSSTimeServer 对照场景。

#### [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：31 · 宿主：github

运行于 STM32 Primer2 的 GNSS 轨迹记录固件/应用，把卫星定位点记下来便于回放与展示。适合嵌入式便携记录与爱好者硬件实验。硬件绑定 Primer2，功能以记录为主，不是跨平台定位 SDK，也不含 RTK 引擎。存储介质与采样间隔决定可记录轨迹时长。电池与存储容量共同限制连续记录时长。

#### [esp32-gps](https://github.com/mrichar1/esp32-gps)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：23 · 宿主：github

在 ESP32 上把 GNSS 模块、串口/蓝牙与 NTRIP 客户端/Caster/转发串起来，方便做物联网终端或农机差分原型。适合嵌入式联调与野外低成本试验。吞吐、天线与长期稳定性弱于工业板卡；公网播发需自行处理账号与安全。

#### [Cryologger-GVT](https://github.com/cryologger/glacier-velocity-tracker)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：19 · 宿主：github

Cryologger Glacier Velocity Tracker 以 Arduino/MicroMod 与 SparkFun ZED-F9P 采集多频 GNSS，面向极地冰川日尺度流速与事后 PPP。提供组装文档与固件，GPL-3.0。是硬件+固件方案，定位解算多依赖外部 PPP 服务；恶劣环境部署需自行供电与防护。

#### [GNSSClock](https://github.com/stevemarple/GNSS_Clock)  
*🏷️ 个人社区*

语言：C++ · 许可：LGPL-2.1 · 星标约：2 · 宿主：github

在 Arduino 上用 GNSS（GPS/GLONASS/Galileo）NMEA 语句与 PPS 秒脉冲实现时钟与守时，方便嵌入式授时和业余无线电时间基准。适合单片机爱好者与简易时频同步。功能止于时钟/授时，不含 RTK 或精密 PVT；可用星座取决于所接 GNSS 模块固件。PPS 布线与晶振稳定度影响短期守时表现。

## 嵌入式/Arduino

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SparkFun_u-blox_GNSS_v3](https://github.com/SparkFun/SparkFun_u-blox_GNSS_v3) | SparkFun u-blox GNSS v3：Arduino 配置库 | C++ | 104 | 🏷️ 个人社区 |

### 详细说明

#### [SparkFun_u-blox_GNSS_v3](https://github.com/SparkFun/SparkFun_u-blox_GNSS_v3)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT-style (SparkFun code) · 星标约：104 · 宿主：github

面向嵌入式/创客的 Arduino 库，用 u-blox Configuration Interface 配置与读取模块，便于采集原始测量或 NMEA。适合低成本接收机原型与教学；不是精密定位引擎，高级 RTK/PPP 仍需配合基站与解算软件。

## 原始测量

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gsdc2023](https://github.com/taroz/gsdc2023) | gsdc2023：手机十米级挑战 2023 解算代码 | Python | 114 | 🏷️ 个人社区 |
| [GNSS_MobileCalculator](https://github.com/RogerioDoCarmo/GNSS_MobileCalculator) | Android 原始伪距 SPS 示例 | Java | 15 | 🏷️ 个人社区 |
| [androidGnss](https://github.com/AILocAR/androidGnss) | Android 原始 GNSS 伪距定位 MATLAB 代码 | MATLAB | 14 | 🏷️ 高校实验室 |
| [google-gnss-logger](https://github.com/gscatto/google-gnss-logger) | google-gnss-logger：GNSS Logger 原始测量 Java 解析库 | Java | 8 | 🏷️ 个人社区 |

### 详细说明

#### [gsdc2023](https://github.com/taroz/gsdc2023)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：114 · 宿主：github

taroz 针对 Google Smartphone Decimeter Challenge 2023 的公开代码与思路，处理手机原始 GNSS 测量与轨迹评估。MIT 许可；衔接 Android 原始观测与低成本定位研究。竞赛规则与数据版本绑定，复现需自备挑战数据集与官方评价指标脚本。

#### [GNSS_MobileCalculator](https://github.com/RogerioDoCarmo/GNSS_MobileCalculator)  
*🏷️ 个人社区*

语言：Java · 许可：NOASSERTION · 星标约：15 · 宿主：github

在 Android 上读取 GNSS 原始伪距并实现标准单点定位（SPS）流程的开源示例（Java）。适合教学演示「手机原始测量→位置」链路。精度与完整性受手机芯片、占空比与 API 限制，不能替代测绘级 RTK；与 GPSTest、Google GNSS Logger 等工具互补。

#### [androidGnss](https://github.com/AILocAR/androidGnss)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：14 · 宿主：github

面向 Android 原始 GNSS 测量的 MATLAB 伪距定位示例与实验代码，方便在桌面端复现手机观测处理。适合课堂与算法对比。输入依赖手机端记录的原始测量文件；实时嵌入式部署需另接 Java/Kotlin 或 NDK 方案。

#### [google-gnss-logger](https://github.com/gscatto/google-gnss-logger)  
*🏷️ 个人社区*

语言：Java · 许可：MIT · 星标约：8 · 宿主：github

MIT 许可的 Java 库，高效解析 Android GNSS Logger 导出的原始测量与传感器事件文本格式，可配置只读所需字段。适合手机原始观测后处理管线。仓库偏库而非 App；上游 Logger 格式若变更需跟进。与已收录 GPSTest 等采集工具互补。

## QZSS嵌入式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [QZQSM](https://github.com/baggio63446333/QZQSM) | QZQSM：Arduino 上解析 QZSS DC Report 的嵌入式库 | C++ | 21 | 🏷️ 个人社区 |

### 详细说明

#### [QZQSM](https://github.com/baggio63446333/QZQSM)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：21 · 宿主：github

面向嵌入式的 QZSS DC Report 报文 Arduino 库，BSD-3-Clause。可在带 GNSS 模块的 MCU 上解析灾情类广播，与桌面端 azarashi 形成软硬互补。依赖具体接收机是否输出原始 DCR/相关 NMEA；天线与区域覆盖会影响可用性。适合创客与应急原型，非航空认证实现。

## 树莓派GNSS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsshat](https://github.com/jimmypaputto/gnsshat) | gnsshat：树莓派 GNSS HAT 的 UBX 驱动与 Flask 面板 | C++ | 22 | 🏷️ 个人社区 |

### 详细说明

#### [gnsshat](https://github.com/jimmypaputto/gnsshat)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：22 · 宿主：github

面向 Jimmy Paputto GNSS HAT 的驱动库，覆盖 u-blox UBX，并提供 C++/C/Python API 与 Flask 实时仪表盘（天空图、RF、RTK 相对图等），MIT 许可。虽绑定厂商板卡，但对通用 UBX 串口/SPI 仍有参考价值。RTK 固定与厘米级显示依赖改正流与天线环境。适合树莓派现场演示与低成本监测。

## Arduino解析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NeoGPS](https://github.com/SlashDevin/NeoGPS) | NeoGPS：Arduino 低内存 NMEA/u-blox GPS 解析库 | C++ | 750 | 🏷️ 个人社区 |

### 详细说明

#### [NeoGPS](https://github.com/SlashDevin/NeoGPS)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：750 · 宿主：github

面向 Arduino 的可配置 NMEA 与 u-blox 报文解析库，强调极低 RAM（可低至约 10 字节量级配置），GPL-3.0。适合资源受限嵌入式定位日志与简易导航，而非测地级解算。需按目标板裁剪消息集；与 TinyGPS 类库相比更偏可配置与 UBX。星数高、许可证明确，补齐移动/嵌入式解析薄点。

## UBX通信

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UbxGps](https://github.com/loginov-rocks/UbxGps) | UbxGps：Arduino 轻量 u-blox UBX 通信库（MIT） | C++ | 152 | 🏷️ 个人社区 |

### 详细说明

#### [UbxGps](https://github.com/loginov-rocks/UbxGps)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：152 · 宿主：github

以简单、快速为目标的 Arduino u-blox UBX 通信库，MIT 许可。适合读取原始 UBX 导航/观测类消息做嵌入式实验。协议字段随模块固件变化，接入前需核对消息类与波特率。不覆盖 NTRIP/RTK 全栈，可与更高层解算或日志工具组合使用。

## uBlox驱动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [bolderflight-ublox](https://github.com/bolderflight/ublox) | bolderflight-ublox：Bolder Flight uBlox Arduino/CMake 驱动 | C++ | 115 | 🏷️ 个人社区 |

### 详细说明

#### [bolderflight-ublox](https://github.com/bolderflight/ublox)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：115 · 宿主：github

Bolder Flight 维护的 uBlox GNSS 通信库，同时支持 Arduino 与 CMake 构建，MIT 许可。面向无人机/航空电子常用接收机接口，偏驱动与报文读写。命名加前缀以免与泛名 ublox 冲突。固件与消息集需匹配具体型号；非 PPP/RTK 引擎。

## Arduino-NMEA

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [MicroNMEA](https://github.com/stevemarple/MicroNMEA) | MicroNMEA：紧凑 Arduino NMEA 解析库（LGPL-2.1） | C++ | 111 | 🏷️ 个人社区 |
| [107-Arduino-NMEA-Parser](https://github.com/107-systems/107-Arduino-NMEA-Parser) | 107-Arduino-NMEA-Parser：多星座 Arduino NMEA 库（MIT） | C++ | 24 | 🏷️ 个人社区 |

### 详细说明

#### [MicroNMEA](https://github.com/stevemarple/MicroNMEA)  
*🏷️ 个人社区*

语言：C++ · 许可：LGPL-2.1 · 星标约：111 · 宿主：github

面向资源受限 MCU 的紧凑 NMEA 解析库，LGPL-2.1，强调小体积与可移植。适合嵌入式日志与简易定位，功能少于 NeoGPS 的 UBX 深度支持。需自行处理串口与语句过滤。补齐 SPDX 明确的 Arduino NMEA 选项。

#### [107-Arduino-NMEA-Parser](https://github.com/107-systems/107-Arduino-NMEA-Parser)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：24 · 宿主：github

可对接 GPS/GLONASS/Galileo/GNSS 模块并解释 NMEA 的 Arduino 库，MIT 许可。API 面向现代 Arduino 核心，适合创客与原型。不覆盖差分改正与精密解算。与 MicroNMEA/NeoGPS 并列时按许可证与 API 偏好选择。
