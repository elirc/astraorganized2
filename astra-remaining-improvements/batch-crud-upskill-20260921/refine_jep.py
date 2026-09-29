from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/a880d6aae28f'
f=P/'Jeopardy-Game/frontend/src/pages/GameSetupPage.jsx';t=f.read_text();old='setPlayers(players.filter((p) => p.id !== playerId));';assert old in t;t=t.replace(old,'setPlayers((currentPlayers) => currentPlayers.filter((p) => p.id !== playerId));');f.write_text(t,encoding='utf-8')
(P/'tests/runtime-player-state.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../Jeopardy-Game/frontend/src/pages/GameSetupPage.jsx',import.meta.url),'utf8');
const start=source.indexOf('    const handleAddPlayer = async () => {');
const end=source.indexOf('    const handleKeyPress =',start);
assert.ok(start>=0 && end>start,'production handler section must exist');
const handlers=source.slice(start,end);
function deferred() { let resolve,reject;const promise=new Promise((a,b)=>{resolve=a;reject=b;});return {promise,resolve,reject}; }
function fixture(options={}) {
  let current=Object.freeze([{id:'first'},{id:'second'},{id:'third'}]), error=null, sessionValue;
  const adds=[], removes=[], creates=[]; let writes=0;
  const context={ players:current, session:options.newSession?null:{id:'session-1'}, gameId:'game-1',newPlayerName:' New ',
    setPlayers: update=>{writes++;current=typeof update==='function'?update(current):update;},
    setNewPlayerName:value=>{context.newPlayerName=value;},setError:value=>{error=value;},setSession:value=>{sessionValue=value;},
    sessionApi:{addPlayer:(id,data)=>{const d=deferred();adds.push({id,data,...d});return d.promise;},removePlayer:(id,player)=>{const d=deferred();removes.push({id,player,...d});return d.promise;},create:id=>{creates.push(id);return Promise.resolve({data:{id:'created-session'}});}}
  };
  const actions=vm.runInNewContext(handlers+'\\n({handleAddPlayer,handleRemovePlayer})',context);
  return {...actions,adds,removes,creates,context,ids:()=>Array.from(current,p=>p.id),error:()=>error,writes:()=>writes,session:()=>sessionValue};
}
test('two out-of-order existing-session additions keep both server records',async()=>{
  const f=fixture();f.context.newPlayerName=' A ';const a=f.handleAddPlayer();f.context.newPlayerName='B';const b=f.handleAddPlayer();
  assert.equal(f.adds[0].id,'session-1');assert.equal(f.adds[0].data.name,'A');assert.equal(f.adds[1].data.name,'B');
  f.adds[1].resolve({data:{id:'b'}});await b;f.adds[0].resolve({data:{id:'a'}});await a;
  assert.deepEqual(f.ids(),['first','second','third','b','a']);assert.equal(f.context.players.length,3);assert.equal(f.context.newPlayerName,'');
});
test('a delayed removal preserves a player appended while it awaited the server',async()=>{
  const f=fixture();const removal=f.handleRemovePlayer('first');const addition=f.handleAddPlayer();
  f.adds[0].resolve({data:{id:'new'}});await addition;f.removes[0].resolve();await removal;
  assert.deepEqual(f.ids(),['second','third','new']);assert.equal(f.removes[0].id,'session-1');
});
test('two overlapping removals do not resurrect either removed player',async()=>{
  const f=fixture();const a=f.handleRemovePlayer('first'),b=f.handleRemovePlayer('second');
  f.removes[1].resolve();await b;f.removes[0].resolve();await a;assert.deepEqual(f.ids(),['third']);
});
test('rejected add and remove report errors without changing player state',async()=>{
  for(const operation of ['add','remove']) {
    const f=fixture();const pending=operation==='add'?f.handleAddPlayer():f.handleRemovePlayer('first');
    (operation==='add'?f.adds:f.removes)[0].reject(new Error('network failed'));await pending;
    assert.deepEqual(f.ids(),['first','second','third']);assert.equal(f.writes(),0);assert.equal(f.error(),'network failed');
  }
});
test('blank player input performs no request and no state write',async()=>{
  const f=fixture();f.context.newPlayerName='   ';await f.handleAddPlayer();assert.equal(f.adds.length,0);assert.equal(f.creates.length,0);assert.equal(f.writes(),0);
});
test('first-session happy path keeps its existing replacement behavior',async()=>{
  const f=fixture({newSession:true});const pending=f.handleAddPlayer();await Promise.resolve();
  assert.deepEqual(f.creates,['game-1']);assert.equal(f.adds[0].id,'created-session');f.adds[0].resolve({data:{id:'first-created'}});await pending;
  assert.equal(f.session().id,'created-session');assert.deepEqual(f.ids(),['first-created']);
});
''',encoding='utf-8')
s=B/'specs/a880d6aae28f.json';j=json.loads(s.read_text())
j['summary']=['Use functional state updaters for existing-session player additions and removals so deferred responses preserve the latest local collection.','Retain first-session creation behavior and existing API-error handling.']
j['limits']=['Six cases execute the exact add/remove handler section extracted from production JSX with deferred API doubles and a modeled functional state setter; React itself is not mounted.','No network, server persistence, browser scheduling or React rendering was executed.','Concurrent first-session creation, session changes while requests are pending, duplicate server records and request idempotency remain outside this bounded existing-session reconciliation fix.']
s.write_text(json.dumps(j,indent=2))
