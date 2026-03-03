# AI Agent Skills - PowerBuilder 11.5 / Dynasif

This directory contains **Agent Skills** following the [Agent Skills open standard](https://agentskills.io). Skills provide domain-specific patterns, conventions, and guardrails that help AI coding assistants (Claude Code, Gemini CLI, Cursor, Codex, etc.) understand PowerBuilder 11.5 and Dynasif project requirements.

## What Are Skills?

[Agent Skills](https://agentskills.io) is an open standard format for extending AI agent capabilities with specialized knowledge. Originally developed by Anthropic and released as an open standard, it is now adopted by multiple agent products.

Skills teach AI assistants how to perform specific tasks. When an AI loads a skill, it gains context about:

- Critical rules (what to always/never do)
- Code patterns and conventions
- Project-specific workflows
- References to detailed documentation

## Setup

Run the setup script to configure skills for all supported AI coding assistants:

```bash
cd skills
./setup.sh
```

This creates symlinks so each tool finds skills in its expected location:

| Tool | Symlink Created |
|------|-----------------|
| Claude Code | `.claude/skills/` |
| Gemini CLI | `.gemini/skills/` |
| Codex (OpenAI) | `.codex/skills/` |
| GitHub Copilot | `.github/copilot-instructions.md` (copy of AGENTS.md) |

After running setup, restart your AI coding assistant to load the skills.

## Available Skills for PowerBuilder 11.5

### Core PowerBuilder Skills

| Skill | Description | Auto-invoke when |
|-------|-------------|------------------|
| `datawindow` | .srd editing, DDDW, validations | Working with .srd files, dw_ objects |
| `functions` | Syntax, tildes, variables | Working with .srf files, function calls |
| `window` | Events, controls, patterns | Working with .srw files, w_ objects |
| `nvo` | Clean Architecture, business logic | Working with .sru files, nvo_ objects |

### Skill Details

#### datawindow
- **File**: `datawindow/SKILL.md`
- **Topics**: Editing .srd files safely, DDDW patterns, ~tif syntax, control IDs
- **References**:
  - `references/editing-srd.md` - Complete .srd editing guide
  - `references/dddw-patterns.md` - DropDownDataWindow patterns
  - `references/validation-rules.md` - Common validations

#### functions
- **File**: `functions/SKILL.md`
- **Topics**: Function calls (assign first), HEX encoding for tildes, variable declaration
- **Key Rules**:
  - Assign function result to variable BEFORE using in IF
  - Use `$$HEX1$$f300$$ENDHEX$$` format for ó (and other tildes)
  - Declare ALL variables at START of function

#### window
- **File**: `window/SKILL.md`
- **Topics**: Window events (Constructor vs Open), controls, master-detail patterns
- **Key Rules**:
  - Constructor runs BEFORE Open
  - Use SetTransObject before Retrieve
  - Follow naming conventions (dw_, cb_, sle_, st_)

#### nvo
- **File**: `nvo/SKILL.md`
- **Topics**: Clean Architecture (4 layers), entities, services, repositories
- **Key Rules**:
  - Use Clean Architecture for NEW features only
  - Don't refactor legacy code unless necessary
  - Follow naming: nvo_entity, nvo_service, nvo_repository

## How to Use Skills

Skills are automatically discovered by the AI agent when you run `./skills/setup.sh`.

### Auto-invocation

Skills auto-invoke based on:
- File extensions (.srd, .srf, .srw, .sru)
- Object prefixes (dw_, w_, nvo_)
- Keywords in conversation (datawindow, DDDW, tildes)

See [AGENTS.md](../AGENTS.md) for complete auto-invoke rules.

### Manual loading

To manually load a skill during a session:

```
Read skills/datawindow/SKILL.md
```

## Directory Structure

```
skills/
├── datawindow/
│   ├── SKILL.md              # Main skill file
│   └── references/           # Detailed docs
│       ├── editing-srd.md
│       ├── dddw-patterns.md
│       └── validation-rules.md
├── functions/
│   ├── SKILL.md
│   └── references/
├── window/
│   ├── SKILL.md
│   └── references/
├── nvo/
│   ├── SKILL.md
│   └── references/
├── setup.sh                  # Setup script for multi-LLM
└── README.md                 # This file
```

## Why Skills Instead of Just Documentation?

1. **Progressive disclosure**: SKILL.md is concise, references/ has details
2. **Auto-invocation**: Skills load automatically based on context
3. **Multi-LLM support**: One skills/ folder, multiple AI assistants
4. **Structured format**: YAML frontmatter + markdown for consistency
5. **Zero duplication**: Symlinks mean one source of truth

## Design Principles

- **Concise**: Only include what AI doesn't already know
- **Progressive disclosure**: Point to detailed docs, don't duplicate
- **Critical rules first**: Lead with ALWAYS/NEVER patterns
- **Minimal examples**: Show patterns, not tutorials

## Adding New Skills

1. Create directory: `skills/{skill-name}/`
2. Add `SKILL.md` with required frontmatter:
   ```yaml
   ---
   name: skill-name
   description: >
     Brief description.
     Trigger: When to auto-invoke this skill.
   metadata:
     scope: [root]
     auto_invoke: "Description for AGENTS.md table"
   allowed-tools: Read, Edit, Write, Glob, Grep, Bash
   ---
   ```
3. Add content: Critical Rules, examples, references
4. Create `references/` for detailed docs
5. Update [AGENTS.md](../AGENTS.md) auto-invoke table
6. Re-run `./skills/setup.sh`

## Resources

- [Agent Skills Standard](https://agentskills.io) - Open standard specification
- [Agent Skills GitHub](https://github.com/anthropics/skills) - Example skills
- [Claude Code Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - Skill authoring guide
- [Dynasif AGENTS.md](../AGENTS.md) - Project-specific agent rules
- [Dynasif CLAUDE.md](../CLAUDE.md) - Claude Code configuration

---

**Last updated:** 2026-01-15
**Version:** 1.0
