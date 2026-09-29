from pathlib import Path
s=Path('astra-remaining-improvements/stage/6844a7b03c83')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('store.js',r'''
import { defaultData } from './data.js';
export const STORAGE_KEY = 'customJeopardy';
const MAX_BYTES = 2 * 1024 * 1024;
function object(value, keys, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !keys.includes(key))) throw new Error(`Invalid ${label} fields.`);
}
function text(value, max, label) { if (typeof value !== 'string' || !value.trim() || value.length > max) throw new Error(`${label} must contain 1-${max} characters.`); return value.trim(); }
function identity(value) { if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,80}$/.test(value)) throw new Error('Invalid record identity.'); return value; }
export function validateState(value) {
  object(value, ['schemaVersion','revision','categories','usedQuestionIds'], 'board');
  if (value.schemaVersion !== 1 || !Number.isSafeInteger(value.revision) || value.revision < 0) throw new Error('Unsupported board version or revision.');
  if (!Array.isArray(value.categories) || value.categories.length > 10) throw new Error('Use at most 10 categories.');
  const ids = new Set(); const questionIds = new Set();
  const claim = id => { identity(id); if (ids.has(id)) throw new Error('Duplicate record identity.'); ids.add(id); return id; };
  const categories = value.categories.map(category => {
    object(category, ['id','name','questions'], 'category'); const id = claim(category.id);
    if (!Array.isArray(category.questions) || category.questions.length > 20) throw new Error('Use at most 20 questions per category.');
    const questions = category.questions.map(question => {
      object(question, ['id','prompt','answer','points'], 'question'); const questionId = claim(question.id); questionIds.add(questionId);
      if (!Number.isInteger(question.points) || question.points < 100 || question.points > 10000 || question.points % 100) throw new Error('Points must be a multiple of 100 from 100 to 10000.');
      return { id: questionId, prompt: text(question.prompt, 1000, 'Prompt'), answer: text(question.answer, 1000, 'Answer'), points: question.points };
    });
    return { id, name: text(category.name, 80, 'Category name'), questions };
  });
  if (!Array.isArray(value.usedQuestionIds) || new Set(value.usedQuestionIds).size !== value.usedQuestionIds.length || value.usedQuestionIds.some(id => !questionIds.has(id))) throw new Error('Used clues must refer to unique existing questions.');
  return { schemaVersion: 1, revision: value.revision, categories, usedQuestionIds: [...value.usedQuestionIds] };
}
export function migrateLegacy(data) {
  if (!Array.isArray(data)) throw new Error('Legacy board must be an array.');
  return validateState({ schemaVersion: 1, revision: 0, categories: data.map((category, index) => {
    object(category, ['category','questions'], 'legacy category');
    if (!Array.isArray(category.questions)) throw new Error('Invalid legacy questions.');
    return { id: `category-${index+1}`, name: category.category, questions: category.questions.map((question, number) => {
      object(question, ['q','a'], 'legacy question'); return { id: `question-${index+1}-${number+1}`, prompt: question.q, answer: question.a, points: (number+1)*100 };
    }) };
  }), usedQuestionIds: [] });
}
export const freshState = () => migrateLegacy(defaultData);
export function parseState(raw) {
  if (raw === null) return freshState();
  if (typeof raw !== 'string' || new TextEncoder().encode(raw).length > MAX_BYTES) throw new Error('Saved board exceeds the 2 MiB limit.');
  let value; try { value = JSON.parse(raw); } catch { throw new Error('Saved board is not valid JSON. Export it before choosing a replacement.'); }
  return Array.isArray(value) ? migrateLegacy(value) : validateState(value);
}
export class BoardStore {
  constructor(storage, locks) { this.storage = storage; this.locks = locks; }
  load() { let raw; try { raw = this.storage.getItem(STORAGE_KEY); } catch { throw new Error('Browser storage is unavailable. No saved data was changed.'); } return { raw, state: parseState(raw) }; }
  async save(candidate, expectedRaw, { replaceInvalid = false } = {}) {
    const normalized = validateState(candidate);
    if (!this.locks?.request) throw new Error('Saving needs Web Locks. Open the local server in a supported browser.');
    return this.locks.request(`quiz-board:${STORAGE_KEY}`, async () => {
      let current; try { current = this.storage.getItem(STORAGE_KEY); } catch { throw new Error('Browser storage is unavailable.'); }
      if (current !== expectedRaw) throw new Error('This board changed in another tab. Reload before saving; your draft is preserved.');
      let revision = 0;
      try { revision = parseState(current).revision; } catch (error) { if (!replaceInvalid) throw error; }
      if (revision >= Number.MAX_SAFE_INTEGER) throw new Error('Revision limit reached; export and review the board.');
      const state = { ...normalized, revision: revision + 1 }; const raw = JSON.stringify(state);
      if (new TextEncoder().encode(raw).length > MAX_BYTES) throw new Error('Board exceeds the 2 MiB limit.');
      try { this.storage.setItem(STORAGE_KEY, raw); } catch { throw new Error('Save failed: browser storage is full or unavailable. Your draft is preserved.'); }
      return { raw, state };
    });
  }
}
export function removeCategory(state, id) { const candidate = structuredClone(state); candidate.categories = candidate.categories.filter(c => c.id !== id); const retained = new Set(candidate.categories.flatMap(c => c.questions.map(q => q.id))); candidate.usedQuestionIds = candidate.usedQuestionIds.filter(id => retained.has(id)); return candidate; }
export function removeQuestion(state, categoryId, id) { const candidate = structuredClone(state); const category = candidate.categories.find(c => c.id === categoryId); if (!category) throw new Error('Category not found.'); category.questions = category.questions.filter(q => q.id !== id); candidate.usedQuestionIds = candidate.usedQuestionIds.filter(value => value !== id); return candidate; }
''')
w('server.js',r'''
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = dirname(fileURLToPath(import.meta.url));
const allowed = new Set(['index.html','styles.css','main.js','board.js','edit.js','data.js','store.js']);
const mime = { html: 'text/html', css: 'text/css', js: 'text/javascript' };
const port = Number(process.env.PORT || 4173);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('Invalid PORT.');
const server = createServer(async (request, response) => {
  const pathname = new URL(request.url, 'http://localhost').pathname; const name = pathname === '/' ? 'index.html' : pathname.slice(1);
  if (!['GET','HEAD'].includes(request.method) || !allowed.has(name)) { response.writeHead(404); response.end('Not found'); return; }
  try { const body = await readFile(join(root,name)); response.writeHead(200, { 'Content-Type': `${mime[name.split('.').pop()]}; charset=utf-8`, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'" }); response.end(request.method === 'HEAD' ? undefined : body); }
  catch { response.writeHead(500); response.end('Asset could not be read'); }
});
server.listen(port,'127.0.0.1',()=>console.log(`Quiz board: http://127.0.0.1:${server.address().port}`));
for(const signal of ['SIGINT','SIGTERM']) process.once(signal,()=>server.close());
''')
w('index.html',r'''
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Quiz board studio</title><link rel="stylesheet" href="styles.css"><script type="module" src="main.js"></script></head>
<body><main><header><p class="eyebrow">LOCAL LEARNING LAB</p><h1>Quiz board studio</h1><p>Build a question bank. Play a round. Keep your work in this browser.</p></header>
<div class="toolbar"><button id="edit-btn">Edit question bank</button><button id="reset-round">New round</button><button id="export-btn">Export board</button><label class="file-button">Import board<input id="import-file" type="file" accept="application/json,.json"></label><button id="reload-btn">Reload saved board</button></div>
<p id="status" role="status" aria-live="polite"></p><div id="error-panel" hidden><p id="error" role="alert"></p><button id="export-raw">Export saved text</button><button id="replace-btn">Replace with example board</button></div>
<p id="progress"></p><div id="board" class="board" aria-label="Question board"></div><p class="footnote">Local storage is shared only by tabs on this exact origin. Export a copy before moving browsers or clearing site data.</p>
</main>
<dialog id="answer-modal" aria-labelledby="clue-title"><h2 id="clue-title">Clue</h2><p id="clue-text"></p><p id="answer-text" hidden></p><div class="actions"><button id="reveal-answer">Reveal answer</button><button id="mark-used">Mark clue used</button><button id="close-answer">Close clue</button></div></dialog>
<dialog id="editor-modal" aria-labelledby="editor-title"><h2 id="editor-title">Edit question bank</h2><p>Changes stay in this draft until Save bank succeeds. Deleting a category removes its questions.</p><p id="editor-error" role="alert"></p><form id="editor-form"><div id="editor-container"></div><div class="actions sticky"><button type="button" id="add-category">Add category</button><button type="submit" id="save-questions">Save bank</button><button type="button" id="close-editor">Cancel editing</button></div></form></dialog>
</body></html>
''')
w('board.js',r'''
export function renderBoard(state, onClue) {
  const board = document.getElementById('board'); board.replaceChildren();
  if (!state.categories.length) { const empty = document.createElement('p'); empty.textContent = 'Your bank is empty. Add a category in the editor.'; board.append(empty); }
  for (const category of state.categories) {
    const column = document.createElement('section'); column.className = 'category';
    const heading = document.createElement('h2'); heading.textContent = category.name; column.append(heading);
    for (const question of category.questions) {
      const tile = document.createElement('button'); tile.className = 'tile'; tile.dataset.questionId = question.id;
      const used = state.usedQuestionIds.includes(question.id); tile.textContent = used ? 'Used' : String(question.points); tile.disabled = used;
      tile.setAttribute('aria-label', `${category.name}: ${question.points} points${used ? ', used' : ''}`); tile.addEventListener('click', () => onClue(question, category.name)); column.append(tile);
    }
    if (!category.questions.length) { const note = document.createElement('p'); note.textContent = 'No questions yet.'; column.append(note); }
    board.append(column);
  }
  document.getElementById('progress').textContent = `${state.usedQuestionIds.length} of ${state.categories.reduce((count, c) => count + c.questions.length, 0)} clues used · revision ${state.revision}`;
}
''')
w('edit.js',r'''
import { removeCategory, removeQuestion } from './store.js';
export function createEditor({ save, getSnapshot }) {
  const dialog = document.getElementById('editor-modal'); const container = document.getElementById('editor-container');
  let draft, baseline;
  function field(labelText, value, change, { max = 1000, numeric = false, multiline = false } = {}) {
    const label = document.createElement('label'); label.append(document.createTextNode(labelText)); const input = document.createElement(multiline ? 'textarea' : 'input');
    input.value = value; input.required = true;
    if (numeric) { input.type = 'number'; input.min = '100'; input.max = '10000'; input.step = '100'; } else input.maxLength = max;
    input.addEventListener('input', () => change(numeric ? Number(input.value) : input.value)); label.append(input); return label;
  }
  function button(label, action) { const result = document.createElement('button'); result.type = 'button'; result.textContent = label; result.addEventListener('click', action); return result; }
  function render() {
    container.replaceChildren();
    draft.categories.forEach((category, categoryIndex) => {
      const section = document.createElement('section'); section.className = 'editor-category';
      section.append(field(`Category ${categoryIndex+1} name`, category.name, value => { category.name = value; }, { max: 80 }));
      section.append(button(`Delete category ${categoryIndex+1}`, () => { if (confirm('Remove this category and its questions from the draft?')) { draft = removeCategory(draft, category.id); render(); } }));
      category.questions.forEach((question, index) => {
        const group = document.createElement('fieldset'); const legend = document.createElement('legend'); legend.textContent = `Question ${index+1}`; group.append(legend);
        group.append(field(`Category ${categoryIndex+1} question ${index+1} prompt`, question.prompt, value => { question.prompt = value; }, { multiline: true }), field(`Category ${categoryIndex+1} question ${index+1} answer`, question.answer, value => { question.answer = value; }, { multiline: true }), field(`Category ${categoryIndex+1} question ${index+1} points`, question.points, value => { question.points = value; }, { numeric: true }));
        group.append(button(`Delete question ${index+1} from category ${categoryIndex+1}`, () => { if (confirm('Remove this question from the draft?')) { draft = removeQuestion(draft, category.id, question.id); render(); } })); section.append(group);
      });
      const add = button(`Add question to category ${categoryIndex+1}`, () => { category.questions.push({ id: crypto.randomUUID(), prompt: '', answer: '', points: 100 }); render(); }); add.disabled = category.questions.length >= 20; section.append(add); container.append(section);
    });
    document.getElementById('add-category').disabled = draft.categories.length >= 10;
  }
  function open() { const current = getSnapshot(); draft = structuredClone(current.state); baseline = current.raw; document.getElementById('editor-error').textContent = ''; render(); dialog.showModal(); }
  document.getElementById('add-category').addEventListener('click', () => { if (draft.categories.length < 10) { draft.categories.push({ id: crypto.randomUUID(), name: '', questions: [] }); render(); } });
  document.getElementById('close-editor').addEventListener('click', () => dialog.close());
  document.getElementById('editor-form').addEventListener('submit', async event => { event.preventDefault(); if (await save(draft, baseline)) dialog.close(); });
  return { open, dialog };
}
''')
print('Quiz board store, static server and accessible CRUD editor written')
