from pathlib import Path
import shutil
B=Path('astrafinalplan/implementation/batch02/stage')
for n in [19,20]:
 p=B/str(n)/'server/test';p.mkdir(exist_ok=True);shutil.copyfile(Path('astrafinalplan/implementation/stage/07/server/test/database.cjs'),p/'database.cjs')
(B/'19/server/test/search.test.cjs').write_text('''const {test}=require('node:test');
const assert=require('node:assert/strict');
const helper=require('./database.cjs');
helper.configure();
const {db}=require('../src/config/db');
const app=require('../src/app');
const {up}=require('../db/migrations/001_init');
test('full-text content search, partial updates and validation through HTTP/PostgreSQL',async(t)=>{
 const cleanup=await helper.prepare(db,up);t.after(cleanup);
 const http=await helper.listen(app);t.after(http.close);
 const create=(title,body,folder='General')=>http.request('POST','/api/notes',{title,body,folder,status:'active',tags:['search','search']});
 const a=await create('Running notes','Practice indexing and queries');assert.equal(a.status,201);
 const b=await create('Other document','Cooking vegetables','HiddenKeyword');assert.equal(b.status,201);
 const id=a.body.data.id;
 assert.deepEqual(a.body.data.tags,['search']);
 let result=await http.request('GET','/api/notes?search=run');
 assert.deepEqual(result.body.data.map(x=>x.id),[id]);
 result=await http.request('GET','/api/notes?search=HiddenKeyword');assert.equal(result.body.data.length,0);
 result=await http.request('GET','/api/notes?search=run&folder=Missing');assert.equal(result.body.data.length,0);
 result=await http.request('GET','/api/notes?search=%25');assert.equal(result.body.data.length,0);
 assert.equal((await http.request('GET','/api/notes?search[]=bad')).status,400);
 assert.equal((await http.request('POST','/api/notes',{title:42})).status,400);
 assert.equal((await http.request('PUT',`/api/notes/${id}`,{tags:[{}]})).status,400);
 const changed=await http.request('PUT',`/api/notes/${id}`,{body:'A revised explanation'});assert.equal(changed.status,200);
 assert.equal(changed.body.data.title,'Running notes');
 assert.equal((await http.request('GET','/api/notes?search=revised')).body.data[0].id,id);
 assert.equal((await db('notes').where({id}).first()).body,'A revised explanation');
 assert.equal((await http.request('GET','/api/notes/2147483648')).status,400);
});
''',encoding='utf-8')
(B/'20/server/test/bookmarks.test.ts').write_text('''import {test} from 'node:test';
import assert from 'node:assert/strict';
import helper from './database.cjs';
helper.configure();
test('bookmark validation and metadata denial leave the stored record intact',async(t)=>{
 const {db}=await import('../src/config/db.js');
 const {up}=await import('../db/migrations/001_init.js');
 const app=(await import('../src/app.js')).default;
 const cleanup=await helper.prepare(db,up);t.after(cleanup);
 const http=await helper.listen(app);t.after(http.close);
 const payload={title:'A guide',url:'https://example.com/guide',collection:'Learning',status:'active',tags:['JS','JS']};
 let result=await http.request('POST','/api/bookmarks',payload);assert.equal(result.status,201);
 const id=result.body.data.id;assert.deepEqual(result.body.data.tags,['JS']);
 for(const change of [{url:'javascript:alert(1)'},{title:42},{tags:'JS'},{url:'https://user:password@example.com'}]) {
  result=await http.request('POST','/api/bookmarks',{...payload,...change});assert.equal(result.status,400);
 }
 result=await http.request('PUT',`/api/bookmarks/${id}`,{title:'Updated'});assert.equal(result.status,200);
 assert.equal(result.body.data.url,payload.url);
 result=await http.request('PUT',`/api/bookmarks/${id}`,{url:'file:///private'});assert.equal(result.status,400);
 assert.equal((await db('bookmarks').where({id}).first()).title,'Updated');
 assert.equal((await db('bookmarks').select('*')).length,1);
 assert.equal((await http.request('POST','/api/bookmarks/metadata',{url:'https://127.0.0.1/private'})).status,400);
 assert.equal((await http.request('GET','/api/bookmarks/2147483648')).status,400);
});
''',encoding='utf-8')
(B/'20/server/test/metadata.test.ts').write_text('''import {test} from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import type https from 'node:https';
import {fetchMetadata,createHtmlTransfer,isPublicIPv4} from '../src/services/metadata.js';
test('public-address policy rejects loopback, private, mapped IPv6 and reserved ranges',()=>{
 for(const ip of ['127.0.0.1','10.0.0.1','172.16.0.1','192.168.1.1','169.254.169.254','100.64.0.1','0.0.0.0','192.0.2.1','198.18.0.1','198.51.100.1','203.0.113.1','224.0.0.1','::1','::ffff:127.0.0.1']) assert.equal(isPublicIPv4(ip),false,ip);
 assert.equal(isPublicIPv4('93.184.216.34'),true);
});
test('real controlled HTTP responses exercise redirects, body caps and timeout without external requests',async(t)=>{
 const hits:string[]=[];const lookups:string[]=[];
 const server=http.createServer((req,res)=>{
  hits.push(req.url || '');
  if(req.url==='/redirect'){res.writeHead(302,{Location:'http://127.0.0.1/protected'});res.end();return;}
  if(req.url==='/slow')return;
  res.setHeader('Content-Type','text/html');
  if(req.url==='/large'){res.write('x'.repeat(100));res.end('x'.repeat(100));return;}
  res.end('<html><title>A &amp; B</title></html>');
 });
 await new Promise<void>(resolve=>server.listen(0,'127.0.0.1',resolve));
 t.after(()=>new Promise<void>(resolve=>{server.close(()=>resolve());server.closeAllConnections();}));
 const port=(server.address() as any).port;
 // Only the connection factory is substituted. Production response handling is unchanged.
 const get=((url:URL,options:any,callback:any)=>{
  options.lookup(url.hostname,{},(error:Error|null,address:string)=>{assert.equal(error,null);lookups.push(address);});
  return http.get({hostname:'127.0.0.1',port,path:url.pathname,signal:options.signal},callback);
 }) as typeof https.get;
 const options={allowedHosts:['allowed.example'],resolve:async()=>['93.184.216.34'],transfer:createHtmlTransfer(get),timeoutMs:1000,maxBytes:128};
 assert.deepEqual(await fetchMetadata('https://allowed.example/ok',options),{url:'https://allowed.example/ok',title:'A & B'});
 await assert.rejects(fetchMetadata('https://allowed.example/redirect',options),/redirects/);
 await assert.rejects(fetchMetadata('https://allowed.example/large',options),/too large/);
 await assert.rejects(fetchMetadata('https://allowed.example/slow',{...options,timeoutMs:100}),/timed out|Could not fetch/);
 const before=hits.length;
 await assert.rejects(fetchMetadata('https://allowed.example/private',{...options,resolve:async()=>['127.0.0.1']}),/public IPv4/);
 await assert.rejects(fetchMetadata('https://unlisted.example/',options),/configured/);
 await assert.rejects(fetchMetadata('https://127.0.0.1/',options),/configured/);
 assert.equal(hits.length,before);assert.equal(hits.includes('/protected'),false);
 assert.ok(lookups.every(ip=>ip==='93.184.216.34'));
});
test('DNS completing after timeout cannot start a transfer',async()=>{
 let transferCalls=0;
 await assert.rejects(fetchMetadata('https://allowed.example/',{
  allowedHosts:['allowed.example'],timeoutMs:10,
  resolve:()=>new Promise(resolve=>setTimeout(()=>resolve(['93.184.216.34']),50)),
  transfer:async()=>{transferCalls++;return '<title>Never</title>';},
 }),/timed out/);
 await new Promise(resolve=>setTimeout(resolve,80));assert.equal(transferCalls,0);
});
''',encoding='utf-8')
p=B/'18/test';p.mkdir(exist_ok=True)
(p/'booking.test.ts').write_text('''import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {randomBytes} from 'node:crypto';
import pg from 'pg';
import {parseBooking} from '../server/src/validation.js';
const input=process.env.ASTRA_TEST_DATABASE_URL;
if(!input || !/^astra_test_[a-z0-9_]+$/.test(new URL(input).pathname.slice(1))) throw new Error('Use a dedicated ASTRA_TEST_DATABASE_URL named astra_test_*');
const schema=`astra_booking_${randomBytes(6).toString('hex')}`;
const url=new URL(input);url.searchParams.set('options',`-c search_path=${schema},public`);process.env.DATABASE_URL=url.href;
test('database enforces concurrent overlap, adjacent slots and failed-edit preservation through HTTP',async(t)=>{
 const admin=new pg.Client({connectionString:input});await admin.connect();
 await admin.query('CREATE EXTENSION IF NOT EXISTS btree_gist');await admin.query('CREATE EXTENSION IF NOT EXISTS pgcrypto');
 await admin.query(`CREATE SCHEMA "${schema}"`);await admin.query(`SET search_path TO "${schema}", public`);
 let sql=await readFile(new URL('../server/db/schema.sql',import.meta.url),'utf8');
 // The schema is unique and empty. Never run the scaffold's DROP TABLE statements against a fallback namespace.
 sql=sql.replace(/^DROP TABLE.*$/gm,'');
 await admin.query(sql);
 const {app}=await import('../server/src/index.js');const {pool}=await import('../server/src/db.js');
 const server=await new Promise<any>(resolve=>{const s=app.listen(0,'127.0.0.1',()=>resolve(s));});
 t.after(async()=>{await new Promise<void>(resolve=>{server.close(()=>resolve());server.closeAllConnections();});await pool.end();await admin.query(`DROP SCHEMA "${schema}" CASCADE`);await admin.end();});
 const base=`http://127.0.0.1:${server.address().port}`;
 async function request(method:string,path:string,body?:unknown){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});return {status:r.status,body:r.status===204?null:await r.json()};}
 const rooms=await request('GET','/api/rooms');const roomId=rooms.body[0].id;
 const booking={roomId,title:'Session',bookedBy:'Junior',startsAt:'2030-03-10T10:00:00Z',endsAt:'2030-03-10T11:00:00Z'};
 const race=await Promise.all([request('POST','/api/bookings',booking),request('POST','/api/bookings',booking)]);
 assert.deepEqual(race.map(x=>x.status).sort(),[201,409]);
 const original=race.find(x=>x.status===201)!.body;
 const adjacent=await request('POST','/api/bookings',{...booking,startsAt:booking.endsAt,endsAt:'2030-03-10T12:00:00Z'});assert.equal(adjacent.status,201);
 const failed=await request('PUT',`/api/bookings/${original.id}`,{...booking,endsAt:'2030-03-10T11:30:00Z'});assert.equal(failed.status,409);
 const persisted=await admin.query('SELECT ends_at FROM bookings WHERE id=$1',[original.id]);assert.equal(persisted.rows[0].ends_at.toISOString(),booking.endsAt.replace('Z','.000Z'));
 const changed=await request('PUT',`/api/bookings/${original.id}`,{...booking,title:'Renamed'});assert.equal(changed.status,200);assert.equal(changed.body.id,original.id);
 for(const change of [{title:42},{startsAt:'2030-02-30T10:00:00Z'},{startsAt:'2030-03-10T10:00'},{endsAt:booking.startsAt}]) assert.equal((await request('POST','/api/bookings',{...booking,...change})).status,400);
 assert.equal((await request('GET','/api/bookings?date=2030-02-30')).status,400);
 assert.equal((await request('DELETE','/api/bookings/not-a-uuid')).status,400);
 const window=new URLSearchParams({roomId,dayStart:'2030-03-10T10:30:00Z',dayEnd:'2030-03-10T11:00:00Z'});
 const filtered=await request('GET','/api/bookings?'+window);assert.deepEqual(filtered.body.map((x:any)=>x.id),[original.id]);
});
test('equivalent offset timestamps normalize and malformed bodies are domain errors',()=>{
 const body={roomId:'00000000-0000-0000-0000-000000000001',title:'T',bookedBy:'J',startsAt:'2030-03-10T03:00:00-07:00',endsAt:'2030-03-10T04:00:00-07:00'};
 assert.equal(parseBooking(body).startsAt,'2030-03-10T10:00:00.000Z');
 for(const value of [null,[],{...body,roomId:42},{...body,title:{}}]) assert.throws(()=>parseBooking(value));
});
''',encoding='utf-8')
print('Wrote PostgreSQL, HTTP and controlled-network tests for the remaining three projects.')
