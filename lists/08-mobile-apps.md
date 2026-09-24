# 移动与嵌入式应用 / Mobile Apps
> **16** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

手机/嵌入式 GNSS 测试、原始测量记录与简易定位。

## Android

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTest](https://github.com/barbeau/gpstest) | 开源 Android GNSS 测试与原始测量记录 | Kotlin | 2402 | 🏷️ 个人社区 ★ 核心 |
| [GPSLogger](https://github.com/BasicAirData/GPSLogger) | Android 开源 GPS 轨迹记录器 | Java | 504 | 🏷️ 个人社区 |
| [bluetooth_gnss](https://github.com/ykasidit/bluetooth_gnss) | Android 蓝牙外接 GNSS/RTK 与 NTRIP 应用 | Java | 123 | 🏷️ 个人社区 |
| [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare) | 手机原始测量定位框架（GPS/Galileo 等） | Java | 73 | 🏷️ 个人社区 |
| [PRIDE-GeoDataLogger](https://github.com/PrideLab/PRIDE-GeoDataLogger) | PRIDE 团队手机多频 GNSS 与 IMU 采集工具 | — | 22 | 🏷️ 高校实验室 |

### 详细说明

#### [GPSTest](https://github.com/barbeau/gpstest)  
*🏷️ 个人社区 ★ 核心*

语言：Kotlin · 许可：Apache-2.0 · 星标约：2402 · 宿主：github

支持多星座双频、SBAS、精度评估与 NMEA/原始测量日志，和 Google 分析工具兼容，是手机 GNSS 测试事实标准之一。适合设备能力摸底与采数。不是精密定位解算器。

#### [GPSLogger](https://github.com/BasicAirData/GPSLogger)  
*🏷️ 个人社区*

语言：Java · 许可：GPL-3.0 · 星标约：504 · 宿主：github

记录轨迹与传感器辅助信息，户外测绘/运动轨迹常用。不做载波相位精密定位。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [bluetooth_gnss](https://github.com/ykasidit/bluetooth_gnss)  
*🏷️ 个人社区*

语言：Java · 许可：GPL-2.0 · 星标约：123 · 宿主：github

通过蓝牙连接外置接收机，在 Android 上使用 NTRIP 做 RTK/差分，已上架应用商店，野外测绘与兴趣玩家常用。适合手机加蓝牙板卡的移动作业。不是原始测量科研 Logger（见 GPSTest、gps-measurement-tools），精密测地仍取决于外置设备、天线与差分服务稳定性。蓝牙链路时延与丢包会表现为固定解不稳定。

#### [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare)  
*🏷️ 个人社区*

语言：Java · 许可：Apache-2.0 · 星标约：73 · 宿主：github

在 Android 上从原始测量解算位置，支持 GPS/Galileo 等，便于算法上机对比。适合教学与原型 App。维护节奏一般；长期采数与设备兼容性测试仍常搭配 GPSTest 等工具。
#### [PRIDE-GeoDataLogger](https://github.com/PrideLab/PRIDE-GeoDataLogger)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：22 · 宿主：github

PRIDE 团队面向智能手机的多频 GNSS 与 IMU 采集工具，便于把手机原始测量送入后续 PPP 或科学研究流程。适合手机大地测量、城市峡谷与行人导航试验。手机天线相位中心与占空比限制明显；采集前应规划时间同步、姿态记录与导出格式，以便对接 PRIDE-PPPAR 或自研脚本。

## 嵌入式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ubxlib](https://github.com/u-blox/ubxlib) | u-blox 官方嵌入式 C 库（GNSS/蜂窝 API） | C | 358 | 🏷️ 官方 |
| [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer) | ESP8266/ESP32 的 GNSS 授时 NTP/PTP 服务器 | C | 232 | 🏷️ 个人社区 |
| [esp32-xbee](https://github.com/nebkat/esp32-xbee) | ESP32 NTRIP/UART 桥接固件（Ardusimple） | C | 119 | 🏷️ 个人社区 |
| [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS) | STM32 u-blox GNSS 库（UBX，含 DMA） | C | 89 | 🏷️ 个人社区 |
| [satpulse](https://github.com/jclark/satpulse) | 跨平台 GNSS 授时、定位与接收机配置 GUI | Go | 63 | 🏷️ 个人社区 |
| [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker) | STM32 Primer2 平台的 GNSS 轨迹记录器 | C | 31 | 🏷️ 个人社区 |
| [esp32-gps](https://github.com/mrichar1/esp32-gps) | ESP32 上整合 GPS、蓝牙与 NTRIP/RTK 转发 | Python | 23 | 🏷️ 个人社区 |
| [GNSSClock](https://github.com/stevemarple/GNSS_Clock) | 基于 GNSS NMEA/PPS 的 Arduino 时钟 | C++ | 2 | 🏷️ 个人社区 |

### 详细说明

#### [ubxlib](https://github.com/u-blox/ubxlib)  
*🏷️ 官方*

语言：C · 许可：Apache-2.0 · 星标约：358 · 宿主：github

u-blox 官方开源的可移植 C 库，面向 MCU/RTOS 场景提供 GNSS 与蜂窝等产品统一 API，作为各平台 SDK 的附加层。Apache-2.0。适合嵌入式原始测量/配置联调；不是精密定位引擎，PC 端解析更常见 pyubx2 等工具。

#### [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：232 · 宿主：github

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
#### [GNSSClock](https://github.com/stevemarple/GNSS_Clock)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：2 · 宿主：github

在 Arduino 上用 GNSS（GPS/GLONASS/Galileo）NMEA 语句与 PPS 秒脉冲实现时钟与守时，方便嵌入式授时和业余无线电时间基准。适合单片机爱好者与简易时频同步。功能止于时钟/授时，不含 RTK 或精密 PVT；可用星座取决于所接 GNSS 模块固件。PPS 布线与晶振稳定度影响短期守时表现。

## 嵌入式/Arduino

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [SparkFun_u-blox_GNSS_v3](https://github.com/SparkFun/SparkFun_u-blox_GNSS_v3) | SparkFun Arduino 库：通过 Configuration Interface 驱动 u-blox GNSS 模块 | C++ | 104 | 🏷️ 个人社区 |

### 详细说明

#### [SparkFun_u-blox_GNSS_v3](https://github.com/SparkFun/SparkFun_u-blox_GNSS_v3)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT-style (SparkFun code) · 星标约：104 · 宿主：github

面向嵌入式/创客的 Arduino 库，用 u-blox Configuration Interface 配置与读取模块，便于采集原始测量或 NMEA。适合低成本接收机原型与教学；不是精密定位引擎，高级 RTK/PPP 仍需配合基站与解算软件。

## 原始测量

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_MobileCalculator](https://github.com/RogerioDoCarmo/GNSS_MobileCalculator) | Android 原始伪距 SPS 示例 | Java | 15 | 🏷️ 个人社区 |
| [androidGnss](https://github.com/AILocAR/androidGnss) | Android 原始 GNSS 伪距定位 MATLAB 代码 | MATLAB | 14 | 🏷️ 高校实验室 |

### 详细说明

#### [GNSS_MobileCalculator](https://github.com/RogerioDoCarmo/GNSS_MobileCalculator)  
*🏷️ 个人社区*

语言：Java · 许可：NOASSERTION · 星标约：15 · 宿主：github

在 Android 上读取 GNSS 原始伪距并实现标准单点定位（SPS）流程的开源示例（Java）。适合教学演示「手机原始测量→位置」链路。精度与完整性受手机芯片、占空比与 API 限制，不能替代测绘级 RTK；与 GPSTest、Google GNSS Logger 等工具互补。

#### [androidGnss](https://github.com/AILocAR/androidGnss)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：Apache-2.0 · 星标约：14 · 宿主：github

面向 Android 原始 GNSS 测量的 MATLAB 伪距定位示例与实验代码，方便在桌面端复现手机观测处理。适合课堂与算法对比。输入依赖手机端记录的原始测量文件；实时嵌入式部署需另接 Java/Kotlin 或 NDK 方案。
