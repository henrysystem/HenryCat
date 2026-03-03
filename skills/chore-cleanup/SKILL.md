---
name: chore-cleanup
description: >
  Safe workspace cleanup for temporary artifacts across any tech stack.
  Trigger: When user asks to clean workspace, remove temp files, or prepare branch before review.
metadata:
  author: dynasif
  version: "1.0 (Universal)"
---

## Purpose
Remove disposable files safely without touching source code, migration scripts, or release artifacts.

## Safety Rules
- Always run in dry-run mode first and show a deletion preview.
- Never delete tracked git files unless user explicitly asks.
- Never delete inside `.git/`, `node_modules/`, `vendor/`, `.venv/`, or `venv/` by default.
- If pattern is ambiguous, keep the file and report it.

## Default Cleanup Targets

### Temporary Files
- `~*`
- `*.tmp`
- `*.temp`
- `*.swp`
- `*.swo`
- `*.cache`

### Crash Dumps
- `*.dmp`
- `*.mdmp`
- `minidump*`

### Environment Logs
- `SCRIPT_*.LOG`
- `SCRIPT_*.log`

### Optional (ask before delete)
- `*.bak`
- `*.old`
- `*.orig`

## Generic Workflow
1. Detect repo root and current branch.
2. Build candidate list with include + exclude patterns.
3. Show grouped preview by folder and extension.
4. Delete only approved targets.
5. Print final report: deleted, skipped, protected.

## Config (Project-level)
Read optional `.ai-config.yml`:

```yaml
cleanup:
  include:
    - "~*"
    - "*.tmp"
    - "*.dmp"
    - "SCRIPT_*.LOG"
  exclude:
    - ".git/**"
    - "deploy/**"
    - "**/*.sql"
  optional_requires_confirm:
    - "*.bak"
```

If config is missing, use defaults above.
