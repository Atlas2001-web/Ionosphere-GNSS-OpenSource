# libswiftnav · Swift GNSS 数值算法 C 库操作手册

目录：[`PROJECTS.json` → `libswiftnav`](../../PROJECTS.json) · 上游 <https://github.com/swift-nav/libswiftnav> · **URL 已核** · tip **`19331e0`**（2025-08-27；无近期 semver tag，仓内最新 tag 仍为 **v2.4.2**）· 许可 **LGPL-3.0** · 本机：CMake **3.31.6** + GCC **14.2.0** → `libswiftnav.a`；`make do-all-tests` → **250 PASSED** / 24 suites；迷你链 `calc_ionosphere` **7.202448** m · **无 PyPI / 无 CLI** · 2026-09-24 05:36 EDT

> 岗位：给软件接收机或自研 C/C++ 提供 **平台无关 GNSS 数值例程**（星历、Klobuchar 电离层、对流层、坐标、时间、单历元求解等）。冲突时：**上游 README / 头文件注释 / 本机 `tests/` > 本文**。  
> **对照：** [libsbp](./libsbp.md) = **SBP 通信协议**；本库 = **数学/算法**，**不**与 Swift 接收机通信。现场壳 → [piksi-tools](./piksi-tools.md)；ROS 2 → [swiftnav-ros2](./swiftnav-ros2.md)。更重的 C++ 底座 → [gnsstk](./gnsstk.md)。

## 1. 用途与边界

**做：**

- 标准 C 静态库 `libswiftnav.a`（头：`#include <swiftnav/...>`）
- 星历：`ephemeris.h`（GPS/GAL/BDS/GLO/SBAS 等 decode / `calc_sat_state` / 健康与有效窗）
- 大气：`ionosphere.h`（Klobuchar `calc_ionosphere`）、`troposphere.h`、`correct_iono_tropo.h`
- 坐标/时间/信号：`coord_system.h`、`gnss_time.h`、`signal.h`、`nav_meas.h`、`single_epoch_solver.h`、大地水准面等
- 单元测试：GoogleTest 目标 `test-swiftnav-common`（+ pedantic 编译检查）

**不做：**

- **不是** 与 Piksi/Swift 交换 SBP → [libsbp](./libsbp.md)（README 明示：*does not provide any functionality for communicating with Swift Navigation receivers*）
- **不是** 现场串口/刷机 → [piksi-tools](./piksi-tools.md)；**不是** ROS 驱动 → [swiftnav-ros2](./swiftnav-ros2.md)
- **不是** 发表级 PPP/RTK 产线 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md)
- **不是** 读 RINEX/IONEX 产品库 → [georinex](./georinex.md) / [ionex-gim](./ionex-gim.md)；本库无观测文件 CLI
- **无 CLI / 无 PyPI**：验收靠 **CMake 编库 + gtest**，禁止臆造“解算 stdout”

一句话：libswiftnav = **Swift 栈里的 C 数值核**；协议在 libsbp，运维在 piksi_tools，ROS 在 swiftnav-ros2。

| libsbp | libswiftnav |
| --- | --- |
| SBP 帧编解码 / `sbp2json` | 星历·电离层·坐标·时间·PVT 例程 |
| 多语言（PyPI `sbp` 等） | 主要是 **C** 静态库 |
| 面向接收机通信 | **不**通信；可嵌入 SDR / 主机程序 |

| 符号 | 含义 |
| --- | --- |
| LSN | LibSwiftNav 简称（上游 README） |
| `swiftnav/*.h` | 对外头；本机安装约 **37** 个 |
| `MAX_CHANNELS` | CMake cache 默认 **63**（`build/max_channels.h`） |
| `test-swiftnav-common` | 主 gtest 可执行文件（**250** cases） |
| `do-all-tests` | Make 目标；**不要**指望裸 `ctest`（本机构造下 “No tests were found!!!”） |

