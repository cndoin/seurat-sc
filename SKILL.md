---
# 下列两个字段是 Claude Agent Skill 的官方必需字段（详见 Claude 官方规范）。
name: seurat-sc
description: "Seurat v5 单细胞与空间转录组分析助手。用于编写、审查、调试、编排 Seurat（R）分析脚本，覆盖 10x/CellRanger/h5/mtx、Visium/Visium HD/Xenium 数据读取、QC 过滤、LogNormalize/SCTransform、FindVariableFeatures、ScaleData、RunPCA/RunUMAP、FindNeighbors/FindClusters、FindMarkers/FindAllMarkers、多样本整合（CCA/RPCA/Harmony/JointPCA/Sketch/Bridge）、参考映射与标签转移（FindTransferAnchors/MapQuery/Azimuth）、细胞周期与模块评分、拟 bulk 聚合、空间可变基因、Mixscape、WNN 多模态、SeuratObject 的 layers/split/merge/JoinLayers。适用于 scRNA-seq、单细胞测序、PBMC、UMAP 聚类、差异表达 marker、细胞注释、去批次整合、线粒体基因百分比、空间转录组、ATAC+RNA 多模态、h5seurat、Seurat v5、layers 等场景，也用于把分析改写成可复现脚本或流水线。"
# 以下字段是 WorkBuddy 宿主扩展，Claude Code 会忽略它们（不报错、不影响解析）。
# 真正的许可证以仓库根目录的 LICENSE 文件为准，这里仅作元数据标注。
license: MIT
version: 1.0.0
allowed-tools: Bash, Read, Grep, Glob
agent_created: true
---

# Seurat v5 · 单细胞分析编排技能

面向 **Seurat 5.x**（本技能事实底座取自源码：Seurat `5.5.1.9005` + SeuratObject `5.0.2`）。

本技能负责：**选对函数 → 写对参数 → 校验脚本 → 编排流程 → 解读报错**。
不负责替用户猜数据、猜基因、猜细胞类型 —— 那些必须由用户给或从结果里读。

---

## 一、不可违反的事实（违反 = 交付幻觉代码）

1. **任何一个 Seurat 函数名，必须能在 `tools/whitelist.json` 里查到。**
   白名单是从 `NAMESPACE` + `R/` 源码解析出的 406 个真实符号。
   交付任何 R 代码前，**必须**跑 `tools/sc_lint.py`，把 error 清零。
   这是本技能存在的第一理由：Seurat 是 LLM 幻觉重灾区。

2. **已知高频幻觉函数（源码里根本没有，见到立即改掉）**

   | 幻觉写法 | 真实情况 |
   | --- | --- |
   | `RunWNN()` | **不存在**。做 WNN：`FindMultiModalNeighbors()` → `RunUMAP(nn.name="weighted.nn")` → `FindClusters(graph.name="wsnn")` |
   | `CoveragePlot()` | 属于 **Signac**，不在 Seurat |
   | `RunALRA()` / `RunDiffusionMap()` | 不在 Seurat |
   | `Read10X_h5()` 之外的 `ReadH5AD()` | 不存在，h5ad 走 `SeuratDisk::LoadH5Seurat()` 或 `zellkonverter` |
   | `FindVariableGenes()` | v3 旧名，**已移除**，用 `FindVariableFeatures()` |
   | `RunPCA(object, do.print=...)` | 参数早已移除，用 `ndims.print` / `nfeatures.print` |
   | `Idents(obj) <- "seurat_clusters"` 当因子 | v5 里 `Idents<-` 接受列名字符串，不要自己 `factor()` |
   | `object@assays$RNA@data` | v5 用 `LayerData(obj, layer="data")` / `GetAssayData()`，直接取 slot 会拿错层 |

3. **v5 用 layers，但 `slot=` 不是一律弃用（实测结论，别一刀切）。**
   预处理链一律用 `layer=` / `save=`：
   - `NormalizeData(layer="counts", save="data")`
   - `FindVariableFeatures(layer="data")`
   - `ScaleData(layer="data", save="scale.data")`
   - `RunPCA(layer="scale.data")`、 `RunICA`/`RunSLSI`/`RunSPCA` 同理
   - 用 `LayerData(obj, layer="data")` 取矩阵，**不要** `obj@assays$RNA@data`

   `slot=` **已被 deprecated 的 12 个函数**（用 `layer=` 替代）：
   `Assays`、`AverageExpression`、`Features`、`FetchData`、
   `FindSpatiallyVariableFeatures`、`GetAssayData`、`LayerData`、`LayerData<-`、
   `PseudobulkExpression`、`RidgePlot`、`SetAssayData`、`VlnPlot`

   `slot=` **仍然合法、照常使用的**（改成 layer 反而报错）：
   `FindMarkers`、`FindAllMarkers`、`FindConservedMarkers`、`FoldChange`、
   `DoHeatmap`、`DimHeatmap`、`FeaturePlot`、`RunUMAP`、`RunMixscape`、
   `SpatialFeaturePlot`、`SpatialPlot`、`TransferData`、`AddModuleScore`、
   `CalcPerturbSig`、`BuildClusterTree`、`PredictAssay`

   判不准就跑 `sc_lint.py`，它会按源码里的真实 `deprecated()` 标记告警。

