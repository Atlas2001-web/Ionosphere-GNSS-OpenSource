# prx · RINEX 3 观测 → 逐星逐信号 CSV（卫星状态 / 钟差 / 改正项）操作手册

> jtec/prx：Python 预处理器。输入 RINEX 3.0x 观测（+ 广播星历），输出**每历元 × 每卫星 × 每码信号一行**的 CSV：原始观测值加卫星位置/速度、钟差、相对论项、TGD、Sagnac、对流层、Klobuchar 电离层、仰角/方位角。它**不解算**位置，但给了最小二乘示例函数（`prx.user.spp_pt_lsq`）。
> 本篇实测：2026-09-26 04:08–04:24 EDT，Debian box（系统时区实为 `Etc/UTC`），uv 托管 Python 3.13.15。未测 `--prx_level 3`（PPP 精密产品）。

## 1. 用途边界

| 能 | 不能 / 未测 |
| --- | --- |
| RINEX 3.0x OBS（`.rnx` / `.crx` / `.gz` / `.zip`）→ CSV | RINEX 2（仓里转换器是空壳，见 §6）、RINEX 4 OBS/NAV |
| 广播星历 G/E/C/R（开普勒 + GLONASS 积分）算卫星状态 | NavIC（I）与 SBAS（S）行：本例全部丢弃 |
| level 1（RTK 用，无改正）/ level 2（SPP，默认）/ level 3（SP3+ATX+BIA） | level 3：**未测**（产品只走 ESA FTP） |
| `prx.user` 里的单点最小二乘、Doppler 测速示例 | 命令行不出位置；无 Parquet 输出（本版只写 CSV） |

## 2. 版本事实

| 项 | 值 |
| --- | --- |
| 仓库 | github.com/jtec/prx，默认分支 `main` = `20a2382`（2026-09-14 16:48 EDT，"satellite phase wind up computation (#239)"），共 182 提交 |
| tag / release | **无**；`pyproject.toml` 写 `version = "0.0.1"`（uv-dynamic-versioning） |
| 许可证 / ★ | MIT / 23（fork 9，open issue 19），2021-11-03 建仓 |
| Python | `requires-python = "<3.14,>=3.10"`；`[tool.uv] python-preference = "only-managed"` |
| 主要依赖（uv.lock 实装） | pandas 2.2.3、numpy 2.2.2、polars 1.31.0、pyarrow 21.0.0、astropy 6.1.7、scipy 1.15.1、hatanaka 2.8.1、georinex 1.16.2（锁 git rev `95ef1d8`）、joblib、gitpython、matplotlib、plotly |
| 入口 | `python src/prx/main.py`；`[project.scripts] prx = "prx:main"` **坏的**（§3） |
| PyPI | 名为 `prx` 的包（0.1.1，简介 "Add your description here"）**是无关项目**，别 `pip install prx` |

## 3. 安装

```bash
export TMPDIR=/tmp/prx-man/tmp UV_CACHE_DIR=/tmp/prx-man/uvcache UV_PYTHON_INSTALL_DIR=/tmp/prx-man/uvpy
git clone https://github.com/jtec/prx.git /tmp/prx-man/src && cd /tmp/prx-man/src   # 克隆 276 MB（含测试数据）
uv sync --no-dev                                   # 自动下载托管 CPython 3.13.15；.venv + 缓存共约 1 GB
.venv/bin/python src/prx/main.py --help
```

`--help` 原文（前面还会打两条 `SyntaxWarning: invalid escape sequence '\.'`，来自 `util.py:43/51`，无害）：

```text
usage: prx [-h] --observation_file_path OBSERVATION_FILE_PATH
           [--prx_level {1,2,3}] [--analysis_center {cod,gfz,grg,wum}]
           [--tropo {saastamoinen,unb3m}]
           [--log-level {debug,info,warning,error,critical}]

prx processes RINEX observations, computes a few useful things such as
satellite position, relativistic effects etc. and outputs everything to a text
file in a convenient format.
...
P.S. GNSS rules!
```

`.venv/bin/prx --help` → `TypeError: 'module' object is not callable`，exit 1（入口指向模块 `prx.main` 而不是函数）。一律用 `python src/prx/main.py`。

## 4. 命令与真实输出

