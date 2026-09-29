from pathlib import Path
import json,re
B=Path(__file__).resolve().parent.parent;P=B/'stage/42df17f9e984'
f=P/'src/services/purchaseOrderService.ts';s=f.read_text()
old='''    const resultingReceivedQuantities = new Map(previouslyReceivedByLineItem);

    for (const incomingLineItem of input.lineItems) {
      resultingReceivedQuantities.set(
        incomingLineItem.purchaseOrderLineItemId,
        (resultingReceivedQuantities.get(incomingLineItem.purchaseOrderLineItemId) ?? 0) +
          incomingLineItem.quantityReceived,
      );
    }'''
assert old in s;s=s.replace(old,'''    // The validation accumulator already includes this payload exactly once.
    const resultingReceivedQuantities = previouslyReceivedByLineItem;''')
s=s.replace('    assertPurchaseOrderStatusTransition(purchaseOrder.status, nextStatus);','''    // Another partial receipt is valid even when the aggregate status is unchanged.
    if (purchaseOrder.status !== nextStatus) {
      assertPurchaseOrderStatusTransition(purchaseOrder.status, nextStatus);
    }''');f.write_text(s,encoding='utf-8')
t=P/'tests/runtime-purchase-receiving.test.mjs';s=t.read_text()
s=s.replace('function harness() {', '''// Schema builders are inert: the test calls the real transition function, not schema.parse.
const schema = new Proxy(function(){}, {get:(_t,key)=>key==='then'?undefined:schema,apply:()=>schema});
const rules=await loadTypeScript('src/lib/validation/purchaseOrderSchemas.ts',{root,stubs:{zod:{z:schema}}});
function harness() {''')
s=s.replace("    id: 'po-1', tenantId: 'tenant-a', status: 'APPROVED',","    id: 'po-1', tenantId: 'tenant-a', status: 'APPROVED', vendor:{name:'Vendor'}, totalAmount:'20',")
s=s.replace("ReceiptStatus: { POSTED: 'POSTED' }","ReceiptStatus: { RECORDED: 'RECORDED', DISCREPANCY_RECORDED:'DISCREPANCY_RECORDED' }")
s=s.replace("    '@/lib/http/errors': { ConflictError: class ConflictError extends Error {}, NotFoundError: class NotFoundError extends Error {} },\n",'')
s=s.replace("{ assertPurchaseOrderStatusTransition: () => {} }","{ assertPurchaseOrderStatusTransition: rules.assertPurchaseOrderStatusTransition }")
s=s.replace("    '@/services/serializers': { serializePurchaseOrder: (x) => x },\n",'')
s=s.replace("distinct valid line item entries still commit one receipt and status","full receipt invokes one receipt and status write")
s+='''
test('partial quantities are counted once, including duplicate entries within bounds',async()=>{
 for(const quantities of [[5],[2,3]]){const h=harness();const {purchaseOrderService}=await loadTypeScript('src/services/purchaseOrderService.ts',{root,stubs:h.stubs});
 await purchaseOrderService.receivePurchaseOrder({tenantId:'tenant-a',userId:'u-1'},'po-1',{receivedAt:new Date(),lineItems:quantities.map(quantityReceived=>({purchaseOrderLineItemId:'line-1',quantityReceived})),discrepancies:[]});
 assert.deepEqual(h.writes.status,['PARTIALLY_RECEIVED']);assert.equal(h.writes.receipt[0].status,'RECORDED');}
});
test('prior receipts plus incoming quantities allow another partial or exact completion, and refuse overage',async()=>{
 for(const [quantity,expected] of [[2,'PARTIALLY_RECEIVED'],[6,'RECEIVED'],[7,null]]){
 const h=harness();h.purchaseOrder.status='PARTIALLY_RECEIVED';h.purchaseOrder.receipts=[{id:'old',status:'RECORDED',receivedAt:new Date(),discrepancies:[],lineItems:[{purchaseOrderLineItemId:'line-1',quantityReceived:4}]}];
 const {purchaseOrderService}=await loadTypeScript('src/services/purchaseOrderService.ts',{root,stubs:h.stubs});
 const run=()=>purchaseOrderService.receivePurchaseOrder({tenantId:'tenant-a',userId:'u-1'},'po-1',{receivedAt:new Date(),lineItems:[{purchaseOrderLineItemId:'line-1',quantityReceived:quantity}],discrepancies:[]});
 if(expected){await run();assert.deepEqual(h.writes.status,[expected]);}else{await assert.rejects(run,/exceed/);assert.deepEqual(h.writes,{receipt:[],status:[],audit:[]});}
 }
});
test('foreign line and nonreceivable state refuse before transaction writes',async()=>{
 for(const [status,line] of [['APPROVED','foreign'],['RECEIVED','line-1']]){const h=harness();h.purchaseOrder.status=status;const {purchaseOrderService}=await loadTypeScript('src/services/purchaseOrderService.ts',{root,stubs:h.stubs});await assert.rejects(purchaseOrderService.receivePurchaseOrder({tenantId:'tenant-a',userId:'u-1'},'po-1',{receivedAt:new Date(),lineItems:[{purchaseOrderLineItemId:line,quantityReceived:1}],discrepancies:[]}));assert.deepEqual(h.writes,{receipt:[],status:[],audit:[]});}
});
''';t.write_text(s,encoding='utf-8')
p=B/'specs/42df17f9e984.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x]
s['summary']=['Accumulate prior and incoming receipt quantities exactly once, rejecting duplicate-entry overage before writes.','Permit additional valid partial receipts while aggregate status remains PARTIALLY_RECEIVED.','Six real-service cases with actual errors, serializer and transition function cover partial, full, prior, duplicate and refusal paths.']
s['limits']=['Repository and transaction adapters; inert Zod schema builders for module loading only, no schema parsing, SQL rollback or concurrent receipt protection tested.','Service assumes validated finite nonnegative quantities; current source reads receipt totals before transaction.']
p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
