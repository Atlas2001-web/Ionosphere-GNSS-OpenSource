# BKG NtripCaster · 专业 NTRIP 播发操作手册

目录：[`PROJECTS.json` → `BKG-NtripCaster`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bkgcaster> · IGS NTRIP 概览 <https://igs.bkg.bund.de/ntrip/index> · FTP `NTRIP/software/NtripCaster/` · GPL

> 岗位：在 **Linux** 上做多客户端 NTRIP v1/v2 **播发**（源表、用户组、挂载点 ACL、中继）。只分发字节，**不解码** RTCM，不做 VRS。参数以包内手册与 `*.dist` 注释为准。

## 1. 用途与边界

**做：** 多用户多挂载点播发；中继远端流到本地挂载点；与 BNC / RTKLIB / 手簿 / [pygnssutils](./pygnssutils.md) 联调。

**不做：** 五分钟单挂载点演示 → `gnssserver`（[pygnssutils](./pygnssutils.md)）；多流 GUI 收流录 RINEX → [bnc](./bnc.md)；TEC/ROTI/PPP；Caster「自动选站 / VRS」。

一句话：正式/课程 **播发站**；电离层产品仍在客户端落盘转 RINEX 之后。

## 2. 安装（Linux）

```bash
# 从 BKG FTP 取 ntripcaster-*.tar.bz2（版本以目录为准）
bunzip2 -k ntripcaster-*.tar.bz2 2>/dev/null || bunzip2 ntripcaster-*.tar.bz2
tar xf ntripcaster-*.tar
cd ntripcaster-*
./configure --prefix="$HOME/ntripcaster"
make -j"$(nproc)"
make install
```

```bash
CONF="$HOME/ntripcaster/conf"   # 以实际前缀为准
cd "$CONF"
for f in ntripcaster.conf sourcetable.dat users.aut groups.aut clientmounts.aut sourcemounts.aut; do
  test -f "${f}.dist" && cp -n "${f}.dist" "$f"
done
dos2unix ntripcaster.conf sourcetable.dat *.aut 2>/dev/null || true
chmod 600 users.aut groups.aut clientmounts.aut sourcemounts.aut
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| configure 缺库 | 依赖不全 | 按包内 README 装 build-essential / 相关库 |
| 解析怪错 | CRLF | `dos2unix` 全部 conf/aut |
| 端口占用 | 2101 已被占 | `ss -lptn | grep 2101`；改 port |
| 无写权限 | 装到系统目录 | 用 `$HOME/ntripcaster` |

## 3. 端到端：最小播发 → 源表 → 订流

### 3.1 主配置

```bash
grep -nE 'port|log|max|security' ntripcaster.conf | head
# 设定：port（常 2101）、日志路径、max 连接；保存为 LF
```

### 3.2 源表 `sourcetable.dat`

按手册列序添加 **STR** 行（字段少一列 → 客户端解析失败）。挂载点名与 ACL **字符级一致**。

```bash
# 例：保留 CAS/NET 头，追加一条 STR（列序以手册为准，勿照抄未核列数的示例）
grep -E '^(CAS|NET|STR)' sourcetable.dat | head
```

### 3.3 账号与 ACL

| 文件 | 内容 |
| --- | --- |
| `users.aut` | `user:password` |
| `groups.aut` | `group:user1,user2` |
| `clientmounts.aut` | 客户端可读挂载点 |
| `sourcemounts.aut` | 源端可推流挂载点 |

```bash
# 教学例（课后立刻改密）：
# echo 'lab:StrongPass_ChangeMe' >> users.aut
# 在 clientmounts.aut / sourcemounts.aut 按手册绑定挂载点
chmod 600 users.aut groups.aut *.aut
```

### 3.4 启动与探活

```bash
# 可执行路径以 install 为准
"$HOME/ntripcaster/bin/ntripcaster" start 2>/dev/null \
  || ./ntripcaster start
"$HOME/ntripcaster/bin/ntripcaster" status 2>/dev/null || true
ss -lptn | grep 2101 || true

# 拉源表（本机有 pygnssutils 时）
gnssntripclient --server 127.0.0.1 --port 2101 --verbosity 2 | tee logs/sourcetable.txt
```

**期望：** 进程在听；源表出现 STR；未授权订流被拒。

### 3.5 授权客户端订流

```bash
gnssntripclient --server 127.0.0.1 --port 2101 \
  --mountpoint LOCAL1 \
  --ntripuser lab --ntrippassword 'StrongPass_ChangeMe' \
  --datatype RTCM --verbosity 2
```

**期望：** 有 RTCM 消息号打印（前提：源端已向该挂载点推流）。

### 3.6 源端推流

源端用 BKG `ntripserver`、接收机 NTRIP Server、或其它推流工具；`sourcemounts.aut` 必须允许该源账号。Caster **不检查** RTCM 语义——内容正确性另验。

### 3.7 中继（语法以手册为准）

```bash
# 示意：把远端挂载点中继到本地 — 确切子命令读包内文档
# relay pull ... 
```

### 3.8 停止 / 重启

```bash
./ntripcaster stop
./ntripcaster restart
```

改 ACL 后不要假设一定热更新：以 status/日志为准；不行就 restart。

## 4. 配置文件字段

| 文件 | 作用 |
| --- | --- |
| `ntripcaster.conf` | 端口、连接数、日志 |
| `sourcetable.dat` | CAS/NET/STR 源表 |
| `users.aut` / `groups.aut` | 账号与组 |
| `clientmounts.aut` | 客户端 ACL |
| `sourcemounts.aut` | 源端 ACL |

| 方向 | 内容 |
| --- | --- |
| 输入 | 上游 NTRIP/TCP、本地推流 |
| 输出 | NTRIP 服务、源表、日志 |
| 不做 | 解码、VRS、TEC |

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 C 播发端 | §3 | 客户端 [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) / [rtklib](./rtklib.md) |
| 落盘科研 | 客户端录盘后 | 路径 A/B（georinex → TEC/ROTI） |
| 单挂载点演示 | 不必上本页 | `gnssserver` |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 源表空 | sourcetable 未部署 / STR 列错 | 对照手册列序；`grep ^STR` |
| 2 | 能连不能订 | clientmounts ACL | 绑定用户↔挂载点 |
| 3 | 奇异解析错 | CRLF | `dos2unix` |
| 4 | 2101 冲突 | 与 gnssserver/BNC 抢端口 | 改 port |
| 5 | 单挂载演示却上全套 | 杀鸡用牛刀 | 换 pygnssutils |
| 6 | 公网默认口令 | 秒被扫 | 强口令；IP 白名单 |
| 7 | 口令文件 world-readable | 权限松 | `chmod 600` |
| 8 | 挂载点名不一致 | 大小写/空格 | 源表与 ACL 逐字核对 |
| 9 | 以为会做 VRS | 产品边界 | 不会；VRS 在网络端 |
| 10 | 日志盘满 | 无轮转 | logrotate；缩 verbosity |
| 11 | IPv4/IPv6 混绑 | 客户端连错族 | 统一监听与客户端 |
| 12 | 改完不生效 | 未写盘/未 restart | 保存后 restart；看 mtime |
| 13 | 源端未推流怪客户端 | 上游空 | 先查 sourcemounts 与源端 |
| 14 | 防火墙未放行 | 端口不通 | 放行 TCP port |
| 15 | 教学口令不轮换 | 事后仍可用 | 课后改密+停服务 |
| 16 | 播发成功≠RTCM 正确 | Caster 不分发语义 | 客户端解码核对消息号 |
| 17 | conf 进 git | 泄密 | gitignore；轮换口令 |
| 18 | Windows 记事本编辑 | CRLF/编码 | Linux/`dos2unix`；UTF-8 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 正式多用户播发 | **BKG NtripCaster** |
| 脚本单挂载点 | pygnssutils `gnssserver` |
| 收流录盘 | BNC |
| 容器化 | 社区 Docker（仍遵 BKG 许可） |

## 8. 相关

[pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · [README](./README.md)
