# TropDS · 对流层延迟格网 AI 降尺度（U-Net）操作手册

目录：[`PROJECTS.json`](../../PROJECTS.json) → `TropDS` · 上游 <https://github.com/Sardingfish/TropDS> · tip **`6bb9ef0`**（2026-07-11）· ★**1** · forks **0** · 许可 **BSD-3-Clause**（仓内 `LICENSE`，GitHub API 同；README 徽章链接写成 MIT，以 LICENSE 为准）· 语言 **Python / PyTorch**（6 个 `.py` 共 **2104** 行）· 论文 Ding et al., *Journal of Geodesy* 2026 · 无 PyPI、无测试、**仓内无数据**

本机验证（**2026-09-26 01:49–01:58 EDT**）：Python **3.11.16** venv，torch **2.14.0+cpu** / numpy **2.4.6**，无 GPU。预训练权重从作者 Google Drive 下载（**130852672** B，实为 RAR5 加密包），用作者在 issue #1 公布的密码解出 `best_model.pth`（**150007202** B）；原样 `inference.py` 在 CPU 上 3.6 s 跑完一张 180×360 格网。输入用 TU Wien VMF3 1° 格网 2024-01-01 00 UTC 的真实 ZWD，stdout 与误差对照见 §4。 **质检复跑通过**（2026-09-26 02:00–02:05 EDT，独立 clone/venv/重新下载）：Drive 包 130852672 B（`Rar!` 头）、7z 报 `Unsupported Method` 得 0 B、unrar+密码解出 150007202 B / sha256 前缀 `a6dd6e6adf360982`、checkpoint epoch 38 / best_val_loss 0.0010780527549998267；VMF3 文件 3434750 B / 64807 行；§4b stdout **逐字一致**（Min 0.6699 / Max 40.3515 / Mean 11.9130 / Std 9.8792，real 3.35 s）；§4c 六行全部复现（RMSE **2.017→2.208** cm、bias +0.622、GRAZ 8.92/10.16/9.91、南北翻转 2.265、ZHD 57.78→265.28 mm）；坑 1/2/5（2.168）/7 实测复现。修：§4a 的 `ln -sf ../output/…` 会建成自指链接，`inference.py` 直接报 Errno 40，改为 `../../output/…` 并补坑 10。**未训练**（仓内无训练数据，训练需 GPU 与多年格网）。

> 岗位：已经有一张**全球 1° 对流层延迟格网（ZHD 或 ZWD）但精度/细节不够**（粗分辨率插值上来的"模糊图"），用 U-Net 把它恢复成更接近高分辨率参考的"清晰图"。**它不算 ZTD/ZWD/PWV**，不读 ERA5/GNSS 原始数据——输入和输出都是现成的 180×360 数组。冲突时：**源码 > 本文 > 上游 README**。  
> 经验模型给先验 → [gtrop](./gtrop.md) / GPT3（[tu-wien-vmf-gpt-codes](./tu-wien-vmf-gpt-codes.md)）；NWM 格网本身（VMF3）→ 同上页；斜路径 → [std-swd-calc](./std-swd-calc.md)；射线追踪 → [radiate](./radiate.md)。

## 1. 用途与边界

**背景词：**

| 术语 | 含义 |
| --- | --- |
| ZHD / ZWD | 天顶干 / 湿延迟；ZHD ≈ 2.3 m 由气压决定、空间平滑，ZWD 0–0.45 m 由水汽决定、空间起伏大（本机 VMF3 当天 ZWD **0.50–43.35 cm**） |
| 格网产品 | 把 ZHD/ZWD 存在全球规则格点上（VMF3 1°×1° = 180×360），用户按经纬度插值、再做高程归算得到测站值 |
| 降尺度 / "去模糊" | 粗格网（例如 5°）插值到 1° 后细节丢失；TropDS 学 "blur → clear" 的映射把细节补回来 |
| blur / clear | 代码里的术语：`{year}_blur.npy` = 待增强输入，`{year}_clear.npy` = 高精度参考（训练标签） |
| freeze mask | 由历史 RMSE 图 `weight.npy` 生成：RMSE < 阈值的格点**直接用输入**，不让网络改 |

**代码实际做的（读 `models.py`/`inference.py`/`datasets.py`）：**

