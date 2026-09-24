# rtklib-py · demo5 思路纯 Python PPK 操作手册

目录：[`PROJECTS.json` → `rtklib-py`](../../PROJECTS.json) · 上游 <https://github.com/rtklibexplorer/rtklib-py> · tip **`5d8968d`**（2023-10-07）· ★**247** · 许可 **MIT** · **无 PyPI** · 本机验证（**2026-09-24 07:20 EDT**；**质检复跑 07:27 EDT**：Python **3.13.15**/numpy **2.5.3**；maxepoch=**40**→`rover.pos` **5493** B；Q **30**×2+**10**×1；首 fix **40.097023872°N** ratio=**3.4**）：Python **3.13.15** / numpy **2.5.3**；仓内 `data/u-blox`（rover **6638661** B/**2163** 历元，base `tmg23590.obs` **17379469** B/**7200** 历元，`rover.nav` **63633** B）；`src/run_ppk.py` + `maxepoch=40` → `rover.pos` **5493** B/**40** 历元；Q：**30**×float(2)+**10**×fix(1)；首 fix **2137 425310.005** → **40.097023872°N −105.147249846°E h=1578.1212** m ratio=**3.4**；末历元 ratio=**3.8**；对照仓内 `py_0315f.pos` 同行近 tow **40.097024085°N … h=1578.1589**（ns 字段本机冒烟写 **0**，参考全日解为 **11–13**）

> 岗位：用 **纯 Python** 复现 rtklibexplorer **demo5** 风格的**事后 PPK**，便于读算法/改实验后迁回 C。冲突时：**仓内 `README.md` / `config_*.py` / 本机 `.pos` > 本文**。  
> CLI 主力 → [rtklib](./rtklib.md)；demo5/EX 二进制 → [rtklib-explorer](./rtklib-explorer.md)；C 扩展绑定 → [pyrtklib](./pyrtklib.md)；CLAS/MADOCA/HAS 现代树 → [mrtklib](./mrtklib.md)。

**与姊妹页差别：**

| 手册 | 本质 |
| --- | --- |
| [rtklib.md](./rtklib.md) | C CLI（`rnx2rtkp`/`convbin`；apt 或自编） |
| [rtklib-explorer.md](./rtklib-explorer.md) | demo5→**EX 2.5.1** C 叉（低成本接收机优化） |
| [pyrtklib.md](./pyrtklib.md) | **pybind11** 调官方 **2.4.3** C 核（有 PyPI） |
| [mrtklib.md](./mrtklib.md) | 现代化 C 树 + `mrtk`（开放 SSR） |
| **本文 rtklib-py** | **纯 Python 子集**，对齐 demo5 思路，**仅 PPK** |

## 1. 用途与边界

**做：**

- `src/run_ppk.py`：读 rover/base OBS + NAV → `*.pos` / `*.pos.stat` / `*.trace`
- 配置 `config_f9p.py`（车载 u-blox）/ `config_phone.py`（GSDC 手机例）
- 星座：GPS + GLONASS + Galileo；双频 PPK；模糊度 fix-and-hold 等 demo5 常见项
- 调试：`trace_level`（3 时消息刻意贴近 demo5）

**不做：**

- **不是** 实时 RTK / NTRIP 客户端 → [rtklib](./rtklib.md) / [rtkbase](./rtkbase.md)
- **不是** `pip install` 包（**PyPI 无** `rtklib-py` / `rtklibpy`）
- **不是** 全量 RTKLIB（无 PPP 产品链、无全部星座/信号；BDS/QZSS 等以源码为准）
- **不是** C 性能生产引擎；解与 demo5「非常接近但非逐字节相同」
- 手机例需改 `run_ppk.py` 注释块；本机冒烟用 **u-blox** 夹具

一句话：rtklib-py = **可读的 demo5-PPK Python 地图**；产线仍回 C/[rtklib-explorer](./rtklib-explorer.md)。

