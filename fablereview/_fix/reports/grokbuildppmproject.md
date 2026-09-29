# grokbuildppmproject — fix report (B15)

Fable, 2026-09-18.

## Done
- review#1 README says taskController was deliberately not changed (present on disk before this pass; verified)
- review#2 05 opens with the workspace note (present on disk before this pass; verified)
- review#3 02 has the Express 4 rejected-async-handler section (present on disk before this pass; verified)
- review#4 05 exercise 8 proves one claim against a real database (present on disk before this pass; verified)

## Skipped
- (none)

## Verification
- No edits needed: all four review items were found already applied on disk (no earlier progress line existed); verified by reading README, 02 and 05

## Course/code consistency check
- README, 02 and 05 agree on the controller-unchanged lesson and the workspace note.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **07** - backend/src/services/taskService.ts (createTaskSchema/updateTaskSchema)

No source code was changed; only the chapter Markdown.
