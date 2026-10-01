# seurat-sc — Seurat v5 skill for AI agents

> **English:** this page · **中文:** [README](README.md) · **Project site:** [English](docs/index.html) / [简体中文](docs/zh-cn/index.html) / [日本語](docs/ja/index.html) / [Español](docs/es/index.html)

`seurat-sc` helps AI coding agents write, check, plan, and troubleshoot R workflows for Seurat v5 single-cell and spatial transcriptomics. Its offline API catalog is generated from Seurat and SeuratObject source interfaces; `sc_lint.py` catches unknown functions, unsupported arguments, deprecated arguments, and common syntax issues before an R script is handed back.

## Install for an AI agent

Clone or download this repository, then run the installer with Python 3.7 or newer. The installer uses only the Python standard library.

```bash
git clone https://github.com/<OWNER>/seurat-sc.git
cd seurat-sc
python3 install.py                 # Claude Code, user scope
python3 install.py --project       # Claude Code, current project
python3 install.py --host workbuddy
python3 install.py --dir <skills-directory>
python3 tools/selftest.py
```

On Windows, use `python` if `python3` is unavailable. Restart the agent host after installation. For Codex or another host, select its skills directory with `--dir`; the package does not claim automatic integration with every host.

### Instructions for agents

Load `SKILL.md` as the entry point and keep the skill directory intact so relative paths resolve. Before delivering an R script, run `python3 tools/sc_lint.py path/to/analysis.R --json`. Treat lint errors as blockers. Consult `references/api-signatures.md` for signatures and `references/workflows.md` for templates. This is a static API snapshot: check the target installation when its Seurat version differs from the documented source versions.

## Capabilities

- **API-aware linting:** checks function names, argument names, deprecated arguments, delimiters, and common full-width punctuation.
- **Offline API lookup:** searches exported Seurat / SeuratObject symbols and extracted signatures.
- **Workflow planning:** maps common requests to suggested function sequences using deterministic rules.
- **Reusable references:** QC, normalization, SCT, integration, mapping, spatial data, WNN, Mixscape, and sketch workflows.
- **Optional R helpers:** `scripts/preflight.R` checks the environment; `scripts/run_seurat.R` runs a supplied script with logs and error handling. Both require R and relevant packages.

It does not infer sample paths, organism, marker genes, cell identities, or numeric results. Static linting does not prove that an analysis runs or that its scientific assumptions are sound.

## Quick examples

```bash
python3 tools/sc_api.py FindMarkers
python3 tools/sc_api.py --search integration
python3 tools/sc_plan.py "Integrate two PBMC samples and find marker genes"
python3 tools/sc_lint.py analysis.R --json
```

## Requirements and verification

- Python 3.7+ for installation and offline tools; no third-party Python packages.
- R 4.0+ and compatible Seurat packages only for optional R helpers and real analysis execution.
- Windows, macOS, and Linux are supported for the Python tools.

Run `python3 tools/selftest.py` to check fixtures, documented R examples, CLI smoke cases, and catalog integrity. `python3 tools/etl/rebuild.py` regenerates the API catalog from upstream source and downloads source unless `--no-fetch` is used with a prepared `.build/` cache.

## Compatibility and attribution

This catalog snapshot was generated from Seurat `5.5.1.9005` and SeuratObject `5.0.2`. `NOTICE` describes upstream projects and attribution. `seurat-sc` is an independent MIT-licensed project and is not affiliated with or endorsed by Satija Lab. See [LICENSE](LICENSE).

Other languages: [简体中文](README.md) · [日本語](docs/ja/index.html) · [Español](docs/es/index.html)
