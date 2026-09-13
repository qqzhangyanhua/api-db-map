---
name: api-db-map
description: Trace backend APIs to the tables and fields they read or write, then render architecture, field-relation, and sequence diagrams (接口查了哪些表, 改了哪些表, 表关联, 字段关系). Explicit-invocation only — call this skill only when the user says "api-db-map" or 「用 api-db-map」.
metadata:
  version: "1.1"
  type: workflow
---

# API → DB Map

Analyze a backend codebase and answer, with evidence, which HTTP APIs read or write which database tables and fields. Then render three diagrams.

If the code does not prove an access, mark it `uncertain` and keep going.

Load [references/ir-schema.md](references/ir-schema.md) before step 3 and emit that shape from then on.

## Output contract

Always produce artifacts under the project root or a path the user named (default `./api-db-map-out/`). Incremental: a new run adds timestamped files and does not replace earlier ones.

```
api-db-map-out/
├── registry.json
├── index.html                          ← entry page (search by path or table)
├── GET__api__orders__-id-/
│   ├── 2026-09-13.json
│   ├── 2026-09-13.html
│   └── 2026-09-13.md
└── _project_overview/                  ← when more than one endpoint is deep-traced
    └── 2026-09-13.html
```

Directory name: `METHOD` + path with `/` → `__` and `{id}` → `-id-` (`GET /api/orders/{id}` → `GET__api__orders__-id-`).
Stamp: `YYYY-MM-DD`; if that `.html` already exists, `YYYY-MM-DDTHH-MM`.

`index.html` is what you open first. Render HTML with `scripts/render_html.py`. Never hand-write the HTML.

Reply in the user's language. If they wrote Chinese, diagram chrome is Chinese (影响架构图 / 表与字段关系 / 接口时序图).

## Workflow

### 1. Scope

Ask only if the project root is ambiguous. Accept optional filters:

- one route (`GET /api/orders/{id}`)
- one module / package
- an OpenAPI / Swagger file
- a live DB URL for schema ground truth (optional, SELECT-only)

The **deep-trace set** is the endpoints this run walks to the database. Freeze it as concrete `METHOD path` ids:

- Named route → that endpoint only
- Named module / OpenAPI slice → endpoints in that slice; if more than 12, take 12 (write methods first) and say so
- No filter → inventory first (step 4), then at most 12. Prefer POST/PUT/PATCH/DELETE over GET. Skip health/metrics unless the user asked.

Untraced inventory ids go on a **coverage list**. They are not rendered and do not belong in the IR `endpoints[]` that you hand to the renderer.

Done when the deep-trace set is an explicit list of ≤12 `METHOD path` values (or fewer if the user named fewer).

### 2. Detect stack

Run `python scripts/detect_stack.py <project-root>`.

Load **only** the path in the script's `playbook` field (file plus `#` anchor, if any). Also load [references/raw-sql.md](references/raw-sql.md).

If detection is weak, ask one clarifying question (framework + ORM), then proceed with filename heuristics + SQL strings rather than stalling.

### 3. Extract schema (ground truth first)

Priority. A source is complete when it yields tables, columns, and primary keys — stop there for those. If it has no foreign keys or `desc`, keep walking later sources for FK and `desc` only.

1. Live DB `information_schema` / `pg_catalog` — SELECT-only, never write
2. Migrations / DDL (Flyway, Liquibase, Alembic, Prisma, Django, `*.sql`)
3. ORM models (`@Entity`, Prisma `model`, SQLAlchemy, Django Model, GORM tags)
4. Infer from SQL strings last, and mark those tables `inferred`

Write tables, columns, PK/UK, FK, nullability, module guess (package / schema name).

Capture a human-readable `desc` per column when the same source exposes one — see "Field descriptions" in [references/ir-schema.md](references/ir-schema.md). Leave it unset rather than guessing from the column name.

### 4. Inventory APIs

Collect `{method, path, handler file, function, line}` from routers, controllers, and OpenAPI if present. Deduplicate by `METHOD path`. Skip health/metrics unless the user asked.

Then freeze the deep-trace set with the step 1 rule. Remaining ids go on the coverage list.

Done when every router/controller in scope is in the inventory or skipped as health/metrics, and the deep-trace set is ≤12.

### 5. Trace handler → database

Walk only the deep-trace set. From each handler, walk callees 2–4 levels (controller → service → repo / mapper). Follow in-repo imports and private methods. Stop at framework / stdlib.

For every table touch, record:

- `op` — SELECT / INSERT / UPDATE / DELETE / UPSERT / JOIN_READ
- `fields_read` / `fields_written` — always emit both as arrays (`[]` when no fields are visible, never omit the key)
- `confidence` — apply **Confidence rules** in [references/ir-schema.md](references/ir-schema.md)
- `evidence` — `file:line`

