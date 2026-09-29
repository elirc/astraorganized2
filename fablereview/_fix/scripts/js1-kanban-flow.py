import sys, json, os
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe, family_express as fx
S = 'js1-kanban-flow'; P = fe.REG[S]['abs']; os.chdir(P); done = []

fe.rw('styles.css', lambda t: t.replace(".link-button.danger {", """.move-column {
  width: 100%;
  margin: 6px 0 0;
  padding: 4px 6px;
  font-size: 0.82rem;
  font-weight: 800;
  color: var(--brand);
  background: none;
  border: 1px solid var(--brand);
  border-radius: 6px;
}

.move-column:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

.link-button.danger {""", 1))
done.append('review#1 .move-column styled (width, margin, font, focus ring) consistent with .link-button')
def noop(t):
    old = """  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(candidate)); }
  catch { showMessage("Could not save the move. The board is unchanged."); return false; }
  state.cards = candidate; render(); showMessage("Card moved."); return true;"""
    new = """  // A drop that changes nothing must not claim it moved anything, and must not write.
  if (JSON.stringify(candidate) === JSON.stringify(state.cards)) { showMessage("Card is already there."); return true; }
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(candidate)); }
  catch { showMessage("Could not save the move. The board is unchanged."); return false; }
  state.cards = candidate; render(); showMessage("Card moved."); return true;"""
    assert old in t
    return t.replace(old, new, 1)
