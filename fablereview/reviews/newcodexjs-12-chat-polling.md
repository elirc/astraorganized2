# newcodexJS/12-chat-polling — Fable review

- **Path:** `newcodexJS/12-chat-polling`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + zod + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** Added a single router-level guard (`chatRouter.use(...)` in `server/src/routes/chatRoutes.ts:12-70`) that resolves `/conversations/:id` or `/messages/:id` to a conversation, requires a `conversation_members` row for the demo user, requires `role === "admin"` for group metadata and member routes, and requires a read receipt's `messageId` to belong to that conversation; group creation now de-duplicates `memberIds`.
- **Course size:** 7,991 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/membership.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 5 | 4 | 5 | 4 | 4 | 4.3 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- This is the batch's best authorization lesson, and it is the right shape: one guard mounted once, rather than a membership check copy-pasted into 19 handlers. The backup `chatRoutes.ts` was 19 bare `chatRouter.<verb>(...)` lines with no ownership check at all.
- The guard correctly distinguishes *existence* from *visibility*: an outsider gets 404, not 403, for every conversation route, so the API does not leak that a room exists. The first test drives five different routes as user 3 and asserts 404 on all of them plus `reactions` count 0 (`test/membership.test.ts`, "outsiders cannot read history, poll, react, type, or change membership").
- Role scoping is per-conversation, not global: `member.role !== "admin"` reads the *membership row* for that conversation. `02-CONCEPTS.md` states the idea explicitly — "being an admin in another group grants nothing here" — and the second test proves it (member user 2 can react, gets 400 on adding a member).
- The limits section is honest about the residual TOCTOU: "This central check is a useful boundary, but it is not a transaction spanning every subsequent read; strict coordination with simultaneous membership removal would need additional policy and locking" (`02-CONCEPTS.md`).
- All 81 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts` sources (81/81).

## Problems found (evidence required)
- **[D2]** The guard reads `req.body.messageId` before validation runs. `chatRoutes.ts` does `db("messages").where({ id: req.body.messageId, conversation_id: conversationId })` inside `chatRouter.use`, which is registered *before* `validateBody(readSchema)` on the route. `POST /api/conversations/:id/read` with an empty body therefore hands Knex an undefined binding; Knex throws a non-`AppError`, and `errorMiddleware` in `server/src/middleware/errors.ts:29-43` converts anything that is not an `AppError` into `new AppError("Unexpected server error")` — a 500 where `readSchema` (`z.object({ messageId: z.number().int().positive() })`) should have produced a 400. No test covers the empty-body case.
- **[D2, minor]** The guard's admin test is path-string based: `req.method === "PUT" && /^\/conversations\/\d+$/.test(req.path)` plus `req.path.includes("/members")`. A future route containing the substring "/members" anywhere (e.g. `/conversations/1/members-count`) silently becomes admin-only. The course presents the regex without flagging its brittleness.
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six differently-labelled boundaries and then repeats one byte-identical paragraph six times, each pointing at "starting with [server/src/routes/chatRoutes.ts](../server/src/routes/chatRoutes.ts) and `chatRouter.use`". The boundary labelled "A React form, button or test sends a concrete operation" therefore sends the learner to the server guard.
- **[D8]** Chapters 04, 05 and 07 are near-duplicates of the sibling courses: `04-TESTING-AND-DEBUGGING.md` is 93.5% character-identical to `newcodexJS/11-survey-builder`'s, `05-PRACTICE.md` 85.1%, `07-TRACE-LAB.md` 81.3%. Whole paragraphs such as "The expectation should not be copied from the function being tested…" appear unchanged across the batch.
- **[D5]** Root `package.json` devDependencies are `{"concurrently": "^9.1.2"}` only, while `test/database.ts` imports `pg`; the course asserts three separate times that "The root workspace also makes pg and tsx available to the root test directory", which is true only through npm hoisting from `server/`, not through any declaration.

## Spot-checks performed
- Claim (`VERIFICATION.md`): "A receipt pointing to another room is rejected" -> read the guard's `req.path.endsWith("/read")` branch and the second test asserting 400 for `{ messageId: foreign }` and 200 for `{ messageId: message }` -> matches.
- Claim: "Group creation deduplicates members" -> the third test posts `memberIds: [1, 2, 2]` and asserts 201; `03-WORKED-CHANGE.md` excerpt of the dedupe is present in `chatController.ts`/`chatService.ts` -> matches.
- Claim: "a deleted message cannot be revived by editing" -> guard resolves messages with `.where({ is_deleted: false })` and throws `NotFoundError`; the third test asserts PUT after DELETE returns 404 -> matches.
- Claim: "Automated test cases: 3" -> `batch04/logs/63-tests.log` shows `# tests 3 / # pass 3 / # fail 0`; `grep -c '^test('` returns 3 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"63","passed":true,"api":"actual isolated HTTP server","api_requests":7}` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Fix the 500-instead-of-400 path in `server/src/routes/chatRoutes.ts`: guard the read-receipt branch with `if (!Number.isSafeInteger(Number(req.body?.messageId)))` and throw `ValidationError`, or move `validateBody(readSchema)` ahead of the membership `use`. Add a test asserting `POST /conversations/:id/read` with `{}` returns 400. (effort: S)
2. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" so each names its own file: 1 the room component in `client/src/`, 2 the client fetch layer, 3 `chatRouter.use` (the guard), 4 `chatService`/`chatModel`, 5 Knex/Postgres, 6 `server/src/utils/http.ts`. (effort: S)
3. Add a paragraph to `02-CONCEPTS.md` on why the guard uses path-regex dispatch rather than per-route middleware, what that costs (silent over-matching of any future path containing "/members"), and what a `requireMember()` / `requireAdmin()` per-route alternative would look like. (effort: S)
4. Add one exercise in `05-PRACTICE.md` that makes the TOCTOU concrete: remove a membership row between the guard and the handler (a test hook or an injected delay) and observe that the read still succeeds. The limitation is stated in prose but never demonstrated. (effort: M)
5. Replace the shared paragraphs in `04-TESTING-AND-DEBUGGING.md` and `05-PRACTICE.md` with chat-specific material (cursor-based polling, unread counts, `last_read_message_id` arithmetic). (effort: M)

## One-paragraph summary for the index
A polling-based chat API where every history read, poll, reaction, typing ping and membership edit previously trusted the caller. The lesson is authorization as a single boundary: one router-level guard that resolves a message to its conversation, checks the `(conversation_id, user_id)` membership pair, scopes the admin role to *that* conversation, and returns 404 rather than 403 so the API does not leak existence. The three tests are real HTTP tests against a disposable Postgres schema and drive five routes as an outsider, a plain member and an admin. Do this one after the survey-builder course; it is the clearest "foreign key is not permission" lesson in the set. Note one real bug the course does not mention: an empty read-receipt body returns 500 instead of 400.
