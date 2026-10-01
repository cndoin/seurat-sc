# CHANGELOG

本项目版本遵循语义化版本（SemVer）：
`MAJOR` = SKILL.md 铁律或工具契约破坏性变更；`MINOR` = 新增能力；`PATCH` = 事实修正 / 文档修补。

## [Unreleased]

### 新增：多语言项目主页与英文 Agent 安装说明（2026-10-01）
- 新增 `README.en.md`，说明 Agent 安装、调用约定、工具能力、版本边界与验证方式。
- 新增 English / 简体中文 / 日本語 / Español 四语静态项目主页，并添加 GitHub Pages 自动部署工作流。

### 新增：跨平台安装与打包（2026-10-01）
- `INSTALL.md`：Windows / macOS / Linux 安装指南（宿主安装、R 环境准备、验证、FAQ）。
- `tools/pack.py`：打包脚本，产出 `zip` + `tar.gz` 双格式；打包前强制文本文件统一 LF，
  并生成 `MANIFEST.md`（文件清单 + SHA-256）。
  已实测：解压后独立跑 `tools/selftest.py` **12/12 全绿、退出码 0**。
- `scripts/preflight.R` 增强：缺包时按来源（conda-forge / CRAN / Bioconductor / GitHub）
  给出可直接复制的安装命令，不再只报「缺某包」。

### 修复
- `scripts/preflight.R` 混入 202 处 CRLF（Windows 文本模式写文件会自动转行尾），
  已统一为 LF —— 否则在 Linux/macOS 上 `#!/usr/bin/env Rscript` 会因 `\r` 找不到解释器。


### 修正：宿主兼容性与开源配套（对齐 Claude Code 官方规范）
- SKILL.md frontmatter 补注释：明确 `name`/`description` 是 Claude 官方必需字段，
  `license`/`version`/`allowed-tools`/`agent_created` 是 WorkBuddy 宿主扩展（Claude 忽略、不报错）。
- `description` 由 672 字符精简到 554 字符（900 字节），双保险低于 1024 上限，并去重触发词堆砌。
- 新增 `CODE_OF_CONDUCT.md`（贡献者公约 1.4 节选）。
- 新增 `.github/workflows/ci.yml`：零依赖 CI 门禁，push/PR 自动跑 `selftest.py` + dogfood 校验。
- 修正 selftest 用例数「12」在文档中的硬编码（实际随 fixtures/文档代码块数漂移），
  改为不依赖具体数字的「全绿 / 退出码 0」表述。

## [1.0.0] - 2026-10-01

首个完整版本。

### 新增：事实底座
- 从 `satijalab/seurat@master`（5.5.1.9005）+ `mojaveazure/seurat-object@develop`（5.0.2）
  解析出 **406 个真实导出符号**，其中 390 个带真实形参表。
- S3 generic 取其全部 method 形参的**并集**，避免"参数明明能传却被判幻觉"。
- 从源码 `deprecated()` 默认值提取 **23 个函数的弃用参数**，不靠人工判断。
- 已验证可复现：同源码重建，符号数 406→406 零增删，`references/*.md` 五个文件 SHA-256 逐字节一致。

### 新增：工具
- `tools/sc_lint.py`：R 脚本静态校验器。函数名存在性（含拼写纠错建议）、
  参数名合法性（识别 `...` 透传）、弃用参数告警、括号/引号配对、中文全角符号检测。
  退出码契约 `0 / 1 / 2`。
- `tools/sc_api.py`：离线签名查询，支持 `--search` / `--module` / `--json`。
- `tools/sc_plan.py`：一句话需求 → 推荐流程（纯规则，不联网、不调 LLM）。
- `tools/selftest.py`：一键自检（fixtures 回归 + 文档代码块 + 工具冒烟 + 数据完整性四类检查），退出码即 CI 门禁。
- `scripts/preflight.R` / `scripts/run_seurat.R`：环境体检与批量执行（需要 R）。

### 新增：文档
- `references/api-signatures.md`（406 符号完整签名，grep 用）
- `references/function-index.md`（按模块分类）
- `references/workflows.md`（QC / SCT / 整合 / 映射 / 空间 / WNN / Mixscape / Sketch 模板）
- `references/pitfalls.md`（v4→v5 迁移坑、参数陷阱、性能与内存）
- `references/environment.md`（安装、版本对齐、离线与 HPC）

### 新增：可复现构建与开源配套
- `tools/etl/`：抓源码 → 解析 → 生成文档的完整链路，零第三方依赖、不依赖 git 二进制。
- `tests/fixtures/`：5 个回归用例，含"作者自己踩过"的 `RunMoransI(features=)` 陷阱用例。
- `install.py`：跨平台安装到 Claude Code（用户级/项目级）、WorkBuddy 或任意目录。
- `LICENSE`（MIT）、`NOTICE`（上游归属）、`README.md`、`CONTRIBUTING.md`、`.gitignore`。

### 兼容性
- SKILL.md frontmatter 符合 Claude Code 规范：`name` / `description`（672 字符，上限 1024）/
  `license` / `version` / `allowed-tools`。
- 不依赖 MCP、不联网、无第三方包；所有路径相对 skill 根目录，无绝对路径。

### 已知边界
- 本机无 R 时，技能只能做到选函数 / 写代码 / 校验 / 规划 / 解读报错，
  不能真实执行出图出数。SKILL.md 已强制要求：此时给用户三选一，禁止编造数值。
