# GAMIT/GLOBK：MIT 高精度 GNSS 网解 + 时间序列/速度场（**未在本机实跑（申请制分发）**）

> **状态**：本篇**没有**在本机编译或运行 GAMIT/GLOBK——源码只发给已登记的机构（发用户名/口令后从 MIT 服务器下载），公开网上没有官方源码或二进制。下面的安装步骤、命令、控制文件与输出名全部来自 MIT 公开文档（2026-09-26 02:05 EDT 下载核对），**没有任何本机 stdout**。数值判据（nrms≈0.2 等）是文档/讲义里的经验值，不是本机结果。
>
> 依据：`GG_Quick_Start_Guide.pdf`（5 页，页脚 v.2026-07-21，写明当前版本 **10.71**）、`Intro_GG.pdf`（54 页，Release 10.7，2018-06-02）、`GAMIT_Ref.pdf`（168 页，2018-06-07）、`GLOBK_Ref.pdf`（95 页，2015-06），均在 <https://geoweb.mit.edu/gg/docs.php>；以及 EarthScope 2024 课程讲义 <https://geoweb.mit.edu/gg/courses/202407_EarthScope/>（`01-GGnix`、`12-workflow_basics`、`13-sh_gamit`、`22-glred_ts`）。手册主体停在 2015–2018，与 10.71 有出入时**以安装包里 `~/gg/help/` 和脚本不带参数时的自带帮助为准**。

## 1. 它做什么（术语先讲清）

| 部分 | 做什么 | 关键词解释 |
| --- | --- | --- |
| **GAMIT** | 一天一解：把多站 RINEX 做**双差相位**最小二乘，估站坐标、卫星轨道（可固定）、天顶对流层延迟、模糊度 | 双差 = 站间差 + 星间差，消掉卫星/接收机钟差；观测量默认 **LC**（无电离层组合） |
| **GLOBK** | 把每天的松弛解（h-file）用卡尔曼滤波合并：出**坐标时间序列**、多期合并解、**速度场** | 松弛解 = 几乎不加约束的解，参考框架留到 `glorg` 再定 |
| 脚本 | `sh_gamit`（批处理 GAMIT）、`sh_glred`（批处理 GLOBK/glred + 画时序） | 两个脚本把几十个小程序串起来 |

用途：构造形变、板块运动、毫米级站坐标、ZTD。与本仓 PPP 工具（[pride-pppar](./pride-pppar.md)、[ginan](./ginan.md)、[groops](./groops.md)）属同一档科研解算软件，但 GAMIT 是**网解**（相对定位），不是单站 PPP。

和电离层的关系（`GAMIT_Ref` 第 8 章、`Intro` 1.2 节）：

- 一阶电离层靠 LC 组合消掉，GAMIT **不输出 TEC**，也不是电离层研究工具。
- 二、三阶项（强电离层时文档称可达 15 mm 路径延迟）可以建模：需要 CODE 的 IONEX（`CODGddd0.yyI`）+ 地磁场模型。手册写法：IONEX 放进 `[project]/ionex/`，`sh_gamit` 加 `-ion`，`sestbl.` 设 `Ion model = GMAP` 与 `Mag field = IGRF11`（同章正文又推荐 IGRF12——以你拿到版本的 `sestbl.` 模板注释为准）。
- 手册明确说 GAMIT 的映射函数按 **CODE** IONEX 写死，**不要用 IGS 综合 IONEX**。
- 1995 年前无精密伪距时用 `LC_HELP`（给电离层约束，`Ionospheric Constraints = 0.0 mm + 8.00 ppm` 是 Intro 模板里的“太阳活动中高年”示例）来固定宽巷模糊度。

## 2. 许可与获取

- 许可页 <https://geoweb.mit.edu/gg/license.php>：**仅限非商业教育和科研**可免费复制、使用、修改；须保留版权声明，并**用邮件把单位名称和地址告诉 MIT**；许可授给**机构**而不是个人，该机构现有成员都可以用；商业用途需向 MIT Technology Licensing Office 另行申请。**不是 OSI/SPDX 开源许可**（PROJECTS.json 记作 `scientific distribution (request)`）。
- 拿到口令后下载（Quick Start 第 3 节，文件名原样）：`com / gamit / help / kf / libraries / tables / test_install` 各一个 `.10.71.tar.gz`，外加最新的 `incremental_updates.<YYYYMMDD>.tar.gz`；文档要求**至少每月**更新一次增量包。

