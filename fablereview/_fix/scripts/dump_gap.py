import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fable_edit as fe

slug = sys.argv[1]
chs = sys.argv[2].split(',')
nlines = int(sys.argv[3]) if len(sys.argv) > 3 else 25
root = fe.REG[slug]['abs']
print('=== SLUG', slug, '| ROOT', root)
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('node_modules', '.git', 'astraupskill', 'dist', 'build', '.next', 'obj', 'bin', 'venv', '.venv', '__pycache__')]
    if dirpath[len(root):].count(os.sep) > 2:
        dirnames[:] = []
    for f in filenames:
        if f in ('package.json',):
            try:
                d = json.load(open(os.path.join(dirpath, f), encoding='utf-8-sig'))
            except Exception:
                continue
            print('--- pkg:', os.path.relpath(os.path.join(dirpath, f), root), json.dumps(d.get('scripts', {})))
        elif f in ('pytest.ini', 'pyproject.toml', 'pom.xml', 'build.gradle', 'requirements.txt') or f.endswith('.csproj') or f.endswith('.sln'):
            print('--- build file:', os.path.relpath(os.path.join(dirpath, f), root))
for ch in chs:
    p = fe.chapter(slug, ch)
    t, _, _ = fe.read(p)
    lines = t.split('\n')
    print('\n=== CHAPTER', os.path.basename(p), len(lines), 'lines')
    print('HEADINGS:', [l for l in lines if l.startswith('#')])
    print('--- first', nlines, 'lines ---')
    print('\n'.join(lines[:nlines]))
    paths = sorted(set(re.findall(r'[\w./\\-]+\.(?:ts|tsx|js|jsx|mjs|cjs|py|java|cs|razor|sql)', t)))
    print('--- referenced files:', paths[:40])
