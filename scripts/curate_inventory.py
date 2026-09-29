"""Resolve inventory-specific ambiguities without consulting previous catalogs."""
from pathlib import Path
from collections import defaultdict
import json
import re
import uuid
import html
from analyze_projects import readable, NAMESPACE, identify_category, analyze
from scan_desktop import ROOT, OUT, save, now

OVERRIDES = {
    '.nettodo': 'ASP.NET Core eShopOnWeb reference storefront demonstrating a monolithic web application.',
    'buildjira': 'Jira-style project and issue tracker; the active app is C#, with earlier JavaScript code retained as archival reference.',
    'buildsubbox': 'ParcelPilot subscription-box UI prototype for subscriber preferences, billing, curation, and fulfillment.',
    'masterdidy': 'Dify LLM application platform with workflow, knowledge-retrieval, and agent components.',
    'masterflag': 'Flagsmith feature-flag and remote-configuration platform.',
    'masterform': 'Formbricks survey and experience-management platform.',
    'masterindicoPYJS': 'Indico event and conference management platform.',
    'mastermatter': 'Mattermost team messaging and collaboration platform.',
    'masternovu': 'Novu notification infrastructure and in-app inbox platform.',
    'masterpload': 'Payload TypeScript CMS and application framework.',
    'masterpostiz': 'Postiz social-media scheduling and publishing application.',
    'masterpre': 'pretalx conference proposal, speaker, and schedule management.',
    'grav1pretalx': 'pretalx conference proposal, speaker, and schedule management.',
    'masterrnative': 'Expo farm-batch tracker for feed, mortality, expenses, and sales.',
    'mastertwenty': 'Twenty open-source CRM with customer records, workflows, and team views.',
    'masternocu': 'NocoBase extensible low-code application platform.',
    'netcleanarch': 'ASP.NET Core Clean Architecture starter/reference application.',
    'netopen3': 'Umbraco content management system and its administration interface.',
    'nopsolutionsnet': 'nopCommerce ecommerce application with storefront, administration, and plugins.',
    'jsdrillapp': 'Reps coding-practice app for building programming fluency through repeated exercises.',
    'jstrain2': 'Workflow automation app with retries, queues, and execution logs; its README also documents an agent watchdog.',
    'jstrain3': 'Workspace containing three DeskPilot app variants; their relationship and intended scope need closer review.',
    'jstrain3.0': 'Ecommerce practice app with feature flags and experiments.',
    'react': 'Small browser-based Jeopardy game.',
    'B1': 'Incident-response workspace with runbooks and incident-management components.',
    'D1': 'Real-time kanban project-board application.',
    'e11': 'Roughflow visual board/editor application.',
    'e17': 'Forum application with moderation, trust levels, and discussion threads.',
    'g1': 'Bagel Atlas directory for exploring bagel shops and cities.',
    'j2': 'Java command-line tracking exercise; consult its README for the tracked entities.',
    'j3': 'Java command-line bank-account simulator with saved account data.',
    'rn1': 'Bluesky social-app source workspace, including mobile/web client components.',
    'ww35': 'Appointment-booking application.',
    'ww39': 'Support-ticket workflow application with service and repository layers.',
    'ww43': 'Notes application with version history, sharing, and conflict-aware saves.',
    'ww49': 'Order-operations dashboard with coupons, fulfillment, refunds, and audit services.',
    'ww6': 'Cloud-cost allocation and chargeback dashboard.',
    'z1': 'Internal request-and-approval workflow application with mocked infrastructure.',
    'z3': 'Two practice apps: a founder CRM and a customer-feedback board.',
    'z7': 'Hiring-pipeline tracker.',
    'z8': 'Event-operations dashboard.',
    'z9': 'Freelancer and agency operations portal.',
    'zz1': 'Multi-tenant CRM with deal workflows and service-layer authorization.',
    'zz6': 'Policy-management and acknowledgment portal with exceptions and reporting.',
    'zz7': 'Procurement dashboard for vendors, sourcing, purchase orders, and reporting.',
    'zz8': 'HRIS and employee-performance review workflows in one workspace.',
    'zz9': 'Internal case-management application with team queues and audit trails.',
    'claudeailab-temp': 'Next.js starter retained alongside the AI-lab project; substantive app behavior was not established.',
    'antiinv': 'Frontend/backend starter with a generic sign-in screen; its intended inventory domain remains unverified.',
    'recipegen-app': 'Weeknight recipe app that suggests dinner ideas from available ingredients.',
    'recipegen-temp': 'Next.js starter retained alongside the recipe app.',
    '3buildhyper': 'HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.',
    'hypernova-inc-main': 'HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.',
    'andie': 'Shopify-related scripting workspace, including a metaobject population utility.',
    'cc': 'CMS web-application prototype.',
    'FinalJep': 'Convex/React app variants with chat components; a Jeopardy implementation was not established in the inspected samples.',
    'finaljepgame': 'Jeopardy game builder and player workspace.',
    'buildbusinesses': 'LocalOps Ledger for keeping daily operating records for small local businesses.',
    'buildsmallplates': 'Small Plates mobile weightlifting log with workout progression and on-device storage.',
    'c#interview': 'Ten-week C# upskilling and interview-preparation curriculum with drills and portfolio work.',
    'finalcallhelp': 'CueDeck desktop conversation-assistance and practice application.',
    'gitjira': 'Sprint plans and build instructions for the separate GitJira issue-tracker app.',
    'harbor': 'Customer-messaging and support-inbox learning project with API, web, worker, and retrieval components.',
    'pulse': 'Product-analytics learning project with event ingestion, consumers, jobs, and a web interface.',
    'grokbuildppmproject': 'Project-portfolio management practice app with portfolios, programs, projects, and tasks.',
    'grokjs': 'JavaScript, .NET, and full-stack practice labs with worked explanations and exercises.',
    'jobtrack': 'Daybook local-first calendar and job-application tracker.',
    'master plan': 'Project-based software-engineering study plans and a progression of practice projects.',
    'readme': 'Existing Desktop inventory document; listed as a reference artifact and not used to discover or assess projects.',
    'VTCode': 'VTCode Rust terminal coding-agent workspace.',
    'antigravupskill': 'Existing architecture reviews and learning notes for Antigravity projects; retained as reference material.',
    'claude docs': 'Software-engineering study plans, worked examples, and coding-practice guidance.',
    'GPTDocs': 'Software-engineering learning and reference documents.',
    'resume': 'Career and résumé reference materials.',
    'lucasrouter': 'Fleet and delivery-routing workspace with searchable stops, delivery status, and a driver interface.',
}
ALIASES = {'Architectureproject': '.netarchitectureproject', '.Architectureproject': '.netarchitectureproject',
           '.Todo': '.nettodo', 'Cleanarch': 'netcleanarch', 'Nopsolutions': 'nopsolutionsnet',
           'Open3': 'netopen3', 'Readme': 'readme', 'MasterPlan': 'master plan',
           'Jsharness': 'VTCode', 'Ppmproject': 'grokbuildppmproject', 'ClaudeDocs': 'claude docs',
           'Jsprojectlearn': 'JSProjectLearn', 'Gptdocs': 'GPTDocs'}

