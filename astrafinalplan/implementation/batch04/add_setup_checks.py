from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/66/test/environments.test.ts';s=p.read_text(encoding='utf-8');s+='''
test("saved request header/parameter arrays survive create, partial edit and duplication",async()=>{
 const r=await api("/requests","POST",{name:"Local fixture",method:"GET",url:"http://localhost:3000/health",headers:[{key:"Accept",value:"application/json"}],params:[{key:"limit",value:"2"}]});assert.equal(r.status,201,JSON.stringify(r.data));const id=r.data.data.id;assert.deepEqual(r.data.data.headers,[{key:"Accept",value:"application/json"}]);const edit=await api(`/requests/${id}`,"PUT",{name:"Renamed"});assert.equal(edit.status,200);assert.deepEqual(edit.data.data.params,[{key:"limit",value:"2"}]);const copy=await api(`/requests/${id}/duplicate`,"POST",{});assert.equal(copy.status,201);assert.deepEqual(copy.data.data.headers,r.data.data.headers);
});
''';p.write_text(s,encoding='utf-8')
p=B/'run_checks.py';s=p.read_text(encoding='utf-8');s=s.replace(" client=root/'client'", " if 58<=n<=71:tasks.append((str(n),'server-build',root/'server',['node',str(H/'node_modules/typescript/bin/tsc'),'-p','tsconfig.json']))\n client=root/'client'");p.write_text(s,encoding='utf-8')
