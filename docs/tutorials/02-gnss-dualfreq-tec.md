# 02 · 双频 GNSS 怎么估 TEC（几何无关、平滑、DCB）

> **课堂定位**：接第一课。你已知道 \(I\approx40.3\,\mathrm{STEC}/f^{2}\) 与码/相一阶符号相反。本课把这句话写进观测方程，逐步推出几何无关（GF）组合，用**假但真实量级的 L1/L2 数字**算一遍；讲清相位模糊度、leveling/平滑、DCB 如何进入 GF；给出 RINEX→STEC 全清单与失效模式。
>
> **写给谁**：第一次打开 RINEX、第一次听到「几何无关」「整周模糊度」「DCB」的人。

---

## 1. 这节课要解决什么

**现场甲**：师兄丢一天 RINEX，说「算 TEC」。你不知道用哪两列、要不要先改周跳、为何和 GIM 对不上。  
**现场乙**：STEC 白天比官方高七八 TECU，晚上也高——有人说没改 DCB。DCB 怎能假装成电子柱？  
**现场丙**：相位曲线漂亮，伪距像心电图。师兄说「载波平滑」。平滑是糊直线吗？

**交付**：用观测方程讲清码/相与 \(+I/-I\)；逐步推导 GF 并完成数值例；解释模糊度与 leveling/平滑；写出 DCB 进入 GF 的预告式；按清单从 RINEX 走到 STEC 并知道每步失效模式；能点名本仓真实工具。

**边界**：要有双频（或多频）观测才谈 GF TEC；单频只能模型改正。本课不建 GIM（03），不把 IRI 当实测（04），不把闪烁当 TEC（05）。

---

## 2. 词表

| 术语 | 人话 | 稍严 |
|---|---|---|
| 双频 \(f_1,f_2\) | 两把无线电尺子 | 如 GPS L1/L2 |
| 伪距 \(P\)（码） | 粗糙但有绝对尺度 | 噪声/多路径大 |
| 载波相位 \(L\) | 精密但缺零点 | 含整周模糊度 |
| 整周模糊度 \(N\) | 不知从第几格起算 | 无周跳弧段内近常数 |
| 周跳 | 尺子掉了重拿 | 模糊度台阶变化 |
| 几何距离 \(\rho\) | 真几何路程（近似） | 对两频公共 |
| 对流层 \(T\) / 钟差 | 中性延迟 / 钟不准 | 一阶对两频公共 |
| 电离层 \(I_i\) | 第 \(i\) 频一阶延迟 | \(I_i=40.3\,\mathrm{STEC}/f_i^{2}\) |
| 几何无关 GF | 两频组合消公共几何 | 留电离层+偏差等 |
| 相位平滑 / leveling | 用相位约束伪距水平 | 绝对靠码，形状靠相 |
| DCB / IFB | 两频码延迟差 | 伪装成 TEC |
| RINEX / 观测类型 | 交换格式 / C1C、L1C… | 偏差产品必须对齐类型 |
| 弧段 | 连续无周跳时段 | 平滑常按弧段 |

**纪律**：未改 DCB 就说「测到真 TEC」不合格；应说「GF 换算值（尚未分离偏差）」或声明产品来源。

---

## 3. 码 vs 相位：观测方程与符号相反

### 3.1 极简伪距（码）方程

对频率 \(i=1,2\)（单位：米）：

\[
P_i=\rho+c(\delta t_r-\delta t^s)+T_{\mathrm{trop}}+I_i+b_{r,i}-b^{s}_{i}+\varepsilon_{P_i}.
\]

| 符号 | 含义 |
|---|---|
| \(P_i\) | 第 \(i\) 频伪距观测（m） |
| \(\rho\) | 站星几何距离（m） |
| \(c(\delta t_r-\delta t^s)\) | 接收机与卫星钟差等效距离 |
| \(T_{\mathrm{trop}}\) | 对流层延迟（m，一阶与频率无关） |
| \(I_i\) | 电离层一阶**群**延迟（m），\(I_i=40.3\,\mathrm{STEC}/f_i^{2}>0\) |
| \(b_{r,i},b^{s}_{i}\) | 接收机/卫星端码硬件延迟（m） |
| \(\varepsilon_{P_i}\) | 噪声、多路径等 |

码测的是群延迟：电子柱让伪距**变长**，故 \(+I_i\)。

### 3.2 极简载波相位方程

\[
L_i=\rho+c(\delta t_r-\delta t^s)+T_{\mathrm{trop}}-I_i+\lambda_i N_i+\delta_{r,i}-\delta^{s}_{i}+\varepsilon_{L_i}.
\]

