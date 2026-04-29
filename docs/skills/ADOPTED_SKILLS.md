# Adopted External Skills

This repository integrates a minimal, pragmatic subset of external Agent Skills to support our current workflows. We do not vend or bundle the skills; we reference them and map them to our roles and commands.

## Superpowers (obra/superpowers)
Focus: development methodology (design → plan → implement → verify).
- Adopted practices: brainstorming, writing-plans, requesting-code-review, test-driven-development, finishing-a-development-branch.
- Where used: `/prd` (spec), `/ralph` (task plan), `/start-task` (branching/plan check), `/finish-task` (verification & closure).
- Link: https://github.com/obra/superpowers

## Anthropics Skills: pdf / docx / xlsx
Focus: handling common office formats in agent workflows.
- pdf: reference for form handling and text extraction. Link: https://github.com/anthropics/skills/tree/main/skills/pdf
- docx: reference for generating/editing docs. Link: https://github.com/anthropics/skills/tree/main/skills/docx
- xlsx: reference for spreadsheets. Link: https://github.com/anthropics/skills/tree/main/skills/xlsx
- Where used:
  - Career materials: exporting resumes and structured docs.
  - AOS (Academy of Path) data sheets: consistent reading/writing of XLSX/CSV.

## Anthropics: frontend-design
Focus: design guardrails for front-end outputs.
- Where used: `frontend_analyst` and `frontend_developer` deliverables.
- Link: https://github.com/anthropics/skills/tree/main/skills/frontend-design

## Marketingskills (coreyhaines31/marketingskills)
Focus: copywriting, social content, SEO/CRO frameworks for marketing output.
- Where used: `post-writer` and `career-architect` (positioning/copy for LinkedIn, portfolio, and content).
- Primary skills adopted: `copywriting`, `copy-editing`, `social-content`, `seo-audit`, `marketing-ideas`.
- Link: https://github.com/coreyhaines31/marketingskills

## Context Engineering (muratcankoylan/agent-skills-for-context-engineering)
Focus: context management patterns (compression, optimization, memory, evaluation).
- Where used: internal agent prompts and long-running tasks (keep context small, high-signal tokens). Principles only.
- Link: https://github.com/muratcankoylan/agent-skills-for-context-engineering

## Webapp Testing & Playwright
Focus: lightweight QA of our portfolio and any future web output.
- Anthropics `webapp-testing` (checklists/examples). Link: https://github.com/anthropics/skills/tree/main/skills/webapp-testing
- Playwright Skill (optional, for true E2E automation). Link: https://github.com/lackeyjb/playwright-skill
- Where used: `/webapp-test` for smoke checks pre‑deploy.

## Skill Creator (anthropics/skill-creator)
Focus: creating our own skills in a standard format when needed.
- Where used: future internalization of bespoke SOPs (only when re-use is clear).
- Link: https://github.com/anthropics/skills/tree/main/skills/skill-creator

---

Adoption Guideline:
- Prefer referencing these skills’ checklists and patterns within our commands and roles instead of duplicating content.
- Keep the changes minimal: only integrate steps that reduce errors or speed up routine work.
- If installation of a plugin/skill is beneficial in your local agent app (Claude/Cursor), follow the linked repositories’ install instructions.

## Internal Skills
These are project-specific and live inside this repository.
- Learning Designer (Course Ops, «Профессионал +. Путь»): `.opencode/agent/learning-designer.md` — методические паттерны для архитектуры дня и сценариев.
