# 软件操作手册索引

本目录共有 **100 篇**操作手册（合计 **22542 行**，`wc -l`，不含本索引）：命令、输入输出、坑、选型。不是教材正文。

概念课见 [`docs/tutorials/`](../tutorials/)。条目以 [`PROJECTS.json`](../../PROJECTS.json) 与 `lists/` 为准。

参数冲突时：**本机 `-h` / 上游 README > 本手册示例**。

---

## 并行写作状态（持续 QC 中）

| 角色 | 负责 | 勿抢 |
| --- | --- | --- |
| **软件手册质检**（本 bot） | 已短硬篇的**二遍质检补洞**（错 I/O、过时旗标、仍薄点）；优先 `georinex` / `rtklib` / `bnc` / `gfzrnx` / `pytecgg` | 勿大改「仍薄/缺篇」同事正在写的文件 |
| **软件用法讲解**（并行） | 写 **尚未短硬 / 缺篇** 新手册 | 勿重写下表已标「已短硬」全文（补丁可协调） |

**下一优先（质检二遍，按弱→强）：** **已质检复跑** `ntripcaster-libev`（2026-09-24 06:21 EDT；tip **`cc17929`**/`VERSION`=**1.1.0**；二进制 **74152** B；口 **2101**；空表 CL=**16**；在线 **STR;LAB1** CL=**111**；源 `ICY 200`=**12** B/`Bad Password`/`Bad Mountpoint`；客 `ICY 200`=**12** B/**401**；未知挂载→源表；占位透传 **match**；**未臆造 RTCM**；交叉 [cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[pygnssutils](./pygnssutils.md)/[data-access](../data-access.md)）。前序 **用法讲解新入库** `ntrip-cpp`（tip **`b431661`**/`1.2.0`；口 **8090**；源 `POST`→`HTTP/1.1 200`；客 `200`/`ICY 200`/`401`；`GET /`→**401**（源表死路径）；样例 Recv[**70**]=`kExmapleData`；两处 CMake/头补丁；交叉 [ntripcaster-libev](./ntripcaster-libev.md)/[cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[data-access](../data-access.md)/[pygnssutils](./pygnssutils.md)；**下一优先** `ntripserver`+`ntripclient` 或 `ntrip-go`（避开已入库篇））。前序  **已质检复跑** `iri-2026-package`+`iri-common-files`（2026-09-24 06:19 EDT；zip **1823544**/sha₁₂=`2377b0c07a43`/`unzip` **69**/解压 **5974782** B；COMMON **351482**/sha₁₂=`5427353c578f`；`cmp` **24/24**；indices **1402576**/**10559**；HEAD tar **CL=6025728**；**未重跑** fort.7→[iri-fortran](./iri-fortran.md)；交叉 [iri-fortran](./iri-fortran.md)/[pyiri](./pyiri.md)/[iri2016](./iri2016.md)）。前序 **用法讲解新入库** `ntripcaster-libev`（tip **`cc17929`**/`VERSION`=**1.1.0**；口 **2101**；空表→在线 **STR;LAB1**；源 `ICY 200`/`ERROR - Bad Password`；客 `ICY 200`/`401`；透传占位字节 **未臆造 RTCM**；交叉 [cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[data-access](../data-access.md)/[pygnssutils](./pygnssutils.md)；**下一优先** `ntrip-cpp`（避开已入库篇））。前序 **已质检复跑** `cors-relay`（2026-09-24 06:17 EDT；tip **`1238947`**/二进制 **188496** B；STR×**3**/CL=**390**；`ICY 200`=**12** B/**401**/未知挂载→源表；**无真源未臆造 RTCM**；交叉 [ntripcaster-libev](./ntripcaster-libev.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[pygnssutils](./pygnssutils.md)）。前序 **用法讲解新入库** `cors-relay`（tip **`1238947`**/`REPO`=`123894`/`2020-04-23`；Caster **8001–8003**/管理 **8000**；源表 STR×**3**；`ICY 200`/`401`；**无真源未臆造 RTCM**；交叉 [data-access](../data-access.md)/[pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[ntripbrowser](./ntripbrowser.md)；**下一优先** `ntripcaster-libev`（同作者播发端；避开已入库篇））。前序 **已质检复跑** `iri-fortran`+`nequick2-ictp`（2026-09-24 06:15 EDT；zip **1823544**/sha₁₂=`2377b0c07a43`；`iri` **1631368** B；fort.7 NmF2=**893124.7**/hmF2=**259.16**/Ne@250=**886713**/TEC=**25.8**/F10.7=**127.2**；NeQuick2 申请页 bnava@/yenca@/**无 zip**→**未编译未臆造 TEC**；交叉 [iri2016](./iri2016.md)/[pyiri](./pyiri.md)/[nequickg](./nequickg.md)）。前序 **已质检复跑** `gsilib`+`rtppp-b2b`（2026-09-24 06:12 EDT；IFB **1921**/C1C=**24070092.563**；`.c` **50**/顶层 **40**；RTPPP CRC **0**/`0x6131`/MT **1–7**/MISSING+`clock_orbit_rtcm.h`；两端均无解算二进制→**未臆造 stdout**）。前序  **用法讲解新入库** `gsilib`+`rtppp-b2b`（GSILIB **1.0.3**/IFB `tr02` **1921**/G01 C1C=**24070092.563**；**无 Wine32 未跑基线解**；RTPPP tip **`9864c66`**/CRC **0**/`0x6131`/MT **1–7**；**缺 BNC 未链接**；交叉 rtklib/pride-pppar/ginan · b2blib/navdecoder/haslib/cssrlib/madocalib）。前序 **质检新短硬** `pynmea2`+`pymap3d`（2026-09-24 06:04 EDT；pynmea2 **1.19.0**/tip **`fcd90dc`**/pytest **105**；北京 GGA lat=**39.90418716666667**/lon=**116.39074266666667**/qual=**1**/sats=**12**/alt=**44.0**；流 **36** 句；pymap3d **3.2.0**/tip **`033895e`**/pytest **397**/skip **11**；北京 ECEF **−2177813.332/4388956.908/4069858.556**；ENU n≈**111.034** m；无 Astropy ECI 警告；避开用法讲解 `cors-relay`/`gsilib`/`rtppp-b2b`）。前序 **质检新短硬** `minmea`+`ntripbrowser`（2026-09-24 05:45 EDT；minmea tip **`c43c9e7`**/check **38/38**；北京 RMC lat=**39.90418625**/lon=**116.39073944**；ntripbrowser **4.0.0**/`3730867`；rtk2go STR **764**/igs **384**/centipede **1269**；巴黎50km **14**/IPGP≈**0.71** km；**未订流**；避开用法讲解 `cors-relay`/`gsilib`/`rtppp-b2b`）。前序 **用法讲解新入库** `ublox_driver`（**1.0.0**/tip **`7961ab7`**；ROS1 catkin；launch×**1**/config×**2**/msg×**0**（gnss_comm）；exec **`ublox_driver`**+**`sync_system_time`**；`advertise`×**7**；**无 ROS/无 Rx** 未 catkin/launch；交叉 [ublox-dgnss](./ublox-dgnss.md)/[pyubx2](./pyubx2.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)/[swiftnav-ros2](./swiftnav-ros2.md)；**下一优先** `cors-relay`（避开已入库篇））。前序 **已质检复跑** `piksi_tools`+`swiftnav-ros2`（2026-09-24 05:42 EDT；JSON **61599**/PosLLH **4686**/n_sats=**15**/无 Rx **exit 1**；tip **`c35c6ef`** vs tag **`5c82573`**；launch×1/`sbp-to-ros`/**NO_ROS**；下一可 `ublox_driver`/`gpsd`/`cors-relay`）。前序  **用法讲解新入库** `gpsd`（Debian **3.25-5+deb13u2**/`/usr/sbin/gpsd: 3.25`；自写 Beijing NMEA→`gpsfake -P 2949`→`gpspipe -w` TPV **mode=3** lat=**39.904187167**/lon=**116.390742667**/altMSL=**44.0**/uSat=**12**/hdop=**0.9**；**无 Rx**/无 systemd 总线；交叉 [pynmeagps](./pynmeagps.md)/[pyubx2](./pyubx2.md)/[pygnssutils](./pygnssutils.md)/[ubx2rinex](./ubx2rinex.md)/[rtkbase](./rtkbase.md)/[bnc](./bnc.md)；**下一优先** `cors-relay`（避开已入库篇）。前序 **已质检复跑** `ppp-wizard`+`gogps-matlab`（2026-09-24 05:41 EDT；拒伪大小 SP3 **1.9 MB**/BIA **200 MB**（原稿 3.3/170）；`package.html` **404**；SP3 **288**/109；CLK AS **1883520**；BIA **2268516**；goGPS tip **`a990ed0`**/1.0.1；ZIM3 **2880**/C1C=**25131594.344**；两端均无客户端/MATLAB→**未臆造 PPP stdout**；下一可 `gpsd`/`cors-relay`/`ublox_driver`，勿抢用法讲解 gsilib/rtppp-b2b）。前序  **用法讲解新入库** `ublox_dgnss`（**0.7.6**/tip **`7ace9d5`**/tag **0.7.6**；六包同版；launch×**11**/config toml×**3**/msg×**65**/srv×**4**；exec **`ublox_dgnss_node`**；**无 ROS/无 Rx** 未 colcon/launch；交叉 [pyubx2](./pyubx2.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)/[swiftnav-ros2](./swiftnav-ros2.md)；**下一优先** `ublox_driver` 或 `gpsd`/`cors-relay`，避开 ppp-wizard/gogps-matlab WIP）。前序 **已质检复跑** `libswiftnav`+`ubx2rinex`（2026-09-24 05:39 EDT；LSN **250 PASSED**/`calc_ionosphere` **7.202448** m；ubx2rinex F9T **298**/G01 C1C=**21360867.696**；coldstart **561**+NAV **9**；下一可 `gpsd`/`cors-relay`/`ublox_dgnss`，避开 ppp-wizard/gogps-matlab WIP）。前序  **用法讲解新入库** `ubx2rinex`（crates.io **0.3.0**/tip **`3b67fd0`**；rustc **1.98.1**+libudev；F9T gz→OBS **298** 历元 G01 L1C=**112252116.071**/C1C=**21360867.696**/D1C=**804.339**；coldstart OBS **561**+NAV **9** eph G12 af0=**−5.816e−4**；pyubx2 无 RAWX→**0** 文件；交叉 [pyubx2](./pyubx2.md)/[pygnssutils](./pygnssutils.md)/[georinex](./georinex.md)/[rinex-cli](./rinex-cli.md)；**下一优先** `gpsd` 或 `cors-relay`（避开 ppp-wizard/gogps-matlab WIP））。前序 **用法讲解新入库** `libswiftnav`（tip **`19331e0`**/LGPL-3.0；CMake→`libswiftnav.a`；`do-all-tests` **250 PASSED**/24 suites；`calc_ionosphere` **7.202448** m；`wgsecef2llh` ≈37.4286N 122.1723W；对照 [libsbp](./libsbp.md) 协议≠数学；交叉 [piksi-tools](./piksi-tools.md)/[swiftnav-ros2](./swiftnav-ros2.md)/[gnsstk](./gnsstk.md)；**下一优先** `ublox_dgnss`）。前序  **用法讲解新入库** `swiftnav-ros2`（包 **`swiftnav_ros2_driver` 1.0.0**/tip **`c35c6ef`**/tag **v1.0.0**；launch×**1**/config×**1**/msg×**1**；exec **`sbp-to-ros`**；**无 ROS/无 Rx** 未 colcon/launch；交叉 [libsbp](./libsbp.md)/[piksi-tools](./piksi-tools.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)；**下一优先** `libswiftnav` 或 `ublox_dgnss`）。前序 **用法讲解新入库** `piksi_tools`（PyPI **4.0.0**/tip **`02f1532`**；`serial_link --file` JSON **61599**；`sbp_msg_2_csv` PosLLH **4686**/nonzero tow **4276** ≈37.7735°N 122.4179°W；roundtrip 对照 libsbp n_sats=**15**；**无 Rx**/Py3.13 `libsettings` 绕过；交叉 [libsbp](./libsbp.md)；**下一优先** `swiftnav-ros2`）。前序 **已质检复跑** `groops`+`rapppid`（2026-09-24 05:31 EDT；GROOPS tip `7e1bd6d`：Sp3Format2Orbit G01 **289**/300 s/gaps=0；OrbitAddVelocityAndAcceleration；GnssClockRinex2InstrumentClock `*.G01.G01.dat` 69182 B；georinex GRAZ **2880**/30；G07 C1C=25383647.774；`01`/`02` 缺 transmitterList/tides（data≈23 G）诚实边界；raPPPid **v5.1**/`28fd517`：CODE **633** `.m`（树 635）/9×`.mat`；OceanLoading **339510** B；无 MATLAB）；raPPPid **v5.1**/`28fd517`：633 `.m`/9 presets；**无 MATLAB** 未跑 GUI；交叉 pride-pppar/great-pvt/rtklib/ginan）。前序 **用法讲解新入库** `rtcm3torinex`（SVN **r9404**/WC **r11044**；本机 **2.9404**；`make` OK；euref STR **222**；centipede VALDM RINEX3 **43** 历元 G03 C1C=**25238622.890**；`-P` NAV **75** 行；rtk2go 无订户 **400**；门户 **obsolete→BNC**；交叉 pyrtcm/bnc/pygnssutils/ntrip-client；**下一优先** `piksi_tools` / `swiftnav-ros2`）。前序  **用法讲解新入库** `rinex-cli`（crates.io **0.12.1**/tip **`f4dd4c3`**/0.13.0；Rust RINEX-QC HTML；ACOR **25** 历元；ESBC `.crx.gz` **2880**；`filegen`/`-P`/`--gzip`；`tbin`/`split` 0.12.1 panic；交叉 georinex/rinexmod/hatanaka/crx2rnx/rnxcmp/teqc/gfzrnx/gnsspy/gnsstools；**下一优先** `rtcm3torinex` 或质检二遍）。前序  **已质检复跑** `graphgnsslib`+`great-pvt`（2026-09-24 05:21 EDT；去 `-s 1`；SPP 251×Q5 / RTK **94**×Q2；GODN 3D≈0.0062 m）。前序  **用法讲解新入库** `libsbp`（PyPI **`sbp` 6.5.2**/tip `2b883ad`；`sbp2json`+`one_msg` AcqResultDepA snr=16.2；roundtrip PosLLH ≈37.8312N 122.2865W n_sats=15；short **2382**/roundtrip **5000**；**无 Rx**；交叉 septentrio-gnss-driver/pyubx2/pyrtcm/pysbf2；**下一优先** `rtcm3torinex`）。前序  **已质检复跑** `crx2rnx`（2026-09-24 05:19 EDT；AJAC 26→17；ACOR C1C=GSI；ESBC gz；`765ddeb`）。前序  **已质检复跑** `ginan`+`rtkbase`（2026-09-24 05:16 EDT；Ginan dry-run+20 epoch ALIC≈0.08 m tip `5033996`；RTKBase ConfigManager+12 unit tip `2ce7ce0`；无 Pi/GNSS）。前序  **用法讲解新入库** `septentrio-gnss-driver`（**1.4.8**/tip `5613af2`；launch×3/config×4/msg×26；**无 ROS/无接收机** 未 colcon/launch；交叉 sbfparser/pysbf2/haslib；**下一优先** `libsbp` 或 `rtcm3torinex`）。前序 **用法讲解新入库** `ntrip-client`（crates.io **0.2.1**/tip `7d4c6d3`；Rust/tokio NTRIP；example CLI `simple-cli`；rtk2go **766**/igs-ip **384**/centipede **1270**；centipede VALDM 8 s **86** 帧；rtk2go 空响应/403；igs 401；交叉 ntripstreams/pygnssutils/bkg-ntripcaster/bnc/crx2rnx）。前序 **用法讲解新入库** `pysbf2`（1.0.5/`a68fe44`；纯 Python SBF；PVTCartesian 往返；pvtcart Type=6/NrSV=36；status CPULoad=28；examples 232；混流 NMEA+RTCM；MSGIDS=125 无 ISM；交叉 sbfparser/haslib/pyubx2）。前序  **用法讲解新入库** `ginan`+`rtkbase`（Ginan **v4.1.4**/`5033996`：预编译 `pea` dry-run OK；PPP `--max_epochs 20` ALIC/DARW/HOB2 `.POS`，ALIC 末历元相对 IGS20 ≈**0.08 m**；RTKBase **2.7.0**/`2ce7ce0`：ConfigManager+`install.sh --help`；**无 Pi/GNSS** 未启 systemd/NTRIP/Web）。前序  **用法讲解新入库** `crx2rnx`（crates.io **2.7.0**/tip `765ddeb`；Rust 仅解压；ACOR C1C G07=23818653.24=GSI；AJAC V2 丢星 17≠26；同名≠hatanaka 捆版；交叉 rnxcmp/hatanaka/rinexmod/georinex）。 **已质检复跑** `navdecoder`+`gnss-multipath-analysis`（HAS **801**/log **48288**/1.1 MB；B2b **7346/532/277**；NMBUS C1C **1.273/1.093**/周跳**47**/nEpochs**293**；2026-09-24 05:10 EDT）。前序  **用法讲解新入库** `gnss-downloader`（Mereithhh tip `e6d0d84`/V3.0；无下载 CLI；WHU 230+CWD、NLST 425；SIZE brdc=57792 / ABPO GN=29294；NASA 明文不可用→data-access Earthdata；交叉 gdds/gampii-good/fast）。 **用法讲解新入库** `DRCycleSlip`（tip `f57d74d`；三频组合注入–探测；BAKO G24 历元700→(23,18,17)；无 PyPI；硬编码 Windows 路径；交叉 cycle-slip-correction/georinex/anubis）。前序 **已质检复跑** `ismr-downloader`（0.2.0/`cca68e4`；缺参 exit 1；SSL + token **400**；登记门禁未落盘）。前序 **已质检复跑** `ntripstreams`+`gampii-good`（rtk2go STR765 / igs-ip STR384 / 订流 400；AgPartner_2 251；GOOD BRDC 11371068 B + atx skip）。前序 **已质检复跑** `claslib`+`b2blib`（dump 3601 / 3580 GGA；WUH2 9×Q=6）。前序 **用法讲解新入库** `ntripstreams`（0.3.5/`889ffb9`；NTRIP asyncio；rtk2go STR765 / igs-ip STR384；无订户订流 400；Rtcm3 样帧+AgPartner_2 251 帧；1029；交叉 pygnssutils/bkg-ntripcaster/bnc/pynmeagps/pyrtcm）。前序 **用法讲解新入库** `pyspartn`（1.1.0/`8fc58f8`；SPARTN 编解码；**无接收机/无 L-band**；传输层往返；OCB/GAD 样例解密；d9s 3007 帧；**无 CLI**→gnssstreamer；交叉 pyubx2/pynmeagps/pygpsclient/haslib/pyrtcm）。前序 **用法讲解新入库** `pyrtcm`（1.2.0/`5d66c7a`；RTCM3 编解码；README 1005 往返；RTCM3.log 11 帧；MSM `parse_msm`；**无 CLI**→gnssstreamer；交叉 pygnssutils/pyubx2/pynmeagps）。前序 **用法讲解新入库** `pyubx2`（1.3.6/`4abbfa6`；UBX 编解码；**无接收机**构造/样例；CFG-MSG/NAV-PVT/ACK 往返；上游 NAV 样例+mon_span 109 帧；**无 CLI**→gnssstreamer；交叉 pygnssutils/pygpsclient/pynmeagps/pyrtcm）。 停写门槛已近——剩余主要是 **登记/环境受限**（`anubis` / `ionomoni` / `iono-scintillation` / `gfzrnx`）无本机真实 I/O 可补；**sh-gim** 保持边界。**已质检复跑** `rinexmod`+`pyubx2`+`ionex-rs`+`madocalib`+`aacgmv2`+`gnsstk`+`teqc`+`pyrtcm` · **质检新短硬** `kamodo`（26.9.2；ΣH=9.1183）· **已短硬入库 `pyglow` + `iri2016` + `apexpy` + `msise00`**。**用法讲解已入库** `ionex-rs` + `madocalib` + `glab-upc` + `pynmeagps` + `gdds` + `gps-measurement-tools` + `pygpsclient`+ `cycle-slip-correction` + `diffionmap` + `cddis-highrate-downloader`。**已质检复跑** `glab-upc` + `pynmeagps` + `gdds` + `gps-measurement-tools` + `pygpsclient` + `gnss_lib_py` + `pyiri` + `pyirtam`+ `fast` + `diffionmap` + `cddis-highrate-downloader`（stdout 对齐；CDDIS LIST 425 已记）。**质检新短硬** `geospacelab`（0.14.8；OMNI SYM_H=-234 + Madrigal TEC max=114）。**用法讲解新入库** `gnsspy`（3.0.1；demo.10o→pandas G07 L1=118767195.326；converter 2→3；无 PyPI）。**已质检复跑** `gnsspy`（3.0.1/`e6879bf`；22×9/2×14；converter 2→3 OK；3→2 回写 Length mismatch 坑已补）。**用法讲解新入库** `gnsstools`（0.0.1/`e496093`；OBS/NAV/SP3 真 I/O；无 PyPI）。**用法讲解/原理课加厚入库** `aacgmv2`（2.7.1；mlat≈50.53 / mlon≈−4.09 / mlt≈10.09 @40N80W 250km）。**用法讲解新入库** `claslib` + `b2blib`（CLAS `1e3a75d`/0.8.4：dump header 3601 + test1 3580 GGA；B2b `fe7c4c0`：WUH2 5 min 9×Q=6）。**用法讲解新入库** `gnsstk` + `teqc`（库 15.3.1/`55ea334`；teqc 2019Feb25 +qc MP12≈0.20）。**用法讲解新入库** `rinexmod`（4.2.1；demo.10o→demo064a.10o MARKER MRKR→DEMO / AGENCY→IPGP；长名 DEMO00FRA…rnx.gz；hatanaka 时钟偏移坑已记）。
**sh-gim：** 保持短边界，禁止注水扩写。  
**停写条件：** 剩余皆 PASS，或仅剩 sh-gim 边界 / 登记受限且无进一步真实 I/O 增益。

---

## 全部手册 + 质检状态

| # | 手册 | 做什么 | 行数 | 状态 |
| ---: | --- | --- | ---: | --- |
| 1 | [georinex.md](./georinex.md) | RINEX → xarray / Python | 305 | **已短硬** R2+R7二遍 · 本机 1.16.2（补 NAV 实跑 I/O） |
| 2 | [gfzrnx.md](./gfzrnx.md) | RINEX 检查 / 拼接 / 抽稀 | 423 | **已短硬** R1+R8 guide [`099bf63`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/099bf63) · **登记受限**（无本机官方二进制；`-sifl` 坑已补；**禁臆造 stdout**） |
| 3 | [anubis.md](./anubis.md) | 观测 QC → XTR/XML | 239 | **已短硬** R6 [`8fe8b6d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/8fe8b6d) · **登记受限**（Free 需注册；无本机 Linux 二进制） |
| 4 | [pytecgg.md](./pytecgg.md) | 校准 sTEC/vTEC（作者 viventriglia） | 593 | **已短硬** R1+R8二遍 [`ff674b4`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/ff674b4) · 本机 1.3.0（ABMF 全日 `calculate_tec`/`veq` 实跑） |
| 5 | [ionomoni.md](./ionomoni.md) | STEC / ROTI / AATR（C++） | 219 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · **登记受限**（官方主推 Win；Linux 无开箱二进制） |
| 6 | [oasis-roti.md](./oasis-roti.md) | ROTI / ΔTEC / SIDX（Python） | 224 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · 本机 pyOASIS 1.0.3 |
| 7 | [ionex-gim.md](./ionex-gim.md) | 读 IONEX GIM | 200 | **已短硬** R3 [`f5845f7`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/f5845f7) · 本机 ionex 0.2 |
| 8 | [sh-gim.md](./sh-gim.md) | 维护者球谐仓**边界**（求解器未开源） | 124 | **边界** · 保持短；禁止扩写成端到端求解教程 |
| 9 | [pygnssutils.md](./pygnssutils.md) | NTRIP CLI / 小 caster | 361 | **已短硬** R5 [`37ac39b`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/37ac39b) · 本机 1.2.7 |
| 10 | [bnc.md](./bnc.md) | BKG 多流客户端 | 274 | **已短硬** R2+R7二遍 · 本机 BNC 2.13.7（REQC 实跑 / NTRIP 标操作步骤） |
| 11 | [bkg-ntripcaster.md](./bkg-ntripcaster.md) | BKG Caster 播发 | 379 | **已短硬** R4 [`bfcd626`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/bfcd626) · 本机 2.0.49 |
| 12 | [rtklib.md](./rtklib.md) | RTK / PPP CLI | 287 | **已短硬** R1+R7二遍 · apt 2.4.3 b34 / EX 2.5.1（PATH 陷阱已写清） |
| 13 | [pride-pppar.md](./pride-pppar.md) | PPP-AR | 289 | **已短硬** R6 [`8fe8b6d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/8fe8b6d) · 本机 3.2.11（`-V`/`-H`/会话头实跑；WUM FTPS 未出解） |
| 14 | [cssrlib.md](./cssrlib.md) | Python PPP / PPP-RTK（CLAS/HAS/BDS） | 243 | **已短硬** R9二遍 · 本机 1.2.1（`nav.t` 坑已补；SPP 60 历元复跑；CLAS/HAS 未跑完） |
| 15 | [gnss-tec.md](./gnss-tec.md) | RINEX → 相对斜 TEC | 198 | **已短硬** R9二遍 · 本机 1.1.1（stdout 对齐脚本；type N NAV 坑） |
| 16 | [pinot.md](./pinot.md) | “not only TEQC” QC/预处理批壳 | 287 | **已短硬** R9二遍 · orderfile/sitecheck/metacheck/subnet/low2upper 复跑；qualitycheck 无 Linux teqc |
| 17 | [autorino.md](./autorino.md) | 厂商 RAW 拉取 → RINEX3/4 | 246 | **已短硬** R9二遍 · 本机 2.4.2 cfgfile_check 复跑；check_rnx `figure_saver` 实错已记；convert 环境受限 |
| 18 | [iono-scintillation.md](./iono-scintillation.md) | MATLAB 闪烁仿真 | 197 | **已短硬** R2 [`246103d`](https://github.com/Atlas2001-web/Ionosphere-GNSS-OpenSource/commit/246103d) · **环境受限**（质检机无 MATLAB；不臆造控制台） |
| 19 | [rnxcmp.md](./rnxcmp.md) | GSI 官方 Hatanaka CRX 压缩/恢复 | 200 | **已短硬** R10质检 · 本机 RNXCMP **4.2.0** 复跑（body 相等；gzip≈1830；`-h` exit 1）；Python 见 [hatanaka](./hatanaka.md) |
| 20 | [hatanaka.md](./hatanaka.md) | Python Hatanaka CRX↔RNX（pip） | 251 | **已短硬** · 本机 hatanaka **2.8.1** / 捆 RNXCMP 4.1.0；`rinex-decompress`/`compress`+georinex 实跑；官方二进制 → [rnxcmp](./rnxcmp.md) |
| 21 | [nequickg.md](./nequickg.md) | Galileo NeQuick-G（Python 社区） | 203 | **已短硬** R10质检 · Py3 移植后 vTEC+Medium 行0/全表36 复跑；`Validation.py` map/plt 坑已补；官方 C 登记受限 |
| 22 | [haslib.md](./haslib.md) | Galileo HAS 解码（SBF/BINEX→SSR） | 170 | **已短硬** R11质检 · 本机 `galileo_has_decoder` **1.0.2**；`-x 3000 -v 1` → 11 HAS；RTCM 9780 / IGS 9800；`-m`/`-h` 坑已补 |
| 23 | [laika.md](./laika.md) | comma.ai 轻量 Python GNSS | 194 | **已短硬** R11质检 · 本机 0.0.1；`slac1700.18o` 2880 历元+PDOP 3.298… 复跑；pytest 17；Earthdata 未跑 |
| 24 | [android_rinex.md](./android_rinex.md) | GnssLogger / 手机原始测量 → RINEX3 | 220 | **已短硬** · 本机 clone `8ea7ab7`；样例 → `nex9_lab.17o` 1379 历元；georinex 1.16.2 探活 |
| 25 | [cosmic-crunch.md](./cosmic-crunch.md) | JPL GENESIS COSMIC-1 大气 L2 ASCII→netCDF4 | 222 | **已短硬** · 本机 2.1.2；`get --test` 10×`.L2.txt.gz` + convert/`--netcdf4` 10×`.nc`；非 CDAAC ionPrf |
| 26 | [pyglow.md](./pyglow.md) | 上层大气气候态（IRI/HWM/IGRF） | 204 | **已短硬** · 本机 tip 1988757 / Py3.8；IRI-2016 ne(250km)=854889；缺 igrf2015 静默退出坑已记 |
| 27 | [iri2016.md](./iri2016.md) | IRI-2016 官方 Fortran→xarray | 170 | **已短硬** · 本机 1.12.0/`ca523ad` / Py3.11；ne@250km=8.55e11 m⁻³；与 pyglow cm⁻³ 对照 |
| 28 | [gnss_lib_py.md](./gnss_lib_py.md) | Stanford NAV Lab：观测/导航 → NavData / WLS | 200 | **已短硬** · 本机 gnss-lib-py **1.1.0**；混合 OBS→126 测值/5 历元；AndroidDerived2023 冒烟 |
| 29 | [pyiri.md](./pyiri.md) | 纯 Python IRI（无 Fortran 绑定） | 182 | **已短硬** · 本机 PyIRI **0.1.7**；单点 2020-04-01 NmF2/vTEC 实跑；对照 pyglow/iri2016 |
| 30 | [awsgnssroutils.md](./awsgnssroutils.md) | AWS Open Data GNSS-RO 查询/下载（calibratedPhase 等） | 245 | **已短硬** · 本机 1.2.7；cosmic1 Phase 2636→3 文件；cosmic2 仅 atm 对照；开放 S3 / rotcol 门禁 |
| 31 | [pyirtam.md](./pyirtam.md) | 纯 Python IRTAM 系数→网格 Ne（对接 PyIRI） | 177 | **已短硬** · 本机 PyIRTAM **0.0.7**；LGDC 2024-06-01 02:15 四系数 + run_PyIRTAM 实跑 |
| 32 | [fast.md](./fast.md) | GNSS 下载 / QC / 广播星历 SPP / 选站 | 215 | **已短硬** · 本机 tip **3.01.01**；ABPO satNum + 1h SPP Δ≈0.69 m；FTP 下载本机失败已记 |
| 33 | [apexpy.md](./apexpy.md) | Apex / 准偶极磁坐标（Apex/QD/MLT） | 174 | **已短硬** · 本机 2.1.1/`eed96cf`；geo2apex(40N,80W,250km)→alat≈50.70；CLI 14 位时间坑 |
| 34 | [msise00.md](./msise00.md) | NRLMSISE-00 中性大气 → xarray | 166 | **已短硬** · 本机 **1.11.1**/`e4ab457`；Tn@250km=1009.87 K；CLI `-w` 需 netCDF4 |
| 35 | [pysatcdaac.md](./pysatcdaac.md) | pysat 生态 CDAAC/COSMIC（ionPrf/ionPhs） | 293 | **已短硬** · 本机 0.0.5；ionprf 2019-01-01 59→53；ionphs 下 144、load 维冲突改 netCDF4 |
| 36 | [diffionmap.md](./diffionmap.md) | 两幅 IONEX 并排对照（VS 图） | 179 | **已短硬** · tip `57ceb1d`；Py3 读 CODG/WHUC 12 图 mean≈24.84；IGRG mean≈13.367；Basemap 出图环境受限 · **质检复跑通过** |
| 37 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) | CDDIS 高采样 15 min 块批量下载 | 179 | **已短硬** · 本机 1.0.2；FTPS 登录+CWD+SIZE 706256；LIST/RETR 425 受限；Linux 无 CRX2RNX · **质检复跑通过** |
| 38 | [cycle-slip-correction.md](./cycle-slip-correction.md) | 周跳探测改正 CLI（EMBRACE/INPE） | 183 | **已短硬** · tip `c465dd4`；无 PyPI；现代钉+BAKO 3.03 40 历元；不写回 RINEX |
| 39 | [gps-measurement-tools.md](./gps-measurement-tools.md) | Google GNSS Logger + MATLAB 伪距/WLS | 203 | **已短硬** · tip `ab1aebb`；demo→android_rinex→georinex 223 历元；MATLAB 环境受限 · **质检复跑通过** |
| 40 | [pygpsclient.md](./pygpsclient.md) | NMEA/UBX/RTCM/NTRIP 桌面 GUI | 224 | **已短硬** · 本机 **1.7.6**/`69b84cf`；pyrinexconv O1677/N55037；无 tkinter GUI 受限 · **质检复跑通过** |
| 41 | [gdds.md](./gdds.md) | IGS/CORS/产品/时序多模块 GUI 下载 | 242 | **已短硬** · tip `2a8543c`；无 CLI；NOAA/ITRF 实拉；WHU CWD 通、NLST 时好时坏（写作 425/质检成功）；CDDIS 401；Earthdata 硬编码须自换 · **质检复跑通过** |
| 42 | [geospacelab.md](./geospacelab.md) | 日地数据管理/可视化（OMNI·指数·TEC map） | 256 | **已短硬** · 本机 **0.14.8**；OMNI SYM_H min=-234；Madrigal TEC 13×180×360 @06:30 max=114；需 cartopy+config |
| 43 | [glab-upc.md](./glab-upc.md) | UPC gAGE 教学 GNSS（SPP/PPP/电离层模型） | 202 | **已短硬** · 官方 v6.0.0 `gLAB_linux`；abmf SPP 2880 历元 3D95≈4.75 m；旧 4.x gcc 链失败已记 · **质检复跑通过** |
| 44 | [pynmeagps.md](./pynmeagps.md) | NMEA 0183 编解码库 | 213 | **已短硬** · 本机 **1.1.7**/`4322c38`；GGA 往返+文件流；交叉 [pygpsclient](./pygpsclient.md)/[pygnssutils](./pygnssutils.md) · **质检复跑通过** |
| 45 | [gnsspy.md](./gnsspy.md) | Python GNSS 读写/分析（pandas + RINEX 2↔3） | 228 | **已短硬** · 本机 **3.0.1**/`e6879bf`；质检复跑 demo.10o→22×9/2历元/14SV G07 L1=118767195.326；converter 2→3 OK（XYZ Y/Z=0；3→2 回写 `read_obsFile` Length mismatch）；**无 PyPI**；对照 [georinex](./georinex.md) · **质检复跑通过** |
| 46 | [ionex-rs.md](./ionex-rs.md) | Rust IONEX 解析/写回（nav-solutions） | 170 | **已短硬** · tip `bcb9171`；CKMG 129575/9.2 TECU/807703 B · **质检复跑通过** |
| 47 | [madocalib.md](./madocalib.md) | QZSS MADOCA-PPP 官方测试库（事后 PPP） | 165 | **已短硬** · VER **2.1**/`0089f7d`；MIZU 118×Q=6 · **质检复跑通过** |
| 48 | [aacgmv2.md](./aacgmv2.md) | AACGM-v2 地磁坐标（mlat/mlon/MLT） | 209 | **已短硬** · **2.7.1**/`5f85579`；mlat≈50.53 · **质检复跑通过** |
| 49 | [gnsstools.md](./gnsstools.md) | 轻量 Python：RINEX/SP3 → pandas / 轨道壳 | 253 | **已短硬** · tip **`e496093`** / **0.0.1**；OBS E7 C1=28344990.66=georinex；SP3 G01 xyz km；**无 PyPI**；对照 [georinex](./georinex.md)/[gnsspy](./gnsspy.md) |
| 50 | [rinexmod.md](./rinexmod.md) | RINEX 头/元数据修改与长短名规范化 | 241 | **已短硬** · **4.2.1**；demo→demo064a.10o MARKER/AGENCY/REC/ANT；长名+gz · **质检复跑通过** |
| 51 | [pyubx2.md](./pyubx2.md) | u-blox UBX 编解码库 | 244 | **已短硬** · **1.3.6**/`4abbfa6`；CFG-MSG/NAV-PVT/ACK 往返；NAV-PVT 53.4507228；mon_span 109 · **质检复跑通过** |
| 53 | [kamodo.md](./kamodo.md) | NASA CCMC 模式输出函数化（SWMF_IE/IRI/GITM…） | 166 | **已短硬** · **kamodo-ccmc 26.9.2**/core **26.8.7**；SWMF_IE Σ_H(12h,0E,70N)=**9.1183** S；phi=−1.7879 kV |
| 52 | [pyrtcm.md](./pyrtcm.md) | RTCM3 编解码库（含 MSM） | 286 | **已短硬** · **1.2.0**/`5d66c7a`；1005 往返；RTCM3.log 11 帧；MSM3 `parse_msm` · **质检复跑通过** |
| 54 | [gnsstk.md](./gnsstk.md) | C++ GNSS 基础库（原 GPSTk）+ apps CLI | 208 | **已短硬** · 库 **15.3.1**/`55ea334` + apps **15.1.1**/`1aeb7d2`；`RinSum` BAHR 120 历元；`timeconvert` week 2437 · **质检复跑通过** |
| 55 | [teqc.md](./teqc.md) | 经典 Translate/Edit/QC（**EOL 2019Feb25**） | 197 | **已短硬** · 静态 `teqc`；demo.18o `+qc` 3 历元 MP12≈0.20 · **质检复跑通过**；后继 [gfzrnx](./gfzrnx.md)/[anubis](./anubis.md)/[rnxcmp](./rnxcmp.md) |
| 56 | [pyspartn.md](./pyspartn.md) | SPARTN 精密改正电文编解码 | 322 | **已短硬** · 本机 **1.1.0**/`8fc58f8`；**无接收机/无 L-band**；传输层 OCB-GPS 往返；GAD nSF=228；d9s 3007 帧；**无 CLI**→[pygnssutils](./pygnssutils.md)；交叉 [pyubx2](./pyubx2.md)/[pynmeagps](./pynmeagps.md)/[pygpsclient](./pygpsclient.md)/[haslib](./haslib.md)/[pyrtcm](./pyrtcm.md) |
| 57 | [gampii-good.md](./gampii-good.md) | GAMP II 配套：GNSS 观测/产品 YAML 下载器（GOOD） | 244 | **已短硬** · tip **`479aa14`** / v3.1；CMake 实编；WHU BRDC mixed3 11 371 068 B + igs14/igs20.atx；无参 Usage exit 255 · **质检复跑通过**（2026-09-24 04:59 EDT） |
| 58 | [ntripstreams.md](./ntripstreams.md) | NTRIP 协议通信（asyncio + RTCM3 帧） | 286 | **已短硬** · 本机 **0.3.5**/`889ffb9`；rtk2go STR**765**/igs-ip STR**384** sourcetable；无订户订流 HTTP 400；`Rtcm3` aamakinen 1005/1077 CRC + AgPartner_2 **251** 帧；1029 编码；交叉 [pygnssutils](./pygnssutils.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[bnc](./bnc.md)/[pynmeagps](./pynmeagps.md)/[pyrtcm](./pyrtcm.md) · **质检复跑通过**（2026-09-24 04:59 EDT；坑 #13 `head` BrokenPipe） |
| 59 | [claslib.md](./claslib.md) | QZSS CLAS Compact SSR→OSR/VRS/PPP-RTK | 182 | **已短硬** · tip **`1e3a75d`**/084/0.8.4；dump header **3601**；test1 **3580** GGA ≈36.1036°N 140.0863°E · **质检复跑通过** |
| 60 | [b2blib.md](./b2blib.md) | 北斗 PPP-B2b C/C++ 解码（嵌 RTKLIB） | 188 | **已短硬** · tip **`fe7c4c0`**；WUH2 5 min **9**×Q=6；首/末 ECEF 对齐 · **质检复跑通过** |
| 61 | [ismr-downloader.md](./ismr-downloader.md) | ISMR Query Tool API 闪烁监测数据 CLI 下载 | 226 | **已短硬** · 本机 **0.2.0**/`cca68e4`；`--help`；假账号 token 400；SSL 需 `--insecure`；**登记门禁未落盘**（交叉 [data-access](../data-access.md)） · **质检复跑通过**（2026-09-24 05:03 EDT） |
| 62 | [drcycleslip.md](./drcycleslip.md) | 三频周跳探测/修复教学（DRCycleSlip） | 197 | **已短硬** · tip **`f57d74d`**；无 PyPI；`search`/`find` + BAKO G24 注入历元 **700→(23,18,17)**；对照 [cycle-slip-correction](./cycle-slip-correction.md)/[georinex](./georinex.md)/[anubis](./anubis.md) |
| 63 | [gnss-downloader.md](./gnss-downloader.md) | PyQt5 NASA/WHU FTP 日采样 GNSS 下载 | 233 | **已短硬** · tip **`e6d0d84`**/V3.0；无下载 CLI；WHU SIZE brdc **57792**；NLST 425；NASA 明文失效→[data-access](../data-access.md) |
| 64 | [navdecoder.md](./navdecoder.md) | PPP-B2b + Galileo HAS 电文解码（Sept/Unicore） | 184 | **已短硬** · tip **`7947333`**；HAS **801**×data collected + log **48288**/1.1 MB；B2b log **7346** / `.ssr` **532** / `.sp3` **277** · **质检复跑通过**（2026-09-24 05:10 EDT） |
| 65 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) | 观测多路径/周跳/SNR 分析（gnssmultipath） | 161 | **已短硬** · PyPI **2.2.0**/tip **`806c3d9`**；NMBUS C1C RMS≈**1.273**/wRMS≈**1.093**；周跳 **47**/nEpochs **293** · **质检复跑通过**（2026-09-24 05:09 EDT） |
| 66 | [crx2rnx.md](./crx2rnx.md) | Rust Hatanaka CRX→RNX 解压 CLI（nav-solutions） | 240 | **已短硬** · **质检复跑通过**（2026-09-24 05:19 EDT；AJAC 26→17；ACOR C1C=GSI；ESBC gz；tip `765ddeb`/2.7.0；交叉 [rnxcmp](./rnxcmp.md)/[hatanaka](./hatanaka.md)/[rinexmod](./rinexmod.md)/[georinex](./georinex.md)）|
| 67 | [sbfparser.md](./sbfparser.md) | Septentrio SBF 官方 Cython 解析（sbf-parser） | 252 | **已短硬** · PyPI **1.0.3**/tip **`ea84256`**；receiver_status TOW=**49638143**；log_0000 **748**/49；ExtEvent 往返；HAS样例 GALRawCNAV=**11774**；无 ISM/4086；交叉 [haslib](./haslib.md)/[ismr-downloader](./ismr-downloader.md)/[pyubx2](./pyubx2.md) |
| 68 | [ginan.md](./ginan.md) | Geoscience Australia 精密定位/改正工具箱（pea） | 213 | **已短硬** · **质检复跑通过**（2026-09-24 05:16 EDT；dry-run+20 epoch ALIC≈0.08 m；tip `5033996`；交叉 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)/[rtkbase](./rtkbase.md)）|
| 69 | [rtkbase.md](./rtkbase.md) | Pi/SBC GNSS 基站 + Web UI（Stefal） | 184 | **已短硬** · **质检复跑通过**（2026-09-24 05:16 EDT；ConfigManager+install help；12 unit；无 Pi/GNSS；tip `2ce7ce0`；交叉 [rtklib](./rtklib.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[ginan](./ginan.md)）|
| 70 | [pysbf2.md](./pysbf2.md) | Septentrio SBF 纯 Python 编解码（semuconsulting） | 294 | **已短硬** · PyPI **1.0.5**/tip **`a68fe44`**；PVTCartesian 往返；pvtcart Type=**6**/NrSV=**36**；status CPULoad=**28**；examples **232**；混流 NMEA+RTCM；`SBF_MSGIDS`=**125** 无 ISM；交叉 [sbfparser](./sbfparser.md)/[haslib](./haslib.md)/[pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)/[pynmeagps](./pynmeagps.md) |
| 71 | [ntrip-client.md](./ntrip-client.md) | Rust NTRIP 客户端（nav-solutions；example `simple-cli`） | 304 | **已短硬** · crates.io **0.2.1**/tip **`7d4c6d3`**；rtk2go **766**/igs-ip **384**/centipede **1270**；VALDM **86** 帧/8 s；交叉 [ntripstreams](./ntripstreams.md)/[pygnssutils](./pygnssutils.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[bnc](./bnc.md)/[crx2rnx](./crx2rnx.md) |
| 72 | [septentrio-gnss-driver.md](./septentrio-gnss-driver.md) | Septentrio ROS1/ROS2 驱动（ROSaic） | 244 | **已短硬** · **1.4.8**/tip **`5613af2`**；launch×**3**/config×**4**/msg×**26**；**无 ROS/无 Rx** 未编译未 launch；交叉 [sbfparser](./sbfparser.md)/[pysbf2](./pysbf2.md)/[haslib](./haslib.md)/[rtkbase](./rtkbase.md) |

| 73 | [graphgnsslib.md](./graphgnsslib.md) | FGO 风格 GNSS/RTK（PolyU；ROS+Ceres） | 185 | **已短硬** · **质检复跑通过**（2026-09-24 05:21 EDT；SPP 251×Q5；RTK **94**×Q2；去 `-s 1`；launch 子目录；无 ROS/Docker；tip `d861802`；交叉 [rtklib](./rtklib.md)/[gnss_lib_py](./gnss_lib_py.md)/[great-pvt](./great-pvt.md)）|
| 74 | [great-pvt.md](./great-pvt.md) | 武大 GREAT 精密 PVT（PPP/RTK，XML） | 186 | **已短硬** · **质检复跑通过**（2026-09-24 05:21 EDT；GODN 1 h DF Float **120** 历元末 3D≈**0.0062 m**；v1.4.0/`8bd3d23`；交叉 [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)/[ginan](./ginan.md)）|
| 75 | [libsbp.md](./libsbp.md) | Swift SBP 多语言协议库（PyPI `sbp`） | 247 | **已短硬** · PyPI **`sbp` 6.5.2**/tip **`2b883ad`**；`sbp2json` one_msg snr=**16.2**；roundtrip PosLLH n_sats=**15**；short **2382**/roundtrip **5000**；**无 Rx**；交叉 [septentrio-gnss-driver](./septentrio-gnss-driver.md)/[pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)/[pysbf2](./pysbf2.md) |
| 76 | [rinex-cli.md](./rinex-cli.md) | Rust RINEX/SP3 后处理 CLI（QC HTML + filegen；nav-solutions） | 295 | **已短硬** · crates.io **0.12.1**/tip **`f4dd4c3`**；ACOR **25** 历元；ESBC gz **2880**；G07 C1C=**23818653.240**；`tbin`/`split` panic；交叉 [georinex](./georinex.md)/[rinexmod](./rinexmod.md)/[hatanaka](./hatanaka.md)/[crx2rnx](./crx2rnx.md)/[rnxcmp](./rnxcmp.md)/[teqc](./teqc.md)/[gfzrnx](./gfzrnx.md)/[gnsspy](./gnsspy.md)/[gnsstools](./gnsstools.md) |
| 77 | [rtcm3torinex.md](./rtcm3torinex.md) | BKG RTCM3→RINEX（NTRIP 单流；obsolete→BNC） | 238 | **已短硬** · SVN **r9404**/WC **r11044**；本机 **2.9404**；`make`；euref STR **222**；VALDM RINEX3 **43** 历元 G03 C1C=**25238622.890**；`-P` **75** 行；rtk2go **400**；交叉 [pyrtcm](./pyrtcm.md)/[bnc](./bnc.md)/[pygnssutils](./pygnssutils.md)/[ntrip-client](./ntrip-client.md)/[ntripstreams](./ntripstreams.md)/[bkg-ntripcaster](./bkg-ntripcaster.md) |
| 78 | [groops.md](./groops.md) | TU Graz 重力场 + GNSS（GROOPS；XML） | 215 | **已短硬** · **质检复跑通过**（2026-09-24 05:33 EDT；Sp3Format2Orbit G01 **289**/300 s/gaps=0；clock **69182** B；georinex GRAZ **2880**/30；G07 C1C=25383647.774；`01`/`02` 缺 transmitterList/`tides/earthAnelastic2003.xml`；tip `7e1bd6d`；交叉 [pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)/[rtklib](./rtklib.md)/[rapppid](./rapppid.md)）|
| 79 | [rapppid.md](./rapppid.md) | VieVS MATLAB PPP（raPPPid） | 169 | **已短硬** · **质检复跑通过**（2026-09-24 05:33 EDT；CODE **633** `.m`（树 635）/9×`.mat`；OceanLoading **339510** B；无 MATLAB；tip `28fd517`/v5.1；交叉 [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)/[rtklib](./rtklib.md)/[groops](./groops.md)）|
| goGPS MATLAB 低成本站 PPP/NET（需 MATLAB） | [gogps-matlab.md](./gogps-matlab.md) |
| 80 | [piksi-tools.md](./piksi-tools.md) | Swift/Piksi 现场 SBP 工具（配 libsbp） | 213 | **已短硬** · **质检复跑通过**（2026-09-24 05:42 EDT；JSON **61599**；PosLLH **4686**/nonzero **4276**/≈37.7735°N；roundtrip n_sats=**15**；无 Rx **exit 1**；`Position saved` stdout；PyPI **4.0.0**/tip **`02f1532`**；交叉 [libsbp](./libsbp.md)/[swiftnav-ros2](./swiftnav-ros2.md)/[libswiftnav](./libswiftnav.md)）|
| 81 | [swiftnav-ros2.md](./swiftnav-ros2.md) | Swift 官方 ROS 2 SBP 驱动 | 219 | **已短硬** · **质检复跑通过**（2026-09-24 05:42 EDT；tip **`c35c6ef`** 超前 tag **v1.0.0**/`5c82573` 4 commit；包 **1.0.0**/MIT；launch×**1**/config×**1**/msg×**1**；exec **`sbp-to-ros`**；`settings.yaml`；**NO_ROS**；交叉 [libsbp](./libsbp.md)/[piksi-tools](./piksi-tools.md)/[libswiftnav](./libswiftnav.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)）|
| 82 | [libswiftnav.md](./libswiftnav.md) | Swift GNSS 数值算法 C 库（星历/电离层等） | 260 | **已短硬** · **质检复跑通过**（2026-09-24 05:39 EDT；gtest **250 PASSED**/24；`calc_ionosphere` **7.202448** m；`wgsecef2llh` 37.42864123/−122.17234450；install **37** 头；tip `19331e0`；对照 [libsbp](./libsbp.md)；交叉 [piksi-tools](./piksi-tools.md)/[swiftnav-ros2](./swiftnav-ros2.md)/[gnsstk](./gnsstk.md)）|
| 83 | [ubx2rinex.md](./ubx2rinex.md) | u-blox UBX→RINEX 采集 CLI（nav-solutions） | 314 | **已短硬** · **质检复跑通过**（2026-09-24 05:39 EDT；F9T `--gps` **298**/georinex 12 SV；G01 L1C=**112252116.071**/C1C=**21360867.696**/D1C=**804.339**；coldstart OBS **561**+NAV **9**；无 RAWX→0；混星缺 TIME OF FIRST OBS→georinex KeyError；tip `3b67fd0`/0.3.0；交叉 [pyubx2](./pyubx2.md)/[georinex](./georinex.md)/[rinex-cli](./rinex-cli.md)）|
| 84 | [ublox-dgnss.md](./ublox-dgnss.md) | ROS 2 u-blox UBX DGNSS 驱动（F9P/F9R/X20P） | 233 | **已短硬** · **0.7.6**/tip **`7ace9d5`**/tag **0.7.6**；六包同版；launch×**11**/config×**3**/msg×**65**/srv×**4**；exec **`ublox_dgnss_node`**；**无 ROS/无 Rx** 未 colcon/launch；交叉 [pyubx2](./pyubx2.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)/[swiftnav-ros2](./swiftnav-ros2.md) |
| 87 | [ublox-driver.md](./ublox-driver.md) | 港科大 ZED-F9P ROS1 驱动（gnss_comm/GVINS） | 232 | **已短硬** · **1.0.0**/tip **`7961ab7`**；ROS1 catkin；launch×**1**/config×**2**/msg×**0**；exec **`ublox_driver`**+**`sync_system_time`**；话题×**7**；**无 ROS/无 Rx** 未 catkin/launch；交叉 [ublox-dgnss](./ublox-dgnss.md)/[pyubx2](./pyubx2.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)/[swiftnav-ros2](./swiftnav-ros2.md) |
| 85 | [gpsd.md](./gpsd.md) | GNSS/AIS 守护进程（多客户端 JSON/NMEA） | 238 | **已短硬** · Debian **3.25-5+deb13u2**；`gpsfake`→TPV mode=**3** lat=**39.904187167**/lon=**116.390742667**/altMSL=**44.0**/uSat=**12**；**无 Rx**；交叉 [pynmeagps](./pynmeagps.md)/[pygnssutils](./pygnssutils.md)/[ubx2rinex](./ubx2rinex.md)/[rtkbase](./rtkbase.md)/[bnc](./bnc.md) |
| 86 | [ppp-wizard.md](./ppp-wizard.md) | CNES 整数零差 PPP-AR 示范（门户+SSR 产品） | 173 | **已短硬** · **质检复跑通过**（2026-09-24 05:41 EDT；`package.html` **404**；`cnt24373` SP3 **288**/109=G31+R19+E27+C32；CLK AS **1883520**；BIA **2268516** 行；解压≈**1.9/144/200 MB**；**无客户端包**未跑 PPP；交叉 [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)/[ginan](./ginan.md)/[great-pvt](./great-pvt.md)）|
| 87 | [gogps-matlab.md](./gogps-matlab.md) | goGPS MATLAB 低成本/多星座 PPP·NET | 197 | **已短硬** · **质检复跑通过**（2026-09-24 05:41 EDT；tip **`a990ed0`**/1.0.1；824 `.m`/427；ZIM3 **2880**/G01 C1C=**25131594.344**；**无 MATLAB** 未跑 GUI；交叉 [rtklib](./rtklib.md)/[graphgnsslib](./graphgnsslib.md)）|

| 88 | [minmea.md](./minmea.md) | 轻量纯 C NMEA 0183 解析（嵌入式） | 143 | **已短硬** · tip **`c43c9e7`**/WTFPL；check **38/38**；GGA lat=**51.11568069**；北京 RMC **39.90418625**/116.39073944；交叉 [pynmeagps](./pynmeagps.md)/[gpsd](./gpsd.md) |
| 89 | [ntripbrowser.md](./ntripbrowser.md) | NTRIP 源表浏览 CLI/API（Emlid） | 148 | **已短硬** · PyPI **4.0.0**/tip **`3730867`**；rtk2go STR **764**/igs **384**/centipede **1269**；巴黎50km **14**/IPGP≈**0.71** km；**未订流**；交叉 [ntripstreams](./ntripstreams.md)/[ntrip-client](./ntrip-client.md)/[pygnssutils](./pygnssutils.md) |
| 90 | [pynmea2.md](./pynmea2.md) | 高星标 Python NMEA 0183 解析 | 177 | **已短硬** · PyPI **1.19.0**/tip **`fcd90dc`**/pytest **105**；北京 GGA **39.90418716666667**/116.39074266666667；流 **36**；交叉 [pynmeagps](./pynmeagps.md)/[minmea](./minmea.md)/[gpsd](./gpsd.md) |
| 91 | [pymap3d.md](./pymap3d.md) | 纯 Python 大地/ECEF/ENU/AER/ECI 转换 | 176 | **已短硬** · PyPI **3.2.0**/tip **`033895e`**/pytest **397**/skip **11**；北京 ECEF **−2177813.332/4388956.908/4069858.556**；ENU n≈**111.034** m；交叉 [apexpy](./apexpy.md)/[aacgmv2](./aacgmv2.md)/[georinex](./georinex.md) |
| 92 | [gsilib.md](./gsilib.md) | GSI 多 GNSS 基线/PPP（IFB/ISB；Win） | 189 | **已短硬** · ver **1.0.3**；IFB tr02 **1921**/G01 C1C=**24070092.563**；**无 Wine32 未跑基线解**；交叉 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md) · **质检复跑通过** |
| 93 | [rtppp-b2b.md](./rtppp-b2b.md) | 北斗 PPP-B2b 实时改正接口（BNC/SBF） | 191 | **已短硬** · tip **`9864c66`**；CRC **0**/`0x6131`；MT **1–7**；MISSING+`clock_orbit`；**缺 BNC 未链接**；交叉 [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md)/[haslib](./haslib.md)/[cssrlib](./cssrlib.md)/[madocalib](./madocalib.md) · **质检复跑通过** |
| 94 | [cors-relay.md](./cors-relay.md) | CORS/NTRIP 差分帐号池中继（libev） | 226 | **已短硬** · tip **`1238947`**/`123894`；二进制 **188496** B；8001–8003 + 管理 8000；STR×**3**/CL=**390**；`ICY 200`=**12** B/`401`/未知挂载→源表；**无真源未臆造 RTCM**；交叉 [ntripcaster-libev](./ntripcaster-libev.md)/[pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[ntripbrowser](./ntripbrowser.md)/[data-access](../data-access.md) · **质检复跑通过** |
| 95 | [iri-fortran.md](./iri-fortran.md) | 官方 IRI Fortran（irimodel.org） | 192 | **已短硬** · IRI-**2026**；fort.7 NmF2=**893124.7**/hmF2=**259.16**/TEC=**25.8**/F10.7=**127.2**；交叉 [iri2016](./iri2016.md)/[pyiri](./pyiri.md)/[pyirtam](./pyirtam.md)/[nequickg](./nequickg.md) · **质检复跑通过** |
| 96 | [nequick2-ictp.md](./nequick2-ictp.md) | ICTP NeQuick 2 源码申请（≠NeQuick-G） | 151 | **已短硬** · **登记受限**；bnava@/yenca@；**无本地编译/无臆造 TEC**；Web R12/F10.7；交叉 [nequickg](./nequickg.md)/[iri-fortran](./iri-fortran.md)/[pyiri](./pyiri.md) · **质检复跑通过** |
| 97 | [ntripcaster-libev.md](./ntripcaster-libev.md) | libev NTRIP Broadcaster（自建播发） | 248 | **已短硬** · **质检复跑通过**（2026-09-24 06:21 EDT；tip **`cc17929`**/`1.1.0`；二进制 **74152** B；口 **2101**；空表 CL=**16**/在线 **STR;LAB1** CL=**111**；`ICY 200`=**12** B/`401`/`Bad Password`/`Bad Mountpoint`；透传 **match**；**未臆造 RTCM**；交叉 [cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[pygnssutils](./pygnssutils.md)/[data-access](../data-access.md)）
| 98 | [iri-2026-package.md](./iri-2026-package.md) | 官方 IRI-2026 zip 发行物（清单/校验） | 155 | **已短硬** · **已质检复跑** 2026-09-24 06:19 EDT · zip **1823544**/sha₁₂=`2377b0c07a43`；`unzip` **69**/解压 **5974782** B；系数已捆；指数另下；**未重跑** fort.7→[iri-fortran](./iri-fortran.md)；交叉 [iri-common-files](./iri-common-files.md)/[pyiri](./pyiri.md)/[iri2016](./iri2016.md) |
| 99 | [iri-common-files.md](./iri-common-files.md) | IRI COMMON_FILES（CCIR/URSI 公共系数） | 150 | **已短硬** · **已质检复跑** 2026-09-24 06:19 EDT · `00_ccir-ursi.zip` **351482**/sha₁₂=`5427353c578f`；`cmp` **24/24** vs 2026 包；≤2016 必下 / 2020+ 已捆；交叉 [iri-2026-package](./iri-2026-package.md)/[iri-fortran](./iri-fortran.md)/[pyiri](./pyiri.md) |
| 100 | [ntrip-cpp.md](./ntrip-cpp.md) | NTRIP 2.0 C++ caster/client/server（ybzwyrcld） | 203 | **已短硬** · tip **`b431661`**/`1.2.0`；口 **8090**；`POST`/`HTTP/1.1 200`；客 `200`/`ICY`/`401`；`GET /`→**401**（源表死）；样例 Recv[**70**]；交叉 [ntripcaster-libev](./ntripcaster-libev.md)/[cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[data-access](../data-access.md) |

**状态图例：** `已短硬` = Round 已按 short-hard 改过且可作二遍质检；`登记受限` / `环境受限` = 无本机官方二进制或运行时，命令以官方/仓内为准、**禁止伪造 stdout**；`边界` = sh-gim 专有求解器未开源；`仍薄` = 尚无短硬或明显缺真实 I/O（当前 **0 篇**——新缺篇由「软件用法讲解」认领后改此表）。

每篇结构：**用途边界 → 安装 → 逐步命令+期望输出 → I/O 字段 → 参数 → 接到哪步 → ≥8 坑 → 选型**。

---

## 30 秒选型

| 你要… | 打开 |
| --- | --- |
| 读 RINEX 进 Python | [georinex.md](./georinex.md) |
| 浏览 NTRIP 源表 / 按距筛选 | [ntripbrowser.md](./ntripbrowser.md) |
| 嵌入式 C 解析 NMEA | [minmea.md](./minmea.md) |
| 经典 Python NMEA 解析（高星标） | [pynmea2.md](./pynmea2.md) |
| 大地/ECEF/ENU/AER 坐标转换 | [pymap3d.md](./pymap3d.md) |
| RINEX → pandas / 2↔3 转换（教学） | [gnsspy.md](./gnsspy.md) |
| 轻量 RINEX/SP3 → pandas（教学；无 PyPI） | [gnsstools.md](./gnsstools.md) |
| C++ GNSS 时间/RINEX 库 + RinSum | [gnsstk.md](./gnsstk.md) |
| 经典 TEQC 翻译/编辑/QC（EOL） | [teqc.md](./teqc.md) |
| 分信号码多路径 + 周跳报告 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) |
| 改/拼/抽稀 RINEX | [gfzrnx.md](./gfzrnx.md) |
| 观测 QC 报告 | [anubis.md](./anubis.md) |
| 周跳探测改正试验（RINEX 3.01–3.03） | [cycle-slip-correction.md](./cycle-slip-correction.md) |
| 三频周跳注入–探测教学（Python） | [drcycleslip.md](./drcycleslip.md) |
| 旧 CORS 缺站/日目录/TEQC 批壳 | [pinot.md](./pinot.md) |
| GNSS 产品下载 + 观测 QC + 粗 SPP | [fast.md](./fast.md) |
| 厂商 RAW→RINEX3/4 台网入库 | [autorino.md](./autorino.md) |
| 批量改 RINEX 头 / 长短名 / 压缩约定 | [rinexmod.md](./rinexmod.md) |
| Hatanaka `.crx` 官方压缩/恢复 | [rnxcmp.md](./rnxcmp.md) |
| Python 解 `.crx` / 脚本压缩（pip） | [hatanaka.md](./hatanaka.md)（官方 → [rnxcmp](./rnxcmp.md)） |
| Rust CLI 仅解压 `.crx`/`.crx.gz`（非 GSI 同名） | [crx2rnx.md](./crx2rnx.md) |
| Rust RINEX QC HTML / filegen / 滤星座写回 | [rinex-cli.md](./rinex-cli.md) |
| Galileo NeQuick-G 模型（脚本） | [nequickg.md](./nequickg.md) |
| IRI-2012/2016 气候态（Python 包装） | [pyglow.md](./pyglow.md) |
| IRI-2016 官方驱动 → xarray | [iri2016.md](./iri2016.md) |
| 纯 Python IRI（无 Fortran） | [pyiri.md](./pyiri.md) |
| 官方 IRI Fortran 金标准（IRI-2026 本机） | [iri-fortran.md](./iri-fortran.md) |
| 官方 IRI-2026 zip 清单 / checksum | [iri-2026-package.md](./iri-2026-package.md) |
| IRI 公共 CCIR/URSI 系数（≤2016 外置） | [iri-common-files.md](./iri-common-files.md) |
| ICTP NeQuick 2（邮件申请；≠ Galileo-G） | [nequick2-ictp.md](./nequick2-ictp.md) |
| IRTAM 同化系数→网格 Ne（纯 Python） | [pyirtam.md](./pyirtam.md) |
| AACGM-v2 磁坐标 / MLT | [aacgmv2.md](./aacgmv2.md) |
| CCMC 模式输出函数化 / 飞越 | [kamodo.md](./kamodo.md) |
| Apex / QD / MLT 磁坐标 | [apexpy.md](./apexpy.md) |
| NRLMSISE-00 中性大气 | [msise00.md](./msise00.md) |
| Android/多源 GNSS → NavData / 教学 WLS | [gnss_lib_py.md](./gnss_lib_py.md) |
| 校准 sTEC/vTEC | [pytecgg.md](./pytecgg.md) |
| 粗相对斜 TEC（无 DCB） | [gnss-tec.md](./gnss-tec.md) |
| ROTI / AATR / ΔTEC | [ionomoni.md](./ionomoni.md) · [oasis-roti.md](./oasis-roti.md) |
| 读 IONEX GIM | [ionex-gim.md](./ionex-gim.md) |
| Rust 读/写 IONEX | [ionex-rs.md](./ionex-rs.md) |
| 两幅 IONEX 并排对照 | [diffionmap.md](./diffionmap.md) |
| CDDIS 高采样（1 s / 15 min）批量 | [cddis-highrate-downloader.md](./cddis-highrate-downloader.md) |
| IGS/CORS/产品/时序 GUI 多模块下载 | [gdds.md](./gdds.md) |
| 轻量 PyQt 点选 WHU/NASA 日文件（2020） | [gnss-downloader.md](./gnss-downloader.md) |
| GAMP/PPP YAML 批下载观测+产品（GOOD） | [gampii-good.md](./gampii-good.md) |
| 球谐 GIM 边界说明 | [sh-gim.md](./sh-gim.md) |
| NTRIP 脚本拉流 / 小 caster | [pygnssutils.md](./pygnssutils.md) |
| asyncio NTRIP 握手 / 轻量 RTCM 帧 | [ntripstreams.md](./ntripstreams.md) |
| Rust/tokio NTRIP 拉流 / 近邻挂载（example CLI） | [ntrip-client.md](./ntrip-client.md) |
| 多流 GUI / 录盘 | [bnc.md](./bnc.md) |
| 自建多用户 Caster | [bkg-ntripcaster.md](./bkg-ntripcaster.md) |
| CORS 帐号池中继再分发（NTRIP 1.0） | [cors-relay.md](./cors-relay.md) |
| 实验室自建轻量 NTRIP 播发（JSON/libev） | [ntripcaster-libev.md](./ntripcaster-libev.md)
| C++ NTRIP 2.0 握手样板（库+exam） | [ntrip-cpp.md](./ntrip-cpp.md)
| RTK / 浮点 PPP | [rtklib.md](./rtklib.md) |
| GA 现代化 PPP/POD（pea / YAML） | [ginan.md](./ginan.md) |
| FGO 因子图 GNSS/RTK（ROS 研究） | [graphgnsslib.md](./graphgnsslib.md) |
| 武大 GREAT 精密 PPP/RTK（XML） | [great-pvt.md](./great-pvt.md) |
| TU Graz 重力场 + GNSS 网解/PPP（XML） | [groops.md](./groops.md) |
| VieVS MATLAB GUI PPP（需许可证） | [rapppid.md](./rapppid.md) |
| Pi 基站 + Web / NTRIP 上行 | [rtkbase.md](./rtkbase.md) |
| PPP-AR | [pride-pppar.md](./pride-pppar.md) |
| CNES 整数 PPP-AR 产品/门户（客户端须申请） | [ppp-wizard.md](./ppp-wizard.md) |
| GSI 异机种 IFB/ISB 基线（Win GUI） | [gsilib.md](./gsilib.md) |
| QZSS MADOCA-PPP 官方参考 | [madocalib.md](./madocalib.md) |
| QZSS CLAS Compact SSR→OSR/VRS/PPP-RTK | [claslib.md](./claslib.md) |
| 北斗 PPP-B2b（嵌 RTKLIB） | [b2blib.md](./b2blib.md) |
| BNC 内 SBF→PPP-B2b 实时改正接口 | [rtppp-b2b.md](./rtppp-b2b.md) |
| Sept/Unicore 流 → B2b/HAS 日志+SSR/SP3 | [navdecoder.md](./navdecoder.md) |
| Python 开放 PPP/PPP-RTK（CLAS/HAS） | [cssrlib.md](./cssrlib.md) |
| Galileo HAS 页 → RTCM/IGS SSR | [haslib.md](./haslib.md) |
| 码多路径 / 周跳报告与出图 | [gnss-multipath-analysis.md](./gnss-multipath-analysis.md) |
| 轻量 Python 观测处理 / 自写估计器 | [laika.md](./laika.md) |
| 手机 GnssLogger → RINEX | [android_rinex.md](./android_rinex.md) |
| Google Logger 套件 / 手机原始测量规范 | [gps-measurement-tools.md](./gps-measurement-tools.md) |
| 板卡 GUI 联调 / NTRIP（tkinter） | [pygpsclient.md](./pygpsclient.md) |
| 教学 SPP/PPP / 误差项拆解（UPC gLAB） | [glab-upc.md](./glab-upc.md) |
| 系统级 GNSS 取位 / 多客户端 JSON（守护进程） | [gpsd.md](./gpsd.md) |
| NMEA 0183 编解码（Python） | [pynmeagps.md](./pynmeagps.md) |
| u-blox UBX 编解码（Python） | [pyubx2.md](./pyubx2.md) |
| u-blox UBX 文件/串口→RINEX OBS/NAV（Rust CLI） | [ubx2rinex.md](./ubx2rinex.md) |
| RTCM3 编解码（Python，含 MSM） | [pyrtcm.md](./pyrtcm.md) |
| NTRIP RTCM3→RINEX 文件（BKG 小工具；优先 BNC） | [rtcm3torinex.md](./rtcm3torinex.md) |
| SPARTN 编解码（Python；PPP-RTK 改正） | [pyspartn.md](./pyspartn.md) |
| 空间天气多源拉取/作图（OMNI·TEC map） | [geospacelab.md](./geospacelab.md) |
| GENESIS COSMIC-1 **大气** L2→netCDF（非 ionPrf） | [cosmic-crunch.md](./cosmic-crunch.md) |
| AWS GNSS-RO 查/下（**calibratedPhase** / 大气三型） | [awsgnssroutils.md](./awsgnssroutils.md) |
| CDAAC **ionPrf / ionPhs**（pysat） | [pysatcdaac.md](./pysatcdaac.md) |
| 闪烁 ISMR（UNESP API 批量） | [ismr-downloader.md](./ismr-downloader.md) |
| Septentrio SBF 块解析（官方 Cython） | [sbfparser.md](./sbfparser.md) |
| Septentrio SBF 编解码（纯 Python，同 pyubx2 栈） | [pysbf2.md](./pysbf2.md) |
| Swift SBP 多语言客户端（PyPI `sbp` / `sbp2json`） | [libsbp.md](./libsbp.md) |
| Swift/Piksi 现场日志·配置·刷机（配 libsbp） | [piksi-tools.md](./piksi-tools.md) |
| Swift 官方 ROS 2 SBP 驱动（Piksi/Duro/Starling） | [swiftnav-ros2.md](./swiftnav-ros2.md) |
| Swift GNSS 数值 C 库（星历/Klobuchar；≠ libsbp） | [libswiftnav.md](./libswiftnav.md) |
| u-blox F9/X20P 实时 ROS 2（USB UBX；Aussie Robots） | [ublox-dgnss.md](./ublox-dgnss.md) |
| u-blox ZED-F9P 实时 ROS 1（港科大；gnss_comm/GVINS） | [ublox-driver.md](./ublox-driver.md) |
| 闪烁仿真（MATLAB） | [iono-scintillation.md](./iono-scintillation.md) |

---

## 工作流路径 A–E

### A · 一日 TEC

[data-access](../data-access.md) →（可选 [gampii-good](./gampii-good.md) / [fast](./fast.md) / [gdds](./gdds.md) / [gnss-downloader](./gnss-downloader.md) 下载·QC / [autorino](./autorino.md) 入库 / [rinexmod](./rinexmod.md) 改头 / [android_rinex](./android_rinex.md) 手机日志 / [pinot](./pinot.md) 旧批壳）→（可选 [gnsspy](./gnsspy.md) 2↔3）→（可选 [rinex-cli](./rinex-cli.md) Rust QC）→ [georinex](./georinex.md) →（可选 [cycle-slip-correction](./cycle-slip-correction.md)/[drcycleslip](./drcycleslip.md) 周跳试验）→（可选 [gnss-multipath-analysis](./gnss-multipath-analysis.md) 多路径）→（可选 [anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)/[gnss-tec](./gnss-tec.md) 粗相对 TEC）→ [pytecgg](./pytecgg.md) → [ionex-gim](./ionex-gim.md) 对照 → 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[09](../tutorials/09-dcb-biases-deep.md)/[16](../tutorials/16-practice-one-day-tec.md)

### B · 不规则体 / 磁暴

ISMR 备数（可选 [ismr-downloader](./ismr-downloader.md)）· SBF 块解析（可选 [sbfparser](./sbfparser.md)/[pysbf2](./pysbf2.md)）· 高采样（可选 [cddis-highrate-downloader](./cddis-highrate-downloader.md)）→ RINEX → [ionomoni](./ionomoni.md) 或 [oasis-roti](./oasis-roti.md)；暴时指数/TEC 产品图可选 [geospacelab](./geospacelab.md) → 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)/[21](../tutorials/21-equatorial-anomaly-bubbles.md)；高 ROTI 时段对照 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md) 固定率；仿真概念见 [iono-scintillation](./iono-scintillation.md)·[13](../tutorials/13-scintillation-modeling.md)

### C · 实时差分 / 实验室 CORS

[gpsd](./gpsd.md) / [pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md) / [ntrip-client](./ntrip-client.md) / [pyrtcm](./pyrtcm.md) / [rtcm3torinex](./rtcm3torinex.md) / [pyspartn](./pyspartn.md) / [pyubx2](./pyubx2.md) / [ubx2rinex](./ubx2rinex.md) / [pysbf2](./pysbf2.md) / [septentrio-gnss-driver](./septentrio-gnss-driver.md) / [libsbp](./libsbp.md) / [libswiftnav](./libswiftnav.md) / [piksi-tools](./piksi-tools.md) / [swiftnav-ros2](./swiftnav-ros2.md) / [ublox-dgnss](./ublox-dgnss.md) / [pynmeagps](./pynmeagps.md) / [pygpsclient](./pygpsclient.md) 或 [bnc](./bnc.md) →（台站侧可选 [rtkbase](./rtkbase.md)；可选 [bkg-ntripcaster](./bkg-ntripcaster.md)/[cors-relay](./cors-relay.md)/[ntripcaster-libev](./ntripcaster-libev.md)/[ntrip-cpp](./ntrip-cpp.md)）→ [rtklib](./rtklib.md)；落盘后再走 A/B；手机 Logger 见 [gps-measurement-tools](./gps-measurement-tools.md)+[android_rinex](./android_rinex.md)

### D · 发表级坐标 / ZTD

QC（[anubis](./anubis.md)/[gfzrnx](./gfzrnx.md)）→ [rtklib](./rtklib.md) 冒烟 →（可选 [ginan](./ginan.md) PPP/POD；[great-pvt](./great-pvt.md)；[groops](./groops.md)；[rapppid](./rapppid.md)；[ppp-wizard](./ppp-wizard.md)；[gogps-matlab](./gogps-matlab.md)；开放服务教学 [cssrlib](./cssrlib.md)；QZSS CLAS [claslib](./claslib.md)；QZSS MADOCA [madocalib](./madocalib.md)；B2b [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md)/[rtppp-b2b](./rtppp-b2b.md)；异机种 Win [gsilib](./gsilib.md)）→ [pride-pppar](./pride-pppar.md) + 精密产品 → 教程 [06](../tutorials/06-iono-positioning.md)

### E · 理解 GIM（非端到端自建）

[ionex-gim](./ionex-gim.md) 读产品（Rust → [ionex-rs](./ionex-rs.md)）；[diffionmap](./diffionmap.md) 两图并排；[sh-gim](./sh-gim.md) 只看公开/专有边界；开源求解看列表里其它 GIM 工具 → 教程 [03](../tutorials/03-gim-ionex.md)/[10](../tutorials/10-build-gim-workflow.md)/[18](../tutorials/18-lab-compare-gims.md)

---

## 事实边界（归属说明，不是目录）

下面两行**不是**「只有这两个软件」，只是容易写错归属的提醒：

| 项目 | 关系 |
| --- | --- |
| [PyTECGg](./pytecgg.md) | 作者 **viventriglia**（不是本仓维护者自有） |
| [SH-GIM](./sh-gim.md) | 本仓维护者自有；**球谐求解器未开源** |
| 本目录其它手册 | 操作说明；许可与 EULA 以上游为准 |

---

最近新增（质检）：**gsilib+rtppp-b2b 质检复跑通过**（2026-09-24 06:12 EDT；IFB 1921/C1C=24070092.563；`.c` 50/40；RTPPP CRC 0/0x6131；MT 1–7；MISSING+clock_orbit；两端无解算二进制未臆造 stdout）。

最近新增（质检）：**iri-fortran+nequick2-ictp 质检复跑通过**（2026-09-24 06:15 EDT；zip 1823544/sha₁₂=`2377b0c07a43`；`iri` 1631368 B；fort.7 NmF2=893124.7/hmF2=259.16/Ne@250=886713/TEC=25.8/F10.7=127.2；对照 iri2016 NmF2 齐、hmF2 259.16≠271.48；NeQuick2 申请页无 zip→未编译未臆造；交叉 iri2016/pyiri/nequickg）。

最近新增（用法讲解）：**iri-fortran**（IRI-2026；fort.7 NmF2=893124.7/hmF2=259.16/Ne@250=886713/TEC=25.8；gfortran 14.2；交叉 iri2016/pyiri/pyirtam/nequickg）+ **nequick2-ictp**（邮件门禁 bnava@/yenca@；未编译未臆造；区分 nequickg；Web 表单可达）。

最近新增（质检复跑）：**iri-2026-package**+**iri-common-files**（2026-09-24 06:19 EDT；zip **1823544**/sha₁₂=`2377b0c07a43`；COMMON **351482**/sha₁₂=`5427353c578f`；`cmp` **24/24**；解压 **5974782** B；**未重跑** fort.7→iri-fortran；交叉 iri-fortran/pyiri/iri2016）。

最近新增（质检）：**cors-relay 质检复跑通过**（2026-09-24 06:17 EDT；tip `1238947`/二进制 **188496** B；STR×3/CL=390；ICY 200=12 B/401/未知挂载→源表；无真源未臆造 RTCM；交叉 ntripcaster-libev/bkg-ntripcaster/pygnssutils）。

最近新增（质检复跑）：**ntripcaster-libev**（2026-09-24 06:21 EDT；tip `cc17929`/`1.1.0`；二进制 **74152** B；口 2101；空表 CL=16；STR;LAB1 CL=111；ICY 200=12 B/401/Bad Password/Bad Mountpoint；透传 match；未臆造 RTCM；交叉 cors-relay/bkg-ntripcaster/pygnssutils）。

最近新增（用法讲解）：**ntrip-cpp**（tip `b431661`/`1.2.0`；口 8090；POST→HTTP/1.1 200；客 200/ICY/401；GET /→401 源表死；Recv[70]=kExmapleData；两处构建补丁；交叉 ntripcaster-libev/cors-relay/bkg-ntripcaster/data-access；下一优先 ntripserver/ntripclient 或 ntrip-go）。

最近新增（用法讲解）：**ntripcaster-libev**（tip `cc17929`/`1.1.0`；口 2101；空表→STR;LAB1；ICY 200/401/Bad Password；透传未臆造 RTCM；交叉 cors-relay/bkg-ntripcaster/data-access/pygnssutils；下一优先 ntrip-cpp）。

最近新增（用法讲解）：**cors-relay**（tip `1238947`/`123894`；8001–8003+管理8000；STR×3；ICY 200/401；无真源未臆造 RTCM；交叉 data-access/pygnssutils/bnc/bkg-ntripcaster/ntripbrowser；下一优先 ntripcaster-libev）。

最近新增（用法讲解）：**gsilib**（1.0.3；IFB tr02 1921/G01 C1C=24070092.563；无 Wine32 未跑基线；交叉 rtklib/pride-pppar/ginan）+ **rtppp-b2b**（`9864c66`；CRC 0/0x6131；MT 1–7；缺 BNC 未链接；交叉 b2blib/navdecoder/haslib/cssrlib/madocalib）。

最近新增（质检）：**pynmea2+pymap3d 短硬入库**（2026-09-24 06:04 EDT；pynmea2 1.19.0/`fcd90dc`/105；北京 GGA 39.90418716666667/116.39074266666667；流36；pymap3d 3.2.0/`033895e`/397；ECEF −2177813.332/4388956.908/4069858.556；ENU≈111.034 m；避开 cors-relay/gsilib/rtppp-b2b）。

最近新增（质检）：**minmea+ntripbrowser 短硬入库**（2026-09-24 05:45 EDT；minmea `c43c9e7`/38 checks；北京 RMC 39.90418625/116.39073944；ntripbrowser 4.0.0 STR 764/384/1269；巴黎14/IPGP≈0.71 km；未订流；避开 cors-relay/gsilib/rtppp-b2b）。

最近新增（质检）：**piksi-tools+swiftnav-ros2 质检复跑通过**（2026-09-24 05:42 EDT；JSON **61599**/PosLLH **4686**/n_sats=**15**/exit **1**；tip `c35c6ef` vs tag `5c82573`；launch×1/`sbp-to-ros`/NO_ROS）。最近新增（用法讲解）：**ublox_driver**（1.0.0/`7961ab7`；ROS1 catkin；launch×1/config×2；ublox_driver+sync_system_time；话题×7；无 ROS/无 Rx 门禁；交叉 ublox-dgnss/pyubx2/septentrio/swiftnav-ros2；下一优先 cors-relay）。

最近新增（质检）：**ppp-wizard+gogps-matlab 质检复跑通过**（2026-09-24 05:41 EDT；修正 SP3/BIA 解压大小 1.9/200 MB；SP3 288/109；AS 1883520；BIA 2268516；ZIM3 2880/C1C=25131594.344；无客户端/MATLAB 边界保留）。

最近新增（用法讲解）：**gpsd**（Debian 3.25-5+deb13u2；gpsfake→TPV mode=3 lat=39.904187167/lon=116.390742667/altMSL=44.0/uSat=12；无 Rx；交叉 pynmeagps/pyubx2/pygnssutils/ubx2rinex/rtkbase/bnc；下一优先 cors-relay）。最近新增（用法讲解）：**ublox_dgnss**（0.7.6/`7ace9d5`/tag 0.7.6；launch×11/config×3/msg×65/srv×4；ublox_dgnss_node；无 ROS/无 Rx 门禁；交叉 pyubx2/septentrio-gnss-driver/swiftnav-ros2；下一优先 ublox_driver 或 gpsd/cors-relay）。最近新增（质检）：**libswiftnav+ubx2rinex 质检复跑通过**（2026-09-24 05:39 EDT；250 PASSED；F9T 298/G01 C1C=21360867.696；coldstart 561+9）。最近新增（用法讲解）：**ubx2rinex**（0.3.0/`3b67fd0`；F9T OBS 298/G01 C1C=21360867.696；coldstart OBS 561+NAV 9；无 RAWX→0；交叉 pyubx2/pygnssutils/georinex/rinex-cli；下一优先 gpsd / cors-relay）。最近新增（用法讲解）：**libswiftnav**（tip `19331e0`/LGPL-3.0；CMake `libswiftnav.a`；gtest **250 PASSED**/24；`calc_ionosphere` **7.202448** m；`wgsecef2llh` ≈37.4286N；对照 libsbp 协议≠数学；交叉 piksi-tools/swiftnav-ros2/gnsstk；下一优先 ublox_dgnss）。最近新增（用法讲解）：**swiftnav-ros2**（`swiftnav_ros2_driver` 1.0.0/`c35c6ef`/v1.0.0；launch×1/config×1/msg×1；sbp-to-ros；无 ROS/无 Rx 门禁；交叉 libsbp/piksi-tools/septentrio-gnss-driver；下一优先 libswiftnav / ublox_dgnss）。最近新增（用法讲解）：**piksi_tools**（4.0.0/`02f1532`；serial_link JSON 61599；PosLLH 4686/≈37.7735N；roundtrip n_sats=15；无 Rx；交叉 libsbp；下一优先 swiftnav-ros2）。最近新增（用法讲解）：**groops**（`7e1bd6d`；Sp3 G01 289 历元；GRAZ 2880/30；未全日 PPP）+ **rapppid**（v5.1/`28fd517`；无 MATLAB；交叉 pride-pppar/great-pvt/rtklib）。最近新增（用法讲解）：**rtcm3torinex**（SVN r9404/WC r11044；2.9404；`make`；euref STR222；VALDM RINEX3 43 历元 G03 C1C=25238622.890；`-P` 75 行；rtk2go 400；obsolete→BNC；交叉 pyrtcm/bnc/pygnssutils/ntrip-client；下一优先 piksi_tools / swiftnav-ros2）。最近新增（质检）：**groops+rapppid 质检复跑通过**（2026-09-24 05:33 EDT；GROOPS Sp3 **289**/gaps=0；CLK 69182 B；GRAZ 2880/30；`01`/`02` 缺 tides/transmitterList；raPPPid CODE 633/树 635；无 MATLAB）。

最近新增（用法讲解）：**rinex-cli**（0.12.1/`f4dd4c3`；ACOR 25 历元 HTML QC；ESBC gz 2880；filegen/-P/--gzip；G07 C1C=23818653.240；tbin/split panic；交叉 georinex/rinexmod/hatanaka/crx2rnx/rnxcmp/teqc/gfzrnx/gnsspy/gnsstools）。最近新增（质检）：**graphgnsslib+great-pvt 质检复跑通过**（2026-09-24 05:21 EDT；去 `-s 1`；SPP 251×Q5 / RTK 94×Q2；GODN 3D≈0.0062 m）。最近新增（用法讲解）：**libsbp**（`sbp` 6.5.2/`2b883ad`；sbp2json one_msg snr=16.2；roundtrip PosLLH 15 SV；short 2382/roundtrip 5000；无 Rx；交叉 septentrio-gnss-driver/pyubx2/pyrtcm/pysbf2；下一优先 rtcm3torinex）。最近新增（用法讲解）：**graphgnsslib**（`d861802`；georinex+RTKLIB 基线；无 ROS/Docker 未跑 FGO；交叉 rtklib/gnss_lib_py/great-pvt）+ **great-pvt**（v1.4.0/`8bd3d23`；GODN 1 h DF Float 120 历元 3D RMS≈0.006 m；交叉 pride-pppar/rtklib/ginan）。

最近新增（用法讲解）：**rinex-cli**（0.12.1/`f4dd4c3`；ACOR 25 历元 HTML QC；ESBC gz 2880；filegen/-P/--gzip；G07 C1C=23818653.240；tbin/split panic；交叉 georinex/rinexmod/hatanaka/crx2rnx/rnxcmp/teqc/gfzrnx/gnsspy/gnsstools）。最近新增（质检）：**crx2rnx 质检复跑通过**（2026-09-24 05:19 EDT；AJAC 26→17；ACOR=GSI）。最近新增（质检）：**ginan+rtkbase 质检复跑通过**（2026-09-24 05:16 EDT；ALIC≈0.08 m；ConfigManager/12 unit）。最近新增（用法讲解）：**septentrio-gnss-driver**（1.4.8/`5613af2`；ROSaic；launch×3/config×4/msg×26；无 ROS/无接收机门禁；交叉 sbfparser/pysbf2/haslib；下一优先 libsbp / rtcm3torinex）。最近新增（用法讲解）：**ntrip-client**（0.2.1/`7d4c6d3`；`simple-cli` list/find-nearest/subscribe；rtk2go 766/igs-ip 384/centipede 1270；VALDM 86 帧；交叉 ntripstreams/pygnssutils/bkg-ntripcaster/bnc/crx2rnx）。最近新增（用法讲解）：**pysbf2**（1.0.5/`a68fe44`；PVTCartesian 往返；pvtcart Type=6 NrSV=36；status CPULoad=28；examples 232；混流 NMEA+RTCM；MSGIDS=125 无 ISM；交叉 sbfparser/haslib/pyubx2；下一优先 septentrio_gnss_driver）。最近新增（质检）：**ginan/rtkbase 质检复跑通过**（2026-09-24 05:16 EDT；ALIC≈0.08 m；ConfigManager 12 unit）。最近新增（用法讲解）：**ginan**（v4.1.4/`5033996`；预编译 pea dry-run；PPP 20 历元 ALIC≈0.08 m vs IGS20；交叉 rtklib/pride-pppar/rtkbase）+ **rtkbase**（2.7.0/`2ce7ce0`；ConfigManager+install help；无 Pi/GNSS 未启服务；交叉 rtklib/bkg-ntripcaster/ginan）。**sbfparser**（1.0.3/`ea84256`；receiver_status TOW 49638143；log 748/49；ExtEvent 往返；HAS GALRawCNAV 11774；tip 无 ISM 块；交叉 haslib/ismr-downloader/pyubx2；下一优先 pysbf2）。最近新增（用法讲解）：**crx2rnx**（2.7.0/`765ddeb`；Rust CRX→RNX；ACOR C1C G07=23818653.24=GSI；AJAC V2 17≠26 SV；PATH 同名陷阱；交叉 rnxcmp/hatanaka/rinexmod/georinex）。最近新增（质检）：**navdecoder/gnss-multipath-analysis 质检复跑通过**（HAS 801/48288/1.1 MB；B2b 7346/532/277；NMBUS C1C 1.273/1.093/周跳47；tips `7947333`/`806c3d9`）。最近新增（用法讲解）：**navdecoder**（`7947333`；HAS 截短 801×data collected + B2b SSR 532；交叉 b2blib/haslib/cssrlib/madocalib）+ **gnss-multipath-analysis**（2.2.0/`806c3d9`；NMBUS C1C RMS≈1.273/wRMS≈1.093 周跳47；交叉 georinex/gfzrnx/teqc/rtklib）。最近新增（质检）：**ismr-downloader 质检复跑通过**（缺参 exit 1；SSL；token 400；tip `cca68e4`）。最近新增（质检）：**ntripstreams/gampii-good 质检复跑通过**（rtk2go 767/STR765；igs-ip 391/STR384；订流 400；AgPartner_2 251；GOOD BRDC 11371068 B + igs14/20.atx skip）。最近新增（用法讲解）：**gnss-downloader**（`e6d0d84`/V3.0；无下载 CLI；WHU SIZE 57792；NLST 425；NASA 明文失效；交叉 gdds/gampii-good/fast/data-access）。最近新增（用法讲解）：**DRCycleSlip**（tip `f57d74d`；无 PyPI；search/find 组合；BAKO G24 注入 700→(23,18,17) deltaN≈-1.23/1.13/-1.10；硬编码 Windows 路径坑；对照 cycle-slip-correction/georinex/anubis）。最近新增（用法讲解）：**ismr-downloader**（0.2.0/`cca68e4`；API token 400 探针；SSL+注册门禁；交叉 data-access ISMR）。最近新增（质检）：**claslib/b2blib 质检复跑通过**（CLAS dump header 3601 + test1 3580 GGA；B2b WUH2 9×Q=6 首末 ECEF 对齐；tow 漂移坑已补）。最近新增（用法讲解）：**claslib**（`1e3a75d`/0.8.4；ssr2osr dump header 3601 + test1 3580 GGA ≈36.1036N 140.0863E；交叉 cssrlib/madocalib/rtklib）+ **b2blib**（`fe7c4c0`；WUH2 5 min 9×Q=6；Linux makefile+硬编码路径坑；交叉 haslib/cssrlib/claslib/madocalib/rtklib）。最近新增（用法讲解）：**ntripstreams**（0.3.5/`889ffb9`；rtk2go STR765 / igs-ip STR384；无订户 400；AgPartner_2 251 帧；1029；交叉 pygnssutils/bkg-ntripcaster/bnc/pynmeagps/pyrtcm）。最近新增（用法讲解）：**gampii-good**（tip `479aa14`/v3.1；CMake `run_GOOD`；WHU BRDC `BRDC00IGS_R_20240010000_01D_MN.rnx` 11371068 B + `igs14.atx`/`igs20.atx`；无参 Usage exit 255；对照 gdds/fast/data-access）。最近新增（用法讲解）：**pyspartn**（1.1.0/`8fc58f8`；SPARTN 传输层往返；GAD SF005=152 nSF=228；d9s 3007=OCB1692+HPAC1127+GAD188；无接收机/无 L-band；无 CLI→gnssstreamer；交叉 pyubx2/pynmeagps/pygpsclient/haslib/pyrtcm）。最近新增（质检）：**gnsstk/teqc/pyrtcm 质检复跑通过**（BAHR 120；teqc MP12≈0.20 EOL 边界确认；RTCM 1005/11 帧/MSM3）。最近新增（质检）：**rinexmod/pyubx2/ionex-rs/madocalib/aacgmv2 质检复跑通过** + **kamodo 短硬入库**（ccmc 26.9.2；SWMF_IE ΣH=9.1183；demo064a；UBX NAV-PVT 53.4507228）。最近新增（用法讲解）：**pyrtcm**（1.2.0/`5d66c7a`；1005 往返 llh≈32.07N 34.77E；RTCM3.log 11 帧；MSM `parse_msm` 8×20；无 CLI→gnssstreamer；交叉 pygnssutils/pyubx2/pynmeagps）。最近新增（用法讲解）：**gnsstk**（库 15.3.1/`55ea334`+apps `1aeb7d2`；BAHR RinSum 120 历元）+ **teqc**（2019Feb25；demo.18o +qc MP12≈0.20；EOL→gfzrnx/anubis/rnxcmp）。最近新增（用法讲解）：**pyubx2**（1.3.6/`4abbfa6`；UBX SET/POLL/ACK 往返；NAV-PVT 53.4507228；mon_span 109；无 CLI→gnssstreamer）。最近新增（用法讲解）：**rinexmod**（4.2.1；demo.10o→demo064a.10o MARKER MRKR→DEMO / AGENCY IPGP / REC TRIMBLE NETR9；长名 DEMO00FRA…rnx.gz；默认 Hatanaka 样例时钟偏移坑；交叉 georinex/autorino/hatanaka）。最近新增（用法讲解）：**gnsstools**（0.0.1/`e496093`；OBS E7 C1=28344990.66=georinex；NAV select G02；SP3 G01；**无 PyPI**/无 setup.py）。最近新增（用法讲解）：**aacgmv2**（2.7.1/`5f85579`；mlat≈50.53/mlon≈−4.09/mlt≈10.09；需 python3-dev；交叉 apexpy）。最近新增（质检）：**gnsspy 质检复跑通过**（3.0.1/`e6879bf`；demo.10o→22×9/2历元/14SV；G07 L1=118767195.326=georinex；converter 2→3 OK / XYZ Y/Z=0；3→2 回写 `read_obsFile` Length mismatch；无 PyPI；`.crx`→first-line ValueError）。最近新增（用法讲解）：**gnsspy**（3.0.1/`e6879bf`；demo.10o pandas 22×9；G07 L1=C georinex；converter 2→3；无 PyPI；`.gz` 读坑）。最近新增（质检）：**glab-upc/pynmeagps/gdds 质检复跑通过**（gLAB 2880/3D95=4.75；pynmea *5D；GDDS WHU NLST 时好时坏）+ **geospacelab**（0.14.8；OMNI/WDC/GFZ + Madrigal TEC；SYM_H=-234；TEC@06:30 max=114）+ **gps-measurement-tools/pygpsclient 质检复跑通过**。最近新增（用法讲解）：**ionex-rs**（crates.io 0.1.0/`bcb9171`；CKMG 129575 点/9.2 TECU/往返）+ **madocalib**（VER 2.1/`0089f7d`；MIZU 118 历元 Q=6）+ **glab-upc**（官方 v6.0.0；abmf SPP 2880 历元 3D95≈4.75 m）+ **pynmeagps**（1.1.7/；GGA 往返）+ **gdds**（`2a8543c`；无 CLI；NOAA brdc/p041+ITRF PSD；WHU FTP 425；CDDIS 401；Earthdata 硬编码）+ **gps-measurement-tools**（`ab1aebb`；demo→android_rinex 223 历元/L1C 全 0；相位样例 nonzero）+ **pygpsclient**（1.7.6；pyrinexconv O1677/N55037；无 tkinter）+ **cycle-slip-correction**（`c465dd4`；无 PyPI；BAKO 3.03 40 历元+PDF；官方 2019 pin 失败改现代钉）+ **diffionmap**（`57ceb1d`；CODG/WHUC 读路径+IGRG mean；Basemap 受限）+ **cddis-highrate-downloader**（1.0.2；FTPS SIZE 706256；RETR 425）+ **msise00**（1.11.1；Tn@250km）+ **pysatCDAAC**（0.0.5；ionprf 59→53；ionphs 144 下、load 维冲突）+ **pyirtam**（0.0.7；LGDC 四系数+IRI/IRTAM NmF2/vTEC）+ **fast**（3.01.01；ABPO satNum+1h SPP；FTP 下载失败记坑）+ **awsgnssroutils**（1.2.7；Phase 3 文件+atm 对照；S3 开放/rotcol 门禁）+ **gnss_lib_py**（1.1.0 NavData/OBS）+ **pyiri**（0.1.7 单点 NmF2/vTEC）。最近新增（质检）：**iri2016**（1.12.0；xarray 剖面+foF2/TEC；与 pyglow 同点对照）+ **pyglow**（Py3.8/`1988757`；IRI-2016/2012 剖面+IGRF/HWM14 实跑；`igrf2015` 静默退出坑）。最近新增（用法讲解）：**cosmic-crunch**（2.1.2；GENESIS L2 10 文件实拉+netCDF groups 探活；边界≠CDAAC ionPrf）。最近质检（R11）：**haslib**（1.0.2；11 HAS；RTCM/IGS 字节；`-m`/`HAS_Decoder.py` 帮助坑）+ **laika**（2880 历元/PDOP/pytest 17 复跑）。最近新增（质检）：**hatanaka**（2.8.1/`rinex-decompress`+georinex 实跑）+ **R10 质检** `rnxcmp`（gzip/CRLF/`-h`）/`nequickg`（Medium 全表 + `map`/plt 坑）。最近新增（用法讲解）：**android_rinex**（GnssLogger→RINEX；1379 历元+georinex 探活）+ **haslib**（1.0.2 SBF→RTCM 11 HAS）+ **laika**（slac1700.18o 实跑；Earthdata 未跑）；前序 **rnxcmp**（GSI RNXCMP 4.2.0 实跑）+ **nequickg**（Py3 移植后 Medium 校验行实跑；官方 C 登记受限）；前序 **pinot**（orderfile/sitecheck/metacheck 实跑）+ **autorino**（2.4.2 cfgfile_check 实跑；convert 环境受限）；前序 **cssrlib**（1.2.1 SPP）+ **gnss-tec**（1.1.1）。最近质检（ops）：**R9 二遍**已补 `cssrlib`（`nav.t`）/`gnss-tec`（stdout+type N）/`pinot`（subnet/low2upper 复跑）/`autorino`（check_rnx `figure_saver` 实错）。**R8 二遍**已补 `pytecgg`（ABMF 全日 veq 实跑；作者 viventriglia）/`gfzrnx`（`-sifl` guide-only，无官方二进制 stdout）。**R7 二遍**已补 `georinex`（NAV 实跑）/`rtklib`（apt↔EX PATH）/`bnc`（REQC vs NTRIP 标签）。Round6：**anubis**（登记受限）+ **pride-pppar**（3.2.11 实跑头；FTPS 未出解）；**sh-gim 未扩**。Round5：**pygnssutils**；Round4：**bkg-ntripcaster**；Round3：**ionex-gim** / **oasis-roti** / **ionomoni**；Round2：**bnc** / **georinex** / **iono-scintillation**；Round1：**gfzrnx** / **rtklib** / **pytecgg**。行数以本表 `wc -l` 为准。

## 推荐阅读顺序（新人）

1. 本页「全部手册」表 + [data-access](../data-access.md)
2. [georinex](./georinex.md) 冒烟
3. 路径 A：[pytecgg](./pytecgg.md) + 教程 02/16
4. 路径 B：[oasis-roti](./oasis-roti.md) 或 [ionomoni](./ionomoni.md) + 教程 05
5. 需要定位再 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
6. 实时课再 [gpsd](./gpsd.md)/[pygnssutils](./pygnssutils.md)/[ntripstreams](./ntripstreams.md)/[ntrip-client](./ntrip-client.md)/[pyrtcm](./pyrtcm.md)/[pyspartn](./pyspartn.md)/[pyubx2](./pyubx2.md)/[ubx2rinex](./ubx2rinex.md)/[septentrio-gnss-driver](./septentrio-gnss-driver.md)/[ublox-dgnss](./ublox-dgnss.md)/[ublox-driver](./ublox-driver.md)/[pynmeagps](./pynmeagps.md)/[pynmea2](./pynmea2.md)/[minmea](./minmea.md)/[pymap3d](./pymap3d.md)/[pygpsclient](./pygpsclient.md)/[bnc](./bnc.md)；教学定位拆解见 [glab-upc](./glab-upc.md)
7. GIM 课 [ionex-gim](./ionex-gim.md) / Rust [ionex-rs](./ionex-rs.md)；SH-GIM 仅边界；CLAS → [claslib](./claslib.md)；MADOCA → [madocalib](./madocalib.md)；B2b → [b2blib](./b2blib.md)/[navdecoder](./navdecoder.md)；多路径 QC → [gnss-multipath-analysis](./gnss-multipath-analysis.md)

---

## 不要做的事

- 不要把未校准相对 TEC 当绝对产品发表。
- 不要期望 SH-GIM clone 后出全球球谐解。
- 不要把 ROTI 当硬件 S4。
- 不要在未 QC 的坏站上硬跑 PPP/TEC。
- 不要把 PPP 残差当 STEC 产品。
- 不要把 Free/Pro、公开/专有功能写混。
- 不要把口令提交进 git。
- 参数冲突时以上游帮助为准。
- 并行写作者：勿同时全文重写同一 `docs/software/*.md`；先改本页状态再动手。

---

## 工具依赖速览

```text
data-access
   ├─ autorino (厂商 RAW→RINEX3/4 入库)
   ├─ rinexmod (RINEX 头/长短名/压缩规范化；autorino 伴生)
   ├─ android_rinex (手机 GnssLogger→RINEX3)
   ├─ cosmic-crunch (GENESIS 大气 RO L2→netCDF；电离层 RO→data-access/CDAAC)
   ├─ awsgnssroutils (AWS RO 三型查/下；电离层用 calibratedPhase；Ne→CDAAC)
   ├─ pysatcdaac (CDAAC ionPrf/ionPhs→pysat；Ne 用 ionprf；ionphs 建议 netCDF4)
   ├─ teqc (EOL 翻译/编辑/QC；后继 gfzrnx/anubis/rnxcmp)
   ├─ gnsstk (C++ 库 + RinSum/RinDump；原 GPSTk)
   ├─ pinot (旧 TEQC 批壳 / 缺站日目录)
   ├─ gampii-good (GAMP II YAML 观测/产品下载 GOOD)
   ├─ fast (下载/QC/粗 SPP/选站)
   ├─ gdds (IGS/CORS/产品/时序 GUI 下载)
   ├─ gnss-downloader (PyQt WHU/NASA 日文件；2020；无下载 CLI)
   ├─ rnxcmp (官方 Hatanaka CRX)
   ├─ hatanaka (Python CRX↔RNX / georinex 依赖)
   ├─ crx2rnx (Rust 仅解压 CRX；≠ GSI/hatanaka 同名)
   ├─ rinex-cli (Rust QC HTML + filegen；≠ 纯库 rinex)
   ├─ gfzrnx (可选清洗)
   ├─ anubis (门禁)
   ├─ georinex (探活)
   ├─ gnsspy (pandas 读 / RINEX 2↔3；无 PyPI)
   ├─ gnsstools (轻量 RINEX/SP3→pandas；无 PyPI；对照 georinex/gnsspy)
   ├─ cycle-slip-correction (R3 周跳试验；不写回 OBS)
   ├─ drcycleslip (三频注入–探测教学；不写回 OBS)
   ├─ gnss-tec / pytecgg (路径 A；粗相对→校准)
   ├─ oasis-roti / ionomoni (路径 B)
   ├─ ionex-gim (对照)
   ├─ ionex-rs (Rust IONEX 读写)
   ├─ diffionmap (两幅 IONEX 并排 VS)
   ├─ cddis-highrate-downloader (CDDIS high-rate 15 min)
   ├─ geospacelab (OMNI/指数/Madrigal TEC 产品图)
   ├─ pyglow (IRI 气候态对照)
   ├─ iri2016 (IRI-2016 → xarray)
   ├─ iri-fortran (官方 IRI-2026 Fortran；fort.7)
   ├─ iri-2026-package / iri-common-files (发行物清单 / 公共系数)
   ├─ pyiri / pyirtam (纯 Python IRI / IRTAM)
   ├─ nequick2-ictp (ICTP NeQuick 2 申请页；≠ nequickg)
   ├─ apexpy (Apex/QD/MLT 磁坐标)
   ├─ aacgmv2 (AACGM-v2 / MLT；交叉 apexpy)
   ├─ kamodo (CCMC 模式场函数化；SWMF_IE)
   ├─ msise00 (NRLMSISE-00 中性大气)
   ├─ gps-measurement-tools (GnssLogger 采集；→ android_rinex)
   ├─ minmea (嵌入式 C NMEA 解析核)
   ├─ pynmea2 (经典高星标 NMEA 解析；对照 pynmeagps)
   ├─ pymap3d (大地/ECEF/ENU/AER；geospace-code)
   ├─ gpsd (系统 GNSS 守护 / gpsfake+gpspipe；默认 2947)
   ├─ pygpsclient (板卡 GUI / NTRIP；捆 pygnssutils)
   ├─ pynmeagps (NMEA 编解码；pygpsclient/pygnssutils 底层)
   ├─ pyubx2 (UBX 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ ubx2rinex (UBX→RINEX OBS/NAV CLI；需 RAWX；对照 pyubx2)
   ├─ pyrtcm (RTCM3 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ rtcm3torinex (NTRIP RTCM3→RINEX；obsolete→BNC；对照 pyrtcm)
   ├─ pyspartn (SPARTN 编解码；pygpsclient/pygnssutils 底层；无 CLI)
   ├─ pysbf2 (SBF 编解码；同栈；无 CLI；对照 sbfparser)
   ├─ septentrio_gnss_driver (ROSaic 实时 ROS；对照 sbfparser/pysbf2)
   ├─ libsbp (Swift SBP；PyPI sbp / sbp2json；对照 pyubx2/pyrtcm/pysbf2)
   ├─ piksi_tools (Swift 现场壳；配 libsbp；无 Rx 用 --file)
   ├─ swiftnav-ros2 (官方 ROS2 SBP 驱动；包 swiftnav_ros2_driver；无 ROS 门禁)
   ├─ libswiftnav (C 数值核；星历/Klobuchar；≠ libsbp 协议)
   ├─ ublox_dgnss (ROS2 USB-UBX；F9P/F9R/X20P；无 ROS 门禁)
   ├─ ublox_driver (ROS1 ZED-F9P；gnss_comm/GVINS；无 ROS 门禁)
   ├─ glab-upc (教学 SPP/PPP；官方 UPC gLAB)
   ├─ ntripbrowser / cors-relay / ntripcaster-libev / ntrip-cpp / pygnssutils / ntripstreams / ntrip-client / bnc / bkg-ntripcaster (路径 C)
   └─ cssrlib / claslib / b2blib / rtppp-b2b / haslib / madocalib / laika / rtklib / great-pvt / groops / rapppid / ppp-wizard / gogps-matlab / gsilib / pride-pppar (路径 D)
sh-gim：仅路径 E 边界，不串进 A/B 主链
iono-scintillation：概念/仿真旁路，不替代实测 ROTI
```

---

## 与 tutorials 对照

| 教程 | 优先手册 |
| --- | --- |
| 02 / 16 | georinex · gnsspy · gnsstools · gnsstk · teqc · rinexmod · hatanaka · crx2rnx · rinex-cli · gnss-tec · pytecgg |
| 03 / 10 / 18 | ionex-gim · ionex-rs · diffionmap · sh-gim(边界) · pyglow |
| 04 | iri-fortran · iri-2026-package · iri-common-files · iri2016 · pyglow · pyiri · pyirtam · apexpy · aacgmv2 · msise00 · nequickg · nequick2-ictp · kamodo |
| 05 / 13 / 21 | oasis-roti · ionomoni · iono-scintillation · geospacelab |
| 06 / 20 | cssrlib · haslib · madocalib · laika · gnss_lib_py · android_rinex · gps-measurement-tools · pygpsclient · pynmeagps · pyubx2 · ubx2rinex · pyrtcm · pyspartn · pysbf2 · septentrio-gnss-driver · ublox-dgnss · ublox-driver · ntripstreams · ntrip-client · cors-relay · ntripcaster-libev · ntrip-cpp · glab-upc · rtklib · great-pvt · groops · rapppid · ppp-wizard · gogps-matlab · gsilib · rtppp-b2b · pride-pppar · ionomoni |
| 09 | pytecgg |

---

## 体量与文风

- 常规工具文：稠密操作优先；已全面 QUALITY 改写，多数 120–450 行
- SH-GIM：短边界说明优先（准确 > 凑行）
- 本索引：先列全手册 + 状态，再写路径
- 禁止问答注水、禁止为凑行数复读、禁止臆造未捕获的 stdout

---

## 相关

[data-access](../data-access.md) · [categories](../categories.md) · [tutorials](../tutorials/README.md) · [`PROJECTS.json`](../../PROJECTS.json)
