from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/1d0b328c6621/astraupskill'
for f in P.glob('*.md'):
 s=f.read_text(encoding='utf-8-sig').replace('Compare the original snapshot and current source during review.','').replace('Source links and evidence remain available for review.','')
 s=s.replace('repository and audit are explicit doubles','the repository also runs from production source; state and audit are explicit adapters').replace('Limits are mocked repositories.','Limits include substituted state and audit persistence.').replace('type contracts, repository, and audit doubles','type-only placeholders, state, id and audit adapters')
 s=s.replace('Two tests pass','Four tests pass').replace('numeric count is two tests','numeric count is four tests')
 s=s.replace('Answers: only draft reaches repository and audit; active and retired stop; missing stops at target lookup.','Write your predictions before reading the separate solutions chapter.')
 if f.name=='02-CONCEPTS.md':s+='''\nAn ACTIVE request could instead have been designed as an idempotent no-op, but this application now chooses explicit rejection to prevent repeated activation history. That is an observable compatibility decision: callers should not assume repeated requests succeed. RETIRED was already rejected; its message now uses the common draft-only wording. The actual repository retires active siblings only when protocolCode matches the target. It leaves other studies and participant pins untouched. These are separate invariants from draft eligibility, so the accepted positive test executes the real repository and inspects all three kinds of state. Audit is a later operation and is not wrapped with activation in a transaction.\n'''
 if f.name=='05-PRACTICE.md':s+='''\nScore two points each for status classification, same-code retirement, unrelated-state preservation, audit payload and failure limitations. Inject audit failure after activation and predict whether the target is still ACTIVE. Explain which evidence would be needed to claim atomicity.\n'''
 if f.name=='07-TRACE-LAB.md':s+='''\n| Scenario | Target after call | Sibling | Audit |
|---|---|---|---|
| Draft success | ACTIVE | Same-code ACTIVE becomes RETIRED | One |
| ACTIVE refusal | Unchanged | Unchanged | None |
| Missing id | No target | Unchanged | None |
| Audit rejects | ACTIVE remains | Retirement remains | One failed attempt |
\n'''
 if f.name=='06-SOLUTIONS-AND-REVIEW.md':s+='''\nThe expanded four-case lab uses the real repository: other-code ACTIVE rows remain the same objects, participant pins remain unchanged and the audit records actor u1 with target draft. An audit rejection propagates after state changed. It does not roll activation back; do not teach it as an atomic operation.\n'''
 if f.name=='VERIFICATION.md':s+='''\nAccepted root capture crud-b05-astra-runtime2 runs four cases using actual service, rule and repository. A first attempt failed because Node retained type-only imports; explicit placeholder exports now satisfy that loader boundary. State/id/audit remain adapters. The suite adds missing and retired refusals, same-code sibling retirement, unrelated protocol and participant preservation, and original audit-error propagation with already-mutated state.\n'''
 s='\n\n'.join(x.strip() for x in s.split('\n\n') if x.strip())+'\n';f.write_text(s,encoding='utf-8');print(f.name,len(s.split()))
sp=B/'specs/1d0b328c6621.json';spec=json.loads(sp.read_text());spec['limits'][0]=spec['limits'][0].replace('only mock-state, id and audit adapters','mock-state, id, audit and type-only export adapters');sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
