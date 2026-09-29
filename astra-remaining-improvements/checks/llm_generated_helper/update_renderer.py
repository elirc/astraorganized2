from pathlib import Path
import hashlib
import json

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/44013f102ff1"
baseline = json.loads((B / "baselines/44013f102ff1.json").read_text(encoding="utf-8"))["files"]
path = S / "src/renderer/app.js"
assert hashlib.sha256(path.read_bytes()).hexdigest() == baseline["src/renderer/app.js"]
text = path.read_text(encoding="utf-8")
text = text.replace("const recordBtn = $('recordBtn');", "const recordBtn = $('recordBtn');\nconst cancelBtn = $('cancelBtn');")
text = text.replace("settingsBtn.disabled = !ui.canSettings;", "settingsBtn.disabled = !ui.canSettings;\n  cancelBtn.hidden = !['recording', 'transcribing', 'generating'].includes(next);\n  cancelBtn.disabled = false;")
start = text.index('// ---------- Settings ----------')
end = text.index('// ---------- Bridge wiring & init ----------', start)
text = text[:start] + '''// ---------- Settings: secrets are write-only, revisions are explicit ----------
const fields = ['resume', 'jobDescription'];
const secretFields = ['siliconflowKey', 'deepseekKey'];
const reloadSettingsBtn = $('reloadSettingsBtn');
let savedNoteTimer = null;
let settingsRevision = null;
let settingsBaseline = null;
let settingsBusy = false;
let settingsNeedsReload = false;

function settingsDraft() {
  return {
    ...Object.fromEntries(fields.map(key => [key, $(key).value])),
    alwaysOnTop: $('alwaysOnTop').checked,
    ...Object.fromEntries(secretFields.flatMap(key => [[key, $(key).value], ['clear' + key, $('clear' + key).checked]])),
  };
}
function settingsDirty() { return settingsBaseline !== null && JSON.stringify(settingsDraft()) !== JSON.stringify(settingsBaseline); }
function syncSettings() {
  for (const element of settingsView.querySelectorAll('input,textarea,button')) element.disabled = settingsBusy;
  saveBtn.disabled = settingsBusy || settingsNeedsReload || !settingsRevision;
  settingsBtn.disabled = settingsBusy || state !== 'idle';
}
function acceptSettings(value) {
  settingsRevision = value.revision;
  settingsNeedsReload = false;
  for (const key of fields) $(key).value = value[key] ?? '';
  $('alwaysOnTop').checked = value.alwaysOnTop;
  for (const key of secretFields) {
    $(key).value = '';
    $('clear' + key).checked = false;
    $(key).placeholder = value.credentials[key] ? 'Saved; leave blank to keep it' : 'Enter a new credential';
    $(key + 'Status').textContent = value.credentials[key] ? 'A credential is saved. Its value is never returned to this screen.' : 'No credential is saved.';
  }
  settingsBaseline = settingsDraft();
}
async function openSettings() {
  if (settingsBusy || state !== 'idle') return;
  if (!settingsView.hidden && settingsDirty() && !confirm('Discard the unsaved settings draft and reload accepted values?')) return;
  settingsBusy = true; syncSettings();
  try {
    acceptSettings(await window.api.getSettings());
    mainView.hidden = true; settingsView.hidden = false; savedNote.hidden = true;
    clearError();
  } catch (error) { showError(error); }
  finally { settingsBusy = false; syncSettings(); }
  if (!settingsView.hidden) $('resume').focus();
}
settingsBtn.addEventListener('click', openSettings);
reloadSettingsBtn.addEventListener('click', openSettings);
backBtn.addEventListener('click', () => {
  if (settingsBusy || (settingsDirty() && !confirm('Discard this unsaved settings draft?'))) return;
  for (const key of secretFields) { $(key).value = ''; $('clear' + key).checked = false; }
  settingsBaseline = null;
  settingsView.hidden = true; mainView.hidden = false; savedNote.hidden = true;
  clearTimeout(savedNoteTimer); settingsBtn.focus();
});
saveBtn.addEventListener('click', async () => {
  if (settingsBusy || settingsNeedsReload || !settingsBaseline) return;
  const draft = settingsDraft();
  const changes = Object.fromEntries([...fields, 'alwaysOnTop'].filter(key => draft[key] !== settingsBaseline[key]).map(key => [key, draft[key]]));
  for (const key of secretFields) {
    if (draft['clear' + key]) changes[key] = '';
    else if (draft[key].trim()) changes[key] = draft[key].trim();
  }
  if (!Object.keys(changes).length) { savedNote.textContent = 'No settings changed.'; savedNote.hidden = false; return; }
  settingsBusy = true; syncSettings(); clearError();
  try {
    const accepted = await window.api.saveSettings({ revision: settingsRevision, changes });
    acceptSettings(accepted);
    savedNote.textContent = 'Settings saved.'; savedNote.hidden = false;
    clearTimeout(savedNoteTimer);
    savedNoteTimer = setTimeout(() => { savedNote.hidden = true; }, 1500);
  } catch (error) {
    settingsNeedsReload = true;
    showError(new Error(`${error.message} Your draft remains here. Copy any changes you need, then reload accepted settings before another save.`));
  } finally { settingsBusy = false; syncSettings(); }
});

cancelBtn.addEventListener('click', async () => {
  if (state === 'recording') {
    stopStream(); chunks = []; setState('idle', 'Recording discarded. Nothing was submitted.'); return;
  }
  if (!['transcribing', 'generating'].includes(state)) return;
  cancelBtn.disabled = true; statusText.textContent = 'Cancelling the current request…';
  try { await window.api.cancelAsk(); }
  catch (error) { showError(error); cancelBtn.disabled = false; }
});

''' + text[end:]
text = text.replace("window.api.onTranscript((text) => {", "const unsubscribeTranscript = window.api.onTranscript((text) => {")
text = text.replace("window.api.onAnswerChunk((chunk) => {", "const unsubscribeAnswer = window.api.onAnswerChunk((chunk) => {")
text = text.replace("if (!s.siliconflowKey || !s.deepseekKey)", "if (!s.credentials.siliconflowKey || !s.credentials.deepseekKey)")
text = text.replace("  // First run: nudge", "  window.addEventListener('beforeunload', () => {\n    stopStream(); unsubscribeTranscript(); unsubscribeAnswer();\n    window.api.cancelAsk().catch(() => {});\n  });\n\n  // First run: nudge")
path.write_text(text, encoding="utf-8")
print("Updated renderer settings contract, write-only credentials, retained drafts and cancellation")
