---
version: alpha
name: Command-center infographic — Frame (video / frame layer)
description: >
  Video-scale expansion of the 95 多Skill系统设计 DESIGN.md. Dark navy command-center canvas,
  cyan routing signal, amber priority, red conflict, green resolution. Inter + Noto Sans SC.
  Panels, nodes, and flow cards — not cream paper, not SaaS gradients.
unit: the frame — 1920×1080 primary
principle: atoms are sacred · composition is free · numbers come from the source

colors:
  canvas: "#07111f"
  background: "#07111f"
  panel: "#0f2236"
  cyan: "#37d5ff"
  amber: "#ffbe55"
  red: "#ff5a67"
  green: "#5ce38a"
  text: "#e8f1ff"

typography:
  kicker:   { fontFamily: "Inter, Noto Sans SC", px: 30, weight: 800, color: "{colors.cyan}" }
  headline: { fontFamily: "Inter, Noto Sans SC", px: 96, weight: 800, lineHeight: 1.08, tracking: "0" }
  h2:       { fontFamily: "Inter, Noto Sans SC", px: 74, weight: 800, lineHeight: 1.12, tracking: "0" }
  lead:     { fontFamily: "Inter, Noto Sans SC", px: 34, weight: 600, lineHeight: 1.55, color: "text@78%" }
  body:     { fontFamily: "Inter, Noto Sans SC", px: 28, weight: 750, lineHeight: 1.45 }
  caption:  { fontFamily: "Inter, Noto Sans SC", px: 28, weight: 650, lineHeight: 1.45, color: "text@68%" }
  node:     { fontFamily: "Inter, Noto Sans SC", px: 27, weight: 850 }
  flow:     { fontFamily: "Inter, Noto Sans SC", px: 42, weight: 800 }
  number:   { fontFamily: "Inter, Noto Sans SC", px: 124, weight: 950, lineHeight: 0.9, color: "{colors.cyan}" }

spacing:
  slide-pad: "86px 110px"
  gap: "44px"
  panel-pad: "36px"
  radius: "8px"

components:
  kicker:
    typography: "{typography.kicker}"
    color: "{colors.cyan}"
    description: "Eyebrow. Cyan, 30px, weight 800. Never a sentence."
  panel:
    backgroundColor: "{colors.panel}@82%"
    border: "1px solid {colors.cyan}@20%"
    rounded: "{spacing.radius}"
    shadow: "0 24px 80px rgba(0,0,0,0.25)"
    description: "Elevated technical surface. One panel job per block."
  node:
    minHeight: "124px"
    rounded: "{spacing.radius}"
    border: "1px solid {colors.text}@12%"
    backgroundColor: "{colors.text}@7%"
    typography: "{typography.node}"
    description: "Skill/table/step chip. .active = green border; .warn = red border."
  skill-row:
    minHeight: "74px"
    rounded: "{spacing.radius}"
    backgroundColor: "{colors.text}@6%"
    border: "1px solid {colors.text}@8%"
    typography: "{typography.body}"
    description: "List row with a 18px signal dot (cyan/amber/red/green)."
  request:
    width: "360px"
    height: "170px"
    rounded: "{spacing.radius}"
    backgroundColor: "{colors.cyan}@12%"
    border: "1px solid {colors.cyan}@42%"
    typography: "{typography.h2}"
    description: "The incoming request plate. One path, nothing else."
  flow-step:
    minHeight: "260px"
    rounded: "{spacing.radius}"
    backgroundColor: "{colors.panel}@86%"
    border: "1px solid {colors.cyan}@24%"
    description: "Four-up closer cards. Strong 42px label + muted caption."
  pipe-card:
    minHeight: "184px"
    rounded: "{spacing.radius}"
    typography: "{typography.body}"
    description: "Pipeline stage. Border tinted red/amber/green for state."
  badge:
    color: "{colors.green}"
    backgroundColor: "{colors.background}@92%"
    border: "1px solid {colors.green}@72%"
    rounded: "{spacing.radius}"
    description: "Resolution chip. Green only. One per frame max."
  big-number:
    typography: "{typography.number}"
    description: "Hero figure in cyan (or green when it is the resolved count)."
