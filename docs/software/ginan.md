# Ginan · Geoscience Australia 精密定位 / 改正工具箱操作手册

目录：[`PROJECTS.json` → `ginan`](../../PROJECTS.json) · 上游 <https://github.com/GeoscienceAustralia/ginan> · Docker Hub `gnssanalysis/ginan` · 许可 **Apache-2.0** · 发布 **v4.1.4** · tip **`5033996`** · 入口 **`pea`** · 本机验证：Linux 预编译 `pea` + 官方 `ppp_example.yaml` → `--dry-run` 通过；`--max_epochs 20` 写出 ALIC/DARW/HOB2 `.POS`（ALIC 末历元相对 IGS20 参考 ≈**0.08 m** 3D，仅冒烟）· 2026-09-24 05:16 EDT · **质检复跑通过**（dry-run；`--max_epochs 20` ALIC 3D≈0.08 m；tip `5033996`）

> 岗位：事后 **PPP / 网解 / POD** 与实时改正试验；YAML 驱动。冲突时：**本机 `pea -h` / 仓内 `exampleConfigs/` > 本文**。轻量 CLI → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；开放 SSR 教学 → [cssrlib](./cssrlib.md)。

## 1. 用途与边界

**做：**

- 多系统事后 **PPP**（`ppp_example.yaml`）、实时 PPP/RTK 示例、**POD**、SP3 拟合/对比、流录制
- 输出 **PBO `.POS`**、**TRACE**、可选 **GPX**；支持 RTS 平滑产物
- 电离层：未组合估计 / 薄层 VTEC 映射（见仓内 `Docs/ionosphere.md`）；本页冒烟**未**开电离层网解模式
- 官方预编译 zip / Docker / `vcpkg`+CMake 源码三种安装路径

**不做：**

- **不是** 树莓派基站 Web UI → [rtkbase](./rtkbase.md)
- **不是** 只解 HAS/B2b 页 → [haslib](./haslib.md) / [navdecoder](./navdecoder.md) / [b2blib](./b2blib.md)
- **不是** 发表级模糊度固定主力（本机未跑满日固定率）→ [pride-pppar](./pride-pppar.md)
- 本机**无 Docker**；源码 `vcpkg` 依赖重，冒烟优先 **Release 预编译**

一句话：Ginan = **GA 现代化 C++ GNSS 分析中心工具箱（pea）**。

**质检边界：** 本机用 Release 预编译 `pea` 做 dry-run + `--max_epochs 20` 冒烟；**未**跑全日 PPP/网解/POD，**未**Docker/`vcpkg` 源码编译。完整解算请自备产品与算力。

| 术语 | 含义 |
| --- | --- |
| `pea` | Positioning Engine / Analysis 主程序 |
| `exampleConfigs/*.yaml` | 官方示例配置；路径相对 `exampleConfigs/` |
| `inputData/{data,products}` | 演示 RINEX / 产品；由 S3 `*.gz` 拉取 |
| `--dry-run` | 只解析配置 + 健全性检查 |
| `--max_epochs` | 截断历元（冒烟必用） |
| `.POS` / `.TRACE` | PBO 坐标时序 / 详细跟踪 |

## 2. 安装

### 2.1 预编译（本机采用）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
curl -fsSL -L -o ginan-linux-x64.zip \
  https://github.com/GeoscienceAustralia/ginan/releases/download/v4.1.4/ginan-linux-x64.zip
