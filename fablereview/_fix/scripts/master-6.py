import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'master-6'; P = fe.REG[S]['abs']; os.chdir(P); done = []

# --- review #4: narrow the P2002 catch
route = 'apps/api/src/routes/learner.routes.ts'
def narrow(t):
    old = '      if ((error as { code?: string }).code === "P2002") throw new HttpError(409, "Already enrolled in this course version");'
    new = '      if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2002") throw new HttpError(409, "Already enrolled in this course version");'
    assert old in t
    t = t.replace(old, new, 1)
    if 'import { Prisma }' not in t and 'Prisma,' not in t.split('\n', 20)[0:20].__str__():
        t = t.replace('import ', 'import { Prisma } from "@prisma/client";\nimport ', 1)
    return t
fe.rw(route, narrow)
def test_fix(t):
    old = '    testState.prisma.$transaction = vi.fn(async () => { throw { code: "P2002" }; });'
    new = '''    testState.prisma.$transaction = vi.fn(async () => {
      throw new Prisma.PrismaClientKnownRequestError("duplicate", { code: "P2002", clientVersion: "test" });
    });'''
    assert old in t
    t = t.replace(old, new, 1)
    if 'from "@prisma/client"' not in t:
        t = t.replace('import ', 'import { Prisma } from "@prisma/client";\nimport ', 1)
    add = '''
  it("does not map a look-alike error object to conflict", async () => {
    testState.reset();
    testState.prisma.course.findFirst = vi.fn(async () => ({ id: "course-1", organizationId: "org-1", status: "PUBLISHED", currentVersionId: "version-1" }));
    testState.prisma.courseVersion.findFirst = vi.fn(async () => testState.version);
    testState.prisma.$transaction = vi.fn(async () => { throw { code: "P2002" }; });
    await expect(dispatch("POST", "/courses/course-1/enroll")).rejects.not.toMatchObject({ status: 409 });
  });

  it("surfaces a transaction that fails after its writes, and the client is told nothing succeeded", async () => {
    testState.reset();
    testState.prisma.course.findFirst = vi.fn(async () => ({ id: "course-1", organizationId: "org-1", status: "PUBLISHED", currentVersionId: "version-1" }));
    testState.prisma.courseVersion.findFirst = vi.fn(async () => testState.version);
    testState.prisma.enrollment.create = vi.fn(async () => { testState.calls.enrollmentCreate++; return { ...testState.enrollment }; });
    testState.prisma.lesson.findMany = vi.fn(async () => [{ id: "lesson-1" }]);
    testState.prisma.lessonProgress.createMany = vi.fn(async () => { testState.calls.progressCreate++; });
    // The callback runs (writes are issued on the transaction client) and then the commit fails.
    testState.prisma.$transaction = vi.fn(async (callback: any) => { await callback(testState.tx); throw new Error("commit failed"); });
    await expect(dispatch("POST", "/courses/course-1/enroll")).rejects.toThrow("commit failed");
    // A mock cannot roll anything back; what this proves is only that the route does not answer 201.
    // The integration test in 04-TESTING-AND-DEBUGGING.md is what proves the rows are absent.
  });
'''
    # append inside the last describe block: insert before the final "});"
    idx = t.rstrip().rfind('});')
    return t[:idx] + add.rstrip('\n') + '\n' + t[idx:]
fe.rw('apps/api/src/routes/learner.routes.test.ts', test_fix)
done.append('review#4 the duplicate-enrollment catch checks `error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2002"`; the existing test throws a real PrismaClientKnownRequestError and a new test proves a look-alike object is not mapped to 409')
done.append('review#2 new test: a $transaction that fails after its writes rejects the request; 04 explains why only an integration test proves the rollback')
fe.append_section(S, '03', '## Why the error check is narrow', """`catch (error) { if ((error as { code?: string }).code === "P2002") ... }` accepted any object with a `code` property, which is duck typing across a trust boundary: a bug that throws `{ code: "P2002" }` from an unrelated helper would be reported to the user as "already enrolled". The route now checks `error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2002"`, and the test constructs a real `PrismaClientKnownRequestError`. The principle: when you map an error to a status code, match the error's *type* and its code, not the shape of a property.""", before='## ')
fe.append_section(S, '04', '## What the mocked transaction proves, and what it cannot', """The route suite drives Express with a fake `prisma` whose `$transaction` simply runs the callback with a `Proxy` over the same object. That proves the route *uses* the transaction client for every write (the assertions count calls on `testState.tx`) and, with the new failing-commit test, that a failed transaction is not reported as success. It cannot prove that PostgreSQL discarded the enrollment, the lesson progress and the domain event together; a fake has nothing to roll back.

To prove the rollback, write one integration test against a disposable database:

```ts
// apps/api/src/routes/enroll.integration.test.ts (runs only when TEST_DATABASE_URL is set)
const prisma = new PrismaClient({ datasources: { db: { url: process.env.TEST_DATABASE_URL } } });
await prisma.$executeRawUnsafe("CREATE OR REPLACE FUNCTION fail_event() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'injected'; END $$");
await prisma.$executeRawUnsafe("CREATE TRIGGER fail_event BEFORE INSERT ON \\"DomainEvent\\" FOR EACH ROW EXECUTE FUNCTION fail_event()");
await expect(dispatchAgainst(prisma, "POST", "/courses/course-1/enroll")).rejects.toBeTruthy();
expect(await prisma.enrollment.count()).toBe(0);
expect(await prisma.lessonProgress.count()).toBe(0);
```

Run it with `docker run --rm -d -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18`, `npx prisma migrate deploy` against that URL, then `TEST_DATABASE_URL=... npm test --workspace @lms/api`.""", before='## ')
done.append('review#2 04 section on the mocked transaction and an integration-test recipe')

