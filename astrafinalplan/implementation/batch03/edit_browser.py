from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch03');R=B/'stage'
p=R/'21/app.js';s=p.read_text(encoding='utf-8');s=s.replace('draftOptions: ["", ""]','draftOptions: [newOption(), newOption()]').replace('state.draftOptions.push("")','state.draftOptions.push(newOption())').replace('input.value = value;','input.value = value.text;\n    input.setAttribute("aria-label", `Option ${index + 1}`);').replace('state.draftOptions[index] = event.target.value','state.draftOptions[index].text = event.target.value').replace('state.draftOptions = poll.options.map((option) => option.text)','state.draftOptions = poll.options.map(({ id, text }) => ({ id, text }))').replace('state.draftOptions = ["", ""]','state.draftOptions = [newOption(), newOption()]')
a=s.index('function savePolls()');b=s.index('function renderOptionRows()',a)
s=s[:a]+'''function newOption() { return { id: crypto.randomUUID(), text: "" }; }

function commitPolls(candidate) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(candidate)); }
  catch { showMessage("Could not save. Your current poll and draft are unchanged."); return false; }
  state.polls = candidate;
  return true;
}

'''+s[b:]
a=s.index('function handleSubmit(');b=s.index('function resetForm()',a)
s=s[:a]+'''function handleSubmit(event) {
  event.preventDefault();
  const question = questionInput.value.trim();
  const draft = state.draftOptions.map(option => ({ ...option, text: option.text.trim() }));
  if (!question || question.length > 160) return showMessage("Add a question of at most 160 characters.");
  if (draft.length < MIN_OPTIONS || draft.length > MAX_OPTIONS || draft.some(x => !x.text || x.text.length > 80))
    return showMessage("Fill every option, or remove its row. Use 2 to 6 options of at most 80 characters.");
  if (new Set(draft.map(x => x.text.toLowerCase())).size !== draft.length)
    return showMessage("Each option must have different text (ignoring letter case).");
  const existing = state.polls.find(poll => poll.id === state.editingId);
  if (state.editingId && !existing) return showMessage("This poll no longer exists.");
  const options = draft.map(option => ({ ...option, votes: existing?.options.find(x => x.id === option.id)?.votes ?? 0 }));
  const poll = { id: existing?.id ?? crypto.randomUUID(), question, options };
  const candidate = existing ? state.polls.map(x => x.id === poll.id ? poll : x) : [poll, ...state.polls];
  if (!commitPolls(candidate)) return;
  showMessage(existing ? "Poll updated." : "Poll created."); resetForm(); render();
}

function vote(pollId, optionId) {
  const candidate = state.polls.map(poll => poll.id !== pollId ? poll : {
    ...poll, options: poll.options.map(option => option.id === optionId ? { ...option, votes: option.votes + 1 } : option)
  });
  if (commitPolls(candidate)) render();
}

function resetVotes(pollId) {
  const candidate = state.polls.map(poll => poll.id !== pollId ? poll : {
    ...poll, options: poll.options.map(option => ({ ...option, votes: 0 }))
  });
  if (commitPolls(candidate)) render();
}

function editPoll(id) {
  const poll = state.polls.find(item => item.id === id); if (!poll) return;
  state.editingId = id; idInput.value = id; questionInput.value = poll.question;
  state.draftOptions = poll.options.map(({ id, text }) => ({ id, text }));
  renderOptionRows(); submitButton.textContent = "Update poll"; cancelButton.hidden = false; questionInput.focus();
}

function deletePoll(id) {
  if (!commitPolls(state.polls.filter(poll => poll.id !== id))) return;
  if (state.editingId === id) resetForm(); showMessage("Poll deleted."); render();
}

'''+s[b:];p.write_text(s,encoding='utf-8')
p=R/'22/app.js';s=p.read_text(encoding='utf-8')
a=s.index('function moveCard(');b=s.index('function render()',a)
s=s[:a]+'''function moveCard(columnId, beforeId, cardId = state.draggingId) {
  const current = state.cards.find(card => card.id === cardId);
  if (!current || !COLUMNS.some(column => column.id === columnId)) return false;
  if (beforeId === cardId) return true;
  if (beforeId && !state.cards.some(card => card.id === beforeId && card.column === columnId)) return false;
  const candidate = state.cards.map(card => ({ ...card }));
  const moved = candidate.find(card => card.id === cardId);
  moved.column = columnId;
  for (const column of COLUMNS) {
    const ordered = candidate.filter(card => card.column === column.id && card.id !== cardId)
      .sort((a,b) => a.order - b.order || a.id.localeCompare(b.id));
    if (column.id === columnId) ordered.splice(beforeId ? ordered.findIndex(card => card.id === beforeId) : ordered.length, 0, moved);
    ordered.forEach((card,index) => { card.order = index; });
  }
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(candidate)); }
  catch { showMessage("Could not save the move. The board is unchanged."); return false; }
  state.cards = candidate; render(); showMessage("Card moved."); return true;
}

function moveByKeyboard(card, direction) {
  const ordered = cardsIn(card.column), index = ordered.findIndex(x => x.id === card.id);
  const before = direction < 0 ? ordered[index - 1]?.id : ordered[index + 2]?.id ?? null;
  if (direction < 0 && index === 0 || direction > 0 && index === ordered.length - 1) return;
  if (moveCard(card.column, before, card.id)) document.querySelector(`[data-id="${card.id}"] .move-column`)?.focus();
}

'''+s[b:]
s=s.replace('  el.append(title, actions);','''  const move = document.createElement("select");
  move.className = "move-column"; move.setAttribute("aria-label", `Move ${card.title} to column`);
  for (const column of COLUMNS) move.add(new Option(column.title, column.id));
  move.value = card.column;
  move.addEventListener("change", () => {
    moveCard(move.value, null, card.id);
    document.querySelector(`[data-id="${card.id}"] .move-column`)?.focus();
  });
  actions.append(iconButton("Move up", () => moveByKeyboard(card,-1)), iconButton("Move down", () => moveByKeyboard(card,1)));
  el.append(title, move, actions);''');p.write_text(s,encoding='utf-8')
for n in [21,22]:
 p=R/str(n)/'package.json';p.write_text(json.dumps({'name':f'astra-{n}-browser-tests','private':True,'scripts':{'test':'node --test test/*.test.cjs'},'devDependencies':{'jsdom':'^25.0.1'}},indent=2)+'\n',encoding='utf-8')
print('Implemented poll option identity and keyboard-safe kanban movement.')
