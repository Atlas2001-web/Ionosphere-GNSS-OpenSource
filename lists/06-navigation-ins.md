# 导航 / Navigation & INS
> **60** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

## B2b组合导航

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [BDS-3-PPP-B2b_IMU_LiDAR](https://github.com/xdinav/BDS-3-PPP-B2b_IMU_LiDAR) | PPP-B2b 与 IMU/LiDAR 融合试验 | — | 6 | 🏷️ 个人社区 |

### 详细说明

#### [BDS-3-PPP-B2b_IMU_LiDAR](https://github.com/xdinav/BDS-3-PPP-B2b_IMU_LiDAR)  
*🏷️ 个人社区*

语言：— · 许可：— · 星标约：6 · 宿主：github

把 PPP-B2b 与 IMU/LiDAR 结合的试验工程，面向高动态或遮挡场景的多传感器融合。适合看改正服务如何进组合导航。成熟度与标定流程因仓库而异，引用前请用自有数据复现关键指标。

## GNSS/INS/视觉

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gici-open](https://github.com/chichengcn/gici-open) | GICI：GNSS/INS/相机紧组合开源库 | C++ | 667 | 🏷️ 高校实验室 核心 |
| [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel) | VINS-Mono 融合轮速计与 GNSS（自动驾驶） | C++ | 280 | 🏷️ 个人社区 |
| [RTK-Visual-Inertial-Navigation](https://github.com/xiaohong-huang/RTK-Visual-Inertial-Navigation) | 滑窗滤波框架下的 RTK 视觉惯性导航 | C++ | 136 | 🏷️ 个人社区 |
| [carvig](https://github.com/Erensu/carvig) | 车载 INS/GNSS/视觉组合导航（C） | C | 120 | 🏷️ 个人社区 |
| [salsa](https://github.com/yxw027/salsa) | GNSS+视觉+惯性状态估计相关实现 | C++ | 14 | 🏷️ 高校实验室 |
| [GVINS-WHU](https://github.com/zhangwhu/GVINS) | 武大相关：PPP-RTK/INS/视觉组合导航（勿与港科大 GVINS-HKUST 混淆） | C++ | 12 | 🏷️ 高校实验室 |

### 详细说明

#### [gici-open](https://github.com/chichengcn/gici-open)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：667 · 宿主：github

工程结构完整，支持 GNSS 精密模式与 INS/相机紧组合。适合户外机器人定位研究。编译配置较重；事后测地 PPP-AR 另选 PRIDE/Ginan。

#### [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：280 · 宿主：github

在 VINS-Mono 上紧耦合轮速计、松耦合 GPS，并在 KAIST 等数据集验证，面向自动驾驶室外定位。适合已有视觉惯性栈、想加轮速与 GNSS 全局约束的团队。依赖 ROS/VINS 生态；GNSS 中断或城市峡谷时仍主要靠视觉惯性与轮速。轮速标度因数误差会在长直道上缓慢积累。数据集标定文件缺失时融合容易发散。

#### [RTK-Visual-Inertial-Navigation](https://github.com/xiaohong-huang/RTK-Visual-Inertial-Navigation)  
*🏷️ 个人社区*

语言：C++ · 许可：GPL-3.0 · 星标约：136 · 宿主：github

在滑窗滤波框架里融合 RTK/DGNSS 与视觉惯性，面向高精度户外机器人与自动驾驶实验。适合已有 VIO 基础、想引入载波相位差分约束的团队。测地网 RTK 服务运维与模糊度完好性监测非其主场；可与 GVINS、gici-open、Multi_Sensor_Fusion 比较紧耦合策略。外参标定质量往往比滤波形式更能决定最终精度。

#### [carvig](https://github.com/Erensu/carvig)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：120 · 宿主：github

面向车辆定位的 INS/GNSS/视觉一体化导航实现（C），把惯导、卫星与视觉观测纳入同一解算框架，服务自动驾驶或车载定位验证。适合做多传感器室外定位的工程与研究生。纯 GNSS 的 RTK/PPP 引擎深度不如 RTKLIB/PRIDE；本库价值在融合架构，文档与外场标定成本需自行评估。传感器外参与时间同步质量会直接限制融合精度。

#### [salsa](https://github.com/yxw027/salsa)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：14 · 宿主：github

融合 GNSS、视觉与惯性的状态估计原型，用于机器人室外全局定位并抑制纯视觉惯性漂移。适合多传感器融合架构与外参标定实验。传感器时间同步与标定成本较高；纯测地精密定位不如专用 PPP/RTK 引擎，本仓库价值在融合框架设计而非载波相位解算深度。

#### [GVINS-WHU](https://github.com/zhangwhu/GVINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：12 · 宿主：github

在 PPP-RTK/INS 基础上再融合视觉观测，面向复杂遮挡环境的连续定位。与 HKUST-Aerial-Robotics/GVINS（现名 GVINS-HKUST）是不同项目，论文、数据集与作者均不相同；引用与复现前核对仓库说明。

## 车载定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [eagleye](https://github.com/MapIV/eagleye) | 基于 GNSS/IMU 的精密车载定位 | C++ | 775 | 🏷️ 个人社区 |

### 详细说明

#### [eagleye](https://github.com/MapIV/eagleye)  
*🏷️ 个人社区*

语言：C++ · 许可：BSD-3-Clause · 星标约：775 · 宿主：github

面向自动驾驶车辆的 GNSS/IMU 精密定位开源栈，工程案例多。适合车载 ROS 生态。测地学参考架与 PPP-AR 产品需求不同。

## FGO/GNSS-UWB

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [FE-GUT](https://github.com/zhaoqj23/FE-GUT) | FE-GUT：因子图+EKF 的 GNSS/UWB 紧组合 | C++ | 79 | 🏷️ 高校实验室 |

### 详细说明

#### [FE-GUT](https://github.com/zhaoqj23/FE-GUT)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：79 · 宿主：github

混合因子图与 EKF，并开源仿真数据，便于复现时间标定实验。适合室内外衔接与 UWB 辅助研究。实网性能取决于 UWB/GNSS 标定质量。

## GNSS/INS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS) | 基于 EKF 的 GNSS/INS 组合导航 | C++ | 1194 | 🏷️ 高校实验室 核心 |
| [imu_x_fusion](https://github.com/cggos/imu_x_fusion) | imu_x_fusion：ESKF/IEKF/UKF 族 IMU+GNSS 松组合 | C++ | 1126 | 🏷️ 个人社区 核心 |
| [imugpslocalization](https://github.com/ydsf16/imu_gps_localization) | imu_gps_localization：ESKF 融合 IMU 与 GPS（C++） | C++ | 734 | 🏷️ 高校实验室 |
| [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS) | 基于优化的 GNSS/INS 组合导航 | C++ | 647 | 🏷️ 高校实验室 ★ 核心 |
| [ignav](https://github.com/Erensu/ignav) | ignav：轻量 INS/GNSS 组合导航（C） | C | 472 | 🏷️ 个人社区 ★ |
| [GINav](https://github.com/kaichen686/GINav) | MATLAB GNSS/INS 松紧组合常用算法实现 | MATLAB | 309 | 🏷️ 个人社区 ★ 核心 |
| [Loose-GNSS-IMU](https://github.com/aaronboda24/Loose-GNSS-IMU) | Loose-GNSS-IMU：经典 GNSS/IMU 松组合卡尔曼 | C++ | 187 | 🏷️ 高校实验室 |
| [KF-GINS-Matlab](https://github.com/i2Nav-WHU/KF-GINS-Matlab) | KF-GINS 的 MATLAB 版：EKF 松/紧组合 GNSS/INS | MATLAB | 137 | 🏷️ 高校实验室 核心 |
| [ublox_dgnss](https://github.com/aussierobots/ublox_dgnss) | ROS2 u-blox UBX 驱动（F9P/F9R/X20P 差分与移动基站） | C++ | 86 | 🏷️ 个人社区 |
| [GIOW-release](https://github.com/i2Nav-WHU/GIOW-release) | 全轮角/里程计辅助的 GNSS/INS/ODO 组合导航算法发布版 | C++ | 75 | 🏷️ 高校实验室 核心 |
| [Wheel-GINS](https://github.com/i2Nav-WHU/Wheel-GINS) | 轮式惯导与 GNSS 组合的导航系统（IEEE TITS 相关） | C++ | 47 | 🏷️ 高校实验室 |
| [GNSS_IMU](https://github.com/rtklibexplorer/GNSS_IMU) | rtklibexplorer 系松组合 GNSS/IMU 的 Python 实现 | Python | 35 | 🏷️ 个人社区 |
| [GINS](https://github.com/zhangwhu/GINS) | PPP-RTK 与惯导组合的 GINS 实现（武大相关） | C | 21 | 🏷️ 高校实验室 |
| [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding) | ROS 框架下 IMU+GPS 点到点导引示例 | C++ | 20 | 🏷️ 个人社区 |
| [KF-GINS-Py](https://github.com/salmoshu/KF-GINS-Py) | KF-GINS 思路的 Python 移植，便于读 EKF 组合导航 | Python | 13 | 🏷️ 高校实验室 |
| [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station) | GNSS/链路丢失时无人机智能返航相关代码 | C | 3 | 🏷️ 个人社区 |

### 详细说明

#### [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS)  
*🏷️ 高校实验室 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：1194 · 宿主：github

经典 EKF 框架的 GNSS/INS 开源实现，文档与课程友好，星标很高。适合教学和基线实现。因子图/滑窗优化性能边界看 OB_GINS/gici。

#### [imu_x_fusion](https://github.com/cggos/imu_x_fusion)  
*🏷️ 个人社区 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：1126 · 宿主：github

同一框架里切换 ESKF、IEKF、UKF 等，公式与代码对应清晰，利于学习滤波器差异。适合课程与算法对照。工业级标定、时间同步与完整性监测需另补；纯测地 PPP 请另选专用引擎。

#### [imugpslocalization](https://github.com/ydsf16/imu_gps_localization)  
*🏷️ 高校实验室*

语言：C++ · 许可：— · 星标约：734 · 宿主：github

示例清晰的 ESKF 松组合实现，星标较高，适合第一次跑通误差状态建模。课程与原型友好。缺少完整测地产品链；高动态/遮挡需加强观测模型。

#### [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS)  
*🏷️ 高校实验室 ★ 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：647 · 宿主：github

武大 i2Nav 开源的优化型 GNSS/INS 组合，在开源组合导航里引用与星标都高。适合车载/机器人紧组合研究。纯测地 PPP-AR 不是目标；视觉相关见 IC-GVINS。

#### [ignav](https://github.com/Erensu/ignav)  
*🏷️ 个人社区 ★*

语言：C · 许可：— · 星标约：472 · 宿主：github

代码轻量、易读，适合固件向开发者移植。功能广度不及现代因子图方案；上线前务必核对状态模型与坐标系约定。

#### [GINav](https://github.com/kaichen686/GINav)  
*🏷️ 个人社区 ★ 核心*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：309 · 宿主：github

以 MATLAB 实现 GNSS 定位及松/紧组合常用滤波与方程，便于改模型、画残差，研究生入门友好。适合课程作业与论文原型。实时嵌入式或高吞吐现场部署需移植到 C/C++ 或其他引擎。

#### [Loose-GNSS-IMU](https://github.com/aaronboda24/Loose-GNSS-IMU)  
*🏷️ 高校实验室*

语言：C++ · 许可：MIT · 星标约：187 · 宿主：github

结构直白，便于第一次跑通松组合闭环与噪声调参。适合课程实验。紧组合、模糊度固定与完整性监测需另寻方案。

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

#### [Wheel-GINS](https://github.com/i2Nav-WHU/Wheel-GINS)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：47 · 宿主：github

围绕轮式/轮上 IMU 与 GNSS 融合的导航实现，配套 IEEE TITS 等论文场景，强调非中心安装惯性器件的运动约束。适合研究车载特殊安装与轮式里程约束。与经典车体中心松组合假设不同，杠杆臂与运动学模型必须按论文设置；纯测地 PPP/RTK 请另接专用引擎。

#### [GNSS_IMU](https://github.com/rtklibexplorer/GNSS_IMU)  
*🏷️ 个人社区*

语言：Python · 许可：BSD-3-Clause · 星标约：35 · 宿主：github

rtklibexplorer 社区风格的松组合 GNSS/IMU Python 实现，便于配合 demo5 博客理解传感器融合步骤。适合入门松组合与噪声调参。不是高阶紧组合，也不含视觉/激光；外场应用前按设备重做 Allan 方差与杆臂标定，复杂场景请改用 KF-GINS 或 OB_GINS。

#### [GINS](https://github.com/zhangwhu/GINS)  
*🏷️ 高校实验室*

语言：C · 许可：— · 星标约：21 · 宿主：github

将 PPP-RTK 改正与惯导结合的 GINS 实现，追求遮挡环境下仍较连续的高精度导航解。适合阅读 PPP-RTK/INS 相关论文时对照工程结构。公开文档与示例数据完整度一般；与 HKUST GVINS、i2Nav KF-GINS 名称接近但路线不同，选用前核对作者与传感器组合。

#### [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：20 · 宿主：github

基于 ROS，融合 IMU 与 GPS，实现从指定起点到终点的导引示例，偏机器人室外导航入门。适合实验室演示与课程项目。状态估计与工程完整度有限；高精度车载/航空组合导航请对照 NaveGo、KF-GINS、OB_GINS 等更完整工具箱。ROS 发行版与消息类型需与仓库分支匹配。室外实测前先在仿真或录包数据上验证。

#### [KF-GINS-Py](https://github.com/salmoshu/KF-GINS-Py)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：13 · 宿主：github

把 KF-GINS 类 EKF 松组合思路落到 Python，便于逐步打印状态与协方差、快速改状态维与观测模型。适合教学与算法原型。数值性能与长航时稳健性不如 C++ 原版；外场应用请回归 KF-GINS/OB_GINS，并严格完成 IMU 噪声标定与杆臂测量后再谈精度。

#### [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：3 · 宿主：github

该仓库讨论无人机在失去 GNSS 定位与地面站通信时，如何尝试智能返回起飞点（说明多为俄文）。适合关注反失联、视觉/惯性备援导航的课题组作思路参考。场景特殊，文档完整度与维护活跃度需要自行评估，不能当作常规 GNSS 定位或 RTK 解算库来用；任何实飞验证必须在合规空域进行，并保留独立冗余保护措施。

## 多传感器融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Multi_Sensor_Fusion](https://github.com/2013fangwentao/Multi_Sensor_Fusion) | Multi_Sensor_Fusion：GNSS/IMU/视觉多源融合 | C++ | 940 | 🏷️ 高校实验室 核心 |
| [MINS](https://github.com/rpng/MINS) | MINS：RPNG 多传感器（含 GNSS）紧组合导航系统 | C++ | 779 | 🏷️ 高校实验室 |
| [GLIO](https://github.com/XikunLiu-huskit/GLIO) | GLIO：GNSS/LiDAR/IMU 紧耦合连续定位 | C | 438 | 🏷️ 高校实验室 |
| [libRSF](https://github.com/TUC-ProAut/libRSF) | libRSF：鲁棒传感器融合与在线定位库 | C++ | 337 | 🏷️ 高校实验室 |
| [syncgpslidarimucam](https://github.com/nkliuhui/sync_gps_lidar_imu_cam) | 激光雷达-IMU-相机-GPS 硬件时间同步方案 | C++ | 252 | 🏷️ 个人社区 |
| [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF) | GREAT 多传感器融合（PPP/RTK+INS 等） | C++ | 150 | 🏷️ 高校实验室 |
| [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation) | GPS_Milemeter_IMU_EKF：GPS+里程计+罗盘 EKF（MATLAB） | MATLAB | 89 | 🏷️ 高校实验室 |

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

给出 lidar、IMU、相机与 GPS 的时间戳硬件同步思路与参考实现，解决多传感器融合前的时钟对齐问题。适合自动驾驶与机器人传感器套件研发。解决的是同步而非状态估计；滤波/建图需另接 VINS、GICI、gtsam 等。硬件触发拓扑要比纯软件时间戳对齐更稳。线缆延时与触发极性要在示波器上核验。选用前建议先跑通作者提供的最小示例。

#### [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：150 · 宿主：github

GREAT 组多传感器融合系统，支持 PPP/RTK 与 INS 等组合。适合已跟 GREAT-PVT 的用户向上集成。文档跟随版本变化。

#### [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：89 · 宿主：github

把 GPS、里程计与罗盘送进 EKF，流程直观。适合车载松组合入门。高精度车道级与视觉惯性请另选现代框架。

## 仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim) | GNSS+INS 轨迹与传感器仿真 | Python | 1487 | 🏷️ 个人社区 核心 |
| [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS) | Indirect_EKF_IMU_GPS：间接法 EKF 的 IMU/GPS 融合仿真 | MATLAB | 96 | 🏷️ 高校实验室 |

### 详细说明

#### [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim)  
*🏷️ 个人社区 核心*

语言：Python · 许可：MIT · 星标约：1487 · 宿主：github

生成运动轨迹、传感器噪声与简单融合仿真，星标很高。适合算法回归测试。真实 GNSS 信号层仿真请看 gps-sdr-sim/SignalSim。

#### [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：96 · 宿主：github

经典间接法误差状态演示，适合对照直接法教材。教学友好。非生产导航栈；实车标定与传感器时延需自补。

## GNSS/视觉/INS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [OpenVINS](https://github.com/rpng/open_vins) | OpenVINS：RPNG 视觉-惯性导航开源研究平台 | C++ | 3115 | 🏷️ 高校实验室 |
| [GVINS-HKUST](https://github.com/HKUST-Aerial-Robotics/GVINS) | GVINS：港科大紧耦合 GNSS-视觉-惯性系统 | C++ | 1160 | 🏷️ 高校实验室 |
| [IC-GVINS](https://github.com/i2Nav-WHU/IC-GVINS) | IC-GVINS：INS 中心的实时 GNSS-VIO 组合导航 | C++ | 690 | 🏷️ 高校实验室 |
| [OKVIS2-X](https://github.com/ethz-mrl/OKVIS2-X) | OKVIS2-X：可融 GNSS 的开源视觉-惯性 SLAM | C++ | 410 | 🏷️ 高校实验室 |
| [gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm) | GNSS 原始测量处理的 ROS 基础定义与工具 | C++ | 164 | 🏷️ 高校实验室 |
| [ublox_driver](https://github.com/HKUST-Aerial-Robotics/ublox_driver) | 面向 ZED-F9P 的 ROS u-blox 驱动 | C++ | 159 | 🏷️ 高校实验室 |
| [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS) | MSCKF 视觉惯性里程计与 GPS 融合 | C++ | 31 | 🏷️ 个人社区 |

### 详细说明

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

#### [OKVIS2-X](https://github.com/ethz-mrl/OKVIS2-X)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：410 · 宿主：github

OKVIS2-X 在经典 OKVIS 视觉惯性框架上扩展稠密深度或 LiDAR，并支持融合 GNSS，面向机器人户外定位。BSD-3 风格许可，附 TRO/arXiv 论文。构建依赖较重；GNSS 为可选传感器，不是独立 PPP/RTK 引擎。

#### [gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：164 · 宿主：github

港科大空中机器人组为 GVINS 等项目抽出的 GNSS 消息与工具包，统一原始观测在 ROS 中的表示。做视觉惯性加 GNSS 融合时几乎都会碰到。单独使用需自备接收机驱动与解算前端；与 ublox_driver、GVINS-Dataset 同生态，测地 RINEX 流水线请另选 georinex、Anubis 等。

#### [ublox_driver](https://github.com/HKUST-Aerial-Robotics/ublox_driver)  
*🏷️ 高校实验室*

语言：C++ · 许可：GPL-3.0 · 星标约：159 · 宿主：github

为机器人实验提供的 u-blox（尤其 ZED-F9P）ROS 驱动，输出与 gnss_comm/GVINS 衔接的原始测量与定位话题。适合搭车载或无人机 GNSS-视觉实验台。不是通用多厂商驱动，也不替代测地接收机网管软件；配置、波特率与固件版本需按仓库说明核对，和官方 u-center 联调可减少踩坑。

#### [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：31 · 宿主：github

在 MSCKF-VIO 上增加 GPS 融合，用卫星位置约束抑制视觉惯性漂移并对齐全球坐标，服务无人机与地面机器人。适合已有 MSCKF 栈、需要全球定位的团队。与上游 MSCKF 的同步情况需自查；城市峡谷 GNSS 质量差时收益有限，精密测地仍用专用 PPP/RTK。相机-IMU 外参标定质量往往比 GPS 权重更敏感。

## GNSS/INS对比

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_INS_Integrations_Comparisons](https://github.com/ZhengdaoLI0602/GNSS_INS_Integrations_Comparisons) | 港理工相关开源：KF/AKF/FGO/AFGO 等 GNSS/INS 二维定位对比实验代码 | MATLAB | 70 | 🏷️ 高校实验室 |

### 详细说明

#### [GNSS_INS_Integrations_Comparisons](https://github.com/ZhengdaoLI0602/GNSS_INS_Integrations_Comparisons)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：see upstream README · 星标约：70 · 宿主：github

配套 Remote Sensing 论文的 MATLAB 实验仓，对比固定增益 KF、自适应 KF、因子图及自适应因子图在 GNSS/INS 二维定位中的表现，FGO 部分参考 MathWorks 示例改造。适合算法课与论文复现。非完整车载三维产品；数据准备脚本需按 README 逐步运行。

## ROS2原始观测

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss_ros_standardization](https://github.com/DaikiNiimi/gnss_ros_standardization) | ROS 2 标准化 GNSS 原始观测/星历话题（u-blox/Septentrio/NovAtel/RTCM3） | C++ | 21 | 🏷️ 个人社区 |

### 详细说明

#### [gnss_ros_standardization](https://github.com/DaikiNiimi/gnss_ros_standardization)  
*🏷️ 个人社区*

语言：C++ · 许可：MIT · 星标约：21 · 宿主：github

统一多品牌接收机原始观测与星历到 ROS 2 标准话题，降低紧组合与多传感器融合的驱动碎片化，含 RTK 演示配置说明。目标是一次开发、多机复用。侧重接口与消息层而非完整 PPP 引擎；具体消息定义、驱动覆盖与硬件接线以仓库文档和演示配置为准。

## 因子图紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GraphRTK-INS](https://github.com/GREAT-WHU/GraphRTK-INS) | 武大 GREAT 因子图模块：RTK 与惯导紧组合 | C++ | 83 | 🏷️ 高校实验室 核心 |
| [GREAT-PIFGO](https://github.com/GREAT-WHU/GREAT-PIFGO) | GREAT 软件中的因子图优化模块（PIFGO） | C++ | 18 | 🏷️ 高校实验室 |
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

语言：C++ · 许可：— · 星标约：3680 · 宿主：github

通用因子图优化库，被 gtsam_gnss、GVINS、FGO-RTK 等大量 GNSS 项目依赖。本身不是 GNSS 解算器；要 GNSS 因子需接 gtsam_gnss 等扩展。

## 数据集

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GVINS-Dataset](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset) | 视觉/惯性/GNSS 原始测量同步数据集 | C++ | 262 | 🏷️ 高校实验室 |

### 详细说明

#### [GVINS-Dataset](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset)  
*🏷️ 高校实验室*

语言：C++ · 许可：NOASSERTION · 星标约：262 · 宿主：github

与 GVINS 配套的同步视觉、IMU 与 GNSS 原始测量数据，方便复现紧耦合实验与对比算法，是 GNSS-VIO 常用测试集之一。本身不含完整解算器；处理请配合 GVINS、gnss_comm、ublox_driver。许可字段为 NOASSERTION，论文复现与再分发前务必阅读仓库说明与引用要求。

## INS工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ahrs](https://github.com/Mayitzin/ahrs) | ahrs：Python AHRS/IMU 姿态估计工具箱 | Python | 726 | 🏷️ 个人社区 |
| [NaveGo](https://github.com/rodralez/NaveGo) | NaveGo：组合导航与惯导分析 MATLAB/Octave 工具箱 | MATLAB | 640 | 🏷️ 高校实验室 |
| [nav_matlab](https://github.com/yandld/nav_matlab) | MATLAB 导航科学计算与组合导航例程 | MATLAB | 276 | 🏷️ 个人社区 |
| [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT) | 斯图加特大学导航所 INS 概念/训练工具包 | C++ | 65 | 🏷️ 高校实验室 |
| [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl) | Julia 卡尔曼滤波库（KF/UKF/AUKF 及方根型） | Julia | 55 | 🏷️ 个人社区 |

### 详细说明

#### [ahrs](https://github.com/Mayitzin/ahrs)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：726 · 宿主：github

实现多种 AHRS/IMU 姿态滤波器，接口友好。适合机器人姿态课与原型。不含 GNSS 定位引擎；与 GNSS 融合需自行松/紧组合。

#### [NaveGo](https://github.com/rodralez/NaveGo)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：640 · 宿主：github

MATLAB/GNU Octave 下仿真与分析惯导/组合导航，流程完整、适合教学。科研快速改公式方便。实时嵌入式与测地 PPP-AR 非其主场。

#### [nav_matlab](https://github.com/yandld/nav_matlab)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：276 · 宿主：github

汇总惯导、GNSS 与 UWB-IMU 等导航算法的 MATLAB 例程库，改公式与画误差曲线方便，中文用户较多。适合教学演示、课程设计与快速原型。实时嵌入式与大规模数据工程需移植到 C++/ROS；与 GINav、TightlyCoupledINSGNSS 等同属 MATLAB 组合导航学习线。示例数据与坐标系约定请严格按仓库说明核对。

#### [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT)  
*🏷️ 高校实验室*

语言：C++ · 许可：MPL-2.0 · 星标约：65 · 宿主：github

斯图加特大学导航研究所（UniStuttgart-INS）开源的 INSTINCT，面向组合导航概念讲解与课程训练，MPL-2.0 许可。适合高校 INS/GNSS 松紧组合教学与算法原型。工业车规、功能安全与量产标定需另评专业方案。

#### [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl)  
*🏷️ 个人社区*

语言：Julia · 许可：— · 星标约：55 · 宿主：github

JuliaGNSS 生态中的滤波库，实现经典 KF、UKF、AUKF 及其方根形式，供 GNSS/导航状态估计在 Julia 中调用。适合已用 Julia 做原型的研究代码。本身不是完整定位引擎，观测模型、周跳与模糊度处理需自建或与其它包组合。与 JuliaGNSS 其它包组合时可减少重复造轮子。方根滤波在病态协方差时通常更数值稳定。

## INS建模

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyins](https://github.com/nmayorov/pyins) | INS 建模与误差分析的教学向 Python 包 | Python | 107 | 🏷️ 个人社区 |

### 详细说明

#### [pyins](https://github.com/nmayorov/pyins)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：107 · 宿主：github

实现 INS 机械编排与误差分析，文档清晰，适合先掌握惯性导航再耦合 GNSS。面向教学与算法试验。不是完整 GNSS/INS 产品，缺实时传感器驱动与工程标定闭环。

## 原始GNSS融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion) | raw-gnss-fusion：原始 GNSS 多传感器融合代码与数据 | — | 160 | 🏷️ 高校实验室 |

### 详细说明

#### [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion)  
*🏷️ 高校实验室*

语言：— · 许可：LGPL-3.0 · 星标约：160 · 宿主：github

便于复现论文设定的原始测量与融合流水线。适合研究起步。不是开箱商用导航软件；依赖与数据许可以仓库为准。

## ROS/RTKLIB

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [rtklib_ros_bridge](https://github.com/MapIV/rtklib_ros_bridge) | MapIV 开源：将 RTKLIB v2.4.3 b34 解算结果桥接到 ROS 的中间件 | C++ | 121 | 🏷️ 个人社区 |

### 详细说明

#### [rtklib_ros_bridge](https://github.com/MapIV/rtklib_ros_bridge)  
*🏷️ 个人社区*

语言：C++ · 许可：NOASSERTION · 星标约：121 · 宿主：github

把经典 RTKLIB 定位输出接入 ROS，便于自动驾驶与机器人栈消费 RTK/PPP 结果。绑定 RTKLIB 2.4.3 b34 一代接口。适合已有 RTKLIB 流水线的 ROS 集成；若需要更新算法内核应另选维护中的 RTKLIB 分支或 MRTKLIB，并注意许可与版本差异。

## 紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TightlyCoupledINSGNSS](https://github.com/benzenemo/TightlyCoupledINSGNSS) | TightlyCoupledINSGNSS：伪距率+双天线测向紧组合（MATLAB） | MATLAB | 291 | 🏷️ 个人社区 |
| [TGINS](https://github.com/heiwa0519/TGINS) | 紧耦合 GNSS/INS 系统 | C++ | 90 | 🏷️ 个人社区 |

### 详细说明

#### [TightlyCoupledINSGNSS](https://github.com/benzenemo/TightlyCoupledINSGNSS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：291 · 宿主：github

观测方程可读，便于研究生改滤波与测向约束。适合课程与仿真。嵌入式实时与模糊度固定需另选 C/C++ 引擎。

#### [TGINS](https://github.com/heiwa0519/TGINS)  
*🏷️ 个人社区*

语言：C++ · 许可：— · 星标约：90 · 宿主：github

紧耦合 GNSS/INS 开源实现，常与 PPPLib 作者社区一并出现。适合紧组合课程实践。维护与许可信息需核对。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

## 车载与机器人

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NTRIP_ROS](https://github.com/Mil1ium/NTRIP_ROS) | ROS+NTRIP+ZED-F9P RTK 接入 | Python | 54 | 🏷️ 个人社区 |

### 详细说明

#### [NTRIP_ROS](https://github.com/Mil1ium/NTRIP_ROS)  
*🏷️ 个人社区*

语言：Python · 许可：GPL-3.0 · 星标约：54 · 宿主：github

ROS 包用于连接 NTRIP caster、接收 RTCM，并服务于 u-blox ZED-F9P 一类 RTK 接收机，方便机器人/自动驾驶实验车接入差分。适合 ROS1/相关车载栈快速打通链路。依赖具体 ROS 发行版与串口/USB 配置；不是通用精密大地测量软件。

## 因子图融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssFGO](https://github.com/hz658832/gnssFGO) | RWTH 在线 GNSS/多传感器因子图定位（ROS2） | C++ | 52 | 🏷️ 高校实验室 |

### 详细说明

#### [gnssFGO](https://github.com/hz658832/gnssFGO)  
*🏷️ 高校实验室*

语言：C++ · 许可：BSD-3-Clause · 星标约：52 · 宿主：github

亚琛工大 IRT 的 gnssFGO（BSD-3-Clause，ROS 2），以连续时间轨迹与因子图融合松/紧耦合 GNSS、激光/视觉里程计等，配套数据集与 Docker。原 rwth-irt 仓已归档，维护迁至本地址。适合车载多传感器研究。依赖 ROS 2 与大量子模块，工程门槛高于纯 GNSS PPP 工具。
