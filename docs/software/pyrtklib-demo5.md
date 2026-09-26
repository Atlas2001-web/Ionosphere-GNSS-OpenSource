# pyrtklib_demo5 · RTKLIB demo5/EX 的 Python 绑定操作手册

目录：[`PROJECTS.json` → `pyrtklib_demo5`](../../PROJECTS.json) · 上游 <https://github.com/IPNL-POLYU/pyrtklib_demo5> · 许可 **MIT**（绑定层；内嵌 RTKLIB 源码另受 Takasu **BSD-2-Clause**）· tip **`05845e3`**（2025-10-03）· PyPI 包名 **`pyrtklib5` 0.2.8** · 导入名 `pyrtklib5` · 内核 `VER_RTKLIB="EX"` / `PATCH_LEVEL="2.5.0"` · 本机 Python **3.13.5** · **2026-09-26 00:46–00:54 EDT** 实跑：仓内 F9P+BRDC `postpos` SPP **2304** 历元全 Q=5；RTKLIB 测试集 GSI 0759/3040 RTK **115** 历元 Q1=**102**/Q2=**13**，首 fix ratio **50.4**；ALGO PPP-static（借 [ppp-rtklib](./ppp-rtklib.md) 数据）**2880**×Q6 · **质检复跑**（2026-09-26 01:00–01:03 EDT，pip 实装 **0.2.8**，`EX 2.5.0`，`PMODE_PPP_STATIC=8`）：`example_pntpos.py` **2333** 行+`done`、首 3 行/末行逐字一致、`test.log` **183003715** B；`run_demo5.py` F9P **2304**×Q5、GSI **115**/Q1 **102**/Q2 **13**、ref pos 与前 5 历元逐字一致、首 fix ratio **50.4**（与 [rtklib-explorer](./rtklib-explorer.md) C 版记录一致）；PPP `loadopts=1`、`mode 8 ionoopt 3 tropopt 3`、**2880**×Q6、末历元 `201.0317` 逐字一致；坑 1（`FileWrapper` already registered）、坑 2（`prcopt_default` 全局引用）、坑 7（`filopt_t` 无 setter）复现。改 1 处：`.pyi` 实为 **6468** 行（原稿“约 5.5k”）。墙时本机共享负载波动大（SPP+RTK 0.92 s、pntpos 7.8 s），仅供参考

> 岗位：在 Python 里调用 **rtklibexplorer 版（demo5 → EX 2.5.0）** 的 C 核心：`readrnx` / `pntpos` / `postpos` / RTCM 解码等。冲突时：**本机 `pyrtklib5.pyi` 函数签名 > 上游 readme > 本文**。

## 0. 先分清三个页面

| 页面 | 是什么 | 内核 | 什么时候看 |
| --- | --- | --- | --- |
| [pyrtklib](./pyrtklib.md) | 同一实验室（港理工 IPNL）的**官方树**绑定，`pip install pyrtklib`，`import pyrtklib` | RTKLIB **2.4.3** | 复现 2.4.3 老结果 |
| **本文** pyrtklib_demo5 | 同作者、同 API 风格，`pip install pyrtklib5`，`import pyrtklib5` | **demo5 → EX 2.5.0** | 要 demo5 的低成本接收机优化、Galileo/北斗、新 AR 逻辑 |
| [rtklib-explorer](./rtklib-explorer.md) | demo5/EX 的 **C 源码与 CLI**（`rnx2rtkp`、RTKPOST） | EX 2.5.1（本库落后一个补丁号） | 只要命令行结果、不写 Python |

一句话：pyrtklib_demo5 = **把 rtklib-explorer 的 C 核心搬进 Python**；接口和 [pyrtklib](./pyrtklib.md) 几乎一样，但**两个包不能在同一进程里 import**（见坑 1）。

## 1. 名词（新手先读）

