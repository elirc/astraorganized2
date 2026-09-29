# JS1/contact-book — fix report (B01)

## Done
- [review #1] **Code fix.** `persistContacts()` replaced by `commitContacts(next)` (`app.js:56-67`): persist first inside a `try`, publish `contacts = next` only after `setItem` returns, otherwise report "Could not save. Your contacts are unchanged." and return false. `saveContact` (`app.js:97-106`) now builds a replacement array and returns early on a failed write, so the form stays populated for a retry and `resetForm()` is only reached on success. `deleteContact` (`app.js:125-131`) got the same treatment. This closes the gap the review named: chapter 2's "state transitions and failure boundaries" section now describes behaviour the project actually has.
- [review #1 tests] Added two cases to `test/duplicates.test.cjs`: a failed write on create (asserts `contacts.length === 2`, storage byte-identical to the fixture, `#name` still `"Cara"`, `/Could not save/`) and a failed write on delete. Suite is now 4 cases.
- [review #2] `README.md` Scope gained a "Known gap: contacts that were already duplicates" paragraph explaining that the rule is enforced on write only, why auto-merge is the wrong answer, and pointing at exercise 3. Also recorded as a "Known limit" in `VERIFICATION.md`.
- [review #3 / backlog 2.4] Replaced the generic "Three variations" block with three real ones that all hinge on the stated matching policy (`trim().toLowerCase()`, not RFC email equality): plus-tag subaddressing (accepted), `U+0130` dotted capital I (accepted, because `'İ'.toLowerCase()` is two code points), trailing dot vs surrounding whitespace (accepted / rejected, with the byte-identical assertion explained).
- [backlog 2.4] "Actual implementation excerpt" now shows changed lines: the excerpt was refreshed to the current `saveContact`, and a new "The changed lines, isolated" subsection shows the delivered uniqueness guard (`app.js:86-95`) and the follow-up write boundary as before/after pairs against `implementation/backups/02/app.js`.
- [review #5] Expanded rather than merged: exercise 3's solution now contains a real normalized-key `Map` index (`emailIndex`, `duplicateGroups`, `findDuplicate`) that replaces the O(n)-per-save `contacts.find` scan and is shared by the guard and the review screen; exercise 4's solution contains the matching `CREATE UNIQUE INDEX contacts_email_key ON contacts (lower(btrim(email)))` plus the 23505→409 translation.
- [backlog 2.3 / 3.11] `06-SOLUTIONS-AND-REVIEW.md`: all four exercises now have real code and a **distinct** review paragraph naming the specific naive implementation that breaks, the demonstration fixture, and the invariant that must not move. Generic "Demonstrate an ordinary case…" count is 0.
- [backlog 2.2] `07-TRACE-LAB.md`: added "The six boundaries of one save" — DOM input surface (`app.js:26-49`, `:167-168`), normalization (`:72-79`), required-field validation (`:81-84`), the collection-level uniqueness rule (`:86-95`), the persistence boundary (`commitContacts`, `:56-67`, called from `:102`/`:125`), publication and render (`:104-106`, `getFilteredContacts:141`) — followed by a backwards trace of one failure and a comparison of the layer-4 and layer-5 rejection paths. The existing "Validate before mutation" section was kept and sharpened with the three places `aria-invalid` is cleared (`:48`, `:95`, `:133`).
- [D1 setup accuracy, same defect the task-board review names] `README.md` and `04-TESTING-AND-DEBUGGING.md` now tell the learner to serve over HTTP instead of opening `index.html` over `file://`, with the reason.
- [backlog 2.7] `npm install --prefer-offline` run; `package-lock.json` now present. No `"latest"` dependency existed (`jsdom: ^25.0.1`).
- [VERIFICATION] Test count 2 → 4 with the split stated, the new scenarios described, and the follow-up run recorded.

## Skipped
- Backlog 2.5 (ownership/authz): not a server project and no user/actor concept. Exercise 4's solution is the bridge — it now contains the server-side uniqueness constraint and the conflict-response mapping.
- Backlog 2.1/2.6/2.8/2.9/2.10: already applied by the wave-1 sweep; verified and not redone.
- Review #4 (strip PostgreSQL/Recipeweb sentences from `VERIFICATION.md:20`): already done by the sweep.
- Review #5's alternative ("merge this course into JS1/task-board"): not taken. The expansion route was chosen instead, per the review's own "either/or".

## Verification
- `npm install --prefer-offline --no-audit --no-fund` → `added 60 packages in 2m`
- `node --test test/duplicates.test.cjs` → `# tests 4 / # pass 4 / # fail 0`
- Line references re-derived after the edit: `loadContacts:51`, `commitContacts:56`, `saveContact:69`, duplicate guard `:86-95`, `editContact:109`, `deleteContact:125`, `resetForm:132`, `getFilteredContacts:141`, `renderContacts:148`, `setMessage:180`. Every citation added or touched in the course was checked against this.

## Course/code consistency check
- `03-WORKED-CHANGE.md`: excerpt re-synced to the current `saveContact` (the old excerpt still showed `contacts.unshift` + `persistContacts()`), "near line 60" → "near line 69".
- `07-TRACE-LAB.md`: every cited line checked individually.
- `README.md` Scope and `VERIFICATION.md` both now describe the write boundary that exists.
- `04-TESTING-AND-DEBUGGING.md` "What the test suite proves" extended with cases 3 and 4.
- Searched the whole course for stale `persistContacts` references: the only remaining occurrence is inside the intentional "before" code block in `03-WORKED-CHANGE.md`.
