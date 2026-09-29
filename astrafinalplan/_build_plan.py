"""Generate a five-stage proposal from the reviewed local inventory; never edit source projects."""
import collections
import hashlib
import json
import pathlib
import re
from urllib.parse import quote, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'astrafinalplan'
DESKTOP = ROOT.parent
REVIEW = ROOT / 'astradocs/project-review.json'
TUTORIALS = ROOT / 'astradocs/project-tutorials.json'
review = json.loads(REVIEW.read_text(encoding='utf-8-sig'))
tutorials = json.loads(TUTORIALS.read_text(encoding='utf-8-sig'))
records = review['projects'] + review['nested_apps']
guides = {p['path']: p for p in tutorials['projects'] + tutorials['nested_app_guides']}
SECTIONS = {
 1: ('01-foundations-and-learning-content.md', 'Foundations and learning content', 'Use one fundamentals course and apply it to one small program. Reference collections support the active project; they are not extra courses to finish.', 'Explain an unfamiliar function, implement a small change without the solution, and diagnose one failing example.'),
 2: ('02-client-apps-and-apis.md', 'Client apps, APIs and persistence', 'Finish one client app, then one API-backed workflow. Keep the current stack; choose TypeScript/React/Node for the main route and defer the C# branch until after a capstone.', 'Demonstrate a usable workflow, invalid input, loading/error states where applicable, and persistence across restart.'),
 3: ('03-full-stack-workflows.md', 'Full-stack workflows and a capstone', 'Select one primary app with a useful domain. Own a complete workflow across interface, server and data, including permissions. Similar projects are alternatives.', 'Reproduce setup from a clean checkout, demonstrate an authorized workflow and a denied action, and explain the code and data changes independently.'),
 4: ('04-domain-rules-and-reliability.md', 'Domain rules and reliability', 'Harden the capstone before starting another app. Select one focused project only when it teaches a missing invariant, transaction or recovery behavior.', 'Show a domain rule holding through an invalid request and a relevant retry, concurrency or restart scenario; explain the failure and recovery path.'),
 5: ('05-architecture-and-specializations.md', 'Architecture and specializations', 'Choose one advanced branch after reliable full-stack delivery. Large upstream repositories are bounded reading/contribution exercises; AI, realtime, games and mobile are optional specializations.', 'Deliver one bounded architectural or specialist improvement, with a reproducible failure scenario, justified tradeoff, and relevant regression or evaluation evidence.'),
}

def section(p):
    return {0:1, 1:1, 2:2, 3:2, 4:3, 5:4, 6:5, 7:5}[p['phase']]

def link(path, label=None):
    target = DESKTOP / path
    return f'[{label or pathlib.PurePosixPath(path).name}]({quote(target.as_posix(), safe="/:")})'

def flat_stack(p):
    stack = p.get('stack', {})
    vals = [x for a in stack.values() for x in a] if isinstance(stack, dict) else stack
    return list(dict.fromkeys(vals))

def is_resource(p):
    return p['phase'] == 0 or p.get('record_kind') == 'learning-or-reference-collection'

def is_reference(p):
    text = (p.get('curriculum_role','') + ' ' + p['assessment']).lower()
    return not is_resource(p) and ('upstream' in text or p.get('curriculum_role','').lower() == 'reference' or 'starter/reference' in p['purpose'].lower() or 'reading established code' in p.get('learning','').lower())

