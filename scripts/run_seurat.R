#!/usr/bin/env Rscript
# run_seurat.R —— 统一执行入口：独立工作目录 + 日志重定向 + 结构化结果
#
# 用法：
#   Rscript scripts/run_seurat.R --script analysis.R --workdir runs/pbmc01
#   Rscript scripts/run_seurat.R --script analysis.R --workdir runs/pbmc01 --json
#
# 做了三件事：
#   1. chdir 到独立工作目录（Seurat 的中间产物写在 CWD，两个任务不能共用）
#   2. 把脚本的所有输出收进 <workdir>/run.log，stdout 保持干净
#   3. tryCatch 捕获错误，退出码 + JSON 都能反映真实成败
#
# 注意：退出码 0 只代表"脚本没抛错"。Seurat 有些路径会静默少算东西，
# 判成败还要看脚本自己写出的结果文件。

args <- commandArgs(trailingOnly = TRUE)

get_arg <- function(flag, default = NULL) {
  i <- match(flag, args)
  if (is.na(i) || i == length(args) + 1) return(default)
  v <- args[i + 1]
  if (is.na(v) || grepl("^--", v)) return(default)
  v
}

script <- get_arg("--script")
workdir <- get_arg("--workdir", ".")
json_only <- "--json" %in% args

if (is.null(script)) {
  cat('{"ok":false,"error":"missing --script"}\n')
  quit(status = 2L, save = "no")
}
if (!file.exists(script)) {
  cat('{"ok":false,"error":"script not found"}\n')
  quit(status = 2L, save = "no")
}
script <- normalizePath(script, winslash = "/", mustWork = TRUE)

if (!dir.exists(workdir)) dir.create(workdir, recursive = TRUE, showWarnings = FALSE)
workdir <- normalizePath(workdir, winslash = "/", mustWork = TRUE)

esc <- function(s) {
  s <- gsub("\\\\", "\\\\\\\\", s)
  s <- gsub('"', '\\\\"', s)
  s
}
jq <- function(s) paste0('"', esc(as.character(s)), '"')

logfile <- file.path(workdir, "run.log")
old <- setwd(workdir)

# ---------- 执行，输出全部进日志 ----------
con <- file(logfile, open = "wt")
sink(con, type = "output")
sink(con, type = "message")

t0 <- Sys.time()
status <- "ok"
errmsg <- NA_character_
warncount <- 0L
wcollect <- character(0)

w_handler <- function(w) {
  warncount <<- warncount + 1L
  if (length(wcollect) < 20) wcollect[[length(wcollect) + 1]] <<- conditionMessage(w)
  invokeRestart("muffleWarning")
}

res <- withCallingHandlers(
  tryCatch({
    source(script, echo = FALSE, local = FALSE)
    "ok"
  }, error = function(e) {
    errmsg <<- conditionMessage(e)
    "error"
  }),
  warning = w_handler
)

elapsed <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
sink(type = "message")
sink(type = "output")
close(con)
setwd(old)

# ---------- 结果 ----------
ok <- identical(res, "ok")
warn_json <- paste(vapply(wcollect, jq, character(1)), collapse = ",")

json <- sprintf('{
  "ok": %s,
  "script": %s,
  "workdir": %s,
  "log": %s,
  "elapsed_sec": %s,
  "warnings": %s,
  "warning_count": %d,
  "error": %s
}',
  if (ok) "true" else "false",
  jq(script), jq(workdir), jq(logfile),
  format(round(elapsed, 1)),
  warn_json, warncount,
  if (is.na(errmsg)) "null" else jq(errmsg))

if (json_only) {
  cat(json, "\n")
} else {
  cat("run_seurat\n", file = stderr())
  cat(sprintf("  script : %s\n", script), file = stderr())
  cat(sprintf("  workdir: %s\n", workdir), file = stderr())
  cat(sprintf("  log    : %s\n", logfile), file = stderr())
  cat(sprintf("  time   : %.1f s\n", elapsed), file = stderr())
  cat(sprintf("  result : %s\n", if (ok) "OK" else paste("FAILED:", errmsg)), file = stderr())
  if (warncount) cat(sprintf("  warn   : %d 条\n", warncount), file = stderr())
  cat("\n--- JSON ---\n")
  cat(json, "\n")
}

quit(status = if (ok) 0L else 1L, save = "no")
