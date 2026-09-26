# galileo-osnma：Galileo OSNMA 导航电文认证（Rust，可 `no_std`）

> 岗位：把 Galileo E1-B I/NAV 页喂进去，判断 **星历/钟差/健康（ADKD0、ADKD12）** 和 **GST-UTC 时间参数（ADKD4）** 是不是 Galileo 真发的。**只做认证**：不解算位置，不测伪距。冲突时以 **上游 README / docs.rs / 本机 `--help`** 为准。

**30 秒概念（零基础）：**

- **OSNMA**（Open Service Navigation Message Authentication）：Galileo 在免费 E1-B 信号里夹带 40 bit/页的密码学数据，接收机据此校验导航电文没被伪造。
- **MAC / 标签（tag）**：用密钥对「电文 + 时间 + 卫星号」算出的短校验码（HMAC-SHA-256 或 CMAC-AES，截短到 40 bit 左右）。标签对得上 ⇒ 电文未被改。
- **TESLA 链**：密钥是一条哈希链 $K_{i}=\mathrm{trunc}(H(K_{i+1}\,\|\,\mathrm{GST}_{i}\,\|\,\alpha))$。卫星**先**发标签、**30 s 后**才公开对应密钥；链根 KROOT 由 ECDSA 公钥签名，公钥再由 Merkle 树根担保。所以：Merkle 根 → 公钥 → KROOT → 每个 TESLA 密钥 → 标签 → 电文。

## 1. 用途边界

| 能做 | 不能做 |
| --- | --- |
| 校验 DSM-KROOT（ECDSA P-256；P-521 需 `p521` feature） | **不是定位解算器**：不出 PVT、不处理伪距/载波 |
| 用 Merkle 根校验空中广播的公钥 DSM-PKR | **不防转发型欺骗（meaconing）**：原样延迟转发的真信号，电文照样认证通过；只能靠接收机时钟/测距一致性发现 |
| TESLA 密钥逐级验证、MACSEQ/ADKD 查表校验 | 不解码电文字段：只返回认证过的**原始比特**（549 bit CED、141 bit 时间参数），物理量自己按 OS SIS ICD 解 |
| ADKD0/4/12 标签累计（≥40 bit 才算认证） | 不做「本地时间 vs GST」偏差检查：调用者给什么 GST 它就信什么（见 §5） |
| 续期/吊销/新 Merkle 树/告警（OAM）等非标称场景 | 不支持热启动（加载已认证 TESLA 密钥）；无 C/Python API（上游路线图） |
| `no_std`、全静态栈分配；嵌入式演示 `osnma-longan-nano` | 不校验页 CRC、不做帧同步：那是接收机/前端的事 |

## 2. 版本与安装

本机 2026-09-26 01:41–02:10 EDT 核实：

| 项 | 值 |
| --- | --- |
| crates.io | **0.11.6**（2026-03-04 04:23 EDT 发布）；总下载 **11559**，近 90 天 **207** |
| 上游 | `daniestevez/galileo-osnma`，默认分支 `main`；tag **v0.11.6** = main 头 **`b6c337b`**（2026-03-04，「update dependencies」），**tag 与 main 无差异** |
| 许可 | `MIT OR Apache-2.0`（GitHub 页只显示 Apache-2.0，以 Cargo.toml 为准）；★89 |
| MSRV / edition | `rust-version = 1.88.0`，edition 2024；本机 rustc **1.98.1** |
| features | 默认 `galmon-osnma` + `osnma-longan-nano`（都拉 `galmon` → **需要 `protoc`** 和 `std`）；另有 `galmon`、`p521`、`std` |
| 规范 | OSNMA SIS ICD v1.1、Receiver Guidelines v1.3 |

```bash
# 只当库用（no_std、无需 protoc）：
cargo add galileo-osnma@0.11.6 --no-default-features
cargo add p256 --features ecdsa,pem   # 读 PEM 公钥用
# 要上游 CLI（galmon-osnma 等）：先装 protoc
git clone https://github.com/daniestevez/galileo-osnma && cd galileo-osnma
PROTOC=/path/to/protoc cargo build --release --bins
```

