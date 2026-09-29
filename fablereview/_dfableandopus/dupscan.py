"""Duplication + size + citation scan over every <project>/dfableandopus folder.
Usage: python dupscan.py [--json out.json]
Reports: per project word counts per file, missing files, share of paragraphs (>= 12 words) that also appear in
another project's folder, and a sample of cited path:line references that do not resolve on disk."""
import json, os, re, sys, glob, collections, hashlib
ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, '..', 'registry.json'), encoding='utf-8-sig'))
FILES = ['README.md', '01-INTERVIEW-QUESTIONS.md', '02-STORIES-AND-RESUME.md', '03-CODE-READING-DRILL.md', '04-TAKE-HOME.md', '05-SYSTEM-DESIGN-FOLLOWUPS.md', '06-FLASHCARDS.md']
norm = lambda p: re.sub(r'\s+', ' ', re.sub(r'`[^`]*`', '`', p)).strip().lower()
paras = collections.defaultdict(set)   # hash -> slugs
per = {}
for r in reg:
    d = os.path.join(r['abs'], 'dfableandopus')
    if not os.path.isdir(d):
        per[r['slug']] = {'missing': FILES}; continue
    info = {'missing': [], 'words': {}, 'bom': [], 'badcites': [], 'ncites': 0}
    hashes = set()
    for f in FILES:
        p = os.path.join(d, f)
        if not os.path.exists(p): info['missing'].append(f); continue
        raw = open(p, 'rb').read()
        if raw.startswith(b'\xef\xbb\xbf'): info['bom'].append(f)
        t = raw.decode('utf-8', 'replace')
        info['words'][f] = len(t.split())
        for para in re.split(r'\n\s*\n', t):
            if para.lstrip().startswith(('```', '|', '#', '<details', '</details')): continue
            if len(para.split()) >= 12: hashes.add(hashlib.md5(norm(para).encode()).hexdigest())
        for m in re.finditer(r'`([\w./\\-]+\.(?:ts|tsx|js|jsx|mjs|cjs|cs|java|py|sql|prisma)):(\d+)', t):
            info['ncites'] += 1
            path = os.path.join(r['abs'], m.group(1).replace('\\', '/'))
            if not os.path.exists(path):
                # bare filename: accept if it names exactly one file in the project (outside node_modules), but count it as a format defect
                cands = [c for c in glob.glob(os.path.join(r['abs'], '**', os.path.basename(m.group(1))), recursive=True) if 'node_modules' not in c]
                if len(cands) == 1:
                    path = cands[0]; info['barecites'] = info.get('barecites', 0) + 1
                else:
                    if len(info['badcites']) < 5: info['badcites'].append(m.group(0))
                    continue
            if True:
                n = int(m.group(2))
                if n > sum(1 for _ in open(path, 'rb')) and len(info['badcites']) < 5: info['badcites'].append(m.group(0) + ' (beyond EOF)')
    info['hashes'] = hashes
    per[r['slug']] = info
for s, i in per.items():
    for h in i.get('hashes', ()): paras[h].add(s)
summary = {}
for s, i in per.items():
    hs = i.get('hashes', set())
    shared = sum(1 for h in hs if len(paras[h]) > 1)
    summary[s] = {'missing': i.get('missing', []), 'words': i.get('words', {}), 'bom': i.get('bom', []),
                  'shared_pct': round(100 * shared / len(hs), 1) if hs else None, 'badcites': i.get('badcites', []), 'ncites': i.get('ncites', 0), 'barecites': i.get('barecites', 0)}
done = [s for s, v in summary.items() if not v['missing']]
print(f'folders complete: {len(done)}/{len(summary)}')
bad = {s: v for s, v in summary.items() if v['missing'] and v['missing'] != FILES}
if bad: print('partial folders:', {s: v['missing'] for s, v in bad.items()})
hi = sorted(((v['shared_pct'], s) for s, v in summary.items() if v['shared_pct'] is not None and v['shared_pct'] > 10), reverse=True)
print('shared paragraphs > 10%:', hi[:20])
bc = {s: v['badcites'] for s, v in summary.items() if v['badcites']}
print('unresolvable citations:', len(bc), dict(list(bc.items())[:8]))
bare = {s: v['barecites'] for s, v in summary.items() if v.get('barecites')}
print('bare-filename citations (format defect, resolved by basename):', bare)
small = {s: [f for f, w in v['words'].items() if w < {'README.md': 200, '01-INTERVIEW-QUESTIONS.md': 1200, '02-STORIES-AND-RESUME.md': 450, '03-CODE-READING-DRILL.md': 900, '04-TAKE-HOME.md': 550, '05-SYSTEM-DESIGN-FOLLOWUPS.md': 700, '06-FLASHCARDS.md': 350}[f]] for s, v in summary.items()}
small = {s: f for s, f in small.items() if f}
print('undersized files:', len(small), dict(list(small.items())[:10]))
boms = {s: v['bom'] for s, v in summary.items() if v['bom']}
if boms: print('BOM:', boms)
if '--json' in sys.argv: json.dump(summary, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
