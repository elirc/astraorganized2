from pathlib import Path
import json,re
B=Path(__file__).resolve().parent;R=B/'stage';spec=[]
for n in range(58,62):
 root=R/str(n);old=(root/'client/src/App.tsx').read_text(encoding='utf-8');form=json.loads(re.search(r'const emptyForm = (\{.*?\});',old,re.S)[1]);fields=list(form);strings=[x for x in fields if x!='tags'];table=re.search(r'db\("([^\"]+)"',(root/'server/src/models/model.ts').read_text(encoding='utf-8'))[1];title=re.search(r'<h1>(.*?)</h1>',old)[1];route='/api/'+table
 schema=',\n  '.join(f'{key}: z.string().trim().min({0 if key=="body" else 1}).max({20000 if key=="body" else 255})'+('.default("")' if key=='body' else '') for key in strings)
 s='''import { z } from "zod";
import * as model from "../models/model.js";
import { NotFoundError, ValidationError } from "../utils/errors.js";
const recordSchema = z.object({
SCHEMA,
  tags: z.array(z.string().trim().min(1).max(50)).max(30).transform(values => [...new Map(values.map(value => [value.toLowerCase(), value])).values()]).default([])
});
function parseId(value: string) {
  if (!/^[1-9]\\d*$/.test(value) || !Number.isSafeInteger(Number(value))) throw new ValidationError("Id must be a positive whole number.");
  return Number(value);
}
function parsePayload(payload: unknown, partial = false) {
  const result = (partial ? recordSchema.partial() : recordSchema).safeParse(payload);
  if (!result.success) throw new ValidationError(result.error.issues.map(issue => issue.path.join(".") + ": " + issue.message).join("; "));
  if (!Object.keys(result.data).length) throw new ValidationError("Provide at least one editable field.");
  return result.data;
}
export function list(query: { search?: unknown; status?: unknown }) {
  if ([query.search,query.status].some(value => value !== undefined && (typeof value !== "string" || value.length > 255))) throw new ValidationError("Filters must be short text values.");
  return model.listRecords(query as {search?:string;status?:string});
}
export async function get(value: string) {
  const record = await model.findRecord(parseId(value));
  if (!record) throw new NotFoundError("Record not found.");
  return record;
}
export function create(payload: unknown) { return model.createRecord(parsePayload(payload)); }
export async function update(value: string, payload: unknown) {
  const record = await model.updateRecord(parseId(value),parsePayload(payload,true));
  if (!record) throw new NotFoundError("Record not found.");
  return record;
}
export async function remove(value: string) {
  const record = await model.deleteRecord(parseId(value));
  if (!record) throw new NotFoundError("Record not found.");
  return record;
}
export function getStats() { return model.stats(); }
'''.replace('SCHEMA',schema)
 (root/'server/src/services/service.ts').write_text(s,encoding='utf-8')
 p=root/'server/src/models/model.ts';s=p.read_text(encoding='utf-8')
 start=s.index('export function listRecords');end=s.index('\n/**',start)
 s=s[:start]+'''export function listRecords(query: { search?: string; status?: string }) {
  const builder = db("TABLE").select("*").orderBy("created_at", "desc").orderBy("id","asc");
  if (query.status) builder.where("status",query.status);
  if (query.search) builder.where(function () { FIELDS.forEach(field => this.orWhereILike(field, `%${query.search}%`)); });
  return builder;
}
'''.replace('TABLE',table).replace('FIELDS',json.dumps(strings))+s[end:]
 s=s.replace('insert(payload)','insert(databasePayload(payload))').replace('...payload, updated_at','...databasePayload(payload), updated_at')
 s+='\nfunction databasePayload(payload: Record<string, unknown>) { return payload.tags === undefined ? payload : { ...payload, tags: JSON.stringify(payload.tags) }; }\n';p.write_text(s,encoding='utf-8')
 (root/'client/src/types.ts').write_text('export interface RecordInput {\n'+''.join(f'  {key}: '+('string[]' if key=='tags' else 'string')+';\n' for key in fields)+'}\nexport interface RecordItem extends RecordInput { id: number; created_at: string; updated_at: string; }\nexport interface Stats {total:number; byStatus:Array<{status:string;count:string}>}\n',encoding='utf-8')
 p=root/'client/src/services/api.ts';s=p.read_text(encoding='utf-8');s='import type {RecordInput,RecordItem,Stats} from "../types";\n'+s
 s=s.replace('function createRecord(payload)','function createRecord(payload: RecordInput)').replace('function updateRecord(id, payload)','function updateRecord(id: number, payload: Partial<RecordInput>)').replace('function deleteRecord(id)','function deleteRecord(id: number)')
 parts=s.split('return unwrap(response);');assert len(parts)==6;s=parts[0]+'return unwrap<RecordItem[]>(response);'+parts[1]+'return unwrap<RecordItem>(response);'+parts[2]+'return unwrap<RecordItem>(response);'+parts[3]+'return unwrap<RecordItem>(response);'+parts[4]+'return unwrap<Stats>(response);'+parts[5]
 s=s.replace('/** Reads the standard API response envelope. */','''// Axios rejects non-2xx responses before unwrap; surface the server's validation message.
api.interceptors.response.use(response => response, error => Promise.reject(new Error(error.response?.data?.error?.message || error.message || "Request failed")));
/** Reads the standard API response envelope. */''');p.write_text(s,encoding='utf-8')
 empty={k:([] if k=='tags' else form[k] if k in ['status','lane','stage'] else '') for k in fields}
 controls='\n'.join(f'''          <label>{key}<{'textarea' if key=='body' else 'input'} value={{Array.isArray(form.{key}) ? (form.{key} as string[]).join(", ") : form.{key}}} onChange={{event => updateField("{key}",event.target.value)}} /></label>''' for key in fields)
 # Dedicated form input type prevents server timestamps and ids from leaking into mutation payloads.
 app='''import {useEffect,useRef,useState, type FormEvent} from "react";
import styles from "./App.module.css";
import "./index.css";
import {createRecord,deleteRecord,listRecords,loadStats,updateRecord} from "./services/api";
import type {RecordInput,RecordItem,Stats} from "./types";
const emptyForm: RecordInput = EMPTY;
export default function App() {
  const [records,setRecords]=useState<RecordItem[]>([]), [stats,setStats]=useState<Stats|null>(null);
  const [form,setForm]=useState<RecordInput>(emptyForm),[editingId,setEditingId]=useState<number|null>(null);
  const [search,setSearch]=useState(""),[error,setError]=useState(""),[message,setMessage]=useState(""),[pending,setPending]=useState(false);
  const sequence=useRef(0),mutation=useRef(false);
  async function refresh() {
    const request=++sequence.current;
    try { const [items,totals]=await Promise.all([listRecords({search}),loadStats()]); if(request===sequence.current){setRecords(items);setStats(totals);setError("");} }
    catch(e){if(request===sequence.current)setError(e instanceof Error?e.message:"Could not load records.");}
  }
  useEffect(()=>{const timer=setTimeout(()=>void refresh(),150);return()=>{clearTimeout(timer);sequence.current++;};},[search]);
  function updateField(field:keyof RecordInput,value:string){setForm(current=>({...current,[field]:field==="tags"?value.split(",").map(tag=>tag.trim()).filter(Boolean):value}));}
  function cancel(){setEditingId(null);setForm(emptyForm);setMessage("");setError("");}
  async function saveRecord(event:FormEvent){
    event.preventDefault();if(mutation.current)return;mutation.current=true;setPending(true);setError("");setMessage("");
    try {if(editingId!==null)await updateRecord(editingId,form);else await createRecord(form);setEditingId(null);setForm(emptyForm);setMessage("Record saved.");await refresh();}
    catch(e){setError(e instanceof Error?e.message:"Could not save record.");}
    finally{mutation.current=false;setPending(false);}
  }
  function editRecord(record:RecordItem){setEditingId(record.id);setForm({FIELDS});setMessage("");setError("");}
  async function removeRecord(id:number){
    if(mutation.current||!window.confirm("Delete this record?"))return;mutation.current=true;setPending(true);setError("");
    try {await deleteRecord(id);if(editingId===id)cancel();setMessage("Record deleted.");await refresh();}
    catch(e){setError(e instanceof Error?e.message:"Could not delete record.");}
    finally{mutation.current=false;setPending(false);}
  }
  return <main className={styles.shell}>
    <section className={styles.header}><div><p>{stats?.total??records.length} records</p><h1>TITLE</h1></div><input aria-label="Search records" placeholder="Search" value={search} onChange={event=>setSearch(event.target.value)}/></section>
    {error&&<div role="alert" className={styles.error}>{error}</div>}<p role="status">{message}</p>
    <section className={styles.grid}><form className={styles.panel} onSubmit={saveRecord}><h2>{editingId===null?"Create":"Edit"} record</h2>
      <fieldset disabled={pending} style={{border:0,padding:0,margin:0}}>
CONTROLS
      <button type="submit">{pending?"Saving…":editingId===null?"Create":"Update"}</button>{editingId!==null&&<button type="button" onClick={cancel}>Cancel</button>}</fieldset>
    </form><section className={styles.list} aria-label="Records">
      {!records.length&&<p>No matching records.</p>}
      {records.map(record=><article className={styles.card} key={record.id}><div><h3>{record.PRIMARY}</h3><p>{record.SECONDARY}</p><small>{record.status}</small></div><div className={styles.actions}><button disabled={pending} onClick={()=>editRecord(record)}>Edit</button><button disabled={pending} onClick={()=>void removeRecord(record.id)}>Delete</button></div></article>)}
    </section></section></main>;
}
'''.replace('EMPTY',json.dumps(empty)).replace('FIELDS',','.join(f'{key}:record.{key}'+('??[]' if key=='tags' else '??""') for key in fields)).replace('CONTROLS',controls).replace('TITLE',title).replace('PRIMARY',strings[0]).replace('SECONDARY',strings[1])
 (root/'client/src/App.tsx').write_text(app,encoding='utf-8')
 spec.append(dict(stage=str(n),table=table,route=route,fields=fields,valid=form,title=title))
(B/'simple-specs.json').write_text(json.dumps(spec,indent=2),encoding='utf-8');print('Updated four small CRUD apps with validated create/partial updates, serialized tags, typed edit forms, cancellation and mutation feedback')
