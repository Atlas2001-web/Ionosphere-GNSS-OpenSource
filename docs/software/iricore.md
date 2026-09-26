# iricore · IRI-2016/2020 的 ctypes Python 包装（剖面 + 垂直/斜 TEC）操作手册

目录：[`PROJECTS.json` → `iricore`](../../PROJECTS.json) · 上游 <https://github.com/MIST-Experiment/iricore> · 文档 <https://iricore.readthedocs.io/en/latest> · PyPI **1.9.0**（2024-10-21 06:09 EDT 上传，只有 sdist + macOS arm64 轮子）· master `92c6d8c`（2024-10-21 05:39 EDT；`git describe` = `1.8.1-9-g92c6d8c`，仓里没有 1.9.0 tag）· 许可 **MIT**（© 2022 Vadym Bidula；内含 IRI 官方 Fortran）· 本机实跑 2026-09-26 05:40–05:52 EDT（CPython 3.13.5，venv，GNU Fortran 14.2.0，CMake 3.31.6）

> 岗位：`pip install` 后一行 Python 拿到 IRI 电子密度剖面、F 层峰值参数，以及**沿视线积分的 vTEC / sTEC**（TECU）。和 [iri2016](./iri2016.md) / [iri2020](./iri2020.md) 的区别：两版 IRI 装在同一个包里；自带 `vtec()`/`stec()`；能用关键字传入实测 foF2/hmF2/F10.7。冲突时：**源码 `iri.py` / `tec.py` / `irioutput.py` 文档串 > 本文**。

## 1. 它解决什么 / 不做什么

**做：**

- `iricore.iri(dt, [h0, h1, dh], lat, lon, version=20)` → `IRIOutput`：`edens`（m⁻³）、`ntemp/itemp/etemp`（K）、离子成分 `o/h/he/o2/no/cluster/n`（默认 %）、`oarr`（100 个附加量：NmF2、hmF2、B0、F10.7、Rz12、IG12…）
- `iricore.vtec(dt, lat, lon)`：90–2000 km 按 0.5 km 步长积分，返回 TECU；`lat/lon` 可以是等长数组
- `iricore.stec(el, az, dt, lat, lon)`：沿给定仰角/方位的直线（球形地球）逐点调 IRI 积分，返回 TECU；`return_details=True` 给出射线经纬高与 Ne
- `iricore.update()`：从 CHAIN 服务器下载新的 `apf107.dat` / `ig_rz.dat`；请求日期超出指数文件时**自动**调用

**不做：**

- 不是 GNSS TEC 估计：不读 RINEX、不求 DCB。它给的是**气候态模型值**，拿来和观测 TEC 对照
- 不做同化（IRTAM 系数驱动见 [pyirtam](./pyirtam.md)）；不含 IRI-2026（最新版见 [iri-fortran](./iri-fortran.md)）
- `refstec()`（带折射的射线追踪 sTEC）本文未实跑
- 不出图、不写文件

| 相邻页面 | 关系 |
| --- | --- |
| [iri2020](./iri2020.md) | 同为 IRI-2020 Fortran；不在 PyPI、每次起子进程；本页 §3.3 在同一场景下 F2 峰值逐位一致 |
| [iri2016](./iri2016.md) / [pyglow](./pyglow.md) | 老版 IRI 包装，接口是 xarray / 对象 |
| [pyiri](./pyiri.md) | 纯 Python 重写的 IRI，不用 Fortran 编译器 |
| [ntcmg](./ntcmg.md) | Galileo 广播模型 NTCM-G；§3 同一时刻同一地点可以拿来比 |
| [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) | 从 RINEX 求观测 TEC，再与本页模型值对比 |

## 2. 安装

```bash
sudo apt install -y cmake gfortran                  # 本机已有：cmake 3.31.6 / GNU Fortran 14.2.0
python3 -m venv ~/iono_ops/.venv-iricore && source ~/iono_ops/.venv-iricore/bin/activate
pip install --no-cache-dir iricore==1.9.0            # Linux 没有轮子 → 走 sdist 现场编译 libiri2016.so / libiri2020.so
python -u -c "import iricore, numpy; print(iricore.__file__, numpy.__version__)"
```

本机装出的版本：iricore 1.9.0、numpy **1.26.4**、pymap3d 3.2.0、fortranformat 2.0.3。`pyproject.toml` 写的是 `numpy = "^1.25.0"`（即 <2），Python 3.13 上没有 numpy 1.26 的轮子，pip 会把 **numpy 也从源码编译**（`numpy-1.26.4.dist-info/WHEEL` 显示 `Generator: meson`、`Tag: cp313-cp313-linux_x86_64`）。和另一个包在同一次 pip 调用里，总共约 1.5 分钟；venv 301 MB。