def canonical(name):
    name = re.sub(r'^(General_|LLM_Generated_|OpenSource_Upskilling_|FableDocs_Projects_)', '', name)
    for old, new in ALIASES.items():
        if name.casefold() == old.casefold():
            return new
    return name

catalog = json.loads((OUT / 'project-catalog.json').read_text(encoding='utf-8'))
index = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))['directories']
boundaries = json.loads((OUT / 'project-boundaries.json').read_text(encoding='utf-8'))
container_paths = sorted(set(boundaries.get('container_only_records_removed', [])) | {p['path'] for p in catalog['projects'] if p['path'].startswith('_Organized Desktop/') and p['path'].count('/') == 1})
loose = [{'container': path, 'files': [path + '/' + name for name in index[path]['files']],
          'note': 'Loose container-level material; not counted as a separate software project.'} for path in container_paths]
save('loose-resources.json', {'resources': loose})
catalog['projects'] = [p for p in catalog['projects'] if p['path'] not in container_paths]
curriculum_root = 'gitvg/astra'
if not any(p['path'] == curriculum_root for p in catalog['projects']):
    curriculum_files = [path + '/' + name for path, item in index.items() if path == curriculum_root or path.startswith(curriculum_root + '/') for name in item['files']]
    boundary = {'path': curriculum_root, 'workspace': curriculum_root, 'boundary': 'nested-learning-collection', 'parent_path': None, 'git_roots': []}
    project = analyze(boundary, curriculum_files, index, [boundary])
    project['purpose'] = 'Software-engineering curriculum with onboarding, learning modules, handbooks, capstone templates, and a validation script.'
    project['category'] = 'Learning & reference'
    project['apparent_state'] = 'tutorial'
    catalog['projects'].append(project)
