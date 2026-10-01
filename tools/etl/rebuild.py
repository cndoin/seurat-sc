#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rebuild.py —— 一键重建 seurat-sc 的事实底座。

链路： 抓源码 -> 解析 NAMESPACE/formals -> 生成 references + whitelist.json

用法：
  python3 rebuild.py                  全量重建（先抓源码，再解析，再生成文档）
  python3 rebuild.py --no-fetch       用 .build/ 里已有的源码重建（离线）
  python3 rebuild.py --ref v5.1.0     指定 seurat 版本重建
  python3 rebuild.py --dry-run        只打印将要执行的步骤

产物（都在 skill 目录内）：
  references/api-signatures.md    全量函数真实签名
  references/function-index.md    按模块分类索引
  tools/whitelist.json            sc_lint.py 用的导出符号 + 参数名 + 弃用参数

改任何一个上游版本后，请重跑本脚本 + `python3 tools/selftest.py`，
保证 references/ 与 whitelist.json 与源码一致。
"""
import argparse
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(os.path.dirname(HERE))
PY = sys.executable or "python3"


def run(script, extra=None):
    cmd = [PY, os.path.join(HERE, script)] + (extra or [])
    print("\n$ %s" % " ".join(cmd))
    r = subprocess.run(cmd, cwd=HERE)
    if r.returncode != 0:
        print("!! %s failed (exit=%d)" % (script, r.returncode))
        sys.exit(r.returncode)


def snapshot(path):
    if not os.path.exists(path):
        return None
    return json.loads(io.open(path, encoding="utf-8").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true", help="跳过抓源码")
    ap.add_argument("--ref", default="master")
    ap.add_argument("--so-ref", default="develop")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wl = os.path.join(SKILL_DIR, "tools", "whitelist.json")
    before = snapshot(wl)

    steps = []
    if not args.no_fetch:
        steps.append(("fetch_sources.py",
                      ["--ref", args.ref, "--so-ref", args.so_ref]))
    steps.append(("build_api.py", []))
    steps.append(("gen_docs.py", []))

    if args.dry_run:
        for s, e in steps:
            print("would run: %s %s" % (s, " ".join(e)))
        return 0

    for s, e in steps:
        run(s, e)

    after = snapshot(wl)
    print("\n===== 结果 =====")
    if before and after:
        b = set(before.get("symbols", {}))
        a = set(after.get("symbols", {}))
        print("符号数: %d -> %d  (新增 %d, 移除 %d)" % (
            len(b), len(a), len(a - b), len(b - a)))
        if a - b:
            print("  新增:", ", ".join(sorted(a - b)[:20]))
        if b - a:
            print("  移除:", ", ".join(sorted(b - a)[:20]))
        if before.get("generated_from") != after.get("generated_from"):
            print("  上游版本: %s -> %s" % (
                before.get("generated_from"), after.get("generated_from")))
    else:
        print("whitelist.json:", len(after.get("symbols", {})) if after else "缺失")

    print("\n下一步：跑 `python3 tools/selftest.py` 确认全部用例仍然通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