上游工具（`galileo-osnma/src/bin/`）：`galmon-osnma`（读 Galmon protobuf 流做认证）、`osnma-test-vectors-to-galmon`（官方 CSV 测试向量 → Galmon 流）、`galmon-filter-inav`、`osnma-longan-nano-client`、`galileo-osnma-sizeof`；外加固件 crate `osnma-longan-nano`（GD32VF103 RISC-V）。

**本机实测：** `cargo test --release` → 单元测试 **28 passed**、doctest **7 passed**、0 failed。`galileo-osnma-sizeof`：`Osnma<FullStorage>` = **78352 B**（36 星 + 慢 MAC），`Osnma<SmallStorage>` = **8752 B**（12 星）。临时加 `riscv32imac-unknown-none-elf` 编 `osnma-longan-nano`（embedded profile）15 s 通过：`text 73462 B / bss 32765 B`；`galileo-osnma --no-default-features` 同目标编译通过（即 `no_std` 可用）。真板未烧录。

## 3. 数据与钥匙从哪来

| 材料 | 来源 | 要注册？ |
| --- | --- | --- |
| **OSNMA 测试向量** `Test_vectors.zip`（10.3 MB） | GSC，Receiver Guidelines v1.3 附件：`https://www.gsc-europa.eu/sites/default/files/sites/all/files/Test_vectors.zip` | **否**，直链可下 |
| 测试向量配套公钥/Merkle 树（PKID 1/2/7/8/9，Merkle_tree_1/2/3） | 同一 zip 内 `cryptographic_material/` | 否 |
| **现行**公钥 `.crt`、Merkle 树 `.xml`（上游 README 写 PKID 2，2025-12-10 起） | GSC Products → OSNMA_PUBLICKEY / OSNMA_MERKLETREE | **是**，需 GSC 账号；本文未取得 |
| 实时 I/NAV | Galmon 公共流 `86.82.68.237:10000`；或自有 u-blox 经 Galmon `ubxtool` | 否 |

测试向量 CSV：每行一颗星，`SVID,NumNavBits,NavBitsHEX`，每星 **432000 bit = 1800 页 × 240 bit = 3600 s**，文件名即首页 GST（如 `16_AUG_2023_GST_05_00_01.csv`）。压缩包只写「Receiver Guidelines 附件」，**未说明是否在轨实录**，本文不作断言。

**本文所有「真实」输出都用测试向量 + 包内自带钥匙。** Galmon 实时流：本机试连一次被环境拦下、未获批准，**未测**；u-blox RXM-SFRBX → `ubxtool` → `galmon-osnma` 路径（`just galmon-osnma-ubxtool /dev/ttyACM0 …`）无接收机，**未测**；现行 PKID 2 钥匙需注册，**未取**。

## 4. 上游 CLI：测试向量实跑

```bash
T=Test_vectors; M1=$T/cryptographic_material/Merkle_tree_1
openssl x509 -in $M1/PublicKey/OSNMA_PublicKey_20230803105952_newPKID_1.crt -noout -pubkey > pk1.pem
ROOT=$(./utils/extract_merkle_tree_root.py $M1/MerkleTree/OSNMA_MerkleTree_20230803105953_newPKID_1.xml)
# ROOT = 0E63F552C8021709043C239032EFFE941BF22C8389032F5F2701E0FBC80148B8
target/release/osnma-test-vectors-to-galmon $T/osnma_test_vectors/configuration_1/16_AUG_2023_GST_05_00_01.csv \
  | RUST_LOG=info target/release/galmon-osnma --pubkey pk1.pem --pkid 1 --merkle-root $ROOT
```

真实输出（全部在 **stderr**，stdout 为空；节选、时间戳省略）：

```text
INFO  galileo_osnma::subframe] starting collection of new subframe (GST Gst { wn: 1251, tow: 277201 })
INFO  galileo_osnma::osnma] no valid TESLA key for the chain in force. unable to validate MACK key
INFO  galileo_osnma::dsm] completed DSM with id = 7, size = 104 bytes
INFO  galileo_osnma::osnma] verified KROOT with public key id 1
INFO  galileo_osnma::osnma] current NMA header: NmaHeader { nma_status: Test, chain_id: 3, chain_and_pubkey_status: Nominal }
INFO  galileo_osnma::osnma] new TESLA key Key { … gst_subframe: Gst { wn: 1251, tow: 277230 } … } successfully validated by Key { … tow: 277170 … }
INFO  galmon_osnma] new CED and status for E02 authenticated (authbits = 40, GST = Gst { wn: 1251, tow: 277230 })
INFO  galmon_osnma] new CED and status for E05 authenticated (authbits = 440, GST = Gst { wn: 1251, tow: 277200 })
INFO  galmon_osnma] new timing parameters for E02 authenticated (authbits = 40, GST = Gst { wn: 1251, tow: 277290 })
```

