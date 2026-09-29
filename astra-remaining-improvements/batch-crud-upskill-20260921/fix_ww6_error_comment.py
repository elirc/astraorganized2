from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/79c315026b95';p=P/'src/lib/http/errors.ts'
snap=P/'astraupskill/snapshots/errors.ts.original.txt';snap.parent.mkdir(exist_ok=True)
assert not snap.exists();snap.write_bytes(p.read_bytes())
t=p.read_text();assert 'src/app/api/**/route.ts' in t;t=t.replace('`src/app/api/**/route.ts`','the src/app/api route tree');p.write_text(t,encoding='utf-8')
s=B/'specs/79c315026b95.json';d=json.loads(s.read_text());d['changedFiles']+=['src/lib/http/errors.ts','astraupskill/snapshots/errors.ts.original.txt'];d['summary'][0]='Fix an accidentally terminated block comment in the real HTTP error module so TypeScript can parse it.';d['limits']=[x for x in d['limits'] if x!='No production fix warranted in reviewed path.'];s.write_text(json.dumps(d,indent=2))
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace('No production source changed, so no snapshot is needed.','A production comment syntax fix is included: the route glob contained a block-comment terminator. The [original error module](snapshots/errors.ts.original.txt) preserves the exact before bytes.').replace('No production source was changed.','Only the malformed route-reference comment in the real error module was corrected; runtime error behavior is unchanged.').replace('rather than an unverified worker patch','with a real error-module comment syntax repair')
 if p.name=='VERIFICATION.md':t+='\nThe initial real-error run failed during TypeScript parsing because a route glob inside the block comment contained a closing-comment token. Rewording that comment made the actual module parse; this is why replacing error doubles matters. Earlier failed evidence remains preserved in the workspace.\n'
 p.write_text(t,encoding='utf-8')