Use `python scripts/extract_sql.py` on raw SQL strings and mapper XML. It is a parser, not the confidence authority: after it returns, apply Confidence rules (`confidence` on a static SQL string stays `med` even if the script said `high`). On MyBatis XML, expand `<include refid>` into the statement body before parsing.

Handler clearly has no DB access (no repo / mapper / SQL / ORM call in the walk): `tables: []` and a one-line note in `meta.notes`.

Walk found DB-shaped calls but no table name: one touch with `name: "<dynamic>"`, `confidence: uncertain`, `evidence: file:line`.

Then write `sequence` as the request path only:

1. Client → Controller, label = `METHOD path`
2. Controller → Service, label = `handler.fn`
3. One step per table touch: Service → table, label = op + columns, `op` = `R` / `W` / `RW`

Done when every deep-traced endpoint has:

- `tables` as an array
- every touch has `op`, `fields_read`, `fields_written`, `confidence`, `evidence`
- `sequence` with the Client → Controller → Service prefix and one step per table touch

### 6. Infer field-level relations

Merge three sources, tagged by `source`:

- `fk` — schema / ORM foreign keys
- `join` — JOIN ON and WHERE a.x = b.y in code
- `inferred` — shared key names used together, low confidence, say so

Cardinality defaults: FK child to parent is `N:1`. Only mark `N:M` when a join table is proven.

Done when every FK found in schema appears in `relations[]`.

### 7. Build IR and render

Combine into `api-db-map.json` exactly as [references/ir-schema.md](references/ir-schema.md). Root is `./api-db-map-out/` unless the user named another path. Rendered IR `endpoints[]` is the deep-trace set only.

Read [references/visualization.md](references/visualization.md) before rendering. The HTML must include T·01, T·02, and T·03.

For **each** deep-traced endpoint:

```bash
dir="$root/$(python scripts/render_index.py --dir-name "$METHOD" "$PATH")"
stamp=$(python scripts/render_index.py --next-stamp "$dir")
# write sliced IR to $dir/$stamp.json  (that endpoint + its tables + relations among them)
python scripts/render_html.py "$dir/$stamp.json" -o "$dir/$stamp.html"
# write $dir/$stamp.md
```

`render_html.py` appends a version onto `registry.json` and regenerates `index.html`.

One deep-traced endpoint: one directory. More than one: one directory per endpoint **and** the combined IR of the deep-trace set rendered to `_project_overview/$stamp.{json,html,md}`.

Also write `$stamp.md` next to the HTML with:

1. Counts (deep-traced APIs, untraced APIs, tables, relations, uncertain items)
2. A summary table of endpoint, method, tables, ops, confidence
3. Mermaid `erDiagram` plus one `sequenceDiagram` for the most complex deep-traced endpoint
4. An **uncertain** section listing evidence paths
5. A **coverage** section listing every untraced `METHOD path`

If an endpoint that accesses the DB has no fields yet, extract them from DTO / mapper result maps / SELECT lists before rendering.

Done when `index.html` lists every deep-traced endpoint just rendered, each card opens the new HTML, previous timestamped files are still on disk, and the coverage section names every untraced inventory id.

### 8. Present to the user

Lead with `index.html`. For a single-endpoint run, also open that endpoint's HTML. Then a short reading guide:

- How many deep-traced APIs write vs only read
- Hottest tables (touched by the most deep-traced endpoints)
- Relations that exist only in code (joins without an FK)
- Uncertain items that need a human look
- Untraced count, then offer to widen

If the user asked about one endpoint, zoom T·01 / T·03 to that endpoint and still show T·02 with unused fields dimmed.

## Guardrails

- Never execute INSERT / UPDATE / DELETE / DDL against a live database. Schema introspection is read-only.
- Never invent a table or column that was not found. Prefer an empty list plus an uncertain note.
- Dynamic or concatenated SQL stays `uncertain`.
- Keep evidence paths (`file:line`) on every table access.
- Stay inside the deep-trace set. After presenting, offer to widen.

## Scripts

| Script | When |
|--------|------|
| `scripts/detect_stack.py <root>` | Step 2; then load the returned `playbook` |
| `scripts/extract_sql.py --file <path>` or `--sql "<stmt>"` | Step 5, raw SQL / mapper XML; re-apply Confidence rules after |
| `scripts/render_index.py --dir-name METHOD '/path'` / `--next-stamp DIR` | Step 7, directory + stamp |
| `scripts/render_html.py <ir.json> -o <out.html>` | Step 7 (also updates registry + index.html) |

## Quality bar

Every deep-traced endpoint has evidence-backed `tables[]` (or a recorded no-DB note, or a `<dynamic>` uncertain touch). `fields_read` and `fields_written` are always present. No invented names. Coverage lists every untraced id. Sparse fields → extract more, then render.
