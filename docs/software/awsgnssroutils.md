# awsgnssroutils · AWS Open Data GNSS-RO 查询/下载操作手册

目录：[`PROJECTS.json` → `awsgnssroutils`](../../PROJECTS.json) · 上游 <https://github.com/gnss-ro/aws-opendata> · 许可 **BSD** · PyPI **`awsgnssroutils` 1.2.7** · CLI **`rotcol`**（共址；账号门禁）· 本机验证：S3 `--no-sign-request` 列表 + `query` cosmic1/`ucar_calibratedPhase` **2636** → 赤道带滤 3 文件下载 + cosmic2/`ucar_atmosphericRetrieval` 对照（2026-09-24 EDT）

> 岗位：从 **AWS Registry of Open Data**（桶 `s3://gnss-ro-data`）按元数据查询、筛选、下载 GNSS 无线电掩星产品。冲突时：**本机 `rotcol -h` / PyPI README / 上游仓 > 本文**。

## 1. 用途与边界

**做：**

- 查询/筛选/下载 AWS 上多中心（`ucar` / `jpl` / `romsaf` / `eumetsat`）RO 产品
- 三型文件（API 名 = `{center}_{type}`）：
  - **`calibratedPhase`**（L1b）：校准 excess phase / SNR 等时序 → **电离层相关入口**
  - **`refractivityRetrieval`**（L2a）：弯曲角/折射度等
  - **`atmosphericRetrieval`**（L2b）：温压湿大气剖面
- Python：`RODatabaseClient` / `OccList`；共址 CLI：`rotcol`（另需外部账号，见下）

**不做：**

- **没有** CDAAC 文件名 `ionPhs` / `ionPrf`，也 **没有** 电子密度 Ne 剖面产品 → Ne / ionPhs 走 [data-access 掩星 RO](../data-access.md) 的 `data.cosmic` 直链
- **不是** JPL GENESIS COSMIC-1 大气 L2 ASCII 批量器 → [cosmic-crunch](./cosmic-crunch.md)
- **不是** 地基双频 TEC / ROTI / GIM → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionex-gim](./ionex-gim.md)
- `rotcol` 共址链默认要 **Space-Track / Earthdata / EUMETSAT** 账号；**AWS RO 本体开放，不需要 AWS 账号**

一句话：awsgnssroutils = **AWS 开放 RO 元数据门户 + 三型产品下载**（电离层用 `calibratedPhase`；Ne 仍回 CDAAC）。

| 术语 | 含义 |
| --- | --- |
| `calibratedPhase` | L1b 校准 excess phase（变量如 `excessPhase`/`snr`）；**最接近**电离层 excess phase 需求 |
| `refractivityRetrieval` | L2a 折射/弯曲角类反演 |
| `atmosphericRetrieval` | L2b 大气 T/P/水汽；对照 [cosmic-crunch](./cosmic-crunch.md) 的 GENESIS 大气 L2 |
| `ionPhs` / `ionPrf` | CDAAC 电离层 excess phase / Ne；**本包 API 无此文件名** |
| `~/.awsgnssroutilsrc` | `setdefaults` 写入的 metadata/data 根与 `version`（本机 `v1.1`） |
| `rotcol` | 旋转共址 CLI；`awsro` 开放，其它 service **门禁** |

### 开放 vs 门禁（本机实测）