## 2. 安装（本机 CMake 路径）

### 2.1 依赖

```bash
sudo apt-get install -y build-essential cmake git
cmake --version   # 本机 3.31.6
gcc --version     # 本机 14.2.0
```

### 2.2 clone + 子模块（必做）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/swift-nav/libswiftnav.git
cd libswiftnav
git rev-parse --short HEAD    # 本机 19331e0

# 子模块：cmake/common + third_party/googletest
# 注意：.gitmodules 里 googletest 默认是 git@…，无 SSH 密钥会挂 → 先改 HTTPS
git config --file=.gitmodules submodule.third_party/googletest.url \
  https://github.com/google/googletest.git
git submodule sync
git submodule update --init --recursive
```

### 2.3 配置 / 编译 / 安装

```bash
mkdir -p build && cd build
cmake -DCMAKE_INSTALL_PREFIX=$HOME/.local/libswiftnav ..
make -j"$(nproc)"
# 期望：Built target swiftnav → build/libswiftnav.a
ls -lh libswiftnav.a
# 本机：~4.5M

make install
ls "$HOME/.local/libswiftnav/include/swiftnav" | wc -l
# 本机安装前缀实测：37 个头；lib/libswiftnav.a
```

可选（本机未强制）：Bazel（`BUILD.bazel` / `make do-all-unit-tests`）；Docker（`make docker-build`，需自构/拉 `swift-build` 基镜像，ECR 对外部用户常不可达）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Could not find … Googletest` / 无测试目标 | 未 `submodule update` | §2.2；HTTPS 改写 googletest URL |
| `Permission denied (publickey)` @ googletest | SSH submodule URL | 改 HTTPS 再 `sync` + `update` |
| `ctest` → `No tests were found!!!` | 测试未注册进 CTest | 用 `make build-all-tests && make do-all-tests` 或直接跑 `tests/test-swiftnav-common` |
| `make` 只出 `.a`、无 test 二进制 | 默认 `all` 不含测试 exe | `make build-all-tests` |
| `clang-format` / `clang-tidy` warning | 本机无工具 | 可忽略；不影响库与 gtest |
| `make install` 带上 gtest/gmock | 上游把捆绑 gtest 一并装进 prefix | 嵌入产品时只链 `libswiftnav.a` + `include/swiftnav` |

## 3. 端到端（本机真跑）

下文 `LSN=~/iono_ops/libswiftnav`，`B=$LSN/build`。

### 3.1 编测试并全量跑

```bash
cd $B
make build-all-tests -j"$(nproc)"
ls -lh tests/test-swiftnav-common tests/test-swiftnav-pedantic
make do-all-tests
# 等价：make do-all-unit-tests
```

**本机（节选）：**

```text
[==========] 250 tests from 24 test suites ran. (2251 ms total)
[  PASSED  ] 250 tests.
...
[100%] Built target do-test-swiftnav-pedantic
[100%] Built target do-all-tests
```

`test-swiftnav-pedantic` 为 pedantic 编译哨兵（几乎无用例输出）；主载荷在 `test-swiftnav-common`。

套件名（`--gtest_list_tests` 头，本机）：`TestAlmanac` `TestBitUtils` `TestCoordSystem` `TestCorrectIonoTropo` `TestDecodeGlonass` `TestEdc` `TestEphemeris` `TestGeoidModel` `TestGloMap` `TestGnssTime` `GnssTimeCppOperators` `TestIonosphere` `TestLinearAlgebra` `TestLogging` `TestNavMeas` `TestPvt` `TestSet` `TestShm` `TestSidSet` `TestSignal` `TestSubsystemStatusReport` `TestTroposphere` + 两组 `TestCoordSystem*` 参数化套件。

### 3.2 过滤：电离层 + 星历有效性

```bash
$B/tests/test-swiftnav-common \
  --gtest_filter='TestIonosphere.*:TestEphemeris.EphemerisValid:TestEphemeris.EphemerisBds'
```

