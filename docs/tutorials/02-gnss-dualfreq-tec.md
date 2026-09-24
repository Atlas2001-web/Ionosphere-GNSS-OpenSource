# 02 · 双频 GNSS 怎么估 TEC（几何无关、平滑、DCB）

> **课堂定位**：接第一课。你已知道 $I\approx40.3\,\mathrm{STEC}/f^{2}$ 与码/相一阶符号相反。本课把这句话写进观测方程，逐步推出几何无关（GF）组合，用**假但真实量级的 L1/L2 数字**算一遍；讲清相位模糊度、leveling/平滑、DCB 如何进入 GF；给出 RINEX→STEC 全清单与失效模式。
> 路线固定为四段：**机制 → 公式拆解（逐步推导）→ 观测签名 → 分析步骤**。
>
> **写给谁**：第一次打开 RINEX、第一次听到「几何无关」「整周模糊度」「DCB」的人；以及要用本仓库 `PROJECTS.json` 工具却还没建立「米 → TECU」量感的人。
>
> **学完交付**：用观测方程讲清码 $+I$ / 相 $-I$ 的因果；逐步推导 GF（符号表→逐步推导→小数值例）并手算 $\alpha\sim9.52\,\mathrm{TECU/m}$；解释模糊度与 leveling/平滑；写出 DCB 进入 GF 的预告式与噪声放大；在时间序列上**一眼区分**好弧 / 周跳 / 多径 / 残余偏差；按清单从 RINEX 走到 STEC 并知道每步失效模式；能点名本仓真实工具。

---

## 0. 开场：三个真实场景

请先合上笔记本，想三件事：

1. **师兄丢一天 RINEX**：说「算 TEC」。你不知道用哪两列、要不要先改周跳、为何和 GIM 对不上。本课把「两列」钉成 $P_1,P_2$（或相位），把「对不上」拆成映射/DCB/周跳三类账。
2. **STEC 全日比官方高七八 TECU**：白天夜里一起偏。有人说没改 DCB。DCB 怎能假装成电子柱？——因为它以**频率相关延迟差**混进 GF，换算后整条曲线平移。
3. **相位漂亮、伪距像心电图**：师兄说「载波平滑」。平滑是糊直线吗？——否。绝对水平靠码，形状靠相；周跳先切弧，再平滑。

**本课地图（请对照目录）：**

| 段落 | 你在学什么 | 类比 |
|---|---|---|
| §1 词表 | 先认名字 | 进厨房前认厨具 |
| §2–4 **机制** | 为何两频能测、码相为何相反、偏差为何假扮 TEC | 谁在骗尺子、雾怎么进账 |
| §5–9 **公式拆解** | 观测方程 → GF → $\alpha$ → leveling | 把菜谱拆成一步一步 |
| §10–11 **观测签名** | 时间序列上长什么样 | 监控录像怎么认人 |
| §12–17 **分析步骤** | RINEX 清单、失效模式、测验 | 值班清单与过关 |

配图均在 [`images/`](./images/)，版权见 [`images/SOURCES.md`](./images/SOURCES.md)。

**边界**：要有双频（或多频）观测才谈 GF TEC；单频只能模型改正。本课不建 GIM（见 [03](./03-gim-ionex.md)），不把 IRI 当实测（见 [04](./04-iri-nequick.md)），不把闪烁当 TEC（见 [05](./05-scintillation-roti.md)）。现象课 19–23 保持独立短文，不回灌成长文墙。

---

## 1. 词表（先扫一遍，主讲后再回看）

### 1.1 观测与几何

| 术语 | 人话 | 稍严 |
|---|---|---|
| 双频 $f_1,f_2$ | 两把无线电尺子 | 如 GPS L1/L2 |
| 伪距 $P$（码） | 粗糙但有绝对尺度 | 噪声/多路径大 |
| 载波相位 $L$ | 精密但缺零点 | 含整周模糊度 |
| 几何距离 $\rho$ | 真几何路程（近似） | 对两频一阶公共 |
| 对流层 $T$ / 钟差 | 中性延迟 / 钟不准 | 一阶对两频公共 |
| 电离层 $I_i$ | 第 $i$ 频一阶延迟 | $I_i=40.3\,\mathrm{STEC}/f_i^{2}$ |

### 1.2 组合、偏差与工艺

| 术语 | 人话 | 稍严 |
|---|---|---|
| 几何无关 GF | 两频组合消公共几何 | 留电离层+偏差等 |
| 无电离层 IF | 定位里故意消掉 $I$ | 与 GF **目的相反** |
| 整周模糊度 $N$ | 不知从第几格起算 | 无周跳弧段内近常数 |
| 周跳 | 尺子掉了重拿 | 模糊度台阶变化 |
| 相位平滑 / leveling | 用相位约束伪距水平 | 绝对靠码，形状靠相 |
| DCB / IFB | 两频码延迟差 | 伪装成 TEC |
| RINEX / 观测类型 | 交换格式 / C1C、L1C… | 偏差产品必须对齐类型 |
| 弧段 | 连续无周跳时段 | 平滑常按弧段 |
| $\alpha$ | 米 → TECU 的尺子 | GPS L1/L2 ≈ 9.52 TECU/m |

**纪律**：未改 DCB 就说「测到真 TEC」不合格；应说「GF 换算值（尚未分离偏差）」或声明产品来源。听到「无电离层」不要当成「几何无关」。

---

# 第一段 · 机制

> 目标：用「因果」讲清——为何两频差分能看见电子柱、码与相位为何符号相反、DCB/周跳为何能毁掉一条「漂亮曲线」。公式只在需要时点名，完整推导留给第二段。

---

## 2. 为何双频能测 TEC？色散是根

![同一 STEC 在不同频率的延迟（色散）](./images/fig-iono-delay-vs-freq.png)

> **看图要点（为什么差能报电子柱）**：按 $I\approx40.3\cdot\mathrm{STEC}/f^{2}$ 绘制。频率越低延迟越大；**两条曲线的竖直差**才是 GF「看见」的东西——不是任一频率的绝对延迟。图源：自制 CC0，见 [`images/SOURCES.md`](./images/SOURCES.md)。

![GNSS 主要频段](./images/fig-gnss-freq-bands.png)

> **看图要点（为什么 L2 更「慢」）**：L1/L2/L5 同属 GHz，但 $I\propto 1/f^{2}$——频率越低，同一 STEC 延迟越大。双频差正是这两条曲线的竖直间距。图源：自制 CC0。

第一课已钉死：一阶群延迟 $I(f)=40.3\,\mathrm{STEC}/f^{2}$。同一路径、同一份电子柱，两把频率尺子读出**不同**延迟：

$$
\frac{I_2}{I_1}=\frac{f_1^{2}}{f_2^{2}}.
$$

GPS L1/L2：$f_1=1575.42\,\mathrm{MHz}$，$f_2=1227.60\,\mathrm{MHz}$，$f_1/f_2=154/120=77/60$，故 $I_2/I_1=(77/60)^{2}\approx1.647$。L2 更「慢」。

**机制一句话**：对流层、几何距离、钟差对两频几乎一样；电离层**强烈色散**。两频相减，公共项退出，色散项留下——这就是几何无关（geometry-free, GF）的物理根。

**因果链（请背）**：

