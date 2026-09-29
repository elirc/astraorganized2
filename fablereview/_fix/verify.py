"""Fable's gate checks after the fix program. Read-only. Usage: python verify.py [--json out.json]

Checks per project (all 153):
  leaked      : sentences naming other projects / wrong-stack environment claims (wave 1)
  agentlang   : agent-process language in course text (manifest/baseline/frozen/root agent)
  codeblocks  : chapters 03,04,06,07 each have >= 1 fenced code block
  chapters    : each 0N-*.md H1 matches its filename topic and body does not open with the next chapter's topic
  tracelab    : 07-TRACE-LAB.md does not repeat one paragraph 3+ times
  reviewpara  : 06-SOLUTIONS-AND-REVIEW.md does not repeat one 'Review:' paragraph under every exercise
  variations  : 03-WORKED-CHANGE.md 'variations' section has concrete content (>= 3 list items or >= 120 words after heading)
  bom         : no UTF-8 BOM after byte 0 in server/*.js, src/**/*.js
  glossary    : README or a chapter has a Glossary/Prerequisites section (wave 2 expectation)
  report      : _fix/reports/<slug>.md exists
"""
import json, os, re, io, sys, glob, hashlib
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
reg = json.load(open(os.path.join(ROOT, 'registry.json')))
SB = json.load(open(os.path.join(ROOT, 'scoreboard.json')))
for _r in reg:
    _sb = SB.get(_r['slug'])
    if _sb and _sb.get('stack'):
        _r['stack'] = _sb['stack']

OTHER_NAMES = ['Poll Studio', 'Kanban Flow', 'Questboard', 'DevDeck', 'Live Chat', 'Legal Case Tracker', 'Recipe Studio', 'Org Explorer']
TOPIC = {'01': 'CODEBASE', '02': 'CONCEPT', '03': 'WORKED', '04': 'TEST', '05': 'PRACTICE', '06': 'SOLUTION', '07': 'TRACE'}
NEXT_OPEN = {'01': r'^\s*(concepts?|the concepts)', '02': r'^\s*the worked change', '03': r'^\s*testing and debugging', '04': r'^\s*(practice|exercises)', '05': r'^\s*(solutions|the solutions)', '06': r'^\s*trace lab'}


def read(p):
    return io.open(p, encoding='utf-8', errors='replace').read()


def paras(t):
    return [re.sub(r'\s+', ' ', p.strip()) for p in re.split(r'\n\s*\n', t) if len(p.split()) >= 20]


