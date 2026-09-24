# gnssrefl · GNSS-IR 反射测量操作手册

目录：[`PROJECTS.json` → `gnssrefl`](../../PROJECTS.json) · 上游 <https://github.com/kristinemlarson/gnssrefl> · tip **`e8d9cd0`**（2026-09-22）· PyPI **`gnssrefl` 4.2.3** · ★**219** · 许可 **GPL-3.0** · 本机验证（**2026-09-24 07:00–07:13 EDT**；**质检复跑 07:21 EDT**：`pip install gnssrefl==4.2.3`；tip **`e8d9cd0`**；仓内夹具 `mchl` DOY **2025/011**；`gnssir -plt False` → `$REFL_CODE/2025/results/mchl/011.txt` **12542** B/**117** 行（头+**111** 弧）；RH 均值 **1.6916** m（**1.375–1.820**）；频点 **1/20/5** → **48/37/26** 弧；`quickLook -plt False` → 最低仰角 **0.0121°**；`quickLook_lsp.png` **187130** B + `quickLook_summary.png` **60482** B）：`pip install gnssrefl==4.2.3`；仓内 `test/data/refl_code` 站 **mchl** DOY **2025/011**；`gnssir` → `$REFL_CODE/2025/results/mchl/011.txt` **12542** B/**117** 行（头+**111** 弧）；RH 均值 **1.6916** m（**1.375–1.820**）；频点码 **1/20/5** → **48/37/26** 弧；`quickLook -plt False` → 最低仰角 **0.0121°**；图 `quickLook_lsp.png` **187130** B + `quickLook_summary.png` **60482** B

> 岗位：从 **RINEX/NMEA → SNR → Lomb–Scargle 反射器高度（RH）**，服务水位、雪深、土壤湿度等 GNSS-IR。冲突时：**本机 `gnssir -h` / 上游 README / ReadTheDocs > 本文**。  
> 读 OBS → [georinex](./georinex.md)；改/抽稀 → [gfzrnx](./gfzrnx.md)；定位/质量对照 → [rtklib](./rtklib.md)；码多路径 QC（非 IR）→ [gnss-multipath-analysis](./gnss-multipath-analysis.md)；前向多路径仿真 → [mpsim](./mpsim.md)。

## 1. 用途与边界

**做：**

- `rinex2snr`：RINEX OBS（+轨道）→ 年/`snr`/站 下的 `.snr??`
- `gnssir_input`：写站 JSON（纬经高、仰角窗、RH 搜索窗、频点、振幅门限）
- `quickLook`：单日 LSP 快检（出图到 `$REFL_CODE/Files/<站>/`）
- `gnssir`：按 JSON 批量出 RH 表（可跨午夜拼邻日 SNR）
- `daily_avg` / `subdaily`：日平均 / 亚日潮汐类后处理；`nmea2snr`：低成本 NMEA→SNR
- `installexe`：拉 CRX2RNX / gfzrnx 等外部二进制（linux64 / macos / mac-newchip）

**不做 / 本机限制：**

- **不是** PPP/RTK 引擎 → [rtklib](./rtklib.md)
- **不是** 只读 RINEX 进 xarray → [georinex](./georinex.md)
- **不是** Estey–Meertens 码多路径报告 → [gnss-multipath-analysis](./gnss-multipath-analysis.md)
- **不是** 前向电磁仿真 → [mpsim](./mpsim.md)
- Windows 官方主推 Docker；本机 Linux venv 实跑
- 本页冒烟用**仓内已有 SNR 夹具**，未重新拉 CDDIS RINEX/SP3（见坑）

一句话：gnssrefl = **GNSS-IR 产线 CLI**（SNR→RH）；几何与 QC 另接读库/定位引擎。

| 术语 | 含义 |
| --- | --- |
| `REFL_CODE` | 输入 JSON、SNR、results、Files、logs 根 |
| `ORBITS` | sp3/nav 缓存根（可与 `REFL_CODE` 同盘） |
| `EXE` | `installexe` 下落二进制目录 |
| SNR 后缀 | 默认 **66**（`rinex2snr`/`gnssir -snr`） |
| 频点码 | JSON/`-fr`：如 **1**=GPS L1，**20**=L2C，**5**=L5（以 `gnssir -h` 为准） |
| RH | 反射器高度（m）；弧段 LSP 峰值，非精密水准 |

## 2. vs georinex / gfzrnx / RTKLIB / gnss-multipath / mpsim

