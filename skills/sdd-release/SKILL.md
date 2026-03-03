---
name: sdd-release
description: >
  SDD Phase 6: Release & Documentation. Finalizes the task by generating documentation and updating history.
  Trigger: After verification passes, when user runs /sdd-release.
metadata:
  author: dynasif
  version: "1.0"
---

## Purpose
To cleanly close the task, document changes, update project history, and save learned knowledge.

## What to Do

1. **Generate Change Log**:
   - Create `docs/cambios/CAMBIOS_[ACTION]_[CONTEXT].txt`.
   - List modified objects and their PBLs.
   - Describe problem and solution clearly.
   - Follow standard template (see `skills/project-workflow/SKILL.md`).

2. **Update Catalog**:
   - Check if any new objects were created.
   - Add them to `CATALOGO_OBJETOS_PBL.md` if missing.

3. **Update History**:
   - Append session summary to `HISTORIAL_BRANCHES_MERGEADOS.md`.
   - Include branch name, date, and key achievements.

4. **Save Learnings (Engram)**:
   - Use `mem_save` to store key insights or patterns discovered.
   - Example: "w_pos.srw uses nvo_venta_service for calculations. Refactor opportunity in event X."

## Output Checklist
- [ ] Created `CAMBIOS_*.txt`
- [ ] Updated `CATALOGO_OBJETOS_PBL.md`
- [ ] Updated `HISTORIAL_BRANCHES_MERGEADOS.md`
- [ ] Saved learnings to Engram
