#!/usr/bin/env python3
"""Smoke test: the four scripts still produce the shapes SKILL.md promises.

    python3 scripts/smoke_test.py

Covers the seams a template or parser edit is most likely to break silently:
render_html injects the IR and keeps all three views, render_index writes a
registry + index page, extract_sql marks JOINed tables read-only, and neither
template leaks unescaped IR text into HTML.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + (f"  — {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


def test_render_html(out_dir: Path) -> None:
    ir_path = ROOT / "assets" / "sample-ir.json"
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    html_path = out_dir / "GET__api__orders__-id-" / "2026-01-01.html"
    proc = run(str(SCRIPTS / "render_html.py"), str(ir_path), "-o", str(html_path))
    check("render_html.py exits 0", proc.returncode == 0, proc.stderr.strip())
    if not html_path.exists():
        check("render_html.py writes the html", False)
        return
    html = html_path.read_text(encoding="utf-8")
    check("IR is injected", "/*__IR__*/{}" not in html and ir["endpoints"][0]["path"] in html)
    check("T02 field fold can expand", "expandedTables" in html and "data-more" in html)
    for view in ("view-t01", "view-t02", "view-t03"):
        check(f"{view} is in the page", f'id="{view}"' in html)
    check("no unreplaced placeholder", "__REGISTRY__" not in html)

    reg_path = out_dir / "registry.json"
    check("registry.json is written", reg_path.exists())
    if reg_path.exists():
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        paths = [e["path"] for e in reg["entries"]]
        # only the endpoint whose id matches the parent directory gets registered,
        # even though the sample IR carries three
        check("registry lists exactly the directory's endpoint", paths == ["/api/orders/{id}"], str(paths))
    index_path = out_dir / "index.html"
    check("index.html is written", index_path.exists())
    if index_path.exists():
        check("index has the registry inlined", "/*__REGISTRY__*/{}" not in
              index_path.read_text(encoding="utf-8"))


def test_stamp_and_dir(out_dir: Path) -> None:
    proc = run(str(SCRIPTS / "render_index.py"), "--dir-name", "GET", "/api/orders/{id}")
    check("--dir-name encodes path params", proc.stdout.strip() == "GET__api__orders__-id-",
          proc.stdout.strip())
    ep_dir = out_dir / "GET__api__orders__-id-"
    proc = run(str(SCRIPTS / "render_index.py"), "--next-stamp", str(ep_dir))
    stamp = proc.stdout.strip()
    check("--next-stamp avoids an existing file", stamp != "2026-01-01" and bool(stamp), stamp)


def test_extract_sql() -> None:
    sql = "SELECT o.id, o.status FROM orders o JOIN users u ON u.id = o.user_id WHERE o.id = 1"
    proc = run(str(SCRIPTS / "extract_sql.py"), "--sql", sql)
    check("extract_sql.py exits 0", proc.returncode == 0, proc.stderr.strip())
    if proc.returncode != 0:
        return
    rec = json.loads(proc.stdout)
    ops = {t["name"]: t["op"] for t in rec["tables"]}
    check("FROM target keeps the statement op", ops.get("orders") == "SELECT", str(ops))
    check("JOINed side is JOIN_READ", ops.get("users") == "JOIN_READ", str(ops))
    check("join predicate column is a read", "user_id" in rec["fields_read"], str(rec["fields_read"]))
    check("join pair resolves aliases",
          rec["joins"] == [{"left": {"table": "users", "column": "id"},
                            "right": {"table": "orders", "column": "user_id"}}],
          json.dumps(rec["joins"]))

    proc = run(str(SCRIPTS / "extract_sql.py"), "--sql", "SELECT * FROM ${tbl} WHERE id = 1")
    rec = json.loads(proc.stdout)
    check("dynamic table stays uncertain", rec["confidence"] == "uncertain")
    check("dynamic table is named <dynamic>", rec["tables"][0]["name"] == "<dynamic>")


def test_escaping(out_dir: Path) -> None:
    """A column comment carrying markup must not reach the page as markup."""
    ir = json.loads((ROOT / "assets" / "sample-ir.json").read_text(encoding="utf-8"))
    payload = "<img src=x onerror=alert(1)>"
    ir["tables"][0]["fields"][0]["desc"] = payload
    ir["endpoints"][0]["path"] = ir["endpoints"][0]["path"] + payload
    hostile = out_dir / "hostile.json"
    hostile.write_text(json.dumps(ir, ensure_ascii=False), encoding="utf-8")
    html_path = out_dir / "hostile.html"
    run(str(SCRIPTS / "render_html.py"), str(hostile), "-o", str(html_path), "--no-index")
    html = html_path.read_text(encoding="utf-8")
    body = html.split("window.__IR__", 1)[-1].split("</script>", 1)[-1]  # skip the inlined JSON
    check("no raw <img onerror> in the rendered body", "onerror=alert" not in body)
    check("templates escape through esc()", len(re.findall(r"function esc\(", html)) == 1)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "api-db-map-out"
        test_render_html(out_dir)
        test_stamp_and_dir(out_dir)
        test_extract_sql()
        test_escaping(out_dir)
    try:
        import sqlglot  # noqa: F401
        print("\n(sqlglot present — extract_sql.py used its parser)")
    except ImportError:
        print("\n(sqlglot absent — extract_sql.py used the regex fallback)")
    if failures:
        print(f"\n{len(failures)} failed: " + ", ".join(failures))
        sys.exit(1)
    print("\nall good")


if __name__ == "__main__":
    main()
