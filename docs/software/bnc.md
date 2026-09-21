# BNC

目录：[`PROJECTS.json` → `BNC`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bnc> · FTP <https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/> · 本机验证：**BNC 2.13.7**（`bnc --help` 真输出）

> 操作手册。祈使句。NTRIP 订阅 / 录盘 / RINEX 编辑。账号口令禁止进 git。

## 1. 一句话用途

拉 NTRIP 源表、订挂载点、落盘 RINEX/原始流；也可用 **REQC** 离线拼接/抽稀。**不算** TEC（→ [pytecgg](./pytecgg.md)）、精密 PPP 长文、自建 Caster（→ [bkg-ntripcaster](./bkg-ntripcaster.md)）。

## 2. 安装（最少步骤）

```bash
mkdir -p ~/bnc && cd ~/bnc
curl -fsSL -o bnc.zip \
  https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/bnc-2.13.7-debian13.zip
unzip -q bnc.zip && chmod +x bnc-2.13.7
sudo apt-get install -y libqt5svg5 libqt5widgets5 libqt5network5 libqt5gui5
./bnc-2.13.7 --version
./bnc-2.13.7 --help | head -n 40
```

| 现象 | 原因 | 修复命令 |
| --- | --- | --- |
| `libQt5Svg.so.5: cannot open` | 缺 Qt5 | `sudo apt-get install -y libqt5svg5 libqt5widgets5 libqt5gui5 libqt5network5` |
| 无头立刻退出 | 未给 conf / 未 `--nw` | `./bnc-2.13.7 --conf lab.bnc --nw` |
| zip 极小 | 其实是 HTML 错误页 | `file bnc.zip; unzip -t bnc.zip` |

**本机 `bnc --help` 开头（真输出）：**

```text
Usage:
   bnc --help
       --nw
       --version
       --display {name}
       --conf {confFileName}
       --file {rawFileName}
       --key  {keyName} {keyValue}
```

## 3. 端到端：离线拼接四段 15 min → 1 h / 30 s（本机真实跑通）

不依赖公网 NTRIP。使用发行包 `Example_Configs`：

```bash
cd ~/bnc/Example_Configs
mkdir -p Output
../bnc-2.13.7 -nw -conf /dev/null \
  -key reqcAction Edit/Concatenate \
  -key reqcObsFile 'Input/BRUX00BEL_S_2021125*_15M_01S_MO.rnx' \
  -key reqcRnxVersion 3 \
  -key reqcSampling '30 sec' \
  -key reqcStartDateTime 1967-11-02T00:00:00 \
  -key reqcEndDateTime 2099-01-01T00:00:00 \
  -key reqcNewMarkerName BRUX_MARKER \
  -key reqcOutLogFile Output/RinexConcat.log \
  -key reqcOutObsFile Output/BRUX00BEL_S_20211251100_01H_30S_MO.rnx
```

| 键 / 旗标 | 含义 |
| --- | --- |
| `--nw` | 无窗口批处理 |
| `--conf /dev/null` | 空底配置；其余用 `--key` 覆盖 |
| `reqcAction` | `Edit/Concatenate` 或 `Analyze` |
| `reqcObsFile` | 输入 OBS（通配符需引号） |
| `reqcRnxVersion` | 输出 RINEX 主版本 2/3/4 |
| `reqcSampling` | 输出采样，例 `30 sec` |
| `reqcStartDateTime` / `reqcEndDateTime` | 时间窗 |
| `reqcNewMarkerName` | 改 MARKER NAME |
| `reqcOutLogFile` / `reqcOutObsFile` | 日志与输出 OBS |

**本机真实日志（截断）：**

```text
------------------------------------------------------------------------------
RINEX File Editing
------------------------------------------------------------------------------
Program           : BNC 2.13.7
RINEX Version     : 3.05
Sampling          : 30 sec
Input Obs Files   : Input/BRUX00BEL_S_2021125*_15M_01S_MO.rnx
Output Obs File   : Output/BRUX00BEL_S_20211251100_01H_30S_MO.rnx
------------------------------------------------------------------------------
Input Obs File: ...11:00:00 ... start: 2021-05-05 11:00:00
Input Obs File: ...11:15:00 ... start: 2021-05-05 11:15:00
Input Obs File: ...11:30:00 ... start: 2021-05-05 11:30:00
Input Obs File: ...11:45:00 ... start: 2021-05-05 11:45:00
```

**本机输出头（截断）+ 统计：** `grep -c '^>'` → **120** 历元（4×15 min @1 s 抽稀 30 s）。

```text
     3.05           OBSERVATION DATA    M                   RINEX VERSION / TYPE
BNC 2.13.7          box                 20260921 022524 UTC PGM / RUN BY / DATE
BRUX_MARK                                                   MARKER NAME
  4027881.6280   306998.5370  4919498.9840                  APPROX POSITION XYZ
    30.000                                                  INTERVAL
  2021     5     5    11     0    0.0000000     GPS         TIME OF FIRST OBS
```

## 4. 可选进阶：一挂载点实时录 RINEX

1. GUI：Add Stream → caster/port/账号 → Get Table → 选 mountpoint。
2. RINEX Observations：Directory、`File interval`、`Sampling`、`Version`。
3. Save → Start。无头复跑：

```bash
bnc --conf ~/bnc_configs/one_mount.bnc --nw
head -n 8 /data/rinex/lab/*.rnx
python -m georinex.time /data/rinex/lab/你的文件.rnx
```

官方 `Example_Configs` 账号仅供示例；生产换自有注册。

## 5. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复命令 |
| --- | --- | --- | --- |
| 1 | `libQt5*.so: not found` | 缺运行库 | `sudo apt-get install -y libqt5svg5 libqt5widgets5 libqt5network5` |
| 2 | 通配无输入 | shell 先展开 `*` | `--key reqcObsFile 'Input/BRUX*_MO.rnx'` |
| 3 | 输出 0 字节 | 路径错 / 未 `--nw` | 查 `reqcOutLogFile`；`ls -l Input` |
| 4 | Get Table 空 | 账号/代理/TLS | 配 `proxyHost`；调试可 `sslIgnoreErrors=2` |
| 5 | 改了 GUI 不生效 | 未 Start/Save | Save Options → Start |
| 6 | 口令进了 git | `.bnc` 含明文 | `chmod 600 lab.bnc; echo '*.bnc' >> .gitignore` |
| 7 | 想拼日却用错工具 | REQC 偏片段编辑 | 大日拼优先 [gfzrnx](./gfzrnx.md) |
| 8 | 实时流转 RTKLIB 无数据 | 未开 TCP 转发 | GUI 设 TCP out；`nc -v 127.0.0.1 2102 \| wc -c` |

## 6. 接到哪一步

- 落盘探活 → [georinex](./georinex.md)；清洗/抽稀 → [gfzrnx](./gfzrnx.md)
- 事后定位 → [rtklib](./rtklib.md)；Caster → [bkg-ntripcaster](./bkg-ntripcaster.md)
- 轻量脚本拉流 → [pygnssutils](./pygnssutils.md)