# msise00 · NRLMSISE-00 中性大气操作手册

目录：[`PROJECTS.json` → `msise00`](../../PROJECTS.json) · 上游 <https://github.com/space-physics/msise00> · 许可 **MIT** · PyPI **`msise00` 1.11.1** · 本机 tip **`e4ab457`** · 首次调用 **CMake+gfortran** 编 `msise00_driver`；`(40°N,80°W)` 2015-03-23 15:30 / 100–500 km 剖面实跑（2026-09-24 EDT）

> 岗位：对给定 **时间/纬经/高度** 算 NRLMSISE-00 **中性密度与温度**（`xarray.Dataset`）。冲突时：**上游 README / `python -m msise00 -h` > 本文**。电离层电子密度见 [iri2016](./iri2016.md) / [pyglow](./pyglow.md) / [pyiri](./pyiri.md)；**不是 TEC 模型**。

## 1. 用途与边界

**做：**

- `msise00.run(time, altkm, glat, glon, indices=None) → xarray.Dataset`
- 变量：`He/O/N2/O2/Ar/H/N/AnomalousO`（m⁻³）、`Total`（kg m⁻³）、`Tn`/`Texo`（K）
- 自动拉 F10.7 / Ap（`geomagindices`）；可用 `indices=` 覆盖
- CLI：`python -m msise00 -t … -a … -c lat lon [-w out.nc] [-q]`

**不做：**