安装后包目录里有 `libiri2016.so`、`libiri2020.so`、`data/`（ccir/ursi/igrf/mcsat 系数 + `index/apf107.dat`、`index/ig_rz.dat`）。**自带指数文件到 2024-06-17 为止**（`apf107.dat` 末行 `24  6 17 …`）。

## 3. 端到端

### 3.1 武汉 2024-03-20 06 UT：剖面 + vTEC + sTEC（用包里自带的指数文件）

`iri_e2e.py`：

```python
from datetime import datetime
import numpy as np, iricore
dt = datetime(2024, 3, 20, 6, 0)   # UT；武汉当地正午附近
lat, lon = 30.5, 114.4
for v in (16, 20):
    r = iricore.iri(dt, [100, 1000, 10], lat, lon, version=v)
    i = int(np.nanargmax(r.edens))
    print(f"IRI-20{v}: height.size={r.height.size} edens.max={r.edens[i]:.4e} m-3 at height={r.height[i]:.0f} km")
    print(f"   oarr[0] NmF2={r.oarr[0]:.4e} m-3  oarr[1] hmF2={r.oarr[1]:.1f} km  oarr[36] TEC={r.oarr[36]:.4e} m-2"
          f"  oarr[40] F10.7={r.oarr[40]:.1f}  oarr[32] Rz12={r.oarr[32]:.1f}  oarr[38] IG12={r.oarr[38]:.1f}")
    print(f"   foF2(由NmF2)={np.sqrt(r.oarr[0]/1.24e10):.2f} MHz  Te(300km)={r.etemp[20]:.0f} K  Ti(300km)={r.itemp[20]:.0f} K  O+(300km)={r.o[20]:.1f} %")
    print(f"   vtec(90-2000km)={iricore.vtec(dt, lat, lon, version=v):.3f} TECU")
    print(f"   stec(el=30,az=180)={iricore.stec(30, 180, dt, lat, lon, version=v):.3f} TECU")
```

本机 stdout（刚装好、未调用过 `update()`，05:47 EDT）：

```text
IRI-2016: height.size=91 edens.max=2.1909e+12 m-3 at height=320 km
   oarr[0] NmF2=2.1924e+12 m-3  oarr[1] hmF2=316.9 km  oarr[36] TEC=0.0000e+00 m-2  oarr[40] F10.7=174.1  oarr[32] Rz12=136.7  oarr[38] IG12=112.5
   foF2(由NmF2)=13.30 MHz  Te(300km)=1866 K  Ti(300km)=1188 K  O+(300km)=98.9 %
   vtec(90-2000km)=65.774 TECU
   stec(el=30,az=180)=136.700 TECU
IRI-2020: height.size=91 edens.max=2.1909e+12 m-3 at height=320 km
   oarr[0] NmF2=2.1924e+12 m-3  oarr[1] hmF2=316.9 km  oarr[36] TEC=-1.0000e+00 m-2  oarr[40] F10.7=174.1  oarr[32] Rz12=136.7  oarr[38] IG12=112.5
   foF2(由NmF2)=13.30 MHz  Te(300km)=1866 K  Ti(300km)=1188 K  O+(300km)=98.9 %
   vtec(90-2000km)=65.774 TECU
   stec(el=30,az=180)=136.700 TECU
```

- 两版 IRI 在默认 `jf` 下输出完全一样。本机又试了 3 个时间地点（2020-06-01 12 UT −10°/−50°、2015-01-01 00 UT 60°/20°），`max|edens16−edens20|` 都是 0.0；每个进程只加载一个 `.so` 的结果也一样，所以不是符号冲突。iricore 给两版传的是**同一套 `jf`**（`get_jf('default')`，其中 [38,39] 选 Shubin hmF2），源码里两版 `irifun.for`/`irisub.for` 有几千行差异，但在这组开关下没有体现（为什么没体现本文未深究）
- `oarr[36]`（TEC）不能用：IRI-2016 给 0、IRI-2020 给 −1。TEC 请用 `iricore.vtec()`
- 136.700/65.774 = 2.08，就是 30° 仰角的倾斜放大系数

### 3.2 取新指数：`update()` 与未来日期

```bash
python -u -c "import iricore; iricore.update()"
```

```text
The index data was successfully updated
```

