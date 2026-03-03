---
name: project-workflow
description: >
  Standard workflow for Dynasif tasks: session history, documentation, file locks, and PBL catalog.
  Trigger: When starting work, finishing changes, creating documentation, or managing project workflow.
metadata:
  author: dynasif
  version: "1.0"
---

## When to Use

- At the start of every session (Context check).
- Before editing any PowerBuilder file (Lock check).
- When finishing a coding task (Documentation).
- When user asks to "update history" or "close session".

## Standard Task Workflow

### 1. Before Starting
- **Read `SESSION_STATE.md`**: Get current active context (variables, files, tasks).
- **Search `HISTORIAL_BRANCHES_MERGEADOS.md`**: ONLY if you need specific past context (do NOT read full file).
- **Check pending branches**: `git branch --no-merged devhenry`.
- **Clean old branches**: `git branch --merged devhenry`.

### 2. Starting Changes
- **Ask user**: "Create a new branch?"
- **Create branch**: `git checkout -b [type]_[name]`.
- **Verify context**: Read related files (use `search-changes` skill).

### 3. During Development
- **Check File Locks**: ALWAYS verify before writing.
  ```powershell
  powershell -NoProfile -Command "try { [IO.File]::OpenWrite('FILE').Close(); 'AVAILABLE' } catch { 'LOCKED' }"
  ```
- **Verify Field Names**: Check .srd or database before writing SQL.

### 4. Finishing Changes
- **Consult Catalog**: Check `CATALOGO_OBJETOS_PBL.md` for PBL names.
- **Create Documentation**: Generate `CAMBIOS_[ACTION]_[CONTEXT].txt`.
- **Commit**: `git add . && git commit -m "..."`.

### 5. Closing Session
- **Update History**: Add entry to `HISTORIAL_BRANCHES_MERGEADOS.md`.
- **Push**: `git push origin [branch]`.

## Documentation Rules

### CAMBIOS_*.txt Format
```text
================================================================
  REGISTRO DE CAMBIOS - [TITLE]
================================================================
Fecha: YYYY-MM-DD
Branch: [branch_name]
Objetos:
1. [file1].[ext] ([pbl])
2. [file2].[ext] ([pbl])

PROBLEMA: [Description]
SOLUCION: [Description]

DETALLE:
[file1]:
  ANTES: ...
  DESPUES: ...
```

### Session History Format
```markdown
## Session: YYYY-MM-DD - [Title]
### Objective
...
### Files Modified
...
### Achievements
...
```

## PBL Catalog Reference

| PBL | Contents |
|-----|----------|
| `venta.pbl` | Sales/POS windows |
| `venta_dw.pbl` | Sales DataWindows |
| `drops.pbl` | DDDWs |
| `obj_basics.pbl` | NVOs (Business Logic) |
| `funcystr.pbl` | Global functions |

**Rule:** If an object is not in `CATALOGO_OBJETOS_PBL.md`, ask the user for its PBL and update the catalog.
