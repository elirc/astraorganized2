from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/73/src/lib/backup.ts';s=p.read_text();s="import { validateBackupRecords } from './backupValidation'\n"+s;s=s.replace("candidate.version > BACKUP_VERSION","candidate.version !== BACKUP_VERSION");s=s.replace('  return { ok: true, backup: candidate as Backup }',"  const problem = validateBackupRecords(candidate)\n  if (problem) return { ok: false, error: problem }\n  return { ok: true, backup: candidate as Backup }");p.write_text(s)
(B/'stage/73/src/lib/backupValidation.ts').write_text('''import { JOB_STAGES } from '../types'
// JSON has no runtime TypeScript types. Check every record before the caller
// replaces any of the calendar, job or settings stores.
export function validateBackupRecords(value: unknown): string | null {
  const object = (v: unknown): v is Record<string, any> => !!v && typeof v === 'object' && !Array.isArray(v)
  const text = (v: unknown): v is string => typeof v === 'string' && v.length <= 100000
  const nonempty = (v: unknown): v is string => text(v) && !!v.trim()
  const integer = (v: unknown, min = 0, max = 1000000) => typeof v === 'number' && Number.isInteger(v) && v >= min && v <= max
  const date = (v: unknown): v is string => typeof v === 'string' && /^\\d{4}-\\d{2}-\\d{2}$/.test(v) && Number.isFinite(Date.parse(v)) && new Date(v).toISOString().slice(0,10) === v
  const local = (v: unknown): v is string => typeof v === 'string' && /^\\d{4}-\\d{2}-\\d{2}T(?:[01]\\d|2[0-3]):[0-5]\\d$/.test(v) && date(v.slice(0,10))
  const stamp = (v: unknown) => text(v) && Number.isFinite(Date.parse(v))
  const unique = (rows: any[]) => rows.every(r=>object(r)&&nonempty(r.id)) && new Set(rows.map(r=>r.id)).size===rows.length
  if(!object(value)) return 'Invalid backup object.'
  const {settings:s,categories,events,applications}=value
  if(!object(s) || !['light','dark','system'].includes(s.theme) || ![0,1].includes(s.weekStartsOn) || !['month','week','day','agenda'].includes(s.defaultView) || !integer(s.dayStartHour,0,23) || !integer(s.dayEndHour,1,24) || s.dayEndHour<=s.dayStartHour || !integer(s.dailyGoal,1) || !integer(s.stalePeriodDays,1) || !text(s.displayName) || ['use24Hour','autoScheduleInterviews','showWeekNumbers'].some(k=>typeof s[k]!=='boolean'))return 'Invalid backup settings.'
  if(!stamp(value.exportedAt))return 'Invalid export timestamp.'
  for(const [name,rows] of [['categories',categories],['events',events],['applications',applications]] as const)if(!Array.isArray(rows)||rows.length>100000||!unique(rows))return `Invalid or duplicate ${name} IDs.`
  for(const c of categories)if(!nonempty(c.name)||!integer(c.slot,1,8)||typeof c.hidden!=='boolean')return 'Invalid calendar category.'
  for(const e of events) {
    if(!nonempty(e.title)||!text(e.notes)||!text(e.location)||!text(e.categoryId)||typeof e.allDay!=='boolean'||!local(e.start)||!local(e.end)||e.end<=e.start||!stamp(e.createdAt)||!stamp(e.updatedAt)||!Array.isArray(e.exceptions)||!e.exceptions.every(date))return 'Invalid calendar event.'
    if(e.recurrence!==null) {const r=e.recurrence;if(!object(r)||!['daily','weekly','monthly','yearly'].includes(r.freq)||!integer(r.interval,1,1000)||!Array.isArray(r.byWeekday)||!r.byWeekday.every((d:unknown)=>integer(d,0,6))||(r.until!==null&&!date(r.until)))return 'Invalid event recurrence.'}
    if(e.detachedFrom!==undefined&&(!object(e.detachedFrom)||!nonempty(e.detachedFrom.seriesId)||!date(e.detachedFrom.date)))return 'Invalid detached event.'
    if(e.jobId!==undefined&&!text(e.jobId))return 'Invalid linked application.'
  }
  for(const a of applications) {
    if(!nonempty(a.company)||!nonempty(a.role)||!JOB_STAGES.includes(a.stage)||!date(a.appliedDate)||!['remote','hybrid','onsite','unknown'].includes(a.workMode)||!stamp(a.createdAt)||!stamp(a.updatedAt)||typeof a.starred!=='boolean'||['location','source','url','notes','contact'].some(k=>!text(a[k]))||!Array.isArray(a.tags)||!a.tags.every(text))return 'Invalid application record.'
    for(const salary of [a.salaryMin,a.salaryMax])if(salary!==null&&(typeof salary!=='number'||!Number.isFinite(salary)||salary<0))return 'Invalid salary.'
    if(a.salaryMin!==null&&a.salaryMax!==null&&a.salaryMin>a.salaryMax)return 'Salary minimum exceeds maximum.'
    if(!Array.isArray(a.history)||!a.history.length||!unique(a.history)||a.history.some((h:any)=>!JOB_STAGES.includes(h.stage)||!date(h.date)||!text(h.note)))return 'Invalid application history.'
  }
  return null
}
''')
p=B/'stage/73/src/lib/backup.test.ts';s=p.read_text();s+='''
describe('nested backup validation', () => {
  it('rejects impossible dates, duplicate identities and invalid recurrence before store replacement', () => {
    for (const mutate of [
      (b: ReturnType<typeof validBackup>) => { b.events[0].start = '2026-02-30T09:00' },
      (b: ReturnType<typeof validBackup>) => { b.events.push({...b.events[0]}) },
      (b: ReturnType<typeof validBackup>) => { b.events[0].recurrence = {freq:'daily',interval:0,byWeekday:[],until:null} },
      (b: ReturnType<typeof validBackup>) => { b.applications[0].history = [] },
      (b: ReturnType<typeof validBackup>) => { b.settings.dayEndHour = b.settings.dayStartHour },
      (b: ReturnType<typeof validBackup>) => { b.applications[0].salaryMin = 200; b.applications[0].salaryMax = 100 },
    ]) { const backup=validBackup(); mutate(backup); expect(parseBackup(JSON.stringify(backup)).ok).toBe(false) }
  })
  it('rejects nested nonobjects and unsupported older versions without throwing', () => {
    const backup=validBackup()
    for(const extra of [{events:[null]},{applications:[{id:'broken'}]},{settings:[]},{version:-1}])expect(parseBackup(JSON.stringify({...backup,...extra})).ok).toBe(false)
  })
})
''';p.write_text(s)
p=B/'stage/74/src/db.ts';s=p.read_text();s="import { validateImport } from './importValidation';\n"+s;start=s.index('  if (payload.schemaVersion !== SCHEMA_VERSION)',s.index('export async function importData'));end=s.index('  const knownIds',start);s=s[:start]+'  validateImport(payload);\n'+s[end:];s=s.replace('const logs = (payload.reviewLogs ?? []).map(l => {','const logs = payload.reviewLogs.filter(l => knownIds.has(l.cardId)).map(l => {');p.write_text(s)
(B/'stage/74/src/importValidation.ts').write_text('''import { ALL_CARD_TYPES, SCHEMA_VERSION, type ExportData } from './types';
/** Validate the entire import before opening the replacement transaction. */
export function validateImport(payload: unknown): asserts payload is ExportData {
 const object=(v:unknown):v is Record<string,any>=>!!v&&typeof v==='object'&&!Array.isArray(v);
 const text=(v:unknown)=>typeof v==='string'&&v.length>0&&v.length<=200;
 const number=(v:unknown,min=0,max=Number.MAX_SAFE_INTEGER)=>typeof v==='number'&&Number.isFinite(v)&&v>=min&&v<=max;
 const integer=(v:unknown,min=0,max=Number.MAX_SAFE_INTEGER)=>number(v,min,max)&&Number.isInteger(v);
 const day=(v:unknown)=>v===null||(typeof v==='string'&&/^\\d{4}-\\d{2}-\\d{2}$/.test(v)&&Number.isFinite(Date.parse(v))&&new Date(v).toISOString().slice(0,10)===v);
 const statuses=['new','learning','review','relearning'];
 const fail=(field:string):never=>{throw new Error(`Malformed backup: ${field}`);};
 if(!object(payload)||payload.schemaVersion!==SCHEMA_VERSION)fail('unsupported schema version');
 const p=payload as Record<string,any>;
 if(!number(p.exportedAt)||!Array.isArray(p.reviewStates)||!Array.isArray(p.reviewLogs)||p.reviewStates.length>100000||p.reviewLogs.length>1000000)fail('review arrays');
 const ids=new Set<string>();
 for(const s of p.reviewStates){if(!object(s)||!text(s.cardId)||ids.has(s.cardId)||!number(s.ease,1,10)||!number(s.intervalDays)||!number(s.due)||!statuses.includes(s.status)||!integer(s.learningStepIndex,0,100)||!integer(s.lapses)||!integer(s.reps))fail('review state');ids.add(s.cardId);}
 for(const l of p.reviewLogs)if(!object(l)||!text(l.cardId)||!number(l.reviewedAt)||!integer(l.grade,0,3)||!number(l.msTaken)||!statuses.includes(l.statusBefore))fail('review log');
 const s=p.settings;if(!object(s)||!integer(s.newCardsPerDay,0,10000)||!integer(s.maxReviewsPerDay,0,100000)||!['light','dark'].includes(s.theme)||!Array.isArray(s.enabledCardTypes)||!s.enabledCardTypes.every((t:any)=>ALL_CARD_TYPES.includes(t))||!Array.isArray(s.enabledDeckIds)||!s.enabledDeckIds.every(text))fail('settings');
 const m=p.meta;if(!object(m)||m.id!=='meta'||m.schemaVersion!==SCHEMA_VERSION||!day(m.lastReviewDay)||!day(m.newIntroDay)||!integer(m.streak)||!integer(m.bestStreak)||m.bestStreak<m.streak||!integer(m.newIntroCount))fail('progress metadata');
}
''')