| | **本文 gnssrefl** | [georinex](./georinex.md) | [gfzrnx](./gfzrnx.md) | [rtklib](./rtklib.md) | [gnss-multipath-analysis](./gnss-multipath-analysis.md) | [mpsim](./mpsim.md) |
| --- | --- | --- | --- | --- | --- | --- |
| 角色 | SNR→RH | OBS→xarray | 编辑/抽稀 | 定位 | 码 MP/周跳 | 前向 SNR 仿真 |
| 输入 | RINEX/NMEA/SNR | RINEX | RINEX | RINEX | OBS+NAV/SP3 | 天线/地表设置 |
| 输出 | RH 表/图 | Dataset | RINEX | `.pos` | Report/CSV | SNR/相位误差曲线 |
| 本机 | pip + mchl 夹具 | 已短硬 | 登记受限 | apt/自编 | NMBUS 实跑 | Octave 仅 setup |

## 3. 安装

```bash
python3 -m venv ~/iono_ops/venv-gnssrefl
source ~/iono_ops/venv-gnssrefl/bin/activate
pip install -U pip
pip install 'gnssrefl==4.2.3'
python -c "from importlib.metadata import version; print(version('gnssrefl'))"
# 期望：4.2.3

export REFL_CODE=~/iono_ops/gnssrefl-run
export ORBITS=~/iono_ops/gnssrefl-run/orbits
export EXE=~/iono_ops/gnssrefl-run/exe
mkdir -p "$REFL_CODE" "$ORBITS" "$EXE"
# 建议写入 ~/.bashrc

installexe linux64    # 可选；RINEX3/Hatanaka 常用
which rinex2snr gnssir quickLook gnssir_input
```

源码对照：`git clone https://github.com/kristinemlarson/gnssrefl.git && git rev-parse --short HEAD` → 本机 tip **`e8d9cd0`**。

## 4. 端到端：mchl 夹具（本机真跑）

与上游 `test/data/refl_code` 同源（回归用 SNR，无需当场下载）。

```bash
source ~/iono_ops/venv-gnssrefl/bin/activate
export REFL_CODE=~/iono_ops/gnssrefl-run ORBITS=$REFL_CODE/orbits EXE=$REFL_CODE/exe

# 从上游测试树灌入 SNR + JSON（路径按你的 clone 调整）
SRC=~/iono_ops/gnssrefl/test/data/refl_code
mkdir -p "$REFL_CODE/2025/snr/mchl" "$REFL_CODE/input"
cp -a "$SRC/2025/snr/mchl/"*.gz "$REFL_CODE/2025/snr/mchl/"
cp -a "$SRC/input/mchl" "$REFL_CODE/input/"
gunzip -kf "$REFL_CODE/2025/snr/mchl/"*.gz

gnssir mchl 2025 11 -plt False
quickLook mchl 2025 11 -plt False
```

**本机结果（4.2.3 / tip `e8d9cd0`，2026-09-24 07:00–07:13 EDT）：**

```text
gnssir：Writing …/2025/results/mchl/011.txt
  Freq 1  QC：92 arcs → … → 48 saved
  Freq 20 QC：68 → … → 37 saved
  Freq 5  QC：50 → … → 26 saved
  Processed 1 days in 0.89 s
结果文件：12542 B / 117 行；数据弧 111
RH：mean=1.6916 m  min=1.375  max=1.820
  fr1 mean=1.6746 (n=48)；fr20=1.7012 (37)；fr5=1.7092 (26)
quickLook：minimum elevation angle … 0.0121
  Files/mchl/quickLook_lsp.png      187130 B
  Files/mchl/quickLook_summary.png   60482 B
```

结果表头字段（节选）：`year doy RH sat UTCtime Azim Amp eminO emaxO NumbOf freq … PkNoise DelT MJD refr`。

### 4.1 自有 RINEX 时的主链（本机未重拉外部数据）

```bash
# 1) OBS → SNR（需轨道；archive/orb 以 -h 为准）
rinex2snr <站> <年> <doy> -orb gnss -snr 66

# 2) 生成/更新站 JSON（纬经高必填或能从元数据解析）
gnssir_input <站> -lat <φ> -lon <λ> -height <h>

# 3) 快检 → 正式 RH
quickLook <站> <年> <doy> -plt False
gnssir <站> <年> <doy> -plt False
```

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `$REFL_CODE/input/<站>/<站>.json` | 仰角、方位、RH 窗、频点、`reqAmp`、折射开关 |
| `$REFL_CODE/<年>/snr/<站>/<站><doy>0.<yy>.snr66` | SNR 时间序列（可 `.gz`） |
| RINEX OBS | `rinex2snr` 入口；3.x 常需 `installexe` 工具链 |

