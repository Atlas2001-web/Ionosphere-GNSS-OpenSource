# IonoMoni · 单站 STEC / ROTI / AATR 操作手册

目录：[`PROJECTS.json` → `IonoMoni`](../../PROJECTS.json) · 上游 <https://github.com/qiliu2025/IonoMoni> · C++17 / CMake · **GPLv3** · 文 <https://doi.org/10.1007/s10291-026-02059-z>

> 岗位：单站双频 → **STEC/VTEC、ROTI、AATR** 时序与站日批处理。配置驱动（XML）。不是硬件 S4，不是全球球谐求解器。键名以包内 `doc/IonoMoni_user_manual_*.pdf` 与样例 XML 为准（本页不臆造未在手册出现的键）。

## 1. 用途与边界

**做：**

- STEC：载波到码 leveling（CCL；平滑 `hatch` / `arc_average`）或无差非组合 PPP（UCPPP）路径（以上游模块为准）
- VTEC：映射函数（含 Klobuchar 选项，视版本）
- ROTI；AATR（Along-Arc TEC Rate，磁暴/赤道/极区扰动常用）
- 多星座 GPS/BDS/Galileo/GLONASS；RINEX 2.x/3.x；`batch_process/`、`plot/` 辅助

**不做：** 硬件 S4；全球 GIM；深度 DCB/绝对 TEC 主力链（→ [pytecgg](./pytecgg.md)，**viventriglia**）；Python ROTI 脚本链主力（→ [oasis-roti](./oasis-roti.md)）。

一句话：**C++ 配置驱动单站监测**；与 OASIS **比趋势**。

## 2. 安装

README 提示优先下 **Releases** 最新包。Windows 预编译在 `bin/`；源码用 CMake presets / VS2022。

```bash
git clone https://github.com/qiliu2025/IonoMoni.git
cd IonoMoni
cmake --list-presets 2>/dev/null || true
# 例（名称以 CMakePresets.json 为准）：
# cmake --preset <preset> && cmake --build --preset <preset>
ls bin/ 2>/dev/null || find build -iname 'IonoMoni*' 2>/dev/null | head
./bin/IonoMoni -h 2>/dev/null || ./bin/IonoMoni 2>&1 | head -n 20
ls doc/
```

绘图/批处理 Python（上游建议 3.13 + venv）：

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # 以仓库文件为准
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| preset 不存在 | 环境与预设不符 | `--list-presets`；或只用 Releases `bin/` |
| 缺 DLL | 未带 `build_resources` | 用完整 Release 包 |
| XML 解析怪 | CRLF | `dos2unix config/*.xml` |
| Linux 编译卡 | 文档主推 Win 预编译 | 跟 `CMakeLists.txt` 补依赖 |

## 3. 端到端：样例 XML → 产品时序

### 3.1 冻结金样配置

```bash
mkdir -p config logs output
# 手册与样例：
ls doc/*.pdf doc/*.xml 2>/dev/null
cp doc/*.xml config/ 2>/dev/null || true
cp config/*.xml config/ionomoni.xml.ok
```

用编辑器改 **绝对路径**：OBS、NAV/SP3、站坐标、系统/频率、截止角、输出目录、STEC/ROTI/AATR 模块开关。改完：

```bash
grep -nE 'rinex|obs|nav|sp3|xyz|coord|elev|roti|aatr|stec|out|smooth|dcb|map' config/*.xml | head -n 80
```

| 配置项（示意，以手册/XML 为准） | 作用 | 错用后果 |
| --- | --- | --- |
| OBS/NAV 或 SP3 路径 | 输入覆盖 | `cannot open` / 空输出 |
| 测站 XYZ | IPP、高度角、映射 | 几何全错 |
| `<smoothing>` | CCL：`hatch`≈近实时；`arc_average`≈事后 | 噪声与时延不同 |
| `<rec_dcb_corr>` | 是否改正接收机 DCB（≥1.1.0） | 绝对值偏移 |
| ROTI/AATR 窗 | 常见 1 min | 改窗勿硬比文献 |
| 映射函数 | STEC→VTEC | 与 IPP 高度声明不一致 |
| 输出目录 | 产品落盘 | 权限/相对路径踩坑 |

### 3.2 跑单站日

```bash
./bin/IonoMoni config/my_site.xml 2>&1 | tee logs/ionomoni_run.log
# 若 CLI 形式不同，以 -h / PDF 为准
ls -la output/ | head
wc -l output/* 2>/dev/null | head
```

