from pathlib import Path
from urllib.parse import quote
import json,re,collections
OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'REMAINING_PROJECT_REVIEW_INVENTORY_2026-09-21.json').read_text())
rows=data['projects']
def link(path,label=None): return f'[{label or path}](../../{quote(path,safe="/.")})'
def cell(s):return str(s).replace('|','/').replace('\n',' ')
def learning(r):return [f for f in r['files'] if re.search(r'(^|/)(learning|upskill|upskilling|astraupskill|dfableandopus)(/|$)',f,re.I)]
first=['_Organized Desktop/08 App And Product Projects/recipegen-app','AlanAndEliSoccer','_Organized Desktop/08 App And Product Projects/HNJOBTRACK']
variants={'aicallhelper','aicallhelper2','fableaihelperv2','fableaihelperv3','finalcallhelp','spacegame','astraspacegameweb','_Organized Desktop/12 Other Projects/3buildhyper','_Organized Desktop/12 Other Projects/hypernova-inc-main','_Organized Desktop/12 Other Projects/FinalJep','_Organized Desktop/04 JavaScript Training/jstrain3','_Organized Desktop/07 Anti Projects/antiinv','_Organized Desktop/06 AI And Learning/codehelper','_Organized Desktop/06 AI And Learning/codehelper/ww20'}
references={'jsharness/VTCode','_Organized Desktop/03 Master Projects/mastermatter','_Organized Desktop/03 Master Projects/MasterStore','_Organized Desktop/05 Numbered Experiments/rn1','_Organized Desktop/12 Other Projects/pyhealth','_Organized Desktop/09 Grav And VG Projects/gravreviewboardjspy','_Organized Desktop/09 Grav And VG Projects/graveopenjspy','_Organized Desktop/09 Grav And VG Projects/VGdemo','_Organized Desktop/01 Net Workspaces/csbootcamp'}
references.update(r['path'] for r in rows if r['path'].startswith('geminiorganized/LLM_Generated_') or 'OpenSource_Upskilling_Snapshot' in r['path'] or 'General_New' in r['path'])
def group(r):
    if r['path'] in first:return '1 — Focused fixes first'
    if r['path'] in variants:return '2 — Choose scope/variant first'
    if r['path'] in references:return '3 — Curriculum/upstream: narrow contribution'
    if learning(r):return '4 — Existing learning material: verify gaps first'
    return '5 — Bounded workflow review'
