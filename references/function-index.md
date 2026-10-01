# Seurat 函数分类索引

版本：Seurat 5.5.1.9005 / SeuratObject 5.0.2。用于快速定位「该用哪个函数」；签名查 `api-signatures.md`。

| 模块 | 函数 |
| --- | --- |
| **io** 数据读取 / 写出 | `LoadAkoya`, `LoadAnnoyIndex`, `LoadCurioSeeker`, `LoadHuBMAPCODEX`, `LoadNanostring`, `LoadSeuratRds`, `LoadSTARmap`, `LoadVizgen`, `LoadXenium`, `Read10X`, `Read10X_Coordinates`, `Read10X_h5`, `Read10X_HD_GeoJson`, `Read10X_Image`, `Read10X_probe_metadata`, `Read10X_ScaleFactors`, `Read10X_Segmentations`, `ReadAkoya`, `ReadMtx`, `ReadNanostring`, `ReadParseBio`, `ReadSlideSeq`, `ReadSTARsolo`, `ReadVitessce`, `ReadVizgen`, `ReadXenium`, `SaveAnnoyIndex`, `SaveSeuratRds` |
| **object** 对象结构 / Layers 操作 | `.AssayClass`, `.BPMatrixMode`, `.CalcN`, `.CheckFmargin`, `.ClassPkg`, `.Collections`, `.Contains`, `.CreateStdAssay`, `.DefaultFOV`, `.Deprecate`, `.DiskLoad`, `.DollarNames`, `.FileMove`, `.FilePath`, `.FilterObjects`, `.FindObject`, `.GetMethod`, `.IsFutureSeurat`, `.MARGIN`, `.PropagateList`, `.SelectFeatures`, `.SparseSlots`, `.Subobjects`, `AddMetaData`, `aggregate`, `as.CellDataSet`, `as.Centroids`, `as.list`, `as.logical`, `as.matrix`, `as.Segmentation`, `Assays`, `AttachDeps`, `CastAssay`, `Cells`, `CheckDots`, `CheckFeaturesNames`, `CheckGC`, `CheckLayersName`, `CheckMatrix`, `ClassKey`, `Command`, `components`, `CreateAssay5Object`, `CreateAssayObject`, `CreateDimReducObject`, `CreateSCTAssayObject`, `CreateSeuratObject`, `DefaultAssay`, `DefaultAssay<-`, `DefaultBoundary<-`, `DefaultDimReduc`, `DefaultFOV<-`, `DefaultLayer`, `DefaultLayer<-`, `Degrees`, `DietSeurat`, `dim`, `dimnames`, `Distances`, `droplevels`, `EmptyDF`, `EmptyMatrix`, `ExtractField`, `Features`, `FetchData`, `FilterObjects`, `GetAssay`, `GetAssayData`, `Graphs`, `head`, `Index`, `Index<-`, `Indices`, `intersect`, `IsNamedList`, `IsS4List`, `IsSparse`, `JoinLayers`, `JS`, `JS<-`, `Key`, `Key<-`, `Keys`, `labels`, `LayerData`, `LayerData<-`, `Layers`, `length`, `lengths`, `levels`, `ListToS4`, `LogMap`, `LogSeuratCommand`, `MatchCells`, `merge`, `Misc`, `Misc<-`, `Molecules`, `names`, `Neighbors`, `PackageCheck`, `PolyVtx`, `print`, `Project`, `Project<-`, `Radians`, `Reductions`, `RegisterSparseMatrix`, `RenameAssays`, `RenameCells`, `S4ToList`, `SetAssayData`, `Simplify`, `SparseEmptyMatrix`, `SpatiallyVariableFeatures`, `split`, `SplitObject`, `Stdev`, `StitchMatrix`, `subset`, `SVFInfo`, `tail`, `Theta`, `Tool`, `Tool<-`, `TopCells`, `TopNeighbors`, `UpdateSCTAssays`, `UpdateSeuratObject`, `UpdateSlots`, `upgrade`, `Version` |
| **qc** 质量控制 / 去双细胞 / 细胞周期 | `BarcodeInflectionsPlot`, `CalculateBarcodeInflections`, `GetResidual`, `HTODemux`, `HTOHeatmap`, `MULTIseqDemux`, `PercentageFeatureSet`, `SampleUMI`, `SubsetByBarcodeInflections` |
| **norm** 归一化 / SCTransform / ScaleData | `FetchResiduals`, `LogNormalize`, `NormalizeData`, `PrepSCTFindMarkers`, `PrepSCTIntegration`, `RelativeCounts`, `ScaleData`, `SCTransform`, `SCTResults`, `SelectSCTIntegrationFeatures` |
| **hvg** 高变基因 / 空间可变基因 | `FindVariableFeatures`, `HVFInfo`, `TopFeatures`, `VariableFeatures`, `VariableFeatures<-`, `VST` |
| **dr** 降维 PCA / UMAP / tSNE / SLSI | `DimHeatmap`, `ElbowPlot`, `Embeddings`, `JackStraw`, `JackStrawPlot`, `L2CCA`, `L2Dim`, `Loadings`, `Loadings<-`, `PCAPlot`, `PCASigGenes`, `PCHeatmap`, `ProjectDim`, `ProjectUMAP`, `RunCCA`, `RunICA`, `RunPCA`, `RunSLSI`, `RunSPCA`, `RunTSNE`, `RunUMAP`, `ScoreJackStraw`, `VizDimLoadings` |
| **cluster** 聚类 / 分群注释 / 聚类树 | `CellsByIdentities`, `FindClusters`, `FindNeighbors`, `FindSubCluster`, `Idents`, `Idents<-`, `NNPlot`, `PlotClusterTree`, `RegroupIdents`, `RenameIdents`, `ReorderIdent`, `RunLeiden`, `SetIdent`, `SetQuantile`, `StashIdent`, `WhichCells` |
| **de** 差异表达 / 拟 bulk 聚合 | `AggregateExpression`, `AverageExpression`, `CreateCategoryMatrix`, `FindAllMarkers`, `FindConservedMarkers`, `FindMarkers`, `FoldChange`, `PseudobulkExpression` |
| **integrate** 多样本整合 / 参考映射 / Bridge | `AddAzimuthResults`, `AnnotateAnchors`, `BridgeCellsRepresentation`, `CCAIntegration`, `FastRPCAIntegration`, `FindBridgeIntegrationAnchors`, `FindBridgeTransferAnchors`, `FindIntegrationAnchors`, `FindTransferAnchors`, `GetIntegrationData`, `GetTransferPredictions`, `HarmonyIntegration`, `IntegrateData`, `IntegrateEmbeddings`, `IntegrateLayers`, `JointPCAIntegration`, `LocalStruct`, `MappingScore`, `MapQuery`, `MixingMetric`, `NNtoGraph`, `PredictAssay`, `PrepareBridgeReference`, `ProjectCellEmbeddings`, `ProjectDimReduc`, `ProjectIntegration`, `RPCAIntegration`, `RunGraphLaplacian`, `SelectIntegrationFeatures`, `SelectIntegrationFeatures5`, `SetIntegrationData`, `TransferData` |
| **sketch** Sketch 大数据草图 | `CountSketch`, `GaussianSketch`, `LeverageScore`, `ProjectData`, `SketchData`, `TransferSketchLabels`, `UnSketchEmbeddings` |
| **viz** 可视化 | `AugmentPlot`, `AutoPointSize`, `BGTextColor`, `BlackAndWhite`, `BlueAndRed`, `BoldTitle`, `CellScatter`, `CellSelector`, `CenterTitle`, `CollapseEmbeddingOutliers`, `ColorDimSplit`, `CombinePlots`, `CustomPalette`, `DarkTheme`, `DimPlot`, `DiscretePalette`, `DoHeatmap`, `DotPlot`, `FeatureLocator`, `FeaturePlot`, `FeatureScatter`, `FontSize`, `fortify`, `GroupCorrelationPlot`, `HoverLocator`, `IFeaturePlot`, `ImageDimPlot`, `ImageFeaturePlot`, `Intensity`, `InteractiveSpatialPlot`, `ISpatialDimPlot`, `ISpatialFeaturePlot`, `LabelClusters`, `LabelPoints`, `LinkedDimPlot`, `LinkedFeaturePlot`, `Luminance`, `NoAxes`, `NoGrid`, `NoLegend`, `PolyDimPlot`, `PolyFeaturePlot`, `PurpleAndYellow`, `RestoreLegend`, `RidgePlot`, `RotatedAxis`, `SeuratAxes`, `SeuratTheme`, `SingleCorPlot`, `SingleDimPlot`, `SingleExIPlot`, `SingleImageMap`, `SingleImagePlot`, `SingleRasterMap`, `SingleSpatialPlot`, `SpatialDimPlot`, `SpatialFeaturePlot`, `SpatialPlot`, `SpatialTheme`, `TSNEPlot`, `UMAPPlot`, `VariableFeaturePlot`, `VlnPlot`, `WhiteBackground` |
| **spatial** 空间转录组 | `Boundaries`, `BuildNicheAssay`, `CreateCentroids`, `CreateFOV`, `CreateMolecules`, `CreateSegmentation`, `Crop`, `DefaultBoundary`, `DefaultFOV`, `FilterSlideSeq`, `FindSpatiallyVariableFeatures`, `GetImage`, `GetTissueCoordinates`, `Images`, `Load10X_Spatial`, `Overlay`, `Radius`, `RunMarkVario`, `RunMoransI`, `ScaleFactors`, `scalefactors` |
| **multiome** 多模态 / WNN | `FindMultiModalNeighbors` |
| **perturb** Mixscape / 扰动 | `CalcPerturbSig`, `DEenrichRPlot`, `MixscapeHeatmap`, `MixscapeLDA`, `PlotPerturbScore`, `PrepLDA`, `RunLDA`, `RunMixscape` |
| **tree** 聚类树工具 | `BuildClusterTree` |
| **convert** 格式转换 | `as.Graph`, `as.Neighbor`, `as.Seurat`, `as.SingleCellExperiment`, `as.sparse` |
| **util** 通用工具 / 模块评分 | `AddModuleScore`, `as.data.frame`, `CaseMatch`, `CellCycleScoring`, `CollapseSpeciesExpressionMatrix`, `CustomDistance`, `ExpMean`, `ExpSD`, `ExpVar`, `FastRowScale`, `GeneSymbolThesarus`, `GroupCorrelation`, `IsGlobal`, `IsMatrixEmpty`, `LogVMR`, `MetaFeature`, `MinMax`, `PercentAbove`, `RandomName`, `RowMergeSparseMatrices`, `UpdateSymbolList` |
| **misc** 其他 | `%!NA%`, `%!na%`, `%iff%`, `%NA%`, `%na%`, `%||%`, `.KeyPattern`, `.RandomKey`, `handlers`, `plan`, `SCTResults<-`, `t`, `with_progress` |

