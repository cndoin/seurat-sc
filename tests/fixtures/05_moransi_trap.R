library(Seurat)
# RunMoransI 的真实签名是 RunMoransI(data, pos, verbose=TRUE)，没有 features 参数。
# 这个用例用于锁死"AI 凭印象补 features="这类幻觉必须被抓出来。
sp <- RunMoransI(sp, features = VariableFeatures(sp))
