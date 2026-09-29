from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/5bbaa8521f2b'
(P/'tests/knowledge-entry-service-runtime.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const plain=x=>JSON.parse(JSON.stringify(x));
async function setup({status='DRAFT', authorId='editor', missing=false, failAudit=false}={}) {
 const calls=[], tx={token:'transaction'};
 const entry={id:'entry',status,authorId,slug:'retries'};
 const repo={findEditableEntryById:async (...args)=>{calls.push(['find',...args]);return missing?null:entry;},
 searchPublishedEntries:async input=>{calls.push(['search',plain(input)]);return [];},
 updateKnowledgeEntryStatus:async (client,id,next)=>{assert.equal(client,tx);calls.push(['write',id,next]);return {...entry,status:next};},
 mapWorkspaceEntry:e=>e};
 for(const name of ['createKnowledgeEntry','findEntryBySlug','findPublishedEntryBySlug','findWorkspaceEntryById','listWorkspaceEntries','updateKnowledgeEntry','updateKnowledgeEntryCuration'])repo[name]=()=>{throw Error('unexpected '+name);};
 const mod=await loadTypeScript('src/services/knowledgeEntryService.ts',{root,stubs:{
 '@prisma/client':{EntryStatus:{DRAFT:'DRAFT',PUBLISHED:'PUBLISHED',ARCHIVED:'ARCHIVED'}},
 '@/lib/db':{db:{$transaction:async fn=>{calls.push(['tx']);return fn(tx);}}},
 '@/repositories/knowledgeEntryRepository':repo,
 '@/repositories/auditLogRepository':{createAuditLog:async(client,input)=>{assert.equal(client,tx);calls.push(['audit',plain(input)]);if(failAudit)throw Error('audit failed');}},
 '@/repositories/tagRepository':{upsertTagsByNames:()=>{throw Error('unexpected tags');}}
 }});
 return {mod,calls};
}
const editor={id:'editor',role:'EDITOR'};
test('search forwards every filter and pagination field',async()=>{
 const {mod,calls}=await setup();await mod.searchKnowledgeBase({q:'retry',tags:['node'],featuredOnly:true,page:2,pageSize:10});
 assert.deepEqual(calls,[['search',{query:'retry',tagSlugs:['node'],featuredOnly:true,page:2,pageSize:10}]]);
});
test('owned draft publishes with one transaction client and exact audit metadata',async()=>{
 const {mod,calls}=await setup();const result=await mod.changeEntryStatus(editor,'entry','PUBLISHED');
 assert.equal(result.status,'PUBLISHED');assert.deepEqual(calls,[['find','editor','EDITOR','entry'],['tx'],['write','entry','PUBLISHED'],['audit',{action:'knowledgeEntry.statusChanged',targetType:'knowledgeEntry',targetId:'entry',entryId:'entry',actorId:'editor',metadata:{previousStatus:'DRAFT',nextStatus:'PUBLISHED'}}]]);
});
test('real ownership and roles deny foreign editor and viewer before transaction',async()=>{
 for(const actor of [{id:'foreign',role:'EDITOR'},{id:'editor',role:'VIEWER'}]){
  const {mod,calls}=await setup();await assert.rejects(mod.changeEntryStatus(actor,'entry','PUBLISHED'),e=>e.statusCode===403&&e.code==='FORBIDDEN');assert.deepEqual(calls.map(c=>c[0]),['find']);
 }
});
test('restore requires admin; published to draft is invalid even for admin; missing is404',async()=>{
 let h=await setup({status:'ARCHIVED'});await assert.rejects(h.mod.changeEntryStatus(editor,'entry','DRAFT'),e=>e.statusCode===403);assert.equal(h.calls.length,1);
 h=await setup({status:'ARCHIVED'});assert.equal((await h.mod.changeEntryStatus({id:'admin',role:'ADMIN'},'entry','DRAFT')).status,'DRAFT');
 h=await setup({status:'PUBLISHED'});await assert.rejects(h.mod.changeEntryStatus({id:'admin',role:'ADMIN'},'entry','DRAFT'),e=>e.statusCode===409&&e.code==='CONFLICT');assert.equal(h.calls.length,1);
 h=await setup({missing:true});await assert.rejects(h.mod.changeEntryStatus(editor,'entry','PUBLISHED'),e=>e.statusCode===404&&e.code==='NOT_FOUND');assert.equal(h.calls.length,1);
});
test('same-status request is accepted and still writes and audits',async()=>{
 const {mod,calls}=await setup();await mod.changeEntryStatus(editor,'entry','DRAFT');assert.deepEqual(calls.map(c=>c[0]),['find','tx','write','audit']);assert.equal(calls[3][1].metadata.previousStatus,calls[3][1].metadata.nextStatus);
});
test('audit failure propagates after adapter write; this harness cannot prove rollback',async()=>{
 const {mod,calls}=await setup({failAudit:true});await assert.rejects(mod.changeEntryStatus(editor,'entry','PUBLISHED'),/audit failed/);assert.deepEqual(calls.map(c=>c[0]),['find','tx','write','audit']);
});
''',encoding='utf-8')
docs={
'README.md':'''# Knowledge publishing workshop

Use [knowledgeEntryService](../src/services/knowledgeEntryService.ts) and its real permission helpers to study CRUD lifecycle rules. The [six-case runtime lab](../tests/knowledge-entry-service-runtime.test.mjs) runs without installing the application. Production source is unchanged: the improvement is an executable workshop with explicit evidence.

Begin by predicting which editor may publish a draft. Then compare ordinary publishing with restoring archived content, and inspect what happens when the requested status is already current. Practice uses a decision table, call tracing, failure injection and a review exercise. Separate service behavior from database guarantees: repository adapters record writes, while the transaction adapter does not emulate rollback, isolation or concurrent readers.''',
'01-CODEBASE-MAP.md':'''# Map the publishing path

changeEntryStatus loads through findEditableEntryById using actor id, role and entry id. Missing data becomes NotFoundError. isValidStatusTransition runs next; canTransitionEntry then applies ownership and role requirements. Only after both checks does db.$transaction receive its callback.

Inside that callback, updateKnowledgeEntryStatus and createAuditLog receive the same transaction object. Audit metadata records previousStatus and nextStatus, and mapWorkspaceEntry prepares the return value. Follow src/lib/auth/permissions.ts to see the actual matrix and src/lib/errors.ts for statusCode and code. The runtime imports both files. Search is a separate mapping path: q becomes query, tags becomes tagSlugs, and pagination and featuredOnly pass through to searchPublishedEntries.''',
'02-CONCEPTS.md':'''# Ownership, lifecycle and repeat requests

An EDITOR can edit their own entry; ADMIN can edit any entry. That rule alone is insufficient to restore content: ARCHIVED to DRAFT additionally requires ADMIN. PUBLISHED to DRAFT is not in the transition matrix, even for ADMIN. Explain why role privilege and valid state transitions are separate checks.

The real matrix accepts equal states. Consequently an owned DRAFT to DRAFT request still enters the transaction, writes and audits. Equal-state acceptance is not a no-op contract here. Before changing this behavior, discuss whether callers expect repeated audit records. The current pre-read occurs before the transaction callback, so transaction membership alone does not establish protection against stale state.''',
'03-WORKED-CHANGE.md':'''# Trace an owned draft publication

The fixture starts with entry id entry, author editor and status DRAFT. The actor has id editor and role EDITOR. Predict the successful call sequence before reading the test: find, transaction, write, audit. The write receives entry and PUBLISHED. Audit uses knowledgeEntry.statusChanged and includes DRAFT and PUBLISHED in metadata.

The test checks the complete metadata and object identity of the transaction passed to both writes. Change only the actor id to foreign and predict the new sequence: find, followed by FORBIDDEN403, with no transaction. This paired example teaches authorization before mutation while avoiding a fake permission helper that would silently allow every caller. Production code is preserved for comparison.''',
'04-TESTING-AND-DEBUGGING.md':'''# Debug at the service boundary

Run node --experimental-vm-modules --test tests/knowledge-entry-service-runtime.test.mjs from the project root. The loader evaluates the real TypeScript service, permissions and error classes. Prisma enum values and database-facing repositories are adapters; no server, generated client or database connection is required.

When a refusal test fails, inspect error.statusCode and error.code before altering fixtures. A generic Error is not equivalent to the domain error. When ordering fails, inspect the recorded calls before claiming persistence corruption. The audit-failure case proves rejection after the write adapter was called; the adapter cannot demonstrate rollback. A real database integration test remains necessary to validate atomic persistence and race behavior.''',
'05-PRACTICE.md':'''# Predict, modify, explain

First draw a table for DRAFT, PUBLISHED and ARCHIVED against each destination, then add actor columns for owner EDITOR, foreign EDITOR and ADMIN. Mark where lifecycle validation runs before authorization. Predict the error for an unauthorized caller requesting PUBLISHED to DRAFT.

Next extend the lab with ARCHIVED to ARCHIVED for the owning editor. Decide whether the current helper permits it and whether an audit should still occur. Do not read the answer chapter until you have written the expected sequence.

Finally propose a database-backed stale-update experiment using two callers. Describe the synchronization point and expected persisted audit records. Keep this proposal separate from the existing adapter tests, which cannot establish concurrent commit behavior.''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Compare the reasoning

PUBLISHED to DRAFT yields CONFLICT409 before the authorization helper runs. ARCHIVED to ARCHIVED is allowed for the owning EDITOR because equal statuses are valid and the admin-only condition applies specifically to ARCHIVED to DRAFT. The service still writes and audits that equal-status request.

A sound review notices that both persistence calls share a transaction client, but the entry read precedes the transaction. To investigate stale writes, pause two real requests after their initial reads and inspect the final row and audit records after both finish. Consider conditional updates or isolation only after defining the desired contract. Do not label the current runtime evidence a database concurrency test or a rollback proof.''',
'07-TRACE-LAB.md':'''# Inject a late failure

Enable failAudit in the fixture and request DRAFT to PUBLISHED as the owner. Stop at each recorded operation. The service first reads, then enters the transaction adapter, then invokes the status write, then invokes audit. The audit adapter throws audit failed, and the service promise rejects.

Write two separate observations: the write adapter was invoked, and the caller received an error. Neither observation says whether a real database transaction committed. The fake transaction simply calls its callback. For a follow-up integration exercise, seed a draft in a test database, force audit persistence failure, and query both tables after rejection. That experiment would address rollback without changing what this portable trace claims.''',
'VERIFICATION.md':'''# Verification scope

Six runtime cases cover search mapping, owned publication, role and ownership refusals, restore and invalid-state boundaries, missing records, equal-status writes and audit failure propagation. Real permissions and AppError subclasses execute alongside the service. Repository and transaction adapters provide deterministic observations, not a database simulation.

The source snapshot preserves the service inspected for this lesson; production source has no functional change. Full Next routing, authentication, repository SQL, database rollback and concurrent isolation are outside this run. The saved terminal evidence identifies the command and assertion count. Read the tests to distinguish runtime assertions from proposed integration exercises before using this material in a review or claiming end-to-end coverage.'''
}
for name,content in docs.items(): (P/'astraupskill'/name).write_text(content+'\n',encoding='utf-8')
s=B/'specs/5bbaa8521f2b.json';spec=json.loads(s.read_text(encoding='utf-8-sig'))
spec['changedFiles']=[p for p in spec['changedFiles'] if not p.startswith('astraupskill/evidence/')]
spec['summary']=['Add six actual-service runtime cases using real knowledge publishing permissions and domain errors.','Add source-grounded decision tables, call tracing, failure injection and review exercises.']
spec['limits']=['Database repositories and transaction are adapters; no Next authentication, SQL filtering, rollback or isolation execution.','Production source unchanged. Equal-status writes and audit behavior documented, not changed.']
s.write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
