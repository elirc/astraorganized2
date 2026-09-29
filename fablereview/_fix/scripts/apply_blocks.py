import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fable_edit as fe


def apply(items):
    for slug, prefix, heading, body in items:
        p = fe.chapter(slug, prefix)
        t, _, _ = fe.read(p)
        if '```' in t:
            print('SKIP (already has block)', slug, prefix)
            continue
        has_h2 = re.search(r'^## ', t, re.M) is not None
        if has_h2:
            changed = fe.append_section(slug, prefix, heading, body, before='## ')
        else:
            changed = fe.append_section(slug, prefix, heading, body)
        t2, _, _ = fe.read(p)
        print(('OK  ' if changed else 'NOCHANGE'), slug, prefix, os.path.basename(p),
              'blocks=', t2.count('```') // 2, '(after intro)' if has_h2 else '(end)')


if __name__ == '__main__':
    apply(json.load(open(sys.argv[1], encoding='utf-8')))
