# Pipeline Security Checklist

| Control | Implementation |
| --- | --- |
| Default token | Workflow default is `contents: read`. |
| Job permissions | Publish and staging declare package permissions; release alone declares `contents: write`. |
| Checkout credentials | Every checkout uses `persist-credentials: false`. |
| Action integrity | Third-party actions are pinned to immutable commit SHAs with release comments. |
| Dependency updates | Dependabot updates GitHub Actions and pinned Python dependencies weekly. |
| Dependency audit | `pip-audit` runs before image publication. |
| Workflow lint | `actionlint` is downloaded at a pinned version with checksum verification. |
| Untrusted changes | Pull requests use `pull_request`; no `pull_request_target` workflow is defined. |
| Input handling | Deployment input is passed through `env`, validated, and resolved to a digest before use. |
| Secret handling | No application or registry secret is stored in workflow source; GHCR uses the run-scoped token. |