def check(r):
    c = os.path.join(r['abs'], 'astraupskill')
    out = {}
    files = {os.path.basename(f)[:2]: f for f in glob.glob(os.path.join(c, '0*.md')) if re.match(r'^\d\d-', os.path.basename(f))}
    alltxt = {os.path.basename(f): read(f) for f in glob.glob(os.path.join(c, '*.md'))}
    joined = '\n'.join(alltxt.values())
    name = r['name'].split('/')[-1].lower().replace('-', ' ')
    # leaked names (wave 1 only) -- a project may legitimately name itself
    leaks = [n for n in OTHER_NAMES if n.lower() not in name and n in joined]
    # wrong-stack env claims
    stack = ' '.join(r.get('stack') or [])
    has_pg = any(k in stack for k in ('postgres', 'pg', 'knex', 'prisma'))
    if r['wave'] == 1 and not has_pg and re.search(r'PostgreSQL 18|port 55439', joined):
        leaks.append('PostgreSQL claim without Postgres')
    out['leaked'] = leaks
    out['agentlang'] = sorted(set(m.group(0) for m in re.finditer(r'root agent|frozen (stage|manifest)|delivery preflight|baselines/<id>|changed-file manifest', joined)))
    out['codeblocks'] = {k: alltxt.get(os.path.basename(files[k]), '').count('```') // 2 for k in ('03', '04', '06', '07') if k in files}
    bad_ch = []
    for k, f in files.items():
        t = alltxt[os.path.basename(f)]
        h1 = (re.search(r'^#\s+(.+)$', t, re.M) or [None, ''])[1]
        body = re.sub(r'^#.*$', '', t, flags=re.M).strip()[:200]
        if k in TOPIC and TOPIC[k].lower() not in h1.lower() and TOPIC[k].lower() not in os.path.basename(f).lower():
            bad_ch.append(f'{k}: h1={h1[:40]}')
        if k in NEXT_OPEN and re.search(NEXT_OPEN[k], body, re.I):
            bad_ch.append(f'{k}: body opens with next chapter topic')
    out['chapters'] = bad_ch
    if '07' in files:
        cnt = Counter(paras(alltxt[os.path.basename(files['07'])]))
        out['tracelab'] = max(cnt.values()) if cnt else 0
    if '06' in files:
        rv = re.findall(r'\*?\*?Review:?\*?\*?\s*(.{40,200})', alltxt[os.path.basename(files['06'])])
        cnt = Counter(x.strip()[:120] for x in rv)
        out['reviewpara'] = max(cnt.values()) if cnt else 0
    if '03' in files:
        t = alltxt[os.path.basename(files['03'])]
        m = re.search(r'^#+\s.*variation.*$', t, re.I | re.M)
        if m:
            seg = t[m.end():]
            nxt = re.search(r'^#+\s', seg, re.M)
            seg = seg[:nxt.start()] if nxt else seg
            out['variations'] = dict(items=len(re.findall(r'^\s*(\d+\.|-|\*)\s', seg, re.M)), words=len(seg.split()))
    boms = []
    for f in glob.glob(os.path.join(r['abs'], 'server', '*.js')) + glob.glob(os.path.join(r['abs'], 'src', '**', '*.js'), recursive=True):
        b = open(f, 'rb').read(4096)
        if b'\xef\xbb\xbf' in b[1:]:
            boms.append(os.path.relpath(f, r['abs']))
    out['bom'] = boms
    out['glossary'] = bool(re.search(r'^#+\s*(glossary|prerequisites|vocabulary)', joined, re.I | re.M))
    out['report'] = os.path.exists(os.path.join(HERE, 'reports', r['slug'] + '.md'))
    # template smell: shared paragraphs measured across wave later
    out['_paras'] = [hashlib.md5(p.encode()).hexdigest() for p in paras(joined)]
    return out


res = {}
for r in reg:
    if os.path.isdir(os.path.join(r['abs'], 'astraupskill')):
        res[r['slug']] = check(r)
# shared-paragraph % within wave 1
idx = defaultdict(set)
for s, o in res.items():
    for h in o['_paras']:
        idx[h].add(s)
for s, o in res.items():
    hs = o.pop('_paras')
    o['shared_pct'] = round(100 * sum(1 for h in hs if len(idx[h]) > 1) / max(1, len(hs)), 1)

fails = defaultdict(list)
for s, o in res.items():
    w = next(r['wave'] for r in reg if r['slug'] == s)
    if o['leaked']: fails['leaked'].append(s)
    if o['agentlang']: fails['agentlang'].append(s)
    if any(v == 0 for v in o['codeblocks'].values()): fails['codeblocks'].append(s)
    if o['chapters']: fails['chapters'].append(s)
    if o.get('tracelab', 0) >= 3: fails['tracelab'].append(s)
    if o.get('reviewpara', 0) >= 3: fails['reviewpara'].append(s)
    v = o.get('variations')
    if w == 1 and v is not None and v['items'] < 3 and v['words'] < 120: fails['variations'].append(s)
    if o['bom']: fails['bom'].append(s)
    if w == 2 and not o['glossary']: fails['glossary'].append(s)
    if not o['report']: fails['report'].append(s)
    if w == 1 and o['shared_pct'] > 40: fails['shared>40'].append(s)

print(f'projects checked: {len(res)}')
for k, v in sorted(fails.items()):
    print(f'{k:12s} {len(v):4d}  ' + ', '.join(v[:12]) + (' ...' if len(v) > 12 else ''))
import statistics
w1 = [o['shared_pct'] for s, o in res.items() if next(r['wave'] for r in reg if r['slug'] == s) == 1]
print('wave-1 shared paragraph % median:', statistics.median(w1) if w1 else None)
if '--json' in sys.argv:
    json.dump(dict(results=res, fails=fails), open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
