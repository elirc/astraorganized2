from pathlib import Path
s=Path('astra-remaining-improvements/stage/b415b13a50ee');p=s/'src/app.js';t=p.read_text(encoding='utf-8');t=t.replace("import { layout } from './layout.js';", "import { layout } from './layout.js';\nimport { normalize, parsePreview, applyMessage } from '../extension/model.js';")
start=t.index('function localRead() {');end=t.index('function toast(message)',start)
t=t[:start]+r'''
let revision = 0, presets = [], messageRevision = 0, settingsRevision = 0, presetRevision = 0, editingPresetId = null;
function localRead() { return parsePreview(localStorage.getItem(key)); }
async function send(message = { type: 'read' }) {
  let data;
  if (extension) data = await chrome.runtime.sendMessage(message);
  else {
    if (!navigator.locks?.request) throw new Error('Open Interlude on localhost in a browser with Web Locks.');
    data = await navigator.locks.request(key, async () => {
      const stored = localRead(); const next = applyMessage(stored,message);
      if (message.type === 'command' && stored.state.phase !== 'break' && next.state.phase === 'break' && next.settings.shuffle) {
        const choices = artworks.filter(art => art.id !== next.settings.art); next.settings.art = choices[Math.floor(Math.random()*choices.length)].id; next.revision++;
      }
      const accepted = normalize(next);
      if (message.type !== 'read') localStorage.setItem(key,JSON.stringify(accepted));
      return accepted;
    });
  }
  if (data?.error) throw new Error(data.error);
  settings = data.settings; state = data.state; revision = data.revision; presets = data.presets;
  return data;
}
''' + t[end:]
t=t.replace("function fillEditors() {", "function fillEditors() {\n  messageRevision = revision; settingsRevision = revision;")
t=t.replace("if (view === 'art') renderGallery();", "if (view === 'art') renderGallery();\n  if (view === 'message' || view === 'settings') fillEditors();\n  if (view === 'message') renderPresets();")
t=t.replace('async function saveSettings(patch, confirmation) {','async function saveSettings(patch, confirmation, expectedRevision = revision) {')
t=t.replace("await send({ type: 'settings', settings: { ...settings, ...patch } });", "const saved = await send({ type: 'settings', settings: patch, expectedRevision });\n    if (currentView === 'message') messageRevision = revision; if (currentView === 'settings') settingsRevision = revision;")
t=t.replace('toast(confirmation);','toast(saved.warning || confirmation);')
t=t.replace("try { await send({ type: 'command', command: action }); renderArt(); renderTimer(); }", "try { const saved = await send({ type: 'command', command: action }); renderArt(); renderTimer(); if (saved.warning) toast(saved.warning); }")
t=t.replace("'Your message is saved');", "'Your message is saved', messageRevision);")
t=t.replace("state.running ? 'Settings saved for your next session' : 'Your rhythm is saved');", "state.running ? 'Settings saved for your next session' : 'Your rhythm is saved', settingsRevision);")
t=t.replace("const file = event.target.files[0]; if (!file) return;", "const file = event.target.files[0]; if (!file) return; const uploadRevision = revision;")
t=t.replace("'Your artwork is ready');", "'Your artwork is ready', uploadRevision);")
t=t.replace("try { await send(); renderTimer(); renderArt(); }", "try { const loaded = await send(); renderTimer(); renderArt(); renderPresets(); if (loaded.warning) toast(loaded.warning); }")
insert=t.index('async function refresh()')
t=t[:insert]+r'''
const library = document.createElement('section'); library.className = 'saved-messages';
library.innerHTML = '<h2>Saved messages</h2><p class="muted">Keep up to 30 reminders. Use copies one into your message draft.</p><div id="preset-list"></div><form id="preset-form"><label for="preset-title">Title</label><input id="preset-title" maxlength="80" required><label for="preset-message">Saved message text</label><textarea id="preset-message" maxlength="500" rows="3" required></textarea><div class="preset-actions"><button class="primary" id="preset-save" type="submit">Create saved message</button><button class="secondary" id="preset-cancel" type="button">Clear saved-message form</button></div><p id="preset-error" role="alert"></p></form>';
$('#message-view').append(library);
function clearPreset() { editingPresetId = null; presetRevision = revision; $('#preset-title').value = ''; $('#preset-message').value = ''; $('#preset-save').textContent = 'Create saved message'; $('#preset-error').textContent = ''; }
function renderPresets() {
  $('#preset-list').replaceChildren();
  for (const preset of presets) {
    const card = document.createElement('article'); card.className = 'preset-card'; const heading = document.createElement('h3'); heading.textContent = preset.title;
    const text = document.createElement('p'); text.textContent = preset.message; const actions = document.createElement('div'); actions.className = 'preset-actions';
    const button = (label, handler) => { const node = document.createElement('button'); node.type = 'button'; node.className = 'secondary'; node.textContent = label; node.addEventListener('click',handler); return node; };
    actions.append(button(`Use ${preset.title}`,()=>{ messageRevision = revision; $('#message-input').value = preset.message; updateMessagePreview(); toast('Message copied into your draft. Save message to apply it.'); }), button(`Edit ${preset.title}`,()=>{ editingPresetId = preset.id; presetRevision = revision; $('#preset-title').value = preset.title; $('#preset-message').value = preset.message; $('#preset-save').textContent = 'Update saved message'; $('#preset-error').textContent = ''; $('#preset-title').focus(); }), button(`Delete ${preset.title}`,async()=>{
      if (!confirm(`Delete saved message "${preset.title}"? Your active reminder stays unchanged.`)) return;
      try { await send({type:'preset',action:'delete',id:preset.id,expectedRevision:revision}); if(editingPresetId===preset.id)clearPreset();renderPresets();toast('Saved message deleted.'); } catch(error) { $('#preset-error').textContent = error.message; }
    }));card.append(heading,text,actions);$('#preset-list').append(card);
  }
}
$('#preset-cancel').addEventListener('click',clearPreset);
$('#preset-form').addEventListener('submit',async event=>{
  event.preventDefault(); const preset = {id:editingPresetId || crypto.randomUUID(),title:$('#preset-title').value,message:$('#preset-message').value};
  try { await send({type:'preset',action:editingPresetId?'update':'create',id:editingPresetId || undefined,preset,expectedRevision:presetRevision});clearPreset();renderPresets();toast('Saved message stored.'); }
  catch(error) { $('#preset-error').textContent = error.message; }
});
const recovery = document.createElement('section'); recovery.className = 'data-tools';
recovery.innerHTML = '<h2>Your local data</h2><p class="muted">Export settings, timer state and saved messages. The preview and extension use separate storage.</p><button class="secondary" id="export-data">Export local data</button><button class="secondary" id="reset-preview">Reset browser preview data</button>';
$('#settings-view').append(recovery);$('#reset-preview').hidden = extension;
$('#export-data').addEventListener('click',async()=>{
  try { const raw = extension ? JSON.stringify(await chrome.storage.local.get(['settings','state','revision','presets']),null,2) : localStorage.getItem(key) || '{}';const url=URL.createObjectURL(new Blob([raw],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download='interlude-local-data.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000); }
  catch(error){toast('Export failed: '+error.message);}
});
$('#reset-preview').addEventListener('click',async()=>{
  if(extension)return;const expected=localStorage.getItem(key);if(!confirm('Replace browser preview settings, timer and saved messages with defaults? Export first to keep a copy.'))return;
  try { await navigator.locks.request(key,async()=>{if(localStorage.getItem(key)!==expected)throw new Error('Preview changed elsewhere. Review before resetting.');localStorage.setItem(key,JSON.stringify(normalize()));});location.reload(); }
  catch(error){toast('Reset failed: '+error.message);}
});
''' + t[insert:]
t=t.replace("await send(); fillEditors(); renderArt(); renderTimer(); icons();", "await send(); fillEditors(); clearPreset(); renderPresets(); renderArt(); renderTimer(); icons();")
p.write_text(t,encoding='utf-8')
p=s/'extension/styles.css';t=p.read_text(encoding='utf-8')+r'''
.saved-messages,.data-tools{margin-top:32px;padding-top:24px;border-top:1px solid var(--border,#dce1d9)}.saved-messages form{max-width:640px;margin-top:24px}.saved-messages label{display:block;margin:16px 0 6px;font-weight:600}.saved-messages input{width:100%;padding:12px;border:1px solid #b8c6b8;border-radius:8px;font:inherit;background:#fff}.preset-card{padding:18px 0;border-bottom:1px solid #dce1d9}.preset-card h3{margin:0 0 8px;overflow-wrap:anywhere}.preset-card p{white-space:pre-wrap;overflow-wrap:anywhere}.preset-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}.preset-actions button{white-space:normal;overflow-wrap:anywhere}#preset-error{color:#9a3527;white-space:pre-wrap}.data-tools button{margin:10px 10px 0 0}
''';p.write_text(t,encoding='utf-8');print('UI uses partial revision-checked settings, message CRUD and explicit data recovery')
