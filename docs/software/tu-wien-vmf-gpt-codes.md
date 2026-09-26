# TU Wien VMF/GPT codes · 对流层映射函数与经验模型官方源码操作手册

目录：[`PROJECTS.json`](../../PROJECTS.json) → `TU-Wien-VMF-GPT-codes`（数据侧另见 `VMF-Data-Server-TropProducts` / `VMF3-GNSS-Products` / `VMF1-GNSS-Products`）· 源码区 <https://vmf.geo.tuwien.ac.at/codes/> · 数据区 <https://vmf.geo.tuwien.ac.at/trop_products/> · 维护：TU Wien 测绘与地理信息系（Böhm / Landskron 等）· **不是 git 仓库**：Apache 目录列表，无版本号、无 tag，只能按文件修改日期追溯 · 许可：源码头只有 `(c) Department of Geodesy and Geoinformation, Vienna University of Technology`，**无开源许可证文本**；数据按站点 Terms of Use（§7）

本机验证（**2026-09-26 00:32–00:39 EDT**）：GNU Octave **9.4.0**、gfortran **14.2.0**、Python **3.13.5**（numpy 2.5.3 / pandas 3.0.6）；**未装 MATLAB**。`/codes/` 顶层计 `.m`×**21** / `.f`×**9** / `.f90`×**7** / `.cpp`×**1**+`.h`×**1** / `.grd`×**5**，另有 `Python_Tools_Adavi/`（**12** 个 `.py`）、`Verification/`（本机 **403**）、`gzwd_rf/`、`vmf3o_SH/`。GRAZ 2024-01-01 00 UTC：`gpt3_5.m`（Octave）= `gpt3_5.f90`（gfortran）= `gpt3_5_fast.py`（Python）逐位一致；`vmf3_grid.m` 原样在 Octave **跑不通**，4 处补丁后出 ZTD=**2.2693** m（§4）。**质检复跑**（2026-09-26 00:45–00:48 EDT，同版本工具链）：`/codes/` 计数 `.m`21/`.f`9/`.f90`7/`.cpp`1/`.h`1/`.grd`5、`gpt3_5.grd` 1146104 B/2593 行/sha₁₂ `3bf35c611e7c`、Verification **403**；4a 全部 13 行、`fast`、F90 两行、Python 行 + `vmf3` site el=5 **10.1579/10.7460**、4c 站点 4 行与 STD、原样 `vmf3_grid` → `Invalid call to round`、照抄 §4c 的 sed（diff **8** 行）→ grid 行 `mfh=10.1590 … ZTD=2.2693` **逐字复现**；坑 2 F90 异目录 exit **0**、坑 10 FC2026 **401**/FC2025 **200**/OP 最新 `VMF3_20260924.H18` 复现。墙时本机共享负载高（load≈37/8 核），`real` 仅供参考。

> 岗位：给 PPP/VLBI/SLR 解算提供**对流层先验**——GPT3 从经纬高+日期给出气压/温度/水汽/映射系数（离线、无需气象数据）；VMF1/VMF3 用 NWM 射线追踪得到的 `ah/aw` 系数算映射函数。冲突时：**源码头注释 > 本文**。  
> 真射线追踪 → [radiate](./radiate.md)（同一团队）；把这些模型用到 SWD → [std-swd-calc](./std-swd-calc.md)；在 PPP 引擎里怎么选 → [ginan](./ginan.md) / [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)。

## 1. 用途与边界

| 术语 | 含义 |
| --- | --- |
| ZTD = ZHD + ZWD | 天顶总延迟 = 干（静力学，气压决定）+ 湿（水汽决定），GRAZ 本机 ≈ **2.27** m |
| 斜延迟 | `STD = ZHD·mf_h(el) + ZWD·mf_w(el) (+ 梯度项)`；5° 仰角时 mf≈10 |
| 映射函数 mf | 天顶→斜向放大系数。VMF1/VMF3 形式为连分式 `a/(b/(c+…))`，`a` 来自 NWM，`b,c` 为经验值 |
| `ah` / `aw` | 干/湿映射函数的 `a` 系数（无量纲，~1.2e-3 / ~5e-4） |
| NWM | 数值天气模型（ECMWF 业务分析/ERA/预报）；VMF 数据全部由它射线追踪得到 |
| GPT / GPT2 / GPT2w / GPT3 | 历代「全球气压温度」经验模型：格网存年均值+年/半年振幅；GPT3 额外给 VMF3 的 `ah/aw` 和梯度 |
| GMF | 全球映射函数（由 VMF1 经验化），无需外部文件 |
| VMF1 vs VMF3 | VMF1（2006）只有 `a` 来自 NWM；VMF3（2018）`b,c` 也重新拟合（球谐到 12 阶），低仰角更好 |

