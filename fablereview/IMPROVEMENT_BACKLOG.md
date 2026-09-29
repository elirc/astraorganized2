# Improvement backlog

Ordered by leverage. Each item says what to change and where. Effort: S = under an hour, M = a session, L = a day or more.
Per-project detail and exact file:line references are in `reviews/<slug>.md` ("Improvements needed" section).

## P0 — act now

| # | Item | Where | Effort |
|---|---|---|---|
| 0.1 | Revoke the Shopify admin token and delete the backup file that still contains it. | `AstraOrganized2/astra-remaining-improvements/backups/cf8875344b43/scripts/populate-metaobjects.js` | S |
| 0.2 | Stop Vitest collecting the archived pre-change test that reseeds the developer database. Add `exclude: ["astraupskill/**"]` to `vitest.config.ts` or rename the file to `.txt`. | `_Organized Desktop/05 Numbered Experiments/e13` | S |
| 0.3 | Restore `.int()` on `forecastAmount` (now accepts decimals against a Prisma `Int` column) and remove the duplicate unused `createPlaybookRunSchema`. | ww17 | S |

## P1 — accuracy defects (course says something the code does not do)

| # | Item | Where | Effort |
|---|---|---|---|
| 1.1 | Replace the fixture "10, 0 and 20 → averages 10, 5 and 10; totals 10, 10, 30" with the test's "10, 0 and 30 → 10, 5, 13.33; 10, 10, 40" in all seven chapter files. | JS1/pulse-analytics/astraupskill | S |
| 1.2 | Rewrite "Tested behavior" to match the test (three threads, page 2, total 3, no delete), in VERIFICATION and the six chapters that repeat it. | JS1/forum-search | S |
| 1.3 | Remove or implement "a fractional cent is rejected rather than silently rounded" (no cent check exists). | JS1/legal-case-tracker, subscription-billing, field-service, research-studies | S each |
| 1.4 | Align the domain-flavoured fixture titles ("Camera kit for field interviews", etc.) with the generic fixture the tests actually use, or change the tests. | JS1 35-40 | S each |
| 1.5 | Replace the invented `publishVersion` excerpt (`retireActiveVersions`, `updateVersion(id, patch)` do not exist) with the real function body. | w24/astraupskill/03-WORKED-CHANGE.md | S |
| 1.6 | Fix the C# claim that `checked` addition detects `decimal` overflow (decimal always throws; `checked` affects integer types only). Add a real midpoint test for `AwayFromZero`. | .netvg/astraupskill/03-WORKED-CHANGE.md:12 | S |
| 1.7 | Chapter files hold the next chapter's content; re-file so each filename, H1 and body agree. | z9/astraupskill, zz8/astraupskill | S |
| 1.8 | State correctly that order lookup, permission, state guard and allocation run inside `$transaction` (03 says "before entering"). | e13/astraupskill/03-WORKED-CHANGE.md | S |
| 1.9 | The printed model solution `roleCapabilities[user.role]?.includes(cap) ?? false` contradicts the shipped `hasOwnProperty` code and throws on the course's own `__proto__` tests. | ww39/astraupskill/06 and 04 | S |
| 1.10 | "Explicitly sending an empty role clears it" is false (`role: z.string().trim().min(1)` returns 400). | newcodexJS/09/astraupskill/02-CONCEPTS.md:7 | S |
| 1.11 | README claims `taskController.ts` was repaired; it is byte-identical to its snapshot. | grokbuildppmproject/astraupskill/README.md | S |
| 1.12 | Broken link Astra added: `docs/code-walkthroughs/audit-log-scope/README.md` does not exist. | master7/README.md item 13 | S |
| 1.13 | Disclose the silently repaired compile error (Python syntax `throw ... from ex;` in the baseline) instead of describing it as a contract fix. | .netgum/astraupskill/03-WORKED-CHANGE.md | S |
| 1.14 | VERIFICATION cites superseded `ww27-test-08` and says 10 tests; the final log says 12. | ww27/astraupskill/VERIFICATION.md | S |
| 1.15 | Separate inherited from delivered test counts: jobtrack (90 vs 4 added), calendar+jobtrack (92 vs 2), devdeck (62 vs 2), newcodexJS/04 (1 block vs ~16 assertions). | those VERIFICATION.md files | S |

