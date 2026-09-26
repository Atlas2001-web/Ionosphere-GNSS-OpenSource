# pyRTKLib-RINEX（alainmuls/pyRTKLib）· 调 rnx2rtkp + 出图的 Python 脚本集 操作手册

目录：[`PROJECTS.json` → `pyRTKLib-RINEX`](../../PROJECTS.json) · 上游 <https://github.com/alainmuls/pyRTKLib> · **无 LICENSE 文件**（GitHub API `license=null`，版权默认归作者，复用/再分发前先问作者）· tip **`4d9a89c`**（2021-02-09，之后无提交；★50）· 本机 Python **3.13.5**（失败）/ **3.8.20**（出图成功）· 解算器 Debian `rnx2rtkp` **2.4.3 b34** · **2026-09-26 01:07–01:10 EDT** 实跑：仓内 Septentrio AsteRx3 Galileo E1 单频 `GALI0171.20O`（2020-01-17 06:00–11:59:59，1 Hz）→ SPP **21359** 历元全 Q=5 → `pyrtkplot.py` 生成 **11** 张 PNG + 9 个 CSV/JSON。上游 `pyrtkproc.py` **原样跑不出结果**（`sys.exit(6)`，见坑 2），本文给出 3 处最小补丁。

> 岗位：把 RINEX 观测交给 RTKLIB 的 `rnx2rtkp` 做 SPP/RTK，再把 `.pos` / `.pos.stat` 画成 UTM 偏移、散点、CN0、伪距残差、仰角、接收机钟差、DOP 图。**它自己不做定位解算**，也不绑定 RTKLIB 的 C 代码。

## 0. 先分清三个 “pyrtklib”

| 页面 | 上游 | 是什么 | 解算在哪 |
| --- | --- | --- | --- |
| **本文** pyrtklib-rinex | alainmuls/pyRTKLib | 一堆独立脚本：生成 conf → `subprocess` 调外部 `rnx2rtkp` → pandas/matplotlib 出图 | 外部可执行 `rnx2rtkp`（PATH 里哪个就用哪个） |
| [pyrtklib](./pyrtklib.md) | IPNL-POLYU/pyrtklib | RTKLIB 2.4.3 C 函数的 **Python 绑定**，`import pyrtklib` | 进程内 C 库 |
| [pyrtklib-demo5](./pyrtklib-demo5.md) | IPNL-POLYU/pyrtklib_demo5 | demo5/EX 2.5.0 的绑定，`import pyrtklib5` | 进程内 C 库 |

没有 `pip install` 包；名字相同纯属巧合，API 毫无关系。

## 1. 名词

| 术语 | 含义 |
| --- | --- |
| RINEX | 接收机无关的 GNSS 观测（`.20O`）/ 导航（`.20N` GPS、`.20E` Galileo、`.20P` 混合）文本格式 |
| `rnx2rtkp` | RTKLIB 的命令行后处理程序；`-k conf` 读配置，`-o` 写 `.pos` |
| `.pos` | 每历元一行：GPST 周+秒、纬经高、Q（1 fix/2 float/5 single）、ns 卫星数、标准差 |
| `.pos.stat` | `out-outstat=residual` 时的附带文件：`$POS` `$VELACC` `$CLK` `$SAT`（方位/仰角/伪距残差/CN0） |
| SPP | 单点定位，只用伪距+广播星历，米级 |
| UTM | 通用横轴墨卡托投影，把经纬度换成东/北（米），便于看“偏了几米” |
| CN0 | 载噪比（dB-Hz），信号强弱 |
| PRres | 伪距残差（m），RTKLIB 最小二乘后每颗星的剩余误差 |
| xDOP | 几何精度因子（H 水平/V 垂直/P 位置/G 几何），越小几何越好 |
| SBF | Septentrio 二进制格式；本仓 `pysbfdaily.py` 负责拼日文件 |

## 2. 仓库里有什么（按用途）