**做：**

- 离线模型：`gpt.m/.f`、`gpt2*.m/.f`、`gpt2_1w.*`、`gpt3_1*.m/.f90`（1° 格网 **27 MB**）、`gpt3_5*.m/.f90`（5° 格网 **1.1 MB**）、`gmf.m/.f`
- 映射函数：`vmf1.m/.f`、`vmf1_ht.m/.f`（带高程改正）、`vmf3.m/.f90`、`vmf3_ht.m/.f90`
- 格网插值：`vmf1_grid.m/.f90`、`vmf3_grid.m/.f90`（读 `trop_products/GRID/` 文件 + `orography_ell_*`，做时间线性、水平双线性、Kouba 2008 高程归算）
- 天顶延迟公式：`saasthyd.m/.f`（Saastamoinen ZHD）、`asknewet.m/.f`（Askne–Nordius ZWD）
- 梯度：`grad_grid.m/.f90`；C++：`gpt2w_C.cpp/.h`

**不做：**

- 不提供 NWM 本身、不做射线追踪（→ [radiate](./radiate.md) 或站点 ONLINE RAY-TRACER）
- 不估计 ZTD；不是可安装包；没有统一的 build/测试脚本
- Python 端口（`Python_Tools_Adavi/`）是第三方转写，与 [std-swd-calc](./std-swd-calc.md) 同作者，非全覆盖

## 2. codes 与 trop_products 的关系

| 你要 | 去哪 | 本机示例 |
| --- | --- | --- |
| 公式/算法源码 | `/codes/*.m|.f|.f90` | `gpt3_5.m` 15400 B |
| GPT 经验格网 | `/codes/*.grd` | `gpt3_5.grd` **1146104** B / **2593** 行（1 行表头，sha256₁₂ `3bf35c611e7c`） |
| 全球 VMF 格网（6 h） | `trop_products/GRID/{1x1,2.5x2,5x5}/{VMF1,VMF3}/{*_OP,*_FC,*_EI}/YYYY/` | `VMF3_20240101.H00` **3434750** B / **64807** 行 |
| 站点 VMF（逐站 6 h） | `trop_products/GNSS/VMF3/VMF3_OP/daily/YYYY/YYYYDDD.vmf3_g` | `2024001.vmf3_g` **195488** B / **2384** 行 |
| 站坐标 / 格点地形 | `station_coord_files/`（`gnss.ell`、`orography_ell_1x1` **583198** B） | GRAZ `47.0671 15.4935 538.30` |

`_OP` = 业务分析（事后），`_FC` = 预报（当季口令保护），`_EI` = ERA-Interim。**格网 `ah/aw` 在零高程/格点高度**，用 `*_grid.m` 或 `*_ht` 版本；**站点文件已在测站高**，直接进 `vmf3.m`。

## 3. 安装（下载即用）

```bash
mkdir -p ~/vmfcodes && cd ~/vmfcodes
B=https://vmf.geo.tuwien.ac.at/codes
for f in gpt3_5.m gpt3_5_fast.m gpt3_5_fast_readGrid.m gpt3_5.f90 gpt3_5.grd \
         vmf3.m vmf3_ht.m vmf3_grid.m saasthyd.m asknewet.m vmf1_ht.m gmf.m; do
  curl -fsSL -O $B/$f
done
curl -fsSL -O $B/Python_Tools_Adavi/gpt3_5_fast.py -O $B/Python_Tools_Adavi/gpt3_5_fast_readGrid.py -O $B/Python_Tools_Adavi/vmf3.py
sudo apt-get install -y octave gfortran        # 本机 Octave 9.4.0 / gfortran 14.2.0
pip install numpy pandas                         # Python 端口只需这两个
```

## 4. 端到端（本机 · GRAZ 2024-01-01 00:00 UTC，MJD 60310.0）

### 4a. GPT3 → ZHD/ZWD → VMF3_ht 斜延迟（Octave，纯离线）

