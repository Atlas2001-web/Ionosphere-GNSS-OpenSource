#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge missing_meta + extras into PROJECTS.json; regenerate lists & README."""
import json
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CAT_META = {
    "ionosphere": {
        "title": "电离层 / Ionosphere",
        "file": "01-ionosphere.md",
        "blurb": "研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。",
        "readme_blurb": "研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与…",
        "who": "研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与…",
        "en": "Ionosphere",
    },
    "troposphere": {
        "title": "对流层 / Troposphere",
        "file": "02-troposphere.md",
        "blurb": "中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。",
        "readme_blurb": "中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，…",
        "who": "中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，…",
        "en": "Troposphere",
    },
    "gnss-data": {
        "title": "GNSS 数据与格式 / GNSS Data I/O",
        "file": "03-gnss-data.md",
        "blurb": "RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。",
        "readme_blurb": "RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与…",
        "who": "RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与…",
        "en": "GNSS Data I/O",
    },
    "gnss-positioning": {
        "title": "精密定位 / Precise Positioning",
        "file": "04-gnss-positioning.md",
        "blurb": "SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。",
        "readme_blurb": "SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优…",
        "who": "SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优…",
        "en": "Precise Positioning",
    },
    "orbit-clock": {
        "title": "轨道与钟差 / Orbit & Clock",
        "file": "05-orbit-clock.md",
        "blurb": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。",
        "readme_blurb": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。",
        "who": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。",
        "en": "Orbit & Clock",
    },
    "navigation-ins": {
        "title": "导航 / GNSS-INS / Navigation & INS",
        "file": "06-navigation-ins.md",
        "blurb": "GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。",
        "readme_blurb": "GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。",
        "who": "GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。",
        "en": "Navigation & INS",
    },
    "gnss-sdr": {
        "title": "软件接收机与信号 / GNSS-SDR",
        "file": "07-gnss-sdr.md",
        "blurb": "从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。",
        "readme_blurb": "从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。",
        "who": "从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。",
        "en": "GNSS-SDR",
    },
    "mobile-apps": {
        "title": "移动与嵌入式应用 / Mobile Apps",
        "file": "08-mobile-apps.md",
        "blurb": "手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。",
        "readme_blurb": "手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。",
        "who": "手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。",
        "en": "Mobile Apps",
    },
    "tools-learning": {
        "title": "学习资源与工具 / Learning & Tools",
        "file": "09-tools-learning.md",
        "blurb": "awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。",
        "readme_blurb": "awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。",
        "who": "awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。",
        "en": "Learning & Tools",
    },
}

CAT_ORDER = list(CAT_META.keys())