数据（BKG 免账号 HTTPS `igs.bkg.bund.de/root_ftp/`，与 [sidereon](./sidereon.md)、[gps-pvt](./gps-pvt.md) 同源）：`IGS/obs/2026/258/WTZR00DEU_R_20262580000_01D_30S_MO.crx.gz`（RINEX 3.04，Leica GR50，2880 历元）、`IGS/BRDC/2026/258/BRDM00DLR_S_20262580000_01D_MN.rnx.gz`。参考坐标：`EUREF/products/2436/ASI0EPNRAP_20262580000_01D_01D_SOL.SNX.gz` WTZR `STAX/Y/Z` = (4075580.2093, 931854.1652, 4801568.3539) m（标石；ARP 高 0.0710 m 未扣）。

**星历必须自己放进观测文件所在目录**（原因见坑 3）。`BRDC00IGS` 与 `BRDC00WRD` 这一天都会让 georinex 报 `ValueError: System I NAV data is not the same length as the number of fields.`，只有 `BRDM00DLR_S` 能用。

```bash
cd /tmp/prx-man/runA        # 目录里只放：观测 + BRDM00DLR_S_20262580000_01D_MN.rnx.gz
/tmp/prx-man/src/.venv/bin/python /tmp/prx-man/src/src/prx/main.py \
  --observation_file_path WTZR00DEU_R_20262580000_02H_30S_MO.rnx   # 00–02 时裁剪版，240 历元
# 日志要点（UTC）：
# 08:12:48 Uncompressed BRDM00DLR_S_20262580000_01D_MN.rnx.gz to BRDM00DLR_S_20262580000_01D_MN.rnx
# 08:12:48 gfzrnx binary not found (try adding it to PATH), skipping repair...
# 08:13:57 Computing times of emission in satellite time      ← 冷启动解析 NAV 约 69 s
# 08:14:01 Generated CSV prx file: <_io.TextIOWrapper name='WTZR00DEU_R_20262580000_02H_30S_MO.csv' ...>
```

| 运行 | 耗时（墙钟） | 输出 |
| --- | --- | --- |
| 2 h，冷缓存 | 76.0 s | 239 历元、**36346 行**、11.5 MB |
| 全天 `.rnx`，NAV 已缓存 | 25.5 s（其中读观测 8.3 s） | 2879 历元、**434766 行**、138029388 B |
| 全天 `.crx.gz` 直喂 | 14 s（缓存全热） | 行数同上 |
| 2 h，`--prx_level 1` | 4.7 s | 36346 行、23 列（无 bias/sagnac/tropo/iono） |

输出第 1 行是 JSON 注释头，第 2 行列名（level 2，27 列）：

```text
# {"approximate_receiver_ecef_position_m": [4075580.8863, 931853.5784, 4801567.9707], "input_files": [{"name": "WTZR00DEU_R_20262580000_02H_30S_MO.rnx", "murmur3_hash": "a4aea00160c25a166e4a8bb8f16fc71b"}, {"name": "BRDM00DLR_S_20262580000_01D_MN.rnx", "murmur3_hash": "f2a9eb033de9a18509ab84ef76563b50"}], "prx_git_commit_id": "unknown", "prx_level": 2, "processing_start_time": "2026-09-26 08:12:48.216", "processing_time": "0 days 00:01:12.972751"}
time_of_reception_in_receiver_time,sat_code_bias_m,sat_clock_offset_m,sat_clock_drift_mps,sat_pos_x_m,sat_pos_y_m,sat_pos_z_m,sat_vel_x_mps,sat_vel_y_mps,sat_vel_z_mps,ephemeris_hash,health_flag,relativistic_clock_effect_m,sagnac_effect_m,tropo_delay_m,carrier_frequency_hz,iono_delay_m,sat_elevation_deg,sat_azimuth_deg,rnx_obs_identifier,C_obs_m,D_obs_hz,L_obs_cycles,LLI,S_obs_dBHz,constellation,prn
2026-09-15 00:00:30.000000,-3.210840,-67330.925886,-0.000954,-10285108.390254,-12223307.156838,21889820.176272,2321.468487,-1236.849417,375.093517,2467840257573081771,0.000000,3.651199,9.786192,31.139027,1575420000.000000,4.605919,4.092146,-21.862021,1C,25976744.361000,2161.543000,136508709.774000,0.000000,37.150000,G,07
```

2 h 行数按系统：C 12361 行/16 星、E 9218/13、G 9061/14、R 5706/13；I、S 零行。第一个历元 00:00:00 不在输出里（坑 5）。