```matlab
% run_gpt3.m
mjd = 60310.0;                        % 2024-01-01 00:00 UTC
lat = 47.0671*pi/180; lon = 15.4935*pi/180; h = 538.30;   % GRAZ (gnss.ell)
tic; [p,T,dT,Tm,e,ah,aw,la,undu,Gn_h,Ge_h,Gn_w,Ge_w] = gpt3_5(mjd,lat,lon,h,0); t1=toc;
printf('GPT3_5  p=%.2f hPa T=%.2f C dT=%.3f K/km Tm=%.2f K e=%.2f hPa\n',p,T,dT,Tm,e);
printf('        ah=%.8f aw=%.8f la=%.4f undu=%.3f m\n',ah,aw,la,undu);
printf('        Gn_h=%.3e Ge_h=%.3e Gn_w=%.3e Ge_w=%.3e m\n',Gn_h,Ge_h,Gn_w,Ge_w);
zhd = saasthyd(p,lat,h); zwd = asknewet(e,Tm,la);
printf('ZHD(saasthyd)=%.4f m  ZWD(asknewet)=%.4f m  ZTD=%.4f m\n',zhd,zwd,zhd+zwd);
for el = [90 30 10 5]
  zd = (90-el)*pi/180;
  [mfh,mfw] = vmf3_ht(ah,aw,mjd,lat,lon,h,zd);
  printf('el=%2d deg  mfh=%.4f mfw=%.4f  STD=%.4f m\n',el,mfh,mfw,zhd*mfh+zwd*mfw);
end
printf('gpt3_5 wall %.3f s\n',t1);
```

`octave -q --no-gui run_gpt3.m`（real **0.840 s**；中间两行 UTF-8 警告见坑 5，已删）：

```text
GPT3_5  p=959.59 hPa T=1.24 C dT=-4.703 K/km Tm=265.49 K e=4.85 hPa
        ah=0.00121094 aw=0.00053970 la=2.5189 undu=45.784 m
        Gn_h=-2.206e-04 Ge_h=-8.750e-05 Gn_w=-2.211e-05 Ge_w=2.275e-06 m
ZHD(saasthyd)=2.1847 m  ZWD(asknewet)=0.0580 m  ZTD=2.2427 m
el=90 deg  mfh=1.0000 mfw=1.0000  STD=2.2427 m
el=30 deg  mfh=1.9929 mfw=1.9968  STD=4.4698 m
el=10 deg  mfh=5.5586 mfw=5.6640  STD=12.4725 m
el= 5 deg  mfh=10.1638 mfw=10.7955  STD=22.8311 m
gpt3_5 wall 0.080 s
```

`gpt3_5_fast_readGrid` + `gpt3_5_fast`（Octave）同输入：`fast p=959.59 ah=0.00121094 aw=0.00053970`。

### 4b. 同一 GPT3 的 Fortran 与 Python 版（交叉验证）

```fortran
! drv.f90
program drv
implicit none
double precision :: mjd, lat(1), lon(1), h(1)
double precision, dimension(1) :: p,T,dT,Tm,e,ah,aw,la,undu,Gnh,Geh,Gnw,Gew
double precision, parameter :: pi = 3.14159265358979d0
mjd = 60310.0d0
lat(1) = 47.0671d0*pi/180d0; lon(1) = 15.4935d0*pi/180d0; h(1) = 538.30d0
call gpt3_5(mjd,lat,lon,h,1,0, p,T,dT,Tm,e,ah,aw,la,undu,Gnh,Geh,Gnw,Gew)
write(*,'(a,f8.2,a,f6.2,a,f7.2,a,f6.2)') 'F90 p=',p(1),' T=',T(1),' Tm=',Tm(1),' e=',e(1)
write(*,'(a,f11.8,a,f11.8,a,f7.4,a,f8.3)') '    ah=',ah(1),' aw=',aw(1),' la=',la(1),' undu=',undu(1)
end program
```

```text
$ gfortran -O2 -o drv gpt3_5.f90 drv.f90 && ./drv
F90 p=  959.59 T=  1.24 Tm= 265.49 e=  4.85
    ah= 0.00121094 aw= 0.00053970 la= 2.5189 undu=  45.784
```

Python（`gpt3_5_fast_readGrid('gpt3_5.grd')` 一次 → `gpt3_5_fast(60310.0, lat[], lon[], h[], 0, grid)`；`vmf3(mjd,lat,lon,zd,ah,aw)` 喂站点系数）：

