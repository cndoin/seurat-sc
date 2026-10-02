# CONTRIBUTING

改这个技能前，先读这一页。核心原则只有一条：**技能里写的每一个 API 事实，都必须能溯源到上游源码。**
凭印象写函数签名 = 引入幻觉，这是这个技能存在的理由，别把它破坏掉。

## 一、改东西之前

```bash
python3 tools/selftest.py      # 必须全绿、退出码 0
```

这是基线。改完之后再跑一次，仍然全绿（退出码 0）才允许提交。

自检跑五类检查，改哪类就重点看哪类：

| 类 | 查什么 | 你什么时候会碰到 |
|---|---|---|
| A | `tests/fixtures/*.R` 的实际输出 == 期望 | 改了 `sc_lint.py` 的规则 |
| B | `references/*.md` 里每个 ```r 代码块 0 error | 改了文档里的示例代码 |
| C | `sc_api` / `sc_plan` 的关键行为 | 改了这两个工具 |
| D | `whitelist.json` 的规模与关键符号 | 重建过事实底座 |
| E | SKILL.md / frontmatter / 入口脚本 / 许可证形态 | 改了 `SKILL.md`、动了文件布局、准备发版 |

**E 类的来历值得知道**：2026-10-02 用 15 个「制造残缺」用例逐条测自检的
检出率，发现 9 处静默放行——删掉 `SKILL.md`（技能唯一入口）、`LICENSE`、
`README.md`、`scripts/*.R`，或者把 frontmatter 的 `name` 改错、
`description` 写到超 1024 字符，旧版自检**一律返回 0**。
一个永不失败的检查等于没有检查，所以补了 E 类。
以后新增检查项也请照这个套路：**先造残缺，确认它真的会红。**

## 二、四类改动的正确做法

### 1. 想加/改一条 API 事实（函数名、参数、弃用标记）

**不要手改 `whitelist.json`，也不要手改 `references/api-signatures.md`。**
这些是生成物。正确做法：

```bash
python3 tools/etl/rebuild.py --no-fetch   # 用 .build/ 里已有的源码重新生成
# 或
python3 tools/etl/rebuild.py              # 顺便从上游重抓源码
python3 tools/selftest.py
```

上游升级版本时：

```bash
python3 tools/etl/rebuild.py --ref v5.2.0
python3 tools/selftest.py
```

然后检查 `rebuild.py` 打印的符号增删列表，确认没有意外的大进大出。

### 2. 想加流程模板（`references/workflows.md`）或避坑条目（`references/pitfalls.md`）

随便写，但**里面的每个 ```r 代码块都会被 `selftest.py` 自动抽取并跑 `sc_lint.py`**。
写了不存在的函数或参数，自检会直接红。这是有意设计的：文档不许含幻觉。

### 3. 想改 `sc_lint.py` 的行为（放宽/收紧规则）

先问自己：会不会引入误报？会不会漏掉真幻觉？
改完必须同时满足：

- `tests/fixtures/01_valid_basic.R` 与 `03_valid_advanced.R` 仍然 0 error（无误报）
- `tests/fixtures/02_hallucination.R` 仍然抓满 6 个 error（无漏报）

如果为了让某个用例通过而放宽规则，说明规则写错了，不是用例写错了。

### 4. 想加新的回归用例

在 `tests/fixtures/` 加 `.R` 文件，并在 `tools/selftest.py` 的 `EXPECT` 表里登记期望：

```python
EXPECT = {
    "06_my_case.R": (0, {}),                     # (期望退出码, {错误码: 出现次数})
}
```

期望值从实际运行结果里取，不要凭空填：

```bash
python3 tools/sc_lint.py tests/fixtures/06_my_case.R --json
```

### 5. 想改文档里写的数字（用例数 / 符号数 / 长度）

文档里的数字过期后**会让读者对项目成熟度判断失真**，所以别让它们漂。

现在的数字来源：

| 文档里的数字 | 真值从哪来 |
|---|---|
| 406 个符号 / 390 带形参 / 23 带弃用标记 | `tools/whitelist.json`（`len(symbols)`、`len(deprecated_args)`） |
| 5 个回归用例 | `tests/fixtures/*.R` 的个数 |
| 自检 N/N 通过 | 跑一次 `python3 tools/selftest.py --json` 取 `total` |
| `description` 字符数 | `SKILL.md` frontmatter 的 `description` |

改数字时**不要 find-replace**——先跑一次把真值量出来，再照着改，
并且留意"都对但都不完整"的情况（如 26 个子命令 = 21 分析 + 5 编排，
写「21」或「18」都不算错但都不精确，要写成精确的那个）。

### 6. 想改 `install.py` 的安装行为

注意两条已固化的安全约定，别回退：

1. **覆盖前必须备份**（`--force` 会把已有安装整体移成 `.bak-<时间戳>`，
   绝不直接删除）。用户可能在里面放了自己的东西。
2. **装完必须回验**：`verify()` 会读回 `SKILL.md`、解 frontmatter、
   核 `name` 与目录名一致、确认关键文件在位。只打印"成功"不算成功。
   改这函数后请补负向测试（造一个坏副本，确认它真的会报错）。

另外 `REPO_ONLY` 里的文件默认**不装给使用者**（CI、贡献指南、发布清单等，
对使用者是噪声）。裁剪后自检必须仍然全绿 —— 这是硬要求。

## 三、硬约束（破坏这些 = 破坏兼容性）

1. **不写绝对路径。** 所有路径相对 skill 根目录（`tools/`、`references/`）。
   换机器、换用户、换宿主都不该需要改任何东西。
2. **不引入第三方依赖。** Python 侧只用标准库。这是"装到任何宿主都能跑"的前提。
3. **命令统一写 `python3`**（Windows 无 `python3` 时用户自行换成 `python`，文档已注明）。
4. **不联网运行。** 所有查询必须离线完成，唯一例外是 `tools/etl/fetch_sources.py`
   （只在显式重建事实底座时才联网）。
5. **SKILL.md 的 `description` 不超过 1024 字符**（Claude Code 的硬上限）。
   目前 554，还有余量，但别把触发词堆到超限。
   `selftest.py` 的 E 类检查会核这个长度，超了自检直接红。
6. **文件用 LF 换行、UTF-8 编码。** 提交前确认没有引入 CRLF 或乱码。

## 四、提交前清单

- [ ] `python3 tools/selftest.py` → 全绿、退出码 0
- [ ] 若改过 API 事实 → 跑过 `tools/etl/rebuild.py`，且生成物已一起提交
- [ ] 无新增绝对路径、无新增第三方依赖
- [ ] `CHANGELOG.md` 已更新
- [ ] 新增文件是 UTF-8 + LF

## 五、报告问题

请带上：Seurat 版本、`sc_lint.py` 的完整输出（`--json`）、最小复现脚本。
如果是"校验器说某个函数不存在但它确实存在"，请给出该函数在哪个包的哪个文件里定义 ——
这通常是上游新增导出，需要重建事实底座。
