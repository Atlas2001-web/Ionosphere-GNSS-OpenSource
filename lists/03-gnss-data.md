# GNSS 数据与格式 / GNSS Data I/O
> 共 **108** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

## RTCM/NTRIP

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyGPSClient](https://github.com/semuconsulting/PyGPSClient) | NMEA/UBX/RTCM/NTRIP 等协议的 Python 图形客户端 | Python | 839 | 🏷️ 个人社区 核心 |
| [ntrip-cpp](https://github.com/ybzwyrcld/ntrip) | NTRIP 2.0 的 C++ caster/client/server 示例 | C++ | 177 | 🏷️ 个人社区 |
| [pygnssutils](https://github.com/semuconsulting/pygnssutils) | NMEA/UBX/RTCM/NTRIP/SPARTN 的 Python CLI 工具集 | Python | 143 | 🏷️ 个人社区 |
| [ntripcaster-docker-bkg](https://github.com/goblimey/ntripcaster) | 容器化构建与运行 BKG NTRIP Caster 的 Docker 方案 | C | 139 | 🏷️ 个人社区 |
| [ntripclient](http://software.rtcm-ntrip.org/wiki/ntripclient) | BKG POSIX ntripclient：命令行拉取 NTRIP 数据流 | C | 129 | 🏷️ 官方 |
| [pyrtcm](https://github.com/semuconsulting/pyrtcm) | RTCM3 报文的 Python 解析与生成库 | Python | 115 | 🏷️ 个人社区 |
| [ntripserver](http://software.rtcm-ntrip.org/wiki/ntripserver) | BKG POSIX ntripserver：把本地 GNSS 流推到 NTRIP 播发器 | C | 74 | 🏷️ 官方 |
| [ntripcaster-libev](https://github.com/tisyang/ntripcaster) | 基于 libev 的高性能 NTRIP Broadcaster（C） | C | 68 | 🏷️ 个人社区 |
| [ntrip-go](https://github.com/go-gnss/ntrip) | Go 语言 NTRIP 客户端与服务端库 | Go | 62 | 🏷️ 个人社区 |
| [caster](https://github.com/Node-NTRIP/caster) | 支持 NTRIP V1/V2 的 Node.js caster 库 | TypeScript | 52 | 🏷️ 个人社区 核心 |
| [cors-relay](https://github.com/tisyang/cors-relay) | CORS/NTRIP 差分流中继与重分发 | C | 49 | 🏷️ 个人社区 |
| [rtcm](https://github.com/Node-NTRIP/rtcm) | RTCM 3 消息编解码（至 3.3） | TypeScript | 48 | 🏷️ 个人社区 |
| [baidu-ntripcaster](https://github.com/baidu/ntripcaster) | 百度开源的 NTRIP Caster 实现 | C | 46 | 🏷️ 个人社区 |
| [millipede-caster](https://github.com/pbeyssac/millipede-caster) | 高性能开源 NTRIP/RTK Caster（C） | C | 43 | 🏷️ 个人社区 |
| [nmea-msgs](https://github.com/ros-drivers/nmea_msgs) | ROS 包：NMEA 相关消息类型定义 | CMake | 38 | 🏷️ 个人社区 |
| [ntripbrowser](https://github.com/emlid/ntripbrowser) | CLI 查询 NTRIP caster 源表与挂载点 | Python | 32 | 🏷️ 个人社区 |
| [rtcm-rs](https://github.com/martinhakansson/rtcm-rs) | RTCM v3 编解码的 Rust crate | Rust | 32 | 🏷️ 个人社区 |
| [gstream](https://github.com/Jin-Whu/gstream) | 面向 GNSS 的开源数据流客户端库 | C++ | 20 | 🏷️ 高校实验室 |
| [NTRIPcaster-python](https://github.com/Rampump/NTRIPcaster) | 轻量 Python NTRIP Caster | Python | 20 | 🏷️ 个人社区 |
| [Caster_Project](https://github.com/KOROyo123/Caster_Project) | Libevent+Redis 跨平台 NTRIP Caster | C++ | 19 | 🏷️ 个人社区 |
| [ntripstreams](https://github.com/stenseng/ntripstreams) | Python NTRIP 协议读写接口 | Python | 16 | 🏷️ 个人社区 |
| [NtripCore](https://github.com/bouskdav/NtripCore) | .NET Core 轻量 NTRIP caster（rev.2） | C# | 14 | 🏷️ 个人社区 |
| [pyspartn](https://github.com/semuconsulting/pyspartn) | 解析 SPARTN 精密改正电文的 Python 库 | Python | 12 | 🏷️ 个人社区 |
| [AgOpenNtripCaster](https://github.com/AgOpenGPS-Official/AgOpenNtripCaster) | AgOpenGPS 生态的开源 NTRIP Caster（C#） | C# | 10 | 🏷️ 个人社区 |
| [ntripCaster-go](https://github.com/xk1yan/ntripCaster) | Go 高性能 NTRIP Caster | Go | 9 | 🏷️ 个人社区 |
| [ntrip-client](https://github.com/nav-solutions/ntrip-client) | 纯 Rust 的简单 NTRIP 客户端对象 | Rust | 4 | 🏷️ 个人社区 |
| [ntrip-core](https://github.com/greenforge-labs/ntrip-core) | Rust 异步 NTRIP 客户端（v1/v2 + TLS） | Rust | 4 | 🏷️ 个人社区 |
| [corshub](https://github.com/peinser/corshub) | 可自托管的 Python NTRIP v2 Caster（CORS 汇聚） | Python | 1 | 🏷️ 个人社区 |
| [ntrip-caster-go](https://github.com/symysak/ntrip-caster) | Go 实现的 NTRIP v1/v2 Caster：就近基站切换、挂载点认证与热重载 | Go | 1 | 🏷️ 个人社区 |
| [BKG-NtripCaster](https://igs.bkg.bund.de/ntrip/bkgcaster) | BKG 专业 NtripCaster：GPL 开源实时 GNSS 流播发服务器 | C | — | 🏷️ 官方 核心 |
| [BNC](https://igs.bkg.bund.de/ntrip/bnc) | BKG 开源多流 Ntrip 客户端：收 RTCM 并可做实时 PPP | C++ | — | 🏷️ 官方 核心 |
| [BNC-source-FTP](https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/) | BKG FTP：BNC 源码与多平台二进制直接下载目录 | C++ | — | 🏷️ 官方 |
| [BNS](http://software.rtcm-ntrip.org/wiki/BNS) | BKG Ntrip State Space Server：实时状态空间改正播发相关工具 | C++ | — | 🏷️ 官方 |
| [Caster-source-FTP](https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/) | BKG FTP：Professional NtripCaster 源码包直接下载 | C | — | 🏷️ 官方 |
| [EUREF-IP-Ntrip-overview](https://igs.bkg.bund.de/ntrip/index) | BKG/IGS NTRIP 数据与工具总览：流列表、BNC 与 Caster 入口 | various | — | 🏷️ 官方 |
| [RTCM-Ntrip-Software](http://software.rtcm-ntrip.org/) | RTCM-Ntrip 官方软件门户：BNC/Caster/POSIX 工具源码与文档 | C/C++ | — | 🏷️ 官方 核心 |

### 详细说明

#### [PyGPSClient](https://github.com/semuconsulting/PyGPSClient)  
*🏷️ 个人社区 核心*

语言：Python · 许可：BSD-3-Clause · 星标约：839 · 宿主：github

桌面 GUI 同时消化 NMEA、u-blox UBX、SBF、RTCM3、NTRIP 与 SPARTN，便于配置接收机、看星空图与差分链路。适合硬件联调、教学演示与低成本 RTK 调试。它是协议与可视化客户端，不是精密 PPP/RTK 解算引擎；底层解析依赖同作者的 pyubx2、pyrtcm、pygnssutils，深度算法请接 RTKLIB 或科研 PPP。

#### [ntrip-cpp](https://github.com/ybzwyrcld/ntrip)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：177 · 宿主：github

提供 NTRIP 2.0 协议下 caster、客户端与服务端示例，星标较高，适合嵌入 C++ 服务或学习握手与挂载点逻辑。二次开发差分转发、教学演示都常见。完整鉴权、集群与监控需自增；Python/Go 生态另有 pygnssutils 与 go-gnss/ntrip，运维桌面场景仍常看 BNC。

#### [pygnssutils](https://github.com/semuconsulting/pygnssutils)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：143 · 宿主：github

在 pyubx2/pyrtcm 之上提供命令行读写、广播与 NTRIP 客户端/caster 小工具，方便把协议流接到管道或测试架。适合自动化采集、回归测试与协议联调。定位解算、质量评估仍需外接 RTKLIB 或科研引擎；相对 BNC 更偏开发者脚本而非运维级多流平台，和 PyGPSClient 形成 CLI/GUI 互补。

#### [ntripcaster-docker-bkg](https://github.com/goblimey/ntripcaster)  
*🏷️ 个人社区*

语言：C · 许可：GPL-3.0 · 星标约：139 · 宿主：github

提供 Dockerfile 与说明，方便构建并运行经典 BKG NTRIP Caster，降低在自有服务器部署播发端的门槛。适合运维与教学试验。上游 BKG 许可与版本须单独遵守；生产环境还应配置监控、TLS 与用户管理。

#### [ntripclient](http://software.rtcm-ntrip.org/wiki/ntripclient)  
*🏷️ 官方*

语言：C · 许可：GPL · 星标约：129 · 宿主：official_site

官方轻量 NTRIP 客户端，从播发器订阅 RTCM 等流并写到标准输出或端口。源码位于 RTCM-Ntrip trunk。适合脚本化取流；需要解码/PPP/GUI 时改用 BNC。

#### [pyrtcm](https://github.com/semuconsulting/pyrtcm)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：115 · 宿主：github

专注 RTCM 3.x 消息编解码，可嵌入 NTRIP 客户端或自研差分链路，便于在 Python 里拆 MSM、站星改正。适合不想拉起完整 BNC 又能看懂差分电文的人。不含 caster 调度与精密定位；与 go-gnss/ntrip、ybzwyrcld/ntrip、nunojpg 系列传输层工具互补，和 pyubx2 同属 semuconsulting 协议栈。

#### [ntripserver](http://software.rtcm-ntrip.org/wiki/ntripserver)  
*🏷️ 官方*

语言：C · 许可：GPL · 星标约：74 · 宿主：official_site

RTCM-Ntrip 官方仓库中的 POSIX ntripserver，用于将接收机或文件流上传至 NtripCaster。源码见 software.rtcm-ntrip.org 浏览器。轻量适合嵌入式/服务器脚本；完整 GUI 与 PPP 请用 BNC。GitHub 上存在社区镜像。

#### [ntripcaster-libev](https://github.com/tisyang/ntripcaster)  
*🏷️ 个人社区*

语言：C · 许可：BSD-3-Clause · 星标约：68 · 宿主：github

基于 C 与 libev 的事件驱动 NTRIP Broadcaster，强调吞吐与并发连接，适合自建 CORS 中继与播发试验。可与同作者 cors-relay 等工具搭配。协议细节与管理界面因版本而异，公网服务请自行做认证与加固。

#### [ntrip-go](https://github.com/go-gnss/ntrip)  
*🏷️ 个人社区*

语言：Go · 许可：Apache-2.0 · 星标约：62 · 宿主：github

用 Go 实现 NTRIP 客户端与服务端能力，便于嵌入云原生或高并发转发服务，部署二进制简单。适合想用单一语言栈做差分流网关的人。协议覆盖、挂载点管理与运维工具不如 BNC 成熟；与 ybzwyrcld/ntrip、nunojpg 系列可按语言生态与性能需求选型。生产环境还需自行补齐日志、限流与监控。

#### [caster](https://github.com/Node-NTRIP/caster)  
*🏷️ 个人社区 核心*

语言：TypeScript · 许可：GPL-3.0 · 星标约：52 · 宿主：github

用 TypeScript/Node 实现的 NTRIP caster 库，声明支持 V1/V2，便于自建小型网络 RTK 分发服务。适合实验室 CORS 试验与课程演示。高并发、计费鉴权与运维监控不如专用商业方案或 BNC 生态成熟；上线前应做压测、源挂死与证书过期等故障演练。

#### [cors-relay](https://github.com/tisyang/cors-relay)  
*🏷️ 个人社区*

语言：C · 许可：BSD-3-Clause · 星标约：49 · 宿主：github

把 CORS 差分数据中继再分发的 C 程序，基于 libev，常见于对接千寻等源并自建内网 caster 的场景。运维本地 RTK 网络、实验室分流时很实用。不是完整商业 caster 套件，账号权限、计费与高可用需自建；可与 ybzwyrcld/ntrip、BNC、ntripserver 对照部署复杂度。

#### [rtcm](https://github.com/Node-NTRIP/rtcm)  
*🏷️ 个人社区*

语言：TypeScript · 许可：GPL-3.0 · 星标约：48 · 宿主：github

覆盖至 RTCM 3.3 的消息编解码，JS/TS 生态少见。适合 Web 或 Node 实时应用。GPL；高性能 C++ 嵌入另选其他实现。

#### [baidu-ntripcaster](https://github.com/baidu/ntripcaster)  
*🏷️ 个人社区*

语言：C · 许可：NOASSERTION · 星标约：46 · 宿主：github

百度公开的 NTRIP Caster 相关实现，可作自建播发与协议学习的对照样本。适合对比 BKG 与社区实现看消息路由。文档与许可声明以仓库当前文件为准；上线前须完成压力、安全与兼容性测试。

#### [millipede-caster](https://github.com/pbeyssac/millipede-caster)  
*🏷️ 个人社区*

语言：C · 许可：BSD-3-Clause · 星标约：43 · 宿主：github

Millipede 是面向 RTK/CORS 场景的开源 NTRIP caster（C，BSD-3-Clause），强调吞吐与可运维部署，适合自建差分播发或做多基站接入试验。协议与鉴权能力需对照其文档与版本说明；公网部署仍要自行处理 TLS、账号与带宽监控。相对 BKG Professional Caster，社区文档更轻，但源码开放便于二次开发。

#### [nmea-msgs](https://github.com/ros-drivers/nmea_msgs)  
*🏷️ 个人社区*

语言：CMake · 许可：— · 星标约：38 · 宿主：github

ros-drivers 维护的 nmea_msgs，定义与 NMEA 标准相关的 ROS 消息，方便驱动、导航与记录节点交换 GNSS 语句。适合 ROS 机器人接入 GNSS 接收机。只提供消息契约，不含语句解析与 PVT；解析与定位需配合 nmea_navsat_driver 等包。消息字段随 ROS 发行版可能微调，编译前核对依赖。

#### [ntripbrowser](https://github.com/emlid/ntripbrowser)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：32 · 宿主：github

Emlid 发布的 CLI，用于拉取并浏览 NTRIP caster 的 source table，快速查看挂载点、位置与格式摘要。适合在接入 RTK 流前做 caster 探活与选站。它不做解算，只解决「这个 caster 里有什么」；下游仍需 ntripclient/BNC/接收机客户端。

#### [rtcm-rs](https://github.com/martinhakansson/rtcm-rs)  
*🏷️ 个人社区*

语言：Rust · 许可：Apache-2.0 · 星标约：32 · 宿主：github

专注 RTCM v3 消息编解码的 Rust crate，便于在服务端或嵌入式旁路处理差分与 SSR 流。适合自建 NTRIP 管道与协议测试。消息类型覆盖随版本增加；与 nav-solutions、pyrtcm 互操作时注意可选字段、端序与厂商扩展。

#### [gstream](https://github.com/Jin-Whu/gstream)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：20 · 宿主：github

面向 GNSS 实时试验的开源数据流客户端库，可把 NTRIP、串口等多源观测收成可编程接口。适合自建监听、转发与录包原型。相对 BKG BNC 或商业 caster 客户端，功能面与运维工具更窄；协议边界、断线重连与鉴权要实测，关键链路建议加监控指标与原始流回放。

#### [NTRIPcaster-python](https://github.com/Rampump/NTRIPcaster)  
*🏷️ 个人社区*

语言：Python · 许可：NOASSERTION · 星标约：20 · 宿主：github

用 Python 实现的简易 NTRIP caster，把 GNSS 观测或 RTCM 改正流转发给客户端，便于实验室或农场级自建播发。适合协议学习与小流量试验；高并发、鉴权审计与生产加固不如 BKG/Millipede 一类实现，公网使用需自行评估安全与稳定性。

#### [Caster_Project](https://github.com/KOROyo123/Caster_Project)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：19 · 宿主：github

以 Libevent 与 Redis 为底座的多平台 NTRIP caster（C++，MIT），宣称支持 NTRIP 1.0/2.0，面向需要会话状态与扩展的自建播发场景。适合有 C++/运维能力的团队做二次开发。部署复杂度高于脚本级 caster；请核对其协议覆盖与鉴权细节后再上生产。

#### [ntripstreams](https://github.com/stenseng/ntripstreams)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：16 · 宿主：github

用 Python 与 NTRIP Caster/客户端传 GNSS 流，适合接 RTCM 改正。适合自建流处理原型。完整 PPP 引擎与播发管理需另接 BNC/自研。

#### [NtripCore](https://github.com/bouskdav/NtripCore)  
*🏷️ 个人社区*

语言：C# · 许可：MIT · 星标约：14 · 宿主：github

用 .NET Core 写的轻量 NTRIP caster，支持 NTRIP revision 2，并带自动就近基站选择一类便利功能，方便 Windows/跨平台服务化部署。适合 .NET 技术栈的 CORS/农机差分试验。功能面相对 BKG 专业版更窄，公网与高可用仍需自行补齐监控与安全策略。

#### [pyspartn](https://github.com/semuconsulting/pyspartn)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：12 · 宿主：github

补齐 SPARTN 精密改正电文解析，方便把 u-blox 等常用 SSR 风格改正接到 NTRIP 或串口流水线。适合低成本 PPP/RTK 改正数试验与协议调试。与 pyrtcm 分工明确：一个管 SPARTN，一个管 RTCM；终端固定效果取决于改正源质量与接收机配置，不能指望解析库单独提高精度。

#### [AgOpenNtripCaster](https://github.com/AgOpenGPS-Official/AgOpenNtripCaster)  
*🏷️ 个人社区*

语言：C# · 许可：— · 星标约：10 · 宿主：github

面向农业自动驾驶与 AgOpenGPS 社区的 NTRIP 播发端（C#），便于农场自建差分播发。适合 DIY CORS 与农机联调。运维、认证与安全加固通常弱于 BKG 级 caster；公网部署需自行处理账号与带宽监控。

#### [ntripCaster-go](https://github.com/xk1yan/ntripCaster)  
*🏷️ 个人社区*

语言：Go · 许可：MIT · 星标约：9 · 宿主：github

Golang 编写的高性能 NTRIP caster 服务软件，便于容器化与横向扩展试验。适合云原生差分播发原型。请对照其 README 确认协议版本、鉴权与挂载点管理能力；关键业务建议与 BKG caster 做互通测试。

#### [ntrip-client](https://github.com/nav-solutions/ntrip-client)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：4 · 宿主：github

纯 Rust 实现的轻量 NTRIP 客户端对象，便于嵌进 nav-solutions 或其他 Rust GNSS 工具链做实时拉流。适合自建差分/SSR 管道原型。功能少于 BNC 与专业运维客户端；TLS、NTRIPv2、挂载点列表与重连策略使用前应读文档，并用断网、鉴权失败等用例做回归。

#### [ntrip-core](https://github.com/greenforge-labs/ntrip-core)  
*🏷️ 个人社区*

语言：Rust · 许可：MIT · 星标约：4 · 宿主：github

面向 Rust 的异步 NTRIP 客户端库（MIT，Tokio），支持 NTRIP v1/v2、rustls TLS、源表解析、就近挂载点选择、重连与 HTTP 代理 CONNECT。适合嵌入自研差分客户端或边缘网关。不是完整 caster；RTCM 解码与定位仍需另接 pyrtcm/RTKLIB 等。

#### [corshub](https://github.com/peinser/corshub)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：1 · 宿主：github

Peinser 发布的自托管 NTRIP v2 caster：汇聚多基站 RTCM 改正并通过 HTTPS 分发给流动站，支持就近挂载点与可审计配置。BSD-3-Clause，适合小型 CORS/社区差分试验。公网部署仍需自行处理 TLS 终结、账号与带宽；功能深度不及 BKG Professional Caster，但源码开放便于二次开发。

#### [ntrip-caster-go](https://github.com/symysak/ntrip-caster)  
*🏷️ 个人社区*

语言：Go · 许可：— · 星标约：1 · 宿主：github

轻量 NTRIP 播发端，支持 v1/v2 客户端拉取与基站推送、按 GGA 就近切换虚拟挂载点、账号认证与 SIGHUP 热重载。适合自建小型 CORS/农机差分播发；密码明文配置、尚无原生 TLS，公网部署需前置反向代理并自行加固。许可未在 GitHub 标明 SPDX，使用前请确认上游条款。

#### [BKG-NtripCaster](https://igs.bkg.bund.de/ntrip/bkgcaster)  
*🏷️ 官方 核心*

语言：C · 许可：GPL · 星标约：— · 宿主：official_site

德国联邦制图与大地测量局发布的 NTRIP 1/2 播发器，基于 Icecast，可同时服务大量客户端。2024 年 9 月起免费提供源码与软件，下载见 BKG FTP。只做流分发不解码内容，不含 VRS；与 BNC 客户端配套常用于 IGS/EUREF 实时站运维与教研演示。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [BNC](https://igs.bkg.bund.de/ntrip/bnc)  
*🏷️ 官方 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：— · 宿主：official_site

德国 BKG 维护的开源多流 NTRIP 客户端，解码 RTCM 2/3，支持实时 PPP、高采样 RINEX 与质量编辑，提供 GUI 与批处理。源码 GPL-3，官方二进制见 BKG FTP。面向实时站运维与教研；微服务化部署需自行封装。

#### [BNC-source-FTP](https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/)  
*🏷️ 官方*

语言：C++ · 许可：GPL-3.0 · 星标约：— · 宿主：official_site

BKG 提供的 BNC 发行目录，含 GPL-3 源码包、各发行版二进制与变更说明，与产品介绍页互补，便于脚本化拉取固定版本做复现。使用时注意版本与依赖库匹配；功能说明与 PPP 选项仍以 BNC 主页文档为准。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。

#### [BNS](http://software.rtcm-ntrip.org/wiki/BNS)  
*🏷️ 官方*

语言：C++ · 许可：GPL · 星标约：— · 宿主：official_site

BKG 的 Ntrip 状态空间服务器条目，面向实时 SSR/改正信息播发场景，源码与说明见 RTCM-Ntrip 发行包。适合研究实时 PPP/SSR 链路搭建；现代部署更常见 BNC 与 Professional Caster 组合，本工具偏专用或历史工作流，接入前请对照当前 trunk 文档。

#### [Caster-source-FTP](https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/)  
*🏷️ 官方*

语言：C · 许可：GPL · 星标约：— · 宿主：official_site

可直接获取 ntripcaster 源码 tar 与校验文件的 FTP 目录，对应 BKG 专业播发器免费开源发行。运维部署时可固定版本号拉取并核对 sha256。配置与安全补丁见同目录 CHANGES 与手册；功能介绍见 bkgcaster 产品页。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [EUREF-IP-Ntrip-overview](https://igs.bkg.bund.de/ntrip/index)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

BKG 托管的 NTRIP/实时 GNSS 服务总览，提供流列表、归档与 BNC/Caster 工具入口。搭建或接入 IGS 实时流时的官方导航页。具体开源组件请分别进入 BNC、Caster 与 RTCM-Ntrip 软件站核对版本与许可证。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [RTCM-Ntrip-Software](http://software.rtcm-ntrip.org/)  
*🏷️ 官方 核心*

语言：C/C++ · 许可：GPL (components) · 星标约：— · 宿主：official_site

BKG/RTCM 维护的 NTRIP 开源软件 Trac 门户，集中入口含 BNC、Professional Caster、POSIX ntripserver/client、BNS、rtcm3torinex 等。可浏览源码树与变更日志。部署前请核对各组件许可证与最新标签；专业播发器亦见 BKG 独立下载页。

## Android/RINEX

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [android_rinex](https://github.com/rokubun/android_rinex) | GnssLogger/GPSTest 日志转 RINEX | Python | 104 | 🏷️ 个人社区 |
| [BUAA-RINEX-Convertor](https://github.com/Jia-le-wang/BUAA-RINEX-Convertor) | 北航：GnssLogger 文本转 RINEX 3.04 | C++ | 20 | 🏷️ 个人社区 |

### 详细说明

#### [android_rinex](https://github.com/rokubun/android_rinex)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-2-Clause · 星标约：104 · 宿主：github

把 Android GNSS Logger / GPSTest 的 CSV 原始测量转成 RINEX，衔接手机数据与经典 GNSS 软件。适合智能手机 PPP/RTK 实验。手机天线/钟差特性仍须在定位端特殊处理。

#### [BUAA-RINEX-Convertor](https://github.com/Jia-le-wang/BUAA-RINEX-Convertor)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：20 · 宿主：github

将 Google GnssLogger 文本日志转为 RINEX 3.04，面向安卓原始观测科研。可与 android_rinex 对照输出差异。维护与星座覆盖需实测。

## 质量检查

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pinot](https://github.com/purpleskyfall/pinot) | “Pinot is not only TEQC”——开源 GNSS 数据质检/预处理取向工具 | Python | 25 | 🏷️ 个人社区 核心 |
| [RNXQCE](https://github.com/cuizilu/RNXQCE) | RINEX 2/3 质量检查工具包，定位为 TEQC 停更后的替代取向 | Fortran | 6 | 🏷️ 个人社区 |
| [geoveil-cn0](https://github.com/miluta7/geoveil-cn0) | Rust/Python：RINEX CN0 质量评分与干扰/欺骗/干扰检测 | Rust | 3 | 🏷️ 个人社区 |
| [grinq](https://github.com/PJarrin/grinq) | RINEX 镜像与 Anubis QC 的 Python 工具箱 | Python | 1 | 🏷️ 个人社区 |
| [Anubis](https://gnutsoftware.com/software/anubis/) | G-Nut/Anubis：多 GNSS RINEX/RTCM 质量检查（Free 开源） | C++ | — | 🏷️ 个人社区 核心 |
| [Anubis-Free-Download](https://gnutsoftware.com/software/anubis/download) | G-Nut/Anubis Free 下载：GPL 源码与 Linux 预编译（Pro 为商业） | C++ | — | 🏷️ 个人社区 |
| [plot-Anubis](https://www.pecny.cz/sw/plots/anubis/) | GOP/Pecny 提供的 Anubis XTR 质检结果静态绘图脚本 | Perl | — | 🏷️ 高校实验室 |
| [TEQC](https://www.unavco.org/software/data-processing/teqc/teqc.html) | UNAVCO/GAGE 经典 TEQC：翻译/编辑/质检（已 EOL，闭源免费） | binary (closed) | — | 🏷️ 官方 核心 |

### 详细说明

#### [pinot](https://github.com/purpleskyfall/pinot)  
*🏷️ 个人社区 核心*

语言：Python · 许可：GPL-2.0 · 星标约：25 · 宿主：github

口号 “Pinot is not only TEQC”，用 Python 做 GNSS 观测质量检查与预处理，意在填补 TEQC 停更后的工具缺口。适合 RINEX 质控、教学与脚本化入库。功能完备度与生态仍不及 Anubis/gfzrnx 组合；切换工具时应用标准站对比指标定义，避免质控阈值误伤。

#### [RNXQCE](https://github.com/cuizilu/RNXQCE)  
*🏷️ 个人社区*

语言：Fortran · 许可：— · 星标约：6 · 宿主：github

Fortran 编写的 GNSS 观测预处理与质量检查工具，宣称支持 RINEX 2/3，定位为 TEQC 停更后的替代取向之一。适合测站运维与数据入库前检查。社区体量小于 Anubis；质控指标与历史 TEQC 输出未必逐项相同，切换时要重训阈值阈值。

#### [geoveil-cn0](https://github.com/miluta7/geoveil-cn0)  
*🏷️ 个人社区*

语言：Rust · 许可：MIT · 星标约：3 · 宿主：github

GNSS 信号质量分析库，输出 0–100 综合评分、星空图与时序，并检测 jamming/spoofing/interference；支持 RINEX 2/3/4 与 Hatanaka。MIT，PyPI。适合 CORS 台站健康度与干扰监测；欺骗检测依赖导航文件可见性对比，算法阈值非认证级威胁情报。

#### [grinq](https://github.com/PJarrin/grinq)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

GRINQ（MIT，DOI 10.5281/zenodo.22228489）面向 GNSS 数据中心作业：多归档 RINEX 检索与镜像、台站管理，并封装 Anubis 生成质检统计。适合区域网运维脚本。QC 依赖需另行注册获取 Anubis 二进制；EarthScope 拉取需安装兼容版 earthscope-sdk。仓库较新，接口可能随版本调整。

#### [Anubis](https://gnutsoftware.com/software/anubis/)  
*🏷️ 个人社区 核心*

语言：C++ · 许可：GPL-3.0 (Free); Pro commercial · 星标约：— · 宿主：official_site

面向数据中心与用户的多星座观测质检工具，支持 RINEX 2/3 与 RTCM 元数据/定量/定性检查及简易 SPP。Free 档提供 Linux 源码（GPL-3）；Pro/实时为商业版。teqc EOL 后常用替代之一，本身不是精密定位引擎。

#### [Anubis-Free-Download](https://gnutsoftware.com/software/anubis/download)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 (Free tier) · 星标约：— · 宿主：official_site

Anubis 免费档下载入口，提供 Linux 预编译与 GPL-3 源码，覆盖基础事后 QC；Pro/实时功能单独收费。收录时仅指向免费开源档。适合替代部分 TEQC 质检流程；若需编辑流或实时监控，请另行评估商业授权档是否必要。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [plot-Anubis](https://www.pecny.cz/sw/plots/anubis/)  
*🏷️ 高校实验室*

语言：Perl · 许可：free (as-is) · 星标约：— · 宿主：official_site

捷克大地测量观测台相关页面提供的 plot_anubis.pl，读取 Anubis 输出的 XTR 生成单站质检图，免费且无支持承诺。适合批量为数据中心出静态图；若需交互仪表盘或实时告警，应评估 Anubis 商业档或其他可视化栈。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。

#### [TEQC](https://www.unavco.org/software/data-processing/teqc/teqc.html)  
*🏷️ 官方 核心*

语言：binary (closed) · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

长期主导 GNSS 预处理的 Translate/Edit/Quality Check 工具，支持多厂商原始格式转 RINEX、抽稀、窗口与粗差检查。源码因厂商 NDA 未公开；2019-02-25 终版后宣布 EOL，官网仍提供多平台二进制。新站建议并行评估 Anubis、GFZRNX、GNSSTK 等开源替代。

## 接收机下载/RINEX转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [autorino](https://github.com/IPGP/autorino) | IPGP 开源：自动拉取主流厂商接收机原始数据并转为 RINEX3/4 | Python | 11 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [autorino](https://github.com/IPGP/autorino)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：GPL-3.0 · 星标约：11 · 宿主：github

巴黎地球物理研究所（IPGP）维护的 Python 工具，对接 Leica/Septentrio/Topcon/Trimble/BINEX 等厂商官方转换链，强调近实时下载、RINEX3/4 转换、拼接与元数据编辑（联动 rinexmod）。适合台网自动化入库。依赖各厂商转换程序授权与安装；非定位解算引擎。

## 掩星格式转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cosmic-crunch](https://github.com/ErickShepherd/cosmic-crunch) | 批量下载 JPL GENESIS COSMIC-1 掩星剖面并转 netCDF4 | Python | 0 | 🏷️ 个人社区 |

### 详细说明

#### [cosmic-crunch](https://github.com/ErickShepherd/cosmic-crunch)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：0 · 宿主：github

把 JPL GENESIS 发布的 COSMIC-1 ASCII Level-2 大气/相关剖面批量拉取并转成 netCDF4，方便对接现代 Python 分析栈。适合需要统一文件格式做掩星气候统计的人。注意它瞄的是 JPL GENESIS 大气剖面链路，不是 CDAAC ionPhs/ionPrf 电离层产品的专用阅读器；电离层 excess phase 请另走 CDAAC/AWS RO。

## Hatanaka/CRX

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [hatanaka](https://github.com/valgur/hatanaka) | Python 调用的 Hatanaka 压缩/解压 | C | 26 | 🏷️ 个人社区 |
| [crz2rnx](https://github.com/zhufengGNSS/crz2rnx) | Hatanaka RNX2CRX/CRX2RNX 相关程序整理（v4 系） | C | 9 | 🏷️ 高校实验室 |
| [crx2rnx](https://github.com/nav-solutions/crx2rnx) | Rust 实现的 CRX2RNX 命令行工具 | Rust | 8 | 🏷️ 个人社区 |
| [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html) | 日本地理院官方 Hatanaka/CompactRINEX 压缩与恢复工具 | C | — | 🏷️ 官方 核心 |
| [RNXCMP-LICENSE](https://terras.gsi.go.jp/ja/crx2rnx/LICENSE.txt) | 日本地理院 RNXCMP 许可证原文（使用/再分发须引用） | text | — | 🏷️ 官方 |

### 详细说明

#### [hatanaka](https://github.com/valgur/hatanaka)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：26 · 宿主：github

把 Hatanaka（RNXCMP）压缩解压接到 Python，方便批量解 CRX。适合 IGS 数据湖前处理。算法权威来源仍是 GSI RNXCMP；本仓库是便利封装。

#### [crz2rnx](https://github.com/zhufengGNSS/crz2rnx)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：9 · 宿主：github

整理 Hatanaka 压缩相关的 RNX2CRX/CRX2RNX 程序，方便在无外网环境解压紧凑 RINEX。适合镜像官方 RNXCMP 流程与批量预处理。请核对与国土地理院官方包版本一致性；长期应以官方发布为准，本仓库更适合作为备份或教学拷贝。

#### [crx2rnx](https://github.com/nav-solutions/crx2rnx)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：8 · 宿主：github

Rust 版 Hatanaka 解压 CLI，便于现代工具链集成。适合不想绑官方 Fortran/C 发行包的场景。与官方 RNXCMP 的比特级兼容性需用样例回归。

#### [RNXCMP](https://terras.gsi.go.jp/ja/crx2rnx.html)  
*🏷️ 官方 核心*

语言：C · 许可：GSI terms (cite Hatanaka 2008) · 星标约：— · 宿主：official_site

GSI 的 RNXCMP（RNX2CRX/CRX2RNX）将 RINEX 2/3/4 观测与 CompactRINEX 互转，是 IGS 数据交换事实标准。官网提供多平台二进制与源码包，使用须遵循地理院条款并引用文献。GitHub 多为镜像，校验请用本页发行。

#### [RNXCMP-LICENSE](https://terras.gsi.go.jp/ja/crx2rnx/LICENSE.txt)  
*🏷️ 官方*

语言：text · 许可：GSI Website Terms (cite Hatanaka 2008) · 星标约：— · 宿主：official_site

GSI 公布的 RNXCMP 许可文本，基于地理院网站条款并要求修改再分发时引用 Hatanaka 2008 文献。打包分发 CompactRINEX 工具或写入衍生软件前应阅读本文件。功能实现与二进制仍以 crx2rnx 主下载页的官方源码包为准。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 周跳

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cycle-slip-correction](https://github.com/embrace-inpe/cycle-slip-correction) | 周跳分析与改正命令行工具 | Python | 14 | 🏷️ 官方 |
| [DRCycleSlip](https://github.com/Jin-Whu/DRCycleSlip) | 周跳探测与修复的 Python 实现 | Python | 4 | 🏷️ 高校实验室 |

### 详细说明

#### [cycle-slip-correction](https://github.com/embrace-inpe/cycle-slip-correction)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：14 · 宿主：github

命令行分析并尝试改正周跳，常用于低纬电离层活跃区数据。适合前处理试验。与定位引擎内置周跳探测策略可能不一致，接入 PPP 前要统一标志。

#### [DRCycleSlip](https://github.com/Jin-Whu/DRCycleSlip)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：4 · 宿主：github

提供 GNSS 周跳探测与修复相关 Python 脚本，便于在预处理阶段清理相位观测、服务后续 TEC 或定位。适合教学和小数据试验。算法完备性与多星座鲁棒性有限，生产级 QC 更常见 Anubis 或规则化流水线；可与 embrace-inpe/cycle-slip-correction 对照方法与评价指标。

## 格式编解码

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EarthScope-gnsstools](https://gitlab.com/earthscope/gnsstools) | EarthScope 官方 Go 库：RINEX/RTCM/BINEX 编解码与处理流水线 | Go | 6 | 🏷️ 官方 |

### 详细说明

#### [EarthScope-gnsstools](https://gitlab.com/earthscope/gnsstools)  
*🏷️ 官方*

语言：Go · 许可：— · 星标约：6 · 宿主：gitlab

EarthScope（原 UNAVCO/GAGE 体系）维护的 Go GNSS 工具集，含 RINEX/RTCM/BINEX/SBF 等编解码、NTRIP 客户端、SPP/TDCP 流水线及可选 TileDB 地理数据模块。适合构建现代数据管道；定位算法深度不及专用 PPP 套件。星数不高但机构背书明确。

## 下载/处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [FAST](https://github.com/ChangChuntao/FAST) | GNSS 数据下载、质量分析、SPP 与选站 | Python | 206 | 🏷️ 个人社区 ★ 核心 |

### 详细说明

#### [FAST](https://github.com/ChangChuntao/FAST)  
*🏷️ 个人社区 ★ 核心*

语言：Python · 许可：GPL-3.0 · 星标约：206 · 宿主：github

模块化 Python 软件：IGS/数据下载、质量分析、单点定位、测站选择等，中文用户多。适合日常数据准备。精密 PPP-AR/科研级 POD 仍需 PRIDE/Ginan 等。

## 下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GAMPII-GOOD](https://github.com/zhouforme0318/GAMPII-GOOD) | GOOD：GNSS 观测与产品下载器（GAMP II 配套） | C++ | 123 | 🏷️ 个人社区 |
| [gnss-downloader](https://github.com/Mereithhh/gnss-downloader) | PyQt5 GUI：从 NASA/WHU FTP 下载 GNSS 数据 | Python | 23 | 🏷️ 个人社区 |
| [GDDS](https://github.com/LECUT/GDDS) | IGS/CORS/产品/时序等多模块 GNSS 下载 | Python | 13 | 🏷️ 个人社区 |
| [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader) | Embrace 空间天气数据服务 API 的自动下载示例 | Python | 4 | 🏷️ 官方 |

### 详细说明

#### [GAMPII-GOOD](https://github.com/zhouforme0318/GAMPII-GOOD)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：123 · 宿主：github

面向 GNSS 观测值与精密产品的批量下载工具（GOOD），常与 GAMP/PPP 研究流程一起使用，星标较高。适合搭数据处理流水线的数据准备段。定位解算请接 GAMP_PPPH、PRIDE 或 RTKLIB；镜像源选择与断点续传策略需按网络环境自测，功能定位上可与 FAST 等下载器对照。批量任务建议记录校验和，避免镜像不同步。

#### [gnss-downloader](https://github.com/Mereithhh/gnss-downloader)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：23 · 宿主：github

带界面的 GNSS 数据下载器，对接常见 FTP 镜像，降低新手门槛。适合偶发下载。大规模自动化与断点策略不如专用脚本/FAST。

#### [GDDS](https://github.com/LECUT/GDDS)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：13 · 宿主：github

分模块下载全球 IGS、后处理产品、区域 CORS、时间序列等，并含解压。适合数据中心助理式抓取。维护活跃度与镜像可用性需自行跟踪。

#### [swds-api-downloader](https://github.com/embrace-inpe/swds-api-downloader)  
*🏷️ 官方*

语言：Python · 许可：MIT · 星标约：4 · 宿主：github

演示如何调用 Embrace 空间天气数据服务（SWDS）API 自动下载产品，方便把取数写进科研脚本。适合 GNSS—空间天气交叉研究的数据入口。接口字段、鉴权与限流可能随官方升级变化；时间范围与产品类型以站点文档为准，勿长期硬编码过期端点。

## 自动化处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [geode](https://github.com/demiangomez/geode) | 自动化 GNSS 数据处理与管理框架 | Python | 61 | 🏷️ 个人社区 |

### 详细说明

#### [geode](https://github.com/demiangomez/geode)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：61 · 宿主：github

把下载、处理、分析、管理串成 Python 框架，减少手写胶水。适合中等规模台网运维原型。核心估计算法深度取决于所接后端。

## RINEX读写

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [georinex](https://github.com/geospace-code/georinex) | 高速 Python RINEX 2/3 NAV/OBS/SP3 读入与 HDF5 转换 | Python | 269 | 🏷️ 高校实验室 🔀 ★ 核心 |
| [rinex](https://github.com/nav-solutions/rinex) | Rust RINEX 解析/生成与 RINEX-Cli（含 SPP/PPP） | Rust | 126 | 🏷️ 个人社区 核心 |
| [RinexReader](https://github.com/aaronboda24/RinexReader) | C++ RINEX 2.x/3.x 读取器 | C++ | 38 | 🏷️ 个人社区 |
| [READ_GNSS](https://github.com/dzd9798/READ_GNSS) | MATLAB 读取多种 GNSS 文件（含 RINEX/IONEX） | MATLAB | 10 | 🏷️ 个人社区 |
| [GNSSNexus-rinex](https://github.com/GNSSNexus/rinex) | RINEX 相关读写/处理组件 | Rust | — | 🏷️ 个人社区 |

### 详细说明

#### [georinex](https://github.com/geospace-code/georinex)  
*🏷️ 高校实验室 🔀 ★ 核心*

语言：Python · 许可：MIT · 星标约：269 · 宿主：github

Python 里最常用的 RINEX 读写库之一，覆盖观测/导航/SP3，可批量转 HDF5，速度接近 C。Atlas2001-web 已 fork。适合数据分析与 TEC/PPP 前处理。写回复杂 RINEX4/RTCM 不是长项；QC 可接 Anubis/rinex-cli。

#### [rinex](https://github.com/nav-solutions/rinex)  
*🏷️ 个人社区 核心*

语言：Rust · 许可：MPL-2.0 · 星标约：126 · 宿主：github

GeoRust/nav-solutions 系 RINEX 库，附 RINEX-Cli，可做质检、SPP/PPP、CGGTTS 等，社区常把它比作 teqc/Anubis/gLAB 的开源组合拳。适合要强类型与高性能 IO 的人。学习曲线比 Python 陡；生态仍在演进。

#### [RinexReader](https://github.com/aaronboda24/RinexReader)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：38 · 宿主：github

轻量 C++ RINEX 读取，覆盖 GPS/GLONASS/Galileo 等常见情况。适合嵌入自研 C++ 程序。功能广度不及 gnsstk；写文件与 QC 需自补。

#### [READ_GNSS](https://github.com/dzd9798/READ_GNSS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：10 · 宿主：github

在 MATLAB 中读入常见 GNSS 相关文件（含 RINEX、IONEX 等），降低自写解析器的成本，方便后续 TEC 或定位实验。适合已有 MATLAB 工作流的学生课题组。功能广度与健壮性不如 georinex、gnsstk；大型工程或多星座新格式建议仍用专门 IO 库并做交叉校验。遇到新 RINEX 版本时应抽检字段再批量入库。

#### [GNSSNexus-rinex](https://github.com/GNSSNexus/rinex)  
*🏷️ 个人社区*

语言：Rust · 许可：Apache-2.0 · 星标约：— · 宿主：github

GNSSNexus 下的 RINEX 组件，适合特定工具链内使用。选型时与 georinex、nav-solutions/rinex 比较维护活跃度与格式版本覆盖。

## RINEX工具

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [uNavTools](https://github.com/IvAn190/uNavTools) | u-blox→RINEX 工具集，内置基于 CSSRlib 的 RTK/PPP | Python | 10 | 🏷️ 个人社区 |
| [GFZRNX](https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox) | GFZ 的 RINEX 检查/拼接/抽样工具箱（科研非商用免费） | binary toolkit | — | 🏷️ 官方 |
| [GFZRNX-UserGuide](https://gnss.git-pages.gfz-potsdam.de/gfzrnx/) | GFZRNX 2.2 用户手册：任务、EULA 与 Hatanaka/统计等操作说明 | docs | — | 🏷️ 官方 |

### 详细说明

#### [uNavTools](https://github.com/IvAn190/uNavTools)  
*🏷️ 个人社区*

语言：Python · 许可：— · 星标约：10 · 宿主：github

命令行工具把 u-blox 原始数据转到 RINEX，并借助 CSSRlib 提供 RTK/PPP 模块，适合低成本板卡到开放增强服务的试验链。工程联调与教学友好。完好性、多频模糊度固定与测地级产品化仍弱于 PRIDE/Ginan/MRTKLIB。

#### [GFZRNX](https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox)  
*🏷️ 官方*

语言：binary toolkit · 许可：proprietary-freeware · 星标约：— · 宿主：official_site

德国地学研究中心 GNSS 工具箱，覆盖观测/导航/气象 RINEX 的检查、修复、抽样、系统选择、拼接拆分与元数据统计。非开源；科研与教育非例行用途可免费申请，例行生产需商业许可。下载入口在 gnss.gfz.de。常与 Anubis、RNXCMP 搭配构成数据中心流水线。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [GFZRNX-UserGuide](https://gnss.git-pages.gfz-potsdam.de/gfzrnx/)  
*🏷️ 官方*

语言：docs · 许可：proprietary-freeware (see EULA) · 星标约：— · 宿主：official_site

GFZ 官方用户指南，详述 RINEX 2/3/4 检查、拼接、抽样、元数据与 Hatanaka 相关操作，并区分科研免费与商业许可。配合 gfzrnx 下载页使用。不是开源源码文档，但对正确理解闭源工具箱能力边界与 EULA 非常关键。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## Galileo HAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [HASlib](https://github.com/nlsfi/HASlib) | 芬兰国家土地测量局开源 Galileo HAS 解码库（SBF/BINEX→SSR） | Python | 65 | 🏷️ 官方 核心 |
| [GHASP-HAS-decoding](https://github.com/borioda/HAS-decoding) | Galileo HAS 解析器 GHASP：E6B 二进制流转 CSV 轨道钟差等改正 | Python | 20 | 🏷️ 个人社区 |

### 详细说明

#### [HASlib](https://github.com/nlsfi/HASlib)  
*🏷️ 官方 核心*

语言：Python · 许可：EUPL-1.2 · 星标约：65 · 宿主：github

NLS/FGI（nlsfi）维护的 Galileo High Accuracy Service 解码库，支持从 Septentrio SBF、BINEX 等输入提取 HAS 改正并输出 IGS/RTCM SSR 等格式，提供库与 CLI。适合把免费 E6-B HAS 改正接入自研 PPP。许可 EUPL-1.2；注意与 RTKLIB 系 HASPPP/MRTKLIB 的能力重叠，按输入格式选型。

#### [GHASP-HAS-decoding](https://github.com/borioda/HAS-decoding)  
*🏷️ 个人社区*

语言：Python · 许可：see upstream README · 星标约：20 · 宿主：github

社区 Python 工具将接收机记录的 E6B/HAS 相关二进制流转为四类 CSV 改正，便于科研语言加载与 PPP 试验。面向解析与分析而非完整定位引擎。更新节奏与许可条款以仓库为准；生产接入可对照官方 HASlib 或嵌入式 HASPPP。

## 处理/教学

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gLAB](https://github.com/valgur/gLAB) | gLAB 非官方镜像；官方发行见 UPC gAGE 下载页 | C | 22 | 🏷️ 个人社区 ★ |

### 详细说明

#### [gLAB](https://github.com/valgur/gLAB)  
*🏷️ 个人社区 ★*

语言：C · 许可：— · 星标约：22 · 宿主：github

社区维护的 gLAB git 镜像，便于版本跟踪；官方二进制/源码与许可以 UPC gAGE 页面为准（本目录另收 gLAB-UPC）。核心 Apache、GUI LGPL。不要把镜像当作唯一权威来源。

## 元数据/SDR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS-Metadata-Standard](https://github.com/IonMetadataWorkingGroup/GNSS-Metadata-Standard) | GNSS 软件接收机元数据标准与工具 | C++ | 59 | 🏷️ 个人社区 |

### 详细说明

#### [GNSS-Metadata-Standard](https://github.com/IonMetadataWorkingGroup/GNSS-Metadata-Standard)  
*🏷️ 个人社区*

语言：C++ · 许可：LGPL-3.0 · 星标约：59 · 宿主：github

定义 SDR/原始采样元数据标准并提供工具，便于交换 IQ 与前端配置。做 GNSS-SDR 或自研接收机时很有用。与 RINEX 观测生态互补而非替代。

## 多路径/QC

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software) | GNSS 观测多路径分析 Python 软件 | Python | 141 | 🏷️ 个人社区 核心 |
| [MAPS](https://github.com/GCCLib/MAPS) | MATLAB GNSS 多路径分析软件 | MATLAB | 35 | 🏷️ 个人社区 |
| [gnss-multipath-detector](https://github.com/EvgeniiMunin/gnss-multipath-detector) | GPS L1 C/A 多路径异常检测模型 | Jupyter Notebook | 28 | 🏷️ 个人社区 |
| [PyRINEX](https://github.com/geumjin99/PyRINEX) | 多用途 Python RINEX 读写与质量分析包 | Python | 16 | 🏷️ 高校实验室 |
| [geoveil-mp](https://github.com/miluta7/geoveil-mp) | Rust/Python：RINEX 逐码多路径 MP 组合、周跳检测与 SNR 序列导出 | Rust | 0 | 🏷️ 个人社区 |

### 详细说明

#### [GNSS_Multipath_Analysis_Software](https://github.com/paarnes/GNSS_Multipath_Analysis_Software)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：141 · 宿主：github

专门分析 GNSS 观测多路径的开源软件，出图与指标适合论文与天线环境评估。适合选址与天线测试。不替代定位引擎；周跳修复见其他工具。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [MAPS](https://github.com/GCCLib/MAPS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：35 · 宿主：github

MATLAB 下的多路径分析开源实现，方便已有 MATLAB 流水线的实验室。与 paarnes 的 Python 软件可对照指标定义。

#### [gnss-multipath-detector](https://github.com/EvgeniiMunin/gnss-multipath-detector)  
*🏷️ 个人社区*

语言：Jupyter Notebook · 许可：— · 星标约：28 · 宿主：github

用数据驱动方法探测 GPS L1 C/A 多路径异常，偏研究 notebook。适合探索 ML+GNSS 质量控。生产嵌入需重做工程化。

#### [PyRINEX](https://github.com/geumjin99/PyRINEX)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：16 · 宿主：github

面向 RINEX 2/3 的 Python 包，支持批处理、多路径与周跳等质量相关分析，可作为 TEQC/Anubis 之外的脚本化 QC 选项。适合自动化质控流水线。指标定义与报告格式因版本而异，正式归档前请与 Anubis/GFZRNX 交叉核对。

#### [geoveil-mp](https://github.com/miluta7/geoveil-mp)  
*🏷️ 个人社区*

语言：Rust · 许可：MIT · 星标约：0 · 宿主：github

面向连续站质控的多路径分析库（Anubis/TEQC 思路），对每个伪距码做 MP 线性组合、弧段去模糊、间隔自适应周跳检测，并导出 SNR。MIT，PyPI 预编译轮。适合长时序台站多路径趋势监控；本身不做精密定位，需配合 SP3 才有高度角加权统计。

## 基础库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyubx2](https://github.com/semuconsulting/pyubx2) | u-blox UBX 协议的 Python 编解码库 | Python | 254 | 🏷️ 个人社区 |
| [gnsstk](https://github.com/SGL-UT/gnsstk) | 原 GPSTk 演进来的 C++ GNSS 基础库 | C++ | 183 | 🏷️ 高校实验室 核心 |
| [pynmeagps](https://github.com/semuconsulting/pynmeagps) | 解析/生成 NMEA 0183 语句的 Python 库，与 pyubx2 同系 | Python | 106 | 🏷️ 个人社区 核心 |
| [gnss-protos](https://github.com/nav-solutions/gnss-protos) | GNSS 广播协议编解码的 Rust 库 | Rust | 4 | 🏷️ 个人社区 |

### 详细说明

#### [pyubx2](https://github.com/semuconsulting/pyubx2)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：254 · 宿主：github

纯 Python 解析与生成 UBX 消息，覆盖配置、原始观测与导航输出，是连接 F9P 等模块的常用积木。嵌入式上位机、自动化测试与数据记录脚本都会用到。不处理 NMEA/RTCM（见 pygnssutils/pyrtcm），也不做定位滤波；若只要串口读星历伪距，它比完整 GUI 更轻，也比直接啃厂商二进制协议省事。

#### [gnsstk](https://github.com/SGL-UT/gnsstk)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：— · 星标约：183 · 宿主：github

德州大学 SGL 的 GNSSTK 库（GPSTk 后继），提供时间系统、坐标、观测模型等底层能力，配套 gnsstk-apps。适合做 C++ 科研软件底座。应用层 PPP/RTK 需自行或接 apps；老文档仍可能写 GPSTk。

#### [pynmeagps](https://github.com/semuconsulting/pynmeagps)  
*🏷️ 个人社区 核心*

语言：Python · 许可：BSD-3-Clause · 星标约：106 · 宿主：github

semuconsulting 协议栈中专责 NMEA 0183 解析与生成的 Python 库，常与 PyGPSClient、pyubx2、pyrtcm 组合使用。适合日志解析、测试桩、桌面监控与自动化脚本。不做精密定位解算；字段完整性随接收机方言与专有语句变化，遇到厂商扩展语句时需要自行补充定义再解析。

#### [gnss-protos](https://github.com/nav-solutions/gnss-protos)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：4 · 宿主：github

集中处理多种 GNSS 广播与传输相关协议编解码的 Rust 库，为 rinex、rtk、ntrip 等 crate 提供底座。适合需要强类型与高性能 IO 的开发者。上层定位/质检算法需另接；协议覆盖范围随版本扩展，集成时建议锁定 crate 版本并跑官方样例报文。

## IGS产品下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSommelier](https://github.com/EarthScope/GNSSommelier) | EarthScope 的 IGS 产品发现与下载平台（多分析中心 SP3/CLK/BIAS 等） | Python | 14 | 🏷️ 官方 |

### 详细说明

#### [GNSSommelier](https://github.com/EarthScope/GNSSommelier)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：14 · 宿主：github

EarthScope 开源的 GNSS 产品联邦工具，按日期与任务在十余个 IGS 分析中心间解析依赖并下载解压 SP3/CLK/BIAS/ERP/IONEX/ATX 等，附 CLI 与可选 PRIDE-PPPAR 流水线封装。解决 PPP 辅助产品分散与命名差异。需网络可达各 AC；与已收录的 EarthScope gnsstools（格式/流）互补。

## RINEX/工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsspy](https://github.com/GNSSpy-Project/gnsspy) | Python GNSS 数据工具包 | Python | 209 | 🏷️ 个人社区 ★ |

### 详细说明

#### [gnsspy](https://github.com/GNSSpy-Project/gnsspy)  
*🏷️ 个人社区 ★*

语言：Python · 许可：MIT · 星标约：209 · 宿主：github

面向 GNSS 观测处理的 Python 工具包，读数据、做基础分析较方便。适合教学与中小脚本。功能深度不及 gnsstk/Ginan；精密定位请接专用引擎。

## 基础库应用

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstk-apps](https://github.com/SGL-UT/gnsstk-apps) | GNSSTK 配套应用程序集 | — | 68 | 🏷️ 高校实验室 |

### 详细说明

#### [gnsstk-apps](https://github.com/SGL-UT/gnsstk-apps)  
*🏷️ 高校实验室*

语言：— · 许可：— · 星标约：68 · 宿主：github

从原 GPSTk 拆出的应用程序仓库，提供基于 gnsstk 的命令行工具。适合不想从零写 C++ 调用的用户。与现代 Python 工具链相比部署偏重。

## RINEX/SP3

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnsstools](https://github.com/arthurdjn/gnsstools) | Python 读 RINEX/SP3 与轨道改正工具 | Python | 39 | 🏷️ 个人社区 |

### 详细说明

#### [gnsstools](https://github.com/arthurdjn/gnsstools)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：39 · 宿主：github

读 RINEX、SP3 等并做轨道相关处理的小工具集。适合脚本原型。大规模生产建议 georinex + 专业定位引擎。

## Android原始观测

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gps-measurement-tools](https://github.com/google/gps-measurement-tools) | Google GNSS Logger 与桌面分析套件 | Java | 841 | 🏷️ 官方 核心 |

### 详细说明

#### [gps-measurement-tools](https://github.com/google/gps-measurement-tools)  
*🏷️ 官方 核心*

语言：Java · 许可：Apache-2.0 · 星标约：841 · 宿主：github

Android 原始 GNSS 测量日志与桌面可视化分析工具，智能手机高精度研究几乎必用。Logger 官方维护状态有变化，常与 GPSTest 日志互通。不是全星座科研 PPP 引擎。

## 接收机接口

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gpsd](https://gitlab.com/gpsd/gpsd) | 跨平台 gpsd：把 GNSS/AIS 接收机协议统一成客户端易用接口 | C | 104 | 🏷️ 个人社区 |
| [gpsd-website](https://gpsd.io/) | gpsd 项目官网：文档、兼容接收机列表与发行说明 | C | — | 🏷️ 个人社区 |

### 详细说明

#### [gpsd](https://gitlab.com/gpsd/gpsd)  
*🏷️ 个人社区*

语言：C · 许可：BSD · 星标约：104 · 宿主：gitlab

长期维护的用户态守护进程，监听串口/USB 上的 NMEA 或厂商二进制，向客户端（默认 2947）提供统一位置/时间服务。发行包见 Savannah/官网 gpsd.io；GitLab 为开发主仓。适合嵌入式与桌面集成取位，不是精密载波相位或科研 PPP 引擎。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

#### [gpsd-website](https://gpsd.io/)  
*🏷️ 个人社区*

语言：C · 许可：BSD · 星标约：— · 宿主：other

gpsd 社区官网，提供安装文档、兼容硬件列表与发布信息。源码开发主仓在 GitLab，发行文件指向 Savannah 镜像。嵌入式或桌面定位服务集成前，建议先读本站兼容性说明，避免误用标签页上的非发行压缩包。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。使用前请核验上游页面与许可条款。

## 基础库(归档)

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GPSTk](https://github.com/SGL-UT/GPSTk) | GPSTk 归档库（请改用 GNSSTK） | C++ | 360 | 🏷️ 高校实验室 |

### 详细说明

#### [GPSTk](https://github.com/SGL-UT/GPSTk)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：360 · 宿主：github

历史 GPSTk 仓库，已声明归档并迁移到 gnsstk / gnsstk-apps。仅作文献与旧脚本对照；新项目请用 GNSSTK。

## ROS NTRIP客户端

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ntrip_client-MicroStrain](https://github.com/LORD-MicroStrain/ntrip_client) | LORD MicroStrain 开源 ROS/ROS2 NTRIP 客户端（收 RTCM，支持网络/VRS） | Python | 118 | 🏷️ 个人社区 |

### 详细说明

#### [ntrip_client-MicroStrain](https://github.com/LORD-MicroStrain/ntrip_client)  
*🏷️ 个人社区*

语言：Python · 许可：NOASSERTION · 星标约：118 · 宿主：github

工业传感器厂商开源的 ROS 节点：连接 NTRIP caster，接收 RTCM 并发布到话题；可通过订阅 NMEA 支持网络 RTK/VRS。分 ros 与 ros2 分支。适合机器人与车载紧耦合前的差分链路。依赖 ROS 工作区；非通用桌面 NTRIP 客户端，许可条款以仓库为准。

## RINEX转换

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rtcm3torinex](http://software.rtcm-ntrip.org/wiki/rtcm3torinex) | BKG rtcm3torinex：RTCM3 流转 RINEX 的官方小工具 | C | 65 | 🏷️ 官方 |
| [prx](https://github.com/jtec/prx) | RINEX 3.05 观测转 CSV | Python | 23 | 🏷️ 个人社区 |
| [ubx2rinex](https://github.com/nav-solutions/ubx2rinex) | Rust 实现的 u-blox 原始观测到 RINEX 转换/采集工具 | Rust | 12 | 🏷️ 个人社区 |

### 详细说明

#### [rtcm3torinex](http://software.rtcm-ntrip.org/wiki/rtcm3torinex)  
*🏷️ 官方*

语言：C · 许可：GPL · 星标约：65 · 宿主：official_site

RTCM-Ntrip 项目提供的 RTCM 3 到 RINEX 转换工具，便于把实时流转成事后文件。说明与附件见官方 wiki。功能聚焦转换；质检与编辑需搭配 Anubis/GFZRNX 等。

#### [prx](https://github.com/jtec/prx)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：23 · 宿主：github

把 RINEX 3.05 观测文件转成 CSV，便于表格软件或简单脚本分析。适合快速查看。高精度批处理与多格式支持不如 georinex。

#### [ubx2rinex](https://github.com/nav-solutions/ubx2rinex)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：12 · 宿主：github

Rust 实现的 u-blox UBX 原始观测反序列化与 RINEX 采集工具，方便把低成本板卡数据送进经典后处理软件。适合外场脚本化采集与自动化。与 android_rinex、georinex 互补；天线高、观测码映射与时钟处理要按接收机配置核对，转换后建议跑质检工具。

## 掩星/CDAAC解析

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pysatCDAAC](https://github.com/pysat/pysatCDAAC) | pysat 生态的 CDAAC/COSMIC 仪器插件（含 ionPhs 等标签） | Python | 3 | 🏷️ 高校实验室 |

### 详细说明

#### [pysatCDAAC](https://github.com/pysat/pysatCDAAC)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：3 · 宿主：github

把 UCAR CDAAC GNSS-RO 产品接到 pysat 数据管理框架，文档与代码中列出 ionphs（电离层 excess phase）、podtec、scnLv1 等标签。适合已在用 pysat 做近地空间数据融合、又想顺手读 COSMIC 掩星文件的人。部分标签加载限制需对照 README；不是独立的 Abel 反演引擎。

## RINEX头编辑/重命名

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rinexmod](https://github.com/IPGP/rinexmod) | IPGP 批量修改 RINEX 头信息与长/短文件名（支持 Hatanaka 与 RINEX 2/3/4） | Python | 11 | 🏷️ 高校实验室 |

### 详细说明

#### [rinexmod](https://github.com/IPGP/rinexmod)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：11 · 宿主：github

与 autorino 配套的元数据工具：批量改头、按站码重命名、支持压缩/非压缩及长短文件名约定，元数据可来自 sitelog、GeodesyML 或命令行。提供 PyPI 安装与 teqc+meta 类头信息速查辅助。专攻头文件与命名规范化，不做观测质量检核或定位。

## NTRIP/实时流转发

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RTStreamHub](https://github.com/ZhangRunzhi20/RTStreamHub) | 无界面 GNSS 实时流转发枢纽（基于 RTKLIB，支持 NTRIP TLS） | C | 14 | 🏷️ 个人社区 |

### 详细说明

#### [RTStreamHub](https://github.com/ZhangRunzhi20/RTStreamHub)  
*🏷️ 个人社区*

语言：C · 许可：GPL-3.0 · 星标约：14 · 宿主：github

面向 Linux 服务器的无头 C/C++ 流转发与缓存工具，在 RTKLIB 基础上增强 NTRIP（含 TLS）接收/推送，适合台站 DTU→Caster 或产品流分发试验。强调保密传输场景下的用户侧接入。部署与证书配置需运维自理；完整 PPP 引擎仍依赖上游 RTKLIB 或其他解算软件。

## 接收机驱动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [septentrio_gnss_driver](https://github.com/septentrio-gnss/septentrio_gnss_driver) | Septentrio GNSS/INS 的 ROS1/ROS2 驱动 | C++ | 133 | 🏷️ 官方 |

### 详细说明

#### [septentrio_gnss_driver](https://github.com/septentrio-gnss/septentrio_gnss_driver)  
*🏷️ 官方*

语言：C++ · 许可：BSD-3-Clause · 星标约：133 · 宿主：github

把 Septentrio 接收机接入机器人操作系统，发布导航与观测话题，便于车载/无人机平台联调。输入为网口/串口 SBF；输出为 ROS 话题。局限：面向机器人集成而非电离层专题处理；闪烁/ISMR 需另接解析模块。

## SP3/轨道钟差格式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [sp3](https://github.com/nav-solutions/sp3) | Rust 高精度 SP3 精密轨道/钟差文件解析、分析与写出库 | Rust | 7 | 🏷️ 个人社区 |

### 详细说明

#### [sp3](https://github.com/nav-solutions/sp3)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：7 · 宿主：github

nav-solutions 生态的 SP3 crate，按 IGS 精密轨道格式做解析、分析与生产写出，与同组织 rinex/ionex 等库配套。适合 Rust 流水线接入精密产品。覆盖以 SP3 为主；完整 CLK/Bias-SINEX 工作流仍需其他库或上游产品工具。

## 预处理索引

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UNAVCO-Preprocessing](https://www.unavco.org/software/data-processing/preprocessing/preprocessing.html) | UNAVCO/GAGE GNSS 预处理工具索引（Hatanaka、GNSSTK、厂商转换等） | various | — | 🏷️ 官方 |

### 详细说明

#### [UNAVCO-Preprocessing](https://www.unavco.org/software/data-processing/preprocessing/preprocessing.html)  
*🏷️ 官方*

语言：various · 许可：varies · 星标约：— · 宿主：official_site

机构整理的 GNSS 预处理工具列表，链到 Hatanaka/RNXCMP、GNSSTK、厂商翻译器与部分历史 QC 工具。本身不是单一软件包，而是权威导航页。下载各工具仍须遵守原作者许可；其中 teqc 已宣布 EOL，仅保留终版二进制。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## RINEX/SP3/格式

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [doris-rinex](https://github.com/nav-solutions/doris) | Rust DORIS RINEX 解析库 | Rust | 3 | 🏷️ 个人社区 |

### 详细说明

#### [doris-rinex](https://github.com/nav-solutions/doris)  
*🏷️ 个人社区*

语言：Rust · 许可：MPL-2.0 · 星标约：3 · 宿主：github

nav-solutions 生态下的 DORIS RINEX 解析 crate（MPL-2.0），把多普勒定轨相关观测读进 Rust 工具链。适合做 DORIS/GNSS 联合或格式研究。覆盖范围以 DORIS RINEX 为主，不是通用 GNSS OBS 解析器；通用 RINEX 请看同组织 rinex 库。

## 下载与质检

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cddis-highrate-downloader](https://github.com/cemalialtuntas/cddis-highrate-downloader) | 批量下载 CDDIS 高采样 GNSS 数据 | Python | 14 | 🏷️ 个人社区 核心 |

### 详细说明

#### [cddis-highrate-downloader](https://github.com/cemalialtuntas/cddis-highrate-downloader)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：14 · 宿主：github

面向 NASA CDDIS 高采样（high-rate）GNSS 归档的 Python 批量下载器，减轻按站/按日手工翻目录的负担。适合闪烁、地震同震、高动态轨迹等需要 1 Hz 以上观测的研究。使用前需 Earthdata 账号与授权；请限速、遵守 NASA 条款，并核对长文件名与校验。

## 接收机协议

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [libsbp](https://github.com/swift-nav/libsbp) | Swift SBP 协议多语言客户端库 | C++ | 76 | 🏷️ 个人社区 核心 |
| [ubx-mga-rinex-ephemeris](https://github.com/jkivilin/ubx-mga-gnss-rinex-ephemeris-converter) | RINEX 导航→u-blox UBX-MGA 辅助星历 | Python | 6 | 🏷️ 个人社区 |

### 详细说明

#### [libsbp](https://github.com/swift-nav/libsbp)  
*🏷️ 个人社区 核心*

语言：C++ · 许可：MIT · 星标约：76 · 宿主：github

Swift Navigation 官方 Swift Binary Protocol（SBP）客户端库集合，覆盖 C/C++ 等绑定，用于与 Piksi/相关硬件交换观测、导航与配置消息。做低成本 RTK 硬件联调或自研记录器时常用。它是协议栈而非完整 PPP/RTK 引擎；解算仍需 RTKLIB/厂商固件或其他库。

#### [ubx-mga-rinex-ephemeris](https://github.com/jkivilin/ubx-mga-gnss-rinex-ephemeris-converter)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：6 · 宿主：github

把 RINEX 导航文件转为 u-blox 8/M8 的 UBX-MGA 星历消息（MIT，Python），覆盖 GPS/QZSS/GLONASS，并附串口注入工具以加速冷启动。适合无网络 AGNSS 或实验室灌星。不解析观测值、不做定位；芯片固件与 MGA 版本需与目标模块匹配。

## 数据接口

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk) | EarthScope 官方 Python SDK（GAGE GNSS API） | Python | 4 | 🏷️ 官方 |

### 详细说明

#### [earthscope-sdk](https://gitlab.com/earthscope/public/earthscope-sdk)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：4 · 宿主：gitlab

EarthScope 发布的 Python 客户端（Apache-2.0，PyPI: earthscope-sdk），统一鉴权后可拉取 GNSS 观测、星历位置等 API 数据，支持同步/异步与 Arrow 加速。适合脚本化获取 NSF GAGE 归档而不必整站下载 RINEX。需 EarthScope 账号/令牌；接口配额与切片窗口以文档为准，和已收录的 gnsstools Go 库互补。

## 产品读写

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssanalysis](https://github.com/GeoscienceAustralia/gnssanalysis) | GA 官方 Python：SINEX/SP3/CLK/Bias 产品工具箱 | Python | 43 | 🏷️ 官方 |

### 详细说明

#### [gnssanalysis](https://github.com/GeoscienceAustralia/gnssanalysis)  
*🏷️ 官方*

语言：Python · 许可：Apache-2.0 · 星标约：43 · 宿主：github

澳大利亚地球科学局开源的 Python 模块（Apache-2.0，pip 可装），覆盖 SINEX、SP3、CLK、IONEX、BSX/BIA、ERP、RINEX、TROP 等产品读写，并附 diffutil、sp3merge、snxmap、orbq 等命令行。面向 Ginan/IGS 产品质检与合并。不是定位引擎；大文件性能与格式边角需对照上游变更日志。

## 数据下载

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_OSI_download](https://github.com/jdesbonnet/GNSS_OSI_download) | 爱尔兰 OSI/Tailte GNSS 网 RINEX 下载脚本 | Python | 1 | 🏷️ 个人社区 |

### 详细说明

#### [GNSS_OSI_download](https://github.com/jdesbonnet/GNSS_OSI_download)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：1 · 宿主：github

MIT 许可的 Python 脚本，从 gnss.osi.ie 批量下载爱尔兰 Active GNSS 站 RINEX（ZIP），可列站号并按日期/小时段抓取。填补西欧岛屿 CORS 自动化缺口。使用前须同意站点条款；公开窗口常约近 30 天。门户偶发网络可达性问题，失败时核对站点状态。