| 路径 | 凭证 | 本机 |
| --- | --- | --- |
| `aws s3 ls --no-sign-request s3://gnss-ro-data/` | **无** | EXIT 0；见 `contributed/` · `dynamo/` |
| `RODatabaseClient.query` / `OccList.download` | **无** AWS 账号 | 元数据+nc 可下 |
| `rotcol setdefaults` → `earthdata` / `eumetsat` / `spacetrack` | 要账号/密钥 | 未跑共址（门禁） |
| `rotcol setdefaults` → `awsro` | 仅本地路径 | 与 `setdefaults(...)` 等价 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install 'awsgnssroutils==1.2.7'
python -c "import importlib.metadata as m; print(m.version('awsgnssroutils'))"
# 期望：1.2.7
rotcol -h | head -5
# 期望：usage: rotcol [-h] {setdefaults,execute} ...
```

依赖会拉 `boto3` / `awscli` / `netcdf4` / `xarray` 等（pip 自动）。Python **≥3.9**。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `rotcol: command not found` | venv 未激活 | `source .venv/bin/activate` |
| 查询极慢 | 元数据未缓存 | 固定 `metadata_root`；或 `populate()` 一次（可数分钟） |
| `NoCredentialsError` 类报错 | 误用需签名的 S3 调用 | RO 开放数据用包 API 或 `--no-sign-request` |

## 3. 端到端：setdefaults → query → filter → download（本机真跑）

### 3.1 开放桶一眼

```bash
aws s3 ls --no-sign-request s3://gnss-ro-data/
# 期望含：PRE contributed/ · PRE dynamo/ · index.html
aws s3 ls --no-sign-request s3://gnss-ro-data/contributed/v1.1/ucar/cosmic1/
# 期望：atmosphericRetrieval/ · calibratedPhase/ · refractivityRetrieval/
```

### 3.2 配置本地根 + 查 cosmic1 一日（含 calibratedPhase）

```bash
mkdir -p ~/iono_ops/ro/{meta,out}
python - <<'PY'
from awsgnssroutils.database import RODatabaseClient, setdefaults
import os
home = os.path.expanduser("~/iono_ops/ro")
setdefaults(metadata_root=f"{home}/meta", data_root=f"{home}/out", version="v1.1")
rodb = RODatabaseClient()
occs = rodb.query(missions="cosmic1",
                  datetimerange=("2010-06-24", "2010-06-25"),
                  availablefiletypes="ucar_calibratedPhase")
print(repr(occs))
print(occs.info("filetype"))
PY
```

**本机结果（2026-09-24 EDT，`awsgnssroutils` 1.2.7；元数据进度条略）：**

```text
Downloading metadata: 100%|██████████| 2/2 ...
Loading metadata: 100%|██████████| 2/2 ...
OccList(2636 items)
{'jpl_atmosphericRetrieval': 1432, 'ucar_calibratedPhase': 2636, 'jpl_refractivityRetrieval': 1432,
 'jpl_calibratedPhase': 1249, 'ucar_refractivityRetrieval': 1874, 'ucar_atmosphericRetrieval': 1841,
 'eumetsat_calibratedPhase': 2061, 'romsaf_atmosphericRetrieval': 1691, 'romsaf_refractivityRetrieval': 1691}
```

要点：`OccList` **没有** `len()`；用 `repr(occs)` 或 `len(occs.values("latitude"))`。`info("filetype")` 在已按 `availablefiletypes` 过滤后仍可能带上同 occultation 的其它中心/类型计数。

### 3.3 滤赤道带 → 下 3 个 calibratedPhase

```bash
python - <<'PY'
from awsgnssroutils.database import RODatabaseClient, setdefaults
import os
from netCDF4 import Dataset
home = os.path.expanduser("~/iono_ops/ro")
setdefaults(metadata_root=f"{home}/meta", data_root=f"{home}/out", version="v1.1")
rodb = RODatabaseClient()
occs = rodb.query(missions="cosmic1",
                  datetimerange=("2010-06-24", "2010-06-25"),
                  availablefiletypes="ucar_calibratedPhase")
band = occs.filter(latituderange=(-10, 10), longituderange=(-180, 180))
sub = band[0:3]
print(repr(band), repr(sub))
print("lats", [float(x) for x in sub.values("latitude")])
paths = sub.download("ucar_calibratedPhase", data_root=f"{home}/out", keep_aws_structure=False)
for p in paths:
    print(os.path.basename(p), os.path.getsize(p))
