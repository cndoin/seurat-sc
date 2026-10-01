library(Seurat)
library(ggplot2)

# ---- 读取与建对象 ----
pbmc.data <- Read10X(data.dir = "data/pbmc3k/filtered_gene_bc_matrices/hg19")
pbmc <- CreateSeuratObject(counts = pbmc.data, project = "pbmc3k",
                           min.cells = 3, min.features = 200)

# ---- QC ----
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")
pbmc <- subset(pbmc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)

# ---- 标准流程 ----
pbmc <- NormalizeData(pbmc, normalization.method = "LogNormalize", scale.factor = 10000)
pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)
pbmc <- ScaleData(pbmc, vars.to.regress = "percent.mt")
pbmc <- RunPCA(pbmc, features = VariableFeatures(object = pbmc), npcs = 30, verbose = FALSE)
pbmc <- FindNeighbors(pbmc, dims = 1:20)
pbmc <- FindClusters(pbmc, resolution = 0.5, random.seed = 0)
pbmc <- RunUMAP(pbmc, dims = 1:20, seed.use = 42)

# ---- marker ----
mk <- FindMarkers(pbmc, ident.1 = "0", ident.2 = "1",
                  test.use = "wilcox", min.pct = 0.25, logfc.threshold = 0.25)
write.csv(mk, "markers_0_vs_1.csv")

p <- DimPlot(pbmc, reduction = "umap", label = TRUE, repel = TRUE)
ggsave("umap.pdf", p, width = 8, height = 6)
saveRDS(pbmc, "pbmc_final.rds")
