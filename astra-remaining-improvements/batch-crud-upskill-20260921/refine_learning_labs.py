from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/7ba004a89f06';t=P/'tests/project-store-runtime.test.mjs';s=t.read_text().replace('{ mkdtemp, readFile }','{ mkdtemp, readFile, writeFile, mkdir, rm }')
s=s.replace("async () => {\n  const dir = await mkdtemp", "async (t) => {\n  const dir = await mkdtemp")
s=s.replace('  const store = new FileProjectStore(dir);',"  t.after(async()=>{assert.ok(path.resolve(dir).startsWith(path.resolve(os.tmpdir())+path.sep));assert.ok(path.basename(dir).startsWith('codehelper-store-'));await rm(dir,{recursive:true,force:true});});\n  const store = new FileProjectStore(dir);")
s=s.replace("  assert.equal(await store.get(), null);\n});", "  assert.equal(await store.get(), null);\n  await store.clear();\n});",1)
s=s.replace("  assert.equal(await store.get(), null);\n});", "  assert.equal(await store.get(), null);\n  await mkdir(path.join(dir,'data'),{recursive:true});await writeFile(path.join(dir,'data','uploaded-project.json'),'{bad json');assert.equal(await store.get(),null);\n});",1)
s+='''
test('saving replaces the whole document and separate base directories remain isolated',async(t)=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'codehelper-store-isolation-'));t.after(async()=>{assert.ok(path.resolve(dir).startsWith(path.resolve(os.tmpdir())+path.sep));assert.ok(path.basename(dir).startsWith('codehelper-store-'));await rm(dir,{recursive:true,force:true});});
 const first=new FileProjectStore(path.join(dir,'first')),second=new FileProjectStore(path.join(dir,'second'));
 await first.save({name:'old',files:[{path:'a',content:'A'}]});await second.save({name:'other',files:[]});await first.save({name:'replacement',files:[]});
 assert.equal((await first.get()).name,'replacement');assert.equal((await first.get()).files.length,0);assert.equal((await second.get()).name,'other');
});
''';t.write_text(s,encoding='utf-8')
P=B/'stage/6712d23cf34a';t=P/'tests/invoice-service-runtime.test.mjs';s=t.read_text();s+='''
test('legal transition matrix carries exact tenant actor and status event',async()=>{
 for(const [from,to] of [['issued','paid'],['issued','failed'],['issued','void'],['failed','paid'],['failed','void']]){
 const log=[];const repo={findTenantInvoiceOrThrow:async(tenant,id)=>{assert.equal(tenant,'tenant-1');assert.equal(id,'inv-1');return{id,status:from};},updateInvoiceStatus:async(...args)=>{log.push(['update',...args]);return{id:'inv-1',status:to};}};
 const svc=createInvoiceService(repo,{publish:async(topic,event)=>log.push(['publish',topic,event])});assert.equal((await svc.updateInvoiceStatus(context,'inv-1',{nextStatus:to})).status,to);
 assert.equal(log[0][1],'tenant-1');assert.equal(log[0][2],'inv-1');assert.equal(log[0][3],to);assert.equal(log[0][4].payload.previousStatus,from);assert.equal(log[0][4].payload.changedByUserId,'user-1');assert.equal(log[1][1],'billing.invoice-events');assert.equal(log[1][2].metadata.causationId,'inv-1');assert.equal(log[1][2].metadata.correlationId,'corr-1');assert.equal(log[1][2].metadata.traceId,'trace-1');
 }
});
test('terminal and unknown persisted states refuse before update or publish',async()=>{
 for(const status of ['paid','void','unknown']){let writes=0;const svc=createInvoiceService({findTenantInvoiceOrThrow:async()=>({id:'inv-1',status}),updateInvoiceStatus:async()=>{writes++;}},{publish:async()=>{writes++;}});await assert.rejects(svc.updateInvoiceStatus(context,'inv-1',{nextStatus:'paid'}),/INVALID_STATUS_TRANSITION/);assert.equal(writes,0);}
});
test('listing scopes tenant and publishing failure follows persistence',async()=>{
 const log=[];const svc=createInvoiceService({listInvoicesByTenant:async tenant=>{log.push(['list',tenant]);return[];},createInvoice:async input=>{log.push(['create',input]);return{id:input.invoiceId};}},{publish:async()=>{log.push(['publish']);throw Error('broker unavailable');}});
 await svc.listInvoices(context);assert.deepEqual(log[0],['list','tenant-1']);await assert.rejects(svc.createInvoice(context,{externalReference:'order-1',amountCents:1200,currency:'USD'}),/broker unavailable/);assert.deepEqual(log.map(c=>c[0]),['list','create','publish']);assert.equal(log[1][1].outboxEvent.metadata.eventName,'billing.invoice.issued');
});
test('repository failure stops publication',async()=>{
 let published=0;const svc=createInvoiceService({createInvoice:async()=>{throw Error('db unavailable');}},{publish:async()=>{published++;}});await assert.rejects(svc.createInvoice(context,{externalReference:'order-1',amountCents:1,currency:'USD'}),/db unavailable/);assert.equal(published,0);
});
''';t.write_text(s,encoding='utf-8')
P=B/'stage/c558dc8dae3b';t=P/'tests/trace-vault-service-runtime.test.mjs';s=t.read_text();s+='''
test('disabled and undetected sources are excluded; project mapping sorts activity',async()=>{
 const calls=[];const disabled={...adapter,sourceId:'disabled',detect:async()=>{throw Error('disabled detection must not run');}};
 const absent={...adapter,sourceId:'absent',detect:async()=>false,listProjects:async()=>{throw Error('absent list must not run');}};
 const active={...adapter,listProjects:async()=>[{id:'old',path:'/old',name:'Old',lastActivityAt:'2024-01-01'},{id:'new',path:'/new',name:'New',lastActivityAt:'2025-01-01'}]};
 const svc=new TraceVaultService({sources:{stub:{enabled:true},disabled:{enabled:false},absent:{enabled:true}}},[disabled,absent,active]);const projects=await svc.listProjects();assert.deepEqual(Array.from(projects,p=>p.id),['new','old']);assert.equal(projects[0].sourceId,'stub');assert.equal(projects[0].path,'/new');assert.equal((await svc.listSessions('missing')).length,0);assert.equal(await svc.getSession('missing'),null);
});
test('case-insensitive search includes thinking text, truncates snippet and enforces positive result limit',async()=>{
 const active={...adapter,readSession:async ref=>({...ref,turns:[0,1].map(index=>({index,userText:'x'.repeat(500),assistantText:'',thinkingBlocks:['Needle'],toolCalls:[]}))})};
 const svc=new TraceVaultService({sources:{stub:{enabled:true}}},[active]);const results=await svc.searchFallback('NEEDLE',1);assert.equal(results.length,1);assert.equal(results[0].turnIndex,0);assert.equal(results[0].text.length,400);
});
test('usage counts completions, tools and activity day; provider failures propagate',async()=>{
 const active={...adapter,readSession:async ref=>({...ref,turns:[{index:0,userText:'',assistantText:'',thinkingBlocks:[],tokenUsage:{prompt:2,completion:3},toolCalls:[{name:'read'},{name:'read'}]},{index:1,userText:'',assistantText:'',thinkingBlocks:[],toolCalls:[{name:'write'}]}]})};
 const svc=new TraceVaultService({sources:{stub:{enabled:true}}},[active]);const stats=await svc.usageStats();assert.equal(stats.totalSessions,1);assert.equal(stats.totalTurns,2);assert.equal(stats.totalPromptTokens,2);assert.equal(stats.totalCompletionTokens,3);assert.equal(stats.toolFrequency.read,2);assert.equal(stats.toolFrequency.write,1);assert.equal(stats.activityByDay['2025-01-01'],1);
 const broken=new TraceVaultService({sources:{stub:{enabled:true}}},[{...adapter,listProjects:async()=>{throw Error('provider unavailable');}}]);await assert.rejects(broken.listProjects(),/provider unavailable/);
});
''';t.write_text(s,encoding='utf-8')
for id,count in [('7ba004a89f06',3),('6712d23cf34a',6),('c558dc8dae3b',5)]:
 p=B/'specs'/f'{id}.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x]
 s['summary'].append(f'Expanded to {count} actual-source runtime cases during Astra review; production source unchanged.')
 s['limits']=['Focused actual-source runtime only; see course verification for adapter and integration boundaries. No full application stack or concurrent persistence proof.']
 p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