| 术语 | 含义 |
| --- | --- |
| RTKLIB | 高须知二（T. Takasu）写的开源 GNSS 定位 C 库，含 SPP/RTK/PPP |
| demo5 / EX | rtklibexplorer（Tim Everett）维护的 RTKLIB 分支，针对 u-blox 等低成本接收机调参；2.5.x 起版本串改为 `EX` |
| SPP（单点定位） | 只用伪距 + 广播星历，米级；`.pos` 中 **Q=5** |
| RTK | 流动站 + 已知基准站做**双差载波相位**，厘米级；需要基准站观测 |
| PPP（精密单点定位） | 单站 + **精密星历 SP3 + 精密钟差 CLK**，静态收敛后厘米–分米级；**Q=6** |
| SP3 / CLK | IGS 分析中心发布的卫星精密轨道（SP3，通常 15 min 间隔）和精密钟差（RINEX CLK，30 s/5 s） |
| 模糊度（ambiguity） | 载波相位中未知的整周数；解出整数 = **fix**，只得到实数估计 = **float** |
| float / fix | RTK 中 **Q=2** 浮点解（分米级），**Q=1** 固定解（厘米级） |
| ratio | LAMBDA 搜索中次优/最优残差比，≥阈值（默认 3.0）才判为 fix；`.pos` 最后一列 |
| fix-and-hold | `modear=3`：固定后把整周约束回灌滤波器，固定更稳但错固定会被“粘住” |
| `Arr1Dxxx` | 绑定提供的一维容器，可当 C 指针用，**无越界检查** |

## 2. 安装

### 2.1 pip（推荐；本机实测）

```bash
python3 -m venv ~/iono_ops/.venv-pyrtklib5
source ~/iono_ops/.venv-pyrtklib5/bin/activate
pip install -U pip
pip install pyrtklib5 numpy pandas      # numpy/pandas 仅示例脚本用
python -c "import pyrtklib5 as p; print(p.VER_RTKLIB, p.PATCH_LEVEL)"
```

本机输出：

```text
Successfully installed numpy-2.5.3 pandas-3.0.6 pyrtklib5-0.2.8 python-dateutil-2.9.0.post0 six-1.17.0
EX 2.5.0
```

安装后目录只有 `__init__.py`、`pyrtklib5.so`、`pyrtklib5.pyi`：**查函数签名就翻 `.pyi`**（0.2.8 实测 **6468** 行）。

### 2.2 源码（无匹配轮子时）

```bash
sudo apt-get install -y cmake g++ python3-dev
git clone https://github.com/IPNL-POLYU/pyrtklib_demo5.git
cd pyrtklib_demo5 && pip install .      # setup.py 调 cmake；Linux 用 -j8
```

Windows 分支写死 `Visual Studio 17 2022` 生成器；macOS 走 `-DDARWIN=ON`（作者要求 GNU gcc）。本机只验证了 pip 轮子。

## 3. 端到端实跑（本机）

数据来源：

- `example/data/F9P_211203_061807.obs` + `BRDC00IGS_R_20213370000_01D_MN.rnx`：**随仓发布**，香港 u-blox F9P，2021-12-03 07:08–07:46 GPST，1 Hz，无基准站。
- GSI `07590920.05o`（流动站）/`30400920.05o`（基准站）+ `.05n`：rtklibexplorer 仓 `test/data/rinex/` 自带（`git clone https://github.com/rtklibexplorer/RTKLIB`），2005-04-02 00:00–00:59:30，30 s。
- ALGO 2022-03-08 + GFZ `gfz22002.sp3/.clk` + `igs14.atx`：[ppp_rtklib](./ppp-rtklib.md) 仓 `code/Data/` 自带。

### 3.1 上游示例 `example_pntpos.py`（逐历元 `pntpos`）

```bash
cd pyrtklib_demo5/example
time python example_pntpos.py > pnt.out
head -3 pnt.out; tail -2 pnt.out; ls -la test.log
```

```text
1638515279 22.320095711226962 114.2112774773991 25.122300871647894
1638515280 22.320103763835718 114.21121508478357 28.31171230133623
1638515281 22.320287217070845 114.21091299682999 214.73372136522084
1638517612 22.319709207224435 114.21128199215725 5.883009229786694
done
-rw-r--r-- 1 box box 183003715 Sep 26 04:45 test.log
real	0m25.375s
```

列是 `GPS 秒(time_t)  纬度  经度  椭球高`，共 **2333** 行。注意：示例**不检查 `pntpos` 返回值**，且 `elmin=0`，城市峡谷里高度在 5–215 m 间跳；`tracelevel(4)` 写出 **183 MB** 日志（坑 4）。

### 3.2 自写 `postpos`：SPP + RTK 一次跑完

`run_demo5.py`（完整脚本，可直接复制）：

