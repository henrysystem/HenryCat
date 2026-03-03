# Claude Code Configuration - Dynasif

## 🧠 Core Knowledge Base

**For all project rules, skills, and workflows, refer to:**
👉 **[AGENTS.md](AGENTS.md)**

`AGENTS.md` is the universal source of truth for:
- Available Skills & Auto-invocation rules
- Project Structure & Tech Stack
- Git Workflow & Critical Rules
- PBL Catalog

---

## ⚡ Claude-Specific Optimization

### 1. Token Efficiency (Lazy Loading)
- **Startup**: Read **ONLY** `SESSION_STATE.md` to get immediate context.
- **Deep History**: Read `HISTORIAL_BRANCHES_MERGEADOS.md` **ONLY** if you need to search for a specific past task.
- **Catalog**: Read `CATALOGO_OBJETOS_PBL.md` **ONLY** when adding new objects or searching for PBLs.
- **Do NOT read all docs at start.**

### 2. SDD Workflow (Agent Teams)
**For complex features, use the Spec-Driven Development flow:**

1.  **Explore**: `/sdd-explore` -> Loads `skills/sdd-explore/SKILL.md`
2.  **Propose**: `/sdd-propose` -> Loads `skills/sdd-propose/SKILL.md`
3.  **Design**: `/sdd-design` -> Loads `skills/sdd-design/SKILL.md`
4.  **Apply**: `/sdd-apply` -> Loads `skills/sdd-apply/SKILL.md`
5.  **Verify**: `/sdd-verify` -> Loads `skills/sdd-verify/SKILL.md`
6.  **Release**: `/sdd-release` -> Loads `skills/sdd-release/SKILL.md`

**Trigger:** When user says "start SDD", "feature mode", or uses slash commands.

### 3. Option Evaluation
**For complex tasks (>10,000 tokens estimated):**
Identify 2-3 approaches and present them before executing.

```markdown
📊 OPTION 1: [Name]
   Tokens: ~X,XXX
   Risk: [Low/Med/High]

📊 OPTION 2: [Name] (RECOMMENDED)
   Tokens: ~X,XXX
   Savings: Y% vs Option 1
   Why: [Justification]

🎯 Proceed with Option 2?
```

### 4. Edit vs Write
- **Prefer `Edit`**: For small changes in large files.
- **Prefer `Write`**: For new files or total rewrites.

---

## 🔗 Context Links (Load on Demand)
- **[AGENTS.md](AGENTS.md)** - Main Router (Always loaded)
- **[SESSION_STATE.md](SESSION_STATE.md)** - 🧠 Active Context (Read at start)
- **[HISTORIAL_BRANCHES_MERGEADOS.md](HISTORIAL_BRANCHES_MERGEADOS.md)** - 📜 Archive (Search only)
- **[CATALOGO_OBJETOS_PBL.md](CATALOGO_OBJETOS_PBL.md)** - 📚 Reference (Search only)