# Each override is a proposed, bounded improvement, not a newly verified defect.
OVERRIDES = {
 'borrowbox': ('Connect one borrowing-rule lesson to the API, domain checks and repository; explain X-Demo-Role and the optional SQLite adapter honestly.', 'Add or strengthen a rule preventing the same equipment from being actively loaned twice. After that rule works, implement the SQLite adapter as a separate persistence milestone.', 'The first loan succeeds and a conflicting second loan fails without changing availability incorrectly. For the adapter milestone, restart the process and verify the loan remains recorded.'),
 'campusops': ('Turn one facilities request into a UI-to-domain-to-repository lesson; distinguish client-supplied demo campus/role headers from verified identity.', 'Complete one facilities request approval flow with a persistent repository. Treat real session-based campus membership as a separate access-control milestone.', 'A valid approval is retained after restart and an invalid transition is rejected. For the identity milestone, prove a client cannot gain another campus by changing a header.'),
 'gitjira-app': ('Extend ARCHITECTURE.md with one issue-transition reading route and a guided exercise followed by an independent variation; link the relevant sprint material from gitjira.', 'Make one issue transition preserve project membership and reject stale writes, using the existing model and version mechanism where present.', 'A project member completes the transition, a nonmember is denied, and two stale competing updates cannot silently overwrite each other; the interface explains the rejected change.'),

 'astra4.2': ('Map timer states and extension events; document source-to-bundle steps and asset fallback behavior.', 'Supply a fallback for missing artwork, add focus/pause/break state tests, and produce the referenced extension bundle from source.', 'Simulate pause/resume and a delayed alarm; confirm no skipped/double break and confirm the packaged extension resolves every referenced asset.'),
 'jobtrack': ('Extend the Daybook cartography with import/export schema, storage ownership and migration examples.', 'Make one import atomic and validate its schema; preserve the current local-first design.', 'Export, clear a disposable profile, and import to recover equivalent records; malformed input must leave existing data intact.'),
 'recipeweb': ('Connect onboarding to shopping-list state, persistence and keyboard interactions; keep the proposed .NET extension labeled as future work.', 'Complete one shopping-list operation with persisted quantities and accessible controls.', 'Reload after changing a quantity; verify it survives and that the same operation works with keyboard input.'),
 'recipeview': ('Diagram Dish → Recipe → Cook Log and the SQLite/photo/search write boundaries.', 'Make one recipe-and-log update atomic and repair or explicitly handle search-index update failure.', 'Force a write failure; verify no half-created log, then verify search returns the committed recipe.'),
 'JSProjectLearn': ('Add a diagnostic and skill-to-mission index to the 334-mission campaign; distinguish current missions from archived exercises.', 'Improve saved-progress integrity and recovery around one mission-unlock transition.', 'Replay completion twice and reload; progress and unlock state must agree without skipping prerequisites.'),
 'grokjs': ('Add prerequisite tags and attempt-before-solution checkpoints to the 200-problem Fable Learning Lab.', 'Make one selected exercise independently runnable with deterministic inputs and clearly separated starter/solution files.', 'Solve a changed-input variant without opening its answer; verify the solution and starter remain distinguishable.'),
 'netnotion': ('Use populated docs/fable as the start; label empty docs/upskill scaffolding and teach page permissions and revision history.', 'Protect a page move/restore operation against inherited-permission bypass and recursive tree cycles.', 'Reject a cycle and a forbidden inherited share; restore content while retaining a coherent revision history.'),
 'netcleanarch': ('Add a side-by-side trace of one endpoint in this starter and the learner’s simpler finished app.', 'Make one small handler change in a learning branch and record whether the architectural abstraction actually helps.', 'Existing relevant tests and one changed-behavior test pass; explain the extra boundary without copying it into unrelated projects.'),
 'spacegamev2': ('Separate existing-build fabledocs from fabledocs2 rebuild specifications and fabledocs3 product onboarding; link each to its actual scope.', 'Choose a baseline against spacegame, then protect one server-side game command against replay.', 'Deliver the same command twice and restart its worker; resources and completion effects must apply once.'),
 'newcodexJS': ('Create a 20-app capability matrix: implemented source, teaching goals, known stubs and FABLE entrypoint.', 'Standardize one selected child’s reproducible setup and fixtures; extend only that child’s actual workflow.', 'The matrix distinguishes generic CRUD from real domain behavior, and the chosen child passes its own completion criterion below.'),
 'newcodex3': ('Index 25 topics and both language variants; explicitly distinguish in-memory C# samples from persistence plans.', 'Choose one TypeScript child first; implement one missing domain rule before comparing its C# counterpart.', 'Demonstrate the chosen child independently; describe the implementations’ actual differences using code and behavior evidence.'),
 'newcodecjs2': ('Add a five-app skill map and identify each simulated integration and intended invariant.', 'Select one of Planr, Bookr, Payr, Blockr or Helpkit and implement its smallest missing end-to-end slice.', 'Meet the selected child’s criterion below and record which integrations remain simulated.'),
 '_Organized Desktop/04 JavaScript Training/jstrain3': ('Replace generic root orientation with a comparison of deskpilot, deskpilot-app and deskpilot-clean; label fixed seeded identity.', 'Choose one implemented variant and complete one flow there; replace demo identity only when introducing real user isolation.', 'Setup instructions open the chosen app rather than the default starter; its chosen flow works and identity limitations are explicit.'),
 '_Organized Desktop/04 JavaScript Training/jstrain5': ('Connect the nine-chapter OpsForge Fable course to a concrete runbook trace and reconcile older per-file learning notes.', 'Improve one runbook execution transition and make a failed step visible and recoverable.', 'A failed runbook step records its outcome; a retry follows the documented state transition without repeating completed side effects.'),
 '_Organized Desktop/02 Build Projects/buildjira': ('Separate the archived JavaScript predecessor from the current C#/React flow and explain demo actor impersonation.', 'Complete one issue transition and replace demo actor selection with a verified session when adding shared-user operation.', 'A nonmember cannot mutate the issue; the valid transition updates the interface and stored issue consistently.'),
 '_Organized Desktop/02 Build Projects/buildagentteachGEM': ('Reconcile baseline gotchas with 04-what-changed.md; add an enrollment-to-certification trace against the selected revision.', 'Enforce one certification eligibility rule at the domain boundary and show the rejection in the UI.', 'An ineligible learner cannot receive a certification through direct API use; the eligible case records completion once.'),
 '_Organized Desktop/02 Build Projects/buildagentteaching': ('Extend the codebase reading guide with a concrete enrollment-to-certification exercise and transaction map.', 'Enforce one certification eligibility rule across the application and persistence boundary.', 'An ineligible learner is rejected; a valid completion and its recorded certification remain consistent after retry.'),
}

