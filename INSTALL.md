# 安装指南（Windows / macOS / Linux 通用）

seurat-sc 是**纯文本技能包**：Python 只用标准库，R 脚本只依赖 Seurat。
没有二进制、没有编译步骤，解压即用。

---

## 一、安装到 Agent 宿主

### Claude Code

```bash
# 用户级（全局生效）
python3 install.py

# 项目级（只对当前项目生效）
python3 install.py --project
```

### WorkBuddy

```bash
python3 install.py --host workbuddy
```

### 其它宿主 / 自定义位置

```bash
python3 install.py --dir <你的 skills 根目录>
```

Windows 上如果没有 `python3`，把命令里的 `python3` 换成 `python`。
装完**重启 Agent 宿主**，让它重新扫描 skills 目录。

---

## 二、准备 R 环境（要真跑分析才需要）

技能的核心校验器 `tools/sc_lint.py` **不需要 R**，装完就能用。
只有"真的执行 R 脚本出图出数"才需要下面这步。

### Windows 首选：官方 CRAN R（推荐）

```bash
# 1. 装官方 R（自带 Rtools 构建的工具链，无需另装编译器）
#    https://cran.r-project.org/bin/windows/base/
#    国内加速（中科大镜像）：https://mirrors.ustc.edu.cn/CRAN/bin/windows/base/

# 2. 装好后在 R 里装 Seurat（CRAN 提供 Windows 预编译二进制，不现场编译）
R -e "install.packages('Seurat', repos='https://mirrors.ustc.edu.cn/CRAN/')"
```

**为什么 Windows 首选官方 CRAN R 而不是 conda-forge**（实测结论，很重要）：

conda-forge 用 mingw-w64 构建 Windows R 包时，把 PE 头 `ImageBase` 设在
`0x180000000` 等 **>2GB 高地址**并启用 `HIGH_ENTROPY_VA`。而 mingw 的
**伪重定位（pseudo-reloc）字段是 32-bit**，只能装正负 2GB 内的偏移。
DLL 一旦加载到 >2GB，`library(Seurat)` 等加载 R 包 DLL 的场景必然触发：

```
Mingw-w64 runtime failure:
32 bit pseudo relocation at 0x7FFA... out of range, targeting 0x7FF9...
```

这是 **conda-forge Windows 包的固有构建缺陷**，与机器配置、ASLR 设置无关，
无法通过改环境变量、兼容层、系统设置绕过。官方 CRAN R 用 Rtools 构建的包 DLL
不受影响——注意根因不是高 ImageBase 本身：实测官方 R 的 R.exe/R.dll 同样是
高基址（0x140000000 / 0x2BB400000）却能正常加载 Seurat。真正的差异在于
Rtools 构建链产出的包 DLL 伪重定位条目都在 32-bit 可达范围内，而 conda-forge
的 mingw 构建把条目生成到了范围外。

> 注：该问题只影响 **Windows + conda-forge 的 R 包 DLL 加载**。
> 技能本体（SKILL.md + Python 校验器）完全不依赖 R 运行，在任何平台都可用。

### macOS / Linux：conda-forge 或系统包管理器

```bash
# conda-forge（三平台统一，免编译）
micromamba create -y -n seurat -c conda-forge \
    r-base r-seurat r-seuratobject r-hdf5r r-jsonlite
micromamba activate seurat
```

| 平台 | 推荐方式 | 命令 |
|---|---|---|
| Windows | **官方 CRAN R**（避开 mingw 伪重定位缺陷） | 见上方"Windows 首选" |
| macOS | Homebrew + CRAN | `brew install r` 然后 R 里 `install.packages("Seurat")` |
| Linux | apt / conda-forge | `apt install r-base` 或 conda-forge |
| 任意 | 官方安装包 | https://cran.r-project.org/ |

`hdf5r` / `sf` 等包用官方 `install.packages()` 在 Windows 上可能现场编译、
缺 Rtools 报错。**官方 CRAN 的 Seurat 主包是预编译二进制**，直接装即可；
若个别依赖需要编译，装 [Rtools](https://cran.r-project.org/bin/windows/Rtools/)。

### 验证环境

```bash
Rscript scripts/preflight.R          # 人读输出
Rscript scripts/preflight.R --json   # 机器可读
```

缺包时它会**直接打印可复制的安装命令**（按 conda / CRAN / Bioconductor / GitHub 区分来源）。

---

## 三、验证技能本身

```bash
python3 tools/selftest.py        # 全绿（退出码 0）才算装好
```

它会跑四类检查：回归用例、文档代码块、工具冒烟、数据完整性。

---

## 四、日常使用

```bash
# 写完 R 脚本后必跑（error 必须为 0）
python3 tools/sc_lint.py my_analysis.R

# 查真实函数签名
python3 tools/sc_api.py FindMarkers

# 一句话需求 -> 推荐流程
python3 tools/sc_plan.py "两个样本 PBMC 整合后找差异基因"
```

---

## 五、系统要求

| 项 | 要求 |
|---|---|
| Python | 3.7+（**只用标准库**，无需 pip install 任何东西） |
| R（可选） | 4.0+，Seurat 5.x。Windows 建议官方 CRAN R |
| 操作系统 | Windows 10+ / macOS / Linux（跨平台，无平台专属代码） |
| 内存 | 8 GB 起；几万细胞建议 16 GB+；百万细胞走 `SketchData()` |
| GPU | **不需要**。Seurat 全程 CPU |

---

## 六、常见问题

**Q：`python3` 找不到？**
Windows 用 `python`。技能里所有命令写 `python3` 是为了跨平台统一，
Windows 用户把命令替换一下即可。

**Q：`tools/selftest.py` 报某个函数不存在？**
上游 Seurat 新增了导出。跑 `python3 tools/etl/rebuild.py` 重建事实底座。

**Q：装到一半报 `Permission denied`？**
目标 skills 目录没有写权限。用 `install.py --dir <可写目录>` 指到用户目录。

**Q：Windows 上 `library(Seurat)` 崩溃，报 "32 bit pseudo relocation out of range"？**
你用了 conda-forge 的 R 包，命中上面说的 mingw 伪重定位缺陷。
**换成官方 CRAN R 即可解决**（见第二节）。这不是技能的问题。

**Q：R 脚本跑不起来？**
先 `Rscript scripts/preflight.R`，看缺哪个包，按它打印的命令装。
