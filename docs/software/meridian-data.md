# 子午工程数据中心（Chinese Meridian Project）· 访问侧 操作手册

入口：[门户](https://www.meridianproject.ac.cn/) · [数据清单及 DOI `/sjj/`](https://www.meridianproject.ac.cn/sjj/) · [数据政策 `/sjzc/`](https://www.meridianproject.ac.cn/sjzc/) · [数据检索 SPA](https://dcstatus.meridianproject.ac.cn/#/sjfw/sjjs?checkLogin=true&lang=cn) · 本机验证 **2026-09-26 03:42–04:00 EDT**，**全程无账号**：没有注册，没有提交任何表单或离线申请，没有下载数据文件。只用了 curl 和系统 Python 3 标准库。唯一下载的是 3 份官方公开的格式说明 PDF，看完即删。

> 岗位：搞清楚子午工程**有哪些数据集（DOI / CSTR）**、**不登录能查到什么**（元数据、文件清单、格式说明）、**哪些必须登录**，以及发表时**怎么致谢和报送**。登录后的真实下载、文件内容解析和批量申请，本文**都没测**。  
> 门槛总表：[data-access 决策表](../data-access.md#电离层与地磁门户决策表) · [E4 子午工程](../data-access.md#dp-e4)。  
> 冲突时：**数据政策原文、格式说明 PDF 与登录后的实际界面 > 本文**。

## 1. 它解决什么，边界在哪

| 层 | 地址 | 不登录（实测） | 本文定位 |
| --- | --- | --- | --- |
| DOI 总表 | `www.meridianproject.ac.cn/sjj/` | ✅ 静态 HTML 表：**1161 个 DOI**（序号、DOI、CSTR、中英文名） | 解析、计数、查 DOI（3.1） |
| DOI 落地页 | `doi.org/10.12176/…` → `vsso.nssdc.ac.cn`（国家空间科学数据中心） | ✅ 页面 + JSON 元数据（时段、体量、许可证、致谢语） | 3.2 |
| 数据检索 SPA | `dcstatus.meridianproject.ac.cn/apis/…` | ✅ 检索、详情、**文件名清单**、格式说明 PDF 链接；❌ 下载与权限相关接口返回 401 | 3.3 |
| 账号 / SSO | `soc.meridianproject.ac.cn/sso/…` | 只看了公开页面，**没有注册** | 3.4 |
| 下载 / 批量（离线服务） | SPA「批量下载」`#/sjfwofflineserviceapply` | ❌ 需要登录；流程只按公开的前端文案描述 | 3.5 |

**不覆盖**：CMONOC 陆态网、地震局台网（门户和账号体系都不同）；cDST 指数和空间天气预报栏目。

## 2. 安装

```bash
curl --version | head -1; python3 -c "import json, re, html, urllib.request; print('ok')"
# 可选：看格式说明 PDF
pdftotext -v 2>&1 | head -1     # poppler-utils
```

## 3. 真实命令与输出

### 3.1 DOI 总表 `/sjj/`：解析与计数（`sjj_parse.py`）

```bash
curl -s -A Mozilla/5.0 https://www.meridianproject.ac.cn/sjj/ -o sjj.html     # 200，336,410 B
```

```python
import re, html, sys, json, collections as C
t = open(sys.argv[1], encoding='utf-8').read()
rows = []
for n, rest in re.findall(r'<tr><td>(\d+)</td>(.*?)</tr>', t, re.S):
    c = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<td>(.*?)</td>', rest, re.S)]
    rows.append(dict(no=int(n), doi=c[0], cstr=c[1], zh=c[2], en=c[3]))
INST = r'(.*?(?:阵列式大口径激光雷达|圆环阵太阳射电成像望远镜|仪|雷达|望远镜|接收机))(\d*)(.*)'
for r in rows:
    r['station'], s = r['zh'].split('站', 1)          # 中文名一律是「台站名 + 站 + 设备 + [01/02] + 产品」
    m = re.match(INST, s)
    r['inst'], r['unit'], r['product'] = (m.group(1), m.group(2), m.group(3)) if m else ('?', '', s)
    r['cls'] = r['doi'].split('/')[1][:5]
print('rows', len(rows), 'unique DOI', len({r['doi'] for r in rows}),
      'no-English', sum(not r['en'] for r in rows), 'unparsed', sum(r['inst'] == '?' for r in rows))
print('row-number dup', [k for k, v in C.Counter(r['no'] for r in rows).items() if v > 1],
      'cstr==14804.11.+doi-suffix', all(r['cstr'] == 'CSTR:14804.11.' + r['doi'].split('/')[1] for r in rows))
print('DOI class', sorted(C.Counter(r['cls'] for r in rows).items()))
print('stations', len({r['station'] for r in rows}), 'instrument types', len({r['inst'] for r in rows}))
print('top instruments', C.Counter(r['inst'] for r in rows).most_common(12))
print('top stations', C.Counter(r['station'] for r in rows).most_common(12))
json.dump(rows, open('sjj.json', 'w'), ensure_ascii=False, indent=0)
```

```text
rows 1161 unique DOI 1161 no-English 77 unparsed 0
row-number dup [870] cstr==14804.11.+doi-suffix True
DOI class [('01.01', 63), ('01.02', 13), ('01.05', 352), ('01.06', 483), ('01.07', 6), ('01.08', 2), ('01.09', 242)]
stations 97 instrument types 54
top instruments [('GNSS电离层TEC与闪烁监测仪', 228), ('电离层数字测高仪', 115), ('双通道全天空气辉成像仪', 104), ('磁通门磁力仪', 87), ('流星雷达', 72), ('中纬高频雷达', 54), ('高频多普勒监测仪', 48), ('双通道光学干涉仪', 48), ('Overhauser磁力仪', 31), ('大气电场仪', 28), ('感应式磁力仪', 28), ('中高层风温激光雷达', 20)]
top stations [('漠河', 79), ('儋州', 47), ('榆中', 44), ('四子王', 42), ('武汉黄陂', 31), ('大理宾川', 30), ('伽师', 30), ('桂林叠彩', 30), ('那曲色尼', 30), ('威海文登', 30), ('和静', 30), ('昌平十三陵', 27)]
```

**DOI 与 CSTR 的对应**：CSTR = `CSTR:14804.11.` + DOI 后缀，1161 条全部成立。例如 `10.12176/01.06.00538-V01` ↔ `CSTR:14804.11.01.06.00538-V01`。版本号全是 `-V01`。

**DOI 中段 `01.0X` 的含义**：01.06 经落地页元数据确认是「空间物理与空间环境>电离层」（`themCategoryTwo=01.06`）。其余按数据集名称归纳如下，**非官方定义**：01.01 太阳、01.02 行星际闪烁、01.05 中高层大气（气辉 / 激光雷达 / 流星雷达）、01.07 极光、01.08 缪子、01.09 地磁与地电场。

**电离层相关的两大类**：
- **GNSS TEC 与闪烁监测仪**：228 个 DOI，覆盖 36 个台站，6 种产品各 38 个（有的台站有 01 / 02 两台）。产品是 RINEX 观测参数、RINEX 星历、导航信号观测参数、垂直绝对 TEC、闪烁指数、斜向相对 TEC。
- **数字测高仪**：115 个 DOI，覆盖 19 个台站。产品是参数、频高图、频高图图片、漂移频谱、漂移速度、多通道 IQ。

查某个站的 DOI：

```bash
python3 -c "import json;[print(r['doi'],r['cstr'],r['zh']) for r in json.load(open('sjj.json')) if r['station']=='武汉黄陂' and '测高' in r['inst']]"
# 10.12176/01.06.00535-V01 … 多通道IQ记录 / 00536 频高图 / 00537 频高图图片 / 00538 电离层参数 / 00539 漂移观测频谱 / 00540 漂移速度
```

### 3.2 DOI 解析：落到国家空间科学数据中心，不是子午工程门户

```bash
curl -sI https://doi.org/10.12176/01.06.00538-V01 | grep -iE '^HTTP|^location'
#  HTTP/2 302
#  location: https://vsso.nssdc.ac.cn/nssdc_zh/html/vssoinfo.html?15539
curl -s https://doi.org/ra/10.12176                          # [{"DOI":"10.12176","RA":"ISTIC"}]
curl -sL -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.12176/01.06.00538-V01
#  200：title「武汉黄陂站电离层数字测高仪电离层参数」，type dataset，publisher「国家空间科学数据中心」，author「中国科学院地质与地球物理研究所」，issued 2026
curl -s -A Mozilla/5.0 "https://vsso.nssdc.ac.cn/nssdc/coreMetadata/getDetail?linkId=15539"    # 落地页自己调用的 JSON，200，5,751 B
```

`getDetail` 返回的关键字段（节选）：

```text
license CC BY-NC-ND 4.0 · sharePlan 即时公开 · shareMathod 线上共享 · shareScope 完全共享
timeSpanBegin 2024-07-19 · timeSpanEnd 2026-03-06 · datasetTotalSize 765460480 · releaseDate 2026-03-18
observatoryCh 武汉黄陂站（desCh 里写有台站编码 OWHHP，坐标 114.45, 31.02）
url https://dcstatus.meridianproject.ac.cn/#/recentBrowsing?id=21226      ← 真正的数据入口（SPA 数据集 id）
acknowledgementChDesc 感谢国家科技基础条件平台-国家空间科学数据中心(https://www.nssdc.ac.cn)提供数据资源。本项成果使用国家重大科技基础设施子午工程科学数据。
```

**抽样**：每隔 25 条取 1 个，共 47 个 DOI，全部解析成功，统计如下。
- 全部落在 `vsso.nssdc.ac.cn`，许可证全部是 **CC BY-NC-ND 4.0**，全部「即时公开」。
- shareScope 为「完全共享」46 个，「有条件共享」1 个（`和静站中纬高频雷达02原始自相关函数`）。
- **9 个**是占位元数据：时段写成 1999-01-01 → 1999-01-01，体量为 0。
- 其余时段大多截止到 2026-03。这只是元数据快照，比 3.3 查到的文件清单要旧。

### 3.3 数据检索 SPA：不登录能调的接口（从 JS bundle 反查）

SPA 由 Vue 构建：入口 `static/js/app.<hash>.js`，另有 48 个分块，在 `manifest.<hash>.js` 里列出，合计约 3.9 MB。axios 的 `baseURL` 是 `/apis`。登录后，令牌存在 `localStorage['Blade-Auth']`，请求时放进同名请求头。从代码里反查出 **92 个路径**，本文只测只读的那一部分，写操作一概没碰。

```bash
B=https://dcstatus.meridianproject.ac.cn/apis
curl -s -A Mozilla/5.0 -H 'Content-Type: application/json' -d '{}' "$B/online/search?current=1&size=20"   # 检索（POST 但只读）
curl -s -A Mozilla/5.0 "$B/online/detail/21226"                                   # 数据集详情
curl -s -A Mozilla/5.0 "$B/online/files?current=1&size=3&id=21226"                # 文件清单（只有名字和大小，fileurl 为空）
curl -s -A Mozilla/5.0 "$B/online/formatSpecification?id=20259"                   # 格式说明 PDF 的 URL
```

| 接口 | 方法 | 无令牌结果 |
| --- | --- | --- |
| `/online/search?current=&size=` | POST `{}` 或 `{"keyword":"测高仪"}` | **200**：共 1147 个数据集（1144 个带 DOI）；`size=200` 时 6 页 |
| `/online/detail/{id}` | GET | **200**：`code` 为 `OWHHP_IDIS01_IOPA_L2_STP`，另有 DOI、CSTR、中文描述；`version` 为 V01.01 |
| `/online/files?id=&current=&size=` | GET | **200**：id 21226 共有 615,918 个文件，最新一个是 `OWHHP_IDIS01_IOPA_L2_STP_20260925213000_V01.01.SAO`（6.89 KB） |
| `/online/formatSpecification?id=` | GET | **200**：返回 `…/s3/open/datasetFormatSpecification/<设备_产品>/…V1.1.pdf`；没有说明文档时 body 为 `code 400`「数据集格式说明文档不存在」 |
| `/online/conditions` · `/online/menu/phyparam` · `/online/sort/list` · `/online/contact/{id}` | POST / GET | **200**：筛选项（圈层、设备、台站、级别等）和排序字典 |
| `/zw2-sjfw/online/quickView?code=` | GET | 200，但对 IOPA 返回「暂无承载数据」 |
| `/online/files/download?id=&fileIds=` | GET | **HTTP 200，body `{"code":401,"msg":"请求未授权"}`** |
| `/online/datasetDic` · `/online/dataTypeData` · `/online/checkAuth` | GET | **401**「缺失令牌,鉴权失败」 |
| `/platform-business/basedata/{base-observatory,instrument-type-data}` · `/platform-business/datatype-data` | POST | **401** |
| `/datamanger/observatory/query` | POST | 500 |

**数据集编码与文件名**：数据集编码形如 `台站_设备nn_产品_级别_时间分割`，1147 条全部是 5 段。文件名在编码后面加上 `_YYYYMMDDhhmmss_Vnn.mm.<扩展名>`。
- 级别有 L0 / L1 / L1A–C / L2 / L3 / AUX 及带 Q 的快视级。
- 时间分割有 STP（逐次探测）、05M、01H、DAY 等。

**文件清单抽样**（`/online/files`，每个数据集只看最新 3 个文件名）：

| 数据集 id · 编码 | 文件数 | 最新文件（大小） |
| --- | --- | --- |
| 20259 `OWHHP_GTSM01_RINX_L1C_05M` RINEX 观测 | 223,690 | `…_20260926074000_V01.00.ORN`（1.79 MB） |
| 20260 `OWHHP_GTSM01_RNXE_AUX_DAY` RINEX 星历 | 761 | `…_20260925000000_V01.00.NRN`（2.88 MB） |
| 20263 `OWHHP_GTSM01_ATEC_L2_DAY` 垂直绝对 TEC | 851 | `…_20260925000000_V01.00.TXT`（156.84 MB） |
| 20261 `OWHHP_GTSM01_ISCI_L2_05M` 闪烁指数 | 212,554 | `…_20260926074000_V01.00.TXT`（21.14 KB） |
| 21224 `OWHHP_IDIS01_IONO_L1_STP` 频高图 | 644,735 | `…_20260925213000_V01.01.RSF`（1.17 MB） |
| 20639 `OSAYA_TISR01_IFIT_L2_DAY` 三亚 ISR 拟合参量 | 809 | `…_20260925000000_V01.00_N_LP_15sec.h5`（54.47 MB） |
| 21228 / 21223 测高仪漂移速度 / IQ，21253 沾益 ISR 电子密度 | **0** | — |

在 07:55 UT 查询时，最新 5 min 文件的时间戳是 `074000`，可见延迟约 15 min，文件名时间应是 UT（ISCI 格式说明写明 `Sampling Time(UTC)`）。**不登录只能看到文件名，拿不到文件**。

**官方格式说明 PDF**（`/s3/open/…`，公开）：抽查 6 个数据集，4 个有说明（RINX、ISCI、TISR_IFIT、TISR_GRID），2 个没有（ATEC、IONO）。原文要点：
- **RINX**（9 页，V1.1）：「采用 RINEX3.03 格式」；文件名 `OBSID_GTSMnn_RINX_L1C_05M_YYYYMMDDhhmmss_Vnn.mm.ORN`。文件头表列出 `#DataName`、`#Station`、`#DataLevel`、`#RecordNumber`、`#ObsParameters: SmpRate=1Hz/5Hz/10Hz` 等以 `#` 开头的子午工程公共头字段。
- **ISCI**（10 页）：`.TXT` 定宽列，列为 Time（UTC）、SatId（`A1I2`，C/G/E/R/S/J/I）、Az、El、S4（`F11.6`，无效值 `-99999999999`）、σ。
- **TISR_IFIT**（7 页）：「以 HDF5 格式存储」，包含 Time、GEO、Fitted parameter（Ne、Ti、Te、V）、Error、Fitstate、Rawne 等。文件名里的 `_D_CD_ITIME` 分别表示扫描模式（E/N/Z/A/F）、编码（LP/AC/BK/LA）和积累时间。

### 3.4 注册、登录与 SSO（只读公开页面，没有提交）

- **注册页** `https://soc.meridianproject.ac.cn/sso/register?lang=zh_CN`（200）：表单 `POST ./register`。必填项有用户名 / 邮箱、真实姓名、密码、手机号（带国家区号）、电子邮件、工作单位和验证码；前端会调用 `uniqueUser`、`uniqueEmail`、`uniquePhone` 做唯一性校验。页面还有「忘记密码」和「解锁申请」。
- **SSO 是 OAuth2 授权码流程**：门户里的登录链接是 `soc…/sso/oauth/authorize?client_id=147283221018093739&redirect_uri=https://soc.meridianproject.ac.cn/por&response_type=code`，未登录时 302 到 **`http://`**`soc.meridianproject.ac.cn/sso/login`（注意是明文 http）。SPA 用 `/apis/oauth/toLogin/soc_sjfw?code=…` 换令牌（不带 code 时返回 400），然后存进 `Blade-Auth`。门户页用 cookie `COOKIE_ZWMHT` 调 `/sso/user`（未登录返回 `status 601`），据此给 SPA 链接带上 `checkLogin=true/false`。
- **落地页的独立账号**：`vsso.nssdc.ac.cn` 是国家空间科学数据中心自己的账号体系，前端有 `frontEndLogin()`，本文没有测试。

### 3.5 批量下载 / 离线服务：公开可见的流程（没有提交）

以下只根据 SPA 前端文案（中英 i18n 字符串）和 NSSDC 落地页 JS 整理，**没有实际走过**：
1. 登录 → 在「用户空间 → 批量下载」（`#/sjfwofflineserviceapply`）点「新增」，填**数据集**、**申请数据开始时间**、**申请数据结束时间**。
2. 管理员审核，状态为「未审核 / 审核通过 / 审核未通过」，并附「审核意见」。通过后管理员填写「打包目录」，列表显示「点击下载」或「暂无下载路径」。
3. 数据订阅**只推送未来数据**。前端提示原文：“您可以在“批量下载”页面提交此部分历史数据的下载申请，网站工作人员将根据申请，为您下载相应数据，并推送至您的用户空间。”
4. 另有「数据权限审批」（`/datasetAuth/apply`，字段为数据级别、数据权限类型），对应元数据里「有条件共享」的数据集。
5. NSSDC 落地页的离线订单：JS 注释写明“线下共享 + 完全共享 = 简易订单(SIMPLE)，其他 = 申请表单(APPLICATION_FORM)”，提交接口是 `/nssdc/orderInfo/dataOrderAdd`，需要登录。

### 3.6 数据政策（2026-06-22 通知，原文摘录自 `/sjzc/`）

- **适用范围**：“凡全部或部分利用子午工程科学数据开展研究工作，并取得任何形式成果的，包括但不限于公开发表的科学论文、学术论著、学位论文，以及未公开发表的研究报告、数据产品、系统开发等成果”，都“应……在成果中规范注明数据来源（DOI标识）并引用子午工程的国家科技资源标识码（CSTR标识：https://cstr.cn/ 31122.02.MSP）”。
- **中文致谢格式（示例）**：“本项成果使用国家重大科技基础设施子午工程三站式非相干散射雷达电离层拟合基本参量数据（DOI: 10.12176/01.06.00065-V01），数据可通过访问https://dcstatus. meridianproject.ac.cn/获取。感谢子午工程（https://cstr.cn/ 31122.02.MSP）工作人员在数据收集和分析方面提供的技术支持和协助。”
- **英文致谢格式（示例）**：“We acknowledge the use of ionospheric fitted basic parameters of Triple-Station Incoherent Scattering Radar from the Chinese Meridian Project (DOI:10.12176/01.06.00065-V01). The data can be accessed via https://dcstatus.meridianproject. ac.cn/. We thank the staff of the Chinese Meridian Project (https://cstr.cn/ 31122.02.MSP) for their technical support and assistance in data collection and analysis.”（原文 URL 里有空格，引用时请去掉。）
- **成果报送**：“用户在使用子午工程数据产出成果后，应及时向子午工程中心提供成果信息（包括成果题目、发表渠道、发表时间、作者信息、单位信息等）”，报送邮箱 **wangjiangyan@nssc.ac.cn**（页面另附联系电话）。
- **约束**：“对未按规定进行致谢的，子午工程中心有权要求其补充或更正；情节严重的，子午工程保留暂停其数据使用权限的权利。”“此前有关规定与本通知不一致的，以本通知为准。”
- **许可证**：政策通知本身没写许可证；DOI 元数据里抽样 47 个**全部是 CC BY-NC-ND 4.0**（非商业、禁止演绎）。

## 4. 输入与输出

- **输入**：台站中文名、设备、产品。先查 `/sjj/` 得到 DOI，再解析句柄拿到 `linkId`，然后调 NSSDC 的 `getDetail`，从里面的 `url` 取出 SPA 数据集 id；或者直接用 SPA 的 `/online/search` 按关键词查。
- **输出（不登录）**：DOI / CSTR、元数据 JSON（时段、体量、许可证、致谢语）、文件名与大小清单、格式说明 PDF。
- **输出（登录后，未测）**：数据文件本身，扩展名按公开清单有 `.ORN`、`.NRN`、`.TXT`、`.DAT`、`.SAO`、`.RSF`、`.PNG`、`.h5`、`.jpg`、`.txt`、`.dat`；另有批量打包目录。
- **台站编码**：5 位字母，以 O 开头，例如 OWHHP 武汉黄陂、OSAYA 三亚、OMOHE 漠河。RINX 格式说明表 2 列出了 GNSS 站的经纬度和海拔。

## 5. 参数

| 位置 | 参数 | 说明 |
| --- | --- | --- |
| DOI 句柄 API | `https://doi.org/api/handles/<DOI>` | `values[type=URL]` 的 `?` 后面就是 NSSDC `linkId`；**要 `.strip()`**（坑 5） |
| NSSDC | `getDetail?linkId=` | GET，无需登录 |
| SPA 检索 | `current`、`size`（实测 200 可用）、body `{"keyword":…}` | `size=50` 时遇到过一次「Too many open files」400 |
| SPA 文件 | `id`（SPA 数据集 id，不是 NSSDC 的 linkId）、`current`、`size` | 只返回文件名和大小 |
| 格式说明 | `formatSpecification?id=` | 同一个 id 有时会返回「不存在」，重试即可（坑 7） |

## 6. 在工作流里接哪一步

- **路径 A · 一日 TEC**（[README](./README.md#a--一日-tec)）：中国区域台站的 TEC 与闪烁有 36 个站（RINEX 3.03、5 min 分割、1/5/10 Hz）。先用本文确认站点和时段有文件，再决定是否申请账号；开放替代见第 8 节。
- **路径 B · 不规则体 / 磁暴**（[README](./README.md#b--不规则体--磁暴)）：用闪烁指数（S4、σ）、测高仪（SAO / RSF）、三亚 ISR（HDF5）去对照 ROTI；地磁台站同样在 01.09 类里。
- 全球 ISR / TEC 的开放拉取见 [madrigal](./madrigal.md)，地磁台站 API 见 [geomag-api](./geomag-api.md)。

## 7. 坑（现象 → 原因 → 修复）

1. **`grep -c` 数出 1161，解析表格只得到 1084 行** → 77 行英文名是 `<br/>`，逐列正则会漏掉 → 按 `<td>…</td>` 取整行再去标签。
2. **按序号去重少了一条** → 序号 870 出现两次、869 缺失（两个不同的 DOI）→ **以 DOI 为主键**，不要用序号。
3. **以为 DOI 落在子午工程门户** → DOI 实际 302 到 NSSDC 的 `vsso.nssdc.ac.cn`（登记机构是 ISTIC）→ 元数据看 NSSDC 的 `getDetail`，数据看它里面的 `url`（dcstatus）。
4. **用 `curl -I` 访问落地页得到 400** → 该站不接受 HEAD 请求 → 用 GET。
5. **解析 DOI 句柄得到的 linkId 带了 `\r\n`，导致 `getDetail` 不是 JSON** → 个别句柄（如 `01.06.00066-V01`）登记的 URL 末尾有换行 → `.strip()`。
6. **元数据时段写着 1999-01-01、体量 0** → 占位元数据，抽样 47 个里有 9 个 → 以 SPA `/online/files` 的文件数为准。有的 DOI 在 SPA 里文件数为 **0**（IQ、漂移、沾益 ISR 的 L2），**有 DOI 不代表有数据**。
7. **接口返回 HTTP 200，但其实失败** → 失败信息写在 body 的 `code` 里（下载接口是 200 + `code 401`，格式说明是 200 + `code 400`）；负载均衡偶尔还会报「Load balancer does not have available server」或「Too many open files」→ 判断 `json['code']==200`，失败后间隔 3 s 重试。
8. **`/sjj/` 的 1161 与 SPA 的 1147 对不上** → 1110 个两边都有，51 个只在 `/sjj/`（中纬高频雷达的网络融合 / 电势产品按站登记 18 个，流星雷达风场剖面 12 个，GNSS 10 个，TYC 4 个等），2 个只在 SPA，另有 3 个 SPA 数据集没有 DOI → 引用以 DOI 为准，找数据以 SPA 为准。
9. **RINEX 文件头可能不标准（推断，未测）** → 格式说明规定了一组以 `#` 开头的子午工程公共头，但 2.3.2 节的样例是空的 → 拿到文件后先看前几行，再交给 RINEX 解析器。
10. **以为可以随便二次发布** → 元数据许可证是 CC BY-NC-ND 4.0，另有 2026-06-22 致谢与报送的强制要求，违者可能被暂停权限 → 只发派生统计并报送成果；不能转存原始文件。
11. **SSO 跳到了 `http://` 登录页** → authorize 的 302 目标是明文 http，而且 `http://soc…/sso/login` 直接返回 200，不会跳到 https → 手动改成 `https://` 后再输入密码。
12. **SPA bundle 里写死了一个框架默认的 Basic 客户端请求头** → 这是 BladeX 类框架的默认配置 → 本文的测试**没有带它**，结果照样是 200 / 401。它不是用户凭证，不要拿它去试任何接口。

## 8. 选型对比（中国区域电离层数据，开放替代）

| 需求 | 选 | 门槛 | 依据 |
| --- | --- | --- | --- |
| 子午工程台站原始 / 级别产品（测高仪 SAO、ISR HDF5、闪烁 S4） | **子午工程**（本文） | 注册账号；批量走离线申请 | 独有台站 |
| 中国区域 GIM | [CAS BDsmart IONEX](../data-access.md#gim--ionex) | 匿名 | 实测 `CAS0OPSFIN_20241310000_01D_30M_GIM.INX.gz` → 200 |
| 中国境内 IGS 站 RINEX | [GFZ ISDC 日观测](../data-access.md#开放产品镜像快径code--gfz--cas) / [CDDIS](../data-access.md#日采样-rinex-obsnavcddis) | GFZ 匿名 / CDDIS 需 Earthdata | GFZ `2024/131` 目录里实测有 `URUM00CHN`、`WUH200CHN` |
| 全球 TEC 格网（含中国） | [madrigal](./madrigal.md) · [E3](../data-access.md#dp-e3) | 匿名（需填姓名 / 邮箱参数） | 已有手册实测 |
| 测高仪（全球，含部分中国站） | [GIRO / DIDBase](../data-access.md#一屏决策) | 网页注册 | 本文未验证中国站点 |
| 地磁台站分钟值 | [geomag-api](./geomag-api.md)（INTERMAGNET） | 匿名 | 子午工程地磁同样需要登录 |
| CMONOC 陆态网 | —— | 本仓库 data-access 尚无条目，本文**未验证** | —— |
