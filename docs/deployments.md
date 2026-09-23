# Deployment and Rollback

The repository currently implements the promotion contract as an ephemeral
validation deployment: the exact image that would be promoted is pulled by
digest, started with PostgreSQL, migrated explicitly, and checked through
`/health`. A cloud-specific adapter can replace the local Docker runtime later
without changing the image or promotion workflow contract.

## Promotion

1. Merge the change to `main` and wait for `ci` to publish the image.
2. Open **Actions > deploy > Run workflow** from `main`.
3. Enter a commit-SHA tag or semver tag produced by the publish job.
4. Confirm that the workflow records the resolved image digest and health check.

The production environment is intentionally named in the workflow so branch
rules, environment variables, and required reviewers can be enabled in GitHub
without changing the application.

## Rollback

Run the same workflow with the tag of a previously validated image. The
workflow resolves that tag to its digest before starting it, so rollback does
not depend on a mutable tag remaining unchanged.

Application rollback does not automatically reverse a database migration.
Schema changes must use backward-compatible expand-and-contract steps, and any
irreversible migration needs a separate recovery procedure.
