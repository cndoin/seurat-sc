# -*- coding: utf-8 -*-
"""生成 seurat-sc skill 的事实文件：
  - references/api-signatures.md   全量函数真实签名（可 grep）
  - references/function-index.md   按模块分类的索引
  - tools/whitelist.json           供 sc_lint.py 做函数/参数存在性校验
"""
import io, os, json, re

_HERE = os.path.dirname(os.path.abspath(__file__))        # tools/etl
SKILL = os.path.dirname(os.path.dirname(_HERE))           # skill 根目录
RAW = os.path.abspath(os.environ.get(
    "SEURAT_RAW", os.path.join(SKILL, ".build", "raw")))
os.makedirs(os.path.join(SKILL, "references"), exist_ok=True)
os.makedirs(os.path.join(SKILL, "tools"), exist_ok=True)
os.makedirs(os.path.join(SKILL, "scripts"), exist_ok=True)

d = json.loads(io.open(os.path.join(RAW, "api_full.json"), encoding="utf-8").read())
fns = d["functions"]

# ---------------- 模块分类 ----------------
# 显式表优先；未命中的按定义文件兜底
TAG = {}

def tagmany(names, t):
    for n in names:
        TAG[n] = t

tagmany("""Read10X Read10X_h5 Read10X_Image Read10X_Coordinates Read10X_ScaleFactors
Read10X_Segmentations Read10X_probe_metadata Read10X_HD_GeoJson ReadMtx ReadAkoya
ReadNanostring ReadXenium ReadVizgen ReadSlideSeq ReadVitessce ReadParseBio
ReadSTARsolo Load10X_Spatial LoadAkoya LoadHuBMAPCODEX LoadNanostring LoadVizgen
LoadXenium LoadSTARmap LoadCurioSeeker LoadAnnoyIndex SaveAnnoyIndex Read10X""".split(), "io")
tagmany("SaveSeuratRds LoadSeuratRds".split(), "io")

tagmany("""PercentageFeatureSet SubsetByBarcodeInflections CalculateBarcodeInflections
BarcodeInflectionsPlot CellCycleScoring HTODemux MULTIseqDemux SampleUMI
HTOHeatmap ClassifyCells ComputeRMetric FindThresh GetResidual""".split(), "qc")

tagmany("""NormalizeData LogNormalize SCTransform ScaleData RegressOutMatrix RelativeCounts
CustomNormalize PrepSCTFindMarkers PrepSCTIntegration SelectSCTIntegrationFeatures
SCTResults GetResidualSCTModel SCTModel_to_vst IsSCT""".split(), "norm")

tagmany("""FindVariableFeatures VST FindSpatiallyVariableFeatures SVFInfo HVFInfo
VariableFeatures VariableFeatures<- DISP CalcDispersion CalcN MVP PrepVSTResults
TopFeatures""".split(), "hvg")

tagmany("""RunPCA RunSPCA RunSLSI RunICA RunUMAP RunTSNE RunCCA ProjectDim ProjectUMAP
JackStraw ScoreJackStraw ElbowPlot JackStrawPlot VizDimLoadings DimHeatmap
PCHeatmap PCAPlot L2Dim PCASigGenes L2CCA L2Norm Embeddings Loadings Loadings<-""".split(), "dr")

tagmany("""FindNeighbors FindClusters FindSubCluster BuildClusterTree PlotClusterTree
RunModularityClustering RunLeiden AnnoyNN HnswNN NNdist NNPlot Idents Idents<-
StashIdent SetIdent SetQuantile RenameIdents ReorderIdent WhichCells CellsByIdentities
RegroupIdents GroupSingletons ComputeSNNwidth""".split(), "cluster")

tagmany("""FindMarkers FindAllMarkers FindConservedMarkers FoldChange WilcoxDETest
MASTDETest DESeq2DETest LRDETest NBModelComparison DifferentialAUC DifferentialLRT
DiffTTest DiffExpTest MarkerTest AUCMarkerTest DEmethods_noprefilter DEmethods_latent
DEmethods_checkdots DEmethods_nocorrect DEmethods_counts PerformDE ValidateCellGroups
IdentsToCells AggregateExpression AverageExpression PseudobulkExpression
CreateCategoryMatrix""".split(), "de")

