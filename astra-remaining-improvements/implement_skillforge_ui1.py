from pathlib import Path
s=Path(__file__).resolve().parent/'stage/a9672affc47e';(s/'src/components').mkdir(exist_ok=True)
(s/'src/components/SavePanel.tsx').write_text('''import type { GameProgress } from "../types";
export function downloadFile(name:string,content:string):void {
 const url=URL.createObjectURL(new Blob([content],{type:'application/json'}));
 try{const anchor=document.createElement('a');anchor.href=url;anchor.download=name;anchor.click();}finally{setTimeout(()=>URL.revokeObjectURL(url),0);}
}
export function SavePanel({progress,error,saving,pending,onLoad,onReset,onError}:{progress:GameProgress;error?:string;saving:boolean;pending:GameProgress|null;onLoad:()=>Promise<void>;onReset:()=>Promise<void>;onError:(message:string)=>void}){
 function exportOriginal(){try{const raw=localStorage.getItem('skillforge.quest.progress.v1');if(raw===null)throw new Error('There is no stored save to export yet.');downloadFile('skillforge-original-save.json',raw);}catch(e){onError((e as Error).message);}}
 function exportPending(){if(!pending)return;try{downloadFile('skillforge-pending-save.json',JSON.stringify({exportedAt:new Date().toISOString(),progress:pending},null,2));}catch(e){onError((e as Error).message);}}
 return <section className={`save-panel ${error?'save-fault':''}`} aria-label="Save status"><div><strong role="status">{saving?'Saving progress…':progress.epoch?`Saved revision ${progress.revision}`:'No saved profile yet'}</strong><p>Drafts stay separate until you save or submit a checkpoint.</p></div>{error&&<p className="save-error" role="alert">{error}</p>}<div className="save-actions"><button disabled={saving} onClick={()=>void onLoad()}>Load current progress</button><button disabled={saving} onClick={exportOriginal}>Export stored data</button>{pending&&<button disabled={saving} onClick={exportPending}>Export pending draft</button>}<button disabled={saving} onClick={()=>void onReset()}>Reset saved progress</button></div></section>;
}
''',encoding='utf-8')
(s/'src/components/LearningNotes.tsx').write_text('''import { useEffect, useMemo, useState } from "react";
import type { Catalog, GameProgress, LearningNote } from "../types";
import { createNote, deleteNote, updateNote } from "../game/notes";
export function LearningNotes({catalog,progress,onProgress,onDirty}:{catalog:Catalog;progress:GameProgress;onProgress:(value:GameProgress)=>Promise<GameProgress>;onDirty:(dirty:boolean)=>void}){
 const [base,setBase]=useState<GameProgress|null>(null);const [editing,setEditing]=useState<string|null>(null);const [title,setTitle]=useState('');const [body,setBody]=useState('');const [missionId,setMissionId]=useState(catalog.missions[0].id);const [query,setQuery]=useState('');const [page,setPage]=useState(1);const [busy,setBusy]=useState(false);const [error,setError]=useState('');
 const missions=useMemo(()=>new Map(catalog.missions.map(m=>[m.id,m.title])),[catalog]);
 useEffect(()=>()=>onDirty(false),[onDirty]);
 const filtered=progress.notes.filter(n=>(n.title+' '+n.body+' '+missions.get(n.missionId)).toLowerCase().includes(query.trim().toLowerCase())).sort((a,b)=>b.updatedAt.localeCompare(a.updatedAt)||a.id.localeCompare(b.id));const pages=Math.max(1,Math.ceil(filtered.length/20));const currentPage=Math.min(page,pages);const visible=filtered.slice((currentPage-1)*20,currentPage*20);
 function open(note?:LearningNote){setBase(progress);setEditing(note?.id??null);setTitle(note?.title??'');setBody(note?.body??'');setMissionId(note?.missionId??progress.lastMissionId??catalog.missions[0].id);setError('');onDirty(true);}
 function close(){setBase(null);setEditing(null);setTitle('');setBody('');onDirty(false);}
 async function save(event:React.FormEvent){event.preventDefault();if(!base)return;setBusy(true);setError('');try{const input={id:editing??crypto.randomUUID(),title,body,missionId};const candidate=editing?updateNote(base,input):createNote(base,input);await onProgress(candidate);close();}catch(e){setError((e as Error).message);}finally{setBusy(false);}}
 async function remove(note:LearningNote){if(!confirm(`Delete learning note "${note.title}"?`))return;setBusy(true);setError('');try{await onProgress(deleteNote(progress,note.id));}catch(e){setError((e as Error).message);}finally{setBusy(false);}}
 return <section className="panel learning-notes" aria-label="Learning notes"><div className="notes-heading"><div><span className="eyebrow">YOUR ENGINEERING JOURNAL</span><h2>Learning notes</h2><p>Keep explanations, examples, and debugging evidence linked to a mission.</p></div><button className="primary-button" disabled={busy||!!base} onClick={()=>open()}>New learning note</button></div>{error&&<p role="alert" className="save-error">{error}</p>}<label className="notes-search">Search learning notes<input value={query} maxLength={120} onChange={e=>{setQuery(e.target.value);setPage(1);}}/></label>
 {base&&<form className="note-editor" onSubmit={save} aria-label="Learning note form"><h3>{editing?'Edit learning note':'Create learning note'}</h3><p>Editing from revision {base.revision}. A rejected save keeps these fields.</p><fieldset disabled={busy}><label>Note title<input required maxLength={120} value={title} onChange={e=>setTitle(e.target.value)}/></label><label>Linked mission<select value={missionId} onChange={e=>setMissionId(e.target.value)}>{catalog.worlds.map(world=><optgroup key={world.id} label={world.name}>{catalog.missions.filter(m=>m.worldId===world.id).map(m=><option key={m.id} value={m.id}>{m.title}</option>)}</optgroup>)}</select></label><label>Note body<textarea required maxLength={10000} rows={8} value={body} onChange={e=>setBody(e.target.value)}/></label></fieldset><div className="save-actions"><button className="primary-button" disabled={busy}>{busy?'Saving note…':'Save learning note'}</button><button type="button" disabled={busy} onClick={()=>{if(confirm('Discard this unsaved note draft?'))close();}}>Discard note draft</button></div></form>}
 {!visible.length&&<p className="notes-empty">{progress.notes.length?'No learning notes match this search.':'No learning notes yet. Create one after your next experiment.'}</p>}<div className="note-cards">{visible.map(note=><article key={note.id} className="note-card"><h3>{note.title}</h3><p className="muted">{missions.get(note.missionId)} · {new Date(note.updatedAt).toLocaleString()}</p><p className="note-preview">{note.body.slice(0,260)}{note.body.length>260?'…':''}</p><details><summary>Read full note</summary><p className="note-body">{note.body}</p></details><div className="save-actions"><button disabled={busy||!!base} onClick={()=>open(note)}>Edit {note.title}</button><button disabled={busy||!!base} onClick={()=>void remove(note)}>Delete {note.title}</button></div></article>)}</div><div className="notes-pages"><span>{filtered.length} matching notes · Page {currentPage} of {pages}</span><button disabled={currentPage===1} onClick={()=>setPage(currentPage-1)}>Previous notes</button><button disabled={currentPage===pages} onClick={()=>setPage(currentPage+1)}>Next notes</button></div></section>;
}
''',encoding='utf-8')
p=s/'src/App.tsx';t=p.read_text(encoding='utf-8');t=t.replace('  challengeKey,','  createProgress,\n  challengeKey,',1).replace('  serializeProgress,','  serializeProgress,\n  resetProgress,\n  STORAGE_KEY,',1);at=t.index('type View =');t=t[:at]+'''import { validateAgainstCatalog, MAX_SAVE_BYTES } from "./game/schema";
import { SavePanel } from "./components/SavePanel";
import { LearningNotes } from "./components/LearningNotes";
'''+t[at:];start=t.index('function App() {');end=t.index('function LoadingScreen(',start)
root='''function App() {
  const [initial] = useState(() => {try{return {progress:loadProgress(),error:undefined as string|undefined};}catch(error){return {progress:createProgress(),error:(error as Error).message};}});
  const [catalog,setCatalog]=useState<Catalog|null>(null);const [catalogError,setCatalogError]=useState<string>();const [catalogReload,setCatalogReload]=useState(0);
  const [progress,setProgress]=useState<GameProgress>(initial.progress);const [saveError,setSaveError]=useState<string|undefined>(initial.error);const [recoveryRequired,setRecoveryRequired]=useState(!!initial.error);
  const [pending,setPending]=useState<GameProgress|null>(null);const [saving,setSaving]=useState(false);const inFlight=useRef(false);const [dirty,setDirty]=useState(false);const [workspaceKey,setWorkspaceKey]=useState(0);
  const [view,setView]=useState<View>("home");const [selectedWorld,setSelectedWorld]=useState("foundations");const [selectedMissionId,setSelectedMissionId]=useState<string>();const [notice,setNotice]=useState<string>();
  useEffect(()=>{const controller=new AbortController();setCatalogError(undefined);fetch('/content/catalog.json',{signal:controller.signal}).then(r=>{if(!r.ok)throw new Error('Mission catalog could not be loaded.');return r.json();}).then((value:Catalog)=>{if(!value||!Array.isArray(value.missions)||!value.missions.length||!Array.isArray(value.worlds))throw new Error('Mission catalog is invalid.');setCatalog(value);}).catch(e=>{if(e.name!=='AbortError')setCatalogError(e.message);});return()=>controller.abort();},[catalogReload]);
  useEffect(()=>{if(!catalog)return;try{validateAgainstCatalog(progress,catalog);}catch(e){setSaveError((e as Error).message);setRecoveryRequired(true);}},[catalog,progress]);
  useEffect(()=>{const changed=(event:StorageEvent)=>{if(event.key===STORAGE_KEY||event.key===null)setSaveError('Another tab changed saved progress. Your displayed data and drafts were kept. Load current progress to review the change.');};window.addEventListener('storage',changed);return()=>window.removeEventListener('storage',changed);},[]);
  useEffect(()=>{const warn=(event:BeforeUnloadEvent)=>{if(dirty){event.preventDefault();event.returnValue='';}};window.addEventListener('beforeunload',warn);return()=>window.removeEventListener('beforeunload',warn);},[dirty]);
  useEffect(()=>{if(!notice)return;const timer=setTimeout(()=>setNotice(undefined),4200);return()=>clearTimeout(timer);},[notice]);
  async function commitProgress(proposal:GameProgress):Promise<GameProgress>{
    if(inFlight.current)throw new Error('A save is already running. Your draft is still here; try again after it finishes.');
    inFlight.current=true;setSaving(true);
    try{if(!catalog)throw new Error('Load the mission catalog before saving.');validateAgainstCatalog(proposal,catalog);const accepted=await persistProgress(proposal);setProgress(accepted);setPending(null);setSaveError(undefined);setDirty(false);return accepted;}
    catch(e){setPending(proposal);setSaveError((e as Error).message);throw e;}
    finally{inFlight.current=false;setSaving(false);}
  }
  function replaceView(next:GameProgress){setProgress(next);setRecoveryRequired(false);setPending(null);setSaveError(undefined);setDirty(false);setWorkspaceKey(v=>v+1);}
  async function loadCurrent(){if(!confirm('Load the saved progress and discard open drafts? Export pending data or copy any text you want to keep first.'))return;try{const next=loadProgress();if(catalog)validateAgainstCatalog(next,catalog);replaceView(next);}catch(e){setSaveError((e as Error).message);}}
  async function resetSaved(){try{const raw=localStorage.getItem(STORAGE_KEY);if(!confirm('Reset all saved progress, answers, reviews and learning notes in this browser? Export a backup first.'))return;replaceView(await resetProgress(raw));setView('home');setSelectedMissionId(undefined);}catch(e){setSaveError((e as Error).message);}}
  const savePanel=<SavePanel progress={progress} error={saveError} saving={saving} pending={pending} onLoad={loadCurrent} onReset={resetSaved} onError={setSaveError}/>;
  const selectedMission=catalog?.missions.find(m=>m.id===selectedMissionId);
  function canLeave(){if(dirty&&!confirm('Leave this view and discard unsaved drafts? Save or copy them first.'))return false;setDirty(false);return true;}
  const openMission=(mission:Mission)=>{if(!isMissionUnlocked(mission,progress)||!canLeave())return;setSelectedMissionId(mission.id);setSelectedWorld(mission.worldId);setView('mission');window.scrollTo({top:0,behavior:'smooth'});};
  const navigate=(next:View)=>{if(!canLeave())return;setView(next);window.scrollTo({top:0,behavior:'smooth'});};
  if(recoveryRequired)return <main className="save-recovery"><h1>Recover your saved progress</h1><p>The original data has not been replaced. Export it before choosing a reset.</p>{savePanel}</main>;
  if(!catalog)return <><div className="startup-save">{savePanel}</div><LoadingScreen message={catalogError} onRetry={()=>setCatalogReload(v=>v+1)}/></>;
  if(!progress.onboarded)return <><div className="startup-save">{savePanel}</div><Onboarding key={workspaceKey} catalog={catalog} progress={progress} onFinish={commitProgress} onDirty={setDirty}/></>;
  return <div className="app-shell" key={workspaceKey}><Sidebar view={view} catalog={catalog} progress={progress} onNavigate={navigate}/><main className="main-shell"><Topbar progress={progress} catalog={catalog}/>{savePanel}
    {view==='home'&&<Dashboard catalog={catalog} progress={progress} onMission={openMission} onJourney={()=>navigate('journey')}/>}
    {view==='journey'&&<Journey catalog={catalog} progress={progress} selectedWorld={selectedWorld} onWorld={setSelectedWorld} onMission={openMission}/>}
    {view==='reviews'&&<Reviews catalog={catalog} progress={progress} onProgress={commitProgress} onNotice={setNotice}/>}
    {view==='profile'&&<Profile catalog={catalog} progress={progress} onProgress={commitProgress} onNotice={setNotice} onDirty={setDirty} onImported={()=>{setDirty(false);setWorkspaceKey(v=>v+1);}}/>}
    {view==='mission'&&selectedMission&&<MissionScreen key={selectedMission.id} mission={selectedMission} catalog={catalog} progress={progress} onProgress={commitProgress} onNotice={setNotice} onBack={()=>navigate('journey')} onNext={openMission} onDirty={setDirty}/>}
  </main>{notice&&<div className="toast" role="status">{notice}</div>}</div>;
}

'''
t=t[:start]+root+t[end:]
t=t.replace('function LoadingScreen({ message }: { message?: string }) {','function LoadingScreen({ message, onRetry }: { message?: string; onRetry: () => void }) {').replace('<p>{message || "Forging your mission map…"}</p>','<p>{message || "Forging your mission map…"}</p>\n      {message && <button onClick={onRetry}>Retry catalog</button>}')
start=t.index('function Onboarding(');end=t.index('function Sidebar(',start);part=t[start:end].replace('  onFinish,','  onFinish,\n  onDirty,').replace('onFinish: (value: GameProgress) => void;','onFinish: (value: GameProgress) => Promise<GameProgress>;\n  onDirty: (dirty: boolean) => void;').replace('  const [minutes, setMinutes] = useState(45);','  const [minutes, setMinutes] = useState(45);\n  const [busy,setBusy] = useState(false);\n  const [error,setError] = useState("");')
a=part.index('        onSubmit={(event) => {');z=part.index('\n      >',a)
part=part[:a]+'''        onSubmit={async (event) => {
          event.preventDefault(); if(!callsign.trim()||busy)return;setBusy(true);setError('');
          try{await onFinish({...progress,callsign:callsign.trim(),sessionMinutes:minutes,onboarded:true});}
          catch(e){setError((e as Error).message);}finally{setBusy(false);}
        }}'''+part[z:]
part=part.replace('onChange={(event) => setCallsign(event.target.value)}','onChange={(event) => {setCallsign(event.target.value);onDirty(true);}}').replace('onClick={() => setMinutes(value)}','onClick={() => {setMinutes(value);onDirty(true);}}').replace('<h2>Create your learner profile</h2>','<h2>Create your learner profile</h2>\n        {error&&<p role="alert">{error}</p>}')
# The existing submit button remains labeled by the original UI; prevent duplicate requests in the handler.
t=t[:start]+part+t[end:];p.write_text(t,encoding='utf-8');print('Wrote recovery UI, note editor, explicit commit root and onboarding integration; mission/profile/review integration pending')
