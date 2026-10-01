# -*- coding: utf-8 -*-
"""从 Seurat / SeuratObject 源码生成 skill 的事实底座：
  1) _raw/api_full.json        全量函数 + 真实 formals + 归属文件
  2) 供下一步生成 markdown 引用
"""
import io, os, re, json

# ---- 路径：全部可用环境变量覆盖，默认落在 skill 目录下的 .build/ ----
_HERE = os.path.dirname(os.path.abspath(__file__))        # tools/etl
SKILL_DIR = os.path.dirname(os.path.dirname(_HERE))       # skill 根目录
BUILD_DIR = os.path.abspath(os.environ.get(
    "SEURAT_BUILD_DIR", os.path.join(SKILL_DIR, ".build")))

SEURAT = os.path.abspath(os.environ.get(
    "SEURAT_SRC", os.path.join(BUILD_DIR, "seurat")))
SO_DIR = os.path.abspath(os.environ.get(
    "SEURATOBJECT_SRC", os.path.join(BUILD_DIR, "seurat-object")))
RAW = os.path.abspath(os.environ.get(
    "SEURAT_RAW", os.path.join(BUILD_DIR, "raw")))
os.makedirs(RAW, exist_ok=True)

# ---------------- 通用：解析 R 文件中的函数定义 ----------------
def strip_comments(s):
    """去掉 # 之后的注释，忽略字符串内的 #"""
    out, inq = [], None
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if inq:
            out.append(ch)
            if ch == inq:
                inq = None
            i += 1
            continue
        if ch in "\"'":
            inq = ch; out.append(ch); i += 1; continue
        if ch == "#":
            while i < n and s[i] != "\n":
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)

def split_args(argstr):
    argstr = strip_comments(argstr)
    args, depth, cur, inq = [], 0, [], None
    for ch in argstr:
        if inq:
            cur.append(ch)
            if ch == inq:
                inq = None
            continue
        if ch in "\"'":
            inq = ch; cur.append(ch); continue
        if ch == "`":
            inq = "`"; cur.append(ch); continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur)); cur = []; continue
        cur.append(ch)
    if "".join(cur).strip():
        args.append("".join(cur))
    out = []
    for a in args:
        a = a.strip()
        if not a:
            continue
        if "=" in a:
            n, d = a.split("=", 1)
            out.append((n.strip(), d.strip()))
        else:
            out.append((a, None))
    return out

FN_RE = re.compile(r"(?P<name>[\w.]+)\s*<-\s*function\s*\(", re.M)

def parse_r(path, rel):
    try:
        src = io.open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return {}
    res = {}
    for m in FN_RE.finditer(src):
        name = m.group("name")
        if name in res:
            continue
        start = m.end() - 1
        depth, i, n, inq = 0, start, len(src), None
        while i < n:
            ch = src[i]
            if inq:
                if ch == inq:
                    inq = None
                i += 1; continue
            if ch in "\"'":
                inq = ch; i += 1; continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if i >= n:
            continue
        argstr = src[start + 1:i]
        try:
            args = split_args(argstr)
        except Exception:
            args = []
        line_no = src[:m.start()].count("\n") + 1
        res[name] = {"file": rel, "line": line_no,
                     "args": [{"name": a, "default": b} for a, b in args]}
    return res

# ---------------- 1. Seurat 源码 ----------------
rdir = os.path.join(SEURAT, "R")
seurat_fns = {}
for fn in sorted(os.listdir(rdir)):
    if fn.endswith(".R"):
        seurat_fns.update(parse_r(os.path.join(rdir, fn), fn))

# ---------------- 1b. SeuratObject 源码 ----------------
so_fns = {}
so_rdir = os.path.join(SO_DIR, "R")
if os.path.isdir(so_rdir):
    for fn in sorted(os.listdir(so_rdir)):
        if fn.endswith(".R"):
            so_fns.update(parse_r(os.path.join(so_rdir, fn), "SO:" + fn))

# ---------------- 2. NAMESPACE ----------------
ns = io.open(os.path.join(SEURAT, "NAMESPACE"), encoding="utf-8").read()
def parse_export(text):
    out = []
    for m in re.finditer(r"^export\(\s*([^)]*)\)", text, re.M):
        inner = m.group(1)
        if inner.startswith('"'):
            out.append(inner.strip('"'))
        else:
            out += [x.strip() for x in inner.split(",") if x.strip()]
    return sorted(set(out))