| 符号 | 含义 |
|---|---|
| \(L_i\) | 相位观测换成的距离（m） |
| \(-I_i\) | 一阶**相位超前**，与码符号相反 |
| \(\lambda_i\) | 波长（m），\(\lambda_i=c/f_i\) |
| \(N_i\) | 整周模糊度（未知整数；连续跟踪时当常数） |
| \(\delta_{r,i},\delta^{s}_{i}\) | 相位硬件延迟类项 |
| \(\varepsilon_{L_i}\) | 相位噪声（通常远小于伪距噪声） |

**课堂口诀**：伪距稳在绝对水平但吵；相位准在相对变化但缺零点；电离层对码 \(+I\)、对相 \(-I\)。

### 3.3 为何 \(I_2>I_1\)（同一 STEC）？

\[
I_i=\frac{40.3}{f_i^{2}}\,\mathrm{STEC}\implies\frac{I_2}{I_1}=\frac{f_1^{2}}{f_2^{2}}.
\]

GPS L1/L2：\(f_1=1575.42\,\mathrm{MHz}\)，\(f_2=1227.60\,\mathrm{MHz}\)，\(f_1/f_2=154/120=77/60\)，故 \(I_2/I_1=(77/60)^{2}\approx1.647\)。频率低的 L2，电离层延迟更大。

---

## 4. 几何无关组合：逐步推导

### 4.1 目标

构造观测量，使 \(\rho\)、\(T_{\mathrm{trop}}\)、钟差等**对两频相同的项**消掉，只留下与 \(I\)（即 STEC）及偏差有关的部分。

### 4.2 伪距 GF：一步一步

写两式：

\[
\begin{aligned}
P_1&=\rho+c\Delta t+T+I_1+(b_{r,1}-b^{s}_{1})+\varepsilon_{P_1},\\
P_2&=\rho+c\Delta t+T+I_2+(b_{r,2}-b^{s}_{2})+\varepsilon_{P_2}.
\end{aligned}
\]

相减：

\[
P_{\mathrm{GF}}\equiv P_1-P_2=(I_1-I_2)+(b_{r,1}-b_{r,2})-(b^{s}_{1}-b^{s}_{2})+\varepsilon_{P_1}-\varepsilon_{P_2}.
\]

公共几何与对流层、钟差消失。电离层差：

\[
I_1-I_2=40.3\,\mathrm{STEC}\left(\frac{1}{f_1^{2}}-\frac{1}{f_2^{2}}\right)=40.3\,\mathrm{STEC}\cdot\frac{f_2^{2}-f_1^{2}}{f_1^{2}f_2^{2}}.
\]

因 \(f_2<f_1\)，\(1/f_2^{2}>1/f_1^{2}\)，故 \(I_1-I_2<0\)；有人定义 \(P_2-P_1\) 使符号为正——**读软件时看清定义**。解 STEC：

\[
\mathrm{STEC}=\frac{1}{40.3}\cdot\frac{f_1^{2}f_2^{2}}{f_2^{2}-f_1^{2}}\big[(P_1-P_2)-\mathrm{DCB}_{\mathrm{terms}}\big]+\cdots
\]

（下面单独写 DCB。）常把频率因子收成 \(\alpha\)：

\[
\mathrm{STEC}=\alpha\,(P_1-P_2-\mathrm{DCB}_{\mathrm{GF}})+\text{噪声},
\]

对 GPS L1/L2，\(\alpha\) 约为 \(9.52\,\mathrm{TECU/m}\) 量级（精确值用上式算；不同教材因 \(P_1-P_2\) 或 \(P_2-P_1\) 差一个符号）。

### 4.3 相位 GF

\[
L_{\mathrm{GF}}\equiv L_1-L_2=-(I_1-I_2)+\lambda_1 N_1-\lambda_2 N_2+\Delta\delta+\varepsilon_{L}.
\]

令模糊度组合 \(B=\lambda_1 N_1-\lambda_2 N_2+\cdots\) 在无周跳弧段内为**未知常数**，则 \(L_{\mathrm{GF}}\) 的时间变化主要反映 STEC 的时间变化（符号注意），绝对水平被 \(B\) 拖住。

### 4.4 常见误解

「GF = 没有误差」——错。多路径、噪声、偏差、高阶、跟踪异常都在。GF 只压掉**频率无关公共几何项**。

---

## 5. 数值例 A：假但真实的 L1/L2（推导用）

设某历元「真」几何+钟差+对流层公共部分 \(\rho+c\Delta t+T=22{,}000{,}000.000\,\mathrm{m}\)（数字只为演算）。  
真 STEC \(=20\,\mathrm{TECU}=2.0\times10^{17}\,\mathrm{m}^{-2}\)。  
用第 01 课系数：

\[
I_1=\frac{40.3\times2.0\times10^{17}}{(1.57542\times10^9)^{2}}\approx3.25\,\mathrm{m},\quad
I_2\approx5.35\,\mathrm{m}.
\]

**暂时令所有硬件延迟=0，噪声=0，模糊度先不管。**

则「理想伪距」：