# name -> entry overrides keyed by full_name or url suffix
NEW_ENTRIES = [
    # ---- from missing_meta ----
    {
        "name": "laika",
        "url": "https://github.com/commaai/laika",
        "desc_zh": "comma.ai 的轻量 Python GNSS 处理库",
        "analysis_zh": "面向自动驾驶与研究的精简 GNSS 库，可下载星历/改正、做伪距定位并与 RTKLIB 风格流程对接，Python 接口干净。适合想快速验证定位链路、而不愿先啃完整测地软件栈的工程师与学生。功能覆盖远小于 PRIDE/Ginan/RTKLIB，模糊度固定与多频多星座产品化能力弱；和 rtklib-py、goGPS 对照时，优势在轻量与可嵌入脚本。",
        "language": "Python",
        "license": "MIT",
        "category": "gnss-positioning",
        "subcategory": "PPP/RTK",
        "markers": ["core"],
        "stars_approx": 723,
    },
    {
        "name": "rtkbase",
        "url": "https://github.com/Stefal/rtkbase",
        "desc_zh": "树莓派等 SBC 上自建 GNSS 基准站与 Web 管理",
        "analysis_zh": "把 u-blox/Septentrio 等接收机、RTKLIB str2str、NTRIP 与 Web GUI 捆成可部署的基准站方案，适合野外站、农场与 DIY CORS。运维人员与低成本 RTK 爱好者最常用。精度与完好性取决于接收机天线与网络质量，不是测地级网平差软件；与 BNC、商业 caster 相比更偏单站自建与易用性。",
        "language": "Python",
        "license": "AGPL-3.0",
        "category": "gnss-positioning",
        "subcategory": "RTK",
        "markers": ["core"],
        "stars_approx": 769,
    },
    {
        "name": "PyGPSClient",
        "url": "https://github.com/semuconsulting/PyGPSClient",
        "desc_zh": "NMEA/UBX/RTCM/NTRIP 等协议的 Python 图形客户端",
        "analysis_zh": "桌面 GUI 同时消化 NMEA、u-blox UBX、SBF、RTCM3、NTRIP 与 SPARTN，便于配置接收机、看星空图与差分链路。适合硬件联调、教学演示与低成本 RTK 调试。它是协议与可视化客户端，不是精密 PPP/RTK 解算引擎；底层解析依赖同作者的 pyubx2/pyrtcm/pygnssutils，深度算法请接 RTKLIB 或科研 PPP。",
        "language": "Python",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": ["core"],
        "stars_approx": 839,
    },
    {
        "name": "pyubx2",
        "url": "https://github.com/semuconsulting/pyubx2",
        "desc_zh": "u-blox UBX 协议的 Python 编解码库",
        "analysis_zh": "纯 Python 解析与生成 UBX 消息，覆盖配置、原始观测与导航输出，是连接 F9P 等模块的常用积木。嵌入式上位机、自动化测试与数据记录脚本都会用到。不处理 NMEA/RTCM（见 pygnssutils/pyrtcm），也不做定位滤波；若只要串口读星历伪距，它比完整 GUI 更轻。",
        "language": "Python",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "基础库",
        "markers": [],
        "stars_approx": 254,
    },
    {
        "name": "pygnssutils",
        "url": "https://github.com/semuconsulting/pygnssutils",
        "desc_zh": "NMEA/UBX/RTCM/NTRIP/SPARTN 的 Python CLI 工具集",
        "analysis_zh": "在 pyubx2/pyrtcm 之上提供命令行读写、广播与 NTRIP 客户端/caster 小工具，方便把协议流接到管道或测试架。适合自动化采集与协议联调。定位解算、质量评估仍需外接；相对 BNC 更偏开发者脚本而非运维级多流平台。",
        "language": "Python",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 143,
    },
    {
        "name": "pyrtcm",
        "url": "https://github.com/semuconsulting/pyrtcm",
        "desc_zh": "RTCM3 报文的 Python 解析与生成库",
        "analysis_zh": "专注 RTCM 3.x 消息编解码，可嵌入 NTRIP 客户端或自研差分链路。适合需要在 Python 里拆 MSM、站星改正而不拉起完整 BNC 的开发者。不含 caster 调度与精密定位；与 go-gnss/ntrip、ybzwyrcld/ntrip 等传输层工具互补。",
        "language": "Python",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 115,
    },
    {
        "name": "Multi_Sensor_Fusion",
        "url": "https://github.com/2013fangwentao/Multi_Sensor_Fusion",
        "desc_zh": "GNSS/IMU/视觉等多源融合与 PPP/INS 紧组合",
        "analysis_zh": "中文社区高星的多传感器融合定位仓库，覆盖 GNSS、IMU、相机，并含 PPP/INS 紧组合思路，文档与示例偏工程实践。适合车载与机器人组合导航入门到中级实现。代码风格与依赖随版本变化，完好性与测地级产品接口不如 Ginan/PRIDE；可与 imu_x_fusion、gici-open、OB_GINS 对照架构差异。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "多传感器融合",
        "markers": ["core"],
        "stars_approx": 940,
    },
    {
        "name": "imu_x_fusion",
        "url": "https://github.com/cggos/imu_x_fusion",
        "desc_zh": "基于 ESKF/IEKF/UKF 的 IMU+GNSS/里程计松组合",
        "analysis_zh": "系统实现多种卡尔曼变体（ESKF、IEKF、UKF 族）与 MAP，把 IMU 与 GNSS 或 6DoF 里程计做松组合，公式与代码对应清晰。适合滤波路线教学和算法对比实验。不含视觉紧组合与测地 PPP-AR；要图优化路线可看 OB_GINS/GTSAM 系，要多传感器紧耦合可看 gici/Multi_Sensor_Fusion。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "GNSS/INS",
        "markers": ["core"],
        "stars_approx": 1126,
    },
    {
        "name": "GLIO",
        "url": "https://github.com/XikunLiu-huskit/GLIO",
        "desc_zh": "GNSS/LiDAR/IMU 紧耦合连续定位",
        "analysis_zh": "把 GNSS 观测与激光惯性里程计紧耦合，强调城市连续、低漂移状态估计，面向户外机器人场景。适合已有 LIO 基础、想引入 GNSS 约束的研究者。测地事后精密处理与模糊度固定不是重点；许可信息需自行确认，部署前应核对数据集与依赖版本。",
        "language": "C",
        "license": "",
        "category": "navigation-ins",
        "subcategory": "多传感器融合",
        "markers": [],
        "stars_approx": 438,
    },
    {
        "name": "libRSF",
        "url": "https://github.com/TUC-ProAut/libRSF",
        "desc_zh": "面向在线定位的鲁棒传感器融合库",
        "analysis_zh": "切姆尼茨工大维护的因子/估计库，强调鲁棒核与在线定位，可接入 GNSS 与测距类观测。适合机器人状态估计与抗野值实验。不是现成的测地 PPP/RTK 产品；与 GTSAM 相比更聚焦鲁棒传感器融合示例，学习曲线中等。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "多传感器融合",
        "markers": [],
        "stars_approx": 337,
    },
    {
        "name": "rtklib-py",
        "url": "https://github.com/rtklibexplorer/rtklib-py",
        "desc_zh": "基于 demo5 的 RTKLIB Python 实现（侧重 PPK）",
        "analysis_zh": "把 rtklibexplorer/demo5 思路迁到 Python，当前以事后 PPK 为主，便于阅读算法与改实验脚本。适合不想编译 C 版、又要贴近 RTKLIB 流程的人。实时 RTK、完整 GUI 与全部信号支持仍以 C 版 RTKLIB/explorer 为准；与 laika 相比更贴近经典差分定位公式。",
        "language": "Python",
        "license": "MIT",
        "category": "gnss-positioning",
        "subcategory": "RTK",
        "markers": [],
        "stars_approx": 244,
    },
    {
        "name": "gnss_comm",
        "url": "https://github.com/HKUST-Aerial-Robotics/gnss_comm",
        "desc_zh": "GNSS 原始测量处理的 ROS 基础定义与工具",
        "analysis_zh": "港科大空中机器人组为 GVINS 等项目抽出的 GNSS 消息与工具包，统一原始观测在 ROS 中的表示。做视觉惯性+GNSS 融合时几乎都会碰到。单独使用需自备接收机驱动与解算；与 ublox_driver、GVINS-Dataset 同生态，测地 RINEX 流水线请另选 georinex 等。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "GNSS/视觉/INS",
        "markers": [],
        "stars_approx": 164,
    },
    {
        "name": "ublox_driver",
        "url": "https://github.com/HKUST-Aerial-Robotics/ublox_driver",
        "desc_zh": "面向 ZED-F9P 的 ROS u-blox 驱动",
        "analysis_zh": "为机器人实验提供的 u-blox（尤其 F9P）ROS 驱动，输出与 gnss_comm/GVINS 衔接的原始测量与定位话题。适合搭车载/无人机 GNSS-视觉实验台。不是通用多厂商驱动，也不替代测地接收机网管；配置与固件版本需按仓库说明核对。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "GNSS/视觉/INS",
        "markers": [],
        "stars_approx": 159,
    },
    {
        "name": "TightlyCoupledINSGNSS",
        "url": "https://github.com/benzenemo/TightlyCoupledINSGNSS",
        "desc_zh": "伪距/伪距率与双天线测向的 INS/GNSS 紧组合（MATLAB）",
        "analysis_zh": "MATLAB 实现伪距、伪距率与 INS 的紧组合，并支持双天线测向观测，公式可读性好。适合研究生改状态方程与观测模型。实时嵌入式与多星座模糊度固定需另行移植；可与 Loose-GNSS-IMU、GINav、KF-GINS 对照松紧组合差异。",
        "language": "MATLAB",
        "license": "BSD-2-Clause",
        "category": "navigation-ins",
        "subcategory": "紧组合",
        "markers": [],
        "stars_approx": 291,
    },
    {
        "name": "Loose-GNSS-IMU",
        "url": "https://github.com/aaronboda24/Loose-GNSS-IMU",
        "desc_zh": "GNSS 与 IMU 的松组合卡尔曼实现",
        "analysis_zh": "经典松组合示例：GNSS 位置/速度更新 IMU 捷联推算，代码结构直白，便于第一次跑通组合导航。适合课程实验与滤波器调参练习。没有紧组合伪距观测与视觉约束；进阶可转向 TightlyCoupledINSGNSS、imu_x_fusion 或 OB_GINS。",
        "language": "C++",
        "license": "MIT",
        "category": "navigation-ins",
        "subcategory": "GNSS/INS",
        "markers": [],
        "stars_approx": 187,
    },
    {
        "name": "ionex",
        "url": "https://github.com/gnss-lab/ionex",
        "desc_zh": "Python 读取 IONEX 电离层图文件",
        "analysis_zh": "gnss-lab 出品的轻量 IONEX 读入模块，把网格 TEC 图载入 Python 便于插值与绘图。做 GIM 对比、穿刺点改正或教学演示时很省事。不生成 GIM、不算 STEC；写 IONEX 或更高阶分析可看 nav-solutions/ionex（Rust）与 IonMap、rtcm2ionex 等配套工具。",
        "language": "Python",
        "license": "MIT",
        "category": "ionosphere",
        "subcategory": "IONEX/TEC图",
        "markers": ["core"],
        "stars_approx": 12,
    },
    {
        "name": "ionex-rs",
        "url": "https://github.com/nav-solutions/ionex",
        "desc_zh": "Rust 实现的 IONEX 解析与处理",
        "analysis_zh": "GeoRust/nav-solutions 生态下的 IONEX 库，强调类型安全与可嵌入 rinex-cli 一类工具链。适合已在 Rust GNSS 栈中处理格网电离层的人。Python 科研脚本更常直接用 gnss-lab/ionex；两者互补而非替代完整 GIM 建模软件。",
        "language": "Rust",
        "license": "MPL-2.0",
        "category": "ionosphere",
        "subcategory": "IONEX/TEC图",
        "markers": ["core"],
        "stars_approx": 7,
    },
    {
        "name": "RTPPP_B2b",
        "url": "https://github.com/floating0516/RTPPP_B2b",
        "desc_zh": "北斗 PPP-B2b 改正数解码与实时 PPP 接口",
        "analysis_zh": "解码北斗 PPP-B2b 广播的精密轨道钟差改正，带流解析、缓冲与完整性检查，便于接入实时 PPP 流水线。做 BDS-3 短报文 PPP 或接收机原型的人应优先看。仓库体量小、许可未标明，工程化与多系统融合仍需自补；可与 PRIDE/Ginan/RTKLIB 实时分支对照改正数接口。",
        "language": "C",
        "license": "",
        "category": "gnss-positioning",
        "subcategory": "PPP",
        "markers": ["core"],
        "stars_approx": 10,
    },
    {
        "name": "ntripclient",
        "url": "https://github.com/nunojpg/ntripclient",
        "desc_zh": "NTRIP 2.0 命令行客户端",
        "analysis_zh": "精简的 NTRIP v2 命令行客户端，适合在嵌入式 Linux 或脚本里拉取差分流。运维与 DIY 基准站场景常见。功能止于传输层，不含 GUI 与 PPP；同作者还有 ntripserver、rtcm3torinex，可与 BNC、pygnssutils 对照选型。",
        "language": "C",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 129,
    },
    {
        "name": "pylgrim",
        "url": "https://github.com/kirienko/pylgrim",
        "desc_zh": "Python 编写的 GNSS 软件接收机",
        "analysis_zh": "用 Python 实现软件接收机链路，并触及 RINEX/IONEX/VMF1 等接口，便于阅读捕获跟踪流程。适合 SDR/GNSS 课程与原型。实时性能与多星座完备性远不及 gnss-sdr、FGI-GSRx；研究级信号仿真请配合 gps-sdr-sim 等。",
        "language": "Python",
        "license": "GPL-3.0",
        "category": "gnss-sdr",
        "subcategory": "软件接收机",
        "markers": [],
        "stars_approx": 21,
    },
    {
        "name": "GRID",
        "url": "https://github.com/mmurrian/GRID",
        "desc_zh": "灵活可扩展的 GNSS/GPS 软件定义接收机",
        "analysis_zh": "定位为成熟、可配置的 GNSS SDR 框架，强调模块灵活。适合已有 SDR 经验、想换一套接收机架构做实验的人。公开星标与文档相对少，上手成本高；主流对比对象仍是 gnss-sdr 与 GNSS-SDRLIB。",
        "language": "",
        "license": "",
        "category": "gnss-sdr",
        "subcategory": "软件接收机",
        "markers": [],
        "stars_approx": 4,
    },
    {
        "name": "SoftGNSS-python",
        "url": "https://github.com/perrysou/SoftGNSS-python",
        "desc_zh": "经典 SoftGNSS 的 Python 移植工具包",
        "analysis_zh": "把教学经典 SoftGNSS 思路迁到 Python，降低 MATLAB 门槛，便于改捕获跟踪实验。适合课堂与自学 SDR。功能深度与实时性不如 gnss-sdr；许可未标明，商用前需自行确认代码来源与授权。",
        "language": "Python",
        "license": "",
        "category": "gnss-sdr",
        "subcategory": "软件接收机",
        "markers": [],
        "stars_approx": 44,
    },
    {
        "name": "ionosphere-plotting",
        "url": "https://github.com/arwildo/ionosphere-plotting",
        "desc_zh": "TEC、foF2 与 DST 等指数的绘图脚本",
        "analysis_zh": "面向电离层指数与 TEC 时间序列的 Python 绑图工具，适合快速出教学图或报告插图。研究级 GIM/STEC 重建请用 gnss-tec、MosGIM2、SH-GIM；本仓库偏可视化，许可与数据接口需自备。",
        "language": "Python",
        "license": "",
        "category": "ionosphere",
        "subcategory": "电离层工具",
        "markers": [],
        "stars_approx": 7,
    },
    {
        "name": "rtcm2ionex",
        "url": "https://github.com/d-roma/rtcm2ionex",
        "desc_zh": "将 RTCM VTEC 消息转为 IONEX",
        "analysis_zh": "把实时 RTCM 垂直 TEC 类消息写成 IONEX 格网文件，便于与事后 GIM 工具链对接。做实时电离层流试验或把 NTRIP 电离层产品落地存档时有用。星标少、场景窄，不替代双频 STEC 估计或球谐 GIM 建模。",
        "language": "Python",
        "license": "GPL-3.0",
        "category": "ionosphere",
        "subcategory": "IONEX/TEC图",
        "markers": [],
        "stars_approx": 3,
    },
    {
        "name": "SegmentsComputation",
        "url": "https://github.com/yujieqing/SegmentsComputation",
        "desc_zh": "体素电离层层析中的射线段矩阵计算",
        "analysis_zh": "专注层析反演里体素穿越段（segment）几何矩阵的算法实现，是三维电子密度反演的前置数值模块。做 GNSS 层析的研究者可直接复用或对照。不是完整层析软件，需自备观测方程与正则化；可与 IonoTomo、synthetic 层析仓库搭配。",
        "language": "C++",
        "license": "",
        "category": "ionosphere",
        "subcategory": "层析",
        "markers": [],
        "stars_approx": 0,
    },
    {
        "name": "RTK-Visual-Inertial-Navigation",
        "url": "https://github.com/xiaohong-huang/RTK-Visual-Inertial-Navigation",
        "desc_zh": "滑窗滤波框架下的 RTK 视觉惯性导航",
        "analysis_zh": "在滑窗滤波里融合 RTK/DGNSS 与视觉惯性，面向高精度户外机器人与自动驾驶实验。适合已有 VIO 基础、想引入载波相位差分的团队。测地网 RTK 服务与模糊度完好性监测非其主场；可与 GVINS、gici-open 比较紧耦合策略。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "navigation-ins",
        "subcategory": "GNSS/INS/视觉",
        "markers": [],
        "stars_approx": 136,
    },
    {
        "name": "nav_matlab",
        "url": "https://github.com/yandld/nav_matlab",
        "desc_zh": "MATLAB 导航科学计算与组合导航例程",
        "analysis_zh": "汇总惯导、GNSS 与 UWB-IMU 等导航算法的 MATLAB 库，改公式方便，中文用户较多。适合教学演示与快速原型。实时嵌入式与大规模数据工程需移植；与 GINav、TightlyCoupledINSGNSS 等同属 MATLAB 组合导航学习线。",
        "language": "MATLAB",
        "license": "",
        "category": "navigation-ins",
        "subcategory": "INS工具包",
        "markers": [],
        "stars_approx": 276,
    },
    {
        "name": "satpulse",
        "url": "https://github.com/jclark/satpulse",
        "desc_zh": "跨平台 GNSS 授时、定位与接收机配置 GUI",
        "analysis_zh": "Go 实现的 GNSS 工具，强调 PPS/PTP/NTP 授时、RINEX/RTCM 与接收机评估配置，可在树莓派等设备上做时间同步。适合时间服务器与精密授时爱好者。不是测地 PPP 引擎；差分与 RTK 能力取决于所接接收机与 NTRIP，可与 bluetooth_gnss、GNSSTimeServer 对照场景。",
        "language": "Go",
        "license": "MIT",
        "category": "mobile-apps",
        "subcategory": "嵌入式",
        "markers": [],
        "stars_approx": 63,
    },
    {
        "name": "IonMap",
        "url": "https://github.com/Jin-Whu/IonMap",
        "desc_zh": "由 IONEX 绘制电离层 TEC 地图",
        "analysis_zh": "读取 IONEX 并绘制电离层图，适合论文插图与课程展示全球/区域 VTEC。功能集中在可视化，不估计 STEC、不做球谐建模；与 gnss-lab/ionex、ionosphere-plotting、SH-GIM 输出对照使用更完整。",
        "language": "Python",
        "license": "",
        "category": "ionosphere",
        "subcategory": "IONEX/TEC图",
        "markers": [],
        "stars_approx": 4,
    },
    {
        "name": "ionex-downloader",
        "url": "https://github.com/ohm1122/ionex-downloader",
        "desc_zh": "批量下载 IONEX/GIM 产品的脚本",
        "analysis_zh": "批处理拉取 IONEX（GIM）文件的小工具，减少手工下 IGS/分析中心产品的重复劳动。适合电离层课题的数据准备阶段。维护活跃度与镜像源覆盖有限，生产流水线更常见用 wget/aria2 或 FAST 等综合下载器。",
        "language": "",
        "license": "",
        "category": "ionosphere",
        "subcategory": "电离层工具",
        "markers": [],
        "stars_approx": 1,
    },
    {
        "name": "Nequick-ITUR",
        "url": "https://github.com/tpl2go/Nequick-ITUR",
        "desc_zh": "ITU-R NeQuick 2 的 Python 封装",
        "analysis_zh": "为 ITU-R NeQuick 2 Fortran 核心提供 Python 包装，便于在脚本里调用气候学电离层模型。做链路预算、单频改正对比或与 GNSS TEC 对照时有用。与 Galileo 专用 NeQuick-G（NequickG）不同标准版本，数值对齐要用官方算例；亦可对照 PyIRI/iri2016。",
        "language": "Fortran",
        "license": "",
        "category": "ionosphere",
        "subcategory": "IRI/NeQuick",
        "markers": [],
        "stars_approx": 4,
    },
    {
        "name": "IonoTomo",
        "url": "https://github.com/Joshuaalbert/IonoTomo",
        "desc_zh": "射电天文射线追踪与电离层层析仿真",
        "analysis_zh": "结合射线追踪与射电观测仿真做电离层层析，面向射电天文与空间天气交叉课题。适合需要正演电离层对射电信号影响的人。不是 GNSS 双频 TEC 业务软件；GNSS 体素层析可并行参考 SegmentsComputation 与 synthetic 层析仓库。",
        "language": "Jupyter Notebook",
        "license": "Apache-2.0",
        "category": "ionosphere",
        "subcategory": "层析",
        "markers": [],
        "stars_approx": 11,
    },
    {
        "name": "READ_GNSS",
        "url": "https://github.com/dzd9798/READ_GNSS",
        "desc_zh": "MATLAB 读取多种 GNSS 文件（含 RINEX/IONEX）",
        "analysis_zh": "在 MATLAB 中读入常见 GNSS 相关文件格式，降低自写解析的成本，方便后续 TEC 或定位实验。适合已有 MATLAB 工作流的学生课题组。功能广度与健壮性不如 georinex/gnsstk；大型工程建议仍用专门 IO 库。",
        "language": "MATLAB",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RINEX读写",
        "markers": [],
        "stars_approx": 10,
    },
    {
        "name": "ionex-analyzer",
        "url": "https://github.com/matador96/ionex-analyzer",
        "desc_zh": "Electron/React 的 IONEX 可视化毕业作品",
        "analysis_zh": "用桌面 Web 技术展示 IONEX 数据的可视化小应用，交互展示友好。适合演示与教学浏览格网 TEC。研究级批处理、插值与建模请回到 Python/MATLAB 工具链；仓库星标低，当作原型即可。",
        "language": "JavaScript",
        "license": "",
        "category": "ionosphere",
        "subcategory": "IONEX/TEC图",
        "markers": [],
        "stars_approx": 0,
    },
    {
        "name": "cors-relay",
        "url": "https://github.com/tisyang/cors-relay",
        "desc_zh": "CORS/NTRIP 差分流中继与重分发",
        "analysis_zh": "把 CORS 差分数据中继再分发的 C 程序，基于 libev，常见于对接千寻等源并自建内网 caster 的场景。运维本地 RTK 网络时很实用。不是完整商业 caster 套件，权限、计费与高可用需自建；可与 ybzwyrcld/ntrip、BNC 对照。",
        "language": "C",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 49,
    },
    {
        "name": "bluetooth_gnss",
        "url": "https://github.com/ykasidit/bluetooth_gnss",
        "desc_zh": "Android 蓝牙外接 GNSS/RTK 与 NTRIP 应用",
        "analysis_zh": "通过蓝牙连接外置接收机，在 Android 上使用 NTRIP 做 RTK/差分，已上架应用商店，野外测绘与兴趣玩家常用。适合手机+蓝牙接收机的移动作业。不是原始测量科研 Logger（见 GPSTest/gps-measurement-tools），精密测地仍取决于外置设备与服务。",
        "language": "Java",
        "license": "GPL-2.0",
        "category": "mobile-apps",
        "subcategory": "Android",
        "markers": [],
        "stars_approx": 123,
    },
    {
        "name": "ntrip-go",
        "url": "https://github.com/go-gnss/ntrip",
        "desc_zh": "Go 语言 NTRIP 客户端与服务端库",
        "analysis_zh": "用 Go 实现 NTRIP 客户端/服务端能力，便于嵌入云原生或高并发转发服务。适合要用单一语言栈做差分流网关的人。协议覆盖与运维工具不如 BNC 成熟；与 ybzwyrcld/ntrip、nunojpg 系列可按语言生态选型。",
        "language": "Go",
        "license": "Apache-2.0",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 62,
    },
    {
        "name": "ntrip-cpp",
        "url": "https://github.com/ybzwyrcld/ntrip",
        "desc_zh": "NTRIP 2.0 的 C++ caster/client/server 示例",
        "analysis_zh": "提供 NTRIP2.0 协议下 caster、客户端与服务端示例，星标较高，适合嵌入 C++ 服务或学习握手与挂载点逻辑。适合二次开发差分转发。完整鉴权、集群与监控需自增；Python/Go 生态另有 pygnssutils 与 go-gnss/ntrip。",
        "language": "C++",
        "license": "MIT",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 177,
    },
    {
        "name": "CDAAC_COSMIC-TEC_Data-Research",
        "url": "https://github.com/haoINvinCbou/CDAAC_COSMIC-TEC_Data-Research",
        "desc_zh": "处理 CDAAC COSMIC 掩星 NetCDF 做 TEC 研究",
        "analysis_zh": "Jupyter 流程读取 CDAAC/COSMIC 掩星 NetCDF，面向 TEC 与掩星电离层研究。做 GNSS-RO 与空基 TEC 的人可作起点。不是地基双频 TEC 或 GIM 软件；数据版本与产品字段需对照 CDAAC 文档。",
        "language": "Jupyter Notebook",
        "license": "",
        "category": "ionosphere",
        "subcategory": "TEC估计",
        "markers": [],
        "stars_approx": 2,
    },
    {
        "name": "synthetic_ionospheric_tomography_isl",
        "url": "https://github.com/suixin11suoyu/synthetic_ionospheric_tomography_isl",
        "desc_zh": "多 GNSS 星间链路辅助电离层层析仿真",
        "analysis_zh": "仿真多 GNSS 星间链路（ISL）辅助的电离层层析，探索新观测几何对电子密度反演的贡献。适合读相关论文后复现实验设置。公开星标低、偏研究原型，落地需自备真实 ISL/地基数据接口。",
        "language": "",
        "license": "",
        "category": "ionosphere",
        "subcategory": "层析",
        "markers": [],
        "stars_approx": 2,
    },
    {
        "name": "GVINS-Dataset",
        "url": "https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset",
        "desc_zh": "视觉/惯性/GNSS 原始测量同步数据集",
        "analysis_zh": "与 GVINS 配套的同步视觉、IMU 与 GNSS 原始测量数据，方便复现紧耦合实验与对比算法。做 GNSS-VIO 的标准测试集之一。本身不含完整解算器；处理请配合 GVINS、gnss_comm、ublox_driver。许可为 NOASSERTION，使用前阅读仓库说明。",
        "language": "C++",
        "license": "NOASSERTION",
        "category": "navigation-ins",
        "subcategory": "数据集",
        "markers": [],
        "stars_approx": 262,
    },
    {
        "name": "rtcm3torinex",
        "url": "https://github.com/nunojpg/rtcm3torinex",
        "desc_zh": "实时把 NTRIP RTCM3 流转成 RINEX",
        "analysis_zh": "从 NTRIP 拉取 RTCM3 并实时写成 RINEX，便于把差分流沉淀为事后可处理观测。野外部署与流归档场景实用。转换完整性依赖 RTCM 消息类型，复杂 MSM/多星座细节需实测；可与 BNC、RTKLIB 转换工具对照。",
        "language": "C",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RINEX转换",
        "markers": [],
        "stars_approx": 65,
    },
    {
        "name": "ntripserver",
        "url": "https://github.com/nunojpg/ntripserver",
        "desc_zh": "NTRIP 2.0 命令行服务端",
        "analysis_zh": "轻量 NTRIP v2 服务端，把本地串口或流发布为挂载点，常与 ntripclient 成对出现。适合单站发布与嵌入式 caster。高并发、用户管理与安全加固不如专用商业/开源 caster；大规模转发可看 cors-relay 或 ybzwyrcld/ntrip。",
        "language": "C",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "markers": [],
        "stars_approx": 74,
    },
    # ---- extras from additional gh searches ----
    {
        "name": "Net_Diff",
        "url": "https://github.com/YizeZhang/Net_Diff",
        "desc_zh": "GNSS 数据下载、定位解算与结果分析套件",
        "analysis_zh": "张一泽等维护的综合工具：覆盖产品下载、多种定位模式与结果分析，中文资料与用户基础较好。适合教学演示和中小规模科研试验。相对 PRIDE-PPPAR/Ginan 等，源码开放形态与工程依赖需按仓库说明核对；大规模业务化 PPP-AR 仍建议对照专用引擎。",
        "language": "HTML",
        "license": "",
        "category": "gnss-positioning",
        "subcategory": "定位软件",
        "markers": [],
        "stars_approx": 178,
    },
    {
        "name": "GREAT-IFCB",
        "url": "https://github.com/GREAT-WHU/GREAT-IFCB",
        "desc_zh": "多 GNSS 频间钟差（IFCB）估计开源软件",
        "analysis_zh": "武大 GREAT 组开源的多星座频间钟差估计工具，服务于精密钟差/偏差产品链路，与 GREAT-PVT 等同一研究线。做三频 PPP、相位偏差与钟差产品的人应关注。独立小工具，不替代完整 POD 套件；轨道与 UPD/OSB 仍多见诸 Ginan/PRIDE/GROOPS。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "orbit-clock",
        "subcategory": "钟差/轨道/UPD",
        "markers": [],
        "stars_approx": 15,
    },
    {
        "name": "GAMPII-GOOD",
        "url": "https://github.com/zhouforme0318/GAMPII-GOOD",
        "desc_zh": "GOOD：GNSS 观测与产品下载器（GAMP II 配套）",
        "analysis_zh": "面向 GNSS 观测值与精密产品的批量下载工具，常与 GAMP/PPP 研究流程一起使用，星标较高。适合搭数据处理流水线的前半段。定位解算请接 GAMP_PPPH、PRIDE 或 RTKLIB；镜像源与断点续传策略需按网络环境自测，也可对照 FAST。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "gnss-data",
        "subcategory": "下载",
        "markers": [],
        "stars_approx": 123,
    },
    {
        "name": "DRCycleSlip",
        "url": "https://github.com/Jin-Whu/DRCycleSlip",
        "desc_zh": "周跳探测与修复的 Python 实现",
        "analysis_zh": "提供 GNSS 周跳探测与修复相关脚本，便于在预处理阶段清理相位观测。适合教学和小数据试验。算法完备性与多星座鲁棒性有限，生产 QC 更常见 Anubis 或自研规则；可与 embrace-inpe/cycle-slip-correction 对照方法。",
        "language": "Python",
        "license": "",
        "category": "gnss-data",
        "subcategory": "周跳",
        "markers": [],
        "stars_approx": 4,
    },
    {
        "name": "PPPH-UAV",
        "url": "https://github.com/BerkayBahadur/PPPH-UAV",
        "desc_zh": "面向无人机摄影测量的 GNSS PPP 处理（MATLAB）",
        "analysis_zh": "在 PPPH 思路上处理无人机原始 GNSS，服务摄影测量轨迹与产品生成，MATLAB 实现便于改流程。做 UAV 测图轨迹增强时可作参考。通用多星座 PPP-AR 与实时能力不如 PRIDE/Ginan；许可未标明，使用前请阅读仓库说明。",
        "language": "MATLAB",
        "license": "",
        "category": "gnss-positioning",
        "subcategory": "PPP",
        "markers": [],
        "stars_approx": 14,
    },
]