```python
import sys
import pyrtklib5 as p
print("pyrtklib5", p.VER_RTKLIB, p.PATCH_LEVEL)
EX, GS = sys.argv[1], sys.argv[2]   # example/data 与 RTKLIB/test/data/rinex

def run(files, out, mode, nf, elmin_deg, navsys):
    prcopt, solopt, filopt = p.prcopt_t(), p.solopt_t(), p.filopt_t()
    p.resetsysopts(); p.getsysopts(prcopt, solopt, filopt)   # 每次拿干净默认值
    prcopt.mode = mode; prcopt.nf = nf; prcopt.navsys = navsys
    prcopt.elmin = elmin_deg * p.D2R; prcopt.sateph = p.EPHOPT_BRDC
    prcopt.modear = 3                  # fix-and-hold
    prcopt.refpos = p.POSOPT_SINGLE    # 基准站坐标=其 SPP 平均（同 rnx2rtkp 默认）
    prcopt.ionoopt = p.IONOOPT_BRDC; prcopt.tropopt = p.TROPOPT_SAAS
    solopt.posf = p.SOLF_LLH; solopt.outhead = 1; solopt.timef = 1
    ret = p.postpos(p.gtime_t(), p.gtime_t(), 0.0, 0.0, prcopt, solopt, filopt,
                    files, len(files), out, "", "")
    print(f"postpos -> {out} ret={ret}")

run([f"{EX}/F9P_211203_061807.obs", f"{EX}/BRDC00IGS_R_20213370000_01D_MN.rnx"],
    "f9p_spp.pos", p.PMODE_SINGLE, 1, 10, p.SYS_GPS | p.SYS_GAL | p.SYS_CMP)
run([f"{GS}/07590920.05o", f"{GS}/30400920.05o", f"{GS}/07590920.05n", f"{GS}/30400920.05n"],
    "gsi_rtk.pos", p.PMODE_KINEMA, 2, 15, p.SYS_GPS)
```

```bash
time python run_demo5.py pyrtklib_demo5/example/data RTKLIB/test/data/rinex
for f in f9p_spp.pos gsi_rtk.pos; do echo "== $f"; grep -v '^%' $f | \
  awk 'NF>=6{n++;q[$6]++} END{printf "epochs=%d",n; for(k in q) printf " Q%s=%d",k,q[k]; print ""}'; done
```

```text
pyrtklib5 EX 2.5.0
postpos -> f9p_spp.pos ret=0
postpos -> gsi_rtk.pos ret=0
real	0m3.937s
== f9p_spp.pos
epochs=2304 Q5=2304
== gsi_rtk.pos
epochs=115 Q2=13 Q1=102
```

`gsi_rtk.pos` 头与前 5 历元（float → fix 的过程）：

```text
% program   : RTKLIB ver.EX 2.5.0
% ref pos   :  35.132063637  139.624300387    75.3847
%  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio
2005/04/02 00:00:00.000   35.160871904  139.613833687    70.5757   2   7   1.5867   1.2230   3.6707   0.6000  -1.2950  -1.4206   0.00    0.0
2005/04/02 00:00:30.000   35.160873148  139.613834962    69.9364   2   7   0.9120   0.8277   1.5787   0.0510  -0.3489  -0.5853   0.00    0.0
2005/04/02 00:01:00.000   35.160873164  139.613835834    69.7524   2   7   0.0000  67.4891  86.8089  67.6817  83.3692  82.9683   0.00    0.0
2005/04/02 00:01:30.000   35.160872161  139.613835985    69.9120   2   7   0.4281   0.5695   0.6132  -0.2314   0.2684  -0.2373   0.00    0.0
2005/04/02 00:02:00.000   35.160872533  139.613836865    69.8576   1   7   0.0000   0.1068   0.0852  -0.0655   0.0944  -0.0971   0.00   50.4
```

**对拍：** 与 [rtklib-explorer](./rtklib-explorer.md) 用 C 版 `rnx2rtkp` EX 2.5.1 跑同数据的结果（115 历元 / Q1=102 / Q2=13 / 首 fix 35.160872533 139.613836865 69.8576 / ratio 50.4）**逐项一致**——Python 绑定没有改算法。

同一脚本换成 [pyrtklib](./pyrtklib.md)（2.4.3，输出路径需包 `Arr1Dchar`，见坑 3）：F9P SPP 只出 **1083** 历元；GSI RTK **115** 历元全 Q1、首历元即 fix（ratio 24.9）。**两个内核结果不同是正常的**，归档时以 `% program` 行区分。

### 3.3 PPP-static：用 `.conf` 装载（SP3/CLK/ATX）

ATX 等**文件路径字段在 Python 里是只读**的（`filopt.satantp = ...` 抛 `AttributeError`），所以 PPP 走 rnx2rtkp 同款配置文件：