| 术语 | 含义 |
| --- | --- |
| `run_ppk.py` | 顶层脚本；会 `chdir` 到 `datadir` |
| `__ppk_config.py` | 运行时从 `cfgfile` 复制出的配置模块 |
| `filtertype` | `forward` / `backward` / `combined`… |
| `armode` | 0 off / 1 continuous / **3** fix-and-hold（f9p 默认） |
| Q | `.pos` 质量：1=fix，2=float，…（同 RTKLIB 习惯） |

## 2. vs rtklib / explorer / pyrtklib / mrtklib

| | **本文** | [rtklib](./rtklib.md) | [rtklib-explorer](./rtklib-explorer.md) | [pyrtklib](./pyrtklib.md) | [mrtklib](./mrtklib.md) |
| --- | --- | --- | --- | --- | --- |
| 实现 | 纯 Python | C CLI | C EX fork | C 绑定 | C 现代树 |
| 场景 | 教学/改算法 PPK | 通用 RTK/PPP | 低成本 RTK | 脚本调 C | PPP-RTK SSR |
| 安装 | clone + numpy | apt/源码 | 源码/发布包 | **pip** | 源码 |
| 本机 | 40 历元 PPK | apt/EX | GSI 实跑 | F9P `pntpos` | SPP/RTK |

## 3. 安装

```bash
python3 -m venv ~/iono_ops/venv-rtklib-py
source ~/iono_ops/venv-rtklib-py/bin/activate
pip install -U pip numpy          # 本机 numpy 2.5.3 可用
git clone https://github.com/rtklibexplorer/rtklib-py.git
cd rtklib-py && git rev-parse --short HEAD   # 5d8968d
ls src/*.py data/u-blox data/phone
# 无 setup.py / 无 PyPI 轮子 → 在 src/ 下直接跑
```

依赖实质：**numpy**（`rtkcmn`/`rtkpos`/`mlambda`…）。勿与 [pyrtklib](./pyrtklib.md) 混名为同一包。

## 4. 端到端（本机 · u-blox 夹具）

```bash
cd /path/to/rtklib-py/src
# 可选：冒烟限历元（默认 None=全日）
# 临时改 run_ppk.py: maxepoch = 40
python3 run_ppk.py
# 输出写在 data/u-blox/（脚本 chdir 后）
ls -la ../data/u-blox/rover.pos ../data/u-blox/rover.pos.stat ../data/u-blox/rover.trace
```

默认输入（`run_ppk.py`）：

| 变量 | 值 |
| --- | --- |
| `datadir` | `../data/u-blox` |
| `rovfile` / `basefile` / `navfile` | `rover.obs` / `tmg23590.obs` / `rover.nav` |
| `cfgfile` | `config_f9p.py` |

**本机结果（maxepoch=40，2026-09-24 07:20 EDT；质检复跑 07:27 EDT）：**

```text
Reading rover/base/nav … Calculating solution …
进度：22:08:00–22:08:29 → Q=2；22:08:30–22:08:39 → Q=1
rover.pos     5493 B / 40 历元
rover.pos.stat  142476 B
rover.trace     625159 B
Q counts: {2: 30, 1: 10}
首 fix: 2137 425310.005  40.097023872 -105.147249846  1578.1212  Q=1  ratio=3.4
末行:   2137 425319.005  40.097023895 -105.147249854  1578.1256  Q=1  ratio=3.8
参考 py_0315f.pos @425319.000 ≈ 40.097024085 -105.147249761  1578.1589  Q=1 ns=13
```

手机例：改 `run_ppk.py` 使用 `data/phone` + `config_phone.py`（GSDC Pixel4）；本机**未**重跑。

全日对照：仓内已有 `py_0315f.pos`（**4522** 行含头）与 `demo5_b34f_f.pos`；完整重跑去掉 `maxepoch` 限制即可（耗时随 **2163** 历元上升）。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| rover/base `.obs` | RINEX 观测；base 头或 `rb` 给基准坐标 |
| `.nav` | 广播星历（可由 rover 附带） |
| `config_*.py` | 对齐 RTKLIB 风格的 Python 配置 |

