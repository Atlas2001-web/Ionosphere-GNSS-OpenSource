# rt-clk-service · 实时钟差/轨道/UPD/IFPB NTRIP 客户端操作手册

目录：[`PROJECTS.json` → `rt-clk-service`](../../PROJECTS.json) · 上游 <https://github.com/DoubleString/rt-clk-service> · tip **`1f44c36`**（`update application;` 2022-08-13 +0800）· **无 tag** · GitHub **license=null** · ★**12** · C++11/CMake · 本机验证（2026-09-24 07:13–07:16 EDT；**质检复跑 07:25 EDT**：`ssr_acq` **539928** B/sha₁₂=`d5985dc96f1d`；仓内预置 **1187984** B；`timeout 10` exit **124**/stdout+stderr **0** B；TCP `103.143.19.54:2101` **超时**；**未臆造** SSR）：`g++ 14.2.0` + `cmake 3.31.6` → `/tmp/rtclk-build/ssr_acq` **539928** B（sha₁₂=`d5985dc96f1d`）；仓内预置 `ssr_acq` **1187984** B（≠本机重编）；**无** `-h`/`--help`（`argc` 未用）；硬编码 NTRIP `usr:psd@103.143.19.54:2101/RTCM32SSR-COM`；本机 `timeout 10 ./ssr_acq` → exit **124**、stdout/stderr **0** B；TCP `103.143.19.54:2101` **超时**；**未连通 caster → 未臆造** ORBCLK/PHASEBIAS/CODEBIAS/IFPB 数值

> 岗位：**RTCM3 SSR 实时流解码演示**（NTRIP 客户端 + 捆版 RTKLIB `input_rtcm3`）→ stdout 打印轨道钟差 / 相位·码偏差 / IFPB。冲突时：**本机源码 `main.cpp` / 上游 README > 本文**。  
> 同链事后钟差 → [great-pce](./great-pce.md)；UPD/IFCB → [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)；滤波定轨 → [great-podflt](./great-podflt.md)；多 AC 综合 → [clkcomb](./clkcomb.md)/[spocc](./spocc.md)；产品门户 → [data-access](../data-access.md)。下游 PPP → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)。**≠** 精密产品生成器，**≠** 终端定位引擎。

## 1. 用途与边界

**做：**

