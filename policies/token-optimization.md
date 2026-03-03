# Token Optimization Policy v1

Principle: optimize tokens without reducing quality, safety, or flexibility.
If there is any conflict, correctness wins over token savings.

## 1. Intent Classifier

Before loading any skill, classify the request:

### LEVEL 1 - TRIVIAL (0 skills, direct execution)

Signals:
- User specifies the exact file/object/control
- Visual/cosmetic change: size, position, color, title, label
- Property change: data type, width, height, format, font
- 1-3 lines affected, no business logic

Action: `grep -> read range -> edit`. No skills.

Examples:
- "Resize field X", "Change color of Y", "Widen the dropdown"
- "Change data type to datetime", "Move button to the right"
- "Fix typo in label", "Change window title"

### LEVEL 2 - MEDIUM (default: 1 skill, no subagent)

Signals:
- Localized logic in 1 object (validation, filter, calculation)
- User indicates where to make the change
- SQL involved but in 1 table/query only

Action: load 1 relevant skill (`datawindow`/`window`/`nvo`). No subagent.

Examples:
- "Add empty-field validation in w_pedidos"
- "Filter dw_clientes retrieve by status"
- "Add calculated field to DataWindow"

### LEVEL 3 - COMPLEX (skills + explore subagent)

Signals:
- Unknown where (requires exploration)
- Crosses multiple objects/tables/modules
- New business flow or redesign

Action: `sdd-explore` first, then skills based on findings, subagents as needed.

Examples:
- "Implement volume discount in billing"
- "Integrate inventory with accounting"
- "Add new tax document type"

### AMBIGUOUS -> ASK, do not escalate

If you cannot classify: ask the user 1 question first.

## 2. Skill Loading Rules

- Load a skill only at the moment it is needed, not preventively
- LEVEL 1: zero skills by default
- LEVEL 2: start with 1 skill, then expand if new evidence requires it
- LEVEL 3: `sdd-explore` first, then stack skills based on findings
- Do not load multiple skills "just in case"

## 2.1 Flexibility and Escalation (Important)

- These are default heuristics, not hard limits
- Escalate freely when risk is high (security, billing, data integrity, prod impact)
- Escalate when uncertainty remains after focused exploration
- Escalate when the user explicitly asks for deep analysis or alternatives
- Never force token savings at the cost of missing requirements

## 3. Subagent Response Format

When launching `mcp_task`/subagents, include this instruction in the prompt:

"Respond ONLY in this format (max 15 lines):
- FINDING: what you found (file:line)
- IMPACT: what it affects
- ACTION: what to do
- RISK: if any
No narrative, no explanations, no introduction."

## 4. File Read Policy

1. Always `grep`/`glob` first to locate exact lines
2. Then read with `offset` + `limit` (30-50 lines max range)
3. Never read full file unless it is smaller than 100 lines
4. For large `.srd`/`.srw`: grep by control/field name, then read +/-20 lines around match

## 5. Context Compression

When context becomes heavy (long sessions, multiple complex tasks):
- Summarize current state in 8-10 lines
- Include: decisions made, files modified, pending items
- Use that summary as working context going forward

## 6. Response Verbosity

- Default: concise (short answers, bullets, code only)
- Expand only if user explicitly asks for detail
- Avoid decorative text, repeated context, and unnecessary preambles
