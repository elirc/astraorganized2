from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/330bb6feda2f'
f=P/'lib/server/privacy.ts';s=f.read_text()
s=s.replace('const identifiers = new Set(person?.identifiers ?? [distinctId]);','const identifiers = new Set(person ? [...person.identifiers, person.canonicalDistinctId] : [distinctId]);')
s=s.replace('const incomingDistinctId = payload.distinct_id || payload.user_id;\n      if (raw.projectId !== projectId || !identifiers.has(incomingDistinctId)) {','const matchesIdentifier =\n        (payload.distinct_id !== undefined && identifiers.has(payload.distinct_id)) ||\n        (payload.user_id !== undefined && identifiers.has(payload.user_id));\n      if (raw.projectId !== projectId || !matchesIdentifier) {')
f.write_text(s,encoding='utf-8')
t=P/'tests/runtime-privacy-alias-delete.test.mjs';s=t.read_text(encoding='utf-8-sig')
s += '''
async function runDelete(data, target) {
 const subject = await loadTypeScript('lib/server/privacy.ts', {root, aliasRoot:root, stubs:{
  '@/lib/server/ids':{id:()=> 'audit-expanded'}, '@/lib/server/clock':{nowIso:()=> 'fixed'},
  '@/lib/server/store':{mutateData:async cb=>cb(data),readData:async()=>data}
 }});
 await subject.deletePersonData('project-1',target,'actor-1');
}
test('alias input discovers canonical-only and mapped-only history while preserving another project',async()=>{
 const data=structuredClone(fixture);
 data.persons[0].identifiers=['device-7'];
 data.personAliases.push({projectId:'project-1',alias:'mapped-only',canonicalDistinctId:'user-1'});
 data.events.push({id:'mapped',projectId:'project-1',distinctId:'mapped-only',properties:{email:'x',phone:'y'}});
 data.eventsRaw.push({id:'mixed',projectId:'project-1',payload:{distinct_id:'other-device',user_id:'user-1',$set:{email:'x',phone:'y'}}});
 const foreign={id:'foreign',projectId:'project-2',distinctId:'device-7',properties:{email:'keep'}};
 const foreignAlias={projectId:'project-2',alias:'device-7',canonicalDistinctId:'user-1'};
 data.events.push(foreign);data.personAliases.push(foreignAlias);
 await runDelete(data,'device-7');
 for(const id of ['event-main','event-alias','mapped']) {
  const row=data.events.find(x=>x.id===id);assert.equal(row.distinctId,'anon_'+id);assert.equal(row.properties.email,undefined);assert.equal(row.properties.phone,undefined);
 }
 assert.equal(data.events.find(x=>x.id==='foreign'),foreign);
 assert.equal(data.personAliases.find(x=>x.projectId==='project-2'),foreignAlias);
 assert.equal(data.personAliases.some(x=>x.projectId==='project-1'&&['device-7','mapped-only'].includes(x.alias)),false);
 const raw=data.eventsRaw.find(x=>x.id==='mixed').payload;
 assert.equal(raw.distinct_id,'anon_mixed');assert.equal(raw.user_id,undefined);assert.equal(raw.$set.email,null);assert.equal(raw.$set.phone,null);
 assert.equal(data.persons[0].canonicalDistinctId,'anon_person-1');assert.deepEqual(Array.from(data.persons[0].identifiers),['anon_person-1']);assert.equal(data.persons[0].properties.email,null);
 assert.equal(data.audits[0].actorUserId,'actor-1');assert.equal(data.audits[0].metadata.distinctId,'device-7');
});
test('missing person still scrubs matching orphan history and preserves unrelated rows',async()=>{
 const data=structuredClone(fixture);data.persons=[];
 await runDelete(data,'device-7');
 assert.equal(data.events.find(x=>x.id==='event-alias').distinctId,'anon_event-alias');
 assert.equal(data.events.find(x=>x.id==='event-main').distinctId,'user-1');
 assert.equal(data.eventsRaw[0].payload.distinct_id,'anon_raw-alias');
 assert.equal(data.personAliases.some(x=>x.alias==='device-7'),false);assert.equal(data.audits.length,1);
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/330bb6feda2f.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'))
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Four actual privacy-service runtime cases use explicit store, id and clock adapters; no Next route, real authorization, filesystem durability or concurrent mutation executed.', 'This bounded change expands identifier matching and alias cleanup in the existing scrubber. It is not complete erasure: other properties, userProperties, sessions, derived tables and audit metadata are not comprehensively scrubbed.', 'No-person deletion still scrubs exact matching event/raw history and aliases; only a completely unmatched id changes audit alone. Export behavior is unchanged.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