## 3. 安装（Linux；按 Quick Start + 讲义，未本机验证）

```bash
sudo apt install gfortran make libx11-dev csh tcsh bc curl      # Debian/Ubuntu 依赖（原文命令）
mkdir -p ~/src/gg/10.71 && cd ~/src/gg/10.71                      # 自选源码目录，文档称 <source>
curl -k -R -O -u <用户名>:<口令> '<url>/source/{com,gamit,help,kf,libraries,tables,test_install}.10.71.tar.gz'
curl -k -R -O -u <用户名>:<口令> '<url>/source/incremental_updates.<YYYY><MM>01.tar.gz'
tar xfzv com.10.71.tar.gz com/install_software
com/install_software                  # 交互问答；找不到 X11 时停下改 libraries/Makefile.config
sudo apt install gmt gmt-dcw gmt-gshhg   # 画图脚本（sh_plot_pos 等）需要 GMT
```

环境变量（讲义 `01-GGnix` 第 47 页，bash 版）：

```bash
gg='/home/you/src/gg/10.71'
PATH="$gg/com:$gg/gamit/bin:$gg/kf/bin:$PATH"; export PATH
HELP_DIR="$gg/help/"; export HELP_DIR
INSTITUTE='XXX'; export INSTITUTE
ln -s /home/you/src/gg/10.71 ~/gg      # 很多脚本认 ~/gg 这个链接，不要删
```

装完用 `test_install/` 自带 README 跑例子，结果与 `test_install/check_files/` 比，“几乎一致”即安装正确（Quick Start 第 6 节）。

数据下载前提（Quick Start 2.5）：CDDIS 自 2020-10-31 停匿名 FTP，脚本改用 Earthdata 认证 HTTPS，需要 `~/.netrc`：

```text
machine urs.earthdata.nasa.gov login <用户名> password <口令>
```

EarthScope（原 UNAVCO）数据要装 EarthScope CLI 并把 `es` 链进 `~/gg/com/`（见 [earthscope-sdk](./earthscope-sdk.md)）。

## 4. 工作流：sh_gamit → sh_glred

项目目录（**不要**建在安装目录里）：

```text
emed18/            ← 项目目录，在这里执行 sh_setup / sh_gamit / sh_glred
├── rinex/         ← 自己的 RINEX（RINEX 3 会被 sh_gamit 自动改成 ssssddds.yyo 短名）
├── tables/        ← sh_setup 生成：控制文件 + 指向 ~/gg/tables 的链接
├── 034/ 035/ ...  ← sh_gamit 每天一个“日目录”
├── glbf/          ← sh_glred -opt H 生成的二进制 h-file
└── gsoln/         ← GLOBK 控制文件与 .org/.pos 结果
```

步骤（`Intro` 2.1 + 讲义 `12-workflow_basics`）：

1. 项目目录下运行 `sh_setup`（参数以其自带帮助为准），把控制文件拷进 `tables/`、链接年度全局表；检查 `otl.grid / atl.grid / map.grid / met.grid` 链接（`sestbl.` 里开了哪个就要有哪个）。
2. 编辑下表的控制文件；`station.info` 与 `.apr` 是讲义里标为“非常重要、必须弄对”的两个。
3. 运行：

```bash
sh_gamit -expt emed -d 2018 034 035 036 >& sh_gamit.log      # Intro 原例；csh 下写 >&!
sh_glred -expt emed -s 2018 34 2018 36 -opt H G T >& sh_glred.log
```

### 4.1 控制文件（在 `tables/`）