def marker_label(p):
    parts = []
    m = p.get("markers") or []
    if "owned" in m:
        parts.append("🚩 自有")
    if "fork" in m:
        parts.append("🔀 Fork")
    if "starred" in m:
        parts.append("★ Star")
    if "core" in m:
        parts.append("核心")
    return " · ".join(parts)


def stars_cell(p):
    s = p.get("stars_approx")
    if s is None or s == "" or s == 0 and p.get("name") not in ("SegmentsComputation", "ionex-analyzer"):
        # show 0 for known zeros; show — for missing
        if s == 0:
            return "0"
        if s is None or s == "":
            return "—"
    if s is None:
        return "—"
    return str(s)


def lang_cell(p):
    return p.get("language") or "—"


def license_cell(p):
    lic = p.get("license") or ""
    return lic if lic else None


def finalize_entry(e):
    out = {
        "name": e["name"],
        "url": e["url"],
        "desc_zh": e["desc_zh"],
        "analysis_zh": e["analysis_zh"],
        "language": e.get("language") or "",
        "license": e.get("license") or "",
        "category": e["category"],
        "subcategory": e["subcategory"],
        "markers": e.get("markers") or [],
        "stars_approx": e.get("stars_approx"),
        "source": "gh-search+verified (missing_meta / extra searches)",
        "featured": False,
        "user_relation": "none",
    }
    return out


