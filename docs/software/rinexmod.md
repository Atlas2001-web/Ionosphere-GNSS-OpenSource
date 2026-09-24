# rinexmod · RINEX 头/元数据批量修改操作手册

目录：[`PROJECTS.json` → `rinexmod`](../../PROJECTS.json) · 上游 <https://github.com/IPGP/rinexmod> · PyPI <https://pypi.org/project/rinexmod/> · 许可 **GPL-3.0** · 本机 **`rinexmod` 4.2.1** / 依赖 **`hatanaka` 2.8.1** · georinex 样例 `demo.10o` 改头实跑（2026-09-24 EDT）

> 岗位：**批量改 RINEX OBS 头字段、按站码重命名、长短文件名、可选 Hatanaka/gzip**。冲突时：**本机 `rinexmod_run -h` / 上游 README > 本文**。伴生台网入库 → [autorino](./autorino.md)；读进 Python → [georinex](./georinex.md)；CRX ↔ RNX → [hatanaka](./hatanaka.md)。**不是**定位 / QC / TEC。

## 1. 用途与边界

**做：**

- CLI `rinexmod_run`：列表或单文件 → 改头 → 写出到**另一目录**
- 元数据源：`-k/--modif_kw` 手写 · `-s` sitelog · `-gml` GeodesyML · GAMIT `-sti`+`-lfi`
- 重命名：`-m` 4/9 字符站码 · `-co` ISO 国家码 · `-l` 长名 / `-sh` 短名 · `-fns basic|flex|exact`
- 压缩：默认高阶 **Hatanaka** + 低阶 **`gz`**；`-nh` 跳过 Hatanaka；`-c gz|Z|none`
- 附加工具：`crzmeta`（teqc+meta 类头信息速查）

**不做：**

- **不是** 读 RINEX → xarray/pandas → [georinex](./georinex.md) · [gnsspy](./gnsspy.md)
- **不是** 厂商 RAW→RINEX 编排 → [autorino](./autorino.md)（其 `rinexmod` 步骤调本包）
- **不是** 观测 QC / 拼日抽稀 → [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md)
- **不是** 定位 / TEC → [rtklib](./rtklib.md) · [pytecgg](./pytecgg.md)
- **不原地改写**：输入输出目录相同 → 错误 30，直接跳过

一句话：rinexmod = **IPGP 台网侧 RINEX 头与命名规范化器**；观测体本身不重算。

| 术语 | 含义 |
| --- | --- |
| `modif_kw` / `-k` | 手写头/文件名字段；覆盖 sitelog 等同名字段 |
| `marker` / `-m` | 用于**文件名**的站码；头里 MARKER NAME 默认同步，可被 `-k marker_name=` 覆盖 |
| 长名 / 短名 | IGS 长名 `SITE00CCC_…_MO.rnx.gz` vs 旧式 `ssssddds.yyt` |
| Hatanaka | 高阶差分压缩（`.crx`）；本包默认走 Python [`hatanaka`](./hatanaka.md) |
| `crzmeta` | 不解压打印头摘要（可 `-p` 画采样间隔） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv rinexmod-demo/.venv
source rinexmod-demo/.venv/bin/activate
pip install -U pip
pip install 'rinexmod==4.2.1'
python -c "import importlib.metadata as m; print(m.version('rinexmod'))"
# 期望：4.2.1
rinexmod_run -h | head -n 12
which crzmeta
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python 过旧 | 换 3.9+（本机 3.13 OK） |
| 依赖一长串 | 正常（hatanaka/pandas/…） | 用 venv |
| 旧文档 `import rinexmod.rinexmod_api` | 4.x 路径已变 | `from rinexmod.api.rinexmod_main import rinexmod` |

## 3. 端到端：改头 + 短名 / 长名（本机真跑）

样例：georinex 上游 `demo.10o`（RINEX **2.11**，2 历元，MARKER=`MRKR`，接收机 `ASHTECH UZ-12`）。

```bash
cd ~/iono_ops/rinexmod-demo && source .venv/bin/activate
mkdir -p data out out_long
curl -fsSL -o data/demo.10o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/demo.10o
# 头摘要（不必先解压）
crzmeta data/demo.10o
```

**本机 `crzmeta` stdout（节选，2026-09-24 EDT）：**

```text
File                          : data/demo.10o
File size (bytes)             : 6878
Rinex version                 : 2.11
Sample rate                   : 00U
File period                   : 01H
Observable type               : M (MIXED)
Marker name                   : MRKR
Operator                      : gAGE
Agency                        : UPC: Technical Unive
Receiver type                 : ASHTECH UZ-12
Antenna type                  : AOAD/M_T        NONE
Start date and time           : 2010-03-05 00:00:00
Final date and time           : 2010-03-05 00:00:30
```

（仅 2 历元 → Sample rate 显示 `00U`；正式站文件会是 `30S` 等。）

