import sys, json, os
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe, family_express as fx
S = 'js1-poll-studio'; P = fe.REG[S]['abs']; os.chdir(P); done = []

fx.prereqs(S, """Two things matter here: array and object literals (a poll is an object holding an array of option objects, each with a stable `id`) and `localStorage` basics (`getItem`/`setItem` store strings, so `JSON.stringify`/`JSON.parse` sit on every write and read, and `setItem` can throw). No server, no React, no SQL.""")
fx.limits(S, """Everything is in one browser tab: `localStorage` is the whole store, a second tab does not see this tab's changes until it reloads, and there is no server to validate anything. The `commitPolls` helper is the only write path; failures are simulated by making `setItem` throw. Exercises are future learner work.""")
done.append('review#1 README prerequisites and VERIFICATION limits are specific to a browser-only app')
fe.rw('index.html', lambda t: t.replace('maxlength="120"', 'maxlength="160"', 1))
fe.append_section(S, '02', '## Two layers, one rule', """`handleSubmit` in `app.js` rejects a question longer than 160 characters. The `<input id="poll-question" maxlength="160">` in `index.html` now says the same thing to the browser, so a user cannot type past the limit and the JavaScript check only fires for pasted or scripted input. Before the fix pass the input said 120 while the code said 160: two layers, two rules, and a confusing experience where the browser stopped you 40 characters early. Keep the two numbers together (or derive one from the other) whenever you add a bound.""")
done.append('review#3 index.html maxlength now matches the 160-character rule in handleSubmit; 02 explains the two-layer bound')
open('.gitattributes', 'w', encoding='utf-8', newline='\n').write('* text=auto eol=lf\n')
done.append('review#4 .gitattributes normalizes line endings to LF so future diffs of app.js are readable')
fx.exercises(S, {
 1: "Starting state: options can be added and removed but not reordered. Add move-up/move-down buttons in `renderOptionRows` (`app.js:64`). Acceptance: after any reorder, `poll.options.map(o => [o.id, o.votes])` is a permutation of the pre-move pairs (ids and votes travel together), and `commitPolls` is called once per move.",
 2: "Starting state: votes are counted but not shown as percentages. Add a percentage per option derived at render time. Acceptance: percentages sum to 100 (or all 0 with no votes), nothing new is stored, and `resetVotes` still zeroes every option.",
 3: "Starting state: `commitPolls` catches a failed `setItem`. Write a test in `test/polls.test.cjs` that makes `Storage.prototype.setItem` throw during a vote. Acceptance: the vote total, the poll and the edit draft are unchanged and the message names the failure (the third delivered test is the model).",
 4: "Starting state: the store is `localStorage`. Port `commitPolls` to a `fetch`-backed store: `PUT /polls` with the candidate array, treat a non-2xx as a failed commit, and publish to `state` only after the response. Acceptance: a test with a stubbed `fetch` that rejects shows the same invariants as exercise 3; this is the path onto the server stack.",
})
fe.set_reviews(S, [
 "reorder must preserve id/vote pairs (assert the permutation), must go through `commitPolls`, and must not renumber ids.",
 "percentages must be derived at render time; the test asserts the sum and that the stored poll is unchanged.",
 "the failing `setItem` must be injected around a vote, and the test must assert vote totals, the poll and the draft in one go.",
 "the fetch-backed commit must keep the same publish-after-commit order and the same failure behavior; the test must stub `fetch` to reject and assert nothing was published.",
]); done.append('review#2 exercises 1-4 with poll-specific acceptance; review#5 exercise 4 ports commit-before-publish to a fetch store (05, 06)')
fe.set_boundaries(S, [
 ("the form decides what to commit", "`app.js:96` `handleSubmit`: reads the question and option rows, validates length and duplicates, builds a `candidate` polls array with stable option ids, and calls `commitPolls(candidate)`."),
 ("the candidate is serialized", "`commitPolls` (`app.js:57`): `JSON.stringify(candidate)` then `localStorage.setItem(STORAGE_KEY, ...)` inside `try`; nothing in `state` has changed yet."),
 ("the storage boundary accepts or throws", "`setItem` can throw (quota, private mode). The `catch` shows a message and returns `false`, so callers return early and `state.polls` still holds the previous value."),
 ("publish only after success", "each caller (`handleSubmit`, `vote`, `resetVotes`, `deletePoll`) assigns `state.polls = candidate` and calls `render()` only when `commitPolls` returned `true`: commit before publish."),
 ("the read path reconstructs state", "`loadPolls` (`app.js:50`) parses `localStorage` on start; a reload proves what was actually committed."),
 ("the render shows committed state", "`render()` (`app.js:150`) draws from `state.polls`; the first test removes an option and checks the remaining ids and votes survived a reconstruction."),
]); done.append('2.2 trace-lab call path section (07)')
fe.set_variations(S, """**Normal variation — remove the first option.** With three options and votes, remove the first: predict the remaining two keep their ids and votes (first test).

**Invalid variation — a duplicate option.** Submit options `["A", "a"]`: predict the rejection message and that the saved poll is unchanged (second test). Paste a 170-character question: predict the browser truncates at 160 (maxlength) and, if scripted, `handleSubmit` rejects it.

**Boundary variation — a failed write.** Make `setItem` throw and vote: predict the totals, the poll and the edit draft unchanged (third test)."""); done.append('2.4 three concrete variations')
fx.pin(P); done.append('dependencies pinned (dev tooling only: this project has no runtime dependencies)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
