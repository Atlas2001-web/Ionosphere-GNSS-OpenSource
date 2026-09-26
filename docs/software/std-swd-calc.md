# STD_SWD_Calc · GNSS 斜路径总延迟/湿延迟计算操作手册

目录：[`PROJECTS.json`](../../PROJECTS.json) → `STD_SWD_Calc` · 上游 <https://github.com/zohrehadavi/STD_SWD_Calc> · tip **`3e4552b`**（2026-07-27，`Update GPT3.py`）· ★**10** · forks **2** · 许可 **GPL-3.0**（仓内 `LICENSE`，GitHub API `spdx_id=GPL-3.0`）· 语言 **Python**（8 个 `.py`，共 **2061** 行）· 无 PyPI、无 `setup.py`、无测试

本机验证（**2026-09-26 00:31–00:40 EDT**）：Python **3.13.5** venv；numpy **2.5.3** / pandas **3.0.6** / scipy **1.18.1** / pyproj **3.8.0** / astropy **8.0.1** / gnsscal **1.1.2** / unlzw3 **0.2.3** / wget **3.2** / pygeodesy **26.9.9**。原样 `import CalcSwd` → **IndentationError**；打 3 处一行补丁后，GRAZ 站 2024-01-01 00 UTC 跑通 GPT3+GMF 与 VMF1 两条 SWD 路径（stdout 见 §4）。CDDIS 星历下载本机**失败**（FTPS `425 Security: Bad IP connecting.`），SINEX 写出整链**未跑**（见 §6 坑 8/9）。

> 岗位：已有 **测站 ZTD**（PPP 解或产品）+ 卫星方位/仰角 → 用 **GPT3/VMF1 模型 ZHD** 与 **GMF/VMF1 映射函数**把天顶量投影成**斜路径湿延迟 SWD**（GNSS 水汽层析的输入）。冲突时：**源码 > 本文 > 上游 README**。  
> 真正沿 NWM 射线积分 → [radiate](./radiate.md)；GPT3/VMF3 官方源码与格网 → [tu-wien-vmf-gpt-codes](./tu-wien-vmf-gpt-codes.md)；ZTD 从哪来 → [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md) / [rtklib](./rtklib.md)。

## 1. 用途与边界

**先弄懂 6 个词：**

| 术语 | 含义 | 量级（本文 GRAZ 实测） |
| --- | --- | --- |
| ZTD（Zenith Total Delay） | 信号从天顶方向穿过中性大气比真空多走的路程，= ZHD + ZWD | **2.2733** m |
| ZHD（Zenith Hydrostatic Delay，干延迟） | 由地面气压决定，可用 Saastamoinen 公式从气压算准到 mm 级 | **2.1847** m（GPT3 气压） |
| ZWD（Zenith Wet Delay，湿延迟） | 由水汽决定，变化快、难建模；≈ 可降水量 PWV 的 6–7 倍 | **0.0886** m |
| 斜延迟 STD / SWD | 沿卫星视线方向的总/湿延迟；低仰角时是天顶值的约 10 倍 | 5° 仰角 SWD **0.9570** m |
| 映射函数 mf(el) | 天顶→斜向的放大系数，干/湿各一条：`STD = ZHD·mf_h + ZWD·mf_w (+ 梯度项)` | 5° 时 mf_w **10.8001** |
| NWM（数值天气模型） | ECMWF 等全球气象格网；VMF1/VMF3 系数就是在 NWM 上射线追踪后拟合出来的 | — |

**做：**

- `GPT3.py`：GPT3（5°×5° 经验格网）→ 气压/温度/水汽压/Tm/ah/aw/大地水准面差距/梯度
- `CalcSwd.py`：Saastamoinen ZHD、`ZWD = ZTD − ZHD`、`SWD = ZWD·mf_w (+ mf_g·(Gn·cos az + Ge·sin az))`
- `GMF_GradinetMF.py`：GMF 映射函数 + Chen–Herring 型梯度映射（`c=0.0032`，再除以 1.4）
- `VMF.py`：从 TU Wien 下载 VMF1 2.5°×2° 格网 → 插值 ah/aw/zhd/zwd → VMF1 映射
- `satellite_read_int_elv_az.py`：从 CDDIS 拉超快星历并算方位/仰角；`Read_Write_TRP.py` 读写 SINEX-TRO；`save_Sinex_SWD_ZTD.py` 串成 SWD SINEX

