# archify-grade-diagram

## Notes

工单全部改同一份渲染模板，只能串行。无 GitHub remote，PR 无法创建。

## Decisions-so-far

- 接缝：`render_html.py` 产物 + Playwright 打开页面断言 DOM/SVG。
- 并行：不做 worktree 并行（会撞模板）。
- 测试：用户要求跳过，01 标 wontfix。

## Fog

无。
