# 学习资源与工具 / Learning & Tools
> 共 **15** 个已收录项目。本文件为链接索引，不含第三方源码。

**这类做什么？** awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。

## 数据集

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset) | 亚洲城市峡谷多传感器定位数据集 | Python | 606 |  |
| [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets) | 武大 i2Nav 整理的车载 GNSS/INS 融合公开数据集列表 | — | 280 | 核心 |
| [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green) | 由 GNSS 垂直位移反演陆地水储量 GNSS2TWS | MATLAB | 33 |  |

### 详细说明

#### [UrbanNavDataset](https://github.com/IPNL-POLYU/UrbanNavDataset)

语言：Python · 星标约：606

香港/东京等城市峡谷多传感器数据，含真值，是 GNSS/INS/视觉算法基准常用集。适合算法评测。本身不是解算软件。

#### [awesome-gins-datasets](https://github.com/i2Nav-WHU/awesome-gins-datasets)  
*核心*

语言：— · 星标约：280

汇总适合车载 GNSS/INS 组合导航评测的公开数据集与说明入口，减少四处搜数据的时间成本。适合写论文基线、算法对比与课程大作业选题。本身不是解算软件；引用各数据集时要核对许可协议、传感器时间同步与标定文件是否齐全，缺失标定会严重扭曲融合精度结论。

#### [gnss2tws-green](https://github.com/jzshhh/gnss2tws_green)

语言：MATLAB · 星标约：33

开源 MATLAB 工具 GNSS2TWS：利用 GNSS 测站日尺度垂直位移，经格林函数等方法推断陆地水储量（TWS）变化，服务水文大地测量。适合已有精密坐标时间序列、做气候水文交叉的研究者。不是导航定位解算器；空间平滑、负载模型与参考框架假设必须按配套论文核对。输入坐标序列质量决定反演可信度。站点分布稀疏时，反演空间分辨率会明显下降。