```text
PY  p=959.59 T=1.24 Tm=265.49 e=4.85 ah=0.00121094 aw=0.00053970 la=2.5189 undu=45.784
PY vmf3 site el=5 mfh=10.1579 mfw=10.7460
readGrid 0.050 s, gpt3 0.016 s
```

### 4c. 真 NWM 数据：站点 VMF3 与格网 VMF3

```bash
curl -fsSL -O https://vmf.geo.tuwien.ac.at/trop_products/GNSS/VMF3/VMF3_OP/daily/2024/2024001.vmf3_g
grep GRAZ 2024001.vmf3_g
# GRAZ      60310.00  0.00120480  0.00058178  2.1686  0.1047   951.19   6.89   8.47
# GRAZ      60310.25  0.00119426  0.00052434  2.1723  0.0706   953.07   3.26   6.49
# GRAZ      60310.50  0.00119736  0.00043794  2.1776  0.0535   955.28   5.43   6.92
# GRAZ      60310.75  0.00119737  0.00043736  2.1815  0.0461   956.94   5.65   5.16
```

站点系数进 `vmf3.m`（`[mfh,mfw]=vmf3(ah,aw,mjd,lat,lon,zd)`，`STD=zhd·mfh+zwd·mfw`）：

```text
VMF3 site el=90  mfh=1.0000 mfw=1.0000  STD=2.2733 m
VMF3 site el=30  mfh=1.9929 mfw=1.9965  STD=4.5308 m
VMF3 site el=10  mfh=5.5575 mfw=5.6568  STD=12.6442 m
VMF3 site el= 5  mfh=10.1579 mfw=10.7460  STD=23.1536 m
```

格网路径（1°×1° VMF3_OP + 地形；`vmf3_grid.m` 需先打坑 6–8 的补丁，得到 `patched/vmf3_grid.m`）：

```bash
mkdir -p grid/2024 oro patched
G=https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/2024
curl -fsSL -o grid/2024/VMF3_20240101.H00 $G/VMF3_20240101.H00
curl -fsSL -o oro/orography_ell_1x1 https://vmf.geo.tuwien.ac.at/station_coord_files/orography_ell_1x1
sed -e 's/round(\(l[a-z]*_deg\),10)/round(\1*1e10)\/1e10/' -e "s#'\\\\#'/#g" \
    -e "s/sprintf('%02s',num2str(\([a-z]*\)(\([a-z_0-9]*\))))/sprintf('%02d',round(\1(\2)))/g" \
    -e "s/max(index),'CommentStyle'/max(index)+100,'CommentStyle'/" vmf3_grid.m > patched/vmf3_grid.m
cp vmf3_ht.m patched/ && cd patched
octave -q --no-gui --eval "lat=47.0671*pi/180; lon=15.4935*pi/180; [mfh,mfw,zhd,zwd]=vmf3_grid('$HOME/vmfcodes/grid','$HOME/vmfcodes/oro',[],60310.0,lat,lon,538.30,85*pi/180,1); printf('VMF3 grid el=5 mfh=%.4f mfw=%.4f zhd=%.4f zwd=%.4f ZTD=%.4f\n',mfh,mfw,zhd,zwd,zhd+zwd)"
```

```text
VMF3 grid el=5 mfh=10.1590 mfw=10.8004 zhd=2.1677 zwd=0.1015 ZTD=2.2693
```

**三路对照（同站同时刻，全部本机输出）：**

| 来源 | ZHD [m] | ZWD [m] | ZTD [m] | STD@5° [m] |
| --- | ---: | ---: | ---: | ---: |
| GPT3（经验，无气象数据） | 2.1847 | 0.0580 | 2.2427 | 22.8311 |
| VMF3 站点文件（NWM） | 2.1686 | 0.1047 | 2.2733 | 23.1536 |
| VMF3 1° 格网（NWM，插值+高程归算） | 2.1677 | 0.1015 | 2.2693 | — |

读法：干延迟三者差 ≤ 1.7 cm；湿延迟 GPT3 只有气候平均，本例比 NWM 少约 4.7 cm——这正是 PPP 里仍要**估计** ZWD、GPT3 只作先验的原因。

## 5. 函数签名与单位

