"""Assemble a report from static reviews; never execute or modify source projects."""
import json, re, os
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DESKTOP = REPO.parent
def read(name, base=HERE):
    return json.loads((base / name).read_text(encoding='utf-8-sig'))
def seq(value):
    return value if isinstance(value, list) else [value] if value else []
def prose(value):
    if isinstance(value, list):
        return '; '.join(prose(x) for x in value if x)
    if isinstance(value, dict):
        return '; '.join(str(k).replace('_', ' ') + ': ' + prose(v) for k,v in value.items() if v)
    return str(value or '').strip()
def clean(value):
    text = prose(value).replace('\ufffd', ' ').replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()
def relpath(value):
    value = str(value).replace('\\','/')
    prefix = str(DESKTOP).replace('\\','/') + '/'
    if value.lower().startswith(prefix.lower()):
        value = value[len(prefix):]
    return value
def link(path, label=None):
    path = relpath(path)
    return '[' + (label or path).replace('[','').replace(']','') + '](../../' + quote(path, safe='/') + ')'
def asphase(value, default=4):
    hit = re.search(r'\b([0-7])\b', str(value))
    return int(hit[1]) if hit else default

stages = {
    0: ('Planning and reference collections', 'No coding prerequisite for reading.', 'Choose one exercise or useful reference and apply it to the active project.'),
    1: ('Language and browser foundations', 'Editor, basic Git, and small-program fluency.', 'Rebuild a small example, change its requirements, and explain the result without the walkthrough.'),
    2: ('Client apps and state', 'Stage 1: language, DOM, events, and async fundamentals.', 'Complete one UI flow with validation, persistence, accessibility, and loading/error states.'),
    3: ('APIs and SQL', 'Stage 1 plus HTTP fundamentals; SQL practice alongside.', 'Implement one API slice with durable data, validation, and a meaningful negative-path test.'),
    4: ('Integrated full-stack workflows', 'Stages 2 and 3: client state, APIs, and relational data.', 'Finish one authenticated workflow and verify authorization, persistence, and an integration failure path.'),
    5: ('Domain rules and reliability', 'Stage 4: a complete, tested full-stack slice.', 'Model a state transition and test concurrency, duplicate requests, or partial failure with durable state.'),
    6: ('Architecture and advanced integrations', 'A completed Stage 5 workflow and experience maintaining it.', 'Trace one feature across boundaries and justify a small design change with a test or decision record.'),
    7: ('Specializations', 'A completed full-stack project; Stage 5/6 concepts where the specialty needs them.', 'Scope one specialty feature and measure its behavior under a relevant failure mode.'),
}
base_list = read('project-catalog.json', REPO)['projects']
base = {x['path']: x for x in base_list}
review_files = ['review-desktop-a-m.json','review-desktop-n-z.json','review-organized.json']
bundles, reviews, child_reviews = {}, {}, []
for filename in review_files:
    bundle = read(filename)
    bundles[filename] = bundle
    for row in bundle['projects']:
        if row.get('parent_path'):
            child_reviews.append(row)
            continue
        key = relpath(row['path'])
        if key in reviews:
            raise ValueError('Duplicate review: '+key)
        reviews[key] = row

gemini = read('review-gemini.json')['projects']
by_id = {x['project_id']: x for x in base_list}
duplicate_groups = read('likely-duplicates.json', REPO)['groups']
related = defaultdict(list)
for group in duplicate_groups:
    for path in group['paths']:
        related[path].extend(p for p in group['paths'] if p != path)

