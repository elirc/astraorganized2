"""Report actual deliveries from this assigned batch, without implying completion."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote, unquote
import json
import re
import sys

C = Path(__file__).resolve().parent
B = C.parent.parent
R = B.parent
sys.path.insert(0, str(B))
from report_evidence import check_summary
batch = sys.argv[1] if len(sys.argv) > 1 else '1'
assert batch in {'1', '2'}
if batch == '2':
    C = C.with_name(C.name + '-02')
target = R / 'astradocs' / ('LUNA_ASTRA_BATCH_REPORT.md' if batch == '1' else 'LUNA_ASTRA_BATCH_02_REPORT.md')
progress = json.loads((B / 'progress.json').read_text(encoding='utf-8'))
ids = ['676bcb38df2b', '52d78d4a92a2'] if batch == '1' else ['ee8b0b1a6855', '9e1958f807df']
complete = sum(row['status'] == 'complete' for row in progress['projects'])
lines = ['# Luna implementation and Astra review', '',
         'Updated ' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + '.', '',
         'Two Luna agents implement separate projects; an Astra agent reviews their plans, code, learning material and test evidence. Root applies reviewed deliveries sequentially and updates the shared reports.', '',
         f'**Collection: {complete} of {progress["total"]} eligible families delivered; {progress["total"] - complete} remain.**', '']
for pid in ids:
    row = next(row for row in progress['projects'] if row['id'] == pid)
    lines += ['## ' + row['path'], '']
    if row['status'] != 'complete':
        lines += ['Assigned and in progress; not counted as delivered.', '']
        review = C / (pid + '-review.md')
        if review.exists():
            review_url = '../astra-remaining-improvements/checks/' + C.name + '/' + review.name
            lines += [f'[Current Astra review notes]({review_url}).', '']
        continue
    m = json.loads((B / 'deliveries' / (pid + '.json')).read_text(encoding='utf-8'))
    assert m['status'] == 'delivered'
    review = C / (pid + '-review.md')
    assert review.is_file(), 'Astra review record required'
    lines += ['- ' + change for change in m['summary']]
    course = quote('../../' + row['path'] + '/astraupskill/README.md', safe='/+')
    evidence = '../astra-remaining-improvements/deliveries/' + pid + '.json'
    review_url = '../astra-remaining-improvements/checks/' + C.name + '/' + review.name
    lines += ['', f'**Learning:** {m["courseFiles"]} guides; {m["courseWords"]:,} words. [Start the course]({course}).', '',
              f'**Verification:** {check_summary(m)}. [Delivery evidence and limits]({evidence}).', '']
    lines += [f'[Astra review]({review_url}).', '']
lines += ['[All completed projects](FINISHED_PROJECTS_SUMMARY.md) · [Full change report](PROJECT_CHANGES_AND_COMPLETION_REPORT.md).', '']
text = '\n'.join(lines)
for url in re.findall(r'\]\(([^)]+)\)', text):
    assert (target.parent / unquote(url)).exists(), url
assert '\ufffd' not in text
target.write_text(text, encoding='utf-8')
print(json.dumps({'report': str(target), 'collectionDelivered': complete, 'linksVerified': True}))
