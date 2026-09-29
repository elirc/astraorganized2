from pathlib import Path
s=Path(__file__).resolve().parent/'stage/a9672affc47e';p=s/'src/game/schema.ts';t=p.read_text(encoding='utf-8');old='for(const key of progress.completedChallenges){const [id,challenge]=key.split(\'::\');if(!mission(id).challenges.some(c=>c.id===challenge))fail("checkpoint is not in this catalog.");}';new='for(const key of progress.completedChallenges){const [id,challenge]=key.split(\'::\');const item=mission(id);const gate=item.challenges.find(c=>c.id===challenge);if(!gate)fail("checkpoint is not in this catalog.");if(!item.prerequisites.every(id=>progress.completedMissions.includes(id))||(progress.responses[key]??"").trim().length<gate!.minLength)fail("completed checkpoint has missing prerequisites or evidence.");}';assert old in t;t=t.replace(old,new);p.write_text(t,encoding='utf-8')
(s/'src/game/storage.test.ts').write_text('''import { describe, it, expect } from "vitest";
import { createProgress } from "./engine";
import { normalizeProgress, parseJson, validateAgainstCatalog, MAX_SAVE_BYTES } from "./schema";
import { createNote, updateNote, deleteNote } from "./notes";
import { loadProgress, persistProgress, resetProgress, serializeProgress, parseProgressExport, STORAGE_KEY } from "./storage";
import type { LockPort, StoragePort } from "./storage";
import type { Catalog } from "../types";
function fixture(raw:string|null=null){let value=raw;return {storage:{getItem:()=>value,setItem:(_key:string,next:string)=>{value=next;}} as StoragePort,raw:()=>value};}
function queue():LockPort{let tail:Promise<unknown>=Promise.resolve();return work=>{const result=tail.then(work);tail=result.catch(()=>undefined);return result;};}
const note={id:'note-one',missionId:'m1',title:'Transactions',body:'Commit the worker and audit together.'};
const now=new Date('2026-01-01T00:00:00.000Z');
it('reads absent storage without writing defaults',()=>{const f=fixture();expect(loadProgress(f.storage)).toEqual(createProgress());expect(f.raw()).toBeNull();});
it('fills legacy revision epoch and notes without erasing existing progress',()=>{const legacy={...createProgress(),callsign:'Learner',onboarded:true};const {revision,epoch,notes,...raw}=legacy;void revision;void epoch;void notes;const f=fixture(JSON.stringify(raw));const read=loadProgress(f.storage);expect(read.revision).toBe(0);expect(read.epoch).toBe('');expect(read.notes).toEqual([]);expect(read.callsign).toBe('Learner');expect(f.raw()).toBe(JSON.stringify(raw));});
it.each(['{broken','{"version":2}',JSON.stringify({...createProgress(),reviews:[]}),JSON.stringify({...createProgress(),onboarded:'yes'})])('preserves corrupt or unsupported saved bytes %s',raw=>{const f=fixture(raw);expect(()=>loadProgress(f.storage)).toThrow();expect(f.raw()).toBe(raw);});
it.each([{xp:NaN},{xp:-1},{sessionMinutes:25},{callsign:'x'.repeat(25)},{completedMissions:['m1','m1']},{responses:{'bad-key':'text'}},{activityDates:['2026-02-30']},{notes:[{...note,updatedAt:'bad'}]},{extra:'unsupported'}])('rejects malformed nested values %j',patch=>{expect(()=>normalizeProgress({...createProgress(),...patch})).toThrow();});
it('rejects prototype-shaped JSON keys and oversized transport',()=>{expect(()=>normalizeProgress(JSON.parse('{"version":1,"responses":{"__proto__":"bad"}}'))).toThrow();expect(()=>parseJson(' '.repeat(MAX_SAVE_BYTES+1))).toThrow(/limit/);});
it('accepts a save only after its storage write and returns detached normalized data',async()=>{const f=fixture();const candidate={...createProgress(),callsign:'Learner',onboarded:true};const accepted=await persistProgress(candidate,f.storage,queue());expect(candidate.revision).toBe(0);expect(accepted.revision).toBe(1);expect(accepted.epoch).not.toBe('');expect(loadProgress(f.storage)).toEqual(accepted);});
it('rejects competing same-revision saves with one accepted winner',async()=>{const f=fixture();const lock=queue();const a={...createProgress(),callsign:'First'};const b={...createProgress(),callsign:'Second'};const results=await Promise.allSettled([persistProgress(a,f.storage,lock),persistProgress(b,f.storage,lock)]);expect(results.map(r=>r.status)).toEqual(['fulfilled','rejected']);expect(loadProgress(f.storage).callsign).toBe('First');expect(loadProgress(f.storage).revision).toBe(1);});
it('leaves storage and proposal unchanged after quota rejection',async()=>{const original=JSON.stringify(createProgress());const f=fixture(original);f.storage.setItem=()=>{throw new DOMException('Quota exceeded','QuotaExceededError');};const proposal={...createProgress(),callsign:'Pending'};await expect(persistProgress(proposal,f.storage,queue())).rejects.toThrow(/Quota/);expect(f.raw()).toBe(original);expect(proposal.revision).toBe(0);});
it('reset checks exact raw data and changes identity so old tabs cannot resurrect drafts',async()=>{const f=fixture();const lock=queue();const initial=await persistProgress({...createProgress(),callsign:'Old'},f.storage,lock);const before=f.raw();f.storage.setItem(STORAGE_KEY,JSON.stringify({...initial,callsign:'Newer'}));await expect(resetProgress(before,f.storage,lock)).rejects.toThrow(/changed/);const reset=await resetProgress(f.raw(),f.storage,lock);expect(reset.epoch).not.toBe(initial.epoch);await expect(persistProgress(initial,f.storage,lock)).rejects.toThrow(/another tab/);expect(loadProgress(f.storage).callsign).toBe('');});
it('exports and validates imported notes without trusting transport metadata',()=>{const data=createNote(createProgress(),note,now);expect(parseProgressExport(serializeProgress(data))).toEqual(data);expect(()=>parseProgressExport(JSON.stringify({progress:data,unexpected:true}))).toThrow();});
it('creates edits and deletes notes without mutating their previous snapshot',()=>{const start=createProgress();const one=createNote(start,note,now);const two=updateNote(one,{...note,title:'Atomic transactions'},new Date('2026-01-02T00:00:00Z'));expect(one.notes[0].title).toBe('Transactions');expect(two.notes[0].id).toBe(one.notes[0].id);expect(two.notes[0].updatedAt).not.toBe(one.notes[0].updatedAt);expect(deleteNote(two,note.id).notes).toEqual([]);expect(start.notes).toEqual([]);});
it('rejects duplicate or missing note identities and blank note content',()=>{const one=createNote(createProgress(),note,now);expect(()=>createNote(one,note,now)).toThrow(/already exists/);expect(()=>updateNote(one,{...note,id:'absent'},now)).toThrow(/no longer/);expect(()=>deleteNote(one,'absent')).toThrow(/no longer/);expect(()=>createNote(createProgress(),{...note,body:' '},now)).toThrow();});
describe('catalog integrity for imported progress',()=>{
 const catalog={missions:[{id:'m1',prerequisites:[],challenges:[{id:'prove',minLength:3}]},{id:'m2',prerequisites:['m1'],challenges:[{id:'prove',minLength:3}]}]} as unknown as Catalog;
 it('rejects unknown notes and checkpoint claims without prerequisites/evidence',()=>{expect(()=>validateAgainstCatalog(createNote(createProgress(),{...note,missionId:'missing'},now),catalog)).toThrow();expect(()=>validateAgainstCatalog({...createProgress(),completedChallenges:['m2::prove'],responses:{'m2::prove':'evidence'}},catalog)).toThrow(/prerequisites/);expect(()=>validateAgainstCatalog({...createProgress(),completedMissions:['m1']},catalog)).toThrow(/incomplete/);});
 it('accepts known mission notes and valid completion records',()=>{const progress=createNote({...createProgress(),completedMissions:['m1'],completedChallenges:['m1::prove'],responses:{'m1::prove':'evidence'}},note,now);expect(validateAgainstCatalog(progress,catalog)).toBe(progress);});
});
''',encoding='utf-8')
p=s/'src/game/engine.test.ts';t=p.read_text(encoding='utf-8');t+='''

describe("runtime progression boundaries", () => {
  it("rejects completing a locked mission and a foreign checkpoint", () => {
    const progress=saveResponse(createProgress(),mission.id,"a","evidence");
    expect(()=>completeChallenge(progress,{...mission,prerequisites:["missing"]},mission.challenges[0])).toThrow(/prerequisites/);
    expect(()=>completeChallenge(progress,mission,{...mission.challenges[0],id:"foreign"})).toThrow(/belong/);
  });
  it("uses the catalog checkpoint reward instead of a supplied altered reward", () => {
    const progress=saveResponse(createProgress(),mission.id,"a","evidence");
    expect(completeChallenge(progress,mission,{...mission.challenges[0],xp:9999}).xp).toBe(30);
  });
  it("rejects early or repeated review rewards", () => {
    const progress={...createProgress(),completedMissions:["m1"],reviews:{m1:{missionId:"m1",stage:0,due:"2026-01-02T00:00:00Z",reviews:0,lapses:0}}};
    expect(()=>reviewMission(progress,"m1","good",new Date("2026-01-01T00:00:00Z"))).toThrow(/not due/);
    const accepted=reviewMission(progress,"m1","good",new Date("2026-01-02T00:00:00Z"));
    expect(()=>reviewMission(accepted,"m1","good",new Date("2026-01-02T00:00:00Z"))).toThrow(/not due/);
  });
  it("rejects invalid clocks, stages and runtime ratings", () => {
    const record={missionId:"m1",stage:0,due:"2026-01-01T00:00:00Z",reviews:0,lapses:0};
    expect(()=>scheduleReview(record,"good",new Date("invalid"))).toThrow(/clock/);
    expect(()=>scheduleReview({...record,stage:-1},"good")).toThrow(/invalid/);
    expect(()=>scheduleReview(record,"unknown" as never)).toThrow(/rating/);
  });
});
''';p.write_text(t,encoding='utf-8');print('Added storage, recovery, CRUD, catalog and progression boundary tests')