- U-Net：5 级编码（32→512 通道）+ 4 级解码 + 1×1 卷积 + `Softplus`（保证输出 > 0）；本机打印 **12,487,073** 个参数
- 输入先 `clip` 到 `[global_min, global_max]` 再归一化到 [0,1]；输出反归一化。`global_min/max` 取自 `data/2020_clear.npy`，没有就取 `data/2024_clear.npy`，再没有就用 **0 / 50**（坑 4、5）
- 可选 `weight.npy`（180×360）→ freeze mask：`output = mask·网络输出 + (1−mask)·输入`
- 训练：`train.py` 读 2020–2023 训练、2024 验证，L1 + 0.1·SSIM，可按 RMSE 图加权，AdamW + 余弦重启

**不做：** 不生成 blur/clear 数据（作者的数据制备流程不在仓内）；不做测站插值与高程归算；不处理非 180×360 格网（也**不报错**，坑 7）；预训练权重对应哪个量（ZHD 还是 ZWD）、什么单位、blur 怎么造的，**README 与 checkpoint 都没写**。

## 2. 安装

```bash
git clone --depth 1 https://github.com/Sardingfish/TropDS && cd TropDS      # 22 MB（大半是 web/asset 图）
python3 -m venv venv && . venv/bin/activate
pip install --index-url https://download.pytorch.org/whl/cpu torch      # 本机 2.14.0+cpu；有 GPU 换 CUDA 版
pip install numpy                                                       # 6 个 .py 实际只 import torch + numpy
```

**不要** `pip install -r requirements.txt`：本机在 `apex>=0.1` 处失败（坑 1），其余 sphinx/jupyter/black 等代码根本不用。

预训练权重（~131 MB）：

```bash
curl -sL -o tropds_model.rar "https://drive.usercontent.google.com/download?id=1_kdhJ5BMXRtx09vCH-zSEvuekKTA1dYc&export=download&confirm=t"
curl -sL https://www.rarlab.com/rar/rarlinux-x64-712.tar.gz | tar xz     # 得到 ./rar/unrar（RARLAB 免费解压版）
./rar/unrar x -y -pJOGE-D-26-00053 tropds_model.rar output/              # 密码 = 论文投稿号，作者在 issue #1 回复
sha256sum output/best_model.pth | cut -c1-16                             # 本机 a6dd6e6adf360982
```

checkpoint 内容（本机 `torch.load` 打印）：`epoch 38`、`best_val_loss 0.0010780527549998267`、键 `model_state_dict / optimizer_state_dict / scheduler_state_dict / history`，只有**一个**模型。

## 3. 文件与参数

| 路径 | 形状 / 类型 | 说明 |
| --- | --- | --- |
| `data/{year}_blur.npy` | `(180,360)` 或 `(N,180,360)` float | 推理输入；`inference.py` 写死 `YEAR_INFERENCE = 2024`（README 说 2025） |
| `data/{year}_clear.npy` | 同上 | 训练标签；**推理时若存在会改变归一化**（坑 5） |
| `data/weight.npy` | `(180,360)` | 历史 RMSE 图；与 `FREEZE_THRESHOLD=0.01` 比较，单位须一致（坑 6） |
| `output/best_model.pth` | torch checkpoint | 推理读 `['model_state_dict']` |
| `output/{year}_deblurred.npy` | 与输入同形 | 推理结果，单位同输入 |

`inference.py` `main()` 里的可改常量：

| 常量 | 默认 | 作用 |
| --- | --- | --- |
| `MODEL_PATH` | `./output/best_model.pth` | 权重 |
| `INPUT_DIR` / `OUTPUT_DIR` | `./data` / `./output` | |
| `YEAR_INFERENCE` | `2024` | 拼文件名 |
| `FREEZE_THRESHOLD` | `0.01` | RMSE 低于此值的格点冻结 |
| `WEIGHT_MAP_PATH` | `./data/weight.npy` | 不存在则不冻结，打印 `Warning: Freeze function not enabled` |
| `base_channels` | `32` | 必须与训练一致，否则 `load_state_dict` 失败 |