tagmany("""FindIntegrationAnchors IntegrateData IntegrateLayers IntegrateEmbeddings
SelectIntegrationFeatures SelectIntegrationFeatures5 FindTransferAnchors TransferData
MapQuery MappingScore CCAIntegration RPCAIntegration HarmonyIntegration
JointPCAIntegration FastRPCAIntegration FindBridgeTransferAnchors
FindBridgeIntegrationAnchors PrepareBridgeReference BridgeCellsRepresentation
FindBridgeAnchor AddAzimuthResults AddAzimuthScores PredictAssay ProjectIntegration
FindAssayAnchor RunIntegration LocalStruct MixingMetric ScoreAnchors FilterAnchors
AnnotateAnchors MappingScore GetIntegrationData SetIntegrationData CreateIntegrationGroups""".split(), "integrate")

tagmany("""DimPlot FeaturePlot VlnPlot RidgePlot DotPlot DoHeatmap CellScatter
FeatureScatter VariableFeaturePlot UMAPPlot TSNEPlot SpatialDimPlot
SpatialFeaturePlot SpatialPlot ImageDimPlot ImageFeaturePlot PolyDimPlot
PolyFeaturePlot LinkedDimPlot LinkedFeaturePlot InteractiveSpatialPlot
CombinePlots LabelClusters LabelPoints CustomPalette DiscretePalette
GroupCorrelationPlot SingleDimPlot SingleImagePlot SingleSpatialPlot
SingleRasterMap SinglePolyPlot NoLegend NoAxes NoGrid RotatedAxis DarkTheme
FontSize CenterTitle BoldTitle WhiteBackground RestoreLegend""".split(), "viz")

tagmany("""Load10X_Spatial FindSpatiallyVariableFeatures RunMoransI RunMarkVario
BuildNicheAssay GetTissueCoordinates GetImage Images Images<- Radius ScaleFactors
Crop Overlay CreateFOV CreateCentroids CreateMolecules CreateSegmentation Boundaries
DefaultBoundary DefaultFOV DefaultImage NullImage Format10X_GeoJson_CellID
scalefactors CellsByImage FilterSlideSeq""".split(), "spatial")

tagmany("""FindMultiModalNeighbors CreateDummyAssay CollapseSpeciesExpressionMatrix
as.CellDataSet.Seurat as.Seurat.CellDataSet""".split(), "multiome")

tagmany("""RunMixscape CalcPerturbSig MixscapeLDA PrepLDA RunLDA MixscapeHeatmap
PlotPerturbScore DEenrichRPlot TopDEGenesMixscape PerturbDiff ProjectVec
DefineNormalMixscape GetMissingPerturb""".split(), "perturb")

tagmany("SketchData ProjectData TransferSketchLabels LeverageScore CountSketch GaussianSketch JLEmbed FeatureSketch UnSketchEmbeddings".split(), "sketch")

tagmany("""CreateSeuratObject CreateAssayObject CreateAssay5Object CreateDimReducObject
CreateSCTAssayObject GetAssayData SetAssayData LayerData JoinLayers split merge subset
DefaultAssay DefaultAssay<- Assays Layers Cells Features FetchData RenameCells
AddMetaData DietSeurat SplitObject UpdateSeuratObject CastAssay Command Misc Misc<- Tool
Tool<- Key Key<- Index Index<- Neighbors Distances Indices Graphs Project Project<-
Reductions Stdev SVFInfo""".split(), "object")

tagmany("""as.Seurat as.SingleCellExperiment as.sparse as.Graph as.Neighbor
as.sparse.IterableMatrix as.sparse.H5Group as.data.frame.Matrix
as.Seurat.SingleCellExperiment as.SingleCellExperiment.Seurat""".split(), "convert")

