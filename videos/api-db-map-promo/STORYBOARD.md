---
format: 1920x1080
duration: 45s
message: "带着证据回答这个接口改了哪些表，不编表名"
arc: Demo Loop
audience: 用 Agent 的后端开发者
mode: collaborative
music: quiet editorial underscore, paper and ink, no drop
---

## Video direction

palette: cream `#FAF9F5` ground, ink `#141413` voice, coral `#CC785C` once per frame (the ✱ kicker), warm navy `#181715` only on the command surface. Type: display = EB Garamond / Songti SC; body = Inter / PingFang SC; mono = JetBrains Mono.

motion: long-tail `power3` settle; VO-paced sequential reveal; no bounce; no breathing; hold still after the last cue, subtle jitter at most. Caption band: keep content in the top ~83%.

rhythm: Frame 1 types then holds the question. Frame 2 is the busiest (three pins). Frame 3 is the breather after the zoom-out locks. Frame 4 types the command and holds the caret.

never: feature bullets, invented table names, `/api/orders`, two coral moments in one frame, front-load-then-freeze, screensaver drift.

## Frame 1 — 哪几张表

- scene: 暖纸上打出「这个接口，改了哪些表？」路径随后打出
- voiceover: "这个接口，改了哪些表？"
- duration: 8s
- poster: 5s
- transition_in: cut
- status: animated
- src: compositions/frames/01-which-tables.html
- type: hook
- persuasion: Rhetorical question
- beat: curiosity + tension
- blueprint: typewriter-reveal (Adapt)
- focal:
- roles:
- sfx: typing
- asset_candidates:

narrativeRole: 用审查里会问出口的那句话开场，先给「为什么要看」再给路径。
keyMessage: 你真正想知道的是：这个接口动了哪些表。

先打出结果语言，不打产品名。路径 `POST /v1/tasks/{task_id}/finalize` 作为被审查的那一条出现，不是功能介绍。

Adapt: keep type-on with caret; skip collapse-to-brand (name waits for Frame 4). Confirmed layout: kicker + display question lower-left, path under it.

Scene 1 (0.0–1.2s): cream field; ✱ REVIEW kicker already seated top-left. Empty headline slot lower-left, asymmetric 70/30. Blinking caret at the first character.
Scene 2 (1.2–5.0s): 「这个接口，改了哪些表？」types on character-by-character. Display role, sentence-case, top 83%.
Scene 3 (5.0–8.0s): path types as a mono sub-line under the question. Hold still; caret blinks only. No collapse, no product name.

## Frame 2 — 证据钉上

- scene: T·02 表卡片作底，三条写表证据钉上 recording_task、upload_session、work_job
- voiceover: "不猜。每一张表，一条证据。"
- duration: 14s
- poster: 10s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-evidence-pins.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: skepticism → clarity
- blueprint: agent-progress-theater (Adapt)
- focal: assets/t02-fields.jpg
- roles: t02-fields = background (dim ~40%)
- sfx: ping
- asset_candidates: assets/t02-fields.jpg — T·02 表与字段关系，钉表背景

narrativeRole: 把「带着证据、不编表名」钉成可见动作，这是整条片子的证明。
keyMessage: 每张被动过的表都有 file:line，不是猜的。

只钉截图里能看见的写：`recording_task` UPDATE、`upload_session` UPDATE finalized、`work_job` INSERT。证据条用 `backend/app.py:297`。不编第四张表。

Adapt: keep receipt cascade + state mutation; trigger is the spoken 「不猜」 not a menu click. Confirmed layout: left chips, right T·02 plate. Camera static.

Scene 1 (0.0–2.5s): T·02 full-bleed dim ~40%. ✱ EVIDENCE kicker + display 「不猜。」 enter left via spring-pop. Asymmetric 42/58. Only this line on the left.
Scene 2 (2.5–6.0s): as VO says 「每一张表，一条证据」, working accent spinner + status 「tracing…」 (finite). First chip recording_task / UPDATE / backend/app.py:297 slides in. Badge flips to check.
Scene 3 (6.0–10.0s): upload_session then work_job cascade in and check off, one per cue. Spinner dies when the last check lands.
Scene 4 (10.0–14.0s): three checked chips + dim T·02 hold still. Subtle jitter on the last check only.

## Frame 3 — 时序证物

- scene: 从一条写操作特写拉出完整 T·03，蓝读橙写
- voiceover: "读哪些列。写哪些列。一次请求，全在这张图。"
- duration: 14s
- poster: 9s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/03-sequence-exhibit.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: clarity + control
- blueprint: zoom-out-workspace-reveal (Adapt)
- focal: assets/t03-sequence.jpg
- roles: t03-sequence = cutout
- sfx: whoosh
- asset_candidates: assets/t03-sequence.jpg — T·03 接口时序图，主证物

narrativeRole: 主证物。证明不只是表名，连读写列和调用链都在。
keyMessage: 一次请求里谁调用谁、读哪些列、写哪些列，一张图看完。

真图当证物，不重画。从橙条 UPDATE 特写拉到全图。

Adapt: keep ONE decelerating zoom-out as the signature. Tight open on the orange UPDATE bar, pull back to the full T·03 plate. Confirmed layout: exhibit dominates, caption under it.

Scene 1 (0.0–3.0s): T·03 cropped tight on the orange UPDATE finalized bar. ✱ EXHIBIT kicker. VO 「读哪些列」— a blue SELECT bar is the only extra cue. Centered, ≥40% canvas.
Scene 2 (3.0–8.5s): VO 「写哪些列」— ONE decelerating zoom-out to the full sequence. Orange write bars stay the focal; rest of the plate comes into frame. Signature move.
Scene 3 (8.5–14.0s): lock at full plate. Caption 「一次请求，全在这张图。」per-word reveal. Hold still. No second camera move.

## Frame 4 — 用 api-db-map

- scene: 命令打出，入口页在边上一闪
- voiceover: "对 Agent 说这一句。"
- duration: 9s
- poster: 6s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/04-invoke.html
- type: cta
- persuasion: Friction reduction
- beat: motivation
- blueprint: prompt-type-submit-generate (Adapt)
- focal: assets/index.jpg
- roles: index = supporting
- sfx: key-press
- asset_candidates: assets/index.jpg — 入口页，收尾闪一下

narrativeRole: 收成可执行的一句，而不是功能清单。
keyMessage: 对 Agent 说「用 api-db-map 分析」就能拿到这张图。

命令：`用 api-db-map 分析 POST /v1/tasks/{task_id}/finalize`。产品名第一次出现。

Adapt: keep CTA install-command end card — headline demotes, navy terminal pill types the invoke. Confirmed layout: command left, index plate right.

Scene 1 (0.0–2.0s): ✱ INVOKE + display 「对 Agent 说这一句。」spring-pop. Asymmetric 70/30. Index plate still empty/hidden.
Scene 2 (2.0–6.5s): headline demotes (scale down, lifts). Navy code-surface stretches in. Command types with caret: 用 api-db-map 分析 POST /v1/tasks/{task_id}/finalize.
Scene 3 (6.5–9.0s): index.jpg supporting plate fades in on the right. Hold; only the caret blinks. No submit, no second command.