\[
P_1=22{,}000{,}000+3.25=22{,}000{,}003.25\,\mathrm{m},
\]
\[
P_2=22{,}000{,}000+5.35=22{,}000{,}005.35\,\mathrm{m}.
\]

\[
P_1-P_2=-2.10\,\mathrm{m}.
\]

用

\[
\mathrm{STEC}=\frac{1}{40.3}\cdot\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}(P_2-P_1)
\]

（此处用 \(P_2-P_1=+2.10\) 使 STEC 为正）：

代入 \(f_1,f_2\) 可得 STEC \(\approx20\,\mathrm{TECU}\)。**要点**：两伪距只差约 2.1 m，却编码了 20 TECU；公共的两千万米被减掉了。

**理想相位**（同一历元，忽略模糊度时）：\(L_1=\rho+T+c\Delta t-I_1\)，\(L_2=\cdots-I_2\)，故 \(L_1-L_2=-(I_1-I_2)=+2.10\,\mathrm{m}\)，与伪距 GF **符号相反**——正是 \(+I\) vs \(-I\) 的直接后果。

---

## 6. 相位模糊度、周跳、leveling / 平滑

### 6.1 模糊度是什么？

相位像精密千分尺：你知道相对转了多少，但不知道墙上零刻度。\(N_i\)（及组合 \(B\)）在**连续跟踪、无周跳**时近似常数；绝对值未知。因此：

- 相位 GF：**相对 STEC 变化**极漂亮；  
- **绝对 STEC 水平**要靠伪距 GF（或其它约束）来钉。

### 6.2 周跳

跟踪中断或失锁，整周数跳变 → \(B\) 换了一个常数 → GF 相位时间序列出现**台阶**。不处理就平滑，会把假台阶抹进「TEC」。

本仓库可点名：`cycle-slip-correction`、`DRCycleSlip`；质量检查：`TEQC`、`Anubis`（均已在 `PROJECTS.json` 核验）。

### 6.3 Leveling（定水平）直觉

在一个无周跳弧段上：

1. 算伪距 GF 序列 \(P_{\mathrm{GF}}(t)\)（吵，但有绝对意义）；  
2. 算相位 GF 序列 \(L_{\mathrm{GF}}(t)\)（静，但差一个未知常数 \(B\)）；  
3. 用弧段内平均等方式估计 \(B\approx\langle P_{\mathrm{GF}}-L_{\mathrm{GF}}^{\mathrm{(iono\ aligned)}}\rangle\)（具体符号与系数依定义）；  
4. 把相位序列平移到与伪距同一绝对水平 → **leveled phase TEC**。

人话：木尺钉高度，千分尺描波形。

### 6.4 载波平滑伪距（另一常用说法）

递推上用相位增量约束伪距变化，得到比生伪距更干净、仍接近绝对的序列，再组 GF。  
**误解**：平滑=低通乱抹；或平滑能消灭周跳。错。先探测/按弧段断开，再平滑。

---

## 7. DCB 如何进入 GF（预告方程）

回到伪距 GF：

\[
P_1-P_2=(I_1-I_2)+\underbrace{(b_{r,1}-b_{r,2})}_{\approx\mathrm{DCB}_r}
-\underbrace{(b^{s}_{1}-b^{s}_{2})}_{\approx\mathrm{DCB}^{s}}+\varepsilon.
\]

卫星差分码偏差 \(\mathrm{DCB}^{s}\) 与接收机 \(\mathrm{DCB}_r\)（口语里 IFB 家族）以**与频率相关的延迟差**进入 GF，和 \((I_1-I_2)\) 加在一起。换算成 TECU 后，看起来就像电子柱整体抬升或压低——白天夜里一起偏，形状像「电离层多了一层楼」，其实是仪器账。

**预告级改正**：

\[
\mathrm{STEC}_{\mathrm{raw}}=\alpha(P_1-P_2),\qquad
\mathrm{STEC}_{\mathrm{corr}}=\alpha\big(P_1-P_2-\mathrm{DCB}_{r}+\mathrm{DCB}^{s}\big)
\]

（符号随 DCB 产品定义与 \(P_1-P_2\) 方向而变；以产品文档为准。）

实务：

1. 卫星端优先用公开 DCB/OSB 产品；  
2. 接收机端常当未知数估计或标定；  
3. **观测类型必须对齐**（C1C 与 C1W 不是自动同一套账）；  
4. 深度见 `09-dcb-biases-deep.md`；本仓偏差相关可点名 `Gkit-Bias`。

量级感：几纳秒的码偏差 × \(c\) 得米，再 ×\(\alpha\) 得 TECU——可以是数 TECU，绝不可「太小忽略」。

---

## 8. 数值例 B：把 GF、模糊度、DCB 串成小故事

