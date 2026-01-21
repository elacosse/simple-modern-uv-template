# Blueprint Framework (Research → Plan → Define → Implement → Test → Refine)

Blueprint is a markdown-driven workflow for going from an initial request to verified changes using a small set of ordered steps. Each step’s behavior is defined by a dedicated instruction file in this directory.

Use the steps **in order** unless you are explicitly resuming an in-progress workflow or clearing generated workflow files.

---

## Correct Order (Recommended Workflow)

### 1) Research (`research.md`) — `/blueprint:research`
**Goal:** Research a topic and capture findings for planning.

**Key rules:**
- Do not change files unless the user explicitly requests it.
- Prefer user-provided links/docs over conflicting web info.

**Output:** Write findings to `RESEARCH.md`.  
If `RESEARCH.md` already exists, you must ask the user whether to overwrite, create a new `tasks/<name>/` directory, or create a VCS branch/workspace.

**Next step:** `/blueprint:plan`

---

### 2) Plan (`plan.md`) — `/blueprint:plan`
**Goal:** Produce a concise, step-by-step plan before any implementation.

**Key rules:**
- First locate and include `RESEARCH.md` (it may be under `tasks/<name>/`).
- Ask clarifying questions and do not execute the plan.

**Output:** Write the plan to `PLAN.md`.  
If `PLAN.md` exists, you must ask the user whether to overwrite, create a new `tasks/<name>/` directory, or create a VCS branch/workspace.

**Next step:** `/blueprint:define`

---

### 3) Define (`define.md`) — `/blueprint:define`
**Goal:** Decompose `PLAN.md` into an actionable task list.

**Key rules:**
- First locate and use `PLAN.md` (may be under `tasks/<name>/`).
- Write tasks as Markdown checkboxes, with indentation for parent/child tasks.
- Tag tasks with categories (e.g. `[frontend]`, `[backend]`, `[test]`) and note parallelizable work.

**Output:** Write the task list to `TODO.md`.  
If `TODO.md` exists, you must ask the user whether to overwrite, create a new `tasks/<name>/` directory, or create a VCS branch/workspace.

**Next step:** `/blueprint:implement`

---

### 4) Implement (`implement.md`) — `/blueprint:implement`
**Goal:** Execute `TODO.md` and produce high-quality code changes.

**Key rules:**
- First locate `PLAN.md` and `TODO.md` (may be under `tasks/<name>/`).
- Follow `TODO.md` sequentially; adhere to existing conventions and architecture.
- Mark completed tasks in `TODO.md` (`- [x] ...`).
- Explain destructive commands before running them.
- Run relevant verification steps when possible.

**Output:** Code changes plus an `ACT.md` implementation log (append with timestamps).

**Next step:** `/blueprint:test`

---

### 5) Test (`test.md`) — `/blueprint:test`
**Goal:** Verify the implementation with an explicit, user-approved test plan.

**Key rules:**
- First locate `PLAN.md`, `TODO.md`, and `ACT.md`.
- If command arguments provide test instructions, those override everything else.
- Otherwise, derive a plan from `PLAN.md` / `TODO.md`, or propose one from existing repo tests.
- Present the test plan and wait for user approval before executing tests.

**Output:** A `TEST.md` log containing the approved plan, commands run, output, and pass/fail results.

**Next step:** If failures occur, refine plan/tasks and proceed via `/blueprint:refine` (or as appropriate).

---

### 6) Refine (`refine.md`) — `/blueprint:refine`
**Goal:** Incorporate user feedback and iterate on the appropriate workflow artifacts.

**Key rules:**
- Gather context by locating `RESEARCH.md`, `PLAN.md`, `TODO.md`, `ACT.md`, `TEST.md`.
- Identify what needs refinement, propose a plan, and get approval before changes.
- Update the relevant file(s): `PLAN.md`, `TODO.md`, `ACT.md`, `TEST.md` depending on what changed.

**Output:** Updated workflow artifacts and a summary for final approval.

---

## Utility Commands

### Resume (`resume.md`) — `/blueprint:resume`
**Goal:** Determine where you left off and recommend the next step.

**How it works:**
- Finds workflow files (`RESEARCH.md`, `PLAN.md`, `TODO.md`, `ACT.md`, `TEST.md`) in the current directory and subdirectories (like `tasks/`).
- Determines the most advanced existing file by precedence:
  `TEST.md` → `ACT.md` → `TODO.md` → `PLAN.md` → `RESEARCH.md`
- If files are found outside the current directory, it must stop and ask you to confirm they’re the correct ones before continuing.
- If required “earlier” files are missing, it must stop and ask how you want to proceed.

### Clear (`clear.md`) — `/blueprint:clear`
**Goal:** Remove all workflow-generated files.

**What it deletes (after explicit confirmation):**
- `RESEARCH.md`
- `PLAN.md`
- `TODO.md`
- `ACT.md`
- `TEST.md`

---

## Command-to-Instruction File Mapping

| Command | Instruction file (this directory) | What it does | Produces/updates |
|--------:|-----------------------------------|--------------|------------------|
| `/blueprint:research` | `research.md` | Research and summarize findings | `RESEARCH.md` |
| `/blueprint:plan` | `plan.md` | Create an implementation plan (no execution) | `PLAN.md` |
| `/blueprint:define` | `define.md` | Turn the plan into a TODO checklist | `TODO.md` |
| `/blueprint:implement` | `implement.md` | Implement tasks and log actions | `ACT.md` (+ code changes) |
| `/blueprint:test` | `test.md` | Create/execute an approved test plan and log results | `TEST.md` |
| `/blueprint:refine` | `refine.md` | Apply feedback and iterate on the right artifact | `PLAN.md` / `TODO.md` / `ACT.md` / `TEST.md` |
| `/blueprint:resume` | `resume.md` | Determine current workflow state and next step | (no required new file) |
| `/blueprint:clear` | `clear.md` | Find + delete workflow files (with confirmation) | (deletes workflow files) |

---

## Practical Usage

1. Start: `/blueprint:research <topic>`
2. Plan: `/blueprint:plan <task>`
3. Break down work: `/blueprint:define`
4. Implement: `/blueprint:implement`
5. Verify: `/blueprint:test`
6. Iterate (as needed): `/blueprint:refine <feedback>`

If you’re not sure what’s next: `/blueprint:resume`  
If you want to clean up generated workflow artifacts: `/blueprint:clear`
