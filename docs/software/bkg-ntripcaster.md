# BKG NtripCaster · 自建 GNSS 实时播发

目录条目：[`PROJECTS.json` → `BKG-NtripCaster`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bkgcaster>  
手册：<https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/ntripcaster_manual.html> · 下载目录：<https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/> · 列表：[03 GNSS 数据](../../lists/03-gnss-data.md)

## 作用与场景

**它是什么**：BKG **Professional NtripCaster**——在 Linux 上按 NTRIP v1/v2 把多路 GNSS 实时流播给大量客户端（源自 Icecast，GPL）。自 **2024-09** 起免费提供含源码软件包（不含安装运维支持）。

**它解决什么**：你要**自己当播发站**（实验室 CORS、课程演示、转发 SSR），而不是只订阅别人的 caster。

**何时用：** 有 Linux 服务器、需要多挂载点与用户权限。  
**何时不用：** 只拉公开流 → [bnc](./bnc.md) / [pygnssutils](./pygnssutils.md)；只要单挂载点试验 → `gnssserver`（见 pygnssutils 文）往往更轻。  
**不做：** 不解码流内容；不做 VRS / 最近基站。

## 安装

仅 Linux（官网说明）。版本号以 FTP 目录当前包为准：

```bash
# 从 https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/ 下载 ntripcaster-*.tar.bz2
bunzip2 ntripcaster-*.tar.bz2 && tar xf ntripcaster-*.tar
cd ntripcaster-*
./configure --prefix=/usr/local/ntripcaster
make && make install
```

在配置目录把 `*.dist` 拷成正式名（**勿用 Windows 记事本**，避免 CRLF）：

```bash
cp ntripcaster.conf.dist ntripcaster.conf
cp sourcetable.dat.dist sourcetable.dat
cp users.aut.dist users.aut
cp groups.aut.dist groups.aut
cp clientmounts.aut.dist clientmounts.aut
cp sourcemounts.aut.dist sourcemounts.aut
# 配置目录常见为 prefix/conf 或 /etc/ntripcaster（以 README/INSTALL 为准）
```

## 最小可跑命令

**1）改 `ntripcaster.conf`**

至少核对（字段名以模板为准）：

- `server_name`：可解析主机名（手册强调不要只填裸 IP）  
- `port`：常见 `2101`（或同时开 `80`）  
- `encoder_password` / `admin_password` / `oper_password`

**2）源表与权限**

- `sourcetable.dat`：`STR` / `CAS` / `NET` 记录  
- `users.aut` / `groups.aut`：用户与组（可限并发）  
- `clientmounts.aut` / `sourcemounts.aut`：谁能拉 / 谁能推

**3）启停**

```bash
./ntripcaster start
./ntripcaster stop
./ntripcaster restart
# 另有 casterwatch 守护 ntripdaemon（见手册）
```

浏览器：`http://<主机>:<端口>/home` · 管理：`http://<主机>:<端口>/admin`。

**4）客户端冒烟**

用 [BNC](./bnc.md) 或 [pygnssutils](./pygnssutils.md) 指向你的主机/端口/挂载点。

**可选中继（手册思路，参数以当前手册为准）**

```text
relay pull -i user:pass -m /LOCAL1 remote.example:2101/REMOTE0
```

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | NtripServer 推流；或 `relay pull` 拉入的流（caster **不解析** RTCM 语义） |
| 输出 | 挂载点订阅；管理 Web；日日志（access / usage / ntripcaster） |
| 容量量级 | 官网称可支撑约 100+ 源、2000+ 客户端（视硬件与配置） |

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 源表为空 | 流未上线或未登记 | 动态源表常只显示**当前可用**流；查 admin → sources |
| 能推不能拉 | 用户组 / clientmounts 不对 | 按手册串：用户→组→挂载点 |
| 改配置不生效 | 未 rehash / 未重启 | admin 的 rehash（尽量不停流）或 resync（会短暂断流） |
| 端口不通 | 防火墙 / `<1024` 权限 | 先用 `2101`；80 需 root 或端口转发 |
| 期望 VRS | 本软件明确不做 | 换网络 RTK 方案 |
| 只想拉 IGS 流 | 建 caster 过重 | 直接 BNC + 允许的公开 caster |

## 接到哪一步分析

- 实时数据概念 → [数据怎么下](../data-access.md)  
- 客户端拉流 / 落盘 → [bnc](./bnc.md) · [pygnssutils](./pygnssutils.md) · [rtklib](./rtklib.md) `str2str`  
- 落成 RINEX 后 → [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md) · [02](../tutorials/02-gnss-dualfreq-tec.md) / [05](../tutorials/05-scintillation-roti.md)

## 目录指针

- `PROJECTS.json`：`BKG-NtripCaster` · 相关：`BNC`、`Caster-source-FTP`、`ntripcaster-docker-bkg`、`pygnssutils`
