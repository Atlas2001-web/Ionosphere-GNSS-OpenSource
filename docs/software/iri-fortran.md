# IRI-Fortran · 官方 IRI Fortran（irimodel.org）操作手册

目录：[`PROJECTS.json` → `IRI-Fortran`](../../PROJECTS.json) · 门户 <https://irimodel.org/> · 本篇验版 **IRI-2026**（目录标注 **07/31/2026**；包内 `iritest.for` 注释 **2026.02**）· 许可 **AS IS + attribution**（包内 `00_iri2016-License.txt`）· 本机验证：拉 `IRI-2026.zip`（**1 823 544** B，sha256₁₂=`2377b0c07a43`）+ `indices/{apf107,ig_rz}.dat` → **gfortran 14.2** 链出 `iri` → `iritest` 管道驱动 → `fort.7`：**(40°N, 80°W)** 2015-03-23 **15.5 UT**，100–500 km / 50 km → NmF2=**893124.7** cm⁻³ / hmF2=**259.16** km / Ne@250=**886713** / TEC(60–2000)=**25.8** TECU · 2026-09-24 06:12 EDT

> 岗位：装 **COSPAR/URSI 官方 Fortran 金标准**，作论文复现 / 包装对照。冲突时：**`00readme.txt` / irisub 注释 / 门户 FAQ > 本文**。Python 快捷：已短硬 [iri2016](./iri2016.md)（IRI-2016 驱动）/ [pyiri](./pyiri.md)（纯 Python）/ [pyirtam](./pyirtam.md)（同化）/ [pyglow](./pyglow.md)。概念课 [04](../tutorials/04-iri-nequick.md)。

## 1. 用途与边界

**做：**

- 下载版本包（**IRI-2026** / IRI-2020 / …）+（按版本需要）**COMMON_FILES** + 最新 **INDICES**
- 用 `iritest.for`（或自写驱动调 `IRI_SUB` / `IRI_WEB`）算气候态 Ne/Te/Ti/Ni、峰值、vTEC
- 对照包装器是否跟得上工作组默认开关（`JF(50)`）

**不做：**

- **不是** 当日实况天气场 / GIM → [ionex-gim](./ionex-gim.md)；同化 → [pyirtam](./pyirtam.md) 或包内 `irirtam.for`
- **不是** Galileo 单频 NeQuick-G → [nequickg](./nequickg.md)；ICTP NeQuick 2 → [nequick2-ictp](./nequick2-ictp.md)
- **不是** 闪烁物理或业务单频改正引擎
- 本页 **不** 声称拥有 SH-GIM / PyTECGg

一句话：IRI-Fortran = **官方气候态电离层国际标准源码入口**；包装方便，金标准仍以本树 + 指数为准。

| 术语 | 含义 |
| --- | --- |
| `JF(50)` | 逻辑开关；默认见 `irisub.for` / `iritest`（例：foF2=URSI、hmF2=Shubin、Te=TBPS-2026） |
| `IRI_SUB` | 单点高度剖面主例程；`OUTF(20,1000)` / `OARR(100)` |
| `IRI_WEB` | 沿 lat/lon/year/… 扫参（`iritest` 调用） |
| COMMON_FILES | 各版共用 CCIR/URSI 系数目录；**≤IRI-2016** 常需另下 |
| INDICES | `ig_rz.dat`（IG12/Rz12）+ `apf107.dat`（ap/F10.7）；**永不进版本包** |
| `fort.7` | `iritest` 标准表输出（stdout 只有提示） |

## 2. 包边界：版本目录 · COMMON_FILES · INDICES