aliases = {
    'General_.Architectureproject':'.netarchitectureproject', 'General_.Open2':'.netopen2',
    'General_.Todo':'.nettodo', 'General_Cleanarch':'netcleanarch',
    'General_Open1':'netopen1', 'General_Open3':'netopen3', 'General_Open5':'netopen5',
    'General_Nopsolutions':'nopsolutionsnet', 'General_MasterPlan':'master plan',
    'General_Gitvg':'gitvg/relay', 'General_Jsharness':'jsharness/VTCode',
    'FableDocs_Projects_Hermes':'hermes', 'LLM_Generated_Applybot':'aiapplybot',
    'LLM_Generated_ClaudeDocs':'claude docs', 'LLM_Generated_Fablehelperv2':'fableaihelperv2',
    'LLM_Generated_Fablehelperv3':'fableaihelperv3', 'LLM_Generated_Helper':'aihelper',
    'LLM_Generated_Rag':'netairag', 'OpenSource_Upskilling_.Ramp':'.netramp',
    'OpenSource_Upskilling_.Stripe':'.netstripe',
}
for label in ['Ecommerceproject','Hrproject','Multitenantproject','Orderproject','Ppmproject','Supportproject','Teamproject']:
    aliases['LLM_Generated_'+label] = 'grokbuild'+label.lower()
for label in ['Auth','Docu','Drop','Intercom','Linear','Notion','Shop','Snapshot','Snapshot1']:
    aliases['OpenSource_Upskilling_'+label] = 'net'+label.lower()
lower_paths = {p.lower(): p for p in reviews}
gemini_mapping = []
for row in gemini:
    path = row['path']
    old = base[path]
    name = path.split('/')[-1]
    candidates = related[path] + seq(aliases.get(name))
    candidates += [re.sub(r'^(General_|LLM_Generated_)','',name)]
    candidates += [p for p,x in reviews.items() if clean(x.get('purpose')) == clean(old['purpose'])]
    origin = next((lower_paths[str(p).lower()] for p in candidates if str(p).lower() in lower_paths),None)
    peer = reviews.get(origin,{})
    phase = asphase(peer.get('phase'), 0 if old['record_kind'].startswith('learning') else 4)
    observed = {'working-looking':'Relevant implementation is present; runtime not verified.', 'tutorial':'Teaching/reference workspace; runtime not verified.', 'unknown':'Static sample does not establish runtime readiness.', 'partial':'Partial implementation; runtime not verified.'}.get(old['apparent_state'],old['apparent_state'])
    # Only carry caveats as local documentation observations, not unverified claims from another copy.
    caveats = []
    for caveat in old.get('documentation_caveats',[]):
        statement = clean(caveat.get('statement',caveat))
        if 'Architectureproject' in name and 'Not finished' in statement:
            continue
        if any(word in statement.lower() for word in ['in-memory','non-durable','simulat','not production','no real authentication','scaffold','placeholder','mock']):
            caveats.append(statement)
    row = dict(row)
    row.update(phase=phase, curriculum_role='Related copy / alternative location',
        learning=peer.get('learning') or 'Study the domain and implementation described here at the assigned stage.',
        prerequisites=peer.get('prerequisites') or stages[phase][1],
        next_action=peer.get('next_action') or stages[phase][2],
        assessment=observed + (' Local documentation: '+ '; '.join(caveats[:2]) if caveats else ''),
        stack=old['stack'], related_learning_path=origin,
        duplicate_note='A corresponding learning option exists at '+str(origin)+'. Select one location after comparing the versions; a matching sample does not establish full-tree equality.' if origin else 'Review this location on its own; no corresponding reviewed source was confidently matched.')
    reviews[path] = row
    if name == 'LLM_Generated_Jsprojectlearn':
        row['learning'] = 'JavaScript refactoring first, then React and TypeScript; this local README describes the older 165-exercise curriculum.'
        row['next_action'] = 'Compare an original/refactored example and implement the change independently. Compare this older curriculum with the current direct Desktop SkillForge Quest before choosing a course.'
        row['assessment'] += ' This copy differs from current Desktop JSProjectLearn, a 334-mission campaign.'
    if name == 'General_Open3':
        row['stack'] = {'languages':['C#','TypeScript','JavaScript'],'frameworks':['ASP.NET Core','Umbraco CMS'],'note':'Upstream CMS reference; frontend tooling is one component.'}
    gemini_mapping.append({'path':path,'related_learning_path':origin,'basis':'saved sample match' if origin in related[path] else 'corresponding name/purpose; not byte identity'})

