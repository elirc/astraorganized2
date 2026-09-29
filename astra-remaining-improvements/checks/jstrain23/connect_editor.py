from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'src/components/WorkspaceApp.js'
t=p.read_text(encoding='utf-8')
t=t.replace('useCallback, useEffect','useEffect')
t=t.replace('import { saveDraft, readDraft, queueSync, readSyncQueue, removeQueuedSync } from "@/lib/offlineStore";', '''import { readLegacyDrafts } from "@/lib/offlineStore";
import { createWorkspaceClient, downloadFile } from "@/lib/workspaceClient.mjs";
import { useWorkspaceConnection } from "./useWorkspaceConnection";''')
start=t.index('export default function WorkspaceApp() {')
t=t[:start]+'''const actions=useWorkspaceStore.getState();

function DraftReview({session,review}) {
  const [choices,setChoices]=useState({});
  const result=session.previewReview(choices);
  const show=value=>value?.present?JSON.stringify(value.value,null,2):'(removed)';
  return <section className="draft-review" aria-label="Draft review">
    <h2>Review your draft against the accepted workspace</h2>
    <p>Independent changes are combined. Choose a value for each conflict. Accepting this review keeps a draft; use Save to submit it.</p>
    {review.result.conflicts.map(conflict=><fieldset key={conflict.path}><legend>{conflict.path}</legend>
      <details><summary>Common starting value</summary><pre>{show(conflict.base)}</pre></details>
      {['local','remote'].map(side=><label key={side}><input type="radio" name={conflict.path} value={side} checked={choices[conflict.path]===side} onChange={()=>setChoices({...choices,[conflict.path]:side})}/>{side==='local'?'Your draft':'Accepted server value'}<pre>{show(conflict[side])}</pre></label>)}
    </fieldset>)}
    {result.validationError&&<p role="alert">{result.validationError}</p>}
    {!result.conflicts.length&&<p>No competing edits were found.</p>}
    <button disabled={!result.ready} onClick={()=>session.acceptReview(choices)}>Accept reviewed draft</button>
  </section>;
}

export default function WorkspaceApp(){
  const [connection,setConnection]=useState(null),[token,setToken]=useState(''),[message,setMessage]=useState(''),[busy,setBusy]=useState(false);
  async function signIn(event){event.preventDefault();setBusy(true);setMessage('');
    try{const api=createWorkspaceClient(token.trim());const snapshot=await api('/api/workspace');setToken('');setConnection({api,snapshot});}
    catch(error){setMessage(error.message);}finally{setBusy(false);}
  }
  if(connection)return <ConnectedWorkspace connection={connection} onSignOut={()=>{actions.reset();setConnection(null);}}/>;
  return <main className="login-shell"><h1>Knowledge Workspace</h1><p>A local owner workspace for pages, blocks, comments and structured records.</p>
    <p>Run <code>npm run setup -- --owner "Your name"</code> in this project first. Keep the printed owner token somewhere private, then enter it here. It stays in memory for this tab.</p>
    <form onSubmit={signIn}><label>Owner token<input type="password" autoComplete="off" required pattern="[a-fA-F0-9]{64}" value={token} onChange={event=>setToken(event.target.value)} /></label><button disabled={busy}>{busy?'Opening…':'Open workspace'}</button></form>
    {message&&<p role="alert">{message}</p>}
  </main>;
}

function ConnectedWorkspace({connection,onSignOut}) {
''' +t[start+len('export default function WorkspaceApp() {'):]
t=t.replace('    pendingSaves,\n    lastSavedAt,','')
t=t.replace('  const store = useWorkspaceStore();','  const store = useWorkspaceStore();\n  const sync=useWorkspaceConnection(connection);')
t=t.replace('  const clientIdRef = useRef(nanoid());\n  const syncTimerRef = useRef(null);\n  const searchTimerRef = useRef(null);','  const [clientId] = useState(()=>nanoid());')
t=t.replace('clientIdRef.current','clientId')
t=t.replace('  const [selectedVersion, setSelectedVersion] = useState(null);','  const [selectedVersion, setSelectedVersion] = useState(null);\n  const [historyPage,setHistoryPage]=useState({pageId:"",page:1,total:0});')
t=t.replace('key !== clientId && value.pageId === activePageId','key !== clientId && value.pageId === activePageId')
t=t.replace('[presence, activePageId]','[presence, activePageId, clientId]')
start=t.index('  const serializableState = useMemo(')
end=t.index('  const onDragEnd = (event)',start)
t=t[:start]+'''  useEffect(()=>{
    const keydown=event=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();actions.setCommandPaletteOpen(!useWorkspaceStore.getState().commandPaletteOpen);}if(event.key==='Escape'){actions.setCommandPaletteOpen(false);setImportOpen(false);}};
    window.addEventListener('keydown',keydown);return()=>window.removeEventListener('keydown',keydown);
  },[]);
  useEffect(()=>{
    if(!loaded||typeof BroadcastChannel==='undefined')return;
    const channel=new BroadcastChannel('knowledge-presence:'+connection.snapshot.instanceId);channelRef.current=channel;
    channel.onmessage=event=>{const data=event.data;if(!data||data.clientId===clientId)return;if(data.type==='presence')actions.setPresence(data.payload);if(data.type==='typing')actions.setTyping(data.payload);};
    const send=()=>{channel.postMessage({type:'presence',clientId,payload:{clientId,pageId:activePageId,userId:currentUser.id,name:currentUser.name,color:currentUser.color}});actions.prunePresence();actions.pruneTyping();};send();
    const timer=setInterval(send,4000);return()=>{clearInterval(timer);channel.close();channelRef.current=null;};
  },[loaded,connection,clientId,activePageId,currentUser.id,currentUser.name,currentUser.color]);
  useEffect(()=>{
    let active=true;const controller=new AbortController();
    const timer=setTimeout(async()=>{
      if(!commandPaletteOpen||!commandPaletteQuery.trim()){if(active)setSearchResults([]);return;}
      try{const result=await connection.api('/api/search?q='+encodeURIComponent(commandPaletteQuery),{signal:controller.signal});if(active)setSearchResults(result.results);}
      catch(error){if(active){setSearchResults([]);actions.setError(error.message);}}
    },180);
    return()=>{active=false;clearTimeout(timer);controller.abort();};
  },[connection,commandPaletteOpen,commandPaletteQuery]);

''' +t[end:]
start=t.index('  const loadVersions = async () => {')
end=t.index('  return (\n    <main className="workspace-shell">',start)
t=t[:start]+'''  const loadVersions = async (page=1) => {
    if(!activePageId)return;
    try{const payload=await connection.api(`/api/workspace/version?pageId=${activePageId}&page=${page}`);actions.setVersionsForPage(activePageId,payload.versions);setHistoryPage({pageId:activePageId,page:payload.page,total:payload.total});}
    catch(error){actions.setError(error.message);}
  };
  const captureSnapshot=async()=>{if(!activePageId)return;const result=await sync.session.current.operation(revision=>connection.api('/api/workspace',{method:'POST',body:{pageId:activePageId},revision}));if(result)await loadVersions();};
  const selectVersion=async versionId=>{try{const payload=await connection.api('/api/workspace/version?versionId='+versionId);setSelectedVersion(payload.version);}catch(error){actions.setError(error.message);}};
  const restoreVersion=async versionId=>{if(!window.confirm('Replace this page content and comments with the snapshot? Current hierarchy and visibility labels stay the same.'))return;const result=await sync.session.current.operation(revision=>connection.api('/api/workspace/version',{method:'PATCH',body:{versionId},revision}));if(result)setSelectedVersion(null);};
  const deleteVersion=async versionId=>{if(!window.confirm('Permanently delete this snapshot? The current page stays unchanged.'))return;const result=await sync.session.current.operation(revision=>connection.api('/api/workspace/version',{method:'DELETE',body:{versionId},revision}));if(result){setSelectedVersion(null);await loadVersions();}};
  const importMarkdown=async()=>{if(!importText.trim())return;const result=await sync.session.current.operation(revision=>connection.api('/api/import/markdown',{method:'POST',body:{title:importTitle,markdown:importText,parentId:activePageId||null},revision}));if(result){actions.setActivePage(result.pageId);setImportOpen(false);setImportText('');}};
  const exportAccepted=async format=>{try{const path=format==='json'?'/api/export/json':`/api/export/${format}?pageId=${activePageId}`;downloadFile(await connection.api(path,{blob:true}),format==='json'?'workspace.json':`page.${format==='markdown'?'md':'html'}`);}catch(error){actions.setError(error.message);}};
  const exportLegacy=async()=>{try{const value=await readLegacyDrafts();if(value)downloadFile(value,'legacy-offline-drafts.json');else actions.setError('No legacy offline drafts were found in this browser.');}catch(error){actions.setError(error.message);}};
  const signOut=async()=>{if(sync.status.busy){actions.setError('Wait for the current request before signing out.');return;}if((sync.status.dirty||sync.status.needsReview)&&!window.confirm('Sign out with unsaved edits? Your local draft will be retained if browser storage is available. Download it first if needed.'))return;await sync.session.current.retain();if(sync.session.current.getSnapshot().warning){actions.setError('Local storage failed. Download the draft before signing out.');return;}onSignOut();};
  if(!loaded||loading||!sync.localReady)return <main className="loading-shell">Loading accepted workspace and checking local drafts…</main>;

''' +t[end:]
t=t.replace('<main className="workspace-shell">','''<div>
    <section className="sync-toolbar" aria-label="Save and recovery controls">
      <p role="status"><strong>{sync.status.phase}</strong>: {sync.status.message}</p>
      {sync.status.warning&&<p role="alert">{sync.status.warning}</p>}
      {error&&<p role="alert">{error} <button onClick={()=>actions.setError('')}>Dismiss</button></p>}
      {sync.remoteNotice&&<p>Another tab accepted changes. Review the latest workspace before your next save.</p>}
      <div><button disabled={sync.status.busy||sync.status.needsReview||Boolean(sync.recovery)} onClick={()=>sync.session.current.save()}>Save</button>
      <button disabled={sync.status.busy||Boolean(sync.recovery)} onClick={sync.review}>Review latest</button>
      <button onClick={()=>downloadFile({base:sync.session.current.accepted,state:sync.session.current.draft},'local-workspace-draft.json')}>Download local draft</button>
      <button disabled={sync.status.busy||Boolean(sync.recovery)} onClick={()=>{if(window.confirm('Discard the local draft and load accepted state?'))sync.session.current.reloadAccepted();}}>Discard draft</button>
      <button onClick={()=>exportAccepted('json')}>Export accepted JSON</button><button onClick={exportLegacy}>Export legacy drafts</button><button disabled={sync.status.busy} onClick={signOut}>Sign out</button></div>
      {sync.recovery&&<section aria-label="Saved local draft"><h2>Saved local draft found</h2><p>Review it before editing. It will not be replayed automatically.</p><button onClick={sync.recover}>Review saved draft</button><button onClick={()=>downloadFile(sync.recovery,'saved-workspace-draft.json')}>Download saved draft</button><button onClick={()=>{if(window.confirm('Discard this saved local draft?'))sync.discardRecovery();}}>Discard saved draft</button></section>}
      {sync.status.review&&<DraftReview key={sync.status.review.latest.revision+sync.status.review.base.revision} session={sync.session.current} review={sync.status.review}/>}
    </section>
    <main className="workspace-shell" inert={Boolean(sync.recovery)||['operation','reviewing','reloading'].includes(sync.status.phase)}>''')