```text
# algo_ppp.conf
pos1-posmode    =ppp-static
pos1-frequency  =l1+l2
pos1-elmask     =15
pos1-ionoopt    =dual-freq
pos1-tropopt    =est-ztd
pos1-sateph     =precise
pos1-navsys     =1
pos2-armode     =off
out-solformat   =llh
file-satantfile =/path/to/Data/igs14.atx
file-rcvantfile =/path/to/Data/igs14.atx
```

```python
import sys, pyrtklib5 as p
conf, D = sys.argv[1], sys.argv[2]
prcopt, solopt, filopt = p.prcopt_t(), p.solopt_t(), p.filopt_t()
p.resetsysopts()
print("loadopts =", p.loadopts(conf, p.sysopts.ptr))
p.getsysopts(prcopt, solopt, filopt)
print("mode", prcopt.mode, "ionoopt", prcopt.ionoopt, "tropopt", prcopt.tropopt)
files = [f"{D}/algo0670.22o", f"{D}/brdc0670.22n", f"{D}/gfz22002.sp3", f"{D}/gfz22002.clk"]
print("postpos ret =", p.postpos(p.gtime_t(), p.gtime_t(), 0.0, 0.0, prcopt, solopt, filopt,
                                 files, len(files), "algo_ppp5.pos", "", ""))
```

```text
loadopts = 1
mode 8 ionoopt 3 tropopt 3
postpos ret = 0
epochs=2880 Q6=2880
2022/03/08 23:59:30.000   45.955800587  -78.071371474   201.0317   6   7   0.0016   0.0033   0.0047  -0.0003   0.0003  -0.0013   0.00    0.0
```

与 IGS 站点 API 给的 ALGO 概略坐标（`45.9558004 -78.0713676 200.829`，只到 0.1 m 级）相比，末历元 dN=+0.021 / dE=−0.300 / dU=+0.202 m。参考值本身是概略值，**这不是精度评定**，只说明链路正确。

## 4. 参数表

### 4.1 `prcopt_t` 常用字段（Python 属性名 = C 成员名）

| 字段 | conf 键 | 取值（本库常量） | 说明 |
| --- | --- | --- | --- |
| `mode` | `pos1-posmode` | `PMODE_SINGLE`=0 / `KINEMA`=2 / `STATIC`=3 / `STATIC_START`=4 / `PPP_KINEMA`=7 / `PPP_STATIC`=8 | EX 多了 static-start，**PPP 编号比 2.4.3 大 1** |
| `nf` | `pos1-frequency` | 1=L1，2=L1+L2，3=+L5 | 单频接收机设 1 |
| `navsys` | `pos1-navsys` | `SYS_GPS`=1、`SYS_GLO`、`SYS_GAL`、`SYS_CMP`… 按位或 | 默认 GPS+GLO+GAL |
| `elmin` | `pos1-elmask` | 弧度（`deg*p.D2R`） | conf 里写度 |
| `sateph` | `pos1-sateph` | `EPHOPT_BRDC` / `EPHOPT_PREC` | PPP 必须 PREC + SP3/CLK |
| `ionoopt` | `pos1-ionoopt` | `IONOOPT_BRDC` / `IONOOPT_IFLC`(=3, dual-freq) | PPP 用 IFLC |
| `tropopt` | `pos1-tropopt` | `TROPOPT_SAAS` / `TROPOPT_EST`(=3) | PPP 估 ZTD |
| `modear` | `pos2-armode` | 0 off / 1 continuous / 2 instantaneous / 3 fix-and-hold | 模糊度固定策略 |
| `refpos` | `ant2-postype` | `POSOPT_POS_LLH`=0 / `POSOPT_POS_XYZ` / `POSOPT_SINGLE`=2 / `POSOPT_RINEX`=4 | RTK 基准站坐标来源；默认 0 且未填坐标 → **空结果** |
| `rb[0..2]` | `ant2-pos1..3` | ECEF 米 | 已知基准站坐标 |

### 4.2 `.pos` 列（`solopt.posf=SOLF_LLH`）

| 列 | 含义 |
| --- | --- |
| `GPST` | 日期 + 时间（`timef=1`；0 为周秒） |
| `latitude/longitude/height` | WGS84 纬经度（°）与**椭球高**（m，不是海拔） |
| `Q` | 1 fix / 2 float / 3 SBAS / 4 DGPS / 5 single / 6 PPP |
| `ns` | 参与解算卫星数 |
| `sdn sde sdu` | 北/东/天 标准差（m，滤波器**形式**精度，不是真误差） |
| `sdne sdeu sdun` | 协方差的符号平方根 |
| `age` | 差分龄期（s），RTK 才有意义 |
| `ratio` | 模糊度 ratio；fix-and-hold 保持期可达 999.9 |

