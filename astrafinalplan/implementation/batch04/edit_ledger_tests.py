from pathlib import Path
import re,json
B=Path('astrafinalplan/implementation/batch04')
for n in range(67,72):
 root=B/'stage'/str(n);p=root/'server/src/services/service.ts';s=p.read_text().replace('value.trim().length > 255','value.trim().length > (key === "title" ? 220 : key === "owner" ? 160 : 40)');p.write_text(s)
 m=(root/'server/src/models/model.ts').read_text();table=re.search(r'const table = "(.*?)"',m)[1];org=re.search(r'const orgColumn = "(.*?)"',m)[1];init=(root/'server/db/migrations/001_init.ts').read_text();parent=re.search(r'createTable\("(.*?)"',init)[1];statuses=json.loads(re.search(r'const allowedStatuses = (.*);',s)[1]);route='/api/'+table
 tests='''import {test,before,after} from "node:test";
import assert from "node:assert/strict";
import {database,request} from "./database.js";
let h:Awaited<ReturnType<typeof database>>;
before(async()=>{h=await database();await h.db("PARENT").insert({id:1,name:"Learning team"});});
after(async()=>{if(h)await h.close();});
const api=(path="",method="GET",body?:unknown)=>request(h.origin,"ROUTE"+path,method,body);
async function create(title:string,status="STATUS"){const r=await api("","POST",{title,status,ORG:1});assert.equal(r.status,201,JSON.stringify(r.data));return r.data.data;}
test("partial edit preserves omitted values; invalid edits leave stored values unchanged",async()=>{
 const a=await create("Partial");let r=await api(`/${a.id}`,"PUT",{title:"Renamed"});assert.equal(r.status,200);assert.equal(r.data.data.owner,a.owner);
 for(const bad of [{title:" "},{metadata:[]},{status:null},{priority:3},{due_at:"2025-02-30"},{ORG:"1"},{}])assert.equal((await api(`/${a.id}`,"PUT",bad)).status,400);
 assert.equal((await api(`/${a.id}`)).data.data.title,"Renamed");assert.equal((await api("/1e2")).status,400);
});
test("archive and restore preserve the previous workflow state and repeats are no-ops",async()=>{
 const a=await create("Lifecycle","SECOND");await api(`/${a.id}/archive`,"PATCH",{});
 const count=async()=>Number((await h.db("audit_log").count("* as count").first()).count);
 const once=await count();await api(`/${a.id}/archive`,"PATCH",{});assert.equal(await count(),once);
 const r=await api(`/${a.id}/restore`,"PATCH",{});assert.equal(r.status,200);assert.equal(r.data.data.status,"SECOND");assert.equal(r.data.data.archived_at,null);
 const restored=await count();await api(`/${a.id}/restore`,"PATCH",{});assert.equal(await count(),restored);
});
test("bulk status rejects missing IDs atomically and records real before/after values",async()=>{
 const a=await create("Bulk");assert.equal((await api("/bulk/status","POST",{ids:[a.id,999999],status:"SECOND"})).status,404);
 assert.equal((await api(`/${a.id}`)).data.data.status,"STATUS");
 const r=await api("/bulk/status","POST",{ids:[a.id,a.id],status:"SECOND"});assert.equal(r.status,200);assert.equal(r.data.data.length,1);
 const audit=await h.db("audit_log").where({action:"bulk_status"}).orderBy("id","desc").first();assert.equal(audit.before.status,"STATUS");assert.equal(audit.after.status,"SECOND");
 const count=await h.db("audit_log").count("* as count").first();await api("/bulk/status","POST",{ids:[a.id],status:"SECOND"});assert.deepEqual(await h.db("audit_log").count("* as count").first(),count);
});
test("ordinary status edits keep archive flags consistent; deleted records cannot be restored",async()=>{
 const a=await create("Flags");await api(`/${a.id}`,"PUT",{status:"archived"});assert.ok((await api(`/${a.id}`)).data.data.archived_at);
 await api(`/${a.id}`,"PUT",{status:"SECOND"});assert.equal((await api(`/${a.id}`)).data.data.archived_at,null);
 await api(`/${a.id}`,"DELETE");assert.equal((await api(`/${a.id}/restore`,"PATCH",{})).status,404);
});
'''
 for a,b in [('PARENT',parent),('ROUTE',route),('ORG',org),('SECOND',statuses[1]),('STATUS',statuses[0])]:tests=tests.replace(a,b)
 (root/'test/crud.test.ts').write_text(tests)
p=B/'stage/55/server/src/index.ts';s=p.read_text();s=s.replace('      if (input.delta < 0) {','      await lockProduct(client, input.productId);\n      await requireWarehouse(client, input.warehouseId);\n      if (input.delta < 0) {');s=s.replace('      const balance = await balanceOf(client, input.productId, input.fromWarehouseId);','      await lockProduct(client, input.productId);\n      await requireWarehouse(client, input.fromWarehouseId);\n      await requireWarehouse(client, input.toWarehouseId);\n      const balance = await balanceOf(client, input.productId, input.fromWarehouseId);')
s=s.replace('const data = body as Partial<NewMovement>;','const data = objectBody(body) as Partial<NewMovement>;').replace('const data = body as Partial<Transfer>;','const data = objectBody(body) as Partial<Transfer>;')
s=s.replace('if (!data.productId)','if (!isUuid(data.productId))').replace('if (!data.warehouseId)','if (!isUuid(data.warehouseId))').replace('if (!data.fromWarehouseId || !data.toWarehouseId)','if (!isUuid(data.fromWarehouseId) || !isUuid(data.toWarehouseId))')
s=s.replace('Math.trunc(Number(data.delta))','data.delta').replace('!Number.isFinite(delta) || delta === 0','typeof delta !== "number" || !Number.isInteger(delta) || delta === 0 || Math.abs(delta) > 2147483647').replace('Math.trunc(Number(data.quantity))','data.quantity').replace('if (!(quantity > 0))','if (typeof quantity !== "number" || !Number.isInteger(quantity) || quantity < 1 || quantity > 2147483647)')
s=s.replace('(data.reason ?? "").trim()','parseReason(data.reason)')
s+='''
function objectBody(body: unknown): object { if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send a JSON object."); return body; }
function isUuid(value: unknown): value is string {return typeof value === "string" && /^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(value);}
function parseReason(value: unknown): string {if (value === undefined) return ""; if (typeof value !== "string" || value.trim().length > 500) throw new ValidationError("Reason must be at most 500 characters."); return value.trim();}
// Every write takes the same product lock before reading balances. This also
// serializes opposing transfers without taking warehouse locks in different orders.
async function lockProduct(client: PoolClient, id: string) {const result=await client.query("SELECT id FROM products WHERE id=$1 FOR UPDATE",[id]);if(!result.rowCount)throw new ValidationError("Product not found.");}
async function requireWarehouse(client: PoolClient, id: string) {const result=await client.query("SELECT id FROM warehouses WHERE id=$1",[id]);if(!result.rowCount)throw new ValidationError("Warehouse not found.");}
'''
p.write_text(s)