missing = set(base)-set(reviews)
if missing:
    raise ValueError('Unreviewed catalog records: '+str(sorted(missing)))

main = {'JSTut','JS1','buildsql','newcodexJS','recipeweb','_Organized Desktop/08 App And Product Projects/grouphelpdesk'}
dotnet_branch = {'csharptut','borrowbox','campusops','meterforge'}
core_refs = {'netcleanarch','.netarchitectureproject'}
purpose_overrides = {'_Organized Desktop/01 Net Workspaces/.netvg': 'AtlasWork is a teaching application for global workforce hiring, payment, and employee/contractor management.', '_Organized Desktop/02 Build Projects/buildCRMPYJS': 'Full-stack internal CRM and sales-pipeline application.', '_Organized Desktop/03 Master Projects/master': 'Personal planning app connecting areas, goals, projects, tasks, daily checklists, and time tracking.', '_Organized Desktop/03 Master Projects/masterlink': 'Linkwarden bookmark collection and webpage-archiving reference application.', '_Organized Desktop/04 JavaScript Training/jstrain1': 'Full-stack JavaScript practice application for tenant-scoped administrative operations.', '_Organized Desktop/05 Numbered Experiments/e13': 'Headless commerce practice platform with multiple sales-channel concepts.', '_Organized Desktop/05 Numbered Experiments/e6': 'Multi-tenant team-workspace scaffold for full-stack practice.', '_Organized Desktop/05 Numbered Experiments/ww16': 'Channel Compass partner-relationship management scaffold with separated routes, validation, and business logic.', '_Organized Desktop/05 Numbered Experiments/ww32': 'Workspace Wire Slack-style messaging application with route, service, and repository boundaries; see the assessment for implementation limits.', '_Organized Desktop/06 AI And Learning/aiapplybot': 'ApplyPilot-derived job-application automation workspace with a six-stage pipeline and an extended auto-apply stage.', '_Organized Desktop/06 AI And Learning/aiapplybotjs': 'TypeScript/Node CLI implementing a six-stage job-search and application pipeline.', '_Organized Desktop/06 AI And Learning/codehelper': 'Coding-assistance workspace combining an editor and LLM chat with uploaded-codebase browsing and generated explanations.', 'aral': 'React PWA language-learning app with client-side SQLite, a progress-event log, and a thin synchronization backend.', 'buildwhiteboard': 'Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.', 'geminiorganized/General_Aral': 'React PWA language-learning workspace with client-side SQLite, a progress-event log, and a thin synchronization backend.', 'geminiorganized/General_Gitvg': 'Relay workflow-automation teaching platform with triggers, actions, connectors, and execution-engine exercises.', 'geminiorganized/General_Recipeview': 'Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.', 'geminiorganized/LLM_Generated_Buildsql': 'SQL Dojo: a 51-lesson PostgreSQL course with SQL exercises and pytest-based grading, from SELECT statements to query-plan tuning.', 'geminiorganized/LLM_Generated_Buildwhiteboard': 'Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.', 'geminiorganized/LLM_Generated_Jsprojectlearn': 'Older 165-exercise refactoring curriculum spanning JavaScript, React, and TypeScript; compare with the newer direct Desktop version.', 'gitvg/agora': 'Single-store e-commerce teaching application with customer catalog/cart/checkout flows and an administrative back office.', 'gitvg/agora-net': 'C#/.NET e-commerce backend for catalog, inventory, carts, checkout reservations, and fulfillment-related rules.', 'gitvg/atlas': 'Employer-of-record teaching platform for hiring, onboarding, paying, and managing an international workforce.', 'gitvg/bazaar-app': 'Shopify-style e-commerce teaching app with a customer storefront and administrative catalog/order workflows.', 'gitvg/folio': 'Collaborative document-editor teaching app covering blocks, concurrent editing, offline merge, comments, permissions, and version history.', 'gitvg/relay': 'Workflow-automation teaching platform with triggers, actions, connectors, and durable-execution concepts across a fifteen-sprint curriculum.', 'gitvg/storefront': 'E-commerce teaching app with customer browsing/cart/order flows and seller product, inventory, order, and image management.', 'recipeview': 'Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.'}
records=[]
for path,row in sorted(reviews.items(),key=lambda x:x[0].lower()):
    old=base.get(path,{})
    phase=asphase(row.get('phase'))
    role=clean(row.get('curriculum_role') or row.get('journey_role') or row.get('route') or row.get('role') or 'Alternative / targeted lab')
    if path in main:
        role='Core route' if path not in {'JSTut','buildsql'} else 'Core supporting practice'
    if path in core_refs:
        role='.NET branch reference, after a working project'
    if path in dotnet_branch:
        role='.NET branch after the primary-stack capstone'
    evidence=[]
    for v in seq(row.get('evidence_files')):
        if isinstance(v,dict):
            v=v.get('path') or v.get('file')
        if v:
            evidence.append(relpath(v))
    for key in ('documentation_inspected','source_files_inspected','manifests_inspected'):
        evidence.extend(relpath(x) for x in old.get('evidence',{}).get(key,[])[:1])
    evidence=list(dict.fromkeys(evidence))
    entry={'path':path,'name':row.get('name') or old.get('name') or path.split('/')[-1],
        'purpose':purpose_overrides.get(path) or clean(row.get('purpose') or old.get('purpose')),
        'stack':row.get('stack') or old.get('stack',{}),
        'assessment':clean(row.get('assessment') or old.get('apparent_state')) + (' Limits: '+clean(row['limitations']) if row.get('limitations') else ''),
        'phase':phase,'stage_name':stages[phase][0],'curriculum_role':role,
        'learning':clean(row.get('learning') or row.get('learning_value') or stages[phase][0]),
        'prerequisites':clean(row.get('prerequisites') or stages[phase][1]),
        'next_action':clean(row.get('next_action') or stages[phase][2]),
        'evidence_files':evidence,
        'related_paths':list(dict.fromkeys(seq(row.get('related_paths'))+related[path]+seq(row.get('related_learning_path')))),
        'duplicate_note':clean(row.get('duplicate_note') or row.get('duplicate_caveat')),
        'record_kind':old.get('record_kind','software-project-or-workspace'),
        'runtime_verification':'not_run','newly_identified':path not in base}
    if not entry['purpose']:
        raise ValueError('Missing purpose: '+path)
    if not entry['evidence_files']:
        entry['assessment'] += ' No readable text/source evidence was available; this entry is a directory/resource inventory only.'
    records.append(entry)

