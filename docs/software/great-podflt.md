# GREAT_PODFLT · 武大实时滤波精密定轨（PODFLT）操作手册

目录：[`PROJECTS.json` → `GREAT_PODFLT`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT_PODFLT> · tip **`bd9fb71`**（`Update README.md` 2026-08-06）· tag **`v1.0.0`** → **`902bee5`** · **GPL-3.0**（PDF §2.2；GitHub license 字段空）· ★**17** · C++14/CMake · 本机验证（2026-09-24 07:04–07:10 EDT）：`g++ 14.2.0` + `cmake 3.31.6` + **`-DUSE_OPENMP=ON`** → `src/build/Bin/great_podflt` **9641192** B + 静态库 `Lib/liblib{GREAT,GNut}.a`（**10732088** / **10111660** B）；`-h`/`-V 1` → **`GREAT/POD_FLT [0.9.0]`**（`$Rev: 2448 $`，源码编于 **Sep 24 2026 11:08:54**）；缺 XML → `xconfig: not file read … File was not found`（exit **0**）；仓内 `sample/.../xml/podflt.xml` 含字面 `/<install_dir>/` → **Start-end tags mismatch** exit **1**；替换占位并指向 `utils/gnss_sys_file/` 后 `-brdm` 空跑：系统文件可读，`/home/iGMAS/...` OBS/NAV/DCB/SNX 全缺 → **88**×`.21o` Incomplete header + **27**×`can not get the xyz from sp3 or rinexn` → exit **1**；落 `logger/great_podlflt.log` **14062** B（≠ XML 写的 `LOGRT.log`）；**无** 新 `orb_*` / `.SP3` → **未臆造** POD；仓内参考 SP3（GPS）**16375106** B / **241957** 行 / 历元 **8641** / PG01 首行 `−13135.440185 13798.701066 18084.192806` / sha₁₂=`c22334bd0d0e`；`orb_*` 为 **Git LFS 指针**（**134** B → 目标 **280719358** B）；PDF **8520528** B

> 岗位：**多 GNSS 滤波精密定轨（POD）**（SRIF；双频无电离层；可选模糊度固定 / EOP / 收发钟同步）→ 产出 SP3 + ORB，供 orbdif ACR 评估与下游 PPP。冲突时：**本机 `great_podflt -h` / `doc/GREAT_PODFLT.pdf` / 样例 `xml/podflt.xml` / 上游 README > 本文**。  
> 同链钟差 → [great-pce](./great-pce.md)；UPD/IFCB → [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)；多 AC 综合 → [clkcomb](./clkcomb.md)/[spocc](./spocc.md)；产品门户 → [data-access](../data-access.md)「SP3 / CLK / bias」。下游 PPP → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)。**≠** 终端定位主引擎。

## 1. 用途与边界

**做：**

- 多 GNSS（**GPS / GLONASS / Galileo / BDS-2/3**）**滤波精密定轨**（Square Root Information Filter, SRIF）
- XML 驱动 CLI：`great_podflt -x podflt.xml [-brdm]`；CMake 编 LibGREAT + LibGNut（捆 Eigen/zlib/pugixml/newmat）
- 力模型：非球形引力、N 体、固体潮/海潮、ECOM2 光压、天线推力等；Adams 积分；LAMBDA 模糊度
- 输出 **SP3** 精密星历 + **ORB** 轨道状态；辅工具 `utils/orbdif/linux/great_orbdif` 做 ACR 残差
- 用户手册 `doc/GREAT_PODFLT.pdf`（**8520528** B）；四系统样例目录 `sample/podflt_ambfix_{G,E,C,R}_2021210/`

**不做：**

- **不是** 精密钟差估计 PCE → [great-pce](./great-pce.md)；**不是** UPD/IFCB → [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)
- **不是** 多 AC 轨道/钟综合 → [clkcomb](./clkcomb.md)/[spocc](./spocc.md)；**不是** 终端 PPP/RTK → [great-pvt](./great-pvt.md)
- GitHub tip **不带**全球网 OBS/NAV（XML 仍写 `/home/iGMAS/...`）→ **禁止**把空跑日志当真 SP3/ORB
- `orb_*` 需 **Git LFS**；本机无 LFS → 仅指针，**勿**当 ORB 产品喂 orbdif

