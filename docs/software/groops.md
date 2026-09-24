# GROOPS · TU Graz 重力场 + GNSS 处理操作手册

目录：[`PROJECTS.json` → `groops`](../../PROJECTS.json) · 上游 <https://github.com/groops-devs/groops> · 文档 <https://groops-devs.github.io/groops/html/index.html> · 数据 <https://ftp.tugraz.at/pub/ITSG/groops> · 许可 **GPL-3.0** · tip **`7e1bd6d`** / 发布标签 **2025-11-15** · 本机验证：CMake Release 编装 `bin/groops`（Compiled: Sep 24 2026 05:25:48）；`scenarioGnssPPP` 上 **Sp3Format2Orbit** G01 → **289** 历元 / 300 s / gaps=0；**OrbitAddVelocityAndAcceleration** 同窗；**GnssClockRinex2InstrumentClock** 写出 `*.G01.G01.dat`；样例 CRX→RNX + georinex GRAZ **2880** 历元 / **30** GPS · **未**跑全日 `02groopsGnssProcessing`（缺完整 `groopsDataDir`，`data.zip`≈23 G）· 2026-09-24 05:27 EDT

> 岗位：大地测量向 **GNSS 网解 / PPP / POD / 重力场恢复**（XML 程序链 + 可选 GUI/MPI）。冲突时：**本机 `groops --help` / 官方 cookbook / `INSTALL.md` > 本文**。轻量 CLI → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；GA YAML → [ginan](./ginan.md)。

## 1. 用途与边界

**做：**

- 站网 GNSS 处理、精密轨道/钟差/偏差、地面站 **PPP**（`GnssProcessing`）
- LEO 运动学/约化动力定轨；GRACE 重力场；仪器时序与绘图（GMT）
- XML 配置；`groopsGui`（Qt）；可选 MPI 并行

**不做：**

- **不是** 开箱单文件 `rnx2rtkp` 替代 → [rtklib](./rtklib.md)
- **不是** 武大 GREAT XML 滤波 PVT → [great-pvt](./great-pvt.md)
- **不是** STEC/ROTI 产品链 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- 本机冒烟为 **SP3/CLK 转换 + 样例 OBS 探活**；正式 PPP 需本地 `groopsDataDir`

一句话：GROOPS = **ITSG/TU Graz 开源大地测量工具箱（重力 + GNSS）**。

| 术语 | 含义 |
| --- | --- |
| `groops` | CLI；读一个或多个 `*.xml` |
| `groopsDataDir` | 全局变量：EOP/潮汐/VMF/天线/发射机元数据根 |
| `Sp3Format2Orbit` | SP3 → GROOPS 轨道仪器文件 |
| `scenarioGnssPPP.zip` | 官方 GRAZ PPP 教学场景（≈89 MB） |

## 2. 安装

### 2.1 Ubuntu/Debian（本机采用）

```bash
sudo apt-get install -y g++ gfortran cmake libexpat1-dev libopenblas-dev
# 可选：libnetcdf-dev liberfa-dev mpi-default-dev qtbase5-dev gmt gmt-gshhg
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/groops-devs/groops.git
cd groops && git rev-parse --short HEAD   # 本机 7e1bd6d
mkdir -p source/build && cd source/build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$HOME/iono_ops/groops \
  -DDISABLE_NETCDF=TRUE   # 无 netCDF 包时
make -j$(nproc) && make install
export PATH="$HOME/iono_ops/groops/bin:$PATH"
groops --help | head -n 20
```

**本机结果：** Usage 含 `--log` / `--global` / `--xsd` / `--doc`；头行含 Compiled 时间戳。

### 2.2 数据目录（正式 PPP 必需）

```bash
# 全量 ≈23 G —— 勿在无磁盘时强下
# curl -L -o data.zip https://ftp.tugraz.at/pub/ITSG/groops/data.zip
# 或按需拉子树：earthRotation/ gnss/ tides/ troposphere/ loading/ ...
mkdir -p ~/iono_ops/groops-data
# 冒烟至少拉 EOP（≈44 MB）：
curl -L -o ~/iono_ops/groops-data/earthRotation/timeSeries_EOP_rapid_IAU2000_desai.dat \
  https://ftp.tugraz.at/pub/ITSG/groops/data/earthRotation/timeSeries_EOP_rapid_IAU2000_desai.dat
```

### 2.3 GUI（可选）