| 脚本 | 作用 | 本机状态 |
| --- | --- | --- |
| `pyrtkproc.py` | 用 `rnx2rtkp.tmpl` 生成 conf，再调 `rnx2rtkp -k conf -o …pos` | **原样在第 208 行 `sys.exit(6)` 退出**；打 3 处补丁后跑通 |
| `pyrtkplot.py` | 读 `.pos` + `.pos.stat` → UTM/ENU、DOP、分布统计、PNG | Py3.13+pandas 3 失败；Py3.8+pandas 0.25 + 1 处 sed 后跑通 |
| `pysbfdaily.py` / `pyconvbin`（README 提到，仓内无 `pyconvbin.py`） | SBF 拼日、转 RINEX | 需 Septentrio `sbf2rin`，未跑 |
| `pyftposnav.py` | FTP 下载导航文件 | 依赖 CDDIS 匿名 FTP（已停），未跑 |
| `rnx_obs_tabular.py` / `gfzrnx_obstab.py` | 观测表格化 | 依赖 `gfzrnx`，未跑 |
| `glab_*.py` | gLAB 输出解析/出图 | 未跑，见 [glab-upc](./glab-upc.md) |
| `data/rnx/` | 样例：`GALI0171.20O/E`（Gal）、`GPSS0171.20O/N`（GPS）、`P1710171.20O/P`（混合），共约 163 MB | 本文用 GALI |

README 假定目录结构 `${HOME}/RxTURP/BEGPIOS/<ASTX|BEGP|uBlox>/YYDDD/`，作者自注“从未在别的目录结构下测过”。模板默认路径写死 `~/amPython/pyRTKLib/rnx2rtkp.tmpl`，一定要 `-t` 覆盖。

## 3. 安装

```bash
git clone --depth 1 https://github.com/alainmuls/pyRTKLib ~/iono_ops/src/pyRTKLib
sudo apt-get install -y rtklib            # 提供 /usr/bin/rnx2rtkp（2.4.3 b34）
```

`requirements.txt` 锁的是 2019 年版本（numpy 1.16.3、pandas 0.24.2、matplotlib 3.0.3）。本机两条路：

```bash
# A. 只跑 pyrtkproc（Py3.13 也行，缺啥装啥）
python3 -m venv ~/iono_ops/venv-pyrtklib-rinex && . ~/iono_ops/venv-pyrtklib-rinex/bin/activate
pip install termcolor pandas numpy matplotlib utm scipy seaborn tabulate geopy pyproj webcolors

# B. 出图用 Py3.8 + 老 pandas（pyrtkplot 在 pandas≥1 下报错，见坑 5）
uv venv -p 3.8 ~/iono_ops/venv-pyrtklib-rinex38 && . ~/iono_ops/venv-pyrtklib-rinex38/bin/activate
grep -vE "^(numpy|pandas|matplotlib|Cython|pudb|urwid|pylint|astroid|flake8|isort|pyproj|kiwisolver)==" \
  ~/iono_ops/src/pyRTKLib/requirements.txt > /tmp/req38.txt
uv pip install -r /tmp/req38.txt numpy==1.17.5 pandas==0.25.3 matplotlib==3.1.3 "kiwisolver<1.4" pyproj==2.6.1.post1
```

本机 B 装出：matplotlib 3.1.3 / numpy 1.17.5 / pandas 0.25.3 / scipy 1.4.1 / seaborn 0.10.1 / termcolor 1.1.0 / utm 0.5.0。

## 4. 端到端实跑（本机，仓内 Galileo 样例）

### 4.1 原样跑：为什么没有输出

```bash
mkdir -p /tmp/prr && cp ~/iono_ops/src/pyRTKLib/data/rnx/GALI0171.20{O,E} /tmp/prr/ && cd /tmp/prr
python ~/iono_ops/src/pyRTKLib/pyrtkproc.py -d /tmp/prr -r GALI0171.20O -e GALI0171.20E -g gal \
  -t ~/iono_ops/src/pyRTKLib/rnx2rtkp.tmpl
```

第一次：

```
INFO: location.py - locateProg !!! did not found executable crz2rnx in path. Program Exits
exit=2
```

放一个 `crz2rnx` 到 PATH（坑 1）后再跑：打印完 `amc.dRTK` JSON 就 `exit=6`，`rtkp/gal/` 目录是空的。

### 4.2 最小补丁（在副本上改，不动上游）

```bash
cd ~/iono_ops/src/pyRTKLib
sed -e 's/^    sys.exit(6)$/    pass  # patched/' \
    -e "s/^    amc.dRTK\['template'\] = template$/    amc.dRTK['template'] = template\n    amc.dRTK['Tropo'] = tropo\n    amc.dRTK['Iono'] = iono/" \
    -e "s/^    if logLevels\[0\] >= amc.dLogLevel\['INFO'\]:/    if True:  # patched/" \
    pyrtkproc.py > /tmp/prr/pyrtkproc_patched.py
```

三处分别对应坑 2、3、4。

### 4.3 解算（Py3.13 venv A）