counts=collections.Counter(group(r) for r in rows)
allfiles=(OUT/'REMAINING_PROJECT_FILE_NAMES_2026-09-21.txt').read_text().splitlines()
missing_evidence=[c['path'] for r in rows for c in r.get('evidenceChecks',[]) if not c['exists']]
lines=['# Remaining projects: review and proposed improvement order','',
       'Reviewed 2026-09-21. **132 project families are still pending in the campaign ledger; all 132 folders exist. This is a planning queue, not a claim that 132 projects are broken or untouched.** No project files were edited, no dependencies installed, and no project tests or servers were run in this review.','',
       '## What the current files show','',
       '- 107 campaign deliveries remain marked delivered; the earlier completed 14-project and 15-project batches stay excluded.',
       '- The pending queue has no exact path overlap with the 153-project Fable registry. Existing enhancements found in pending folders must still be preserved; the registry alone does not establish who last changed every file.',
       f"- **{sum(bool(r['testFiles']) for r in rows)} families** have test-related filename indicators; **{sum(bool(learning(r)) for r in rows)} families** have recognized learning-document paths. These are discovery indicators, not passing-test or course-quality claims.",
       '- `csbootcamp` illustrates the limit of filename counts: it has a custom `bootcamp/_lib/Check/Check.cs` assertion harness even though the conventional test-name scan finds no tests.',
       '- `codehelper/ww20` is a separately queued child of `codehelper`. Do not improve both as independent copies of the same files. Its current package name is `multi-tenant-event-platform`; it needs its own scope decision.',
       '- The review deliberately did not reinstall the dependencies removed during cleanup. Reinstall only what a selected future project needs.', '',
       '## Recommended first batch: three concrete fixes','',
       'These findings are supported by reading the named source files. They have not been reproduced by running the applications. Add a failing regression first when implementation begins.','',
       '### 1. recipegen-app — validate request and provider data','',
       f"Evidence: {link(first[0]+'/app/api/recipes/route.ts','API route')} (lines 72–79 and 125 onward), {link(first[0]+'/lib/storage.ts','browser storage')} (lines 21 and 55), and {link(first[0]+'/app/HomeClient.tsx','submission flow')}.",
       '- A JSON `null` request parses successfully, then is destructured outside a guard at line 125. That bypasses the intended controlled validation response.',
       '- Provider output validation checks only a few truthy fields and two arrays before casting to `Recipe`; field types, numeric bounds and nested entries are not validated.',
       '- Saved history/favorites accept any valid JSON shape as an array; malformed-but-valid stored data can reach consumers.',
       '**Proposed improvement:** explicit object/field validation at both boundaries, a mockable provider, defensive stored-data parsing, and useful storage-error behavior. **Acceptance cases:** null body, non-string ingredients, invalid servings, malformed recipe arrays, valid response, corrupt storage, and provider failure—all without a paid API call. No conventional test files were found.','',
       '### 2. AlanAndEliSoccer — make saved study progress resilient','',
       f"Evidence: {link('AlanAndEliSoccer/soccer-laws-app/src/components/law-page/LawProgressToggle.tsx','LawProgressToggle.tsx')} (lines 7–13, 19, and 31). The actual app root is `soccer-laws-app`, not the outer family directory.",
       '- `readProgress()` returns parsed JSON without checking that it is an array of valid law numbers; stored `{}` or `null` can reach the `.includes()` call.',
       '- The storage write is not caught, so storage-denied or quota failures throw after UI state has already changed.',
       '**Proposed improvement:** extract a small validated persistence helper, retain usable in-memory state when saving fails, and add reload/toggle regressions. **Acceptance cases:** empty storage, malformed JSON, wrong JSON type, duplicates/out-of-range entries, unavailable storage and a normal reload. No conventional test files were found.','',
       '### 3. HNJOBTRACK — recover interrupted imports','',
       f"Evidence: {link(first[2]+'/backend/app/services/scraper.py','scraper.py')} (lines 38–59 and the batch-insert loop), and {link(first[2]+'/backend/app/api/admin.py','admin pipeline')}.",
       '- The scraper inserts a `pending` thread before fetching comments. On another run, any existing thread is returned immediately regardless of status.',
       '- If fetching or a later insertion batch fails, a retry can skip the missing comments and advance to parsing an incomplete import.',
       '**Proposed improvement:** status-aware resumable import with idempotent comment writes and explicit failure/retry state. **Acceptance cases:** failure immediately after thread creation, failure after one insert batch, retry without duplicates, already-complete import and malformed input. Use fake HTTP/database adapters; do not send notifications. No conventional test files were found.','',
       '## Next: verify existing work before proposing more changes','',
       '| Project | Fresh evidence / proposed next check |','|---|---|',
       f"| {link('_Organized Desktop/05 Numbered Experiments/ww36','ww36')} | Source already uses serializable reservation transactions, actor-scoped visibility, and lifecycle guards; tests and `docs/learning/testing-rationale.md` already exist. Verify their baseline; add a missing concurrent/repeated lifecycle case only if it adds coverage. Do not redo the existing safeguards. |",
       f"| {link('_Organized Desktop/05 Numbered Experiments/ww26','ww26')} | The sampled release test mocks transactions and repositories and checks an already-released lease. A real database contention/stale-owner check is a proposed follow-up, not a confirmed missing implementation. Review the full suite first. |",
       f"| {link('_Organized Desktop/01 Net Workspaces/.netcalendy','.netcalendy')} | Existing application/domain/integration test files and extensive `docs/upskill` material. Verify booking-overlap and timezone-boundary coverage before expanding the course. |",
       f"| {link('ankijs')} | Existing scheduler, sync/outbox, repository and UI tests plus `docs/upskill`. Start with a coverage review of one offline/replay invariant; do not regenerate the existing curriculum. |",
       f"| {link('tagalog')} | Existing core lesson/session test files. Review guest-to-account progress replay and the package boundary first; no sync defect was established in this pass. |",
       f"| {link('_Organized Desktop/05 Numbered Experiments/ww43','ww43')} | Current note-service, repository, route-auth and schema tests plus learning documents. Check stale revision and sharing coverage before adding another change. |", '',
       '## Resolve variants and reference projects deliberately','',
       '- Choose a baseline within the audio-assistant families (`aicallhelper`, `aicallhelper2`, `fableaihelperv2`, `fableaihelperv3`, `finalcallhelp`) before repeating the same improvement. Similar purpose is not proof of identical files.',
       '- Compare `spacegame` with `astraspacegameweb`, and `3buildhyper` with `hypernova-inc-main`, before selecting a copy to change.',
       '- `FinalJep`, `jstrain3`, `antiinv`, and the `codehelper` parent/child boundary need scope clarification from their implementations rather than assumptions from folder names.',
       '- Existing curricula, snapshot histories, and large upstream projects belong on a narrow exercise/contribution track. Do not rewrite whole courses, modify starter solutions wholesale, or treat upstream size as a reason to overhaul them.', '',
       '## Full remaining-project review','',
       'All 132 queued families are listed below. Purpose and suggested workflow are carried forward from the September 6 source catalog unless specifically updated above. Current file/test/learning indicators come from the fresh September 21 inventory. “Test indicators” can include fixtures/configuration or vendored examples; “learning files” is a path-name heuristic. Neither measures executed coverage.','']