整小时（26 星 × 1800 页，3.38 MB Galmon 流）**0.54 s** 跑完：stderr 25870 行，`galmon_osnma` 认证事件 160 条（CED 138、时间参数 22）。上游 `utils/run_test_vectors.sh` 跑全部 **28** 个场景 24 s，出现的 ERROR/WARN 都是脚本注释里「预期会出现」的类型（`CPKS is new Merkle tree`、`could not verify public key: Invalid`、`received OSNMA Alert Message; deleting all cryptographic material` 等）。

## 5. 可编译示例（直接读测试向量 CSV，不需要 protoc）

`Cargo.toml`：`galileo-osnma = { version = "0.11.6", default-features = false }`、`p256 = { version = "0.13", features = ["ecdsa","pem"] }`、`hex = "0.4"`。`src/main.rs`（本机编译通过）：

```rust
use galileo_osnma::{Gst, InavBand, Osnma, PublicKey, Svn, storage::FullStorage};
use p256::pkcs8::DecodePublicKey;

fn main() {
    let a: Vec<String> = std::env::args().collect(); // csv pem pkid merkle_hex wn tow
    let pem = std::fs::read_to_string(&a[2]).unwrap();
    let vk = p256::ecdsa::VerifyingKey::from_public_key_pem(&pem).unwrap();
    let pk = PublicKey::from_p256(vk, a[3].parse().unwrap()).force_valid();
    let root: [u8; 32] = hex::decode(&a[4]).unwrap().try_into().unwrap();
    let mut osnma = Osnma::<FullStorage>::from_merkle_tree(root, Some(pk), false);
    let gst0 = Gst::new(a[5].parse().unwrap(), a[6].parse().unwrap());
    let rows: Vec<(u8, Vec<u8>)> = std::fs::read_to_string(&a[1]).unwrap().lines().skip(1)
        .map(|l| { let f: Vec<&str> = l.split(',').collect();
                   (f[0].parse().unwrap(), hex::decode(f[2]).unwrap()) }).collect();
    let mut first = None;
    for k in 0..1800 { // 每 SV 1800 页 × 2 s
        let gst = gst0.add_seconds(2 * k);
        for (sv, d) in &rows {
            let page = &d[k as usize * 30..][..30]; // 一页 240 bit = 偶半页 + 奇半页
            let bit = |i: usize| (page[i / 8] >> (7 - i % 8)) & 1;
            let (mut word, mut osnma_field) = ([0u8; 16], [0u8; 5]);
            for (j, i) in (2..114).chain(122..138).enumerate() { word[j / 8] |= bit(i) << (7 - j % 8); }
            for (j, i) in (138..178).enumerate() { osnma_field[j / 8] |= bit(i) << (7 - j % 8); }
            if word[0] >> 2 == 63 { continue; } // dummy 字
            let svn = Svn::try_from(*sv).unwrap();
            osnma.feed_inav(&word, svn, gst, InavBand::E1B);
            osnma.feed_osnma(&osnma_field, svn, gst);
        }
        if first.is_none() && Svn::iter().any(|s| osnma.get_ced_and_status(s).is_some()) {
            first = Some(2 * k + 2);
        }
    }
    let ced: Vec<_> = Svn::iter().filter_map(|s| osnma.get_ced_and_status(s).map(|d| (s, d))).collect();
    let tim = Svn::iter().filter(|&s| osnma.get_timing_parameters(s).is_some()).count();
    println!("first CED auth after {:?} s; CED SVs = {}; timing SVs = {}", first, ced.len(), tim);
    for (s, d) in ced.iter().take(3) {
        let iod = d.data()[..10].iter().fold(0u16, |x, b| x << 1 | *b as u16);
        println!("{s}: IODnav={iod} authbits={} GST={:?}", d.authbits(), d.gst());
    }
}
```

