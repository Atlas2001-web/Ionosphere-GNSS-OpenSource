# NOTES — 编纂与核验说明

生成日期：2026-09-14  
条目数：**207**

## 来源

1. 既有 PROJECTS.json（55，电离层较完整）
2. research/seed_urls.json（282：awesome-gnss + Navigation-Learning）
3. 人工核验：GitHub API / 官方站点（VMF、RNXCMP、BNC、Anubis、EGNOS Toolkit）
4. 维护者 stars / forks（SH-GIM、PyTECGg、georinex）

## 过滤

- 不收录私有库与虚构 URL
- Navigation-Learning 中与 GNSS/PNT 无关的纯 SLAM/深度学习列表已过滤
- Fork 去重为上游 canonical URL，fork 关系写入 markers

## 分类计数

| category | count |
|---|---:|
| ionosphere | 37 |
| troposphere | 15 |
| gnss-data | 30 |
| gnss-positioning | 51 |
| orbit-clock | 2 |
| navigation-ins | 16 |
| gnss-sdr | 45 |
| mobile-apps | 4 |
| tools-learning | 10 |
| **total** | **210** |

## 稀疏领域

对流层独立 GitHub 项目偏少（标准码在 TU Wien）；轨道/钟差/DCB 多集成于大型套件，故不硬凑数量。

## 质量修订（2026-09-14）

- 重写 Navigation-Learning 模板分析 **59** 条；删除 404/非 GNSS **3** 条（CSolgaard/GNSS-IR、iliasam/gps_rf_frontend_sim、aipixel/GPS-Gaussian）
- 纠正 SupakunZ/GNSS_RTK → `gnss-positioning`；若干 SDR/INS 条目归入 `gnss-sdr` / `navigation-ins`
- 剔除全文复制粘贴的 README对照 / IGS交叉检查 结尾套话
- 当前条目：**207**

## 质量修订（2026-09-14）

- 重写 Navigation-Learning 模板分析 **59** 条；删除 404/非 GNSS **3** 条（CSolgaard/GNSS-IR、iliasam/gps_rf_frontend_sim、aipixel/GPS-Gaussian）
- 纠正 SupakunZ/GNSS_RTK → `gnss-positioning`；误放的 SDR/INS 条目分别归入 `gnss-sdr` / `navigation-ins`
- 剔除全文复制粘贴的 README对照 / IGS交叉检查 结尾套话
- 当前条目：**207**
