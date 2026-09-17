# 15 · 从论文到开源：别只收藏 PDF

> 前置：[08 用目录](./08-how-to-use-this-catalog.md) · [17 路线图](./17-roadmap-beginner-to-expert.md)

---

## 落地四问（读任何电离层方法论文）

1. **观测是什么？** RINEX / IONEX / 测高仪 / 掩星 / 闪烁接收机 / 卫星原位？  
2. **算法核心开源吗？** GitHub、GitLab、Zenodo、机构页？还是「可应要求提供」？  
3. **评价能否用公开 IGS 站复现？**  
4. **本仓库有没有同任务替代品？** 打开 [`PROJECTS.json`](../../PROJECTS.json) 或 `lists/01-ionosphere.md` 搜关键词。

---

## 推荐动作顺序

```
读数据与方法节
  → 在 lists/ 搜 TEC、IONEX、ROTI、IRI、tomography…
  → 克隆上游最小例子 / 读 README 算例
  → 先复现「量级与形态」，再追小数点
  → 笔记本记录：论文设定 vs 你用的开源差异
```

---

## 常见坑

| 坑 | 怎么绕 |
|---|---|
| 数据不公开 | 换 IGS 公开站做「同类实验」，不硬称完全复现 |
| 仓库只有画图脚本 | 回头用 `gnss-tec` / `ionex` 补齐前端 |
| 把 ML 预报当物理同化 | 看输入特征与是否泄漏 |
| 忽略 DCB/映射 | 先读 [09](./09-dcb-biases-deep.md) |

维护者自有如 `SH-GIM`：目录只收录链接；学习球谐 GIM 时优先对照公开 IGS 产品与通用库。

## 下一课

[16 一日实战](./16-practice-one-day-tec.md) 把「能找工具」变成「今天出图」。
