# 导航 / GNSS-INS / Navigation & INS
> 共 **27** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。

## 因子图库

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gtsam](https://github.com/borglab/gtsam) | GTSAM 平滑与建图因子图库 | C++ | 3680 | 核心 |

### 详细说明

#### [gtsam](https://github.com/borglab/gtsam)  
*核心*

语言：C++ · 星标约：3680

通用因子图优化库，被 gtsam_gnss、GVINS、FGO-RTK 等大量 GNSS 项目依赖。本身不是 GNSS 解算器；要 GNSS 因子需接扩展。


## 仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim) | GNSS+INS 轨迹与传感器仿真 | Python | 1487 | 核心 |
| [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS) | 间接法卡尔曼滤波 IMU/GPS 融合仿真（MATLAB） | MATLAB | 96 |  |

### 详细说明

#### [gnss-ins-sim](https://github.com/Aceinna/gnss-ins-sim)  
*核心*

语言：Python · 许可：MIT · 星标约：1487

生成运动轨迹、传感器噪声与简单融合仿真，星标很高。适合算法回归测试。真实 GNSS 信号层仿真请看 gps-sdr-sim/SignalSim。

#### [IndirectEKFIMUGPS](https://github.com/hgpvision/Indirect_EKF_IMU_GPS)

语言：MATLAB · 星标约：96

MATLAB 仿真仓库：用间接法卡尔曼滤波融合 IMU 与 GPS，传感器数据由仿真生成，便于推导弹、调噪声参数与画误差曲线。适合课程推导与滤波器对照。不含真实外场驱动；落地需接真实 IMU/GNSS、重做轴系与噪声标定，并评估时间同步误差。间接法状态定义与直接法不同，对照论文阅读更顺。状态维数变化时要同步改协方差初始化。


## GNSS/INS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS) | 基于 EKF 的 GNSS/INS 组合导航 | C++ | 1194 | 核心 |
| [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS) | 基于优化的 GNSS/INS 组合导航 | C++ | 647 | ★ Star · 核心 |
| [GINav](https://github.com/kaichen686/GINav) | MATLAB GNSS 与 GNSS/INS 组合算法 | MATLAB | 309 | ★ Star · 核心 |
| [imugpslocalization](https://github.com/ydsf16/imu_gps_localization) | 误差状态卡尔曼滤波融合 IMU 与 GPS（C++） | C++ | 734 |  |
| [ignav](https://github.com/Erensu/ignav) | INS 与 GNSS 组合导航实现 | C | 472 | ★ Star |
| [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding) | ROS 框架下 IMU+GPS 点到点导引示例 | C++ | 20 |  |
| [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station) | GNSS/链路丢失时无人机智能返航相关代码 | C | 3 |  |

### 详细说明

#### [KF-GINS](https://github.com/i2Nav-WHU/KF-GINS)  
*核心*

语言：C++ · 许可：GPL-3.0 · 星标约：1194

经典 EKF 框架的 GNSS/INS 开源实现，文档与课程友好，星标很高。适合教学和基线实现。因子图/滑窗优化性能边界看 OB_GINS/gici。

#### [OB_GINS](https://github.com/i2Nav-WHU/OB_GINS)  
*★ Star · 核心*

语言：C++ · 许可：GPL-3.0 · 星标约：647

武大 i2Nav 开源的优化型 GNSS/INS 组合，在开源组合导航里引用与星标都高。适合车载/机器人紧组合研究。纯测地 PPP-AR 不是目标；视觉相关见 IC-GVINS。

#### [GINav](https://github.com/kaichen686/GINav)  
*★ Star · 核心*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：309

MATLAB 实现 GNSS 及松/紧组合常用算法，改方程方便。适合研究生入门。实时嵌入式部署需移植。

#### [imugpslocalization](https://github.com/ydsf16/imu_gps_localization)

语言：C++ · 星标约：734

用误差状态卡尔曼滤波（ESKF）融合 IMU 与 GPS 的开源 C++ 实现，示例清晰、星标较高，是学习松组合与误差状态建模的常用入口。适合导航算法初学者与机器人定位原型。默认偏松组合教学场景；载波相位 RTK 或视觉紧组合不在核心范围，需另接相应模块。IMU 噪声参数要用 Allan 方差等方法实测，不宜照搬默认值。

#### [ignav](https://github.com/Erensu/ignav)  
*★ Star*

语言：C · 星标约：472

C 语言组合导航实现，轻量、易嵌入。适合固件向开发者。功能广度与现代因子图方案不同，选前看清状态模型。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [ImuGpsGuiding](https://github.com/JackJu-HIT/ImuGpsGuiding)

语言：C++ · 星标约：20

基于 ROS，融合 IMU 与 GPS，实现从指定起点到终点的导引示例，偏机器人室外导航入门。适合实验室演示与课程项目。状态估计与工程完整度有限；高精度车载/航空组合导航请对照 NaveGo、KF-GINS、OB_GINS 等更完整工具箱。ROS 发行版与消息类型需与仓库分支匹配。室外实测前先在仿真或录包数据上验证。

#### [Smart-UAV-Return-GNSS-Station](https://github.com/citec-spbu/Smart-UAV-Return-GNSS-Station)

语言：C · 星标约：3

该仓库讨论无人机在失去 GNSS 定位与地面站通信时，如何尝试智能返回起飞点（说明多为俄文）。适合关注反失联、视觉/惯性备援导航的课题组作思路参考。场景特殊，文档完整度与维护活跃度需要自行评估，不能当作常规 GNSS 定位或 RTK 解算库来用；任何实飞验证必须在合规空域进行，并保留独立冗余保护措施。


## GNSS/INS/视觉

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gici-open](https://github.com/chichengcn/gici-open) | GNSS/INS/相机紧组合开源库 GICI | C++ | 667 | 核心 |
| [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel) | VINS-Mono 融合轮速计与 GNSS（自动驾驶） | C++ | 280 |  |
| [carvig](https://github.com/Erensu/carvig) | 车载 INS/GNSS/视觉组合导航（C） | C | 120 |  |

### 详细说明

#### [gici-open](https://github.com/chichengcn/gici-open)  
*核心*

语言：C++ · 许可：GPL-3.0 · 星标约：667

多传感器紧组合库，支持 GNSS（含精密定位模式）与 INS/相机，工程结构完整。适合机器人户外定位。编译与配置复杂；测地事后处理另选 PRIDE。

#### [VINS-GPS-Wheel](https://github.com/Wallong/VINS-GPS-Wheel)

语言：C++ · 星标约：280

在 VINS-Mono 上紧耦合轮速计、松耦合 GPS，并在 KAIST 等数据集验证，面向自动驾驶室外定位。适合已有视觉惯性栈、想加轮速与 GNSS 全局约束的团队。依赖 ROS/VINS 生态；GNSS 中断或城市峡谷时仍主要靠视觉惯性与轮速。轮速标度因数误差会在长直道上缓慢积累。数据集标定文件缺失时融合容易发散。

#### [carvig](https://github.com/Erensu/carvig)

语言：C · 星标约：120

面向车辆定位的 INS/GNSS/视觉一体化导航实现（C），把惯导、卫星与视觉观测纳入同一解算框架，服务自动驾驶或车载定位验证。适合做多传感器室外定位的工程与研究生。纯 GNSS 的 RTK/PPP 引擎深度不如 RTKLIB/PRIDE；本库价值在融合架构，文档与外场标定成本需自行评估。传感器外参与时间同步质量会直接限制融合精度。


## GNSS/视觉/INS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GVINS](https://github.com/HKUST-Aerial-Robotics/GVINS) | 紧耦合 GNSS-视觉-惯性系统 | C++ | 1160 |  |
| [IC-GVINS](https://github.com/i2Nav-WHU/IC-GVINS) | INS 中心的稳健实时 GNSS-视觉-惯性导航 | C++ | 690 |  |
| [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS) | MSCKF 视觉惯性里程计与 GPS 融合 | C++ | 31 |  |

### 详细说明

#### [GVINS](https://github.com/HKUST-Aerial-Robotics/GVINS)

语言：C++ · 许可：GPL-3.0 · 星标约：1160

港科大开源 GVINS，把 GNSS 约束进 VIO，改善全局一致性。适合无人机/户外 SLAM。对 GNSS 原始观测质量敏感。

#### [IC-GVINS](https://github.com/i2Nav-WHU/IC-GVINS)

语言：C++ · 许可：GPL-3.0 · 星标约：690

以 INS 为中心耦合 GNSS 与视觉，强调实时与稳健。适合户外机器人/自动驾驶定位研究。标定与同步数据要求高。

#### [msckfvioGPS](https://github.com/loveforeverLi/msckf_vio_GPS)

语言：C++ · 星标约：31

在 MSCKF-VIO 上增加 GPS 融合，用卫星位置约束抑制视觉惯性漂移并对齐全球坐标，服务无人机与地面机器人。适合已有 MSCKF 栈、需要全球定位的团队。与上游 MSCKF 的同步情况需自查；城市峡谷 GNSS 质量差时收益有限，精密测地仍用专用 PPP/RTK。相机-IMU 外参标定质量往往比 GPS 权重更敏感。


## 车载定位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [eagleye](https://github.com/MapIV/eagleye) | 基于 GNSS/IMU 的精密车载定位 | C++ | 775 |  |

### 详细说明

#### [eagleye](https://github.com/MapIV/eagleye)

语言：C++ · 许可：BSD-3-Clause · 星标约：775

面向自动驾驶车辆的 GNSS/IMU 精密定位开源栈，工程案例多。适合车载 ROS 生态。测地学参考架与 PPP-AR 产品需求不同。


## INS工具包

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [NaveGo](https://github.com/rodralez/NaveGo) | NaveGo：组合导航与惯导分析 MATLAB/Octave 工具箱 | MATLAB | 640 |  |
| [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT) | 组合导航概念与训练用 INS 工具包 | C++ | 65 |  |
| [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl) | Julia 卡尔曼滤波库（KF/UKF/AUKF 及方根型） | Julia | 55 |  |

### 详细说明

#### [NaveGo](https://github.com/rodralez/NaveGo)

语言：MATLAB · 星标约：640

开源 MATLAB/GNU Octave 工具箱 NaveGo，用于处理组合导航系统并分析惯性传感器，覆盖仿真与后处理教学流程，社区认可度高。适合导航专业课与算法对照实验。相对 C++ 实时库更偏离线研究；可与 KF-GINS、GINav 等并列阅读滤波与误差建模差异。Octave 兼容性因版本而异，复杂算例优先 MATLAB。

#### [INSTINCT](https://github.com/UniStuttgart-INS/INSTINCT)

语言：C++ · 许可：MPL-2.0 · 星标约：65

斯图加特大学 INS 工具包，强调概念与训练。适合教学实验。工业车规方案需另评。

#### [KalmanFilters.jl](https://github.com/JuliaGNSS/KalmanFilters.jl)

语言：Julia · 星标约：55

JuliaGNSS 生态中的滤波库，实现经典 KF、UKF、AUKF 及其方根形式，供 GNSS/导航状态估计在 Julia 中调用。适合已用 Julia 做原型的研究代码。本身不是完整定位引擎，观测模型、周跳与模糊度处理需自建或与其它包组合。与 JuliaGNSS 其它包组合时可减少重复造轮子。方根滤波在病态协方差时通常更数值稳定。


## 多传感器融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [syncgpslidarimucam](https://github.com/nkliuhui/sync_gps_lidar_imu_cam) | 激光雷达-IMU-相机-GPS 硬件时间同步方案 | C++ | 252 |  |
| [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF) | GREAT 多传感器融合（PPP/RTK+INS 等） | C++ | 150 |  |
| [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation) | GPS+里程计+罗盘 EKF 融合定位（MATLAB） | MATLAB | 89 |  |

### 详细说明

#### [syncgpslidarimucam](https://github.com/nkliuhui/sync_gps_lidar_imu_cam)

语言：C++ · 星标约：252

给出 lidar、IMU、相机与 GPS 的时间戳硬件同步思路与参考实现，解决多传感器融合前的时钟对齐问题。适合自动驾驶与机器人传感器套件研发。解决的是同步而非状态估计；滤波/建图需另接 VINS、GICI、gtsam 等。硬件触发拓扑要比纯软件时间戳对齐更稳。线缆延时与触发极性要在示波器上核验。选用前建议先跑通作者提供的最小示例。

#### [GREAT-MSF](https://github.com/GREAT-WHU/GREAT-MSF)

语言：C++ · 许可：GPL-3.0 · 星标约：150

GREAT 组多传感器融合系统，支持 PPP/RTK 与 INS 等组合。适合已跟 GREAT-PVT 的用户向上集成。文档跟随版本变化。

#### [GPSMilemeterIMUEKFLocation](https://github.com/gilbertz/GPS_Milemeter_IMU_EKFLocation)

语言：MATLAB · 星标约：89

MATLAB 实现：以 GPS、里程计与电子罗盘为观测，用扩展卡尔曼滤波（EKF）融合输出滤波位置，便于车载多传感器定位教学。适合课程作业与算法对比实验。观测与噪声模型相对简化；视觉紧组合或 RTK 模糊度固定需改用 KF-GINS、GraphGNSSLib 等专用库。电子罗盘磁干扰环境下需额外标定或降权。


## 原始GNSS融合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion) | 原始 GNSS 与其他传感器融合的代码与数据 | — | 160 |  |

### 详细说明

#### [raw-gnss-fusion](https://github.com/JonasBchrt/raw-gnss-fusion)

许可：LGPL-3.0 · 星标约：160

公开原始 GNSS 与多传感器融合的代码、数据与结果，便于复现论文设定。适合研究起步。不是开箱即用商业导航软件。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## INS建模

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [pyins](https://github.com/nmayorov/pyins) | Python 惯性导航建模与分析 | Python | 107 |  |

### 详细说明

#### [pyins](https://github.com/nmayorov/pyins)

语言：Python · 许可：MIT · 星标约：107

INS 机械编排与误差分析的 Python 包，教学清晰。适合先搞懂 INS 再耦合 GNSS。不是完整 GNSS/INS 产品。


## 紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TGINS](https://github.com/heiwa0519/TGINS) | 紧耦合 GNSS/INS 系统 | C++ | 90 |  |

### 详细说明

#### [TGINS](https://github.com/heiwa0519/TGINS)

语言：C++ · 星标约：90

紧耦合 GNSS/INS 开源实现，常与 PPPLib 作者社区一并出现。适合紧组合课程实践。维护与许可信息需核对。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 因子图紧组合

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [tightly-coupled-gnss-imu-fgo](https://github.com/inuex35/tightly-coupled-gnss-imu-fgo) | GTSAM 上 RTK+IMU 紧组合（LAMBDA/预积分） | Python | 17 |  |

### 详细说明

#### [tightly-coupled-gnss-imu-fgo](https://github.com/inuex35/tightly-coupled-gnss-imu-fgo)

语言：Python · 许可：BSD-3-Clause · 星标约：17

在 GTSAM 因子图上做双差 RTK+IMU 预积分，含 LAMBDA 固定，并给东京城市数据复现。适合 FGO 路线研究。Python 原型性能有限。
