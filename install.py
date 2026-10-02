#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install.py —— 把 seurat-sc 技能装到某个 Agent 宿主的 skills 目录。

只用标准库，跨平台（Windows / macOS / Linux）。默认复制而不是软链：
Windows 上 os.symlink() 可能「返回成功却造出不可解析的目录」，且常需管理员权限。

用法：
  python3 install.py                          装到 Claude Code 用户级 ~/.claude/skills/seurat-sc
  python3 install.py --project                装到当前项目 ./.claude/skills/seurat-sc
  python3 install.py --host workbuddy         装到 ~/.workbuddy/skills/seurat-sc
  python3 install.py --dir /path/to/skills    装到任意目录（目录下会建 seurat-sc/）
  python3 install.py --force                  目标已存在时覆盖（覆盖前自动备份）
  python3 install.py --dry-run                只打印将做什么
  python3 install.py --keep-repo-files        连仓库侧文件（CI/贡献指南等）一起装

安全约定：
  * 覆盖已有安装前，先把它整体移成 <目标>.bak-<时间戳>，绝不直接删除。
  * 装完做独立回验（读回 SKILL.md、解 frontmatter、核 name、确认入口脚本），
    只打印「成功」不算成功。
  * 默认裁掉仓库侧文件，装给用户的是「运行时要用的那一份」。