1. 同一路径、同一份电子柱 → 两频延迟不同（$\propto 1/f^{2}$）。  
2. 几何 / 对流层 / 钟差对两频一阶相同 → 差分时被减掉。  
3. 差分留下的主要是 $(I_1-I_2)$（外加 DCB、多路径差、噪声）→ 乘频率因子 $\alpha$ → STEC。  
4. 没有第二把尺子，就没有「差」可测——只能模型猜。

**厨房类比**：两把温度计插进同一锅汤。若锅本身（几何）和房间温度（对流层）对两表一样，只有「汤里放了多少辣椒」（电子柱）让两表读数差不同——差分就报辣椒量。单频等于只有一把温度计：你只能查菜谱猜「该有多辣」，不能现测。

单频没有第二把尺子，只能用模型**猜** $I$（Klobuchar、NeQuick-G、IRI…）。双频是**测**色散差，再换成 STEC。

![单频猜 vs 双频测](./images/fig-singlefreq-vs-dualfreq.png)

> **看图要点（为什么必须双频）**：左栏单频只能拿气候/广播模型贴真延迟；右栏第二把尺子直接量色散差。**误读**：以为「单频改正完 = 测到了 TEC」。改正是猜，GF 才是测。图源：自制 CC0。

![双频差 → STEC 思路](./images/fig-dualfreq-tec.png)

> **看图要点（为什么减法有效）**：$P_1-P_2$（或 $P_2-P_1$）消去公共几何/对流层/钟差，留下色散项（及 DCB）。箭头背后的方程在第二段写全——本图只钉「差从哪来」。图源：自制 CC0。

---

## 3. 码 vs 相位：两把尺子，符号相反


![双频伪距差到 STEC](./images/fig-pseudorange-to-stec.png)

> **看图要点（为什么先看米再乘 $\alpha$）**：上方面板是吵闹的 $P_1-P_2$（米），下方乘上 $\alpha$ 得到 STEC——噪声先在米域放大再进 TECU。方程写在图上，不是流程框。图源：自制 CC0。

### 3.1 伪距（码）：绝对但吵

码测的是**群延迟**：电子柱让能量包络（码相关峰）传播变慢，伪距**变长** → 观测方程里写 $+I_i$。因果三句：

1. 色散介质中群折射率 $n_g>1$ → 群速 $<c$ → 码「迟到」。  
2. 迟到等效成多走了一段路 → 伪距偏大 → 方程里是**加号**。  
3. 伪距有绝对尺度（知道「大约多少米」），但噪声与多路径大——像木尺：刻度从零开始，但手抖。

### 3.2 载波相位：精密但缺零点

相位测的是**相路径**：一阶相位折射率 $n_p<1$，相位超前，方程里写 $-I_i$。因果三句：

1. 相速 $>c$（能量仍不超光速；相位是波峰位置）→ 载波相位「提前」。  
2. 提前等效成少走了一段路 → 相位距离偏小 → 方程里是**减号**。  
3. 相对变化极漂亮，但整周模糊度 $N_i$ 未知——像千分尺：你知道相对转了多少，不知道墙上零刻度在哪。

**课堂口诀**：伪距稳在绝对水平但吵；相位准在相对变化但缺零点；电离层对码 $+I$、对相 $-I$。同一份雾，两把尺子读数符号相反——这是色散关系（$n_g-1=-(n_p-1)$ 一阶）的直接后果，不是口诀炫技。

![码 +I / 相位 −I：同一份电子柱](./images/fig-code-phase-signs.png)

> **看图要点（为什么符号相反）**：上箭头变长（码群延迟），下箭头变短（相位超前）。同一份电子柱，两把尺子方向相反——GF 推导里码差与相位差因此带相反符号结构。**误读**：把码相延迟直接平均当「真延迟」。图源：自制 CC0。

### 3.3 几何无关在「减」什么？

![双频几何无关组合示意](./images/fig-dualfreq-geometry-free.png)

> **看图要点（为什么叫几何无关）**：两把尺子差分——公共几何/对流层/钟差退出，色散项留下。名字强调「几何被消」，不是「误差全消」。图源：自制 CC0，见 [`images/SOURCES.md`](./images/SOURCES.md)。

GF **不是**魔法橡皮擦。它只对**频率无关的公共项**做减法：

| 项 | 两频是否近似相同？ | 因果一句 | GF 后 |
|---|---|---|---|
| 几何距离 $\rho$ | 是（忽略天线相位中心频率差等小项） | 同一条射线几何路程 | **消掉** |
| 接收机/卫星钟差 | 是（一阶） | 钟不准不挑频率 | **消掉** |
| 对流层 $T$ | 是（L 波段几乎不色散） | 中性大气对两频几乎同延迟 | **消掉** |
| 电离层 $I_i$ | **否**，$\propto1/f_i^{2}$ | 色散 → 两频延迟不同 | **留下差** |
| 码硬件延迟 $b_i$ | **否** | 两频硬件延迟不同 | **留下 DCB** |
| 多路径/噪声 | 否 | 反射/热噪与频率相关 | 残留，常放大 |

**消什么 / 留什么（请默念）**：

- **消**：频率无关公共项（几何、一阶钟差、对流层）。  
- **留**：一切频率相关项——你想要的 $(I_1-I_2)$，以及你不想要的 DCB、多路径差、噪声差。  

**金句**：凡是频率相关的，都会留下来——GF 是筛子，不是消毒柜。

### 3.4 与「无电离层组合」一句话区分

![无电离层组合：权重消掉一阶 I](./images/fig-iono-free-combo.png)

> **看图要点（为什么 IF≠GF）**：右栏 IF 用加权消掉一阶 $I$、保住几何，服务定位，代价是噪声放大；本课 GF 方向相反。**误读**：把 IF 距离观测当成 TEC 图，或把「无电离层」听成「几何无关」。图源：自制 CC0。

定位里常见 **ionosphere-free（IF）**：故意把一阶 $I$ 消掉，留下几何，服务定位。  
本课 **geometry-free（GF）**：故意把几何消掉，留下 $I$，服务 TEC。  
二者系数不同、目的相反。搞混会整条流水线反着做。

---

## 4. 偏差与周跳：假 TEC 的两个机制源

### 4.1 DCB：仪器账假装成电子柱

![DCB 伪装成 TEC 偏移](./images/fig-bias-dcb.png)

> **看图要点（为什么像「多了一层楼」）**：未改正 DCB ≈ 整条 STEC 曲线整体平移数 TECU——形状还在，零点错了。像厨房秤没去皮：汤的起伏还对，读数整天高一截。图源：自制 CC0。

![DCB：整日平行抬升示意](./images/fig-dcb-parallel-shift.png)

> **看图要点（为什么是平行抬升）**：形状还在，整天差一截常数——白天夜里**一起**偏。**误读**：把平行偏移写成「白天 TEC 暴涨」或「暴时增强」。图源：自制 CC0。

卫星与接收机在两频上的码硬件延迟不同，差分后留下 $\mathrm{DCB}_{\mathrm{GF}}$。它与 $(I_1-I_2)$ 加在一起，乘 $\alpha$ 后看起来就像 TEC 整体抬升或压低——**白天夜里一起偏**，这是 DCB 的典型观测签名（见第三段）。

量级感：$1\,\mathrm{ns}\times c\approx0.30\,\mathrm{m}$；再 ×$\alpha\approx9.52\,\mathrm{TECU/m}$ → 约 $2.85\,\mathrm{TECU}$。几纳秒绝不可「太小忽略」。

### 4.2 周跳：模糊度台阶 = 假突变