locations=defaultdict(list)
for row in records:
    path=row['path']
    if path.startswith('_Organized Desktop/'):
        location='/'.join(path.split('/')[:2])
    elif path.startswith('geminiorganized/'):
        location='geminiorganized'
    elif path.startswith('gitvg/'):
        location='Desktop / gitvg nested repositories'
    elif path.startswith('jsharness/'):
        location='Desktop / jsharness nested repositories'
    else:
        location='Desktop / direct workspaces'
    locations[location].append(row)

intro=(HERE/'_master_intro.md').read_text(encoding='utf-8-sig').rstrip()
intro=intro.replace('Stages 2 and 3: client state, APIs, and relational data.','Stages 2 and 3: client state, APIs, and relational data.')
lines=[intro,'','## Coverage and corrections','',
    f'**{len(records)} reviewed project/workspace and resource-collection records.** The earlier inventory contained {len(base)}; this review adds '+', '.join(link(x['path']) for x in records if x['newly_identified'])+'. Bundled teaching exercises stay beneath their parent workspaces rather than inflating this count.','',
    '| Location | Reviewed records |','|---|---:|']
for location,rows in sorted(locations.items()):
    lines.append(f'| {location} | {len(rows)} |')
lines+=['','The historical discovery covered 108 Git roots, 100,421 directories, and 415,133 files after exclusions. Those are the earlier scan totals, not a claim that every file was freshly reread for this report. Its 56 candidate copy/version groups use selected file fingerprints, not complete directory comparisons. See [historical scan validation](../inventory-validation.json).','',
    'Corrections that materially affect your learning order:','',
    '- `.nettodo` is the eShopOnWeb reference storefront. `netopen3` is the Umbraco C#/.NET CMS source. Their names or stale framework tags should not place them among beginner CRUD apps.',
    '- `astra4.2` is a browser break/timer extension with a local preview server; its implementation was missing from the earlier catalog.',
    '- `newcodecjs2` contains five architecture scaffolds. `newcodexJS` contains 20 app folders. `newcodex3/apps` contains 25 numbered concepts with TypeScript and .NET variants (50 folders). README counts and project titles can overstate the implemented scope.',
    '- `netsnapshot` and `netsnapshot1` teach TypeScript/Node + React through saved steps; the “net” prefix does not make them C# courses.',
    '- The modular-monolith README describes shortcomings in other sample applications; its “not finished/no authentication” wording should not be attributed to `.netarchitectureproject` itself.',
    '- A frontend connected to demo identity or a memory adapter can be an excellent learning artifact while still needing work before it demonstrates real authentication or durable persistence.','',
    '## Exercise collections: order inside the workspace','',
    '| Workspace | Suggested internal order and scope |','|---|---|',
    '| '+link('csharptut')+' | Chapters 00–15 for language/data/async; 16–21 for I/O, HTTP, DI, EF, APIs and tests; 22 for the CRUD capstone. Use 23–24 for study guidance. The repository assumes general programming basics; start with a basic language lesson first if variables, loops, and functions are unfamiliar. |',
    '| '+link('JSTut')+' | JS fundamentals first; Node, TypeScript, React and SQL as the active project requires; advanced and C#/.NET companion sections later. Use its workbooks for recall and independent implementation. |',
    '| '+link('JS1')+' | Selected path: task-board → contact-book → focus-timer → issue-desk → secure-notes → invoice-studio → room-booking. The README spans vanilla JS, React/Express, TypeScript/Postgres, richer workflows, and .NET variants. Move between tiers when the relevant checkpoint is met; do not complete all variants. |',
    '| '+link('JSProjectLearn')+' | The current source is SkillForge Quest: 334 missions across 10 worlds, with 1,839 preserved source files recorded in its migration report. Use it as an alternative fundamentals campaign; sequential gates may require earlier unlocks. Its Gemini counterpart retains an older 165-exercise curriculum, so these are materially different versions. |',
    '| '+link('_Organized Desktop/04 JavaScript Training/trainjs')+' | Follow foundations → functions/data → objects/modules/errors → DOM → async/fetch → Node/tooling → backend → testing → TypeScript → React → capstone. Defer advanced architecture until after an application slice. |',
    '| '+link('_Organized Desktop/04 JavaScript Training/jstrain2.2')+' | A large multi-track curriculum, not a small starter app. Choose a flight plan and relevant JS/TS/C# lessons; use its portfolio workspaces to apply them. |',
    '| '+link('newcodexJS')+' | Start with 01-task-manager, then select a distinct data or workflow problem. Later apps often reuse CRUD/admin patterns; “realtime chat” and “marketplace” names do not prove sockets or payments are implemented. See the child catalog below. |',
    '| '+link('newcodecjs2')+' and '+link('newcodex3')+' | Architecture/workflow reading scaffolds. Choose one business domain and one language variant after ordinary full-stack work; trace a feature and complete one missing durable behavior. See the child catalog below. |',
    '| '+link('netsnapshot')+' and '+link('netsnapshot1')+' | Start at 00-walking-skeleton and compare adjacent snapshots using NOTES/CHANGES. Predict the next change, inspect it, then independently implement a small variant. Saved copies are sequential course states, not separate capstones. |','',
    '## Complete per-project catalog','',
    'Each entry has a stage, purpose, stack, static assessment, learning value, prerequisite, next action, and source links. Main-route assignments above take priority; other entries are choices within their stated stage.','']

