# IRI-COMMON-FILES · 官方公共 CCIR/URSI 系数目录操作手册

目录：[`PROJECTS.json` → `IRI-COMMON-FILES`](../../PROJECTS.json) · 门户 <https://irimodel.org/COMMON_FILES/> · 本机复拉 **2026-09-24 06:15 EDT**：`00_ccir-ursi.zip` **351 482** B，sha256=`5427353c578f7cdae9d6f3041ba9a8f3a1ce855732c70f64f77ec5f81963466a`（sha₁₂=`5427353c578f`）· **24** 文件：`ccir11–22.asc` + `ursi11–22.asc` · 与 IRI-2026 包内同名文件本机 **byte 一致** · **质检复跑** 2026-09-24 06:19 EDT（复拉 zip **351482**/sha₁₂=`5427353c578f` 与本地 **byte 一致**；`unzip -l` **24** 文件/无子目录；`cmp` vs [iri-2026-package](./iri-2026-package.md) 内同名 **24/24**；HEAD zip **CL=351482**/门户索引 mtime **2023-10-29**；tar **CL=921600**；散 `.asc` 索引多标 **2013-04**；**未臆造** Ne/TEC→[iri-fortran](./iri-fortran.md)）

> 岗位：讲清 **何时必须另下** 这套公共系数、文件放哪、以及 **混年版** 的坑。冲突时：**irimodel 说明 / 目标版本 `00readme.txt` > 本文**。编译跑数见 [iri-fortran](./iri-fortran.md)；2026 整包清单见 [iri-2026-package](./iri-2026-package.md)。

## 1. 用途与边界

**做：**

- 为 **IRI-2016 及更早**（及任何**未**把系数打进版本 zip 的树）补齐 `ccir%%.asc` / `ursi%%.asc`
- 核 `00_ccir-ursi.zip`（或 `.tar`）checksum，并确认解压到与 `.for` **同一运行目录**
- 对照 2020+/2026：系数已在版本包内时，本目录变为**校验/补缺**源，而非第二套“更新通道”

**不做：**

