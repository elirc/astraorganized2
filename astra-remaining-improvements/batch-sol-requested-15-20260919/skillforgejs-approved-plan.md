# SkillForgeJS approved plan

## Defect and boundary

Lesson completion could commit before review seeds and gamification awards. A later failure left the lesson complete, while a retry saw the completion and skipped the missing effects. Concurrent repeats could also observe an incomplete award summary.

## Change

- Put eligibility, the unique completion insert, review seeds, lesson XP, quest progress, and achievement writes in one Prisma interactive transaction.
- Thread the transaction client and one injected timestamp through every nested helper while preserving optional defaults for existing callers.
- Treat only the exact lesson-completion `P2002` target as the idempotent loser and return a no-award summary using the same injected client.
- Retry only bounded, recognized SQLite lock/write-conflict errors.

## Acceptance and verification

A helper-owned temporary SQLite database must prove ineligible lessons write nothing, first completion creates exact-time review states and one award path, a late injected failure rolls every write back, and two real concurrent calls leave one completion, one review-state set, one lesson XP event, and one quest advancement. Run the focused test runner plus typecheck after dependencies are available.
