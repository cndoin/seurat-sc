#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sc_plan.py —— 一句话需求 -> Seurat 流程建议（离线规则，不联网、不调用 LLM）

用法：
  python sc_plan.py "两个样本 PBMC 整合后找 marker"
  python sc_plan.py "空间转录组 Visium 数据分析" --json
  python sc_plan.py --list

输出的是「该按什么顺序调哪些函数」，不是可直接跑的完整脚本；
完整模板在 references/workflows.md。
"""
import io, os, sys, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.join(HERE, "whitelist.json")

PLANS = [
    {
        "id": "basic-cluster",
        "title": "单样本标准聚类（LogNormalize 路线）",
        "keys": ["标准流程", "聚类", "基础分析", "常规", "pbmc", "单样本", "basic", "cluster", "standard", "走一遍", "流程"],
        "steps": [
            "CreateSeuratObject(min.cells=3, min.features=200)",
            "PercentageFeatureSet(pattern='^MT-') 计算线粒体比例",
            "subset() 按 nFeature_RNA / percent.mt 过滤",
            "NormalizeData(layer='counts', save='data')",
            "FindVariableFeatures(selection.method='vst', nfeatures=2000)",
            "ScaleData(layer='data', save='scale.data')",
            "RunPCA(npcs=30~50, layer='scale.data')  + ElbowPlot 定 PCs",
            "FindNeighbors(dims=1:X) -> FindClusters(resolution=0.5~1.2)",
            "RunUMAP(dims=1:X, seed.use=42)",
            "FindAllMarkers(only.pos=TRUE) 找各群 marker",
        ],
        "notes": ["dims 必须先用 ElbowPlot/JackStraw 定，不要拍脑袋写 1:30",
                  "FindClusters 的 resolution 决定群数，先跑 0.5 再调"],
    },
    {
        "id": "sct",
        "title": "SCTransform 路线",
        "keys": ["sct", "sctransform", "vst", "正则化", "归一化", "sctransform流程", "v2"],
        "steps": [
            "SCTransform(assay='RNA', new.assay.name='SCT', vst.flavor='v2', variable.features.n=3000)",
            "RunPCA(assay='SCT') -> RunUMAP -> FindNeighbors -> FindClusters（同上）",
            "找 marker 前必须先 PrepSCTFindMarkers(assay='SCT')",
            "FindMarkers(assay='SCT', slot='data') / FindAllMarkers(assay='SCT')",
        ],
        "notes": ["走 SCT 就不要再 NormalizeData / ScaleData，会重复",
                  "SCT 上不要 ScaleData；PCA 直接用 SCT assay",
                  "多样本 SCT 整合需先 split() 再逐层 SCTransform"],
    },
    {
        "id": "integrate-v5",
        "title": "多样本整合（v5 layers + IntegrateLayers）",
        "keys": ["整合", "去批次", "批次", "多样本", "合并", "integration", "integrate", "batch", "harmony", "cca", "rpca", "jointpca"],
        "steps": [
            "merge() 合并样本（add.cell.ids 加前缀）或直接读入多样本",
            "obj[['RNA']] <- split(obj[['RNA']], f=obj$orig.ident) 切层",
            "NormalizeData -> FindVariableFeatures -> ScaleData -> RunPCA（逐层自动跑）",
            "IntegrateLayers(method=RPCAIntegration / CCAIntegration / HarmonyIntegration / JointPCAIntegration, orig.reduction='pca', new.reduction='integrated.rpca')",
            "JoinLayers() 合并层",
            "FindNeighbors(reduction='integrated.rpca', dims=1:30) -> FindClusters -> RunUMAP(reduction='integrated.rpca')",
        ],
        "notes": ["v5 首选这条；IntegrateData() 是 v4 API，只在要返回整合矩阵时用",
                  "Harmony 走 HarmonyIntegration，需装 harmony 包",
                  "样本量大 / 差异大：RPCA 比 CCA 稳且快"],
    },
    {
        "id": "map-query",
        "title": "参考映射 / 标签转移",
        "keys": ["映射", "注释", "转移", "标签", "参考", "reference", "query", "mapquery", "azimuth", "transfer", "细胞类型注释"],
        "steps": [
            "FindTransferAnchors(reference=ref, query=q, dims=1:30, reduction='pcaproject')",
            "TransferData(anchorset=anchors, refdata=ref$celltype) 得到 prediction.score",
            "按 prediction.score 阈值过滤低置信细胞",
            "或一步到位：MapQuery(anchorset, reference, query, refdata)",
        ],
        "notes": ["reference 与 query 必须是同物种、同模态",
                  "Azimuth 结果可用 AddAzimuthScores / AddAzimuthResults 写回"],
    },
    {
        "id": "bridge",
        "title": "Bridge 整合（把新数据挂到已整合参考上）",
        "keys": ["bridge", "桥接", "已整合参考", "新数据加入", "bridgeintegration"],
        "steps": [
            "PrepareBridgeReference(reference, bridge, ref.reduction, ...)",
            "FindBridgeTransferAnchors(reference, bridge, ...)",
            "FindBridgeIntegrationAnchors(query, bridge, ...)",
            "把 query 投影到已整合参考空间",
        ],
        "notes": ["适合「参考集已整合好，只想把新样本挂上去」的场景",
                  "不适合从零整合多样本"],
    },
    {
        "id": "sketch",
        "title": "百万级细胞 Sketch 流程",
        "keys": ["百万", "大数据", "百万细胞", "sketch", "草图", "太大", "内存", "超大规模"],
        "steps": [
            "SketchData(assay='RNA', ncells=20000~50000, sketched.assay='sketch', method='LeverageScore', seed=123)",
            "DefaultAssay(obj) <- 'sketch'，在草图上跑标准流程（Normalize/FindVariableFeatures/Scale/PCA/Cluster/UMAP）",
            "ProjectData(sketched.assay='sketch', assay='RNA', full.reduction='pca', sketched.reduction='pca.sketch') 把降维投影回全量",
            "TransferSketchLabels() 把草图上的 cluster 标签传回全量细胞",
        ],
        "notes": ["sketch 上的 cluster label 要 TransferSketchLabels 才能回到全量细胞",
                  "差异表达建议在全量细胞上做"],
    },
    {
        "id": "de",
        "title": "差异表达 / marker 基因",
        "keys": ["差异", "差异表达", "marker", "标记基因", "deg", "de", "找基因", "差异基因", "上调", "下调"],
        "steps": [
            "确认 Idents 或 group.by 已设好",
            "FindMarkers(ident.1, ident.2, test.use='wilcox', min.pct=0.25, logfc.threshold=0.25)",
            "或 FindAllMarkers(only.pos=TRUE, min.pct=0.25, return.thresh=0.01)",
            "SCT assay 必须先 PrepSCTFindMarkers()",
            "样本间比较用 FindConservedMarkers(ident.1, grouping.var='orig.ident')",
            "拟 bulk：AggregateExpression(group.by=c('seurat_clusters','orig.ident')) 或 PseudobulkExpression()",
        ],
        "notes": ["test.use 可选 wilcox / bimod / roc / t / negbinom / poisson / LR / MAST / DESeq2",
                  "MAST/DESeq2 需要额外装包；默认 wilcox 最快",
                  "min.pct 太小会得到大量无意义基因"],
    },
    {
        "id": "spatial",
        "title": "空间转录组（Visium / Visium HD / Xenium / Vizgen / Nanostring / Akoya）",
        "keys": ["空间", "空间转录组", "visium", "visium hd", "xenium", "vizgen", "nanostring", "akoya", "stereoseq", "slice", "组织切片"],
        "steps": [
            "Load10X_Spatial(data.dir, bin.size=) / LoadXenium / LoadVizgen / LoadNanostring / LoadAkoya",
            "QC：VlnPlot/SpatialFeaturePlot 看 nFeature_Spatial",
            "SCTransform(assay='Spatial') 或 NormalizeData",
            "FindSpatiallyVariableFeatures(selection.method='moransi' 或 'markvariogram')",
            "RunMoransI / RunMarkVario 单独算空间自相关",
            "SpatialFeaturePlot / SpatialDimPlot 出图",
            "可选：BuildNicheAssay(fov, group.by) 做 niche 分析",
        ],
        "notes": ["RunMoransI 的签名是 (data, pos, verbose)，没有 features 参数 —— 别写错",
                  "Visium HD 用 bin.size 指定 8/16 微米 bin",
                  "Xenium/Vizgen 这类单细胞级数据可读为带坐标的 Seurat 对象"],
    },
    {
        "id": "multiome",
        "title": "多模态 / WNN（RNA + ATAC / ADT）",
        "keys": ["多模态", "wnn", "atac", "rna+atac", "cite", "adt", "multiome", "多组学"],
        "steps": [
            "各模态分别建 assay 并各自降维（RNA: PCA；ATAC: LSI）",
            "FindMultiModalNeighbors(reduction.list=list('pca','lsi'), dims.list=list(1:30, 2:30), modality.weight.name=...)",
            "RunUMAP(nn.name='weighted.nn', reduction.name='wnn.umap', reduction.key='wnnUMAP_')",
            "FindClusters(graph.name='wsnn', algorithm=3, resolution=1)",
        ],
        "notes": ["**没有 RunWNN() 这个函数** —— 源码里不存在，别写",
                  "ATAC 侧的 LSI 通常来自 Signac（第三方包）"],
    },
    {
        "id": "qc",
        "title": "质量控制与过滤",
        "keys": ["qc", "质控", "过滤", "线粒体", "核糖体", "双细胞", "percent.mt", "质控图", "过滤细胞"],
        "steps": [
            "PercentageFeatureSet(pattern='^MT-') -> percent.mt；核糖体 ^RP[SL]",
            "VlnPlot / FeatureScatter(nFeature_RNA vs nCount_RNA) 看分布",
            "subset(subset = nFeature_RNA > X & nFeature_RNA < Y & percent.mt < Z)",
            "细胞周期：CellCycleScoring(s.features, g2m.features)",
            "去双细胞：Seurat 本体不提供，用 scDblFinder / DoubletFinder（第三方）",
        ],
        "notes": ["阈值必须看图定，不要写死 5%/2500",
                  "人 MT- 大写；小鼠是 mt- 小写 —— 别猜物种"],
    },
    {
        "id": "perturb",
        "title": "Mixscape / 扰动分析",
        "keys": ["mixscape", "扰动", "crispr", "perturb", "敲除", "敲低", "lda"],
        "steps": [
            "CalcPerturbSig(object, assay='RNA', gd.class='guide', ...)",
            "RunMixscape(object, assay='PRTB', labels='guide', nt.cell.class='NT', ...)",
            "PlotPerturbScore(target.gene.class, mixscape.class) / MixscapeHeatmap(ident.1, ident.2) 看结果",
            "差异分析回到 FindMarkers(assay='RNA')，配合 mixscape_class 分组",
            "可选：MixscapeLDA / PrepLDA / RunLDA 做主题建模",
        ],
        "notes": ["需要 Perturb-seq / CROP-seq 这类带 guide 的数据",
                  "PerturbDiff / TopDEGenesMixscape 是内部函数、未导出，不能调用"],
    },
    {
        "id": "io",
        "title": "数据读取与写出",
        "keys": ["读取", "读入", "导入", "10x", "cellranger", "h5", "mtx", "rds", "保存", "导出", "read", "load", "save"],
        "steps": [
            "10x 三文件：Read10X(data.dir) -> CreateSeuratObject",
            "10x h5：Read10X_h5(filename)",
            "非 10x 矩阵：ReadMtx(mtx, features, cells)",
            "h5ad：SeuratDisk::LoadH5Seurat()（第三方）",
            "保存：SaveSeuratRds() / LoadSeuratRds()；saveRDS() 亦可",
        ],
        "notes": ["Read10X 的 data.dir 指向 filtered_feature_bc_matrix 所在目录",
                  "矩阵行列搞反会导致 CreateSeuratObject 报维度错"],
    },
    {
        "id": "annotate",
        "title": "细胞类型注释与重命名",
        "keys": ["注释", "重命名", "改名", "细胞类型", "rename", "idents", "细胞群命名"],
        "steps": [
            "new.names <- c('0'='T cell', '1'='B cell', ...)",
            "obj <- RenameIdents(obj, new.names)",
            "obj$celltype <- Idents(obj) 固化到 meta.data",
            "或用 FindTransferAnchors/TransferData 自动注释（见 map-query）",
        ],
        "notes": ["RenameIdents 的命名向量是 旧名=新名",
                  "注释依据必须来自 marker 或参考集，不要凭空命名"],
    },
]

def score(plan, q):
    ql = q.lower()
    s = 0
    for k in plan["keys"]:
        if k.lower() in ql:
            s += max(2, len(k))
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="一句话需求")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        for p in PLANS:
            print("%-14s %s" % (p["id"], p["title"]))
        return 0
    if not a.query:
        ap.print_help()
        return 2

    ranked = sorted(((score(p, a.query), p) for p in PLANS),
                    key=lambda x: -x[0])
    hits = [(s, p) for s, p in ranked if s > 0]
    if not hits:
        sys.stderr.write("没有匹配到已知流程，试试 --list 看支持哪些，或换个说法\n")
        return 1

    if a.json:
        print(json.dumps([{"id": p["id"], "title": p["title"], "score": s,
                           "steps": p["steps"], "notes": p["notes"]}
                          for s, p in hits[:3]], ensure_ascii=False, indent=2))
        return 0

    print("需求: %s" % a.query)
    print()
    for s, p in hits[:3]:
        print("== %s  （匹配度 %d）" % (p["title"], s))
        for i, st in enumerate(p["steps"], 1):
            print("   %d. %s" % (i, st))
        if p["notes"]:
            print("   注意:")
            for nt in p["notes"]:
                print("     - %s" % nt)
        print()
    print("完整代码模板见 references/workflows.md；写完后必须跑 tools/sc_lint.py 校验。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
