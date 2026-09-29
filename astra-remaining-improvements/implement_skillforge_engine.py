from pathlib import Path
s=Path(__file__).resolve().parent/'stage/a9672affc47e';p=s/'src/types.ts';t=p.read_text(encoding='utf-8');t=t.replace('export interface GameProgress {','export interface LearningNote {\n  id: string;\n  missionId: string;\n  title: string;\n  body: string;\n  updatedAt: string;\n}\n\nexport interface GameProgress {\n  revision: number;\n  notes: LearningNote[];');p.write_text(t,encoding='utf-8')
p=s/'src/game/engine.ts';t=p.read_text(encoding='utf-8');t=t.replace('    version: 1,','    version: 1,\n    revision: 0,\n    notes: [],',1)
t=t.replace('const REVIEW_INTERVALS = [2, 7, 30, 90, 180, 365] as const;', '''const REVIEW_INTERVALS = [2, 7, 30, 90, 180, 365] as const;
function clock(now: Date): void {
  if (!(now instanceof Date) || !Number.isFinite(now.getTime()) || now.getTime() < 0) throw new Error("Use a valid clock value.");
}
function checkedXp(value: number): number {
  if (!Number.isSafeInteger(value) || value < 0 || value > 1_000_000_000) throw new Error("Progress XP is outside its supported range.");
  return value;
}
function ratingValue(rating: ReviewRating): void {
  if (!["again", "hard", "good", "easy"].includes(rating)) throw new Error("Unknown review rating.");
}''')
t=t.replace('  const key = challengeKey(mission.id, challenge.id);\n  const response =', '''  clock(now);
  if (!isMissionUnlocked(mission, progress)) throw new Error("Complete this mission's prerequisites first.");
  const canonical = mission.challenges.find(item => item.id === challenge.id);
  if (!canonical) throw new Error("This checkpoint does not belong to the mission.");
  challenge = canonical;
  const key = challengeKey(mission.id, challenge.id);
  const response =''')
t=t.replace('xp: progress.xp + challenge.xp + (newlyCompleted ? mission.xp : 0),','xp: checkedXp(progress.xp + challenge.xp + (newlyCompleted ? mission.xp : 0)),')
t=t.replace('export function createReviewRecord(missionId: string, now = new Date()): ReviewRecord {\n  return {','export function createReviewRecord(missionId: string, now = new Date()): ReviewRecord {\n  clock(now);\n  return {')
t=t.replace('  let stage = record.stage;','''  clock(now); ratingValue(rating);
  if (!Number.isInteger(record.stage) || record.stage < 0 || record.stage > REVIEW_INTERVALS.length || !Number.isSafeInteger(record.reviews) || record.reviews < 0 || !Number.isSafeInteger(record.lapses) || record.lapses < 0 || record.lapses > record.reviews) throw new Error("The review record is invalid.");
  let stage = record.stage;''')
t=t.replace('  const existing = progress.reviews[missionId];','''  clock(now); ratingValue(rating);
  const existing = progress.reviews[missionId];''')
t=t.replace('  if (!existing) throw new Error("Complete the mission before reviewing it.");','''  if (!existing || !progress.completedMissions.includes(missionId)) throw new Error("Complete the mission before reviewing it.");
  const due = new Date(existing.due).getTime();
  if (!Number.isFinite(due) || due > now.getTime()) throw new Error("This mission is not due for review yet.");''')
t=t.replace('xp: progress.xp + ({ again: 5, hard: 10, good: 20, easy: 30 }[rating]),','xp: checkedXp(progress.xp + ({ again: 5, hard: 10, good: 20, easy: 30 }[rating])),')
p.write_text(t,encoding='utf-8')
p=s/'src/game/engine.test.ts';t=p.read_text(encoding='utf-8').replace('const progress = { ...createProgress(), reviews: { m1:', 'const progress = { ...createProgress(), completedMissions: ["m1"], reviews: { m1:');p.write_text(t,encoding='utf-8');print('Added engine prerequisite, checkpoint, due-review and runtime-value guards; verification pending')
