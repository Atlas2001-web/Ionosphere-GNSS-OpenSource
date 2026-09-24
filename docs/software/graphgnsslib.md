# GraphGNSSLib · FGO 风格 GNSS/RTK 操作手册

目录：[`PROJECTS.json` → `GraphGNSSLib`](../../PROJECTS.json) · 上游 <https://github.com/weisongwen/GraphGNSSLib> · 许可 **GPL-3.0** · tip **`d861802`**（2022-12-29）· 捆 **RTKLIB 2.4.3 b33** + **Ceres** · 本机验证：仓内 TST 数据 **georinex** 可读；同数据 **rnx2rtkp** SPP 5 min **251** 历元 Q=5、RTK 浮点窗约 **24**×Q=2；**无 ROS/无 Docker → 未跑 FGO 节点** · 2026-09-24 05:17 EDT

> 岗位：伪距/多普勒（及 RTK 双差相位）进 **因子图（FGO）** 事后定位，对照 WLS/EKF。冲突时：**仓内 README / launch / 本机 `roslaunch` > 本文**。经典 RTK/PPP → [rtklib](./rtklib.md)；Python NavData/WLS → [gnss_lib_py](./gnss_lib_py.md)。

## 1. 用途与边界

**做：**

- **GNSS Positioning（FGO）**：伪距+多普勒；`RTK_FGO=0`
- **GNSS-RTK（FGO 浮点）**：双差伪距/相位+多普勒；LAMBDA **逐历元**；`RTK_FGO=1`
- 内嵌 RTKLIB 读 RINEX → ROS topic → Ceres；CSV 轨迹
- 自带香港 TST 动/静示例 + `groundTruth_TST.csv`

**不做：**

- **不是** 无 ROS 的 CLI PPP → [rtklib](./rtklib.md) / [ginan](./ginan.md) / [pride-pppar](./pride-pppar.md) / [great-pvt](./great-pvt.md)
- **不是** 生产 CORS / 全弧固定主力（README：float + 逐历元 LAMBDA）
- **不是** LEO 扩展（见 GraphGNSSLib_LEO）
- 本机 **无 ROS Kinetic/Melodic、无 Docker** → FGO 未编译；§3.1–3.2 为可复现冒烟

一句话：GraphGNSSLib = **ROS+Ceres 上的 GNSS/RTK 因子图研究包**。

| 术语 | 含义 |
| --- | --- |
| FGO | Factor Graph Optimization（Ceres） |
| `RTK_FGO` | `global_fusion/RTKLIB/src/rtklib.h`：0 定位 / 1 RTK |
| `psr_doppler_fusion` | 伪距+多普勒 FGO launch |
| `psr_doppler_car_rtk` | RTK-FGO launch |

## 2. 安装

### 2.1 官方环境

上游：**Ubuntu 16.04 + ROS Kinetic**；`docker/` 基于 `ros:kinetic-perception`（Ceres **1.12.0**）。

```bash
sudo apt-get install -y cmake libgoogle-glog-dev libatlas-base-dev \
  libeigen3-dev ros-kinetic-novatel-msgs
mkdir -p ~/GraphGNSSLib/src && cd ~/GraphGNSSLib/src
git clone https://github.com/weisongwen/GraphGNSSLib.git
cd ~/GraphGNSSLib && catkin_make
source ~/GraphGNSSLib/devel/setup.bash && catkin_make
```

Ceres 必须用仓内 `support_files/ceres-solver.tar.gz`，**不要**直接拉最新主线。

### 2.2 Docker（有守护进程时）

```bash
cd ~/GraphGNSSLib/src/GraphGNSSLib/docker
make build    # tag: ros:GraphGNSSLib
```

### 2.3 本机可做核对

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/weisongwen/GraphGNSSLib.git
cd GraphGNSSLib && git rev-parse --short HEAD   # d861802
ls global_fusion/dataset/gps_solution_TST/
grep -n 'RTK_FGO' global_fusion/RTKLIB/src/rtklib.h | head
```

**本机（`d861802`，2026-09-24 05:17 EDT）：** 数据与 launch 齐全；`RTK_FGO` 默认 **0**；无 ROS/Docker → 未 `catkin_make`。

## 3. 端到端

### 3.1 数据探活（本机 · georinex）

```bash
cd ~/iono_ops/GraphGNSSLib
python3 - <<'PY'
import georinex as gr
rover='global_fusion/dataset/gps_solution_TST/COM3_190428_124409.obs'
base='global_fusion/dataset/gps_solution_TST/hksc1180.19o'
for p in (rover, base):
    x=gr.load(p, tlim=('2019-04-28T12:44:00','2019-04-28T12:50:00'), use='G')
    print(p.split('/')[-1], 'epochs', len(x.time), 'sv', len(x.sv))
print('GT', sum(1 for _ in open(
    'global_fusion/dataset/gps_solution_TST/groundTruth_TST.csv')))
PY
```

**本机结果：** 流动站 **326** 历元 / **8** GPS；基准站 **13** 历元 / **11** GPS（30 s）；GT **485** 行。

### 3.2 RTKLIB 基线（本机 · 同文件）

```bash
DS=global_fusion/dataset
rnx2rtkp -p 0 -s 1 -ts 2019/04/28 12:44:00 -te 2019/04/28 12:50:00 \
  $DS/gps_solution_TST/COM3_190428_124409.obs \
  $DS/gps_solution_TST/hksc1180.19n -o /tmp/graphgnss_spp.pos
