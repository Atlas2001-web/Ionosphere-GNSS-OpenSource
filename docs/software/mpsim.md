# mpsim · GNSS 多路径前向仿真器操作手册

目录：[`PROJECTS.json` → `mpsim`](../../PROJECTS.json) · 上游 <https://github.com/ufrgs-gnss-lab/mpsim> · tip **`61be627`**（2020-11-26）· ★**48** · 许可 **BSD-2-Clause**（`LICENSE`，Felipe Geremia Nievinski）· 本机验证（**2026-09-24 07:01–07:13 EDT**；**质检复跑 07:22 EDT**）：clone tip **`61be627`**；**1617** 个 `.m`（写作 **1615**）；`script/` 驱动 **14**；**Octave 9.4.0**：未移 MEX 时 `interp2_linear_c.mex` **invalid ELF**（magic `MZ`，Windows 产物）/`*.mexglx` ELFCLASS32；按手册移走 `.mex`+仅含 `%!test` 的 `.m` 后 → `snr_settings`→`snr_setup` **OK**（`setup_ok t=0.74`）→`snr_fwd` **OK**（`snr_len=250`；snr **34.6240–53.1458** dB mean **45.9008**；carrier **−0.0137802–0.0166744** m；code **−0.289898–0.140195** m）；写作曾报 `snr_fwd` concatenation 失败 —— **本 QC 未复现**（移 MEX+.m 后 fwd 通）；`mkoctfile`/`octave-dev` 未装；**未抄论文插图数字**

> 岗位：**平面/分层地表 + 天线方向图**下的 GNSS 多路径前向模型（SNR、载波/码误差），复现 Nievinski & Larson *GPS Solutions* 2014 附图。冲突时：**`help snr_fwd` / `README.TXT` / 论文 > 本文**。  
> 观测域码 MP 分析 → [gnss-multipath-analysis](./gnss-multipath-analysis.md)；RINEX 读入 → [georinex](./georinex.md)；实测定位 → [rtklib](./rtklib.md)；GNSS-IR 反演 → [gnssrefl](./gnssrefl.md)。

## 1. 用途与边界

**做：**

- `snr_settings` / `snr_setup` / `snr_fwd`：默认或定制几何 → 干涉 SNR、载波误差、码误差
- `get_permittivity`：地表介电；天线：预载 `TRM29659.00`+`SCIT` 等方向图
- `script/fig*.m`：论文图 A1–A9、B2–B3 驱动；`image/` 有参考 PNG
- `snr_demo.html`：浏览器教程；Octave 可用 `--traditional`

**不做 / 本机限制：**

- **不是** 从 RINEX 估 MP RMS → [gnss-multipath-analysis](./gnss-multipath-analysis.md)
- **不是** GNSS-IR 水位反演产线 → [gnssrefl](./gnssrefl.md)
- **不是** 接收机/基带仿真 → [gps-sdr-sim](./gps-sdr-sim.md) / [gnss-sdr](./gnss-sdr.md)
- **官方主路径 = MATLAB**；Octave：须移走无效 `.mex`/测试桩 `.m` 后 `snr_fwd` 可通（质检已复跑）
- 预编译 MEX **不能**在本机 x86_64 Octave 9 加载；无 `mkoctfile` 未现场重编
- **禁止**把论文插图数字抄成“本机 stdout”

一句话：mpsim = **多路径前向仿真（MATLAB 生态）**；本机移走无效 MEX + 测试桩 `.m` 后 `snr_setup`/`snr_fwd` 均可跑通；默认真值见头注（**非**论文插图拷贝）。

| 术语 | 含义 |
| --- | --- |
| `sett.ref.height_ant` | 天线相位中心距反射面高度 (m)；默认示例常改 **1.5–5** |
| `sett.sat.elev.*` | 仰角 min/max/rate（度） |
| `snr_db` | 合成 SNR（dB） |
| `carrier_error` / `code_error` | 多路径引起的载波/码误差 (m) |
| densemap | 天线增益方位–仰角栅格；评估走 `interp2_linear_c`（C-MEX）或 Octave `interp2` 回退 |

## 2. vs gnss-multipath-analysis / gnssrefl / georinex / RTKLIB

