from pathlib import Path
import re,json
B=Path(__file__).resolve().parent.parent;D=B/'stage/54397e702f3f/astraupskill'
for p in D.glob('*.md'):
    t=p.read_text()
    t=re.sub(r'\bADMIN\b','OPS_MANAGER',t)
    t=re.sub(r'\bMANAGER\b','PRODUCT_MANAGER',t)
    t=t.replace('both conditions are false','the isDefault condition is false because it is omitted')
    t=t.replace('5. Target preserves OPS_MANAGER/true; no peer clear.', '5. Target preserves OPS_MANAGER/true; OPS_MANAGER peers are cleared even for a name-only update.')
    t=t.replace('Four tests cover','Eight tests cover')
    t=t.replace('Four tests passed','Eight tests passed')
    t=t.replace('It proves four PATCH cases and the service side effect.', 'It checks effective-state cases and actual service calls for role transfer, explicit unset, setting a default, moving a nondefault, renaming a default, and a missing resource.')
    t=t.replace('The earlier npm dependency attempt remains recorded in `checks/54397e702f3f/results-crud-b01.json`; the runtime loader is the passing terminal check.', 'Earlier dependency-attempt records remain in the workspace checks directory; the captured runtime evidence below is the accepted terminal check.')
    t=t.replace('Ask for audit coverage if ordering changes. Ask for audit coverage if ordering changes.', 'Ask for audit coverage if ordering changes.')
    if p.name=='02-CONCEPTS.md':
        t+='\nThe existing create operation is also outside this repair: it can create a default without clearing peers. Therefore the invariant above is the intended product rule, not a global guarantee established by this PATCH fix. A later database constraint and migration must account for both create and update paths and reconcile existing data explicitly.\n'
    if p.name=='04-TESTING-AND-DEBUGGING.md':
        t+='\nThe expanded runtime suite also calls the actual service for a role-omitted new default, a nondefault role move, a name-only edit of a default, and a missing id. A name-only edit still clears peers because the effective default remains true; do not predict no write merely because role is absent.\n'
    p.write_text(t,encoding='utf-8')
f=B/'specs/54397e702f3f.json';s=json.loads(f.read_text())
s['summary']=['Repair default-peer clearing for dashboard configuration PATCHes with omitted role or default fields.','Add eight runtime regressions plus nine source-linked CRUD chapters with effective-state exercises and solved traces.']
s['limits']=['Focused Node runtime tests use explicit Prisma transaction spies; real SQL rollback, isolation, HTTP authorization and browser behavior were not executed.','Normal Vitest suite, full typecheck and build were not run. The existing pre-read and create path mean this PATCH repair does not guarantee global or concurrent default uniqueness.']
f.write_text(json.dumps(s,indent=2),encoding='utf-8')
print('Analytics teaching corrected to actual role enums and tested branches')