def anchor(text):
    return 'location-'+re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')
for location in sorted(locations):
    lines.append('- ['+location+'](#'+anchor(location)+')')
lines.append('')
for location,rows in sorted(locations.items()):
    lines+=['<a id="'+anchor(location)+'"></a>','', '### '+location,'']
    for row in sorted(rows,key=lambda r:(r['phase'],r['path'].lower())):
        path=row['path']
        lines+=['#### '+path,'',
            f'**Stage {row["phase"]}: {row["stage_name"]}. {row["curriculum_role"]}.** '+link(path,'Open folder'),'',
            row['purpose'],'',
            '- **Stack:** '+clean(row['stack'])+'.',
            '- **Review:** '+row['assessment'],
            '- **Learn:** '+row['learning'],
            '- **Before starting:** '+row['prerequisites'],
            '- **Next:** '+row['next_action']]
        ev=row['evidence_files']
        selected=[]
        for predicate in (lambda p:p.lower().endswith(('.md','.txt')),lambda p:p.lower().endswith(('.cs','.ts','.tsx','.js','.jsx','.rs','.py','.java','.html')),lambda p:True):
            hit=next((p for p in ev if p not in selected and predicate(p)),None)
            if hit:
                selected.append(hit)
            if len(selected)>=3:
                break
        lines.append('- **Evidence:** '+(', '.join(link(p,Path(p).name) for p in selected)+'.' if selected else 'Directory/resource inventory only; no readable implementation evidence was established.'))
        if row['related_paths']:
            lines.append('- **Related versions/options:** '+', '.join(link(p) for p in row['related_paths'][:4])+'. '+row['duplicate_note'])
        lines.append('')

