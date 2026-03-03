---
name: sdd-propose
description: >
  SDD Phase 2: Proposal. Defines the intent, scope, and high-level approach.
  Trigger: After exploration, when user runs /sdd-propose.
metadata:
  author: dynasif
  version: "2.0 (Universal)"
---

## Purpose
To define WHAT we are going to do and WHY, before discussing HOW.

## What to Do

1. **Define Intent**:
   - One sentence summary of the goal.

2. **Define Scope**:
   - **In Scope**: What will change.
   - **Out of Scope**: What will NOT change.

3. **Define Approach**:
   - High-level strategy (e.g., "Implement Observer pattern", "Add new API endpoint", "Create new Window").

4. **Rollback Plan**:
   - How to revert if things go wrong (e.g., "Revert git branch", "Database migration down").

## Output Format (proposal.md)

```markdown
# Proposal: [Title]

## Intent
[One sentence]

## Scope
- [ ] Add Feature X
- [ ] Refactor Module Y

## Approach
[Strategy description]

## Risks & Mitigation
| Risk | Probability | Mitigation |
|------|-------------|------------|
| API Latency | Medium | Implement caching |
```
