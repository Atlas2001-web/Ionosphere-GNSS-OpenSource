# 对流层 / Troposphere
> 共 **13** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。

## 反射测量/PWV相关

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [gnssrefl](https://github.com/kristinemlarson/gnssrefl) | GNSS-IR：反射信号估水位/土壤湿度/雪深 | Python | 217 | 核心 |

### 详细说明

#### [gnssrefl](https://github.com/kristinemlarson/gnssrefl)  
*核心*

语言：Python · 许可：GPL-3.0 · 星标约：217

GNSS 干涉反射测量（GNSS-IR）主流开源工具，用反射信号估水位、土壤湿度、雪深等，也常与近地表环境/湿延迟研究相关。文档与 Docker 支持较好。定位解算不是目标；要 ZTD/PWV 主产品仍用 PPP+气象流程。


## 大气延迟/InSAR

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PyAPS](https://github.com/insarlab/PyAPS) | 基于全球大气模式的大气相位屏（APS） | Python | 86 |  |
| [ICAMS](https://github.com/ymcmrs/ICAMS) | 顾及对流层空间随机特性的 InSAR 大气改正工具箱 | Python | 44 |  |

### 详细说明

#### [PyAPS](https://github.com/insarlab/PyAPS)

语言：Python · 许可：GPL-3.0 · 星标约：86

用全球大气模式生成大气相位屏，服务 InSAR 对流层改正，思路与 GNSS 气象同源（湿延迟结构）。适合 InSAR+GNSS 联合的人理解三维湿延迟。不直接输出测站 ZTD 产品。

#### [ICAMS](https://github.com/ymcmrs/ICAMS)

语言：Python · 星标约：44

ICAMS 用全球大气模式做 InSAR 对流层改正，并考虑空间随机特性。适合高级 InSAR 大气研究。与 GNSS 单站 ZTD 流程接口需自行桥接。


## VMF/GGOS产品

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products) | 基于 GGOS/VMF 产品在 RTKLIB 中解算对流层延迟 | C | 43 |  |

### 详细说明

#### [GGOS-Tropo-RTKLIB](https://github.com/tianruivpn1001/C-project-for-solving-tropospheric-delay-using-GGOS-tropospheric-products)

语言：C · 星标约：43

在 RTKLIB 二次开发中接入 GGOS/VMF 格网做对流层延迟，带较详细中文编译笔记。适合 Windows/VS 环境下改 RTKLIB 学 VMF。作者亦说明与官方 MATLAB 参考存在数值差，科研前应用官方码交叉验证。


## GNSS气象/PWV

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS) | GPS 可降水量（PWV）分析与 ML 应用工具 | Python | 22 |  |

### 详细说明

#### [PW_from_GPS](https://github.com/ZiskinZiv/PW_from_GPS)

语言：Python · 许可：MIT · 星标约：22

从 GPS 相关产品做可降水量分析，并带机器学习应用示例。适合 GNSS 气象入门与区域 PWV 研究。从原始 RINEX 到 ZWD 的完整 PPP 链需另接 PRIDE/Ginan 等。


## ZTD/ZWD/VMF

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc) | 由 GPT/VMF 等计算 GNSS STD/SWD 与模型 ZTD | Python | 10 | 核心 |

### 详细说明

#### [STD_SWD_Calc](https://github.com/zohrehadavi/STD_SWD_Calc)  
*核心*

语言：Python · 许可：GPL-3.0 · 星标约：10

Python 包生成斜路径干/湿延迟（STD/SWD）以及基于 GPT/VMF 的模型 ZTD，直接对接维也纳映射函数生态。适合 GNSS 气象、PPP 先验对流层、与实测 ZTD 对比。站点元数据与 VMF 格网下载要自己准备；业务化连续运行需另写调度。


