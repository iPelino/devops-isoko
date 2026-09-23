# Value Stream: The Isoko Build Window

Pod: solo practice build (iPelino), paired with an AI assistant (GitHub Copilot
CLI) for issue drafting and implementation.

## 1. The steps

| # | Step | Process time | Wait time | What caused the wait |
| --- | --- | --- | --- | --- |
| 1 | Read `SCENARIO.md`, draft 6 vertical-slice issues (#4-#9) | ~15 min | 0 | none - single-agent drafting |
| 2 | Cross-check issues against `foundations/` (NFR.md, data-model.md, openapi.yaml, acceptance tests); fix 4 issues, add 5 backlog issues (#10-#14) | ~10 min | 0 | none |
| 3 | Scaffold Django project + wire up DRF/ruff, commit baseline | ~4 min | 0 | none |
| 4 | Implement 6 functional endpoints (health, auth, search, detail, orders x2), one commit per issue, tests green after each | ~11 min | ~1 min | waiting on test/lint runs between commits (a few seconds each, not a person) |
| 5 | Open PR #15 for review | <1 min | 0 | none |
| 6 | Human review/merge of PR #15 | - | ongoing | waiting on repo owner's review - this is the first real "wait on a person" in this value stream |

## 2. Totals

- Total lead time (first step to `make acceptance`-equivalent, i.e. all 23
  tests green): ~40 minutes across steps 1-4.
- Total process time: ~39 minutes.
- Total wait time: ~1 minute (tool/test execution, not human wait).
- **% of lead time that was waiting:** ~2.5%

This is unrepresentative of a real pod: with one person (plus an AI pair)
and no review gate yet, there was nobody to wait *on* until step 6. The
first genuine person-wait in this value stream is the open PR sitting for
review right now.

## 3. DORA metrics for the build window

| Metric | This build's number | How it was counted |
| --- | --- | --- |
| Deployment frequency | 1 (ran the server once, via `runserver`, for the smoke test) | counted live `runserver` sessions during the build |
| Lead time for changes (commit to running, typical) | ~1-2 minutes | time between a feature commit and the next manual/automated test run confirming it worked |
| Change failure rate | 0% (0/8 feature+chore commits broke the test suite) | every commit was preceded by a green `manage.py test` run |
| Failed-run recovery time | ~2 minutes | one DRF import-path error (`rest_framework.authtoken.authentication` did not exist in this DRF version) - fixed by locating the real class and correcting the settings import |

`rework rate`: not tracked - no formal review gate existed yet at the time
of the build (PR #15 review is pending, see step 6 above).

## 4. The biggest wait, and what would remove it

The biggest wait in this value stream is not in the build itself but in
what comes right after it: PR #15 has been open since the build finished
and cannot merge until a human reviews it. In a solo/practice context this
is unavoidable, but in a real pod this is exactly the wait a working
agreement (see `docs/working-agreement.md`) should shrink - by naming a
reviewer and a turnaround target *before* the first PR ever gets opened,
instead of discovering the bottleneck after the fact.
