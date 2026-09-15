---
format: 1920x1080
duration: 55s
message: "带着证据回答，不编表名"
arc: PAS
audience: 用 Agent 的后端开发者
mode: collaborative
music: restrained technical command-center underscore, dark and dry, no drop, no vocal
---

## Video direction

palette: canvas `#07111f`, panel `#0f2236`, text `#e8f1ff`, cyan `#37d5ff` routing, amber `#ffbe55` warn, red `#ff5a67` conflict, green `#5ce38a` resolved. Type roles: kicker / display / lead / node from frame.md (Inter + Noto Sans SC). 8px radius, 1px cyan-tinted borders.

motion: 95-style sequential entrance — kicker, then title, then lead, then cards/nodes stagger — stretched across the shot so the last card lands in the back half. Smooth long-tail `power3`. No bounce, no breathing, no back-half camera push. Hold still after the last cue; subtle jitter at most. Caption band: content in the top ~83%. No voiceover: each on-screen line is its own reveal cue.

rhythm: Frame 2 and Frame 7 are breathers (titlecard / still rule). Frame 5 is the busiest (three receipt rows). Frame 8 types the command then holds the caret.

never: cream paper, coral spike, EB Garamond, purple-blue gradients, orbs, invented table names / ops / file paths, `/api/orders`, product screenshots, front-load-then-freeze, screensaver drift.

## Frame 1 — 哪几张表

- scene: 深蓝底上打出审查会问的那句，右边是被审的那条接口
- voiceover:
- duration: 5s
- poster: 3s
- transition_in: cut
- status: animated
- src: compositions/frames/01-which-tables.html
- type: hook
- persuasion: Rhetorical question
- beat: curiosity + tension
- blueprint: compose
- rules: spring-pop-entrance, dynamic-content-sequencing, center-outward-expansion
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 用审查里会问出口的那句话开场，先给「为什么要看」。
keyMessage: 你真正想知道的是：这个接口动了哪些表。

compose: 95-style sequential type beats on a confirmed sketch (kicker + title + lead over request plate left / 2×3 warn nodes right). No token-swap, no logo payoff.

Scene 1 (0.0–1.0s): navy field; kicker enters via spring-pop entrance (`spring-pop-entrance`). Asymmetric 45/55. Title slot empty.
Scene 2 (1.0–2.2s): title 「这个接口到底改了哪些表？」per-word staggered reveal (`dynamic-content-sequencing`). Display role. Top 83%.
Scene 3 (2.2–3.2s): lead 「Agent 不该猜表名。」spring-pop. Request plate `POST /v1/tasks/{task_id}/finalize` slides in from the left (`spring-pop-entrance`).
Scene 4 (3.2–5.0s): six warn nodes 「？」cascade via cluster→outward expansion (`center-outward-expansion`). Hold still. No product name.

## Frame 2 — 不编表名

- scene: 一句话定论落在画面正中：带着证据回答，不编表名
- voiceover:
- duration: 5s
- poster: 3s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-the-rule.html
- type: product_intro
- persuasion: Value claim
- beat: clarity
- blueprint: titlecard-reveal (Adapt)
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 在第二拍落地 brief 的那句话，后面全是它的证据。
keyMessage: 带着证据回答，不编表名。

Adapt: keep one restrained reveal then still hold. Three green nodes are the landing, not a logo.

Scene 1 (0.0–1.2s): navy field; kicker 「一条硬规则」spring-pop (`spring-pop-entrance`). Centered.
Scene 2 (1.2–2.8s): title 「带着证据回答，不编表名」slide-up (`spring-pop-entrance`). Display role.
Scene 3 (2.8–5.0s): lead, then three green nodes `file:line` / 不编表名 / `uncertain` stagger (`dynamic-content-sequencing`). Hold still. No product name.

## Frame 3 — 猜表名会怎样

- scene: 双栏面板，左边三种翻车，右边三种缺失
- voiceover:
- duration: 6s
- poster: 3s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-guessing.html
- type: pain_point
- persuasion: Pain agitation
- beat: frustration
- blueprint: comparison-split (Adapt)
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 说明为什么「猜」过不了审查，把规则反面说清楚。
keyMessage: 没证据的表名，审查会停在这里。

Adapt: keep two equal-weight panels from opposite sides. Drop 3D book-open tilt (95 is flat). Signature is the mirrored dual panel.

Scene 1 (0.0–1.2s): kicker + title enter (`spring-pop-entrance`). Split-screen empty.
Scene 2 (1.2–3.4s): left panel slides from left, three rows cascade (`dynamic-content-sequencing`): 编了不存在的表 / 漏了真正被写的表 / 没有 file:line.
Scene 3 (3.4–6.0s): right panel slides from right, three rows cascade: 没人管「查了哪些」 / 「改了哪些」 / 「能不能确定」. Hold. No fourth row.

## Frame 4 — 从 handler 走到表

- scene: 四段管道，Handler → Service → Mapper/SQL → Table
- voiceover:
- duration: 6s
- poster: 4s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-trace.html
- type: feature_showcase
- persuasion: Mechanism
- beat: intrigue → control
- blueprint: spatial-pan-stations (Adapt)
- focal:
- roles:
- sfx: whoosh
- asset_candidates:

narrativeRole: 证明答案来自代码路径，不是模型记忆。
keyMessage: 从 handler 往下走到表，不从印象里掏表名。

Adapt: keep sequential station reveals. Drop virtual-camera pan (95 is a flat pipe). Stations light left-to-right.