## 经验模型

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UNB3m](https://github.com/ohm1122/UNB3m) | UNB3m 中性大气延迟模型 | — | 3 | ★ Star |

### 详细说明

#### [UNB3m](https://github.com/ohm1122/UNB3m)  
*★ Star*

语言：— · 星标约：3

UNB 系列中性大气经验模型，无实测气象时给天顶延迟粗值。适合教学与低精度先验。精度不及 VMF+数值天气模式；精密 PPP 优先 VMF3/GPT3。


## 反射测量

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS) | TechDemoSat-1 GNSS-R 数据处理示例（SSTL） | MATLAB | 34 |  |
| [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3) | GNSS-IR 反射测量 MATLAB 工具（Larson 实验室） | MATLAB | 30 |  |
| [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python) | GNSS-IR 反射测量 Python 脚本（Larson） | Python | 26 |  |
| [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost) | 低成本 GNSS 反射测量分析（MATLAB/Python） | MATLAB | 14 |  |
| [gnssr-synth](https://github.com/purnelldj/gnssr_synth) | GNSS-R 水位观测分析与合成 SNR 数据 | MATLAB | 11 |  |

### 详细说明

#### [GNSSRMERRByS](https://github.com/pjalesSSTL/GNSSR_MERRByS)

语言：MATLAB · 星标约：34

Surrey Satellite Technology 提供的 TechDemoSat-1（MERRByS）星载 GNSS-R 示例处理材料，演示空间反射数据的读取与初步产品步骤。面向星载 GNSS-R、海洋与地表遥感读者。这是任务示例而非通用地基 GNSS-IR 软件；地基水位/雪深请用 gnssrefl 等，两者观测几何与校正链不同。

#### [gnssIR-matlab-v3](https://github.com/kristinemlarson/gnssIR_matlab_v3)

语言：MATLAB · 星标约：30

Kristine Larson 团队发布的 GNSS 干涉反射（GNSS-IR）MATLAB 新版，用信噪比（SNR）随高度角振荡反演反射面高度，常用于水位、雪深与土壤湿度。面向已有 MATLAB 流程的地球物理与大地测量用户。边界是反射测高/环境遥感，不做对流层 ZTD；Python 产线请优先对照同作者持续维护的 gnssrefl，本仓库更偏 MATLAB 用户留存版本。

#### [gnssIR-python](https://github.com/kristinemlarson/gnssIR_python)

语言：Python · 星标约：26

Larson 实验室较早的 GNSS-IR Python 脚本集，从 GNSS 观测提取 SNR 干涉条纹并估计反射器高度，服务水位与地表环境监测。适合想在纯脚本环境快速试验 GNSS-IR 的研究者。工程化、命令行与多星座流程弱于现维护的 gnssrefl；新项目建议直接用 gnssrefl，本库可作算法对照或旧文复现。

#### [gnssrlowcost](https://github.com/purnelldj/gnssr_lowcost)

语言：MATLAB · 星标约：14

面向低成本 GNSS 硬件的反射测量分析，同时给出 MATLAB 与 Python 路径，降低 GNSS-R/IR 入门与课程实验门槛。适合教学站与原型站网。测高精度与稳定性通常不及大地型天线+gnssrefl；使用前需核对天线相位中心、多路径几何与采样率是否满足干涉条纹分辨需求。场地开阔度与多路径环境会显著影响可用弧段长度。

#### [gnssr-synth](https://github.com/purnelldj/gnssr_synth)

语言：MATLAB · 星标约：11

MATLAB 工具：获取并分析 GNSS-R 水位观测，同时可生成合成 SNR，便于方法试验、误差传播与教学演示。面向反射测高与水文监测研究者。侧重水位场景与合成数据，不是覆盖雪深/土壤湿度的完整 GNSS-IR 套件；低成本接收机路线可并读同作者 gnssr_lowcost，产线级处理仍常回 gnssrefl。


## VMF/GPT官方代码

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes) | TU Wien 官方 VMF1/VMF3/GPT 开源代码与格网 | Fortran/MATLAB/C++ | — | 核心 |

### 详细说明

#### [TU-Wien-VMF-GPT-codes](https://vmf.geo.tuwien.ac.at/codes)  
*核心*

语言：Fortran/MATLAB/C++

维也纳工大官方发布的 VMF1/VMF3、GPT/GPT2w/GPT3、GMF 等源码与格网，是对流层映射与气象先验的事实标准入口。GNSS PPP/VLBI/气象反演几乎都会间接用到。托管在官网而非 GitHub；VMF 预报产品常需注册。配套可用 STD_SWD_Calc 或 RTKLIB/PRIDE 内嵌实现。
