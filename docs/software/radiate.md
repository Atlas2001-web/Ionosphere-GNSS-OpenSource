# RADIATE · 对流层射线追踪操作手册

目录：[`PROJECTS.json` → `RADIATE`](../../PROJECTS.json) · 上游 <https://github.com/TUW-VieVS/RADIATE> · tip **`7e81779`**（2025-07-04）· ★**23** · 许可 **GPL-3.0** · 语言 **Fortran** · 本机验证（**2026-09-24 07:19–07:22 EDT**）：`gfortran 14.2.0`；`FUN_TEXT` **55**×`.f90`；`./compile_RADIATE.sh` 多遍 → `radiate` **540976** B；`Version: 2.0_Fortran` / `Sub-version: global_limit`；HTTPS 拉 `gnss.ell` **31110** B/**660** 行、`vlbi.ell` **11308** B/**264** 行；解压 undulation **149402880** B；样例 GRIB **83079619** B×2（`2018010400/06`）；`-createUniAzel` + `smoke.ell`（ABPO/ALIC/BJFS/GRAZ/POTS）→ `2018010400_UNI.radiate` **20350** B/**60** 观测 / `.trp` **17878** B；墙时 **9.484** s；ABPO ZTD=**2.1061** m（ZHD **1.9235**/ZWD **0.1826**）STD@5°=**21.4995** m/@30°=**4.1986** m；sha₁₂ `.radiate`=`64608d6510b8` / `.trp`=`b5d98fa30ca9`