```bash
sudo apt-get install -y qtbase5-dev
cd ~/iono_ops/groops/gui && qmake && make
# 或发布页预编译 Windows GUI
```

## 3. 端到端

### 3.1 官方 scenarioGnssPPP（本机已解压）

```bash
mkdir -p ~/iono_ops/groops-run && cd ~/iono_ops/groops-run
curl -L -o scenarioGnssPPP.zip \
  https://ftp.tugraz.at/pub/ITSG/groops/scenario/scenarioGnssPPP.zip
unzip -qo scenarioGnssPPP.zip
cat scenarioGnssPPP/README.txt
# 改各 XML 中 groopsDataDir → 本机路径后再：
# groops 01groopsConvert.xml
# groops 02groopsGnssProcessing.xml
# groops 03groopsPlots.xml   # 需 GMT
```

场景含 GRAZ 2020-01-01/02 CRX、TUG repro3 SP3/CLK/OBX/BIA；脚本：`01` 转换 → `02` PPP → `03` 图。cookbook：<https://groops-devs.github.io/groops/html/cookbook.gnssPpp.html>。

### 3.2 本机真跑：SP3 → 轨道（+ 速度）

```bash
# 最小 XML（路径按本机改）
cat > /tmp/sp3_G01.xml <<'XML'
<?xml version="1.0" encoding="UTF-8" ?>
<groops>
  <global>
    <filename label="groopsDataDir">/path/to/groops-data</filename>
  </global>
  <program>
    <Sp3Format2Orbit>
      <outputfileOrbit>/tmp/orbit_2020-01-01.G01.dat</outputfileOrbit>
      <satelliteIdentifier>G01</satelliteIdentifier>
      <earthRotation>
        <file>
          <inputfileEOP>{groopsDataDir}/earthRotation/timeSeries_EOP_rapid_IAU2000_desai.dat</inputfileEOP>
          <interpolationDegree>3</interpolationDegree>
        </file>
      </earthRotation>
      <inputfile>.../scenarioGnssPPP/igs/TUG0R03FIN_20200010000_01D_05M_ORB.SP3.gz</inputfile>
    </Sp3Format2Orbit>
  </program>
</groops>
XML
groops -l /tmp/sp3.log /tmp/sp3_G01.xml
```

**本机结果（`7e1bd6d`，2026-09-24 05:26 EDT）：**

```text
--- Sp3Format2Orbit ---
read ... TUG0R03FIN_20200010000_01D_05M_ORB.SP3.gz
  time start: 2020-01-01_00-00-00
  time end:   2020-01-02_00-00-00
  epochs: 289   median sampling: 300 seconds   gaps: 0
--- OrbitAddVelocityAndAcceleration ---  epochs: 289  gaps: 0
--- GnssClockRinex2InstrumentClock ---
  Write clocks .../clock_2020-01-01.G01.G01.dat   # 注意 identifier 会拼进文件名
```

### 3.3 样例观测探活（本机 · crx2rnx + georinex）

```bash
cd scenarioGnssPPP/igs
gunzip -k -f GRAZ00AUT_R_20200010000_01D_30S_MO.crx.gz
crx2rnx GRAZ00AUT_R_20200010000_01D_30S_MO.crx \
  -o GRAZ00AUT_R_20200010000_01D_30S_MO.rnx
python3 - <<'PY'
import georinex as gr, numpy as np
p='GRAZ00AUT_R_20200010000_01D_30S_MO.rnx'
x=gr.load(p, tlim=('2020-01-01T00:00:00','2020-01-01T01:00:00'), use='G')
y=gr.load(p, use='G', meas=['C1C'])
print('1h', len(x.time), 'sv', list(x.sv.values)[:5], '...')
print('day', len(y.time), 'sv', len(y.sv))
s=x['C1C'].sel(sv='G07').values
print('G07 C1C', float(s[np.isfinite(s)][0]))
PY
```

**本机结果：** 1 h **121** 历元 / 11 GPS；全日 **2880** / **30** GPS；G07 C1C 首值 **25383647.774** m。

| 输入 | 说明 |
| --- | --- |
| `TUG0R03FIN_*_ORB.SP3.gz` | TUG repro3 精密轨道 |
| `TUG0R03FIN_*_CLK.CLK.gz` | 精密钟差 |
| `GRAZ00AUT_*_MO.crx.gz` | GRAZ 30 s 观测 |
| EOP `timeSeries_EOP_rapid_IAU2000_desai.dat` | 地自转 |