def sort_projects(projects):
    # Keep SH-GIM first within ionosphere; otherwise sort by stars desc within category groups when regenerating lists.
    # For PROJECTS.json preserve: existing order, then append new.
    return projects


def regenerate_lists(projects):
    by_cat = defaultdict(list)
    for p in projects:
        by_cat[p["category"]].append(p)

    for cat in CAT_ORDER:
        meta = CAT_META[cat]
        items = by_cat.get(cat, [])
        # subcategory order: first-seen order preferring higher stars within subcat
        sub_order = []
        sub_map = OrderedDict()
        for p in items:
            sc = p.get("subcategory") or "其他"
            if sc not in sub_map:
                sub_map[sc] = []
                sub_order.append(sc)
            sub_map[sc].append(p)
        for sc in sub_order:
            sub_map[sc].sort(key=lambda x: (-(x.get("stars_approx") or 0), x["name"].lower()))
            # SH-GIM always first in its subcategory
            if cat == "ionosphere" and sc == "GIM/球谐映射":
                sub_map[sc].sort(key=lambda x: (0 if x["name"] == "SH-GIM" else 1, -(x.get("stars_approx") or 0), x["name"].lower()))

        lines = []
        lines.append(f"# {meta['title']}")
        lines.append(f"> **{len(items)}** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区")
        lines.append("")
        lines.append(meta["blurb"])
        lines.append("")

        for sc in sub_order:
            group = sub_map[sc]
            lines.append(f"## {sc}")
            lines.append("")
            lines.append("| 项目 | 一句话 | 语言 | ★ | 标记 |")
            lines.append("|---|---|---|---:|---|")
            for p in group:
                ml = marker_label(p)
                lines.append(
                    f"| [{p['name']}]({p['url']}) | {p['desc_zh']} | {lang_cell(p)} | {stars_cell(p)} | {ml} |"
                )
            lines.append("")
            lines.append("### 详细说明")
            lines.append("")
            for p in group:
                ml = marker_label(p)
                if ml:
                    lines.append(f"#### [{p['name']}]({p['url']})  ")
                    lines.append(f"*{ml}*")
                else:
                    lines.append(f"#### [{p['name']}]({p['url']})")
                lines.append("")
                bits = [f"语言：{lang_cell(p)}"]
                lic = license_cell(p)
                if lic:
                    bits.append(f"许可：{lic}")
                st = p.get("stars_approx")
                if st is not None and st != "":
                    bits.append(f"星标约：{st}")
                lines.append(" · ".join(bits))
                lines.append("")
                lines.append(p["analysis_zh"])
                lines.append("")
            lines.append("")

        path = ROOT / "lists" / meta["file"]
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def readme_preview_rows(projects, cat, limit=7):
    items = [p for p in projects if p["category"] == cat]
    # prioritize: featured, core, then stars
    def key(p):
        return (
            0 if p.get("featured") else 1,
            0 if "core" in (p.get("markers") or []) else 1,
            0 if "owned" in (p.get("markers") or []) else 1,
            -(p.get("stars_approx") or 0),
        )
    items = sorted(items, key=key)
    # SH-GIM first for ionosphere
    if cat == "ionosphere":
        items = sorted(items, key=lambda p: (0 if p["name"] == "SH-GIM" else 1, key(p)[1], key(p)[2], key(p)[3]))
    return items[:limit]


