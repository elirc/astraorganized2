"""Fable's safe course-editing helpers (wave-1 and wave-2 authoring pass, 2026-09-17).

All writes preserve CRLF/LF and BOM state and go through temp-file + os.replace so a failed write cannot truncate a chapter.
"""
import io, os, re, json, tempfile, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DESK = r"C:\Users\Owner\Desktop"
REG = {r['slug']: r for r in json.load(open(os.path.join(ROOT, 'registry.json')))}


def read(p):
    raw = open(p, 'rb').read()
    return raw.decode('utf-8-sig').replace('\r\n', '\n'), (b'\r\n' in raw), raw.startswith(b'\xef\xbb\xbf')


def write(p, text, crlf, bom):
    out = text.replace('\n', '\r\n') if crlf else text
    data = (b'\xef\xbb\xbf' if bom else b'') + out.encode('utf-8')
    d = os.path.dirname(p)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.fable-', suffix='.tmp')
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
    assert os.path.getsize(tmp) == len(data) and len(data) > 0
    os.replace(tmp, p)


def rw(p, fn):
    """Apply fn(text)->text; returns True if changed."""
    t, crlf, bom = read(p)
    n = fn(t)
    if n != t:
        write(p, n, crlf, bom)
        return True
    return False


def course(slug):
    return os.path.join(REG[slug]['abs'], 'astraupskill')


def chapter(slug, prefix):
    c = course(slug)
    for f in os.listdir(c):
        if f.startswith(prefix) and f.endswith('.md'):
            return os.path.join(c, f)
    raise FileNotFoundError(prefix)


def replace_section(text, heading_regex, new_body, level='## '):
    """Replace the body under the first heading matching heading_regex (keeps the heading line), up to the next heading of same or higher level."""
    m = re.search(r'^(' + re.escape(level) + r'.*' + heading_regex + r'.*)$', text, re.M | re.I)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r'^#{1,' + str(len(level.strip())) + r'} ', text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return text[:m.end()] + '\n\n' + new_body.strip('\n') + '\n\n' + text[end:]


def set_boundaries(slug, boundaries):
    """boundaries: list of 6 (title, body) tuples. Rewrites '### Boundary N' blocks in 07 (batch04 family) or inserts a call-path section otherwise."""
    p = chapter(slug, '07')
    def fn(t):
        blocks = '\n\n'.join(f'### Boundary {i+1} — {title}\n\n{body.strip()}' for i, (title, body) in enumerate(boundaries))
        if re.search(r'^### Boundary 1', t, re.M):
            m = re.search(r'^## Trace the real call path.*$', t, re.M)
            nxt = re.search(r'^## ', t[m.end():], re.M)
            end = m.end() + nxt.start()
            return t[:m.end()] + '\n\n' + blocks + '\n\n' + t[end:]
        if '## Trace the real call path' in t:
            return replace_section(t, 'Trace the real call path', blocks)
        # batch01-03 family: insert before "## Expected observations" or "## Follow the implementation"
        anchor = re.search(r'^## (Expected observations|Follow the implementation|Follow the layers|Match validation)', t, re.M)
        sec = '## Trace the real call path\n\n' + blocks + '\n\n'
        if not anchor:
            # fall back to the first second-level heading after the title block
            anchor = re.search(r'^## ', t[200:], re.M)
            if anchor:
                pos = 200 + anchor.start()
                return t[:pos] + sec + t[pos:]
        return t[:anchor.start()] + sec + t[anchor.start():] if anchor else t.rstrip('\n') + '\n\n' + sec
    return rw(p, fn)


def set_reviews(slug, reviews):
    """Replace each '**Review:**' paragraph under ### Exercise N in 06 with reviews[N-1]."""
    p = chapter(slug, '06')
    def fn(t):
        parts = re.split(r'(^### Exercise \d+.*$)', t, flags=re.M)
        out = [parts[0]]
        for i in range(1, len(parts), 2):
            head, body = parts[i], parts[i + 1]
            n = int(re.search(r'\d+', head).group()) - 1
            if n < len(reviews) and reviews[n]:
                body = re.sub(r'^\*\*Review:\*\*.*$', '**Review:** ' + reviews[n].strip(), body, count=1, flags=re.M)
            out += [head, body]
        return ''.join(out)
    return rw(p, fn)


