#!/usr/bin/env python3
"""Integration checks for CLI installation and the optional base-R runner."""
import argparse
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
checks = []


def run(args, expected=0, cwd=None):
    result = subprocess.run(args, cwd=cwd or ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=180)
    assert result.returncode == expected, (args, result.returncode, result.stdout, result.stderr)
    return result


def check(name, action):
    try:
        action()
        checks.append((name, True))
        print("PASS " + name)
    except Exception as error:
        checks.append((name, False))
        print("FAIL %s: %s" % (name, error))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rscript")
    args = parser.parse_args()
    py = sys.executable
    for tool, extra in [
        ("selftest", []), ("sc_api", ["FindMarkers"]),
        ("sc_plan", ["Integrate two PBMC samples"]),
        ("sc_lint", ["tests/fixtures/01_valid_basic.R"]),
    ]:
        check(tool + " pure JSON", lambda tool=tool, extra=extra:
              json.loads(run([py, str(ROOT / "tools" / (tool + ".py"))] + extra + ["--json"]).stdout))
    with tempfile.TemporaryDirectory(prefix="seurat-integration-") as temp:
        for helper in ("preflight.R", "run_seurat.R"):
            check(helper + " static lint", lambda helper=helper: json.loads(run(
                [py, str(ROOT / "tools/sc_lint.py"), str(ROOT / "scripts" / helper), "--json"]).stdout))
        base = Path(temp)
        def source_archive_checks():
            spec = importlib.util.spec_from_file_location("fetch_sources", ROOT / "tools/etl/fetch_sources.py")
            fetch = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(fetch)
            for name, rejected in [("source/README", False), ("../escaped-file", True)]:
                blob = io.BytesIO()
                with tarfile.open(fileobj=blob, mode="w:gz") as archive:
                    member = tarfile.TarInfo(name)
                    member.size = 2
                    archive.addfile(member, io.BytesIO(b"ok"))
                fetch.get = lambda *a, **kw: blob.getvalue()
                dest = base / ("unsafe-source" if rejected else "safe-source")
                try:
                    fetch.fetch_tarball("owner/repo", "commit", str(dest))
                except ValueError:
                    assert rejected
                else:
                    assert not rejected
                    assert (dest / "README").read_bytes() == b"ok"
            assert not (base / "escaped-file").exists()
        check("source archive extraction and traversal rejection", source_archive_checks)
        install_cmd = [py, str(ROOT / "install.py"), "--dir", str(base / "skills")]
        dest = base / "skills" / "seurat-sc"

        def install_checks():
            run(install_cmd + ["--dry-run"])
            assert not dest.exists()
            run(install_cmd)
            assert (dest / "SKILL.md").is_file()
            assert not (dest / ".git").exists()
            run(install_cmd, expected=1)
            (dest / "user-notes.txt").write_text("keep me", encoding="utf-8")
            run(install_cmd + ["--force"])
            backups = list(dest.parent.glob("seurat-sc.bak-*"))
            assert len(backups) == 1
            assert (backups[0] / "user-notes.txt").read_text(encoding="utf-8") == "keep me"
            json.loads(run([py, str(dest / "tools" / "selftest.py"), "--json"]).stdout)
            run([py, str(ROOT / "install.py"), "--host", "workbuddy", "--project"], expected=2)
            run([py, str(ROOT / "install.py"), "--dir", str(ROOT / "_nested"), "--dry-run"], expected=2)
        check("install, dry-run, duplicate, backup, installed selftest, invalid targets", install_checks)

        if args.rscript:
            runner = [args.rscript, "--vanilla", str(ROOT / "scripts" / "run_seurat.R")]
            def rcase(name, content, code, warnings):
                script = base / (name + ".R")
                script.write_text(content, encoding="utf-8")
                result = run(runner + ["--script", str(script), "--workdir", str(base / name), "--json"], expected=code)
                data = json.loads(result.stdout)
                assert data["ok"] == (code == 0)
                assert isinstance(data["warnings"], list)
                assert data["warning_count"] == warnings, data
                assert len(data["warnings"]) == min(warnings, 20)
                assert Path(data["log"]).is_file()
                return data
            check("R no warnings and variable isolation", lambda: rcase(
                "clean", 'res <- "user"; logfile <- "user"; cat("hello"); writeLines("ok", "result.txt")', 0, 0))
            check("R single warning with control characters", lambda: rcase(
                "warning", 'warning("line1\\nline2\\tquote\\\"slash\\\\"); cat("done")', 0, 1))
            check("R repeated warnings and collection cap", lambda: rcase(
                "warnings", 'for (i in 1:25) warning(paste("warning", i))', 0, 25))
            check("R runtime error JSON", lambda: rcase("error", 'stop("first\\nsecond")', 1, 0))
            check("R syntax error JSON", lambda: rcase("syntax", 'x <- (', 1, 0))
            check("R missing arguments JSON", lambda: json.loads(run(runner + ["--json"], expected=2).stdout))
            check("R missing script JSON", lambda: json.loads(run(
                runner + ["--script", str(base / "missing.R"), "--json"], expected=2).stdout))
            check("R preflight JSON", lambda: json.loads(run(
                [args.rscript, "--vanilla", str(ROOT / "scripts" / "preflight.R"), "--json"],
                expected=preflight_code(args.rscript)).stdout))
    print("%d/%d passed" % (sum(ok for _, ok in checks), len(checks)))
    return int(any(not ok for _, ok in checks))


def preflight_code(rscript):
    # Preflight legitimately fails when required Seurat packages are absent.
    result = subprocess.run([rscript, "--vanilla", str(ROOT / "scripts" / "preflight.R"), "--json"],
                            capture_output=True, timeout=180)
    assert result.returncode in (0, 1, 2), result.returncode
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

