# BKG NtripCaster

目录：[`PROJECTS.json` → `BKG NtripCaster`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/caster> · 手册/下载见 BKG NTRIP FTP `NTRIP/software/NtripCaster/` · GPL

## 用途

- BKG **Professional NtripCaster**：Linux 上按 NTRIP v1/v2 向多客户端播发 GNSS 实时流。
- 解决「自己当播发站」（实验室 CORS、课程演示、转发 SSR）。
- **不做**：解码流内容；不做 VRS/最近基站。
- 只订阅公开流 → [bnc](./bnc.md)/[pygnssutils](./pygnssutils.md)；单挂载点试验 → `gnssserver` 更轻。

## 安装

仅 Linux（以官网说明为准）。版本以 FTP 当前包为准：

```bash
# 下载 ntripcaster-*.tar.bz2 后：
bunzip2 ntripcaster-*.tar.bz2 && tar xf ntripcaster-*.tar
cd ntripcaster-*
./configure --prefix=/usr/local/ntripcaster
make && make install
```

配置目录把 `*.dist` 拷成正式名（**勿用 Windows 记事本**，避免 CRLF）：

```bash
cp ntripcaster.conf.dist ntripcaster.conf
cp sourcetable.dat.dist sourcetable.dat
cp users.aut.dist users.aut
cp groups.aut.dist groups.aut
cp clientmounts.aut.dist clientmounts.aut
cp sourcemounts.aut.dist sourcemounts.aut
```

## 快速上手

```bash
# 1) 编辑 ntripcaster.conf：端口、日志、最大用户等
# 2) 编辑 sourcetable.dat：挂载点行（STR/CAS/NET）
# 3) 编辑 users.aut / groups.aut / *mounts.aut：账号与挂载点 ACL
# 4) 启动
./ntripcaster start
./ntripcaster status   # 若版本支持
# 5) 客户端探活
gnssntripclient --server 127.0.0.1 --port 2101 --verbosity 2
# 或 BNC 拉本机源表

# 停止 / 重启
./ntripcaster stop
./ntripcaster restart
```

中继示例（语法以手册为准）：

```bash
relay pull -i user:pass -m /LOCAL1 remote.example:2101/REMOTE0
```

**预期：** 进程起来；源表可拉；授权用户能订挂载点；未授权被拒。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | 上游 NTRIP/TCP 源、本地推流端 |
| 输出 | 对客户端的 NTRIP 服务、源表、日志 |
| 配置 | conf、sourcetable、*.aut |

## 常用参数

| 文件/项 | 作用 |
|---|---|
| `ntripcaster.conf` | 监听端口、连接数、日志路径 |
| `sourcetable.dat` | 源表（客户端看到的挂载点目录） |
| `users.aut` / `groups.aut` | 用户与组 |
| `clientmounts.aut` / `sourcemounts.aut` | 客户端/源端挂载点权限 |
| `ntripcaster start\|stop\|restart` | 进程控制 |

## 接到工作流哪一步

- 路径 C 的「播发端」；客户端用 [bnc](./bnc.md)/[pygnssutils](./pygnssutils.md)/[rtklib](./rtklib.md)
- 落盘科研仍回 A/B

## 常见问题

| 现象 | 处理 |
|---|---|
| 源表空 | sourcetable 未装或格式错；查日志 |
| 能连不能订 | clientmounts ACL；用户组 |
| CRLF 配置怪 | `dos2unix` 配置文件 |
| 端口占用 | 与 `gnssserver`/其它服务错开 2101 |
| 只要单挂载点演示 | 优先 [pygnssutils](./pygnssutils.md) `gnssserver` |
| 公网暴露 | 强口令、防火墙、TLS（若手册支持） |

## 相关工具

[bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [rtklib](./rtklib.md)

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
