"""Record Astra's explicit review notes and bind approval to exact reviewed bytes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('id')
parser.add_argument('--source', required=True)
parser.add_argument('--teaching', required=True)
parser.add_argument('--tests', required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
base = here.parent
stage = base/'stage'/args.id
spec_path = base/'specs'/f'{args.id}.json'
spec = json.loads(spec_path.read_text(encoding='utf-8'))
result_path = (base/spec['checks']['resultsFile']).resolve()
assert result_path.is_relative_to((base/'checks'/args.id).resolve())
result = json.loads(result_path.read_text(encoding='utf-8'))
assert result['passed'] is True
assert isinstance(result['executedTests'], int) and result['executedTests'] > 0
chapters = ['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md',
            '04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md',
            '07-TRACE-LAB.md','VERIFICATION.md']
names = spec['changedFiles'] + ['astraupskill/'+name for name in chapters]
assert len(names) == len(set(names))
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
review = {
    'id': args.id, 'approved': True, 'reviewedAt': datetime.now(timezone.utc).isoformat(),
    'sourceReview': args.source, 'teachingReview': args.teaching, 'testReview': args.tests,
    'specSHA256': digest(spec_path),
    'fileHashes': {name: digest(stage/name) for name in names},
    'evidenceHashes': {
        p.relative_to(base).as_posix(): digest(p)
        for p in sorted((base/'checks'/args.id).iterdir()) if p.is_file()
    },
}
(here/f'{args.id}-astra-review.json').write_text(json.dumps(review, indent=2), encoding='utf-8')
print(json.dumps({'id': args.id, 'reviewedFiles': len(names), 'approved': True}))
