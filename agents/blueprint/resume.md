You have been asked to resume the most recent workflow.

## Resume Workflow

Your goal is to determine where the user left off and recommend the next logical step.

A workflow is defined by one or more of the following files:
1. `RESEARCH.md`
2. `PLAN.md`
3. `TODO.md`
4. `ACT.md`
5. `TEST.md`

## Resume Rules
*  Do not expect all 5 files to always be present.
*  The order of the files is paramount; if a file lower on the list exists, it is expected that the previous file must also exist. The only exception to this rule is `RESEARCH.md`.
*  If an expected file is not found, stop the resume task and raise this as an issue to the user. Ask the user how they want to proceed. The user _may_ choose to proceed without one of the required files; inform them of that option as well as any other options you believe relevant. Only if the user explicitly requests you continue without a required file should you do so.

## Resume Steps

Follow the steps below to resume the user's workflow.

1.  **Find Files:** Use your tools to search for workflow files in the current directory and any subdirectories (like `tasks/`).
2.  **Determine suitability:** If workflow files are not found in the current directory (the default) but are found elsewhere (like `tasks/`), _stop and ask the user if these are the correct files before proceeding to the next step._
3.  **Determine State:** Determine the last completed task by identifying the existing workflow file with the highest precedence. The order of precedence is: `TEST.md` -> `ACT.md` -> `TODO.md` -> `PLAN.md` -> `RESEARCH.md`. Do not use file timestamps to determine the state. Proceed to locate all files *first* before confirming the current state. Note that tasks _may_ have a parent-child relationship, and if they do, ensure to make note of this for the next step.
4.  **Summarize Current State:** Based on your analysis of all of the found files, summarize the current state of the work to the user and the next action (task) to be taken. Do *not* begin refactoring work during or immediately after this step. Be brief but not so much so that it is not clear to the user what the next task is.
5.  **Unclear status:** If you cannot find any workflow files, inform the user that no active workflow was found and suggest starting with `/blueprint:research` or `/blueprint:plan`. If you are unable to clearly understand the next step from the provided files, say so to the user and recommend they come up with their own next step based on your summary and recommend they make any necessary adjustments to the files, then recommend they resume work with `/blueprint:implement`.
6.  **User feedback & refinement:** Allow the user to provide feedback on the resume plan. If the user has provided additional instruction or feedback, update the relevant workflow files and resummarize the current plan and updated next task (if applicable). Again wait for explicit user confirmation of the updated plan before proceeding.
7.  **Begin:** Once the user has given explicit instructions that the resume plan looks good, you are to begin executing the steps in `TODO.md`.
