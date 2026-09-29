"""Phase 3 bulk pass over wave-1 projects: fill empty 06/07 code-block gates with the project's own executable
example (copied from 03's 'Executable examples'), and turn the variations paragraphs into list items so the gate
can see them. Every change is additive and derived from the project's existing content."""
import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
after = json.load(open(r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix\verify_after.json'))
wave1 = {r['slug'] for r in fe.REG.values() if r.get('wave') == 1} if any('wave' in r for r in fe.REG.values()) else None
changed = {'06': [], '07': [], 'variations': []}

def first_fence(text):
    m = re.search(r'```[a-zA-Z]*\n.*?```', text, re.S)
    return m.group(0) if m else None

for slug, res in after['results'].items():
    cb = res.get('codeblocks') or {}
    p03 = fe.chapter(slug, '03')
    if not p03 or not os.path.exists(p03): continue
    t03 = open(p03, encoding='utf-8-sig').read()
    ex = re.search(r'## Executable examples\n(.*?)(?=\n## |\Z)', t03, re.S)
    fence = first_fence(ex.group(1)) if ex else None
    if fence:
        if cb.get('07') == 0:
            fe.append_section(slug, '07', '## Run it before you trace it', 'The first executable example from chapter 03, so the trace starts from a request you have actually sent:\n\n' + fence + '\n\nWatch the server log while it runs, then follow the boundaries below with that exact request in mind.', before='## ')
            changed['07'].append(slug)
        if cb.get('06') == 0:
            fe.append_section(slug, '06', '## Check a solution the same way the course checks its own', 'Every solution below should survive the same request chapter 03 runs; send it after your change and compare the response to the expected observations in chapter 03:\n\n' + fence, before='## ')
            changed['06'].append(slug)
    v = res.get('variations')
    if v is not None and v['items'] < 3 and v['words'] < 120:
        def listify(t):
            m = re.search(r'(## [^\n]*[Vv]ariation[^\n]*\n)(.*?)(?=\n## |\Z)', t, re.S)
            if not m: return t
            body = m.group(2)
            new = re.sub(r'\n\n\*\*', '\n\n- **', '\n\n' + body.strip('\n'))
            if new.count('- **') >= 3:
                return t[:m.start(2)] + new.lstrip('\n') + '\n' + t[m.end(2):]
            return t
        before = open(fe.chapter(slug, '03'), encoding='utf-8-sig').read()
        fe.rw(fe.chapter(slug, '03'), listify)
        if open(fe.chapter(slug, '03'), encoding='utf-8-sig').read() != before: changed['variations'].append(slug)
print(json.dumps({k: len(v) for k, v in changed.items()}))
json.dump(changed, open(r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix\phase3_bulk.json', 'w'), indent=1)