一句话：**GREAT_PODFLT = 武大 GREAT 开源实时滤波精密定轨器**（POD 本体；PCE/UPD 是同栈旁路）。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** GREAT_PODFLT | 滤波精密定轨 CLI | `great_podflt -x …` → SP3 / ORB |
| [great-pce](./great-pce.md) | 精密卫星钟差估计 | `GREAT_PCE -x …` → `clk_*` |
| [great-upd](./great-upd.md) / [great-ifcb](./great-ifcb.md) | UPD / IFCB | `GREAT-UPD` / `GREAT-IFCB` |
| [clkcomb](./clkcomb.md) / [spocc](./spocc.md) | 多 AC 钟/轨综合 | `clkcomb` / SPOCC 登记墙 |
| [ginan](./ginan.md) / [groops](./groops.md) | 大型 POD/产品套件 | 非 GREAT 滤波章 |
| 官方 IGS SP3 | 现成产品 | CDDIS；本工具自产 `GRT0…SP3` |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++`≥7（本机 14.2）+ `cmake`≥3.5 + GNU `make` | 源码编译 |
| OpenMP（`libgomp`） | **必须** `-DUSE_OPENMP=ON`，否则链接 `omp_*` 失败 |
| 捆在 `third-party/{Eigen,zlib}` | Linux 默认路径已写死相对 `src/` |
| `utils/gnss_sys_file/`（仓内已带） | ATX/DE405/EGM/ERP/潮汐等 |
| CDDIS Earthdata / 自备全球网 OBS+brdm（可选） | 真跑 POD；见 [data-access](../data-access.md) |
| Git LFS（可选） | 拉取 `orb_*` 真文件（≈280 MB/套） |

### Linux 源码（本机已通；推荐）

```bash
sudo apt install -y build-essential cmake libgomp1   # 本机已有 g++ 14.2.0 / cmake 3.31.6
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GREAT-WHU/GREAT_PODFLT.git
cd GREAT_PODFLT
git rev-parse --short HEAD   # 本机：bd9fb71

cd src && mkdir -p build && cd build
# 默认 USE_OPENMP=OFF 仍会 -fopenmp 编译 → 链接缺 omp_*；务必 ON：
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_OPENMP=ON
make -j$(nproc)              # 产物在本目录 Bin/（非 build_Linux/）
ls -la Bin/great_podflt      # 本机：9641192 B
# 本机为静态 liblibGREAT.a / liblibGNut.a + 动态 libgomp —— 一般无需 LD_LIBRARY_PATH
# （对照 great-pce / great-upd 的 .so + LD_LIBRARY_PATH 坑）
./Bin/great_podflt -h
```

**本机 `-h`：**

```text
GREAT/POD_FLT [0.9.0] compiled: Sep 24 2026 11:08:54 ($Rev: 2448 $)

Usage: 

    -h|--help              .. this help                          
    -V int                 .. version                            
    -v int                 .. verbosity level                    
    -x file                .. configuration input file           
    --                     .. configuration from stdinp          
    -l file                .. log output file                    
    -X                     .. output default configuration in XML