- **不是** 太阳/地磁指数 → [indices](https://irimodel.org/indices/)（`apf107.dat` / `ig_rz.dat`）；与 COMMON_FILES **无关**
- **不** 提供 Ne/TEC 金标准数字 → 引用 [iri-fortran](./iri-fortran.md)
- **不是** PyIRI 自带 `coefficients/` → [pyiri](./pyiri.md)（路径约定不同，勿混拷）
- **不是** 用本目录“升级”成 IRI-2026 物理（升级靠版本包源码，不是靠换 `.asc`）

一句话：COMMON_FILES = **各版共用的 foF2 等 CCIR/URSI 月系数**；≤2016 常外置，2020+ 多已内置。

| 术语 | 含义 |
| --- | --- |
| `ccirMM.asc` | CCIR 系数；`MM`=11…22 对应月份习惯编码（与源码读名一致） |
| `ursiMM.asc` | URSI 系数；成对 12 个 |
| `00_ccir-ursi.zip` | 推荐打包（本机 **351482** B）；另有 `00_ccir-ursi.tar`（门户约 **900 KB**） |
| 运行目录 | `iritest` / `IRI_SUB` 打开系数时的 **cwd**（通常即源码目录） |

## 2. ≤2016 外置 vs 2020+ 内置

| 场景 | COMMON_FILES | INDICES | 版本 zip |
| --- | --- | --- | --- |
| IRI-2001…**2016** 典型 | **必下**到与 `.for` 同目录 | 必下 | 版本目录另下 |
| IRI-**2020** / **2026** | 已在版本 zip（24×`.asc`） | 仍必下 | 见 [iri-2026-package](./iri-2026-package.md) |
| 只克隆 GitHub 包装 | 包装可能自带旧副本 | 常自带或另拉 | 以包装 README 为准 |

本机交叉核验（2026-09-24；质检复跑 06:19 EDT **24/24 `cmp -s`**）：COMMON_FILES 全部 `ccir%%.asc`/`ursi%%.asc` 与 `IRI-2026.zip` 内同名文件 **byte 一致**——说明 2026 捆的是同一套公共系数，不是“另一代秘密文件”。因此对 2026 用户：缺文件时优先查是否漏解压 zip，而不是先怀疑 COMMON 页过期。


## 2.1 与兄弟手册分工

| 问题 | 手册 |
| --- | --- |
| zip 里有没有系数 / sha 多少 | [iri-2026-package](./iri-2026-package.md) |
| 系数从 COMMON 页怎么下、拷哪 | **本页** |
| `gfortran`、`printf` 管道、`fort.7` 金标准 | [iri-fortran](./iri-fortran.md) |
| pip xarray / 纯 Python | [iri2016](./iri2016.md) / [pyiri](./pyiri.md) |

门户 COMMON_FILES 索引里单个 `.asc` 的 Last-modified 多标 **2013-04**；打包 `00_ccir-ursi.zip` 标 **2023-10-29**（本机内容仍与 2026 包内一致）。**mtime 新 ≠ 物理模型升级**——升级 IRI 请换版本源码包。

本文 **不** 编造任何 Ne/TEC；需要数字时只引用 [iri-fortran](./iri-fortran.md) 已公布的 `fort.7` 结果。


## 3. 下载与落盘（本机已通）

```bash
mkdir -p ~/iono_ops/iri-common-files && cd ~/iono_ops/iri-common-files
UA='Mozilla/5.0'
curl -fsSL -A "$UA" -o 00_ccir-ursi.zip \
  'https://irimodel.org/COMMON_FILES/00_ccir-ursi.zip'
sha256sum 00_ccir-ursi.zip
# 期望（本机 2026-09-24 06:15 EDT）：
# 5427353c578f7cdae9d6f3041ba9a8f3a1ce855732c70f64f77ec5f81963466a  00_ccir-ursi.zip
wc -c 00_ccir-ursi.zip   # 期望：351482

unzip -l 00_ccir-ursi.zip
# 期望：24 files；ccir11–22 + ursi11–22；无子目录
mkdir -p COMMON && unzip -qo 00_ccir-ursi.zip -d COMMON
ls COMMON/ccir*.asc | wc -l   # 12
ls COMMON/ursi*.asc | wc -l   # 12
```

**接到旧版源码树（示意，路径按你的 IRI-YYYY 解压根改）：**

```bash
# 例：IRI-2016 源码目录（名称以官网包为准）
SRC=~/iono_ops/iri-2016/IRI-zip   # 或你的实际 cwd
cp -a ~/iono_ops/iri-common-files/COMMON/ccir*.asc \
      ~/iono_ops/iri-common-files/COMMON/ursi*.asc \
      "$SRC/"
# 指数仍单独：
curl -fsSL -A "$UA" -o "$SRC/apf107.dat" \
  'https://irimodel.org/indices/apf107.dat'
curl -fsSL -A "$UA" -o "$SRC/ig_rz.dat" \
  'https://irimodel.org/indices/ig_rz.dat'
ls "$SRC"/ccir*.asc "$SRC"/ursi*.asc | wc -l   # 期望：24
```

**接到 IRI-2026：** 一般 **不必**再拷；若误删系数，可从本 zip 补回，或重新解 [IRI-2026.zip](./iri-2026-package.md)。完整编译→`fort.7` → [iri-fortran](./iri-fortran.md)。

门户散挂的同名 `ccir%%.asc` / `ursi%%.asc` 与打包 zip 同源；日常用 zip 一次拉齐即可。质检复跑 HEAD：`00_ccir-ursi.tar` **CL=921600**（可选）；zip **CL=351482**。

## 4. 文件放哪（对照）

| 文件 | 放哪 | 谁读 |
| --- | --- | --- |
| `ccir%%.asc` / `ursi%%.asc` | 与 `iritest` **同一 cwd** | Fortran 打开固定文件名 |
| `apf107.dat` / `ig_rz.dat` | 同上 | `READAPF107` / `READ_IG_RZ` |
| `mcsat%%.dat` / `igrf*.dat` | 版本包内（非 COMMON_FILES） | 2020+ 默认 hmF2/IGRF |
| PyIRI `coefficients/` | 包内树；**不要**用本页 `.asc` 覆盖凑合 | [pyiri](./pyiri.md) |


## 4.1 开关侧：CCIR vs URSI（勿在本页改 JF）

IRI 用 `JF` 在 CCIR/URSI foF2 等选项间切换；**默认推荐集**写在 `irisub.for` 注释与 `iritest` 里。本页只保证磁盘上 **两套 `.asc` 都在 cwd**，避免“开关指 URSI 却缺 `ursi11.asc`”。

具体改哪一位 `JF`、以及改完如何重链——一律跟 [iri-fortran](./iri-fortran.md)，避免 companion 与金标准篇各写一套开关表。

月文件命名：源码打开的是 **`ccir11.asc`…`ccir22.asc`**（及 `ursi*`），不是 `ccir01`。丢文件时按 **11–22** 清点，不要按日历 1–12 文件名去找。


## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | ≤2016：`Cannot open file ccir11.asc` | 只下了版本包 | 解本页 zip **进源码 cwd** |
| 2 | 系数在 `~/Downloads/COMMON/`，程序仍找不到 | 相对路径只认 cwd | `cp` 进运行目录，或 `cd` 到含系数处再跑 |
| 3 | 把 COMMON_FILES 当成“2026 升级包” | 系数几乎不动；升级靠版本 `.for` | 换 [iri-2026-package](./iri-2026-package.md) 整包 |
| 4 | 2012 源码 + 2026 目录里零散 `.for` 混编 | ABI/默认 `JF`/附属 `.dat` 不一致 | **整树同一年版**；勿拣文件拼装 |
| 5 | 用 COMMON 的 `.asc` 覆盖 PyIRI 系数目录 | 格式/命名/球谐架构不同 | PyIRI 只用包内 `coefficients/` |
| 6 | 有系数仍炸在 `ig_rz.dat` | 混淆 COMMON ≠ INDICES | 另下 [indices](https://irimodel.org/indices/) |
| 7 | Windows 解压后大小写 / 扩展名被改 | 源码大小写敏感约定 | 保持小写 `.asc` 文件名 |
| 8 | 两套 IRI 共用一目录，旧 `mcsat`/`igrf` 残留 | 混年版数据文件 | 每版独立目录；指数可共享拷贝但勿混源码 |

## 6. 接到哪步

- 官方 2026 发行物清单 → [iri-2026-package](./iri-2026-package.md)
- 金标准编译跑数 → [iri-fortran](./iri-fortran.md)
- Python：[iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [pyglow](./pyglow.md)
- 教程 [04](../tutorials/04-iri-nequick.md)

## 7. 工作流（短）

1. 确认目标版本：**≤2016** → 必下本页；**2020+** → 先查版本 zip 是否已有 24×`.asc`  
2. `curl` `00_ccir-ursi.zip` → `sha256sum` → 解到源码 cwd  
3. 另下 **INDICES**（永远另步）  
4. 跳转 [iri-fortran](./iri-fortran.md) 或对应年版包装器；论文写明 **IRI-YYYY + 系数来源（包内 / COMMON_FILES）**

## 8. 选型（一行）

| 你要… | 打开 |
| --- | --- |
| 补 CCIR/URSI 公共系数 | **本页** |
| IRI-2026 zip 有无捆系数 | [iri-2026-package](./iri-2026-package.md) |
| gfortran / `fort.7` | [iri-fortran](./iri-fortran.md) |
| 不碰 Fortran | [pyiri](./pyiri.md) / [iri2016](./iri2016.md) |

门户散文件与 zip 并行提供时，优先 zip，避免漏下某一个月的 `ursi%.asc`。
