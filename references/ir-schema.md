# api-db-map IR schema

Renderer and extractors share one combined document: `api-db-map.json`.
During analysis you MAY write working files (`schema.json`, `endpoints.json`, `impact.json`, `relations.json`) and then merge them.

Never invent tables, columns, or relations. If evidence is weak, keep the object and set `confidence` to `uncertain`.

## Combined document

```ts
type Op = "SELECT" | "INSERT" | "UPDATE" | "DELETE" | "UPSERT" | "JOIN_READ"
type Conf = "high" | "med" | "low" | "uncertain"
type Card = "1:1" | "1:N" | "N:1" | "N:M"

interface ApiDbMap {
  meta: {
    project: string
    root: string
    stack: { lang: string; framework: string; orm: string; db?: string }
    generated_at: string
    confidence_tier: "T1_live_db" | "T2_migrations" | "T3_orm" | "T4_sql_strings"
    notes?: string[]
  }
  tables: Table[]
  relations: Relation[]
  endpoints: Endpoint[]
  table_api_index: Record<string, string[]>
}

interface Table {
  name: string
  schema?: string
  module?: string
  fields: Field[]
}

interface Field {
  name: string
  type: string
  pk?: boolean
  uk?: boolean
  nullable?: boolean
  fk?: { table: string; column: string; onDelete?: string; card?: Card }
  desc?: string                // human-readable meaning, e.g. "昵称" for nick_name. See "Field descriptions" below.
}

interface Relation {
  from: { table: string; field: string }
  to: { table: string; field: string }
  card: Card
  source: "fk" | "join" | "inferred"
}

interface Endpoint {
  id: string                  // "PUT /api/orders/{id}"
  method: string              // GET POST PUT PATCH DELETE
  path: string
  handler: { file: string; fn: string; line?: number }
  tables: EndpointTable[]
  sequence: SeqStep[]
}

interface EndpointTable {
  name: string
  op: Op
  fields_read: string[]
  fields_written: string[]
  confidence: Conf
  evidence: string            // "OrderMapper.xml:88"
}

interface SeqStep {
  from: string                // Client | Controller | Service | Repo | <table> | Cache
  to: string
  label: string
  op?: "R" | "W" | "RW"
}
```

## Field descriptions

Capture `Field.desc` opportunistically while extracting schema (step 3) — never invent one. Common sources, in the same priority order as schema extraction itself:

1. Live DB — `information_schema.columns.column_comment` (MySQL) / `pg_catalog` column description (Postgres)
2. DDL / migrations — `COMMENT '...'` on the column, Prisma `///` doc-comments above a field
3. ORM annotations / docstrings — see the per-stack recipes in `references/stack-patterns.md`
4. Leave `desc` unset if none of the above exist. Do not guess a description from the column name.

If a table has a comment too (DDL `COMMENT = '...'` on the table, or a class-level doc-comment), keep it in `Table.module` only if it doubles as a grouping label; otherwise drop it — the schema has no dedicated table-description slot yet.

## Confidence rules

| Level | When |
|---|---|
| high | ORM model / `@Query` / MyBatis XML with static table / Prisma client call |
| med | Raw SQL string with a clear FROM / INTO / UPDATE target |
| low | Query builder with a variable table, Spring Data derived query name only |
| uncertain | String concat, MyBatis `${}` table, reflection, dynamic datasource |

## Render mapping

- T-01 nodes = `endpoints[]` + `tables[]`; edges = `endpoints[].tables`
- T-02 nodes = `tables[].fields`; edges = `relations[]`; each field row shows `type` (or `PK`/`→ table.column` for keys) plus `desc` when present
- T-03 participants + messages = `endpoints[].sequence`
- Click filter uses `table_api_index` plus `fields_read` / `fields_written` to dim unused fields

## Working-file split (optional)

If the repo is large, write these first, then merge:

1. `schema.json` → `{ tables, relations }`
2. `endpoints.json` → `{ endpoints: [{id,method,path,handler}] }`
3. `impact.json` → `{ endpoints: [{id,tables,sequence}] }`
4. Merge into `api-db-map.json` and add `table_api_index`
