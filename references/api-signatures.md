# Seurat 全量函数签名库（自源码提取，非文档转述）

> 数据源：github.com/satijalab/seurat `master`（Seurat 5.5.1.9005） + mojaveazure/seurat-object `develop`（SeuratObject 5.0.2）。
> 每条签名由 `R/` 源码的真实 `formals` 解析得到；S3 generic 取其全部 method 参数的并集。
> 用法：`grep -n "^## <函数名>" references/api-signatures.md` 精确查，不要整篇读。

共 406 个已知符号，其中 390 个解析到真实参数表。


## MODULE: io — 数据读取 / 写出（28）

### LoadAkoya
`LoadAkoya(filename, type=c('inform', 'processor', 'qupath'), fov, assay='Akoya', ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：LoadAkoya

### LoadAnnoyIndex
`LoadAnnoyIndex(object, file)`

- 来源：`utilities.R` · 包：Seurat · 实现：LoadAnnoyIndex

### LoadCurioSeeker
`LoadCurioSeeker(data.dir, assay="Spatial")`

- 来源：`preprocessing.R` · 包：Seurat · 实现：LoadCurioSeeker

### LoadHuBMAPCODEX
`LoadHuBMAPCODEX(data.dir, fov, assay='CODEX')`

- 来源：`convenience.R` · 包：Seurat · 实现：LoadHuBMAPCODEX

### LoadNanostring
`LoadNanostring(data.dir, fov, assay='Nanostring')`

- 来源：`convenience.R` · 包：Seurat · 实现：LoadNanostring

### LoadSeuratRds
`LoadSeuratRds(file, ...)`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：LoadSeuratRds

### LoadSTARmap
`LoadSTARmap(data.dir, counts.file="cell_barcode_count.csv", gene.file="genes.csv", qhull.file="qhulls.tsv", centroid.file="centroids.tsv", assay="Spatial", image="image")`

- 来源：`preprocessing.R` · 包：Seurat · 实现：LoadSTARmap

### LoadVizgen
`LoadVizgen(data.dir, fov, assay='Vizgen', z=3L)`

- 来源：`convenience.R` · 包：Seurat · 实现：LoadVizgen

### LoadXenium
`LoadXenium(data.dir, fov='fov', assay='Xenium', mols.qv.threshold=20, cell.centroids=TRUE, molecule.coordinates=TRUE, segmentations=NULL, flip.xy=FALSE)`

- 来源：`convenience.R` · 包：Seurat · 实现：LoadXenium

### Read10X
`Read10X(data.dir, gene.column=2, cell.column=1, unique.features=TRUE, strip.suffix=FALSE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X

### Read10X_Coordinates
`Read10X_Coordinates(filename, filter.matrix)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_Coordinates

### Read10X_h5
`Read10X_h5(filename, use.names=TRUE, unique.features=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_h5

### Read10X_HD_GeoJson
`Read10X_HD_GeoJson(data.dir, segmentation.type="cell")`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_HD_GeoJson

### Read10X_Image
`Read10X_Image(image.dir, image.name="tissue_lowres_image.png", assay="Spatial", slice="slice1", filter.matrix=TRUE, image.type="VisiumV2")`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_Image

### Read10X_probe_metadata
`Read10X_probe_metadata(data.dir, filename='raw_probe_bc_matrix.h5')`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_probe_metadata

### Read10X_ScaleFactors
`Read10X_ScaleFactors(filename)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_ScaleFactors

### Read10X_Segmentations
`Read10X_Segmentations(image.dir, data.dir, image.name="tissue_lowres_image.png", assay="Spatial.Polygons", slice="slice1.polygons", segmentation.type="cell", compact=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Read10X_Segmentations

### ReadAkoya
`ReadAkoya(filename, type=c('inform', 'processor', 'qupath'), filter='DAPI|Blank|Empty', inform.quant=c('mean', 'total', 'min', 'max', 'std'))`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadAkoya

### ReadMtx
`ReadMtx(mtx, cells, features, cell.column=1, feature.column=2, cell.sep="\t", feature.sep="\t", skip.cell=0, skip.feature=0, mtx.transpose=FALSE, unique.features=TRUE, strip.suffix=FALSE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadMtx

### ReadNanostring
`ReadNanostring(data.dir, mtx.file=NULL, metadata.file=NULL, molecules.file=NULL, segmentations.file=NULL, type='centroids', mol.type='pixels', metadata=NULL, mols.filter=NA_character_, genes.filter=NA_character_, fov.filter=NULL, subset.counts.matrix=NULL, cell.mols.only=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadNanostring

### ReadParseBio
`ReadParseBio(data.dir, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：ReadParseBio

### ReadSlideSeq
`ReadSlideSeq(coord.file, assay='Spatial')`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadSlideSeq

### ReadSTARsolo
`ReadSTARsolo(data.dir, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：ReadSTARsolo

### ReadVitessce
`ReadVitessce(counts=NULL, coords=NULL, molecules=NULL, type=c('segmentations', 'centroids'), filter=NA_character_)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadVitessce

### ReadVizgen
`ReadVizgen(data.dir, transcripts=NULL, spatial=NULL, molecules=NULL, type='segmentations', mol.type='microns', metadata=NULL, filter=NA_character_, z=3L)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadVizgen

### ReadXenium
`ReadXenium(data.dir, outs=c("segmentation_method", "matrix", "m..., type="centroids", mols.qv.threshold=20, flip.xy=F)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ReadXenium

### SaveAnnoyIndex
`SaveAnnoyIndex(object, file)`

- 来源：`utilities.R` · 包：Seurat · 实现：SaveAnnoyIndex

### SaveSeuratRds
`SaveSeuratRds(object, file=NULL, move=TRUE, destdir=deprecated(), relative=FALSE, ...)`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：SaveSeuratRds


## MODULE: object — 对象结构 / Layers 操作（133）

### .AssayClass
`.AssayClass(object)`

- 来源：`SO:utils.R` · 包：S3 · 实现：.AssayClass.default
- 方法变体：`*Assay5T*`, `*StdAssay*`, `*default*`

### .BPMatrixMode
`.BPMatrixMode(object, simplify=FALSE)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.BPMatrixMode

### .CalcN
`.CalcN(object, layer='counts', simplify=TRUE, ...)`

- 来源：`SO:assay5.R` · 包：S3 · 实现：.CalcN.default
- 方法变体：`*Assay*`, `*IterableMatrix*`, `*StdAssay*`, `*default*`

### .CheckFmargin
`.CheckFmargin(fmargin)`

- 来源：`SO:layers.R` · 包：SeuratObject · 实现：.CheckFmargin

### .ClassPkg
`.ClassPkg(object)`

- 来源：`SO:utils.R` · 包：S3 · 实现：.ClassPkg.default
- 方法变体：`*DelayedArray*`, `*R6*`, `*R6ClassGenerator*`, `*default*`

### .Collections
`.Collections(object, exclude=character(length = 0L), ...)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.Collections

### .Contains
`.Contains(object)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.Contains

### .CreateStdAssay
`.CreateStdAssay(counts, min.cells=0, min.features=0, cells=NULL, features=NULL, transpose=FALSE, type='Assay5', layer='counts', csum=Matrix::colSums, fsum=Matrix::rowSums, ...)`

- 来源：`SO:assay5.R` · 包：S3 · 实现：.CreateStdAssay.default
- 方法变体：`*Matrix*`, `*default*`, `*list*`

### .DefaultFOV
`.DefaultFOV(object, assay=NULL)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.DefaultFOV

### .Deprecate
`.Deprecate(when, what, with=NULL, ..., pkg=NULL, env=missing_arg(), user_env=missing_arg())`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.Deprecate

### .DiskLoad
`.DiskLoad(x)`

- 来源：`SO:utils.R` · 包：S3 · 实现：.DiskLoad.default
- 方法变体：`*10xMatrixH5*`, `*AnnDataMatrixH5*`, `*DelayedMatrix*`, `*H5ADMatrix*`, `*HDF5Matrix*`, `*IterableMatrix*`, `*MatrixDir*`, `*MatrixH5*`, `*TileDBMatrix*`, `*default*`

### .DollarNames
`.DollarNames(x, pattern='')`

- 来源：`SO:assay.R` · 包：S3 · 实现：.DollarNames.Assay
- 方法变体：`*Assay*`, `*FOV*`, `*StdAssay*`

### .FileMove
`.FileMove(path, new_path, overwrite=FALSE, n=1L)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.FileMove

### .FilePath
`.FilePath(x)`

- 来源：`SO:utils.R` · 包：S3 · 实现：.FilePath.default
- 方法变体：`*DelayedMatrix*`, `*IterableMatrix*`, `*default*`

### .FilterObjects
`.FilterObjects(object, classes.keep=c('Assay', 'StdAssay', 'DimReduc'))`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.FilterObjects

### .FindObject
`.FindObject(object, name, exclude=c('misc', 'tools'))`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.FindObject

### .GetMethod
`.GetMethod(fxn, cls)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.GetMethod

### .IsFutureSeurat
`.IsFutureSeurat(version, lib.loc=NULL)`

- 来源：`SO:zzz.R` · 包：SeuratObject · 实现：.IsFutureSeurat

### .MARGIN
`.MARGIN(x, type=c('features', 'cells'), ...)`

- 来源：`SO:default.R` · 包：S3 · 实现：.MARGIN.default
- 方法变体：`*Assay5T*`, `*CsparseMatrix*`, `*RsparseMatrix*`, `*default*`

### .PropagateList
`.PropagateList(x, names, default=NA)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.PropagateList

### .SelectFeatures
`.SelectFeatures(object, all.features=NULL, nfeatures=Inf, ...)`

- 来源：`SO:assay5.R` · 包：S3 · 实现：.SelectFeatures.StdAssay
- 方法变体：`*StdAssay*`, `*list*`

### .SparseSlots
`.SparseSlots(x, type=c('pointers', 'entries', 'indices'))`

- 来源：`SO:sparse.R` · 包：S3 · 实现：.SparseSlots.CsparseMatrix
- 方法变体：`*CsparseMatrix*`, `*RsparseMatrix*`, `*spam*`

### .Subobjects
`.Subobjects(object, exclude=c('misc', 'tools'), collapse=TRUE, ...)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：.Subobjects

### AddMetaData
`AddMetaData(object, metadata, col.name=NULL)`

- 来源：`SO:assay.R` · 包：Seurat · 实现：AddMetaData.Assay
- 方法变体：`*Assay*`

### aggregate
`aggregate(x, by=NULL, set=NULL, drop=TRUE, ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：aggregate.FOV
- 方法变体：`*FOV*`, `*Molecules*`

### as.CellDataSet
`as.CellDataSet(x, assay=NULL, reduction=NULL, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：as.CellDataSet.Seurat
- 方法变体：`*Seurat*`

### as.Centroids
`as.Centroids(x, nsides=NULL, radius=NULL, theta=NULL, ...)`

- 来源：`SO:utils.R` · 包：S3 · 实现：as.Centroids.Segmentation
- 方法变体：`*Segmentation*`

### as.list
`as.list(x, complete=FALSE, ...)`

- 来源：`SO:command.R` · 包：S3 · 实现：as.list.SeuratCommand
- 方法变体：`*SeuratCommand*`

### as.logical
`as.logical(x, ...)`

- 来源：`SO:jackstraw.R` · 包：S3 · 实现：as.logical.JackStrawData
- 方法变体：`*JackStrawData*`

### as.matrix
`as.matrix(x, ...)`

- 来源：`SO:logmap.R` · 包：S3 · 实现：as.matrix.LogMap
- 方法变体：`*LogMap*`

### as.Segmentation
`as.Segmentation(x, ...)`

- 来源：`SO:utils.R` · 包：S3 · 实现：as.Segmentation.Centroids
- 方法变体：`*Centroids*`

### Assays
`Assays(object, slot=deprecated(), ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Assays.Seurat
- 方法变体：`*Seurat*`

### AttachDeps
`AttachDeps(deps)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：AttachDeps

### CastAssay
`CastAssay(object, to, assay=NULL, layers=NA, verbose=TRUE, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：CastAssay.Seurat
- 方法变体：`*Seurat*`, `*StdAssay*`

### Cells
`Cells(x, layer=NULL, simplify=TRUE, boundary=NULL, margin=1L, assay=NULL, ...)`

- 来源：`SO:default.R` · 包：Seurat · 实现：Cells.default
- 方法变体：`*Centroids*`, `*DimReduc*`, `*FOV*`, `*Graph*`, `*Neighbor*`, `*SCTAssay*`, `*SCTModel*`, `*STARmap*`, `*Segmentation*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`

### CheckDots
`CheckDots(..., fxns=NULL)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：CheckDots

### CheckFeaturesNames
`CheckFeaturesNames(data)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：CheckFeaturesNames

### CheckGC
`CheckGC(option='SeuratObject.memsafe')`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：CheckGC

### CheckLayersName
`CheckLayersName(matrix.list, layers.type=c('counts', 'data'))`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：CheckLayersName

### CheckMatrix
`CheckMatrix(object, checks=c('infinite', 'logical', 'integer', '..., ...)`

- 来源：`SO:utils.R` · 包：S3 · 实现：CheckMatrix.default
- 方法变体：`*dMatrix*`, `*default*`, `*lMatrix*`

### ClassKey
`ClassKey(class, package=NULL)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：ClassKey

### Command
`Command(object, command=NULL, value=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Command.Seurat
- 方法变体：`*Seurat*`

### components
`components(object, model, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：components.SCTAssay

### CreateAssay5Object
`CreateAssay5Object(counts=NULL, data=NULL, min.cells=0, min.features=0, csum=NULL, fsum=NULL, ...)`

- 来源：`SO:assay5.R` · 包：SeuratObject · 实现：CreateAssay5Object

### CreateAssayObject
`CreateAssayObject(counts, data, min.cells=0, min.features=0, key=NULL, check.matrix=FALSE, ...)`

- 来源：`SO:assay.R` · 包：Seurat · 实现：CreateAssayObject

### CreateDimReducObject
`CreateDimReducObject(embeddings=new(Class = 'matrix'), loadings=new(Class = 'matrix'), projected=new(Class = 'matrix'), assay=NULL, stdev=numeric(), key=NULL, global=FALSE, jackstraw=NULL, misc=list())`

- 来源：`SO:dimreduc.R` · 包：Seurat · 实现：CreateDimReducObject

### CreateSCTAssayObject
`CreateSCTAssayObject(counts, data, scale.data=NULL, umi.assay="RNA", min.cells=0, min.features=0, SCTModel.list=NULL)`

- 来源：`objects.R` · 包：Seurat · 实现：CreateSCTAssayObject

### CreateSeuratObject
`CreateSeuratObject(counts, assay='RNA', names.field=1L, names.delim='_', meta.data=NULL, project='SeuratProject', min.cells=0, min.features=0, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：CreateSeuratObject.default
- 方法变体：`*Assay*`, `*default*`

### DefaultAssay
`DefaultAssay(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：DefaultAssay.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*Graph*`, `*Seurat*`, `*SeuratCommand*`, `*SpatialImage*`, `*StdAssay*`

### DefaultAssay<-
`DefaultAssay<-(object, ...)`

- 来源：`SO:assay.R` · 包：Seurat · 实现：DefaultAssay.Assay

### DefaultBoundary<-
`DefaultBoundary<-(object)`

- 来源：`SO:fov.R` · 包：SeuratObject · 实现：DefaultBoundary.FOV

### DefaultDimReduc
`DefaultDimReduc(object, assay=NULL)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：DefaultDimReduc

### DefaultFOV<-
`DefaultFOV<-(object, assay=NULL, ...)`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：DefaultFOV.Seurat

### DefaultLayer
`DefaultLayer(object, ...)`

- 来源：`SO:assay.R` · 包：S3 · 实现：DefaultLayer.Assay
- 方法变体：`*Assay*`, `*StdAssay*`

### DefaultLayer<-
`DefaultLayer<-(object, ...)`

- 来源：`SO:assay.R` · 包：SeuratObject · 实现：DefaultLayer.Assay

### Degrees
`Degrees(rad)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：Degrees

### DietSeurat
`DietSeurat(object, layers=NULL, features=NULL, assays=NULL, dimreducs=NULL, graphs=NULL, misc=TRUE, counts=deprecated(), data=deprecated(), scale.data=deprecated(), ...)`

- 来源：`objects.R` · 包：Seurat · 实现：DietSeurat

### dim
`dim(x)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：dim.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*FOV*`, `*Neighbor*`, `*STARmap*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`, `*StdAssay*`, `*VisiumV1*`

### dimnames
`dimnames(x)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：dimnames.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*Seurat*`, `*StdAssay*`

### Distances
`Distances(object, ...)`

- 来源：`SO:neighbor.R` · 包：Seurat · 实现：Distances.Neighbor
- 方法变体：`*Neighbor*`

### droplevels
`droplevels(x, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：droplevels.Seurat
- 方法变体：`*LogMap*`, `*Seurat*`

### EmptyDF
`EmptyDF(n)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：EmptyDF

### EmptyMatrix
`EmptyMatrix(repr='C', type='d')`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：EmptyMatrix

### ExtractField
`ExtractField(string, field=1, delim="_")`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：ExtractField

### Features
`Features(x, assay=NULL, layer=c('data', 'scale.data', 'counts'), slot=deprecated(), simplify=TRUE, projected=NULL, set=NULL, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：Features.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*FOV*`, `*Molecules*`, `*SCTAssay*`, `*SCTModel*`, `*Seurat*`, `*StdAssay*`

### FetchData
`FetchData(object, vars, cells=NULL, layer=NULL, clean=TRUE, slot=deprecated(), simplify=TRUE, nmols=NULL, seed=NA_integer_, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：FetchData.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*FOV*`, `*Molecules*`, `*Seurat*`, `*StdAssay*`, `*VisiumV1*`

### FilterObjects
`FilterObjects(object, classes.keep=c('Assay', 'StdAssay', 'DimReduc'))`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：FilterObjects

### GetAssay
`GetAssay(object, assay=NULL, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：GetAssay.Seurat
- 方法变体：`*Seurat*`

### GetAssayData
`GetAssayData(object, assay=NULL, layer=NULL, slot=deprecated(), ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：GetAssayData.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### Graphs
`Graphs(object, slot=NULL)`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：Graphs

### head
`head(x, n=10L, ...)`

- 来源：`SO:assay.R` · 包：S3 · 实现：head.Assay
- 方法变体：`*Assay*`

### Index
`Index(object, ...)`

- 来源：`SO:neighbor.R` · 包：Seurat · 实现：Index.Neighbor
- 方法变体：`*Neighbor*`

### Index<-
`Index<-(object, ...)`

- 来源：`SO:neighbor.R` · 包：Seurat · 实现：Index.Neighbor

### Indices
`Indices(object, ...)`

- 来源：`SO:neighbor.R` · 包：Seurat · 实现：Indices.Neighbor
- 方法变体：`*Neighbor*`

### intersect
`intersect(x, y=missing_arg(), ...)`

- 来源：`SO:logmap.R` · 包：S3 · 实现：intersect.LogMap
- 方法变体：`*LogMap*`

### IsNamedList
`IsNamedList(x, all.unique=TRUE, allow.empty=FALSE, pass.zero=FALSE)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：IsNamedList

### IsS4List
`IsS4List(x)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：IsS4List

### IsSparse
`IsSparse(x)`

- 来源：`SO:sparse.R` · 包：SeuratObject · 实现：IsSparse

### JoinLayers
`JoinLayers(object, assay=NULL, layers=NULL, new=NULL, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：JoinLayers.Seurat
- 方法变体：`*Seurat*`, `*StdAssay*`

### JS
`JS(object, slot=NULL, ...)`

- 来源：`SO:dimreduc.R` · 包：Seurat · 实现：JS.DimReduc
- 方法变体：`*DimReduc*`, `*JackStrawData*`

### JS<-
`JS<-(object, slot=NULL, ...)`

- 来源：`SO:dimreduc.R` · 包：Seurat · 实现：JS.DimReduc

### Key
`Key(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Key.Seurat
- 方法变体：`*Assay*`, `*KeyMixin*`, `*Seurat*`, `*SpatialImage*`

### Key<-
`Key<-(object, ...)`

- 来源：`SO:assay.R` · 包：Seurat · 实现：Key.Assay

### Keys
`Keys(object, ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：Keys.FOV
- 方法变体：`*FOV*`

### labels
`labels(object, values, select=c('first', 'last', 'common', 'all'), simplify=TRUE, ...)`

- 来源：`SO:logmap.R` · 包：S3 · 实现：labels.LogMap
- 方法变体：`*LogMap*`

### LayerData
`LayerData(object, layer=NULL, assay=NULL, slot=deprecated(), cells=NULL, features=NULL, fast=FALSE, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：LayerData.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### LayerData<-
`LayerData<-(object, layer=NULL, cells=NULL, features=NULL, slot=deprecated(), ...)`

- 来源：`SO:assay.R` · 包：SeuratObject · 实现：LayerData.Assay

### Layers
`Layers(object, search=NA, assay=NULL, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：Layers.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### length
`length(x)`

- 来源：`SO:dimreduc.R` · 包：S3 · 实现：length.DimReduc
- 方法变体：`*Centroids*`, `*DimReduc*`, `*FOV*`

### lengths
`lengths(x, use.names=TRUE)`

- 来源：`SO:centroids.R` · 包：S3 · 实现：lengths.Centroids
- 方法变体：`*Centroids*`, `*Segmentation*`

### levels
`levels(x)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：levels.Seurat
- 方法变体：`*SCTAssay*`, `*Seurat*`

### ListToS4
`ListToS4(x)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：ListToS4

### LogMap
`LogMap(y)`

- 来源：`SO:logmap.R` · 包：SeuratObject · 实现：LogMap

### LogSeuratCommand
`LogSeuratCommand(object, return.command=FALSE)`

- 来源：`SO:command.R` · 包：Seurat · 实现：LogSeuratCommand

### MatchCells
`MatchCells(new, orig, ordered=FALSE)`

- 来源：`SO:default.R` · 包：S3 · 实现：MatchCells.NULL
- 方法变体：`*NULL*`, `*character*`, `*numeric*`

### merge
`merge(x=NULL, y=NULL, add.cell.ids=NULL, collapse=FALSE, merge.data=TRUE, merge.dr=FALSE, project=getOption(x = 'Seurat.object.project'..., labels=NULL, na.rm=TRUE, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：merge.Seurat
- 方法变体：`*Assay*`, `*DimReduc*`, `*SCTAssay*`, `*Seurat*`, `*StdAssay*`

### Misc
`Misc(object, ...)`

- 来源：`SO:generics.R` · 包：Seurat · 实现：Misc

### Misc<-
`Misc<-(?)`

- 来源：`—` · 包：Seurat · 实现：—

### Molecules
`Molecules(object, ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：Molecules.FOV
- 方法变体：`*FOV*`

### names
`names(x)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：names.Seurat
- 方法变体：`*DimReduc*`, `*FOV*`, `*Seurat*`

### Neighbors
`Neighbors(object, slot=NULL)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Neighbors

### PackageCheck
`PackageCheck(..., error=TRUE)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：PackageCheck

### PolyVtx
`PolyVtx(n, r=1L, xc=0L, yc=0L, t1=0)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：PolyVtx

### print
`print(x, dims=1:5, nfeatures=20, projected=FALSE, ...)`

- 来源：`SO:dimreduc.R` · 包：S3 · 实现：print.DimReduc
- 方法变体：`*DimReduc*`

### Project
`Project(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Project.Seurat
- 方法变体：`*Seurat*`

### Project<-
`Project<-(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Project.Seurat

### Radians
`Radians(deg)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：Radians

### Reductions
`Reductions(object, slot=NULL)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Reductions

### RegisterSparseMatrix
`RegisterSparseMatrix(class, package=NULL)`

- 来源：`SO:sparse.R` · 包：SeuratObject · 实现：RegisterSparseMatrix

### RenameAssays
`RenameAssays(object, assay.name=NULL, new.assay.name=NULL, verbose=TRUE, ...)`

- 来源：`SO:seurat.R` · 包：SeuratObject · 实现：RenameAssays

### RenameCells
`RenameCells(object, add.cell.id=missing_arg(), new.names=missing_arg(), for.merge=deprecated(), old.names=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：RenameCells.Seurat
- 方法变体：`*Assay*`, `*Centroids*`, `*DimReduc*`, `*FOV*`, `*Neighbor*`, `*SCTAssay*`, `*STARmap*`, `*Segmentation*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`, `*StdAssay*`

### S4ToList
`S4ToList(object)`

- 来源：`SO:utils.R` · 包：S3 · 实现：S4ToList.default
- 方法变体：`*default*`, `*list*`

### SetAssayData
`SetAssayData(object, layer='data', new.data, slot=deprecated(), assay=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：SetAssayData.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### Simplify
`Simplify(coords, tol, topologyPreserve=TRUE)`

- 来源：`SO:molecules.R` · 包：S3 · 实现：Simplify.Molecules
- 方法变体：`*Molecules*`, `*Spatial*`

### SparseEmptyMatrix
`SparseEmptyMatrix(nrow, ncol, rownames=NULL, colnames=NULL)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：SparseEmptyMatrix

### SpatiallyVariableFeatures
`SpatiallyVariableFeatures(object, method="moransi", assay=NULL, decreasing=TRUE, selection.method=deprecated(), ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：SpatiallyVariableFeatures.Seurat
- 方法变体：`*Assay*`, `*Seurat*`

### split
`split(x, f, drop=FALSE, assay=NULL, layers=NA, ret=c('assay', 'multiassays', 'layers'), ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：split.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### SplitObject
`SplitObject(object, split.by="ident")`

- 来源：`objects.R` · 包：Seurat · 实现：SplitObject

### Stdev
`Stdev(object, reduction='pca', ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Stdev.Seurat
- 方法变体：`*DimReduc*`, `*Seurat*`

### StitchMatrix
`StitchMatrix(x, y, rowmap, colmap, ...)`

- 来源：`SO:utils.R` · 包：S3 · 实现：StitchMatrix.default
- 方法变体：`*IterableMatrix*`, `*default*`, `*dgCMatrix*`, `*matrix*`

### subset
`subset(x, subset, cells=NULL, features=NULL, idents=NULL, return.null=FALSE, layers=NULL, score.threshold=NULL, disallowed.dataset.pairs=NULL, dataset.matrix=NULL, group.by=NULL, disallowed.ident.pairs=NULL, ident.matrix=NULL, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：subset.Seurat
- 方法变体：`*AnchorSet*`, `*Assay*`, `*Centroids*`, `*DimReduc*`, `*FOV*`, `*Molecules*`, `*SCTAssay*`, `*STARmap*`, `*Segmentation*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`

### SVFInfo
`SVFInfo(object, method=c("markvariogram", "moransi"), status=FALSE, assay=NULL, selection.method=deprecated(), ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：SVFInfo.Seurat
- 方法变体：`*Assay*`, `*Seurat*`

### tail
`tail(x, n=10L, ...)`

- 来源：`SO:assay.R` · 包：S3 · 实现：tail.Assay
- 方法变体：`*Assay*`

### Theta
`Theta(object)`

- 来源：`SO:centroids.R` · 包：S3 · 实现：Theta.Centroids
- 方法变体：`*Centroids*`

### Tool
`Tool(object, slot=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Tool.Seurat
- 方法变体：`*Seurat*`

### Tool<-
`Tool<-(object, slot=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Tool.Seurat

### TopCells
`TopCells(object, dim=1, ncells=20, balanced=FALSE, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：TopCells

### TopNeighbors
`TopNeighbors(object, cell, n=5)`

- 来源：`objects.R` · 包：Seurat · 实现：TopNeighbors

### UpdateSCTAssays
`UpdateSCTAssays(object)`

- 来源：`objects.R` · 包：Seurat · 实现：UpdateSCTAssays

### UpdateSeuratObject
`UpdateSeuratObject(object)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：UpdateSeuratObject

### UpdateSlots
`UpdateSlots(object)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：UpdateSlots

### upgrade
`upgrade(object, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：upgrade.seurat
- 方法变体：`*seurat*`

### Version
`Version(object, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：Version.Seurat
- 方法变体：`*Seurat*`


## MODULE: qc — 质量控制 / 去双细胞 / 细胞周期（9）

### BarcodeInflectionsPlot
`BarcodeInflectionsPlot(object)`

- 来源：`visualization.R` · 包：Seurat · 实现：BarcodeInflectionsPlot

### CalculateBarcodeInflections
`CalculateBarcodeInflections(object, barcode.column="nCount_RNA", group.column="orig.ident", threshold.low=NULL, threshold.high=NULL)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：CalculateBarcodeInflections

### GetResidual
`GetResidual(object, features, assay=NULL, umi.assay="RNA", clip.range=NULL, replace.value=FALSE, na.rm=TRUE, verbose=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：GetResidual

### HTODemux
`HTODemux(object, assay="HTO", positive.quantile=0.99, init=NULL, nstarts=100, kfunc="clara", nsamples=100, seed=42, verbose=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：HTODemux

### HTOHeatmap
`HTOHeatmap(object, assay='HTO', classification=paste0(assay, '_classification'), global.classification=paste0(assay, '_classification.global'), ncells=5000, singlet.names=NULL, raster=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：HTOHeatmap

### MULTIseqDemux
`MULTIseqDemux(object, assay="HTO", quantile=0.7, autoThresh=FALSE, maxiter=5, qrange=seq(from = 0.1, to = 0.9, by = 0.05), verbose=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：MULTIseqDemux

### PercentageFeatureSet
`PercentageFeatureSet(object, pattern=NULL, features=NULL, col.name=NULL, assay=NULL)`

- 来源：`utilities.R` · 包：Seurat · 实现：PercentageFeatureSet

### SampleUMI
`SampleUMI(data, max.umi=1000, upsample=FALSE, verbose=FALSE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：SampleUMI

### SubsetByBarcodeInflections
`SubsetByBarcodeInflections(object)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：SubsetByBarcodeInflections


## MODULE: norm — 归一化 / SCTransform / ScaleData（10）

### FetchResiduals
`FetchResiduals(object, features, assay=NULL, umi.assay="RNA", layer="counts", clip.range=NULL, reference.SCT.model=NULL, replace.value=FALSE, na.rm=TRUE, verbose=TRUE, umi.object, ...)`

- 来源：`preprocessing5.R` · 包：Seurat · 实现：FetchResiduals.Seurat
- 方法变体：`*SCTAssay*`, `*Seurat*`

### LogNormalize
`LogNormalize(data, scale.factor=1e4, margin=2L, verbose=TRUE, ...)`

- 来源：`generics.R` · 包：Seurat · 实现：LogNormalize

### NormalizeData
`NormalizeData(object, normalization.method=c('LogNormalize', 'CLR', 'RC'), scale.factor=1e4, cmargin=2L, margin=1L, verbose=TRUE, block.size=NULL, assay=NULL, layer='counts', save='data', ...)`

- 来源：`preprocessing5.R` · 包：Seurat · 实现：NormalizeData.default
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`, `*V3Matrix*`, `*default*`

### PrepSCTFindMarkers
`PrepSCTFindMarkers(object, assay="SCT", umi.assay="RNA", layer="counts", verbose=TRUE)`

- 来源：`differential_expression.R` · 包：Seurat · 实现：PrepSCTFindMarkers.V5
- 方法变体：`*V5*`

### PrepSCTIntegration
`PrepSCTIntegration(object.list, assay=NULL, anchor.features=2000, sct.clip.range=NULL, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：PrepSCTIntegration

### RelativeCounts
`RelativeCounts(data, scale.factor=1, verbose=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：RelativeCounts

### ScaleData
`ScaleData(object, features=NULL, vars.to.regress=NULL, latent.data=NULL, split.by=NULL, model.use='linear', use.umi=FALSE, do.scale=TRUE, do.center=TRUE, scale.max=10, block.size=1000, min.cells.to.block=3000, verbose=TRUE, assay=NULL, layer='data', by.layer=FALSE, save='scale.data', ...)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：ScaleData.default
- 方法变体：`*Assay*`, `*IterableMatrix*`, `*Seurat*`, `*StdAssay*`, `*default*`

### SCTransform
`SCTransform(object, cell.attr=NULL, reference.SCT.model=NULL, do.correct.umi=TRUE, ncells=5000, residual.features=NULL, variable.features.n=3000, variable.features.rv.th=1.3, vars.to.regress=NULL, latent.data=NULL, do.scale=FALSE, do.center=TRUE, clip.range=c(-sqrt(x = ncol(x = umi) / 30), sqrt..., vst.flavor='v2', conserve.memory=FALSE, return.only.var.genes=TRUE, seed.use=1448145, verbose=TRUE, assay="RNA", new.assay.name='SCT', layer='counts', ...)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：SCTransform.default
- 方法变体：`*Assay*`, `*IterableMatrix*`, `*Seurat*`, `*StdAssay*`, `*default*`

### SCTResults
`SCTResults(object, assay="SCT", slot, model=NULL, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：SCTResults.Seurat
- 方法变体：`*SCTAssay*`, `*SCTModel*`, `*Seurat*`

### SelectSCTIntegrationFeatures
`SelectSCTIntegrationFeatures(object, nfeatures=3000, assay=NULL, verbose=TRUE, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：SelectSCTIntegrationFeatures


## MODULE: hvg — 高变基因 / 空间可变基因（6）

### FindVariableFeatures
`FindVariableFeatures(object, method=VST, nfeatures=2000L, verbose=TRUE, selection.method=selection.method, loess.span=0.3, clip.max='auto', mean.function=FastExpMean, dispersion.function=FastLogVMR, num.bin=20, binning.method="equal_width", mean.cutoff=c(0.1, 8), dispersion.cutoff=c(1, Inf), assay=NULL, layer=NULL, span=0.3, clip=NULL, key=NULL, ...)`

- 来源：`preprocessing5.R` · 包：Seurat · 实现：FindVariableFeatures.default
- 方法变体：`*Assay*`, `*SCTAssay*`, `*Seurat*`, `*StdAssay*`, `*V3Matrix*`, `*default*`

### HVFInfo
`HVFInfo(object, method=NULL, status=FALSE, assay=NULL, selection.method=deprecated(), layer=NULL, strip=TRUE, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：HVFInfo.Seurat
- 方法变体：`*Assay*`, `*SCTAssay*`, `*Seurat*`, `*StdAssay*`

### TopFeatures
`TopFeatures(object, dim=1, nfeatures=20, projected=FALSE, balanced=FALSE, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：TopFeatures

### VariableFeatures
`VariableFeatures(object, method=NULL, assay=NULL, nfeatures=NULL, layer=NA, simplify=TRUE, selection.method=deprecated(), use.var.features=TRUE, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：VariableFeatures.Seurat
- 方法变体：`*Assay*`, `*SCTAssay*`, `*SCTModel*`, `*Seurat*`, `*StdAssay*`

### VariableFeatures<-
`VariableFeatures<-(object, method=NULL, selection.method=deprecated(), ...)`

- 来源：`SO:assay.R` · 包：Seurat · 实现：VariableFeatures.Assay

### VST
`VST(data, margin=1L, nselect=2000L, span=0.3, clip=NULL, verbose=TRUE, ...)`

- 来源：`preprocessing5.R` · 包：Seurat · 实现：VST.default
- 方法变体：`*IterableMatrix*`, `*default*`, `*dgCMatrix*`, `*matrix*`


## MODULE: dr — 降维 PCA / UMAP / tSNE / SLSI（23）

### DimHeatmap
`DimHeatmap(object, dims=1, nfeatures=30, cells=NULL, reduction='pca', disp.min=-2.5, disp.max=NULL, balanced=TRUE, projected=FALSE, ncol=NULL, fast=TRUE, raster=TRUE, slot='scale.data', assays=NULL, combine=TRUE, legend.position="right")`

- 来源：`visualization.R` · 包：Seurat · 实现：DimHeatmap

### ElbowPlot
`ElbowPlot(object, ndims=20, reduction='pca', plot_type=c("stdev", "variance", "cumulative_va...)`

- 来源：`visualization.R` · 包：Seurat · 实现：ElbowPlot

### Embeddings
`Embeddings(object, reduction='pca', ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Embeddings.Seurat
- 方法变体：`*DimReduc*`, `*Seurat*`

### JackStraw
`JackStraw(object, reduction="pca", assay=NULL, dims=20, num.replicate=100, prop.freq=0.01, verbose=TRUE, maxit=1000)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：JackStraw

### JackStrawPlot
`JackStrawPlot(object, dims=1:5, cols=NULL, reduction='pca', xmax=0.1, ymax=0.3)`

- 来源：`visualization.R` · 包：Seurat · 实现：JackStrawPlot

### L2CCA
`L2CCA(object, ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：L2CCA

### L2Dim
`L2Dim(object, reduction, new.dr=NULL, new.key=NULL)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：L2Dim

### Loadings
`Loadings(object, reduction='pca', projected=FALSE, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Loadings.Seurat
- 方法变体：`*DimReduc*`, `*Seurat*`

### Loadings<-
`Loadings<-(object, reduction='pca', projected=FALSE, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Loadings.Seurat

### PCAPlot
`PCAPlot(object, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：PCAPlot

### PCASigGenes
`PCASigGenes(object, pcs.use, pval.cut=0.1, use.full=FALSE, max.per.pc=NULL)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：PCASigGenes

### PCHeatmap
`PCHeatmap(object, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：PCHeatmap

### ProjectDim
`ProjectDim(object, reduction="pca", assay=NULL, dims.print=1:5, nfeatures.print=20, overwrite=FALSE, do.center=FALSE, verbose=TRUE)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：ProjectDim

### ProjectUMAP
`ProjectUMAP(query, query.dims=NULL, reference, reference.dims=NULL, k.param=30, nn.method="annoy", n.trees=50, annoy.metric="cosine", l2.norm=FALSE, cache.index=TRUE, index=NULL, neighbor.name="query_ref.nn", reduction.model, query.reduction, reference.reduction, reduction.name="ref.umap", reduction.key="refUMAP_", ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：ProjectUMAP.default
- 方法变体：`*DimReduc*`, `*Seurat*`, `*default*`

### RunCCA
`RunCCA(object1, object2, standardize=TRUE, num.cc=20, seed.use=42, verbose=FALSE, assay1=NULL, assay2=NULL, features=NULL, renormalize=FALSE, rescale=FALSE, compute.gene.loadings=TRUE, add.cell.id1=NULL, add.cell.id2=NULL, ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunCCA.default
- 方法变体：`*Seurat*`, `*default*`

### RunICA
`RunICA(object, assay=NULL, nics=50, rev.ica=FALSE, ica.function="icafast", verbose=TRUE, ndims.print=1:5, nfeatures.print=30, reduction.name="ica", reduction.key="ica_", seed.use=42, features=NULL, layer='scale.data', ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunICA.default
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`, `*default*`

### RunPCA
`RunPCA(object, assay=NULL, npcs=50, rev.pca=FALSE, weight.by.var=TRUE, verbose=TRUE, ndims.print=1:5, nfeatures.print=30, reduction.key="PC_", seed.use=42, approx=TRUE, features=NULL, layer='scale.data', reduction.name="pca", ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunPCA.default
- 方法变体：`*Assay*`, `*Seurat*`, `*Seurat5*`, `*StdAssay*`, `*default*`

### RunSLSI
`RunSLSI(object, assay=NULL, n=50, reduction.key="SLSI_", graph=NULL, verbose=TRUE, seed.use=42, features=NULL, layer="data", reduction.name="slsi", ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunSLSI.default
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`, `*default*`

### RunSPCA
`RunSPCA(object, assay=NULL, npcs=50, reduction.key="SPC_", graph=NULL, verbose=FALSE, seed.use=42, features=NULL, layer='scale.data', reduction.name="spca", ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunSPCA.default
- 方法变体：`*Assay*`, `*Assay5*`, `*Seurat*`, `*default*`

### RunTSNE
`RunTSNE(object, reduction="pca", cells=NULL, dims=1:5, features=NULL, seed.use=1, tsne.method="Rtsne", dim.embed=2, distance.matrix=NULL, reduction.name="tsne", reduction.key="tSNE_", assay=NULL, ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunTSNE.Seurat
- 方法变体：`*DimReduc*`, `*Seurat*`, `*dist*`, `*matrix*`

### RunUMAP
`RunUMAP(object, reduction.key='UMAP_', assay=NULL, reduction.model=NULL, return.model=FALSE, umap.method='uwot', n.neighbors=30L, n.components=2L, metric='cosine', n.epochs=NULL, learning.rate=1.0, min.dist=0.3, spread=1.0, set.op.mix.ratio=1.0, local.connectivity=1L, repulsion.strength=1, negative.sample.rate=5, a=NULL, b=NULL, uwot.sgd=FALSE, uwot.approx_pow=FALSE, uwot.init="spectral", seed.use=42, metric.kwds=NULL, angular.rp.forest=FALSE, densmap=FALSE, dens.lambda=2, dens.frac=0.3, dens.var.shift=0.1, verbose=TRUE, densmap.kwds=NULL, dims=NULL, reduction='pca', features=NULL, graph=NULL, nn.name=NULL, slot='data', reduction.name='umap', ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：RunUMAP.default
- 方法变体：`*Graph*`, `*Neighbor*`, `*Seurat*`, `*default*`

### ScoreJackStraw
`ScoreJackStraw(object, reduction="pca", dims=1:5, score.thresh=1e-5, do.plot=FALSE, ...)`

- 来源：`dimensional_reduction.R` · 包：Seurat · 实现：ScoreJackStraw.Seurat
- 方法变体：`*DimReduc*`, `*JackStrawData*`, `*Seurat*`

### VizDimLoadings
`VizDimLoadings(object, dims=1:5, nfeatures=30, col='blue', reduction='pca', projected=FALSE, balanced=FALSE, ncol=NULL, combine=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：VizDimLoadings


## MODULE: cluster — 聚类 / 分群注释 / 聚类树（16）

### CellsByIdentities
`CellsByIdentities(object, idents=NULL, cells=NULL, return.null=FALSE)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：CellsByIdentities

### FindClusters
`FindClusters(object, modularity.fxn=1, initial.membership=NULL, node.sizes=NULL, resolution=0.8, method=deprecated(), algorithm=1, leiden_method=c("leidenbase", "igraph"), leiden_objective_function=c("modularity", "CPM"), n.start=10, n.iter=10, random.seed=0, group.singletons=TRUE, temp.file.location=NULL, edge.file.name=NULL, verbose=TRUE, graph.name=NULL, cluster.name=NULL, ...)`

- 来源：`clustering.R` · 包：Seurat · 实现：FindClusters.default
- 方法变体：`*Seurat*`, `*default*`

### FindNeighbors
`FindNeighbors(object, query=NULL, distance.matrix=FALSE, k.param=20, return.neighbor=FALSE, compute.SNN=!return.neighbor, prune.SNN=1/15, nn.method="annoy", n.trees=50, annoy.metric="euclidean", nn.eps=0, verbose=TRUE, l2.norm=FALSE, cache.index=FALSE, index=NULL, features=NULL, reduction="pca", dims=1:10, assay=NULL, do.plot=FALSE, graph.name=NULL, ...)`

- 来源：`clustering.R` · 包：Seurat · 实现：FindNeighbors.default
- 方法变体：`*Assay*`, `*Seurat*`, `*default*`, `*dist*`

### FindSubCluster
`FindSubCluster(object, cluster, graph.name, subcluster.name="sub.cluster", resolution=0.5, algorithm=1)`

- 来源：`clustering.R` · 包：Seurat · 实现：FindSubCluster

### Idents
`Idents(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Idents.Seurat
- 方法变体：`*Seurat*`

### Idents<-
`Idents<-(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Idents.Seurat

### NNPlot
`NNPlot(object, reduction, nn.idx, query.cells, dims=1:2, label=FALSE, label.size=4, repel=FALSE, sizes.highlight=2, pt.size=1, cols.highlight=c("#377eb8", "#e41a1c"), na.value="#bdbdbd", order=c("self", "neighbors", "other"), show.all.cells=TRUE, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：NNPlot

### PlotClusterTree
`PlotClusterTree(object, direction="downwards", ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：PlotClusterTree

### RegroupIdents
`RegroupIdents(object, metadata)`

- 来源：`utilities.R` · 包：Seurat · 实现：RegroupIdents

### RenameIdents
`RenameIdents(object, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：RenameIdents.Seurat
- 方法变体：`*Seurat*`

### ReorderIdent
`ReorderIdent(object, var, reverse=FALSE, afxn=mean, reorder.numeric=FALSE, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：ReorderIdent.Seurat
- 方法变体：`*Seurat*`

### RunLeiden
`RunLeiden(object, method=deprecated(), leiden_method=c("leidenbase", "igraph"), partition.type=c( 'RBConfigurationVertexPartition', ..., leiden_objective_function=c("modularity", "CPM"), initial.membership=NULL, node.sizes=NULL, resolution.parameter=1, random.seed=1, n.iter=10)`

- 来源：`clustering.R` · 包：Seurat · 实现：RunLeiden

### SetIdent
`SetIdent(object, cells=NULL, value, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：SetIdent.Seurat
- 方法变体：`*Seurat*`

### SetQuantile
`SetQuantile(cutoff, data)`

- 来源：`utilities.R` · 包：Seurat · 实现：SetQuantile

### StashIdent
`StashIdent(object, save.name='orig.ident', ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：StashIdent.Seurat
- 方法变体：`*Seurat*`

### WhichCells
`WhichCells(object, cells=NULL, idents=NULL, expression, slot='data', invert=FALSE, downsample=Inf, seed=1, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：WhichCells.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`


## MODULE: de — 差异表达 / 拟 bulk 聚合（8）

### AggregateExpression
`AggregateExpression(object, assays=NULL, features=NULL, return.seurat=FALSE, group.by='ident', add.ident=NULL, normalization.method="LogNormalize", scale.factor=10000, margin=1, verbose=TRUE, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：AggregateExpression

### AverageExpression
`AverageExpression(object, assays=NULL, features=NULL, return.seurat=FALSE, group.by='ident', add.ident=NULL, layer='data', slot=deprecated(), verbose=TRUE, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：AverageExpression

### CreateCategoryMatrix
`CreateCategoryMatrix(labels, method=c('aggregate', 'average'), cells.name=NULL)`

- 来源：`utilities.R` · 包：Seurat · 实现：CreateCategoryMatrix

### FindAllMarkers
`FindAllMarkers(object, assay=NULL, features=NULL, group.by=NULL, logfc.threshold=0.1, test.use='wilcox', slot='data', min.pct=0.01, min.diff.pct=-Inf, node=NULL, verbose=TRUE, only.pos=FALSE, max.cells.per.ident=Inf, random.seed=1, latent.vars=NULL, min.cells.feature=3, min.cells.group=3, mean.fxn=NULL, fc.name=NULL, base=2, return.thresh=1e-2, densify=FALSE, ...)`

- 来源：`differential_expression.R` · 包：Seurat · 实现：FindAllMarkers

### FindConservedMarkers
`FindConservedMarkers(object, ident.1, ident.2=NULL, grouping.var, assay='RNA', slot='data', min.cells.group=3, meta.method=metap::minimump, verbose=TRUE, ...)`

- 来源：`differential_expression.R` · 包：Seurat · 实现：FindConservedMarkers

### FindMarkers
`FindMarkers(object, slot="data", cells.1=NULL, cells.2=NULL, features=NULL, logfc.threshold=0.1, test.use="wilcox", min.pct=0.01, min.diff.pct=-Inf, verbose=TRUE, only.pos=FALSE, max.cells.per.ident=Inf, random.seed=1, latent.vars=NULL, min.cells.feature=3, min.cells.group=3, fc.results=NULL, densify=FALSE, fc.slot="data", pseudocount.use=1, norm.method=NULL, mean.fxn=NULL, fc.name=NULL, base=2, recorrect_umi=TRUE, ident.1=NULL, ident.2=NULL, group.by=NULL, subset.ident=NULL, assay=NULL, reduction=NULL, ...)`

- 来源：`differential_expression.R` · 包：Seurat · 实现：FindMarkers.default
- 方法变体：`*Assay*`, `*DimReduc*`, `*SCTAssay*`, `*Seurat*`, `*default*`

### FoldChange
`FoldChange(object, cells.1, cells.2, mean.fxn=NULL, fc.name=NULL, features=NULL, slot="data", pseudocount.use=1, base=2, norm.method=NULL, ident.1=NULL, ident.2=NULL, group.by=NULL, subset.ident=NULL, assay=NULL, reduction=NULL, ...)`

- 来源：`differential_expression.R` · 包：Seurat · 实现：FoldChange.default
- 方法变体：`*Assay*`, `*DimReduc*`, `*SCTAssay*`, `*Seurat*`, `*default*`

### PseudobulkExpression
`PseudobulkExpression(object, assays=NULL, features=NULL, return.seurat=FALSE, group.by='ident', add.ident=NULL, layer='data', slot=deprecated(), method='average', normalization.method="LogNormalize", scale.factor=10000, margin=1, verbose=TRUE, assay, category.matrix, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：PseudobulkExpression.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`


## MODULE: integrate — 多样本整合 / 参考映射 / Bridge（32）

### AddAzimuthResults
`AddAzimuthResults(object=NULL, filename)`

- 来源：`utilities.R` · 包：Seurat · 实现：AddAzimuthResults

### AnnotateAnchors
`AnnotateAnchors(anchors, vars=NULL, slot=NULL, object.list=NULL, assay=NULL, reference=NULL, query=NULL, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：AnnotateAnchors.default
- 方法变体：`*IntegrationAnchorSet*`, `*TransferAnchorSet*`, `*default*`

### BridgeCellsRepresentation
`BridgeCellsRepresentation(object.list, bridge.object, object.reduction, bridge.reduction, laplacian.reduction='lap', laplacian.dims=1:50, bridge.assay.name="Bridge", return.all.assays=FALSE, l2.norm=TRUE, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：BridgeCellsRepresentation

### CCAIntegration
`CCAIntegration(object=NULL, assay=NULL, layers=NULL, orig=NULL, new.reduction='integrated.dr', reference=NULL, features=NULL, normalization.method=c("LogNormalize", "SCT"), dims=1:30, k.filter=NA, scale.layer='scale.data', dims.to.integrate=NULL, k.weight=100, weight.reduction=NULL, sd.weight=1, sample.tree=NULL, preserve.order=FALSE, verbose=TRUE, ...)`

- 来源：`integration5.R` · 包：Seurat · 实现：CCAIntegration

### FastRPCAIntegration
`FastRPCAIntegration(object.list, reference=NULL, anchor.features=2000, k.anchor=20, dims=1:30, scale=TRUE, normalization.method=c("LogNormalize", "SCT"), new.reduction.name='integrated_dr', npcs=50, findintegrationanchors.args=list(), verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：FastRPCAIntegration

### FindBridgeIntegrationAnchors
`FindBridgeIntegrationAnchors(extended.reference, query, query.assay=NULL, dims=1:30, scale=FALSE, reduction=c('lsiproject', 'pcaproject'), integration.reduction=c('direct', 'cca'), verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：FindBridgeIntegrationAnchors

### FindBridgeTransferAnchors
`FindBridgeTransferAnchors(extended.reference, query, query.assay=NULL, dims=1:30, scale=FALSE, reduction=c('lsiproject', 'pcaproject'), bridge.reduction=c('direct', 'cca'), verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：FindBridgeTransferAnchors

### FindIntegrationAnchors
`FindIntegrationAnchors(object.list=NULL, assay=NULL, reference=NULL, anchor.features=2000, scale=TRUE, normalization.method=c("LogNormalize", "SCT"), sct.clip.range=NULL, reduction=c("cca", "rpca", "jpca", "rlsi"), l2.norm=TRUE, dims=1:30, k.anchor=5, k.filter=200, k.score=30, max.features=200, nn.method="annoy", n.trees=50, eps=0, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：FindIntegrationAnchors

### FindTransferAnchors
`FindTransferAnchors(reference, query, normalization.method="LogNormalize", recompute.residuals=TRUE, reference.assay=NULL, reference.neighbors=NULL, query.assay=NULL, reduction="pcaproject", reference.reduction=NULL, project.query=FALSE, features=NULL, scale=TRUE, npcs=30, l2.norm=TRUE, dims=1:30, k.anchor=5, k.filter=NA, k.score=30, max.features=200, nn.method="annoy", n.trees=50, eps=0, approx.pca=TRUE, mapping.score.k=NULL, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：FindTransferAnchors

### GetIntegrationData
`GetIntegrationData(object, integration.name, slot)`

- 来源：`objects.R` · 包：Seurat · 实现：GetIntegrationData

### GetTransferPredictions
`GetTransferPredictions(object, assay="predictions", slot="data", score.filter=0.75)`

- 来源：`integration.R` · 包：Seurat · 实现：GetTransferPredictions

### HarmonyIntegration
`HarmonyIntegration(object, orig, features=NULL, scale.layer='scale.data', new.reduction='harmony', layers=NULL, npcs=NULL, key='harmony_', theta=NULL, lambda=NULL, sigma=0.1, nclust=NULL, tau=0, block.size=0.05, max.iter.harmony=10L, max.iter.cluster=20L, epsilon.cluster=1e-05, epsilon.harmony=0.01, verbose=TRUE, ...)`

- 来源：`integration5.R` · 包：Seurat · 实现：HarmonyIntegration

### IntegrateData
`IntegrateData(anchorset, new.assay.name="integrated", normalization.method=c("LogNormalize", "SCT"), features=NULL, features.to.integrate=NULL, dims=1:30, k.weight=100, weight.reduction=NULL, sd.weight=1, sample.tree=NULL, preserve.order=FALSE, eps=0, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：IntegrateData

### IntegrateEmbeddings
`IntegrateEmbeddings(anchorset, new.reduction.name="integrated_dr", reductions=NULL, dims.to.integrate=NULL, k.weight=100, weight.reduction=NULL, sd.weight=1, sample.tree=NULL, preserve.order=FALSE, verbose=TRUE, reference, query, query.assay=NULL, reuse.weights.matrix=TRUE, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：IntegrateEmbeddings.IntegrationAnchorSet
- 方法变体：`*IntegrationAnchorSet*`, `*TransferAnchorSet*`

### IntegrateLayers
`IntegrateLayers(object, method, orig.reduction='pca', assay=NULL, features=NULL, layers=NULL, scale.layer='scale.data', ...)`

- 来源：`integration5.R` · 包：Seurat · 实现：IntegrateLayers

### JointPCAIntegration
`JointPCAIntegration(object=NULL, assay=NULL, layers=NULL, orig=NULL, new.reduction='integrated.dr', reference=NULL, features=NULL, normalization.method=c("LogNormalize", "SCT"), dims=1:30, k.anchor=20, scale.layer='scale.data', dims.to.integrate=NULL, k.weight=100, weight.reduction=NULL, sd.weight=1, sample.tree=NULL, preserve.order=FALSE, verbose=TRUE, ...)`

- 来源：`integration5.R` · 包：Seurat · 实现：JointPCAIntegration

### LocalStruct
`LocalStruct(object, grouping.var, idents=NULL, neighbors=100, reduction="pca", reduced.dims=1:10, orig.dims=1:10, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：LocalStruct

### MappingScore
`MappingScore(anchors, combined.object, query.neighbors, ref.embeddings, query.embeddings, kanchors=50, ndim=50, ksmooth=100, ksnn=20, snn.prune=0, subtract.first.nn=TRUE, nn.method="annoy", n.trees=50, query.weights=NULL, verbose=TRUE, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：MappingScore.default
- 方法变体：`*AnchorSet*`, `*default*`

### MapQuery
`MapQuery(anchorset, query, reference, refdata=NULL, new.reduction.name=NULL, reference.reduction=NULL, reference.dims=NULL, query.dims=NULL, store.weights=FALSE, reduction.model=NULL, transferdata.args=list(), integrateembeddings.args=list(), projectumap.args=list(), verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：MapQuery

### MixingMetric
`MixingMetric(object, grouping.var, reduction="pca", dims=1:2, k=5, max.k=300, eps=0, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：MixingMetric

### NNtoGraph
`NNtoGraph(nn.object, col.cells=NULL, weighted=FALSE)`

- 来源：`integration.R` · 包：Seurat · 实现：NNtoGraph

### PredictAssay
`PredictAssay(object, nn.idx, assay, reduction=NULL, dims=NULL, return.assay=TRUE, slot="scale.data", features=NULL, mean.function=rowMeans, seed=4273, verbose=TRUE)`

- 来源：`clustering.R` · 包：Seurat · 实现：PredictAssay

### PrepareBridgeReference
`PrepareBridgeReference(reference, bridge, reference.reduction='pca', reference.dims=1:50, normalization.method=c('SCT', 'LogNormalize'), reference.assay=NULL, bridge.ref.assay='RNA', bridge.query.assay='ATAC', supervised.reduction=c('slsi', 'spca', NULL), bridge.query.reduction=NULL, bridge.query.features=NULL, laplacian.reduction.name='lap', laplacian.reduction.key='lap_', laplacian.reduction.dims=1:50, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：PrepareBridgeReference

### ProjectCellEmbeddings
`ProjectCellEmbeddings(query, reference, reference.assay=NULL, reduction="pca", dims=1:50, scale=TRUE, normalization.method=NULL, verbose=TRUE, features=NULL, nCount_UMI=NULL, feature.mean=NULL, feature.sd=NULL, query.assay=NULL, block.size=10000, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：ProjectCellEmbeddings.default
- 方法变体：`*Assay*`, `*IterableMatrix*`, `*SCTAssay*`, `*Seurat*`, `*StdAssay*`, `*default*`

### ProjectDimReduc
`ProjectDimReduc(query, reference, mode=c('pcaproject', 'lsiproject'), reference.reduction, combine=FALSE, query.assay=NULL, reference.assay=NULL, features=NULL, do.scale=TRUE, reduction.name=NULL, reduction.key=NULL, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：ProjectDimReduc

### ProjectIntegration
`ProjectIntegration(object, sketched.assay='sketch', assay='RNA', reduction='integrated_dr', features=NULL, layers='data', reduction.name=NULL, reduction.key=NULL, method=c('sketch', 'data'), ratio=0.8, sketched.layers=NULL, seed=123, verbose=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：ProjectIntegration

### RPCAIntegration
`RPCAIntegration(object=NULL, assay=NULL, layers=NULL, orig=NULL, new.reduction='integrated.dr', reference=NULL, features=NULL, normalization.method=c("LogNormalize", "SCT"), dims=1:30, k.filter=NA, scale.layer='scale.data', dims.to.integrate=NULL, k.weight=100, weight.reduction=NULL, sd.weight=1, sample.tree=NULL, preserve.order=FALSE, verbose=TRUE, ...)`

- 来源：`integration5.R` · 包：Seurat · 实现：RPCAIntegration

### RunGraphLaplacian
`RunGraphLaplacian(object, n=50, reduction.key="LAP_", verbose=TRUE, graph, reduction.name="lap", ...)`

- 来源：`integration.R` · 包：Seurat · 实现：RunGraphLaplacian.default
- 方法变体：`*Seurat*`, `*default*`

### SelectIntegrationFeatures
`SelectIntegrationFeatures(object.list, nfeatures=2000, assay=NULL, verbose=TRUE, fvf.nfeatures=2000, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：SelectIntegrationFeatures

### SelectIntegrationFeatures5
`SelectIntegrationFeatures5(object, nfeatures=2000, assay=NULL, method=NULL, layers=NULL, verbose=TRUE, ...)`

- 来源：`integration.R` · 包：Seurat · 实现：SelectIntegrationFeatures5

### SetIntegrationData
`SetIntegrationData(object, integration.name, slot, new.data)`

- 来源：`objects.R` · 包：Seurat · 实现：SetIntegrationData

### TransferData
`TransferData(anchorset, refdata, reference=NULL, query=NULL, query.assay=NULL, weight.reduction='pcaproject', l2.norm=FALSE, dims=NULL, k.weight=50, sd.weight=1, eps=0, n.trees=50, verbose=TRUE, slot="data", prediction.assay=FALSE, only.weights=FALSE, store.weights=TRUE)`

- 来源：`integration.R` · 包：Seurat · 实现：TransferData


## MODULE: sketch — Sketch 大数据草图（7）

### CountSketch
`CountSketch(nsketch, ncells, seed=NA_integer_, ...)`

- 来源：`sketching.R` · 包：Seurat · 实现：CountSketch

### GaussianSketch
`GaussianSketch(nsketch, ncells, seed=NA_integer_, ...)`

- 来源：`sketching.R` · 包：Seurat · 实现：GaussianSketch

### LeverageScore
`LeverageScore(object, nsketch=5000L, ndims=NULL, method=CountSketch, eps=0.5, seed=123L, verbose=TRUE, vf.method=NULL, layer='data', features=NULL, assay=NULL, var.name='leverage.score', over.write=FALSE, ...)`

- 来源：`sketching.R` · 包：Seurat · 实现：LeverageScore.default
- 方法变体：`*Seurat*`, `*StdAssay*`, `*default*`

### ProjectData
`ProjectData(object, assay='RNA', sketched.assay='sketch', sketched.reduction, full.reduction, dims, normalization.method=c("LogNormalize", "SCT"), refdata=NULL, k.weight=50, umap.model=NULL, recompute.neighbors=FALSE, recompute.weights=FALSE, verbose=TRUE)`

- 来源：`sketching.R` · 包：Seurat · 实现：ProjectData

### SketchData
`SketchData(object, assay=NULL, ncells=5000L, sketched.assay='sketch', method=c('LeverageScore', 'Uniform'), var.name="leverage.score", over.write=FALSE, seed=123L, cast='dgCMatrix', verbose=TRUE, features=NULL, ...)`

- 来源：`sketching.R` · 包：Seurat · 实现：SketchData

### TransferSketchLabels
`TransferSketchLabels(object, sketched.assay='sketch', reduction, dims, refdata=NULL, k=50, reduction.model=NULL, neighbors=NULL, recompute.neighbors=FALSE, recompute.weights=FALSE, verbose=TRUE)`

- 来源：`sketching.R` · 包：Seurat · 实现：TransferSketchLabels

### UnSketchEmbeddings
`UnSketchEmbeddings(atom.data, atom.cells=NULL, orig.data, embeddings, sketch.matrix=NULL)`

- 来源：`integration.R` · 包：Seurat · 实现：UnSketchEmbeddings


## MODULE: viz — 可视化（64）

### AugmentPlot
`AugmentPlot(plot, width=10, height=10, dpi=100)`

- 来源：`visualization.R` · 包：Seurat · 实现：AugmentPlot

### AutoPointSize
`AutoPointSize(data, raster=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：AutoPointSize

### BGTextColor
`BGTextColor(background, threshold=186, w3c=FALSE, dark='black', light='white')`

- 来源：`visualization.R` · 包：Seurat · 实现：BGTextColor

### BlackAndWhite
`BlackAndWhite(mid=NULL, k=50)`

- 来源：`visualization.R` · 包：Seurat · 实现：BlackAndWhite

### BlueAndRed
`BlueAndRed(k=50)`

- 来源：`visualization.R` · 包：Seurat · 实现：BlueAndRed

### BoldTitle
`BoldTitle(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：BoldTitle

### CellScatter
`CellScatter(object, cell1, cell2, features=NULL, highlight=NULL, cols=NULL, pt.size=1, smooth=FALSE, raster=NULL, raster.dpi=c(512, 512))`

- 来源：`visualization.R` · 包：Seurat · 实现：CellScatter

### CellSelector
`CellSelector(plot, object=NULL, ident='SelectedCells', ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：CellSelector

### CenterTitle
`CenterTitle(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：CenterTitle

### CollapseEmbeddingOutliers
`CollapseEmbeddingOutliers(object, reduction='umap', dims=1:2, group.by='ident', outlier.sd=2, reduction.key='UMAP_')`

- 来源：`visualization.R` · 包：Seurat · 实现：CollapseEmbeddingOutliers

### ColorDimSplit
`ColorDimSplit(object, node, left.color='red', right.color='blue', other.color='grey50', ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：ColorDimSplit

### CombinePlots
`CombinePlots(plots, ncol=NULL, legend=NULL, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：CombinePlots

### CustomPalette
`CustomPalette(low="white", high="red", mid=NULL, k=50)`

- 来源：`visualization.R` · 包：Seurat · 实现：CustomPalette

### DarkTheme
`DarkTheme(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：DarkTheme

### DimPlot
`DimPlot(object, dims=c(1, 2), cells=NULL, cols=NULL, pt.size=NULL, reduction=NULL, group.by=NULL, split.by=NULL, shape.by=NULL, order=NULL, shuffle=FALSE, seed=1, label=FALSE, label.size=4, label.color='black', label.box=FALSE, repel=FALSE, alpha=1, stroke.size=NULL, cells.highlight=NULL, cols.highlight='#DE2D26', sizes.highlight=1, na.value='grey50', ncol=NULL, combine=TRUE, raster=NULL, raster.dpi=c(512, 512), label.size.cutoff=0)`

- 来源：`visualization.R` · 包：Seurat · 实现：DimPlot

### DiscretePalette
`DiscretePalette(n, palette=NULL, shuffle=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：DiscretePalette

### DoHeatmap
`DoHeatmap(object, features=NULL, cells=NULL, group.by='ident', group.bar=TRUE, group.colors=NULL, disp.min=-2.5, disp.max=NULL, slot='scale.data', assay=NULL, label=TRUE, size=5.5, hjust=0, vjust=0, angle=45, raster=TRUE, draw.lines=TRUE, lines.width=NULL, group.bar.height=0.02, combine=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：DoHeatmap

### DotPlot
`DotPlot(object, features, assay=NULL, cols=c("lightgrey", "blue"), col.min=-2.5, col.max=2.5, dot.min=0, dot.scale=6, idents=NULL, group.by=NULL, split.by=NULL, cluster.idents=FALSE, scale=TRUE, scale.by='radius', scale.min=NA, scale.max=NA)`

- 来源：`visualization.R` · 包：Seurat · 实现：DotPlot

### FeatureLocator
`FeatureLocator(plot, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：FeatureLocator

### FeaturePlot
`FeaturePlot(object, features, dims=c(1, 2), cells=NULL, cols=if (blend) { c('lightgrey', '#ff0000'..., pt.size=NULL, alpha=1, stroke.size=NULL, order=FALSE, min.cutoff=NA, max.cutoff=NA, reduction=NULL, split.by=NULL, keep.scale="feature", shape.by=NULL, slot='data', assay=NULL, blend=FALSE, blend.threshold=0.5, label=FALSE, label.size=4, label.color="black", repel=FALSE, ncol=NULL, coord.fixed=FALSE, by.col=TRUE, sort.cell=deprecated(), interactive=FALSE, combine=TRUE, raster=NULL, raster.dpi=c(512, 512))`

- 来源：`visualization.R` · 包：Seurat · 实现：FeaturePlot

### FeatureScatter
`FeatureScatter(object, feature1, feature2, cells=NULL, shuffle=FALSE, seed=1, group.by=NULL, split.by=NULL, cols=NULL, pt.size=1, shape.by=NULL, span=NULL, smooth=FALSE, combine=TRUE, slot='data', plot.cor=TRUE, ncol=NULL, raster=NULL, raster.dpi=c(512, 512), jitter=FALSE, log=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：FeatureScatter

### FontSize
`FontSize(x.text=NULL, y.text=NULL, x.title=NULL, y.title=NULL, main=NULL, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：FontSize

### fortify
`fortify(model, data, nmols=NULL, seed=NA_integer_, ...)`

- 来源：`visualization.R` · 包：S3 · 实现：fortify.Centroids
- 方法变体：`*Centroids*`, `*Molecules*`, `*Segmentation*`

### GroupCorrelationPlot
`GroupCorrelationPlot(object, assay=NULL, feature.group="feature.grp", cor="nCount_RNA_cor")`

- 来源：`visualization.R` · 包：Seurat · 实现：GroupCorrelationPlot

### HoverLocator
`HoverLocator(plot, information=NULL, axes=TRUE, dark.theme=FALSE, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：HoverLocator

### IFeaturePlot
`IFeaturePlot(object, feature, dims=c(1, 2), reduction=NULL, slot='data')`

- 来源：`visualization.R` · 包：Seurat · 实现：IFeaturePlot

### ImageDimPlot
`ImageDimPlot(object, fov=NULL, boundaries=NULL, group.by=NULL, split.by=NULL, cols=NULL, shuffle.cols=FALSE, size=0.5, molecules=NULL, mols.size=0.1, mols.cols=NULL, mols.alpha=1.0, nmols=1000, alpha=1.0, border.color='white', border.size=NULL, na.value='grey50', dark.background=TRUE, crop=FALSE, cells=NULL, overlap=FALSE, axes=FALSE, combine=TRUE, coord.fixed=TRUE, flip_xy=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：ImageDimPlot

### ImageFeaturePlot
`ImageFeaturePlot(object, features, fov=NULL, boundaries=NULL, cols=if (isTRUE(x = blend)) { c("lightgrey..., size=0.5, min.cutoff=NA, max.cutoff=NA, split.by=NULL, molecules=NULL, mols.size=0.1, mols.cols=NULL, nmols=1000, alpha=1.0, border.color='white', border.size=NULL, dark.background=TRUE, blend=FALSE, blend.threshold=0.5, crop=FALSE, cells=NULL, scale=c('feature', 'all', 'none'), overlap=FALSE, axes=FALSE, combine=TRUE, coord.fixed=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：ImageFeaturePlot

### Intensity
`Intensity(color)`

- 来源：`visualization.R` · 包：Seurat · 实现：Intensity

### InteractiveSpatialPlot
`InteractiveSpatialPlot(object, image=NULL, image.scale="lowres", group.by=NULL, alpha=1.0, pt.size.factor=1.0, overlay_image=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：InteractiveSpatialPlot

### ISpatialDimPlot
`ISpatialDimPlot(object, image=NULL, image.scale="lowres", group.by=NULL, alpha=c(0.3, 1))`

- 来源：`visualization.R` · 包：Seurat · 实现：ISpatialDimPlot

### ISpatialFeaturePlot
`ISpatialFeaturePlot(object, feature, image=NULL, image.scale="lowres", slot='data', alpha=c(0.1, 1))`

- 来源：`visualization.R` · 包：Seurat · 实现：ISpatialFeaturePlot

### LabelClusters
`LabelClusters(plot, id, clusters=NULL, labels=NULL, split.by=NULL, repel=TRUE, box=FALSE, geom='GeomPoint', position="median", ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：LabelClusters

### LabelPoints
`LabelPoints(plot, points, labels=NULL, repel=FALSE, xnudge=0.3, ynudge=0.05, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：LabelPoints

### LinkedDimPlot
`LinkedDimPlot(object, dims=1:2, reduction=NULL, image=NULL, image.scale="lowres", group.by=NULL, alpha=c(0.1, 1), combine=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：LinkedDimPlot

### LinkedFeaturePlot
`LinkedFeaturePlot(object, feature, dims=1:2, reduction=NULL, image=NULL, image.scale="lowres", slot='data', alpha=c(0.1, 1), combine=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：LinkedFeaturePlot

### Luminance
`Luminance(color)`

- 来源：`visualization.R` · 包：Seurat · 实现：Luminance

### NoAxes
`NoAxes(..., keep.text=FALSE, keep.ticks=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：NoAxes

### NoGrid
`NoGrid(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：NoGrid

### NoLegend
`NoLegend(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：NoLegend

### PolyDimPlot
`PolyDimPlot(object, group.by=NULL, cells=NULL, poly.data='spatial', flip.coords=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：PolyDimPlot

### PolyFeaturePlot
`PolyFeaturePlot(object, features, cells=NULL, poly.data='spatial', ncol=ceiling(x = length(x = features) / 2), min.cutoff=0, max.cutoff=NA, common.scale=TRUE, flip.coords=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：PolyFeaturePlot

### PurpleAndYellow
`PurpleAndYellow(k=50)`

- 来源：`visualization.R` · 包：Seurat · 实现：PurpleAndYellow

### RestoreLegend
`RestoreLegend(..., position='right')`

- 来源：`visualization.R` · 包：Seurat · 实现：RestoreLegend

### RidgePlot
`RidgePlot(object, features, cols=NULL, idents=NULL, sort=FALSE, assay=NULL, group.by=NULL, y.max=NULL, same.y.lims=FALSE, log=FALSE, ncol=NULL, slot=deprecated(), layer='data', stack=FALSE, combine=TRUE, fill.by=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：RidgePlot

### RotatedAxis
`RotatedAxis(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：RotatedAxis

### SeuratAxes
`SeuratAxes(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：SeuratAxes

### SeuratTheme
`SeuratTheme(?)`

- 来源：`visualization.R` · 包：Seurat · 实现：SeuratTheme

### SingleCorPlot
`SingleCorPlot(data, col.by=NULL, cols=NULL, pt.size=NULL, smooth=FALSE, rows.highlight=NULL, legend.title=NULL, na.value='grey50', span=NULL, raster=NULL, raster.dpi=NULL, plot.cor=TRUE, jitter=TRUE)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleCorPlot

### SingleDimPlot
`SingleDimPlot(data, dims, col.by=NULL, cols=NULL, pt.size=NULL, shape.by=NULL, alpha=1, alpha.by=NULL, stroke.size=NULL, order=NULL, label=FALSE, repel=FALSE, label.size=4, cells.highlight=NULL, cols.highlight='#DE2D26', sizes.highlight=1, na.value='grey50', raster=NULL, raster.dpi=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleDimPlot

### SingleExIPlot
`SingleExIPlot(data, idents, split=NULL, type='violin', sort=FALSE, y.max=NULL, adjust=1, pt.size=0, alpha=1, cols=NULL, seed.use=42, log=FALSE, fill.by='ident', add.noise=TRUE, raster=NULL, raster.dpi=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleExIPlot

### SingleImageMap
`SingleImageMap(data, order=NULL, title=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleImageMap

### SingleImagePlot
`SingleImagePlot(data, col.by=NA, col.factor=TRUE, cols=NULL, shuffle.cols=FALSE, size=0.1, molecules=NULL, mols.size=0.1, mols.cols=NULL, mols.alpha=1.0, alpha=molecules %iff% 0.3 %||% 0.6, border.color='white', border.size=NULL, na.value='grey50', dark.background=TRUE, ...)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleImagePlot

### SingleRasterMap
`SingleRasterMap(data, raster=TRUE, cell.order=NULL, feature.order=NULL, colors=PurpleAndYellow(), disp.min=-2.5, disp.max=2.5, limits=NULL, group.by=NULL)`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleRasterMap

### SingleSpatialPlot
`SingleSpatialPlot(data, image, cols=NULL, image.alpha=1, image.scale="lowres", pt.alpha=NULL, crop=TRUE, pt.size.factor=NULL, shape=21, stroke=NA, stroke.alpha=NA, col.by=NULL, alpha.by=NULL, cells.highlight=NULL, cols.highlight=c('#DE2D26', 'grey50'), geom=c('spatial', 'interactive', 'poly', '..., na.value='grey50')`

- 来源：`visualization.R` · 包：Seurat · 实现：SingleSpatialPlot

### SpatialDimPlot
`SpatialDimPlot(object, group.by=NULL, images=NULL, cols=NULL, crop=TRUE, cells.highlight=NULL, cols.highlight=c('#DE2D26', 'grey50'), facet.highlight=FALSE, label=FALSE, label.size=7, label.color='white', repel=FALSE, ncol=NULL, combine=TRUE, pt.size.factor=1.6, alpha=c(1, 1), image.alpha=1, image.scale="lowres", shape=21, stroke=NA, stroke.alpha=NA, label.box=TRUE, interactive=FALSE, information=NULL, plot_segmentations=FALSE)`

- 来源：`convenience.R` · 包：Seurat · 实现：SpatialDimPlot

### SpatialFeaturePlot
`SpatialFeaturePlot(object, features, images=NULL, crop=TRUE, slot='data', keep.scale="feature", min.cutoff=NA, max.cutoff=NA, ncol=NULL, combine=TRUE, pt.size.factor=1.6, alpha=c(1, 1), image.alpha=1, image.scale="lowres", shape=21, stroke=NA, stroke.alpha=NA, interactive=FALSE, information=NULL, plot_segmentations=FALSE)`

- 来源：`convenience.R` · 包：Seurat · 实现：SpatialFeaturePlot

### SpatialPlot
`SpatialPlot(object, group.by=NULL, features=NULL, images=NULL, cols=NULL, image.alpha=1, image.scale="lowres", crop=TRUE, slot='data', keep.scale="feature", min.cutoff=NA, max.cutoff=NA, cells.highlight=NULL, cols.highlight=c('#DE2D26', 'grey50'), facet.highlight=FALSE, label=FALSE, label.size=5, label.color='white', label.box=TRUE, repel=FALSE, ncol=NULL, combine=TRUE, pt.size.factor=1.6, alpha=c(1, 1), shape=21, stroke=NA, stroke.alpha=NA, interactive=FALSE, do.identify=FALSE, identify.ident=NULL, do.hover=FALSE, information=NULL, plot_segmentations=FALSE)`

- 来源：`visualization.R` · 包：Seurat · 实现：SpatialPlot

### SpatialTheme
`SpatialTheme(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：SpatialTheme

### TSNEPlot
`TSNEPlot(object, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：TSNEPlot

### UMAPPlot
`UMAPPlot(object, ...)`

- 来源：`convenience.R` · 包：Seurat · 实现：UMAPPlot

### VariableFeaturePlot
`VariableFeaturePlot(object, cols=c('black', 'red'), pt.size=1, log=NULL, selection.method=NULL, assay=NULL, raster=NULL, raster.dpi=c(512, 512))`

- 来源：`visualization.R` · 包：Seurat · 实现：VariableFeaturePlot

### VlnPlot
`VlnPlot(object, features, cols=NULL, pt.size=NULL, alpha=1, idents=NULL, sort=FALSE, assay=NULL, group.by=NULL, split.by=NULL, adjust=1, y.max=NULL, same.y.lims=FALSE, log=FALSE, ncol=NULL, slot=deprecated(), layer=NULL, split.plot=FALSE, stack=FALSE, combine=TRUE, fill.by='feature', flip=FALSE, add.noise=TRUE, raster=NULL, raster.dpi=300)`

- 来源：`visualization.R` · 包：Seurat · 实现：VlnPlot

### WhiteBackground
`WhiteBackground(...)`

- 来源：`visualization.R` · 包：Seurat · 实现：WhiteBackground


## MODULE: spatial — 空间转录组（21）

### Boundaries
`Boundaries(object, ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：Boundaries.FOV
- 方法变体：`*FOV*`

### BuildNicheAssay
`BuildNicheAssay(object, fov, group.by, assay="niche", cluster.name="niches", neighbors.k=20, niches.k=4, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：BuildNicheAssay

### CreateCentroids
`CreateCentroids(coords, nsides=Inf, radius=NULL, theta=0L)`

- 来源：`SO:centroids.R` · 包：S3 · 实现：CreateCentroids.default
- 方法变体：`*Centroids*`, `*default*`

### CreateFOV
`CreateFOV(coords, molecules=NULL, assay='Spatial', key=NULL, name=NULL, ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：CreateFOV.Centroids
- 方法变体：`*Centroids*`, `*list*`

### CreateMolecules
`CreateMolecules(coords, ...)`

- 来源：`SO:molecules.R` · 包：S3 · 实现：CreateMolecules.Molecules
- 方法变体：`*Molecules*`, `*NULL*`

### CreateSegmentation
`CreateSegmentation(coords)`

- 来源：`SO:segmentation.R` · 包：S3 · 实现：CreateSegmentation.Segmentation
- 方法变体：`*Segmentation*`

### Crop
`Crop(object, x=NULL, y=NULL, coords=c("plot", "tissue"), ...)`

- 来源：`SO:fov.R` · 包：S3 · 实现：Crop.FOV
- 方法变体：`*FOV*`, `*Molecules*`

### DefaultBoundary
`DefaultBoundary(object)`

- 来源：`SO:fov.R` · 包：S3 · 实现：DefaultBoundary.FOV
- 方法变体：`*FOV*`

### DefaultFOV
`DefaultFOV(object, assay=NULL, ...)`

- 来源：`SO:seurat.R` · 包：S3 · 实现：DefaultFOV.Seurat
- 方法变体：`*Seurat*`

### FilterSlideSeq
`FilterSlideSeq(object, image="image", center=NULL, radius=NULL, do.plot=TRUE)`

- 来源：`objects.R` · 包：Seurat · 实现：FilterSlideSeq

### FindSpatiallyVariableFeatures
`FindSpatiallyVariableFeatures(object, spatial.location, selection.method=c('markvariogram', 'moransi'), r.metric=5, x.cuts=NULL, y.cuts=NULL, verbose=TRUE, layer="scale.data", slot=deprecated(), features=NULL, nfeatures=2000, assay=NULL, image=NULL, ...)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：FindSpatiallyVariableFeatures.default
- 方法变体：`*Assay*`, `*Seurat*`, `*default*`

### GetImage
`GetImage(object, mode=c('grob', 'raster', 'plotly', 'raw'), image=NULL, ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：GetImage.Seurat
- 方法变体：`*STARmap*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`, `*VisiumV1*`

### GetTissueCoordinates
`GetTissueCoordinates(object, image=NULL, full=TRUE, which=NULL, features=NULL, qhulls=FALSE, scale='lowres', cols=c('imagecol', 'imagerow'), ...)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：GetTissueCoordinates.Seurat
- 方法变体：`*Centroids*`, `*FOV*`, `*Molecules*`, `*STARmap*`, `*Segmentation*`, `*Seurat*`, `*SlideSeq*`, `*SpatialImage*`, `*VisiumV1*`, `*VisiumV2*`

### Images
`Images(object, assay=NULL)`

- 来源：`SO:seurat.R` · 包：Seurat · 实现：Images

### Load10X_Spatial
`Load10X_Spatial(data.dir, filename="filtered_feature_bc_matrix.h5", assay="Spatial", slice="slice1", bin.size=NULL, filter.matrix=TRUE, to.upper=FALSE, image=NULL, image.name="tissue_lowres_image.png", segmentation.type=NULL, compact=TRUE, ...)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：Load10X_Spatial

### Overlay
`Overlay(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### Radius
`Radius(object, scale="lowres", ...)`

- 来源：`objects.R` · 包：Seurat · 实现：Radius.VisiumV1

### RunMarkVario
`RunMarkVario(spatial.location, data, ...)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：RunMarkVario

### RunMoransI
`RunMoransI(data, pos, verbose=TRUE)`

- 来源：`preprocessing.R` · 包：Seurat · 实现：RunMoransI

### ScaleFactors
`ScaleFactors(object, ...)`

- 来源：`generics.R` · 包：Seurat · 实现：ScaleFactors

### scalefactors
`scalefactors(spot=1, fiducial=1, hires=1, lowres=1)`

- 来源：`objects.R` · 包：Seurat · 实现：scalefactors


## MODULE: multiome — 多模态 / WNN（1）

### FindMultiModalNeighbors
`FindMultiModalNeighbors(object, reduction.list, dims.list, k.nn=20, l2.norm=TRUE, knn.graph.name="wknn", snn.graph.name="wsnn", weighted.nn.name="weighted.nn", modality.weight.name=NULL, knn.range=200, prune.SNN=1/15, sd.scale=1, cross.contant.list=NULL, smooth=FALSE, return.intermediate=FALSE, modality.weight=NULL, verbose=TRUE)`

- 来源：`clustering.R` · 包：Seurat · 实现：FindMultiModalNeighbors


## MODULE: perturb — Mixscape / 扰动（8）

### CalcPerturbSig
`CalcPerturbSig(object, assay=NULL, features=NULL, slot="data", gd.class="guide_ID", nt.cell.class="NT", split.by=NULL, num.neighbors=NULL, reduction="pca", ndims=15, new.assay.name="PRTB", verbose=TRUE)`

- 来源：`mixscape.R` · 包：Seurat · 实现：CalcPerturbSig

### DEenrichRPlot
`DEenrichRPlot(object, ident.1=NULL, ident.2=NULL, balanced=TRUE, logfc.threshold=0.25, assay=NULL, max.genes, test.use='wilcox', p.val.cutoff=0.05, cols=NULL, enrich.database=NULL, num.pathway=10, return.gene.list=FALSE, ...)`

- 来源：`mixscape.R` · 包：Seurat · 实现：DEenrichRPlot

### MixscapeHeatmap
`MixscapeHeatmap(object, ident.1=NULL, ident.2=NULL, balanced=TRUE, logfc.threshold=0.25, assay="RNA", max.genes=100, test.use='wilcox', max.cells.group=NULL, order.by.prob=TRUE, group.by=NULL, mixscape.class="mixscape_class", prtb.type="KO", fc.name="avg_log2FC", pval.cutoff=5e-2, ...)`

- 来源：`mixscape.R` · 包：Seurat · 实现：MixscapeHeatmap

### MixscapeLDA
`MixscapeLDA(object, assay=NULL, ndims.print=1:5, nfeatures.print=30, reduction.key="LDA_", seed=42, pc.assay="PRTB", labels="gene", nt.label="NT", npcs=10, verbose=TRUE, logfc.threshold=0.25)`

- 来源：`mixscape.R` · 包：Seurat · 实现：MixscapeLDA

### PlotPerturbScore
`PlotPerturbScore(object, target.gene.class="gene", target.gene.ident=NULL, mixscape.class="mixscape_class", col="orange2", split.by=NULL, before.mixscape=FALSE, prtb.type="KO")`

- 来源：`mixscape.R` · 包：Seurat · 实现：PlotPerturbScore

### PrepLDA
`PrepLDA(object, de.assay="RNA", pc.assay="PRTB", labels="gene", nt.label="NT", npcs=10, verbose=TRUE, logfc.threshold=0.25)`

- 来源：`mixscape.R` · 包：Seurat · 实现：PrepLDA

### RunLDA
`RunLDA(object, labels, assay=NULL, verbose=TRUE, ndims.print=1:5, nfeatures.print=30, reduction.key="LDA_", seed=42, features=NULL, reduction.name="lda", ...)`

- 来源：`mixscape.R` · 包：Seurat · 实现：RunLDA.default
- 方法变体：`*Assay*`, `*Seurat*`, `*default*`

### RunMixscape
`RunMixscape(object, assay="PRTB", slot="scale.data", labels="gene", nt.class.name="NT", new.class.name="mixscape_class", min.de.genes=5, min.cells=5, de.assay="RNA", logfc.threshold=0.25, iter.num=10, verbose=FALSE, split.by=NULL, fine.mode=FALSE, fine.mode.labels="guide_ID", prtb.type="KO")`

- 来源：`mixscape.R` · 包：Seurat · 实现：RunMixscape


## MODULE: tree — 聚类树工具（1）

### BuildClusterTree
`BuildClusterTree(object, assay=NULL, features=NULL, dims=NULL, reduction="pca", graph=NULL, slot='data', reorder=FALSE, reorder.numeric=FALSE, verbose=TRUE)`

- 来源：`tree.R` · 包：Seurat · 实现：BuildClusterTree


## MODULE: convert — 格式转换（5）

### as.Graph
`as.Graph(x, weighted=TRUE, ...)`

- 来源：`SO:graph.R` · 包：Seurat · 实现：as.Graph.Matrix
- 方法变体：`*Matrix*`, `*Neighbor*`

### as.Neighbor
`as.Neighbor(x, ...)`

- 来源：`SO:neighbor.R` · 包：Seurat · 实现：as.Neighbor.Graph
- 方法变体：`*Graph*`

### as.Seurat
`as.Seurat(x, slot='counts', assay='RNA', verbose=TRUE, counts='counts', data='logcounts', project='SingleCellExperiment', ...)`

- 来源：`objects.R` · 包：Seurat · 实现：as.Seurat.CellDataSet
- 方法变体：`*CellDataSet*`, `*SingleCellExperiment*`

### as.SingleCellExperiment
`as.SingleCellExperiment(x, assay=NULL, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：as.SingleCellExperiment.Seurat
- 方法变体：`*Seurat*`

### as.sparse
`as.sparse(x, ...)`

- 来源：`objects.R` · 包：Seurat · 实现：as.sparse.IterableMatrix


## MODULE: util — 通用工具 / 模块评分（21）

### AddModuleScore
`AddModuleScore(object, features, pool=NULL, nbin=24, ctrl=100, k=FALSE, assay=NULL, name='Cluster', seed=1, search=FALSE, slot='data', kmeans.obj, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：AddModuleScore.Seurat
- 方法变体：`*Assay*`, `*Seurat*`, `*StdAssay*`

### as.data.frame
`as.data.frame(x, row.names=NULL, optional=FALSE, stringsAsFactors=getOption(x = "stringsAsFactors", def..., ...)`

- 来源：`utilities.R` · 包：S3 · 实现：as.data.frame.Matrix
- 方法变体：`*Matrix*`

### CaseMatch
`CaseMatch(search, match)`

- 来源：`utilities.R` · 包：Seurat · 实现：CaseMatch

### CellCycleScoring
`CellCycleScoring(object, s.features, g2m.features, ctrl=NULL, set.ident=FALSE, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：CellCycleScoring

### CollapseSpeciesExpressionMatrix
`CollapseSpeciesExpressionMatrix(object, prefix="HUMAN_", controls="MOUSE_", ncontrols=100)`

- 来源：`utilities.R` · 包：Seurat · 实现：CollapseSpeciesExpressionMatrix

### CustomDistance
`CustomDistance(my.mat, my.function, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：CustomDistance

### ExpMean
`ExpMean(x, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：ExpMean

### ExpSD
`ExpSD(x)`

- 来源：`utilities.R` · 包：Seurat · 实现：ExpSD

### ExpVar
`ExpVar(x)`

- 来源：`utilities.R` · 包：Seurat · 实现：ExpVar

### FastRowScale
`FastRowScale(mat, center=TRUE, scale=TRUE, scale_max=10)`

- 来源：`utilities.R` · 包：Seurat · 实现：FastRowScale

### GeneSymbolThesarus
`GeneSymbolThesarus(symbols, timeout=10, several.ok=FALSE, search.types=c('alias_symbol', 'prev_symbol'), verbose=TRUE, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：GeneSymbolThesarus

### GroupCorrelation
`GroupCorrelation(object, assay=NULL, slot="scale.data", var=NULL, group.assay=NULL, min.cells=5, ngroups=6, do.plot=TRUE)`

- 来源：`utilities.R` · 包：Seurat · 实现：GroupCorrelation

### IsGlobal
`IsGlobal(object, ...)`

- 来源：`SO:default.R` · 包：Seurat · 实现：IsGlobal.default
- 方法变体：`*DimReduc*`, `*SpatialImage*`, `*default*`

### IsMatrixEmpty
`IsMatrixEmpty(x)`

- 来源：`SO:utils.R` · 包：S3 · 实现：IsMatrixEmpty.default
- 方法变体：`*default*`

### LogVMR
`LogVMR(x, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：LogVMR

### MetaFeature
`MetaFeature(object, features, meta.name='metafeature', cells=NULL, assay=NULL, slot='data')`

- 来源：`utilities.R` · 包：Seurat · 实现：MetaFeature

### MinMax
`MinMax(data, min, max)`

- 来源：`utilities.R` · 包：Seurat · 实现：MinMax

### PercentAbove
`PercentAbove(x, threshold)`

- 来源：`utilities.R` · 包：Seurat · 实现：PercentAbove

### RandomName
`RandomName(length=5L, chars=letters, ...)`

- 来源：`SO:utils.R` · 包：SeuratObject · 实现：RandomName

### RowMergeSparseMatrices
`RowMergeSparseMatrices(mat1, mat2)`

- 来源：`SO:utils.R` · 包：Seurat · 实现：RowMergeSparseMatrices

### UpdateSymbolList
`UpdateSymbolList(symbols, timeout=10, several.ok=FALSE, verbose=TRUE, ...)`

- 来源：`utilities.R` · 包：Seurat · 实现：UpdateSymbolList


## MODULE: misc — 其他（13）

### %!NA%
`%!NA%(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### %!na%
`%!na%(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### %iff%
`%iff%(?)`

- 来源：`—` · 包：Seurat · 实现：—

### %NA%
`%NA%(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### %na%
`%na%(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### %||%
`%||%(?)`

- 来源：`—` · 包：Seurat · 实现：—

### .KeyPattern
`.KeyPattern(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### .RandomKey
`.RandomKey(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### handlers
`handlers(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### plan
`plan(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### SCTResults<-
`SCTResults<-(?)`

- 来源：`—` · 包：Seurat · 实现：—

### t
`t(?)`

- 来源：`—` · 包：SeuratObject · 实现：—

### with_progress
`with_progress(?)`

- 来源：`—` · 包：SeuratObject · 实现：—
