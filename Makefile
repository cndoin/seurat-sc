# seurat-sc 的常用命令别名。
#
# 这里只放命令别名，不放真逻辑 —— 逻辑都在 tools/*.py 里。
# 这样 Windows 用户不装 make 也能照着手敲。
#
# Windows 原生没有 make。等价手敲命令（PowerShell / cmd 把 python3 换成 python）：
#   make check   ->  python3 tools/selftest.py
#   make lint    ->  python3 tools/sc_lint.py scripts/run_seurat.R --json
#   make rebuild ->  python3 tools/etl/rebuild.py && python3 tools/selftest.py
#   make pack    ->  python3 tools/pack.py
#   make clean   ->  python3 -c "import shutil;[shutil.rmtree(p,ignore_errors=True) for p in ['.build','tools/__pycache__','tools/etl/__pycache__']]"

PY ?= python3

.PHONY: help check test lint api plan rebuild pack clean

help:
	@echo "make check    跑全套门禁（自检，退出码 0 才算过）—— 提交前必须跑"
	@echo "make test     同 check"
	@echo "make lint     校验 scripts/ 下的 R 脚本本身也干净（dogfood）"
	@echo "make api      查真实函数签名，例：make api FN=FindMarkers"
	@echo "make plan     一句话规划流程，例：make plan Q=\"两个样本整合后找差异基因\""
	@echo "make rebuild  重建事实底座（唯一联网步骤，会抓上游源码）"
	@echo "make pack     打包 zip + tar.gz 到 ../dist/，并刷新 MANIFEST.md"
	@echo "make clean    清掉构建产物（.build / __pycache__）"

check:
	$(PY) tools/selftest.py

test: check

lint:
	$(PY) tools/sc_lint.py scripts/preflight.R --json
	$(PY) tools/sc_lint.py scripts/run_seurat.R --json

api:
	@test -n "$(FN)" || { echo "用法：make api FN=FindMarkers"; exit 2; }
	$(PY) tools/sc_api.py "$(FN)"

plan:
	@test -n "$(Q)" || { echo '用法：make plan Q="两个样本 PBMC 整合"'; exit 2; }
	$(PY) tools/sc_plan.py "$(Q)"

rebuild:
	$(PY) tools/etl/rebuild.py
	$(PY) tools/selftest.py

pack:
	$(PY) tools/pack.py

clean:
	$(PY) -c "import shutil;[shutil.rmtree(p,ignore_errors=True) for p in ['.build','tools/__pycache__','tools/etl/__pycache__','tests/__pycache__']]"
	@echo "cleaned（只删构建产物，不动源码与事实底座）"
