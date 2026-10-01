# seurat-sc · Seurat v5 单细胞分析 Agent Skill

> **English:** [README](README.en.md) · **中文:** 当前页面 · **Project site:** [English](https://cndoin.github.io/seurat-sc/) / [简体中文](https://cndoin.github.io/seurat-sc/zh-cn/) / [日本語](https://cndoin.github.io/seurat-sc/ja/) / [Español](https://cndoin.github.io/seurat-sc/es/)

给 AI Agent 用的 Seurat v5 技能包：让 Agent 写出的 R 代码**不出现幻觉函数、不出现幻觉参数**。

它不是一个 Seurat 教程，也不是 API 文档的抄写件。它的全部事实来自**程序解析上游 R 包源码**
（`NAMESPACE` + `R/*.R` 的真实 `formals`），并且任何交付前的 R 脚本都会被静态校验器拦一遍。

- 上游底座：Seurat `5.5.1.9005`（master）+ SeuratObject `5.0.2`（develop）
- 收录符号：**406 个**（其中 390 个带真实形参表，23 个函数带源码级弃用标记）
- 依赖：**零第三方包**，只用 Python 3 标准库 + 可选 R

---

## 为什么需要它

LLM 写 Seurat 代码的典型翻车方式，不是逻辑错，是**编造 API**：

| 幻觉 | 真相 |
|---|---|
| `RunWNN(obj)` | **这个函数不存在**。WNN 是三步：`FindMultiModalNeighbors` → `RunUMAP(nn.name="weighted.nn")` → `FindClusters(graph.name="wsnn")` |
| `FindVariableGenes()` | 真实名是 `FindVariableFeatures()` |
| `RunMoransI(obj, features=...)` | 真实签名是 `RunMoransI(data, pos, verbose=TRUE)`，**没有 `features`** |
| 一律把 `slot=` 改成 `layer=` | 只有 12 个函数弃用了 `slot=`；`FindMarkers` / `DoHeatmap` / `FeaturePlot` / `RunUMAP` 上 `slot=` 仍然合法，改了反而报错 |
| `PerturbDiff()` / `TopDEGenesMixscape()` | 有定义但**未导出**，用户根本调不到 |

上表每一条都是本技能在提取过程中实际撞出来的（第 3 条连作者自己都踩了，被校验器当场抓出）。

## 30 秒上手

```bash
# 1. 装到 Claude Code（用户级）
python3 install.py
#   WorkBuddy:  python3 install.py --host workbuddy
#   项目级:     python3 install.py --project

# 2. 确认技能本身没坏
python3 tools/selftest.py          # 全绿（fixtures+文档+工具+数据四类检查），退出码 0

# 3. 交付 R 代码前，必跑
python3 tools/sc_lint.py my_analysis.R --json
```

Windows 上若没有 `python3`，把命令里的 `python3` 换成 `python`。

## 三个工具

| 命令 | 作用 |
|---|---|
| `python3 tools/sc_lint.py <脚本.R>` | **核心**。静态校验：函数名是否存在（含拼写纠错建议）、参数名是否合法、弃用参数告警、括号/引号配对、中文全角符号 |
| `python3 tools/sc_api.py FindMarkers` | 离线查真实签名。`--search <关键词>` 模糊搜，`--module de` 列模块 |
| `python3 tools/sc_plan.py "<一句话需求>"` | 需求 → 推荐流程与函数序列（纯规则，不联网、不调 LLM） |

`sc_lint.py` 的退出码：`0` = 无 error；`1` = 有 error；`2` = 用法错误。
写进 CI 就是 `python3 tools/sc_lint.py script.R || exit 1`。

实测精度：干净脚本 **0 误报**；植入 6 个幻觉的脚本 **6 个全中**。

## 目录结构

```
seurat-sc/
├── SKILL.md                  # Agent 的唯一常驻入口（决策路由 + 铁律 + 失败协议）
├── install.py                # 跨平台安装到各 Agent 宿主
├── INSTALL.md                # 安装指南（Windows / macOS / Linux）
├── MANIFEST.md               # 文件清单 + SHA-256（由 pack.py 生成）
├── LICENSE                   # MIT
├── NOTICE                    # 上游归属与许可证声明
├── CONTRIBUTING.md           # 改这个技能前必读
├── CHANGELOG.md
├── references/
│   ├── api-signatures.md     # 406 个符号的完整真实签名（86 KB，用 grep 查，别整读）
│   ├── function-index.md     # 按模块 / S3 method / S4 类分类
│   ├── workflows.md          # 可直接改用的流程模板（QC/SCT/整合/映射/空间/WNN/Mixscape/Sketch）
│   ├── pitfalls.md           # v4→v5 迁移坑、参数陷阱、性能与内存
│   └── environment.md        # 安装、版本对齐、离线与 HPC 场景
├── scripts/
│   ├── preflight.R           # 环境体检（版本/依赖/内存）
│   └── run_seurat.R          # 批量执行 R 脚本（日志 + 退出码）
├── tools/
│   ├── sc_lint.py            # 核心校验器
│   ├── sc_api.py             # 签名查询
│   ├── sc_plan.py            # 流程规划
│   ├── selftest.py           # 一键自检（fixtures+文档+工具+数据四类检查）
│   ├── pack.py               # 打包成 zip + tar.gz，强制 LF、生成 MANIFEST
│   ├── whitelist.json        # 事实底座（机器读）
│   └── etl/                  # 事实底座的重建链路
│       ├── rebuild.py        #   一键重建（抓源码 → 解析 → 生成文档）
│       ├── fetch_sources.py  #   抓上游源码（不依赖 git 二进制）
│       ├── build_api.py      #   解析 NAMESPACE + formals
│       └── gen_docs.py       #   生成 references + whitelist.json
└── tests/fixtures/*.R        # 5 个回归用例（含"作者踩过的坑"陷阱用例）
```

## 重建事实底座

`whitelist.json` 与 `references/` 不是手写常量，全部可由上游源码重新生成：

```bash
python3 tools/etl/rebuild.py            # 抓源码 + 解析 + 生成
python3 tools/etl/rebuild.py --no-fetch # 用 .build/ 里已有的源码离线重建
python3 tools/etl/rebuild.py --ref v5.1.0   # 指定 Seurat 版本
```

已验证的复现性：用同一份源码重建，`whitelist.json` 符号数 406 → 406（零增删），
`references/*.md` 五个文件 SHA-256 **逐字节一致**。

重建后必须跑 `python3 tools/selftest.py`。

## 宿主兼容性

只依赖 **Bash + Read + Grep**：不联网、不依赖 MCP、不依赖任何宿主专有能力。
所有路径一律相对 skill 根目录书写，不含任何绝对路径。

| 宿主 | 位置 | 命令 |
|---|---|---|
| Claude Code 用户级 | `~/.claude/skills/seurat-sc/` | `python3 install.py` |
| Claude Code 项目级 | `<项目>/.claude/skills/seurat-sc/` | `python3 install.py --project` |
| WorkBuddy | `~/.workbuddy/skills/seurat-sc/` | `python3 install.py --host workbuddy` |
| 其它 | 自定义 | `python3 install.py --dir <skills 根目录>` |

## 能力边界（说清楚，不含糊）

- **能做**：选函数、写脚本、校验脚本、规划流程、解读报错、环境体检建议。
- **不能做**：在没有 R 的机器上真实执行 `Rscript` 出图出数。
  技能要求在这种情况下给用户三选一（本机装 R / 交服务器 / GitHub Actions），
  **并明确禁止假装跑过或编造任何数值结果**。

## 许可证与归属

本技能以 **MIT** 发布（见 `LICENSE`）。

它不隶属于 Satija Lab，也不是 Seurat 官方产物。事实底座派生自
[Seurat](https://github.com/satijalab/seurat)（MIT, © 2021 Seurat authors）与
[SeuratObject](https://github.com/mojaveazure/seurat-object)（MIT）的源码，
仅提取接口性事实信息，不含上游实现代码。完整声明见 `NOTICE`。
