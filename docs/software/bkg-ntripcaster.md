# BKG NtripCaster · 专业 NTRIP 播发操作手册

目录：[`PROJECTS.json` → `BKG-NtripCaster`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bkgcaster> · FTP <https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/> · 手册 <https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/ntripcaster_manual.html> · GPL-3.0 · 本机验证 **2.0.49**（`configure`/`make install`/`ntripcaster start` + BKG `ntripserver` 推流 + [pygnssutils](./pygnssutils.md) 订流）

> 岗位：在 **Linux** 上做多客户端 NTRIP v1/v2 **播发**（源表、用户组、挂载点 ACL、中继）。只分发字节，**不解码** RTCM，不做 VRS / 最近站。参数以包内 `README`/`INSTALL`、`*.dist` 注释与 `ntripcaster_manual.html` 为准。口令禁止进 git。

## 1. 用途与边界

**做：** 多用户多挂载点播发；NTRIP 2.0 源端推流 / 1.0 `encoder_password` 推流；中继远端流到本地挂载点；与 [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) / [rtklib](./rtklib.md) / 手簿联调。

**不做：** 五分钟单挂载点演示 → `gnssserver`（[pygnssutils](./pygnssutils.md)）；多流 GUI 收流录 RINEX → [bnc](./bnc.md)；TEC/ROTI/PPP；Caster「自动选站 / VRS」；校验 RTCM CRC（内容对错另验）。

一句话：正式/课程 **播发站**；电离层产品仍在客户端落盘转 RINEX 之后。

## 2. 安装（Linux，本机 2.0.49）

FTP 目录以官网为准（当前常见 `ntripcaster-2.0.49.tar.bz2`；亦有 `.sha256`）。

```bash
mkdir -p ~/src && cd ~/src
curl -fsSL -O https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/ntripcaster-2.0.49.tar.bz2
curl -fsSL -O https://igs.bkg.bund.de/root_ftp/NTRIP/software/caster/ntripcaster-2.0.49.tar.bz2.sha256
sha256sum -c ntripcaster-2.0.49.tar.bz2.sha256
# 期望：ntripcaster-2.0.49.tar.bz2: OK

tar xjf ntripcaster-2.0.49.tar.bz2
cd ntripcaster-2.0.49
./configure --prefix="$HOME/ntripcaster"
# 结尾期望：Ok, everything seems ok. Now do 'make'.
make -j"$(nproc)"
make install
ls "$HOME/ntripcaster/bin/ntripcaster" "$HOME/ntripcaster/sbin/ntripdaemon"
```

| 前缀布局（非 `--enable-fsstd`） | 路径 |
| --- | --- |
| 启动脚本 | `$prefix/bin/ntripcaster`、`casterwatch` |
| 守护进程 | `$prefix/sbin/ntripdaemon` |
| 配置 | `$prefix/conf/*.dist` |
| 日志 / 运行时 | `$prefix/logs`、`$prefix/var` |
| HTML 模板 | `$prefix/templates` |

系统目录安装：`./configure --enable-fsstd`（二进制常进 `/usr/sbin`，配置 `/etc/ntripcaster`）——需 root；教学优先 `$HOME/ntripcaster`。

```bash
CONF="$HOME/ntripcaster/conf"
cd "$CONF"
for f in ntripcaster.conf sourcetable.dat users.aut groups.aut clientmounts.aut sourcemounts.aut; do
  test -f "${f}.dist" && cp -n "${f}.dist" "$f"
done
# Windows 编辑过则：
# dos2unix ntripcaster.conf sourcetable.dat *.aut
chmod 600 users.aut groups.aut clientmounts.aut sourcemounts.aut
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `configure` 缺编译器 | 无 gcc/make | `build-essential` |
| `sha256sum` 失败 | 下成 HTML 错误页 | `ls -l` 看体积（约 266K）；换镜像/重下 |
| 装到 `/usr/local` 无写权限 | 默认 prefix | `--prefix="$HOME/ntripcaster"` |
| 解析怪错 | CRLF | `dos2unix` 全部 conf/aut |
| `port 80` 起不来 | 特权端口 | 注释掉 `port 80`，只用 `2101`（或 root/`setcap`） |

`ntripdaemon` 帮助（本机）：

```text
NtripCaster - Version 2.0.49
Usage:
ntripcaster [-P <port>] [-p password] [-l <file>] [-d <directory>] [-c <configfile>] [-b]
	-d: Use this directory as the location of the config files
	-b: Force NtripCaster server into the background
```

（日常用包装脚本 `$prefix/bin/ntripcaster start|stop|restart`，它会调 `casterwatch` → `ntripdaemon -d $CONF -b`。）

## 3. 端到端：最小播发 → 推流 → 源表出现 STR → 订流

下列为本机 **2.0.49** 真跑（2026-09-24）。口令仅教学，课后立刻改。

### 3.1 改主配置 `ntripcaster.conf`

必改（安装后 `*.dist` 里路径已按 prefix 写好，仍要改主机名与口令）：

```bash
grep -nE '^(server_name|port |logdir|pidfilename|templatedir|encoder_password|admin_password|oper_password|console_mode|max_)' \
  "$CONF/ntripcaster.conf"
```

| 键 | 含义 | 本机做法 |
| --- | --- | --- |
| `server_name` | **主机名**（禁止写 IP）；须能解析到本机 | `getent hosts "$(hostname)"`；不行就写 `/etc/hosts` |
| `port` | 监听端口，可多行 | 保留 `2101`；无 root 时注释 `port 80` |
| `encoder_password` | **NTRIP 1.0 源端**口令 | 改强口令 |
| `admin_password` / `oper_password` | Telnet/管理，非挂载点 ACL | 改强口令 |
| `max_clients` / `max_sources` / `throttle` | 连接与带宽上限 | 按机器改 |
| `logdir` / `pidfilename` / `templatedir` | 日志、PID、模板 | 保持 `$prefix/...` |
| `console_mode` | 0/1 控制台；**3=后台** | 脚本启动用 3 |
| `sourcetablefile` | 源表文件名 | 默认 `sourcetable.dat` |

`*.dist` 里还有示例中继（默认注释）：

```text
#relay pull -i user1:pass1 -m /TITZ0 129.217.182.51:2101/TITZ0
```

### 3.2 源表 `sourcetable.dat`

列定义见 <http://software.rtcm-ntrip.org/wiki/Sourcetable> 与包内手册。**动态源表**只返回**当时在线**的 STR（无源 → 客户端看不到该挂载点）。不要手写 `ENDSOURCETABLE`（Caster 会追加）。

教学最小三行（列数与 `*.dist` 中 STR 一致，19 段）：

```bash
cat > "$CONF/sourcetable.dat" <<'EOF'
CAS;127.0.0.1;2101;LAB;LocalLab;0;XXX;0.00;0.00;Lab caster
NET;LABNET;LocalLab;B;N;none;none;lab@example.invalid;none
STR;LOCAL1;LabMount;RTCM 3.0;1004(1);2;GPS;LABNET;XXX;0.00;0.00;0;0;none;none;B;N;0;lab
EOF
# STR 字段 16（例中 `B`）只是「是否需认证」的客户端提示；
# 真正 ACL 只看 clientmounts.aut（上游手册原文结论）。
```

### 3.3 账号与 ACL

| 文件 | 语法（见各文件头注释） |
| --- | --- |
| `users.aut` | `user:password` |
| `groups.aut` | `group:user1,user2` 可选 `[:max]` / `[:ipN]` |
| `clientmounts.aut` | `/MOUNT:group1,...`；**必须**限制 `/admin`、`/oper` |
| `sourcemounts.aut` | 源端可推的 `/MOUNT:group...`；`default:` / `all` 见注释 |

```bash
cat > "$CONF/users.aut" <<'EOF'
lab:StrongPass_ChangeMe
src:SourcePass_ChangeMe
adminlab:lab_adm_ChangeMe
EOF
cat > "$CONF/groups.aut" <<'EOF'
clients:lab
sources:src
admins:adminlab
EOF
cat > "$CONF/clientmounts.aut" <<'EOF'
/admin:admins
/oper:admins
/LOCAL1:clients
EOF
cat > "$CONF/sourcemounts.aut" <<'EOF'
/LOCAL1:sources
EOF
chmod 600 "$CONF"/*.aut
```

### 3.4 启动

```bash
"$HOME/ntripcaster/bin/ntripcaster" start
ss -lptn | grep 2101
```

**本机真实启动横幅：**

```text
Starting Ntrip caster...
NtripCaster Version 2.0.49 Initializing...
NtripCaster comes with NO WARRANTY, to the extent permitted by law.
You may redistribute copies of NtripCaster under the terms of the
GNU General Public License.
For more information about these matters, see the file named COPYING.
Starting thread engine...
```

**本机真实日志（`$prefix/logs/ntripcaster-YYMMDD.log`）：**

```text
[24/Sep/2026:06:39:18] [0:Main Thread] Trying to fork
[24/Sep/2026:06:39:18] [0:Main Thread] Detached (pid: ...)
[24/Sep/2026:06:39:18] [0:Main Thread] Starting main connection handler...
[24/Sep/2026:06:39:18] [0:Main Thread] Listening on port 2101...
[24/Sep/2026:06:39:18] [0:Main Thread] Using 'cursor' as servername...
[24/Sep/2026:06:39:18] [0:Main Thread] Server limits: 1000 clients, 1000 clients per source, 40 sources, 2 admins
[24/Sep/2026:06:39:18] [0:Main Thread] WWW Admin interface accessible at http://cursor:2101/admin
[24/Sep/2026:06:39:18] [0:Main Thread] Starting Calender Thread...
[24/Sep/2026:06:39:18] [0:Main Thread] Starting relay connector thread...
```

`ss` 期望：`0.0.0.0:2101` 上有 `ntripdaemon`。

### 3.5 尚无源：拉源表（只有 CAS/NET）

```bash
curl -sS -D - --max-time 5 \
  -H 'User-Agent: NTRIP lab/1.0' -H 'Ntrip-Version: Ntrip/2.0' \
  -o /tmp/st.raw 'http://127.0.0.1:2101/'
head -n 5 /tmp/st.raw
```

**本机真实响应头 / 体（无源时 STR 不出现）：**

```text
HTTP/1.1 200 OK
Ntrip-Version: Ntrip/2.0
Server: NTRIP BKG Caster/2.0.49
Content-Type: gnss/sourcetable

CAS;127.0.0.1;2101;LAB;LocalLab;0;XXX;0.00;0.00;Lab caster
NET;LABNET;LocalLab;B;N;none;none;lab@example.invalid;none
ENDSOURCETABLE
```

同效 CLI：

```bash
gnssntripclient --server 127.0.0.1 --port 2101 --verbosity 2 --timeout 5 --retries 1
```

**本机：** `Sourcetable retrieved`；body 含同上 CAS/NET（有源后才含 STR）。

### 3.6 源端推流（BKG `ntripserver`，NTRIP 2.0）

另取 FTP `NTRIP/software/ntripserver.zip`，`make` 出 `./ntripserver`。把任意字节流（串口/TCP/文件）推到挂载点——Caster **不验** RTCM。

```bash
# 例：本机 TCP 泵 9101 → 推到 LOCAL1（用户 src 须在 sourcemounts）
./ntripserver -M 2 -H 127.0.0.1 -P 9101 \
  -O 1 -a 127.0.0.1 -p 2101 -m LOCAL1 \
  -n src -c 'SourcePass_ChangeMe' -R 5
```

| 旗标 | 含义 |
| --- | --- |
| `-M 2` | 输入=TCP 客户端连上游 |
| `-O 1` | 输出=NTRIP 2.0 HTTP POST |
| `-a/-p/-m` | 目的 Caster 主机/端口/挂载点（无前导 `/`） |
| `-n/-c` | NTRIP 2.0 源用户/口令（对 `users.aut`） |
| `-O 3` + `-c` | NTRIP 1.0：口令走 Caster 的 `encoder_password` |

**本机真实推流握手：**

```text
Destination caster request:
POST /LOCAL1 HTTP/1.1
Host: 127.0.0.1
Ntrip-Version: Ntrip/2.0
User-Agent: NTRIP NtripServerPOSIX/1.10685
Authorization: Basic ...
Transfer-Encoding: chunked

Destination caster response:
HTTP/1.1 200 OK
Server: NTRIP BKG Caster/2.0.49

transfering data ...
```

**Caster 日志：**

```text
Accepted encoder on mountpoint /LOCAL1 from 127.0.0.1. 1 sources connected
```

此后源表出现 STR：

```text
STR;LOCAL1;LabMount;RTCM 3.0;1004(1);2;GPS;LABNET;XXX;0.00;0.00;0;0;none;none;B;N;0;lab
ENDSOURCETABLE
```

接收机 NTRIP Server / BNC 「上传」同理：挂载点名与 `sourcemounts.aut` 字符级一致。

### 3.7 鉴权与订流

```bash
# 无凭证 → 401
curl -sS -D - --max-time 5 -o /dev/null \
  -H 'User-Agent: NTRIP lab/1.0' 'http://127.0.0.1:2101/LOCAL1'
# 期望头：HTTP/1.1 401 Unauthorized + WWW-Authenticate: Basic realm="/LOCAL1"

# 有用户但无源（或非 NTRIP UA）→ 日志常见 Not authorized / No NTRIP client / 403
# 正式客户端：
gnssntripclient --server 127.0.0.1 --port 2101 \
  --mountpoint LOCAL1 \
  --ntripuser lab --ntrippassword 'StrongPass_ChangeMe' \
  --datatype RTCM --verbosity 2 --timeout 5 --retries 1
```

**本机真实（已推流）：**

```text
Streaming RTCM data from 127.0.0.1:2101/LOCAL1 ...
```

Caster：`Accepted http client ... on mountpoint [/LOCAL1]. 1 clients connected`。

> 本机教学泵推的是**假字节**时，客户端会刷 `RTCM3 message invalid - failed CRC`——这正好说明：**Caster 只搬字节，不保证 RTCM 合法**。真接收机/BNC 录盘后再验消息号。

录盘与多流 GUI → [bnc](./bnc.md)；脚本探活 → [pygnssutils](./pygnssutils.md)。

### 3.8 中继（语法来自上游手册 / `*.dist`，非臆造）

写入 `ntripcaster.conf` 或管理控制台（启动后 `help`）：

```text
relay pull -i user:pass -m /LOCAL_REMOTE 203.0.113.10:2101/REMOTE0
```

含义（手册）：从远端 `REMOTE0` 拉流，挂到本地 `/LOCAL_REMOTE`。亦支持无 NTRIP、纯 IP:port 拉流（见 `ntripcaster_manual.html`「Operating…」）。改完 `rehash` 或 `ntripcaster restart`。

### 3.9 停止 / 重启 / 多实例

```bash
"$HOME/ntripcaster/bin/ntripcaster" stop
# 期望：Stopping Ntrip caster...
"$HOME/ntripcaster/bin/ntripcaster" restart
# 多实例（≥2.0.10）：conf 下建子目录；ntripcaster start <dirname>
# 并改该实例 pid/watchdog 文件名（见包内 README）
```

改 ACL 后不要假设一定热更新：看日志；不行就 `restart`。Web：`http://<host>:2101/home`、`/admin`（须 ACL）。

## 4. 配置文件与 I/O

| 文件 | 作用 |
| --- | --- |
| `ntripcaster.conf` | 端口、限额、口令、日志、中继、别名 |
| `sourcetable.dat` | CAS/NET/STR；动态表过滤离线 STR |
| `users.aut` / `groups.aut` | 账号与组 |
| `clientmounts.aut` | 客户端可读挂载点（含 `/admin`） |
| `sourcemounts.aut` | 源端可推挂载点 |

| 方向 | 内容 |
| --- | --- |
| 输入 | NTRIP/TCP 推流、`relay pull`、本地源 |
| 输出 | NTRIP 服务、动态源表、`logs/ntripcaster-*.log` / `access-*.log` / `usage-*.log` |
| 不做 | 解码、VRS、TEC |

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 C 播发端 | §3 | 客户端 [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) / [rtklib](./rtklib.md) |
| 落盘科研 | 客户端录盘后 | 路径 A/B（[georinex](./georinex.md) → TEC/ROTI） |
| 单挂载点演示 | 不必上本页 | `gnssserver` |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 源表只有 CAS/NET，无 STR | 动态表：挂载点无在线源 | 先推流 / `relay`；再拉源表 |
| 2 | 能连不能订（401） | `clientmounts` 未绑用户组 | `/LOCAL1:clients` + `groups.aut` |
| 3 | 口令对仍 403 / 无数据 | 源端未推或已死 | 看日志 `Accepted encoder`；`usage` 带宽 |
| 4 | 日志 `No NTRIP client` | curl 缺 NTRIP UA | 用 `gnssntripclient` / 加 `User-Agent: NTRIP ...` |
| 5 | 奇异解析错 | CRLF | `dos2unix` |
| 6 | 2101 冲突 | 与 `gnssserver`/BNC 抢端口 | `ss -lptn`；改 `port` |
| 7 | `port 80` bind 失败 | 非 root | 删/注释 `port 80` |
| 8 | `server_name` 异常 / 难连 | 写成 IP 或不解析 | 主机名 + `/etc/hosts` |
| 9 | `/admin` 裸奔 | `clientmounts` 空组未锁 | `/admin:admins`；强管理口令 |
| 10 | 公网默认 `letmein` | `*.dist` 默认口令 | 全改；防火墙；IP ACL |
| 11 | 口令文件 world-readable | 权限松 | `chmod 600` |
| 12 | 挂载点名不一致 | 大小写/漏 `/` | 源表 STR 名与 ACL `/NAME` 逐字核对 |
| 13 | 以为会做 VRS | 产品边界 | 不会；VRS 在网络端 |
| 14 | 播发成功但 CRC 刷屏 | Caster 不验 RTCM | 查上游设备；换真 RTCM |
| 15 | 改完不生效 | 未写盘/未 restart | 保存后 restart；看 mtime |
| 16 | 日志盘满 | 无轮转 | logrotate；降 `logfiledebuglevel` |
| 17 | conf/aut 进 git | 泄密 | gitignore；轮换口令 |
| 18 | 单挂载演示却上全套 | 杀鸡用牛刀 | 换 [pygnssutils](./pygnssutils.md) `gnssserver` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 正式多用户播发 / 中继 | **BKG NtripCaster** |
| 脚本单挂载点 | [pygnssutils](./pygnssutils.md) `gnssserver` |
| 收流录盘 / 多流 GUI | [bnc](./bnc.md) |
| 源端推流工具 | BKG `ntripserver`（同 FTP `NTRIP/software/`） |
| 容器化 | 社区 Docker（仍遵 BKG 许可；配置文件同本页） |

## 8. 相关

[pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md) · [README](./README.md)
