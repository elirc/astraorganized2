from pathlib import Path

BASE = Path(__file__).resolve().parent / 'stage'
def read(n,f): return (BASE/n/f).read_text(encoding='utf-8')
def write(n,f,s):
    p=BASE/n/f; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def replace(n,f,a,b):
    s=read(n,f)
    assert a in s,(n,f,a[:70])
    write(n,f,s.replace(a,b))

# Keep deletion and its recovery record in one atomic localStorage value.
replace('01','app.js','const state = {\n  tasks: loadTasks(),','const savedBoard = loadBoard();\nconst state = {\n  tasks: savedBoard.tasks,\n  deleted: savedBoard.deleted,')
replace('01','app.js','function loadTasks() {\n  const saved = localStorage.getItem(STORAGE_KEY);\n  return saved ? JSON.parse(saved) : starterTasks;\n}', '''function loadBoard() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return { tasks: starterTasks, deleted: null };
  const parsed = JSON.parse(saved);
  // Existing installations stored only an array. Upgrade without discarding it.
  if (Array.isArray(parsed)) return { tasks: parsed, deleted: null };
  return { tasks: parsed.tasks, deleted: parsed.deleted ?? null };
}''')
replace('01','app.js','JSON.stringify(state.tasks)','JSON.stringify({ version: 2, tasks: state.tasks, deleted: state.deleted })')
replace('01','app.js','function deleteTask(id) {\n  state.tasks = state.tasks.filter((task) => task.id !== id);\n  saveTasks();\n  resetForm();\n  showMessage("Task deleted.");\n  render();\n}', '''function commitBoard(tasks, deleted) {
  try {
    // Persist first. A quota/security error must not consume an undo or hide a task.
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 2, tasks, deleted }));
  } catch {
    showMessage("Could not save this change. Your task and undo history are unchanged.");
    return false;
  }
  state.tasks = tasks;
  state.deleted = deleted;
  return true;
}

function deleteTask(id) {
  const index = state.tasks.findIndex((task) => task.id === id);
  if (index < 0) return;
  const deleted = { task: state.tasks[index], index };
  if (!commitBoard(state.tasks.filter((task) => task.id !== id), deleted)) return;
  resetForm();
  showMessage("Task deleted. You can undo the most recent deletion, even after reload.");
  render();
}

function undoDelete() {
  if (!state.deleted) return;
  const { task, index } = state.deleted;
  if (state.tasks.some((item) => item.id === task.id)) {
    showMessage("That task already exists; undo would create a duplicate.");
    return;
  }
  const tasks = [...state.tasks];
  tasks.splice(Math.min(index, tasks.length), 0, task);
  if (!commitBoard(tasks, null)) return;
  // Reveal the restored task even if an old filter would hide it.
  state.query = ""; state.status = "All";
  searchInput.value = ""; statusFilter.value = "All";
  showMessage("Task restored.");
  render();
}''')
replace('01','app.js','const emptyState = document.querySelector("#empty-state");','const emptyState = document.querySelector("#empty-state");\nconst undoButton = document.querySelector("#undo-delete");\nundoButton.addEventListener("click", undoDelete);')
replace('01','app.js','function render() {','function render() {\n  undoButton.disabled = !state.deleted;')
replace('01','index.html','<div class="toolbar">','<button type="button" id="undo-delete" class="secondary" disabled>Undo last deletion</button>\n      <div class="toolbar">')

# Duplicate matching is a product policy: trim and compare case-insensitively,
# preserving the stored display spelling and excluding the record being edited.
replace('02','app.js','  if (editingId) {\n    contacts = contacts.map', '''  const duplicate = contacts.find((item) =>
    item.id !== editingId && item.email.trim().toLowerCase() === contact.email.toLowerCase()
  );
  if (duplicate) {
    setMessage(`A contact with this email already exists: ${duplicate.name}.`);
    emailInput.setAttribute("aria-invalid", "true");
    emailInput.focus();
    return;
  }
  emailInput.removeAttribute("aria-invalid");

  if (editingId) {
    contacts = contacts.map''')
replace('02','app.js','function resetForm() {','function resetForm() {\n  emailInput.removeAttribute("aria-invalid");')
replace('02','index.html','id="email" type="email"','id="email" aria-describedby="message" type="email"')
replace('02','app.js','renderContacts();\n\nfunction loadContacts()', 'emailInput.addEventListener("input", () => emailInput.removeAttribute("aria-invalid"));\nrenderContacts();\n\nfunction loadContacts()')

# The interval wakes the UI; the deadline, not callback count, is the clock.
replace('03','app.js','  intervalId: null','  deadline: null,\n  duration: 25 * 60,\n  intervalId: null')
replace('03','app.js','function startTimer() {\n  if (timer.mode === "idle") {\n    timer.remaining = configuredSeconds();\n  }', '''function startTimer() {
  if (timer.mode === "running") return;
  clearInterval(timer.intervalId);
  if (timer.mode === "idle") {
    timer.remaining = configuredSeconds();
    timer.duration = timer.remaining;
  }
  timer.deadline = Date.now() + timer.remaining * 1000;''')