## P2 — wave-1 generator sweeps (one change lands in up to 75 courses)

These should be done by editing the generator in `AstraOrganized2/astrafinalplan/implementation/*/write_learning.py` / `enrich_learning.py`
(or by one scripted pass over `JS1/*/astraupskill` and `newcodexJS/*/astraupskill`), not project by project.

| # | Item | Effort |
|---|---|---|
| 2.1 | Make environment/limits paragraphs per-stack. Remove "PostgreSQL 18.1" from browser-only projects, the jsdom/`app.js` paragraph from API projects, and the leaked "For Poll Studio and Kanban Flow..." / "Questboard, DevDeck and Live Chat" sentences from every course they do not belong to. | M |
| 2.2 | `07-TRACE-LAB.md`: generate six distinct boundary paragraphs (client form → serializer → HTTP → validator → repository/transaction → response) each pointing at the right file, instead of one paragraph six times. | M |
| 2.3 | `06-SOLUTIONS-AND-REVIEW.md`: one review paragraph per exercise instead of the same "Review: Demonstrate an ordinary case..." under all four. | M |
| 2.4 | `03-WORKED-CHANGE.md`: supply the "three variations" it promises, and make the "Actual implementation excerpt" contain changed lines (stock-catalog, mini-blog, project-risks, procurement-portal, property-rentals, patient-intake currently excerpt unchanged code). | M |
| 2.5 | Add an **ownership/authorization** exercise to every server project (all routes are unauthenticated; no course closes the gap). This is the largest curriculum hole for the stated goal. | L |
| 2.6 | De-minify delivered test files (`test/*.test.ts` with 5-10 statements per line) so "read each test as arrange → act → assert" is possible. | M (scripted Prettier pass) |
| 2.7 | Reproducibility: pin Node/Postgres in README (not only VERIFICATION); add `CREATE DATABASE` + `CREATE EXTENSION pgcrypto` to TS Postgres setups; replace `"latest"` deps with pinned versions and commit lockfiles; note that `test/*.test.ts` globs do not expand under cmd.exe; offer a Docker Postgres fallback. | M |
| 2.8 | Hygiene: strip the BOM left at line 2 of the five in-memory servers (`import { pathToFileURL }` prepended above U+FEFF); delete dead injected helpers (`realDate`, `whole`) and unreachable legacy guards; fix mojibake at `JS1/snippet-vault/src/store.js:1`; style the unstyled `.move-column` select in kanban-flow. | M |
| 2.9 | Tell learners to read diffs with `git diff -w` / `diff --strip-trailing-cr`, because whole-file CRLF and Prettier churn hide 4-line changes. Or re-deliver touched files with the repo's original line endings and quote style. | S / L |
| 2.10 | Collapse clone families in the index: keep one course per family (equipment-maintenance; learning-paths; project-risks; subscription-billing; newcodexJS 07; newcodexJS 16) and mark the rest as "same lesson, different nouns". | S |

## P3 — wave-2 packaging sweeps

