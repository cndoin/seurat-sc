#!/usr/bin/env Rscript
# preflight.R —— Seurat 运行环境预检，输出 JSON
#
# 用法：
#   Rscript scripts/preflight.R            # 人读
#   Rscript scripts/preflight.R --json     # stdout 只有一个 JSON
#
# stdout 只放数据；人类提示走 stderr。
# 任何 required=TRUE 且 installed=FALSE 的项，都不要带着缺口往下跑。

args <- commandArgs(trailingOnly = TRUE)
json_only <- "--json" %in% args

esc <- function(s) {
  s <- gsub("\\\\", "\\\\\\\\", s)
  s <- gsub('"', '\\\\"', s)
  s
}
jq <- function(s) paste0('"', esc(as.character(s)), '"')

# ---------- 探测 ----------
rver <- paste(R.version$major, R.version$minor, sep = ".")
rnum <- as.numeric(paste(R.version$major,
                         strsplit(R.version$minor, "\\.")[[1]][1], sep = "."))

pkg_info <- function(p) {
  v <- tryCatch(as.character(packageVersion(p)), error = function(e) NULL)
  list(name = p, installed = !is.null(v), version = if (is.null(v)) NA else v)
}

# 包来源映射：conda / cran / bioc / github
# 用途：缺包时给出精确安装命令，不靠猜。
# conda-forge 全是预编译二进制，Windows 上绕开编译地狱，所以优先标 conda。
PKG_SRC <- c(
  Seurat = "conda", SeuratObject = "conda", sctransform = "conda",
  ggplot2 = "conda", patchwork = "conda", Matrix = "conda", irlba = "conda",
  uwot = "conda", Rtsne = "conda", igraph = "conda", RcppAnnoy = "conda",
  RcppHNSW = "conda", leidenbase = "conda", harmony = "conda",
  BPCells = "cran", enrichR = "cran", jsonlite = "conda",
  future = "conda", future.apply = "conda", data.table = "conda",
  hdf5r = "conda", arrow = "conda",
  DESeq2 = "bioc", MAST = "bioc", limma = "bioc", glmGamPoi = "bioc",
  SingleCellExperiment = "bioc", scDblFinder = "bioc",
  presto = "github", Signac = "github", SeuratDisk = "github", Azimuth = "github"
)

# GitHub 仓库映射（只列本技能会用到的，不瞎猜）
PKG_GH <- c(
  presto = "immunogenomics/presto",
  Signac = "stuart-lab/signac",
  SeuratDisk = "mojaveazure/seurat-disk",
  Azimuth = "satijalab/azimuth"
)

# 给出该包的安装命令
install_hint <- function(pkg) {
  src <- PKG_SRC[[pkg]]
  if (is.null(src) || is.na(src)) src <- "cran"
  if (src == "conda") {
    paste0("micromamba install -y -c conda-forge r-", tolower(pkg))
  } else if (src == "bioc") {
    paste0("BiocManager::install('", pkg, "')")
  } else if (src == "github") {
    gh <- PKG_GH[[pkg]]
    if (is.null(gh)) gh <- paste0("UNKNOWN/", tolower(pkg))
    paste0("remotes::install_github('", gh, "')")
  } else {
    paste0("install.packages('", pkg, "')")
  }
}

core <- c("Seurat", "SeuratObject")
# required=FALSE 的是"用到才需要"的可选依赖
optional <- c(
  "sctransform", "ggplot2", "patchwork", "Matrix", "irlba", "uwot", "Rtsne",
  "igraph", "RcppAnnoy", "RcppHNSW", "leidenbase", "harmony", "BPCells",
  "presto", "future", "future.apply", "data.table", "hdf5r", "arrow",
  "DESeq2", "MAST", "limma", "glmGamPoi", "SingleCellExperiment",
  "Signac", "SeuratDisk", "Azimuth", "scDblFinder", "enrichR", "jsonlite"
)

items <- list()
for (p in core) {
  info <- pkg_info(p)
  info$required <- TRUE
  items[[length(items) + 1]] <- info
}
for (p in optional) {
  info <- pkg_info(p)
  info$required <- FALSE
  items[[length(items) + 1]] <- info
}

# ---------- 系统与资源 ----------
cores <- tryCatch(parallel::detectCores(all.tests = FALSE, logical = TRUE),
                  error = function(e) NA)
mem_gb <- tryCatch({
  if (Sys.info()[["sysname"]] == "Windows") {
    as.numeric(memory.limit()) / 1024
  } else if (file.exists("/proc/meminfo")) {
    l <- readLines("/proc/meminfo", n = 1, warn = FALSE)
    as.numeric(strsplit(l, "\\s+")[[1]][3]) / 1024 / 1024
  } else NA
}, error = function(e) NA)

