from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/d7c9faad43d9'
t=P/'tests/runtime-shop-city.test.mjs';s=t.read_text()
s=s.replace("const storage = { json: JSON.stringify(base), writes: 0 };", "const storage = { json: JSON.stringify(base), writes: 0, error: null };\nfunction reset() { storage.json=JSON.stringify({...base,shops:[{id:9,cityId:7,name:'Existing'}]});storage.writes=0;storage.error=null; }")
s=s.replace('storage.writes++; storage.json = value;', 'storage.writes++; if(storage.error) throw storage.error; storage.json = value;')
s=s.replace('root, aliasRoot: root,','root, aliasRoot: path.join(root, \'src\'),')
start=s.index("    '@/lib/utils':");end=s.index('\n  }',start)
s=s[:start]+'''    clsx: {default:()=>''},
    slugify: {default:(value, options)=>{assert.equal(options.lower,true);assert.equal(options.strict,true);assert.equal(options.trim,true);return value.trim().toLowerCase().replace(/[^a-z0-9]+/g,'-');}}
'''+s[end:]
s=s[:s.index("test('shop creation")]+'''
test('valid parent preserves existing rows, normalizes payload and serializes once',async()=>{
 reset();const shop=await mod.createShopStore({...payload,name:' Good Shop ',address:'   ',specialties:[' plain ','plain','']});
 assert.equal(shop.id,10);assert.equal(shop.cityId,7);assert.equal(shop.name,'Good Shop');assert.equal(shop.slug,'good-shop');assert.equal(shop.address,null);assert.deepEqual(Array.from(shop.specialties),['plain']);assert.equal(shop.isPublished,false);assert.equal(shop.createdAt,shop.updatedAt);
 assert.equal(storage.writes,1);const saved=JSON.parse(storage.json);assert.deepEqual(saved.shops[0],{id:9,cityId:7,name:'Existing'});assert.deepEqual(saved.shops[1],JSON.parse(JSON.stringify(shop)));assert.deepEqual(saved.cities,base.cities);
});
test('unknown and wrong-type parent ids preserve serialized bytes with zero file writes',async()=>{
 for(const cityId of [999,'7']) {reset();const before=storage.json;await assert.rejects(()=>mod.createShopStore({...payload,cityId}),/City not found/);assert.equal(storage.writes,0);assert.equal(storage.json,before);}
});
test('write failure reaches caller without a successful return or saved new row',async()=>{
 reset();const error=new Error('disk unavailable');storage.error=error;const before=storage.json;
 await assert.rejects(()=>mod.createShopStore(payload),e=>e===error);assert.equal(storage.writes,1);assert.equal(storage.json,before);
});
test('repeated valid creates allocate subsequent ids and retain the existing duplicate-name policy',async()=>{
 reset();const first=await mod.createShopStore(payload);const second=await mod.createShopStore(payload);
 assert.equal(first.id,10);assert.equal(second.id,11);assert.equal(first.slug,second.slug);assert.equal(storage.writes,2);assert.equal(JSON.parse(storage.json).shops.length,3);
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/d7c9faad43d9.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'))
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Four runtime cases execute actual store and utility source with filesystem, path, slugify, clsx, scoring and schema adapters. Real nullable-text and array normalization execute; third-party slug behavior is not established.', 'No native filesystem, SQL, HTTP auth, cascade, locking or concurrent write behavior executed. readStore may call mkdir before rejecting an unknown city; zero writes means zero writeFile calls, not zero filesystem activity.', 'The write-failure adapter throws before storing bytes; this does not prove native writeFile is atomic or preserves a file on partial failure. Local Next.js guides absent after cleanup; no framework API was changed.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