ds = Dataset(paths[0])
print("dims", {k: len(v) for k, v in ds.dimensions.items()})
print("vars", list(ds.variables.keys()))
ds.close()
PY
```

**本机 stdout（截断进度条）：**

```text
OccList(165 items) OccList(3 items)
lats [4.107458010773411, -5.936207479695009, 3.6341669104420853]
Downloading ucar_calibratedPhase: 100%|██████████| 3/3 ...
calibratedPhase_cosmic1_ucar_2021.0390_cosmic1c4-G22-201006240737.nc 870474
calibratedPhase_cosmic1_ucar_2021.0390_cosmic1c4-G22-201006241330.nc 900874
calibratedPhase_cosmic1_ucar_2021.0390_cosmic1c2-G25-201006241354.nc 1326474
dims {'time': 5599, 'obscode': 3, 'xyz': 3, 'signal': 3}
vars ['startTime', 'endTime', 'navBitsPresent', 'snrCode', 'phaseCode', 'carrierFrequency',
      'time', 'snr', 'excessPhase', 'rangeModel', 'phaseModel', 'positionLEO', 'positionGNSS']
```

### 3.4 对照：cosmic2 同窗可能只有大气产品

```bash
python - <<'PY'
from awsgnssroutils.database import RODatabaseClient, setdefaults
import os
home = os.path.expanduser("~/iono_ops/ro")
setdefaults(metadata_root=f"{home}/meta", data_root=f"{home}/out", version="v1.1")
rodb = RODatabaseClient()
# data-access 示例日：本机仅大气
occs = rodb.query(missions="cosmic2", datetimerange=("2021-02-18", "2021-02-19"))
print(repr(occs), occs.info("filetype"))
# 若误筛 calibratedPhase → OccList(0 items)
print(repr(rodb.query(missions="cosmic2", datetimerange=("2021-02-18", "2021-02-19"),
                      availablefiletypes="ucar_calibratedPhase")))
paths = occs[0:1].download("ucar_atmosphericRetrieval",
                           data_root=f"{home}/out_atm", keep_aws_structure=False)
print(paths[0])
from netCDF4 import Dataset
ds = Dataset(paths[0]); print(list(ds.variables.keys())); ds.close()
PY
```

**本机结果：**

```text
OccList(3582 items) {'ucar_atmosphericRetrieval': 3369}
OccList(0 items)
.../atmosphericRetrieval_cosmic2_ucar_0001.0001_cosmic2e2-R18-202102180024.nc
['refTime', 'refLongitude', 'refLatitude', 'altitude', 'geopotential', 'refractivity',
 'pressure', 'temperature', 'waterVaporPressure', 'quality', 'superRefractionAltitude', 'setting']
