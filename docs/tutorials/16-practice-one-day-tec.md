# 16 · 一日实战：从下载到一张 TEC 图

目标：用**公开数据 + 目录内工具**，当天跑通最小闭环。

## 路线 A（最快）：只读 GIM

1. 在 [`docs/data-access.md`](../data-access.md) / `CDDIS-IONEX` 说明下拿到某日 IONEX。
2. 用 `ionex` 或列表中的 IONEX 读取库加载。
3. 画出全球或中国区 VTEC 填色图 + 色标（TECU）。
4. 再读相邻两小时，看日变化是否「东边升起」。

成功标准：图上看得出赤道异常双峰或中纬日变，而不是噪声雪花。

## 路线 B（进阶）：单站 STEC

1. 下载某 IGS 站一天 RINEX（观测 + 导航）。
2. 用 `gnss-tec`（或同类）估各卫星 STEC 时间序列。
3. 处理周跳与高度角截止；讨论是否应用 DCB（见 09）。
4. 把穿刺点 VTEC 与同时刻 IGS GIM 插值比较。

成功标准：能解释「为什么和 GIM 差一截常数 / 低高度角更散」。

## 路线 C（选做）：扰动对照

选一个已知空间天气日，对路线 A 做安静日差分（见 14）。

## 工具索引

| 步骤 | 去哪 |
|---|---|
| 找软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) |
| 找数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 注册下载 | [`docs/data-access.md`](../data-access.md) |
| 不会选工具 | [08](./08-how-to-use-this-catalog.md) |

## 延伸阅读

- [10 GIM 流水线](./10-build-gim-workflow.md) · [17 路线图](./17-roadmap-beginner-to-expert.md)
