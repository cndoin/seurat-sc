#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest.py —— seurat-sc skill 的一键自检（CI 门禁）

跑五类检查：
  A. fixtures 回归   每个 tests/fixtures/*.R 的实际输出必须等于期望
  B. 文档代码块      references/*.md 里所有 ```r 块必须 0 error（文档不能含幻觉）
  C. 工具冒烟        sc_api / sc_plan 的关键行为
  D. 数据完整性      whitelist.json 的规模与关键符号
  E. 包完整性        SKILL.md / frontmatter / 入口脚本 / 许可证等交付文件在位

退出码契约（CI 直接吃这个）：
  0 = 全部通过
  1 = 有用例失败
  2 = 用法错误 / 依赖文件缺失

用法：
  python3 tools/selftest.py            人类可读（stdout）
  python3 tools/selftest.py --json     纯 JSON 到 stdout，人类可读信息走 stderr
"""

# E 类检查的由来（负向测试实测，2026-10-02）：
# 用 15 个「制造残缺」用例逐条测本脚本的检出率，发现 9 处静默放行 ——
# 删掉 SKILL.md（技能唯一入口）、LICENSE、README、scripts/*.R，或者把
# frontmatter 的 name 改错、description 写到超 1024 字符，本脚本一律返回 0。
# 一个永不失败的检查等于没有检查，故补 E 类。

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
    def __init__(self, stream=None):
        self.cases = []
        self.stream = stream          # None = 静默（--json 模式必须保持 stdout 纯净）

    def add(self, name, ok, detail=""):
        self.cases.append({"name": name, "ok": bool(ok), "detail": detail})
        if self.stream is not None:
            self.stream.write("%s  %-46s %s\n" % (
                "PASS" if ok else "FAIL", name, detail if not ok else ""))
            self.stream.flush()

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


FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

# 交付文件必检清单（安装副本裁剪后仍必须齐全的那些）。
# 注意：不要列 .github/ 、CONTRIBUTING.md 、CODE_OF_CONDUCT.md 、MANIFEST.md
# ——它们属于仓库侧文件，install.py 会把它们从安装副本里裁掉，
# 列进来会让「裁剪后的副本自检必然报红」，比没有测试更糟。
DELIVERABLES = [
    ("SKILL.md", "技能唯一入口"),
    ("README.md", "项目说明"),
    ("INSTALL.md", "安装指南"),
    ("LICENSE", "许可证正文"),
    ("NOTICE", "上游归属声明"),
    ("CHANGELOG.md", "变更记录"),
    ("references/api-signatures.md", "事实底座（人读）"),
    ("tools/whitelist.json", "事实底座（机器读）"),
    ("scripts/preflight.R", "环境体检脚本"),
    ("scripts/run_seurat.R", "批量执行脚本"),
    ("tools/etl/rebuild.py", "事实底座重建入口"),
]


def check_package(rep):
    """E. 包完整性 —— 交付文件在位 + SKILL.md frontmatter 合法 + 许可证形态。

    本组是 2026-10-02 负向测试补的：旧版 selftest 在下列情况下全部返回 0 ——
    删 SKILL.md（技能唯一入口）、删 LICENSE / README、删 scripts/*.R、
    frontmatter 的 name 与目录名不符、description 超 1024 字符（Claude Code
    硬上限，超了技能装不上）。这些缺口会让「装出来的坏副本」被判为健康。
    """
    # --- SKILL.md 与 frontmatter ---
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    if not os.path.isfile(skill_md):
        rep.add("SKILL.md exists", False, skill_md)
    else:
        rep.add("SKILL.md exists", True)
        txt = io.open(skill_md, encoding="utf-8").read()
        m = FM.match(txt)
        if not m:
            rep.add("SKILL.md frontmatter parses", False, "缺少 --- 包裹的 YAML 头")
        else:
            rep.add("SKILL.md frontmatter parses", True)
            fm = m.group(1)
            g = re.search(r"^name:\s*(\S+)", fm, re.M)
            exp = os.path.basename(SKILL_DIR)
            rep.add("frontmatter name == dir name", bool(g) and g.group(1) == exp,
                    "name=%s dir=%s" % (g.group(1) if g else "?", exp))
            d = re.search(r'^description:[ \t]*"?(.*?)"?[ \t]*$', fm, re.M)
            desc = d.group(1) if d else ""
            rep.add("description non-empty", bool(desc.strip()), "len=%d" % len(desc))
            rep.add("description <= 1024 chars", len(desc) <= 1024,
                    "len=%d（Claude Code 硬上限）" % len(desc))
            rep.add("frontmatter has license",
                    bool(re.search(r"^license:\s*\S+", fm, re.M)))

    # --- 交付文件在位 ---
    missing = [p for p, _ in DELIVERABLES
               if not os.path.exists(os.path.join(SKILL_DIR, p))]
    rep.add("deliverable files present (%d)" % len(DELIVERABLES), not missing,
            "missing=%s" % missing)

    # --- 许可证形态：必须是纯 MIT，不能夹带附加限制 ---
    lic = os.path.join(SKILL_DIR, "LICENSE")
    if os.path.isfile(lic):
        t = io.open(lic, encoding="utf-8").read()
        is_mit = ("MIT License" in t) and ("WITHOUT WARRANTY OF ANY KIND" in t)
        tainted = re.search(
            r"(?i)(non-?commercial|shall not be used|restricted to|prohibited"
            r"|additional (term|condition|restriction)|no derivative)", t)
        rep.add("LICENSE is plain MIT (no add-on limits)", is_mit and not tainted,
                "mit=%s tainted=%s" % (is_mit, bool(tainted)))

    # --- 行尾策略：仓库里若有 .gitattributes 就必须锁 LF ---
    ga = os.path.join(SKILL_DIR, ".gitattributes")
    if os.path.exists(ga):
        rep.add(".gitattributes locks LF", "eol=lf" in io.open(ga, encoding="utf-8").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="stdout 只输出 JSON；人类可读信息改走 stderr")
    args = ap.parse_args()

    # --json 模式下人类可读信息一律走 stderr，保证 stdout 可被 json.loads 直接吃。
    # （旧版把两类输出混在 stdout，与文档「机器可读」的承诺不符。）
    log = sys.stderr if args.json else sys.stdout

    def echo(s=""):
        log.write(s + "\n")
        log.flush()

    rep = Report(log)
    echo("===== A. fixtures =====")
    check_fixtures(rep)
    echo("\n===== B. 文档代码块 =====")
    check_docs(rep)
    echo("\n===== C. 工具冒烟 =====")
    check_tools(rep)
    echo("\n===== D. 数据完整性 =====")
    check_data(rep)
    echo("\n===== E. 包完整性 =====")
    check_package(rep)

    total = len(rep.cases)
    failed = rep.failed
    echo("\n===== 汇总: %d/%d 通过 =====" % (total - len(failed), total))
    if args.json:
        print(json.dumps({
            "total": total, "passed": total - len(failed),
            "failed": len(failed), "cases": rep.cases,
        }, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
