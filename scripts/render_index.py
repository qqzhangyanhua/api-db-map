#!/usr/bin/env python3
"""Build api-db-map-out/index.html from registry.json.

Called automatically by render_html.py after each diagram generation.
Can also be run standalone:
    python scripts/render_index.py api-db-map-out/
    python scripts/render_index.py --next-stamp api-db-map-out/GET__api__orders__-id-
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


PLACEHOLDER = "/*__REGISTRY__*/{}"
SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_ROOT / "assets" / "index.template.html"
READ_OPS = {"SELECT", "JOIN_READ"}
WRITE_OPS = {"INSERT", "UPDATE", "DELETE", "UPSERT"}
CONF_KEYS = ("high", "med", "low", "uncertain")
UNSAFE_DIR = re.compile(r"[^A-Za-z0-9._-]+")


def path_to_dir(method: str, path: str) -> str:
    """GET /api/orders/{id} → GET__api__orders__-id-"""
    safe = (path or "").replace("{", "-").replace("}", "-")
    if safe.startswith("/"):
        safe = safe[1:]
    safe = safe.replace("/", "__")
    safe = UNSAFE_DIR.sub("-", safe)
    return f"{(method or 'GET').upper()}__{safe}"


def next_stamp(dir_path: Path) -> str:
    """YYYY-MM-DD, or YYYY-MM-DDTHH-MM if that day's html already exists."""
    dir_path.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone()
    day = now.strftime("%Y-%m-%d")
    if not (dir_path / f"{day}.html").exists():
        return day
    hm = now.strftime("%Y-%m-%dT%H-%M")
    if not (dir_path / f"{hm}.html").exists():
        return hm
    return now.strftime("%Y-%m-%dT%H-%M-%S")


def is_result_dir(name: str) -> bool:
    return name == "_project_overview" or "__" in name


def registry_root(html_path: Path) -> Path:
    parent = html_path.resolve().parent
    if is_result_dir(parent.name):
        return parent.parent
    return parent


def should_index(html_path: Path) -> bool:
    parent = html_path.resolve().parent
    if is_result_dir(parent.name):
        return True
    if parent.name == "api-db-map-out":
        return True
    return (parent / "registry.json").exists()


def load_registry(out_dir: Path) -> dict:
    reg_path = out_dir / "registry.json"
    if reg_path.exists():
        data = json.loads(reg_path.read_text(encoding="utf-8"))
        data.setdefault("entries", [])
        return data
    return {"updated_at": "", "entries": []}


def save_registry(out_dir: Path, registry: dict) -> None:
    registry["updated_at"] = datetime.now().astimezone().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "registry.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def rel_to(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def endpoint_meta(ep: dict) -> tuple[list[str], str, dict]:
    touches = ep.get("tables") or []
    tables = list(dict.fromkeys(t.get("name") for t in touches if t.get("name")))
    ops = {t.get("op") for t in touches}
    has_r = bool(ops & READ_OPS)
    has_w = bool(ops & WRITE_OPS)
    if has_r and has_w:
        rw = "read-write"
    elif has_w:
        rw = "write"
    else:
        rw = "read"
    conf = {k: 0 for k in CONF_KEYS}
    for t in touches:
        key = t.get("confidence") or "uncertain"
        if key not in conf:
            key = "uncertain"
        conf[key] += 1
    return tables, rw, conf


def make_version(out_dir: Path, ep: dict, html_path: Path, ir_path: Path) -> dict:
    tables, rw, conf = endpoint_meta(ep)
    try:
        ir_path.resolve().relative_to(out_dir.resolve())
        json_path = ir_path
    except ValueError:
        json_path = html_path.with_suffix(".json")
    md_path = html_path.with_suffix(".md")
    return {
        "timestamp": datetime.now().astimezone().isoformat(),
        "html": rel_to(html_path, out_dir),
        "json": rel_to(json_path, out_dir),
        "md": rel_to(md_path, out_dir),
        "tables": tables,
        "table_count": len(tables),
        "rw": rw,
        "confidence": conf,
    }


def upsert_entry(registry: dict, method: str, path: str, dir_name: str, version: dict) -> None:
    key = (method.upper(), path)
    for existing in registry["entries"]:
        if (existing["method"].upper(), existing["path"]) == key:
            versions = existing.setdefault("versions", [])
            for i, old in enumerate(versions):
                if old.get("html") == version["html"]:
                    versions[i] = version
                    return
            versions.append(version)
            return
    registry["entries"].append({
        "method": method.upper(),
        "path": path,
        "dir": dir_name,
        "versions": [version],
    })


def register_endpoint(registry: dict, out_dir: Path, ep: dict, html_path: Path, ir_path: Path) -> None:
    method = ep.get("method") or "GET"
    path = ep.get("path") or ""
    upsert_entry(registry, method, path, path_to_dir(method, path), make_version(out_dir, ep, html_path, ir_path))


def after_html_render(ir: dict, ir_path: Path, html_path: Path) -> None:
    """Update registry.json and rebuild index.html. No-op outside api-db-map-out trees."""
    html_path = html_path.resolve()
    ir_path = Path(ir_path).resolve()
    if not should_index(html_path):
        return
    out_dir = registry_root(html_path)
    parent = html_path.parent.name
    registry = load_registry(out_dir)
    if is_result_dir(parent) and parent != "_project_overview":
        for ep in ir.get("endpoints") or []:
            if path_to_dir(ep.get("method") or "", ep.get("path") or "") == parent:
                register_endpoint(registry, out_dir, ep, html_path, ir_path)
    else:
        registry["overview"] = rel_to(html_path, out_dir)
    save_registry(out_dir, registry)
    rebuild_index(out_dir)


def render_index(registry: dict, template: str) -> str:
    payload = json.dumps(registry, ensure_ascii=False)
    if PLACEHOLDER not in template:
        raise SystemExit("index template missing /*__REGISTRY__*/{} placeholder")
    return template.replace(PLACEHOLDER, payload, 1)


def rebuild_index(out_dir: Path, template_path: Path | None = None) -> Path:
    tp = template_path or DEFAULT_TEMPLATE
    if not tp.exists():
        raise SystemExit(f"index template not found: {tp}")
    registry = load_registry(out_dir)
    html = render_index(registry, tp.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"wrote {index_path} ({index_path.stat().st_size} bytes, {len(registry['entries'])} entries)")
    return index_path


def main() -> None:
    p = argparse.ArgumentParser(description="Rebuild api-db-map index.html from registry.json")
    p.add_argument("out_dir", nargs="?", type=Path, default=Path("api-db-map-out"),
                   help="Directory containing registry.json (default: api-db-map-out/)")
    p.add_argument("--template", type=Path, default=None, help="Override index template path")
    p.add_argument("--next-stamp", type=Path, default=None, metavar="DIR",
                   help="Print the next collision-safe stamp for DIR and exit")
    p.add_argument("--dir-name", nargs=2, metavar=("METHOD", "PATH"),
                   help="Print the endpoint directory name and exit")
    args = p.parse_args()
    if args.dir_name is not None:
        print(path_to_dir(args.dir_name[0], args.dir_name[1]))
        return
    if args.next_stamp is not None:
        print(next_stamp(args.next_stamp.resolve()))
        return
    rebuild_index(args.out_dir.resolve(), args.template)


if __name__ == "__main__":
    main()
