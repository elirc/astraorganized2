"""Render the read-only inventory into an approval-ready cleanup report."""
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote
import json
import csv

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent
data = json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
rows = data['candidates']

def key(path):
    return str(path).replace('\\','/').rstrip('/').casefold()

def size(value):
    if value >= 1024**3: return f'{value/1024**3:,.2f} GiB'
    if value >= 1024**2: return f'{value/1024**2:,.1f} MiB'
    return f'{value/1024:,.1f} KiB'

def union(items):
    roots=[]
    for row in sorted(items,key=lambda r:len(r['path'])):
        if not any(key(row['path']).startswith(key(p['path'])+'/') for p in roots): roots.append(row)
    return sum(r['bytes'] for r in roots)

def linked(path):
    import os
    rel=os.path.relpath(path,DOCS).replace('\\','/')
    return f'[{str(path).replace(chr(92), "/")}]({quote(rel,safe="/:.")})'

a=[r for r in rows if r['tier']=='A']
b=[r for r in rows if r['tier']=='B']
c=[r for r in rows if r['tier']=='C']
local_a=[r for r in a if r['scope']!='Shared user cache']
shared_a=[r for r in a if r['scope']=='Shared user cache']
sum_a=union(a)
sum_ab=union(a+b)
summary={
    'modifiedProjects':data['modifiedProjects'], 'scanRoots':data['scanRoots'],
    'candidateCount':len(rows),'tierACount':len(a),'tierBCount':len(b),'tierCCount':len(c),
    'projectAndCampaignTierABytes':union(local_a),'sharedCacheTierABytes':union(shared_a),
    'allTierABytes':sum_a,'tierBAdditionalBytesAfterA':sum_ab-sum_a,
    'tierAAndBUnionBytes':sum_ab,'scanErrors':len(data['errors']),
    'missingOrUnscannedRoots':[r for r in data['projects'] if r['status'] != 'scanned'],
    'skippedLinks':len(data['skippedLinks']),'freeBytesAtScan':data['disk']['free'],
    'unit':'Logical file bytes; not guaranteed disk space reclaimed',
    'deleted':False,
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
project_rows=[]
for result in data['projects']:
    matching=[r for r in rows if r['project']==result['project'] and r['scope']==result.get('scope')]
    localA=[r for r in matching if r['tier']=='A']
    localB=[r for r in matching if r['tier']=='B']
    project_rows.append({'project':result['project'],'scope':result.get('scope',''),
                         'path':result.get('path',''),'status':result['status'],
                         'totalGiB':round(result['bytes']/1024**3,4),
                         'tierAGiB':round(union(localA)/1024**3,4),
                         'tierBAdditionalGiB':round((union(localA+localB)-union(localA))/1024**3,4),
                         'candidateCount':len(matching)})
with (OUT/'projects.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=['project','scope','path','status','totalGiB','tierAGiB','tierBAdditionalGiB','candidateCount'])
    writer.writeheader();writer.writerows(sorted(project_rows,key=lambda r:-r['tierAGiB']))

lines=['# Disk cleanup proposal — modified upskilling projects','',
       '**Report only. Nothing has been deleted, moved, uninstalled, or cleaned. Your confirmation is required before any cleanup.**','',
       f"Measured {data['startedAt']} to {data['finishedAt']} (UTC). C: had **{size(data['disk']['free'])} free** at the end of the scan.",'',
       f"Scope: **{data['modifiedProjects']} previously modified project paths**, consolidated into **{data['scanRoots']} non-overlapping canonical scan roots**, plus AstraOrganized2 work areas and the shared caches listed below. This includes the earlier Fable-reviewed projects for inventory only; their code was not changed. The 132 unrelated queued project families were not added to the canonical-project scan.",'',
       'The scope comes from the [153-project registry](../fablereview/registry.json) and completed entries in the [delivery ledger](../astra-remaining-improvements/progress.json). Nested entries covered by a parent scan are recorded in the JSON inventory. This is not a scan of every file on the device.','',
       '## Size summary and proposed approval groups','',
       '| Group | Measured logical size | Meaning |','|---|---:|---|',
       f'| A1: project/campaign dependencies and caches | **{size(union(local_a))}** | Best first cleanup candidates for a source-only learning archive. |',
       f'| A2: shared user package/browser caches | **{size(union(shared_a))}** | Optional separate approval; affects other development projects too. |',
       f'| B: additional space after A1+A2 | **{size(sum_ab-sum_a)}** | Build/output folders and delivered staging copies; inspect contents before selecting. |',
       f'| A+B combined, paths counted once | **{size(sum_ab)}** | Conditional logical-size ceiling, not guaranteed free-space gain. |','',
       '**These are logical file sizes, not measured reclaimable disk allocation.** NTFS compression, sparse files and package-store hard links can make actual freed space smaller. Symlinks/junctions were not followed. Nested candidates are not added twice in the totals above. In the CSV, `containedIn` identifies a parent candidate; do not sum all CSV rows.','',
       '## A1 — remove dependencies/caches while keeping the lessons','',
       'If you approve this group, the intended result is readable source, tests and learning documents without installed runtimes/dependencies/build caches. Reinstalling packages or tools and rebuilding would be necessary to run projects later. Keep package manifests, lockfiles, project/solution files, tool configuration, migrations and all source. This assumes you have not stored personal edits inside dependency/cache directories.','',
       'Largest measured A1 candidates (the CSV contains every path):','',
       '| ID | Size | Project/work area | Exact path |','|---|---:|---|---|']
for row in sorted(local_a,key=lambda r:-r['bytes'])[:30]:
    lines.append(f"| {row['id']} | {size(row['bytes'])} | {row['project']} | {linked(row['path'])} |")
lines += ['', '## A2 — optional shared caches', '',
          'These are outside the individual project folders. Removing them usually forces package/browser downloads later and can interrupt offline restore. They are not evidence that the corresponding software should be uninstalled.', '',
          '| ID | Size | Exact path |', '|---|---:|---|']
for row in sorted(shared_a,key=lambda r:-r['bytes']):
    lines.append(f"| {row['id']} | {size(row['bytes'])} | {linked(row['path'])} |")
lines += ['', '## B — larger optional deletions requiring a content check', '',
          'A folder named `build`, `dist`, `bin`, `obj`, `vendor`, `artifacts` or `logs` is not automatically disposable. It can contain tracked files, custom scripts, database backups, useful screenshots or accepted evidence. These entries are candidates to inspect, not blanket deletion instructions. `.yarn` and IDE folders can contain configuration worth retaining.', '',
          'Delivered staging copies under `astra-remaining-improvements/stage` have delivery manifests, but the size scan does not prove every staged file is duplicated. Before removing a whole copy, verify no later unique edits and retain the canonical project, guides, original snapshots and accepted check evidence. Smaller A candidates inside a staging copy are already counted in A.', '',
          '| ID | Whole folder size | Additional after A | Type | Exact path |', '|---|---:|---:|---|---|']
for row in sorted(b,key=lambda r:-r['bytes'])[:35]:
    nested_a=[r for r in a if key(r['path']).startswith(key(row['path'])+'/')]
    incremental=max(0,row['bytes']-union(nested_a))
    lines.append(f"| {row['id']} | {size(row['bytes'])} | {size(incremental)} | {row['kind']} | {linked(row['path'])} |")
lines += ['', '## C — keep by default; only delete after a specific review', '',
          'These are deliberately excluded from the proposed A+B total. Git history, backup/quarantine folders, unconfirmed staging areas, local databases and large archives may hold unique work or data. A remote repository does not prove uncommitted files or local branches are backed up. Database/VM files should not be removed as ordinary caches.', '',
          '| ID | Size | Why retained | Exact path |', '|---|---:|---|---|']
for row in sorted(c,key=lambda r:-r['bytes'])[:25]:
    lines.append(f"| {row['id']} | {size(row['bytes'])} | {row['kind']} | {linked(row['path'])} |")
lines += ['', '## Keep for upskilling', '',
          '- Application source, tests, SQL/migrations, examples, fixtures and source assets.',
          '- `astraupskill`, `upskilling`, `dfableandopus`, README files, project documentation, exercises and solutions.',
          '- Canonical verification logs/screenshots and original-file snapshots used by those guides.',
          '- Dependency manifests and lockfiles; `.csproj`/solution files; configuration and environment files needed to reconstruct the project.',
          '- `.git` and backups unless you explicitly choose to give up their history/recovery value.',
          '- Astra delivery manifests, baselines, progress ledgers and the cleanup inventory until the approved cleanup is checked.', '',
          'The cleanup proposal does not remove whole canonical learning projects. Deleting installed dependencies does not normally reduce the usefulness of reading source or Markdown guides, but rendered apps, code execution, tests, and some editor tooling will stop working until restored.', '',
          '## Full inventory and limitations', '',
          f"- [Every candidate path and size — CSV](disk-space-audit-2026-09-20/candidates.csv): {len(rows)} entries (A: {len(a)}, B: {len(b)}, C: {len(c)}).",
          '- [Totals by project/work area — CSV](disk-space-audit-2026-09-20/projects.csv).',
          '- [Raw project totals, candidates, errors and skipped links — JSON](disk-space-audit-2026-09-20/inventory.json).',
          '- [Deduplicated summary — JSON](disk-space-audit-2026-09-20/summary.json).',
          '- [Read-only scanner](disk-space-audit-2026-09-20/scan.py) and [scan log](disk-space-audit-2026-09-20/scan.log).',
          f"- Scan errors: **{len(data['errors'])}**. Skipped links/reparse points: **{len(data['skippedLinks'])}**. Sizes exclude unreadable and linked targets; see the inventory for paths.",
          f"- Missing or unscanned roots: **{len(summary['missingOrUnscannedRoots'])}**; recorded separately in the summary JSON.",
          '- This scan did not inspect running processes, Docker volumes, the Recycle Bin, Windows system folders, or cloud storage. It did not check Git tracking or hash-compare every staging copy. Shared caches are explicitly separated because their use is not project-exclusive.',
          '- Actual cleanup would recheck selected paths and preserve excluded source/data. No deletion commands or automatic cleanup job have been scheduled.', '',
          '## Confirmation choices', '',
          'You can approve **A1 only**, **A1+A2**, or specific candidate IDs/paths from the CSV. B and C require explicit selections after their contents/recovery value are checked. Until then, all project and cache files remain in place.', '']
report=DOCS/'DISK_CLEANUP_PROPOSAL_2026-09-20.md'
report.write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(summary,indent=2))
print(str(report))
