---
name: sdd-verify
description: >
  SDD Phase 5: Verification. Quality gate to ensure code matches design and follows rules.
  Trigger: After implementation, when user runs /sdd-verify.
metadata:
  author: dynasif
  version: "2.0 (Universal)"
---

## Purpose
To act as a QA Engineer / Code Reviewer.

## What to Do

1. **Static Analysis**:
   - Read modified files.
   - Check against `design.md` requirements.

2. **Standard Verification**:
   - [ ] Syntax is valid?
   - [ ] Style guide followed (PEP8, Prettier, PB Rules)?
   - [ ] No hardcoded secrets/paths?
   - [ ] Error handling is robust?

3. **Tech-Specific Checks**:
   - **PB**: HEX tildes, SQLCA check.
   - **Python**: Type hints, `if __name__ == "__main__"`.
   - **JS**: Console.log removed, useEffect deps correct.

4. **Logic Check**:
   - Does the flow make sense?
   - Are edge cases handled?

## Output Format (verify-report.md)

```markdown
# Verification Report

## Status: PASS / FAIL / WARNING

## Checklist
- [x] Syntax Rules
- [x] Design Match
- [ ] Optimization

## Issues Found
1. **Critical**: Unhandled exception in line 50.
2. **Warning**: Variable name `x` is unclear.

## Verdict
Fix issues and re-run verify.
```
