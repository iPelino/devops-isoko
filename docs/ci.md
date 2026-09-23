# Continuous Integration

The root workflow runs the same local quality commands used by contributors:

- `make lint`
- `make format-check`
- `make coverage`
- an HTTP smoke test against a running Gunicorn process

The test and smoke jobs each receive a fresh PostgreSQL 16 service. Coverage is
uploaded as a short-lived artifact. Image publication runs only for push events
after all quality and smoke gates pass; pull requests never receive package
write permissions or publish images.

The image is tagged with the commit SHA and, for `v*` tags, semver tags. The
workflow exposes the resulting digest to the release job so the GitHub release
records the exact image bytes that were built.