4. **整合方式按场景分三类，别混用**

   | 场景 | 用什么 |
   | --- | --- |
   | 多样本（同模态）整合 | v5 首选：`split()` → 逐层 `NormalizeData`+`FindVariableFeatures`+`ScaleData`+`RunPCA` → `IntegrateLayers(method=CCAIntegration/RPCAIntegration/HarmonyIntegration/JointPCAIntegration)` |
   | 旧脚本 / 需要 return 整合矩阵 | `FindIntegrationAnchors()` + `IntegrateData()`（v4 API，仍保留） |
   | query → reference 映射 | `FindTransferAnchors()` + `TransferData()`，或 `MapQuery()` |
   | 有已整合参考想挂新数据（v5 Bridge） | `PrepareBridgeReference()` + `FindBridgeTransferAnchors()` + `FindBridgeIntegrationAnchors()` |
   | 百万级细胞 | `SketchData()` → 在 sketch assay 上跑 → `ProjectData()` / `TransferSketchLabels()` |

5. ** assay 必须显式。** 多 assay 时默认走 `DefaultAssay()`，
   SCT / RNA / Spatial / sketch 混用时，不写 `assay=` 是静默错误的常见来源。

6. **随机种子要固定**，否则结果不可复现：
   `RunUMAP(seed.use=42)`、`FindClusters(random.seed=0)`、
   `SCTransform(seed.use=1448145)`、`SketchData(seed=123)`、
   `FindMarkers(random.seed=1)`。

7. **绝不臆造的东西**：文件路径、样本名、基因 symbol、cluster id、
   细胞类型注释、物种（人和鼠的基因大小写不同）、测序平台。
   这些只能来自用户输入或脚本实际输出。

---

## 二、标准动作序列（先按这个走）

```
1. 明确任务类型   → tools/sc_plan.py "<一句话需求>"  给出推荐流程
2. 查真实签名     → grep -n "^## <函数名>" references/api-signatures.md
3. 写 R 脚本      → 每个任务一个独立工作目录 + 独立 .R 文件
4. 强制校验       → python3 tools/sc_lint.py <script.R> --json   （error 必须 0）
5. 环境检查       → Rscript scripts/preflight.R --json          （有 R 的机器上）
6. 执行           → Rscript scripts/run_seurat.R --script <file> --workdir <dir>
7. 读结果         → 从输出文件读数字，不靠复述
```

**第 4 步不能跳。** 没跑校验就说"脚本写好了"，等于没验证。

---

## 三、任务 → 流程路由表

