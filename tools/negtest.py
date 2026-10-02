#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""negtest.py —— 负向自测：证明门禁真的会失败。

铁律：**一个永不失败的检查等于没有检查。**

本脚本检查的不是技能，而是**检查本身**。它对交付物故意制造残缺，
确认对应的门禁真的会报错。如果某条门禁对残缺输入仍然放行，
说明那道门是假的 —— 装进 CI 也拦不住任何东西。

它固化的是 2026-10-02 那次审计发现的问题：旧版 selftest 对
「删掉 SKILL.md / LICENSE / README / scripts/*.R、frontmatter 的 name 改错、
description 超 1024」等 9 种残缺状态一律返回 0。

退出码：
  0 = 所有负向用例都被正确检出
  1 = 有门禁失效（有残缺没被检出）
  2 = 环境错误（连技能本体都跑不起来）

用法：
  python3 tools/negtest.py            人类可读
  python3 tools/negtest.py --json     纯 JSON 到 stdout
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SKILL_NAME = os.path.basename(SKILL_DIR)
PY = sys.executable or "python3"

EXCLUDE = {".git", ".build", "__pycache__", ".venv", "raw", ".mypy_cache",
           ".pytest_cache", ".idea", ".vscode"}

results = []          # (name, ok, detail)
log_stream = sys.stdout


def emit(s=""):
    if log_stream is not None:
        log_stream.write(s + "\n")
        log_stream.flush()


# --------------------------------------------------------------- 夹具
def fresh_copy(dst):
    """把技能树复制到 dst。

    注意：dst 的最后一段目录名**必须**等于 SKILL_NAME ——
    selftest 的 E 类检查与 install.verify() 都会核对
    「frontmatter 的 name == 目录名」，改名会让基线用例假红。
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(
        SKILL_DIR, dst,
        ignore=lambda d, names: [n for n in names
                                 if n in EXCLUDE or n.endswith((".pyc", ".pyo"))])


def rm(d, rel):
    p = os.path.join(d, rel.replace("/", os.sep))
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.exists(p):
        os.remove(p)


def set_skill_name(d, value):
    p = os.path.join(d, "SKILL.md")
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"^name:.*$", "name: %s" % value, s, count=1, flags=re.M)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


# --------------------------------------------------------------- 门禁调用
# 约定：所有 gate_* 返回 True = **门禁报错了**（检出问题）。
def gate_selftest(d):
    r = subprocess.run([PY, os.path.join(d, "tools", "selftest.py"), "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=d)
    return r.returncode != 0


def gate_lint(d, rel):
    p = os.path.join(d, rel.replace("/", os.sep))
    r = subprocess.run([PY, os.path.join(d, "tools", "sc_lint.py"), p, "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=d)
    return r.returncode != 0


def gate_verify(d):
    """install.verify() 返回问题列表；非空 = 报错。"""
    sys.path.insert(0, d)
    sys.modules.pop("install", None)
    try:
        import install
        return len(install.verify(d)) > 0
    finally:
        sys.path.pop(0)
        sys.modules.pop("install", None)


def gate_json_impure(d):
    """selftest --json 的 stdout 不是纯 JSON 就算门禁报错。"""
    r = subprocess.run([PY, os.path.join(d, "tools", "selftest.py"), "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=d)
    try:
        json.loads(r.stdout.decode("utf-8", "replace"))
        return False
    except Exception:
        return True


# --------------------------------------------------------------- 用例框架
def check(name, mutate, runner, expect_gate_error=True):
    """expect_gate_error=True : 制造残缺后，期望门禁报错（检出）
       expect_gate_error=False: 完好副本，期望门禁放行（基线）"""
    root = tempfile.mkdtemp(prefix="sc_negtest_")
    dst = os.path.join(root, SKILL_NAME)
    try:
        fresh_copy(dst)
        if mutate:
            mutate(dst)
        got = bool(runner(dst))
        ok = (got == expect_gate_error)
        detail = "门禁%s，期望%s" % ("报错" if got else "放行",
                                     "报错" if expect_gate_error else "放行")
    except Exception as e:
        ok, detail = False, "harness error: %s" % e
    finally:
        shutil.rmtree(root, ignore_errors=True)
    results.append((name, ok, detail))
    emit("%s  %-50s %s" % ("PASS" if ok else "FAIL", name, "" if ok else detail))


def main():
    global log_stream
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="stdout 只输出 JSON；人类可读信息走 stderr")
    args = ap.parse_args()
    log_stream = sys.stderr if args.json else sys.stdout

    emit("=== 负向自测：门禁是否真的会失败 ===")

    # --- 反向基线：完好的副本必须放行（否则下面全是假红）---
    check("BASELINE 完好副本 -> selftest 放行", None, gate_selftest,
          expect_gate_error=False)
    check("BASELINE 干净脚本 -> sc_lint 放行",
          None, lambda d: gate_lint(d, "tests/fixtures/01_valid_basic.R"),
          expect_gate_error=False)
    check("BASELINE 完好副本 -> install.verify() 放行", None, gate_verify,
          expect_gate_error=False)

    # --- sc_lint 必须拦住幻觉 ---
    check("sc_lint 拦住幻觉脚本（02_hallucination）",
          None, lambda d: gate_lint(d, "tests/fixtures/02_hallucination.R"))
    check("sc_lint 拦住幻觉参数（05_moransi_trap）",
          None, lambda d: gate_lint(d, "tests/fixtures/05_moransi_trap.R"))

    # --- selftest 必须发现「交付物残缺」---
    check("selftest 发现 SKILL.md 缺失", lambda d: rm(d, "SKILL.md"), gate_selftest)
    check("selftest 发现 name 与目录名不符",
          lambda d: set_skill_name(d, "definitely-wrong-name"), gate_selftest)
    check("selftest 发现 LICENSE 缺失", lambda d: rm(d, "LICENSE"), gate_selftest)
    check("selftest 发现入口脚本缺失",
          lambda d: rm(d, "scripts/run_seurat.R"), gate_selftest)
    check("selftest 发现事实底座缺失",
          lambda d: rm(d, "tools/whitelist.json"), gate_selftest)
    check("selftest 发现重建入口缺失",
          lambda d: rm(d, "tools/etl/rebuild.py"), gate_selftest)

    # --- install.verify() 必须能认出坏副本 ---
    check("install.verify() 认出缺 SKILL.md 的副本",
          lambda d: rm(d, "SKILL.md"), gate_verify)
    check("install.verify() 认出 name 不符的副本",
          lambda d: set_skill_name(d, "wrong-name"), gate_verify)
    check("install.verify() 认出关键文件缺失的副本",
          lambda d: rm(d, "tools/sc_lint.py"), gate_verify)

    # --- --json 必须机器可读（CI 与外部脚本依赖这一点）---
    check("selftest --json 的 stdout 是纯 JSON", None, gate_json_impure,
          expect_gate_error=False)

    bad = [r for r in results if not r[1]]
    total = len(results)
    emit()
    emit("===== 汇总: %d/%d 通过 =====" % (total - len(bad), total))
    if args.json:
        print(json.dumps({
            "total": total,
            "passed": total - len(bad),
            "failed": len(bad),
            "cases": [{"name": n, "ok": o, "detail": dt} for n, o, dt in results],
        }, ensure_ascii=False, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