```

可执行文件名是 **`great_podflt`（全小写 + 下划线）**，不是 `GREAT_PODFLT` / `GREAT-PODFLT`。PDF/README 写 `util/`，仓内实际目录是 **`utils/`**。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `undefined reference to omp_get_*` / `GOMP_parallel` | 未开 OpenMP 链接 | `cmake … -DUSE_OPENMP=ON` 后重编 |
| `Start-end tags mismatch` | XML 含 `/<install_dir>/` 被解析成标签 | 换成真实绝对路径（勿留尖括号占位） |
| `error while loading shared libraries: libgomp.so.1` | 缺 OpenMP 运行时 | `apt install libgomp1` |
| 缺 `-x` 文件仍 exit **0** | `xconfig: … File was not found` | 改路径；**勿**当成功 |
| 无 OBS 仍扫站表后 exit **1** | iGMAS 路径空 | 见 §3.2；**勿当成功 SP3** |

## 3. 端到端（本机真跑）

### 3.1 帮助 / 缺配置 / 默认 XML

```bash
BIN=~/iono_ops/GREAT_PODFLT/src/build/Bin/great_podflt
$BIN -h                 # GREAT/POD_FLT [0.9.0] …  ；exit 0
$BIN -V 1               # 同上版本行  ；exit 0
$BIN -x /tmp/no_such_podflt.xml
# → xconfig: not file read /tmp/no_such_podflt.xml File was not found  ；exit 0（注意非 1）
$BIN -X | head           # 倾倒默认 XML 骨架（gen/inputs/outputs/rec…） ；exit 0
$BIN                     # 无参：用法提示 + “check your xml file with input node…” ；exit 0
```

额外旗标（帮助未列、源码有）：**`-brdm`** → 用混合广播星历、跳过部分 `rinexc` 逻辑（`gcfg_podflt.cpp`）。

### 3.2 样例 XML 空跑（**陷阱**；本机真跑）

`sample/podflt_ambfix_G_2021210/` **只有** `xml/` + `result/`（参考 SP3/orbdif）；**无** OBS/NAV。仓内 XML 字面含 `/<install_dir>/…`（破 XML）与 `/home/iGMAS/gnss_data/...`（本机不存在）。

```bash
ROOT=~/iono_ops/GREAT_PODFLT
# 1) 原样 → 解析失败
$BIN -x $ROOT/sample/podflt_ambfix_G_2021210/xml/podflt.xml
# → xconfig: not file read … Start-end tags mismatch  ；exit 1

# 2) 替换占位为真实 ROOT，输出改到 /tmp（本机做法）
python3 - <<'PY'
from pathlib import Path
import re
root = Path.home()/"iono_ops/GREAT_PODFLT"
src = (root/"sample/podflt_ambfix_G_2021210/xml/podflt.xml").read_text()
text = src.replace("/<install_dir>/GREAT_PODFLT", str(root))
out = Path("/tmp/podflt-smoke")
for d in ("xml","logger","result"):
    (out/d).mkdir(parents=True, exist_ok=True)
text = re.sub(r"<log>\s*.*?\s*</log>", f"<log> {out}/logger/LOGRT.log </log>", text, count=1)
text = re.sub(r"<orb>\s*.*?\s*</orb>", f"<orb> {out}/result/orb_out </orb>", text, count=1)
text = re.sub(r"<sp3>\s*.*?\s*</sp3>", f"<sp3> {out}/result/out.SP3 </sp3>", text, count=1)
(out/"xml/podflt.xml").write_text(text)
print("wrote", out/"xml/podflt.xml")
PY
$BIN -x /tmp/podflt-smoke/xml/podflt.xml -brdm
# stdout 节选（本机）：
#   Reading file:///…/utils/gnss_sys_file/igs20.atx     ← 系统文件 OK
#   Reading file:///home/iGMAS/gnss_data/obs/2021/210/abpo2100.21o
#   Error: Exception opening file …/abpo2100.21o: std::exception
#   …（全球网站表逐站失败；末 brdm2100.21p 同）
# exit 1
ls -la /tmp/podflt-smoke/logger /tmp/podflt-smoke/result
# logger/great_podlflt.log  14062 B   ← 注意文件名拼写 podlflt（源码硬编码）
# result/ 空 —— 无 orb_out / out.SP3
```

**判据：** 有效产品应落在 XML `<outputs>` 的 `<sp3>` / `<orb>`，且 SP3 含 `#aP…` 头与 `PG##` 行。**无这些文件 + exit 1 = 失败**，尽管读过 ATX/DE405。

### 3.3 仓内参考 SP3（只读验收；非本机重算）

```bash
SP3=$ROOT/sample/podflt_ambfix_G_2021210/result/GRT0MGXRAP_20212100000_01D_05M_ORB.SP3
wc -c -l $SP3          # 16375106 B / 241957 行
head -8 $SP3
# #aP2021  7 29  0  0  0.00000000    8641 ORBIT IGb14 NAV GPST
# +   27   G01G02…   （27 GPS）
rg -c '^PG01' $SP3     # 8641
rg '^PG01' $SP3 | head -1
# PG01 -13135.440185  13798.701066  18084.192806      0.000000   0   0
sha256sum $SP3 | cut -c1-12   # c22334bd0d0e
head -5 $ROOT/sample/podflt_ambfix_G_2021210/result/orb_2021210
# version https://git-lfs.github.com/spec/v1
# oid sha256:c07eb1e1…  size 280719358   ← LFS 指针，非轨道体
```

