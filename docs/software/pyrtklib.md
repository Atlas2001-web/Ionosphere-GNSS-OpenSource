# pyrtklib · RTKLIB Python 绑定操作手册

目录：[`PROJECTS.json` → `pyrtklib`](../../PROJECTS.json) · 上游 <https://github.com/IPNL-POLYU/pyrtklib> · 许可 **MIT** · tip **`1c468db`**（2025-10-03）· PyPI **`pyrtklib` 0.2.7** · 捆 **RTKLIB 2.4.3**（`VER_RTKLIB`）· 本机：pip 轮子 + 仓内 F9P OBS/`BRDC` → `readrnx` **56934** 测值 · 首历元 `pntpos` **ok=1 / Q=5 / ns=4** → **22.320106847°N 114.211129029°E h=22.700 m** · 前 60 历元 `pntpos_ok=23` · **2026-09-24 06:25 EDT**

> 岗位：在 Python 脚本里直接调 RTKLIB **C 核心**（`readrnx` / `pntpos` / `postpos` / RTCM…），做批量后处理与 DL 紧耦合试验。冲突时：**仓内 `readme.md` / `.pyi` / 本机函数签名 > 本文**。日常 CLI → [rtklib](./rtklib.md)；纯 Python NavData/WLS → [gnss_lib_py](./gnss_lib_py.md)；ROS 因子图 → [graphgnsslib](./graphgnsslib.md)。

