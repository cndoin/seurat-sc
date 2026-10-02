# CHANGELOG

本项目版本遵循语义化版本（SemVer）：
`MAJOR` = SKILL.md 铁律或工具契约破坏性变更；`MINOR` = 新增能力；`PATCH` = 事实修正 / 文档修补。

## [Unreleased]

### 2026-10-02 发布前复核
- 修复执行器警告 JSON、控制字符转义与用户变量覆盖；修复预检 Inf 内存值、Linux 内存解析及写入探针。
- 修复安装路径重叠、frontmatter 字段跨行误读与负向测试临时目录冲突。
- 修复自定义构建目录和源码更新链路，并拒绝不安全的归档路径。
- 新增 CLI/安装/R 执行器集成测试并纳入 CI，更新网页文档链接；实测范围见 REVIEW-2026-10-02.md。

### 新增：开源就绪度审计与门禁加固（2026-10-02）
- `SECURITY.md`：安全政策 + 威胁模型。明确列出**本项目语境下的漏洞定义** ——
  除常规项外还包括「校验器漏报幻觉」「自检假绿」「事实底座被污染」
  「畸形输入打崩工具」等非传统类别（本项目的最大风险不是被入侵，
  而是让使用者写出错的代码、或被错误地告知"没问题"）。
- `tools/negtest.py`：负向自测（15 用例）。对副本故意制造残缺，逐条断言
  门禁真的会报错。**3 个反向基线 + 12 个残缺用例全部通过**。
- `Makefile`：常用命令别名（不含真逻辑）；顶部注释给出 Windows 等价手敲命令。
- `.editorconfig`：缩进策略，与既有的 `.gitattributes` 配套
  （只写其中一个，Windows 上 git 的 autocrlf 会制造整文件 CRLF diff）。
- `.github/PULL_REQUEST_TEMPLATE.md`（含自检清单）+
  `.github/ISSUE_TEMPLATE/{bug_report,feature_request}.md`。
- CI 升级为**三平台 × 两版本矩阵**（ubuntu/windows/macos × py3.10/3.13，
  `fail-fast: false` + `concurrency` + 最小 `permissions`），并新增 `package`
  job 阻止 `MANIFEST.md` 与文件树漂移。

### 修复：自检的 9 处静默放行（重要）
审计用 15 个「制造残缺」用例逐条测 `selftest.py` 的检出率，发现它在下列
情况下**全部返回 0**（即装出一个坏副本也会被判为健康）：
删 `SKILL.md`（技能唯一入口）、`LICENSE`、`README.md`、`scripts/*.R`、
`tools/etl/rebuild.py`，或把 frontmatter 的 `name` 改成与目录名不符、
`description` 写到超 1024 字符（Claude Code 硬上限，超了技能装不上）。
- `tools/selftest.py` 新增 **E 类「包完整性」检查**（四类 → 五类）：
  SKILL.md 存在且 frontmatter 可解析、`name` 与目录名一致、
  `description` 非空且 ≤1024、`license` 字段在位、11 个交付文件在位、
  LICENSE 是**纯 MIT**（扫描附加限制条款）、`.gitattributes` 锁 LF。
- 自检用例数 12 → 21。

### 修复：selftest --json 不是纯 JSON
- 旧版把人类可读文本与 JSON 混在 stdout，与文档「机器可读」的承诺不符，
  按 `json.loads()` 解析必然失败。现改为：`--json` 时 stdout **只**输出 JSON，
  人类可读信息走 stderr。CI 新增对该契约的断言。

### 修复：install.py 三个安全问题
- **覆盖前不备份**（数据丢失风险）：旧版 `--force` 直接 `shutil.rmtree(dest)`，
  用户放在目标目录里的东西会被无提示抹掉。现改为整体移成
  `<目标>.bak-<时间戳>`，并打印备份路径。
- **装完不回验**：旧版只跑 selftest 就算完。新增 `verify()`：读回 `SKILL.md`、
  解 frontmatter、核 `name` 与目录名一致、确认关键文件在位、查 description
  长度；不通过则非零退出并保留现场。
- **把仓库侧文件装给使用者**：`.github/`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、
  `.gitignore`、`.gitattributes`、`install.py`、`MANIFEST.md` 现在默认裁掉
  （`--keep-repo-files` 可保留）。裁剪清单经实验验证：**裁剪后自检仍全绿**。
- `--project` 配非 claude 宿主时改为明确报错（退出码 2），不再静默降级。

### 修正：文档数字漂移
- `CONTRIBUTING.md` 写 `description 目前 672` —— 实测 **554**
  （672 是 2026-10-01 精简前的历史值）。已改准，并补「文档数字的真值从哪来」对照表。
- `CONTRIBUTING.md` 补：自检五类检查说明、E 类检查的来历、
  「先造残缺确认它真的会红」的维护契约、`install.py` 的安全约定。
- `README.md`：目录结构补全新增文件；「30 秒上手」补 `negtest`；
  新增「质量怎么保证的」与「安全」两节。

### 新增：与开源 Seurat 的等效性/稳定性/效率验证（2026-10-01）
- `VERIFICATION.md`：完整验证报告。核心结论：技能入口与原生 Rscript 运行
  **逐位一致**（pbmc_small + PBMC 3K 2638 细胞）；对官方 vignette 成品对象
  **ARI 0.9644**、9 簇 1:1 映射 9 种经典细胞类型、marker 重叠 9.8/10；
  28/28 经典 marker 归属正确；同种子 ×5 逐位复现、跨种子聚类 ARI=1.0；
  失败协议 4/4 正确；技能包装零计算开销（+2.7s 进程/日志层）。

### 修复：验证发现的文档缺口
- `references/pitfalls.md` 新增参数陷阱 9：`run_seurat.R` 以 `source()` 执行
  脚本，被包装脚本内 `commandArgs()` 拿到的是包装器自己的参数，给分析脚本
  传参必须用环境变量（否则按位置取参解析出垃圾值并报错）。
- `references/pitfalls.md` 新增参数陷阱 10：top marker 按 `avg_log2FC` 裸排序
  会被 pct.1 极低的罕见表达基因刷榜，应按 `p_val` 排序 + `pct.1>0.25` 过滤。
- `SKILL.md` 执行段落补对应注意提示。

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