| 文件 | 管什么 | 新手要改吗 |
| --- | --- | --- |
| `process.defaults` | 计算环境、轨道/数据来源、采样与时段、归档、邮件地址（`mailto`）、`aprf`（apr 文件名）、`minxf` 等 | 少量 |
| `sites.defaults` | 用哪些本地/IGS 站、元数据怎么更新（`ftprnx`、`xstinfo` 等关键词） | **要**：列出你的站 |
| `station.info` | 各站随时间变化的接收机、天线型号、天线高 | **要**：错了会系统性偏 |
| `*.apr` / `lfile.` | 先验坐标（apr 固定不变；lfile 每天按相位解更新，默认调整 >0.3 m 才改写） | 先验要好于约 10 m |
| `sestbl.` | 解算选项：`Choice of Experiment`（BASELINE/RELAX./ORBIT）、`Choice of Observable`（LC_AUTCLN/LC_HELP/L1_ONLY…）、`Zenith Delay Estimation`、`Interval zen`、`Antenna Model`、`Ion model`、`Mag field` | 默认可用 |
| `sittbl.` | 按站给约束（紧约束的站必须在 apr 里有准坐标） | 保证至少一站受约束 |
| `autcln.cmd` | 自动周跳/粗差清理 | 一般不改 |
| `gsoln/globk*.cmd`、`glorg*.cmd` | GLOBK 合并与定框架（`glorg` 里列参考站、`apr_site`/`apr_neu` 控是否估速度） | 至少改 glorg 的参考站 |

### 4.2 sh_gamit 常用选项（Intro 2.1 原列表）

| 选项 | 含义 |
| --- | --- |
| `-expt <4字符>` | 实验名，出现在 h/q 文件名里 |
| `-d yyyy ddd ddd…` / `-s` / `-r` | 指定日、连续区间、或“今天往前第 N 天” |
| `-gnss G/R/C/E/I` | 处理 GPS 以外系统（日目录加系统后缀，如 `034E`） |
| `-orbit igsf/igsr/codm…` | 轨道产品（默认 igsf） |
| `-eops usno/usnd` | 地球定向参数 |
| `-sessinfo 30 2880 0 0` | 采样(s)、历元数、起始 HH MM |
| `-noftp` | 不从外部下载 |
| `-pres ELEV` | 画相位–高度角与天空图 |
| `-netext <c>` / `-yrext` | 日目录加后缀/年前缀，用于同一天多种处理 |
| `-ion` | 链接 `ionex/` 下 IONEX，用于高阶电离层项 |
| `-copt` / `-dopt` | 日目录里压缩/删除哪些文件 |

`sh_glred -opt`：`H` 把 GAMIT ASCII h-file 转成二进制放进 `glbf/`；`G` 跑 glred；`T` 用 `tssum` 从 `.org` 抽 `.pos` 并调 `sh_plot_pos` 画时序；`LB/LC/F` 链接或下载外部（MIT/SOPAC）h-file 合并。

## 5. 输出文件与怎么读

| 文件（Intro 2.2 例名） | 是什么 |
| --- | --- |
| `xblyt0.034` | x-file：makex 输出的 GAMIT ASCII 观测 |
| `cblyt0.034` | c-file：二进制，含 O−C 与偏导；第 6 字符 a/b… 表示迭代次数 |
| `qscala.034` | q-file：solve 完整解报告；第 6 字符 `p`=预解，`a`=终解 |
| `hscala.00034` | GAMIT h-file：松弛解 + 协方差，唯一带长年份、要带到 GLOBK 的文件 |
| `h0002031200_scal.glx` | GLOBK 二进制 h-file（htoglb 生成，名字可任意） |
| `globk..org` / `glred_*.org` | glorg 解报告（坐标、调整量、框架） |
| `*.pos` | 每站坐标时间序列（标准 GLOBK 时序格式） |
| `sh_gamit_<DDD>.summary` | 每天摘要（同时邮件发送） |
| `autcln.post.sum` / `autcln.prefit.sum` | 清理统计、各站相位 RMS |
| `GAMIT.fatal` / `GAMIT.warning` | 出错原因 |

按讲义 `13-sh_gamit` 第 19–20 页读 `sh_gamit_<DDD>.summary`：

