---
name: api-db-map
description: Trace backend APIs to the database tables and fields they query or modify, then render architecture, ER-field, and sequence diagrams (接口查了哪些表, 改了哪些表, 表关联, 字段关系). Explicit-invocation only — call this skill only when the user names it directly (says "api-db-map" or 用 api-db-map). Do not auto-trigger just because a message mentions tables, endpoints, schema, or field relationships in general; wait for the user to name the skill.
metadata:
  version: "1.0"
  type: workflow
---

# API → DB Map

Analyze a backend codebase and answer, with evidence, which HTTP APIs read or write which database tables and fields. Then render three diagrams in the product style of architecture / relationship / sequence cards.

Do not invent tables, columns, or relations. If the code does not prove an access, mark it `uncertain` and keep going.

## Output contract

Always produce these artifacts under the project root or a path the user named (default `./api-db-map-out/`):

| File | Role |
|------|------|
| `api-db-map.json` | Combined IR. Schema in [references/ir-schema.md](references/ir-schema.md) |
| `api-db-map.html` | Primary deliverable. Self-contained, interactive |
| `api-db-map.md` | Fallback report with summary tables + Mermaid |

Render the HTML with `scripts/render_html.py`. Never hand-write the HTML.

Reply in the user's language. If they wrote Chinese, diagram chrome is Chinese (影响架构图 / 表与字段关系 / 接口时序图).

## Workflow

### 1. Scope

Ask only if the project root is ambiguous. Accept optional filters:

- one route (`GET /api/orders/{id}`)
- one module / package
- an OpenAPI / Swagger file
- a live DB URL for schema ground truth (optional, SELECT-only)

If the user gave no filter, analyze the whole backend, then highlight the highest-impact endpoints first.

### 2. Detect stack

Run `python scripts/detect_stack.py <project-root>`.

Then load **only** the matching playbook from [references/stack-patterns.md](references/stack-patterns.md). Always also use the raw-SQL section.

If detection is weak, ask one clarifying question (framework + ORM), then proceed with filename heuristics + SQL strings rather than stalling.

### 3. Extract schema (ground truth first)

Priority, stop at the first complete source:

1. Live DB `information_schema` / `pg_catalog` — SELECT-only, never write
2. Migrations / DDL (Flyway, Liquibase, Alembic, Prisma, Django, `*.sql`)
3. ORM models (`@Entity`, Prisma `model`, SQLAlchemy, Django Model, GORM tags)
4. Infer from SQL strings last, and mark those tables `inferred`

Write tables, columns, PK/UK, FK, nullability, module guess (package / schema name).

Also capture a human-readable `desc` per column whenever the same source exposes one (DB column comment, DDL `COMMENT`, ORM annotation, doc-comment) — see "Field descriptions" in [references/ir-schema.md](references/ir-schema.md). Leave it unset rather than guessing from the column name.

### 4. Inventory APIs

Collect `{method, path, handler file, function, line}` from routers, controllers, and OpenAPI if present. Deduplicate by `METHOD path`. Skip health/metrics unless the user asked.

### 5. Trace handler → database

From each handler, walk callees 2–4 levels (controller → service → repo / mapper). Follow in-repo imports and private methods. Stop at framework / stdlib.

For every table touch, record:

- `op` — SELECT / INSERT / UPDATE / DELETE / UPSERT / JOIN_READ
- `fields_read` / `fields_written` — always emit both as arrays (`[]` when no fields are visible, never omit the key)
- `confidence` — high / med / low / uncertain
- `evidence` — `file:line`

Confidence rules:

- **high** — ORM model op, annotated query, MyBatis XML with a static table, Prisma client call
- **med** — static SQL string with a clear FROM / INTO / UPDATE
- **low** — derived query name only, query builder with a variable table
- **uncertain** — concatenated SQL, MyBatis dynamic table, reflection, dynamic datasource. Record evidence. Do **not** guess a table name.

Use `python scripts/extract_sql.py` on raw SQL strings and mapper XML.

### 6. Infer field-level relations

Merge three sources, tagged by `source`:

- `fk` — schema / ORM foreign keys
- `join` — JOIN ON and WHERE a.x = b.y in code
- `inferred` — shared key names used together, low confidence, say so

Cardinality defaults: FK child to parent is `N:1`. Only mark `N:M` when a join table is proven.

### 7. Build IR and render

Combine into `api-db-map.json` exactly as [references/ir-schema.md](references/ir-schema.md). Then:

```bash
python scripts/render_html.py api-db-map-out/api-db-map.json -o api-db-map-out/api-db-map.html
```

Visual rules live in [references/visualization.md](references/visualization.md). The HTML must include all three views:

- **T·01 影响架构图** — API cards on the left, tables on the right, arrows labeled with the SQL verb. Dashed = read, solid = write.
- **T·02 表与字段关系** — each table is a card with fields. Draw edges from FK field to referenced PK field, not just table-to-table. Dim fields the selected API does not touch.
- **T·03 接口时序图** — Client to Controller to Service to each touched table, messages labeled with method + columns.

Also write `api-db-map.md` with:

1. Counts (APIs, tables, relations, uncertain items)
2. A summary table of endpoint, method, tables, ops, confidence
3. Mermaid `erDiagram` plus one `sequenceDiagram` for the most complex endpoint
4. An **uncertain** section listing evidence paths

### 8. Present to the user

Lead with the HTML file (render it). Then a short reading guide:

- How many APIs write vs only read
- Hottest tables (touched by the most endpoints)
- Relations that exist only in code (joins without an FK)
- Uncertain items that need a human look

If the user asked about one endpoint, zoom T·01 / T·03 to that endpoint and still show T·02 with unused fields dimmed.

## Guardrails

- Never execute INSERT / UPDATE / DELETE / DDL against a live database. Schema introspection is read-only.
- Never invent a table or column that was not found. Prefer an empty list plus an uncertain note.
- Dynamic or concatenated SQL stays `uncertain`.
- Keep evidence paths (`file:line`) on every table access.
- Do not dump per-stack regex into this file. Those live in `references/stack-patterns.md`.
- If the repo is huge, analyze the requested module first, then offer to widen.

## Scripts

| Script | When |
|--------|------|
| `scripts/detect_stack.py <root>` | Step 2 |
| `scripts/extract_sql.py --file <path>` or `--sql "<stmt>"` | Step 5, raw SQL / mapper XML |
| `scripts/render_html.py <ir.json> -o <out.html>` | Step 7 |

## Quality bar

The HTML should read like the reference product cards: cream grid canvas, rounded typed nodes, dashed group boxes, a bottom legend with counts, T·01 / T·02 / T·03 pills. If the first render looks sparse (one API, no fields), go back and extract fields from DTO / mapper result maps / SELECT lists before handing it over.
