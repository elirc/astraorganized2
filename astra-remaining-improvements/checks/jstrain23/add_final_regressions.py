from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'test/session.test.mjs';t=p.read_text(encoding='utf-8');t+='''
test('reverting to accepted content clears the dirty display without sending another write',async()=>{let calls=0;const session=new WorkspaceSession({load:async()=>snapshot(),save:async()=>{calls++;}});session.start(snapshot());const draft=state();draft.pages[0].title='Temporary';session.edit(draft);session.edit(state());assert.equal(session.dirty(),false);assert.equal(await session.save(),true);assert.equal(calls,0);assert.equal(session.getSnapshot().phase,'saved');});
test('malformed saved drafts cannot replace the rendered accepted document',()=>{const session=new WorkspaceSession({load:async()=>snapshot(),save:async()=>snapshot()});session.start(snapshot());assert.throws(()=>session.recover({base:snapshot(),state:{pages:'broken'}}));assert.deepEqual(session.draft,state());});
''';p.write_text(t,encoding='utf-8')
p=Path(__file__).with_name('browser_check.py');t=p.read_text()
needle="passed('real two-tab stale write refused with local draft retained')"
t=t.replace(needle,needle+'''
            page.get_by_label('Page title',exact=True).fill('First tab accepted again');explicit_save(page)
            retained=other.evaluate("""() => new Promise((resolve,reject)=>{const request=indexedDB.open('knowledge-workspace-drafts-v2');request.onerror=()=>reject(request.error);request.onsuccess=()=>{const db=request.result,tx=db.transaction('drafts','readonly'),read=tx.objectStore('drafts').getAll();let value;read.onsuccess=()=>{value=read.result;};tx.oncomplete=()=>{db.close();resolve(value);};};})""")
            assert any(value['state']['pages'][0]['title']=='Second tab retained' for value in retained);passed('one tab acceptance does not clear another tab retained IndexedDB draft')''')
needle="recovery=page.get_by_role('region',name='Saved local draft',exact=True);expect(recovery).to_be_visible();recovery.get_by_role"
t=t.replace(needle,"""recovery=page.get_by_role('region',name='Saved local draft',exact=True);expect(recovery).to_be_visible();page.get_by_role('button',name='Sign out',exact=True).click();expect(page.get_by_label('Owner token')).to_be_visible();login(page);expect(recovery).to_be_visible();passed('sign-out preserves a saved draft that has not been reviewed');recovery.get_by_role""")
p.write_text(t)
for p in [s/'README.md',s/'astraupskill/01-CODEBASE-MAP.md',s/'astraupskill/VERIFICATION.md']:
    t=p.read_text(encoding='utf-8').replace('95 tests','97 tests').replace('13 save-session checks','15 save-session checks').replace('all 95','all 97')
    if p.name=='README.md':t=t.replace('Local drafts are scoped to the workspace instance in IndexedDB.','Local drafts are scoped to the workspace instance and individual editing session in IndexedDB. A successful save clears only its own draft. Saved sessions are offered one at a time; unselected sessions remain stored for a later sign-in.')
    p.write_text(t,encoding='utf-8')
