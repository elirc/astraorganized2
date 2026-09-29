from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parent.parent;p=b/'stage/06f66ec88e8d'
baseline=json.loads((b/'baselines/06f66ec88e8d.json').read_text(encoding='utf-8-sig'))
rel='src/services/admin/gateway-route-service.test.ts';raw=(p/'astraupskill/snapshots'/rel).read_bytes();assert hashlib.sha256(raw).hexdigest()==baseline['files'][rel];(p/rel).write_bytes(raw)
(p/'tests/runtime-route-status.test.mjs').write_text('''import assert from 'node:assert/strict';
import test from 'node:test';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const actor={userId:'u1',role:'OPERATIONS_ENGINEER',email:'ops@example.test',name:'Ops',accessibleServiceIds:['svc1']};
async function fixture(options={}) {
  const calls={reads:[],updates:[],transactions:0};const tx=Object.freeze({transaction:true});
  const route=options.missing?null:{id:'r1',status:options.status||'DRAFT',policies:options.noPolicy?[]:[{id:'p1'}]};
  const result={id:'r1',status:'ACTIVE'};
  const repo={findAccessibleRouteById:async(...args)=>{calls.reads.push(args);return route;},
    updateGatewayRouteStatus:async(client,id,status)=>{assert.equal(client,tx);calls.updates.push({id,status});if('error' in options)throw options.error;return result;},
    listAccessibleRoutes:async()=>[],createGatewayRoute:async()=>{}};
  const prisma={$transaction:async fn=>{calls.transactions++;return fn(tx);}};
  const service=await loadTypeScript('src/services/admin/gateway-route-service.ts',{root,stubs:{
    '@prisma/client':{GatewayRouteStatus:{},UserRole:{}},'@/lib/prisma':{prisma},
    '@/repositories/gateway-route-repository':repo,'@/repositories/upstream-service-repository':{findAccessibleServiceById:async()=>null}
  }});
  return {service,calls,result,run:(who=actor,next='ACTIVE')=>service.transitionRouteStatus(who,'r1',next)};
}
test('P2025 after successful pre-read maps to the real 404 AppError',async()=>{
  const f=await fixture({error:{code:'P2025'}});await assert.rejects(f.run(),e=>e.status===404&&e.message==='Route not found'&&e.constructor.name==='AppError');
  assert.equal(f.calls.transactions,1);assert.deepEqual(f.calls.updates,[{id:'r1',status:'ACTIVE'}]);
});
test('unrelated object and primitive persistence failures preserve identity',async()=>{
  for(const error of [new Error('database unavailable'),{code:'P2002'},null,'failure']) {
    const f=await fixture({error});let caught=false;try{await f.run();}catch(actual){caught=true;assert.equal(actual,error);}assert.equal(caught,true);
  }
});
test('successful legal transition returns the repository result through the same transaction',async()=>{
  const f=await fixture();assert.equal(await f.run(),f.result);assert.equal(f.calls.transactions,1);
  assert.equal(f.calls.reads[0][0],actor);assert.equal(f.calls.reads[0][1],'r1');assert.deepEqual(f.calls.updates,[{id:'r1',status:'ACTIVE'}]);
});
test('real role policy rejects analysts before lookup or transaction',async()=>{
  const f=await fixture();await assert.rejects(f.run({...actor,role:'ANALYST'}),e=>e.status===403);
  assert.deepEqual(f.calls,{reads:[],updates:[],transactions:0});
});
test('missing pre-read, illegal transition and missing active policy never write',async()=>{
  for(const [options,next,status] of [[{missing:true},'ACTIVE',404],[{status:'PAUSED'},'DEGRADED',409],[{noPolicy:true},'ACTIVE',400]]) {
    const f=await fixture(options);await assert.rejects(f.run(actor,next),e=>e.status===status);
    assert.equal(f.calls.transactions,0);assert.equal(f.calls.updates.length,0);
  }
});
''',encoding='utf-8')
f=b/'specs/06f66ec88e8d.json';s=json.loads(f.read_text(encoding='utf-8-sig'));s['changedFiles']=[n for n in s['changedFiles'] if n not in [rel,'astraupskill/snapshots/'+rel] and not n.startswith('astraupskill/evidence/')];s['limits']=['Five runtime cases execute actual transition service, AppError and role policy with repository and Prisma transaction adapters. Native Vitest, Prisma/PostgreSQL and Next HTTP middleware were not run.','P2025 is simulated after a successful pre-read; no real concurrent delete or transaction rollback was executed. Status and policy preconditions remain separate reads and are not made atomic by this error translation.'];f.write_text(json.dumps(s,indent=2),encoding='utf-8')
