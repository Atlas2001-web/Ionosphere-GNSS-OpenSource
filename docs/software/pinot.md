# Pinot · “Pinot is not only TEQC” 质检/预处理操作手册

目录：[`PROJECTS.json` → `pinot`](../../PROJECTS.json) · 上游 <https://github.com/purpleskyfall/pinot> · 脚本文档索引 <http://gnss.help/2017/02/16/pinot-content/>（链接已失效，2026-09-26 检查域名已不存在） · **GPL-2.0** · Python3 脚本集（非 PyPI 包）· 本机验证：`orderfile` / `sitecheck` / `metacheck` / `subnet` / `low2upper` 实跑（2026-09-24 ET）；`qualitycheck` 因无 Linux `teqc` 仅冒烟失败路径

> 岗位：CORS / 台网 **静态 RINEX 批处理**——缺站检查、头信息比对、IGS 日目录整理、子网划分；QC 数字靠 **TEQC `+qc`**。冲突时：**本机脚本 `-h` / 上游 README > 本文**。

## 1. 用途与边界

**做：**

- 批量：厂商原始 → RINEX 2.11（`trimble2rnx` / `leica2rnx`，依赖 `runpkr00`/`teqc` 等）
- 批量：RINEX ↔ Compact RINEX（`crnx2rnx` / `rnx2crnx`，依赖 RNXCMP）
- 批量：缺站检查（`sitecheck`）、元数据漂移（`metacheck`）、TEQC QC 摘要（`qualitycheck`）
- 批量：头标准化（`unificate`）、站点改名（`renamesite`）、大小写（`low2upper`/`up2lower`）
- 批量：按 IGS 日目录整理（`orderfile`）、按 YAML 子网分拣（`subnet`）

**不做：**

- **不是** 现代 Anubis 式 XTR/XML 多系统 QC → [anubis](./anubis.md)
- **不是** RINEX 3/4 拼接/抽稀主力 → [gfzrnx](./gfzrnx.md)
- **不是** 接收机近实时拉取 + RINEX3/4 官方转换链 → [autorino](./autorino.md)
- **不是** TEC / 定位解算 → [gnss-tec](./gnss-tec.md) / [rtklib](./rtklib.md)
- 仓内附带的 `teqc.exe` / `crx2rnx.exe` / `runpkr00.exe` 是 **Windows** 二进制；Linux 需自备同名可执行并进 `PATH`

一句话：Pinot = **TEQC/RNXCMP 外包的 Python 批处理壳**；口号 “not only TEQC”，但核心 QC 仍绑 TEQC。

| 术语 | 含义 |
| --- | --- |
| `_sites.yml` | `sitecheck` 站点列表（4 字符小写） |
| `_sitesinfo.yml` | `metacheck` / `unificate` 的接收机/天线/坐标参考 |
| `_sitemap.yml` | `renamesite` 旧站名→新站名 |
| `_subnet.yml` | `subnet` 网名→站列表 |
| MP1/MP2 / SN1/SN2 / CSR | TEQC QC：多路径、信噪比、周跳比（`1000/olps`） |

## 2. 安装

```bash
cd ~/iono_ops
git clone --depth 1 https://github.com/purpleskyfall/pinot.git
cd pinot
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install PyYAML tqdm
# 可选外部工具（按你要用的脚本）：
#   teqc（UNAVCO，已停更；qualitycheck/unificate/厂商转 RINEX 需要）
#   crx2rnx / rnx2crx（RNXCMP；crnx2rnx.py / rnx2crnx.py）
#   runpkr00（Trimble 旧链；trimble2rnx.py）
which teqc crx2rnx || echo "缺外部二进制：对应脚本会失败或空结果"
python sitecheck.py -h | head -n 5
# 期望：usage: sitecheck.py ...
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ModuleNotFoundError: yaml` / `tqdm` | 未装依赖 | `pip install PyYAML tqdm` |
| `TypeError: load() missing ... Loader` | **PyYAML≥5.1/6** 禁裸 `yaml.load` | 见 §3.0 兼容补丁 |
| `teqc: not found` | Linux 无 TEQC | 自备二进制进 `PATH`；或改用 [anubis](./anubis.md) |
| 仓内 `.exe` 在 Linux 无法执行 | Windows 附件 | 不要 `chmod +x teqc.exe` 当 Linux 用 |

## 3. 端到端：短 OBS → sitecheck / metacheck / orderfile（本机真跑）

样本：georinex 测试 OBS（RINEX **2.11**，2018-06-22 = **doy 173**），复制为经典短名以便 `sitecheck` 匹配。

### 3.0 PyYAML 兼容（必做，否则 sitecheck/metacheck 直接炸）

上游仍写 `yaml.load(stream)`。本机 **PyYAML 6.0.3** 报：