Scene 1 (0.0–1.2s): kicker + title (`spring-pop-entrance`). Full-width strip empty.
Scene 2 (1.2–4.4s): four pipe-cards Handler → Service → Mapper / SQL → Table reveal left-to-right (`dynamic-content-sequencing`); cyan arrows after each card.
Scene 3 (4.4–6.0s): last card Table holds. Stillness. Not an install step.

## Frame 5 — 证据钉上

- scene: 已知的三张写表，每张一行 op，右侧统一钉 file:line
- voiceover:
- duration: 7s
- poster: 4s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-evidence.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: skepticism → clarity
- blueprint: agent-progress-theater (Adapt)
- focal:
- roles:
- sfx: ping
- asset_candidates:

narrativeRole: 把「带着证据」变成可见的三行收据，这是整条片子的证明。
keyMessage: 每张被动过的表都有证据，不是猜的。

Adapt: keep receipt cascade + check-off. Trigger is the title, not a menu click. Only three verified writes.

Scene 1 (0.0–1.4s): kicker + title + muted path `POST /v1/tasks/{task_id}/finalize` (`spring-pop-entrance`). Panel empty.
Scene 2 (1.4–3.2s): first row recording_task · UPDATE + green file:line badge (`dynamic-content-sequencing`).
Scene 3 (3.2–5.0s): upload_session · UPDATE checks in.
Scene 4 (5.0–7.0s): work_job · INSERT checks in. Hold three rows. Do not invent paths. Do not add task_grant / upload_part.

## Frame 6 — 三张图

- scene: 三张流程卡，T·01 / T·02 / T·03
- voiceover:
- duration: 7s
- poster: 4s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/06-three-views.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: clarity + control
- blueprint: grid-card-assemble (Adapt)
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 一次跟踪的产出是三张图，不是一句口头答案。
keyMessage: 架构、字段、时序，一次请求看完。

Adapt: keep staggered card cascade. Three flow-steps, no zoom-out to a vaster wall. No screenshots.

Scene 1 (0.0–1.4s): kicker + title (`spring-pop-entrance`). Triptych empty.
Scene 2 (1.4–5.2s): T·01 / T·02 / T·03 cards cascade (`center-outward-expansion`): 影响架构图 · 表与字段关系 · 接口时序图, each with its one-line caption.
Scene 3 (5.2–7.0s): three cards hold. Stillness.

## Frame 7 — 标 uncertain

- scene: 三条降级规则，最后一枚绿色徽章
- voiceover:
- duration: 5s
- poster: 3s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-uncertain.html
- type: benefit_highlight
- persuasion: Risk reversal
- beat: trust
- blueprint: compose
- rules: spring-pop-entrance, dynamic-content-sequencing
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 泼冷水。产品可信，是因为它会停下来。
keyMessage: 证明不了就标 uncertain，不要假装知道。

compose: sequential statement beats on a bare panel, then a green badge. Skip logo slam. Breather frame.

Scene 1 (0.0–1.2s): kicker + title (`spring-pop-entrance`).
Scene 2 (1.2–3.6s): three rows land one by one (`dynamic-content-sequencing`): 拼接 SQL → uncertain / 动态表名 → uncertain / 高风险猜测 → 停下.
Scene 3 (3.6–5.0s): green badge 「代码证明不了的，标 uncertain」spring-pop. Hold.

## Frame 8 — 用 api-db-map

- scene: 产品名第一次出现，打出开口令
- voiceover:
- duration: 7s
- poster: 5s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-invoke.html
- type: cta
- persuasion: Friction reduction
- beat: motivation
- blueprint: prompt-type-submit-generate (Adapt)
- focal:
- roles:
- sfx: key-press
- asset_candidates:

narrativeRole: 收成可执行的一句。
keyMessage: 对 Agent 说「用 api-db-map」才跑。

Adapt: keep install-command end card — headline seated, command types with caret. No submit, no generated answer. Product name first appearance.

Scene 1 (0.0–1.6s): kicker + title 「说这一句，才跑」+ muted 「提到表或接口，不会自动触发」(`spring-pop-entrance`). Asymmetric 40/60.
Scene 2 (1.6–3.2s): request plate 「用 api-db-map」spring-pop left.
Scene 3 (3.2–7.0s): command types with caret (`discrete-text-sequence` + `context-sensitive-cursor`): 用 api-db-map 分析 POST /v1/tasks/{task_id}/finalize. Hold; only caret blinks. No submit.

## Frame 9 — 结论

- scene: 四个流程卡收束整条片子
- voiceover:
- duration: 7s
- poster: 4s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-close.html
- type: branding
- persuasion: Rule of three
- beat: peace of mind
- blueprint: titlecard-reveal (Adapt)
- focal:
- roles:
- sfx: none
- asset_candidates:

narrativeRole: 把机制收成四个词，回扣那句 message。
keyMessage: 带着证据回答，不编表名。

Adapt: keep restrained title then hold. Four closer cards are the lockup, not a logo. Final frame may settle, no exit tween required beyond hold.

Scene 1 (0.0–1.4s): kicker + title 「核心不是再猜一张表」(`spring-pop-entrance`).
Scene 2 (1.4–2.8s): lead 「而是让接口到表的路径可被审查。」
Scene 3 (2.8–7.0s): four flow-steps 追代码 / 钉证据 / 画三图 / 标 uncertain cascade (`center-outward-expansion`). Hold to end.
