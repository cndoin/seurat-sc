# Seurat 流程模板

> 所有代码块的函数与参数名均已通过 `tools/sc_lint.py` 校验（基于源码 formals）。
> 复制到新脚本后**仍要再跑一次 lint**，因为改动可能引入错误。
> 参数取值（阈值、dims、resolution）必须按实际数据调整，不要照抄。

---

## 0. 通用开头

```r
library(Seurat)
library(ggplot2)
library(patchwork)

set.seed(42)
# Seurat v5 默认已经启用 future 友好的并行；CPU 多时可显式开
# library(future); plan("multisession", workers = 4)
rm(list = ls()); gc(verbose = FALSE)
```

---

## 1. 读取 10x 数据

```r
# 三个文件（barcodes.tsv.gz / features.tsv.gz / matrix.mtx.gz）
counts <- Read10X(data.dir = "data/pbmc3k/filtered_gene_bc_matrices/hg19/")
obj <- CreateSeuratObject(counts = counts, project = "pbmc3k",
                          min.cells = 3, min.features = 200)

# h5 格式
counts_h5 <- Read10X_h5(filename = "data/pbmc3k/filtered_feature_bc_matrix.h5")
obj <- CreateSeuratObject(counts = counts_h5, project = "pbmc3k", min.features = 200)

# 非 10x 的 mtx
mtx <- ReadMtx(mtx = "matrix.mtx", features = "features.tsv", cells = "barcodes.tsv")
obj <- CreateSeuratObject(counts = mtx)
```

---

## 2. QC 与过滤

```r
# 线粒体（人 ^MT-；小鼠 ^mt-，物种必须先确认）
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")
# 核糖体
obj[["percent.ribo"]] <- PercentageFeatureSet(obj, pattern = "^RP[SL]")

# 先看分布再定阈值，不要直接套 5 / 2500
VlnPlot(obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
        ncol = 3, pt.size = 0.1)
FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "percent.mt")
FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")

# 阈值按上面两张图定
obj <- subset(obj, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
```

---

## 3. 标准聚类（LogNormalize 路线）

```r
obj <- NormalizeData(obj, normalization.method = "LogNormalize",
                     scale.factor = 10000, layer = "counts", save = "data")
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)

all.genes <- rownames(obj)
obj <- ScaleData(obj, features = all.genes, layer = "data", save = "scale.data")

obj <- RunPCA(obj, features = VariableFeatures(object = obj), npcs = 50,
              layer = "scale.data", verbose = FALSE)

# 定 PCs：看拐点
ElbowPlot(obj, ndims = 50)
# 更严格：JackStraw（慢，细胞多时跳过）
# obj <- JackStraw(obj, num.replicate = 100); obj <- ScoreJackStraw(obj, dims = 1:20)
# JackStrawPlot(obj, dims = 1:20)

ndims <- 1:20          # 按 ElbowPlot 结果改
obj <- FindNeighbors(obj, reduction = "pca", dims = ndims)
obj <- FindClusters(obj, resolution = 0.5, random.seed = 0)
obj <- RunUMAP(obj, reduction = "pca", dims = ndims, seed.use = 42)

DimPlot(obj, reduction = "umap", label = TRUE, repel = TRUE)
```

**细胞周期回归**（可选，在 ScaleData 之前算分）

```r
s.genes <- cc.genes$s.genes
g2m.genes <- cc.genes$g2m.genes
obj <- CellCycleScoring(obj, s.features = s.genes, g2m.features = g2m.genes)
obj <- ScaleData(obj, vars.to.regress = c("S.Score", "G2M.Score"),
                 features = all.genes, layer = "data", save = "scale.data")
```

---

## 4. SCTransform 路线

```r
obj <- SCTransform(obj, assay = "RNA", new.assay.name = "SCT",
                   vst.flavor = "v2", variable.features.n = 3000,
                   conserve.memory = TRUE, seed.use = 1448145)

# 不要再跑 NormalizeData / ScaleData
obj <- RunPCA(obj, assay = "SCT", npcs = 50, verbose = FALSE)
obj <- RunUMAP(obj, reduction = "pca", dims = 1:30, assay = "SCT", seed.use = 42)
obj <- FindNeighbors(obj, assay = "SCT", reduction = "pca", dims = 1:30)
obj <- FindClusters(obj, resolution = 0.8, random.seed = 0)

# SCT 上找 marker：必须先 prep
obj <- PrepSCTFindMarkers(obj, assay = "SCT", verbose = FALSE)
mk <- FindMarkers(obj, assay = "SCT", slot = "data", ident.1 = "0",
                  logfc.threshold = 0.25, min.pct = 0.25, only.pos = TRUE)
all_mk <- FindAllMarkers(obj, assay = "SCT", only.pos = TRUE,
                         min.pct = 0.25, return.thresh = 0.01)
```

---

## 5. 多样本整合（v5 首选：layers + IntegrateLayers）

