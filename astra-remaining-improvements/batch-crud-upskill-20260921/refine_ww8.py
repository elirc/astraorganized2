from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/4d914b7440f4'
p=P/'tests/runtime-job-claim-contract.test.mjs';t=p.read_text();a=t.index('const calls =');b=t.index('const mod =',a);t=t[:a]+t[b:]
t=t.replace("  const result = await mod.markJobRunning(db, 'job-1');", "  const calls=[]; const db={extractionJob:{updateMany:async args=>{calls.push(args);return {count:1};}}};\n  const result = await mod.markJobRunning(db, 'job-1');")
t=t.replace("  db.extractionJob.updateMany = async (args) => { calls.push(args); return { count: 0 }; };", "  const calls=[]; const db={extractionJob:{updateMany:async args=>{calls.push(args);return {count:0};}}};")
t=t.replace('calls[1]','calls[0]')
t+='''
test('database error propagates without fabricating a successful claim',async()=>{
 const error=new Error('claim unavailable');let calls=0;
 const db={extractionJob:{updateMany:async()=>{calls++;throw error;}}};
 await assert.rejects(mod.markJobRunning(db,'job-1'),e=>e===error);assert.equal(calls,1);
});
''';p.write_text(t)
s=B/'specs/4d914b7440f4.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['summary'][0]='Verify actual extraction-job claim predicate, attempt increment, result forwarding and database error propagation without claiming a concurrent worker execution.';s.write_text(json.dumps(d,indent=2))
for p in (P/'astraupskill').glob('*.md'):
 t=p.read_text().replace("'''",'').replace(".''",'.').replace('evidence/4d914b7440f4-runtime-job-claim-contract.tap.txt','evidence/crud-b07-astra-runtime.log').replace('2 tests passed','3 tests passed').replace('two-case contract','three-case contract').replace('two branches execute','three cases execute')
 t=t.replace('zero means another worker claimed the job','zero means the queued predicate no longer matches (for example, another worker claimed or deleted the job)')
 t=t.replace('It proves the positive claim fields and the refusal signal.','It proves positive claim arguments, zero-count forwarding and database error propagation.')
 t=t.replace('returns a zero-count refusal for competing workers','forwards a supplied zero-count result')
 if p.name=='VERIFICATION.md':t+='\nThe third case injects a database error and checks exact error identity with one attempted call. All fixtures are independent. Count0 is returned by the adapter, not produced by an actual race; only a database-backed test could demonstrate that runtime outcome under competing workers.\n'
 p.write_text(t,encoding='utf-8')
