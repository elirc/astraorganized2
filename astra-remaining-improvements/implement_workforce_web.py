from pathlib import Path
s=Path(__file__).resolve().parent/'stage/56044dcd81ce'
files={
'apps/web/vite.config.ts':'''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],server:{host:'127.0.0.1',port:5173,strictPort:true,proxy:{'/api':process.env.API_TARGET??'http://127.0.0.1:3000'}}});
''',
'apps/web/src/api.ts':'''export class ApiError extends Error {constructor(message:string,public status:number,public requestId?:string){super(message);}}
export async function request<T>(path:string,token:string,method='GET',body?:unknown):Promise<T>{
 const response=await fetch(`/api${path}`,{method,headers:{...(token?{Authorization:`Bearer ${token}`} : {}),...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});
 const value=await response.json().catch(()=>({error:'The server returned an unreadable response.'}));
 if(!response.ok)throw new ApiError(value.error??'Request failed.',response.status,value.requestId);return value;
}
export type Actor={id:string;tenantId:string;email:string;role:string;tenantName:string};
export type Company={id:string;name:string};
export type Profile={firstName:string;lastName:string;email:string;companyId:string;countryCode:string;jobTitle:string;department:string};
export type Worker=Profile & {id:string;version:number;employmentStatus:string;company:Company};
export type Audit={id:string;action:string;entityId:string;actorUserId:string;createdAt:string};
export type Page={items:Worker[];total:number;page:number;limit:number};
export const moves:Record<string,string[]>={DRAFT:['ONBOARDING'],ONBOARDING:['ACTIVE','TERMINATED'],ACTIVE:['PAUSED','TERMINATED'],PAUSED:['ACTIVE','TERMINATED'],TERMINATED:[]};
export const profileOf=(w:Worker):Profile=>({firstName:w.firstName,lastName:w.lastName,email:w.email,companyId:w.companyId,countryCode:w.countryCode,jobTitle:w.jobTitle??'',department:w.department??''});
''',
'apps/web/src/App.tsx':'''import { useEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { ApiError, moves, profileOf, request } from './api';
import type { Actor, Audit, Company, Page, Profile, Worker } from './api';
import './App.css';
type Session={token:string;actor:Actor};
const empty=(companyId=''):Profile=>({firstName:'',lastName:'',email:'',companyId,countryCode:'US',jobTitle:'',department:''});
function App(){
 const [session,setSession]=useState<Session|null>(null);const [email,setEmail]=useState('client.admin@acme.example.com');const [password,setPassword]=useState('');
 const [data,setData]=useState<Page>({items:[],total:0,page:1,limit:20});const [companies,setCompanies]=useState<Company[]>([]);const [audit,setAudit]=useState<Audit[]>([]);
 const [page,setPage]=useState(1);const [search,setSearch]=useState('');const [query,setQuery]=useState('');const [status,setStatus]=useState('');
 const [editing,setEditing]=useState<Worker|null>(null);const [draft,setDraft]=useState<Profile>(empty());const [formOpen,setFormOpen]=useState(false);
 const [busy,setBusy]=useState(false);const [loading,setLoading]=useState(false);const [error,setError]=useState('');const [notice,setNotice]=useState('');const [reload,setReload]=useState(0);const generation=useRef(0);
 function failure(e:unknown){setError(e instanceof ApiError?`${e.message}${e.requestId?` (reference ${e.requestId})`:''}`:e instanceof Error?e.message:'Request failed.');}
 useEffect(()=>{
  if(!session)return;const ticket=++generation.current;let active=true;
  async function load(){setLoading(true);try{const qs=new URLSearchParams({page:String(page),limit:'20',q:query});if(status)qs.set('status',status);
   const [workers,choices,events]=await Promise.all([request<Page>(`/workers?${qs}`,session!.token),request<Company[]>('/companies',session!.token),request<Audit[]>('/audit',session!.token)]);
   if(active&&ticket===generation.current){setData(workers);setCompanies(choices);setAudit(events);}
  }catch(e){if(active&&ticket===generation.current)failure(e);}finally{if(active&&ticket===generation.current)setLoading(false);}}
  void load();return()=>{active=false;};
 },[session,page,query,status,reload]);
 async function login(e:FormEvent){e.preventDefault();setBusy(true);setError('');try{const result=await request<Session>('/auth/login','','POST',{email,password});setSession(result);setPassword('');setPage(1);setQuery('');setSearch('');setStatus('');setNotice('Signed in.');}catch(e){failure(e);}finally{setBusy(false);}}
 function open(worker:Worker|null){setEditing(worker);setDraft(worker?profileOf(worker):empty(companies[0]?.id));setFormOpen(true);setError('');setNotice('');}
 async function save(e:FormEvent){e.preventDefault();if(!session)return;setBusy(true);setError('');setNotice('');try{await request<Worker>(editing?`/workers/${editing.id}`:'/workers',session.token,editing?'PUT':'POST',editing?{...draft,version:editing.version}:draft);setFormOpen(false);setEditing(null);setDraft(empty());setNotice(editing?'Worker updated.':'Worker created.');setReload(v=>v+1);}catch(e){failure(e);}finally{setBusy(false);}}
 async function change(worker:Worker,next:string){if(!session || !confirm(`Move ${worker.firstName} ${worker.lastName} to ${next.toLowerCase()}?`))return;setBusy(true);setError('');setNotice('');try{await request(`/workers/${worker.id}/status`,session.token,'POST',{version:worker.version,status:next});setNotice('Status updated.');setReload(v=>v+1);}catch(e){failure(e);}finally{setBusy(false);}}
 async function remove(worker:Worker){if(!session || !confirm(`Delete draft ${worker.firstName} ${worker.lastName}? This cannot be undone.`))return;setBusy(true);setError('');setNotice('');try{await request(`/workers/${worker.id}`,session.token,'DELETE',{version:worker.version});setNotice('Draft worker deleted.');if(data.items.length===1&&page>1)setPage(v=>v-1);else setReload(v=>v+1);}catch(e){failure(e);}finally{setBusy(false);}}
 async function refreshDraft(){if(!session||!editing||!confirm('Replace the form with the current saved worker? Copy any draft text you want to keep first.'))return;setBusy(true);try{const current=await request<Worker>(`/workers/${editing.id}`,session.token);setEditing(current);setDraft(profileOf(current));setError('');setNotice('Current worker loaded.');}catch(e){failure(e);}finally{setBusy(false);}}
 function signOut(){if(formOpen&&!confirm('Sign out and discard the open form?'))return;generation.current++;setSession(null);setData({items:[],total:0,page:1,limit:20});setAudit([]);setCompanies([]);setFormOpen(false);setEditing(null);setDraft(empty());setError('');setNotice('');}
 const field=(name:keyof Profile,label:string,max:number,type='text')=><label key={name}>{label}<input name={name} type={type} required={['firstName','lastName','email','countryCode'].includes(name)} maxLength={max} value={draft[name]} onChange={e=>setDraft({...draft,[name]:e.target.value})}/></label>;
 return <div className="shell"><header><div className="brand"><span className="mark">GW</span><div><strong>GlobalWorkforce</strong><span>People operations workspace</span></div></div>{session&&<div className="identity"><span>{session.actor.tenantName}<small>{session.actor.email} · {session.actor.role.replaceAll('_',' ')}</small></span><button disabled={busy} onClick={signOut}>Sign out</button></div>}</header>
 <main><div className="intro"><p className="eyebrow">OPERATIONS / WORKER DIRECTORY</p><h1>A clear view of your people.</h1><p>Manage worker profiles, follow their status, and review the record of every change.</p></div>
 {error&&<div role="alert" className="alert">{error}</div>}{notice&&<p role="status" className="notice">{notice}</p>}
 {!session?<section className="login panel"><h2>Sign in to your workspace</h2><p>Use an account created by the local demo seed.</p><form onSubmit={login}><label>Email<input autoComplete="username" type="email" required value={email} onChange={e=>setEmail(e.target.value)}/></label><label>Password<input autoComplete="current-password" type="password" required maxLength={200} value={password} onChange={e=>setPassword(e.target.value)}/></label><button className="primary" disabled={busy}>{busy?'Signing in…':'Sign in'}</button></form></section>:<>
 <div className="summary"><section><span>Matching workers</span><strong>{data.total}</strong></section><section><span>Workspace</span><strong>{session.actor.tenantName}</strong></section><section><span>Directory scope</span><strong>Current organization</strong></section></div>
 <section className="panel"><div className="section-heading"><div><h2>Worker directory</h2><p>Create a draft, update details, and track the next step.</p></div><button className="primary" disabled={busy||formOpen||loading||!companies.length} onClick={()=>open(null)}>Add worker</button></div>
 <form className="filters" onSubmit={e=>{e.preventDefault();setPage(1);setQuery(search);}}><label>Search workers<input value={search} onChange={e=>setSearch(e.target.value)} maxLength={100} placeholder="Name or email"/></label><button disabled={busy}>Search</button><label>Status<select value={status} onChange={e=>{setPage(1);setStatus(e.target.value);}}><option value="">All statuses</option>{Object.keys(moves).map(v=><option key={v}>{v}</option>)}</select></label><button type="button" disabled={busy||loading} onClick={()=>{setError('');setReload(v=>v+1);}}>Refresh directory</button></form>
 {loading&&<p role="status">Loading workers…</p>}<div className="table-wrap"><table><thead><tr><th>Worker</th><th>Company / role</th><th>Status</th><th>Actions</th></tr></thead><tbody>{data.items.map(w=><tr key={w.id}><td><strong>{w.firstName} {w.lastName}</strong><small>{w.email}</small></td><td>{w.company.name}<small>{w.jobTitle||'Role not specified'} · {w.countryCode}</small></td><td><span className={`badge ${w.employmentStatus.toLowerCase()}`}>{w.employmentStatus.toLowerCase()}</span><small>Revision {w.version}</small></td><td><div className="actions"><button disabled={busy||formOpen||loading} onClick={()=>open(w)}>{w.employmentStatus==='TERMINATED'?'View':'Edit'}</button>{moves[w.employmentStatus]?.map(next=><button key={next} disabled={busy||formOpen||loading} onClick={()=>void change(w,next)}>Move to {next.toLowerCase()}</button>)}{w.employmentStatus==='DRAFT'&&<button className="danger" disabled={busy||formOpen||loading} onClick={()=>void remove(w)}>Delete draft</button>}</div></td></tr>)}</tbody></table></div>
 {!loading&&!data.items.length&&<p className="empty">No workers match this view. Adjust the filters or add a worker.</p>}<div className="pagination"><span>Page {page} · {data.total} matching</span><button disabled={busy||loading||page===1} onClick={()=>setPage(v=>v-1)}>Previous</button><button disabled={busy||loading||page*20>=data.total} onClick={()=>setPage(v=>v+1)}>Next</button></div></section>
 {formOpen&&<section className="panel editor" aria-label="Worker form"><h2>{editing?'Worker profile':'New draft worker'}</h2><p>{editing?`Editing revision ${editing.version}. Failed saves keep this form.`:'Drafts can be deleted until onboarding begins.'}</p><form onSubmit={save}><fieldset disabled={busy||editing?.employmentStatus==='TERMINATED'}><div className="form-grid">{field('firstName','First name',80)}{field('lastName','Last name',80)}{field('email','Worker email',254,'email')}<label>Company<select required value={draft.companyId} onChange={e=>setDraft({...draft,companyId:e.target.value})}>{!companies.some(c=>c.id===draft.companyId)&&<option value="">Choose an active company</option>}{companies.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label>{field('countryCode','Country code',2)}{field('jobTitle','Job title',120)}{field('department','Department',100)}</div></fieldset><div className="actions">{editing?.employmentStatus!=='TERMINATED'&&<button className="primary" disabled={busy}>{busy?'Saving…':'Save worker'}</button>}<button type="button" disabled={busy} onClick={()=>{if(confirm('Close this form and discard unsaved changes?')){setFormOpen(false);setEditing(null);setDraft(empty());}}}>Close form</button>{editing&&<button type="button" disabled={busy} onClick={()=>void refreshDraft()}>Load current worker</button>}</div></form></section>}
 <section className="panel audit"><div className="section-heading"><div><h2>Recent worker activity</h2><p>The latest 30 recorded changes in this workspace.</p></div></div>{audit.length?<ol>{audit.map(a=><li key={a.id}><span><strong>{a.action.replaceAll('_',' ').toLowerCase()}</strong><small>Worker {a.entityId} · Actor {a.actorUserId}</small></span><time dateTime={a.createdAt}>{new Date(a.createdAt).toLocaleString()}</time></li>)}</ol>:<p className="empty">No worker changes have been recorded yet.</p>}</section>
 </>}<footer>GlobalWorkforce · Local learning edition</footer></main></div>;
}
export default App;
'''}
for rel,content in files.items():(s/rel).write_text(content,encoding='utf-8')
print('Wrote connected React directory and profile editor')
