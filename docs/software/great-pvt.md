# GREAT-PVT · 武大 GREAT 精密 PVT 操作手册

目录：[`PROJECTS.json` → `GREAT-PVT`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-PVT> · 许可 **GPL-3.0** · tip **`8bd3d23`** / tag **v1.4.0** · 预编译 Linux `GREAT_PVT` 自称 **`$Ver: 1.1$`**（2024-11-04）· 本机验证：样例 `PPPFLT_2023305` **GODN** 静态双频浮点 **1 h** → **120** 历元 `.flt`；末历元 XYZ=`(1130760.6978,-4831298.6741,3994155.2036)`，RMS≈(0.0043,0.0034,0.0028)→3D≈**0.0062 m**；NSat=**29** Quality=**2**；与同 XML 冒烟备份首末 **逐字段一致** · 2026-09-24 05:15 EDT · **质检复跑通过**（2026-09-24 05:21 EDT；tip `8bd3d23`/v1.4.0；`-h` → `GRAET-PVT [$Ver: 1.1 $]`）

> 岗位：多系统 **PPP / PPP-AR / RTK** 滤波精密 PVT（XML 驱动）。冲突时：**本机 `GREAT_PVT -h` / `doc/*.xml` / PDF > 本文**。轻量 CLI → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；GA YAML 工具箱 → [ginan](./ginan.md)。

**质检边界：** 冒烟为 **1 h 浮点**（非全日、未开 UPD 固定）；预编译 Linux 二进制即可，**无需** GPU/许可证。RTK 样例包未复跑（体积大）。

## 1. 用途与边界

**做：**

- 多系统（GPS/GLO/GAL/BDS-2/3）**IF / 非差非组合** PPP；浮点与固定
- 双频 / 混频 **RTK** 滤波
- 预编译 Windows/Linux 二进制 + CMake 源码；批处理与绘图脚本在 `util/`
- 样例：`sample_data/PPPFLT_2023305.zip`、`RTKFLT_2020351.zip`

**不做：**

- **不是** 实时多用户 Caster / Pi 基站 → [bkg-ntripcaster](./bkg-ntripcaster.md) / [rtkbase](./rtkbase.md)
- **不是** FGO/ROS 研究栈 → [graphgnsslib](./graphgnsslib.md)
- **不是** STEC/ROTI 产品链 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- 本页冒烟为 **1 h 浮点**；全日固定率/外符合需自备产品与参考坐标

一句话：GREAT-PVT = **武大 GREAT 组开源精密 PVT（LibGREAT + LibGnut）**。

| 术语 | 含义 |
| --- | --- |
| `GREAT_PVT` | CLI 入口；`-x config.xml` |
| `.flt` | 滤波结果（周内秒 + ECEF + RMS + NSat + AmbStatus） |
| `PPPFLT` / `RTKFLT` | 样例包：PPP 滤波 / RTK 滤波 |
| UPD | 宽巷/窄巷相位小数偏差（固定解） |

## 2. 安装

### 2.1 预编译（本机采用）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/GREAT-WHU/GREAT-PVT.git
cd GREAT-PVT && git rev-parse --short HEAD && git describe --tags --always
# 8bd3d23 / v1.4.0
chmod +x bin/Linux/GREAT_PVT
export LD_LIBRARY_PATH="$PWD/bin/Linux:${LD_LIBRARY_PATH:-}"
./bin/Linux/GREAT_PVT -h | head -n 20
```

**期望：** 头行含 `GRAET-PVT [$Ver: 1.1 $]`（上游拼写如此）；Usage 含 `-x file`。

### 2.2 源码（可选）

```bash
cmake -S src -B src/build -DCMAKE_BUILD_TYPE=Release
cmake --build src/build --config Release
# 产物多在 src/build_Linux 一类目录；仍需把 *.so 放进 LD_LIBRARY_PATH
```

### 2.3 样例数据

```bash
cd ~/iono_ops/GREAT-PVT
unzip -qo sample_data/PPPFLT_2023305.zip -d ~/iono_ops/great-run/
ls ~/iono_ops/great-run/PPPFLT_2023305/{obs,gnss,model,xml,result} | head
```

## 3. 端到端：GODN 1 h 静态 DF 浮点（本机真跑）

官方 XML 含 Windows 反斜杠与全日窗；Linux 冒烟改正斜杠、缩窗、单站。

### 3.1 准备 XML

```bash
RUN=~/iono_ops/great-run/PPPFLT_2023305
cd "$RUN"
python3 - <<'PY'
from pathlib import Path
src=Path('xml/GREAT_PPPFLT_static_DF_Float.xml')
txt=src.read_text().replace('\\','/')
txt=txt.replace('<end> 2023-11-01 23:59:30 </end>','<end> 2023-11-01 01:00:00 </end>')
# 若模板标签为 beg/end：
txt=txt.replace('2023-11-01 23:59:30','2023-11-01 01:00:00')
lines=[]
for L in txt.splitlines(True):
    if 'harb3050.23o' in L or 'HARB' in L and '<rec>' in L: 
        if 'harb3050' in L: continue
    if '<rec>' in L: L='        <rec> GODN                </rec>\n'
    lines.append(L)
Path('xml/smoke_GODN_1h_float.xml').write_text(''.join(lines))
print('ok', Path('xml/smoke_GODN_1h_float.xml').stat().st_size)
PY
```

核对输入文件存在：`obs/godn3050.23o`、`gnss/COD0MGXFIN_*`、`model/igs20_2290.atx` 等（以解压树为准）。

### 3.2 运行

```bash
export LD_LIBRARY_PATH=~/iono_ops/GREAT-PVT/bin/Linux:$LD_LIBRARY_PATH
cd ~/iono_ops/great-run/PPPFLT_2023305
# 避免覆盖样例参考：先备份
cp -n result/GODN-PPP_sta_DF_Float.flt result/GODN-PPP_sta_DF_Float.flt.bak 2>/dev/null || true
~/iono_ops/GREAT-PVT/bin/Linux/GREAT_PVT -x xml/smoke_GODN_1h_float.xml
wc -l result/GODN-PPP_sta_DF_Float.flt
tail -n 3 result/GODN-PPP_sta_DF_Float.flt
```

### 3.3 本机结果（质检复跑 · v1.4.0 / tip `8bd3d23`，2026-09-24 05:21 EDT）

```text
GREAT_PVT -h → GRAET-PVT [$Ver: 1.1 $] … -x file
GODN 2023-11-01 00:00–01:00  进度至 100%；Forward filter duration ~3 s
result/GODN-PPP_sta_DF_Float.flt ：122 行（2 行头 + 120 历元）
首历元 sow=259230 XYZ=(1130760.0786,-4831296.6734,3994154.2047)
  RMS≈(0.8745,2.5145,1.9945)；NSat=30；Amb=Float；Quality=6
末历元 sow=262800 XYZ=(1130760.6978,-4831298.6741,3994155.2036)
  RMS=(0.0043,0.0034,0.0028)→3D≈0.0062 m；NSat=29；Amb=Float；Quality=2
与同 XML 冒烟备份首末历元逐字段一致（≠样例包全日 result_ref）
```

| 输入 | 说明 |
| --- | --- |
| `xml/smoke_GODN_1h_float.xml` | 缩窗单站浮点 |
| `obs/godn3050.23o` | GODN 30 s 观测 |
| `gnss/COD0MGXFIN_*SP3/CLK` + DCB + brdc | 精密产品 |
| `model/*` | ATX / EOP / ocean / DE |

| 输出 | 含义 |
| --- | --- |
| `*-PPP_sta_DF_Float.flt` | 周内秒、ECEF、速度、RMS、NSat、PDOP、AmbStatus、Quality |
| `*-PPP` 日志 | 详细 PPP 跟踪（若 XML 打开） |

固定解：在 XML 启用 `<upd>` 宽巷/窄巷文件并换 `*_Fixed.xml` 模板；本机冒烟 **未** 开固定。

## 4. 关键参数

| 项 | 作用 |
| --- | --- |
| `-x file` | XML 配置（必需） |
| `-h` / `-V` | 帮助 / 版本 |
| `<beg>/<end>/<int>` | 时段与采样 |
| `<sys>` / `<rec>` | 系统与站名（4 字大写） |
| `<obs_combination>` | `IONO_FREE` / `RAW_ALL` 等 |
| `<pos_kin>` | false 静态 / true 动态 |
| UPD 节点 | 固定解必需；缺则浮点或报错 |

## 5. 接到哪步

- 冒烟/教学 RTK → [rtklib](./rtklib.md)；FGO 对照 → [graphgnsslib](./graphgnsslib.md)
- 发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；GA 中心型 → [ginan](./ginan.md)
- 产品下载 → [data-access](../data-access.md) / [gampii-good](./gampii-good.md)
- 工作流 **D**：QC →（可选本文 PPP）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `error while loading shared libraries: libLibGREAT.so` | 未设 `LD_LIBRARY_PATH` | `export LD_LIBRARY_PATH=~/iono_ops/GREAT-PVT/bin/Linux:$LD_LIBRARY_PATH` |
| 2 | 找不到观测/SP3 | XML 仍是 `obs\...` 反斜杠 | `sed -i 's#\\#/#g' your.xml` |
| 3 | 跑起来立刻结束无 `.flt` | 站名/路径/时段无交 | 查 `<rec>` 与 `rinexo` 文件名；放宽 `<beg>/<end>` |
| 4 | 固定解失败 | 未给 UPD 或系统不一致 | 用样例 `*_Fixed.xml` + `upd/`；或先浮点 |
| 5 | 与 [pride-pppar](./pride-pppar.md) 坐标差大 | 产品/天线/约束不同 | 同 SP3/CLK/ATX 再比；看 `.flt` RMS |
| 6 | 把 1 h 浮点当发表坐标 | 未收敛评估 | 全日 + 外符合；或 [pride-pppar](./pride-pppar.md) |
| 7 | `GREAT_PVT: command not found` | 未 chmod / 路径错 | `chmod +x bin/Linux/GREAT_PVT`；写绝对路径 |
| 8 | 头行写 `GRAET-PVT` | 上游拼写 | 忽略；以 `-h` 能出 Usage 为准 |
| 9 | 覆盖了样例 `result/*.flt` | 同名输出 | 跑前 `cp` 备份；或改 XML `<flt>` 路径 |
| 10 | RTK 样例巨大 IO | `RTKFLT_2020351.zip` ~400 MB 解压 | 磁盘预留；先 PPP 冒烟 |
| 11 | 期望直接出 STEC | 软件是 PVT | TEC→[pytecgg](./pytecgg.md) |
| 12 | CMake 编过但运行链到旧 `.so` | `LD_LIBRARY_PATH` 指向 bin 预编译 | `ldd $(which GREAT_PVT)` 核对 |
| 13 | 1 h 冒烟末历元 ≠ `result_ref_bak` 全日末 | 参考是全日解 | 只与同窗同 XML 自备份比；或扩 `<end>` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 武大 GREAT 精密 PPP/RTK（XML） | **本文 GREAT-PVT** |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| GA pea/YAML | [ginan](./ginan.md) |
| 轻量 CLI | [rtklib](./rtklib.md) |
| FGO 研究 | [graphgnsslib](./graphgnsslib.md) |

## 8. 相关

[pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [ginan](./ginan.md) · [graphgnsslib](./graphgnsslib.md) · [gampii-good](./gampii-good.md) · [data-access](../data-access.md) · [README](./README.md)

- 文档：`doc/GREAT-PVT_1.0.pdf`、`doc/GREAT-PVT_manual_1.0.pdf`
- QQ 交流群见上游 README（可选）