| # | Item | Where | Effort |
|---|---|---|---|
| 3.1 | Add code blocks. Seven courses have none in any chapter: inline the transaction body, the validator and the regression test. | e13, ww17, ww27, ww39, z6, z9, globgame | M each |
| 3.2 | Remove agent-process language aimed at the delivery reviewer ("the root agent applies the frozen manifest", "compare hashes to baselines/<id>.json"). | ww39, ww5, z6, z9, and grep all wave-2 VERIFICATION.md for "manifest", "baseline", "stage" | S |
| 3.3 | Copy the cited evidence (logs, TRX, screenshots) into `astraupskill/evidence/` so a learner holding only the repo can verify a number. Best predictor of score in B12/B14. | grok* family, buildantigVG, z6, z9, buildbusinesses | S each |
| 3.4 | Add a red-first exercise: restore `astraupskill/snapshots/*` (or `docs/original`), run the focused test, record the failures, then restore the fix. Snapshots ship in most wave-2 projects and no exercise uses them. | all wave-2 projects with snapshots | S each |
| 3.5 | Add a glossary + prerequisites box + per-chapter time estimate (only meterforge has one). Junior-fit is the lowest wave-2 dimension. | all wave-2 | S each |
| 3.6 | Add `08-TRANSLATION.md` to off-stack projects: a table mapping each enforced invariant to its Express/Zod/Prisma and ASP.NET/EF Core equivalent (`RowVersion`, `[Timestamp]`, `ON CONFLICT`, conditional `updateMany`, If-Match → 412/428). | j1-j7, e14, e15, aiapplybot, buildsubbox, buildgum, JSProjectLearn, astra4.2, andie, buildsmallplates | M each |
| 3.7 | Convert bespoke console harnesses to xUnit + `WebApplicationFactory<Program>` so `dotnet test` proves the change and the learner writes a `[Fact]`. | netpastebin, nettrello, buildjira, nethris (Python checks), buildasana (child-process test) | M each |
| 3.8 | Bridge in-memory lessons to the database: one paragraph per course giving the `SaveChangesAsync` / `ON CONFLICT` / `RowVersion` equivalent of the `lock` / `ConcurrentDictionary` code just written. | meterforge, borrowbox, campusops, Ramp, master 6, master2/3 (mocked Prisma) | S each |
| 3.9 | Format monolith files a junior cannot read: `buildwhiteboard/client/src/App.tsx:194` (~900-char line), `buildsql/src/App.tsx` (1,098 lines), `astra4.2/src/app.js:202`, `react/test/store.test.js`, `J1/test/.../TaskWorkflowTest.java`, `andie/scripts/lib/*.js`. | listed | S each |
| 3.10 | Close the "new return value nobody consumes" pattern: wire the booleans/warnings into the UI, or make it exercise 1. | buildsmallplates, astra4.2, LLM_Generated_Helper | S each |
| 3.11 | Move inline solutions out of practice chapters into `06-SOLUTIONS-AND-REVIEW.md`; give real answers for exercises 5-7 instead of review heuristics. | jdtrrain2.1, b1, z1, ww5, most .NET and Prisma courses | M each |
| 3.12 | Remove or test the claimed Serializable isolation (no P2034 handling, retry test only proves a loop counts to two). | master2, master3 | M |
| 3.13 | Fix the tautological transaction test (fake's own catch restores state) and write the two real ones already specified in prose. | zz8, z6 | M |
| 3.14 | Disclose that `checks/.../final/` holds two failing frontend tests superseded by `verified/`. | grokbuildmultitenantproject | S |
| 3.15 | Windows-only commands everywhere: add macOS/Linux equivalents, `.nvmrc` / `engines`, and the missing `test` npm scripts (e6, jstrain3.0). | wave-2 READMEs | S each |

## P4 — latent bugs reviewers found that no course mentions

| Project | Bug |
|---|---|
| master4 | `res-${order.id}-${line.skuId}-${Date.now()}` reservation ids collide for two lines of the same SKU in one millisecond. |
| master2 | Webhook derives its tenant from caller-supplied demo headers; the tenant scoping the lesson rests on the untrusted party. |
| newcodexJS/12-chat-polling | `POST /conversations/:id/read` with an empty body returns 500, not 400 (guard reads `req.body.messageId` before validation). |
| newcodexJS/14 | `ensureNoConflict` only matches `status: "confirmed"`; the invariant silently depends on `appointmentService.ts:125`. |
| newcodexJS/05 | `isPublic: body.isPublic !== false` defaults an omitted field to public in an ownership course. |
| job track/live-chat | `mark_read` range query still runs outside the transaction (`server/src/socket.js:132-139`). |
| job track/KDS | existence check outside the transaction at `server/src/routes/api.js:192-197` (disclosed; make it the compare-and-set exercise). |
| JS1/task-board, finance-dashboard | create branch still uses unguarded `saveTasks()` / `saveState()` while delete/undo use persist-then-publish. |
| JS1/reading-list | id tie-break at `app.js:145` delivered untested; legacy numeric ids throw. |
| buildjira | `ApplyPatch` and `CopyMutableIssueFields` list 8 fields by hand with no compile-time tie; a 9th patchable field is silently dropped behind a 200. |
| netzen | `Ticket.Create` still accepts `(TicketPriority)99` while `UpdatePriority` rejects it. |
| j3 | mutates memory then saves with no rollback (inverts the pattern taught in j1/j2). |
| JSProjectLearn | tree drifted after delivery (files dated 2026-09-11 not in the manifest); VERIFICATION counts are stale. |
