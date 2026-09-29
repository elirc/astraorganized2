from pathlib import Path
s=Path('astra-remaining-improvements/stage/6844a7b03c83')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('main.js',r'''
import { BoardStore, STORAGE_KEY, freshState, parseState } from './store.js';
import { renderBoard } from './board.js';
import { createEditor } from './edit.js';
const byId = id => document.getElementById(id);
let storage;
try { storage = window.localStorage; } catch { storage = { getItem() { throw new Error('Storage unavailable'); }, setItem() { throw new Error('Storage unavailable'); } }; }
const store = new BoardStore(storage, navigator.locks);
let current = { state: freshState(), raw: null }, valid = true, busy = false, clue = null;
const editor = createEditor({ getSnapshot: () => current, save: (draft, baseline) => save(draft, baseline, 'Question bank saved.') });
function error(message) { byId('error').textContent = message; byId('error-panel').hidden = !message; byId('editor-error').textContent = message; byId('replace-btn').hidden = valid; byId('export-raw').hidden = valid; }
function status(message) { byId('status').textContent = message; }
function render() {
  renderBoard(current.state, showClue);
  byId('edit-btn').disabled = !valid; byId('reset-round').disabled = !valid; byId('import-file').disabled = !valid;
  if (!valid) document.querySelectorAll('.tile').forEach(button => { button.disabled = true; });
}
function load() {
  try { current = store.load(); valid = true; error(''); }
  catch (cause) { valid = false; let raw = null; try { raw = storage.getItem(STORAGE_KEY); } catch { /* Recovery still explains unavailable storage. */ } current = { state: freshState(), raw }; error(cause.message); }
  render();
}
async function save(draft, baseline, message, options) {
  if (busy) return false;
  busy = true; const controls = [...document.querySelectorAll('button,input,textarea')].map(element => [element, element.disabled]); controls.forEach(([element]) => { element.disabled = true; });
  try { const committed = await store.save(draft, baseline, options); current = committed; valid = true; error(''); status(message); render(); return true; }
  catch (cause) { error(cause.message); status(''); return false; }
  finally { busy = false; controls.forEach(([element, disabled]) => { if (element.isConnected) element.disabled = disabled; }); byId('edit-btn').disabled = !valid; byId('reset-round').disabled = !valid; byId('import-file').disabled = !valid; }
}
function showClue(question, category) {
  clue = { question: structuredClone(question), raw: current.raw };
  byId('clue-title').textContent = `${category} · ${question.points} points`; byId('clue-text').textContent = question.prompt;
  byId('answer-text').textContent = question.answer; byId('answer-text').hidden = true; byId('answer-modal').showModal();
}
byId('reveal-answer').addEventListener('click', () => { byId('answer-text').hidden = false; });
byId('close-answer').addEventListener('click', () => byId('answer-modal').close());
byId('mark-used').addEventListener('click', async () => {
  if (!clue) return;
  const draft = structuredClone(current.state);
  if (!draft.categories.some(category => category.questions.some(question => question.id === clue.question.id))) { error('This clue was removed. Close it and reload the board.'); return; }
  if (!draft.usedQuestionIds.includes(clue.question.id)) draft.usedQuestionIds.push(clue.question.id);
  if (await save(draft, clue.raw, 'Clue marked used.')) byId('answer-modal').close();
});
byId('edit-btn').addEventListener('click', () => { if (valid && !busy) editor.open(); });
byId('reload-btn').addEventListener('click', () => { load(); if (valid) status('Saved board reloaded.'); });
byId('reset-round').addEventListener('click', async () => {
  if (!confirm('Start a new round? Questions stay; used clues become available again.')) return;
  const draft = structuredClone(current.state); draft.usedQuestionIds = []; await save(draft, current.raw, 'New round started.');
});
function download(text, name) { const url = URL.createObjectURL(new Blob([text], { type: 'application/json' })); const link = document.createElement('a'); link.href = url; link.download = name; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); }
byId('export-btn').addEventListener('click', () => { if (valid) download(JSON.stringify(current.state,null,2),'quiz-board.json'); else error('Use Export saved text to preserve the unreadable original.'); });
byId('export-raw').addEventListener('click', () => { if (current.raw !== null) download(current.raw,'quiz-board-recovery.txt'); else error('There is no readable saved text to export.'); });
byId('replace-btn').addEventListener('click', async () => {
  if (!confirm('Replace the unreadable saved data with the example board? Export saved text first if you want to keep it.')) return;
  await save(freshState(), current.raw, 'Example board saved.', { replaceInvalid: true });
});
byId('import-file').addEventListener('change', async event => {
  const file = event.target.files?.[0]; event.target.value = ''; if (!file || busy) return; const baseline = current.raw;
  try {
    if (file.size > 2*1024*1024) throw new Error('Import must be at most 2 MiB.');
    const draft = parseState(await file.text());
    if (!confirm('Replace this saved board with the imported question bank and round state?')) return;
    await save(draft, baseline, 'Imported board saved.');
  } catch (cause) { error(cause.message); }
});
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY && event.key !== null) return;
  load(); status('Saved board changed in another tab.');
  if (editor.dialog.open) byId('editor-error').textContent = 'Another tab changed the saved board. This draft is preserved; cancel and reload before editing again.';
});
for (const dialog of document.querySelectorAll('dialog')) dialog.addEventListener('cancel', event => { if (busy) event.preventDefault(); });
load();
''')
w('styles.css',r'''
:root{font-family:system-ui,sans-serif;color:#182b44;background:#f2f5fa;line-height:1.5}*{box-sizing:border-box}body{margin:0}main{max-width:1280px;margin:auto;padding:32px 24px 60px}h1{font-size:clamp(2rem,5vw,3rem);line-height:1.1;margin:10px 0}h2{font-size:1.1rem}.eyebrow{font-size:.8rem;letter-spacing:.12em;color:#4664ab;font-weight:750}.toolbar,.actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center}button,.file-button{font:inherit;border:1px solid #8396bc;border-radius:7px;padding:9px 14px;background:white;color:#223f79;cursor:pointer}button:hover:not(:disabled){background:#e6edfc}button:disabled{opacity:.5;cursor:not-allowed}:focus-visible{outline:3px solid #db9118;outline-offset:3px}.file-button{position:relative;overflow:hidden}.file-button input{position:absolute;inset:0;opacity:0;width:100%;cursor:pointer}.board{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:14px}.category{min-width:0}.category h2{background:white;min-height:78px;border:1px solid #d8e1f0;padding:14px;border-radius:9px;overflow-wrap:anywhere;display:flex;align-items:center;justify-content:center;text-align:center}.category p{text-align:center}.tile{display:block;width:100%;min-height:92px;margin:10px 0;background:#234a93;color:#f8dc86;border:none;font-size:1.65rem;font-weight:750}.tile:hover:not(:disabled){background:#16366e}.tile:disabled{background:#d5deec;color:#506178;opacity:1}.footnote{color:#536780;font-size:.9rem;margin-top:24px}#status{min-height:24px;color:#11664c}#error-panel{border:1px solid #d6a29d;background:#fff1ef;border-radius:8px;padding:12px;margin:16px 0}#error,#editor-error{color:#912f24;white-space:pre-wrap;overflow-wrap:anywhere}dialog{border:1px solid #b6c7df;border-radius:12px;padding:24px;max-width:min(760px,calc(100vw - 24px));width:100%;max-height:90vh;overflow:auto;box-shadow:0 24px 80px #14223f55}dialog::backdrop{background:#172843aa}#clue-text,#answer-text{font-size:1.2rem;white-space:pre-wrap;overflow-wrap:anywhere}#answer-text{background:#edf6ef;padding:16px;border-radius:8px}.editor-category{border:1px solid #cbd7ea;border-radius:8px;padding:16px;margin:18px 0}label{display:flex;flex-direction:column;gap:5px;font-weight:600;margin:10px 0}input,textarea{font:inherit;border:1px solid #859abd;border-radius:5px;padding:9px;width:100%;min-width:0}textarea{min-height:72px;resize:vertical}fieldset{border:1px solid #d0daea;padding:12px;min-width:0;margin:14px 0}legend{font-weight:650}.sticky{position:sticky;bottom:-24px;background:#fff;padding:14px 0;border-top:1px solid #d0daea}@media(max-width:520px){main{padding:22px 12px}.board{grid-template-columns:1fr 1fr;gap:10px}.category h2{font-size:.9rem;padding:10px}.tile{min-height:76px}dialog{padding:16px}.sticky{bottom:-16px}.toolbar button,.toolbar .file-button{font-size:.9rem}}
''')
w('.gitignore','node_modules/\ntest-results/\nplaywright-report/\n.verification/\n')
w('playwright.config.js',r'''
import { defineConfig } from '@playwright/test';
const port = Number(process.env.QUIZ_TEST_PORT || 24763);
export default defineConfig({ testDir: './e2e', workers: 1, retries: 0, timeout: 30000, expect: { timeout: 7000 }, use: { baseURL: `http://127.0.0.1:${port}`, browserName: 'chromium', trace: 'retain-on-failure' }, webServer: { command: 'node server.js', url: `http://127.0.0.1:${port}`, env: { PORT: String(port) }, reuseExistingServer: false, timeout: 30000 } });
''')
print('Gameplay, persistence recovery, import/export and responsive layout written')
