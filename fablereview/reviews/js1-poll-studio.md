# JS1/poll-studio — Fable review

- **Path:** `JS1/poll-studio`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + DOM + localStorage (no build, no server)  ·  **Batch:** B03
- **Astra's change (one line):** Draft option rows now carry stable UUIDs so votes follow the option rather than its array index; `handleSubmit` gained length/blank/case-insensitive-duplicate validation; and every mutation (save, vote, reset, delete) routes through a new `commitPolls(candidate)` that writes to localStorage first and only then publishes the candidate into `state.polls`.
- **Course size:** 5,953 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 in `test/polls.test.cjs` (+ `test/browser.cjs` jsdom loader)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 3 | 4 | 5 | 4 | 3 | 4.0 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- The change is a genuine correctness fix, not cosmetics. Before, `app.js` kept votes only when `existing.options.length === texts.length` and matched by index (`backups/21/app.js:112-118`); removing one row silently reassigned every other option's votes. After, votes are looked up by option id: `votes: existing?.options.find(x => x.id === option.id)?.votes ?? 0` (`app.js:107`).
- `commitPolls` (`app.js:66-71`) is a real commit-before-publish boundary: `localStorage.setItem` is attempted inside `try`, and `state.polls = candidate` only runs on success. All four mutators use it.
- The tests exercise behaviour, not call counts. Test 3 overrides `w.Storage.prototype.setItem` to throw and then asserts that `state.polls` is byte-identical before/after a vote, a submit and a delete, *and* that the in-progress question draft survives (`test/polls.test.cjs:19-25`).
- Test 1 asserts against the authoritative store, not just memory: `JSON.parse(w.localStorage.getItem('js1-poll-studio'))[0].options[0].votes === 7`.
- `index.html` hint text was updated to match the new behaviour, so the UI does not lie about vote retention.

## Problems found (evidence required)
- **[D8]** The scaffolding is a shared template. `astraupskill/05-PRACTICE.md` is byte-identical to `JS1/pulse-analytics/astraupskill/05-PRACTICE.md` except for the fixture line and four exercise titles; the "Review:" paragraph is repeated verbatim under all four exercises in `06-SOLUTIONS-AND-REVIEW.md` ("Demonstrate an ordinary case and a case that would break a naive implementation…").
- **[D8/D1]** `README.md` Prerequisites carries cross-batch boilerplate irrelevant here: "For React projects, review props, state and event handlers. For API projects, review JSON, HTTP methods and promises, then learn the relevant SQL operations…" — this project has neither React nor an API. `VERIFICATION.md` similarly says "PostgreSQL 18.1 where applicable" and lists limits about "status-command semantics… and transaction scope".
- **[D2]** The whole of `app.js` was rewritten from LF to CRLF line endings, so `diff -r backup project` reports 100% churn and the real ~40-line change is invisible without `--strip-trailing-cr`. Same for `index.html`/`README.md`.
- **[D4]** Off the target stacks: no React, no Node/Express, no SQL, no HTTP. The transferable ideas (identity vs index, validate-then-commit) are real but the learner practises them only against `localStorage`.
- **[D2, minor]** The 160-char question and 80-char option limits live only in `handleSubmit`; `index.html` has `maxLength` on option inputs but not on `#poll-question`, so the server-of-record rule and the UI affordance disagree.

## Spot-checks performed
- "The excerpt below comes from app.js near line 96" (`03-WORKED-CHANGE.md`) -> `sed -n '96p' app.js` = `function handleSubmit(event) {` -> matches exactly, and the pasted excerpt is the current source verbatim.
- VERIFICATION claims 3 automated cases and a passing Chromium check -> `implementation/batch03/logs/21-tests.log` shows `# tests 3 / # pass 3 / # fail 0`; `browser-checks.json` entry `{"project":"21","passed":true}` with `logs/21-browser.png` on disk -> matches.
- "Public API retains 7 votes and Dark mode retains 2, for 9 total" -> `starterPolls` in `app.js:6-14` holds Mobile 4 / Public API 7 / Dark mode 2, and `test/polls.test.cjs:8` asserts `'7,2'` after removing row 1 -> matches.
- "a failed write preserves … the current draft" -> verified in `test/polls.test.cjs:22-23`, which re-reads `#poll-question` after the throwing setItem -> matches.

## Improvements needed (ordered, concrete, actionable)
1. In `astraupskill/README.md` and `VERIFICATION.md`, delete the React/API/PostgreSQL boilerplate sentences and replace the Prerequisites paragraph with the two things this course actually needs: array/object literals and `localStorage` basics. (effort: S)
2. In `05-PRACTICE.md`, replace the generic exercise wrappers with poll-specific acceptance criteria — e.g. for Exercise 1 state "after reordering, assert `options.map(o => [o.id, o.votes])` is a permutation of the pre-move pairs". Right now every exercise body is the same paragraph. (effort: M)
3. Add `maxlength="160"` to `#poll-question` in `index.html` so the UI matches the rule in `handleSubmit`, and mention the two-layer validation in `02-CONCEPTS.md`. (effort: S)
4. Add a `.gitattributes` or re-save touched files as LF so future diffs of `app.js` are readable. (effort: S)
5. Add one exercise that ports the same commit-before-publish idea to a `fetch`-backed store, to give the lesson a path onto the target stack. (effort: M)

## One-paragraph summary for the index
A short, honest course on two ideas that bite every CRUD developer: an array index is not an identity, and state should not be published until the write succeeds. The code change is real (votes now follow option ids, and every mutation goes through a single `commitPolls` boundary) and the three jsdom tests actually force a storage failure and check that neither the saved poll nor the in-progress draft is damaged. The weak spots are scaffolding, not substance: the practice and solutions chapters are a shared template with the noun swapped, and the README's prerequisites talk about React and SQL that this project does not have. Because it is plain DOM + localStorage with no server, treat it as an elective warm-up before the Express projects in this batch rather than a core stop. Budget two to three hours.
