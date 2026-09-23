# Working Agreement

Pod: solo practice build (iPelino). This is a one-person repo used for
Week 1 DevOps-fundamentals practice, not a multi-person pod - the sections
below are written the way they would be for a real pod, with notes on
what changes because there is only one person here.

## 1. Branching

- Trunk: `main`, always in a state that `make test`/`manage.py test` and
  `ruff check`/`ruff format --check` pass on.
- Branch naming: `feature/<slice-name>` for functional work (e.g.
  `feature/isoko-functional-endpoints`), `chore/<topic>` for process or
  tooling work (e.g. `chore/f1.1-f1.3-devops-fundamentals`).
- Batch size: one branch per vertical slice or NFR session, merged same
  day - a branch should never outlive the issue it closes.

## 2. Review

- Who reviews a PR before it merges into `main`: normally a teammate, not
  the author. Solo, there is no second reviewer, so every PR still goes
  through GitHub's PR flow (not a direct push) so there is a reviewable
  diff and a CI/lint gate to check, even without a second pair of eyes.
- What a reviewer checks, at minimum: tests pass, `ruff check`/`format
  --check` clean, the diff matches the linked issue's acceptance
  criteria, no unrelated files touched.
- Turnaround target: same day for a solo repo; in a real pod, no PR
  waits more than 4 working hours before someone pings the reviewer.

## 3. Commits

- Message convention: Conventional Commits - `<type>: <subject>`, types
  `feat`, `fix`, `chore`, `docs`, `test`; body references the issue it
  closes (`Closes #N`).
- What never gets committed: `.env` files, real secrets/tokens, `db.sqlite3`,
  `__pycache__`, anything the pre-commit `gitleaks`-style secret check
  would flag (see F1.4).

## 4. When someone is stuck

- How long before asking for help: 15 minutes of no progress on a single
  error, or any blocker that touches shared infrastructure (branch
  protection, CI).
- Who to ask, in what order: in a real pod, the pair partner first, then
  the pod captain, then the instructor. Solo, "asking for help" means
  consulting the workshop docs (`NFR.md`, `SCENARIO.md`, the acceptance
  suite) or the reference implementation on `f1-s1-start` before spending
  more than 15 minutes stuck.

## 5. Signed off by

| Name | Initial |
| --- | --- |
| iPelino (repo owner, solo practice build) | IP |
