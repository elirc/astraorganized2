from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/ec28c8c40e53'
p=P/'tests/runtime-aggregation-state-lab.test.mjs';t=p.read_text();t='\n'.join(l for l in t.split('\n') if not l.startswith('class AppError'))
t=t.replace("{ root, stubs: {\n  '@/lib/http/app-error': { AppError },\n}}",'{ root }');p.write_text(t)
s=B/'specs/ec28c8c40e53.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['limits'].append('State guard and real AppError execute without behavior doubles. Worker claim and completion transactions were inspected, not executed.');s.write_text(json.dumps(d,indent=2))
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace('evidence/astra-crud-b07-ww47.log','evidence/crud-b07-astra-runtime.log').replace('evidence/results-crud-b07.json','evidence/results.json').replace('guard?s',"guard's").replace('with an explicit AppError boundary','with the actual AppError class and no behavior doubles').replace('from the staged project','from the project directory')
 t=t.replace('after rollups commit','inside the rollup completion transaction').replace('already uses an atomic queued-to-running update','uses a conditional queued-to-running update')
 t=t.replace('then checks count one, preventing two workers from both claiming the same row.','then checks count one. This is the intended single-claim boundary; the pure lab does not execute concurrent workers.')
 if p.name=='VERIFICATION.md':t+='\nSource inspection also shows separate claim and completion transactions. A process crash after claim can leave RUNNING work; this policy lab adds no recovery mechanism. Terminal refusal is a state-helper contract, not evidence that every service write enforces its current persisted status.\n'
 p.write_text(t,encoding='utf-8')