- 站数等于预期；各站 postfit RMS 大约 3–10 mm；**不能有 RMS=0 的站**（说明 autcln 把数据全删了）。
- 四行 `Postfit nrms`（Constrained free/fixed、Loose free/fixed）都应约 **0.2**；约束解明显大于松弛解 = 约束过紧。
- `Percent fixed`：Intro 说 LC_AUTCLN 下宽巷（WL）通常应 >90%，窄巷（NL）比例取决于时段长度、网形与轨道质量；讲义的笼统判据是“多数”模糊度固定——噪声大的日子 70–85%、最好的日子 >90%。
- 时序（`.pos` / `sh_plot_pos` 图）看日重复性和跳变；地震/换天线要在 globk 的 earthquake/rename 文件里加断点。

## 6. 坑（全部来自公开文档与讲义，未本机复现）

1. **现象**：脚本做数值运算出错、GMT 画图异常。**原因**：系统区域设置用逗号作小数点。**修复**：`export LC_NUMERIC=C`（写进 `~/.bashrc`）。
2. **现象**：`install_software` 找不到 X11。**原因**：缺 `libX11` 或 `Xlib.h`，或路径不标准。**修复**：`sudo apt install libx11-dev` 后重跑；仍不行就改 `libraries/Makefile.config` 里的 `X11LIBPATH`/`X11INCPATH`。
3. **现象**：轨道/RINEX 自动下载失败。**原因**：CDDIS 已停匿名 FTP。**修复**：`echo "machine urs.earthdata.nasa.gov login <用户名> password <口令>" >> ~/.netrc && chmod 600 ~/.netrc`。
4. **现象**：某站在解里但无数据或无调整量。**原因**：先验坐标偏差 >10 m，过不了 autcln。**修复**：查 `autcln.prefit.sum` 的 range rms，把可靠坐标（前一次解或伪距解）追加进 `tables/*.apr` 后重跑该日。
5. **现象**：约束解 nrms 明显大于松弛解。**原因**：`sittbl.` 约束过紧或某约束站坐标不准。**修复**：`grep "Postfit nrms" 034/sh_gamit_034.summary` 确认后，`sittbl.` 只留一个最可靠站受约束再跑。
6. **现象**：相位残差随高度角有大而系统的形状、坐标系统性偏。**原因**：`station.info` 天线型号/天线高错。**修复**：`sh_upd_stnfo -ref station.info -l sd`（Intro 原例）按 RINEX 头与 `sites.defaults` 更新后人工核对。
7. **现象**：开了高阶电离层项但效果可疑。**原因**：用了 IGS 综合 IONEX（GAMIT 按 CODE 映射函数写死），或处理 1998 年前低分辨率 IONEX。**修复**：只把 `CODGddd0.yyI` 放进 `[project]/ionex/` 再 `sh_gamit ... -ion`。
8. **现象**：莫名报错、与新数据/新天线不兼容。**原因**：没装增量更新。**修复**：下载最新 `incremental_updates.<YYYYMMDD>.tar.gz` 解到 `<source>` 后重跑 `com/install_software`。
9. **现象**：某天中断，不知原因。**原因**：缺文件或格式错，屏幕日志没保存。**修复**：`cat 034/GAMIT.fatal`，并始终 `sh_gamit ... >& sh_gamit.log` 留日志（报 bug 时发日志文本，不要截图）。

## 7. 诚实边界与替代

- 本篇**无实跑**：没有 test_install 结果、没有 summary/q-file/.pos 实例；所有命令以你拿到的版本自带帮助为准。手册 2015–2018 年版与 10.71 可能有差异（例如 IGRF 版本号）。
- 电离层研究本身（TEC/ROTI/GIM）请用本仓的专门工具：[gnss-tec](./gnss-tec.md)、[pytecgg](./pytecgg.md)、[ionex-gim](./ionex-gim.md)；GAMIT 只在“高阶电离层项对坐标的影响”这一侧相关。
- 想要可以直接下载运行的开源精密解算：[pride-pppar](./pride-pppar.md)（PPP-AR）、[ginan](./ginan.md)、[groops](./groops.md)、[rtklib](./rtklib.md)。卫星几何/轨道外推见 [gmat](./gmat.md)。