沿用例 A 的真 STEC=20 TECU，\(I_1=3.25\,\mathrm{m}\)，\(I_2=5.35\,\mathrm{m}\)，公共项 \(G=22{,}000{,}000\,\mathrm{m}\)。

现设卫星+接收机总码 GF 偏差使

\[
P_1-P_2=(I_1-I_2)+\Delta b=-2.10+0.40=-1.70\,\mathrm{m}.
\]

若你**不改 DCB**，把 \(-1.70\,\mathrm{m}\) 当纯电离层差，STEC 会从 20 偏到约 \(20\times(1.70/2.10)\approx16.2\,\mathrm{TECU}\)（或依符号定义偏到另一侧）——系统性偏差约 4 TECU。

相位侧：设 \(\lambda_1 N_1-\lambda_2 N_2=B=12.00\,\mathrm{m}\)（未知常数）。则

\[
L_1-L_2=-(I_1-I_2)+B=2.10+12.00=14.10\,\mathrm{m}.
\]

时间上 STEC 变，\(2.10\) 变，\(B\) 不变 → 曲线形状对，水平错。用弧段 leveling：把相位 GF 平移到与（DCB 改正后的）伪距 GF 一致，恢复绝对水平。

**周跳**：某时刻 \(B:12.00\to12.00+\lambda_{\mathrm{eff}}\)（有效波长量级跳变）→ 曲线台阶。平滑前必须切弧或修复。

---

## 9. RINEX → STEC：全清单与失效模式

| 步 | 做什么 | 不做 / 做错会怎样 |
|---|---|---|
| 1 | 确认双频观测类型存在 | 单频强行 GF → 无意义 |
| 2 | 读 RINEX：时间、PRN、\(P,L\)、（可选）CN0 | 垃圾进垃圾出。工具：`georinex`、`rinex`、`PyRINEX` |
| 3 | 解压/转换若需要 | 工具：`crx2rnx`、`hatanaka`、`RNXCMP`、`GFZRNX` |
| 4 | 时间与系统对齐 | 错星错历元组合 |
| 5 | 仰角截止 + 粗差剔除 | 低仰角多路径主导「假天气」 |
| 6 | 周跳探测与弧段划分 | 假台阶进 STEC。`cycle-slip-correction`、`DRCycleSlip`；质检 `TEQC`、`Anubis` |
| 7 | 组伪距/相位 GF | 频率对选错 → 尺度错 |
| 8 | Leveling / 相位平滑（按弧段） | 绝对水平吵或假台阶被抹 |
| 9 | 改正 DCB（类型对齐） | 整条曲线平移数 TECU。`Gkit-Bias` |
| 10 | 乘频率因子 → STEC(t)（TECU） | 单位错（m 当 TECU）故事崩 |
| 11 | （可选）薄壳+IPP→VTEC | 壳高/映射未声明就与 GIM 打架。`Get_IPP` |

**算出后体检**：单位是否 TECU？夜侧是否大量离谱负值？高仰角多星映射 VTEC 是否大致接近？与 GIM 比是整体平移（优先 DCB）还是形状全拧（周跳/频率/时间）？低仰角是否单独检查？

