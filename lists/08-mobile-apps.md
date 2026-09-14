# 移动与嵌入式应用 / Mobile Apps
> 共 **8** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。

## Android

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTest](https://github.com/barbeau/gpstest) | 开源 Android GNSS 测试与原始测量记录 | Kotlin | 2402 | ★ Star · 核心 |
| [GPSLogger](https://github.com/BasicAirData/GPSLogger) | Android 开源 GPS 轨迹记录器 | Java | 504 |  |
| [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare) | 安卓端用原始测量做定位的框架 | Java | 73 |  |

### 详细说明

#### [GPSTest](https://github.com/barbeau/gpstest)  
*★ Star · 核心*

语言：Kotlin · 许可：Apache-2.0 · 星标约：2402

支持多星座双频、SBAS、精度评估与 NMEA/原始测量日志，和 Google 分析工具兼容，是手机 GNSS 测试事实标准之一。适合设备能力摸底与采数。不是精密定位解算器。

#### [GPSLogger](https://github.com/BasicAirData/GPSLogger)

语言：Java · 许可：GPL-3.0 · 星标约：504

记录轨迹与传感器辅助信息，户外测绘/运动轨迹常用。不做载波相位精密定位。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [GNSS_Compare](https://github.com/TheGalfins/GNSS_Compare)

语言：Java · 许可：Apache-2.0 · 星标约：73

在手机上从原始测量解算位置，支持 GPS/Galileo 等，便于算法上机。维护节奏一般；采数仍常用 GPSTest。


## 嵌入式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer) | ESP8266/ESP32 的 GNSS 授时 NTP/PTP 服务器 | C | 232 |  |
| [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS) | STM32 u-blox GNSS 库（UBX，含 DMA） | C | 89 |  |
| [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker) | STM32 Primer2 平台的 GNSS 轨迹记录器 | C | 31 |  |
| [esp32-gps](https://github.com/mrichar1/esp32-gps) | ESP32 GPS 控制：串口/蓝牙/RTK/NTRIP | Python | 23 |  |
| [GNSSClock](https://github.com/stevemarple/GNSS_Clock) | 基于 GNSS NMEA/PPS 的 Arduino 时钟 | C++ | 2 |  |

### 详细说明

#### [GNSSTimeServer](https://github.com/Montecri/GNSSTimeServer)

语言：C · 星标约：232

以太网/WiFi GNSS 授时服务器：以 GPS/北斗/GLONASS/Galileo 为时间源，对外提供 NTP、RDATE、PTP，硬件基于 ESP8266/ESP32 与 Arduino 生态。适合实验室、业余台站本地时间同步。精度受模块、天线与网络抖动限制，达不到电信机房原子钟等级；天线与固件选项对照上游说明。

#### [STM32-GNSS](https://github.com/SimpleMethod/STM32-GNSS)

语言：C · 星标约：89

面向 STM32 的 u-blox GNSS 库，支持 UBX 协议与 DMA，作者称在 NEO-M8、MAX-M8、NEO-M9N 等模块上验证。适合嵌入式读取 NMEA/UBX、配置接收机。库本身不做高精度解算；若要 RTK，需模块固件支持并另接 NTRIP/电台改正数。不同 u-blox 固件协议细节仍有差异，注意版本。

#### [STM32Primer2-GNSS-Tracker](https://github.com/nemuisan/STM32Primer2_GNSS_Tracker)

语言：C · 星标约：31

运行于 STM32 Primer2 的 GNSS 轨迹记录固件/应用，把卫星定位点记下来便于回放与展示。适合嵌入式便携记录与爱好者硬件实验。硬件绑定 Primer2，功能以记录为主，不是跨平台定位 SDK，也不含 RTK 引擎。存储介质与采样间隔决定可记录轨迹时长。电池与存储容量共同限制连续记录时长。

#### [esp32-gps](https://github.com/mrichar1/esp32-gps)

语言：Python · 星标约：23

在 ESP32 上整合 GPS 与 NTRIP/RTK 改正转发，适合物联网终端原型。

#### [GNSSClock](https://github.com/stevemarple/GNSS_Clock)

语言：C++ · 星标约：2

在 Arduino 上用 GNSS（GPS/GLONASS/Galileo）NMEA 语句与 PPS 秒脉冲实现时钟与守时，方便嵌入式授时和业余无线电时间基准。适合单片机爱好者与简易时频同步。功能止于时钟/授时，不含 RTK 或精密 PVT；可用星座取决于所接 GNSS 模块固件。PPS 布线与晶振稳定度影响短期守时表现。