连续跟踪时，组合模糊度 $B=\lambda_1 N_1-\lambda_2 N_2+\cdots$ 近常数。失锁或中断使整周数跳变 → $B$ 换常数 → 相位 GF 时间序列出现**台阶**。因果三句：

1. 相位方程里 $\lambda_i N_i$ 在无周跳弧段内当常数。  
2. 周跳 = $N_i$ 突然加/减整数 → 组合 $B$ 换一个新常数。  
3. STEC 曲线因此出现台阶；不切弧就平滑，会把假台阶抹成「缓变天气」。

量级感：L1 跳 +1 周 ≈ 0.19 m → 假 STEC ≈ $9.52\times0.19\approx1.8\,\mathrm{TECU}$（视 GF 定义）。一眼像天气事件，其实是尺子掉了重拿。

### 4.3 Leveling / 平滑：机制动机（公式见第二段）

生伪距 GF 噪声经 $\alpha$ 放大后可达数 TECU；相位 GF 相对变化漂亮但差一个未知 $B$。工程上：**码钉绝对水平，相描波形**——这叫 leveling（定水平）或载波平滑伪距。动机写在误差传播里，不是「把曲线弄好看」。顺序纪律：先周跳切弧 → 再 leveling/平滑 → 再谈「漂亮 STEC」。

---

# 第二段 · 公式拆解（逐步推导）

> 目标：每个符号有单位、有人话、有「这一步在干什么」。不要背「几何无关」四个字，要能复述推导链并手算 $\alpha$。

---

## 5. 公式路线图（先看全图，再逐步拆）

$$
I_i=\frac{40.3}{f_i^{2}}\,\mathrm{STEC}
\;\xrightarrow{\text{obs eq}}\;
P_i=\cdots+I_i,\quad L_i=\cdots-I_i+\lambda_i N_i
\;\xrightarrow{P_1-P_2}\;
\mathrm{GF}
\;\xrightarrow{\alpha}\;
\mathrm{STEC}
\;\xrightarrow{\text{leveling}}\;
\mathrm{STEC}_{\mathrm{lev}}(t).
$$

读法（中文在公式外）：延迟公式 → 写入码/相方程 → 差分消几何 → 频率因子换成 TECU → leveling 得到干净绝对 STEC。

---

## 6. 解剖台 A：观测方程——每个符号

> 解剖台统一格式：**符号表 → 逐步推导（每步人话）→ 小数值例**。

### 6.1 符号表（码与相共用骨架）

| 符号 | 含义 | 单位 / 备注 |
|---|---|---|
| $P_i$ / $L_i$ | 第 $i$ 频伪距 / 相位距离 | m |
| $\rho$ | 站星几何距离 | m；两频一阶公共 |
| $c(\delta t_r-\delta t^s)$ | 接收机与卫星钟差等效距离 | m；$c\approx2.99792458\times10^{8}\,\mathrm{m/s}$ |
| $T_{\mathrm{trop}}$ | 对流层延迟 | m；一阶与频率无关 |
| $I_i$ | 电离层一阶延迟 | m；$I_i=40.3\,\mathrm{STEC}/f_i^{2}>0$ |
| $b_{r,i},b^{s}_{i}$ | 接收机/卫星端**码**硬件延迟 | m |
| $\lambda_i,N_i$ | 波长、整周模糊度 | m、无量纲；$\lambda_i=c/f_i$ |
| $\delta_{r,i},\delta^{s}_{i}$ | 相位硬件延迟类项 | m |
| $\varepsilon_{P_i},\varepsilon_{L_i}$ | 码/相噪声与多路径 | m；相位通常小得多 |

### 6.2 逐步推导（每步一句人话）

1. 把「站星距离」拆成：真几何 + 钟差等效 + 对流层 + 电离层 + 硬件延迟 + 噪声。  
2. **伪距**吃的是群延迟 → 电离层项带**加号**：

$$
P_i=\rho+c(\delta t_r-\delta t^s)+T_{\mathrm{trop}}+I_i+b_{r,i}-b^{s}_{i}+\varepsilon_{P_i}.
$$

3. **相位**吃的是相位超前 → 电离层项带**减号**，并多出未知整周 $\lambda_i N_i$：

$$
L_i=\rho+c(\delta t_r-\delta t^s)+T_{\mathrm{trop}}-I_i+\lambda_i N_i+\delta_{r,i}-\delta^{s}_{i}+\varepsilon_{L_i}.
$$

4. 两式骨架几乎相同，差别钉在三处：$+I$ vs $-I$、有无 $\lambda N$、码延迟 $b$ vs 相位延迟 $\delta$。  
5. 波长口诀：L1 $\lambda_1\approx0.1903\,\mathrm{m}$，L2 $\lambda_2\approx0.2442\,\mathrm{m}$（$\lambda=c/f$）。

### 6.3 小数值例：同一 STEC 的 $I_1,I_2$

取 $\mathrm{STEC}=20\,\mathrm{TECU}=2.0\times10^{17}\,\mathrm{m}^{-2}$（沿用 01 课系数 40.3）：

$$
I_1=\frac{40.3\times2.0\times10^{17}}{(1.57542\times10^{9})^{2}}\approx3.25\,\mathrm{m},\qquad
I_2\approx5.35\,\mathrm{m}.
$$

验算比例：$I_2/I_1\approx5.35/3.25\approx1.646\approx(f_1/f_2)^{2}$。✓

再练一手：若 $\mathrm{STEC}=10\,\mathrm{TECU}$（减半），则 $I_1\approx1.625\,\mathrm{m}$，$I_2\approx2.675\,\mathrm{m}$，差 $I_2-I_1\approx1.05\,\mathrm{m}$——后面 $\alpha\times1.05\approx10\,\mathrm{TECU}$ 会接上。

---

## 7. 解剖台 B：几何无关组合——逐步推导

### 7.1 符号表

| 符号 | 含义 | 单位 / 备注 |
|---|---|---|
| $P_{\mathrm{GF}},L_{\mathrm{GF}}$ | 伪距 / 相位几何无关组合 | m |
| $\Delta t$ | $\delta t_r-\delta t^s$ | s |
| $T$ | $T_{\mathrm{trop}}$ 简写 | m |
| $\mathrm{DCB}_{\mathrm{GF}}$ | 码 GF 硬件延迟差 | m |
| $\alpha$ | 米 → TECU 的频率因子 | TECU/m；L1/L2≈9.52 |
| $B$ | 相位模糊度组合 | m；无周跳弧段内近常数 |

### 7.2 逐步推导（伪距 GF；每步人话）

写两式（令 $\Delta t=\delta t_r-\delta t^s$，$T=T_{\mathrm{trop}}$）：

$$
\begin{aligned}
P_1&=\rho+c\Delta t+T+I_1+(b_{r,1}-b^{s}_{1})+\varepsilon_{P_1},\\
P_2&=\rho+c\Delta t+T+I_2+(b_{r,2}-b^{s}_{2})+\varepsilon_{P_2}.
\end{aligned}
$$

1. **相减消公共项**：几何 $\rho$、钟差、对流层 $T$ 同时出现在两式 → 差分后消失。

$$
P_{\mathrm{GF}}\equiv P_1-P_2=(I_1-I_2)+(b_{r,1}-b_{r,2})-(b^{s}_{1}-b^{s}_{2})+\varepsilon_{P_1}-\varepsilon_{P_2}.
$$

