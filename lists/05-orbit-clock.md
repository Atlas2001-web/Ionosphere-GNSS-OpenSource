# 轨道与钟差 / Orbit & Clock
> 共 **6** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** 精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。

## 时间比对

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [cggtts](https://github.com/nav-solutions/cggtts) | CGGTTS 远程时间比对解析与调度 | Rust | 18 |  |

### 详细说明

#### [cggtts](https://github.com/nav-solutions/cggtts)

语言：Rust · 许可：MPL-2.0 · 星标约：18

处理 CGGTTS 格式与轨迹调度，服务 GNSS 共视/全视时间比对。适合时间频率实验室。一般导航定位用户用不上。


## 钟差/轨道/UPD

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD) | 武大 GREAT 开源多星座 UPD（未校准相位延迟）估计软件 | C++ | 19 | 核心 |
| [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT) | GREAT 多星座实时滤波精密定轨（POD）模块 | C++ | 17 | 核心 |
| [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB) | 多 GNSS 频间钟差（IFCB）估计开源软件 | C++ | 15 |  |
| [rt-clk-service](https://github.com/DoubleString/rt-clk-service) | 实时 GNSS 钟差/轨道/UPD/IFPB 服务相关 | C++ | 12 |  |
| [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE) | 武大 GREAT 团队精密卫星钟差估计软件 | C++ | 9 | 核心 |

### 详细说明

#### [GREAT-UPD](https://github.com/GREAT-WHU/GREAT-UPD)  
*核心*

语言：C++ · 许可：GPL-3.0 · 星标约：19

专门估计多星座 GNSS UPD/未校准相位延迟类产品，为 PPP-AR 模糊度固定提供相位偏差输入。适合需要自建相位偏差链路的课题组与教学演示。产品字段与 IGS OSB/UPD 惯例必须对齐才能接到 PRIDE 等下游；参考卫星选择、日边界与站网几何会直接影响稳定性，发布前应用公开网做交叉检验。

#### [GREAT_PODFLT](https://github.com/GREAT-WHU/GREAT_PODFLT)  
*核心*

语言：C++ · 星标约：17

执行多 GNSS 实时滤波精密轨道确定（POD），偏产品生成与定轨算法验证，而非终端定位。适合轨道/钟差方向研究生对照 GREAT 流水线。公开算例与力模型文档完整度需自查；与 Ginan、GROOPS 等大型套件相比，更适合精读 GREAT 定轨滤波环节，而不是替代整套业务定轨系统。

#### [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB)

语言：C++ · 许可：GPL-3.0 · 星标约：15

武大 GREAT 组开源的多星座频间钟差（IFCB）估计工具，服务于精密钟差与偏差产品链路，与 GREAT-PVT 等同一研究线。做三频 PPP、相位偏差与钟差产品的人应关注。它是独立小工具，不替代完整 POD 套件；轨道与 UPD/OSB 能力仍多见诸 Ginan、PRIDE、GROOPS 等大型系统。

#### [rt-clk-service](https://github.com/DoubleString/rt-clk-service)

语言：C++ · 星标约：12

面向实时钟差、轨道与 UPD/IFPB 等偏差产品的服务向代码，贴近 PPP-AR 实时链。适合研究实时产品生成。公开完整度有限，需自备数据与对照 IGS 产品。

#### [GREAT-PCE](https://github.com/GREAT-WHU/GREAT-PCE)  
*核心*

语言：C++ · 许可：GPL-3.0 · 星标约：9

聚焦精密卫星钟差估计，可与 GREAT-UPD、POD 模块组成轨道钟差产品链，服务 PPP 与时间传递相关研究。适合钟差建模、实时/事后产品试验。输入轨道与地面站网质量决定上限；若目标只是终端定位，通常直接使用 IGS/分析中心钟差即可，不必自建整条钟差产线。