- **不是** IRI / 电子密度 → [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [pyiri](./pyiri.md)
- **不是** 磁坐标 → [apexpy](./apexpy.md)
- **不是** GIM/TEC → [ionex-gim](./ionex-gim.md)
- 首次运行需 **gfortran + cmake**（build-on-run）

一句话：msise00 = **NRLMSISE-00 的 pip 友好驱动**，返回 xarray，便于 GNSS 气象/掩星/耦合背景。

| 术语 | 含义 |
| --- | --- |
| `altkm` | 标量、列表或 `(start,stop,step)` |
| `Total` | 总质量密度 **kg m⁻³**（不是数密度） |
| `Tn` / `Texo` | 中性温度 / 外逸层温度（K） |
| `f107`/`f107s`/`Ap` | 写入 `attrs`；可 `indices=` 覆盖 |

## 2. 安装

```bash
sudo apt-get install -y gfortran cmake   # 首次编译需要
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv msise00-demo/.venv
source msise00-demo/.venv/bin/activate
pip install -U pip
pip install 'msise00==1.11.1' numpy
# CLI 写 NetCDF 另装：
pip install netCDF4
python -c "import msise00; print(msise00.__version__)"
# 期望：1.11.1
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 首次很慢 / 刷 CMake | build-on-run | 等编完；确认有 `gfortran`/`cmake` |
| `geomagindices` FTP 失败 | 指数源网络 | 重试；或 `indices={'f107':…,'f107s':…,'Ap':…}` |
| CLI `-w` → `cannot write NetCDF` | 未装后端 | `pip install netCDF4` |

## 3. 端到端：高度剖面（本机真跑）

与 IRI 手册同点：2015-03-23 15:30 UT，**(40°N, 80°W)**，100–500 km、步长 50 km。

```bash
cd ~/iono_ops/msise00-demo && source .venv/bin/activate
python - <<'PY'
import msise00

alts = list(range(100, 501, 50))
ds = msise00.run(time='2015-03-23T15:30', altkm=alts, glat=40, glon=-80)
print('msise00', msise00.__version__)
print('alts_km', [int(a) for a in ds.alt_km.values])

def col(name):
    return [float(x) for x in ds[name].values.ravel()]

print('Tn_K', [round(x, 2) for x in col('Tn')])
print('Total_kg_m3', [f'{x:.6e}' for x in col('Total')])
print('O_m3', [f'{x:.6e}' for x in col('O')])
print('N2_m3', [f'{x:.6e}' for x in col('N2')])
print('f107', float(ds.attrs['f107']),
      'f107s', round(float(ds.attrs['f107s']), 6),
      'Ap', float(ds.attrs['Ap']))
i = alts.index(250)
print('Tn_250', round(col('Tn')[i], 2),
      'O_250', f"{col('O')[i]:.6e}",
      'Total_250', f"{col('Total')[i]:.6e}")

ds2 = msise00.run(time='2015-03-23T15:30', altkm=250, glat=40, glon=-80,
                  indices={'f107': 100., 'f107s': 100., 'Ap': 4.})
print('override_Tn250', round(float(ds2['Tn'].values.ravel()[0]), 2))
print('override_attrs_f107_Ap', ds2.attrs['f107'], ds2.attrs['Ap'])
PY
```

**本机 stdout（2026-09-24 EDT，`msise00` 1.11.1；首次会编 Fortran，此处从略）：**

```text
msise00 1.11.1
alts_km [100, 150, 200, 250, 300, 350, 400, 450, 500]
Tn_K [184.24, 706.36, 940.89, 1009.87, 1030.53, 1036.83, 1038.79, 1039.41, 1039.61]
Total_kg_m3 ['5.482990e-07', '1.953361e-09', '2.880542e-10', '7.735296e-11', '2.597024e-11', '9.875775e-12', '4.063815e-12', '1.762729e-12', '7.945620e-13']
O_m3 ['4.803420e+17', '1.681782e+16', '4.348048e+15', '1.650972e+15', '6.928315e+14', '3.016596e+14', '1.339208e+14', '6.029752e+13', '2.748532e+13']
N2_m3 ['9.062672e+18', '2.936697e+16', '3.437433e+15', '6.674701e+14', '1.483682e+14', '3.478984e+13', '8.411930e+12', '2.082711e+12', '5.267368e+11']
f107 129.05 f107s 128.286667 Ap 11.0
Tn_250 1009.87 O_250 1.650972e+15 Total_250 7.735296e-11
override_Tn250 883.88
override_attrs_f107_Ap 100.0 4.0
```

| 字段 | 含义 |
| --- | --- |
| `Tn_250`≈1009.9 K | 250 km 中性温度 |
| `O_250` / `N2_250` | 数密度 m⁻³ |
| `Total_250`≈7.74e-11 | 质量密度 kg m⁻³ |
| `override_*` | 手写 F10.7/Ap 后 Tn 降到 ≈883.9 K |

### 3.1 CLI → NetCDF

```bash
pip install netCDF4   # 若尚未装
python -m msise00 -t 2015-03-23T15:30 -a 250 -c 40 -80 -w /tmp/msise00_demo.nc -q
python - <<'PY'
import xarray as xr
ds = xr.open_dataset('/tmp/msise00_demo.nc')
print('cli_Tn', float(ds['Tn'].values.ravel()[0]))
print('cli_O', float(ds['O'].values.ravel()[0]))
print('cli_f107', ds.attrs['f107'])
PY
```

**本机 stdout（CLI 会先刷 `geomagindices` 下载日志，可略）：**

```text
computing 2015-03-23T15:30
saving /tmp/msise00_demo.nc
cli_Tn 1009.87
cli_O 1650972300000000.0
cli_f107 129.05
```

## 4. 接到哪步

- 中性背景 / 阻力 / 掩星大气 → **本文**；电子密度气候态 → [iri2016](./iri2016.md) / [pyglow](./pyglow.md)（pyglow 也绑 MSIS，安装重）
- 磁坐标分箱 → [apexpy](./apexpy.md)
- 教程中性/耦合概念 → [04](../tutorials/04-iri-nequick.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 首次调用长时间 CMake | build-on-run | 装 `gfortran`/`cmake`；等一次编完 |
| 2 | `geomagindices` FTP/HTTP 失败 | 指数源网络 | `indices={'f107':…,'f107s':…,'Ap':…}` |
| 3 | CLI `-w` ValueError 无 NetCDF 后端 | 未装 `netCDF4`/`h5netcdf` | `pip install netCDF4` |
| 4 | 把 `Total` 当数密度 | 单位是 **kg m⁻³** | 数密度用 `O`/`N2`/… |
| 5 | 与旧 MSISE 表差一截 | F10.7/Ap 源或日期不同 | 写明 `attrs`；或锁 `indices=` |
| 6 | 当 TEC/IRI 用 | 只出中性 | 接 [iri2016](./iri2016.md) |
| 7 | `float(ds['Tn'])` TypeError | 仍是多维 | `.values.ravel()[0]` 或 `.sel(…)` |
| 8 | 无头绘图弹窗 | CLI 默认想画图 | 加 `-q` |
| 9 | 与 pyglow MSIS 数字不完全一致 | 驱动/指数路径不同 | 对照时锁同一 F10.7/Ap |
| 10 | 极高高度 AnomalousO 主导误解 | 模式在高空的已知分支 | 读变量含义；研究用注明 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| NRLMSISE-00 → xarray | **本文 msise00** |
| IRI + HWM + MSIS 全家桶 | [pyglow](./pyglow.md) |
| 仅 IRI 电子密度 | [iri2016](./iri2016.md) · [pyiri](./pyiri.md) |
| Apex/QD | [apexpy](./apexpy.md) |

- 文档/上游：<https://github.com/space-physics/msise00>
- 兄弟：[pyglow](./pyglow.md) · [iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [apexpy](./apexpy.md) · [nequickg](./nequickg.md)
