# IRI-2026-package · 官方 IRI-2026 zip 包操作手册

目录：[`PROJECTS.json` → `IRI-2026-package`](../../PROJECTS.json) · 门户目录 <https://irimodel.org/IRI-2026/> · 许可 **AS IS + attribution**（包内 `00_iri2016-License.txt`）· 本机复拉 **2026-09-24 06:15 EDT**：`IRI-2026.zip` **1 823 544** B，sha256=`2377b0c07a4332c441cf010dc50b26dde8cfd4928d0335fb9a6560dced6a8f82`（sha₁₂=`2377b0c07a43`）· 编译/跑数 **见** [iri-fortran](./iri-fortran.md)（勿在本篇重跑 `iritest`）· **质检复跑** 2026-09-24 06:19 EDT（复拉 zip **1823544**/sha₁₂=`2377b0c07a43` 与本地 **byte 一致**；`unzip -l` **69** 条目/解压 **68** 文件/合计 **5974782** B；ccir+ursi **24**；包内无 `apf107`/`ig_rz`；`apf107` **1402576**/`ig_rz` **10559** 仍对齐；HEAD tar **CL=6025728**/zip mtime **2026-08-07**；与 [iri-common-files](./iri-common-files.md) `cmp` **24/24**；**未重跑** `iritest`/`fort.7`→引用 [iri-fortran](./iri-fortran.md)）

> 岗位：核对 **IRI-2026 发行物**里有什么、没有什么，以及和 **INDICES / COMMON_FILES / 旧版目录** 的边界。冲突时：**`00readme.txt` / irimodel 目录页 > 本文**。端到端 gfortran→`fort.7` 金标准数字只引用 [iri-fortran](./iri-fortran.md)。

## 1. 用途与边界

**做：**

- 从官方目录取 **IRI-2026.zip**（或同内容 `IRI-2026.tar`）并核 checksum
- 弄清 zip 内已捆 **CCIR/URSI**、IGRF、MCSAT、源码；**永不**含最新太阳/地磁指数
- 选型：官方 2026 包 vs 旧版包 vs Python 包装

**不做：**

- **不** 重复 [iri-fortran](./iri-fortran.md) 的 `gfortran` 链命令与 `fort.7` 剖面逐步跑法
- **不** 替代 [iri-common-files](./iri-common-files.md)（≤2016 另下公共系数时的专页）
- **不是** 纯 Python / pip 驱动 → [pyiri](./pyiri.md) / [iri2016](./iri2016.md)
- **不是** Galileo NeQuick-G → [nequickg](./nequickg.md)

一句话：本页 = **发行物清单 + 下载核验**；算数请跳 [iri-fortran](./iri-fortran.md)。

| 术语 | 含义 |
| --- | --- |
| `IRI-2026.zip` | 推荐下载；解出顶层目录 **`IRI-zip/`** |
| `IRI-2026.tar` | 同批内容的 tar（更大；门户约 **5.7 MB**） |
| INDICES | `https://irimodel.org/indices/` 的 `apf107.dat` / `ig_rz.dat`；**不进版本 zip** |
| COMMON_FILES | ≤2016 常另下的 `ccir%%.asc`/`ursi%%.asc`；**2020+ 已打进版本 zip** |
| 目录散文件 | 门户 `/IRI-2026/` 还挂了单个 `.for`/`.dat`；**系数 `.asc` 只在 zip 内** |

## 2. 包内有什么 vs 没有什么

本机 `unzip -l IRI-2026.zip`：**69** 条目（含 `IRI-zip/` 目录），解压后 **68** 个文件；质检复跑合计解压 **5974782** B。