def regenerate_readme(projects, counts):
    total = len(projects)
    lines = []
    lines.append("# Ionosphere-GNSS-OpenSource")
    lines.append("")
    lines.append("**电离层 · 对流层 · GNSS · 导航（PNT）开源软件精选索引**  ")
    lines.append("Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation")
    lines.append("")
    lines.append(f"[![Projects](https://img.shields.io/badge/verified%20projects-{total}-blue.svg)](./PROJECTS.json)")
    lines.append("[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)")
    lines.append("")
    lines.append("> **这是链接索引（curated index），不是代码大合集。**  ")
    lines.append("> 所有条目均为已核对的公开 URL；需要时请前往**上游仓库**克隆并遵守其许可证。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 亮点：自有项目 SH-GIM")
    lines.append("")
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append("| **项目** | [Atlas2001-web/SH-GIM](https://github.com/Atlas2001-web/SH-GIM) |")
    lines.append("| **一句话** | 基于球谐展开的全球电离层映射（GIM）MATLAB 源码 |")
    lines.append("| **语言 / 许可** | MATLAB · MIT |")
    lines.append("| **定位** | 本索引「电离层 / GIM」类别下的**旗舰自有项目** |")
    lines.append("")
    lines.append("从事 GIM / TEC 球谐建模时，建议优先阅读 SH-GIM，并对照 MosGIM2、PyTECGg、gnss-tec、tec-suite 与 IONEX 工具。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 如何使用")
    lines.append("")
    lines.append("1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  ")
    lines.append("2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  ")
    lines.append("3. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json) · 扩充研究稿：[`research/expanded_projects.json`](./research/expanded_projects.json)  ")
    lines.append("4. 克隆上游，不要把第三方源码拷进本仓库")
    lines.append("")
    lines.append("### 标记")
    lines.append("")
    lines.append("| 标记 | 含义 |")
    lines.append("|:---:|---|")
    lines.append("| 🚩 | Atlas2001-web 自有公开仓库 |")
    lines.append("| 🔀 | 维护者已 fork（表中列上游；fork 地址见项目页） |")
    lines.append("| ★ | 维护者 GitHub 星标种子 |")
    lines.append("| 核心 | 建议优先阅读 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 分类一览")
    lines.append("")
    lines.append("| 分类 | 适合谁 | 列表 | 数量 |")
    lines.append("|---|---|---|---:|")
    for cat in CAT_ORDER:
        m = CAT_META[cat]
        cn = m["title"].split(" / ")[0].replace("导航 / GNSS-INS", "导航 / GNSS-INS")
        # short name for table
        short = {
            "ionosphere": "**电离层** `ionosphere`",
            "troposphere": "**对流层** `troposphere`",
            "gnss-data": "**GNSS 数据与格式** `gnss-data`",
            "gnss-positioning": "**精密定位** `gnss-positioning`",
            "orbit-clock": "**轨道与钟差** `orbit-clock`",
            "navigation-ins": "**导航 / GNSS-INS** `navigation-ins`",
            "gnss-sdr": "**软件接收机与信号** `gnss-sdr`",
            "mobile-apps": "**移动与嵌入式应用** `mobile-apps`",
            "tools-learning": "**学习资源与工具** `tools-learning`",
        }[cat]
        lines.append(f"| {short} | {m['who']} | [{m['file']}](./lists/{m['file']}) | {counts[cat]} |")
    lines.append(f"| **合计** | | [`PROJECTS.json`](./PROJECTS.json) | **{total}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    section_heads = {
        "ionosphere": ("## 电离层 / Ionosphere", CAT_META["ionosphere"]["blurb"]),
        "troposphere": ("## 对流层 / Troposphere", CAT_META["troposphere"]["blurb"]),
        "gnss-data": ("## GNSS 数据与格式 / GNSS Data I/O", CAT_META["gnss-data"]["blurb"]),
        "gnss-positioning": ("## 精密定位 / Precise Positioning", CAT_META["gnss-positioning"]["blurb"]),
        "orbit-clock": ("## 轨道与钟差 / Orbit & Clock", "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。"),
        "navigation-ins": ("## 导航 / GNSS-INS / Navigation & INS", CAT_META["navigation-ins"]["blurb"]),
        "gnss-sdr": ("## 软件接收机与信号 / GNSS-SDR", CAT_META["gnss-sdr"]["blurb"]),
        "mobile-apps": ("## 移动与嵌入式应用 / Mobile Apps", CAT_META["mobile-apps"]["blurb"]),
        "tools-learning": ("## 学习资源与工具 / Learning & Tools", CAT_META["tools-learning"]["blurb"]),
    }

    for cat in CAT_ORDER:
        head, blurb = section_heads[cat]
        m = CAT_META[cat]
        lines.append(head)
        lines.append("")
        lines.append(blurb)
        lines.append("")
        lines.append(f"完整列表与逐项分析 → [{m['file']}](./lists/{m['file']})")
        lines.append("")
        lines.append("| 项目 | 简介 | 标记 |")
        lines.append("|---|---|---|")
        for p in readme_preview_rows(projects, cat):
            ml = marker_label(p)
            lines.append(f"| [{p['name']}]({p['url']}) | {p['desc_zh']} | {ml} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 与 Atlas2001-web 的关系")
    lines.append("")
    lines.append("- 🚩 **[SH-GIM](https://github.com/Atlas2001-web/SH-GIM)**：自有旗舰（GIM）")
    lines.append("- 🔀 Fork：[PyTECGg](https://github.com/viventriglia/PyTECGg) → [Atlas2001-web/PyTECGg](https://github.com/Atlas2001-web/PyTECGg)；[georinex](https://github.com/geospace-code/georinex) → [Atlas2001-web/georinex](https://github.com/Atlas2001-web/georinex)")
    lines.append("- ★ 大量电离层/GNSS 星标已作为种子纳入")
    lines.append("- 私有 `SH-GIM-proprietary` **不收录**")
    lines.append("")
    lines.append("## 仓库结构")
    lines.append("")
    lines.append("```")
    lines.append("Ionosphere-GNSS-OpenSource/")
    lines.append("├── README.md")
    lines.append("├── PROJECTS.json")
    lines.append("├── NOTES.md / CONTRIBUTING.md")
    lines.append("├── docs/categories.md")
    lines.append("├── lists/01–09-*.md")
    lines.append("└── research/")
    lines.append("    ├── expanded_projects.json")
    lines.append("    ├── category_plan.md")
    lines.append("    ├── missing_meta.json")
    lines.append("    └── new_finds.json")
    lines.append("```")
    lines.append("")
    lines.append("## 贡献")
    lines.append("")
    lines.append("见 [CONTRIBUTING.md](./CONTRIBUTING.md)。提交新链接前请确认上游可公开访问，并写清分类与一句话用途。")
    lines.append("")
    lines.append("## 免责声明")
    lines.append("")
    lines.append("本目录仅供信息汇总，不构成对任何项目的背书。无线电信号仿真与发射请遵守当地法规。使用第三方软件的风险由用户自行承担。")
    lines.append("")

    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def update_categories_md(counts):
    path = ROOT / "docs" / "categories.md"
    text = path.read_text(encoding="utf-8")
    # update counts in place
    import re
    mapping = {
        "ionosphere": counts["ionosphere"],
        "troposphere": counts["troposphere"],
        "gnss-data": counts["gnss-data"],
        "gnss-positioning": counts["gnss-positioning"],
        "orbit-clock": counts["orbit-clock"],
        "navigation-ins": counts["navigation-ins"],
        "gnss-sdr": counts["gnss-sdr"],
        "mobile-apps": counts["mobile-apps"],
        "tools-learning": counts["tools-learning"],
    }
    for cat, n in mapping.items():
        text = re.sub(
            rf"(## `{cat}`[\s\S]*?- 当前条目数：\*\*)\d+(\*\*)",
            rf"\g<1>{n}\2",
            text,
            count=1,
        )
    path.write_text(text, encoding="utf-8")


