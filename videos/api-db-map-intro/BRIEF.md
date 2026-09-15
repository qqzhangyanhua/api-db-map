---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "带着证据回答，不编表名"
destination: youtube
aspect: 1920x1080
language: zh
audience: 用 Agent 的后端开发者
length: 55s
angle: 系统图解
narration: no
capture: none
---

## Intent

产品介绍片，不是功能清单，也不是审讯冷开场。用 95 片那种深蓝 command-center 信息图，把 api-db-map 讲成一套秩序：Agent 不该猜表名；从 handler 追到表，每张表钉 `file:line`；一次跟踪画出架构、字段、时序三张图；证明不了就标 `uncertain`。观众是用 Agent 的后端开发者。无口播，画面上的字就是解说。

## Assets

- `/Users/zhangyanhua/todos/AI智能体系列/文章/95_多Skill系统冲突设计_video/DESIGN.md` — 视觉系统（深蓝底、青/琥珀/红/绿信号、Inter + Noto Sans SC）。本片 `frame.md` 的品牌真源。
- `/Users/zhangyanhua/todos/AI智能体系列/文章/95_多Skill系统冲突设计_video/index.html` — 构图参考（kicker / 面板 / 节点 / 流程卡），不抄文案。

事实以仓库 README 与现有预览图为准：接口示例 `POST /v1/tasks/{task_id}/finalize`，表包括 `recording_task`、`task_grant`、`upload_session`、`upload_part`、`work_job`。不要改口成 `/api/orders`。

## Customizations

- 无口播 + 轻配乐（克制技术向 BGM）。不做字幕轨：字在画面上。
- 纯信息图，不上产品截图、不重画产品页。
- 设计不走 shipped preset 的奶油纸气质；`frame.md` 按 95 `DESIGN.md` 展开。
- 新工程，不覆盖 `videos/api-db-map-promo/`。

## Notes

- 55 秒、无旁白：每幕 kicker + 一句标题 + 3–6 个节点，密度对齐 95 片。
- 数字、表名、接口路径必须来自 README 或上述预览图，禁止编造。
- 调用口令：`用 api-db-map` / `/api-db-map`。显式调用，提到表或接口不会自动触发。
- 安装：`npx skills add qqzhangyanhua/api-db-map`。
