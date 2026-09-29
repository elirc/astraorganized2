from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch02/stage')
def edit(n,file,old,new):
 p=B/str(n)/file;s=p.read_text(encoding='utf-8');assert old in s,(n,file,old[:80]);p.write_text(s.replace(old,new),encoding='utf-8')
def add(n,file,text):
 p=B/str(n)/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
# Flashcards: bounded session state with explicit completion and a filtered snapshot.
edit(11,'app.js','  flipped: false\n','  flipped: false,\n  unlearnedOnly: false,\n  studyError: ""\n')
edit(11,'app.js','  state.deck = event.target.value;\n  render();','  state.deck = event.target.value;\n  if (state.mode === "study") startStudy(false);\n  else render();')
edit(11,'app.js','form.addEventListener("submit", handleSubmit);','document.querySelector("#unlearned-only").addEventListener("change", (event) => {\n  state.unlearnedOnly = event.target.checked;\n  if (state.mode === "study") startStudy(false);\n});\n\nform.addEventListener("submit", handleSubmit);')
edit(11,'app.js','function startStudy(shuffle) {\n  const cards = visibleCards();','function startStudy(shuffle) {\n  const cards = visibleCards().filter((card) => !state.unlearnedOnly || !card.known);\n  state.studyError = "";')
start=(B/'11/app.js').read_text();a=start.index('function grade(known) {');b=start.index('\nfunction renderStudy()',a)
edit(11,'app.js',start[a:b],'''function grade(known) {
  const card = currentStudyCard();
  if (!card || !state.flipped) return;
  const next = state.cards.map((item) => item.id === card.id ? { ...item, known } : item);
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    state.studyError = "Could not save your grade. Try again; this card has not advanced.";
    renderStudy();
    return;
  }
  state.cards = next;
  state.studyError = "";
  state.studyIndex += 1;
  state.flipped = false;
  renderStudy();
}
''')
edit(11,'app.js','  againButton.disabled = controlsDisabled;\n  knownButton.disabled = controlsDisabled;','  againButton.disabled = controlsDisabled || !state.flipped;\n  knownButton.disabled = controlsDisabled || !state.flipped;')
edit(11,'app.js','    studyProgress.textContent = "Card 0 of 0";\n    flashcardText.textContent = "No cards in this deck. Add some in Manage.";','    studyProgress.textContent = total ? `Completed ${total} of ${total}` : "Card 0 of 0";\n    flashcardText.textContent = total ? "Session complete. Start again with Shuffle & restart." : "No matching cards. Change the deck or unlearned filter, or add cards in Manage.";')
edit(11,'app.js','    studySummary.textContent = "";','    studySummary.textContent = total ? `${state.studyOrder.filter((id) => state.cards.find((item) => item.id === id)?.known).length}/${total} marked "got it"` : "";')
edit(11,'app.js','  studySummary.textContent = `${knownCount}/${total} marked "got it"`;','  studySummary.textContent = state.studyError || `${knownCount}/${total} marked "got it"`;')
p=B/'11/index.html';s=p.read_text();s,count=re.subn(r'(<select id="deck-filter"[\s\S]*?</select>)',r'\1\n          <label><input type="checkbox" id="unlearned-only"> Study unlearned cards only</label>',s);assert count==1;p.write_text(s,encoding='utf-8')
# Habits: calendar-day streaks, including best historical run.
edit(12,'app.js','    header.append(title, streak);','    const best = document.createElement("span");\n    best.className = "streak-badge best-streak";\n    best.textContent = `Best: ${bestStreak(habit)} days`;\n    header.append(title, streak, best);')
edit(12,'app.js','      cell.setAttribute("aria-pressed", String(done));','      cell.setAttribute("aria-pressed", String(done));\n      cell.setAttribute("aria-label", `${habit.name}: ${iso}`);')
edit(12,'app.js','  const cursor = startOfToday();\n  while','  const cursor = startOfToday();\n  // Today is still in progress; yesterday may anchor an active streak.\n  if (!habit.history[isoDate(cursor)]) cursor.setDate(cursor.getDate() - 1);\n  while')
edit(12,'app.js','function button(label, variant, onClick) {','''function bestStreak(habit, today = isoDate(startOfToday())) {
  const days = Object.entries(habit.history).filter(([date, checked]) => {
    if (checked !== true || !/^\\d{4}-\\d{2}-\\d{2}$/.test(date) || date > today) return false;
    const parsed = new Date(`${date}T00:00:00Z`);
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === date;
  }).map(([date]) => Date.parse(`${date}T00:00:00Z`) / 86400000).sort((a, b) => a - b);
  let best = 0, run = 0, previous;
  for (const day of days) {
    run = previous !== undefined && day === previous + 1 ? run + 1 : 1;
    best = Math.max(best, run);
    previous = day;
  }
  return best;
}

function button(label, variant, onClick) {''')
# Reading list: compose filters and deterministic ordering without mutating source.
edit(13,'app.js','let sortMode = "title";','let sortMode = "title";\nlet statusFilter = "All";')
edit(13,'app.js','form.addEventListener("submit", saveBook);','document.querySelector("#status-filter").addEventListener("change", (event) => {\n  statusFilter = event.target.value;\n  renderBooks();\n});\n\nform.addEventListener("submit", saveBook);')
edit(13,'app.js','      return searchable.includes(searchTerm);','      return (statusFilter === "All" || book.status === statusFilter) && searchable.includes(searchTerm);')
edit(13,'app.js','        return Number(b.rating) - Number(a.rating);','        return Number(b.rating) - Number(a.rating) || a.title.localeCompare(b.title) || a.id.localeCompare(b.id);')
edit(13,'app.js','      return a[sortMode].localeCompare(b[sortMode]);','      return a[sortMode].localeCompare(b[sortMode]) || a.id.localeCompare(b.id);')
edit(13,'app.js','  booksList.innerHTML = "";','  document.querySelector("#reading-summary").textContent = `Showing ${visibleBooks.length} of ${books.length} books. ${books.filter((book) => book.status === "Finished").length} finished overall.`;\n  booksList.innerHTML = "";')
p=B/'13/index.html';s=p.read_text();s,count=re.subn(r'(<select id="sort"[\s\S]*?</select>)',r'\1\n        <label for="status-filter">Reading status</label>\n        <select id="status-filter"><option value="All">All statuses</option><option>Want to Read</option><option>Reading</option><option>Finished</option></select>\n        <p id="reading-summary" role="status"></p>',s);assert count==1;p.write_text(s,encoding='utf-8')
# Budget: validate money text and sum integer cents; write before publication.
edit(15,'app.js','    amount: Number(amountInput.value),','    amount: parseCents(amountInput.value) / 100,')
edit(15,'app.js','  if (!transaction.description || !transaction.category || !transaction.date || transaction.amount <= 0) {','  if (!transaction.description || !transaction.category || !isRealDate(transaction.date) || !Number.isFinite(transaction.amount) || !["income", "expense"].includes(transaction.type)) {')
edit(15,'app.js','setMessage("Add a valid description, category, amount, and date.");','setMessage("Use a description, category, real date, and a positive amount with at most two decimal places (maximum 999999999.99).");')
s=(B/'15/app.js').read_text();a=s.index('  if (editingId) {');b=s.index('  resetForm();',a)
edit(15,'app.js',s[a:b],'''  const next = editingId
    ? transactions.map((current) => current.id === editingId ? { ...transaction, id: editingId } : current)
    : [transaction, ...transactions];
  if (!commitTransactions(next)) return;
  setMessage(editingId ? "Transaction updated." : "Transaction added.");
''')
edit(15,'app.js','  transactions = transactions.filter((transaction) => transaction.id !== id);\n  persistTransactions();','  if (!commitTransactions(transactions.filter((transaction) => transaction.id !== id))) return;')
edit(15,'app.js','    summary[transaction.type] += transaction.amount;','    summary[transaction.type] += Math.round(transaction.amount * 100);')
edit(15,'app.js','formatCurrency(totals.income);','formatCurrency(totals.income / 100);')
edit(15,'app.js','formatCurrency(totals.expense);','formatCurrency(totals.expense / 100);')
edit(15,'app.js','formatCurrency(totals.income - totals.expense);','formatCurrency((totals.income - totals.expense) / 100);')
edit(15,'app.js','function formatCurrency(value) {','''function parseCents(text) {
  if (!/^(?:0|[1-9]\\d*)(?:\\.\\d{1,2})?$/.test(text)) return NaN;
  const [whole, fraction = ""] = text.split(".");
  const cents = Number(whole) * 100 + Number(fraction.padEnd(2, "0"));
  return Number.isSafeInteger(cents) && cents > 0 && cents <= 99999999999 ? cents : NaN;
}

function isRealDate(value) {
  const parsed = new Date(`${value}T00:00:00Z`);
  return /^\\d{4}-\\d{2}-\\d{2}$/.test(value) && Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}

function commitTransactions(next) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); }
  catch { setMessage("Could not save. Your transactions are unchanged; try again."); return false; }
  transactions = next;
  return true;
}

function formatCurrency(value) {''')
# Pantry: expiration and stock are distinct, inclusive threshold maintained.
edit(16,'app.js','  if (!item.name || !item.expires || item.quantity < 0 || item.minimum < 0) {','  if (!item.name || !isRealDate(item.expires) || !Number.isFinite(item.quantity) || !Number.isFinite(item.minimum) || quantityInput.value === "" || minimumInput.value === "" || item.quantity < 0 || item.minimum < 0) {')
edit(16,'app.js','(activeFilter === "Fresh" && !isLow)','(activeFilter === "Fresh" && !isLow && !isExpired(item)) || (activeFilter === "Expired" && isExpired(item))')
edit(16,'app.js','    const statusText = item.quantity <= item.minimum ? "Low" : "Fresh";','    const low = item.quantity <= item.minimum;\n    const expired = isExpired(item);\n    const statusText = [low ? "Low stock" : "Stock OK", ...(expired ? ["Expired"] : [])].join(" · ");')
edit(16,'app.js','    status.classList.toggle("low", statusText === "Low");','    status.classList.toggle("low", low || expired);')
edit(16,'app.js','function formatDate(dateValue) {','''function localToday() {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

function isExpired(item, today = localToday()) { return item.expires < today; }

function isRealDate(value) {
  const date = new Date(`${value}T00:00:00Z`);
  return /^\\d{4}-\\d{2}-\\d{2}$/.test(value) && Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

document.addEventListener("visibilitychange", () => { if (!document.hidden) renderItems(); });

function formatDate(dateValue) {''')
p=B/'16/index.html';s=p.read_text();s=s.replace('<option value="Fresh">Fresh</option>','<option value="Fresh">In stock &amp; not expired</option>');s=s.replace('</select>\n      </div>', '</select>\n      </div>')
s,count=re.subn(r'(<select id="filter"[\s\S]*?)(</select>)',r'\1<option value="Expired">Expired</option>\2',s);assert count==1;p.write_text(s,encoding='utf-8')
# Snippet store: atomic failure semantics; deduplicated tags; rejected clipboard promise handled.
p=B/'17/src/store.js';s=p.read_text();s=s.replace('function persist() {\n  localStorage.setItem(STORAGE_KEY, JSON.stringify(snippets));\n}', 'function commit(next) {\n  localStorage.setItem(STORAGE_KEY, JSON.stringify(next));\n  snippets = next;\n}')
a=s.index('function parseTags(raw) {');b=s.index('\nexport function getSnippet',a)
s=s[:a]+'''function parseTags(raw) {
  const seen = new Set();
  return raw.split(",").map((tag) => tag.trim()).filter((tag) => {
    const key = tag.toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
'''+s[b:]
s=s.replace('  if (input.id) {\n    snippets = snippets.map((snippet) =>\n      snippet.id === input.id ? { ...snippet, ...base } : snippet\n    );\n  } else {\n    snippets.unshift({ id: crypto.randomUUID(), createdAt: new Date().toISOString(), ...base });\n  }\n  persist();','''  if (!base.title || !base.code.trim()) throw new Error("Add a title and some code.");
  if (input.id && !snippets.some((item) => item.id === input.id)) throw new Error("This snippet no longer exists.");
  const next = input.id
    ? snippets.map((snippet) => snippet.id === input.id ? { ...snippet, ...base } : snippet)
    : [{ id: crypto.randomUUID(), createdAt: new Date().toISOString(), ...base }, ...snippets];
  commit(next);''')
