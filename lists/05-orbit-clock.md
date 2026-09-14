# 轨道与钟差 / Orbit & Clock
> 共 **3** 个已收录项目。本文件为链接索引，不含第三方源码。

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
| [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB) | 多 GNSS 频间钟差（IFCB）估计开源软件 | C++ | 15 |  |
| [rt-clk-service](https://github.com/DoubleString/rt-clk-service) | 实时 GNSS 钟差/轨道/UPD/IFPB 服务相关 | C++ | 12 |  |

### 详细说明

#### [GREAT-IFCB](https://github.com/GREAT-WHU/GREAT-IFCB)

语言：C++ · 许可：GPL-3.0 · 星标约：15

武大 GREAT 组开源的多星座频间钟差（IFCB）估计工具，服务于精密钟差与偏差产品链路，与 GREAT-PVT 等同一研究线。做三频 PPP、相位偏差与钟差产品的人应关注。它是独立小工具，不替代完整 POD 套件；轨道与 UPD/OSB 能力仍多见诸 Ginan、PRIDE、GROOPS 等大型系统。

#### [rt-clk-service](https://github.com/DoubleString/rt-clk-service)

语言：C++ · 星标约：12

面向实时钟差、轨道与 UPD/IFPB 等偏差产品的服务向代码，贴近 PPP-AR 实时链。适合研究实时产品生成。公开完整度有限，需自备数据与对照 IGS 产品。
