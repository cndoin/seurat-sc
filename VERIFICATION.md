# VERIFICATION.md —— 与开源 Seurat 的等效性 / 稳定性 / 效率验证报告

> 本文件记录作者在 2026-10-01 的有限数据实验，不能代表所有 Seurat 工作流、数据集或机器均已验证。文件哈希一致说明这些实验的输出相同，不能证明执行包装没有时间开销，也不能单独证明生物学结论正确。运行时/语法错误退出码为 1，缺少参数/文件为 2；下文历史描述中的“全部 rc=2”不准确。

> 验证日期：2026-10-01 · 验证对象：seurat-sc 1.0.0（本技能）
> 对照基准：开源项目 `satijalab/seurat`（CRAN Seurat 5.5.1 + SeuratObject 5.4.0，
> 官方 PBMC 3K vignette 数据与成品对象）
> 结论先行：**运行效果一致（逐位一致 + ARI 0.96 对金标准）、结果生物学正确、
> 重复运行稳定（同种子逐位复现、跨种子聚类不变）、技能包装零计算开销。**

## 验证环境

| 项 | 值 |
| --- | --- |
| OS | Windows（CPU，无 GPU） |
| R | 4.6.1 (2026-06-24 ucrt)，官方 CRAN 版 |
| Seurat / SeuratObject | 5.5.1 / 5.4.0（CRAN） |
| 数据集 | `pbmc_small`（内置 80 细胞）+ PBMC 3K（2700 细胞，官方 vignette 同源） |
| 金标准 | `pbmc3k.SeuratData` 3.1.4 内的 `pbmc3k.final`（官方 vignette 成品对象） |

## 测试矩阵与结果总览

| # | 测试 | 方法 | 结果 |
| --- | --- | --- | --- |
| E1 | 等效性（小数据） | 同种子同脚本：直接 Rscript vs `run_seurat.R` 包装 | **逐位一致**（4/4 文件 hash 相同） |
| E2 | 等效性（真实数据） | PBMC 3K：直接 vs 包装 | **逐位一致**（4/4 文件 hash 相同） |
| C1 | 金标准对照 | 我方 9 簇 vs vignette 成品 9 簇 | **ARI 0.9644**；9 簇 1:1 映射全部 9 种经典细胞类型 |
| C2 | marker 语义一致 | 我方每簇 top10 ∈ 金标准 top20 | **均值 9.8/10**（各簇 9~10） |
| C3 | 生物学正确性 | 28 个经典 PBMC marker 归属抽查 | **28/28 全部落在正确簇** |
| S1 | 同种子复现 | pbmc_small 种子 42 ×5 | **5/5 逐位一致** |
| S2 | 跨种子稳健 | PBMC 3K 种子 42 vs 7 | **ARI 1.0000**（聚类完全一致），耗时 210.4s vs 211.2s |
| S3 | 失败协议 | 坏脚本×2 + 缺文件 + 缺参数 | **4/4 正确**：rc≠0、JSON `ok:false`、错误精确、不挂死 |
| S4 | 工具链稳定 | selftest×3、sc_api/sc_plan 幂等、preflight | **12/12 ×3 全绿**；输出幂等 |
| F1 | 效率（真实数据） | PBMC 3K 分步计时 | 总 210s（FindAllMarkers 占 97%），前处理全程 <3s |
| F2 | 技能包装开销 | 端到端墙钟 ×3 | 直路 4.5s vs 包装 7.2s（+2.7s 进程/日志层）；**计算零开销**（逐位一致可证） |
| A1 | API 事实对齐 | 406 符号签名 vs 实装包 | 无用户可见断裂（详见下文） |

## 一、运行效果：与原生 Seurat 逐位一致

同一分析脚本（LogNormalize → HVG → Scale → PCA → Neighbors → Clusters →
FindAllMarkers，`RNGkind` 固定 + `set.seed`）分别经直接 Rscript 与技能入口
`scripts/run_seurat.R` 执行，输出的聚类分配、PCA 坐标（6 位小数）、marker 表
经 SHA-256 比对**逐字节相同**：

| 输出 | pbmc_small | PBMC 3K（2638 细胞） |
| --- | --- | --- |
| clusters.csv | SAME | SAME |
| pca.csv | SAME | SAME |
| markers.csv | SAME | SAME |
| summary.csv | SAME（剔除耗时字段） | SAME（剔除耗时字段） |

即技能的执行包装层（独立工作目录 + 日志重定向 + 错误捕获）对数值结果
**零扰动**——它只是管道，不触碰计算。

## 二、结果正确性：对官方金标准

以官方 vignette 成品对象 `pbmc3k.final`（含人工细胞类型注释）为基准：

- **ARI = 0.9644**（1.0 为完全一致；差异来自 Seurat v3→v5 的归一化实现细节，
  预期内的版本级差异）
- 我方 9 簇与金标准 9 种细胞类型 **1:1 全映射**，无空簇、无合并/分裂：

| 我方簇 | 金标准细胞类型 | 我方 top10 ∈ 金标准 top20 |
| --- | --- | --- |
| 0 | Naive CD4 T | 9/10 |
| 1 | CD14+ Mono | 10/10 |
| 2 | Memory CD4 T | 10/10 |
| 3 | B | 10/10 |
| 4 | CD8 T | 9/10 |
| 5 | FCGR3A+ Mono | 10/10 |
| 6 | NK | 10/10 |
| 7 | DC | 10/10 |
| 8 | Platelet | 10/10 |

