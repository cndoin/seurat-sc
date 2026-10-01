#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pack.py —— 把 seurat-sc 技能打成跨平台发布包（zip + tar.gz）

特点：
  * 纯标准库，无第三方依赖
  * 打包前强制把文本文件统一为 LF，保证 Linux/macOS 能正确执行 shell/R 脚本
  * 生成 MANIFEST.md（文件清单 + SHA-256），便于校验完整性
  * 自动排除 .git / __pycache__ / .build 等开发期产物

用法：
  python3 tools/pack.py                # 输出到 ../dist/
  python3 tools/pack.py --out <目录>   # 指定输出目录
"""
import argparse
import hashlib
import io
import os
import sys
import tarfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
NAME = os.path.basename(SKILL.rstrip("/\\"))

EXCLUDE_DIRS = {".git", "__pycache__", ".build", ".venv", "node_modules", "dist"}
# MANIFEST.md 由本脚本生成并单独加入，必须从 collect() 排除，否则打进两次
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "MANIFEST.md"}
TEXT_EXT = (".md", ".py", ".R", ".json", ".yml", ".yaml", ".txt", ".sh",
            ".gitignore", ".gitattributes", ".Rbuildignore")


def is_text(rel):
    return rel.endswith(TEXT_EXT) or os.path.basename(rel) in (".gitignore", ".gitattributes")


def collect():
    out = []
    for dp, dn, fn in os.walk(SKILL):
        dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
        for f in sorted(fn):
            if f in EXCLUDE_FILES:
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, SKILL).replace("\\", "/")
            out.append((rel, p))
    return sorted(out)


def read_norm(path):
    """读文件；文本统一 LF（Windows 上 python 文本模式会产生 CRLF，必须归一）"""
    b = io.open(path, "rb").read()
    return b.replace(b"\r\n", b"\n")


def build_manifest(files):
    lines = [
        "# MANIFEST",
        "",
        "打包自 seurat-sc 技能包。每个文件的 SHA-256 前 12 位，便于核对完整性。",
        "",
        "| 文件 | 字节 | SHA-256(12) |",
        "|---|---:|---|",
    ]
    total = 0
    for rel, p in files:
        b = read_norm(p)
        total += len(b)
        lines.append("| `%s` | %d | `%s` |" % (rel, len(b), hashlib.sha256(b).hexdigest()[:12]))
    lines += ["", "**合计 %d 个文件 / %d 字节**" % (len(files), total), ""]
    return "\n".join(lines).encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description="打包 seurat-sc")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(SKILL), "dist"))
    args = ap.parse_args()

    files = collect()
    if not files:
        print("没有找到可打包文件", file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    stamp = "1.0.0"

    # 1. MANIFEST
    manifest = build_manifest(files)
    mp = os.path.join(SKILL, "MANIFEST.md")
    io.open(mp, "wb").write(manifest)

    # 2. zip（Windows / 通用）
    zp = os.path.join(args.out, "%s-%s.zip" % (NAME, stamp))
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, p in files + [("MANIFEST.md", mp)]:
            z.writestr("%s/%s" % (NAME, rel), read_norm(p))

    # 3. tar.gz（Linux / macOS）
    tp = os.path.join(args.out, "%s-%s.tar.gz" % (NAME, stamp))
    with tarfile.open(tp, "w:gz") as t:
        for rel, p in files + [("MANIFEST.md", mp)]:
            b = read_norm(p)
            info = tarfile.TarInfo("%s/%s" % (NAME, rel))
            info.size = len(b)
            info.mode = 0o755 if rel.endswith(".py") or rel.endswith(".sh") else 0o644
            import io as _io
            t.addfile(info, _io.BytesIO(b))

    print("文件数   : %d" % (len(files) + 1))
    print("zip      : %s (%.1f KB)" % (zp, os.path.getsize(zp) / 1024))
    print("tar.gz   : %s (%.1f KB)" % (tp, os.path.getsize(tp) / 1024))
    print("MANIFEST : %s" % mp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
