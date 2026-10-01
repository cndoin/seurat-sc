# Seurat 避坑清单

按「踩了会怎样」排序。每条都来自源码或官方行为，不是经验之谈。

---

## 一、v4 → v5 迁移（最容易静默出错）

| 变化 | v4 写法 | v5 正确写法 |
| --- | --- | --- |
| 数据层 | `slot = "data"` | 预处理链改用 `layer =` / `save =`（见下） |
| 多样本整合 | `FindIntegrationAnchors()` + `IntegrateData()` | 首选 `split()` + `IntegrateLayers()` + `JoinLayers()` |
| 取矩阵 | `obj@assays$RNA@data` | `LayerData(obj, layer = "data")` / `GetAssayData()` |
| 旧对象 | 直接分析 | `obj <- UpdateSeuratObject(obj)` |
| 高变基因 | `FindVariableGenes()` | `FindVariableFeatures()`（旧名已删除） |
| 打印 PCA | `do.print = TRUE` | `ndims.print` / `nfeatures.print` |
| 聚类算法 | `method = "igraph"` | `algorithm =`（`method` 已 deprecated） |

**`slot=` 弃用的 12 个函数**（源码里默认值就是 `deprecated()`）：
`Assays`、`AverageExpression`、`Features`、`FetchData`、
`FindSpatiallyVariableFeatures`、`GetAssayData`、`LayerData`、`LayerData<-`、
`PseudobulkExpression`、`RidgePlot`、`SetAssayData`、`VlnPlot`

**`slot=` 仍然合法的**（改成 layer 反而报错）：
`FindMarkers`、`FindAllMarkers`、`FindConservedMarkers`、`FoldChange`、
`DoHeatmap`、`DimHeatmap`、`FeaturePlot`、`RunUMAP`、`RunMixscape`、
`SpatialFeaturePlot`、`SpatialPlot`、`TransferData`、`AddModuleScore`、
`CalcPerturbSig`、`BuildClusterTree`、`PredictAssay`

另外两个已弃用参数：`FeaturePlot(sort.cell=)` → 用 `order=`；
`FindClusters(method=)` → 用 `algorithm=`。

---

## 二、不存在但常被写出来的函数（幻觉高发区）

| 幻觉写法 | 真相 |
| --- | --- |
| `RunWNN()` | 不存在。WNN = `FindMultiModalNeighbors()` → `RunUMAP(nn.name="weighted.nn")` → `FindClusters(graph.name="wsnn")` |
| `CoveragePlot()` | 属于 Signac，不在 Seurat |
| `FindVariableGenes()` | v3 旧名，已删除 |
| `ReadH5AD()` | 不存在，走 SeuratDisk 或 zellkonverter |
| `RunALRA()` / `RunDiffusionMap()` | 不存在 |
| `PerturbDiff()` / `TopDEGenesMixscape()` | 源码里有定义但**未导出**，用户调不到 |
| `RunMoransI(obj, features = ...)` | `RunMoransI(data, pos, verbose)`，**没有 features 参数**。要空间自相关用 `FindSpatiallyVariableFeatures(selection.method="moransi")` |
| `RenameIdents(obj, new.names = vec)` | 走 `...`，官方用法是位置传命名向量：`RenameIdents(obj, named_vec)` |

---

## 三、参数陷阱

1. **`dims` 不能拍脑袋。** `FindNeighbors(dims=)` / `RunUMAP(dims=)` 的 PC 数
   必须先用 `ElbowPlot(obj, ndims=50)` 定。随手写 `1:30` 会把噪声当信号，
   聚类结果全是假的。

2. **`resolution` 决定群数。** 0.4→少，1.2→多。没有"正确值"，
   先 0.5，看 marker 是否可解释再调。同一份数据换 resolution 就得重跑
   FindClusters → UMAP 不用重跑（但为此重画更稳）。

3. **`min.pct` 别设太小。** `min.pct=0` 会得到一堆只在 1 个细胞里表达的"marker"。
   常用 0.1~0.25。

4. **SCT 上找 marker 必须先 `PrepSCTFindMarkers()`。**
   不跑这一步，SCT 的 counts 没重建，logFC 和 p 值都不可信。
   `sc_lint.py` 检测到 `FindMarkers(assay="SCT")` 却没 prep 会告警。

5. **SCT 流程里不要再跑 `NormalizeData` / `ScaleData`。**
   SCTransform 已经产出 pearson residual（就是归一+校正后的结果），
   再 Scale 一遍等于二次处理。

6. **assay 必须显式。** 对象里同时有 RNA / SCT / sketch / integrated 时，
   不写 `assay=` 就走 `DefaultAssay()`，很容易算错 assay 还不报错。

