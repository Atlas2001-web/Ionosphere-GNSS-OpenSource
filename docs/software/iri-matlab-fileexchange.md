# IRI-MATLAB-FileExchange · MathWorks File Exchange IRI 封装操作手册

目录：[`PROJECTS.json` → `IRI-MATLAB-FileExchange`](../../PROJECTS.json) · File Exchange <https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model> · irimodel.org 明确列出的 **MATLAB version** 入口 · 作者 **Drew Compston** · 许可 **BSD-2-Clause**（旧版 zip 内 `license.txt`，见坑 9）· 页面标 **Version 2.0.0.0**（**30.4 KB**；2026-09-26 抓取已显示为 **2.0.0（31.5 KB）**）· 发布 **2019-12-07** · 本机核页 **2026-09-24 06:18 EDT**（WebFetch 可读；本机 `curl` 对该域 **HTTP 403**）· **无 MATLAB / 无 Octave → 未下载 zip、未跑 `iri2016`/`iritest.m`（禁止臆造 Ne/TEC）** · **质检复跑** 2026-09-24 06:24 EDT（WebFetch 再确认 **2.0.0.0**/30.4 KB/**7 Dec 2019**/hack+`curl`；本机 `curl` **403**/body **476** B；CCMC vitmo→`IRI~2012/`/`IRI~2016/` **200**；`IRI~2020/` **200**但 FE **无**对应函数；irimodel.org 文案 **MATLAB version → IRI-2012 and IRI-2016**；**无 matlab/octave**→**未臆造 Ne/TEC**；交叉 [iri-fortran](./iri-fortran.md)/[iri-2026-package](./iri-2026-package.md)/[iri-common-files](./iri-common-files.md)/[pyiri](./pyiri.md)/[iri2016](./iri2016.md)）

> **质检复跑通过（2026-09-26 06:07–06:09 EDT）**：许可核实。File Exchange 下载路径 `versions/1…15` 的 zip（1.0.0–1.14.0）都带 `license.txt`，内容是 BSD 2-Clause（© 2014 Drew Compston），已改坑 9 和目录行。2.0.0 的 zip 拿不到（16–60 全 404），页面 License 弹窗抓取为空，2.0.0 许可文本属于**环境受限**。另外：页面现在显示 2.0.0 / 31.5 KB；条目页 curl 仍 403（476 B），但旧版 zip 可以匿名 200 下载（已改 §3 第 1 步和坑 10）。仍无 MATLAB，未跑 iri2016。
>
> 岗位：讲清这条 **官方指向的 MATLAB 入口**实际在干什么、能跟到哪一代 IRI、以及和 Fortran 金标准 / COMMON_FILES / IRI-2026 的边界。冲突时：**File Exchange 页面说明 + irimodel.org 链接文案 > 本文**。本地金标准数字只引用 [iri-fortran](./iri-fortran.md)。

## 1. 用途与边界

**做：**

- 在已有 **MATLAB** 环境里，用提交物提供的 `iri2012` / `iri2016` 函数取 CCMC 在线 IRI 输出
- 快速对照气候态剖面（教学、粗扫参数），不想先编 Fortran 时的权宜入口
- 核对 irimodel.org 首页「MATLAB version」指向的就是本 File Exchange 条目（本机 2026-09-24 抓取 irimodel 首页：文案写 **IRI-2012 and IRI-2016**）

**不做：**

- **不是** 本地绑定官方 `.for` / 自带 `ccir%%.asc` → 那是 [iri-fortran](./iri-fortran.md) / [iri-2026-package](./iri-2026-package.md) / [iri-common-files](./iri-common-files.md)
- **不是** IRI-2020 / **IRI-2026** 的 MATLAB 发行 → 工作组最新 Fortran 仍在 irimodel；CCMC 另有 IRI-2020 在线页，**本提交物页面未宣称支持 2020/2026**
- **不是** 纯 Python → [pyiri](./pyiri.md) / [iri2016](./iri2016.md) / [pyglow](./pyglow.md)
- **不是** GNSS 定位引擎 → [gogps-matlab](./gogps-matlab.md)（同属 MATLAB 栈，问题域不同）
- 本页 **无** 本机 Ne/TEC 数字——质检机无 MATLAB

一句话：File Exchange #34863 = **用 `curl` 打 CCMC 网页的 MATLAB 薄封装（作者自称 hack）**；方便，但不是官方 Fortran 运行时。

| 术语 | 含义 |
| --- | --- |
| File ID **34863** | MathWorks File Exchange 条目号 |
| `iri2012` / `iri2016` | 提交物内两个入口函数（v2 去掉已失效的 iri2007） |
| CCMC VITMO / Instant Run | NASA CCMC 在线跑模型；旧 `…/iri20xx_vitmo.php` 现会跳到 `/models/IRI~20xx/` |
| `iritest.m` | 页面说明中的示例脚本（可配 `parfor`） |
| `curl` | 真请求走系统终端；Unix/macOS 常自带，Windows 需自备 `curl.exe` |

## 2. 它和官方 Fortran / COMMON_FILES / IRI-2026 的关系