2. **展开电离层差**（把 $I_i=40.3\,\mathrm{STEC}/f_i^{2}$ 代入）：

$$
I_1-I_2=40.3\,\mathrm{STEC}\left(\frac{1}{f_1^{2}}-\frac{1}{f_2^{2}}\right)=40.3\,\mathrm{STEC}\cdot\frac{f_2^{2}-f_1^{2}}{f_1^{2}f_2^{2}}.
$$

3. **符号约定**：因 $f_2<f_1$，$I_1-I_2<0$。有人定义 $P_2-P_1$ 使差分为正——**读软件时看清定义**。本课后文统一用 $P_2-P_1$。  
4. **解出 STEC**：把频率因子收成 $\alpha$，硬件延迟差收成 $\mathrm{DCB}_{\mathrm{GF}}$：

$$
\mathrm{STEC}=\frac{1}{40.3}\cdot\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}\big[(P_2-P_1)-\mathrm{DCB}_{\mathrm{terms}}\big]+\cdots
$$

$$
\mathrm{STEC}=\alpha\,(P_2-P_1-\mathrm{DCB}_{\mathrm{GF}})+\varepsilon.
$$

（$\varepsilon$：噪声与未建模项。）

### 7.3 手算 $\alpha$（本课毕业演算）

$$
\alpha=\frac{1}{40.3}\cdot\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}.
$$

代入 $f_1=1.57542\times10^{9}\,\mathrm{Hz}$，$f_2=1.22760\times10^{9}\,\mathrm{Hz}$：

1. $f_1^{2}\approx2.4819\times10^{18}$，$f_2^{2}\approx1.5070\times10^{18}$；  
2. $f_1^{2}-f_2^{2}\approx9.749\times10^{17}$（**频率差**写在分母——两频越近，$\alpha$ 越大、噪声越放大）；  
3. $f_1^{2}f_2^{2}\approx3.740\times10^{36}$；  
4. $f_1^{2}f_2^{2}/(f_1^{2}-f_2^{2})\approx3.836\times10^{18}$；  
5. $/40.3\Rightarrow\alpha\approx9.52\times10^{16}\,\mathrm{m}^{-2}/\mathrm{m}=9.52\,\mathrm{TECU/m}$。

**请在自己计算器上复现。** 不同教材因 $P_1-P_2$ 或 $P_2-P_1$ 差一个符号；本课统一对 $P_2-P_1$ 取 $\alpha>0$。

**频率差直觉**：若两频几乎重合，$f_1^{2}-f_2^{2}\to0$，$\alpha\to\infty$——差分尺子退化，1 mm 噪声也会被吹成天文数字 TEC。L1/L2 差得够开，才有可用的 $\alpha\sim9.52$。

### 7.4 相位 GF（符号表接上）

$$
L_{\mathrm{GF}}\equiv L_1-L_2=-(I_1-I_2)+\lambda_1 N_1-\lambda_2 N_2+\Delta\delta+\varepsilon_{L}.
$$

逐步人话：

1. 相位方程里电离层是 $-I_i$，故差分后电离层项相对伪距**差一个负号结构**。  
2. 令模糊度组合 $B=\lambda_1 N_1-\lambda_2 N_2+\cdots$ 在无周跳弧段内为**未知常数**。  
3. 于是 $L_{\mathrm{GF}}$ 的**时间变化**主要反映 STEC 的时间变化；**绝对水平**被 $B$ 拖住——这就是 leveling 的入口。

### 7.5 小数值例 A：假但真实的 L1/L2

设公共部分 $G:=\rho+c\Delta t+T=22{,}000{,}000.000\,\mathrm{m}$（数字只为演算）。真 STEC $=20\,\mathrm{TECU}$，$I_1=3.25\,\mathrm{m}$，$I_2=5.35\,\mathrm{m}$。暂令硬件延迟=0、噪声=0、模糊度先不管。

理想伪距：

$$
P_1=G+I_1=22{,}000{,}003.25\,\mathrm{m},\qquad
P_2=G+I_2=22{,}000{,}005.35\,\mathrm{m}.
$$

$$
P_2-P_1=+2.10\,\mathrm{m}\implies\mathrm{STEC}=\alpha\times2.10\approx9.52\times2.10\approx20.0\,\mathrm{TECU}.
$$

**要点**：两伪距只差约 2.1 m，却编码了 20 TECU；公共的两千万米被减掉了。

理想相位（忽略模糊度）：$L_1=G-I_1$，$L_2=G-I_2$，故

$$
L_1-L_2=-(I_1-I_2)=+2.10\,\mathrm{m},
$$

与伪距 GF（若用 $P_1-P_2=-2.10$）**符号结构相反**——正是 $+I$ vs $-I$ 的直接后果。实践中常统一符号使 $P_2-P_1$ 与 leveled 相位同向。

再验一手频率差：$I_2-I_1=2.10\,\mathrm{m}$ 恰等于例中差分；若 STEC 加倍到 40 TECU，差分应 ≈4.20 m，$\alpha\times4.20\approx40\,\mathrm{TECU}$。

---

## 8. 解剖台 C：模糊度、Leveling、平滑

### 8.1 符号表

| 符号 | 含义 | 单位 / 备注 |
|---|---|---|
| $N_i$ / $B$ | 单频整周 / GF 组合模糊度 | 无量纲 / m |
| $[t_a,t_b]$ | 无周跳弧段 | — |
| $\hat{B}$ | 弧段估得的模糊度水平 | m |
| $n$ | 载波平滑窗口长度 | 历元数；弧断即重置 |
| $\Phi$ | 相位距离（平滑用） | m |

### 8.2 逐步推导：模糊度 → leveling（每步人话）

1. 相位像精密千分尺：相对转角准，零点未知。$N_i$（及组合 $B$）在**连续跟踪、无周跳**时近似常数。  
2. 因此相位 GF：**相对 STEC 变化**极漂亮；**绝对 STEC 水平**要靠伪距 GF（或其它约束）来钉。  
3. 设弧段 $t\in[t_a,t_b]$ 已周跳清洁。定义（符号约定使电离层项同向）：

$$
P_{\mathrm{GF}}(t)=P_2(t)-P_1(t),\qquad
L_{\mathrm{GF}}(t)=L_1(t)-L_2(t).
$$

4. 实现时把 $L_{\mathrm{GF}}$ 统一到与 $P_{\mathrm{GF}}$ 同向。理想无噪无偏时，某约定下 $P_{\mathrm{GF}}+L_{\mathrm{GF}}\approx B$（常数）。  
5. 弧段平均估常数：

$$
\hat{B}=\frac{1}{N}\sum_{k=1}^{N}\big(P_{\mathrm{GF}}(t_k)\mp L_{\mathrm{GF}}(t_k)\big).
$$

$\mp$ 的符号依你的 $L_{\mathrm{GF}}$ 定义而定。  
6. 把相位序列平移到与伪距同一绝对水平 → **leveled phase TEC**，再乘 $\alpha$。  
7. **人话**：木尺钉高度，千分尺描波形。若先做了 DCB 改正，应在 $P_{\mathrm{GF}}$ 上改，再 leveling。

**权重变体**：伪距噪声大，可用低仰角降权、或只用高 CN0 历元估 $B$。不同软件默认不同——**对比结果前读 leveling 一节**。

### 8.3 载波平滑伪距（概念级）

Hatch 滤波一类的直觉：