seurat_exports = parse_export(ns)
so_exports = parse_export(io.open(os.path.join(SO_DIR, "NAMESPACE"), encoding="utf-8").read())
# 运算符/替换函数里的引号
seurat_exports = [x.strip('"') for x in seurat_exports]
so_exports = [x.strip('"') for x in so_exports]

s3 = []
for m in re.finditer(r'^S3method\(\s*"?([\w.<\-]+)"?\s*,\s*"?([\w.]+)"?', ns, re.M):
    s3.append({"generic": m.group(1), "class": m.group(2)})
s4cls = []
for m in re.finditer(r"^exportClasses\(([^)]*)\)", ns, re.M):
    s4cls += [x.strip().strip('"') for x in m.group(1).split(",") if x.strip()]

# SeuratObject 的 S3（一并收进白名单，脚本里会用到）
so_ns = io.open(os.path.join(SO_DIR, "NAMESPACE"), encoding="utf-8").read()
so_s3 = []
for m in re.finditer(r'^S3method\(\s*"?([\w.<\-]+)"?\s*,\s*"?([\w.]+)"?', so_ns, re.M):
    so_s3.append({"generic": m.group(1), "class": m.group(2)})

# ---------------- 3. 组装导出记录 ----------------
def find_def(name, table):
    """导出名 -> 实际定义（可能是 name.default / name.Seurat / name.Assay ...）"""
    if name in table:
        return name, table[name]
    # 替换函数 `Foo<-` 定义写作 `Foo<-` 或 `setMethod`
    for suf in (".default", ".Seurat", ".Assay", ".StdAssay", ".SCTAssay",
                ".DimReduc", ".VisiumV1", ".Seurat5", ".V3Matrix", ".matrix",
                ".data.frame", ".dist", ".Graph", ".Neighbor", ".Assay5",
                ".SCTModel", ".IterableMatrix", ".dgCMatrix"):
        cand = name + suf
        if cand in table:
            return cand, table[cand]
    return None, None

records = {}
for name in seurat_exports:
    key, d = find_def(name, seurat_fns)
    rec = {"name": name, "pkg": "Seurat", "kind": "function", "def": key}
    if d:
        rec["file"] = d["file"]
        rec["line"] = d["line"]
        rec["args"] = d["args"]
    else:
        rec["file"] = None; rec["line"] = None; rec["args"] = []
    records[name] = rec

# S3 method 变体的参数并入对应 generic
s3_argmap = {}
for item in s3:
    g, c = item["generic"], item["class"]
    cand = "%s.%s" % (g, c)
    if cand in seurat_fns:
        s3_argmap.setdefault(g, {})[c] = seurat_fns[cand]["args"]
        # 若 generic 本身没有本地定义，用第一个 method 的签名兜底
        if g in records and not records[g]["args"]:
            records[g]["args"] = seurat_fns[cand]["args"]
            records[g]["def"] = cand
            records[g]["file"] = seurat_fns[cand]["file"]

def find_so_def(name):
    if name in so_fns:
        return name, so_fns[name]
    base = name.replace("<-", "")
    for suf in (".Assay", ".Assay5", ".Seurat", ".DimReduc", ".default", ".Graph",
                ".Neighbor", ".StdAssay", ".SCTAssay", ".Any", ".matrix",
                ".dgCMatrix", ".data.frame", ".factor", ".character", ".numeric",
                ".logical", ".list", ".Spatial", ".FOV", ".VisiumV1", ".SlideSeq",
                ".STARmap", ".Molecules", ".Centroids", ".Segmentation", ".LogMap",
                ".IterableMatrix", ".Matrix", ".sparseMatrix", ".data.table"):
        cand = base + suf
        if cand in so_fns:
            return cand, so_fns[cand]
    return None, None

# ---------------- 3b. generic 的真实参数 = 其所有 S3 method 参数的并集 ----------------
def merge_args(list_of_arglists):
    """并集：同名参数取第一个有默认值的；保持首次出现顺序"""
    idx, out = {}, []
    for al in list_of_arglists:
        for a in al:
            n = a["name"]
            if n in ("...",):
                continue
            if n not in idx:
                idx[n] = dict(a)
                out.append(n)
            else:
                if idx[n].get("default") is None and a.get("default") is not None:
                    idx[n] = dict(a)
    if any(any(a["name"] == "..." for a in al) for al in list_of_arglists):
        idx["..."] = {"name": "...", "default": None}
        out.append("...")
    return [idx[n] for n in out]