replace('03','app.js','function pauseTimer() {\n  clearInterval(timer.intervalId);', '''function pauseTimer() {
  if (timer.mode !== "running") return;
  timer.remaining = Math.max(0, (timer.deadline - Date.now()) / 1000);
  if (timer.remaining === 0) { completeSession(); return; }
  timer.deadline = null;
  clearInterval(timer.intervalId);''')
replace('03','app.js','function resetTimer() {','function resetTimer() {\n  timer.deadline = null;')
replace('03','app.js','  timer.remaining -= 1;','  if (timer.mode !== "running") return;\n  timer.remaining = Math.max(0, (timer.deadline - Date.now()) / 1000);')
replace('03','app.js','function completeSession() {','function completeSession() {\n  if (timer.mode !== "running") return;\n  timer.mode = "idle";\n  timer.deadline = null;')
replace('03','app.js','Math.round(configuredSeconds() / 60)','Math.round(timer.duration / 60)')
replace('03','app.js','formatClock(timer.remaining)','formatClock(Math.ceil(timer.remaining))')
replace('03','app.js','renderTimer();\nrenderSessions();','document.addEventListener("visibilitychange", () => {\n  if (!document.hidden) tick();\n});\nrenderTimer();\nrenderSessions();')

# Reuse the existing modal for editing, with explicit validation and persistence
# before publishing a replacement state.
replace('04','app.js','let charts = {};','let charts = {};\nlet editingExpenseId = null;')
replace('04','app.js','  els.openAddModal.addEventListener("click", () => {\n    updateCategoryOptions();','  els.openAddModal.addEventListener("click", () => {\n    editingExpenseId = null;\n    els.entryType.disabled = false;\n    document.querySelector("#entryModal h3").textContent = "Add money movement";\n    document.querySelector("#entryError").textContent = "";\n    updateCategoryOptions();')
replace('04','app.js','  if (!entry.amount || entry.amount < 0) return;', '''  const error = validateEntry(entry);
  const errorNode = document.querySelector("#entryError");
  if (error) { errorNode.textContent = error; return; }
  errorNode.textContent = "";
  if (editingExpenseId) {
    const existing = state.expenses.find((item) => item.id === editingExpenseId);
    if (!existing) { errorNode.textContent = "This expense no longer exists."; return; }
    const updated = { ...existing, ...entry, id: existing.id, category: els.entryCategory.value };
    const next = { ...state, expenses: state.expenses.map((item) => item.id === existing.id ? updated : item) };
    try { localStorage.setItem(storageKey, JSON.stringify(next)); }
    catch { errorNode.textContent = "Could not save. The original expense is unchanged."; return; }
    state = next;
    editingExpenseId = null;
    els.entryType.disabled = false;
    els.entryForm.reset();
    els.entryModal.close();
    render();
    return;
  }''')
write('04','app.js',read('04','app.js')+'''
function validateEntry(entry) {
  if (!Number.isFinite(entry.amount) || entry.amount <= 0 || entry.amount > 999999999.99)
    return "Enter an amount greater than zero and no more than 999,999,999.99.";
  if (Math.abs(entry.amount * 100 - Math.round(entry.amount * 100)) > 0.00001)
    return "Use no more than two decimal places.";
  if (!entry.description) return "Enter a description.";
  if (!/^\\d{4}-\\d{2}-\\d{2}$/.test(entry.date)) return "Enter a valid date.";
  const date = new Date(`${entry.date}T00:00:00Z`);
  if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== entry.date)
    return "Enter a real calendar date.";
  return "";
}

function editExpense(id) {
  const expense = state.expenses.find((item) => item.id === id);
  if (!expense) return;
  editingExpenseId = id;
  els.entryType.value = "expense";
  els.entryType.disabled = true;
  updateCategoryOptions();
  els.entryOwner.value = expense.owner;
  els.entryDate.value = expense.date;
  els.entryAmount.value = expense.amount;
  els.entryCategory.value = expense.category;
  els.entryDescription.value = expense.description;
  document.querySelector("#entryModal h3").textContent = "Edit expense";
  document.querySelector("#entryError").textContent = "";
  els.entryModal.showModal();
  els.entryDescription.focus();
}
''')
replace('04','app.js','  els.expenseRows.querySelectorAll("[data-delete-expense]")', '''  els.expenseRows.querySelectorAll("[data-edit-expense]").forEach((button) => {
    button.addEventListener("click", () => editExpense(button.dataset.editExpense));
  });
  els.expenseRows.querySelectorAll("[data-delete-expense]")''')
# Insert before the existing delete control without guessing its surrounding CSS.
s=read('04','app.js'); marker='data-delete-expense="${expense.id}"'
idx=s.index(marker); start=s.rfind('<button',0,idx)
s=s[:start]+'<button type="button" class="icon-button" data-edit-expense="${expense.id}" aria-label="Edit ${escapeHtml(expense.description)}">Edit</button>\n            '+s[start:]
write('04','app.js',s)
replace('04','index.html','<div class="modal-actions">','<p id="entryError" role="alert"></p>\n        <div class="modal-actions">')
print('Prepared behavior changes for projects 01–04')
