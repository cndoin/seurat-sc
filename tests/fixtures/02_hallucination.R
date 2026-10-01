library(Seurat)

obj <- RunWNN(obj)
CoveragePlot(obj, region = "chr1-1-1000")

mk <- FindMarkers(obj, test.use = "wilcox", fake.param = 1)
mk2 <- findmarkers(obj)

obj <- NormalizeData(obj, slot = "counts")
obj <- RunPCA(obj, do.print = TRUE, npcs = 30)
obj <- FindVariableGenes(obj, nfeatures = 2000)

d <- obj@assays$RNA@data