- 经 **NTRIP** 订 RTCM3 SSR 挂载点，解码并 **printf** 到终端：广播星历、轨道+钟差（`[   ORBCLK]`）、相位偏差（`[PHASEBIAS]`）、码偏差（`[ CODEBIAS]`）、IFPB（`[     IFPB]`）
- 单可执行文件 **`ssr_acq`**；捆 `src/Rtklib/` + `pthread`
- README 宣称中国 beta：`103.143.19.54:2101` 挂载 `RTCM32SSR`（APC）/ `RTCM32SSR-COM`（COM），间隔 15 s，支持 G/E/B2/B3；欧/美条目为空
- 论文索引 DOI [10.1007/s10291-022-01287-3](https://doi.org/10.1007/s10291-022-01287-3)（三频 PPP-AR 应用文；**不是**本仓用户手册）

**不做：**

- **不是** 事后 CLK/SP3/OSB 估计 → [great-pce](./great-pce.md)/[great-podflt](./great-podflt.md)/[gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md)
- **不是** 多 AC 综合 → [clkcomb](./clkcomb.md)/[spocc](./spocc.md)；**不是** PPP/RTK 引擎 → [great-pvt](./great-pvt.md)/[rtklib](./rtklib.md)
- **无** CLI 参数、**无** 配置文件、**无** 落盘产品（仅 stdout）；caster 不可达时进程空转、**禁止**把空跑当成已收 SSR
- 硬编码口令仅演示；生产须自改源码并自备可用挂载点

一句话：**rt-clk-service = 最小 RTCM3 SSR NTRIP 解码 demo**（看懂实时轨道/钟/UPD/IFPB 流；不替代 GREAT/Gkit 产品链）。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** rt-clk-service | NTRIP→SSR stdout | `./ssr_acq` 死循环打印 |
| [great-pce](./great-pce.md) | 事后精密钟差 | `GREAT_PCE -x …` → `clk_*` |
| [great-upd](./great-upd.md) / [great-ifcb](./great-ifcb.md) | UPD / IFCB 估计 | `GREAT-UPD` / `GREAT-IFCB` |
| [great-podflt](./great-podflt.md) | 滤波精密定轨 | `great_podflt -x …` → SP3/ORB |
| [clkcomb](./clkcomb.md) / [spocc](./spocc.md) | 多 AC 钟/轨综合 | 离线文件进、文件出 |
| [bnc](./bnc.md) / [cssrlib](./cssrlib.md) | 通用 SSR 播发/解码 | 有 GUI/脚本，非本仓 |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++`≥5（本机 **14.2.0**）+ `cmake`≥2.8（本机 **3.31.6**）+ `make` | 源码编译 |
| `pthread`（glibc） | `target_link_libraries(… pthread)` |
| 可达的 NTRIP SSR 源 | 真冒烟；本机验证时 `103.143.19.54:2101` **不可达** |
| （可选）仓内预置 `ssr_acq` | 可能是异机构建；**推荐本机重编** |

### Linux 源码（本机已通）

```bash
sudo apt install -y build-essential cmake   # 本机已有 g++ 14.2.0 / cmake 3.31.6
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/DoubleString/rt-clk-service.git
cd rt-clk-service
git rev-parse --short HEAD   # 本机：1f44c36

mkdir -p /tmp/rtclk-build && cd /tmp/rtclk-build
cmake ~/iono_ops/rt-clk-service -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
ls -la ssr_acq                 # 本机：539928 B
sha256sum ssr_acq | cut -c1-12  # 本机：d5985dc96f1d
```

**本机产物：**

| 项 | 值 |
| --- | --- |
| 路径 | `/tmp/rtclk-build/ssr_acq` |
| 大小 | **539928** B |
| sha256₁₂ | `d5985dc96f1d` |
| 动态库 | `libstdc++` / `libm` / `libgcc_s` / `libc` |
| 仓内预置 | 树根 `ssr_acq` **1187984** B（勿与重编混用） |

可执行文件名是 **`ssr_acq`**，不是 `rt-clk-service`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `cmake_minimum_required` 弃用警告 | `CMakeLists.txt` 写 `2.8` | 可忽略；或改 `3.10` |
| 大量 `ISO C++ forbids converting a string constant to 'char*'` | 捆 RTKLIB 旧风格 | 警告，不阻断 |
| `undefined reference to pthread_*` | 未链 pthread | 确认 `CMakeLists.txt` 有 `pthread` 后重配 |
| 跑起来无任何输出 | caster 超时/重连；源码无连接失败 printf | 先测 TCP；改硬编码路径 |
| 想换挂载点无效 | **`argc` 未解析**，路径写死在 `main` | 改 `main.cpp` 字符串后重编 |

## 3. 端到端（本机真跑；质检复跑 2026-09-24 07:25 EDT）

### 3.1 无帮助 / 无参数（本机）

```bash
BIN=/tmp/rtclk-build/ssr_acq
$BIN -h          # 与无参相同：忽略 argv，直接连硬编码 caster
$BIN --help
timeout 10 $BIN >/tmp/rtclk.out 2>/tmp/rtclk.err
echo exit:$?     # 本机：124
wc -c /tmp/rtclk.out /tmp/rtclk.err   # 本机：0 0
```

**本机连通性：**

```bash
timeout 3 bash -c 'echo >/dev/tcp/103.143.19.54/2101'; echo tcp:$?
# 本机：tcp:124（连接超时）
timeout 8 curl -sS -m 7 -H 'Ntrip-Version: Ntrip/1.0' -H 'User-Agent: NTRIP curl/7' \
  -D - -o /tmp/rtclk-st.txt "http://103.143.19.54:2101/" | head
# 本机：curl (28) Connection timed out；无源表体
```

### 3.2 改源后期望行型（源码 printf；**本机未收到 SSR，数值勿抄**）

硬编码（`main.cpp`）：

```cpp
char c_pth[256] = {"usr:psd@103.143.19.54:2101/RTCM32SSR-COM"};
```

改为 `user:pass@host:port/MOUNT`（`stropen(…, STR_NTRIPCLI, …)`），重编后再跑。解码成功时行型来自源码（保留上游拼写 `receving`/`ephmeris`/`idoe`）：

```text
receving ephmeris: G01 2234  123456.0
receving GLONASS ephemeris: R01 2234  123456.0
[   ORBCLK] 2234    123456.000 G01 orb:     0.123     0.456    -0.789 iode:    12 c:     1.234 idoe:    12
[PHASEBIAS] 2234    123456.000 G01 pbias: L1C     0.011 L2W     0.022 ... yangle:     12.345 yrate:  0.0001
[ CODEBIAS] 2234    123456.000 G01 cbias: L1C     0.011 L2W     0.022 ...
[     IFPB] 2234    123456.000 G01 ifpb:     0.123 t0:   120000.000
```

源码格式串（本机摘录）：

```text
printf("receving ephmeris: %s %d %9.1lf\n", prn, week, toe);
printf("receving GLONASS ephemeris: %s %d %9.1lf\n", prn, week, toe);
printf("[   ORBCLK] %04d %13.3lf %s orb: %9.3lf %9.3lf %9.3lf iode: %5d c: %9.3lf idoe: %5d\n", clk.wk, clk.sow, cprn, orb.dx[i][0],
printf("[PHASEBIAS] %04d %13.3lf %s pbias: %-100s yangle: %9.3lf yrate:%9.4lf \n", wk, sow, cprn,
printf("[ CODEBIAS] %04d %13.3lf %s cbias: %-100s\n", wk, sow, cprn, p_obsstr);
printf("[     IFPB] %04d %13.3lf %s ifpb: %9.3lf t0:%13.3lf\n", wk, sow, cprn, ssr[isat].ifpb, sow_t0); /// ifpb in cycles, the GPS L5 carrier measurements should directly add this corrections, if sow_t0 is different, new ambiguity should be set
```

说明（源码注释，非本机测值）：

- `ORBCLK`：仅当同一卫星轨道与钟差均更新时打印；`c` 为钟差改正；BDS 用 `iodcrc`，其余用 `iode`
- `PHASEBIAS`：`pbias` **米**；换周需 `/ λ`；附 yaw 角/角速率
- `IFPB`：**周**；GPS L5 载波可直接加；`t0` 变化须重置模糊度
- `input_rtcm3` 返回值：`2` 星历、`10` 轨道钟、`20` 偏差/IFPB

**禁止**在未连通时把上面示例数字当真实产品。

## 4. 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | NTRIP RTCM3 SSR 二进制流（硬编码 `usr:psd@103.143.19.54:2101/RTCM32SSR-COM` 或改源后的 `user:pass@host:port/mnt`） |
| 输出 | **仅 stdout 文本行**；无 CLK/SP3/BIA 文件、无日志路径参数 |
| 超时 | `strsettimeout(stream, 60000, 10000)` → 60 s 超时 / 10 s 重连 |
| 持久化 | 无；杀进程即停 |

## 5. 参数

| 「参数」 | 实际 |
| --- | --- |
| CLI | **无**。`main(int argc, char *args[])` 不读 `argv` |
| 挂载/账号 | 改路径字符串后 `cmake && make` |
| 传输类型 | 源码固定 `STR_NTRIPCLI`（TCP 直连一行被注释掉） |
| 解码集合 | 仅处理 `input_rtcm3` 的 2/10/20；其它返回值丢弃 |

## 6. 接到哪步

```text
NTRIP SSR（自备或 README beta）
    → rt-clk-service / ssr_acq（看懂实时 ORBCLK / PHASEBIAS / IFPB）
        → 对照 IGS/分析中心 CLK·OSB：[data-access](../data-access.md)
        → 事后自产链：[great-podflt](./great-podflt.md) + [great-pce](./great-pce.md) + [great-upd](./great-upd.md)
        → 多 AC 综合：[clkcomb](./clkcomb.md) / [spocc](./spocc.md)
        → 终端 PPP-AR：[great-pvt](./great-pvt.md) / [pride-pppar](./pride-pppar.md)
```

电离层岗位：本工具**不**出 TEC/GIM；只帮助确认实时 SSR 偏差流是否到达。

## 7. 坑（≥8）

1. **无 `-h`**：任何 argv 都被忽略；勿期待 usage。
2. **路径写死**：忘改硬编码会一直打 README 中国 beta；本机 2026-09-24 该 IP:**2101** 超时。
3. **空 stdout ≠ 崩溃**：超时重连静默；务必用 `timeout` + `wc -c` 判断。
4. **预置二进制 ≠ 重编**：仓内 **1187984** B vs Release **539928** B；混用难复现。
5. **CMake 2.8**：新 CMake 仅警告；勿当配置失败。
6. **`-Wwrite-strings` 刷屏**：捆 RTKLIB；不代表链接失败。
7. **ORBCLK 要双更新**：仅 orb 或仅 clk 时源码分支为空，可能长时间无 `ORBCLK` 行。
8. **PHASEBIAS 单位是米**：当周跳/模糊度用时必须 `/ λ`；IFPB 才是周。
9. **口令明文**：路径中的演示账号在源码与字符串表；勿当生产密钥。
10. **无落盘**：不能当产品归档；要 CLK/BIA 仍走 [clkcomb](./clkcomb.md)/[data-access](../data-access.md)。
11. **license 空**：GitHub `license=null`；商用前自审捆 RTKLIB 与论文 DOI 许可。
12. **欧/美源 README 空白**：抄中国 IP 到境外环境必失败；自备 caster。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 快速看 SSR 是否在流 | **本文** `ssr_acq` | 单二进制、改一行路径 |
| 事后精密钟差/UPD/IFCB | [great-pce](./great-pce.md)/[great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md) | 有 XML/样例产品链 |
| 实时/滤波定轨 | [great-podflt](./great-podflt.md) | SP3/ORB 出盘 |
| 多 AC 钟差合成 | [clkcomb](./clkcomb.md) | 离线 CLK 进、合成 CLK 出 |
| 通用 NTRIP/RTCM 工具 | [bnc](./bnc.md)/[pyrtcm](./pyrtcm.md)/[ntrip-go](./ntrip-go.md) | 可配源表、录流、GUI |
| 终端 PPP | [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md) | 本仓只解码不定位 |

**别用它**：当正式实时产品平台、当 OSB/CLK 归档器、或在无 caster 时「跑一下出数」。
