---
name: sdd-spec
description: >
  SDD Phase 1.5: Specification. Writes a detailed RFC/Technical Spec for complex logic.
  Trigger: For complex features (Backend, Algo-Trading), before Design phase.
metadata:
  author: dynasif
  version: "1.0"
---

## Purpose
To define the mathematical model, architecture, or protocol in detail before thinking about classes or functions. Use for Logic-Heavy tasks.

## What to Do

1. **Analyze Requirements**:
   - Understand the "Hard Problem" (e.g., Risk calculation formula, Sync protocol).

2. **Define Definitions**:
   - Glossary of terms.
   - Mathematical formulas (LaTeX style if needed).
   - State Machines diagrams (textual).

3. **Constraints**:
   - Performance (ms latency).
   - Memory usage.
   - Security constraints.

## Output Format (SPECIFICATION.md)

```markdown
# RFC: [Title]

## Abstract
High-level summary of the technical solution.

## Algorithms / Logic
### Risk Calculation
$$ Risk = (Balance * Percentage) / StopLossDistance $$

## Data Flow
1. Ingest Tick -> 2. Normalize -> 3. Calculate Indicators -> 4. Signal

## Edge Cases
- Disconnection during trade.
- Negative balance.
```
