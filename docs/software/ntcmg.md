# ntcmg · Galileo NTCM-G 广播电离层模型 C++ 实现（lguldur/ntcmg）操作手册

目录：[`PROJECTS.json` → `ntcmg`](../../PROJECTS.json) · 上游 <https://github.com/lguldur/ntcmg> · 规范 [NTCM-G Ionospheric Model Description, Issue 1.0, May 2022](https://www.gsc-europa.eu/sites/default/files/NTCM-G_Ionospheric_Model_Description_-_v1.0.pdf)（GSC，PDF 3503216 B，本机可匿名下载）· master `a458b3f`（2024-04-08 01:09 EDT；无 tag、无 release、无构建脚本）· 许可 **MIT**（© 2023 David Duchet）· 本机实跑 2026-09-26 05:45–05:52 EDT（g++ 14.2，Debian）

> **质检复跑通过（2026-09-26 05:57–06:02 EDT）**：g++ 14.2.0，`a458b3f`。驱动 0 警告；`--test` 输出 0.000303；三档首行 33.7567 / 28.3208 / 51.5270；§3.2 的 89.3515 / 165.6327 / 256.7137、§3.3 的 24.7620 / 5.1005、坑 2 的 33.6218、坑 3 的 108.8859 逐字一致。新增：108 组逐组全部对上（内嵌表 = 规范 PDF 表）。卫星几何确是自定的，不来自星历，§3.2 的推导无法用 `aer2geodetic` 直接复现（已注明）。
>
> 岗位：给定 Galileo 导航电文里的 3 个有效电离水平系数 `ai0, ai1, ai2`，以及接收机和卫星的大地坐标，算出这条链路的 **sTEC（TECU）** 和 **单频距离延迟（m）**。整个仓就 `ntcmg.h` + `ntcmg.cpp` 两个文件，没有 `main`，要自己写驱动。冲突时：**GSC 规范 PDF > `ntcmg.cpp` > 本文**。

## 1. 它解决什么 / 不做什么

**做：**

- `ntcmg::stec(ai0, ai1, ai2, rxlat, rxlon, rxalt, satlat, satlon, satalt, utc_hour, doy)` → sTEC（TECU）。经纬度用**弧度**，高度用**米**
- `ntcmg::iono_delay(STEC, freq_Hz)` → 40.3·STEC·10¹⁶/f²（米）
- `ntcmg::test()` → 用规范 Annex D 的 108 组验证数据（高/中/低太阳活动各 36 组）自检，返回 √Σ(差²)
- 实现的是规范里 Eq. 1–34：ECEF → 仰角/方位 → 450 km 穿刺点 → 地方时、太阳赤纬、地磁纬度 → F1…F5 → VTEC → 映射函数 → STEC

**不做：**

- 不读 RINEX 导航文件、不从星历算卫星位置：`ai` 和卫星经纬高都得自己准备（§3.2 用 `grep` + pymap3d）
- 没有仰角截止，也不检查卫星是否在地平线以上（坑 5）
- 不是 NeQuick-G（NeQuick-G 是逐点电子密度积分；NTCM-G 是 12 个系数的经验 VTEC 公式，两者用同一套 `ai`）
- 没有 Python 绑定、没有 CMake、没有单元测试框架

| 相邻页面 | 关系 |
| --- | --- |
| [nequickg](./nequickg.md) / [galileo-nequick-g](./galileo-nequick-g.md) | 同样由 Galileo `ai0–ai2` 驱动的另一种模型（社区 Python 版 / GSC 官方 C） |
| [libswiftnav](./libswiftnav.md) / [glab-upc](./glab-upc.md) | 含 GPS Klobuchar 广播模型，可以做“单频广播改正”对比 |
| [iricore](./iricore.md) | 同一时刻、同一地点的 IRI 气候值 vTEC |
| [ionex-gim](./ionex-gim.md) | 事后 GIM 真值；评估广播模型残差时用 |