t=t.replace('    </main>\n  );\n}', '    </main></div>\n  );\n}')
t=t.replace('<h2>Notion Clone</h2>','<h2>Knowledge Workspace</h2>')
start=t.index('                <span className="save-status">')
end=t.index('                <button onClick={captureSnapshot}>',start)
t=t[:start]+'''                <button onClick={()=>exportAccepted('markdown')}><FiDownload/> Accepted MD</button>
                <button onClick={()=>exportAccepted('html')}><FiDownload/> Accepted HTML</button>
''' +t[end:]
t=t.replace('<button onClick={loadVersions}>Versions</button>','<button onClick={()=>loadVersions()}>Versions</button>')
t=t.replace('<option value="public">Public link</option>','<option value="public">Public label (owner only)</option>')
t=t.replace('<option value="workspace">Workspace</option>','<option value="workspace">Workspace label (owner only)</option>')
t=t.replace('<select value={activePage.shared','<select aria-label="Visibility label; all pages remain owner only" value={activePage.shared')
t=t.replace('onClick={() => store.softDeletePage(activePage.id)}','aria-label="Move page and descendants to trash" onClick={() => {if(window.confirm("Move this page and all descendants to trash?"))store.softDeletePage(activePage.id);}}')
t=t.replace('onClick={() => store.toggleFavorite(activePage.id)}','aria-label="Toggle favorite" onClick={() => store.toggleFavorite(activePage.id)}')
t=t.replace('className="page-icon"','aria-label="Page icon" maxLength={16} className="page-icon"')
t=t.replace('className="page-title"','aria-label="Page title" maxLength={200} className="page-title"')
t=t.replace('<select value={activePage.parentId','<select aria-label="Parent page" value={activePage.parentId')
t=t.replace('{activePage.coverImage && (','{/^https:\\/\\/[^\\s]+$/.test(activePage.coverImage||"") && (()=>{try{const url=new URL(activePage.coverImage);return !url.username&&!url.password;}catch{return false;}})() && (')
t=t.replace('className="cover-input"','aria-label="HTTPS cover image URL" maxLength={2048} className="cover-input"')
t=t.replace('onDelete={(blockId) => store.removeBlock({ pageId: activePage.id, blockId })}','onDelete={(blockId) => {if(!pageThreads.some(thread=>thread.blockId===blockId)||window.confirm("Delete this block and its comments?"))store.removeBlock({ pageId: activePage.id, blockId });}}')
t=t.replace('No teammates on this page.','No other local tabs on this page.')
t=t.replace('<FiUsers /> Presence','<FiUsers /> Local tab presence')
t=t.replace('<h3>Version History</h3>','''<h3>Version History</h3>
          {historyPage.pageId===activePageId&&<div><span>{historyPage.total} snapshots; page {historyPage.page}</span><button disabled={historyPage.page<=1} onClick={()=>loadVersions(historyPage.page-1)}>Previous snapshots</button><button disabled={historyPage.page*20>=historyPage.total} onClick={()=>loadVersions(historyPage.page+1)}>Next snapshots</button></div>}''')