E/C/R 同结构：参考 SP3 分别为 **14586401** / **16971341** / **13990166** B；各套 `orb_*` 同为 LFS 指针。

### 3.4 orbdif（预编译；本机冒烟）

```bash
ORB=$ROOT/utils/orbdif/linux/great_orbdif
chmod +x $ORB            # 克隆后默认可无执行位 → Permission denied
$ORB -h
# GREAT-orbdif [1.0.0] compiled: Apr 12 2026 10:24:05 ($Rev: 2448 $)
# Usage: -h|-V|-v|-x|-l|-X …
$ORB -x $ROOT/sample/podflt_ambfix_G_2021210/xml/orbdif.xml
# → Reading file://E:\GREAT\…\cod21683.sp3  + F:\…\orb_2021210
# → Exception opening …（Win 盘符 + LFS 空壳） ；exit 0
# 有效对比须：改 XML 为 Linux 路径 + 真 SP3 参考 + LFS 拉齐的 orb_*
```

### 3.5 自备数据真跑（本机未拉 OBS）

PDF 表 4-1：观测/导航（或 `-brdm` + brdm）、ATX/BLQ/JPL/ERP/EGM/潮汐/闰秒/satinfo/太阳地磁指数、DCB、SINEX 等。观测拉取见 [data-access](../data-access.md)。本机**未**用 CDDIS 自产新 SP3——**禁止**抄写臆造历元。

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | XML | `<gen>` 时窗/`sys`/`rec`/`int`；星座块；`<process … ambfix …>`；`<inputs>`；`<outputs>`；力模型/模糊度 |
| 入 | RINEX OBS | `<rno>` 或 process `obs_dir` 通配；样例写 `/home/iGMAS/gnss_data/obs/…` |
| 入 | RINEX NAV / brdm | `<rnn>`；CLI **`-brdm`** |
| 入 | 系统文件 | `utils/gnss_sys_file/`：`igs20.atx`、`jpleph_de405`、`EIGEN6S4`、`erp_2021_2024`、潮汐、太阳/地磁指数等 |
| 入 | DCB / SINEX | 样例 XML 指向 iGMAS `dcb/`、`snx/` |
| 出 | SP3（`<sp3>`） | 精密星历；样例名 `GRT0MGXRAP_…_ORB.SP3` |
| 出 | ORB（`<orb>`） | 轨道状态/转移；供 orbdif；**LFS** |
| 出 | 日志 | **`great_podlflt.log`**（拼写少一个 `f`；≠ XML `LOGRT.log`） |
| 辅 | ORBDIF | `great_orbdif -x orbdif.xml` → ACR 残差时序 |

**无 OBS 包时禁止抄写臆造 `PG##` 坐标当自跑结果**（可引用仓内 `result/` 参考文件并标明来源）。

## 5. 参数（XML / CLI）

| 键 / 旗标 | 本机样例（GPS `podflt.xml`） | 含义 |
| --- | --- | --- |
| `-x file` | `xml/podflt.xml` | 配置 |
| `-h` / `-V` / `-X` / `-v` / `-l` | — | 帮助 / 版本 / 默认骨架 / 详细度 / 日志 |
| `-brdm` | 本机空跑已加 | 混合广播星历路径 |
| `<beg>`/`<end>`/`<int>` | 2021-07-29 → 07-31 / **30** s | 时窗与采样 |
| `<sys>` | `GPS`（E/C/R 各套一例） | 单系统样例 |
| `<rec>` | ≈**80+** 站四字符小写 | 全球网列表 |
| `ambfix` / `fix_dd_mode` | `true` / `IND` | 模糊度固定 |
| `tropo` | 样例误写 **`ture`** | 应为 true；对照源码容错 |
| `ref_clk` | `AREG` | 参考钟站 |
| `num_threads` | `8` | OpenMP 线程 |
| `read_ofile_mode` | `REALTIME` + `obs_dir` | 仿实时读盘通配 |
| `<outputs>` 内 `sp3`/`orb`/`log` | 样例外带 `/<install_dir>/` | **必须**改绝对路径 |