| 输出 | 说明 |
| --- | --- |
| `$REFL_CODE/<年>/results/<站>/<doy>.txt` | RH 弧表（本机 011.txt） |
| `$REFL_CODE/Files/<站>/quickLook_*.png` | 快检图 |
| `$REFL_CODE/logs/<站>/…` | 屏统/调试日志 |

## 6. 参数速查

| 命令/旗标 | 本机常用 | 备注 |
| --- | --- | --- |
| `gnssir … -plt False` | 批处理 | 无显示环境必关 |
| `-snr 66` | 与 `rinex2snr` 一致 | 错后缀=找不到文件 |
| `-fr 1 20 5` | 覆盖 JSON 频点 | 与 `reqAmp` 长度对齐 |
| `gnssir_input -e1/-e2` | 仰角窗 | 过窄→弧少 |
| `-h1/-h2` | RH 搜索窗 (m) | 须盖住先验高度 |
| `rinex2snr -orb` | `gnss`/`nav`/… | 无网则预置 `$ORBITS` |

## 7. 接到哪步

1. 原始 OBS 探活 → [georinex](./georinex.md)；抽时段/改系统 → [gfzrnx](./gfzrnx.md)  
2. 站坐标/质量粗检 → [rtklib](./rtklib.md)（勿把 RH 当平面坐标）  
3. 天线/多路径污染对照 → [gnss-multipath-analysis](./gnss-multipath-analysis.md)  
4. 合成 SNR 教学/算法 → [mpsim](./mpsim.md)  
5. 数据礼仪与 Earthdata → [data-access](../data-access.md)

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ORBITS environment variable` 退出 | 未 export 或路径不存在 | `mkdir` + `export ORBITS=…`（注意拼写 **ORBITS**） |
| 2 | `REFL_CODE` 下找不到 snr/json | 目录约定年/站层级错 | 对照 `$REFL_CODE/<年>/snr/<站>/` 与 `input/<站>/` |
| 3 | `rinex2snr` 挂起/401 | CDDIS/Earthdata 门禁 | 预下载或见 [data-access](../data-access.md)；夹具冒烟可跳过 |
| 4 | 0 arcs saved | 仰角/方位/振幅门限过严 | 先 `quickLook`；放宽 `e1/e2`、`reqAmp`、`-azim*` |
| 5 | RH 跳变数米 | 旁瓣/多反射面/未掩遮 | 收紧方位扇区；对照潮位/实测；换频点交叉 |
| 6 | 与水准/测深差系统性偏差 | 未做 APC/雪深/潮汐模型 | 读结果头 `Phase Center…NOT been applied`；后处理自定 |
| 7 | JSON `gzip=False` 警告 | 旧默认 | 让其改 True，或 CLI `-gzip F` 显式保留 |
| 8 | 邻日弧在午夜截断 | 未载入 ± 小时 | 新版本默认可拼邻日；确认两侧 SNR 在盘 |
| 9 | `installexe` 后仍无 CRX | `EXE` 未进 `PATH` | `export PATH="$EXE:$PATH"` |
| 10 | Windows 路径混乱 | 官方不鼓励原生 pip | 用 Docker/WSL；路径一律正斜杠 |
| 11 | 把 RH 当椭球高发表 | 概念混淆 | RH=反射面相对天线的几何高；坐标用 [rtklib](./rtklib.md) |
| 12 | PyPI 无 TestData | 轮子不含夹具 | clone 上游 `test/data/refl_code` |

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 水位/雪深/土壤 GNSS-IR 产线 | **本文 gnssrefl** |
| 只读 RINEX 做自定义分析 | [georinex](./georinex.md) |
| 官方级 RINEX 编辑 | [gfzrnx](./gfzrnx.md) |
| 坐标/基线/PPP | [rtklib](./rtklib.md) |
| 码多路径 RMS/周跳报告 | [gnss-multipath-analysis](./gnss-multipath-analysis.md) |
| 合成多路径 SNR（论文图复现） | [mpsim](./mpsim.md) |

## 10. 相关

[georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [rtklib](./rtklib.md) · [gnss-multipath-analysis](./gnss-multipath-analysis.md) · [mpsim](./mpsim.md) · [data-access](../data-access.md) · [README](./README.md)
