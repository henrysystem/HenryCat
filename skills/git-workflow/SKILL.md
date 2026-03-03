---
name: git-workflow
description: >
  Git workflow for Dynasif: branch management, merge strategy, conflict resolution, QA approval.
  Trigger: When creating branches, merging, pushing, resolving conflicts, or managing git workflow.
metadata:
  author: dynasif
  version: "1.0"
---

## When to Use

- Before creating any new branch.
- When ready to merge changes to `devhenry`.
- When handling merge conflicts.
- When cleaning up old branches.

## Core Rules

### ALWAYS
1. **Ask user** before creating a new branch.
2. **Sync with `devhenry`** before merging (pull + merge devhenry into branch).
3. **Complete pre-merge checklist** before merging to devhenry.
4. **Keep branches alive** until QA approves (NEVER delete immediately after merge).
5. **Use underscore `_`** in branch names (NEVER slash `/`).
6. **Push to remote** immediately after merge.
7. **Document merge** in `HISTORIAL_BRANCHES_MERGEADOS.md`.

### NEVER
1. **Delete branches** without explicit QA approval.
2. **Use slash `/`** in branch names (PowerBuilder 11.5 incompatible).
3. **Merge** without syncing with `devhenry` first.
4. **Accumulate changes** for more than 7 days in a branch.
5. **Force push** to `devhenry`.

## Branch Naming

Pattern: `[type]_[description_with_underscores]`

| Type | Description | Example |
|------|-------------|---------|
| `fix` | Bug fixes | `fix_decimales_cc_tarjeta` |
| `feat` | New features | `feat_validacion_stock_proforma` |
| `refactor` | Code restructuring | `refactor_login_logic` |
| `docs` | Documentation only | `docs_actualizar_readme` |
| `chore` | Maintenance | `chore_limpieza_branches` |

## Workflow

### 1. Before Starting Work
1. **Check pending branches**:
   ```bash
   git branch --no-merged devhenry
   ```
   *If conflicts with your planned work, suggest merging first.*

2. **Clean old branches**:
   ```bash
   git branch --merged devhenry
   ```
   *Suggest deleting branches merged >7 days ago (with user approval).*

3. **Create new branch** (if approved):
   ```bash
   git checkout devhenry && git pull origin devhenry
   git checkout -b feat_nombre_branch
   ```

### 2. During Development
- Sync with `devhenry` daily if working multiple days.
- One branch = one feature/fix.

### 3. Pre-Merge Checklist
- [ ] `git checkout devhenry && git pull`
- [ ] `git checkout [branch] && git merge devhenry`
- [ ] Conflicts resolved & compiles successfully
- [ ] `CATALOGO_OBJETOS_PBL.md` updated
- [ ] `CAMBIOS_*.txt` created
- [ ] Commit messages descriptive
- [ ] No debug code left

### 4. Merging to devhenry
```bash
git checkout devhenry
git merge [branch]
git push origin devhenry
# STOP - Do NOT delete branch yet!
```

## QA Approval Policy

**CRITICAL:** PowerBuilder projects require compilation and rigorous testing.
1. **NEVER** delete a branch immediately after merging.
2. **Wait** for QA confirmation that tests passed.
3. **Delete** only when explicit approval is given or >7 days have passed safely.

## Conflict Resolution

1. Identify files: `git status`
2. Analyze both versions (yours vs incoming).
3. **PowerBuilder objects (.srw, .srd)**:
   - Be extremely careful with binary header changes.
   - Prefer keeping the most recent logic if functionally compatible.
4. Commit resolution: `git commit -m "merge: Resolve conflicts"`
5. **COMPILE IMMEDIATELY** after resolving.