wd <- getwd()
wd_writable <- tryCatch({
  tf <- file.path(wd, ".sc_preflight_write_test")
  writeLines("ok", tf); unlink(tf); TRUE
}, error = function(e) FALSE)

# ---------- 判定 ----------
hard_fail <- c()
if (isTRUE(rnum < 4.0)) hard_fail <- c(hard_fail, "R 版本 < 4.0，Seurat 5 要求 R >= 4.0")
seurat_ok <- FALSE
for (it in items) {
  if (it$name == "Seurat" && it$installed) {
    seurat_ok <- TRUE
    sv <- it$version
    parts <- as.numeric(strsplit(sv, "\\.")[[1]])
    if (length(parts) && parts[1] < 5) {
      hard_fail <- c(hard_fail, paste0("Seurat 版本为 ", sv, "，本技能面向 v5，v4 的差异很大"))
    }
  }
}
if (!seurat_ok) hard_fail <- c(hard_fail, "未安装 Seurat：install.packages('Seurat')")
if (!wd_writable) hard_fail <- c(hard_fail, paste0("工作目录不可写：", wd))

# ---------- 输出 ----------
pkg_json <- paste(vapply(items, function(it) {
  hint <- if (isTRUE(it$installed)) "null" else jq(install_hint(it$name))
  sprintf('{"name":%s,"required":%s,"installed":%s,"version":%s,"install_hint":%s}',
          jq(it$name),
          if (isTRUE(it$required)) "true" else "false",
          if (isTRUE(it$installed)) "true" else "false",
          if (is.na(it$version)) "null" else jq(it$version),
          hint)
}, character(1)), collapse = ",\n    ")

issues_json <- paste(vapply(hard_fail, jq, character(1)), collapse = ",")

json <- sprintf('{
  "ok": %s,
  "r": {"version": %s, "ok": %s},
  "seurat": {"installed": %s},
  "workdir": {"path": %s, "writable": %s},
  "system": {"cores": %s, "mem_gb": %s, "os": %s},
  "packages": [
    %s
  ],
  "issues": [%s]
}',
  if (length(hard_fail)) "false" else "true",
  jq(rver), if (isTRUE(rnum >= 4.0)) "true" else "false",
  if (seurat_ok) "true" else "false",
  jq(wd), if (wd_writable) "true" else "false",
  if (is.na(cores)) "null" else format(cores),
  if (is.na(mem_gb)) "null" else format(round(mem_gb, 1)),
  jq(Sys.info()[["sysname"]]),
  pkg_json, issues_json)

if (json_only) {
  cat(json, "\n")
} else {
  cat("Seurat 环境预检\n", file = stderr())
  cat(sprintf("  R        : %s %s\n", rver,
              if (isTRUE(rnum >= 4.0)) "(ok)" else "(版本过低)"), file = stderr())
  cat(sprintf("  Seurat   : %s\n",
              if (seurat_ok) {
                v <- items[[which(vapply(items, function(x) x$name, "") == "Seurat")]]$version
                v
              } else "未安装"), file = stderr())
  cat(sprintf("  SeuratObj: %s\n",
              if (any(vapply(items, function(x) x$name == "SeuratObject" && x$installed, TRUE)))
                items[[which(vapply(items, function(x) x$name, "") == "SeuratObject")]]$version
              else "未安装"), file = stderr())
  miss <- Filter(function(x) x$required && !x$installed, items)
  opt_miss <- Filter(function(x) !x$required && !x$installed, items)
  if (length(miss)) {
    cat("  缺失必需包: ", paste(vapply(miss, function(x) x$name, ""), collapse = ", "),
        "\n", file = stderr())
  }
  cat("  缺失可选包: ", paste(vapply(opt_miss, function(x) x$name, ""), collapse = ", "),
      "\n", file = stderr())
  # 缺包时给出可直接复制的安装命令，按包来源区分
  all_miss <- c(miss, opt_miss)
  if (length(all_miss)) {
    cat("\n  --- 安装命令（按来源，可直接复制）---\n", file = stderr())
    for (it in all_miss) {
      cat(sprintf("    %s      # %s\n", install_hint(it$name),
                  if (isTRUE(it$required)) "必需" else "可选"), file = stderr())
    }
    cat("  提示：优先用 conda-forge 预编译包，Windows 上免编译。\n", file = stderr())
  }
  cat(sprintf("  资源      : %s 核 / %s GB / %s\n", cores, round(mem_gb, 1),
              Sys.info()[["sysname"]]), file = stderr())
  cat("\n", file = stderr())
  cat("--- JSON ---\n")
  cat(json, "\n")
}

quit(status = if (length(hard_fail)) 1L else 0L, save = "no")