**与 [rtklib.md](./rtklib.md) 的差别：** `rtklib.md` 讲 **`rnx2rtkp`/`convbin` CLI**（含 explorer EX）；本文是 **pybind11 绑定**——接口接近 C（`Arr1D*` 指针容器），**没有**独立 CLI。内核停在官方树 **2.4.3**；要 demo5/explorer 算法请走姊妹仓 [pyrtklib_demo5](https://github.com/IPNL-POLYU/pyrtklib_demo5)，勿与本包混装。

## 1. 用途与边界

**做：**

- `pip install pyrtklib` 后 `from pyrtklib import *` / `import pyrtklib as prl`
- 读 RINEX OBS/NAV → `obs_t`/`nav_t`；单历元 `pntpos`；全弧 `postpos`
- 城市峡谷 + 深度学习权重等试验（论文 TITS 2025；前端另见 TASGNSS）

**不做：**

- **不是** `rnx2rtkp` 替代品 → [rtklib](./rtklib.md)
- **不是** 纯 Python 重写 → rtklibexplorer/`rtklib-py`；也不是 Alain Muls 的 [pyRTKLib](https://github.com/alainmuls/pyRTKLib)（教学绘图，**无**原生绑定）
- **不是** 发表级 PPP-AR / CLAS/MADOCA 主力 → [pride-pppar](./pride-pppar.md) / [mrtklib](./mrtklib.md) / [ginan](./ginan.md)
- **不是** TEC/ROTI 产品 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- 示例 `example_postpos.py` 依赖的 Whampoa 基线文件 **未**随 0.2.7 数据目录发布 → 本机用 F9P+BRDC 做 `pntpos` 冒烟，**未**臆造 `postpos` stdout

一句话：pyrtklib = **港理工 IPNL 的 RTKLIB 2.4.3 Python 扩展**（C 性能 + 脚本编排）。

| 术语 | 含义 |
| --- | --- |
| `VER_RTKLIB` | 绑定内嵌核心版本字符串（本机 **`2.4.3`**） |
| `Arr1Dchar` / `Arr1Dobsd_t` … | 可当指针用的 1D 容器；**无边界检查** |
| `FileWrapper` | v0.2.7 起管理 `FILE*` 上下文（RTCM 续读等） |
| `pntpos` / `postpos` | 单历元 SPP / 事后处理入口（同 C API） |
| `pyrtklib_demo5` | 对接 rtklibexplorer demo5 的**另一仓库** |

## 2. 安装

### 2.1 pip（推荐）

```bash
python3 -m venv ~/iono_ops/.venv-pyrtklib
source ~/iono_ops/.venv-pyrtklib/bin/activate
pip install -U pip
pip install pyrtklib
python -c "import pyrtklib as p; print(p.VER_RTKLIB, p.__file__)"
# 本机：2.4.3 …/site-packages/pyrtklib/__init__.py · PyPI 0.2.7 · cp313 manylinux
```

轮子按 **CPython 小版本 + 平台** 分发（含 3.12/3.13）。无匹配轮子时再源码编。

### 2.2 源码（无轮子时）

```bash
sudo apt-get install -y cmake g++ python3-dev
git clone https://github.com/IPNL-POLYU/pyrtklib.git
cd pyrtklib && python setup.py install
# 或：pip install .
```

依赖 **cmake + C/C++ 编译器**；macOS 作者提示优先 GNU 工具链（RTKLIB 用了 GNU C 特性）。

### 2.3 核对 tip / 样例数据

```bash
cd ~/iono_ops && git clone --depth 1 https://github.com/IPNL-POLYU/pyrtklib.git
cd pyrtklib && git rev-parse --short HEAD   # 1c468db
ls example/data/
# BRDC00IGS_R_20213370000_01D_MN.rnx · F9P_211203_061807.obs
```

## 3. 端到端（本机 · `readrnx` + `pntpos`）

```bash
cd ~/iono_ops/pyrtklib/example
python <<'PY'
import pyrtklib as prl, math
obs, nav, sta = prl.obs_t(), prl.nav_t(), prl.sta_t()
# 注意：绑定签名无 type 参数 → (file, rcv, opt, obs, nav, sta)
print('obs', prl.readrnx('data/F9P_211203_061807.obs', 1, '', obs, nav, sta), 'n', obs.n)
print('nav', prl.readrnx('data/BRDC00IGS_R_20213370000_01D_MN.rnx', 1, '', obs, nav, sta),
      'nav.n', nav.n, 'ng', nav.ng)
i = n = 0
while i + n < obs.n and abs(prl.timediff(obs.data[i+n].time, obs.data[i].time)) <= 0.05:
    n += 1
sol = prl.sol_t(); sol.time = obs.data[0].time
azel = prl.Arr1Ddouble(n * 2)
ssat = prl.Arr1Dssat_t(prl.MAXSAT)
msg = prl.Arr1Dchar(128)
ok = prl.pntpos(obs.data.ptr, n, nav, prl.prcopt_default, sol, azel, ssat.ptr, msg)
pos = prl.Arr1Ddouble(3); prl.ecef2pos(sol.rr, pos)
print('pntpos', ok, 'stat', sol.stat, 'ns', sol.ns)
print(f'{pos[0]*180/math.pi:.9f} {pos[1]*180/math.pi:.9f} {pos[2]:.3f}')
PY
```

**本机结果（2026-09-24 06:25 EDT）：**

| 项 | 值 |
| --- | --- |
| `readrnx` OBS | ret **1**，`obs.n`=**56934** |
| `readrnx` NAV | ret **1**，`nav.n`=**11530**，`ng`=**1152** |
| 首历元星数 | **24**（`time.time`=1638515280） |
| `pntpos` | **ok=1**，`stat`=**5**（single），`ns`=**4** |
| LLH | **22.320106847°N 114.211129029°E**，h=**22.700** m |
| 前 60 历元 | `pntpos_ok`=**23**（城市峡谷/可视不足属正常；勿当固定率） |

### 3.1 官方 `postpos` 示例（本机未跑完整基线）

```bash
# example/example_postpos.py 默认要：
#   data/20210714.2.whampoa.ublox.f9p.obs + hksc1950.21[fon]
# 当前 example/data/ 仅 F9P+BRDC → 缺基线文件时不要硬跑后假装有 .pos
python example_postpos.py   # 有完整数据时：写 pyexample_output.txt
```

需要 CLI 对照同一 OBS 时：先 [rtklib](./rtklib.md) 的 `rnx2rtkp -p 0`，再回脚本比 ECEF。

## 4. 关键 API / 参数

| API / 项 | 作用 |
| --- | --- |
| `readrnx(path, rcv, opt, obs, nav, sta)` | 读 RINEX；**无**第 4 个 type 字符串（与旧 C 文档习惯不同） |
| `pntpos(...)` | 单历元伪距定位 → `sol_t` |
| `postpos(ts,te,tint,…,prcopt,solopt,…,files,…)` | 事后处理；文件列表为 Python `list[str]` |
| `prcopt_default` / `solopt_default` | 默认定解算/输出选项；可改 `mode`/`nf`/`navsys` |
| `PMODE_SINGLE`=0 · `PMODE_KINEMA`=2 | 与 RTKLIB 同号 |
| `Arr1D*` 切片 / `list(arr)` | 调试打印；写入越界 → segfault |

## 5. 接到哪步

| 下一步 | 手册 |
| --- | --- |
| CLI 冒烟 / explorer EX | [rtklib](./rtklib.md) |
| Python NavData / 手机测量 | [gnss_lib_py](./gnss_lib_py.md) |
| ROS+Ceres FGO | [graphgnsslib](./graphgnsslib.md) |
| 现代 PPP-RTK（CLAS/MADOCA/HAS） | [mrtklib](./mrtklib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md) |
| 工作流 D | QC →（可选 pyrtklib 批处理）→ PPP-AR；教程 [06](../tutorials/06-iono-positioning.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `TypeError: readrnx(): incompatible…` 多一个 `''` | 绑定签名无 type 参数 | `readrnx(path,1,'',obs,nav,sta)` |
| 2 | `pip` 找不到轮子 | 平台/ABI 无匹配 | 换 3.10–3.13 或按 §2.2 源码编 |
| 3 | 与 `pyrtklib_demo5` 同 venv 互相覆盖 | 包名冲突 | 分 venv；demo5 单独装 |
| 4 | `Arr1D` 赋值后偶发崩 | 无边界检查 / 悬挂指针 | 少改 `obs.data=`；长度先对上 `n`/`nmax` |
| 5 | `example_postpos` FileNotFound | Whampoa 文件未随包 | 自备基线或只跑 §3 |
| 6 | 以为输出=explorer EX | 内核是 **2.4.3** 非 demo5 | 算法对齐 → `pyrtklib_demo5` 或 [rtklib](./rtklib.md) explorer |
| 7 | `postpos` 返回非 0 | 缺 NAV/时间窗/基线坐标 | 先 `pntpos` 单历元；查 `prcopt.rb` |
| 8 | 把 `stat=5` 当固定 | Q5=single | 固定看 Q=1；相对定位配基线 |
| 9 | 与 alainmuls/pyRTKLib 搞混 | 同名不同实现 | 认准 **IPNL-POLYU/pyrtklib** |
| 10 | macOS clang 编不过 | GNU 扩展 | 按上游用 brew gcc 或直接 pip 轮子 |
| 11 | 期望出 STEC/GIM | 本包是定位绑定 | TEC → [pytecgg](./pytecgg.md) |
| 12 | `FileWrapper` 读 RTCM 停住 | EOF 未清 | `fp.cleareof()` 后再读（见 readme 示例） |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Python 调原生 RTKLIB C | **本文 pyrtklib** |
| 命令行 `.pos` / explorer | [rtklib](./rtklib.md) |
| demo5 算法的 Python 绑定 | `pyrtklib_demo5`（另仓） |
| NavData + 教学 WLS | [gnss_lib_py](./gnss_lib_py.md) |
| FGO 研究 | [graphgnsslib](./graphgnsslib.md) |
| CLAS/MADOCA/HAS 一体 CLI | [mrtklib](./mrtklib.md) |

## 8. 相关

[rtklib](./rtklib.md) · [gnss_lib_py](./gnss_lib_py.md) · [graphgnsslib](./graphgnsslib.md) · [mrtklib](./mrtklib.md) · [ginan](./ginan.md) · [pride-pppar](./pride-pppar.md) · [cssrlib](./cssrlib.md) · [README](./README.md)

- 论文：Hu et al., *IEEE TITS* 2025（doi:10.1109/TITS.2025.3552691）；代码≠论文逐行
- 更 Pythonic 前端：TASGNSS（PolyU-TASLAB）