### 4.1 用仓内最小二乘示例做单点定位

仓库没有命令行 SPP，`src/prx/test/test_main.py` 里是逐历元调用 `prx.user.spp_pt_lsq(df)`（伪距改正式：`C + sat_clock_offset + relativistic − sagnac − iono − tropo − sat_code_bias`，每星座一个钟差）。照测试写法：仰角 >10°、`health_flag == 0`、单频信号，全天逐历元（核心几行）：

```python
from prx import user
df, md = user.parse_prx_csv_file("WTZR00DEU_R_20262580000_01D_30S_MO.csv")
df = df[(df.sat_elevation_deg > 10) & (df.health_flag == 0)]
sub = df.query("(constellation == 'G') and (rnx_obs_identifier in ['1C'])")
for t, g in sub.groupby("time_of_reception_in_receiver_time"):
    x = user.spp_pt_lsq(g.copy())      # x[:3] = ECEF 位置（m），x[3:] = 各星座接收机钟差（m）
    # 与 SINEX 参考坐标求 ENU 差 → 统计
```


| 信号选择 | 解 | 3D 中位 / 95% | 水平中位 | ENU 平均（m） |
| --- | --- | --- | --- | --- |
| GPS `1C` | 2879 历元，9.0 星 | **1.608 / 3.028 m** | 0.883 m | (+0.160, +0.531, −1.093) |
| G `1C` + E `1C` + C `2I` | 2879，26.1 行 | **1.467 / 2.663 m** | 0.855 m | (+0.186, +0.599, −1.130) |
| 再加 R `1C`（原样） | 2879，候选 32.5 行 | 1.467 / 2.663 m（与上行**完全相同**） | — | — |
| 加 R `1C`，R 的 `sat_code_bias_m` 补 0 | 2879 | 1.571 / 3.866 m | 0.943 m | (+0.064, +0.606, −1.092) |

同站同日、同为 GPS 广播星历（但用 BRDC00IGS）：[gps-pvt](./gps-pvt.md) 记 1.357/3.269 m，RTKLIB 2.4.3 记 1.489/3.089 m（引用，未在本篇重跑）。脚本 3 组共 41 s。

### 4.2 时区

默认（UTC）与 `TZ=America/New_York` 各跑一次 2 h：CSV 正文**逐字节相同**；只有头里的 `processing_start_time` 跟着本地墙钟走（08:12 对 04:15，且不带时区）。

## 5. 交叉检查（独立实现）

自写脚本：**自写** RINEX 3 NAV 解析 + 开普勒轨道/钟差（G、E I/NAV、C 非 GEO；与 prx 同样选 toe ≤ 发射时刻的最近一组），观测值用 **georinex** 重读（prx 读观测走自己的解析器）。仰角用头里 `APPROX POSITION XYZ`（prx 也用它）。全天 CSV 随机抽 200 行（`random_state=258`；C 74 / G 68 / E 58，196 个历元）：

| 量 | \|prx − 独立\| 中位 | 最大 |
| --- | --- | --- |
| 伪距 `C_obs_m` vs georinex | 0 m | 0 m |
| 卫星位置 3D | 1.45 mm | 3.15 mm |
| `sat_clock_offset_m` vs c·(a₀+a₁Δt+a₂Δt²) | 2.6×10⁻⁷ m | 5.0×10⁻⁷ m |
| `relativistic_clock_effect_m` vs c·F·e·√A·sin E | 2.7×10⁻⁷ m | 4.9×10⁻⁷ m |
| `sat_elevation_deg` | 2.5×10⁻⁷ ° | 5.0×10⁻⁷ ° |
| `sat_code_bias_m` vs c·TGD（E1 用 BGD E5b/E1） | 2.6×10⁻⁷ m | 4.9×10⁻⁷ m |

钟差、仰角、TGD 的差就是 CSV 固定 6 位小数的舍入。符号：钟差、相对论项与伪距**同向相加**，TGD 相减。GLONASS 轨道、对流层、电离层未做独立核对（未测）。

## 6. 错误用例（2 h 文件 + BRDM 星历；「合成」= 人工改过的文件）