| 用户要什么 | 关键函数序列（顺序不能乱） |
| --- | --- |
| 从 10x 建对象 | `Read10X()` / `Read10X_h5()` → `CreateSeuratObject(min.cells=3, min.features=200)` |
| QC 过滤 | `PercentageFeatureSet(pattern="^MT-")` → `subset(subset= nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)` |
| 标准聚类流程 | `NormalizeData` → `FindVariableFeatures` → `ScaleData` → `RunPCA` → `FindNeighbors` → `FindClusters` → `RunUMAP` |
| SCTransform 流程 | `SCTransform(vst.flavor="v2")` → `RunPCA` → `RunUMAP` → `FindNeighbors`/`FindClusters`（**不要**再 ScaleData/NormalizeData） |
| 找 marker | `FindMarkers(ident.1=, min.pct=0.25, logfc.threshold=0.25, test.use="wilcox")` 或 `FindAllMarkers(only.pos=TRUE)` |
| SCT assay 找 marker | **先** `PrepSCTFindMarkers()`，再 `FindMarkers(assay="SCT", slot="data")` |
| 细胞周期 | `CellCycleScoring(s.features=, g2m.features=)` → `ScaleData(vars.to.regress=c("S.Score","G2M.Score"))` |
| 模块评分 | `AddModuleScore(features=list(...), name="...")` |
| 多样本整合 | `split(f="orig.ident")` → 每层预处理 → `IntegrateLayers(method=RPCAIntegration)` → `JoinLayers()` |
| 参考注释映射 | `FindTransferAnchors(reference, query)` → `TransferData()` → 或 `MapQuery()` |
| 拟 bulk / 差异 | `AggregateExpression(group.by=...)` / `PseudobulkExpression()` |
| 空间转录组 | `Load10X_Spatial()` → `SCTransform(assay="Spatial")` → `FindSpatiallyVariableFeatures()` / `RunMoransI()` → `SpatialFeaturePlot()` |
| Visium HD / 单细胞级空间 | `Load10X_Spatial(bin.size=)` / `Read10X_HD_GeoJson()` |
| 百万细胞 | `SketchData(ncells=)` → 切到 `sketch` assay → 标准流程 → `ProjectData()` / `TransferSketchLabels()` |
| Mixscape 扰动 | `CalcPerturbSig()` → `RunMixscape()` → `MixscapeHeatmap()` / `PlotPerturbScore()` |
| WNN 多模态 | `FindMultiModalNeighbors(reduction.list=, dims.list=)` → `RunUMAP(nn.name="weighted.nn")` → `FindClusters(graph.name="wsnn")` |
| 去双细胞 | 用 `scDblFinder`/`DoubletFinder`（第三方），Seurat 本体不提供 |
| 保存/读取 | `SaveSeuratRds()` / `LoadSeuratRds()`；跨 h5 用 SeuratDisk |

细节代码模板见 `references/workflows.md`。

---

## 四、常用函数签名速查（从源码提取的真实 formals）

```r
CreateSeuratObject(counts, assay="RNA", names.field=1, names.delim="_",
                   meta.data=NULL, project="SeuratProject", min.cells=0, min.features=0)
Read10X(data.dir, gene.column=2, cell.column=1, unique.features=TRUE, strip.suffix=FALSE)
PercentageFeatureSet(object, pattern=NULL, features=NULL, col.name=NULL, assay=NULL)
subset(x, subset, cells, features, idents, layers=NULL, ...)

NormalizeData(object, normalization.method=c("LogNormalize","CLR","RC"),
              scale.factor=1e4, margin=1, assay=NULL, layer="counts", save="data", verbose=TRUE)
FindVariableFeatures(object, selection.method="vst", nfeatures=2000, assay=NULL, layer=NULL)
ScaleData(object, features=NULL, vars.to.regress=NULL, latent.data=NULL, split.by=NULL,
          model.use="linear", do.scale=TRUE, do.center=TRUE, scale.max=10,
          assay=NULL, layer="data", save="scale.data")
SCTransform(object, assay="RNA", new.assay.name="SCT", vst.flavor="v2",
            variable.features.n=3000, ncells=5000, seed.use=1448145, conserve.memory=FALSE)

RunPCA(object, assay=NULL, npcs=50, features=NULL, layer="scale.data",
       reduction.name="pca", approx=TRUE, seed.use=42, verbose=TRUE)
RunUMAP(object, dims=1:30, reduction="pca", n.neighbors=30, min.dist=0.3,
        metric="cosine", umap.method="uwot", seed.use=42, reduction.name="umap")
RunTSNE(object, dims=1:30, reduction="pca", perplexity=30, ...)
FindNeighbors(object, reduction="pca", dims=1:10, k.param=20,
              nn.method="annoy", prune.SNN=1/15, compute.SNN=TRUE, assay=NULL)
FindClusters(object, resolution=0.8, algorithm=1, random.seed=0,
             n.start=10, n.iter=10, group.singletons=TRUE, graph.name=NULL)

FindMarkers(object, ident.1=NULL, ident.2=NULL, group.by=NULL, features=NULL,
            logfc.threshold=0.1, test.use="wilcox", min.pct=0.01, only.pos=FALSE,
            slot="data", assay=NULL, random.seed=1, latent.vars=NULL)
FindAllMarkers(object, assay=NULL, logfc.threshold=0.1, test.use="wilcox",
               min.pct=0.01, only.pos=FALSE, return.thresh=1e-2, random.seed=1)
PrepSCTFindMarkers(object, assay="SCT", verbose=TRUE)

CellCycleScoring(object, s.features, g2m.features, ctrl=NULL, set.ident=FALSE)
AddModuleScore(object, features, pool=NULL, nbin=24, ctrl=100, assay=NULL, name="Cluster")
AggregateExpression(object, assays=NULL, group.by="ident", return.seurat=FALSE,
                    normalization.method="LogNormalize", scale.factor=10000)

IntegrateLayers(object, method, orig.reduction="pca", assay=NULL,
                features=NULL, layers=NULL, scale.layer="scale.data")
FindIntegrationAnchors(object, assay=NULL, anchor.features=2000,
                       normalization.method="LogNormalize", reduction="cca", dims=1:30, k.anchor=5)
IntegrateData(anchorset, dims=1:30, normalization.method="LogNormalize", new.assay.name="integrated")
FindTransferAnchors(reference, query, dims=1:30, normalization.method="LogNormalize",
                    reference.reduction=NULL, reduction="pcaproject", npcs=30, k.anchor=5)
TransferData(anchorset, refdata, weight.reduction=NULL, dims=1:30, k.weight=50)

SketchData(object, assay=NULL, ncells=5000, sketched.assay="sketch",
           method=c("LeverageScore","Uniform","Gibbs"), seed=123)
ProjectData(object, sketched.assay="sketch", assay="RNA", full.reduction="pca",
            sketched.reduction="pca", refdata=NULL, verbose=TRUE)

Load10X_Spatial(data.dir, filename="filtered_feature_bc_matrix.h5", assay="Spatial",
                slice="slice1", bin.size=NULL, image=NULL, to.upper=FALSE)
FindSpatiallyVariableFeatures(object, assay=NULL, selection.method="moransi",
                              nfeatures=2000, ...)

DimPlot(object, dims=c(1,2), reduction=NULL, group.by=NULL, split.by=NULL,
        label=FALSE, repel=FALSE, raster=NULL, ncol=NULL)
FeaturePlot(object, features, dims=c(1,2), reduction=NULL, slot="data", min.cutoff=NA,
            max.cutoff=NA, blend=FALSE, raster=NULL)
VlnPlot(object, features, group.by=NULL, split.by=NULL, slot=NULL, layer=NULL,
        pt.size=NULL, stack=FALSE, combine=TRUE)
DotPlot(object, features, group.by=NULL, cols=c("lightgrey","blue"), dot.scale=6)
DoHeatmap(object, features=NULL, group.by="ident", slot="scale.data", raster=TRUE)
SpatialFeaturePlot(object, features, ...)
```

