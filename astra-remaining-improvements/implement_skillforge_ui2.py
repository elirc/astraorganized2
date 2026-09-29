from pathlib import Path
s=Path(__file__).resolve().parent/'stage/a9672affc47e';p=s/'src/App.tsx';t=p.read_text(encoding='utf-8')
start=t.index('function MissionScreen(');end=t.index('function CodeLab(',start);part=t[start:end]
part=part.replace('  onNext,','  onNext,\n  onDirty,').replace('onProgress: (p: GameProgress) => void;','onProgress: (p: GameProgress) => Promise<GameProgress>;\n  onDirty: (dirty: boolean) => void;')
part=part.replace('  const [content, setContent] = useState<MissionContent>();','''  const [content, setContent] = useState<MissionContent>();
  const [contentError,setContentError] = useState<string>();
  const [contentReload,setContentReload] = useState(0);
  const [draftProgress,setDraftProgress] = useState(progress);
  const [busy,setBusy] = useState(false);
  const updateDraft = (next:GameProgress) => {setDraftProgress(next);onDirty(true);};
  useEffect(()=>()=>onDirty(false),[onDirty]);
  async function saveDrafts(){if(busy)return;setBusy(true);try{setDraftProgress(await onProgress(draftProgress));onNotice('Mission drafts saved.');}catch(e){onNotice((e as Error).message);}finally{setBusy(false);}}
''')
a=part.index('  useEffect(() => {\n    setContent(undefined);');z=part.index('  if (!content)',a)
part=part[:a]+'''  useEffect(() => {
    const controller=new AbortController();setContent(undefined);setContentError(undefined);
    fetch(`/content/${mission.contentFile}`,{signal:controller.signal})
      .then(r=>{if(!r.ok)throw new Error('This mission could not be loaded.');return r.json();})
      .then((data:MissionContent)=>{if(data.id!==mission.id||!Array.isArray(data.files)||!data.files.length)throw new Error('This mission archive is invalid.');setContent(data);const preferred=data.files.find(f=>/LEARN\\.md$/i.test(f.path))||data.files.find(f=>/README\\.md$/i.test(f.path))||data.files[0];setActivePath(preferred.path);})
      .catch(e=>{if(e.name!=='AbortError')setContentError(e.message);});
    return()=>controller.abort();
  },[mission,contentReload]);
'''+part[z:]
part=part.replace('<div className="mission-loading">Decrypting mission archive…</div>','''<div className="mission-loading">{contentError||'Decrypting mission archive…'}</div>
        {contentError&&<><p role="alert">{contentError}</p><button onClick={()=>setContentReload(v=>v+1)}>Retry mission</button><button onClick={onBack}>Back to journey</button></>}''')
# These occurrences are restricted to MissionScreen; CodeLab edits only the local mission draft.
part=part.replace('progress={progress}\n            onProgress={onProgress}', 'progress={draftProgress}\n            onProgress={updateDraft}\n            disabled={busy}')
part=part.replace('const response = progress.responses[key] || "";', 'const response = draftProgress.responses[key] || "";')
part=part.replace('disabled={done}', 'disabled={done || busy}\n                  maxLength={100000}')
part=part.replace('''                    onProgress(
                      saveResponse(
                        progress,''','''                    updateDraft(
                      saveResponse(
                        draftProgress,''')
part=part.replace('done || response.trim().length < challenge.minLength','done || busy || response.trim().length < challenge.minLength')
part=part.replace('''                    onClick={() => {
                      try {
                        const updated = completeChallenge(
                          progress,''','''                    onClick={async () => {
                      if(busy)return;setBusy(true);
                      try {
                        const updated = completeChallenge(
                          draftProgress,''')
part=part.replace('                        onProgress(updated);','                        const accepted = await onProgress(updated);\n                        setDraftProgress(accepted);')
part=part.replace('''                      } catch (error) {
                        onNotice((error as Error).message);
                      }
                    }}''','''                      } catch (error) {
                        onNotice((error as Error).message);
                      } finally {setBusy(false);}
                    }}''')
# Put the explicit save action before the lesson/lab panes.
needle='  return (\n    <div className="page mission-page">';assert needle in part
part=part.replace(needle,needle+'''\n      <section className="mission-draft-bar"><p>Answers and scratch code are drafts. Save them here; submitting a checkpoint also saves this mission's drafts. Checkpoints are self-reported evidence, not automatic correctness grading.</p><button className="primary-button" disabled={busy} onClick={()=>void saveDrafts()}>{busy?'Saving…':'Save mission drafts'}</button></section>''',1)
t=t[:start]+part+t[end:]
# Review success is reported only after persistence, and failed answers stay in the form.
start=t.index('function Reviews(');end=t.index('function Profile(',start);part=t[start:end].replace('onProgress: (p: GameProgress) => void;','onProgress: (p: GameProgress) => Promise<GameProgress>;')
a=part.index('''                        onClick={() => {
                          onProgress(''');z=part.index('\n                        }}',a)