```bash
cd /tmp/prr && . ~/iono_ops/venv-pyrtklib-rinex/bin/activate
PATH=~/iono_ops/pyrr-bin:$PATH PYTHONPATH=~/iono_ops/src/pyRTKLib \
  python pyrtkproc_patched.py -d /tmp/prr -r GALI0171.20O -e GALI0171.20E -g gal \
  -t ~/iono_ops/src/pyRTKLib/rnx2rtkp.tmpl 2>&1 | grep -v "PATH \["
```

关键输出（墙时 3.4 s，exit 0）：

```
INFO: pyrtkproc_patched.py - main: Running:
/usr/bin/rnx2rtkp -k /tmp/prr/rtkp/gal/GALI0171_20O-GAL.conf -o rtkp/gal/GALI0171_20O.pos GALI0171.20O  GALI0171.20E
INFO: pyrtkproc_patched.py - main: Created statistics file: rtkp/gal/GALI0171_20O.pos.stat
```

产物：`GALI0171_20O-GAL.conf`（5477 B）、`.pos`（2819979 B）、`.pos.stat`（15030586 B）、`GALI0171.20O-proc.log`。

`.pos` 头与前 2 行：

```
% program   : RTKLIB ver.2.4.3
% obs start : 2020/01/17 06:00:00.0 GPST (week2088 453600.0s)
% obs end   : 2020/01/17 11:59:59.0 GPST (week2088 475199.0s)
% pos mode  : Single
% elev mask : 5.0 deg
% ionos opt : Broadcast
% tropo opt : Saastamoinen
% navi sys  : Galileo
2088 453600.0   50.844014537    4.392935137   148.4432   5   5   9.8322   8.2462   8.7020  -8.6186  -6.8543   8.2437   0.00    0.0
2088 453601.0   50.844012123    4.392937633   148.0841   5   5   9.8307   8.2442   8.7029  -8.6167  -6.8536   8.2437   0.00    0.0
```

统计：21600 个观测历元中 **21359** 行有解，全部 Q=5；`.pos.stat` 中 `$POS`/`$VELACC`/`$CLK` 各 21359 行、`$SAT` 135228 行。

### 4.4 出图（Py3.8 venv B + 1 处 sed）

```bash
cp -r ~/iono_ops/src/pyRTKLib /tmp/prr/pyRTKLib-p && rm -rf /tmp/prr/pyRTKLib-p/data
grep -rl "weight='strong'" /tmp/prr/pyRTKLib-p --include=*.py | xargs sed -i "s/weight='strong'/weight='bold'/g"   # 7 个文件
. ~/iono_ops/venv-pyrtklib-rinex38/bin/activate && export MPLBACKEND=Agg
PYTHONPATH=/tmp/prr/pyRTKLib-p python /tmp/prr/pyRTKLib-p/pyrtkplot.py -d /tmp/prr/rtkp/gal \
  -f GALI0171_20O.pos -m 50.8440152778 4.3929283333 151.39179
```

`-m` 用的是脚本 help 里给的 RMA（比利时皇家军事学院）参考点，与样例 APPROX 位置吻合。墙时 14.6 s，exit 0。日志节选（去色）：

```
INFO: pyrtkplot.py - main: dataframe dfStatENU (#8)
             dUTM.E        dUTM.N         dEllH
count  21359.000000  21359.000000  21359.000000
mean  -0.057524      1.251318     -1.796772
std    0.564449      0.986051      1.092835
min   -2.441171     -1.386530     -8.110490
max    3.573664      7.348987      2.807410
INFO: pyrtkplot.py - main: dataframe dfDistXDOP (#6)
             HDOP  VDOP   PDOP   GDOP
(0.0, 2.0]  16211  6758  1307   718
(2.0, 3.0]  3686   8692  13492  13879
(6.0, inf]  75     1462  1462   2578
INFO: plot_position.py - plotUTMOffset: created plot /tmp/prr/rtkp/gal/png/GALI0171_20O-ENU.png
```

`GALI0171_20O.pos.json` 里的加权平均：`lat 50.84402462707088 / lon 4.392927681445908 / ellH 149.54345134479408`，sdn/sde/sdu = 3.284 / 2.723 / 5.310 m；PDOP<6 的历元占 93.2 %；用到 13 颗 Galileo（E01 E03 E04 E05 E09 E11 E13 E15 E19 E21 E24 E25 E27）。

即：单频 Galileo SPP 相对参考点北向偏 +1.25 m、高程 −1.80 m，水平 1σ 约 0.6–1.0 m——这是单频广播星历 SPP 的正常量级，不代表脚本有精度增益。

