from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/2f59a0d07a85'
t=P/'tests/reply-parent-boundary.test.mjs'
s=t.read_text(encoding='utf-8-sig')
s=s.replace("const state = { parent: null, transactions: 0 };", "const state = { parent: null, transactions: 0, calls: [], closed: false, error: null };\nconst created = { id: 'new-post' };\nconst user = { id: 'u1', createdAt: new Date(), trustLevelLevel: 0 };\nconst tx = { post: { findFirst: async (arg) => { assert.equal(arg.where.topicId, 'topic-a'); state.calls.push('last'); return { position: 3 }; }, create: async ({data}) => { state.calls.push(['create', data]); return created; } }, topic: { update: async ({where,data}) => { assert.equal(where.id, 'topic-a'); assert.equal(data.replyCount.increment, 1); state.calls.push('topic-counter'); } }, user: { update: async ({where,data}) => { assert.equal(where.id, 'u1'); assert.equal(data.postsCreatedCount.increment, 1); state.calls.push('user-counter'); } } }; ")
start=s.index('const prisma =');end=s.index('\nconst parse',start)
s=s[:start]+'''const prisma = {
 post: { findUnique: async ({where,select}) => { state.calls.push('parent'); assert.ok(where.id); if(state.error) throw state.error; if(select) assert.equal(select.topicId,true); return state.parent; } },
 topic: { findUniqueOrThrow: async ({where}) => { assert.equal(where.id,'topic-a'); return { id: 'topic-a', state: state.closed ? 'CLOSED' : 'OPEN', category: {}, authorId: 'u1', author: {preferences:{}}, slug:'topic-a' }; } },
 siteSetting: { findMany: async () => [] }, subscription: {findMany: async () => []},
 user: {findUniqueOrThrow: async () => user}, trustLevel: {findMany: async () => []},
 $transaction: async (fn) => { state.transactions++; return fn(tx); }
};''' +s[end:]
s += '''
test('same-topic and top-level replies preserve payload, counters and result', async () => {
 for(const parentPostId of ['parent-a',undefined]) {
  state.parent={topicId:'topic-a',authorId:'u1',author:{preferences:{}}};state.transactions=0;state.calls=[];state.closed=false;state.error=null;
  assert.equal(await mod.createReply(user,{topicId:'topic-a',parentPostId,content:'hello'}),created);
  assert.equal(state.transactions,1);
  const create=state.calls.find(x=>Array.isArray(x));
  assert.deepEqual(JSON.parse(JSON.stringify(create[1])), {topicId:'topic-a',authorId:'u1',...(parentPostId?{parentPostId}:{}),contentMarkdown:'hello',position:4});
  assert.deepEqual(state.calls.filter(x=>x!=='parent').map(x=>Array.isArray(x)?x[0]:x),['last','create','topic-counter','user-counter']);
  assert.equal(state.calls.filter(x=>x==='parent').length,parentPostId?2:0);
 }
});
test('closed topic refuses before parent lookup and transaction',async()=>{
 state.closed=true;state.calls=[];state.transactions=0;
 await assert.rejects(mod.createReply(user,{topicId:'topic-a',parentPostId:'p',content:'hello'}),/not open/);
 assert.equal(state.transactions,0);assert.deepEqual(state.calls,[]);state.closed=false;
});
test('parent lookup failure preserves identity and prevents transaction',async()=>{
 const error=new Error('lookup unavailable');state.error=error;state.transactions=0;
 await assert.rejects(mod.createReply(user,{topicId:'topic-a',parentPostId:'p',content:'hello'}),e=>e===error);
 assert.equal(state.transactions,0);state.error=null;
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/2f59a0d07a85.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'))
spec['limits']=['Five Node runtime cases execute the actual forum module with Prisma, schema, enum, permission and external helper adapters. Same-topic/top-level cases run internal notification and trust orchestration against adapters, not real deliveries or persistence.', 'No Next.js, native Prisma, Zod schema, actual permission policy, database isolation or durable rollback was executed. Parent validation is a pre-transaction membership check; concurrent parent changes remain outside this correction.', 'Local Next.js guides were absent after dependency cleanup. No Next.js API or route was changed.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