```r
# obj 已 merge 好，meta.data 里有 orig.ident / sample
obj[["RNA"]] <- split(obj[["RNA"]], f = obj$sample)

# 逐层预处理（Seurat 会自动对每个 layer 跑）
obj <- NormalizeData(obj, layer = "counts", save = "data", verbose = FALSE)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
obj <- ScaleData(obj, layer = "data", save = "scale.data", verbose = FALSE)
obj <- RunPCA(obj, npcs = 30, verbose = FALSE)

# 四选一：RPCA（快，推荐）/ CCA（差异大）/ Harmony / JointPCA
obj <- IntegrateLayers(object = obj, method = RPCAIntegration,
                       orig.reduction = "pca", new.reduction = "integrated.rpca",
                       verbose = FALSE)
# obj <- IntegrateLayers(object = obj, method = HarmonyIntegration,
#                        orig.reduction = "pca", new.reduction = "harmony", verbose = FALSE)

obj <- JoinLayers(obj)
obj <- FindNeighbors(obj, reduction = "integrated.rpca", dims = 1:30)
obj <- FindClusters(obj, resolution = 0.8, random.seed = 0)
obj <- RunUMAP(obj, reduction = "integrated.rpca", dims = 1:30, seed.use = 42)

DimPlot(obj, group.by = "sample")          # 看样本是否混匀
DimPlot(obj, split.by = "sample")
```

**v4 兼容路线**（需要整合后的表达矩阵时用）

```r
features <- SelectIntegrationFeatures(object.list = obj.list, nfeatures = 3000)
anchors  <- FindIntegrationAnchors(object.list = obj.list, anchor.features = features,
                                   reduction = "rpca", dims = 1:30)
combined <- IntegrateData(anchorset = anchors, dims = 1:30, new.assay.name = "integrated")
DefaultAssay(combined) <- "integrated"
combined <- ScaleData(combined, verbose = FALSE)
combined <- RunPCA(combined, npcs = 30, verbose = FALSE)
combined <- RunUMAP(combined, reduction = "pca", dims = 1:30, seed.use = 42)
```

---

## 6. 参考映射 / 标签转移

```r
anchors <- FindTransferAnchors(reference = ref, query = query,
                               normalization.method = "LogNormalize",
                               reduction = "pcaproject", dims = 1:30)
pred <- TransferData(anchorset = anchors, refdata = ref$celltype, dims = 1:30)
query <- AddMetaData(query, metadata = pred)

# 只保留高置信
query$transferred <- ifelse(query$prediction.score.max > 0.7,
                            query$predicted.id, NA_character_)

# 一步法（同时把 query 投影到参考 UMAP）
# query <- MapQuery(anchorset = anchors, reference = ref, query = query,
#                   refdata = list(celltype = "celltype"),
#                   reference.reduction = "pca", reduction.model = "umap")
```

**重命名细胞类型**

```r
new.ids <- c("0" = "Naive CD4 T", "1" = "Memory CD4 T", "2" = "CD14+ Mono",
             "3" = "B", "4" = "CD8 T", "5" = "FCGR3A+ Mono",
             "6" = "NK", "7" = "DC", "8" = "Platelet")
obj <- RenameIdents(obj, new.ids)      # 位置传参：命名向量
obj$celltype <- Idents(obj)            # 固化到 meta.data
DimPlot(obj, label = TRUE, repel = TRUE)
```

---

## 7. 差异表达

```r
Idents(obj) <- "seurat_clusters"

# 两群比较
mk <- FindMarkers(obj, ident.1 = "0", ident.2 = "1",
                  test.use = "wilcox", min.pct = 0.25, logfc.threshold = 0.25,
                  only.pos = FALSE, random.seed = 1)
# test.use 可选：wilcox / bimod / roc / t / negbinom / poisson / LR / MAST / DESeq2

# 全部群
all_mk <- FindAllMarkers(obj, only.pos = TRUE, min.pct = 0.25,
                         logfc.threshold = 0.25, return.thresh = 0.01)
top10 <- all_mk |> group_by(cluster) |> top_n(n = 10, wt = avg_log2FC)

# 跨样本保守 marker
cons <- FindConservedMarkers(obj, ident.1 = "0", grouping.var = "sample",
                             assay = "RNA", slot = "data")

# 拟 bulk（样本间差异更稳）
pb   <- AggregateExpression(obj, group.by = c("seurat_clusters", "sample"),
                            return.seurat = TRUE)
pbc  <- PseudobulkExpression(obj, group.by = c("seurat_clusters", "sample"),
                             layer = "data", method = "average")
```

---

## 8. 空间转录组

