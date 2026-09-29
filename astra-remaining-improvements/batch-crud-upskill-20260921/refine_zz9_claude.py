from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/3ee259e51792'
t=P/'tests/runtime-case-clearable-fields.test.mjs';s=t.read_text()
s='\n'.join(l for l in s.splitlines() if not any(x in l for x in ["'@/lib/auth/authorize':","'@/lib/errors':","'@/lib/workflow/caseWorkflow':"]))
s=s.replace("CASE_WORKER: 'CASE_WORKER'","CASE_WORKER: 'CASE_WORKER', TEAM_LEAD:'TEAM_LEAD',AUDITOR:'AUDITOR'")
s+='''
test('present nonempty values pass through, and foreign team or auditor refuse before write',async()=>{
 const h=makeHarness();const {updateCase}=await loadTypeScript('src/services/caseService.ts',{root,stubs:h.stubs});
 await updateCase(h.actor,'case-1',{requesterEmail:'new@example.test',sourceSystem:'portal'});assert.equal(h.writes[0].requesterEmail,'new@example.test');assert.equal(h.writes[0].sourceSystem,'portal');
 for(const actor of [{id:'w',role:'CASE_WORKER',teamId:'foreign'},{id:'a',role:'AUDITOR',teamId:null}]){const d=makeHarness();const m=await loadTypeScript('src/services/caseService.ts',{root,stubs:d.stubs});await assert.rejects(m.updateCase(actor,'case-1',{sourceSystem:''}),e=>e.status===403);assert.equal(d.writes.length,0);}
});
test('real team scope reaches repository and restricted notes are filtered for worker',async()=>{
 const h=makeHarness();let scope;h.existing.notes=[{id:'public',isRestricted:false},{id:'private',isRestricted:true}];
 h.stubs['@/repositories/caseRepository'].findCaseById=async(id,where)=>{assert.equal(id,'case-1');scope=where;return h.existing;};
 const {updateCase}=await loadTypeScript('src/services/caseService.ts',{root,stubs:h.stubs});const out=await updateCase({id:'w',role:'CASE_WORKER',teamId:'team-1'},'case-1',{sourceSystem:''});
 assert.deepEqual(JSON.parse(JSON.stringify(scope)),{owningTeamId:'team-1'});assert.deepEqual(Array.from(out.notes,n=>n.id),['public']);
});
''';t.write_text(s+'\n',encoding='utf-8')
p=B/'specs/3ee259e51792.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x];s['summary'].append('Five actual-service cases execute real permissions, team scope, note filtering and domain errors.');p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
P=B/'stage/fa998c611f1d';t=P/'tests/runtime-experiment-route.test.mjs';s=t.read_text();s=s.replace("const state = { row: initial, updates: [] };","const state = { row: initial, updates: [], predicates: [], removeAfterWrite:false };")
s=s.replace("where: () => ({ run: () => { state.updates.push(data); if (state.row) state.row = { ...state.row, ...data }; } })","where: predicate => ({ run: () => { state.predicates.push(predicate);state.updates.push(data); if (state.row) state.row = { ...state.row, ...data };if(state.removeAfterWrite)state.row=null; } })")
s+='''
test('existing PATCH serializes tags, scopes update and returns merged fields',async()=>{
 const h=harness({id:'exp-1',title:'Old',tags:'[]',status:'active'});const {PATCH}=await loadTypeScript('src/app/api/experiments/[id]/route.ts',{root,stubs:h.stubs});
 const response=await PATCH({json:async()=>({title:'New',tags:['crud'],status:'completed',unexpected:'ignored'})},{params:Promise.resolve({id:'exp-1'})});
 assert.equal(response.status,200);assert.equal(response.body.title,'New');assert.deepEqual(Array.from(response.body.tags),['crud']);assert.equal(h.state.updates[0].tags,'["crud"]');assert.equal(Object.hasOwn(h.state.updates[0],'unexpected'),false);assert.ok(Number.isInteger(h.state.updates[0].completedAt));assert.equal(h.state.predicates[0].id,'exp-1');
});
test('PATCH returns404 if reread disappears after write adapter',async()=>{
 const h=harness({id:'exp-1',tags:'[]'});h.state.removeAfterWrite=true;const {PATCH}=await loadTypeScript('src/app/api/experiments/[id]/route.ts',{root,stubs:h.stubs});const response=await PATCH({json:async()=>({title:'New'})},{params:Promise.resolve({id:'exp-1'})});assert.equal(response.status,404);assert.equal(h.state.updates.length,1);
});
''';t.write_text(s,encoding='utf-8')
p=B/'specs/fa998c611f1d.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x];s['summary'].append('Five runtime route cases also cover successful PATCH payload/tag serialization and missing post-write reread.');s['limits'].append('DELETE uses a pre-read and does not inspect affected-row count; concurrent disappearance after lookup remains outside this fix.');p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
