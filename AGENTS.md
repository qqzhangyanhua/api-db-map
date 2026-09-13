## This repo

`api-db-map` is an Agent Skill, not an application. What ships is `SKILL.md` (the workflow an agent follows), `references/` (loaded on demand, one file per concern), `scripts/` (Python 3, no required third-party packages), and `assets/` (the HTML templates).

Invariants to keep when editing:

- `SKILL.md` is the contract. Change a script's flags or output shape and you must update the step that calls it plus the `## Scripts` table.
- Script calls in `SKILL.md` are `python3 "$SKILL_DIR/scripts/..."`. The skill is installed outside the project being analyzed, and bare `python` does not exist on macOS.
- Never name a shell variable `PATH` in an example.
- Every string that comes from the analyzed repo — table names, paths, column comments — reaches the page through `esc()`. Don't interpolate IR values into `innerHTML` raw.
- `assets/diagram.template.html` and `assets/index.template.html` hold the `/*__IR__*/{}` and `/*__REGISTRY__*/{}` placeholders that `render_html.py` and `render_index.py` fill. Output HTML is never hand-written.
- Run `python3 scripts/smoke_test.py` after touching any script or template.

## Issue tracker

Issues live as markdown files under `.scratch/<feature>/` (local only, gitignored). See `docs/agents/issue-tracker.md`.

Triage state is a `Status:` line at the top of each issue file, using one of `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`.