t=t.replace('{selectedVersion && (','{selectedVersion?.pageId===activePageId && (')
t=t.replace('                Restore this version\n              </button>','                Restore this version\n              </button>\n              <button className="inline-btn danger" onClick={()=>deleteVersion(selectedVersion.id)}>Delete this snapshot</button>')
t=t.replace('                    <strong>{users.find((user) => user.id === comment.authorId)?.name || "User"}:</strong> {comment.content}','''                    <strong>{users.find((user) => user.id === comment.authorId)?.name || "User"}:</strong> {comment.content}
                    <button aria-label="Edit comment" onClick={()=>{const content=window.prompt('Edit comment',comment.content);if(content!==null)actions.editComment({commentId:comment.id,content});}}>Edit</button>
                    <button aria-label="Delete comment" onClick={()=>{if(window.confirm('Delete this comment?'))actions.removeComment(comment.id);}}>Delete</button>''')
t=t.replace('                <span>Block {thread.blockId.slice(0, 6)}</span>','                <span>Block {thread.blockId.slice(0, 6)}</span><button onClick={()=>{if(window.confirm("Delete this thread and all replies?"))actions.removeThread(thread.id);}}>Delete thread</button>')
t=t.replace('className="block-type-select"','aria-label="Block type" className="block-type-select"')
t=t.replace('className={`block-input','aria-label={`${mapBlockTypeLabel(block.type)} text`} maxLength={50000} className={`block-input')
t=t.replace('className="inline-btn" onClick={() => onComment(block.id)}','aria-label="Comment on block" className="inline-btn" onClick={() => onComment(block.id)}')
t=t.replace('className="inline-btn danger" onClick={() => onDelete(block.id)}','aria-label="Delete block" className="inline-btn danger" onClick={() => onDelete(block.id)}')
t=t.replace('input autoFocus value={query}','input aria-label="Search accepted workspace" autoFocus value={query} maxLength={200}')
t=t.replace('<input value={importTitle}','<input aria-label="Import page title" maxLength={200} value={importTitle}')
t=t.replace('<textarea value={importText}','<textarea aria-label="Markdown to import" maxLength={500000} value={importText}')
p.write_text(t,encoding='utf-8')
