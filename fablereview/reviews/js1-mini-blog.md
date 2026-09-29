# JS1/mini-blog — Fable review

- **Path:** `JS1/mini-blog`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory repository, posts -> comments) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** One-line type gates were added to the front of `validatePost` and `validateComment` so non-string payloads (`title: {}`, `author: 4`, `text: {}`) are rejected before the existing length checks, plus a JSON-object body guard and a testable `export const app`; the substantive parent-scoped-delete and cascade behaviour was **not changed** — it was given regression coverage. The React client, which never mounted, was repaired with a new `client/src/main.jsx`.
- **Course size:** 5,677 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 3 | 3 | 5 | 4 | 4 | 4 | 2 | 3.6 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- **Honest scoping.** The report says plainly "Tests verify existing parent-scoped deletion and cascade behavior" rather than dressing characterization tests up as new features. That is the right instinct and is rarer than it should be.
- The parent-scoping test is genuinely the most valuable test in the batch. `test/api.test.js:8` creates a comment under post A and then attempts `DELETE /api/posts/{B}/comments/{commentId}`, asserting **404** — that is the IDOR-shaped bug ("route nesting is not authorization unless you check it") that real CRUD apps ship. It then asserts the comment still exists under A, and that deleting A makes `/api/posts/{A}/comments` 404 rather than returning orphans.
- The type gate is placed correctly, before the `.trim()` calls that would throw on a non-string: `if (!isText(title,3) || !isText(author,2) || !isText(body,1,20000))` at `server/server.js:78`, ahead of `title.trim()`.
- Test 2 checks non-creation, not just the status code: after three rejected comment payloads it asserts `(await call('/api/posts/{id}/comments')).data.length === 0`.
- Real client repair: `backups/29/client/index.html` loaded `/src/App.jsx`, which has no `createRoot`; `client/src/main.jsx` is new and `index.html` now points at it.

## Problems found (evidence required)
- **[D2] The code change is thin.** Excluding the client mount fix and the test harness plumbing, the whole change is three inserted lines (`server/server.js:21-25` body guard, line 78, line 96). The relationship/cascade behaviour the course is *about* was already in `backups/29/server/server.js`. Compared to its batch siblings (course-roster's 409 uniqueness, stock-catalog's pagination validation, org-explorer's transaction), this one delivers characterization coverage rather than an improvement.
- **[D2]** Dead code: both `whole` (`server/server.js:200`) and `realDate` (line 201) are defined and never called in this file — two of the three copy-pasted helpers are unused here. Only `isText` is used.
- **[D2]** The legacy guards are now unreachable: `if (!title || title.trim().length < 3)` (`server/server.js:79`) cannot fire after line 78, and the same holds for author/body and for both comment checks. The excerpt printed in `03-WORKED-CHANGE.md` shows this duplication verbatim without comment — a learner reading the chapter is shown dead code as the worked example.
- **[D8]** Template. `05-PRACTICE.md`, `06-SOLUTIONS-AND-REVIEW.md` and `04-TESTING-AND-DEBUGGING.md` are the shared batch scaffolding; the "Review:" paragraph repeats verbatim under each exercise.
- **[D8/D1]** `README.md` Prerequisites is the shared paragraph telling the learner to "learn the relevant SQL operations as you trace the request" — there is no SQL here, the repository is an in-memory `Map`/array. `VERIFICATION.md` Limits mentions "transaction scope"; there are no transactions.
- **[D6]** `logs/29-browser-failure.png` exists next to `logs/29-browser.png`, but `browser-checks.json` records only `{"project":"29","passed":true}` with no mention of the failure or what changed between the two. The clean "integrated browser checks passed" claim is not fully supported by its own evidence folder.
- **[D2]** `htmlFor="lesson-field-1..3"` ids in `client/src/App.jsx`. **[D5]** all deps `"latest"`, no lockfile.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 94" -> `sed -n '94p'` = `function validateComment(req, res, next) {`; the pasted excerpt matches the file verbatim (including the now-dead legacy branches) -> matches.
- "A comment under A cannot be deleted through B" -> `test/api.test.js:8` asserts 404 on the cross-parent delete and line 9 asserts the comment count under A is still 1 -> matches.
- "Deleting A removes access to its comments" -> `test/api.test.js:10-11` asserts 204 on the post delete then 404 on the comment list -> matches.
- "Object-valued text returns 400 and creates no comment" -> `test/api.test.js:14-16` loops `{author:4,...}`, `{text:{}}`, `{text:'x'.repeat(2001)}` and then asserts zero comments exist -> matches.
- Report claim "18 files; nine course files; 2 passing regression cases" -> `delivery-manifest.json` lists 18 entries for stage 29, of which 9 are `astraupskill/*`; `logs/29-tests.log` shows `# tests 2 / # pass 2 / # fail 0` -> matches.
- I checked whether the change actually prevents anything new: `title: {}` under the old code would reach `title.trim()` and throw a `TypeError` -> an unhandled 500 rather than a 400. So the gate does convert a crash into a clean rejection. Real, if small.

## Improvements needed (ordered, concrete, actionable)
1. **Give this project a real change to teach.** The obvious one is missing and the course even hints at it: comment creation does not verify the parent post exists *atomically* with the insert, and `DELETE /api/posts/:id` cascades by iterating. Add a `POST /api/posts/:id/comments` guard returning 404 for an unknown parent, and a test that a comment cannot be attached to a post deleted between the two calls. That turns a characterization exercise into a lesson. (effort: M)
2. Delete the unused `whole` and `realDate` helpers at `server/server.js:200-201`, and collapse the unreachable legacy branches in `validatePost`/`validateComment` — then re-generate the `03-WORKED-CHANGE.md` excerpt, which currently prints dead code as the worked example. (effort: S)
3. Reconcile `logs/29-browser-failure.png` with `VERIFICATION.md`: either describe what failed and was fixed, or remove the stale artifact. (effort: S)
4. Replace the SQL sentence in `README.md` Prerequisites with what this project actually needs: nested Express routes, `req.params` on two levels, and array-backed repositories. (effort: S)
5. Rewrite `05-PRACTICE.md` Exercises 1-4 with blog-specific criteria — e.g. "add comment editing scoped to its parent and prove with a test that a valid comment id under the wrong post id returns 404, not 200". (effort: M)
6. Rename `lesson-field-N` ids; add a lockfile. (effort: S)

## One-paragraph summary for the index
The domain is the right one — a parent/child relationship where a comment belongs to exactly one post — and the headline test is the most valuable single assertion in this batch: a comment created under post A returns 404 when you try to delete it through post B. That is the nested-route authorization mistake real applications ship. Be aware, though, that the course is mostly *documenting* behaviour that already existed; the actual code change is three inserted lines of type checking plus a repair to a React client that never mounted, and the server was left with two unused helper functions and a set of unreachable legacy guards that the worked-change chapter prints as its example. Read it for the relationship and scoping lesson; do not expect to learn much from the diff.
