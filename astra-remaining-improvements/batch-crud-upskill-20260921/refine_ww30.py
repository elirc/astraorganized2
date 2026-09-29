from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/41ea8dcef618'
p=P/'tests/runtime-cache-expiry.test.mjs';t=p.read_text().replace("now = 1100; assert.equal(cache.get('exact'), null);", "now = 1100; assert.equal(cache.get('exact'), null); now = 1000; assert.equal(cache.get('exact'), null, 'expired entry was deleted even if the clock moves backward');")
p.write_text(t)
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace(".''",'.').replace('evidence/41ea8dcef618-runtime-cache-expiry.tap.txt','evidence/crud-b06-astra-runtime.log')
 t=t.replace('The exact-expiry case should also call `get` again and still receive null, proving deletion rather than a temporary sentinel.','The exact-expiry case rewinds the injected clock to insertion time and still receives null. This distinguishes deletion from repeatedly suppressing a retained expired entry.')
 t=t.replace('The first read should delete it; the second should also return null. Why is this stronger than one assertion? It distinguishes eviction from returning a stale or cached sentinel.','After expiry, rewind the injected clock before the second read. Returning null now proves the value was removed rather than merely withheld while the clock was beyond expiry.')
 t=t.replace('Exercise two checks lazy eviction: the first read deletes, so the second cannot recover the value.','Exercise two checks lazy eviction by rewinding the clock after expiry; the deleted value cannot reappear.')
 t=t.replace('role-aware keys are sufficient only for the product’s current visibility model','role-aware keys must be assessed against the actual visibility model')
 t=t.replace('The current product uses global order data and role in the key.','The inspected service includes role in the key; this lab does not certify row-level authorization.')
 p.write_text(t,encoding='utf-8')
s=B/'specs/41ea8dcef618.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];s.write_text(json.dumps(d,indent=2))
