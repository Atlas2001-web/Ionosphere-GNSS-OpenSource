# pygnssutils · NTRIP 客户端 / 简易 Caster（Python）

目录条目：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pygnssutils>  
文档：<https://www.semuconsulting.com/pygnssutils> · 列表：[03 GNSS 数据](../../lists/03-gnss-data.md)

## 作用与场景

在 pyubx2 / pyrtcm 等协议库之上提供 **CLI + 类**：

- `gnssntripclient`：从 NTRIP Caster 拉 RTCM3 / SPARTN；
- `gnssserver`：TCP 转发，或单挂载点 **NTRIP Server/Caster**；
- `gnssstreamer`：串口 / 文件 / NTRIP 等多源读写与过滤。

**何时用：** 实验室联调低成本接收机、脚本化录差分流、自建单挂载点试验 caster、把 RTCM 喂给 RTKLIB `str2str` / 板卡。  
**何时改用 BNC：** 需要多流运维 GUI、录高采样 RINEX、内置实时 PPP——见 [bnc.md](./bnc.md)。

## 安装

需要 **Python ≥ 3.10**。

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -U pygnssutils
gnssntripclient -h
```

账号可用环境变量 `PYGPSCLIENT_USER` / `PYGPSCLIENT_PASSWORD`；勿把密码写进公开仓库。

## 最小示例

**1）探活 sourcetable**

```bash
gnssntripclient \
  --server example-caster.example.org --port 2101 --https 0 \
  --datatype RTCM --ntripversion 2.0 \
  --reflat 39.9 --reflon 116.4 \
  --ntripuser "$NTRIP_USER" --ntrippassword "$NTRIP_PASS" \
  --verbosity 2
```

**2）订阅指定挂载点**

```bash
gnssntripclient \
  --server example-caster.example.org --port 2101 \
  --mountpoint YOUR_MOUNT --datatype RTCM \
  --ggainterval 60 --reflat 39.9 --reflon 116.4 \
  --ntripuser "$NTRIP_USER" --ntrippassword "$NTRIP_PASS" \
  --verbosity 2
```

成功时日志会出现 RTCM 消息类型（如 1005 / 1077）。参数名以 `gnssntripclient -h` 与当前上游为准。

**3）本机单挂载点试验 caster**

```bash
gnssserver \
  --inport "/dev/ttyACM0" --hostip 0.0.0.0 --outport 2101 \
  --ntripmode 1 --protfilter 4 --format 2 \
  --ntripuser myuser --ntrippassword mypassword --verbosity 2
```

挂载点名默认可为 `pygnssutils`（以上游当前说明为准）。再用本包客户端或 [BNC](./bnc.md) 验证。

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | NTRIP 源表与差分流；串口/TCP 上的 NMEA、UBX、SBF、RTCM3、SPARTN 等 |
| 输出 | 解析日志；转发到串口/文件/TCP 的二进制流；caster 模式下的 RTCM 播发 |
| 不做 | 精密定位滤波、TEC/ROTI 产品（外接 [RTKLIB](./rtklib.md) / TEC 工具） |

## 常见坑

1. **401/403**：核对用户、密码、NTRIPv1/v2、挂载点是否开放。  
2. **VRS 要 GGA**：网络 RTK 常需周期性上报近似位置（`--ggainterval`、`--reflat/lon`）。  
3. **自签 HTTPS**：按上游说明配置证书路径。  
4. **误当 BNC**：多流 GUI / 内置 PPP 不是本包重点。  
5. **公网裸奔 caster**：至少设密码、防火墙与限流。

## 接到哪一步分析

- 实时定位：流 → [RTKLIB](./rtklib.md) `str2str` / `rtkrcv`，或接收机板卡。  
- 事后电离层：先落成 RINEX，再 [georinex](./georinex.md) → TEC / ROTI。  
- 同子类对照：BNC 等（见 `lists/03-gnss-data.md`）。  
- 数据入口：[data-access.md](../data-access.md)。