### 3.1 手写关键词 + 短名写出（`-nh -c none`）

```bash
rinexmod_run -a -i data/demo.10o -o out \
  -fr -nh -c none -v -sh \
  -m DEMO \
  -k marker_name='DEMO' agency='IPGP' operator='RINEXMOD' \
     receiver_type='TRIMBLE NETR9' antenna_type='TRM59800.00'
```

**本机日志（去 ANSI，节选）：**

```text
...|I|rinexmod       |# Inp. file: data/demo.10o
...|W|rinexmod       |Site's country not retrieved. RINEX will not be properly renamed: data/demo.10o
...|W|_mod_rec_check |DEMO00XXX rec. model type in RINEX (ASHTECH UZ-12) & in metadata (TRIMBLE NETR9) are different.
...|W|sort_header    |unable to sort header's lines, action skipped (RNXv3 only)
...|I|rinexmod       |# Out. file: .../out/demo064a.10o
```

`-v` 时 DEBUG 元数据摘要（同次运行写入 `*_rinexmod_errors.log`）：

```text
RINEX Origin Metadata :
Marker name                   : MRKR
Agency                        : UPC: Technical Unive
Receiver type                 : ASHTECH UZ-12
Antenna type                  : AOAD/M_T        NONE
Final date and time           : 2010-03-05 00:00:30

RINEX Manual Keywords-Modified Metadata:
Marker name                   : DEMO
Operator                      : RINEXMOD
Agency                        : IPGP
Receiver type                 : TRIMBLE NETR9
Antenna type                  : TRM59800.00
```

**写出头字段对照（`out/demo064a.10o`）：**

| 字段 | 输入 | 输出 |
| --- | --- | --- |
| MARKER NAME | `MRKR` | `DEMO` |
| OBSERVER / AGENCY | `gAGE` / `UPC: Technical…` | `RINEXMOD` / `IPGP` |
| REC # / TYPE | `ASHTECH UZ-12` | `TRIMBLE NETR9` |
| ANT # / TYPE | `AOAD/M_T NONE` | `TRM59800.00` |
| TIME OF LAST OBS | 头写全日 `23:59:30` | **按数据**改写 `00:00:30` |
| 注释 | — | 增 `RinexMod 4.2.1 METADATA UPDATE …` + `rinexmoded with keywords:…` |
| 文件名 | `demo.10o` | `demo064a.10o`（短名；doy=064） |
| 体积 | 6878 B | 7141 B（头注释变长；**2 历元体保留**） |

georinex 探活改后文件：`demo064a.10o: 2010-03-05T00:00:00 … 2 30.0`（与输入一致）。

### 3.2 长名 + gzip（跳过 Hatanaka）

本样例历元行时钟偏移 `   -0.12345` **不合 RNX2CRX 格式**；默认 Hatanaka 会炸（见坑 3）。教学用 `-nh`：

```bash
rinexmod_run -a -i data/demo.10o -o out_long \
  -fr -nh -l -c gz -v \
  -m DEMO00FRA -co FRA \
  -k marker_name='DEMO' agency='IPGP' operator='RINEXMOD'
ls out_long/
# DEMO00FRA_R_20100640000_01H_00U_MO.rnx.gz
```

**本机：** 写出 **1814 B** gzip；解压后 MARKER=`DEMO`，AGENCY=`IPGP`，文件名 **9 字符站码 + `_R_` + 年积日 `2010064` + `_01H_00U_MO.rnx.gz`**。

### 3.3 API（4.2.1 真路径）

上游 README 仍写 `rinexmod.rinexmod_api`——**本机 4.2.1 无此模块**。用：

```bash
python - <<'PY'
from rinexmod.api.rinexmod_main import rinexmod
from pathlib import Path
out = Path('out_api'); out.mkdir(exist_ok=True)
path = rinexmod(
    'data/demo.10o', str(out),
    modif_kw={
        'marker_name': 'APID', 'agency': 'IONO', 'operator': 'API',
        'receiver_type': 'SEPT POLARX5', 'antenna_type': 'SEPCHOKE_B3E6',
    },
    marker='APID', force_rnx_load=True,
    no_hatanaka=True, compression='none', shortname=False, verbose=False,
)
print(path)
PY
# 本机：out_api/APID00XXX_R_20100640000_01H_00U_MO.rnx
# 头：MARKER=APID；OBSERVER/AGENCY=API/IONO；REC=SEPT POLARX5；ANT=SEPCHOKE_B3E6
# 要短名：shortname=True → 本机 out_api_sh/shrt064a.10o
```

## 4. I/O 与关键参数

| 输入 | 输出 |
| --- | --- |
| RINEX 2/3/4 OBS（可 `.gz` / `.Z` / `.crx`） | 改头后的 OBS（默认常再 Hatanaka+gz） |
| sitelog / GeodesyML / `-k` / GAMIT station.info+L-file | 写入头的仪器/坐标/机构等 |
| `-m` / `-co` / `-fns` | 短名或长名文件名 |