```text
TypeError: load() missing 1 required positional argument: 'Loader'
```

一次会话补丁（写入 `~/iono_ops/run_pinot.py`）：
```bash
cat > ~/iono_ops/run_pinot.py <<'PY'
import sys, yaml, runpy
_orig = yaml.load
def _compat_load(stream, Loader=None):
    if Loader is None:
        return yaml.safe_load(stream)
    return _orig(stream, Loader=Loader)
yaml.load = _compat_load
script = sys.argv[1]
sys.argv = [script] + sys.argv[2:]
runpy.run_path(script, run_name="__main__")
PY
# 用法：python ~/iono_ops/run_pinot.py ~/iono_ops/pinot/sitecheck.py ...
```

### 3.1 取数与摆放

```bash
mkdir -p ~/iono_ops/data/pinot_demo && cd ~/iono_ops/data/pinot_demo
curl -fsSL -o _raw.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
cp _raw.18o bjfs1730.18o
cp _raw.18o shao1730.18o
cp _raw.18o chan1730.18o
cat > sites_demo.yml <<'EOF'
- bjfs
- shao
- chan
- wuhn
- kunm
EOF
head -n 2 bjfs1730.18o
# 期望：RINEX VERSION / TYPE 含 OBSERVATION DATA；绝不是 <!DOCTYPE
```

### 3.2 sitecheck（缺站）

| 参数 | 作用 |
| --- | --- |
| `-cfg` | YAML 站列表；默认 `_sites.yml` |
| `-yr` / `-doy` | 年、年积日（必填） |
| `-r` | 递归子目录 |
| 位置参数目录 | 找短名 `ssssddds.yyo/d` 或长名 `…_MO.rnx/crx` |

```bash
cd ~/iono_ops/data/pinot_demo
python ~/iono_ops/run_pinot.py ~/iono_ops/pinot/sitecheck.py \
  -cfg sites_demo.yml -yr 2018 -doy 173 .
```

**本机 stdout（2026-09-24 ET）：**

```text
Start processing: .
Observations not found at 2018, 173 for: kunm, wuhn
```

| 输出 | 含义 |
| --- | --- |
| `Observations not found … for: kunm, wuhn` | YAML 有、目录无匹配文件名的站 |
| 无该行 | 列表站当日 OBS 齐 |

### 3.3 metacheck（头 vs YAML）

```bash
cat > sitesinfo_demo.yml <<'EOF'
bjfs:
    receiver: "TRIMBLE NETR8"
    antenna: "TRM59900.00     SCIS"
    position: "-2148744.8407  4426642.9605  4044657.8518"
    delta: "0.0465        0.0000        0.0000"
EOF
python ~/iono_ops/run_pinot.py ~/iono_ops/pinot/metacheck.py \
  -cfg sitesinfo_demo.yml -out list bjfs1730.18o
```

**本机截断 stdout：**

```text
Start processing: bjfs1730.18o

bjfs1730.18o has difference:
receiver in cfg file: TRIMBLE NETR8
receiver in obs file: Unknown
antenna in cfg file: TRM59900.00     SCIS
antenna in obs file: UNKNOWN EXT
position in cfg file: -2148744.8407  4426642.9605  4044657.8518
position in obs file: -4647137.5830  2562189.6255 -3526626.7006
delta in cfg file: 0.0465        0.0000        0.0000
delta in obs file: 2.0000        0.0000        0.0000
```

| 字段 | 含义 | 误用 |
| --- | --- | --- |
| `receiver` / `antenna` | 头 `REC # / TYPE`、`ANT # / TYPE` 切片 | 把测试样例头当真站 |
| `position` | `APPROX POSITION XYZ`；`-thd` 默认 **10 m** | 阈值过小刷屏 |
| `delta` | `ANTENNA: DELTA H/E/N` | 空格格式与 YAML 不一致被判差 |

`-out table` 打成宽表，便于 `grep`。

### 3.4 orderfile（IGS 日目录）

**不依赖 PyYAML / TEQC**，本机可直接跑：

```bash
cd ~/iono_ops/data/pinot_demo
python ~/iono_ops/pinot/orderfile.py -k -out ordered bjfs1730.18o shao1730.18o
find ordered -type f
```

**本机 stdout：**

```text
Start processing: bjfs1730.18o, shao1730.18o
bjfs1730.18o => ordered/2018/173/18o
shao1730.18o => ordered/2018/173/18o
```

落盘：`ordered/2018/173/18o/*.18o`（年 / doy / `yy`+类型）。`-k` 保留原文件；不加则**移动**。

### 3.5 qualitycheck（需 TEQC；本机未装）