| 组 | 本机 zip 内 | 说明 |
| --- | --- | --- |
| 许可 / 说明 | `00_iri2016-License.txt`、`00readme.txt` | 许可文件名仍带 2016 字样，以内容为准 |
| 主源码 | `irisub.for` `irifun.for` `iritec.for` `iridreg.for` `iriflip.for` `iritest.for` | `00readme` 链命令所列 |
| 附属物理 | `igrf.for` `cira.for` `rocdrift.for` | IGRF / NRLMSIS-00 / 赤道漂移 |
| IRTAM 钩子 | `irirtam.for` `irirtam-test.for` | **在 zip 内**；门户 HTML 目录列表未必逐条列出 |
| CCIR/URSI | `ccir11.asc`…`ccir22.asc` + `ursi11`…`ursi22`（**24**） | **已捆**；与 [COMMON_FILES](./iri-common-files.md) 同名文件本机 **byte 一致** |
| IGRF 系数 | `dgrf1945.dat`…`dgrf2020.dat`、`igrf2025.dat`、`igrf2025s.dat` | 磁坐标 |
| Shubin hmF2 | `mcsat11.dat`…`mcsat22.dat`（12） | 月系数 |
| 其它数据 | `ibp_emp_coeffs.dat` | 包内经验系数 |
| **INDICES** | **无** `apf107.dat` / **无** `ig_rz.dat` | 必须另下 [indices](https://irimodel.org/indices/) |

对照门户 HTML 索引（2026-09-24 抓取）：可见 zip/tar、多数 `.for`、`dgrf*`/`mcsat*`/`ibp_*`；**看不到** `ccir*`/`ursi*` 散文件——它们只在压缩包里。勿以为“目录页没列系数 = 包也不带”。

| 构件 | IRI-2016 及更早 | **IRI-2026**（本页） |
| --- | --- | --- |
| 版本 zip | 要下 | 要下（本机 **1823544** B） |
| COMMON_FILES | **常另下** | **已在 zip**（仍可对照 [iri-common-files](./iri-common-files.md)） |
| INDICES | **必下且常更新** | **同上**（本机 `apf107.dat` **1 402 576** B / `ig_rz.dat` **10 559** B） |


## 2.1 门户目录页 vs zip（易混）

门户 <https://irimodel.org/IRI-2026/> 是 **Apache 风格索引**：可见 `IRI-2026.zip` / `IRI-2026.tar`、多数 `.for`、`dgrf*`、`mcsat*`、`ibp_emp_coeffs.dat` 等散文件（本机抓取时目录项 mtime 多标 **2026-07-31**，zip/tar **2026-08-07**）。

| 只看 HTML 索引时 | 实际 |
| --- | --- |
| 不见 `ccir*`/`ursi*` | **在 zip 内**（24 个） |
| 不见 `irirtam*.for` | **在 zip 内** |
| 不见 `apf107`/`ig_rz` | **正确**：指数在 [/indices/](https://irimodel.org/indices/) |
| 可逐个 `curl` `.for` | 可行但易漏附属 `.dat` → **优先整包 zip** |

`00readme.txt` 仍写经典 `f77 -o iri iritest.for … rocdrift.for` 列表；现代机用 `gfortran -std=legacy` 的完整命令 **只维护在** [iri-fortran](./iri-fortran.md)，本页不复制以免双源漂移。


## 3. 下载 + checksum（本机已复拉）

```bash
mkdir -p ~/iono_ops/iri-2026-package && cd ~/iono_ops/iri-2026-package
UA='Mozilla/5.0'
curl -fsSL -A "$UA" -o IRI-2026.zip \
  'https://irimodel.org/IRI-2026/IRI-2026.zip'
# 可选同批 tar（更大）：
# curl -fsSL -A "$UA" -o IRI-2026.tar \
#   'https://irimodel.org/IRI-2026/IRI-2026.tar'
sha256sum IRI-2026.zip
# 期望（本机 2026-09-24 06:15 EDT 复拉，与 iri-fortran 验包一致）：
# 2377b0c07a4332c441cf010dc50b26dde8cfd4928d0335fb9a6560dced6a8f82  IRI-2026.zip
# 字节：1823544
wc -c IRI-2026.zip

# 指数（不在 zip 内）
curl -fsSL -A "$UA" -o apf107.dat \
  'https://irimodel.org/indices/apf107.dat'
curl -fsSL -A "$UA" -o ig_rz.dat \
  'https://irimodel.org/indices/ig_rz.dat'
ls -la apf107.dat ig_rz.dat
# 期望量级：apf107 ≈1.3–1.4 MB；ig_rz ≈10 KB（门户会随日期改 mtime）

unzip -l IRI-2026.zip | tail -3
# 期望末行附近：69 files / 解压合计 5974782 B（≈5.97 MB）
unzip -qo IRI-2026.zip
ls IRI-zip/ccir*.asc IRI-zip/ursi*.asc | wc -l   # 期望：24
ls IRI-zip/apf107.dat IRI-zip/ig_rz.dat 2>&1 | head -2
# 期望：No such file（指数需 cp 进来，见下）
cp -a apf107.dat ig_rz.dat IRI-zip/
```

**门户并行体积（质检复跑 HEAD）：** `IRI-2026.tar` **CL=6025728**（Last-Modified **2026-08-07**）；zip **CL=1823544** 同日；zip 仍是日常首选。

编译与 `iritest`→`fort.7` **整段命令与金标准数字** → [iri-fortran §3–4](./iri-fortran.md)（本机曾得 NmF2=**893124.7** / hmF2=**259.16** / Ne@250=**886713** / TEC=**25.8**；本文不重跑、不另造剖面）。

## 4. 输入输出速查（包级）

| 输入 | 约定 |
| --- | --- |
| 运行 cwd | 解压后的 **`IRI-zip/`**（系数与指数同目录） |
| 系数名 | 源码读 **`ccir%%.asc` / `ursi%%.asc`**（不是旧文档 `.DAT` 口头名） |
| 指数 | `ig_rz.dat` + `apf107.dat` 必须在 cwd |

| 输出 | 位置 |
| --- | --- |
| `iritest` 表 | **`fort.7`**（细节见 [iri-fortran](./iri-fortran.md)） |
| 许可归属 | 论文/分发保留 `00_iri2016-License.txt` 要求 |

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 只下了目录里单个 `.for`，跑起来缺 `ccir11.asc` | 散文件列表**不含**系数 | 下 **整包 zip**，不要手拼半套 |
| 2 | zip 解完仍 `Cannot open ig_rz.dat` | 指数**永不进**版本包 | 从 [indices](https://irimodel.org/indices/) 另下并 `cp` 进 `IRI-zip/` |
| 3 | 以为 2026 还要再下 COMMON_FILES | 2020+ 已捆 24×`.asc` | 可跳过；≤2016 才必看 [iri-common-files](./iri-common-files.md) |
| 4 | 用 2016 pip 包对照“官方 2026”逐层咬死 | 版本/默认 `JF` 不同 | 论文写 **IRI-2026**；数值以 [iri-fortran](./iri-fortran.md) 为准，勿强行对齐 [iri2016](./iri2016.md) |
| 5 | `IRI-2026.tar` 与 zip 混用两套解压目录 | 重复树 / 旧指数残留 | 固定一种格式；指数每次显式覆盖 |
| 6 | 门户 zip 更新后本机旧 sha 对不上 | 工作组换包 | 重拉并改笔记里的 sha/字节；勿死记过期 hash |
| 7 | 找到 `irirtam.for` 却当气候态默认路径 | IRTAM 是同化钩子 | 气候态用 `iritest`/`IRI_SUB`；同化见 [pyirtam](./pyirtam.md) |
| 8 | 西经 / UT+25 / 表在 stdout | 驱动约定 | 全部按 [iri-fortran §5–6](./iri-fortran.md)，本页不重复 |

## 6. 接到哪步

- **编译 + 真跑剖面** → [iri-fortran](./iri-fortran.md)
- ≤2016 公共系数 / 混年版 → [iri-common-files](./iri-common-files.md)
- Python：[iri2016](./iri2016.md)（2016 Fortran→xarray）· [pyiri](./pyiri.md)（纯 Python，自带系数）· [pyglow](./pyglow.md)
- 概念课 [04](../tutorials/04-iri-nequick.md) · 数据 [data-access](../data-access.md)

## 7. 工作流（短）

1. `curl` **IRI-2026.zip** → `sha256sum` / `wc -c` 对照本页本机值（或门户更新后的新值）  
2. `unzip` → 确认 **24** 个 `ccir`/`ursi`；**另下** indices 拷进 `IRI-zip/`  
3. 跳转 [iri-fortran](./iri-fortran.md) 完成 `gfortran` 与 `fort.7`  
4. 写论文锁定：**包日期 + sha 或 mtime + JF 默认**；需要 xarray 再桥包装器并声明版本差

## 8. 选型（一行）

| 你要… | 打开 |
| --- | --- |
| 官方 2026 发行物核验 | **本页** |
| 本机编译跑数 | [iri-fortran](./iri-fortran.md) |
| 旧版另下 CCIR/URSI | [iri-common-files](./iri-common-files.md) |
| pip / 纯 Python | [iri2016](./iri2016.md) / [pyiri](./pyiri.md) |