**完整 406 个符号的签名库在 `references/api-signatures.md`**，
用 `grep -n "^## <函数名>"` 精确查，不要整篇读。

---

## 五、工具

| 工具 | 干什么 | 依赖 R 吗 |
| --- | --- | --- |
| `tools/sc_lint.py` | **核心**。静态校验 R 脚本：函数名是否存在（含大小写/拼写纠错建议）、参数名是否合法（`...` 透传能识别 `method=RPCAIntegration`）、deprecated 参数告警、括号与引号配对、中文全角符号、SCT 缺 prep | 否 |
| `tools/sc_api.py` | 查函数签名/模块归属，支持模糊搜索 | 否 |
| `tools/sc_plan.py` | 一句话需求 → 推荐流程与函数序列 | 否 |
| `scripts/preflight.R` | 检查 R / Seurat / SeuratObject 版本与常用依赖，输出 JSON | 是 |
| `scripts/run_seurat.R` | 统一执行入口：独立工作目录 + 日志重定向 + 错误捕获 | 是 |

用法：

```bash
# 校验（必做）
python3 tools/sc_lint.py my_analysis.R --json

# 查签名
python3 tools/sc_api.py FindMarkers
python3 tools/sc_api.py --search integration

# 规划流程
python3 tools/sc_plan.py "两个样本的 PBMC 数据整合后找差异基因"

# 环境（需要 R）
Rscript scripts/preflight.R --json

# 执行（需要 R）
Rscript scripts/run_seurat.R --script my_analysis.R --workdir runs/pbmc01
```

> 注意：被包装脚本内 `commandArgs()` 拿到的是 run_seurat.R 自己的参数，
> 给分析脚本传参请用环境变量（见 `references/pitfalls.md` 参数陷阱 9）。

`sc_lint.py` 的退出码：0 = 无 error；1 = 有 error；2 = 用法错误。
warning 不阻断（例如 deprecated 参数），但要在回复里说明。

---

## 六、失败协议（按症状查）

