# 对流层 / Troposphere
> 共 **22** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。

## GNSS气象/PWV

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS) | GPS 可降水量（PWV）分析与 ML 应用工具 | Python | 22 | 🏷️ 个人社区 |

### 详细说明

#### [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：22 · 宿主：github

从 GPS 相关产品做可降水量分析，并带机器学习应用示例。适合 GNSS 气象入门与区域 PWV 研究。从原始 RINEX 到 ZWD 的完整 PPP 链需另接 PRIDE/Ginan 等。

## VMF/GGOS产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products) | 基于 GGOS/VMF 产品在 RTKLIB 中解算对流层延迟 | C | 43 | 🏷️ 个人社区 |

### 详细说明

#### [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：43 · 宿主：github

在 RTKLIB 二次开发中接入 GGOS/VMF 格网做对流层延迟，带较详细中文编译笔记。适合 Windows/VS 环境下改 RTKLIB 学 VMF。作者亦说明与官方 MATLAB 参考存在数值差，科研前应用官方码交叉验证。

## VMF/GPT官方代码

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes) | TU Wien 官方 VMF1/VMF3/GPT/GMF 源码与格网目录 | Fortran/MATLAB/C++ | — | 🏷️ 官方 · 核心 |
| [VMF-TUWien-Home](https://vmf.geo.tuwien.ac.at/) | TU Wien VMF 主页：对流层映射函数产品与代码入口 | Fortran/MATLAB | — | 🏷️ 官方 |

### 详细说明

#### [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes)  
*🏷️ 官方 · 核心*

语言：Fortran/MATLAB/C++ · 许可：TU Wien site terms · 星标约：— · 宿主：official_site

维也纳工大公开的 VMF1/VMF3、GPT/GPT2w/GPT3、GMF、Saastamoinen 等 Fortran/MATLAB/C++ 实现与格网文件，是对流层映射与气象先验的权威入口。目录持续更新（含 vmf3_grid 等）。预报产品获取常需遵循站点注册要求；可与 STD_SWD_Calc 等脚本联用。

#### [VMF-TUWien-Home](https://vmf.geo.tuwien.ac.at/)  
*🏷️ 官方*

语言：Fortran/MATLAB · 许可：TU Wien terms · 星标约：— · 宿主：official_site

维也纳工大 VMF 服务门户，说明 VMF1/VMF3 格网产品与 GPT 系列气象模型，并链到 /codes 开源实现。PPP/VLBI 对流层延迟建模的权威数据与代码源头。格网下载常需遵循站点条款；具体源码文件见 codes 目录条目，勿与第三方拷贝混淆。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## ZTD/ZWD/VMF

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc) | 由 GPT/VMF 等计算 GNSS STD/SWD 与模型 ZTD | Python | 10 | 🏷️ 个人社区 · 核心 |

### 详细说明

#### [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc)  
*🏷️ 个人社区 · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：10 · 宿主：github

Python 包生成斜路径干/湿延迟（STD/SWD）以及基于 GPT/VMF 的模型 ZTD，直接对接维也纳映射函数生态。适合 GNSS 气象、PPP 先验对流层、与实测 ZTD 对比。站点元数据与 VMF 格网下载要自己准备；业务化连续运行需另写调度。