tagmany("""AddModuleScore CellCycleScoring ExpMean ExpSD ExpVar FastRowScale LogVMR
MetaFeature MinMax PercentAbove GroupCorrelation CaseMatch UpdateSymbolList
GeneSymbolThesarus RandomName MergeSparseMatrices RowMergeSparseMatrices
CollapseSpeciesExpressionMatrix IsGlobal IsMatrixEmpty""".split(), "util")

tagmany("""BuildClusterTree DFT GetAllInternalNodes GetDescendants GetLeftDescendants
GetRightDescendants MergeNode NodeHasChild NodeHasOnlyChildren""".split(), "tree")

# 文件兜底
FILE_TAG = {
    "preprocessing.R": "norm", "preprocessing5.R": "norm",
    "dimensional_reduction.R": "dr", "clustering.R": "cluster",
    "differential_expression.R": "de", "integration.R": "integrate",
    "integration5.R": "integrate", "visualization.R": "viz",
    "convenience.R": "viz", "utilities.R": "util", "objects.R": "object",
    "sketching.R": "sketch", "mixscape.R": "perturb", "tree.R": "tree",
    "data.R": "data", "generics.R": "generic", "reexports.R": "reexport",
}
for name, r in fns.items():
    if name in TAG:
        continue
    f = r.get("file") or ""
    if f.startswith("SO:"):
        TAG[name] = "object"
    else:
        TAG[name] = FILE_TAG.get(f, "misc")

MODULES = [
    ("io", "数据读取 / 写出"),
    ("object", "对象结构 / Layers 操作"),
    ("qc", "质量控制 / 去双细胞 / 细胞周期"),
    ("norm", "归一化 / SCTransform / ScaleData"),
    ("hvg", "高变基因 / 空间可变基因"),
    ("dr", "降维 PCA / UMAP / tSNE / SLSI"),
    ("cluster", "聚类 / 分群注释 / 聚类树"),
    ("de", "差异表达 / 拟 bulk 聚合"),
    ("integrate", "多样本整合 / 参考映射 / Bridge"),
    ("sketch", "Sketch 大数据草图"),
    ("viz", "可视化"),
    ("spatial", "空间转录组"),
    ("multiome", "多模态 / WNN"),
    ("perturb", "Mixscape / 扰动"),
    ("tree", "聚类树工具"),
    ("convert", "格式转换"),
    ("util", "通用工具 / 模块评分"),
    ("misc", "其他"),
]

# ---------------- 生成 api-signatures.md ----------------
def fmt_args(args, maxlen=40):
    out = []
    for a in args:
        n = a["name"]
        dv = a["default"]
        if dv is None:
            out.append(n)
        else:
            dv = " ".join(dv.split())
            if len(dv) > maxlen:
                dv = dv[:maxlen - 3] + "..."
            out.append("%s=%s" % (n, dv))
    return ", ".join(out)

lines = []
lines.append("# Seurat 全量函数签名库（自源码提取，非文档转述）")
lines.append("")
lines.append("> 数据源：github.com/satijalab/seurat `master`（Seurat %s）"
            " + mojaveazure/seurat-object `develop`（SeuratObject %s）。"
            % (d["seurat_version"], d["seuratobject_version"]))
lines.append("> 每条签名由 `R/` 源码的真实 `formals` 解析得到；S3 generic 取其全部 method 参数的并集。")
lines.append("> 用法：`grep -n \"^## <函数名>\" references/api-signatures.md` 精确查，不要整篇读。")
lines.append("")
lines.append("共 %d 个已知符号，其中 %d 个解析到真实参数表。" %
             (len(fns), sum(1 for r in fns.values() if r["args"])))
lines.append("")

bymod = {}
for name, r in fns.items():
    bymod.setdefault(TAG[name], []).append(name)

