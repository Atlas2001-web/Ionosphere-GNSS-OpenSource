# 贡献指南 / Contributing

感谢关注 **Ionosphere-GNSS-OpenSource**！本仓库是**精选链接索引**，不是代码合集。

## 可贡献内容

- 新增真实存在的开源项目（须提供可访问的公开 URL）
- 修正描述、语言、许可证、分类错误
- 改进 README / 分类文档结构

## 请勿

- 提交未经核验或虚构的 GitHub URL
- 将大型第三方源码直接拷入本仓库
- 公开提及或链接私有仓库（例如专有/未开源版本）

## 提交流程建议

1. Fork 本仓库并新建分支
2. 在 `PROJECTS.json` 增加条目（字段：`name, url, desc_zh, desc_en, language, license, category, subcategory, user_relation`）
3. 同步更新对应 `lists/*.md` 与 `README.md` 表格
4. 在 PR 中说明如何核验该仓库存在（例如 GitHub 页面可打开）

## 分类约定

| category | 含义 |
|---|---|
| `ionosphere` | 电离层 / TEC / GIM / IRI / 闪烁 / 层析 |
| `gnss-data` | RINEX / SP3 / ANTEX / RTCM 等数据与格式 |
| `gnss-positioning` | PPP / RTK / PPP-RTK / POD |
| `navigation-ins` | IMU / INS / GNSS-INS / PNT |
| `tools-learning` | 可视化、分析、教育示例 |

`user_relation` 取值：`owned` | `forked` | `starred` | `none`