fe.rw('app.js', noop)
fe.append_section(S, '02', '## Feedback for operations that changed nothing', """`moveCard` now compares the renumbered `candidate` with `state.cards` before writing. If nothing changed (a card dropped onto its own position), it says `Card is already there.` and returns without touching `localStorage`. Two reasons: a message that says "moved" when nothing moved trains users to distrust messages, and a no-op write is still a write that can fail (quota) and can overwrite another tab's newer state. The same idea appears on the server courses as the idempotency guard in a status handler.""")
done.append('review#4 no-op drops report "Card is already there." and skip the write; 02 explains feedback for no-op operations')
def patch_test(t):
    add = '''
test("a stale snapshot committing over a newer one wins by last write: the persisted board loses the earlier move", () => {
  const d = app(),
    a = d.window.lesson;
  a.state.cards = [
    { id: "a", title: "A", column: "todo", order: 0 },
    { id: "b", title: "B", column: "todo", order: 1 },
  ];
  d.window.localStorage.setItem("js1-kanban-flow", JSON.stringify(a.state.cards));
  // Tab 1 and tab 2 both start from this board.
  const tab2Snapshot = JSON.parse(JSON.stringify(a.state.cards));
  // Tab 1 moves A to doing and persists.
  assert.equal(a.moveCard("doing", null, "a"), true);
  assert.equal(JSON.parse(d.window.localStorage.getItem("js1-kanban-flow")).find((x) => x.id === "a").column, "doing");
  // Tab 2 still holds the old board in memory and moves B: it persists its whole (stale) board.
  a.state.cards = tab2Snapshot;
  assert.equal(a.moveCard("done", null, "b"), true);
  const persisted = JSON.parse(d.window.localStorage.getItem("js1-kanban-flow"));
  assert.equal(persisted.find((x) => x.id === "b").column, "done");
  assert.equal(persisted.find((x) => x.id === "a").column, "todo", "tab 1's move was overwritten: last writer wins");
  d.window.close();
});
test("dropping a card onto its own position writes nothing", () => {
  const d = app(),
    a = d.window.lesson;
  a.state.cards = [{ id: "a", title: "A", column: "todo", order: 0 }];
  d.window.localStorage.setItem("js1-kanban-flow", "sentinel");
  assert.equal(a.moveCard("todo", null, "a"), true);
  assert.equal(d.window.localStorage.getItem("js1-kanban-flow"), "sentinel");
  d.window.close();
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/movement.test.cjs', patch_test); done.append('review#5 fourth test shows the cross-tab last-writer-wins conflict; fifth test proves a no-op drop writes nothing')
fx.prereqs(S, """Two things matter here: array copies and renumbering (`moveCard` builds a `candidate` copy, re-sorts each column and rewrites `order` from 0), and `localStorage` as the only store, including the fact that a second tab holding an older board will overwrite a newer one. No server, no React, no SQL.""")
fx.limits(S, """Single tab only: there is no `storage` event handling, so two open tabs overwrite each other (the fourth test shows it); rename uses `prompt()`; the store is `localStorage` with no server. The keyboard move control is the accessible alternative to drag-and-drop. Exercises are future learner work.""")
done.append('review#2 README prerequisites and VERIFICATION limits state the real limits (single tab, no storage event, prompt rename)')
fx.exercises(S, {
 1: "Starting state: drop targets are columns and cards. Add a per-column `order` invariant check after every move in `moveCard`. Acceptance: after any move, for every column the set of `order` values equals `0..n-1` (write the assertion as a helper and use it in every test).",
 2: "Starting state: cards have a title only. Add a `dueDate` field with the same calendar validation as the server courses (`YYYY-MM-DD`, real day). Acceptance: `2027-02-29` is rejected without writing, and a card sorted by due date keeps the id tie-break.",
 3: "Starting state: `handleAdd` writes then renders. Make a storage failure during add leave the board and the form unchanged. Acceptance: a test that makes `setItem` throw during add asserts the card list length and the input value are unchanged.",
 4: "Starting state: two tabs overwrite each other. Listen to the `storage` event and reload `state.cards` from the newer value before applying a move. Acceptance: the fourth test's scenario now keeps both moves (A in doing, B in done) when the second tab refreshes before moving; document the remaining window.",
})
fe.set_reviews(S, [
 "the invariant helper must check every column after every move in every test, and must fail if two cards share an `order` in one column.",
 "the date rule must be the same round-trip check the server courses use, the rejection must not write, and the sort must fall back to id.",
 "the failure must be injected during add, and the test must assert both the board and the form draft are unchanged.",
 "the `storage` handler must merge by reloading before a move (not by blindly replacing `state`), and the write-up must name the remaining race between reload and write.",
]); done.append('review#3 exercises 1-4 with board-specific acceptance; distinct review paragraphs (05, 06)')
fe.set_boundaries(S, [
 ("the drop or keyboard control decides what to move", "`app.js:144` (drop) and `moveByKeyboard` (`app.js:105`) call `moveCard(columnId, beforeId, cardId)`; the `.move-column` select (`app.js:188`) is the keyboard path."),
 ("`moveCard` builds a candidate", "`app.js:86`: validate the target column and `beforeId`, copy every card, set the moved card's column, re-sort and renumber every column from 0."),
 ("no-op detection", "if the candidate equals the current board, report `Card is already there.` and return without writing (fix pass)."),
 ("the storage boundary accepts or throws", "`localStorage.setItem` inside `try`; on failure show the message and return `false` with `state.cards` untouched."),
 ("publish only after success", "`state.cards = candidate; render(); showMessage(\"Card moved.\")` runs only after the write succeeded: commit before publish."),
 ("the read path reconstructs state", "`loadCards` (`app.js:30`) parses `localStorage` on start; the first test reloads to prove the persisted order, and the fourth shows what a stale tab does to it."),
]); done.append('2.2 trace-lab call path section (07)')
fe.set_variations(S, """**Normal variation — move between columns.** Move A from `todo` to `doing` before C: predict B becomes order 0 in `todo`, A order 0 and C order 1 in `doing` (first test).

**Invalid variation — a bad target.** Move to a column that does not exist, or before a card in another column: predict `false` and no write (second test). Drop A onto its own position: predict `Card is already there.` and no write (fifth test).

**Boundary variation — two tabs.** Follow the fourth test by hand with two browser tabs: move in tab 1, then move in tab 2 without reloading; reload both and see tab 1's move gone."""); done.append('2.4 three concrete variations')
fx.pin(P); done.append('dependencies pinned (dev tooling only)')
fx.bump_verification_count(S, 3, 2, 'test/movement.test.cjs')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
