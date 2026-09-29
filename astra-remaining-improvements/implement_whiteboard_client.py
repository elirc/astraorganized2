from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
(P/'client/src/App.tsx').write_text(r'''import { useCallback, useEffect, useRef, useState } from 'react';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';
import './index.css';

type DocumentInfo = { id: string; title: string; version: number; createdAt: string; updatedAt: string; characters: number };
type Session = { doc: Y.Doc; text: Y.Text; provider: WebsocketProvider };
type Person = { id: number; name: string; color: string };
const syncUrl = (import.meta.env.VITE_SYNC_URL || 'ws://127.0.0.1:1234').replace(/\/$/, '');
const apiUrl = syncUrl.replace(/^ws/, 'http');
const validId = (value: string) => /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/.test(value);
function rememberedRoom() {
  try { const value = localStorage.getItem('collab-room'); return value && validId(value) ? value : 'welcome'; }
  catch { return 'welcome'; }
}
async function request<T>(path: string, method = 'GET', input?: unknown, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, { method, signal, headers: input === undefined ? undefined : { 'Content-Type': 'application/json' }, body: input === undefined ? undefined : JSON.stringify(input) });
  if (!response.ok) {
    const result = await response.json().catch(() => ({ error: 'Server request failed.' }));
    throw new Error(result.error || 'Server request failed.');
  }
  return response.status === 204 ? undefined as T : response.json();
}
function replaceText(session: Session, next: string) {
  const previous = session.text.toString();
  let prefix = 0; let suffix = 0;
  while (prefix < previous.length && prefix < next.length && previous[prefix] === next[prefix]) prefix++;
  while (suffix < previous.length - prefix && suffix < next.length - prefix && previous[previous.length - 1 - suffix] === next[next.length - 1 - suffix]) suffix++;
  session.doc.transact(() => {
    const removed = previous.length - prefix - suffix;
    if (removed) session.text.delete(prefix, removed);
    const inserted = next.slice(prefix, next.length - suffix);
    if (inserted) session.text.insert(prefix, inserted);
  }, 'editor-input');
}

export default function App() {
  const [room, setRoom] = useState(rememberedRoom);
  const [roomInput, setRoomInput] = useState(room);
  const [generation, setGeneration] = useState(0);
  const [text, setText] = useState('');
  const [status, setStatus] = useState('Connecting');
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [current, setCurrent] = useState<DocumentInfo | null>(null);
  const [title, setTitle] = useState('');
  const [name, setName] = useState('Editor');
  const [people, setPeople] = useState<Person[]>([]);
  const [search, setSearch] = useState('');
  const [replacement, setReplacement] = useState('');
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const sessionRef = useRef<Session | null>(null);
  const profileRef = useRef({ name: 'Editor', color: '#76d7c4' });
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const importRef = useRef<HTMLInputElement>(null);
  const refreshDocuments = useCallback(async () => {
    const result = await request<{ documents: DocumentInfo[] }>('/api/documents');
    setDocuments(result.documents);
  }, []);

  useEffect(() => {
    profileRef.current = { name: name.trim() || 'Editor', color: '#76d7c4' };
    sessionRef.current?.provider.awareness.setLocalStateField('user', profileRef.current);
  }, [name]);

  useEffect(() => {
    const controller = new AbortController();
    let active = true; let session: Session | null = null;
    async function connect() {
      try {
        const document = await request<DocumentInfo>('/api/documents', 'POST', { id: room }, controller.signal);
        if (!active) return;
        setCurrent(document); setTitle(document.title); setText(''); setPeople([]);
        try { localStorage.setItem('collab-room', room); } catch { /* The current session still works without browser storage. */ }
        const doc = new Y.Doc(); const shared = doc.getText('markdown-content');
        const provider = new WebsocketProvider(syncUrl, room, doc, { connect: false, disableBc: true });
        session = { doc, text: shared, provider }; sessionRef.current = session;
        const updateText = () => { if (active) setText(shared.toString()); };
        shared.observe(updateText);
        provider.on('status', ({ status: connection }: { status: string }) => {
          if (active) setStatus(connection === 'connected' ? 'Synchronizing' : 'Reconnecting');
        });
        provider.on('sync', (synced: boolean) => { if (active && synced) setStatus('Live'); });
        provider.on('connection-close', (event: CloseEvent | null) => {
          if (active && event?.code === 4004) {
            provider.disconnect(); setStatus('Deleted'); setCurrent(null);
            setError('This document was deleted. Join a different document ID.');
            void refreshDocuments().catch(() => {});
          }
        });
        const updatePeople = () => {
          if (!active) return;
          setPeople([...provider.awareness.getStates()].map(([id, state]) => ({ id, name: String(state.user?.name || 'Editor'), color: String(state.user?.color || '#76d7c4') })));
        };
        provider.awareness.on('change', updatePeople);
        provider.awareness.setLocalStateField('user', profileRef.current);
        updatePeople(); provider.connect();
        await refreshDocuments();
      } catch (failure) {
        if (active) { setStatus('Unavailable'); setCurrent(null); setError(failure instanceof Error ? failure.message : 'Could not open document.'); }
      }
    }
    void connect();
    return () => {
      active = false; controller.abort();
      if (sessionRef.current === session) sessionRef.current = null;
      session?.provider.destroy(); session?.doc.destroy();
    };
  }, [room, generation, refreshDocuments]);

  const editable = status === 'Live' && !busy;
  function join(id: string) {
    const next = id.trim();
    if (!validId(next)) { setError('Use 1–64 letters, numbers, underscores or hyphens for the room ID.'); return; }
    setError(''); setNotice(''); setStatus('Connecting'); setRoomInput(next); setRoom(next); setGeneration(value => value + 1);
  }
  function edit(next: string) {
    if (!editable || !sessionRef.current) return;
    replaceText(sessionRef.current, next);
  }
  async function rename() {
    if (!current) return;
    setBusy(true); setError('');
    try {
      const updated = await request<DocumentInfo>(`/api/documents/${current.id}`, 'PATCH', { title, version: current.version });
      setCurrent(updated); setTitle(updated.title); setNotice('Title saved.'); await refreshDocuments();
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : 'Rename failed.');
      // Refresh the expected version, while preserving the proposed title for review.
      const latest = await request<DocumentInfo>(`/api/documents/${current.id}`).catch(() => null);
      if (latest) setCurrent(latest);
    } finally { setBusy(false); }
  }
  async function remove() {
    if (!current || !window.confirm(`Delete “${current.title}”? This document ID cannot be reused.`)) return;
    setBusy(true); setError('');
    try {
      await request<void>(`/api/documents/${current.id}`, 'DELETE', { version: current.version });
      sessionRef.current?.provider.disconnect(); setStatus('Deleted'); setCurrent(null); setNotice('Document deleted. Join a new ID to continue.');
      await refreshDocuments();
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : 'Deletion failed.');
      const latest = await request<DocumentInfo>(`/api/documents/${current.id}`).catch(() => null);
      if (latest) setCurrent(latest);
    } finally { setBusy(false); }
  }
  function format(marker: string) {
    const input = textareaRef.current;
    if (!input || !editable) return;
    const start = input.selectionStart; const end = input.selectionEnd;
    edit(text.slice(0, start) + marker + text.slice(start, end) + marker + text.slice(end));
    input.focus();
  }
  async function copy() {
    try { await navigator.clipboard.writeText(text); setNotice('Markdown copied.'); }
    catch { setError('Clipboard access failed. Select and copy the editor text instead.'); }
  }
  function download() {
    const url = URL.createObjectURL(new Blob([text], { type: 'text/markdown;charset=utf-8' }));
    const link = document.createElement('a'); link.href = url; link.download = `${room}.md`; link.click(); URL.revokeObjectURL(url);
  }
  async function importFile(file?: File) {
    if (!file || !sessionRef.current || !editable) return;
    if (file.size > 256 * 1024) { setError('Import a Markdown file no larger than 256 KB.'); return; }
    const target = sessionRef.current;
    try {
      const content = await file.text();
      if (sessionRef.current === target && window.confirm('Replace this document with the imported Markdown?')) replaceText(target, content);
    } catch { setError('The selected file could not be read.'); }
    if (importRef.current) importRef.current.value = '';
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand-block"><p className="eyebrow">Shared writing workspace</p><h1>Collaborative Editor</h1><p>Write Markdown together and manage local documents.</p></div>
      <section className="sidebar-section"><div className="section-title"><h2>Documents</h2><button type="button" disabled={busy} onClick={() => void refreshDocuments().catch(() => setError('Could not refresh documents.'))}>Refresh</button></div>
        <div className="document-list">{documents.map(document => <button type="button" key={document.id} disabled={busy} className={`document-item ${room === document.id ? 'active' : ''}`} onClick={() => join(document.id)}><span>{document.title}</span><small>{document.id}</small></button>)}</div>
      </section>
      <label className="field">Your display name<input maxLength={50} value={name} onChange={event => setName(event.target.value)} /></label>
      <section className="sidebar-section"><h2>People here</h2><div className="presence-list" data-testid="presence-list">{people.map(person => <span className="presence-user" key={person.id}><span className="avatar" style={{ backgroundColor: person.color }}>{person.name.slice(0, 1)}</span>{person.name}</span>)}</div></section>
      <p className="session-note">Live means synchronized with the server. It is not a per-edit disk-save receipt.</p>
    </aside>
    <main className="main-area">
      <header className="topbar"><form className="room-controls" onSubmit={event => { event.preventDefault(); join(roomInput); }}><label className="room-field">Room name<input value={roomInput} disabled={busy} onChange={event => setRoomInput(event.target.value)} /></label><button className="primary-action" disabled={busy}>Join</button></form><span data-testid="connection-status" className={`connection-pill ${status === 'Live' ? 'connected' : 'disconnected'}`}>{status}</span></header>
      {error && <p role="alert" className="message error">{error}</p>}{notice && <p role="status" className="message">{notice}</p>}
      <section className="toolbar" aria-label="Document details"><label className="field">Document title<input value={title} maxLength={100} disabled={!current || busy} onChange={event => setTitle(event.target.value)} /></label><button disabled={!current || busy} onClick={() => void rename()}>Save title</button><button disabled={!current || busy} onClick={() => void remove()}>Delete document</button></section>
      <section className="toolbar" aria-label="Markdown tools"><button disabled={!editable} onClick={() => format('**')}>Bold</button><button disabled={!editable} onClick={() => format('*')}>Italic</button><button onClick={() => void copy()}>Copy Markdown</button><button onClick={download}>Download Markdown</button><button disabled={!editable} onClick={() => importRef.current?.click()}>Import Markdown</button><input aria-label="Import Markdown file" type="file" accept=".md,.markdown,.txt,text/plain,text/markdown" hidden ref={importRef} onChange={event => void importFile(event.target.files?.[0])} /></section>
      <section className="workspace" data-mode="split"><div className="panel editor-panel"><div className="panel-header"><h2>Markdown</h2><span>{text.length} characters</span></div><textarea aria-label="Markdown editor" data-testid="markdown-editor" ref={textareaRef} className="markdown-editor" value={text} disabled={!editable} onChange={event => edit(event.target.value)} placeholder="Start typing markdown here..." /></div><div className="panel preview-panel"><div className="panel-header"><h2>Preview</h2></div><div data-testid="markdown-preview" className="markdown-preview"><ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]} skipHtml>{text}</ReactMarkdown></div></div></section>
      <section className="utility-panel"><h2>Find and replace</h2><div className="find-row"><input aria-label="Search" placeholder="Search" value={search} onChange={event => setSearch(event.target.value)} /><input aria-label="Replace" placeholder="Replace" value={replacement} onChange={event => setReplacement(event.target.value)} /><button disabled={!editable || !search} onClick={() => edit(text.replace(search, () => replacement))}>First</button><button disabled={!editable || !search} onClick={() => edit(text.split(search).join(replacement))}>All</button></div></section>
    </main>
  </div>;
}
''',encoding='utf-8')
p=P/'client/src/index.css';s=p.read_text();s+='''\n/* Connection and command feedback for the implemented document workflow. */
button:disabled, textarea:disabled { cursor: not-allowed; opacity: 0.65; }
.message { margin: 0; padding: 12px 16px; border: 1px solid var(--line); border-radius: 8px; }
.message.error { color: var(--danger); }
.session-note { color: var(--muted); font-size: 0.85rem; line-height: 1.5; }
.toolbar .field { flex: 1; min-width: 180px; }
@media (max-width: 520px) { .find-row { grid-template-columns: 1fr; } .room-controls { flex-wrap: wrap; } }
''';p.write_text(s,encoding='utf-8')
