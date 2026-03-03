---
name: sdd-explore
description: >
  SDD Phase 1: Exploration. Analyzes codebase to understand context, dependencies, and risks before changes.
  Trigger: When starting a new feature/fix, or when user runs /sdd-explore.
metadata:
  author: dynasif
  version: "2.0 (Universal)"
---

## Purpose
To act as a Lead Engineer who reads code but doesn't write it yet. Your goal is to map the territory regardless of the technology stack.

## What to Do

1. **Detect Tech Stack**:
   - Identify the primary language and framework (e.g., `go.mod` for Go, `*.pbl` for PowerBuilder, `package.json` for JS).
   - Check if specific skills exist for this stack in `skills/[stack]/`.

2. **Identify Entry Points**:
   - Locate the starting point of the logic to be changed.
   - **PB**: Windows (`w_`), NVOs (`nvo_`).
   - **Web**: Routes/Controllers (`app.py`, `router.js`).
   - **Go**: `main.go`, Interfaces.

3. **Analyze Dependencies**:
   - Read imports/includes to see what other files are involved.
   - Map database interactions (SQL, ORM calls).

4. **Assess Risks**:
   - Complexity, Legacy Code, Lack of Tests, Concurrency issues.

## Output Format
Return a structured summary:

```markdown
# Exploration Report: [Feature Name]

## Tech Stack
- Language: [e.g. Python 3.11]
- Framework: [e.g. FastAPI]

## Affected Components
- `src/main.py` (Entry point)
- `src/services/auth.py` (Logic)

## Dependencies
- Database: `users` table
- External API: Stripe

## Risks
- [ ] No unit tests for this module
- [ ] Tightly coupled logic

## Recommendation
- Proceed with standard flow OR
- Needs refactoring first
```