# Rules use purpose/learning/action evidence, never a folder name alone.
DOMAINS = [
 (r'proxy endpoint|http proxying|metadata.fetch|response limits', 'outbound target validation, timeouts and response limits', 'Use a controlled HTTP stub to verify one allowed request, a forbidden target, a redirect to a forbidden target, a timeout and an oversized response; rejected requests must not reach protected destinations.'),
 (r'approved batch|bulk import|rollback scope|staging, mapping', 'staging, approval and atomic batch commits', 'Stage valid and invalid rows, reject commit before approval, then commit the approved batch twice; rollback must preserve unrelated records.'),
 (r'incident timeline|observability|structured event|recovery drill', 'event correlation, incident transitions and recovery evidence', 'Emit a controlled failure, find its correlated event and reconstruct the incident timeline; demonstrate the recovery action and record the changed observable state.'),
 (r'versioned settings|stale settings|billing/security settings', 'settings versions, privilege boundaries and audit history', 'Reject a stale write and a viewer mutation; a permitted update must produce one coherent configuration revision and audit event.'),

 (r'booking|scheduling|reservation|appointment|interview conflict', 'availability and local-time conversion', 'Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.'),
 (r'payment|billing|invoice|subscription|commission|payout', 'money units, state transitions and duplicate deliveries', 'Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.'),
 (r'inventory|e-commerce|ecommerce|checkout|storefront|marketplace', 'stock ownership, checkout and order transitions', 'Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.'),
 (r'oauth|identity provider|refresh revocation|identity proof', 'identity proof, session lifecycle and trust boundaries', 'Exercise the valid identity path and an expired, revoked or replayed credential; verify denial happens before protected state changes.'),
 (r'game|combat|construction completion|strategy simulation', 'server authority, timer ownership and command ordering', 'Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.'),
 (r'retrieval|\brag\b|mock model|ai-powered|ai agents|coding.agent', 'tool or retrieval boundaries and explicit failure behavior', 'Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.'),
 (r'chat|realtime|real-time|room fanout|message cursors', 'membership, event identity and reconnect behavior', 'Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.'),
 (r'offline|guest.*sync|synchronization|local-first', 'local persistence, replay and conflict resolution', 'Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.'),
 (r'upload|file.sharing|cloud storage|quota|document signing', 'ownership, upload/finalization state and storage boundaries', 'Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.'),
 (r'wiki|page cycle|document.editor|content modeling|recursive blocks|revisions', 'tree structure, revisions and inherited permissions', 'Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.'),
 (r'workflow.automation|retry polic|durable.execution|cursor sync|integrations /|connectors', 'step state, retries and adapter contracts', 'Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.'),
 (r'feature.flag|rollout|targeting|bucketing', 'deterministic targeting and configuration versions', 'Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.'),
 (r'analytics|aggregation|reporting|metric|csv normalization', 'event identity, aggregation and reporting filters', 'Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.'),
 (r'learning.management|enrollment|certification|lesson completion|spaced|scheduler', 'eligibility, progress and completion transitions', 'Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.'),
 (r'hris|workforce|employee|employer.of.record|onboarding|payroll|leave request', 'employee lifecycle, approval and tenant scope', 'Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.'),
 (r'issue|kanban|task|project.management|lead/deal|crm|applicant', 'ownership, ordering and lifecycle transitions', 'Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.'),
 (r'support|ticket|helpdesk|sla|internal notes', 'ticket visibility, assignment and service deadlines', 'Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.'),
 (r'survey|form.builder|dynamic schemas|published schema', 'schema versions and response validation', 'Validate against a published schema; reject foreign, hidden-invalid or outdated inputs without partially saving a response.'),
 (r'blog|publication|headless.cms|content type|cms', 'content validation, publication and access boundaries', 'Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.'),
 (r'timer|chrome|browser extension', 'time-driven state and browser lifecycle events', 'Use a controllable clock; pause/resume and reload while verifying persisted state and no repeated completion event.'),
]