生成的 11 张 PNG（`rtkp/gal/png/`）：`ENU` `ENU-dist` `scatter` `scatter-bin` `CN0` `GAL-CN0-dist` `PRres` `GAL-PRres-dist` `Elev` `CLK` `XDOP`。

## 5. 参数表

### 5.1 `pyrtkproc.py`

| 旗标 | 默认 | 写进 conf 的键 | 说明 |
| --- | --- | --- | --- |
| `-d DIR` | `./` | —— | 根目录；脚本先 `chdir` 过去，`-r/-e` 相对它 |
| `-r ROVEROBS` | 必填 | `${roverObs}` | 流动站 RINEX O；以 `D.Z` 结尾才会调 `crz2rnx` |
| `-b BASEOBS` | 空 | `${baseObs}` | `-m` 非 single 时必填 |
| `-e EPHEM…` | 必填 | `${navFiles}` | 导航文件，可多个 |
| `-m MODE` | `single` | `pos1-posmode` | single/dgps/kinematic/static/moving-base/fixed/ppp-kinematic/ppp-static |
| `-f {1..5}` | 1 | `pos1-frequency` | 1=l1 … 5=l1+l2+l5+l6+l7 |
| `-c {0..14}` | 5 | `pos1-elmask` | 截止高度角；**不接受 ≥15** |
| `-g` | `gal` | `pos1-navsys` | gps=1/sbas=2/glo=4/gal=8/com=9/qzs=16/comp=32；**一次只能选一个**（`com=9`=GPS+Gal） |
| `-s` | `brdc` | `pos1-sateph` | brdc/precise/… |
| `-a` | `saas` | `pos1-tropopt` | off/saas/sbas/est-ztd/est-ztdgrad（补丁 2 后才生效） |
| `-i` | `brdc` | `pos1-ionoopt` | off/brdc/sbas/dual-freq/…（同上） |
| `-t` | `~/amPython/pyRTKLib/rnx2rtkp.tmpl` | —— | 模板；务必显式给 |

模板里写死的其余项：`out-outstat=residual`（所以一定有 `.pos.stat`）、`out-solformat=llh`、`out-timeform=tow`、`pos1-soltype=forward`、`pos2-armode=continuous`。

### 5.2 `pyrtkplot.py`

| 旗标 | 说明 |
| --- | --- |
| `-f FILE` | `.pos` 文件名（相对 `-d`）；`.pos.stat` 自动按同名找 |
| `-d DIR` | 结果目录 |
| `-m LAT LON H` | 参考点（度/度/m）；缺省 `0 0 0` = 用均值作参考 |
| `-p` | 交互显示；无显示器时不要加，并设 `MPLBACKEND=Agg` |

### 5.3 `pyrtkplot.py` 产物字段（`.pos.posn` CSV）

`WNC,TOW,lat,lon,ellH,Q,ns,sdn,sde,sdu,sdne,sdeu,sdun,age,ratio,DT,UTM.E,UTM.N,UTM.Z,UTM.L,dUTM.E,dUTM.N,dEllH,PDOP,HDOP,VDOP,GDOP`。`.pos.sats`：`WNC,TOW,SV,Freq,Azim,Elev,PRres,CFres,Valid,CN0,DT`；`.pos.clks`：`WNC,TOW,mode,rcv,GPS,GLO,GAL,OTH,DT`（单位按 RTKLIB `$CLK`，ns）。

## 6. 坑（现象 → 原因 → 一条修复命令）

