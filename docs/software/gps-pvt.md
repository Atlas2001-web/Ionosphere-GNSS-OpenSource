# gps_pvt · Ruby 驱动的 GNSS 单点定位（C++ 核心）操作手册

> fenrir-naru/gps_pvt：Ruby gem，C++ 核心取自 [ninja-scan-light](https://github.com/fenrir-naru/ninja-scan-light)，经 SWIG 包装。**逐历元最小二乘单点定位**（SPP，非差分、非 RTK/PPP），读 RINEX 2/3 NAV/OBS/CLK、SP3、ANTEX、UBX（RXM-RAWX/SFRBX）、RTCM3、SUPL。
> 本篇实测：2026-09-26 03:52–04:06 EDT，Debian trixie box，Ruby 3.3.8。未在真接收机测试。

## 1. 用途边界

| 能 | 不能 / 未测 |
| --- | --- |
| RINEX OBS + NAV → 逐历元 CSV（位置、钟差、DOP、速度、逐星残差/权重/方位/仰角） | 差分、RTK、PPP、载波相位解算 |
| UBX 文件（RAWX+SFRBX）直接解，不必先转 RINEX | Galileo / BeiDou 测距（只 GPS、QZSS 默认；SBAS、GLONASS 用 `--with=` 开） |
| SP3 / RINEX CLK / ANTEX 换精密星历 | 双频无电离层组合（RINEX OBS 只认 `C1`/`C1C`，见 §7） |
| Ruby API：逐历元回调、改权重、剔星 | 串口 `/dev/tty*`、Ntrip、SUPL：**未在真接收机测试**，本篇只测文件 |

## 2. 版本事实

| 项 | 值 |
| --- | --- |
| RubyGems | **0.10.5**，2026-07-29 20:29 EDT；上一版 0.10.4（2024-12-15） |
| tag | `v0.10.5` = `14abd10`（2026-07-29 20:23 EDT）；共 45 个 tag |
| 默认分支 | **`master`**（不是 main）`6551a4c`，2026-08-22 03:14 EDT（"Modernize decompression of .Z; use gzip"），领先 tag 3 提交；另有 `sdr` 分支 |
| 许可证 | 仓库 `LICENSE` 实为 **BSD 3-Clause**（Copyright 2022 M.Naruoka），首行写"适用于无自带许可声明的文件"；`ext/ninja-scan-light` 各头文件自带 BSD 式声明。GitHub API 显示 `NOASSERTION`（推测因首行附注使 licensee 认不出） |
| ★ | 6（fork 6），2021-12-17 建仓 |
| Ruby | gemspec `required_ruby_version >= 2.3.0`；本机只测 3.3.8 |
| 原生扩展 | **要编译**（`ext/gps_pvt/extconf.rb`，SWIG 生成的 `GPS_wrap.cxx` 等 → `GPS.so`/`Coordinate.so`/`SylphideMath.so`）；需 g++、`ruby-dev` |
| 依赖 | ffi 1.17.4、rubyserial 0.6.0（自动装） |
| 可执行 | `gps_pvt`、`gps_get`、`gps2ubx` |

## 3. 安装

```bash
export TMPDIR=/tmp/gpspvt-man/tmp GEM_HOME=/tmp/gpspvt-man/gems PATH=/tmp/gpspvt-man/gems/bin:$PATH
sudo apt-get install -y --no-install-recommends ruby ruby-dev   # trixie: ruby 3.3.8, gem 3.6.7
gem install gps_pvt -v 0.10.5 --no-document                     # 55 s（含 C++ 编译），GEM_HOME 53 MB
export TZ=UTC                                                    # 必须，见坑 1
```

`--help` 不是合法选项：先把用法打到 stderr，再抛 `Unknown receiver options: [[:help, ""]] (RuntimeError)`，**退出码 1**。用法原文（节选）：

```text
Usage: .../exe/gps_pvt GPS_file1 GPS_file2 ...
As GPS_file, rinex_nav(*.YYn, *.YYh, *.YYq, *.YYg), rinex_obs(*.YYo), ubx(*.ubx), SP3(*.sp3), and ANTEX(*.atx) format are currently supported.
If you want to specify its format manually, command options like --rinex_nav=file_name are available.
In addition to --rinex_nav, --rinex_obs, --rinex_clk, --ubx, --sp3, --antex, --rtcm3, and --supl are supported.
Supported RINEX versions are 2 and 3.
A file having additional ".gz" or ".Z" extension is recognized as a compressed file.
Usage: .../exe/gps2ubx GPS_file ... > as_you_like.ubx      # RINEX OBS / RTCM3 → RXM-RAWX(+SFRBX)
Usage: .../exe/gps_get file_or_URI(s) ...                   # 取文件/URI/串口原样输出（含解压）
```

常用 `--key=value`（`receiver.rb` 源码）：`--elevation_mask_deg=10`（**默认 0°**）、`--with=GLONASS|SBAS|PRN`、`--without=PRN`、`--start_time`/`--end_time`、`--base_station=X,Y,Z`（出 rel_E/N/U）、`--online_ephemeris[=URL]`、`--weight=elevation|identical`（README 未列，见坑 5）。

## 4. 实测 A：RINEX（与 [sidereon](./sidereon.md) 同一份数据）

数据（BKG 免账号镜像 `igs.bkg.bund.de/root_ftp/`）：`IGS/obs/2026/258/WTZR00DEU_R_20262580000_01D_30S_MO.crx.gz`（hatanaka 2.8.1 解压，RINEX 3.04，Leica GR50，2880 历元）、`IGS/BRDC/2026/258/BRDC00WRD_R_…_MN.rnx.gz`（3.05）与 `BRDC00IGS_R_…_MN.rnx.gz`（3.04）、`IGS/products/2436/IGS0OPSRAP_20262580000_01D_15M_ORB.SP3.gz` + `…_05M_CLK.CLK.gz`。参考：`EUREF/products/2436/ASI0EPNRAP_…_SOL.SNX.gz` WTZR `STAX/Y/Z` = (4075580.2093, 931854.1652, 4801568.3539) m（标石，ARP 高 0.0710 m 未扣）。

```bash
gps_pvt --elevation_mask_deg=10 --rinex_nav=BRDCIGS258.rnx --rinex_obs=WTZR258.rnx > pvt.csv
```

stderr（真实）：

```text
Elevation mask: 10.0 deg
Read RINEX NAV file (BRDCIGS258.rnx): 11284 items.
Reading RINEX observation file (WTZR258.rnx).., 2880 epochs.
```

stdout 前 2 行（真实，`cut -d, -f1-2,8-12,16,17,29` 截列）：

```text
week,itow_rcv,sec_rcv_UTC,receiver_clock_error_meter,longitude,latitude,height,gdop,pdop,used_satellites
2436,172800.0,42.0,-0.38501420141382203,12.87892520262213,49.14420940509333,666.0973560074344,1.7402657200616343,1.5470291806244354,9
2436,172830.0,12.0,0.10754722495841779,12.878924058303397,49.14420930872265,666.2056794520468,1.7378797748391637,1.5450706135774641,9
```

`itow_rcv` 172800.0 = 2026-09-15 00:00:00 GPST，`sec_rcv_UTC` 42.0 是 UTC 的 23:59:42（前一天）。

统计（自写 Python 把 lat/lon/height 转 ECEF 再转参考点 ENU；`TZ=UTC`）：

| 输入 | 解率 | 平均用星 | 平均 ENU（m） | 水平 中位/95%（m） | 3D 中位/95%（m） | 耗时 |
| --- | ---: | ---: | --- | --- | --- | ---: |
| BRDC00IGS，掩膜 10° | 2880/2880 | 9.0 | (+0.087, +0.290, −0.947) | 0.770 / 1.444 | **1.357 / 3.269** | 4.57 s |
| BRDC00IGS，默认 0° | 2880/2880 | 10.8 | (+0.098, +0.269, −0.907) | 0.787 / 1.449 | 1.347 / 2.971 | 4.61 s |
| BRDC00WRD，掩膜 10° | 2880/2880 | 8.9 | (−0.064, +0.765, **+3.616**) | 0.872 / 2.155 | 3.989 / 6.415 | 4.58 s |
| BRDC00WRD，默认 0° | 2880/2880 | 10.7 | (−0.062, +0.779, +3.752) | 0.897 / 2.118 | 4.263 / 6.634 | 4.75 s |
| BRDC00WRD + `--with=GLONASS`，10° | 2880/2880 | 15.7 | (−0.119, +1.358, +3.625) | 1.622 / 3.980 | 4.441 / 8.421 | 5.62 s |
| BRDC00IGS + `--with=GLONASS`，10° | 2880/2880 | 15.8 | 与 GPS 行相同（逐历元差 ≤0.1 mm） | 0.770 / 1.444 | 1.357 / 3.269 | 5.76 s |
| SP3+CLK（BRDC00IGS 头），10° | 2851/2880 | 9.0 | (+1.313, +4.561, −6.232) | 6.402 / 15.912 | **11.290 / 23.989** | 6.52 s |
| SP3+CLK+ANTEX igs20（BRDC00WRD 头），10° | 2851/2880 | 9.0 | (+1.164, +5.079, −1.779) | 7.040 / 16.354 | 9.958 / 21.623 | 6.76 s |

- **BRDC00WRD 天向 +3.6 m 的原因**：该合并文件头**没有 `GPSA/GPSB IONOSPHERIC CORR`**，gps_pvt 不做 Klobuchar 且不告警；RTKLIB 同文件会退回内置默认系数。RTKLIB 关电离层（`ionoopt=off`）得 U +3.868 m、3D 4.158 m，与之吻合。换带 GPSA/GPSB 的 BRDC00IGS 即恢复。
- **SP3 反而差 7 倍**：插值本身没问题（G01/G05 三个时刻对 10 点拉格朗日差 ≤2 mm）。SP3+CLK 与广播两次运行的逐星平均残差差值与 BRDC 的 TGD×c 相关 0.60（斜率 0.79）→ **疑似精密钟模式未扣 TGD/DCB**（未改源码验证）。最后 29 历元（23:45:30 GPST 起，晚于 SP3 末历元）静默空行，不外推。
- 历元耗时约 1.6 ms；Ruby API 同任务 2.89 s（§6）。

## 5. 实测 B：UBX（rtkexplorer F9P 2020-12-24）

rtkexplorer「U-blox F9P kinematic PPP data set 12/24/20」zip（sha256 `fd9e58a1…ddf6f8`）内 `rover.ubx`（14071360 B，sha256 `ba2e782f…95156a`），真值同包 `rover_ppk.pos`（RTKLIB demo5 PPK，Q=1），按 GPST 线性插值到 `itow_rcv`。

```bash
gps_pvt rover.ubx > ubx.csv          # 8.59 s
```

```text
Reading UBX file (rover.ubx) ......, found packets are {[2, 19]=>92962, [2, 21]=>4521}
```

首个有解行（真实，截列 `1-2,8-12,29`）；前 25 行位置列为空（等星历）。F9P 的 Galileo/GLONASS/BeiDou RAWX 全被忽略，平均只用 8.9 颗 GPS：

```text
week,itow_rcv,sec_rcv_UTC,receiver_clock_error_meter,longitude,latitude,height,used_satellites
2137,422947.005,49.00500000000466,1433930.3920458828,-105.14726209595695,40.097033423025024,1582.6621885700151,9
```

`receiver_clock_error_meter` 1433930 m ≈ 4.78 ms：F9P 不驾驭钟，正常。

| 解 | 解数 | 3D 误差 中位 / p95 / max（m） | 水平中位 | 天向中位 |
| --- | ---: | --- | ---: | ---: |
| **gps_pvt 0.10.5 UBX，全程** | 4496/4521（首解 21:29:07 GPST，首个 RAWX 后 25 s） | **3.045 / 5.140 / 9.481** | 0.460 | +2.983 |
| gps_pvt UBX，前 400 历元（与 rt-navi 同窗） | 375/400 | 3.441 / 5.692 / 6.057 | 0.646 | +3.401 |
| gps_pvt UBX + `--rinex_nav=`（头补 GPSA/GPSB），全程 | 4521/4521 | 2.951 / 4.950 / 9.336 | 0.475 | +2.889 |
| 同上，前 400 历元 | 400/400 | 2.056 / 2.852 / 3.508 | 1.131 | +0.524 |
| gps_pvt RINEX 路径（convbin 2.4.3 转 obs + 补 GPSA/GPSB nav） | 4521/4521 | **1.010 / 2.325** / 8.397 | 0.629 | +0.175 |
| RTKLIB rnx2rtkp 2.4.3 单点 L1 GPS 10°（同 obs/nav） | 4521/4521 | 1.206 / 3.168 / 15.869 | 0.709 | −0.322 |
| F9P 自带 GGA（引 [rt-navi](./rt-navi.md)，383 历元） | — | 1.281 中位 | — | — |
| rt-navi 补丁 SPP + 只留 L1（引 [rt-navi](./rt-navi.md)） | 173/400 | 14.246 / 22.589 / 23.080 | 5.669 | +13.063 |

**UBX 路径的 +3 m 天向**：用 API 探测，`gps_space_node.is_valid_iono` 在第 614 历元（itow 423535.005）才因 SFRBX 第 18 页变真；但变真之后高程反而跳回"无电离层改正"水平（带 nav 的一次：前 578 历元高程中位 1577.98 m，424000 s 后 1579.39 m；RINEX 路径全程 ≈1576.4–1577.9 m）。解出的系数 α=[8.38e−9, −1.49e−8, −5.96e−8, 1.19e−7]、β=[94208, −131072, −131072, 851968] 填进 RINEX 头后 RINEX 路径正常。根因未查。结论：**UBX 直解比 rt-navi 好 4–5 倍，但比 F9P 自带解差约 2.4 倍；要 1 m 级请先 convbin 转 RINEX 再喂 gps_pvt**。

## 6. Ruby API（实跑）

```ruby
require 'gps_pvt'
rcv = GPS_PVT::Receiver.new(:elevation_mask_deg => '10')
rcv.parse_rinex_nav('BRDCIGS258.rnx')
n = ok = 0; nsat = 0
rcv.parse_rinex_obs('WTZR258.rnx'){|pvt, meas|
  n += 1
  next unless pvt.position_solved?
  ok += 1; nsat += pvt.used_satellites
  printf("%s lat=%.7f lon=%.7f h=%.3f pdop=%.2f\n", pvt.receiver_time.to_a.inspect,
    *[:lat, :lng].collect{|k| pvt.llh.send(k) / Math::PI * 180}, pvt.llh.alt, pvt.pdop) if n == 1
}
printf("epochs %d solved %d mean sats %.1f\n", n, ok, nsat.to_f / ok)
```

```text
[2436, 172800.0] lat=49.1442094 lon=12.8789252 h=666.097 pdop=1.55
epochs 2880 solved 2880 mean sats 9.0          # real 0m2.889s
```

参考点椭球高 666.027 m，`llh.alt` 是**椭球高**。README 里的 `solver.hooks[:relative_property]` 自定义权重在本机 Ruby 3.3.8 上**段错误**（坑 5），只用只读回调。

## 7. 交叉检查

- **RTKLIB 同数据**（`posmode=single`、`frequency=l1`、`elmask=10`、`ionoopt=brdc`、`tropopt=saas`、`navsys=1`）：BRDC00IGS 2880/2880，平均 ENU (+0.178, +0.257, −1.106) m，3D 1.489/3.089 m；gps_pvt 1.357/3.269 m；**逐历元两者位置差 中位 0.454 m、p95 1.179 m、max 2.393 m**。BRDC00WRD 时 RTKLIB 1.534/3.141 m（与 sidereon 篇一致）。SP3+CLK：RTKLIB 1.599/3.006 m，gps_pvt 11.290/23.989 m。
- **RINEX 字段**：首历元 11 颗 GPS 的 `L1_range(prn)` 与原文 `C1C` 逐值 max|Δ| = 0（如 G05 24265041.597 m）。gps_pvt 只把 `C1`/`C1C` 映射为 L1（正则 `/^1C?$/`），`C1W`/`C2W`/`C5Q` 不读。
- **UBX 字段 vs pyubx2 1.3.7**：首个 RXM-RAWX（week 2137，rcvTow 422922.005，numMeas 62）9 颗 GPS L1C/A 的 `prMes` 与 `L1_range` max|Δ| = 0；`L1_rate` = −doMes × λ_L1（G04：doMes −1109.248 Hz → 211.083 m/s）。

## 8. 错误用例（`TZ=UTC`；标「合成」者为本地构造）

| 用例 | 退出码 | 表现 |
| --- | ---: | --- |
| 空 OBS 或空 NAV（合成，0 B） | **134** | C++ `std::out_of_range … __pos (which is 60) > this->size() (which is 0)`，abort |
| 空 UBX（合成） | 0 | `found packets are {}`，stdout 0 行，**静默** |
| OBS 截断在历元中间（合成，前 15 MB） | 0 | 读 1410 历元全解，残缺尾历元静默丢 |
| UBX 截断（合成，前 3000037 B） | 0 | 915 历元 / 890 解，静默 |
| OBS 伪距坏字段 `25989XYZ.865`（合成，G07） | 0 | 被读成 **25989.0 m** 不报错；该历元无解（19/20） |
| NAV 坏字段 sqrtA=`abc.def`（合成，G07 全部 14 条） | **139** | 段错误 `receiver.rb:365: [BUG] Segmentation fault` |
| 错天星历（真实：DOY 250 BRDC 解 DOY 258） | 0 | 2880 行全空位置，`used_satellites=0`，**静默** |
| 观测不足 4 颗（合成：只留 G05/G07/G13） | 0 | 20 行全空位置，静默 |
| 只给 OBS 不给 NAV | 0 | 20 行全空，静默 |
| `.rnx.gz` NAV | 0 | 自动解压，结果与明文同 |
| `.crx.gz`（Hatanaka） | **134** | `basic_string::substr` 异常 abort；**不支持 CRX**，先 `crx2rnx` |
| 扩展名 `.rnx`（未加 `--rinex_obs=`） | 1 | `Format cannot be guessed, use --(format, ex. rinex_nav)=BRDC258.rnx` |
| UBX 中段 50 个 RAWX 校验和翻转（合成） | 0 | 4471 历元，坏包**静默跳过**、无告警 |
| UBX 开头 50 个（或全部）RAWX 校验和坏（合成） | 1 | `guess_leap_seconds: Wrong arguments for overloaded method` 线程异常 |
| 文件不存在 | 1 | `No such file or directory @ rb_sysopen - nonexist.rnx (Errno::ENOENT)` |
| 未知选项 `--foo=1` / `--help` | 1 | `Unknown receiver options: [[:foo, "1"]]` |

## 9. I/O

- 输入：按扩展名猜（`.YYo/.YYn/.YYg/.YYh/.YYq/.ubx/.sp3/.atx`，可再加 `.gz/.Z`）；RINEX 3 长文件名 `.rnx/.clk` **猜不出**，必须 `--rinex_obs=` 等显式指定。CLI 里文件顺序无所谓（OBS 写在 NAV 前也 20/20 解）；API 里须先 `parse_rinex_nav` 再 `parse_rinex_obs`（UBX 自带星历可省）。CRX 先解：`crx2rnx` 或 `python -c "import hatanaka; …"`。
- 输出：stdout CSV，1 行表头 + 每历元 1 行（无解也有行，位置列空），WTZR 全天 376 列、6.3 MB。列：`week,itow_rcv`（GPST）、`year…sec_rcv_UTC`（**UTC 日历**，比 GPST 少 18 s）、`receiver_clock_error_meter`、`longitude,latitude`（度）、`height`（椭球高 m）、`rel_E/N/U`（仅 `--base_station`）、GDOP…TDOP、σ、`v_north/v_east/v_down`、`used_satellites`、PRN 位图、GPS 1–32 与 QZSS 193–202 每星 6 列（残差/权重/方位/仰角/slopeH/slopeV）、`wssr…`、每星 `L1_range/L1_rate`。GLONASS 参与解算但**不出逐星列**。
- stderr：每次运行都先打整段 Usage，再打读文件进度；脚本判错看退出码，不要看 stderr 是否为空。

## 10. 坑

1. **时区 bug**：在有夏令时的 `TZ`（box 默认 America/New_York）下，SP3/RINEX CLK/GLONASS 星历时间偏 1 h。实测 `SP3#position(G01, 01:00 GPST)` 返回 00:00 的值；SP3 解 3D 中位 **3115 km**；`--with=GLONASS` 1001 历元后段错误。GPS 广播解逐字节不受影响（两边同偏）；2020-12 UBX 在冬令时下也一致。`TZ=UTC` 或 Asia/Tokyo 正常。**一律 `export TZ=UTC`**。
2. NAV 头缺 `GPSA/GPSB`（如 BKG `BRDC00WRD`）→ 不做电离层改正、不告警，天向 +3.6 m。用 `BRDC00IGS` 或站点 `_GN` 文件。
3. UBX 直解天向 +3 m（§5），SFRBX 电离层页生效后反而退化；精度优先走 convbin→RINEX。
4. SP3+CLK 模式比广播差（疑缺 TGD）；SP3 末历元之后不外推、静默空行。
5. `--weight=elevation` / `--weight=identical` 与 API `hooks[:relative_property]` 在 Ruby 3.3.8 上段错误（exit 139），GPS-only 也崩。其他 Ruby 版本未测。
6. GLONASS 权重随 NAV 源变：BRDC00IGS 下加 GLONASS 位置几乎不变（≤0.1 mm），BRDC00WRD 下水平变差到 1.622 m。未查因，默认别开。
7. 只读 L1 C/A（`C1C`）；Galileo/BeiDou 观测直接丢，不报。
8. 坏伪距字段按前缀数字读（`25989XYZ.865` → 25989.0）不报错；坏 NAV 字段段错误。
9. `--help` 退出码 1；默认掩膜 0°。

## 11. 选型

| 需求 | 选 |
| --- | --- |
| 要 Ruby 脚本里逐历元拿 PVT/DOP/残差，GPS L1 单点即可 | **gps_pvt**（`TZ=UTC`、NAV 带 GPSA/GPSB） |
| 标准后处理 SPP/RTK/PPP、多系统、双频 | [RTKLIB](./rtklib.md)（同数据 3D 1.489 m，SP3 模式也正常） |
| Rust 库、多系统 SPP | [sidereon](./sidereon.md)（同 WTZR 数据 GPS 1.983 m）、[gnss-rtk](./gnss-rtk.md) |
| u-blox 串口实时 PVT（Rust PoC） | [rt-navi](./rt-navi.md)（同 `rover.ubx` 14.246 m，需补丁） |
| 只解析/构造 UBX 字段，不定位 | [pyubx2](./pyubx2.md)（本篇用它逐值核对 RAWX） |
| UBX → RINEX | RTKLIB `convbin`、[ubx2rinex](./ubx2rinex.md)；gps_pvt 只有反向 `gps2ubx` |

未测：串口/Ntrip/SUPL 实时输入、`gps2ubx`/`gps_get` 输出核对、`--online_ephemeris`、RTCM3 文件、SBAS 测距、RINEX 2 输入、Windows/其他 Ruby 版本、速度解精度。