| 输出 | 说明 |
| --- | --- |
| `<rov>.pos` | RTKLIB 风格解（周/TOW/纬度/经度/高/Q/ns/…） |
| `<rov>.pos.stat` | 状态统计 |
| `<rov>.trace` | `trace_level>0` 时 stderr 重定向 |

## 6. 参数速查（`config_f9p.py` 节选）

| 项 | 本机默认 | 备注 |
| --- | --- | --- |
| `nf` | 2 | 频点数 |
| `pmode` | `kinematic` | 或 `static` |
| `filtertype` | `forward` | combined 等见源码 |
| `elmin` / `elmaskar` | 15° | 浮点 / AR 仰角门 |
| `cnr_min` | `[35,35]` | 信噪比门 |
| `armode` | 3 | fix-and-hold |
| `thresar` | 3 | AR 比值阈 |
| `gnss_t` | GPS,GLO,GAL | 处理星座 |
| `rb` / `rr_f` | 全 0 | 0→用 RINEX 头 / 标准起算 |

改配置后必须保证 `run_ppk.py` 里 `cfgfile` 指向对应文件；脚本每跑会覆盖 `__ppk_config.py`。

## 7. 接到哪步

1. 同一数据用 C 对照 → [rtklib-explorer](./rtklib-explorer.md) / [rtklib](./rtklib.md)  
2. 要在脚本里调 C 核而非重写 → [pyrtklib](./pyrtklib.md)  
3. 开放 SSR / CLAS 等 → [mrtklib](./mrtklib.md) / [cssrlib](./cssrlib.md)  
4. 观测准备 → [georinex](./georinex.md)；产品级 PPP-AR → [pride-pppar](./pride-pppar.md)

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ModuleNotFoundError: __ppk_config` | 不在 `src/` 跑或复制失败 | `cd src` 再 `python3 run_ppk.py` |
| 2 | `No module named numpy` | 未装依赖 | `pip install numpy` |
| 3 | pip 找不到包 | **无 PyPI** | 只能 clone；别搜错成 [pyrtklib](./pyrtklib.md) |
| 4 | 与 demo5 `.pos` 不完全重合 | 实现子集 + 数值路径差 | README 已声明；比趋势/固定段而非逐历元盲对齐 |
| 5 | `ns` 列为 0 | 冒烟/写出路径差异 | 看 Q 与坐标；对照 `py_0315f.pos` 全日参考 |
| 6 | 路径像 Windows | 旧注释 `C:\gps\...` | 用仓内相对 `../data/...` |
| 7 | 实时流/串口 | 本包不做 | 换 [rtklib](./rtklib.md) `str2str` / [rtkbase](./rtkbase.md) |
| 8 | 当 PPP-AR 引擎 | 无精密产品链 | [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md) |
| 9 | 与 pyrtklib API 混用 | 一个是纯 Python，一个是 C 扩展 | 分清 import 路径与版本 |
| 10 | `trace` 吞掉终端 | `sys.stderr` 重定向到文件 | 查 `*.trace`；或 `trace_level=0` |
| 11 | tip 停在 2023 | 上游低活跃 | 锁定 **`5d8968d`**；改算法自担回迁 |
| 12 | 手机例无解 | 仍指向 u-blox 配置 | 切换 `run_ppk.py` 注释块 + `config_phone.py` |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 读/改 PPK 算法（Python） | **本文 rtklib-py** |
| 生产/日常 RTK·PPP CLI | [rtklib](./rtklib.md) |
| 低成本接收机 demo5/EX | [rtklib-explorer](./rtklib-explorer.md) |
| Python 调 C 核批量 | [pyrtklib](./pyrtklib.md) |
| CLAS/MADOCA/HAS 现代树 | [mrtklib](./mrtklib.md) |

## 10. 相关

[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md) · [pyrtklib](./pyrtklib.md) · [mrtklib](./mrtklib.md) · [cssrlib](./cssrlib.md) · [pride-pppar](./pride-pppar.md) · [georinex](./georinex.md) · [README](./README.md)
