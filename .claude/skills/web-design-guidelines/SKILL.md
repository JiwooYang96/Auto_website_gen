---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Vercel's Web Interface Guidelines.

## How it works

1. Read the rules in `rules.md` next to this file (a saved copy, so reviews work
   offline and give the same results every run).
2. Read the specified files (or ask which files to review).
3. Check them against every rule in `rules.md`.
4. Output findings in the terse `file:line` format `rules.md` describes.

Many rules are written for React (`onClick`, `<Link>`, `priority`). For this
project's single-file HTML sites, apply the plain HTML/CSS equivalent and skip rules
that don't apply (forms, routing, data fetching) instead of reporting them.

To update the rules, replace `rules.md` with the latest `command.md` from
https://github.com/vercel-labs/web-interface-guidelines.

## Source and license

Adapted from vercel-labs/agent-skills@1a2c79d (web-design-guidelines, MIT). The original
fetches the rules from GitHub on every run; this copy reads `rules.md` instead.
`rules.md` is `command.md` from vercel-labs/web-interface-guidelines@434b7f9
(MIT, see LICENSE).