1. **`did not found executable crz2rnx in path. Program Exits`，exit 2** → `main()` 无条件 `locateProg('crz2rnx')`，缺失即退出，哪怕输入不是 `.D.Z` → 装 RNXCMP（见 [rnxcmp](./rnxcmp.md)），或临时占位：`mkdir -p ~/iono_ops/pyrr-bin && ln -sf "$(command -v crx2rnx)" ~/iono_ops/pyrr-bin/crz2rnx`（占位不能真解 `.Z`）。
2. **打印完 JSON 就结束，exit 6，`rtkp/<gnss>/` 为空** → tip `4d9a89c` 在 `roverobs_decomp()` 之后留着调试用 `sys.exit(6)` → `sed -i 's/^    sys.exit(6)$/    pass/' pyrtkproc_patched.py`。
3. **去掉 exit 后 `Traceback … KeyError: 'Tropo'`，exit 1，目录仍空** → `create_rnx2rtkp_settings()` 按模板占位符 `${Tropo}`/`${Iono}` 去取 `amc.dRTK['Tropo']`，而 `main()` 只存了 `atm_tropo`/`atm_iono` → 在 `amc.dRTK['template'] = template` 后补两行（见 §4.2 第二条 `-e`）。
4. **`TypeError: '>=' not supported between instances of 'str' and 'int'`（第 228 行）** → `logLevels[0]` 是字符串 `'INFO'`，却和 `dLogLevel['INFO']` 整数比较 → `sed -i "s/^    if logLevels\[0\] >= amc.dLogLevel\['INFO'\]:/    if True:/" pyrtkproc_patched.py`。
5. **`pyrtkplot.py` 一启动 `ValueError: Value must be a nonnegative integer or None`** → `pd.set_option('display.max_colwidth', -1)` 在 pandas≥1.0 被禁 → 用 §3 路线 B（pandas 0.25.3 + Py3.8）：`uv venv -p 3.8 ~/iono_ops/venv-pyrtklib-rinex38`。
6. **画图时 `ValueError: weight is invalid`** → 7 个绘图模块用了 matplotlib 不认的 `weight='strong'` → `grep -rl "weight='strong'" . --include=*.py | xargs sed -i "s/weight='strong'/weight='bold'/g"`。
7. **`pip install -r requirements.txt` 失败，`module 'configparser' has no attribute 'SafeConfigParser'`** → numpy 1.16.3 等 2019 锁版在 Py3.13 无轮子、源码构建用了已删 API → 不要装原锁文件，按 §3 A/B 选装。
8. **`-c 15` 报 `invalid choice`** → argparse `choices=range(0, 15)` 只到 14 → 要 15° 就改生成的 conf 再手跑：`sed -i 's/^pos1-elmask *=.*/pos1-elmask =15/' rtkp/gal/*-GAL.conf && rnx2rtkp -k rtkp/gal/GALI0171_20O-GAL.conf -o rtkp/gal/GALI0171_20O.pos GALI0171.20O GALI0171.20E`（本机实测：`% elev mask : 15.0 deg`，有解历元 21359→**20563**）。
9. **想同时解 GPS+Galileo，`-g gps gal` 报错** → `-g` 只收一个值；GPS+Gal 的代号是 `com`（=9） → `-g com -e GPSS0171.20N GALI0171.20E`（本机未跑，仅按代码映射）。
10. **结果和同事用 RTKPOST 跑的对不上** → 脚本调 PATH 里第一个 `rnx2rtkp`，本机是 Debian 2.4.3 b34，作者 help 目录是 2.4.2 手册；demo5 版行为不同 → 先确认：`which -a rnx2rtkp && rnx2rtkp -? 2>&1 | head -3`。

## 7. 诚实边界

- 无许可证文件：只能阅读和本地使用，再分发/改作需作者授权。
- 2021-02 后无维护；两个主脚本在 tip 上都**不能原样运行**（proc 被 `sys.exit(6)` 截断、plot 与 pandas≥1 / 任何 matplotlib 不兼容），本文补丁是最小可跑修复，不是官方修复。
- 本机只验证了 Galileo 单频 SPP → 出图一条链；**未跑** RTK（`-b`）、GPS/混合样例、SBF→RINEX（需 Septentrio `sbf2rin`）、`pyftposnav.py`（CDDIS FTP 已停，本机 425）、gLAB 部分。
- 精度完全取决于 `rnx2rtkp`；脚本只做投影、统计、出图。要厘米级请直接用 [rtklib](./rtklib.md) / [rtklib-explorer](./rtklib-explorer.md) 配 RTK/PPP。
- 模板把 `file-staposfile` 也填成了输出 `.pos` 路径（原作如此）；只在 `ant2-postype=posfile` 时才被读取，本次单点模式无影响。

## 8. 交叉链接

- 解算器本体：[rtklib](./rtklib.md) · [rtklib-explorer](./rtklib-explorer.md) · 学习版源码示例：[learning-rtklib](./learning-rtklib.md)
- 真正的 Python 绑定：[pyrtklib](./pyrtklib.md) · [pyrtklib-demo5](./pyrtklib-demo5.md) · 纯 Python 重写：[rtklib-py](./rtklib-py.md)
- RINEX 预检/压缩：[gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [rnxcmp](./rnxcmp.md) · [crx2rnx](./crx2rnx.md)
- Septentrio 数据：[pysbf2](./pysbf2.md) · [sbfparser](./sbfparser.md)；gLAB：[glab-upc](./glab-upc.md)