unzip -qo ginan-linux-x64.zip
./ginan-linux-x64/pea -h | head -n 20
# 期望：PEA starting... (HEAD v4.1.4-…) 与 Options 列表
```

### 2.2 Docker（有 Docker 时推荐）

```bash
docker run -it -v "$(pwd):/data" gnssanalysis/ginan:v4.1.4 bash
pea --help
cd /ginan/exampleConfigs && pea --config ppp_example.yaml --dry-run
```

### 2.3 源码（开发；本机未编）

```bash
git clone --depth 1 --branch v4.1.4 https://github.com/GeoscienceAustralia/ginan.git
# 按 README：安装 vcpkg → cmake --preset release → cmake --build --preset release
# 产物：src/../bin/pea
```

克隆示例与列表（拉数需要）：

```bash
cd ~/iono_ops
git clone --depth 1 https://github.com/GeoscienceAustralia/ginan.git
cd ginan && git rev-parse --short HEAD   # 本机 5033996
```

## 3. 端到端：`ppp_example` 20 历元（本机真跑）

官方例：2019-07-18（DOY **199**）ALIC/DARW/HOB2 + IGS REPRO3 产品。列表文件在 S3 上是 **`路径.gz`**（`getFiles.sh` 会加后缀）。

### 3.1 拉最小输入

```bash
cd ~/iono_ops/ginan/inputData/data
BASE=https://peanpod.s3.ap-southeast-2.amazonaws.com/aux/data
for f in ALIC00AUS_R_20191990000_01D_30S_MO.rnx \
         DARW00AUS_R_20191990000_01D_30S_MO.rnx \
         HOB200AUS_R_20191990000_01D_30S_MO.rnx; do
  curl -fsSL -o "$f.gz" "$BASE/$f.gz" && gzip -df "$f.gz"
done

cd ~/iono_ops/ginan/inputData/products
PBASE=https://peanpod.s3.ap-southeast-2.amazonaws.com/aux/products
for f in igs20.atx finals.data.iau2000.txt igs_satellite_metadata.snx \
  IGS1R03SNX_20191950000_07D_07D_CRD.SNX brdm1990.19p \
  IGS2R03FIN_20191990000_01D_30S_CLK.CLK \
  IGS2R03FIN_20191990000_01D_01D_OSB.BIA \
  IGS2R03FIN_20191990000_01D_05M_ORB.SP3; do
  curl -fsSL -o "$f.gz" "$PBASE/$f.gz" && gzip -df "$f.gz"
done
mkdir -p tables
for f in igrf14coeffs.txt DE436.1950.2050 gpt_25.grd \
         OLOAD_GO.BLQ ALOAD_GO.BLQ opoleloadcoefcmcor.txt \
         sat_yaw_bias_rate.snx qzss_yaw_modes.snx bds_yaw_modes.snx; do
  curl -fsSL -o "tables/$f.gz" "$PBASE/tables/$f.gz" && gzip -df "tables/$f.gz"