```text
$ ./mini configuration_1/16_AUG_2023_GST_05_00_01.csv pk1.pem 1 0E63F5…48B8 1251 277201
first CED auth after Some(90) s; CED SVs = 24; timing SVs = 22
E02: IODnav=82 authbits=1080 GST=Gst { wn: 1251, tow: 280770 }
E03: IODnav=76 authbits=47880 GST=Gst { wn: 1251, tow: 280770 }
E04: IODnav=82 authbits=880 GST=Gst { wn: 1251, tow: 280770 }
```

**结果汇总**（首次认证耗时按数据内 GST，从首页起算；本机扩展版程序另统计 KROOT/TESLA 次数、字段）：

| 场景 | KROOT 验证 | TESLA 密钥通过 | DSM-PKR 验证 | CED 认证 SV（ADKD0/12） | 时间参数 SV（ADKD4） | 首次认证 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| configuration_1（26 星，PKID 1） | 1 | 119 | 0 | **24** | **22** | CED **+90 s**，时间 **+120 s** |
| 同上 `only_slowmac=true`（仅 ADKD12） | 1 | 119 | 0 | **24** | 0 | 23 星 **+390 s**，E36 +810 s |
| configuration_2（26 星，PKID 2） | 3 | 106 | 3 | **25** | **17** | CED **+450 s**，时间 +480 s |
| configuration_2，**只给 Merkle 根**（空中取公钥） | 3 | 106 | 3 | 25 | 17 | +450 s |

认证过的字段示例（configuration_1 首次）：E02 字 1 `IODnav=76`、`t0e=276000 s`；E05/E27 `IODnav=74`、`t0e=274800 s`；ADKD4 时间参数里 `ΔtLS = 18 s`（字 6：A0 32 bit、A1 **24** bit、ΔtLS 8 bit）。慢 MAC 晚约 300 s：ADKD12 的密钥延迟 10 个子帧才公开。

## 6. I/O 表

| 方向 | 接口 | 形状 / 单位 |
| --- | --- | --- |
| 入 | `feed_inav(&[u8;16], Svn, Gst, InavBand)` | 128 bit I/NAV 字 = 偶半页 data 112 bit + 奇半页 data 16 bit；`Gst` 为该**页起点** |
| 入 | `feed_osnma(&[u8;5], Svn, Gst)` | 奇半页 40 bit OSNMA 字段（全 0 自动忽略） |
| 入 | `from_merkle_tree([u8;32], Option<PublicKey<Validated>>, bool)` / `from_pubkey(...)` | Merkle 根 256 bit；公钥 P-256（或 P-521）+ PKID；`bool` = 只做慢 MAC |
| 出 | `get_ced_and_status(Svn)` → `Option<NavMessageData>` | 549 bit（字 1–5 去掉类型号拼接）、`authbits()`、`gst()` |
| 出 | `get_timing_parameters(Svn)` | 141 bit（字 6 的 99 bit + 字 10 的 42 bit） |
| 出 | `log` 日志 | KROOT/TESLA/标签失败等只走 `log`，无错误返回值 |
| CLI 入 | `galmon-osnma --pubkey PEM --pkid N --merkle-root HEX [--pubkey-p521 HEX] [--slow-mac-only]` | stdin：Galmon protobuf 传输流 |
| CLI 出 | stderr（env_logger，默认 info） | `new CED and status for Exx authenticated (authbits = …, GST = …)` |

## 7. 错误用例（本机实测；输入均为测试向量**合成**篡改）