`train.py` 关键常量：`YEARS_TRAIN=[2020,2021,2022,2023]`、`YEAR_VAL=2024`、`BATCH_SIZE=32`、`EPOCHS=200`、`L1_WEIGHT=1.0`、`SSIM_WEIGHT=0.1`、`WEIGHT_MODE='inverse'`、`NUM_WORKERS=0`。

## 4. 端到端（本机 · VMF3 1° ZWD，2024-01-01 00 UTC）

思路：拿 TU Wien 真实 VMF3 1° 格网 ZWD 当 "clear"，把它 5°×5° 块平均再铺回 1° 当 "blur"（模拟粗格网），喂给预训练模型，看输出是否更接近 clear。

### 4a. 准备数据

```bash
mkdir -p run/data run/output && cd run
curl -fsSL -o VMF3_20240101.H00 https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/2024/VMF3_20240101.H00   # 3434750 B，64807 行
cp ../*.py . && ln -sf ../../output/best_model.pth output/   # 链接目标相对 run/output/ 解析，写 ../output 会自指（坑 10）
cat > prep.py <<'PY'
import numpy as np
d=np.loadtxt('VMF3_20240101.H00',comments='!')
lat=d[:,0].reshape(180,360); lon=d[:,1].reshape(180,360)
zwd=(d[:,5]*100).reshape(180,360)          # m -> cm, row0 = lat 89.5 (north)
print('grid', zwd.shape, 'lat', lat[0,0], '->', lat[-1,0], 'lon', lon[0,0], '->', lon[0,-1])
blur=zwd.reshape(36,5,72,5).mean(axis=(1,3))   # 5x5 deg block mean
blur=np.kron(blur,np.ones((5,5)))              # back to 1x1 (blocky)
np.save('data/2024_blur.npy',blur.astype(np.float32)); np.save('clear_2024.npy',zwd.astype(np.float32))
print('ZWD clear  [cm] min=%.2f max=%.2f mean=%.2f'%(zwd.min(),zwd.max(),zwd.mean()))
print('blur-clear RMSE = %.3f cm'%np.sqrt(((blur-zwd)**2).mean()))
PY
python prep.py && python inference.py
```

VMF3 格网列为 `lat lon ah aw zhd zwd`（m），北→南、经度 0.5→359.5，正好 180×360。选 **cm** 是因为默认归一化上限 50 恰好罩住 ZWD（0.5–43.35 cm）。

### 4b. 本机 stdout（原样，`real 0m3.597s`）

```text
grid (180, 360) lat 89.5 -> -89.5 lon 0.5 -> 359.5
ZWD clear  [cm] min=0.50 max=43.35 mean=11.29
blur-clear RMSE = 2.017 cm

============================================================
Start inference - processing 2024 data
============================================================
Using default statistics: min=0.00, max=50.00
Loading model: ./output/best_model.pth
Model configuration: base_channels=32
Model loaded to device: cpu
Model parameters: 12,487,073

Warning: Freeze function not enabled

Loading data: ./data/2024_blur.npy
Original data shape: (180, 360)
Data type: float32

Start processing...
Processing complete, output shape: (180, 360)

Result saved: ./output/2024_deblurred.npy
Output shape: (180, 360)

Output data statistics:
  Min: 0.6699
  Max: 40.3515
  Mean: 11.9130
  Std: 9.8792

============================================================
Inference complete!
============================================================
```

### 4c. 评估（本机自写 `evalds.py` / `evalzhd.py`，调用仓内 `TroposphericDelayInference`）

```text
RMSE vs VMF3 1deg ZWD [cm]:  blur=2.017  TropDS=2.208
mean bias TropDS-clear = +0.622 cm
GRAZ cell (47.5N,15.5E): clear=8.92 blur=10.16 TropDS=9.91 cm
south-up input: RMSE TropDS=2.265 cm
ZHD[dm] range 11.56..23.58  RMSE blur=57.78 mm  TropDS=265.28 mm
ZWD[cm] range 0.50..43.35  RMSE blur=20.17 mm  TropDS=22.08 mm
```

**怎么读：**