**本机：**

```text
[==========] Running 4 tests from 2 test suites.
[ RUN      ] TestEphemeris.EphemerisBds
[       OK ] TestEphemeris.EphemerisBds (0 ms)
[ RUN      ] TestEphemeris.EphemerisValid
ERROR: null ephemeris
INFO: GPS L1CA 1 invalid ephemeris ...
...（负例探针的 ERROR/INFO 日志，属夹具预期）
[       OK ] TestEphemeris.EphemerisValid (0 ms)
[ RUN      ] TestIonosphere.CalcIonosphere
[       OK ] TestIonosphere.CalcIonosphere (0 ms)
[ RUN      ] TestIonosphere.DecodeIonoParameters
[       OK ] TestIonosphere.DecodeIonoParameters (0 ms)
[==========] 4 tests from 2 test suites ran. (0 ms total)
[  PASSED  ] 4 tests.
```

说明：`EphemerisValid` 打印的 `ERROR:`/`INFO:` 来自库内 logging（故意喂坏星历），**不是** gtest 失败。

### 3.3 迷你 C：链静态库调用 `calc_ionosphere`

（数值对齐仓内 `tests/test_ionosphere.cc` 第一组真值 **7.202** m，容差 1 mm。）

```bash
cat > /tmp/lsn_iono_demo.c <<'C'
#include <stdio.h>
#include <swiftnav/constants.h>
#include <swiftnav/ionosphere.h>
int main(void) {
  gps_time_t t = {.tow = 479820, .wn = 1875};
  ionosphere_t i = {.a0 = 0.1583e-7, .a1 = -0.7451e-8,
                    .a2 = -0.5960e-7, .a3 = 0.1192e-6,
                    .b0 = 0.1290e6, .b1 = -0.2130e6,
                    .b2 = 0.6554e5, .b3 = 0.3277e6};
  double d = calc_ionosphere(&t, -35.3 * D2R, 149.1 * D2R,
                             0.0, 15.0 * D2R, &i);
  printf("calc_ionosphere L1 delay_m=%.6f\n", d);
  return 0;
}
C
cc -O2 -I$LSN/include -I$B /tmp/lsn_iono_demo.c $B/libswiftnav.a -lm \
  -o /tmp/lsn_iono_demo
/tmp/lsn_iono_demo
```

**本机 stdout：**

```text
calc_ionosphere L1 delay_m=7.202448
```

### 3.4 迷你 C：`wgsecef2llh`

```bash
cat > /tmp/lsn_llh_demo.c <<'C'
#include <stdio.h>
#include <swiftnav/coord_system.h>
int main(void) {
  double ecef[3] = {-2700304.735, -4292604.736, 3855338.764};
  double llh[3];
  wgsecef2llh(ecef, llh);
  printf("llh deg=%.8f %.8f h=%.3f\n",
         llh[0] * 180.0 / 3.141592653589793,
         llh[1] * 180.0 / 3.141592653589793, llh[2]);
  return 0;
}
C
cc -O2 -I$LSN/include /tmp/lsn_llh_demo.c $B/libswiftnav.a -lm -o /tmp/lsn_llh_demo
/tmp/lsn_llh_demo
```

**本机 stdout：**

```text
llh deg=37.42864123 -122.17234450 h=100.211
```

## 4. I/O 字段（嵌入时常用）

| API / 产物 | 输入 | 输出 / 含义 |
| --- | --- | --- |
| `libswiftnav.a` | CMake 构建 | 静态库；链时加 `-lm` |
| `calc_ionosphere` | `gps_time_t`、用户 lat/lon、方位/高度角（rad）、`ionosphere_t` α/β | L1 电离层延迟（米） |
| `decode_*_ephemeris` / `calc_sat_state` | 导航比特 / `ephemeris_t` + 时间 | ECEF 位置速度 / 钟差等（见 `ephemeris.h`） |
| `wgsecef2llh` / 逆变换 | ECEF 米 | 纬经高（rad / m） |
| `test-swiftnav-common` | 无外部数据文件 | gtest PASS/FAIL；部分用例打 logging |