## 反射测量

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS) | TechDemoSat-1 GNSS-R 数据处理示例（SSTL） | MATLAB | 34 | 🏷️ 个人社区 |
| [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3) | GNSS-IR 反射测量 MATLAB 工具（Larson 实验室） | MATLAB | 30 | 🏷️ 高校实验室 |
| [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python) | GNSS-IR 反射测量 Python 脚本（Larson） | Python | 26 | 🏷️ 高校实验室 |
| [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost) | 低成本 GNSS 反射测量分析（MATLAB/Python） | MATLAB | 14 | 🏷️ 个人社区 |
| [gnssr-synth](https://github.com/purnelldj/gnssr_synth) | GNSS-R 水位观测分析与合成 SNR 数据 | MATLAB | 11 | 🏷️ 个人社区 |

### 详细说明

#### [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：30 · 宿主：github

Kristine Larson 团队发布的 GNSS 干涉反射（GNSS-IR）MATLAB 新版，用信噪比（SNR）随高度角振荡反演反射面高度，常用于水位、雪深与土壤湿度。面向已有 MATLAB 流程的地球物理与大地测量用户。边界是反射测高/环境遥感，不做对流层 ZTD；Python 产线请优先对照同作者持续维护的 gnssrefl，本仓库更偏 MATLAB 用户留存版本。

#### [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：26 · 宿主：github

Larson 实验室较早的 GNSS-IR Python 脚本集，从 GNSS 观测提取 SNR 干涉条纹并估计反射器高度，服务水位与地表环境监测。适合想在纯脚本环境快速试验 GNSS-IR 的研究者。工程化、命令行与多星座流程弱于现维护的 gnssrefl；新项目建议直接用 gnssrefl，本库可作算法对照或旧文复现。

#### [gnssr-synth](https://github.com/purnelldj/gnssr_synth)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：11 · 宿主：github

MATLAB 工具：获取并分析 GNSS-R 水位观测，同时可生成合成 SNR，便于方法试验、误差传播与教学演示。面向反射测高与水文监测研究者。侧重水位场景与合成数据，不是覆盖雪深/土壤湿度的完整 GNSS-IR 套件；低成本接收机路线可并读同作者 gnssr_lowcost，产线级处理仍常回 gnssrefl。

#### [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：14 · 宿主：github

面向低成本 GNSS 硬件的反射测量分析，同时给出 MATLAB 与 Python 路径，降低 GNSS-R/IR 入门与课程实验门槛。适合教学站与原型站网。测高精度与稳定性通常不及大地型天线+gnssrefl；使用前需核对天线相位中心、多路径几何与采样率是否满足干涉条纹分辨需求。场地开阔度与多路径环境会显著影响可用弧段长度。

#### [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：34 · 宿主：github

Surrey Satellite Technology 提供的 TechDemoSat-1（MERRByS）星载 GNSS-R 示例处理材料，演示空间反射数据的读取与初步产品步骤。面向星载 GNSS-R、海洋与地表遥感读者。这是任务示例而非通用地基 GNSS-IR 软件；地基水位/雪深请用 gnssrefl 等，两者观测几何与校正链不同。

## 反射测量/PWV相关

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | GNSS-IR：反射信号估水位/土壤湿度/雪深 | Python | 217 | 🏷️ 高校实验室 · 核心 |

### 详细说明

#### [gnssrefl](https://github.com/kristinemlarson/gnssrefl)  
*🏷️ 高校实验室 · 核心*

语言：Python · 许可：GPL-3.0 · 星标约：217 · 宿主：github

GNSS 干涉反射测量（GNSS-IR）主流开源工具，用反射信号估水位、土壤湿度、雪深等，也常与近地表环境/湿延迟研究相关。文档与 Docker 支持较好。定位解算不是目标；要 ZTD/PWV 主产品仍用 PPP+气象流程。

## 大气延迟/InSAR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyAPS](https://github.com/insarlab/PyAPS) | 基于全球大气模式的大气相位屏（APS） | Python | 86 | 🏷️ 高校实验室 |
| [ICAMS](https://github.com/ymcmrs/ICAMS) | 顾及对流层空间随机特性的 InSAR 大气改正工具箱 | Python | 44 | 🏷️ 高校实验室 |

### 详细说明

#### [ICAMS](https://github.com/ymcmrs/ICAMS)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：44 · 宿主：github

ICAMS 用全球大气模式做 InSAR 对流层改正，并考虑空间随机特性。适合高级 InSAR 大气研究。与 GNSS 单站 ZTD 流程接口需自行桥接。

#### [PyAPS](https://github.com/insarlab/PyAPS)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：86 · 宿主：github

用全球大气模式生成大气相位屏，服务 InSAR 对流层改正，思路与 GNSS 气象同源（湿延迟结构）。适合 InSAR+GNSS 联合的人理解三维湿延迟。不直接输出测站 ZTD 产品。

## 经验模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UNB3m](https://github.com/ohm1122/UNB3m) | UNB3m 中性大气延迟模型 | — | 3 | 🏷️ 个人社区 · ★ Star |

### 详细说明

#### [UNB3m](https://github.com/ohm1122/UNB3m)  
*🏷️ 个人社区 · ★ Star*

语言：— · 许可：— · 星标约：3 · 宿主：github

UNB 系列中性大气经验模型，无实测气象时给天顶延迟粗值。适合教学与低精度先验。精度不及 VMF+数值天气模式；精密 PPP 优先 VMF3/GPT3。

## 相似项目补录

| 项目 | 一句话 | ★ | 标记 |
|---|---|---:|---|
| [mphw](https://github.com/ufrgs-gnss-lab/mphw) | 低成本 GNSS-IR/反射测量开源硬件 | 25 | 🏷️ 高校实验室 |
| [GNSSR_MERRByS_Python](https://github.com/pjalesSSTL/GNSSR_MERRByS_Python) | TechDemoSat-1 星载 GNSS-R Python 示例 | 19 | 🏷️ 高校实验室 |
| [GNSS-REFLECTOMETRY-PROCESSING](https://github.com/oriolcervello/GNSS-REFLECTOMETRY-PROCESSING) | GPU 加速 GNSS-R 处理 | 17 | 🏷️ 个人社区 |
| [gnssr4river](https://github.com/lroineau/gnssr4river) | 面向河流水文的 GNSS-R Python 工具箱 | 8 | 🏷️ 个人社区 |
| [GNSS_RR](https://github.com/lasteine/GNSS_RR) | 雪面 GNSS 反射/折射连续估计 | 7 | 🏷️ 高校实验室 |
| [NearRealTimeGNSSIR](https://github.com/cemalialtuntas/NearRealTimeGNSSIR) | 近实时 GNSS-IR 软件原型 | 5 | 🏷️ 个人社区 |
| [gpssnrpy](https://github.com/kristinemlarson/gpssnrpy) | RINEX SNR 提取与高度角工具 | 6 | 🏷️ 高校实验室 |
| [DDM-Former](https://github.com/daixinzhao/DDM-Former) | GNSS-R DDM 海面风速 Transformer 模型 | 10 | 🏷️ 高校实验室 |

### 详细说明

#### [mphw](https://github.com/ufrgs-gnss-lab/mphw)
*🏷️ 高校实验室*

语言：MATLAB · 许可：NOASSERTION

开源低成本 GNSS-IR/反射测量硬件方案（MPHW），配合 SNR 反射测高。适合教学站与原型站网，降低进入 GNSS-R 的硬件门槛。精度受天线与场地多路径制约，科研级水位/雪深仍常对照 gnssrefl + 大地型天线。

#### [GNSSR_MERRByS_Python](https://github.com/pjalesSSTL/GNSSR_MERRByS_Python)
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：—

Surrey TechDemoSat-1（MERRByS）星载 GNSS-R 的 Python/Jupyter 示例，演示空间反射数据读取与初步处理。适合星载 GNSS-R 入门。地基 GNSS-IR 请用 gnssrefl；两者几何与校正链不同。

#### [GNSS-REFLECTOMETRY-PROCESSING](https://github.com/oriolcervello/GNSS-REFLECTOMETRY-PROCESSING)
*🏷️ 个人社区*

语言：Cuda · 许可：GPL-3.0

面向 GNSS 反射测量的 GPU/CUDA 处理实验代码，适合做吞吐或算法加速试验。硬件与驱动依赖重；业务流水线需自行封装 I/O 与质控。

#### [gnssr4river](https://github.com/lroineau/gnssr4river)
*🏷️ 个人社区*

语言：Python · 许可：—

开源 Python GNSS-R/IR 工具箱，偏向河流/水位等水文应用场景。适合把反射测高接到水文监测脚本。功能覆盖面小于 gnssrefl 全家桶，复杂站点仍建议用主流工具交叉检验。

#### [GNSS_RR](https://github.com/lasteine/GNSS_RR)
*🏷️ 高校实验室*

语言：Python · 许可：CC0-1.0

联合反射/折射（GNSS-RR）连续估计雪/粒雪累积、表面质量与密度的方法代码，面向冰冻圈监测。场景专一；通用水位 GNSS-IR 不是其主场。

#### [NearRealTimeGNSSIR](https://github.com/cemalialtuntas/NearRealTimeGNSSIR)
*🏷️ 个人社区*

语言：HTML · 许可：GPL-3.0

朝近实时 GNSS-IR 流水线努力的实现，目标从 SNR 提取水位/雪深/土壤湿度等环境参数。适合做自动化监测原型。工程完整度与多星座支持需实测，稳定产线可对照 gnssrefl。

#### [gpssnrpy](https://github.com/kristinemlarson/gpssnrpy)
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0

从 GPS RINEX 提取 SNR，并结合导航电文算高度角/方位角，还带下载辅助。常作为 GNSS-IR 前处理积木，与 gnssrefl 生态 complementary。

#### [DDM-Former](https://github.com/daixinzhao/DDM-Former)
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0

用 Transformer 从 GNSS-R DDM 估全球海面风速的研究代码（DDM-Former）。适合遥感/机器学习交叉读者。不是地基 GNSS-IR 工具，输入输出与传统 SNR 干涉测高不同。

