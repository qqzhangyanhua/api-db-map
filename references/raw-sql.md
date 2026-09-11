# Raw SQL extraction

Use this playbook for every stack, and as the only playbook when the ORM is unknown.

## Harvest candidates

Search source (exclude vendor dirs) for:

- String literals containing `SELECT `, `INSERT `, `UPDATE `, `DELETE `, `WITH `, `MERGE `
- Template strings / text blocks (Java `"""`, Python `"""`, Go raw `` ` ``)
- MyBatis XML statement bodies
- `@Query("...")`, `@Select("...")`, `text("...")`, `sql.SQL`, `db.Exec("...")`

## Parse

Prefer `sqlglot` (see `scripts/extract_sql.py`). Fall back to regex if the script or sqlglot is missing.

Extract:

- tables: FROM / JOIN / INTO / UPDATE / DELETE FROM / USING
- fields_read: SELECT list (ignore `*`, keep `table.col` and aliases that map to a real col)
- fields_written: INSERT column list, UPDATE SET targets
- op: SELECT→SELECT, INSERT→INSERT, UPDATE→UPDATE, DELETE→DELETE, INSERT..ON CONFLICT/ON DUPLICATE→UPSERT, JOIN-only side table→JOIN_READ

Aliases: `FROM orders o` → table `orders`. Resolve `o.status` to `orders.status`.

## Dynamic SQL

If the table name is built by concat / format / `${}` / f-string with a variable:

```
confidence = uncertain
name = "<dynamic>"
evidence = file:line
```

Do not invent the runtime table. List the expression in `meta.notes`.

## Regex fallback (when sqlglot is absent)

```
FROM\s+([`"]?[\w.]+[`"]?)
JOIN\s+([`"]?[\w.]+[`"]?)
INTO\s+([`"]?[\w.]+[`"]?)
UPDATE\s+([`"]?[\w.]+[`"]?)
DELETE\s+FROM\s+([`"]?[\w.]+[`"]?)
```

Strip quotes and schema prefix for `tables[].name`; keep schema in `tables[].schema` when present (`public.orders` → schema=public, name=orders).
