# Visualization spec — api-db-map

Render from `api-db-map.json` (see references/ir-schema.md). Primary artifact is a single self-contained HTML file. Mermaid is fallback only.

## Archify visual system

Match https://github.com/tt-a1i/archify chrome, not a pixel clone of CloudFront infra.

- Default: `classic` + `dark` (neutral slate chrome, matches archify's own default)
- Presets, picked from a `风格` dropdown (swatch + name + one-line purpose, matches archify's own picker):
  - **经典 Classic** — 稳定的技术默认风格 (stable, neutral technical default)
  - **信号流 Signal Flow** — 突出动态流向 (emphasizes read/write flow direction)
  - **蓝图 Blueprint** — 工程评审 (squared corners, cool drafting palette, for engineering review)
  - **编辑风格 Editorial** — 适合发布与上线说明 (warm paper, for release notes / launch docs)
- Theme toggle: 浅色 (light) / 深色 (dark), `localStorage`-backed, `T` key shortcut. `S` key cycles presets.
- Font: JetBrains Mono + PingFang SC / Noto Sans SC
- Nodes: translucent semantic fill + 1.5px stroke, 12px radius, no drop shadow
- API = backend emerald, Table = database violet, Write = cloud amber, FK = security rose
- Canvas card + T·01 pill + caption + legend, like Archify's architecture / workflow / sequence pages

## When to load this file

Load after impact IR is written. Do not invent layout rules that contradict this spec.

## Output files

- `api-db-map.html` — interactive, screenshot-style
- `api-db-map.md` — summary table + mermaid fallback
- Keep `api-db-map.json` next to them

Use `scripts/render_html.py` when present. Otherwise copy `assets/diagram.template.html`, replace `/*__IR__*/{}` with the JSON.

## Chrome (must match the user's figure)

- Canvas: cream paper `#F6F3EC` with 24px dot grid `#E6E1D6`
- Cards: white `#FFFEFB`, 12px radius, 1.5px colored stroke, no drop shadow
- Group boxes: 2px dashed rounded rect, 16px padding
- Font: `"PingFang SC","Noto Sans SC","Segoe UI",system-ui,sans-serif`
- Title pills top-left of each panel: `T · 01` / `T · 02` / `T · 03`
- Caption under each panel: Chinese title + one-line description
- Footer legend with colored dots and counts

## Color tokens (Archify vocabulary)

Default page: `data-preset="classic"` + `data-theme="dark"`. Also ship Signal Flow / Blueprint / Editorial + light toggle. Tokens live as CSS variables in `assets/diagram.template.html`.

| Role | Light stroke / fill | Dark stroke | Use |
|---|---|---|---|
| API / endpoint | `#0891B2` / `rgba(34,211,238,.15)` | `#22D3EE` | frontend cards |
| Service / handler | `#059669` / `rgba(52,211,153,.18)` | `#34D399` | backend |
| Table | `#7C3AED` / `rgba(167,139,250,.20)` | `#A78BFA` | database cards |
| Read / SELECT | `#1D4ED8` | `#67E8F9` | dashed edges, R badge |
| Write | `#C2410C` / `#EA580C` | `#FB923C` | solid edges, W badge |
| FK / field link | `#E11D48` | `#FB7185` | field-to-field |
| Uncertain | `#64748B` | `#94A3B8` | dashed slate |
| Module group | `#D97706` dashed lane | `#FBBF24` | dashed group |

Typography: `"JetBrains Mono", "Noto Sans Mono CJK SC", "PingFang SC", ui-monospace, monospace`.
Nodes: 10–12px radius, 1.5px stroke, no drop shadow. Grid 24px. Caption + legend under canvas.
Toolbar: T·01/T·02/T·03 + 搜索框 + R/W chips + 查找 (`/`) + 路径追踪 (`R`) + 风格 dropdown (经典/信号流/蓝图/编辑风格) + 浅色/深色 theme toggle. Zoom control docks to the viewport corner, independent of the toolbar.

Op badges on table cards: `R` read color, `W` write color, `RW` amber.

## T-01 影响架构图

Question: which APIs touch which tables.

- Left column: endpoint cards. Title = `METHOD`, subtitle = path. Badge = table count.
- Right column: table cards grouped by `module` or `schema` inside a dashed group box.
- Edge from endpoint to table. Label = op (`SELECT` / `INSERT` / …). Solid = write, dashed = read, amber = both.
- Uncertain edges use slate dashed + `?`.
- Click an API to dim unrelated tables and edges.

Caption:
- 标题：影响架构图
- 说明：接口到数据表的读写边界——谁查谁、谁改谁，按模块铺开。

## T-02 表与字段关系图

Question: how tables and fields connect, and which fields this API actually uses.

- Each table is a card: header (table name + R/W badges) + field rows.
- PK row: bold + `PK`. FK row: tinted rose + `→ table.col`.
- Draw edges from FK field to referenced PK field (field grain, not table grain).
- Edge label = cardinality `1:1` / `1:N` / `N:1` / `N:M`. Color = FK rose. `source=join|inferred` uses dashed stroke.
- When an endpoint is selected: fields in `fields_read` or `fields_written` stay full opacity; unused fields go to 0.35. Written fields get an orange tick; read fields a blue tick.

Caption:
- 标题：表与字段关系图
- 说明：主外键与字段级连线——选中接口后高亮实际读写字段，其余淡化。

## T-03 接口时序图

Question: for one API, in what order do DB ops happen.

- Participants across the top: Client, Controller, Service, then one lifeline per touched table (and Cache if present).
- Messages from `endpoints[].sequence`.
- Activation bar color: R blue, W orange, RW amber.
- Label includes SQL verb + columns when known.
- Default to the first endpoint; clicking a T-01/list row switches T-03.

Caption:
- 标题：接口时序图
- 说明：一次请求里谁调用谁、何时落库、读哪些列、写哪些列。

## Interaction

- Search box filters endpoints by path / method / table name.
- Method chips: GET POST PUT PATCH DELETE.
- R / W / RW toggles hide edges.
- Hover field: highlight that field's FK path.
- **Zoom**: bottom-right `−`/`100%`/`+` control (fixed to viewport), `+`/`-`/`0` keys. Scales via CSS `zoom` so the browser's own page scroll handles panning — no custom pan/drag code needed.
- **Detail / evidence panel** (right-side drawer): clicking an endpoint card shows its handler `file:line` plus every table touch with op, confidence, `fields_read`/`fields_written`, and the raw `evidence` string (e.g. `OrderMapper.xml:88`). Clicking a table card shows every endpoint that touches it with the same evidence. Has a "复制链接" button (see deep-linking below).
- **Node finder** (`/` key or 查找 button): a centered overlay with live search over all endpoints and tables (substring match on id/path/handler/module), arrow-key navigation, Enter to jump — sets the endpoint filter or opens the table detail panel and closes itself.
- **Route probe / path tracing** (`R` key or 路径追踪 button): pick a start and end node (endpoint or table, via the node finder in a special picking mode) and it runs BFS over the bipartite endpoint↔table graph to find the shortest path, then renders it as a chip chain. Step controls (prev/play/next/总览) walk the path one node at a time, highlighting the current node (`.path-step`) vs the rest of the path (`.path`) on the diagram; dims everything off-path. Useful for "what else touches the same table as this endpoint" / "how are these two tables coupled through the API layer" questions.
- **URL deep-linking**: current tab, selected endpoint, selected table, and an active route are all encoded into `location.hash` (`#tab=..&ep=..&tbl=..&route=..`) via `history.replaceState` (never `pushState`, so it never pollutes browser history). Reloading or sharing the URL restores the same state. Copy-link buttons on the detail panel and route panel put `location.href` on the clipboard (with an `execCommand` fallback for browsers that block Clipboard API on `file://`).

## Fallback mermaid (api-db-map.md)

T-01: `flowchart LR` with endpoint and table subgraphs.
T-02: `erDiagram` plus a short field-mapping table.
T-03: `sequenceDiagram`.

Do not use mermaid as the primary deliverable when HTML can be written.

## Layout rules (keep readable)

- Prefer column layout over force layout for T-01/T-02.
- Max ~12 table cards on T-01 before grouping-only (drill into module).
- Field list: show PK + FK + touched fields first; collapse the rest behind `+N more` if > 10.
- Never invent tables or fields to make the diagram prettier.
- Uncertain items stay visible and labeled, not dropped.
