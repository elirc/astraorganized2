from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent;p=b/'stage/43d6b6358f56'
(p/'tests/api-key-verify-boundary.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const columns=new Proxy({}, {get:(_target,name)=>({column:name})});
const eq=(a,b)=>({op:'eq',a,b}),isNull=a=>({op:'isNull',a}),and=(...items)=>({op:'and',items});
function matches(row,where) {
  if(where.op==='and') return where.items.every(item=>matches(row,item));
  if(where.op==='isNull') return row[where.a.column]===null;
  return row[where.a.column]===where.b;
}
const token='test-token',prefix='sk_test';
const active={id:'key-1',organizationId:'org-a',keyPrefix:prefix,keyHash:crypto.createHash('sha256').update(token).digest('hex'),revokedAt:null,deletedAt:null};
async function fixture(rows=[active],options={}) {
  const calls={queries:[],updates:[]};
  const db={query:{apiKeys:{findFirst:async args=>{
    calls.queries.push(args);if(options.readError)throw options.readError;
    return rows.find(row=>matches(row,args.where));
  }}},update:table=>{assert.equal(table,columns);return {set:data=>({where:async where=>{
    calls.updates.push({data,where});if(options.writeError)throw options.writeError;
  }})};}};
  const mod=await loadTypeScript('lib/services/apiKeys.ts',{root,stubs:{
    crypto:{default:crypto},'drizzle-orm':{eq,isNull,and},'@/lib/db/index':{db},'@/lib/db/schema':{apiKeys:columns}
  }});
  return {calls,verify:(key=prefix+'.'+token,org='org-a')=>mod.verifyApiKey(org,key)};
}
test('malformed keys perform no database read or last-used write',async()=>{
  for(const key of ['',prefix, prefix+'.', '.'+token, prefix+'.'+token+'.extra',prefix+'..'+token]) {
    const f=await fixture();assert.equal(await f.verify(key),null,key);
    assert.equal(f.calls.queries.length,0);assert.equal(f.calls.updates.length,0);
  }
});
test('active key uses real SHA-256 and updates its last-used timestamp',async()=>{
  const f=await fixture();assert.equal(await f.verify(),active);
  const filters=f.calls.queries[0].where.items;
  assert.equal(filters.find(x=>x.a.column==='keyHash').b,active.keyHash);
  assert.equal(filters.find(x=>x.a.column==='organizationId').b,'org-a');
  assert.equal(filters.filter(x=>x.op==='isNull').length,2);
  assert.equal(f.calls.updates.length,1);const update=f.calls.updates[0];
  assert.equal(update.where.a.column,'id');assert.equal(update.where.b,'key-1');
  assert.ok(Number.isFinite(update.data.lastUsedAt.getTime()));
});
test('deleted, revoked, foreign, mismatched and missing keys perform no write',async()=>{
  for(const patch of [{deletedAt:new Date()},{revokedAt:new Date()},{organizationId:'org-b'},{keyHash:'wrong'},{keyPrefix:'other'}]) {
    const f=await fixture([{...active,...patch}]);assert.equal(await f.verify(),null);
    assert.equal(f.calls.queries.length,1);assert.equal(f.calls.updates.length,0);
  }
  const missing=await fixture([]);assert.equal(await missing.verify(),null);assert.equal(missing.calls.updates.length,0);
});
test('database errors preserve identity instead of reporting successful verification',async()=>{
  for(const field of ['readError','writeError']) {
    const failure=new Error(field),f=await fixture([active],{[field]:failure});
    await assert.rejects(f.verify(),e=>e===failure);
    assert.equal(f.calls.updates.length,field==='readError'?0:1);
  }
});
''',encoding='utf-8')
f=b/'specs/43d6b6358f56.json';s=json.loads(f.read_text(encoding='utf-8-sig'));s['limits']=['Four runtime cases execute actual apiKeys.ts with real Node SHA-256 and explicit Drizzle/schema/database predicate adapters. No Next.js, native ORM or PostgreSQL is executed.','The sequential verification read and lastUsedAt write are unchanged; concurrent revocation/deletion between them is not made atomic. Key verification does not establish every caller permission or organization lifecycle rule.'];f.write_text(json.dumps(s,indent=2),encoding='utf-8')