- 在"5° 块平均"这种人造模糊上，预训练模型**没有改善**：RMSE 2.017 → 2.208 cm，且整体偏大 +0.62 cm。GRAZ 所在格点从 10.16 拉回到 9.91 cm（参考 8.92），局部方向对但整体不赢
- 同样的流程喂 ZHD（dm，落在 0–50 内）误差从 58 mm 变成 265 mm，明显不是这个 checkpoint 的训练对象；ZWD-cm 输出至少保持量级和空间形态 → **推测**发布权重对应 ZWD、单位近似 cm，但作者没写，不能当结论
- 南北翻转输入 RMSE 从 2.208 变 2.265 cm：结果对行序敏感但不剧烈，训练数据的行序也未公开
- 结论：论文里的增益依赖作者自己的 blur 制备方式与归一化统计量；**拿别人的格网直接套预训练权重不保证变好**。要用于生产，请用自己的 blur/clear 对重训（§5），或向作者要数据制备脚本

### 4d. 与 GPT3 / VMF3 / GTrop 的关系

TropDS 不产出测站值，放在同一张表里只为说明分工。GRAZ 数字见 [gtrop §4d](./gtrop.md) 与 [tu-wien-vmf-gpt-codes §4](./tu-wien-vmf-gpt-codes.md)；本页 GRAZ 格点值是**格点中心、格点高度**，未做高程归算，不能直接和站点 0.1047 m 比。

| 维度 | TropDS | GPT3 | VMF3 格网 | GTrop |
| --- | --- | --- | --- | --- |
| 性质 | 格网后处理（AI） | 经验模型 | NWM 实况产品 | 经验模型 |
| 输入 | 180×360 数组 | MJD/lat/lon/h | 下载 6 h 文件 | lat/lon/h/年/doy |
| 输出 | 180×360 数组（同单位） | p/T/e/Tm/ah/aw/梯度 | ah/aw/ZHD/ZWD | ZHD/ZWD/Tm |
| 测站插值+高程归算 | 否 | 内置 | 用户做（`vmf3_grid.m`） | 内置 |
| 需要 GPU/数据 | 训练需 GPU+多年格网；推理 CPU 秒级 | 否 | 网络 | 否 |
| GRAZ 2024-01-01 ZWD | 格点 9.91 cm（本机，参考 8.92） | 0.0580 m | 0.1015 m（格网归算后） | 0.0641 m |

## 5. 自己训练（未在本机执行）

数据要求（`datasets.py` 断言）：每年一对 `{year}_blur.npy` / `{year}_clear.npy`，形状 `(N,180,360)`，两者同形；可选 `weight.npy`。然后：

```bash
python train.py            # 读 data/2020–2024；输出 output/best_model.pth、training_history.npy、training_report.txt
```

本机未跑：没有作者的数据；按 VMF3 自造多年数据需下载数千个 6 h 文件，CPU 上 12.5 M 参数 × 200 epoch 不现实。README 建议 8 GB+ 显存。

## 6. 坑（除注明外均本机复现）

