---
name: sdd-apply
description: >
  SDD Phase 4: Implementation. Writes the actual code following the design.
  Trigger: After design approval, when user runs /sdd-apply.
metadata:
  author: dynasif
  version: "2.0 (Universal)"
---

## Purpose
To execute the changes defined in `design.md` safely and accurately.

## What to Do

1. **Load Specific Skills**:
   - Check `AGENTS.md` for available skills relevant to the current stack.
   - Example: If PB, load `datawindow`. If Python, load `pandas`.

2. **Check Locks/Context**:
   - Verify file availability (git status, locks if applicable).

3. **Execute Changes**:
   - Apply edits incrementally (one file at a time).
   - Use `Edit` tool.
   - **Test/Compile** after each edit if possible.

4. **Verify Syntax**:
   - Apply language-specific rules (from loaded skills).
   - Examples:
     - PB: Check HEX tildes.
     - Python: Check indentation and types.
     - JS: Check async/await.

## Rules
- **Stick to Design**: Do not invent new features. If design is wrong, stop and ask.
- **Incremental**: Don't do everything in one shot if it's huge.
