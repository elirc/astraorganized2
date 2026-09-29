from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/5c252a248ab8'
(P/'tests/runtime-country-rule-upsert.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const {createComplianceRepository}=await loadTypeScript('src/repositories/prisma/complianceRepository.ts',{root});
const base={countryCode:'US',ruleKey:'minimum_wage',ruleValue:{amount:20},effectiveFrom:new Date('2026-01-01T00:00:00Z'),isActive:true};
const plain=x=>JSON.parse(JSON.stringify(x));
function fixture(){const calls=[];const result={id:'returned-rule'};return {calls,result,repo:createComplianceRepository({countryRule:{upsert:async args=>{calls.push(args);return result;}}})};}
test('complete composite selector and create payload reach actual upsert',async()=>{
 const f=fixture();assert.equal(await f.repo.upsertRule('tenant-a',base),f.result);
 assert.deepEqual(plain(f.calls[0].where),{tenantId_countryCode_ruleKey_effectiveFrom:{tenantId:'tenant-a',countryCode:'US',ruleKey:'minimum_wage',effectiveFrom:base.effectiveFrom.toISOString()}});
 assert.deepEqual(plain(f.calls[0].create),plain({tenantId:'tenant-a',...base}));
});
test('repeat input keeps identity and updates only mutable fields',async()=>{
 const f=fixture();await f.repo.upsertRule('tenant-a',base);
 const changed={...base,ruleValue:{amount:22},effectiveTo:new Date('2026-12-31T00:00:00Z'),isActive:false};await f.repo.upsertRule('tenant-a',changed);
 assert.deepEqual(plain(f.calls[1].where),plain(f.calls[0].where));
 assert.deepEqual(plain(f.calls[1].update),{ruleValue:{amount:22},effectiveTo:changed.effectiveTo.toISOString(),isActive:false});
});
test('different tenant produces a different selector and create tenant',async()=>{
 const f=fixture();for(const tenant of ['tenant-a','tenant-b'])await f.repo.upsertRule(tenant,base);
 assert.notDeepEqual(plain(f.calls[0].where),plain(f.calls[1].where));
 assert.equal(f.calls[1].where.tenantId_countryCode_ruleKey_effectiveFrom.tenantId,'tenant-b');assert.equal(f.calls[1].create.tenantId,'tenant-b');
});
test('database rejection is preserved rather than reported as a saved rule',async()=>{
 const failure=new Error('database unavailable');let count=0;
 const repo=createComplianceRepository({countryRule:{upsert:async()=>{count++;throw failure;}}});
 await assert.rejects(repo.upsertRule('tenant-a',base),e=>e===failure);assert.equal(count,1);
});
''')
s=B/'specs/5c252a248ab8.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];s.write_text(json.dumps(d,indent=2))
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace(".''",'.').replace('Two tests','Four tests').replace('two tests','four tests').replace('two passing','four passing').replace('2 tests passed','4 tests passed').replace('evidence/5c252a248ab8-runtime-country-rule-upsert.tap.txt','evidence/crud-b06-astra-runtime.log')
 t=t.replace('| observed result | rule-1 | rule-1 |','| observed result | adapter return | adapter return |')
 t=t.replace('the returned stub still uses the same fake ID','the adapter return is independent of the selector')
 if p.name=='VERIFICATION.md':t+='\nAdditional cases check different tenant arguments and identity-preserving propagation of a database rejection. Each test owns its fixture, so repeat-write assertions do not depend on a previous test running. The adapter does not choose insert versus update or persist rows. An omitted effectiveTo remains undefined in update; it does not explicitly clear an existing end date.\n'
 p.write_text(t,encoding='utf-8')
