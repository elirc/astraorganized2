from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];C=Path(__file__).resolve().parent
manifest=json.loads((B/'deliveries/44013f102ff1.json').read_text(encoding='utf-8'))
assert manifest['status']=='delivered'
root=B.parent.parent/manifest['project']
for entry in manifest['files']:
    assert hashlib.sha256((root/entry['file']).read_bytes()).hexdigest()==entry['after_sha256'],entry['file']
progress=json.loads((B/'progress.json').read_text(encoding='utf-8'))
finished=sum(p['status']=='complete' for p in progress['projects'])
assert finished==35
message=f'''# Delivered: LLM_Generated_Helper / Practice Journal

Applied to `{manifest['project']}`. Family 44013f102ff1. All 93 delivered file hashes verified again in the original folder. Nine course guides, 6,355 words, 64 checked local course links, five visually reviewed screenshots. 140 distinct passing checks: 120 Node, 14 actual journal browser workflows, six desktop renderer checks with a mocked preload bridge. Four supplemental clean-copy/setup groups passed; the repeated 120 tests are not added again.

Canonical data and real Electron userData were not used. No actual audio, native Electron, provider requests, OS encryption or Windows installer were tested. Existing desktop dependency versions were retained. A single-owner local JSON store, global revision, bounded data/activity, explicit recovery, and absence of durable creation receipts remain documented limitations.

Both source workflows are delivered: dependency-free Practice Journal with four CRUD resources and robust update/review behavior; existing desktop settings/IPC repairs with explicit credentials, revisions, cancellation and visible errors. Preserved 27 original code/documentation snapshots. Updated root and existing documentation to route to the new course, with the earlier alternative specification labeled historical.

Final evidence: results.json, browser-03/results.json, renderer-02/results.json, clean-01/results.json and ../../deliveries/44013f102ff1.json. The two earlier journal runs stopped on incorrect test wording; browser-03 passed all workflows. After clean-copy checks, the desktop textarea layout and stale success-note behavior were corrected and rechecked in renderer-02, then syntax checked. Do not rerun one-shot preservation/finalization generators or deliver again.

Overall progress: {finished}/{progress['total']} eligible families delivered; {progress['total']-finished} remain. The complete goal is still active, not finished. Update reports with render_progress_report.py and render_new_project_report.py. Requested report: astradocs/NEW_PROJECTS_CHANGE_REPORT.md.
'''
(C/'DELIVERED.md').write_text(message,encoding='utf-8')
(C/'CURRENT_CHECKPOINT.md').write_text(message,encoding='utf-8')
print(json.dumps({'canonicalFilesVerified':len(manifest['files']),'delivered':finished,'remaining':progress['total']-finished}),flush=True)
