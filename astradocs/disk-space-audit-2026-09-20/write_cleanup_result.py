import json,collections
from pathlib import Path
OUT=Path(__file__).resolve().parent
plan=json.loads((OUT/'approved-cleanup-plan-2026-09-21.json').read_text())
events=[json.loads(s) for s in (OUT/'cleanup-results-2026-09-21.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
assert events[-1]['event']=='finish','Cleanup is still running'
targets=[e for e in events if e['event']=='target']
assert len(targets)==len(plan['selected'])
lucas=json.loads((OUT/'lucasrouter-after.json').read_text())
counts=collections.Counter(e['status'] for e in targets)
remaining=[e for e in targets if Path(e['path']).exists()]
errors=[e for e in targets if e['errors']]
def gib(n): return f'{n/1024**3:,.2f} GiB'
finish=events[-1]
resumed=any(e['event']=='resume' for e in events)
summary={'statusCounts':dict(counts),'deletedFiles':sum(e['deletedFiles'] for e in targets),'deletedLogicalBytes':sum(e['deletedLogicalBytes'] for e in targets),'fileAndLogicalByteCountsAreLowerBounds':resumed,'freeBytesBefore':finish['freeBytesBefore'],'freeBytesAfter':finish['freeBytes'],'observedFreeSpaceIncrease':finish['observedFreeSpaceIncrease'],'lucasrouterMetadataUnchanged':lucas['unchanged'],'remainingSelectedPaths':len(remaining),'targetsWithErrors':len(errors),'retainedInventoryCandidates':len(plan['skipped'])}
(OUT/'cleanup-summary-2026-09-21.json').write_text(json.dumps(summary,indent=2))
lines=['# Disk cleanup completed — 2026-09-21','',
       'Authorized by: “yes clean up delete all except for the lucasrouter project”. Cleanup was applied to dependencies, caches and checked generated outputs from the previous proposal. Source, learning documents, backups and Git history remain. Whole staging copies were retained because duplicate verification was not completed; their separately listed dependencies/caches were cleaned where eligible.','',
       f"- Selected paths: **{len(targets)}**; results: **{dict(counts)}**.",
       f"- Recorded files deleted: **{summary['deletedFiles']:,}**; recorded logical bytes removed: **{gib(summary['deletedLogicalBytes'])}**. These are lower bounds: deletion was paused and resumed with parallel file operations, so part of the interrupted target is not included in its per-file counters.",
       f"- C: free space before: **{gib(finish['freeBytesBefore'])}**; after: **{gib(finish['freeBytes'])}**.",
       f"- Observed free-space increase: **{gib(finish['observedFreeSpaceIncrease'])}**. Other device activity can affect this measurement.",
       f"- Lucasrouter main and staging-folder metadata fingerprints unchanged: **{lucas['unchanged']}**. This compares names, sizes, modification times and attributes without following links; it is not a file-content hash audit.",
       f"- Selected paths still present: **{len(remaining)}**; paths with deletion errors: **{len(errors)}**.", '',
       '## Lucasrouter exclusions','']
lines += [f'- `{p}`' for p in plan['protectedPaths']]
lines += ['', 'Shared npm, pnpm, NuGet, pip and Playwright caches outside the project were included in the approved cleanup. Future package restores or browser installs, including for Lucasrouter, may need downloads. No Lucasrouter project/staging path was selected.', '',
          '## Largest removed locations','', '| ID | Logical bytes deleted | Path |','|---|---:|---|']
for e in sorted(targets,key=lambda e:-e['deletedLogicalBytes'])[:35]:
    lines.append(f"| {e['id']} | {gib(e['deletedLogicalBytes'])} | `{e['path']}` |")
lines += ['', '## Retained items','',
          'The retained list includes Lucasrouter, Git history, archives/data, backups, original snapshots, learning/check evidence, whole staging work areas, and ambiguous folders. Some folders called `build`, `Logs` and `target` contain actual source. None of these were removed just because of their name.', '',
          '| Reason | Candidate count |','|---|---:|']
for reason,count in collections.Counter(r['reason'] for r in plan['skipped']).most_common(): lines.append(f'| {reason} | {count} |')
if errors:
    lines += ['', '## Deletion errors / partial removals','']
    for e in errors: lines.append(f"- `{e['path']}` — {e['status']}; {len(e['errors'])} errors. Exact errors are in the result log.")
lines += ['', '## Audit files','',
          '- [Approved paths and every retention reason](disk-space-audit-2026-09-20/approved-cleanup-plan-2026-09-21.json).',
          '- [Per-path deletion outcomes and errors](disk-space-audit-2026-09-20/cleanup-results-2026-09-21.jsonl).',
          '- [Machine-readable totals](disk-space-audit-2026-09-20/cleanup-summary-2026-09-21.json).',
          '- [Lucasrouter before/after verification](disk-space-audit-2026-09-20/lucasrouter-after.json).',
          '- [Original cleanup proposal](DISK_CLEANUP_PROPOSAL_2026-09-20.md) — historical measurements, not a current inventory.', '',
          'Applications were not rebuilt or tested after removal: dependencies were deliberately removed for source-based upskilling. No application was uninstalled and no unrelated running process was terminated.', '']
(OUT.parent/'DISK_CLEANUP_COMPLETED_2026-09-21.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(summary,indent=2))
