from pathlib import Path
import json,shutil
b=Path(__file__).resolve().parent.parent;p=b/'stage/195e77d61335';app=p/'social-app'
course=p/'astraupskill';snap=course/'snapshots';snap.mkdir(parents=True,exist_ok=True)
for rel,name in [('src/state/queries/profile.ts','profile.ts.original.txt'),('package.json','package.json.original.txt')]:
 f=app/rel;target=snap/name;assert not target.exists();target.write_bytes(f.read_bytes())
f=app/'src/state/queries/profile.ts';s=f.read_text();start=s.index('function useProfileUnblockMutation()');a=s[:start];z=s[start:];old='    onSuccess(_, {did}) {\n      resetProfilePostsQueries(queryClient, did, 1000)';assert old in z;z=z.replace(old,'    onSuccess(_, {did}) {\n      void queryClient.invalidateQueries({queryKey: RQKEY_MY_BLOCKED()})\n      resetProfilePostsQueries(queryClient, did, 1000)',1);f.write_text(a+z,encoding='utf-8')
f=app/'package.json';s=f.read_text();anchor='    "test": ';assert anchor in s;s=s.replace(anchor,'    "test:crud-upskill": "node --experimental-vm-modules --test tests/crud-upskill/profile-unblock.test.mjs",\n'+anchor,1);f.write_text(s,encoding='utf-8')
t=app/'tests/crud-upskill';t.mkdir(parents=True,exist_ok=True);shutil.copyfile(b/'batch-crud-upskill-20260921/test-tools/load-typescript.mjs',t/'load-typescript.mjs')
(t/'profile-unblock.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
import vm from 'node:vm';
import {loadTypeScript} from './load-typescript.mjs';

const root = fileURLToPath(new URL('../../', import.meta.url));
const source = readFileSync(new URL('../../src/state/queries/profile.ts', import.meta.url), 'utf8');
const start = source.indexOf('function useProfileUnblockMutation()');
const end = source.indexOf('async function whenAppViewReady(', start);
assert.ok(start >= 0 && end > start, 'production hook boundaries exist');
const hookSource = stripTypeScriptTypes(source.slice(start, end));
const blocked = await loadTypeScript('src/state/queries/my-blocked-accounts.ts', {root, stubs:{
  '@tanstack/react-query': {useInfiniteQuery:()=>{}}, '#/state/session':{useAgent:()=>{}}
}});
function fixture({account={did:'did:actor'}, deleteImpl=async()=>{}}={}) {
  const calls={deletes:[],invalidations:[],resets:[]};
  const queryClient={invalidateQueries:async args=>{calls.invalidations.push(args);}};
  const context={
    useSession:()=>({currentAccount:account}), useQueryClient:()=>queryClient,
    useAgent:()=>({app:{bsky:{graph:{block:{delete:async args=>{calls.deletes.push(args);return deleteImpl(args);}}}}}}),
    useMutation:options=>options,
    AtUri:class {constructor(uri){this.rkey=uri.split('/').at(-1);}},
    RQKEY_MY_BLOCKED:blocked.RQKEY,
    resetProfilePostsQueries:(client,did,delay)=>{assert.equal(client,queryClient);calls.resets.push({did,delay});}
  };
  const mutation=vm.runInNewContext(hookSource+';useProfileUnblockMutation()',context);
  // Model the library lifecycle explicitly; React/TanStack are not mounted.
  const run=async variables=>{const value=await mutation.mutationFn(variables);await mutation.onSuccess(value,variables);};
  return {calls,mutation,run};
}
const variables={did:'did:target',blockUri:'at://did:actor/app.bsky.graph.block/block-1'};
const plain=value=>JSON.parse(JSON.stringify(value));

test('successful unblock deletes the record and invalidates the real blocked-list key',async()=>{
  const f=fixture();await f.run(variables);
  assert.deepEqual(plain(f.calls.deletes),[{repo:'did:actor',rkey:'block-1'}]);
  assert.deepEqual(plain(f.calls.invalidations),[{queryKey:['my-blocked-accounts']}]);
  assert.deepEqual(f.calls.resets,[{did:'did:target',delay:1000}]);
});
test('signed-out mutation rejects before remote deletion or success effects',async()=>{
  const f=fixture({account:undefined});
  // Pass null because destructuring defaults intentionally represent a signed-in fixture.
  const signedOut=fixture({account:null});
  await assert.rejects(signedOut.run(variables),/Not signed in/);
  assert.deepEqual(signedOut.calls,{deletes:[],invalidations:[],resets:[]});
});
test('remote deletion error retains identity and never reaches success invalidation',async()=>{
  const failure=new Error('remote unavailable');const f=fixture({deleteImpl:async()=>{throw failure;}});
  await assert.rejects(f.run(variables),e=>e===failure);
  assert.equal(f.calls.deletes.length,1);assert.deepEqual(f.calls.invalidations,[]);assert.deepEqual(f.calls.resets,[]);
});
test('pending deletion does not publish success and resolves before both cache effects',async()=>{
  let resolve;const pending=new Promise(r=>{resolve=r;});const f=fixture({deleteImpl:()=>pending});
  const operation=f.run(variables);await Promise.resolve();
  assert.equal(f.calls.deletes.length,1);assert.equal(f.calls.invalidations.length,0);assert.equal(f.calls.resets.length,0);
  resolve();await operation;assert.equal(f.calls.invalidations.length,1);assert.equal(f.calls.resets.length,1);
});
''',encoding='utf-8')
spec={'id':'195e77d61335','project':'_Organized Desktop/05 Numbered Experiments/rn1','summary':['Invalidate the blocked-accounts query after successful unblock so the deletion is reflected in the cached list, matching the existing block path.','Preserve remote deletion, signed-out rejection and profile feed reset behavior; add a portable Yarn learning test script.'],'changedFiles':['social-app/src/state/queries/profile.ts','social-app/package.json','social-app/tests/crud-upskill/profile-unblock.test.mjs','social-app/tests/crud-upskill/load-typescript.mjs','astraupskill/snapshots/profile.ts.original.txt','astraupskill/snapshots/package.json.original.txt'],'checks':{'format':'json','resultsFile':'checks/195e77d61335/results-crud-b04.json'},'limits':['Four focused cases execute the exact extracted production unblock hook and actual blocked-query key, using session/agent/query-client/AtUri doubles and an explicitly modeled mutation lifecycle.','No mounted React, TanStack cache engine, real AT Protocol server, native Jest, lint, typecheck, Expo or mobile/browser rendering was executed.','Invalidation schedules query refresh; this does not prove immediate removal from every list, successful refetch, rollback, request idempotency or session-switch safety.']}
(b/'specs/195e77d61335.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
