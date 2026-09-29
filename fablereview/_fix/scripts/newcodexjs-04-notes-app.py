import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-04-notes-app'
P = fe.REG[S]['abs']
os.chdir(P)
done = ['review#1 test split into four named blocks and review#4 tie-break test were completed by the earlier fix agent (verified on disk)']

fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **1 test block containing ~16 assertions** (`server/test/search.test.cjs`) across create, search, filter, partial update and four validation rejections.", "Automated test cases: **4** named blocks in `server/test/search.test.cjs` (search semantics, filter composition, deterministic ordering, partial update and validation rejections), about twenty assertions in total. Astra delivered them as one block; the fix pass split them so the count reflects the coverage.", 1))
done.append('review#1 VERIFICATION count updated to the four named blocks')

# review #2: GIN index migration + EXPLAIN walkthrough
mig = '''/** Adds the expression index the search predicate in models/model.js can use. */
exports.up = async function up(knex) {
  await knex.raw(
    "CREATE INDEX IF NOT EXISTS notes_search_idx ON notes USING GIN (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, '')))",
  );
};
exports.down = async function down(knex) {
  await knex.raw("DROP INDEX IF EXISTS notes_search_idx");
};
'''
open('server/db/migrations/002_search_index.js', 'w', encoding='utf-8', newline='\n').write(mig)
fe.append_section(S, '04', '## Seeing the index work: `EXPLAIN` before and after', """The search predicate in `server/src/models/model.js` is `to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')) @@ plainto_tsquery('english', ?)`. Without an index PostgreSQL has to compute the vector for every row on every search. Migration `server/db/migrations/002_search_index.js` adds a GIN index on exactly that expression; the expression must match the query text for the planner to use it.

Watch it happen in `psql` against your development database (run `npm run migrate` first):

```sql
INSERT INTO notes (title, body, folder, status)
SELECT 'note ' || g, repeat('lorem ipsum ', 50), 'bulk', 'active' FROM generate_series(1, 20000) g;
EXPLAIN ANALYZE SELECT * FROM notes
 WHERE to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')) @@ plainto_tsquery('english', 'ipsum');
```

Before the migration the plan is `Seq Scan on notes` with a `Filter:` line and a time that grows with the table. After `npm run migrate` the same statement shows `Bitmap Heap Scan on notes` fed by `Bitmap Index Scan on notes_search_idx`. The tests do not depend on the index (they apply only `001_init.js` into a throwaway schema); correctness is the same either way, which is the point: an index changes cost, not answers.""", before='## ')
done.append('review#2 migration 002_search_index.js (GIN expression index) and an EXPLAIN walkthrough in 04')

# review #3: replace generic Mermaid with the real request path
def fix01(t):
    start = t.find('```mermaid')
    if start < 0:
        return t
    end = t.find('```', start + 10) + 3
    tail_para = t.find('\n\n', end)
    new = '''```mermaid
flowchart LR
    A[Search box in client/src/App.jsx] -->|250 ms debounce, line 43| B[GET /api/notes?search=...]
    B --> C[routes -> controller.list]
    C --> D[services/service.js list: bounds search/status/folder]
    D --> E[models/model.js listRecords: to_tsvector @@ plainto_tsquery, ORDER BY created_at DESC, id DESC]
    E --> F[PostgreSQL: notes table, optional GIN index 002]
    F --> G[sendSuccess envelope -> React list]
```

Every box is a file you can open; the arrows are the order a search request actually takes.'''
    return t[:start] + new + t[tail_para:] if tail_para > 0 else t[:start] + new
fe.rw(fe.chapter(S, '01'), fix01)
done.append('review#3 01 diagram replaced with the real request path')

# review #5: concrete exercises 2 and 4
fe.rw(fe.chapter(S, '05'), lambda t: t.replace("Rank by relevance with stable ties.\n\nClose the worked-change chapter while implementing. Describe your design in three sentences: the data you will add or reuse, the rule it must preserve, and the observation that proves it.",
    "Rank by relevance with stable ties: add `ts_rank(to_tsvector('english', ...), plainto_tsquery('english', ?))` as a selected column and order by it descending, then by `created_at DESC, id DESC`. Prove it changes result order: insert one note whose title contains `postgres index` twice and another that mentions `index` once in the body, search `postgres index`, and assert the first note comes first even though it was created earlier.\n\nClose the worked-change chapter while implementing. Describe your design in three sentences: the data you will add or reuse, the rule it must preserve, and the observation that proves it.", 1).replace(
    "Design multilingual search.\n\nWrite a short design note before coding.",
    "Design multilingual search: add a `language` column (per note or per workspace, decide and justify), build the vector with `to_tsvector(language::regconfig, ...)`, and show what happens to stemming by inserting `running` and searching `run` under `english` and then under `simple` (no stemming). The expression index from exercise 1 must include the language or it will not be used.\n\nWrite a short design note before coding.", 1))
