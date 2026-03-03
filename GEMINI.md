# Gemini CLI Configuration

## Core Knowledge Base

**For all project rules, skills, and workflows, refer to:**
**[AGENTS.md](AGENTS.md)**

`AGENTS.md` is the universal source of truth for:
- Intent Classifier (when to load skills vs execute directly)
- Available Skills
- Token Optimization Policy
- Project Structure & Tech Stack

---

## Token Efficiency (Lazy Loading)

- **Startup**: Read **ONLY** `SESSION_STATE.md` to get immediate context.
- **Deep History**: Read `HISTORIAL_BRANCHES_MERGEADOS.md` **ONLY** if you need to search for a specific past task.
- **Catalog**: Read `CATALOGO_OBJETOS_PBL.md` **ONLY** when adding new objects or searching for PBLs.
- **Do NOT read all docs at start.**

## SDD Workflow

For complex features, use the Spec-Driven Development flow:

1. **Explore**: Load `skills/sdd-explore/SKILL.md`
2. **Propose**: Load `skills/sdd-propose/SKILL.md`
3. **Design**: Load `skills/sdd-design/SKILL.md`
4. **Apply**: Load `skills/sdd-apply/SKILL.md`
5. **Verify**: Load `skills/sdd-verify/SKILL.md`
6. **Release**: Load `skills/sdd-release/SKILL.md`

## Context Links (Load on Demand)

- **[AGENTS.md](AGENTS.md)** - Main Router (Always loaded)
- **[SESSION_STATE.md](SESSION_STATE.md)** - Active Context (Read at start)
- **[HISTORIAL_BRANCHES_MERGEADOS.md](HISTORIAL_BRANCHES_MERGEADOS.md)** - Archive (Search only)
- **[CATALOGO_OBJETOS_PBL.md](CATALOGO_OBJETOS_PBL.md)** - Reference (Search only)
