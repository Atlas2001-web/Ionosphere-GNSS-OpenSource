# IonoMoni · 单站 STEC / ROTI / AATR 操作手册

目录：[`PROJECTS.json` → `IonoMoni`](../../PROJECTS.json) · 上游 <https://github.com/qiliu2025/IonoMoni> · C++17 / CMake · **GPLv3** · 文 <https://doi.org/10.1007/s10291-026-02059-z> · 手册对照仓内 `doc/IonoMoni_user_manual_v1.1.2.pdf` + `doc/IonoMoni.xml`（**v1.1.2**）

> 岗位：单站双频 → **STEC/VTEC、ROTI、AATR**。配置驱动（XML）。CLI：**`IonoMoni -x <xml>`**（见 `batch_process/.../run_cmd_IonoMoni_multi.py`）。不是硬件 S4，不是全球球谐求解器。键名以 PDF / 样例 XML 为准——本页不臆造未出现的键。

## 1. 用途与边界

**做：**

- STEC：载波到码 leveling（CCL；`<smoothing>` = `hatch` / `arc_mean`）或无差非组合 PPP（`PPP_STEC` / UCPPP）
- VTEC：映射函数（`<mapping_function>` 0=SLM … 5=Klobuchar，≥1.1.1）
- ROTI；AATR（磁暴/赤道/极区扰动常用）
- 多星座 GPS/BDS/Galileo/GLONASS；RINEX 2.x/3.x；`batch_process/`、`plot/` 辅助

**不做：** 硬件 S4；全球 GIM；深度 DCB/绝对 TEC 主力链（→ [pytecgg](./pytecgg.md)，**viventriglia**）；Python ROTI 脚本链主力（→ [oasis-roti](./oasis-roti.md)）。

一句话：**C++ 配置驱动单站监测**；与 OASIS **比趋势**。官方预编译主推 **Windows**；Linux 需自编译（CMake presets 当前条件为 Windows）。

## 2. 安装

README：**优先下 Releases 最新包**。Windows 预编译在 `bin/`；源码用 VS2022 + CMake preset（`Release with XML`）。

```bash
git clone https://github.com/qiliu2025/IonoMoni.git
cd IonoMoni
ls doc/ bin/ 2>/dev/null
ls doc/*.pdf doc/*.xml
# Windows（Releases 或本地编出后）：
#   IonoMoni.exe -x path\to\config.xml
# 源码构建（摘自手册）：VS2022 选 preset “Release with XML”，
# 把 build_resources/* 拷到 out/build/release-with-xml/，再生成 IonoMoni.exe
cmake --list-presets 2>/dev/null || true
```

绘图/批处理 Python（上游建议 3.13 + venv）：

