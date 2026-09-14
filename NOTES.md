# NOTES — 编纂与核验说明

生成日期：2026-09-14  
目标仓库名：`Ionosphere-GNSS-OpenSource`

## 数据来源优先级

1. **用户自有**：Atlas2001-web/SH-GIM（旗舰）
2. **用户 Fork**：PyTECGg、georinex
3. **用户 GitHub Stars**（电离层 / GNSS / 导航三类）作为主种子
4. **社区知名项目**补充：Ginan、raPPPid、rtklibexplorer、gici-open、PyIRI、iri2016/2020、gnss-tec、tec-suite、NeQuick、GNSSNexus/rinex、pyins、GREAT-MSF、GPSPACE、gnssrefl、闪烁仿真器等

## 核验方法

- 早期批次：GitHub REST API `GET /repos/{owner}/{repo}`（获取 language / license / stars）
- 全量批次：对 `https://github.com/{owner}/{repo}` 做 HTTP HEAD，要求 **200**
- API 触发 403 限流后，不以“搜不到”为由删除已 HEAD 通过的星标项目
- **不收录**：虚构 URL、未确认存在的仓库、私有库（SH-GIM-proprietary）

## 刻意省略

- `SH-GIM-proprietary`：私有，不在公开 README / lists 中出现
- 未找到稳定公开源码镜像的专有工具（如部分商业 PPP 服务前端）
- teqc（已 EOL，官方分发不在 GitHub；未强行编造镜像）
- 官方 BNC：主要在 BKG SVN/FTP（`software.rtcm-ntrip.org`）；社区镜像存在但非唯一权威，本期未强制列入主表

## 分类计数（当前）

| category | count |
|---|---:|
| ionosphere | 29 |
| gnss-data | 6 |
| gnss-positioning | 10 |
| navigation-ins | 7 |
| tools-learning | 3 |
| **total** | **55** |

## 用户关系计数

- owned: 1（SH-GIM）
- forked: 2（PyTECGg, georinex）
- starred: 多数星标种子已纳入
- none: 社区补充项

## 后续可增强（未阻塞本期交付）

- 用未限流的 API token 回填全部 `language` / `license` / `stars`
- 增加 ANTEX/RTCM 专用读写库专题
- 增加 CSRS-PPP 在线服务说明（非源码）与 GPSPACE 编译笔记
- 可视化类可补充更多绘图/QC 工具（Anubis 官方页等非 GitHub 源）

## 文件清单

```
/workspace/ionosphere-gnss-catalog/
├── README.md
├── PROJECTS.json
├── NOTES.md
├── CONTRIBUTING.md
├── docs/categories.md
└── lists/01–05-*.md
```