part=part[:a]+'''                        onClick={async () => {
                          try {
                            await onProgress(reviewMission(progress,mission.id,rating));
                            setAnswers({...answers,[mission.id]:''});
                            onNotice(`${rating.toUpperCase()} recorded. Next review scheduled.`);
                          } catch(error){onNotice((error as Error).message);}'''+part[z:]
t=t[:start]+part+t[end:]
# Import validates first, then asks to replace the captured baseline. Local note drafts are reset only after acceptance.
start=t.index('function Profile(');end=t.index('const isReferenceFile',start);part=t[start:end].replace('  onNotice,','  onNotice,\n  onDirty,\n  onImported,').replace('onProgress: (p: GameProgress) => void;','onProgress: (p: GameProgress) => Promise<GameProgress>;\n  onDirty: (dirty: boolean) => void;\n  onImported: () => void;')
old='''                  onProgress(parseProgressExport(await file.text()));
                  onNotice("Save imported successfully.");'''
new='''                  if(file.size>MAX_SAVE_BYTES)throw new Error('Import exceeds the 4 MiB file limit.');
                  const imported=validateAgainstCatalog(parseProgressExport(await file.text()),catalog);
                  if(!confirm(`Replace saved progress and open drafts with ${imported.completedMissions.length} completed missions and ${imported.notes.length} notes? Export a backup first.`))return;
                  await onProgress({...imported,revision:progress.revision,epoch:progress.epoch});
                  onImported();onNotice("Save imported successfully.");''';assert old in part;part=part.replace(old,new)
part=part.replace('''                } catch (error) {
                  onNotice((error as Error).message);
                }
              }}''','''                } catch (error) {
                  onNotice((error as Error).message);
                } finally {event.target.value='';}
              }}''')
