# autorino · IPGP 接收机拉取 → RINEX3/4 操作手册

目录：[`PROJECTS.json` → `autorino`](../../PROJECTS.json) · 上游 <https://github.com/IPGP/autorino> · 文档 <https://ipgp.github.io/autorino/> · 伴生 [rinexmod](https://github.com/IPGP/rinexmod) · **GPL-3.0** · 本机验证 **2.4.2**（rinexmod 4.2.1 / geodezyx 5.2.0，2026-09-24 ET）：CLI `--help`、`autorino_cfgfile_check` 合并样例站配置实跑；厂商 RAW→RINEX **未跑**（缺官方转换器授权/二进制）

> 岗位：台网 **自动下载主流厂商原始数据 → 官方工具转 RINEX3/4 → 拼接/切分 → rinexmod 改头改名**。近实时可到约 5 min。冲突时：**本机 `autorino_* --help` / 官方 docs > 本文**。

## 1. 用途与边界

**做：**

1. **Download**：FTP/HTTP 等从接收机拉 RAW（Trimble T02、Leica MDB、Septentrio SBF、Topcon、BINEX…）
2. **Convert**：调用厂商/社区转换器 → RINEX3/4（路径写在 YAML `environment.conv_software_paths`）
3. **Handle**：splice / split（可挂 `gfzrnx` / ConvertoCPP 等）
4. **Metadata**：经 **rinexmod** 改头、长名、压缩、注释（autorino **默认认为头不可信**，以外源 sitelog/站配置为准）

**不做：**

- **不是** 定位 / PPP / TEC → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) / [pytecgg](./pytecgg.md)
- **不是** 观测 QC 报告主力 → [anubis](./anubis.md)；旧 TEQC 批壳 → [pinot](./pinot.md)
- **不是** 替代厂商 EULA：转换器需自行下载/授权；**GFZRNX 例行使用需商业许可**（上游明文警告）
- 本机无接收机、无 `t0xConvert`/`sbf2rin`/`mdb2rinex` 时，**不要假装跑通 convert**

一句话：autorino = **IPGP 台网入库流水线编排器**；算力在外部转换器 + rinexmod。

| 术语 | 含义 |
| --- | --- |
| `site_id` / `SITE_ID9` / `SITE_ID4` | 9 字符站码 / 其 4 字符前缀（路径模板占位） |
| `session_01D30S` | 会话名：日文件、30 s 采样（可改） |
| `steps` | `download` / `convert` / `split` / `splice` / `rinexmod` |
| `$AUTORINO_DIR` / `$AUTORINO_ENV` | 仓根路径；含 `environment` 的 YAML |
| `rinexmod` | 改头/长名/压缩伴生包 |

## 2. 安装

```bash
cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
# 推荐：直接装 GitHub（含 console_scripts）
python -m pip install "git+https://github.com/IPGP/autorino.git"
# 或开发：git clone && pip install -e .
python -c "import importlib.metadata as m; print(m.version('autorino'), m.version('rinexmod'))"
# 期望类似：2.4.2 4.2.1

export AUTORINO_DIR=~/iono_ops/autorino          # clone 后的仓根（不是仓内第二层 autorino/ 包目录）
export AUTORINO_ENV=${AUTORINO_DIR}/configfiles/main/autorino_main_cfg.yml
# 未设 AUTORINO_ENV 时回落到包内 autorino/cfgenv/autorino_env_default.yml（本机如此）

autorino_cfgfile_run --help | head -n 8
```

**本机截断（2026-09-24 ET）：**

```text
260924T07:48:29.667|I|read_env       |autorino & rinexmod version: 2.4.2 & 4.2.1
260924T07:48:29.668|I|read_env       |Loading environment configfile: .../autorino_env_default.yml
usage: autorino_cfgfile_run [-h] -c CONFIG
```

工作目录须先存在（check/run 会强校验 parent）：

```bash
mkdir -p ~/autorino_workflow/{tmp,log,raw,rnx} ~/sitelogs
```

