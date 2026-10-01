library(Seurat)
library(ggplot2)
library(patchwork)

# ---------- 1. SCTransform + 多样本整合（v5 layers 路线） ----------
obj <- readRDS("merged.rds")
obj[["RNA"]] <- split(obj[["RNA"]], f = obj$orig.ident)

obj <- NormalizeData(obj, normalization.method = "LogNormalize", scale.factor = 1e4, verbose = FALSE)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
obj <- ScaleData(obj, verbose = FALSE)
obj <- RunPCA(obj, npcs = 30, verbose = FALSE)

obj <- IntegrateLayers(object = obj, method = RPCAIntegration,
                       orig.reduction = "pca", new.reduction = "integrated.rpca",
                       verbose = FALSE)
obj <- JoinLayers(obj)
obj <- FindNeighbors(obj, reduction = "integrated.rpca", dims = 1:30)
obj <- FindClusters(obj, resolution = 0.8, algorithm = 1, random.seed = 0)
obj <- RunUMAP(obj, reduction = "integrated.rpca", dims = 1:30, seed.use = 42)

# ---------- 2. SCT 差异化表达 ----------
sct <- SCTransform(obj, assay = "RNA", new.assay.name = "SCT", vst.flavor = "v2",
                   variable.features.n = 3000, conserve.memory = TRUE)
sct <- PrepSCTFindMarkers(sct, assay = "SCT", verbose = FALSE)
mk <- FindMarkers(sct, assay = "SCT", slot = "data", ident.1 = "0",
                  logfc.threshold = 0.25, test.use = "wilcox", only.pos = TRUE)
all_mk <- FindAllMarkers(sct, assay = "SCT", only.pos = TRUE, min.pct = 0.25)

# ---------- 3. 细胞周期 + 模块评分 ----------
s.genes <- cc.genes$s.genes
g2m.genes <- cc.genes$g2m.genes
obj <- CellCycleScoring(obj, s.features = s.genes, g2m.features = g2m.genes, set.ident = TRUE)
obj <- AddModuleScore(obj, features = list(s.genes), name = "S_Score", assay = "RNA")

# ---------- 4. 参考映射 ----------
anchors <- FindTransferAnchors(reference = ref, query = obj, dims = 1:30,
                               normalization.method = "LogNormalize", reduction = "pcaproject")
predictions <- TransferData(anchorset = anchors, refdata = ref$celltype, dims = 1:30)

# ---------- 5. 空间 ----------
sp <- Load10X_Spatial(data.dir = "spatial/", filename = "filtered_feature_bc_matrix.h5",
                      assay = "Spatial", slice = "slice1", bin.size = NULL)
sp <- SCTransform(sp, assay = "Spatial", ncells = 3000, verbose = FALSE)
sp <- FindSpatiallyVariableFeatures(sp, assay = "SCT", selection.method = "moransi", nfeatures = 2000)
sp <- RunMoransI(sp, pos = GetTissueCoordinates(sp), verbose = FALSE)
p1 <- SpatialFeaturePlot(sp, features = c("MS4A1"), image.alpha = 0.6)
p2 <- SpatialDimPlot(sp, label = TRUE)

# ---------- 6. Sketch 大数据 ----------
big <- SketchData(obj, assay = "RNA", ncells = 20000, sketched.assay = "sketch",
                  method = "LeverageScore", seed = 123)
DefaultAssay(big) <- "sketch"
big <- FindVariableFeatures(big)
big <- ScaleData(big)
big <- RunPCA(big, reduction.name = "pca.sketch")
big <- ProjectData(object = big, sketched.assay = "sketch", assay = "RNA",
                   full.reduction = "pca", sketched.reduction = "pca.sketch")

# ---------- 7. 可视化 ----------
v1 <- VlnPlot(obj, features = c("MS4A1", "CD79A"), layer = "data", stack = TRUE)
v2 <- DotPlot(obj, features = c("MS4A1", "CD79A"), group.by = "seurat_clusters")
v3 <- FeaturePlot(obj, features = "MS4A1", min.cutoff = "q10")
v4 <- DoHeatmap(obj, features = top10$gene, group.by = "seurat_clusters", slot = "scale.data")
v5 <- DimPlot(obj, group.by = "orig.ident", split.by = "orig.ident")
v1 + v2 + v3

# ---------- 8. 拟 bulk ----------
pb <- AggregateExpression(obj, group.by = c("seurat_clusters", "orig.ident"), return.seurat = TRUE)

SaveSeuratRds(obj, file = "final.seurat.rds")