def domain(p):
    for text in [p['next_action'], p.get('learning',''), p['purpose']]:
        for pattern, focus, gate in DOMAINS:
            if re.search(pattern,text.lower()): return focus,gate
    return ('the documented workflow and its state boundary', 'Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.')

def disposition(p):
    if is_resource(p): return 'Supporting resource; improve only when using it with an active project.'
    if p['path'].startswith('geminiorganized/'): return 'Alternate copy; compare and choose a working baseline before investing.'
    if p.get('parent_path'): return 'Optional targeted exercise; choose one topic and one language variant.'
    if is_reference(p): return 'Upstream/starter reference; choose a bounded study or contribution task.'
    if p['phase']==7: return 'Optional specialization after the capstone and reliability stage.'
    if p['path'] in PRIMARY: return 'Primary route candidate; complete this milestone before adding an alternative.'
    return 'Alternative project; select for a measured skill gap, not as additional mandatory work.'

PRIMARY = ['_Organized Desktop/04 JavaScript Training/jstrain2.2','JS1','recipeweb','newcodexJS/01-task-manager','newcodexJS/05-recipe-manager','gitjira-app','gitvg/agora','gitvg/relay']

def tasks(p,g):
    focus, gate = domain(p)
    objective = p.get('learning','code navigation and implementation')
    action = p['next_action'].strip()
    override = OVERRIDES.get(p['path'])
    if override: lesson, build, gate = override
    elif is_resource(p):
        lesson = f'Turn the material on {objective} into one active-project exercise: a prediction, an independent attempt, a worked answer and a reflection prompt. Start with: {action}'
        build = 'Improve this resource itself: add an index, intended audience, prerequisite milestone and links to the actual exercise/code evidence. Date historical claims and distinguish advice from observed behavior.'
        gate = 'Complete one linked exercise in the active project, record the result and verify that a reader can find its prompt and evidence from this resource’s index.'
    elif p['phase']==1:
        lesson = f'Add a short diagnostic and a predict → attempt → explain progression for {objective}; reveal solutions only after the attempt. Tie one exercise to an unfamiliar variation.'
        build = f'Improve one runnable exercise or small program, beginning with: {action} Give it deterministic inputs, clear failure feedback and separate starter/solution material.'
        gate = 'Run the selected exercise, solve a changed-input variant without its answer, and explain an intentionally introduced failure. Verify starter files still leave meaningful work for the learner.'
    else:
        level=g['classification']
        if level=='Codebase walkthrough / study pack':
            lesson=f'Extend the existing walkthrough with a source-linked trace of {focus}, an expected-state example and a guided-to-independent change exercise. Tie it to {objective}.'
        elif level=='Structured tutorial / exercises':
            lesson=f'Add a worked → partially guided → independent exercise for {focus}; make learners predict state before running it. Teach {objective} with a separate answer and rubric.'
        elif level=='Developer explanation / brief orientation':
            lesson=f'Expand the orientation into a 30–60 minute walkthrough of {focus}: ordered source files, one input-to-state trace, a diagram and one independent change targeting {objective}.'
        else:
            lesson=f'Create a small codebase guide from implemented source: setup, ordered file map, one trace of {focus}, known stubs and one exercise targeting {objective}. Keep proposed architecture separate.'
        build=f'First scoped project change: {action} Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.'
        if is_reference(p): build += ' Keep the change inside one upstream module or starter example and document its conventions.'
        if p['phase']==2: gate='For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. '+gate+' Use local fixtures if no server exists; a server is a later milestone.'
        elif p['phase']==3: gate+=' If persistence is implemented, verify state across process restart and a failed write.'
    if g.get('placeholder_samples'):
        lesson += ' Label the sampled placeholder chapters; complete only the chapter required by this exercise.'
    if p['path']=='netnotion': lesson += ' Do not treat the empty alternative guide as a completed course.'
    if is_resource(p): finish='Record one demonstrated skill and remove or label unsupported claims; do not invent an application feature for a reference-only folder.'
    else: finish='After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.'
    return {'learning_content':lesson,'project_improvement':build,'acceptance':gate,'finish':finish}