## 5. 关键参数

| 项 | 本机/默认 | 说明 |
| --- | --- | --- |
| `MAX_CHANNELS` | 63 | `cmake -DMAX_CHANNELS=…` 可改 |
| `CMAKE_INSTALL_PREFIX` | 自定 | 建议用户前缀，避免污染系统 |
| `LIBSWIFTNAV_ENABLE_STDERR_LOGGING` | ON | 库默认可打 stderr 日志（见 §3.2） |
| 构建系统 | CMake（手册路径）或 Bazel | CI/`Makefile` 亦走 Bazel 标签过滤 |

## 6. 接到哪步

- 已有 Swift 硬件/SBP 日志：先 [libsbp](./libsbp.md) / [piksi-tools](./piksi-tools.md) 拿观测与导航消息，再在自研代码里链本库做星历/大气。
- ROS 2 话题： [swiftnav-ros2](./swiftnav-ros2.md)（链的是 **C libsbp**，不是本库）。
- 要完整 PPP/RTK：观测落盘后走 [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) 等；本库只提供积木。
- 电离层产品/双频 TEC：仍用 [georinex](./georinex.md)+[pytecgg](./pytecgg.md)/[ionex-gim](./ionex-gim.md)；Klobuchar 仅广播模型，不等于 GIM。

## 7. 坑（≥8）

1. **名字像 libsbp**：装错仓 / 指望 `pip install` → 无 PyPI；本库只 CMake/Bazel。  
2. **子模块 SSH**：`third_party/googletest` 默认 `git@github.com` → 改 HTTPS（§2.2）。  
3. **`ctest` 空跑**：必须 `make do-all-tests` 或直接跑 `tests/test-swiftnav-*`。  
4. **默认 `make` 不含测试 exe**：先 `build-all-tests`。  
5. **gtest 日志里的 ERROR**：负例用例会打 `ERROR: null ephemeris` 等——以 `[ PASSED ]` 为准。  
6. **与 libsbp 版本无关**：本库不解析 SBP；不要把 SBP tip 和 LSN tip 绑死。  
7. **API 漂移**：仓描述写 *API 随版本变*；钉 tip/`19331e0` 或自打 tag；头文件为准。  
8. **`make install` 灌 gtest**：prefix 会多 `libgtest*.a` / `include/gtest`——部署清单勿整包拷给用户。  
9. **无 RINEX CLI**：别在本库找 `RinSum`；那是 [gnsstk](./gnsstk.md)-apps。  
10. **Docker 基镜像**：README 的 ECR `swift-build` 需 Swift 内网/自构；外部优先本机 CMake。  
11. **浅克隆 + submodule**：`--depth 1` 后仍需 `submodule update --init`；漏了会“能编库、无测试”。  
12. **许可 LGPL-3.0**：静态链进专有二进制时注意义务；协议栈 libsbp 是 MIT——别混谈。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| Swift SBP 编解码 / JSON | [libsbp](./libsbp.md) |
| Piksi 串口日志·刷机 | [piksi-tools](./piksi-tools.md) |
| ROS 2 收 SBP | [swiftnav-ros2](./swiftnav-ros2.md) |
| C 嵌入：星历/Klobuchar/坐标 | **本页 libswiftnav** |
| 更全 C++ RINEX/时间/apps | [gnsstk](./gnsstk.md) |
| 端到端 RTK/PPP | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md) |

Swift 开源栈四件套：**libsbp（协议）· libswiftnav（数学）· piksi_tools（现场）· swiftnav-ros2（ROS）**。下一缺口建议：**ublox_dgnss**（ROS 2 u-blox DGNSS；对照 septentrio/swiftnav ROS）或其它尚未短硬的厂商驱动。
