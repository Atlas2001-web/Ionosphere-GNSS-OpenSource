# IonoMoni · 单站 STEC/VTEC · ROTI · AATR（C++）

目录条目：[`PROJECTS.json` → `IonoMoni`](../../PROJECTS.json) · 上游 <https://github.com/qiliu2025/IonoMoni>  
列表：[01 电离层](../../lists/01-ionosphere.md) · 许可：GPLv3（以上游为准）  
请优先从仓库 **Releases** 下载与 `doc/` 用户手册版本一致的包。

## 作用与场景

面向**单站双频（多星座）**观测，用 XML 配置驱动计算：

- STEC（载波到伪距整平 CCL；也可走非差非组合 PPP 类路径）；
- VTEC（映射函数）；
- **ROTI**、**AATR** 等扰动 / 不规则体监测指标。

**何时用：** 台站日处理、空间天气个例、需要编译型性能与批处理。  
**何时不用：** 只想在 Python 里探活 RINEX → [georinex](./georinex.md)；只要 ROTI 脚本产线也可看 [oasis-roti](./oasis-roti.md)；全球球谐 GIM → [sh-gim](./sh-gim.md)（维护者自有，仅短述）或其他开源 GIM。

## 安装

1. **Windows：** Releases 常提供 `bin/` 可执行文件与依赖 DLL（VS2022 / Win64）。  
2. **从源码（CMake）：**

```bash
git clone https://github.com/qiliu2025/IonoMoni.git
cd IonoMoni
# 按 doc/ 手册与 CMakePresets.json 选择预设后：
cmake --preset <your-preset>
cmake --build build --config Release
```

3. 批处理 / 绘图脚本：建议独立 Python 虚拟环境，依赖见上游 `requirements.txt`。  
4. 配置样例：`doc/` 下 XML（文件名以当前 Release 手册为准）。

## 最小示例

逻辑最小流程（标签名以你使用的 XML / 手册为准）：

1. 准备某站一日 RINEX OBS（2.x/3.x）及手册要求的 SP3 / DCB / EOP 等。  
2. 复制样例 XML，改：输入路径、输出目录、启用模块（STEC / ROTI / AATR / VTEC 等）、截止高度角、平滑方式。  
3. 运行（可执行文件名以 Release 为准）：

```bash
./bin/IonoMoni path/to/your_config.xml
```

4. 用仓库 `plot/` 脚本或自写 pandas/matplotlib 画 STEC/ROTI 时序。

## 输入输出

| 方向 | 典型内容 |
|---|---|
| 输入 | 单站 RINEX OBS；精密轨道 SP3；DCB 等偏差产品（按模块）；XML |
| 输出 | STEC/VTEC、ROTI、AATR 等序列（格式见手册与 `plot/` 示例） |
| 中间 | 弧段划分、相位整平、穿刺点与映射 |

## 常见坑

1. **未读手册改 XML**：模块开关、平滑选项、接收机 DCB 开关直接影响数值。  
2. **脏观测当闪烁**：周跳、多路径会造成 ROTI 尖峰；先 QC（Anubis / GFZRNX / [georinex](./georinex.md)）。  
3. **SP3 / PRN 覆盖**：轨道必须覆盖处理弧段；用最新 Release。  
4. **缺 DCB**：弧段可能被剔除或系统偏差变大。  
5. **GPLv3**：嵌入闭源产线需合规评估。

## 接到哪一步分析

- 现象课：[05 闪烁与 ROTI](../tutorials/05-scintillation-roti.md)、[20 磁暴 TEC](../tutorials/20-storm-tec-analysis.md)。  
- 可编程 TEC 校准流水线（另一作者）：[pytecgg](./pytecgg.md)。  
- 高 ROTI 时段可与 [RTKLIB](./rtklib.md) 固定率/残差对照。  
- 产品侧 ROTI 图可视化小工具见目录 `igs-roti`（对照用，不替代本机从观测计算）。
