from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent
p=b/'stage/efb20378d966'
f=p/'tests/runtime-role-duplicates.test.mjs';s=f.read_text(encoding='utf-8-sig')
s=s.replace('const repository = {','const tx = Object.freeze({ transactionIdentity: true });\n  const repository = {')
s=s.replace('calls.findMembership++; return membership;', "assert.equal(args[0].tenantId, 'tenant-1'); assert.equal(args[1], tx); calls.findMembership++; return membership;")
s=s.replace('async (args) => { calls.replace.push(args);', 'async (args, client) => { assert.equal(client, tx); calls.replace.push(args);')
s=s.replace('return ids.map((id) => ({ id, tenantId }));', 'return [...new Set(ids)].map((id) => ({ id, tenantId }));')
s=s.replace('return callback({});','return callback(tx);')
s=s.replace('calls.audit.push(args);', 'assert.equal(args.client, tx); calls.audit.push(args);')
s=s.replace("const result = await service.replaceTenantUserRoles({ tenantId: 'tenant-1', membershipId: 'membership-1', actor, roleIds: ['role-a', 'role-a', 'role-b'] });", "const input = Object.freeze(['role-a', 'role-a', 'role-b']);\n  const result = await service.replaceTenantUserRoles({ tenantId: 'tenant-1', membershipId: 'membership-1', actor, roleIds: input });\n  assert.deepEqual(input, ['role-a', 'role-a', 'role-b']);\n  assert.equal(f.calls.validate[0].tenantId, 'tenant-1');\n  assert.equal(f.calls.replace[0].tenantId, 'tenant-1');\n  assert.equal(f.calls.replace[0].membershipId, 'membership-1');")
s=s.replace("const failure = new Error('unique relation failure');", "const failure = new Error('repository unavailable');")
f.write_text(s,encoding='utf-8')
for f in (p/'astraupskill').glob('*.md'):
 s=f.read_text(encoding='utf-8-sig')
 s=s.replace("A request such as `['role-reader', 'role-reader', 'role-editor']` could pass `findRolesByIds` validation if the repository returned three rows, yet the membership relation has a uniqueness boundary for one membership and one role.", "For `['role-reader', 'role-reader', 'role-editor']`, the actual tenant-scoped repository query returns two distinct role rows. Comparing that count with three raw input items rejected an otherwise valid membership set with status 400 before persistence. The fix accepts this duplicate intent by normalizing first; the original code did not persist duplicate edges on this path.")
 s=s.replace('A duplicate list could therefore reach [replaceMembershipRoles](../server/src/repositories/userRepository.js), whose relation creation has a uniqueness boundary. The failure would be discovered after the service had accepted the request shape, and any debugging record would still show the duplicate input.', 'Because the actual role query returns distinct rows, valid duplicate input failed that comparison and raised status 400 before transaction entry. [replaceMembershipRoles](../server/src/repositories/userRepository.js) was not reached for such input. Normalization changes the API policy from accidental duplicate rejection to tolerant set replacement, while retaining missing-role rejection.')
 s=s.replace('arrays created inside the loaded module are not reference-equal to host arrays, so the test compares serialized values.', 'arrays created inside the loaded module have different realm prototypes, so the test compares serialized values rather than treating a cross-realm prototype mismatch as a value mismatch.')
 if f.name=='VERIFICATION.md': s+='\nThe fixture returns distinct role rows, freezes the caller input, and checks that lookup, replacement and audit receive the same modeled transaction handle. This verifies argument wiring, not database atomicity. The separate createTenantUser path is unchanged; this lesson concerns role replacement only. Role validation remains outside the transaction, so concurrent role deletion remains a database-level concern.\n'
 f.write_text(s,encoding='utf-8')
f=b/'specs/efb20378d966.json';spec=json.loads(f.read_text(encoding='utf-8-sig'))
spec['id']='efb20378d966';spec['project']='_Organized Desktop/04 JavaScript Training/jstrain1'
spec['summary'][0]='Accept duplicate role intent by normalizing before count validation, membership replacement and audit; previously valid duplicate IDs were rejected with status 400.'
spec['changedFiles']=[x for x in spec['changedFiles'] if not x.startswith('astraupskill/evidence/')]
spec['limits']=[x for x in spec['limits'] if not x.startswith('The nine course')]+['Only role replacement is normalized; user creation is unchanged. Role validation remains outside the transaction; the test checks shared transaction-handle wiring, not real isolation.']
f.write_text(json.dumps(spec,indent=2),encoding='utf-8')
