#!/usr/bin/env python3
"""Inject api-db-map.json into assets/diagram.template.html."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


PLACEHOLDER = "/*__IR__*/{}"


def render(ir: dict, template: str) -> str:
    payload = json.dumps(ir, ensure_ascii=False)
    if PLACEHOLDER not in template:
        raise SystemExit("template missing /*__IR__*/{} placeholder")
    return template.replace(PLACEHOLDER, payload, 1)


def main() -> None:
    here = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description="Render api-db-map.html from IR JSON")
    p.add_argument("ir", nargs="?", type=Path, default=here / "assets" / "sample-ir.json")
    p.add_argument("--ir", dest="ir_opt", type=Path, default=None)
    p.add_argument("--template", type=Path, default=here / "assets" / "diagram.template.html")
    p.add_argument("-o", "--out", type=Path, default=Path("api-db-map.html"))
    p.add_argument("--no-index", action="store_true",
                   help="Skip registry.json / index.html update")
    args = p.parse_args()
    ir_path = args.ir_opt or args.ir
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    html = render(ir, args.template.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes)")
    if not args.no_index:
        try:
            from render_index import after_html_render
        except ImportError:
            import sys
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from render_index import after_html_render
        after_html_render(ir, ir_path, args.out)


if __name__ == "__main__":
    main()