厂商转换器安装见官方 [external converters](https://ipgp.github.io/autorino/external_converters.html)；装好后把可执行名或绝对路径写进 `environment.conv_software_paths`（或保证在 `$PATH`）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Custom environment configfile not defined` | 未 export `AUTORINO_ENV` | 指向含 `environment:` 的 YAML；或接受 default |
| `tmp does not exists, create it manually` | 工作父目录未建 | `mkdir -p ~/autorino_workflow/tmp` |
| `pip` 拉一长串依赖 | 正常（geodezyx/rinexmod/…） | 用 venv，勿污染系统 Python |

## 3. 端到端：样例站 YAML → cfgfile_check（本机真跑）

完整 download/convert 需要通网的接收机与厂商二进制。本节验证 **配置合并与 CLI**，这是上线前的最小门禁。

### 3.1 修正仓内样例 include 路径

仓内 `configfiles/sites/autorino_site_trimble_cfg.yml` 写了 `../profile/...`，实际目录名是 **`profiles/`**：

```bash
cd ${AUTORINO_DIR:-~/iono_ops/autorino}/configfiles/sites
sed 's|../profile/|../profiles/|' autorino_site_trimble_cfg.yml \
  > autorino_site_trimble_fixed.yml
# 将站配置里的 hostname/login/password 换成你的接收机；样例是占位
mkdir -p ~/autorino_workflow/{tmp,log,raw,rnx} ~/sitelogs
```

### 3.2 关键参数（`autorino_cfgfile_run` / `check`）

| 参数 | 作用 |
| --- | --- |
| `-c` / `--config` | 站 YAML 或目录（目录下全部 `.yml`） |
| `-i` / `--include_config` | 额外 include，覆盖站文件里的 `include` |
| `-s` / `-e` | 历元起止：`yesterday`、`2025-01-01`、`2025-140` 等 |
| `-p` | 周期：`1D` / `1H` / `15M` |
| `-si` / `-xsi` | 只跑/排除某些 `site_id` |
| `-sp` / `-xsp` | 只跑/排除步骤：`download convert split splice rinexmod` |
| `-f` | 强制重做（覆盖 YAML 里 `force: false`） |

`autorino_cfgfile_check`：`-c` 必填；`-o` 写出**合并后** YAML。

### 3.3 本机：cfgfile_check

```bash
cd ${AUTORINO_DIR}/configfiles/sites
autorino_cfgfile_check -c autorino_site_trimble_fixed.yml -o /tmp/autorino_checked.yml
wc -l /tmp/autorino_checked.yml
head -n 40 /tmp/autorino_checked.yml
```

**本机结果：** 退出 0；合并文件 **105** 行。截断：

```text
cfgfile_version: 20.2
environment:
  conv_software_paths:
    convbin: convbin
    ...
    t0xconvert: t0xConvert
    trm2rinex: trm2rinex:cli-light
    ...
station:
  access:
    protocol: ftp
    hostname: 192.168.0.1
    ...
  device:
    rec_type: TRIMBLE NETR9
    ant_type: TRM55971.00     NONE
  site:
    site_id: SITE00FRA
  sessions:
    session_01D30S:
      steps:
        download: { active: true, ... inp_file_regex: <SITE_ID4>______%Y%m%d0000A.T02 }
        convert:  { active: true, options.converter: auto, rinexmod_options.longname: true, ... }
```

| 字段 | 含义 |
| --- | --- |
| `conv_software_paths.*` | 转换器可执行名/路径；Trimble 官方键小写 `t0xconvert`、值常为 `t0xConvert` |
| `trimble_default_software` | 默认用 `trm2rinex`（docker）还是 `t0xconvert` |
| `inp_file_regex` | 远端/本地 RAW 名模板（含 `<SITE_ID4>`、`%Y%m%d`） |
| `out_dir_structure` | 如 `<SITE_ID9>/%Y/%j` |
| `rinexmod_options` | `longname` / `compression: gz` / `filename_style` 等 |

### 3.4 工作流启动（有接收机时）

```bash
# 仅检查配置合并（无下载）
autorino_cfgfile_check -c autorino_site_trimble_fixed.yml -o /tmp/ok.yml

# 跑 download+convert，限定站与日期（示例）
autorino_cfgfile_run -c autorino_site_trimble_fixed.yml \
  -s 2025-01-01 -e '10 days ago' \
  -sp download convert -f

# 或：已有本地 RAW 目录时，单独转换
autorino_convert_rnx -i /path/to/raws -o ~/autorino_workflow/rnx \
  -t '<SITE_ID9>/%Y/%j' -m ~/sitelogs -frnx
```

API 等价（官方 cookbook）：`autorino.api.convert_rnx(inp_raws, out_dir, ...)`。

### 3.5 check_rnx 冒烟（本机部分成功）

```bash
mkdir -p /tmp/aro_rnx_demo/SITE00FRA/2018/173
# 放入符合猜测长名的文件才能 ok_inp=True；此处仅演示 CLI
autorino_check_rnx -i /tmp/aro_rnx_demo -t '<SITE_ID9>/%Y/%j' \
  -s 2018-06-22 -e 2018-06-22 -o /tmp/aro_check_out -l SITE00FRA
```

**本机截断 stdout（autorino 2.4.2 + geodezyx 5.2.0，2026-09-24 ET）：**

```text
...|I|guess_local_rnx|nbr local RINEX files guessed: 1
...|I|print_table    |CheckGnss SITE00FRA/...
  fname  site      epoch_srt         epoch_end  ok_inp  ok_out  ...
0   NaN  SITE00FRA 18-06-22 00:00:00 18-06-22 23:59:59   False   False  ..._MO.crx.gz
...|I|check_rnx      |Check:
| epoch_srt   |   SITE |
| 2018-173    |      0 |
AttributeError: module 'geodezyx.utils' has no attribute 'figure_saver'. Did you mean: 'pickle_saver'?
```

表（完备率 0）先出来，再在写图阶段炸。出图需 geodezyx/autorino 版本对齐或等上游修。**禁止当作转换成功。**

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| 站 YAML + main/profile include | `cfgfile_version` 与文档一致（样例 20.2） |
| 接收机 RAW | 与 `inp_file_regex` / 转换器匹配 |
| sitelog 或 `device.*` | 改头元数据源 |
| 外部转换器 | 见官方 converters 页 |

| 输出 | 下游 |
| --- | --- |
| RINEX3/4（常 `.rnx.gz` 长名） | [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md) / 路径 A TEC |
| `~/autorino_workflow/raw` 归档 | 保留原始（工具不删 RAW） |
| check 表 / 日志 | 运维缺数告警 |

**明确不输出：** 坐标解、TEC、Anubis XTR。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 台网近实时入库 | §3.4 | [gfzrnx](./gfzrnx.md) 抽稀 → [anubis](./anubis.md) QC |
| 只有旧静态盘 + TEQC 习惯 | — | [pinot](./pinot.md) |
| 一日 TEC | 本页落 RINEX 后 | 路径 A：[georinex](./georinex.md)→[pytecgg](./pytecgg.md) |
| 实时流不是机内文件 | — | [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `config file doesn't exists! .../sites/configfiles/main/...` | include 相对路径解析错 / 旧相对根 | 在 `configfiles/sites` 下跑；include 写 `../main/...` |
| 2 | include `../profile/...` FileNotFound | 目录实为 `profiles/` | `sed 's|../profile/|../profiles/|' …` |
| 3 | `tmp does not exists, create it manually` | 未建工作父目录 | `mkdir -p ~/autorino_workflow/tmp` |
| 4 | convert 立刻失败 / 找不到转换器 | `PATH` 或 YAML 路径未指到二进制 | `which t0xConvert sbf2rin mdb2rinex convbin`；改 `conv_software_paths` |
| 5 | Trimble 键名混淆 | 键 `t0xconvert` vs 值 `t0xConvert` | 对照 `autorino_env_default.yml`；官方大小写敏感 |
| 6 | 头被改“错了” | 设计上**以外源元数据覆盖** | 先改 sitelog/站 YAML；看 convert 后 firmware/SN 警告 |
| 7 | `gfzrnx` 例行跑被质询 | 许可限制 | 换 Converto/其它 handle；有许可再写进 YAML |
| 8 | `check_rnx` 表有了但 `AttributeError: ... figure_saver` | geodezyx 5.2.0 无该符号（提示 `pickle_saver`） | 钉兼容 geodezyx 或跳过出图；先用表 |
| 9 | docker `trm2rinex:cli-light` 拉不起 | 未装 Docker / 无镜像 | 改 `trimble_default_software: t0xconvert` 并用官方 Linux 转换器 |
| 10 | 多站同时 FTP 打满链路 | 同 `datalink` 并发 | 站配置里设不同 `datalink` 标签或错峰 `-si` |
| 11 | 把 Pinot/`teqc` 当 RINEX3/4 主链 | 工具年代不同 | RINEX3/4 用 autorino；旧 2.11 批壳用 [pinot](./pinot.md) |
| 12 | 密码写进 git | 站 YAML 含 `password` | 私有配置仓 / 环境注入；**勿提交口令** |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 厂商 RAW→RINEX3/4 台网自动化 | **autorino** |
| 旧静态 RINEX2 + TEQC 批处理 | **Pinot** |
| 观测 QC 报告 | **Anubis** |
| 已有 RINEX 清洗 | **gfzrnx** |
| NTRIP 拉流 | [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) |

## 8. 相关

[pinot](./pinot.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [georinex](./georinex.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [data-access](../data-access.md) · [README](./README.md)
