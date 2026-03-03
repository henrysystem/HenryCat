---
name: memory-protocol
description: >
  Protocol for persistent memory (Engram). Rules for saving decisions, searching context, and closing sessions.
  Trigger: When making decisions, fixing bugs, learning patterns, or closing sessions.
metadata:
  author: dynasif
  version: "1.0"
---

## Purpose
To combat "amnesia" between sessions. We save **signals** (decisions, learnings), not noise.

## Core Rules

### 1. Save Proactively (`mem_save`)
**When to save:**
- **Decision**: "Chose approach A over B because..."
- **Bugfix**: "Fixed invalid HEX syntax in w_pos."
- **Discovery**: "Found that table X uses column Y for status."
- **Pattern**: "Project uses nvo_service for logic."

**Format:**
```text
**What**: [One sentence summary]
**Why**: [Motivation/Reason]
**Where**: [Files/Objects affected]
**Learned**: [Gotchas/Tips]
```

### 2. Search First (`mem_search`)
**When to search:**
- Before asking "how do I...?"
- Before re-implementing a feature.
- When error messages look familiar.

### 3. Close Session (`mem_session_summary`)
**ALWAYS** run this before exiting:
```text
## Goal
[What we did]

## Accomplished
- [x] Task 1
- [x] Task 2

## Next Steps
- [ ] Task 3
```

## Project Identification (Critical)

Always use the current working directory name as project identifier.
Example: if working in `D:\Pintulac\01_PRODUCCION\dynasif`, use `--project dynasif`.

This ensures memories stay scoped per project and do not leak across codebases.

## Tools (Engram MCP)
- `mem_save`: Save a note.
- `mem_search`: Search notes.
- `mem_session_summary`: Save session summary.
- `mem_context`: Get context from previous session.

## MCP Configuration (Multi-LLM)

Engram runs as a single MCP server. Each LLM needs its own config file:

- **Claude Code**: `.claude/config.json`
- **Gemini CLI**: `.gemini/settings.json`
- **Codex**: `.codex/config.json`

All point to the same binary: `engram.exe mcp`
All share the same database: `~/.engram/engram.db`
