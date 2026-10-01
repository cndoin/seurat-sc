# CONTRIBUTING

改这个技能前，先读这一页。核心原则只有一条：**技能里写的每一个 API 事实，都必须能溯源到上游源码。**
凭印象写函数签名 = 引入幻觉，这是这个技能存在的理由，别把它破坏掉。

## 一、改东西之前

```bash
python3 tools/selftest.py      # 必须全绿、退出码 0
```

这是基线。改完之后再跑一次，仍然全绿（退出码 0）才允许提交。

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

## 三、硬约束（破坏这些 = 破坏兼容性）

1. **不写绝对路径。** 所有路径相对 skill 根目录（`tools/`、`references/`）。
   换机器、换用户、换宿主都不该需要改任何东西。
2. **不引入第三方依赖。** Python 侧只用标准库。这是"装到任何宿主都能跑"的前提。
3. **命令统一写 `python3`**（Windows 无 `python3` 时用户自行换成 `python`，文档已注明）。
4. **不联网运行。** 所有查询必须离线完成，唯一例外是 `tools/etl/fetch_sources.py`
   （只在显式重建事实底座时才联网）。
5. **SKILL.md 的 `description` 不超过 1024 字符**（Claude Code 的硬上限）。
   目前 672，还有余量，但别把触发词堆到超限。
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
