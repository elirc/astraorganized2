"""Re-sync the 'Executable examples' fenced block in every wave-1 03-WORKED-CHANGE.md with the current (Prettier-formatted) test file."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fable_edit as fe

changed, skipped = [], []
for slug, r in fe.REG.items():
    if r['wave'] != 1:
        continue
    try:
        p = fe.chapter(slug, '03')
    except FileNotFoundError:
        skipped.append((slug, 'no 03')); continue
    t, crlf, bom = fe.read(p)
    m = re.search(r'^## Executable examples\s*\n\n(.*?)\n\n```(\w+)\n(.*?)\n```', t, re.S | re.M)
    if not m:
        skipped.append((slug, 'no executable examples block')); continue
    link = re.search(r'\]\(\.\./([^)]+)\)', m.group(1))
    if not link:
        skipped.append((slug, 'no link')); continue
    tf = os.path.join(r['abs'], link.group(1).replace('/', os.sep))
    if not os.path.isfile(tf):
        skipped.append((slug, 'missing ' + link.group(1))); continue
    code = open(tf, encoding='utf-8-sig').read().replace('\r\n', '\n').rstrip('\n')
    if code == m.group(3):
        continue
    new = t[:m.start(3)] + code + t[m.end(3):]
    fe.write(p, new, crlf, bom)
    changed.append(slug)
print('re-synced', len(changed), 'courses:', changed)
print('skipped', len(skipped), ':', skipped[:10])
json.dump(dict(changed=changed, skipped=skipped), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_examples.json'), 'w'), indent=1)
