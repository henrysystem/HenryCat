---
name: model-routing
description: >
  Defines model orchestration policy by task type, with fallback when limits are reached.
  Trigger: When selecting AI model/provider strategy for analysis, coding, or debugging.
metadata:
  author: dynasif
  version: "1.0 (Universal)"
---

## Purpose
Provide a portable decision layer for multi-model workflows in any project.

## Orchestrator Layer
The orchestrator is policy-based:
- Router: `AGENTS.md`
- Execution modules: project `skills/`
- Model policy: this skill + optional `.ai-config.yml`

## Default Policy
- Deep analysis / architecture: prefer `gemini`
- Main implementation: prefer `opus`
- Bug fixing / precision edits: prefer `codex`
- If preferred model is unavailable or quota-limited: use configured fallback order.

## Fallback Rules
1. Try preferred model.
2. If quota/availability fails, try next model.
3. If none available, continue with session default.
4. Log selected model in task notes when relevant.

## Config (Project-level)
Read optional `.ai-config.yml`:

```yaml
model_routing:
  enabled: true
  policy:
    analysis: ["gemini", "opus", "codex"]
    coding: ["opus", "codex", "gemini"]
    bugfix: ["codex", "opus", "gemini"]
  on_limit: "fallback"
```

This is vendor-agnostic guidance; apply using each tool's native model selection mechanism.
