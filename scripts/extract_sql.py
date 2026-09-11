#!/usr/bin/env python3
"""Extract tables, ops, and columns from a SQL string or a MyBatis/XML/SQL file."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TABLE_RE = re.compile(
    r"""(?:
        \bFROM\s+([`\"\[]?[\w.]+[`\"\]]?)
      | \bJOIN\s+([`\"\[]?[\w.]+[`\"\]]?)
      | \bINTO\s+([`\"\[]?[\w.]+[`\"\]]?)
      | \bUPDATE\s+([`\"\[]?[\w.]+[`\"\]]?)
      | \bDELETE\s+FROM\s+([`\"\[]?[\w.]+[`\"\]]?)
      | \bUPDATE\s+([`\"\[]?[\w.]+[`\"\]]?)\s+SET
    )""",
    re.I | re.X,
)
INSERT_COLS_RE = re.compile(r"INSERT\s+INTO\s+[^\s(]+\s*\(([^)]+)\)", re.I | re.S)
UPDATE_SET_RE = re.compile(r"\bSET\s+(.+?)(?:\bWHERE\b|\bRETURNING\b|$)", re.I | re.S)
SELECT_LIST_RE = re.compile(r"\bSELECT\s+(DISTINCT\s+)?(.+?)\bFROM\b", re.I | re.S)
XML_STMT_RE = re.compile(
    r"<(select|insert|update|delete)\b([^>]*)>(.*?)</\1>",
    re.I | re.S,
)
DYN_TABLE_RE = re.compile(r"\$\{[^}]+\}|`?\+\s*\w+|f[\"'].*\{")


def strip_ident(name: str) -> tuple[str | None, str]:
    name = name.strip().strip('`"[]')
    if "." in name:
        schema, tbl = name.split(".", 1)
        return schema, tbl
    return None, name


def classify(sql: str) -> str:
    s = sql.lstrip().upper()
    if s.startswith("INSERT") and ("ON CONFLICT" in s or "ON DUPLICATE" in s):
        return "UPSERT"
    if s.startswith("SELECT") or s.startswith("WITH"):
        return "SELECT"
    if s.startswith("INSERT"):
        return "INSERT"
    if s.startswith("UPDATE"):
        return "UPDATE"
    if s.startswith("DELETE"):
        return "DELETE"
    return "SELECT"


def split_cols(blob: str) -> list[str]:
    out = []
    for part in blob.split(","):
        part = re.sub(r"\s+", " ", part).strip()
        if not part or part == "*":
            continue
        part = re.sub(r"\s+AS\s+\w+$", "", part, flags=re.I)
        # take last ident: o.status → status, keep table if present
        m = re.search(r"([\w]+)\.([\w]+)$", part)
        if m:
            out.append(m.group(2))
            continue
        m = re.search(r"([\w]+)$", part)
        if m and m.group(1).upper() not in {"ASC", "DESC", "NULL"}:
            out.append(m.group(1))
    # unique preserve order
    seen = set()
    uniq = []
    for c in out:
        if c.lower() not in seen:
            seen.add(c.lower())
            uniq.append(c)
    return uniq


def parse_with_sqlglot(sql: str) -> dict | None:
    try:
        import sqlglot
        from sqlglot import exp
    except Exception:
        return None
    try:
        tree = sqlglot.parse_one(sql, error_level=None)
    except Exception:
        return None
    if tree is None:
        return None
    tables = []
    for t in tree.find_all(exp.Table):
        schema, name = t.db, t.name
        if name:
            tables.append({"schema": schema, "name": name})
    fields_read, fields_written = [], []
    for c in tree.find_all(exp.Column):
        if c.name:
            fields_read.append(c.name)
    if isinstance(tree, exp.Insert):
        for c in tree.args.get("columns") or []:
            if getattr(c, "name", None):
                fields_written.append(c.name)
    if isinstance(tree, exp.Update):
        for eq in tree.find_all(exp.EQ):
            left = eq.left
            if isinstance(left, exp.Column) and left.name:
                fields_written.append(left.name)
    return {
        "tables": tables,
        "fields_read": _uniq(fields_read),
        "fields_written": _uniq(fields_written),
        "engine": "sqlglot",
    }


def _uniq(xs: list[str]) -> list[str]:
    seen, out = set(), []
    for x in xs:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def parse_regex(sql: str) -> dict:
    tables = []
    for m in TABLE_RE.finditer(sql):
        raw = next(g for g in m.groups() if g)
        schema, name = strip_ident(raw)
        tables.append({"schema": schema, "name": name})
    # dedupe tables
    seen, uniq_t = set(), []
    for t in tables:
        k = (t["schema"], t["name"].lower())
        if k not in seen:
            seen.add(k)
            uniq_t.append(t)
    fields_read, fields_written = [], []
    sm = SELECT_LIST_RE.search(sql)
    if sm:
        fields_read = split_cols(sm.group(2))
    im = INSERT_COLS_RE.search(sql)
    if im:
        fields_written = split_cols(im.group(1))
    um = UPDATE_SET_RE.search(sql)
    if um:
        sets = []
        for part in um.group(1).split(","):
            left = part.split("=")[0]
            sets.extend(split_cols(left))
        fields_written = _uniq(fields_written + sets)
    return {
        "tables": uniq_t,
        "fields_read": fields_read,
        "fields_written": fields_written,
        "engine": "regex",
    }


def analyze_sql(sql: str, source: str = "") -> dict:
    cleaned = re.sub(r"<!--.*?-->", " ", sql, flags=re.S)
    cleaned = re.sub(r"/\*.*?\*/", " ", cleaned, flags=re.S)
    cleaned = re.sub(r"--.*?$", " ", cleaned, flags=re.M)
    # flatten mybatis tags to spaces so FROM table still visible
    flattened = re.sub(r"</?[^>]+>", " ", cleaned)
    parsed = parse_with_sqlglot(flattened) or parse_regex(flattened)
    op = classify(flattened)
    conf = "med"
    if DYN_TABLE_RE.search(sql):
        conf = "uncertain"
        if not parsed["tables"]:
            parsed["tables"] = [{"schema": None, "name": "<dynamic>"}]
    elif parsed["engine"] == "sqlglot" and parsed["tables"]:
        conf = "high"
    return {
        "op": op,
        "tables": parsed["tables"],
        "fields_read": parsed["fields_read"],
        "fields_written": parsed["fields_written"] if op != "SELECT" else [],
        "confidence": conf,
        "evidence": source,
        "engine": parsed["engine"],
        "sql_preview": re.sub(r"\s+", " ", flattened).strip()[:240],
    }


def analyze_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    results = []
    if path.suffix.lower() == ".xml" or "<mapper" in text[:500].lower() or "<sqlmap" in text[:500].lower():
        for m in XML_STMT_RE.finditer(text):
            kind, attrs, body = m.group(1), m.group(2), m.group(3)
            id_m = re.search(r'\bid\s*=\s*["\']([^"\']+)', attrs)
            stmt_id = id_m.group(1) if id_m else kind
            line = text[: m.start()].count("\n") + 1
            rec = analyze_sql(body, f"{path}:{line}#{stmt_id}")
            # XML tag is a stronger op signal
            tag_op = {"select": "SELECT", "insert": "INSERT", "update": "UPDATE", "delete": "DELETE"}[kind.lower()]
            rec["op"] = tag_op
            results.append(rec)
        return results
    rec = analyze_sql(text, f"{path}:1")
    return [rec]


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract tables/fields from SQL or mapper XML")
    ap.add_argument("--file", "-f", help="SQL or MyBatis XML file")
    ap.add_argument("--sql", help="Raw SQL string")
    ap.add_argument("--source", default="", help="evidence label")
    args = ap.parse_args()
    if args.file:
        print(json.dumps(analyze_file(Path(args.file)), indent=2, ensure_ascii=False))
    elif args.sql:
        print(json.dumps(analyze_sql(args.sql, args.source or "<cli>"), indent=2, ensure_ascii=False))
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