def choose_evidence(evidence):
    chosen=[]
    for suffixes in [('.md','.txt'),('.cs','.ts','.tsx','.js','.jsx','.rs','.py','.java','.html'),()]:
        hit=next((p for p in evidence if p not in chosen and (not suffixes or p.lower().endswith(suffixes))),None)
        if hit: chosen.append(hit)
    return chosen

# Keep nested teaching applications visibly separate from repository/workspace counts.
lines+=['## Nested-app details and supplemental review notes','',
    f'The following {len(child_reviews)} child applications sit inside three already-counted workspaces. They receive their own learning assignments here without increasing the {len(records)} workspace/resource count.','']
for row in sorted(child_reviews,key=lambda x:(x['parent_path'],asphase(x['phase']),x['path'])):
    path=relpath(row['path'])
    phase=asphase(row['phase'])
    lines+=['### '+path,'',
        f'**Stage {phase}: {stages[phase][0]}. '+clean(row.get('route','Alternative exercise'))+'.** '+link(path,'Open app folder'),'',
        clean(row['purpose']),'',
        '- **Stack:** '+clean(row.get('stack'))+'.',
        '- **Review:** '+clean(row.get('assessment')),
        '- **Learn:** '+clean(row.get('learning')),
        '- **Before starting:** '+clean(row.get('prerequisites') or stages[phase][1]),
        '- **Next:** '+clean(row.get('next_action')),
        '- **Evidence:** '+', '.join(link(p,Path(p).name) for p in choose_evidence(row.get('evidence_files',[])))+'.','']
    if row.get('duplicate_caveat'):
        lines+=['- **Variant guidance:** '+clean(row['duplicate_caveat']),'']

def markdown_value(key,value,depth=3):
    if key in {'projects','method','reviewed_at','root','scope','phase_scale','stage_definitions','coverage','review_method'}:
        return []
    title=key.replace('_',' ').capitalize()
    output=['#'*depth+' '+title,'']
    if isinstance(value,list):
        for entry in value:
            if isinstance(entry,dict):
                path=entry.get('path') or entry.get('name') or entry.get('project')
                if path:
                    output+=['**'+clean(path)+'**','']
                for field,text in entry.items():
                    if field in {'path','name','project'} or not text:
                        continue
                    output.append('- **'+field.replace('_',' ').capitalize()+':** '+clean(text))
                output.append('')
            else:
                output.append('- '+clean(entry))
    elif isinstance(value,dict):
        for field,text in value.items():
            output+=markdown_value(field,text, min(depth+1,5))
    else:
        output.append(clean(value))
    output.append('')
    return output