def render(p, g, pid):
    t=tasks(p,g)
    target_section=section(p)
    item={'id':pid,'path':p['path'],'kind':'nested teaching app' if p.get('parent_path') else 'project/workspace/resource','section':target_section,'original_phase':p['phase'],'disposition':disposition(p),'purpose':p['purpose'],'prerequisites':p['prerequisites'],'learning_focus':p.get('learning',''),'assessment':p['assessment'],'guide_classification':g['classification'],'guide_entrypoint':g.get('entrypoint'),'tasks':t}
    lines=[f'<a id="{pid}"></a>',f'### {p["path"]}', '',p['purpose'], '', f'- **Use / order:** {item["disposition"]} Original milestone {p["phase"]}; prerequisites: {p["prerequisites"]}', f'- **Baseline:** {p["assessment"]}']
    stack=flat_stack(p)
    if stack: lines.append('- **Recorded stack:** '+', '.join(stack)+'.')
    if p.get('parent_path'): lines.append('- **Parent workspace:** '+link(p['parent_path'])+'. Parent-level work does not replace this child’s task.')
    lines.append(f'- **Learning content now:** {g["classification"]}. '+('Start at '+link(g['entrypoint'])+'.' if g.get('entrypoint') else 'No populated entrypoint verified in the tutorial review.'))
    lines += [f'- **1 — Improve the upskilling content:** {t["learning_content"]}', f'- **2 — Improve the project/resource:** {t["project_improvement"]}', f'- **3 — Prove completion:** {t["acceptance"]}', f'- **4 — Consolidate:** {t["finish"]}']
    if g.get('notes'): lines.append('- **Documentation caveats:** '+' '.join(g['notes']))
    related=p.get('related_paths',[])
    if related: lines.append('- **Related locations to compare:** '+', '.join(link(x,x) for x in related)+'. Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.')
    if p.get('duplicate_caveat'): lines.append('- **Variant caveat:** '+p['duplicate_caveat'])
    evidence=list(dict.fromkeys(p.get('evidence_files',[])))[:3]
    if evidence: lines.append('- **Source-review evidence:** '+', '.join(link(x) for x in evidence)+'.')
    return item,'\n'.join(lines)+'\n'

