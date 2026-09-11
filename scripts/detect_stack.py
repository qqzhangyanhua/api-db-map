#!/usr/bin/env python3
"""Detect backend language, framework, and ORM from a project root."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Callable

SKIP = {".git", "node_modules", ".venv", "venv", "target", "dist", "build", "__pycache__", ".idea", "vendor"}


def read(p: Path, n: int = 200_000) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:n]
    except Exception:
        return ""


def exists_any(root: Path, names: list[str]) -> Path | None:
    for n in names:
        p = root / n
        if p.exists():
            return p
    return None


def find_files(root: Path, matcher: Callable[[Path, str], bool], limit: int = 500) -> list[Path]:
    """Walk root, pruning SKIP dirs during traversal (not after), collecting matches."""
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        dp = Path(dirpath)
        for fn in filenames:
            if matcher(dp, fn):
                out.append(dp / fn)
                if len(out) >= limit:
                    return out
    return out


def detect(root: Path) -> dict:
    signals: list[str] = []
    lang = framework = orm = db = ""

    pom = exists_any(root, ["pom.xml", "build.gradle", "build.gradle.kts"])
    req = exists_any(root, ["requirements.txt", "pyproject.toml", "Pipfile"])
    pkg = exists_any(root, ["package.json"])
    gomod = exists_any(root, ["go.mod"])
    prisma = find_files(root, lambda _d, fn: fn == "schema.prisma", limit=5)

    text_blob = ""
    for p in [pom, req, pkg, gomod]:
        if p:
            text_blob += read(p).lower() + "\n"

    if pom:
        lang = "java"
        signals.append(str(pom.relative_to(root)))
        if "spring" in text_blob:
            framework = "spring"
        if "mybatis-plus" in text_blob or "mybatis_plus" in text_blob:
            orm = "mybatis-plus"
        elif "mybatis" in text_blob:
            orm = "mybatis"
        elif "data-jpa" in text_blob or "hibernate" in text_blob:
            # matches both "spring-data-jpa" and the common Spring Boot starter
            # artifact id "spring-boot-starter-data-jpa".
            orm = "jpa"
    elif exists_any(root, ["manage.py"]) or (req and "django" in text_blob):
        lang = "py"
        framework = "django"
        orm = "django-orm"
        signals.append("django")
    elif req or exists_any(root, ["main.py", "app.py"]):
        lang = "py"
        py_files = find_files(root, lambda _d, fn: fn.endswith(".py"), limit=300)
        if "fastapi" in text_blob or any("fastapi" in read(p).lower() for p in py_files):
            framework = "fastapi"
            signals.append("fastapi")
        if "sqlmodel" in text_blob:
            orm = "sqlmodel"
        elif "sqlalchemy" in text_blob:
            orm = "sqlalchemy"
        elif "prisma" in text_blob:
            orm = "prisma"
        elif "tortoise" in text_blob:
            orm = "tortoise"
    elif pkg:
        pj = read(pkg).lower()
        lang = "ts" if (root / "tsconfig.json").exists() else "js"
        signals.append("package.json")
        if "@nestjs/core" in pj:
            framework = "nest"
        elif "express" in pj:
            framework = "express"
        elif "fastify" in pj:
            framework = "fastify"
        elif "koa" in pj:
            framework = "koa"
        if "@prisma/client" in pj or prisma:
            orm = "prisma"
        elif "typeorm" in pj:
            orm = "typeorm"
        elif "drizzle-orm" in pj:
            orm = "drizzle"
        elif "sequelize" in pj:
            orm = "sequelize"
    elif gomod:
        lang = "go"
        gm = read(gomod).lower()
        signals.append("go.mod")
        if "gin-gonic/gin" in gm:
            framework = "gin"
        elif "go-chi/chi" in gm:
            framework = "chi"
        elif "gofiber/fiber" in gm:
            framework = "fiber"
        if "gorm.io/gorm" in gm:
            orm = "gorm"

    if prisma and not orm:
        orm = "prisma"
        signals.append("schema.prisma")

    xmls = find_files(
        root,
        lambda d, fn: fn.lower().endswith(".xml") and (fn.endswith("Mapper.xml") or d.name == "mapper"),
        limit=50,
    )
    if xmls and not orm:
        lang = lang or "java"
        framework = framework or "spring"
        orm = "mybatis"
        signals.append(str(xmls[0].relative_to(root)))

    if "postgres" in text_blob or "postgresql" in text_blob:
        db = "postgresql"
    elif "mysql" in text_blob:
        db = "mysql"
    elif "sqlite" in text_blob:
        db = "sqlite"

    return {
        "root": str(root.resolve()),
        "lang": lang or "unknown",
        "framework": framework or "unknown",
        "orm": orm or "unknown",
        "db": db or "unknown",
        "signals": signals[:12],
        "playbook": _playbook(framework, orm),
    }


def _playbook(framework: str, orm: str) -> str:
    # Check orm-specific Java cases before the generic `framework == "spring"` fallback,
    # otherwise Spring+JPA projects are always misrouted to the MyBatis playbook.
    if orm == "jpa":
        return "references/stack-patterns.md#java--spring--jpa"
    if orm in {"mybatis", "mybatis-plus"}:
        return "references/stack-patterns.md#java--spring--mybatis--plus"
    if framework == "django":
        return "references/stack-patterns.md#python--django"
    if framework == "fastapi":
        return "references/stack-patterns.md#python--fastapi--sqlalchemy--sqlmodel"
    if orm == "prisma":
        return "references/stack-patterns.md#node--prisma"
    if orm in {"typeorm", "drizzle", "sequelize"}:
        return "references/stack-patterns.md#node--typeorm--drizzle--sequelize"
    if orm == "gorm":
        return "references/stack-patterns.md#go--gin--gorm"
    if framework == "spring":
        # Spring detected but ORM unclear (no JPA/MyBatis signal, no mapper XML found yet).
        return "references/stack-patterns.md#java--spring--mybatis--plus"
    return "references/raw-sql.md"


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"not a directory: {root}"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(detect(root), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