1. **现象** `ERROR: No matching distribution found for apex>=0.1`（`pip install -r requirements.txt` 中断） → **原因** PyPI 上 `apex` 只有 0.9.x 的 dev 预发布版，默认不选；且 NVIDIA apex 本就不是这个包；`Pillow-SIMD` 也只有需编译的 sdist → **修复** 只装真正用到的：`pip install --index-url https://download.pytorch.org/whl/cpu torch && pip install numpy`
2. **现象** 7-Zip 25.01 解压权重：`ERROR: Unsupported Method : best_model.pth`，得到 0 字节文件 → **原因** 包名 `.zip` 实为 RAR5 且加密，7z 不支持该方法 → **修复** `curl -sL https://www.rarlab.com/rar/rarlinux-x64-712.tar.gz | tar xz && ./rar/unrar x -y -pJOGE-D-26-00053 tropds_model.rar output/`
3. **现象** `unrar` 卡住不动（等密码输入）或 `Incorrect password for best_model.pth` → **原因** README 只写 "unzip using ID"，真实密码在 issue #1 作者回复里（论文投稿号，不是 Drive 文件 ID） → **修复** `./rar/unrar x -y -pJOGE-D-26-00053 tropds_model.rar output/ </dev/null`
4. **现象** 输入 ZHD（mm/cm）后输出全在 50 附近封顶或误差暴涨（dm 输入 RMSE 58 → 265 mm） → **原因** 找不到 `2020_clear.npy` 时归一化用默认 0–50，`SingleSampleDataset` 会把 >50 的值 `clip` 掉；而且发布权重不是按该量/单位训练的 → **修复** 先检查量程：`python -c "import numpy as n;a=n.load('data/2024_blur.npy');print(a.min(),a.max())"`，超出 0–50 就换单位或用与训练一致的 `global_min/max` 重训
5. **现象** 同一输入，放不放 `data/2024_clear.npy` 结果不同（RMSE 2.208 vs 2.168 cm，打印 `Using validation data statistics: min=0.50, max=43.35`） → **原因** `main()` 按文件存在与否悄悄切换归一化统计量 → **修复** 推理目录只放 blur：`mv data/2024_clear.npy ./ && python inference.py`，或在 `TroposphericDelayInference(..., global_min=0.0, global_max=50.0)` 显式传值
6. **现象** 输出与输入逐点相同，日志 `Frozen region ratio: 100.00%`、`Min: 10.0000 Max: 10.0000` → **原因** `weight.npy` 的 RMSE 全低于 `FREEZE_THRESHOLD=0.01`（单位不匹配，如 m 对 cm），整张图被冻结 → **修复** `python -c "import numpy as n;w=n.load('data/weight.npy');print(w.min(),w.max(),(w<0.01).mean())"`，冻结比例接近 1 就删掉或换单位
7. **现象** 喂 181×360（例如含两极的 1° 格网）照样出 `Output shape: (181, 360)`，没有任何报错 → **原因** 推理路径没有形状检查（训练的 `datasets.py` 才断言 180×360），U-Net 对任意尺寸都能前向 → **修复** 先转成格心 180×360：`python -c "import numpy as n;a=n.load('g181.npy');n.save('data/2024_blur.npy',0.5*(a[1:]+a[:-1]))"`（沿纬向相邻格线取平均，经向 361→360 同理去掉重复经线）
8. **现象** 按 README（2025）只放了 `data/2025_blur.npy`，运行只打印 `Error: Data file does not exist - ./data/2024_blur.npy` → **原因** 年份写死在 `main()` 里是 2024 → **修复** `sed -i 's/YEAR_INFERENCE = 2024/YEAR_INFERENCE = 2025/' inference.py`
9. **现象** 以为要 GPU → **原因** README 前提写 CUDA；推理其实 CPU 可跑（本机 180×360 单张 3.6 s 墙时含加载） → **修复** 装 CPU 版 torch 即可：`pip install --index-url https://download.pytorch.org/whl/cpu torch`

10. **现象** `OSError: [Errno 40] Too many levels of symbolic links: './output/best_model.pth'`（质检照抄旧版 §4a 实测） → **原因** 在 `run/` 里 `ln -sf ../output/best_model.pth output/`，符号链接目标相对**链接所在目录** `run/output/` 解析，指回自己 → **修复** `rm output/best_model.pth && ln -sf ../../output/best_model.pth output/`（或写绝对路径）

## 7. 诚实边界

- E2E 用的是**本人构造**的 blur（5° 块平均），不是论文的数据；§4c 的"变差"只说明预训练权重不能泛化到这种输入，**不否定**论文结论
- 权重对应的物理量/单位/行序未公开，§4c 的 "ZWD、cm" 是根据误差表现的推测
- 未训练、未跑 `metrics.py` 全套指标、未用 GPU；ERA5 等 NWM 原始数据没有用到（TropDS 本身不读 ERA5，用 ERA5 需 CDS 账号，本机没有）
- Google Drive 链接与密码均来自上游 README / issue，将来可能失效

## 8. 选型

| 需求 | 用 |
| --- | --- |
| 已有粗/模糊全球 ZHD/ZWD 格网，有配套高精度参考可训练 | **TropDS** |
| 只要某点的 ZHD/ZWD/Tm 先验 | [gtrop](./gtrop.md) 或 GPT3（[tu-wien-vmf-gpt-codes](./tu-wien-vmf-gpt-codes.md)） |
| 要当天实测格网 | VMF3（同上页） |
| 从 NWM 严格积分斜延迟 | [radiate](./radiate.md) |
| ZTD→斜路径湿延迟 | [std-swd-calc](./std-swd-calc.md) |