| | **本文 mpsim** | [gnss-multipath-analysis](./gnss-multipath-analysis.md) | [gnssrefl](./gnssrefl.md) | [georinex](./georinex.md) | [rtklib](./rtklib.md) |
| --- | --- | --- | --- | --- | --- |
| 方向 | **前向**仿真 | **后向**观测分析 | SNR→RH | 读 RINEX | 定位 |
| 输入 | sett/setup | OBS+NAV/SP3 | RINEX/SNR | RINEX | RINEX |
| 输出 | SNR/误差曲线 | RMS/周跳报告 | RH 表 | xarray | `.pos` |
| 本机 | setup+fwd OK（移 MEX） | NMBUS 实跑 | mchl 实跑 | 已短硬 | apt/自编 |

## 3. 安装

### 3.1 MATLAB（上游推荐；本机无）

```matlab
% 把 init.m 拖进 MATLAB 命令窗，或：
run('/path/to/mpsim/init.m')
help snr_fwd
snr_fwd   % 无参：默认 setup + 出图
```

### 3.2 Octave（本机 9.4.0；有限）

```bash
sudo apt-get install -y octave          # 本机：9.4.0
# 可选：octave-statistics（apt 502 时本机未装；README 建议 pkg load statistics）
git clone --depth 1 https://github.com/ufrgs-gnss-lab/mpsim.git
cd mpsim && git rev-parse --short HEAD  # 61be627
find . -name '*.m' | wc -l               # 1617（质检）
```

```octave
octave --traditional --no-gui
graphics_toolkit('gnuplot')   % 或 qt；无显示可跳过出图
% pkg load statistics
run('/path/to/mpsim/init.m')  % 内含 init_plot；无 GUI 时建议手写 addpath（见 §4）
```

`init.m` 要点：`addpath(genpath(lib))` + `script`；Octave 下可能 `rename` 掉自带的 `isequaln` 阴影。

## 4. 端到端

### 4.1 文档最小例（MATLAB；本机未出数值）

```matlab
sett = snr_settings();
sett.ref.height_ant = 5.0;   % 或 1.5 等
setup = snr_setup(sett);
[result, snr_db, carrier_error, code_error] = snr_fwd(setup);
% 无输出参数则直接作图
```

论文图：`cd script; figA1` …（先 `run ../init.m`）。对照 `image/matlab/` 或 `image/octave/` PNG。

### 4.2 本机 Octave 冒烟（可复现边界）

避开 `init_plot`、移走坏 MEX 后：

```bash
cd /path/to/mpsim/lib/util/interp
mkdir -p /tmp/mpsim-mex-bak
# 无效/32 位预编译，防止 Octave 误加载：
mv -f interp2_linear_c.mex lininterp1f.mex /tmp/mpsim-mex-bak/ 2>/dev/null || true
# 将仅含 %!test 的 interp2_linear_c.m 移走，迫使 densemap 走内置 interp2 回退
mv -f interp2_linear_c.m /tmp/mpsim-mex-bak/ 2>/dev/null || true
```

```octave
warning('off','all');
base = '/path/to/mpsim';
addpath(genpath(fullfile(base,'lib')));
addpath(genpath(fullfile(base,'script')));
addpath(base);
sett = snr_settings();
disp(fieldnames(sett));           % sat ref opt ant sfc bias
sett.ref.height_ant = 1.5;
sett.sat.elev.max = 30;
sett.sat.elev.min = 5;
sett.sat.elev.rate = 2;
tic; setup = snr_setup(sett); fprintf('setup_ok t=%.2f\n', toc);
[result, snr_db, carrier_error, code_error] = snr_fwd(setup);
```

**本机实录：**

```text
sett fields: sat, ref, opt, ant, sfc, bias
ref fields: height_ant, height_off, velocity, dist_arp_pivot, ignore_vec_apc_arp
setup_ok t=0.74
fwd_ok snr_len=250 snr_min=34.6240 snr_max=53.1458 snr_mean=45.9008
carrier −0.0137802–0.0166744 m；code −0.289898–0.140195 m
→ 上列为默认 `snr_fwd` 本机真值（移无效 MEX+测试桩 `.m` 后）；**非**论文插图拷贝
```

未移走 MEX 时更早失败：`interp2_linear_c.mex: invalid ELF header` 或 `wrong ELF class: ELFCLASS32`。

### 4.3 有 MATLAB 时的检查清单

1. `run init.m`  
2. `snr_fwd` 默认出图应非空  
3. `script/figA3`（或任选）对比 `image/`  
4. 改 `height_ant`、介电、天线型号，看 SNR 振荡周期变化（**幅度以你本机图为准**）

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `sett` | `snr_settings` 结构：卫星弧、天线、地表、偏置 |
| 天线数据 | `lib/snr/data/ant/`（扩展格式受 `load_extended` 控制） |
| 无 RINEX | 纯几何/电磁前向；观测分析另接 [georinex](./georinex.md) |

