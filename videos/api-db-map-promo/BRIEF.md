---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "带着证据回答这个接口改了哪些表，不编表名"
destination: youtube
aspect: 1920x1080
language: zh
audience: 用 Agent 的后端开发者
length: 45s
angle: code-review-interrogation
style_preset: code-editorial
narration: minimal
capture: none
---

## Intent

代码审查问答，不是功能清单。冷开场只问一句：`POST /v1/tasks/{task_id}/finalize` 改了哪些表。沉默半拍后，`file:line` 证据条钉上表名。卖点是带着证据回答、不编表名。气质是暖奶油纸上的审查笔记，不是 SaaS 广告。

## Assets

- `/Users/zhangyanhua/AI/skills/api-db-map/assets/preview-t03-sequence.jpg` — T·03 接口时序图；主证物。
- `/Users/zhangyanhua/AI/skills/api-db-map/assets/preview-t02-fields.jpg` — T·02 表与字段关系；钉表背景。
- `/Users/zhangyanhua/AI/skills/api-db-map/assets/preview-index.jpg` — 入口页；收尾闪一下。

事实以这三张图为准：接口是 `POST /v1/tasks/{task_id}/finalize`，表包括 `recording_task`、`task_grant`、`upload_session`、`upload_part`、`work_job`。不要改口成 `/api/orders`。

## Customizations

- 证据条 callout：把 `file:line` 钉到表名上，不配功能 bullet。
- 用户截图当证物贴进画面，不重画产品页。
- 字幕主导、极短冷口播（沉默半拍是概念的一部分）。
- 设计预设 code-editorial（暖纸审查笔记）。无官网，不爬站。

## Notes

- 45 秒塞不下三张图都当主画面：主证物 T·03，T·02 当钉表背景，入口页只在收尾闪一下。
- 数字、表名、接口路径必须来自上述截图或仓库 README，禁止编造。
- 口播音色开工后选。
- HeyGen 未登录，用户选择离线：Kokoro 口播 + MusicGen 配乐。