"""
import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import time

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

# 一律排除：构建中间产物与缓存
EXCLUDE_DIRS = {".build", "__pycache__", ".git", ".venv", "raw"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
EXCLUDE_SUFFIX = (".pyc", ".pyo")

# 仓库侧文件：对「使用者」没有意义，默认不装。
# 这些文件的存在是为了维护这个仓库（CI、贡献流程、发布包清单），
# 装进 skills 目录只是噪声。裁剪后自检仍全绿（已用 _tools 的裁剪实验验证）。
REPO_ONLY = {
    ".github",             # CI / issue / PR 模板
    ".gitignore",          # git 相关
    ".gitattributes",      # git 相关
    "install.py",          # 已经装完了，不需要再来一份安装器
    "MANIFEST.md",         # 发布包清单
    "CONTRIBUTING.md",     # 仓库治理
    "CODE_OF_CONDUCT.md",  # 仓库治理
}

# 回验：这些文件不在位，装出来的副本就是坏的
MUST_HAVE = [
    "SKILL.md",
    "tools/sc_lint.py",
    "tools/whitelist.json",
    "references/api-signatures.md",
]


def make_ignore(keep_repo):
    drop = set() if keep_repo else REPO_ONLY

    def ignored(path, names):
        out = [n for n in names
               if n in EXCLUDE_DIRS or n in EXCLUDE_FILES
               or n.endswith(EXCLUDE_SUFFIX) or n in drop]
        return out

    return ignored


def backup(dest):
    """把已有安装整体移成 .bak-<时间戳>，返回备份路径。"""
    ts = time.strftime("%Y%m%d-%H%M%S")
    bak = "%s.bak-%s" % (dest, ts)
    i = 1
    while os.path.exists(bak):
        bak = "%s.bak-%s-%d" % (dest, ts, i)
        i += 1
    shutil.move(dest, bak)
    return bak


def verify(dest):
    """装完回验：读回 SKILL.md、解 frontmatter、核 name、确认入口文件在位。

    返回问题列表（空 = 通过）。
    """
    problems = []
    skill_md = os.path.join(dest, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ["SKILL.md 不存在：%s" % skill_md]

    try:
        txt = io.open(skill_md, encoding="utf-8").read()
    except Exception as e:
        return ["SKILL.md 读不出（编码问题？）：%s" % e]

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    if not m:
        problems.append("SKILL.md 的 YAML frontmatter 解析不了（缺 --- 包裹）")
    else:
        fm = m.group(1)
        g = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not g:
            problems.append("frontmatter 缺 name 字段")
        elif g.group(1) != SKILL_NAME:
            problems.append("frontmatter name=%s，与目录名 %s 不一致（宿主会读不到）"
                            % (g.group(1), SKILL_NAME))
        d = re.search(r'^description:[ \t]*"?(.*?)"?[ \t]*$', fm, re.M)
        if not d or not d.group(1).strip():
            problems.append("frontmatter 的 description 为空")
        elif len(d.group(1)) > 1024:
            problems.append("description 长度 %d 超过 Claude Code 的 1024 上限"
                            % len(d.group(1)))

    for rel in MUST_HAVE:
        if not os.path.exists(os.path.join(dest, rel)):
            problems.append("关键文件缺失：%s" % rel)
    return problems


def main():
    ap = argparse.ArgumentParser(description="安装 seurat-sc 技能")
    ap.add_argument("--host", choices=sorted(HOST_ROOT.keys()), default="claude")
    ap.add_argument("--project", action="store_true",
                    help="装到当前项目（只对 claude 有意义：./.claude/skills/）")
    ap.add_argument("--dir", default=None, help="显式指定 skills 根目录")
    ap.add_argument("--force", action="store_true",
                    help="目标已存在时覆盖（覆盖前先备份成 .bak-<时间戳>）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-repo-files", action="store_true",
                    help="连仓库侧文件（CI/贡献指南/清单）一起装，默认裁掉")
    ap.add_argument("--no-selftest", action="store_true",
                    help="装完不跑自检（仅用于调试安装流程）")
    args = ap.parse_args()

    # --project 只对 claude 有意义；配错宿主时明确报错，不做静默降级
    if args.project and args.host != "claude":
        print("--project 只对 --host claude 有意义（项目级路径 ./.claude/skills/）。\n"
              "要装到其它宿主请用 --host %s 或 --dir。" % args.host)
        return 2

    if args.dir:
        root = os.path.abspath(os.path.expanduser(args.dir))
    elif args.project:
        root = os.path.abspath(os.path.join(os.getcwd(), ".claude", "skills"))
    else:
        root = os.path.expanduser(HOST_ROOT[args.host])

    dest = os.path.join(root, SKILL_NAME)
    source_real = os.path.normcase(os.path.realpath(HERE))
    dest_real = os.path.normcase(os.path.realpath(dest))
    try:
        related = os.path.commonpath([source_real, dest_real])
    except ValueError:
        related = None
    if related in (source_real, dest_real) and source_real != dest_real:
        print("Source and destination must not contain one another.")
        return 2
    print("源     : %s" % HERE)
    print("目标   : %s" % dest)

    if dest_real == source_real:
        print("\n源和目标相同，无需安装。")
        return 0

    backup_path = None
    if os.path.exists(dest):
        if not args.force:
            print("\n目标已存在。加 --force 覆盖（覆盖前会自动备份），"
                  "或先手动删除：%s" % dest)
            return 1
        if args.dry_run:
            print("\n[dry-run] 目标已存在，--force 时会先备份成 .bak-<时间戳> 再覆盖")
        else:
            backup_path = backup(dest)
            print("\n目标已存在，已备份到：%s" % backup_path)

    if not args.keep_repo_files:
        print("裁剪   : %s（--keep-repo-files 可保留）" % ", ".join(sorted(REPO_ONLY)))
    print("排除   : %s" % ", ".join(sorted(EXCLUDE_DIRS)))
    if args.dry_run:
        print("\n[dry-run] 未做任何改动")
        return 0

    os.makedirs(root, exist_ok=True)
    shutil.copytree(HERE, dest, ignore=make_ignore(args.keep_repo_files))

    n = sum(len(f) for _, _, f in os.walk(dest))
    print("\n已安装：%d 个文件 -> %s" % (n, dest))

    # --- 独立回验（不依赖 selftest，直接读回来验）---
    problems = verify(dest)
    if problems:
        print("\n!! 安装回验未通过（装出来的副本不可用，或会读不到）：")
        for p in problems:
            print("   - %s" % p)
        print("   请保留现场排查；原安装的备份在：%s"
              % (backup_path or "（本次无覆盖）"))
        return 1
    print("回验通过：SKILL.md 可解析、name 与目录名一致、关键文件在位。")

    # --- 顺手跑技能自带自检（跳过 --no-selftest）---
    if not args.no_selftest:
        selftest = os.path.join(dest, "tools", "selftest.py")
        if os.path.exists(selftest):
            print("\n运行自检：")
            r = subprocess.run([sys.executable or "python3", selftest])
            if r.returncode != 0:
                print("\n!! 自检未通过，请检查上面输出：%s" % dest)
                return r.returncode

    print("\n安装完成。重启 Agent 宿主后即可使用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
