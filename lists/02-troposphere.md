# 对流层 / Troposphere
> **47** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区

中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

## 星载GNSS-R

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSR_MERRByS_Python](https://github.com/pjalesSSTL/GNSSR_MERRByS_Python) | GNSSR_MERRByS_Python：TechDemoSat-1 星载 GNSS-R 示例 | Jupyter Notebook | 19 | 🏷️ 高校实验室 |
| [DDM-Former](https://github.com/daixinzhao/DDM-Former) | DDM-Former：GNSS-R DDM 海面风速 Transformer | Python | 10 | 🏷️ 高校实验室 |

### 详细说明

#### [GNSSR_MERRByS_Python](https://github.com/pjalesSSTL/GNSSR_MERRByS_Python)  
*🏷️ 高校实验室*

语言：Jupyter Notebook · 许可：— · 星标约：19 · 宿主：github

Surrey TechDemoSat-1（MERRByS）星载 GNSS-R 的 Python/Jupyter 示例，演示空间反射数据读取与初步处理。适合星载 GNSS-R 入门。地基 GNSS-IR 请用 gnssrefl；两者几何与校正链不同。

#### [DDM-Former](https://github.com/daixinzhao/DDM-Former)  
*🏷️ 高校实验室*

语言：Python · 许可：Apache-2.0 · 星标约：10 · 宿主：github

用 Transformer 从 GNSS-R DDM 估全球海面风速的研究代码（DDM-Former）。适合遥感/机器学习交叉读者。不是地基 GNSS-IR 工具，输入输出与传统 SNR 干涉测高不同。

## GNSS气象/PWV

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [geodezyx](https://github.com/IPGP/geodezyx) | geodezyx：IPGP 大地测量/地球物理 Python 工具箱 | Python | 33 | 🏷️ 高校实验室 |
| [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS) | PW_from_GPS：GPS 可降水量（PWV）分析与 ML 工具 | Python | 22 | 🏷️ 个人社区 |
| [pwv_kpno](https://github.com/mwvgroup/pwv_kpno) | pwv_kpno：SuomiNet GPS PWV 驱动的透过率模型 | Python | 11 | 🏷️ 高校实验室 |
| [OpATOM](https://github.com/benceturak/GeoPack/tree/GPSTomographyToolbox/GPSTomographyToolbox) | OpATOM：BME GNSS 对流层湿折射率 MART 层析工具箱 | Python | 3 | 🏷️ 高校实验室 |
| [ATom-TUWien](https://github.com/GregorMoeller/ATom) | ATom-TUWien：GNSS 大气层析与湿折射率三维重建 | MATLAB | 2 | 🏷️ 高校实验室 |

### 详细说明

#### [geodezyx](https://github.com/IPGP/geodezyx)  
*🏷️ 高校实验室*

语言：Python · 许可：LGPL-3.0 · 星标约：33 · 宿主：github

巴黎地球物理研究所（IPGP）维护的 Python 大地测量/地球物理工具箱，大气模块可做 ZWD→PWV、GPT/VMF 相关接口调用。适合把 GNSS 气象量接到地球物理脚本。完整精密定位请另接专用引擎；网格文件与依赖版本需按文档准备。

#### [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：22 · 宿主：github

从 GPS 相关产品做可降水量分析，并带机器学习应用示例。适合 GNSS 气象入门与区域 PWV 研究。从原始 RINEX 到 ZWD 的完整 PPP 链需另接 PRIDE/Ginan 等。

#### [pwv_kpno](https://github.com/mwvgroup/pwv_kpno)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：11 · 宿主：github

用 SuomiNet 等 GPS 反演的 PWV 驱动 MODTRAN 类大气透过率，默认服务 Kitt Peak，也可扩展到其它站点。面向天文测光改正与 GNSS 气象交叉验证。不是从 RINEX 估 ZWD 的 PPP 引擎；站点扩展需配置与文献引用。

#### [OpATOM](https://github.com/benceturak/GeoPack/tree/GPSTomographyToolbox/GPSTomographyToolbox)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：3 · 宿主：github

BME 大地测量组发布的开源 Python 层析工具箱，由 ZWD/梯度、SP3、VMF1 网格重建三维湿折射率并可换算水汽密度，含 MART 迭代、粗差剔除与探空气球验证样例。适合近实时 GNSS 气象层析实验；输入偏 Bernese TRP/VMF1 工作流，区域尺度与体素设计需按研究区自调。用户指南见 gpsmet.geod.bme.hu。

#### [ATom-TUWien](https://github.com/GregorMoeller/ATom)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：GPL-3.0 · 星标约：2 · 宿主：github

维也纳工业大学 GNSS-ATom 项目的 MATLAB 层析软件，沿弯曲信号路径重建低层大气三维湿折射率，并支持广播星历→方位角、ZTD→斜延迟、数值天气模式与折射场互转。GPL-3。适合对流层层析方法教学；依赖 MATLAB GUI 与多种大地测量格式，不是实时业务系统。

## VMF/GGOS产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products) | GGOS-Tropo-RTKLIB：VMF 接入 RTKLIB 对流层 | C | 43 | 🏷️ 个人社区 |

### 详细说明

#### [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products)  
*🏷️ 个人社区*

语言：C · 许可：— · 星标约：43 · 宿主：github

在 RTKLIB 二次开发中接入 GGOS/VMF 格网做对流层延迟，带较详细中文编译笔记。适合 Windows/VS 环境下改 RTKLIB 学 VMF。作者亦说明与官方 MATLAB 参考存在数值差，科研前应用官方码交叉验证。

## GNSS-IR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssSNR](https://github.com/kristinemlarson/gnssSNR) | gnssSNR：RINEX→SNR/几何角，GNSS-IR 前置工具 | Fortran | 15 | 🏷️ 高校实验室 |
| [GIRAS-GPS-Solutions](https://github.com/cemalialtuntas/GIRAS-GPS-Solutions) | GIRAS：MATLAB 开源 GNSS-IR 分析（GPS Solutions 配套） | MATLAB | 13 | 🏷️ 高校实验室 |
| [FresnelMaps](https://github.com/kristinemlarson/FresnelMaps) | FresnelMaps：GNSS-IR 菲涅耳区地图生成工具 | Python | 9 | 🏷️ 高校实验室 |
| [gnssr4river](https://github.com/lroineau/gnssr4river) | gnssr4river：面向河流水文的 GNSS-R Python 工具箱 | Python | 8 | 🏷️ 高校实验室 |
| [gpssnrpy](https://github.com/kristinemlarson/gpssnrpy) | gpssnrpy：RINEX SNR 提取与高度角/方位角 | Python | 6 | 🏷️ 高校实验室 |
| [NearRealTimeGNSSIR](https://github.com/cemalialtuntas/NearRealTimeGNSSIR) | NearRealTimeGNSSIR：近实时 GNSS-IR 软件原型 | HTML | 5 | 🏷️ 高校实验室 |
| [FindSnowOutliers](https://github.com/kristinemlarson/FindSnowOutliers) | FindSnowOutliers：SNR 检测天线积雪异常 | MATLAB | 4 | 🏷️ 高校实验室 |
| [gnssr-raspberry](https://github.com/ITC-Water-Resources/gnssr-raspberry) | gnssr-raspberry：树莓派 GNSS 反射测量（ITC 水资源） | Python | 3 | 🏷️ 高校实验室 |
| [gpsonlySNR](https://github.com/kristinemlarson/gpsonlySNR) | gpsonlySNR：GPS RINEX→SNR 提取工具 | Fortran | 2 | 🏷️ 高校实验室 |

### 详细说明

#### [gnssSNR](https://github.com/kristinemlarson/gnssSNR)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：15 · 宿主：github

Kristine Larson 团队工具，从 RINEX 剥离 SNR 及卫星方位角、高度角，常作为 gnssrefl / GNSS-IR 反射测量流水线前置。MIT 许可，Fortran 实现。适合反射测高与多路径研究；RINEX 版本支持以说明为准，完整反射反演与站点元数据请接 gnssrefl 等下游工具。

#### [GIRAS-GPS-Solutions](https://github.com/cemalialtuntas/GIRAS-GPS-Solutions)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：13 · 宿主：github

Altuntas 与 Tunalioglu 发布的 MATLAB GNSS-IR 工具，可读 RINEX 2/3 与广播/精密星历，支持多星座，含第一菲涅耳区计算与基于 SNR 的反射体高度估计及可视化。适合教学与站点级反射测量试验。依赖 MATLAB 环境；大规模业务化反演可对照 Kristen Larson 的 gnssrefl。

#### [FresnelMaps](https://github.com/kristinemlarson/FresnelMaps)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：9 · 宿主：github

Kristine Larson 团队工具，为地基 GNSS-IR/反射测量绘制菲涅耳区地图，辅助选址与几何解释。MIT 许可；与 gnssSNR、gnssrefl 同谱系前置工具。输入站坐标与天线高需准确，输出服务实验设计，本身不做水位或雪深反演。

#### [gnssr4river](https://github.com/lroineau/gnssr4river)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：8 · 宿主：github

开源 Python GNSS-R/IR 工具箱，偏向河流/水位等水文应用场景。适合把反射测高接到水文监测脚本。功能覆盖面小于 gnssrefl 全家桶，复杂站点仍建议用主流工具交叉检验。

#### [gpssnrpy](https://github.com/kristinemlarson/gpssnrpy)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：6 · 宿主：github

从 GPS RINEX 提取 SNR，并结合导航电文算高度角/方位角，还带下载辅助。常作为 GNSS-IR 前处理积木，与 gnssrefl 生态 complementary。

#### [NearRealTimeGNSSIR](https://github.com/cemalialtuntas/NearRealTimeGNSSIR)  
*🏷️ 高校实验室*

语言：HTML · 许可：GPL-3.0 · 星标约：5 · 宿主：github

朝近实时 GNSS-IR 流水线努力的实现，目标从 SNR 提取水位/雪深/土壤湿度等环境参数。适合做自动化监测原型。工程完整度与多星座支持需实测，稳定产线可对照 gnssrefl。

#### [FindSnowOutliers](https://github.com/kristinemlarson/FindSnowOutliers)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：4 · 宿主：github

Kristine Larson 团队 Matlab 工具：利用 SNR 判断天线积雪何时污染 GPS 坐标解。MIT 许可；属 GNSS-IR/多路径谱系的质控辅助。输入需匹配的 SNR 与坐标时序，真正雪深或水位反演请接 gnssrefl 等下游工具完成。

#### [gnssr-raspberry](https://github.com/ITC-Water-Resources/gnssr-raspberry)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：3 · 宿主：github

ITC Water Resources 在树莓派上运行的 GNSS 反射测量实验工程，面向低成本水文监测站。适合野外原型与教学演示。仓库星标较少、文档随版本变化；水位/土壤湿度产品建议对照 gnssrefl 与大地型天线结果。

#### [gpsonlySNR](https://github.com/kristinemlarson/gpsonlySNR)  
*🏷️ 高校实验室*

语言：Fortran · 许可：MIT · 星标约：2 · 宿主：github

Larson 团队 Fortran 工具，翻译/读取 GPS RINEX 并提取 SNR，服务反射测量流水线。MIT 许可；与 gnssSNR、gpssnrpy 同谱系、更偏 GPS-only 路径。RINEX 版本支持以说明为准，完整 GNSS-IR 反演需再接 gnssrefl 处理。

## GNSS-IR水位

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GMR-Water](https://github.com/GRseRG-CUMTB/GMR-Water) | GMR-Water：矿大（北京）GNSS 多路径反射水位反演 | MATLAB | 7 | 🏷️ 高校实验室 |

### 详细说明

#### [GMR-Water](https://github.com/GRseRG-CUMTB/GMR-Water)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：see upstream README · 星标约：7 · 宿主：github

面向 GNSS 多路径反射信号的水位检索实现，提供从观测到水位产品的处理流程，适合水文与近岸监测试验。许可与依赖以仓库说明为准。站点几何、天线环境与 SNR 质量对结果影响大；与通用 GNSS-IR 套件（如 gnssrefl、GIRAS）对照选型时可看其水文专项流程与示例。

## GNSS-R处理

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS-REFLECTOMETRY-PROCESSING](https://github.com/oriolcervello/GNSS-REFLECTOMETRY-PROCESSING) | GNSS-REFLECTOMETRY-PROCESSING：GPU 加速 GNSS-R 处理 | Cuda | 17 | 🏷️ 个人社区 |

### 详细说明

#### [GNSS-REFLECTOMETRY-PROCESSING](https://github.com/oriolcervello/GNSS-REFLECTOMETRY-PROCESSING)  
*🏷️ 个人社区*

语言：Cuda · 许可：GPL-3.0 · 星标约：17 · 宿主：github

面向 GNSS 反射测量的 GPU/CUDA 处理实验代码，适合做吞吐或算法加速试验。硬件与驱动依赖重；业务流水线需自行封装 I/O 与质控。

## GNSS-IR/RR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSS_RR](https://github.com/lasteine/GNSS_RR) | GNSS_RR：雪面反射/折射连续估计（冰冻圈） | Python | 7 | 🏷️ 高校实验室 |

### 详细说明

#### [GNSS_RR](https://github.com/lasteine/GNSS_RR)  
*🏷️ 高校实验室*

语言：Python · 许可：CC0-1.0 · 星标约：7 · 宿主：github

联合 GNSS 反射与折射连续估计雪/粒雪累积、表面质量与密度，面向冰冻圈监测。场景专一；通用水位 GNSS-IR 不是其主场。

## 反射测量

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS) | GNSSRMERRByS：TechDemoSat-1 星载 GNSS-R 示例（SSTL） | MATLAB | 34 | 🏷️ 个人社区 |
| [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3) | gnssIR-matlab-v3：Larson 实验室 GNSS-IR MATLAB | MATLAB | 30 | 🏷️ 高校实验室 |
| [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python) | gnssIR_python：Larson 实验室 GNSS-IR Python 脚本 | Python | 26 | 🏷️ 高校实验室 |
| [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost) | gnssrlowcost：低成本 GNSS 反射测量分析 | MATLAB | 14 | 🏷️ 个人社区 |
| [gnssr-synth](https://github.com/purnelldj/gnssr_synth) | gnssr-synth：GNSS-R 水位分析与合成 SNR | MATLAB | 11 | 🏷️ 个人社区 |

### 详细说明

#### [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS)  
*🏷️ 个人社区*

语言：MATLAB · 许可：— · 星标约：34 · 宿主：github

Surrey Satellite Technology 提供的 TechDemoSat-1（MERRByS）星载 GNSS-R 示例处理材料，演示空间反射数据的读取与初步产品步骤。面向星载 GNSS-R、海洋与地表遥感读者。这是任务示例而非通用地基 GNSS-IR 软件；地基水位/雪深请用 gnssrefl 等，两者观测几何与校正链不同。

#### [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：30 · 宿主：github

Kristine Larson 团队发布的 GNSS 干涉反射（GNSS-IR）MATLAB 新版，用信噪比（SNR）随高度角振荡反演反射面高度，常用于水位、雪深与土壤湿度。面向已有 MATLAB 流程的地球物理与大地测量用户。边界是反射测高/环境遥感，不做对流层 ZTD；Python 产线请优先对照同作者持续维护的 gnssrefl，本仓库更偏 MATLAB 用户留存版本。

#### [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：26 · 宿主：github

Larson 实验室较早的 GNSS-IR Python 脚本集，从 GNSS 观测提取 SNR 干涉条纹并估计反射器高度，服务水位与地表环境监测。适合想在纯脚本环境快速试验 GNSS-IR 的研究者。工程化、命令行与多星座流程弱于现维护的 gnssrefl；新项目建议直接用 gnssrefl，本库可作算法对照或旧文复现。

#### [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：14 · 宿主：github

面向低成本 GNSS 硬件的反射测量分析，同时给出 MATLAB 与 Python 路径，降低 GNSS-R/IR 入门与课程实验门槛。适合教学站与原型站网。测高精度与稳定性通常不及大地型天线+gnssrefl；使用前需核对天线相位中心、多路径几何与采样率是否满足干涉条纹分辨需求。场地开阔度与多路径环境会显著影响可用弧段长度。

#### [gnssr-synth](https://github.com/purnelldj/gnssr_synth)  
*🏷️ 个人社区*

语言：MATLAB · 许可：MIT · 星标约：11 · 宿主：github

MATLAB 工具：获取并分析 GNSS-R 水位观测，同时可生成合成 SNR，便于方法试验、误差传播与教学演示。面向反射测高与水文监测研究者。侧重水位场景与合成数据，不是覆盖雪深/土壤湿度的完整 GNSS-IR 套件；低成本接收机路线可并读同作者 gnssr_lowcost，产线级处理仍常回 gnssrefl。

## 反射测量/PWV相关

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | gnssrefl：GNSS-IR 反射测量工具 | Python | 217 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [gnssrefl](https://github.com/kristinemlarson/gnssrefl)  
*🏷️ 高校实验室 核心*

语言：Python · 许可：GPL-3.0 · 星标约：217 · 宿主：github

GNSS 干涉反射测量（GNSS-IR）主流开源工具，用反射信号估水位、土壤湿度、雪深等，也常与近地表环境/湿延迟研究相关。文档与 Docker 支持较好。定位解算不是目标；要 ZTD/PWV 主产品仍用 PPP+气象流程。

## 大气延迟/InSAR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ITU-Rpy](https://github.com/inigodelportillo/ITU-Rpy) | ITU-Rpy：ITU-R 大气衰减建议的 Python 库 | Python | 172 | 🏷️ 个人社区 |
| [PyAPS](https://github.com/insarlab/PyAPS) | PyAPS：全球模式大气相位屏（APS） | Python | 86 | 🏷️ 高校实验室 |
| [ICAMS](https://github.com/ymcmrs/ICAMS) | ICAMS：InSAR 对流层改正（全球大气模式） | Python | 44 | 🏷️ 高校实验室 |
| [TropDS](https://github.com/Sardingfish/TropDS) | 物理约束 U-Net 深度学习对流层延迟格网降尺度框架 TropDS | Python | 1 | 🏷️ 高校实验室 |

### 详细说明

#### [ITU-Rpy](https://github.com/inigodelportillo/ITU-Rpy)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：172 · 宿主：github

将 ITU-R P. 系列大气衰减与传播建议实现为 Python 库，用于雨衰、气体衰减等链路预算，常与卫星/GNSS 相关传播分析对照。MIT 许可；目录已有 ITU-R 软件索引页，本条补齐可脚本化的 P 系列工具包。注意建议书版本与适用频段，它不是 GNSS 观测解算器。

#### [PyAPS](https://github.com/insarlab/PyAPS)  
*🏷️ 高校实验室*

语言：Python · 许可：GPL-3.0 · 星标约：86 · 宿主：github

用全球大气模式生成大气相位屏，服务 InSAR 对流层改正，思路与 GNSS 气象同源（湿延迟结构）。适合 InSAR+GNSS 联合的人理解三维湿延迟。不直接输出测站 ZTD 产品。

#### [ICAMS](https://github.com/ymcmrs/ICAMS)  
*🏷️ 高校实验室*

语言：Python · 许可：— · 星标约：44 · 宿主：github

用全球大气模式做 InSAR 对流层改正，并考虑空间随机特性。适合高级 InSAR 大气研究。与 GNSS 单站 ZTD 流程接口需自行桥接。

#### [TropDS](https://github.com/Sardingfish/TropDS)  
*🏷️ 高校实验室*

语言：Python · 许可：BSD-3-Clause · 星标约：1 · 宿主：github

与 Mapping-Function-Height-Correction-Models 同一作者团队的深度学习项目，BSD-3-Clause 许可，Python/PyTorch 实现。针对空间大地测量中粗分辨率 ZHD/ZWD 格网，采用带物理约束的 U-Net 将低分辨率延迟图恢复为高分辨率，以提升 GNSS、InSAR 对流层改正精度，并提供项目网页与示例动画。据仓库新闻已于 2026 年 6 月被 Journal of Geodesy 接收。适合研究 AI 对流层建模或需要高分辨率延迟格网的用户；训练需 GPU 与再分析数据，模型泛化性应在本地区自行评估。

## GNSS-IR硬件

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [mphw](https://github.com/ufrgs-gnss-lab/mphw) | mphw：低成本 GNSS-IR/反射测量开源硬件 | MATLAB | 25 | 🏷️ 高校实验室 |

### 详细说明

#### [mphw](https://github.com/ufrgs-gnss-lab/mphw)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：NOASSERTION · 星标约：25 · 宿主：github

开源低成本 GNSS-IR/反射测量硬件方案（MPHW），配合 SNR 反射测高。适合教学站与原型站网，降低进入 GNSS-R 的硬件门槛。精度受天线与场地多路径制约，科研级水位/雪深仍常对照 gnssrefl + 大地型天线。

## GNSS-IR/多路径仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [mpsim](https://github.com/ufrgs-gnss-lab/mpsim) | mpsim：GNSS 多路径前向仿真器 | MATLAB | 48 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [mpsim](https://github.com/ufrgs-gnss-lab/mpsim)  
*🏷️ 高校实验室 核心*

语言：MATLAB · 许可：BSD-2-Clause · 星标约：48 · 宿主：github

Nievinski 与 Larson 发表于 GPS Solutions 的开源多路径仿真器，用几何光学前向模型模拟近地表反射对 GNSS 观测的影响，服务 GNSS-IR 与定位多路径研究。支持 Matlab/Octave，附路径初始化脚本。面向机理仿真而非直接水位检索流水线；实测反演常与 gnssrefl、GIRAS 等工具衔接。

## 射线追踪/NWM

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [RADIATE](https://github.com/TUW-VieVS/RADIATE) | RADIATE：对流层射线追踪程序 | Fortran | 23 | 🏷️ 高校实验室 核心 |

### 详细说明

#### [RADIATE](https://github.com/TUW-VieVS/RADIATE)  
*🏷️ 高校实验室 核心*

语言：Fortran · 许可：GPL-3.0 · 星标约：23 · 宿主：github

TU Wien VieVS 组发布的 Fortran 射线追踪程序，可对微波与光学频段观测重建对流层延迟及相关参数，输入依赖数值天气预报场。适合与 VMF/GPT 产品对照、做高精度延迟研究或 VLBI/GNSS 联合试验。NWM 数据获取与预处理需自备；官方亦有校内 Git 镜像，公开仓以 GitHub 为准。

## ZTD/ZWD/VMF

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc) | STD_SWD_Calc：斜路径延迟与模型 ZTD | Python | 10 | 🏷️ 个人社区 核心 |

### 详细说明

#### [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc)  
*🏷️ 个人社区 核心*

语言：Python · 许可：GPL-3.0 · 星标约：10 · 宿主：github

Python 包生成斜路径干/湿延迟（STD/SWD）以及基于 GPT/VMF 的模型 ZTD，直接对接维也纳映射函数生态。适合 GNSS 气象、PPP 先验对流层、与实测 ZTD 对比。站点元数据与 VMF 格网下载要自己准备；业务化连续运行需另写调度。

## VMF/GPT官方代码

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Mapping-Function-Height-Correction-Models](https://github.com/Sardingfish/Mapping-Function-Height-Correction-Models) | 对流层映射函数高程改正模型参数与 MATLAB 脚本（J Geod 2024 配套） | MATLAB | 2 | 🏷️ 高校实验室 |
| [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes) | TU Wien 官方 VMF1/VMF3/GPT/GMF 源码与格网目录 | Fortran/MATLAB/C++ | — | 🏷️ 官方 核心 |
| [VMF-TUWien-Home](https://vmf.geo.tuwien.ac.at/) | VMF-TUWien-Home：TU Wien VMF/GPT 对流层产品与代码门户 | Fortran/MATLAB | — | 🏷️ 官方 |

### 详细说明

#### [Mapping-Function-Height-Correction-Models](https://github.com/Sardingfish/Mapping-Function-Height-Correction-Models)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：MIT · 星标约：2 · 宿主：github

Ding 等 2024 年发表于 Journal of Geodesy 的映射函数垂直建模方法配套仓库，MIT 许可。VMF1/VMF3 等映射函数产品只在地表给出，飞机、无人机或高山测站需要高程改正；仓库提供最小模型参数集与 MATLAB 脚本，按用户高度恢复系数 a 并输出改正后的映射函数。适合 GNSS/VLBI 高精度处理中研究对流层映射误差的读者，与 TU Wien VMF 代码配合使用。平台标注为 Windows，数据量精简，便于复现论文结论。

#### [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes)  
*🏷️ 官方 核心*

语言：Fortran/MATLAB/C++ · 许可：TU Wien site terms · 星标约：— · 宿主：official_site

维也纳工大公开的 VMF1/VMF3、GPT/GPT2w/GPT3、GMF、Saastamoinen 等 Fortran/MATLAB/C++ 实现与格网文件，是对流层映射与气象先验的权威入口。目录持续更新（含 vmf3_grid 等）。预报产品获取常需遵循站点注册要求；可与 STD_SWD_Calc 等脚本联用。

#### [VMF-TUWien-Home](https://vmf.geo.tuwien.ac.at/)  
*🏷️ 官方*

语言：Fortran/MATLAB · 许可：TU Wien terms · 星标约：— · 宿主：official_site

维也纳工大 VMF 服务门户，说明 VMF1/VMF3 格网产品与 GPT 系列气象模型，并链到 /codes 开源实现。PPP/VLBI 对流层延迟建模的权威数据与代码源头。格网下载常需遵循站点条款；具体源码文件见 codes 目录条目，勿与第三方拷贝混淆。收录前已用 HTTP 核验页面可访问；使用请遵守上游许可与引用要求。

## 经验模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UNB3m](https://github.com/ohm1122/UNB3m) | UNB3m：UNB 中性大气延迟模型实现 | — | 3 | 🏷️ 个人社区 ★ |

### 详细说明

#### [UNB3m](https://github.com/ohm1122/UNB3m)  
*🏷️ 个人社区 ★*

语言：— · 许可：— · 星标约：3 · 宿主：github

UNB 系列中性大气经验模型，无实测气象时给天顶延迟粗值。适合教学与低精度先验。精度不及 VMF+数值天气模式；精密 PPP 优先 VMF3/GPT3。

## 大气模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [lowtran](https://github.com/space-physics/lowtran) | lowtran：LOWTRAN7 大气消光模型的 Python 封装 | Python | 118 | 🏷️ 高校实验室 |
| [msise00](https://github.com/space-physics/msise00) | NRLMSISE-00 的 Python/Matlab 封装 | Python | 63 | 🏷️ 高校实验室 |
| [hwm14](https://github.com/gemini3d/hwm14) | hwm14：NRL 水平风场模型开源 CMake 构建 | Fortran | 7 | 🏷️ 高校实验室 |
| [GTrop](https://github.com/sun1753814280/GTrop) | 基于 1979–2017 再分析资料的全球对流层延迟与加权平均温度经验模型 GTrop（MATLAB） | MATLAB | 5 | 🏷️ 高校实验室 |

### 详细说明

#### [lowtran](https://github.com/space-physics/lowtran)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：118 · 宿主：github

space-physics 维护的 LOWTRAN7 现代封装，用 f2py/CMake 在 Python 中直接传 xarray，避免读写文本卡。用于大气透过率、消光与辐照度估算，可服务 GNSS 气象/传播仿真周边。需 Fortran 编译器；不是对流层 ZTD 映射官方库。MIT。

#### [msise00](https://github.com/space-physics/msise00)  
*🏷️ 高校实验室*

语言：Python · 许可：MIT · 星标约：63 · 宿主：github

把经典 NRLMSISE-00 中性大气模式包成 Python/Matlab 接口，便于算密度、温度等高度剖面。GNSS 气象与火箭/掩星背景大气、以及部分电离层驱动耦合研究常作辅料。注意它是中性大气模式，不是 TEC/IRI；引用与系数版本请按 NRL 原文献与仓库说明。

#### [hwm14](https://github.com/gemini3d/hwm14)  
*🏷️ 高校实验室*

语言：Fortran · 许可：Apache-2.0 · 星标约：7 · 宿主：github

gemini3d 维护的 NRL Horizontal Wind Model 2014 可构建库，用 CMake 生成 libhwm14，供上层大气/电离层耦合与轨迹仿真调用。Apache-2.0。是中性风经验模型而非 GNSS 处理软件；旧 HWM93 包装仓已归档，新集成优先此仓。

#### [GTrop](https://github.com/sun1753814280/GTrop)  
*🏷️ 高校实验室*

语言：MATLAB · 许可：— · 星标约：5 · 宿主：github

论文“A global model for estimating tropospheric delay and weighted mean temperature developed with atmospheric reanalysis data from 1979 to 2017”配套代码仓库，MATLAB 实现，由学术作者公开。模型以长期再分析资料拟合天顶对流层延迟与加权平均温度 Tm 的时空变化，可在无实测气象参数时为 GNSS 定位和 PWV 反演提供先验值，定位上类似 GPT3 等经验模型的替代或对照。仓库说明较少且未声明许可，复用前应联系作者并引用原文。同作者另有区域版 CTrop。

## 对流层产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [IGS-Troposphere-WG](https://igs.org/wg/troposphere/) | IGS 对流层工作组：ZTD/梯度产品与活动入口 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [IGS-Troposphere-WG](https://igs.org/wg/troposphere/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

介绍 IGS 对流层联合产品、分析中心角色及会议活动，是查找 ZTD、梯度与相关试点的入口页。页面本身不托管大容量产品文件，下载通常走 CDDIS/IGN 等数据中心。对流层产品与电离层/轨道产品解耦，引用时需核对产品版本与时延。收录前已用 HTTP 核验可访问；使用请遵守 IGS 与上游条款。

## GNSS-VOD

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssvod](https://github.com/vincenthumphrey/gnssvod) | gnssvod：由 GNSS 接收机输出估计植被光学厚度 VOD（MIT） | Python | 7 | 🏷️ 个人社区 |

### 详细说明

#### [gnssvod](https://github.com/vincenthumphrey/gnssvod)  
*🏷️ 个人社区*

语言：Python · 许可：MIT · 星标约：7 · 宿主：github

读取 GNSS 接收机输出并分析植被光学厚度（VOD）的 Python 工具，MIT 许可。属 GNSS 反射/衰减遥感旁支，与测地定位互补。星数不高但许可证清晰、主题明确。结果依赖天线环境与预处理；不替代专用 GNSS-IR 套件如 gnssrefl。适合生态/水文遥感试验。

## EPN对流层

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EUREF-EPN-Troposphere](https://www.epncb.oma.be/_productsservices/troposphere/) | EUREF EPN：对流层产品与服务专页 | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [EUREF-EPN-Troposphere](https://www.epncb.oma.be/_productsservices/troposphere/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

EPN 中央局对流层产品服务页，汇总欧洲永久 GNSS 网的对流层延迟相关产品入口。与已收录 EPN 主页、观测 FTP 互补，本页专指对流层派生产品。GNSS 气象与 ZTD 对比常用。收录前已 HTTP 核验；下载与引用遵循 EPN/EUREF 规定。

## VMF产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [VMF1-GNSS-Products](https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF1/) | TU Wien：VMF1 GNSS 对流层产品目录 | data-portal | — | 🏷️ 官方 |
| [VMF3-GNSS-Products](https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF3/) | TU Wien：VMF3 GNSS 对流层产品目录（EI/FC/OP） | data-portal | — | 🏷️ 官方 |

### 详细说明

#### [VMF1-GNSS-Products](https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF1/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

VMF 数据服务器上较早期的 VMF1 GNSS 产品目录，与 VMF3 目录并列。历史解算与文献复现仍常引用 VMF1。与 trop_products 总页、codes 页互补。收录前已 HTTP 核验；引用格式见 TU Wien VMF 说明。

#### [VMF3-GNSS-Products](https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF3/)  
*🏷️ 官方*

语言：data-portal · 许可：portal-terms · 星标约：— · 宿主：official_site

维也纳工大 VMF 数据服务器上 VMF3 面向 GNSS 的产品目录，含 VMF3_EI/FC/OP 等子目录。与已收录 trop_products 总目录、VMF 主页互补，本 URL 直达 VMF3。精密定位与 ZTD 映射常用网格。收录前已 HTTP 核验；使用请引用 TU Wien VMF 文档。