plans=[]
for index,p in enumerate(records,1):
    item,body=render(p,guides[p['path']],f'p{index:03}')
    plans.append((p,item,body))

for n,(filename,title,intro,gate) in SECTIONS.items():
    subset=[x for x in plans if x[1]['section']==n]
    roots=sum(not p.get('parent_path') for p,_,_ in subset)
    nested=len(subset)-roots
    lines=[f'# Section {n}: {title}', '', '[Plan index](README.md)', '',intro, '',f'**Stage exit criterion:** {gate}', '',f'**Coverage:** {roots} project/workspace/resource records and {nested} nested teaching apps. Entries are grouped by original milestone and alphabetized within it; alphabetical position is not a mandatory execution order. Use the short route in the index.', '', 'All actions below are proposals based on the September 6–7 static reviews. Reproduce the baseline before claiming a defect or improvement. Existing tests and docs may already cover a proposed case; assess and strengthen them rather than duplicate them.', '', '## Entries', '']
    for p,item,body in sorted(subset,key=lambda x:(x[0]['phase'],x[0]['path'].lower())):
        lines.append(f'- [{p["path"]}](#{item["id"]})')
    lines += ['', '## Per-project improvement plans', '']
    for p,item,body in sorted(subset,key=lambda x:(x[0]['phase'],x[0]['path'].lower())): lines += [body,'---','']
    (OUT/filename).write_text('\n'.join(lines),encoding='utf-8')

by_path={item['path']:item for _,item,_ in plans}
def entry(path):
    item=by_path[path]
    return f'[{path}]({SECTIONS[item["section"]][0]}#{item["id"]})'

intro=['# Astra final improvement plan', '', '[All 50 implemented projects and learning courses](../astrdocs/ALL_50_PROJECTS_REPORT.md), including the next-30 delivery.', '', '[Completed implementations and learning courses for the first ten projects](TEN_PROJECTS_IMPLEMENTED.md).', '', '**Created:** 2026-09-08. **Scope:** 389 Desktop project/workspace/resource records, including all 202 `_Organized Desktop` records, plus 75 individually planned nested teaching apps: **464 entries**.', '', 'The recommendation is to improve a small sequence deeply and use the rest as targeted exercises or references. Every reviewed location has an improvement plan; it is not necessary to finish every location. Copies remain separate because the prior review did not establish full-tree identity.', '', '## Five sections', '', '| Section | Focus | Root records | Nested apps |', '|---|---|---:|---:|']
for n,(filename,title,_,_) in SECTIONS.items():
    subset=[p for p in records if section(p)==n]
    intro.append(f'| [{n}. {title}]({filename}) | Original milestones '+{1:'0–1',2:'2–3',3:'4',4:'5',5:'6–7'}[n]+f' | {sum(not p.get("parent_path") for p in subset)} | {sum(bool(p.get("parent_path")) for p in subset)} |')