def main():
    with open(ROOT / "PROJECTS.json", encoding="utf-8") as f:
        cat = json.load(f)
    existing_urls = {p["url"].rstrip("/").lower() for p in cat["projects"]}

    added = []
    for raw in NEW_ENTRIES:
        e = finalize_entry(raw)
        u = e["url"].rstrip("/").lower()
        if u in existing_urls:
            print("SKIP dup", e["name"], e["url"])
            continue
        # analysis length check
        nchars = len(e["analysis_zh"])
        if nchars < 150 or nchars > 300:
            print(f"WARN length {e['name']}: {nchars}")
        cat["projects"].append(e)
        existing_urls.add(u)
        added.append(e)

    from collections import Counter as _Counter
    counts = _Counter(p["category"] for p in cat["projects"])
    cat["project_count"] = len(cat["projects"])
    cat["counts_by_category"] = {k: counts[k] for k in CAT_ORDER}
    cat["generated"] = "2026-09-14"

    with open(ROOT / "PROJECTS.json", "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(ROOT / "research" / "new_finds.json", "w", encoding="utf-8") as f:
        json.dump(added, f, ensure_ascii=False, indent=2)
        f.write("\n")

    regenerate_lists(cat["projects"])
    regenerate_readme(cat["projects"], cat["counts_by_category"])
    update_categories_md(cat["counts_by_category"])

    # update NOTES lightly
    notes = ROOT / "NOTES.md"
    notes.write_text(
        notes.read_text(encoding="utf-8").rstrip()
        + f"\n\n## 增量合并（2026-09-14）\n\n"
        + f"- 自 `research/missing_meta.json` 与补充 gh 检索合并新增 **{len(added)}** 条\n"
        + f"- 当前条目：**{cat['project_count']}**\n"
        + f"- 分类计数：{dict(cat['counts_by_category'])}\n"
        + f"- 详见 `research/new_finds.json`\n",
        encoding="utf-8",
    )

    print("ADDED", len(added))
    print("TOTAL", cat["project_count"])
    print("COUNTS", cat["counts_by_category"])
    for a in added:
        print(f"  + {a['name']:40s} {a['category']:18s} stars={a['stars_approx']} markers={a['markers']} len={len(a['analysis_zh'])}")


if __name__ == "__main__":
    main()
