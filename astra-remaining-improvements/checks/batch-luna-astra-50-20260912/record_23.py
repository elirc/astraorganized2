from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parents[2]; F=Path(__file__).resolve().parent
(F/'4c54d18d7d97-review.md').write_text('''# Astra review: jstrain3.0

Reviewed production cart/order handlers, lazy connection and app factories, checkout service, validator, all six SQLite test cases and nine guides. Six tests and client production build passed. Root corrected ownership-query wording, transaction ownership, preflight versus rollback examples, total-overflow coverage and portable verification. Included the complete executable fixture. Mechanical preflight verified seven executable hashes, eight exact snapshots and 23 local links; 43 files delivered with 6,027 course words including the complete fixture.

Actual rollback evidence aborts the second order line after the first stock decrement. It is not a concurrent-writer or forced zero-row predicate test. Identity is injected and handlers are invoked directly; no listener/JWT/payment test. REAL dollars, demo auth and absence of durable idempotency/logging remain explicit limits. Canonical apply verified original hashes.
''',encoding='utf-8')
(F/'2d739127d551-review.md').write_text('''# Astra review: jdtrrain2.1

Reviewed actual PATCH, move, bulk-sprint and API wrapper code, activity helper, input parsers, all eleven cases and all nine guides. Root added Prisma Int bounds, strict move/issue IDs and four route cases covering positive moves, changed-only bulk writes, missing/foreign PATCH relations and same-sized foreign populations. Test VM receives the host Date constructor. Lint required renaming two test-loader locals; the final eleven-test rerun and fresh lint passed. Application production build passed before that test-only rename.

Replaced inaccurate earlier teaching material with the actual Next/Prisma flow, matched trace answers, portable pnpm commands, exact evidence and a complete route fixture. Mechanical preflight checked nine executable hashes, six original snapshots and 38 local links. Delivered 46 files with 5,833 course words including the complete fixture. Prisma and identity are mocked: database rollback, isolation, sessions and browser behavior are not proven. Move activity remains outside its transaction; POST and demo-identity gaps and last-write-wins edits are explicit limits. Canonical apply verified original hashes.
''',encoding='utf-8')
selection=json.loads((F/'selection.json').read_text(encoding='utf-8')); progress=json.loads((B/'progress.json').read_text(encoding='utf-8')); byid={p['id']:p for p in progress['projects']}; pending=[p for p in selection['projects'] if byid[p['id']]['status']!='complete']
(F/'REMAINING_QUEUE.md').write_text('# Remaining next-50 queue\n\nOnly canonical deliveries count. Fresh Luna assignments own one named project; Astra reviews and applies.\n\n'+'\n'.join('- '+p['id']+' — '+p['path'] for p in pending)+'\n',encoding='utf-8')
state={'root':'Astra plans, independently reviews, validates and applies; maintains reports','batchDelivered':50-len(pending),'overallDelivered':sum(p['status']=='complete' for p in progress['projects']),'luna_course_finish':'Master6 3e4e08e349a1 implementation; jdtrrain frozen and delivered','luna_checkout_finish':'appmakertrack b7429e8bf71d implementation; jstrain3.0 frozen and delivered','luna_ramp':'Ramp a0a0ff059e64 implementation','rootSetupHandles':{'e13':96074,'z1':74993,'appmakertrack':60463},'retired':'All older queue workers must not resume or edit delivered projects.'}
(F/'active-work.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
for script in ['render_progress_report.py','render_new_project_report.py','render_completion_summary.py','render_finished_summary.py','render_next50_report.py','checks/batch-luna-astra-20260912/render_batch_report.py']:
 cmd=[sys.executable,'-X','utf8',str(B/script)]
 if script.endswith('render_batch_report.py'):cmd.append('2')
 subprocess.run(cmd,check=True)