for filename,bundle in bundles.items():
    selected_keys=[k for k in bundle if any(token in k for token in ['nested','child','curriculum','sequence','recommend','coverage_note','empty','excluded','placeholder','omission'])]
    for key in selected_keys:
        lines+=markdown_value(key,bundle[key])
lines+=['## Candidate copies and versions','',
    'These 56 groups come from the earlier multi-file sample comparison. They are retained as navigation and workload-reduction hints. This review does not authorize deletion or declare a canonical working copy. Compare the feature you need and its tests, then choose one directory for the assignment.','',
    '| Group | Locations with matching saved samples |','|---|---|']
for i,group in enumerate(duplicate_groups,1):
    lines.append('| '+str(i)+' | '+'; '.join(link(p) for p in group['paths'])+' |')
lines+=['','## Non-project folders and boundaries','',
    '`AstraOrganized`, `AstraOrganized2`, and `project-inventory` contain inventory/report artifacts; they are navigation references, not additional application assignments. Empty or container-only folders are tracked in the supplemental coverage notes above. `geminiorganized/General_.Hris` contains only an empty client folder, and `geminiorganized/General_Amasterplan` is empty in the current check. Shortcuts, OS metadata, dependencies, build outputs, agent state, secrets, and unrelated loose personal documents are outside the software-project learning catalog.','',
    'Project components such as an API, frontend, shared package, test project, or historical snapshot remain within their parent workspace. Independently versioned repositories under a container retain their own records. This report adds documentation only; source folders retain their locations.','']

report='\n'.join(lines)
if (HERE/'_coverage_summary.md').exists():
    report=report.replace('# Desktop projects: master SWE upskilling report\n', '# Desktop projects: master SWE upskilling report\n\n'+(HERE/'_coverage_summary.md').read_text(encoding='utf-8').strip()+'\n',1)
(HERE/'MASTER_REPORT.md').write_text(report,encoding='utf-8')
payload={'review_date':'2026-09-06','method':'Source catalog review plus fresh static samples; no source project was executed or modified.',
    'record_count':len(records),'prior_catalog_count':len(base),'projects':records,'nested_app_count':len(child_reviews),'nested_apps':child_reviews,'gemini_learning_relationships':gemini_mapping,
    'supporting_reviews':review_files+['review-gemini.json']}
(HERE/'project-review.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'README.md').write_text('# AstraDocs\n\nStart with [MASTER_REPORT.md](MASTER_REPORT.md): the recommended SWE learning sequence and the complete project-by-project review.\n\n[project-review.json](project-review.json) contains the same learning placements and source links as structured data. The review JSON files preserve supporting observations; underscore-prefixed files are report assembly helpers. No project source was changed.\n',encoding='utf-8')

# Check report coverage and actual local link targets; these checks do not execute projects.
broken=[]
links=[]
for target in re.findall(r'\]\(([^)]+)\)',report):
    if target.startswith(('https://','http://','#')):
        continue
    decoded=unquote(target.split('#')[0])
    check=(HERE/decoded).resolve()
    links.append(str(check))
    if not check.exists():
        broken.append({'target':target,'resolved':str(check)})
missing_evidence=[]
for row in records+child_reviews:
    for path in row['evidence_files']:
        if not (DESKTOP/path).is_file():
            missing_evidence.append(path)
validation={'records':len(records),'nested_apps':len(child_reviews),'prior_records_covered':len(set(base)&set(reviews)),
    'new_records':[x['path'] for x in records if x['newly_identified']],
    'phase_counts':dict(sorted(Counter(x['phase'] for x in records).items())),
    'all_prior_records_reviewed':not missing,'report_local_links_checked':len(links),
    'broken_report_links':broken,'missing_evidence':sorted(set(missing_evidence)),
    'gemini_fresh_files_read':sum(len(x['fresh_checks']) for x in gemini),
    'gemini_read_errors':[e for x in gemini for e in x['errors']],
    'runtime_tests':'not run; report-only task',
    'valid':not broken and not missing_evidence}
(HERE/'report-validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=True))
if not validation['valid']:
    raise SystemExit(1)