intro += ['', '## Suggested execution order', '', 'This is a milestone sequence, not a calendar commitment. Keep one main project and at most one short reinforcement exercise active. Move on when you meet the stage criterion; skip a fundamentals milestone you can already demonstrate.', '',
 '1. **Foundations:** use '+entry('_Organized Desktop/04 JavaScript Training/jstrain2.2')+' as the main course; use '+entry('JS1')+' for a small independent browser exercise. Improve the diagnostic, attempt/solution separation and feedback. JSProjectLearn and other courses are alternatives, not parallel homework.',
 '2. **Client, API and SQL:** improve '+entry('recipeweb')+' with a persisted, keyboard-usable shopping-list flow; '+entry('jobtrack')+' is an alternative for local-data practice. Then complete '+entry('newcodexJS/01-task-manager')+'. Verify setup and the source behind the FABLE lesson; document where the scaffold differs from the explanation.',
 '3. **Full-stack capstone:** use '+entry('newcodexJS/05-recipe-manager')+' for account ownership and a transaction, then choose '+entry('gitjira-app')+' as the capstone. Own one useful issue workflow from UI to stored state, including authorization and failure feedback. Continue improving it instead of adding another full-stack app.',
 '4. **Reliability:** add a concurrency/retry or transaction case to that capstone. Use '+entry('gitvg/agora')+' only if checkout/stock teaches the missing rule. After the capstone, '+entry('borrowbox')+' followed by '+entry('campusops')+' is an optional C#/.NET branch if it serves your role goals.',
 '5. **Advanced branch:** use '+entry('gitvg/relay')+' for one bounded retry/adapter exercise after the reliability gate. Alternatively choose one advanced reference, AI, mobile or game project after its relevant prerequisites; do not start all branches.',
 '', '## What to improve in the learning content', '',
 'For the chosen project, improve the existing populated Fable/tutorial location first. Use a single linked entrypoint rather than create another competing edition. Add these components only where missing:', '',
 '- **Start here:** audience, prerequisites, measured setup instructions, fixtures and the one supported learning path.',
 '- **Codebase map:** source-linked entrypoints, major boundaries, a request/event/data-flow example and the observed state before and after.',
 '- **Practice:** predict the behavior, run a worked example, complete a guided change, then solve an independent variation; keep answers separate.',
 '- **Failure lab:** one relevant invalid action, interrupted write, retry or concurrency case. Include expected results and debugging clues, not only the happy path.',
 '- **Completion rubric:** explain the changed code, demonstrate behavior, show focused verification and record the tradeoff.',
 '- **Provenance:** reviewed revision/date, actual implementation versus plans/mocks, and a list of outdated or empty chapters. Do not delete intentional exercise TODOs.',
 '', 'For resource-only folders, improve the index, exercises, evidence and relevance to the active project. For large upstream codebases, write one feature trace and a bounded contribution exercise. Neither needs a speculative full rewrite.', '',
 '## How to carry out each project plan', '',
 'Each entry has an evidence baseline, documentation starting point, a content task, a project/resource task and a completion criterion. The existing review’s learning focus and next action supply the project-specific scope; documentation maturity determines whether to extend a course or create a first walkthrough. Acceptance scenarios are proposed engineering exercises, not newly observed failures.', '',
 'Use this order for an activated entry: **reproduce → explain → change → verify → update the lesson**. Record the setup commands and their results in that project when implementation begins. If a proposed behavior already works, improve its explanation or add a missing meaningful regression rather than rebuild it. Keep the current dependency versions initially; investigate any actual setup failure before proposing upgrades.', '',
 'For alternate copies, first compare the relevant manifest, source, docs and working setup. Pick a baseline and record why; preserve distinct exercises and do not infer that a later name or folder suffix means better code. For JS/.NET pairs, complete one implementation, then use the other for a small comparison exercise.', '',
 'Use fake providers and local data for payment, email, AI and external integration lessons. A UI prototype gets honest local behavior and a clear future API contract before production architecture. Backend-only projects do not need a frontend merely to satisfy a checklist.', '',
 '## Progress tracking', '',
 '| Entry | Status | Baseline/setup evidence | Content change | Project change | Completion evidence | Next decision |',
 '|---|---|---|---|---|---|---|',
 '| Selected project path | Not started / Active / Verified / Deferred | Commands and observed result | Guide or exercise | Bounded behavior | Test/demo and explanation | Continue / consolidate / switch |', '',
 'A useful study session ends with a small demonstrated behavior or a diagnosed obstacle. Count independently explained and verified changes, not pages read or repositories opened. Keep remaining entries deferred until they address a measured gap.', '',
 '## Coverage and evidence', '',
 '- [Master source review](../astradocs/MASTER_REPORT.md) and [structured project review](../astradocs/project-review.json): project identity, stack, learning focus, prerequisites, assessment and next action.',
 '- [Tutorial report](../astradocs/PROJECT_TUTORIALS_REPORT.md) and [structured tutorial review](../astradocs/project-tutorials.json): guide classification, populated entrypoints, placeholders and caveats.',
 '- [Final Desktop coverage review](../astradocs/FINAL_REVIEW.md): recursive discovery coverage and excluded dependency/generated directories. The 29 empty placeholders remain documented there; they have no codebase to improve and are not counted as projects here.',
 '- [Machine-readable improvement plans](project-plans.json) and [validation results](validation.json).', '',
 'This is a planning synthesis of the completed September 6–7 reviews, not a new execution audit or a new full Desktop scan. No source app was built, tested or modified for this plan. The baseline assessments remain static observations; reproduce them against the selected current checkout before implementation. Scope reconciliation and local-link validation are performed for this deliverable.', '',
 '## Rebuild the report', '', '`python astrafinalplan/_build_plan.py` regenerates the five sections, index and structured plans from the two reviewed JSON inputs, then validates coverage and links. Edit the generator’s curated overrides/rules if regenerating; direct edits to generated reports would otherwise be replaced.', '']