for mod, title in MODULES:
    names = sorted(bymod.get(mod, []), key=lambda x: x.lower())
    if not names:
        continue
    lines.append("")
    lines.append("## MODULE: %s — %s（%d）" % (mod, title, len(names)))
    lines.append("")
    for name in names:
        r = fns[name]
        sig = fmt_args(r["args"])
        src = r.get("file") or "—"
        pkg = r.get("pkg", "?")
        defn = r.get("def") or "—"
        lines.append("### %s" % name)
        lines.append("`%s(%s)`" % (name, sig if sig else "?"))
        lines.append("")
        lines.append("- 来源：`%s` · 包：%s · 实现：%s" % (src, pkg, defn))
        if r.get("variants"):
            lines.append("- 方法变体：%s" % ", ".join("`*%s*`" % v for v in r["variants"][:12]))
        lines.append("")

# ---------------- 生成 function-index.md ----------------
idx = []
idx.append("# Seurat 函数分类索引")
idx.append("")
idx.append("版本：Seurat %s / SeuratObject %s。用于快速定位「该用哪个函数」；"
           "签名查 `api-signatures.md`。" % (d["seurat_version"], d["seuratobject_version"]))
idx.append("")
idx.append("| 模块 | 函数 |")
idx.append("| --- | --- |")
for mod, title in MODULES:
    names = sorted(bymod.get(mod, []), key=lambda x: x.lower())
    if not names:
        continue
    idx.append("| **%s** %s | %s |" % (mod, title, ", ".join("`%s`" % n for n in names)))
idx.append("")
idx.append("## S3 method 覆盖（%d 条）" % len(d["s3methods"]))
idx.append("")
idx.append("形如 `generic.class`；调用时写 `generic(obj, ...)` 由 R 自动分派。")
idx.append("")
gens = {}
for x in d["s3methods"]:
    gens.setdefault(x["generic"], []).append(x["class"])
idx.append("| generic | 支持的方法类 |")
idx.append("| --- | --- |")
for g in sorted(gens, key=lambda x: x.lower()):
    idx.append("| `%s` | %s |" % (g, ", ".join("`%s`" % c for c in sorted(gens[g]))))
idx.append("")
idx.append("## S4 类（%d）" % len(d["s4classes"]))
idx.append("")
idx.append(", ".join("`%s`" % c for c in sorted(set(d["s4classes"]))))
idx.append("")

def w(path, text):
    with io.open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    print("written", path, len(text), "chars")

w(os.path.join(SKILL, "references", "api-signatures.md"), "\n".join(lines))
w(os.path.join(SKILL, "references", "function-index.md"), "\n".join(idx))

# ---------------- whitelist.json ----------------
# ---------------- deprecated 参数（源码里默认值为 deprecated() 的，硬事实） ----------------
DEPRE_TIPS = {
    "slot": "v5 用 layer=（或 save=）取代 slot=",
    "sort.cell": "已移除，用 order=",
    "do.print": "已移除，用 ndims.print / nfeatures.print",
    "assay.use": "用 assay=",
    "reduction.use": "用 reduction=",
    "dims.use": "用 dims=",
    "verbose": None,
}
deprecated = {}
for n, r in fns.items():
    hits = {}
    for a in r["args"]:
        dv = (a.get("default") or "")
        if "deprecated()" in dv or "deprecated(" in dv:
            hits[a["name"]] = DEPRE_TIPS.get(a["name"]) or "该参数已弃用"
    if hits:
        deprecated[n] = hits
print("deprecated params found in", len(deprecated), "functions")
print("  sample:", list(deprecated.items())[:6])

wl = {
    "generated_from": {
        "seurat": d["seurat_version"],
        "seuratobject": d["seuratobject_version"],
        "source": "github.com/satijalab/seurat@master + mojaveazure/seurat-object@develop",
    },
    "symbols": {
        n: {
            "pkg": r.get("pkg"),
            "module": TAG[n],
            "args": [a["name"] for a in r["args"]],
            "def": r.get("def"),
        }
        for n, r in fns.items()
    },
    "deprecated_args": deprecated,
}
with io.open(os.path.join(SKILL, "tools", "whitelist.json"), "wb") as f:
    f.write(json.dumps(wl, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
print("written whitelist.json", len(wl["symbols"]), "symbols")

# 统计
print()
for mod, title in MODULES:
    print("  %-10s %d" % (mod, len(bymod.get(mod, []))))
