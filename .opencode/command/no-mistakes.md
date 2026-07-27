---
description: Git gate with AI-driven validation pipeline before push
---

Sets up a local git proxy that intercepts `git push no-mistakes`, runs AI validation (review, test, lint, docs check) in a disposable worktree, and only forwards to origin after all checks pass. Modes: `init` (install gate for this repo), `status` (check current run), `approve` (approve a step), `fix` (auto-fix findings), `abort` (cancel run). Agent skill: `/no-mistakes <task>` = do task + commit + gate it. See https://kunchenguid.github.io/no-mistakes/