**不做：**

- **不做射线追踪**：斜延迟由「天顶值 × 映射函数」得到，不沿 NWM 积分；需要真射线追踪用 [radiate](./radiate.md)
- **不估计 ZTD**：ZTD 必须外部给（PPP 引擎或 IGS/VMF 产品）
- **不是**可 `pip install` 的包；README 提到的 `Main_program.py` / `input_data.py` **在全部 git 历史里都不存在**

## 2. 文件地图

| 文件 | 行数 | 关键函数 | 外部依赖 |
| --- | ---: | --- | --- |
| `GPT3.py` | 418 | `gpt3_5_fast_readGrid`, `gpt3_5_fast(mjd,lat,lon,h_ell,it)` | `gpt3_5.grd`（cwd 相对路径） |
| `CalcSwd.py` | 181 | `ZHD_Saastamoinen`, `asknewet`, `CalcZWD`, `CalcSWDgrad`, `CalcSTD` | GPT3/VMF/GMF |
| `GMF_GradinetMF.py` | 148 | `gmf`, `gradient_MF(elev)` | — |
| `VMF.py` | 309 | `download_VMF`, `read_vmf1_grid`, `vmf1_ht`, `vmf1` | 网络 → `vmf.geo.tuwien.ac.at` |
| `GPT.py` | 209 | `gpt`（初代 GPT） | — |
| `satellite_read_int_elv_az.py` | 395 | `Download_Ultra_Orbit`, `Int_Orbit`, `Orbit_ELV_AZ` | CDDIS FTPS |
| `Read_Write_TRP.py` | 264 | `Readwrite_TRO_ZTD` | SINEX-TRO 文件 |
| `save_Sinex_SWD_ZTD.py` | 137 | `write_Sinex_SWD` | 以上全部 + pygeodesy |

仓内数据：`gpt3_5.grd` **1146104** B（与 TU Wien `/codes/gpt3_5.grd` **逐字节相同**，`cmp` 通过）；`geoids/egm2008-5.pgm` **18671444** B。

## 3. 安装

```bash
git clone https://github.com/zohrehadavi/STD_SWD_Calc.git
cd STD_SWD_Calc && git rev-parse --short HEAD        # 3e4552b
python3 -m venv ~/venv-stdswd && . ~/venv-stdswd/bin/activate
# README 列的 7 个 + 源码里实际 import 但 README 漏写的 scipy / pygeodesy
pip install pandas numpy scipy pyproj astropy gnsscal unlzw3 wget pygeodesy

# 必打补丁（原因见 §6）：CRLF 文件，按内容替换，已在全新 clone 上验证
sed -i '145s/^ def/def/' CalcSwd.py
sed -i -e 's#\\\\Mapping_Fcn\\\\vmf1\\\\#/Mapping_Fcn/vmf1/#g' \
       -e 's/jd = mjd + 2400000.5/jd = mjd + 2400001.0/' \
       -e 's/mjd_6h_list = np.array(\[mjd_6h_list - 0.25,mjd_6h_list,mjd_6h_list + 0.25\])/mjd_6h_list = np.ravel([mjd_6h_list - 0.25,mjd_6h_list,mjd_6h_list + 0.25])/' VMF.py
mkdir -p Mapping_Fcn/vmf1
git diff --stat      # CalcSwd.py 2 +-  /  VMF.py 8 ++++----
python -W ignore -c "import CalcSwd, save_Sinex_SWD_ZTD; print('import OK')"
```

`-W ignore` 只是压掉 `pd.read_csv(sep='\s+')` 的 `SyntaxWarning: invalid escape sequence '\s'`（Python 3.12+ 提示，不影响结果）。

## 4. 端到端（本机 · GRAZ 2024-01-01 00:00 UTC）