def collect_generic_args(table):
    """table 里所有 `gen.class <- function` 形式 -> {gen: {class: args}}"""
    g = {}
    for fname, d in table.items():
        if "." not in fname:
            continue
        gen, cls = fname.rsplit(".", 1)
        if not gen or not cls:
            continue
        g.setdefault(gen, {})[cls] = d["args"]
    return g

gen_from_seurat = collect_generic_args(seurat_fns)
gen_from_so = collect_generic_args(so_fns)
all_generic_args = {}
for src in (gen_from_so, gen_from_seurat):
    for k, v in src.items():
        all_generic_args.setdefault(k, {}).update(v)

# S3method() 声明里出现的 generic 也要进白名单（如 subset/merge/split/levels）
s3_generics = sorted({x["generic"] for x in s3 + so_s3})

applied = 0
for gen, variants in all_generic_args.items():
    if gen not in records:
        # 未在 export() 里、但声明了 S3 method 的 generic（subset/merge/split 等）
        if gen not in s3_generics:
            continue
        records[gen] = {"name": gen, "pkg": "S3", "kind": "generic",
                        "def": None, "file": None, "line": None, "args": []}
    # .default 优先，否则并集
    chosen = None
    for pref in ("default", "Seurat", "Assay", "StdAssay", "DimReduc"):
        if pref in variants and variants[pref]:
            chosen = variants[pref]
            break
    if chosen is None:
        chosen = merge_args(list(variants.values()))
    merged = merge_args([chosen] + list(variants.values()))
    if merged:
        r = records[gen]
        # 只有当我们比现有信息更全时才覆盖
        if len(merged) > len(r["args"]):
            r["args"] = merged
            r["variants"] = sorted(variants.keys())
            pref_cls = None
            for pref in ("default", "Seurat", "Assay", "StdAssay", "DimReduc"):
                if pref in variants and variants[pref]:
                    pref_cls = pref
                    break
            if pref_cls is None and variants:
                pref_cls = sorted(variants.keys())[0]
            cand = "%s.%s" % (gen, pref_cls)
            if cand in seurat_fns:
                r["def"] = cand; r["file"] = seurat_fns[cand]["file"]; r["line"] = seurat_fns[cand]["line"]
            elif cand in so_fns:
                r["def"] = cand; r["file"] = so_fns[cand]["file"]; r["line"] = so_fns[cand]["line"]
            applied += 1

for name in so_exports:
    key, d = find_so_def(name)
    if name in records:
        # Seurat 已收录但没签名 -> 用 SO 的定义补齐
        if d and not records[name]["args"]:
            records[name]["args"] = d["args"]
            records[name]["def"] = key
            records[name]["file"] = d["file"]
            records[name]["line"] = d["line"]
        continue
    rec = {"name": name, "pkg": "SeuratObject", "kind": "function", "def": key}
    if d:
        rec["file"] = d["file"]; rec["line"] = d["line"]; rec["args"] = d["args"]
    else:
        rec["file"] = None; rec["line"] = None; rec["args"] = []
    records[name] = rec

# ---------------- 4. 版本 ----------------
def read_ver(p):
    d = io.open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r"^Version:\s*(\S+)", d, re.M)
    return m.group(1) if m else "?"

ver_seurat = read_ver(os.path.join(SEURAT, "DESCRIPTION"))
ver_so = read_ver(os.path.join(SO_DIR, "DESCRIPTION"))

data = {
    "seurat_version": ver_seurat,
    "seuratobject_version": ver_so,
    "functions": records,
    "s3methods": s3 + so_s3,
    "s4classes": s4cls,
    "internal_functions": sorted(seurat_fns.keys()),
}
out = json.dumps(data, ensure_ascii=False)
with io.open(os.path.join(RAW, "api_full.json"), "wb") as f:
    f.write(out.encode("utf-8"))

# ---------------- 5. 统计 ----------------
n_sig = sum(1 for r in records.values() if r["args"])
print("Seurat version:", ver_seurat, "| SeuratObject:", ver_so)
print("total known symbols:", len(records))
print("  Seurat exports:", len(seurat_exports))
print("  SeuratObject exports:", len(so_exports))
print("  with real formals:", n_sig)
print("  S3 method entries:", len(s3) + len(so_s3))
print("  internal fns parsed:", len(seurat_fns))
no_sig = sorted(n for n, r in records.items() if not r["args"])
print("  no formals (%d): %s" % (len(no_sig), ", ".join(no_sig[:80])))
