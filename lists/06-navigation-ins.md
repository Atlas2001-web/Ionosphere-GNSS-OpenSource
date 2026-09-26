# 导航 / Navigation & INS
> **72** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

## ROS驱动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ublox-ros](https://github.com/KumarRobotics/ublox) | ublox-ros：KumarRobotics ROS1 经典 u-blox GPS 驱动 | C++ | 537 | 🏷️ 高校实验室 |
| [nmea_navsat_driver](https://github.com/ros-drivers/nmea_navsat_driver) | nmea_navsat_driver：ROS NMEA→NavSatFix 通用驱动 | Python | 287 | 🏷️ 个人社区 |
| [novatel_gps_driver](https://github.com/swri-robotics/novatel_gps_driver) | novatel_gps_driver：SWRI 社区 NovAtel GNSS ROS 驱动（BSD-3） | C++ | 175 | 🏷️ 个人社区 |
| [ublox_driver](https://github.com/HKUST-Aerial-Robotics/ublox_driver) | ublox_driver：ZED-F9P 向 ROS u-blox 驱动 | C++ | 159 | 🏷️ 高校实验室 |
| [novatel_oem7_driver](https://github.com/novatel/novatel_oem7_driver) | novatel_oem7_driver：NovAtel OEM7/SPAN 厂商 ROS 驱动（MIT） | C++ | 123 | 🏷️ 个人社区 |
| [rtklib_ros_bridge](https://github.com/MapIV/rtklib_ros_bridge) | rtklib_ros_bridge：RTKLIB 结果桥接 ROS | C++ | 121 | 🏷️ 个人社区 |
| [fixposition_driver](https://github.com/fixposition/fixposition_driver) | fixposition_driver：Vision-RTK/PBx 视觉惯性 GNSS 的 ROS 驱动 | C++ | 66 | 🏷️ 个人社区 |
| [nmea-msgs](https://github.com/ros-drivers/nmea_msgs) | nmea_msgs：ROS 用 NMEA 消息接口（ros-drivers） | CMake | 38 | 🏷️ 个人社区 |
| [gnss_ros_standardization](https://github.com/DaikiNiimi/gnss_ros_standardization) | gnss_ros_standardization：ROS 2 标准化 GNSS 话题 | C++ | 21 | 🏷️ 个人社区 |
| [swiftnav-ros2](https://github.com/swift-nav/swiftnav-ros2) | swiftnav-ros2：Swift Navigation 厂商 ROS 2 SBP 驱动（MIT） | C++ | 15 | 🏷️ 个人社区 |
| [UnicoreDriver](https://github.com/zltan-whu/UnicoreDriver) | 基于官方协议实现的和芯星通 UM982/UM980 ROS 驱动（C++） | C++ | 11 | 🏷️ 个人社区 |
| [trimble_driver_ros](https://github.com/trimble-oss/trimble_driver_ros) | Trimble 厂商开源 ROS/ROS 2 驱动：解析 GSOF 输出并发布标准与自定义话题 | C++ | 10 | 🏷️ 个人社区 |

### 详细说明

#### [ublox-ros](https://github.com/KumarRobotics/ublox)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：537 · 宿主：github

KumarRobotics 维护的 ROS 驱动，解析 u-blox 接收机消息并发布导航/传感器话题，BSD-3-Clause，社区星数高。面向机器人定位栈，而非测地后处理。消息集与固件版本需匹配；ROS2 场景可另评 ublox_dgnss 等。目录名 ublox-ros 以免与其他 ublox 条目混淆。

#### [nmea_navsat_driver](https://github.com/ros-drivers/nmea_navsat_driver)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：287 · 宿主：github

ros-drivers 组织下的 NMEA 卫星导航设备驱动，将 GGA/RMC 等语句转为 ROS NavSatFix 等消息，BSD-3-Clause。适合通用 NMEA 接收机接入，不解析 UBX 私有协议。串口配置与语句选择影响延迟与完整性。与厂商专用驱动互补。

#### [novatel_gps_driver](https://github.com/swri-robotics/novatel_gps_driver)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：175 · 宿主：github

Southwest Research Institute 维护的 NovAtel GPS/GNSS ROS 驱动，BSD-3-Clause，在移动机器人与自动驾驶栈中使用较广。偏消息解析与话题发布，不替代 NovAtel 厂商新版 OEM7 驱动的全部能力。串口/以太网连接与最佳实践见仓库文档。适合 ROS1 时代工程对照；新项目可并行评估 NovAtel 厂商 OEM7 驱动。

#### [ublox_driver](https://github.com/HKUST-Aerial-Robotics/ublox_driver)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：159 · 宿主：github

为机器人实验提供的 u-blox（尤其 ZED-F9P）ROS 驱动，输出与 gnss_comm/GVINS 衔接的原始测量与定位话题。适合搭车载或无人机 GNSS-视觉实验台。不是通用多厂商驱动，也不替代测地接收机网管软件；配置、波特率与固件版本需按仓库说明核对，和官方 u-center 联调可减少踩坑。

#### [novatel_oem7_driver](https://github.com/novatel/novatel_oem7_driver)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：123 · 宿主：github

Hexagon/NovAtel 维护的 OEM7 系列 GNSS/SPAN 厂商 ROS 驱动，MIT 许可，支持定位、原始观测与惯导相关话题发布。面向车载/机器人集成，而非测地后处理套件。消息定义与固件版本需匹配；多天线/SPAN 配置依赖硬件与校准。与社区旧版 novatel_gps_driver 并存时注意选型。

#### [rtklib_ros_bridge](https://github.com/MapIV/rtklib_ros_bridge)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：121 · 宿主：github

把经典 RTKLIB 定位输出接入 ROS，便于自动驾驶与机器人栈消费 RTK/PPP 结果。绑定 RTKLIB 2.4.3 b34 一代接口。适合已有 RTKLIB 流水线的 ROS 集成；若需要更新算法内核应另选维护中的 RTKLIB 分支或 MRTKLIB，并注意许可与版本差异。

#### [fixposition_driver](https://github.com/fixposition/fixposition_driver)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：66 · 宿主：github

Fixposition 厂商 Linux ROS 驱动，对接 Vision-RTK 2、PBx-A1 等视觉惯性 GNSS 定位传感器，MIT 许可。面向机器人/自动驾驶紧组合定位话题，而非测地后处理。依赖厂商硬件与时间同步配置；与纯 GNSS RTK 方案选型不同。适合评估视觉辅助 RTK 的 ROS 集成。

#### [nmea-msgs](https://github.com/ros-drivers/nmea_msgs)  
*🏷️ 个人社区*

语言：CMake · 许可：BSD (package.xml; clause variant unspecified) · 星标约：38 · 宿主：github

ros-drivers 组织维护的 nmea_msgs，定义与 NMEA 相关的 ROS 消息，方便驱动、导航与录包节点交换 GNSS 语句。适合机器人接入 GNSS 接收机。只提供消息契约，不含语句解析与 PVT；解析需另接驱动或 nmea_navsat_driver 一类包。

#### [gnss_ros_standardization](https://github.com/DaikiNiimi/gnss_ros_standardization)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：21 · 宿主：github

统一多品牌接收机原始观测与星历到 ROS 2 标准话题，降低紧组合与多传感器融合的驱动碎片化，含 RTK 演示配置说明。目标是一次开发、多机复用。侧重接口与消息层而非完整 PPP 引擎；具体消息定义、驱动覆盖与硬件接线以仓库文档和演示配置为准。

#### [swiftnav-ros2](https://github.com/swift-nav/swiftnav-ros2)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：15 · 宿主：github

Swift Navigation 厂商 ROS 2 驱动，通过 Swift Binary Protocol（SBP）接入其 GNSS/INS 接收机，MIT 许可。与 libsbp、piksi_tools 等同栈，面向机器人实时定位话题。固件与 SBP 版本需匹配；不覆盖非 Swift 品牌接收机。适合 ROS 2 车载/机器人集成评估。

#### [UnicoreDriver](https://github.com/zltan-whu/UnicoreDriver)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：11 · 宿主：github

开发者 Zhiliang Tan（账号名带 whu）发布的 ROS Noetic 驱动，GPL-3.0 许可，C++ 实现，依赖 Boost（CMake 要求 Eigen3，但源码未用到）。依据和芯星通 UM982 官方协议开发，在 UM982 与 UM980 上测试；需用 UPrecise 配置接收机输出 BESTNAVXYZB，驱动经串口读取并发布 nav_msgs/Odometry 话题，launch 文件支持多台接收机分命名空间接入，并可配置 NTRIP 获取 RTK 固定解。适合在组合导航或多传感器平台中接入国产 RTK 板卡。仓库 2025 年一次性发布，后续更新较少。

#### [trimble_driver_ros](https://github.com/trimble-oss/trimble_driver_ros)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-2-Clause · 星标约：10 · 宿主：github

Trimble 公司 trimble-oss 组织发布的 ROS 2 软件包，BSD-2-Clause 许可，C++ 实现。解析 Trimble General Serial Output Format（GSOF）的一个子集，可选发布 sensor_msgs/NavSatFix 与 nav_msgs/Odometry 等标准消息（以 GSOF49 首个位置或 set_origin 服务设定的原点构建局部切平面），同时提供专用 GSOF 话题；主要在 Applanix 组合导航产品上测试。适合在自动驾驶、移动测绘平台中接入 Trimble/Applanix 定位定姿系统。README 详列节点参数、话题与服务。

## 多传感器融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Multi_Sensor_Fusion](https://github.com/2013fangwentao/Multi_Sensor_Fusion) | Multi_Sensor_Fusion：GNSS/IMU/视觉多源融合 | C++ | 940 | 🏷️ 高校实验室 核心 |
| [MINS](https://github.com/rpng/MINS) | MINS：RPNG 多传感器（含 GNSS）紧组合导航系统 | C++ | 779 | 🏷️ 高校实验室 |
| [GLIO](https://github.com/XikunLiu-huskit/GLIO) | GLIO：GNSS/LiDAR/IMU 紧耦合连续定位 | C | 438 | 🏷️ 高校实验室 |
| [libRSF](https://github.com/TUC-ProAut/libRSF) | libRSF：鲁棒传感器融合与在线定位库 | C++ | 337 | 🏷️ 高校实验室 |
| [syncgpslidarimucam](https://github.com/nkliuhui/sync_gps_lidar_imu_cam) | syncgpslidarimucam：多传感器硬件授时同步 | C++ | 252 | 🏷️ 个人社区 |
| [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion) | raw-gnss-fusion：原始 GNSS 多传感器融合代码与数据 | Python | 160 | 🏷️ 个人社区 |
| [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF) | GREAT-MSF：PPP/RTK+INS 多传感器融合 | C++ | 150 | 🏷️ 高校实验室 |
| [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation) | GPS_Milemeter_IMU_EKF：GPS+里程计+罗盘 EKF（MATLAB） | MATLAB | 89 | 🏷️ 个人社区 |
| [FE-GUT](https://github.com/zhaoqj23/FE-GUT) | FE-GUT：因子图+EKF 的 GNSS/UWB 紧组合 | C++ | 79 | 🏷️ 个人社区 |
| [gnssFGO](https://github.com/hz658832/gnssFGO) | RWTH 在线 GNSS/多传感器因子图定位（ROS2） | C++ | 52 | 🏷️ 高校实验室 |
| [BDS-3-PPP-B2b_IMU_LiDAR](https://github.com/xdinav/BDS-3-PPP-B2b_IMU_LiDAR) | BDS-3-PPP-B2b_IMU_LiDAR：PPP-B2b 与 IMU/LiDAR 融合试验 | — | 6 | 🏷️ 个人社区 |

### 详细说明

#### [Multi_Sensor_Fusion](https://github.com/2013fangwentao/Multi_Sensor_Fusion)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：940 · 宿主：github

中文社区高星工程仓，覆盖 GNSS、IMU、相机及 PPP/INS 紧组合思路。适合车载与机器人组合导航入门。文档偏实践；生产标定与完整性需自建流程。

#### [MINS](https://github.com/rpng/MINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：779 · 宿主：github

同一 RPNG 组发布的 MINS，在滤波框架下紧组合 IMU、相机、LiDAR、GNSS 与轮速，并支持在线外参标定与仿真评测。覆盖 VINS、GPS-INS、LIO 等多用例，文档与 ROS1/ROS2 CI 较完整。计算与传感器配置门槛较高；不是纯 GNSS PPP/RTK 引擎。

#### [GLIO](https://github.com/XikunLiu-huskit/GLIO)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：438 · 宿主：github

把 GNSS 观测拉进 LIO，强调城市连续、低漂移。适合已有激光惯性基础、想补绝对约束的团队。标定与时间同步要求高；纯开阔测地请用 PPP 引擎。

#### [libRSF](https://github.com/TUC-ProAut/libRSF)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：337 · 宿主：github

强调鲁棒核与在线估计，可接入 GNSS 与测距类观测，示例偏机器人。适合抗野值/滑窗实验。不是开箱测地 PPP 产品。

#### [syncgpslidarimucam](https://github.com/nkliuhui/sync_gps_lidar_imu_cam)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：252 · 宿主：github

给出 lidar、IMU、相机与 GPS 的时间戳硬件同步思路与参考实现，解决多传感器融合前的时钟对齐问题。适合自动驾驶与机器人传感器套件研发。解决的是同步而非状态估计；滤波/建图需另接 VINS、GICI、gtsam 等。硬件触发拓扑要比纯软件时间戳对齐更稳。线缆延时与触发极性要在示波器上核验。

#### [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion)  
*🏷️ 个人社区*

语言：Python · 许可：LGPL-3.0 · 星标约：160 · 宿主：github

ICRA 2023 论文（Beuchert、Camurri、Fallon）配套仓库：用因子图把原始 GNSS 载波相位与 IMU、激光雷达融合，不需要基准站也能在地球坐标系中做无漂移、无跳变的定位。内容分三块：基于 GTSAM 与 GPSTk 的时间相对双差载波相位因子演示脚本（输入 UBX，非实时代码）、公开机器人数据集（GNSS/IMU/lidar）使用说明、各数据集上的结果。适合研究起步与论文复现；环境停留在 Python 3.7 与 GPSTk 8，不是开箱商用导航软件。

#### [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：150 · 宿主：github

GREAT 组多传感器融合系统，支持 PPP/RTK 与 INS 等组合。适合已跟 GREAT-PVT 的用户向上集成。文档跟随版本变化。

#### [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：89 · 宿主：github

用 iPhone 的 GPS 取经纬度、电子罗盘取航向、加速度计积分代替里程计，再用 EKF 融合，流程直观。适合车载松组合入门。高精度车道级与视觉惯性请另选现代框架。

#### [FE-GUT](https://github.com/zhaoqj23/FE-GUT)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：79 · 宿主：github

混合因子图与 EKF，并开源仿真数据，便于复现时间标定实验。适合室内外衔接与 UWB 辅助研究。实网性能取决于 UWB/GNSS 标定质量。

#### [gnssFGO](https://github.com/hz658832/gnssFGO)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：52 · 宿主：github

亚琛工大 IRT 的 gnssFGO（BSD-3-Clause，ROS 2），以连续时间轨迹与因子图融合松/紧耦合 GNSS、激光/视觉里程计等，配套数据集与 Docker。原 rwth-irt 仓已归档，维护迁至本地址。适合车载多传感器研究。依赖 ROS 2 与大量子模块，工程门槛高于纯 GNSS PPP 工具。

#### [BDS-3-PPP-B2b_IMU_LiDAR](https://github.com/xdinav/BDS-3-PPP-B2b_IMU_LiDAR)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：6 · 宿主：github

把 PPP-B2b 与 IMU/LiDAR 结合的试验工程，面向高动态或遮挡场景的多传感器融合。适合看改正服务如何进组合导航。成熟度与标定流程因仓库而异，引用前请用自有数据复现关键指标。

## GNSS/INS/视觉

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [VINS-Mono](https://github.com/HKUST-Aerial-Robotics/VINS-Mono) | VINS-Mono：经典单目视觉惯性状态估计器 | C++ | 6044 | 🏷️ 高校实验室 |
| [VINS-Fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) | VINS-Fusion：港科大多传感器视觉惯性估计器 | C++ | 4728 | 🏷️ 高校实验室 |
| [OpenVINS](https://github.com/rpng/open_vins) | OpenVINS：RPNG 视觉-惯性导航开源研究平台 | C++ | 3115 | 🏷️ 高校实验室 |
| [GVINS-HKUST](https://github.com/HKUST-Aerial-Robotics/GVINS) | GVINS：港科大紧耦合 GNSS-视觉-惯性系统 | C++ | 1160 | 🏷️ 高校实验室 |
| [IC-GVINS](https://github.com/i2Nav-WHU/IC-GVINS) | IC-GVINS：INS 中心的实时 GNSS-VIO 组合导航 | C++ | 690 | 🏷️ 高校实验室 |
| [gici-open](https://github.com/chichengcn/gici-open) | GICI：GNSS/INS/相机紧组合开源库 | C++ | 667 | 🏷️ 高校实验室 核心 |
| [OKVIS2-X](https://github.com/ethz-mrl/OKVIS2-X) | OKVIS2-X：可融 GNSS 的开源视觉-惯性 SLAM | C++ | 410 | 🏷️ 高校实验室 |
| [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel) | VINS-GPS-Wheel：VINS-Mono+轮速+GNSS | C++ | 280 | 🏷️ 个人社区 |
| [gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm) | gnss_comm：ROS GNSS 原始测量消息与工具 | C++ | 164 | 🏷️ 高校实验室 |
| [RTK-Visual-Inertial-Navigation](https://github.com/xiaohong-huang/RTK-Visual-Inertial-Navigation) | RTK-VIN：滑窗滤波 RTK 视觉惯性导航 | C++ | 136 | 🏷️ 个人社区 |
| [carvig](https://github.com/Erensu/carvig) | carvig：车载 INS/GNSS/视觉组合导航 | C | 120 | 🏷️ 个人社区 |
| [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS) | msckfvioGPS：MSCKF 视觉惯性里程计与 GPS 融合 | C++ | 31 | 🏷️ 个人社区 |
| [salsa](https://github.com/yxw027/salsa) | salsa：GNSS+视觉+惯性状态估计原型 | C++ | 14 | 🏷️ 个人社区 |
| [GVINS-WHU](https://github.com/zhangwhu/GVINS) | GVINS-WHU：PPP-RTK/INS/视觉组合导航（个人仓） | C++ | 12 | 🏷️ 个人社区 |

### 详细说明

#### [VINS-Mono](https://github.com/HKUST-Aerial-Robotics/VINS-Mono)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：6044 · 宿主：github

VINS 系列奠基之作，单目视觉与 IMU 紧耦合优化估计，衍生大量 GNSS/轮速扩展（如 VINS-GPS-Wheel）。GPL-3.0，教学与二次开发引用极高。本身不含 GNSS，但是目录中 GVINS/融合工作的重要上游；部署需注意标定、曝光与回环，代码以 ROS1 生态为主。

#### [VINS-Fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：4728 · 宿主：github

HKUST Aerial Robotics 发布的优化式多传感器状态估计器，在 VINS-Mono 基础上扩展双目/立体与多传感器融合，社区常接 GNSS 作户外约束。GPL-3.0；与 OpenVINS、GVINS、IC-GVINS 形成 VIO/GVINS 谱系对照。偏机器人/无人机，非测地级 PPP；标定与时间同步要求高，文档与星标均很成熟。

#### [OpenVINS](https://github.com/rpng/open_vins)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：3115 · 宿主：github

罗切斯特理工 RPNG 组的 OpenVINS，是广泛引用的开源视觉-惯性里程计研究平台，提供 MSCKF 类滤波、在线标定与评测工具，并被后续多传感器项目复用。本身以相机+IMU 为主，GNSS 融合需看扩展或姊妹项目 MINS。ROS/非 ROS 构建均有文档；许可 GPL-3.0。

#### [GVINS-HKUST](https://github.com/HKUST-Aerial-Robotics/GVINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：1160 · 宿主：github

HKUST Aerial Robotics 把 GNSS 因子织进 VIO，改善长航时全局一致性。适合无人机与户外 SLAM。对 GNSS 原始观测质量与初始化敏感；城市峡谷仍需多路径策略。

#### [IC-GVINS](https://github.com/i2Nav-WHU/IC-GVINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：690 · 宿主：github

i2Nav 开源的 INS 中心多传感器组合，把 GNSS 与视觉约束进惯性状态，强调实时稳健。适合户外机器人与自动驾驶定位研究。标定、时间同步与数据集质量要求高；纯测地事后 PPP 请另选 PRIDE/Ginan。

#### [gici-open](https://github.com/chichengcn/gici-open)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：667 · 宿主：github

工程结构完整，支持 GNSS 精密模式与 INS/相机紧组合。适合户外机器人定位研究。编译配置较重；事后测地 PPP-AR 另选 PRIDE/Ginan。

#### [OKVIS2-X](https://github.com/ethz-mrl/OKVIS2-X)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：410 · 宿主：github

OKVIS2-X 在经典 OKVIS 视觉惯性框架上扩展稠密深度或 LiDAR，并支持融合 GNSS，面向机器人户外定位。BSD-3 风格许可，附 TRO/arXiv 论文。构建依赖较重；GNSS 为可选传感器，不是独立 PPP/RTK 引擎。

#### [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：280 · 宿主：github

在 VINS-Mono 上紧耦合轮速计、松耦合 GPS，并在 KAIST 等数据集验证，面向自动驾驶室外定位。适合已有视觉惯性栈、想加轮速与 GNSS 全局约束的团队。依赖 ROS/VINS 生态；GNSS 中断或城市峡谷时仍主要靠视觉惯性与轮速。轮速标度因数误差会在长直道上缓慢积累。数据集标定文件缺失时融合容易发散。

#### [gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：164 · 宿主：github

港科大空中机器人组为 GVINS 等项目抽出的 GNSS 消息与工具包，统一原始观测在 ROS 中的表示。做视觉惯性加 GNSS 融合时几乎都会碰到。单独使用需自备接收机驱动与解算前端；与 ublox_driver、GVINS-Dataset 同生态，测地 RINEX 流水线请另选 georinex、Anubis 等。

#### [RTK-Visual-Inertial-Navigation](https://github.com/xiaohong-huang/RTK-Visual-Inertial-Navigation)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：136 · 宿主：github

在滑窗滤波框架里融合 RTK/DGNSS 与视觉惯性，面向高精度户外机器人与自动驾驶实验。适合已有 VIO 基础、想引入载波相位差分约束的团队。测地网 RTK 服务运维与模糊度完好性监测非其主场；可与 GVINS、gici-open、Multi_Sensor_Fusion 比较紧耦合策略。外参标定质量往往比滤波形式更能决定最终精度。

#### [carvig](https://github.com/Erensu/carvig)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：120 · 宿主：github

面向车辆定位的 INS/GNSS/视觉一体化导航实现（C），把惯导、卫星与视觉观测纳入同一解算框架，服务自动驾驶或车载定位验证。适合做多传感器室外定位的工程与研究生。纯 GNSS 的 RTK/PPP 引擎深度不如 RTKLIB/PRIDE；本库价值在融合架构，文档与外场标定成本需自行评估。传感器外参与时间同步质量会直接限制融合精度。

#### [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS)  
*🏷️ 个人社区*

语言：C++ · 许可：academic non-commercial (Penn MSCKF_VIO terms, no redistribution) · 星标约：31 · 宿主：github

在 MSCKF-VIO 上增加 GPS 融合，用卫星位置约束抑制视觉惯性漂移并对齐全球坐标，服务无人机与地面机器人。适合已有 MSCKF 栈、需要全球定位的团队。与上游 MSCKF 的同步情况需自查；城市峡谷 GNSS 质量差时收益有限，精密测地仍用专用 PPP/RTK。相机-IMU 外参标定质量往往比 GPS 权重更敏感。

#### [salsa](https://github.com/yxw027/salsa)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：14 · 宿主：github

融合 GNSS、视觉与惯性的状态估计原型，用于机器人室外全局定位并抑制纯视觉惯性漂移。适合多传感器融合架构与外参标定实验。传感器时间同步与标定成本较高；纯测地精密定位不如专用 PPP/RTK 引擎，本仓库价值在融合框架设计而非载波相位解算深度。

#### [GVINS-WHU](https://github.com/zhangwhu/GVINS)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0-or-later · 星标约：12 · 宿主：github

仓库描述只有「PPP-RTK/INS/Visual」，没有 README。目录含 ic_gvins（结构同 i2Nav IC-GVINS）、gnss_comm-main（HKUST gnss_comm）与 data_to_rosbag，看名称是在其上加入 PPP-RTK。与 HKUST-Aerial-Robotics/GVINS是不同项目、不同作者；使用和引用前先读源码。

## GNSS/INS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS) | KF-GINS：基于 EKF 的 GNSS/INS 组合导航 | C++ | 1194 | 🏷️ 高校实验室 核心 |
| [imu_x_fusion](https://github.com/cggos/imu_x_fusion) | imu_x_fusion：ESKF/IEKF/UKF 族 IMU+GNSS 松组合 | C++ | 1126 | 🏷️ 个人社区 核心 |
| [eagleye](https://github.com/MapIV/eagleye) | eagleye：车载 GNSS/IMU 精密定位开源栈 | C++ | 775 | 🏷️ 个人社区 |
| [imugpslocalization](https://github.com/ydsf16/imu_gps_localization) | imu_gps_localization：ESKF 融合 IMU 与 GPS（C++） | C++ | 734 | 🏷️ 个人社区 |
| [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS) | OB_GINS：基于优化的 GNSS/INS 组合导航 | C++ | 647 | 🏷️ 高校实验室 ★ 核心 |
| [ignav](https://github.com/Erensu/ignav) | ignav：轻量 INS/GNSS 组合导航（C） | C | 472 | 🏷️ 个人社区 ★ |
| [fusioncore](https://github.com/manankharwar/fusioncore) | fusioncore：户外机器人 IMU/轮速/GPS 的 UKF 融合 | C++ | 366 | 🏷️ 个人社区 |
| [GINav](https://github.com/kaichen686/GINav) | MATLAB GNSS/INS 松紧组合常用算法实现 | MATLAB | 309 | 🏷️ 个人社区 ★ 核心 |
| [EKF_IMU_GPS](https://github.com/balamuruganky/EKF_IMU_GPS) | EKF_IMU_GPS：IMU 预测 GNSS 的 EKF 融合示例 | C++ | 212 | 🏷️ 个人社区 |
| [Loose-GNSS-IMU](https://github.com/aaronboda24/Loose-GNSS-IMU) | Loose-GNSS-IMU：经典 GNSS/IMU 松组合卡尔曼 | C++ | 187 | 🏷️ 个人社区 |
| [KF-GINS-Matlab](https://github.com/i2Nav-WHU/KF-GINS-Matlab) | KF-GINS-Matlab：EKF 松/紧组合 MATLAB 版 | MATLAB | 137 | 🏷️ 高校实验室 核心 |
| [ublox_dgnss](https://github.com/aussierobots/ublox_dgnss) | ublox_dgnss：ROS2 u-blox UBX 驱动 | C++ | 86 | 🏷️ 个人社区 |
| [GIOW-release](https://github.com/i2Nav-WHU/GIOW-release) | GIOW：GNSS/INS/ODO 轮速辅助组合导航 | C++ | 75 | 🏷️ 高校实验室 核心 |
| [GNSS_INS_Integrations_Comparisons](https://github.com/ZhengdaoLI0602/GNSS_INS_Integrations_Comparisons) | GNSS/INS 二维定位算法对比 | MATLAB | 70 | 🏷️ 高校实验室 |
| [Wheel-GINS](https://github.com/i2Nav-WHU/Wheel-GINS) | Wheel-GINS：轮式 IMU+GNSS 组合导航 | C++ | 47 | 🏷️ 高校实验室 |
| [GNSS_IMU](https://github.com/rtklibexplorer/GNSS_IMU) | GNSS_IMU：松组合 GNSS/IMU 的 Python 实现 | Python | 35 | 🏷️ 个人社区 |
| [GINS](https://github.com/zhangwhu/GINS) | GINS：PPP-RTK 与惯导组合导航实现 | C | 21 | 🏷️ 个人社区 |
| [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding) | ImuGpsGuiding：ROS 下 IMU+GPS 点到点导引示例 | C++ | 20 | 🏷️ 个人社区 |
| [KF-GINS-Py](https://github.com/salmoshu/KF-GINS-Py) | KF-GINS-Py：KF-GINS 思路的 Python EKF 移植 | Python | 13 | 🏷️ 个人社区 |
| [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station) | Smart-UAV-Return-GNSS-Station：失联/失锁时 UAV 智能返航 | C | 3 | 🏷️ 高校实验室 |

### 详细说明

#### [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：1194 · 宿主：github

经典 EKF 框架的 GNSS/INS 开源实现，文档与课程友好，星标很高。适合教学和基线实现。因子图/滑窗优化性能边界看 OB_GINS/gici。

#### [imu_x_fusion](https://github.com/cggos/imu_x_fusion)  
*🏷️ 个人社区 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：1126 · 宿主：github

同一框架里切换 ESKF、IEKF、UKF 等，公式与代码对应清晰，利于学习滤波器差异。适合课程与算法对照。工业级标定、时间同步与完整性监测需另补；纯测地 PPP 请另选专用引擎。

#### [eagleye](https://github.com/MapIV/eagleye)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：775 · 宿主：github

面向自动驾驶车辆的 GNSS/IMU 精密定位开源栈，工程案例多。适合车载 ROS 生态。测地学参考架与 PPP-AR 产品需求不同。

#### [imugpslocalization](https://github.com/ydsf16/imu_gps_localization)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：734 · 宿主：github

示例清晰的 ESKF 松组合实现，星标较高，适合第一次跑通误差状态建模。课程与原型友好。缺少完整测地产品链；高动态/遮挡需加强观测模型。

#### [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS)  
*🏷️ 高校实验室 ★ 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：647 · 宿主：github

武大 i2Nav 开源的优化型 GNSS/INS 组合，在开源组合导航里引用与星标都高。适合车载/机器人紧组合研究。纯测地 PPP-AR 不是目标；视觉相关见 IC-GVINS。

#### [ignav](https://github.com/Erensu/ignav)  
*🏷️ 个人社区 ★*

语言：C · 许可：— · 星标约：472 · 宿主：github

README 列出松组合、SPP/PPP/DGPS/RTK 紧组合、里程计/磁力计/双天线辅助和 NHC/ZUPT 约束，目前只支持 Linux 编译。功能广度不及现代因子图方案；上线前务必核对状态模型与坐标系约定。

#### [fusioncore](https://github.com/manankharwar/fusioncore)  
*🏷️ 个人社区*

语言：C++ · 许可：Apache-2.0 · 星标约：366 · 宿主：github

面向户外机器人的 23 状态 UKF，融合 IMU、轮速编码器与 GPS（亦可接视觉 SLAM），约 100 Hz，并尝试报告哪路传感器导致发散。Apache-2.0；提供无 ROS 依赖的 C++ 滤波库与 ROS 2 包。偏移动机器人定位而非测地 PPP；部署需自备外参与时间同步标定。

#### [GINav](https://github.com/kaichen686/GINav)  
*🏷️ 个人社区 ★ 核心*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：309 · 宿主：github

以 MATLAB 实现 GNSS 定位及松/紧组合常用滤波与方程，便于改模型、画残差，研究生入门友好。适合课程作业与论文原型。实时嵌入式或高吞吐现场部署需移植到 C/C++ 或其他引擎。

#### [EKF_IMU_GPS](https://github.com/balamuruganky/EKF_IMU_GPS)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：212 · 宿主：github

balamuruganky 的 C++ EKF 示例：以 IMU 传播预测 GNSS 量测，演示松组合思路。MIT 许可；与目录中 IndirectEKFIMUGPS 为不同实现。适合教学与原型验证，非工业级 INS；过程噪声、量测噪声与坐标系约定需按自有传感器重新标定。

#### [Loose-GNSS-IMU](https://github.com/aaronboda24/Loose-GNSS-IMU)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：187 · 宿主：github

C++（Eigen）松组合示例：IMU 在 ECEF 系做机械编排，GNSS 位置/速度作卡尔曼观测更新，实现参照 Groves《Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems》第 2 版，附输入样例与 ECEF/ENU、速度、姿态结果图。结构直白，适合课程实验与第一次调噪声参数。工程为 Visual Studio 2017 解决方案，2019 年后未更新；紧组合、模糊度固定与完好性监测需另寻方案。

#### [KF-GINS-Matlab](https://github.com/i2Nav-WHU/KF-GINS-Matlab)  
*🏷️ 高校实验室 核心*

语言：MATLAB · 许可：GPL-3.0 · 星标约：137 · 宿主：github

与 C++ 版 KF-GINS 对应的 MATLAB 实现，状态、观测与噪声调参过程更直观，便于课堂推导误差状态卡尔曼滤波。适合组合导航课程与算法复现。实时性能、ROS 集成与工程稳健性不如 C++ 原版；外场长航时建议回到 KF-GINS 或 OB_GINS，并把 IMU Allan 方差标定与杆臂参数补全。

#### [ublox_dgnss](https://github.com/aussierobots/ublox_dgnss)  
*🏷️ 个人社区*

语言：C++ · 许可：Apache-2.0 · 星标约：86 · 宿主：github

面向 ROS2 的 u-blox UBX USB 驱动，支持 ZED-F9P/F9R/X20P 等高精度模块，含差分与 moving-base 配置。适合机器人/车载室外定位联调。不是测地级 PPP 引擎；精密解算请外接 RTKLIB 或科研软件。

#### [GIOW-release](https://github.com/i2Nav-WHU/GIOW-release)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：— · 星标约：75 · 宿主：github

将轮速/轮角与 GNSS、INS 一并估计，面向地面车辆在遮挡路段仍保持连续定位的需求。适合自动驾驶底盘导航与园区车辆试验。传感器时间同步、轮速标度因数与轮胎滑移会显著影响结果；城市峡谷 GNSS 中断时，系统上限取决于惯导质量与里程计约束是否可信。

#### [GNSS_INS_Integrations_Comparisons](https://github.com/ZhengdaoLI0602/GNSS_INS_Integrations_Comparisons)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：70 · 宿主：github

配套 Remote Sensing 论文的 MATLAB 实验仓，对比固定增益 KF、自适应 KF、因子图及自适应因子图在 GNSS/INS 二维定位中的表现，FGO 部分参考 MathWorks 示例改造。适合算法课与论文复现。非完整车载三维产品；数据准备脚本需按 README 逐步运行。

#### [Wheel-GINS](https://github.com/i2Nav-WHU/Wheel-GINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：47 · 宿主：github

围绕轮式/轮上 IMU 与 GNSS 融合的导航实现，配套 IEEE TITS 等论文场景，强调非中心安装惯性器件的运动约束。适合研究车载特殊安装与轮式里程约束。与经典车体中心松组合假设不同，杠杆臂与运动学模型必须按论文设置；纯测地 PPP/RTK 请另接专用引擎。

#### [GNSS_IMU](https://github.com/rtklibexplorer/GNSS_IMU)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：35 · 宿主：github

rtklibexplorer 社区风格的松组合 GNSS/IMU Python 实现，便于配合 demo5 博客理解传感器融合步骤。适合入门松组合与噪声调参。不是高阶紧组合，也不含视觉/激光；外场应用前按设备重做 Allan 方差与杆臂标定，复杂场景请改用 KF-GINS 或 OB_GINS。

#### [GINS](https://github.com/zhangwhu/GINS)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：21 · 宿主：github

仓库描述只有「PPP-RTK/INS」，没有 README。src 下是 RTKLIB 派生的 C 文件（pntpos/ppppos/pppar/rtkpos 等）加 PSINS 惯导代码和 GNSS/IMU 配置类，另有 Example 目录。具体场景、传感器与数据格式需读源码确认。与 HKUST GVINS、i2Nav KF-GINS 名称接近但不是同一项目。

#### [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：20 · 宿主：github

基于 ROS，融合 IMU 与 GPS，实现从指定起点到终点的导引示例，偏机器人室外导航入门。适合实验室演示与课程项目。状态估计与工程完整度有限；高精度车载/航空组合导航请对照 NaveGo、KF-GINS、OB_GINS 等更完整工具箱。ROS 发行版与消息类型需与仓库分支匹配。室外实测前先在仿真或录包数据上验证。

#### [KF-GINS-Py](https://github.com/salmoshu/KF-GINS-Py)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：13 · 宿主：github

把 KF-GINS 类 EKF 松组合思路落到 Python，便于逐步打印状态与协方差、快速改状态维与观测模型。适合教学与算法原型。数值性能与长航时稳健性不如 C++ 原版；外场应用请回归 KF-GINS/OB_GINS，并严格完成 IMU 噪声标定与杆臂测量后再谈精度。

#### [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：3 · 宿主：github

该仓库讨论无人机在失去 GNSS 定位与地面站通信时，如何尝试智能返回起飞点（说明多为俄文）。适合关注反失联、视觉/惯性备援导航的课题组作思路参考。场景特殊，文档完整度与维护活跃度需要自行评估，不能当作常规 GNSS 定位或 RTK 解算库来用；任何实飞验证必须在合规空域进行，并保留独立冗余保护措施。

## 仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim) | gnss-ins-sim：GNSS+INS 轨迹与传感器仿真 | Python | 1487 | 🏷️ 个人社区 核心 |
| [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS) | Indirect_EKF_IMU_GPS：间接法 EKF 的 IMU/GPS 融合仿真 | MATLAB | 96 | 🏷️ 个人社区 |

### 详细说明

#### [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：1487 · 宿主：github

生成运动轨迹、传感器噪声与简单融合仿真，星标很高。适合算法回归测试。真实 GNSS 信号层仿真请看 gps-sdr-sim/SignalSim。

#### [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：96 · 宿主：github

间接法（误差状态）卡尔曼滤波的 IMU/GPS 融合 MATLAB 仿真，IMU 与 GPS 数据均由程序仿真生成，适合对照直接法教材理解误差状态建模。仓库 2017 年后未更新，不含实测数据；非生产导航栈，实车标定与传感器时延需自补。

## 因子图紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GraphRTK-INS](https://github.com/GREAT-WHU/GraphRTK-INS) | GraphRTK-INS：RTK/INS 因子图紧组合 | C++ | 83 | 🏷️ 高校实验室 核心 |
| [GREAT-PIFGO](https://github.com/GREAT-WHU/GREAT-PIFGO) | GREAT-PIFGO：武大 GREAT 因子图优化模块 | C++ | 18 | 🏷️ 高校实验室 |
| [tightly-coupled-gnss-imu-fgo](https://github.com/inuex35/tightly-coupled-gnss-imu-fgo) | tightly-coupled-gnss-imu-fgo：FGO 路线 RTK+IMU 原型 | Python | 17 | 🏷️ 个人社区 |

### 详细说明

#### [GraphRTK-INS](https://github.com/GREAT-WHU/GraphRTK-INS)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：— · 星标约：83 · 宿主：github

GREAT 软件栈中的因子图优化组件，把 RTK 载波相位观测与惯导预积分等约束放进同一图优化框架，面向连续高精度导航。适合跟进武大公开组合导航算法与论文复现。依赖、编译选项与样例数据随仓库版本变化；与 GREAT-MSF、KF-GINS、OB_GINS 对照时重点看因子设计、鲁棒核与边缘化策略，而不只比轨迹图观感。

#### [GREAT-PIFGO](https://github.com/GREAT-WHU/GREAT-PIFGO)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：18 · 宿主：github

GREAT 体系内的因子图优化实现，面向精密定位与组合导航相关因子组织，便于对照论文中的图优化表述。适合已经在读 GREAT-PVT/MSF 的用户深入源码。与 GraphRTK-INS、GREAT-MSF 概念有重叠，选用前仔细阅读 README 的适用场景、输入观测类型与样例数据，避免重复造轮子。

#### [tightly-coupled-gnss-imu-fgo](https://github.com/inuex35/tightly-coupled-gnss-imu-fgo)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：17 · 宿主：github

在 GTSAM 上做双差 RTK+IMU 预积分，含 LAMBDA 固定，并给东京城市数据复现。适合 FGO 路线研究。Python 原型性能有限，工程部署需重写。

## 因子图库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gtsam](https://github.com/borglab/gtsam) | GTSAM：因子图平滑/建图库（GNSS 扩展需另接） | C++ | 3680 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [gtsam](https://github.com/borglab/gtsam)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：BSD-3-Clause · 星标约：3680 · 宿主：github

通用因子图优化库，被 gtsam_gnss、GVINS、FGO-RTK 等大量 GNSS 项目依赖。本身不是 GNSS 解算器；要 GNSS 因子需接 gtsam_gnss 等扩展。

## INS工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ahrs](https://github.com/Mayitzin/ahrs) | ahrs：Python AHRS/IMU 姿态估计工具箱 | Python | 726 | 🏷️ 个人社区 |
| [NaveGo](https://github.com/rodralez/NaveGo) | NaveGo：组合导航与惯导分析 MATLAB/Octave 工具箱 | MATLAB | 640 | 🏷️ 高校实验室 |
| [nav_matlab](https://github.com/yandld/nav_matlab) | nav_matlab：MATLAB 导航与组合导航例程 | MATLAB | 276 | 🏷️ 个人社区 |
| [pyins](https://github.com/nmayorov/pyins) | INS 建模与误差分析的教学向 Python 包 | Python | 107 | 🏷️ 个人社区 |
| [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT) | 斯图加特大学导航所 INS 概念/训练工具包 | C++ | 65 | 🏷️ 高校实验室 |
| [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl) | KalmanFilters.jl：Julia KF/UKF/AUKF 库 | Julia | 55 | 🏷️ 个人社区 |

### 详细说明

#### [ahrs](https://github.com/Mayitzin/ahrs)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：726 · 宿主：github

实现多种 AHRS/IMU 姿态滤波器，接口友好。适合机器人姿态课与原型。不含 GNSS 定位引擎；与 GNSS 融合需自行松/紧组合。

#### [NaveGo](https://github.com/rodralez/NaveGo)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：LGPL-3.0 · 星标约：640 · 宿主：github

MATLAB/GNU Octave 下仿真与分析惯导/组合导航，流程完整、适合教学。科研快速改公式方便。实时嵌入式与测地 PPP-AR 非其主场。

#### [nav_matlab](https://github.com/yandld/nav_matlab)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：276 · 宿主：github

汇总惯导、GNSS 与 UWB-IMU 等导航算法的 MATLAB 例程库，改公式与画误差曲线方便，中文用户较多。适合教学演示、课程设计与快速原型。实时嵌入式与大规模数据工程需移植到 C++/ROS；与 GINav、TightlyCoupledINSGNSS 等同属 MATLAB 组合导航学习线。示例数据与坐标系约定请严格按仓库说明核对。

#### [pyins](https://github.com/nmayorov/pyins)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：107 · 宿主：github

实现 INS 机械编排与误差分析，文档清晰，适合先掌握惯性导航再耦合 GNSS。面向教学与算法试验。不是完整 GNSS/INS 产品，缺实时传感器驱动与工程标定闭环。

#### [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT)  
*🏷️ 高校实验室*

语言：C++ · 许可：MPL-2.0 · 星标约：65 · 宿主：github

斯图加特大学导航研究所（UniStuttgart-INS）开源的 INSTINCT，面向组合导航概念讲解与课程训练，MPL-2.0 许可。适合高校 INS/GNSS 松紧组合教学与算法原型。工业车规、功能安全与量产标定需另评专业方案。

#### [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：MIT · 星标约：55 · 宿主：github

JuliaGNSS 生态中的滤波库，实现经典 KF、UKF、AUKF 及其方根形式，供 GNSS/导航状态估计在 Julia 中调用。适合已用 Julia 做原型的研究代码。本身不是完整定位引擎，观测模型、周跳与模糊度处理需自建或与其它包组合。与 JuliaGNSS 其它包组合时可减少重复造轮子。方根滤波在病态协方差时通常更数值稳定。

## 紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TightlyCoupledINSGNSS](https://github.com/benzenemo/TightlyCoupledINSGNSS) | TightlyCoupledINSGNSS：伪距率+双天线测向紧组合（MATLAB） | MATLAB | 291 | 🏷️ 个人社区 |
| [TGINS](https://github.com/heiwa0519/TGINS) | TGINS：紧耦合 GNSS/INS 系统 | C++ | 90 | 🏷️ 高校实验室 |

### 详细说明

#### [TightlyCoupledINSGNSS](https://github.com/benzenemo/TightlyCoupledINSGNSS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：291 · 宿主：github

基于 Groves 组合导航教材（中译本）附带的紧组合仿真代码改写，用伪距、伪距率与 INS 数据做紧组合解算，支持双天线测向约束，附一组手推车实测数据及 Inertial Explorer 参考解。观测方程可读，便于研究生改滤波与测向约束。嵌入式实时与模糊度固定需另选 C/C++ 引擎。

#### [TGINS](https://github.com/heiwa0519/TGINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：90 · 宿主：github

紧耦合 GNSS/INS 开源实现，常与 PPPLib 作者社区一并出现。适合紧组合课程实践。维护与许可信息需核对。

## IMU驱动

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [python-openimu](https://github.com/Aceinna/python-openimu) | python-openimu：Aceinna OpenIMU Python 驱动与 WebSocket 服务 | Python | 53 | 🏷️ 个人社区 |

### 详细说明

#### [python-openimu](https://github.com/Aceinna/python-openimu)  
*🏷️ 个人社区*

语言：Python · 许可：Apache-2.0 · 星标约：53 · 宿主：github

Aceinna 设备的 Python 通信工具，支持 OpenIMU、OpenRTK 与 INS401（后者走 100BASE-T1 以太网，需装 pcap 库），提供数据记录与 WebSocket 服务。Apache-2.0；README 以 Python 3.7 为测试环境，2023 年后少有更新。偏设备接口与日志，本身不做 GNSS 解算；可与同厂商的 gnss-ins-sim 配合做组合导航实验。
