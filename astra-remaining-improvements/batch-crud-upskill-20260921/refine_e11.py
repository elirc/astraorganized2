from pathlib import Path
import json,re
b=Path(__file__).resolve().parent.parent;p=b/'stage/3b0530b090c4'
f=p/'server/store.ts';s=f.read_text(encoding='utf-8-sig');start=s.index('export const createShareRecord');s=s[:start]+s[start:].replace('if (!db.rooms[roomId]) {','if (!Object.hasOwn(db.rooms, roomId) || !db.rooms[roomId]) {',1);f.write_text(s,encoding='utf-8')
(p/'tests/share-room-integrity.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
async function fixture(options={}) {
  const state={db:{rooms:options.rooms||{},shares:{existing:{token:'existing',roomId:'old'}}},writes:0,tokens:0};
  const fs={mkdir:async()=>{},stat:async()=>{},readFile:async()=>{if(options.readError)throw options.readError;return JSON.stringify(state.db);},
    writeFile:async(_p,text)=>{state.writes++;if(options.writeError)throw options.writeError;state.db=JSON.parse(text);}};
  const mod=await loadTypeScript('server/store.ts',{root,globals:{process:{cwd:()=>root}},stubs:{
    'node:fs/promises':fs,'node:path':{default:path},nanoid:{nanoid:size=>{assert.equal(size,18);state.tokens++;return 'share-token';}},
    '../src/lib/scene.js':{emptyScene:()=>({}),mergeScenes:a=>a}
  }});
  return {state,mod};
}
test('missing and inherited room names never generate or persist a share',async()=>{
  for(const id of ['missing','__proto__','constructor','toString']) {
    const f=await fixture();await assert.rejects(f.mod.createShareRecord(id),/Room not found/);
    assert.equal(f.state.tokens,0);assert.equal(f.state.writes,0);assert.deepEqual(Object.keys(f.state.db.shares),['existing']);
  }
});
test('existing room creates one share and retains unrelated stored records',async()=>{
  const room={roomId:'room1',scene:{title:'Board'}};const f=await fixture({rooms:{room1:room}});
  const share=await f.mod.createShareRecord('room1');assert.equal(share.token,'share-token');assert.equal(share.roomId,'room1');
  assert.ok(Number.isFinite(share.createdAt));assert.equal(f.state.tokens,1);assert.equal(f.state.writes,1);
  assert.deepEqual(f.state.db.rooms.room1,room);assert.equal(f.state.db.shares.existing.token,'existing');
  const readback=await f.mod.getShareRecord('share-token');assert.equal(JSON.stringify(readback),JSON.stringify(share));
});
test('read failure propagates before token generation and share writes',async()=>{
  const failure=new Error('read unavailable'),f=await fixture({readError:failure});
  await assert.rejects(f.mod.createShareRecord('room1'),e=>e===failure);assert.equal(f.state.tokens,0);assert.equal(f.state.writes,0);
});
test('failed persistence does not return a successful share',async()=>{
  const failure=new Error('write unavailable'),f=await fixture({rooms:{room1:{roomId:'room1'}},writeError:failure});
  await assert.rejects(f.mod.createShareRecord('room1'),e=>e===failure);assert.equal(f.state.tokens,1);assert.equal(f.state.writes,1);
  assert.equal(Object.hasOwn(f.state.db.shares,'share-token'),false);
});
''',encoding='utf-8')
f=b/'specs/3b0530b090c4.json';s=json.loads(f.read_text(encoding='utf-8-sig'));s['summary'][0]='Require an own room-map entry before share token generation or persistence, rejecting missing and inherited object-property names.';s['limits']=['Four runtime cases execute actual store source with real Node path and explicit filesystem/nanoid/scene adapters; no Express, auth signing or real filesystem persistence was executed.','No-share-write assertions assume an initialized store; readDb may create initial directories/database when absent. File read-modify-write remains non-atomic and existing orphan shares are not migrated.','The existing route has no new explicit mapping of the service error to HTTP404; this fix establishes a store rejection, not a newly verified HTTP error contract.'];f.write_text(json.dumps(s,indent=2),encoding='utf-8')
for f in (p/'astraupskill').glob('*.md'):
 s=f.read_text(encoding='utf-8-sig')
 for a,c in {'route?s':"route's",'endpoint?s':"endpoint's",'?Room missing?':'"Room missing"','?it fails.?':'"it fails."'}.items():s=s.replace(a,c)
 paragraphs=s.split('\n\n');seen=set();unique=[]
 for q in paragraphs:
  if q.strip() and q.strip() in seen:continue
  seen.add(q.strip());unique.append(q)
 s='\n\n'.join(unique).replace('if (!db.rooms[roomId])','if (!Object.hasOwn(db.rooms, roomId) || !db.rooms[roomId])')
 s=s.replace('two passing subtests','four passing subtests').replace('two passing tests','four passing tests').replace('crud-b04-e11-runtime4','crud-b04-astra-runtime').replace('runtime4 is the final passing evidence','the expanded root run is the accepted evidence')
 s=s.replace('filesystem, path, nanoid, and scene doubles','filesystem, nanoid and scene doubles plus real Node path').replace('fs, path, nanoid, and scene imports','fs, nanoid and scene imports plus real Node path')
 s=s.replace('preserving existing callers and avoiding a fabricated share token','rejecting invalid creation before returning a fabricated share token')
 s=s.replace('normal creation cannot create that state','sequential creation from a valid store snapshot rejects an absent parent')
 s=s.replace('every stored share names an existing room at creation time','a successful share write was based on a snapshot containing an own room entry')
 s=s.replace('The patch prevents new orphans.','The patch rejects absent parents in the read snapshot; concurrent writes remain outside the guarantee.')
 s=s.replace('Preserve the existing error text so callers can continue handling failures consistently.','The message matches the neighboring saveRoomScene error, but this newly rejected share path has no added HTTP status mapping.')
 extras={
 'README.md':'Root review also checked object-map identity: inherited names such as constructor and __proto__ must not count as rooms. The guard uses Object.hasOwn before reading the entry. Four runtime cases include those names, valid readback, read failure and failed persistence. The route has no newly added 404 mapping for this store error.',
 '01-CODEBASE-MAP.md':'JSON.parse produces ordinary object maps, so property access can also find inherited properties. The own-property check is part of identifying a stored room. Trace it before the truthiness check, then inspect the parsed snapshot rather than assuming every JavaScript property represents persisted data.',
 '02-CONCEPTS.md':'An own-property test answers whether the JSON map stores that key. A truthiness check alone also accepts Object.prototype members, which are not room records. The combination rejects inherited names and invalid empty entries. Initialization is separate: readDb may create an empty database before this guard rejects a missing room.',
 '03-WORKED-CHANGE.md':'Try roomId constructor against an empty parsed rooms object. Ordinary property access returns an inherited function, so the first draft guard would continue. Object.hasOwn returns false and stops token creation. The expanded negative test makes that JavaScript object-model detail observable without inventing a database constraint.',
 '04-TESTING-AND-DEBUGGING.md':'The expanded suite checks inherited names and token-call counts, preserves unrelated records, reads the share back through the actual getter, and injects read/write errors. Real path handling is retained. Its stat adapter models initialized storage; zero writes must not be generalized to first-time database initialization.',
 '05-PRACTICE.md':'Add constructor and __proto__ as room ids in an empty parsed map. Predict property access versus Object.hasOwn, then explain which result should permit a child write. Finally, distinguish a failed database read from a missing room in a successfully read database; both reject, but only one is a domain absence.',
 '06-SOLUTIONS-AND-REVIEW.md':'Inherited constructor and __proto__ names fail Object.hasOwn and produce no token or share write in the initialized-store fixture. Read errors retain identity before token generation. Write errors retain identity after a token is generated; the caller receives no successful share. The suite does not prove real-disk atomicity or rollback.',
 '07-TRACE-LAB.md':'Use a compact ledger: missing/inherited parent -> read -> reject; valid parent -> read -> token -> write -> return; read error -> reject before token; write error -> token -> attempted write -> reject. The fixture assumes initialization already exists. A first-use trace may include initialization writes even for a missing room.',
 'VERIFICATION.md':'Four named cases now cover missing/inherited keys, successful persistence and getter readback, original read-error identity and original write-error identity. The no-write claim concerns share persistence in an initialized store. No assertion establishes HTTP404 for the new rejection, because the unchanged Express route has no explicit mapping for this error.'}
 s+='\n\n'+extras[f.name]+'\n';f.write_text(s,encoding='utf-8')