| 输出 | 说明 |
| --- | --- |
| `result.*` | 直达/反射 phasor、时延、功率等（见 `help snr_fwd`） |
| `snr_db` | 干涉 SNR |
| `carrier_error` / `code_error` | 多路径误差 (m) |
| 图窗 / `image/*.png` | 论文参考图（非本机新算） |

## 6. 参数速查

| 字段/开关 | 作用 |
| --- | --- |
| `sett.ref.height_ant` | 天线高；控制振荡频率 |
| `sett.sat.elev.min/max/rate` | 仰角采样；rate 越大越快越粗 |
| `sett.ant.model` / `radome` | 默认 `TRM29659.00` / `SCIT` |
| `sett.ant.load_extended` | 扩展方向图；与 densemap 相关 |
| `sett.sfc.*` | 地表类型/分层/粗糙度（详 `help snr_settings`） |
| `graphics_toolkit` | Octave：`gnuplot` 偏稳，`qt` 偏好看 |

## 7. 接到哪步

1. 理解 MP 振荡 → 本文；对照实测码 MP → [gnss-multipath-analysis](./gnss-multipath-analysis.md)  
2. 反射测高反演 → [gnssrefl](./gnssrefl.md)（反问题；本文是正问题）  
3. 站观测准备 → [georinex](./georinex.md) / [gfzrnx](./gfzrnx.md)；坐标 → [rtklib](./rtklib.md)  
4. 数据与文献 → [data-access](../data-access.md)；引用仓内两篇 *GPS Solut.* 2014 DOI

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `invalid ELF header` 加载 `.mex` | 预编译不是本机 Octave/64 位产物 | 移走 `.mex`；MATLAB 用匹配 MEX；或 `mkoctfile` 重编 `.c` |
| 2 | `ELFCLASS32` / `mexglx` | 32 位 Linux MEX | 同上；勿强行 `ln -s mexglx mex` |
| 3 | `invalid call to script interp2_linear_c.m` | 同名文件只有 `%!test` 无 `function` | 移走该 `.m`，让 catch 走 `interp2` |
| 4 | `X should be regularly spaced`（纯 M 包装） | `interp2_linear_m` 假设规则网格 | 不要用简陋 wrapper；走官方 catch→`interp2` |
| 5 | `concatenation … struct … scalar`（写作） | 本 QC **未复现**；移 MEX+.m 后 `snr_fwd` 通 | 先移无效 MEX/测试桩；仍失败再换 MATLAB |
| 6 | `init_plot` / GUI 挂起 | 无显示、toolkit 不稳 | `--no-gui`；手写 `addpath`；`graphics_toolkit('gnuplot')` |
| 7 | 统计函数缺失 | 未 `pkg load statistics` | 装 `octave-statistics` 后 load；或 MATLAB |
| 8 | 把 `image/*.png` 当本机结果 | 图是发行物 | 正文写清“参考图”；只报道你本地算出的数组 |
| 9 | 与 teqc/MP12 数值对不上 | 前向模型 ≠ 观测组合定义 | 只比趋势/周期；定量用 [gnss-multipath-analysis](./gnss-multipath-analysis.md) |
| 10 | 当 GNSS-IR 反演工具 | 无 RINEX→RH 管线 | 反演用 [gnssrefl](./gnssrefl.md) |
| 11 | `height_ant` 与实测天线高混淆 | ARP/APC/支柱定义不同 | 对齐相位中心与反射面定义后再比 |
| 12 | tip 停留 2020 | 上游低活跃 | 锁定 **`61be627`**；改代码自担 |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 论文级多路径 SNR/误差前向 | **本文 mpsim**（优先 MATLAB） |
| 实测码多路径 / 周跳报告 | [gnss-multipath-analysis](./gnss-multipath-analysis.md) |
| GNSS-IR 反射器高度 | [gnssrefl](./gnssrefl.md) |
| 读/洗 RINEX | [georinex](./georinex.md) / [gfzrnx](./gfzrnx.md) |
| 定位引擎 | [rtklib](./rtklib.md) |

## 10. 相关

[gnss-multipath-analysis](./gnss-multipath-analysis.md) · [gnssrefl](./gnssrefl.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [rtklib](./rtklib.md) · [gps-sdr-sim](./gps-sdr-sim.md) · [data-access](../data-access.md) · [README](./README.md)

- Nievinski & Larson (2014) DOI:10.1007/s10291-013-0331-y（建模）  
- Nievinski & Larson (2014) DOI:10.1007/s10291-014-0370-z（开源说明）
