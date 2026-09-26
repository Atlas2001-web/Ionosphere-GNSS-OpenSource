# cosmic-crunch · JPL GENESIS COSMIC-1 L2 掩星 ASCII→netCDF4 操作手册

目录：[`PROJECTS.json` → `cosmic-crunch`](../../PROJECTS.json) · 上游 <https://github.com/ErickShepherd/cosmic-crunch> · 许可 **MIT** · PyPI **`cosmic-crunch` 2.1.2** · 本机验证：`get --test` 拉 **10** 个 `.L2.txt.gz` + `convert`/`--netcdf4` 出 **10** 个 `.L2.nc`（2026-09-24 EDT）· **质检复跑**（2026-09-26 00:47 EDT）：PyPI **2.1.2** 仍最新；`get --test` **6.7 s** 拉 **10** 个/合计 **260585** B；单文件+目录 convert 摘要逐字对齐；nlev **417**/NCEP **379**；修 Height 上界 **59.699**（原稿 59.700 是四舍五入误写）；重复 convert **静默覆盖**（Skipped 仍 0）

> 岗位：从 **JPL GENESIS** 批量拉取 COSMIC-1（FORMOSAT-3）**大气** Level-2 ASCII（折射/温压湿），并转成 **netCDF4**。冲突时：**本机 `cosmic-crunch -h` / 上游 README > 本文**。

## 1. 用途与边界

**做：**

- 爬取 `https://genesis.jpl.nasa.gov/ftp/glevels`（可用 `--base-url` / `COSMIC_CRUNCH_BASE_URL` 覆盖）下的 COSMIC **L2/txt** `.L2.txt.gz`
- 就地 / 下载后转 **netCDF4**（组名 `COSMIC1-Profile`、`NCEP_FNL-Profile`）
- CLI：`cosmic-crunch get` · `cosmic-crunch convert`；`--test` 只下小子集冒烟

**不做：**