```

（该 atm 文件本机 **35021** bytes；变量全是大气量，无 `excessPhase` / Ne。）

## 4. I/O 字段

| 路径 / 字段 | 含义 |
| --- | --- |
| `~/.awsgnssroutilsrc` | JSON：`metadata_root` · `data_root` · `version` |
| `metadata_root/v1.1/<mission>_YYYY-MM-DD.json` | 日元数据缓存（本机 cosmic2 日文件约 MB 级） |
| `{center}_calibratedPhase` `.nc` | L1b；关键变量 **`excessPhase`** `(time, signal)` · **`snr`** |
| `{center}_atmosphericRetrieval` `.nc` | L2b；`temperature` / `pressure` / `waterVaporPressure` / `refractivity` |
| `{center}_refractivityRetrieval` `.nc` | L2a 折射类（本机未下文件，仅见 `info` 计数） |
| 全局属性例 | `file_type` · `processing_center` · `mission` · `leo` · `occGnss` |
| CDAAC `ionPhs`/`ionPrf` | **不在**本 API；见 [data-access](../data-access.md) |

## 5. 参数（常用）

| API / 旗标 | 作用 | 本机注意 |
| --- | --- | --- |
| `setdefaults(..., version="v1.1")` | 元数据/数据根 | 当前开放数据主用 v1.1 |
| `query(missions=..., datetimerange=...)` | 建 OccList | ISO 日期字符串；窗勿过大 |
| `availablefiletypes=` | 查询时按类型筛 | 无货 → `OccList(0 items)`（见 cosmic2） |
| `filter(latituderange=..., ...)` | 再筛 | 亦支持 transmitter/receiver/geometry/localtime |
| `occs[i:j]` | 切片 | 无 `len()`；冒烟先切 1–3 |
| `download(filetype, keep_aws_structure=False)` | 下载 | `False` 扁平落到 `data_root` |
| `info("filetype"\|"mission"\|...)` | 汇总 | filetype 值为计数 dict |
| `values("latitude")` 等 | numpy 掩码数组 | 可 `len(...)` 当条数 |
| `rotcol setdefaults` / `execute` | 共址 | 非 awsro 服务要账号；本手册未跑 |

完整：`rotcol -h` · `rotcol setdefaults -h` · `rotcol execute -h` · 上游 PyPI README。

## 6. 接到哪步

1. **电离层 excess phase（AWS）**：本手册 `calibratedPhase` → 自写双频/差分 excess phase 分析；**不要**指望包内有 Ne。
2. **电离层 Ne / CDAAC ionPhs·ionPrf**：停——[data-access 掩星 RO](../data-access.md) `data.cosmic` 直链（或后续 pysatCDAAC 类工具）。
3. **大气 RO 剖面（AWS）**：`atmosphericRetrieval` / `refractivityRetrieval`；与 [cosmic-crunch](./cosmic-crunch.md)（GENESIS ASCII→netCDF）**同源任务不同发布链**，勿无 QC 硬拼。
4. **RO↔红外/微波共址**：`rotcol`（先 `setdefaults` 齐账号）→ 输出 NetCDF；本机未实跑。
5. **地基 TEC 主链**：与本包无关 → 路径 A。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 当 ionPrf / Ne 用 | AWS 三型无名 Ne | 看变量表；Ne 走 CDAAC |
| 2 | `availablefiletypes=...Phase` → 0 items | 该任务日未贡献该型 | 先无滤 `info("filetype")` |
| 3 | `len(occs)` TypeError | OccList 无 `__len__` | `repr` 或 `len(values(...))` |
| 4 | 把 cosmic-crunch L2 当 AWS 同文件 | GENESIS ≠ AWS netCDF | 分列手册；对照元数据 |
| 5 | data-access 示例日无 Phase | cosmic2 `2021-02-18` 本机仅 atm | 换有 `calibratedPhase` 的窗（如 cosmic1 2010-06-24） |
| 6 | 查询每次很慢 | 清了 meta 或根路径漂 | 固定 `metadata_root`；勿乱删 JSON |
| 7 | `rotcol execute` 失败 | Earthdata/EUMETSAT/Space-Track 未设 | 只跑 AWS 下载可不管；共址再 `setdefaults` |
| 8 | 裸下全日无切片 | 文件海量（本机一日 Phase 两千+） | 先 `filter` + `[0:3]` 冒烟 |
| 9 | 与 `atmosphericRetrieval` 比相位 | 大气产品无 `excessPhase` | 看 `vars`；产品层级不同 |
| 10 | registry.opendata.aws 深链 404 | 门户链易变 | 用包 API 或 `s3://gnss-ro-data/` |

## 8. 选型

| 你要… | 打开 |
| --- | --- |
| AWS 批量查/下 RO（含 **calibratedPhase**） | **本手册 awsgnssroutils** |
| CDAAC **ionPhs / ionPrf** 直链 | [data-access RO](../data-access.md) |
| GENESIS COSMIC-1 **大气** L2 ASCII→netCDF | [cosmic-crunch](./cosmic-crunch.md) |
| 地基校准 TEC | [pytecgg](./pytecgg.md) |
| RO↔辐射仪共址 | `rotcol`（账号齐全后） |

相关：[data-access](../data-access.md) · [cosmic-crunch](./cosmic-crunch.md) · [README](./README.md) · [`PROJECTS.json`](../../PROJECTS.json)