| 构件 | URL | IRI-2016 及更早 | IRI-2020 / **IRI-2026** |
| --- | --- | --- | --- |
| 版本源码+IGRF+MCSAT+… | `https://irimodel.org/IRI-YYYY/` | 要下 | 要下（2026：`IRI-2026.zip`） |
| CCIR/URSI 系数 | [COMMON_FILES](https://irimodel.org/COMMON_FILES/) | **必下**（`.asc`） | **已打进 zip**（本机 12+12×`ccir%%.asc`/`ursi%%.asc`） |
| 太阳/地磁指数 | [indices](https://irimodel.org/indices/) | **必下且常更新** | **同上**（本机 `apf107.dat` **1 402 576** B / `ig_rz.dat` **10 559** B） |
| 日更镜像（可选） | ECHAIM `apf107.dat` / `ig_rz.dat` | 业务复现建议 | 业务复现建议 |

目录对照（`PROJECTS.json`）：门户总入口 **`IRI-Fortran`**；单版 **`IRI-2026-package`**；公共系数 **`IRI-COMMON-FILES`**；指数 **`IRI-indices`**。本手册覆盖总入口，验跑落在 **2026** 包。

## 3. 安装 / 获取（本机已通）

```bash
sudo apt-get install -y gfortran   # 本机已有：GNU Fortran 14.2.0
mkdir -p ~/iono_ops/iri-fortran && cd ~/iono_ops/iri-fortran
UA='Mozilla/5.0'
curl -fsSL -A "$UA" -o IRI-2026.zip \
  'https://irimodel.org/IRI-2026/IRI-2026.zip'
curl -fsSL -A "$UA" -o apf107.dat \
  'https://irimodel.org/indices/apf107.dat'
curl -fsSL -A "$UA" -o ig_rz.dat \
  'https://irimodel.org/indices/ig_rz.dat'
# ≤2016 另加：curl …/COMMON_FILES/00_ccir-ursi.zip && unzip …
unzip -qo IRI-2026.zip          # 解出 IRI-zip/
cd IRI-zip
cp -a ../apf107.dat ../ig_rz.dat .
ls ccir*.asc ursi*.asc | wc -l  # 期望：24
```

编译（官方 `00readme.txt` 的 `f77` 列表；本机用 `gfortran -std=legacy`）：

```bash
cd ~/iono_ops/iri-fortran/IRI-zip
gfortran -O2 -std=legacy -ffixed-line-length-none -o iri \
  iritest.for irisub.for irifun.for iritec.for iridreg.for \
  igrf.for cira.for iriflip.for rocdrift.for
ls -la iri
# 期望：可执行文件（本机 ≈1.6 MB）；igrf.for 可能刷越界 Warning，可忽略
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ig_rz.dat: No such file` | 指数未拷进运行目录 | `cp ../ig_rz.dat ../apf107.dat .` |
| `ccir11.asc` 找不到 | ≤2016 漏 COMMON_FILES | 下并解压到**同一 cwd** |
| 链接缺 `rocdrift` | 2020+ 赤道漂移独立文件 | 把 `rocdrift.for` 加入链命令 |

## 4. 端到端：`iritest` → `fort.7`（本机真跑）

对齐 [iri2016](./iri2016.md) 同点：**地理** 40°N / 80°W（东经输入 **−80** 或 **280**）、2015-03-23 **15.5 UT**、高度变量 100→500 km 步长 50、标准表、TEC 60–2000 km、**默认 JF**。

```bash
cd ~/iono_ops/iri-fortran/IRI-zip
rm -f fort.7
printf '%s\n' \
  '0,40.0,-80.0' \
  '2015,0323,1,15.5' \
  '250.0' \
  '1' \
  '100.0,500.0,50.0' \
  '0' \
  '60.0,2000.0' \
  '0' \
  '0' | ./iri >iritest_stdout.txt 2>&1
# 交互末行：Enter 0 to exit → 必须再喂一个 0（勿喂 n）
sed -n '1,55p' fort.7
```

**本机 `fort.7` 要点（2026-09-24 06:12 EDT，IRI-2026 / gfortran 14.2）：**

```text
yyyy/mmdd(or -ddd)/hh.h):2015/ 323/15.5UT  geog Lat/Long/Alt= 40.0/ 280.0/ 250.0
Peak Densities/cm-3: NmF2= 893124.7   NmF1= 254768.3   NmE= 140870.7
Peak Heights/km:     hmF2=   259.16   hmF1=   153.38   hmE=   110.00
Solar radio flux F10.7 (daily)                        127.2
TEC … from    60.0 to  2000.0 km …
  100.0 113860 …
  250.0 886713 …
  500.0 207921 …
```

对照：同点 [iri2016](./iri2016.md)（IRI-**2016** 包装）NmF2≈**893124.7** cm⁻³ 对齐，但 hmF2/Ne 剖面因版本与默认 `JF`（本包 Shubin + COR2 topside + TBPS-2026 Te）而**不必**逐层相等——写论文请写明 **IRI-2026 + 默认开关**。

### 4.1 最小自写驱动长什么样（结构示意，勿抄虚假数值）

任何调用都必须先读指数，再清 `OARR`，再设 `JF` 默认，再调 `IRI_SUB`。UT 进 `IRI_SUB` 时 **`DHOUR = UT + 25`**（见 `irisub` 注释；`iritest` 已替你换算）。

```fortran
c 示意：与 iritest 同依赖列表编译；勿当可独立粘贴的“验证答案”
      LOGICAL JF(50)
      REAL OUTF(20,1000), OARR(100)
      DO I=1,50
        JF(I)=.TRUE.
      END DO
      JF(4)=.FALSE.   ! 与 iritest 默认一致的关键几项（完整表见源码）
      JF(5)=.FALSE.
      JF(6)=.FALSE.
      JF(23)=.FALSE.
      JF(30)=.FALSE.
      JF(33)=.FALSE.
      JF(35)=.FALSE.
      JF(39)=.FALSE.
      JF(40)=.FALSE.
      CALL READ_IG_RZ
      CALL READAPF107
      DO I=1,100
        OARR(I)=-1.0
      END DO
      CALL IRI_SUB(JF,0,40.0,280.0,2015,323,15.5+25.0,
     &             100.0,500.0,50.0,OUTF,OARR)
c OUTF(1,*)=Ne[m-3]；OARR(1)=NmF2 … 细节见门户 IRI-output-arrays
      END
```

## 5. 输入输出速查

| 输入 | 约定 |
| --- | --- |
| `JMAG` | `0` 地理 / `1` 地磁 |
| `ALONG` | **东经**；西经可用负值（本机 −80→表头 280） |
| `MMDD` | `0323` 或负 DOY |
| `iritest` 的 `iut` | `0`=LT / `1`=UT |
| 系数文件名 | 源码读 **`ccir%%.asc` / `ursi%%.asc`**（非旧文档里的 `.DAT` 字样） |

| 输出 | 位置 / 单位 |
| --- | --- |
| 标准表 | **`fort.7`**（非 stdout） |
| Ne 列 | **cm⁻³**（表头）；`OUTF(1,*)` 为 **m⁻³** |
| TEC | `OARR`/`fort.7`：**1×10¹⁶ m⁻²** = TECU |
| 消息 | `jf(12)=t`→stdout；`f`→`MESSAGES.TXT` |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Fortran runtime error: Bad integer` 在退出提示后 | 末行喂了 `n`/`y` | 再喂整数 **`0`** 退出 |
| 2 | 算完了但终端无剖面 | 表写在 **unit 7** | `cat fort.7` |
| 3 | `Cannot open file ig_rz.dat` | 指数不在 cwd | `cp …/indices/*.dat .` |
| 4 | ≤2016 缺 `ccir11.asc` | COMMON_FILES 未合并 | 下 [COMMON_FILES](https://irimodel.org/COMMON_FILES/) 解到同目录 |
| 5 | 与 `iri2016` pip 剖面差一截 | **版本/JF 默认不同** | 论文写清 IRI-YYYY + JF；勿强行逐层对齐 |
| 6 | `gfortran` 一堆 `Array reference out of bounds` | `igrf.for` 旧式固定维 | `-std=legacy` 继续链；本机已出可执行文件 |
| 7 | TEC 离谱 / 指数像“过期气候” | `apf107`/`ig_rz` 太旧 | 重拉 [indices](https://irimodel.org/indices/) 或 ECHAIM 日更 |
| 8 | 直接调 `IRI_SUB` 时间错 25 h | 忘了 UT+25 | `DHOUR = UT + 25.0`；或继续用 `iritest`/`IRI_WEB` |
| 9 | 西经写成 `80` 当东经 | 经度约定 | 用 **−80** 或 **280** |
| 10 | 想改 topside/Te 却“没变化” | 未改 `JF` 或改后未重链 | 对照 `iritest` 默认块；改 `.for` 后重 `gfortran` |

## 7. 接到哪步

- 气候态对照实测 TEC/GIM：[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · 教程 [04](../tutorials/04-iri-nequick.md)
- 快速 Python：[iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [pyglow](./pyglow.md)；同化 [pyirtam](./pyirtam.md)
- 在线点算（无本地 Fortran）：CCMC IRI 页面（门户链出）；本地金标准仍以本树为准
- 数据入口：[data-access](../data-access.md)

## 8. 工作流（短）

1. 下 **IRI-2026.zip** + **indices**（≤2016 再加 COMMON_FILES）→ 解压并把指数拷进源码目录  
2. `gfortran … -o iri`（九个 `.for`）  
3. `printf` 管道跑 `iritest` → 读 **`fort.7`**  
4. 写进论文/对照脚本时锁定 **版本日期 + JF 默认**；需要 xarray 再桥 [iri2016](./iri2016.md)/自写读 `OUTF`
