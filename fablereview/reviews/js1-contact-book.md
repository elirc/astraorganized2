# JS1/contact-book — Fable review

- **Path:** `JS1/contact-book`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests)  ·  **Batch:** B01
- **Astra's change (one line):** Added a case-insensitive, whitespace-trimmed duplicate-email guard to `saveContact` that excludes the record currently being edited, plus `aria-invalid`/focus feedback on the email field, and rejects before any array mutation or storage write.
- **Course size:** 4,969 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/duplicates.test.cjs`, plus harness `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 4 | 4 | 5 | 4 | 4 | 3 | 4.0 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- The change teaches the single most common junior uniqueness bug correctly: the `item.id !== editingId` term in the predicate (`app.js:76-78`). `07-TRACE-LAB.md` calls it out explicitly — "Without that exclusion, every unchanged-email edit finds itself and looks like a duplicate" — which is exactly the failure a junior ships.
- Validate-before-mutate is enforced and tested. The first test asserts `localStorage.getItem(KEY)` is *byte-identical* to the fixture after a rejected create and after a rejected edit, not just that an error message appeared. That is a much better oracle than checking the message.
- Accessibility is part of the change, not an afterthought: `emailInput.setAttribute("aria-invalid","true")` plus `focus()` on failure, and `removeAttribute("aria-invalid")` on the success path (`app.js:79-84`). The test asserts the attribute.
- The trace lab honestly flags the limit of an in-memory uniqueness check: "two concurrent requests could both pass an array-like duplicate check. A uniqueness constraint on the chosen normalized representation would provide a separate database safeguard." That is the right bridge to the Postgres courses later in this batch.

## Problems found (evidence required)
- **[D2]** The change is about 8 lines of production code and 2 tests for a 4,969-word course. Unlike its sibling `JS1/task-board`, there is no failed-write path: `persistContacts()` (`app.js:55-57`) still writes unguarded and the course's own `02-CONCEPTS.md` section "State transitions and failure boundaries" ("If memory changes first and persistence fails, the UI can show data that will disappear after reload") describes a hazard this project never addresses or tests. The generic chapter and the specific change are talking past each other.
- **[D2]** The duplicate rule is only applied on write. Existing storage can already contain two contacts differing by case; nothing detects or reports that, and the course does not mention it as a known gap in `README.md` Scope.
- **[D8]** `02-CONCEPTS.md`, `05-PRACTICE.md` and `06-SOLUTIONS-AND-REVIEW.md` are cross-project templates with a handful of substituted lines. `05-PRACTICE.md` shares 42 of 47 lines with `newcodexJS/05-recipe-manager/astraupskill/05-PRACTICE.md`; the paragraph "Start by locating the current input, handler and output. Write an acceptance example before editing. Make one small change, run the focused tests…" is byte-identical in all ten B01 courses.
- **[D3]** `03-WORKED-CHANGE.md`'s "Three variations to work through" names no actual variations for this project — the learner is told to invent them.
- **[D6]** `VERIFICATION.md:20` claims "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" for a project with no database, and mentions Recipeweb's dependency tree. Shared-harness boilerplate in a per-project honesty document.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): excerpt of `saveContact` "near line 60". -> `sed -n '59,84p' app.js` — `function saveContact(event)` is at line 59 and the quoted body matches character for character, including `` `A contact with this email already exists: ${duplicate.name}.` ``. -> **matches.**
- Course claim (`VERIFICATION.md`): "Ada owns Ada@Example.com. Creating Other with \" ada@example.COM \" fails." -> `test/duplicates.test.cjs` fills `#email` with `' ada@example.COM '` and asserts storage is unchanged; `app.js:77` compares `item.email.trim().toLowerCase() === contact.email.toLowerCase()` where `contact.email` was already trimmed at `app.js:65`. -> **matches.**
- Course claim (`07-TRACE-LAB.md`): "The invalid email field receives focus and `aria-invalid`". -> `app.js:81-82`. -> **matches.**
- Course claim (`VERIFICATION.md`): "Real Chromium browser interaction | Passed". -> `implementation/browser-checks.json` project "02" passed; `implementation/browser_checks.cjs:46-53` drives the real duplicate-create flow and asserts the email input holds focus. -> **matches.**
- Delivery claim: 2 test cases, 4,969 words. -> `test/duplicates.test.cjs` has exactly 2 `test(` blocks; `wc -w astraupskill/*` totals 4,969. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Extend the change (or at least the course) to cover the failed-write path so the chapter-2 "state transitions and failure boundaries" section is actually exercised here: route `persistContacts` through a try/catch that keeps the form open and the array unchanged, and add a third test that throws from `Storage.prototype.setItem` (mirror `JS1/task-board/test/undo.test.cjs`). Effort: S.
2. Add a "pre-existing duplicates" subsection to `README.md` Scope and one exercise: detect and report case-duplicates already in storage without auto-merging them. Effort: S.
3. Replace the generic "Three variations" block in `03-WORKED-CHANGE.md` with three real fixtures and expected outcomes (e.g. unicode-case `İ`, a trailing dot, `ada+tag@example.com`) and state explicitly that this app's matching policy is trim+lowercase, not RFC email equality. Effort: S.
4. Trim the PostgreSQL/Recipeweb sentences from `VERIFICATION.md:20`. Effort: S.
5. Because the change is so small, either merge this course into `JS1/task-board` as a second exercise or expand it with a normalized-key index (`Map` keyed by `trim().toLowerCase()`) so it earns a standalone slot. Effort: M.

## One-paragraph summary for the index
A very small but correct lesson on the classic "editing a record makes it look like its own duplicate" bug: uniqueness is compared case-insensitively on a trimmed key, the record under edit is excluded, and rejection happens before any mutation or write. Every claim in the course matches `app.js`, and the two tests assert that storage is byte-identical after a rejected save rather than trusting the error message. The problem is proportion — about eight lines of production code carry 4,969 words, most of which is a template shared with the other nine courses, and the project never demonstrates the failed-write handling its own concepts chapter preaches. Take it as a 45-minute elective after `JS1/task-board`, mainly for the trace lab, and don't expect it to stretch you.