done
# 或：cd data && bash getData.sh；cd products && bash getProducts.sh（全量更大）
```

### 3.2 dry-run + 短 PPP

```bash
export PEA=~/iono_ops/ginan-linux-x64/pea   # 按 2.1 解压路径改
cd ~/iono_ops/ginan/exampleConfigs
"$PEA" --config ppp_example.yaml --dry-run
"$PEA" --config ppp_example.yaml --max_epochs 20 -q
ls outputs/ppp_example_HEAD/*.POS | head
```

**本机结果（v4.1.4 / tip `5033996`，2026-09-24 05:11 EDT；质检复跑 2026-09-24 05:16 EDT 同数）：**

```text
Dry-run successful: configuration and sanity checks passed
Process Modes: Preprocessor/SPP/PPP=1；RTS Smoothing=1；Ionospheric=0
Systems: GPS/GLO/GAL=1；BDS/QZSS=0
epoch_interval: 30
产出 outputs/ppp_example_HEAD/：
  ALIC/DARW/HOB2 各 .POS + _smoothed.POS + .TRACE + .GPX
  ALIC .POS：20 历元；参考 IGS20 XYZ≈(-4052052.725, 4212835.987, -2545104.614)
  末历元 2019-07-18T00:09:30 ≈(-4052052.753, 4212836.061, -2545104.628)
  相对参考 3D≈0.08 m（仅 10 min 冒烟，非全日收敛声明）
```

| 输入 | 说明 |
| --- | --- |
| `ppp_example.yaml` | 静态双频 GPS+GAL 事后 PPP 骨架 |
| `…/data/*1990*MO.rnx` | 三站 30 s RINEX |
| `…/products/IGS2R03FIN_…` | SP3/CLK/BIA + ATX/ERP/SNX/表 |

| 输出 | 含义 |
| --- | --- |
| `*.POS` | PBO 时序；含参考坐标与历元 XYZ/NEU |
| `*_smoothed.POS` | RTS 平滑后 |
| `*.TRACE` | 高详跟踪（本机单站 ~10–12 MB / 20 历元） |
| `*.GPX` | 轨迹浏览 |

配置骨架（节选，完整见仓内文件）：

```yaml
inputs:
  inputs_root: ./products/
  atx_files: [igs20.atx]
  satellite_data:
    nav_files: [brdm1990.19p]
    clk_files: [IGS2R03FIN_20191990000_01D_30S_CLK.CLK]
    sp3_files: [IGS2R03FIN_20191990000_01D_05M_ORB.SP3]
  gnss_observations:
    gnss_observations_root: ../data/
    rnx_inputs:
      - ALIC00AUS_R_20191990000_01D_30S_MO.rnx
outputs:
  outputs_root: ./outputs/<CONFIG>
  pos: { output: true, filename: <SOURCE>.POS }
```

## 4. 关键参数

| 旗标 / 键 | 作用 |
| --- | --- |
| `-y/--config` | YAML 配置 |
| `--dry-run` | 只检查 |
| `--max_epochs` / `-n` | 截断历元 |
| `--epoch_interval` / `-i` | 历元间隔 |
| `receiver_options.*.elevation_mask` | 截止角（例 15°） |
| `models.ionospheric_components` | 2/3 阶电离层改正开关 |
| `Process Modes` 摘要 | dry-run 打印：PPP/RTS/Ionospheric 等 |

## 5. 接到哪步

- 快速 SPP/RTK → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)
- 开放改正教学 → [cssrlib](./cssrlib.md) / [claslib](./claslib.md) / [madocalib](./madocalib.md)
- 台站硬件基站 → [rtkbase](./rtkbase.md)；产品获取 → [data-access](../data-access.md) / [gampii-good](./gampii-good.md)
- 工作流 **D**：QC →（可选本文 PPP 冒烟）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | S3 `404` 下 RINEX/产品 | URL 缺 **`.gz`** | `curl …/$f.gz && gzip -df` |
| 2 | `pea: not found` / 动态库缺 | 未解压或非 glibc 环境 | 用官方 `ginan-linux-x64.zip`；或 Docker |
| 3 | dry-run 缺文件 | 未拉 `inputData` 或 symlink 断 | 确认 `exampleConfigs/{data,products}` → `../inputData/…` |
| 4 | TRACE 暴涨占盘 | `trace.level` 高 + 全日 | 冒烟加 `--max_epochs`；降 level |
| 5 | 把 20 历元当发表坐标 | 未收敛/未评估 | 全日 + 对照 SNX；或 [pride-pppar](./pride-pppar.md) |
| 6 | Docker 命令失败 | 本机无 daemon | 改预编译；或装 Docker 后再拉 `gnssanalysis/ginan:v4.1.4` |
| 7 | `vcpkg` 编数小时/内存炸 | 依赖巨 | 优先预编译/Docker |
| 8 | 期望直接出 STEC 产品 | 例程 Ionospheric=0 | 读 `Docs/ionosphere.md` 改配置；TEC 产线 → [pytecgg](./pytecgg.md) |
| 9 | Windows `.POS` 约 2.1 GB 截断 | 上游已知限制 | 大任务用 Linux/Docker |
| 10 | 与 [rtklib](./rtklib.md) 坐标对不上 | 模型/产品/参考架不同 | 同产品同站再比；看 TRACE 警告 |
| 11 | `getData.sh` 要 `wget` | 脚本写死 wget | `apt install wget` 或改用本文 curl |
| 12 | 实时例无流 | 需 NTRIP/网络账户 | 先事后例；实时见 `rt_ppp_example.yaml` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| GA 现代化 PPP/POD/YAML 工具箱 | **本文 Ginan** |
| 轻量事后 RTK/PPP CLI | [rtklib](./rtklib.md) |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| Python 开放 PPP-RTK | [cssrlib](./cssrlib.md) |
| Pi 基站 + Web/NTRIP | [rtkbase](./rtkbase.md) |

## 8. 相关

[rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [cssrlib](./cssrlib.md) · [rtkbase](./rtkbase.md) · [gampii-good](./gampii-good.md) · [data-access](../data-access.md) · [README](./README.md)

- 引用：ION 2024 Pacific PNT（README “How to cite”）
- 例程说明：`exampleConfigs/README.md`
