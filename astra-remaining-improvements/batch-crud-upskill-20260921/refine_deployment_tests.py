from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent;p=b/'stage/2906d0b177f3'
f=p/'tests/runtime-deployment-ownership.test.mjs';s=f.read_text(encoding='utf-8-sig')
s=s.replace('where: [], create: []','where: [], create: [], team: [], policy: []')
s=s.replace('calls.where.push(args); return environment;', 'calls.where.push(args); return environment && environment.id === args.where.id && (!args.where.applicationId || environment.applicationId === args.where.applicationId) ? environment : null;')
s=s.replace("getTeamRole: async () => 'OWNER'", "getTeamRole: async args => { f.calls.team.push(args); return 'OWNER'; }")
s=s.replace("canDeployToEnvironment: () => true, canPerform: () => true", "canDeployToEnvironment: (...args) => { f.calls.policy.push(['environment',...args]); return true; }, canPerform: (...args) => { f.calls.policy.push(['action',...args]); return true; }")
s=s.replace('const f = fixture(null); const route', "const f = fixture({ id:'env-from-app-b', applicationId:'app-b' }); const route")
s=s.replace('assert.equal(f.calls.create.length, 0);\n});', 'assert.equal(f.calls.create.length, 0);\n  assert.equal(f.calls.team.length, 0); assert.equal(f.calls.policy.length, 0);\n});',1)
s=s.replace("assert.equal(f.calls.create[0].actorUserId, 'actor-1');", "assert.equal(f.calls.create[0].actorUserId, 'actor-1');\n  assert.equal(JSON.stringify(f.calls.team), JSON.stringify([{userId:'actor-1',teamId:'team-a'}]));\n  assert.deepEqual(f.calls.policy, [['action','OWNER','deploy'],['environment','OWNER','staging']]);\n  assert.equal(f.calls.create[0].version,'1.2.3');")
f.write_text(s,encoding='utf-8')
f=b/'specs/2906d0b177f3.json';spec=json.loads(f.read_text(encoding='utf-8-sig'));spec['id']='2906d0b177f3';spec['project']='_Organized Desktop/04 JavaScript Training/jstrain2.4';spec['changedFiles']=[x for x in spec['changedFiles'] if not x.startswith('astraupskill/evidence/')];spec['limits']=[x for x in spec['limits'] if not x.startswith('Nine course')];spec['limits'].append('Other deployment creation callers and GET behavior are unchanged; the guard validates the relationship at lookup time and does not make later writes atomic.');f.write_text(json.dumps(spec,indent=2),encoding='utf-8')
