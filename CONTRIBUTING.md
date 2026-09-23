# Contributing

## Commit messages

This repo uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short summary>

<body - what changed and why, wrap at ~72 chars>

Closes #<issue-number>
```

Common types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`.

## Workflow

1. Create a branch off `main`: `feature/<slice-name>` for functional work,
   `chore/<topic>` for process/tooling.
2. Keep the branch scoped to one issue/vertical slice where possible.
3. Before opening a PR: `python manage.py test marketplace`, `ruff check .`,
   `ruff format --check .` must all pass locally (pre-commit runs the ruff
   checks automatically on every commit).
4. Open a PR referencing the issue(s) it closes (`Closes #N`). Do not merge
   your own PR without review once branch protection is enabled.

## Code style

- `ruff` is the single source of truth for lint/format - see
  `pyproject.toml` for the (minimal) project-specific rule overrides.
- Prefer Django/DRF idioms (class-based views, serializers, migrations)
  over hand-rolled equivalents.
