---
description: Scaffold a well-designed agent loop with best-practice coaching and cross-model review
---

Scaffold an agent loop in the target directory (default: ./looper-output). If --template <name> given, use that pattern (security-scan, code-review, bug-hunt, docs-sync, research-synthesis). Interview goal, verification criteria, host model, council (reviewer+judge), gates/control (max_iterations, no-progress stop, budget cap). Show ASCII preview, emit loop.yaml + LOOP.md + RUN_IN_SESSION.md + run-loop.py. If target has existing loop.yaml, treat as edit/resume.