| 构件 | 本 File Exchange | 官方路径 |
| --- | --- | --- |
| 物理内核 | **远程** CCMC 所托管的 IRI-2012 / IRI-2016 服务 | 本机 [iri-fortran](./iri-fortran.md) 编译 `irisub.for` 等 |
| CCIR/URSI 系数 | **不落盘**；跟远端服务版本走 | ≤2016 常另下 [iri-common-files](./iri-common-files.md)；2020+ 多已进版本 zip |
| INDICES（`apf107`/`ig_rz`） | 由远端维护；你 **看不见**本地指数文件 | 必须另下 [indices](https://irimodel.org/indices/)，见 [iri-2026-package](./iri-2026-package.md) |
| IRI-2026 | **页面未提供**对应函数 | [iri-2026-package](./iri-2026-package.md) + [iri-fortran](./iri-fortran.md) |
| 可复现论文金标准 | 弱（依赖网页、网络、远端默认开关） | 强：固定 zip sha + 指数 + `fort.7` |

作者在 File Exchange 上写明：这是 **hack**——通过操作系统终端的 `curl` 查询在线接口，**需要联网**，且 **偏慢**；并给出旧链接：

- `iri2012` → `https://ccmc.gsfc.nasa.gov/modelweb/models/iri2012_vitmo.php`
- `iri2016` → `https://ccmc.gsfc.nasa.gov/modelweb/models/iri2016_vitmo.php`

本机 2026-09-24 探测：上述 PHP 地址 **HTTP 200**，但 **最终落地**为 CCMC 新站：

- `…/models/IRI~2012/`（仍见 Instant Run）
- `…/models/IRI~2016/`
- 另有 `…/models/IRI~2020/`（**本提交物无对应函数**）

因此：**“能打开 CCMC 页”≠“v2.0.0.0 的 curl 解析逻辑仍匹配旧 HTML”**。升级 IRI 物理请换官方 Fortran 包，不要指望本条目 magically 变成 2026。

### 2.1 兄弟手册怎么选

| 你要… | 打开 |
| --- | --- |
| 本机 gfortran → `fort.7` 金标准 | [iri-fortran](./iri-fortran.md) |
| 核 IRI-2026.zip 里有什么 | [iri-2026-package](./iri-2026-package.md) |
| ≤2016 外置 CCIR/URSI | [iri-common-files](./iri-common-files.md) |
| pip / xarray 绑 IRI-2016 Fortran | [iri2016](./iri2016.md) |
| 纯 Python、无 Fortran | [pyiri](./pyiri.md) |
| MATLAB 里做 PPP/NET（不是 IRI） | [gogps-matlab](./gogps-matlab.md) |
| 只有 MATLAB + 接受联网慢查 | **本页** |

## 3. 获取（诚实：本机未落盘）

1. 打开 File Exchange 条目 → **Download**。旧版 zip 本机可以匿名下载：`curl -A 'Mozilla/5.0' https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/34863/versions/15/download/zip` → 200，29565 B，内容是 1.14.0 的 `iri2007.m`/`iri2012.m`/`ecef2geod.m`/`iritest.m`/`license.txt`。2.0.0 的 zip 这个路径拿不到，请用浏览器下载。
2. 解压到 MATLAB 路径可及的目录；把该目录 `addpath`（或放进已有工具箱路径）。
3. 确认系统能跑 `curl`（Windows：按页面建议自装并把 `curl.exe` 放同目录或 PATH）。
4. 按包内 `iritest.m` / 函数头注释改经纬、高度、时间、扫参。

```bash
# 本机（无 MATLAB）只能核「入口页是否可被非浏览器抓取」：
curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' -A 'Mozilla/5.0' -L \
  'https://www.mathworks.com/matlabcentral/fileexchange/34863-international-reference-ionosphere-iri-model'
# 期望（本机 2026-09-24；质检复跑 06:24 EDT）：403 … body≈476 B Access Denied（CDN/反爬；浏览器或 WebFetch 仍可读页面元数据）

# CCMC 旧 vitmo → 新模型页（本机；质检复跑同）：
curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' -A 'Mozilla/5.0' -L \
  'https://ccmc.gsfc.nasa.gov/modelweb/models/iri2016_vitmo.php'
# 期望：200 https://ccmc.gsfc.nasa.gov/models/IRI~2016/
# 对照：iri2012_vitmo.php → …/IRI~2012/ ；另有 …/IRI~2020/（本 FE 无函数）
```

**无 MATLAB 时的替代（本机已短硬）：**

```bash
# 官方 Fortran 金标准（有数字）→ 见 iri-fortran.md
# 纯 Python 气候态 → pip / clone PyIRI，见 pyiri.md
# IRI-2016 xarray 驱动 → iri2016.md
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 质检机无 `matlab` | 环境受限 | 改走 [iri-fortran](./iri-fortran.md)/[pyiri](./pyiri.md)；**勿编造** File Exchange stdout |
| File Exchange `curl` 403 | 站点反爬 / 需登录会话 | 用浏览器下载；自动化另寻官方 zip |
| Windows 报找不到 curl | 未装 / 不在 PATH | 按页面装 curl，或与 `.m` 同目录 |
| `parfor` 很慢 | 每次调用都打网页 | 作者自述 dual-core 上 `iri2012` 约数分钟量级；减网格或改本地 Fortran |
| 想复现 IRI-2026 论文开关 | 本包装停在 2016 在线代 | 换 [iri-2026-package](./iri-2026-package.md) |

## 4. 页面事实清单（抓取，非 README 抄写）

本机 WebFetch（2026-09-24；质检复跑 06:24 EDT 再读一致）可见：

| 项 | 值 |
| --- | --- |
| 标题 | International Reference Ionosphere (IRI) Model |
| 版本 | **2.0.0.0**（30.4 KB）；2026-09-26 抓取显示 **2.0.0（31.5 KB）**，页面版本表共 14 个版本（1.0.0 2012-01-31 → 2.0.0 2019-12-07） |
| 发布 | **7 Dec 2019** |
| 兼容 | “Compatible with any release”；Win / macOS / Linux |
| 依赖 | MATLAB；`curl`（Windows 另下） |
| v2 变更摘要 | 移除 iri2007；更新 iri2012 适配新站；**新增 iri2016** |
| 示例 | `iritest.m`；可选 File Exchange **32101**（`parfor_progress`） |
| 启发条目 | 页面 Acknowledgements 指向 MSIS-E-00 等（非本手册范围） |

**不要**把 “Compatible with any release” 理解成 “永远兼容 CCMC 前端”——MATLAB 版本兼容 ≠ HTML 刮取稳定。

## 5. 接到哪一步

| 下一步 | 手册 |
| --- | --- |
| 需要可引用的本地 Ne/TEC | [iri-fortran](./iri-fortran.md) |
| 脚本化 Python 气候态 | [pyiri](./pyiri.md) / [iri2016](./iri2016.md) |
| 对照 GIM / 实测 TEC | [ionex-gim](./ionex-gim.md) / [pytecgg](./pytecgg.md) |
| MATLAB 定位实验 | [gogps-matlab](./gogps-matlab.md) |
| 概念 | 教程 [04](../tutorials/04-iri-nequick.md) |

## 6. 坑（≥10）

1. **名称像本地模型，实则联网刮网页**——断网即废；批量网格会打爆远端并极慢。
2. **不是 IRI-2026**——irimodel 文案与 File Exchange 均停在 2012/2016 表述；新物理去官方 zip。
3. **与 COMMON_FILES 无关**——你不会得到一份可 `cmp` 的 `ccir11.asc`；别把本包装当系数分发渠道。
4. **与 IRI-2026.zip 字节无关**——不能用来校验 [iri-2026-package](./iri-2026-package.md) 的 sha256。
5. **旧 `*_vitmo.php` 已跳转新前端**——v2（2019）解析逻辑可能已与 2026 年 HTML 不匹配；先单点试 `iri2016`，失败勿盲扫。
6. **CCMC 有 IRI-2020 页 ≠ 本函数能跑 2020**——缺第三方补丁就不要自称 2020/2026。
7. **Windows 缺 curl**——页面已写明；装错架构的 `curl.exe` 会静默失败。
8. **结果随远端默认开关**——论文复现应对齐 [iri-fortran](./iri-fortran.md) 的 `JF(50)` / 指数文件，而不是一次网页输出。
9. **许可是 BSD-2-Clause**（2026-09-26 质检核实）。版本 1–15（1.0.0 到 1.14.0）的 zip 都自带 `license.txt`（1313 B）：`Copyright (c) 2014, Drew Compston`，两条再分发条款加免责声明，是标准 BSD 2-Clause 文本；PROJECTS 条目现在也写的是 `BSD-2-Clause`。2.0.0（2019）的 zip 用同一下载路径拿不到（`versions/16…60` 都是 404），File Exchange 页的 “View License” 弹窗在抓取结果里是空的，所以 **2.0.0 的 `license.txt` 本机没亲眼看到**。再分发时保留版权声明和免责声明。
10. **本机 MathWorks 条目页 403**——质检复跑仍是 **403**/476 B。但 `mlc-downloads/…/versions/N/download/zip` 对旧版本匿名返回 200（N=1–4、6、8–15；5、7 返回 401）。拿不到的是 2.0.0，要人工用浏览器下载。
11. **与 [iri2016](./iri2016.md)（space-physics）不是同一个包装**——后者走本地 Fortran；本条走 CCMC HTTP。
12. **Octave 非官方目标**——作者写的是 MATLAB + 系统 curl；Octave 差异自行承担，本文不保证。

## 7. 选型

| 场景 | 选 |
| --- | --- |
| 已有 MATLAB，偶发查气候态，可接受慢与联网 | 本 File Exchange |
| 论文 / 金标准 / 离线 | [iri-fortran](./iri-fortran.md) + [iri-2026-package](./iri-2026-package.md) |
| Python 流水线 | [pyiri](./pyiri.md) 或 [iri2016](./iri2016.md) |
| MATLAB 做 GNSS 定位 | [gogps-matlab](./gogps-matlab.md)（别和 IRI 封装混为一谈） |

