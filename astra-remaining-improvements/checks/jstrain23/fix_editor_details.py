from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'src/components/DatabaseBlock.js';t=p.read_text(encoding='utf-8').replace("'neq'","'ne'").replace('map(([name,items])=>','map(([name,items],index)=>').replace('className="board-column" key={name}','className="board-column" key={name+index}');p.write_text(t,encoding='utf-8')
p=s/'src/components/WorkspaceApp.js';t=p.read_text(encoding='utf-8').replace('    workspaceId,\n','').replace('    loaded,\n','    loaded,\n');p.write_text(t,encoding='utf-8')
p=s/'test/session.test.mjs';t=p.read_text(encoding='utf-8');t+='''
test('typing during an already-running server operation is retained for reconciliation',async()=>{const pending=deferred();const session=new WorkspaceSession({load:async()=>snapshot(),save:async({state})=>snapshot(state,'b')});session.start(snapshot());const operation=session.operation(()=>pending.promise);const draft=state();draft.pages[0].title='Typed during import';session.edit(draft);pending.resolve(snapshot(state(),'b'));assert.equal(await operation,null);assert.equal(session.draft.pages[0].title,'Typed during import');assert.equal(session.getSnapshot().needsReview,true);});
''';p.write_text(t,encoding='utf-8')