输入选择（全部可复核）：GRAZ 坐标取 TU Wien `station_coord_files/gnss.ell`（`47.0671 15.4935 538.30`）；**ZTD 取 VMF3_OP 站点产品 `2024001.vmf3_g` 中 GRAZ @MJD 60310.00 的 zhd+zwd = 2.1686+0.1047 m**（这是 NWM 模型值，代替 PPP 估计的 ZTD 做演示）；仰角/方位 90/30/10/5°、0/90/180/270° 为人为挑选的测试几何。

```bash
curl -fsSL -O https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF3/VMF3_OP/daily/2024/2024001.vmf3_g
grep GRAZ 2024001.vmf3_g | head -1
# GRAZ      60310.00  0.00120480  0.00058178  2.1686  0.1047   951.19   6.89   8.47
```

### 4a. GPT3 ZHD + GMF 映射（纯离线）

`demo_graz.py`（放在仓库根目录运行，因 `gpt3_5.grd` 用相对路径打开）：

```python
import time, numpy as np
from GPT3 import gpt3_5_fast
from CalcSwd import ZHD_Saastamoinen, CalcZWD, CalcSWDgrad
mjd = 60310.0                                   # 2024-01-01 00:00 UTC
lat, lon, h = np.radians(47.0671), np.radians(15.4935), 538.30   # GRAZ, VMF gnss.ell
t0 = time.time()
P,T,dT,Tm,e,ah,aw,la,undu,Gn_h,Ge_h,Gn_w,Ge_w = gpt3_5_fast(mjd,lat,lon,h,it=0)
h_ortho = h - float(np.ravel(undu)[0])
print(f"GPT3: p={float(np.ravel(P)[0]):.2f} hPa  undu={float(np.ravel(undu)[0]):.3f} m  h_ortho={h_ortho:.3f} m")
zhd = float(np.ravel(ZHD_Saastamoinen(mjd,h,h_ortho,lat,lon))[0])
ZTD = 2.1686 + 0.1047            # GRAZ zhd+zwd from VMF3_OP 2024001.vmf3_g @ MJD 60310.00
zwd = float(np.ravel(CalcZWD(mjd,ZTD,h,h_ortho,lat,lon,'zhd_GPT'))[0])
print(f"ZTD(input)={ZTD:.4f} m  ZHD(GPT3+Saast.)={zhd:.4f} m  ZWD={zwd:.4f} m")
ELV = np.array([90., 30., 10., 5.]); AZ = np.array([0., 90., 180., 270.])
for grad in ('False','True'):
    SWD,ZWD,mfw,mfg = CalcSWDgrad(mjd,ZTD,lat,lon,h,h_ortho,float(np.ravel(Gn_w)[0]),float(np.ravel(Ge_w)[0]),AZ,ELV,'GMF','zhd_GPT',grad)
    for i in range(len(ELV)):
        print(f"grad={grad:5s} el={ELV[i]:4.0f} az={AZ[i]:5.0f}  mfw={float(np.ravel(mfw)[i]):8.4f}  SWD={float(np.ravel(SWD)[i]):.4f} m")
print(f"wall {time.time()-t0:.2f} s")
```

本机 stdout（`python -W ignore demo_graz.py`，real **0.965 s**）：

```text
GPT3: p=959.59 hPa  undu=45.784 m  h_ortho=492.516 m
ZTD(input)=2.2733 m  ZHD(GPT3+Saast.)=2.1847 m  ZWD=0.0886 m
grad=False el=  90 az=    0  mfw=  1.0000  SWD=0.0886 m
grad=False el=  30 az=   90  mfw=  1.9968  SWD=0.1769 m
grad=False el=  10 az=  180  mfw=  5.6644  SWD=0.5019 m
grad=False el=   5 az=  270  mfw= 10.8001  SWD=0.9570 m
grad=True  el=  90 az=    0  mfw=  1.0000  SWD=0.0886 m
grad=True  el=  30 az=   90  mfw=  1.9968  SWD=0.1769 m
grad=True  el=  10 az=  180  mfw=  5.6644  SWD=0.5024 m
grad=True  el=   5 az=  270  mfw= 10.8001  SWD=0.9569 m
wall 0.17 s
```