pos=part.rfind('''    </div>
  );''');assert pos!=-1;part=part[:pos]+'''      <LearningNotes catalog={catalog} progress={progress} onProgress={onProgress} onDirty={onDirty}/>
'''+part[pos:]
t=t[:start]+part+t[end:]
# Replace the lab implementation with a lifecycle-managed worker while keeping its local draft callback.
start=t.index('function CodeLab(');end=t.index('function Reviews(',start)
lab='''function CodeLab({mission,progress,onProgress,disabled=false}:{mission:Mission;progress:GameProgress;onProgress:(progress:GameProgress)=>void;disabled?:boolean}) {
 const saved=progress.responses[challengeKey(mission.id,'code-lab')];
 const starter=`// ${mission.title}\\n// Make a small claim, then test it.\\nconsole.assert(2 + 2 === 4, "Addition should work");\\nconsole.log("Experiment complete");`;
 const code=saved??starter;const [output,setOutput]=useState('Run the lab to see output.');const [running,setRunning]=useState(false);const cancel=useRef<(()=>void)|null>(null);
 useEffect(()=>()=>cancel.current?.(),[]);
 const run=()=>{cancel.current?.();setRunning(true);cancel.current=startLab(code,result=>{setRunning(false);setOutput(`${result.ok?'COMPLETED':'ERROR'}\\n${result.lines.join('\\n')||'(no output)'}`);});};
 return <section className="code-lab"><div className="code-lab-heading"><div><span className="eyebrow">ACTIVE LAB</span><h3>Test the idea in JavaScript</h3><p>Scratch code stays in this mission's draft until you save it. Include assertions and edge cases; a completed run alone does not prove correctness.</p></div><button onClick={run} disabled={running||disabled}>{running?'Running…':'Run code ▶'}</button></div><div className="code-lab-grid"><textarea aria-label="JavaScript scratch lab" spellCheck={false} disabled={disabled} maxLength={100000} value={code} onChange={event=>onProgress(saveResponse(progress,mission.id,'code-lab',event.target.value))}/><pre aria-live="polite">{output}</pre></div></section>;
}

'''
t=t[:start]+lab+t[end:];t=t.replace('import { LearningNotes } from "./components/LearningNotes";','import { LearningNotes } from "./components/LearningNotes";\nimport { startLab } from "./game/lab";')
p.write_text(t,encoding='utf-8')
(s/'src/game/lab.ts').write_text('''export type LabResult={ok:boolean;lines:string[]};
// This is a local execution helper, not a security boundary or automated grader.
export const workerSource = `self.onmessage = async ({data}) => {
 const lines=[];let total=0;let truncated=false;let assertionFailed=false;
 const show=value=>{try{return (typeof value==='string'?value:JSON.stringify(value)??String(value)).slice(0,2000);}catch{return '[unprintable value]';}};
 const add=(...args)=>{if(lines.length>=100||total>=50000){truncated=true;return;}const line=args.slice(0,20).map(show).join(' ').slice(0,Math.min(2000,50000-total));lines.push(line);total+=line.length;};
 console.log=add;console.error=(...args)=>add('ERROR:',...args);console.assert=(condition,...args)=>{if(!condition){assertionFailed=true;add('ASSERTION FAILED:',...args);}};
 let ok=true;try{const result=await (0,eval)(data);if(result!==undefined)add('RETURN:',result);}catch(error){ok=false;add(error?.name||'Error',error?.message||String(error));}
 if(truncated)lines.push('[Output truncated after 100 lines or 50,000 characters.]');
 self.postMessage({ok:ok&&!assertionFailed,lines});
};`;
export function startLab(code:string,receive:(result:LabResult)=>void):()=>void {
 let worker:Worker|undefined;let url:string|undefined;let timer:ReturnType<typeof setTimeout>|undefined;let done=false;
 const cleanup=()=>{if(timer)clearTimeout(timer);worker?.terminate();if(url)URL.revokeObjectURL(url);};
 const finish=(result:LabResult)=>{if(done)return;done=true;cleanup();receive(result);};
 try{
  if(code.length>100000)throw new Error('Lab code exceeds 100,000 characters.');
  url=URL.createObjectURL(new Blob([workerSource],{type:'text/javascript'}));worker=new Worker(url);
  timer=setTimeout(()=>finish({ok:false,lines:['Timeout: the lab stopped after 2.5 seconds. Check for an infinite loop.']}),2500);
  worker.onerror=event=>{event.preventDefault();finish({ok:false,lines:['Worker error: '+event.message.slice(0,2000)]});};
  worker.onmessage=event=>{const data=event.data;if(!data||typeof data.ok!=='boolean'||!Array.isArray(data.lines)||data.lines.length>101||data.lines.some((line:unknown)=>typeof line!=='string'||line.length>2000)){finish({ok:false,lines:['The lab returned an invalid result.']});return;}finish(data as LabResult);};
  worker.postMessage(code);
 }catch(error){finish({ok:false,lines:[(error as Error).message]});}
 return()=>{if(done)return;done=true;cleanup();};
}
''',encoding='utf-8')
css='''
/* Explicit save boundaries and mission-linked learning notes. */
.save-panel{margin:18px 0 26px;padding:18px 20px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}.save-panel strong{color:var(--cyan);font-size:.85rem}.save-panel p,.mission-draft-bar p{color:var(--muted);font-size:.8rem;line-height:1.6;margin:8px 0}.save-fault{border-color:var(--amber)}.save-error{color:var(--rose)!important;white-space:pre-wrap;overflow-wrap:anywhere}.save-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.save-actions button,.notes-pages button,.mission-loading+button{border:1px solid var(--line);background:var(--surface-2);border-radius:8px;padding:10px 12px;cursor:pointer;font-size:.8rem}.save-actions button:disabled,.notes-pages button:disabled{opacity:.45;cursor:not-allowed}.startup-save,.save-recovery{max-width:1100px;margin:24px auto;padding:0 22px}.save-recovery{padding-top:45px}.mission-draft-bar{padding:18px;background:var(--surface);border:1px solid var(--line);border-radius:12px;margin:20px 0}.mission-draft-bar button{margin-top:10px}.learning-notes{margin-top:28px}.notes-heading{display:flex;justify-content:space-between;align-items:center;gap:20px}.notes-heading p,.note-editor p{font-size:.85rem;color:var(--muted);line-height:1.6}.learning-notes label{display:block;font-size:.85rem;margin:14px 0;color:var(--text)}.learning-notes input,.learning-notes textarea,.learning-notes select{display:block;width:100%;margin-top:8px;padding:12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--text);font:inherit}.learning-notes select:focus-visible{outline:3px solid var(--cyan);outline-offset:2px}.learning-notes fieldset{padding:0;border:0;min-width:0}.note-editor{padding:20px;border:1px solid var(--cyan);border-radius:10px;margin:20px 0}.note-cards{display:grid;gap:16px;margin-top:22px}.note-card{border:1px solid var(--line);padding:20px;border-radius:10px;background:var(--surface-2);min-width:0}.note-card h3{overflow-wrap:anywhere;margin:0 0 9px}.note-card p{font-size:.85rem;line-height:1.6}.note-preview,.note-body{white-space:pre-wrap;overflow-wrap:anywhere}.note-card summary{cursor:pointer;color:var(--cyan);font-size:.85rem}.notes-pages{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:22px}.notes-pages span{font-size:.8rem;color:var(--muted);margin-right:auto}.notes-empty{color:var(--muted);padding:20px 0}@media(max-width:700px){.notes-heading{align-items:flex-start;flex-direction:column}.save-actions button{max-width:100%;white-space:normal;overflow-wrap:anywhere}.note-editor,.note-card{padding:15px}.notes-pages span{width:100%}.save-panel{padding:16px}.startup-save{padding:0 14px}.learning-notes{min-width:0}}
'''
p=s/'src/styles.css';p.write_text(p.read_text(encoding='utf-8')+css,encoding='utf-8');print('Integrated mission drafts, confirmed imports, persisted review success, retryable content fetches and bounded lab lifecycle')