**TEC 主路径工具（已核验）**：`gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`TEC-calculation-MATLAB`、`ionotec`、`PyTECGg`、`TEC_calculation_RINEX3`。

定位套件 `gLAB`、`RTKLIB`、`laika`、`PRIDE-PPPAR`、`GAMPII-GOOD` 可能含电离层组合，但**不要默认 PPP 一次跑完 = 可发表 STEC 产品**。

---

## 10. 常见误解

1. GF 后没有误差。  
2. 相位 TEC 更真所以可扔掉伪距。  
3. 平滑=随便低通。  
4. DCB 太小可忽略。  
5. 任意两频随便减、不问类型与偏差产品。  
6. RINEX 有 L1/L2 = 高质量双频。  
7. STEC 与 GIM 的 VTEC 直接减就判算法死刑——先问映射/壳高/时间/DCB。  
8. 周跳修好 = 模糊度已固定成正确整数（难度不是同一级）。

---

## 11. 课堂测验（带演算）

**题 1.** 伪距与相位方程里电离层项符号各是什么？为什么？  
**答：** 伪距 \(+I\)（群延迟）；相位 \(-I\)（相位超前）；来自 \(n_g>1\)、\(n_p<1\)。

**题 2.** 写出 \(P_{\mathrm{GF}}=P_1-P_2\) 后剩下的主要项。  
**答：** \(I_1-I_2\) + 接收机/卫星码延迟差 + 噪声多路径。

**题 3.** 例 A 中 \(I_1=3.25\,\mathrm{m}\)，\(I_2=5.35\,\mathrm{m}\)。\(P_1-P_2\) 与 \(L_1-L_2\)（忽略模糊度与偏差）各多少？  
**答：** \(P_1-P_2=-2.10\,\mathrm{m}\)；\(L_1-L_2=+2.10\,\mathrm{m}\)。

**题 4.** 模糊度在无周跳弧段内扮演什么角色？Leveling 在干什么？  
**答：** 未知常数偏置；用伪距 GF 把相位 GF 平移到正确绝对水平。

**题 5.** 例 B 中 \(\Delta b=+0.40\,\mathrm{m}\) 混入 \(P_1-P_2\) 且不改 DCB，约导致多少 TECU 偏差（相对 20 TECU、2.10 m 标尺）？  
**答：** 约 \(20\times0.40/2.10\approx3.8\,\mathrm{TECU}\) 量级。

**题 6.** 列出 RINEX→STEC 至少六步，并各给一种失效模式。  
**答：** 见第 9 节表（读数、仰角、周跳、GF、平滑、DCB、换算等）。

**题 7.** 为何观测类型要和 DCB 产品对齐？举本仓一个偏差相关 name、两个 TEC 估计 name。  
**答：** 不同码类型偏差定义不同。`Gkit-Bias`；如 `gnss-tec`、`Seemala-GPS-TEC`。

**题 8.** 只有单频能否做本课 GF TEC？你的 STEC 与 GIM VTEC 相减前要问什么？  
**答：** 不能。是否映射、壳高、时间、IPP、DCB。

**题 9.** GPS \(I_2/I_1\approx(f_1/f_2)^{2}\approx1.647\)。若 \(I_1=4.00\,\mathrm{m}\)，\(I_2\approx?\)  
**答：** \(\approx6.59\,\mathrm{m}\)。

**题 10.** 周跳在相位 GF 序列上通常长什么样？平滑前应怎样？  
**答：** 台阶；先探测/修复或按弧段断开。

---

## 12. 和仓库工具对上号（核验名）

| 目的 | name |
|---|---|
| 估 TEC | `gnss-tec`、`pygnss-tec`、`tec-suite`、`Seemala-GPS-TEC`、`Okoh-MATLAB-TEC-from-RINEX`、`IONOLAB-TEC-Software`、`TEC-calculation-MATLAB`、`ionotec`、`PyTECGg`、`TEC_calculation_RINEX3` |
| 读 RINEX | `georinex`、`rinex`、`PyRINEX` |
| 压缩转换 | `crx2rnx`、`hatanaka`、`RNXCMP`、`GFZRNX` |
| 质检/周跳 | `TEQC`、`Anubis`、`cycle-slip-correction`、`DRCycleSlip` |
| 穿刺点 | `Get_IPP` |
| 偏差 | `Gkit-Bias` |
| 产品对比预告 | `CDDIS-IONEX`、`SH-GIM`、`mosgim` |

---

## 13. 加深：频率因子 \(\alpha\) 手算一遍

令 \(P_2-P_1=I_2-I_1=40.3\,\mathrm{STEC}(1/f_2^{2}-1/f_1^{2})\)。则

\[
\alpha=\frac{\mathrm{STEC}}{P_2-P_1}=\frac{1}{40.3}\cdot\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}.
\]

代入 \(f_1=1.57542\times10^9\)，\(f_2=1.22760\times10^9\)：

- \(f_1^{2}\approx2.4819\times10^{18}\)，\(f_2^{2}\approx1.5070\times10^{18}\)；  
- \(f_1^{2}-f_2^{2}\approx9.749\times10^{17}\)；  
- \(f_1^{2}f_2^{2}\approx3.740\times10^{36}\)；  
- \(f_1^{2}f_2^{2}/(f_1^{2}-f_2^{2})\approx3.836\times10^{18}\)；  
- \(/40.3\approx9.52\times10^{16}\,\mathrm{m}^{-2}/\mathrm{m}=9.52\,\mathrm{TECU/m}\)。

故 \(P_2-P_1=2.10\,\mathrm{m}\) → STEC \(\approx9.52\times2.10\approx20.0\,\mathrm{TECU}\)。**请在自己计算器上复现**；这是本课「真懂 GF」的毕业演算。

---

## 14. 板书应留八行

1. \(P=+I\)，\(L=-I\)；\(I=40.3\,\mathrm{STEC}/f^{2}\)。  
2. \(P_1-P_2=(I_1-I_2)+\mathrm{DCB}_{\mathrm{GF}}+\varepsilon\)。  
3. \(\mathrm{STEC}=\alpha(P_2-P_1-\mathrm{DCB}\ldots)\)，L1/L2 上 \(\alpha\sim9.52\,\mathrm{TECU/m}\)。  
4. 相位 GF 多一个常数模糊度组合 \(B\)。  
5. Leveling/平滑：码定水平，相描形状；先处理周跳。  
6. DCB 伪装成 TEC；类型对齐；`Gkit-Bias`。  
7. 九至十一节清单：每步都有失效模式。  
8. 对比 GIM 前先统一 STEC/VTEC/映射/DCB。

---

## 15. 下一课与出门任务

下一课 **[03-gim-ionex.md](./03-gim-ionex.md)**：多站 STEC 映射汇成 VTEC 场 → GIM；IONEX 字段；分析中心。

**出门任务**：抄写第 9 节清单成一页检查表；对一份双频 RINEX 只完成「列出观测类型、确认双频」；用手算复现第 13 节 \(\alpha\approx9.52\,\mathrm{TECU/m}\)。

---

## 16. 失效模式速查（值班贴）

| 症状 | 优先怀疑 |
|---|---|
| 全日相对 GIM 整体偏高/偏低数 TECU | DCB/类型错配、\(\alpha\) 符号 |
| 某段突然台阶后平移 | 周跳未切弧 |
| 仅低仰角疯抖 | 多路径；截止角 |
| 夜侧大量负 TEC | 周跳、DCB、单位、弧段 leveling 失败 |
| 与 GIM「形状全拧」 | 时间错位、频率对错、错误卫星系统混用 |
| 数值大 10 倍或小 10 倍 | TECU vs \(10^{16}\) 缩放；IONEX 0.1 TECU 存储习惯（03 课） |
| 换接收机后旧偏差失效 | 接收机 DCB 不能无限期沿用 |

---

## 17. 综合演算作业（建议提交）

已知某弧段无周跳。某历元 DCB 已改正后的伪距：\(P_1=22{,}150{,}012.40\,\mathrm{m}\)，\(P_2=22{,}150{,}015.55\,\mathrm{m}\)。相位 GF 已 leveling，使该历元相位导出的 STEC 与伪距一致。取 \(\alpha=9.52\,\mathrm{TECU/m}\)（对 \(P_2-P_1\)）。

(1) \(P_2-P_1=?\)  
(2) STEC≈?  
(3) 若未改正的 DCB 使 \(P_2-P_1\) 少了 0.50 m，STEC 偏差约多少 TECU？  
(4) 若仰角 \(30^\circ\)、\(H=450\,\mathrm{km}\)、\(M\approx1.70\)（用 01 课结果），等效 VTEC≈?

**答：** (1) 3.15 m；(2) \(9.52\times3.15\approx30.0\,\mathrm{TECU}\)；(3) \(9.52\times0.50\approx4.8\,\mathrm{TECU}\)；(4) \(30.0/1.70\approx17.6\,\mathrm{TECU}\)。

---

## 18. 收束

双频估 TEC 的逻辑链是：色散 \(I\propto1/f^{2}\) → 码 \(+I\)、相 \(-I\) → GF 消去公共几何 → 频率因子换成 STEC → 相位提供干净变化、伪距/leveling 提供绝对水平 → DCB 必须从 GF 里拿走 → 周跳决定弧段。RINEX 流水线每一步都有可命名的失效模式。会手算 \(\alpha\) 与例 A/B，才算从「听说几何无关」升级到「能查账」。

引用项目名均来自 `PROJECTS.json` 核验。未 git push。下一文件：`03-gim-ionex.md`。


---

## 19. 观测方程再展开：每一项「进 GF 还是不进」

把伪距方程写全一点，便于判断哪些会被 \(P_1-P_2\) 杀掉：

| 项 | 两频是否近似相同？ | GF 后 |
|---|---|---|
| 几何距离 \(\rho\) | 是（忽略天线相位中心频率差等小项） | 消掉 |
| 接收机/卫星钟差 | 是（一阶） | 消掉 |
| 对流层 \(T\) | 是（L 波段几乎不色散） | 消掉 |
| 电离层 \(I_i\) | **否**，\(\propto1/f_i^{2}\) | **留下差** |
| 码硬件延迟 \(b_i\) | **否** | **留下 DCB** |
| 多路径/噪声 | 否 | 残留，常放大 |

相位侧同理，额外留下 \(\lambda_1 N_1-\lambda_2 N_2\)。  
**课堂金句**：GF 不是魔法橡皮擦，它是「只对频率无关公共项」的减法器；凡是频率相关的，都会留下来——包括你想要的电离层和你不想要的 DCB、多路径差。

天线相位中心改正（PCO/PCV）若频率相关且未妥善处理，也会漏进 GF，表现为厘米到分米级的系统差，换算 TECU 后可观。入门课点到为止：读高端软件文档时寻找「天线改正是否分频率」。

---

## 20. Leveling 的一个可写公式（弧段平均法）

设弧段 \(t\in[t_a,t_b]\)，已周跳清洁。定义（符号约定与第 4 节一致，使电离层项同向）：

\[
P_{\mathrm{GF}}(t)=P_1(t)-P_2(t),\qquad
L_{\mathrm{GF}}(t)=L_1(t)-L_2(t).
\]

理想无噪无偏时 \(P_{\mathrm{GF}}=I_1-I_2\)，\(L_{\mathrm{GF}}=-(I_1-I_2)+B\)。于是

\[
P_{\mathrm{GF}}(t)+L_{\mathrm{GF}}(t)\approx B
\]

（在此符号约定下）应为常数。用弧段平均估计

\[
\hat{B}=\frac{1}{N}\sum_{k=1}^{N}\big(P_{\mathrm{GF}}(t_k)+L_{\mathrm{GF}}(t_k)\big),
\]

再构造 leveled 相位 GF：

\[
L_{\mathrm{GF}}^{\mathrm{(lev)}}(t)=L_{\mathrm{GF}}(t)-\hat{B}\approx-(I_1-I_2)\ \text{或按你的符号对齐到 }I_1-I_2.
\]

最后乘 \(\alpha\) 得 STEC。若先做了 DCB 改正，应在 \(P_{\mathrm{GF}}\) 上改，再 leveling。

**权重变体**：伪距噪声大，可用低仰角降权、或只用高 CN0 历元估 \(B\)。不同软件默认不同——**对比结果前读 leveling 一节**。

---

## 21. 平滑递推（概念级，不绑死某一家公式）

载波平滑伪距的经典直觉（Hatch 滤波一类）是：

\[
\hat{P}(t)=\frac{1}{n}P(t)+\frac{n-1}{n}\big(\hat{P}(t-1)+\Phi(t)-\Phi(t-1)\big),
\]

其中 \(\Phi\) 为相位距离，\(n\) 为平滑窗口长度（有上界）。人话：新伪距给一点绝对信息，相位差分提供低噪增量。  
**对 TEC**：常先各自平滑 \(P_1,P_2\)（或直接平滑 GF），再进入 GF→STEC。窗口太短噪；太长则周跳后收敛慢、或跨过真实突变。弧段一断，\(n\) 重置。

---

## 22. 多系统 / 多频课堂提醒

入门文献写 GPS L1/L2。现代数据可能是 L1/L5、BDS B1/B2、Galileo E1/E5a 等。原则不变：两频、延迟差携电离层。实务核对：

1. 该频率是否有稳定码与相位；  
2. DCB/OSB 产品是否覆盖该类型；  
3. \(\alpha\) 必须用**这对频率**重算，不能照搬 L1/L2 的 9.52；  
4. 多系统混合估接收机 DCB 时，系统间偏差（ISB）可能再搅一摊——入门先单系统跑通。

---

## 23. 与第一课、第三课的接口检查表

从 01 带来：\(I=40.3\,\mathrm{STEC}/f^{2}\)；码相符号；STEC vs VTEC；\(M(E)\)。  
本课交出：STEC(t) 时间序列（最好已 DCB、已周跳处理）。  
交给 03：多站 STEC + IPP + 映射 → 格网/球谐 VTEC → IONEX。

**能不映射就不急着映射**：若科研问题只关心相对 STEC 变化或扰动检测，可直接分析 STEC，少一层薄壳假设污染。

---

## 24. 口述答辩（助教用，抽四问）

1. 在黑板上从 \(P_1,P_2\) 推出 \(P_1-P_2\)，圈出 DCB。  
2. 解释为何 \(L_1-L_2\) 与 \(P_1-P_2\) 在理想情况下符号相反。  
3. 手算：\(P_2-P_1=1.05\,\mathrm{m}\)，\(\alpha=9.52\)，STEC=?  
4. 描述 leveling 三步。  
5. 给出「整体平移 vs 形状全拧」的诊断口诀。  
6. 说出三个本仓 RINEX→TEC 相关 `name`。

合格：能写方程、能算 \(\alpha\) 应用题，不只会背「几何无关」四个字。

---

## 25. 再做一个完整迷你数值（从米到 TECU 到 VTEC）

公共项 \(G=21{,}500{,}000.000\,\mathrm{m}\)。真 STEC=15 TECU ⇒ 用比例相对例 A（20 TECU 时差 2.10 m）：差 \(\Delta I=I_2-I_1=2.10\times15/20=1.575\,\mathrm{m}\)。  
故理想 \(P_2-P_1=1.575\,\mathrm{m}\)。加未建模 DCB 使观测 \(P_2-P_1=1.575+0.25=1.825\,\mathrm{m}\)。

- 未改 DCB：\(\mathrm{STEC}_{\mathrm{raw}}=9.52\times1.825\approx17.4\,\mathrm{TECU}\)（偏高 2.4）。  
- 改正后：\(9.52\times1.575\approx15.0\,\mathrm{TECU}\)。  
- 仰角 \(60^\circ\)，\(M\approx1.13\)（01 课表）：\(\mathrm{VTEC}\approx15.0/1.13\approx13.3\,\mathrm{TECU}\)。

请独立重算一遍，确认「0.25 m 的偏差 ×9.52 ≈ 2.4 TECU」印在直觉里。

---

## 26. 本课强制记忆卡片

\[
P_i=\cdots+I_i+\cdots,\quad L_i=\cdots-I_i+\lambda_i N_i+\cdots,
\]
\[
P_1-P_2=(I_1-I_2)+\mathrm{DCB}_{\mathrm{GF}}+\varepsilon,
\]
\[
\alpha=\frac{1}{40.3}\frac{f_1^{2}f_2^{2}}{f_1^{2}-f_2^{2}}\sim9.52\,\mathrm{TECU/m}\ (\mathrm{GPS\ L1/L2}),
\]
\[
\hat{B}\approx\langle P_{\mathrm{GF}}+L_{\mathrm{GF}}\rangle_{\mathrm{arc}},\quad
\mathrm{STEC}=\alpha(P_2-P_1-\mathrm{DCB}\ldots).
\]

默写以上，第二课机制部分毕业。


---

## 27. 伪距噪声如何被 \(\alpha\) 放大？（量感）

设单频伪距噪声标准差 \(\sigma_P\approx0.3\,\mathrm{m}\)（粗量级，视接收机与多路径而定），且两频噪声近似独立，则

\[
\sigma(P_2-P_1)\approx\sqrt{2}\,\sigma_P\approx0.42\,\mathrm{m}.
\]

乘 \(\alpha\approx9.52\,\mathrm{TECU/m}\)：

\[
\sigma_{\mathrm{STEC}}\approx9.52\times0.42\approx4\,\mathrm{TECU}.
\]

这就是「生伪距 GF TEC 很吵」的数量来源。相位噪声若 \(\sigma_L\approx0.003\,\mathrm{m}\) 量级，GF 后仍远小于伪距，故相对变化漂亮。Leveling/平滑的工程动机，一半就写在这道误差传播里：用相位压时间噪声，用伪距保绝对水平。

若低仰角多路径使 \(\sigma_P\) 升到 1 m，生伪距 STEC 噪声可到 ~10 TECU——此时不截止仰角，任何「精细结构」论文都可疑。

---

## 28. 代码级头脑伪代码（不绑定语言）

```
for each station-day RINEX:
  types = list_obs_types()
  assert dual_frequency(types)
  for each satellite arc:
    elev = compute_elevation(ephemeris, approx_xyz)
    drop if elev < cutoff
    detect_cycle_slips(L1, L2) -> split arcs
    for each clean arc:
      P_GF = P1 - P2
      L_GF = L1 - L2
      P_GF = apply_satellite_DCB(P_GF, obs_type, product)
      B_hat = mean(P_GF + L_GF)   # sign per convention
      L_lev = L_GF - B_hat
      STEC = alpha * align_sign(L_lev or smoothed P_GF)
      optionally estimate receiver DCB as daily constant
      write STEC(t), optionally map to VTEC via M(E), IPP
