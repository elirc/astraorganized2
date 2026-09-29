# _Organized Desktop/03 Master Projects/master 6 — fix report (B10)

Fable, 2026-09-18.

## Done
- review#4 the duplicate-enrollment catch checks `error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2002"`; the existing test throws a real PrismaClientKnownRequestError and a new test proves a look-alike object is not mapped to 409
- review#2 new test: a $transaction that fails after its writes rejects the request; 04 explains why only an integration test proves the rollback
- review#2 04 section on the mocked transaction and an integration-test recipe
- review#5 02 explains the outbox row and the worker contract (lease, retry, at-least-once, consumer dedupe)
- review#3 01 workspace table, ignore list and definitions; README pacing
- review#1 three implement-it exercises with acceptance contracts (05) and answers (06)

## Skipped
- (none)

## Verification
- npm test --workspaces via junctioned stage node_modules: @lms/api 16 passed (13 delivered + 3, incl. the narrowed P2002 tests), @lms/domain 15 passed; typecheck exit 0 for @lms/api and @lms/domain (web/worker not re-run: unchanged); junctions removed

## Course/code consistency check
- The narrowed catch and the test that constructs a real PrismaClientKnownRequestError agree; the mock-rollback limit is stated in the test comment, in 04 and in the report.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (organization scope, three identities agree, published version selection, enrolled version, completion rule, requirement evaluation, completion percent, certificate eligibility, requirements not met, replay, durable effects together, domain event). Verified every term against the source before citing it: the files `apps/api/src/routes/learner.routes.ts`, `apps/api/prisma/schema.prisma`, `packages/domain/src/completion.ts`, `apps/api/src/events.ts`, and the symbols and identifiers `organizationFor`, `x-organization-id`, `findFirst`, `learner.routes.ts`, `course.currentVersionId`, `status: "PUBLISHED"`, `courseVersionId`, `model Enrollment`, `completionRuleJson`, `schema.prisma`, `completionRuleFor`, `isCourseComplete`, `calculateLessonCompletionPercent`, `canIssueCertificate`, `HttpError(409, ...)`, `status === "COMPLETED"`, `prisma.$transaction`, `recordDomainEvent`, `model DomainEvent`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **07** - apps/api/src/routes/learner.routes.ts (enroll route transaction)

No source code was changed; only the chapter Markdown.
