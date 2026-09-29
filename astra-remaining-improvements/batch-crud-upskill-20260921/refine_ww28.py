from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/5528ac452b91'
p=P/'tests/runtime-upload-bounds.test.mjs';t=p.read_text()
t='\n'.join(l for l in t.split('\n') if not l.startswith('class ValidationError') and not l.startswith('class ConflictError'))
t=t.replace("activeTenantId: 'tenant-1'", "activeTenantId: 'tenant-1', tenantRole: 'TENANT_MEMBER'")
a=t.index("{ root, stubs: {"); b=t.index('  }});',a)
t=t[:a]+'{ root });'+t[b+6:]
t=t.replace('e.status === 400','e.statusCode === 400')
t+='''
test('upper bound retry preserves chunk identity and deletes before replacing storage', async () => {
  const f = fixture();
  f.fileRepository.findChunkByPart = (tenant, file, part) => {
    assert.deepEqual([tenant, file, part], ['tenant-1', 'file-1', 2]);
    return { id: 'existing-2', partNumber: 2 };
  };
  f.fileRepository.upsertChunk = chunk => {
    assert.equal(chunk.id, 'existing-2');
    assert.equal(chunk.partNumber, 2);
    f.calls.push(['upsert', 2]);
  };
  const service = await serviceFor(f);
  const result = await service.uploadPart(session, 'upload-1', { partNumber: 2, contentBase64: 'eA==' });
  assert.equal(result.retriedPart, true);
  assert.deepEqual(f.calls, [['delete'], ['write', 2], ['upsert', 2]]);
});
'''
p.write_text(t)
s=B/'specs/5528ac452b91.json';d=json.loads(s.read_text(encoding='utf-8-sig'))
d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')]
d['summary']=[n.replace('four dependency-free','five dependency-free') for n in d['summary']]
d['limits'].append('Actual guards, permission rules, base64 utility and error classes execute. Repository/storage adapters do not verify durable storage or atomic retry replacement; delete precedes replacement write.')
s.write_text(json.dumps(d,indent=2))