```r
# Visium
sp <- Load10X_Spatial(data.dir = "spatial/",
                      filename = "filtered_feature_bc_matrix.h5",
                      assay = "Spatial", slice = "slice1")
# Visium HD（指定 bin）
# sp <- Load10X_Spatial(data.dir = "hd/", bin.size = 16)
# Xenium / Vizgen / Nanostring / Akoya
# sp <- LoadXenium(data.dir = "xenium_out/")
# sp <- LoadVizgen(data.dir = "vizgen_out/")

sp <- SCTransform(sp, assay = "Spatial", ncells = 3000, verbose = FALSE)
sp <- FindSpatiallyVariableFeatures(sp, assay = "SCT",
                                    selection.method = "moransi", nfeatures = 2000)
top <- SpatiallyVariableFeatures(sp, selection.method = "moransi")

SpatialFeaturePlot(sp, features = top[1:6], image.alpha = 0.6, ncol = 3)
SpatialDimPlot(sp, label = TRUE, alpha = 0.7)

# niche 分析（单细胞级空间数据）
# sp <- BuildNicheAssay(sp, fov = "fov", group.by = "celltype",
#                       neighbors.k = 20, niches.k = 4)
```

> `RunMoransI` 的真实签名是 `RunMoransI(data, pos, verbose)`，**没有 `features` 参数**。
> 需要空间自相关用 `FindSpatiallyVariableFeatures(selection.method = "moransi")`，
> 或按源码签名传 `data` / `pos`。

---

## 9. WNN 多模态（RNA + ATAC / ADT）

```r
# RNA 侧 PCA、ATAC 侧 LSI（ATAC 的 LSI 通常来自 Signac）
obj <- FindMultiModalNeighbors(
  obj,
  reduction.list = list("pca", "lsi"),
  dims.list = list(1:30, 2:30),
  modality.weight.name = "RNA.weight"
)
obj <- RunUMAP(obj, nn.name = "weighted.nn",
               reduction.name = "wnn.umap", reduction.key = "wnnUMAP_")
obj <- FindClusters(obj, graph.name = "wsnn", algorithm = 3,
                    resolution = 1, verbose = FALSE)
DimPlot(obj, reduction = "wnn.umap", label = TRUE, group.by = "seurat_clusters")
```

> **没有 `RunWNN()`。** 源码里不存在这个函数，WNN 靠上面三步完成。

---

## 10. Sketch（百万级细胞）

```r
obj <- SketchData(obj, assay = "RNA", ncells = 20000,
                  sketched.assay = "sketch", method = "LeverageScore", seed = 123)

DefaultAssay(obj) <- "sketch"
obj <- FindVariableFeatures(obj, verbose = FALSE)
obj <- ScaleData(obj, verbose = FALSE)
obj <- RunPCA(obj, reduction.name = "pca.sketch", verbose = FALSE)
obj <- FindNeighbors(obj, reduction = "pca.sketch", dims = 1:50)
obj <- FindClusters(obj, cluster.name = "sketch_cluster", resolution = 1)
obj <- RunUMAP(obj, reduction = "pca.sketch", dims = 1:50,
               reduction.name = "umap.sketch", seed.use = 42)

# 投影回全量
obj <- ProjectData(obj, sketched.assay = "sketch", assay = "RNA",
                   full.reduction = "pca", sketched.reduction = "pca.sketch",
                   refdata = list(sketch_cluster = "sketch_cluster"))
DefaultAssay(obj) <- "RNA"
```

---

## 11. Mixscape / 扰动

```r
obj <- CalcPerturbSig(obj, assay = "RNA", slot = "data", gd.class = "guide_ID",
                      nt.cell.class = "NT", reduction = "pca", ndims = 15,
                      new.assay.name = "PRTB", num.neighbors = 20)
obj <- RunMixscape(obj, assay = "PRTB", labels = "gene", nt.class.name = "NT",
                   new.class.name = "mixscape_class", min.de.genes = 5,
                   min.cells = 5, de.assay = "RNA", logfc.threshold = 0.25,
                   prtb.type = "KO")
PlotPerturbScore(obj, target.gene.class = "gene",
                 mixscape.class = "mixscape_class", prtb.type = "KO")
MixscapeHeatmap(obj, ident.1 = "NT", ident.2 = "KO",
                assay = "RNA", group.by = "mixscape_class",
                mixscape.class = "mixscape_class", max.genes = 100)
```

---

## 12. 常用出图

```r
# marker 可视化
VlnPlot(obj, features = c("MS4A1", "CD79A"), layer = "data", stack = TRUE, pt.size = 0)
FeaturePlot(obj, features = c("MS4A1", "CD79A"), reduction = "umap", ncol = 2)
DotPlot(obj, features = c("MS4A1", "CD79A", "CD3E"), group.by = "seurat_clusters") +
  RotatedAxis()
DoHeatmap(obj, features = top10$gene, group.by = "seurat_clusters",
          slot = "scale.data", raster = TRUE)
RidgePlot(obj, features = c("MS4A1"), layer = "data")

# 组合与保存
p <- (DimPlot(obj, label = TRUE) | FeaturePlot(obj, features = "MS4A1"))
ggsave("umap_feature.pdf", p, width = 12, height = 5)
```

---

## 13. 保存 / 加载

```r
SaveSeuratRds(obj, file = "final.seurat.rds")
obj <- LoadSeuratRds("final.seurat.rds")
# 或 base R
saveRDS(obj, "final.rds"); obj <- readRDS("final.rds")
```