| 函数 | 输入 | 输出 |
| --- | --- | --- |
| `gpt3_5(mjd,lat,lon,h_ell,it)` | mjd 标量；lat/lon **弧度**向量；h_ell 椭球高 m；`it=1` 关季节项 | `p`hPa `T`°C `dT`°C/km `Tm`K `e`hPa `ah aw`（零高程）`la` `undu`m `Gn_h Ge_h Gn_w Ge_w` m |
| `gpt3_5_fast(mjd,lat,lon,h_ell,it,grid)` | 同上 + `grid=gpt3_5_fast_readGrid` | 同上（批量快） |
| `saasthyd(p,dlat,hell)` | hPa, rad, m | `zhd` m（头注释例：p=1000, 48°, 200 m → 2.2763，2025-01-16 修订） |
| `asknewet(e,Tm,lambda)` | hPa, K, 无量纲（=GPT3 `la`） | `zwd` m |
| `vmf3(ah,aw,mjd,lat,lon,zd)` | 测站高系数；rad | `mfh mfw` |
| `vmf3_ht(ah,aw,mjd,lat,lon,h_ell,zd)` | 零高程系数（GPT3/格网）；m；rad | `mfh mfw`（含 Niell 高程改正） |
| `vmf3_grid(indir_grid,indir_oro,cache,mjd,lat,lon,h_ell,zd,grid_res)` | 目录下须有 `YYYY/VMF3_YYYYMMDD.Hhh`；`cache` 首次传 `[]`；`grid_res`=1 或 5 | `mfh mfw zhd zwd cache` |
| Python `vmf3(mjd,lat,lon,zd,ah,aw)` | **参数顺序与 .m 不同** | `mfh, mfw` |

格网文件列：`lat lon ah aw zhd zwd`（`!` 开头 7 行表头，`Range/resolution: -89.5 89.5 0.5 359.5 1 1`）。站点文件列：`站名 MJD ah aw zhd zwd p[hPa] T[°C] e[hPa]`。

## 6. 坑（现象 → 原因 → 修复）

1. **下 `Verification/*.txt` 得 403** → 该子目录对外关闭（目录页可见、文件不可取）→ 用本手册 4a/4b 三语言互相比对代替官方参考值：  
   `curl -s -o /dev/null -w "%{http_code}\n" https://vmf.geo.tuwien.ac.at/codes/Verification/gpt3_5_fast_grid.txt   # 本机 403`
2. **Fortran 可执行在别的目录跑，只打印 `Error: gpt3_5.grd can't be opened...check if it is stored in the same directory as gpt3_5.f90!`，退出码却是 0** → 格网按当前目录相对路径打开，失败不设非零码，批处理不会察觉 → 先 cd 到格网目录或软链：  
   `ln -sf ~/vmfcodes/gpt3_5.grd . && ./drv`
3. **把 GPT3 或格网的 `ah` 直接喂 `vmf3.m`，高山站映射偏** → GPT3/格网系数指零高程，须用 `_ht` 版；站点 `.vmf3_g` 才用无 `_ht` 版 → 按来源选函数：  
   `grep -n "zero height\|has to be used with the grid" gpt3_5.m vmf3_ht.m`
4. **Python `vmf3.py` 结果离谱** → 端口签名是 `vmf3(mjd,lat,lon,zd,ah,aw)`，MATLAB 是 `vmf3(ah,aw,mjd,lat,lon,zd)`；照抄 .m 的顺序会把系数当 MJD → 调用前看签名：  
   `grep -n "^def " vmf3.py gpt3_5_fast.py`
5. **Octave 每次调用刷 `warning: Invalid UTF-8 byte sequences have been replaced.`** → `vmf3.m`/`vmf3_ht.m`/`vmf3_grid.m`/`gpt3_5_fast.m` 注释含 Latin-1 字符（ö），不影响数值 → 转码一次（本机转码后警告计数 0）：  
   `for f in vmf3.m vmf3_ht.m vmf3_grid.m gpt3_5_fast.m; do iconv -f latin1 -t utf-8 $f -o $f.u && mv $f.u $f; done`
6. **Octave 跑 `vmf3_grid.m` 报 `Invalid call to round`** → MATLAB 的 `round(x,10)` 两参形式 Octave 9.4 不支持 →  
   `sed -i 's/round(\(l[a-z]*_deg\),10)/round(\1*1e10)\/1e10/' vmf3_grid.m`