| 参数 | 作用 |
| --- | --- |
| `-i` / `-o` | 输入（列表文件 / 多路径 / 单文件）与**输出目录**（必填） |
| `-a` | 单文件模式（否则 `-i` 常被当成路径列表文件） |
| `-k KEY=VAL …` | `marker_name` `agency` `operator` `receiver_*` `antenna_*` `interval` `filename_*` … |
| `-m` / `-co` | 站码 / ISO 国家码（长名 `SITE00CCC`） |
| `-s` / `-gml` / `-sti`+`-lfi` | sitelog / GeodesyML / GAMIT 元数据 |
| `-fr` | 强制加载非标准文件名 |
| `-nh` / `-c` | 跳过 Hatanaka；低阶 `gz`（默认）/`Z`/`none` |
| `-l` / `-sh` | 强制长名（并倾向 gzip）/ 强制短名 |
| `-v` / `-d` | 改前改后元数据；调试（遇错停） |
| `-rm` | 写出成功后删输入——**高风险** |

完整列表以 `rinexmod_run -h` 为准（4.2.1 另有 `-krr` 保留原接收机记录、`-rnd` 仪器换日取整等）。

## 5. 接到哪步

- 台网 RAW→RINEX 后改头入库 → [autorino](./autorino.md) 的 `rinexmod` 步骤，或本文 CLI
- 改完探活 / 进 Python → [georinex](./georinex.md)；Hatanaka 官方二进制 → [rnxcmp](./rnxcmp.md)；pip 解压 → [hatanaka](./hatanaka.md)
- 一日 TEC 路径：下载/转换 → **（可选本文规范化头）** → [georinex](./georinex.md) → [pytecgg](./pytecgg.md)
- 拼日/抽稀正式产品仍用 [gfzrnx](./gfzrnx.md)，不要指望 rinexmod 做切割

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Input and output folders are the same!` | 禁止原地改 | `-o` 指到**别的**目录 |
| 2 | 单文件被当列表读挂 | 未加 `-a` | 单文件务必 `-a` |
| 3 | `HatanakaException: invalid format for clock offset` | 样例/坏历元行（如 `demo.10o` 的 `-0.12345`） | `-nh`；或先修历元；正式站文件再开默认 Hatanaka |
| 4 | `Site's country not retrieved` / 长名带 `XXX` | 无 `-co` / sitelog / 9 字符表 | `-co FRA` 或 `-m DEMO00FRA` / `-n` 九字符表 |
| 5 | `_mod_rec_check` 警告机型不一致 | `-k receiver_type` 与原头不同 | 核对 sitelog；警告不阻断写出 |
| 6 | `sort_header … RNXv3 only` | RINEX 2 头不排序 | 可忽略；升 R3 再指望排序 |
| 7 | Sample rate `00U` | 历元太少推不出间隔 | 用全日/多历元文件；或 `-k interval=` / `filename_data_freq=` |
| 8 | `import rinexmod.rinexmod_api` ModuleNotFound | README 旧路径 | `from rinexmod.api.rinexmod_main import rinexmod` |
| 9 | 默认不写新元数据 | 未给 `-k`/`-s`/… | 至少提供一种元数据源 |
| 10 | 把头改了当 QC/定位完成 | 只动头与文件名 | 接 [anubis](./anubis.md)/[georinex](./georinex.md)/[rtklib](./rtklib.md) |
| 11 | `-rm` 误删原盘 | 写出成功即删输入 | 默认勿开；备份后再用 |
| 12 | 与 [autorino](./autorino.md) 版本漂移 | 流水线钉死两包版本 | 本机对照：autorino 2.4.2 ↔ rinexmod **4.2.1** |

## 7. 选型与链接

| 你要… | 用 |
| --- | --- |
| 批量改 RINEX 头 / 长短名 / 压缩约定 | **本文 rinexmod** |
| 厂商 RAW 拉取→转 RINEX→再调本包 | [autorino](./autorino.md) |
| RINEX → xarray | [georinex](./georinex.md) |
| Python CRX↔RNX | [hatanaka](./hatanaka.md) |
| 官方 RNXCMP 二进制 | [rnxcmp](./rnxcmp.md) |
| 拼日 / 抽稀 / 切片 | [gfzrnx](./gfzrnx.md) |

- 上游：<https://github.com/IPGP/rinexmod>
- PyPI：<https://pypi.org/project/rinexmod/>
- 兄弟：[autorino](./autorino.md) · [georinex](./georinex.md) · [hatanaka](./hatanaka.md) · [rnxcmp](./rnxcmp.md) · [gfzrnx](./gfzrnx.md) · [pinot](./pinot.md)
