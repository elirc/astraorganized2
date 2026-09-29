from pathlib import Path
import json, hashlib, re
BASE = Path(__file__).resolve().parent
DESKTOP = BASE.parents[2]
manifest = json.loads((BASE/'delivery-manifest.json').read_text())
summary = json.loads((BASE/'delivery-summary.json').read_text())
courses = json.loads((BASE/'courses.json').read_text())
for item in manifest:
    target = DESKTOP/item['project']/item['file']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['after_sha256'], str(target)
for row in summary:
    folder = DESKTOP/row['project']/'astraupskill'
    for file in folder.glob('*.md'):
        text = re.sub(r'```.*?```', '', file.read_text(encoding='utf-8'), flags=re.S)
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' not in link:
                assert (file.parent/link.split('#')[0]).exists(), (file, link)
lines = ['# Ten projects implemented', '', 'Completed 2026-09-08. The changes and learning courses are installed in the actual Desktop project folders below. Work through them in this order.', '', '| Order | Project and learning course | Implemented improvement | Test cases |', '|---|---|---|---:|']
improvements = [
    'Persistent one-level undo, including reload and failed-write handling.',
    'Case-insensitive duplicate-email validation that supports editing your own record.',
    'Deadline-based countdown, accurate pause/resume and single completion logging.',
    'Validated expense editing with stable identity and persisted totals.',
    'Saved shopping quantities, keyboard-editable controls and consistent clipboard output.',
    'Validated application JSON export/import with atomic replacement and failure feedback.',
    'CRUD regression coverage, bounded identifiers/titles and unchanged overdue-date editing.',
    'Quoted/multiline CSV parsing, complete batch validation and transactional imports.',
    'Correct category aggregates, month/date filtering and amount validation.',
    'Owner-scoped updates, strict nested validation and transaction rollback coverage.',
]
for i, (row, improvement) in enumerate(zip(summary, improvements), 1):
    link = '../../' + row['project'] + '/astraupskill/README.md'
    lines.append(f'| {i} | [{row["project"]}]({link}) | {improvement} | {row["test_cases"]} |')
lines += ['', '## Learning material', '', f'Each project has an `astraupskill` folder linked from its root README. Together the courses contain {sum(x["learning_files"] for x in summary)} Markdown files and approximately {sum(x["learning_words"] for x in summary):,} words, including source and test examples.', '', 'Each course includes prerequisites and setup, a linked codebase map, concepts explained from first principles, worked changes with actual code, test and debugging guidance, guided and independent exercises, solutions and a review rubric, and an honest verification record. Existing Fable/tutorial material is preserved. The exercises are follow-up learning tasks; they are clearly distinguished from implemented behavior.', '', '## Verification', '', f'- {sum(x["test_cases"] or 0 for x in summary)} automated test cases passed across the ten project suites.', '- All six relevant Vite client builds passed; Recipeweb lint and both Recipe Manager TypeScript checks passed.', '- Six real Chromium interaction checks passed, covering persistence, validation, timing, keyboard quantity editing, clipboard output and backup import/export.', '- The four backend suites exercised real HTTP/database behavior against an isolated PostgreSQL 18.1 test instance, including ownership denial and late transaction rollback.', '- Every delivered file was checked against its staged SHA-256 after application; all learning-document links were checked in the actual project folders.', '', 'Verification ran on isolated working copies using Node 22.16.0 and a shared dependency harness; Recipeweb additionally used its own dependency tree. Daybook passed 89 tests in its full run; the remaining form test passed a focused retry with a 120-second limit. The isolated Vitest harness also needed a longer worker startup allowance. Assertions were unchanged. Byte-identical verified source was then applied to the originals. The original projects still require their documented local dependency/environment setup. These checks do not certify all unrelated functionality or production readiness.', '', '## Change evidence', '', '- [Per-project delivery summary](implementation/delivery-summary.json)', '- [Exact delivered file manifest](implementation/delivery-manifest.json)', '- [Automated check results](implementation/checks.json)', '- [Browser interaction results](implementation/browser-checks.json)', '- [Source changes](implementation/source-changes.diff)', '', 'Original versions of changed files are retained locally in `implementation/backups`. Project databases, personal records, existing dependency trees and unrelated source files were not replaced.', '']
report = BASE.parent/'TEN_PROJECTS_IMPLEMENTED.md'
report.write_text('\n'.join(lines), encoding='utf-8')
readme = BASE.parent/'README.md'
text = readme.read_text(encoding='utf-8')
entry = '\n[Completed implementations and learning courses for the first ten projects](TEN_PROJECTS_IMPLEMENTED.md).\n'
if 'TEN_PROJECTS_IMPLEMENTED.md' not in text:
    position = text.index('\n') + 1
    readme.write_text(text[:position] + entry + text[position:], encoding='utf-8')
print(json.dumps({'verified_original_files': len(manifest), 'report': str(report), 'projects': len(summary)}))
