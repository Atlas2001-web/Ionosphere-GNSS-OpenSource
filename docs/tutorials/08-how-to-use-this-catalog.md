# 08 · 怎么按研究问题在本仓库找软件

本仓库是**链接索引**：读 list → 点上游 URL → 克隆遵守其许可证。不要把第三方源码拷进本仓。

下面按「你要干什么」指路。标记含义见根 [`README.md`](../../README.md)。

---

## 总流程（每次都适用）

1. 用一句话写清问题（例：「从 RINEX 估 STEC 并画 ROTI」）。  
2. 打开 [`docs/categories.md`](../categories.md) 确认类别。  
3. 打开对应 `lists/*.md`，按**子类**扫表，读「详细中文分析」。  
4. 需要数据时看 [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) + [`docs/data-access.md`](../data-access.md)。  
5. 机器检索：`PROJECTS.json` 里搜 `name` / `subcategory` / `category`。

---

## 场景 A：想估 TEC（RINEX → STEC/VTEC）

| 步骤 | 去哪 |
|---|---|
| 概念 | [01](./01-ionosphere-tec-basics.md)、[02](./02-gnss-dualfreq-tec.md) |
| 软件 | [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) → 子类 **TEC 估计**（如 `gnss-tec`、`tec-suite`、`pygnss-tec`、`Seemala-GPS-TEC`） |
| 读 RINEX / QC | [`lists/03-gnss-data.md`](../../lists/03-gnss-data.md)（`georinex`、`TEQC`…） |
| 观测数据 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)（CDDIS 等） |

---

## 场景 B：想读 / 画 IONEX（GIM 产品）

| 步骤 | 去哪 |
|---|---|
| 概念 | [03-gim-ionex.md](./03-gim-ionex.md) |
| 读图软件 | `01-ionosphere` → **IONEX/TEC 图**（`ionex`、`ionex-rs`、`ionex_reader`…） |
| 自己建图 | 同列表 → **GIM / GIM/球谐映射**（`mosgim` 等；`SH-GIM` 仅 🚩 点名） |
| 下载产品 | `10-gnss-datasets` → `CDDIS-IONEX`、`JPL-IONEX-Rapid` 等；说明见 [`data-access.md`](../data-access.md) |

---

## 场景 C：想跑 IRI / NeQuick / NeQuick-G

| 步骤 | 去哪 |
|---|---|
| 概念 | [04-iri-nequick.md](./04-iri-nequick.md) |
| 软件 | `01-ionosphere` → **IRI 模型 / IRI/NeQuick / NeQuick-G 官方**（`IRI-Fortran`、`IRI-2026-package`、`PyIRI`、`iri2020`、`NeQuick2-ICTP`、`Galileo-NeQuick-G`…） |
| 注意 | IRI 常需 COMMON 系数与指数文件，条目里会写 |

---

## 场景 D：想下 GNSS / 电离层数据

| 步骤 | 去哪 |
|---|---|
| 门户与注册 | [`docs/data-access.md`](../data-access.md) |
| 条目表 | [`lists/10-gnss-datasets.md`](../../lists/10-gnss-datasets.md) |
| 例 | 观测/产品：`CDDIS-GNSS-Archive`；GIM：`CDDIS-IONEX`；掩星：`COSMIC-CDAAC`；测高：`GIRO-DIDBase` |

---

## 场景 E：想看闪烁 / ROTI

| 步骤 | 去哪 |
|---|---|
| 概念 | [05-scintillation-roti.md](./05-scintillation-roti.md) |
| 软件 | `01-ionosphere` → **闪烁**、**闪烁/ROTI**（`igs-roti`、`Okoh-MATLAB-ROT-ROTI`、`gnss-scintillation-simulator`、`scintill-ai`、`BiScEF`…） |
| 若需先有 TEC | 先走场景 A |

---

## 场景 F：定位里处理电离层

| 步骤 | 去哪 |
|---|---|
| 概念 | [06-iono-positioning.md](./06-iono-positioning.md) |
| 定位套件 | [`lists/04-gnss-positioning.md`](../../lists/04-gnss-positioning.md)（`RTKLIB`、`gLAB-UPC`、`PRIDE-PPPAR`、`ginan`…） |
| 单频模型源码 | `01-ionosphere` 中 Klobuchar / NeQuick-G 相关条目 |

---

## 场景 G：测高仪或掩星

见 [07](./07-ionosonde-occultation.md)：软件偏 `01-ionosphere`，数据偏 `10-gnss-datasets`。

---

## 别踩的坑

1. **索引仓 ≠ 代码合集** — 只保留核对过的链接。  
2. **🚩 维护者自有** — 只收录、不写长分析（如 `SH-GIM`）。  
3. **同名不同源** — 以 `PROJECTS.json` 的 `url` 为准。  
4. **先数据后软件** — 没 RINEX/IONEX，再好的 TEC 程序也空转。

---

## 延伸阅读（本仓库）

- 本系列目录：[README.md](./README.md)
- [`docs/categories.md`](../categories.md)
- [`docs/data-access.md`](../data-access.md)
- [`lists/01-ionosphere.md`](../../lists/01-ionosphere.md) · [`03-gnss-data.md`](../../lists/03-gnss-data.md) · [`04-gnss-positioning.md`](../../lists/04-gnss-positioning.md) · [`10-gnss-datasets.md`](../../lists/10-gnss-datasets.md)
- [`PROJECTS.json`](../../PROJECTS.json)