`-X` 默认骨架**远简于**样例 `podflt.xml`——勿当生产模板。

## 6. 接到哪一步

```text
[data-access] 拉全球网 OBS + brdm/NAV + DCB/SNX +（复用）utils/gnss_sys_file
        ↓
  GREAT_PODFLT  →  SP3 + ORB
        ↓
  great_orbdif  →  ACR / RMS（对照 IGS/CODE SP3）
        ↓
  （旁路）great-pce 估钟 / great-upd·IFCB 偏差 / clkcomb·spocc 多 AC 综合
        ↓
  great-pvt / pride-pppar / ginan / ppp-wizard
```

POD 产品服务定位/同化；**不**替代 TEC/GIM。

## 7. 坑（≥8）

1. **`/<install_dir>/` 破 XML**：尖括号被当成标签 → `Start-end tags mismatch`；须换成真实前缀。
2. **Git 无 OBS**：样例仅 `result/` 参考 + 系统文件；XML 仍写 `/home/iGMAS/...` → 空跑 exit **1**，**无**新 SP3。
3. **`orb_*` = Git LFS**：本机 **134** B 指针（目标 ≈**280 MB**）；无 `git lfs pull` 则 orbdif 读失败。
4. **OpenMP 链接**：默认 `USE_OPENMP=OFF` 仍 `-fopenmp` 编译 → `undefined reference to omp_*`；务必 `-DUSE_OPENMP=ON`。
5. **日志名 `great_podlflt.log`**：少写一个 `f`；XML 的 `LOGRT.log` **不会**按字面出现。
6. **二进制名 / 目录**：`great_podflt` 小写；产物在 `src/build/Bin/`；辅目录是 **`utils/`** 不是 README 的 `util/`。
7. **静态库 vs 兄弟篇 `.so`**：本机 PODFLT 链 `liblib*.a`，一般**不必** `LD_LIBRARY_PATH`；但 **仍依赖 `libgomp.so.1`**。对照 [great-pce](./great-pce.md) 的 `libLibGREAT.so` 陷阱，勿混抄。
8. **orbdif 预编译**：需 `chmod +x`；样例 `orbdif.xml` 含 **Win 盘符路径**，Linux 必改。
9. **缺文件 exit 码怪**：缺 `-x` 文件 exit **0**；XML 标签错 exit **1**——脚本勿只看 0。
10. **`tropo="ture"`**：样例笔误；真跑前核对 PDF/源码期望值。
11. **≠ PCE ≠ UPD ≠ clkcomb**：POD 定轨；PCE 估钟；UPD/IFCB 相位/频间偏差；clkcomb/SPOCC 综合多 AC。
12. **规模门禁**：样例多日 × 数十站 × 30 s + 模糊度——缺内存/线程先砍 `<rec>` / `num_threads` / 时窗。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 自建多星座 **滤波精密轨道** | **GREAT_PODFLT** | SRIF POD；有 PDF/样例 SP3 |
| 自建 **精密钟差** | [great-pce](./great-pce.md) | 同 GREAT；估钟非定轨 |
| 自建 **UPD / IFCB** | [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md) | 偏差链 |
| 多 AC 钟/轨综合 | [clkcomb](./clkcomb.md)/[spocc](./spocc.md) | 合成非单 AC 滤波 |
| 大型业务 POD | [ginan](./ginan.md)/[groops](./groops.md) | 整套产品线 |
| 武大 GREAT PPP | [great-pvt](./great-pvt.md) | 消费轨道/钟差 |
| 只要分析中心 SP3 | [data-access](../data-access.md) | 不必自定轨 |
| 实时钟差/轨道/UPD 服务骨架 | `rt-clk-service`（待手册） | 同 orbit-clock 族 |

**下一步候选（目录仍缺短硬）：** **`rt-clk-service`**（PROJECTS 同 subcategory「钟差/轨道/UPD」；实时钟差/轨道/UPD/IFPB 服务）或 **`gnssanalysis`**（GA：SINEX/SP3/CLK/Bias 工具箱）——仍在 GREAT/Gkit/bias/orbit-clock 族；**勿**抢 `cggtts`/`rinex2bin` WIP；**勿建** gnssrefl/mpsim。