(OUT/'README.md').write_text('\n'.join(intro),encoding='utf-8')
payload={'created':'2026-09-08','basis':'Static project review (2026-09-06) and tutorial review (2026-09-07); proposed work, not implemented or runtime verified','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (REVIEW,TUTORIALS)},'root_records':len(review['projects']),'nested_apps':len(review['nested_apps']),'plans':[item for _,item,_ in plans]}
(OUT/'project-plans.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

expected={p['path'] for p in records}
actual=[p['path'] for p in payload['plans']]
errors=[]
if len(actual)!=len(set(actual)): errors.append('Duplicate project paths')
if set(actual)!=expected: errors.append('Project coverage mismatch')
if set(guides)!=expected: errors.append('Tutorial/project inventory mismatch')
checked=0
# Create the validation target before checking the index link on a first build.
(OUT/'validation.json').write_text('{"valid": false, "status": "validation in progress"}\n',encoding='utf-8')
for file in OUT.glob('*.md'):
    content=file.read_text(encoding='utf-8')
    for match in re.finditer(r'\]\(([^)]+)\)',content):
        target=match.group(1)
        path,_,anchor=target.partition('#')
        path,anchor=unquote(path),unquote(anchor)
        dest=(pathlib.Path(path) if re.match(r'^[A-Za-z]:/',path) else file.parent/path) if path else file
        checked+=1
        if not dest.exists(): errors.append(f'{file.name}: missing {target}')
        elif anchor and dest.suffix=='.md' and f'id="{anchor}"' not in dest.read_text(encoding='utf-8'):
            errors.append(f'{file.name}: missing anchor {target}')
for p,item,_ in plans:
    if not all(item['tasks'].values()): errors.append('Empty task: '+p['path'])
    if not (OUT/SECTIONS[item['section']][0]).read_text(encoding='utf-8').count(f'id="{item["id"]}"')==1: errors.append('Missing or repeated entry: '+p['path'])
validation={'valid':not errors,'root_records':len(review['projects']),'organized_records':sum(p['path'].startswith('_Organized Desktop/') for p in review['projects']),'nested_apps':len(review['nested_apps']),'total_individual_plans':len(actual),'sections':{str(n):{'file':s[0],'root_records':sum(section(p)==n for p in review['projects']),'nested_apps':sum(section(p)==n for p in review['nested_apps'])} for n,s in SECTIONS.items()},'local_links_checked':checked,'errors':errors,'source_app_runtime_checks':'not performed; this deliverable is a plan'}
(OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
print(json.dumps(validation,indent=2))
if errors: raise SystemExit(1)