交叉核对：同一输入下 TU Wien 官方 `gpt3_5.m`（Octave）/`gpt3_5.f90`（gfortran）/`saasthyd.m` 给出 p=**959.59** hPa、undu=**45.784** m、ZHD=**2.1847** m，与本仓逐位一致（见 [tu-wien-vmf-gpt-codes §4](./tu-wien-vmf-gpt-codes.md)）。梯度用的是 GPT3 湿梯度（Gn_w≈−2.2e-05 m、Ge_w≈2.3e-06 m），所以 `grad=True` 只在低仰角差 0.1–0.5 mm。

### 4b. VMF1 格网 ZHD + VMF1 映射（需联网，补丁后）

```python
# demo_vmf.py
import numpy as np
from VMF import read_vmf1_grid
from CalcSwd import CalcSWDgrad
lat, lon, h, h_ortho = np.radians(47.0671), np.radians(15.4935), 538.30, 492.516
ah,aw,zhd,zwd = read_vmf1_grid(60310.0,[47.0671,15.4935,538.30])
print(f"VMF1 grid @GRAZ: ah={float(ah):.8f} aw={float(aw):.8f} zhd={float(zhd):.4f} zwd={float(zwd):.4f}")
ELV = np.array([90., 30., 10., 5.]); AZ = np.zeros(4)
SWD,ZWD,mfw,mfg = CalcSWDgrad(60310.0,2.2733,lat,lon,h,h_ortho,0,0,AZ,ELV,'VMF','zhd_VMF','False')
print('ZWD =', np.round(np.ravel(ZWD),4)); print('mfw =', np.round(np.ravel(mfw),4)); print('SWD =', np.round(np.ravel(SWD),4))
```

本机 stdout（real **10.823 s**，含首次下载 4 个 `VMFG_20240101.H00–H18`，每个 **668655** B，落在 `Mapping_Fcn/vmf1/`）：

```text
VMF1 grid @GRAZ: ah=0.00122188 aw=0.00053192 zhd=2.0839 zwd=0.0800
ZWD = [0.1894]
mfw = [ 1.      1.9968  5.6656 10.8087]
SWD = [0.1894 0.3782 1.0731 2.0472]
```

**读结果：** 4b 的 ZWD 比 4a 大 **0.10 m**，不是真水汽差——VMF1 格网 zhd 是**格点地形高度**上的值，本仓未做高程归算（GRAZ 周边格点在阿尔卑斯更高处 → zhd 偏小 → ZWD 偏大）。对照 VMF3 站点产品 zhd=**2.1686** m。做层析时优先用 4a 路径或站点产品（坑 6）。

## 5. 输入 / 输出字段

`CalcSWDgrad(mjd, ZTD, dlat, dlon, dhgt, h_ortho, gn, ge, AZ, ELV, Type_MF, Type_zhd, grad)`：

| 参数 | 单位 / 取值 | 说明 |
| --- | --- | --- |
| `mjd` | 日（标量） | 修正儒略日；一次调用一个历元 |
| `ZTD` | m | 外部给的天顶总延迟 |
| `dlat`, `dlon` | **弧度** | 椭球纬度、经度（传度数不会报错，结果全错） |
| `dhgt` | m | 椭球高 |
| `h_ortho` | m | 正高；Saastamoinen 分母用 `0.00000028·h_ortho`；可用 `h_ell − undu(GPT3)` |
| `gn`, `ge` | m | 北/东水平梯度；无则填 0 |
| `AZ`, `ELV` | **度**（数组） | 方位、仰角（注意与经纬度单位不同） |
| `Type_MF` | `'GMF'` / 其他=VMF1 | 其他任何字符串都会走 VMF1 并触发下载 |
| `Type_zhd` | `'zhd_GPT'` / `'zhd_VMF'` | ZHD 来源 |
| `grad` | 字符串 `'True'` / `'False'` | 是字符串比较，传布尔 `True` 等于关掉梯度 |