rnx2rtkp -p 2 -s 1 -ts 2020/06/03 03:02:00 -te 2020/06/03 03:10:00 \
  $DS/gps_solution_TST2/2020_06_03_TST_03.obs \
  $DS/gps_solution_TST2/hksc155d.20o \
  $DS/gps_solution_TST2/hksc155d.20n \
  $DS/gps_solution_TST2/hksc155d.20b -o /tmp/graphgnss_rtk.pos
grep -v '^%' /tmp/graphgnss_spp.pos | awk 'NF>=8' | wc -l
grep -v '^%' /tmp/graphgnss_rtk.pos | awk 'NF>=8{c[$6]++}END{for(k in c)print k,c[k]}'
```

**本机结果：** SPP **251** 历元 Q=**5**，末点约 `22.30460°N 114.18601°E`；RTK 窗约 **24**×Q=**2**（浮点），其余回落单点——城市数据正常，**勿**当固定率。

### 3.3 官方 FGO（需 ROS；本机未跑）

```bash
# 定位：rtklib.h 中 RTK_FGO=0 后编译
source ~/GraphGNSSLib/devel/setup.bash
roslaunch global_fusion dataublox_TST20190428.launch
roslaunch global_fusion psr_doppler_fusion.launch
# CSV：~/GraphGNSSLib/trajectory_psr_dop_fusion.csv

# RTK：#define RTK_FGO 1 → 重编
roslaunch global_fusion dataublox_TST20200603.launch
roslaunch global_fusion psr_doppler_car_rtk.launch
# CSV：~/GraphGNSSLib/FGO_trajectoryllh_pdrtk.csv
```

| 输入 | 说明 |
| --- | --- |
| `COM3_190428_124409.obs` + `hksc1180.19[onb]` | 2019-04-28 动态 |
| `2020_06_03_TST_03.obs` + `hksc155d.20*` | 2020-06-03 静态 RTK |
| `groundTruth_TST.csv` | 周/秒/纬经高 |

| 输出 | 含义 |
| --- | --- |
| `trajectory_psr_dop_fusion.csv` | 定位 FGO |
| `FGO_trajectoryllh_pdrtk.csv` | RTK-FGO LLH |

## 4. 关键参数

| 项 | 作用 |
| --- | --- |
| `RTK_FGO` | 0/1；改后 **必须** `catkin_make` |
| launch `mode` | 0 SPP / 1 DGPS / 2 kinematic |
| launch `nf` | 频率数 |
| Ceres | 钉 1.12.x |
| RViz | 无 GUI 时从 launch 去掉 |

## 5. 接到哪步

- CLI RTK/PPP → [rtklib](./rtklib.md)；精密 PPP-AR → [pride-pppar](./pride-pppar.md) / [great-pvt](./great-pvt.md) / [ginan](./ginan.md)
- Python → [gnss_lib_py](./gnss_lib_py.md)；开放 PPP-RTK → [cssrlib](./cssrlib.md)
- 工作流 **D**：QC →（可选 FGO 对比）→ 发表级链；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 找不到 Ceres | 版本/路径错 | 用 `support_files/ceres-solver.tar.gz` |
| 2 | 改 `RTK_FGO` 无效 | 未重编 | `catkin_make && source devel/setup.bash` |
| 3 | 缺 `novatel_msgs` | 依赖未装 | `apt install ros-$ROS_DISTRO-novatel-msgs` |
| 4 | RViz 拖死会话 | `required="true"` | 无显示时注释 rviz 节点 |
| 5 | CSV 找不到 | 写到 cwd/家目录 | `find ~ -name 'trajectory_psr_dop_fusion.csv'` |
| 6 | 新 Ubuntu 编不过 | 仅测过 Kinetic | 用仓内 Docker / 16.04 |
| 7 | 本机无 ROS/Docker | 共享 CI 常见 | 先跑 §3.1–3.2；FGO 换有 ROS 的机器 |
| 8 | 把逐历元 LAMBDA 当全弧固定 | 算法设定 | 读 README Notes；生产固定→[pride-pppar](./pride-pppar.md) |
| 9 | 与 RTKLIB 轨迹差大 | 窗口/权重不同 | 同数据先 `rnx2rtkp` 再比 |
| 10 | 期望出 STEC | 本仓是定位 | TEC→[pytecgg](./pytecgg.md) |
| 11 | CMake 指向 Melodic | 与 README Kinetic 不一致 | `echo $ROS_DISTRO` 后对齐 |
| 12 | launch 找不到 dataset | clone 不在 catkin `src/` | 按 §2.1 工作空间布局 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| FGO vs WLS/EKF 对照 | **本文 GraphGNSSLib** |
| 日常 RTK/PPP CLI | [rtklib](./rtklib.md) |
| 武大 GREAT 精密 PVT | [great-pvt](./great-pvt.md) |
| Python NavData/WLS | [gnss_lib_py](./gnss_lib_py.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |

## 8. 相关

[rtklib](./rtklib.md) · [gnss_lib_py](./gnss_lib_py.md) · [great-pvt](./great-pvt.md) · [ginan](./ginan.md) · [cssrlib](./cssrlib.md) · [pride-pppar](./pride-pppar.md) · [README](./README.md)

- 论文：Wen & Hsu, ICRA 2021（代码≠论文逐行）
- LEO：GraphGNSSLib_LEO
