---
name: skill-creator
description: >
  Generates new Agent Skills following the Gentleman-Skills standard.
  Trigger: When user asks to "create a new skill", "add support for X", or "learn a new library".
metadata:
  author: dynasif
  version: "1.0"
---

## Purpose
To standardize knowledge capture. Instead of answering a question once, we create a reusable skill file.

## Workflow

### 1. Gather Information
Ask the user for:
- **Name**: Short, lowercase, hyphenated (e.g., `react-query`).
- **Description**: What it does and when to use it (Trigger).
- **Critical Rules**: What to ALWAYS do and NEVER do.
- **Patterns**: Code snippets or examples.

### 2. Generate File
Create a new file at `skills/[category]/[name]/SKILL.md` with this template:

```markdown
---
name: [name]
description: >
  [description]
  Trigger: [triggers]
metadata:
  author: [user/project]
  version: "1.0"
---

## When to Use
[Context description]

## Core Rules

### ALWAYS
- [Rule 1]
- [Rule 2]

### NEVER
- [Rule 1]
- [Rule 2]

## Examples
[Code snippets]
```

### 3. Register
- Append the new skill to `AGENTS.md` table.
- (Optional) Update `setup.sh` or install script if needed.

## Proactive Usage
If you find yourself explaining the same concept twice (e.g., "In React we use hooks..."), PROPOSE creating a skill for it.