7. **随机种子。** `RunUMAP(seed.use=42)`、`FindClusters(random.seed=0)`、
   `SCTransform(seed.use=1448145)`、`SketchData(seed=123)`、
   `FindMarkers(random.seed=1)`。不设就不可复现。

8. **`subset()` 的过滤条件参数名就叫 `subset`：**
   `subset(obj, subset = nFeature_RNA > 200)`。写成 `subset(obj, nFeature_RNA > 200)` 会报错。

---

## 四、性能与内存

| 症状 | 对策 |
| --- | --- |
| `ScaleData` 卡住 / 爆内存 | 只 scale 高变基因：`ScaleData(obj, features = VariableFeatures(obj))`；或分块 `block.size` |
| PCA 慢 | `RunPCA(approx = TRUE)`（默认就是 TRUE）；细胞多时别用 `RunPCA(approx=FALSE)` |
| SCTransform 内存高 | `SCTransform(conserve.memory = TRUE)` |
| 几十万~百万细胞 | 走 `SketchData()`；或 `BPCells` 把矩阵存磁盘 |
| 想并行 | `library(future); plan("multisession", workers = 4)`；Seurat v5 对多步有 future 支持 |
| 出图慢（点太多） | `DimPlot(raster = TRUE)` / `FeaturePlot(raster = TRUE)`，或直接存 `raster.dpi` |
| 反复读写对象 | 用 `SaveSeuratRds()`；对象里别塞太多冗余 reduction（`DietSeurat()` 精简） |

---

## 五、数据层面的坑

1. **物种决定基因大小写。** 人 `^MT-` / 小鼠 `^mt-`。搞反会得到全 0 的 percent.mt，
   QC 等于没做。**必须问用户确认物种，不要猜。**

2. **矩阵别转置错。** `CreateSeuratObject` 要求 行=基因、列=细胞。
   `Read10X` 会自动处理；自己读 mtx 时行rows对错了会报维度不匹配。

3. **重复 cell barcode。** 多样本 merge 不加 `add.cell.ids` 会撞名，
   Seurat 会报错或直接覆盖。

4. **Windows 中文/空格路径。** R 在 Windows 上对非 ASCII 路径敏感，
   工作目录一律用纯 ASCII。

5. **10x 目录结构。** `Read10X(data.dir)` 指向包含
   `barcodes.tsv.gz` / `features.tsv.gz` / `matrix.mtx.gz` 的那一层，
   不是它的父目录。Visium 则用 `Load10X_Spatial(data.dir)` 指向
   spaceranger 输出目录（含 `filtered_feature_bc_matrix.h5` 和 `spatial/`）。

---

## 六、结果解读的坑

1. **UMAP 上的"距离"没有定量意义。** 只能看"分没分开"，
   不能说"群 A 和群 B 更近所以更相似"。要定量看 `BuildClusterTree()` 或
   `AggregateExpression()` 后的相关性。

2. **cluster 数 ≠ 细胞类型数。** 同一个细胞类型常被拆成多个 cluster
   （因细胞周期、批次、应激），也可能一个 cluster 混了多种类型。
   注释看 marker，不看 cluster 编号。

3. **整合成功 ≠ 生物学正确。** 样本混匀了也可能是过整合
   （把真实差异抹掉了）。检查：已知 marker 是否还在、是否有样本特异的
   细胞类型被"抹平"。

4. **差异表达的 p 值在单细胞里天然极小。** 细胞数多时几乎所有基因都"显著"，
   必须同时看 `avg_log2FC` 和 `pct.1/pct.2`，不要只筛 `p_val_adj < 0.05`。

---

## 七、报错对照表

| 报错原文（关键字） | 原因 | 处置 |
| --- | --- | --- |
| `could not find function "xxx"` | 函数不存在 / 包没加载 | `library(Seurat)`；查 whitelist |
| `unused argument (xxx = ...)` | 参数名不存在 | `sc_api.py <函数名>` 查真实参数 |
| `Please run PrepSCTFindMarkers` | SCT 上直接 FindMarkers | 先跑 `PrepSCTFindMarkers()` |
| `Layer 'xxx' not found` | 层名错 / 没跑对应预处理 | `Layers(obj)` 看有哪些层 |
| `non-conformable arguments` | 矩阵维度不匹配 | 检查 ScaleData 是否成功、layer 是否对 |
| `Error in IntegrateLayers ... method` | method 传了字符串 | 传函数本身：`method = RPCAIntegration`（不加引号） |
| `there is no package called 'leidenbase'` | Leiden 算法缺依赖 | `install.packages("leidenbase")` 或改 `algorithm = 1`（Louvain） |
| `cannot allocate vector of size` | 内存不够 | 见性能表；ScaleData 只 scale HVG |
| `invalid 'times' argument` / dims 越界 | `dims` 超过实际 PC 数 | `RunPCA(npcs=)` 要 ≥ max(dims) |
