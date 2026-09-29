from pathlib import Path
s=Path(__file__).resolve().parent/'stage/a9672affc47e'
p=s/'src/types.ts';t=p.read_text(encoding='utf-8').replace('  revision: number;','  revision: number;\n  epoch: string;');p.write_text(t,encoding='utf-8')
p=s/'src/game/engine.ts';t=p.read_text(encoding='utf-8').replace('    revision: 0,','    revision: 0,\n    epoch: "",',1);p.write_text(t,encoding='utf-8')
(s/'src/game/schema.ts').write_text('''import { createProgress, challengeKey } from "./engine";
import type { Catalog, GameProgress, LearningNote, ReviewRecord } from "../types";
export const MAX_SAVE_BYTES = 4 * 1024 * 1024;
const idPattern = /^[A-Za-z0-9_-]{1,160}$/;
const reserved = new Set(["__proto__", "constructor", "prototype"]);
function fail(message: string): never { throw new Error(`Save data: ${message}`); }
export function object(value: unknown, allowed?: readonly string[]): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return fail("expected an object.");
  const record = value as Record<string, unknown>;
  if (Object.keys(record).some(key => reserved.has(key) || (allowed && !allowed.includes(key)))) fail("unknown or unsupported field.");
  return record;
}
function text(value: unknown, max: number, label: string, empty = false): string {
  if (typeof value !== "string" || value.length > max || (!empty && !value.trim())) return fail(`${label} is missing or too long.`);
  return value;
}
function integer(value: unknown, max: number, label: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0 || value > max) return fail(`${label} must be a bounded nonnegative integer.`);
  return value;
}
export function identity(value: unknown): string {
  if (typeof value !== "string" || !idPattern.test(value) || reserved.has(value)) return fail("invalid identity.");
  return value;
}
function date(value: unknown, label: string): string {
  const raw = text(value,40,label); const parsed = new Date(raw);
  if (!/^\\d{4}-\\d{2}-\\d{2}T/.test(raw) || !Number.isFinite(parsed.getTime()) || parsed.getTime()<0) return fail(`${label} is not a supported timestamp.`);
  return parsed.toISOString();
}
function ids(value: unknown, label: string): string[] {
  if (!Array.isArray(value) || value.length > 5000) return fail(`${label} must be a bounded list.`);
  const result = value.map(identity); if (new Set(result).size !== result.length) fail(`${label} contains duplicates.`); return result;
}
export function normalizeNote(value: unknown): LearningNote {
  const note=object(value,["id","missionId","title","body","updatedAt"]);
  return {id:identity(note.id),missionId:identity(note.missionId),title:text(note.title,120,"note title").trim(),body:text(note.body,10000,"note body"),updatedAt:date(note.updatedAt,"note update")};
}
export function normalizeProgress(value: unknown): GameProgress {
  const raw=object(value,["version","revision","epoch","notes","callsign","sessionMinutes","onboarded","xp","completedMissions","completedChallenges","responses","reviews","activityDates","lastMissionId"]);
  if(raw.version!==1)fail("unsupported version. Export the original before choosing recovery.");
  const defaults=createProgress(); const data={...defaults,...raw};
  const callsign=text(data.callsign,24,"callsign",true);
  if(typeof data.onboarded!=="boolean" || (data.onboarded&&!callsign.trim()))fail("invalid learner profile.");
  if(![15,30,45,60].includes(data.sessionMinutes as number))fail("invalid focus block.");
  const revision=integer(data.revision,Number.MAX_SAFE_INTEGER,"revision");
  const epoch=text(data.epoch,80,"save identity",true);if(epoch&&!/^[A-Za-z0-9_-]{1,80}$/.test(epoch))fail("invalid save identity.");
  const completedMissions=ids(data.completedMissions,"completed missions");
  if(!Array.isArray(data.completedChallenges)||data.completedChallenges.length>15000)fail("invalid completed checkpoints.");
  const responseKey=(key:unknown):string=>{if(typeof key!=="string")return fail("invalid response identity.");const parts=key.split("::");if(parts.length!==2)fail("invalid response identity.");parts.forEach(identity);return key;};
  const completedChallenges=(data.completedChallenges as unknown[]).map(responseKey);if(new Set(completedChallenges).size!==completedChallenges.length)fail("duplicate checkpoint completion.");
  const responses:Record<string,string>=Object.create(null);const suppliedResponses=object(data.responses);
  if(Object.keys(suppliedResponses).length>15000)fail("too many responses.");
  for(const [key,value] of Object.entries(suppliedResponses))responses[responseKey(key)]=text(value,100000,"response",true);
  const reviews:Record<string,ReviewRecord>=Object.create(null);const suppliedReviews=object(data.reviews);
  if(Object.keys(suppliedReviews).length>5000)fail("too many reviews.");
  for(const [key,value] of Object.entries(suppliedReviews)){
    identity(key);const item=object(value,["missionId","stage","due","reviews","lapses","lastRating","lastReviewed"]);
    if(item.missionId!==key||!completedMissions.includes(key))fail("review must belong to a completed mission.");
    const count=integer(item.reviews,1000000,"review count");const lapses=integer(item.lapses,count,"review lapses");
    if(item.lastRating!==undefined&&!['again','hard','good','easy'].includes(item.lastRating as string))fail("invalid review rating.");
    reviews[key]={missionId:key,stage:integer(item.stage,6,"review stage"),due:date(item.due,"review due"),reviews:count,lapses,...(item.lastRating===undefined?{}:{lastRating:item.lastRating as ReviewRecord['lastRating']}),...(item.lastReviewed===undefined?{}:{lastReviewed:date(item.lastReviewed,"last review")})};
  }
  if(!Array.isArray(data.activityDates)||data.activityDates.length>40000)fail("invalid activity dates.");
  const activityDates=(data.activityDates as unknown[]).map(value=>{if(typeof value!=="string"||!/^\\d{4}-\\d{2}-\\d{2}$/.test(value))return fail("invalid activity day.");const day=new Date(value+'T00:00:00.000Z');if(!Number.isFinite(day.getTime())||day.toISOString().slice(0,10)!==value)fail("invalid activity day.");return value;});
  if(new Set(activityDates).size!==activityDates.length)fail("duplicate activity day.");
  if(!Array.isArray(data.notes)||data.notes.length>1000)fail("at most 1,000 learning notes are supported.");
  const notes=(data.notes as unknown[]).map(normalizeNote);if(new Set(notes.map(note=>note.id)).size!==notes.length)fail("duplicate learning-note identity.");
  return {version:1,revision,epoch,notes,callsign,sessionMinutes:data.sessionMinutes as number,onboarded:data.onboarded as boolean,xp:integer(data.xp,1000000000,"XP"),completedMissions,completedChallenges,responses,reviews,activityDates,...(data.lastMissionId===undefined?{}:{lastMissionId:identity(data.lastMissionId)})};
}
export function validateAgainstCatalog(progress:GameProgress,catalog:Catalog):GameProgress {
  const missions=new Map(catalog.missions.map(m=>[m.id,m]));
  const mission=(id:string)=>{const found=missions.get(id);if(!found)fail(`mission ${id} is not in this catalog.`);return found!;};
  for(const id of progress.completedMissions){const item=mission(id);if(!item.prerequisites.every(id=>progress.completedMissions.includes(id))||!item.challenges.every(c=>progress.completedChallenges.includes(challengeKey(id,c.id))))fail(`mission ${id} has incomplete prerequisites or checkpoints.`);}
  for(const key of progress.completedChallenges){const [id,challenge]=key.split('::');if(!mission(id).challenges.some(c=>c.id===challenge))fail("checkpoint is not in this catalog.");}
  for(const key of Object.keys(progress.responses)){const [id,challenge]=key.split('::');if(challenge!=="code-lab"&&!mission(id).challenges.some(c=>c.id===challenge))fail("response is not in this catalog.");else mission(id);}
  for(const note of progress.notes)mission(note.missionId);
  if(progress.lastMissionId)mission(progress.lastMissionId);
  return progress;
}
export function boundedJson(value:unknown):string {
  const raw=JSON.stringify(value);if(raw.length>MAX_SAVE_BYTES||new TextEncoder().encode(raw).length>MAX_SAVE_BYTES)fail("save exceeds the 4 MiB data limit. Export and reduce oversized drafts.");return raw;
}
export function parseJson(raw:string):unknown {
  if(raw.length>MAX_SAVE_BYTES||new TextEncoder().encode(raw).length>MAX_SAVE_BYTES)fail("file exceeds the 4 MiB data limit.");
  try{return JSON.parse(raw);}catch{throw new Error("Saved progress is unreadable. No data was replaced; export the original before resetting.");}
}
''',encoding='utf-8')
(s/'src/game/storage.ts').write_text('''import { createProgress } from "./engine";
import { boundedJson, normalizeProgress, object, parseJson } from "./schema";
import type { GameProgress } from "../types";
export const STORAGE_KEY = "skillforge.quest.progress.v1";
export type StoragePort=Pick<Storage,"getItem"|"setItem">;
export type LockPort=<T>(work:()=>T|Promise<T>)=>Promise<T>;
export const browserLock:LockPort=work=>{
  if(!navigator.locks)throw new Error("This browser cannot coordinate saves. Use a browser with Web Locks on localhost or HTTPS.");
  return navigator.locks.request(STORAGE_KEY,work);
};
export function loadProgress(storage:StoragePort=localStorage):GameProgress {
  const raw=storage.getItem(STORAGE_KEY);return raw===null?createProgress():normalizeProgress(parseJson(raw));
}
export async function persistProgress(progress:GameProgress,storage:StoragePort=localStorage,lock:LockPort=browserLock):Promise<GameProgress> {
  const proposal=normalizeProgress(progress);
  return lock(()=>{
    const current=loadProgress(storage);
    if(proposal.revision!==current.revision||proposal.epoch!==current.epoch)throw new Error("Progress changed in another tab. Export your pending draft or copy its text, then load current progress before retrying.");
    if(current.revision===Number.MAX_SAFE_INTEGER)throw new Error("Save revision is exhausted. Export for recovery.");
    const accepted={...proposal,revision:current.revision+1,epoch:current.epoch||crypto.randomUUID()};
    storage.setItem(STORAGE_KEY,boundedJson(accepted));return accepted;
  });
}
export function serializeProgress(progress:GameProgress):string {return boundedJson({exportedAt:new Date().toISOString(),progress:normalizeProgress(progress)});}
export function parseProgressExport(value:string):GameProgress {
  const parsed=object(parseJson(value),["exportedAt","progress"]);return normalizeProgress(parsed.progress);
}
export async function resetProgress(expectedRaw:string|null,storage:StoragePort=localStorage,lock:LockPort=browserLock):Promise<GameProgress> {
  return lock(()=>{
    if(storage.getItem(STORAGE_KEY)!==expectedRaw)throw new Error("Saved data changed while recovery was open. Export and review the current data first.");
    const next={...createProgress(),epoch:crypto.randomUUID()};storage.setItem(STORAGE_KEY,boundedJson(next));return next;
  });
}
''',encoding='utf-8')
(s/'src/game/notes.ts').write_text('''import type { GameProgress, LearningNote } from "../types";
import { normalizeNote, normalizeProgress } from "./schema";
type NoteInput=Omit<LearningNote,"updatedAt">;
export function createNote(progress:GameProgress,input:NoteInput,now=new Date()):GameProgress {
  const note=normalizeNote({...input,updatedAt:now.toISOString()});
  if(progress.notes.some(item=>item.id===note.id))throw new Error("A note with this identity already exists.");
  return normalizeProgress({...progress,notes:[...progress.notes,note]});
}
export function updateNote(progress:GameProgress,input:NoteInput,now=new Date()):GameProgress {
  const note=normalizeNote({...input,updatedAt:now.toISOString()});
  if(!progress.notes.some(item=>item.id===note.id))throw new Error("This note no longer exists. Keep its text before loading current progress.");
  return normalizeProgress({...progress,notes:progress.notes.map(item=>item.id===note.id?note:item)});
}
export function deleteNote(progress:GameProgress,id:string):GameProgress {
  if(!progress.notes.some(item=>item.id===id))throw new Error("This note no longer exists.");
  return normalizeProgress({...progress,notes:progress.notes.filter(item=>item.id!==id)});
}
''',encoding='utf-8');print('Wrote strict save schema, revision/epoch commits, recovery compare-and-set, and learning-note CRUD; UI integration pending')