| 输入 | 退出码 | 表现 |
| --- | --- | --- |
| 空文件（合成） | 1 | `TypeError: expected str, bytes or os.PathLike object, not NoneType` |
| 截到 1.3 MB（合成，停在记录中间） | **0** | 静默：120 历元 / 17152 行，半截的末历元照样输出 |
| RINEX 2.11（仓内真文件 `tlse001b.23o`） | 1 | 同上 `TypeError`（`rinex_2_to_rinex_3` 直接返回 None） |
| RINEX 4.00 OBS（合成：只改版本行） | 1 | 同上 `TypeError` |
| RINEX 4.02 NAV（真 `BRD400DLR_S`） | 1 | 日志 `still not RINEX 3, giving up.`，被跳过，转去自动下载，下到 BRDC00IGS 后报 `ValueError: System I NAV data ...` |
| `.crx.gz` 全天 | 0 | 正常；输入旁留下 `.crx` 和 `.rnx` 两个中间文件 |
| 目录里没星历（真，走自动下载） | 1 | 第一次：ESA FTP `urllib.error.URLError: <urlopen error [Errno 111] Connection refused>`；FTP 通了以后：下到的 BRDC00IGS 同样报 `ValueError: System I ...` |
| 只有前一天星历（真 BRDM 2026-257） | **0** | 静默：只剩 1 个历元（00:00:00）149 行 |
| BRDC00IGS 2026-258（真） | 1 | `ValueError: System I NAV data is not the same length as the number of fields.` |
| 伪距字段写成字母（合成） | 1 | `ValueError: could not convert string to float: 'ABCDEFGHIJ.K'` |
| 删掉 `APPROX POSITION XYZ`（合成） | 1 | `KeyError: 'APPROX POSITION XYZ'` |
| `APPROX POSITION XYZ` 为 0 0 0（合成） | 1 | 本该走首历元自举，却报 `KeyError: "['sat_pos_x_m', ...] not in index"` |
| `TIME OF FIRST OBS` 标 GLO（合成） | 1 | `AssertionError: Time scales other than GPST not supported yet` |
| 短名 `wtzr2580.26o` | 0 | 正常，输出 `wtzr2580.csv`，36346 行 |
| 路径不存在 | 1 | `[ERROR] ... does not exist.` |

派生验证（合成）：从 BRDC00IGS 删掉 169 条 I 记录后可跑，2 h 出 37934 行（E 9718 / G 9387 / R 6468，比 BRDM 多），共有行卫星位置差中位 4×10⁻⁵ m。

## 7. I/O 字段（level 2）

| 列 | 含义 | 单位 |
| --- | --- | --- |
| `time_of_reception_in_receiver_time` | 接收机钟面接收时刻（GPST，字符串，μs 位） | — |
| `C_obs_m` / `L_obs_cycles` / `D_obs_hz` / `S_obs_dBHz` | RINEX 原值：伪距 / 载波相位 / 多普勒 / 载噪比 | m / 周 / Hz / dB-Hz |
| `LLI` | 相位失锁标志（跟 L 列走） | — |
| `rnx_obs_identifier` | 频段 + 跟踪码，如 `1C`、`2W`、`5Q`；**每个码观测一行** | — |
| `constellation` / `prn` | G/E/C/R；PRN 为两位字符串（`07`），pandas 默认读成整数 7 | — |
| `sat_pos_*_m` / `sat_vel_*_mps` | 发射时刻卫星 ECEF 位置/速度（**未**转到接收时刻坐标系） | m / m/s |
| `sat_clock_offset_m` / `sat_clock_drift_mps` | c × 广播钟差（不含相对论项）及其变率 | m / m/s |
| `relativistic_clock_effect_m` | 偏心率相对论项 | m |
| `sat_code_bias_m` | c × TGD/BGD × γ；R 全部、G `5Q`、E `6C`/`8Q`、C `1P`/`5P` 为空 | m |
| `sagnac_effect_m` | 地球自转改正（求解时从伪距减） | m |
| `tropo_delay_m` | Saastamoinen（默认）或 UNB3m 斜延迟 | m |
| `iono_delay_m` | NAV 头 GPSA/GPSB 的 Klobuchar，**所有星座**都用它，再乘 (f_L1/f)² | m |
| `carrier_frequency_hz` | 该信号载波频率（GLONASS FDMA 按频道号） | Hz |
| `sat_elevation_deg` / `sat_azimuth_deg` | 相对头里概略坐标；方位角范围 **−180…180°** | ° |
| `ephemeris_hash` | 所用星历的哈希，uint64（超出 int64） | — |
| `health_flag` | 广播健康字（C 取 SatH1）；**不过滤** | — |

