---
name: chore-archive
description: >
  Organizes change artifacts into deploy folders and creates external backups.
  Trigger: When user asks to archive SQL/DML/change files or prepare deliverables.
metadata:
  author: dynasif
  version: "1.0 (Universal)"
---

## Purpose
Standardize release artifacts in-repo and outside the repo, without losing QA traceability.

## Core Rules
- Use branch name as archive folder name by default.
- Move loose change files to `deploy/<branch_name>/` inside repo.
- Copy (do not move) from `deploy/<branch_name>/` to external backup.
- Never delete source code or business files outside archive patterns.

## Input Resolution
1. Resolve `branch_name` from git.
2. Resolve `change_name`:
   - Default: `branch_name`
   - Optional override from config
3. Resolve external backup root from config/env.

## Default Include Patterns
- `*.sql`
- `*.dml`
- `CAMBIOS*.txt`
- `CHANGELOG*.txt`

## Default Exclude Patterns
- `deploy/**`
- `.git/**`
- `**/node_modules/**`
- `**/vendor/**`

## Workflow
1. Dry-run: show files that will be moved.
2. Ensure `deploy/<branch_name>/` exists.
3. Move matched loose files to `deploy/<branch_name>/`.
4. Ensure external folder `<backup_root>/<change_name>/` exists.
5. Copy archived files from deploy folder to external backup.
6. Report summary with moved/copied/skipped counts.

## Config (Project-level)
Read optional `.ai-config.yml`:

```yaml
archive:
  internal_root: "deploy"
  use_branch_as_change_name: true
  include:
    - "*.sql"
    - "*.dml"
    - "CAMBIOS*.txt"
  exclude:
    - "deploy/**"
  external_backup_root: "D:/Backups/Funcionalidades/Respaldos"
```

Override with env vars when needed:
- `ARCHIVE_EXTERNAL_ROOT`
- `ARCHIVE_CHANGE_NAME`