返回 `SWD, ZWD, mf_w, MF_G`（m, m, 无量纲, 无量纲）。`CalcSTD(mjd,dlat,dlon,dhgt,h_ortho,AZ,ELV,Type_MF,Type_zhd)` 返回 `STD, ZTD`，**只在 VMF1 模式可用**：`'GMF','zhd_GPT'` 本机报 `UnboundLocalError: ... 'zwd'`；`'VMF','zhd_VMF'` 本机得 `STD= [ 4.3127 22.0409]`（30°/5°）`ZTD= [2.1639]`——ZTD 全来自未做高程归算的 VMF1 格网（对照站点产品 2.2733 m，见坑 6）。

`gpt3_5_fast(mjd, lat, lon, h_ell, it)` 输出 13 项：`p`[hPa] `T`[°C] `dT`[K/km] `Tm`[K] `e`[hPa] `ah` `aw`（VMF3 系数，零高程）`la` `undu`[m] `Gn_h Ge_h Gn_w Ge_w`[m]；每项形状 **(1,1)**。`it=1` 关掉年/半年项。

`*.vmf3_g` 站点行（本机 GRAZ 首行）：`站名 MJD ah aw zhd[m] zwd[m] p[hPa] T[°C] e[hPa]`。

## 6. 坑（现象 → 原因 → 修复）

1. **`import CalcSwd` 直接崩** → `IndentationError: unindent does not match any outer indentation level`（line 145）→ 上游最近一次提交给 `def CalcSTD` 多缩进了 1 个空格 →  
   `sed -i '145s/^ def/def/' CalcSwd.py`
2. **照 README 找 `Main_program.py` / `input_data.py` 找不到** → 这两个文件从未提交（`git log --all --name-only` 无记录）→ 自己写驱动，最小例见 §4a：  
   `git log --all --name-only --format= | grep -i -E 'main|input' || echo "never committed"`
3. **目录里冒出 `…\Mapping_Fcn\vmf1\xxxx.tmp` 这种带反斜杠的文件，随后 `FileNotFoundError`** → `VMF.py` 硬编码 Windows 路径 `pwd+"\\Mapping_Fcn\\vmf1\\"`；Linux 下反斜杠是普通字符，`wget` 把它当文件名前缀写到**上一级目录** →  
   `sed -i 's#\\\\Mapping_Fcn\\\\vmf1\\\\#/Mapping_Fcn/vmf1/#g' VMF.py && mkdir -p Mapping_Fcn/vmf1`
4. **VMF1 取错一天（2024-01-01 读成 `VMFG_20231231.*`）** → `mjd_to_ymd` 用 `int(mjd+2400000.5)`，漏了儒略日从正午起算的 +0.5：MJD 51544（2000-01-01）返回 1999-12-31 →  
   `sed -i 's/jd = mjd + 2400000.5/jd = mjd + 2400001.0/' VMF.py`（补丁后 60310.0→2024-01-01、60370.0→2024-03-01 已验证）
5. **`TypeError: only 0-dimensional arrays can be converted to Python scalars`（VMF.py `int(hh)`）** → 单历元时 `mjd_6h_list` 被堆成 (3,1) 数组，numpy 2.x 不再允许 `int()` 转 1 元素数组 →  
   `sed -i 's/mjd_6h_list = np.array(\[mjd_6h_list - 0.25,mjd_6h_list,mjd_6h_list + 0.25\])/mjd_6h_list = np.ravel([mjd_6h_list - 0.25,mjd_6h_list,mjd_6h_list + 0.25])/' VMF.py`
6. **`zhd_VMF` 路径 ZWD 系统性偏大（本机 +0.10 m）** → `read_vmf1_grid` 对格网 zhd 只做 `griddata` 水平插值，没有从格点地形高度归算到测站高 → 改用 GPT3+Saastamoinen（或自行按 Kouba 2008 归算 / 用 TU Wien `vmf1_grid.m`）：  
   在调用里把 `Type_zhd='zhd_VMF'` 换成 `Type_zhd='zhd_GPT'`
7. **`gpt3_5_fast` 报 `TypeError ... 0-dimensional` 或循环很慢** → 本仓 `GPT3.py` 只接受**标量** lat/lon/h，而且每次调用都重读 1.1 MB 格网（50 次调用 **2.37 s**；TU Wien 站上的 `gpt3_5_fast.py` 先读一次格网再循环 **0.69 s**）→ 批量时改用官方端口：  
   `curl -fsSLO https://vmf.geo.tuwien.ac.at/codes/Python_Tools_Adavi/gpt3_5_fast.py -O https://vmf.geo.tuwien.ac.at/codes/Python_Tools_Adavi/gpt3_5_fast_readGrid.py`
