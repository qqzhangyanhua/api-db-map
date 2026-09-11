# 01 · 测试基建与夹具

Type: task
Status: wontfix
Blocked by:

搭 Playwright + `pnpm test`，加入 `sample-ir.json` 之外的两份小 IR（13 表；超 10 字段 + 无 op 回程）。不断言图，只保证能渲染出 HTML。

Spec: `.scratch/archify-grade-diagram/spec.md` · Testing Decisions / Further Notes 第一步。

## Answer

用户明确不要测试。Playwright / 夹具 / `package.json` 已撤掉。
