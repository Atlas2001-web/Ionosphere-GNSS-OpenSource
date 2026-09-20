# IonoMoni

目录：[`PROJECTS.json` → `IonoMoni`](../../PROJECTS.json) · 上游 <https://github.com/qiliu2025/IonoMoni>

## 用途

- C++ 单站电离层监测：从 RINEX 算 **STEC/VTEC、ROTI、AATR** 等。
- 适合磁暴/不规则体个例的时间序列与批量站日处理。
- **不是**硬件 S4/σφ；**不是**全球球谐 GIM 求解器。
- 与 OASIS：同属扰动指标；IonoMoni 偏 C++/配置驱动，OASIS 偏 Python 脚本链。

## 安装

```bash
git clone https://github.com/qiliu2025/IonoMoni.git
cd IonoMoni
# 按仓库 README 选择 preset（名称以仓库为准）
cmake --preset <your-preset>
cmake --build build --config Release
# 可执行文件常见于 build/ 或 bin/
./bin/IonoMoni -h 2>/dev/null || ls build bin
```

依赖：CMake、C++ 编译器；其它库以 README/`CMakeLists.txt` 为准。

## 快速上手

```bash
# 1) 复制并编辑 XML/配置（站坐标、观测路径、阈值、截止角、输出目录）
cp config/example.xml config/my_site.xml
# 编辑路径与站信息（示例路径不可直接用）

# 2) 运行
./bin/IonoMoni config/my_site.xml

# 3) 看输出（文件名以仓库为准）
ls output/
# 常见：stec/roti/aatr 时间序列或中间文件

# 4) 绘图（若提供 plot/）
# 按 plot/ 说明把结果放入指定目录后运行 Python 脚本
python plot/PythonScripts/plot_roti.py   # 名称以仓库实际为准
```

**预期：** 配置合法时写出 STEC/ROTI 等序列；缺 OBS/NAV 或路径错会在日志报错退出。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS（双频）；导航或精密星历（以配置为准）；XML 配置 |
| 输出 | STEC/VTEC、ROTI、AATR 等时序；日志；可选图 |
| 不做 | 校准绝对 TEC 的完整 DCB 产品替代（看配置能力）；全球 GIM |

## 常用参数

以 XML/配置项为准（名称随版本变）：

| 项 | 说明 |
|---|---|
| 观测/星历路径 | 必须存在且时间覆盖 |
| 测站坐标 | 错坐标 → IPP/高度角全错 |
| 截止高度角 | 过低噪声大；过高弧段少 |
| 系统/频率 | 与数据一致 |
| ROTI 窗口 | 常见 1 min；改窗口勿跨论文硬比 |
| 输出目录 | 绝对路径更稳 |

## 接到工作流哪一步

- 路径 B 核心；教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)
- 读盘探活：[georinex](./georinex.md)；QC：[anubis](./anubis.md)
- 绝对 TEC 对照：[pytecgg](./pytecgg.md)；第二套 ROTI：[oasis-roti](./oasis-roti.md)
- 高 ROTI 时段定位：[rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| cmake preset 找不到 | 列 `cmake --list-presets`；读 README |
| 输出空 | 检查双频、时间覆盖、截止角 |
| ROTI 与 OASIS 量级差 | 窗口/周跳策略不同；看趋势同向即可 |
| 当 S4 用 | 错；硬件闪烁看 ISMR 等 |
| 站坐标 WGS84 搞错 | 用头文件/日志坐标核对 |
| 1 Hz 太慢/太大 | 先 [gfzrnx](./gfzrnx.md) 抽稀再评估窗口 |

## 相关工具

[oasis-roti](./oasis-roti.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [iono-scintillation](./iono-scintillation.md)

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
