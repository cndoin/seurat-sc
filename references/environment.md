# Seurat 环境搭建

---

## 1. 最低要求（来自 DESCRIPTION，非估算）

```
R            >= 4.0.0        （推荐 4.3+，太旧会撞不上 Bioconductor 版本）
Seurat       5.x
SeuratObject >= 5.0.2        （Seurat 会自动装）
LinkingTo    Rcpp / RcppEigen / RcppProgress  → 需要能编译 C++
```

Seurat 的 `Imports` 有 50 多个包（ggplot2、Matrix、uwot、Rtsne、igraph、
RcppAnnoy、RcppHNSW、sctransform、future、plotly、spatstat.* 等），
`install.packages("Seurat")` 会自动拉。**第一次装大约 10–30 分钟**，
Linux 上需要系统库（见第 3 节）。

---

## 2. 安装

### 2.1 CRAN（最省事）

```r
install.packages("Seurat")
```

### 2.2 官方 r-universe（要最新开发版）

DESCRIPTION 里声明了 `Additional_repositories:
https://satijalab.r-universe.dev, https://bnprks.r-universe.dev`，
所以官方推荐这样装：

```r
options(repos = c(
  satijalab = "https://satijalab.r-universe.dev",
  bnprks    = "https://bnprks.r-universe.dev",
  CRAN      = "https://cloud.r-project.org"
))
install.packages("Seurat")
```

### 2.3 从 GitHub（要 master 上的最新功能）

```r
# install.packages("remotes")
remotes::install_github("satijalab/seurat", ref = "master")
# 若 SeuratObject 也要最新
remotes::install_github("mojaveazure/seurat-object", ref = "develop")
```

---

## 3. 系统依赖

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install -y \
  libcurl4-openssl-dev libssl-dev libxml2-dev \
  libhdf5-dev libpng-dev libjpeg-dev libtiff5-dev \
  libgeos-dev libgdal-dev libproj-dev \
  libglpk-dev libmagick++-dev \
  build-essential gfortran
```

`hdf5r`（读 h5 用）特别依赖 `libhdf5-dev`；
`sf` / `spatstat`（空间数据）依赖 GEOS / GDAL / PROJ。

### CentOS / RHEL

```bash
sudo yum install -y openssl-devel libcurl-devel libxml2-devel \
  hdf5-devel libpng-devel libjpeg-turbo-devel geos-devel gdal-devel \
  glpk-devel ImageMagick-c++-dev gcc gcc-gfortran
```

### Windows

装 [Rtools](https://cran.r-project.org/bin/windows/Rtools/)（版本要与 R 大版本对应），
勾选"添加到 PATH"。

### macOS

```bash
brew install hdf5 geos gdal proj gsl imagemagick
```

---

## 4. 常用可选包（用到才装）

| 包 | 用途 | 安装 |
| --- | --- | --- |
| `harmony` | `HarmonyIntegration()` | `install.packages("harmony")` |
| `BPCells` | 磁盘矩阵，百万细胞省内存 | `remotes::install_github("bnprks/BPCells")` |
| `leidenbase` | `FindClusters` 用 Leiden（默认走 igraph） | `install.packages("leidenbase")` |
| `presto` | 快速差异表达 | `remotes::install_github("immunogenomics/presto")` |
| `glmGamPoi` | `sctransform` 加速 | `BiocManager::install("glmGamPoi")` |
| `DESeq2` / `MAST` / `limma` | FindMarkers 的其它检验 | `BiocManager::install(c("DESeq2","MAST","limma"))` |
| `Signac` | ATAC / WNN 的 LSI / `CoveragePlot` | `BiocManager::install("Signac")` |
| `SeuratDisk` | h5Seurat / h5ad 互转 | `remotes::install_github("mojaveazure/seurat-disk")` |
| `Azimuth` | 参考注释 | `remotes::install_github("satijalab/azimuth")` |
| `SeuratData` | 官方示例数据（pbmc3k 等） | `remotes::install_github("satijalab/seurat-data")` |
| `scDblFinder` | 去双细胞（Seurat 本体不提供） | `BiocManager::install("scDblFinder")` |
| `enrichR` | `DEenrichRPlot()` 富集 | `install.packages("enrichR")` |

`preflight.R` 会检查上面这些包装没装。

---

## 5. 验证

```bash
Rscript scripts/preflight.R --json
```

```r
packageVersion("Seurat")        # 5.x
packageVersion("SeuratObject")  # >= 5.0.2
library(Seurat)
```

---

## 6. 三种跑不起来的场景与出路

### 6.1 本机（Windows）没装 R

实测确认：当前机器 `which R` / `which Rscript` 均无输出。
此时本技能仍可做「选函数 / 写代码 / 校验 / 规划 / 解读报错」，
但**跑不出数和图**。给出三选一，不要假装跑过：

1. 装 R ≥ 4.3 + Rtools，再 `install.packages("Seurat")`（本机最重）；
2. 交付脚本到 Linux 服务器 / HPC / Colab；
3. GitHub Actions 编排（见 6.3）。

### 6.2 离线 / 内网机器

```r
# 有网机器上打包
pkgs <- c("Seurat", "harmony", "presto")
dir.create("pkg_cache")
install.packages(pkgs, destdir = "pkg_cache", dependencies = TRUE)
# 拷到内网后
install.packages(list.files("pkg_cache", full.names = TRUE), repos = NULL)
```

生产环境建议用 `renv` 锁版本：`renv::init()` / `renv::snapshot()` / `renv::restore()`。

### 6.3 GitHub Actions

```yaml
- uses: r-lib/actions/setup-r@v2
  with:
    r-version: '4.3'
- uses: r-lib/actions/setup-r-dependencies@v2
  with:
    packages: |
      any::Seurat
      any::harmony
      any::rmarkdown
- name: Run analysis
  run: Rscript scripts/run_seurat.R --script analysis.R --workdir runs/ci --json
```

配合 `actions/cache` 缓存 R 包目录可大幅提速。

---

## 7. 版本对齐的硬约束

1. **Seurat 5 必须配 SeuratObject ≥ 5.0.2**。装完检查 `packageVersion("SeuratObject")`。
2. **v4 时代保存的 `.rds` 在 v5 打开要先 `UpdateSeuratObject()`**，
   否则 layers / Assay5 结构对不上，报错很隐晦。
3. **Bioconductor 版本与 R 版本绑定**。R 4.0 装不上新版 DESeq2/MAST；
   要用这些检验方法就上 R ≥ 4.3。
4. **sctransform ≥ 0.4.1**（DESCRIPTION 里写死的），旧版会和 v5 的 SCT 流程冲突。
