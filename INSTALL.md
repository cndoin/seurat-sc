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

### 推荐：conda-forge（三平台统一，免编译）

```bash
# 1. 装 micromamba（单文件，无需管理员）
#    https://github.com/mamba-org/micromamba#installation

# 2. 一次装齐 R + Seurat（预编译二进制，Windows 免编译地狱）
micromamba create -y -n seurat -c conda-forge \
    r-base r-seurat r-seuratobject r-hdf5r r-jsonlite

# 3. 激活
micromamba activate seurat
```

### 各平台替代方案

| 平台 | 方式 | 命令 |
|---|---|---|
| Windows | conda-forge（推荐） | 见上 |
| macOS | Homebrew + CRAN | `brew install r` 然后 R 里 `install.packages("Seurat")` |
| Linux | apt / conda | `apt install r-base` 或 conda-forge |
| 任意 | 官方安装包 | https://cran.r-project.org/ |

**Windows 上强烈建议走 conda-forge**：`hdf5r` / `sf` 等包用官方 `install.packages()`
会现场编译，缺 Rtools 就报错；conda-forge 全是预编译二进制。

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
| R（可选） | 4.0+，Seurat 5.x |
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

**Q：R 脚本跑不起来？**
先 `Rscript scripts/preflight.R`，看缺哪个包，按它打印的命令装。
