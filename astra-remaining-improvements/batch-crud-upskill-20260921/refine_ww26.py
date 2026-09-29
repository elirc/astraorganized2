from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/971a7c784720'
p=P/'tests/runtime-lock-coordinator-lab.test.mjs'
t=p.read_text()
t=t.replace("class ApiError extends Error { constructor(status, code, message) { super(message); this.status = status; this.code = code; } }\n",'')
a=t.index("    '@/lib/auth/permissions':")
b=t.index("    '@/lib/db/prisma':",a)
t=t[:a]+t[b:]
t=t.replace("    '@/lib/http/apiError': { ApiError },\n",'').replace("LockAcquireOutcome: {}, Session: {}", "LockAcquireOutcome: {}, Session: {}, UserRole: {}")
t=t.replace('e instanceof ApiError && ', '')
p.write_text(t)
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace('scope?s',"scope's").replace('transaction?s',"transaction's").replace('lab?s',"lab's").replace('project?s',"project's").replace('owner?s',"owner's").replace('?concurrency?', 'concurrency')
 t=t.replace('supplies an ApiError class, permission rule, database transaction, and repository operations','loads the real ApiError and permission rule, while supplying database transaction and repository adapters')
 t=t.replace('from the staged project','from the project directory').replace('evidence/astra-crud-b06-ww26.log','evidence/crud-b06-astra-runtime.log').replace('evidence/results-crud-b06.json','evidence/results.json')
 p.write_text(t,encoding='utf-8')
s=B/'specs/971a7c784720.json'; d=json.loads(s.read_text(encoding='utf-8-sig'))
d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')]
d['limits'].append('Authorization and ApiError execute from actual source; repository/transaction adapters do not establish row locking or isolation.')
s.write_text(json.dumps(d,indent=2))