$$
\hat{P}(t)=\frac{1}{n}P(t)+\frac{n-1}{n}\big(\hat{P}(t-1)+\Phi(t)-\Phi(t-1)\big),
$$

其中 $\Phi$ 为相位距离，$n$ 为平滑窗口（有上界）。人话：新伪距给一点绝对信息，相位差分提供低噪增量。弧段一断，$n$ 重置。

**误解**：平滑=低通乱抹；或平滑能消灭周跳。错。先探测/按弧段断开，再平滑。

### 8.4 小数值例 B：串起模糊度与 DCB

沿用例 A：$I_2-I_1=2.10\,\mathrm{m}$，真 STEC=20 TECU。现设总码 GF 偏差使观测

$$
P_2-P_1=(I_2-I_1)+\Delta b=2.10+0.40=2.50\,\mathrm{m}.
$$

若不改 DCB：$\mathrm{STEC}_{\mathrm{raw}}=9.52\times2.50\approx23.8\,\mathrm{TECU}$（偏高约 3.8 TECU）。

相位侧：设 $B=12.00\,\mathrm{m}$（未知常数）。在与 $P_2-P_1$ 同向的约定下，相位 GF 观测 = $2.10+12.00=14.10\,\mathrm{m}$。时间上 STEC 变，$2.10$ 变，$B$ 不变 → 曲线形状对，水平错。Leveling 把相位平移到与（DCB 改正后的）伪距一致：例如估得 $\hat{B}\approx12.00$，则 leveled 相位距离 ≈ $14.10-12.00=2.10\,\mathrm{m}$ → $\alpha\times2.10\approx20\,\mathrm{TECU}$。

**周跳**：某时刻 $B:12.00\to12.00+\lambda_{\mathrm{eff}}$ → 曲线台阶。例：L1 跳 +1 周 ≈0.19 m → 假 STEC 跳 ≈$9.52\times0.19\approx1.8\,\mathrm{TECU}$。平滑前必须切弧或修复。

---

## 9. 解剖台 D：DCB 预告式、噪声放大、换频

### 9.1 符号表

| 符号 | 含义 | 单位 / 备注 |
|---|---|---|
| $\mathrm{DCB}_{\mathrm{GF}}$ | 码 GF 硬件延迟差 | m |
| $\sigma_P,\sigma_L$ | 单频伪距 / 相位噪声 | m |
| $\sigma_{\mathrm{STEC}}$ | 换算后 STEC 噪声 | TECU |
| $\alpha_{15}$ | L1/L5 频率因子 | TECU/m；≈7.76 |
| $M(E)$ | 映射函数 | 无量纲；见 01 |

### 9.2 逐步推导：DCB 进入 GF（每步人话）

1. 两频码硬件延迟不同 → 差分后**不会**被消掉：

$$
P_2-P_1=(I_2-I_1)+\underbrace{(b_{r,2}-b_{r,1})-(b^{s}_{2}-b^{s}_{1})}_{\approx\mathrm{DCB}_{\mathrm{GF}}}+\varepsilon.
$$

2. 预告级改正（符号随产品定义与差分方向而变；以文档为准）：

$$
\mathrm{STEC}_{\mathrm{raw}}=\alpha(P_2-P_1),\qquad
\mathrm{STEC}_{\mathrm{corr}}=\alpha\big(P_2-P_1-\mathrm{DCB}_{\mathrm{GF}}\big).
$$

3. 实务四条：卫星端优先用公开 DCB/OSB；接收机端常当未知数；**观测类型必须对齐**（C1C≠C1W）；深度见 [09](./09-dcb-biases-deep.md)，本仓可点名 `Gkit-Bias`。  
4. **纳秒口诀**：$1\,\mathrm{ns}\approx0.30\,\mathrm{m}\approx2.85\,\mathrm{TECU}$（L1/L2）；$0.1\,\mathrm{m}\approx0.95\,\mathrm{TECU}$。

### 9.3 逐步推导：噪声如何被 $\alpha$ 放大

1. 设单频 $\sigma_P\approx0.3\,\mathrm{m}$，两频独立 → 差分噪声 $\sqrt{2}$ 倍。  
2. 再乘 $\alpha$：

$$
\sigma(P_2-P_1)\approx\sqrt{2}\,\sigma_P\approx0.42\,\mathrm{m},\qquad
\sigma_{\mathrm{STEC}}\approx9.52\times0.42\approx4\,\mathrm{TECU}.
$$

3. 这就是「生伪距 GF TEC 很吵」的数量来源；相位 $\sigma_L\approx0.003\,\mathrm{m}$ 量级时 GF 后仍远小于伪距。  
4. Leveling/平滑的一半动机写在这道误差传播里。  
5. 低仰角多路径使 $\sigma_P\to1\,\mathrm{m}$ 时，生伪距 STEC 噪声可到 ~10 TECU——不截止仰角，任何「精细结构」论文都可疑。

### 9.4 换频：L1/L5 的 $\alpha$ 不同

GPS L5 $f_5=1176.45\,\mathrm{MHz}$：

$$
\alpha_{15}=\frac{1}{40.3}\frac{f_1^{2}f_5^{2}}{f_1^{2}-f_5^{2}}\approx7.76\,\mathrm{TECU/m}.
$$

**含义**：同样 1 m 的差分，换成 TECU 的尺子与 L1/L2 不同。混用频率对却套错 $\alpha$，尺度必歪。DCB 产品也必须覆盖该频率对/码类型。多系统（BDS、Galileo）原则不变，入门先单系统跑通。

### 9.5 小数值例：迷你流水线（米 → STEC → VTEC）

已 DCB、无周跳、leveling 完成：$P_2-P_1=2.35\,\mathrm{m}$。

1. $\mathrm{STEC}=9.52\times2.35\approx22.4\,\mathrm{TECU}$。  
2. 仰角 $E=35°$，$H=450\,\mathrm{km}$（用 01 课映射）：$M\approx1.55$。  
3. $\mathrm{VTEC}\approx22.4/1.55\approx14.5\,\mathrm{TECU}$。  
4. 与 GIM 在 IPP 插值比：差 0.5 TECU 可属噪声/模型；差 8 TECU 且全日同号 → 先查 DCB。

穿刺点几何可点名 `Get_IPP`；薄壳细节回 [01](./01-ionosphere-tec-basics.md)。

![薄壳几何：斜路径 STEC 与穿刺点 VTEC](./images/fig-stec-vtec-shell.png)

> **看图要点（为什么 STEC≠VTEC）**：斜水管穿薄壳 → IPP；竖直雾厚 = VTEC；斜管总量 ≈ $M(E)\times$ VTEC。本课先交出 STEC；映射是另账，别把未映射 STEC 直接减 GIM VTEC。图源：自制 CC0。

---

# 第三段 · 观测签名

> 目标：看见 STEC 时间序列或与 GIM 对比图时，能说出「这是什么长相、因果是什么、别和什么搞混」；四种工艺签名能**一眼区分**。  
> 深度现象剧本留给 [19–23](./19-phenomena-overview.md)；本课只建立**测量工艺的第一眼签名**。

---

## 10. STEC 时间序列上会长什么样？

### 10.0 一眼区分：好弧 / 周跳 / 多径 / 残余偏差

