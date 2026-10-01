#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest.py —— seurat-sc skill 的一键自检（CI 门禁）

跑四类检查：
  A. fixtures 回归   每个 tests/fixtures/*.R 的实际输出必须等于期望
  B. 文档代码块      references/*.md 里所有 ```r 块必须 0 error（文档不能含幻觉）
  C. 工具冒烟        sc_api / sc_plan 的关键行为
  D. 数据完整性      whitelist.json 的规模与关键符号

退出码契约（CI 直接吃这个）：
  0 = 全部通过
  1 = 有用例失败
  2 = 用法错误 / 依赖文件缺失

用法：
  python3 tools/selftest.py            人类可读
  python3 tools/selftest.py --json     机器可读
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
PY = sys.executable or "python3"

LINT = os.path.join(HERE, "sc_lint.py")
API = os.path.join(HERE, "sc_api.py")
PLAN = os.path.join(HERE, "sc_plan.py")
WL = os.path.join(HERE, "whitelist.json")
FIXTURES = os.path.join(SKILL_DIR, "tests", "fixtures")
REFS = os.path.join(SKILL_DIR, "references")

# 期望表：文件名 -> (期望退出码, 期望 error code 多重集合为空则写 None)
# code 用 "code" 或 "code:count" 表达
EXPECT = {
    "01_valid_basic.R":     (0, {}),                                     # 干净脚本 0 噪音
    "02_hallucination.R":   (1, {"unknown-function": 3, "unknown-arg": 3}),
    "03_valid_advanced.R":  (0, {}),                                     # 复杂流程 0 误报
    "04_syntax_error.R":    (1, {"syntax": 2}),
    "05_moransi_trap.R":    (1, {"unknown-arg": 1}),                     # RunMoransI(features=) 幻觉
}

BLOCK = re.compile(r"```r\n(.*?)```", re.S)


def lint_json(path):
    """跑 sc_lint.py --json，返回 (returncode, parsed_dict)"""
    r = subprocess.run([PY, LINT, path, "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = r.stdout.decode("utf-8", "replace")
    try:
        return r.returncode, json.loads(out)
    except Exception:
        return r.returncode, {"_raw": out, "_stderr": r.stderr.decode("utf-8", "replace")}


def count_codes(items):
    c = {}
    for it in items:
        c[it.get("code", "?")] = c.get(it.get("code", "?"), 0) + 1
    return c


class Report(object):
    def __init__(self):
        self.cases = []

    def add(self, name, ok, detail=""):
        self.cases.append({"name": name, "ok": bool(ok), "detail": detail})
        print("%s  %-46s %s" % ("PASS" if ok else "FAIL", name,
                                detail if not ok else ""))

    @property
    def failed(self):
        return [c for c in self.cases if not c["ok"]]


def check_fixtures(rep):
    if not os.path.isdir(FIXTURES):
        rep.add("fixtures dir exists", False, FIXTURES)
        return
    for fn in sorted(os.listdir(FIXTURES)):
        if not fn.endswith(".R"):
            continue
        path = os.path.join(FIXTURES, fn)
        want_exit, want_codes = EXPECT.get(fn, (0, {}))
        rc, d = lint_json(path)
        got = count_codes(d.get("errors", []))
        if rc != want_exit:
            rep.add("fixture %s" % fn, False,
                    "exit %d != %d; errors=%s" % (rc, want_exit, got))
            continue
        if want_codes and got != want_codes:
            rep.add("fixture %s" % fn, False,
                    "codes %s != %s" % (got, want_codes))
            continue
        if not want_codes and got:
            rep.add("fixture %s" % fn, False, "unexpected errors %s" % got)
            continue
        rep.add("fixture %s" % fn, True)


def check_docs(rep):
    if not os.path.isdir(REFS):
        rep.add("references dir exists", False, REFS)
        return
    total = bad = 0
    details = []
    for fn in sorted(os.listdir(REFS)):
        if not fn.endswith(".md"):
            continue
        txt = io.open(os.path.join(REFS, fn), encoding="utf-8").read()
        for i, m in enumerate(BLOCK.finditer(txt), 1):
            total += 1
            tmp = os.path.join(tempfile.gettempdir(),
                               "sc_doc_%s_%d.R" % (fn[:8], i))
            with io.open(tmp, "wb") as f:
                f.write(m.group(1).encode("utf-8"))
            rc, d = lint_json(tmp)
            if rc != 0:
                bad += 1
                details.append("%s#%d: %s" % (fn, i, count_codes(d.get("errors", []))))
    rep.add("doc code blocks (%d blocks, %d bad)" % (total, bad), bad == 0,
            "; ".join(details[:5]))


def check_tools(rep):
    # sc_api：真实函数能查到
    r = subprocess.run([PY, API, "FindMarkers", "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ok = r.returncode == 0 and "FindMarkers" in r.stdout.decode("utf-8", "replace")
    rep.add("sc_api FindMarkers", ok)

    # sc_api：幻觉函数必须非零退出
    r = subprocess.run([PY, API, "RunWNN", "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rep.add("sc_api rejects RunWNN", r.returncode != 0,
            "exit=%d" % r.returncode)

    # sc_plan：能给出流程
    r = subprocess.run([PY, PLAN, "两个样本 PBMC 整合后找差异基因", "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = r.stdout.decode("utf-8", "replace")
    steps = 0
    if r.returncode == 0:
        try:
            j = json.loads(out)
            # sc_plan --json 返回数组：每项是一套候选流程 {id,title,score,steps,notes}
            plans = j if isinstance(j, list) else [j]
            steps = sum(len(p.get("steps") or []) for p in plans)
        except Exception:
            steps = 0
    rep.add("sc_plan returns steps", steps > 0, "steps=%d" % steps)


def check_data(rep):
    if not os.path.exists(WL):
        rep.add("whitelist.json exists", False, WL)
        return
    w = json.loads(io.open(WL, encoding="utf-8").read())
    syms = w.get("symbols", {})
    rep.add("whitelist size >= 400", len(syms) >= 400, "size=%d" % len(syms))
    need = ["FindMarkers", "SCTransform", "IntegrateLayers", "RunUMAP",
            "FindTransferAnchors", "CreateSeuratObject", "FindClusters"]
    missing = [n for n in need if n not in syms]
    rep.add("key symbols present", not missing, "missing=%s" % missing)
    rep.add("has generated_from", "generated_from" in w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rep = Report()
    print("===== A. fixtures =====")
    check_fixtures(rep)
    print("\n===== B. 文档代码块 =====")
    check_docs(rep)
    print("\n===== C. 工具冒烟 =====")
    check_tools(rep)
    print("\n===== D. 数据完整性 =====")
    check_data(rep)

    total = len(rep.cases)
    failed = rep.failed
    print("\n===== 汇总: %d/%d 通过 =====" % (total - len(failed), total))
    if args.json:
        print(json.dumps({
            "total": total, "passed": total - len(failed),
            "failed": len(failed), "cases": rep.cases,
        }, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
