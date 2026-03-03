---
name: sdd-design
description: >
  SDD Phase 3: Design. Detailed technical specification of changes (objects, functions, SQL).
  Trigger: After proposal, when user runs /sdd-design.
metadata:
  author: dynasif
  version: "2.0 (Universal)"
---

## Purpose
To plan the code changes structurally (pseudo-code or signatures) before touching the actual files.

## What to Do

1. **Component Specification**:
   - List files/classes/objects to modify.
   - Define new functions/methods (signatures: inputs/outputs).

2. **Data Modeling**:
   - SQL changes (Schema, Migrations).
   - State changes (Store, Context, Instance Variables).

3. **Logic Flow**:
   - Pseudo-code for complex algorithms.
   - Error handling strategy.

## Output Format (design.md)

```markdown
# Design: [Title]

## Database/State Changes
- `ALTER TABLE users ADD COLUMN...` OR
- New React Context for Auth

## Component Changes

### 1. [File/Class Name]
- **Function/Event**: `processData()`
- **Logic**:
  1. Validate inputs
  2. Call API
  3. Handle errors

### 2. [New File]
- **Responsibility**: Helper for data transformation.
- **Methods**: `transform(data) -> JSON`

## Validation Plan
- Unit test for transformation
- Integration test for API call
```