| 签名 | 一眼抓手 | 因果 | 别当成 |
|---|---|---|---|
| **好弧** | 日变化轮廓光滑；高仰角多星映射后彼此靠近 | 周跳已切、DCB 已齐、噪声被 leveling 压住 | 「光滑 = 真值」——绝对水平仍靠码与 DCB |
| **周跳** | **突然台阶**后平移到新水平；常单星、单弧 | 模糊度组合 $B$ 换常数 | TID / 暴时突变（那些很少呈完美台阶） |
| **多径 / 低仰角噪** | 仅低仰角疯抖；高仰角正常；伪距 GF 比相位抖 | 反射路径 + $M(E)$ 放大 | 闪烁（闪烁看 S4/σφ/ROTI，见 05） |
| **残余偏差（DCB 等）** | 相对 GIM **全日平行抬升/压低**；白天夜里一起偏 | $\mathrm{DCB}_{\mathrm{GF}}$ 或类型错配进 GF | 「白天 TEC 暴涨 30%」 |

**口诀**：台阶 → 周跳；平行平移 → DCB；只在低仰角疯 → 多径；轮廓对、水平对、抖得合理 → 才谈好弧。

### 10.1 安静日「气候」形状（测量侧）

| 看什么 | 常见长相 | 别误读 |
|---|---|---|
| 生伪距 GF STEC | 日变化轮廓在，但抖数 TECU | 抖 ≠ 闪烁；多是码噪/多路径 |
| Leveled 相位 STEC | 同轮廓，平滑得多 | 绝对水平仍依赖码与 DCB |
| 高仰角多星 | 映射后 VTEC 彼此更靠近 | 仍非「真值」 |

安静日 STEC 常随地方时正午升高、夜间下降（机制见 01）。本课关心的是：**你的曲线是真日变化，还是 DCB/周跳画出来的？**

### 10.2 DCB：全日整体平移

| 签名 | 长相 | 因果 |
|---|---|---|
| 相对 GIM / 邻站 | 白天夜里**一起**偏高或偏低数 TECU | $\mathrm{DCB}_{\mathrm{GF}}$ 进 GF |
| 换接收机后 | 旧偏差突然失效 | 接收机 DCB 不能无限期沿用 |
| 换观测类型 | 平移量突变 | C1C≠C1W 账本 |

**纪律**：整体平移优先查 DCB/类型/$\alpha$ 符号；不要先喊「电离层增强了 30%」。

### 10.3 周跳：台阶与假事件

| 签名 | 长相 | 处置 |
|---|---|---|
| 相位 GF / leveled STEC | 突然台阶后平移到新水平 | 切弧或修复（`cycle-slip-correction`、`DRCycleSlip`） |
| 未切弧就平滑 | 台阶被抹成「缓变天气」 | 先探测，再平滑 |
| 与「真天气」比 | 台阶常近乎瞬时、幅度接近 $\alpha\cdot\lambda$ 量级 | 真 TID/暴时少见完美台阶 |
| 质检线索 | `TEQC`、`Anubis` | 先看病历再开药 |

### 10.4 低仰角：几何 + 多路径假天气

低仰角 $M(E)$ 放大（01 课），多路径亦放大。签名：仅低仰角疯抖、高仰角正常。设截止角（常见 10°–20° 量级，视应用）；对比「事件」前先问仰角。

### 10.5 与 GIM 对比的诊断口诀

| 症状 | 优先怀疑 |
|---|---|
| 全日相对 GIM 整体偏高/偏低数 TECU | DCB/类型错配、$\alpha$ 符号 |
| 某段突然台阶后平移 | 周跳未切弧 |
| 仅低仰角疯抖 | 多路径；截止角 |
| 夜侧大量负 TEC | 周跳、DCB、单位、弧段 leveling 失败 |
| 与 GIM「形状全拧」 | 时间错位、频率对错、错误卫星系统混用 |
| 数值大/小约 10 倍 | TECU 缩放；IONEX 0.1 TECU 存储习惯（03 课） |
| STEC 直接减 GIM VTEC 就判死刑 | 先问映射、壳高、IPP、时间 |

**分析纪律**：**没有 DCB/周跳/映射三问，就没有资格说「我的算法比官方差 8 TECU」。**

### 10.6 TEC 大 ≠ 闪烁强（再次钉死）

本课产出的是柱含量 STEC/VTEC。闪烁看小尺度不规则性。高 TEC 安静等离子体可以几乎不闪；详见 [05](./05-scintillation-roti.md)。

---

# 第四段 · 分析步骤

> 目标：给你一套可执行的值班清单——从 RINEX 到 STEC；**每步补失败模式**；并完成演算过关。

---

## 11. RINEX → STEC：全清单与失效模式

| 步 | 做什么 | 失败模式（补强） | 一眼后果 |
|---|---|---|---|
| 1 | 确认双频观测类型存在 | 单频强行 GF；把 IF 观测当 GF | 无意义曲线或尺度全拧 |
| 2 | 读 RINEX：时间、PRN、$P,L$、（可选）CN0 | 类型读错列；时间戳时区错 | 垃圾进垃圾出。工具：`georinex`、`rinex`、`PyRINEX` |
| 3 | 解压/转换若需要 | Hatanaka 未解压就读；版本混用 | 缺观测 / 读失败。`crx2rnx`、`hatanaka`、`RNXCMP`、`GFZRNX` |
| 4 | 时间与系统对齐 | GPS/BDS 周错位；跨天未处理 | 错星错历元组合 |
| 5 | 仰角截止 + 粗差剔除 | 截止角过低或不做 | 低仰角多路径主导「假天气」 |
| 6 | 周跳探测与弧段划分 | 漏检；或检了却整段硬平滑 | 假台阶进 STEC。`cycle-slip-correction`、`DRCycleSlip`；质检 `TEQC`、`Anubis` |
| 7 | 组伪距/相位 GF | 频率对选错；$P_1-P_2$ 与 $\alpha$ 符号打架 | 尺度错或符号反 |
| 8 | Leveling / 相位平滑（按弧段） | 跨周跳 leveling；窗口跨弧 | 绝对水平吵或假台阶被抹 |
| 9 | 改正 DCB（类型对齐） | 产品类型与观测类型不对齐；忘改正 | 整条曲线平移数 TECU。`Gkit-Bias` |
| 10 | 乘频率因子 $\alpha$ → STEC(t)（TECU） | 套错 $\alpha$（如 L1/L5 仍用 9.52）；m 当 TECU | 尺度崩或故事崩 |
| 11 | （可选）薄壳+IPP→VTEC | 壳高/映射未声明就与 GIM 横比 | 假冲突。`Get_IPP` |

**算出后体检**：单位是否 TECU？夜侧是否大量离谱负值？高仰角多星映射 VTEC 是否大致接近？与 GIM 比是整体平移（优先 DCB）还是形状全拧（周跳/频率/时间）？低仰角是否单独检查？

**头脑伪代码（不绑定语言）：**

```
for each station-day RINEX:
  types = list_obs_types()
  assert dual_frequency(types)
  for each satellite:
    elev = compute_elevation(...)
    drop if elev < cutoff
    detect_cycle_slips(L1, L2) -> split arcs
    for each clean arc:
      P_GF = P2 - P1
      L_GF = align_sign(L1 - L2)
      P_GF = apply_satellite_DCB(P_GF, obs_type, product)
      B_hat = mean(P_GF ∓ L_GF)   # sign per convention
      L_lev = L_GF 平移到与 P_GF 同水平
      STEC = alpha * (L_lev 或 smoothed P_GF)
      optionally estimate receiver DCB as daily constant
      write STEC(t); optionally map to VTEC via M(E), IPP
```