之后 `apf107.dat` 从 24275 行变成 25104 行，末行 `26  9 24 …`（到 2026-09-24）。同一个 3.1 场景再跑，IRI-2020 输出变了：

```text
20 nan count edens: 0 / 91 NmF2 2277256200000.0 hmF2 316.8589 F10.7 174.1 Rz12 99.3187 IG12 119.216125
   vtec 63.1942256001024
16 nan count edens: 91 / 91 NmF2 -1.0 hmF2 -1.0 F10.7 -1.0 Rz12 -1.0 IG12 -1.0
.../iricore/tec.py:118: UserWarning: NANs or INFs found in the IRI output; setting them to 0.
   vtec 0.0
```

- IRI-2020：Rz12 从 136.7 变成 99.3，IG12 从 112.5 变成 119.2，F10.7 的 365 天均值从 161.4 变成 176.4（`apf107.dat` 里 `24  3 20` 这一行的最后一列）→ NmF2 从 2.1924e12 变成 2.2773e12，vTEC 从 65.774 变成 **63.194** TECU。**自带的 `ig_rz.dat` 对 2024 年用的是预测值，更新后换成了实测值**
- IRI-2016：更新后**整条剖面都是 NaN**，`vtec` 只发一个 warning，然后返回 0.0（见坑 1）

请求一个包里没有的日期时会自动更新：

```text
Requested date is not covered in database. Updating indices.
The index data was successfully updated
hmF2=293.8 km NmF2=1.4121e+12 m-3 F10.7(oarr[40])=101.7 vtec=40.804 TECU
```

（2026-09-20 06 UT 武汉；`oarr[40]`=101.7 与 `apf107.dat` 里 `26  9 20` 行的日 F10.7 `101.7` 一致。）

### 3.3 与 [iri2020](./iri2020.md) 同一场景交叉核对：2020-04-01 12 UT，20°N 10°E，90–700 km

```python
dt = datetime(2020, 4, 1, 12); r = iricore.iri(dt, [90, 700, 10], 20.0, 10.0, version=20)
print(f"NmF2_m-3={r.oarr[0]:.6e} hmF2_km={r.oarr[1]:.2f} foF2_MHz={np.sqrt(r.oarr[0]/1.24e10):.4f} F10.7={r.oarr[40]:.1f} Rz12={r.oarr[32]:.2f} IG12={r.oarr[38]:.2f}")
print(f"vTEC_trapz_90-700km_TECU={np.trapz(r.edens, r.height*1e3)/1e16:.3f}  iricore.vtec(90-700,hstep=0.5)={iricore.vtec(dt,20.0,10.0,htop=700):.3f}")
```

```text
NmF2_m-3=1.494191e+12 hmF2_km=335.00 foF2_MHz=10.9772 F10.7=69.2 Rz12=2.33 IG12=-9.12
vTEC_trapz_90-700km_TECU=38.690  iricore.vtec(90-700,hstep=0.5)=38.755
```

NmF2/hmF2/foF2 与 iri2020 页 §3.1 **逐位相同**（1.494191e+12 / 335.00 / 10.9772）；自带文件和更新后的文件跑出来一样（2020 年的指数没变）。90–700 km 梯形积分 vTEC 是 38.690，iri2020 页是 38.149，差 1.4%：峰值一样，峰以外的剖面有差别。原因可能是两个驱动传的 `jf` 不同（iri2020 驱动设了 `jf(22)=.false.`），本文未逐项核对。

### 3.4 数组、用户输入、积分步长

```text
grid: edens.shape=(3, 91) oarr.shape=(3, 100) hmF2(oarr[:,1])=[354.  316.9 257. ] NmF2(oarr[:,0])=[1.4996615e+12 2.2772562e+12 1.4494926e+12] t=0.01s
vtec(lat array)= [52.492 63.194 43.774] TECU
user foF2=10 MHz -> oarr[0] NmF2=1.2400e+12 m-3; vtec=36.987 TECU
vtec hstep=0.5 km -> 63.194 TECU
vtec hstep=2.0 km -> 63.555 TECU
vtec hstep=10.0 km -> 65.329 TECU
vtec htop=1000 km -> 60.429 TECU
stec details keys=['ds', 'edens', 'h', 'lat', 'lon', 'oarr'] npoints=(1000,) IPP-ish lat at h=450: 24.494 t=0.85s
```