| 用例（合成） | 库的行为 / 日志原文 |
| --- | --- |
| 翻转 E02 某个字 1 页的 1 bit（page 25，bit 40） | `E02 InavCed at Gst { wn: 1251, tow: 277260 } tag0 wrong (auth by E02)`、`SlowMac … tag4 wrong`；该子帧不计 authbits，E02 仍靠前一子帧的正确电文在 +90 s 认证，**被篡改的版本从不返回** |
| 每个字 1 页都翻同一 bit（持续伪造星历） | 每子帧 `tag0 wrong`，E02 **始终不认证**（24→23 星），其余星不受影响 |
| 错误公钥（PKID 2 的钥当 PKID 1） | `could not verify KROOT: WrongEcdsa` → 0 认证 |
| 公钥对、PKID 填错 | `could not verify KROOT because public key with id 1 is not available` → 0 认证 |
| 只给错误 Merkle 根（configuration_2） | `could not verify public key: Invalid` + `could not verify KROOT because no public key is available` → 0 认证 |
| 公钥对 + Merkle 根错 | DSM-PKR 报 `Invalid`，但**已给的公钥照用**，认证照常（25 星） |
| 丢 1 个子帧（全部星，tow 277230 起 30 s） | 无报错；TESLA 通过 119→118，首次认证 +90→**+150 s**（丢 277260 则 +180 s） |
| GST 偏 +2 s / +10 s（子帧内错位） | `block 2 already stored, but its contents differ…`，KROOT 都拼不出，0 认证 |
| GST 偏 ±30 s / +3600 s（整子帧错，或旧数据改时戳重放） | KROOT 仍验过，但每个密钥 `could not validate TESLA key …`（2150 条），0 认证 |
| 原样重放同一小时（GST 倒退） | `got a key in MACK which is older than our current valid key`，重放段 MACK 全拒；首遍已认证的数据仍留在存储里 |

## 8. 坑

1. **默认 features 要 `protoc`**：`cargo build` 报 `Could not find protoc`。只用库就 `default-features = false`，本机无 protoc 也能编。
2. **结论只在日志里**：标签失败、KROOT 失败都不返回 `Err`，只打 `log`；要把失败计入告警，得自己装 logger 或比较 `get_*` 的返回。
3. **GST 由你负责**：库没有「本地时钟偏差上限」参数。Receiver Guidelines 要求先保证时间同步（ADKD0/4 约 30 s 量级、只用慢 MAC 可放宽）；时间不可信时用 `only_slowmac=true`，并在接收机侧另做检查。
4. **不查 CRC**：翻 1 bit 的页若过了你的 CRC 过滤，库只能靠标签失败发现；前端必须先按 OS SIS ICD 做 CRC 与奇偶页配对。
5. **dummy 字 / 告警页要自己丢**：上游 CLI 丢类型 63；告警页 OSNMA 字段无效，Galmon 数据里无法识别。
6. **只给 Merkle 根要等 DSM-PKR**：公钥每 6 h（GST 00/06/12/18 时）才播；configuration_1 这一小时里没有 PKR，只给根就 0 认证。
7. **首次认证不是即刻**：至少要收齐 DSM-KROOT（多星多子帧拼块）+ 下一子帧的密钥；本测 90–450 s，慢 MAC 再多约 300 s。无热启动。
8. **`authbits` 是累计量**：≥40 bit 才返回；E03 可累积到 47880，别当成标签数。
9. **P-521 与 CLI**：`--pubkey` 只收 P-256 PEM，P-521 走 `--pubkey-p521 <SEC1 hex>`；longan-nano 固件关了 `p521` 以省 flash。
10. **Galmon 流乱序**：上游 CLI 会丢旧子帧的字并修 Galmon 的 TOW bug；自己接接收机时按页起点 GST 顺序喂。
11. **现行钥匙要注册**：GSC 公钥/Merkle 树需账号；公开测试向量的钥匙不能用于现网数据。

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 嵌入式 / 接收机固件里做 OSNMA（`no_std`、静态内存） | **galileo-osnma** |
| Python 里做 OSNMA 研究、回放日志 | Algafix/OSNMA（PROJECTS 已登记，暂无手册） |
| 接收机自带 OSNMA 状态（Septentrio、u-blox SEC-OSNMA） | [septentrio-gnss-driver](./septentrio-gnss-driver.md) 的 `osnma.mode`；[ublox](./ublox.md)（SEC-OSNMA 在 proto31 仍 Unknown） |
| 抓 u-blox RXM-SFRBX 原始子帧 | [pyubx2](./pyubx2.md) / [ublox](./ublox.md)，再自行拼成 I/NAV 字喂本库 |
| 从 IF 采样到电文（含 OSNMA 模块）的软件接收机 | [fgi-gsrx](./fgi-gsrx.md) |
| GST/UTC/GPST 时间换算 | [hifitime](./hifitime.md)；星座/SV 定义 [gnss-rs](./gnss-rs.md) |
| 各家二进制协议总览 | [gnss-protos](./gnss-protos.md) |

参考：OSNMA SIS ICD v1.1、Receiver Guidelines v1.3（GSC 官网 PDF）；docs.rs/galileo-osnma。