```

对照第 9 节表逐行打勾；任何开源工具（`gnss-tec`、`Seemala-GPS-TEC`、`tec-suite` 等）都应能在 README 里找到对应开关。找不到 DCB 或周跳章节，就降低对其绝对 TEC 的信任，改只信相对变化。

---

## 29. 与「无电离层组合」的一句话区分（防混淆）

定位里常见 **ionosphere-free（IF）** 组合：故意把一阶 \(I\) 消掉，留下几何，服务定位。  
本课 **geometry-free（GF）** 组合：故意把几何消掉，留下 \(I\)，服务 TEC。  
二者系数不同、目的相反。听到「无电离层」不要当成「几何无关」——搞混会整条流水线反着做。

---

## 30. 收束朗读稿

双频 GNSS 估 TEC，本质是色散测量。码观测携带 \(+I\)，相位携带 \(-I\) 与整周未知数。两频相减得到几何无关组合，公共距离与对流层退出，电离层差与 DCB 留下。频率因子 \(\alpha\) 把米换成 TECU；GPS L1/L2 约 9.52 TECU/m。相位模糊度在无周跳弧段是常数，用伪距 leveling 或平滑钉绝对水平。DCB 必须改正且观测类型对齐，否则数 TECU 的假电子柱会跟你一整天。RINEX 流水线从确认双频、质检、周跳、GF、平滑、DCB 到输出 STEC，每步都有失效模式。会手算 \(\alpha\) 与例题，才算真正下课。

（完）下一课：`03-gim-ionex.md`。引用名均经 `PROJECTS.json` 核验。未 git push。

---

## 31. 最后提醒

本文件按机制优先重写：观测方程、GF 逐步推导、L1/L2 数值例、模糊度与 leveling、DCB 预告式、RINEX→STEC 失效模式、\(\alpha\) 手算与综合作业均保留课堂语气但不再用空洞加长凑字。所有 `name` 均对照 `PROJECTS.json` 核验。未执行 git push。

（完）

配套上一课：`01-ionosphere-tec-basics.md`。配套下一课：`03-gim-ionex.md`。