（已更新指数，IRI-2020；lat=[10, 30.5, 50]，lon 都是 114.4。）`oarr0=10.0` 小于 100，被当成 foF2（MHz）：NmF2 = 1.24e10×10² = 1.24e12，和输出一致。所以用户输入**是能用的**，catalog 里“未实现 OARR 用户输入”这句话对 1.9.0 已经过时（`92c6d8c` 提交说明就是 “Added manual user input to vtec() and stec()”）。

## 4. 参数 / 字段

| 函数 | 参数 | 单位 / 取值 | 源码约束 |
| --- | --- | --- | --- |
| `iri` | `dt` | naive `datetime`，**UT** | 带时区会 `TypeError`（坑 6） |
| | `altrange` | `[起, 止, 步]` km | 点数 >1000 报 `ValueError` |
| | `lat`, `lon` | 地理 °；可以是等长数组 | 长度不等报 `ValueError` |
| | `version` | `16` 或 `20`（默认 20） | 其他值会触发一个 `TypeError`（坑 4） |
| | `jf` | `'default'` / `'default_edens'` / 50 元 int 数组 | 表格见 `get_jf` 文档串 |
| | `oarr0/1/2/3/4/5/9/14/32/34/38/40/45` | foF2(MHz, <100) 或 NmF2(m⁻³)；hmF2 km；Rz12；IG12；F10.7 等 | 传入后自动把对应 `jf` 置 0 |
| `vtec` | `hbot/htop/hstep` | km，默认 90/2000/0.5 | `hbot<60` 或 `htop>2000` 报 `ValueError` |
| `stec` | `el, az` | ° | 直线、球形地球（`pm.Ellipsoid(R_EARTH, R_EARTH)`） |
| | `hobs` | **m**（传给 `pymap3d.aer2geodetic`） | 射线的高度网格仍是 `heights`（km），与 `hobs` 无关 |
| | `npoints` / `heights` | 默认 90–2000 km 等分 1000 点 | |

`IRIOutput` 常用字段（单位见 `irioutput.py` 文档串，已与 §3 输出对过）：

| 字段 | 含义 | 单位 |
| --- | --- | --- |
| `height` | 高度网格 | km |
| `edens` | 电子密度 | m⁻³（负值→NaN） |
| `etemp` / `itemp` / `ntemp` | 电子 / 离子 / 中性温度 | K |
| `o, h, he, o2, no, cluster, n` | 离子成分 | %（默认 `jf[21]`=1） |
| `oarr[0]` / `oarr[1]` | NmF2 / hmF2 | m⁻³ / km |
| `oarr[9]` | B0 | km |
| `oarr[32]` / `oarr[38]` | Rz12 / IG12 | — |
| `oarr[40]` / `oarr[45]` | F10.7 日值 / 81 天均值 | sfu |
| `oarr[36]` | TEC | 本包不计算（0 或 −1） |

## 5. 怎么读结果

- **foF2 ↔ NmF2**：foF2(MHz) = √(NmF2 / 1.24e10)，NmF2 用 m⁻³。3.1 里 2.1924e12 → 13.30 MHz，是太阳活动高年春分正午的中纬度量级
- **vTEC 是模型的气候值**：一天内的扰动、磁暴都不会体现。和观测对比时，差 20–30% 很常见。这里 2024-03-20 武汉 IRI-2020 给 63.194 TECU（已更新指数），NTCM-G 用当天 Galileo 广播系数给 89.35 TECU（[ntcmg](./ntcmg.md) §3.2），两个模型本身就差 40%
- **sTEC/vTEC 比**：30° 仰角约 2.08。这是沿真实射线积分的结果，不是单层映射函数
- **积分设置会影响结果**：`hstep` 从 0.5 km 改成 10 km，vTEC 多了 2.1 TECU；`htop` 从 2000 km 降到 1000 km，vTEC 少了 2.8 TECU（1000 km 以上等离子体层那部分）。和 GNSS TEC（到 20200 km）比时要注意这一点
- **换指数文件，同一历史日期的结果也会变**（§3.2）：写论文时要记下 `apf107.dat`/`ig_rz.dat` 的末行