对照上表逐行打勾。任何开源工具（`gnss-tec`、`Seemala-GPS-TEC`、`tec-suite` 等）都应能在 README 里找到对应开关。找不到 DCB 或周跳章节，就降低对其绝对 TEC 的信任，改只信相对变化。

**定位套件** `gLAB`、`RTKLIB`、`laika`、`PRIDE-PPPAR`、`GAMPII-GOOD` 可能含电离层组合，但**不要默认 PPP 一次跑完 = 可发表 STEC 产品**。

---

## 12. 常见误解专节

| # | 误解 | 打假 |
|---|---|---|
| A | GF 后没有误差 | 只消频率无关公共项；DCB/多路径/噪声仍在 |
| B | 相位 TEC 更真，可扔掉伪距 | 相位缺绝对水平；要 leveling |
| C | 平滑 = 随便低通 | 先周跳切弧；平滑有窗口与重置 |
| D | DCB 太小可忽略 | 数 ns → 数 TECU |
| E | 任意两频随便减 | 类型与偏差产品必须对齐；$\alpha$ 要重算 |
| F | RINEX 有 L1/L2 = 高质量双频 | 还要看完整性、CN0、周跳率 |
| G | STEC 减 GIM VTEC 就判算法死刑 | 先问映射/壳高/时间/DCB |
| H | 周跳修好 = 模糊度已固定成正确整数 | 难度不是同一级 |
| I | 「无电离层」=「几何无关」 | IF 消 $I$；GF 留 $I$ |
| J | 负 TEC = 负电子 | 先查周跳、DCB、单位、符号 |
| K | 单频也能做本课 GF | 不能；单频只能模型猜 |
| L | 换频仍用 9.52 | L1/L5 等必须重算 $\alpha$ |

### 误解 M：「leveled 相位 STEC 很光滑 = 绝对水平已经正确」（补坑）

光滑只说明相对变化被相位约束住了。绝对水平仍钉在伪距 GF（及 DCB）上。DCB 错 0.4 m，leveled 曲线照样漂亮地错 3.8 TECU——**好看 ≠ 水平对**。

### 误解 N：「$P_2-P_1$ 与软件默认 $P_1-P_2$ 差个符号，乘负 $\alpha$ 就行，不必改文档」（补坑）

符号约定必须与 $\alpha$ 定义、DCB 产品符号、相位 leveling 同向约定**整条链一致**。只在最后乘个负号，常把 DCB 改正方向也弄反，平移加倍。

### 误解 O：「夜侧出现负 TECU，说明电离层电子变负了」（补坑）

电子柱不能为负。夜侧大量负值优先查：周跳未切弧、DCB/类型错、GF 符号反、单位（把 m 当 TECU）、弧段太短 leveling 失败。先排工艺，再谈物理。

---

## 13. 和本仓库工具对上号

下列 `name` 均已对照根目录 `PROJECTS.json` 核验存在。本仓是索引，不内嵌上游完整源码。

| 目的 | name |
|---|---|
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`TEC-calculation-MATLAB`、`ionotec`、`PyTECGg`、`TEC_calculation_RINEX3` |
| 读 RINEX | `georinex`、`rinex`、`PyRINEX` |
| 压缩转换 | `crx2rnx`、`hatanaka`、`RNXCMP`、`GFZRNX` |
| 质检/周跳 | `TEQC`、`Anubis`、`cycle-slip-correction`、`DRCycleSlip` |
| 穿刺点 | `Get_IPP` |
| 偏差 | `Gkit-Bias` |
| 产品对比预告 | `CDDIS-IONEX`、`SH-GIM`、`mosgim` |

流程物理根 → [01-ionosphere-tec-basics.md](./01-ionosphere-tec-basics.md)；读 IONEX / 建图 → [03-gim-ionex.md](./03-gim-ionex.md)；DCB 深挖 → [09-dcb-biases-deep.md](./09-dcb-biases-deep.md)。

**别做**：把本索引仓当数据中心；未声明 DCB/周跳就发「精密 STEC」论文图；把 STEC 当 VTEC 与 GIM 打架。

---

## 14. 课堂测验（带演算的完整答案）

> **阅读提示：** 请在 github.com 网页预览本文。下面答案刻意写成纯文本，避免公式块在测验区露源码。

**题 1.** 伪距与相位方程里电离层项符号各是什么？为什么？  
**答：** 伪距 +I（群延迟）；相位 −I（相位超前）；来自 n_g−1>0、n_p−1<0。

**题 2.** 写出 P_GF = P_1−P_2 后剩下的主要项。  
**答：** I_1−I_2 + 接收机/卫星码延迟差 + 噪声多路径。

**题 3.** 例 A 中 I_1=3.25 m，I_2=5.35 m。P_2−P_1 与（忽略模糊度时）同向相位差各多少？用 α=9.52 还原 STEC。  
**答：** 2.10 m；STEC≈20.0 TECU。

**题 4.** 模糊度在无周跳弧段内扮演什么角色？Leveling 在干什么？  
**答：** 未知常数偏置；用伪距 GF 把相位 GF 平移到正确绝对水平。

**题 5.** Δb=+0.40 m 混入 P_2−P_1 且不改 DCB（相对 2.10 m、20 TECU 标尺），约导致多少 TECU 偏差？  
**答：** 约 20×0.40/2.10≈3.8 TECU（或 9.52×0.40≈3.8）。

**题 6.** 列出 RINEX→STEC 至少六步，并各给一种失效模式。  
**答：** 见第 11 节表（读数、仰角、周跳、GF、平滑、DCB、换算等）。

**题 7.** 为何观测类型要和 DCB 产品对齐？举本仓一个偏差相关 name、两个 TEC 估计 name。  
**答：** 不同码类型偏差定义不同。Gkit-Bias；如 gnss-tec、Seemala-GPS-TEC。

**题 8.** 只有单频能否做本课 GF TEC？你的 STEC 与 GIM VTEC 相减前要问什么？  
**答：** 不能。是否映射、壳高、时间、IPP、DCB。

**题 9.** GPS I_2/I_1≈1.647。若 I_1=4.00 m，I_2≈？  
**答：** ≈6.59 m。

**题 10.** 周跳在相位 GF 序列上通常长什么样？平滑前应怎样？  
**答：** 台阶；先探测/修复或按弧段断开。

**题 11.** 1 ns 的 GF 码偏差约多少米、多少 TECU（L1/L2，α≈9.52）？  
**答：** ≈0.30 m；≈2.85 TECU。

**题 12.** IF 与 GF 目的各一句。  
**答：** IF 消 I 保几何（定位）；GF 消几何留 I（TEC）。

**题 13.** 手算 α 的数量级：约多少 TECU/m（GPS L1/L2）？L1/L5 大约更大还是更小？  
**答：** ≈9.52；L1/L5 更小（≈7.76）。

**题 14.** 生伪距 σ_P≈0.3 m、两频独立时，σ_STEC 约多少 TECU？这解释了什么工程选择？  
**答：** ≈4 TECU；解释为何要相位 leveling/平滑。

**题 15.** 一眼区分：曲线突然台阶后平移，优先怀疑什么？全日相对 GIM 平行偏高 5 TECU，优先怀疑什么？仅低仰角疯抖呢？  
**答：** 周跳；DCB/类型/α 符号；多路径（先查截止角）。