```bash
python ~/iono_ops/pinot/qualitycheck.py -out table bjfs1730.18o
# 有 teqc + 可选 -nav brdc 时输出：date start end hours percent SN1 SN2 MP1 MP2 CSR
```

**本机无 `teqc` 时：**

```text
Start processing: bjfs1730.18o
     file          date         start           end        hours  percent   SN1     SN2     MP1    MP2    CSR
Quality check failed files: bjfs1730.18o
```

表头会印，行空 + `failed files` = 外部 `teqc +qc` 退出非 0。有二进制后再跑；指标含义以上游 TEQC 报告为准，**禁止臆造数字**。

### 3.6 其它常用一行

```bash
# 子网分拣（要 YAML 补丁）
python ~/iono_ops/run_pinot.py ~/iono_ops/pinot/subnet.py \
  -cfg ~/iono_ops/pinot/_subnet.yml -k -out subnets \
  bjfs1730.18o shao1730.18o chan1730.18o
# 本机 stdout：
# bjfs1730.18o => subnets/net1
# bjfs1730.18o => subnets/net3
# shao1730.18o => subnets/net2
# chan1730.18o => subnets/net1

# 文件名小写→大写（无 YAML）
python ~/iono_ops/pinot/low2upper.py -k -out uppered bjfs1730.18o
# 本机 stdout：
# Start processing: bjfs1730.18o
# 1 files have been processed.
# BJFS1730.18O
```

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| RINEX OBS 2.x / 部分长名 | `sitecheck` 认短名与 `…_MO.(crx|rnx)` |
| YAML 四件套 | 站名 **小写 4 字符** |
| `teqc` / RNXCMP / `runpkr00` | QC、压扩、厂商链 |

| 输出 | 下游 |
| --- | --- |
| 缺站列表 / 元数据差表 | 运维补数、改头 |
| `year/doy/yyo` 树 | 入库、交 [gfzrnx](./gfzrnx.md)/[anubis](./anubis.md) |
| TEQC QC 表 | 门禁阈值（自定） |

**明确不输出：** XTR/XML、RINEX4 官方链、TEC。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 台网日数据是否齐 | §3.2 | 补传 / [data-access](../data-access.md) |
| 换机换天线稽核 | §3.3 | sitelog；改头用 `unificate`（要 TEQC） |
| 入库前目录规范化 | §3.4 | [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md) → 路径 A |
| 近实时厂商 RAW→RINEX3/4 | — | [autorino](./autorino.md) |
| 现代多系统 QC 报告 | — | [anubis](./anubis.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `TypeError: load() missing ... Loader` | PyYAML 6 禁裸 `yaml.load` | `python run_pinot.py sitecheck.py …`（§3.0） |
| 2 | `Quality check failed files: …` 且无数字 | `PATH` 无 `teqc` | `which teqc`；装 UNAVCO 二进制或换 [anubis](./anubis.md) |
| 3 | `sitecheck` 全站 missing | doy/年与文件名不一致 | 文件名 doy 与 `-doy` 对齐；或 `-r` |
| 4 | 长名站未被识别 | 类型后缀非 `MO` / 扩展名不对 | 对照脚本正则；或先改短名 |
| 5 | `orderfile` 后原文件消失 | 默认 **move** | 加 `-k` |
| 6 | `metacheck` 全站 position 报警 | `-thd` 默认 10 m | `-thd 30` 或更新 `_sitesinfo.yml` |
| 7 | `unificate` / `crnx2rnx` import 失败 | 缺 `tqdm` | `pip install tqdm` |
| 8 | Linux 跑 `.exe` | 仓内 Windows 附件 | 装原生 `teqc`/`crx2rnx` 进 `PATH` |
| 9 | `trimble2rnx` 无输出 | 无 `runpkr00`+`teqc` | 装两者；或改 [autorino](./autorino.md) |
| 10 | 把 Pinot QC 当 Anubis 等价 | 指标/系统覆盖不同 | 切换工具时**同站对比定义** |
| 11 | `subnet` 站落空网 | 站名不在 `_subnet.yml` | 补 YAML 或改文件名前 4 字符 |
| 12 | 只处理 `.18o` 忽略 `.18d` | Compact 需先解压 | `crnx2rnx.py -k -out rinex *.18d`（需 RNXCMP） |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 旧 CORS 脚本化缺站/改名/日目录 | **Pinot** |
| 现代 QC 报告（XTR/XML） | **Anubis** |
| RINEX 3/4 抽稀拼接 | **gfzrnx** |
| 厂商 RAW 近实时→RINEX3/4 | **autorino** |
| 读盘探活 | [georinex](./georinex.md) |

## 8. 相关

[autorino](./autorino.md) · [anubis](./anubis.md) · [gfzrnx](./gfzrnx.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · [README](./README.md)