---

# Command-center infographic — Frame

## Overview

Dark navy command-center. The 95 多Skill系统设计 visual system applied to api-db-map: precise routing diagrams, modular nodes, crisp lines, restrained cinematic contrast. Calm, direct, architectural. Chinese engineering article register — not a SaaS ad, not cream-paper editorial.

**Key characteristics:**

- Ground `{colors.background}` `#07111f`; elevated surfaces `{colors.panel}` `#0f2236`.
- Cyan `#37d5ff` is routing and active signal; amber `#ffbe55` priority/warning; red `#ff5a67` conflict; green `#5ce38a` stable resolution.
- Text `{colors.text}` `#e8f1ff`. Headings heavy, compact line-height, **no negative letter spacing**.
- Inter + Noto Sans SC. 8px radius. 1px cyan-tinted borders. Soft drop only on panels.

## The Frame

- **Primary:** 1920×1080. Padding `86px 110px`.
- **Safe area:** keep load-bearing type inside the pad; no tiny labels.
- **Container:** `#root` is the frame. Ground is a 80px cyan grid at 5–6% plus two restrained radials (cyan 18/18, green 78/74) — copied from the 95 composition, not a decorative blob field.

## Colors

`{colors.background}` canvas. `{colors.panel}` cards. `{colors.cyan}` kickers, arrows, active borders, big numbers. `{colors.amber}` warning dots. `{colors.red}` conflict / warn nodes. `{colors.green}` resolved nodes, badges, the "3 not 20" figure. `{colors.text}` all copy. Lead and caption drop to 78% / 68% of text.

## Typography

Kicker 30 / H1 96 / H2 74 / lead 34 / row 28 / node 27 / flow strong 42 / big-number 124. Weight 800–950 on display, 600–750 on body. Never shrink a load-bearing line below 27px.

## Depth & Surface

Panel: 1px cyan@20% border + one `0 24px 80px` black@25% shadow. Nodes: 1px text@12% border, no shadow. No glassmorphism, no orbs, no purple gradients.

## Shapes

8px radius everywhere. 18px signal dots. Arrows are cyan glyphs, not illustrated.

## Frame Treatments

### 1 · Cover (hook · request + warn nodes)

Kicker + H1 + lead. Right: request plate + 2×3 warn nodes.

### 2 · Dual panel (pain / rule)

Two `{components.panel}` columns. Rows with signal dots.

### 3 · Node grid (fields / evidence units)

Six `{components.node}` cells. `.active` green when the unit is the product's rule.

### 4 · Big-number split (contrast)

Two panels, one figure each (cyan vs green).

### 5 · Pipeline (mechanism)

`{components.pipe-card}` + cyan arrows. Three or four stages.

### 6 · Four-up closer (T·01 / T·02 / T·03 / invoke)

`{components.flow-step}` row.

## Composition Rules

### Do

- Open every frame with a cyan kicker.
- One H1 or H2. Short lead. 3–6 nodes or rows.
- Signal color means state: cyan route, amber warn, red conflict, green resolved.
- Table names, paths, ops only from README / existing product preview.

### Don't

- No generic blue-purple gradients.
- No decorative blobs, orbs, bokeh, or stock-like backgrounds.
- No dense paragraphs copied from the README.
- No tiny labels that require pausing to read.
- No floating card stacks inside other cards.
- No cream paper, no EB Garamond, no coral spike — that is the other promo.

## Numerals & Claims (hard rule)

Never invent table names, ops, file:line, or counts. Known write ops from the product preview: `recording_task` UPDATE, `upload_session` UPDATE, `work_job` INSERT. Endpoint: `POST /v1/tasks/{task_id}/finalize`. Evidence is shown as the `file:line` pattern; do not fabricate paths.

## Known Gaps

- Motion out of scope here; 95's GSAP is kicker/title/panel stagger with `power3.out`, no bounce.
- Fonts staged locally: `assets/fonts/Inter-400.woff2`, `Inter-700.woff2`, `NotoSansSC-400.ttf`.
- No shipped preset. Brand truth is `DESIGN.md` (copied from the 95 project) plus this file.