# --- review #5: outbox
fe.append_section(S, '02', '## What the OutboxMessage row is for', """`recordDomainEvent` (`apps/api/src/events.ts`) writes a `DomainEvent` and an `OutboxMessage` on the transaction client, so the message exists exactly when the enrollment exists. Nothing in `apps/api` sends it: that is a worker's job, and `apps/worker` has no tests and is not covered by this course. What the worker must do, in order: `SELECT ... FOR UPDATE SKIP LOCKED` a batch of unsent rows and stamp a lease; publish each one; mark it sent; on crash, the lease expires and another worker retries. Delivery is therefore *at least once*, and consumers must de-duplicate by message id. Predict what happens if the worker marks the row sent *before* publishing (a lost message) versus after (a duplicate on crash), and why the second is the right failure to choose.""")
done.append('review#5 02 explains the outbox row and the worker contract (lease, retry, at-least-once, consumer dedupe)')

# --- review #3: codebase map expansion + README pacing/glossary
fe.append_section(S, '01', '## The four workspaces, and what to ignore for now', """| workspace | owns | files this course touches |
|---|---|---|
| `packages/domain` | pure rules: `isCourseComplete`, requirement lists, status transitions | `src/completion.ts` and its tests |
| `apps/api` | Express routes, Prisma, transactions, events | `src/routes/learner.routes.ts`, `src/events.ts`, `src/routes/learner.routes.test.ts` |
| `apps/web` | the Next.js UI | none: ignore for now |
| `apps/worker` | outbox delivery (no tests) | none: read chapter 2's outbox section only |

Terms used before they are defined elsewhere: **IDOR** (insecure direct object reference: a request names an id it should not be allowed to touch; the three-scope guard organization/user/version is the defense); **transaction client** (`tx` inside `prisma.$transaction(async (tx) => ...)`: every write that must commit together goes through it, not through `prisma`); **outbox** (a row written in the same transaction as the change, delivered later by a worker); **P2002** (Prisma's unique-constraint violation code, mapped to 409 in the enroll route).""", before='## ')
fe.append_section(S, 'README', '## Pacing', """map 45 min, concepts 75 min, worked change 90 min, testing 60 min, practice 4-6 h (the implement-it exercises), solutions 45 min, trace lab 45 min. Do the practice exercises in order; each names its acceptance test.""", before='## ')
done.append('review#3 01 workspace table, ignore list and definitions; README pacing')

# --- review #1: implement-it exercises
fe.append_section(S, '05', '## Implement-it exercises', """**Exercise 9 - Guard a route Astra did not cover.** Pick one learner route without the three-scope guard (organization, user, enrolled version). Add it and write the tests: a request naming another organization's enrollment is 404; a request naming another user's enrollment is 404; a quiz from the wrong version is 403 with the enrollment unchanged. Acceptance: the three tests pass and the existing suite is unchanged.

**Exercise 10 - Withdraw transactionally.** Add `POST /enrollments/:id/withdraw` that sets `status: "WITHDRAWN"`, deletes pending lesson progress, and records exactly one `enrollment.withdrawn` domain event and outbox row on the transaction client. Acceptance: a mock test counts one transaction and one event; a repeated withdraw is a 409 with no second event.

**Exercise 11 - Red first.** Write a failing test for the rule "a course with an empty `requiredLessonIds` and no assessments cannot be completed by an empty progress record" in `packages/domain`, then make it pass without breaking the existing completion tests. Acceptance: the test was red before the change (paste the failing output into your notes).""", before='## ')
fe.append_section(S, '06', '## Implement-it exercise answers', """**9.** The guard is one `findFirst` with `where: { id, organizationId, userId }` before any write; a quiz check compares `quiz.courseVersionId` with `enrollment.courseVersionId`. 404 for the first two (do not reveal existence), 403 for the version mismatch (the enrollment exists and is yours, but the content is not part of it).

**10.** Inside `prisma.$transaction`: `enrollment.update` with a `WHERE status <> "WITHDRAWN"` guard (Prisma: `updateMany` and check `count`), `lessonProgress.deleteMany({ where: { enrollmentId, status: "NOT_STARTED" } })`, then `recordDomainEvent(..., tx)`. A `count` of 0 means already withdrawn: throw `HttpError(409)` inside the callback so nothing else runs.

**11.** The failing assertion is `expect(isCourseComplete(rule, emptyProgress)).toBe(false)`; the fix distinguishes "no requirements" (nothing to complete, so not complete) from "all requirements met". Keep the existing tests green: they cover the populated cases.""", before='## ')
done.append('review#1 three implement-it exercises with acceptance contracts (05) and answers (06)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