- **不是** UCAR **CDAAC** `ionPhs` / `ionPrf`（电离层 excess phase / Ne 剖面）阅读器或下载器 → 见 [data-access 掩星 RO](../data-access.md) · [awsgnssroutils](https://github.com/gnss-ro/aws-opendata) · [data.cosmic](https://data.cosmic.ucar.edu/gnss-ro/)
- **不是** 地基双频 TEC / ROTI / GIM → [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md) / [oasis-roti](./oasis-roti.md) / [ionex-gim](./ionex-gim.md)
- **不** 处理 ROM SAF ROPP 流水线；**不** 替代气象同化前的质控链
- 默认 instrument 子串 `cosmic`；其它 GENESIS 任务树需自核 `--instrument`

一句话：cosmic-crunch = **GENESIS COSMIC-1 大气 L2 ASCII 批量下载 + netCDF4 适配器**（不是 CDAAC 电离层产品工具）。

| 术语 | 含义 |
| --- | --- |
| GENESIS L2 | JPL 发布的 GPS-OCC-L2 大气反演剖面（折射度 / T / P / 水汽压） |
| CDAAC ionPrf / ionPhs | UCAR 电离层 Ne / excess phase；**本包不拉、不读** |
| `jpl_cosmic/YYYY/YYYY-MM-DD/{txt,nc}/` | 本机落地树（相对 cwd） |
| `--test` | 只下当前过滤命中的一小撮文件（本机 10 个）做连通性冒烟 |
| `COSMIC1-Profile` / `NCEP_FNL-Profile` | netCDF **group**：掩星反演 vs NCEP FNL 对照剖面 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install 'cosmic-crunch==2.1.2'
cosmic-crunch --version
# 期望：cosmic-crunch 2.1.2
python -c "import importlib.metadata as m; print(m.version('cosmic-crunch'))"
# 期望：2.1.2
```

依赖：`netcdf4` · `pandas` · `requests` · `tqdm`（pip 自动装）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `cosmic-crunch: command not found` | venv 未激活 / 未装入口点 | `source .venv/bin/activate`；重装包 |
| `No module named 'netCDF4'` | 环境残缺 | `pip install netcdf4` |
| 旧文档写 `/ftp/pub/genesis/...` | v1 根已死 | 用默认 `.../ftp/glevels` 或显式 `--base-url` |

## 3. 端到端：`get --test` → convert → 探活（本机真跑）

默认在 **当前工作目录** 写 `jpl_cosmic/` 与 `cosmic_crunch.log`。本机用 `~/iono_ops/cosmic_data`。

### 3.1 下载小样本（GENESIS 在线）

```bash
cd ~/iono_ops/cosmic_data
source ~/iono_ops/.venv/bin/activate
cosmic-crunch get --test --year_regex 2019 --date_regex 2019-01-03
find jpl_cosmic -name '*.L2.txt.gz' | wc -l
# 期望：10
ls jpl_cosmic/2019/2019-01-03/txt/ | head
```

**本机 stdout（截断进度条；2026-09-24 EDT，`cosmic-crunch` 2.1.2，EXIT 0）：**

```text
Crawling all ./cosmic<#>/postproc: 100%|██████████| 1/1 ...
Crawling all ./cosmic<#>/.../<year>: 100%|██████████| 1/1 ...
Crawling all ./cosmic<#>/.../<date>: 100%|██████████| 1/1 ...
Crawling all ./cosmic<#>/.../L2/<format>: 100%|██████████| 1/1 ...
Downloading data files: 100%|██████████| 10/10 ...
```

落地例：`jpl_cosmic/2019/2019-01-03/txt/20190103_0000co1_g72_2p6.L2.txt.gz`（本机 **25840** bytes）。

### 3.2 一眼 ASCII 头（大气产品边界）

```bash
zcat jpl_cosmic/2019/2019-01-03/txt/20190103_0000co1_g72_2p6.L2.txt.gz | head -n 12
```

**本机截断：**

```text
ProductCreationTime = 2020-07-29T22:13:07
ShortName = GPS-OCC-L2
LongName = GPS-Occultation-Level-2
DataSetID = 20190103_0000co1_g72_2p6
ParameterName = {"Atmosphere", "Refractivity", "Temperature", "Pressure" , "Water Vapor Pressure"}
PlatformShortName = COSMIC1
SensorShortName = COSMIC1-IGOR
VersionID = 2.6
ProcessingLevel = 2
```

要点：`ParameterName` 全是 **大气** 量；没有 Ne / TEC / ionPrf。

### 3.3 转 netCDF4（单文件 / 整目录）

```bash
# 单文件
cosmic-crunch convert \
  jpl_cosmic/2019/2019-01-03/txt/20190103_0000co1_g72_2p6.L2.txt.gz

# 或目录递归（本机 10 文件）
cosmic-crunch convert jpl_cosmic/2019/2019-01-03/txt/
find jpl_cosmic -name '*.L2.nc' | wc -l
# 期望：10；nc 与 txt 同日目录并列：.../nc/*.L2.nc
```

**本机 stdout（单文件，EXIT 0）：**

```text
Converting ASCII to netCDF4: 100%|██████████| 1/1 ...

ASCII to netCDF4 conversion summary:
 - Successful conversions: 1
 - Skipped conversions:    0
 - Conversion errors:      0
 - Total number of files:  1
```

**目录 10 文件摘要（同机）：** `Successful conversions: 10` · `Skipped: 0` · `errors: 0`。

一步到位：`cosmic-crunch get --test --year_regex 2019 --date_regex 2019-01-03 --netcdf4`（本机同样 10 txt + 10 nc，convert 摘要同上）。

### 3.4 探活 netCDF groups

```bash
python - <<'PY'
from netCDF4 import Dataset
p = "jpl_cosmic/2019/2019-01-03/nc/20190103_0000co1_g72_2p6.L2.nc"
ds = Dataset(p)
print("groups", list(ds.groups))
print("ShortName", ds.ShortName, "ParameterName", list(ds.ParameterName))
g = ds.groups["COSMIC1-Profile"]
print("nlev", len(g.dimensions["Index"]), "vars", list(g.variables))
h = g.variables["Height"][:]
print(f"Height km: {h.min():.3f} .. {h.max():.3f}")
ds.close()
PY
```

**本机结果：**

```text
groups ['COSMIC1-Profile', 'NCEP_FNL-Profile']
ShortName GPS-OCC-L2 ParameterName ['Atmosphere', 'Refractivity', 'Temperature', 'Pressure', 'Water Vapor Pressure']
nlev 417 vars ['Height', 'Lat', 'Lon', 'Refractivity', 'Temperature', 'Pressure', 'WV Pressure']
Height km: 0.399 .. 59.699
```

（同文件 `NCEP_FNL-Profile`：`Index=379`，变量同名；根组 **无** 变量，字段在 group 内。全局属性真值：`Transmitter=gps72`、`Receiver=cosmic1`、`RisingSettingMode=Setting`。）

> 质检补坑：同目录**再跑** `convert` 仍报 `Successful conversions: 10`/`Skipped: 0`——**无跳过已存在 nc**、直接覆盖；`--skip_empty` 只跳“全空数组”文件，不是增量开关。增量请自己先 `find … -name '*.L2.nc'` 过滤。

## 4. I/O 字段

| 路径 / 字段 | 含义 |
| --- | --- |
| `*.L2.txt.gz` | GENESIS ASCII 源；头键值 + 剖面表（类型码 68/83） |
| `*.L2.nc` | 转换产物；全局属性抄自 ASCII 头；剖面在 **groups** |
| 全局 `Transmitter` / `Receiver` | 例 `gps72` / `cosmic1` |
| 全局 `RisingSettingMode` | `Rising` / `Setting` |
| 全局 `LowestAltitude` | 最低高度（km） |
| group 变量 `Height` | 高度 km（本机 COSMIC1 0.399–59.699；全局 `LowestAltitude`=0.399119） |
| `Lat` / `Lon` | 切点纬度/经度 |
| `Refractivity` | 折射度 N |
| `Temperature` / `Pressure` | 温度 K / 气压 hPa 量级（以文件为准） |
| `WV Pressure` | 水汽压；缺测在 ASCII 为 `-9999` |

## 5. 参数（常用）

| 旗标 | 作用 | 本机注意 |
| --- | --- | --- |
| `get --test` | 小子集下载 | 冒烟必开；全日勿裸跑无正则 |
| `--year_regex` / `--date_regex` | 年/日过滤 | 例 `2019` · `2019-01-03` |
| `--instrument` | 目录子串过滤 | 默认 `cosmic` |
| `--base-url` | 覆盖爬取根 | 优先于 `COSMIC_CRUNCH_BASE_URL` |
| `--netcdf4` | 下载后立即转换 | 等价 get + convert |
| `--processes N` | 进程池 | 默认 1；站点限流时勿盲目加大 |
| `--skip_empty` | 跳过全空数组文件 | 空文件默认仍会尝试写 nc |
| `--compress` / `--complevel` | zlib 压缩 nc | 默认关；小剖面可能压后变大 |
| `convert PATH…` | 文件或目录递归 | 输出写到并列 `nc/` |

完整列表：`cosmic-crunch get -h` · `cosmic-crunch convert -h`。

## 6. 接到哪步

1. **大气 RO 气候/对照**：本手册 `get` → `convert` → 自写 xarray/netCDF4 统计；对照场已在 `NCEP_FNL-Profile`。
2. **电离层 Ne / excess phase**：停——改走 [data-access 掩星 RO](../data-access.md)：CDAAC 直链 `ionPhs`/`ionPrf` 或 `pip install awsgnssroutils`（AWS 三型，**无** ionPhs 文件名）。
3. **地基 TEC 主链**：与本包无关 → 路径 A（[georinex](./georinex.md) / [pytecgg](./pytecgg.md)）。
4. **模型气候态对照**（可选）：大气剖面可与 IRI/中性大气模型比趋势；电离层剖面仍用 CDAAC Ne，勿拿 GENESIS L2 `Temperature` 冒充 Ne。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 当 ionPrf 用 | 名字含 COSMIC | 看 `ParameterName`；电离层走 CDAAC/AWS |
| 2 | `nvars==0` 误判空文件 | 变量在 **group** | `list(ds.groups)` 再读 |
| 3 | 无过滤全日爬 | 站宽、文件海量 | 必加 `--year_regex`/`--date_regex`；先 `--test` |
| 4 | 旧 URL 404 | v1 `/ftp/pub/genesis` 已死 | 用默认 glevels 或 `--base-url` |
| 5 | cwd 下突然多出 `jpl_cosmic/` | 相对路径落地 | 固定工作目录再跑 |
| 6 | `cosmic_crunch.log` 空 | 正常时少写 | 失败再看；别当无运行证据 |
| 7 | `--compress` 体积变大 | 多小变量 | 默认别开；大剖面再试 |
| 8 | 与 AWS `atmosphericRetrieval` 硬拼 | 版本/中心不同 | 分列元数据；勿无 QC 拼时间序列 |
| 9 | 把 `-9999` 当真值 | ASCII 缺测 | 转后检查；绘图前掩膜 |
| 10 | 并行把站点打挂 | `--processes` 过大 | 保持 1–2；加过滤 |

## 8. 选型

| 你要… | 打开 |
| --- | --- |
| JPL GENESIS COSMIC-1 **大气** L2 → netCDF | **本手册 cosmic-crunch** |
| CDAAC / AWS **电离层** RO（ionPhs/ionPrf/calibratedPhase…） | [data-access RO](../data-access.md) · awsgnssroutils / CDAAC |
| 地基双频校准 TEC | [pytecgg](./pytecgg.md) |
| 读 IONEX GIM | [ionex-gim](./ionex-gim.md) |
| 手机/厂商 → RINEX | [android_rinex](./android_rinex.md) / [autorino](./autorino.md) |

相关：[data-access](../data-access.md) · [README](./README.md) · [`PROJECTS.json`](../../PROJECTS.json)