> 岗位：用 **NWM 格网**做微波/光学射线追踪，产斜路径与天顶干/湿延迟及映射因子（VLBI/GNSS/SLR/DORIS）。冲突时：**仓内 README / `FUN_TEXT/RADIATE_readme.txt` / 本机 stdout > 本文**。  
> GNSS-IR 反演 → [gnssrefl](./gnssrefl.md)；多路径前向 → [mpsim](./mpsim.md)；精密 PPP → [pride-pppar](./pride-pppar.md)；网解/对流层模块生态 → [groops](./groops.md)；定位 CLI → [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 编译 `FUN_TEXT/radiate`；读 `DATA/GRIB/*.txt`（1°×1°、25 层 Z/Q/T）+ azel 或 `-createUniAzel`
- 输出 `RESULTS/RADIATE/*.radiate` 与可选 `RESULTS/TRP/*.trp`（斜/天顶延迟、映射因子）
- 垂向插值 `-profilewise`（默认）/`-gridwise`；射线 `-pwl`（Fortran 主路径）；`-microwave` / `-optical`（532 nm）
- 站坐标：`vlbi.ell` / `gnss.ell` / `slr.ell` / `doris.ell` / 格网点文件（门户下载）

**不做 / 本机限制：**

- **不是** GNSS-IR / 多路径 SNR 产线 → [gnssrefl](./gnssrefl.md) / [mpsim](./mpsim.md)
- **不是** PPP/RTK 引擎 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 官方 VMF/GPT 映射函数源码门户本身（VMF 站坐标/产品另见 `vmf.geo.tuwien.ac.at`）
- `.grib` 二进制与 ECMWF 拉取脚本**不**随仓；须自备已转好的文本 NWM（样例仅两历元）
- 仓内 `azel_18SEP21XU`（2018 DOY **264**）与样例 GRIB（**20180104**）**日期不一致**；VLBI 样例本机在 epolog 文件名空格处曾中断——冒烟改走 `-createUniAzel` 对齐 GRIB 日

一句话：RADIATE = **VieVS Fortran 射线追踪器**（NWM→斜/天顶延迟）；数据整形与站录自备。

| 术语 | 含义 |
| --- | --- |
| NWM / GRIB 文本 | `DATA/GRIB/` 下全球 1° 格网；头含 lat/lon/层/参数/时刻 |
| azel | 每观测一行：扫描号、MJD、站、方位/仰角 [rad]… |
| `-createUniAzel` | 按 `DATA/INPUT/AZEL_spec.txt` 内生均匀方位–仰角，不读实体 azel |
| `.radiate` / `.trp` | 全字段射线结果 / TROPO_PATH_DELAY 交换格式 |
| `smoke.ell` | 本机缩站表（冒烟用；非上游文件名） |

## 2. vs gnssrefl / mpsim / pride-pppar / groops

| | **本文 RADIATE** | [gnssrefl](./gnssrefl.md) | [mpsim](./mpsim.md) | [pride-pppar](./pride-pppar.md) | [groops](./groops.md) |
| --- | --- | --- | --- | --- | --- |
| 角色 | NWM 射线追踪 | SNR→RH | 多路径前向 | PPP-AR | 重力+GNSS XML |
| 输入 | GRIB 文本+azel/站 | RINEX/SNR | sett | OBS+产品 | XML+产品 |
| 输出 | ZTD/STD/映射 | RH 表 | SNR/误差 | `.pos`/AR | 轨道/钟/网解 |
| 本机 | 编译+60 观测 | mchl 实跑 | Octave/MATLAB | 3.2.11 | Sp3 实跑 |

## 3. 安装

```bash
sudo apt-get install -y gfortran unzip curl   # 本机 gfortran 14.2.0
git clone https://github.com/TUW-VieVS/RADIATE.git
cd RADIATE && git rev-parse --short HEAD      # 7e81779

# 必做：解压最细 undulation（勿提交解压结果）
cd DATA/UNDULATIONS
unzip -o global_undulations_dint_lat0.125_dint_lon0.125.txt.zip
# → 149402880 B

# 站坐标（须 https；http 会 301 成 HTML）
mkdir -p ../STATIONS
curl -fsSL -o ../STATIONS/gnss.ell https://vmf.geo.tuwien.ac.at/station_coord_files/gnss.ell
curl -fsSL -o ../STATIONS/vlbi.ell https://vmf.geo.tuwien.ac.at/station_coord_files/vlbi.ell

cd ../../FUN_TEXT
# 首次常因 .mod 依赖失败；README：rm *.mod 后至少跑两遍
rm -f *.mod radiate
./compile_RADIATE.sh    # 内含两次 gfortran -ffree-line-length-none -O3 -o radiate *.f90
# 若仍无二进制：再跑 1–2 遍，或循环至出现 radiate
ls -la radiate           # 本机 540976 B
./radiate                # 无参 → 提示缺 AZEL/站文件
```

校内镜像（GEO 域）：`https://git.geo.tuwien.ac.at/vievs/RADIATE/RADIATE.git`（公开以 GitHub 为准）。

## 4. 端到端（本机 · 对齐样例 GRIB 的 createUniAzel）

```bash
cd /path/to/RADIATE
# 样例 NWM 提到工作目录（无子目录）
cp -n DATA/GRIB/sample/201801040*.txt DATA/GRIB/

# AZEL_spec：日期必须能匹配 GRIB 文件名时刻
cat > DATA/INPUT/AZEL_spec.txt <<'EOF'
# start / end / epochs_per_day / n_azimuth / elevations(deg)
2018/01/04
2018/01/04
2
4
5 15 30
EOF

# 缩站（全量 gnss.ell≈660 站 × 方位×仰角会很慢）
printf '%s\n' \
  'ABPO    -19.0183    47.2292  1553.00  33302' \
  'ALIC    -23.6701   133.8855   603.40  50137' \
  'BJFS     39.6086   115.8925    87.40  21601' \
  'GRAZ     47.0671    15.4935   538.30  11001M002' \
  'POTS     52.3793    13.0661   144.40  14106' \
  > DATA/STATIONS/smoke.ell

cd FUN_TEXT
./radiate azel_2018010400_UNI.txt smoke.ell -createUniAzel -one_epoch_per_obs
```

**本机结果（2026-09-24 07:21–07:22 EDT）：**

```text
Version: 2.0_Fortran / Sub-version: global_limit
Session: 2018010400_UNI
Stations: ABPO ALIC BJFS GRAZ POTS × 4 az × 3 elev = 60 obs
Ray-tracing … Finished!  Total elapsed … 9.484 s
RESULTS/RADIATE/2018010400_UNI.radiate  20350 B / 60 obs
RESULTS/TRP/2018010400_UNI.trp          17878 B
No .err-file (no errors)
ABPO: ZTD=2.1061  ZHD=1.9235  ZWD=0.1826  STD@5°=21.4995  STD@30°=4.1986
ALIC: ZTD=2.2298  ZHD=2.1623  ZWD=0.0674  STD@5°=22.5871  STD@30°=4.4435
GRAZ: ZTD=2.2040  ZHD=2.1594  ZWD=0.0445  STD@5°=22.4151  STD@30°=4.3920
```

`.radiate` 关键字段（节选）：ztd/zhd/zwd、std/shd/swd、站仰角、几何弯曲、总/干/湿映射因子；站气象列在 createUniAzel 下可为 `NaN`（延迟来自 NWM 插值列）。

### 4.1 读实体 azel（生产主路径）

```bash
# azel → DATA/AZEL/（无子目录）；NWM 历元须盖住观测时刻
./radiate azel_YYYYMMDDhh_UNI.txt gnss.ell -profilewise -pwl -microwave -trp
# 多会话：编辑/运行 FUN_TEXT/run_multiple_sessions.sh
```

本机对 `azel_18SEP21XU.txt`：能建 `epolog2_18SEP21XU     _20180921*.txt`，随后 `Problem with opening epolog-file`（会话名空格填充与打开路径不一致）；且无 20180921 GRIB → **未**对该 VLBI 会话臆造延迟。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `DATA/GRIB/*.txt` | 全球 1°、25 层；样例各 **83079619** B |
| `DATA/AZEL/*.txt` 或 `AZEL_spec.txt` | 观测几何；方位/仰角为 **rad**（spec 里仰角为 **度**） |
| `DATA/STATIONS/*.ell` | 椭球纬经高；门户 `station_coord_files/` |
| `DATA/UNDULATIONS/…0.125…txt` | 大地水准差距；须先 unzip |

| 输出 | 说明 |
| --- | --- |
| `RESULTS/RADIATE/<session>.radiate` | 主结果（本机 60 行数据） |
| `RESULTS/TRP/<session>.trp` | 交换格式（`-trp` 默认开） |
| `DATA/ERROR_LOG/*.err` | 有错才写；本机冒烟无 |
| `DATA/EPOLOG*` / `SESSION_INDEX*` | 中间文件；`-cleanup` 可清 |

## 6. 参数速查

| 旗标 | 默认/本机 | 备注 |
| --- | --- | --- |
| 位置参数 1–2 | azel 名 + 站文件名 | **必填**；相对 `FUN_TEXT/` 解析到 `../DATA/…` |
| `-profilewise` / `-gridwise` | profilewise | 垂向插值策略 |
| `-pwl` | 默认 | Fortran 实现；`-ref_pwl`/`-Thayer` 仅 MATLAB 版 |
| `-microwave` / `-optical` | microwave | 光学波长 532 nm |
| `-one_epoch_per_obs` / `-two_epochs_per_obs` | two | two 更准、约 2× 时 |
| `-trp` / `-notrp` | trp | 是否写 `.trp` |
| `-readAzel` / `-createUniAzel` | readAzel | 均匀网格教学/冒烟用后者 |
| `-cleanup` | 默认 nocleanup | 清 epolog/index |

## 7. 接到哪步

1. 延迟产品进 PPP/网解先验 → [pride-pppar](./pride-pppar.md) / [groops](./groops.md)（导入方式自定）  
2. 只需站坐标级定位 → [rtklib](./rtklib.md)；反射测高 → [gnssrefl](./gnssrefl.md)  
3. 多路径机理对照 → [mpsim](./mpsim.md)  
4. NWM/产品礼仪 → [data-access](../data-access.md)；VMF 门户 `https://vmf.geo.tuwien.ac.at/`

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 首遍 `Cannot open module file …mod` | `*.f90` 无序一次链 | `rm *.mod`；`compile_RADIATE.sh` **≥2** 遍 |
| 2 | `scl enable devtoolset-4` 挂起 | 旧 CentOS 行未注释 | 脚本里已注释；勿开 |
| 3 | 站文件变成 HTML | `http://` 301 | 改用 **`https://vmf.geo.tuwien.ac.at/...`** |
| 4 | undulation 缺失/体积不对 | 未 unzip 0.125° | `unzip -o …0.125….zip`（约 **149** MB） |
| 5 | 运行极慢或内存炸 | 全 `gnss.ell` + 密方位/仰角 | 缩站表；减 `AZEL_spec` 方位/仰角数 |
| 6 | 无延迟 / 找不到 GRIB | 观测日 ≠ `DATA/GRIB/` 文件名日 | 自备对齐文本 NWM；勿混用 01-04 样例与 09-21 azel |
| 7 | `Problem with opening epolog-file` | 会话名空格填充与打开路径 | 换短会话名；或走 `-createUniAzel`；查 `EPOLOG2/` 实名 |
| 8 | 把样例 GRIB 当任意日通用场 | 仅 20180104 两时次 | 业务日须自转 ECMWF→文本（README 承认此为最大门槛） |
| 9 | azel 仰角单位混用 | 实体 azel=**rad**，spec=**deg** | 对照样例；`0.087…`≈5° |
| 10 | `-ref_pwl` 无效 | Fortran 未实现 | 只用 `-pwl` 或 MATLAB 版 |
| 11 | 行被截断编译错 | 无 `-ffree-line-length-none` | 用仓内 `compile_RADIATE.sh` |
| 12 | 把 `.radiate` 当 RINEX | 格式是 VieVS 射线结果 | 定位仍用 [rtklib](./rtklib.md)；延迟作对流层输入 |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| NWM 射线追踪 / 斜路径延迟研究 | **本文 RADIATE** |
| GNSS-IR 水位/雪深 | [gnssrefl](./gnssrefl.md) |
| 多路径 SNR 前向 | [mpsim](./mpsim.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| 重力场+GNSS 网解 XML | [groops](./groops.md) |
| 日常 RTK/PPP CLI | [rtklib](./rtklib.md) |

## 10. 相关

[gnssrefl](./gnssrefl.md) · [mpsim](./mpsim.md) · [pride-pppar](./pride-pppar.md) · [groops](./groops.md) · [rtklib](./rtklib.md) · [data-access](../data-access.md) · [README](./README.md)