**题 16.** 为何 leveled 很光滑仍可能绝对水平错数 TECU？  
**答：** 光滑来自相位相对约束；绝对水平仍靠伪距与 DCB——DCB 错则整条漂亮地错。

---

## 15. 综合演算作业（建议限时 25 分钟）

已知某弧段无周跳。某历元 DCB 已改正后的伪距：$P_1=22{,}150{,}012.40\,\mathrm{m}$，$P_2=22{,}150{,}015.55\,\mathrm{m}$。相位 GF 已 leveling，使该历元相位导出的 STEC 与伪距一致。取 $\alpha=9.52\,\mathrm{TECU/m}$（对 $P_2-P_1$）。

**(1)** $P_2-P_1=?$  
**(2)** STEC≈?  
**(3)** 若未改正的 DCB 使 $P_2-P_1$ 少了 0.50 m，STEC 偏差约多少 TECU？  
**(4)** 若仰角 $30°$、$H=450\,\mathrm{km}$、$M\approx1.70$（用 01 课结果），等效 VTEC≈?

**参考答案（纯文本）：**

(1) 3.15 m。  
(2) 9.52×3.15≈30.0 TECU。  
(3) 9.52×0.50≈4.8 TECU。  
(4) 30.0/1.70≈17.6 TECU。

**加练 A：** 真 STEC=15 TECU 时，相对例 A（20 TECU、差 2.10 m），理想 $P_2-P_1=1.575\,\mathrm{m}$。若未建模 DCB 使观测变成 1.825 m：未改正 STEC≈17.4 TECU（偏高 2.4）；改正后 15.0；仰角 60°、$M\approx1.13$ 时 VTEC≈13.3 TECU。

**加练 B（噪声）：** 若单频 $\sigma_P=0.5\,\mathrm{m}$，估 $\sigma(P_2-P_1)$ 与 $\sigma_{\mathrm{STEC}}$（$\alpha=9.52$）。  
参考：≈0.71 m；≈6.7 TECU——说明为何低仰角、未平滑的伪距 GF 不适合谈「亚 TECU 结构」。

---

## 16. 板书八行 · 符号速查 · 口述检查

**板书八行：**

1. $P=+I$，$L=-I$；$I=40.3\,\mathrm{STEC}/f^{2}$。  
2. $P_2-P_1=(I_2-I_1)+\mathrm{DCB}_{\mathrm{GF}}+\varepsilon$。  
3. $\mathrm{STEC}=\alpha(P_2-P_1-\mathrm{DCB}\ldots)$，L1/L2 上 $\alpha\sim9.52\,\mathrm{TECU/m}$。  
4. 相位 GF 多一个常数模糊度组合 $B$。  
5. Leveling/平滑：码定水平，相描形状；先处理周跳。  
6. DCB 伪装成 TEC；类型对齐；`Gkit-Bias`。  
7. 第 11 节清单：每步都有失效模式。  
8. 对比 GIM 前先统一 STEC/VTEC/映射/DCB；IF≠GF。

**符号速查卡：**

$$
P_i=\cdots+I_i+\cdots,\quad L_i=\cdots-I_i+\lambda_i N_i+\cdots,
$$

$$
P_2-P_1=(I_2-I_1)+\mathrm{DCB}_{\mathrm{GF}}+\varepsilon,
$$

$$
\alpha=\frac{1}{40.3}\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}\sim9.52\,\mathrm{TECU/m}\ (\mathrm{GPS\ L1/L2}),
$$

$$
\mathrm{STEC}=\alpha(P_2-P_1-\mathrm{DCB}\ldots),\quad
1\,\mathrm{ns}\approx0.30\,\mathrm{m}\approx2.85\,\mathrm{TECU}.
$$

**值班速算条（建议抄卡片）：**

- $\alpha_{L1L2}\approx9.52\,\mathrm{TECU/m}$（对 $P_2-P_1$）。  
- $1\,\mathrm{ns}\approx0.30\,\mathrm{m}\approx2.85\,\mathrm{TECU}$。  
- $0.1\,\mathrm{m}\approx0.95\,\mathrm{TECU}$。  
- 周跳 +1 周 @L1 ≈0.19 m≈1.8 TECU（视 GF 定义）。  
- 先周跳切弧，再 leveling，再 DCB，再乘 $\alpha$。  
- 与 GIM 比：平移→DCB；拧巴→周跳/时间/频率对。

**口述检查（任抽三问）：**

1. 在黑板上从 $P_1,P_2$ 推出 $P_2-P_1$，圈出 DCB。  
2. 解释为何理想情况下码 GF 与相位 GF 携带相反符号结构。  
3. 手算：$P_2-P_1=1.05\,\mathrm{m}$，$\alpha=9.52$，STEC=?  
4. 描述 leveling 三步。  
5. 给出「整体平移 vs 形状全拧」的诊断口诀。  
6. 说出三个本仓 RINEX→TEC 相关 `name`。

合格标准：能写方程、能算 $\alpha$ 应用题，不只会背「几何无关」四个字。

---

## 17. 与前后课的接口 · 出门任务

| 你现在会的 | 下一课才会的 | 不要提前假装会 |
|---|---|---|
| 从 $P_1,P_2$ 解出 STEC | 多站建 GIM、IONEX 字段 | 「彩图 = 真值」 |
| DCB 进 GF 的预告式 | DCB 产品深挖与类型迷宫 | 不问 README 就发论文图 |
| 周跳切弧 + leveling | 闪烁指数 / ROTI | 把抖当成 TEC 物理 |
| 点名 `gnss-tec` 等 | 空间天气专题分析流程 | 「活跃」二字交差 |

从 01 带来：$I=40.3\,\mathrm{STEC}/f^{2}$；码相符号；STEC vs VTEC；$M(E)$。  
本课交出：STEC(t) 时间序列（最好已 DCB、已周跳处理）。  
交给 03：多站 STEC + IPP + 映射 → 格网/球谐 VTEC → IONEX。

**能不映射就不急着映射**：若科研问题只关心相对 STEC 变化或扰动检测，可直接分析 STEC，少一层薄壳假设污染。

**下一课**：[03-gim-ionex.md](./03-gim-ionex.md)——多站 STEC 映射汇成 VTEC 场；IONEX 字段；分析中心。

**出门任务**：

1. 抄写第 11 节清单成一页检查表；  
2. 对一份双频 RINEX 只完成「列出观测类型、确认双频」；  
3. 用手算复现第 7.2 节 $\alpha\approx9.52\,\mathrm{TECU/m}$。

**版本说明**：本文件按「机制 → 公式拆解 → 观测签名 → 分析步骤」与 01/07/09 课同深度加厚；机制写透色散因果与 GF 消/留；各解剖台统一「符号表→逐步推导→小数值例」；观测签名补好弧/周跳/多径/残余偏差一眼表；分析清单与误解 M–O 补失败模式；嵌入 `fig-dualfreq-*`、`fig-gnss-freq-bands`、`fig-code-phase-signs`、`fig-singlefreq-vs-dualfreq`、`fig-stec-vtec-shell` 等自制 CC0 图；引用项目名均来自 `PROJECTS.json` 核验。现象课 19–23 保持独立短文，不回灌成长文墙。

**相关软件 / 数据入口**：[`georinex`](../software/georinex.md) · [`gfzrnx`](../software/gfzrnx.md) · [`pytecgg`](../software/pytecgg.md) · [`data-access`](../data-access.md)

（完）