8. **`Download_Ultra_Orbit(..., Name_Datasource='IGS')` 报 `UnboundLocalError: cannot access local variable 'destination'`**（本机实测）→ 非 `igv` 分支用了未定义的 `D`/`DoY`，异常被裸 `except: pass` 吞掉，最后 `return destination` 才炸 → 目前只有 `igv`（GLONASS 目录下的 IGS 超快）分支写全了：  
   `python -W ignore -c "from satellite_read_int_elv_az import Download_Ultra_Orbit as d; print(d(2024,1,1,'.','you@example.org','igv',0))"`——本机 stdout 为 `./IGR22952.SP3`，但 `ls` 该文件**不存在**：返回的是拼好的路径，不代表下载成功（原因见坑 9）
9. **星历下载静默失败、后续文件不存在** → 本仓走 CDDIS **FTPS 匿名**（邮箱当密码）且吞掉所有异常；本机直接测 `FTP_TLS(...).nlst()` 得到 `ftplib.error_temp: 425 Security: Bad IP connecting.`（数据通道被拒）→ 改用 Earthdata 账号 + HTTPS 手动下 SP3，再喂给 `Int_Orbit`/`Orbit_ELV_AZ` 之后的步骤（账号配置见 [data-access](../data-access.md)；本机无账号未跑）：  
   `curl -n -L -c ~/.urs_cookies -b ~/.urs_cookies -O https://cddis.nasa.gov/archive/gnss/products/2295/IGS0OPSULT_20240010000_02D_15M_ORB.SP3.gz`
10. **在别的目录运行脚本报 `FileNotFoundError: gpt3_5.grd` / `ModuleNotFoundError: GPT3`** → 格网按 cwd 相对路径打开、模块靠同目录导入 → 始终在仓库根执行：  
    `cd /path/to/STD_SWD_Calc && python -W ignore your_script.py`

## 7. 接到 GNSS / 电离层工作流的哪一步

- **ZTD 来源**：[pride-pppar](./pride-pppar.md)（`ztd_` 文件）、[ginan](./ginan.md)（PPP 估对流层）、[rtklib](./rtklib.md)（`pos1-tropopt=est-ztd`；RTKLIB 默认 NMF，编译 `-DIERS_MODEL` 才用 GMF）。把它们的 ZTD 当本仓 `ZTD` 输入，映射函数最好与 PPP 解算时一致，否则 SWD 带映射函数差。
- **SWD → 水汽层析**：GNSS 水汽层析以 SWD 为观测量（作者引用的 J Geod 2022 即层析方法论文）；PWV 需再乘 Tm 相关换算因子（`asknewet` 的逆过程，本仓未提供）。
- **与电离层的关系**：对流层是**非色散**延迟，双频无电离层组合消不掉，必须建模/估计；做 TEC/GIM（教程 [06](../tutorials/06-iono-positioning.md)）时 ZTD 误差会进坐标和钟差，不会进几何无关 TEC。
- **需要真射线追踪的 STD**（低仰角、强水平梯度）：[radiate](./radiate.md)；GNSS-IR 的仰角折射改正用的是 GPT2w，见 [gnssrefl](./gnssrefl.md)。

## 8. 许可与引用

- 代码 **GPL-3.0**：修改后再分发须同样开源。`gpt3_5.grd` 与 `GPT3.py`/`VMF.py` 源自 TU Wien（Landskron & Böhm 2018 GPT3/VMF3），VMF1 格网受 VMF Data Server 使用条款约束（非预报产品 CC BY 4.0，需致谢 ECMWF），详见 [tu-wien-vmf-gpt-codes §7](./tu-wien-vmf-gpt-codes.md)。
- 作者要求引用：Adavi, Weber & Rohm, J Geod 96, 27 (2022), doi:10.1007/s00190-022-01620-1；Zenodo doi:10.5281/zenodo.8405850。
