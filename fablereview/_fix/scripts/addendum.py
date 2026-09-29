import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fable_edit as fe

HERE = fe.HERE

DATA = {
 'buildantigvg': [('04', 'root `package.json` test scripts (`test:api`/`test:web`/`test:e2e`)'),
                  ('07', '`apps/api/src/workers.ts:233-246` (WorkersController routes)')],
 'jstrain2-3': [('04', '`scripts/test.mjs` (whole file)'), ('07', '`src/lib/workspaceApi.mjs:70-75` (`revision()` If-Match guard)')],
 'd1': [('04', '`package.json` `scripts.test` (node --import tsx --test ...)'), ('07', '`src/lib/socket/actions.ts:249-272` (`card:update` handler)')],
 'grokbuildecommerceproject': [('04', 'root `package.json` test scripts'), ('07', '`backend/src/repositories/orderRepository.ts:85-102` (checkout advisory lock + receipt lookup)')],
 'buildsmallplates': [('04', '`package.json` (`vitest run`, `tsc --noEmit`)'), ('07', '`src/db/repos.ts:433-467` (`updateSet`)')],
 'react': [('03', '`store.js:48-62` (`BoardStore.save`)'), ('04', '`package.json` test/test:browser/verify'),
           ('06', '`test/store.test.js:106-119` (concurrent-save case)'), ('07', '`main.js:65-69` (storage event listener)')],
 'buildsubbox': [('03', '`src/model.js:381-394` (`quoteBox` input contract)'), ('06', '`src/repository.js:11-24` (`commit`)'),
                 ('07', '`test/model.test.mjs:250-263` (replay / changed-cycle cases)')],
 'e12': [('06', '`src/server/contracts.js:186-194` (`validateStrategySettings`)'), ('07', '`src/server/services.js:837-853` (`createFlag` guards)')],
 'e13': [('03', '`src/lib/commerce/orders.ts:261-277` (pre-transaction guards)'), ('04', '`vitest.config.ts` (astraupskill exclude)'),
         ('06', '`src/lib/commerce/commerce.test.ts:277-297` (duplicate-line snapshot case)'), ('07', '`src/lib/commerce/orders.ts:556-571` (refund replay boundary)')],
 'j1': [('03', '`src/todo/service/TaskManager.java:39-51` (expected/replace/editTask)'), ('04', '`scripts/verify.py` invocation + `TODO_VERIFY_RESULTS_DIR`'),
        ('06', '`test/todo/TaskWorkflowTest.java:64` (atomic-replacement failure case)'), ('07', '`src/todo/repository/TaskRepository.java:39-51` (`save`)')],
 'aiheartbeat': [('07', '`packages/dashboard/lib/workspace-store.ts:66-76` (`saveWorkspaceItem`)')],
 'netvg': [('07', '`src/PeblClone.Application/Workforce/HiringQuoteCalculator.cs:17-38` (shape gates)')],
 'geminiorganized-opensource-upskilling-ramp': [('07', '`backend/Services/ExpenseService.cs:187-201` (`StartReimbursement`)')],
 'buildgum': [('06', '`src/repository.ts:41-65` (`restore`)'), ('07', '`src/repository.ts:26-39` (`commit` with replay)')],
 'master7': [('03', '`apps/api/src/services.ts:28-35` (`auditLogScope`/`visibleAuditLogs`)'), ('04', 'root `package.json` (`test`, `verify`)'),
             ('06', '`apps/api/src/audit-scope.test.ts:31-42`'), ('07', '`apps/api/src/services.ts:134-145` (`auditLogs` endpoint)')],
 'nettrello': [('07', '`src/NetTrello.Api/Contracts/BoardDtos.cs:63-78` (`ResolveAgainst`)')],
 'jsprojectlearn': [('03', '`src/game/notes.ts:14-28` (`updateNote`)'), ('04', '`package.json` test/build/test:browser commands'),
                    ('06', '`src/game/storage.test.ts:136-157` (reset identity case)'), ('07', '`src/game/storage.ts:20-36` (`persistProgress`)')],
 'geminiorganized-opensource-upskilling-stripe': [('07', '`tests/Billing.Tests/HttpTests.cs:106-115` (`ExactHttpRetryReturnsSameBodyAndEtag`)')],
 'astra4-2': [('04', '`package.json` scripts + documented grep-invert browser run'), ('06', '`extension/model.js:67-76` (`applyMessage` preset branch)'),
              ('07', '`src/app.js:128-135` (`saveSettings`)')],
 'appmakertrack': [('07', '`lib/time-entry-service.ts:4-15` (`stopRunningEntry`)')],
 'grokbuildhrproject': [('04', 'root `package.json` test scripts'), ('07', '`backend/src/repositories/leaveRepository.ts:239-251` (`decide` guards)')],
 'andie': [('04', '`scripts/lib/client.js:7-20` (`redact`/`detailed`)'), ('06', '`scripts/lib/planner.js:4-15` (`stable`/`canonical`/`hash`)'),
           ('07', '`scripts/lib/planner.js:156-171` (`buildPlan`)')],
 'j3': [('04', '`test/bankapp/RegressionTests.java:50-57` (competing withdrawals)')],
 'b1': [('03', '`src/lib/platform.ts:671-680` (parent/child projections)'), ('04', '`checks/incident-detail-regression.mjs`, `checks/incident-list-pagination.mjs` run commands'),
        ('07', '`src/lib/platform.ts:652-665` (`getIncidentDetail` head)')],
 'aiapplybot': [('04', '`tests/test_store.py:57-71` (concurrent writers)'), ('06', '`applybot/application_store.py:217-241` (`update`)'),
                ('07', '`applybot/application_store.py:217-225` (version comparison)')],
 'job-track-restaurant-kitchen-display-system': [('03', '`server/src/lib/validation.js:22-26` (`listOrdersSchema`)'),
                                                 ('06', '`server/test/kds.test.cjs:92-107` (global 86 case)')],
 'grokbuildorderproject': [('04', 'root `package.json` test scripts')],
 'missioncontrol': [('04', '`README.md` documented `dotnet test`'), ('07', '`src/FleetCommand.Host/Services/TaskService.cs:87-113` (`UpdateAsync`)')],
}

CH = {'03': '03-WORKED-CHANGE.md', '04': '04-TESTING-AND-DEBUGGING.md', '06': '06-SOLUTIONS-AND-REVIEW.md', '07': '07-TRACE-LAB.md'}

for slug, entries in DATA.items():
    p = os.path.join(HERE, 'reports', slug + '.md')
    if not os.path.exists(p):
        print('MISSING REPORT', slug)
        continue
    text = io.open(p, encoding='utf-8').read()
    if '## Phase 3 addendum (code blocks)' in text:
        print('ALREADY', slug)
        continue
    lines = ['', '## Phase 3 addendum (code blocks)', '',
             'Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:', '']
    for ch, src in entries:
        lines.append(f'- `{CH[ch]}` — quoted from {src}')
    lines.append('')
    with io.open(p, 'a', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    print('APPENDED', slug)