## 2. 安装 / 编译

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/lguldur/ntcmg.git          # 236 KB，3 个源文件：ntcmg.h 56 行 / ntcmg.cpp 1354 行 / README 3 行
cd ntcmg && git log -1 --format='%h %ad' --date=iso     # a458b3f 2024-04-08 07:09:20 +0200
```

仓里没有 `main`。下面这个 `ntcmg_cli.cpp` 驱动是本文写的，做两件事：把输入从“度/米”转成库要求的“弧度/米”；同时打印 E1、E5a 两个频点的延迟。

```cpp
// 小驱动：度/米输入 → ntcmg::stec / iono_delay（ntcmg.h 要求弧度）
#include <cstdio>
#include <cstdlib>
#include "ntcmg.h"
int main(int argc, char** argv) {
    const double d2r = 3.1415926535898 / 180.0;
    if (argc == 2) { std::printf("test() sqrt(sum diff^2 over 108 cases)=%.6f TECU\n", ntcmg::test()); return 0; }
    if (argc != 12) { std::fprintf(stderr, "usage: %s ai0 ai1 ai2 rxlat rxlon rxalt_m satlat satlon satalt_m utc_h doy\n       %s --test\n", argv[0], argv[0]); return 1; }
    double v[11]; for (int i = 0; i < 11; ++i) v[i] = std::atof(argv[i + 1]);
    double s = ntcmg::stec(v[0], v[1], v[2], v[3]*d2r, v[4]*d2r, v[5], v[6]*d2r, v[7]*d2r, v[8], v[9], v[10]);
    std::printf("STEC=%.4f TECU  delay_E1(1575.42MHz)=%.4f m  delay_E5a(1176.45MHz)=%.4f m\n",
                s, ntcmg::iono_delay(s, 1575.42e6), ntcmg::iono_delay(s, 1176.45e6));
    return 0;
}
```

```bash
g++ -O2 -Wall -o ntcmg_cli ntcmg_cli.cpp ntcmg.cpp -I.     # 本机 0 警告（单独 `g++ -c -Wall -Wextra ntcmg.cpp` 也 0 警告）
```

## 3. 端到端

### 3.1 自检：规范 Annex D 验证数据

```bash
./ntcmg_cli --test
```

```text
test() sqrt(sum diff^2 over 108 cases)=0.000303 TECU
```

作者注释写的是 “0 is good. ~0.0003 is good enough”。这个值是 108 组差值平方和再开方，所以单组误差只会更小。再从规范表格里每档各抽第一行，手工喂给驱动（注意规范表格的列顺序是**经度在前**，驱动的参数顺序是**纬度在前**）：

```text
high#1 expect 33.7567:
STEC=33.7567 TECU  delay_E1(1575.42MHz)=5.4812 m  delay_E5a(1176.45MHz)=9.8292 m
med#1 expect 28.3208:
STEC=28.3208 TECU  delay_E1(1575.42MHz)=4.5985 m  delay_E5a(1176.45MHz)=8.2464 m
low#1 expect 51.5270:
STEC=51.5270 TECU  delay_E1(1575.42MHz)=8.3666 m  delay_E5a(1176.45MHz)=15.0035 m
```

三行都和规范 “Output STEC (TECU)” 列一致，到小数点后 4 位（对应命令：`./ntcmg_cli 236.831641 -0.39362878 0.00402826613 82.49 -62.34 78.11 54.29 8.23 20281546.18 0 105` 等，`ai` 取规范 7.1/7.2/7.3 节）。

质检复跑又把全部 108 组逐组喂给同一个驱动：`ntcmg.cpp` 里 `test()` 内嵌的三张表，与规范 PDF（`pdftotext -layout`）Annex D 的 108 行 9 列**完全相同**；驱动输出与期望值的差按 4 位小数打印全部为 0（最大 |差| <0.00005 TECU）。所以 0.000303 是库自带 `test()` 的 √Σ差²，驱动本身逐组也对得上规范。

### 3.2 真实广播系数：2024-03-20（doy 080）06 UT，武汉

**取 `ai`**：BKG 的 IGS 镜像提供匿名 HTTPS 下载，DLR 合并导航文件的头里有 `GAL` 行：

```bash
curl -fsSO https://igs.bkg.bund.de/root_ftp/IGS/BRDC/2024/080/BRDM00DLR_S_20240800000_01D_MN.rnx.gz   # 1192894 B
zcat BRDM00DLR_S_20240800000_01D_MN.rnx.gz | grep "IONOSPHERIC CORR"
```

```text
GPSA   3.2596e-08  7.4506e-09 -1.7881e-07  0.0000e+00       IONOSPHERIC CORR    
GPSB   1.3517e+05  0.0000e+00 -2.6214e+05  1.3107e+05       IONOSPHERIC CORR    
GAL    1.1800e+02 -3.4766e-01  2.7039e-02                   IONOSPHERIC CORR    
BDSA   3.2596e-08  6.7055e-08 -1.0133e-06  1.5497e-06       IONOSPHERIC CORR    
...
```

→ `ai0=118.00`（sfu）、`ai1=−0.34766`（sfu/°）、`ai2=0.027039`（sfu/°²）。

**卫星几何**：从武汉（30.5°N 114.4°E，0 m）看过去，仰角 90°/30°/10°、方位 180°，卫星放在 Galileo 轨道高度 23222 km。用 pymap3d 3.2.0 `aer2geodetic` 算出卫星的经纬高：

```text
90 0 30.5000 114.4000 23222000.0
30 180 -18.8011 114.4000 23232305.9
10 180 -37.3101 114.4000 23240621.4
```

（这是人为设定的几何，不是某颗真实卫星在 06:00 的位置，也不是从星历算的。）质检复跑：用 `geodetic2aer` 反算，这两个位置的仰角确实是 30.0000° / 10.0000°。但直接 `aer2geodetic(180, el, 23222000, 30.5, 114.4, 0)`（把 23222 km 当斜距）得到的是 `-17.7489 114.4 20616605.0`，不是上表的值，上表的具体算法没能复现。好在 sTEC 只取决于视线方向：把卫星放在同一方向、斜距不同的这个点上，结果仍是 165.6327；换成地心半径 6371+23222 km 的点，结果是 165.6326。

```bash
A="118.00 -0.34766 0.027039"
./ntcmg_cli $A 30.5 114.4 0  30.5000 114.4000 23222000.0 6 80
./ntcmg_cli $A 30.5 114.4 0 -18.8011 114.4000 23232305.9 6 80
./ntcmg_cli $A 30.5 114.4 0 -37.3101 114.4000 23240621.4 6 80
```

```text
STEC=89.3515 TECU  delay_E1(1575.42MHz)=14.5082 m  delay_E5a(1176.45MHz)=26.0172 m
STEC=165.6327 TECU  delay_E1(1575.42MHz)=26.8942 m  delay_E5a(1176.45MHz)=48.2285 m
STEC=256.7137 TECU  delay_E1(1575.42MHz)=41.6832 m  delay_E5a(1176.45MHz)=74.7493 m
```

- 仰角 90° 时映射函数 = 1（Eq. 33 中 sin z = 0），所以 **89.3515 TECU 就是 NTCM-G 在武汉头顶 450 km 处的 VTEC**。同一时刻 [iricore](./iricore.md) 的 IRI-2020 给 63.194 TECU（已更新指数）
- 仰角 30°/10° 时 sTEC 分别是 90° 时的 1.854 倍和 2.873 倍。注意这里穿刺点往南移了，VTEC 本身也在变，比值并不是纯粹的映射函数
- 延迟换算核对：40.3×89.3515e16/(1575.42e6)² = 14.508 m，和输出一致

### 3.3 改一个量看灵敏度（同一驱动）

| 改动 | 输出 STEC (TECU) | 说明 |
| --- | ---: | --- |
| 基准（90°，06 UT） | 89.3515 | §3.2 第一行 |
| UTC 改成 18 h（当地约 01:38 LT） | 24.7620 | 夜间，F1 日变化项变小 |
| `ai0=ai1=ai2=0` | 5.1005 | F5 只剩 k11=1.41808 TECU；规范对全零 `ai` 有没有特殊规定，本文未核对 |

## 4. 参数 / 字段

`ntcmg::stec` 参数（单位来自 `ntcmg.h` 注释，与规范 Table 1 对照过）：

| 参数 | 单位 | 从哪来 |
| --- | --- | --- |
| `ai0, ai1, ai2` | sfu、sfu/°、sfu/°² | Galileo F/NAV、I/NAV 电离层参数；RINEX 3 头 `GAL … IONOSPHERIC CORR` |
| `rxlat, rxlon` | **rad**，WGS-84 大地坐标 | 接收机近似位置 |
| `rxalt` | **m**，椭球高 | 同上 |
| `satlat, satlon` | **rad** | 由广播星历算 ECEF 再转大地坐标（本库不做） |
| `satalt` | **m** | 同上 |
| `utc_time` | 小时（0–24，可带小数） | UT |
| `doy` | 天（1 月 1 日 = 1） | |

中间量（`ntcmg.cpp` 常量；Re/hI/π/地磁极与规范 Table 2、k1–k12 与 Table 3 一致，a/b 为 WGS-84 椭球参数）：

| 符号 | 值 | 作用 |
| --- | --- | --- |
| `hI` | 450 km | 穿刺点高度 |
| `Re` | 6371 km | 球半径（映射函数、穿刺点） |
| `a, b` | 6378137 / 6356752.3142 m | WGS-84，用于 ECEF |
| `PHIgnp, LAMBDAgnp` | 79.74°, −71.78° | 地磁北极（算地磁纬度） |
| `k1…k12` | 0.92519 … 0.13985 TECU/sfu | 经验系数 |
| `Azpar` | √(ai0² + 1633.33·ai1² + 4802000·ai2² + 3266.67·ai0·ai2) | 本例手算 167.496 → F5 = 1.41808 + 0.13985×167.496 = 24.8424 TECU |

## 5. 怎么读结果

- **量级**：NTCM-G 本来就是给**单频用户**做广播改正的，规范 Annex C 用它和 NeQuick-G、IGS GIM（IGSG）比，给的是统计残差。用来“估个十几米的 L1 延迟”合适，用来做 TEC 科研图不合适
- **vTEC 看 90° 仰角**：库没有单独暴露 VTEC，令卫星在头顶，即 sTEC = VTEC
- **E1 与 E5a 延迟之比 = (1575.42/1176.45)² = 1.793**：双频用户直接做无电离层组合就行，用不上这个模型
- **`ai` 是整个系统共用的**：一整天通常就几组值，按区域调整不了；局地误差大时要看 GIM

## 6. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 武汉头顶的 sTEC 算成 36.5396 TECU（正确值 89.3515） | 直接把**度**传给了要求**弧度**的 `ntcmg::stec`；函数照样返回一个看起来合理的数 | 调用时换算：`ntcmg::stec(ai0,ai1,ai2, lat*M_PI/180, lon*M_PI/180, h, ...)`，或者用 §2 的驱动 |
| 2 | 照规范表格顺序抄参数，high#1 得到 33.6218（应为 33.7567），差得不多，很难发现 | 规范 Annex D 表格是“经度、纬度”，函数签名是“纬度、经度” | `./ntcmg_cli 236.831641 -0.39362878 0.00402826613 82.49 -62.34 78.11 54.29 8.23 20281546.18 0 105`（先纬度后经度） |
| 3 | 卫星高度写成 km（23232.3059），30° 那条链路得到 108.8859（应为 165.6327） | `satalt`/`rxalt` 单位是**米**；卫星被放到了离地面约 23 km 的地方，仰角全错 | 乘 1000：`./ntcmg_cli $A 30.5 114.4 0 -18.8011 114.4 23232305.9 6 80` |
| 4 | 卫星在地平线以下（本机 pymap3d 算出仰角 −65.66°）仍然输出 `STEC=28.0447` | 代码里没有仰角判断，Eq. 23 算出负仰角也照常往下算 | 调用前先过滤：`python -c "import pymap3d as pm;print(pm.geodetic2aer(satlat,satlon,sath,rxlat,rxlon,rxh)[1])"`，只算仰角 >0（或 >截止角）的卫星 |
| 5 | `undefined reference to 'ntcmg::stec(double, …)'` | 只编译了自己的 main，没有链接 `ntcmg.cpp`（仓里没有库文件） | `g++ -O2 -o ntcmg_cli ntcmg_cli.cpp ntcmg.cpp -I.` |
| 6 | 两个 `.cpp` 都 `#include "ntcmg.cpp"` → `multiple definition of 'ntcmg::a'`（还有 `b`、`pi`） | `ntcmg.cpp` 在命名空间里定义了非 const 全局变量 `a, b, pi, Re, hI…` | 只 include 头文件，`ntcmg.cpp` 单独编译一次：`g++ -c ntcmg.cpp -o ntcmg.o` |
| 7 | 延迟只有 1e-16 m 量级 | 用了 2024-04-08 之前的版本：`iono_delay` 少乘 1e16（修复提交 `a458b3f` “iono_delay STEC * 1e16”） | `git -C ntcmg pull && git -C ntcmg log -1 --format=%h`（应为 `a458b3f` 或更新） |
| 8 | 在 `BRDC00WRD_S_…_MN.rnx` 里 `grep "IONOSPHERIC CORR"` 什么也找不到 | BKG 的 WRD 合并文件（BNC 从实时流生成）头里本来就没有电离层参数（本机 2024/080 实测） | 换 DLR 的合并文件：`curl -fsSO https://igs.bkg.bund.de/root_ftp/IGS/BRDC/2024/080/BRDM00DLR_S_20240800000_01D_MN.rnx.gz` |
| 9 | 以为 `test()` 返回的是 RMS | 实际是 108 组差值的 √Σ差²，没有除以组数 | 要逐组误差就按 §3.1 手工逐行跑，和规范表格对比 |

## 7. 许可与诚实边界

- 代码 MIT（© 2023 David Duchet）；模型与验证数据出自 GSC 规范（© European Union 2022，按其使用条款）。广播文件来自 IGS/BKG 公开目录。
- **实跑**：g++ 编译、`test()`、规范三档各第一行、2024/080 DLR 广播 `ai` + 三种仰角、UT/全零 `ai` 灵敏度、坑 1–6 与坑 8 都在本机复现过。
- **未实跑**：坑 7 的旧版本（依据是提交 diff）；用真实星历算卫星位置；与 GIM 或 NeQuick-G 做残差统计；嵌入式或实时使用。
- 代码是单个作者的规范移植（★3），和规范验证数据对得上，但没有经过 GSC 认证；用于产品前请用规范 Annex D 全表回归一遍。

## 8. 链接

- 教程：[04 IRI 与 NeQuick](../tutorials/04-iri-nequick.md) · [06 电离层与定位](../tutorials/06-iono-positioning.md)
- 兄弟：[nequickg](./nequickg.md) · [galileo-nequick-g](./galileo-nequick-g.md) · [iricore](./iricore.md) · [libswiftnav](./libswiftnav.md) · [glab-upc](./glab-upc.md) · [ionex-gim](./ionex-gim.md)
