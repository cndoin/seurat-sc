#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install.py —— 把 seurat-sc 技能装到某个 Agent 宿主的 skills 目录。

只用标准库，跨平台（Windows / macOS / Linux）。默认复制（不是软链，
因为 Windows 建符号链接常需要管理员权限）。

用法：
  python3 install.py                          装到 Claude Code 用户级 ~/.claude/skills/seurat-sc
  python3 install.py --project                装到当前项目 ./.claude/skills/seurat-sc
  python3 install.py --host workbuddy         装到 ~/.workbuddy/skills/seurat-sc
  python3 install.py --dir /path/to/skills    装到任意目录（目录下会建 seurat-sc/）
  python3 install.py --force                  目标已存在时覆盖
  python3 install.py --dry-run                只打印将做什么

装完后请重启 Agent 宿主，让它重新扫描 skills 目录。
"""
import argparse
import os
import shutil
import sys

SKILL_NAME = "seurat-sc"
HERE = os.path.dirname(os.path.abspath(__file__))

# 宿主的 skills 根目录。只列确认过的：
#   Claude Code  -> ~/.claude/skills/   （项目级 ./.claude/skills/）
#   WorkBuddy    -> ~/.workbuddy/skills/
# 其它宿主（Codex 等）请用 --dir 显式指定，本脚本不做猜测。
HOST_ROOT = {
    "claude": os.path.join("~", ".claude", "skills"),
    "workbuddy": os.path.join("~", ".workbuddy", "skills"),
}

EXCLUDE_DIRS = {".build", "__pycache__", ".git", ".venv", "raw"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}


def ignored(path, names):
    return [n for n in names if n in EXCLUDE_DIRS or n in EXCLUDE_FILES]


def main():
    ap = argparse.ArgumentParser(description="安装 seurat-sc 技能")
    ap.add_argument("--host", choices=sorted(HOST_ROOT.keys()), default="claude")
    ap.add_argument("--project", action="store_true",
                    help="装到当前项目（只对 claude 有意义：./.claude/skills/）")
    ap.add_argument("--dir", default=None, help="显式指定 skills 根目录")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dir:
        root = os.path.abspath(os.path.expanduser(args.dir))
    elif args.project and args.host == "claude":
        root = os.path.abspath(os.path.join(os.getcwd(), ".claude", "skills"))
    else:
        root = os.path.expanduser(HOST_ROOT[args.host])

    dest = os.path.join(root, SKILL_NAME)
    print("源     : %s" % HERE)
    print("目标   : %s" % dest)

    if os.path.abspath(dest) == os.path.abspath(HERE):
        print("\n源和目标相同，无需安装。")
        return 0

    if os.path.exists(dest):
        if not args.force:
            print("\n目标已存在。加 --force 覆盖，或先手动删除：%s" % dest)
            return 1
        print("\n目标已存在，--force：先删除")
        if not args.dry_run:
            shutil.rmtree(dest)

    print("排除   : %s" % ", ".join(sorted(EXCLUDE_DIRS)))
    if args.dry_run:
        print("\n[dry-run] 未做任何改动")
        return 0

    os.makedirs(root, exist_ok=True)
    shutil.copytree(HERE, dest, ignore=ignored)

    n = sum(len(f) for _, _, f in os.walk(dest))
    print("\n已安装：%d 个文件 -> %s" % (n, dest))

    # 装完顺手自检，避免装过去的是个坏包
    selftest = os.path.join(dest, "tools", "selftest.py")
    if os.path.exists(selftest):
        print("\n运行自检：")
        r = __import__("subprocess").run([sys.executable or "python3", selftest])
        if r.returncode != 0:
            print("\n!! 自检未通过，请检查上面输出")
            return r.returncode
        print("\n自检通过。重启 Agent 宿主后即可使用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