7. **随后报 `textscan: invalid stream number = -1`** → 两个原因叠加：路径用 Windows `'\'` 拼接；`sprintf('%02s',num2str(1))` 在 Octave 补**空格**不补 0，文件名变成 `VMF3_2024 1 1.H 0` →  
   `sed -i -e "s#'\\\\#'/#g" -e "s/sprintf('%02s',num2str(\([a-z]*\)(\([a-z_0-9]*\))))/sprintf('%02d',round(\1(\2)))/g" vmf3_grid.m`
8. **再报 `VMF3_data_all(15496,_): out of bound 15489`** → `textscan(...,max(index),'CommentStyle','!')` 在 Octave 里把 7 行 `!` 表头也计入读取条数，少读 7 行 →  
   `sed -i "s/max(index),'CommentStyle'/max(index)+100,'CommentStyle'/" vmf3_grid.m`（`Inf` 本机报 `REPEAT = inf is too large`，不可用）
9. **`vmf3_grid` 读不到文件/历元对不上** → 期望 `indir/YYYY/VMF3_YYYYMMDD.Hhh` 年子目录 + 相邻两个 6 h 历元（观测不在整 6 h 上时）；地形文件名须是 `orography_ell_1x1`（或 `_5x5`，与 `grid_res` 一致）→  
   `mkdir -p grid/2024 && curl -fsSL -o grid/2024/VMF3_20240101.H06 https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/2024/VMF3_20240101.H06`
10. **想要当年预报格网却得 401** → `*_FC` 基于 ECMWF 预报，按许可口令保护（按季换，联系 vmf@tuwien.ac.at）；本机 `VMF3_FC/2026/` **401**、`VMF3_FC/2025/` **200**（往年开放）；`*_OP` 约滞后 1 天（本机看到最新 `VMF3_20260924.H18`，服务器时间戳 2026-09-25 18:32）→ 事后处理用 OP，实时先用 GPT3：  
    `curl -s -o /dev/null -w "%{http_code}\n" https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_FC/2026/`

## 7. 许可与引用

- **源码**：文件头仅版权声明，**没有**给出 GPL/MIT 等许可条款；可下载使用，但二次分发/商用前应联系 vmf@tuwien.ac.at 确认。本仓收录只链接不转载。
- **数据**（`terms.html`）：免费使用；须引用 re3data「VMF Data Server」doi:10.17616/R3RD2H 并**致谢 ECMWF**；基于 ECMWF 业务分析/ERA-Interim 的「非有效」产品（验证时刻早于 24 h）按 **CC BY 4.0**；基于预报的产品为非商业科研专用、口令保护，往年预报产品按业务产品条款开放。
- 方法文献：VMF1 Böhm et al. 2006 doi:10.1029/2005JB003629；VMF3/GPT3 Landskron & Böhm 2018 doi:10.1007/s00190-017-1066-2；格网高程归算 Kouba 2008 doi:10.1007/s00190-007-0170-0（均见源码头注释）。

## 8. 接到 GNSS / 电离层工作流的哪一步

- **PPP 引擎配置**：[ginan](./ginan.md) `inputs.troposphere` 有 `gpt2grid_files` / `vmf_files` / `orography_files`，模型可选 `[standard,sbas,vmf3,gpt2,cssr]`（本机 ginan tip `5033996` 的 `ppp_example.yaml` 默认 `gpt2` + `tables/gpt_25.grd`）；换 VMF3 就把 §2 的格网与 `orography_ell_1x1` 喂进去。[rtklib](./rtklib.md) 内置 Saastamoinen + NMF（`-DIERS_MODEL` 编译换 GMF），不读 VMF 文件；[pride-pppar](./pride-pppar.md) 的 ZTD/映射选项见其 `-H`。
- **斜延迟/水汽**：[std-swd-calc](./std-swd-calc.md) 把本页 GPT3/VMF1 的 Python 版串成 SWD；真射线追踪对照 [radiate](./radiate.md)（其站坐标文件同样来自 `station_coord_files/`）。
- **GNSS-IR**：[gnssrefl](./gnssrefl.md) 的仰角折射改正内置 GPT2w（`gpt_1wA.pickle`，对应本页 `gpt2_1w.grd`）。
- **电离层处理**：对流层非色散，双频无电离层组合不消除它；做 TEC/GIM 时 ZTD 不进几何无关组合，但 PPP 估电离层（非差非组合）时对流层先验好坏直接影响电离层参数收敛，见教程 [06](../tutorials/06-iono-positioning.md)。