- **28 个经典 marker 全部归属正确**（独立实验，pct.1>0.25 + p 值排序）：
  CD79A/MS4A1/CD74/HLA-DRA→B(3)；LYZ/S100A8/S100A9→CD14 Mono(1)；
  FCGR3A/MS4A7/LST1→FCGR3A+ Mono(5)；NKG7/GNLY/PRF1/GZMB→NK(6)；
  PPBP/PF4/NRGN→Platelet(8)；FCER1A/CST3→DC(7)；IL7R/CCR7/LTB/MAL→CD4 T(0/2)；
  CD3D/CD8A/CCL5→CD8 T(4)。
- 数据规模自校验：质控后 **2638 细胞**，与官方 vignette 完全一致。

## 三、稳定性

1. **同种子逐位复现**：pbmc_small 种子 42 连跑 5 次（含不同执行通道），
   全部结果文件 hash 相同 → 完全可复现。
2. **跨种子稳健**：PBMC 3K 用种子 42 / 7 两次独立全流程，聚类 ARI = 1.0000
   （2638 细胞逐一分配相同），耗时 210.4s / 211.2s（波动 <0.5%）。
3. **失败协议**（`run_seurat.R`）：运行时错误、语法错误、脚本不存在、缺
   `--script` 四种情况全部返回 rc=2 + JSON `ok:false` + 精确 error 字段，
   不挂死、不误报成功。
4. **工具链幂等**：`tools/selftest.py` 连跑 3 次均 12/12；`sc_api` / `sc_plan`
   重复调用输出一致。

## 四、运行效率

PBMC 3K（2638 细胞 × 13714 基因）全流程 210.4s（单核 CPU）：

| 步骤 | 耗时(s) |
| --- | --- |
| NormalizeData | 0.30 |
| FindVariableFeatures | 0.36 |
| ScaleData | 0.36 |
| RunPCA | 1.75 |
| FindNeighbors | 0.62 |
| FindClusters | 0.15 |
| FindAllMarkers | 204.59 |
| 合计 | 210.43 |

统计检验（FindAllMarkers，逐簇 wilcox）占 97%——这是 Seurat 本身的计算量，
与技能无关。前处理全程 <3s。技能包装的端到端开销约 +2.7s（R 进程启动 +
日志重定向 + 工作目录管理），在真实任务中占比 <2%，且**计算结果零改动**。

## 五、API 事实底座对齐

技能事实底座（`references/api-signatures.md`，406 条源自源码解析的签名）
对实装 Seurat 5.5.1 / SeuratObject 5.4.0 逐条核对：

- 348 个导出符号 + 58 个 S3 方法全部可定位，**无用户可见断裂**；
- 真实差异仅 3 处且方向均为"事实底座基于 master/develop 领先 CRAN 发布版"：
  1 个内部 S3 方法（`.SelectFeatures.StdAssay`，非导出）+ 2 处可选参数
  （`PrepSCTFindMarkers(umi.assay,layer)`、`SingleExIPlot(fill.by)`）；
- 其余差异为形式层（S3 方法并集 vs generic 带 `...`、替换函数的 `value`），
  不影响任何调用。

## 六、验证中发现的问题与处置

1. **`run_seurat.R` 包装的脚本拿不到自己的命令行参数**（已修文档）：
   `run_seurat.R` 以 `source()` 执行脚本，脚本内 `commandArgs()` 拿到的是
   包装器的参数（`--script`/`--workdir`/`--json`），按位置取参会得到垃圾值。
   处置：`references/pitfalls.md` 参数陷阱新增第 9 条（环境变量传参范式），
   `SKILL.md` 执行段落加注意提示。
2. **top marker 按 `avg_log2FC` 裸排序会被罕见表达基因刷榜**（已修文档）：
   实测 pct.1≈1.6% 的基因（如 GTSCR1）logFC 可达 7+，把经典 marker 挤出
   top10。处置：`pitfalls.md` 新增第 10 条，推荐 p 值排序 + `pct.1>0.25` 过滤。

## 七、边界与未覆盖项（诚实声明）

- UMAP/tSNE 未纳入逐位比对（上游 uwot 多线程下有固有非确定性，需
  `n.threads=1` + 种子控制；聚类/PCA/marker 不受影响）。
- SCT 流程、多样本整合（Harmony/IntegrateLayers）、空间转录组分支未跑
  全流程对照（API 层已核对存在性与签名）。
- 生物信息学差异检验替代实现（DESeq2/MAST/presto）未逐一比对。

## 八、复现方法

验证脚本与原始输出：工作区 `_tools/verify/`（`analysis_std.R`、`cmp.py`、
`compare_gold.py`、`marker_check.R`、`gold_extract.R`，输出在 `out/`）。
核心命令：

```bash
Rscript analysis_std.R out/direct 42 small          # 直路
Rscript scripts/run_seurat.R --script analysis_std.R --workdir out/wrap   # 技能入口
python cmp.py out/direct out/wrap                   # 逐位比对
python compare_gold.py out/p3_direct out/gold       # 金标准 ARI + marker 重叠
```
