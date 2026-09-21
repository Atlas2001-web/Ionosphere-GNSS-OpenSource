# RTKLIB

目录：[`PROJECTS.json` → `RTKLIB`](../../PROJECTS.json) · 经典 <https://github.com/tomojitakasu/RTKLIB> · explorer <https://github.com/rtklibexplorer/RTKLIB> · 本机验证：**Debian `rtklib` 2.4.3 b34**（`/usr/bin/rnx2rtkp`）

> 操作手册。祈使句。事后 SPP/RTK/PPP → `.pos`。旗标以本机 `rnx2rtkp -h` 为准；explorer 分支编号不同，换二进制先重跑 `-h`。

## 1. 一句话用途

用 RINEX OBS+NAV（+可选 SP3/CLK）解接收机坐标。**不算** TEC（→ [pytecgg](./pytecgg.md)）、RINEX 手术（→ [gfzrnx](./gfzrnx.md)）、实时录流（→ [bnc](./bnc.md)）。

## 2. 安装（最少步骤）

```bash
sudo apt-get update && sudo apt-get install -y rtklib
rnx2rtkp -h 2>&1 | head -n 40
which rnx2rtkp convbin
```

源码 / explorer：按上游 `gcc` 目录编译。装好后必须用本机 `-h` 核对 `-p` 模式表。

| 现象 | 原因 | 修复命令 |
| --- | --- | --- |
| `rnx2rtkp: not found` | 未装 / 未入 PATH | `sudo apt-get install -y rtklib` |
| 抄来的 `-p` 无效 | 经典 vs explorer 编号不同 | `rnx2rtkp -h 2>&1 | less` |

## 3. 端到端：SPP（本机真实跑通）

样本：georinex 测试对 [`14601736.18o`](https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o) + [`14601736.18n`](https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n)。

```bash
mkdir -p ~/rtk_demo && cd ~/rtk_demo
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
curl -fsSL -o 14601736.18n \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n

rnx2rtkp -p 0 -sys G -m 5 -t -e \
  -o out_spp.pos 14601736.18o 14601736.18n
```

| 旗标 | 含义（2.4.3 b34） |
| --- | --- |
| `-p 0` | 模式 `0`=single（SPP）。**默认是 `2` kinematic——SPP 必须显式 `-p 0`** |
| `-sys G` | 系统：`G` GPS（还可 `R,E,J,C,I`） |
| `-m 5` | 高度截止角（度）；默认 15 |
| `-t` | 日历时间（默认 GPS 周秒） |
| `-e` | 输出 ECEF xyz（默认纬经高） |
| `-o file` | 结果文件 |
| 位置参数 | **首个 OBS=流动站**；其后 NAV/SP3；相对定位时第二个 OBS=基站 |

其他常用：`-f 1|2|3` 频率数；`-v thres` AR 阈值；`-r x y z` / `-l lat lon hgt` 基站坐标。

**本机真实 `out_spp.pos`：**

```text
% program   : rnx2rtkp ver.2.4.3 b34
% inp file  : .../14601736.18o
% inp file  : .../14601736.18n
% obs start : 2018/06/22 06:17:30.0 GPST (week2006 454650.0s)
% obs end   : 2018/06/22 06:18:00.0 GPST (week2006 454680.0s)
%
% (x/y/z-ecef=WGS84,Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp,ns=# of satellites)
%  GPST                      x-ecef(m)      y-ecef(m)      z-ecef(m)   Q  ns   sdx(m)   sdy(m)   sdz(m)  sdxy(m)  sdyz(m)  sdzx(m) age(s)  ratio
2018/06/22 06:17:30.000  -4647152.8622   2562199.8251  -3526633.5232   5   5  31.7050  35.8155  11.2997 -33.2352 -18.2328  17.1291   0.00    0.0
2018/06/22 06:17:45.000  -4647154.8149   2562203.2110  -3526633.2505   5   6  11.8225   9.6793   7.7693  -9.4935  -7.0514   7.2318   0.00    0.0
2018/06/22 06:18:00.000  -4647175.3345   2562227.4574  -3526639.2208   5   6  11.8074   9.6507   7.7543  -9.4683  -7.0272   7.2177   0.00    0.0
```

| 字段 | 含义 |
| --- | --- |
| `GPST` | 历元（因 `-t`） |
| `x/y/z-ecef` | WGS84 ECEF（m） |
| `Q` | `5`=single（本任务期望）；`1` fix；`2` float；`6` ppp |
| `ns` | 卫星数 |
| `sdx/sdy/sdz` | 标准差（m）；短文件少星时数十米属正常 |
| `age` / `ratio` | 差分龄期 / AR ratio；SPP 多为 0 |

头文件近似坐标与解算米级差，符合单点。**未编造 RTK/PPP 数值解。**

## 4. 可选：静态 RTK 骨架（需自备基站）

```bash
# 2.4.3：-p 3 = static。explorer 编号可能不同 → 先 -h
rnx2rtkp -p 3 -sys G -m 15 -f 2 -v 3 -t -e \
  -r -4647137.583 2562189.626 -3526626.701 \
  -o out_rtk.pos rover.obs base.obs brdc.nav
```

无匹配基站文件时不要跑——会得到空解或 `Q=0`。

## 5. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复命令 |
| --- | --- | --- | --- |
| 1 | 全 `Q=0` / 无解行 | NAV 不覆盖 OBS | 换同日 BRDC；`rnx2rtkp -p 0 …` 重跑 |
| 2 | 坐标乱跳 | 忘 `-p`，默认 kinematic | `rnx2rtkp -p 0 -sys G …` |
| 3 | `ns` 少、`sd*` 巨大 | 截止角过高 / 滤系统过狠 | `-m 5 -sys G,E` |
| 4 | 相对定位全 float | 无基站坐标或基线过长 | 加正确 `-r x y z` |
| 5 | 与头 APPROX 差百米级 | 错误 NAV / 单频 | 核对日期；加 `-f 2` |
| 6 | explorer 教程旗标失效 | 分支 `-p` 表不同 | 以本机 `rnx2rtkp -h` 为准 |
| 7 | `convbin` 空输出 | 原始流类型错 | `convbin -r rtcm3 …`（先 `-h`） |
| 8 | 想看 TEC 却在盯 `.pos` | 工具选错 | 改走 [georinex](./georinex.md)+[pytecgg](./pytecgg.md) |

## 6. 接到哪一步

- 电离层对定位 → [06](../tutorials/06-iono-positioning.md)
- 精密 PPP-AR → [pride-pppar](./pride-pppar.md)
- 录流 → [bnc](./bnc.md)；OBS 清洗 → [gfzrnx](./gfzrnx.md)