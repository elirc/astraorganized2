from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/79c315026b95'
p=P/'tests/runtime-allocation-state-lab.test.mjs';t=p.read_text();t='\n'.join(l for l in t.split('\n') if not l.startswith('class ValidationError'))
a=t.index("  '@prisma/client':");b=t.index('}});',a)
t=t[:a]+'''  '@/repositories/allocationRunRepository': {createAllocationRun:()=>{},getAllocationRunById:()=>{},listAllocationRuns:()=>{},replaceAllocationResults:()=>{},updateAllocationRunStatus:()=>{}},
  '@/services/allocationEngineService': {computeAllocationResults:()=>{}},
  '@/lib/queue/allocationQueue': {registerAllocationWorker:()=>{},enqueueAllocationRun:()=>{}},
'''+t[b:]
t=t.replace('e.status === 422', "e.statusCode === 422 && e.code === 'VALIDATION_ERROR'")
p.write_text(t)
s=B/'specs/79c315026b95.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['limits'].append('Real ValidationError is loaded. Unexecuted repository/engine exports and queue registration are adapted. Worker catch directly writes FAILED without transition guard; terminal helper refusal does not certify worker immutability.');s.write_text(json.dumps(d,indent=2))
