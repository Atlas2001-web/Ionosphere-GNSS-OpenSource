# pygnssutils

目录：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pygnssutils> · PyPI `pygnssutils` · BSD-3-Clause

## 用途

- Python CLI/库：NTRIP 客户端、轻量 caster、串口/文件流探活。
- 主命令：`gnssntripclient`、`gnssserver`、`gnssstreamer`。
- **不做** TEC/ROTI/PPP；生产多用户播发用 [bkg-ntripcaster](./bkg-ntripcaster.md)。

## 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip pygnssutils
gnssntripclient -h | head
gnssserver -h | head
gnssstreamer -h | head
```

可选 GUI：`pip install pygpsclient`（失败不影响 CLI）。

凭据建议用环境变量（勿提交仓库）：

```bash
export PYGPSCLIENT_USER='your_user'
export PYGPSCLIENT_PASSWORD='your_pass'
```

## 快速上手

```bash
# A) 只拉源表（探活）
gnssntripclient \
  --server example-caster.example.org --port 2101 \
  --https 0 --datatype RTCM --ntripversion 2.0 \
  --reflat 39.9 --reflon 116.4 \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2

# B) 订阅挂载点（VRS 常需 GGA）
gnssntripclient \
  --server example-caster.example.org --port 2101 \
  --mountpoint YOUR_MOUNT --datatype RTCM --ntripversion 2.0 \
  --ggainterval 60 \
  --reflat 39.9042 --reflon 116.4074 --refalt 44.0 \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2

# C) 本机串口 → 单挂载点 caster
# 终端1
gnssserver --inport /dev/ttyACM0 --hostip 0.0.0.0 --outport 2101 \
  --ntripmode 1 --protfilter 4 --format 2 \
  --ntripuser labuser --ntrippassword 'change-me-now' --verbosity 2
# 终端2
gnssntripclient --server 127.0.0.1 --port 2101 --mountpoint pygnssutils \
  --ntripuser labuser --ntrippassword 'change-me-now' --datatype RTCM --verbosity 2

# D) 看板卡吐什么
gnssstreamer --inport /dev/ttyACM0 --verbosity 2

# E) 仅 TCP 转发（非 NTRIP）
gnssserver --inport /dev/ttyACM0 --hostip 127.0.0.1 --outport 50010 \
  --ntripmode 0 --verbosity 2
```

**预期：** A 打印源表行；B 持续出现 RTCM 类型（如 1005/1077）；C 本机可订。参数以本地 `-h` 为准。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | Caster、串口、TCP、已录文件 |
| 输出 | RTCM/UBX/NMEA 字节流、日志；可重定向落盘 |
| 不做 | RINEX 科学产品（需另转）；STEC/ROTI |

## 常用参数

| 命令 | 关键选项 |
|---|---|
| `gnssntripclient` | `--server --port --mountpoint --datatype --ntripversion --ggainterval --reflat/lon/alt --https` |
| `gnssserver` | `--inport --outport --ntripmode --protfilter --hostip` |
| `gnssstreamer` | `--inport`、协议过滤 |

`ggainterval -1` 常表示不发 GGA（以 `-h` 为准）。端口 **2101** 勿与其它服务冲突。

## 接到工作流哪一步

- 路径 C 入口；流给 [rtklib](./rtklib.md) 或落盘后走 TEC/ROTI
- 多流 GUI 对照：[bnc](./bnc.md)
- 正式对外播发：[bkg-ntripcaster](./bkg-ntripcaster.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| CLI 找不到 | 确认 venv 已激活 |
| VRS 无数据 | 发送合理 GGA；检查纬经高 |
| 401 | 用户口令/挂载点 ACL |
| `gnssserver` 无流 | 串口权限、波特率、`protfilter` |
| 想要 TEC | 落盘→转 RINEX→[pytecgg](./pytecgg.md) |
| 与 BNC 抢端口 | 错开 2101 |

## 相关工具

[bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md)

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