extra_path = '_Organized Desktop/06 AI And Learning/ailearningpath'
if not any(p['path'] == extra_path for p in catalog['projects']):
    materials = [extra_path + '/' + name for name in index[extra_path]['files']]
    catalog['projects'].append({
        'project_id': str(uuid.uuid5(NAMESPACE, extra_path.casefold())), 'name': 'ailearningpath',
        'path': extra_path, 'absolute_path': str(ROOT / extra_path), 'workspace_path': extra_path,
        'category': 'Learning & reference', 'purpose': 'Applied architecture and project-based software-engineering learning plans in two ODT documents.',
        'purpose_evidence': materials, 'stack': {k: [] for k in ['languages', 'frameworks', 'data', 'infrastructure', 'testing', 'integrations']},
        'apparent_state': 'tutorial', 'runtime_verification': 'not_run', 'implemented_features': [],
        'learning_material': {'matching_resource_count': 2, 'key_paths': materials, 'selection': 'Document filenames inspected; ODT contents not reviewed.'},
        'repository': {'git_repository': False, 'git_roots': [], 'parent_project_id': None, 'components': [], 'related_projects': []},
        'scope': {'source_files': 0, 'document_files': 2, 'test_files': 0, 'boundary_reason': 'learning-document-collection'},
        'evidence': {'manifests_inspected': [], 'source_files_inspected': [], 'documentation_inspected': [], 'tests_inspected': [], 'tree_source': 'scan-index.json'},
        'uncertainties': ['ODT documents cataloged by descriptive filenames only.'], 'inspection_level': 'document-filenames-only',
        'sample_fingerprint': None, 'fingerprint_file_count': 0, 'last_reviewed': now(),
    })
