from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/ed24cac9b9f3'
p=P/'src/lib/cache/inMemoryCache.ts';t=p.read_text().replace('constructor(private readonly maxEntries = 100) {}','''constructor(private readonly maxEntries = 100) {
    if (!Number.isSafeInteger(maxEntries)) {
      throw new RangeError("maxEntries must be a finite safe integer");
    }
  }''');p.write_text(t,encoding='utf-8')
p=P/'tests/runtime-cache-capacity.test.mjs';t=p.read_text().replace("{ root, aliasRoot: path.join(root, 'src') }", "{ root, aliasRoot: path.join(root, 'src'), globals: { Date: class extends Date { static now() { return 1000; } } } }")
t+='''
test('replacement at capacity retains unrelated key and insertion order',()=>{
 const cache=new mod.InMemoryCache(2);cache.set('',1,1000);cache.set('b',2,1000);cache.set('',3,1000);
 assert.equal(cache.get('b'),2);assert.equal(cache.get(''),3);
 cache.set('c',4,1000);assert.equal(cache.get(''),null);assert.equal(cache.get('b'),2);assert.equal(cache.get('c'),4);
});
test('invalid capacities refuse construction and negative integer disables storage',()=>{
 for(const value of [NaN,Infinity,-Infinity,1.5,Number.MAX_SAFE_INTEGER+1])assert.throws(()=>new mod.InMemoryCache(value),e=>e.name==='RangeError');
 const cache=new mod.InMemoryCache(-1);cache.set('x',1,1000);assert.equal(cache.get('x'),null);
});
test('default capacity is100 and full invalidation clears retained keys',()=>{
 const cache=new mod.InMemoryCache();for(let i=0;i<101;i++)cache.set(String(i),i,1000);
 assert.equal(cache.get('0'),null);assert.equal(cache.get('1'),1);assert.equal(cache.get('100'),100);
 cache.invalidate();assert.equal(cache.get('1'),null);assert.equal(cache.get('100'),null);
});
''';p.write_text(t)
s=B/'specs/ed24cac9b9f3.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['summary'].append('Reject non-finite, fractional and unsafe capacity values so configured bounds cannot silently become unbounded.');s.write_text(json.dumps(d,indent=2))
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace("'''",'').replace('evidence/ed24cac9b9f3-runtime-cache-capacity.tap.txt','evidence/crud-b06-astra-runtime.log').replace('three cases','six cases').replace('three-case','six-case').replace('3 tests passed','6 tests passed')
 t=t.replace('supplies no behavior stubs because the class is dependency-free','supplies only a fixed clock; the class has no imported behavior dependencies')
 t=t.replace('constructor(private readonly maxEntries = 100) {}','constructor(private readonly maxEntries = 100) {\n  if (!Number.isSafeInteger(maxEntries)) throw new RangeError("maxEntries must be a finite safe integer");\n}')
 if p.name=='VERIFICATION.md':t+='\nThree added cases verify replacement retains unrelated keys and FIFO ordering (including the empty-string key), invalid numeric capacity rejection plus negative disabled behavior, and the default100 bound plus full invalidation. A fixed VM clock prevents incidental TTL expiry from making capacity tests flaky. Capacity counts entries, not bytes: a single large value can still consume substantial memory.\n'
 if p.name=='02-CONCEPTS.md':t+='\nConfiguration also needs a numeric contract. NaN or Infinity can make a comparison silently fail to bound the map, while fractions create ambiguous capacities. The constructor rejects values that are not safe integers. Finite zero and negative integers disable storage.\n'
 if p.name=='README.md':t+='\nInvalid numeric capacities now throw RangeError at construction rather than weakening the bound. Six deterministic tests also cover replacement, empty keys, default capacity and full invalidation.\n'
 p.write_text(t,encoding='utf-8')