## S3 method 覆盖（506 条）

形如 `generic.class`；调用时写 `generic(obj, ...)` 由 R 自动分派。

| generic | 支持的方法类 |
| --- | --- |
| `.AssayClass` | `Assay5T`, `StdAssay`, `default` |
| `.CalcN` | `Assay`, `IterableMatrix`, `StdAssay`, `default` |
| `.ClassPkg` | `DelayedArray`, `R6`, `R6ClassGenerator`, `default` |
| `.CreateStdAssay` | `Matrix`, `default`, `list`, `matrix` |
| `.DiskLoad` | `10xMatrixH5`, `AnnDataMatrixH5`, `DelayedMatrix`, `H5ADMatrix`, `HDF5Matrix`, `IterableMatrix`, `MatrixDir`, `MatrixH5`, `TileDBMatrix`, `default` |
| `.DollarNames` | `Assay`, `Assay5`, `FOV`, `JackStrawData`, `Seurat`, `SeuratCommand`, `StdAssay` |
| `.FilePath` | `DelayedMatrix`, `IterableMatrix`, `default` |
| `.MARGIN` | `Assay5T`, `CsparseMatrix`, `RsparseMatrix`, `default`, `spam` |
| `.SelectFeatures` | `StdAssay`, `list` |
| `.SparseSlots` | `CsparseMatrix`, `RsparseMatrix`, `spam` |
| `AddMetaData` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `AddModuleScore` | `Assay`, `Seurat`, `StdAssay` |
| `aggregate` | `FOV`, `Molecules` |
| `AnnotateAnchors` | `IntegrationAnchorSet`, `TransferAnchorSet`, `default` |
| `as.CellDataSet` | `Seurat` |
| `as.Centroids` | `Segmentation` |
| `as.data.frame` | `Matrix` |
| `as.Graph` | `Matrix`, `Neighbor`, `matrix` |
| `as.list` | `SeuratCommand` |
| `as.logical` | `JackStrawData` |
| `as.matrix` | `LogMap` |
| `as.Neighbor` | `Graph` |
| `as.Segmentation` | `Centroids` |
| `as.Seurat` | `CellDataSet`, `SingleCellExperiment` |
| `as.SingleCellExperiment` | `Seurat` |
| `as.sparse` | `H5Group`, `IterableMatrix`, `Matrix`, `data.frame`, `matrix`, `ngCMatrix` |
| `Assays` | `Seurat` |
| `Boundaries` | `FOV` |
| `CastAssay` | `Assay5`, `Seurat`, `StdAssay` |
| `Cells` | `Assay5`, `Centroids`, `DimReduc`, `FOV`, `Graph`, `Neighbor`, `SCTAssay`, `SCTModel`, `STARmap`, `Segmentation`, `Seurat`, `SlideSeq`, `SpatialImage`, `StdAssay`, `VisiumV1`, `default` |
| `CheckMatrix` | `dMatrix`, `default`, `lMatrix` |
| `Command` | `Seurat` |
| `components` | `SCTAssay` |
| `CreateCentroids` | `Centroids`, `default` |
| `CreateFOV` | `Centroids`, `Segmentation`, `data.frame`, `list` |
| `CreateMolecules` | `Molecules`, `NULL`, `data.frame` |
| `CreateSegmentation` | `Segmentation`, `data.frame` |
| `CreateSeuratObject` | `Assay`, `Assay5`, `StdAssay`, `default` |
| `Crop` | `Centroids`, `FOV`, `Molecules`, `Segmentation` |
| `DefaultAssay` | `Assay`, `Assay5`, `DimReduc`, `Graph`, `Seurat`, `SeuratCommand`, `SpatialImage`, `StdAssay` |
| `DefaultAssay<-` | `Assay`, `Assay5`, `DimReduc`, `Graph`, `Seurat`, `SpatialImage`, `StdAssay` |
| `DefaultBoundary` | `FOV` |
| `DefaultBoundary<-` | `FOV` |
| `DefaultFOV` | `Seurat` |
| `DefaultFOV<-` | `Seurat` |
| `DefaultLayer` | `Assay`, `Assay5`, `StdAssay` |
| `DefaultLayer<-` | `Assay5`, `StdAssay` |
| `dim` | `Assay`, `Assay5`, `DimReduc`, `FOV`, `Neighbor`, `STARmap`, `Seurat`, `SlideSeq`, `SpatialImage`, `StdAssay`, `VisiumV1`, `VisiumV2` |
| `dimnames` | `Assay`, `Assay5`, `DimReduc`, `Seurat`, `StdAssay` |
| `dimnames<-` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `Distances` | `Neighbor` |
| `droplevels` | `LogMap`, `Seurat` |
| `Embeddings` | `DimReduc`, `Seurat` |
| `Features` | `Assay`, `Assay5`, `DimReduc`, `FOV`, `Molecules`, `SCTAssay`, `SCTModel`, `Seurat`, `StdAssay` |
| `FetchData` | `Assay`, `Assay5`, `DimReduc`, `FOV`, `Molecules`, `Seurat`, `StdAssay`, `VisiumV1` |
| `FetchResiduals` | `SCTAssay`, `Seurat` |
| `FindClusters` | `Seurat`, `default` |
| `FindMarkers` | `Assay`, `DimReduc`, `SCTAssay`, `Seurat`, `StdAssay`, `default` |
| `FindNeighbors` | `Assay`, `Seurat`, `default`, `dist` |
| `FindSpatiallyVariableFeatures` | `Assay`, `Seurat`, `StdAssay`, `default` |
| `FindVariableFeatures` | `Assay`, `SCTAssay`, `Seurat`, `StdAssay`, `V3Matrix`, `default` |
| `FoldChange` | `Assay`, `DimReduc`, `SCTAssay`, `Seurat`, `StdAssay`, `default` |
| `fortify` | `Centroids`, `Molecules`, `Segmentation` |
| `GetAssay` | `Seurat` |
| `GetAssayData` | `Assay`, `Seurat`, `StdAssay` |
| `GetImage` | `STARmap`, `Seurat`, `SlideSeq`, `SpatialImage`, `VisiumV1`, `VisiumV2` |
| `GetTissueCoordinates` | `Centroids`, `FOV`, `Molecules`, `STARmap`, `Segmentation`, `Seurat`, `SlideSeq`, `SpatialImage`, `VisiumV1`, `VisiumV2` |
| `head` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `HVFInfo` | `Assay`, `Assay5`, `SCTAssay`, `Seurat`, `StdAssay` |
| `Idents` | `Seurat` |
| `Idents<-` | `Seurat` |
| `Index` | `Neighbor` |
| `Index<-` | `Neighbor` |
| `Indices` | `Neighbor` |
| `IntegrateEmbeddings` | `IntegrationAnchorSet`, `TransferAnchorSet` |
| `intersect` | `LogMap` |
| `is.finite` | `Centroids` |
| `is.infinite` | `Centroids` |
| `IsGlobal` | `DimReduc`, `SpatialImage`, `default` |
| `IsMatrixEmpty` | `default` |
| `JoinLayers` | `Assay5`, `Seurat`, `StdAssay` |
| `JS` | `DimReduc`, `JackStrawData` |
| `JS<-` | `DimReduc`, `JackStrawData` |
| `Key` | `Assay`, `Assay5`, `DimReduc`, `KeyMixin`, `NULL`, `Seurat`, `SpatialImage`, `character` |
| `Key<-` | `Assay`, `Assay5`, `DimReduc`, `KeyMixin`, `SpatialImage` |
| `Keys` | `FOV`, `Seurat` |
| `labels` | `LogMap` |
| `LayerData` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `LayerData<-` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `Layers` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `length` | `Centroids`, `DimReduc`, `FOV` |
| `lengths` | `Centroids`, `Segmentation` |
| `levels` | `SCTAssay`, `Seurat` |
| `levels<-` | `SCTAssay`, `Seurat` |
| `LeverageScore` | `Assay`, `Seurat`, `StdAssay`, `default` |
| `Loadings` | `DimReduc`, `Seurat` |
| `Loadings<-` | `DimReduc` |
| `LogNormalize` | `IterableMatrix`, `V3Matrix`, `data.frame`, `default` |
| `MappingScore` | `AnchorSet`, `default` |
| `MatchCells` | `NULL`, `character`, `numeric` |
| `merge` | `Assay`, `Assay5`, `DimReduc`, `SCTAssay`, `Seurat`, `StdAssay` |
| `Misc` | `Assay`, `Assay5`, `DimReduc`, `Seurat`, `StdAssay` |
| `Misc<-` | `Assay`, `Assay5`, `DimReduc`, `Seurat`, `StdAssay` |
| `Molecules` | `FOV` |
| `names` | `DimReduc`, `FOV`, `Seurat` |
| `NormalizeData` | `Assay`, `Seurat`, `StdAssay`, `V3Matrix`, `default` |
| `print` | `DimReduc` |
| `Project` | `Seurat` |
| `Project<-` | `Seurat` |
| `ProjectCellEmbeddings` | `Assay`, `IterableMatrix`, `SCTAssay`, `Seurat`, `StdAssay`, `default` |
| `ProjectUMAP` | `DimReduc`, `Seurat`, `default` |
| `PseudobulkExpression` | `Assay`, `Seurat`, `StdAssay` |
| `Radius` | `Centroids`, `STARmap`, `SlideSeq`, `SpatialImage`, `VisiumV1`, `VisiumV2` |
| `RenameCells` | `Assay`, `Assay5`, `Centroids`, `DimReduc`, `FOV`, `Neighbor`, `SCTAssay`, `STARmap`, `Segmentation`, `Seurat`, `SlideSeq`, `SpatialImage`, `StdAssay`, `VisiumV1` |
| `RenameIdents` | `Seurat` |
| `ReorderIdent` | `Seurat` |
| `RunCCA` | `Seurat`, `default` |
| `RunGraphLaplacian` | `Seurat`, `default` |
| `RunICA` | `Assay`, `Seurat`, `StdAssay`, `default` |
| `RunLDA` | `Assay`, `Seurat`, `default` |
| `RunPCA` | `Assay`, `Seurat`, `Seurat5`, `StdAssay`, `default` |
| `RunSLSI` | `Assay`, `Seurat`, `StdAssay`, `default` |
| `RunSPCA` | `Assay`, `Assay5`, `Seurat`, `default` |
| `RunTSNE` | `DimReduc`, `Seurat`, `dist`, `matrix` |
| `RunUMAP` | `Graph`, `Neighbor`, `Seurat`, `default` |
| `S4ToList` | `default`, `list` |
| `ScaleData` | `Assay`, `IterableMatrix`, `Seurat`, `StdAssay`, `default` |
| `ScaleFactors` | `STARmap`, `SlideSeq`, `VisiumV1`, `VisiumV2` |
| `ScoreJackStraw` | `DimReduc`, `JackStrawData`, `Seurat` |
| `SCTransform` | `Assay`, `IterableMatrix`, `Seurat`, `StdAssay`, `default` |
| `SCTResults` | `SCTAssay`, `SCTModel`, `Seurat` |
| `SCTResults<-` | `SCTAssay`, `SCTModel` |
| `SetAssayData` | `Assay`, `Seurat`, `StdAssay` |
| `SetIdent` | `Seurat` |
| `Simplify` | `Molecules`, `Spatial` |
| `SpatiallyVariableFeatures` | `Assay`, `Seurat` |
| `split` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `StashIdent` | `Seurat` |
| `Stdev` | `DimReduc`, `Seurat` |
| `StitchMatrix` | `IterableMatrix`, `default`, `dgCMatrix`, `matrix` |
| `subset` | `AnchorSet`, `Assay`, `Assay5`, `Centroids`, `DimReduc`, `FOV`, `Molecules`, `SCTAssay`, `STARmap`, `Segmentation`, `Seurat`, `SlideSeq`, `SpatialImage`, `StdAssay`, `VisiumV1` |
| `SVFInfo` | `Assay`, `Seurat` |
| `tail` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `Theta` | `Centroids` |
| `Tool` | `Seurat` |
| `Tool<-` | `Seurat` |
| `upgrade` | `seurat` |
| `VariableFeatures` | `Assay`, `Assay5`, `SCTAssay`, `SCTModel`, `Seurat`, `StdAssay` |
| `VariableFeatures<-` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |
| `Version` | `Seurat` |
| `VST` | `IterableMatrix`, `default`, `dgCMatrix`, `matrix` |
| `WhichCells` | `Assay`, `Assay5`, `Seurat`, `StdAssay` |

## S4 类（16）

`AnchorSet`, `Assay`, `BridgeReferenceSet`, `DimReduc`, `Graph`, `IntegrationAnchorSet`, `IntegrationData`, `JackStrawData`, `ModalityWeights`, `Neighbor`, `Seurat`, `SeuratCommand`, `SpatialImage`, `TransferAnchorSet`, `VisiumV1`, `VisiumV2`