for label in sorted(counts):
    lines += [f'### {label} ({counts[label]})','', '| Project | Files | Test indicators | Learning files | Proposed next action |','|---|---:|---:|---:|---|']
    for r in rows:
        if group(r)!=label:continue
        action=r.get('priorReview',{}).get('next_action','Define the event-platform child boundary, then trace one event through gateway, service and consumer using existing tests.')
        if r['path'] in first:action='Implement the focused regression-led fix described above.'
        elif label.startswith('4'):action='Verify existing work before edits. '+action
        lines.append(f"| {link(r['path'])} | {r['fileCount']:,} | {len(r['testFiles'])} | {len(learning(r))} | {cell(action)} |")
    lines += ['']
lines += ['## Filename lists and review limits','',
          '- [Project names / Desktop-relative family paths](REMAINING_PROJECT_NAMES_2026-09-21.txt): 132 entries.',
          f'- [All inventoried filenames, with Desktop-relative paths](REMAINING_PROJECT_FILE_NAMES_2026-09-21.txt): **{len(allfiles):,} unique entries**. Full paths distinguish repeated names such as `README.md`.',
          '- [Per-project files, manifests, package scripts, evidence checks and scan errors](REMAINING_PROJECT_REVIEW_INVENTORY_2026-09-21.json).',
          '- [Original remaining queue](REMAINING_PROJECTS_TO_DO_2026-09-19.md) and [delivery ledger](../astra-remaining-improvements/progress.json) were not altered; reviewing is not delivery.',
          '- Filename discovery used `rg --files --hidden --no-ignore` with explicit directory exclusions and no symlink-following flag. It includes source, docs, assets, configurations, snapshots and any generated files outside excluded folders. It is not a hand-certified list of authored source files.',
          '- Excluded directory names: '+', '.join('`'+n+'`' for n in data['excludedDirectoryNames'])+'.',
          '- Filesystem listing errors: 0. All 132 roots exist. Nested family entries can repeat in per-project inventories; the standalone filename list is deduplicated.',
          f'- Older catalog evidence paths missing today: {len(missing_evidence)}; absence can mean a move or rename and is not itself a defect. See inventory `evidenceChecks`.',
          '- No secret/environment-file contents were read. Their filenames may appear in the path inventory.',
          '- This is a queue-wide static review with targeted source samples, not a line-by-line audit of 80,414 files. No build, test-pass, performance, security or runtime readiness claims are made.', '']
(OUT/'REMAINING_PROJECT_REVIEW_2026-09-21.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'groups':dict(counts),'projects':len(rows),'uniqueFiles':len(allfiles),'missingPriorEvidence':len(missing_evidence)},indent=2))