**期望：** 出现 stec/vtec/roti/aatr 类时序（确切文件名见手册）；日志无致命 `cannot open`。空输出 → 先查双频、时间覆盖、截止角。

### 3.3 绘图（可选）

`plot/` 约定输入子目录（名称以仓库为准），例如 `data_roti` / `data_ccl` / `data_aatr` / `data_ppp` → `output/`：

```bash
ls plot/PythonScripts/
# 按 README 把产品拷入对应 data_* 再调用脚本
```

### 3.4 批处理

```bash
for xml in config/sites/*.xml; do
  b=$(basename "$xml" .xml)
  ./bin/IonoMoni "$xml" 2>&1 | tee "logs/${b}.log" || echo FAIL "$xml" | tee -a logs/fail.list
done
test -f logs/fail.list && wc -l logs/fail.list
```

### 3.5 门禁与交叉验证

1. [anubis](./anubis.md) lite 通过再批跑。  
2. 绝对 TEC 形态 → [pytecgg](./pytecgg.md)。  
3. 同站日 [oasis-roti](./oasis-roti.md)：只比高值时段同向。  
4. 高 ROTI/AATR 窗 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) 固定率。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS 2/3 | 双频；星座按配置 |
| NAV / SP3 | 模块需要时必给；AATR 对 SP3 敏感 |
| EOP 等 | 见 `poleut1` / 手册 |
| XML | 主控制面 |

| 输出 | 说明 |
| --- | --- |
| STEC / VTEC | 单站时序 ≠ GIM 栅格 |
| ROTI / AATR | 扰动指数 |
| 日志 / 图 | 排错与展示 |

**明确不输出：** IONEX 全球图、硬件 S4、可发表级 DCB 产品（除非另接产品链）。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 B 扰动 | §3 | [05](../tutorials/05-scintillation-roti.md) · [20](../tutorials/20-storm-tec-analysis.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 与定位对照 | §3.5 | [06](../tutorials/06-iono-positioning.md) |
| 绝对 TEC | — | [pytecgg](./pytecgg.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 前门禁 | — | [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 输出空 | 缺双频 / 空窗 / 截止角过高 | `python -m georinex.time OBS`；放宽角；读日志 |
| 2 | cmake 失败 | 预设不匹配 | Releases `bin/`；或按 README 用 VS |
| 3 | AATR 离谱 | 错 SP3 / 日不匹配 | 同日 SP3；升级 ≥1.1.0 |
| 4 | 与 OASIS 量级差 | 窗口/周跳不同 | 比趋势；记录定义 |
| 5 | 当 S4 用 | 误解 | 称 ROTI/AATR；S4→ISMR |
| 6 | 站坐标错 | IPP/映射错 | 填已知坐标或 PPP 粗解 |
| 7 | 1 Hz 极慢/OOM | 数据量 | `gfzrnx -smp 30` |
| 8 | cron 相对路径 | cwd 漂移 | XML 内全部绝对路径 |
| 9 | 坏站未 QC | 缺口/MP | Anubis 门禁 |
| 10 | 改窗硬比文献 | 定义变 | 报告写窗口 |
| 11 | 单站 VTEC 当 GIM 发表 | 产品形态不同 | GIM→[ionex-gim](./ionex-gim.md) |
| 12 | 缺 DCB 仍进解 | 旧版行为 | 升 ≥1.0.0；查剔除逻辑 |
| 13 | 并行打满盘 | 多站同写 | 限并发 |
| 14 | GPST/UTC 混用 | 时间系 | 统一再对齐事件 |
| 15 | XML 解析失败 | CRLF/标签坏 | `dos2unix`；回滚 `.ok` |
| 16 | 作者/许可与 OASIS 混淆 | 两项目独立 | IonoMoni GPLv3；OASIS CC BY-NC |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| C++ 批监测 STEC+ROTI+AATR | **IonoMoni** |
| Python 链 ROTI/ΔTEC/SIDX | OASIS |
| 校准绝对 TEC | pytecgg（viventriglia） |
| 读 IGS GIM | ionex-gim |

## 8. 相关

[oasis-roti](./oasis-roti.md) · [pytecgg](./pytecgg.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [ionex-gim](./ionex-gim.md) · [iono-scintillation](./iono-scintillation.md) · [README](./README.md) · [data-access](../data-access.md)
