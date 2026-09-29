# JS1/kanban-flow — Fable review

- **Path:** `JS1/kanban-flow`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + DOM drag-and-drop + localStorage  ·  **Batch:** B03
- **Astra's change (one line):** `moveCard` was rewritten from an in-place mutator into a validating, immutable, boolean-returning operation: it rejects unknown columns and `beforeId`s that are not in the target column, treats a self-drop as a no-op, builds a fully renumbered copy of every column, persists that copy, and only then publishes it; plus a keyboard path (per-card column `<select>` and Move up/down buttons) that reuses the same function.
- **Course size:** 5,722 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 in `test/movement.test.cjs` (+ `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 3 | 4 | 5 | 4 | 3 | 4.0 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- The before/after contrast is exactly the kind a junior needs. The old `moveCard` mutated `dragged.column` *before* validating anything and renumbered only the destination column (`backups/22/app.js:87-105`), so the source column kept stale order values. The new one copies (`state.cards.map(card => ({ ...card }))`, `app.js:91`) and renumbers **every** column in the `for (const column of COLUMNS)` loop (`app.js:94-99`).
- Persistence is a commit boundary: `try { localStorage.setItem(...) } catch { showMessage(...); return false; }` then `state.cards = candidate` (`app.js:100-102`). A rejected write leaves the board object untouched, and the test proves it by string-comparing the array.
- Ordering is made deterministic: the sort comparator falls back to id (`a.order - b.order || a.id.localeCompare(b.id)`, `app.js:95`), which is the right lesson about ties.
- The accessibility work is functional, not decorative — `moveByKeyboard` computes the insertion target, calls the same `moveCard`, and restores focus to the re-rendered element (`app.js:105-110`); test 3 asserts `document.activeElement.className === 'move-column'` after a `change` event.

## Problems found (evidence required)
- **[D8]** Template scaffolding. `astraupskill/04-TESTING-AND-DEBUGGING.md` and `05-PRACTICE.md` differ from the poll-studio / pulse-analytics versions only in the fixture sentence and a few nouns; `06-SOLUTIONS-AND-REVIEW.md` repeats the identical "Review:" paragraph under every exercise.
- **[D8/D1]** `astraupskill/README.md` Prerequisites still says "For API projects, review JSON, HTTP methods and promises, then learn the relevant SQL operations as you trace the request" — there is no API and no SQL in this project. `VERIFICATION.md` "Limits" mentions "status-command semantics… and transaction scope", neither of which exists here.
- **[D2]** No CSS was added for the new per-card `<select class="move-column">` (`styles.css` is untouched — it is not in `delivery-manifest.json` for stage 22), so the keyboard control renders unstyled inside `.card-actions`.
- **[D2]** `moveCard` now calls `showMessage("Card moved.")` on every successful drop (`app.js:102`), including drops that change nothing visually; the old code was silent. Minor UX regression not mentioned anywhere in the course.
- **[D2]** Whole-file CRLF rewrite of `app.js`, so an unqualified `diff -r` against the backup shows every line changed.
- **[D4]** No React, Node, HTTP or SQL. The invariant/ordering lesson transfers, but nothing here is practised on the target stacks.

## Spot-checks performed
- "The excerpt below comes from app.js near line 86" (`03-WORKED-CHANGE.md`) -> `sed -n '86p' app.js` = `function moveCard(columnId, beforeId, cardId = state.draggingId) {` -> matches.
- "Move A from todo [A,B] before C in doing. B becomes order 0; A/C become orders 0/1" (report + course fixture) -> `test/movement.test.cjs:5-10` sets exactly that fixture and asserts `b.order === 0`, `c.order === 1`, and the persisted `a.order === 0` in `doing` -> matches.
- "A self-drop does nothing" -> `app.js:88` `if (beforeId === cardId) return true;` and `test/movement.test.cjs:13` asserts state is unchanged -> matches.
- VERIFICATION claims 3 cases + passing Chromium -> `logs/22-tests.log` `# tests 3 / # pass 3 / # fail 0`; `browser-checks.json` `{"project":"22","passed":true}` with `logs/22-browser.png` present -> matches.
- I hand-traced `moveByKeyboard` for `[A,B,C]` moving A down: `before = ordered[index+2] = C`; inside `moveCard` the candidate list without A is `[B,C]`, `findIndex(C) = 1`, insert at 1 -> `[B,A,C]`. Correct, and the `index === ordered.length - 1` guard prevents the out-of-range case.

## Improvements needed (ordered, concrete, actionable)
1. Add styling for `.move-column` in `styles.css` (width, margin, font-size consistent with `.link-button`) — the delivered keyboard control is currently unstyled. (effort: S)
2. Strip the API/SQL/transaction boilerplate from `astraupskill/README.md` Prerequisites and `VERIFICATION.md` Limits; state the real limits instead (single-tab only; no cross-tab `storage` event handling; `prompt()`-based rename). (effort: S)
3. Rewrite `05-PRACTICE.md` Exercise 1-4 bodies with board-specific acceptance criteria (e.g. "after any move, assert that for every column the set of `order` values equals `0..n-1`") instead of the shared paragraph. (effort: M)
4. Suppress or reword the "Card moved." message for no-op drops, and add a sentence in `02-CONCEPTS.md` about feedback for operations that changed nothing. (effort: S)
5. Add a fourth test covering a cross-tab conflict (two `state.cards` snapshots committing over each other) — the course discusses stale state but nothing exercises it. (effort: M)

## One-paragraph summary for the index
A tight lesson on ordering invariants: the board's `order` fields must always be a dense `0..n-1` per column, and the rewritten `moveCard` earns that by validating first, renumbering a copy of every column, saving, and only then publishing. The three jsdom tests are real — they check renumbering of both source and destination, reject invalid targets and self-drops, and force a `setItem` failure to prove the board is untouched. The keyboard controls are a genuine bonus for accessibility, though nobody styled the new dropdown. As with the rest of this batch, the practice and solutions chapters are shared boilerplate, and the project is plain DOM rather than React/Node — do it as an elective for the invariant habit, not as a stack lesson.