## 6. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `update()` 以后 `version=16` 整条 `edens` 都是 NaN，`oarr` 全是 −1，`vtec` 只发 `UserWarning: NANs or INFs found…` 然后返回 **0.0** | IRI-2016 的 `read_ig_rz` 数组是 `aig(806),arz(806)`；新 `ig_rz.dat` 从 1958-01 一直到 2028-11，装不下（IRI-2020 源码 2023-12 已把数组加大到 1600） | 更新后只用 IRI-2020：`iricore.vtec(dt, lat, lon, version=20)`；非要用 2016 就把包目录下的 `data/index/ig_rz.dat` 换回 sdist 里的原文件 |
| 2 | 同一个历史日期，昨天和今天算出来的 vTEC 不一样（65.774 → 63.194） | 请求日期晚于 2024-06-17 时会**自动** `update()`，覆盖包内的 `ig_rz.dat`（Rz12 预测值换成实测值）和 `apf107.dat` | 复现实验前把两个文件存档：`python -c "import iricore,os;print(os.path.dirname(iricore.__file__)+'/data/index')"`，然后 `cp` 备份 |
| 3 | `RuntimeError: Requested indices are not available yet. The update latency is usually 2-3 days.` | 当天或最近 2–3 天的 `apf107` 还没发布（本机 2026-09-26 请求 09-30 时出现） | 把日期往前推，或手动给指数：`iricore.iri(dt, [100,1000,10], lat, lon, oarr40=150, oarr45=150)` |
| 4 | `version=2020` → `TypeError: sequence item 0: expected str instance, int found` | 只接受 `16`/`20`；报错那行 `", ".join(IRI_VERSIONS)` 拼接的是 int，所以本该提示的 `ValueError` 变成了 `TypeError` | `iricore.iri(dt, [100,1000,10], lat, lon, version=20)` |
| 5 | `ValueError: The specified altitude range and step require more than 1000 points…` | IRI_SUB 一次最多 1000 个高度点（如 60–2000 km 步长 1 km） | 分段算或加大步长：`iricore.iri(dt, [60, 2000, 2], lat, lon)`（`vtec()` 自己会分段） |
| 6 | `TypeError: can't compare offset-naive and offset-aware datetimes` | 传了带时区的 `datetime`；内部用 `dt.hour` 当 UT，并与 naive 的 `_LAST_DATE` 比较 | 先转成 UT 再去掉时区：`dt = dt.astimezone(timezone.utc).replace(tzinfo=None)` |
| 7 | 在 numpy 1.26 环境里 `np.trapezoid` 报 `AttributeError` | iricore 限定 numpy<2，而 `trapezoid` 是 numpy 2.0 才有的名字 | 用旧名：`np.trapz(r.edens, r.height*1e3)/1e16` |
| 8 | `pip install iricore` 很慢，或者报 `CMake`/`gfortran` 找不到 | Linux 没有轮子，要现场编译两个 Fortran 库，Python 3.13 上还得编译 numpy 1.26 | `sudo apt install -y cmake gfortran && pip install --no-cache-dir iricore==1.9.0` |
| 9 | 拿 `oarr[36]` 当 TEC，得到 0 或 −1 | 本包调用的 IRI_SUB 不填这个量 | `iricore.vtec(dt, lat, lon)`（TECU） |
| 10 | 在 clone 下来的仓里跑 `pytest tests` → `ImportError: Could not import IRI libraries…` | 测试 `import src.iricore`，要求 `.so` 编译在源码树里，并且要在 `tests/` 目录下运行（数据路径写的是 `data/…`） | 要么不跑，要么先在源码树里编译：`cd iricore && cmake . && make`（本文未实跑） |

## 7. 许可与诚实边界

- 包装代码 MIT；IRI Fortran 与系数按 IRI 官方条款（AS IS + 署名，见 [iri-fortran](./iri-fortran.md)）。指数文件来自 CHAIN（`chain-new.chain-project.net/echaim_downloads/`），本机 2026-09-26 可以匿名下载。
- **实跑**：pip 源码安装；§3.1–3.4 全部输出；`update()` 和自动更新；坑 1–7 的报错都在本机复现过。
- **未实跑**：`refstec()`（射线追踪）、仓内 `tests/`、`jf` 的 FIRI/NeQuick 顶部等非默认组合、Windows/macOS。为什么两版 IRI 在默认 `jf` 下结果相同，没有逐行比对 Fortran 源码。
- 维护：最后一次提交是 2024-10；**绑定的是 IRI-2016/2020，不是 IRI-2026**。

## 8. 链接

- 教程：[04 IRI 与 NeQuick](../tutorials/04-iri-nequick.md) · [01 TEC 基础](../tutorials/01-ionosphere-tec-basics.md)
- 兄弟：[iri2020](./iri2020.md) · [iri2016](./iri2016.md) · [iri-fortran](./iri-fortran.md) · [pyiri](./pyiri.md) · [pyirtam](./pyirtam.md) · [ntcmg](./ntcmg.md) · [pymsis](./pymsis.md)
