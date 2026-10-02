---
name: Bug 报告
about: 校验器漏报/误报、自检假绿、工具崩溃、安装失败
title: "[bug] "
labels: bug
---

## 一句话说明

<!-- 例：sc_lint 把一个真实存在的参数判成了幻觉 -->

## 属于哪一类

- [ ] **漏报**：幻觉函数/参数没被拦下（最严重，优先处理）
- [ ] **误报**：正常代码被判成幻觉
- [ ] **自检假绿**：交付物残缺但 `selftest.py` 仍返回 0
- [ ] **崩溃**：工具吐 traceback 或挂死，而不是给可读错误 + 非零退出
- [ ] **安装**：`install.py` 装不上 / 装完用不了
- [ ] **文档错**：文档里的数字/命令/路径与实际不符
- [ ] 其它

## 环境

- 技能版本（`SKILL.md` 的 `version`，或 `git rev-parse HEAD`）：
- 操作系统：
- Python 版本（`python3 --version`）：
- 有 R 吗（`Rscript --version`，没有就写"无"）：
- 事实底座版本：Seurat 　／ SeuratObject （见 `whitelist.json` 的 `generated_from`）

## 最小复现

```
（贴上产生问题的 R 脚本或命令）
```

## 期望 vs 实际

- 期望：
- 实际：

## 完整输出

```
（贴 `python3 tools/sc_lint.py your.R --json` 的完整输出，或出错命令的完整 stdout/stderr）
```

> 如果是「校验器说某个函数不存在，但它确实存在」：
> 请给出该函数**在哪个包的哪个文件里定义**（如 `Seurat/R/xxx.R`）。
> 这种情况通常是上游新增导出，需要重建事实底座（见 CONTRIBUTING）。
