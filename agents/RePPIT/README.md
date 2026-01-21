# RePPIT Framework (Research → Proposal → Plan → Implement → Test)

RePPIT is a lightweight, markdown-driven workflow for taking a request from “understand what exists” through “ship code” with structured checkpoints and minimal rework.

This directory contains the instruction files (the “agents”) for each phase. Use them **in order**.

---

## Correct Order (Recommended Workflow)

### 1) Research (`research.md`)
**Goal:** Document the codebase *exactly as it exists today* relevant to the request—no opinions, no suggested improvements.

**When to use:** Whenever you’re changing an existing system or need confidence about current behavior/structure.

**Output:** A structured research document (typically placed in `agents/research/` per the instructions in `research.md`) with concrete file path + line references.

---

### 2) Proposal (`proposal.md`)
**Goal:** Turn research + the user’s request into **1–2 solution approaches** grounded in what was discovered.

**Hard requirement:** A research document from step 1.

**Output:** “Solution Proposals” with trade-offs, validation ideas, and open questions.

---

### 3) Plan (`plan.md`)
**Goal:** Produce an implementation plan *without writing any code*.

**Key behavior:** Clarify scope/constraints first, mirror the design-doc template structure (as directed by `plan.md`), and write a concise, actionable plan.

**Output:** A plan markdown file (commonly under a `tasks/`-like location, depending on your repo conventions).

---

### 4) Implement (`implement.md`)
**Goal:** Execute the plan by writing production-quality code incrementally and validating as you go.

**Hard requirement:** A plan document exists (and any referenced research has been read).

**Output:** Code changes + tests + any necessary docs/config updates, strictly matching the plan (no scope creep).

---

### 5) Test / Review (`test.md`)
**Goal:** Review all uncommitted changes (staged + unstaged) and produce a prioritized action list.

**When to use:** Before you consider the work “done” or ready for PR, and anytime you want a tight feedback loop on a diff.

**Output:** A concise code review summary + prioritized action items with file:line references.

---

## File-to-Step Mapping (What Each Markdown File Does)

| Step | File | Purpose | Inputs | Outputs |
|------|------|---------|--------|---------|
| 1 | `research.md` | Describe current codebase state relevant to the query; **no suggestions** | User request + any mentioned files | Research document with path:line references |
| 2 | `proposal.md` | Generate 1–2 solution proposals grounded in research | Request + research doc | Two proposals with trade-offs/validation/open questions |
| 3 | `plan.md` | Write an implementation plan only (no code changes) | Chosen proposal + constraints | Plan doc (structured, actionable) |
| 4 | `implement.md` | Implement the plan incrementally with tests and validation | Plan doc (+ research if referenced) | Production-ready code changes |
| 5 | `test.md` | Review uncommitted changes and produce action items | Git status/diffs/log | Prioritized fix list with file:line refs |

---

## How to Use This Directory (Practical Guidance)

1. Start with `research.md` whenever you’re not 100% sure how the current system works.
2. Use `proposal.md` to convert research into decision-ready options.
3. Use `plan.md` to lock scope and sequence before touching code.
4. Use `implement.md` to build exactly what’s in the plan, incrementally, with tests.
5. Use `test.md` to review your uncommitted diff and generate must-fix/recommended/consider items.

---

## Common Guardrails (What RePPIT Optimizes For)

- **No guessing:** research first, cite file paths and line ranges.
- **Decision before execution:** proposals + plan before implementation.
- **No scope creep:** implementation follows the plan.
- **Continuous validation:** tests and checks as you implement.
- **Tight feedback:** review uncommitted changes before declaring done.

---

## Suggested Prompts (Optional)

- Research:
  - “Use `agents/RePPIT/research.md` to document how `<feature>` works today and where changes should hook in.”
- Proposal:
  - “Based on `agents/research/<doc>.md`, use `agents/RePPIT/proposal.md` to propose two approaches for `<request>`.”
- Plan:
  - “Use `agents/RePPIT/plan.md` to write a plan for Proposal 1 with acceptance criteria and rollout notes.”
- Implement:
  - “Use `agents/RePPIT/implement.md` to implement the plan in `tasks/<plan>.md` and add tests.”
- Test/Review:
  - “Use `agents/RePPIT/test.md` to review my uncommitted changes and list must-fix items first.”

---

## Notes

- If you skip `research.md`, you’ll often pay for it later with rework—RePPIT is designed to avoid that.
- If research reveals unknowns that block proposals/plans, go back to `research.md` and expand the investigation rather than guessing.