读回用 `prx.user.parse_prx_csv_file(path)`（polars，`ephemeris_hash` 按字符串读）。

## 8. 坑

1. **PyPI 同名包**：`pip install prx` 装到的是无关的 0.1.1。要从 GitHub 装（uv sync，或 `pip install git+https://github.com/jtec/prx`，后者未测）。
2. **`prx` 命令行入口坏**：exit 1 `TypeError: 'module' object is not callable`。
3. **自动下载基本不可用**：先走 ESA `gssc.esa.int` 匿名 FTP，FTP 抛错**不捕获**，写好的 BKG HTTPS 兜底根本走不到；本机 FTP 时通时断。下到的 BRDC00IGS（2026-258）又因 NavIC 记录让 georinex 崩。而且下载文件放在**包目录** `prx/rinex_nav/nav_files/YYYY/DDD/`，会一直留着被下次复用。不需账号，但可靠做法是自己把 `BRDM00DLR_S_…_MN.rnx(.gz)` 放进观测目录。
4. **用户星历发现规则**：在观测文件父目录**递归** `rglob("*")`，凡是像 `XXXXXXXXX_X_YYYYDDDHHMM_01D_?N.rnx*` 的都算；有一个坏的就整次失败。日期从**文件名**第 13–19 位取，不看内容。
5. **丢首历元**：发射时刻 ≈ 接收 − 70 ms，00:00:00 历元落到前一天，前一天没星历就整历元静默丢掉（2880→2879）。只放前一天星历则反过来只剩这 1 个历元，exit 0。
6. **不设高度角掩膜、不过滤健康**：输出低到 1.06°；全天 2641 行 `health_flag ≠ 0`（R08/15/16/20、E14/E18）。自己筛。
7. **GLONASS 在示例 LSQ 里被静默丢掉**：R 的 `sat_code_bias_m` 全空，改正后伪距成 NaN 被丢，加不加 R 结果一样（§4.1）。补 0 才用上。
8. **没有合适星历的行直接删**：同一观测，BRDM 比（删掉 I 记录的）BRDC00IGS 少 1588 行，无提示。
9. **只写 CSV**：尽管依赖 pyarrow/polars，本版无 Parquet；全天 30 s 采样 138 MB。输出与输入同名 `.csv`，已存在则直接覆盖。
10. **到处写文件**：`.gz`、`.crx` 在输入旁解压；joblib 磁盘缓存在包目录 `prx/diskcache`（本例 71 MB）。只读目录或共享 site-packages 下要当心。
11. **前提断言**：`TIME OF FIRST OBS` 必须 GPS，`RCV CLOCK OFFS APPL` 必须 0；RINEX 2/4 OBS 只报 NoneType `TypeError`，不说原因。
12. **首次解析慢**：georinex 读 8 MB 混合 NAV 约 69 s，之后按文件内容哈希命中缓存。
13. **`prx_git_commit_id` 写 `unknown`**：从 clone 直接跑也这样，头里不能用来追溯版本。
14. 装了 `gfzrnx` 就会被自动调用去「修复」文件（本机没有，未测）。

## 9. 选型

| 你要… | 用 |
| --- | --- |
| 自己写估计器 / 机器学习，要「一行一观测 + 卫星状态 + 改正」的表 | **prx** |
| 只读 RINEX 进 xarray | [georinex](./georinex.md)（prx 读 NAV 就靠它） |
| Python 里 NavData + WLS，含 Android 原始测量 | [gnss_lib_py](./gnss_lib_py.md) |
| 直接出 SPP/RTK/PPP 解，成熟配置 | [rtklib](./rtklib.md) |
| Ruby 逐历元 GPS PVT/DOP/残差，或 UBX 直解 | [gps-pvt](./gps-pvt.md) |
| Rust 一步到位 OBS+NAV → 坐标 | [sidereon](./sidereon.md) |

prx 位置在 georinex（读）和 RTKLIB/gps_pvt/sidereon（解）之间：只算预测量，不给解。卫星状态与自写开普勒代码差在毫米级，可以直接当「广播星历真值表」用。

## 10. 未测

`--prx_level 3`（SP3/CLK/ATX/BIA，只从 ESA FTP 下）、`--tropo unb3m`、`--analysis_center`、gfzrnx 自动修复、`.zip` 输入、跨天观测、多天星历、GLONASS 轨道与对流层/电离层列的独立核对、`pip install git+…` 安装路径、Windows/macOS。