def set_variations(slug, body):
    p = chapter(slug, '03')
    return rw(p, lambda t: replace_section(t, r'variations', body) or t)


def set_excerpt(slug, intro, code, lang):
    """Replace the fenced block under '## Actual implementation excerpt' and its intro paragraph."""
    p = chapter(slug, '03')
    def fn(t):
        m = re.search(r'^## Actual implementation excerpt.*$', t, re.M)
        nxt = re.search(r'^## ', t[m.end():], re.M)
        end = m.end() + nxt.start()
        return t[:m.end()] + '\n\n' + intro.strip() + '\n\n```' + lang + '\n' + code.strip('\n') + '\n```\n\n' + t[end:]
    return rw(p, fn)


def add_exercise(slug, title, practice_body, solution_body, number=7):
    """Append an exercise to 05 (before Completion rubric) and its solution to 06 (before Review questions)."""
    p5, p6 = chapter(slug, '05'), chapter(slug, '06')
    h5 = f'## Exercise {number} — {title}'
    h6 = f'### Exercise {number} — {title}'
    def f5(t):
        if h5 in t:
            return re.sub(re.escape(h5) + r'.*?(?=^## )', h5 + '\n\n' + practice_body.strip() + '\n\n', t, flags=re.S | re.M)
        a = re.search(r'^## Completion rubric', t, re.M)
        sec = h5 + '\n\n' + practice_body.strip() + '\n\n'
        return t[:a.start()] + sec + t[a.start():] if a else t.rstrip('\n') + '\n\n' + sec
    def f6(t):
        if h6 in t:
            return re.sub(re.escape(h6) + r'.*?(?=^##)', h6 + '\n\n' + solution_body.strip() + '\n\n', t, flags=re.S | re.M)
        a = re.search(r'^## Review questions', t, re.M)
        sec = h6 + '\n\n' + solution_body.strip() + '\n\n'
        return t[:a.start()] + sec + t[a.start():] if a else t.rstrip('\n') + '\n\n' + sec
    return rw(p5, f5), rw(p6, f6)


def append_section(slug, prefix, heading, body, before=None):
    p = chapter(slug, prefix)
    def fn(t):
        if heading in t:
            return replace_section(t, re.escape(heading.lstrip('# ')), body, level=heading.split(' ')[0] + ' ') or t
        sec = heading + '\n\n' + body.strip() + '\n\n'
        if before:
            a = re.search(r'^' + re.escape(before), t, re.M)
            if a:
                return t[:a.start()] + sec + t[a.start():]
        return t.rstrip('\n') + '\n\n' + sec
    return rw(p, fn)


def sub(slug, prefix, old, new, count=0):
    p = chapter(slug, prefix)
    return rw(p, lambda t: t.replace(old, new) if count == 0 else t.replace(old, new, count))


def report(slug, batch, done, skipped, verification, consistency, notes=''):
    r = REG[slug]
    lines = [f"# {r['name']} — fix report ({batch})", '', f'Fable, {datetime.date.today().isoformat()}.', '', '## Done']
    lines += [f'- {d}' for d in done] or ['- (none)']
    lines += ['', '## Skipped'] + ([f'- {s}' for s in skipped] or ['- (none)'])
    lines += ['', '## Verification'] + ([f'- {v}' for v in verification] or ['- none run'])
    lines += ['', '## Course/code consistency check'] + ([f'- {c}' for c in consistency] or ['- (none)'])
    if notes:
        lines += ['', '## Notes', notes]
    os.makedirs(os.path.join(HERE, 'reports'), exist_ok=True)
    io.open(os.path.join(HERE, 'reports', slug + '.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    os.makedirs(os.path.join(HERE, 'progress'), exist_ok=True)
    with io.open(os.path.join(HERE, 'progress', batch + '.jsonl'), 'a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(dict(slug=slug, done=done, skipped=skipped, verified=('tests' if any('pass' in v.lower() for v in verification) else 'syntax' if verification else 'none'), notes=notes)) + '\n')
