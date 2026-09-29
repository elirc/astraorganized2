"""Aggregate reviewer JSONL lines + Fable's template-smell metrics into SCOREBOARD.md and scoreboard.json."""
import json, glob, os, io, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
reg = {r['slug']: r for r in json.load(open(os.path.join(ROOT, 'registry.json')))}
smell = json.load(open(os.path.join(HERE, 'fable-template-smell.json')))['per_course']

rows = {}
for f in sorted(glob.glob(os.path.join(HERE, 'B*.jsonl'))):
    batch = os.path.basename(f)[:-6]
    for line in io.open(f, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        try:
            j = json.loads(line)
        except Exception as e:
            print('BAD LINE in', batch, ':', line[:120], e)
            continue
        j['batch'] = batch
        rows[j['slug']] = j  # last write wins

missing = [s for s in reg if s not in rows]
extra = [s for s in rows if s not in reg]
print(f'reviews: {len(rows)} / {len(reg)}  missing={len(missing)} extra={extra}')
if missing:
    print('MISSING:', missing)

DIMS = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']
for s, j in rows.items():
    sc = j.get('scores') or {}
    vals = [sc.get(d) for d in DIMS if isinstance(sc.get(d), (int, float))]
    j['avg_calc'] = round(sum(vals) / len(vals), 2) if vals else None
    j['review_file'] = f'reviews/{s}.md'
    j['exists_review'] = os.path.exists(os.path.join(ROOT, 'reviews', s + '.md'))
    j['shared_pct'] = smell.get(s, {}).get('shared_pct')
    j['words'] = smell.get(s, {}).get('words')
    j['wave'] = reg[s]['wave'] if s in reg else j.get('wave')
    j['name'] = reg[s]['name'] if s in reg else j.get('name')
    # Fable normalization: the rubric's verdict thresholds are a floor; the stricter of reviewer verdict and rule wins.
    sc = j.get('scores') or {}
    m = min(sc.values()) if sc else 5
    a = j['avg_calc'] or 0
    rule = 'REWORK' if (a < 3.0 or m == 1 or sc.get('D1', 5) <= 2 or sc.get('D6', 5) <= 2) else ('IMPROVE' if (a < 4.0 or m == 2) else 'KEEP')
    order = {'KEEP': 0, 'IMPROVE': 1, 'REWORK': 2}
    j['rule_verdict'] = rule
    j['fable_verdict'] = max([j.get('verdict', 'KEEP'), rule], key=lambda v: order.get(v, 0))

json.dump(rows, open(os.path.join(ROOT, 'scoreboard.json'), 'w'), indent=1)

verdicts = Counter(j.get('fable_verdict') for j in rows.values())
reviewer_verdicts = Counter(j.get('verdict') for j in rows.values())
roles = Counter(j.get('role') for j in rows.values())
by_wave = defaultdict(list)
for j in rows.values():
    by_wave[j['wave']].append(j)

out = []
out.append('# Scoreboard: every Astra-changed project, scored by the review fleet\n')
out.append(f'{len(rows)} of {len(reg)} projects reviewed. Scores are 1-5 per dimension from `RUBRIC.md`; avg is the mean of D1-D8.\n')
out.append('| Verdict | Count |\n|---|---:|')
for k, v in verdicts.most_common():
    out.append(f'| {k} | {v} |')
out.append('\n| Path role | Count |\n|---|---:|')
for k, v in roles.most_common():
    out.append(f'| {k} | {v} |')
out.append('')
for w in sorted(by_wave):
    xs = by_wave[w]
    avgs = [j['avg_calc'] for j in xs if j['avg_calc'] is not None]
    dimmeans = {d: round(statistics.mean([j['scores'][d] for j in xs if isinstance((j.get('scores') or {}).get(d), (int, float))]), 2) for d in DIMS}
    out.append(f'**Wave {w}** ({len(xs)} projects): mean avg {round(statistics.mean(avgs), 2)}, median {round(statistics.median(avgs), 2)}. Dimension means: ' + ', '.join(f'{d}={v}' for d, v in dimmeans.items()) + '\n')

out.append('\n## All projects (sorted by avg, then name)\n')
out.append('| # | Project | Wave | Batch | ' + ' | '.join(DIMS) + ' | Avg | Verdict (final) | Role | Shared para % | Words | Top fix |')
out.append('|---:|---|---:|---|' + '---|' * len(DIMS) + '---:|---|---|---:|---:|---|')
srt = sorted(rows.values(), key=lambda j: (-(j['avg_calc'] or 0), j['name']))
for i, j in enumerate(srt, 1):
    sc = j.get('scores') or {}
    out.append(f"| {i} | [{j['name']}]({j['review_file']}) | {j['wave']} | {j['batch']} | " + ' | '.join(str(sc.get(d, '')) for d in DIMS) +
               f" | {j['avg_calc']} | {j.get('fable_verdict')}{'*' if j.get('fable_verdict')!=j.get('verdict') else ''} | {j.get('role')} | {j.get('shared_pct')} | {j.get('words')} | {(j.get('top_fix') or '').replace('|', '/')} |")

io.open(os.path.join(ROOT, 'SCOREBOARD.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('wrote SCOREBOARD.md')
print('verdicts', dict(verdicts), 'roles', dict(roles))
