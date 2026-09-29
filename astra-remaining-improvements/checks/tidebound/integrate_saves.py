from pathlib import Path

S = Path(__file__).resolve().parents[2] / 'stage/4de416cd300b'
p = S / 'src/main.ts'
t = p.read_text(encoding='utf-8')
t = t.replace("import './style.css';", "import './style.css';\nimport './voyages.css';\nimport { VoyageRepository, VoyageError, type Voyage, type Slot } from './voyages';\nimport { VoyageLibrary } from './voyageLibrary';")
t = t.replace('const $ =', 'async function start() {\nconst $ =', 1)
start = t.index("let state:GameState, recoveryMessage='';")
end = t.index('let selectedIsland=', start)
t = t[:start] + '''let state:GameState = newGame('TIDEBOUND'), recoveryMessage='';
let repository: VoyageRepository | null = null;
const slots: Partial<Record<Slot, Voyage>> = {};
const blockedSlots = new Set<Slot>();
let generation = 0, switching = false;
let operations: Promise<unknown> = Promise.resolve();
function enqueue<T>(operation: () => Promise<T>): Promise<T> {
  const next = operations.then(operation, operation);
  operations = next.catch(() => undefined);
  return next;
}
try {
  repository = await VoyageRepository.open();
  const rows = await repository.list();
  for (const slot of ['manual', 'autosave'] as const) {
    slots[slot] = rows.find(row => row.kind === slot);
    if (!slots[slot]) {
      // Copy valid legacy slots once. The old keys are never changed or deleted.
      try {
        const raw = localStorage.getItem('tidebound.' + slot);
        if (raw) slots[slot] = await repository.saveSlot(slot, 0, raw);
      } catch (error) {
        if (error instanceof VoyageError && error.code === 'conflict') {
          slots[slot] = (await repository.read(slot)).voyage;
        } else {
          blockedSlots.add(slot);
          recoveryMessage += `The previous ${slot} could not be copied. Its original data is untouched. Use the library or export to preserve new work. `;
        }
      }
    }
  }
  if (slots.autosave) {
    try { const saved = await repository.read('autosave'); state = saved.state; slots.autosave = saved.voyage; }
    catch { blockedSlots.add('autosave'); recoveryMessage += 'The stored autosave could not be opened; automatic writes are paused. Export new work or save a separate checkpoint. '; }
  }
} catch {
  recoveryMessage += 'Browser storage is unavailable. You can play and export, but local saves are disabled. ';
  repository?.close(); repository = null;
  try { const raw = localStorage.getItem('tidebound.autosave'); if (raw) state = parseSave(raw); } catch { /* Keep original bytes untouched. */ }
}
''' + t[end:]
position = "const currentIsland=()=>"
t = t.replace(position, "const library = new VoyageLibrary(repository, () => serializeGame(state), raw => switchVoyage(parseSave(raw)));\n" + position)
t = t.replace('<h3>Your voyages</h3>', '<h3>Your voyages</h3><button class="primary" data-action="voyage-library">Open voyage library</button><p>Save named checkpoints, add learning notes, and manage earlier experiments. The library pauses the simulation.</p>')
start = t.index('function hasSave(')
end = t.index('function loadState(', start)
t = t[:start] + '''function hasSave(slot:Slot){return !!slots[slot];}
function saveDate(slot:Slot){return slots[slot] ? new Date(slots[slot]!.savedAt).toLocaleString() : repository ? 'No voyage saved yet' : 'Storage unavailable';}
function save(slot:Slot='manual',silent=false):Promise<boolean>{
 if(switching)return Promise.resolve(false);
 const raw=serializeGame(state), capturedGeneration=generation;
 return enqueue(async()=>{
  if(capturedGeneration!==generation)return false;
  if(blockedSlots.has(slot)){
   if(!silent)toast('This save slot needs review. Load its stored version or save a separate checkpoint in the voyage library.','warning');
   return false;
  }
  try{
   if(!repository)throw new Error('Local storage is unavailable. Export your voyage from Settings.');
   const saved=await repository.saveSlot(slot,slots[slot]?.revision??0,raw);
   slots[slot]=saved;
   $('#save-status').textContent=slot==='manual'?'Voyage saved':'Autosaved just now';
   if(!silent){toast('Your voyage has been saved.','good');if(activePanel==='settings')renderModal();}
   return true;
  }catch(error){
   if(error instanceof VoyageError&&error.code==='conflict')blockedSlots.add(slot);
   $('#save-status').textContent='Save needs attention';
   toast(error instanceof Error?error.message:'Unable to save. Export your voyage to keep it safe.','warning');
   return false;
  }
 });
}
async function switchVoyage(next:GameState, source?:{voyage:Voyage}){
 if(switching)throw new Error('A voyage is already loading. Please wait.');
 switching=true;
 try{
  await enqueue(async()=>{
   if(!repository)throw new Error('Local storage is unavailable. Export your current voyage before reloading.');
   // Replacing the active world requires a committed autosave first.
   if(source?.voyage.kind==='autosave'){
    slots.autosave=source.voyage;
   }else{
    const saved=await repository.saveSlot('autosave',slots.autosave?.revision??0,serializeGame(next));
    slots.autosave=saved;
   }
   if(source&&(source.voyage.kind==='manual'||source.voyage.kind==='autosave')){
    slots[source.voyage.kind]=source.voyage;blockedSlots.delete(source.voyage.kind);
   }
   blockedSlots.delete('autosave');
   generation++;loadState(next);lastAutosave=performance.now();
   $('#save-status').textContent='Loaded saved voyage';
  });
 }finally{switching=false;}
}
''' + t[end:]
t = t.replace("document.addEventListener('click',event=>{", "document.addEventListener('click',async event=>{", 1)
t = t.replace("audio.start(state);const action=target.dataset.action!,id=target.dataset.id!;", "audio.start(state);const action=target.dataset.action!,id=target.dataset.id!;\n if(switching)return;\n if(action==='voyage-library'){state.speed=0;closePanel();renderHud();void library.open();return;}")
old = next(line for line in t.splitlines() if "if(action==='load'){" in line)
t = t.replace(old, ''' if(action==='load'){
  pendingSlot=target.dataset.slot as Slot;activePanel='load-confirm';
  $('#modal').innerHTML=`<section class="modal-sheet compact" role="dialog" aria-modal="true" aria-label="Load saved voyage">${panelHeader('RETURN TO A SAVED WORLD','Replace the active voyage?','Unsaved active progress will be replaced. Cancel and save a separate checkpoint first if you need it.')}<div class="button-row"><button class="primary" data-action="confirm-load">Load saved voyage</button><button class="secondary" data-action="panel" data-panel="settings">Cancel load</button></div></section>`;return;
 }
 if(action==='confirm-load'){
  try{if(!repository)throw new Error('Storage is unavailable.');const saved=await repository.read(pendingSlot);await switchVoyage(saved.state,saved);toast('Welcome back to your islands.','good');}
  catch(error){toast(error instanceof Error?error.message:'Unable to open this save.','warning');}return;
 }''')
