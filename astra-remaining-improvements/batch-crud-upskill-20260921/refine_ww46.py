from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/7ff66e57d973'
p=P/'tests/runtime-project-status-race.test.mjs';t=p.read_text();t='\n'.join(l for l in t.split('\n') if not l.startswith('class HttpError') and "'@/lib/http/http-error': { HttpError }" not in l)
t=t.replace('missing = false }','missing = false, reloadMissing = false, failUpdate = false }')
t=t.replace("const calls = []; let phase = 'before';", "const calls = []; const tx = {}; const error = new Error('update unavailable'); let phase = 'before';")
t=t.replace('async input => { calls.push([\'find\'', "async (input, client) => { if (phase === 'after') assert.equal(client, tx); calls.push(['find'")
t=t.replace('return missing ? null :', "return (missing || (reloadMissing && phase === 'after')) ? null :")
t=t.replace("updateProjectStatus: async input => {", "updateProjectStatus: async (input, client) => { assert.equal(client, tx);")
t=t.replace("if (count === 1) phase = 'after';", "if (failUpdate) throw error; if (count === 1) phase = 'after';")
t=t.replace("return fn({ name: 'transaction' });", "return fn(tx);")
t=t.replace('return { calls, repos, db };','return { calls, repos, db, error, tx };')
t=t.replace("createAuditLog: async data => f.calls.push(['audit', data.action])", "createAuditLog: async (data,client) => { assert.equal(client,f.tx); assert.deepEqual(JSON.parse(JSON.stringify(data.metadata)),{from:'ACTIVE',to:'ARCHIVED'}); return f.calls.push(['audit', data.action]); }")
t+='''
test('missing post-update reload refuses without audit',async()=>{
 const f=fixture({reloadMissing:true});const m=await serviceFor(f);
 await assert.rejects(m.transitionOrganizationProjectStatus(input),e=>e.status===500);
 assert.deepEqual(f.calls.map(x=>x[0]),['find','update','find']);
});
test('repository failure preserves identity and prevents reread and audit',async()=>{
 const f=fixture({failUpdate:true});const m=await serviceFor(f);
 await assert.rejects(m.transitionOrganizationProjectStatus(input),e=>e===f.error);
 assert.deepEqual(f.calls.map(x=>x[0]),['find','update']);
});
test('actual repository update predicate includes organization and id but no previous status',async()=>{
 const calls=[];const result={count:1};const db={project:{updateMany:async args=>{calls.push(args);return result;}}};
 const r=await loadTypeScript('src/repositories/project-repository.ts',{root,stubs:{'@prisma/client':enums,'@/lib/db':{prisma:db}}});
 assert.equal(await r.updateProjectStatus({organizationId:'org-1',projectId:'project-1',status:'ARCHIVED'},db),result);
 assert.deepEqual(JSON.parse(JSON.stringify(calls)),[{where:{id:'project-1',organizationId:'org-1'},data:{status:'ARCHIVED'}}]);
});
''';p.write_text(t)
s=B/'specs/7ff66e57d973.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['summary']=[n.replace('four runtime','seven runtime') for n in d['summary']];d['limits'].append('The repository predicate includes organization and id, not expected status; count checking is not optimistic concurrency control. Real HttpError and role/status policy execute with generated enum adapters.');s.write_text(json.dumps(d,indent=2))