done.append('review#5 exercises 2 and 4 made concrete (ts_rank proof; language config with a stemming demonstration)')

B = [
("the search box decides when to ask",
 "`client/src/App.jsx:41-43`: a `useEffect` on the search text waits 250 ms (`setTimeout(refresh, 250)`) and cancels the timer on the next keystroke, so the server sees one request per pause, not one per key. The stale-response race (exercise 3) lives here."),
("the request leaves the browser",
 "`GET /api/notes?search=<text>&status=&folder=` through the client's API service; the response envelope is unwrapped and the list is replaced wholesale."),
("the service bounds the filters",
 "`server/src/services/service.js:25` `list(query)`: each of `search`, `status`, `folder` must be a string of at most 255 characters (line 27), otherwise `ValidationError`; `sanitizePayload` (line 9) does the same for writes and rejects an empty edit with `At least one note field is required.`"),
("the model builds one query",
 "`server/src/models/model.js:4` `listRecords`: `ORDER BY created_at DESC, id DESC` (the tie-break the third test pins), exact `status`/`folder` filters, and the full-text predicate over `title || ' ' || body` with `plainto_tsquery`, which strips operators so `%` and `*` are plain words, never wildcards."),
("PostgreSQL evaluates the text search",
 "`to_tsvector('english', ...)` stems words (`running` matches `run`) and ignores stop words; the optional GIN index from migration 002 makes it cheap. Ids and timestamps are not in the vector, which is what the first test proves by searching for a fragment of an id and getting nothing."),
("the envelope returns rows the client renders",
 "`sendSuccess` returns `{ success: true, data: [...] }`; the client replaces its list. Because ordering is stable, a re-run of the same search gives the same order, which is what makes the stale-response race detectable in a test."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the migration must create the GIN index on the exact expression used in `listRecords` (byte-for-byte, including `coalesce` and the `' '` separator) or the planner will not use it; your evidence is the two `EXPLAIN` plans from chapter 4 pasted into the write-up, and the four tests still green.",
"`ts_rank` must be computed from the same `tsquery` used for filtering, ordering must fall back to `created_at DESC, id DESC` for equal ranks, and the test must show a lower-ranked but newer note ordered *after* a higher-ranked older one.",
"the test must delay the first search response and resolve the second first (mock the API in a client test), then release the first and assert the second's results are still displayed; explain which line in `App.jsx` (the cleared timer, or a request sequence guard you add) makes it pass.",
"the design must state where `language` lives, how the expression index changes (`to_tsvector(language::regconfig, ...)` cannot use a per-row column in an index expression unless it is immutable; say how you handle that), and demonstrate stemming differences with a two-word fixture.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.set_variations(S, """**Normal variation — stemming.** Create notes with `running shoes` and `a good run`, search `run`. Predict both match (English stemming). Search `%`: predict zero matches and no error (`plainto_tsquery` treats it as no words).

**Invalid variation — an oversized filter.** `GET /api/notes?search=<300 characters>`. Predict 400 `Filters must be text up to 255 characters.` before any query. `PUT /api/notes/:id` with `{}`: predict 400 `At least one note field is required.` and the row unchanged.

**Boundary variation — equal timestamps.** Insert two notes in one transaction so `created_at` is identical (the third test does this with `db.transaction`), list them twice, and predict the order is identical both times because of `id DESC`; then remove the second `orderBy` on a throwaway branch and observe whether PostgreSQL still happens to agree (it may, which is why the test exists)."""); done.append('2.4 three concrete variations')
fe.add_exercise(S, 'ownership and authorization',
"""Notes have no owner. Add one end to end.

1. Migration `003_owner.js`: `owner text NOT NULL DEFAULT 'anonymous'` on `notes`.
2. Middleware in `server/src/app.js`: read `X-Actor`, attach `req.actor`; blank on `POST`/`PUT`/`DELETE` -> 401.
3. `service.list` adds `owner: req.actor` to the filters and `listRecords` applies it in the `WHERE`; `get`, `update` and `remove` load with `{ id, owner }` and answer 404 for a foreign note.
4. Test: `ana` creates two notes; `ben` lists (empty), gets one (404), edits (404, unchanged); `ana` sees both.""",
"""Reference: `listRecords(query)` gains `builder.where("owner", query.owner)`; `findRecord(id, owner)` becomes `.where({ id, owner }).first()`; the service passes `req.actor` through. Keep the search predicate unchanged so the index still applies.

Review: the owner belongs in every `WHERE`, including search, so a full-text hit on someone else's note never leaks; explain why 404 (not 403) is the right answer for a foreign id."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
