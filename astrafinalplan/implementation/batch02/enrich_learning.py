from pathlib import Path
import json
B=Path(__file__).resolve().parent
labs=[
('A session is a snapshot, not a live filter', '''const cards = [{id:'a',known:false},{id:'b',known:false}];
const order = cards.filter(card => !card.known).map(card => card.id);
// After grading a, keep order ['a','b']; advance cursor from 0 to 1.
// Refiltering to ['b'] before advancing would skip b.
''', 'Write four rows: initial cursor 0; reveal a; grade a and move to 1; grade b and move to 2. The last cursor equals order.length and means complete. A storage rejection inserts a branch before cursor movement: neither knowledge state nor cursor changes. Repeat grade after completion and explain why it must be harmless. Now change decks during a session: restarting is a deliberate reset, not retaining an order containing records from the previous deck. Distinguish an empty eligible set from a completed nonempty session; both have no current card, but their messages differ.'),
('Calendar adjacency survives daylight-saving transitions', '''const labels = ['2024-03-09', '2024-03-10', '2024-03-11'];
const ordinals = labels.map(day => Date.parse(day + 'T00:00:00Z') / 86400000);
console.log(ordinals[1] - ordinals[0]); // 1
console.log(ordinals[2] - ordinals[1]); // 1
''', 'These UTC ordinals index already chosen calendar labels; they do not choose the habit user\'s timezone. Compare this to subtracting local midnight timestamps across a daylight-saving boundary. One elapsed-time difference can be 23 hours while the labels remain consecutive dates. Add an invalid February 30 and explain why validation must precede ordinal conversion. Next list current-versus-best examples: an old five-day run with no check yesterday gives best five and current zero; a two-day run ending yesterday gives current two while today is still available. Removing one historic check may split the best run without changing the recent current run.'),
('Filtering and sorting are separate operations', '''const books = [
  {id:'z',title:'Zebra',rating:5,status:'Finished'},
  {id:'a',title:'Alpha',rating:5,status:'Finished'},
  {id:'b',title:'Beta',rating:5,status:'Reading'},
];
const visible = [...books].filter(book => book.status === 'Finished')
  .sort((a,b) => b.rating-a.rating || a.title.localeCompare(b.title));
console.log(visible.map(book => book.id)); // ['a','z']
console.log(books.map(book => book.id));   // ['z','a','b']
''', 'Add an author predicate to this reduced model and write the full truth table: matching status/matching text; matching status/nonmatching text; nonmatching status/matching text; neither. Only the first appears. Then explain two different denominators: matching count comes from visible, while overall finished count comes from books. An empty view does not mean saved data is empty. Finally change one visible book to Reading in the real editor. It should leave the Finished view and remain retrievable in All, with the same id. That is a state change followed by a new projection, not a deletion.'),
('Queue the whole operation', '''// Reduced ordering example, not a substitute for the file repository.
let tail = Promise.resolve();
function enqueue(operation) {
  const result = tail.then(operation);
  tail = result.catch(() => {}); // later work can still run
  return result;                // this caller still sees rejection
}
''', 'Draw an unsafe interleaving: A reads [welcome], B reads [welcome], A writes [welcome,a], B writes [welcome,b]. A disappears. Merely ordering the final writes keeps that same wrong result. Now put each read-modify-write in enqueue: B reads only after A commits and therefore sees a. Trace the rename-failure test next. The target file must still contain the exact previous bytes, not just an equivalent-looking list. The temporary sibling is owned by this operation and is cleaned up on failure. A later successful operation proves that the rejected promise did not poison tail. Reopening the repository after completion proves persistence, but two independent repository instances writing concurrently are outside this single-owner guarantee.'),
('Represent money deliberately', '''const tenCents = 10;
const twentyCents = 20;
console.log(tenCents + twentyCents); // 30
console.log((tenCents + twentyCents) / 100); // 0.3 for formatting
// Production parseCents validates text before constructing these integers.
''', 'Walk through 12.50: whole text 12 becomes 1200 cents, fractional text 50 contributes 50, total 1250. For 12.5, right-padding produces the same 50 cents. For 12.005, reject rather than silently rounding a newly entered value. The existing storage schema still saves dollar numbers; explain the compatibility boundary and why a complete migration would be a different task. Now trace an edit: original array, candidate array, serialized candidate, storage outcome, published array. A failure between serialization and publication keeps the original array. Totals remain whole-ledger values even when the user filters to one type; label that scope instead of assuming filters necessarily affect every dashboard number.'),
('Two independent flags need four cases', '''const today = '2026-09-08';
const low = item => item.quantity <= item.minimum;
const expired = item => item.expires < today;
// Validated YYYY-MM-DD labels can be compared lexicographically.
''', 'Build a four-row table: low and expired; low and not expired; stocked and expired; stocked and not expired. The Expired filter accepts rows one and three. Low accepts one and two. The combined in-stock/nonexpired view accepts only four. A stock count and an expired count may overlap; adding those counts does not give unique affected items. Test equality independently: quantity equals minimum is low, while expires equals today is not yet expired under this app\'s stated rule. Invalid dates must never reach the comparison as new saved data. Inspect why localToday uses local getters rather than a UTC string conversion, then identify the visibility refresh and its limit for a continuously visible tab at midnight.'),
('A module owns a commit boundary', '''const seen = new Set();
const tags = ' Utility,utility, Events '.split(',').map(x => x.trim())
  .filter(tag => {
    const key = tag.toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key); return true;
  });
console.log(tags); // ['Utility','Events']
''', 'The Set stores comparison keys, while the returned array keeps display strings. Do not accidentally lowercase every saved tag simply because comparison is case-insensitive. Trace saving a snippet across main.js, store.js and dom.js: the form gathers input, the store owns persistence, and rendering observes the committed result. Force setItem to reject in a disposable test fixture and verify that neither getSnippet nor storage exposes the candidate title. Then examine the clipboard case: existence of writeText is not proof that its promise fulfills. The helper converts denial to false, and the UI displays feedback. Explain why returning false and throwing are different contracts that callers must handle intentionally.'),
('Half-open ranges allow back-to-back reservations', '''const overlaps = (a,b) => a.start < b.end && b.start < a.end;
console.log(overlaps({start:10,end:11},{start:11,end:12})); // false
console.log(overlaps({start:10,end:11.5},{start:11,end:12})); // true
''', 'This reduced predicate explains interval semantics but is not the database safeguard. Two requests can both observe no overlap before either inserts. In the real test, the PostgreSQL exclusion constraint arbitrates and returns one success plus one conflict. Then update the winner to overlap the adjacent booking: the failed statement must preserve the old end time. Separate that invariant from stale-edit protection, which still needs a version policy. Follow a local datetime through the browser conversion into an ISO instant. The edit flow must preserve seconds and milliseconds even when changing only a title. A local day window is bounded by two calendar midnights; at daylight-saving changes it may contain 23 or 25 hours.'),
('A document query should not match an internal field', '''-- Conceptual core of the actual parameterized model query:
SELECT id, title FROM notes
WHERE to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))
   @@ plainto_tsquery('english', 'run');
''', 'Predict Running notes matching run through stemming. Predict a note whose folder alone contains HiddenKeyword not matching that content query. Filtering by folder is still available as a separate exact predicate. A percent sign is ordinary search input, not an instruction to match every row. The real model binds the term through a parameter; the literal above is only a readable SQL example. Next draw the client race: old request starts, new request starts, new completes, old completes. Debouncing alone does not determine which result wins. A request version rejects old state publication, including old error/loading updates. Test this with controlled delayed responses; do not rely on internet timing to reproduce it.'),
('A valid bookmark URL is not automatic fetch permission', '''// Reduced policy examples; these strings are not fetched by this lesson.
const cases = [
  'https://allowed.example/page', // still needs configured host + public DNS
  'https://127.0.0.1/private',    // metadata rejects IP literals
  'http://allowed.example/page', // metadata requires HTTPS
  'javascript:alert(1)',        // bookmark validation rejects this scheme
];
''', 'Follow every boundary before a request: URL shape and credentials, exact configured hostname, port, resolved address set, then a pinned connection lookup. An allowed hostname that resolves partly to private addresses is rejected before transfer. If DNS finishes after the deadline, the abort check prevents a late connection. A redirect response is rejected without following Location, so a redirect toward a private target is never contacted. The transfer also limits headers, bytes, encoding and total time. The controlled test maps only the connection factory to a local HTTP server, preserving production response handling. Finally distinguish preview from save: preview returns text, and the form applies it only if the URL still matches. Creating a bookmark itself never makes the outbound request.')
]
courses=json.loads((B/'courses.json').read_text(encoding='utf-8'))
for n,(title,code,explanation) in enumerate(labs,11):
 folder=B/'stage'/str(n)/'astraupskill';c=courses[n-11]
 lang='sql' if n==19 else 'javascript'
 text=f'''# Trace lab: {title}

[Course index](README.md)

## Work the reduced example first

The following example isolates one idea. The linked project source remains the executable implementation; do not paste this teaching model over it.

```{lang}
{code}```

## Follow the boundary with concrete values

{explanation}

## Connect the model to real code

Open [{c['source']}](../{c['source']}) beside [{c['test']}](../{c['test']}). Identify the caller, the input representation, the decisive guard or transition, and the observable result. Write the value at each step of this actual fixture before executing it:

{c['example']}

If the observation differs from your prediction, find the first changed representation or branch. Do not jump straight to altering the expected assertion. Explain whether the fixture, implementation or your mental model was wrong.

## Independent checkpoint

Change one boundary value and write a new expected-state table. Include an ordinary case and a failure or empty case. Describe which data should remain identical and which visible feedback should change. Finish with a five-minute walkthrough explaining the responsibility of each relevant file and one explicitly unsupported scenario.
'''
 (folder/'07-TRACE-LAB.md').write_text(text,encoding='utf-8')
 p=folder/'README.md';s=p.read_text(encoding='utf-8');s=s.replace('## Your first session','8. [Step-by-step trace lab](07-TRACE-LAB.md)\n\n## Your first session');p.write_text(s,encoding='utf-8')
 # Make every relevant test and existing short orientation discoverable.
 tests=list((folder.parent/'test').glob('*.test.*'))+list((folder.parent/'server/test').glob('*.test.*'))
 p=folder/'04-TESTING-AND-DEBUGGING.md';s=p.read_text(encoding='utf-8');s+='\n## All regression files in this project\n\n'+ '\n'.join(f'- [{t.relative_to(folder.parent).as_posix()}](../{t.relative_to(folder.parent).as_posix()})' for t in tests)+'\n';p.write_text(s,encoding='utf-8')
 if (folder.parent/'CODEBASE_GUIDE.md').exists():
  p=folder/'README.md';s=p.read_text(encoding='utf-8');s+='\n[Existing concise codebase guide](../CODEBASE_GUIDE.md) remains available as a companion orientation.\n';p.write_text(s,encoding='utf-8')
print('Added ten trace labs, full regression navigation and existing-guide links.')
