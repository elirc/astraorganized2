from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent;p=b/'stage/529eba39810c'
(p/'tests/runtime-refund-scope.test.mjs').write_text('''import assert from 'node:assert/strict';
import test from 'node:test';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const input={paymentId:'pay-1',amountMinor:40,reason:'customer request',session:{userId:'u1',email:'u@example.test'}};
async function fixture(options={}) {
  const calls=[],tx=Object.freeze({transaction:true});
  function effect(name,client){assert.equal(client,tx);calls.push(name);}
  const service=await loadTypeScript('src/services/refundService.ts',{root,globals:{crypto:{randomUUID:()=> 'fixed-uuid'}},stubs:{
    '@prisma/client':{RefundStatus:{PENDING:'PENDING',SUCCEEDED:'SUCCEEDED'}},
    '../lib/db':{prisma:{$transaction:async fn=>{calls.push('transaction');return fn(tx);}}},
    '../repositories/paymentRepository':{
      findPaymentById:async(id,client)=>{effect('payment',client);assert.equal(id,'pay-1');return options.missing?null:{id,amountMinor:100,status:options.status||'SUCCEEDED'};},
      transitionPaymentStatus:async(data,client)=>{effect('payment-status',client);assert.equal(data.paymentId,'pay-1');assert.equal(data.nextStatus,'REFUNDED');}
    },
    '../repositories/refundRepository':{
      sumSuccessfulRefundsForPayment:async(id,client)=>{effect('sum',client);assert.equal(id,'pay-1');return options.refunded??60;},
      createRefund:async(data,client)=>{effect('create',client);assert.equal(data.createdByUserId,'u1');assert.equal(data.paymentId,'pay-1');assert.equal(data.reason,input.reason);return {id:'refund-1',...data};},
      transitionRefundStatus:async(id,status,provider,client)=>{effect('refund-status',client);assert.equal(id,'refund-1');assert.equal(status,'SUCCEEDED');assert.equal(provider,'prov_ref_fixed-uuid');}
    },
    '../repositories/paymentEventRepository':{createPaymentEvent:async(data,client)=>{
      effect(data.type,client);assert.equal(data.paymentId,'pay-1');assert.equal(data.actorUserId,'u1');assert.equal(data.actorLabel,'u@example.test');
      if(options.eventError)throw options.eventError;
    }}
  }});
  return {calls,run:()=>service.createRefundForPayment(input)};
}
test('full remaining refund binds both reads and every write to one transaction client',async()=>{
  const f=await fixture();const result=await f.run();assert.equal(result.paymentStatus,'REFUNDED');assert.equal(result.refundStatus,'SUCCEEDED');
  assert.equal(result.refundId,'refund-1');assert.equal(result.providerRefundId,'prov_ref_fixed-uuid');
  assert.deepEqual(f.calls,['transaction','payment','sum','create','REFUND_REQUESTED','refund-status','payment-status','REFUND_SUCCEEDED']);
});
test('partial refund keeps payment succeeded and omits full-refund transition',async()=>{
  const f=await fixture({refunded:10});assert.equal((await f.run()).paymentStatus,'SUCCEEDED');
  assert.deepEqual(f.calls,['transaction','payment','sum','create','REFUND_REQUESTED','refund-status','REFUND_SUCCEEDED']);
});
test('real refund policy rejects excess amount and ineligible payment before writes',async()=>{
  for(const [options,code] of [[{refunded:80},'REFUND_AMOUNT_EXCEEDS_CAPTURE'],[{status:'FAILED'},'PAYMENT_NOT_REFUNDABLE']]) {
    const f=await fixture(options);await assert.rejects(f.run(),e=>e.status===409&&e.code===code);assert.deepEqual(f.calls,['transaction','payment','sum']);
  }
});
test('missing payment stops before aggregation and creation',async()=>{
  const f=await fixture({missing:true});await assert.rejects(f.run(),e=>e.status===404&&e.code==='PAYMENT_NOT_FOUND');assert.deepEqual(f.calls,['transaction','payment']);
});
test('event failure preserves identity and stops later success transitions',async()=>{
  const failure=new Error('event write failed'),f=await fixture({eventError:failure});await assert.rejects(f.run(),e=>e===failure);
  assert.deepEqual(f.calls,['transaction','payment','sum','create','REFUND_REQUESTED']);
});
''',encoding='utf-8')
f=b/'specs/529eba39810c.json';s=json.loads(f.read_text(encoding='utf-8-sig'));s['changedFiles']=[n for n in s['changedFiles'] if not n.startswith('astraupskill/evidence/')];s['limits']=['Five runtime cases execute actual refund service, state machine and RouteError with explicit repository/transaction/UUID adapters. No native Prisma, PostgreSQL, HTTP or provider payment operation was executed.','Passing the transaction client keeps reads and writes in the same transaction, but default isolation does not by itself prevent simultaneous refunds from exceeding the allowance. No locking, serializable retry or durable idempotency was added.','The existing service simulates provider success with a generated id; tests do not establish real-provider refunds, real database rollback or request authorization.'];f.write_text(json.dumps(s,indent=2),encoding='utf-8')