overrides_lower = {key.casefold(): value for key, value in OVERRIDES.items()}
for project in catalog['projects']:
    project.setdefault('documented_purpose', project['purpose'])
    key = canonical(project['name']).casefold()
    if key in overrides_lower:
        project['purpose'] = overrides_lower[key]
        project['purpose_review'] = 'Clarified from local README, UI titles, component paths, or source samples; no external catalog used.'
    else:
        text = html.unescape(project['purpose']).lstrip('\ufeff')
        text = re.sub(r'(?i)\b(?:production-grade|production-ready|production-style|production-shaped|production-minded|enterprise-style|high-quality|powerful|complete|realistic|beautifully designed)\b\s*', '', text)
        text = re.sub(r'(?i)^This (?:repository|repo|project) (?:contains|is) (?:a |an )?', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            text = text[0].upper() + text[1:]
        if len(text) > 210:
            text = text[:207].rsplit(' ', 1)[0].rstrip(',:;-') + '…'
        project['purpose'] = text
    caveats = []
    # Resolve documentation/implementation ambiguity, not another broad source scan.
    for path in project['evidence']['documentation_inspected'][:1]:
        if key in {'readme', 'antigravupskill'}:
            continue
        text = readable(path, 16000)
        for line in text.splitlines():
            if re.search(r'(?i)(archival|archived|not production|not implemented|not finished|planned.only|mocked|mock payments|stubbed|in.memory|simulated|prototype|starter|scaffold|stack \(planned\))', line):
                line = re.sub(r'[*`#]', '', line).strip()
                if 15 < len(line) < 450:
                    caveats.append({'statement': line[:300], 'source': path, 'basis': 'Documentation caveat; not independently runtime-verified'})
    project['documentation_caveats'] = caveats[:4]
    if not project['scope']['source_files']:
        project['record_kind'] = 'learning-or-reference-collection'
        project['apparent_state'] = 'tutorial' if project['learning_material']['matching_resource_count'] else 'unknown'
        if key in {'readme', 'resume', 'master plan', 'antigravupskill'}:
            project['category'] = 'Plans, career & inventory references'
    else:
        project['record_kind'] = 'software-project-or-workspace'
        if key in {'claudeailab-temp', 'recipegen-temp', 'buildsubbox', 'antiinv', 'finaljep'}:
            project['apparent_state'] = 'partial'
    if key == 'readme':
        project['assessment_exclusion'] = 'Existing project index recognized as metadata. Its project list was not used for discovery, grouping, stack detection, or assessments.'
        project['evidence']['documentation_inspected'] = []
        project['purpose_evidence'] = None
    if key == 'buildjira':
        project['uncertainties'].append('README and active Program.cs identify the C# app as current; older TypeScript/React sources are explicitly archival.')
    project['last_reviewed'] = now()
    if key in {'astra1', 'astra2', 'astraspacegameweb', 'spacegame', 'spacegamev2', 'alanandelisoccer', 'react', 'finaljepgame', 'globgame'}:
        project['category'] = 'Games & language learning'
    if key in {'ankijs', 'devdeck', 'buildermentor', 'buildsql', 'skillforgejs', 'js1', 'jstut', 'jsprojectlearn', 'grokjs', 'groktuts', 'jsdrillapp', 'c#interview', 'csharptut'}:
        project['category'] = 'Learning & reference'
    if project['path'] == curriculum_root:
        project['record_kind'] = 'learning-or-reference-collection'
        project['category'] = 'Learning & reference'
        project['apparent_state'] = 'tutorial'

projects = sorted(catalog['projects'], key=lambda p: p['path'].lower())
ids = {p['project_id'] for p in projects}
for project in projects:
    project['repository']['related_projects'] = [r for r in project['repository']['related_projects'] if r['project_id'] in ids]
catalog['projects'] = projects
catalog['updated_at'] = now()
catalog['method'] = 'Independent read-only filesystem discovery, followed by static samples and targeted clarification of ambiguous descriptions. Stated purpose and documentation caveats are separated from observed code constructs. No installations, builds, tests, or project runtimes were executed.'
catalog['independence']['phase'] = 'independent-review-complete'
save('project-catalog.json', catalog)
duplicates = json.loads((OUT / 'likely-duplicates.json').read_text(encoding='utf-8'))
duplicates['groups'] = [g for g in duplicates['groups'] if all(i in ids for i in g['project_ids'])]
save('likely-duplicates.json', duplicates)
boundaries['omitted_workspaces'] = [b for b in boundaries['omitted_workspaces'] if b['path'] != extra_path]
boundaries['container_only_records_removed'] = container_paths
boundaries['final_project_paths'] = [p['path'] for p in projects]
save('project-boundaries.json', boundaries)
print(json.dumps({'records': len(projects), 'containers_separated': len(container_paths), 'odt_collection_added': extra_path, 'duplicate_groups': len(duplicates['groups'])}))