此外 EX 版 `postpos` 会**额外生成 `<name>_events.pos`**（事件标记文件；无事件时只有文件头）。

## 5. 坑（现象 → 原因 → 修复）

1. **`ImportError: generic_type: type "FileWrapper" is already registered!`** → 同一解释器里先 `import pyrtklib` 再 `import pyrtklib5`，两个 pybind11 模块注册了同名类型（本机实测）→ 分 venv：`python3 -m venv ~/.venv-p5 && ~/.venv-p5/bin/pip install pyrtklib5`
2. **第二次跑的结果被第一次的设置污染** → `prcopt = p.prcopt_default` 拿到的是**全局对象引用**（本机：改 `a.mode` 后 `p.prcopt_default.mode` 同步变），`copy.copy` 又报 `cannot pickle` → 每次用 `prcopt=p.prcopt_t(); p.resetsysopts(); p.getsysopts(prcopt, solopt, filopt)`
3. **上游 `example_postpos.py` 报 `TypeError: postpos(): incompatible function arguments`** → 0.2.8 的输出路径参数是 `str`，示例还在传 `Arr1Dchar`（2.4.3 版 pyrtklib 反而**只**收 `Arr1Dchar`）；且示例所需 Whampoa/`hksc1950.21*` 数据**未随仓发布** → `sed -i 's/output_path = Arr1Dchar("pyexample_output.txt")/output_path = "pyexample_output.txt"/; s/print(output_path.ptr)/print(output_path)/' example_postpos.py`，再换成自有数据（本机改后能跑到 `rtklib status: 0`，但因缺文件**不产出结果文件**、也不报错）
4. **跑一次示例磁盘多出 183 MB** → `example_pntpos.py` 里 `traceopen('test.log'); tracelevel(4)` → `sed -i 's/^tracelevel(4)/tracelevel(0)/' example_pntpos.py`（或调试完 `rm test.log`）
5. **RTK 输出只有文件头、`% ref pos : 0.000000000 0.000000000 0.0000`** → `getsysopts` 默认 `refpos=0`（`POSOPT_POS_LLH`，用手填坐标）但没填 → 脚本里加 `prcopt.refpos = p.POSOPT_SINGLE`（或 `POSOPT_RINEX` 用基准站 RINEX 头坐标，或填 `prcopt.rb[0..2]`）
6. **PPP 跑出来是 PPP-fixed/模式不对** → 把 2.4.3 的整数 `mode=7` 直接搬过来；EX 中 7 是 PPP-kinematic、8 才是 PPP-static → 一律用常量：`python -c "import pyrtklib5 as p; print(p.PMODE_PPP_STATIC)"`（本机 8）
7. **`AttributeError: property '' of 'filopt_t' object has no setter`** → `char[]` 字段（ATX、DCB、geoid 路径等）在绑定里只读 → 写 conf 用 `p.loadopts(conf, p.sysopts.ptr)` + `p.getsysopts(...)`，见 §3.3
8. **城市数据 SPP 高度跳几十米** → 示例 `elmin=0`、不查返回值、F9P 多路径 → 至少 `prcopt.elmin = 10*p.D2R`，并检查 `pntpos` 返回值与 `msg`

## 6. 诚实边界

- 上游自述 EX 2.5.0 适配为“roughly adapt… not fully tested”；本机只验证了 SPP / GPS 双频 RTK / GPS PPP-static 三条链路，**未测** RTCM 流、GLONASS AR、PPP-AR、实时 `rtksvr`。
- 内核 **EX 2.5.0**，比 [rtklib-explorer](./rtklib-explorer.md) tip 的 2.5.1 旧；需要最新修复请用 C 版 CLI。
- 本机无 Windows/macOS，未验证对应轮子；源码编译路径未跑。
- 论文里的深度学习紧耦合部分在另仓 TDL-GNSS / 前端 TASGNSS，本页不覆盖。

## 7. 交叉链接

- CLI 与配置细节：[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md)
- 2.4.3 绑定：[pyrtklib](./pyrtklib.md)；纯 Python 重写 demo5 思路：[rtklib-py](./rtklib-py.md)
- PPP 学习代码（本页 §3.3 数据来源）：[ppp-rtklib](./ppp-rtklib.md)；CLAS/MADOCA/HAS：[mrtklib](./mrtklib.md)；城市 PPP 研究叉：[urban-rtklib](./urban-rtklib.md)
- RINEX 预检：[georinex](./georinex.md) · [gfzrnx](./gfzrnx.md)
