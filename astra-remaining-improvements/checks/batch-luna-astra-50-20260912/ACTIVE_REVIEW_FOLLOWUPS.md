# Active Astra review followups after delivery 23

These findings were sent to the assigned Luna workers. They are not completion claims. Root must inspect final diffs and test results after source freeze.

## Master6 — luna_course_finish

- Preserve legacy requireAllLessons semantics when requiredLessonIds is absent; current fallback to [] incorrectly makes missing/incomplete progress pass.
- Explicit required IDs must have defined semantics even if boolean flags are false. Validate stored rule field types, finite 0–100 quiz score, unique nonempty IDs and enrolled-version membership instead of silently filtering malformed arrays into empty requirements.
- Separate missing lesson/quiz/assignment cases; combined missing assessment fixture hides independent defects.
- Test completion ownership and missing organization, positive progress timestamps/quiz/submission and duplicate enrollment409. Scope-aware mocks must inspect IDs and actor/org.
- Actual event/audit helper client use needs evidence: distinct transaction client and real helpers or focused helper tests. Replacing both helpers and reusing prisma as tx does not establish outbox grouping.
- Restore generated baseline tsbuildinfo. Final typecheck/workspace tests/build after source changes; nine accurate guides.

## Ramp — luna_ramp

- Remove DataStore's false claim that swapping the database is the only persistence change and services do not use dictionaries.
- Update should evaluate a validated candidate's policy before assigning live fields or touching timestamps.
- Delete must coordinate with command gate. A command must not mutate a detached object if deletion wins; retrieve or recheck under the same lock.
- RefreshPolicy and receipt/read mutation races remain explicit limits if out of scope.
- Add positive Create/Update normalization, invalid amount/enum/blank/date matrix, actual capacity-one queue rejection, throwing queue and repeated reimbursement command no-enqueue coverage.
- TimeSpan.Zero Task.WhenAll invokes duplicate worker calls without proving overlapping execution; avoid concurrent proof claims.
- Await tests (fix xUnit1031); exclude nested test Content from Web SDK glob to avoid recursive output copies. No repeated clean needed. Final tests/build and source freeze then guides.

## appmakertrack — luna_checkout_finish

- Next route modules must not export arbitrary injectable factory functions. Put factories in lib helpers and export only supported HTTP/config names from route.ts.
- Align parseSeconds test error assertions, add positive manual/start cases, omitted-note stop assertion and derived duration overflow.
- Board same-column final loop should not first rewrite sourceRemaining. Ticket has no position uniqueness constraint; temporary-position collision commentary must reflect actual schema or be simplified. Future unique constraints would expose same-column double-write collisions.
- Root review-followup file b7429e8bf71d-review-followup.md remains the primary implementation checklist.

## Setup and reports

- e13 npm ci root-install-01 passed (40 minutes). Client generation root-generate-01 session49104 uses a dummy SQLite URL and does not initialize a database. Installed Next documentation is available; AGENTS requires reading it before source edits.
- z1 install root-install-01 session74993 remains active; z6 install root-install-01 session7157 was started after e13 completed. appmaker install root-install-02 session60463 belongs to assigned Luna to poll.
- All reports reflect23/50 and65/239. Latest audit65 projects3079files:64 match, only JSProjectLearn's known nine later user edits differ; no missing files.
