"""Put Luna's reviewed draft into the common learner course layout."""
from pathlib import Path
import json
import hashlib
import shutil

B=Path(__file__).resolve().parent
pid='a1d53294d3b0'
stage=B/'stage'/pid
draft=stage/'docs/code-walkthroughs/audit-log-scope'
course=stage/'astraupskill'
course.mkdir(exist_ok=True)
mapping={'01-map.md':'01-CODEBASE-MAP.md','02-scope.md':'02-CONCEPTS.md','03-change.md':'03-WORKED-CHANGE.md','04-fixture.md':'04-TESTING-AND-DEBUGGING.md','05-practice.md':'05-PRACTICE.md','06-solutions.md':'06-SOLUTIONS-AND-REVIEW.md','07-trace.md':'07-TRACE-LAB.md'}
for old,new in mapping.items():
    target=course/new
    assert not target.exists(), 'Do not overwrite later review repairs'
    target.write_text((draft/old).read_text(encoding='utf-8'),encoding='utf-8')
snapshots=course/'snapshots'
snapshots.mkdir(exist_ok=True)
baseline=json.loads((B/'baselines'/(pid+'.json')).read_text(encoding='utf-8'))['files']
snapshot_files=[]
for original,saved,name in [
    ('apps/api/src/services.ts','original-services.ts','services-before.ts.txt'),
    ('apps/api/src/store.ts','original-store.ts','store-before.ts.txt'),
    ('apps/api/src/api.test.ts','original-api.test.ts','api-tests-before.ts.txt'),
    ('docs/features/07-audit-log-viewer.md','original-07-audit-log-viewer.md','audit-feature-before.md.txt')]:
    source=B/'checks'/pid/'snapshots'/saved
    assert hashlib.sha256(source.read_bytes()).hexdigest()==baseline[original],original
    target=snapshots/name
    shutil.copyfile(source,target)
    snapshot_files.append(target.relative_to(stage).as_posix())
(course/'README.md').write_text('''# Master7: protect audit data in every response

Start with a small but important CRUD application question: when an organization administrator opens a dashboard, whose audit records may appear in its JSON? Master7 already restricted its dedicated audit endpoint, but the dashboard assembled a separate response containing the newest global records. This course follows the fix that applies organization scope to that second read path. You will practice tracing authorization through the actual HTTP route, service and in-memory data store.

The application is a learning management system with organizations, courses, enrollments, progress, submissions and certificates. Its root npm workspace contains an Express API, a Vite web client and shared contracts/domain packages. The current running services use the synthetic in-memory store. A Prisma schema is also present, but these dashboard tests do not use a persistent database. Keeping that distinction clear is part of learning to assess a codebase accurately.

Read the chapters in this order:

1. [Codebase map](01-CODEBASE-MAP.md): follow login, actor resolution and the dashboard request to its response projection.
2. [Concepts](02-CONCEPTS.md): distinguish authentication, organization authorization and filtering before a result limit.
3. [Worked change](03-WORKED-CHANGE.md): compare the global slice with the scoped implementation.
4. [Testing and debugging](04-TESTING-AND-DEBUGGING.md): understand the seeded two-organization fixture and actual local HTTP regression.
5. [Practice](05-PRACTICE.md): predict staff, platform administrator and learner responses, including a limit boundary.
6. [Solutions](06-SOLUTIONS-AND-REVIEW.md): check those predictions against complete examples and explain each assertion.
7. [Trace lab](07-TRACE-LAB.md): account for every step from the synthetic actor to the returned audit list.
8. [Verification](VERIFICATION.md): reproduce the nineteen-test run, type check and build, then read their limits.

Use the exact original [service](snapshots/services-before.ts.txt), [store](snapshots/store-before.ts.txt) and [test](snapshots/api-tests-before.ts.txt) snapshots for before/after study. They have a `.txt` suffix so they cannot accidentally become compiled duplicate source. Preserve the existing broader project documentation; this course focuses on one concrete defect rather than claiming to explain every enrollment workflow.

By the end, you should be able to explain why a correct audit endpoint did not protect the separate dashboard projection, write a negative test with another organization's record, and justify filtering before slicing. A good review answer identifies both the protection and its boundary: the local HTTP test checks response ownership, while persistent database isolation and browser behavior need different evidence. Use that habit when moving from junior implementation work toward independent feature reviews.
''',encoding='utf-8')
root_readme=stage/'README.md'
text=root_readme.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text:
    root_readme.write_text(text.rstrip()+'\n\n## CRUD upskilling course\n\nFollow the [dashboard audit-scope course](astraupskill/README.md) for the actual code path, worked repair, HTTP regression, practice and solutions.\n',encoding='utf-8')
feature=stage/'docs/features/07-audit-log-viewer.md'
text=feature.read_text(encoding='utf-8')
text+='\n\n## Dashboard scope follow-up verification\n\nThe dashboard scope improvement passed nineteen tests, TypeScript checking and the full workspace build. See the [current course verification](../../astraupskill/VERIFICATION.md) for commands, raw evidence and the in-memory coverage boundary. The older build-journal `verify` entry above records its own historical work.\n'
feature.write_text(text,encoding='utf-8')
spec_path=B/'specs'/(pid+'.json')
spec=json.loads(spec_path.read_text(encoding='utf-8'))
spec['project']='_Organized Desktop/03 Master Projects/master7'
spec['summary']=[
    'Scope dashboard audit records to the actor organization before taking 25 entries; preserve platform administrator visibility and the learner empty-list contract.',
    'Add synthetic two-organization audit fixtures and a real local HTTP regression covering staff, platform administrators and learners; nineteen tests, type checking and the workspace build pass.',
    'Add a source-linked CRUD course with exact original snapshots, worked examples, practice solutions and recorded verification evidence.'
]
spec['changedFiles']=[f for f in spec['changedFiles'] if not f.startswith('docs/code-walkthroughs/audit-log-scope/')]+['README.md']+snapshot_files
spec.pop('evidence',None)
spec_path.write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'id':pid,'copiedChapters':len(mapping),'exactSnapshots':len(snapshot_files)}))