s=s.replace('  snippets = snippets.filter((snippet) => snippet.id !== id);\n  persist();','  commit(snippets.filter((snippet) => snippet.id !== id));');p.write_text(s,encoding='utf-8')
edit(17,'src/main.js','  saveSnippet({','  try { saveSnippet({')
edit(17,'src/main.js','    code: codeInput.value\n  });','    code: codeInput.value\n  }); } catch { showMessage("Could not save this snippet. Your saved data and form are unchanged."); return; }')
edit(17,'src/main.js','  deleteSnippet(id);','  try { deleteSnippet(id); } catch { showMessage("Could not delete this snippet. Try again."); return; }')
edit(17,'src/dom.js','    await navigator.clipboard.writeText(text);\n    return true;','    try {\n      await navigator.clipboard.writeText(text);\n      return true;\n    } catch { return false; }')
for n in [11,12,13,15,16]:
 add(n,'package.json',json.dumps({'name':f'astra-browser-exercise-{n}','private':True,'scripts':{'test':'node --test test/*.test.cjs'},'devDependencies':{'jsdom':'^25.0.1'}},indent=2)+'\n')
add(17,'package.json',json.dumps({'name':'astra-snippet-vault','private':True,'type':'module','scripts':{'test':'node --test test/*.test.js'}},indent=2)+'\n')
print('Implemented six browser project improvements in isolated stages.')