## 课程笔记

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning) | 导航定位开源项目解读与学习笔记（中文） | — | 2417 | ★ Star · 核心 |
| [learning_rtklib](https://github.com/libing64/learning_rtklib) | RTKLIB 学习相关材料 | — | 163 |  |
| [RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN) | RTKLIB 中文手册解读与源码解析笔记 | — | 54 |  |

### 详细说明

#### [Navigation-Learning](https://github.com/LiZhengXiao99/Navigation-Learning)  
*★ Star · 核心*

语言：— · 星标约：2417

系统整理 RTKLIB/GAMP/GREAT/Ginan/GINav/GICI 等源码阅读笔记与开源清单，中文学习路径非常完整。适合入门导航软件。笔记非上游文档，实现细节以各项目为准。

#### [learning_rtklib](https://github.com/libing64/learning_rtklib)

语言：— · 星标约：163

围绕 RTKLIB 的学习材料/笔记向仓库，降低读 C 代码的门槛。与 Navigation-Learning 互补。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [RTKLIB-Manual-CN](https://github.com/salmoshu/RTKLIB-Manual-CN)

语言：— · 星标约：54

系统梳理 RTKLIB 工具使用、算法要点与工程阅读路径的中文笔记，降低中文读者入门与源码导读成本。适合自学、培训与课题组内部分享。不是可执行定位库；内容可能落后于最新 RTKLIB 或 demo5 分支，关键公式与编译选项请回对官方手册与当前源码。


## 资源列表

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [awesome-gnss](https://github.com/barbeau/awesome-gnss) | 开源 GNSS 软件与资源社区列表 | — | 599 | 核心 |
| [awesome-gnss](https://github.com/hdkarimi/awesome-gnss) | GNSS/RNSS 开源工具、数据与课程的 awesome 列表 | — | 50 |  |

### 详细说明

#### [awesome-gnss](https://github.com/barbeau/awesome-gnss)  
*核心*

语言：— · 许可：Apache-2.0 · 星标约：599

Sean Barbeau 维护的 awesome 列表，覆盖 App、桌面工具、库与文献入口，本目录大量种子来源之一。适合定期浏览查新。本身不含算法实现。

#### [awesome-gnss](https://github.com/hdkarimi/awesome-gnss)

语言：— · 许可：MIT · 星标约：50

策展 GNSS/RNSS 相关开源软件、数据、工具与慕课入口的 awesome 列表，帮助新人快速摸清领域版图。适合浏览式调研与课程资源推荐。链接时效性需自行点击验证；与本精选目录互补——awesome 偏广度，本目录强调核验 URL、分类与中文技术分析。


## 可视化

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility) | Google Earth 鱼眼可见性分析 | MATLAB | 137 |  |
| [EasyGNSS](https://github.com/whigg/EasyGNSS) | 面向低成本 GNSS 的图形界面辅助工具 | Python | 4 |  |

### 详细说明

#### [ge-gnss-visibility](https://github.com/taroz/ge-gnss-visibility)

语言：MATLAB · 许可：MIT · 星标约：137

在任意位置生成虚拟鱼眼天顶图并判断 GNSS 可见性，城市遮挡研究直观。需要 Google Earth 相关环境。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。

#### [EasyGNSS](https://github.com/whigg/EasyGNSS)

语言：Python · 许可：GPL-3.0 · 星标约：4

为低成本 GNSS 接收机提供简易图形界面，降低配置、查看星空与状态的门槛。适合教学演示、业余爱好者台站与快速连通性检查。精密解算与质检能力有限；深入分析请导出 RINEX 后接入 RTKLIB、Anubis 或 georinex 流水线。


## 认证/完好性

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [OSNMA](https://github.com/Algafix/OSNMA) | Galileo OSNMA 协议 Python 实现 | Python | 52 |  |

### 详细说明

#### [OSNMA](https://github.com/Algafix/OSNMA)

语言：Python · 许可：EUPL-1.2 · 星标约：52

实现 Galileo 开放业务消息认证（OSNMA），用于抗欺骗研究与接收机试验。适合安全/完好性方向。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## RTK网络客户端

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [polaris](https://github.com/PointOneNav/polaris) | Point One RTK 网络服务通信软件 | — | 33 |  |

### 详细说明

#### [polaris](https://github.com/PointOneNav/polaris)

语言：— · 许可：MIT · 星标约：33

与 Point One 的 RTK 网络服务通信的开源客户端侧代码，便于接云端改正。服务本身非开源；适合对接其生态。仓库公开可查，细节以当前上游文档为准，避免把过时脚本当生产基线。


## 高程/大地水准面

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [earth-gravitational-model](https://github.com/barbeau/earth-gravitational-model) | WGS84 海拔转 EGM84 海拔的轻量库 | Java | 18 |  |

### 详细说明

#### [earth-gravitational-model](https://github.com/barbeau/earth-gravitational-model)

语言：Java · 许可：LGPL-2.1 · 星标约：18

把 GeoTools 大地水准面模型做成轻量 Java 库，方便 Android 上做海拔转换。测地学严密应用请用专业大地水准面产品。


## PNT仿真

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [kshana](https://github.com/ashfordeOU/kshana) | 开源可复现 PNT 韧性仿真（轨道/完好性/融合） | Rust | 6 |  |

### 详细说明

#### [kshana](https://github.com/ashfordeOU/kshana)

语言：Rust · 许可：AGPL-3.0 · 星标约：6

覆盖轨道、参考架、可用性/DOP、GNSS/INS、ARAIM/SBAS 保护级等的仿真框架，带跨语言绑定。适合完好性与韧性研究。AGPL；项目较新。


## SBAS

| 项目 | 一句话 | 语言 | ★ | 标记 |
|---|---|---|---:|---|
| [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos) | EGNOS/SBAS 工具集（SourceForge） | — | — |  |

### 详细说明

#### [EGNOS-Toolkit](https://sourceforge.net/projects/libegnos)

语言：—

面向 EGNOS 等 SBAS 的开源工具集，Linux 下可做增强信号相关试验。托管在 SourceForge；现代多星座 SBAS 研究还需补充新资料。