| 输出 | 含义 |
| --- | --- |
| `orbit_*.G01.dat` | GROOPS 轨道仪器（本机 25 KB） |
| `clock_*.dat` | 仪器钟差（路径常再拼 `{identifier}`） |
| `02` PPP 产物 | 坐标/残差/对流层等（需完整 dataDir） |

## 4. 关键参数

| 项 | 作用 |
| --- | --- |
| `groops cfg.xml` | 跑配置（可多个） |
| `--global name=value` | 覆盖/追加全局变量（如 `timeStart`） |
| `--xsd out.xsd` | 导出完整配置 schema（本机 ≈1.1 MB） |
| `--log file` | 追加日志；目录则按脚本分文件 |
| `--silent` | 安静模式 |
| `DISABLE_NETCDF` 等 | CMake 关掉外部源（见 `INSTALL.md`） |
| `OPENBLAS_NUM_THREADS=1` | 与 MPI 同开时建议钉 1 |

## 5. 接到哪步

- 教学/冒烟 PPP → [rtklib](./rtklib.md)；发表级 AR → [pride-pppar](./pride-pppar.md)；武大滤波 → [great-pvt](./great-pvt.md)；GA → [ginan](./ginan.md)
- CRX/探活 → [crx2rnx](./crx2rnx.md) / [georinex](./georinex.md)；产品下载 → [data-access](../data-access.md)
- 工作流 **D**：QC →（可选本文网解/PPP）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `must contain 'inputfileEOP'` / 找不到元数据 | `groopsDataDir` 仍是 `/itsg/...` | 改全局或 `--global groopsDataDir=$HOME/iono_ops/groops-data` |
| 2 | convert/PPP 立刻报缺 VMF/潮汐/天线 | 未下完整 data | 按 cookbook 拉子树；或接受仅做 SP3/CLK 冒烟 |
| 3 | `netCDF library *NOT* found` | 未装 libnetcdf | `apt install libnetcdf-dev` 重 cmake；或不跑 grd 转换 |
| 4 | MPI 版未生成 | 缺 mpi-cxx | `apt install mpi-default-dev`；或用单进程 `groops` |
| 5 | 钟差文件名变 `*.G01.G01.dat` | `identifier` 拼进输出模板 | 输出路径勿再手工加 `.G01`；或接受双后缀 |
| 6 | `must contain 'intervals'`（钟差） | 新接口必填时段 | 抄场景 XML 的 `<intervals><uniformInterval>…` |
| 7 | 把 289 历元 SP3 转换当 PPP 坐标 | 未跑 `GnssProcessing` | 备齐 dataDir 后跑 `02groopsGnssProcessing.xml` |
| 8 | 图脚本失败 | 未装 GMT | `apt install gmt gmt-gshhg` |
| 9 | 与 [pride-pppar](./pride-pppar.md) 坐标差大 | 产品/模型/参数化不同 | 同 SP3/CLK/ATX 再比；读 cookbook 参数 |
| 10 | 期望直接出 STEC 产品 | 软件是测地处理 | TEC→[pytecgg](./pytecgg.md)；GROOPS 可估 STEC 约束但非发表 TEC 链 |
| 11 | `data.zip` 下不动 / 盘满 | ≈23 G | 只同步场景需要的目录 |
| 12 | OpenBLAS + MPI 变慢 | 线程争用 | `export OPENBLAS_NUM_THREADS=1` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 重力场 + 网解/PPP 科研栈（XML） | **本文 GROOPS** |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| 武大 GREAT 滤波 PVT | [great-pvt](./great-pvt.md) |
| GA pea/YAML | [ginan](./ginan.md) |
| 轻量 CLI RTK/PPP | [rtklib](./rtklib.md) |
| MATLAB GUI PPP | [rapppid](./rapppid.md) |

## 8. 相关

[pride-pppar](./pride-pppar.md) · [ginan](./ginan.md) · [rtklib](./rtklib.md) · [great-pvt](./great-pvt.md) · [rapppid](./rapppid.md) · [crx2rnx](./crx2rnx.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · [README](./README.md)

- 论文：Mayer-Guerr et al., 2021, *Computers & Geosciences*（DOI 10.1016/j.cageo.2021.104864）
- cookbook PPP / Network：官方 html 文档
