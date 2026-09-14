# 分类规划 / Category Plan

生成日期：2026-09-14  
目标：在电离层之外覆盖对流层、数据格式、精密定位、轨道钟差、组合导航、SDR、移动端与学习资源。  
数据来源：`PROJECTS.json` 初稿（55） + `research/seed_urls.json`（282） + 人工核验（awesome-gnss / TU Wien VMF / RNXCMP / BNC / Anubis）。

## 分类树与实际数量

| slug | 中文名 | 目标 | 实际 | 说明 |
|---|---|---:|---:|---|
| ionosphere | 电离层 | 30–45 | 37 | GIM/TEC/IRI/NeQuick/闪烁/层析/IONEX；含旗舰 SH-GIM |
| troposphere | 对流层 | 6–15 | 13 | ZTD/ZWD/VMF/GPT/PWV/GNSS-IR；含 TU Wien 官方 codes |
| gnss-data | GNSS 数据 I/O | 20–35 | 31 | RINEX/SP3/RTCM/NTRIP/Hatanaka/QC/下载 |
| gnss-positioning | 精密定位 | 25–45 | 30 | SPP/RTK/PPP/PPP-AR/因子图 |
| orbit-clock | 轨道与钟差 | 3–10 | 2 | 独立小库稀少（见下） |
| navigation-ins | 导航 / GNSS-INS | 15–30 | 27 | 松紧组合、FGO、GNSS-视觉-惯性 |
| gnss-sdr | 软件接收机 | 10–25 | 48 | GNSS-SDR、SoftGNSS、信号仿真（种子较多） |
| mobile-apps | 移动应用 | 4–10 | 8 | GPSTest、Logger、Compare 等 |
| tools-learning | 学习资源 | 8–15 | 11 | awesome、Navigation-Learning、数据集、SBAS |

**合计：207**（目标区间 150–220）

## 领域稀疏说明

- **对流层**：映射函数与 GPT 官方实现在 https://vmf.geo.tuwien.ac.at/codes/ ，GitHub 上「从 RINEX 到 ZTD」完整开源明显少于电离层/PPP。已收 STD_SWD_Calc、UNB3m、GGOS-Tropo、PW_from_GPS、gnssrefl、PyAPS、ICAMS。
- **轨道/钟差/DCB（稀疏）**：精密轨道、钟差与 UPD/OSB 能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件内部，独立小库少，故 `orbit-clock` 类刻意保持精简、不注水。
- **SBAS**：EGNOS Toolkit 在 SourceForge；其余能力常在接收机/SDR 内，暂挂 tools-learning。
- **Navigation-Learning**：原列表含大量纯 SLAM/深度学习条目，已按 GNSS/PNT 关键词过滤。

## 标记约定

- `owned`：Atlas2001-web/SH-GIM
- `fork`：PyTECGg、georinex（表中列上游）
- `starred`：维护者星标种子
- `core`：建议优先阅读

## 交付文件

- `research/expanded_projects.json` — 机器可读扩充表
- `research/category_plan.md` — 本文件
- `PROJECTS.json` / `README.md` / `lists/01–09-*.md` / `docs/categories.md`
