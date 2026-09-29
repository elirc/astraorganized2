# JS1/focus-timer — Fable review

- **Path:** `JS1/focus-timer`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests)  ·  **Batch:** B01
- **Astra's change (one line):** Replaced per-tick decrement with deadline arithmetic (`remaining = max(0, (deadline - Date.now())/1000)`), made `startTimer` idempotent by clearing any prior interval, preserved sub-second remainder across pause/resume, and guarded `completeSession` with a `mode !== "running"` check so a late queued callback cannot log a second session.
- **Course size:** 5,049 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/timer.test.cjs`, plus harness `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 3 | 5 | 4 | 4 | 3 | 4.1 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- The tests are the strongest in the browser half of this batch. `test/timer.test.cjs` uses the harness's controllable clock (`app.advance(45000)`) to simulate a throttled tab, asserts the display reads `00:15` rather than `00:59`, and then proves idempotency twice over: `app.intervals.size === 1` after `startTimer(); startTimer()`, and exactly one logged session after `tick(); tick(); completeSession()`.
- The sub-second test is precise and would catch a real regression: pause at 1250 ms, assert `timer.remaining === 58.75`, advance 120 s of paused time, resume, advance 58,749 ms → still running, advance 1 more ms → idle. Rounding the stored remainder would fail this immediately.
- The reasoning paragraph in `03-WORKED-CHANGE.md` is genuinely instructive and honest about its limits: "Date.now is a wall clock and can jump if the system clock changes; this implementation fixes delayed-callback drift, not every possible clock-adjustment problem."
- `README.md` Scope states the invariant crisply — "The interval is a wake-up mechanism. The deadline determines remaining time." — which is the actual mental-model fix.

## Problems found (evidence required)
- **[D4]** This is the least CRUD-relevant lesson in B01. The target profile is validation, ownership/authz, transactions, idempotency, pagination and persistence; this project delivers timer arithmetic and event-loop scheduling. The transferable CRUD content is one idea — the idempotency guard at `app.js:117` (`if (timer.mode !== "running") return;`) preventing a duplicate write — which a junior can get more cheaply from the double-submit case in a real API. Session persistence itself is untouched: `saveSessions()` is still an unguarded `localStorage.setItem`.
- **[D2, minor]** `completeSession` sets `timer.mode = "idle"` twice (`app.js:118` and `app.js:132`) — dead code introduced by the change, in the exact function the course asks the learner to study for its guard.
- **[D8]** `05-PRACTICE.md` differs from `newcodexJS/05-recipe-manager/astraupskill/05-PRACTICE.md` in only 5 substituted lines out of 47; the surrounding instructions ("Close the worked-change chapter while implementing. Describe your design in three sentences…") are byte-identical across all ten courses. `06-SOLUTIONS-AND-REVIEW.md` repeats the same "Review: Demonstrate an ordinary case and a case that would break a naive implementation…" sentence verbatim under all four exercises.
- **[D3]** "Three variations to work through" in `03-WORKED-CHANGE.md` supplies no actual variations, only generic instructions to construct them.
- **[D6]** `VERIFICATION.md:20` asserts "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" in a project with no database. Boilerplate in an honesty document.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): excerpt of `tick()` "near line 106". -> `sed -n '106,113p' app.js` — `function tick()` is at line 106 and the body matches exactly, including `Math.max(0, (timer.deadline - Date.now()) / 1000)`. -> **matches.**
- Course claim (`VERIFICATION.md`): "If paused at 1.25 seconds, 58.75 seconds remain; a two-minute pause does not consume them." -> `pauseTimer` at `app.js:84-89` recomputes `remaining` from the deadline and nulls the deadline; `startTimer` at `app.js:76` rebuilds `deadline = Date.now() + timer.remaining * 1000`. Test 2 asserts `58.75` then survives `advance(120000)`. -> **matches.**
- Course claim (`README.md` Scope): "repeated starts do not stack intervals". -> `app.js:70-71` (`if (timer.mode === "running") return; clearInterval(timer.intervalId);`) and the test's `assert.equal(app.intervals.size, 1)`. -> **matches.**
- Course claim (`VERIFICATION.md`): "Real Chromium browser interaction | Passed". -> `implementation/browser-checks.json` project "03" passed; `implementation/browser_checks.cjs:54-59` injects a fake `Date.now`, drives a 1-minute session and asserts `#timer-display` reads `00:15` and `#session-count` reads `1`. -> **matches.**
- Delivery claim: 3 test cases, 5,049 words. -> 3 `test(` blocks; `wc -w` totals 5,049. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Remove the duplicated `timer.mode = "idle"` at `app.js:132` (line 118 already set it) so the guard the course teaches is not surrounded by dead code. Effort: S.
2. Re-frame the course for CRUD transfer: add a chapter-2 subsection "the same guard in an HTTP handler" that maps `if (timer.mode !== "running") return;` onto a double-submitted POST and an idempotency key, and cross-link `newcodexJS/02-contact-book` (transactional import) as the server-side counterpart. Without this the lesson stays off the target stacks. Effort: M.
3. Apply and test write-failure handling for `saveSessions()` so the persistence half of the lesson matches what `02-CONCEPTS.md` claims about failure boundaries. Effort: S.
4. Replace the generic "Three variations" block with concrete clock fixtures (system clock jumps backwards mid-session; `advance` past the deadline while paused; two `tick()` calls in the same millisecond) and their expected outcomes. Effort: S.
5. Delete the PostgreSQL/Recipeweb sentences from `VERIFICATION.md:20`. Effort: S.

## One-paragraph summary for the index
The best-tested of the four plain-browser courses: it replaces "subtract one second per tick" with deadline arithmetic, makes `startTimer` idempotent, and proves with a controllable clock that a 45-second browser stall shows `00:15` rather than `00:59` and that a late callback cannot log two sessions. Every line reference and excerpt checks out, and the course is honest that it fixes callback drift rather than every clock anomaly. The catch is relevance: if your goal is CRUD web development, timer arithmetic is a detour, and the only directly transferable idea is the idempotency guard. Take it as a two-hour elective if you want a clean lesson in "scheduled callbacks are not a measure of elapsed time"; skip it if you are short on time and go straight to the `newcodexJS` API courses.
