# Branch Protection: main

Pod: solo practice build (iPelino).

Configured via the GitHub API (`PUT /repos/iPelino/devops-isoko/branches/main/protection`)
rather than the settings UI, but the effect is identical:

- [x] Require a pull request before merging
- [x] Require at least 1 approval
- [x] Require review from Code Owners
- [x] Block force pushes
- [x] Do not allow bypassing the above settings (including for the repo owner) - `enforce_admins: true`

## Proof it works

```
$ echo "protected" >> docs/pair-test.md
$ git add docs/pair-test.md && git commit -m "test: direct push protection probe"
$ git push origin main
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: Review all repository rules at https://github.com/iPelino/devops-isoko/rules?ref=refs%2Fheads%2Fmain
remote:
remote: - Changes must be made through a pull request.
To ipelino:iPelino/devops-isoko.git
 ! [remote rejected] main -> main (push declined due to repository rule violations)
error: failed to push some refs to 'ipelino:iPelino/devops-isoko.git'
```

The test commit was then discarded locally (`git reset --hard HEAD~1`) and
never merged - `main` was left exactly as it was before the probe.