```bash
python3 -m venv .venv && source .venv/bin/activate   # Win: py -3.13 -m venv .venv
pip install -r requirements.txt   # 以仓库文件为准
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| preset 不存在 / 全是 windows-* | 环境非 Win | 用 Releases `bin/`；Linux 跟 `CMakeLists.txt` 自迁 |
| 缺 DLL | 未带 `build_resources` | 用完整 Release 包；拷 DLL 到 exe 旁 |
| XML 解析怪 | CRLF / 标签坏 | `dos2unix config/*.xml`；回滚金样 |
| `command not found` | PATH | 把含 `IonoMoni.exe` 的目录加入 PATH |

**质检机说明：** 本轮 Linux 质检机**未**跑通官方 Windows 二进制；下列命令与键名来自仓内 XML / PDF / 批处理脚本真实内容，**不伪造** `IonoMoni` stdout。

## 3. 端到端：样例 XML → 产品时序

### 3.1 冻结金样配置

```bash
mkdir -p config logs result
cp doc/IonoMoni.xml config/ionomoni.xml
cp config/ionomoni.xml config/ionomoni.xml.ok
# 核对真实键（本机从 doc/IonoMoni.xml 抽出）：
grep -nE 'function|rinexo|rinexn|sp3|THREE_SP3|bias|rec>|sys>|smoothing|rec_dcb|roti_window|aatr|mapping_function|minimum_elev|ion_height|txt>' config/ionomoni.xml | head -n 60
```

**样例 `<gen>` / `<inputs>` / `<process>`（摘自 `doc/IonoMoni.xml`，路径需改成你的绝对路径）：**

```xml
<gen>
  <function>CCL_STEC  </function><!-- CCL_STEC | PPP_STEC | ROTI | AATR -->
  <beg> 2023-04-10 00:00:00 </beg>
  <end> 2023-04-10 23:59:30 </end>
  <int> 30 </int><!-- 手册：当前仅 30 s -->
  <sys> GPS </sys>
  <rec> HRAO CORD </rec><!-- 4 字大写站码 -->
  <est> FLT </est>
</gen>
<inputs>
  <rinexo> obs\....o </rinexo>
  <rinexn> gnss\BRDC....rnx </rinexn>
  <sp3> gnss\COD0MGXFIN_....SP3 </sp3>
  <THREE_SP3> <!-- CCL/ROTI/AATR：建议 昨/今/明 三天 SP3 -->
    ...D-1...SP3
    ...D0...SP3
    ...D+1...SP3
  </THREE_SP3>
  <bias> gnss\CAS0MGXRAP_....BSX </bias>
  <!-- PPP_STEC 另需 rinexc/atx/blq/de/eop 等，见手册 §8 -->
</inputs>
<outputs>
  <txt> .\result\$(function)\$(rec).txt </txt>
</outputs>
<process>
  <roti_window> 10 </roti_window>
  <rot_unit> min </rot_unit><!-- sec | min -->
  <aatr_interval> 120 </aatr_interval>
  <arc_min_length> 10 </arc_min_length>
  <ion_height> 350000 </ion_height><!-- 米 -->
  <mapping_function> 0 </mapping_function><!-- 0 SLM … 5 Klobuchar -->
  <minimum_elev> 7 </minimum_elev>
  <smoothing> arc_mean </smoothing><!-- arc_mean | hatch -->
  <rec_dcb_corr> true </rec_dcb_corr>
</process>
```

| 配置项 | 作用 | 错用后果 |
| --- | --- | --- |
| `<function>` | `CCL_STEC` / `PPP_STEC` / `ROTI` / `AATR` | 模式错 → 产物不对 |
| `<rinexo>` / `<rinexn>` / `<sp3>` / `<THREE_SP3>` | 输入覆盖 | `cannot open` / 空输出 |
| `<rec>` 站码 | 4 字大写 | 与 OBS MARKER 不一致 → 跳站 |
| `<smoothing>` | CCL：`hatch`≈近实时；`arc_mean`≈事后 | 噪声与时延不同 |
| `<rec_dcb_corr>` | 接收机 DCB（≥1.1.0） | 绝对值偏移 |
| `<roti_window>` / `<aatr_interval>` | 指数窗 | 改窗勿硬比文献 |
| `<mapping_function>` / `<ion_height>` | STEC→VTEC | 与 IPP 高声明不一致 |
| `<txt>` | 产品路径；可用 `$(function)` `$(rec)` | 相对路径踩 cwd |

**输入按模式（手册 §8）：**

| 模式 | 最少输入 |
| --- | --- |
| `CCL_STEC` | OBS + SP3/THREE_SP3 + DCB（`bias`） |
| `PPP_STEC` | OBS + NAV + SP3 + CLK + DCB + atx/blq/de/eop… |
| `ROTI` / `AATR` | OBS + 精密轨道（SP3/THREE_SP3） |

### 3.2 跑单站日

```bash
# Windows 例（路径按 Releases / 本地 build 调整）
IonoMoni.exe -x config\ionomoni.xml
# 或把 stdout 落盘（批处理脚本同款）：
# IonoMoni.exe -x "config\ionomoni.xml" > logs\run.cmd_log 2>&1

ls result/ 2>/dev/null || ls ./out/build/release-with-xml/result/ 2>/dev/null
# 期望：出现按站/系统命名的 STEC/ROT/ROTI 或 AATR 文本（矩阵或列表，见图 5.5.3/5.5.4）
# 成功日志特征（批处理样例 cmd_log）："Successfully read XML" → "IonoMoni program finished."
```

**期望：** `result/$(function)/` 下非空 `.txt`；日志无致命 cannot open。空输出 → 先查双频、时间窗、`<rec>`、截止角。

### 3.3 批处理

```bash
cd batch_process/PythonScripts
# 编辑 ../ini/run_IonoMoni.ini：function / site_path / IonoMoni 可执行路径 / 数据池路径
python run_cmd_IonoMoni_multi.py -year 2023 -beg 305 -end 306 -ini ../ini/run_IonoMoni.ini
# 产出：project/<function>/<YYYY>_<DOY>/ 下每日 XML + IonoMoni_result/
```

内部实际调用形如：`{IonoMoni} -x "{xmlPath}" > run_cmd_IonoMoni_*.cmd_log`。

### 3.4 绘图（可选）

`plot/`：`data_roti` / `data_ccl` / `data_aatr` / `data_ppp` → `output/`（名称以仓库为准）。把对应模式文本拷入后再跑 `plot/PythonScripts/`。

### 3.5 门禁与交叉验证

1. [anubis](./anubis.md) lite 通过再批跑。  
2. 绝对 TEC 形态 → [pytecgg](./pytecgg.md)。  
3. 同站日 [oasis-roti](./oasis-roti.md)：只比高值时段同向。  
4. 高 ROTI/AATR 窗 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) 固定率。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| RINEX OBS 2/3 | 双频；手册当前采样 **30 s** |
| NAV / SP3 / THREE_SP3 / bias… | 按模式表 |
| XML | 主控制面；`-x` 传入 |

| 输出 | 说明 |
| --- | --- |
| STEC / VTEC 文本 | 单站时序 ≠ GIM 栅格 |
| ROT / ROTI / AATR | 扰动指数 |
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
| 1 | 输出空 | 缺双频 / 空窗 / 截止角过高 / 站码错 | 查 OBS；放宽 `<minimum_elev>`；`<rec>` 对 MARKER |
| 2 | cmake 失败 | 预设仅 Windows | Releases `bin/`；或 VS2022 |
| 3 | AATR 离谱 | 错 SP3 / 日不匹配 | 用 `<THREE_SP3>` 昨今明；升级 ≥1.1.0 |
| 4 | 与 OASIS 量级差 | 窗口/周跳不同 | 比趋势；记录 `<roti_window>` |
| 5 | 当 S4 用 | 误解 | 称 ROTI/AATR；S4→ISMR |
| 6 | 站坐标/几何错 | IPP/映射错 | 填已知坐标；核 `<ion_height>` |
| 7 | 1 Hz 极慢/OOM | 数据量；手册主推 30 s | `gfzrnx -smp 30` |
| 8 | cron 相对路径 | cwd 漂移 | XML 内全部绝对路径 |
| 9 | 坏站未 QC | 缺口/MP | Anubis 门禁 |
| 10 | 改窗硬比文献 | 定义变 | 报告写窗口 |
| 11 | 单站 VTEC 当 GIM 发表 | 产品形态不同 | GIM→[ionex-gim](./ionex-gim.md) |
| 12 | 缺 DCB 仍进解 | 旧版行为 | 升 ≥1.0.0；查剔除逻辑 |
| 13 | XML 解析失败 | CRLF/标签坏 | `dos2unix`；回滚 `.ok` |
| 14 | 作者/许可与 OASIS 混淆 | 两项目独立 | IonoMoni GPLv3；OASIS CC BY-NC |
| 15 | `smoothing` 写成 `arc_average` | 键值是 **`arc_mean`** | 对照样例 XML |
| 16 | Linux 指望开箱二进制 | 官方主推 Win | Releases 或自编译 |
| 17 | PPP_STEC 缺 CLK/atx | 模式输入不全 | 按手册 §8 清单补齐 |
| 18 | 忘记 `-x` | CLI 未加载配置 | `IonoMoni -x config.xml` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| C++ 批监测 STEC+ROTI+AATR | **IonoMoni** |
| Python 链 ROTI/ΔTEC/SIDX | OASIS |
| 校准绝对 TEC | pytecgg（viventriglia） |
| 读 IGS GIM | ionex-gim |

## 8. 相关

[oasis-roti](./oasis-roti.md) · [pytecgg](./pytecgg.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [ionex-gim](./ionex-gim.md) · [iono-scintillation](./iono-scintillation.md) · [README](./README.md) · [data-access](../data-access.md)
