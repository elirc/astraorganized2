"""Astra-only guarded delivery of one reviewed campaign project."""
from pathlib import Path
import json,hashlib,subprocess,sys
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
B=HERE.parent
pid=sys.argv[1]
policy=json.loads((HERE/'campaign.json').read_text())
matches=[(batch,row) for batch in policy['batches'] for row in batch['projects'] if row['id']==pid]
assert len(matches)==1,'Not in this campaign'
batch,row=matches[0]
parts=Path(row['path']).parts
assert not any(s.casefold() in policy['protectedNameParts'] for s in parts)
assert not any(s in row['path'].casefold() for s in policy['protectedSubstrings'])
review=json.loads((HERE/f'{pid}-astra-review.json').read_text())
assert review['approved'] is True and review['id']==pid
assert review.get('sourceReview') and review.get('teachingReview') and review.get('testReview')
assert hashlib.sha256((B/'specs'/f'{pid}.json').read_bytes()).hexdigest()==review['specSHA256'],'Spec changed after review'
for name,expected in review['evidenceHashes'].items():
    evidence=(B/name).resolve()
    assert evidence.is_relative_to((B/'checks'/pid).resolve())
    assert hashlib.sha256(evidence.read_bytes()).hexdigest()==expected,'Check evidence changed after review'
stage=B/'stage'/pid
for name,expected in review['fileHashes'].items():
    full=Path(row['path'])/name
    assert not any(s.casefold() in policy['protectedNameParts'] for s in full.parts),'Protected nested project'
    assert not any(s in str(full).casefold() for s in policy['protectedSubstrings']),'Protected applybot variant'
    path=(stage/name).resolve()
    assert path.is_relative_to(stage.resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Changed after review: {name}'
spec=json.loads((B/'specs'/f'{pid}.json').read_text())
assert isinstance(spec['summary'],list) and spec['summary'] and all(isinstance(s,str) for s in spec['summary'])
assert isinstance(spec['limits'],list)
assert isinstance(spec['changedFiles'],list) and len(spec['changedFiles'])==len(set(spec['changedFiles']))
chapters=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
assert set(review['fileHashes'])==set(spec['changedFiles'])|{'astraupskill/'+n for n in chapters}
subprocess.run([sys.executable,'-X','utf8',str(B/'review_handoff.py'),pid],check=True)
subprocess.run([sys.executable,'-X','utf8',str(B/'prepare_delivery.py'),row['path']],check=True)
subprocess.run([sys.executable,'-X','utf8',str(B/'apply_delivery.py'),pid],check=True)
row['status']='complete';row['completedAt']=datetime.now(timezone.utc).isoformat()
batch['status']='complete' if all(r['status']=='complete' for r in batch['projects']) else 'in_progress'
(HERE/'campaign.json').write_text(json.dumps(policy,indent=2),encoding='utf-8')
print(json.dumps({'batch':batch['batch'],'project':row['path'],'delivered':True,'protectedScopeChecked':True}))
