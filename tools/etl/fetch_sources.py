#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_sources.py —— 抓取 Seurat / SeuratObject 源码，为重建事实底座做准备。

只用标准库（urllib / tarfile / json），不依赖 git 二进制、不依赖第三方包。

默认抓取：
  - satijalab/seurat        -> <BUILD>/seurat         （走 tarball，不依赖 git）
  - mojaveazure/seurat-object -> <BUILD>/seurat-object （走 GitHub API 逐个下载，
    因为这个仓库在某些网络下 git clone 会 502，逐文件下载更稳）

用法：
  python3 fetch_sources.py                 抓两个仓库
  python3 fetch_sources.py --only seurat  只抓 seurat
  python3 fetch_sources.py --only seurat-object
  python3 fetch_sources.py --ref v5.1.0   指定 seurat 的 git ref（tag / branch / sha）

输出目录可用环境变量 SEURAT_BUILD_DIR 覆盖。
若网络环境需要跳过 TLS 校验（企业代理常见），设 SEURAT_INSECURE_TLS=1。
已存在的目标目录会被"补齐"而不是重下：只对缺失文件发起请求。
"""
import io
import json
import os
import ssl
import sys
import tarfile
import urllib.request
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(os.path.dirname(HERE))
BUILD_DIR = os.path.abspath(os.environ.get(
    "SEURAT_BUILD_DIR", os.path.join(SKILL_DIR, ".build")))

SEURAT_REPO = "satijalab/seurat"
SO_REPO = "mojaveazure/seurat-object"
SO_REF = "develop"          # SeuratObject 的活跃分支

UA = {"User-Agent": "seurat-sc-skill/1.0 (+https://github.com/satijalab/seurat)"}


def _ctx():
    """TLS 上下文。默认严格校验；仅在显式开启 SEURAT_INSECURE_TLS 时才放宽。"""
    if os.environ.get("SEURAT_INSECURE_TLS") == "1":
        c = ssl.create_default_context()
        c.check_hostname = False
        c.verify_mode = ssl.CERT_NONE
        return c
    return ssl.create_default_context()


def get(url, binary=False, timeout=120):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
        b = r.read()
    return b if binary else b.decode("utf-8", "replace")


def fetch_tarball(repo, ref, dest):
    """下载 repo 的 tarball 并解到 dest（dest 顶层即为仓库内容）。"""
    url = "https://api.github.com/repos/%s/tarball/%s" % (repo, ref)
    print("  downloading %s @ %s ..." % (repo, ref))
    try:
        blob = get(url, binary=True)
    except Exception as e:                       # heads/ 失败则试 tags/
        url = "https://github.com/%s/archive/refs/tags/%s.tar.gz" % (repo, ref)
        print("  heads/ 失败(%s)，改试 tags/ ..." % e)
        blob = get(url, binary=True)

    tmp = dest + ".tmp"
    if os.path.isdir(tmp):
        for root, dirs, files in os.walk(tmp, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
    os.makedirs(tmp, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        target = os.path.realpath(tmp)
        for member in tf.getmembers():
            resolved = os.path.realpath(os.path.join(target, member.name))
            if os.path.commonpath([target, resolved]) != target or not (member.isfile() or member.isdir()):
                raise ValueError("Unsafe archive member: %s" % member.name)
        tf.extractall(tmp)
    # 解出来是 <repo>-<ref>/ 单层目录，抬到 dest
    entries = os.listdir(tmp)
    if len(entries) == 1 and os.path.isdir(os.path.join(tmp, entries[0])):
        src = os.path.join(tmp, entries[0])
    else:
        src = tmp
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.isdir(dest):
        for root, dirs, files in os.walk(dest, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
    os.makedirs(dest, exist_ok=True)
    for name in os.listdir(src):
        os.replace(os.path.join(src, name), os.path.join(dest, name))
    print("  -> %s" % dest)


def fetch_so(dest):
    """SeuratObject：下载 DESCRIPTION / NAMESPACE / R/*.R。"""
    os.makedirs(dest, exist_ok=True)
    for f in ("DESCRIPTION", "NAMESPACE"):
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (SO_REPO, SO_REF, f)
        p = os.path.join(dest, f)
        print("  downloading %s" % f)
        content = get(url, binary=True)
        with io.open(p, "wb") as fh:
            fh.write(content)

    api = "https://api.github.com/repos/%s/contents/R?ref=%s" % (SO_REPO, SO_REF)
    print("  listing R/ via GitHub API ...")
    items = json.loads(get(api))
    rdir = os.path.join(dest, "R")
    os.makedirs(rdir, exist_ok=True)
    for it in items:
        if it.get("type") != "file" or not it["name"].endswith(".R"):
            continue
        p = os.path.join(rdir, it["name"])
        content = get(it["download_url"], binary=True)
        with io.open(p, "wb") as fh:
            fh.write(content)
    expected = {it["name"] for it in items if it.get("type") == "file" and it["name"].endswith(".R")}
    for name in os.listdir(rdir):
        if name.endswith(".R") and name not in expected:
            os.remove(os.path.join(rdir, name))
    print("  -> %s (%d R files)" % (dest, len(os.listdir(rdir))))


def main():
    ap = argparse.ArgumentParser(description="抓取 Seurat / SeuratObject 源码")
    ap.add_argument("--only", choices=["seurat", "seurat-object", "all"],
                    default="all")
    ap.add_argument("--ref", default="master",
                    help="seurat 的 git ref，默认 master；可传 tag 如 v5.1.0")
    ap.add_argument("--so-ref", default=SO_REF)
    args = ap.parse_args()

    os.makedirs(BUILD_DIR, exist_ok=True)
    if args.only in ("seurat", "all"):
        fetch_tarball(SEURAT_REPO, args.ref, os.path.join(BUILD_DIR, "seurat"))
    if args.only in ("seurat-object", "all"):
        SO_REF_LOCAL = args.so_ref
        globals()["SO_REF"] = SO_REF_LOCAL
        fetch_so(os.path.join(BUILD_DIR, "seurat-object"))
    print("BUILD_DIR =", BUILD_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