| 症状 | 真实原因 | 处置 |
| --- | --- | --- |
| `could not find function "xxx"` | 函数不存在或包名写错 | 查 whitelist；注意 SeuratObject 的函数不需要前缀 |
| `unused argument (...)` | 参数名幻觉 | `sc_api.py` 查真实参数名 |
| `object 'integrated' not found` | 用了 v4 的 IntegrateData 但没跑，或 v5 流程没 JoinLayers | 按整合三选一重走 |
| `Error in LayerData: layer 'data' not found` | 还没 NormalizeData，或层名写错 | 先跑 NormalizeData(save="data") |
| FindMarkers 报 `assay SCT` 相关错 | 没跑 `PrepSCTFindMarkers()` | SCT 找 marker 前必须先 prep |
| UMAP 每次不一样 | 没设 seed | `RunUMAP(seed.use=42)` |
| 内存爆 / 太慢 | 矩阵太大 | `ScaleData` 后 `RunPCA(approx=TRUE)`；百万细胞走 `SketchData()`；或 `conserve.memory=TRUE` |
| 整合后 cluster 全是样本特异 | 用了 IntegrateData 但下游没切 assay | v4：分析前 `DefaultAssay(obj) <- "integrated"`；v5：用 IntegrateLayers + JoinLayers |
| `non-conformable arguments` in RunPCA | features 数与 scale.data 不符 / 有 NA | 检查 ScaleData 是否成功、是否指定了错误 layer |
| 中文路径 / 空格路径报错 | R 在 Windows 上对编码敏感 | 工作目录用纯 ASCII 路径 |
| 基因名全部找不到 | 物种搞错（人大写 / 鼠首字母大写其余小写） | 向用户确认物种，别猜 |

更多坑见 `references/pitfalls.md`。

---

## 七、本机环境边界（诚实说明）

每次任务先运行 `Rscript scripts/preflight.R --json` 检查当前环境；不要沿用技能作者机器的历史状态。如果当前机器没有可用 R：

- 本技能在本机可以完整做到：**选函数、写代码、校验脚本、规划流程、解读报错**；
- 本技能在本机**做不到**：真实跑 `Rscript` 出图出数。
- 需要真跑时，给用户三选一，说清楚代价：
  1. 本机装 R（≥4.0）+ `install.packages("Seurat")`（Seurat v5 依赖多，装一次约 10–30 分钟）；
  2. 交付脚本交给 Linux 服务器 / HPC / Colab；
  3. GitHub Actions（`r-lib/actions/setup-r` + 缓存 `renv`）。

**不要假装跑过、不要编造任何数值结果。** 没跑就是没跑。

---

## 八、参考文件

- `references/api-signatures.md` —— 406 个真实符号的完整签名（grep 用）
- `references/function-index.md` —— 按模块 / S3 method / S4 类分类的索引
- `references/workflows.md` —— 可直接改用的流程模板（QC、SCT、整合、映射、空间、WNN、Mixscape、Sketch）
- `references/pitfalls.md` —— v4→v5 迁移坑、参数陷阱、性能与内存
- `references/environment.md` —— 安装、版本对齐、离线与 HPC 场景

---

## 九、宿主兼容性（Claude Code / WorkBuddy / 其它 Agent）

本技能只依赖三样东西：**Bash（跑 python3）+ Read + Grep**。
不联网、不依赖 MCP、不依赖任何宿主专有能力，因此任何支持「目录型 skill」
的 Agent 宿主都能用。

| 宿主 | 安装位置 | 安装命令 |
|---|---|---|
| Claude Code（用户级） | `~/.claude/skills/seurat-sc/` | `python3 install.py` |
| Claude Code（项目级） | `<项目>/.claude/skills/seurat-sc/` | `python3 install.py --project` |
| WorkBuddy | `~/.workbuddy/skills/seurat-sc/` | `python3 install.py --host workbuddy` |
| 其它宿主 | 自定义 | `python3 install.py --dir <skills 根目录>` |

约定（改动本技能时必须遵守，否则会破坏兼容性）：

1. 所有路径一律**相对 skill 根目录**写：`tools/sc_lint.py`、`references/workflows.md`。
   不写任何绝对路径 —— 换机器、换用户、换宿主都不用改。
2. 命令统一写 `python3`；Windows 上若没有 `python3`，把它换成 `python`。
3. SKILL.md 是唯一常驻入口。`references/*.md` 按需 grep 读取，不要整篇加载
   （`api-signatures.md` 有 86 KB，整读既慢又挤占上下文）。
4. 改动技能后必须跑 `python3 tools/selftest.py`（fixtures 回归 + 文档代码块 + 工具冒烟 + 数据完整性 + 包完整性五类检查，全绿才能提交）；
   交付 R 代码前必须跑 `python3 tools/sc_lint.py <脚本>`（error 必须为 0）。