t = t.replace("let newSeed='';", "let newSeed='', pendingImport='';\nlet pendingSlot:Slot='manual';")
old = next(line for line in t.splitlines() if "if(action==='new-game'){" in line)
t = t.replace(old, " if(action==='new-game'){try{await switchVoyage(newGame(newSeed));toast('A new horizon. A new beginning.','good');}catch(error){toast(error instanceof Error?error.message:'Unable to start voyage.','warning');}return;}\n if(action==='confirm-import'){try{await switchVoyage(parseSave(pendingImport));pendingImport='';toast('Your voyage has arrived safely.','good');}catch(error){toast(error instanceof Error?error.message:'Unable to import voyage.','warning');}return;}")
old = next(line for line in t.splitlines() if "$('#import-file').addEventListener('change'" in line)
t = t.replace(old, '''$('#import-file').addEventListener('change',async event=>{
 const input=event.target as HTMLInputElement,file=input.files?.[0];if(!file)return;
 try{
  if(file.size>5_000_000)throw new Error('This save is too large. Please choose a Tidebound JSON export under 5 MB.');
  const raw=await file.text();parseSave(raw);pendingImport=raw;
  openPanel('import-confirm');
  $('#modal').innerHTML=`<section class="modal-sheet compact" role="dialog" aria-modal="true" aria-label="Import saved voyage">${panelHeader('A VOYAGE FROM ANOTHER SHORE','Replace the active voyage?','The import is valid. Confirm to replace your active world and automatic save. Save a separate checkpoint first if you need your current progress.')}<div class="button-row"><button class="primary" data-action="confirm-import">Import this voyage</button><button class="secondary" data-action="panel" data-panel="settings">Cancel import</button></div></section>`;
 }catch(error){toast(error instanceof Error?error.message:'This save could not be imported.','warning');}finally{input.value='';}
});''')
t = t.replace("document.addEventListener('keydown',event=>{", "document.addEventListener('keydown',event=>{\n if(library.isOpen)return;")
t = t.replace("button:not(:disabled),input,select,summary,a[href]", "button:not(:disabled),input,textarea,select,summary,a[href]")
t = t.replace("window.addEventListener('pagehide',()=>save('autosave',true));", "// Do not claim that asynchronous storage can finish during page teardown.\nwindow.addEventListener('beforeunload',event=>{if(switching){event.preventDefault();}});")
t += "\n}\nvoid start().catch(error => { console.error(error); const app=document.querySelector('#app'); if(app)app.textContent='Tidebound could not start. Check WebGL2 support and reload. Existing saves were not cleared.'; });\n"
p.write_text(t, encoding='utf-8')
print('Integrated versioned slots and library without changing original project files.')
