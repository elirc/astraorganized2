"""Shared fixes for the JS1 Express in-memory family (batch03 style courses)."""
import os, re, json
import fable_edit as fe

PINS_JS = {"@vitejs/plugin-react": "^6.1.1", "concurrently": "^9.2.1", "cors": "^2.8.6", "express": "^4.22.2", "react": "^18.3.1", "react-dom": "^18.3.1", "vite": "^8.2.2"}
PINS_TS = {**PINS_JS, "dotenv": "^16.6.1", "pg": "^8.23.0", "@types/cors": "^2.8.19", "@types/express": "^4.17.23", "@types/node": "^22.19.0", "@types/pg": "^8.15.5", "@types/react": "^18.3.27", "@types/react-dom": "^18.3.7", "tsx": "^4.23.13", "typescript": "^5.9.3"}


def pin(project, pins=PINS_JS):
    p = os.path.join(project, 'package.json')
    pj = json.load(open(p, encoding='utf-8'))
    for sec in ('dependencies', 'devDependencies'):
        for k in pj.get(sec, {}):
            pj[sec][k] = pins.get(k, pj[sec][k])
    open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')


def remove_unused_helpers(server_js, names=('isText', 'whole', 'realDate')):
    """Delete one-line helper definitions that have no call sites."""
    removed = []
    def fn(t):
        nonlocal removed
        out = t
        for n in names:
            calls = len(re.findall(r'\b' + n + r'\(', out))
            if calls == 1:  # definition only
                out2 = re.sub(r'^function ' + n + r'\(.*\n', '', out, count=1, flags=re.M)
                if out2 != out:
                    removed.append(n)
                    out = out2
        return out
    fe.rw(server_js, fn)
    return removed


def drop_blocks(path, blocks):
    """Remove exact multi-line blocks (unreachable legacy guards)."""
    def fn(t):
        for b in blocks:
            assert b in t, 'block not found: ' + b[:60]
            t = t.replace(b, '', 1)
        return t
    fe.rw(path, fn)


def rename_lesson_fields(app_jsx):
    """lesson-field-N -> field-<name> from the bound form key; also updates htmlFor."""
    t, crlf, bom = fe.read(app_jsx)
    mapping = {}
    for m in re.finditer(r'id="(lesson-field-\d+)"[^>]*?value=\{form\.(\w+)\}', t):
        mapping[m.group(1)] = 'field-' + re.sub(r'([a-z])([A-Z])', r'\1-\2', m.group(2)).lower()
    for old, new in mapping.items():
        t = t.replace(old, new)
    fe.write(app_jsx, t, crlf, bom)
    return mapping


def prereqs(slug, text):
    fe.rw(fe.chapter(slug, 'README'), lambda t: fe.replace_section(t, r'Prerequisites', text) or t)


def exercises(slug, bodies):
    """bodies: dict {1: text, 2: text, ...}: replaces the generic paragraph under each exercise prompt line."""
    p = fe.chapter(slug, '05')
    def fn(t):
        for n, body in bodies.items():
            m = re.search(r'^## Exercise ' + str(n) + r' .*$\n\n(.+?)\n\n(.+?)\n\n', t, re.M | re.S)
            if not m:
                continue
            prompt, generic = m.group(1), m.group(2)
            if generic.startswith('#'):
                continue
            t = t[:m.start(2)] + body.strip() + t[m.end(2):]
        return t
    fe.rw(p, fn)


def limits(slug, text):
    fe.rw(fe.chapter(slug, 'VERIFICATION'), lambda t: fe.replace_section(t, r'Limits', text) or t)


def dedupe_fixture(slug):
    """Keep the worked-fixture paragraph in 03 and VERIFICATION; replace the copies in 01/04/05/06/07 with a link.
    Also replace the duplicated setup fence in 04 and VERIFICATION with a link to the README."""
    v, _, _ = fe.read(fe.chapter(slug, 'VERIFICATION'))
    m = re.search(r'^## Tested behavior\s*\n\n(.+?)\n\n', v, re.M | re.S)
    fixture = m.group(1).strip() if m else None
    changed = []
    if fixture:
        for pre in ('01', '04', '05', '06', '07'):
            try:
                p = fe.chapter(slug, pre)
            except FileNotFoundError:
                continue
            def fn(t):
                if fixture not in t:
                    return t
                return t.replace(fixture, 'The worked fixture is defined once in [chapter 3](03-WORKED-CHANGE.md#predict-this-example); use those exact values here.', 1)
            if fe.rw(p, fn):
                changed.append(pre)
    # setup fences
    for pre in ('04', 'VERIFICATION'):
        p = fe.chapter(slug, pre)
        def fn2(t):
            return re.sub(r'From the project root, use Node\.js and npm:\n\n```powershell\n.*?```\n\n(.*?)\n\n', 'Setup commands are in the [course README](README.md#start-the-project); run them once, then continue here.\n\n', t, count=1, flags=re.S)
        if fe.rw(p, fn2):
            changed.append(pre + ':setup')
    return changed


def bump_verification_count(slug, delivered, added, file):
    fe.rw(fe.chapter(slug, 'VERIFICATION'), lambda t: re.sub(r'Automated test cases: \*\*' + str(delivered) + r'\*\*\.', f'Automated test cases: **{delivered}** delivered by Astra, plus **{added}** added in the fix pass, for {delivered + added} in `{file}`.', t, count=1))
