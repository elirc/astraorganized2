from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
helper='''const fs=require('node:fs');
const path=require('node:path');
const {JSDOM}=require('jsdom');
const {randomUUID}=require('node:crypto');
exports.load=function(symbols){
 const root=path.resolve(__dirname,'..');
 const dom=new JSDOM(fs.readFileSync(path.join(root,'index.html'),'utf8'),{url:'http://localhost',runScripts:'outside-only'});
 Object.defineProperty(dom.window.crypto,'randomUUID',{value:randomUUID});
 dom.window.eval(fs.readFileSync(path.join(root,'app.js'),'utf8')+'\\nwindow.lesson = {'+symbols+'};');
 return dom;
};
'''
for n in [21,22]:
 p=B/str(n)/'test';p.mkdir(exist_ok=True);(p/'browser.cjs').write_text(helper,encoding='utf-8')
(B/'21/test/polls.test.cjs').write_text('''const test=require('node:test');const assert=require('node:assert/strict');const {load}=require('./browser.cjs');
function app(){return load('state,editPoll,handleSubmit,vote,deletePoll');}
test('removing the first option preserves the remaining option ids and votes',()=>{
 const d=app(),w=d.window,a=w.lesson,p=a.state.polls[0],ids=p.options.map(x=>x.id).slice(1).join(',');
 a.editPoll(p.id);w.document.querySelector('[aria-label="Remove option 1"]').click();
 a.handleSubmit({preventDefault(){}});
 assert.equal(a.state.polls[0].options.map(x=>x.id).join(','),ids);
 assert.equal(a.state.polls[0].options.map(x=>x.votes).join(','),'7,2');
 assert.equal(JSON.parse(w.localStorage.getItem('js1-poll-studio'))[0].options[0].votes,7);d.window.close();
});
test('blank or duplicate options are rejected without changing the saved poll',()=>{
 const d=app(),a=d.window.lesson,p=a.state.polls[0];a.editPoll(p.id);const before=JSON.stringify(a.state.polls);
 a.state.draftOptions[0].text=' API ';a.state.draftOptions[1].text='api';a.handleSubmit({preventDefault(){}});
 assert.match(d.window.document.querySelector('#form-message').textContent,/different text/);assert.equal(JSON.stringify(a.state.polls),before);
 a.state.draftOptions[1].text='';a.handleSubmit({preventDefault(){}});assert.match(d.window.document.querySelector('#form-message').textContent,/Fill every/);d.window.close();
});
test('failed writes preserve vote totals, the poll and the edit draft',()=>{
 const d=app(),w=d.window,a=w.lesson,p=a.state.polls[0];a.editPoll(p.id);w.document.querySelector('#poll-question').value='Retain this draft';
 const before=JSON.stringify(a.state.polls);w.Storage.prototype.setItem=()=>{throw new Error('quota');};
 a.vote(p.id,p.options[0].id);assert.equal(JSON.stringify(a.state.polls),before);
 a.handleSubmit({preventDefault(){}});assert.equal(JSON.stringify(a.state.polls),before);assert.equal(w.document.querySelector('#poll-question').value,'Retain this draft');
 a.deletePoll(p.id);assert.equal(JSON.stringify(a.state.polls),before);d.window.close();
});
''',encoding='utf-8')
(B/'22/test/movement.test.cjs').write_text('''const test=require('node:test');const assert=require('node:assert/strict');const {load}=require('./browser.cjs');
function app(){return load('state,moveCard,render');}
test('moving between columns renumbers both columns and survives persisted reconstruction',()=>{
 const d=app(),a=d.window.lesson;
 a.state.cards=[{id:'a',title:'A',column:'todo',order:0},{id:'b',title:'B',column:'todo',order:1},{id:'c',title:'C',column:'doing',order:0}];
 assert.equal(a.moveCard('doing','c','a'),true);
 assert.equal(a.state.cards.find(x=>x.id==='b').order,0);assert.equal(a.state.cards.find(x=>x.id==='c').order,1);
 const saved=JSON.parse(d.window.localStorage.getItem('js1-kanban-flow'));assert.equal(saved.find(x=>x.id==='a').column,'doing');assert.equal(saved.find(x=>x.id==='a').order,0);d.window.close();
});
test('self drops, invalid targets and storage failures cannot corrupt order',()=>{
 const d=app(),w=d.window,a=w.lesson,id=a.state.cards[0].id;const before=JSON.stringify(a.state.cards);
 assert.equal(a.moveCard('todo',id,id),true);assert.equal(JSON.stringify(a.state.cards),before);
 assert.equal(a.moveCard('missing',null,id),false);assert.equal(a.moveCard('doing','unknown',id),false);
 w.Storage.prototype.setItem=()=>{throw new Error('quota');};assert.equal(a.moveCard('doing',null,id),false);assert.equal(JSON.stringify(a.state.cards),before);d.window.close();
});
test('keyboard controls move and reorder a card without drag events',()=>{
 const d=app(),w=d.window,a=w.lesson;
 a.state.cards=[{id:'a',title:'A',column:'todo',order:0},{id:'b',title:'B',column:'todo',order:1}];a.render();
 const card=w.document.querySelector('[data-id="a"]');[...card.querySelectorAll('button')].find(x=>x.textContent==='Move down').click();
 assert.equal(a.state.cards.find(x=>x.id==='a').order,1);
 const select=w.document.querySelector('[data-id="a"] select');select.value='done';select.dispatchEvent(new w.Event('change'));
 assert.equal(a.state.cards.find(x=>x.id==='a').column,'done');assert.equal(w.document.activeElement.className,'move-column');d.window.close();
});
''',encoding='utf-8')
print('Added six behaviour tests for the first two projects.')
